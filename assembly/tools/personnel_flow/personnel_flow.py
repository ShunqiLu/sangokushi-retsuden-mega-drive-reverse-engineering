#!/usr/bin/env python3
"""Reproducible G-5510 personnel command and exploration analysis.

All ROM addresses in this module are linear BIN / 68000 addresses.  The
canonical input is identity-gated before any parsing or output is attempted.
The candidate-data importer always writes a new full-ROM copy and never
overwrites either its input or an existing output.
"""

from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import csv
import hashlib
import io
import json
import os
import struct
import tempfile
from pathlib import Path
from typing import Any, Iterable, Sequence


CANONICAL_SIZE = 1_048_576
CANONICAL_SHA256 = reference_value(__name__, 'CANONICAL_SHA256')
SCHEMA_VERSION = "g5510-personnel-flow-v1"
CANDIDATE_BUNDLE_FORMAT = "g5510-exploration-candidates-v1"

MENU_START = 0x0929F4
MENU_END = 0x092A16
DISPATCH_TABLE_START = 0x00E024
DISPATCH_TABLE_END = 0x00E050
DISPATCH_TARGET_BASE = 0x00E0EE
CANDIDATE_POINTER_TABLE = 0x011080
CANDIDATE_BLOCK_START = 0x0AADE2
CANDIDATE_BLOCK_END = 0x0AB8C4
SCENARIO_YEARS = (189, 200, 215)
FORCE_SELECTOR_CODES = (0x01, 0x05, 0x0A, 0x02)
CITY_OFFSET_WORD_COUNT = 41  # slot 0 is an invalid/dummy index; cities are 1..40.


class PersonnelFlowError(ValueError):
    """Raised when identity, structure, arithmetic, or output safety fails."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_be16(data: bytes | bytearray, offset: int) -> int:
    if offset < 0 or offset + 2 > len(data):
        raise PersonnelFlowError(f"BE16 read outside input at 0x{offset:X}")
    return struct.unpack_from(">H", data, offset)[0]


def read_be32(data: bytes | bytearray, offset: int) -> int:
    if offset < 0 or offset + 4 > len(data):
        raise PersonnelFlowError(f"BE32 read outside input at 0x{offset:X}")
    return struct.unpack_from(">I", data, offset)[0]


def pack_be16(value: int) -> bytes:
    return struct.pack(">H", require_u16(value, "BE16 value"))


def pack_be32(value: int) -> bytes:
    if type(value) is not int or not 0 <= value <= 0xFFFFFFFF:
        raise PersonnelFlowError(f"BE32 value must be an integer in 0..0xFFFFFFFF: {value!r}")
    return struct.pack(">I", value)


def require_u16(value: Any, label: str) -> int:
    if type(value) is not int or not 0 <= value <= 0xFFFF:
        raise PersonnelFlowError(f"{label} must be an integer in 0..0xFFFF: {value!r}")
    return value


def canonical_rom(path: Path) -> bytes:
    if not path.is_file():
        raise PersonnelFlowError(f"canonical ROM is missing: {path}")
    data = path.read_bytes()
    digest = sha256_bytes(data)
    if len(data) != CANONICAL_SIZE or digest != CANONICAL_SHA256:
        raise PersonnelFlowError(
            "canonical ROM identity mismatch: "
            f"size={len(data)} sha256={digest}; expected "
            f"size={CANONICAL_SIZE} sha256={CANONICAL_SHA256}"
        )
    return data


ANCHORS: tuple[dict[str, Any], ...] = (
    {"name": "MenuCommandRecords", "start": 0x0929F4, "end": 0x092A16,
     "sha256": reference_value(__name__, 'field'),
     "role": "category records and real menu-cell command bytes", "evidence": "confirmed"},
    {"name": "CommandDispatcher", "start": 0x00DFB0, "end": 0x00DFD8,
     "sha256": reference_value(__name__, 'field_2'),
     "role": "FFF579 normalization and indexed dispatch", "evidence": "confirmed"},
    {"name": "CommandDispatchTable", "start": 0x00E024, "end": 0x00E050,
     "sha256": reference_value(__name__, 'field_3'),
     "role": "22 signed BE16 offsets for commands 0x04..0x19", "evidence": "confirmed"},
    {"name": "PersonnelDispatcher", "start": 0x00FC82, "end": 0x00FC98,
     "sha256": reference_value(__name__, 'field_4'),
     "role": "command 0x16 subcommand discriminator", "evidence": "confirmed"},
    {"name": "ExplorationCore", "start": 0x010A58, "end": 0x010AA8,
     "sha256": reference_value(__name__, 'field_5'),
     "role": "exploration action write, candidate call, and zero/nonzero branch", "evidence": "confirmed"},
    {"name": "DifficultyTable", "start": 0x010A4C, "end": 0x010A58,
     "sha256": reference_value(__name__, 'field_6'),
     "role": "three raw multiplier/addend pairs selected by FFEFD2", "evidence": "confirmed"},
    {"name": "ExplorationScoreAndBand", "start": 0x010AA8, "end": 0x010B24,
     "sha256": reference_value(__name__, 'field_7'),
     "role": "word-truncated score and seven-band selector", "evidence": "confirmed"},
    {"name": "ResultTable", "start": 0x010B24, "end": 0x010C74,
     "sha256": reference_value(__name__, 'field_8'),
     "role": "7 x 6 x 4 BE16 raw outcome-code table", "evidence": "confirmed"},
    {"name": "ResultChooser", "start": 0x010C74, "end": 0x010D0C,
     "sha256": reference_value(__name__, 'field_9'),
     "role": "candidate/RNG selection and player-force gate", "evidence": "confirmed"},
    {"name": "ResultDispatchTable", "start": 0x010D0C, "end": 0x010D14,
     "sha256": reference_value(__name__, 'field_10'),
     "role": "four BE16 handler offsets indexed by raw codes 0/2/4/6", "evidence": "confirmed"},
    {"name": "ZeroResultHandler", "start": 0x010D14, "end": 0x010D36,
     "sha256": reference_value(__name__, 'field_11'),
     "role": "zero-result growth call and downstream message setup", "evidence": "confirmed"},
    {"name": "GrowthHelper", "start": 0x010E12, "end": 0x010E38,
     "sha256": reference_value(__name__, 'field_12'),
     "role": "RNG call and selected-officer FFC000 word increment", "evidence": "confirmed"},
    {"name": "CandidatePointerTable", "start": 0x011080, "end": 0x01108C,
     "sha256": reference_value(__name__, 'field_13'),
     "role": "three scenario candidate-descriptor pointers", "evidence": "confirmed"},
    {"name": "CandidateBuilder", "start": 0x01108C, "end": 0x0111A6,
     "sha256": reference_value(__name__, 'field_14'),
     "role": "priority force/year, city rule, and high-bit CC00 candidate construction", "evidence": "confirmed"},
    {"name": "CandidateDataBlock", "start": 0x0AADE2, "end": 0x0AB8C4,
     "sha256": reference_value(__name__, 'field_15'),
    "role": "three contiguous variable-length exploration candidate scenarios", "evidence": "confirmed"},
)

_DATA_ANCHORS = {
    "MenuCommandRecords", "CommandDispatchTable", "DifficultyTable", "ResultTable",
    "ResultDispatchTable", "CandidatePointerTable", "CandidateDataBlock",
}
_ANCHOR_SEMANTIC_SCOPE: dict[str, tuple[str, str]] = {
    "MenuCommandRecords": ("confirmed", "all 22 menu cells and labels observed in real prompt-base UI"),
    "CommandDispatcher": ("confirmed", "mechanics static; real UI command values observed; personnel target executed"),
    "CommandDispatchTable": ("confirmed", "all 22 offsets/targets static; command 0x16 target executed here"),
    "PersonnelDispatcher": ("confirmed", "0x21 exploration executed; non-0x21 fallback static and 0x46 UI-only"),
    "ExplorationCore": ("confirmed", "default zero-candidate path executed through its result handler"),
    "DifficultyTable": ("probable", "static nonzero-candidate score path; not naturally executed here"),
    "ExplorationScoreAndBand": ("probable", "static nonzero-candidate path; not naturally executed here"),
    "ResultTable": ("probable", "shape and raw words confirmed; natural nonzero result not executed"),
    "ResultChooser": ("probable", "static candidate/RNG access; natural nonzero result not executed"),
    "ResultDispatchTable": ("probable", "raw targets confirmed; only code-0 target executed naturally"),
    "ZeroResultHandler": ("confirmed", "natural scenario-0 zero-candidate execution reached 010D34 return"),
    "GrowthHelper": ("confirmed", "natural execution changed RNG and FFC000[CC] by +3"),
    "CandidatePointerTable": ("confirmed", "scenario-0 descriptor selected in natural zero-candidate execution"),
    "CandidateBuilder": ("probable", "routine executed and returned zero; detailed rule meanings recovered statically"),
    "CandidateDataBlock": ("probable", "byte layout/round-trip confirmed; candidate meanings recovered statically"),
}
ANCHORS = tuple(
    {
        **row,
        "primary_role": "m68k_data" if row["name"] in _DATA_ANCHORS else "m68k_code",
        "semantic_evidence": _ANCHOR_SEMANTIC_SCOPE[row["name"]][0],
        "runtime_scope": _ANCHOR_SEMANTIC_SCOPE[row["name"]][1],
    }
    for row in ANCHORS
)


def verify_anchor(rom: bytes | bytearray, anchor: dict[str, Any]) -> str | None:
    observed = sha256_bytes(bytes(rom[anchor["start"]:anchor["end"]]))
    if observed == anchor["sha256"]:
        return None
    return f"{anchor['name']}: observed {observed}, expected {anchor['sha256']}"


def verify_anchors(rom: bytes | bytearray) -> list[str]:
    return [failure for row in ANCHORS if (failure := verify_anchor(rom, row))]


COMMAND_DEFINITIONS: tuple[dict[str, Any], ...] = (
    {"command": 0x04, "category": "domestic", "category_zh": "內政", "label": "開發", "slug": "development", "row": 0, "column": 0, "menu_offset": 0x0929FA},
    {"command": 0x05, "category": "domestic", "category_zh": "內政", "label": "調動", "slug": "transfer", "row": 0, "column": 1, "menu_offset": 0x0929FB},
    {"command": 0x06, "category": "domestic", "category_zh": "內政", "label": "情報", "slug": "domestic-information", "row": 0, "column": 2, "menu_offset": 0x0929FC},
    {"command": 0x07, "category": "domestic", "category_zh": "內政", "label": "福利", "slug": "welfare", "row": 1, "column": 0, "menu_offset": 0x0929FD},
    {"command": 0x08, "category": "domestic", "category_zh": "內政", "label": "任命", "slug": "appointment", "row": 1, "column": 1, "menu_offset": 0x0929FE},
    {"command": 0x09, "category": "domestic", "category_zh": "內政", "label": "稅率", "slug": "tax-rate", "row": 1, "column": 2, "menu_offset": 0x0929FF},
    {"command": 0x0A, "category": "domestic", "category_zh": "內政", "label": "教育", "slug": "education", "row": 2, "column": 0, "menu_offset": 0x092A00},
    {"command": 0x0B, "category": "domestic", "category_zh": "內政", "label": "運輸", "slug": "transport", "row": 2, "column": 1, "menu_offset": 0x092A01},
    {"command": 0x0C, "category": "domestic", "category_zh": "內政", "label": "結束", "slug": "domestic-end", "row": 2, "column": 2, "menu_offset": 0x092A02},
    {"command": 0x0D, "category": "diplomacy", "category_zh": "外交", "label": "同盟", "slug": "alliance", "row": 0, "column": 0, "menu_offset": 0x092A05},
    {"command": 0x0E, "category": "diplomacy", "category_zh": "外交", "label": "借債", "slug": "borrow", "row": 0, "column": 1, "menu_offset": 0x092A06},
    {"command": 0x0F, "category": "diplomacy", "category_zh": "外交", "label": "情報", "slug": "diplomacy-information", "row": 0, "column": 2, "menu_offset": 0x092A07},
    {"command": 0x10, "category": "diplomacy", "category_zh": "外交", "label": "計策", "slug": "stratagem", "row": 1, "column": 0, "menu_offset": 0x092A08},
    {"command": 0x11, "category": "diplomacy", "category_zh": "外交", "label": "還債", "slug": "repay", "row": 1, "column": 1, "menu_offset": 0x092A09},
    {"command": 0x12, "category": "diplomacy", "category_zh": "外交", "label": "結束", "slug": "diplomacy-end", "row": 1, "column": 2, "menu_offset": 0x092A0A},
    {"command": 0x13, "category": "military", "category_zh": "軍備", "label": "徵兵", "slug": "recruitment", "row": 0, "column": 0, "menu_offset": 0x092A0D},
    {"command": 0x14, "category": "military", "category_zh": "軍備", "label": "武器", "slug": "weapons", "row": 0, "column": 1, "menu_offset": 0x092A0E},
    {"command": 0x15, "category": "military", "category_zh": "軍備", "label": "情報", "slug": "military-information", "row": 0, "column": 2, "menu_offset": 0x092A0F},
    {"command": 0x16, "category": "military", "category_zh": "軍備", "label": "人材", "slug": "personnel", "row": 1, "column": 0, "menu_offset": 0x092A10},
    {"command": 0x17, "category": "military", "category_zh": "軍備", "label": "防衛", "slug": "defense", "row": 1, "column": 1, "menu_offset": 0x092A11},
    {"command": 0x19, "category": "military", "category_zh": "軍備", "label": "訓練", "slug": "training", "row": 1, "column": 2, "menu_offset": 0x092A12},
    {"command": 0x18, "category": "military", "category_zh": "軍備", "label": "結束", "slug": "military-end", "row": 2, "column": 1, "menu_offset": 0x092A14},
)


def dispatch_rows(rom: bytes) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for table_order, command in enumerate(range(0x04, 0x1A)):
        offset = DISPATCH_TABLE_START + table_order * 2
        raw = read_be16(rom, offset)
        signed = raw - 0x10000 if raw & 0x8000 else raw
        target = (DISPATCH_TARGET_BASE + signed) & 0xFFFFFFFF
        rows.append({
            "table_order": table_order,
            "command": command,
            "command_hex": f"0x{command:02X}",
            "table_rom_offset": offset,
            "table_rom_offset_hex": f"0x{offset:06X}",
            "raw_offset": raw,
            "raw_offset_hex": f"0x{raw:04X}",
            "signed_offset": signed,
            "target": target,
            "target_hex": f"0x{target:06X}",
            "evidence": "confirmed",
            "evidence_detail": "exact_44_byte_table_and_68000_indexed_jsr",
        })
    return rows


def command_catalog(rom: bytes) -> list[dict[str, Any]]:
    table = {row["command"]: row for row in dispatch_rows(rom)}
    rows: list[dict[str, Any]] = []
    for menu_order, definition in enumerate(COMMAND_DEFINITIONS):
        command = definition["command"]
        if rom[definition["menu_offset"]] != command:
            raise PersonnelFlowError(
                f"menu command mismatch at 0x{definition['menu_offset']:06X}: "
                f"observed 0x{rom[definition['menu_offset']]:02X}, expected 0x{command:02X}"
            )
        dispatch = table[command]
        rows.append({
            **definition,
            "menu_order": menu_order,
            "table_order": dispatch["table_order"],
            "command_hex": f"0x{command:02X}",
            "menu_rom_offset_hex": f"0x{definition['menu_offset']:06X}",
            "command_ram": "0xFFF579",
            "ui_evidence": "confirmed",
            "ui_evidence_detail": "real_prompt_base_menu_and_bounded_per_item_FFF579_replay",
            "dispatch_table_rom_offset": dispatch["table_rom_offset"],
            "dispatch_table_rom_offset_hex": dispatch["table_rom_offset_hex"],
            "dispatch_raw_offset": dispatch["raw_offset"],
            "dispatch_raw_offset_hex": dispatch["raw_offset_hex"],
            "handler_target": dispatch["target"],
            "handler_target_hex": dispatch["target_hex"],
            "handler_evidence": "confirmed",
            "handler_evidence_detail": "static_dispatch_table_decode",
            "handler_runtime_scope": (
                "confirmed_real_ui_to_handler_and_core_in_this_bundle"
                if command == 0x16 else "not_replayed_to_handler_by_this_bundle"
            ),
        })
    return rows


def menu_layout(rom: bytes) -> list[dict[str, Any]]:
    by_position = {
        (row["category"], row["row"], row["column"]): row
        for row in command_catalog(rom)
    }
    result: list[dict[str, Any]] = []
    categories = (
        ("domestic", "內政", 3, 0x0929FA),
        ("diplomacy", "外交", 2, 0x092A05),
        ("military", "軍備", 3, 0x092A0D),
    )
    for category, category_zh, row_count, start in categories:
        for row_index in range(row_count):
            for column in range(3):
                item = by_position.get((category, row_index, column))
                rom_offset = start + row_index * 3 + column
                value = rom[rom_offset]
                if item is None and value != 0:
                    raise PersonnelFlowError(
                        f"unexpected nonzero blank menu cell at 0x{rom_offset:06X}"
                    )
                result.append({
                    "category": category,
                    "category_zh": category_zh,
                    "row": row_index,
                    "column": column,
                    "menu_rom_offset": rom_offset,
                    "menu_rom_offset_hex": f"0x{rom_offset:06X}",
                    "raw_value": value,
                    "raw_value_hex": f"0x{value:02X}",
                    "is_blank": item is None,
                    "command_hex": "" if item is None else item["command_hex"],
                    "label": "" if item is None else item["label"],
                    "menu_order": "" if item is None else item["menu_order"],
                    "evidence": "confirmed",
                    "evidence_detail": "exact_menu_byte_plus_real_prompt_base_layout",
                })
    return result


def personnel_subcommand_target(subcommand: int) -> dict[str, Any]:
    require_u16(subcommand, "subcommand")
    byte_value = subcommand & 0xFF
    if byte_value == 0x21:
        return {"subcommand_byte": byte_value, "target": 0x010A58, "path": "exploration"}
    return {
        "subcommand_byte": byte_value,
        "target": 0x0111AC,
        "path": "selection_fallback_for_every_value_other_than_0x21",
    }


DIFFICULTY_PAIRS = ((0x0065, 0x0064), (0x0065, 0x0032), (0x0033, 0x0000))
SCORE_BAND_MAXIMA = (0x0032, 0x0064, 0x0096, 0x00C8, 0x00FA, 0x012C)


def difficulty_adjustment(rng_d0_low_word: int, selector_index: int) -> int:
    rng = require_u16(rng_d0_low_word, "rng_d0_low_word")
    if type(selector_index) is not int or not 0 <= selector_index < len(DIFFICULTY_PAIRS):
        raise PersonnelFlowError(
            f"FFEFD2 selector must be 0..2 for the 12-byte table: {selector_index!r}"
        )
    multiplier, addend = DIFFICULTY_PAIRS[selector_index]
    return (((rng * multiplier) >> 16) + addend) & 0xFFFF


def wrapped_exploration_score(
    virtue_byte: int, intelligence_word: int, rng_d0_low_word: int, selector_index: int
) -> int:
    if type(virtue_byte) is not int or not 0 <= virtue_byte <= 0xFF:
        raise PersonnelFlowError(f"virtue_byte must be 0..255: {virtue_byte!r}")
    intelligence = require_u16(intelligence_word, "intelligence_word")
    return (virtue_byte + intelligence + difficulty_adjustment(rng_d0_low_word, selector_index)) & 0xFFFF


def score_band(score_word: int) -> int:
    score = require_u16(score_word, "score_word")
    for index, maximum in enumerate(SCORE_BAND_MAXIMA):
        if score <= maximum:
            return index
    return 6


def intelligence_band(intelligence_word: int) -> int:
    value = require_u16(intelligence_word, "intelligence_word")
    for index, maximum in enumerate((30, 60, 80, 90, 100)):
        if value <= maximum:
            return index
    return 5


def result_table(rom: bytes) -> list[list[list[int]]]:
    words = [read_be16(rom, 0x010B24 + index * 2) for index in range(168)]
    if any(value not in (0, 2, 4, 6) for value in words):
        raise PersonnelFlowError("result table contains a value outside raw codes 0/2/4/6")
    return [
        [
            words[(score_index * 6 + intel_index) * 4:(score_index * 6 + intel_index + 1) * 4]
            for intel_index in range(6)
        ]
        for score_index in range(7)
    ]


def result_cell(rom: bytes, score_index: int, intel_index: int, rng_class: int) -> int:
    if type(score_index) is not int or not 0 <= score_index < 7:
        raise PersonnelFlowError(f"score band must be 0..6: {score_index!r}")
    if type(intel_index) is not int or not 0 <= intel_index < 6:
        raise PersonnelFlowError(f"intelligence band must be 0..5: {intel_index!r}")
    if type(rng_class) is not int or not 0 <= rng_class < 4:
        raise PersonnelFlowError(f"RNG class must be 0..3: {rng_class!r}")
    return result_table(rom)[score_index][intel_index][rng_class]


RESULT_HANDLER_TARGETS = {0: 0x010D14, 2: 0x010D64, 4: 0x010D64, 6: 0x010DB4}


def result_handler_target(raw_code: int) -> int:
    if raw_code not in RESULT_HANDLER_TARGETS:
        raise PersonnelFlowError(
            f"raw result code is a byte offset and must be one of 0/2/4/6: {raw_code!r}"
        )
    return RESULT_HANDLER_TARGETS[raw_code]


def candidate_count(return_word: int) -> dict[str, Any]:
    value = require_u16(return_word, "candidate return word")
    return {"raw_word": value, "priority_force_year_flag": bool(value & 0x8000), "count": value & 0x7FFF}


def zero_result_growth_increment(rng_word_after_0x0083D4: int) -> int:
    value = require_u16(rng_word_after_0x0083D4, "post-RNG word stored at FFF61C")
    return ((value * 3) >> 16) + 1


def _parse_force_list(rom: bytes, start: int, maximum_end: int, label: str) -> tuple[list[dict[str, int]], int, int]:
    entries: list[dict[str, int]] = []
    cursor = start
    while True:
        if cursor + 2 > maximum_end:
            raise PersonnelFlowError(f"{label}: missing negative terminator before 0x{maximum_end:06X}")
        year = read_be16(rom, cursor)
        if year & 0x8000:
            return entries, year, cursor
        if cursor + 4 > maximum_end:
            raise PersonnelFlowError(f"{label}: truncated year/officer record at 0x{cursor:06X}")
        entries.append({"year_threshold_raw": year, "officer_id": read_be16(rom, cursor + 2)})
        cursor += 4


def qualifier_details(raw: int) -> dict[str, Any]:
    value = require_u16(raw, "qualifier_raw")
    if value & 0x8000:
        return {"qualifier_kind": "unconditional_flagged", "qualifier_value": value & 0x7FFF}
    if value & 0x4000:
        return {"qualifier_kind": "literal_force_code", "qualifier_value": value & 0xFF}
    return {"qualifier_kind": "reference_officer_id", "qualifier_value": value}


def _parse_city_rules(
    rom: bytes, start: int, end: int, scenario_index: int, city_id: int
) -> tuple[list[dict[str, Any]], int]:
    entries: list[dict[str, Any]] = []
    cursor = start
    while True:
        if cursor + 2 > end:
            raise PersonnelFlowError(
                f"scenario {scenario_index} city {city_id}: missing terminator before 0x{end:06X}"
            )
        year = read_be16(rom, cursor)
        if year & 0x8000:
            cursor += 2
            if cursor != end:
                raise PersonnelFlowError(
                    f"scenario {scenario_index} city {city_id}: bytes remain after terminator at 0x{cursor:06X}"
                )
            return entries, year
        if cursor + 6 > end:
            raise PersonnelFlowError(
                f"scenario {scenario_index} city {city_id}: truncated six-byte rule at 0x{cursor:06X}"
            )
        officer = read_be16(rom, cursor + 2)
        qualifier = read_be16(rom, cursor + 4)
        entries.append({
            "year_threshold_raw": year,
            "candidate_officer_id": officer,
            "qualifier_raw": qualifier,
            **qualifier_details(qualifier),
        })
        cursor += 6


def parse_candidate_scenarios(rom: bytes) -> list[dict[str, Any]]:
    scenario_starts = [read_be32(rom, CANDIDATE_POINTER_TABLE + index * 4) for index in range(3)]
    if scenario_starts[0] != CANDIDATE_BLOCK_START or scenario_starts != sorted(scenario_starts):
        raise PersonnelFlowError(f"unexpected candidate scenario pointer table: {scenario_starts!r}")
    scenario_ends = scenario_starts[1:] + [CANDIDATE_BLOCK_END]
    scenarios: list[dict[str, Any]] = []
    for scenario_index, (year, start, end) in enumerate(zip(SCENARIO_YEARS, scenario_starts, scenario_ends)):
        pointers = [read_be32(rom, start + index * 4) for index in range(6)]
        if pointers[0] != start + 24:
            raise PersonnelFlowError(f"scenario {scenario_index}: first list does not follow descriptor")
        if not (pointers[0] < pointers[1] < pointers[2] <= pointers[3] <= pointers[4] < pointers[5] < end):
            raise PersonnelFlowError(f"scenario {scenario_index}: invalid descriptor pointer order {pointers!r}")

        force_lists: list[dict[str, Any]] = []
        for slot in range(4):
            maximum_end = pointers[slot + 1] if slot < 3 else pointers[4] + 2
            entries, terminator, terminator_offset = _parse_force_list(
                rom, pointers[slot], maximum_end, f"scenario {scenario_index} force slot {slot}"
            )
            expected_terminator_offset = pointers[slot + 1] - 2 if slot < 3 else pointers[4]
            if terminator_offset != expected_terminator_offset:
                raise PersonnelFlowError(
                    f"scenario {scenario_index} force slot {slot}: terminator at "
                    f"0x{terminator_offset:06X}, expected 0x{expected_terminator_offset:06X}"
                )
            force_lists.append({
                "slot": slot,
                "selector_force_code": FORCE_SELECTOR_CODES[slot],
                "rom_offset": pointers[slot],
                "rom_offset_hex": f"0x{pointers[slot]:06X}",
                "entries": entries,
                "terminator_raw": terminator,
                "terminator_rom_offset": terminator_offset,
                "terminator_rom_offset_hex": f"0x{terminator_offset:06X}",
                "terminator_aliases_city_offset_entry_zero": slot == 3,
            })

        city_offsets = [read_be16(rom, pointers[4] + index * 2) for index in range(CITY_OFFSET_WORD_COUNT)]
        if city_offsets[0] != force_lists[3]["terminator_raw"] or not city_offsets[0] & 0x8000:
            raise PersonnelFlowError(
                f"scenario {scenario_index}: fourth force-list terminator/city offset[0] alias is not preserved"
            )
        usable_offsets = city_offsets[1:]
        if usable_offsets[0] != 0 or any(value & 1 for value in usable_offsets):
            raise PersonnelFlowError(f"scenario {scenario_index}: invalid city offset table")
        if usable_offsets != sorted(usable_offsets):
            raise PersonnelFlowError(f"scenario {scenario_index}: city offsets are not monotonic")

        city_rules: list[dict[str, Any]] = []
        for city_id in range(1, 41):
            relative = city_offsets[city_id]
            relative_end = city_offsets[city_id + 1] if city_id < 40 else end - pointers[5]
            if relative_end < relative or pointers[5] + relative_end > end:
                raise PersonnelFlowError(f"scenario {scenario_index} city {city_id}: invalid rule bounds")
            entries, terminator = _parse_city_rules(
                rom, pointers[5] + relative, pointers[5] + relative_end, scenario_index, city_id
            )
            city_rules.append({
                "city_id": city_id,
                "relative_offset": relative,
                "relative_offset_hex": f"0x{relative:04X}",
                "rom_offset": pointers[5] + relative,
                "rom_offset_hex": f"0x{pointers[5] + relative:06X}",
                "entries": entries,
                "terminator_raw": terminator,
            })

        qualifier_counts = {key: 0 for key in ("unconditional_flagged", "literal_force_code", "reference_officer_id")}
        for city in city_rules:
            for entry in city["entries"]:
                qualifier_counts[entry["qualifier_kind"]] += 1
        scenario_bytes = rom[start:end]
        scenarios.append({
            "scenario_index": scenario_index,
            "scenario_year": year,
            "descriptor_rom_offset": start,
            "descriptor_rom_offset_hex": f"0x{start:06X}",
            "scenario_end": end,
            "scenario_end_hex": f"0x{end:06X}",
            "scenario_length": end - start,
            "scenario_sha256": sha256_bytes(scenario_bytes),
            "descriptor_pointers": pointers,
            "descriptor_pointers_hex": [f"0x{pointer:06X}" for pointer in pointers],
            "force_year_lists": force_lists,
            "city_offset_table_rom_offset": pointers[4],
            "city_offset_table_rom_offset_hex": f"0x{pointers[4]:06X}",
            "city_offset_words": city_offsets,
            "city_rule_stream_rom_offset": pointers[5],
            "city_rule_stream_rom_offset_hex": f"0x{pointers[5]:06X}",
            "city_rules": city_rules,
            "shared_alias": {
                "rom_offset": pointers[4],
                "rom_offset_hex": f"0x{pointers[4]:06X}",
                "raw_word": city_offsets[0],
                "roles": ["force_year_list_3_terminator", "city_offset_table_entry_0"],
                "evidence": "confirmed",
            },
            "statistics": {
                "force_year_entry_counts": [len(row["entries"]) for row in force_lists],
                "force_year_entry_total": sum(len(row["entries"]) for row in force_lists),
                "city_rule_count": sum(len(row["entries"]) for row in city_rules),
                "nonempty_city_count": sum(bool(row["entries"]) for row in city_rules),
                "max_rules_per_city": max(len(row["entries"]) for row in city_rules),
                "qualifier_counts": qualifier_counts,
            },
        })
    return scenarios


def candidate_bundle(rom: bytes) -> dict[str, Any]:
    scenarios = parse_candidate_scenarios(rom)
    return {
        "format": CANDIDATE_BUNDLE_FORMAT,
        "canonical_source": {"size": len(rom), "sha256": sha256_bytes(rom)},
        "candidate_block": {
            "start": CANDIDATE_BLOCK_START,
            "start_hex": f"0x{CANDIDATE_BLOCK_START:06X}",
            "end": CANDIDATE_BLOCK_END,
            "end_hex": f"0x{CANDIDATE_BLOCK_END:06X}",
            "length": CANDIDATE_BLOCK_END - CANDIDATE_BLOCK_START,
            "sha256": sha256_bytes(rom[CANDIDATE_BLOCK_START:CANDIDATE_BLOCK_END]),
        },
        "scenario_pointer_table": {
            "rom_offset": CANDIDATE_POINTER_TABLE,
            "rom_offset_hex": f"0x{CANDIDATE_POINTER_TABLE:06X}",
            "count": 3,
        },
        "semantics_boundary": (
            "Names describe proven access shape. Year/force/qualifier meanings are static interpretations; "
            "natural nonzero outcome branches and selection subcommand 0x46 were not executed."
        ),
        "scenarios": scenarios,
    }


def _entry_u16(entry: dict[str, Any], key: str, label: str) -> int:
    if not isinstance(entry, dict) or key not in entry:
        raise PersonnelFlowError(f"{label}: missing {key}")
    return require_u16(entry[key], f"{label}.{key}")


def _serialize_candidate_scenario(
    supplied: dict[str, Any], baseline: dict[str, Any]
) -> bytes:
    if not isinstance(supplied, dict):
        raise PersonnelFlowError("scenario entry must be an object")
    if supplied.get("scenario_index") != baseline["scenario_index"]:
        raise PersonnelFlowError("scenario indices must remain ordered and unchanged")
    if supplied.get("scenario_year") != baseline["scenario_year"]:
        raise PersonnelFlowError("scenario year labels must remain unchanged")
    if supplied.get("descriptor_rom_offset") != baseline["descriptor_rom_offset"]:
        raise PersonnelFlowError("scenario descriptor offsets must remain unchanged")
    if supplied.get("descriptor_pointers") != baseline["descriptor_pointers"]:
        raise PersonnelFlowError("scenario descriptor pointers must remain unchanged")
    force_lists = supplied.get("force_year_lists")
    city_rules = supplied.get("city_rules")
    city_offsets = supplied.get("city_offset_words")
    if not isinstance(force_lists, list) or len(force_lists) != 4:
        raise PersonnelFlowError("each scenario must contain exactly four force_year_lists")
    if not isinstance(city_rules, list) or len(city_rules) != 40:
        raise PersonnelFlowError("each scenario must contain exactly 40 city rule lists")
    if not isinstance(city_offsets, list) or len(city_offsets) != 41:
        raise PersonnelFlowError("each scenario must preserve exactly 41 city offset words")

    start = baseline["descriptor_rom_offset"]
    payload = bytearray(b"\0" * 24)
    pointers: list[int] = []
    for slot, (row, expected) in enumerate(zip(force_lists, baseline["force_year_lists"])):
        if not isinstance(row, dict) or row.get("slot") != slot:
            raise PersonnelFlowError(f"scenario {baseline['scenario_index']}: force list slots must be 0..3")
        if row.get("selector_force_code") != FORCE_SELECTOR_CODES[slot]:
            raise PersonnelFlowError(f"scenario {baseline['scenario_index']} force slot {slot}: selector code changed")
        entries = row.get("entries")
        if not isinstance(entries, list) or len(entries) != len(expected["entries"]):
            raise PersonnelFlowError(
                f"scenario {baseline['scenario_index']} force slot {slot}: record-count changes are unsafe"
            )
        pointers.append(start + len(payload))
        for entry_index, entry in enumerate(entries):
            label = f"scenario {baseline['scenario_index']} force {slot} entry {entry_index}"
            payload += pack_be16(_entry_u16(entry, "year_threshold_raw", label))
            payload += pack_be16(_entry_u16(entry, "officer_id", label))
        terminator = _entry_u16(row, "terminator_raw", f"scenario {baseline['scenario_index']} force {slot}")
        if not terminator & 0x8000:
            raise PersonnelFlowError("force-list terminators must retain bit 15")
        if slot < 3:
            payload += pack_be16(terminator)

    # The fourth list's terminator is deliberately not appended separately.
    # It is the same physical word as city-offset entry zero.
    pointers.append(start + len(payload))
    alias_word = require_u16(city_offsets[0], "city_offset_words[0]")
    fourth_terminator = require_u16(force_lists[3]["terminator_raw"], "force list 3 terminator")
    if alias_word != fourth_terminator or not alias_word & 0x8000:
        raise PersonnelFlowError(
            "force list 3 terminator and city offset entry 0 must remain one shared negative word"
        )

    rule_stream = bytearray()
    rebuilt_offsets = [alias_word]
    for city_index, (city, expected_city) in enumerate(zip(city_rules, baseline["city_rules"]), start=1):
        if not isinstance(city, dict) or city.get("city_id") != city_index:
            raise PersonnelFlowError("city IDs must remain ordered 1..40")
        entries = city.get("entries")
        if not isinstance(entries, list) or len(entries) != len(expected_city["entries"]):
            raise PersonnelFlowError(
                f"scenario {baseline['scenario_index']} city {city_index}: record-count changes are unsafe"
            )
        rebuilt_offsets.append(len(rule_stream))
        if city.get("relative_offset") != rebuilt_offsets[-1]:
            raise PersonnelFlowError(
                f"scenario {baseline['scenario_index']} city {city_index}: relative offset is inconsistent"
            )
        for entry_index, entry in enumerate(entries):
            label = f"scenario {baseline['scenario_index']} city {city_index} entry {entry_index}"
            year = _entry_u16(entry, "year_threshold_raw", label)
            officer = _entry_u16(entry, "candidate_officer_id", label)
            qualifier = _entry_u16(entry, "qualifier_raw", label)
            decoded_qualifier = qualifier_details(qualifier)
            if entry.get("qualifier_kind") != decoded_qualifier["qualifier_kind"] or entry.get("qualifier_value") != decoded_qualifier["qualifier_value"]:
                raise PersonnelFlowError(f"{label}: decoded qualifier fields do not match qualifier_raw")
            if year & 0x8000:
                raise PersonnelFlowError(f"{label}: nonterminator year must not have bit 15")
            payload_entry = pack_be16(year) + pack_be16(officer) + pack_be16(qualifier)
            rule_stream += payload_entry
        terminator = _entry_u16(city, "terminator_raw", f"scenario {baseline['scenario_index']} city {city_index}")
        if not terminator & 0x8000:
            raise PersonnelFlowError("city rule terminators must retain bit 15")
        rule_stream += pack_be16(terminator)

    supplied_offsets = [require_u16(value, f"city_offset_words[{index}]") for index, value in enumerate(city_offsets)]
    if supplied_offsets != rebuilt_offsets:
        raise PersonnelFlowError("city offset words do not exactly match the variable rule stream")
    for value in rebuilt_offsets:
        payload += pack_be16(value)
    pointers.append(start + len(payload))
    payload += rule_stream
    payload[:24] = b"".join(pack_be32(pointer) for pointer in pointers)

    if len(payload) != baseline["scenario_length"]:
        raise PersonnelFlowError("scenario length changed; relocation outside the proven region is refused")
    if pointers != baseline["descriptor_pointers"]:
        raise PersonnelFlowError("descriptor layout changed; only fixed-shape record edits are accepted")
    return bytes(payload)


def serialize_candidate_bundle(bundle: dict[str, Any], canonical_base: bytes) -> bytes:
    if not isinstance(bundle, dict) or bundle.get("format") != CANDIDATE_BUNDLE_FORMAT:
        raise PersonnelFlowError(f"bundle format must be {CANDIDATE_BUNDLE_FORMAT}")
    source = bundle.get("canonical_source")
    if not isinstance(source, dict) or source.get("size") != CANONICAL_SIZE or source.get("sha256") != CANONICAL_SHA256:
        raise PersonnelFlowError("bundle canonical_source identity is missing or mismatched")
    block = bundle.get("candidate_block")
    if not isinstance(block, dict) or any((
        block.get("start") != CANDIDATE_BLOCK_START,
        block.get("end") != CANDIDATE_BLOCK_END,
        block.get("length") != CANDIDATE_BLOCK_END - CANDIDATE_BLOCK_START,
    )):
        raise PersonnelFlowError("bundle candidate_block bounds are missing or mismatched")
    supplied_scenarios = bundle.get("scenarios")
    if not isinstance(supplied_scenarios, list) or len(supplied_scenarios) != 3:
        raise PersonnelFlowError("bundle must contain exactly three scenarios")
    baseline = parse_candidate_scenarios(canonical_base)
    result = bytearray()
    for supplied, expected in zip(supplied_scenarios, baseline):
        result += _serialize_candidate_scenario(supplied, expected)
    expected_length = CANDIDATE_BLOCK_END - CANDIDATE_BLOCK_START
    if len(result) != expected_length:
        raise PersonnelFlowError(f"rebuilt candidate block is {len(result)} bytes, expected {expected_length}")
    return bytes(result)


def _resolve_nonexistent(path: Path) -> Path:
    try:
        return path.parent.resolve(strict=True) / path.name
    except FileNotFoundError as exc:
        raise PersonnelFlowError(f"output parent directory does not exist: {path.parent}") from exc


def _refuse_binary_collision(input_path: Path, output_path: Path) -> None:
    if output_path.suffix.lower() != ".bin":
        raise PersonnelFlowError("import output must use a .bin extension")
    input_resolved = input_path.resolve(strict=True)
    output_resolved = _resolve_nonexistent(output_path)
    if output_resolved == input_resolved:
        raise PersonnelFlowError("output must not be the canonical ROM input")
    if output_path.exists() or output_path.is_symlink():
        raise PersonnelFlowError(f"output already exists; refusing overwrite: {output_path}")


def load_bundle(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise PersonnelFlowError(f"bundle must be a regular JSON file: {path}")
    if path.suffix.lower() != ".json":
        raise PersonnelFlowError("bundle input must use a .json extension")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PersonnelFlowError(f"malformed bundle JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise PersonnelFlowError("bundle root must be a JSON object")
    return value


def extract_bundle(rom_path: Path, output_path: Path) -> dict[str, Any]:
    rom = canonical_rom(rom_path)
    if output_path.suffix.lower() != ".json":
        raise PersonnelFlowError("extract output must use a .json extension")
    if output_path.exists() or output_path.is_symlink():
        raise PersonnelFlowError(f"extract output already exists: {output_path}")
    output_resolved = _resolve_nonexistent(output_path)
    if output_resolved == rom_path.resolve(strict=True):
        raise PersonnelFlowError("extract output must not collide with canonical ROM input")
    bundle = candidate_bundle(rom)
    with output_path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(bundle, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return bundle


def import_bundle(base_rom_path: Path, bundle_path: Path, output_rom_path: Path) -> dict[str, Any]:
    rom = canonical_rom(base_rom_path)
    _refuse_binary_collision(base_rom_path, output_rom_path)
    bundle = load_bundle(bundle_path)
    candidate_bytes = serialize_candidate_bundle(bundle, rom)
    rebuilt = bytearray(rom)
    rebuilt[CANDIDATE_BLOCK_START:CANDIDATE_BLOCK_END] = candidate_bytes
    # Fixed-shape imports leave the external pointer table intact by design.
    with output_rom_path.open("xb") as handle:
        handle.write(rebuilt)
        handle.flush()
        os.fsync(handle.fileno())
    return {
        "output_size": len(rebuilt),
        "output_sha256": sha256_bytes(rebuilt),
        "candidate_block_sha256": sha256_bytes(candidate_bytes),
        "byte_identical_to_base": bytes(rebuilt) == rom,
    }


def _field(
    name: str, start: int, end: int, shape: str, evidence: str, role: str,
    semantic_evidence: str | None = None,
) -> dict[str, Any]:
    return {
        "id": f"personnel-flow:m68k_ram:{start:06x}:{name}",
        "name": name,
        "address_space": "m68k_ram",
        "start": start,
        "end": end,
        "start_hex": f"0x{start:06X}",
        "end_hex": f"0x{end:06X}",
        "shape": shape,
        "evidence": evidence,
        "semantic_evidence": semantic_evidence or evidence,
        "role": role,
    }


FIELDS: tuple[dict[str, Any], ...] = (
    _field("CommandByte", 0xFFF579, 0xFFF57A, "u8", "confirmed", "real UI command value 0x04..0x19"),
    _field("PersonnelSubcommandByte", 0xFFF57A, 0xFFF57B, "u8", "confirmed", "real UI observed 0x21 exploration and 0x46 selection"),
    _field("SelectionNestedDiscriminator", 0xFFF57D, 0xFFF57E, "u8", "confirmed", "0111AC tests 0x4A; broader meaning unknown", "unknown"),
    _field("PromptOrPhaseWord", 0xFFF38C, 0xFFF38E, "BE16", "confirmed", "exploration entry observed 0x0048; exact global semantics unknown", "unknown"),
    _field("SelectedCity", 0xFFF392, 0xFFF394, "BE16", "confirmed", "candidate builder city index; proven data indices 1..40"),
    _field("SelectedOfficer", 0xFFF3A6, 0xFFF3A8, "BE16", "confirmed", "acting officer and per-officer array index"),
    _field("OfficerActionByteBase", 0xFFCD00, 0xFFCE00, "u8[256]", "confirmed", "exploration writes selected entry to 1 before candidate construction"),
    _field("RngState", 0xFFF61C, 0xFFF620, "BE32 storage / BE16-at-base consumers", "confirmed", "unchanged through 01108C; changed by later 0083D4 call"),
    _field("OfficerGrowthWordBase", 0xFFC000, 0xFFC200, "BE16[256]", "confirmed", "10E12 adds 1..3 to selected officer after zero result"),
    _field("DifficultySelector", 0xFFEFD2, 0xFFEFD4, "BE16", "confirmed", "indexes three pairs at 010A4C; valid range inferred as 0..2", "probable"),
    _field("CandidateScenarioSelector", 0xFFEFE4, 0xFFEFE6, "BE16", "confirmed", "indexes three BE32 descriptors at 011080"),
    _field("CandidateBuffer", 0xFFEF24, 0xFFEF26, "first BE16 of variable list", "confirmed", "candidate IDs terminated by FFFF; dynamic extent not claimed"),
    _field("CurrentYearByte", 0xFFF374, 0xFFF375, "u8", "confirmed", "compared unsigned against low byte of candidate year words", "probable"),
    _field("OfficerLocationOrFlagBase", 0xFFCC00, 0xFFCD00, "u8[256]", "confirmed", "zero/action tests, reference lookup, and high-bit candidate scan"),
    _field("CityForceCodeBase", 0xFFF427, 0xFFF450, "u8[41 including index 0]", "confirmed", "maps officer city byte to selector force code"),
    _field("OfficerIntelligenceWordBase", 0xFFB600, 0xFFB800, "BE16[256]", "confirmed", "score and six-band result-table input", "probable"),
    _field("OfficerVirtueByteBase", 0xFFC200, 0xFFC300, "u8[256]", "confirmed", "byte contribution to exploration score", "probable"),
)


def _relationship(
    identifier: str,
    kind: str,
    evidence: str,
    semantic_evidence: str,
    source_space: str,
    source_start: int,
    source_end: int,
    target_space: str,
    target_start: int,
    target_end: int,
    transform: str,
    limitation: str,
) -> dict[str, Any]:
    return {
        "id": f"personnel-flow:{identifier}",
        "kind": kind,
        "evidence": evidence,
        "semantic_evidence": semantic_evidence,
        "source": {"address_space": source_space, "start": source_start, "end": source_end},
        "target": {"address_space": target_space, "start": target_start, "end": target_end},
        "transform": transform,
        "limitation": limitation,
        "source_address_space": source_space,
        "source_start": source_start,
        "source_end": source_end,
        "source_start_hex": f"0x{source_start:06X}",
        "source_end_hex": f"0x{source_end:06X}",
        "target_address_space": target_space,
        "target_start": target_start,
        "target_end": target_end,
        "target_start_hex": f"0x{target_start:06X}",
        "target_end_hex": f"0x{target_end:06X}",
    }


RELATIONSHIPS: tuple[dict[str, Any], ...] = (
    _relationship(
        "menu-command-to-ram", "runtime_ui_state_write", "confirmed", "confirmed",
        "m68k_rom", 0x0929F4, 0x092A16, "m68k_ram", 0xFFF579, 0xFFF57A,
        "real prompt-base menu confirmation stores the selected 0x04..0x19 command byte",
        "This edge establishes values, not every handler's user-facing semantic effect.",
    ),
    _relationship(
        "command-ram-to-dispatch", "static_indexed_dispatch", "confirmed", "confirmed",
        "m68k_ram", 0xFFF579, 0xFFF57A, "m68k_rom", 0x00DFB0, 0x00DFD8,
        "subtract 4, shift word left one, read signed BE16 at 00E024, JSR from base 00E0EE",
        "No local range check protects malformed command bytes.",
    ),
    _relationship(
        "dispatch-entry-16-to-handler", "static_dispatch_target", "confirmed", "confirmed",
        "m68k_rom", 0x00E048, 0x00E04A, "m68k_rom", 0x00FC82, 0x00FC98,
        "BE16 offset 1B94 added to base 00E0EE",
        "The handler then depends on FFF57A.",
    ),
    _relationship(
        "subcommand-21-to-exploration", "runtime_control_flow", "confirmed", "confirmed",
        "m68k_ram", 0xFFF57A, 0xFFF57B, "m68k_rom", 0x010A58, 0x010AA8,
        "00FC82 compares byte 0x21 and calls 010A58; the real UI edge was executed",
        "Only the captured zero-candidate result was naturally followed.",
    ),
    _relationship(
        "subcommand-non21-to-selection", "static_control_flow", "confirmed", "probable",
        "m68k_ram", 0xFFF57A, 0xFFF57B, "m68k_rom", 0x0111AC, 0x0111C0,
        "every byte other than 0x21 takes the BSR 0111AC fallback; real UI showed 0x46",
        "The 0x46 handler/core path was not naturally executed.",
    ),
    _relationship(
        "exploration-to-candidate-builder", "runtime_subroutine_call", "confirmed", "confirmed",
        "m68k_rom", 0x010A84, 0x010A92, "m68k_rom", 0x01108C, 0x0111A6,
        "selected city/officer are passed in D0.W/D1.W and the low-word return is tested",
        "Upper register words remain stale after MOVE.W and are not semantic return data.",
    ),
    _relationship(
        "candidate-selector-to-pointer-table", "static_indexed_pointer_read", "confirmed", "confirmed",
        "m68k_ram", 0xFFEFE4, 0xFFEFE6, "m68k_rom", 0x011080, 0x01108C,
        "FFEFE4.W is multiplied by four to select one of three BE32 descriptor pointers",
        "No local bounds check exists; safe tooling accepts only 0..2.",
    ),
    _relationship(
        "zero-candidate-to-zero-handler", "runtime_conditional_control_flow", "confirmed", "confirmed",
        "m68k_rom", 0x010A90, 0x010AA6, "m68k_rom", 0x010D14, 0x010D36,
        "zero low-word return branches at 010AA2 and calls 010D14",
        "RNG is unchanged at this branch but not through the complete handler.",
    ),
    _relationship(
        "zero-handler-to-growth", "runtime_subroutine_call", "confirmed", "confirmed",
        "m68k_rom", 0x010D14, 0x010D18, "m68k_rom", 0x010E12, 0x010E38,
        "010D14 calls growth helper; 0083D4 changes RNG and FFC000[officer] increases 1..3",
        "Captured officer CC increased 0028->002B after RNG CAAB8C7A->F5037F8A.",
    ),
    _relationship(
        "result-table-to-result-dispatch", "static_indexed_dispatch", "confirmed", "probable",
        "m68k_rom", 0x010B24, 0x010C74, "m68k_rom", 0x010D0C, 0x010D14,
        "7x6x4 word table yields raw byte offsets 0/2/4/6 into four handler-offset words",
        "Natural nonzero branches and human-facing meanings for codes 2/4/6 were not executed.",
    ),
)


EXPLORATION_RUNTIME = {
    "evidence": "confirmed",
    "run_scope": "natural_real_UI_prompt_base_scenario_0_zero_candidate_path",
    "key_path": ["C", "Right", "Right", "C", "Right", "Right", "C", "Down", "C", "C", "Left", "Left", "C", "C"],
    "entry": {
        "handler": "0x00FC82", "core": "0x010A58", "command": "0x16", "subcommand": "0x21",
        "selected_city": "0x0003", "selected_officer": "0x00CC", "prompt_or_phase": "0x0048",
        "action_before": "0x00", "rng": "0xCAAB8C7A",
    },
    "checkpoints": [
        {"pc": "0x010A84", "stage": "after_action_write", "cd00_cc": "0x01", "rng": "0xCAAB8C7A", "growth_c198": "0x0028"},
        {"pc": "0x010A92", "stage": "after_01108C_and_MOVE.W", "d0_low_word": "0x0000", "d7_low_word": "0x0000", "d7_upper_word_stale": "0x1900", "rng": "0xCAAB8C7A"},
        {"pc": "0x010AA2", "stage": "zero_branch_entry", "rng": "0xCAAB8C7A", "growth_c198": "0x0028"},
        {"pc": "0x010D14", "stage": "zero_result_handler_entry", "rng": "0xCAAB8C7A", "growth_c198": "0x0028"},
        {"pc": "0x010E12", "stage": "growth_helper_before_rng", "rng": "0xCAAB8C7A", "growth_c198": "0x0028"},
        {"pc": "0x010E18", "stage": "after_0083D4_rng_call", "rng": "0xF5037F8A", "growth_c198": "0x0028"},
        {"pc": "0x010E36", "stage": "after_growth_add", "rng": "0xF5037F8A", "growth_c198": "0x002B", "increment": 3},
        {"pc": "0x010D34", "stage": "zero_result_return", "rng": "0xF5037F8A", "growth_c198": "0x002B", "f612": "0x0206", "f362": "0x000D"},
    ],
    "boundary": (
        "RNG unchanged is confirmed only through 01108C return/010AA2 and 010E12 entry. "
        "That statement does not describe the complete zero-result command: the subsequent "
        "0083D4 call changes RNG and the selected growth word."
    ),
    "unexecuted": [
        {"path": "selection subcommand 0x46 handler/core", "evidence": "probable"},
        {"path": "nonzero exploration result and raw result handlers 0x02/0x04/0x06", "evidence": "probable"},
    ],
}


def command_runtime_observations() -> list[dict[str, Any]]:
    return [
        {
            "category": row["category"], "label": row["label"], "slug": row["slug"],
            "command": row["command"], "command_hex": f"0x{row['command']:02X}",
            "first_nonzero_FFF579": f"0x{row['command']:02X}",
            "status": "confirmed_real_UI_bounded_prompt_base_replay",
            "evidence": "confirmed",
        }
        for row in COMMAND_DEFINITIONS
    ]


def _optional_package_hash(name: str) -> str | None:
    path = Path(__file__).with_name(name)
    return sha256_file(path) if path.is_file() else None


def payload(rom: bytes) -> dict[str, Any]:
    failures = verify_anchors(rom)
    if failures:
        raise PersonnelFlowError("anchor verification failed: " + "; ".join(failures))
    candidates = candidate_bundle(rom)
    return {
        "schema": SCHEMA_VERSION,
        "canonical_source": {"size": len(rom), "sha256": sha256_bytes(rom)},
        "address_space": "linear BIN / Motorola 68000 ROM unless explicitly RAM",
        "anchors": list(ANCHORS),
        "command_catalog": command_catalog(rom),
        "menu_layout": menu_layout(rom),
        "dispatch_table": dispatch_rows(rom),
        "personnel_dispatch": {
            "command": "0x16", "handler": "0x00FC82", "subcommand_ram": "0xFFF57A",
            "exploration": {"observed_ui_value": "0x21", "target": "0x010A58", "evidence": "confirmed"},
            "selection": {"observed_ui_value": "0x46", "target": "0x0111AC", "evidence": "probable",
                          "boundary": "00FC82 checks only equality with 0x21; every other byte takes this path"},
        },
        "difficulty_table": [
            {"selector": index, "multiplier": pair[0], "addend": pair[1], "evidence": "confirmed"}
            for index, pair in enumerate(DIFFICULTY_PAIRS)
        ],
        "score_band_unsigned_maxima": list(SCORE_BAND_MAXIMA),
        "result_table": result_table(rom),
        "result_dispatch": [
            {"raw_code": code, "handler_target": target, "handler_target_hex": f"0x{target:06X}", "evidence": "confirmed"}
            for code, target in RESULT_HANDLER_TARGETS.items()
        ],
        "candidate_data_summary": {
            "format": candidates["format"], "candidate_block": candidates["candidate_block"],
            "scenarios": [
                {key: scenario[key] for key in (
                    "scenario_index", "scenario_year", "descriptor_rom_offset_hex", "scenario_end_hex",
                    "scenario_length", "scenario_sha256", "descriptor_pointers_hex", "statistics", "shared_alias"
                )}
                for scenario in candidates["scenarios"]
            ],
        },
        "fields": list(FIELDS),
        "relationships": list(RELATIONSHIPS),
        "dynamic_validation": {
            "catalog": command_runtime_observations(),
            "exploration": EXPLORATION_RUNTIME,
            "replay_script_hashes": {
                name: _optional_package_hash(name) for name in (
                    "trace_exploration_ui.lua", "debug_exploration_ui.cmd",
                    "run_exploration_ui.ps1", "trace_command_catalog.lua", "run_command_catalog.ps1"
                )
            },
        },
        "evidence_boundary": {
            "confirmed": "22 UI labels/positions to FFF579, dispatch bytes/targets, exploration 0x21 zero path through 10D34",
            "probable": "selection 0x46 beyond UI value and static dispatcher; nonzero exploration outcomes",
            "unknown": "human-facing meanings of raw candidate qualifiers/result codes beyond demonstrated access shape",
        },
    }


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _csv_text(rows: Sequence[dict[str, Any]], fieldnames: Sequence[str] | None = None) -> str:
    if fieldnames is None:
        fieldnames = list(rows[0]) if rows else []
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def _atomic_write_text(path: Path, text: str) -> None:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise PersonnelFlowError(f"refusing to replace symlink output: {path}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(normalized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


GENERATED_FILENAMES = (
    "personnel_flow.json", "command_catalog.csv", "dispatch_table.csv", "menu_layout.csv",
    "anchors.csv", "fields.csv", "relationships.csv", "difficulty_table.csv",
    "result_table.csv", "scenario_candidates.json", "scenario_force_year.csv",
    "scenario_city_rules.csv", "dynamic_validation.json", "symbols.inc",
)


def _paths_overlap(left: Path, right: Path) -> bool:
    """Return whether either resolved path contains the other."""

    return left == right or left in right.parents or right in left.parents


def _require_directory_parent(path: Path, *, label: str) -> None:
    """Reject a not-yet-created path whose nearest existing parent is not a directory."""

    parent = path.parent
    while True:
        if parent.exists() or parent.is_symlink():
            if not parent.is_dir():
                raise PersonnelFlowError(
                    f"{label} has a non-directory ancestor: {parent}"
                )
            return
        if parent == parent.parent:
            raise PersonnelFlowError(f"{label} has no existing directory ancestor")
        parent = parent.parent


def _validate_generation_paths(rom_path: Path, output_dir: Path, report_path: Path | None) -> None:
    rom_resolved = rom_path.resolve(strict=True)
    output_resolved = output_dir.resolve(strict=False)
    if output_dir.is_symlink() or (output_dir.exists() and not output_dir.is_dir()):
        raise PersonnelFlowError("generated output must be a real directory, not a file or symlink")
    _require_directory_parent(output_resolved, label="generated output")

    generated_targets: dict[Path, str] = {}
    for name in GENERATED_FILENAMES:
        target = output_dir / name
        target_resolved = target.resolve(strict=False)
        generated_targets[target_resolved] = name
        if target_resolved == rom_resolved:
            raise PersonnelFlowError("a generated artifact would overwrite the canonical ROM input")
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise PersonnelFlowError(
                f"generated artifact target must be a regular file path: {target}"
            )

    if _paths_overlap(output_resolved, rom_resolved):
        raise PersonnelFlowError("generated output tree collides with canonical ROM input")

    if report_path is None:
        return
    report_resolved = report_path.resolve(strict=False)
    if report_resolved == output_resolved:
        raise PersonnelFlowError("report output collides with the generated output directory")
    if report_resolved in generated_targets:
        raise PersonnelFlowError(
            f"report output collides with a generated artifact: {generated_targets[report_resolved]}"
        )
    if _paths_overlap(report_resolved, output_resolved):
        raise PersonnelFlowError("report output overlaps the generated output tree")
    if _paths_overlap(report_resolved, rom_resolved):
        raise PersonnelFlowError("report output tree collides with canonical ROM input")
    if report_path.is_symlink() or (report_path.exists() and report_path.is_dir()):
        raise PersonnelFlowError("report output must be a regular file path, not a directory or symlink")
    _require_directory_parent(report_resolved, label="report output")


def _flatten_result_rows(rom: bytes) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    table = result_table(rom)
    for score_index in range(7):
        for intel_index in range(6):
            for rng_class in range(4):
                raw = table[score_index][intel_index][rng_class]
                rows.append({
                    "score_band": score_index, "intelligence_band": intel_index, "rng_class": rng_class,
                    "raw_code": raw, "raw_code_hex": f"0x{raw:04X}",
                    "handler_target_hex": f"0x{result_handler_target(raw):06X}", "evidence": "confirmed",
                })
    return rows


def _candidate_csv_rows(candidates: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    force_rows: list[dict[str, Any]] = []
    city_rows: list[dict[str, Any]] = []
    for scenario in candidates["scenarios"]:
        for force_list in scenario["force_year_lists"]:
            for entry_index, entry in enumerate(force_list["entries"]):
                force_rows.append({
                    "scenario_index": scenario["scenario_index"], "scenario_year": scenario["scenario_year"],
                    "slot": force_list["slot"], "selector_force_code": force_list["selector_force_code"],
                    "entry_index": entry_index, **entry,
                })
        for city in scenario["city_rules"]:
            for entry_index, entry in enumerate(city["entries"]):
                city_rows.append({
                    "scenario_index": scenario["scenario_index"], "scenario_year": scenario["scenario_year"],
                    "city_id": city["city_id"], "relative_offset": city["relative_offset"],
                    "entry_index": entry_index, **entry,
                })
    return force_rows, city_rows


def symbols_text() -> str:
    rows = [
        "; Generated by tools/personnel_flow/personnel_flow.py. Linear ROM unless RAM.",
        "CommandDispatchTable                 = $00E024",
        "CommandDispatchTargetBase            = $00E0EE",
        "PersonnelCommandHandler              = $00FC82",
        "ExplorationCore                      = $010A58",
        "ExplorationDifficultyTable           = $010A4C",
        "ExplorationResultTable               = $010B24",
        "ExplorationResultDispatchTable       = $010D0C",
        "ExplorationZeroResult                = $010D14",
        "ExplorationGrowthHelper              = $010E12",
        "ExplorationScenarioPointerTable      = $011080",
        "ExplorationCandidateBuilder          = $01108C",
        "CommandByte                          = $FFF579",
        "PersonnelSubcommandByte              = $FFF57A",
        "SelectedCity                         = $FFF392",
        "SelectedOfficer                      = $FFF3A6",
        "OfficerActionByteBase                = $FFCD00",
        "RngState                             = $FFF61C",
        "OfficerGrowthWordBase                = $FFC000",
        "CandidateScenarioSelector            = $FFEFE4",
        "CandidateBuffer                      = $FFEF24",
    ]
    return "\n".join(rows) + "\n"


def report_text(data: dict[str, Any]) -> str:
    command_rows = data["command_catalog"]
    scenario_rows = data["candidate_data_summary"]["scenarios"]
    lines = [
        "# G-5510 personnel commands and exploration flow",
        "",
        f"Canonical BIN: `{data['canonical_source']['sha256']}` ({data['canonical_source']['size']} bytes).",
        "All addresses are linear BIN/68000 addresses unless marked RAM.",
        "",
        "## Outcome",
        "",
        "The 22 visible domestic/diplomacy/military menu items are closed through their real prompt-base UI values and the exact 44-byte indexed dispatch table. Command `0x16` reaches `0x00FC82`; real subcommand `0x21` reaches exploration core `0x010A58`. The captured scenario takes the zero-candidate path, consumes RNG later in `0x010E12`, and increments the selected officer's `FFC000` word by three.",
        "",
        "## Command catalog (menu order)",
        "",
        "| UI # | Category | Cell | Label | Command | Table # | Offset word | Handler | UI evidence | Handler evidence |",
        "|---:|---|---:|---|---:|---:|---:|---:|---|---|",
    ]
    for row in command_rows:
        lines.append(
            f"| {row['menu_order']} | {row['category_zh']} | {row['row']},{row['column']} | {row['label']} | "
            f"`{row['command_hex']}` | {row['table_order']} | `{row['dispatch_raw_offset_hex']}` | "
            f"`{row['handler_target_hex']}` | **confirmed** real UI | **confirmed** static |"
        )
    lines += [
        "",
        "The menu order is not the numeric table order: military row order contains `0x19 訓練` before centered `0x18 結束`; the dispatch table remains numeric `0x04..0x19`.",
        "",
        "## Dispatch mechanics",
        "",
        "Exact `0x04..0x19` table bytes at `0x00E024..0x00E050` (44 bytes): `00 00 00 46 03 0A 03 0C 03 52 04 8E 04 A4 06 A2 07 34 07 F8 0B 74 0C E6 0C E8 1A 0E 1B 02 1B 06 1B 28 1B 92 1B 94 1B AA 1C 02 1C 06`.",
        "",
        "`0x00DFC0` clears `D0.W`, loads `FFF579`, subtracts four, doubles the word, reads a BE16 at `0x00E024 + 2*(command-4)`, then performs `JSR (0x00E0EE,D0.W)`. There is no local range check. The 68000 indexed `.W` displacement is sign-extended; invalid command bytes can wrap during word subtraction/shift and read outside the 44-byte table.",
        "",
        "## Personnel dispatcher",
        "",
        "At `0x00FC82`, only `FFF57A == 0x21` is special and calls `0x010A58`. Every other byte branches to `0x0111AC`; `0x46` was observed on the real 選拔 UI, but that handler/core was not naturally executed here, so its semantic closure remains **probable**.",
        "",
        "## Exploration zero-path runtime closure",
        "",
        "Prompt-base keys: `C, Right, Right, C, Right, Right, C, Down, C, C, Left, Left, C, C`.",
        "",
        "| Checkpoint | Observed state |",
        "|---|---|",
        "| `00FC82 -> 010A58` | `FFF579=16`, `FFF57A=21`, `FFF38C=0048`, `FFF392=0003`, `FFF3A6=00CC`, `CD00[CC]=00`, RNG `CAAB8C7A` |",
        "| `010A84` | `CD00[CC] 00 -> 01`; RNG still `CAAB8C7A` |",
        "| `010A92 / 010AA2` | candidate return low word `0000`; zero branch; RNG still `CAAB8C7A` |",
        "| `010E12` entry | `FFC000[CC]=0028`; RNG still `CAAB8C7A` |",
        "| after `0083D4` | RNG becomes `F5037F8A` |",
        "| `010E36` | low-word formula gives `floor(3*0xF503/65536)+1 = 3`; `FFC000[CC]=002B` |",
        "| `010D34` | natural return reached with RNG `F5037F8A`, growth `002B` |",
        "",
        "The phrase “RNG unchanged” is limited to candidate construction and the zero-branch/growth-helper entry. It does not describe the complete zero-result command.",
        "",
        "## Static exploration core",
        "",
        "`0x010A58` has three special `FFF38C` branches (`006E -> 010EE0`, `0072 -> 010F1C`, `0073 -> 010F38`). The default path writes the action byte, calls `0x01108C`, and tests only the returned low word. `MOVE.W D0,D7` does not clear D7's upper word; the trace retained stale `0x1900` above a zero low word. Later candidate math masks the low word with `0x7FFF`.",
        "",
        "For a nonzero candidate count, `0x010AA8` forms a wrapping 16-bit score from the `FFC200` byte, `FFB600` word, an RNG product and the `0x010A4C` pair selected by `FFEFD2`. `0x010ADE` bins that unsigned word into seven bands. `0x010C74` chooses one candidate, bins its `FFB600` word into six bands, chooses one of four RNG classes, and reads the `7 x 6 x 4` table at `0x010B24`. Those natural nonzero branches were not run and remain **probable** semantically.",
        "",
        "The 168 result words contain only raw codes `0,2,4,6`. They index the four words at `0x010D0C` as byte offsets, reaching `010D14`, `010D64`, `010D64`, and `010DB4`. Human-facing meanings for codes `2/4/6` are not promoted beyond static structure.",
        "",
        "## Candidate descriptors and lossless format",
        "",
        "The pointer table `0x011080` selects one of three 24-byte/six-BE32 descriptors using `FFEFE4*4`. The first four pointers select force-code/year lists for raw codes `1,5,10,2`; the fifth points to 41 BE16 city offsets (dummy index 0 plus cities 1..40); the sixth points to variable city-rule streams.",
        "",
        "Each force/year record is two words and ends when the year word has bit 15. Each city record is three words `(year_threshold_raw, candidate_officer_id, qualifier_raw)` and each city list has its own negative year terminator. Qualifier access shape is: bit15 = unconditional; otherwise bit14 = literal force code in the low byte; otherwise the word is an officer reference whose CC00 city byte is mapped through F427. These names stay close to proven access behavior.",
        "",
        "Crucial overlap: the fourth force list's terminating word and city-offset entry 0 are the same physical word. The exporter exposes this alias and the importer emits it once, then verifies all descriptor pointers and per-city offsets.",
        "",
        "| Scenario | Descriptor..end | Force/year counts | City rules | Nonempty cities | Max/city | Qualifiers (unconditional/literal/reference) |",
        "|---:|---|---|---:|---:|---:|---|",
    ]
    for scenario in scenario_rows:
        stats = scenario["statistics"]
        q = stats["qualifier_counts"]
        lines.append(
            f"| {scenario['scenario_index']} ({scenario['scenario_year']}) | `{scenario['descriptor_rom_offset_hex']}..{scenario['scenario_end_hex']}` | "
            f"{stats['force_year_entry_counts']} | {stats['city_rule_count']} | {stats['nonempty_city_count']} | {stats['max_rules_per_city']} | "
            f"{q['unconditional_flagged']}/{q['literal_force_code']}/{q['reference_officer_id']} |"
        )
    lines += [
        "",
        "The three scenario blocks exactly cover `0x0AADE2..0x0AB8C4` (2786 bytes). Import accepts value edits only when every variable list retains its record count, recomputes and checks all offsets, refuses relocation, requires a canonical base, and creates a new `.bin` exclusively. An unchanged extract/import is byte-identical to the canonical ROM.",
        "",
        "## 68000 and malformed-state boundaries",
        "",
        "- `FFEFD2` and `FFEFE4` are used as word-scaled indices without local bounds checks; the safe model accepts only 0..2.",
        "- City ID 0 maps to the shared negative dummy word; proven usable city lists are IDs 1..40.",
        "- Score additions and shifts are word-sized where the instructions are `.W`; overflow wraps before unsigned band comparisons.",
        "- Candidate return count is the low 15 bits. Bit 15 marks the priority force/year path; upper register words can remain stale after `MOVE.W`.",
        "- Result-table callers establish score 0..6, intelligence 0..5 and RNG class 0..3. The raw table itself has no self-describing bounds metadata.",
        "- The importer rejects malformed JSON, booleans masquerading as integers, changed record counts, broken terminators/alias words, inconsistent offsets, input/output collisions, symlinks, and existing output files.",
        "",
        "## Generation safety",
        "",
        "Before writing any artifact, generation resolves and compares the canonical ROM, output directory, optional report, and all 14 named artifact paths. It rejects equality, ancestor/descendant tree overlap, a report at or below a planned artifact, and any planned artifact path already occupied by a directory or symlink.",
        "",
        "## Evidence boundary",
        "",
        "**Confirmed:** exact ROM anchors; 22 real UI labels/cells to `FFF579`; complete dispatch table; exploration `0x21` UI through zero-result return, RNG change and growth update; descriptor/table shapes and exact round trip.",
        "",
        "**Probable:** 選拔 `0x46` beyond its observed UI value and static fallback dispatcher; all natural nonzero exploration result meanings.",
        "",
        "**Unknown:** broader meanings of `FFF38C`, `FFF57D`, candidate qualifier payloads ignored by bit15, and user-facing semantics of raw result codes not naturally observed.",
        "",
    ]
    return "\n".join(lines)


def generate(rom_path: Path, output_dir: Path, report_path: Path | None = None) -> dict[str, str]:
    _validate_generation_paths(rom_path, output_dir, report_path)
    rom = canonical_rom(rom_path)
    data = payload(rom)
    candidates = candidate_bundle(rom)
    force_rows, city_rows = _candidate_csv_rows(candidates)
    catalog_rows = data["command_catalog"]
    dispatch = data["dispatch_table"]
    layout = data["menu_layout"]
    anchor_rows = [
        {**row, "start_hex": f"0x{row['start']:06X}", "end_hex": f"0x{row['end']:06X}", "length": row["end"] - row["start"]}
        for row in ANCHORS
    ]
    difficulty_rows = [
        {"selector": index, "rom_offset_hex": f"0x{0x010A4C + index * 4:06X}", "multiplier": pair[0], "addend": pair[1], "evidence": "confirmed"}
        for index, pair in enumerate(DIFFICULTY_PAIRS)
    ]
    artifacts = {
        "personnel_flow.json": _json_text(data),
        "command_catalog.csv": _csv_text(catalog_rows),
        "dispatch_table.csv": _csv_text(dispatch),
        "menu_layout.csv": _csv_text(layout),
        "anchors.csv": _csv_text(anchor_rows),
        "fields.csv": _csv_text(list(FIELDS)),
        "relationships.csv": _csv_text(list(RELATIONSHIPS)),
        "difficulty_table.csv": _csv_text(difficulty_rows),
        "result_table.csv": _csv_text(_flatten_result_rows(rom)),
        "scenario_candidates.json": _json_text(candidates),
        "scenario_force_year.csv": _csv_text(force_rows),
        "scenario_city_rules.csv": _csv_text(city_rows),
        "dynamic_validation.json": _json_text(data["dynamic_validation"]),
        "symbols.inc": symbols_text(),
    }
    for name, text in artifacts.items():
        _atomic_write_text(output_dir / name, text)
    if report_path is not None:
        _atomic_write_text(report_path, report_text(data))
    return {name: sha256_bytes(text.encode("utf-8")) for name, text in artifacts.items()}


def verify(rom_path: Path) -> dict[str, Any]:
    rom = canonical_rom(rom_path)
    failures = verify_anchors(rom)
    if failures:
        raise PersonnelFlowError("; ".join(failures))
    candidates = parse_candidate_scenarios(rom)
    return {
        "canonical_sha256": sha256_bytes(rom),
        "anchors": len(ANCHORS),
        "commands": len(command_catalog(rom)),
        "dispatch_bytes": DISPATCH_TABLE_END - DISPATCH_TABLE_START,
        "result_words": sum(len(cell) for band in result_table(rom) for cell in band),
        "candidate_scenarios": len(candidates),
        "candidate_bytes": CANDIDATE_BLOCK_END - CANDIDATE_BLOCK_START,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify_parser = subparsers.add_parser("verify", help="identity-gate and verify all static anchors")
    verify_parser.add_argument("--rom", type=Path, required=True)
    generate_parser = subparsers.add_parser("generate", help="generate deterministic analysis artifacts")
    generate_parser.add_argument("--rom", type=Path, required=True)
    generate_parser.add_argument("--output", type=Path, required=True)
    generate_parser.add_argument("--report", type=Path)
    extract_parser = subparsers.add_parser("extract", help="write a new structured candidate JSON bundle")
    extract_parser.add_argument("--rom", type=Path, required=True)
    extract_parser.add_argument("--output", type=Path, required=True)
    import_parser = subparsers.add_parser("import", help="import a candidate bundle to a new full-ROM copy")
    import_parser.add_argument("--rom", type=Path, required=True)
    import_parser.add_argument("--bundle", type=Path, required=True)
    import_parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "verify":
            print(json.dumps(verify(args.rom), sort_keys=True))
        elif args.command == "generate":
            print(json.dumps(generate(args.rom, args.output, args.report), sort_keys=True))
        elif args.command == "extract":
            bundle = extract_bundle(args.rom, args.output)
            print(json.dumps({"output": str(args.output), "scenarios": len(bundle["scenarios"])}, sort_keys=True))
        elif args.command == "import":
            print(json.dumps(import_bundle(args.rom, args.bundle, args.output), sort_keys=True))
        else:  # pragma: no cover
            raise AssertionError(args.command)
    except PersonnelFlowError as exc:
        print(f"ERROR: {exc}", file=os.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
