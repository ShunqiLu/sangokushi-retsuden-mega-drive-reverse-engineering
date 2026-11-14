"""144 literal battle-action BYTE sources under the original shared reader.

Physical 3-mode/3-type catalogs are editor allocations, never CPU clamps.
The source view keeps two live mode reads separate and takes a supplied RNG WORD.
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
OUTPUT_ROOT=ROOT/"build/battle_action_byte_fields"
FORMAL_ROOT=ROOT/"analysis/battle_action_byte_fields/generated"
DEFAULT_BUNDLE=FORMAL_ROOT
DEFAULT_FIELDS=FORMAL_ROOT/"fields.json"
FORMAT="g5510-battle-action-literal-BYTE-sources-v1"
EDITABLE_BYTES=144
MAX_JSON=1024*1024
MEMBERS=frozenset(("fields.json","fields.schema.json","validation.json","manifest.json"))
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
MAP_PATH="analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
MAP_SHA256=reference_value(__name__, 'MAP_SHA256')
# Source start/end, unsigned quantity threshold, original entry, three LEA PCs.
TABLES=(
    (0x2A39E,0x2A3C2,70,0x2A344,(0x2A34C,0x2A360,0x2A36A)),
    (0x2A3F4,0x2A418,60,0x2A3C2,(0x2A3CA,0x2A3DE,0x2A3E8)),
    (0x2A44C,0x2A470,60,0x2A418,(0x2A420,0x2A434,0x2A43E)),
    (0x2A4A6,0x2A4CA,50,0x2A470,(0x2A478,0x2A48C,0x2A496)),
)
SOURCE_HASHES=(
    reference_value(__name__, 'SOURCE_HASHES'),
    reference_value(__name__, 'SOURCE_HASHES_2'),
    reference_value(__name__, 'SOURCE_HASHES_3'),
    reference_value(__name__, 'SOURCE_HASHES_4'),
)
BODIES=(
    (0x27388,0x2738C,reference_value(__name__, 'BODIES')),
    (0x273B6,0x273BA,reference_value(__name__, 'BODIES_2')),
    (0x2A29A,0x2A308,reference_value(__name__, 'BODIES_3')),
    (0x2A314,0x2A344,reference_value(__name__, 'BODIES_4')),
    (0x2A344,0x2A39E,reference_value(__name__, 'BODIES_5')),
    (0x2A3C2,0x2A3F4,reference_value(__name__, 'BODIES_6')),
    (0x2A418,0x2A44C,reference_value(__name__, 'BODIES_7')),
    (0x2A470,0x2A4A4,reference_value(__name__, 'BODIES_8')),
    (0x83D4,0x83FA,reference_value(__name__, 'BODIES_9')),
)
sha,dump=shared.sha,shared.dump
keys,same,uint,exact_list=shared.keys,shared.same,shared.uint,shared.exact_list
load_fields=shared.load_fields
safe_path,read_bounded,put=shared.safe_path,shared.read_bounded,shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE or sha(rom)!=ROM_SHA256:
        raise ValueError("canonical full ROM bytes, size and SHA-256 required")
    for start,end,digest in BODIES:
        if sha(rom[start:end])!=digest: raise ValueError("pinned original caller/reader differs")
    for (start,end,*_),digest in zip(TABLES,SOURCE_HASHES):
        if sha(rom[start:end])!=digest: raise ValueError("pinned literal source differs")


def metadata():
    return dict(format=FORMAT,confidence="candidate",source_format_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        physical_scope=[dict(start=s,end=e,bytes=e-s,sha256=h) for (s,e,*_),h in zip(TABLES,SOURCE_HASHES)],
        evidence=dict(consumers=[dict(start=s,end=e,sha256=h) for s,e,h in BODIES],
            original_ledger=dict(path=MAP_PATH,sha256=MAP_SHA256,reachability_confidence="heuristic"),
            accepted_raw_snapshot=dict(layout=LAYOUT_ID,resources=61,raw_BYTES=47829,
                source_raw_difference_BYTES=144,source_typed_overlap_BYTES=0),
            callers=[dict(PC=0x27388,entry=0x2A29A),dict(PC=0x273B6,entry=0x2A29A)],
            dispatch=dict(call=0x2A2FA,PC_base=0x2A2FC,displacement_BYTE=0x18,base=0x2A314,
                shifted_index_WORD_PC=0x2A2F8,
                branch_PCs=[0x2A314,0x2A318,0x2A31C,0x2A320,0x2A324,0x2A328],
                original_branch_targets=[0x2A470,0x2A470,0x2A418,0x2A418,0x2A3C2,0x2A344],
                subsequent_JMP_PC=0x2A304,subsequent_JMP_base=0x2A32C),
            mode=dict(RAM_WORD=0xFFEFD2,first_read="TST.W independently live",second_read="CMPI.W2 independently live when first nonzero",
                first_read_PCs=[0x2A344,0x2A3C2,0x2A418,0x2A470],
                second_read_PCs=[0x2A356,0x2A3D4,0x2A42A,0x2A482],
                selection="first==0:base0; otherwise second==2:base2; otherwise base1",
                two_reads_assumed_atomic=False),
            reader=dict(compare_PC=0x2A374,quantity_WORD_object_offset=0x1C,
                unsigned_BCS_PC=0x2A378,BCS_condition="unsigned threshold < quantity",
                plus2_PC=0x2A37A,plus2_condition="unsigned quantity <= threshold including tie",
                type_WORD_read=0x2A37C,type_WORD_object_offset=0x0C,
                ASL_WORD2_PC=0x2A380,signed_LEA_PC=0x2A382,
                RNG_call=0x2A386,RNG_entry=0x83D4,RNG_result_WORD_mask=1,
                RNG_lowbit_mask_PC=0x2A38C,plus1_PC=0x2A392,
                CLR_WORD_PC=0x2A394,BYTE_read_PC=0x2A396,output_WORD_write_PC=0x2A398,
                output_object_WORD_offset=0x24,RNG_A2_preserved_by_pinned_helper=True,
                actual_natural_RNG_input_domain="unknown")),
        exclusions=dict(unread_2A4A4_2A4A6_gap_BYTES=2,code_and_neighbor_aliases_not_emitted=True),
        independent_CPU_comparison=False,source_business_meaning="unknown",
        claims=dict(all_literal_BYTE_bits_preserved=True,CPU_type_or_mode_clamp=False,
            full_RNG_RAM_stack_bus_execution=False,natural_gameplay_domain_complete=False,
            recovered_functions_added=0,high_level_semantic_compiler_coverage_added=0))


def pinned(value,expected,mutable,label):
    keys(value,{*expected,*mutable},label)
    for key,original in expected.items(): same(value[key],original,label+"."+key)


def table_fixed(index):
    start,end,threshold,entry,LEAs=TABLES[index]
    return dict(id=f"rom_{start:06X}_battle_action_BYTE_source",table_index=index,start=start,end=end,
        role="literal_BYTE_written_as_object_action_WORD",threshold_WORD=threshold,
        original_entry=entry,mode_catalog_count=3,type_catalog_count=3,
        original_LEA_PCs=list(LEAs),mode_bases=[start+12*i for i in range(3)])


def pair_fixed(table,mode,type_slot,side):
    start=TABLES[table][0]+12*mode+4*type_slot+2*side
    threshold=TABLES[table][2]
    return dict(id=f"rom_{start:06X}_RNG_bit_BYTE_pair",start=start,end=start+2,
        mode_slot=mode,type_slot=type_slot,
        quantity_side="at_or_below_threshold" if side else "above_threshold",
        constructed_witness=dict(mode_first_WORD=0 if mode==0 else 1,
            mode_second_WORD=2 if mode==2 else mode,type_WORD=type_slot,
            quantity_WORD=threshold if side else threshold+1),
        natural_input_confidence="unknown")


def source_view(image,table_index,mode_first_WORD,mode_second_WORD,type_WORD,quantity_WORD,RNG_output_WORD):
    """Exact local source-read projection, with supplied two mode reads and RNG WORD.

    This does not execute RNG, dispatch, other objects, or final hardware/gameplay.
    """
    if type(image) is not bytes or len(image)!=ROM_SIZE:
        raise ValueError("complete edited bytes image required")
    table=uint(table_index,3,"physical table role")
    first=uint(mode_first_WORD,65535,"first live mode WORD")
    second=uint(mode_second_WORD,65535,"second live mode WORD")
    kind=uint(type_WORD,65535,"full type WORD")
    quantity=uint(quantity_WORD,65535,"unsigned quantity WORD")
    rng=uint(RNG_output_WORD,65535,"supplied RNG output WORD")
    mode=0 if first==0 else (2 if second==2 else 1)
    offset=(kind<<2)&65535
    signed_offset=offset-65536 if offset&32768 else offset
    side=2 if quantity<=TABLES[table][2] else 0
    address=TABLES[table][0]+12*mode+side+signed_offset+(rng&1)
    if not 0<=address<ROM_SIZE: raise ValueError("source read outside provided ROM")
    return dict(table_index=table,selected_mode=mode,second_mode_read_used=first!=0,
        type_index_WORD=offset,signed_type_offset=signed_offset,quantity_pair_BYTE_offset=side,
        supplied_RNG_low_bit=rng&1,address=address,BYTE=image[address],written_object_WORD=image[address],
        inside_authored_table=TABLES[table][0]<=address<TABLES[table][1],
        RNG_executed=False,full_CPU_execution=False)


def extract(rom):
    verify_rom(rom)
    tables=[]
    for t in range(4):
        pairs=[]
        for mode in range(3):
            for kind in range(3):
                for side in range(2):
                    fixed=pair_fixed(t,mode,kind,side)
                    pairs.append(dict(**fixed,RNG_bit0_BYTE=rom[fixed["start"]],RNG_bit1_BYTE=rom[fixed["start"]+1]))
        tables.append(dict(**table_fixed(t),pairs=pairs))
    return dict(**metadata(),tables=tables)


def blocks(rom,fields):
    verify_rom(rom)
    pinned(fields,metadata(),{"tables"},"battle action BYTE source package")
    result=[]
    for t,table in enumerate(exact_list(fields["tables"],4,"physical tables")):
        pinned(table,table_fixed(t),{"pairs"},"physical table")
        raw=bytearray()
        for i,pair in enumerate(exact_list(table["pairs"],18,"physical two-BYTE pairs")):
            mode,remainder=divmod(i,6)
            kind,side=divmod(remainder,2)
            pinned(pair,pair_fixed(t,mode,kind,side),{"RNG_bit0_BYTE","RNG_bit1_BYTE"},"literal BYTE pair")
            raw.extend((uint(pair["RNG_bit0_BYTE"],255,"RNG bit0 BYTE"),uint(pair["RNG_bit1_BYTE"],255,"RNG bit1 BYTE")))
        result.append(dict(id=table["id"],start=table["start"],end=table["end"],
            data=bytes(raw),role="confirmed_full_BYTE_battle_action_source"))
    if sum(len(r["data"]) for r in result)!=144: raise ValueError("fixed144 source byte cost differs")
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
    fields=extract(rom)
    props={k:fixed(v) for k,v in metadata().items()}
    tables=[]
    for table in fields["tables"]:
        pairs=[]
        for pair in table["pairs"]:
            pairs.append(obj({k:dict(type="integer",minimum=0,maximum=255) if k in
                ("RNG_bit0_BYTE","RNG_bit1_BYTE") else fixed(v) for k,v in pair.items()}))
        tables.append(obj({**{k:fixed(v) for k,v in table.items() if k!="pairs"},"pairs":exact(pairs)}))
    props["tables"]=exact(tables)
    result=obj(props); result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="All144 literal BYTEs editable; fixed physical addresses and diagnostic witnesses, not CPU clamps."
    return result


def render_bundle(rom):
    fields=extract(rom); serialized=dump(fields)
    image=rebuild(rom,load_fields(serialized)); encoded=blocks(rom,fields)
    views=[source_view(image,t,**pair["constructed_witness"],RNG_output_WORD=bit)
        for t,table in enumerate(fields["tables"]) for pair in table["pairs"] for bit in (0,1)]
    read_union={v["address"] for v in views}
    authored={p for row in encoded for p in range(row["start"],row["end"])}
    if image!=rom or read_union!=authored or len(read_union)!=144:
        raise ValueError("whole-ROM serialized roundtrip or exact read union differs")
    report=dict(**metadata(),editable_bytes=144,physical_blocks=4,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),constructed_source_read_union_BYTES=len(read_union),
        all144_BYTE_read_witnesses=views,
        alias_examples=[source_view(image,0,1,1,v,71,0) for v in (3,0x4000,0x2000,0xFFFF)],
        blocks=[{k:v for k,v in row.items() if k!="data"}|dict(bytes=len(row["data"]),sha256=sha(row["data"])) for row in encoded])
    members={"fields.json":serialized,"fields.schema.json":dump(schema(rom)),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=144,physical_blocks=4,
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
        result=dict(path=str(target),editable_bytes=144,members={name:sha(data) for name,data in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS: raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data: raise ValueError("canonical bundle drift: "+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=144,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None: put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=144,exact_canonical=image==rom,
            bytes=len(image),sha256=sha(image))
    print(json.dumps(result,sort_keys=True)); return 0


if __name__=="__main__": raise SystemExit(main())
