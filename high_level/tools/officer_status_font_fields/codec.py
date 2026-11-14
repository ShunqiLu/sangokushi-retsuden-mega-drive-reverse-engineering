"""Lossless 80-byte counted-font source selected by the original masked BYTE.

Ten editable rows hold four full WORDs each. CPU rows10..12 read older-owned
sources, not extra rows. The last5 bytes also feed the counted font8 reader.
Negative WORDs are procedural cells, never terminators/dialogue controls.
Only the CLI performs I/O; diagnostics read original or edited complete images.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared
from tools.text_font import text_font_assets as font

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
OUTPUT_ROOT = ROOT / "build/officer_status_font_fields"
FORMAL_ROOT = ROOT / "analysis/officer_status_font_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 80
START, END = 0x08A3D6, 0x08A426
BYTE_ALIAS_START = 0x08A421
OLD_ALIAS_END = 0x08A43E
BLOCK_ID = "rom_08A3D6_counted_status_font_WORDs"
FORMAT = "g5510-counted-status-font-fixed-WORD-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = "build/direct_code/layout/" + LAYOUT_ID + "/m68k_bank08.s"
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
CONSUMERS = (
    (0x00B39E, 0x00B3D4, reference_value(__name__, 'CONSUMERS')),
    (0x005330, 0x005356, reference_value(__name__, 'CONSUMERS_2')),
    (0x00AE8A, 0x00AF48, reference_value(__name__, 'CONSUMERS_3')),
)
INSTRUCTIONS = (
    (0xB39E, "41f8c700"), (0xB3A2, "14302000"), (0xB3A6, "0242000f"),
    (0xB3AA, "0c420004"), (0xB3AE, "63000006"), (0xB3B2, "04420003"),
    (0xB3B6, "31c2f63a"), (0xB3BA, "e74a"), (0xB3BC, "41f90008a3d6"),
    (0xB3C2, "41f02000"), (0xB3C6, "363c0003"), (0xB3CA, "43f8d300"),
    (0xB3CE, "4eb90000ae8a"),
    (0x5330, "3438f364"), (0x5334, "024200ff"), (0x5338, "3602"),
    (0x533A, "e54a"), (0x533C, "d443"), (0x533E, "41f90008a421"),
    (0x5344, "41f02000"), (0x5348, "43f8d300"), (0x534C, "363c0004"),
    (0x5350, "4eb90000af1e"),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    for start, end, expected in CONSUMERS:
        if sha(rom[start:end]) != expected:
            raise ValueError("pinned original consumer/reader bytes differ")


def metadata():
    return dict(
        format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(id=BLOCK_ID, start=START, end=END, bytes=EDITABLE_BYTES,
                            editable_rows=10, WORDs_per_row=4, stride_bytes=8, WORD_order="big"),
        evidence=dict(
            confidence="confirmed", source="canonical bytes + older instruction ledger + counted-font reader",
            enhanced_source=dict(path=ENHANCED_PATH, sha256=ENHANCED_SHA256,
                                 original_caller_reachability_confidence="heuristic"),
            frozen_raw_layout=dict(id=LAYOUT_ID, path=LAYOUT_PATH, sha256=LAYOUT_SHA256,
                line=7109, bank=8, offset=0xA3D6, length=80,
                all_emitted_bytes_raw=True, old_typed_baseline_overlap_bytes=0),
            consumers=[dict(start=start, end=end, bytes=end - start, sha256=expected)
                       for start, end, expected in CONSUMERS],
            instructions=[dict(address=address, bytes=raw, original_confidence="heuristic")
                          for address, raw in INSTRUCTIONS],
            WORD_source=dict(source_BYTE_RAM=0xFFC700, source_BYTE_read=0xB3A2,
                ANDI_W=0xB3A6, mask_WORD=15, unsigned_BLS_compare=4,
                BLS_address=0xB3AE, SUBI_if_above=3, SUBI_address=0xB3B2,
                row_rule="nibble if nibble <= 4 else nibble - 3", local_rows=list(range(13)),
                LSL_W_address=0xB3BA, shift=3, source_LEA=0xB3BC, effective_base=START,
                D3_load=0xB3C6, D3_original=3, WORD_count=4, JSR=0xB3CE, reader=0xAE8A,
                termination="caller_D3_plus_one_not_source_marker", CPU_clamp=False,
                indexed_path_only=True, full_C700_RAM_lookup_and_E640_alternative_modeled=False),
            older_source_alias=dict(rows=[10, 11, 12], start=END, end=OLD_ALIAS_END, bytes=24,
                old_font_BYTE_range=[0x8A426, 0x8A430], old_font_WORD_range=[0x8A430, 0x8A462],
                emitted=False, diagnostic_reads_literal_WORDs=True,
                alias_bitmap_addresses_not_validated_as_editor_cells=True),
            BYTE_source_alias=dict(source_global_WORD_RAM=0xFFF364, WORD_read=0x5330,
                ANDI_W=0x5334, mask_WORD=255, source_LEA=0x533E, effective_base=BYTE_ALIAS_START,
                index_rule="5 * (F364.W & 0x00FF)", D3_load=0x534C, D3_original=4,
                BYTE_count=5, JSR=0x5350, reader=0xAF1E,
                source_WORD_min=0, source_WORD_max=65535, masked_BYTE_min=0, masked_BYTE_max=255,
                overlap_start=BYTE_ALIAS_START, overlap_end=END, overlap_bytes=5,
                CPU_clamp=False, separate_editing_authority=False),
            glyph_grammar=dict(
                negative_WORD="procedural_cell_using_caller_D0_D1_not_a_terminator_or_dialogue_control",
                sign_branch=0xAE90, procedural_entry=0xAED8,
                positive_WORD="original_full_WORD_font16_bitmap_address",
                offset_rule="(((WORD & 0xFF00) << 3) & 0xFFFF) | (((WORD & 0x00FF) << 5) & 0xFFFF)",
                zero_extend_LONG=0xAEA2, LONG_index=0xAEAE,
                font16_start=font.FONT16_START, font16_end=font.FONT16_END, bitmap_bytes=32,
                font8_start=font.FONT8_START, font8_end=font.FONT8_END, bitmap8_bytes=8,
                full_attribute_alias_bits_preserved=True, natural_column_clamp=False,
                source_8000_or_FFFF_terminates=False)),
        unreferenced_08AB04_08AC04=dict(start=0x8AB04, end=0x8AC04, confidence="unknown", emitted=False),
        row_business_names="unknown", Unicode_mapping="unknown", edited_gameplay_safety="unknown",
        independent_CPU_comparison=False,
    )


def glyph_cell(word):
    """Counted reader sign branch; preserve full WORD and its attribute aliases."""
    uint(word, 0xFFFF, "full counted font WORD")
    if word & 0x8000:
        return dict(kind="procedural_cell", WORD=word)
    offset = font.font16_offset(word)
    if offset + 32 > font.FONT16_END - font.FONT16_START:
        raise ValueError("positive WORD bitmap read outside existing physical font16 allocation")
    return dict(kind="font16_bitmap", WORD=word)


def row_fixed(index):
    return dict(id=f"status_font_row_{index}", row_index=index,
                start=START + 8 * index, end=START + 8 * (index + 1))


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["rows"] = [dict(**row_fixed(row), cells=[glyph_cell(int.from_bytes(rom[p:p+2], "big"))
        for p in range(START + 8 * row, START + 8 * row + 8, 2)]) for row in range(10)]
    return fields


def pinned(row, fixed, mutable, label):
    keys(row, set(fixed) | set(mutable), label)
    for key, value in fixed.items():
        same(row[key], value, label + "." + key)


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {"rows"}, "counted status font package")
    raw = bytearray()
    for index, row in enumerate(exact_list(fields["rows"], 10, "editable font rows")):
        pinned(row, row_fixed(index), {"cells"}, "font row")
        for cell in exact_list(row["cells"], 4, "counted font row cells"):
            keys(cell, {"kind", "WORD"}, "font cell")
            same(cell, glyph_cell(cell["WORD"]), "font sign-branch kind and full WORD")
            raw.extend(cell["WORD"].to_bytes(2, "big"))
    if len(raw) != EDITABLE_BYTES:
        raise ValueError("fixed 80-byte source cost differs")
    return [dict(id=BLOCK_ID, start=START, end=END, data=bytes(raw),
                 role="confirmed_actually_read_counted_font_source_WORDs")]


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def row_index(source_BYTE):
    nibble = uint(source_BYTE, 255, "already-fetched C700 source BYTE") & 15
    return nibble if nibble <= 4 else nibble - 3


def lookup_WORDs(image, source_BYTE):
    """The indexed path's four literal reads, including rows10..12 old aliases."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires a complete bytes image")
    row = row_index(source_BYTE)
    start = START + 8 * row
    addresses = list(range(start, start + 8, 2))
    return dict(row_index=row, start=start, end=start + 8,
                inside_edit_scope=start < END, addresses=addresses,
                WORDs=[int.from_bytes(image[p:p+2], "big") for p in addresses])


def font8_read_address(f364_WORD):
    return BYTE_ALIAS_START + 5 * (uint(f364_WORD, 65535, "complete F364 selector WORD") & 255)


def lookup_font8(image, f364_WORD):
    """Actual five BYTE indices from an edited image; no canonical-extract gate."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires a complete bytes image")
    start = font8_read_address(f364_WORD)
    return dict(masked_selector_BYTE=f364_WORD & 255, start=start, end=start + 5,
                glyph_indices=list(image[start:start+5]),
                inside_edit_scope=START <= start and start + 5 <= END)


def schema():
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def exact(items):
        return dict(type="array", prefixItems=items, items=False, minItems=len(items), maxItems=len(items))
    def fixed(value):
        if type(value) is dict:
            return obj({key: fixed(item) for key, item in value.items()})
        if type(value) is list:
            return exact([fixed(item) for item in value])
        return dict(type={str: "string", int: "integer", bool: "boolean"}[type(value)], const=value)
    properties = {key: fixed(value) for key, value in metadata().items()}
    cell = obj(dict(kind=dict(type="string", enum=["font16_bitmap", "procedural_cell"]),
                    WORD=dict(type="integer", minimum=0, maximum=65535)))
    properties["rows"] = exact([obj({**{key: fixed(value) for key, value in row_fixed(i).items()},
        "cells": dict(type="array", minItems=4, maxItems=4, items=cell)}) for i in range(10)])
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Runtime additionally validates positive full-WORD bitmap addresses and sign-branch kinds. Counted WORDs have no terminator; raw rows10..12 and the font8 BYTE alias are diagnostics, not emit authorities."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom or image[END:OLD_ALIAS_END] != rom[END:OLD_ALIAS_END]:
        raise ValueError("whole-ROM serialized field roundtrip or old alias preservation differs")
    encoded = blocks(rom, fields)[0]
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
        editable_WORDs=40, whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        original_source_hex=rom[START:END].hex(), preview_is_editing_authority=False,
        original_old_owned_alias_examples=[lookup_WORDs(rom, byte) for byte in (13, 14, 15)],
        original_font8_alias_example=lookup_font8(rom, 0),
        original_font8_FFFF_example=lookup_font8(rom, 65535),
        blocks=[{key: value for key, value in encoded.items() if key != "data"}
                | dict(bytes=len(encoded["data"]), sha256=sha(encoded["data"]))])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in officer_status_font_fields build scope or the exact formal bundle")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "import", "verify"))
    parser.add_argument("--rom", default=str(DEFAULT_ROM))
    parser.add_argument("--fields")
    parser.add_argument("--bundle")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    target = None
    if args.command == "export":
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError("export requires a fresh output only")
        target = fresh_output(args.output, bundle=True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None:
            raise ValueError("import requires fields and fresh output")
        target = fresh_output(args.output)
        if target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.bundle is not None and args.fields is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom = read_bounded(args.rom, ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            put(target / name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES,
                      members={name: sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        members = render_bundle(rom)
        for name, data in members.items():
            if read_bounded(bundle / name, MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=EDITABLE_BYTES,
                      whole_ROM_exact=True, whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=EDITABLE_BYTES,
                      exact_canonical=image == rom, bytes=len(image), sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
