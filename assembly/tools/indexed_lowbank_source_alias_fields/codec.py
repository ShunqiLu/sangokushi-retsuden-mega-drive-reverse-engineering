"""1170 physical BYTE aliases witnessed by two original indexed source readers.

This is conditional physical consumption, not a newly identified function,
natural selector domain or classification of the original fragment's purpose.
"""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
import json
import re
from pathlib import Path
from tools.battle_deployment_parameters import codec as shared
from tools.indexed_scalar_source_fields import codec as readers

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE, ROM_SHA256 = readers.ROM_SIZE, readers.ROM_SHA256
DEFAULT_ROM = readers.DEFAULT_ROM
OUTPUT_ROOT = ROOT / "build/indexed_lowbank_source_alias_fields"
FORMAL_ROOT = ROOT / "analysis/indexed_lowbank_source_alias_fields/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-indexed-lowbank-conditional-source-BYTE-aliases-v1"
EDITABLE_BYTES = 1170
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json","fields.schema.json","validation.json","manifest.json"))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
BANK_SHA256 = reference_value(__name__, 'BANK_SHA256')
SPANS = (
    (0x1550,0x1566),
    (0x1CDA,0x1CEA),
    (0x204A,0x2050),
    (0x2264,0x2268),
    (0x24D4,0x24DC),
    (0x395A,0x3966),
    (0x39B0,0x3A00),
    (0x3C66,0x3CA6),
    (0x3D24,0x3E48),
    (0x416E,0x4178),
    (0x487C,0x4890),
    (0x4A52,0x4A54),
    (0x50BE,0x50C6),
    (0x514A,0x5164),
    (0x584A,0x5864),
    (0x58DE,0x58E4),
    (0x59C0,0x59D8),
    (0x5AE6,0x5AEE),
    (0x69B7,0x69B8),
    (0x69D8,0x69DA),
    (0x69ED,0x69F2),
    (0x6A07,0x6A0A),
    (0x6B94,0x6B98),
    (0x6BF8,0x6BF9),
    (0x6CC8,0x6CD6),
    (0x6E9A,0x6EB7),
    (0x6FB5,0x6FC9),
    (0x70AE,0x70DE),
    (0x7234,0x7238),
    (0x7414,0x7418),
    (0x7556,0x755A),
    (0x76F7,0x76FF),
    (0x7D34,0x7D4D),
    (0x8089,0x808A),
    (0x80D0,0x80F4),
    (0xA81E,0xA82E),
    (0xAAAC,0xAAB4),
    (0xB40C,0xB414),
    (0xB6E2,0xB724),
    (0xBBD4,0xBBDA),
    (0xBBF6,0xBC00),
    (0xBC1C,0xBC24),
    (0xBD66,0xBD76),
    (0xDA7E,0xDA8E),
    (0xDB10,0xDB20),
    (0xE024,0xE050),
    (0xE78F,0xE790),
    (0xEC5C,0xEC62),
    (0xEE0C,0xEE16),
    (0xFA1A,0xFA3A),
    (0xFA6A,0xFA8A),
    (0xFAC0,0xFAE0),
)
sha, dump, load_fields = shared.sha, shared.dump, shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        source_confidence="confirmed_conditional_original_reads", confidence="candidate",
        executable_code_added=0, recovered_functions_added=0, owner_bytes_added=0,
        natural_domains_added=0, complete_domains_added=0,
        original_business_and_code_purpose="unknown", natural_input_domains="unknown",
        evidence=dict(frozen87_layout=LAYOUT_ID,bank0_sha256=BANK_SHA256,
            pattern=dict(prefix_start=0x68A,prefix_end=0x696,read_PC=0x690,
                source_base=0x696,index="s16(u16(already_fetched_F6C4_WORD<<2))",
                complete_in_ROM_window_union=[2,0x8696],new_raw_BYTES=843),
            curve=dict(prefix_start=0x949E,prefix_end=0x94CA,read_PC=0x94BE,
                captured_index_before_memory_SUBQ2=True, timer_WORD_supplied=0,
                original_timer_BPL_stop=True, original_index_BMI_stop=True,
                constructed_positive_even_index_WORDs=True, reads_per_window=11,
                source_base=0x94CA,complete_window_union=[0x94CA,0x114DE],new_lowbank_raw_BYTES=327,
                physical_bank0_emit_only=True, following_oldtyped_sources_not_emitted=True)),
        supplied_values_not_natural_writer_proof=True, oldtyped_neighbors_emitted_again=False,
        CPU_hardware_RAM_CCR_stack="not executed", independent_CPU_comparison=False)


def verify_rom(rom):
    readers.verify_rom(rom)


def witness(address):
    shared.uint(address,ROM_SIZE-1,"physical alias BYTE address")
    if not any(a <= address < z for a,z in SPANS):
        raise ValueError("only new lowbank physical aliases have witnesses")
    if address < 0x8696:
        offset = ((address-0x696)//4)*4
        start = 0x696+offset
        return dict(reader="pattern",selector_WORD=(offset&65535)>>2,
            original_read_PC=0x690,source_start=start,window_BYTES=4,byte_index=address-start)
    captured = (address-0x94CA)&~1
    return dict(reader="curve",selector_WORD=captured,timer_WORD=0,
        original_read_PC=0x94BE,source_start=0x94CA+captured,window_BYTES=22,
        byte_index=address-(0x94CA+captured))


def source_view(image,proof):
    """Read original source prefix through an explicit supplied selector."""
    if proof["reader"] == "pattern":
        return [readers.pattern_source_view(image,proof["selector_WORD"])]
    return readers.curve_source_view(image,proof["selector_WORD"],proof["timer_WORD"])["reads"]


def group_fixed(index):
    a,z=SPANS[index]
    return dict(id=f"rom_{a:06X}_{z:06X}_conditional_source_BYTEs",start=a,end=z,bytes=z-a,
        original_fragment_business_role="unknown",one_physical_edit_authority=True)


def pinned(value,fixed,mutable,label):
    shared.keys(value,set(fixed)|set(mutable),label)
    for key,item in fixed.items():
        shared.same(value[key],item,label+"."+key)


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),sources=[dict(**group_fixed(i),BYTEs=list(rom[a:z]))
        for i,(a,z) in enumerate(SPANS)])


def blocks(rom,fields):
    verify_rom(rom)
    pinned(fields,metadata(),{"sources"},"conditional source package")
    rows=[]
    for i,row in enumerate(shared.exact_list(fields["sources"],len(SPANS),"fixed allocations")):
        fixed=group_fixed(i)
        pinned(row,fixed,{"BYTEs"},"physical source fragment")
        data=bytes(shared.uint(v,255,"full source BYTE") for v in
            shared.exact_list(row["BYTEs"],fixed["bytes"],"fixed BYTE count"))
        rows.append(dict(id=fixed["id"],start=fixed["start"],end=fixed["end"],data=data,
            role="conditional_original_indexed_source_BYTE_alias_unknown_primary_purpose"))
    if sum(len(r["data"]) for r in rows)!=EDITABLE_BYTES or any(a["end"]>b["start"] for a,b in zip(rows,rows[1:])):
        raise ValueError("1170 disjoint physical BYTE scope differs")
    return rows


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):
        image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def raw_guard(bank_source):
    """Pure exact allocation check against frozen87 bank0 text."""
    if type(bank_source)is not bytes or sha(bank_source)!=BANK_SHA256:
        raise ValueError("frozen87 bank0 native SHA differs")
    raw=set()
    for a,n in re.findall(rb'\.incbin "segments/bank00\.bin", 0x([0-9A-F]+), 0x([0-9A-F]+)',bank_source):
        start=int(a,16)
        raw.update(range(start,start+int(n,16)))
    expected={p for a,z in SPANS for p in range(a,z)}
    if raw!=expected or len(raw)!=EDITABLE_BYTES:
        raise ValueError("exact sole bank0 raw authority differs")
    return dict(verified=True,editable_bytes=EDITABLE_BYTES,physical_spans=len(SPANS))


def schema():
    def walk(value):
        if type(value)is dict:
            props={k:walk(v) for k,v in value.items()}
            return dict(type="object",properties=props,required=list(props),additionalProperties=False)
        if type(value)is list:
            return dict(type="array",prefixItems=[walk(v) for v in value],items=False,
                minItems=len(value),maxItems=len(value))
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    result=walk(dict(**metadata(),sources=[dict(**group_fixed(i),BYTEs=[]) for i in range(len(SPANS))]))
    for i,(a,z) in enumerate(SPANS):
        result["properties"]["sources"]["prefixItems"][i]["properties"]["BYTEs"]=dict(
            type="array",items=dict(type="integer",minimum=0,maximum=255),minItems=z-a,maxItems=z-a)
    result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    return result


def audit_witnesses(image):
    readers.image_bytes(image)
    proofs=[]
    for a,z in SPANS:
        for address in range(a,z):
            proof=witness(address)
            events=source_view(image,proof)
            if len(events)!=(1 if proof["reader"]=="pattern" else 11):
                raise ValueError("original complete source window count differs")
            if any(e["status"]!="source_read" for e in events):
                raise ValueError("witness source reaches a boundary")
            payload=b"".join(e["value"].to_bytes(e["width_BYTES"],"big") for e in events)
            if payload[proof["byte_index"]]!=image[address] or events[0]["address"]+proof["byte_index"]!=address:
                raise ValueError("original input witness position/BYTE differs")
            proofs.append(dict(address=address,source_BYTE=image[address],**proof))
    if len(proofs)!=EDITABLE_BYTES:
        raise ValueError("missing perBYTE witness")
    return proofs


def render_bundle(rom):
    fields=extract(rom)
    image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:
        raise ValueError("serialized whole-ROM roundtrip differs")
    proofs=audit_witnesses(image)
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=len(SPANS),
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),per_BYTE_witnesses=proofs,
        limitations=["1170 bytes are conditional source aliases, not mnemonic recovery or primary-purpose completion.",
            "Constructed supplied inputs do not prove natural F6C4/F618/F61A writers or safe gameplay.",
            "Old source bytes and 11-WORD window tails above bank0 are read live but not emitted.",
            "Following VDP/RAM writes, DIVU, callbacks, flags, stack and original routines are not executed."])
    members={"fields.json":dump(fields),"fields.schema.json":dump(schema()),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,
        members={n:dict(bytes=len(b),sha256=sha(b)) for n,b in members.items()}))
    return members


def fresh_output(value,formal=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not(formal and path==FORMAL_ROOT):
        raise ValueError("dedicated build output or exact formal export required")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh target with existing parent required")
    return path


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=("export","import","verify"))
    p.add_argument("--rom",default=str(DEFAULT_ROM))
    p.add_argument("--fields")
    p.add_argument("--bundle")
    p.add_argument("--output")
    args=p.parse_args(argv)
    target=None
    if args.command=="export":
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError("export requires fresh output only")
        target=fresh_output(args.output,formal=True)
    elif args.command=="import":
        if args.output is None or args.bundle is not None:
            raise ValueError("import requires fresh .bin")
        target=fresh_output(args.output)
        if target.suffix.lower()!=".bin":
            raise ValueError("fresh .bin required")
    elif args.output is not None or(args.fields is not None and args.bundle is not None):
        raise ValueError("verify is read-only")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=="export":
        members=render_bundle(rom)
        target.mkdir()
        for name,data in members.items():
            put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={n:sha(b) for n,b in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data:
                raise ValueError("canonical member drift:"+name)
        result=dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,sha256=ROM_SHA256)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:
            put(target,image)
        result=dict(exact_canonical=image==rom,editable_bytes=EDITABLE_BYTES,sha256=sha(image))
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
