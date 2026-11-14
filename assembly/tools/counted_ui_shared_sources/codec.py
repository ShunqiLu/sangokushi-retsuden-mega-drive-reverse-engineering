"""96 counted UI bytes from three repeat sources and four original callers."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
import json
from pathlib import Path
from tools.counted_ui_row_sources import codec as old

ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=old.DEFAULT_ROM
ROM_SIZE,ROM_SHA256=old.ROM_SIZE,old.ROM_SHA256
OUTPUT_ROOT=ROOT/"build/counted_ui_shared_sources"
FORMAL_ROOT=ROOT/"analysis/counted_ui_shared_sources/generated"
DEFAULT_FIELDS=FORMAL_ROOT/"fields.json"
MAX_JSON=1024*1024
EDITABLE_BYTES=96
MEMBERS=old.MEMBERS
FORMAT="g5510-three-shared-counted-UI-repeat-WORD-sources-v1"
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH="build/direct_code/night-gnu-54aiz6ts/layout-canonical/"+LAYOUT_ID
FROZEN_READER_PATH="tools/counted_ui_row_sources/codec.py"
FROZEN_READER_SHA256=reference_value(__name__, 'FROZEN_READER_SHA256')
SOURCES=((0x3138A,0x313A6,38,7),(0x315EA,0x31612,6,10),(0x20DA2,0x20DBE,12,7))
SOURCE_HASHES=(reference_value(__name__, 'SOURCE_HASHES'),
    reference_value(__name__, 'SOURCE_HASHES_2'),
    reference_value(__name__, 'SOURCE_HASHES_3'))
# Source role, setup start/end, actual LEA/call, D1 rows, D2 destination, body SHA.
CALLERS=(
    (0,0x319E0,0x319F8,0x319EE,0x319F2,7,0xCA02,reference_value(__name__, 'CALLERS')),
    (1,0x3158E,0x315A8,0x3158E,0x315A0,10,0xC3A2,reference_value(__name__, 'CALLERS_2')),
    (2,0x21024,0x2103C,0x21024,0x21036,6,0xC19C,reference_value(__name__, 'CALLERS_3')),
    (2,0x2103C,0x21054,0x2103C,0x2104E,7,0xC51C,reference_value(__name__, 'CALLERS_4')))
sha,dump=old.sha,old.dump
uint,exact_list,pinned=old.uint,old.exact_list,old.pinned
load_fields,safe_path,read_bounded,put=old.load_fields,old.safe_path,old.read_bounded,old.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE or sha(rom)!=ROM_SHA256:
        raise ValueError("canonical complete source ROM required")
    for _,start,end,*_,digest in CALLERS:
        if sha(rom[start:end])!=digest:raise ValueError("original complete setup/call source differs")
    start,end,digest=old.READER
    if sha(rom[start:end])!=digest:raise ValueError("original 26BFA reader differs")
    for (start,end,*_),digest in zip(SOURCES,SOURCE_HASHES):
        if sha(rom[start:end])!=digest:raise ValueError("original repeat source differs")


def metadata():
    return dict(format=FORMAT,confidence="candidate",source_format_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        physical_scope=[dict(start=s,end=e,bytes=e-s,sha256=h) for (s,e,*_),h in zip(SOURCES,SOURCE_HASHES)],
        evidence=dict(original_reader=dict(start=old.READER[0],end=old.READER[1],sha256=old.READER[2]),
            frozen_pure_validation=dict(path=FROZEN_READER_PATH,sha256=FROZEN_READER_SHA256),
            original_ledger=dict(path=old.MAP_PATH,sha256=old.MAP_SHA256,reachability_confidence="heuristic"),
            accepted_77_raw_snapshot=dict(layout=LAYOUT_ID,path=LAYOUT_PATH,raw_BYTES=45022,
                newly_admitted_BYTES=96,older_typed_overlap_BYTES=0),
            callers=[dict(source_role=r,setup_start=s,setup_end=e,LEA=lea,true_JSR=call,sha256=h,
                D0_LONG=0xC0000000|SOURCES[r][2],D1_WORD=n,D2_WORD=dest,source_stop=SOURCES[r][0]+4*n)
                for r,s,e,lea,call,n,dest,h in CALLERS],
            actual_grammar=dict(source_WORD_read=0x26C10,sign_branch=0x26C12,
                selector_formula="((control_WORD&7FFF)>>7)&FFFE",only_observed_selector=0,
                dispatch_directory=0x26C4C,dispatch_WORD_read=0x26C2E,dispatch_call=0x26C32,
                handler=0x26C58,low_BYTE_count=0x26C58,payload_WORD_read=0x26C5E,
                remaining_width_subtract=0x26C6C,row_remaining_test=0x26C36,row_DBRA=0x26C3A,
                original_attribute_OR_WORD=0xC000,stop="exact original column count and D1 rows, no marker"),
            shared_prefix=dict(source=0x20DA2,first_true_JSR=0x21036,first_rows=6,first_stop=0x20DBA,
                second_true_JSR=0x2104E,second_rows=7,second_stop=0x20DBE,physical_emit_count=1),
            zero_payloads_are_consumed_full_WORDs_not_padding=True),
        exclusions=dict(old304_not_changed_or_reemitted=True,unobserved_direct_ascending_numeric_grammar_not_added=True,
            nearby_code_and_unread_tails_not_emitted=True),
        source_business_names_and_natural_execution="unknown",all_callers_and_RAM_writers="unknown",
        edited_gameplay_safety="unknown",independent_CPU_comparison=False,
        complete_RAM_VDP_queue_bus_CCR_stack_and_business_algorithm="not modeled")


def source_fixed(role):
    start,end,columns,rows=SOURCES[role]
    return dict(source_role=role,id=f"rom_{start:06X}_counted_repeat_WORD_source",start=start,end=end,
        columns=columns,physical_rows=rows,WORD_order="big")


def row_fixed(role,index):
    p=SOURCES[role][0]+4*index
    return dict(index=index,start=p,end=p+4,control_WORD=0x8000|SOURCES[role][2],
        emitted_cells=SOURCES[role][2],dispatch_BYTE_offset=0,handler=0x26C58)


def extract(rom):
    verify_rom(rom)
    result=metadata();sources=[]
    for r,(start,end,columns,rows) in enumerate(SOURCES):
        values=[]
        for i in range(rows):
            p=start+4*i
            if int.from_bytes(rom[p:p+2],"big")!=0x8000|columns:raise ValueError("original exact repeat framing differs")
            values.append(dict(**row_fixed(r,i),payload_WORD=int.from_bytes(rom[p+2:p+4],"big")))
        sources.append(dict(**source_fixed(r),rows=values))
    result["repeat_sources"]=sources
    return result


def blocks(rom,fields):
    verify_rom(rom);pinned(fields,metadata(),{"repeat_sources"},"counted repeat package");result=[]
    for r,source in enumerate(exact_list(fields["repeat_sources"],3,"three actual sources")):
        fixed=source_fixed(r);pinned(source,fixed,{"rows"},"fixed physical repeat source");data=bytearray()
        for i,row in enumerate(exact_list(source["rows"],fixed["physical_rows"],"fixed physical rows")):
            pinned(row,row_fixed(r,i),{"payload_WORD"},"exact original repeat control")
            data.extend(row["control_WORD"].to_bytes(2,"big"))
            data.extend(uint(row["payload_WORD"],65535,"complete repeated payload WORD").to_bytes(2,"big"))
        result.append(dict(id=fixed["id"],start=fixed["start"],end=fixed["end"],data=bytes(data),
            role="confirmed_counted_repeat_full_WORD_source"))
    if sum(len(r["data"]) for r in result)!=96:raise ValueError("fixed96 byte cost differs")
    return result


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def source_view(image,caller_index):
    """Narrow static-caller repeat-source projection, not a CPU execution."""
    if type(image) is not bytes or len(image)!=ROM_SIZE:raise ValueError("complete edited bytes image required")
    caller=CALLERS[uint(caller_index,3,"diagnostic original caller role")]
    role,_,_,_,_,n,dest,_=caller;start,end,columns,_=SOURCES[role];rows=[];reads=[]
    for i in range(n):
        p=start+4*i;control=int.from_bytes(image[p:p+2],"big")
        if control!=0x8000|columns:raise ValueError("edited source outside admitted fixed repeat framing")
        payload=int.from_bytes(image[p+2:p+4],"big");reads.extend(range(p,p+4))
        rows.append(dict(index=i,start=p,end=p+4,control_WORD=control,payload_WORD=payload,
            emitted_WORD=payload|0xC000,emitted_cells=columns))
    return dict(caller_index=caller_index,source_role=role,destination_WORD=dest,rows=rows,
        next_source=start+4*n,physical_source_end=end,read_addresses=reads,source_only=True,
        editing_authority=False,CPU_execution=False,natural_execution=False,
        physical_source_end_is_CPU_clamp=False)


def schema(rom):
    def walk(value,field=None):
        if field=="payload_WORD":return dict(type="integer",minimum=0,maximum=65535)
        if type(value) is dict:
            props={k:walk(v,k) for k,v in value.items()}
            return dict(type="object",properties=props,required=list(props),additionalProperties=False)
        if type(value) is list:return dict(type="array",prefixItems=[walk(v) for v in value],items=False,minItems=len(value),maxItems=len(value))
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    result=walk(extract(rom));result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    return result


def render_bundle(rom):
    fields=extract(rom);serialized=dump(fields);image=rebuild(rom,load_fields(serialized));pieces=blocks(rom,fields)
    views=[source_view(rom,i) for i in range(4)];actual={p for row in views for p in row["read_addresses"]}
    expected={p for s,e,*_ in SOURCES for p in range(s,e)}
    if image!=rom or actual!=expected or len(actual)!=96:raise ValueError("exact serialized source/read union differs")
    report=dict(**metadata(),editable_bytes=96,physical_blocks=3,physical_rows=24,original_callers=4,
        source_read_union_BYTES=96,whole_ROM_exact=True,whole_ROM_sha256=sha(image),original_source_views=views,
        blocks=[{k:v for k,v in r.items() if k!="data"}|dict(bytes=len(r["data"]),sha256=sha(r["data"])) for r in pieces])
    members={"fields.json":serialized,"fields.schema.json":dump(schema(rom)),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=96,physical_blocks=3,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):raise ValueError("dedicated fresh output or exact formal bundle required")
    if path.exists() or not path.parent.is_dir():raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("command",choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM));parser.add_argument("--fields");parser.add_argument("--bundle");parser.add_argument("--output")
    args=parser.parse_args(argv);target=None
    if args.command=="export":
        if args.output is None or args.fields is not None or args.bundle is not None:raise ValueError("export needs fresh output only")
        target=fresh_output(args.output,bundle=True)
    elif args.command=="import":
        if args.output is None or args.bundle is not None:raise ValueError("import needs fields and fresh output")
        target=fresh_output(args.output)
        if target.suffix.lower()!=".bin":raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None):raise ValueError("verify is read-only")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=="export":
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=96,members={name:sha(data) for name,data in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS:raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data:raise ValueError("canonical bundle drift: "+name)
        result=dict(verified=True,editable_bytes=96,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:put(target,image)
        result=dict(bytes=len(image),editable_bytes=96,sha256=sha(image),exact_canonical=image==rom)
    print(json.dumps(result,sort_keys=True));return 0


if __name__=="__main__":raise SystemExit(main())
