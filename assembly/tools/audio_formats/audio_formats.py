#!/usr/bin/env python3
"""Canonical extraction and topology-preserving editing of G-5510 audio assets.

This is not a synthesizer or an executed-PC trace. It exports structures whose
loaders are known, preserving all register bits and shared instrument banks.
Only table/header bytes and directly selected instrument records receive
confirmed ownership; next-header-delimited instrument allocation is probable.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import struct
import tempfile
from typing import Any


ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
PROJECT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = PROJECT.parent / "work" / "original_g5510.bin"
SCHEMA_VERSION = 1
FORMAT = "g5510-audio-definitions-and-fm-instruments"
OPERATOR_REGISTER_OFFSETS = (0, 8, 4, 12)
REGISTER_FIELDS = (
    "detune_multiple", "rate_scale_attack", "amplitude_decay",
    "sustain_rate", "sustain_release",
)
REGISTER_MAP = (
    0xB0, 0x30, 0x38, 0x34, 0x3C, 0x50, 0x58, 0x54, 0x5C,
    0x60, 0x68, 0x64, 0x6C, 0x70, 0x78, 0x74, 0x7C,
    0x80, 0x88, 0x84, 0x8C, 0x40, 0x48, 0x44, 0x4C,
)
ANCHORS = (
    ("pointer_index_le", 0x0028, 0x0035, "A*2 indexing and little-endian pointer load"),
    ("instrument_stride", 0x0484, 0x049E, "shared music/SFX base plus instrument index times 25"),
    ("instrument_register_map", 0x04C8, 0x04E1, "25 register bases in serialized record order"),
    ("instrument_loader", 0x04E5, 0x050A, "21 register writes then saved TL parameter pointer"),
    ("music_header_loader", 0x0556, 0x05E3, "6-byte header, 4-byte ordinary and 6-byte PSG descriptors"),
    ("music_channel_defaults", 0x05E3, 0x05F7, "driver slot flags/channel IDs, separate from serialized descriptors"),
    ("sfx_header_loader", 0x0600, 0x0689, "4-byte header and six-byte channel descriptors"),
    ("tempo_reload", 0x0866, 0x087F, "tempo reload periodically delays ten music slots"),
    ("sequence_dispatch", 0x0B78, 0x0B88, "E0-FF handlers and common increment/continuation"),
    ("instrument_selector", 0x0D2D, 0x0D70, "EF instrument index and optional external-music bank selector"),
    ("instrument_tl_writer", 0x0D8A, 0x0DA9, "TL bit7 selects channel attenuation addition, mask 7F before write"),
)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_rom(rom: bytes) -> None:
    if type(rom) is not bytes or len(rom) != ROM_SIZE or _sha(rom) != ROM_SHA256:
        raise ValueError("base ROM is not the canonical G-5510 BIN")
    if tuple(rom[0x69D2 + 0x04C8:0x69D2 + 0x04E1]) != REGISTER_MAP:
        raise ValueError("instrument register-map evidence differs")


def to_rom(space: str, address: int) -> int:
    if type(address) is not int:
        raise ValueError("Z80 address must be an integer")
    if space == "banked" and 0x8000 <= address <= 0xFFFF:
        return 0xF0000 + address
    if space == "local" and 0x1000 <= address < 0x1C00:
        return 0x699C + address
    raise ValueError("address is outside the supported audio mapping")


def _word(rom: bytes, offset: int) -> int:
    return struct.unpack_from("<H", rom, offset)[0]


def _bank_id(space: str, address: int) -> str:
    return f"{space}_instrument_{address:04x}"


def _record(raw: bytes, index: int) -> dict[str, Any]:
    if len(raw) != 25:
        raise ValueError("instrument must contain exactly 25 bytes")
    operators = []
    for column, register_offset in enumerate(OPERATOR_REGISTER_OFFSETS):
        operator = {"register_offset": register_offset}
        for row, name in enumerate(REGISTER_FIELDS):
            operator[name] = raw[1 + 4 * row + column]
        operator["total_level"] = raw[21 + column] & 0x7F
        operator["channel_attenuation_enabled"] = bool(raw[21 + column] & 0x80)
        operators.append(operator)
    return {"index": index, "feedback_algorithm": raw[0], "operators": operators}


def extract(rom: bytes) -> dict[str, Any]:
    """Extract editable values; all addresses/topology are canonical fixed data."""
    verify_rom(rom)
    music_ptrs = list(struct.unpack_from("<31H", rom, 0xF823F))
    sfx_ptrs = list(struct.unpack_from("<16H", rom, to_rom("local", 0x1000)))
    music = []
    sfx = []
    banks: dict[str, dict[str, Any]] = {}
    for index, address in enumerate(music_ptrs):
        start = to_rom("banked", address)
        base, ordinary_count, psg_count, multiplier, tempo = struct.unpack_from("<H4B", rom, start)
        cursor = start + 6
        ordinary = []
        for _ in range(ordinary_count):
            sequence, transpose, attenuation = struct.unpack_from("<H2B", rom, cursor)
            ordinary.append({"sequence_ptr": sequence, "transpose": transpose, "attenuation": attenuation})
            cursor += 4
        psg = []
        for _ in range(psg_count):
            sequence, transpose, attenuation, modulation, envelope = struct.unpack_from("<H4B", rom, cursor)
            psg.append({"sequence_ptr": sequence, "transpose": transpose, "attenuation": attenuation,
                        "modulation_selector": modulation, "envelope_selector": envelope})
            cursor += 6
        bank_id = _bank_id("banked", base)
        music.append({"id": f"music_{index + 0x81:02x}", "command": index + 0x81,
                      "space": "banked", "z80_address": address, "rom_offset": start,
                      "instrument_bank_id": bank_id,
                      "header": {"instrument_base": base, "driver_slot_count": ordinary_count,
                                 "psg_slot_count": psg_count, "duration_multiplier": multiplier,
                                 "tempo_reload": tempo}, "ordinary_slots": ordinary, "psg_slots": psg})
        end = music_ptrs[index + 1] if index < 30 else 0xE31D
        if base >= end or (end - base) % 25:
            raise ValueError("music instrument allocation is not whole records")
        banks[bank_id] = _make_bank(rom, "banked", base, end,
                                  "next_music_definition" if index < 30 else "last_song_direct_EF_00_and_01")
    # A8 deliberately aliases A3's instrument bank. Bound each unique local
    # bank by the first subsequent SFX definition, not by its consumer's ID.
    for index, address in enumerate(sfx_ptrs):
        start = to_rom("local", address)
        base, multiplier, count = struct.unpack_from("<H2B", rom, start)
        cursor = start + 4
        slots = []
        for _ in range(count):
            flags, channel, sequence, transpose, attenuation = struct.unpack_from("<BBHBB", rom, cursor)
            slots.append({"flags": flags, "channel_id": channel, "sequence_ptr": sequence,
                          "transpose": transpose, "attenuation": attenuation})
            cursor += 6
        bank_id = _bank_id("local", base)
        sfx.append({"id": f"sfx_{index + 0xA0:02x}", "command": index + 0xA0,
                    "space": "local", "z80_address": address, "rom_offset": start,
                    "instrument_bank_id": bank_id,
                    "header": {"instrument_base": base, "duration_multiplier": multiplier,
                               "channel_count": count}, "slots": slots})
        if bank_id not in banks:
            end = next((pointer for pointer in sfx_ptrs if pointer > base), 0x16ED)
            if base >= end or (end - base) % 25:
                raise ValueError("SFX instrument allocation is not whole records")
            banks[bank_id] = _make_bank(rom, "local", base, end,
                                      "next_sfx_definition" if end != 0x16ED else "last_sfx_record_before_16ed_gap")
    return {"schema_version": SCHEMA_VERSION, "format": FORMAT,
            "source": {"size": ROM_SIZE, "sha256": ROM_SHA256},
            "music_pointer_table": {"rom_offset": 0xF823F, "z80_address": 0x823F, "pointers": music_ptrs},
            "sfx_pointer_table": {"rom_offset": to_rom("local", 0x1000), "z80_address": 0x1000, "pointers": sfx_ptrs},
            "music": music, "sfx": sfx, "instrument_banks": list(banks.values())}


def _make_bank(rom: bytes, space: str, start: int, end: int, boundary: str) -> dict[str, Any]:
    offset = to_rom(space, start)
    count = (end - start) // 25
    return {"id": _bank_id(space, start), "space": space, "z80_start": start,
            "rom_offset": offset, "record_count": count, "allocation_end_exclusive": end,
            "allocation_evidence": boundary, "allocation_status": "probable",
            "records": [_record(rom[offset + 25 * i:offset + 25 * (i + 1)], i) for i in range(count)]}


def _keys(value: Any, expected: Any, label: str) -> None:
    if type(value) is not dict or set(value) != set(expected):
        raise ValueError(f"{label}: missing or unknown fields")


def _same(value: Any, expected: Any, label: str) -> None:
    if type(value) is not type(expected) or value != expected:
        raise ValueError(f"{label}: immutable canonical topology differs")
    if type(expected) is dict:
        _keys(value, expected, label)
        for key in expected:
            _same(value[key], expected[key], f"{label}.{key}")
    elif type(expected) is list:
        for index, (item, ref) in enumerate(zip(value, expected)):
            _same(item, ref, f"{label}[{index}]")


def _integer(value: Any, maximum: int, label: str) -> int:
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError(f"{label}: expected integer 0..{maximum}")
    return value


def _sequence(value: Any, space: str, label: str) -> int:
    value = _integer(value, 65535, label)
    low, high = (0x827D, 0xE31D) if space == "banked" else (0x1022, 0x16ED)
    if not low <= value < high:
        raise ValueError(f"{label}: pointer leaves supported audio allocation")
    return value


def _list_shape(value: Any, expected: list[Any], label: str) -> None:
    if type(value) is not list or len(value) != len(expected):
        raise ValueError(f"{label}: list length/topology differs")


def _encode_record(value: Any, expected: dict[str, Any], label: str) -> bytes:
    _keys(value, expected, label)
    _same(value["index"], expected["index"], label + ".index")
    raw = bytearray(25)
    raw[0] = _integer(value["feedback_algorithm"], 255, label + ".feedback_algorithm")
    _list_shape(value["operators"], expected["operators"], label + ".operators")
    for col, (operator, ref) in enumerate(zip(value["operators"], expected["operators"])):
        _keys(operator, ref, label + ".operator")
        _same(operator["register_offset"], ref["register_offset"], label + ".operator.register_offset")
        for row, name in enumerate(REGISTER_FIELDS):
            raw[1 + 4 * row + col] = _integer(operator[name], 255, label + "." + name)
        level = _integer(operator["total_level"], 127, label + ".total_level")
        if type(operator["channel_attenuation_enabled"]) is not bool:
            raise ValueError(label + ": channel_attenuation_enabled must be Boolean")
        raw[21 + col] = level | (0x80 if operator["channel_attenuation_enabled"] else 0)
    return bytes(raw)


def encode_edits(rom: bytes, assets: Any) -> list[tuple[int, bytes, str]]:
    """Validate editable fields and return only fixed, canonical owned writes.

    The baseline is canonical; edited asset values are deliberately NOT sealed.
    Counts, bank references, positions, record identities and pointer-table
    topology cannot move. Sequence pointers may change only within supported
    audio data mappings; this does not prove the destination is playable code.
    """
    baseline = extract(rom)
    _keys(assets, baseline, "assets")
    for name in ("schema_version", "format", "source", "music_pointer_table", "sfx_pointer_table"):
        _same(assets[name], baseline[name], name)
    writes = []
    for group in ("music", "sfx"):
        _list_shape(assets[group], baseline[group], group)
        for value, ref in zip(assets[group], baseline[group]):
            label = ref["id"]
            _keys(value, ref, label)
            mutable = {"header", "ordinary_slots", "psg_slots"} if group == "music" else {"header", "slots"}
            for key in set(ref) - mutable:
                _same(value[key], ref[key], label + "." + key)
            header = value["header"]
            _keys(header, ref["header"], label + ".header")
            for key in ref["header"]:
                if key not in {"duration_multiplier", "tempo_reload"}:
                    _same(header[key], ref["header"][key], label + ".header." + key)
            multiplier = _integer(header["duration_multiplier"], 255, label + ".duration_multiplier")
            if group == "music":
                raw = bytearray(struct.pack("<H4B", header["instrument_base"], header["driver_slot_count"],
                                            header["psg_slot_count"], multiplier,
                                            _integer(header["tempo_reload"], 255, label + ".tempo_reload")))
                collections = ("ordinary_slots", "psg_slots")
            else:
                raw = bytearray(struct.pack("<H2B", header["instrument_base"], multiplier, header["channel_count"]))
                collections = ("slots",)
            for collection in collections:
                _list_shape(value[collection], ref[collection], label + "." + collection)
                for slot, ref_slot in zip(value[collection], ref[collection]):
                    _keys(slot, ref_slot, label + ".slot")
                    sequence = _sequence(slot["sequence_ptr"], ref["space"], label + ".sequence_ptr")
                    fields = {k: _integer(v, 255, label + "." + k) for k, v in slot.items() if k != "sequence_ptr"}
                    if collection == "slots":
                        # Flags/channel IDs determine runtime destination and
                        # therefore are topology, not an unrestricted byte edit.
                        _same(fields["flags"], ref_slot["flags"], label + ".flags")
                        _same(fields["channel_id"], ref_slot["channel_id"], label + ".channel_id")
                        raw.extend(struct.pack("<BBHBB", fields["flags"], fields["channel_id"], sequence,
                                               fields["transpose"], fields["attenuation"]))
                    elif collection == "ordinary_slots":
                        raw.extend(struct.pack("<H2B", sequence, fields["transpose"], fields["attenuation"]))
                    else:
                        raw.extend(struct.pack("<H4B", sequence, fields["transpose"], fields["attenuation"],
                                               fields["modulation_selector"], fields["envelope_selector"]))
            writes.append((ref["rom_offset"], bytes(raw), label))
    _list_shape(assets["instrument_banks"], baseline["instrument_banks"], "instrument_banks")
    for value, ref in zip(assets["instrument_banks"], baseline["instrument_banks"]):
        label = ref["id"]
        _keys(value, ref, label)
        for key in set(ref) - {"records"}:
            _same(value[key], ref[key], label + "." + key)
        _list_shape(value["records"], ref["records"], label + ".records")
        for record, ref_record in zip(value["records"], ref["records"]):
            writes.append((ref["rom_offset"] + ref_record["index"] * 25,
                           _encode_record(record, ref_record, label), label + f"[{ref_record['index']}]"))
    # Do not let accidental topology aliasing silently choose the last writer.
    previous_end = 0
    for start, raw, name in sorted(writes):
        if start < previous_end or start + len(raw) > len(rom):
            raise ValueError("overlapping or out-of-ROM typed asset: " + name)
        previous_end = start + len(raw)
    return writes


def rebuild(rom: bytes, assets: Any) -> bytes:
    result = bytearray(rom)
    for start, raw, _ in encode_edits(rom, assets):
        result[start:start + len(raw)] = raw
    return bytes(result)


def selected_record_witnesses(rom: bytes, assets: dict[str, Any]) -> list[dict[str, Any]]:
    """Narrow static proofs: walk command-only prefixes from header entries.

    Stop at first note/duration, control transfer, FF, stop or unsupported
    command. No scanning for EF-looking bytes within arbitrary sequence data.
    Both ordinary FM and local FM SFX are eligible; PSG selectors do not read
    FM records. The special music first slot is excluded.
    """
    widths = {0xE0: 1, 0xE1: 1, 0xE2: 1, 0xE4: 5, 0xE5: 2, 0xE6: 1, 0xE7: 0,
              0xE8: 1, 0xE9: 2, 0xEA: 3, 0xEB: 3, 0xEC: 1, 0xED: 2, 0xEE: 2,
              0xF0: 4, 0xF1: 2, 0xF3: 1, 0xF4: 1, 0xF5: 1,
              0xFA: 1, 0xFB: 1, 0xFC: 1, 0xFD: 1, 0xFE: 4}
    banks = {bank["id"]: bank for bank in assets["instrument_banks"]}
    music = {song["command"]: song for song in assets["music"]}
    witnesses = []
    for group in ("music", "sfx"):
        for definition in assets[group]:
            slots = definition["ordinary_slots"][1:] if group == "music" else definition["slots"]
            for slot_index, slot in enumerate(slots, 1 if group == "music" else 0):
                if group == "sfx" and slot["channel_id"] & 0x80:
                    continue
                cursor = slot["sequence_ptr"]
                entry = cursor
                # Avoid parsing through an allocated instrument bank or header;
                # a later first note is not a reason to claim whole sequences.
                upper = definition["header"]["instrument_base"]
                if upper <= cursor:  # shared or intentionally nonlocal stream
                    upper = 0x16ED if definition["space"] == "local" else 0xE31D
                for _ in range(128):
                    if not cursor < upper:
                        break
                    offset = to_rom(definition["space"], cursor)
                    opcode = rom[offset]
                    if opcode == 0xEF:
                        if cursor + 2 > upper:
                            break
                        selector = rom[offset + 1]
                        length = 2 + bool(selector & 0x80)
                        if cursor + length > upper:
                            break
                        target = definition
                        if selector & 0x80:
                            target = music.get(rom[offset + 2])
                            if target is None:
                                break
                        bank = banks[target["instrument_bank_id"]]
                        index = selector & 0x7F
                        if index >= bank["record_count"]:
                            break
                        witnesses.append({"definition_id": definition["id"], "slot_index": slot_index,
                                          "entry_z80": entry, "selector_z80": cursor,
                                          "selector_rom": offset, "bytes": rom[offset:offset + length].hex(),
                                          "bank_id": bank["id"], "record_index": index,
                                          "status": "confirmed", "evidence": "header-seeded command-only prefix; EF consumer 0D2D-0D69"})
                        cursor += length
                    elif opcode in widths and cursor + 1 + widths[opcode] <= upper:
                        cursor += 1 + widths[opcode]
                    else:
                        break
    return witnesses


def build_map(rom: bytes, assets: dict[str, Any]) -> dict[str, Any]:
    if rebuild(rom, assets) != rom:
        raise ValueError("proof map is generated only from canonical extracted values")
    witnesses = selected_record_witnesses(rom, assets)
    selected = {(w["bank_id"], w["record_index"]) for w in witnesses}
    intervals = []
    def own(name: str, start: int, end: int, role: str, evidence: str) -> None:
        intervals.append({"id": name, "rom_start": start, "rom_end_exclusive": end,
                          "length": end - start, "role": role, "status": "confirmed",
                          "ownership": "primary", "evidence": evidence,
                          "sha256": _sha(rom[start:end])})
    own("music_pointer_table", 0xF823F, 0xF827D, "u16le_music_definition_pointers", "055E-0561,31 canonical definitions")
    own("sfx_pointer_table", to_rom("local", 0x1000), to_rom("local", 0x1020),
        "u16le_sfx_definition_pointers", "0600-060B,A0-AF dispatch range")
    for start, raw, name in encode_edits(rom, assets):
        if name.startswith("music_") or name.startswith("sfx_"):
            own(name, start, start + len(raw), "typed_audio_definition",
                "0556-05E2" if name.startswith("music_") else "0600-0686")
    allocations = []
    for bank in assets["instrument_banks"]:
        chosen = [i for i in range(bank["record_count"]) if (bank["id"], i) in selected]
        allocations.append({key: value for key, value in bank.items() if key != "records"} |
                           {"selected_record_indices": chosen,
                            "unselected_record_indices": [i for i in range(bank["record_count"]) if i not in chosen]})
        for index in chosen:
            start = bank["rom_offset"] + 25 * index
            own(f"{bank['id']}_record_{index}", start, start + 25,
                "typed_fm_instrument_25", "header-seeded EF selection + 0493 stride + 04E5/0D8A consumers")
    intervals.sort(key=lambda item: item["rom_start"])
    for left, right in zip(intervals, intervals[1:]):
        if left["rom_end_exclusive"] > right["rom_start"]:
            raise ValueError("confirmed ownership intervals overlap")
    anchors = [{"id": name, "space": "z80_driver", "z80_start": start,
                "z80_end_exclusive": end, "rom_start": 0x69D2 + start,
                "rom_end_exclusive": 0x69D2 + end, "bytes": rom[0x69D2 + start:0x69D2 + end].hex(),
                "status": "confirmed", "ownership": "observation_only", "evidence": description}
               for name, start, end, description in ANCHORS]
    owners = [{"id": row["id"], "start": row["rom_start"], "end": row["rom_end_exclusive"],
               "kind": row["role"], "confidence": row["status"], "semantic": row["role"],
               "evidence": row["evidence"], "sha256": row["sha256"]} for row in intervals]
    return {"schema_version": 1, "package": "audio_formats", "source": assets["source"],
            "canonical_source": assets["source"], "owners": owners,
            "scope": "Canonical static typed headers and FM records; no executed-PC or playback claim",
            "summary": {"music_definitions": len(assets["music"]), "sfx_definitions": len(assets["sfx"]),
                        "unique_instrument_banks": len(assets["instrument_banks"]),
                        "allocated_instrument_records": sum(b["record_count"] for b in assets["instrument_banks"]),
                        "selected_instrument_records": len(selected), "selection_witnesses": len(witnesses),
                        "confirmed_owned_bytes": sum(row["length"] for row in intervals),
                        "confirmed_ownership_intervals": len(intervals),
                        "typed_serialized_bytes": sum(len(raw) for _, raw, _ in encode_edits(rom, assets)) + 94},
            "consumer_anchors": anchors, "register_map": list(REGISTER_MAP),
            "operator_register_offsets": list(OPERATOR_REGISTER_OFFSETS),
            "instrument_allocations": allocations, "selected_record_witnesses": witnesses,
            "confirmed_ownership_intervals": intervals,
            "unknowns": [
                "Most sequence instructions, branches/calls, song durations and actual playback remain unparsed.",
                "Unselected allocated 25-byte records are typed probable allocation, not confirmed ownership.",
                "Counts based on next definition cannot prove every allocated instrument is ever selected.",
                "Canonical music92 PSG envelope selector15 is preserved; envelope table lifetime/access is not closed.",
                "Root slot08/800E is pitch modulation, not FM instruments; slot0A/815D is attenuation envelopes.",
                "Attenuation envelope11 ends F0 80, yielding cursor128 outside its own allocation; no closed envelope proof.",
                "SFX A8 shares A3 instrument116A; local16ED gap and all sequence/padding bytes are untouched.",
                "Edits preserve fixed layout but neither validate musical intent nor promise playability.",
            ]}


def asset_schema() -> dict[str, Any]:
    """Machine-readable structural schema; canonical topology is also checked."""
    u8 = {"type": "integer", "minimum": 0, "maximum": 255}
    u16 = {"type": "integer", "minimum": 0, "maximum": 65535}
    def obj(properties: dict[str, Any]) -> dict[str, Any]:
        return {"type": "object", "additionalProperties": False, "required": list(properties), "properties": properties}
    def arr(items: dict[str, Any], count: int | None = None) -> dict[str, Any]:
        result = {"type": "array", "items": items}
        if count is not None:
            result.update(minItems=count, maxItems=count)
        return result
    text = {"type": "string"}
    nonnegative = {"type": "integer", "minimum": 0}
    operator = obj({"register_offset": {"enum": list(OPERATOR_REGISTER_OFFSETS)}, **{key: u8 for key in REGISTER_FIELDS},
                    "total_level": {"type": "integer", "minimum": 0, "maximum": 127},
                    "channel_attenuation_enabled": {"type": "boolean"}})
    record = obj({"index": nonnegative, "feedback_algorithm": u8, "operators": arr(operator, 4)})
    ordinary = {"sequence_ptr": u16, "transpose": u8, "attenuation": u8}
    common = {"id": text, "command": u8, "space": text, "z80_address": u16,
              "rom_offset": nonnegative, "instrument_bank_id": text}
    music = obj(common | {"header": obj({"instrument_base": u16, "driver_slot_count": u8,
                                         "psg_slot_count": u8, "duration_multiplier": u8, "tempo_reload": u8}),
                          "ordinary_slots": arr(obj(ordinary)),
                          "psg_slots": arr(obj(ordinary | {"modulation_selector": u8, "envelope_selector": u8}))})
    sfx = obj(common | {"header": obj({"instrument_base": u16, "duration_multiplier": u8, "channel_count": u8}),
                        "slots": arr(obj({"flags": u8, "channel_id": u8} | ordinary))})
    bank = obj({"id": text, "space": text, "z80_start": u16, "rom_offset": nonnegative,
                "record_count": nonnegative, "allocation_end_exclusive": u16,
                "allocation_evidence": text, "allocation_status": {"const": "probable"}, "records": arr(record)})
    pointer = lambda n: obj({"rom_offset": nonnegative, "z80_address": u16, "pointers": arr(u16, n)})
    schema = obj({"schema_version": {"const": SCHEMA_VERSION}, "format": {"const": FORMAT},
                  "source": obj({"size": {"const": ROM_SIZE}, "sha256": {"const": ROM_SHA256}}),
                  "music_pointer_table": pointer(31), "sfx_pointer_table": pointer(16),
                  "music": arr(music, 31), "sfx": arr(sfx, 16), "instrument_banks": arr(bank, 46)})
    schema.update({"$schema": "https://json-schema.org/draft/2020-12/schema",
                   "title": "G-5510 editable audio assets",
                   "description": "Structural schema only; importer additionally checks immutable canonical topology, exact types, pointer mappings and nonoverlapping writes."})
    return schema


def _json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def render_report(mapping: dict[str, Any]) -> bytes:
    s = mapping["summary"]
    lines = ["# G-5510 类型化音频定义与 FM 乐器", "",
             "证据为原版 ROM 机器指令和静态数据；本包没有新增 executed-PC trace 或播放验证。", "",
             f"- 音乐定义：{s['music_definitions']}；本地 SFX 定义：{s['sfx_definitions']}。",
             f"- 唯一乐器 bank：{s['unique_instrument_banks']}；结构分配记录：{s['allocated_instrument_records']}。",
             f"- 从描述符入口命令前缀证明被选用的记录：{s['selected_instrument_records']}，证据 {s['selection_witnesses']} 条。",
             f"- 本包已确认拥有 {s['confirmed_owned_bytes']} 字节，{s['confirmed_ownership_intervals']} 个互不重叠区间。",
             f"- 可类型化回装 {s['typed_serialized_bytes']} 字节（含只读指针表）；其中 probable 分配不计入 confirmed。", "",
             "## 字段布局", "",
             "音乐头：instrument_base:u16le、driver_slot_count:u8、psg_slot_count:u8、duration_multiplier:u8、tempo_reload:u8。",
             "普通槽每项4字节：sequence_ptr:u16le、transpose:u8、attenuation:u8。",
             "PSG槽每项6字节：上述字段加 modulation_selector:u8、envelope_selector:u8。",
             "SFX头：instrument_base:u16le、duration_multiplier:u8、channel_count:u8。",
             "SFX槽每项6字节：flags:u8、channel_id:u8、sequence_ptr:u16le、transpose:u8、attenuation:u8。", "",
             "音乐第一槽走特殊节奏更新，driver_slot_count 不等于物理 FM 通道数量。tempo_reload 是倒计时延迟机制而不是 BPM。", "",
             "FM记录固定25字节，寄存器顺序：`" + " ".join(f"{v:02X}" for v in REGISTER_MAP) + "`。",
             "operator register_offset 序列为 0、8、4、12（不假定 YM 逻辑算子编号）；前21字节完整保留，最后4字节拆成7位 total_level 和 channel_attenuation_enabled 布尔标志。",
             "驱动对带标志的 TL 先加通道衰减，最后 AND 7F 后写 YM；所有未解释/保留寄存器位仍完整保留。", "",
             "## 编辑与证据分离", "",
             "assets.json 是可编辑资产；manifest.json 是原版证据。import 不要求资产整体哈希匹配。",
             "地址、记录数量、共享 bank 身份、通道 IDs 与指针表保持原版拓扑；字段值可修改。",
             "允许原版中的高值/保留位，不冒充音效质量验证。不会重新计算 Mega Drive ROM checksum：输出仅改变明确编辑的字节。", "",
             "## 未决边界", ""]
    lines += ["- " + item for item in mapping["unknowns"]]
    lines += ["", "## 机器指令锚点", "", "| ID | Z80范围（末端不含） | 线性ROM范围（末端不含） |", "|---|---|---|"]
    for anchor in mapping["consumer_anchors"]:
        lines.append(f"| {anchor['id']} | {anchor['z80_start']:04X}–{anchor['z80_end_exclusive']:04X} | {anchor['rom_start']:06X}–{anchor['rom_end_exclusive']:06X} |")
    return ("\n".join(lines) + "\n").encode("utf-8")


def render_bundle(rom: bytes) -> dict[str, bytes]:
    assets = extract(rom)
    mapping = build_map(rom, assets)
    stream = io.StringIO(newline="")
    fields = ("id", "rom_start", "rom_end_exclusive", "length", "role", "status", "ownership", "evidence", "sha256")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(mapping["confirmed_ownership_intervals"])
    return {"assets.json": _json(assets), "assets.schema.json": _json(asset_schema()),
            "manifest.json": _json(mapping), "ownership.csv": stream.getvalue().encode("utf-8"),
            "README.md": render_report(mapping)}


def safe_path(value: str | Path, *, regular_input: bool = False) -> Path:
    raw = Path(value)
    if ".." in raw.parts:
        raise ValueError("parent traversal is not accepted")
    absolute = raw.absolute()
    for component in reversed((absolute, *absolute.parents)):
        try:
            info = component.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("symlink/reparse path component rejected")
    if regular_input and (not absolute.is_file() or not stat.S_ISREG(absolute.stat().st_mode)):
        raise ValueError("input must be an existing regular file")
    return absolute.resolve()


def _separate(output: Path, inputs: list[Path]) -> None:
    for source in inputs:
        if output == source or output in source.parents or source in output.parents:
            raise ValueError("output overlaps an input path")


def _read(path: Path, maximum: int) -> bytes:
    safe_path(path, regular_input=True)
    if path.stat().st_size > maximum:
        raise ValueError("input exceeds size limit")
    with path.open("rb") as stream:
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        raise ValueError("input exceeds size limit")
    return data


def load_assets(data: bytes) -> Any:
    if type(data) is not bytes or len(data) > 8 * 1024 * 1024:
        raise ValueError("asset JSON exceeds size/type limit")
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result
    def bad_constant(value: str) -> None:
        raise ValueError("non-finite JSON constant: " + value)
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError("invalid asset JSON") from error


def _cleanup_stage(staging: Path, expected: dict[str, bytes], identity: os.stat_result) -> None:
    """Remove only the unchanged files this invocation successfully produced."""
    if not staging.exists():
        return
    safe_path(staging)
    current = staging.stat()
    if (current.st_dev, current.st_ino) != (identity.st_dev, identity.st_ino):
        raise ValueError("temporary directory identity changed; refusing cleanup")
    children = list(staging.iterdir())
    if {child.name for child in children} != set(expected):
        raise ValueError("unexpected temporary contents; refusing cleanup")
    for child in children:
        safe_path(child, regular_input=True)
        if _read(child, len(expected[child.name])) != expected[child.name]:
            raise ValueError("modified temporary output; refusing cleanup")
    for child in children:
        child.unlink()
    staging.rmdir()


def export_files(rom_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    source = safe_path(rom_path, regular_input=True)
    target = safe_path(output_dir)
    _separate(target, [source])
    if target.exists():
        raise ValueError("output directory must be fresh")
    if not target.parent.is_dir():
        raise ValueError("output parent must already exist")
    rom = _read(source, ROM_SIZE)
    bundle = render_bundle(rom)
    staging = Path(tempfile.mkdtemp(prefix=".audio-formats-", dir=target.parent))
    identity = staging.stat()
    produced: dict[str, bytes] = {}
    try:
        for name, data in bundle.items():
            with (staging / name).open("xb") as stream:
                stream.write(data)
            produced[name] = data
        safe_path(output_dir)
        if target.exists():
            raise ValueError("output appeared during generation")
        os.rename(staging, target)
    finally:
        _cleanup_stage(staging, produced, identity)
    return {"output": str(target), "files": sorted(bundle), "roundtrip_exact": True}


def import_files(rom_path: str | Path, asset_path: str | Path, output_file: str | Path) -> dict[str, Any]:
    source = safe_path(rom_path, regular_input=True)
    asset = safe_path(asset_path, regular_input=True)
    target = safe_path(output_file)
    _separate(target, [source, asset])
    if target.exists():
        raise ValueError("output file must be fresh")
    if not target.parent.is_dir():
        raise ValueError("output parent must already exist")
    rom = _read(source, ROM_SIZE)
    rebuilt = rebuild(rom, load_assets(_read(asset, 8 * 1024 * 1024)))
    descriptor, tempname = tempfile.mkstemp(prefix=".audio-formats-", dir=target.parent)
    temporary = Path(tempname)
    complete = False
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(rebuilt)
            stream.flush()
            os.fsync(stream.fileno())
        complete = True
        safe_path(output_file)
        # Hard-link publication is atomic and never replaces an existing path.
        os.link(temporary, target)
    finally:
        if temporary.exists():
            safe_path(temporary, regular_input=True)
            if complete and _read(temporary, len(rebuilt)) == rebuilt:
                temporary.unlink()
            else:
                raise ValueError("incomplete or modified temporary output retained for inspection")
    return {"output": str(target), "sha256": _sha(rebuilt),
            "changed_bytes": sum(a != b for a, b in zip(rom, rebuilt)),
            "canonical_roundtrip": rebuilt == rom}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    export = subparsers.add_parser("export", help="create a fresh canonical typed asset bundle")
    export.add_argument("--rom", type=Path, default=DEFAULT_ROM)
    export.add_argument("--output", type=Path, required=True)
    pack = subparsers.add_parser("import", help="write a fresh BIN from canonical base and editable asset JSON")
    pack.add_argument("--rom", type=Path, default=DEFAULT_ROM)
    pack.add_argument("--assets", type=Path, required=True)
    pack.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = export_files(args.rom, args.output) if args.command == "export" else import_files(args.rom, args.assets, args.output)
    except (ValueError, OSError) as error:
        parser.exit(2, f"audio_formats: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
