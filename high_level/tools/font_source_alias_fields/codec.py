"""574 unique source BYTEs read conditionally by the original AE8A renderer.

22 complete 32-BYTE glyph witnesses include 130 already-typed neighboring
BYTEs. Only five original raw ranges are editable/emitted here. The different
main-dialogue signed-WORD consumer is kept separate, not used as this proof.
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
OUTPUT_ROOT = ROOT / "build/font_source_alias_fields"
FORMAL_ROOT = ROOT / "analysis/font_source_alias_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-positive-glyph-font-alias-physical-BYTE-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
EDITABLE_BYTES, GLYPH_SOURCE_BYTES, ALIAS_COUNT = 574, 32, 22
FONT_BASE = 0x8159C
RANGES = (
    (0x89EDC, 0x89EFC, reference_value(__name__, 'RANGES')),
    (0x8A2B6, 0x8A374, reference_value(__name__, 'RANGES_2')),
    (0x8A462, 0x8A46A, reference_value(__name__, 'RANGES_3')),
    (0x8A4AC, 0x8A504, reference_value(__name__, 'RANGES_4')),
    (0x8AB04, 0x8AC04, reference_value(__name__, 'RANGES_5')),
)
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
WITNESS_WORDS = (0x110A, *range(0x1128, 0x112F), 0x1136, *range(0x1138, 0x113C), *range(0x122B, 0x1234))
NEIGHBORS = ((0x8A29C, 0x8A2B6), (0x8A374, 0x8A37C), (0x8A45C, 0x8A462), (0x8A46A, 0x8A47C),
             (0x8A49C, 0x8A4AC), (0x8A504, 0x8A51C), (0x8AAFC, 0x8AB04), (0x8AC04, 0x8AC1C))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = "build/direct_code/layout/" + LAYOUT_ID + "/m68k_bank08.s"
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
MAP_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
MAP_SHA256 = reference_value(__name__, 'MAP_SHA256')
OLD_FONT_PATH = "tools/text_font/text_font_assets.py"
OLD_FONT_SHA256 = reference_value(__name__, 'OLD_FONT_SHA256')
CONSUMERS = (
    (0xAE8A, 0xAF1E, reference_value(__name__, 'CONSUMERS')),
    (0x28A9E, 0x28B98, reference_value(__name__, 'CONSUMERS_2')),
    (0x3FFAA, 0x40076, reference_value(__name__, 'CONSUMERS_3')),
    (0x671CA, 0x6722A, reference_value(__name__, 'CONSUMERS_4')),
    (0x6738C, 0x673A6, reference_value(__name__, 'CONSUMERS_5')),
)
INSTRUCTIONS = (
    (0xAE8E, "3818"), (0xAE90, "6b46"), (0xAE92, "3a04"), (0xAE94, "0245ff00"),
    (0xAE98, "e74d"), (0xAE9A, "024400ff"), (0xAE9E, "eb4c"), (0xAEA0, "8845"),
    (0xAEA2, "02840000ffff"), (0xAEA8, "45f90008159c"), (0xAEAE, "45f24800"),
    (0xAEB2, "3a3c000f"), (0xAEB6, "6100004c"), (0xAEBC, "61000046"),
    (0xAEC6, "51cdffee"), (0xAECE, "51cbffbe"), (0xAF06, "1c1a"),
    (0x28AD0, "207900ff700e"), (0x28AD6, "3010"), (0x28ADE, "0c40ff00"),
    (0x28AEA, "0c40ff01"), (0x28AF6, "0c40ff02"), (0x28B02, "0c40ff03"),
    (0x28B06, "661c"), (0x28B34, "363c0000"), (0x28B38, "4eb90000ae8a"),
    (0x3FFCE, "207900ff700e"), (0x3FFD4, "3010"), (0x3FFD6, "0240bfff"),
    (0x4003E, "0800000f"), (0x40042, "66000048"), (0x40056, "363c0000"), (0x4005A, "4eb90000ae8a"),
    (0x671D2, "3010"), (0x671D8, "6730"), (0x671DA, "6b4e"), (0x671E8, "610001a2"),
    (0x6738C, "3200"), (0x6738E, "0241ff00"), (0x67392, "e749"),
    (0x67394, "024000ff"), (0x67398, "eb48"), (0x6739A, "8041"),
    (0x6739C, "45f90008159c"), (0x673A2, "45f20000"),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical complete ROM bytes, size and SHA-256 required")
    for start, end, expected in (*CONSUMERS, *RANGES):
        if sha(rom[start:end]) != expected:
            raise ValueError("pinned original consumer/physical source differs")


def offset_WORD(glyph_WORD):
    value = uint(glyph_WORD, 65535, "complete original glyph WORD")
    return (((value & 0xFF00) << 3) & 65535) | ((value & 255) << 5)


def _inside(address):
    return any(start <= address < end for start, end, _ in RANGES)


def witness_fixed(word):
    offset = offset_WORD(word)
    start = FONT_BASE + offset
    return dict(glyph_WORD=word, offset_WORD=offset, start=start, end=start+32,
        source_BYTE_reads=32, editable_source_BYTES=sum(_inside(a) for a in range(start, start+32)))


def source_fixed(start, end):
    return dict(id=f"rom_{start:06X}_font_source_BYTEs", start=start, end=end, bytes=end-start)


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=[dict(**source_fixed(s, e), source_sha256=h) for s, e, h in RANGES],
        serialization="one complete editable source BYTE per physical address; no glyph/row second authority",
        source_union_BYTES=EDITABLE_BYTES, source_union_sha256=SOURCE_SHA256,
        glyph_witnesses=[witness_fixed(w) for w in WITNESS_WORDS],
        already_typed_neighbor_aliases=[dict(start=s, end=e, bytes=e-s, emitted_again=False) for s, e in NEIGHBORS],
        preview_rows_are_read_only=True,
        evidence=dict(consumers=[dict(start=s, end=e, bytes=e-s, sha256=h) for s, e, h in CONSUMERS],
            instructions=[dict(address=a, bytes=b, source_confidence="original_enhanced_CFG_row") for a, b in INSTRUCTIONS],
            original_map=dict(path=MAP_PATH, sha256=MAP_SHA256),
            old_font_formula=dict(path=OLD_FONT_PATH, sha256=OLD_FONT_SHA256, editor_glyph_count_not_CPU_clamp=True),
            frozen_raw_layout=dict(id=LAYOUT_ID, path=LAYOUT_PATH, sha256=LAYOUT_SHA256, bank=8,
                snapshot_resources=52, snapshot_raw_BYTES=49595, raw_difference_BYTES=574,
                typed_neighbor_BYTES=130, typed_source_overlap_BYTES=0),
            renderer=dict(entry=0xAE8A, token_read=0xAE8E, bit15_branch=0xAE90,
                permitted_glyph_WORD=[0, 0x7FFF], negative_WORDs_read_no_bitmap=True,
                offset_formula="(((WORD & FF00)<<3) & FFFF) | ((WORD & 00FF)<<5)",
                shifts_are_WORD_width=True, zeroextend_ANDI_LONG=0xAEA2, index_LEA_LONG=0xAEAE,
                original_base=FONT_BASE, original_font_physical_end=0x896DC, old_font_end_is_CPU_clamp=False,
                per_glyph_source_BYTE_read=0xAF06, per_row_calls=[0xAEB6, 0xAEBC], rows=16,
                row_BYTES=2, original_reader_unit="BYTE, not eight LONG reads", DBRA_rows=0xAEC6,
                glyph_source_BYTES=32, glyph_output_BYTES=128, MSB_left=True,
                source_address_union_start=0x8159C, source_address_union_end=0x9159C,
                distinct_offset_WORDs=2048, all_source_reads_in_ROM=True),
            callers=[dict(call=0x28B38, stream_RAM_pointer=0xFF700E, reload_A0=0x28AD0,
                token_check=0x28AD6, controls_compared=[0xFF00, 0xFF01, 0xFF02, 0xFF03], D3_WORD=0,
                glyph_catalog_CPU_clamp=False, reachability_confidence="heuristic_original_CFG"),
                dict(call=0x4005A, stream_RAM_pointer=0xFF700E, reload_A0=0x3FFCE,
                token_check=0x3FFD4, check_copy_AND_BFFF=0x3FFD6, bit15_guard=0x4003E, D3_WORD=0,
                renderer_reloads_original_WORD=True, glyph_catalog_CPU_clamp=False,
                reachability_confidence="heuristic_original_CFG")],
            signed_main_dialogue=dict(entry_token_read=0x671D2, zero_branch=0x671D8, negative_branch=0x671DA,
                permitted_positive_glyph_WORD=[1, 0x7FFF], zero_is_special_fixed_bitmap=True,
                original_font_LEA_WORD=0x673A2, same_offset_WORD_but_signed_index=True,
                source_union_start=0x7959C, source_union_end=0x8959C, snapshot_raw_difference_BYTES=0,
                proves_new_8AB04_source=False, example_WORD=0x122B, signed_source_start=0x7AAFC,
                independent_from_AE8A=True),
            witness_summary=dict(complete_32_BYTE_witnesses=22, source_read_union_BYTES=704,
                new_physical_raw_BYTES=574, preserved_neighbor_alias_BYTES=130,
                all_witness_WORDs_bit15_clear=True, all_witness_low_BYTEs_at_most_3F=True,
                input_construction_is_not_natural_domain=True),
            officer_name_extension=False, officer257_claim=False, contents_are_not_shape_padding=True),
        natural_glyph_selection="unknown", Unicode_character_identity="unknown", complete_font_domain="unknown",
        independent_CPU_comparison=False, complete_text_algorithm=False)


def lookup(image, glyph_WORD):
    """One original AE8A nonnegative glyph read from an edited whole image."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic requires a complete bytes image")
    word = uint(glyph_WORD, 65535, "complete original glyph WORD")
    if word & 0x8000:
        raise ValueError("AE90 negative/control path reads no glyph bitmap")
    fixed = witness_fixed(word)
    raw = image[fixed["start"]:fixed["end"]]
    if len(raw) != 32:
        raise ValueError("original complete glyph source leaves mapped ROM")
    return dict(**fixed, source_BYTEs=list(raw), row_bits_MSB_left=[f"{int.from_bytes(raw[i:i+2], 'big'):016b}" for i in range(0, 32, 2)],
        already_typed_or_other_source_BYTES=32-fixed["editable_source_BYTES"],
        inside_edit_scope=fixed["editable_source_BYTES"] == 32, preview_is_editing_authority=False)


def witnesses_for_source(ROM_address):
    address = uint(ROM_address, ROM_SIZE-1, "physical ROM address")
    if not _inside(address):
        raise ValueError("address outside unique new physical source ranges")
    result = []
    for word in WITNESS_WORDS:
        fixed = witness_fixed(word)
        if fixed["start"] <= address < fixed["end"]:
            index = address-fixed["start"]
            result.append(dict(glyph_WORD=word, ROM_address=address, source_BYTE_index=index,
                               row=index//2, row_BYTE=index%2))
    return result


def audit_witness_union(rom):
    verify_rom(rom)
    source = {a for s, e, _ in RANGES for a in range(s, e)}
    witnessed = set()
    for word in WITNESS_WORDS:
        view = lookup(rom, word)
        if word & 0x8000 or view["end"]-view["start"] != 32:
            raise ValueError("fixed positive glyph witness does not read complete source")
        witnessed.update(range(view["start"], view["end"]))
    neighbors = {a for s, e in NEIGHBORS for a in range(s, e)}
    if len(source) != EDITABLE_BYTES or len(WITNESS_WORDS) != ALIAS_COUNT or source | neighbors != witnessed or source & neighbors:
        raise ValueError("fixed raw/witness/old-typed alias difference differs")
    return dict(complete_32_BYTE_witnesses=22, distinct_source_BYTES=len(witnessed),
                physical_editable_BYTES=len(source), already_typed_neighbor_BYTES=len(neighbors),
                physical_unwitnessed_BYTES=len(source-witnessed), unique_editing_authority=True,
                old_neighbors_emitted_again=False)


def extract(rom):
    verify_rom(rom)
    audit_witness_union(rom)
    return dict(**metadata(), sources=[dict(**source_fixed(s, e), source_BYTEs=list(rom[s:e])) for s, e, _ in RANGES])


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"sources"}, "physical font source fields")
    for key, expected in fixed.items():
        same(fields[key], expected, "physical font source fields." + key)
    result = []
    for value, (start, end, _) in zip(exact_list(fields["sources"], 5, "fixed source range count"), RANGES):
        row = source_fixed(start, end)
        keys(value, set(row) | {"source_BYTEs"}, "fixed physical source range")
        for key, expected in row.items():
            same(value[key], expected, "fixed physical source range." + key)
        data = bytes(uint(v, 255, "complete source BYTE") for v in exact_list(value["source_BYTEs"], end-start, "fixed source BYTE count"))
        result.append(dict(id=row["id"], start=start, end=end, data=data, role="conditional_original_1bpp_font_source_alias_BYTEs"))
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
    rows = [obj({**{k: fixed(v) for k, v in source_fixed(s, e).items()},
                 "source_BYTEs": dict(type="array", minItems=e-s, maxItems=e-s, items=dict(type="integer", minimum=0, maximum=255))}) for s, e, _ in RANGES]
    result = obj({**{k: fixed(v) for k, v in metadata().items()},
        "sources": dict(type="array", prefixItems=rows, items=False, minItems=5, maxItems=5)})
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "574 complete physical source BYTEs; glyph and MSB-left row previews are not editing authority."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("serialized whole-ROM roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=5,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), witness_union=audit_witness_union(rom),
        glyph_alias_examples=[lookup(rom, w) for w in (0x110A, 0x1128, 0x1136, 0x1138, 0x122B, 0x1233, 0x522B)],
        blocks=[{k: v for k, v in row.items() if k != "data"} | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=5,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in font_source_alias_fields build scope or exact formal bundle")
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
