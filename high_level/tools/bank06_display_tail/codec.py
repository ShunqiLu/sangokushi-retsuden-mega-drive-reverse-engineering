"""676 source bytes recovered from the682-byte tail06BF0A..06C1B4.

Four original A1 VDP-copy loops read512 bytes/16 tiles. Ten fixed AE8A calls
read82 complete WORDs/164 bytes. Two unproved gaps totaling6 bytes remain raw.
Counted font-WORD semantics/pixel helpers are reused from the frozen bank08
package; no old scope, whole renderer or independent CPU claim is extended.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.vdp_word_streams import format as shared
from tools.bank08_display_resources import codec as display

DEFAULT_ROM = shared.DEFAULT_ROM
FORMAL_ROOT = ROOT / "analysis/bank06_display_tail/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
OUTPUT_ROOT = ROOT / "build/bank06_display_tail"
FORMAT = "candidate-bank06-fixed-display-tail-fields-v1"
EDITABLE_BYTES = 676
# Source start/end, A1 LEA, count load, VDP write, DBRA, count opcode.
TILES = ((0x06BF6E, 0x06C02E, 0x0178E6, 0x0178EC, 0x0178F0, 0x0178F6, 0x363C),
         (0x06C02E, 0x06C0AE, 0x01795A, 0x017960, 0x017964, 0x01796A, 0x323C),
         (0x06C0E8, 0x06C168, 0x01796E, 0x017974, 0x017978, 0x01797E, 0x323C),
         (0x06C174, 0x06C1B4, 0x0178C8, 0x0178CE, 0x0178D2, 0x0178D8, 0x363C))
WORD_GROUPS = ((0x06BF0A, 0x06BF0E), (0x06BF12, 0x06BF42), (0x06BF44, 0x06BF6E),
               (0x06C0AE, 0x06C0E8), (0x06C168, 0x06C174))
# source, WORD count, source LEA, D3 count load, JSR.
WORD_READS = ((0x06BF0A, 2, 0x000B64, 0x000B72, 0x000B76),
              (0x06BF12, 20, 0x000BCA, 0x000BD0, 0x000BD4),
              (0x06BF3A, 3, 0x000AAE, 0x000AC0, 0x000AC4),
              (0x06BF40, 1, 0x000AD8, 0x000ADE, 0x000AE2),
              (0x06BF44, 10, 0x000BF2, 0x000BFC, 0x000C00),
              (0x06BF58, 11, 0x0177DA, 0x0177EC, 0x0177F0),
              (0x06C0AE, 12, 0x017A1A, 0x017A2C, 0x017A30),
              (0x06C0C6, 12, 0x017A5E, 0x017A70, 0x017A74),
              (0x06C0DE, 5, 0x017EDE, 0x017EEC, 0x017EF4),
              (0x06C168, 6, 0x018768, 0x018764, 0x01876E))
UNKNOWN = ((0x06BF0E, 0x06BF12), (0x06BF42, 0x06BF44))
sha = shared.sha
dump = shared.dump
keys = shared.keys
uint = shared.uint
glyph_cell = display.glyph_cell
glyph_word = display.glyph_word
tile_pixels = display.tile_pixels
tile_bytes = display.tile_bytes
exact_list = display.exact_list


def ident(start, kind):
    return f"rom_{start:06X}_{kind}"


def metadata():
    return dict(format=FORMAT,
                canonical_source=dict(size=shared.ROM_SIZE, sha256=shared.ROM_SHA),
                confidence="confirmed_read_encoding_candidate_visual_role",
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def check(rom, address, raw, label):
    if rom[address:address + len(raw)] != raw:
        raise ValueError(label + ": original consumer bytes differ")


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != shared.ROM_SIZE or sha(rom) != shared.ROM_SHA:
        raise ValueError("canonical ROM bytes/size/identity required")
    if sha(rom[display.READER_START:display.READER_END]) != display.READER_SHA:
        raise ValueError("shared original counted-font reader differs")
    for start, end, lea, load, write, dbra, register in TILES:
        check(rom, lea, b"\x43\xf9" + start.to_bytes(4, "big"), "tile A1 LEA")
        check(rom, load, register.to_bytes(2, "big") + ((end - start) // 4 - 1).to_bytes(2, "big"), "tile LONG count")
        check(rom, write, bytes.fromhex("23d900c00000"), "A1 VDP LONG write")
        counter = {0x323C: 0x51C9, 0x363C: 0x51CB}[register]
        check(rom, dbra, counter.to_bytes(2, "big") + (write - dbra - 2).to_bytes(2, "big", signed=True), "tile DBRA")
    covered = set()
    for start, count, lea, load, call in WORD_READS:
        check(rom, lea, b"\x41\xf9" + start.to_bytes(4, "big"), "font WORD LEA")
        check(rom, load, bytes.fromhex("363c") + (count - 1).to_bytes(2, "big"), "font D3 count")
        check(rom, call, bytes.fromhex("4eb90000ae8a"), "font WORD JSR")
        covered.update(range(start, start + 2 * count))
    if covered != {p for start, end in WORD_GROUPS for p in range(start, end)}:
        raise ValueError("fixed WORD reads do not exactly cover source fields")


def tile_topology(spec):
    start, end, lea, load, write, dbra, _ = spec
    return dict(id=ident(start, "tiles"), start=start, end=end, source_register="A1",
                source_LEA=lea, LONG_count_load=load, VDP_LONG_write=write, DBRA=dbra,
                physical_tiles=(end - start) // 32, source_LONGs=(end - start) // 4,
                tile_width=8, tile_height=8, bits_per_pixel=4)


def word_topology(start, end):
    return dict(id=ident(start, "font_WORDs"), start=start, end=end, WORD_order="big",
                reader=0x00AE8A, physical_WORDs=(end - start) // 2,
                termination="caller_D3_plus_one_not_source_marker")


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["tile_uploads"] = [dict(**tile_topology(spec), tiles=[dict(id=ident(p, "tile"),
        pixels=tile_pixels(rom[p:p + 32])) for p in range(spec[0], spec[1], 32)]) for spec in TILES]
    fields["font_WORD_sources"] = [dict(**word_topology(start, end),
        cells=[glyph_cell(int.from_bytes(rom[p:p + 2], "big")) for p in range(start, end, 2)]) for start, end in WORD_GROUPS]
    blocks(rom, fields)
    return fields


def fixed_row(row, fixed, mutable, label):
    keys(row, set(fixed) | set(mutable), label)
    for key, value in fixed.items():
        shared.same(row[key], value, label + "." + key)


def blocks(rom, fields):
    verify_rom(rom)
    fixed_row(fields, metadata(), {"tile_uploads", "font_WORD_sources"}, "package")
    result = []
    for row, spec in zip(exact_list(fields["tile_uploads"], 4, "tile uploads"), TILES):
        fixed = tile_topology(spec)
        fixed_row(row, fixed, {"tiles"}, "tile upload")
        data = bytearray()
        for tile, p in zip(exact_list(row["tiles"], fixed["physical_tiles"], "tiles"), range(spec[0], spec[1], 32)):
            fixed_row(tile, dict(id=ident(p, "tile")), {"pixels"}, "tile")
            data.extend(tile_bytes(tile["pixels"]))
        result.append(dict(id=row["id"], start=spec[0], end=spec[1], data=bytes(data), role="candidate_fixed_VDP_4bpp_tile_upload"))
    for row, (start, end) in zip(exact_list(fields["font_WORD_sources"], 5, "font WORD groups"), WORD_GROUPS):
        fixed_row(row, word_topology(start, end), {"cells"}, "font WORD group")
        data = b"".join(glyph_word(cell).to_bytes(2, "big") for cell in exact_list(row["cells"], (end - start) // 2, "font cells"))
        result.append(dict(id=row["id"], start=start, end=end, data=data, role="candidate_counted_font16_source_WORDs"))
    result.sort(key=lambda row: row["start"])
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES or any(len(row["data"]) != row["end"] - row["start"] for row in result):
        raise ValueError("fixed676-byte source cost differs")
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
    properties = {key: fixed(value) for key, value in metadata().items()}
    properties.update(tile_uploads=rows_schema(tiles), font_WORD_sources=rows_schema(words))
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Runtime additionally checks fixed source costs, counted-WORD sign branch and existing bitmap addresses. Unproved6-byte gaps and natural selector domains are not adopted."
    return result


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom or any(image[start:end] != rom[start:end] for start, end in UNKNOWN):
        raise ValueError("whole-ROM serialized source roundtrip or unknown preservation differs")
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=9,
        VDP_tile_bytes=512, physical_tiles=16, counted_font_WORD_bytes=164, counted_font_WORDs=82,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        original_counted_reader=dict(start=display.READER_START, end=display.READER_END, sha256=display.READER_SHA),
        fixed_WORD_reads=[dict(start=start, end=start + 2 * count, WORDs=count, source_LEA=lea,
            D3_load=load, source_JSR=call) for start, count, lea, load, call in WORD_READS],
        original_VDP_copy_source_register="A1", source_negative_WORDs_are_procedural_not_terminators=True,
        unknown_intervals=[list(span) for span in UNKNOWN], unknown_bytes_excluded=6,
        scope_container=[0x06BF0A, 0x06C1B4], source_WORDs_and_pixel_indices_not_Unicode=True,
        older_exclusions=["sprite_word_resources source counts ending06BF0A", "battlefield terrain allocation starting06C1B4"],
        reused_implementation=["bank08_display_resources.glyph_cell", "glyph_word", "tile_pixels", "tile_bytes"],
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
        raise ValueError("output must stay in build/bank06_display_tail or be the fresh formal generated directory")
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
