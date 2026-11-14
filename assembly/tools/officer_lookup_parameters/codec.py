"""Lossless 12-BYTE officer lookup parameters, without invented selector clamps.

Only three original physical groups of four BYTEs are editable. Diagnostic
lookups read original or edited images at real addresses, including code aliases.
The original 60-byte consumer evidence is pinned; no complete RAM algorithm is
claimed. Generic bounded JSON/path helpers reuse the frozen deployment package.
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
OUTPUT_ROOT = ROOT / "build/officer_lookup_parameters"
FORMAL_ROOT = ROOT / "analysis/officer_lookup_parameters/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 12
START, END = 0x01F910, 0x01F91C
BLOCK_ID = "rom_01F910_officer_lookup_parameters"
FORMAT = "g5510-officer-lookup-fixed-BYTE-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
CONSUMER_START, CONSUMER_END = 0x01F8D4, 0x01F910
CONSUMER_SHA256 = reference_value(__name__, 'CONSUMER_SHA256')
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
INSTRUCTIONS = (
    (0x01F8D4, "3200"), (0x01F8D6, "e349"), (0x01F8D8, "d240"),
    (0x01F8DA, "4dfa0034"), (0x01F8DE, "4243"), (0x01F8E0, "4242"),
    (0x01F8E2, "14351000"), (0x01F8E6, "16362000"),
    (0x01F8EA, "584e"), (0x01F8EC, "14351001"),
    (0x01F8F0, "b6362000"), (0x01F8F4, "64000006"), (0x01F8F8, "16362000"),
    (0x01F8FC, "584e"), (0x01F8FE, "14351002"),
    (0x01F902, "b6362000"), (0x01F906, "64000006"), (0x01F90A, "16362000"),
    (0x01F90E, "4e75"),
)
CALLS = ((0x01B730, "610041a2"), (0x01B76E, "61004164"),
         (0x01F804, "610000ce"), (0x01F842, "61000090"))
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    if sha(rom[CONSUMER_START:CONSUMER_END]) != CONSUMER_SHA256:
        raise ValueError("pinned original consumer bytes differ")
    for address, raw in CALLS:
        if rom[address:address + 4] != bytes.fromhex(raw):
            raise ValueError("pinned original direct call differs")


def metadata():
    return dict(
        format=FORMAT, confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(id=BLOCK_ID, start=START, end=END, bytes=EDITABLE_BYTES,
                            groups=3, BYTEs_per_group=4),
        evidence=dict(
            confidence="confirmed", source="canonical consumer bytes + existing enhanced instruction table",
            enhanced_source=dict(path=ENHANCED_PATH, sha256=ENHANCED_SHA256,
                                 original_confidence="heuristic", runtime_reachability="candidate"),
            consumer=dict(start=CONSUMER_START, end=CONSUMER_END, bytes=60, sha256=CONSUMER_SHA256),
            instructions=[dict(address=address, bytes=raw, original_confidence="heuristic")
                          for address, raw in INSTRUCTIONS],
            direct_calls=[dict(address=address, bytes=raw, PC_base=address + 2,
                               destination=CONSUMER_START) for address, raw in CALLS],
            first_call_source=dict(LEA_address=0x01B71E, bytes="4bf8ea88", A5_RAM=0xFFEA88,
                                   applies_to_calls=[0x01B730, 0x01B76E]),
            lookup_base=dict(LEA_address=0x01F8DA, bytes="4dfa0034", PC_base=0x01F8DC,
                             displacement_WORD=0x0034, effective_base=START),
            source_index=dict(D1_WORD="(3 * D0.WORD) & 0xFFFF", index_interpretation="signed D1.W",
                              source_displacements=[0, 1, 2],
                              address_rule="A5 + signed(D1.W) + displacement; do not sign after adding displacement"),
            selector=dict(clear_D2_WORD=0x01F8E0, load_width="BYTE", minimum=0, maximum=255,
                          physical_items_per_group=4, CPU_clamp=False,
                          lookup_rule="01F910 + 4*group + selector_BYTE"),
            maximum=dict(clear_D3_WORD=0x01F8DE, initial_read=0x01F8E6,
                         group_advances=[0x01F8EA, 0x01F8FC],
                         compare_BYTE=[0x01F8F0, 0x01F902],
                         BCC_addresses=[0x01F8F4, 0x01F906],
                         reread_if_carry=[0x01F8F8, 0x01F90A],
                         retained_operation="unsigned BYTE maximum of three actual lookup results",
                         complete_RAM_algorithm=False)),
        natural_parameter_semantics="unknown", edited_gameplay_safety="unknown",
        independent_CPU_comparison=False,
    )


def group_fixed(index):
    return dict(id=f"officer_lookup_group_{index}", index=index,
                start=START + 4 * index, end=START + 4 * (index + 1))


def entry_fixed(group, index):
    return dict(id=f"officer_lookup_g{group}_item_{index}", index=index,
                address=START + 4 * group + index)


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["groups"] = [dict(**group_fixed(group),
                             entries=[dict(**entry_fixed(group, index), BYTE=rom[START + 4 * group + index])
                                      for index in range(4)]) for group in range(3)]
    return fields


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"groups"}, "officer lookup package")
    for key, value in fixed.items():
        same(fields[key], value, "package." + key)
    raw = bytearray()
    for group, row in enumerate(exact_list(fields["groups"], 3, "physical groups")):
        pinned = group_fixed(group)
        keys(row, set(pinned) | {"entries"}, "group")
        for key, value in pinned.items():
            same(row[key], value, "group." + key)
        for index, entry in enumerate(exact_list(row["entries"], 4, "physical group entries")):
            pinned_entry = entry_fixed(group, index)
            keys(entry, set(pinned_entry) | {"BYTE"}, "group entry")
            for key, value in pinned_entry.items():
                same(entry[key], value, "entry." + key)
            raw.append(uint(entry["BYTE"], 255, "parameter BYTE"))
    if len(raw) != EDITABLE_BYTES:
        raise ValueError("fixed 12-BYTE encoded cost differs")
    return [dict(id=BLOCK_ID, start=START, end=END, data=bytes(raw),
                 role="confirmed_physical_officer_lookup_BYTE_parameters")]


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def source_offsets(d0_WORD):
    """Three source offsets: sign the wrapped D1.W before BYTE displacements."""
    uint(d0_WORD, 0xFFFF, "D0.W")
    d1_WORD = (3 * d0_WORD) & 0xFFFF
    signed = d1_WORD - 0x10000 if d1_WORD & 0x8000 else d1_WORD
    return tuple(signed + displacement for displacement in (0, 1, 2))


def lookup_address(group, selector_BYTE):
    """The group index selects a diagnostic base, never clamps the BYTE selector."""
    uint(group, 2, "diagnostic group")
    uint(selector_BYTE, 255, "selector BYTE")
    return START + 4 * group + selector_BYTE


def lookup(image, group, selector_BYTE):
    """Read the actual BYTE, including code aliases, from original or edited ROM."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires a complete bytes image")
    return image[lookup_address(group, selector_BYTE)]


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
    groups = []
    for group in range(3):
        row = {key: fixed(value) for key, value in group_fixed(group).items()}
        row["entries"] = exact([obj({**{key: fixed(value) for key, value in entry_fixed(group, index).items()},
                                     "BYTE": dict(type="integer", minimum=0, maximum=255)}) for index in range(4)])
        groups.append(obj(row))
    properties["groups"] = exact(groups)
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Three physical groups of four full BYTEs; no CPU selector clamp or reconstructed natural domain."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("whole-ROM serialized field roundtrip differs")
    encoded = blocks(rom, fields)[0]
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
                  group_count=3, physical_BYTEs_per_group=4,
                  original_group_hex=[rom[START + 4 * group:START + 4 * (group + 1)].hex() for group in range(3)],
                  whole_ROM_exact=True, whole_ROM_sha256=sha(image),
                  selector_4_addresses=[lookup_address(group, 4) for group in range(3)],
                  selector_255_addresses=[lookup_address(group, 255) for group in range(3)],
                  post_editor_code_alias=dict(address=END, original_bytes=rom[END:END + 4].hex(),
                                              group2_selector4_BYTE=lookup(rom, 2, 4), physical_emit=False),
                  source_D0_D555_offsets=list(source_offsets(0xD555)),
                  blocks=[{key: value for key, value in encoded.items() if key != "data"}
                          | dict(bytes=len(encoded["data"]), sha256=sha(encoded["data"]))])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in officer_lookup_parameters build scope or the exact formal bundle")
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
