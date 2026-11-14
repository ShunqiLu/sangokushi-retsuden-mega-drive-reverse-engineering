#!/usr/bin/env python3
"""Stateful syntax recovery from original music, SFX and rhythm channel entries.

This follows the game's Z80 readers, not a generic music-file specification.
Static stream interpretation is distinct from scheduled playback. Unsupported
memory aliases and external-state changes remain explicit analysis outcomes.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.audio_formats import audio_formats as formats

WIDTHS = (1,1,1,0,5,2,1,0,1,2,3,3,1,2,2,None,4,2,0,1,1,1,2,4,2,0,1,1,1,1,4,None)
NAMES = ("pan","fine_detune","global_1c16","stop_reset","pan_envelope","attenuation_pair",
         "fm_attenuation","tie","note_off_delay","lfo_pan","timers","add_timers","psg_attenuation",
         "relative_register","absolute_register","instrument","vibrato_parameters","modulation_pair",
         "stop","psg_noise","modulation","psg_envelope","jump","loop","call","return",
         "duration_multiplier","transpose","slide_mode","raw_frequency_mode","channel3_frequencies","extended")
FF_WIDTHS = (1,1,1,1,None,1,4,2)
FM_RHYTHM = (0xA80,0xAA2,0xAAE,0xAB7,0xACB,0xAED,0xAC2,0xB0F,0xB34,0xB56)
PSG_RHYTHM = (0xA4A,0xA55)
ROM_SHA256 = formats.ROM_SHA256


class SequenceError(ValueError):
    pass


class Memory:
    def __init__(self, rom: bytes):
        self.rom = rom

    @staticmethod
    def offset(address: int) -> int:
        if type(address) is not int or not 0 <= address <= 0xFFFF:
            raise SequenceError("invalid Z80 address")
        if address < 0x1000:
            return 0x69D2 + address
        if address < 0x1C00:
            return 0x699C + address
        if address >= 0x8000:
            return 0xF0000 + address
        raise SequenceError(f"unbacked_runtime_read:{address:04X}")

    def read(self, address: int, count: int = 1) -> bytes:
        if type(count) is not int or count < 0 or address + count > 0x10000:
            raise SequenceError("wrapped_or_oversize_read")
        offsets = [self.offset(address + i) for i in range(count)]
        if offsets and offsets != list(range(offsets[0], offsets[0] + count)):
            raise SequenceError("copy_alias_boundary_read")
        return bytes(self.rom[i] for i in offsets)

    def byte(self, address: int) -> int:
        return self.read(address)[0]


@dataclass(frozen=True)
class Mode:
    reader: str = "ordinary"
    raw_frequency: bool = False
    slide: bool = False


def decode(memory: Memory, pc: int, mode: Mode) -> dict[str, Any]:
    """Decode exactly one command or timed event using the original read order."""
    if mode.reader not in ("ordinary", "rhythm"):
        raise SequenceError("unknown reader")
    first = memory.byte(pc)
    if first >= 0xE0:
        size = WIDTHS[first - 0xE0]
        if first == 0xEF:
            size = 2 if memory.byte(pc + 1) & 0x80 else 1
        if first == 0xFF:
            sub = memory.byte(pc + 1)
            if sub >= len(FF_WIDTHS):
                raise SequenceError(f"unbounded_ff_subcommand:{sub:02X}")
            size = FF_WIDTHS[sub]
            if sub == 4:
                count = memory.byte(pc + 4)
                if count == 0:
                    raise SequenceError("ff04_zero_count_65536_copy")
                size = 3 + count
            assert size is not None
            arguments = list(memory.read(pc + 2, size))
            return {"type": "command", "opcode": first, "subcommand": sub,
                    "arguments": arguments, "size": 2 + size}
        assert size is not None
        return {"type": "command", "opcode": first,
                "arguments": list(memory.read(pc + 1, size)), "size": size + 1}
    if mode.reader == "rhythm":
        if first < 0x80:
            return {"type": "duration", "duration": first, "size": 1}
        next_byte = memory.byte(pc + 1)
        return {"type": "rhythm", "mask": first,
                "duration": next_byte if next_byte < 0x80 else None,
                "size": 2 if next_byte < 0x80 else 1}
    # The raw-frequency test precedes the signed note/duration distinction.
    if mode.raw_frequency:
        low = memory.byte(pc + 1)
        duration_at = pc + 3 if mode.slide else pc + 2
        return {"type": "raw_frequency", "frequency": (first << 8) | low,
                "detune": memory.byte(pc + 2) if mode.slide else None,
                "duration": memory.byte(duration_at), "size": 4 if mode.slide else 3}
    if first < 0x80:
        return {"type": "duration", "duration": first, "size": 1}
    if mode.slide:
        return {"type": "note", "note": first, "detune": memory.byte(pc + 1),
                "duration": memory.byte(pc + 2), "size": 3}
    next_byte = memory.byte(pc + 1)
    return {"type": "note", "note": first, "detune": None,
            "duration": next_byte if next_byte < 0x80 else None,
            "size": 2 if next_byte < 0x80 else 1}


def seed_entries(rom: bytes) -> list[dict[str, Any]]:
    data = formats.extract(rom)
    seeds = []
    for group in ("music", "sfx"):
        for definition in data[group]:
            collections = ("ordinary_slots", "psg_slots") if group == "music" else ("slots",)
            for collection in collections:
                for index, slot in enumerate(definition[collection]):
                    seeds.append({"id": f"{definition['id']}:{collection}:{index}",
                                  "entry": slot["sequence_ptr"],
                                  "reader": "rhythm" if collection == "ordinary_slots" and index == 0 else "ordinary",
                                  "source": "header_descriptor", "definition": definition["id"],
                                  "group": group,
                                  "instrument_base": definition["header"]["instrument_base"],
                                  "psg": collection == "psg_slots" or bool(slot.get("channel_id", 0) & 0x80)})
    # Structurally valid rhythm template prefixes. Potential spawns only:
    # runtime channel collision suppression and actual mask selection are separate.
    memory = Memory(rom)
    for kind, table, descriptors in (("fm", 0xA60, FM_RHYTHM), ("psg", 0xA46, PSG_RHYTHM)):
        actual = struct.unpack("<" + str(len(descriptors)) + "H", memory.read(table, len(descriptors) * 2))
        if actual != descriptors:
            raise SequenceError("rhythm descriptor table drift")
        for index, descriptor in enumerate(descriptors):
            entry = int.from_bytes(memory.read(descriptor, 2), "little")
            seeds.append({"id": f"rhythm_{kind}_{index+1}", "entry": entry, "reader": "ordinary",
                          "source": "potential_rhythm_template", "descriptor": descriptor,
                          "instrument_base": None, "psg": kind == "psg"})
    return seeds


def walk(memory: Memory, seed: dict[str, Any], max_states: int = 200000) -> dict[str, Any]:
    """Explore deterministic local parser state to stop/repeated state/barrier.

    Timing, synthesis and external channel overwrites are not abstracted into
    evidence of actual playback. The eight shared bytes +28..2F model both
    F7 counters and the first four F8 return slots, including the SFX bank
    pointer alias. Access outside this modeled pool is an explicit barrier.
    """
    mode = Mode(seed["reader"])
    pc = seed["entry"]
    cursor = 0x30
    pool = bytearray(8)
    if seed.get("group") == "sfx":
        pool[2:4] = seed["instrument_base"].to_bytes(2, "little")
    mask = 0
    paused = False
    seen = set()
    views: dict[str, dict[str, Any]] = {}
    edges: set[tuple[int, int, str]] = set()
    issues = []
    selected = set()
    spawn_selectors = set()
    maximum_depth = 0
    status = "state_limit"
    for _ in range(max_states):
        state = (pc, mode, cursor, bytes(pool), mask, paused)
        if state in seen:
            status = "repeated_local_state"
            break
        seen.add(state)
        try:
            event = decode(memory, pc, mode)
        except SequenceError as error:
            issues.append({"address": pc, "reason": str(error)})
            status = "unresolved"
            break
        key = f"{pc:04x}:{mode.reader}:{int(mode.raw_frequency)}:{int(mode.slide)}"
        views[key] = {"id": key, "address": pc, "rom_offset": memory.offset(pc),
                      "reader": mode.reader, "raw_frequency": mode.raw_frequency, "slide": mode.slide,
                      "event": event}
        if event["type"] in ("note", "rhythm") and not (mode.slide and mode.reader == "ordinary"):
            # A >=80 lookahead controls event length without being consumed.
            if event["duration"] is None:
                views[key]["nonconsuming_lookahead"] = {"address": pc + 1,
                    "rom_offset": memory.offset(pc + 1), "value": memory.byte(pc + 1)}
        next_pc = pc + event["size"]
        edge_kind = "next"
        if event["type"] == "command":
            opcode, args = event["opcode"], event["arguments"]
            if opcode in (0xE3, 0xF2):
                status = "stop"
                break
            if opcode == 0xFC:
                mode = Mode(mode.reader, mode.raw_frequency, args[0] == 1)
            elif opcode == 0xFD:
                mode = Mode(mode.reader, args[0] == 1, mode.slide)
            elif opcode in (0xF6, 0xF8):
                if opcode == 0xF8:
                    if cursor - 2 < 0x28:
                        issues.append({"address": pc, "reason": "call_stack_aliases_unmodeled_state_at_depth5"})
                        status = "unresolved"
                        break
                    cursor -= 2
                    pool[cursor - 0x28:cursor - 0x26] = (pc + 2).to_bytes(2, "little")
                    maximum_depth = max(maximum_depth, (0x30 - cursor) // 2)
                next_pc = args[0] | args[1] << 8
                edge_kind = "call" if opcode == 0xF8 else "jump"
            elif opcode == 0xF9:
                if cursor >= 0x30:
                    issue = {"address": pc, "reason": "return_reads_next_channel_state", "channel_offset": cursor}
                    if seed.get("id") == "music_90:ordinary_slots:0" and pc == 0xBA19:
                        issue.update(conditional_target=0x81,
                            condition="pristine post-loader next channel flags80/id00; natural execution unknown")
                    issues.append(issue)
                    status = "unresolved"
                    break
                next_pc = (int.from_bytes(pool[cursor - 0x28:cursor - 0x26], "little") + 1) & 0xFFFF
                cursor += 2
                edge_kind = "return"
            elif opcode == 0xF7:
                index, count, low, high = args
                offset = (index + 0x28) & 0xFF
                if not 0x28 <= offset <= 0x2F:
                    issues.append({"address": pc, "reason": f"loop_cell_alias_outside_pool:{offset:02X}"})
                    status = "unresolved"
                    break
                index = offset - 0x28
                if pool[index] == 0:
                    pool[index] = count
                pool[index] = (pool[index] - 1) & 0xFF
                if pool[index]:
                    next_pc = low | high << 8
                    edge_kind = "loop_taken"
                else:
                    edge_kind = "loop_exit"
            elif opcode == 0xEF and not seed.get("psg") and mode.reader != "rhythm":
                base = int.from_bytes(pool[2:4], "little") if seed.get("group") == "sfx" else seed.get("instrument_base")
                selected.add((pc, args[0] & 0x7F, args[1] if args[0] & 0x80 else None, base))
            elif opcode == 0xFF:
                sub = event["subcommand"]
                if sub in (2, 4):
                    issues.append({"address": pc, "reason": "external_command_state" if sub == 2 else "self_modifying_inline_destination"})
                    status = "unresolved"
                    break
                if sub == 3 and seed.get("definition", "").startswith("music"):
                    paused = args[0] != 0
        else:
            if event["type"] == "rhythm":
                mask = event["mask"]
            if mode.reader == "rhythm" and mask != 0x80:
                fm, psg = mask & 0x0F, (mask >> 4) & 7
                if fm:
                    spawn_selectors.add((pc, "fm", fm))
                if psg:
                    spawn_selectors.add((pc, "psg", psg))
                if fm > len(FM_RHYTHM) or psg > len(PSG_RHYTHM):
                    issues.append({"address": pc, "reason": "rhythm_selector_outside_typed_prefix"})
            if paused:
                issues.append({"address": next_pc, "reason": "paused_until_external_reactivation"})
                status = "unresolved"
                break
        if not 0 <= next_pc <= 0xFFFF:
            issues.append({"address": pc, "reason": "sequence_pointer_wrap"})
            status = "unresolved"
            break
        edges.add((pc, next_pc, edge_kind))
        pc = next_pc
    else:
        issues.append({"address": pc, "reason": "analysis_state_budget_not_closure"})
    return {"seed": seed, "status": status, "states": len(seen), "maximum_call_depth": maximum_depth,
            "views": sorted(views.values(), key=lambda row: row["id"]),
            "edges": [{"source": a,"target": b,"kind": k} for a,b,k in sorted(edges)],
            "issues": issues, "selected_instruments": sorted(selected, key=lambda row: (row[0], row[1], row[2] or -1)),
            "rhythm_spawns": sorted(spawn_selectors)}


def analyse(rom: bytes) -> dict[str, Any]:
    formats.verify_rom(rom)
    memory = Memory(rom)
    contexts = [walk(memory, seed) for seed in seed_entries(rom)]
    views = {view["id"]: view for context in contexts for view in context["views"]}
    touched = {view["rom_offset"] + i for view in views.values() for i in range(view["event"]["size"])}
    return {"source": {"size": len(rom), "sha256": ROM_SHA256}, "contexts": contexts,
            "views": sorted(views.values(), key=lambda row: row["id"]),
            "summary": {"contexts": len(contexts), "unique_views": len(views), "typed_bytes": len(touched),
                        "statuses": dict(Counter(c["status"] for c in contexts)),
                        "issues": dict(Counter(i["reason"] for c in contexts for i in c["issues"])),
                        "maximum_call_depth": max(c["maximum_call_depth"] for c in contexts)}}


def selected_records(rom: bytes, result: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Resolve EF witnesses to allocated records, retaining unclosed selections."""
    definitions = formats.extract(rom)
    music = {item["command"]: item for item in definitions["music"]}
    banks = {item["id"]: item for item in definitions["instrument_banks"]}
    by_address = {(item["space"], item["z80_start"]): item for item in banks.values()}
    selected: dict[tuple[str, int], dict[str, Any]] = {}
    issues = []
    for context in result["contexts"]:
        seed = context["seed"]
        for pc, index, external, base in context["selected_instruments"]:
            space = "local" if seed.get("group") == "sfx" else "banked"
            bank = by_address.get((space, base))
            if external is not None:
                song = music.get(external)
                bank = banks[song["instrument_bank_id"]] if song else None
            witness = {"context": seed["id"], "selector_z80": pc, "selector_rom": Memory.offset(pc),
                       "index": index, "external_music": external, "current_bank": base}
            if bank is None or index >= bank["record_count"]:
                issues.append(witness | {"reason": "EF_selection_outside_typed_instrument_allocation"})
                continue
            key = (bank["id"], index)
            if key not in selected:
                selected[key] = {"id": f"{bank['id']}_record_{index}", "bank": bank["id"],
                    "index": index, "rom_offset": bank["rom_offset"] + 25 * index,
                    "record": bank["records"][index], "witnesses": []}
            selected[key]["witnesses"].append(witness)
    return [selected[key] for key in sorted(selected)], issues


def _spans(addresses: set[int]) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for address in sorted(addresses):
        if spans and spans[-1][1] == address:
            spans[-1] = (spans[-1][0], address + 1)
        else:
            spans.append((address, address + 1))
    return spans


def encode_event(event: Any, expected: dict[str, Any]) -> bytes:
    """Fixed event shape, editable operands; never an opaque hex payload."""
    formats._keys(event, expected, "event")
    for key in ("type", "size", "opcode", "subcommand"):
        if key in expected:
            formats._same(event[key], expected[key], "event." + key)
    byte = lambda value: formats._integer(value, 255, "event byte")
    kind = expected["type"]
    if kind == "command":
        formats._list_shape(event["arguments"], expected["arguments"], "command.arguments")
        raw = bytes([event["opcode"]] + ([event["subcommand"]] if "subcommand" in event else [])
                    + [byte(value) for value in event["arguments"]])
        if event["opcode"] == 0xEF and bool(event["arguments"][0] & 0x80) != bool(expected["arguments"][0] & 0x80):
            raise SequenceError("EF selector changes operand width")
        if event.get("subcommand") == 4 and event["arguments"][2] != expected["arguments"][2]:
            raise SequenceError("FF04 count changes inline span")
    elif kind == "duration":
        raw = bytes([formats._integer(event["duration"], 127, "standalone duration")])
    else:
        raw_values = []
        if kind == "raw_frequency":
            frequency = formats._integer(event["frequency"], 0xDFFF, "raw frequency")
            raw_values += [frequency >> 8, frequency & 255]
        else:
            field = "mask" if kind == "rhythm" else "note"
            value = byte(event[field])
            if not 0x80 <= value < 0xE0:
                raise SequenceError("note/rhythm outside original token domain")
            raw_values.append(value)
        if "detune" in expected:
            if expected["detune"] is None:
                formats._same(event["detune"], None, "detune presence")
            else:
                raw_values.append(byte(event["detune"]))
        if expected["duration"] is None:
            formats._same(event["duration"], None, "duration presence")
        else:
            maximum = 255 if kind == "raw_frequency" or expected.get("detune") is not None else 127
            raw_values.append(formats._integer(event["duration"], maximum, "duration"))
        raw = bytes(raw_values)
    if len(raw) != expected["size"]:
        raise SequenceError("event encoding length drift")
    return raw


def _extract_from_analysis(rom: bytes, result: dict[str, Any]) -> dict[str, Any]:
    from tools.audio_sequences import rhythm
    records, _ = selected_records(rom, result)
    return {"schema_version": 1, "format": "g5510_stateful_sequence_views",
            "source": result["source"],
            "views": [{key: value for key, value in view.items() if key != "nonconsuming_lookahead"}
                      for view in result["views"]],
            "selected_instruments": [{key: value for key, value in record.items() if key != "witnesses"}
                                     for record in records], "rhythm": rhythm.extract(rom)}


def extract(rom: bytes) -> dict[str, Any]:
    return _extract_from_analysis(rom, analyse(rom))


def rebuild(rom: bytes, assets: Any) -> bytes:
    from tools.audio_sequences import rhythm
    expected = extract(rom)
    formats._keys(assets, expected, "assets")
    for key in ("schema_version", "format", "source"):
        formats._same(assets[key], expected[key], key)
    writes: dict[int, int] = {}
    def add(start: int, raw: bytes) -> None:
        for i, value in enumerate(raw, start):
            if i in writes and writes[i] != value:
                raise SequenceError(f"conflicting aliased views at ROM {i:06X}")
            writes[i] = value
    for field in ("views", "selected_instruments"):
        formats._list_shape(assets[field], expected[field], field)
        for item, original in zip(assets[field], expected[field]):
            formats._keys(item, original, field)
            payload = "event" if field == "views" else "record"
            for key in original.keys() - {payload}:
                formats._same(item[key], original[key], field + "." + key)
            raw = encode_event(item[payload], original[payload]) if payload == "event" else formats._encode_record(item[payload], original[payload], item["id"])
            add(item["rom_offset"], raw)
    rhythm_rebuilt = rhythm.rebuild(rom, assets["rhythm"])
    for item in rhythm.ranges(rom):
        add(item["start"], rhythm_rebuilt[item["start"]:item["end"]])
    rebuilt = bytearray(rom)
    for offset, value in writes.items():
        rebuilt[offset] = value
    result = bytes(rebuilt)
    memory = Memory(result)
    # Validate optional lookahead and all aliased views against final bytes.
    # This does not claim edited branch targets or inter-channel timing play correctly.
    for view in assets["views"]:
        actual = decode(memory, view["address"], Mode(view["reader"], view["raw_frequency"], view["slide"]))
        if actual != view["event"]:
            raise SequenceError("edited bytes change a retained event view: " + view["id"])
    return result


ANCHORS = (
    ("ordinary_reader", 0x1D6, 0x2A8, "note/raw/slide read order and duration multiplication"),
    ("channel_initialization", 0x6C2, 0x6EC, "stack cursor30 and zero channel state after descriptor"),
    ("rhythm_reader", 0x98F, 0xA46, "rhythm mask/duration parser and nested template selection"),
    ("command_continuation", 0xB78, 0xB88, "shared command dispatch and ordinary INC DE continuation"),
    ("extended_handlers", 0xC2C, 0xC7D, "FF02 clobbered DE, FF03 active flags, FF04 inline LDIR"),
    ("instrument_consumer", 0xD2D, 0xD6A, "EF local/external bank selection"),
)


def _manifest_from_analysis(rom: bytes, result: dict[str, Any]) -> dict[str, Any]:
    from tools.audio_sequences import rhythm
    records, instrument_issues = selected_records(rom, result)
    selected_templates = {f"rhythm_{kind}_{index}" for c in result["contexts"]
                          if c["seed"]["source"] == "header_descriptor" for _, kind, index in c["rhythm_spawns"]}
    confirmed_ids = {view["id"] for c in result["contexts"]
                     if c["seed"]["source"] == "header_descriptor" or c["seed"]["id"] in selected_templates
                     for view in c["views"]}
    confirmed_bytes = {v["rom_offset"] + i for v in result["views"] if v["id"] in confirmed_ids
                       for i in range(v["event"]["size"])}
    all_bytes = {v["rom_offset"] + i for v in result["views"] for i in range(v["event"]["size"])}
    owners = []
    def own(start: int, end: int, kind: str, evidence: str) -> None:
        owners.append({"id": f"{kind}_{start:06x}", "start": start, "end": end, "kind": kind,
                       "confidence": "confirmed", "evidence": evidence,
                       "sha256": hashlib.sha256(rom[start:end]).hexdigest()})
    for start, end in _spans(confirmed_bytes):
        own(start, end, "typed_sequence_events", "header-seeded local parser state or witnessed rhythm mask; not natural playback")
    for record in records:
        own(record["rom_offset"], record["rom_offset"] + 25, "selected_fm_record",
            "stateful EF witness and fixed 25-byte consumer; editable field codec")
    # Templates remain probable by default; only byte ranges actually selected
    # by header-rooted masks are promoted below using the independent codec.
    rhythm_assets = rhythm.extract(rom)
    masks = sorted({0x80 | index if kind == "fm" else 0x80 | (index << 4)
        for c in result["contexts"] if c["seed"]["source"] == "header_descriptor" for _, kind, index in c["rhythm_spawns"]})
    rhythm_selection = rhythm.selection_for_masks(rom, rhythm_assets, masks)
    selected_structure: dict[int, tuple[int, str]] = {}
    for chosen in rhythm_selection["selected"]:
        descriptor = next(d for d in rhythm_assets["descriptors"] if d["id"] == chosen["descriptor_id"])
        header = next(h for h in rhythm_assets["channel_headers"] if h["family"] == chosen["family"])
        table = next(t for t in rhythm_assets["pointer_tables"] if t["id"] == chosen["family"] + "_descriptors")
        selected_structure[header["rom_offset"]] = (3, "selected_rhythm_header")
        selected_structure[descriptor["rom_offset"]] = (6, "selected_rhythm_descriptor")
        selected_structure[table["rom_offset"] + (descriptor["index"] - 1) * 2] = (2, "selected_rhythm_pointer")
        if chosen["voice_id"]:
            voice = next(v for v in rhythm_assets["voice_records"] if v["id"] == chosen["voice_id"])
            voice_table = next(t for t in rhythm_assets["pointer_tables"] if t["id"] == "fm_voices")
            selected_structure[voice["rom_offset"]] = (25, "selected_rhythm_voice")
            selected_structure[voice_table["rom_offset"] + descriptor["fields"]["voice_index"] * 2] = (2, "selected_rhythm_pointer")
    for start, (size, kind) in sorted(selected_structure.items()):
        own(start, start + size, kind, "canonical rhythm mask selects resource conditional on target bit2 clear; not playback")
    owners.sort(key=lambda row: row["start"])
    for left, right in zip(owners, owners[1:]):
        if left["end"] > right["start"]:
            raise SequenceError("confirmed sequence/instrument/rhythm ownership overlaps")
    return {"schema_version": 1, "package": "audio_sequences", "canonical_source": result["source"],
            "scope": "Statically seeded local syntax/control state; no scheduled playback or global driver closure",
            "summary": result["summary"] | {"header_contexts": 307, "potential_rhythm_contexts": 12,
                "confirmed_sequence_bytes": len(confirmed_bytes),
                "probable_sequence_bytes": len(all_bytes - confirmed_bytes),
                "selected_instrument_records": len(records),
                "instrument_witnesses": sum(len(r["witnesses"]) for r in records),
                "confirmed_rhythm_structure_bytes": sum(size for size, _ in selected_structure.values()),
                "confirmed_owned_bytes": sum(r["end"] - r["start"] for r in owners),
                "confirmed_owner_intervals": len(owners)},
            "owners": owners,
            "probable_sequence_ranges": [{"start": a,"end": b,"confidence": "probable"}
                                          for a,b in _spans(all_bytes - confirmed_bytes)],
            "rhythm_selection": rhythm_selection, "rhythm_structural_ranges": rhythm.ranges(rom),
            "instrument_records": records, "instrument_issues": instrument_issues,
            "contexts": [{key: ([v["id"] for v in value] if key == "views" else value)
                          for key,value in c.items()} for c in result["contexts"]],
            "nonconsuming_lookaheads": [{"view": v["id"], **v["nonconsuming_lookahead"]}
                                      for v in result["views"] if "nonconsuming_lookahead" in v],
            "anchors": [{"id": name, "start": 0x69D2 + a, "end": 0x69D2 + b,
                         "evidence": description, "bytes": rom[0x69D2+a:0x69D2+b].hex()}
                        for name,a,b,description in ANCHORS],
            "unknowns": ["music90 initial F9 reads adjacent channel RAM; pristine target0081 is conditional, not executed evidence.",
                "Local repeated parser state proves a syntax cycle, not a played-song duration or whole driver state cycle.",
                "External writes, SFX collisions, tempo, synthesis, envelope selector lifetimes and audible correctness remain open.",
                "FF02 DE clobber, FF04 self modification, pool-external aliases and unmapped/wrapped reads remain explicit barriers.",
                "Only mask-selected embedded templates count as confirmed sequence bytes; unselected potential templates stay probable.",
                "Edits preserve event views and byte layout, not musical validity; checksum is not silently repaired."]}


def build_manifest(rom: bytes) -> dict[str, Any]:
    return _manifest_from_analysis(rom, analyse(rom))


def _csv(rows: list[dict[str, Any]]) -> bytes:
    stream = io.StringIO(newline="")
    if rows:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def render_bundle(rom: bytes) -> dict[str, bytes]:
    result = analyse(rom)
    assets = _extract_from_analysis(rom, result)
    manifest = _manifest_from_analysis(rom, result)
    if rebuild(rom, assets) != rom:
        raise SequenceError("canonical typed sequence roundtrip failed")
    s = manifest["summary"]
    report = ["# G-5510 状态化音序", "", "所有地址须区分 Z80 与线性 ROM；本包没有新增自然播放证据。", "",
        f"319 入口上下文＝307 乐曲/SFX 描述符＋12 潜在节奏模板。{s['unique_views']} 个状态相关事件视图，{s['typed_bytes']} 字节音序可编辑回装。",
        f"静态入口有消费见证的音序 {s['confirmed_sequence_bytes']} 字节；仅潜在模板 {s['probable_sequence_bytes']} 字节保留 probable。",
        f"结束分布：{s['statuses']}；最大调用深度 {s['maximum_call_depth']}。",
        f"完整局部控制流发现 {s['selected_instrument_records']} 条 FM 记录、{s['instrument_witnesses']} 条 EF 选择见证。", "",
        "## 格式与状态", "", "普通读者先判断 E0..FF 命令，再判断 raw-frequency。普通00..7F是独立时值；80..DF音符/休止只在下一字节<80时消费可选时值。",
        "slide 模式对音符强制读取 detune:u8 和 duration:u8；raw 模式读取频率:u16be，加可选 detune 与强制 duration。强制参数允许80..FF，不是新命令。",
        "首音乐槽是独立 rhythm mask 读者，不因 raw/slide 位改变长度。保留 mask，独立 duration 会重用它；FM低4位、PSG bits4..6选模板，碰撞抑制仍属运行边界。",
        "F6跳转，F8把P+2写入通道共享池返回槽，F9读取后加1；F7使用(index+28)&FF字节偏移，计数0表示256次。池+28..2F和SFX bank指针共享真实存储，不是独立数组。",
        "E3/F2停止当前更新；FF02可能改写DE，FF04按参数源地址向内联流复制，作为显式解析边界。FF03暂停不终止当前命令链。", "",
        "## 编辑", "", "assets.json 包含带模式/地址标识的事件字段、FM寄存器字段和节奏结构；它没有整体内容哈希封印。",
        "长度、字段形状和地址保持固定；允许音高、时值、参数和寄存器修改。多个视图覆盖同一字节时必须一致；导入拒绝互相矛盾的别名及改变保留视图长度的 lookahead。",
        "manifest.json 是独立原版证据，contexts保留所有入口、分支、循环、返回、解析结果和异常；未消费的lookahead另列，不能多算为本事件字节。", "", "## 未闭合边界", ""]
    report += ["- " + text for text in manifest["unknowns"]]
    return {"assets.json": formats._json(assets), "manifest.json": formats._json(manifest),
            "owners.csv": _csv(manifest["owners"]),
            "events.csv": _csv([{"id": v["id"], "z80_address": v["address"], "rom_offset": v["rom_offset"],
                "reader": v["reader"], "raw_frequency": v["raw_frequency"], "slide": v["slide"],
                "type": v["event"]["type"], "opcode_name": NAMES[v["event"]["opcode"]-0xE0] if v["event"]["type"] == "command" else "",
                "size": v["event"]["size"], "fields": json.dumps(v["event"], sort_keys=True)} for v in result["views"]]),
            "README.md": ("\n".join(report) + "\n").encode("utf-8")}


def export_files(rom_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    source = formats.safe_path(rom_path, regular_input=True)
    target = formats.safe_path(output_dir)
    formats._separate(target, [source])
    if target.exists() or not target.parent.is_dir():
        raise SequenceError("output directory must be fresh with existing parent")
    bundle = render_bundle(formats._read(source, formats.ROM_SIZE))
    staging = Path(tempfile.mkdtemp(prefix=".audio-sequences-", dir=target.parent))
    identity, produced = staging.stat(), {}
    try:
        for name, data in bundle.items():
            with (staging / name).open("xb") as stream:
                stream.write(data)
            produced[name] = data
        formats.safe_path(output_dir)
        if target.exists():
            raise SequenceError("output appeared during generation")
        os.rename(staging, target)
    finally:
        formats._cleanup_stage(staging, produced, identity)
    return {"output": str(target), "files": sorted(bundle), "roundtrip_exact": True}


def import_files(rom_path: str | Path, asset_path: str | Path, output_file: str | Path) -> dict[str, Any]:
    source = formats.safe_path(rom_path, regular_input=True)
    asset = formats.safe_path(asset_path, regular_input=True)
    target = formats.safe_path(output_file)
    formats._separate(target, [source, asset])
    if target.exists() or not target.parent.is_dir():
        raise SequenceError("output file must be fresh with existing parent")
    rom = formats._read(source, formats.ROM_SIZE)
    result = rebuild(rom, formats.load_assets(formats._read(asset, 8 * 1024 * 1024)))
    descriptor, name = tempfile.mkstemp(prefix=".audio-sequences-", dir=target.parent)
    temporary, complete = Path(name), False
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(result)
            stream.flush()
            os.fsync(stream.fileno())
        complete = True
        formats.safe_path(output_file)
        os.link(temporary, target)
    finally:
        if temporary.exists():
            formats.safe_path(temporary, regular_input=True)
            if complete and formats._read(temporary, len(result)) == result:
                temporary.unlink()
            else:
                raise SequenceError("incomplete/modified temporary output retained")
    return {"output": str(target), "sha256": hashlib.sha256(result).hexdigest(),
            "changed_bytes": sum(a != b for a,b in zip(rom, result)), "canonical_roundtrip": result == rom}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("analyse", "export", "import"))
    parser.add_argument("--rom", type=Path, default=formats.DEFAULT_ROM)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--assets", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "analyse":
            result = analyse(formats._read(formats.safe_path(args.rom, regular_input=True), formats.ROM_SIZE))["summary"]
        else:
            if args.output is None or (args.command == "import" and args.assets is None):
                raise SequenceError("output/assets arguments required")
            result = export_files(args.rom, args.output) if args.command == "export" else import_files(args.rom, args.assets, args.output)
    except (ValueError, OSError) as error:
        parser.exit(2, f"audio_sequences: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
