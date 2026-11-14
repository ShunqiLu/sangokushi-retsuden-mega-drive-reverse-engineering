"""1018 actually-read source bytes, disjoint from both original font banks.

704 VDP-upload bytes use22 physical4bpp tiles;152 counted full WORDs feedAE8A;
10 counted BYTE indices feedAF1E. AE8A's negative WORD draws a procedural cell:
8000/FFFF are NOT terminators or main-dialogue dispatches here. All398 bytes
outside the proven fixed reads remain unknown, including indexed-table gaps.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.vdp_word_streams import format as shared
from tools.text_font import text_font_assets as font

DEFAULT_ROM = shared.DEFAULT_ROM
FORMAL_ROOT = ROOT / "analysis/bank08_display_resources/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
OUTPUT_ROOT = ROOT / "build/bank08_display_resources"
FORMAT = "candidate-bank08-fixed-display-source-fields-v1"
EDITABLE_BYTES = 1018
# Source start/end, LEA, immediate count, write, DBRA, count-register opcode.
TILES = ((0x089EFC, 0x089F5C, 0x0055B0, 0x0055C0, 0x0055C4, 0x0055CA, 0x303C),
         (0x089F5C, 0x089F7C, 0x0052EA, 0x0052F0, 0x0052F4, 0x0052FA, 0x383C),
         (0x089F7C, 0x08A07C, 0x00B2B6, 0x00B2BC, 0x00B2C0, 0x00B2C6, 0x363C),
         (0x08A07C, 0x08A0BC, 0x000654, 0x00065A, 0x00065E, 0x000664, 0x303C),
         (0x08A0BC, 0x08A1BC, 0x0108B2, 0x0108B8, 0x0108BC, 0x0108C2, 0x303C))
WORD_GROUPS = ((0x08A1BC, 0x08A216), (0x08A374, 0x08A3D6),
               (0x08A430, 0x08A462), (0x08A46A, 0x08A4AC))
# source, WORD count, source LEA (None for retained-A0 continuation), D3 load, JSR.
WORD_READS = ((0x08A1BC, 25, 0x005022, 0x005028, 0x00502C),
              (0x08A1EE, 3, None, 0x00504E, 0x005052),
              (0x08A1F4, 4, 0x0050C6, 0x0050CC, 0x0050D0),
              (0x08A1FC, 2, 0x005204, 0x00520E, 0x005212),
              (0x08A200, 10, 0x005218, 0x00521E, 0x005222),
              (0x08A214, 1, 0x00A864, 0x00A86A, 0x00A872),
              (0x08A374, 6, 0x00C396, 0x00C39C, 0x00C3A4),
              (0x08A380, 3, 0x005134, 0x00513A, 0x00513E),
              (0x08A386, 3, 0x0051BA, 0x0051C0, 0x0051C4),
              (0x08A38C, 26, 0x00B28E, 0x00B298, 0x00B29C),
              (0x08A3C0, 1, 0x00B2F0, 0x00B2FA, 0x00B2FE),
              (0x08A3C2, 10, 0x00B352, 0x00B35C, 0x00B360),
              (0x08A430, 4, 0x00CD2C, 0x00CD36, 0x00CD3A),
              (0x08A438, 6, 0x0007C0, 0x0007D2, 0x0007D6),
              (0x08A444, 9, 0x0006AA, 0x0006BC, 0x0006C0),
              (0x08A456, 6, 0x0006EE, 0x00070E, 0x000712),
              (0x08A46A, 6, 0x0055DC, 0x0055E6, 0x0055EA),
              (0x08A476, 5, 0x000C56, 0x000C68, 0x000C6C),
              (0x08A480, 16, 0x00DB6C, 0x00DB7E, 0x00DB82),
              (0x08A4A0, 6, 0x00DB9A, 0x00DBA4, 0x00DBA8))
BYTE_GROUP = (0x08A426, 0x08A430)
UNKNOWN = ((0x089EDC, 0x089EFC), (0x08A2B6, 0x08A374),
           (0x08A3D6, 0x08A426), (0x08A462, 0x08A46A), (0x08A4AC, 0x08A504))
READER_START = 0x00AE8A
READER_END = 0x00AF48
READER_SHA = reference_value(__name__, 'READER_SHA')
sha = shared.sha
dump = shared.dump
keys = shared.keys
uint = shared.uint


def ident(start, kind):
    return f"rom_{start:06X}_{kind}"


def metadata():
    return dict(format=FORMAT,
                canonical_source=dict(size=shared.ROM_SIZE, sha256=shared.ROM_SHA),
                confidence="confirmed_read_encoding_candidate_visual_role",
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def exact_list(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ": exact physical source count required")
    return value


def check(rom, address, raw, label):
    if rom[address:address + len(raw)] != raw:
        raise ValueError(label + ": original consumer bytes differ")


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != shared.ROM_SIZE or sha(rom) != shared.ROM_SHA:
        raise ValueError("canonical ROM bytes/size/identity required")
    if sha(rom[READER_START:READER_END]) != READER_SHA:
        raise ValueError("original complete counted WORD/BYTE font readers differ")
    for start, end, lea, count_pc, write, dbra, register in TILES:
        check(rom, lea, b"\x41\xf9" + start.to_bytes(4, "big"), "tile LEA")
        check(rom, count_pc, register.to_bytes(2, "big") + ((end - start) // 4 - 1).to_bytes(2, "big"), "tile LONG count")
        check(rom, write, bytes.fromhex("23d800c00000"), "tile VDP LONG write")
        counter = {0x303C: 0x51C8, 0x383C: 0x51CC, 0x363C: 0x51CB}[register]
        check(rom, dbra, counter.to_bytes(2, "big") + (write - dbra - 2).to_bytes(2, "big", signed=True), "tile DBRA")
    covered = set()
    for start, count, lea, load, call in WORD_READS:
        if lea is not None:
            check(rom, lea, b"\x41\xf9" + start.to_bytes(4, "big"), "font WORD LEA")
        check(rom, load, bytes.fromhex("363c") + (count - 1).to_bytes(2, "big"), "font D3 count")
        check(rom, call, bytes.fromhex("4eb90000ae8a"), "font WORD JSR")
        covered.update(range(start, start + 2 * count))
    expected = {p for start, end in WORD_GROUPS for p in range(start, end)}
    if covered != expected:
        raise ValueError("fixed WORD reads do not exactly cover physical source fields")
    # AE8A saves D4-D7/A2, not A0; the first25 WORDs leave A0 at08A1EE.
    check(rom, 0x00504A, bytes.fromhex("43f8d300363c00024eb90000ae8a"), "retained-A0 continuation")
    check(rom, 0x005370, bytes.fromhex("41f90008a42643f8" "d300363c00094eb90000af1e"), "font BYTE fixed read")


def glyph_cell(word):
    """AE8E BMI is procedural-cell selection, not text control dispatch."""
    uint(word, 65535, "complete counted font WORD")
    if word >= 0x8000:
        return dict(kind="procedural_cell", WORD=word)
    # AE8A zero-extends the computed offset and uses a LONG index, unlike the
    # separate main-dialogue signed-index reader. Preserve aliases/full WORD.
    offset = font.font16_offset(word)
    if offset + 32 > font.FONT16_END - font.FONT16_START:
        raise ValueError("glyph read outside existing physical16x16 bitmap catalog")
    return dict(kind="font16_bitmap", WORD=word)


def glyph_word(cell):
    keys(cell, {"kind", "WORD"}, "counted font cell")
    shared.same(cell, glyph_cell(cell["WORD"]), "counted font cell kind/WORD")
    return cell["WORD"]


def tile_topology(spec):
    start, end, lea, count_pc, write, dbra, _ = spec
    return dict(id=ident(start, "tiles"), start=start, end=end, source_LEA=lea,
                LONG_count_load=count_pc, VDP_LONG_write=write, DBRA=dbra,
                physical_tiles=(end - start) // 32, tile_width=8, tile_height=8,
                bits_per_pixel=4, source_LONGs=(end - start) // 4)


def word_topology(start, end):
    return dict(id=ident(start, "font_WORDs"), start=start, end=end, WORD_order="big",
                reader=0x00AE8A, physical_WORDs=(end - start) // 2,
                termination="caller_D3_plus_one_not_source_marker")


def byte_topology():
    start, end = BYTE_GROUP
    return dict(id=ident(start, "font_BYTEs"), start=start, end=end, reader=0x00AF1E,
                source_LEA=0x005370, D3_load=0x00537A, source_JSR=0x00537E,
                physical_BYTEs=end - start, termination="caller_D3_plus_one_not_source_marker")


def tile_pixels(raw):
    if type(raw) is not bytes or len(raw) != 32:
        raise ValueError("one complete32-byte physical tile required")
    return [[component for value in raw[y * 4:y * 4 + 4] for component in (value >> 4, value & 15)] for y in range(8)]


def tile_bytes(pixels):
    raw = bytearray()
    for row in exact_list(pixels, 8, "tile rows"):
        values = [uint(value, 15, "4bpp pixel index") for value in exact_list(row, 8, "tile columns")]
        raw.extend((values[x] << 4) | values[x + 1] for x in range(0, 8, 2))
    return bytes(raw)


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["tile_uploads"] = [dict(**tile_topology(spec), tiles=[dict(id=ident(p, "tile"),
        pixels=tile_pixels(rom[p:p + 32])) for p in range(spec[0], spec[1], 32)]) for spec in TILES]
    fields["font_WORD_sources"] = [dict(**word_topology(start, end),
        cells=[glyph_cell(int.from_bytes(rom[p:p + 2], "big")) for p in range(start, end, 2)]) for start, end in WORD_GROUPS]
    fields["font_BYTE_source"] = dict(**byte_topology(), glyph_indices=list(rom[BYTE_GROUP[0]:BYTE_GROUP[1]]))
    blocks(rom, fields)
    return fields


def fixed_row(row, fixed, mutable, label):
    keys(row, set(fixed) | set(mutable), label)
    for key, value in fixed.items():
        shared.same(row[key], value, label + "." + key)


def blocks(rom, fields):
    verify_rom(rom)
    fixed_row(fields, metadata(), {"tile_uploads", "font_WORD_sources", "font_BYTE_source"}, "package")
    result = []
    for row, spec in zip(exact_list(fields["tile_uploads"], 5, "tile uploads"), TILES):
        fixed = tile_topology(spec)
        fixed_row(row, fixed, {"tiles"}, "tile upload")
        raw = bytearray()
        for tile, p in zip(exact_list(row["tiles"], fixed["physical_tiles"], "tiles"), range(spec[0], spec[1], 32)):
            fixed_row(tile, dict(id=ident(p, "tile")), {"pixels"}, "tile")
            raw.extend(tile_bytes(tile["pixels"]))
        result.append(dict(id=row["id"], start=spec[0], end=spec[1], data=bytes(raw), role="candidate_fixed_VDP_4bpp_tile_upload"))
    for row, (start, end) in zip(exact_list(fields["font_WORD_sources"], 4, "font WORD groups"), WORD_GROUPS):
        fixed_row(row, word_topology(start, end), {"cells"}, "font WORD group")
        data = b"".join(glyph_word(cell).to_bytes(2, "big") for cell in exact_list(row["cells"], (end - start) // 2, "font cells"))
        result.append(dict(id=row["id"], start=start, end=end, data=data, role="candidate_counted_font16_source_WORDs"))
    row = fields["font_BYTE_source"]
    fixed_row(row, byte_topology(), {"glyph_indices"}, "font BYTE group")
    data = bytes(uint(index, 255, "font8 glyph BYTE index") for index in exact_list(row["glyph_indices"], 10, "font BYTE indices"))
    result.append(dict(id=row["id"], start=BYTE_GROUP[0], end=BYTE_GROUP[1], data=data, role="candidate_counted_font8_source_BYTEs"))
    result.sort(key=lambda row: row["start"])
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES or any(len(row["data"]) != row["end"] - row["start"] for row in result):
        raise ValueError("fixed1018-byte physical source cost differs")
    if any(a["end"] > b["start"] for a, b in zip(result, result[1:])):
        raise ValueError("overlapping physical source fields")
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def load_fields(data):
    return shared.load_json(data)


def schema(rom):
    fields = extract(rom)
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({key: fixed(item) for key, item in value.items()})
        return dict(type={str: "string", int: "integer"}[type(value)], const=value)
    def array(count, item):
        return dict(type="array", minItems=count, maxItems=count, items=item)
    def rows_schema(rows):
        return dict(type="array", prefixItems=rows, items=False, minItems=len(rows), maxItems=len(rows))
    pixel = dict(type="integer", minimum=0, maximum=15)
    tiles = []
    for row in fields["tile_uploads"]:
        properties = {key: fixed(value) for key, value in row.items() if key != "tiles"}
        properties["tiles"] = rows_schema([obj(dict(id=fixed(tile["id"]), pixels=array(8, array(8, pixel)))) for tile in row["tiles"]])
        tiles.append(obj(properties))
    cell = obj(dict(kind=dict(type="string", enum=["font16_bitmap", "procedural_cell"]), WORD=dict(type="integer", minimum=0, maximum=65535)))
    words = []
    for row in fields["font_WORD_sources"]:
        properties = {key: fixed(value) for key, value in row.items() if key != "cells"}
        properties["cells"] = array(len(row["cells"]), cell)
        words.append(obj(properties))
    byte_properties = {key: fixed(value) for key, value in fields["font_BYTE_source"].items() if key != "glyph_indices"}
    byte_properties["glyph_indices"] = array(10, dict(type="integer", minimum=0, maximum=255))
    properties = {key: fixed(value) for key, value in metadata().items()}
    properties.update(tile_uploads=rows_schema(tiles), font_WORD_sources=rows_schema(words), font_BYTE_source=obj(byte_properties))
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Runtime additionally checks exact source locations/cost, WORD sign-branch kinds and existing bitmap addresses. No source terminator, indexed-table domain or unread gap is adopted."
    return result


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom or any(image[start:end] != rom[start:end] for start, end in UNKNOWN):
        raise ValueError("whole-ROM serialized source roundtrip or unknown preservation differs")
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=10,
        VDP_tile_bytes=704, physical_tiles=22, counted_font_WORD_bytes=304, counted_font_WORDs=152,
        counted_font_BYTEs=10, whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        original_counted_readers=dict(start=READER_START, end=READER_END, sha256=READER_SHA,
            WORD_reader=0x00AE8E, negative_WORD_branch=0x00AED8, WORD_count_DBRA=0x00AECE,
            BYTE_reader=0x00AF24, BYTE_count_DBRA=0x00AF3E),
        fixed_WORD_reads=[dict(start=start, end=start + 2 * count, WORDs=count, source_LEA=lea,
            D3_load=load, source_JSR=call, retained_A0_continuation=lea is None) for start, count, lea, load, call in WORD_READS],
        additional_short_alias_upload=dict(source_LEA=0x00531A, start=0x08A0BC, end=0x08A0DC, extra_emit_bytes=0),
        font_WORD_kind_histogram={kind: sum(cell["kind"] == kind for row in fields["font_WORD_sources"] for cell in row["cells"])
                                  for kind in ("font16_bitmap", "procedural_cell")},
        source_negative_WORDs_are_procedural_not_terminators=True,
        font16_index_is_zero_extended_LONG_not_main_dialogue_signed_WORD=True,
        font_BYTES_are_counted_indices_not_terminated_ASCII=True,
        unknown_intervals=[list(span) for span in UNKNOWN], unknown_bytes_excluded=398,
        reused_implementation=["text_font.text_font_assets.font16_offset", "existing8x8 VDP4bpp pixel layout"],
        source_read_encoding_confidence="confirmed", visual_roles_confidence="candidate",
        Unicode_labels_added=0, independent_CPU_comparison=False, complete_renderer_reimplemented=False,
        port_timing_proven=False, natural_selector_domain_complete=False, edited_gameplay_safety="unknown")
    members = {"fields.json": dump(fields), "fields.schema.json": dump(schema(rom)), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}, independent_CPU_comparison=False))
    return members


def fresh_output(value):
    path = shared.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError("output must stay in build/bank08_display_resources or be the fresh formal generated directory")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "import", "verify"))
    parser.add_argument("--rom", default=str(DEFAULT_ROM))
    parser.add_argument("--fields", default=str(DEFAULT_FIELDS))
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    target = None
    if args.command != "verify":
        if args.output is None:
            raise ValueError("fresh output required")
        target = fresh_output(args.output)  # Output authority BEFORE input reads.
        if args.command == "import" and target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin required")
    elif args.output is not None:
        raise ValueError("verify does not write")
    rom = shared.read_bounded(args.rom, shared.ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            shared.put(target / name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES,
                      members={name: sha(data) for name, data in members.items()})
    else:
        fields = load_fields(shared.read_bounded(args.fields, shared.MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            shared.put(target, image)
        result = dict(path=None if target is None else str(target), sha256=sha(image), exact_canonical=image == rom, editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
