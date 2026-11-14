#!/usr/bin/env python3
"""Lossless field-level codec and 68000 emission model for duel sprite records.

The ownership claim is about the directory and terminated record grammar, not
about the lifetime of selectors or the maximum sprites emitted in a frame.
Only the canonical input is accepted by extraction/import; the importer edits
fixed slots in a separate ROM and intentionally does not repair its checksum.
"""

from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import csv
import hashlib
import io
import json
import os
import shutil
import stat
import struct
import tempfile
from pathlib import Path
from typing import Any

ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
TABLE_START, TABLE_END, DATA_END = 0x29038, 0x29154, 0x2A22E
SLOT_COUNT = 71
RECORD_SIZE = 6
CONSUMER_START, CONSUMER_END = 0x28F9C, 0x29038
CONSUMER_SHA256 = reference_value(__name__, 'CONSUMER_SHA256')
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
DEFAULT_OUTPUT = ROOT / "analysis/sprite_records/generated"


class SpriteError(ValueError):
    """A codec, identity, boundary, or publication invariant failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SpriteError(message)


def exact_keys(value: Any, keys: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == keys, f"{label}: wrong keys/type")


def integer(value: Any, low: int, high: int, label: str) -> int:
    require(type(value) is int and low <= value <= high, f"{label}: expected integer {low}..{high}")
    return value


def boolean(value: Any, label: str) -> bool:
    require(type(value) is bool, f"{label}: expected boolean")
    return value


def canonical(rom: bytes) -> None:
    require(type(rom) is bytes and len(rom) == ROM_SIZE, "wrong ROM size/type")
    require(hashlib.sha256(rom).hexdigest() == ROM_SHA256, "wrong canonical ROM hash")


def regular_path(path: Path, *, must_exist: bool = True) -> Path:
    """Inspect the lexical chain before resolution, including Windows junctions."""
    absolute = Path(os.path.abspath(path))
    # abspath normalizes '..'; inspecting the original chain first is important
    # when a link precedes '..'. Reject that syntax instead of interpreting it.
    require(".." not in path.parts, "parent traversal is not accepted")
    for component in [*reversed(absolute.parents), absolute]:
        try:
            info = component.lstat()
        except FileNotFoundError:
            continue
        require(not stat.S_ISLNK(info.st_mode), f"symbolic-link path refused: {component}")
        require(not getattr(info, "st_file_attributes", 0) & 0x400,
                f"reparse path refused: {component}")
        if component != absolute:
            require(stat.S_ISDIR(info.st_mode), "non-directory ancestor")
    if must_exist:
        require(absolute.is_file(), f"missing/nonregular input: {absolute}")
    return absolute


def fresh_target(path: Path, inputs: tuple[Path, ...]) -> Path:
    target = regular_path(path, must_exist=False)
    require(not target.exists(), f"output already exists: {target}")
    require(target.parent.is_dir(), "output parent must already exist")
    for source in inputs:
        resolved = regular_path(source)
        require(target != resolved and target not in resolved.parents and resolved not in target.parents,
                "input/output paths overlap")
    return target


def read_rom(path: Path) -> bytes:
    rom = regular_path(path).read_bytes()
    canonical(rom)
    return rom


RECORD_KEYS = {"end", "control_unused", "size_unused", "width_tiles", "height_tiles",
               "y_offset", "x_offset", "tile_index", "horizontal_flip", "vertical_flip",
               "palette", "priority"}


def decode_record(raw: bytes) -> dict[str, Any]:
    require(type(raw) is bytes and len(raw) == RECORD_SIZE, "record must contain exactly six bytes")
    control, size, y, x, attribute = struct.unpack(">BBbbH", raw)
    return {
        "end": bool(control & 0x80), "control_unused": control & 0x7F,
        "size_unused": size >> 4, "width_tiles": ((size >> 2) & 3) + 1,
        "height_tiles": (size & 3) + 1, "y_offset": y, "x_offset": x,
        "tile_index": attribute & 0x7FF, "horizontal_flip": bool(attribute & 0x800),
        "vertical_flip": bool(attribute & 0x1000), "palette": (attribute >> 13) & 3,
        "priority": bool(attribute & 0x8000),
    }


def encode_record(record: dict[str, Any]) -> bytes:
    exact_keys(record, RECORD_KEYS, "record")
    control = 128 * boolean(record["end"], "end") + integer(record["control_unused"], 0, 127, "control_unused")
    size = (integer(record["size_unused"], 0, 15, "size_unused") << 4)
    size |= (integer(record["width_tiles"], 1, 4, "width_tiles") - 1) << 2
    size |= integer(record["height_tiles"], 1, 4, "height_tiles") - 1
    y = integer(record["y_offset"], -128, 127, "y_offset")
    x = integer(record["x_offset"], -128, 127, "x_offset")
    attribute = integer(record["tile_index"], 0, 0x7FF, "tile_index")
    attribute |= boolean(record["horizontal_flip"], "horizontal_flip") << 11
    attribute |= boolean(record["vertical_flip"], "vertical_flip") << 12
    attribute |= integer(record["palette"], 0, 3, "palette") << 13
    attribute |= boolean(record["priority"], "priority") << 15
    return struct.pack(">BBbbH", control, size, y, x, attribute)


def layout(rom: bytes) -> tuple[list[int], list[tuple[int, int]]]:
    """Prove directory/payload partition from all pointers and consumer terminators."""
    canonical(rom)
    pointers = list(struct.unpack(f">{SLOT_COUNT}I", rom[TABLE_START:TABLE_END]))
    require(len(set(pointers)) == SLOT_COUNT and min(pointers) == TABLE_END, "directory uniqueness/start changed")
    require(all(TABLE_END <= p < DATA_END and (p - TABLE_END) % 6 == 0 for p in pointers),
            "invalid descriptor pointer")
    ordered = sorted(pointers)
    spans = list(zip(ordered, ordered[1:] + [DATA_END]))
    for start, end in spans:
        require((end - start) % 6 == 0, "misaligned descriptor boundary")
        flags = [rom[pos] & 0x80 for pos in range(start, end, 6)]
        require(flags and flags[-1] and not any(flags[:-1]), "first terminator does not match next boundary")
    return pointers, spans


def export_assets(rom: bytes) -> dict[str, Any]:
    pointers, spans = layout(rom)
    return {
        "format": "g5510-duel-sprite-records-v1",
        "canonical_rom_sha256": ROM_SHA256,
        "directory_start": TABLE_START, "directory_end": TABLE_END, "payload_end": DATA_END,
        "pointers": pointers,
        "descriptors": [{"start": start, "records": [decode_record(rom[p:p + 6])
                         for p in range(start, end, 6)]} for start, end in spans],
    }


def import_assets(rom: bytes, assets: dict[str, Any]) -> bytes:
    """Allow field edits and pointer aliases without changing any physical capacity."""
    _, spans = layout(rom)
    exact_keys(assets, {"format", "canonical_rom_sha256", "directory_start", "directory_end",
                       "payload_end", "pointers", "descriptors"}, "assets")
    require(assets["format"] == "g5510-duel-sprite-records-v1" and
            assets["canonical_rom_sha256"] == ROM_SHA256, "wrong format/base identity")
    for key, expected in (("directory_start", TABLE_START), ("directory_end", TABLE_END), ("payload_end", DATA_END)):
        require(type(assets[key]) is int and assets[key] == expected, f"{key}: relocation refused")
    pointers = assets["pointers"]
    require(type(pointers) is list and len(pointers) == SLOT_COUNT, "wrong pointer count/type")
    starts = {start for start, _ in spans}
    require(all(type(pointer) is int and pointer in starts for pointer in pointers),
            "pointer must address an existing complete descriptor")
    descriptors = assets["descriptors"]
    require(type(descriptors) is list and len(descriptors) == SLOT_COUNT, "wrong descriptor count/type")
    result = bytearray(rom)
    result[TABLE_START:TABLE_END] = struct.pack(f">{SLOT_COUNT}I", *pointers)
    for descriptor, (start, end) in zip(descriptors, spans):
        exact_keys(descriptor, {"start", "records"}, "descriptor")
        require(type(descriptor["start"]) is int and descriptor["start"] == start, "descriptor order/relocation changed")
        records = descriptor["records"]
        require(type(records) is list and len(records) == (end - start) // 6, "record capacity changed")
        encoded = b"".join(encode_record(record) for record in records)
        require(all(not record["end"] for record in records[:-1]) and records[-1]["end"],
                "terminal record must remain at fixed physical boundary")
        result[start:end] = encoded
    require(len(result) == len(rom), "import changed ROM size")
    return bytes(result)


def emit_descriptor(records: list[dict[str, Any]], *, y_origin: int, x_origin: int,
                    attribute_base: int, sprite_count: int) -> dict[str, Any]:
    """Reproduce the bounded 028FCE..02902C loop, including 16-bit wrap/contamination.

    This pure model returns the new SAT bytes and an optional previous-link patch.
    It does not assert that an arbitrary RAM pointer/count pair is well-formed.
    Whether the previous-link patch occurs depends on A0 != FFFFF800, not count.
    """
    require(type(records) is list and len(records) > 0, "descriptor is empty")
    y_origin = integer(y_origin, 0, 0xFFFF, "y_origin")
    x_origin = integer(x_origin, 0, 0xFFFF, "x_origin")
    attribute_base = integer(attribute_base, 0, 0xFFFF, "attribute_base")
    count = integer(sprite_count, 0, 0xFFFF, "sprite_count")
    raw_records = [encode_record(record) for record in records]
    require(not any(raw[0] & 128 for raw in raw_records[:-1]) and bool(raw_records[-1][0] & 128),
            "descriptor must end at its first terminator")
    base, flips = attribute_base & 0xE7FF, attribute_base & 0x1800
    old_link = count & 255
    count = (count + 1) & 0xFFFF
    output = bytearray()
    for raw in raw_records:
        _, size, y, x, tile = struct.unpack(">BBbbH", raw)
        y_word = (y + y_origin + 128) & 0xFFFF
        size_link = ((size << 8) | count) & 0xFFFF
        count = (count + 1) & 0xFFFF
        # ASR.W #7, ANDI.W #$18: the sign extension is removed by the mask.
        # Counter high bits can contaminate this word; do not clamp to a byte.
        width = 8 + ((size_link >> 7) & 0x18)
        tile_word = ((tile + base) & 0xFFFF) ^ flips
        if flips & 0x800:
            x = -x - width
        x_word = (x + x_origin + 128) & 0xFFFF
        output.extend(struct.pack(">4H", y_word, size_link, tile_word, x_word))
    output[-5] = 0  # MOVE.B #0,-5(A0) affects only the final link byte.
    return {"sat_bytes": bytes(output), "final_sprite_count": (count - 1) & 0xFFFF,
            "pointer_advance": 8 * len(records), "previous_link_byte_if_not_reset_pointer": old_link}


def selector_class(index: int) -> str:
    if index < 54:
        return "conditional ordinary: 18*kind + 6*direction + frame (028E80..028EA4)"
    if index in (60, 61):
        return "conditional effect: ((FF7008 >> 4) & 1) + 60 (028F32..028F3E)"
    if 54 <= index <= 58 or 62 <= index <= 66:
        return "conditional overlay: (62 if kind == 0 else 54) + frame for frame0..4 (028F18..028F26)"
    if index == 67:
        return "confirmed immediate 67 at 027DE8/027EBE/027F78/027FFA"
    if index >= 68:
        return "conditional zero-health: byte[028F8C + kind] for kind 0..2 (028F54..028F5C)"
    return "unknown selector reachability; confirmed terminated descriptor grammar"


def build_manifest(rom: bytes) -> dict[str, Any]:
    assets = export_assets(rom)
    rebuilt = import_assets(rom, assets)
    pointers, spans = layout(rom)
    require(rebuilt == rom, "canonical field round trip failed")
    require(hashlib.sha256(rom[CONSUMER_START:CONSUMER_END]).hexdigest() == CONSUMER_SHA256,
            "consumer identity failed")
    owners = [{"id": "sprite-directory", "start": TABLE_START, "end": TABLE_END,
               "kind": "be32_sprite_descriptor_pointer_directory", "evidence": "confirmed",
               "role": "71 absolute pointers consumed by 028FA6..028FAC", "primary_ownership": True}]
    owners += [{"id": f"sprite-descriptor-{start:06x}", "start": start, "end": end,
                "kind": "terminated_6byte_sprite_records", "evidence": "confirmed",
                "role": "typed records consumed by 028FCE..02901C; first bit7 terminator matches next physical boundary",
                "primary_ownership": True} for start, end in spans]
    for owner in owners:
        owner["byte_count"] = owner["end"] - owner["start"]
        owner["sha256"] = hashlib.sha256(rom[owner["start"]:owner["end"]]).hexdigest()
    return {
        "format": "g5510-sprite-record-analysis-v1", "rom_sha256": ROM_SHA256,
        "consumer": {"start": CONSUMER_START, "end": CONSUMER_END, "sha256": CONSUMER_SHA256,
                     "evidence": "confirmed", "primary_ownership": False},
        "summary": {"directory_slots": 71, "unique_descriptors": 71, "records": 719,
                    "directory_bytes": TABLE_END - TABLE_START, "record_bytes": DATA_END - TABLE_END,
                    "owned_bytes": DATA_END - TABLE_START, "minimum_records": 3, "maximum_records": 25,
                    "canonical_roundtrip": True, "complete_selector_lifetime": False,
                    "complete_frame_bound": False, "runtime_observations": 0},
        "owners": owners,
        "slots": [{"index": index, "pointer_address": TABLE_START + 4 * index, "start": pointer,
                   "end": dict(spans)[pointer], "records": (dict(spans)[pointer] - pointer) // 6,
                   "selection_evidence": selector_class(index)} for index, pointer in enumerate(pointers)],
        "unknowns": [
            "Canonical lifetime bounds on object kind/direction/frame are not proved by this package.",
            "Selector59 has typed records but no reviewed caller under the local frame0..4 premises.",
            "Total sprites per frame, valid FF7002 pointer lifetime and absence of FF7018 alias writes remain unproved.",
            "No live sprite/SAT trace or emulator differential test is claimed; emitter checks are static arithmetic models.",
            "Control bits0..6 are unconsumed by this routine; size bits4..7 are copied, their hardware meaning is not claimed.",
            "Individual art/character identities and tile-to-VRAM runtime mapping remain outside this package.",
        ],
    }


def csv_text(rows: list[dict[str, Any]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def assembly(assets: dict[str, Any]) -> str:
    result = ["| Generated typed sprite data. GNU m68k assembler, big endian.",
              "| Place this section at ROM 0x029038. This file does not set the origin.",
              "SpriteDescriptorDirectory:"]
    result += [f"  .long 0x029038 + SpriteDescriptor_{pointer:06X} - SpriteDescriptorDirectory | selector {index}"
               for index, pointer in enumerate(assets["pointers"])]
    for descriptor in assets["descriptors"]:
        result.append(f"SpriteDescriptor_{descriptor['start']:06X}:")
        for record in descriptor["records"]:
            raw = encode_record(record)
            result += ["  .byte " + ", ".join(f"0x{value:02X}" for value in raw[:4]) +
                       f" | end={int(record['end'])}, size={record['width_tiles']}x{record['height_tiles']}, " +
                       f"dy={record['y_offset']}, dx={record['x_offset']}",
                       f"  .word 0x{int.from_bytes(raw[4:], 'big'):04X} | tile={record['tile_index']}, " +
                       f"H={int(record['horizontal_flip'])}, V={int(record['vertical_flip'])}, " +
                       f"palette={record['palette']}, priority={int(record['priority'])}"]
    return "\n".join(result) + "\n"


def report(manifest: dict[str, Any]) -> str:
    return """# Typed duel sprite records (Phase 13)

Evidence status: **confirmed static grammar and canonical lossless field codec**.
The directory at `029038..029154` contains 71 unique absolute BE32 pointers.
Their payload is a gapless, nonoverlapping partition of `029154..02A22E`:
719 six-byte records, 3..25 per descriptor. Every first terminating record ends
exactly at the next physical pointer (or the known code boundary `02A22E`).
These 4,598 bytes have a typed importer, not an opaque-byte wrapper. The consumer
`028F9C..029038` is observation-only here; no duplicate code ownership is added.

## Record grammar and evidence

| Offset | Field | Evidence / exact operation |
| --- | --- | --- |
| +0 | control: bit7 terminates, bits0..6 preserved | `029014` advances by6; `029016` tests bit7 of previous record |
| +1 | size: width bits2..3, height bits0..1, upper nibble retained | `028FDC..028FE6` shifts byte8 and ORs 16-bit link/count |
| +2 | signed Y offset | `028FCE..028FDA`: sign extend, add D0 and128 |
| +3 | signed X offset | `028FFC..029012`: sign extend, optional -x-width, add D1 and128 |
| +4 | BE16 tile/attribute word | `028FF2..028FFA`: add (D3&E7FF) modulo16, XOR (D3&1800) |

Tile/attribute fields are exported separately: 11-bit tile index, horizontal and
vertical flips, two-bit palette, priority. These bit names express the normal
Mega Drive SAT word layout; the consumer arithmetic can carry across fields.
Control unused bits and size upper bits are never discarded. No Y-coordinate
compensation is done for vertical flip. Horizontal compensation depends on the
base D3 bit11, not the final XOR'ed tile word or the record's own flip flag.

Each record emits four BE16 words (Y, size/link, tile/attribute, X), eight bytes.
At entry `028FBE` patches the preceding link byte only if A0 != FFFFF800;
at exit `02901E` clears only the final link byte. Counter arithmetic is word-size:
the model preserves wraparound and counter high bits contaminating size/width.
The pointer advance is 8*record_count, 24..200 bytes per canonical descriptor.
This is a per-call result, **not a total-per-frame upper bound**.

## Selection and limitations

`027DE8/027EBE/027F78/027FFA` select67 directly. `028F32..028F3E` selects
60 or61 conditionally on reaching the call. `028F54..028F5C` indexes the byte
table `44 45 46 FF` at028F8C, selecting68..70 only for kind0..2.
`028E80..028EA4` computes 18*kind+6*direction+frame; 0..53 follows only
under kind0..2/direction0..2/frame0..5 premises, not proved lifetimes here.
`028F18..028F26` selects base62 for kind0, base54 otherwise, plus overlay frame;
the local `028EE6..028F06` cycle bounds that frame to0..4 under valid entry state.
Thus54..58 and62..66 have conditional overlay callers. Selector59 remains a
confirmed descriptor with no reviewed selector under these local premises.

The complete selector lifetime, FF7002 pointer lifetime, total per-frame sprite
count and absence of writes aliasing FF7018 remain **unknown**. This package does
not close Phase12's indirect-domain blocker. No natural runtime observation or
emulator differential result is claimed. Art identities and runtime VRAM tile
ownership are also unknown here.

## Reproduction and editable outputs

`assets.json` is the editable fixed-layout source; every byte has a typed field.
`sprite_records.s` renders the same source as GNU m68k assembly, place at029038.
`manifest.json`, `owners.csv`, `slots.csv` and `records.csv` are analysis outputs.
Import accepts field edits and directory aliases to existing descriptor starts,
but refuses relocation, changing descriptor length or moving the first terminator.
It only changes `029038..02A22E` in a separate output ROM. No checksum rewrite is
performed. Canonical export/import is exactly equal to the original 1MiB BIN.

Run commands and validation limits are described in `tools/sprite_records/README.md`.
"""


def render(rom: bytes) -> dict[str, bytes]:
    assets, manifest = export_assets(rom), build_manifest(rom)
    rows = []
    for descriptor in assets["descriptors"]:
        rows.extend({"descriptor_start": descriptor["start"], "record_index": index,
                     "address": descriptor["start"] + 6 * index, **record}
                    for index, record in enumerate(descriptor["records"]))
    strings = {
        "assets.json": json.dumps(assets, ensure_ascii=False, indent=2) + "\n",
        "manifest.json": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        "owners.csv": csv_text(manifest["owners"]), "slots.csv": csv_text(manifest["slots"]),
        "records.csv": csv_text(rows), "sprite_records.s": assembly(assets),
        "SPRITE_RECORDS.md": report(manifest),
    }
    return {name: content.encode("utf-8") for name, content in strings.items()}


def generate(rom_path: Path, output: Path) -> dict[str, Any]:
    rom = read_rom(rom_path)
    target = fresh_target(output, (rom_path,))
    outputs = render(rom)
    staging = Path(tempfile.mkdtemp(prefix=".sprite-records-", dir=target.parent))
    try:
        for name, data in outputs.items():
            (staging / name).write_bytes(data)
        fresh_target(target, (rom_path,))
        # Windows rename refuses existing targets; POSIX directory replacement
        # is guarded immediately beforehand. This is not an adversarial-FS API.
        staging.rename(target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return build_manifest(rom)["summary"]


def write_import(rom_path: Path, assets_path: Path, output: Path) -> dict[str, Any]:
    rom = read_rom(rom_path)
    source = regular_path(assets_path)
    target = fresh_target(output, (rom_path, source))
    # Reject duplicate object keys rather than silently accepting last-value wins.
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        require(len({key for key, _ in values}) == len(values), "duplicate JSON key")
        return dict(values)
    assets = json.loads(source.read_text(encoding="utf-8"), object_pairs_hook=pairs)
    encoded = import_assets(rom, assets)
    descriptor, temporary = tempfile.mkstemp(prefix=".sprite-records-import-", dir=target.parent)
    staging = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
        fresh_target(target, (rom_path, source))
        staging.rename(target)
    finally:
        if staging.exists():
            staging.unlink()
    return {"output": str(target), "sha256": hashlib.sha256(encoded).hexdigest(),
            "canonical_roundtrip": encoded == rom,
            "changed_bytes": sum(left != right for left, right in zip(rom, encoded))}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("verify", "generate", "import"))
    parser.add_argument("--rom", type=Path, default=DEFAULT_ROM)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--assets", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "generate":
            result = generate(args.rom, args.output)
        elif args.command == "import":
            require(args.assets is not None, "--assets is required for import")
            result = write_import(args.rom, args.assets, args.output)
        else:
            result = build_manifest(read_rom(args.rom))["summary"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (SpriteError, OSError, json.JSONDecodeError) as error:
        parser.exit(2, f"sprite_records: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
