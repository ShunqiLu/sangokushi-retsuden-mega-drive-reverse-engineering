#!/usr/bin/env python3
"""Resolve 68000 indirect calls and jumps using table shapes and next-PC observations."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import struct
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Sequence

import m68k_code_map as code_map


EVIDENCE_SCHEMA_VERSION = "1.0"
TRACE_PC_RE = re.compile(r"^([0-9A-Fa-f]{6}):")
PC_INDEX_SOURCE_RE = re.compile(r",\s*(d[0-7])\.w\)$")
ADDRESS_INDEX_SOURCE_RE = re.compile(r"^\((a[0-7]),\s*(d[0-7])\.w\)$")
PC_WORD_LOAD_RE = re.compile(
    r"^\$([0-9a-f]+)\(pc,\s*d[0-7]\.w\),\s*(d[0-7])$"
)
PC_LEA_RE = re.compile(r"^\$([0-9a-f]+)\(pc\),\s*(a[0-7])$")
PC_LONG_POINTER_RE = re.compile(
    r"^\$([0-9a-f]+)\(pc,\s*(d[0-7])\.w\),\s*(a[0-7])$"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def decode_summary(decoder: code_map.M68KCodeMap, address: int) -> dict[str, Any] | None:
    instruction = decoder._decode_one(address)
    if instruction is None or int(instruction.size) <= 0:
        return None
    return {
        "bytes": bytes(instruction.bytes).hex(),
        "size": int(instruction.size),
        "text": (
            instruction.mnemonic
            + (f" {instruction.op_str}" if instruction.op_str else "")
        ),
    }


def instruction_owner_map(
    rom_size: int, instructions: Iterable[dict[str, Any]]
) -> list[int]:
    owners = [-1] * rom_size
    for instruction in instructions:
        start = int(instruction["address"])
        for address in range(start, start + int(instruction["size"])):
            if 0 <= address < rom_size:
                owners[address] = start
    return owners


def previous_instructions(
    instruction_list: list[dict[str, Any]],
    instruction_index: dict[int, int],
    source: int,
    *,
    count: int = 12,
    distance: int = 0x60,
) -> list[dict[str, Any]]:
    index = instruction_index[source]
    return [
        instruction
        for instruction in instruction_list[max(0, index - count):index]
        if source - int(instruction["address"]) <= distance
    ]


def validate_effective_target(
    target: int,
    rom: bytes,
    owners: Sequence[int],
    decoder: code_map.M68KCodeMap,
) -> dict[str, Any] | None:
    if target & 1 or target < 0x200 or target >= len(rom):
        return None
    if owners[target] not in {-1, target}:
        return None
    return decode_summary(decoder, target)


def hint_map(document: dict[str, Any], rom_sha256: str) -> dict[int, dict[str, Any]]:
    reference = document.get("rom_sha256")
    if reference is not None and str(reference).lower() != rom_sha256:
        raise ValueError("use hints prepared for the input ROM")
    result: dict[int, dict[str, Any]] = {}
    for item in document.get("word_offset_table_boundaries", []):
        source = int(item["source"], 0) if isinstance(item["source"], str) else int(item["source"])
        normalised = dict(item)
        for key in ("table_start", "end_exclusive", "dispatch_base"):
            value = normalised[key]
            normalised[key] = int(value, 0) if isinstance(value, str) else int(value)
        result[source] = normalised
    return result


def bra_hint_map(document: dict[str, Any], rom_sha256: str) -> dict[int, dict[str, Any]]:
    reference = document.get("rom_sha256")
    if reference is not None and str(reference).lower() != rom_sha256:
        raise ValueError("use hints prepared for the input ROM")
    result: dict[int, dict[str, Any]] = {}
    for item in document.get("bra_w_table_sources", []):
        source_raw = item["source"]
        source = int(source_raw, 0) if isinstance(source_raw, str) else int(source_raw)
        normalised = dict(item)
        for key in ("base_hint", "first_slot_offset", "entry_count"):
            value = normalised[key]
            normalised[key] = int(value, 0) if isinstance(value, str) else int(value)
        result[source] = normalised
    return result


def recover_relative_offset_table(
    unresolved: dict[str, Any],
    *,
    rom: bytes,
    instructions: list[dict[str, Any]],
    instruction_index: dict[int, int],
    owners: Sequence[int],
    decoder: code_map.M68KCodeMap,
    boundary_hints: dict[int, dict[str, Any]],
) -> dict[str, Any] | None:
    source = int(unresolved["source"])
    source_instruction = instructions[instruction_index[source]]
    source_operand = str(source_instruction["operand"]).lower()
    direct_match = PC_INDEX_SOURCE_RE.search(source_operand)
    address_match = ADDRESS_INDEX_SOURCE_RE.match(source_operand)
    index_register = (
        direct_match.group(1)
        if direct_match
        else address_match.group(2)
        if address_match
        else None
    )
    if index_register is None:
        return None

    preceding = previous_instructions(instructions, instruction_index, source)
    table_start: int | None = None
    load_address: int | None = None
    for instruction in reversed(preceding):
        if not str(instruction["mnemonic"]).lower().startswith("move.w"):
            continue
        match = PC_WORD_LOAD_RE.match(str(instruction["operand"]).lower())
        if match and match.group(2) == index_register:
            table_start = int(match.group(1), 16)
            load_address = int(instruction["address"])
            break
    if table_start is None:
        return None

    base_hint = unresolved.get("base_hint")
    dispatch_base = int(base_hint) if base_hint is not None else None
    if dispatch_base is None and address_match:
        address_register = address_match.group(1)
        for instruction in reversed(preceding):
            match = PC_LEA_RE.match(str(instruction["operand"]).lower())
            if match and match.group(2) == address_register:
                dispatch_base = int(match.group(1), 16)
                break
    if dispatch_base is None:
        return None

    hint = boundary_hints.get(source)
    if hint:
        if hint["table_start"] != table_start or hint["dispatch_base"] != dispatch_base:
            raise ValueError(f"boundary hint mismatch at 0x{source:X}")
        end_exclusive = int(hint["end_exclusive"])
        boundary_evidence = "analyst_reviewed_boundary"
        boundary_detail = str(hint["reason"])
    else:
        known_boundaries = sorted(
            address
            for address in instruction_index
            if table_start < address < dispatch_base
        )
        if known_boundaries:
            end_exclusive = known_boundaries[0]
            boundary_evidence = "next_recursive_code_boundary"
            boundary_detail = (
                f"table stops at already-recursively-decoded instruction "
                f"0x{end_exclusive:06X}"
            )
        else:
            end_exclusive = dispatch_base
            boundary_evidence = "dispatch_base_adjacent"
            boundary_detail = "packed word table ends exactly at dispatch base"

    nominal_table_start = table_start
    byte_length = end_exclusive - nominal_table_start
    if (
        nominal_table_start < 0x200
        or end_exclusive > len(rom)
        or byte_length < 4
        or byte_length & 1
        or byte_length // 2 > 256
    ):
        return None

    # Some dispatchers intentionally make index zero impossible (for example,
    # a bit-position loop starts at one).  In that case the encoded PC base can
    # overlap the preceding RTS while the first legal entry begins at +2.  Try
    # only a small aligned prefix and select the longest completely validated
    # suffix. A candidate table ends at its first invalid entry.
    candidates: list[tuple[list[dict[str, Any]], int]] = []
    for first_offset in range(0, min(18, byte_length), 2):
        candidate_start = nominal_table_start + first_offset
        if any(owners[address] != -1 for address in range(candidate_start, end_exclusive)):
            continue
        candidate_entries: list[dict[str, Any]] = []
        for index, entry_address in enumerate(range(candidate_start, end_exclusive, 2)):
            raw_value = struct.unpack_from(">h", rom, entry_address)[0]
            effective_target = dispatch_base + raw_value
            target_decode = validate_effective_target(
                effective_target, rom, owners, decoder
            )
            if target_decode is None:
                candidate_entries = []
                break
            candidate_entries.append(
                {
                    "index": index,
                    "entry_address": entry_address,
                    "entry_address_hex": code_map.hex_address(entry_address),
                    "entry_bytes": rom[entry_address:entry_address + 2].hex(),
                    "raw_signed_value": raw_value,
                    "effective_target": effective_target,
                    "effective_target_hex": code_map.hex_address(effective_target),
                    "target_bytes": target_decode["bytes"],
                    "target_instruction": target_decode["text"],
                }
            )
        if len(candidate_entries) >= 2:
            candidates.append((candidate_entries, first_offset))
    if not candidates:
        return None
    entries, first_entry_offset = max(
        candidates, key=lambda item: (len(item[0]), -item[1])
    )
    table_start = nominal_table_start + first_entry_offset

    return {
        "kind": "signed_word_relative_offset_table",
        "table_start": table_start,
        "table_start_hex": code_map.hex_address(table_start),
        "end_exclusive": end_exclusive,
        "end_exclusive_hex": code_map.hex_address(end_exclusive),
        "entry_width": 2,
        "entry_count": len(entries),
        "nominal_table_base": nominal_table_start,
        "nominal_table_base_hex": code_map.hex_address(nominal_table_start),
        "first_entry_offset": first_entry_offset,
        "dispatch_base": dispatch_base,
        "dispatch_base_hex": code_map.hex_address(dispatch_base),
        "index_register": index_register,
        "offset_load_address": load_address,
        "boundary_evidence": boundary_evidence,
        "boundary_detail": boundary_detail,
        "entries": entries,
    }


def bra_run(
    base_hint: int,
    first_offset: int,
    *,
    rom: bytes,
    owners: Sequence[int],
    decoder: code_map.M68KCodeMap,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for index in range(256):
        slot = base_hint + first_offset + index * 4
        instruction = decoder._decode_one(slot)
        if instruction is None:
            break
        raw = bytes(instruction.bytes)
        if (
            decoder._mnemonic_base(instruction) != "bra"
            or int(instruction.size) != 4
            or raw[:2] != b"\x60\x00"
        ):
            break
        target = decoder._branch_target(instruction)
        if target is None or validate_effective_target(target, rom, owners, decoder) is None:
            break
        entries.append(
            {
                "index": index,
                "entry_address": slot,
                "entry_address_hex": code_map.hex_address(slot),
                "entry_bytes": raw.hex(),
                "raw_signed_value": struct.unpack(">h", raw[2:4])[0],
                "effective_target": slot,
                "effective_target_hex": code_map.hex_address(slot),
                "branch_target": target,
                "branch_target_hex": code_map.hex_address(target),
                "target_bytes": raw.hex(),
                "target_instruction": f"bra.w ${target:x}",
            }
        )
    return entries


def recover_bra_table(
    unresolved: dict[str, Any],
    *,
    rom: bytes,
    instructions: list[dict[str, Any]],
    instruction_index: dict[int, int],
    owners: Sequence[int],
    decoder: code_map.M68KCodeMap,
    baseline_table: dict[str, Any] | None,
    analyst_hint: dict[str, Any] | None,
) -> dict[str, Any] | None:
    source = int(unresolved["source"])
    base_hint_raw = unresolved.get("base_hint")
    if base_hint_raw is None:
        return None
    base_hint = int(base_hint_raw)
    if baseline_table:
        first_offset = int(baseline_table["first_slot_offset"])
        minimum_entries = 4
        boundary_evidence = "baseline_four_slot_shape"
    elif analyst_hint:
        if int(analyst_hint["base_hint"]) != base_hint:
            raise ValueError(f"BRA.W hint base mismatch at 0x{source:X}")
        first_offset = int(analyst_hint["first_slot_offset"])
        minimum_entries = int(analyst_hint["entry_count"])
        boundary_evidence = "analyst_reviewed_short_bra_table"
    else:
        first_offset = 0
        minimum_entries = 1
        boundary_evidence = "short_table_with_index_scale"
        preceding = previous_instructions(
            instructions, instruction_index, source, count=4, distance=0x18
        )
        source_operand = str(instructions[instruction_index[source]]["operand"]).lower()
        index_match = PC_INDEX_SOURCE_RE.search(source_operand)
        index_register = index_match.group(1) if index_match else None
        scaled = any(
            str(item["mnemonic"]).lower().split(".", 1)[0] in {"asl", "lsl"}
            and re.search(
                rf"#\$2,\s*{re.escape(index_register or '')}$",
                str(item["operand"]).lower(),
            )
            for item in preceding
        )
        if not scaled:
            return None

    candidates = [
        (
            bra_run(
                base_hint,
                offset,
                rom=rom,
                owners=owners,
                decoder=decoder,
            ),
            offset,
        )
        for offset in range(first_offset, first_offset + 18, 2)
    ]
    entries, actual_offset = max(candidates, key=lambda item: (len(item[0]), -item[1]))
    if len(entries) < minimum_entries:
        return None
    if baseline_table and actual_offset != first_offset:
        raise ValueError(f"baseline BRA.W table offset changed at 0x{source:X}")
    if analyst_hint and (
        actual_offset != first_offset
        or len(entries) != int(analyst_hint["entry_count"])
    ):
        raise ValueError(f"BRA.W hint extent mismatch at 0x{source:X}")
    return {
        "kind": "bra_w_trampoline_table",
        "table_start": entries[0]["entry_address"],
        "table_start_hex": entries[0]["entry_address_hex"],
        "end_exclusive": entries[-1]["entry_address"] + 4,
        "end_exclusive_hex": code_map.hex_address(entries[-1]["entry_address"] + 4),
        "entry_width": 4,
        "entry_count": len(entries),
        "dispatch_base": base_hint,
        "dispatch_base_hex": code_map.hex_address(base_hint),
        "first_slot_offset": actual_offset,
        "boundary_evidence": boundary_evidence,
        "boundary_detail": (
            str(analyst_hint["reason"])
            if analyst_hint
            else "consecutive aligned four-byte BRA.W trampolines; the following "
            "word is not another BRA.W slot"
        ),
        "entries": entries,
    }


def recover_pointer_table(
    unresolved: dict[str, Any],
    *,
    rom: bytes,
    instructions: list[dict[str, Any]],
    instruction_index: dict[int, int],
    owners: Sequence[int],
    decoder: code_map.M68KCodeMap,
) -> dict[str, Any] | None:
    source = int(unresolved["source"])
    operand = str(instructions[instruction_index[source]]["operand"]).lower()
    register_match = re.match(r"^\((a[0-7])\)$", operand)
    if register_match is None:
        return None
    address_register = register_match.group(1)
    table_start: int | None = None
    index_register: str | None = None
    load_address: int | None = None
    for instruction in reversed(previous_instructions(instructions, instruction_index, source)):
        if not str(instruction["mnemonic"]).lower().startswith("movea.l"):
            continue
        match = PC_LONG_POINTER_RE.match(str(instruction["operand"]).lower())
        if match and match.group(3) == address_register:
            table_start = int(match.group(1), 16)
            index_register = match.group(2)
            load_address = int(instruction["address"])
            break
    if table_start is None:
        return None
    boundaries = sorted(address for address in instruction_index if address > table_start)
    if not boundaries:
        return None
    end_exclusive = boundaries[0]
    byte_length = end_exclusive - table_start
    if byte_length < 8 or byte_length % 4 or byte_length // 4 > 128:
        return None
    if any(owners[address] != -1 for address in range(table_start, end_exclusive)):
        return None

    entries: list[dict[str, Any]] = []
    for index, entry_address in enumerate(range(table_start, end_exclusive, 4)):
        target = struct.unpack_from(">I", rom, entry_address)[0]
        target_decode = validate_effective_target(target, rom, owners, decoder)
        if target_decode is None:
            return None
        entries.append(
            {
                "index": index,
                "entry_address": entry_address,
                "entry_address_hex": code_map.hex_address(entry_address),
                "entry_bytes": rom[entry_address:entry_address + 4].hex(),
                "raw_absolute_value": target,
                "effective_target": target,
                "effective_target_hex": code_map.hex_address(target),
                "target_bytes": target_decode["bytes"],
                "target_instruction": target_decode["text"],
            }
        )
    return {
        "kind": "absolute_long_function_pointer_table",
        "table_start": table_start,
        "table_start_hex": code_map.hex_address(table_start),
        "end_exclusive": end_exclusive,
        "end_exclusive_hex": code_map.hex_address(end_exclusive),
        "entry_width": 4,
        "entry_count": len(entries),
        "index_register": index_register,
        "pointer_load_address": load_address,
        "boundary_evidence": "next_recursive_code_boundary",
        "boundary_detail": (
            f"six aligned in-ROM long pointers end at decoded code 0x{end_exclusive:06X}"
        ),
        "entries": entries,
    }


def parse_trace_transitions(
    trace_paths: Sequence[Path], source_addresses: set[int]
) -> tuple[dict[int, dict[int, dict[str, Any]]], list[dict[str, Any]]]:
    transitions: dict[int, dict[int, dict[str, Any]]] = defaultdict(dict)
    trace_metadata: list[dict[str, Any]] = []
    for path in sorted(trace_paths, key=lambda item: code_map.portable_path(item).lower()):
        scenario = path.stem
        previous_pc: int | None = None
        line_count = 0
        edge_count = 0
        with path.open("r", encoding="utf-8", errors="replace") as stream:
            for line in stream:
                match = TRACE_PC_RE.match(line)
                if match is None:
                    continue
                pc = int(match.group(1), 16)
                line_count += 1
                if previous_pc in source_addresses:
                    record = transitions[previous_pc].setdefault(
                        pc,
                        {
                            "target": pc,
                            "observation_count": 0,
                            "scenarios": Counter(),
                        },
                    )
                    record["observation_count"] += 1
                    record["scenarios"][scenario] += 1
                    edge_count += 1
                previous_pc = pc
        trace_metadata.append(
            {
                "path": code_map.portable_path(path),
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
                "scenario": scenario,
                "instruction_lines": line_count,
                "transitions_after_indirect_sources": edge_count,
            }
        )
    return transitions, trace_metadata


def build_evidence(
    rom_path: Path,
    baseline_map_path: Path,
    hints_path: Path,
    trace_paths: Sequence[Path],
    *,
    capstone_path: Path | None,
) -> dict[str, Any]:
    rom = rom_path.read_bytes()
    rom_sha256 = hashlib.sha256(rom).hexdigest()
    baseline = load_json(baseline_map_path)
    if baseline.get("rom", {}).get("sha256") != rom_sha256:
        raise ValueError("baseline code map belongs to a different ROM")
    hints_document = load_json(hints_path)
    hints = hint_map(hints_document, rom_sha256)
    bra_hints = bra_hint_map(hints_document, rom_sha256)
    capstone = code_map.load_capstone(capstone_path)
    decoder = code_map.M68KCodeMap(
        rom, capstone_module=capstone, infer_bra_tables=False
    )
    instructions = list(baseline["instructions"])
    instruction_index = {
        int(instruction["address"]): index
        for index, instruction in enumerate(instructions)
    }
    owners = instruction_owner_map(len(rom), instructions)
    baseline_bra_tables = {
        int(table["source"]): table
        for table in baseline.get("heuristic_dispatch_tables", [])
    }

    sites: list[dict[str, Any]] = []
    for unresolved in baseline["unresolved_transfers"]:
        source = int(unresolved["source"])
        source_instruction = instructions[instruction_index[source]]
        table = recover_relative_offset_table(
            unresolved,
            rom=rom,
            instructions=instructions,
            instruction_index=instruction_index,
            owners=owners,
            decoder=decoder,
            boundary_hints=hints,
        )
        mechanism = "data_driven_dispatch"
        classification_detail = "signed word offsets relative to a code base"
        if table is None:
            table = recover_pointer_table(
                unresolved,
                rom=rom,
                instructions=instructions,
                instruction_index=instruction_index,
                owners=owners,
                decoder=decoder,
            )
            if table is not None:
                mechanism = "function_pointer_call"
                classification_detail = "absolute long function pointers loaded into an address register"
        if table is None:
            table = recover_bra_table(
                unresolved,
                rom=rom,
                instructions=instructions,
                instruction_index=instruction_index,
                owners=owners,
                decoder=decoder,
                baseline_table=baseline_bra_tables.get(source),
                analyst_hint=bra_hints.get(source),
            )
            if table is not None:
                classification_detail = "PC-indexed fixed-width BRA.W trampoline table"

        if table is None:
            mechanism = "unproved_indirect_transfer"
            classification_detail = "no table shape survived conservative validation"
            table = {
                "kind": "unknown",
                "entry_count": 0,
                "entries": [],
                "boundary_evidence": "none",
                "boundary_detail": "unresolved",
            }
        sites.append(
            {
                "source": source,
                "source_hex": code_map.hex_address(source),
                "source_bytes": str(source_instruction["bytes"]),
                "source_instruction": (
                    str(source_instruction["mnemonic"])
                    + (
                        f" {source_instruction['operand']}"
                        if source_instruction["operand"]
                        else ""
                    )
                ),
                "transfer_type": unresolved["type"],
                "operand": unresolved["operand"],
                "original_reason": unresolved["reason"],
                "base_hint": unresolved.get("base_hint"),
                "mechanism": mechanism,
                "classification_confidence": (
                    "probable" if mechanism != "unproved_indirect_transfer" else "unknown"
                ),
                "classification_detail": classification_detail,
                "target_set_complete": False,
                "target_set_limit": "index range is not independently proven",
                "table": table,
                "observed_targets": [],
                "rejected_trace_transitions": [],
                "resolution_status": "probable_table_targets_only",
            }
        )

    site_by_source = {int(site["source"]): site for site in sites}
    transitions, trace_metadata = parse_trace_transitions(
        trace_paths, set(site_by_source)
    )
    rejected_rows: list[dict[str, Any]] = []
    for source, targets in sorted(transitions.items()):
        site = site_by_source[source]
        effective_targets = {
            int(entry["effective_target"])
            for entry in site["table"].get("entries", [])
        }
        for target, raw_record in sorted(targets.items()):
            scenarios = dict(sorted(raw_record["scenarios"].items()))
            record = {
                "target": target,
                "target_hex": code_map.hex_address(target),
                "observation_count": int(raw_record["observation_count"]),
                "scenario_counts": scenarios,
            }
            if target not in effective_targets:
                rejected = {
                    **record,
                    "reason": (
                        "next traced PC is outside the decoded table (interrupt or trace discontinuity)"
                    ),
                }
                site["rejected_trace_transitions"].append(rejected)
                rejected_rows.append({"source": source, **rejected})
                continue
            target_decode = decode_summary(decoder, target)
            if target_decode is None:
                raise ValueError(f"trace target no longer decodes at 0x{target:X}")
            site["observed_targets"].append(
                {
                    **record,
                    "target_bytes": target_decode["bytes"],
                    "target_instruction": target_decode["text"],
                    "evidence_level": "confirmed",
                    "corroboration": [
                        "runtime_next_pc_transition",
                        "static_table_membership",
                        "target_bytes_match_canonical_rom",
                    ],
                }
            )
        if site["observed_targets"]:
            site["resolution_status"] = "confirmed_observed_targets_partial"

    sites.sort(key=lambda item: int(item["source"]))
    mechanism_counts = Counter(site["mechanism"] for site in sites)
    transfer_counts = Counter(site["transfer_type"] for site in sites)
    runtime_sites = sum(bool(site["observed_targets"]) for site in sites)
    confirmed_edges = sum(len(site["observed_targets"]) for site in sites)
    probable_unique_targets = sum(
        len(
            {
                int(entry["effective_target"])
                for entry in site["table"].get("entries", [])
            }
        )
        for site in sites
    )
    summary = {
        "baseline_unresolved_site_count": len(baseline["unresolved_transfers"]),
        "classified_site_count": len(sites),
        "transfer_type_counts": dict(sorted(transfer_counts.items())),
        "mechanism_counts": dict(sorted(mechanism_counts.items())),
        "architectural_return_site_count": 0,
        "static_table_site_count": sum(
            site["table"].get("entry_count", 0) > 0 for site in sites
        ),
        "static_table_entry_count": sum(
            int(site["table"].get("entry_count", 0)) for site in sites
        ),
        "probable_unique_target_count": probable_unique_targets,
        "runtime_observed_site_count": runtime_sites,
        "site_without_confirmed_target_count": len(sites) - runtime_sites,
        "runtime_confirmed_edge_count": confirmed_edges,
        "runtime_confirmed_observation_count": sum(
            int(target["observation_count"])
            for site in sites
            for target in site["observed_targets"]
        ),
        "rejected_trace_transition_count": len(rejected_rows),
        "rejected_trace_observation_count": sum(
            int(row["observation_count"]) for row in rejected_rows
        ),
        "fully_resolved_site_count": 0,
        "target_domain_still_unknown_site_count": len(sites),
    }
    return {
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "rom": {
            "path": code_map.portable_path(rom_path),
            "size": len(rom),
            "sha256": rom_sha256,
        },
        "baseline": {
            "path": code_map.portable_path(baseline_map_path),
            "sha256": sha256_file(baseline_map_path),
            "schema_version": baseline.get("schema_version"),
            "coverage": baseline["coverage"],
        },
        "hints": {
            "path": code_map.portable_path(hints_path),
            "sha256": sha256_file(hints_path),
            "count": len(hints) + len(bra_hints),
        },
        "traces": trace_metadata,
        "policy": {
            "confirmed": (
                "consecutive runtime next-PC transition corroborated by an exact "
                "static table member and canonical target bytes"
            ),
            "probable": (
                "explicitly referenced ROM table with validated width, boundary, "
                "entry bytes, and even decodable in-ROM targets"
            ),
            "unknown": "open index range; each observation describes a single edge",
        },
        "summary": summary,
        "sites": sites,
    }


def site_rows(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for site in evidence["sites"]:
        table = site["table"]
        rows.append(
            {
                "source": site["source"],
                "source_hex": site["source_hex"],
                "transfer_type": site["transfer_type"],
                "source_instruction": site["source_instruction"],
                "mechanism": site["mechanism"],
                "classification_confidence": site["classification_confidence"],
                "table_kind": table.get("kind"),
                "table_start": table.get("table_start"),
                "table_start_hex": table.get("table_start_hex"),
                "table_end_exclusive": table.get("end_exclusive"),
                "table_end_exclusive_hex": table.get("end_exclusive_hex"),
                "table_entry_width": table.get("entry_width"),
                "table_entry_count": table.get("entry_count", 0),
                "boundary_evidence": table.get("boundary_evidence"),
                "observed_target_count": len(site["observed_targets"]),
                "confirmed_observation_count": sum(
                    int(item["observation_count"])
                    for item in site["observed_targets"]
                ),
                "rejected_transition_count": len(site["rejected_trace_transitions"]),
                "resolution_status": site["resolution_status"],
                "target_set_complete": site["target_set_complete"],
                "target_set_limit": site["target_set_limit"],
            }
        )
    return rows


def target_rows(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for site in evidence["sites"]:
        observed = {
            int(item["target"]): item for item in site["observed_targets"]
        }
        for entry in site["table"].get("entries", []):
            target = int(entry["effective_target"])
            runtime = observed.get(target)
            rows.append(
                {
                    "source": site["source"],
                    "source_hex": site["source_hex"],
                    "transfer_type": site["transfer_type"],
                    "mechanism": site["mechanism"],
                    "table_kind": site["table"].get("kind"),
                    "table_index": entry["index"],
                    "entry_address": entry["entry_address"],
                    "entry_address_hex": entry["entry_address_hex"],
                    "entry_bytes": entry["entry_bytes"],
                    "effective_target": target,
                    "effective_target_hex": entry["effective_target_hex"],
                    "branch_target": entry.get("branch_target"),
                    "branch_target_hex": entry.get("branch_target_hex"),
                    "evidence_level": "confirmed" if runtime else "probable",
                    "observation_count": (
                        int(runtime["observation_count"]) if runtime else 0
                    ),
                    "scenario_counts": runtime.get("scenario_counts", {}) if runtime else {},
                    "target_set_complete": False,
                }
            )
    return rows


def markdown_report(evidence: dict[str, Any], enhanced_result: dict[str, Any]) -> str:
    summary = evidence["summary"]
    coverage = enhanced_result["coverage"]
    lines = [
        "# 68000 indirect transfers",
        "",
        f"- Indirect sites: {summary['classified_site_count']}",
        f"- Reachable instruction bytes: {coverage['reachable_code_bytes']}",
        f"- Confirmed runtime edges: {summary['runtime_confirmed_edge_count']}",
        "",
        "| Source | Transfer | Table | Entries | Runtime targets | Status |",
        "|---:|---|---|---:|---:|---|",
    ]
    for site in evidence["sites"]:
        table = site["table"]
        lines.append(
            f"| 0x{site['source']:06X} | {site['transfer_type']} | "
            f"{table.get('kind', 'unknown')} | {table.get('entry_count', 0)} | "
            f"{len(site['observed_targets'])} | {site['resolution_status']} |"
        )
    lines.extend(("", "Table shapes supply candidate targets. An observed transition confirms its own edge.", ""))
    return "\n".join(lines)


def write_text_lf(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


def write_indirect_outputs(
    output_dir: Path,
    evidence: dict[str, Any],
    enhanced_result: dict[str, Any],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = output_dir / "indirect_evidence.json"
    write_text_lf(
        evidence_path,
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
    )
    code_map.write_csv(
        output_dir / "indirect_sites.csv",
        [
            "source",
            "source_hex",
            "transfer_type",
            "source_instruction",
            "mechanism",
            "classification_confidence",
            "table_kind",
            "table_start",
            "table_start_hex",
            "table_end_exclusive",
            "table_end_exclusive_hex",
            "table_entry_width",
            "table_entry_count",
            "boundary_evidence",
            "observed_target_count",
            "confirmed_observation_count",
            "rejected_transition_count",
            "resolution_status",
            "target_set_complete",
            "target_set_limit",
        ],
        site_rows(evidence),
    )
    code_map.write_csv(
        output_dir / "indirect_targets.csv",
        [
            "source",
            "source_hex",
            "transfer_type",
            "mechanism",
            "table_kind",
            "table_index",
            "entry_address",
            "entry_address_hex",
            "entry_bytes",
            "effective_target",
            "effective_target_hex",
            "branch_target",
            "branch_target_hex",
            "evidence_level",
            "observation_count",
            "scenario_counts",
            "target_set_complete",
        ],
        target_rows(evidence),
    )
    rejected_rows = [
        {
            "source": site["source"],
            "source_hex": site["source_hex"],
            **item,
        }
        for site in evidence["sites"]
        for item in site["rejected_trace_transitions"]
    ]
    code_map.write_csv(
        output_dir / "rejected_trace_transitions.csv",
        [
            "source",
            "source_hex",
            "target",
            "target_hex",
            "observation_count",
            "scenario_counts",
            "reason",
        ],
        rejected_rows,
    )
    write_text_lf(
        output_dir / "INDIRECT_TRANSFER_REPORT.md",
        markdown_report(evidence, enhanced_result),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Recover and validate evidence for M68000 indirect transfers"
    )
    parser.add_argument("rom", type=Path)
    parser.add_argument("--baseline-code-map", type=Path, required=True)
    parser.add_argument("--trace", type=Path, action="append", default=[])
    parser.add_argument("--trace-summary", type=Path, action="append", default=[])
    parser.add_argument("--hints", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--capstone-path", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rom_before = args.rom.read_bytes()
    runtime_trace = code_map.load_runtime_trace_summaries(
        args.trace_summary, rom_before
    )
    capstone = code_map.load_capstone(args.capstone_path)
    root_baseline_document = load_json(args.baseline_code_map)
    root_sources = {
        int(item["source"])
        for item in root_baseline_document["unresolved_transfers"]
    }
    iteration_records: list[dict[str, Any]] = []
    evidence: dict[str, Any] | None = None
    enhanced_result: dict[str, Any] | None = None

    # Importing probable table members intentionally discovers additional code.
    # That code can contain further genuine indirect instructions, so iterate
    # until the analysed site's set equals the evidence site's set.  Temporary
    # Intermediate maps support convergence; the output records the final map.
    with tempfile.TemporaryDirectory(prefix="m68k_indirect_") as temporary:
        current_baseline_path = args.baseline_code_map
        for iteration in range(1, 9):
            evidence = build_evidence(
                args.rom,
                current_baseline_path,
                args.hints,
                args.trace,
                capstone_path=args.capstone_path,
            )
            evidence_path_iteration = Path(temporary) / f"evidence_{iteration:02d}.json"
            write_text_lf(
                evidence_path_iteration,
                json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
            )
            loaded_iteration = code_map.load_indirect_evidence(
                evidence_path_iteration, rom_before
            )
            analysis = code_map.M68KCodeMap(
                rom_before,
                capstone_module=capstone,
                runtime_trace=runtime_trace,
                indirect_evidence=loaded_iteration,
            )
            analysis.analyse()
            enhanced_result = analysis.result(args.rom)
            if not enhanced_result["validation"]["all_passed"]:
                raise RuntimeError(
                    f"enhanced indirect map failed internal validation at iteration {iteration}"
                )
            evidence_sources = {int(site["source"]) for site in evidence["sites"]}
            result_sources = {
                int(item["source"])
                for item in enhanced_result["unresolved_transfers"]
            }
            iteration_records.append(
                {
                    "iteration": iteration,
                    "evidence_site_count": len(evidence_sources),
                    "result_site_count": len(result_sources),
                    "new_site_count": len(result_sources - evidence_sources),
                    "reachable_code_bytes": enhanced_result["coverage"][
                        "reachable_code_bytes"
                    ],
                    "conflict_count": enhanced_result["coverage"]["conflict_count"],
                    "decode_failure_count": enhanced_result["coverage"][
                        "decode_failure_count"
                    ],
                }
            )
            if result_sources == evidence_sources:
                break
            current_baseline_path = Path(temporary) / f"code_map_{iteration:02d}.json"
            write_text_lf(
                current_baseline_path,
                json.dumps(enhanced_result, ensure_ascii=False, indent=2) + "\n",
            )
        else:
            raise RuntimeError("indirect-site discovery did not reach a fixed point in 8 passes")

    assert evidence is not None and enhanced_result is not None
    final_site_by_source = {int(site["source"]): site for site in evidence["sites"]}
    root_baseline = {
        "path": code_map.portable_path(args.baseline_code_map),
        "sha256": sha256_file(args.baseline_code_map),
        "schema_version": root_baseline_document.get("schema_version"),
        "coverage": root_baseline_document["coverage"],
    }
    evidence["fixed_point_input"] = {
        "schema_version": evidence["baseline"].get("schema_version"),
        "coverage": evidence["baseline"].get("coverage"),
        "note": (
            "last temporary iteration input; content-derived coverage only, "
            "because temporary evidence paths are deliberately not serialized"
        ),
    }
    evidence["baseline"] = root_baseline
    evidence["root_baseline"] = root_baseline
    evidence["fixed_point_iterations"] = iteration_records
    fixed_point_input_site_count = evidence["summary"][
        "baseline_unresolved_site_count"
    ]
    evidence["summary"].update(
        {
            "baseline_unresolved_site_count": len(root_sources),
            "fixed_point_input_site_count": fixed_point_input_site_count,
            "initial_unresolved_site_count": len(root_sources),
            "newly_exposed_site_count": len(final_site_by_source) - len(root_sources),
            "initial_cohort_runtime_observed_site_count": sum(
                bool(final_site_by_source[source]["observed_targets"])
                for source in root_sources
            ),
            "initial_cohort_without_confirmed_target_count": sum(
                not final_site_by_source[source]["observed_targets"]
                for source in root_sources
            ),
            "fixed_point_iteration_count": len(iteration_records),
        }
    )

    # Publish and re-import the final document so the enhanced map records the
    # stable, user-visible evidence path rather than a temporary iteration file.
    args.output_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = args.output_dir / "indirect_evidence.json"
    write_text_lf(
        evidence_path,
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
    )
    loaded_evidence = code_map.load_indirect_evidence(evidence_path, rom_before)
    final_analysis = code_map.M68KCodeMap(
        rom_before,
        capstone_module=capstone,
        runtime_trace=runtime_trace,
        indirect_evidence=loaded_evidence,
    )
    final_analysis.analyse()
    enhanced_result = final_analysis.result(args.rom)
    if not enhanced_result["validation"]["all_passed"]:
        raise RuntimeError("final enhanced indirect map failed internal validation")
    code_map.write_outputs(args.output_dir / "enhanced_map", enhanced_result)
    if args.rom.read_bytes() != rom_before:
        raise RuntimeError("the input ROM changed during analysis")
    write_indirect_outputs(args.output_dir, evidence, enhanced_result)
    coverage = enhanced_result["coverage"]
    print(
        "M68000 indirect analysis complete: "
        f"{evidence['summary']['classified_site_count']} sites, "
        f"{evidence['summary']['runtime_confirmed_edge_count']} confirmed runtime edges, "
        f"{evidence['summary']['site_without_confirmed_target_count']} sites without a confirmed target, "
        f"{coverage['reachable_code_bytes']} reachable bytes, "
        f"{coverage['conflict_count']} conflicts, "
        f"{coverage['decode_failure_count']} decode failures"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
