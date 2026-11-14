"""1644 BYTE aliases read by the original F39A.W indexed increment source.

Conditional source consumption does not recover the original fragment's
business/code meaning or prove natural F39A input and safe arithmetic.
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
OUTPUT_ROOT = ROOT / "build/increment_selector_source_alias_fields"
FORMAL_ROOT = ROOT / "analysis/increment_selector_source_alias_fields/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-increment-selector-conditional-source-BYTE-aliases-v1"
EDITABLE_BYTES = 1644
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json","fields.schema.json","validation.json","manifest.json"))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
BANK_SHA256 = reference_value(__name__, 'BANK_SHA256')
SPANS = (
    (0x2021C,0x2025A),
    (0x20522,0x20524),
    (0x206B2,0x206B8),
    (0x2197C,0x219AA),
    (0x22456,0x22470),
    (0x235B6,0x235CC),
    (0x246EE,0x24806),
    (0x24AEA,0x24AF0),
    (0x24C14,0x24C20),
    (0x24C34,0x24C40),
    (0x24C54,0x24C60),
    (0x24C74,0x24C80),
    (0x24C94,0x24CA0),
    (0x24CB4,0x24CC0),
    (0x24CD4,0x24CE0),
    (0x24CF4,0x24D00),
    (0x24D14,0x24D20),
    (0x24D34,0x24D40),
    (0x24D54,0x24D60),
    (0x24D74,0x24D80),
    (0x24D94,0x24DA0),
    (0x24DB4,0x24DC0),
    (0x24DD4,0x24DE0),
    (0x24DF4,0x24E00),
    (0x24E14,0x24E20),
    (0x24E34,0x24E40),
    (0x24E54,0x24E60),
    (0x24E74,0x24E80),
    (0x24E94,0x24EA0),
    (0x24EB4,0x24EC0),
    (0x24ED4,0x24EE0),
    (0x24EF4,0x24F00),
    (0x24F14,0x24F20),
    (0x24F34,0x24F40),
    (0x24F54,0x24F60),
    (0x24F74,0x24F80),
    (0x24F94,0x24FA0),
    (0x24FB4,0x24FC0),
    (0x24FD4,0x24FE0),
    (0x24FF4,0x25000),
    (0x25014,0x25020),
    (0x25034,0x25040),
    (0x25054,0x25060),
    (0x25074,0x25080),
    (0x25094,0x250A0),
    (0x250B4,0x250C0),
    (0x250D4,0x250E0),
    (0x250F4,0x25100),
    (0x25114,0x25120),
    (0x25134,0x25140),
    (0x25154,0x25160),
    (0x25174,0x25180),
    (0x25194,0x251A0),
    (0x251B4,0x251C0),
    (0x251D4,0x251E0),
    (0x251F4,0x25200),
    (0x25480,0x2548C),
    (0x254A0,0x254AC),
    (0x254C0,0x254CC),
    (0x254E0,0x254EC),
    (0x25500,0x2550C),
    (0x25520,0x2552C),
    (0x25540,0x2554C),
    (0x25560,0x2556C),
    (0x25580,0x2558C),
    (0x255A0,0x255AC),
    (0x255C0,0x255CC),
    (0x255E0,0x255EC),
    (0x25600,0x2560C),
    (0x25620,0x2562C),
    (0x25640,0x2564C),
    (0x25660,0x2566C),
    (0x25680,0x2568C),
    (0x256A0,0x256AC),
    (0x256C0,0x256CC),
    (0x256E0,0x256EC),
    (0x25700,0x2570C),
    (0x25720,0x2572C),
    (0x25740,0x2574C),
    (0x25760,0x2576C),
    (0x25780,0x2578C),
    (0x257A0,0x257AC),
    (0x257C0,0x257CC),
    (0x257E0,0x257EC),
    (0x25800,0x2580C),
    (0x25820,0x2582C),
    (0x25840,0x2584C),
    (0x25860,0x2586C),
    (0x25880,0x2588C),
    (0x258A0,0x258AC),
    (0x258C0,0x258CC),
    (0x258E0,0x258EC),
    (0x25900,0x2590C),
    (0x25920,0x2592C),
    (0x25940,0x2594C),
    (0x25960,0x2596C),
    (0x25980,0x2598C),
    (0x259A0,0x259AC),
    (0x259C0,0x259CC),
    (0x259E0,0x259EC),
    (0x25A00,0x25A0C),
    (0x25A20,0x25A2C),
    (0x25A40,0x25A4C),
    (0x25A60,0x25A6C),
    (0x26C4C,0x26C58),
    (0x27660,0x27666),
    (0x2767C,0x27682),
    (0x27A7E,0x27A84),
    (0x2800E,0x28012),
    (0x288BA,0x288BE),
    (0x28A9A,0x28A9E),
)
sha, dump, load_fields = shared.sha, shared.dump, shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def metadata():
    return dict(format=FORMAT,canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        source_confidence="confirmed_conditional_original_LONG_reads",confidence="candidate",
        executable_code_added=0,recovered_functions_added=0,owner_bytes_added=0,
        natural_domains_added=0,complete_domains_added=0,
        original_business_and_code_purpose="unknown",natural_input_domains="unknown",
        evidence=dict(frozen87_layout=LAYOUT_ID,bank2_sha256=BANK_SHA256,
            original_prefix=dict(start=0x20B68,end=0x20BC2,
                sha256=reference_value(__name__, 'metadata')),
            original_read=dict(selector_RAM=0xFFF39A,selector_WORD_read=0x20B8A,
                shift_WORD_PC=0x20B8E,read_LONG_PC=0x20B90,subtract_read_LONG_PC=0x20BAC,
                source_base=0x20BC2,index="s16(u16(F39A_WORD<<2))",
                complete_source_union=[0x18BC2,0x28BC2],physical_bank2_emit_only=True),
            constructed_prefix=dict(F602_BYTE=1,F608_before_WORD=1,
                masked_input_nonzero=True,timer_SUBQ_WORD_becomes_zero=True,
                input_bit1_clear_selects_add=True,selector_not_clamped_by_this_prefix=True),
            ALU_and_following_cmp_update_not_executed=True),
        supplied_values_not_natural_writer_proof=True,oldtyped_neighbors_emitted_again=False,
        CPU_hardware_RAM_CCR_stack="not executed",independent_CPU_comparison=False)


def verify_rom(rom):
    readers.verify_rom(rom)


def witness(address):
    shared.uint(address,ROM_SIZE-1,"physical alias BYTE address")
    if not any(a<=address<z for a,z in SPANS):
        raise ValueError("only allocated increment source BYTE aliases have witnesses")
    offset=((address-0x20BC2)//4)*4
    start=0x20BC2+offset
    return dict(reader="increment_F39A",selector_WORD=(offset&65535)>>2,
        original_read_PC=0x20B90,source_start=start,window_BYTES=4,byte_index=address-start)


def source_view(image,proof):
    """Read original full LONG, not ADD.L or its following state update."""
    return [readers.increment_source_view(image,0,proof["selector_WORD"])]


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
        raise ValueError("1644 disjoint physical BYTE scope differs")
    return rows


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):
        image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def raw_guard(bank_source):
    """Pure exact raw intersection against the frozen87 bank2 source."""
    if type(bank_source)is not bytes or sha(bank_source)!=BANK_SHA256:
        raise ValueError("frozen87 bank2 native SHA differs")
    raw=set()
    for a,n in re.findall(rb'\.incbin "segments/bank02\.bin", 0x([0-9A-F]+), 0x([0-9A-F]+)',bank_source):
        start=0x20000+int(a,16)
        raw.update(p for p in range(start,start+int(n,16)) if 0x18BC2<=p<0x28BC2)
    expected={p for a,z in SPANS for p in range(a,z)}
    if raw!=expected or len(raw)!=EDITABLE_BYTES:
        raise ValueError("exact sole original increment source raw intersection differs")
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
            if len(events)!=1:
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
        limitations=["1644 bytes are conditional source aliases, not mnemonic recovery or primary-purpose completion.",
            "Constructed supplied inputs do not prove natural F39A writers or safe increment arithmetic.",
            "Old typed neighbors of the original LONG window are read live but not emitted.",
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
