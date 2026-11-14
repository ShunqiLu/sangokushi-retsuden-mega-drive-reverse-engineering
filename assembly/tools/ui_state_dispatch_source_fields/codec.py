"""274 original source bytes, in three distinct physical field groups.

The 80-byte counted stream is not a dispatch table. The two offset groups own
194 bytes, not a closed natural CPU selector/target domain. All source values
are original literals; only framing/counts and fixed editor topology are pinned.
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
OUTPUT_ROOT = ROOT / "build/ui_state_dispatch_source_fields"
FORMAL_ROOT = ROOT / "analysis/ui_state_dispatch_source_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 274
FORMAT = "g5510-UI-counted-stream-and-signed-dispatch-source-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
STREAM_START, STREAM_END = 0x2118, 0x2168
STREAM_SHA256 = reference_value(__name__, 'STREAM_SHA256')
# Source start/end, JSR signed-offset base, already-fetched input RAM WORD, read PC.
TABLES = ((0x2438, 0x2490, 0x2490, 0xFFF362, 0x241C),
          (0x254E, 0x25B8, 0x25B8, 0xFFF380, 0x2544))
TABLE_SHA256 = (reference_value(__name__, 'TABLE_SHA256'),
                reference_value(__name__, 'TABLE_SHA256_2'))
UNION_SHA256 = reference_value(__name__, 'UNION_SHA256')
CONSUMERS = (
    (0x20F0, 0x2118, reference_value(__name__, 'CONSUMERS')),
    (0x26BFA, 0x26C8E, reference_value(__name__, 'CONSUMERS_2')),
    (0x2416, 0x2438, reference_value(__name__, 'CONSUMERS_3')),
    (0x2490, 0x254E, reference_value(__name__, 'CONSUMERS_4')),
)
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_BANK_SHA256 = reference_value(__name__, 'LAYOUT_BANK_SHA256')
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def signed_WORD(word):
    word = uint(word, 65535, "WORD")
    return word - 65536 if word & 32768 else word


def image_bytes(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("complete bytes image required")


def verify_rom(rom):
    image_bytes(rom)
    if sha(rom) != ROM_SHA256:
        raise ValueError("canonical source SHA-256 required")
    for start, end, expected in CONSUMERS:
        if sha(rom[start:end]) != expected:
            raise ValueError("complete original consumer/caller body differs")
    ranges = ((STREAM_START, STREAM_END),) + tuple((s, e) for s, e, *_ in TABLES)
    if sha(b"".join(rom[s:e] for s, e in ranges)) != UNION_SHA256:
        raise ValueError("original literal source differs")


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=[dict(start=STREAM_START, end=STREAM_END, bytes=80,
                            role="counted_UI_row_stream", sha256=STREAM_SHA256)] +
            [dict(start=s, end=e, bytes=e-s, role="signed_WORD_dispatch_offsets", sha256=h)
             for (s, e, *_), h in zip(TABLES, TABLE_SHA256)],
        evidence=dict(source="canonical consumer bytes, counted closure and original indexed WORD reads",
            enhanced_ledger=dict(path=ENHANCED_PATH, sha256=ENHANCED_SHA256,
                stream_caller_confidence="heuristic", stream_reader_confidence="runtime_confirmed",
                dispatch_consumer_confidence="runtime_confirmed"),
            frozen_raw_layout=dict(id=LAYOUT_ID, bank00_sha256=LAYOUT_BANK_SHA256,
                                  emitted_raw_bytes=EDITABLE_BYTES, typed_overlap_bytes=0),
            consumers=[dict(start=s, end=e, sha256=h) for s, e, h in CONSUMERS],
            counted_source=dict(A0_LEA=0x210C, PC_base=0x210E, displacement_WORD=0x000A,
                true_JSR=0x2110, target=0x26BFA, caller_D0_LONG=0xC0000008,
                caller_D1_WORD=7, caller_D2_WORD=0xC422, columns=8, lines=7,
                row_count_load=0x26C02, row_count_subtract=0x26C04, row_DBRA=0x26C3A,
                source_WORD_read=0x26C10, sign_branch=0x26C12,
                direct_count_decrement=0x26C1C, row_remaining_test=0x26C36,
                negative_dispatch="((control_WORD & 7FFF) >> 7) & ~1",
                used_selectors=[0, 2], repeat_payload_read=0x26C5E,
                ascending_payload_read=0x26C78, ascending_ADDQ_WORD=0x26C82,
                count="original nonzero low control BYTE", output_prefix_WORD=0xC000,
                source_stop="seven counted rows of eight cells; no source marker",
                unused_handlers_and_full_dispatch_domain="unknown"),
            state_dispatch=dict(input_WORD_RAM=0xFFF362, input_read=0x2416,
                index_LSL_WORD=0x241A, read_PC=0x241C, read_PC_base=0x241E,
                displacement_BYTE=0x1A, read_base=0x2438, original_guard="none",
                JSR_PC=0x2420, JSR_PC_base=0x2422, JSR_displacement_BYTE=0x6E,
                JSR_base=0x2490, constructed_local_read_witnesses=[0, 43],
                physical_WORD_count=44, physical_count_is_not_CPU_clamp=True),
            event_dispatch=dict(input_WORD_RAM=0xFFF380, input_read=0x2490,
                unsigned_60_compare=0x2494, BCC=0x2498, FF_compare=0x2500,
                guard="unsigned input >= 0060 and input != 00FF",
                input_subtract_WORD=0x253E, index_LSL_WORD=0x2542,
                read_PC=0x2544, read_PC_base=0x2546, displacement_BYTE=8,
                read_base=0x254E, JSR_PC=0x2548, JSR_PC_base=0x254A,
                JSR_displacement_BYTE=0x6E, JSR_base=0x25B8,
                constructed_local_read_witnesses=[0x60, 0x94], physical_WORD_count=53,
                physical_count_is_not_CPU_clamp=True),
            dispatch_addressing=dict(index="LSL.W wraps16 then final index WORD is sign extended",
                offset="complete BE16 source, sign extended into PC-relative JSR address",
                natural_selector_domain="unknown", indirect_target_domain_closed=False,
                original_targets_are_readonly_diagnostics_not_editor_constraints=True,
                out_of_ROM_indexed_reads_are_explicit_external_boundaries=True)),
        source_business_names="unknown", edited_gameplay_safety="unknown",
        full_RAM_VDP_stack_bus_CPU_execution=False, independent_CPU_comparison=False,
        exclusions=dict(code_and_neighbor_tables_not_emitted=True,
                        all_writers_and_natural_state_paths_not_proven=True))


def stream_fixed():
    return dict(id="rom_002118_counted_UI_rows", start=STREAM_START, end=STREAM_END,
                role="counted_UI_row_stream", columns=8, lines=7, WORD_order="big")


def table_fixed(index):
    start, end, target_base, ram, pc = TABLES[index]
    return dict(id=f"rom_{start:06X}_signed_dispatch_offsets", start=start, end=end,
        role="signed_WORD_dispatch_offsets", WORD_count=(end-start)//2,
        WORD_order="big", index=index, input_WORD_RAM=ram, read_PC=pc, JSR_base=target_base)


def offset_fixed(table_index, index):
    return dict(id=f"dispatch_{table_index}_offset_{index:02d}", index=index,
                address=TABLES[table_index][0] + 2*index)


def pinned(row, fixed, mutable, label):
    keys(row, set(fixed) | set(mutable), label)
    for key, value in fixed.items(): same(row[key], value, label + "." + key)


def decode_stream(image):
    """Package grammar for the original 7x8 counted source and two used handlers.

    This bounded parser accepts edited whole-image payloads. It is not a CPU
    model of arbitrary control edits, zero-count DBRA or unused handlers.
    """
    image_bytes(image)
    cursor, rows = STREAM_START, []
    def take():
        nonlocal cursor
        if cursor + 2 > STREAM_END:
            raise ValueError("counted source parser crossed its disclosed editing boundary")
        word = int.from_bytes(image[cursor:cursor+2], "big")
        cursor += 2
        return word
    for row_index in range(7):
        start, cells, operations = cursor, 0, []
        while cells < 8:
            address, word = cursor, take()
            if word < 0x8000:
                op = dict(kind="direct_WORD", start=address, end=cursor,
                          emitted_cells=1, WORD=word)
            else:
                selector, count = ((word & 0x7FFF) >> 7) & ~1, word & 255
                if selector not in (0, 2) or not count:
                    raise ValueError("outside the two original handler/nonzero-count parser contracts")
                payload = take()
                op = dict(kind="repeat_WORD" if selector == 0 else "ascending_WORD",
                    start=address, end=cursor, emitted_cells=count, control_WORD=word,
                    payload_WORD=payload)
            cells += op["emitted_cells"]
            if cells > 8: raise ValueError("operation exceeds original eight-cell row")
            operations.append(op)
        rows.append(dict(row_index=row_index, start=start, end=cursor, cells=8, operations=operations))
    if cursor != STREAM_END: raise ValueError("counted source does not stop at original end")
    return dict(**stream_fixed(), rows=rows)


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result["counted_stream"] = decode_stream(rom)
    result["dispatch_tables"] = [dict(**table_fixed(t), offsets=[dict(**offset_fixed(t,i),
        offset_WORD=int.from_bytes(rom[s+2*i:s+2*i+2], "big")) for i in range((e-s)//2)])
        for t, (s,e,*_) in enumerate(TABLES)]
    return result


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {"counted_stream", "dispatch_tables"}, "source package")
    original = decode_stream(rom)
    stream = fields["counted_stream"]
    pinned(stream, stream_fixed(), {"rows"}, "counted stream")
    raw = bytearray()
    for row, expected in zip(exact_list(stream["rows"], 7, "counted rows"), original["rows"]):
        pinned(row, {k:v for k,v in expected.items() if k != "operations"}, {"operations"}, "row")
        for op, source in zip(exact_list(row["operations"], len(expected["operations"]), "operations"), expected["operations"]):
            mutable = {"WORD"} if source["kind"] == "direct_WORD" else {"payload_WORD"}
            pinned(op, {k:v for k,v in source.items() if k not in mutable}, mutable, "operation")
            if source["kind"] == "direct_WORD":
                word = uint(op["WORD"], 32767, "direct WORD retaining original nonnegative branch")
                raw.extend(word.to_bytes(2,"big"))
            else:
                raw.extend(op["control_WORD"].to_bytes(2,"big"))
                raw.extend(uint(op["payload_WORD"],65535,"complete run payload WORD").to_bytes(2,"big"))
    result = [dict(id=stream["id"], start=STREAM_START, end=STREAM_END,
                   data=bytes(raw), role="confirmed_counted_UI_source_WORDs")]
    for t, row in enumerate(exact_list(fields["dispatch_tables"], 2, "distinct dispatch groups")):
        fixed = table_fixed(t)
        pinned(row, fixed, {"offsets"}, "dispatch group")
        data = bytearray()
        for i, op in enumerate(exact_list(row["offsets"],fixed["WORD_count"],"physical offset WORDs")):
            pinned(op, offset_fixed(t,i), {"offset_WORD"}, "offset")
            data.extend(uint(op["offset_WORD"],65535,"complete signed-offset WORD bits").to_bytes(2,"big"))
        result.append(dict(id=fixed["id"],start=fixed["start"],end=fixed["end"],
                           data=bytes(data),role="confirmed_signed_WORD_dispatch_source"))
    if [len(r["data"]) for r in result] != [80,88,106] or any(
            a["end"] > b["start"] for a,b in zip(result,result[1:])):
        raise ValueError("exact three disjoint physical byte costs differ")
    return result


def rebuild(rom, fields):
    rows = blocks(rom,fields)
    image = bytearray(rom)
    for row in rows: image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def lookup_dispatch(image, table_index, selector_WORD):
    """Original local indexed read/JSR-address diagnostic, never target execution.

    Inputs are already fetched RAM WORDs. Live edited source/neighbor/code bytes
    are read without extraction/hash gates or catalog clamps. Non-ROM effective
    addresses are boundaries: no negative Python indexing or guessed RAM value.
    """
    image_bytes(image)
    t = uint(table_index,1,"physical dispatch role selector, not CPU input")
    value = uint(selector_WORD,65535,"already fetched input WORD")
    result = dict(table_index=t,selector_WORD=value,source_only=True,
                  natural_execution=False,CPU_execution=False)
    if t == 1 and (value < 0x60 or value == 0xFF):
        return dict(**result,status="other_original_branch_no_secondary_lookup")
    input_index = value if t == 0 else (value-0x60)&65535
    index = (input_index<<1)&65535
    start,end,target_base,_,pc = TABLES[t]
    address = (start+signed_WORD(index))&0xFFFFFFFF
    result.update(index_WORD=index,read_address=address,read_PC=pc,
                  read_inside_editable_group=start<=address<end)
    if not 0<=address<=ROM_SIZE-2:
        return dict(**result,status="outside_ROM_read_boundary")
    word = int.from_bytes(image[address:address+2],"big")
    target = (target_base+signed_WORD(word))&0xFFFFFFFF
    return dict(**result,status="offset_WORD_read",offset_WORD=word,JSR_target=target,
                JSR_target_WORD_aligned=not bool(target&1),
                JSR_target_inside_ROM=target<ROM_SIZE)


def stream_preview(image):
    """Derived WORD rows with original C000 OR and ADDQ.W2; never editable."""
    source = decode_stream(image)
    rows = []
    for row in source["rows"]:
        words = []
        for op in row["operations"]:
            if op["kind"] == "direct_WORD": words.append(op["WORD"]|0xC000)
            else:
                word = op["payload_WORD"]|0xC000
                for _ in range(op["emitted_cells"]):
                    words.append(word)
                    if op["kind"] == "ascending_WORD": word=(word+2)&65535
        rows.append(words)
    return dict(rows=rows,decoded_WORDs=56,source_only=True,editing_authority=False,
                natural_execution=False,CPU_execution=False)


def source_reference_union(image):
    """Owned source-read union under declared constructed local inputs only."""
    stream=decode_stream(image)
    addresses={p for row in stream["rows"] for op in row["operations"] for p in range(op["start"],op["end"])}
    for t,(start,end,*_) in enumerate(TABLES):
        for i in range((end-start)//2):
            row=lookup_dispatch(image,t,i if t==0 else 0x60+i)
            if row["read_address"] != start+2*i: raise ValueError("local WORD-read witness differs")
            addresses.update(range(row["read_address"],row["read_address"]+2))
    return addresses


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
    rows=[]
    for row in fields["counted_stream"]["rows"]:
        ops=[]
        for op in row["operations"]:
            p={k:fixed(v) for k,v in op.items()}
            name="WORD" if op["kind"]=="direct_WORD" else "payload_WORD"
            p[name]=dict(type="integer",minimum=0,maximum=32767 if name=="WORD" else 65535)
            ops.append(obj(p))
        rows.append(obj({**{k:fixed(v) for k,v in row.items() if k!="operations"},"operations":exact(ops)}))
    props["counted_stream"]=obj({**{k:fixed(v) for k,v in stream_fixed().items()},"rows":exact(rows)})
    props["dispatch_tables"]=exact([obj({**{k:fixed(v) for k,v in table_fixed(t).items()},
        "offsets":exact([obj({**{k:fixed(v) for k,v in offset_fixed(t,i).items()},
            "offset_WORD":dict(type="integer",minimum=0,maximum=65535)})
            for i in range(table_fixed(t)["WORD_count"])])}) for t in range(2)])
    result=obj(props)
    result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="Three distinct source roles. Stream counts/controls and direct sign fixed; full payload/offset WORDs mutable. Physical tables do not close natural CPU domains or restrict JSR targets."
    return result


def render_bundle(rom):
    fields=extract(rom); serialized=dump(fields)
    image=rebuild(rom,load_fields(serialized)); rows=blocks(rom,fields)
    expected={p for row in rows for p in range(row["start"],row["end"])}
    if image!=rom or source_reference_union(rom)!=expected or len(expected)!=EDITABLE_BYTES:
        raise ValueError("serialized whole-ROM roundtrip or original owned read union differs")
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=3,
        counted_source_bytes=80,dispatch_source_bytes=194,original_dispatch_offset_WORDs=[44,53],
        local_owned_read_union_bytes=len(expected),source_union_sha256=UNION_SHA256,
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        counted_row_source_bytes=[r["end"]-r["start"] for r in fields["counted_stream"]["rows"]],
        counted_source_preview=stream_preview(rom),
        original_targets_diagnostic_only=[[lookup_dispatch(rom,t,i if t==0 else 0x60+i)["JSR_target"]
            for i in range(table_fixed(t)["WORD_count"])] for t in range(2)],
        overread_diagnostics=[lookup_dispatch(rom,0,44),lookup_dispatch(rom,0,0xFFFF),
            lookup_dispatch(rom,1,0x95),lookup_dispatch(rom,1,0xFFFF)],
        code_and_neighbor_tables_emitted=False,
        blocks=[{k:v for k,v in row.items() if k!="data"}|dict(bytes=len(row["data"]),sha256=sha(row["data"])) for row in rows])
    members={"fields.json":serialized,"fields.schema.json":dump(schema(rom)),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=3,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError("output must stay in UI state source build scope or exact formal bundle")
    if path.exists() or not path.parent.is_dir(): raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM)); parser.add_argument("--fields")
    parser.add_argument("--bundle"); parser.add_argument("--output")
    args=parser.parse_args(argv); target=None
    if args.command=="export":
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError("export requires a fresh output only")
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
