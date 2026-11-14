#!/usr/bin/env python3
"""Editable envelope tokens and explicit bounded interpretations of Z80 consumers.

Allocation boundaries are not execution boundaries: this package preserves all
allocated bytes, but only pointer-seeded consumed byte extents receive ownership.
No sound synthesis, natural playback, selector lifetime or global ROM closure is
claimed. The pure interpreter accepts an explicit mapped memory window.
"""

from __future__ import annotations

import argparse
import csv
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
from tools.audio_formats import audio_formats as af

ROM_SIZE, ROM_SHA256 = af.ROM_SIZE, af.ROM_SHA256
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
DEFAULT_OUTPUT = ROOT / "analysis/audio_envelopes/generated"
FAMILIES = {
    "pitch": {"table": 0x800E, "end": 0x815D,
              "starts": (0x8022, 0x8038, 0x8044, 0x8050, 0x8092, 0x80C7, 0x8104, 0x811E, 0x8138, 0x8149)},
    "attenuation": {"table": 0x815D, "end": 0x8200,
                    "starts": (0x8173, 0x8175, 0x817C, 0x8195, 0x81A1, 0x81AC, 0x81BB, 0x81C4,
                               0x81D5, 0x81E1, 0x81F6)},
}
ANCHORS = (
    ("root_pointer_lookup", 0x0020, 0x0035, "root+C lookup followed by zero-extended A*2 LE16 pointer selection"),
    ("pitch_consumer", 0x03B7, 0x040B, "root08 pitch selector, cursor+25, scale+22, signed delta and control grammar"),
    ("indexed_byte_read", 0x047D, 0x0484, "zero-extended cursor adds to base modulo65536, BC holds read address"),
    ("fm_attenuation_entry", 0x030C, 0x031A, "positive selector-1 via root0A and shared attenuation reader"),
    ("psg_attenuation_entry", 0x0F43, 0x0F54, "nonzero selector-1 via root0A and shared attenuation reader"),
    ("attenuation_consumer", 0x0F78, 0x0FAC, "cursor+17, literal values and high-bit redirect/hold/keyoff grammar"),
    ("conditional_psg_keyoff", 0x0FAC, 0x0FCA, "flag4 set; flag2 suppresses write; sign-gated PSG7F11 keyoff byte(s)"),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def integer(value: Any, low: int, high: int, label: str) -> int:
    require(type(value) is int and low <= value <= high, f"{label}: integer {low}..{high} required")
    return value


def keys(value: Any, expected: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == expected, f"{label}: wrong object shape")


def family(kind: Any) -> dict[str, Any]:
    require(type(kind) is str and kind in FAMILIES, "unknown envelope family")
    return FAMILIES[kind]


def rom_offset(address: int) -> int:
    return 0xF0000 + integer(address, 0x8000, 0xFFFF, "banked Z80 address")


def verify_rom(rom: bytes) -> None:
    af.verify_rom(rom)
    require(rom[0xF8008:0xF800C] == bytes.fromhex("0e805d81"), "root08/root0A envelope directory identity")
    for kind, info in FAMILIES.items():
        actual = struct.unpack_from(f"<{len(info['starts'])}H", rom, rom_offset(info["table"]))
        require(actual == info["starts"], f"{kind}: pointer evidence changed")
        require(info["table"] + 2 * len(actual) == actual[0], "directory does not end at first allocation")


def token_width(kind: str, opcode: int) -> int:
    family(kind)
    integer(opcode, 0, 255, "opcode")
    return 2 if (opcode in (0x82, 0x84) if kind == "pitch" else opcode >= 128 and opcode not in (0x80, 0x81, 0x83)) else 1


def decode_token(kind: str, raw: bytes) -> dict[str, Any]:
    require(type(raw) is bytes and len(raw) >= 1, "token bytes missing")
    opcode = raw[0]
    require(len(raw) == token_width(kind, opcode), "token size differs from consumer width")
    if opcode < 128:
        return {"kind": "delta" if kind == "pitch" else "value", "value": opcode}
    if opcode == 0x80:
        return {"kind": "reset"}
    if opcode == 0x81:
        return {"kind": "hold_81"}
    if opcode == 0x83:
        return {"kind": "hold_83" if kind == "pitch" else "keyoff_83"}
    if kind == "pitch":
        if opcode == 0x82:
            return {"kind": "jump", "cursor": raw[1]}
        if opcode == 0x84:
            return {"kind": "add_scale", "increment": raw[1]}
        return {"kind": "delta", "value": opcode - 256}
    return {"kind": "redirect", "opcode": opcode, "cursor": raw[1]}


def encode_token(kind: str, token: Any) -> bytes:
    family(kind)
    require(type(token) is dict and type(token.get("kind")) is str, "typed token kind required")
    name = token["kind"]
    singles = {"reset": 0x80, "hold_81": 0x81,
               "hold_83" if kind == "pitch" else "keyoff_83": 0x83}
    if name in singles:
        keys(token, {"kind"}, "single-byte control")
        return bytes([singles[name]])
    if name == ("delta" if kind == "pitch" else "value"):
        keys(token, {"kind", "value"}, "value token")
        value = integer(token["value"], -123 if kind == "pitch" else 0, 127, "value")
        return bytes([value & 255])
    if kind == "pitch" and name in ("jump", "add_scale"):
        field, opcode = ("cursor", 0x82) if name == "jump" else ("increment", 0x84)
        keys(token, {"kind", field}, "pitch control")
        return bytes([opcode, integer(token[field], 0, 255, field)])
    if kind == "attenuation" and name == "redirect":
        keys(token, {"kind", "opcode", "cursor"}, "attenuation redirect")
        opcode = integer(token["opcode"], 128, 255, "redirect opcode")
        require(opcode not in (0x80, 0x81, 0x83), "special control cannot encode as redirect")
        return bytes([opcode, integer(token["cursor"], 0, 255, "cursor")])
    raise ValueError("token kind does not belong to this envelope family")


def decode_allocation(kind: str, raw: bytes) -> list[dict[str, Any]]:
    """Linear token grammar, NOT a claim that every token is reached from cursor0."""
    family(kind)
    require(type(raw) is bytes and len(raw) > 0, "allocation bytes missing")
    result, cursor = [], 0
    while cursor < len(raw):
        width = token_width(kind, raw[cursor])
        result.append(decode_token(kind, raw[cursor:cursor + width]))
        cursor += width
    return result


def extract(rom: bytes) -> dict[str, Any]:
    verify_rom(rom)
    tables = []
    for kind, info in FAMILIES.items():
        starts = info["starts"]
        allocations = [{"z80_start": start, "tokens": decode_allocation(kind, rom[rom_offset(start):rom_offset(end)])}
                       for start, end in zip(starts, starts[1:] + (info["end"],))]
        tables.append({"family": kind, "z80_pointer_start": info["table"], "z80_allocation_end": info["end"],
                       "pointers": list(starts), "allocations": allocations})
    return {"format": "g5510-audio-envelopes-v1", "canonical_rom_sha256": ROM_SHA256, "tables": tables}


def encode_edits(rom: bytes, assets: Any) -> list[tuple[int, bytes]]:
    verify_rom(rom)
    keys(assets, {"format", "canonical_rom_sha256", "tables"}, "assets")
    require(assets["format"] == "g5510-audio-envelopes-v1" and assets["canonical_rom_sha256"] == ROM_SHA256,
            "wrong editable asset format/base identity")
    require(type(assets["tables"]) is list and len(assets["tables"]) == 2, "two envelope families required")
    edits = []
    for table, (kind, info) in zip(assets["tables"], FAMILIES.items()):
        keys(table, {"family", "z80_pointer_start", "z80_allocation_end", "pointers", "allocations"}, "family")
        require(table["family"] == kind, "family order changed")
        for field, expected in (("z80_pointer_start", info["table"]), ("z80_allocation_end", info["end"])):
            require(type(table[field]) is int and table[field] == expected, "fixed envelope region moved")
        starts = info["starts"]
        pointers = table["pointers"]
        require(type(pointers) is list and len(pointers) == len(starts), "pointer count/type changed")
        require(all(type(pointer) is int and pointer in starts for pointer in pointers),
                "pointer alias must address an existing allocation in this family")
        edits.append((rom_offset(info["table"]), struct.pack(f"<{len(starts)}H", *pointers)))
        allocations = table["allocations"]
        require(type(allocations) is list and len(allocations) == len(starts), "allocation count/type changed")
        for allocation, start, end in zip(allocations, starts, starts[1:] + (info["end"],)):
            keys(allocation, {"z80_start", "tokens"}, "allocation")
            require(type(allocation["z80_start"]) is int and allocation["z80_start"] == start,
                    "allocation reordered or relocated")
            require(type(allocation["tokens"]) is list and allocation["tokens"], "token list is empty/nonlist")
            encoded = b"".join(encode_token(kind, token) for token in allocation["tokens"])
            require(len(encoded) == end - start, "fixed allocation capacity changed")
            edits.append((rom_offset(start), encoded))
    return edits


def rebuild(rom: bytes, assets: Any) -> bytes:
    output = bytearray(rom)
    for start, raw in encode_edits(rom, assets):
        output[start:start + len(raw)] = raw
    return bytes(output)


def evaluate_tick(memory: bytes, *, memory_start: int, family_name: str, base: int, cursor: int = 0,
                  scale: int = 0, frequency: int = 0, flags: int = 0, channel_id: int = 0,
                  max_steps: int = 1024) -> dict[str, Any]:
    """Execute one envelope-reader invocation over explicitly mapped Z80 bytes.

    Memory boundaries are observer limits, not invented driver terminators.
    Cursor wraps at eight bits; base+cursor and operand-address additions wrap
    at16 bits. Control loops terminate analysis with an explicit outcome.
    Pitch sample output is based on this invocation's frequency input, not an
    assumption of frequency accumulation between independent driver frames.
    """
    kind = family_name
    family(kind)
    require(type(memory) is bytes and 0 < len(memory) <= 65536, "mapped memory must be bytes, length1..65536")
    integer(memory_start, 0, 65535, "memory_start")
    require(memory_start + len(memory) <= 65536, "mapped window crosses address-space end")
    integer(base, 0, 65535, "base")
    integer(cursor, 0, 255, "cursor")
    integer(scale, 0, 255, "scale")
    integer(frequency, 0, 65535, "frequency")
    integer(flags, 0, 255, "flags")
    integer(channel_id, 0, 255, "channel_id")
    integer(max_steps, 1, 65536, "max_steps")
    reads: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    outcome, value, steps, missing = "step_limit", None, 0, None
    keyoff_writes: list[int] = []
    return_mode = "not_returned"

    def read(address: int, role: str) -> int | None:
        nonlocal missing
        if not memory_start <= address < memory_start + len(memory):
            missing = address
            return None
        result = memory[address - memory_start]
        reads.append({"address": address, "role": role, "value": result})
        return result

    for _ in range(max_steps):
        if (cursor, scale) in seen:
            outcome = "control_cycle"
            break
        seen.add((cursor, scale))
        steps += 1
        address = (base + cursor) & 65535
        opcode = read(address, "opcode")
        if opcode is None:
            outcome = "memory_unmapped"
            break
        if opcode < 128 or (kind == "pitch" and opcode >= 0x85):
            value = opcode if opcode < 128 else opcode - 256
            if kind == "pitch":
                frequency = (frequency + value * (scale + 1)) & 65535
            cursor = (cursor + 1) & 255
            outcome, return_mode = "sample", "normal"
            break
        if opcode == 0x80:
            cursor = 0
            continue
        if opcode in (0x81, 0x83):
            flags |= 64 if kind == "pitch" else 16
            outcome = "key_off" if kind == "attenuation" and opcode == 0x83 else "hold"
            return_mode = "unwind_one_return"
            if outcome == "key_off" and not flags & 4:
                candidate = (0x1F + channel_id) & 255
                if candidate & 128:
                    keyoff_writes.append(candidate)
                    if flags & 1:
                        keyoff_writes.append(255)
            break
        operand = read((address + 1) & 65535, "operand")
        if operand is None:
            outcome = "memory_unmapped"
            break
        if kind == "pitch" and opcode == 0x84:
            scale = (scale + operand) & 255
            cursor = (cursor + 2) & 255
        else:
            cursor = operand
    return {"outcome": outcome, "return_mode": return_mode, "cursor": cursor, "scale": scale,
            "frequency": frequency, "flags": flags, "value": value, "steps": steps, "reads": reads,
            "missing_address": missing, "psg_7f11_writes": keyoff_writes}


def allocation_path(rom: bytes, kind: str, start: int, end: int) -> dict[str, Any]:
    """Audit cursor0 read coverage, stopping honestly at allocation-window limits.

    Cursor projection suffices for byte-role coverage: scale changes pitch
    magnitude, never instruction selection. A repeated cursor is NOT proof that
    the full frequency/scale state or audible output repeats.
    """
    memory = rom[rom_offset(start):rom_offset(end)]
    cursor, scale, flags, ticks, samples = 0, 0, 0, 0, 0
    seen_cursors: set[int] = set()
    visited: set[int] = set()
    last: dict[str, Any] = {}
    while cursor not in seen_cursors:
        seen_cursors.add(cursor)
        ticks += 1
        last = evaluate_tick(memory, memory_start=start, family_name=kind, base=start,
                             cursor=cursor, scale=scale, flags=flags)
        visited.update(row["address"] for row in last["reads"])
        cursor, scale, flags = last["cursor"], last["scale"], last["flags"]
        if last["outcome"] != "sample":
            break
        samples += 1
    outcome = "cursor_projection_cycle" if last["outcome"] == "sample" else last["outcome"]
    return {"start": start, "end": end, "initial_cursor": 0, "initial_scale": 0, "outcome": outcome,
            "reader_invocations": ticks, "sample_returns": samples, "final_cursor": cursor, "final_scale": scale,
            "missing_address": last["missing_address"], "consumed_addresses": sorted(visited),
            "unconsumed_addresses": sorted(set(range(start, end)) - visited),
            "cursor_graph_closed_within_allocation": outcome in ("hold", "key_off", "control_cycle", "cursor_projection_cycle"),
            "full_audio_state_period_proved": False}


def spans(addresses: list[int]) -> list[tuple[int, int]]:
    result = []
    for address in sorted(set(addresses)):
        if result and result[-1][1] == address:
            result[-1] = (result[-1][0], address + 1)
        else:
            result.append((address, address + 1))
    return result


def build_manifest(rom: bytes) -> dict[str, Any]:
    assets = extract(rom)
    require(rebuild(rom, assets) == rom, "canonical typed envelope roundtrip failed")
    owners, paths, probable = [], [], []
    for table in assets["tables"]:
        kind, info = table["family"], FAMILIES[table["family"]]
        owners.append({"id": f"{kind}_pointer_directory", "start": rom_offset(info["table"]),
                       "end": rom_offset(info["starts"][0]), "kind": "u16le_envelope_pointers",
                       "evidence": "root08/0A plus0028 LE16 pointer indexing; last entry ends at minimum payload pointer"})
        for index, (start, end) in enumerate(zip(info["starts"], info["starts"][1:] + (info["end"],))):
            path = allocation_path(rom, kind, start, end)
            path.update({"family": kind, "selector": index + 1, "allocation_evidence": "probable adjacent-pointer extent",
                         "path_evidence": "confirmed static consumer with cursor0 and mapped allocation window"})
            paths.append(path)
            for part, (left, right) in enumerate(spans(path["consumed_addresses"])):
                owners.append({"id": f"{kind}_{index + 1:02d}_consumed_{part}", "start": rom_offset(left),
                               "end": rom_offset(right), "kind": f"typed_{kind}_envelope_tokens",
                               "evidence": f"{kind} actual consumer cursor0 path reads; token-field roundtrip; no natural playback claim"})
            for left, right in spans(path["unconsumed_addresses"]):
                probable.append({"family": kind, "start": rom_offset(left), "end": rom_offset(right),
                                 "confidence": "probable", "reason": "typed allocation bytes not read from cursor0; no primary ownership"})
    for owner in owners:
        owner.update({"confidence": "confirmed", "primary_ownership": True,
                      "byte_count": owner["end"] - owner["start"],
                      "sha256": hashlib.sha256(rom[owner["start"]:owner["end"]]).hexdigest()})
    anchors = [{"id": name, "z80_start": start, "z80_end": end, "rom_start": 0x69D2 + start,
                "rom_end": 0x69D2 + end, "role": role, "confidence": "confirmed", "primary_ownership": False,
                "sha256": hashlib.sha256(rom[0x69D2 + start:0x69D2 + end]).hexdigest()}
               for name, start, end, role in ANCHORS]
    return {"format": "g5510-audio-envelope-analysis-v1", "rom_sha256": ROM_SHA256,
            "summary": {"pitch_pointers": 10, "attenuation_pointers": 11, "typed_allocations": 21,
                        "editable_bytes": 498, "confirmed_owned_bytes": sum(item["byte_count"] for item in owners),
                        "typed_unconsumed_bytes": sum(item["end"] - item["start"] for item in probable),
                        "cross_allocation_paths": sum(item["outcome"] == "memory_unmapped" for item in paths),
                        "runtime_observations": 0, "global_selector_domain_proved": False,
                        "complete_playback_proved": False, "canonical_roundtrip": True},
            "owners": owners, "probable_allocations": probable, "anchors": anchors, "paths": paths,
            "unknowns": ["Pointer allocation shape does not prove natural selector range or song use.",
                         "First pitch allocation bytes8034..8038 follow a hold and are not cursor0-owned.",
                         "Last attenuation F080 redirects to cursor128, requesting8276 outside its allocation.",
                         "Cross-allocation reads require explicitly mapped external bytes; they are not inferred silence or termination.",
                         "Repeated cursor projection proves read-role coverage, not full state/audio periodicity.",
                         "No emulator differential playback, musical interpretation or overall sound-engine closure."]}


def validate_manifest(value: Any, rom: bytes) -> None:
    require(json.dumps(value, sort_keys=True, separators=(",", ":")) ==
            json.dumps(build_manifest(rom), sort_keys=True, separators=(",", ":")),
            "evidence manifest differs from canonical analysis (editable tokens belong in assets.json)")


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def csv_bytes(rows: list[dict[str, Any]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def report(manifest: dict[str, Any]) -> bytes:
    summary = manifest["summary"]
    text = f"""# Pitch and attenuation envelopes (Phase 14)

Evidence: confirmed static Z80 consumer grammar and typed canonical roundtrip;
not natural playback. Ten pitch pointers at800E and eleven attenuation pointers
at815D lead to21 adjacent-pointer-delimited allocations. The complete498-byte
directory/allocation representation is editable, but only
{summary['confirmed_owned_bytes']} bytes have confirmed pointer-seeded read roles.
The remaining{summary['typed_unconsumed_bytes']} bytes are typed probable allocation,
not primary ownership. Original BIN/SMD files remain read-only.

## Exact token grammar

| Consumer | Byte(s) | Effect |
| --- | --- | --- |
| Pitch03C2..040A |00..7F,85..FF|signed delta, multiplied by(scale+1), added modulo65536 to invocation frequency|
| Pitch |80|cursor=0, reevaluate immediately|
| Pitch |81 or83|set channel flag6, unwind one return; no cursor increment|
| Pitch |82,u8|set eight-bit cursor to operand, reevaluate|
| Pitch |84,u8|scale=(scale+operand)mod256; cursor+=2mod256, reevaluate|
| Attenuation0F7B..0FAB |00..7F|return unsigned value, cursor+=1mod256|
| Attenuation |80|cursor=0, reevaluate|
| Attenuation |81|set flag4, unwind one return without ordinary value emission|
| Attenuation |83|set flag4, unwind one return and enter conditional PSG keyoff0FAC|
| Attenuation |82 or84..FF,u8|preserve opcode; cursor=operand, reevaluate|

Pitch scaleFF produces256 DJNZ additions, not zero. There is no signed-delta
interpretation for high attenuation bytes. Keyoff0FAC suppresses writes under
flag2; otherwise only a negative eight-bit(1F+channel_id) writes7F11, with an
additionalFF write when flag0 is set. These are modeled write values, not trace
events. Pitch output uses the supplied frequency for this invocation; no
unsupported assumption accumulates it across separate playback frames.

## Allocation boundaries are not execution boundaries

Pitch1 holds at8033. Its trailing8034..8038 (`84 CE 82 00`) is preserved as
typed tokens but unconsumed from cursor0 and excluded from confirmed ownership.
Other sample loops are represented as cursor-projection cycles, distinct from
control-only loops inside one invocation. Scale may keep changing even when
the cursor repeats, so full-state or audible periodicity is not claimed.

Attenuation11 has `F0 80` at81FE..8200. This is a two-byte redirect to cursor128,
requesting base81F6+128=8276. The allocation-limited audit returns
`memory_unmapped` and records8276; it does not invent an allocation-local stop.
The pure interpreter can follow this address when a caller supplies a larger
mapped window. Any extra mapped reads are not automatically owned envelope data.

The bounded model reports `sample`, `hold`, `key_off`, `control_cycle`,
`memory_unmapped` or `step_limit`, preserving cursor/scale/flags/frequency and
actual observed read addresses. Base+cursor and operand-address arithmetic wrap
at16 bits, while cursor updates wrap at8 bits.

## Reproduction

`assets.json` is the editable typed source. `manifest.json`, `owners.csv`,
`tokens.csv` and this report are reproducible analysis outputs. Fixed-layout
import permits valid token edits, equal-capacity grammar changes and directory
aliases to existing allocations within each family; it rejects relocation,
capacity changes, invalid numeric types, malformed commands and unknown keys.
Unchanged import exactly reproduces the original1MiB ROM; edits touch only
F800E..F8200 and do not silently rewrite the cartridge checksum.

See tools/audio_envelopes/README.md for commands and validation boundaries.
"""
    return text.encode("utf-8")


def render_bundle(rom: bytes) -> dict[str, bytes]:
    assets, manifest = extract(rom), build_manifest(rom)
    tokens = []
    owned = {address for owner in manifest["owners"] for address in range(owner["start"], owner["end"])}
    for table in assets["tables"]:
        for allocation in table["allocations"]:
            position = allocation["z80_start"]
            for token in allocation["tokens"]:
                raw = encode_token(table["family"], token)
                tokens.append({"family": table["family"], "allocation": allocation["z80_start"],
                               "z80_address": position, "rom_offset": rom_offset(position), "width": len(raw),
                               "token": json.dumps(token, sort_keys=True, separators=(",", ":")),
                               "hex": raw.hex(), "consumed_from_cursor0": all(rom_offset(position) + i in owned for i in range(len(raw)))})
                position += len(raw)
    return {"assets.json": json_bytes(assets), "manifest.json": json_bytes(manifest),
            "owners.csv": csv_bytes(manifest["owners"]), "tokens.csv": csv_bytes(tokens),
            "AUDIO_ENVELOPES.md": report(manifest)}


def export_files(rom_path: str | Path, output: str | Path) -> dict[str, Any]:
    source, target = af.safe_path(rom_path, regular_input=True), af.safe_path(output)
    af._separate(target, [source])
    require(not target.exists() and target.parent.is_dir(), "output must be fresh with existing parent")
    rom = af._read(source, ROM_SIZE)
    bundle = render_bundle(rom)
    staging = Path(tempfile.mkdtemp(prefix=".audio-envelopes-", dir=target.parent))
    identity, produced = staging.stat(), {}
    try:
        for name, data in bundle.items():
            with (staging / name).open("xb") as stream:
                stream.write(data)
            produced[name] = data
        af.safe_path(output)
        require(not target.exists(), "output appeared during generation")
        os.rename(staging, target)
    finally:
        af._cleanup_stage(staging, produced, identity)
    return build_manifest(rom)["summary"]


def import_files(rom_path: str | Path, asset_path: str | Path, output: str | Path) -> dict[str, Any]:
    source, assets_file = af.safe_path(rom_path, regular_input=True), af.safe_path(asset_path, regular_input=True)
    target = af.safe_path(output)
    af._separate(target, [source, assets_file])
    require(not target.exists() and target.parent.is_dir(), "output must be fresh with existing parent")
    rom = af._read(source, ROM_SIZE)
    result = rebuild(rom, af.load_assets(af._read(assets_file, 8 * 1024 * 1024)))
    fd, name = tempfile.mkstemp(prefix=".audio-envelopes-import-", dir=target.parent)
    staging, complete = Path(name), False
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(result)
            stream.flush()
            os.fsync(stream.fileno())
        complete = True
        af.safe_path(output)
        os.link(staging, target)  # exclusive publication; never replace an existing output
    finally:
        if staging.exists():
            af.safe_path(staging, regular_input=True)
            if complete and af._read(staging, len(result)) == result:
                staging.unlink()
            else:
                raise ValueError("incomplete/modified staging output retained for inspection")
    return {"sha256": hashlib.sha256(result).hexdigest(), "canonical_roundtrip": result == rom,
            "changed_bytes": sum(a != b for a, b in zip(rom, result))}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("verify", "generate", "import"))
    parser.add_argument("--rom", type=Path, default=DEFAULT_ROM)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--assets", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "verify":
            result = build_manifest(af._read(af.safe_path(args.rom, regular_input=True), ROM_SIZE))["summary"]
        elif args.command == "generate":
            result = export_files(args.rom, args.output)
        else:
            require(args.assets is not None, "import requires --assets")
            result = import_files(args.rom, args.assets, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as error:
        parser.exit(2, f"audio_envelopes: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
