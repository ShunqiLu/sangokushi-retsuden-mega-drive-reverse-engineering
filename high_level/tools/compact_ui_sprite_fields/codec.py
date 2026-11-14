"""170 actual source bytes: ten compact original AC08/AC10 sprite templates.

Records own full X, attribute and packed shape/Y WORDs, followed by the first
8000 X terminator. Only X=8000 is forbidden inside a fixed record. Actual clips
and the F300 BYTE cap can stop payload reads; physical counts are not CPU caps.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared
from tools.ui_cursor_sprite_templates import codec as ac08

ROOT=Path(__file__).resolve().parents[2]
ROM_SIZE=0x100000
ROM_SHA256=reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM=ROOT.parent/"work/original_g5510.bin"
OUTPUT_ROOT=ROOT/"build/compact_ui_sprite_fields"
FORMAL_ROOT=ROOT/"analysis/compact_ui_sprite_fields/generated"
DEFAULT_BUNDLE=FORMAL_ROOT
DEFAULT_FIELDS=FORMAL_ROOT/"fields.json"
EDITABLE_BYTES=170
FORMAT="g5510-compact-UI-sprite-source-WORD-fields-v1"
MAX_JSON=1024*1024
MEMBERS=frozenset(("fields.json","fields.schema.json","validation.json","manifest.json"))
# Begin/end, LEA, true JSR, actual entry, CLR D2, local already-computed X/Y origins.
SPECS=(
    (0x240E,0x2416,0x23F6,0x2406,0xAC08,0x2404,0xA0,0x98),
    (0xA198,0xA1B2,0xA174,0xA190,0xAC10,0xA182,0x80,0x80),
    (0x12CB6,0x12CBE,0x12C96,0x12CAE,0xAC08,0x12CAC,0xD8,0x120),
    (0x13FDC,0x13FE4,0x13FC0,0x13FD4,0xAC08,0x13FD2,0xD8,0x128),
    (0x14150,0x1416A,0x14128,0x14148,0xAC10,0x1413A,0x80,0x80),
    (0x1A244,0x1A25E,0x1A238,0x1A23C,0xAC08,0x1A236,0x80,0x80),
    (0x1B0EA,0x1B104,0x1B0D4,0x1B0E2,0xAC08,0x1B0E0,0xB0,0x168),
    (0x1EC18,0x1EC32,0x1EC0A,0x1EC10,0xAC08,0x1EC08,0x80,0x80),
    (0x20C54,0x20C5C,0x20C38,0x20C4C,0xAC08,0x20C4A,0xE0,0x110),
    (0x20D94,0x20D9C,0x20D78,0x20D8C,0xAC08,0x20D8A,0xF8,0x110),
)
SPANS=tuple((s,e) for s,e,*_ in SPECS)
SOURCE_SHA256=reference_value(__name__, 'SOURCE_SHA256')
CONSUMER=(0xAC08,0xAD06,reference_value(__name__, 'CONSUMER'))
CALLERS=(
    (0x23F6,0x240E,reference_value(__name__, 'CALLERS')),
    (0xA14E,0xA198,reference_value(__name__, 'CALLERS_2')),
    (0x12C84,0x12CB6,reference_value(__name__, 'CALLERS_3')),
    (0x13FAA,0x13FDC,reference_value(__name__, 'CALLERS_4')),
    (0x14120,0x14150,reference_value(__name__, 'CALLERS_5')),
    (0x1A200,0x1A244,reference_value(__name__, 'CALLERS_6')),
    (0x1B0C2,0x1B0EA,reference_value(__name__, 'CALLERS_7')),
    (0x1EBF6,0x1EC18,reference_value(__name__, 'CALLERS_8')),
    (0x20C30,0x20C54,reference_value(__name__, 'CALLERS_9')),
    (0x20D70,0x20D94,reference_value(__name__, 'CALLERS_10')),
)
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_BANK_HASHES=(
    (0,reference_value(__name__, 'LAYOUT_BANK_HASHES')),
    (1,reference_value(__name__, 'LAYOUT_BANK_HASHES_2')),
    (2,reference_value(__name__, 'LAYOUT_BANK_HASHES_3')),
)
ENHANCED_PATH="analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256=reference_value(__name__, 'ENHANCED_SHA256')
SOURCE_PLAN_PATH="tools/ui_cursor_sprite_templates/codec.py"
SOURCE_PLAN_SHA256=reference_value(__name__, 'SOURCE_PLAN_SHA256')
sha,dump=shared.sha,shared.dump
keys,same,uint,exact_list=shared.keys,shared.same,shared.uint,shared.exact_list
load_fields=shared.load_fields
safe_path,read_bounded,put=shared.safe_path,shared.read_bounded,shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE or sha(rom)!=ROM_SHA256:
        raise ValueError("complete canonical ROM bytes, size and SHA-256 required")
    for s,e,h in (CONSUMER,)+CALLERS:
        if sha(rom[s:e])!=h:raise ValueError("complete original reader/caller differs")
    if sha(b"".join(rom[s:e] for s,e in SPANS))!=SOURCE_SHA256:
        raise ValueError("original compact sprite source union differs")


def template_fixed(index):
    start,end,lea,call,target,d2,x,y=SPECS[index]
    return dict(id=f"rom_{start:06X}_compact_sprite_template",index=index,start=start,end=end,
        record_count=(end-start-2)//6,terminator_WORD=0x8000,terminator_address=end-2,
        source_LEA=lea,LEA_PC_base=lea+2,true_JSR=call,entry=target,D2_CLR_WORD=d2,
        original_D2_WORD=0,local_X_origin_WORD=x,local_Y_origin_WORD=y)


def record_fixed(address):
    return dict(id=f"rom_{address:06X}_sprite_record",address=address,
        X_address=address,attribute_address=address+2,packed_shape_Y_address=address+4)


def metadata():
    return dict(format=FORMAT,confidence="candidate",source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        physical_scope=[dict(start=s,end=e,bytes=e-s) for s,e in SPANS],source_union_sha256=SOURCE_SHA256,
        evidence=dict(source="original true AC08/AC10 callers, source WORD read order and conditional first-term closure",
            enhanced_ledger=dict(path=ENHANCED_PATH,sha256=ENHANCED_SHA256,
                renderer_confidence="runtime_confirmed",source_A198_caller_confidence="runtime_confirmed",
                other_source_callers_confidence="heuristic"),
            frozen_raw_layout=dict(id=LAYOUT_ID,banks=[dict(bank=b,sha256=h) for b,h in LAYOUT_BANK_HASHES],
                emitted_raw_bytes=EDITABLE_BYTES,older_typed_overlap_bytes=0),
            consumer=dict(start=CONSUMER[0],end=CONSUMER[1],sha256=CONSUMER[2]),
            callers=[dict(start=s,end=e,sha256=h) for s,e,h in CALLERS],
            original_call_paths=[template_fixed(i) for i in range(10)],
            entry_distinction=dict(AC08_clear_camera_WORDs=[0xAC08,0xAC0C],camera_WORD_RAM=[0xFFFFF60A,0xFFFFF60E],
                AC10_does_not_clear_camera=True,AC10_sources=[0xA198,0x14150],
                caller_camera_copies=dict(A198=[0xA184,0xA18A],source_14150=[0x1413C,0x14142]),
                origin_formula="D3.W=(D0.W-F60A.W+0080)&FFFF; D4.W=(D1.W-F60E.W+0080)&FFFF",
                all_local_D2_WORDs_cleared=True,original_flip_branches_not_taken=True),
            source_format=dict(WORD_order="big",stride=6,X_offset=0,attribute_offset=2,packed_shape_Y_offset=4,
                X_or_first_8000_READ=0xAC5E,first_8000_compare=0xAC60,
                first_8000_branch=0xAC64,packed_shape_Y_READ=0xAC9C,attribute_READ=0xACE8,
                source_advance=0xACF4,only_X_8000_is_framing=True,
                attribute_all16_bits_retained=True,packed_all16_bits_retained=True,
                packed_Y="sign extended low12 bits; high4 shape bits retained separately by original LONG shift",
                attribute_path="complete source attribute WORD EOR masked D2.W; original local D2=0",
                term_has_no_attribute_or_packed_reads=True,physical_record_count_not_CPU_cap=True),
            conditional_reads=dict(unsigned_X_clip=[0x70,0x160],unsigned_Y_clip=[0x70,0x1C0],
                packed_only_read_after_X_clip=True,attribute_only_read_after_Y_clip=True,
                F300_unsigned_BYTE_limit=80,entry_limit_PC=0xAC2C,post_record_limit_PC=0xACF6,
                accepted_BYTE_increment=0xACE4,count_or_clip_can_prevent_payload_reads=True),
            local_witnesses=[dict(source=s,already_computed_D3_WORD=x,already_computed_D4_WORD=y,
                already_fetched_F300_BYTE=0,already_cleared_D2_WORD=0,
                upstream_RAM_and_gate_reachability="unknown") for s,_,_,_,_,_,x,y in SPECS],
            frozen_pure_source_read_plan=dict(path=SOURCE_PLAN_PATH,sha256=SOURCE_PLAN_SHA256,
                edited_whole_image=True,canonical_extract_not_required_for_diagnostic=True,
                immutable_source_projection_not_CPU=True)),
        business_names_and_natural_RAM_selection="unknown",all_callers_and_RAM_writers="unknown",
        edited_gameplay_safety="unknown",independent_CPU_comparison=False,
        complete_renderer_RAM_queue_VDP_bus_stack_CCR="not modeled",
        exclusions=dict(nearby_glyphs_zero_gaps_code_and_other_typed_neighbors_not_emitted=True))


def pinned(row,fixed,mutable,label):
    keys(row,set(fixed)|set(mutable),label)
    for key,value in fixed.items():same(row[key],value,label+"."+key)


def extract(rom):
    verify_rom(rom)
    result=metadata();result["templates"]=[]
    for i,(start,end,*_) in enumerate(SPECS):
        if rom[end-2:end]!=b"\x80\x00":raise ValueError("original first terminator differs")
        records=[dict(**record_fixed(p),X_WORD=int.from_bytes(rom[p:p+2],"big"),
            attribute_WORD=int.from_bytes(rom[p+2:p+4],"big"),
            packed_shape_Y_WORD=int.from_bytes(rom[p+4:p+6],"big")) for p in range(start,end-2,6)]
        result["templates"].append(dict(**template_fixed(i),records=records))
    blocks(rom,result)
    return result


def blocks(rom,fields):
    verify_rom(rom)
    pinned(fields,metadata(),{"templates"},"compact sprite package")
    result=[]
    for i,template in enumerate(exact_list(fields["templates"],10,"ten physical templates")):
        fixed=template_fixed(i);pinned(template,fixed,{"records"},"fixed template")
        data=bytearray()
        for j,record in enumerate(exact_list(template["records"],fixed["record_count"],"physical records")):
            pinned(record,record_fixed(fixed["start"]+6*j),{"X_WORD","attribute_WORD","packed_shape_Y_WORD"},"record")
            x=uint(record["X_WORD"],65535,"complete X WORD")
            if x==0x8000:raise ValueError("X 8000 is first-term framing, not a record")
            for word in (x,uint(record["attribute_WORD"],65535,"complete attribute WORD"),
                         uint(record["packed_shape_Y_WORD"],65535,"complete packed shape/Y WORD")):
                data.extend(word.to_bytes(2,"big"))
        data.extend(b"\x80\x00")
        if len(data)!=fixed["end"]-fixed["start"]:raise ValueError("fixed template byte cost differs")
        result.append(dict(id=fixed["id"],start=fixed["start"],end=fixed["end"],data=bytes(data),
            role="confirmed_AC08_AC10_compact_source_WORD_records_and_first_term"))
    if sum(len(r["data"]) for r in result)!=EDITABLE_BYTES or any(a["end"]>b["start"] for a,b in zip(result,result[1:])):
        raise ValueError("disjoint exact 170-byte source scope differs")
    return result


def rebuild(rom,fields):
    rows=blocks(rom,fields);image=bytearray(rom)
    for row in rows:image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def source_view(image,start,x_origin_WORD,y_origin_WORD,sprite_count_BYTE=0,*,record_budget=256):
    """Original D2=0 immutable-source read projection on a live edited image.

    Origin/count inputs are already computed/fetched WORD/WORD/BYTE values.
    Exceptions for odd/out-of-ROM reads denote external boundaries, never
    catalog clamps. No RAM writes, flips, interrupts or CPU faults are modeled.
    """
    return ac08.source_view(image,start,x_origin_WORD,y_origin_WORD,sprite_count_BYTE,record_budget=record_budget)


def source_reference_union(image):
    """Disclosed local origins/count=0 witnesses, not natural execution proof."""
    addresses=set()
    for start,end,_,_,_,_,x,y in SPECS:
        view=source_view(image,start,x,y)
        if view["status"]!="first_8000_TERM" or view["next_source"]!=end-2:
            raise ValueError("original local witness did not reach its first term")
        if not all(row["accepted"] for row in view["records"]):
            raise ValueError("original local witness did not read each complete record")
        for event in view["read_events"]:addresses.update(range(event["address"],event["address"]+2))
    return addresses


def schema():
    def obj(props):return dict(type="object",properties=props,required=list(props),additionalProperties=False)
    def exact(items):return dict(type="array",prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def fixed(value):
        if type(value) is dict:return obj({k:fixed(v) for k,v in value.items()})
        if type(value) is list:return exact([fixed(v) for v in value])
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    word=dict(type="integer",minimum=0,maximum=65535)
    props={k:fixed(v) for k,v in metadata().items()}
    props["templates"]=exact([obj({**{k:fixed(v) for k,v in template_fixed(i).items()},
        "records":exact([obj({**{k:fixed(v) for k,v in record_fixed(spec[0]+6*j).items()},
            "X_WORD":{**word,"not":{"const":32768}},"attribute_WORD":word,"packed_shape_Y_WORD":word})
            for j in range((spec[1]-spec[0]-2)//6)])}) for i,spec in enumerate(SPECS)])
    result=obj(props);result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="Full X/attribute/packed shape-Y WORDs; only X8000 is first-term framing. Actual clips/state cap and edited whole-image source diagnostics are retained, not replaced by physical catalog counts."
    return result


def render_bundle(rom):
    fields=extract(rom);serialized=dump(fields);image=rebuild(rom,load_fields(serialized))
    rows=blocks(rom,fields);expected={p for s,e in SPANS for p in range(s,e)}
    if image!=rom or source_reference_union(rom)!=expected or len(expected)!=EDITABLE_BYTES:
        raise ValueError("serialized whole-ROM roundtrip or conditional source read union differs")
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=10,templates=10,records=25,first_term_WORDs=10,
        local_owned_read_union_bytes=len(expected),whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        original_local_read_plans=[source_view(rom,s,x,y) for s,_,_,_,_,_,x,y in SPECS],
        neighbors_and_code_emit_bytes=0,
        blocks=[{k:v for k,v in r.items() if k!="data"}|dict(bytes=len(r["data"]),sha256=sha(r["data"])) for r in rows])
    members={"fields.json":serialized,"fields.schema.json":dump(schema()),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=10,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError("output must stay in compact sprite build scope or exact formal bundle")
    if path.exists() or not path.parent.is_dir():raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM));parser.add_argument("--fields")
    parser.add_argument("--bundle");parser.add_argument("--output")
    args=parser.parse_args(argv);target=None
    if args.command=="export":
        if args.output is None or args.fields is not None or args.bundle is not None:raise ValueError("export requires fresh output only")
        target=fresh_output(args.output,bundle=True)
    elif args.command=="import":
        if args.output is None or args.bundle is not None:raise ValueError("import requires fields and fresh output")
        target=fresh_output(args.output)
        if target.suffix.lower()!=".bin":raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.bundle is not None and args.fields is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=="export":
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={name:sha(data) for name,data in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS:raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data:raise ValueError("canonical generated bundle drift: "+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON));image=rebuild(rom,fields)
        if target is not None:put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=EDITABLE_BYTES,
            exact_canonical=image==rom,bytes=len(image),sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=="__main__":raise SystemExit(main())
