"""190 literal WORD sources for five existing state-dependent relative JSRs.

The source WORDs are confirmed reads. Catalog counts are not CPU clamps, and
targets remain live diagnostics, including one original target with unknown code.
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
OUTPUT_ROOT=ROOT/"build/state_dispatch_word_fields"
FORMAL_ROOT=ROOT/"analysis/state_dispatch_word_fields/generated"
DEFAULT_BUNDLE=FORMAL_ROOT
DEFAULT_FIELDS=FORMAL_ROOT/"fields.json"
FORMAT="g5510-state-relative-JSR-literal-WORD-sources-v1"
EDITABLE_BYTES=190
MAX_JSON=1024*1024
MEMBERS=frozenset(("fields.json","fields.schema.json","validation.json","manifest.json"))
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
MAP_PATH="analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
MAP_SHA256=reference_value(__name__, 'MAP_SHA256')
# Source start/end, target base, selector RAM WORD, BYTE mask, exact6 bypass,
# source-read PC, true JSR PC, source index/read-entry start.
TABLES=(
    (0xF78,0xF98,0xF98,0xFFF612,True,False,0xF3A,0xF44,0xF30),
    (0x17D2,0x17FA,0x17FA,0xFFF362,False,False,0x17A8,0x17AC,0x17A2),
    (0xE0C4,0xE0EE,0xFE06,0xFFF65A,False,True,0xE05E,0xE068,0xE050),
    (0x13D58,0x13D7A,0x13D7A,0xFFF362,False,False,0x13D4E,0x13D52,0x13D48),
    (0x18D0A,0x18D34,0x18D34,0xFFF612,True,False,0x18CDC,0x18CE0,0x18CD2),
)
SOURCE_HASHES=(
    reference_value(__name__, 'SOURCE_HASHES'),
    reference_value(__name__, 'SOURCE_HASHES_2'),
    reference_value(__name__, 'SOURCE_HASHES_3'),
    reference_value(__name__, 'SOURCE_HASHES_4'),
    reference_value(__name__, 'SOURCE_HASHES_5'),
)
BODIES=(
    (0xF10,0xF78,reference_value(__name__, 'BODIES')),
    (0x1798,0x17D2,reference_value(__name__, 'BODIES_2')),
    (0xE050,0xE0C4,reference_value(__name__, 'BODIES_3')),
    (0x13D48,0x13D58,reference_value(__name__, 'BODIES_4')),
    (0x18CB4,0x18D0A,reference_value(__name__, 'BODIES_5')),
)
sha,dump=shared.sha,shared.dump
keys,same,uint,exact_list=shared.keys,shared.same,shared.uint,shared.exact_list
load_fields=shared.load_fields
safe_path,read_bounded,put=shared.safe_path,shared.read_bounded,shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE or sha(rom)!=ROM_SHA256:
        raise ValueError("canonical full ROM bytes, size and SHA-256 required")
    for start,end,digest in BODIES:
        if sha(rom[start:end])!=digest: raise ValueError("pinned original reader/call body differs")
    for (start,end,*_),digest in zip(TABLES,SOURCE_HASHES):
        if sha(rom[start:end])!=digest: raise ValueError("pinned literal WORD source differs")


def metadata():
    return dict(format=FORMAT,confidence="candidate",source_format_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        physical_scope=[dict(start=s,end=e,bytes=e-s,sha256=h) for (s,e,*_),h in zip(TABLES,SOURCE_HASHES)],
        evidence=dict(consumers=[dict(start=s,end=e,sha256=h) for s,e,h in BODIES],
            original_ledger=dict(path=MAP_PATH,sha256=MAP_SHA256,reachability_confidence="heuristic"),
            accepted_raw_snapshot=dict(layout=LAYOUT_ID,resources=61,raw_BYTES=47829,
                source_raw_difference_BYTES=190,source_typed_overlap_BYTES=0),
            source_encoding="literal BE16 signed relative JSR offset; full WORD retained",
            index_encoding="optional original ANDI.W00FF; LSL.W1 modulo16 then signed WORD address addition",
            target_encoding="target_base + signed source WORD, modulo32",
            F78_read=dict(load_PC=0xF30,mask_PC=0xF34,shift_PC=0xF38,
                read_PC=0xF3A,PC_base=0xF3C,displacement_BYTE=0x3C,
                target_LEA_PC=0xF3E,PC_base_for_LEA=0xF40,LEA_displacement_WORD=0x58,JSR_PC=0xF44),
            state17_read=dict(load_PC=0x17A2,shift_PC=0x17A6,read_PC=0x17A8,
                PC_base=0x17AA,displacement_BYTE=0x28,JSR_PC=0x17AC,
                JSR_PC_base=0x17AE,JSR_displacement_BYTE=0x4C),
            E0C4_read=dict(load_PC=0xE050,exact6_compare=0xE054,equality_branch=0xE058,
                equality_tail_JMP=0xE0BC,equality_target=0x30AC6,
                shift_PC=0xE05C,read_PC=0xE05E,PC_base=0xE060,displacement_BYTE=0x64,
                target_LEA_PC=0xE062,PC_base_for_LEA=0xE064,LEA_displacement_WORD=0x1DA2,
                JSR_PC=0xE068,slot6_constructed_read_selector_WORD=0x8006,
                slot6_original_target=0x103E8,slot6_original_target_code_confidence="unknown",
                slot6_target_code_admitted=False),
            state13_read=dict(caller_JSR=0x36DC,entry=0x13D48,shift_PC=0x13D4C,
                read_PC=0x13D4E,PC_base=0x13D50,displacement_BYTE=8,
                JSR_PC=0x13D52,JSR_PC_base=0x13D54,JSR_displacement_BYTE=0x26),
            state18_read=dict(load_PC=0x18CD2,mask_PC=0x18CD6,shift_PC=0x18CDA,
                read_PC=0x18CDC,PC_base=0x18CDE,displacement_BYTE=0x2C,
                JSR_PC=0x18CE0,JSR_PC_base=0x18CE2,JSR_displacement_BYTE=0x52)),
        source_business_meaning="unknown",independent_CPU_comparison=False,
        claims=dict(catalog_counts_are_CPU_clamps=False,original_targets_are_edit_constraints=False,
            complete_indirect_target_domain=False,any_target_code_admitted=False,
            full_preceding_callee_RAM_stack_VDP_bus_execution=False,natural_domain_complete=False,
            recovered_functions_added=0,high_level_semantic_compiler_coverage_added=0))


def table_fixed(index):
    start,end,base,ram,mask,bypass,read,call,entry=TABLES[index]
    return dict(id=f"rom_{start:06X}_relative_JSR_WORD_source",table_index=index,start=start,end=end,
        role="signed_relative_JSR_source_WORD",WORD_order="big",WORD_count=(end-start)//2,
        original_target_base=base,selector_RAM_WORD=ram,original_BYTE_mask=mask,
        original_exact6_bypass=bypass,source_read_PC=read,JSR_PC=call,local_read_entry=entry)


def offset_fixed(table,index):
    start=TABLES[table][0]+2*index
    return dict(id=f"rom_{start:06X}_relative_offset_WORD",slot=index,address=start,
        constructed_selector_WORD=0x8006 if table==2 and index==6 else index,
        natural_selector_confidence="unknown")


def pinned(value,expected,mutable,label):
    keys(value,{*expected,*mutable},label)
    for key,original in expected.items(): same(value[key],original,label+"."+key)


def s16(value):
    return value-65536 if value&32768 else value


def source_view(image,table_index,selector_WORD):
    """Original local read/JSR-address projection, not target/callee execution."""
    if type(image) is not bytes or len(image)!=ROM_SIZE: raise ValueError("complete edited bytes image required")
    table=uint(table_index,4,"physical source role")
    selector=uint(selector_WORD,65535,"already fetched full selector WORD")
    start,end,base,_,mask,bypass,_,_,_=TABLES[table]
    result=dict(table_index=table,selector_WORD=selector,source_only=True,CPU_execution=False,target_code_admitted=False)
    if bypass and selector==6:
        return dict(**result,status="original_exact6_tail_JMP_no_source_read",tail_JMP_target=0x30AC6)
    value=selector&255 if mask else selector
    index=(value<<1)&65535
    address=(start+s16(index))&0xFFFFFFFF
    result.update(index_WORD=index,read_address=address,inside_authored_source=start<=address<end)
    if not 0<=address<=ROM_SIZE-2: return dict(**result,status="outside_ROM_read_boundary")
    WORD=int.from_bytes(image[address:address+2],"big")
    target=(base+s16(WORD))&0xFFFFFFFF
    return dict(**result,status="offset_WORD_read",offset_WORD=WORD,signed_offset=s16(WORD),
        target=target,target_WORD_aligned=not bool(target&1),target_inside_ROM=target<ROM_SIZE,
        target_execution_simulated=False)


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),tables=[dict(**table_fixed(t),offsets=[dict(**offset_fixed(t,i),
        offset_WORD=int.from_bytes(rom[start+2*i:start+2*i+2],"big")) for i in range((end-start)//2)])
        for t,(start,end,*_) in enumerate(TABLES)])


def blocks(rom,fields):
    verify_rom(rom)
    pinned(fields,metadata(),{"tables"},"relative JSR source package")
    result=[]
    for t,table in enumerate(exact_list(fields["tables"],5,"physical source groups")):
        fixed=table_fixed(t); pinned(table,fixed,{"offsets"},"source group")
        raw=bytearray()
        for i,offset in enumerate(exact_list(table["offsets"],fixed["WORD_count"],"physical source WORDs")):
            pinned(offset,offset_fixed(t,i),{"offset_WORD"},"literal source offset")
            raw.extend(uint(offset["offset_WORD"],65535,"complete offset WORD bits").to_bytes(2,"big"))
        result.append(dict(id=table["id"],start=table["start"],end=table["end"],data=bytes(raw),
            role="confirmed_relative_JSR_full_WORD_source"))
    if sum(len(r["data"]) for r in result)!=190: raise ValueError("fixed190 source byte cost differs")
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
    fields=extract(rom); props={k:fixed(v) for k,v in metadata().items()}
    props["tables"]=exact([obj({**{k:fixed(v) for k,v in table.items() if k!="offsets"},
        "offsets":exact([obj({k:dict(type="integer",minimum=0,maximum=65535) if k=="offset_WORD"
            else fixed(v) for k,v in offset.items()}) for offset in table["offsets"]])}) for table in fields["tables"]])
    result=obj(props); result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="95 full literal WORD offsets; fixed physical source topology, no target/domain restrictions."
    return result


def render_bundle(rom):
    fields=extract(rom); serialized=dump(fields); image=rebuild(rom,load_fields(serialized))
    encoded=blocks(rom,fields)
    views=[source_view(image,t,row["constructed_selector_WORD"]) for t,table in enumerate(fields["tables"]) for row in table["offsets"]]
    reads={p for row in views for p in (row["read_address"],row["read_address"]+1)}
    authored={p for row in encoded for p in range(row["start"],row["end"])}
    if image!=rom or reads!=authored or len(reads)!=190: raise ValueError("whole-ROM roundtrip or exact190 read union differs")
    report=dict(**metadata(),editable_bytes=190,physical_blocks=5,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),constructed_source_read_union_BYTES=190,
        all95_WORD_read_witnesses=views,original_targets_diagnostic_only=True,
        unknown_original_target=dict(table_index=2,slot=6,target=0x103E8,code_admitted=False),
        original_guard_and_alias_examples=[source_view(image,t,v) for t,v in
            ((2,6),(2,0x8006),(1,20),(1,0x4000),(3,17),(4,21),(0,16),(0,0xFFFF))],
        blocks=[{k:v for k,v in row.items() if k!="data"}|dict(bytes=len(row["data"]),sha256=sha(row["data"])) for row in encoded])
    members={"fields.json":serialized,"fields.schema.json":dump(schema(rom)),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=190,physical_blocks=5,
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
        result=dict(path=str(target),editable_bytes=190,members={name:sha(data) for name,data in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS: raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data: raise ValueError("canonical bundle drift: "+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=190,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None: put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=190,exact_canonical=image==rom,
            bytes=len(image),sha256=sha(image))
    print(json.dumps(result,sort_keys=True)); return 0


if __name__=="__main__": raise SystemExit(main())
