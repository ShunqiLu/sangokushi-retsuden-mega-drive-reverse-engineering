#!/usr/bin/env python3
"""Evidence-graded Z80/audio map for the verified Mega Drive ROM.

Code seeds come from reset, IM 1, reachable control flow and validated
dispatch tables.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from z80_decoder import DecodeError, Instruction, decode_instruction
from z80_payload import (
    RUNTIME_SIZE,
    TRANSFERS,
    build_manifest,
    components_from_runtime,
    compose_runtime,
    extract_components,
    rebuild_rom,
    sha256,
    write_extraction,
)


SCHEMA_VERSION = 1
CONFIDENCE_RANK = {"unknown": 0, "candidate": 1, "probable": 2, "confirmed": 3}


def hex4(value: int | None) -> str:
    return "" if value is None else f"{value:04X}"


def hex6(value: int | None) -> str:
    return "" if value is None else f"{value:06X}"


def stronger(left: str, right: str) -> str:
    return left if CONFIDENCE_RANK[left] >= CONFIDENCE_RANK[right] else right


def portable_project_path(path: Path) -> str:
    """Record the local basename as the input label."""
    return path.name


@dataclass
class Seed:
    address: int
    confidence: str
    evidence_type: str
    detail: str
    source_address: int | None = None
    function_entry: bool = False

    def evidence(self) -> dict[str, Any]:
        return {
            "type": self.evidence_type,
            "confidence": self.confidence,
            "detail": self.detail,
            "source_address": self.source_address,
        }


@dataclass
class DispatchTable:
    name: str
    start: int
    end: int
    dispatcher: int
    confidence: str
    purpose: str
    entries: list[dict[str, Any]] = field(default_factory=list)
    caveats: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "address_space": "z80_ram",
            "start": self.start,
            "end_exclusive": self.end,
            "length": self.end - self.start,
            "dispatcher": self.dispatcher,
            "confidence": self.confidence,
            "purpose": self.purpose,
            "entries": self.entries,
            "caveats": self.caveats,
        }


class ConservativeCFG:
    """Recursive traversal with byte ownership and explicit conflict records."""

    def __init__(
        self,
        image: bytes,
        seeds: Iterable[Seed],
        reserved_ranges: Iterable[tuple[int, int, str]] = (),
    ) -> None:
        self.image = image
        self.instructions: dict[int, Instruction] = {}
        self.confidence: dict[int, str] = {}
        self.evidence: dict[int, list[dict[str, Any]]] = defaultdict(list)
        self.edges: list[dict[str, Any]] = []
        self._edge_keys: set[tuple[Any, ...]] = set()
        self.functions: dict[int, dict[str, Any]] = {}
        self.conflicts: list[dict[str, Any]] = []
        self.decode_failures: list[dict[str, Any]] = []
        self.unresolved: list[dict[str, Any]] = []
        self.owner: list[int | None] = [None] * len(image)
        self.reserved: list[str | None] = [None] * len(image)
        for start, end, label in reserved_ranges:
            for address in range(max(0, start), min(len(image), end)):
                self.reserved[address] = label
        self.initial_seeds = list(seeds)
        self._queue: deque[Seed] = deque()

    def add_function(
        self,
        address: int,
        confidence: str,
        entry_type: str,
        detail: str,
        source: int | None,
    ) -> None:
        row = self.functions.setdefault(
            address,
            {
                "address": address,
                "confidence": confidence,
                "entry_types": [],
                "evidence": [],
            },
        )
        row["confidence"] = stronger(row["confidence"], confidence)
        if entry_type not in row["entry_types"]:
            row["entry_types"].append(entry_type)
        evidence = {
            "type": entry_type,
            "confidence": confidence,
            "detail": detail,
            "source_address": source,
        }
        if evidence not in row["evidence"]:
            row["evidence"].append(evidence)

    def enqueue(self, seed: Seed) -> None:
        self._queue.append(seed)
        if seed.function_entry:
            self.add_function(
                seed.address,
                seed.confidence,
                seed.evidence_type,
                seed.detail,
                seed.source_address,
            )

    def add_edge(
        self,
        source: int,
        target: int | None,
        edge_type: str,
        confidence: str,
        status: str,
    ) -> None:
        key = (source, target, edge_type, confidence, status)
        if key in self._edge_keys:
            return
        self._edge_keys.add(key)
        self.edges.append(
            {
                "source": source,
                "target": target,
                "type": edge_type,
                "confidence": confidence,
                "status": status,
            }
        )

    def _target_seed(
        self,
        instruction: Instruction,
        target: int,
        confidence: str,
        kind: str,
        function_entry: bool,
    ) -> None:
        if not 0 <= target < len(self.image):
            self.add_edge(
                instruction.address, target, kind, confidence, "outside_loaded_image"
            )
            self.unresolved.append(
                {
                    "source": instruction.address,
                    "type": "direct_target_outside_loaded_image",
                    "target": target,
                    "confidence": confidence,
                    "detail": instruction.text,
                }
            )
            return
        self.add_edge(instruction.address, target, kind, confidence, "resolved")
        self.enqueue(
            Seed(
                target,
                confidence,
                f"direct_{kind}",
                instruction.text,
                instruction.address,
                function_entry,
            )
        )

    def _fallthrough(self, instruction: Instruction, confidence: str) -> None:
        target = instruction.address + instruction.size
        if target >= len(self.image):
            self.add_edge(
                instruction.address, target, "fallthrough", confidence, "outside_loaded_image"
            )
            return
        self.add_edge(instruction.address, target, "fallthrough", confidence, "resolved")
        self.enqueue(
            Seed(
                target,
                confidence,
                "linear_fallthrough",
                instruction.text,
                instruction.address,
            )
        )

    def _propagate(self, instruction: Instruction, confidence: str) -> None:
        flow = instruction.flow_type
        if flow in {"call", "conditional_call", "rst"}:
            assert instruction.target is not None
            kind = "rst" if flow == "rst" else "call"
            self._target_seed(
                instruction,
                instruction.target,
                confidence,
                kind,
                function_entry=True,
            )
            self._fallthrough(instruction, confidence)
        elif flow in {
            "conditional_jump",
            "conditional_relative",
            "djnz",
        }:
            assert instruction.target is not None
            self._target_seed(
                instruction,
                instruction.target,
                confidence,
                "branch_taken",
                function_entry=False,
            )
            self._fallthrough(instruction, confidence)
        elif flow in {"jump", "relative_jump"}:
            assert instruction.target is not None
            self._target_seed(
                instruction,
                instruction.target,
                confidence,
                "jump",
                function_entry=False,
            )
        elif flow == "conditional_return":
            self.unresolved.append(
                {
                    "source": instruction.address,
                    "type": "conditional_return",
                    "target": None,
                    "confidence": confidence,
                    "detail": instruction.text,
                }
            )
            self._fallthrough(instruction, confidence)
        elif flow in {"return", "interrupt_return"}:
            self.unresolved.append(
                {
                    "source": instruction.address,
                    "type": flow,
                    "target": None,
                    "confidence": confidence,
                    "detail": instruction.text,
                }
            )
        elif flow == "indirect_jump":
            self.add_edge(
                instruction.address, None, "indirect_jump", confidence, "unresolved"
            )
            self.unresolved.append(
                {
                    "source": instruction.address,
                    "type": "indirect_jump",
                    "target": None,
                    "confidence": confidence,
                    "detail": instruction.text,
                }
            )
        elif flow == "halt":
            self.unresolved.append(
                {
                    "source": instruction.address,
                    "type": "halt_resume_requires_interrupt_model",
                    "target": instruction.address + instruction.size,
                    "confidence": confidence,
                    "detail": instruction.text,
                }
            )
        else:
            self._fallthrough(instruction, confidence)

    def analyse(self) -> "ConservativeCFG":
        for seed in self.initial_seeds:
            self.enqueue(seed)
        while self._queue:
            seed = self._queue.popleft()
            address = seed.address
            if not 0 <= address < len(self.image):
                continue
            if self.reserved[address] is not None:
                self.conflicts.append(
                    {
                        "type": "target_hits_reserved_data",
                        "target": address,
                        "owner": self.reserved[address],
                        "source": seed.source_address,
                        "confidence": seed.confidence,
                    }
                )
                continue
            if address in self.instructions:
                old = self.confidence[address]
                self.evidence[address].append(seed.evidence())
                if CONFIDENCE_RANK[seed.confidence] > CONFIDENCE_RANK[old]:
                    self.confidence[address] = seed.confidence
                    self._propagate(self.instructions[address], seed.confidence)
                continue
            existing = self.owner[address]
            if existing is not None and existing != address:
                self.conflicts.append(
                    {
                        "type": "target_inside_instruction",
                        "target": address,
                        "owner": existing,
                        "source": seed.source_address,
                        "confidence": seed.confidence,
                    }
                )
                continue
            try:
                instruction = decode_instruction(self.image, address)
            except DecodeError as error:
                self.decode_failures.append(
                    {
                        "address": address,
                        "source": seed.source_address,
                        "confidence": seed.confidence,
                        "error": str(error),
                    }
                )
                continue
            overlap = None
            reserved = None
            for byte_address in range(address, address + instruction.size):
                if byte_address >= len(self.owner):
                    overlap = byte_address
                    break
                if self.owner[byte_address] is not None:
                    overlap = byte_address
                    break
                if self.reserved[byte_address] is not None:
                    reserved = (byte_address, self.reserved[byte_address])
                    break
            if overlap is not None or reserved is not None:
                self.conflicts.append(
                    {
                        "type": "instruction_overlaps_code"
                        if overlap is not None
                        else "instruction_overlaps_reserved_data",
                        "target": address,
                        "overlap_at": overlap if overlap is not None else reserved[0],
                        "owner": self.owner[overlap]
                        if overlap is not None and overlap < len(self.owner)
                        else reserved[1],
                        "source": seed.source_address,
                        "confidence": seed.confidence,
                    }
                )
                continue
            self.instructions[address] = instruction
            self.confidence[address] = seed.confidence
            self.evidence[address].append(seed.evidence())
            for byte_address in range(address, address + instruction.size):
                self.owner[byte_address] = address
            self._propagate(instruction, seed.confidence)
        self.edges.sort(
            key=lambda row: (
                row["source"],
                -1 if row["target"] is None else row["target"],
                row["type"],
            )
        )
        return self

    def code_byte_sets(self) -> dict[str, set[int]]:
        result: dict[str, set[int]] = defaultdict(set)
        for address, instruction in self.instructions.items():
            confidence = self.confidence[address]
            result[confidence].update(range(address, address + instruction.size))
        return result


ARCHITECTURAL_SEEDS = (
    Seed(
        0x0000,
        "confirmed",
        "z80_reset_vector",
        "architectural reset entry; loaded byte stream begins DI, DI, IM 1",
        function_entry=True,
    ),
    Seed(
        0x0038,
        "confirmed",
        "z80_im1_vector",
        "reset path executes IM 1 at Z80 0x0002",
        source_address=0x0002,
        function_entry=True,
    ),
)


KNOWN_SYMBOLS: dict[int, tuple[str, str, str]] = {
    0x0000: ("z80_reset", "confirmed", "architectural reset vector"),
    0x0008: ("ym2612_wait_ready", "probable", "polls YM2612 port 0 status bit 7"),
    0x0010: ("ym2612_write_channel_routine", "probable", "RST 10 channel-aware YM write path"),
    0x0018: ("ym2612_write_port0_routine", "probable", "RST 18 jumps to the port-0 write body"),
    0x0020: ("bank_root_lookup", "probable", "loads root pointer from 1C02 then dereferences it"),
    0x0028: ("word_pointer_index", "probable", "indexes a little-endian pointer table by A*2"),
    0x0030: ("read_le16_from_hl", "probable", "reads a little-endian word through HL"),
    0x0038: ("im1_interrupt", "confirmed", "IM 1 vector selected by reset code"),
    0x0053: ("driver_main", "confirmed", "direct reset jump target"),
    0x04AC: ("ym2612_port0_write", "confirmed", "reachable absolute writes to 4000/4001"),
    0x04BF: ("ym2612_port1_write", "confirmed", "reachable absolute writes to 4002/4003"),
    0x050A: ("sound_command_dispatch", "probable", "range partitions command byte and dispatches"),
    0x070C: ("z80_bank_register_init", "confirmed", "reachable writes to memory-mapped 6000"),
    0x07E7: ("driver_state_clear", "confirmed", "overlapping LDIR zero-fill of runtime state"),
    0x087F: ("mailbox_poll", "confirmed", "reads Z80 RAM 1C0A/1C0B/1C0C"),
    0x0B78: ("sequence_command_dispatch", "confirmed", "E0-FF sequence command dispatcher"),
}


def _word(image: bytes, address: int) -> int:
    return image[address] | (image[address + 1] << 8)


def discover_dispatch_tables(strict: ConservativeCFG, image: bytes) -> list[DispatchTable]:
    """Recognise only three driver-specific, shape-validated pointer tables."""
    tables: list[DispatchTable] = []

    # The sequence parser at 01E4 sends bytes >= E0 to 0B78.  0B78 subtracts
    # E0, indexes by two through RST 28, and JP (HL), proving 32 entries.
    signature = bytes.fromhex("21840be5d6e0218f0bef1ae9")
    if 0x0B78 in strict.instructions and image[0x0B78 : 0x0B78 + len(signature)] == signature:
        entries = []
        valid = True
        for index in range(32):
            entry_address = 0x0B8F + index * 2
            target = _word(image, entry_address)
            target_valid = 0 <= target < 0x0FCA and not 0x0B8F <= target < 0x0BCF
            valid &= target_valid
            entries.append(
                {
                    "index": index,
                    "command": 0xE0 + index,
                    "entry_address": entry_address,
                    "target": target,
                    "target_valid": target_valid,
                    "confidence": "confirmed" if target_valid else "unknown",
                }
            )
        tables.append(
            DispatchTable(
                "sequence_command_e0_ff",
                0x0B8F,
                0x0BCF,
                0x0B83,
                "confirmed" if valid else "probable",
                "music/SFX sequence command handlers for byte values E0-FF",
                entries,
                [] if valid else ["one or more target words leave the driver extent"],
            )
        )

    # Handler FF reaches a second byte-indexed table.  The code has no visible
    # bound check; accept only the consecutive in-driver pointer prefix and do
    # stop the table at the first out-of-range word.
    nested_signature = bytes.fromhex("21cf0bef131ae9")
    if 0x0B88 in strict.instructions and image[0x0B88 : 0x0B88 + len(nested_signature)] == nested_signature:
        entries = []
        cursor = 0x0BCF
        while cursor + 1 < len(image) and len(entries) < 32:
            target = _word(image, cursor)
            if not (0x0038 <= target < 0x0FCA) or 0x0BCF <= target < cursor + 2:
                break
            entries.append(
                {
                    "index": len(entries),
                    "entry_address": cursor,
                    "target": target,
                    "target_valid": True,
                    "confidence": "probable",
                }
            )
            cursor += 2
        if entries:
            tables.append(
                DispatchTable(
                    "sequence_ff_subcommand_prefix",
                    0x0BCF,
                    cursor,
                    0x0B8E,
                    "probable",
                    "valid consecutive prefix of the FF nested command table",
                    entries,
                    [
                        "no bound check for the subcommand byte has been proven",
                        "the first target outside the driver marks the table boundary",
                    ],
                )
            )

    # External sound-control bytes E0-F8 pass through 052D.  Only the first
    # four consecutive words are valid driver targets; higher values remain
    # deliberately unresolved rather than decoding following code as a table.
    control_signature = bytes.fromhex("d6e0212d05efe9")
    if 0x0526 in strict.instructions and image[0x0526 : 0x0526 + len(control_signature)] == control_signature:
        entries = []
        cursor = 0x052D
        while cursor + 1 < len(image) and len(entries) < 25:
            target = _word(image, cursor)
            if not (0x0038 <= target < 0x0FCA) or 0x052D <= target < cursor + 2:
                break
            entries.append(
                {
                    "index": len(entries),
                    "command": 0xE0 + len(entries),
                    "entry_address": cursor,
                    "target": target,
                    "target_valid": True,
                    "confidence": "probable",
                }
            )
            cursor += 2
        if entries:
            tables.append(
                DispatchTable(
                    "external_control_command_valid_prefix",
                    0x052D,
                    cursor,
                    0x052C,
                    "probable",
                    "valid target prefix for external control commands beginning at E0",
                    entries,
                    [
                        "the range check permits E0-F8 but entries after this prefix decode to invalid targets",
                        "handler entries cover supported command values",
                    ],
                )
            )
    return tables


def analyse_cfg(image: bytes) -> tuple[ConservativeCFG, ConservativeCFG, list[DispatchTable]]:
    strict = ConservativeCFG(image, ARCHITECTURAL_SEEDS).analyse()
    tables = discover_dispatch_tables(strict, image)
    final = strict
    # The E0-FF table makes handler 0B88 reachable; that handler exposes the
    # nested FF table. Repeat reachable traversal until the table set stabilizes.
    for _ in range(3):
        reserved = [(table.start, table.end, table.name) for table in tables]
        seeds = list(ARCHITECTURAL_SEEDS)
        for table in tables:
            for entry in table.entries:
                if not entry["target_valid"]:
                    continue
                seeds.append(
                    Seed(
                        entry["target"],
                        table.confidence,
                        "dispatch_table_target",
                        f"{table.name}[{entry['index']}]",
                        entry["entry_address"],
                        function_entry=True,
                    )
                )
        final = ConservativeCFG(image, seeds, reserved).analyse()
        discovered = discover_dispatch_tables(final, image)
        by_name = {table.name: table for table in tables}
        for table in discovered:
            by_name.setdefault(table.name, table)
        updated = list(by_name.values())
        if len(updated) == len(tables):
            break
        tables = updated
    return strict, final, tables


def simulate_bank_configuration(overlay: bytes) -> dict[str, Any]:
    if len(overlay) < 4:
        raise ValueError("overlay is too small for bank configuration")
    # 070C writes RLCA(1C01) once, then the successive low bits of 1C00.
    first = ((overlay[1] << 1) | (overlay[1] >> 7)) & 0xFF
    value = overlay[0]
    writes = [first & 1]
    for _ in range(8):
        writes.append(value & 1)
        value = ((value >> 1) | ((value & 1) << 7)) & 0xFF
    bank_register = sum(bit << index for index, bit in enumerate(writes))
    return {
        "serial_bits_lsb_first": writes,
        "bank_register_9bit": bank_register,
        "m68k_base": bank_register << 15,
        "z80_window_start": 0x8000,
        "z80_window_end_exclusive": 0x10000,
        "confidence": "confirmed",
        "evidence": "reachable 070C routine plus overlay bytes at Z80 1C00/1C01",
    }


def banked_to_rom(z80_address: int, bank: dict[str, Any]) -> int:
    if not 0x8000 <= z80_address <= 0xFFFF:
        raise ValueError(f"not a banked Z80 address: 0x{z80_address:04X}")
    return bank["m68k_base"] + z80_address - 0x8000


def _bank_word(rom: bytes, z80_address: int, bank: dict[str, Any]) -> int:
    offset = banked_to_rom(z80_address, bank)
    if offset + 2 > len(rom):
        raise ValueError("banked word leaves ROM")
    return rom[offset] | (rom[offset + 1] << 8)


def _pointer_table(
    rom: bytes,
    bank: dict[str, Any],
    name: str,
    start: int,
    count: int,
    purpose: str,
    confidence: str,
) -> dict[str, Any]:
    entries = []
    for index in range(count):
        entry = start + index * 2
        target = _bank_word(rom, entry, bank)
        entries.append(
            {
                "index": index,
                "entry_z80_address": entry,
                "entry_rom_offset": banked_to_rom(entry, bank),
                "target_z80_address": target,
                "target_rom_offset": banked_to_rom(target, bank)
                if 0x8000 <= target <= 0xFFFF
                else None,
            }
        )
    return {
        "name": name,
        "address_space": "z80_banked_window",
        "start": start,
        "end_exclusive": start + count * 2,
        "rom_start": banked_to_rom(start, bank),
        "rom_end_exclusive": banked_to_rom(start + count * 2 - 1, bank) + 1,
        "entry_count": count,
        "purpose": purpose,
        "confidence": confidence,
        "entries": entries,
    }


def build_banked_audio_map(
    rom: bytes, image: bytes, cfg: ConservativeCFG, bank: dict[str, Any]
) -> dict[str, Any]:
    used_slots: dict[int, list[int]] = defaultdict(list)
    # These are the reachable RST 20 sites and the C definitions on their
    # incoming paths.  060A is deliberately shared by the C=02 and C=06 arms.
    root_lookups = {
        0x0315: (0x0A,),
        0x03BB: (0x08,),
        0x0560: (0x04,),
        0x060A: (0x02, 0x06),
        0x089E: (0x00,),
        0x0F4E: (0x0A,),
    }
    for address, slots in root_lookups.items():
        instruction = cfg.instructions.get(address)
        if not instruction or instruction.flow_type != "rst" or instruction.target != 0x20:
            continue
        for slot in slots:
            used_slots[slot].append(address)

    root_entries = []
    for slot in range(0, 0x0E, 2):
        pointer = _bank_word(rom, 0x8000 + slot, bank)
        root_entries.append(
            {
                "slot": slot,
                "entry_z80_address": 0x8000 + slot,
                "entry_rom_offset": banked_to_rom(0x8000 + slot, bank),
                "pointer": pointer,
                "pointer_rom_offset": banked_to_rom(pointer, bank)
                if pointer >= 0x8000
                else None,
                "reachable_lookup_sites": sorted(used_slots.get(slot, [])),
                "status": "confirmed" if slot in used_slots else "candidate",
            }
        )

    tables = [
        _pointer_table(
            rom,
            bank,
            "pitch_modulation_envelope_pointer_table",
            0x800E,
            10,
            "root slot 0x08 at 03B9-03BC selects pitch envelopes consumed at 03C2-040A; first target 0x8022 follows ten words, global selector bound remains open",
            "probable",
        ),
        _pointer_table(
            rom,
            bank,
            "attenuation_envelope_pointer_table",
            0x815D,
            11,
            "root slot 0x0A at 0313-0317/0F4C-0F50 selects attenuation envelopes consumed at 0F7B-0FAB; global selector bound remains open",
            "probable",
        ),
        _pointer_table(
            rom,
            bank,
            "music_definition_pointer_table",
            0x823F,
            31,
            "commands 0x81-0x9F index 31 banked music definitions",
            "confirmed",
        ),
    ]

    local_entries = []
    for index in range(16):
        entry = 0x1000 + index * 2
        target = _word(image, entry)
        local_entries.append(
            {
                "index": index,
                "command": 0xA0 + index,
                "entry_z80_address": entry,
                "target_z80_address": target,
                "target_valid": 0x1020 <= target < 0x16EE,
            }
        )
    local_table = {
        "name": "local_sfx_a0_af_pointer_table",
        "address_space": "z80_ram",
        "start": 0x1000,
        "end_exclusive": 0x1020,
        "entry_count": 16,
        "purpose": "local SFX structures for external command values A0-AF",
        "confidence": "confirmed"
        if all(row["target_valid"] for row in local_entries)
        else "probable",
        "entries": local_entries,
    }

    regions = [
        {
            "name": "bank_root_table",
            "z80_start": 0x8000,
            "z80_end_exclusive": 0x800E,
            "rom_start": banked_to_rom(0x8000, bank),
            "rom_end_exclusive": banked_to_rom(0x800D, bank) + 1,
            "category": "command_root_table",
            "confidence": "confirmed",
        },
        {
            "name": "pitch_modulation_envelope_candidates",
            "z80_start": 0x8022,
            "z80_end_exclusive": 0x815D,
            "rom_start": banked_to_rom(0x8022, bank),
            "rom_end_exclusive": banked_to_rom(0x815C, bank) + 1,
            "category": "pitch_modulation_envelope_data",
            "confidence": "probable",
        },
        {
            "name": "attenuation_envelope_candidates",
            "z80_start": 0x8173,
            "z80_end_exclusive": 0x8200,
            "rom_start": banked_to_rom(0x8173, bank),
            "rom_end_exclusive": banked_to_rom(0x81FF, bank) + 1,
            "category": "attenuation_envelope_data",
            "confidence": "probable",
        },
        {
            "name": "sound_priority_bytes",
            "z80_start": 0x8200,
            "z80_end_exclusive": 0x823F,
            "rom_start": banked_to_rom(0x8200, bank),
            "rom_end_exclusive": banked_to_rom(0x823E, bank) + 1,
            "category": "command_priority_table",
            "confidence": "confirmed",
        },
        {
            "name": "banked_music_definitions_and_sequences",
            "z80_start": 0x827D,
            "z80_end_exclusive": 0x10000,
            "rom_start": banked_to_rom(0x827D, bank),
            "rom_end_exclusive": min(len(rom), banked_to_rom(0xFFFF, bank) + 1),
            "category": "music_sequence_or_definition_data",
            "confidence": "probable",
        },
    ]
    return {
        "configuration": bank,
        "root_entries": root_entries,
        "pointer_tables": tables,
        "local_pointer_table": local_table,
        "regions": regions,
        "caveats": [
            "root slot 0x08 contains pitch modulation; FM records use header bases and the 25-byte stride at 0484-049D",
            "envelope extents are candidates; F0 80 at 81FE sets a cursor beyond the last attenuation allocation",
            "banked music range may contain alignment/padding and shared parameter blocks",
        ],
    }


def memory_reference_rows(cfg: ConservativeCFG) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for address in sorted(cfg.instructions):
        instruction = cfg.instructions[address]
        confidence = cfg.confidence[address]
        for reference in instruction.memory_refs:
            target = reference["address"]
            if 0x0000 <= target <= 0x1FFF:
                region = "z80_ram"
            elif 0x4000 <= target <= 0x4003:
                region = "ym2612"
            elif target == 0x6000:
                region = "z80_bank_register"
            elif target == 0x7F11:
                region = "psg"
            elif 0x8000 <= target <= 0xFFFF:
                region = "m68k_banked_window"
            else:
                region = "unmapped_or_unknown"
            rows.append(
                {
                    "instruction": address,
                    "instruction_text": instruction.text,
                    "target": target,
                    "direction": reference["direction"],
                    "width": reference["width"],
                    "addressing": reference["addressing"],
                    "region": region,
                    "confidence": confidence,
                }
            )
        immediate = instruction.details.get("immediate16")
        if (
            immediate is not None
            and instruction.details.get("immediate_kind") == "pointer_or_value"
            and (0x1C00 <= immediate <= 0x1FFF or 0x8000 <= immediate <= 0xFFFF)
        ):
            rows.append(
                {
                    "instruction": address,
                    "instruction_text": instruction.text,
                    "target": immediate,
                    "direction": "address_constant",
                    "width": 2,
                    "addressing": "immediate16",
                    "region": "z80_runtime_state"
                    if immediate < 0x2000
                    else "m68k_banked_window",
                    "confidence": confidence,
                }
            )
    return rows


def hardware_access_rows(memory_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    names = {
        0x4000: "YM2612 status/address port 0",
        0x4001: "YM2612 data port 0",
        0x4002: "YM2612 address port 1",
        0x4003: "YM2612 data port 1",
        0x6000: "Mega Drive Z80 bank register",
        0x7F11: "SN76489/PSG write port",
    }
    result = []
    for row in memory_rows:
        if row["target"] not in names:
            continue
        copy = dict(row)
        copy["hardware"] = names[row["target"]]
        result.append(copy)
    return result


def runtime_state_fields(image: bytes) -> list[dict[str, Any]]:
    definitions = [
        (0x1C00, 1, "bank_serial_low_8_bits", "confirmed", "consumed by 070C"),
        (0x1C01, 1, "bank_serial_ninth_bit_source", "confirmed", "RLCA then first 6000 write"),
        (0x1C02, 2, "banked_root_pointer", "confirmed", "loaded by RST 20 helper; value 8000"),
        (0x1C04, 2, "ym_timer_a_reload", "probable", "split into YM registers 24/25"),
        (0x1C06, 1, "ym_timer_b_reload", "probable", "written to YM register 26"),
        (0x1C07, 1, "driver_active_or_mode", "probable", "IRQ/main-loop tests and command handlers write it"),
        (0x1C09, 1, "selected_current_command", "probable", "mailbox arbitration copies selected byte here"),
        (0x1C0A, 1, "m68k_mailbox_primary", "confirmed", "68000 0080BA write; Z80 087F poll"),
        (0x1C0B, 1, "m68k_mailbox_secondary", "confirmed", "68000 0080B2 write; Z80 087F poll"),
        (0x1C0C, 1, "z80_internal_third_command_slot", "probable", "Z80 poll includes it; no 68000 direct writer found"),
        (0x1C40, 0x1E0, "fm_channel_state_structs", "probable", "IX base 1C40 and stride 30h"),
        (0x1D90, 0x90, "additional_channel_state", "probable", "explicit DE destination and structured copies"),
        (0x1E20, 0x60, "psg_channel_state_group", "probable", "IX base 1E20 and two 30h records"),
        (0x1E80, 0x120, "secondary_channel_state_group", "probable", "IX base 1E80 and six 30h records"),
        (0x1FFD, 2, "stack_top", "confirmed", "LD SP,1FFD at reset"),
        (0x1FFF, 1, "irq_countdown", "confirmed", "reset initializes to 3; IM1 handler decrements"),
    ]
    rows = []
    for start, length, name, confidence, evidence in definitions:
        available_end = min(len(image), start + length)
        rows.append(
            {
                "start": start,
                "end_exclusive": start + length,
                "length": length,
                "name": name,
                "initial_bytes": image[start:available_end].hex(),
                "present_in_1e00_image": start < len(image),
                "confidence": confidence,
                "evidence": evidence,
            }
        )
    return rows


def _compress_primary_regions(
    image: bytes, cfg: ConservativeCFG, tables: list[DispatchTable]
) -> list[dict[str, Any]]:
    labels: list[tuple[str, str, str]] = [
        ("unknown", "unknown", "not classified") for _ in image
    ]

    def paint(start: int, end: int, category: str, confidence: str, evidence: str) -> None:
        for address in range(max(0, start), min(len(labels), end)):
            labels[address] = (category, confidence, evidence)

    paint(
        0x0000,
        0x0FCA,
        "driver_inline_data_candidate",
        "candidate",
        "driver bytes outside the visible instruction graph",
    )
    paint(
        0x0FCA,
        0x1000,
        "duplicated_local_audio_prefix",
        "confirmed",
        "exactly equals Z80 1000-1035 because ROM source ranges overlap by 36h bytes",
    )
    paint(
        0x1000,
        0x16EE,
        "local_sfx_sequence_and_parameter_data",
        "probable",
        "A0-AF pointer table targets this range; highest target is below 16EE",
    )
    paint(
        0x16EE,
        0x1C00,
        "foreign_m68k_source_copy",
        "confirmed",
        "maps to ROM 00808A-00859B, beginning at confirmed 68000 mailbox code",
    )
    paint(
        0x1C00,
        0x1C09,
        "runtime_configuration_state",
        "confirmed",
        "13-byte overlay initializes bank/timer/mode fields",
    )
    paint(
        0x1C09,
        0x1E00,
        "runtime_workspace_cleared_on_start",
        "confirmed",
        "reachable 07E7 LDIR zero-fill covers 1C09-1F9F",
    )
    for table in tables:
        paint(
            table.start,
            table.end,
            f"dispatch_table:{table.name}",
            table.confidence,
            f"shape-validated dispatcher at {table.dispatcher:04X}",
        )
    for address, instruction in cfg.instructions.items():
        confidence = cfg.confidence[address]
        for byte_address in range(address, address + instruction.size):
            labels[byte_address] = (
                "reachable_z80_code",
                confidence,
                f"instruction starts at {address:04X}",
            )

    rows = []
    start = 0
    current = labels[0]
    for address in range(1, len(labels) + 1):
        if address == len(labels) or labels[address] != current:
            category, confidence, evidence = current
            rows.append(
                {
                    "start": start,
                    "end_exclusive": address,
                    "length": address - start,
                    "category": category,
                    "confidence": confidence,
                    "evidence": evidence,
                }
            )
            if address < len(labels):
                start = address
                current = labels[address]
    return rows


def load_m68k_interface(code_generated: Path | None) -> dict[str, Any]:
    if code_generated is None:
        return {
            "status": "unknown",
            "reason": "No M68000 code map was supplied",
            "mailbox_function": [],
            "call_sites": [],
        }
    instructions_path = code_generated / "instructions.csv"
    edges_path = code_generated / "edges.csv"
    if not instructions_path.is_file() or not edges_path.is_file():
        return {
            "status": "unknown",
            "reason": "M68000 code-map CSV files were not present",
            "mailbox_function": [],
            "call_sites": [],
        }
    rows: dict[int, dict[str, str]] = {}
    with instructions_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows[int(row["address"])] = row
    mailbox_function = []
    for address in sorted(rows):
        if 0x00808A <= address <= 0x0080CE:
            row = rows[address]
            mailbox_function.append(
                {
                    "address": address,
                    "bytes": row["bytes"],
                    "mnemonic": row["mnemonic"],
                    "operand": row["operand"],
                    "confidence": row["confidence"],
                }
            )
    incoming: list[dict[str, Any]] = []
    with edges_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for edge in csv.DictReader(handle):
            if edge.get("target_hex") != "00808A" or edge.get("type") not in {"call", "jump"}:
                continue
            source = int(edge["source"])
            source_row = rows.get(source, {})
            command: int | None = None
            command_address: int | None = None
            for predecessor_address in sorted(
                (value for value in rows if source - 20 <= value < source), reverse=True
            ):
                predecessor = rows[predecessor_address]
                match = re.search(
                    r"#\$([0-9a-f]+),\s*d0$", predecessor.get("operand", ""), re.I
                )
                if match and predecessor.get("mnemonic", "").startswith("move"):
                    command = int(match.group(1), 16) & 0xFF
                    command_address = predecessor_address
                    break
            incoming.append(
                {
                    "source": source,
                    "edge_type": edge["type"],
                    "confidence": source_row.get("confidence", "unknown"),
                    "immediate_command": command,
                    "command_load_address": command_address,
                    "status": edge.get("status", ""),
                }
            )
    incoming.sort(key=lambda row: row["source"])
    function_complete = [row["address"] for row in mailbox_function] == [
        0x00808A,
        0x008090,
        0x008098,
        0x0080A0,
        0x0080A2,
        0x0080A8,
        0x0080AA,
        0x0080B0,
        0x0080B2,
        0x0080B8,
        0x0080BA,
        0x0080C0,
        0x0080C6,
        0x0080CE,
    ]
    return {
        "status": "confirmed" if function_complete else "probable",
        "m68k_address_space": "linear ROM execution addresses",
        "z80_address_space": "Z80 RAM; M68000 sees it at A00000+A",
        "function_entry": 0x00808A,
        "protocol": [
            "set FF3F00 guard flag",
            "request Z80 bus through A11100 and wait for grant",
            "write D0 low byte to A01C0A if empty, otherwise A01C0B if empty",
            "drop the command if both slots are occupied",
            "clear guard and release Z80 bus",
        ],
        "mailboxes": [
            {
                "m68k_address": 0xA01C0A,
                "z80_address": 0x1C0A,
                "role": "primary command slot",
                "status": "confirmed",
            },
            {
                "m68k_address": 0xA01C0B,
                "z80_address": 0x1C0B,
                "role": "secondary command slot",
                "status": "confirmed",
            },
            {
                "m68k_address": 0xA01C0C,
                "z80_address": 0x1C0C,
                "role": "Z80-polled third/internal slot; no direct 68000 writer proven",
                "status": "probable",
            },
        ],
        "z80_consumer_entry": 0x087F,
        "mailbox_function": mailbox_function,
        "call_sites": incoming,
    }


def assign_function_owners(cfg: ConservativeCFG) -> dict[int, list[int]]:
    intraprocedural = defaultdict(list)
    for edge in cfg.edges:
        if edge["status"] != "resolved" or edge["target"] is None:
            continue
        if edge["type"] in {"fallthrough", "branch_taken", "jump"}:
            intraprocedural[edge["source"]].append(edge["target"])
    entries = set(cfg.functions)
    owners: dict[int, set[int]] = defaultdict(set)
    for entry in sorted(entries):
        queue = deque([entry])
        seen: set[int] = set()
        while queue:
            address = queue.popleft()
            if address in seen or address not in cfg.instructions:
                continue
            if address != entry and address in entries:
                continue
            seen.add(address)
            owners[address].add(entry)
            queue.extend(intraprocedural.get(address, []))
    return {address: sorted(values) for address, values in owners.items()}


def build_call_graph(cfg: ConservativeCFG, owners: dict[int, list[int]]) -> list[dict[str, Any]]:
    rows = []
    for edge in cfg.edges:
        if edge["type"] not in {"call", "rst"}:
            continue
        source_owners = owners.get(edge["source"], [])
        rows.append(
            {
                "source_instruction": edge["source"],
                "source_functions": source_owners,
                "target_function": edge["target"],
                "type": edge["type"],
                "confidence": edge["confidence"],
                "status": edge["status"],
            }
        )
    return rows


def serialise_instructions(
    cfg: ConservativeCFG, owners: dict[int, list[int]]
) -> list[dict[str, Any]]:
    rows = []
    for address in sorted(cfg.instructions):
        instruction = cfg.instructions[address]
        rows.append(
            {
                "address": address,
                "size": instruction.size,
                "bytes": instruction.raw.hex(),
                "mnemonic": instruction.mnemonic,
                "operand": instruction.operand,
                "flow_type": instruction.flow_type,
                "target": instruction.target,
                "confidence": cfg.confidence[address],
                "function_owners": owners.get(address, []),
                "discovery_evidence": cfg.evidence[address],
            }
        )
    return rows


def coverage_summary(
    image: bytes, strict: ConservativeCFG, final: ConservativeCFG
) -> dict[str, Any]:
    strict_sets = strict.code_byte_sets()
    final_sets = final.code_byte_sets()
    strict_bytes = set().union(*strict_sets.values()) if strict_sets else set()
    final_bytes = set().union(*final_sets.values()) if final_sets else set()
    confirmed = final_sets.get("confirmed", set())
    probable = final_sets.get("probable", set()) - confirmed
    driver_extent = 0x0FCA
    final_driver = {value for value in final_bytes if value < driver_extent}
    unresolved_unique = {
        (row["source"], row["type"], row.get("target")) for row in final.unresolved
    }
    return {
        "loaded_image_bytes": len(image),
        "strict_direct_flow_instruction_count": len(strict.instructions),
        "strict_direct_flow_code_bytes": len(strict_bytes),
        "final_instruction_count": len(final.instructions),
        "final_code_bytes": len(final_bytes),
        "confirmed_code_bytes": len(confirmed),
        "probable_only_code_bytes": len(probable),
        "dispatch_added_code_bytes": len(final_bytes - strict_bytes),
        "loaded_image_code_percent": round(len(final_bytes) * 100 / len(image), 6),
        "driver_extent_start": 0,
        "driver_extent_end_exclusive": driver_extent,
        "driver_extent_bytes": driver_extent,
        "driver_reachable_code_bytes": len(final_driver),
        "driver_reachable_code_percent": round(
            len(final_driver) * 100 / driver_extent, 6
        ),
        "highest_reachable_instruction_end": max(
            (address + instruction.size for address, instruction in final.instructions.items()),
            default=0,
        ),
        "conflict_count": len(final.conflicts),
        "decode_failure_count": len(final.decode_failures),
        "unresolved_transfer_count": len(unresolved_unique),
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            cooked = {}
            for field in fields:
                value = row.get(field, "")
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False, sort_keys=True)
                cooked[field] = value
            writer.writerow(cooked)


def write_listing(path: Path, instruction_rows: list[dict[str, Any]]) -> None:
    lines = []
    for row in instruction_rows:
        marker = "C" if row["confidence"] == "confirmed" else "P"
        target = "" if row["target"] is None else f" -> {row['target']:04X}"
        lines.append(
            f"{row['address']:04X}: [{marker}] {row['bytes']:<16} "
            f"{row['mnemonic']:<6} {row['operand']}{target}".rstrip()
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def crosscheck_mame_linear_listing(
    listing_path: Path, instruction_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    if not listing_path.is_file():
        return {
            "status": "not_run",
            "reason": f"listing absent: {listing_path}",
        }
    boundaries: dict[int, str] = {}
    pattern = re.compile(r"^([0-9a-fA-F]{4}):\s+((?:[0-9a-fA-F]{2}\s+)+)")
    for line in listing_path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = pattern.match(line)
        if match:
            boundaries[int(match.group(1), 16)] = "".join(match.group(2).split()).lower()
    compared = []
    absent = []
    mismatches = []
    for row in instruction_rows:
        expected = boundaries.get(row["address"])
        if expected is None:
            absent.append(row["address"])
            continue
        compared.append(row["address"])
        if expected != row["bytes"]:
            mismatches.append(
                {
                    "address": row["address"],
                    "recursive_bytes": row["bytes"],
                    "mame_linear_bytes": expected,
                }
            )
    return {
        "status": "exact_on_shared_boundaries" if not mismatches else "mismatch",
        "listing": portable_project_path(listing_path),
        "reachable_instruction_count": len(instruction_rows),
        "shared_instruction_boundaries": len(compared),
        "exact_byte_and_length_matches": len(compared) - len(mismatches),
        "reachable_boundaries_absent_from_linear_sweep": absent,
        "mismatches": mismatches,
        "caveat": "MAME listing supplies a decoder cross-check",
    }


def load_runtime_capture_evidence(path: Path, runtime: bytes) -> dict[str, Any]:
    if not path.is_file():
        return {"status": "not_available", "path": str(path)}
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    capture = payload.get("z80_capture", {})
    expected_hash = capture.get("expected_sha256")
    if expected_hash != sha256(runtime) or capture.get("size") != len(runtime):
        return {
            "status": "rejected",
            "path": portable_project_path(path),
            "reason": "capture summary belongs to a different runtime image",
            "summary_expected_sha256": expected_hash,
            "actual_expected_sha256": sha256(runtime),
        }
    return {
        "status": "confirmed_crosscheck",
        "path": portable_project_path(path),
        "capture_sha256": capture.get("capture_sha256"),
        "expected_sha256": expected_hash,
        "size": capture.get("size"),
        "matching_bytes": capture.get("matching_bytes"),
        "different_bytes": capture.get("different_bytes"),
        "match_ratio": capture.get("match_ratio"),
        "first_difference_offsets": capture.get("first_difference_offsets", []),
        "interpretation": "differences begin in runtime workspace after driver startup",
    }


def render_report(result: dict[str, Any]) -> str:
    rom = result["source"]
    coverage = result["coverage"]
    runtime = result["payload_manifest"]["runtime"]
    lines = [
        "# Z80 驱动地址图",
        "",
        f"- 输入：{rom['path']}。",
        f"- 运行映像：{runtime['size']} 字节。",
        f"- 指令：{len(result['instructions'])} 条。",
        f"- 访存记录：{len(result['memory_references'])} 项。",
        f"- 解码冲突：{len(result['conflicts'])} 项。",
        f"- 动态目标：{len(result['unresolved_transfers'])} 项。",
        "",
        "地址表和反汇编使用 Z80 运行地址。完整 JSON 保存控制流、硬件访问、ROM 地址映射与覆盖统计。",
        "",
    ]
    lines.extend(f"- {name}: {value}" for name, value in coverage.items() if type(value) in (int, float))
    return "\n".join(lines) + "\n"


def build_result(
    rom_path: Path,
    rom: bytes,
    components: dict[str, bytes],
    image: bytes,
    strict: ConservativeCFG,
    final: ConservativeCFG,
    tables: list[DispatchTable],
    m68k_interface: dict[str, Any],
    mame_listing: Path | None = None,
    runtime_capture_summary: Path | None = None,
) -> dict[str, Any]:
    owners = assign_function_owners(final)
    instructions = serialise_instructions(final, owners)
    memory_rows = memory_reference_rows(final)
    hardware_rows = hardware_access_rows(memory_rows)
    bank = simulate_bank_configuration(components["overlay_1c00"])
    bank_map = build_banked_audio_map(rom, image, final, bank)
    runtime, shadow = compose_runtime(components)
    component_rebuilt = rebuild_rom(rom, components)
    flattened_rebuilt = rebuild_rom(rom, components_from_runtime(runtime, shadow))
    functions = []
    for address in sorted(final.functions):
        row = dict(final.functions[address])
        symbol = KNOWN_SYMBOLS.get(address)
        row["symbol"] = symbol[0] if symbol else f"z80_sub_{address:04x}"
        row["semantic_confidence"] = symbol[1] if symbol else "unknown"
        row["semantic_evidence"] = symbol[2] if symbol else "not yet named"
        functions.append(row)
    dispatch_by_source = {table.dispatcher: table for table in tables}
    unresolved = []
    unresolved_seen: set[tuple[Any, ...]] = set()
    for item in final.unresolved:
        copy = dict(item)
        table = dispatch_by_source.get(copy["source"])
        if table and copy["type"] == "indirect_jump":
            copy["type"] = "indirect_jump_partially_resolved_by_table"
            copy["resolved_table"] = table.name
            copy["resolved_target_count"] = len(table.entries)
        key = (copy["source"], copy["type"], copy.get("target"))
        if key in unresolved_seen:
            continue
        unresolved_seen.add(key)
        unresolved.append(copy)
    result = {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "path": portable_project_path(rom_path),
            "size": len(rom),
            "sha256": sha256(rom),
        },
        "address_spaces": {
            "rom": "linear deinterleaved Mega Drive ROM byte offsets",
            "m68k": "68000 CPU addresses for this fixed ROM mapping",
            "z80_ram": "Z80 logical RAM addresses 0000-1FFF",
            "z80_banked_window": "Z80 8000-FFFF mapped through serial bank register",
        },
        "confidence_policy": {
            "confirmed": "architectural/direct machine-code evidence or exact validated transfer/table mechanics",
            "probable": "shape-validated indirect target or semantic inference with multiple structural anchors",
            "candidate": "suggested data boundary",
            "unknown": "classification pending",
        },
        "payload_manifest": build_manifest(rom, components),
        "roundtrip_validation": {
            "component_rebuild_exact": component_rebuilt == rom,
            "component_rebuild_sha256": sha256(component_rebuilt),
            "runtime_plus_shadow_rebuild_exact": flattened_rebuilt == rom,
            "runtime_plus_shadow_rebuild_sha256": sha256(flattened_rebuilt),
            "source_overlap_consistent": runtime[0x0FCA:0x1000]
            == runtime[0x1000:0x1036],
            "flattened_runtime_alone_lossless": False,
            "required_sidecar": "z80_runtime_shadow_1c00.bin",
        },
        "coverage": coverage_summary(image, strict, final),
        "vectors": [
            {"address": 0x0000, "kind": "reset", "status": "confirmed"},
            {"address": 0x0038, "kind": "IM1 interrupt", "status": "confirmed"},
            {
                "address": 0x0066,
                "kind": "architectural NMI location",
                "status": "unknown_not_seeded",
                "caveat": "falls within reset-main reachable code; no NMI trigger evidence",
            },
        ],
        "instructions": instructions,
        "edges": final.edges,
        "functions": functions,
        "call_graph": build_call_graph(final, owners),
        "dispatch_tables": [table.to_dict() for table in tables],
        "primary_runtime_regions": _compress_primary_regions(image, final, tables),
        "runtime_state_fields": runtime_state_fields(image),
        "memory_references": memory_rows,
        "hardware_accesses": hardware_rows,
        "banked_audio_map": bank_map,
        "m68k_z80_interface": m68k_interface,
        "conflicts": final.conflicts,
        "decode_failures": final.decode_failures,
        "unresolved_transfers": unresolved,
    }
    result["mame_linear_crosscheck"] = crosscheck_mame_linear_listing(
        mame_listing, instructions
    ) if mame_listing is not None else {"status": "not_run"}
    result["runtime_capture_evidence"] = load_runtime_capture_evidence(
        runtime_capture_summary, runtime
    ) if runtime_capture_summary is not None else {"status": "not_available"}
    return result


def write_outputs(output: Path, result: dict[str, Any], rom: bytes, components: dict[str, bytes]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    write_extraction(output, rom, components)
    (output / "z80_audio_map.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(
        output / "instructions.csv",
        result["instructions"],
        [
            "address",
            "size",
            "bytes",
            "mnemonic",
            "operand",
            "flow_type",
            "target",
            "confidence",
            "function_owners",
            "discovery_evidence",
        ],
    )
    write_csv(
        output / "edges.csv",
        result["edges"],
        ["source", "target", "type", "confidence", "status"],
    )
    write_csv(
        output / "functions.csv",
        result["functions"],
        [
            "address",
            "symbol",
            "confidence",
            "semantic_confidence",
            "entry_types",
            "semantic_evidence",
            "evidence",
        ],
    )
    write_csv(
        output / "call_graph.csv",
        result["call_graph"],
        [
            "source_instruction",
            "source_functions",
            "target_function",
            "type",
            "confidence",
            "status",
        ],
    )
    table_rows = []
    for table in result["dispatch_tables"]:
        for entry in table["entries"]:
            row = {
                "table": table["name"],
                "table_confidence": table["confidence"],
                "dispatcher": table["dispatcher"],
                **entry,
            }
            table_rows.append(row)
    write_csv(
        output / "dispatch_table_entries.csv",
        table_rows,
        [
            "table",
            "table_confidence",
            "dispatcher",
            "index",
            "command",
            "entry_address",
            "target",
            "target_valid",
            "confidence",
        ],
    )
    write_csv(
        output / "regions.csv",
        result["primary_runtime_regions"],
        ["start", "end_exclusive", "length", "category", "confidence", "evidence"],
    )
    write_csv(
        output / "runtime_state_fields.csv",
        result["runtime_state_fields"],
        [
            "start",
            "end_exclusive",
            "length",
            "name",
            "initial_bytes",
            "present_in_1e00_image",
            "confidence",
            "evidence",
        ],
    )
    write_csv(
        output / "memory_references.csv",
        result["memory_references"],
        [
            "instruction",
            "instruction_text",
            "target",
            "direction",
            "width",
            "addressing",
            "region",
            "confidence",
        ],
    )
    write_csv(
        output / "hardware_accesses.csv",
        result["hardware_accesses"],
        [
            "instruction",
            "instruction_text",
            "target",
            "hardware",
            "direction",
            "width",
            "confidence",
        ],
    )
    write_csv(
        output / "m68k_mailbox_calls.csv",
        result["m68k_z80_interface"].get("call_sites", []),
        [
            "source",
            "edge_type",
            "confidence",
            "immediate_command",
            "command_load_address",
            "status",
        ],
    )
    write_csv(
        output / "conflicts.csv",
        result["conflicts"],
        ["type", "target", "overlap_at", "owner", "source", "confidence"],
    )
    write_csv(
        output / "decode_failures.csv",
        result["decode_failures"],
        ["address", "source", "confidence", "error"],
    )
    write_csv(
        output / "unresolved_transfers.csv",
        result["unresolved_transfers"],
        [
            "source",
            "type",
            "target",
            "confidence",
            "detail",
            "resolved_table",
            "resolved_target_count",
        ],
    )
    write_listing(output / "reachable_disassembly.lst", result["instructions"])
    (output / "Z80_AUDIO_REPORT.md").write_text(
        render_report(result), encoding="utf-8"
    )
    validation = result["roundtrip_validation"]
    mame = result.get("mame_linear_crosscheck", {})
    (output / "VALIDATION.md").write_text(
        "# Z80 payload validation\n\n"
        f"- Component rebuild exact: `{validation['component_rebuild_exact']}`\n"
        f"- Runtime + shadow rebuild exact: `{validation['runtime_plus_shadow_rebuild_exact']}`\n"
        f"- Shared 0x36-byte source copies agree: `{validation['source_overlap_consistent']}`\n"
        f"- MAME shared-boundary byte/length matches: "
        f"`{mame.get('exact_byte_and_length_matches', 0)}/"
        f"{mame.get('shared_instruction_boundaries', 0)}`\n"
        f"- Conflicts preserved: `{len(result['conflicts'])}`\n"
        f"- Decode failures preserved: `{len(result['decode_failures'])}`\n",
        encoding="utf-8",
    )


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True, help="linear G-5510 BIN")
    parser.add_argument("--output", type=Path, required=True, help="fresh output directory")
    parser.add_argument(
        "--m68k-code-generated",
        type=Path,
        help="optional directory with 68000 instructions.csv and edges.csv",
    )
    parser.add_argument(
        "--mame-linear-listing",
        type=Path,
        help="optional existing listing from MAME unidasm",
    )
    parser.add_argument(
        "--runtime-capture-summary",
        type=Path,
        help="optional existing report from analyze_runtime_capture.py",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.output.exists() or args.output.is_symlink():
        parser.error("--output must name a fresh directory")
    rom = args.rom.read_bytes()
    components = extract_components(rom)
    image, _shadow = compose_runtime(components)
    strict, final, tables = analyse_cfg(image)
    interface = load_m68k_interface(args.m68k_code_generated)
    result = build_result(
        args.rom,
        rom,
        components,
        image,
        strict,
        final,
        tables,
        interface,
        args.mame_linear_listing,
        args.runtime_capture_summary,
    )
    write_outputs(args.output, result, rom, components)
    print(json.dumps(result["coverage"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
