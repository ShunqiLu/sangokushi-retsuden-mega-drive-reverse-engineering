"""Sixteen full coordinate WORDs with proven selector12..19 source reads.

The two24-WORD physical containers are not fully admitted. Only the actual
static guard chain's eight pairs are authored; read-entry aliases remain
whole-image diagnostics, without clamping them to the editor's eight slots.
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
OUTPUT_ROOT = ROOT / "build/scene_coordinate_word_fields"
FORMAL_ROOT = ROOT / "analysis/scene_coordinate_word_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
MAX_JSON = 1024 * 1024
FORMAT = "g5510-scene-conditional-coordinate-WORD-source-v1"
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
EDITABLE_BYTES = 32
X_BASE, Y_BASE = 0x039BEC, 0x039C1C
SELECTORS = tuple(range(12, 20))
RANGES = ((0x039C04, 0x039C14), (0x039C34, 0x039C44))
BODIES = (
    (0x039802, 0x03980E, reference_value(__name__, 'BODIES')),
    (0x039AA6, 0x039AB2, reference_value(__name__, 'BODIES_2')),
    (0x039B10, 0x039B3A, reference_value(__name__, 'BODIES_3')),
    (0x039BC0, 0x039BEC, reference_value(__name__, 'BODIES_4')),
)
INSTRUCTIONS = (
    (0x039802, "0c79000a00ff7026"), (0x03980A, "6400029a"),
    (0x039AA6, "0c79000b00ff7026"), (0x039AAE, "62000060"),
    (0x039B10, "0c79001300ff7026"), (0x039B18, "620001d6"),
    (0x039B1C, "527900ff703c"), (0x039B22, "0c79009000ff703c"),
    (0x039B2A, "67000094"), (0x039B2E, "0c79009000ff703c"),
    (0x039B36, "62000114"), (0x039BC0, "303900ff7026"),
    (0x039BC6, "e340"), (0x039BC8, "41fa0022"), (0x039BCE, "43fa004c"),
    (0x039BD4, "32300000"), (0x039BD8, "34310000"),
    (0x039BDC, "33c100ff7028"), (0x039BE2, "33c200ff702a"),
    (0x039BE8, "60000062"),
)
EVIDENCE_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
EVIDENCE_SHA256 = reference_value(__name__, 'EVIDENCE_SHA256')
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical original ROM bytes, size and SHA-256 required")
    for start, end, digest in BODIES:
        if sha(rom[start:end]) != digest:
            raise ValueError("pinned original guard/read consumer differs")
    for address, raw in INSTRUCTIONS:
        if rom[address:address + len(raw) // 2] != bytes.fromhex(raw):
            raise ValueError("pinned original consumer opcode differs")


def metadata():
    return dict(
        format=FORMAT, confidence="confirmed", business_scene_names="unknown",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(
            emit_BYTES=32, full_WORD_count=16, pair_count=8,
            ranges=[dict(start=start, end=end, bytes=end-start) for start, end in RANGES],
            containers=[dict(axis=axis, start=base, end=base+48, physical_WORD_count=24,
                             all_container_WORDs_admitted=False) for axis, base in (("X", X_BASE), ("Y", Y_BASE))],
            unadmitted_container_BYTES=64, physical_capacity_is_CPU_clamp=False),
        evidence=dict(
            source="canonical original guard/read opcodes and existing enhanced instruction ledger",
            original_ledger=dict(path=EVIDENCE_PATH, sha256=EVIDENCE_SHA256,
                                 original_reachability_confidence="heuristic", runtime_file_read=False),
            bodies=[dict(start=start, end=end, bytes=end-start, sha256=digest) for start, end, digest in BODIES],
            instructions=[dict(address=address, bytes=raw) for address, raw in INSTRUCTIONS],
            guard_chain=dict(selector_RAM=0xFF7026, unsigned_lower_gate=10,
                             initial_compare_PC=0x039802, branch_PC=0x03980A,
                             second_compare_PC=0x039AA6, second_unsigned_upper=11,
                             upper_compare_PC=0x039B10, upper_unsigned_maximum=19,
                             increment_WORD_PC=0x039B1C, counter_RAM=0xFF703C,
                             after_increment_equals=0x0090, equality_compare_PC=0x039B22,
                             equality_branch_PC=0x039B2A, read_entry=0x039BC0,
                             actual_static_selectors=list(SELECTORS),
                             stable_live_selector_assumption=True,
                             interrupts_or_other_RAM_writers_simulated=False),
            read_stage=dict(entry=0x039BC0, end=0x039BEC, selector_WORD_load_PC=0x039BC0,
                            WORD_shift_PC=0x039BC6, index="s16((selector.W << 1) & FFFF)",
                            X_LEA_PC=0x039BC8, X_PC_base=0x039BCA, X_displacement_WORD=0x0022,
                            Y_LEA_PC=0x039BCE, Y_PC_base=0x039BD0, Y_displacement_WORD=0x004C,
                            X_WORD_read_PC=0x039BD4, Y_WORD_read_PC=0x039BD8,
                            X_RAM_write_PC=0x039BDC, X_RAM=0xFF7028,
                            Y_RAM_write_PC=0x039BE2, Y_RAM=0xFF702A,
                            following_branch_PC=0x039BE8, following_target=0x039C4C,
                            original_local_index_clamp=False)),
        diagnostic_read_entry_is_natural_admission=False,
        edited_gameplay_safety="unknown", complete_scene_algorithm=False,
        independent_CPU_comparison=False,
    )


def pair_fixed(selector):
    return dict(id=f"scene_coordinate_selector_{selector:02d}", selector_WORD=selector,
                X_address=X_BASE+2*selector, Y_address=Y_BASE+2*selector,
                source_read_confidence="confirmed_static_conditional_read")


def word(image, address):
    return int.from_bytes(image[address:address+2], "big")


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result["coordinate_pairs"] = [dict(**pair_fixed(selector),
        X_WORD=word(rom, X_BASE+2*selector), Y_WORD=word(rom, Y_BASE+2*selector)) for selector in SELECTORS]
    return result


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"coordinate_pairs"}, "coordinate source package")
    for key, value in fixed.items():
        same(fields[key], value, "package." + key)
    pairs = exact_list(fields["coordinate_pairs"], 8, "eight admitted coordinate pairs")
    axes = {"X": bytearray(), "Y": bytearray()}
    for selector, pair in zip(SELECTORS, pairs):
        pinned = pair_fixed(selector)
        keys(pair, set(pinned) | {"X_WORD", "Y_WORD"}, "coordinate pair")
        for key, value in pinned.items():
            same(pair[key], value, "pair." + key)
        for axis in axes:
            axes[axis].extend(uint(pair[axis+"_WORD"], 0xFFFF, "full coordinate WORD").to_bytes(2, "big"))
    return [dict(id=f"rom_{start:06X}_scene_coordinate_{axis}_WORDs", start=start, end=end,
                 data=bytes(axes[axis]), role="confirmed_static_conditional_scene_coordinate_full_WORD_source")
            for axis, (start, end) in zip(("X", "Y"), RANGES)]


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def read_addresses(selector_WORD):
    """Original read-entry formula, not the static outer guard or editor clamp."""
    uint(selector_WORD, 0xFFFF, "full selector WORD")
    shifted = (selector_WORD << 1) & 0xFFFF
    signed = shifted - 0x10000 if shifted & 0x8000 else shifted
    return X_BASE+signed, Y_BASE+signed


def read_entry(image, selector_WORD, D0_LONG=0, D1_LONG=0, D2_LONG=0):
    """Narrow live-image WORD lookup view. It does not enter the original gate."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic source view requires a complete bytes image")
    for name, value in (("D0", D0_LONG), ("D1", D1_LONG), ("D2", D2_LONG)):
        uint(value, 0xFFFFFFFF, name+" full LONG")
    x, y = read_addresses(selector_WORD)
    if not 0 <= x < ROM_SIZE-1 or not 0 <= y < ROM_SIZE-1:
        raise ValueError("read-entry source outside supplied ROM image")
    x_word, y_word = word(image, x), word(image, y)
    inside = lambda address: any(start <= address and address+2 <= end for start, end in RANGES)
    return dict(selector_WORD=selector_WORD, X_address=x, Y_address=y,
                X_WORD=x_word, Y_WORD=y_word,
                D0_LONG=(D0_LONG & 0xFFFF0000) | ((selector_WORD << 1) & 0xFFFF),
                D1_LONG=(D1_LONG & 0xFFFF0000) | x_word,
                D2_LONG=(D2_LONG & 0xFFFF0000) | y_word,
                X_inside_edit_scope=inside(x), Y_inside_edit_scope=inside(y),
                diagnostic_only=True, original_outer_guards_entered=False,
                natural_read_admission=False)


def static_guard(selector_WORD, counter_before_WORD):
    """Stable-selector branch projection only, not an interrupt/live-RAM model."""
    uint(selector_WORD, 0xFFFF, "full selector WORD")
    uint(counter_before_WORD, 0xFFFF, "counter before increment WORD")
    in_counter_path = 12 <= selector_WORD <= 19
    after = (counter_before_WORD+1) & 0xFFFF if in_counter_path else counter_before_WORD
    return dict(selector_WORD=selector_WORD, counter_before_WORD=counter_before_WORD,
                counter_path_taken=in_counter_path, counter_after_WORD=after,
                conditional_read_taken=in_counter_path and after == 0x0090,
                stable_live_selector_assumption=True, complete_runtime_admission=False)


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
        return dict(type={str:"string", int:"integer", bool:"boolean"}[type(value)], const=value)
    properties = {key: fixed(value) for key, value in metadata().items()}
    properties["coordinate_pairs"] = exact([obj({**{key: fixed(value) for key, value in pair_fixed(selector).items()},
        "X_WORD": dict(type="integer", minimum=0, maximum=0xFFFF),
        "Y_WORD": dict(type="integer", minimum=0, maximum=0xFFFF)}) for selector in SELECTORS])
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Eight conditional pairs; full16 bits are editable, unadmitted24-slot neighbors are not authored."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("serialized coordinate fields whole-ROM roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=32, physical_blocks=2,
                  whole_ROM_exact=True, whole_ROM_sha256=sha(image),
                  original_pairs=fields["coordinate_pairs"],
                  static_guard_examples=[static_guard(selector, counter) for selector, counter in
                                         ((12, 0x008F), (19, 0x008F), (11, 0x008F), (20, 0x008F), (12, 0xFFFF))],
                  diagnostic_alias_examples=[read_entry(rom, selector) for selector in (12, 19, 24, 0x8000, 0x4000, 0xFFFF)],
                  blocks=[{key:value for key, value in row.items() if key != "data"}
                          | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=32, physical_blocks=2,
        members={name:dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("dedicated scene coordinate build output or exact formal bundle required")
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
            put(target/name, data)
        result = dict(path=str(target), editable_bytes=32,
                      members={name:sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name, data in render_bundle(rom).items():
            if read_bounded(bundle/name, MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=32, whole_ROM_exact=True,
                      whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=32,
                      exact_canonical=image == rom, bytes=len(image), sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
