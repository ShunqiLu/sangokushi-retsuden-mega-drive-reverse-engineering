"""172 typed source bytes with distinct battle, motion and panel roles.

Physical source groups are editing units, not CPU index limits. Read views use
the complete edited image and original WORD wrap/sign-extension arithmetic.
They do not execute RAM writers, random numbers, rendering or indirect calls.
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
OUTPUT_ROOT = ROOT / "build/runtime_indexed_source_fields"
FORMAL_ROOT = ROOT / "analysis/runtime_indexed_source_fields/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
MAX_JSON = 1024 * 1024
EDITABLE_BYTES = 172
MEMBERS = frozenset(("fields.json", "validation.json", "manifest.json"))
sha, dump = shared.sha, shared.dump
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
BODIES = (
    (0x28CAA, 0x28D32, reference_value(__name__, 'BODIES')),
    (0x3A1E0, 0x3A2DC, reference_value(__name__, 'BODIES_2')),
    (0x3569A, 0x35710, reference_value(__name__, 'BODIES_3')),
)
SOURCE_HASHES = (
    (0x28D32, 0x28D62, reference_value(__name__, 'SOURCE_HASHES')),
    (0x28D6E, 0x28D74, reference_value(__name__, 'SOURCE_HASHES_2')),
    (0x3A2DC, 0x3A322, reference_value(__name__, 'SOURCE_HASHES_3')),
    (0x35710, 0x35740, reference_value(__name__, 'SOURCE_HASHES_4')),
)
# Each descriptor has one physical authority. Pointer fields retain all32 bits.
GROUPS = (
    ("skill_threshold_WORDs", 0x28D32, 2, 6, 0x28F96),
    ("skill_bonus_WORDs", 0x28D3E, 2, 6, 0x28CCA),
    ("mode0_equipment_WORDs", 0x28D4A, 2, 4, 0x28CE2),
    ("mode1_equipment_WORDs", 0x28D52, 2, 4, 0x28CF8),
    ("other_mode_equipment_WORDs", 0x28D5A, 2, 4, 0x28D06),
    ("class_divisor_WORDs", 0x28D6E, 2, 3, 0x28D16),
    ("scene_X_motion_WORDs", 0x3A2DC, 2, 20, 0x3A1F0),
    ("scene_palette_source_LONGs", 0x3A306, 4, 7, 0x3A2A8),
    ("panel_primary_source_LONGs", 0x35710, 4, 6, 0x356A0),
    ("panel_secondary_source_LONGs", 0x35728, 4, 6, 0x35706),
)
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')


def metadata():
    return dict(format="g5510-runtime-indexed-distinct-source-fields-v1",
        confidence="candidate", source_format_confidence="confirmed",
        canonical_source=dict(bytes=ROM_SIZE, sha256=ROM_SHA256),
        physical_BYTES=172, battle_parameter_BYTES=54, scene_source_BYTES=70, panel_pointer_BYTES=48,
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        evidence=dict(consumers=[dict(start=s, end=e, sha256=h) for s,e,h in BODIES],
            counter_helper=dict(start=0x28F90, end=0x28F9C, bytes_hex="323cfffe5441b05a64fa4e75",
                                initial_index_WORD=0xFFFE, increment_WORD=2, comparison="unsigned BCC"),
            accepted_raw_snapshot=dict(layout=LAYOUT_ID, raw_BYTES=48259, admitted_raw_BYTES=172),
            excluded_unknown_range=dict(start=0x28D62, end=0x28D6E, bytes=12),
            scene_motion=dict(counter_RAM=0xFF703C, first_WORD_read=0x3A1F0,
                counter_add=0x3A1F6, second_counter_add=0x3A22A, marker_read=0x3A23E,
                marker_compare=0x3A240, marker_reset=0x3A248, marker_address=0x3A304,
                marker_WORD=0x00FF, original_counter_BYTE_offsets=list(range(0,40,2)),
                complete_RAM_writer_domain=False),
            palette=dict(counter_RAM=0xFF7004, conditional_increment=0x3A294,
                increment_WORD=4, source_LONG_read=0x3A2A8, copy_LONG_read=0x3A2B2,
                DBRA=0x3A2B4, original_LONG_count=8, source_pointer_targets_not_reauthored=True),
            panel=dict(selector_RAM=0xFFF348, WORD_shift=2,
                source_LONG_reads=[0x356A0,0x35702,0x35706], original_calls=[0x3562C,0x35634],
                body_directory_sizes_are_not_CPU_limits=True)),
        source_views_read_only=True, natural_selection="unknown", edited_gameplay_safety="unknown",
        full_CPU_or_VDP_execution=False, independent_CPU_comparison=False)


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE or sha(rom)!=ROM_SHA256:
        raise ValueError("canonical full ROM identity required")
    for start,end,digest in (*BODIES,*SOURCE_HASHES):
        if sha(rom[start:end])!=digest: raise ValueError("pinned original source/consumer changed")
    if rom[0x28F90:0x28F9C].hex()!=metadata()["evidence"]["counter_helper"]["bytes_hex"]:
        raise ValueError("original unsigned threshold counter changed")


def descriptor(group):
    name,start,size,count,PC=group
    return dict(id=name, start=start, end=start+size*count, value_BYTE_width=size,
                physical_count=count, original_source_read_PC=PC)


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(), groups=[dict(**descriptor(g), values=[
        int.from_bytes(rom[p:p+g[2]],"big") for p in range(g[1],g[1]+g[2]*g[3],g[2])]) for g in GROUPS],
        motion_marker=dict(address=0x3A304, WORD=0x00FF, framing_fixed=True))


def blocks(rom,fields):
    verify_rom(rom)
    keys(fields,set(metadata())|{"groups","motion_marker"},"indexed source fields")
    for key,value in metadata().items(): same(fields[key],value,"metadata."+key)
    same(fields["motion_marker"],dict(address=0x3A304,WORD=0xFF,framing_fixed=True),"motion marker")
    encoded={}
    for group,row in zip(GROUPS,exact_list(fields["groups"],len(GROUPS),"distinct source groups")):
        fixed=descriptor(group);keys(row,set(fixed)|{"values"},"source group")
        for key,value in fixed.items(): same(row[key],value,"group."+key)
        size,count=group[2:4]
        encoded[group[0]]=b"".join(uint(v,(1<<(8*size))-1,"complete source value").to_bytes(size,"big")
            for v in exact_list(row["values"],count,"physical source values"))
    sources=[
        ("battle_threshold_and_equipment_words",0x28D32,0x28D62,b"".join(encoded[g[0]] for g in GROUPS[:5])),
        ("battle_class_divisor_words",0x28D6E,0x28D74,encoded[GROUPS[5][0]]),
        ("scene_motion_and_palette_sources",0x3A2DC,0x3A322,encoded[GROUPS[6][0]]+b"\x00\xff"+encoded[GROUPS[7][0]]),
        ("panel_primary_and_secondary_sources",0x35710,0x35740,encoded[GROUPS[8][0]]+encoded[GROUPS[9][0]]),
    ]
    if sum(len(data) for _,_,_,data in sources)!=172: raise ValueError("source BYTE cost differs")
    return [dict(id=name,start=s,end=e,data=data,role="confirmed_distinct_indexed_source_fields")
            for name,s,e,data in sources]


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields): image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def s16(value):
    value&=0xFFFF
    return value-0x10000 if value&0x8000 else value


def read_source(image,address,width,PC):
    if type(image)is not bytes or len(image)!=ROM_SIZE: raise ValueError("complete edited bytes image required")
    if address&1: raise ValueError("original WORD/LONG read would address-error at odd boundary")
    if not 0<=address<=ROM_SIZE-width: raise ValueError("source read outside this ROM image")
    return dict(source_read_PC=PC,address=address,value_BYTE_width=width,
                value=int.from_bytes(image[address:address+width],"big"))


def threshold_index_view(image,skill_WORD,read_budget=32769):
    """28F90's sequential reads and wrapping D1.W; FFFF is not a marker."""
    skill=uint(skill_WORD,0xFFFF,"skill WORD")
    uint(read_budget,32769,"explicit source-read budget")
    if not read_budget: raise ValueError("positive read budget required")
    events=[];index=0xFFFE;address=0x28D32
    for _ in range(read_budget):
        index=(index+2)&0xFFFF
        event=read_source(image,address,2,0x28F96);events.append(event);address+=2
        if skill<event["value"]: return dict(index_WORD=index,events=events)
    raise ValueError("original sequential read continues beyond explicit budget")


def battle_source_view(image,skill_WORD,mode_WORD,equipment_WORD,class_WORD):
    result=threshold_index_view(image,skill_WORD)
    index=result["index_WORD"]
    mode=uint(mode_WORD,0xFFFF,"mode WORD")
    equipment=uint(equipment_WORD,0xFFFF,"equipment WORD")
    troop_class=uint(class_WORD,0xFFFF,"class WORD")
    base,PC=(0x28D4A,0x28CE2) if mode==0 else ((0x28D52,0x28CF8) if mode==1 else (0x28D5A,0x28D06))
    result["bonus"]=read_source(image,0x28D3E+s16(index),2,0x28CCA)
    result["equipment"]=read_source(image,base+s16(equipment<<1),2,PC)
    result["divisor"]=read_source(image,0x28D6E+2*(troop_class&3),2,0x28D16)
    return result


def scene_source_view(image,motion_counter_WORD,palette_counter_WORD):
    motion=uint(motion_counter_WORD,0xFFFF,"motion counter BYTE-offset WORD")
    palette=uint(palette_counter_WORD,0xFFFF,"palette counter BYTE-offset WORD")
    return dict(X=read_source(image,0x3A2DC+s16(motion),2,0x3A1F0),
                marker_probe=read_source(image,0x3A2DC+s16(motion+4),2,0x3A23E),
                palette_pointer=read_source(image,0x3A306+s16(palette),4,0x3A2A8),
                values_at_original_reads=True, complete_state_transition=False)


def panel_source_view(image,selector_WORD):
    selector=uint(selector_WORD,0xFFFF,"panel selector WORD")
    offset=(selector<<2)&0xFFFF
    return dict(offset_WORD=offset,
        primary=read_source(image,0x35710+s16(offset),4,0x356A0),
        secondary=read_source(image,0x35728+s16(offset),4,0x35706),
        pointer_targets_followed=False)


def render_bundle(rom):
    fields=extract(rom);serialized=dump(fields)
    image=rebuild(rom,load_fields(serialized))
    if image!=rom: raise ValueError("whole ROM roundtrip differs")
    report=dict(**metadata(),editable_bytes=172,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        blocks=[{k:v for k,v in b.items() if k!="data"}|dict(bytes=len(b["data"]),sha256=sha(b["data"])) for b in blocks(rom,fields)],
        threshold_witnesses=[dict(input_WORD=value,**threshold_index_view(image,value)) for value in (0,31,61,81,101,130)],
        panel_pointer_witnesses=[dict(selector_WORD=i,**panel_source_view(image,i)) for i in range(6)],
        scene_witnesses=[scene_source_view(image,i*2,(i%7)*4) for i in range(20)])
    members={"fields.json":serialized,"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=172,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not(path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not(bundle and path==FORMAL_ROOT):
        raise ValueError("dedicated fresh indexed-source output required")
    if path.exists() or not path.parent.is_dir(): raise ValueError("fresh path with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM));parser.add_argument("--fields")
    parser.add_argument("--bundle");parser.add_argument("--output")
    args=parser.parse_args(argv);target=None
    if args.command=="export":
        if args.output is None or args.fields is not None or args.bundle is not None: raise ValueError("export requires fresh output only")
        target=fresh_output(args.output,bundle=True)
    elif args.command=="import":
        if args.output is None or args.bundle is not None: raise ValueError("import requires fields/fresh output")
        target=fresh_output(args.output)
        if target.suffix.lower()!=".bin": raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None): raise ValueError("verify accepts fields or bundle without output")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=="export":
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items(): put(target/name,data)
        result=dict(path=str(target),editable_bytes=172,members={name:sha(data) for name,data in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS: raise ValueError("exact three-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data: raise ValueError("formal bundle drift: "+name)
        result=dict(path=str(bundle),editable_bytes=172,verified=True,whole_ROM_exact=True,sha256=ROM_SHA256)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None: put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=172,exact_canonical=image==rom,bytes=len(image),sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0
