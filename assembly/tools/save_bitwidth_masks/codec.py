"""Lossless original BE32 masks shared by the SRAM bit packer and reader.

The 33 physical editor slots do not clamp the original full WORD selector.
Fields come from literal ROM LONGs, never a replacement mask formula. All
LONG values are editable without changing allocation or claiming save safety.
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
OUTPUT_ROOT = ROOT / "build/save_bitwidth_masks"
FORMAL_ROOT = ROOT / "analysis/save_bitwidth_masks/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
START, END, COUNT = 0x00929A, 0x00931E, 33
EDITABLE_BYTES = 132
ID = "rom_00929A_save_bitwidth_BE32_masks"
FORMAT = "g5510-save-bitwidth-BE32-masks-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
CONSUMERS = (
    (0x00922A, 0x00929A, reference_value(__name__, 'CONSUMERS'), "runtime_confirmed"),
    (0x00931E, 0x009390, reference_value(__name__, 'CONSUMERS_2'), "runtime_reachable"),
)
INSTRUCTIONS = (
    (0x009230, "45fa0068"), (0x009234, "3a00"), (0x009236, "e54d"),
    (0x009238, "2a325000"), (0x00926A, "ce85"), (0x009298, "4e75"),
    (0x009324, "45faff74"), (0x009328, "3a00"), (0x00932A, "e54d"),
    (0x00932C, "2a325000"), (0x009376, "ce85"), (0x00938E, "4e75"),
    (0x008478, "61000db0"), (0x008AE2, "6100083a"),
)
EVIDENCE = (
    ("analysis/save_data/SRAM_SAVE_FORMAT.md", reference_value(__name__, 'EVIDENCE')),
    ("analysis/runtime/save_record.md", reference_value(__name__, 'EVIDENCE_2')),
    ("analysis/save_data/generated/fixed_segments.csv", reference_value(__name__, 'EVIDENCE_3')),
    ("analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv", reference_value(__name__, 'EVIDENCE_4')),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    for start, end, digest, _ in CONSUMERS:
        if sha(rom[start:end]) != digest:
            raise ValueError("pinned complete original SRAM consumer differs")
    for address, raw in INSTRUCTIONS:
        if rom[address:address + len(raw) // 2] != bytes.fromhex(raw):
            raise ValueError("pinned original consumer instruction differs")


def metadata():
    return dict(
        format=FORMAT, confidence="confirmed", physical_format_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(id=ID, start=START, end=END, bytes=EDITABLE_BYTES,
                            slots=COUNT, bytes_per_slot=4, endianness="big",
                            physical_capacity_is_CPU_clamp=False),
        evidence=dict(
            source="canonical literal LONGs + complete original consumer bytes + existing save evidence",
            documents=[dict(path=path, sha256=digest, runtime_file_read=False) for path, digest in EVIDENCE],
            consumers=[dict(start=start, end=end, bytes=end-start, sha256=digest,
                            original_reachability_confidence=confidence)
                       for start, end, digest, confidence in CONSUMERS],
            instructions=[dict(address=address, bytes=raw) for address, raw in INSTRUCTIONS],
            addressing=[dict(LEA_address=0x009230, PC_base=0x009232,
                             displacement_WORD=0x0068, effective_base=START,
                             indexed_LONG_read=0x009238, AND_LONG_address=0x00926A),
                        dict(LEA_address=0x009324, PC_base=0x009326,
                             displacement_WORD=0xFF74, effective_base=START,
                             indexed_LONG_read=0x00932C, AND_LONG_address=0x009376)],
            index_rule="signed_WORD((D0_WORD << 2) & 0xFFFF); full selector WORD, no CPU clamp",
            old_fixed_generic_segments=46,
            old_fixed_segment_widths=[1, 2, 4, 5, 6, 7, 8, 9, 10, 14, 17, 18, 20],
            runtime_scope="original controlled save executes packer; not every table slot was runtime observed",
            literal_table_role="low-bit masks indexed by original field bit width",
            original_width_zero_LONG=0, original_width_32_LONG=0xFFFFFFFF,
            alias_after_table=dict(selector_WORD=33, address=END,
                                   original_LONG=0x53424243, is_code=True, physical_emit=False)),
        edited_values_need_not_equal_low_bit_formula=True,
        edited_save_compatibility="unknown", complete_SRAM_algorithm=False,
        independent_CPU_comparison=False,
    )


def slot_fixed(index):
    return dict(id=f"save_width_mask_{index:02d}", physical_slot=index,
                original_bit_width_index=index, address=START + 4 * index)


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result["masks"] = [dict(**slot_fixed(index),
                            LONG=int.from_bytes(rom[START+4*index:START+4*index+4], "big"))
                       for index in range(COUNT)]
    return result


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"masks"}, "save mask package")
    for key, value in fixed.items():
        same(fields[key], value, "package." + key)
    data = bytearray()
    for index, slot in enumerate(exact_list(fields["masks"], COUNT, "physical mask slots")):
        pinned = slot_fixed(index)
        keys(slot, set(pinned) | {"LONG"}, "mask slot")
        for key, value in pinned.items():
            same(slot[key], value, "slot." + key)
        data.extend(uint(slot["LONG"], 0xFFFFFFFF, "full mask LONG").to_bytes(4, "big"))
    if len(data) != EDITABLE_BYTES:
        raise ValueError("fixed physical mask cost differs")
    return [dict(id=ID, start=START, end=END, data=bytes(data),
                 role="confirmed_original_SRAM_bitwidth_full_BE32_masks")]


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def read_address(selector_WORD):
    """Diagnostic original WORD shift/wrap and signed index; not an editor clamp."""
    uint(selector_WORD, 0xFFFF, "field width selector WORD")
    shifted = (selector_WORD << 2) & 0xFFFF
    signed = shifted - 0x10000 if shifted & 0x8000 else shifted
    return START + signed


def lookup(image, selector_WORD):
    """Read a literal LONG from any complete original/edited image, including code aliases."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires a complete bytes image")
    address = read_address(selector_WORD)
    return dict(selector_WORD=selector_WORD, address=address,
                LONG=int.from_bytes(image[address:address+4], "big"),
                inside_physical_edit_scope=START <= address and address + 4 <= END)


def masked_LONG(image, selector_WORD, input_LONG):
    """Narrow AND.L diagnostic only; does not simulate packing or unpacking RAM."""
    return uint(input_LONG, 0xFFFFFFFF, "input LONG") & lookup(image, selector_WORD)["LONG"]


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
    properties["masks"] = exact([obj({**{key: fixed(value) for key, value in slot_fixed(index).items()},
                                     "LONG": dict(type="integer", minimum=0, maximum=0xFFFFFFFF)})
                                  for index in range(COUNT)])
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "33 fixed physical BE32 masks; source literals, not formula-generated values or a CPU selector clamp."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("whole-ROM serialized fields roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
                  whole_ROM_exact=True, whole_ROM_sha256=sha(image),
                  original_masks=[slot["LONG"] for slot in fields["masks"]],
                  source_table_sha256=sha(rom[START:END]),
                  selector_diagnostics=[lookup(rom, value) for value in (0, 32, 33, 0x2000, 0x4000, 0xFFFF)],
                  blocks=[{key: value for key, value in row.items() if key != "data"}
                          | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in save_bitwidth_masks build scope or exact formal bundle")
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
