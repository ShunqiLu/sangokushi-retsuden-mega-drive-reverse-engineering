"""232 actually-read source bytes for original 0677F0 selector WORD lookups.

Ten physical catalogs are not CPU scan boundaries. Complete key/value WORDs
are editable; a key sign-bit edit intentionally changes live default behavior.
No counted UI stream, renderer, natural selector domain or full CPU is claimed.
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
OUTPUT_ROOT=ROOT/"build/ui_selector_pair_fields"
FORMAL_ROOT=ROOT/"analysis/ui_selector_pair_fields/generated"
DEFAULT_BUNDLE=FORMAL_ROOT
DEFAULT_FIELDS=FORMAL_ROOT/"fields.json"
EDITABLE_BYTES=232
MAX_JSON=1024*1024
MAX_DIAGNOSTIC_SCAN_PAIRS=ROM_SIZE//4
FORMAT="g5510-UI-selector-key-value-WORD-fields-v1"
MEMBERS=frozenset(("fields.json","fields.schema.json","validation.json","manifest.json"))
# Source begin/end, original LEA, true BSR, full caller body SHA-256, dispatch witness.
TABLES=(
    (0x677D4,0x677F0,0x677B2,0x677B6,reference_value(__name__, 'TABLES'),0x60),
    (0x6780C,0x67818,0x67804,0x67808,reference_value(__name__, 'TABLES_2'),0x61),
    (0x67820,0x67858,0x67818,0x6781C,reference_value(__name__, 'TABLES_3'),0x62),
    (0x67862,0x6787E,0x67858,0x6785C,reference_value(__name__, 'TABLES_4'),0x63),
    (0x6788A,0x678A2,0x6787E,0x67882,reference_value(__name__, 'TABLES_5'),0x64),
    (0x678D4,0x678DC,0x678CA,0x678CE,reference_value(__name__, 'TABLES_6'),0x6A),
    (0x678EC,0x67900,0x678DC,0x678E0,reference_value(__name__, 'TABLES_7'),0x6C),
    (0x67916,0x6791E,0x6790C,0x67910,reference_value(__name__, 'TABLES_8'),0x6F),
    (0x67946,0x6794E,0x6793A,0x6793E,reference_value(__name__, 'TABLES_9'),0x75),
    (0x67990,0x679B8,0x67980,0x67984,reference_value(__name__, 'TABLES_10'),0x80),
)
SPANS=tuple((s,e) for s,e,*_ in TABLES)
ORIGINAL_KEYS=(
    (0x13,0x21,0x14,0x17,0x57,0x40,0x8000),
    (0x2F,0x93,0x8000),
    (0x85,0x1E,0x47,0x4E,0x51,0x58,0x5D,0x5F,0x62,0x64,0x68,0x71,0x76,0x8000),
    (0x26,0x32,0x5E,0x63,0x67,0x4A,0x4D),
    (0x6,0x46,0x15,0x5C,0x61,0x66),
    (0x1F,0x75),(0x27,0x6D,0xB1,0xBA,0x8000),
    (0x36,0x49),(0xE,0x1A),(0x6B,0x6E,0x77,0x73,0x79,0x7B,0x7F,0x81,0x83,0xA7),
)
SOURCE_SHA256=reference_value(__name__, 'SOURCE_SHA256')
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_BANK_SHA256=reference_value(__name__, 'LAYOUT_BANK_SHA256')
ENHANCED_PATH="analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256=reference_value(__name__, 'ENHANCED_SHA256')
DISPATCH_SOURCE=(0x6774C,0x677B2,reference_value(__name__, 'DISPATCH_SOURCE'))
CONSUMERS=(
    (0x676C4,0x67728,reference_value(__name__, 'CONSUMERS')),
    (0x677F0,0x67804,reference_value(__name__, 'CONSUMERS_2')),
    (0x678A2,0x678CA,reference_value(__name__, 'CONSUMERS_3')),
    (0x67900,0x6790C,reference_value(__name__, 'CONSUMERS_4')),
    (0x6791E,0x6793A,reference_value(__name__, 'CONSUMERS_5')),
    (0x6794E,0x67980,reference_value(__name__, 'CONSUMERS_6')),
    (0x679B8,0x679E0,reference_value(__name__, 'CONSUMERS_7')),
)+tuple((lea,start,h) for start,_,lea,_,h,_ in TABLES)
sha,dump=shared.sha,shared.dump
keys,same,uint,exact_list=shared.keys,shared.same,shared.uint,shared.exact_list
load_fields=shared.load_fields
safe_path,read_bounded,put=shared.safe_path,shared.read_bounded,shared.put


def image_bytes(image):
    if type(image) is not bytes or len(image)!=ROM_SIZE:
        raise ValueError("complete bytes image required")


def verify_rom(rom):
    image_bytes(rom)
    if sha(rom)!=ROM_SHA256: raise ValueError("canonical source SHA-256 required")
    for start,end,expected in CONSUMERS+(DISPATCH_SOURCE,):
        if sha(rom[start:end])!=expected: raise ValueError("original caller/reader/alias source differs")
    if sha(b"".join(rom[s:e] for s,e in SPANS))!=SOURCE_SHA256:
        raise ValueError("original key/value source union differs")


def table_fixed(index):
    start,end,lea,call,_,state=TABLES[index]
    return dict(id=f"rom_{start:06X}_selector_WORD_pairs",index=index,start=start,end=end,
        physical_pairs=(end-start)//4,WORD_order="big",source_LEA=lea,LEA_PC_base=lea+2,
        true_BSR=call,reader=0x677F0,original_state_WORD_witness=state,
        original_negative_default_present=any(k&0x8000 for k in ORIGINAL_KEYS[index]))


def pair_fixed(table,index):
    start=TABLES[table][0]+4*index
    original_key=ORIGINAL_KEYS[table][index]
    return dict(index=index,key_address=start,value_address=start+2,
        original_key_WORD=original_key,original_negative_default=bool(original_key&0x8000),
        original_read_witness_selector_WORD=0xFFFF if original_key&0x8000 else original_key)


def metadata():
    return dict(format=FORMAT,confidence="candidate",source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        physical_scope=[dict(start=s,end=e,bytes=e-s) for s,e in SPANS],
        source_union_sha256=SOURCE_SHA256,
        evidence=dict(source="canonical true LEA/BSR callers, exact key/default reader, constructed WORD read witnesses",
            enhanced_ledger=dict(path=ENHANCED_PATH,sha256=ENHANCED_SHA256,
                outer_dispatch_and_reader_confidence="runtime_confirmed",
                most_source_callers_confidence="heuristic",source_678EC_caller_confidence="runtime_confirmed"),
            frozen_raw_layout=dict(id=LAYOUT_ID,bank06_sha256=LAYOUT_BANK_SHA256,
                emitted_raw_bytes=EDITABLE_BYTES,older_typed_overlap_bytes=0),
            original_instruction_and_alias_spans=[dict(start=s,end=e,sha256=h) for s,e,h in CONSUMERS],
            reader=dict(entry=0x677F0,selector_READ=0x677F0,selector_RAM=0xFFFFF38C,
                selector_width="complete WORD, not BYTE",key_postincrement_WORD_READ=0x677F4,
                BMI_before_equality=0x677F6,CMP_WORD=0x677F8,BEQ=0x677FA,
                unmatched_skip_value_WORD=0x677FC,next_key_branch=0x677FE,
                value_WORD_READ=0x67800,RTS=0x67802,
                stop="first key with bit15 set, otherwise first complete key WORD equal to selector",
                value_is_read_only_after_stop=True,negative_key_low15_bits_not_compared=True,
                no_counted_UI_renderer_or_26BFA_call=True,physical_catalog_ends_are_not_CPU_stops=True),
            dispatch=dict(entry=0x676C4,input_RAM=0xFFFFF380,full_WORD=True,
                unsigned_threshold_0060=0x676C8,BCC_secondary_path=0x676CC,
                subtract_WORD_0060=0x676DE,LSL_WORD_1=0x676E2,
                signed_PC_indexed_offset_WORD_READ=0x676E4,offset_base=0x6774C,
                LEA_base=0x676E8,target_base=0x677B2,signed_JSR_WORD=0x676EE,
                formula="index_WORD=((state_WORD-0060)<<1)&FFFF; offset read at 6774C+s16(index_WORD); JSR 677B2+s16(offset_WORD)",
                original_local_call_witnesses=[dict(state_WORD=t[5],offset_address=0x6774C+2*(t[5]-0x60),
                    original_offset_WORD=t[2]-0x677B2,target=t[2]) for t in TABLES],
                already_typed_offset_source=dict(start=DISPATCH_SOURCE[0],end=DISPATCH_SOURCE[1],
                    sha256=DISPATCH_SOURCE[2],physical_emit=False),
                physical_offset_count_is_not_CPU_clamp=True,natural_dispatch_domain="unknown"),
            read_witnesses=[dict(table_index=t,pair_index=i,**pair_fixed(t,i))
                for t,group in enumerate(ORIGINAL_KEYS) for i in range(len(group))],
            original_negative_defaults=dict(table_indices=[0,1,2,6],key_WORD=0x8000,
                other_six_catalogs_have_no_negative_key=True),
            edited_keys=dict(complete_WORD_min=0,complete_WORD_max=65535,
                sign_bit_edit_changes_default_behavior=True,duplicate_keys_keep_first_match=True,
                original_default_WORD_not_silently_restored=True),
            diagnostics=dict(edited_whole_image=True,scan_budget_is_not_original_CPU_stop=True,
                original_code_neighbor_alias_reads_are_not_emitted=True,
                source_values_are_not_called_pointers_or_renderer_cells=True)),
        original_business_names="unknown",natural_selector_and_all_writer_domains="unknown",
        edited_gameplay_safety="unknown",independent_CPU_comparison=False,
        full_RAM_CCR_stack_bus_and_UI_algorithm="not modeled")


def pinned(row,fixed,mutable,label):
    keys(row,set(fixed)|set(mutable),label)
    for key,value in fixed.items(): same(row[key],value,label+"."+key)


def extract(rom):
    verify_rom(rom)
    result=metadata()
    result["tables"]=[dict(**table_fixed(t),pairs=[dict(**pair_fixed(t,i),
        key_WORD=int.from_bytes(rom[p:p+2],"big"),value_WORD=int.from_bytes(rom[p+2:p+4],"big"))
        for i,p in enumerate(range(spec[0],spec[1],4))]) for t,spec in enumerate(TABLES)]
    return result


def blocks(rom,fields):
    verify_rom(rom)
    pinned(fields,metadata(),{"tables"},"selector pair package")
    result=[]
    for t,table in enumerate(exact_list(fields["tables"],10,"ten physical tables")):
        fixed=table_fixed(t)
        pinned(table,fixed,{"pairs"},"physical table")
        raw=bytearray()
        for i,pair in enumerate(exact_list(table["pairs"],fixed["physical_pairs"],"fixed physical pair cost")):
            pinned(pair,pair_fixed(t,i),{"key_WORD","value_WORD"},"complete source pair")
            raw.extend(uint(pair["key_WORD"],65535,"complete literal key WORD").to_bytes(2,"big"))
            raw.extend(uint(pair["value_WORD"],65535,"complete literal value WORD").to_bytes(2,"big"))
        if len(raw)!=fixed["end"]-fixed["start"]: raise ValueError("fixed physical byte cost differs")
        result.append(dict(id=fixed["id"],start=fixed["start"],end=fixed["end"],data=bytes(raw),
            role="confirmed_literal_selector_key_value_WORD_pairs"))
    if sum(len(r["data"]) for r in result)!=EDITABLE_BYTES or any(a["end"]>b["start"] for a,b in zip(result,result[1:])):
        raise ValueError("disjoint exact 232-byte source cost differs")
    return result


def rebuild(rom,fields):
    rows=blocks(rom,fields);image=bytearray(rom)
    for row in rows: image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def lookup(image,table_index,selector_WORD,scan_budget=256):
    """Narrow live source scan, including keys/values outside the owned catalog.

    The diagnostic budget reports unfinished scanning; it never substitutes a
    result, CPU stop, catalog clamp or natural selector bound. Skipped value
    WORDs are not reported as CPU reads. Key sign is tested before equality.
    """
    image_bytes(image)
    t=uint(table_index,9,"physical table role selector")
    selector=uint(selector_WORD,65535,"complete fetched selector WORD")
    budget=uint(scan_budget,MAX_DIAGNOSTIC_SCAN_PAIRS,"diagnostic scan budget")
    if not budget: raise ValueError("positive diagnostic budget required")
    start,end=SPANS[t];p=start;trace=[];reads=[]
    result=dict(table_index=t,selector_WORD=selector,scan_budget=budget,
        diagnostic_budget_is_CPU_stop=False,source_only=True,natural_execution=False,CPU_execution=False)
    for _ in range(budget):
        if not 0<=p<=ROM_SIZE-2:
            return dict(**result,status="outside_ROM_key_read_boundary",next_key_address=p,trace=trace,read_addresses=reads)
        key=int.from_bytes(image[p:p+2],"big")
        reads.extend((p,p+1))
        trace.append(dict(key_address=p,key_WORD=key,key_inside_physical_catalog=start<=p<end))
        reason="negative_key_default" if key&0x8000 else ("equal_key_WORD" if key==selector else None)
        if reason is not None:
            value_address=p+2
            if value_address>ROM_SIZE-2:
                return dict(**result,status="outside_ROM_value_read_boundary",stop_reason=reason,
                    selected_key_address=p,selected_key_WORD=key,value_address=value_address,trace=trace,read_addresses=reads)
            value=int.from_bytes(image[value_address:value_address+2],"big")
            reads.extend((value_address,value_address+1))
            return dict(**result,status="value_WORD_read",stop_reason=reason,selected_key_address=p,
                selected_key_WORD=key,value_address=value_address,value_WORD=value,
                selected_pair_inside_physical_catalog=start<=p and p+4<=end,trace=trace,read_addresses=reads)
        p=(p+4)&0xFFFFFFFF
    return dict(**result,status="diagnostic_scan_budget_exhausted",next_key_address=p,trace=trace,read_addresses=reads)


def original_witness_read_union(image):
    """Constructed original pair witnesses, not a natural selector/domain proof."""
    result=set()
    for t,group in enumerate(ORIGINAL_KEYS):
        for key in group:
            row=lookup(image,t,0xFFFF if key&0x8000 else key)
            result.update(row["read_addresses"])
    return result


def schema():
    def obj(props): return dict(type="object",properties=props,required=list(props),additionalProperties=False)
    def exact(items): return dict(type="array",prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def fixed(value):
        if type(value) is dict:return obj({k:fixed(v) for k,v in value.items()})
        if type(value) is list:return exact([fixed(v) for v in value])
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    word=dict(type="integer",minimum=0,maximum=65535)
    props={k:fixed(v) for k,v in metadata().items()}
    props["tables"]=exact([obj({**{k:fixed(v) for k,v in table_fixed(t).items()},
        "pairs":exact([obj({**{k:fixed(v) for k,v in pair_fixed(t,i).items()},
            "key_WORD":word,"value_WORD":word}) for i in range(len(ORIGINAL_KEYS[t]))])}) for t in range(10)])
    result=obj(props);result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="Fixed ten physical key/value catalogs; both literal WORDs preserve all 16 editable bits. Key sign changes live default behavior; physical ends and diagnostic budgets are not CPU stops."
    return result


def render_bundle(rom):
    fields=extract(rom);serialized=dump(fields);image=rebuild(rom,load_fields(serialized))
    expected={p for s,e in SPANS for p in range(s,e)}
    if image!=rom or original_witness_read_union(rom)!=expected or len(expected)!=EDITABLE_BYTES:
        raise ValueError("serialized whole-ROM roundtrip or constructed actual source read union differs")
    rows=blocks(rom,fields)
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=10,physical_pairs=58,
        original_positive_keys=54,original_negative_defaults=4,constructed_owned_read_union_bytes=len(expected),
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        original_FFFF_lookups=[lookup(rom,t,0xFFFF) for t in range(10)],
        old_dispatch_directory_emit_bytes=0,reader_code_emit_bytes=0,
        blocks=[{k:v for k,v in r.items() if k!="data"}|dict(bytes=len(r["data"]),sha256=sha(r["data"])) for r in rows])
    members={"fields.json":serialized,"fields.schema.json":dump(schema()),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=10,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError("output must stay in selector pair build scope or exact formal bundle")
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
