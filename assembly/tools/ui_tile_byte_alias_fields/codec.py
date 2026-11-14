"""36 original raw BYTEs read by the 4BDA indexed UI tile source consumer.

Input zero stops the outer source loop. Nonzero complete BYTE inputs and
original modes 0/4 construct complete four-BYTE source windows, without a
physical-catalog clamp. D4.W high-BYTE carry survives the next MOVE.B.
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
OUTPUT_ROOT = ROOT / "build/ui_tile_byte_alias_fields"
FORMAL_ROOT = ROOT / "analysis/ui_tile_byte_alias_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-ui-indexed-tile-physical-BYTE-alias-fields-v1"
EDITABLE_BYTES = 36
SOURCE_BASE, UNION_START, UNION_END = 0x92C26, 0x92A26, 0x92E26
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
RANGES = ((0x92C2A, 0x92C4A, reference_value(__name__, 'RANGES')),
    (0x92C52, 0x92C56, reference_value(__name__, 'RANGES_2')))
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
CONSUMERS = ((0x4B28, 0x4B5A, reference_value(__name__, 'CONSUMERS')),
    (0x4B5A, 0x4B7A, reference_value(__name__, 'CONSUMERS_2')),
    (0x4B7A, 0x4C1A, reference_value(__name__, 'CONSUMERS_3')),
    (0x4C1A, 0x4C34, reference_value(__name__, 'CONSUMERS_4')))
INSTRUCTIONS = ((0x4B34, "4247"), (0x4B36, "43f8f580"), (0x4B3A, "4a317000"),
    (0x4B3E, "670c"), (0x4B44, "61000034"), (0x4B7E, "4245"),
    (0x4B80, "3238f372"), (0x4B84, "e349"), (0x4B86, "47f8c000"),
    (0x4B8A, "3c331000"), (0x4B8E, "47f8be00"), (0x4B92, "bc731000"),
    (0x4B96, "64000006"), (0x4B9A, "3a3c0004"), (0x4B9E, "1219"),
    (0x4BA0, "d205"), (0x4BA4, "4881"), (0x4BA6, "e549"),
    (0x4BCC, "45f900092c26"), (0x4BD2, "363c0003"), (0x4BD6, "383cc000"),
    (0x4BDA, "18321000"), (0x4BDE, "613a"), (0x4BE0, "5241"),
    (0x4BE2, "51cbfff6"), (0x4BF4, "4a11"), (0x4BF6, "6720"),
    (0x4C16, "6086"), (0x4C18, "4e75"), (0x4C1A, "3084"),
    (0x4C1C, "5244"), (0x4C1E, "31440018"), (0x4C22, "5244"),
    (0x4C24, "d0fc0002"), (0x4C28, "3084"), (0x4C2A, "5244"),
    (0x4C2C, "31440018"), (0x4C30, "5448"), (0x4C32, "4e75"))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = "build/direct_code/layout/" + LAYOUT_ID + "/m68k_bank09.s"
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
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


def _inputs(source_BYTE, mode):
    value = uint(source_BYTE, 255, "complete original input BYTE")
    mode = uint(mode, 4, "original comparison-selected mode")
    if mode not in (0, 4):
        raise ValueError("original mode must be 0 or 4")
    return value, mode


def source_start(source_BYTE, mode):
    """Potential original address; outer-zero guard is handled by lookup."""
    value, mode = _inputs(source_BYTE, mode)
    combined = (value + mode) & 255
    extended = combined if combined < 128 else combined-256
    shifted = (extended << 2) & 65535
    return SOURCE_BASE + (shifted if shifted < 0x8000 else shifted-65536)


def _inside(address):
    return any(s <= address < e for s, e, _ in RANGES)


def lookup(image, source_BYTE, mode):
    """One original nonzero outer input's source reads and narrow D4.W view.

This is not the complete RAM-mode-selection/output-buffer CPU algorithm.
Zero returns its real outer stop; combined selector zero is still readable.
"""
    _image(image)
    value, mode = _inputs(source_BYTE, mode)
    if value == 0:
        return dict(input_BYTE=value, mode=mode, outer_stopped=True, source_BYTE_reads=0,
            source_BYTEs=[], reads=[], tile_WORDs=[], diagnostic_is_complete_CPU=False)
    combined = (value + mode) & 255
    extended = combined if combined < 128 else combined-256
    offset = (extended << 2) & 65535
    start = source_start(value, mode)
    D4_WORD = 0xC000
    reads, tile_words = [], []
    for i in range(4):
        address = start+i
        byte = image[address]
        high_before = D4_WORD & 0xFF00
        D4_WORD = high_before | byte  # MOVE.B keeps the previous high BYTE.
        emitted = [(D4_WORD+j) & 65535 for j in range(4)]
        D4_WORD = emitted[-1]  # Three original ADDQ.W operations, not four.
        reads.append(dict(address=address, source_BYTE=byte, high_WORD_before_MOVE_BYTE=high_before,
            loaded_D4_WORD=emitted[0], emitted_tile_WORDs=emitted, helper_return_D4_WORD=D4_WORD,
            original_WORD_write_offsets=[4*i, 4*i+0x18, 4*i+2, 4*i+0x1A],
            editable_source=_inside(address)))
        tile_words.extend(emitted)
    return dict(input_BYTE=value, mode=mode, combined_BYTE=combined, EXT_WORD=extended & 65535,
        shifted_offset_WORD=offset, signed_offset=extended*4, start=start, end=start+4,
        outer_stopped=False, D3_WORD=3, source_BYTE_reads=4, source_BYTEs=list(image[start:start+4]),
        reads=reads, tile_WORDs=tile_words, return_D4_WORD=D4_WORD,
        editable_source_BYTES=sum(_inside(a) for a in range(start, start+4)),
        physical_catalog_CPU_clamp=False, diagnostic_is_complete_CPU=False)


def witnesses_for_source(ROM_address):
    address = uint(ROM_address, ROM_SIZE-1, "physical source BYTE address")
    if not _inside(address):
        raise ValueError("address outside unique new physical source ranges")
    combined = (address-SOURCE_BASE)//4
    value = combined & 255
    mode = 0
    if value == 0:
        value, mode = 0xFC, 4
    start = source_start(value, mode)
    return dict(input_BYTE=value, mode=mode, combined_BYTE=combined & 255,
        start=start, end=start+4, source_BYTE_index=address-start, input_is_nonzero=True)


def audit_witness_union(rom):
    verify_rom(rom)
    starts = {source_start(value, mode) for mode in (0, 4) for value in range(1, 256)}
    if starts != set(range(UNION_START, UNION_END, 4)):
        raise ValueError("nonzero-input complete source read union differs")
    source = {a for s, e, _ in RANGES for a in range(s, e)}
    if len(source) != EDITABLE_BYTES or sum(e-s for s, e, _ in RANGES) != EDITABLE_BYTES:
        raise ValueError("physical source union must be disjoint and exact")
    for address in source:
        witness = witnesses_for_source(address)
        if witness["input_BYTE"] == 0 or not witness["start"] <= address < witness["end"]:
            raise ValueError("physical BYTE lacks a complete nonzero original input witness")
        view = lookup(rom, witness["input_BYTE"], witness["mode"])
        if view["source_BYTE_reads"] != 4 or view["source_BYTEs"][witness["source_BYTE_index"]] != rom[address]:
            raise ValueError("source witness BYTE position/read differs")
    return dict(physical_editable_BYTES=36, complete_source_windows=256, window_BYTES=4,
        read_union_BYTES=1024, all_complete_reads_in_ROM=True, physical_unwitnessed_BYTES=0,
        zero_outer_inputs_read_source=False, combined_zero_read_witness=dict(input_BYTE=0xFC, mode=4),
        unique_editing_authority=True, typed_neighbors_emitted_again=False)


def source_fixed(start, end):
    return dict(id=f"rom_{start:06X}_ui_tile_source_BYTEs", start=start, end=end, bytes=end-start)


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=[dict(**source_fixed(s, e), source_sha256=h) for s, e, h in RANGES],
        source_union_BYTES=EDITABLE_BYTES, source_union_sha256=SOURCE_SHA256,
        serialization="one complete physical source BYTE; source/tile WORD views are read-only",
        evidence=dict(consumers=[dict(start=s, end=e, bytes=e-s, sha256=h) for s, e, h in CONSUMERS],
            instructions=[dict(address=a, bytes=b) for a, b in INSTRUCTIONS],
            original_map=dict(path=MAP_PATH, sha256=MAP_SHA256),
            frozen_raw_layout=dict(id=LAYOUT_ID, path=LAYOUT_PATH, sha256=LAYOUT_SHA256,
                snapshot_resources=81, snapshot_raw_BYTES=44366, bank=9, raw_difference_BYTES=36,
                emitted_already_typed_overlap_BYTES=0),
            caller=dict(entry=0x4B28, initial_A1_RAM=0xFFF580, original_call=0x4B44,
                first_zero_test=0x4B3A, first_zero_branch=0x4B3E,
                next_zero_test=0x4BF4, next_zero_branch=0x4BF6, next_source_branch=0x4C16,
                input_zero_is_outer_stop=True, mode_values=[0, 4],
                mode_unsigned_comparison=dict(RAM_index_WORD=0xFFF372, shift_WORD=0x4B84,
                    left_base_RAM=0xFFC000, right_base_RAM=0xFFBE00, CMP_WORD=0x4B92, BCC=0x4B96,
                    mode0="left WORD >= right WORD unsigned", mode4="left WORD < right WORD unsigned"),
                natural_RAM_input_domain="unknown", complete_RAM_access_domain="unknown"),
            reader=dict(input_BYTE_read=0x4B9E, ADD_BYTE=0x4BA0, mode_add_wraps_BYTE=True,
                EXT_WORD=0x4BA4, shift_WORD=0x4BA6, base_LEA=0x4BCC, base=SOURCE_BASE,
                formula="92C26 + s16((s8((input_BYTE+mode)&FF) << 2) & FFFF)",
                source_BYTE_read=0x4BDA, source_step_WORD=0x4BE0, D3_WORD=3, DBRA=0x4BE2,
                complete_source_BYTE_reads=4, read_union_start=UNION_START, read_union_end=UNION_END,
                read_union_BYTES=1024, nonzero_supplied_inputs=255, modes=2,
                distinct_complete_windows=256, all_reads_in_ROM=True,
                physical_catalog_not_CPU_clamp=True, constructed_not_natural_selection=True),
            output_WORD_view=dict(D4_WORD_initialization=0x4BD6, initial_D4_WORD=0xC000,
                MOVE_BYTE_preserves_previous_high_BYTE=True, helper=0x4C1A, helper_end=0x4C34,
                writes_WORDs_per_source_BYTE=4, WORD_additions_per_helper=3,
                helper_does_not_modify_D1=True, high_BYTE_carry_survives_next_source=True,
                original_helper_WORD_write_offsets=[0, 0x18, 2, 0x1A],
                no_hardware_attribute_mask_applied=True),
            old_neighbors=dict(glyph_source_alias=0x92C0A, old_glyph_end=0x92C2A,
                gap_start=0x92C4A, gap_end=0x92C52, emitted_again=False, live_edited_image=True),
            witness_starts=[witnesses_for_source(s) for s, _, _ in RANGES],
            contents_are_not_padding=True, no_sprite_or_font_bitmap_emitted=True),
        natural_source_selection="unknown", tile_business_identity="unknown", complete_UI_algorithm=False,
        independent_CPU_comparison=False)


def extract(rom):
    verify_rom(rom)
    audit_witness_union(rom)
    return dict(**metadata(), sources=[dict(**source_fixed(s, e), source_BYTEs=list(rom[s:e])) for s, e, _ in RANGES])


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"sources"}, "physical UI tile source fields")
    for key, expected in fixed.items():
        same(fields[key], expected, "physical UI tile source fields." + key)
    result = []
    for value, (start, end, _) in zip(exact_list(fields["sources"], 2, "fixed source range count"), RANGES):
        row = source_fixed(start, end)
        keys(value, set(row) | {"source_BYTEs"}, "fixed physical source")
        for key, expected in row.items():
            same(value[key], expected, "fixed physical source." + key)
        data = bytes(uint(v, 255, "complete source BYTE") for v in
            exact_list(value["source_BYTEs"], end-start, "fixed source BYTE count"))
        result.append(dict(id=row["id"], start=start, end=end, data=data, role="conditional_indexed_ui_tile_source_BYTE_alias"))
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
        "source_BYTEs": dict(type="array", minItems=e-s, maxItems=e-s,
            items=dict(type="integer", minimum=0, maximum=255))}) for s, e, _ in RANGES]
    result = obj({**{k: fixed(v) for k, v in metadata().items()},
        "sources": dict(type="array", prefixItems=rows, items=False, minItems=2, maxItems=2)})
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "36 physical source BYTEs; original tile WORD output is a read-only derived view."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("serialized whole-ROM roundtrip differs")
    encoded = blocks(rom, fields)
    witnesses = sorted({(w["input_BYTE"], w["mode"]) for s, e, _ in RANGES for a in range(s, e)
        for w in (witnesses_for_source(a),)})
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=2,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), witness_union=audit_witness_union(rom),
        complete_witness_views=[lookup(rom, value, mode) for value, mode in witnesses],
        stop_and_wrap_examples=[lookup(rom, value, mode) for value, mode in ((0, 0), (0, 4), (0xFC, 4), (0x7F, 0), (0x80, 0), (0xFF, 4))],
        blocks=[{k: v for k, v in row.items() if k != "data"} |
            dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=2,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in ui_tile_byte_alias_fields build scope or exact formal bundle")
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
