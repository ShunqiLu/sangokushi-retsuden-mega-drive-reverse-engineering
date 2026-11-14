"""250 source bytes: counted14x10 UI operations and8x8 VDP attributes.

The first source uses numeric-LONG handler6, not numeric-WORD handler4.
Its original controls/counts remain fixed while complete payload WORD/LONGs
are editable. The second source preserves all16 bits of64 VDP attribute WORDs.
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
OUTPUT_ROOT = ROOT / "build/ui_resource_word_sources"
FORMAL_ROOT = ROOT / "analysis/ui_resource_word_sources/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
MAX_JSON = 1024 * 1024
FORMAT = "g5510-counted-LONGvalue-UI-and-VDP-WORD-sources-v1"
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
EDITABLE_BYTES = 250
STREAM_START, STREAM_END = 0x00D2EE, 0x00D368
TILE_START, TILE_END = 0x03C2A4, 0x03C324
VDP_INPUTS = (0xE820, 0xE8A0, 0xE920, 0xE9A0, 0xEA20, 0xEAA0, 0xEB20, 0xEBA0)
BSR_PCS = (0x3C244, 0x3C24C, 0x3C254, 0x3C25C, 0x3C264, 0x3C26C, 0x3C274, 0x3C27C)
BODIES = (
    (0x00D298, 0x00D2CA, reference_value(__name__, 'BODIES')),
    (0x011F4A, 0x011F70, reference_value(__name__, 'BODIES_2')),
    (0x026BFA, 0x026D1C, reference_value(__name__, 'BODIES_3')),
    (0x03C23A, 0x03C2A4, reference_value(__name__, 'BODIES_4')),
    (0x03B2B0, 0x03B2D8, reference_value(__name__, 'BODIES_5')),
)
SOURCE_HASHES = (
    (STREAM_START, STREAM_END, reference_value(__name__, 'SOURCE_HASHES')),
    (TILE_START, TILE_END, reference_value(__name__, 'SOURCE_HASHES_2')),
)
MAP_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
MAP_SHA256 = reference_value(__name__, 'MAP_SHA256')
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical complete ROM bytes, size and SHA-256 required")
    for start, end, digest in (*BODIES, *SOURCE_HASHES):
        if sha(rom[start:end]) != digest:
            raise ValueError("pinned original consumer/source differs")
    # The dispatch is read as WORD displacements from26C58, not handler numbers.
    if rom[0x26C4C:0x26C58].hex() != "0000001a0036007e00c400d8":
        raise ValueError("original source-handler offset directory differs")


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_format_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(emit_BYTES=250, row_stream_source_BYTES=122, VDP_WORD_source_BYTES=128,
                            ranges=[dict(start=s, end=e, bytes=e-s) for s, e, _ in SOURCE_HASHES]),
        evidence=dict(
            consumers=[dict(start=s, end=e, bytes=e-s, sha256=h) for s, e, h in BODIES],
            original_ledger=dict(path=MAP_PATH, sha256=MAP_SHA256, reachability_confidence="heuristic",
                                 actual_compiled_PC_inventory_count=53044),
            accepted_raw_snapshot=dict(layout=LAYOUT_ID, resources=55, raw_BYTES=49017,
                                       source_raw_difference_BYTES=250, source_typed_overlap_BYTES=0),
            stream_callers=[dict(LEA_PC=0xD2A6, LEA_PC_base=0xD2A8, displacement_WORD=0x46,
                                 call_PC=0xD2B6, reader=0x26BFA, original_D0_LONG=0xC000000E,
                                 original_D1_WORD=10, original_D2_WORD=0xC41A),
                            dict(LEA_PC=0x11F58, LEA_absolute_LONG=STREAM_START,
                                 call_PC=0x11F6A, reader=0x26BFA, original_D0_LONG=0xC000000E,
                                 original_D1_WORD=10, original_D2_WORD=0xC3B2)],
            stream_grammar=dict(source_WORD_read=0x26C10, negative_branch=0x26C12,
                direct_WORD_positive_sign_required=True, direct_attribute_OR_original_high_WORD=0xC000,
                row_remaining_WORD=14, row_count_WORD=10, row_counter_test=0x26C36, line_DBRA=0x26C3A,
                source_stop="ten original rows of fourteen emitted cells; no source terminator",
                negative_selector="((control_WORD & 7FFF) >> 7) & FFFE",
                directory=0x26C4C, directory_read=0x26C2E, call_PC=0x26C32, call_PC_base=0x26C34,
                handler_target_base=0x26C58, used_selector_BYTE_offsets=[0, 2, 6],
                used_displacements_WORD=[0, 0x1A, 0x7E], used_targets=[0x26C58, 0x26C72, 0x26CD6],
                repeat_payload_read=0x26C5E, ascending_payload_read=0x26C78, ascending_increment_WORD=2,
                numeric_LONG_pointer_read=0x26CDA, numeric_LONG_value_read=0x26CE0,
                numeric_formatter_call=0x26CEE, numeric_formatter=0x1270A,
                numeric_RAM_formatter_simulated=False,
                unused_numeric_WORD_handler=0x26C8E, numeric_WORD_handler_not_used_by_this_source=True,
                control_WORDs_and_counts_pinned=True, complete_dispatch_domain=False),
            VDP_read=dict(source_LEA=0x3C23A, source_PC_base=0x3C23C, displacement_WORD=0x68,
                source_base=TILE_START, call_PCs=list(BSR_PCS), helper_entry=0x3C282,
                A2_push_PC=0x3C282, command_setup_call=0x3C28E, command_helper=0x3B2B0,
                A2_restore_PC=0x3C292, count_load=0x3C296, original_D0_count=7,
                source_WORD_read=0x3C298, DBRA_PC=0x3C29E,
                per_call_WORD_count=8, true_call_count=8, total_WORD_count=64,
                A2_progression="eight WORD postincrements per helper; no reset between original calls",
                VDP_source_full_WORD_bits_preserved=True, writes_port=0xC00000,
                original_address_inputs=list(VDP_INPUTS))),
        source_views_are_read_only=True, natural_selection="unknown", business_scene_identity="unknown",
        edited_gameplay_safety="unknown", complete_RAM_or_VDP_execution=False,
        independent_CPU_comparison=False)


def pinned(value, fixed, mutable, label):
    keys(value, set(fixed) | set(mutable), label)
    for key, expected in fixed.items():
        same(value[key], expected, label+"."+key)


def stream_fixed():
    return dict(id="rom_00D2EE_weapon_price_row_source", start=STREAM_START, end=STREAM_END,
                columns=14, lines=10, source_BYTEs=122, original_attribute_OR_WORD=0xC000)


def decode_stream(image):
    """Source framing projection only. Numeric RAM pointers are not dereferenced."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("source projection requires a complete bytes image")
    p, rows = STREAM_START, []
    for row_index in range(10):
        begin, count, operations = p, 0, []
        while count < 14:
            if p+2 > STREAM_END:
                raise ValueError("source WORD beyond admitted stream")
            start = p
            WORD = int.from_bytes(image[p:p+2], "big")
            p += 2
            if WORD < 0x8000:
                operation = dict(kind="direct_WORD", start=start, end=p, emitted_cells=1, WORD=WORD)
            else:
                selector, emitted = ((WORD & 0x7FFF) >> 7) & 0xFFFE, WORD & 255
                if selector not in (0, 2, 6) or not emitted:
                    raise ValueError("source handler/count outside this admitted framing")
                size = 4 if selector == 6 else 2
                if p+size > STREAM_END:
                    raise ValueError("control payload beyond admitted stream")
                value = int.from_bytes(image[p:p+size], "big")
                operation = dict(kind={0:"repeat_WORD", 2:"ascending_WORD", 6:"numeric_LONG_value_ref"}[selector],
                                 start=start, end=p+size, emitted_cells=emitted, control_WORD=WORD,
                                 dispatch_BYTE_offset=selector, handler={0:0x26C58, 2:0x26C72, 6:0x26CD6}[selector])
                operation["RAM_ref_LONG" if selector == 6 else "payload_WORD"] = value
                p += size
            count += operation["emitted_cells"]
            if count > 14:
                raise ValueError("source operation overruns original14-cell row")
            operations.append(operation)
        rows.append(dict(row_index=row_index, start=begin, end=p, emitted_cells=14, operations=operations))
    if p != STREAM_END:
        raise ValueError("original row counters do not close exactly at D368")
    return dict(**stream_fixed(), rows=rows)


def tile_row_fixed(index):
    start = TILE_START+index*16
    return dict(id=f"rom_{start:06X}_VDP_attribute_row", row_index=index, start=start, end=start+16,
                WORD_count=8, original_BSR_PC=BSR_PCS[index], VDP_address_input_WORD=VDP_INPUTS[index])


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(), row_stream=decode_stream(rom),
        VDP_rows=[dict(**tile_row_fixed(index), attribute_WORDs=[int.from_bytes(rom[p:p+2], "big")
            for p in range(TILE_START+index*16, TILE_START+(index+1)*16, 2)]) for index in range(8)])


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {"row_stream", "VDP_rows"}, "UI source package")
    stream = fields["row_stream"]
    pinned(stream, stream_fixed(), {"rows"}, "counted row stream")
    original = decode_stream(rom)
    raw = bytearray()
    for row, expected in zip(exact_list(stream["rows"], 10, "original row count"), original["rows"]):
        pinned(row, {k:v for k,v in expected.items() if k != "operations"}, {"operations"}, "source row")
        for operation, source in zip(exact_list(row["operations"], len(expected["operations"]), "original operations"), expected["operations"]):
            mutable = {"WORD"} if source["kind"] == "direct_WORD" else ({"payload_WORD"} if "payload_WORD" in source else {"RAM_ref_LONG"})
            pinned(operation, {k:v for k,v in source.items() if k not in mutable}, mutable, "source operation")
            if source["kind"] == "direct_WORD":
                WORD = uint(operation["WORD"], 0x7FFF, "positive direct source WORD retaining sign branch")
                raw.extend(WORD.to_bytes(2, "big"))
            else:
                raw.extend(operation["control_WORD"].to_bytes(2, "big"))
                name = "payload_WORD" if "payload_WORD" in source else "RAM_ref_LONG"
                size = 2 if name == "payload_WORD" else 4
                raw.extend(uint(operation[name], (1 << (size*8))-1, "complete source payload "+name).to_bytes(size, "big"))
    if len(raw) != 122:
        raise ValueError("fixed counted-source BYTE cost differs")
    tiles = bytearray()
    for index, row in enumerate(exact_list(fields["VDP_rows"], 8, "eight VDP source rows")):
        pinned(row, tile_row_fixed(index), {"attribute_WORDs"}, "VDP source row")
        for WORD in exact_list(row["attribute_WORDs"], 8, "eight full VDP WORDs"):
            tiles.extend(uint(WORD, 0xFFFF, "complete VDP attribute WORD").to_bytes(2, "big"))
    return [dict(id="rom_00D2EE_counted_UI_LONG_value_source", start=STREAM_START, end=STREAM_END,
                 data=bytes(raw), role="confirmed_counted_UI_ROW_WORD_LONG_source"),
            dict(id="rom_03C2A4_VDP_tile_attribute_WORDs", start=TILE_START, end=TILE_END,
                 data=bytes(tiles), role="confirmed_eight_by_eight_VDP_attribute_WORD_source")]


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def tile_source_view(image):
    """Live full-WORD attribute bits, not a second editing authority or VDP model."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("tile source view requires complete bytes image")
    result = []
    for index in range(8):
        cells = []
        for column in range(8):
            address = TILE_START+16*index+2*column
            WORD = int.from_bytes(image[address:address+2], "big")
            cells.append(dict(address=address, column=column, WORD=WORD, tile_index=WORD & 0x7FF,
                horizontal_flip=bool(WORD & 0x0800), vertical_flip=bool(WORD & 0x1000),
                palette=(WORD >> 13) & 3, priority=bool(WORD & 0x8000)))
        result.append(dict(**tile_row_fixed(index), attributes=cells, preview_is_editing_authority=False))
    return result


def schema(rom):
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({k:fixed(v) for k,v in value.items()})
        if type(value) is list:
            return exact([fixed(v) for v in value])
        return dict(type={str:"string", int:"integer", bool:"boolean"}[type(value)], const=value)
    def exact(items):
        return dict(type="array", prefixItems=items, items=False, minItems=len(items), maxItems=len(items))
    original = decode_stream(rom)
    rows = []
    for row in original["rows"]:
        ops = []
        for source in row["operations"]:
            mutable = "WORD" if source["kind"] == "direct_WORD" else ("payload_WORD" if "payload_WORD" in source else "RAM_ref_LONG")
            maximum = {"WORD":0x7FFF, "payload_WORD":0xFFFF, "RAM_ref_LONG":0xFFFFFFFF}[mutable]
            ops.append(obj({**{k:fixed(v) for k,v in source.items() if k != mutable},
                            mutable:dict(type="integer", minimum=0, maximum=maximum)}))
        rows.append(obj({**{k:fixed(v) for k,v in row.items() if k != "operations"}, "operations":exact(ops)}))
    properties = {k:fixed(v) for k,v in metadata().items()}
    properties["row_stream"] = obj({**{k:fixed(v) for k,v in stream_fixed().items()}, "rows":exact(rows)})
    properties["VDP_rows"] = exact([obj({**{k:fixed(v) for k,v in tile_row_fixed(i).items()},
        "attribute_WORDs":dict(type="array", minItems=8, maxItems=8, items=dict(type="integer", minimum=0, maximum=0xFFFF))}) for i in range(8)])
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Fixed counted operation framing with true LONG numeric refs, plus64 full16bit VDP attributes."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("serialized UI source whole-ROM roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=250, physical_blocks=2, whole_ROM_exact=True,
        whole_ROM_sha256=sha(image), counted_rows=decode_stream(image), VDP_source_rows=tile_source_view(image),
        blocks=[{k:v for k,v in row.items() if k != "data"} | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json":serialized, "fields.schema.json":dump(schema(rom)), "validation.json":dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=250, physical_blocks=2,
        members={name:dict(bytes=len(data), sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("dedicated UI resource output or exact formal bundle required")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "import", "verify"))
    parser.add_argument("--rom", default=str(DEFAULT_ROM)); parser.add_argument("--fields")
    parser.add_argument("--bundle"); parser.add_argument("--output")
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
        members = render_bundle(rom); target.mkdir()
        for name,data in members.items(): put(target/name, data)
        result = dict(path=str(target), editable_bytes=250, members={name:sha(data) for name,data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name, MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=250, whole_ROM_exact=True, whole_ROM_sha256=ROM_SHA256)
    else:
        image = rebuild(rom, load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON)))
        if target is not None: put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=250,
                      exact_canonical=image == rom, bytes=len(image), sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
