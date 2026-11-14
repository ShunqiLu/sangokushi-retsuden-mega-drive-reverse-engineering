"""Nineteen literal battle-outcome mask BYTEs, with the original special bypass.

This packet owns no CPU clamp, RNG or full battle-outcome algorithm. Five
physical editor groups contain four BYTEs except the fourth group's selector 2,
which bypasses this direct mask consumer. Other signed aliases can read that
excluded BYTE and remain available in diagnostics without becoming editable.
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
OUTPUT_ROOT = ROOT / "build/battle_outcome_masks"
FORMAL_ROOT = ROOT / "analysis/battle_outcome_masks/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
START, END, EXCLUDED = 0x041EF4, 0x041F08, 0x041F02
EDITABLE_BYTES = 19
FORMAT = "g5510-battle-outcome-conditional-BYTE-masks-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
BASES = (0x041EF4, 0x041EF8, 0x041EFC, 0x041F00, 0x041F04)
SELECTORS = ((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 3), (0, 1, 2, 3))
RANGES = ((START, EXCLUDED), (EXCLUDED + 1, END))
# Full original mask-stage bodies; the shared action tail and preconditions
# include calls, and are documented rather than simulated by this resource.
BODIES = (
    (0x041DDE, 0x041E1E, reference_value(__name__, 'BODIES')),
    (0x041E1E, 0x041E4C, reference_value(__name__, 'BODIES_2')),
    (0x041E4C, 0x041E76, reference_value(__name__, 'BODIES_3')),
    (0x041E76, 0x041EB6, reference_value(__name__, 'BODIES_4')),
    (0x041EB6, 0x041EF4, reference_value(__name__, 'BODIES_5')),
)
LEAS = ((0x041DF8, 0x00FA), (0x041E3C, 0x00BA), (0x041E66, 0x0094),
        (0x041EA6, 0x0058), (0x041EE4, 0x001E))
READS = (0x041DFE, 0x041E42, 0x041E6C, 0x041EAC, 0x041EEA)
INSTRUCTIONS = (
    (0x041DC8, "61000014"), (0x041DCC, "61000050"), (0x041DD0, "6100007a"),
    (0x041DD4, "610000a0"), (0x041DD8, "610000dc"), (0x041DDC, "4e75"),
    (0x041DF4, "3238efd2"), (0x041DF8, "41fa00fa"), (0x041DFE, "c0301000"),
    (0x041E38, "3238efd2"), (0x041E3C, "41fa00ba"), (0x041E42, "c0301000"),
    (0x041E62, "3238efd2"), (0x041E66, "41fa0094"), (0x041E6C, "c0301000"),
    (0x041E8E, "3238efd2"), (0x041E92, "0c410002"), (0x041E96, "660e"),
    (0x041E98, "02400007"), (0x041E9C, "0c400005"), (0x041EA0, "6500ff62"),
    (0x041EA6, "41fa0058"), (0x041EAC, "c0301000"),
    (0x041EE0, "3238efd2"), (0x041EE4, "41fa001e"), (0x041EEA, "c0301000"),
)
EVIDENCE_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
EVIDENCE_SHA256 = reference_value(__name__, 'EVIDENCE_SHA256')
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    for start, end, digest in BODIES:
        if sha(rom[start:end]) != digest:
            raise ValueError("pinned complete original mask consumer differs")
    for address, raw in INSTRUCTIONS:
        if rom[address:address + len(raw) // 2] != bytes.fromhex(raw):
            raise ValueError("pinned original consumer instruction differs")


def metadata():
    return dict(
        format=FORMAT, confidence="candidate", physical_format_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(container_start=START, container_end=END, emit_BYTES=19,
                            ranges=[dict(start=start, end=end, bytes=end-start) for start, end in RANGES],
                            physical_group_count=5, physical_capacity_is_CPU_clamp=False,
                            excluded_BYTE=dict(address=EXCLUDED, original_BYTE=1,
                                               physical_emit=False, role="fourth direct mask stage bypasses selector 2; other aliases may read")),
        evidence=dict(
            source="canonical consumer bytes + existing enhanced instruction CSV",
            original_ledger=dict(path=EVIDENCE_PATH, sha256=EVIDENCE_SHA256,
                                 original_reachability_confidence="heuristic", runtime_file_read=False),
            bodies=[dict(start=start, end=end, bytes=end-start, sha256=digest) for start, end, digest in BODIES],
            instructions=[dict(address=address, bytes=raw) for address, raw in INSTRUCTIONS],
            consumers=[dict(physical_group=index, LEA_address=lea, PC_base=lea+2,
                            displacement_WORD=displacement, effective_base=BASES[index],
                            AND_BYTE_address=READS[index], selector_RAM=0xFFEFD2,
                            index="signed full D1.W, without CPU clamp")
                       for index, (lea, displacement) in enumerate(LEAS)],
            special_path=dict(physical_group=3, selector_WORD=2, compare=0x041E92,
                              branch=0x041E96, ANDI_WORD_address=0x041E98, immediate_mask=7,
                              compare_WORD_address=0x041E9C, unsigned_less_than=5,
                              branch_to_shared_action=0x041EA0, shared_action=0x041E04,
                              mask_BYTE_read=False),
            alias_example=dict(physical_group=4, selector_WORD=0xFFFE, address=EXCLUDED,
                               excluded_from_edit=True, CPU_BYTE_read=True)),
        parameter_business_meaning="unknown", consumer_reachability_confidence="heuristic",
        edited_gameplay_safety="unknown", complete_battle_outcome_algorithm=False,
        independent_CPU_comparison=False,
    )


def group_fixed(group):
    return dict(id=f"battle_mask_stage_{group:02d}", physical_group=group, base=BASES[group])


def BYTE_fixed(group, selector):
    return dict(id=f"battle_mask_stage_{group:02d}_slot_{selector}",
                physical_selector=selector, address=BASES[group] + selector)


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result["groups"] = [dict(**group_fixed(group),
                             masks=[dict(**BYTE_fixed(group, selector), BYTE=rom[BASES[group]+selector])
                                    for selector in SELECTORS[group]]) for group in range(5)]
    return result


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"groups"}, "battle mask package")
    for key, value in fixed.items():
        same(fields[key], value, "package." + key)
    literals = {}
    for group, entry in enumerate(exact_list(fields["groups"], 5, "physical mask groups")):
        pinned = group_fixed(group)
        keys(entry, set(pinned) | {"masks"}, "mask group")
        for key, value in pinned.items():
            same(entry[key], value, "group." + key)
        for selector, item in zip(SELECTORS[group], exact_list(entry["masks"], len(SELECTORS[group]), "physical mask slots")):
            pinned_BYTE = BYTE_fixed(group, selector)
            keys(item, set(pinned_BYTE) | {"BYTE"}, "mask BYTE")
            for key, value in pinned_BYTE.items():
                same(item[key], value, "mask." + key)
            literals[BASES[group]+selector] = uint(item["BYTE"], 255, "full mask BYTE")
    if len(literals) != 19 or EXCLUDED in literals:
        raise ValueError("fixed physical BYTE scope differs")
    return [dict(id=f"rom_{start:06X}_battle_outcome_mask_BYTEs", start=start, end=end,
                 data=bytes(literals[address] for address in range(start, end)),
                 role="confirmed_physical_conditional_battle_mask_full_BYTEs") for start, end in RANGES]


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def read_address(group, selector_WORD):
    """Actual mask-stage address; None means the fourth-stage selector-2 bypass."""
    uint(group, 4, "physical consumer group")
    uint(selector_WORD, 0xFFFF, "selector WORD")
    if group == 3 and selector_WORD == 2:
        return None
    signed = selector_WORD - 0x10000 if selector_WORD & 0x8000 else selector_WORD
    return BASES[group] + signed


def mask_stage(image, group, selector_WORD, input_D0_LONG):
    """Narrow post-precondition mask stage, not helpers, RNG or whole battle logic."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic mask stage requires complete bytes image")
    uint(input_D0_LONG, 0xFFFFFFFF, "input D0 LONG")
    address = read_address(group, selector_WORD)
    if address is None:
        result = (input_D0_LONG & 0xFFFF0000) | (input_D0_LONG & 7)
        return dict(group=group, selector_WORD=selector_WORD, mask_BYTE_read=False,
                    D0_LONG=result, shared_action_if=(result & 0xFFFF) < 5)
    BYTE = image[address]
    result = (input_D0_LONG & 0xFFFFFF00) | ((input_D0_LONG & 0xFF) & BYTE)
    return dict(group=group, selector_WORD=selector_WORD, mask_BYTE_read=True,
                address=address, mask_BYTE=BYTE, D0_LONG=result,
                shared_action_if=(result & 0xFF) == 0,
                inside_physical_edit_scope=any(start <= address < end for start, end in RANGES))


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
    properties["groups"] = exact([obj({**{key: fixed(value) for key, value in group_fixed(group).items()},
        "masks": exact([obj({**{key: fixed(value) for key, value in BYTE_fixed(group, selector).items()},
                             "BYTE": dict(type="integer", minimum=0, maximum=255)}) for selector in SELECTORS[group]])})
                                  for group in range(5)])
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "19 fixed physical BYTEs; fourth direct consumer bypasses selector 2, while signed aliases remain unclamped."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("whole-ROM serialized fields roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=19, physical_blocks=2,
                  whole_ROM_exact=True, whole_ROM_sha256=sha(image),
                  original_group_BYTEs=[[item["BYTE"] for item in group["masks"]] for group in fields["groups"]],
                  excluded_BYTE_unchanged=image[EXCLUDED] == rom[EXCLUDED],
                  selector_diagnostics=[mask_stage(rom, group, selector, 0x1234ABFF)
                                        for group, selector in ((3, 2), (4, 0xFFFE), (0, 14), (1, 0xFFFF), (0, 4))],
                  blocks=[{key: value for key, value in row.items() if key != "data"}
                          | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=19, physical_blocks=2,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in battle_outcome_masks build scope or exact formal bundle")
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
