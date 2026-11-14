"""192 actually-readable bytes of original primary/secondary WORD thresholds.

Three primary physical catalogs have 15 pairs each, plus three secondary pairs.
The three 4-byte gaps stay raw. Catalogs are not CPU selector clamps. Pure data
APIs preserve every literal WORD; only the CLI opens or writes files.
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
OUTPUT_ROOT = ROOT / "build/ai_threshold_pair_fields"
FORMAL_ROOT = ROOT / "analysis/ai_threshold_pair_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 192
FORMAT = "g5510-AI-threshold-literal-WORD-pair-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
PRIMARY_BASE, SECONDARY_BASE = 0x311FC, 0x312BC
PRIMARY_STARTS = (0x311FC, 0x3123C, 0x3127C)
GAPS = (0x31238, 0x31278, 0x312B8)
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = "build/direct_code/layout/" + LAYOUT_ID + "/m68k_bank03.s"
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
CONSUMERS = (
    (0x30EB4,0x30ED8,reference_value(__name__, 'CONSUMERS')),
    (0x30ED8,0x30EE8,reference_value(__name__, 'CONSUMERS_2')),
    (0x30EE8,0x30F54,reference_value(__name__, 'CONSUMERS_3')),
    (0x3096A,0x309A2,reference_value(__name__, 'CONSUMERS_4')),
    (0x30FAA,0x30FD8,reference_value(__name__, 'CONSUMERS_5')),
    (0x31110,0x3117C,reference_value(__name__, 'CONSUMERS_6')),
    (0x32500,0x3251E,reference_value(__name__, 'CONSUMERS_7')),
    (0x3076E,0x30776,reference_value(__name__, 'CONSUMERS_8')),
    (0x2AD88,0x2ADB8,reference_value(__name__, 'CONSUMERS_9')),
    (0x2B01A,0x2B050,reference_value(__name__, 'CONSUMERS_10')),
)
INSTRUCTIONS = (
    (0x30EB8,"43fa001e","heuristic"), (0x30EBE,"303c000f","heuristic"),
    (0x30EC2,"10d9","heuristic"), (0x30EC4,"51c8fffc","heuristic"),
    (0x30F08,"14300000","heuristic"), (0x30F0C,"6b000012","heuristic"),
    (0x30F10,"16301000","heuristic"), (0x30F14,"6b00000a","heuristic"),
    (0x30F32,"12300000","runtime_confirmed"), (0x30F36,"4881","runtime_confirmed"),
    (0x30F4A,"31c1f376","runtime_confirmed"), (0x30976,"6b00002a","runtime_confirmed"),
    (0x3099C,"6100060c","runtime_confirmed"), (0x30FAA,"61000164","runtime_confirmed"),
    (0x31116,"41fa00e4","runtime_confirmed"), (0x3111C,"3038efd2","runtime_confirmed"),
    (0x31120,"ed48","runtime_confirmed"), (0x31122,"d0c0","runtime_confirmed"),
    (0x31124,"3038f376","runtime_confirmed"), (0x31128,"e548","runtime_confirmed"),
    (0x31136,"b2700000","runtime_confirmed"), (0x3113A,"6500000e","runtime_confirmed"),
    (0x3113E,"5842","runtime_confirmed"), (0x31140,"b2700002","runtime_confirmed"),
    (0x31144,"65000004","runtime_confirmed"), (0x31148,"5842","runtime_reachable"),
    (0x31150,"45fa016a","runtime_confirmed"), (0x31162,"b0722000","runtime_confirmed"),
    (0x31166,"6500000e","runtime_confirmed"), (0x3116A,"5241","runtime_confirmed"),
    (0x3116C,"b0722002","runtime_confirmed"), (0x31170,"65000004","runtime_confirmed"),
    (0x31176,"31c1f726","runtime_confirmed"),
    (0x32500,"41f9000311fc","runtime_confirmed"), (0x3250A,"e548","runtime_confirmed"),
    (0x3250C,"32300000","runtime_confirmed"),
    (0x3076E,"31f900ff7024efd2","heuristic"), (0x2AD9A,"3c3c0002","heuristic"),
    (0x2AD9E,"4eba027a","heuristic"), (0x2ADA4,"33c500ff7024","heuristic"),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE or sha(rom)!=ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    for start,end,expected in CONSUMERS:
        if sha(rom[start:end])!=expected: raise ValueError("pinned original consumer/source bytes differ")


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256), owner_bytes_added=0,
        natural_domains_added=0,complete_domains_added=0,
        physical_scope=[dict(start=s,end=s+60,bytes=60,pairs=15) for s in PRIMARY_STARTS]
            +[dict(start=SECONDARY_BASE,end=SECONDARY_BASE+12,bytes=12,pairs=3)],
        preserved_raw_gaps=[dict(start=s,end=s+4,bytes=4,original_hex="00000000",confidence="unknown",
            emitted=False,padding_claim=False) for s in GAPS],
        evidence=dict(source="canonical original consumer/source bytes + old enhanced ledger",
            enhanced_source=dict(path=ENHANCED_PATH,sha256=ENHANCED_SHA256),
            frozen_raw_layout=dict(id=LAYOUT_ID,path=LAYOUT_PATH,sha256=LAYOUT_SHA256,line=113,
                bank=3,offset=0x11FC,length=204,typed_bytes_this_package=192,unemitted_bytes=12,old_typed_overlap_bytes=0),
            consumers=[dict(start=s,end=e,bytes=e-s,sha256=h) for s,e,h in CONSUMERS],
            instructions=[dict(address=a,bytes=b,original_confidence=q) for a,b,q in INSTRUCTIONS],
            constructed_F376_path=dict(copy_LEA=0x30EB8,PC_base=0x30EBA,source=0x30ED8,
                counted_copy_BYTES=16,original_hex="000102030405060708090a0b0c0d0eff",
                shuffle="only exchanges nonnegative BYTE entries; original 00..0E remain, FF remains negative",
                BYTE_read=0x30F32,EXT_WORD=0x30F36,RAM_WORD_write=0x30F4A,negative_guard=0x30976,
                call_path=[0x3099C,0x30FAA,0x31110],constructed_nonnegative_indices=list(range(15)),
                zero_index14_is_read=True,all_F376_writers_exhausted=False,natural_CPU_domain="unknown"),
            group_source=dict(WORD_copy=0x3076E,source_RAM=0xFF7024,destination_RAM=0xFFEFD2,
                setting_max_load=0x2AD9A,setting_helper=0x2B01A,setting_WORD_write=0x2ADA4,
                constructed_setting_values=[0,1,2],all_group_writers_exhausted=False),
            primary_reader=dict(entry=0x31110,LEA=0x31116,PC_base=0x31118,displacement_WORD=0x00E4,
                base=PRIMARY_BASE,group_WORD_shift=6,group_signed_ADDA=0x31122,selector_WORD_shift=2,
                first_WORD_read=0x31136,second_WORD_read=0x31140,second_displacement=2,
                compare="unsigned BCS; first fail adds4, second fail adds4",secondary_offsets=[0,4,8],
                RNG_WORD_source=0xFFF61C,scaled_WORD="floor(unsigned RNG WORD * 16 / 65536)",
                selector_arithmetic="wrap each WORD shift, sign-extend each index before addressing; displacement added after sign"),
            secondary_reader=dict(LEA=0x31150,PC_base=0x31152,displacement_WORD=0x016A,base=SECONDARY_BASE,
                first_WORD_read=0x31162,second_WORD_read=0x3116C,compare="unsigned BCS; ordered outcomes0/1/2",
                second_displacement=2,scaled_WORD="floor(unsigned RNG WORD * 8 / 65536)",destination_RAM=0xFFF726),
            first_WORD_alias=dict(LEA=0x32500,read=0x3250C,base=PRIMARY_BASE,selector_WORD_shift=2,
                literal_source_shared=True,additional_emit=False),
            catalog_is_CPU_clamp=False,full_RAM_RNG_algorithm=False),
        business_meanings="unknown",edited_gameplay_safety="unknown",independent_CPU_comparison=False)


def group_fixed(index):
    start=PRIMARY_STARTS[index]
    return dict(group_index=index,start=start,end=start+60,pair_count=15,WORD_order="big")


def pair_fixed(start,index):
    return dict(pair_index=index,start=start+4*index,end=start+4*index+4)


def secondary_fixed():
    return dict(start=SECONDARY_BASE,end=SECONDARY_BASE+12,pair_count=3,WORD_order="big")


def extract(rom):
    verify_rom(rom)
    def pairs(start,count):
        return [dict(**pair_fixed(start,i),WORDs=[int.from_bytes(rom[p:p+2],"big")
            for p in (start+4*i,start+4*i+2)]) for i in range(count)]
    fields=metadata()
    fields["primary_groups"]=[dict(**group_fixed(i),pairs=pairs(s,15)) for i,s in enumerate(PRIMARY_STARTS)]
    fields["secondary"]=dict(**secondary_fixed(),pairs=pairs(SECONDARY_BASE,3))
    return fields


def pinned(value,fixed,mutable,label):
    keys(value,set(fixed)|set(mutable),label)
    for key,expected in fixed.items(): same(value[key],expected,label+"."+key)


def blocks(rom,fields):
    verify_rom(rom)
    pinned(fields,metadata(),{"primary_groups","secondary"},"threshold pair package")
    result=[]
    groups=exact_list(fields["primary_groups"],3,"primary groups")
    for index,source in enumerate(groups+[fields["secondary"]]):
        fixed=group_fixed(index) if index<3 else secondary_fixed()
        pinned(source,fixed,{"pairs"},"pair source")
        raw=bytearray()
        for i,pair in enumerate(exact_list(source["pairs"],fixed["pair_count"],"fixed pairs")):
            pinned(pair,pair_fixed(fixed["start"],i),{"WORDs"},"complete WORD pair")
            for word in exact_list(pair["WORDs"],2,"pair WORD count"):
                raw.extend(uint(word,65535,"complete literal threshold WORD").to_bytes(2,"big"))
        if len(raw)!=fixed["end"]-fixed["start"]: raise ValueError("fixed pair byte cost differs")
        result.append(dict(id=f"rom_{fixed['start']:06X}_threshold_pairs",start=fixed["start"],end=fixed["end"],
            data=bytes(raw),role="primary_WORD_threshold_pairs" if index<3 else "secondary_WORD_threshold_pairs"))
    if sum(len(r["data"]) for r in result)!=EDITABLE_BYTES or any(a["end"]>b["start"] for a,b in zip(result,result[1:])):
        raise ValueError("exact 192-byte nonoverlapping emit scope differs")
    return result


def rebuild(rom,fields):
    encoded=blocks(rom,fields)
    image=bytearray(rom)
    for row in encoded: image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def signed_WORD(word):
    return word-65536 if word&0x8000 else word


def image_pair(image,start):
    if type(image) is not bytes or len(image)!=ROM_SIZE: raise ValueError("diagnostic requires complete bytes image")
    if not 0<=start<=ROM_SIZE-4: raise ValueError("pair read outside complete image")
    return dict(start=start,end=start+4,addresses=[start,start+2],
        WORDs=[int.from_bytes(image[p:p+2],"big") for p in (start,start+2)])


def lookup_primary(image,group_WORD,selector_WORD):
    """Full original WORD arithmetic, not a physical catalog or CPU clamp."""
    group=uint(group_WORD,65535,"complete group WORD")
    selector=uint(selector_WORD,65535,"complete selector WORD")
    group_offset=(group<<6)&65535
    selector_offset=(selector<<2)&65535
    start=PRIMARY_BASE+signed_WORD(group_offset)+signed_WORD(selector_offset)
    return dict(**image_pair(image,start),group_shifted_WORD=group_offset,selector_shifted_WORD=selector_offset,
        inside_edit_scope=any(s<=start and start+4<=s+60 for s in PRIMARY_STARTS))


def lookup_secondary(image,D2_WORD):
    """Original signed D2.W addressing, including values beyond 0/4/8."""
    offset=uint(D2_WORD,65535,"complete secondary offset WORD")
    start=SECONDARY_BASE+signed_WORD(offset)
    return dict(**image_pair(image,start),offset_WORD=offset,inside_edit_scope=SECONDARY_BASE<=start and start+4<=SECONDARY_BASE+12)


def lookup_first_WORD_alias(image,selector_WORD):
    view=lookup_primary(image,0,selector_WORD)
    return dict(address=view["start"],WORD=view["WORDs"][0],inside_edit_scope=view["inside_edit_scope"])


def threshold_choice(scaled_WORD,WORDs):
    """Narrow ordered unsigned BCS outcomes only; no independent RNG model."""
    value=uint(scaled_WORD,65535,"unsigned scaled WORD")
    first,second=[uint(w,65535,"unsigned threshold WORD") for w in exact_list(WORDs,2,"pair WORD count")]
    return 0 if value<first else (1 if value<second else 2)


def schema():
    def obj(properties): return dict(type="object",properties=properties,required=list(properties),additionalProperties=False)
    def exact(items): return dict(type="array",prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def fixed(value):
        if type(value) is dict: return obj({k:fixed(v) for k,v in value.items()})
        if type(value) is list: return exact([fixed(v) for v in value])
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    def pair(start,index):
        return obj({**{k:fixed(v) for k,v in pair_fixed(start,index).items()},
            "WORDs":dict(type="array",minItems=2,maxItems=2,items=dict(type="integer",minimum=0,maximum=65535))})
    def group(desc):
        return obj({**{k:fixed(v) for k,v in desc.items()},"pairs":exact([pair(desc["start"],i) for i in range(desc["pair_count"])])})
    result=obj({**{k:fixed(v) for k,v in metadata().items()},
        "primary_groups":exact([group(group_fixed(i)) for i in range(3)]),"secondary":group(secondary_fixed())})
    result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="192 original literal WORD fields; 15-pair physical catalogs do not clamp CPU inputs. Three 4B raw gaps preserved; no ordering normalization."
    return result


def render_bundle(rom):
    fields=extract(rom)
    serialized=dump(fields)
    image=rebuild(rom,load_fields(serialized))
    if image!=rom: raise ValueError("serialized whole-ROM roundtrip differs")
    encoded=blocks(rom,fields)
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=4,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),preview_is_editing_authority=False,
        index14_source_WORDs=[lookup_primary(rom,i,14)["WORDs"] for i in range(3)],
        index15_unemitted_views=[lookup_primary(rom,i,15) for i in range(3)],
        negative_selector_code_alias=lookup_primary(rom,0,65535),
        blocks=[{k:v for k,v in row.items() if k!="data"}|dict(bytes=len(row["data"]),sha256=sha(row["data"])) for row in encoded])
    members={"fields.json":serialized,"fields.schema.json":dump(schema()),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=4,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError("output must stay in ai_threshold_pair_fields build scope or exact formal bundle")
    if path.exists() or not path.parent.is_dir(): raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM))
    parser.add_argument("--fields")
    parser.add_argument("--bundle")
    parser.add_argument("--output")
    args=parser.parse_args(argv)
    target=None
    if args.command=="export":
        if args.output is None or args.fields is not None or args.bundle is not None: raise ValueError("export requires fresh output only")
        target=fresh_output(args.output,bundle=True)
    elif args.command=="import":
        if args.output is None or args.bundle is not None: raise ValueError("import requires fields and fresh output")
        target=fresh_output(args.output)
        if target.suffix.lower()!=".bin": raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=="export":
        members=render_bundle(rom)
        target.mkdir()
        for name,data in members.items(): put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={name:sha(data) for name,data in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS: raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data: raise ValueError("canonical bundle drift: "+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON))
        image=rebuild(rom,fields)
        if target is not None: put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=EDITABLE_BYTES,
            bytes=len(image),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__=="__main__": raise SystemExit(main())
