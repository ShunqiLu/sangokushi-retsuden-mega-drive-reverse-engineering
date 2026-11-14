"""Lossless 20+6 actually-selected source bytes from original city-cycle tables.

Each editable value is the full original big-endian WORD, not a regenerated
formula or signed preview. Only expense slots0/1/4 are editable; slots2/3 remain
unknown. ANDI.W #5 selects offsets0/2/8/10, and offset10 reads code4484, unclamped.
Pure data APIs reuse only the frozen deployment package's bounded helpers.
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
OUTPUT_ROOT = ROOT / "build/city_cycle_parameters"
FORMAL_ROOT = ROOT / "analysis/city_cycle_parameters/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 26
FORMAT = "g5510-city-cycle-fixed-complete-WORD-parameters-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
PAIR_START, PAIR_END = 0x016CFC, 0x016D10
DIRECTORY_START, DIRECTORY_END = 0x016DE0, 0x016DEA
PAIR_ID = "rom_016CFC_city_cycle_WORD_pairs"
DIRECTORY_PREFIX_ID = "rom_016DE0_city_cycle_selected_WORDs_0_1"
DIRECTORY_LAST_ID = "rom_016DE8_city_cycle_selected_WORD_4"
DIRECTORY_INDICES = (0, 1, 4)
UNKNOWN_START, UNKNOWN_END = 0x016DE4, 0x016DE8
THRESHOLDS = (55, 65, 75, 85)
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = "build/direct_code/layout/" + LAYOUT_ID + "/m68k_bank01.s"
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
CONSUMERS = (
    (0x016C98, 0x016CFC, reference_value(__name__, 'CONSUMERS')),
    (0x016D40, 0x016DE0, reference_value(__name__, 'CONSUMERS_2')),
)
# Audit anchors from the older heuristic ledger, checked against original bytes.
INSTRUCTIONS = (
    (0x16CA0, "4243"), (0x16CA2, "0c42002d"), (0x16CA6, "6352"),
    (0x16CA8, "0c420037"), (0x16CAC, "631a"), (0x16CAE, "5843"),
    (0x16CB0, "0c420041"), (0x16CB4, "6312"), (0x16CB6, "5843"),
    (0x16CB8, "0c42004b"), (0x16CBC, "630a"), (0x16CBE, "5843"),
    (0x16CC0, "0c420055"), (0x16CC4, "6302"), (0x16CC6, "5843"),
    (0x16CCA, "4eb9000083d4"), (0x16CD2, "43fa0028"),
    (0x16CD6, "34313000"), (0x16CDA, "c4f8f61c"),
    (0x16CDE, "4842"), (0x16CE0, "d4713002"), (0x16CFA, "4e75"),
    (0x16D40, "49f8c700"), (0x16D82, "43fa005c"), (0x16D8A, "3618"),
    (0x16D8C, "6b10"), (0x16D8E, "18343000"), (0x16D92, "02440005"),
    (0x16D96, "e34c"), (0x16D98, "d4714000"), (0x16DEA, "4484"),
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
            raise ValueError("pinned original consumer bytes differ")
    if rom[DIRECTORY_END:DIRECTORY_END + 2] != bytes.fromhex("4484"):
        raise ValueError("original outside-directory code alias differs")


def metadata():
    return dict(
        format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=[dict(id=PAIR_ID, start=PAIR_START, end=PAIR_END, bytes=20,
                             physical_pairs=5, WORDs_per_pair=2, WORD_order="big"),
                        dict(id=DIRECTORY_PREFIX_ID, start=DIRECTORY_START, end=UNKNOWN_START,
                             bytes=4, physical_WORD_indices=[0, 1], WORD_order="big"),
                        dict(id=DIRECTORY_LAST_ID, start=UNKNOWN_END, end=DIRECTORY_END,
                             bytes=2, physical_WORD_indices=[4], WORD_order="big")],
        evidence=dict(
            confidence="confirmed", source="canonical consumer bytes + older heuristic instruction ledger",
            enhanced_source=dict(path=ENHANCED_PATH, sha256=ENHANCED_SHA256,
                                 original_consumer_reachability_confidence="heuristic"),
            frozen_raw_layout=dict(id=LAYOUT_ID, path=LAYOUT_PATH, sha256=LAYOUT_SHA256,
                lines=[183, 185], bank=1, offsets=[0x6CFC, 0x6DE0], lengths=[20, 10],
                all_26_emitted_source_bytes_raw=True, old_typed_baseline_overlap_bytes=0),
            consumers=[dict(start=start, end=end, bytes=end - start, sha256=expected)
                       for start, end, expected in CONSUMERS],
            instructions=[dict(address=address, bytes=raw, original_confidence="heuristic")
                          for address, raw in INSTRUCTIONS],
            pair_reader=dict(entry=0x16C98, selector="unsigned D2.W after source LONG read",
                disabled_CMP=0x16CA2, disabled_threshold_WORD=45, disabled_BLS=0x16CA6,
                disabled_RTS=0x16CFA, disabled_path_reads_source=False,
                BLS_threshold_WORDs=list(THRESHOLDS), D3_WORD_offsets=[0, 4, 8, 12, 16],
                LEA=0x16CD2, LEA_bytes="43fa0028", PC_base=0x16CD4,
                displacement_WORD=0x28, effective_base=PAIR_START,
                first_WORD_read=0x16CD6, second_WORD_read=0x16CE0,
                first_use="MULU.W F61C.W then SWAP D2", second_use="ADD.W to D2.W",
                complete_RAM_algorithm_modeled=False),
            directory_reader=dict(entry=0x16D40, source_BYTE_read=0x16D8E,
                source_RAM_base=0xFFC700, LEA=0x16D82, LEA_bytes="43fa005c",
                PC_base=0x16D84, displacement_WORD=0x5C, effective_base=DIRECTORY_START,
                ANDI_W=0x16D92, mask_WORD=5, LSL_W=0x16D96, shift=1,
                selected_byte_offsets=[0, 2, 8, 10], WORD_read=0x16D98,
                container_physical_WORDs=5, editable_physical_WORD_indices=list(DIRECTORY_INDICES),
                physical_slots_not_selected_on_this_path=[2, 3],
                unknown_unemitted_range=dict(start=UNKNOWN_START, end=UNKNOWN_END, bytes=4),
                container_is_not_edit_scope=True, CPU_clamp=False,
                offset_10_address=DIRECTORY_END, offset_10_is_code=True,
                offset_10_original_WORD=0x4484, original_code_operation="NEG.L D4")),
        parameter_business_meanings="unknown", edited_gameplay_safety="unknown",
        independent_CPU_comparison=False,
    )


def pair_fixed(index):
    return dict(id=f"city_cycle_pair_{index}", index=index, D3_WORD_offset=4 * index,
                first_address=PAIR_START + 4 * index, second_address=PAIR_START + 4 * index + 2)


def directory_fixed(index):
    return dict(id=f"city_cycle_directory_{index}", physical_index=index,
                address=DIRECTORY_START + 2 * index)


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["pairs"] = [dict(**pair_fixed(index),
        first_WORD=int.from_bytes(rom[PAIR_START + 4 * index:PAIR_START + 4 * index + 2], "big"),
        second_WORD=int.from_bytes(rom[PAIR_START + 4 * index + 2:PAIR_START + 4 * index + 4], "big"))
        for index in range(5)]
    fields["WORD_directory"] = [dict(**directory_fixed(index),
        WORD=int.from_bytes(rom[DIRECTORY_START + 2 * index:DIRECTORY_START + 2 * index + 2], "big"))
        for index in DIRECTORY_INDICES]
    return fields


def pinned(row, fixed, mutable, label):
    keys(row, set(fixed) | set(mutable), label)
    for key, value in fixed.items():
        same(row[key], value, label + "." + key)


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {"pairs", "WORD_directory"}, "city cycle package")
    pairs = bytearray()
    for index, entry in enumerate(exact_list(fields["pairs"], 5, "physical WORD pairs")):
        pinned(entry, pair_fixed(index), {"first_WORD", "second_WORD"}, "WORD pair")
        for key in ("first_WORD", "second_WORD"):
            pairs.extend(uint(entry[key], 0xFFFF, "full parameter WORD").to_bytes(2, "big"))
    directory = bytearray()
    for index, entry in zip(DIRECTORY_INDICES, exact_list(fields["WORD_directory"], 3, "selected physical WORDs")):
        pinned(entry, directory_fixed(index), {"WORD"}, "directory WORD")
        directory.extend(uint(entry["WORD"], 0xFFFF, "full directory WORD").to_bytes(2, "big"))
    result = [dict(id=PAIR_ID, start=PAIR_START, end=PAIR_END, data=bytes(pairs),
                   role="confirmed_complete_WORD_parameter_pairs"),
              dict(id=DIRECTORY_PREFIX_ID, start=DIRECTORY_START, end=UNKNOWN_START,
                   data=bytes(directory[:4]), role="confirmed_selected_complete_WORDs_0_1"),
              dict(id=DIRECTORY_LAST_ID, start=UNKNOWN_END, end=DIRECTORY_END,
                   data=bytes(directory[4:]), role="confirmed_selected_complete_WORD_4")]
    if [len(row["data"]) for row in result] != [20, 4, 2] or any(a["end"] > b["start"] for a, b in zip(result, result[1:])):
        raise ValueError("fixed 20+4+2 source byte costs or nonoverlap differs")
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for entry in blocks(rom, fields):
        image[entry["start"]:entry["end"]] = entry["data"]
    return bytes(image)


def pair_index(selector_WORD):
    """Original unsigned BLS paths; <=45 returns without reading either WORD."""
    uint(selector_WORD, 0xFFFF, "unsigned source selector WORD")
    return None if selector_WORD <= 45 else sum(selector_WORD > threshold for threshold in THRESHOLDS)


def lookup_income(image, selector_WORD):
    """Only the local source reads, from original or edited complete bytes image."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires a complete bytes image")
    index = pair_index(selector_WORD)
    if index is None:
        return dict(source_read=False, pair_index=None, D3_WORD_offset=0, addresses=[], WORDs=[])
    address = PAIR_START + 4 * index
    return dict(source_read=True, pair_index=index, D3_WORD_offset=4 * index,
                addresses=[address, address + 2],
                WORDs=[int.from_bytes(image[p:p + 2], "big") for p in (address, address + 2)])


def expense_read_address(selector_BYTE):
    """ANDI.W #5 after BYTE read clears the other WORD bits before LSL.W #1."""
    return DIRECTORY_START + 2 * (uint(selector_BYTE, 255, "source selector BYTE") & 5)


def lookup_expense(image, selector_BYTE):
    """Read the actual full WORD, including offset10's outside-scope code alias."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires a complete bytes image")
    address = expense_read_address(selector_BYTE)
    return dict(address=address, D4_WORD_offset=address - DIRECTORY_START,
                WORD=int.from_bytes(image[address:address + 2], "big"),
                inside_edit_scope=address in {DIRECTORY_START + 2 * index for index in DIRECTORY_INDICES})


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
    word = dict(type="integer", minimum=0, maximum=65535)
    properties = {key: fixed(value) for key, value in metadata().items()}
    properties["pairs"] = exact([obj({**{key: fixed(value) for key, value in pair_fixed(i).items()},
        "first_WORD": word, "second_WORD": word}) for i in range(5)])
    properties["WORD_directory"] = exact([obj({**{key: fixed(value) for key, value in directory_fixed(i).items()},
        "WORD": word}) for i in DIRECTORY_INDICES])
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Only thirteen actually-selected literal big-endian WORDs are editable; expense slots2/3 remain unknown/unemitted and code offset10 is not a sixth slot."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom or image[UNKNOWN_START:UNKNOWN_END] != rom[UNKNOWN_START:UNKNOWN_END]:
        raise ValueError("whole-ROM serialized field roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=3,
        physical_pairs=5, editable_directory_WORDs=3, container_directory_WORDs=5,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        original_pairs_hex=rom[PAIR_START:PAIR_END].hex(),
        original_directory_container_hex=rom[DIRECTORY_START:DIRECTORY_END].hex(),
        unknown_unemitted_directory_hex=rom[UNKNOWN_START:UNKNOWN_END].hex(),
        expense_BYTE_5_code_alias_example=lookup_expense(rom, 5),
        income_WORD_45_no_read_example=lookup_income(rom, 45),
        income_WORD_FFFF_example=lookup_income(rom, 65535),
        preview_is_editing_authority=False,
        blocks=[{key: value for key, value in row.items() if key != "data"}
                | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=3,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in city_cycle_parameters build scope or the exact formal bundle")
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
