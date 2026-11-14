#!/usr/bin/env python3
"""City transport rules, record formats and the fixed cargo editor.

Player dispatch selects cargo, writes a four-byte outgoing record and
deducts the source resources. Arrival reads the original cargo row and
credits the target. The executable models use the caller's ROM data for
cargo amounts and city coordinates.
"""

from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import hashlib
import json
import os
import stat
import struct
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


CANONICAL_BIN_SIZE = 0x100000
CANONICAL_BIN_SHA256 = reference_value(__name__, 'CANONICAL_BIN_SHA256')
CANONICAL_SMD_SIZE = 1_049_088
CANONICAL_SMD_SHA256 = reference_value(__name__, 'CANONICAL_SMD_SHA256')
COMMAND_ID = 0x0B
CITY_COUNT = 40
OFFICER_COUNT = 256
RESOURCE_CAP = 999_999
TRANSPORT_RECORD_SIZE = 4
TRANSPORT_RECORD_BASE = 0xFFCDFC
CITY_GOLD_BASE = 0xFFDFFC
CITY_FOOD_BASE = 0xFFE09C

CARGO_TABLE_START = 0x013B68
CARGO_TABLE_END = 0x013B80
CARGO_RECORD_SIZE = 8
CARGO_COUNT = 3
CARGO_TABLE_SHA256 = reference_value(__name__, 'CARGO_TABLE_SHA256')
CARGO_BUNDLE_FORMAT = "g5510-transport-cargo-v1"

COORDINATE_TABLE_START = 0x0D4ACA
COORDINATE_TABLE_END = 0x0D4B6A
COORDINATE_TABLE_SHA256 = reference_value(__name__, 'COORDINATE_TABLE_SHA256')
COORDINATE_BIASED_BASE = 0x0D4AC6


class TransportFlowError(ValueError):
    """Controlled validation error for this package."""


@dataclass(frozen=True)
class Anchor:
    name: str
    start: int
    end: int
    sha256: str
    evidence: str
    role: str
    owns_bytes: bool = True

    @property
    def length(self) -> int:
        return self.end - self.start


ANCHORS: tuple[Anchor, ...] = (
    Anchor(
        "CommandDispatchWord", 0x00E032, 0x00E034,
        reference_value(__name__, 'field'),
        "confirmed_static",
        "command 0x0B signed PC-relative dispatch word 0x06A2 resolves to 0x00E790",
    ),
    Anchor(
        "SourceTransportPendingGate", 0x001C88, 0x001CFA,
        reference_value(__name__, 'field_2'),
        "confirmed_static",
        "for command 0x0B, reject a source whose four-byte outgoing record starts nonzero; message 0xB8",
    ),
    Anchor(
        "PlayerMapSourceSnapshot", 0x0026B6, 0x0026DA,
        reference_value(__name__, 'field_3'),
        "confirmed_static",
        "copy selected source city FFF392 to retained source field FFF3A8 before target selection",
    ),
    Anchor(
        "PlayerTransportWrapper", 0x00E790, 0x00E7B0,
        reference_value(__name__, 'field_4'),
        "confirmed_static",
        "call common commit at 0x00E7B0, then set post-command UI state and return",
    ),
    Anchor(
        "TransportCommit", 0x00E7B0, 0x00E822,
        reference_value(__name__, 'field_5'),
        "confirmed_static",
        "encode source outgoing record and deduct selected fixed cargo from source gold/food",
    ),
    Anchor(
        "CargoSelectionController", 0x013AB6, 0x013B68,
        reference_value(__name__, 'field_6'),
        "confirmed_static",
        "wrap choice 0..2, load cargo, enforce source resource gates, and enter target-map selection",
    ),
    Anchor(
        "CargoTable", CARGO_TABLE_START, CARGO_TABLE_END,
        CARGO_TABLE_SHA256,
        "confirmed_static",
        "three fixed BE32 gold/food pairs",
    ),
    Anchor(
        "TransportAnimationDispatcher", 0x016660, 0x016748,
        reference_value(__name__, 'field_7'),
        "confirmed_static",
        "scan 40 outgoing records; when none are active advance month/year bytes",
    ),
    Anchor(
        "TransportMovementAndCollision", 0x016748, 0x0168C6,
        reference_value(__name__, 'field_8'),
        "confirmed_static",
        "prepare record position, perform path/collision checks, and step toward target",
    ),
    Anchor(
        "ArrivalCredit", 0x0168C6, 0x016922,
        reference_value(__name__, 'field_9'),
        "confirmed_static",
        "credit table-selected gold/food to target with independent cap 999999, then clear record byte 0",
    ),
    Anchor(
        "MovementRecordSetup", 0x016ACC, 0x016B3A,
        reference_value(__name__, 'field_10'),
        "confirmed_static",
        "expand record coordinates and target city coordinate into pathfinding working state",
    ),
    Anchor(
        "AITransportSelection", 0x0323C2, 0x0324EE,
        reference_value(__name__, 'field_11'),
        "static_access_semantics_probable",
        "probable AI cargo/destination selection; exact bounded arithmetic retained without upgrading semantics",
    ),
    Anchor(
        "CityCoordinateTable", COORDINATE_TABLE_START, COORDINATE_TABLE_END,
        COORDINATE_TABLE_SHA256,
        "confirmed_shared_resource",
        "40 city fixed16 x/y pairs; authoritative ownership belongs to world_map",
        owns_bytes=False,
    ),
)


EXPECTED_INSTRUCTIONS: tuple[tuple[int, bytes, str], ...] = (
    (0x00E7B0, bytes.fromhex("3038f3a8"), "load retained source city"),
    (0x00E7C8, bytes.fromhex("43f9000d4ac6"), "load biased city-coordinate base"),
    (0x00E802, bytes.fromhex("41f900013b68"), "load cargo-table base"),
    (0x00E80C, bytes.fromhex("94b00000"), "subtract selected gold from source"),
    (0x00E818, bytes.fromhex("94b00004"), "subtract selected food from source"),
    (0x013B08, bytes.fromhex("303c00bd"), "insufficient-gold message id"),
    (0x013B18, bytes.fromhex("303c00c7"), "insufficient-food message id"),
    (0x0168C8, bytes.fromhex("1416"), "read record byte 0"),
    (0x0168CA, bytes.fromhex("02420003"), "mask record type low two bits"),
    (0x0168D8, bytes.fromhex("43f900013b60"), "biased arrival cargo-table base"),
    (0x0168EA, bytes.fromhex("0c83000f423f"), "gold cap 999999"),
    (0x016908, bytes.fromhex("0c83000f423f"), "food cap 999999"),
    (0x01691A, bytes.fromhex("4216"), "clear record byte 0"),
    (0x0323F6, bytes.fromhex("4eb90000e7b0"), "probable AI calls common commit"),
    (0x032416, bytes.fromhex("0cb000004e201000"), "probable AI gold threshold 20000"),
    (0x032424, bytes.fromhex("0cb100004e201000"), "probable AI food threshold 20000"),
    (0x0324D8, bytes.fromhex("8cfc000a"), "AI helper unsigned divide by 10"),
    (0x0324E4, bytes.fromhex("e78e"), "AI helper multiply quotient by 8 before add-back"),
)


CARGO_LABELS = ("金1萬", "米1萬", "金和米")


def sha256_bytes(data: bytes | bytearray) -> str:
    return hashlib.sha256(bytes(data)).hexdigest()


def _canonical_file(path: Path, *, size: int, sha256: str, label: str) -> bytes:
    if not path.is_file() or path.is_symlink():
        raise TransportFlowError(f"{label} must be a regular non-symlink file: {path}")
    data = path.read_bytes()
    if len(data) != size:
        raise TransportFlowError(f"{label} size mismatch: observed {len(data)}, expected {size}")
    observed = sha256_bytes(data)
    if observed != sha256:
        raise TransportFlowError(f"{label} SHA-256 mismatch: observed {observed}, expected {sha256}")
    return data


def canonical_bin(path: Path) -> bytes:
    """Load and identity-gate the canonical linear BIN."""

    return _canonical_file(
        path,
        size=CANONICAL_BIN_SIZE,
        sha256=CANONICAL_BIN_SHA256,
        label="canonical linear BIN",
    )


def canonical_smd(path: Path) -> bytes:
    """Load and identity-gate the canonical interleaved SMD."""

    return _canonical_file(
        path,
        size=CANONICAL_SMD_SIZE,
        sha256=CANONICAL_SMD_SHA256,
        label="canonical SMD",
    )


def verify_anchors(rom: bytes) -> list[dict[str, Any]]:
    if len(rom) != CANONICAL_BIN_SIZE:
        raise TransportFlowError("anchor verification requires the canonical-size linear BIN")
    rows: list[dict[str, Any]] = []
    for anchor in ANCHORS:
        region = rom[anchor.start:anchor.end]
        if len(region) != anchor.length:
            raise TransportFlowError(f"anchor {anchor.name} is outside the ROM")
        observed = sha256_bytes(region)
        if observed != anchor.sha256:
            raise TransportFlowError(
                f"anchor {anchor.name} mismatch: observed {observed}, expected {anchor.sha256}"
            )
        rows.append({
            **asdict(anchor),
            "length": anchor.length,
            "start_hex": f"0x{anchor.start:06X}",
            "end_hex": f"0x{anchor.end:06X}",
            "status": "PASS",
        })
    for address, expected, role in EXPECTED_INSTRUCTIONS:
        observed = rom[address:address + len(expected)]
        if observed != expected:
            raise TransportFlowError(
                f"instruction anchor mismatch at 0x{address:06X}: "
                f"observed {observed.hex()}, expected {expected.hex()} ({role})"
            )
    return rows


def command_dispatch_target(rom: bytes, command_id: int = COMMAND_ID) -> int:
    """Resolve the indexed signed-word target used by command dispatch.

    The dispatch code computes the word address from the command byte and uses
    the table's PC-relative convention.  For command 0x0B, the concrete table
    word is at 0x00E032 and resolves to 0x00E790.
    """

    if command_id != COMMAND_ID:
        raise TransportFlowError("this bounded package resolves only command 0x0B")
    word_address = 0x00E032
    relative = struct.unpack_from(">h", rom, word_address)[0]
    # The effective PC base for this indexed table entry is 0x00E0EE.
    return 0x00E0EE + relative


def _check_city(city_id: int) -> int:
    if isinstance(city_id, bool) or not isinstance(city_id, int) or not 1 <= city_id <= CITY_COUNT:
        raise TransportFlowError(f"city_id must be 1..{CITY_COUNT}")
    return city_id


def _check_choice(choice: int) -> int:
    if isinstance(choice, bool) or not isinstance(choice, int) or not 0 <= choice < CARGO_COUNT:
        raise TransportFlowError("transport choice must be 0..2")
    return choice


def city_gold_address(city_id: int) -> int:
    return CITY_GOLD_BASE + 4 * _check_city(city_id)


def city_food_address(city_id: int) -> int:
    return CITY_FOOD_BASE + 4 * _check_city(city_id)


def transport_record_address(city_id: int) -> int:
    return TRANSPORT_RECORD_BASE + 4 * _check_city(city_id)


def cargo_options(rom: bytes) -> list[dict[str, Any]]:
    """Decode the exact three fixed cargo pairs."""

    if len(rom) < CARGO_TABLE_END:
        raise TransportFlowError("ROM is too short for the cargo table")
    rows: list[dict[str, Any]] = []
    for choice in range(CARGO_COUNT):
        offset = CARGO_TABLE_START + choice * CARGO_RECORD_SIZE
        gold, food = struct.unpack_from(">II", rom, offset)
        rows.append({
            "choice_index": choice,
            "record_type": choice + 1,
            "label_zh": CARGO_LABELS[choice],
            "offset": offset,
            "offset_hex": f"0x{offset:06X}",
            "gold": gold,
            "food": food,
            "evidence": "confirmed_static",
        })
    return rows


def cargo_for_choice(rom: bytes, choice: int) -> tuple[int, int]:
    row = cargo_options(rom)[_check_choice(choice)]
    return int(row["gold"]), int(row["food"])


def city_coordinate(rom: bytes, city_id: int) -> tuple[int, int]:
    """Return shared world-map fixed16 ``(x, y)`` for a city."""

    city_id = _check_city(city_id)
    offset = COORDINATE_TABLE_START + (city_id - 1) * 4
    return struct.unpack_from(">HH", rom, offset)


def encode_transport_record(
    *, source_city: int, target_city: int, choice: int, rom: bytes
) -> bytes:
    """Encode the exact four-byte record produced by 0x00E7B0."""

    _check_city(source_city)
    _check_city(target_city)
    _check_choice(choice)
    x_fixed16, y_fixed16 = city_coordinate(rom, source_city)
    x_cell = x_fixed16 >> 4
    y_cell = y_fixed16 >> 4
    if x_cell > 0xFF or y_cell > 0xFF:
        raise TransportFlowError("source coordinate does not fit the transport record")
    return bytes((0x10 | (choice + 1), y_cell, x_cell, target_city))


def decode_transport_record(record: bytes | bytearray) -> dict[str, Any]:
    if len(record) != TRANSPORT_RECORD_SIZE:
        raise TransportFlowError("transport record must be exactly four bytes")
    flags_type, y_cell, x_cell, target_city = bytes(record)
    return {
        "active": flags_type != 0,
        "flags_type": flags_type,
        "record_type": flags_type & 0x03,
        "flag_0x10": bool(flags_type & 0x10),
        "y_cell": y_cell,
        "x_cell": x_cell,
        "target_city": target_city,
    }


def player_commit_model(
    *,
    source_city: int,
    target_city: int,
    choice: int,
    source_gold: int,
    source_food: int,
    rom: bytes,
) -> dict[str, Any]:
    """Model the successful player commit after the UI affordability gates."""

    _check_city(source_city)
    _check_city(target_city)
    _check_choice(choice)
    if any(isinstance(value, bool) or not isinstance(value, int) or value < 0
           for value in (source_gold, source_food)):
        raise TransportFlowError("source resources must be nonnegative integers")
    cargo_gold, cargo_food = cargo_for_choice(rom, choice)
    if source_gold < cargo_gold:
        raise TransportFlowError("insufficient source gold; real UI emits message 0xBD")
    if source_food < cargo_food:
        raise TransportFlowError("insufficient source food; real UI emits message 0xC7")
    record = encode_transport_record(
        source_city=source_city,
        target_city=target_city,
        choice=choice,
        rom=rom,
    )
    return {
        "source_city": source_city,
        "target_city": target_city,
        "choice": choice,
        "cargo_gold": cargo_gold,
        "cargo_food": cargo_food,
        "source_gold": source_gold - cargo_gold,
        "source_food": source_food - cargo_food,
        "record": record,
        "record_hex": record.hex().upper(),
        "separate_fee": 0,
        "officer_or_troop_cargo": False,
        "rng_used": False,
    }


def arrival_model(
    *, target_gold: int, target_food: int, record: bytes | bytearray, rom: bytes
) -> dict[str, Any]:
    """Model 0x0168C6 for a valid active type-1..3 transport record."""

    if any(isinstance(value, bool) or not isinstance(value, int) or value < 0
           for value in (target_gold, target_food)):
        raise TransportFlowError("target resources must be nonnegative integers")
    decoded = decode_transport_record(record)
    record_type = int(decoded["record_type"])
    if record_type not in (1, 2, 3):
        raise TransportFlowError("arrival model requires active record type 1..3")
    target_city = _check_city(int(decoded["target_city"]))
    cargo_gold, cargo_food = cargo_for_choice(rom, record_type - 1)
    cleared = bytes((0, bytes(record)[1], bytes(record)[2], bytes(record)[3]))
    return {
        "target_city": target_city,
        "record_type": record_type,
        "cargo_gold": cargo_gold,
        "cargo_food": cargo_food,
        "target_gold": min(target_gold + cargo_gold, RESOURCE_CAP),
        "target_food": min(target_food + cargo_food, RESOURCE_CAP),
        "record": cleared,
        "record_hex": cleared.hex().upper(),
    }


def advance_calendar_when_no_record(*, year_byte: int, month_byte: int) -> tuple[int, int]:
    """Model only the no-active-record month/year update at 0x0166C4..0x0166D4."""

    for name, value in (("year_byte", year_byte), ("month_byte", month_byte)):
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 0xFF:
            raise TransportFlowError(f"{name} must be an unsigned byte")
    month_byte = (month_byte + 1) & 0xFF
    if month_byte >= 12:
        year_byte = (year_byte + 1) & 0xFF
        month_byte = 0
    return year_byte, month_byte


def ai_cargo_choice(*, source_gold: int, source_food: int) -> int | None:
    """Exact choice arithmetic from 0x032404..0x032448.

    The association with an AI transport sender remains semantically probable.
    ``None`` corresponds to D0.w == 0xFFFF.
    """

    if any(isinstance(value, bool) or not isinstance(value, int) or value < 0
           for value in (source_gold, source_food)):
        raise TransportFlowError("AI source resources must be nonnegative integers")
    if source_gold >= 20_000:
        return 2 if source_food >= 20_000 else 0
    if source_food >= 20_000:
        return 1
    return None


def ai_destination_food_need(officer_troops: Sequence[int]) -> int:
    """Exact normal-domain arithmetic in helper 0x0324AC..0x0324EC.

    The caller contributes ``troops + 100`` for each officer whose low-six-bit
    city code matches, takes unsigned floor division by ten, then multiplies
    the quotient by nine.
    """

    total = 0
    for troops in officer_troops:
        if isinstance(troops, bool) or not isinstance(troops, int) or not 0 <= troops <= 0xFFFFFFFF:
            raise TransportFlowError("officer troop quantities must be unsigned BE32-domain integers")
        total += troops + 100
    return 9 * (total // 10)


def ai_destination_model(
    *,
    source_city: int,
    active_force_code: int,
    city_force_codes: Mapping[int, int],
    city_skip_bytes: Mapping[int, int],
    city_gold: Mapping[int, int],
    city_food: Mapping[int, int],
    officers: Sequence[tuple[int, int]],
) -> dict[str, Any]:
    """Model the bounded probable AI destination loop at 0x03244A..0x0324AA.

    Candidate cities are scanned from 40 down to 1.  A candidate must match
    the active force byte, have a zero skip byte, differ from the source, and
    have food below the exact helper requirement.  The strict comparison on
    ``gold + food`` preserves the first (therefore highest city ID) on ties.
    """

    _check_city(source_city)
    if isinstance(active_force_code, bool) or not isinstance(active_force_code, int) or not 0 <= active_force_code <= 0xFF:
        raise TransportFlowError("active_force_code must be an unsigned byte")
    grouped: dict[int, list[int]] = {city: [] for city in range(1, CITY_COUNT + 1)}
    for raw_city, troops in officers:
        if isinstance(raw_city, bool) or not isinstance(raw_city, int) or not 0 <= raw_city <= 0xFF:
            raise TransportFlowError("officer city values must be unsigned bytes")
        city = raw_city & 0x3F
        if isinstance(troops, bool) or not isinstance(troops, int) or not 0 <= troops <= 0xFFFFFFFF:
            raise TransportFlowError("officer troop quantity must be an unsigned integer")
        if 1 <= city <= CITY_COUNT:
            grouped[city].append(troops)
    best_city: int | None = None
    best_total = 0xFFFFFFFF
    candidates: list[dict[str, Any]] = []
    for city in range(CITY_COUNT, 0, -1):
        try:
            force = city_force_codes[city]
            skip = city_skip_bytes[city]
            gold = city_gold[city]
            food = city_food[city]
        except KeyError as exc:
            raise TransportFlowError(f"missing AI city input for city {city}") from exc
        for name, value in (("force", force), ("skip", skip)):
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 0xFF:
                raise TransportFlowError(f"city {city} {name} must be an unsigned byte")
        for name, value in (("gold", gold), ("food", food)):
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 0xFFFFFFFF:
                raise TransportFlowError(f"city {city} {name} must be an unsigned BE32-domain integer")
        need = ai_destination_food_need(grouped[city])
        accepted = (
            (force & 0xFF) == active_force_code
            and skip == 0
            and city != source_city
            and food < need
        )
        total = (gold + food) & 0xFFFFFFFF
        selected_now = accepted and total < best_total
        if selected_now:
            best_total = total
            best_city = city
        if accepted:
            candidates.append({
                "city": city,
                "food_need": need,
                "gold_plus_food_u32": total,
                "selected_when_scanned": selected_now,
            })
    return {
        "destination_city": best_city,
        "best_gold_plus_food_u32": None if best_city is None else best_total,
        "scan_order": "40_down_to_1",
        "tie_policy": "highest_city_id_retained",
        "semantic_evidence": "probable",
        "candidates": candidates,
    }


def cargo_bundle(rom: bytes) -> dict[str, Any]:
    return {
        "format": CARGO_BUNDLE_FORMAT,
        "source": {
            "kind": "linear_bin",
            "size": CANONICAL_BIN_SIZE,
            "sha256": CANONICAL_BIN_SHA256,
        },
        "resource": {
            "id": "transport_cargo_table",
            "start": CARGO_TABLE_START,
            "end": CARGO_TABLE_END,
            "record_size": CARGO_RECORD_SIZE,
            "count": CARGO_COUNT,
            "encoding": "three fixed records: BE32 gold, BE32 food",
            "canonical_sha256": CARGO_TABLE_SHA256,
        },
        "entries": [
            {
                "choice_index": row["choice_index"],
                "record_type": row["record_type"],
                "label_zh": row["label_zh"],
                "gold": row["gold"],
                "food": row["food"],
            }
            for row in cargo_options(rom)
        ],
    }


def _strict_int(value: Any, *, name: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TransportFlowError(f"{name} must be an integer, not a boolean or another JSON type")
    if not minimum <= value <= maximum:
        raise TransportFlowError(f"{name} must be in {minimum}..{maximum}")
    return value


def serialize_cargo_bundle(bundle: Mapping[str, Any]) -> bytes:
    if not isinstance(bundle, Mapping):
        raise TransportFlowError("cargo bundle root must be a JSON object")
    if set(bundle) != {"format", "source", "resource", "entries"}:
        raise TransportFlowError("cargo bundle top-level fields are missing or unexpected")
    if bundle.get("format") != CARGO_BUNDLE_FORMAT:
        raise TransportFlowError("cargo bundle format mismatch")
    expected_source = {
        "kind": "linear_bin",
        "size": CANONICAL_BIN_SIZE,
        "sha256": CANONICAL_BIN_SHA256,
    }
    if bundle.get("source") != expected_source:
        raise TransportFlowError("cargo bundle source identity or shape changed")
    expected_resource = {
        "id": "transport_cargo_table",
        "start": CARGO_TABLE_START,
        "end": CARGO_TABLE_END,
        "record_size": CARGO_RECORD_SIZE,
        "count": CARGO_COUNT,
        "encoding": "three fixed records: BE32 gold, BE32 food",
        "canonical_sha256": CARGO_TABLE_SHA256,
    }
    if bundle.get("resource") != expected_resource:
        raise TransportFlowError("cargo resource relocation, count, encoding, or identity changed")
    entries = bundle.get("entries")
    if not isinstance(entries, list) or len(entries) != CARGO_COUNT:
        raise TransportFlowError("cargo bundle must contain exactly three entries")
    output = bytearray()
    for choice, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            raise TransportFlowError(f"cargo entry {choice} must be an object")
        if set(entry) != {"choice_index", "record_type", "label_zh", "gold", "food"}:
            raise TransportFlowError(f"cargo entry {choice} fields are missing or unexpected")
        if entry.get("choice_index") != choice or entry.get("record_type") != choice + 1:
            raise TransportFlowError(f"cargo entry {choice} index/type is fixed and cannot be reordered")
        if entry.get("label_zh") != CARGO_LABELS[choice]:
            raise TransportFlowError(f"cargo entry {choice} label is descriptive and immutable")
        gold = _strict_int(entry.get("gold"), name=f"entries[{choice}].gold", minimum=0, maximum=RESOURCE_CAP)
        food = _strict_int(entry.get("food"), name=f"entries[{choice}].food", minimum=0, maximum=RESOURCE_CAP)
        output += struct.pack(">II", gold, food)
    if len(output) != CARGO_TABLE_END - CARGO_TABLE_START:
        raise TransportFlowError("rebuilt cargo table length changed")
    return bytes(output)


def load_json_object(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink() or path.suffix.lower() != ".json":
        raise TransportFlowError(f"bundle must be a regular .json file: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TransportFlowError(f"malformed cargo bundle JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise TransportFlowError("cargo bundle root must be an object")
    return value


def _is_reparse_or_symlink(path: Path) -> bool:
    try:
        metadata = path.lstat()
    except (FileNotFoundError, NotADirectoryError):
        return False
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(metadata.st_mode) or bool(
        getattr(metadata, "st_file_attributes", 0) & reparse_flag
    )


def _assert_no_reparse_in_existing_chain(path: Path) -> None:
    """Reject every existing symlink/junction component from ``path`` to root."""

    candidate = Path(os.path.abspath(path))
    while True:
        if (candidate.exists() or candidate.is_symlink()) and _is_reparse_or_symlink(candidate):
            raise TransportFlowError(f"refusing output through symlink/reparse component: {candidate}")
        if candidate == candidate.parent:
            return
        candidate = candidate.parent


def _resolved_fresh_output(path: Path, *, suffix: str) -> Path:
    if path.suffix.lower() != suffix:
        raise TransportFlowError(f"output must use a {suffix} extension")
    if path.exists() or path.is_symlink():
        raise TransportFlowError(f"output already exists; refusing overwrite: {path}")
    _assert_no_reparse_in_existing_chain(path.parent)
    try:
        parent = path.parent.resolve(strict=True)
    except FileNotFoundError as exc:
        raise TransportFlowError(f"output parent does not exist: {path.parent}") from exc
    if not parent.is_dir() or _is_reparse_or_symlink(parent):
        raise TransportFlowError(f"output parent must be a real directory: {parent}")
    return parent / path.name


def extract_bundle(rom_path: Path, output_path: Path) -> dict[str, Any]:
    rom = canonical_bin(rom_path)
    output = _resolved_fresh_output(output_path, suffix=".json")
    if output == rom_path.resolve(strict=True):
        raise TransportFlowError("extract output collides with canonical ROM")
    bundle = cargo_bundle(rom)
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(bundle, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return bundle


def import_bundle(base_rom_path: Path, bundle_path: Path, output_rom_path: Path) -> dict[str, Any]:
    rom = canonical_bin(base_rom_path)
    output = _resolved_fresh_output(output_rom_path, suffix=".bin")
    if output == base_rom_path.resolve(strict=True):
        raise TransportFlowError("import output collides with canonical ROM")
    rebuilt_table = serialize_cargo_bundle(load_json_object(bundle_path))
    rebuilt = bytearray(rom)
    rebuilt[CARGO_TABLE_START:CARGO_TABLE_END] = rebuilt_table
    with output.open("xb") as handle:
        handle.write(rebuilt)
        handle.flush()
        os.fsync(handle.fileno())
    changed_offsets = [
        CARGO_TABLE_START + index
        for index, (before, after) in enumerate(zip(
            rom[CARGO_TABLE_START:CARGO_TABLE_END], rebuilt_table
        ))
        if before != after
    ]
    return {
        "output_size": len(rebuilt),
        "output_sha256": sha256_bytes(rebuilt),
        "cargo_table_sha256": sha256_bytes(rebuilt_table),
        "byte_identical_to_base": bytes(rebuilt) == rom,
        "changed_byte_count": len(changed_offsets),
        "changed_offsets": changed_offsets,
        "changed_offsets_hex": [f"0x{value:06X}" for value in changed_offsets],
        "changes_bounded_to_cargo_table": all(CARGO_TABLE_START <= value < CARGO_TABLE_END for value in changed_offsets),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify = subparsers.add_parser("verify", help="verify canonical BIN/SMD identities and static anchors")
    verify.add_argument("bin", type=Path)
    verify.add_argument("smd", type=Path)

    extract = subparsers.add_parser("extract", help="extract the fixed cargo table as JSON")
    extract.add_argument("bin", type=Path)
    extract.add_argument("output", type=Path)

    import_parser = subparsers.add_parser("import", help="import a fixed-shape cargo JSON into a fresh BIN")
    import_parser.add_argument("bin", type=Path)
    import_parser.add_argument("bundle", type=Path)
    import_parser.add_argument("output", type=Path)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "verify":
            rom = canonical_bin(args.bin)
            canonical_smd(args.smd)
            result = {
                "status": "PASS",
                "anchors": len(verify_anchors(rom)),
                "dispatch_target": f"0x{command_dispatch_target(rom):06X}",
            }
        elif args.command == "extract":
            result = extract_bundle(args.bin, args.output)
        else:
            result = import_bundle(args.bin, args.bundle, args.output)
    except TransportFlowError as exc:
        parser.error(str(exc))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
