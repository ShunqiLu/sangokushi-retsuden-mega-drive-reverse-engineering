"""Lossless marker source for the original canonical empty VDP WORD-RLE stream.

Only EE5EF is emitted. Neighbouring terrain bytes and directory pointers are
read live by diagnostics, never re-authored. Empty describes the canonical
image, not every permitted marker edit or a hard three-BYTE allocation stop.
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
OUTPUT_ROOT = ROOT / "build/vdp_empty_marker_fields"
FORMAL_ROOT = ROOT / "analysis/vdp_empty_marker_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
MAX_JSON = 1024 * 1024
FORMAT = "g5510-vdp-canonical-empty-marker-BYTE-source-v1"
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
EDITABLE_BYTES = 1
START, END = 0x0EE5EF, 0x0EE5F0
BLOCK_ID = "rom_0EE5EF_vdp_word_RLE_marker"
DIRECTORY_BASE = 0x0387BA
ALIASES = (76, 78, 79)
BASELINE_LAYOUT = reference_value(__name__, 'BASELINE_LAYOUT')
BODIES = (
    (0x039658, 0x03969A, reference_value(__name__, 'BODIES')),
    (0x03975E, 0x0397A2, reference_value(__name__, 'BODIES_2')),
    (0x03B2B0, 0x03B2D8, reference_value(__name__, 'BODIES_3')),
)
INSTRUCTIONS = (
    (0x03975E, "363900ff7026"), (0x039764, "e543"),
    (0x039766, "43faf052"), (0x03976A, "20713000"),
    (0x03976E, "6100fee8"), (0x039772, "303900ff7026"),
    (0x039778, "4dfaf220"), (0x03977C, "12360000"),
    (0x039780, "0c010001"), (0x039784, "6600001c"),
    (0x039788, "363900ff7026"), (0x03978E, "5243"),
    (0x039790, "e543"), (0x039792, "43faf026"),
    (0x039796, "20713000"), (0x03979E, "6100feb8"),
    (0x039660, "61001c4e"), (0x039664, "1218"),
    (0x039666, "1418"), (0x039668, "b202"),
    (0x03966A, "67000010"), (0x03966E, "1818"),
    (0x039670, "e142"), (0x039672, "1404"),
    (0x039674, "33c200c00000"), (0x03967A, "60ea"),
    (0x03967C, "7600"), (0x03967E, "1618"),
    (0x039680, "67000016"), (0x039684, "1818"),
    (0x039686, "1418"), (0x039688, "e144"),
    (0x03968A, "1802"), (0x03968C, "33c400c00000"),
    (0x039692, "51cbfff8"), (0x039696, "60ce"), (0x039698, "4e75"),
)
sha, dump = shared.sha, shared.dump
keys, same, uint = shared.keys, shared.same, shared.uint
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical original ROM bytes, size and SHA-256 required")
    for start, end, digest in BODIES:
        if sha(rom[start:end]) != digest:
            raise ValueError("original directory-reader/WORD-RLE/helper differs")
    for address, raw in INSTRUCTIONS:
        if rom[address:address + len(raw)//2] != bytes.fromhex(raw):
            raise ValueError("pinned original reader opcode differs")
    for alias in ALIASES:
        address = DIRECTORY_BASE + 4*alias
        if int.from_bytes(rom[address:address+4], "big") != START:
            raise ValueError("original empty-stream directory alias differs")


def metadata():
    return dict(
        format=FORMAT, confidence="confirmed_source_format",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(start=START, end=END, bytes=1, role="WORD_RLE_marker_BYTE",
                            marker_BYTE_full_range_editable=True),
        shared_dependency=dict(start=END, end=END+2, canonical_BYTES=[0, 0],
                               authority="world_resources.terrain_codes",
                               physically_emitted_here=False, edited_image_read_live=True),
        evidence=dict(
            original_ledger="analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv",
            original_ledger_sha256=reference_value(__name__, 'metadata'),
            bodies=[dict(start=a, end=b, sha256=digest) for a,b,digest in BODIES],
            instructions=[dict(address=a, bytes=raw) for a,raw in INSTRUCTIONS],
            directory_aliases=[dict(selector_WORD=i, LONG_address=DIRECTORY_BASE+4*i,
                                    original_LONG_target=START) for i in ALIASES],
            read_path=dict(selector_RAM=0xFF7026, load_PC=0x03975E,
                           shift_WORD_PC=0x039764, index="s16((selector.W << 2) & FFFF)",
                           directory_LEA_PC=0x039766, directory_PC_base=0x039768,
                           displacement_WORD=0xF052, directory_base=DIRECTORY_BASE,
                           LONG_read_PC=0x03976A, call_PC=0x03976E,
                           optional_next_selector_gate_read_PC=0x03977C,
                           optional_gate_base=0x03899A, optional_gate_equals_BYTE=1,
                           optional_next_selector_ADDQ_WORD_PC=0x03978E,
                           optional_LONG_read_PC=0x039796, optional_call_PC=0x03979E,
                           original_local_selector_clamp=False),
            grammar=dict(marker_read_PC=0x039664, first_payload_BYTE_read_PC=0x039666,
                         literal_low_BYTE_read_PC=0x03966E, count_BYTE_read_PC=0x03967E,
                         repeat_high_BYTE_read_PC=0x039684, repeat_low_BYTE_read_PC=0x039686,
                         terminator="marker BYTE followed by zero count BYTE",
                         nonzero_count_output_WORDs="count BYTE + 1 (DBRA)",
                         canonical_read_start=START, canonical_read_stop=END+2,
                         canonical_decoded_WORDs=0, read_stop_is_edited_allocation_clamp=False),
            raw_baseline=dict(layout_id=BASELINE_LAYOUT, bytes_added=1,
                              old_vdp_empty_stream_physical_emit_bytes=0)),
        natural_selector_76_78_79_writer="unknown",
        natural_selector_domain="unknown", edited_gameplay_safety="unknown",
        source_view_is_CPU_or_runtime_proof=False, independent_CPU_comparison=False,
    )


def marker_fixed():
    return dict(id=BLOCK_ID, address=START, role="first_BYTE_WORD_RLE_marker")


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(), marker=dict(**marker_fixed(), BYTE=rom[START]))


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"marker"}, "marker source package")
    for key,value in fixed.items():
        same(fields[key], value, "package."+key)
    pinned = marker_fixed()
    keys(fields["marker"], set(pinned) | {"BYTE"}, "marker")
    for key,value in pinned.items():
        same(fields["marker"][key], value, "marker."+key)
    data = bytes([uint(fields["marker"]["BYTE"], 255, "full marker BYTE")])
    return [dict(id=BLOCK_ID, start=START, end=END, data=data, role="confirmed_WORD_RLE_marker_BYTE_source")]


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def read_entry_source(image, selector_WORD, next_selector=False):
    """Live directory read-entry arithmetic, not the optional gate or natural domain."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("full edited ROM bytes required")
    uint(selector_WORD, 0xFFFF, "selector WORD")
    if type(next_selector) is not bool:
        raise ValueError("strict next-selector flag required")
    index = ((selector_WORD + int(next_selector)) << 2) & 0xFFFF
    signed = index - 0x10000 if index & 0x8000 else index
    address = DIRECTORY_BASE + signed
    target = int.from_bytes(image[address:address+4], "big")
    return dict(selector_WORD=selector_WORD, next_selector=next_selector,
                index_WORD=index, signed_index=signed, LONG_address=address,
                source_address=target, target_inside_ROM=0 <= target < ROM_SIZE,
                original_gate_entered=False, natural_read_admission=False)


def source_view(image, selector_WORD=76, next_selector=False, source_BYTE_budget=256, output_WORD_budget=8192):
    """Actual BYTE/BE16 grammar projection with explicit diagnostic resource bounds.

    No EE5F2 hard stop is imposed. Every consumed source BYTE is recorded with
    its original read PC, including partial commands when a budget/boundary ends.
    This excludes VDP timing, CPU registers/flags, interrupts and gameplay entry.
    """
    uint(source_BYTE_budget, ROM_SIZE, "source BYTE budget")
    uint(output_WORD_budget, 0x100000, "output WORD budget")
    entry = read_entry_source(image, selector_WORD, next_selector)
    cursor = entry["source_address"]
    reads, output, commands = [], [], []
    status = None

    def take(pc):
        nonlocal cursor, status
        if not 0 <= cursor < ROM_SIZE:
            status = "outside_supplied_ROM"
            return None
        if len(reads) >= source_BYTE_budget:
            status = "source_BYTE_budget_exhausted"
            return None
        value = image[cursor]
        reads.append(dict(address=cursor, BYTE=value, original_read_PC=pc,
                          inside_edit_scope=START <= cursor < END))
        cursor += 1
        return value

    marker = take(0x039664)
    while status is None:
        address = cursor
        first = take(0x039666)
        if status is not None:
            break
        if first == marker:
            count = take(0x03967E)
            if status is not None:
                break
            if count == 0:
                commands.append(dict(role="terminator", address=address, BYTE_count=2))
                status = "terminated_marker_zero"
                break
            high, low = take(0x039684), None
            if status is None:
                low = take(0x039686)
            if status is not None:
                break
            value, repeat = (high << 8) | low, count+1
            commands.append(dict(role="repeat", address=address, WORD=value,
                                 encoded_count_BYTE=count, output_WORD_count=repeat))
        else:
            low = take(0x03966E)
            if status is not None:
                break
            value, repeat = (first << 8) | low, 1
            commands.append(dict(role="literal", address=address, WORD=value, output_WORD_count=1))
        if len(output)+repeat > output_WORD_budget:
            output.extend([value]*max(0, output_WORD_budget-len(output)))
            status = "output_WORD_budget_exhausted"
            break
        output.extend([value]*repeat)
    return dict(**entry, marker_BYTE=marker, status=status, source_cursor=cursor,
                source_BYTE_count=len(reads), output_WORDs=output, commands=commands, source_reads=reads,
                source_BYTE_budget=source_BYTE_budget, output_WORD_budget=output_WORD_budget,
                canonical_empty_semantics=status == "terminated_marker_zero" and not output,
                source_budget_is_original_CPU_limit=False, output_budget_is_original_CPU_limit=False,
                whole_CPU_or_runtime_comparison=False)


def schema():
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({key:fixed(item) for key,item in value.items()})
        if type(value) is list:
            return dict(type="array", prefixItems=[fixed(item) for item in value], items=False,
                        minItems=len(value), maxItems=len(value))
        return dict(type={str:"string", int:"integer", bool:"boolean"}[type(value)], const=value)
    properties = {key:fixed(value) for key,value in metadata().items()}
    properties["marker"] = obj({**{key:fixed(value) for key,value in marker_fixed().items()},
                                 "BYTE":dict(type="integer", minimum=0, maximum=255)})
    return dict(**obj(properties), **{"$schema":"https://json-schema.org/draft/2020-12/schema"},
                description="One full marker BYTE; neighbour terrain is live dependency, not duplicate authority.")


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("whole-ROM marker serialized roundtrip differs")
    report = dict(**metadata(), editable_bytes=1, physical_blocks=1, whole_ROM_exact=True,
                  whole_ROM_sha256=sha(image), source_sha256=sha(rom[START:END]),
                  alias_views=[source_view(rom, selector) for selector in ALIASES])
    members = {"fields.json":serialized, "fields.schema.json":dump(schema()), "validation.json":dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=1, physical_blocks=1,
        members={name:dict(bytes=len(data), sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("dedicated marker build output or exact formal bundle required")
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
            raise ValueError("export requires fresh output only")
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
        for name,data in members.items():
            put(target/name, data)
        result = dict(path=str(target), editable_bytes=1, members={name:sha(data) for name,data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name, MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: "+name)
        result = dict(path=str(bundle), verified=True, editable_bytes=1, whole_ROM_exact=True,
                      whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=1,
                      exact_canonical=image == rom, bytes=len(image), sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
