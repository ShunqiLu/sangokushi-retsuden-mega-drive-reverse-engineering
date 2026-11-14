"""270 original setup-UI source bytes, with full-width live alias diagnostics.

Coordinates, sentinel lists and sprite records are distinct editable objects.
Physical counts constrain this editor, never the original CPU selector domain.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.ui_cursor_sprite_templates import codec as sprites

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = sprites.DEFAULT_ROM
ROM_SIZE, ROM_SHA256 = sprites.ROM_SIZE, sprites.ROM_SHA256
OUTPUT_ROOT = ROOT / "build/setup_ui_sprite_fields"
FORMAL_ROOT = ROOT / "analysis/setup_ui_sprite_fields/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-setup-UI-coordinate-and-sprite-source-fields-v1"
EDITABLE_BYTES = 270
START, END = 0x2B050, 0x2B15E
MAX_JSON = 1024 * 1024
MEMBERS = sprites.MEMBERS
LISTS = ((0x2B05A, 0x2B06A), (0x2B06A, 0x2B07A), (0x2B07A, 0x2B084))
TEMPLATES = ((0x2B084, 0x2B0B6), (0x2B0B6, 0x2B0E8), (0x2B0E8, 0x2B10E),
    (0x2B10E, 0x2B116), (0x2B116, 0x2B124), (0x2B124, 0x2B132),
    (0x2B132, 0x2B13A), (0x2B13A, 0x2B142), (0x2B142, 0x2B14A), (0x2B14A, 0x2B15E))
# Original LEAs and actual call sites; 302AC / 30484 are transparent wrappers.
CALLERS = ((0x2AD7A, 0x2B084, 0x2AD80, 0x2AF8A),
    (0x2ADAA, 0x2B0B6, 0x2ADB0, 0x2AF8A), (0x2ADDA, 0x2B0E8, 0x2ADE0, 0x2AF8A),
    (0x2AE0A, 0x2B084, 0x2AE10, 0x2AF8A), (0x2AF04, 0x2B10E, 0x2AF0A, 0xAC08),
    (0x2AF7C, 0x2B10E, 0x2AF82, 0xAC08), (0x302E8, 0x2B116, 0x302EC, 0x302AC),
    (0x30318, 0x2B124, 0x3031C, 0x302AC), (0x30348, 0x2B124, 0x3034C, 0x302AC),
    (0x30378, 0x2B124, 0x3037C, 0x302AC), (0x303B8, 0x2B132, 0x303BE, 0xAC08),
    (0x303E8, 0x2B13A, 0x303F6, 0x30484), (0x30426, 0x2B142, 0x30434, 0x30484),
    (0x306DC, 0x2B14A, 0x306E6, 0xAC08))
PINS = ((0x2AEC8, "4bfa0190"), (0x2AEDE, "4bfa018a"), (0x2AEE8, "4bfa0190"),
    (0x2AEEE, "301d"), (0x2AEF0, "0c40ffff"), (0x2AEFA, "e040"),
    (0x2AEFC, "024000ff"), (0x2AF00, "024100ff"), (0x2AF90, "0c450005"),
    (0x2AF94, "6720"), (0x2AF96, "e345"), (0x2AF98, "43fa00b6"),
    (0x2AF9E, "32315000"), (0x2AFB0, "4eb90000ac08"),
    (0x302AC, "3200e040024000ff024100ff42824eb90000ac084e75"),
    (0x30484, "e34047faffe432330000303c00b042824eb90000ac084e75"))
sha, dump = sprites.sha, sprites.dump
keys, same, uint, exact_list = sprites.keys, sprites.same, sprites.uint, sprites.exact_list
load_fields, safe_path, read_bounded, put = sprites.load_fields, sprites.safe_path, sprites.read_bounded, sprites.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical bytes, size and SHA required")
    start,end,digest = sprites.CONSUMER
    if sha(rom[start:end]) != digest:
        raise ValueError("complete original AC08 source reader differs")
    for address, raw in PINS:
        if rom[address:address + len(raw) // 2] != bytes.fromhex(raw):
            raise ValueError("original setup coordinate reader/wrapper differs")
    for lea, source, call, target in CALLERS:
        if rom[lea:lea + 2] != b"\x41\xfa" or lea + 2 + int.from_bytes(rom[lea + 2:lea + 4], "big", signed=True) != source:
            raise ValueError("original PC-relative A0 source pointer differs")
        if rom[call:call + 2] == b"\x4e\xba":
            actual = call + 2 + int.from_bytes(rom[call + 2:call + 4], "big", signed=True)
        elif rom[call:call + 2] == b"\x4e\xb9":
            actual = int.from_bytes(rom[call + 2:call + 6], "big")
        else:
            raise ValueError("original JSR opcode differs")
        if actual != target:
            raise ValueError("original consumer/wrapper target differs")


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(start=START, end=END, bytes=270, coordinate_bytes=52, sprite_bytes=218),
        evidence=dict(original_reader=sprites.CONSUMER[0], original_reader_end=sprites.CONSUMER[1],
            original_reader_sha256=sprites.CONSUMER[2],
            callers=[dict(A0_LEA=a, source=s, JSR=c, target=t, reachability="older_heuristic") for a,s,c,t in CALLERS],
            coordinate_instructions=[dict(address=a, bytes=b) for a,b in PINS],
            coordinate_table_read=0x2AF9E, selector="u16(F7022.W<<1), then sign-extended; input 5 bypasses read",
            coordinate_list_read=0x2AEEE, first_FFFF_stops=True, high_BYTE_X_low_BYTE_Y=True,
            physical_counts_are_not_CPU_clamps=True, source_projection="D2=0; no RAM writes, IRQ, bus or frames"),
        natural_selection_domain="unknown", edited_gameplay_safety="unknown", independent_CPU_comparison=False)


def fixed(start, end, role):
    return dict(id=f"rom_{start:06X}_{role}", start=start, end=end)


def coordinate(raw):
    return dict(x_BYTE=raw[0], y_BYTE=raw[1])


def coordinate_bytes(row, sentinel=False):
    keys(row, {"x_BYTE", "y_BYTE"}, "coordinate")
    data = bytes((uint(row["x_BYTE"], 255, "X BYTE"), uint(row["y_BYTE"], 255, "Y BYTE")))
    if sentinel and data == b"\xff\xff":
        raise ValueError("early coordinate list terminator")
    return data


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["selector_coordinates"] = [coordinate(rom[p:p + 2]) for p in range(START, START + 10, 2)]
    fields["coordinate_lists"] = [dict(**fixed(s,e,"coordinate_list"), terminator_WORD=65535,
        coordinates=[coordinate(rom[p:p + 2]) for p in range(s,e - 2,2)]) for s,e in LISTS]
    fields["templates"] = [dict(**fixed(s,e,"sprite_template"), terminator_WORD=32768,
        records=[sprites.record(rom[p:p + 6],p) for p in range(s,e - 2,6)]) for s,e in TEMPLATES]
    if any(rom[e - 2:e] != b"\xff\xff" for _,e in LISTS) or any(rom[e - 2:e] != b"\x80\x00" for _,e in TEMPLATES):
        raise ValueError("original first terminator differs")
    blocks(rom, fields)
    return fields


def blocks(rom, fields):
    verify_rom(rom)
    sprites.pinned(fields, metadata(), {"selector_coordinates", "coordinate_lists", "templates"}, "setup source package")
    data = b"".join(coordinate_bytes(row) for row in exact_list(fields["selector_coordinates"],5,"physical selector coordinates"))
    result = [dict(**fixed(START,START + 10,"selector_coordinates"),data=data,role="full_BYTE_coordinate_pairs")]
    for row,(s,e) in zip(exact_list(fields["coordinate_lists"],3,"physical coordinate lists"),LISTS):
        sprites.pinned(row, dict(**fixed(s,e,"coordinate_list"),terminator_WORD=65535), {"coordinates"}, "coordinate list")
        data = b"".join(coordinate_bytes(item,True) for item in exact_list(row["coordinates"],(e-s-2)//2,"list pair count")) + b"\xff\xff"
        result.append(dict(**fixed(s,e,"coordinate_list"),data=data,role="coordinate_pairs_and_first_FFFF"))
    for row,(s,e) in zip(exact_list(fields["templates"],10,"physical templates"),TEMPLATES):
        sprites.pinned(row, dict(**fixed(s,e,"sprite_template"),terminator_WORD=32768), {"records"}, "template")
        data = b"".join(sprites.record_bytes(item,s + 6*i) for i,item in enumerate(exact_list(row["records"],(e-s-2)//6,"record count"))) + b"\x80\x00"
        result.append(dict(**fixed(s,e,"sprite_template"),data=data,role="packed_sprite_records_and_first_8000"))
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES or result[-1]["end"] != END or any(a["end"] != b["start"] for a,b in zip(result,result[1:])):
        raise ValueError("fixed nonoverlapping 270-byte cost differs")
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields): image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def selector_view(image, selector_WORD):
    """Full original WORD index arithmetic, including table/list aliases."""
    uint(selector_WORD,65535,"F7022 WORD")
    if type(image) is not bytes or len(image) != ROM_SIZE: raise ValueError("full bytes image required")
    if selector_WORD == 5: return dict(status="original_selector_5_bypass", read_events=[])
    offset = (selector_WORD << 1) & 65535
    address = START + (offset - 65536 if offset & 32768 else offset)
    word = int.from_bytes(image[address:address+2],"big")
    return dict(status="read", address=address, WORD=word, x_BYTE=word>>8,y_BYTE=word&255,
        read_events=[dict(address=address,bytes=2,PC=0x2AF9E)])


def list_view(image, start, pair_budget=256):
    """Original first-FFFF source plan; budget is only a diagnostic boundary."""
    if type(image) is not bytes or len(image) != ROM_SIZE: raise ValueError("full bytes image required")
    uint(start,ROM_SIZE-2,"source");uint(pair_budget,65535,"external pair budget")
    if start & 1 or not pair_budget: raise ValueError("even source and positive external budget required")
    events, coordinates = [],[]
    for i in range(pair_budget):
        address=start+2*i
        if address>ROM_SIZE-2: raise ValueError("source boundary, not modeled CPU bus")
        word=int.from_bytes(image[address:address+2],"big")
        events.append(dict(address=address,bytes=2,WORD=word,PC=0x2AEEE))
        if word==65535:return dict(status="first_FFFF",read_events=events,coordinates=coordinates)
        coordinates.append(coordinate(image[address:address+2]))
    return dict(status="external_pair_budget",read_events=events,coordinates=coordinates)


def reference_union(image):
    addresses=set()
    for selector in range(5):
        view=selector_view(image,selector)
        addresses.update(range(view["address"],view["address"]+2))
    for start,end in LISTS:
        view=list_view(image,start)
        if view["status"]!="first_FFFF" or view["read_events"][-1]["address"]!=end-2: raise ValueError("list closure differs")
        for event in view["read_events"]: addresses.update(range(event["address"],event["address"]+2))
    for start,end in TEMPLATES:
        for p in range(start,end-2,6):
            x=int.from_bytes(image[p:p+2],"big")
            y=sprites.sprite_format.signed(int.from_bytes(image[p+4:p+6],"big")&4095,12)
            view=sprites.source_view(image,start,(128-x)&65535,(128-y)&65535)
            if view["status"]!="first_8000_TERM" or view["next_source"]!=end-2: raise ValueError("sprite source closure differs")
            for event in view["read_events"]:addresses.update(range(event["address"],event["address"]+2))
    return addresses


def schema():
    def obj(p):return dict(type="object",properties=p,required=list(p),additionalProperties=False)
    def exact(items):return dict(type="array",prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def number(lo,hi):return dict(type="integer",minimum=lo,maximum=hi)
    def literal(v):
        if type(v) is dict:return obj({k:literal(x) for k,x in v.items()})
        if type(v) is list:return exact([literal(x) for x in v])
        return dict(const=v)
    pair=obj(dict(x_BYTE=number(0,255),y_BYTE=number(0,255)))
    props={k:literal(v) for k,v in metadata().items()}
    props["selector_coordinates"]=exact([pair]*5)
    props["coordinate_lists"]=exact([obj(dict(**{k:literal(v) for k,v in fixed(s,e,"coordinate_list").items()},
        terminator_WORD=literal(65535),coordinates=exact([pair]*((e-s-2)//2)))) for s,e in LISTS])
    def record_schema(address):return obj(dict(id=literal(sprites.sprite_format.ident(address)),x_offset=number(-32767,32767),
        tile_index=number(0,2047),horizontal_flip=dict(type="boolean"),vertical_flip=dict(type="boolean"),
        palette=number(0,3),priority=dict(type="boolean"),width_tiles=number(1,4),height_tiles=number(1,4),y_offset=number(-2048,2047)))
    props["templates"]=exact([obj(dict(**{k:literal(v) for k,v in fixed(s,e,"sprite_template").items()},terminator_WORD=literal(32768),
        records=exact([record_schema(p) for p in range(s,e-2,6)]))) for s,e in TEMPLATES])
    result=obj(props);result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="Runtime additionally forbids FFFF inside coordinate lists; physical editing costs do not clamp original selectors."
    return result


def render_bundle(rom):
    fields=extract(rom); image=rebuild(rom,load_fields(dump(fields))); rows=blocks(rom,fields)
    actual=reference_union(rom)
    if image!=rom or actual!=set(range(START,END)):raise ValueError("serialized roundtrip/source union differs")
    report=dict(**metadata(),editable_bytes=270,physical_blocks=14,coordinate_pairs=23,
        sprite_records=33,sprite_terminators=10,coordinate_list_terminators=3,
        constructed_source_union_bytes=len(actual),whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        selector_5_bypasses=True,selector_6_alias=selector_view(image,6),
        selector_FFFF_alias=selector_view(image,65535),natural_source_union=False,
        blocks=[{k:v for k,v in row.items() if k!="data"}|dict(bytes=len(row["data"]),sha256=sha(row["data"])) for row in rows])
    members={"fields.json":dump(fields),"fields.schema.json":dump(schema()),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(format=FORMAT,editable_bytes=270,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):raise ValueError("output outside setup fields scope")
    if path.exists() or not path.parent.is_dir():raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("command",choices=("export","import","verify"))
    p.add_argument("--rom",default=str(DEFAULT_ROM));p.add_argument("--fields",default=str(DEFAULT_FIELDS));p.add_argument("--output")
    args=p.parse_args(argv);target=None
    if args.command!="verify":
        if not args.output:raise ValueError("fresh output required")
        target=fresh_output(args.output,args.command=="export")
        if args.command=="import" and target.suffix.lower()!=".bin":raise ValueError("fresh BIN required")
    elif args.output:raise ValueError("verify writes no output")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=="export":
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields,MAX_JSON)))
        if target is not None:put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=EDITABLE_BYTES,exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0
