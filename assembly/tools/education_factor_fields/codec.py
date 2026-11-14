"""Lossless 25-BYTE grid selected by the original unsigned WORD thresholds.

The editable authority remains each complete BYTE. EXT.W views describe only
D2.W, not the whole CPU LONG register. Data APIs are pure; only the CLI reads
or writes files. Bounded JSON/path helpers reuse the frozen deployment package.
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
OUTPUT_ROOT = ROOT / "build/education_factor_fields"
FORMAL_ROOT = ROOT / "analysis/education_factor_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 25
START, END = 0x00E776, 0x00E78F
BLOCK_ID = "rom_00E776_education_factor_fields"
FORMAT = "g5510-education-factor-fixed-BYTE-grid-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
THRESHOLDS = (20, 40, 60, 80)
CONSUMER_START, CONSUMER_END = 0x00E71E, 0x00E776
CONSUMER_SHA256 = reference_value(__name__, 'CONSUMER_SHA256')
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
INSTRUCTIONS = (
    (0xE71E, "4243"), (0xE720, "0c410014"), (0xE724, "6522"),
    (0xE726, "363c0005"), (0xE72A, "0c410028"), (0xE72E, "6518"),
    (0xE730, "363c000a"), (0xE734, "0c41003c"), (0xE738, "650e"),
    (0xE73A, "363c000f"), (0xE73E, "0c410050"), (0xE742, "6504"),
    (0xE744, "363c0014"), (0xE748, "0c400014"), (0xE74C, "651a"),
    (0xE74E, "5243"), (0xE750, "0c400028"), (0xE754, "6512"),
    (0xE756, "5243"), (0xE758, "0c40003c"), (0xE75C, "650a"),
    (0xE75E, "5243"), (0xE760, "0c400050"), (0xE764, "6502"),
    (0xE766, "5243"), (0xE768, "41fa000c"), (0xE76C, "4e71"),
    (0xE76E, "14303000"), (0xE772, "4882"), (0xE774, "4e75"),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    if sha(rom[CONSUMER_START:CONSUMER_END]) != CONSUMER_SHA256:
        raise ValueError("pinned original consumer bytes differ")


def metadata():
    return dict(
        format=FORMAT, confidence="confirmed", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(id=BLOCK_ID, start=START, end=END, bytes=EDITABLE_BYTES,
                            rows=5, columns=5, order="row_D1_bucket then col_D0_bucket"),
        evidence=dict(
            confidence="confirmed", source="canonical consumer bytes + existing runtime-confirmed instruction rows",
            enhanced_source=dict(path=ENHANCED_PATH, sha256=ENHANCED_SHA256,
                                 original_confidence="runtime_confirmed", trace_label="defense_month"),
            consumer=dict(start=CONSUMER_START, end=CONSUMER_END, bytes=88, sha256=CONSUMER_SHA256),
            instructions=[dict(address=address, bytes=raw, original_confidence="runtime_confirmed")
                          for address, raw in INSTRUCTIONS],
            row_selector=dict(register="unsigned D1.W", compare_WORDs=list(THRESHOLDS),
                              CMP_addresses=[0xE720, 0xE72A, 0xE734, 0xE73E],
                              BCS_addresses=[0xE724, 0xE72E, 0xE738, 0xE742],
                              D3_WORD_row_offsets=[0, 5, 10, 15, 20]),
            column_selector=dict(register="unsigned D0.W", compare_WORDs=list(THRESHOLDS),
                                 CMP_addresses=[0xE748, 0xE750, 0xE758, 0xE760],
                                 BCS_addresses=[0xE74C, 0xE754, 0xE75C, 0xE764],
                                 ADDQ1_addresses=[0xE74E, 0xE756, 0xE75E, 0xE766]),
            selector_domain=dict(input_WORD_min=0, input_WORD_max=65535,
                                 index_rule="5*row_D1_bucket + col_D0_bucket",
                                 index_min=0, index_max=24),
            lookup_base=dict(LEA_address=0xE768, bytes="41fa000c", PC_base=0xE76A,
                             displacement_WORD=0x000C, effective_base=START),
            result=dict(read_address=0xE76E, bytes="14303000", original_width="BYTE",
                        EXT_W_address=0xE772, EXT_W_bytes="4882",
                        WORD_rule="BYTE if BYTE < 128 else BYTE | 0xFF00",
                        signed_WORD_rule="BYTE if BYTE < 128 else BYTE - 256",
                        modeled_register_width="D2.W only", D2_LONG_synthesized=False)),
        natural_bucket_business_names="unknown", edited_gameplay_safety="unknown",
        independent_CPU_comparison=False,
    )


def row_fixed(row):
    return dict(id=f"education_factor_row_{row}", row_D1_bucket=row,
                start=START + 5 * row, end=START + 5 * (row + 1))


def cell_fixed(row, column):
    index = 5 * row + column
    return dict(id=f"education_factor_r{row}_c{column}", row_D1_bucket=row,
                col_D0_bucket=column, index=index, address=START + index)


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["grid"] = [dict(**row_fixed(row),
                           cells=[dict(**cell_fixed(row, column), BYTE=rom[START + 5 * row + column])
                                  for column in range(5)]) for row in range(5)]
    return fields


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"grid"}, "education factor package")
    for key, value in fixed.items():
        same(fields[key], value, "package." + key)
    raw = bytearray()
    for row, entry in enumerate(exact_list(fields["grid"], 5, "physical grid rows")):
        pinned = row_fixed(row)
        keys(entry, set(pinned) | {"cells"}, "grid row")
        for key, value in pinned.items():
            same(entry[key], value, "row." + key)
        for column, cell in enumerate(exact_list(entry["cells"], 5, "physical grid columns")):
            pinned_cell = cell_fixed(row, column)
            keys(cell, set(pinned_cell) | {"BYTE"}, "grid cell")
            for key, value in pinned_cell.items():
                same(cell[key], value, "cell." + key)
            raw.append(uint(cell["BYTE"], 255, "full parameter BYTE"))
    if len(raw) != EDITABLE_BYTES:
        raise ValueError("fixed 25-BYTE encoded cost differs")
    return [dict(id=BLOCK_ID, start=START, end=END, data=bytes(raw),
                 role="confirmed_unsigned_WORD_selected_BYTE_factor_grid")]


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def bucket(word):
    """Original unsigned CMP.W/BCS classification for a complete input WORD."""
    uint(word, 0xFFFF, "unsigned selector WORD")
    return sum(word >= threshold for threshold in THRESHOLDS)


def lookup_index(d0_WORD, d1_WORD):
    return 5 * bucket(d1_WORD) + bucket(d0_WORD)


def WORD_view(BYTE):
    """Preserve the original BYTE and describe exactly EXT.W, never EXT.L."""
    uint(BYTE, 255, "full parameter BYTE")
    return dict(BYTE=BYTE, D2_WORD=BYTE if BYTE < 128 else BYTE | 0xFF00,
                signed_D2_WORD=BYTE if BYTE < 128 else BYTE - 256)


def lookup(image, d0_WORD, d1_WORD):
    """Read and extend the selected BYTE from a complete original or edited image."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires a complete bytes image")
    row, column = bucket(d1_WORD), bucket(d0_WORD)
    index = 5 * row + column
    return dict(row_D1_bucket=row, col_D0_bucket=column, index=index,
                address=START + index, **WORD_view(image[START + index]))


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
    for row in range(5):
        entry = {key: fixed(value) for key, value in row_fixed(row).items()}
        entry["cells"] = exact([obj({**{key: fixed(value) for key, value in cell_fixed(row, column).items()},
                                     "BYTE": dict(type="integer", minimum=0, maximum=255)}) for column in range(5)])
        rows.append(obj(entry))
    properties["grid"] = exact(rows)
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Fixed 5 by 5 original BYTE grid; numeric bucket indices have no invented business labels."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("whole-ROM serialized field roundtrip differs")
    encoded = blocks(rom, fields)[0]
    views = [dict(address=START + index, **WORD_view(rom[START + index])) for index in range(EDITABLE_BYTES)]
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
                  grid_rows=5, grid_columns=5, whole_ROM_exact=True, whole_ROM_sha256=sha(image),
                  original_grid_hex=rom[START:END].hex(),
                  original_BYTE_and_EXT_WORD_preview=views,
                  preview_is_editing_authority=False,
                  FFFF_selector_example=lookup(rom, 0xFFFF, 0xFFFF),
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
        raise ValueError("output must stay in education_factor_fields build scope or the exact formal bundle")
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
