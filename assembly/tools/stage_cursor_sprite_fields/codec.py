"""Lossless fields for nine original stage-selected AC08 sprite streams.

The editor owns 162 stream bytes and nine BE16 offsets, exactly 180 bytes.
Physical counts do not clamp the full-WORD selector. Diagnostics project only
original immutable-source reads, not complete RAM, rendering or CPU execution.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared
from tools.ui_cursor_sprite_templates import codec as ac08

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
OUTPUT_ROOT = ROOT / "build/stage_cursor_sprite_fields"
FORMAL_ROOT = ROOT / "analysis/stage_cursor_sprite_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 180
FORMAT = "g5510-stage-cursor-sprite-source-WORD-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
SOURCE_START, STREAM_END, SOURCE_END = 0xD978, 0xDA1A, 0xDA2C
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
PREFIX = (0xD8EC, 0xD978, reference_value(__name__, 'PREFIX'))
CONSUMER = (0xAC08, 0xAD06, reference_value(__name__, 'CONSUMER'))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_BANK_SHA256 = reference_value(__name__, 'LAYOUT_BANK_SHA256')
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
SPECS = ((0xD978, 0xD992), (0xD992, 0xD9AC), (0xD9AC, 0xD9C6),
         (0xD9C6, 0xD9E0), (0xD9E0, 0xD9EE), (0xD9EE, 0xD9FC),
         (0xD9FC, 0xDA0A), (0xDA0A, 0xDA18), (0xDA18, 0xDA1A))
# Local already-fetched state/counter witnesses. They do not prove natural RAM
# reachability through earlier calls or exhaust all writers of F362/F36A.
WITNESSES = ((0, 0, 0xD978, -1), (7, 0, 0xDA18, 0xDA1A),
             (3, 10, 0xDA18, 0xDA1C), (3, 9, 0xDA0A, 0xDA1E),
             (3, 8, 0xD9FC, 0xDA20), (3, 7, 0xD9EE, 0xDA22),
             (3, 6, 0xD9E0, 0xDA24), (3, 5, 0xD9C6, 0xDA26),
             (3, 4, 0xD9AC, 0xDA28), (7, 6, 0xD992, 0xDA2A))
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def signed_WORD(value):
    value = uint(value, 65535, "WORD")
    return value - 65536 if value & 32768 else value


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    for start, end, expected in (PREFIX, CONSUMER):
        if sha(rom[start:end]) != expected:
            raise ValueError("complete pinned original call/selector/consumer differs")
    if sha(rom[SOURCE_START:SOURCE_END]) != SOURCE_SHA256:
        raise ValueError("original literal source differs")


def template_fixed(spec):
    start, end = spec
    return dict(id=f"rom_{start:06X}_stage_sprite_stream", start=start, end=end,
                record_count=(end - start - 2) // 6, terminator_WORD=0x8000)


def record_fixed(address):
    return dict(id=f"rom_{address:06X}_sprite_record", address=address)


def offset_fixed(index):
    return dict(id=f"stage_sprite_offset_{index:02d}", index=index,
                address=STREAM_END + 2 * index)


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(start=SOURCE_START, end=SOURCE_END, stream_bytes=162,
                            offset_WORD_bytes=18, sha256=SOURCE_SHA256),
        evidence=dict(
            source="original true call chain, selector instructions and AC08 WORD-read grammar",
            enhanced_ledger=dict(path=ENHANCED_PATH, sha256=ENHANCED_SHA256,
                local_call_selector_confidence="older_runtime_reachable_not_new_natural_proof",
                renderer_confidence="older_runtime_confirmed"),
            frozen_raw_layout=dict(id=LAYOUT_ID, bank00_sha256=LAYOUT_BANK_SHA256,
                emitted_raw_bytes=EDITABLE_BYTES, typed_overlap_bytes=0),
            pinned_prefix=dict(start=PREFIX[0], end=PREFIX[1], sha256=PREFIX[2]),
            consumer=dict(start=CONSUMER[0], end=CONSUMER[1], sha256=CONSUMER[2]),
            calls=dict(flag_bit_test=0xD8EC, flag_BYTE_RAM=0xFFF3A5, bit=2,
                before_A0_calls=[0xD8F4, 0xD8F8], A0_LEA=0xD8FC,
                A0_PC_base=0xD8FE, A0_displacement_WORD=0x007A,
                selector_BSR=0xD914, actual_AC08_JSR=0xD918),
            selector=dict(state_WORD_RAM=0xFFF362, counter_WORD_RAM=0xFFF36A,
                state3_gate="unsigned counter > 3",
                state3_index="LSL.W 1 of (10-counter).W; if subtraction N set, first CLR.W",
                state3_LEA=0xD946, state3_PC_base=0xD948,
                state3_displacement_WORD=0x00D4, state3_base=0xDA1C,
                state3_read=0xD94C, state3_ADDA_WORD=0xD950,
                state7_gate="unsigned counter <= 6",
                state7_index="LSL.W 2 of (counter-2).W; if subtraction N set, first CLR.W",
                state7_LEA=0xD96A, state7_PC_base=0xD96C,
                state7_displacement_WORD=0x00AE, state7_base=0xDA1A,
                state7_read=0xD970, state7_ADDA_WORD=0xD974,
                index_addressing="sign extend final shifted WORD before address addition",
                offset_addressing="ADDA.W sign extends fetched complete BE16 offset",
                physical_directory_count_is_not_CPU_clamp=True,
                FFFF_state3_alias=dict(read_address=0xDA32, original_WORD=0x6600,
                                     original_source=0x13F78, code_not_emitted=True)),
            sprite_source=dict(stride=6, WORD_order="big", X_offset=0,
                attribute_offset=2, packed_shape_Y_offset=4,
                X_or_first_8000_read=0xAC5E, first_8000_compare=0xAC60,
                packed_shape_Y_read=0xAC9C, attribute_read=0xACE8,
                source_advance=0xACF4, original_D2_WORD=0,
                original_D0_WORD=0x38, original_D1_WORD=0x80,
                original_local_origin_WORDs=[0xB8, 0x100],
                X_clip=[0x70, 0x160], Y_clip=[0x70, 0x1C0],
                F300_BYTE_unsigned_limit=80, entry_count_test=0xAC2C,
                accepted_increment=0xACE4, post_record_count_test=0xACF6,
                clipping_and_state_limit_can_stop_payload_reads=True,
                immutable_source_projection_only=True),
            local_read_witnesses=[dict(state_WORD=s, counter_WORD=c,
                original_source=p, offset_read_address=a) for s, c, p, a in WITNESSES]),
        source_business_names="unknown", natural_RAM_state_reachability="unknown",
        earlier_call_RAM_effects_and_all_state_writers="unknown",
        edited_gameplay_safety="unknown", independent_CPU_comparison=False,
        exclusions=dict(next_code_start=0xDA2C, next_code_not_emitted=True,
                        complete_RAM_renderer_bus_stack_not_modeled=True))


def pinned(row, fixed, mutable, label):
    keys(row, set(fixed) | set(mutable), label)
    for key, value in fixed.items():
        same(row[key], value, label + "." + key)


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result["templates"] = []
    for spec in SPECS:
        start, end = spec
        if rom[end - 2:end] != b"\x80\x00":
            raise ValueError("fixed original first terminator differs")
        rows = [dict(**record_fixed(p), X_WORD=int.from_bytes(rom[p:p + 2], "big"),
            attribute_WORD=int.from_bytes(rom[p + 2:p + 4], "big"),
            packed_shape_Y_WORD=int.from_bytes(rom[p + 4:p + 6], "big"))
            for p in range(start, end - 2, 6)]
        result["templates"].append(dict(**template_fixed(spec), records=rows))
    result["offsets"] = [dict(**offset_fixed(i),
        offset_WORD=int.from_bytes(rom[STREAM_END + 2 * i:STREAM_END + 2 * i + 2], "big"))
        for i in range(9)]
    blocks(rom, result)
    return result


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {"templates", "offsets"}, "stage sprite fields")
    result = []
    for row, spec in zip(exact_list(fields["templates"], 9, "physical streams"), SPECS):
        fixed = template_fixed(spec)
        pinned(row, fixed, {"records"}, "stream")
        data = bytearray()
        for i, item in enumerate(exact_list(row["records"], fixed["record_count"], "records")):
            pinned(item, record_fixed(fixed["start"] + 6 * i),
                   {"X_WORD", "attribute_WORD", "packed_shape_Y_WORD"}, "record")
            x = uint(item["X_WORD"], 65535, "X WORD")
            if x == 0x8000:
                raise ValueError("8000 is framing, not a record X WORD")
            for value in (x, uint(item["attribute_WORD"], 65535, "attribute WORD"),
                          uint(item["packed_shape_Y_WORD"], 65535, "packed shape/Y WORD")):
                data.extend(value.to_bytes(2, "big"))
        data.extend(b"\x80\x00")
        if len(data) != fixed["end"] - fixed["start"]:
            raise ValueError("fixed stream byte cost differs")
        result.append(dict(id=fixed["id"], start=fixed["start"], end=fixed["end"],
                           data=bytes(data), role="confirmed_AC08_source_WORD_records_and_first_term"))
    directory = bytearray()
    for i, row in enumerate(exact_list(fields["offsets"], 9, "physical offset WORDs")):
        pinned(row, offset_fixed(i), {"offset_WORD"}, "offset")
        directory.extend(uint(row["offset_WORD"], 65535, "full offset WORD").to_bytes(2, "big"))
    result.append(dict(id="rom_00DA1A_stage_sprite_offsets", start=STREAM_END, end=SOURCE_END,
                       data=bytes(directory), role="confirmed_signed_ADDA_WORD_offsets"))
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES or any(
            a["end"] != b["start"] for a, b in zip(result, result[1:])):
        raise ValueError("exact adjacent non-overlapping 180-byte scope differs")
    return result


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def lookup(image, state_WORD, counter_WORD, flag_BYTE=4):
    """Local selector source-read projection using live edited whole-image bytes.

    State/counter are already fetched RAM WORDs. No earlier callees, RAM writes,
    sprite queue, bus faults or natural state reachability are simulated here.
    Physical nine-slot allocation never restricts the original CPU index.
    """
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("complete bytes image required for lookup")
    state = uint(state_WORD, 65535, "state WORD")
    counter = uint(counter_WORD, 65535, "counter WORD")
    flag = uint(flag_BYTE, 255, "flag BYTE")
    result = dict(state_WORD=state, counter_WORD=counter, flag_BYTE=flag,
                  source_only=True, natural_execution=False, CPU_execution=False)
    if not flag & 4:
        return dict(**result, status="flag_bit2_clear_no_call")
    base, index, pc = -1, 0, -1
    if state == 3 and counter > 3:
        value = (10 - counter) & 65535
        if value & 32768: value = 0  # BPL tests subtraction N, not signed >= with V.
        index, base, pc = (value << 1) & 65535, 0xDA1C, 0xD94C
    elif state == 7 and counter <= 6:
        value = (counter - 2) & 65535
        if value & 32768: value = 0
        index, base, pc = (value << 2) & 65535, 0xDA1A, 0xD970
    if base == -1:
        return dict(**result, status="original_base_no_offset_read", source=SOURCE_START)
    address = base + signed_WORD(index)
    if not 0 <= address <= ROM_SIZE - 2:
        raise ValueError("lookup reached an out-of-ROM read boundary")
    value = int.from_bytes(image[address:address + 2], "big")
    source = (SOURCE_START + signed_WORD(value)) & 0xFFFFFFFF
    return dict(**result, status="offset_WORD_read", index_WORD=index, read_PC=pc,
        read_address=address, offset_WORD=value, source=source,
        read_inside_editable_directory=STREAM_END <= address < SOURCE_END,
        source_inside_stream_allocation=SOURCE_START <= source < STREAM_END,
        source_WORD_aligned=not bool(source & 1))


def source_view(image, start, x_origin_WORD=0xB8, y_origin_WORD=0x100,
                sprite_count_BYTE=0, *, record_budget=256):
    """Frozen original AC08 D2=0 live-image read plan, not a renderer or CPU.

    Origin inputs are already computed D3/D4; count is already fetched F300.
    Odd/out-of-ROM WORD reads and a diagnostic budget are explicit external
    boundaries, never replacements for a CPU clamp or a first terminator.
    """
    return ac08.source_view(image, start, x_origin_WORD, y_origin_WORD,
                            sprite_count_BYTE, record_budget=record_budget)


def source_reference_union(image):
    """Owned read union from disclosed local states and F300=0, not all reads."""
    addresses = set()
    ends = dict(SPECS)
    for state, counter, expected_source, expected_offset in WITNESSES:
        row = lookup(image, state, counter)
        if row["source"] != expected_source or row.get("read_address", -1) != expected_offset:
            raise ValueError("original local selector witness differs")
        if expected_offset != -1:
            addresses.update(range(expected_offset, expected_offset + 2))
        view = source_view(image, expected_source)
        if view["status"] != "first_8000_TERM" or view["next_source"] + 2 != ends[expected_source]:
            raise ValueError("original selected stream did not stop at its first term")
        for event in view["read_events"]:
            addresses.update(range(event["address"], event["address"] + event["bytes"]))
    return addresses


def schema():
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def exact(items):
        return dict(type="array", prefixItems=items, items=False, minItems=len(items), maxItems=len(items))
    def fixed(value):
        if type(value) is dict: return obj({k: fixed(v) for k, v in value.items()})
        if type(value) is list: return exact([fixed(v) for v in value])
        return dict(type={str: "string", int: "integer", bool: "boolean"}[type(value)], const=value)
    word = dict(type="integer", minimum=0, maximum=65535)
    props = {k: fixed(v) for k, v in metadata().items()}
    streams = []
    for spec in SPECS:
        row = template_fixed(spec)
        cells = [obj({**{k: fixed(v) for k, v in record_fixed(row["start"] + 6 * i).items()},
            "X_WORD": {**word, "not": {"const": 32768}},
            "attribute_WORD": word, "packed_shape_Y_WORD": word}) for i in range(row["record_count"])]
        streams.append(obj({**{k: fixed(v) for k, v in row.items()}, "records": exact(cells)}))
    props["templates"] = exact(streams)
    props["offsets"] = exact([obj({**{k: fixed(v) for k, v in offset_fixed(i).items()},
                                   "offset_WORD": word}) for i in range(9)])
    result = obj(props)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Full original WORD payloads and signed offsets; fixed first-8000 framing and physical editor counts are not CPU clamps or natural-domain proof."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    rows = blocks(rom, fields)
    actual = source_reference_union(rom)
    if image != rom or actual != set(range(SOURCE_START, SOURCE_END)):
        raise ValueError("serialized whole-ROM roundtrip or original owned read union differs")
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=10,
        stream_count=9, record_count=24, first_terminator_WORDs=9, offset_WORDs=9,
        local_owned_read_union_bytes=len(actual), local_witness_F300_BYTE=0,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        offset_WORDs_original=[row["offset_WORD"] for row in fields["offsets"]],
        full_WORD_code_alias=lookup(rom, 3, 65535),
        code_and_other_typed_resources_emitted=False,
        blocks=[{k: v for k, v in row.items() if k != "data"}
                | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in rows])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()),
               "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        physical_blocks=10, members={name: dict(bytes=len(data), sha256=sha(data))
                                    for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in stage sprite build scope or exact formal bundle")
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
        for name, data in members.items(): put(target / name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES,
                      members={name: sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS:
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
        if target is not None: put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=EDITABLE_BYTES,
                      exact_canonical=image == rom, bytes=len(image), sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
