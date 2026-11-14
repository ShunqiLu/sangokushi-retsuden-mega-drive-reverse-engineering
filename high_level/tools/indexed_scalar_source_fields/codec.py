"""214 original indexed scalar/directory BYTEs with distinct reader contracts.

Physical editing allocations are not CPU clamps. Diagnostics take already
fetched values and read an edited complete image; no CPU, bus or RAM execution.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
import re
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
OUTPUT_ROOT = ROOT / "build/indexed_scalar_source_fields"
FORMAL_ROOT = ROOT / "analysis/indexed_scalar_source_fields/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-indexed-scalar-source-fields-v1"
EDITABLE_BYTES = 214
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_BANKS = {0: reference_value(__name__, 'LAYOUT_BANKS'), 2: reference_value(__name__, 'LAYOUT_BANKS_2')}
# The directory has four independent LONG-pointer/WORD-counter records.
# Other rows have exactly one full-width scalar editing representation.
SPECS = (
    ("F6C4_indexed_LONGs", 0x696, 0x6A6, 4),
    ("FB04_copy_curve_WORDs", 0x94CA, 0x9508, 2),
    ("ability_source_BYTEs", 0xB9DE, 0xB9EA, 1),
    ("counted_glyph_directory", 0xBBA0, 0xBBB8, 6),
    ("F39E_increment_LONGs", 0x20BC2, 0x20BDA, 4),
    ("F3BA_increment_LONGs", 0x20D02, 0x20D1A, 4),
    ("C700_divisor_and_quotient_adjust_WORDs", 0x21114, 0x21128, 2),
    ("F770_position_delta_WORDs", 0x249F4, 0x24A14, 2),
)
GUARDS = (
    (0x68A, 0x696, reference_value(__name__, 'GUARDS')),
    (0x949E, 0x94CA, reference_value(__name__, 'GUARDS_2')),
    (0xB982, 0xB9DE, reference_value(__name__, 'GUARDS_3')),
    (0xBB4C, 0xBBA0, reference_value(__name__, 'GUARDS_4')),
    (0x20B68, 0x20BC2, reference_value(__name__, 'GUARDS_5')),
    (0x20CA8, 0x20D02, reference_value(__name__, 'GUARDS_6')),
    (0x2106C, 0x21114, reference_value(__name__, 'GUARDS_7')),
    (0x24990, 0x249F4, reference_value(__name__, 'GUARDS_8')),
)
sha, dump = shared.sha, shared.dump
load_fields, safe_path = shared.load_fields, shared.safe_path
read_bounded, put = shared.read_bounded, shared.put


def image_bytes(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("complete immutable bytes image required")


def verify_rom(rom):
    image_bytes(rom)
    if sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM SHA required")
    for start, end, digest in GUARDS:
        if sha(rom[start:end]) != digest:
            raise ValueError("original reader bytes differ")


def metadata():
    return dict(format=FORMAT, source_confidence="confirmed", confidence="candidate",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        ownership_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        functions_added=0, independent_CPU_comparison=False,
        evidence=dict(raw_layout=LAYOUT_ID, original_readers=[
            dict(start=s, end=e, sha256=h) for s, e, h in GUARDS],
            pattern=dict(read_PC=0x690, formula="696+s16(u16(F6C4_WORD<<2))", width=4),
            curve=dict(read_PC=0x94BE, captured_F618_before_SUBQ2=True,
                F61A_SUBQ1_then_BPL_stop=True, F618_BMI_stop=True,
                DBRA_initial10_reads11_WORDs=True, destination=0xFFFB04),
            ability=dict(first_read=0xB99E, comparisons=[0xB9A6,0xB9B6],
                conditional_rereads=[0xB9AE,0xB9BE], indices="three already-fetched zero-extended BYTEs",
                unsigned_BYTE_max=True),
            glyph_directory=dict(header_BYTE_guard_upper_exclusive96=True,
                read_LONG_PC=0xBB6A, read_WORD_PC=0xBB6E, stride_BYTES=6,
                count_WORD_is_original_D3_not_count_plus_one=True, payload_not_followed=True),
            increments=dict(add_PCs=[0x20B90,0x20CD0], sub_PCs=[0x20BAC,0x20CEC],
                formula="base+s16(u16(already_fetched_selector_WORD<<2))", width=4),
            divisor_adjust=dict(divisor_PC=0x21094, divisor_index="u16((already_fetched_C700_BYTE&7)<<1)",
                adjust_PC=0x210EC, quotient_upper_bounds=[5,8,12,15], equality_stays_lower_bucket=True,
                DIVU_and_state_update_not_executed=True),
            position_delta=dict(first_PC=0x249A2, second_PC=0x249A6,
                base_includes_live_code=0x249F0, unsigned_F770_WORD_less_than9=True,
                original_slot0_OR_and_RTS_WORDs_not_emitted=True)),
        physical_catalog_not_CPU_domain=True, broader_names_and_natural_inputs="unknown",
        CPU_RAM_CCR_bus_stack_rendering="not executed")


def group_fixed(index):
    role, start, end, width = SPECS[index]
    return dict(id=f"rom_{start:06X}_{role}", role=role, start=start, end=end,
        width_BYTES=width, count=(end-start)//width)


def pinned(row, expected, mutable, label):
    shared.keys(row, set(expected)|set(mutable), label)
    for key, value in expected.items():
        shared.same(row[key], value, label+"."+key)


def extract(rom):
    verify_rom(rom)
    sources = []
    for i, (_, start, end, width) in enumerate(SPECS):
        fixed = group_fixed(i)
        if width == 6:
            rows = [dict(pointer_LONG=int.from_bytes(rom[p:p+4],"big"),
                         counter_WORD=int.from_bytes(rom[p+4:p+6],"big"))
                    for p in range(start,end,6)]
            sources.append(dict(**fixed, records=rows))
        else:
            sources.append(dict(**fixed,
                values=[int.from_bytes(rom[p:p+width],"big") for p in range(start,end,width)]))
    return dict(**metadata(), sources=sources)


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {"sources"}, "indexed scalar package")
    rows = []
    for i, source in enumerate(shared.exact_list(fields["sources"],len(SPECS),"source groups")):
        fixed = group_fixed(i)
        width = fixed["width_BYTES"]
        mutable = "records" if width == 6 else "values"
        pinned(source, fixed, {mutable}, "source")
        values = shared.exact_list(source[mutable],fixed["count"],"fixed source count")
        if width == 6:
            payload = []
            for record in values:
                shared.keys(record, {"pointer_LONG","counter_WORD"}, "glyph directory record")
                pointer = shared.uint(record["pointer_LONG"],0xFFFFFFFF,"complete source pointer LONG")
                counter = shared.uint(record["counter_WORD"],0xFFFF,"complete original D3 WORD")
                payload.append(pointer.to_bytes(4,"big")+counter.to_bytes(2,"big"))
            data = b"".join(payload)
        else:
            data = b"".join(shared.uint(value,(1<<(width*8))-1,"complete scalar").to_bytes(width,"big")
                            for value in values)
        if len(data) != fixed["end"]-fixed["start"]:
            raise ValueError("source cost differs")
        rows.append(dict(id=fixed["id"],start=fixed["start"],end=fixed["end"],data=data,
                         role="confirmed_original_indexed_scalar_or_directory_source"))
    if sum(len(row["data"]) for row in rows) != EDITABLE_BYTES:
        raise ValueError("214-BYTE physical scope differs")
    if any(a["end"] > b["start"] for a,b in zip(rows,rows[1:])):
        raise ValueError("source overlap/order")
    return rows


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom,fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def s16(word):
    return word-65536 if word&0x8000 else word


def read_source(image, address, width, pc):
    image_bytes(image)
    if width > 1 and address&1:
        return dict(status="odd_WORD_address_boundary_not_executed", address=address,
                    width_BYTES=width, PC=pc, read_addresses=[])
    if not 0 <= address <= ROM_SIZE-width:
        return dict(status="outside_ROM_boundary_not_executed", address=address,
                    width_BYTES=width, PC=pc, read_addresses=[])
    return dict(status="source_read",address=address,width_BYTES=width,PC=pc,
        value=int.from_bytes(image[address:address+width],"big"),
        read_addresses=list(range(address,address+width)))


def pattern_source_view(image, F6C4_WORD):
    word = shared.uint(F6C4_WORD,65535,"already-fetched F6C4 WORD")
    return read_source(image,0x696+s16((word<<2)&65535),4,0x690)


def curve_source_view(image, F618_WORD, F61A_WORD=0):
    image_bytes(image)
    captured = shared.uint(F618_WORD,65535,"already-fetched F618 WORD")
    timer = (shared.uint(F61A_WORD,65535,"already-fetched F61A WORD")-1)&65535
    if not timer&0x8000:
        return dict(status="original_F61A_BPL_stop",reads=[],F61A_after_WORD=timer)
    if captured&0x8000:
        return dict(status="original_F618_BMI_stop",reads=[],F61A_after_WORD=3)
    reads = []
    for offset in range(0,22,2):
        event = read_source(image,0x94CA+captured+offset,2,0x94BE)
        reads.append(event)
        if event["status"] != "source_read":
            break
    return dict(status=reads[-1]["status"],reads=reads,F61A_after_WORD=3,
                F618_after_WORD=(captured-2)&65535,captured_index_WORD=captured)


def ability_source_view(image, fetched_ability_BYTEs):
    indices = shared.exact_list(fetched_ability_BYTEs,3,"three fetched RAM ability BYTEs")
    indices = [shared.uint(value,255,"already-zero-extended BYTE") for value in indices]
    events = [read_source(image,0xB9DE+indices[0],1,0xB99E)]
    maximum = events[0]["value"]
    for index, compare_pc, reread_pc in zip(indices[1:],(0xB9A6,0xB9B6),(0xB9AE,0xB9BE)):
        compare = read_source(image,0xB9DE+index,1,compare_pc)
        events.append(compare)
        if maximum < compare["value"]:
            reread = read_source(image,0xB9DE+index,1,reread_pc)
            events.append(reread)
            maximum = reread["value"]
    return dict(reads=events,maximum_BYTE=maximum,following_ability_update_executed=False)


def glyph_directory_source_view(image, fetched_header_BYTE):
    image_bytes(image)
    selector = shared.uint(fetched_header_BYTE,255,"already fetched header BYTE")
    if selector >= 96:
        return dict(status="original_unsigned_BCC_stop",reads=[])
    base = 0xBBA0+6*selector
    return dict(status="source_read",reads=[
        read_source(image,base,4,0xBB6A),read_source(image,base+4,2,0xBB6E)],
        payload_pointer_not_followed=True)


def increment_source_view(image, table, selector_WORD, *, subtract=False):
    table = shared.uint(table,1,"original increment table")
    selector = shared.uint(selector_WORD,65535,"already fetched increment selector WORD")
    if type(subtract) is not bool:
        raise ValueError("strict subtract flag")
    base = (0x20BC2,0x20D02)[table]
    pc = ((0x20B90,0x20CD0),(0x20BAC,0x20CEC))[subtract][table]
    return read_source(image,base+s16((selector<<2)&65535),4,pc)


def divisor_source_view(image, fetched_C700_BYTE):
    value = shared.uint(fetched_C700_BYTE,255,"already fetched C700 BYTE")
    return read_source(image,0x21114+2*(value&7),2,0x21094)


def adjust_source_view(image, formed_quotient_WORD):
    value = shared.uint(formed_quotient_WORD,65535,"already formed quotient WORD")
    bucket = sum(value > upper for upper in (5,8,12,15))
    return read_source(image,0x2111E+2*bucket,2,0x210EC)


def position_delta_source_view(image, F770_WORD):
    image_bytes(image)
    value = shared.uint(F770_WORD,65535,"already fetched F770 WORD")
    if value >= 9:
        return dict(status="original_unsigned_BCC_stop",reads=[])
    address = 0x249F0+4*value
    return dict(status="source_read",reads=[
        read_source(image,address,2,0x249A2),read_source(image,address+2,2,0x249A6)])


def constructed_read_union(rom):
    events = [pattern_source_view(rom,i) for i in range(4)]
    for index in (0,20,40):
        events.extend(curve_source_view(rom,index)["reads"])
    for index in range(12):
        events.extend(ability_source_view(rom,[index]*3)["reads"])
    for index in range(4):
        events.extend(glyph_directory_source_view(rom,index)["reads"])
    events.extend(increment_source_view(rom,table,i) for table in range(2) for i in range(6))
    events.extend(divisor_source_view(rom,i) for i in range(8))
    events.extend(adjust_source_view(rom,i) for i in (0,6,9,13,16))
    for index in range(1,9):
        events.extend(position_delta_source_view(rom,index)["reads"])
    return {p for event in events for p in event["read_addresses"]}


def raw_guard(bank_sources):
    """Pure validation against separately supplied frozen 81-layout bank text."""
    shared.keys(bank_sources,set(LAYOUT_BANKS),"required old-layout banks")
    raw = set()
    for bank, digest in LAYOUT_BANKS.items():
        body = bank_sources[bank]
        if type(body) is not bytes or sha(body) != digest:
            raise ValueError("frozen old-layout bank SHA differs")
        for b, offset, count in re.findall(
            rb'\.incbin "segments/bank([0-9a-f]{2})\.bin", 0x([0-9A-F]+), 0x([0-9A-F]+)',body):
            if int(b,16) != bank:
                raise ValueError("raw bank mismatch")
            start = bank*65536+int(offset,16)
            raw.update(range(start,start+int(count,16)))
    expected = {p for _,start,end,_ in SPECS for p in range(start,end)}
    if len(expected) != EDITABLE_BYTES or not expected <= raw:
        raise ValueError("source not fully raw in accepted81")
    return dict(verified=True,editable_bytes=EDITABLE_BYTES,layout_id=LAYOUT_ID)


def schema(rom):
    def walk(value):
        if type(value) is dict:
            props = {key:walk(item) for key,item in value.items()}
            return dict(type="object",properties=props,required=list(props),additionalProperties=False)
        if type(value) is list:
            items = [walk(item) for item in value]
            return dict(type="array",prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    result = walk(extract(rom))
    for i,(_,_,_,width) in enumerate(SPECS):
        props = result["properties"]["sources"]["prefixItems"][i]["properties"]
        if width == 6:
            for item in props["records"]["prefixItems"]:
                for name, maximum in (("pointer_LONG",0xFFFFFFFF),("counter_WORD",65535)):
                    item["properties"][name] = dict(type="integer",minimum=0,maximum=maximum)
        else:
            props["values"]["prefixItems"] = [
                dict(type="integer",minimum=0,maximum=(1<<(width*8))-1)
                for _ in range(group_fixed(i)["count"])]
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return result


def render_bundle(rom):
    fields = extract(rom)
    rows = blocks(rom,fields)
    image = rebuild(rom,load_fields(dump(fields)))
    expected = {p for _,start,end,_ in SPECS for p in range(start,end)}
    if image != rom or constructed_read_union(rom) != expected:
        raise ValueError("whole-ROM roundtrip or 214-BYTE original read witness union differs")
    report = dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=len(rows),
        constructed_read_union_BYTES=len(expected),whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        blocks=[{k:v for k,v in row.items() if k!="data"}|
                dict(bytes=len(row["data"]),sha256=sha(row["data"])) for row in rows])
    members = {"fields.json":dump(fields),"fields.schema.json":dump(schema(rom)),
               "validation.json":dump(report)}
    members["manifest.json"] = dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(body),sha256=sha(body)) for name,body in members.items()}))
    return members


def fresh_output(value, formal=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (formal and path == FORMAL_ROOT):
        raise ValueError("dedicated output or exact formal path required")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM))
    parser.add_argument("--fields")
    parser.add_argument("--bundle")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    target = None
    if args.command == "export":
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError("export requires fresh output only")
        target = fresh_output(args.output,formal=True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None:
            raise ValueError("import requires fields and fresh output")
        target = fresh_output(args.output)
        if target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError("verify is read-only")
    rom = read_bounded(args.rom,ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name, body in members.items():
            put(target/name,body)
        result = dict(path=str(target),editable_bytes=EDITABLE_BYTES,
                      members={name:sha(body) for name,body in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name, body in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON) != body:
                raise ValueError("canonical generated bundle drift:"+name)
        result = dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,sha256=ROM_SHA256)
    else:
        image = rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:
            put(target,image)
        result = dict(path=None if target is None else str(target),editable_bytes=EDITABLE_BYTES,
                      exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
