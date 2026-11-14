"""8 original portrait token BYTEs consumed before the first external pixel.

The complete source WORDs at AADDA..AADE2 have one editable authority.
The FFFF token is consumed before its 2B647A pixel source boundary; neither
that pixel address nor the preceding already-typed pixels is emitted here.
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
OUTPUT_ROOT = ROOT / "build/portrait_frontier_word_fields"
FORMAL_ROOT = ROOT / "analysis/portrait_frontier_word_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-portrait-preboundary-token-full-WORD-fields-v1"
EDITABLE_BYTES = 8
START, END = 0xAADDA, 0xAADE2
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
CONSUMER_START, CONSUMER_END = 0x661D4, 0x662E4
CONSUMER_SHA256 = reference_value(__name__, 'CONSUMER_SHA256')
TOKEN_BASE, PIXEL_BASE = 0xAE39A, 0xB649A
WITNESS_WORD = 0x021B
ORIGINAL_WORDS = (0x04C5, 0x04EE, 0x04EF, 0xFFFF)
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = "build/direct_code/layout/" + LAYOUT_ID + "/m68k_bank0a.s"
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
MAP_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
MAP_SHA256 = reference_value(__name__, 'MAP_SHA256')
INSTRUCTIONS = ((0x661EA, "3200"), (0x661EC, "e349"), (0x661EE, "d240"),
    (0x661F0, "eb49"), (0x661F2, "41f9000ae39a"), (0x661F8, "d0c1"),
    (0x661FA, "610000b8"), (0x662B4, "383c002f"), (0x662B8, "3418"),
    (0x662BA, "61000008"), (0x662BE, "51ccfff8"), (0x662C2, "4e75"),
    (0x662C4, "43f9000b649a"), (0x662CA, "02820000ffff"), (0x662D0, "eb8a"),
    (0x662D2, "d3c2"), (0x662D4, "363c0007"), (0x662D8, "23d900c00000"),
    (0x662DE, "51cbfff8"), (0x662E2, "4e75"))
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical complete ROM bytes, size and SHA-256 required")
    if sha(rom[START:END]) != SOURCE_SHA256 or sha(rom[CONSUMER_START:CONSUMER_END]) != CONSUMER_SHA256:
        raise ValueError("pinned original consumer/token source differs")


def primary_start(D0_WORD):
    value = uint(D0_WORD, 65535, "complete supplied D0 WORD")
    offset = (value*96) & 65535
    return TOKEN_BASE + (offset if offset < 0x8000 else offset-65536)


def lookup(image, D0_WORD):
    """Ordered primary-source prefix, not the whole portrait/CPU algorithm.

Each WORD is recorded first, then each of its eight LONG sources in order.
A sample-external source is an explicit diagnostic boundary, not a CPU clamp.
"""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic requires complete bytes image; edited images are allowed")
    value = uint(D0_WORD, 65535, "complete supplied D0 WORD")
    start = primary_start(value)
    tokens, pixels = [], []
    result = dict(D0_WORD=value, primary_start=start, original_primary_WORD_count=48,
        source_projection_not_CPU=True, complete_portrait_plan=False,
        external_boundary_is_diagnostic_not_CPU_stop=True)
    for item in range(48):
        address = start+item*2
        if not 0 <= address <= ROM_SIZE-2:
            return dict(**result, status="out_of_ROM_token_source", token_reads=tokens, pixel_LONG_reads=pixels,
                boundary=dict(item=item, address=address, bytes=2))
        word = int.from_bytes(image[address:address+2], "big")
        pixel_start = PIXEL_BASE + word*32  # ANDI.L FFFF, LSL.L #5, ADDA.L.
        tokens.append(dict(item=item, address=address, token_WORD=word, source_BYTEs=list(image[address:address+2]),
            pixel_start=pixel_start, already_consumed=True, token_is_terminator=False,
            editable_source=START <= address < END))
        for index in range(8):
            source = pixel_start+index*4
            if not 0 <= source <= ROM_SIZE-4:
                return dict(**result, status="out_of_ROM_pixel_source", token_reads=tokens, pixel_LONG_reads=pixels,
                    boundary=dict(item=item, token_address=address, token_WORD=word, LONG_index=index,
                        address=source, bytes=4, token_already_consumed=True))
            pixels.append(dict(item=item, LONG_index=index, address=source, bytes=4,
                value_LONG=int.from_bytes(image[source:source+4], "big"), read_only_old_source=True))
    return dict(**result, status="in_ROM_primary_source_plan", token_reads=tokens, pixel_LONG_reads=pixels,
        secondary_and_palette_not_projected=True)


def witness_fixed():
    return dict(D0_WORD=WITNESS_WORD, primary_start=0xAADBA,
        items=[16, 17, 18, 19], token_addresses=list(range(START, END, 2)),
        original_token_WORDs=list(ORIGINAL_WORDS), completed_pixel_tiles_before_external=19,
        token_WORDs_consumed_before_external=20, pixel_LONGs_read_before_external=152,
        first_external_pixel=dict(item=19, token_address=0xAADE0, token_WORD=0xFFFF,
            LONG_index=0, address=0x2B647A, bytes=4, token_already_consumed=True),
        complete_portrait_plan=False, conditional_not_natural=True)


def audit_witness(rom):
    verify_rom(rom)
    plan = lookup(rom, WITNESS_WORD)
    expected = witness_fixed()
    selected = [row for row in plan["token_reads"] if START <= row["address"] < END]
    if (plan["primary_start"] != expected["primary_start"] or plan["status"] != "out_of_ROM_pixel_source"
        or plan["boundary"] != expected["first_external_pixel"] or len(plan["token_reads"]) != 20
        or len(plan["pixel_LONG_reads"]) != 152 or [r["item"] for r in selected] != expected["items"]
        or [r["address"] for r in selected] != expected["token_addresses"]
        or [r["token_WORD"] for r in selected] != expected["original_token_WORDs"]):
        raise ValueError("original ordered prefix/frontier witness differs")
    return dict(physical_editable_BYTES=8, full_token_WORDs=4, token_WORDs_before_external=20,
        earlier_complete_pixel_tiles=19, earlier_in_ROM_pixel_LONG_reads=152,
        new_pixel_BYTES_emitted=0, every_new_WORD_consumed_before_first_external=True,
        complete_portrait_plan=False, unique_editing_authority=True)


def source_fixed():
    return dict(id="rom_0AADDA_portrait_frontier_token_WORDs", start=START, end=END, WORD_count=4, bytes=8)


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=[dict(**source_fixed(), source_sha256=SOURCE_SHA256)],
        source_union_BYTES=EDITABLE_BYTES, source_union_sha256=SOURCE_SHA256,
        serialization="four complete big-endian token WORDs, one physical authority; pixel reads are diagnostic only",
        original_witness=witness_fixed(),
        evidence=dict(consumer=dict(start=CONSUMER_START, end=CONSUMER_END,
                bytes=CONSUMER_END-CONSUMER_START, sha256=CONSUMER_SHA256),
            instructions=[dict(address=a, bytes=b) for a, b in INSTRUCTIONS],
            original_map=dict(path=MAP_PATH, sha256=MAP_SHA256),
            frozen_raw_layout=dict(id=LAYOUT_ID, path=LAYOUT_PATH, sha256=LAYOUT_SHA256,
                snapshot_resources=81, snapshot_raw_BYTES=44366, bank=10, raw_difference_BYTES=8,
                emitted_already_typed_overlap_BYTES=0),
            primary_source=dict(base=TOKEN_BASE, formula="AE39A + s16((D0_WORD*96) & FFFF)",
                multiply_WORD_wrap_then_signed=True, original_BSR=0x661FA,
                counter_WORD=47, WORD_count=48, WORD_read=0x662B8, source_step_BYTES=2,
                helper_BSR=0x662BA, DBRA=0x662BE, physical_catalog_CPU_clamp=False),
            primary_pixels=dict(base=PIXEL_BASE, formula="B649A + zeroextend(token_WORD)*32 + 4*LONG_index",
                ANDI_LONG=0x662CA, shift_LONG=0x662D0, ADDA_LONG=0x662D2,
                counter_WORD=7, LONG_count=8, LONG_read=0x662D8, DBRA=0x662DE,
                token_bit15_is_not_control=True, FFFF_is_not_terminator=True,
                token_read_precedes_pixel_LONGs=True, no07FF_mask=True,
                first_unknown_external_source_not_mirrored_or_filled=True,
                boundary_is_diagnostic_not_original_CPU_stop=True),
            original_preboundary_new_tokens=[dict(item=item, address=START+2*i, token_WORD=word,
                pixel_start=PIXEL_BASE+word*32, pixel_source_in_ROM=word != 0xFFFF)
                for i, (item, word) in enumerate(zip(range(16, 20), ORIGINAL_WORDS))],
            old_token_neighbor_BYTEs_emitted=0, preceding_old_pixel_BYTEs_emitted=0,
            secondary_or_palette_new_BYTES=0, independent_from_complete60_source_catalog=True),
        natural_D0_selection="unknown", natural_token_values="unknown", safe_picture_or_playback="unknown",
        complete_portrait_algorithm=False, independent_CPU_comparison=False)


def extract(rom):
    verify_rom(rom)
    audit_witness(rom)
    return dict(**metadata(), token_sources=[dict(**source_fixed(),
        WORDs=[int.from_bytes(rom[a:a+2], "big") for a in range(START, END, 2)])])


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"token_sources"}, "portrait frontier fields")
    for key, expected in fixed.items():
        same(fields[key], expected, "portrait frontier fields." + key)
    value = exact_list(fields["token_sources"], 1, "fixed physical source range count")[0]
    row = source_fixed()
    keys(value, set(row) | {"WORDs"}, "fixed token source")
    for key, expected in row.items():
        same(value[key], expected, "fixed token source." + key)
    data = b"".join(uint(word, 65535, "complete token WORD").to_bytes(2, "big")
        for word in exact_list(value["WORDs"], 4, "fixed full token WORD count"))
    return [dict(id=row["id"], start=START, end=END, data=data, role="original_preboundary_portrait_token_WORDs")]


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
    row = obj({**{k: fixed(v) for k, v in source_fixed().items()},
        "WORDs": dict(type="array", minItems=4, maxItems=4,
            items=dict(type="integer", minimum=0, maximum=65535))})
    result = obj({**{k: fixed(v) for k, v in metadata().items()},
        "token_sources": dict(type="array", prefixItems=[row], items=False, minItems=1, maxItems=1)})
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "8 original preboundary token BYTEs as four full WORDs; no pixels or complete-plan claim."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("serialized whole-ROM roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), ordered_witness=audit_witness(rom),
        original_primary_prefix=lookup(rom, WITNESS_WORD),
        blocks=[{k: v for k, v in row.items() if k != "data"} |
            dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in portrait_frontier_word_fields build scope or exact formal bundle")
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
