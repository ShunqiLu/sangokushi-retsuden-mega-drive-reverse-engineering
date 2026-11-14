"""304 actual counted UI source bytes: twelve sources and thirteen callers.

Only the original direct/repeat/ascending grammar is admitted. Framing remains
fixed; true payload WORDs keep all bits. No other candidate reader is conflated.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared

ROOT=Path(__file__).resolve().parents[2]
ROM_SIZE=0x100000
ROM_SHA256=reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM=ROOT.parent/"work/original_g5510.bin"
OUTPUT_ROOT=ROOT/"build/counted_ui_row_sources"
FORMAL_ROOT=ROOT/"analysis/counted_ui_row_sources/generated"
DEFAULT_BUNDLE=FORMAL_ROOT
DEFAULT_FIELDS=FORMAL_ROOT/"fields.json"
FORMAT="g5510-batch-counted-UI-direct-repeat-ascending-WORD-sources-v1"
EDITABLE_BYTES=304
MAX_JSON=1024*1024
MEMBERS=frozenset(("fields.json","fields.schema.json","validation.json","manifest.json"))
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
MAP_PATH="analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
MAP_SHA256=reference_value(__name__, 'MAP_SHA256')
SECONDARY_SOURCE_PATH="src/m68k/secondary_dispatch_descendants.s"
SECONDARY_SOURCE_SHA256=reference_value(__name__, 'SECONDARY_SOURCE_SHA256')
# Start/end, original columns/rows. Physical allocation is not a CPU read clamp.
SOURCES=(
    (0x20AC,0x20B8,13,3),(0x21D6,0x21F2,8,7),(0x3772,0x378E,38,7),
    (0x5CB8,0x5CC8,11,4),(0xA4E6,0xA506,10,4),(0xA520,0xA530,10,4),
    (0xBF3A,0xBF5A,6,8),(0x10570,0x1058C,38,7),(0x15C62,0x15C7E,38,7),
    (0x1672C,0x16748,38,7),(0x309E0,0x309FC,38,7),(0x31938,0x31954,8,7),
)
SOURCE_HASHES=(
    reference_value(__name__, 'SOURCE_HASHES'),
    reference_value(__name__, 'SOURCE_HASHES_2'),
    reference_value(__name__, 'SOURCE_HASHES_3'),
    reference_value(__name__, 'SOURCE_HASHES_4'),
    reference_value(__name__, 'SOURCE_HASHES_5'),
    reference_value(__name__, 'SOURCE_HASHES_6'),
    reference_value(__name__, 'SOURCE_HASHES_7'),
    reference_value(__name__, 'SOURCE_HASHES_8'),
    reference_value(__name__, 'SOURCE_HASHES_9'),
    reference_value(__name__, 'SOURCE_HASHES_10'),
    reference_value(__name__, 'SOURCE_HASHES_11'),
    reference_value(__name__, 'SOURCE_HASHES_12'),
)
# Source role, setup block start/end, LEA, true JSR, literal destination or -1
# for the original live F36A.W-derived destination. 309E0 has two real callers.
CALLERS=(
    (0,0x2050,0x2074,0x206A,0x206E,-1),
    (1,0x21BC,0x21D6,0x21CA,0x21CE,0xC422),
    (2,0x374C,0x3772,0x375A,0x375E,0xCA02),
    (3,0x5C98,0x5CB8,0x5CA6,0x5CAA,0xC084),
    (4,0xA4CC,0xA4E6,0xA4DA,0xA4DE,0xC09C),
    (5,0xA506,0xA520,0xA514,0xA518,0xC09C),
    (6,0xBF1A,0xBF3A,0xBF28,0xBF2C,0xC3A0),
    (7,0x10544,0x10570,0x10552,0x10556,0xCA02),
    (8,0x15C3C,0x15C62,0x15C4A,0x15C4E,0xCA02),
    (9,0x1670C,0x1672C,0x1671A,0x1671E,0xCA02),
    (10,0x309C0,0x309E0,0x309CE,0x309D2,0xCA02),
    (10,0x30B6E,0x30B8E,0x30B7C,0x30B80,0xCA02),
    (11,0x3191E,0x31938,0x3191E,0x31930,0xC420),
)
CALLER_HASHES=(
    reference_value(__name__, 'CALLER_HASHES'),
    reference_value(__name__, 'CALLER_HASHES_2'),
    reference_value(__name__, 'CALLER_HASHES_3'),
    reference_value(__name__, 'CALLER_HASHES_4'),
    reference_value(__name__, 'CALLER_HASHES_5'),
    reference_value(__name__, 'CALLER_HASHES_6'),
    reference_value(__name__, 'CALLER_HASHES_7'),
    reference_value(__name__, 'CALLER_HASHES_8'),
    reference_value(__name__, 'CALLER_HASHES_9'),
    reference_value(__name__, 'CALLER_HASHES_10'),
    reference_value(__name__, 'CALLER_HASHES_11'),
    reference_value(__name__, 'CALLER_HASHES_12'),
    reference_value(__name__, 'CALLER_HASHES_13'),
)
READER=(0x26BFA,0x26C8E,reference_value(__name__, 'READER'))
sha,dump=shared.sha,shared.dump
keys,same,uint,exact_list=shared.keys,shared.same,shared.uint,shared.exact_list
load_fields=shared.load_fields
safe_path,read_bounded,put=shared.safe_path,shared.read_bounded,shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE or sha(rom)!=ROM_SHA256:
        raise ValueError("canonical full ROM bytes, size and SHA-256 required")
    bodies=[(s,e,h) for (_,s,e,*_),h in zip(CALLERS,CALLER_HASHES)]+[READER]
    for start,end,digest in bodies:
        if sha(rom[start:end])!=digest: raise ValueError("pinned original setup/call/reader differs")
    for (start,end,*_),digest in zip(SOURCES,SOURCE_HASHES):
        if sha(rom[start:end])!=digest: raise ValueError("pinned literal source differs")


def metadata():
    callers=[]
    for (role,start,end,LEA,call,destination),digest in zip(CALLERS,CALLER_HASHES):
        columns,lines=SOURCES[role][2:]
        callers.append(dict(source_role=role,setup_start=start,setup_end=end,sha256=digest,
            LEA_PC=LEA,LEA_PC_base=LEA+2,JSR_PC=call,reader=0x26BFA,
            original_D0_LONG=0xC0000000|columns,original_D1_WORD=lines,
            original_D2_WORD=destination,destination_is_live_F36A_derived=destination==-1))
    return dict(format=FORMAT,confidence="candidate",source_format_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        physical_scope=[dict(start=s,end=e,bytes=e-s,sha256=h) for (s,e,*_),h in zip(SOURCES,SOURCE_HASHES)],
        evidence=dict(original_callers=callers,reader=dict(start=READER[0],end=READER[1],sha256=READER[2]),
            original_ledger=dict(path=MAP_PATH,sha256=MAP_SHA256,reachability_confidence="heuristic"),
            conditional_secondary_source=dict(path=SECONDARY_SOURCE_PATH,sha256=SECONDARY_SOURCE_SHA256,
                LEA_PC=0x10552,JSR_PC=0x10556,reachability_confidence="candidate"),
            accepted_raw_snapshot=dict(layout=LAYOUT_ID,resources=67,raw_BYTES=46619,
                source_raw_difference_BYTES=304,source_typed_overlap_BYTES=0),
            grammar=dict(source_WORD_read=0x26C10,source_sign_branch=0x26C12,
                direct_cells=1,direct_WORD_original_sign=0,original_attribute_OR_WORD=0xC000,
                negative_selector="((control_WORD&7FFF)>>7)&FFFE",
                directory=0x26C4C,directory_WORD_read=0x26C2E,dispatch_call=0x26C32,
                used_selectors=[0,2],used_handler_targets=[0x26C58,0x26C72],
                repeat_payload_WORD_read=0x26C5E,ascending_payload_WORD_read=0x26C78,
                ascending_increment_WORD=2,run_count_source="nonzero original control low BYTE",
                repeat_remaining_subtract=0x26C6C,ascending_remaining_subtract=0x26C88,
                row_remaining_test=0x26C36,row_DBRA=0x26C3A,
                stop="original exact columns per row and original D1 rows, not a terminator"),
            live_destination=dict(RAM_WORD=0xFFF36A,read_PC=0x205A,
                formula="WORD(C234 + WORD(WORD(3*F36A.W)<<7))",source_read_count_independent=True),
            shared_source=dict(source=0x309E0,real_callers=[0x309D2,0x30B80],physical_emit_count=1)),
        exclusions=dict(other_reader_candidates_not_retyped=True,
            font_sprite_menu_BYTE_LONG_sources_not_this_grammar=True,
            unused_numeric_RAM_pointer_handlers_not_admitted_here=True,
            zero_payloads_are_consumed_WORDs_not_padding=True,source_tail_growth_not_allowed=True),
        source_business_names="unknown",independent_CPU_comparison=False,
        claims=dict(full_payload_WORD_bits_preserved=True,source_direct_sign_fixed=True,
            physical_source_boundary_is_CPU_clamp=False,full_RAM_VDP_queue_bus_CPU_execution=False,
            natural_domain_complete=False,recovered_functions_added=0,high_level_semantic_compiler_coverage_added=0))


def source_fixed(index):
    start,end,columns,lines=SOURCES[index]
    return dict(id=f"rom_{start:06X}_counted_UI_rows",source_role=index,start=start,end=end,
        columns=columns,lines=lines,WORD_order="big",source_stop="row counter and width")


def pinned(value,expected,mutable,label):
    keys(value,{*expected,*mutable},label)
    for key,original in expected.items(): same(value[key],original,label+"."+key)


def decode_stream(image,source_role):
    """Bounded source grammar projection, never general CPU/VDP execution."""
    if type(image) is not bytes or len(image)!=ROM_SIZE: raise ValueError("complete edited bytes image required")
    role=uint(source_role,11,"physical source role")
    start,end,columns,lines=SOURCES[role]
    cursor,rows=start,[]
    def take():
        nonlocal cursor
        if cursor+2>end: raise ValueError("source WORD crossed admitted physical boundary")
        value=int.from_bytes(image[cursor:cursor+2],"big"); cursor+=2
        return value
    for row_index in range(lines):
        row_start,cells,operations=cursor,0,[]
        while cells<columns:
            op_start,WORD=cursor,take()
            if WORD<0x8000:
                op=dict(kind="direct_WORD",start=op_start,end=cursor,emitted_cells=1,WORD=WORD)
            else:
                selector,count=((WORD&0x7FFF)>>7)&0xFFFE,WORD&255
                if selector not in (0,2) or not count:
                    raise ValueError("handler/count outside this admitted repeat/ascending source grammar")
                payload=take()
                op=dict(kind="repeat_WORD" if selector==0 else "ascending_WORD",start=op_start,end=cursor,
                    emitted_cells=count,control_WORD=WORD,dispatch_BYTE_offset=selector,
                    handler=0x26C58 if selector==0 else 0x26C72,payload_WORD=payload)
            cells+=op["emitted_cells"]
            if cells>columns: raise ValueError("source operation overruns original row width")
            operations.append(op)
        rows.append(dict(row_index=row_index,start=row_start,end=cursor,emitted_cells=columns,operations=operations))
    if cursor!=end: raise ValueError("original row count did not stop exactly at admitted end")
    return dict(**source_fixed(role),rows=rows)


def source_preview(image,source_role):
    source=decode_stream(image,source_role); rows=[]
    for row in source["rows"]:
        values=[]
        for op in row["operations"]:
            if op["kind"]=="direct_WORD": values.append(op["WORD"]|0xC000)
            else:
                WORD=op["payload_WORD"]|0xC000
                for _ in range(op["emitted_cells"]):
                    values.append(WORD)
                    if op["kind"]=="ascending_WORD": WORD=(WORD+2)&0xFFFF
        rows.append(values)
    return dict(source_role=source_role,rows=rows,source_only=True,editing_authority=False,CPU_execution=False)


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),row_sources=[decode_stream(rom,i) for i in range(12)])


def blocks(rom,fields):
    verify_rom(rom); pinned(fields,metadata(),{"row_sources"},"counted UI source package")
    result=[]
    for i,source in enumerate(exact_list(fields["row_sources"],12,"physical source groups")):
        pinned(source,source_fixed(i),{"rows"},"counted source")
        original=decode_stream(rom,i); raw=bytearray()
        for row,expected in zip(exact_list(source["rows"],SOURCES[i][3],"original rows"),original["rows"]):
            pinned(row,{k:v for k,v in expected.items() if k!="operations"},{"operations"},"source row")
            for op,before in zip(exact_list(row["operations"],len(expected["operations"]),"original operations"),expected["operations"]):
                mutable={"WORD"} if before["kind"]=="direct_WORD" else {"payload_WORD"}
                pinned(op,{k:v for k,v in before.items() if k not in mutable},mutable,"source operation")
                if before["kind"]=="direct_WORD":
                    raw.extend(uint(op["WORD"],0x7FFF,"direct WORD preserving sign branch").to_bytes(2,"big"))
                else:
                    raw.extend(op["control_WORD"].to_bytes(2,"big"))
                    raw.extend(uint(op["payload_WORD"],0xFFFF,"complete source payload WORD").to_bytes(2,"big"))
        if len(raw)!=source["end"]-source["start"]: raise ValueError("original source byte cost differs")
        result.append(dict(id=source["id"],start=source["start"],end=source["end"],data=bytes(raw),
            role="confirmed_counted_UI_full_WORD_source"))
    if sum(len(r["data"]) for r in result)!=304: raise ValueError("fixed304 source byte cost differs")
    return result


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields): image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def schema(rom):
    def obj(properties):
        return dict(type="object",properties=properties,required=list(properties),additionalProperties=False)
    def exact(items):
        return dict(type="array",prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def fixed(value):
        if type(value) is dict: return obj({k:fixed(v) for k,v in value.items()})
        if type(value) is list: return exact([fixed(v) for v in value])
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    fields=extract(rom); props={k:fixed(v) for k,v in metadata().items()}; sources=[]
    for source in fields["row_sources"]:
        rows=[]
        for row in source["rows"]:
            ops=[]
            for op in row["operations"]:
                name="WORD" if op["kind"]=="direct_WORD" else "payload_WORD"
                ops.append(obj({k:dict(type="integer",minimum=0,maximum=32767 if name=="WORD" else 65535)
                    if k==name else fixed(v) for k,v in op.items()}))
            rows.append(obj({**{k:fixed(v) for k,v in row.items() if k!="operations"},"operations":exact(ops)}))
        sources.append(obj({**{k:fixed(v) for k,v in source.items() if k!="rows"},"rows":exact(rows)}))
    props["row_sources"]=exact(sources)
    result=obj(props); result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="Twelve actual counted sources. Original topology/control counts fixed, payload WORDs all bits, direct sign preserved."
    return result


def render_bundle(rom):
    fields=extract(rom); serialized=dump(fields); image=rebuild(rom,load_fields(serialized)); encoded=blocks(rom,fields)
    reads={p for source in fields["row_sources"] for row in source["rows"] for op in row["operations"] for p in range(op["start"],op["end"])}
    authored={p for row in encoded for p in range(row["start"],row["end"])}
    if image!=rom or reads!=authored or len(reads)!=304: raise ValueError("whole-ROM roundtrip or exact source-read union differs")
    ops=[op for source in fields["row_sources"] for row in source["rows"] for op in row["operations"]]
    report=dict(**metadata(),editable_bytes=304,physical_blocks=12,original_callers=13,
        counted_rows=sum(s[3] for s in SOURCES),operations=len(ops),source_read_union_BYTES=304,
        operation_counts={name:sum(op["kind"]==name for op in ops) for name in ("direct_WORD","repeat_WORD","ascending_WORD")},
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        original_source_previews=[source_preview(image,i) for i in range(12)],
        blocks=[{k:v for k,v in row.items() if k!="data"}|dict(bytes=len(row["data"]),sha256=sha(row["data"])) for row in encoded])
    members={"fields.json":serialized,"fields.schema.json":dump(schema(rom)),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=304,physical_blocks=12,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError("dedicated fresh output or exact formal bundle required")
    if path.exists() or not path.parent.is_dir(): raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM)); parser.add_argument("--fields")
    parser.add_argument("--bundle"); parser.add_argument("--output")
    args=parser.parse_args(argv); target=None
    if args.command=="export":
        if args.output is None or args.fields is not None or args.bundle is not None: raise ValueError("export needs fresh output only")
        target=fresh_output(args.output,bundle=True)
    elif args.command=="import":
        if args.output is None or args.bundle is not None: raise ValueError("import needs fields and fresh output")
        target=fresh_output(args.output)
        if target.suffix.lower()!=".bin": raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None): raise ValueError("verify is read-only")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=="export":
        members=render_bundle(rom); target.mkdir()
        for name,data in members.items(): put(target/name,data)
        result=dict(path=str(target),editable_bytes=304,members={name:sha(data) for name,data in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS: raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data: raise ValueError("canonical bundle drift: "+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=304,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None: put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=304,exact_canonical=image==rom,
            bytes=len(image),sha256=sha(image))
    print(json.dumps(result,sort_keys=True)); return 0


if __name__=="__main__": raise SystemExit(main())
