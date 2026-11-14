"""246 actual source bytes with three distinct original reader contracts.

BYTE factor/bias pairs, counted repeat-WORD UI rows, and WORD state/dispatch
sources are separate field roles. Fixed editor extents never clamp CPU inputs.
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
OUTPUT_ROOT = ROOT / "build/ui_runtime_source_fields"
FORMAL_ROOT = ROOT / "analysis/ui_runtime_source_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-BYTE-parameter-counted-UI-WORD-state-dispatch-sources-v1"
EDITABLE_BYTES = 246
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
MAP_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
MAP_SHA256 = reference_value(__name__, 'MAP_SHA256')
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
SOURCE_HASHES = (
    (0x11380, 0x113BC, reference_value(__name__, 'SOURCE_HASHES')),
    (0x134CC, 0x13510, reference_value(__name__, 'SOURCE_HASHES_2')),
    (0x6773C, 0x677B2, reference_value(__name__, 'SOURCE_HASHES_3')),
)
BODIES = (
    (0x11258, 0x1125C, reference_value(__name__, 'BODIES')),
    (0x11312, 0x11380, reference_value(__name__, 'BODIES_2')),
    (0x83D4, 0x83FA, reference_value(__name__, 'BODIES_3')),
    (0x13482, 0x134CC, reference_value(__name__, 'BODIES_4')),
    (0x26BFA, 0x26C72, reference_value(__name__, 'BODIES_5')),
    (0x676C4, 0x6773C, reference_value(__name__, 'BODIES_6')),
)
STREAMS = (
    (0x134CC, 0x134E4, 11, 6, 0x13490, 0x13494, 0xC09C),
    (0x134E4, 0x13500, 15, 7, 0x134A8, 0x134AC, 0xC494),
    (0x13500, 0x13510, 13, 4, 0x134C0, 0x134C4, 0xC0B4),
)
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


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_format_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(emit_BYTES=246, factor_bias_BYTEs=60, counted_UI_source_BYTEs=68,
            state_pair_WORD_BYTEs=16, relative_call_WORD_BYTEs=102,
            ranges=[dict(start=s, end=e, bytes=e-s) for s, e, _ in SOURCE_HASHES]),
        evidence=dict(consumers=[dict(start=s, end=e, sha256=h) for s,e,h in BODIES],
            original_ledger=dict(path=MAP_PATH, sha256=MAP_SHA256, reachability_confidence="heuristic"),
            accepted_raw_snapshot=dict(layout=LAYOUT_ID, resources=61, raw_BYTES=47829,
                source_raw_difference_BYTES=246, source_typed_overlap_BYTES=0),
            factor_bias=dict(caller=0x11258, entry=0x11312, RNG_call=0x11312, RNG_entry=0x83D4,
                seed_LONG_read_write_RAM=0xFFF61C, post_RNG_multiply_WORD_read=0x11370,
                post_RNG_multiply_RAM_WORD=0xFFF61C,
                parameter_axis_BYTE_read=0x11320, parameter_axis_RAM_base=0xFFC300,
                masked_axis_BYTE_read=0x11358, masked_axis_RAM_base=0xFFC700,
                officer_index_WORD_RAM=0xFFF3A6, officer_index_signed_before_RAM_base_add=True,
                unsigned_BYTE_thresholds=[30,50,70,80,90], bucket_count=6,
                pair_index="5*bucket+(second_axis_BYTE&7)", constructed_pair_indices=list(range(33)),
                LEA_PC=0x11364, PC_base=0x11366, displacement_WORD=0x1A, source=0x11380,
                factor_BYTE_read=0x1136C, bias_BYTE_read=0x11378,
                arithmetic="MULU.W factor_BYTE*post_RNG_seed_WORD; SWAP; ADD.W bias_BYTE",
                catalog_pairs=30, code_alias_pair_indices=[30,31,32], natural_domain="unknown"),
            counted_UI=dict(entry=0x26BFA, source_WORD_read=0x26C10, negative_branch=0x26C12,
                dispatch_directory=0x26C4C, dispatch_WORD_read=0x26C2E,
                dispatch_call=0x26C32, dispatch_target_base=0x26C58,
                repeat_handler=0x26C58, repeat_payload_WORD_read=0x26C5E,
                repeat_count_mask=255, row_remaining_subtract=0x26C6C,
                row_remaining_test=0x26C36, row_DBRA=0x26C3A,
                stop="original row count and emitted width, not a source terminator",
                original_payload_zero_role="consumed tile attribute WORD, not padding"),
            state_pairs=dict(caller=0x6771C, entry=0x67728, selector_RAM_WORD=0xFFF6C4,
                shift_WORD_bits=2, first_PC=0x6772E, first_PC_base=0x67730,
                first_displacement_WORD=12, second_PC=0x67734, second_PC_base=0x67736,
                second_displacement_WORD=8, first_RAM_WORD=0xFFF612, second_RAM_WORD=0xFFF362,
                physical_pairs=4, static_selector_writers=[dict(PC=p,WORD=w) for p,w in
                    ((0xE60,0),(0xE0A,1),(0xDCC,2),(0xE14,3))], natural_domain="unknown"),
            dispatch=dict(entry=0x676C4, selector_RAM_WORD=0xFFF380,
                unsigned_guard_PC=0x676C8, unsigned_minimum_WORD=0x60,
                subtract_PC=0x676DE, shift_WORD_bits=1, read_PC=0x676E4,
                PC_base=0x676E6, displacement_WORD=0x66, source=0x6774C,
                target_LEA_PC=0x676E8, target_PC_base=0x676EA, target_displacement_WORD=0xC8,
                target_base=0x677B2, call_PC=0x676EE, call_mode="JSR(A0,D0.W) signed WORD",
                physical_WORDs=51, constructed_selector_WORDs=list(range(0x60,0x93)),
                lower_guard_path_source=0x676D6, lower_guard_path_is_call=False,
                catalog_capacity_is_CPU_clamp=False, natural_domain="unknown")),
        independent_CPU_comparison=False, claims=dict(all_fields_lossless=True,
            full_gameplay_rule_recovery=False, complete_natural_parameter_domain=False,
            CPU_selector_clamp=False, whole_CPU_execution=False))


def pinned(value, expected, mutable, label):
    keys(value, {*expected, *mutable}, label)
    for key, original in expected.items():
        same(value[key], original, label+"."+key)


def pair_fixed(index):
    bucket, low = divmod(index, 5)
    return dict(id=f"rom_{0x11380+2*index:06X}_factor_bias", pair_index=index,
        start=0x11380+2*index, end=0x11382+2*index,
        constructed_witness=dict(first_axis_BYTE=(0,31,51,71,81,91)[bucket], second_axis_BYTE=low),
        business_meaning_confidence="unknown")


def stream_fixed(index):
    start,end,columns,lines,LEA,call,VDP = STREAMS[index]
    return dict(id=f"rom_{start:06X}_counted_repeat_UI", start=start, end=end,
        columns=columns, lines=lines, original_D0_LONG=0xC0000000|columns,
        original_D1_WORD=lines, original_D2_WORD=VDP, original_LEA_PC=LEA,
        original_call_PC=call, source_stop="row counter and width", original_attribute_OR_WORD=0xC000)


def row_fixed(stream_index, row_index):
    start = STREAMS[stream_index][0]+4*row_index
    return dict(row_index=row_index, start=start, end=start+4, kind="repeat_WORD",
        control_WORD=0x8000|STREAMS[stream_index][2], emitted_cells=STREAMS[stream_index][2],
        dispatch_BYTE_offset=0, handler=0x26C58, payload_address=start+2)


def state_fixed(index):
    start=0x6773C+4*index
    return dict(id=f"rom_{start:06X}_state_pair", slot=index, start=start, end=start+4,
        constructed_selector_WORD=index, first_RAM_WORD=0xFFF612, second_RAM_WORD=0xFFF362)


def call_fixed(index):
    start=0x6774C+2*index
    return dict(id=f"rom_{start:06X}_relative_call", slot=index, start=start, end=start+2,
        constructed_selector_WORD=0x60+index, target_base=0x677B2, encoding="BE16 signed offset")


def image_only(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("live source view requires complete bytes image")


def word(image, address):
    if not 0 <= address <= ROM_SIZE-2:
        raise ValueError("source WORD beyond provided ROM image")
    return int.from_bytes(image[address:address+2], "big")


def s16(value):
    return value-0x10000 if value & 0x8000 else value


def factor_source_view(image, first_axis_BYTE, second_axis_BYTE):
    """Only original source address/read projection; does not call or replace RNG."""
    image_only(image)
    first=uint(first_axis_BYTE,255,"first axis BYTE")
    second=uint(second_axis_BYTE,255,"second axis BYTE")
    bucket=sum(first > threshold for threshold in (30,50,70,80,90))
    index=5*bucket+(second & 7)
    address=0x11380+2*index
    return dict(bucket=bucket, pair_index=index, factor_address=address, bias_address=address+1,
        factor_BYTE=image[address], bias_BYTE=image[address+1], admitted_field_pair=index < 30,
        code_alias=index >= 30, RNG_executed=False)


def state_source_view(image, selector_WORD):
    image_only(image)
    selector=uint(selector_WORD,0xFFFF,"state selector WORD")
    offset=s16((selector << 2) & 0xFFFF)
    first, second=0x6773C+offset, 0x6773E+offset
    return dict(selector_WORD=selector, signed_offset=offset, first_address=first, second_address=second,
        first_WORD=word(image,first), second_WORD=word(image,second),
        admitted_field_pair=0x6773C <= first < 0x6774C)


def dispatch_source_view(image, selector_WORD):
    image_only(image)
    selector=uint(selector_WORD,0xFFFF,"dispatch selector WORD")
    if selector < 0x60:
        address=0x676D6+s16((selector << 1)&0xFFFF)
        return dict(selector_WORD=selector, call_path=False, source_address=address,
            WORD=word(image,address), admitted_field_WORD=False)
    address=0x6774C+s16((((selector-0x60)&0xFFFF)<<1)&0xFFFF)
    offset=word(image,address)
    return dict(selector_WORD=selector, call_path=True, source_address=address, offset_WORD=offset,
        signed_call_offset=s16(offset), target=0x677B2+s16(offset),
        admitted_field_WORD=0x6774C <= address < 0x677B2,
        target_execution_simulated=False)


def stream_source_view(image, index):
    image_only(image)
    uint(index,2,"counted stream index")
    rows=[]
    for row_index in range(STREAMS[index][3]):
        fixed=row_fixed(index,row_index)
        if word(image,fixed["start"]) != fixed["control_WORD"]:
            raise ValueError("source framing outside admitted original repeat grammar")
        payload=word(image,fixed["payload_address"])
        rows.append(dict(**fixed,payload_WORD=payload,
            emitted_attribute_WORD=payload | 0xC000))
    return dict(**stream_fixed(index), rows=rows, VDP_or_RAM_execution_simulated=False)


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),
        factor_bias_pairs=[dict(**pair_fixed(i),factor_BYTE=rom[0x11380+2*i],
            bias_BYTE=rom[0x11381+2*i]) for i in range(30)],
        counted_UI_streams=[dict(**stream_fixed(i),rows=[dict(**row_fixed(i,j),
            payload_WORD=word(rom,STREAMS[i][0]+4*j+2)) for j in range(STREAMS[i][3])]) for i in range(3)],
        state_pairs=[dict(**state_fixed(i),first_WORD=word(rom,0x6773C+4*i),
            second_WORD=word(rom,0x6773E+4*i)) for i in range(4)],
        relative_calls=[dict(**call_fixed(i),offset_WORD=word(rom,0x6774C+2*i)) for i in range(51)])


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields,metadata(),{"factor_bias_pairs","counted_UI_streams","state_pairs","relative_calls"},"source package")
    raw=bytearray()
    for i,pair in enumerate(exact_list(fields["factor_bias_pairs"],30,"factor/bias physical pairs")):
        pinned(pair,pair_fixed(i),{"factor_BYTE","bias_BYTE"},"factor/bias pair")
        raw.extend((uint(pair["factor_BYTE"],255,"factor BYTE"),uint(pair["bias_BYTE"],255,"bias BYTE")))
    result=[dict(id="rom_011380_factor_bias_BYTE_pairs",start=0x11380,end=0x113BC,
        data=bytes(raw),role="confirmed_BYTE_factor_bias_source")]
    for i,stream in enumerate(exact_list(fields["counted_UI_streams"],3,"counted source streams")):
        pinned(stream,stream_fixed(i),{"rows"},"counted stream")
        raw=bytearray()
        for j,row in enumerate(exact_list(stream["rows"],STREAMS[i][3],"source rows")):
            pinned(row,row_fixed(i,j),{"payload_WORD"},"repeat source row")
            raw.extend(row["control_WORD"].to_bytes(2,"big"))
            raw.extend(uint(row["payload_WORD"],0xFFFF,"complete repeat payload WORD").to_bytes(2,"big"))
        result.append(dict(id=stream["id"],start=stream["start"],end=stream["end"],
            data=bytes(raw),role="confirmed_counted_repeat_WORD_UI_source"))
    raw=bytearray()
    for i,pair in enumerate(exact_list(fields["state_pairs"],4,"state physical pairs")):
        pinned(pair,state_fixed(i),{"first_WORD","second_WORD"},"state pair")
        for key in ("first_WORD","second_WORD"):
            raw.extend(uint(pair[key],0xFFFF,"complete state WORD").to_bytes(2,"big"))
    result.append(dict(id="rom_06773C_state_WORD_pairs",start=0x6773C,end=0x6774C,
        data=bytes(raw),role="confirmed_state_WORD_pair_source"))
    raw=bytearray()
    for i,call in enumerate(exact_list(fields["relative_calls"],51,"relative call WORDs")):
        pinned(call,call_fixed(i),{"offset_WORD"},"relative call source")
        raw.extend(uint(call["offset_WORD"],0xFFFF,"complete relative call WORD").to_bytes(2,"big"))
    result.append(dict(id="rom_06774C_relative_call_WORDs",start=0x6774C,end=0x677B2,
        data=bytes(raw),role="confirmed_signed_relative_JSR_WORD_source"))
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES:
        raise ValueError("fixed246 source byte cost differs")
    return result


def rebuild(rom, fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):
        image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def schema(rom):
    def obj(properties):
        return dict(type="object",properties=properties,required=list(properties),additionalProperties=False)
    def exact(items):
        return dict(type="array",prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def fixed(value):
        if type(value) is dict:
            return obj({k:fixed(v) for k,v in value.items()})
        if type(value) is list:
            return exact([fixed(v) for v in value])
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    def mutable(row,fields):
        return obj({k:dict(type="integer",minimum=0,maximum=fields[k]) if k in fields else fixed(v)
            for k,v in row.items()})
    original=extract(rom)
    properties={k:fixed(v) for k,v in metadata().items()}
    properties["factor_bias_pairs"]=exact([mutable(row,{"factor_BYTE":255,"bias_BYTE":255}) for row in original["factor_bias_pairs"]])
    streams=[]
    for stream in original["counted_UI_streams"]:
        stream_fields={k:fixed(v) for k,v in stream.items() if k != "rows"}
        stream_fields["rows"]=exact([mutable(row,{"payload_WORD":0xFFFF}) for row in stream["rows"]])
        streams.append(obj(stream_fields))
    properties["counted_UI_streams"]=exact(streams)
    properties["state_pairs"]=exact([mutable(row,{"first_WORD":0xFFFF,"second_WORD":0xFFFF}) for row in original["state_pairs"]])
    properties["relative_calls"]=exact([mutable(row,{"offset_WORD":0xFFFF}) for row in original["relative_calls"]])
    result=obj(properties)
    result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="Three separate reader roles; fixed physical editor costs, no CPU clamp or target restriction."
    return result


def render_bundle(rom):
    fields=extract(rom)
    serialized=dump(fields)
    image=rebuild(rom,load_fields(serialized))
    if image != rom:
        raise ValueError("serialized source whole-ROM roundtrip differs")
    encoded=blocks(rom,fields)
    report=dict(**metadata(),editable_bytes=246,physical_blocks=6,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),
        factor_pair_witnesses=[factor_source_view(image,**p["constructed_witness"]) for p in fields["factor_bias_pairs"]],
        factor_code_aliases=[factor_source_view(image,91,i) for i in (5,6,7)],
        counted_UI_source_views=[stream_source_view(image,i) for i in range(3)],
        state_pair_witnesses=[state_source_view(image,i) for i in range(4)],
        original_call_source_views=[dispatch_source_view(image,i) for i in range(0x60,0x93)],
        dispatch_aliases=[dispatch_source_view(image,i) for i in (0x93,0x8060,0xFFFF)],
        blocks=[{k:v for k,v in r.items() if k != "data"} | dict(bytes=len(r["data"]),sha256=sha(r["data"])) for r in encoded])
    members={"fields.json":serialized,"fields.schema.json":dump(schema(rom)),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=246,physical_blocks=6,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("dedicated fresh output or exact formal bundle required")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM)); parser.add_argument("--fields")
    parser.add_argument("--bundle"); parser.add_argument("--output")
    args=parser.parse_args(argv)
    target=None
    if args.command == "export":
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError("export requires fresh output only")
        target=fresh_output(args.output,bundle=True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None:
            raise ValueError("import requires fields and fresh output")
        target=fresh_output(args.output)
        if target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command == "export":
        members=render_bundle(rom); target.mkdir()
        for name,data in members.items(): put(target/name,data)
        result=dict(path=str(target),editable_bytes=246,members={name:sha(data) for name,data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: "+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=246,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None: put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=246,
            exact_canonical=image == rom,bytes=len(image),sha256=sha(image))
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
