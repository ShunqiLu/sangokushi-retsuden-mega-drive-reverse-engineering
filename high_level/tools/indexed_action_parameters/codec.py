"""Lossless original 7 x 6 x 4 WORD table, with narrow original read diagnostics.

Full consumer construction closes exactly 336 source bytes. The diagnostic
accepts the observed WORD at F61C after the original RNG call, not a RNG seed.
It neither executes that RNG nor simulates preconditions, RAM or downstream
dispatch. All literal WORDs remain editable without a fabricated value enum.
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
OUTPUT_ROOT = ROOT / "build/indexed_action_parameters"
FORMAL_ROOT = ROOT / "analysis/indexed_action_parameters/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
START, END, EDITABLE_BYTES = 0x010B24, 0x010C74, 336
ROWS, SUBROWS, COLUMNS = 7, 6, 4
ROW_STRIDE, SUBROW_STRIDE = 48, 8
PRIMARY_THRESHOLDS = (50, 100, 150, 200, 250, 300)
SECONDARY_THRESHOLDS = (30, 60, 80, 90, 100)
ID = "rom_010B24_indexed_action_full_WORDs"
FORMAT = "g5510-indexed-action-full-WORD-table-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
SECTIONS = (
    (0x010ADE, 0x010B24, reference_value(__name__, 'SECTIONS'), "primary_unsigned_bucket_and_A0"),
    (0x010C74, 0x010D0C, reference_value(__name__, 'SECTIONS_2'), "first_complete_consumer"),
    (0x010F92, 0x011080, reference_value(__name__, 'SECTIONS_3'), "second_complete_consumer_with_shared_tail"),
    (0x0083D4, 0x0083FA, reference_value(__name__, 'SECTIONS_4'), "original_RNG_callee_not_simulated"),
)
INSTRUCTIONS = (
    (0x010A98, "61000044"), (0x010A9C, "610001d6"),
    (0x010F2E, "6100fbae"), (0x010F32, "6100005e"),
    (0x0330A6, "4eb900010ade"), (0x0330AC, "4eb900010c74"),
    (0x010ADE, "4243"), (0x010B12, "3803"), (0x010B14, "e34b"),
    (0x010B16, "d644"), (0x010B18, "e94b"), (0x010B1A, "41fa0008"),
    (0x010B20, "d0c3"), (0x010B22, "4e75"),
    (0x010CCC, "e74a"), (0x010CCE, "4eb9000083d4"), (0x010CD4, "7000"),
    (0x010CD6, "3038f61c"), (0x010CDA, "e588"), (0x010CDC, "4840"),
    (0x010CDE, "e348"), (0x010CE0, "d440"), (0x010CE2, "30302000"),
    (0x010D0A, "4e75"), (0x010FA6, "6300fd24"), (0x010FCC, "e74a"),
    (0x010FCE, "4eb9000083d4"), (0x010FD4, "7000"), (0x010FD6, "3038f61c"),
    (0x010FDA, "e588"), (0x010FDC, "4840"), (0x010FDE, "e348"),
    (0x010FE0, "d440"), (0x010FE2, "4a702000"), (0x01107E, "4e75"),
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
    for start, end, digest, _ in SECTIONS:
        if sha(rom[start:end]) != digest:
            raise ValueError("pinned complete original consumer section differs")
    for address, raw in INSTRUCTIONS:
        if rom[address:address + len(raw) // 2] != bytes.fromhex(raw):
            raise ValueError("pinned original consumer instruction differs")


def metadata():
    return dict(
        format=FORMAT, confidence="candidate", physical_format_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(id=ID, start=START, end=END, bytes=336, WORDs=168,
                            rows=7, subrows=6, columns=4, row_stride_BYTES=48,
                            subrow_stride_BYTES=8, endianness="big",
                            physical_capacity_is_global_CPU_clamp=False),
        evidence=dict(
            source="complete original consumer bytes + existing enhanced instruction CSV",
            original_ledger=dict(path=EVIDENCE_PATH, sha256=EVIDENCE_SHA256,
                                 runtime_file_read=False, confidence="mixed runtime_reachable/heuristic"),
            sections=[dict(start=start, end=end, bytes=end-start, sha256=digest, role=role)
                      for start, end, digest, role in SECTIONS],
            instructions=[dict(address=address, bytes=raw) for address, raw in INSTRUCTIONS],
            primary_bucket=dict(entry=0x010ADE, input="full unsigned D2.W at producer entry",
                                thresholds=list(PRIMARY_THRESHOLDS), branch="BLS inclusive",
                                constructed_bucket_min=0, constructed_bucket_max=6,
                                result_offset="48 * bucket, computed with WORD arithmetic",
                                LEA=0x010B1A, PC_base=0x010B1C, displacement_WORD=8,
                                ADDA_WORD=0x010B20),
            secondary_bucket=dict(input="full unsigned WORD read from B600",
                                  thresholds=list(SECONDARY_THRESHOLDS), branch="BLS inclusive",
                                  constructed_bucket_min=0, constructed_bucket_max=5,
                                  offset="8 * bucket"),
            column=dict(input="full observed F61C WORD AFTER original RNG JSR",
                        original_RNG_entry=0x0083D4, RNG_reads_LONG_at_RAM=0xFFF61C,
                        RNG_writes_LONG_at_RAM=0xFFF61C, RNG_preserves_A0=True,
                        original_RNG_executed_by_this_API=False,
                        sequence="MOVEQ 0; MOVE.W F61C; LSL.L #2; SWAP; LSL.W #1",
                        low_WORD_result="2 * (post_RNG_F61C_WORD >> 14)",
                        columns_min=0, columns_max=3),
            consumers=[dict(entry=0x010C74, last_RTS=0x010D0A,
                            source_read=0x010CE2, operation="MOVE.W (A0,D2.W),D0"),
                       dict(entry=0x010F92, last_RTS=0x01107E,
                            source_read=0x010FE2, operation="TST.W (A0,D2.W)",
                            low_bucket_shared_branch=0x010FA6, target=0x010CCC,
                            low_bucket_reads=0x010CE2, low_bucket_operation="MOVE.W")],
            constructed_read_min=START, constructed_read_max=END-2,
            original_following_code=dict(address=END, first_WORD=0x3C07, physical_emit=False)),
        parameter_business_meaning="unknown", edited_gameplay_safety="unknown",
        complete_RAM_algorithm=False, natural_reachable_gameplay_domain="unknown",
        independent_CPU_comparison=False,
    )


def row_fixed(row):
    return dict(id=f"action_bucket_{row:02d}", physical_row=row,
                start=START + row * ROW_STRIDE, end=START + (row+1) * ROW_STRIDE)


def subrow_fixed(row, subrow):
    return dict(id=f"action_bucket_{row:02d}_subbucket_{subrow:02d}", physical_subrow=subrow,
                start=START + row*ROW_STRIDE + subrow*SUBROW_STRIDE)


def WORD_fixed(row, subrow, column):
    return dict(id=f"action_parameter_r{row:02d}_s{subrow:02d}_c{column:02d}",
                physical_column=column, address=START + row*ROW_STRIDE + subrow*SUBROW_STRIDE + 2*column)


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result["rows"] = [dict(**row_fixed(row), subrows=[dict(**subrow_fixed(row, subrow),
        columns=[dict(**WORD_fixed(row, subrow, column),
                      WORD=int.from_bytes(rom[START+48*row+8*subrow+2*column:START+48*row+8*subrow+2*column+2], "big"))
                 for column in range(COLUMNS)]) for subrow in range(SUBROWS)]) for row in range(ROWS)]
    return result


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"rows"}, "indexed action package")
    for key, value in fixed.items():
        same(fields[key], value, "package." + key)
    data = bytearray()
    for row, entry in enumerate(exact_list(fields["rows"], ROWS, "physical rows")):
        pinned = row_fixed(row)
        keys(entry, set(pinned) | {"subrows"}, "row")
        for key, value in pinned.items():
            same(entry[key], value, "row." + key)
        for subrow, inner in enumerate(exact_list(entry["subrows"], SUBROWS, "physical subrows")):
            pinned = subrow_fixed(row, subrow)
            keys(inner, set(pinned) | {"columns"}, "subrow")
            for key, value in pinned.items():
                same(inner[key], value, "subrow." + key)
            for column, item in enumerate(exact_list(inner["columns"], COLUMNS, "physical columns")):
                pinned = WORD_fixed(row, subrow, column)
                keys(item, set(pinned) | {"WORD"}, "parameter WORD")
                for key, value in pinned.items():
                    same(item[key], value, "WORD." + key)
                data.extend(uint(item["WORD"], 0xFFFF, "full parameter WORD").to_bytes(2, "big"))
    if len(data) != EDITABLE_BYTES:
        raise ValueError("fixed physical WORD cost differs")
    return [dict(id=ID, start=START, end=END, data=bytes(data),
                 role="confirmed_constructed_unsigned_bucket_indexed_full_WORDs")]


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def bucket(value_WORD, thresholds):
    uint(value_WORD, 0xFFFF, "full unsigned bucket input WORD")
    return sum(value_WORD > threshold for threshold in thresholds)


def column_from_post_rng_WORD(value_WORD):
    """Only the original post-call WORD-to-column arithmetic, not a seed or RNG."""
    return uint(value_WORD, 0xFFFF, "observed post-RNG F61C WORD") >> 14


def signed_WORD(value):
    uint(value, 0xFFFF, "index WORD")
    return value - 0x10000 if value & 0x8000 else value


def direct_read(image, row_D3_WORD, index_D2_WORD):
    """Two original signed indexed offsets; even code aliases are not clamped."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic read requires a complete bytes image")
    address = START + signed_WORD(row_D3_WORD) + signed_WORD(index_D2_WORD)
    if address & 1:
        raise ValueError("odd 68000 WORD address requires address-error exception; not simulated")
    WORD = int.from_bytes(image[address:address+2], "big")
    return dict(address=address, WORD=WORD, is_zero=WORD == 0,
                inside_physical_edit_scope=START <= address and address+2 <= END)


def lookup(image, primary_D2_WORD, B600_WORD, post_rng_F61C_WORD, consumer=0):
    """Construct a source read from observed inputs, without executing upstream RNG/RAM."""
    uint(consumer, 1, "consumer route")
    row = bucket(primary_D2_WORD, PRIMARY_THRESHOLDS)
    subrow = bucket(B600_WORD, SECONDARY_THRESHOLDS)
    column = column_from_post_rng_WORD(post_rng_F61C_WORD)
    result = direct_read(image, row*48, subrow*8+column*2)
    read_pc = 0x010CE2 if consumer == 0 or subrow == 0 else 0x010FE2
    result.update(primary_bucket=row, secondary_bucket=subrow, column=column,
                  post_rng_F61C_WORD=post_rng_F61C_WORD, source_read=read_pc,
                  operation="MOVE.W" if read_pc == 0x010CE2 else "TST.W",
                  upstream_RNG_simulated=False, downstream_dispatch_simulated=False)
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
    properties["rows"] = exact([obj({**{key: fixed(value) for key, value in row_fixed(row).items()},
        "subrows": exact([obj({**{key: fixed(value) for key, value in subrow_fixed(row, subrow).items()},
            "columns": exact([obj({**{key: fixed(value) for key, value in WORD_fixed(row, subrow, column).items()},
                "WORD": dict(type="integer", minimum=0, maximum=0xFFFF)}) for column in range(COLUMNS)])})
                         for subrow in range(SUBROWS)])}) for row in range(ROWS)])
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Original full WORD literals in 7x6x4 constructed read scope; post-RNG WORD input is not a RNG seed."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("whole-ROM serialized fields roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=336, physical_blocks=1,
                  whole_ROM_exact=True, whole_ROM_sha256=sha(image),
                  source_table_sha256=sha(rom[START:END]),
                  original_WORDs=[int.from_bytes(rom[a:a+2], "big") for a in range(START, END, 2)],
                  literal_zero_WORDs=sum(rom[a:a+2] == bytes(2) for a in range(START, END, 2)),
                  zero_words_have_constructed_read_evidence=True,
                  narrow_diagnostics=[lookup(rom, a, b, seed, consumer)
                                      for a, b, seed, consumer in ((0, 0, 0, 0), (0xFFFF, 0xFFFF, 0xFFFF, 0),
                                                                 (300, 30, 0x8000, 1), (301, 31, 0xC000, 1))],
                  excluded_code_alias=direct_read(rom, 336, 0),
                  blocks=[{key: value for key, value in row.items() if key != "data"}
                          | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=336, physical_blocks=1,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in indexed_action_parameters build scope or exact formal bundle")
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
        result = dict(path=str(target), editable_bytes=336, members={name: sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name, data in render_bundle(rom).items():
            if read_bounded(bundle / name, MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=336,
                      whole_ROM_exact=True, whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=336,
                      exact_canonical=image == rom, bytes=len(image), sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
