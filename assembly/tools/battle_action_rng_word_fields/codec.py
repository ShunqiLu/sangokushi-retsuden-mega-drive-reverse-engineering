"""60 lossless source bytes for five original six-WORD RNG parameter groups.

Only complete literal WORDs are editable. Mask/threshold views are derived.
D6 is already a WORD byte offset; physical six-item groups never clamp CPU
inputs. Diagnostics take supplied RNG WORDs and do not generate random values.
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
OUTPUT_ROOT = ROOT / "build/battle_action_rng_word_fields"
FORMAL_ROOT = ROOT / "analysis/battle_action_rng_word_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 60
FORMAT = "g5510-battle-action-RNG-literal-WORD-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
SPANS = ((0x2A6B4,0x2A6CC),(0x2A6F2,0x2A6FE),(0x2A9E2,0x2A9FA))
# Physical start, original PC-indexed read, signed displacement BYTE, true BSR.
TABLES = ((0x2A6B4,0x2A6DA,0xD8,0x2A6DE),
          (0x2A6C0,0x2A6E4,0xDA,0x2A6E8),
          (0x2A6F2,0x2A6FE,0xF2,0x2A702),
          (0x2A9E2,0x2A9C8,0x18,0x2A9CC),
          (0x2A9EE,0x2A9D4,0x18,0x2A9D8))
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_BANK_SHA256 = reference_value(__name__, 'LAYOUT_BANK_SHA256')
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
THRESHOLDS = (0x28,0x3C,0x50,0x64,0x78,0xFFFF)
THRESHOLD_SOURCE = (0x2A308,0x2A314,
    reference_value(__name__, 'THRESHOLD_SOURCE'))
CONSUMERS = (
    (0x28F90,0x28F9C,reference_value(__name__, 'CONSUMERS')),
    (0x2A2D8,0x2A2EE,reference_value(__name__, 'CONSUMERS_2')),
    (0x2A5F4,0x2A6B4,reference_value(__name__, 'CONSUMERS_3')),
    (0x2A6CC,0x2A6F2,reference_value(__name__, 'CONSUMERS_4')),
    (0x2A6FE,0x2A70C,reference_value(__name__, 'CONSUMERS_5')),
    (0x2A9C8,0x2A9E2,reference_value(__name__, 'CONSUMERS_6')),
    (0x2A9FA,0x2AA14,reference_value(__name__, 'CONSUMERS_7')),
    (0x83D4,0x83FA,reference_value(__name__, 'CONSUMERS_8')),
)
sha,dump = shared.sha,shared.dump
keys,same,uint,exact_list = shared.keys,shared.same,shared.uint,shared.exact_list
load_fields = shared.load_fields
safe_path,read_bounded,put = shared.safe_path,shared.read_bounded,shared.put


def signed_WORD(word):
    word=uint(word,65535,"WORD")
    return word-65536 if word&32768 else word


def image_bytes(image):
    if type(image) is not bytes or len(image)!=ROM_SIZE:
        raise ValueError("complete bytes image required")


def verify_rom(rom):
    image_bytes(rom)
    if sha(rom)!=ROM_SHA256: raise ValueError("canonical source SHA-256 required")
    for start,end,expected in CONSUMERS+(THRESHOLD_SOURCE,):
        if sha(rom[start:end])!=expected: raise ValueError("pinned original source/consumer body differs")
    if sha(b"".join(rom[s:e] for s,e in SPANS))!=SOURCE_SHA256:
        raise ValueError("original literal parameter source differs")


def table_fixed(index):
    start,read,displacement,call=TABLES[index]
    return dict(id=f"rom_{start:06X}_battle_RNG_WORDs",index=index,start=start,end=start+12,
        WORD_count=6,WORD_order="big",read_PC=read,read_PC_base=read+2,
        signed_displacement_BYTE=displacement,BSR_PC=call,BSR_target=0x2AA00)


def metadata():
    return dict(format=FORMAT,confidence="candidate",source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        physical_scope=[dict(start=s,end=e,bytes=e-s) for s,e in SPANS],
        source_union_sha256=SOURCE_SHA256,
        evidence=dict(source="canonical indexed WORD readers, actual D6 producer and true RNG-predicate calls",
            enhanced_ledger=dict(path=ENHANCED_PATH,sha256=ENHANCED_SHA256,
                action_consumer_confidence="heuristic",RNG_body_confidence="confirmed"),
            frozen_raw_layout=dict(id=LAYOUT_ID,bank02_sha256=LAYOUT_BANK_SHA256,
                emitted_raw_bytes=EDITABLE_BYTES,older_typed_overlap_bytes=0),
            consumers=[dict(start=s,end=e,sha256=h) for s,e,h in CONSUMERS],
            already_typed_threshold_source=dict(start=THRESHOLD_SOURCE[0],end=THRESHOLD_SOURCE[1],
                sha256=THRESHOLD_SOURCE[2],original_WORDs=list(THRESHOLDS),physical_emit=False),
            D6_producer=dict(input_read=0x2A2D8,input="complete WORD at A0+1E",
                A2_LEA=0x2A2DC,PC_base=0x2A2DE,displacement_WORD=0x002A,
                true_BSR=0x2A2E2,callee=0x28F90,D1_to_D6=0x2A2E6,
                original_D1_start=0xFFFE,ADDQ_WORD_2=0x28F94,
                unsigned_compare_WORD_postincrement=0x28F96,BCC_continue=0x28F98,
                local_input_witnesses=[0,0x28,0x3C,0x50,0x64,0x78],
                corresponding_returned_D6_WORD_byte_offsets=[0,2,4,6,8,10],
                D6_already_byte_offset_no_second_multiply=True,
                input_FFFF="no WORD threshold can be greater; continuation/scanning boundary not modeled",
                natural_input_domain="unknown"),
            parameter_reads=[table_fixed(i) for i in range(5)],
            addressing=dict(index="signed complete D6.W byte offset, not slot index",
                physical_six_WORD_groups_are_not_CPU_clamps=True,
                odd_WORD_addresses_are_external_address_exception_boundaries=True,
                neighbor_and_code_aliases_use_edited_image=True),
            predicate=dict(entry=0x2AA00,copy_WORD=0x2AA00,mask_WORD=0x2AA02,
                mask=7,threshold_LSR_WORD_4=0x2AA06,actual_RNG_JSR=0x2AA08,
                RNG_entry=0x83D4,RNG_low_WORD_AND=0x2AA0E,unsigned_CMP_WORD=0x2AA10,
                BCS="unsigned (supplied_original_RNG_WORD & (source_WORD & 7)) < (source_WORD >> 4)",
                source_bit3_ignored_by_this_predicate_but_retained=True,
                upper12_threshold_bits_retained=True,actual_RNG_D2_D3_D6_preserved=True,
                RNG_input_is_supplied_not_generated=True,
                natural_RNG_state_distribution_or_uniformity="unknown")),
        table_business_names="unknown",edited_gameplay_safety="unknown",
        natural_domains_and_all_callers="unknown",independent_CPU_comparison=False,
        exclusions=dict(old_threshold_12B_not_emitted=True,code_aliases_not_emitted=True,
                        full_RAM_flags_stack_bus_CPU_algorithm_not_modeled=True))


def pinned(row,fixed,mutable,label):
    keys(row,set(fixed)|set(mutable),label)
    for key,value in fixed.items(): same(row[key],value,label+"."+key)


def extract(rom):
    verify_rom(rom)
    result=metadata()
    result["parameter_tables"]=[dict(**table_fixed(i),WORDs=[int.from_bytes(rom[p:p+2],"big")
        for p in range(spec[0],spec[0]+12,2)]) for i,spec in enumerate(TABLES)]
    return result


def blocks(rom,fields):
    verify_rom(rom)
    pinned(fields,metadata(),{"parameter_tables"},"battle RNG source package")
    data=[]
    for i,row in enumerate(exact_list(fields["parameter_tables"],5,"five physical parameter tables")):
        pinned(row,table_fixed(i),{"WORDs"},"parameter table")
        data.append(b"".join(uint(w,65535,"complete literal parameter WORD").to_bytes(2,"big")
            for w in exact_list(row["WORDs"],6,"fixed six WORD source cost")))
    grouped=(data[0]+data[1],data[2],data[3]+data[4])
    result=[dict(id=f"rom_{s:06X}_battle_RNG_source_span",start=s,end=e,data=raw,
                 role="confirmed_full_WORD_RNG_parameter_sources")
            for (s,e),raw in zip(SPANS,grouped)]
    if [len(r["data"]) for r in result]!=[24,12,24] or any(
            a["end"]>b["start"] for a,b in zip(result,result[1:])):
        raise ValueError("three disjoint 24+12+24 source byte costs differ")
    return result


def rebuild(rom,fields):
    rows=blocks(rom,fields); image=bytearray(rom)
    for row in rows: image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def predicate(source_WORD,supplied_RNG_WORD):
    """Narrow original CMP.W carry predicate with already supplied RNG output.

    No RNG generation/distribution, other condition flags, original D0.L upper
    half, caller effects or full CPU behavior is claimed by this diagnostic.
    """
    word=uint(source_WORD,65535,"source WORD")
    rng=uint(supplied_RNG_WORD,65535,"supplied original RNG output WORD")
    mask,threshold=word&7,word>>4
    masked=rng&mask
    return dict(source_WORD=word,supplied_RNG_WORD=rng,mask_WORD=mask,
                threshold_WORD=threshold,ignored_bit3=(word>>3)&1,
                masked_RNG_WORD=masked,BCS=masked<threshold,
                source_only=True,natural_execution=False,CPU_execution=False)


def lookup(image,table_index,D6_WORD,supplied_RNG_WORD=None):
    """Read a live signed-indexed WORD, including edited neighbor/code aliases.

    The 0..4 table-role selector is diagnostic catalog choice, not original D6.
    D6 is already a byte offset. Odd reads are reported without host decoding;
    this diagnostic does not execute the original address exception or callee.
    """
    image_bytes(image)
    index=uint(table_index,4,"physical table role selector")
    d6=uint(D6_WORD,65535,"already fetched D6 WORD byte offset")
    if supplied_RNG_WORD is not None: uint(supplied_RNG_WORD,65535,"supplied original RNG output WORD")
    start=TABLES[index][0]
    address=(start+signed_WORD(d6))&0xFFFFFFFF
    result=dict(table_index=index,D6_WORD=d6,read_PC=TABLES[index][1],read_address=address,
                read_inside_editable_table=start<=address<start+12,
                source_only=True,natural_execution=False,CPU_execution=False)
    if address&1: return dict(**result,status="odd_WORD_address_exception_boundary")
    if not 0<=address<=ROM_SIZE-2: return dict(**result,status="outside_ROM_read_boundary")
    word=int.from_bytes(image[address:address+2],"big")
    result.update(status="source_WORD_read",source_WORD=word)
    if supplied_RNG_WORD is not None: result["predicate"]=predicate(word,supplied_RNG_WORD)
    return result


def source_reference_union(image):
    """Declared local D6 return witnesses, not all natural/possible reads."""
    addresses=set()
    for t in range(5):
        for d6 in (0,2,4,6,8,10):
            row=lookup(image,t,d6)
            addresses.update(range(row["read_address"],row["read_address"]+2))
    return addresses


def schema():
    def obj(properties):
        return dict(type="object",properties=properties,required=list(properties),additionalProperties=False)
    def exact(items):
        return dict(type="array",prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def fixed(value):
        if type(value) is dict: return obj({k:fixed(v) for k,v in value.items()})
        if type(value) is list: return exact([fixed(v) for v in value])
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    props={k:fixed(v) for k,v in metadata().items()}
    props["parameter_tables"]=exact([obj({**{k:fixed(v) for k,v in table_fixed(i).items()},
        "WORDs":dict(type="array",minItems=6,maxItems=6,
                     items=dict(type="integer",minimum=0,maximum=65535))}) for i in range(5)])
    result=obj(props); result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="Five complete literal WORD sources. Derived mask/threshold are not editing authority; bit3 retained; D6 is a full signed WORD byte offset and source catalog counts are not CPU clamps."
    return result


def render_bundle(rom):
    fields=extract(rom); serialized=dump(fields); image=rebuild(rom,load_fields(serialized))
    rows=blocks(rom,fields); expected={p for s,e in SPANS for p in range(s,e)}
    if image!=rom or source_reference_union(rom)!=expected or len(expected)!=EDITABLE_BYTES:
        raise ValueError("serialized whole-ROM roundtrip or actual owned source union differs")
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=3,physical_parameter_tables=5,
        parameter_WORDs=30,local_owned_read_union_bytes=len(expected),whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),
        original_WORDs=[row["WORDs"] for row in fields["parameter_tables"]],
        original_derived_views=[[predicate(word,0) for word in row["WORDs"]] for row in fields["parameter_tables"]],
        D6_000C_live_aliases=[lookup(rom,t,12) for t in range(5)],
        D6_FFFF_odd_boundaries=[lookup(rom,t,65535) for t in range(5)],
        old_threshold_source_emit_bytes=0,
        blocks=[{k:v for k,v in row.items() if k!="data"}|dict(bytes=len(row["data"]),sha256=sha(row["data"])) for row in rows])
    members={"fields.json":serialized,"fields.schema.json":dump(schema()),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=3,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError("output must stay in battle RNG source build scope or exact formal bundle")
    if path.exists() or not path.parent.is_dir(): raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM)); parser.add_argument("--fields")
    parser.add_argument("--bundle"); parser.add_argument("--output")
    args=parser.parse_args(argv); target=None
    if args.command=="export":
        if args.output is None or args.fields is not None or args.bundle is not None: raise ValueError("export requires fresh output only")
        target=fresh_output(args.output,bundle=True)
    elif args.command=="import":
        if args.output is None or args.bundle is not None: raise ValueError("import requires fields and fresh output")
        target=fresh_output(args.output)
        if target.suffix.lower()!=".bin": raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.bundle is not None and args.fields is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=="export":
        members=render_bundle(rom); target.mkdir()
        for name,data in members.items(): put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={name:sha(data) for name,data in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS: raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data: raise ValueError("canonical generated bundle drift: "+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)); image=rebuild(rom,fields)
        if target is not None: put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=EDITABLE_BYTES,
                    exact_canonical=image==rom,bytes=len(image),sha256=sha(image))
    print(json.dumps(result,sort_keys=True)); return 0


if __name__=="__main__": raise SystemExit(main())
