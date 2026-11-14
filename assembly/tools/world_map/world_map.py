#!/usr/bin/env python3
"""Lossless extractor/importer for confirmed G-5510 world-map resources.

The four resources intentionally remain separate:

* a 40 x 8 ordered, directed AI city-neighbour candidate table;
* 40 fixed-point city world-coordinate pairs;
* a 72 x 72 static terrain-code grid used by weighted pathfinding; and
* the six-byte terrain-code-to-static-cost lookup table.

Nothing in this module calls the neighbour table a player movement or road
graph.  The importer writes a new ROM copy, never changes the canonical input,
never relocates a resource, never reorders neighbours, and never invents
reverse edges.
"""

from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import csv
import hashlib
import json
import struct
import sys
import tempfile
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


CANONICAL_SIZE = 1_048_576
CANONICAL_SHA256 = reference_value(__name__, 'CANONICAL_SHA256')
BUNDLE_FORMAT = "g5510-world-map-v1"

CITY_COUNT = 40
NEIGHBOR_RECORD_SIZE = 8
GRID_WIDTH = 72
GRID_HEIGHT = 72

NEIGHBOR_START = 0x0D4BE2
NEIGHBOR_END = 0x0D4D22
COORDINATE_START = 0x0D4ACA
COORDINATE_END = 0x0D4B6A
TERRAIN_START = 0x0EE5F0
TERRAIN_END = 0x0EFA30
TERRAIN_LUT_START = 0x00670A
TERRAIN_LUT_END = 0x006710

SCENARIO_189_DESCRIPTOR = 0x08AC04
CANONICAL_ASYMMETRIC_EDGES = ((20, 33), (34, 36))


class WorldMapError(ValueError):
    """Controlled validation failure for a world-map bundle."""


@dataclass(frozen=True)
class ResourceSpec:
    resource_id: str
    filename: str
    start: int
    end: int
    kind: str
    shape: str
    semantic_status: str
    evidence: str
    canonical_sha256: str

    @property
    def length(self) -> int:
        return self.end - self.start


RESOURCE_SPECS: tuple[ResourceSpec, ...] = (
    ResourceSpec(
        "ai_city_neighbor_candidates",
        "ai_city_neighbor_candidates.bin",
        NEIGHBOR_START,
        NEIGHBOR_END,
        "ordered_directed_u8_lists_ff_terminated_fixed_records",
        "40_records_x_8_bytes",
        "confirmed",
        (
            "12 static decoded/candidate BE32 references to biased base 0x0D4BDA; "
            "city_id<<3; signed-byte 0xFF termination; runtime execution at "
            "0x031A70..0x031AB4 and 0x033160..0x0331BA in defense_month"
        ),
        reference_value(__name__, 'field'),
    ),
    ResourceSpec(
        "city_world_coordinates",
        "city_world_coordinates.bin",
        COORDINATE_START,
        COORDINATE_END,
        "be16_fixed16_xy_pairs",
        "40_records_x_4_bytes",
        "confirmed",
        (
            "direct consumers in rendering, city hit testing, AI selection and "
            "path-grid setup; map drawing at 0x067ADC is runtime-confirmed"
        ),
        reference_value(__name__, 'field_2'),
    ),
    ResourceSpec(
        "weighted_path_terrain_codes",
        "weighted_path_terrain_codes.bin",
        TERRAIN_START,
        TERRAIN_END,
        "row_major_u8_terrain_codes",
        "72_rows_x_72_columns",
        "confirmed",
        (
            "0x006562 expands 5184 bytes through the six-byte LUT into FF0000; "
            "the 0x006518 path routine and 0x00664E frontier loop perform weighted "
            "wavefront pathfinding; all are runtime-confirmed"
        ),
        reference_value(__name__, 'field_3'),
    ),
    ResourceSpec(
        "terrain_code_static_cost_lut",
        "terrain_code_static_cost_lut.bin",
        TERRAIN_LUT_START,
        TERRAIN_LUT_END,
        "u8_countdown_or_signed_negative_block",
        "6_entries",
        "confirmed",
        (
            "direct runtime-confirmed LUT base/index reads at 0x00656E/0x00657E "
            "and 0x0142BA/0x0142C2"
        ),
        reference_value(__name__, 'field_4'),
    ),
)

RESOURCE_BY_ID = {spec.resource_id: spec for spec in RESOURCE_SPECS}


@dataclass(frozen=True)
class ConsumerEvidence:
    resource_id: str
    pc: int
    role: str
    status: str
    static_evidence: str
    runtime_evidence: str
    relationship: str = "direct_rom_read"


_NEIGHBOR_XREFS = (
    0x031A74,
    0x032774,
    0x032822,
    0x0328D8,
    0x032A68,
    0x032C40,
    0x033160,
    0x03321A,
    0x033906,
    0x033958,
    0x033A70,
    0x033B6C,
)

CONSUMER_EVIDENCE: tuple[ConsumerEvidence, ...] = tuple(
    ConsumerEvidence(
        "ai_city_neighbor_candidates",
        pc,
        (
            "scan ordered neighbour city IDs"
            if pc != 0x033B6C
            else "shortlist a neighbour city before physical weighted-path evaluation"
        ),
        (
            "confirmed"
            if pc in (0x031A74, 0x033160)
            else "candidate"
            if pc == 0x03321A
            else "probable"
        ),
        (
            "direct BE32 reference to biased base 0x0D4BDA and decoded city_id<<3 loop"
            if pc != 0x03321A
            else "complete static decode; current enhanced CFG has a coverage hole here"
        ),
        (
            "runtime_execute:defense_month:0x031A70-0x031AB4; "
            "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
            if pc == 0x031A74
            else "runtime_execute:defense_month:0x033160-0x0331BA; "
            "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
            if pc == 0x033160
            else "not_observed_in_current_trace"
        ),
    )
    for pc in _NEIGHBOR_XREFS
) + (
    ConsumerEvidence(
        "city_world_coordinates",
        0x0065F4,
        "project all 40 city footprints into the 72x72 path grid",
        "confirmed",
        "sequential 40-record (A1)+/DBRA loop aligned to city IDs 1..40",
        "runtime_execute:save_record_valid; analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv",
    ),
    ConsumerEvidence(
        "city_world_coordinates",
        0x067ADC,
        "draw cities on the world map",
        "confirmed",
        "direct coordinate-table indexing loop",
        "runtime_execute:defense_month,save_record_valid; analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv",
    ),
    ConsumerEvidence(
        "weighted_path_terrain_codes",
        0x006562,
        "expand 72x72 terrain codes through the six-byte LUT into FF0000",
        "confirmed",
        "decoded 5184-iteration initialization path",
        "runtime_execute:save_record_valid; analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv",
        "direct_rom_transform",
    ),
    ConsumerEvidence(
        "weighted_path_terrain_codes",
        0x006518,
        "path-routine entry; calls terrain initialization, then weighted four-neighbour frontier logic at 0x00664E",
        "confirmed",
        "runtime-confirmed routine entry plus decoded/runtime-confirmed frontier countdown at 0x00664E..0x0066C0",
        "runtime_execute:save_record_valid; analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv",
        "derived_runtime_consumer",
    ),
    ConsumerEvidence(
        "weighted_path_terrain_codes",
        0x0142A2,
        "query raw terrain code and LUT-derived cost for one cell",
        "confirmed",
        "direct grid and LUT reads",
        "runtime_execute:save_record_valid; analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv",
    ),
    ConsumerEvidence(
        "weighted_path_terrain_codes",
        0x016874,
        "consume the FF4000 reconstructed direction stream",
        "confirmed",
        "decoded 1..4 direction dispatch and fixed-point coordinate updates",
        "runtime_execute:save_record_valid; analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv",
        "derived_runtime_consumer",
    ),
    ConsumerEvidence(
        "terrain_code_static_cost_lut",
        0x00656E,
        "load LUT base for full 72x72 static terrain expansion; indexed read at 0x00657E",
        "confirmed",
        "direct PC-relative LEA of ROM 0x00670A followed by terrain-code indexed byte read",
        "runtime_execute:save_record_valid; analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv",
    ),
    ConsumerEvidence(
        "terrain_code_static_cost_lut",
        0x0142BA,
        "load LUT base for single-cell terrain query; indexed read at 0x0142C2",
        "confirmed",
        "direct absolute LEA of ROM 0x00670A followed by terrain-code indexed byte read",
        "runtime_execute:save_record_valid; analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv",
    ),
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_be16(data: bytes, offset: int) -> int:
    return struct.unpack_from(">H", data, offset)[0]


def read_be32(data: bytes, offset: int) -> int:
    return struct.unpack_from(">I", data, offset)[0]


def canonical_rom(path: Path) -> bytes:
    data = path.read_bytes()
    digest = sha256_bytes(data)
    if len(data) != CANONICAL_SIZE or digest != CANONICAL_SHA256:
        raise WorldMapError(
            "canonical ROM identity mismatch: "
            f"size={len(data)} sha256={digest}; expected "
            f"size={CANONICAL_SIZE} sha256={CANONICAL_SHA256}"
        )
    return data


def _resource_payloads(rom: bytes) -> dict[str, bytes]:
    payloads = {
        spec.resource_id: rom[spec.start : spec.end] for spec in RESOURCE_SPECS
    }
    for spec in RESOURCE_SPECS:
        payload = payloads[spec.resource_id]
        digest = sha256_bytes(payload)
        if len(payload) != spec.length or digest != spec.canonical_sha256:
            raise WorldMapError(
                f"{spec.resource_id}: canonical region mismatch: "
                f"length={len(payload)} sha256={digest}; expected "
                f"length={spec.length} sha256={spec.canonical_sha256}"
            )
    return payloads


def parse_neighbor_table(data: bytes) -> tuple[tuple[int, ...], ...]:
    expected_length = CITY_COUNT * NEIGHBOR_RECORD_SIZE
    if len(data) != expected_length:
        raise WorldMapError(
            f"AI neighbour table length {len(data)} != {expected_length}"
        )

    rows: list[tuple[int, ...]] = []
    for city_id in range(1, CITY_COUNT + 1):
        start = (city_id - 1) * NEIGHBOR_RECORD_SIZE
        raw = data[start : start + NEIGHBOR_RECORD_SIZE]
        try:
            terminator = raw.index(0xFF)
        except ValueError as error:
            raise WorldMapError(
                f"city {city_id}: neighbour record has no 0xFF terminator"
            ) from error
        # A zero-neighbour row (0xFF in slot zero) is safe for the actual
        # sentinel-controlled consumer.  The canonical graph happens to have
        # 1..7 entries per row, but that is a golden property, not a format
        # restriction on intentional mods.
        if any(value != 0xFF for value in raw[terminator:]):
            raise WorldMapError(
                f"city {city_id}: non-0xFF byte appears after the terminator"
            )
        neighbors = tuple(raw[:terminator])
        if any(neighbor < 1 or neighbor > CITY_COUNT for neighbor in neighbors):
            raise WorldMapError(
                f"city {city_id}: neighbour IDs must be in 1..{CITY_COUNT}"
            )
        # The CPU would physically consume duplicate/self IDs, but their AI
        # weighting and gameplay effects are unvalidated.  The public bundle
        # intentionally applies a conservative normalized-relationship policy.
        if city_id in neighbors:
            raise WorldMapError(f"city {city_id}: self-neighbour is not allowed")
        if len(set(neighbors)) != len(neighbors):
            raise WorldMapError(f"city {city_id}: duplicate neighbour ID")
        rows.append(neighbors)
    return tuple(rows)


def neighbor_summary(rows: Sequence[Sequence[int]]) -> dict[str, Any]:
    directed_edges = {
        (city_id, neighbor)
        for city_id, neighbors in enumerate(rows, start=1)
        for neighbor in neighbors
    }
    reciprocal_pairs = {
        tuple(sorted((source, target)))
        for source, target in directed_edges
        if (target, source) in directed_edges
    }
    unordered_pairs = {
        tuple(sorted((source, target))) for source, target in directed_edges
    }
    asymmetric = sorted(
        (source, target)
        for source, target in directed_edges
        if (target, source) not in directed_edges
    )
    histogram = Counter(len(neighbors) for neighbors in rows)
    return {
        "directed_entry_count": len(directed_edges),
        "unordered_pair_count": len(unordered_pairs),
        "reciprocal_pair_count": len(reciprocal_pairs),
        "asymmetric_directed_edges": [
            {"from_city_id": source, "to_city_id": target}
            for source, target in asymmetric
        ],
        "degree_min": min(len(neighbors) for neighbors in rows),
        "degree_max": max(len(neighbors) for neighbors in rows),
        "degree_histogram": {
            str(degree): count for degree, count in sorted(histogram.items())
        },
        "ordering_preserved": True,
        "auto_symmetrization": False,
    }


def parse_city_coordinates(data: bytes) -> tuple[dict[str, int], ...]:
    expected_length = CITY_COUNT * 4
    if len(data) != expected_length:
        raise WorldMapError(
            f"city coordinate table length {len(data)} != {expected_length}"
        )
    coordinates: list[dict[str, int]] = []
    for index in range(CITY_COUNT):
        offset = index * 4
        city_id = index + 1
        x_fixed16 = read_be16(data, offset)
        y_fixed16 = read_be16(data, offset + 2)
        x_cell = x_fixed16 >> 4
        y_cell = y_fixed16 >> 4
        if not (1 <= x_cell < GRID_WIDTH and 0 <= y_cell < GRID_HEIGHT):
            raise WorldMapError(
                f"city {city_id}: path-grid cell ({x_cell},{y_cell}) is outside "
                f"the valid footprint range x=1..{GRID_WIDTH - 1}, "
                f"y=0..{GRID_HEIGHT - 1}"
            )
        footprint_left = y_cell * GRID_WIDTH + x_cell - 1
        footprint_city = y_cell * GRID_WIDTH + x_cell
        coordinates.append(
            {
                "city_id": city_id,
                "x_fixed16": x_fixed16,
                "y_fixed16": y_fixed16,
                "x_cell": x_cell,
                "y_cell": y_cell,
                "footprint_left_index": footprint_left,
                "footprint_city_index": footprint_city,
            }
        )
    return tuple(coordinates)


def validate_terrain_grid(data: bytes) -> bytes:
    expected_length = GRID_WIDTH * GRID_HEIGHT
    if len(data) != expected_length:
        raise WorldMapError(f"terrain grid length {len(data)} != {expected_length}")
    invalid = next(
        ((index, value) for index, value in enumerate(data) if value > 5), None
    )
    if invalid is not None:
        index, value = invalid
        raise WorldMapError(
            f"terrain grid contains unsupported code 0x{value:02X} at "
            f"index {index} (x={index % GRID_WIDTH}, y={index // GRID_WIDTH})"
        )
    return data


def validate_terrain_lut(data: bytes) -> bytes:
    if len(data) != 6:
        raise WorldMapError(f"terrain LUT length {len(data)} != 6")
    # Every byte value is representable by the ROM format.  The canonical LUT
    # is [1, FF, 3, 1, 2, 1], but fixing edited bundles to those semantics would
    # defeat the purpose of importing terrain-cost mods.
    return data


def lut_value_semantics(value: int) -> dict[str, Any]:
    if not 0 <= value <= 0xFF:
        raise WorldMapError(f"LUT value {value} is outside one byte")
    signed_negative_blocked = value >= 0x80
    return {
        "signed_negative_blocked": signed_negative_blocked,
        "countdown_ticks": (
            None if signed_negative_blocked else 256 if value == 0 else value
        ),
        "note": (
            "blocked by TST.B/BMI"
            if signed_negative_blocked
            else "zero underflows to 0xFF on first SUBQ.B; expands after 256 ticks"
            if value == 0
            else "positive byte countdown cost"
        ),
    }


def terrain_runtime_bytes(terrain: bytes, lut: bytes) -> bytes:
    """Return the canonical static u8->zero-extended-BE16 expansion.

    Dynamic unit costs, city hard blocks and predecessor bytes are applied by
    later runtime phases and therefore do not belong in this static transform.
    """

    validate_terrain_grid(terrain)
    validate_terrain_lut(lut)
    expanded = bytearray(len(terrain) * 2)
    for index, terrain_code in enumerate(terrain):
        expanded[index * 2 + 1] = lut[terrain_code]
    return bytes(expanded)


def path_edit_warnings(state: Mapping[str, Any]) -> list[str]:
    terrain = state["terrain"]
    lut = state["terrain_lut"]
    warnings = [
        "structural validation does not prove route reachability; terrain/LUT edits "
        "can exhaust the frontier and make the original no-route loop fail to return"
    ]
    blocked_cell_count = sum(lut[terrain_code] >= 0x80 for terrain_code in terrain)
    if blocked_cell_count == len(terrain):
        warnings.append(
            "all 5184 static terrain cells are signed-negative blocked; nontrivial "
            "path requests are at high risk of an infinite no-route loop"
        )
    if any(value == 0 for value in lut):
        warnings.append(
            "the edited LUT contains zero; each affected frontier entry underflows "
            "and consumes 256 countdown ticks"
        )
    return warnings


def validate_world_resources(
    payloads: Mapping[str, bytes], *, require_canonical_footprints: bool = False
) -> dict[str, Any]:
    required = {spec.resource_id for spec in RESOURCE_SPECS}
    if set(payloads) != required:
        missing = sorted(required - set(payloads))
        extra = sorted(set(payloads) - required)
        raise WorldMapError(f"resource set mismatch: missing={missing} extra={extra}")

    neighbors = parse_neighbor_table(payloads["ai_city_neighbor_candidates"])
    coordinates = parse_city_coordinates(payloads["city_world_coordinates"])
    terrain = validate_terrain_grid(payloads["weighted_path_terrain_codes"])
    lut = validate_terrain_lut(payloads["terrain_code_static_cost_lut"])

    expected_city_cells = {
        coordinate["footprint_left_index"] for coordinate in coordinates
    } | {coordinate["footprint_city_index"] for coordinate in coordinates}
    actual_city_cells = {index for index, value in enumerate(terrain) if value == 1}
    if require_canonical_footprints and actual_city_cells != expected_city_cells:
        missing = sorted(expected_city_cells - actual_city_cells)
        extra = sorted(actual_city_cells - expected_city_cells)
        raise WorldMapError(
            "terrain code 1 must exactly match the 80 city footprint cells: "
            f"missing={missing[:8]} extra={extra[:8]}"
        )

    return {
        "neighbors": neighbors,
        "neighbor_summary": neighbor_summary(neighbors),
        "coordinates": coordinates,
        "terrain": terrain,
        "terrain_lut": lut,
        "city_footprint_cells": tuple(sorted(expected_city_cells)),
        "terrain_code_1_cells": tuple(sorted(actual_city_cells)),
        "terrain_code_1_exactly_matches_footprints": (
            actual_city_cells == expected_city_cells and len(expected_city_cells) == 80
        ),
    }


def scenario_189_city3_golden(rom: bytes, state: Mapping[str, Any]) -> dict[str, Any]:
    force_pointer = read_be32(rom, SCENARIO_189_DESCRIPTOR)
    officer_pointer = read_be32(rom, SCENARIO_189_DESCRIPTOR + 4)
    gold_pointer = read_be32(rom, SCENARIO_189_DESCRIPTOR + 0x0C)
    city_index = 2
    coordinate = state["coordinates"][city_index]
    result = {
        "status": "confirmed",
        "scenario_index": 0,
        "scenario_year": 189,
        "city_id": 3,
        "ui_name_traditional_chinese": "代縣",
        "city_force_id_probable": rom[force_pointer + city_index],
        "city_primary_officer_id_probable": read_be16(
            rom, officer_pointer + city_index * 2
        ),
        "officer_display_name": "劉備",
        "city_gold_confirmed": read_be32(rom, gold_pointer + city_index * 4),
        "ordered_neighbor_ids": list(state["neighbors"][city_index]),
        "neighbor_rom_offset": NEIGHBOR_START + city_index * NEIGHBOR_RECORD_SIZE,
        "neighbor_rom_offset_hex": _hex(
            NEIGHBOR_START + city_index * NEIGHBOR_RECORD_SIZE
        ),
        "x_fixed16": coordinate["x_fixed16"],
        "y_fixed16": coordinate["y_fixed16"],
        "coordinate_rom_offset": COORDINATE_START + city_index * 4,
        "coordinate_rom_offset_hex": _hex(COORDINATE_START + city_index * 4),
        "x_cell": coordinate["x_cell"],
        "y_cell": coordinate["y_cell"],
        "footprint_indices": [
            coordinate["footprint_left_index"],
            coordinate["footprint_city_index"],
        ],
        "footprint_rom_offsets": [
            TERRAIN_START + coordinate["footprint_left_index"],
            TERRAIN_START + coordinate["footprint_city_index"],
        ],
        "evidence": (
            "scenario 189 descriptor tables plus controlled city-3 UI observation; "
            "world coordinate, neighbour and terrain tables independently align"
        ),
    }
    expected = {
        "city_force_id_probable": 1,
        "city_primary_officer_id_probable": 0x00CC,
        "city_gold_confirmed": 8000,
        "ordered_neighbor_ids": [2, 4, 13],
        "x_fixed16": 0x02D0,
        "y_fixed16": 0x0088,
        "x_cell": 45,
        "y_cell": 8,
        "footprint_indices": [620, 621],
    }
    for key, value in expected.items():
        if result[key] != value:
            raise WorldMapError(
                f"scenario 189 city-3 golden mismatch for {key}: "
                f"{result[key]!r} != {value!r}"
            )
    return result


def _hex(value: int, width: int = 6) -> str:
    return f"0x{value:0{width}X}"


def _consumer_dict(entry: ConsumerEvidence) -> dict[str, Any]:
    result = asdict(entry)
    result["pc_hex"] = _hex(entry.pc)
    return result


GENERATED_FILES: tuple[dict[str, Any], ...] = (
    {"path": "ai_city_neighbor_candidates.bin", "kind": "import_source", "text": False},
    {"path": "city_world_coordinates.bin", "kind": "import_source", "text": False},
    {"path": "weighted_path_terrain_codes.bin", "kind": "import_source", "text": False},
    {"path": "terrain_code_static_cost_lut.bin", "kind": "import_source", "text": False},
    {"path": "city_neighbors.csv", "kind": "friendly_projection", "text": True},
    {"path": "city_coordinates.csv", "kind": "friendly_projection", "text": True},
    {"path": "terrain_grid.csv", "kind": "friendly_projection", "text": True},
    {"path": "terrain_lut.csv", "kind": "friendly_projection", "text": True},
    {"path": "consumer_evidence.csv", "kind": "evidence", "text": True},
    {"path": "manifest.json", "kind": "resource_manifest", "text": True},
    {"path": "WORLD_MAP_REPORT.md", "kind": "evidence_report", "text": True},
)


def build_manifest(
    rom: bytes, payloads: Mapping[str, bytes], state: Mapping[str, Any]
) -> dict[str, Any]:
    resources: list[dict[str, Any]] = []
    for spec in RESOURCE_SPECS:
        descriptor = asdict(spec)
        descriptor.update(
            {
                "start_hex": _hex(spec.start),
                "end_hex": _hex(spec.end),
                "length": spec.length,
                "extracted_canonical_sha256": sha256_bytes(payloads[spec.resource_id]),
                "address_space": "m68k_rom_linear_bin",
                "import_authoritative": True,
            }
        )
        if spec.resource_id == "ai_city_neighbor_candidates":
            descriptor.update(
                {
                    "record_count": CITY_COUNT,
                    "record_width": NEIGHBOR_RECORD_SIZE,
                    "city_id_base": 1,
                    "sentinel": 0xFF,
                    "biased_consumer_base": 0x0D4BDA,
                    "preserve_record_order": True,
                    "preserve_neighbor_order": True,
                }
            )
        elif spec.resource_id == "city_world_coordinates":
            descriptor.update(
                {
                    "record_count": CITY_COUNT,
                    "record_width": 4,
                    "field_order": ["x_fixed16_be", "y_fixed16_be"],
                    "grid_shift": 4,
                    "biased_consumer_base": 0x0D4AC6,
                }
            )
        elif spec.resource_id == "weighted_path_terrain_codes":
            descriptor.update(
                {
                    "width": GRID_WIDTH,
                    "height": GRID_HEIGHT,
                    "layout": "row_major_y_then_x",
                    "value_domain": [0, 1, 2, 3, 4, 5],
                    "runtime_transform": "lut_u8_to_zero_extended_be16_then_dynamic_overlays",
                }
            )
        elif spec.resource_id == "terrain_code_static_cost_lut":
            descriptor.update(
                {
                    "record_count": 6,
                    "record_width": 1,
                    "canonical_bytes_hex": "01 FF 03 01 02 01",
                }
            )
        resources.append(descriptor)

    terrain_histogram = Counter(state["terrain"])
    manifest = {
        "format": BUNDLE_FORMAT,
        "schema_version": 1,
        "source_rom": {
            "path": "original_g5510.bin",
            "size": len(rom),
            "sha256": sha256_bytes(rom),
            "address_space": "linear BIN / 68000 ROM byte offsets",
        },
        "confidence_policy": {
            "confirmed": "direct code consumer, runtime trace, exact table shape or round-trip evidence",
            "probable": "strong code/index correlation while the exact gameplay label remains open",
            "candidate": "plausible hypothesis requiring additional consumer or runtime evidence",
            "unknown": "no semantic role assigned",
        },
        "terminology": {
            "ai_city_neighbor_candidates": "confirmed ordered directed AI strategic relation",
            "weighted_path_terrain_codes": "confirmed physical-map input to weighted wavefront pathfinding",
            "player_road_graph": "unknown; no current evidence that the AI neighbour table constrains player movement",
        },
        "resources": resources,
        "written_byte_count": sum(spec.length for spec in RESOURCE_SPECS),
        "neighbor_summary": state["neighbor_summary"],
        "coordinate_summary": {
            "record_count": len(state["coordinates"]),
            "record_width": 4,
            "coordinate_encoding": "BE16 x_fixed16, BE16 y_fixed16",
            "path_cell_conversion": "x_cell=x_fixed16>>4; y_cell=y_fixed16>>4",
            "city_footprint_rule": "(x_cell-1,y_cell) and (x_cell,y_cell)",
            "distinct_footprint_cell_count": len(state["city_footprint_cells"]),
            "terrain_code_1_exactly_matches_footprints": True,
        },
        "terrain_summary": {
            "width": GRID_WIDTH,
            "height": GRID_HEIGHT,
            "cell_count": len(state["terrain"]),
            "code_histogram": {
                str(code): count for code, count in sorted(terrain_histogram.items())
            },
            "canonical_lut_values": list(state["terrain_lut"]),
            "lut_value_semantics": {
                "0": "not blocked initially; byte decrement underflows and expands after 256 ticks",
                "1..127": "positive countdown cost",
                "128..255": "signed-negative and skipped as blocked by TST.B/BMI",
            },
            "expanded_static_cost_histogram": {
                str(cost): count
                for cost, count in sorted(
                    Counter(state["terrain_lut"][code] for code in state["terrain"]).items()
                )
            },
            "static_zero_extended_be16_sha256": sha256_bytes(
                terrain_runtime_bytes(state["terrain"], state["terrain_lut"])
            ),
            "runtime_expansion_target": {
                "address_space": "m68k_ram",
                "start": 0xFF0000,
                "start_hex": "0xFF0000",
                "layout": "72x72 BE16; high byte predecessor/visited, low byte static or dynamic cost",
            },
            "runtime_route_buffers": ["0xFF4000", "0xFF4800"],
            "runtime_weighted_route_cost": "0xFFF644",
            "runtime_dynamic_overlays": [
                {
                    "pc_range": "0x006588..0x0065F4",
                    "written_value": 0x007F,
                    "role": "active-object high traversal cost, not an absolute block",
                    "status": "confirmed",
                },
                {
                    "pc_range": "0x0065F4..0x006622",
                    "written_value": 0x00FF,
                    "role": "two hard-block footprint cells for each of 40 cities",
                    "status": "confirmed",
                },
            ],
        },
        "consumer_evidence": [_consumer_dict(entry) for entry in CONSUMER_EVIDENCE],
        "canonical_scenario_189_city3_golden": scenario_189_city3_golden(rom, state),
        "excluded_adjacent_data": [
            {
                "start": 0x0D4B6A,
                "end": 0x0D4BE2,
                "start_hex": "0x0D4B6A",
                "end_hex": "0x0D4BE2",
                "shape": "40_records_x_3_bytes",
                "status": "unknown",
                "reason": "distinct biased-base consumers exist, but semantics are not confirmed",
            },
            {
                "start": 0x0D4D22,
                "start_hex": "0x0D4D22",
                "status": "confirmed",
                "reason": "independent six-point coordinate-list consumers lock the neighbour-table end boundary",
            },
        ],
        "import_policy": {
            "fixed_placement_only": True,
            "preserve_neighbor_order": True,
            "auto_symmetrize": False,
            "recalculate_rom_checksum": False,
            "write_new_output_only": True,
            "path_reachability_validation": False,
            "safety_scope": (
                "format and fixed-address structural validation only; blocking edits "
                "can exhaust the original frontier without a no-route exit"
            ),
            "neighbor_graph_policy": (
                "conservative semantic policy: reject self/duplicate IDs and require "
                "canonical 0xFF termination/padding; the CPU encoding could physically "
                "consume some rejected forms, but their gameplay effect is unvalidated"
            ),
        },
        "generated_files": list(GENERATED_FILES),
    }
    return manifest


def write_json(path: Path, value: Any) -> None:
    path.write_bytes(
        (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"
        )
    )


def write_csv(
    path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, Any]]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(fieldnames),
            extrasaction="raise",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))


def _write_friendly_outputs(
    output_dir: Path, payloads: Mapping[str, bytes], state: Mapping[str, Any]
) -> None:
    neighbor_data = payloads["ai_city_neighbor_candidates"]
    asymmetric = {
        (item["from_city_id"], item["to_city_id"])
        for item in state["neighbor_summary"]["asymmetric_directed_edges"]
    }
    neighbor_rows = []
    for city_id, neighbors in enumerate(state["neighbors"], start=1):
        raw = neighbor_data[
            (city_id - 1) * NEIGHBOR_RECORD_SIZE : city_id * NEIGHBOR_RECORD_SIZE
        ]
        neighbor_rows.append(
            {
                "city_id": city_id,
                "rom_offset": NEIGHBOR_START + (city_id - 1) * NEIGHBOR_RECORD_SIZE,
                "rom_offset_hex": _hex(
                    NEIGHBOR_START + (city_id - 1) * NEIGHBOR_RECORD_SIZE
                ),
                "neighbor_count": len(neighbors),
                "neighbor_ids_ordered": ";".join(str(value) for value in neighbors),
                "asymmetric_outbound_ids": ";".join(
                    str(value) for value in neighbors if (city_id, value) in asymmetric
                ),
                "terminator_index": len(neighbors),
                "raw_record_hex": raw.hex().upper(),
                **{
                    f"slot_{slot + 1}_hex": f"0x{value:02X}"
                    for slot, value in enumerate(raw)
                },
            }
        )
    write_csv(
        output_dir / "city_neighbors.csv",
        (
            "city_id",
            "rom_offset",
            "rom_offset_hex",
            "neighbor_count",
            "neighbor_ids_ordered",
            "asymmetric_outbound_ids",
            "terminator_index",
            "raw_record_hex",
            *(f"slot_{slot}_hex" for slot in range(1, 9)),
        ),
        neighbor_rows,
    )

    coordinate_rows = [
        {
            "city_id": item["city_id"],
            "rom_offset": COORDINATE_START + (item["city_id"] - 1) * 4,
            "rom_offset_hex": _hex(COORDINATE_START + (item["city_id"] - 1) * 4),
            "x_fixed16": item["x_fixed16"],
            "x_fixed16_hex": f"0x{item['x_fixed16']:04X}",
            "y_fixed16": item["y_fixed16"],
            "y_fixed16_hex": f"0x{item['y_fixed16']:04X}",
            "x_cell": item["x_cell"],
            "y_cell": item["y_cell"],
            "footprint_left_index": item["footprint_left_index"],
            "footprint_city_index": item["footprint_city_index"],
        }
        for item in state["coordinates"]
    ]
    write_csv(
        output_dir / "city_coordinates.csv",
        (
            "city_id",
            "rom_offset",
            "rom_offset_hex",
            "x_fixed16",
            "x_fixed16_hex",
            "y_fixed16",
            "y_fixed16_hex",
            "x_cell",
            "y_cell",
            "footprint_left_index",
            "footprint_city_index",
        ),
        coordinate_rows,
    )

    terrain_rows = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            index = y * GRID_WIDTH + x
            terrain_code = state["terrain"][index]
            static_cost = state["terrain_lut"][terrain_code]
            value_semantics = lut_value_semantics(static_cost)
            terrain_rows.append(
                {
                    "x": x,
                    "y": y,
                    "rom_offset": TERRAIN_START + index,
                    "rom_offset_hex": _hex(TERRAIN_START + index),
                    "terrain_code": terrain_code,
                    "static_cost": static_cost,
                    "static_cost_hex": f"0x{static_cost:02X}",
                    "signed_negative_blocked": str(
                        value_semantics["signed_negative_blocked"]
                    ).lower(),
                    "countdown_ticks": (
                        ""
                        if value_semantics["countdown_ticks"] is None
                        else value_semantics["countdown_ticks"]
                    ),
                }
            )
    write_csv(
        output_dir / "terrain_grid.csv",
        (
            "x",
            "y",
            "rom_offset",
            "rom_offset_hex",
            "terrain_code",
            "static_cost",
            "static_cost_hex",
            "signed_negative_blocked",
            "countdown_ticks",
        ),
        terrain_rows,
    )

    lut_rows = [
        {
            "terrain_code": code,
            "rom_offset": TERRAIN_LUT_START + code,
            "rom_offset_hex": _hex(TERRAIN_LUT_START + code),
            "static_cost_or_ff": value,
            "static_cost_hex": f"0x{value:02X}",
            "signed_negative_blocked": str(
                lut_value_semantics(value)["signed_negative_blocked"]
            ).lower(),
            "countdown_ticks": (
                ""
                if lut_value_semantics(value)["countdown_ticks"] is None
                else lut_value_semantics(value)["countdown_ticks"]
            ),
            "machine_semantics": lut_value_semantics(value)["note"],
            "status": "confirmed",
        }
        for code, value in enumerate(state["terrain_lut"])
    ]
    write_csv(
        output_dir / "terrain_lut.csv",
        (
            "terrain_code",
            "rom_offset",
            "rom_offset_hex",
            "static_cost_or_ff",
            "static_cost_hex",
            "signed_negative_blocked",
            "countdown_ticks",
            "machine_semantics",
            "status",
        ),
        lut_rows,
    )

    evidence_rows = []
    for entry in CONSUMER_EVIDENCE:
        evidence_rows.append(
            {
                "resource_id": entry.resource_id,
                "pc": entry.pc,
                "pc_hex": _hex(entry.pc),
                "role": entry.role,
                "status": entry.status,
                "static_evidence": entry.static_evidence,
                "runtime_evidence": entry.runtime_evidence,
                "relationship": entry.relationship,
            }
        )
    write_csv(
        output_dir / "consumer_evidence.csv",
        (
            "resource_id",
            "pc",
            "pc_hex",
            "role",
            "status",
            "static_evidence",
            "runtime_evidence",
            "relationship",
        ),
        evidence_rows,
    )


def render_report(manifest: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    resources = manifest["resources"]
    lines = [
        "# G-5510 world map, AI neighbour candidates and weighted path data",
        "",
        "Status: **confirmed data layouts and key runtime consumers; remaining static",
        "consumers are probable/candidate; player road-graph interpretation remains unknown**.",
        "",
        "All addresses below are linear BIN / 68000 ROM byte offsets. The canonical",
        f"input is the 1 MiB image with SHA-256 `{CANONICAL_SHA256.upper()}`.",
        "",
        "## 1. Resource inventory",
        "",
        "| Resource | ROM range | Length | Shape | Status | SHA-256 |",
        "|---|---:|---:|---|---|---|",
    ]
    for resource in resources:
        lines.append(
            "| `{resource_id}` | `{start_hex}..{end_hex}` | {length} | {shape} | "
            "**{semantic_status}** | `{canonical_sha256}` |".format(**resource)
        )

    summary = state["neighbor_summary"]
    asymmetric_text = ", ".join(
        f"{edge['from_city_id']}→{edge['to_city_id']}"
        for edge in summary["asymmetric_directed_edges"]
    )
    lines.extend(
        [
            "",
            "The fixed-placement importer covers exactly **5,670 bytes**. It does not",
            "recalculate the Mega Drive header checksum; a one-byte source edit therefore",
            "remains one changed ROM byte in the output copy.",
            "",
            "## 2. Ordered directed AI city-neighbour candidates",
            "",
            "The **confirmed** table at `0x0D4BE2..0x0D4D22` is 40 fixed records of",
            "eight bytes. Code uses the one-based biased base `0x0D4BDA + city_id*8`,",
            "reads ordered byte IDs, and stops on a negative byte (`0xFF`). Consumers",
            "index city arrays such as `FFF427 + neighbour_city_id`.",
            "",
            f"Canonical invariants: {summary['directed_entry_count']} directed entries,",
            f"{summary['reciprocal_pair_count']} reciprocal pairs and two one-way entries",
            f"({asymmetric_text}). There are no self-links, duplicate row entries or IDs",
            "outside 1..40. Import preserves byte order and never auto-symmetrizes.",
            "",
            "This is a **confirmed AI strategic neighbour/candidate relation**. Calling it",
            "a player movement or road graph is currently **unknown/unconfirmed**: known",
            "player/path-cost code can call the physical pathfinder without reading it.",
            "",
            "### Canonical rows",
            "",
            "| City | Ordered neighbour IDs |",
            "|---:|---|",
        ]
    )
    for city_id, neighbors in enumerate(state["neighbors"], start=1):
        lines.append(f"| {city_id} | {', '.join(str(value) for value in neighbors)} |")

    lines.extend(
        [
            "",
            "### Consumer evidence",
            "",
            "| PC | Resource | Relationship | Role | Status | Runtime evidence |",
            "|---:|---|---|---|---|---|",
        ]
    )
    for entry in CONSUMER_EVIDENCE:
        lines.append(
            f"| `{_hex(entry.pc)}` | `{entry.resource_id}` | `{entry.relationship}` | {entry.role} | "
            f"**{entry.status}** | {entry.runtime_evidence} |"
        )

    terrain = manifest["terrain_summary"]
    lut = terrain["canonical_lut_values"]
    histogram = ", ".join(
        f"{code}:{count}" for code, count in terrain["code_histogram"].items()
    )
    lines.extend(
        [
            "",
            "The neighbour loops at `0x031A74` and `0x033160` are **confirmed** by",
            "runtime observation in the current `defense_month` trace. Nine other decoded",
            "references remain **probable** static consumers; `0x03321A` remains a",
            "**candidate** because it is a coherent manual decode in a current CFG hole.",
            "",
            "## 3. City coordinates and the physical weighted grid",
            "",
            "The **confirmed** coordinate table at `0x0D4ACA..0x0D4B6A` contains",
            "40 `(BE16 x_fixed16, BE16 y_fixed16)` records. Rendering, hit testing, AI",
            "selection and path-grid setup share these coordinates.",
            "",
            "The **confirmed** terrain input at `0x0EE5F0..0x0EFA30` is a row-major",
            f"72×72 u8 grid. Canonical code histogram: `{histogram}`.",
            "",
            f"The canonical LUT at `0x00670A..0x006710` is `{lut}`: its values are",
            "positive costs `1/2/3` or the signed-negative block `0xFF`. Direct LUT",
            "reads at `0x00656E/0x00657E` and `0x0142BA/0x0142C2` are runtime-confirmed.",
            "`0x006562` expands the grid into 72×72",
            "BE16 cells at `FF0000`. The high byte later records visited/predecessor",
            "direction and the low byte holds static or dynamic cost.",
            "",
            "The routine beginning at `0x006518` calls terrain initialization at",
            "`0x00651C`; the frontier loop at `0x00664E..0x0066C0` is a weighted",
            "wavefront, not ordinary unit-cost BFS. Cost is counted down before",
            "four-neighbour expansion. `FFF644` is weighted",
            "route cost; the `1..4,FF` stream reconstructed in `FF4000` is the per-cell",
            "direction path.",
            "",
            "For edited LUT bytes, machine behaviour is: `01..7F` positive countdown",
            "cost; `80..FF` signed-negative and skipped as blocked; `00` initially passes",
            "the sign test but underflows on the first byte decrement, expanding only after",
            "256 countdown ticks. The low-level importer permits all byte values because",
            "each has defined machine behaviour; it does not mislabel only `FF` as blocked.",
            "",
            "Runtime overlays are separate from the static ROM grid: active objects receive",
            "`0x007F` (very high cost, not absolute blocking) at `0x006588..0x0065F4`;",
            "the two cells for every city receive `0x00FF` hard blocks at",
            "`0x0065F4..0x006622`.",
            "",
            "For every canonical city, `(x_cell-1,y_cell)` and `(x_cell,y_cell)` are",
            "terrain code 1. The 80 distinct footprint cells are exactly all 80 code-1",
            "cells in the grid, with no missing or extra cell.",
            "",
            "Raw terrain codes 0, 2, 3, 4 and 5 do not yet have confirmed visual names.",
            "The tool deliberately does not label them road, water, mountain or similar.",
            "",
            "## 4. Scenario 189 city-3 golden alignment",
            "",
        ]
    )
    golden = manifest["canonical_scenario_189_city3_golden"]
    lines.extend(
        [
            "The **confirmed/probable fields remain individually labelled**:",
            "",
            f"- UI city: `{golden['city_id']} 代縣`; officer display: `劉備`.",
            f"- City→force slot (**probable semantic**): `{golden['city_force_id_probable']}`.",
            f"- City primary officer (**probable semantic**): `0x{golden['city_primary_officer_id_probable']:04X}`.",
            f"- Gold (**confirmed**): `{golden['city_gold_confirmed']}`.",
            f"- Ordered neighbour IDs (**confirmed**): `{golden['ordered_neighbor_ids']}`.",
            f"- Fixed coordinates (**confirmed**): `(0x{golden['x_fixed16']:04X}, 0x{golden['y_fixed16']:04X})`.",
            f"- Grid cell and footprint (**confirmed**): `({golden['x_cell']},{golden['y_cell']})`, indices `{golden['footprint_indices']}`.",
            "",
            "This validates the shared city-ID alignment across scenario state, UI",
            "observation, neighbour rows, coordinates and path-grid footprint. It does",
            "not independently prove that each neighbour pair is geographically correct.",
            "",
            "## 5. Lossless edit contract",
            "",
            "The four `*.bin` files are the authoritative import sources. CSV files are",
            "deterministic read-only projections for review; editing a CSV alone has no",
            "effect. Import validates fixed lengths, IDs, terminators, padding, duplicate",
            "and self-links, terrain value range and coordinate/grid index safety. The",
            "exact code-1/city-footprint relationship is a canonical golden invariant; it",
            "is not forced onto an intentional coordinate or terrain mod.",
            "",
            "Self-links and duplicate neighbour IDs are rejected by a conservative",
            "normalized-relationship policy, not because the CPU could not read those",
            "bytes. Likewise, the importer requires canonical `0xFF` termination/padding",
            "although any signed-negative byte would stop the machine loop. The gameplay",
            "effects of these noncanonical encodings are unvalidated, so v1 does not emit",
            "them silently.",
            "",
            "A clean extract/import must reproduce the complete canonical ROM byte for",
            "byte. Edits are written only to the four fixed intervals in a new output",
            "file. The manifest cannot relocate an asset, and the input ROM must pass the",
            "canonical size/SHA-256 gate.",
            "",
            "This is structural validation, not a proof that every edited route remains",
            "reachable. The original loop at `0x006544..0x006554` continues after",
            "`0x00664E`/`0x0066B4..0x0066C0` report an exhausted frontier; sufficiently",
            "blocking terrain or LUT edits can therefore make a no-route calculation fail",
            "to return. Import reports this warning but does not impose an unproven global",
            "connectivity policy on intentional mods.",
            "",
            "Repository policy ignores generated `*.bin` payloads. Run `extract` into a",
            "fresh local bundle such as `generated/world_map` before import; the committed",
            "manifest, CSV and Markdown files are deterministic audit artifacts.",
            "",
            "## 6. Explicit exclusions and remaining unknowns",
            "",
            "- `0x0D4B6A..0x0D4BE2` is a distinct 40×3 table with biased-base consumers,",
            "  but its semantics remain **unknown** and it is not exported here.",
            "- `0x0D4D22` begins an independent six-point coordinate list; consumer xrefs",
            "  confirm it is not a 41st neighbour record.",
            "- Player movement legality through the AI neighbour table remains **unknown**.",
            "- Terrain artwork and the visual names of terrain codes remain **unknown**.",
            "- The two one-way edges may be design choices or original bugs; the tool",
            "  preserves them and makes no unsupported correction.",
            "",
            "## 7. Reproduction",
            "",
            "```powershell",
            "python tools\\world_map\\world_map.py extract `",
            "  --rom ..\\work\\original_g5510.bin `",
            "  --output generated\\world_map",
            "",
            "python tools\\world_map\\world_map.py verify `",
            "  --rom ..\\work\\original_g5510.bin `",
            "  --bundle generated\\world_map",
            "",
            "python -m unittest -v tools.world_map.test_world_map",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def extract_bundle(rom_path: Path, output_dir: Path) -> dict[str, Any]:
    rom = canonical_rom(rom_path)
    payloads = _resource_payloads(rom)
    state = validate_world_resources(payloads, require_canonical_footprints=True)
    if output_dir.exists():
        raise WorldMapError(f"refusing to overwrite existing output directory: {output_dir}")
    output_dir.mkdir(parents=True)

    for spec in RESOURCE_SPECS:
        (output_dir / spec.filename).write_bytes(payloads[spec.resource_id])
    _write_friendly_outputs(output_dir, payloads, state)
    manifest = build_manifest(rom, payloads, state)
    write_json(output_dir / "manifest.json", manifest)
    (output_dir / "WORLD_MAP_REPORT.md").write_bytes(
        render_report(manifest, state).encode("utf-8")
    )
    return manifest


def _validate_manifest(manifest: Mapping[str, Any], canonical_base: bytes) -> None:
    if manifest.get("format") != BUNDLE_FORMAT or manifest.get("schema_version") != 1:
        raise WorldMapError("unsupported or missing world-map bundle format")
    source = manifest.get("source_rom")
    if not isinstance(source, Mapping):
        raise WorldMapError("manifest source_rom is missing or malformed")
    if source.get("size") != CANONICAL_SIZE or source.get("sha256") != CANONICAL_SHA256:
        raise WorldMapError("bundle was not extracted from the canonical ROM")
    resources = manifest.get("resources")
    if not isinstance(resources, list) or len(resources) != len(RESOURCE_SPECS):
        raise WorldMapError("manifest resource list was changed")
    for descriptor, spec in zip(resources, RESOURCE_SPECS):
        if not isinstance(descriptor, Mapping):
            raise WorldMapError("malformed resource descriptor")
        expected = {
            "resource_id": spec.resource_id,
            "filename": spec.filename,
            "start": spec.start,
            "end": spec.end,
            "length": spec.length,
            "kind": spec.kind,
            "shape": spec.shape,
            "canonical_sha256": spec.canonical_sha256,
            "extracted_canonical_sha256": spec.canonical_sha256,
        }
        for key, value in expected.items():
            if descriptor.get(key) != value:
                raise WorldMapError(
                    f"{spec.resource_id}: manifest {key} was changed: "
                    f"{descriptor.get(key)!r} != {value!r}"
                )

    canonical_payloads = _resource_payloads(canonical_base)
    canonical_state = validate_world_resources(
        canonical_payloads, require_canonical_footprints=True
    )
    expected_manifest = build_manifest(
        canonical_base, canonical_payloads, canonical_state
    )
    if dict(manifest) != expected_manifest:
        raise WorldMapError(
            "manifest audit metadata differs from the canonical generated manifest"
        )


def _checked_write(
    image: bytearray,
    ownership: dict[int, tuple[int, str]],
    offset: int,
    payload: bytes,
    label: str,
) -> None:
    end = offset + len(payload)
    if offset < 0 or end > len(image):
        raise WorldMapError(f"{label}: write 0x{offset:X}..0x{end:X} outside base ROM")
    for index, value in enumerate(payload):
        position = offset + index
        previous = ownership.get(position)
        if previous is not None and previous[0] != value:
            raise WorldMapError(
                f"conflicting writes at 0x{position:06X}: {previous[1]} "
                f"has 0x{previous[0]:02X}, {label} has 0x{value:02X}"
            )
        ownership[position] = (value, label)
    image[offset:end] = payload


def import_bundle(
    base_rom_path: Path, bundle_dir: Path, output_rom_path: Path
) -> dict[str, Any]:
    if base_rom_path.resolve() == output_rom_path.resolve():
        raise WorldMapError("refusing to overwrite the base/original ROM in place")
    if output_rom_path.exists():
        raise WorldMapError(f"refusing to overwrite existing output file: {output_rom_path}")
    base = canonical_rom(base_rom_path)
    try:
        manifest = json.loads((bundle_dir / "manifest.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        raise WorldMapError(f"cannot read bundle manifest: {error}") from error
    if not isinstance(manifest, Mapping):
        raise WorldMapError("bundle manifest root must be an object")
    _validate_manifest(manifest, base)

    payloads: dict[str, bytes] = {}
    for spec in RESOURCE_SPECS:
        payload_path = bundle_dir / spec.filename
        try:
            payload = payload_path.read_bytes()
        except OSError as error:
            raise WorldMapError(
                f"{spec.resource_id}: cannot read payload {spec.filename}: {error}"
            ) from error
        if len(payload) != spec.length:
            raise WorldMapError(
                f"{spec.resource_id}: payload length {len(payload)} != {spec.length}"
            )
        payloads[spec.resource_id] = payload
    edited_state = validate_world_resources(payloads)

    image = bytearray(base)
    ownership: dict[int, tuple[int, str]] = {}
    for spec in RESOURCE_SPECS:
        _checked_write(
            image,
            ownership,
            spec.start,
            payloads[spec.resource_id],
            spec.resource_id,
        )

    output_rom_path.parent.mkdir(parents=True, exist_ok=True)
    with output_rom_path.open("xb") as handle:
        handle.write(image)
    changed = [index for index, (old, new) in enumerate(zip(base, image)) if old != new]
    return {
        "output": str(output_rom_path),
        "size": len(image),
        "sha256": sha256_bytes(image),
        "changed_byte_count": len(changed),
        "first_changed_offset": changed[0] if changed else None,
        "last_changed_offset": changed[-1] if changed else None,
        "written_byte_count": len(ownership),
        "rom_checksum_recalculated": False,
        "warnings": path_edit_warnings(edited_state),
    }


def verify_bundle(rom_path: Path, bundle_dir: Path) -> dict[str, Any]:
    canonical = canonical_rom(rom_path)
    with tempfile.TemporaryDirectory(prefix="g5510-world-map-roundtrip-") as temporary:
        rebuilt_path = Path(temporary) / "roundtrip.bin"
        result = import_bundle(rom_path, bundle_dir, rebuilt_path)
        rebuilt = rebuilt_path.read_bytes()
    if rebuilt != canonical:
        mismatch = next(
            index
            for index, (expected, actual) in enumerate(zip(canonical, rebuilt))
            if expected != actual
        )
        raise WorldMapError(f"round-trip mismatch at ROM 0x{mismatch:06X}")
    return {
        **result,
        "output": "temporary/roundtrip.bin",
        "exact_match": True,
        "expected_sha256": CANONICAL_SHA256,
    }


def default_rom_path() -> Path:
    return Path(__file__).resolve().parents[3] / "work" / "original_g5510.bin"


def command_extract(args: argparse.Namespace) -> int:
    manifest = extract_bundle(args.rom, args.output)
    print(
        f"extracted resources={len(manifest['resources'])} "
        f"written_bytes={manifest['written_byte_count']} output={args.output}"
    )
    return 0


def command_import(args: argparse.Namespace) -> int:
    print(json.dumps(import_bundle(args.base_rom, args.bundle, args.output), sort_keys=True))
    return 0


def command_verify(args: argparse.Namespace) -> int:
    print(json.dumps(verify_bundle(args.rom, args.bundle), sort_keys=True))
    return 0


def command_roundtrip(args: argparse.Namespace) -> int:
    extract_bundle(args.rom, args.work_dir)
    result = import_bundle(args.rom, args.work_dir, args.output)
    if result["sha256"] != CANONICAL_SHA256 or result["changed_byte_count"] != 0:
        raise WorldMapError("extract/import round-trip was not an exact canonical match")
    print(json.dumps({**result, "exact_match": True}, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser("extract", help="extract world-map resources")
    extract_parser.add_argument("--rom", type=Path, default=default_rom_path())
    extract_parser.add_argument("--output", type=Path, required=True)
    extract_parser.set_defaults(func=command_extract)

    import_parser = subparsers.add_parser(
        "import", help="import fixed world-map resources into a new ROM copy"
    )
    import_parser.add_argument("--base-rom", type=Path, default=default_rom_path())
    import_parser.add_argument("--bundle", type=Path, required=True)
    import_parser.add_argument("--output", type=Path, required=True)
    import_parser.set_defaults(func=command_import)

    verify_parser = subparsers.add_parser("verify", help="verify an exact clean round-trip")
    verify_parser.add_argument("--rom", type=Path, default=default_rom_path())
    verify_parser.add_argument("--bundle", type=Path, required=True)
    verify_parser.set_defaults(func=command_verify)

    roundtrip_parser = subparsers.add_parser(
        "roundtrip", help="extract then import to a persistent output copy"
    )
    roundtrip_parser.add_argument("--rom", type=Path, default=default_rom_path())
    roundtrip_parser.add_argument("--work-dir", type=Path, required=True)
    roundtrip_parser.add_argument("--output", type=Path, required=True)
    roundtrip_parser.set_defaults(func=command_roundtrip)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, WorldMapError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    sys.exit(main())
