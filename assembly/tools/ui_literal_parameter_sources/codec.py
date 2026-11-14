"""184 original source bytes, with separate glyph, LONG, parameter and menu roles.

Literal fields retain all source bits. Diagnostic source views read an edited
whole image, not a clamped physical catalog or an emulated game/CPU.
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
OUTPUT_ROOT=ROOT/"build/ui_literal_parameter_sources"
FORMAL_ROOT=ROOT/"analysis/ui_literal_parameter_sources/generated"
DEFAULT_FIELDS=FORMAL_ROOT/"fields.json"
FORMAT="g5510-literal-UI-distinct-source-roles-v1"
EDITABLE_BYTES=184
MAX_JSON=1024*1024
MEMBERS=frozenset(("fields.json","fields.schema.json","validation.json","manifest.json"))
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
ENHANCED_PATH="analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256=reference_value(__name__, 'ENHANCED_SHA256')
SPANS=((0x8D8,0x8DE),(0x54C6,0x54CA),(0x568E,0x5694),
       (0x124FC,0x1252C),(0x1F97E,0x1F99C),(0x3F8C4,0x3F8DC),
       (0x27F6,0x2806),(0x12840,0x12872))
SOURCE_HASHES=(
    reference_value(__name__, 'SOURCE_HASHES'),
    reference_value(__name__, 'SOURCE_HASHES_2'),
    reference_value(__name__, 'SOURCE_HASHES_3'),
    reference_value(__name__, 'SOURCE_HASHES_4'),
    reference_value(__name__, 'SOURCE_HASHES_5'),
    reference_value(__name__, 'SOURCE_HASHES_6'),
    reference_value(__name__, 'SOURCE_HASHES_7'),
    reference_value(__name__, 'SOURCE_HASHES_8'))
CONSUMERS=(
    (0x82A,0x842,reference_value(__name__, 'CONSUMERS')),
    (0x5474,0x5496,reference_value(__name__, 'CONSUMERS_2')),
    (0x560C,0x5666,reference_value(__name__, 'CONSUMERS_3')),
    (0xAE8A,0xAF1E,reference_value(__name__, 'CONSUMERS_4')),
    (0x12470,0x124FC,reference_value(__name__, 'CONSUMERS_5')),
    (0x1F91C,0x1F97E,reference_value(__name__, 'CONSUMERS_6')),
    (0x3F890,0x3F8C4,reference_value(__name__, 'CONSUMERS_7')),
    (0x27CE,0x27DA,reference_value(__name__, 'CONSUMERS_8')),
    (0x2818,0x2822,reference_value(__name__, 'CONSUMERS_9')),
    (0x1280E,0x12818,reference_value(__name__, 'CONSUMERS_10')),
    (0x12878,0x128E2,reference_value(__name__, 'CONSUMERS_11')))
GLYPH_ROLES=((0x8D8,3,0x836,0x83C),(0x54C6,2,0x5482,0x5490),(0x568E,3,0x5658,0x5660))
MENU_ROLES=((0x27F6,2),(0x12840,6))
sha,dump=shared.sha,shared.dump
keys,same,uint,exact_list=shared.keys,shared.same,shared.uint,shared.exact_list
load_fields=shared.load_fields
safe_path,read_bounded,put=shared.safe_path,shared.read_bounded,shared.put


def image_bytes(image):
    if type(image) is not bytes or len(image)!=ROM_SIZE: raise ValueError("complete bytes image required")


def verify_rom(rom):
    image_bytes(rom)
    if sha(rom)!=ROM_SHA256: raise ValueError("canonical source SHA-256 required")
    for start,end,expected in CONSUMERS:
        if sha(rom[start:end])!=expected: raise ValueError("original consumer source differs")
    for (start,end),expected in zip(SPANS,SOURCE_HASHES):
        if sha(rom[start:end])!=expected: raise ValueError("original literal source differs")


def metadata():
    return dict(format=FORMAT,confidence="candidate",source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        physical_scope=[dict(start=s,end=e,bytes=e-s,sha256=h) for (s,e),h in zip(SPANS,SOURCE_HASHES)],
        evidence=dict(enhanced_ledger=dict(path=ENHANCED_PATH,sha256=ENHANCED_SHA256),
            frozen_raw_layout=dict(id=LAYOUT_ID,raw_bytes=46619,admitted_source_bytes=184,older_typed_overlap_bytes=0),
            pinned_original_consumers=[dict(start=s,end=e,sha256=h) for s,e,h in CONSUMERS],
            glyph=dict(reader=0xAE8A,source_WORD_read=0xAE8E,negative_test=0xAE90,
                negative_WORD_selects_fill_not_font=True,source_count_DBRA=0xAECE,
                roles=[dict(start=s,WORD_count=n,D3_WORD=n-1,LEA=lea,JSR=call) for s,n,lea,call in GLYPH_ROLES],
                font_base=0x8159C,nonnegative_address_formula="8159C + u16(((WORD&FF00)<<3) | ((WORD&00FF)<<5))",
                original_codepoint_bit_mapping_not_Unicode=True,font_and_fill_pixels_not_emitted=True),
            indexed_LONG=dict(first_base=0x124FC,second_base=0x12514,physical_entries_each=6,
                selector_RAM=0xFFFFF39A,index_formula="u16(u16(5-F39A_WORD)<<2), sign extend once for address",
                source_LONG_reads=[0x1249C,0x124B4,0x124CC,0x124E4],
                two_paths="add or subtract under original BYTE-input/timer/LONG carry and comparison guards",
                physical_six_entries_not_CPU_clamp=True,original_cap_and_money_RAM_not_simulated=True),
            battle_pair=dict(producer_start=0x1F91C,LEA=0x1F962,first_BYTE_read=0x1F966,second_BYTE_read=0x1F974,
                first_RAM=0xFFFF80DA,second_RAM=0xFFFF8125,
                original_index_formula="first-match comparison outcome*8 + second-first-match outcome*2",
                comparison_outcomes_each=4,physical_pairs=15,
                code_alias=dict(index_WORD=30,start=0x1F99C,original_BYTES="6100",emitted=False),
                first_index_sign_extend_before_second_displacement_1=True,physical_15_pairs_not_CPU_clamp=True),
            battle_WORDs=dict(LEA=0x3F8AA,reads=[0x3F8B0,0x3F8B6,0x3F8BC],
                guards="RAM80DB BYTE equals3 and RAM80C4 bit7 set",selector_RAM=0xFFFFF320,
                index_formula="(F320_WORD >> 3) & 0006",group_displacements=[0,8,16],
                output_RAMs=[0xFFFFFB02,0xFFFFFB04,0xFFFFFB06],all_full_WORD_bits_preserved=True),
            menu=dict(reader=0x12878,selector_RAM=0xFFFFF38C,full_WORD=True,
                bypass_cmp=0x1287C,bypass_branch=0x12880,bypass_selector_WORD=0x93,
                bypass="original RAM F500 scan, not simulated, source reads none",
                key_WORD_read=0x12884,equality_branch=0x12886,unmatched_skip_8=0x12888,
                matched_LONG_read=0x1288C,matched_WORD_read=0x1289A,record_stride=8,
                true_source_calls=[dict(LEA=0x27CE,JSR=0x27D4),dict(LEA=0x2818,JSR=0x281C),dict(LEA=0x1280E,BSR=0x12814)],
                trailing_key=dict(start=0x12870,end=0x12872,original_WORD=0x93,
                    read_witness_selector_WORD=0,diagnostic_steps=7),
                unread_original_0093_payload=dict(start=0x12872,end=0x12878,bytes=6,emitted=False),
                no_negative_key_sentinel=True,physical_catalogs_are_not_scan_stops=True,
                edited_trailing_key_may_select_unowned_live_payload=True)),
        original_business_names="unknown",natural_reachability_and_all_selector_writers="unknown",
        edited_gameplay_safety="unknown",independent_CPU_comparison=False,
        full_RAM_CCR_stack_bus_UI_and_business_algorithms="not modeled")


def pinned(row,fixed,mutable,label):
    keys(row,set(fixed)|set(mutable),label)
    for key,value in fixed.items(): same(row[key],value,label+"."+key)


def literal(rom,p,width,index,name):
    return dict(index=index,address=p,width_BYTES=width,**{name:int.from_bytes(rom[p:p+width],"big")})


def extract(rom):
    verify_rom(rom); fields=metadata()
    fields["glyph_WORD_lists"]=[dict(index=i,start=s,WORD_count=n,
        glyphs=[literal(rom,s+2*j,2,j,"glyph_WORD") for j in range(n)]) for i,(s,n,*_) in enumerate(GLYPH_ROLES)]
    fields["indexed_LONG_arrays"]=[dict(index=i,start=s,LONG_count=6,
        entries=[literal(rom,s+4*j,4,j,"literal_LONG") for j in range(6)]) for i,s in enumerate((0x124FC,0x12514))]
    fields["battle_BYTE_pairs"]=[dict(index=i,start=0x1F97E+2*i,index_WORD=2*i,
        first_BYTE=rom[0x1F97E+2*i],second_BYTE=rom[0x1F97F+2*i]) for i in range(15)]
    fields["battle_WORD_groups"]=[dict(index=i,start=0x3F8C4+8*i,
        entries=[literal(rom,0x3F8C4+8*i+2*j,2,j,"literal_WORD") for j in range(4)]) for i in range(3)]
    fields["menu_records"]=[dict(index=i,start=s,records=[dict(index=j,start=s+8*j,
        key_WORD=int.from_bytes(rom[s+8*j:s+8*j+2],"big"),
        literal_LONG=int.from_bytes(rom[s+8*j+2:s+8*j+6],"big"),
        literal_WORD=int.from_bytes(rom[s+8*j+6:s+8*j+8],"big")) for j in range(n)]) for i,(s,n) in enumerate(MENU_ROLES)]
    fields["menu_trailing_scan_key"]=dict(address=0x12870,key_WORD=int.from_bytes(rom[0x12870:0x12872],"big"))
    return fields


def blocks(rom,fields):
    original=extract(rom)
    mutable=set(original)-set(metadata()); pinned(fields,metadata(),mutable,"distinct source roles")
    def walk(value,before,label):
        if type(before) is list:
            return b"".join(walk(a,b,label) for a,b in zip(exact_list(value,len(before),label),before))
        if type(before) is dict:
            names={k for k in before if k in ("glyph_WORD","literal_LONG","literal_WORD","first_BYTE","second_BYTE","key_WORD")}
            children={k for k,v in before.items() if type(v) is list}
            pinned(value,{k:v for k,v in before.items() if k not in names|children},names|children,label)
            if children: return b"".join(walk(value[k],before[k],label+"."+k) for k in before if k in children)
            raw=bytearray()
            for k in before:
                if k in names:
                    width=4 if k=="literal_LONG" else (1 if k in ("first_BYTE","second_BYTE") else 2)
                    raw.extend(uint(value[k],(1<<(8*width))-1,label+"."+k).to_bytes(width,"big"))
            return bytes(raw)
        raise ValueError("unexpected source topology")
    glyph=[walk(a,b,"glyph source") for a,b in zip(exact_list(fields["glyph_WORD_lists"],3,"glyph lists"),original["glyph_WORD_lists"])]
    longs=walk(fields["indexed_LONG_arrays"],original["indexed_LONG_arrays"],"two LONG roles")
    pairs=walk(fields["battle_BYTE_pairs"],original["battle_BYTE_pairs"],"battle BYTE pairs")
    words=walk(fields["battle_WORD_groups"],original["battle_WORD_groups"],"three WORD roles")
    menus=[walk(a,b,"menu source") for a,b in zip(exact_list(fields["menu_records"],2,"two menu roles"),original["menu_records"])]
    tail=walk(fields["menu_trailing_scan_key"],original["menu_trailing_scan_key"],"trailing scan key")
    data=glyph+[longs,pairs,words,menus[0],menus[1]+tail]
    if [len(b) for b in data]!=[e-s for s,e in SPANS]: raise ValueError("fixed 184-byte source costs differ")
    return [dict(id=f"rom_{s:06X}_literal_role_{i}",start=s,end=e,data=b,
        role=("glyph_WORD","indexed_LONG","battle_BYTE_pair","battle_WORD","menu_record_or_scan_key")[0 if i<3 else i-2 if i<6 else 4])
        for i,((s,e),b) in enumerate(zip(SPANS,data))]


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields): image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def read_source(image,p,width):
    image_bytes(image)
    if not 0<=p<=ROM_SIZE-width: return dict(status="outside_ROM_source_boundary",address=p,width_BYTES=width)
    return dict(status="source_read",address=p,width_BYTES=width,value=int.from_bytes(image[p:p+width],"big"),
        read_addresses=list(range(p,p+width)))


def s16(word): return word-65536 if word&0x8000 else word


def glyph_source_view(image,role):
    role=uint(role,2,"glyph role");s,n,*_=GLYPH_ROLES[role]; rows=[]
    for i in range(n):
        row=read_source(image,s+2*i,2);w=row["value"]
        row.update(kind="negative_WORD_fill" if w&0x8000 else "glyph_source_address",
            glyph_source=None if w&0x8000 else 0x8159C+((((w&0xFF00)<<3)|((w&255)<<5))&65535))
        rows.append(row)
    return rows


def indexed_LONG_source_view(image,F39A_WORD):
    selector=uint(F39A_WORD,65535,"complete F39A WORD")
    offset=((5-selector)<<2)&65535
    return dict(index_WORD=offset,signed_index=s16(offset),catalog_is_CPU_clamp=False,
        first=read_source(image,0x124FC+s16(offset),4),second=read_source(image,0x12514+s16(offset),4))


def battle_pair_source_view(image,index_WORD):
    offset=s16(uint(index_WORD,65535,"complete formed BYTE-pair index WORD"))
    return dict(index_WORD=index_WORD,signed_index=offset,physical_pairs_not_CPU_clamp=True,
        first=read_source(image,0x1F97E+offset,1),second=read_source(image,0x1F97F+offset,1))


def battle_WORD_source_view(image,F320_WORD,guard_80DB_BYTE=3,guard_80C4_BYTE=0x80):
    value=uint(F320_WORD,65535,"complete F320 WORD")
    byte=uint(guard_80DB_BYTE,255,"complete 80DB BYTE");flag=uint(guard_80C4_BYTE,255,"complete 80C4 BYTE")
    if byte!=3 or not flag&128: return dict(status="original_guard_bypass",reads=[])
    offset=(value>>3)&6
    return dict(status="source_reads",index_WORD=offset,reads=[read_source(image,0x3F8C4+d+offset,2) for d in (0,8,16)])


def menu_source_view(image,role,selector_WORD,scan_budget=256):
    image_bytes(image);role=uint(role,1,"physical menu role");selector=uint(selector_WORD,65535,"complete F38C WORD")
    budget=uint(scan_budget,ROM_SIZE//8,"diagnostic budget")
    if not budget: raise ValueError("positive diagnostic budget required")
    if selector==0x93: return dict(status="original_0093_RAM_bypass",reads=[],RAM_path_simulated=False)
    p=MENU_ROLES[role][0];reads=[]
    for _ in range(budget):
        key=read_source(image,p,2);reads.append(key)
        if key["status"]!="source_read": return dict(status=key["status"],reads=reads)
        if key["value"]==selector:
            value=read_source(image,p+2,4);word=read_source(image,p+6,2)
            reads.extend((value,word))
            return dict(status="matched_source_record" if value["status"]==word["status"]=="source_read" else "outside_ROM_payload_boundary",
                matched_key_address=p,reads=reads,literal_LONG=value.get("value"),literal_WORD=word.get("value"),
                natural_execution=False,CPU_execution=False)
        p=(p+8)&0xFFFFFFFF
    return dict(status="diagnostic_budget_exhausted",reads=reads,next_key_address=p,budget_is_CPU_stop=False)


def constructed_read_union(rom):
    reads=[]
    for role in range(3): reads.extend(glyph_source_view(rom,role))
    for F39A in range(6):
        view=indexed_LONG_source_view(rom,F39A);reads.extend((view["first"],view["second"]))
    for index in range(0,30,2):
        view=battle_pair_source_view(rom,index);reads.extend((view["first"],view["second"]))
    for F320 in (0,16,32,48): reads.extend(battle_WORD_source_view(rom,F320)["reads"])
    for role,(s,n) in enumerate(MENU_ROLES):
        for i in range(n): reads.extend(menu_source_view(rom,role,int.from_bytes(rom[s+8*i:s+8*i+2],"big"))["reads"])
    reads.extend(menu_source_view(rom,1,0,7)["reads"])
    return {p for row in reads for p in row.get("read_addresses",[])}


def schema(rom):
    editable={"glyph_WORD":65535,"literal_LONG":0xFFFFFFFF,"literal_WORD":65535,
              "first_BYTE":255,"second_BYTE":255,"key_WORD":65535}
    def walk(value,field=None):
        if field in editable: return dict(type="integer",minimum=0,maximum=editable[field])
        if type(value) is dict:
            props={k:walk(v,k) for k,v in value.items()}
            return dict(type="object",properties=props,required=list(props),additionalProperties=False)
        if type(value) is list:
            return dict(type="array",prefixItems=[walk(v) for v in value],items=False,minItems=len(value),maxItems=len(value))
        if value is None: return dict(type="null",const=None)
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    result=walk(extract(rom));result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    return result


def render_bundle(rom):
    fields=extract(rom);serialized=dump(fields);image=rebuild(rom,load_fields(serialized)); rows=blocks(rom,fields)
    expected={p for s,e in SPANS for p in range(s,e)}
    if image!=rom or constructed_read_union(rom)!=expected or len(expected)!=184:
        raise ValueError("exact whole-image/source read union differs")
    report=dict(**metadata(),editable_bytes=184,physical_blocks=8,constructed_source_read_union_BYTES=184,
        role_BYTE_costs=dict(glyph_WORDs=16,indexed_LONGs=48,battle_BYTE_pairs=30,battle_WORD_groups=24,menu_records_and_key=66),
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        pair_code_alias=battle_pair_source_view(image,30),menu_0093_bypass=menu_source_view(image,1,0x93),
        trailing_key_read=menu_source_view(image,1,0,7),
        blocks=[{k:v for k,v in r.items() if k!="data"}|dict(bytes=len(r["data"]),sha256=sha(r["data"])) for r in rows])
    members={"fields.json":serialized,"fields.schema.json":dump(schema(rom)),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=184,physical_blocks=8,
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
    parser.add_argument("--rom",default=str(DEFAULT_ROM));parser.add_argument("--fields")
    parser.add_argument("--bundle");parser.add_argument("--output")
    args=parser.parse_args(argv);target=None
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
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items(): put(target/name,data)
        result=dict(path=str(target),editable_bytes=184,members={name:sha(data) for name,data in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS: raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data: raise ValueError("canonical bundle drift: "+name)
        result=dict(verified=True,editable_bytes=184,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None: put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=184,exact_canonical=image==rom,
            bytes=len(image),sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=="__main__": raise SystemExit(main())
