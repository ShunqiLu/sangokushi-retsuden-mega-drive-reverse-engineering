"""253 unique physical BYTEs consumed as original AE8A counted token WORDs.

201 BYTEs are conditional F65A input aliases; 52 BYTEs are six finite lists.
Only physical BYTEs are editable. Complete WORD/bitmap views read an edited
whole image and never overwrite the already-typed neighboring half-WORDs.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
OUTPUT_ROOT = ROOT / "build/counted_glyph_source_fields"
FORMAL_ROOT = ROOT / "analysis/counted_glyph_source_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-counted-glyph-source-physical-BYTE-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
EDITABLE_BYTES, ALIAS_BYTES, FINITE_BYTES = 253, 201, 52
ALIAS_BASE, ALIAS_START, ALIAS_END = 0x6BF0E, 0x63F0E, 0x73F0E
FONT_BASE = 0x8159C
RANGES = (
    (0x65DF1, 0x65DF3, reference_value(__name__, 'RANGES')),
    (0x6618F, 0x66199, reference_value(__name__, 'RANGES_2')),
    (0x661CA, 0x661D4, reference_value(__name__, 'RANGES_3')),
    (0x6683E, 0x6689E, reference_value(__name__, 'RANGES_4')),
    (0x66C10, 0x66C28, reference_value(__name__, 'RANGES_5')),
    (0x671B0, 0x671B6, reference_value(__name__, 'RANGES_6')),
    (0x67238, 0x6724E, reference_value(__name__, 'RANGES_7')),
    (0x67502, 0x6750A, reference_value(__name__, 'RANGES_8')),
    (0x67516, 0x6751E, reference_value(__name__, 'RANGES_9')),
    (0x676D6, 0x676DE, reference_value(__name__, 'RANGES_10')),
    (0x68C13, 0x68C14, reference_value(__name__, 'RANGES_11')),
    (0x6BF0E, 0x6BF12, reference_value(__name__, 'RANGES_12')),
    (0x6BF42, 0x6BF44, reference_value(__name__, 'RANGES_13')),
    (0x92C0A, 0x92C2A, reference_value(__name__, 'RANGES_14')),
    (0x119A4, 0x119AA, reference_value(__name__, 'RANGES_15')),
    (0x1665E, 0x16660, reference_value(__name__, 'RANGES_16')),
    (0x18844, 0x18848, reference_value(__name__, 'RANGES_17')),
    (0x33032, 0x33038, reference_value(__name__, 'RANGES_18')),
    (0xA4CA, 0xA4CC, reference_value(__name__, 'RANGES_19')),
)
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
# (source start, source end, original D3.W, original LEA PC, call PC)
FINITE_LISTS = ((0x92C0A, 0x92C2A, 15, 0x4A66, 0x4A74),
    (0x119A4, 0x119AA, 2, 0x11928, 0x1193A),
    (0x1665E, 0x16660, 0, 0x16630, 0x1663A),
    (0x18844, 0x18848, 1, 0x18814, 0x1881C),
    (0x33032, 0x33038, 2, 0x32FD8, 0x32FEA),
    (0xA4CA, 0xA4CC, 0, 0xA496, 0xA4A0))
CONSUMERS = (
    (0xAE8A, 0xAF1E, reference_value(__name__, 'CONSUMERS')),
    (0x5174, 0x518C, reference_value(__name__, 'CONSUMERS_2')),
    (0x4A66, 0x4A7A, reference_value(__name__, 'CONSUMERS_3')),
    (0x11928, 0x11940, reference_value(__name__, 'CONSUMERS_4')),
    (0x16630, 0x16640, reference_value(__name__, 'CONSUMERS_5')),
    (0x18814, 0x18822, reference_value(__name__, 'CONSUMERS_6')),
    (0x32FD8, 0x32FF0, reference_value(__name__, 'CONSUMERS_7')),
    (0xA496, 0xA4A6, reference_value(__name__, 'CONSUMERS_8')),
)
INSTRUCTIONS = ((0x5174, "3638f65a"), (0x5178, "e54b"), (0x517A, "41f90006bf0e"),
    (0x5180, "d0c3"), (0x5182, "363c0001"), (0x5186, "4eb90000ae8a"),
    (0xAE8E, "3818"), (0xAE90, "6b46"), (0xAE94, "0245ff00"), (0xAE98, "e74d"),
    (0xAE9A, "024400ff"), (0xAE9E, "eb4c"), (0xAEA0, "8845"), (0xAEA2, "02840000ffff"),
    (0xAEA8, "45f90008159c"), (0xAEAE, "45f24800"), (0xAEB2, "3a3c000f"),
    (0xAEB6, "6100004c"), (0xAEBC, "61000046"), (0xAEC6, "51cdffee"),
    (0xAECE, "51cbffbe"), (0xAF02, "60c6"), (0xAF06, "1c1a"),
    (0x4A66, "41f900092c0a"), (0x4A70, "363c000f"), (0x4A74, "4eb90000ae8a"),
    (0x11928, "41fa007a"), (0x11936, "363c0002"), (0x1193A, "4eb90000ae8a"),
    (0x16630, "41fa002c"), (0x16638, "4243"), (0x1663A, "4eb90000ae8a"),
    (0x18814, "41fa002e"), (0x18818, "363c0001"), (0x1881C, "4eb90000ae8a"),
    (0x32FD8, "41fa0058"), (0x32FE6, "363c0002"), (0x32FEA, "4eb90000ae8a"),
    (0xA496, "41fa0032"), (0xA49C, "363c0000"), (0xA4A0, "4eb90000ae8a"))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = "build/direct_code/night-gnu-2ai3zu8p/layout-canonical/" + LAYOUT_ID
LAYOUT_BANKS = ((0, reference_value(__name__, 'LAYOUT_BANKS')),
    (1, reference_value(__name__, 'LAYOUT_BANKS_2')),
    (3, reference_value(__name__, 'LAYOUT_BANKS_3')),
    (6, reference_value(__name__, 'LAYOUT_BANKS_4')),
    (9, reference_value(__name__, 'LAYOUT_BANKS_5')))
MAP_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
MAP_SHA256 = reference_value(__name__, 'MAP_SHA256')
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical complete ROM bytes, size and SHA-256 required")
    for start, end, expected in (*CONSUMERS, *RANGES):
        if sha(rom[start:end]) != expected:
            raise ValueError("pinned original consumer/source differs")


def _image(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic requires complete bytes image; edited images are allowed")


def signed_WORD(word):
    word = uint(word, 65535, "complete WORD")
    return word if word < 0x8000 else word - 65536


def alias_start(F65A_WORD):
    word = uint(F65A_WORD, 65535, "complete supplied RAM F65A WORD")
    return ALIAS_BASE + signed_WORD((word << 2) & 65535)


def glyph_offset_WORD(token_WORD):
    word = uint(token_WORD, 65535, "complete token WORD")
    return (((word & 0xFF00) << 3) & 65535) | ((word & 255) << 5)


def _inside(address):
    return any(s <= address < e for s, e, _ in RANGES)


def token_view(image, address):
    """One original source WORD and its fill/glyph path, not an emulator."""
    _image(image)
    address = uint(address, ROM_SIZE-2, "original WORD source address")
    if address & 1:
        raise ValueError("original 68000 WORD read has odd address boundary")
    source = image[address:address+2]
    word = int.from_bytes(source, "big")
    result = dict(start=address, end=address+2, token_WORD=word, source_BYTEs=list(source),
        editable_source_BYTES=sum(_inside(a) for a in range(address, address+2)),
        read_only_view=True, token_consumed_even_if_negative=True, token_is_terminator=False)
    if word & 0x8000:
        return dict(**result, path="negative_fill", glyph_source_BYTES=0)
    offset = glyph_offset_WORD(word)
    start = FONT_BASE + offset
    return dict(**result, path="nonnegative_glyph", offset_WORD=offset, zeroextended_offset_LONG=offset,
        glyph_start=start, glyph_end=start+32, glyph_source_BYTES=32,
        glyph_source_BYTEs=list(image[start:start+32]))


def lookup(image, F65A_WORD):
    """Original 05174 caller's two WORD reads, with low-WORD wrap then sign."""
    _image(image)
    word = uint(F65A_WORD, 65535, "complete supplied RAM F65A WORD")
    offset = (word << 2) & 65535
    start = alias_start(word)
    return dict(F65A_WORD=word, shifted_offset_WORD=offset, signed_offset=signed_WORD(offset),
        start=start, end=start+4, D3_WORD=1, source_WORD_reads=2,
        source_BYTEs=list(image[start:start+4]),
        editable_source_BYTES=sum(_inside(a) for a in range(start, start+4)),
        tokens=[token_view(image, start), token_view(image, start+2)], physical_catalog_CPU_clamp=False)


def list_lookup(image, list_index):
    """One of six original fixed callers; index selects diagnostics, not CPU."""
    _image(image)
    index = uint(list_index, len(FINITE_LISTS)-1, "fixed diagnostic caller index")
    start, end, count, lea, call = FINITE_LISTS[index]
    return dict(list_index=index, start=start, end=end, D3_WORD=count, source_WORD_reads=count+1,
        original_LEA=lea, original_call=call, source_BYTEs=list(image[start:end]),
        tokens=[token_view(image, address) for address in range(start, end, 2)],
        is_counted_not_terminated=True, raw_tail_not_reader_stop=True)


def source_fixed(index):
    start, end, _ = RANGES[index]
    return dict(id=f"rom_{start:06X}_counted_token_source_BYTEs", start=start, end=end, bytes=end-start,
        role="conditional_F65A_token_source_alias" if index < 13 else "finite_counted_token_list")


def witnesses_for_source(ROM_address):
    address = uint(ROM_address, ROM_SIZE-1, "physical source BYTE address")
    for index, (start, end, _) in enumerate(RANGES):
        if start <= address < end:
            if index < 13:
                word = ((address-ALIAS_BASE)//4) & 0x3FFF
                source = alias_start(word)
                slot = address-source
                return dict(kind="conditional_F65A", F65A_WORD=word, start=source, end=source+4,
                    WORD_index=slot//2, WORD_BYTE=slot%2, source_BYTE_index=slot)
            source, _, count, lea, call = FINITE_LISTS[index-13]
            slot = address-source
            return dict(kind="finite_list", list_index=index-13, start=source,
                end=source+2*(count+1), original_LEA=lea, original_call=call,
                WORD_index=slot//2, WORD_BYTE=slot%2, source_BYTE_index=slot)
    raise ValueError("address outside unique new physical source ranges")


def audit_witness_union(rom):
    verify_rom(rom)
    source = {a for s, e, _ in RANGES for a in range(s, e)}
    if len(source) != EDITABLE_BYTES or sum(e-s for s, e, _ in RANGES) != EDITABLE_BYTES:
        raise ValueError("physical source union must be disjoint and exact")
    starts = {alias_start(w) for w in range(65536)}
    if starts != set(range(ALIAS_START, ALIAS_END, 4)):
        raise ValueError("full WORD construction/read union differs")
    for address in source:
        witness = witnesses_for_source(address)
        if not witness["start"] <= address < witness["end"] or witness["start"] < 0 or witness["end"] > ROM_SIZE:
            raise ValueError("physical BYTE lacks a complete in-ROM original read witness")
        if witness["start"] + witness["source_BYTE_index"] != address:
            raise ValueError("source witness BYTE position differs")
    if any(end-start != 2*(count+1) for start, end, count, _, _ in FINITE_LISTS):
        raise ValueError("finite counted WORD read extent differs")
    return dict(physical_editable_BYTES=253, conditional_source_BYTES=201, finite_source_BYTES=52,
        distinct_complete_alias_windows=16384, complete_alias_window_BYTES=4,
        complete_alias_read_union_BYTES=65536, finite_source_WORDs=26,
        physical_unwitnessed_BYTES=0, unique_editing_authority=True, typed_neighbors_emitted_again=False)


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=[dict(**source_fixed(i), source_sha256=h) for i, (_, _, h) in enumerate(RANGES)],
        source_union_BYTES=EDITABLE_BYTES, source_union_sha256=SOURCE_SHA256,
        serialization="one full BYTE per physical address; complete WORD/bitmap views are read-only",
        evidence=dict(consumers=[dict(start=s, end=e, bytes=e-s, sha256=h) for s, e, h in CONSUMERS],
            instructions=[dict(address=a, bytes=b) for a, b in INSTRUCTIONS],
            original_map=dict(path=MAP_PATH, sha256=MAP_SHA256),
            frozen_raw_layout=dict(id=LAYOUT_ID, path=LAYOUT_PATH,
                banks=[dict(bank=b, sha256=h) for b, h in LAYOUT_BANKS],
                snapshot_resources=75, snapshot_raw_BYTES=45219, source_raw_difference_BYTES=253,
                existing_typed_overlap_emitted_BYTES=0),
            conditional_caller=dict(start=0x5174, RAM_WORD=0xFFF65A, shift_WORD=0x5178,
                base=ALIAS_BASE, ADDA_WORD=0x5180, formula="6BF0E + s16((F65A_WORD << 2) & FFFF)",
                D3_WORD=1, call=0x5186, full_WORD_inputs=65536, distinct_complete_windows=16384,
                read_union_start=ALIAS_START, read_union_end=ALIAS_END, all_reads_in_ROM=True,
                physical_edit_catalog_not_CPU_clamp=True, constructed_input_not_natural_domain=True,
                source_input_domain_writer_closure="unknown"),
            finite_callers=[dict(start=s, end=e, D3_WORD=n, source_WORD_reads=n+1, original_LEA=l, original_call=c)
                for s, e, n, l, c in FINITE_LISTS],
            renderer=dict(entry=0xAE8A, source_WORD_read=0xAE8E, endian="big", source_step_BYTES=2,
                outer_count="D3.W + 1 WORDs, including bit15-set fill tokens", DBRA=0xAECE,
                negative_branch=0xAE90, negative_is_fill_not_terminator=True, negative_reads_bitmap=False,
                fill_returns_to_outer_count=0xAF02, nonnegative_WORD=[0, 0x7FFF],
                glyph_offset="(((WORD & FF00)<<3) & FFFF) | ((WORD & 00FF)<<5)",
                final_offset_zeroextend=0xAEA2, glyph_LEA_LONG=0xAEAE, glyph_base=FONT_BASE,
                bitmap_BYTE_read=0xAF06, per_row_calls=[0xAEB6, 0xAEBC], rows=16, row_BYTES=2,
                bitmap_BYTES=32, catalog_extent_is_CPU_clamp=False),
            witness_starts=[witnesses_for_source(s) for s, _, _ in RANGES],
            neighbor_WORD_halves_preserved=True, no_font_bitmap_source_emitted=True,
            signed_main_dialogue_is_separate=True, inferred_padding=False, new_officer257=False),
        natural_F65A_selection="unknown", natural_token_values="unknown", Unicode_identity="unknown",
        complete_text_algorithm=False, independent_CPU_comparison=False)


def extract(rom):
    verify_rom(rom)
    audit_witness_union(rom)
    return dict(**metadata(), sources=[dict(**source_fixed(i), source_BYTEs=list(rom[s:e]))
        for i, (s, e, _) in enumerate(RANGES)])


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"sources"}, "counted source fields")
    for key, expected in fixed.items():
        same(fields[key], expected, "counted source fields." + key)
    result = []
    for index, value in enumerate(exact_list(fields["sources"], len(RANGES), "fixed physical source range count")):
        row = source_fixed(index)
        keys(value, set(row) | {"source_BYTEs"}, "fixed physical source")
        for key, expected in row.items():
            same(value[key], expected, "fixed physical source." + key)
        data = bytes(uint(v, 255, "complete source BYTE") for v in
            exact_list(value["source_BYTEs"], row["bytes"], "fixed source BYTE count"))
        result.append(dict(id=row["id"], start=row["start"], end=row["end"], data=data, role=row["role"]))
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES:
        raise ValueError("fixed source union length differs")
    return result


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def schema():
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({k: fixed(v) for k, v in value.items()})
        if type(value) is list:
            return dict(type="array", prefixItems=[fixed(v) for v in value], items=False, minItems=len(value), maxItems=len(value))
        return dict(type={str: "string", int: "integer", bool: "boolean"}[type(value)], const=value)
    rows = [obj({**{k: fixed(v) for k, v in source_fixed(i).items()},
        "source_BYTEs": dict(type="array", minItems=e-s, maxItems=e-s,
            items=dict(type="integer", minimum=0, maximum=255))}) for i, (s, e, _) in enumerate(RANGES)]
    result = obj({**{k: fixed(v) for k, v in metadata().items()},
        "sources": dict(type="array", prefixItems=rows, items=False, minItems=19, maxItems=19)})
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "253 complete physical source BYTEs; original complete WORD views are read-only."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("serialized whole-ROM roundtrip differs")
    encoded = blocks(rom, fields)
    witness_words = sorted({witnesses_for_source(a)["F65A_WORD"] for s, e, _ in RANGES[:13] for a in range(s, e)})
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=19,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), witness_union=audit_witness_union(rom),
        complete_alias_views=[lookup(rom, word) for word in witness_words],
        finite_list_views=[list_lookup(rom, i) for i in range(6)],
        blocks=[{k: v for k, v in row.items() if k != "data"} |
            dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=19,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in counted_glyph_source_fields build scope or exact formal bundle")
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
            raise ValueError("export requires fresh output only")
        target = fresh_output(args.output, bundle=True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None:
            raise ValueError("import requires fields and fresh output")
        target = fresh_output(args.output)
        if target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom = read_bounded(args.rom, ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            put(target/name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES, members={name: sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name, data in render_bundle(rom).items():
            if read_bounded(bundle/name, MAX_JSON) != data:
                raise ValueError("canonical bundle drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=EDITABLE_BYTES, whole_ROM_exact=True, whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=EDITABLE_BYTES,
            bytes=len(image), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
