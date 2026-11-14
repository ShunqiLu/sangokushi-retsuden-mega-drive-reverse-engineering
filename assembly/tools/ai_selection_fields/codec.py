"""Lossless physical AI-selection BYTE rows, with faithful signed cursor reads.

Exactly fourteen original physical rows of fourteen BYTEs are editable. All
two-BYTE stride gaps remain outside the emit. Selector WORD capacity is not
clamped to physical rows. Diagnostics use edited images and preserve actual
code aliases. Parameter business semantics remain candidate/unknown.
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
OUTPUT_ROOT = ROOT / "build/ai_selection_fields"
FORMAL_ROOT = ROOT / "analysis/ai_selection_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 196
ROW_COUNT, ROW_BYTES, STRIDE = 14, 14, 16
START, INITIAL_CURSOR = 0x032652, 0x032660
LAST_ROW_END, CONTAINER_STOP = 0x032730, 0x032732
FORMAT = "g5510-ai-selection-fixed-reverse-BYTE-rows-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
CONSUMER_START, CONSUMER_END = 0x0325E4, 0x032652
CONSUMER_SHA256 = reference_value(__name__, 'CONSUMER_SHA256')
SEALED_PATH = "analysis/dispatch_code/generated/instructions.json"
SEALED_SHA256 = reference_value(__name__, 'SEALED_SHA256')
FROZEN_RULE_PATH = "tools/recovered_rules/ai_selection_rules.py"
FROZEN_RULE_SHA256 = reference_value(__name__, 'FROZEN_RULE_SHA256')
INSTRUCTIONS = (
    (0x325E4, "41f8f428"), (0x325E8, "4241"), (0x325EA, "343c0027"),
    (0x325EE, "b018"), (0x325F0, "66000004"), (0x325F4, "5241"),
    (0x325F6, "51cafff6"), (0x325FA, "4e75"),
    (0x325FC, "47f8e640"), (0x32600, "43fa005e"), (0x32604, "4e71"),
    (0x32606, "3038f376"), (0x3260A, "e948"), (0x3260C, "d2c0"),
    (0x3260E, "4243"), (0x32610, "383cffff"), (0x32614, "303c000d"),
    (0x32618, "3a38f376"), (0x3261C, "e34d"), (0x3261E, "45f8e710"),
    (0x32622, "3a325000"), (0x32626, "0c210001"), (0x3262A, "62000020"),
    (0x3262E, "0105"), (0x32630, "6600001a"), (0x32634, "3c00"),
    (0x32636, "e34e"), (0x32638, "4a736000"), (0x3263C, "6b00000e"),
    (0x32640, "61a2"), (0x32642, "b243"), (0x32644, "63000006"),
    (0x32648, "3601"), (0x3264A, "3800"), (0x3264C, "51c8ffd8"),
    (0x32650, "4e75"),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def ident(row):
    return f"rom_{START + STRIDE * row:06X}_ai_selection_row_{row:02d}"


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    if sha(rom[CONSUMER_START:CONSUMER_END]) != CONSUMER_SHA256:
        raise ValueError("pinned original AI consumer bytes differ")
    if rom[CONTAINER_STOP:CONTAINER_STOP + 4] != bytes.fromhex("61000040"):
        raise ValueError("pinned code entry after physical row container differs")


def gaps():
    return [dict(start=INITIAL_CURSOR + STRIDE * row,
                 end=INITIAL_CURSOR + STRIDE * row + 2,
                 original_hex="0000", bytes=2, physical_emit=False,
                 role="unknown; retained stride BYTEs") for row in range(ROW_COUNT)]


def metadata():
    return dict(
        format=FORMAT, confidence="candidate", physical_format_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(start=START, last_row_end=LAST_ROW_END, stride_container_stop=CONTAINER_STOP,
                            rows=ROW_COUNT, BYTEs_per_row=ROW_BYTES, stride_BYTES=STRIDE,
                            emit_BYTES=EDITABLE_BYTES, excluded_stride_BYTES=28,
                            excluded_gaps=gaps(), physical_row_capacity_is_CPU_clamp=False),
        evidence=dict(
            confidence="confirmed", source="canonical consumer bytes + existing sealed instruction rows",
            sealed_source=dict(path=SEALED_PATH, sha256=SEALED_SHA256,
                               original_confidence="candidate", discovery_confidence="heuristic"),
            frozen_rule_reference=dict(path=FROZEN_RULE_PATH, sha256=FROZEN_RULE_SHA256,
                                       runtime_file_read=False),
            consumer=dict(start=CONSUMER_START, end=CONSUMER_END, bytes=110,
                          entry_addresses=[0x325E4, 0x325FC], sha256=CONSUMER_SHA256),
            instructions=[dict(address=address, bytes=raw, original_confidence="candidate")
                          for address, raw in INSTRUCTIONS],
            row_cursor=dict(register="A1", LEA_address=0x32600, bytes="43fa005e",
                            PC_base=0x32602, displacement_WORD=0x005E, initial_cursor=INITIAL_CURSOR,
                            selector_read_address=0x32606, selector_RAM=0xFFF376,
                            LSL_W4_address=0x3260A, signed_ADDA_W_address=0x3260C,
                            offset_rule="signed_WORD((selector_WORD << 4) & 0xFFFF)",
                            predecrement_read_address=0x32626,
                            read_candidate_order=list(range(13, -1, -1)), loop_D0_WORD_initial=13),
            gate_order=[dict(order=0, address=0x32626, operation="CMPI.B #1,-(A1)",
                             following_branch=0x3262A, branch="BHI unsigned BYTE > 1 skips"),
                        dict(order=1, address=0x3262E, operation="BTST candidate,E710-derived WORD",
                             following_branch=0x32630, branch="BNE skips"),
                        dict(order=2, address=0x32638, operation="TST.W E640 head at candidate*2",
                             following_branch=0x3263C, branch="BMI negative WORD skips"),
                        dict(order=3, address=0x32640, operation="call 0325E4 count forty F428 BYTEs",
                             following_compare=0x32642, branch_address=0x32644,
                             branch="BLS keeps existing result on count <= best")],
            excluded_code_alias=dict(selector_WORD=14, start=CONTAINER_STOP, end=0x32740,
                                     original_hex="610000404a426b000028363c0005",
                                     physical_emit=False, sealed_entry=CONTAINER_STOP)),
        parameter_business_meaning="unknown", policy_interpretation_confidence="candidate",
        consumer_reachability_confidence="candidate", edited_gameplay_safety="unknown",
        complete_RAM_algorithm=False, independent_CPU_comparison=False,
    )


def row_fixed(row):
    return dict(id=ident(row), physical_row=row, start=START + STRIDE * row,
                end=INITIAL_CURSOR + STRIDE * row)


def BYTE_fixed(row, candidate):
    return dict(id=f"ai_selection_r{row:02d}_candidate_{candidate:02d}",
                candidate_index=candidate, address=START + STRIDE * row + candidate)


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["rows"] = [dict(**row_fixed(row),
                           candidates=[dict(**BYTE_fixed(row, candidate), BYTE=rom[START + STRIDE * row + candidate])
                                       for candidate in range(ROW_BYTES)]) for row in range(ROW_COUNT)]
    return fields


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"rows"}, "AI selection package")
    for key, value in fixed.items():
        same(fields[key], value, "package." + key)
    result = []
    for row, entry in enumerate(exact_list(fields["rows"], ROW_COUNT, "physical rows")):
        pinned = row_fixed(row)
        keys(entry, set(pinned) | {"candidates"}, "row")
        for key, value in pinned.items():
            same(entry[key], value, "row." + key)
        raw = bytearray()
        for candidate, item in enumerate(exact_list(entry["candidates"], ROW_BYTES, "physical row BYTEs")):
            pinned_BYTE = BYTE_fixed(row, candidate)
            keys(item, set(pinned_BYTE) | {"BYTE"}, "candidate BYTE")
            for key, value in pinned_BYTE.items():
                same(item[key], value, "BYTE." + key)
            raw.append(uint(item["BYTE"], 255, "full parameter BYTE"))
        result.append(dict(id=ident(row), start=pinned["start"], end=pinned["end"], data=bytes(raw),
                           role="candidate_reverse_AI_selection_full_BYTE_row"))
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES:
        raise ValueError("fixed 196-BYTE cost differs")
    if any(left["end"] + 2 != right["start"] for left, right in zip(result, result[1:])):
        raise ValueError("fixed stride gap topology differs")
    return result


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def row_cursor(selector_WORD):
    """Wrap the WORD shift first, then sign ADDA.W; preserve the full input WORD."""
    uint(selector_WORD, 0xFFFF, "row selector WORD")
    shifted = (selector_WORD << 4) & 0xFFFF
    signed = shifted - 0x10000 if shifted & 0x8000 else shifted
    return dict(selector_WORD=selector_WORD, shifted_WORD=shifted, signed_offset=signed,
                initial_cursor=(INITIAL_CURSOR + signed) & 0xFFFFFFFF)


def lookup(image, selector_WORD):
    """Ordered ROM reads only; downstream RAM gates are documented, not simulated."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires a complete bytes image")
    result = row_cursor(selector_WORD)
    cursor = result["initial_cursor"]
    reads = []
    for candidate in range(13, -1, -1):
        cursor = (cursor - 1) & 0xFFFFFFFF
        BYTE = image[cursor]
        reads.append(dict(candidate_index=candidate, address=cursor, BYTE=BYTE,
                          passes_unsigned_BYTE_gate=BYTE <= 1))
    result.update(final_cursor=cursor, reads=reads, downstream_RAM_gates_simulated=False)
    return result


def schema():
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def exact(items):
        return dict(type="array", prefixItems=items, items=False, minItems=len(items), maxItems=len(items))
    def fixed(value):
        if type(value) is dict:
            return obj({key: fixed(item) for key, item in value.items()})
        if type(value) is list:
            return exact([fixed(item) for item in value])
        return dict(type={str: "string", int: "integer", bool: "boolean"}[type(value)], const=value)
    properties = {key: fixed(value) for key, value in metadata().items()}
    rows = []
    for row in range(ROW_COUNT):
        entry = {key: fixed(value) for key, value in row_fixed(row).items()}
        entry["candidates"] = exact([obj({**{key: fixed(value) for key, value in BYTE_fixed(row, candidate).items()},
                                          "BYTE": dict(type="integer", minimum=0, maximum=255)}) for candidate in range(ROW_BYTES)])
        rows.append(obj(entry))
    properties["rows"] = exact(rows)
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Fourteen original 14-BYTE physical rows; 2-BYTE gaps do not emit and full selector WORDs are never clamped."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("whole-ROM serialized field roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=ROW_COUNT,
                  whole_ROM_exact=True, whole_ROM_sha256=sha(image),
                  original_row_hex=[row["data"].hex() for row in encoded],
                  gap_BYTEs_retained=[dict(start=row["start"], end=row["end"], hex=rom[row["start"]:row["end"]].hex(),
                                          physical_emit=False) for row in gaps()],
                  selector_diagnostics={f"0x{selector:04X}": lookup(rom, selector) for selector in (0, 13, 14, 0x0800, 0x1000, 0xFFFF)},
                  blocks=[{key: value for key, value in row.items() if key != "data"}
                          | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=ROW_COUNT,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in ai_selection_fields build scope or the exact formal bundle")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "import", "verify"))
    parser.add_argument("--rom", default=str(DEFAULT_ROM))
    parser.add_argument("--fields")
    parser.add_argument("--bundle")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    target = None
    if args.command == "export":
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError("export requires a fresh output only")
        target = fresh_output(args.output, bundle=True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None:
            raise ValueError("import requires fields and fresh output")
        target = fresh_output(args.output)
        if target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.bundle is not None and args.fields is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom = read_bounded(args.rom, ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            put(target / name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES,
                      members={name: sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        members = render_bundle(rom)
        for name, data in members.items():
            if read_bounded(bundle / name, MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=EDITABLE_BYTES,
                      whole_ROM_exact=True, whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=EDITABLE_BYTES,
                      exact_canonical=image == rom, bytes=len(image), sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
