"""296 actually-read bytes: two 8-WORD sources and two counted UI row streams.

Original topology/counts and complete 32-bit RAM refs are pinned. Palette WORDs,
direct positive source WORDs and full repeat/ascending payload WORDs are mutable.
Aliases are diagnostics, not additional emit blocks. No full RAM renderer model.
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
OUTPUT_ROOT = ROOT / "build/duel_ui_row_stream_fields"
FORMAL_ROOT = ROOT / "analysis/duel_ui_row_stream_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 296
START, END = 0x028100, 0x028228
FORMAT = "g5510-counted-duel-UI-source-WORD-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
PALETTES = ((0x28100, 0x28110, 0x28DBA, 0x28DC4, 0x28DC8),
            (0x28110, 0x28120, 0x28BEA, 0x28BE0, 0x28BEE))
STREAMS = ((0x28120, 0x28174, 3, 0x26FF0, 0x27004),
           (0x28174, 0x28228, 5, 0x27010, 0x27024))
ALIASES = ((0x281A0, 0xFF706C, 0x27506), (0x281B6, 0xFF70BC, 0x2751C),
           (0x281EC, 0xFF706E, 0x2709C), (0x28202, 0xFF70BE, 0x271D4))
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = "build/direct_code/layout/" + LAYOUT_ID + "/m68k_bank02.s"
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
CONSUMERS = (
    (0x26BFA, 0x26CD6, reference_value(__name__, 'CONSUMERS')),
    (0x26FF0, 0x2700A, reference_value(__name__, 'CONSUMERS_2')),
    (0x27010, 0x2702A, reference_value(__name__, 'CONSUMERS_3')),
    (0x2709C, 0x270B6, reference_value(__name__, 'CONSUMERS_4')),
    (0x271D4, 0x271EE, reference_value(__name__, 'CONSUMERS_5')),
    (0x27506, 0x27534, reference_value(__name__, 'CONSUMERS_6')),
    (0x28BE0, 0x28BF4, reference_value(__name__, 'CONSUMERS_7')),
    (0x28DBA, 0x28DCE, reference_value(__name__, 'CONSUMERS_8')),
)
INSTRUCTIONS = (
    (0x26FF0, "41fa112e"), (0x26FF6, "203c60000028"), (0x26FFC, "323c0003"), (0x27004, "4eb900026bfa"),
    (0x27010, "41fa1162"), (0x27016, "203c60000028"), (0x2701C, "323c0005"), (0x27024, "4eb900026bfa"),
    (0x2709C, "41fa114e"), (0x270A6, "203c60000004"), (0x270AC, "323c0001"),
    (0x271D4, "41fa102c"), (0x271DE, "203c60000004"), (0x271E4, "323c0001"),
    (0x27506, "41fa0c98"), (0x2751C, "41fa0c98"), (0x27526, "203c60000004"), (0x2752C, "323c0001"),
    (0x28BE0, "3e3c0007"), (0x28BEA, "45faf524"), (0x28BEE, "36da"), (0x28BF0, "51cffffc"),
    (0x28DBA, "45faf344"), (0x28DC4, "363c0007"), (0x28DC8, "36da"), (0x28DCA, "51cbfffc"),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    for start, end, expected in CONSUMERS:
        if sha(rom[start:end]) != expected:
            raise ValueError("pinned original reader/caller bytes differ")


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(start=START, end=END, bytes=EDITABLE_BYTES, palette_source_bytes=32,
                            row_stream_source_bytes=264, emitted_blocks=4),
        evidence=dict(confidence="confirmed", source="canonical consumers, strict counted read closure, old ledger",
            enhanced_source=dict(path=ENHANCED_PATH, sha256=ENHANCED_SHA256, original_caller_confidence="heuristic"),
            frozen_raw_layout=dict(id=LAYOUT_ID, path=LAYOUT_PATH, sha256=LAYOUT_SHA256,
                                  line=780, bank=2, offset=0x8100, length=296, old_typed_overlap_bytes=0),
            consumers=[dict(start=s, end=e, bytes=e-s, sha256=h) for s,e,h in CONSUMERS],
            instructions=[dict(address=a, bytes=b, original_confidence="heuristic") for a,b in INSTRUCTIONS],
            palette_reads=dict(WORD_count=8, count_loads=[0x28DC4, 0x28BE0], WORD_reads=[0x28DC8, 0x28BEE],
                               destinations="A3 preset to FFFB00 or FFFB20; full palette/RAM algorithm not modeled"),
            row_reader=dict(entry=0x26BFA, WORD_read=0x26C10, sign_branch=0x26C12,
                positive_WORD="direct source cell, OR with original caller high WORD", direct_count_decrement=0x26C1C,
                negative_selector_rule="((control_WORD & 0x7FFF) >> 7) & ~1",
                dispatch_table=0x26C4C, dispatch_base=0x26C58,
                used_selectors=[0, 2, 4], used_handlers=[0x26C58, 0x26C72, 0x26C8E],
                run_count="low control BYTE; original nonzero counts pinned",
                repeat_payload_read=0x26C5E, ascending_payload_read=0x26C78,
                ascending_increment=2, indirect_LONG_read=0x26C92,
                row_remaining_counter="D3 = D0.W, each operation subtracts emitted cell count",
                row_loop=0x26C36, lines_DBRA=0x26C3A, termination="caller counters, not source marker",
                full_dispatch_domain_claim=False, independent_RAM_numeric_rendering=False),
            embedded_aliases=[dict(start=s, end=s+6, bytes=6, original_RAM_ref_LONG=p,
                                   caller_LEA=pc, width=4, lines=1, emitted_again=False) for s,p,pc in ALIASES]),
        original_topology_counts_and_RAM_refs_pinned=True, business_meanings="unknown",
        Unicode_mapping="unknown", edited_gameplay_safety="unknown", independent_CPU_comparison=False)


def palette_fixed(spec):
    start, end, lea, counter, read = spec
    return dict(id=f"rom_{start:06X}_palette_WORD_source", start=start, end=end, WORD_order="big",
                WORD_count=8, source_LEA=lea, counter_load=counter, WORD_read=read)


def stream_fixed(spec):
    start, end, lines, lea, call = spec
    return dict(id=f"rom_{start:06X}_counted_row_stream", start=start, end=end, source_LEA=lea,
                source_call=call, original_D0_LONG=0x60000028, columns=40, lines=lines, reader=0x26BFA)


def decode_stream(image, spec):
    """Source grammar for the three actually-used handlers, never a full CPU model."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("counted source decoding requires complete bytes image")
    fixed = stream_fixed(spec)
    p = fixed["start"]
    rows = []
    for row_index in range(fixed["lines"]):
        begin, emitted, operations = p, 0, []
        while emitted < 40:
            if p + 2 > fixed["end"]:
                raise ValueError("source read outside fixed counted stream")
            start = p
            word = int.from_bytes(image[p:p+2], "big")
            p += 2
            if word < 0x8000:
                operation = dict(kind="direct_WORD", start=start, end=p, emitted_cells=1, WORD=word)
            else:
                selector = ((word & 0x7FFF) >> 7) & ~1
                count = word & 255
                if not count or selector not in (0, 2, 4):
                    raise ValueError("unsupported original source handler or zero run count")
                cost = 4 if selector == 4 else 2
                if p + cost > fixed["end"]:
                    raise ValueError("control payload outside fixed counted stream")
                operation = dict(kind={0:"repeat_WORD", 2:"ascending_WORD", 4:"indirect_RAM_WORD"}[selector],
                                 start=start, end=p+cost, emitted_cells=count, control_WORD=word)
                value = int.from_bytes(image[p:p+cost], "big")
                operation["RAM_ref_LONG" if selector == 4 else "payload_WORD"] = value
                p += cost
            emitted += operation["emitted_cells"]
            if emitted > 40:
                raise ValueError("operation overruns original row width")
            operations.append(operation)
        rows.append(dict(row_index=row_index, start=begin, end=p, cell_count=40, operations=operations))
    if p != fixed["end"]:
        raise ValueError("counted source stop differs from original end")
    return dict(**fixed, rows=rows)


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["palettes"] = [dict(**palette_fixed(spec), WORDs=[int.from_bytes(rom[p:p+2], "big")
        for p in range(spec[0], spec[1], 2)]) for spec in PALETTES]
    fields["streams"] = [decode_stream(rom, spec) for spec in STREAMS]
    return fields


def pinned(value, fixed, mutable, label):
    keys(value, set(fixed) | set(mutable), label)
    for key, expected in fixed.items():
        same(value[key], expected, label + "." + key)


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {"palettes", "streams"}, "counted UI package")
    result = []
    for row, spec in zip(exact_list(fields["palettes"], 2, "palette sources"), PALETTES):
        pinned(row, palette_fixed(spec), {"WORDs"}, "palette source")
        raw = b"".join(uint(word, 65535, "full palette source WORD").to_bytes(2, "big")
                       for word in exact_list(row["WORDs"], 8, "palette WORD count"))
        result.append(dict(id=row["id"], start=spec[0], end=spec[1], data=raw, role="counted_palette_RAM_WORD_source"))
    for stream, spec in zip(exact_list(fields["streams"], 2, "counted streams"), STREAMS):
        original = decode_stream(rom, spec)
        pinned(stream, stream_fixed(spec), {"rows"}, "stream")
        raw = bytearray()
        for row, expected in zip(exact_list(stream["rows"], spec[2], "stream lines"), original["rows"]):
            pinned(row, {k:v for k,v in expected.items() if k != "operations"}, {"operations"}, "stream row")
            for op, source in zip(exact_list(row["operations"], len(expected["operations"]), "fixed operations"), expected["operations"]):
                mutable = {"WORD"} if source["kind"] == "direct_WORD" else ({"payload_WORD"} if "payload_WORD" in source else set())
                pinned(op, {k:v for k,v in source.items() if k not in mutable}, mutable, "source operation")
                if source["kind"] == "direct_WORD":
                    word = uint(op["WORD"], 65535, "complete direct source WORD")
                    if word & 0x8000:
                        raise ValueError("direct source WORD must retain original positive sign branch")
                    raw.extend(word.to_bytes(2, "big"))
                else:
                    raw.extend(op["control_WORD"].to_bytes(2, "big"))
                    if "payload_WORD" in source:
                        raw.extend(uint(op["payload_WORD"], 65535, "complete run payload WORD").to_bytes(2, "big"))
                    else:
                        raw.extend(op["RAM_ref_LONG"].to_bytes(4, "big"))
        if len(raw) != spec[1] - spec[0]:
            raise ValueError("fixed counted stream encoded cost differs")
        result.append(dict(id=stream["id"], start=spec[0], end=spec[1], data=bytes(raw), role="fixed_counted_UI_row_source"))
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES or any(a["end"] != b["start"] for a,b in zip(result,result[1:])):
        raise ValueError("exact 296-byte source closure or contiguous nonoverlap differs")
    return result


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def lookup_alias(image, alias_index):
    """Catalog view of the fixed caller's six source bytes from an edited image."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires complete bytes image")
    index = uint(alias_index, 3, "fixed alias catalog index, not a CPU selector")
    start = ALIASES[index][0]
    return dict(start=start, end=start+6, control_WORD=int.from_bytes(image[start:start+2], "big"),
                RAM_ref_LONG=int.from_bytes(image[start+2:start+6], "big"))


def schema(rom):
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def exact(items):
        return dict(type="array", prefixItems=items, items=False, minItems=len(items), maxItems=len(items))
    def fixed(value):
        if type(value) is dict: return obj({k:fixed(v) for k,v in value.items()})
        if type(value) is list: return exact([fixed(v) for v in value])
        return dict(type={str:"string", int:"integer", bool:"boolean"}[type(value)], const=value)
    fields = extract(rom)
    properties = {k:fixed(v) for k,v in metadata().items()}
    properties["palettes"] = exact([obj({**{k:fixed(v) for k,v in row.items() if k != "WORDs"},
        "WORDs":dict(type="array", minItems=8, maxItems=8, items=dict(type="integer",minimum=0,maximum=65535))}) for row in fields["palettes"]])
    streams = []
    for stream in fields["streams"]:
        rows = []
        for row in stream["rows"]:
            ops = []
            for op in row["operations"]:
                op_props = {k:fixed(v) for k,v in op.items()}
                if "WORD" in op: op_props["WORD"] = dict(type="integer", minimum=0, maximum=32767)
                if "payload_WORD" in op: op_props["payload_WORD"] = dict(type="integer", minimum=0, maximum=65535)
                ops.append(obj(op_props))
            rows.append(obj({**{k:fixed(v) for k,v in row.items() if k != "operations"}, "operations":exact(ops)}))
        streams.append(obj({**{k:fixed(v) for k,v in stream.items() if k != "rows"}, "rows":exact(rows)}))
    properties["streams"] = exact(streams)
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Original topology/counts/full LONG refs fixed; full palette and run-payload WORDs editable, direct WORDs retain sign branch. No source terminator, reconstructed literal formula or repeated alias emit."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom: raise ValueError("serialized whole-ROM source roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=4,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), preview_is_editing_authority=False,
        original_aliases=[lookup_alias(rom,i) for i in range(4)],
        row_source_lengths=[[row["end"]-row["start"] for row in stream["rows"]] for stream in fields["streams"]],
        blocks=[{k:v for k,v in row.items() if k != "data"} | dict(bytes=len(row["data"]),sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json":serialized, "fields.schema.json":dump(schema(rom)), "validation.json":dump(report)}
    members["manifest.json"] = dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=4,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in duel_ui_row_stream_fields build scope or exact formal bundle")
    if path.exists() or not path.parent.is_dir(): raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM))
    parser.add_argument("--fields")
    parser.add_argument("--bundle")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    target = None
    if args.command == "export":
        if args.output is None or args.fields is not None or args.bundle is not None: raise ValueError("export requires fresh output only")
        target = fresh_output(args.output,bundle=True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None: raise ValueError("import requires fields and fresh output")
        target = fresh_output(args.output)
        if target.suffix.lower() != ".bin": raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom = read_bounded(args.rom,ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name,data in members.items(): put(target/name,data)
        result = dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={name:sha(data) for name,data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS: raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON) != data: raise ValueError("canonical bundle drift: "+name)
        result = dict(path=str(bundle),verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON))
        image = rebuild(rom,fields)
        if target is not None: put(target,image)
        result = dict(path=None if target is None else str(target),editable_bytes=EDITABLE_BYTES,
                      bytes=len(image),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__ == "__main__": raise SystemExit(main())
