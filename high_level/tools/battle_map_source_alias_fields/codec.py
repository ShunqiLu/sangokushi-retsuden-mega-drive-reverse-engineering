"""Editable BYTE sources reached by an original signed-WORD pointer/map reader.

Only05D030..05D5E4 is authored. The canonical constructed80DA.W=2670 path
reads an existing compact-sprite field as a LONG pointer, then enters03AACE.
The original32-row stop and marker/count-zero paths remain live after edits.
This is a data-read/control-edge projection, not execution of a whole CPU/VDP.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path
from tools.battle_deployment_parameters import codec as shared

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE, ROM_SHA256 = shared.ROM_SIZE, shared.ROM_SHA256
DEFAULT_ROM = shared.DEFAULT_ROM
OUTPUT_ROOT = ROOT / "build/battle_map_source_alias_fields"
FORMAL_ROOT = ROOT / "analysis/battle_map_source_alias_fields/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
MAX_JSON = 16 * 1024 * 1024
FORMAT = "g5510-conditional-battle-map-RLE-source-BYTE-alias-v1"
START, END, EDITABLE_BYTES = 0x5D030, 0x5D5E4, 1460
TABLE_BASE, WITNESS_WORD, POINTER_SOURCE = 0x3DC90, 0x2670, 0x37650
BLOCK_ID = "rom_05D030_conditional_map_reader_BYTE_aliases"
BASELINE_LAYOUT = reference_value(__name__, 'BASELINE_LAYOUT')
BASELINE_MANIFEST_SHA = reference_value(__name__, 'BASELINE_MANIFEST_SHA')
BODIES = (
    (0x3DBDC, 0x3DBFC, reference_value(__name__, 'BODIES')),
    (0x3AACE, 0x3AB52, reference_value(__name__, 'BODIES_2')),
    (0x3B2B0, 0x3B2D8, reference_value(__name__, 'BODIES_3')),
)
sha, dump, keys, same, uint, exact_list = shared.sha, shared.dump, shared.keys, shared.same, shared.uint, shared.exact_list
safe_path, read_bounded, put, load_fields = shared.safe_path, shared.read_bounded, shared.put, shared.load_fields


def verify_code(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("complete bytes image required")
    for start, end, digest in BODIES:
        if sha(image[start:end]) != digest:
            raise ValueError("pinned original caller/reader/helper bytes differ")


def verify_rom(rom):
    verify_code(rom)
    if sha(rom) != ROM_SHA256:
        raise ValueError("canonical original ROM SHA required")


def metadata():
    return dict(format=FORMAT, confidence="confirmed_conditional_source_encoding",
        resource_role="candidate_map_reader_source_BYTE_alias_not_main_map_ownership",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        physical_scope=dict(start=START, end=END, bytes=EDITABLE_BYTES, one_physical_authority=True),
        raw_baseline=dict(layout_id=BASELINE_LAYOUT, manifest_sha256=BASELINE_MANIFEST_SHA,
                          raw_intersection_BYTES=EDITABLE_BYTES),
        evidence=dict(bodies=[dict(start=a, end=z, sha256=h) for a, z, h in BODIES],
            producer_PC=0x3DBDC, producer_RAM=0xFFFF80DA, producer_width_BYTES=2,
            shift_PC=0x3DBE0, shift_bits=2, shift_width_BITS=16,
            pointer_table_LEA_PC=0x3DBE2, pointer_table_PC_base=0x3DBE4,
            pointer_table_displacement_WORD=0xAC, pointer_table_base=TABLE_BASE,
            pointer_read_PC=0x3DBE8, pointer_width_BYTES=4, pointer_EA_index="sign_extended_shifted_WORD",
            original_JSR_PC=0x3DBF8, original_JSR_bytes="4ebaced4", original_JSR_target=0x3AACE,
            original_helper_BSR_PC=0x3AAE4, helper_entry=0x3B2B0,
            constructed_WORD=WITNESS_WORD, original_pointer_source=POINTER_SOURCE,
            original_pointer_LONG=START, pointer_source_old_author="compact_sprite_records",
            original_rows=32, original_WORDs_per_row=32, row_limit_is_original_not_budget=True,
            witness_is_constructed_not_natural=True),
        baseline_raw_prefix_not_emitted_here=dict(start=0x5CE22, end=START, bytes=526,
            emitted=False, separate_conditional_source_package="rle_gap_source_alias_fields"),
        original_pointer_fields_edited_here=False, old_title_cross_reads_emit_BYTES=0,
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        source_address_CPU_BITS=32, source_bus_BITS=24,
        recovered_functions_added=0, independent_CPU_comparison=False,
        whole_CPU_or_VDP_model=False, natural80DA_domain_proved=False,
        padding_admission=False, main_map_owner_admission=False)


def pointer_address(selector_WORD):
    word = (uint(selector_WORD, 65535, "80DA.W") << 2) & 65535
    return TABLE_BASE + (word - 65536 if word & 32768 else word)


def source_view(image, selector_WORD=WITNESS_WORD, source_BYTE_budget=65536):
    """Run the genuine local producer/pointer/parser path over a live image.

    Original call encodings are guarded and reported, not synthetic CPU frames.
    The scalar selector is the supplied live WORD read at03DBDC; no editor-slot
    count constrains it. Interrupts, shared RAM mutation and device timing are
    outside this read-only projection.
    """
    uint(selector_WORD, 65535, "80DA.W")
    uint(source_BYTE_budget, 65536, "external source BYTE budget")
    verify_code(image)
    address = pointer_address(selector_WORD)
    target = int.from_bytes(image[address:address + 4], "big")
    cursor = target
    reads, words, edges = [], [], []
    result = dict(selector_WORD=selector_WORD, shifted_WORD=selector_WORD << 2 & 65535,
        producer_read=dict(PC=0x3DBDC, address=0xFFFF80DA, width_BYTES=2, WORD=selector_WORD),
        pointer_read=dict(PC=0x3DBE8, address=address, width_BYTES=4, LONG=target),
        original_control_edge=dict(PC=0x3DBF8, bytes="4ebaced4", kind="JSR", target=0x3AACE),
        control_edges=edges, source_reads=reads, output_WORDs=words,
        natural80DA_domain_proved=False, whole_CPU_or_VDP_model=False)
    class Stop(Exception):
        def __init__(self, reason): self.reason = reason
    def take(pc):
        nonlocal cursor
        if len(reads) == source_BYTE_budget:
            raise Stop("external_source_BYTE_budget")
        bus = cursor & 0xFFFFFF
        if not 0 <= bus < ROM_SIZE:
            raise Stop("unmapped_source_BYTE_boundary")
        value = image[bus]
        reads.append(dict(PC=pc, address=bus, CPU_address=cursor, width_BYTES=1, BYTE=value,
                          inside_edit_scope=START <= bus < END))
        cursor = cursor + 1 & 0xFFFFFFFF
        return value
    def finish(status, following=None):
        result.update(status=status, source_cursor=cursor, source_BYTES=len(reads),
            decoded_WORDs=len(words), completed_rows=len(words) // 32, following_PC=following,
            source_reads_inside_edit_scope=sum(row["inside_edit_scope"] for row in reads))
        return result
    #03AACE clears raw/OR flags, setsD6=32;03AAE4 enters the original helper.
    edges.extend([dict(PC=0x3AAE4, kind="BSR", target=0x3B2B0),
                  dict(PC=0x3B2D6, kind="RTS", target=0x3AAE8)])
    try:
        marker = take(0x3AAF0)
        result["marker_BYTE"] = marker
        while True:
            first = take(0x3AAF2)
            if first != marker:
                second = take(0x3AB02)
                count, output_PC = 1, 0x3AB08
            else:
                count = take(0x3AB14)
                if count == 0:
                    return finish("original_marker_zero", 0x3DBFC)
                first, second = take(0x3AB1A), take(0x3AB1E)
                count += 1
                output_PC = 0x3AB24
            value = first << 8 | second
            for _ in range(count):
                words.append(dict(PC=output_PC, width_BYTES=2, WORD=value))
                if len(words) == 1024:
                    #03AB40 pops the row-helper BSR return with MOVEM.L D0;
                    #03AB44 RTS then returns to the original caller03DBFC.
                    edges.append(dict(PC=0x3AB40, kind="row_helper_return_pop", width_BYTES=4,
                                      paired_RTS=False))
                    return finish("original_32row_limit", 0x3DBFC)
                if len(words) % 32 == 0:
                    edges.extend([dict(PC=0x3AB4A, kind="BSR", target=0x3B2B0),
                                  dict(PC=0x3B2D6, kind="RTS", target=0x3AB4E)])
    except Stop as stop:
        return finish(stop.reason)


def canonical_witnesses(rom):
    verify_rom(rom)
    view = source_view(rom)
    if (view["pointer_read"]["address"], view["pointer_read"]["LONG"],
        view["status"], view["source_BYTES"], view["decoded_WORDs"]) != (POINTER_SOURCE, START, "original_32row_limit", 2049, 1024):
        raise ValueError("original constructed pointer/1024WORD path differs")
    witnesses = {row["address"]: row["PC"] for row in view["source_reads"] if row["inside_edit_scope"]}
    if set(witnesses) != set(range(START, END)):
        raise ValueError("not every original source BYTE has a true read witness")
    return witnesses


def extract(rom):
    witnesses = canonical_witnesses(rom)
    return dict(**metadata(), source_BYTEs=[dict(address=a, original_read_PC=witnesses[a], BYTE=rom[a])
                for a in range(START, END)])


def blocks(rom, fields):
    witnesses = canonical_witnesses(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"source_BYTEs"}, "conditional source fields")
    for key, value in fixed.items(): same(fields[key], value, "package." + key)
    data = bytearray()
    for a, row in zip(range(START, END), exact_list(fields["source_BYTEs"], EDITABLE_BYTES, "source BYTEs")):
        keys(row, {"address", "original_read_PC", "BYTE"}, "source BYTE")
        same(row["address"], a, "source address/order")
        same(row["original_read_PC"], witnesses[a], "original read witness")
        data.append(uint(row["BYTE"], 255, "source BYTE full bits"))
    return [dict(id=BLOCK_ID, start=START, end=END, data=bytes(data),
                 role="candidate_conditional_original_map_reader_BYTE_source_alias")]


def rebuild(rom, fields):
    row = blocks(rom, fields)[0]
    return rom[:START] + row["data"] + rom[END:]


def schema():
    def obj(properties): return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict: return obj({key: fixed(item) for key, item in value.items()})
        if type(value) is list: return dict(type="array", prefixItems=[fixed(item) for item in value], items=False, minItems=len(value), maxItems=len(value))
        return dict(type={str:"string", int:"integer", bool:"boolean"}[type(value)], const=value)
    properties = {key: fixed(value) for key, value in metadata().items()}
    properties["source_BYTEs"] = dict(type="array", minItems=EDITABLE_BYTES, maxItems=EDITABLE_BYTES,
        items=obj(dict(address=dict(type="integer", minimum=START, maximum=END-1),
            original_read_PC=dict(type="integer", enum=[0x3AAF0,0x3AAF2,0x3AB02,0x3AB14,0x3AB1A,0x3AB1E]),
            BYTE=dict(type="integer", minimum=0, maximum=255))))
    return dict(**obj(properties), **{"$schema":"https://json-schema.org/draft/2020-12/schema"},
        description="Original conditional RLE source BYTEs; addresses/read witnesses fixed, values full0..255. Not padding or natural-map ownership.")


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom: raise ValueError("whole-ROM serialized roundtrip differs")
    view = source_view(image)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), source_sha256=sha(rom[START:END]),
        canonical_projection=view, canonical_BYTE_witnesses=EDITABLE_BYTES,
        old_typed_source_read_BYTES=view["source_BYTES"]-EDITABLE_BYTES,
        no_natural_domain_or_whole_function_admission=True,
        limitations=["Supplied80DA WORD is constructed; upstream lifetime remains unknown.",
            "The original lookup aliases compact sprite fields; this is not an ordinary5-slot selector claim.",
            "Marker/count/row exit can block previously reached BYTEs after edits.",
            "Old title cross-reads remain live and are never re-emitted here.",
            "Control edges verify original call/helper byte paths, not full CPU/RAM/VDP execution."])
    members = {"fields.json":dump(fields), "fields.schema.json":dump(schema()), "validation.json":dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("dedicated build output or exact fresh formal bundle required")
    if path.exists() or not path.parent.is_dir(): raise ValueError("fresh output and existing parent required")
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
        if args.output is None or args.fields is not None or args.bundle is not None: raise ValueError("export requires output only")
        target = fresh_output(args.output, bundle=True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None: raise ValueError("import requires fresh .bin output")
        target = fresh_output(args.output)
        if target.suffix.lower() != ".bin": raise ValueError("fresh .bin required")
    elif args.output is not None or args.fields is not None and args.bundle is not None:
        raise ValueError("verify writes nothing and takes fields or bundle")
    rom = read_bounded(args.rom, ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items(): put(target/name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES)
    elif args.command == "verify" and args.bundle is not None:
        path = safe_path(args.bundle)
        if not path.is_dir() or {p.name for p in path.iterdir()} != MEMBERS: raise ValueError("exact4 members required")
        for name, data in render_bundle(rom).items():
            if read_bounded(path/name, MAX_JSON) != data: raise ValueError("generated member drift: " + name)
        result = dict(verified=True, editable_bytes=EDITABLE_BYTES, whole_ROM_exact=True)
    else:
        image = rebuild(rom, load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON)))
        if target is not None: put(target, image)
        result = dict(exact_canonical=image == rom, sha256=sha(image), editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__": raise SystemExit(main())
