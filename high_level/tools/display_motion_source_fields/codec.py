"""168 lossless scene-motion, coordinate and display-color source bytes.

The editing groups follow original read widths. Local read views take fetched
WORD inputs, preserve wrapping/signed addresses, and never execute renderers,
RAM writers or pointer targets. Physical group sizes are not CPU index limits.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
OUTPUT_ROOT = ROOT / "build/display_motion_source_fields"
FORMAL_ROOT = ROOT / "analysis/display_motion_source_fields/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 168
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "validation.json", "manifest.json"))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
# Start, physical item count, byte width, neutral role, original read PC.
GROUPS = (
    (0x30ED8, 16, 1, "scene_initial_RAM_BYTEs", 0x30EC2),
    (0x39A82, 36, 1, "motion_unsigned_compare_BYTEs", 0x39A04),
    (0x39BEC, 12, 2, "coordinate_first_WORDs", 0x39BD4),
    (0x39C1C, 12, 2, "coordinate_second_WORDs", 0x39BD8),
    (0x39E26, 6, 4, "motion_source_LONGs", 0x39DEE),
    (0x3A3B2, 7, 4, "alternate_motion_source_LONGs", 0x3A37E),
    (0x6747E, 8, 2, "display_color_source_WORDs", 0x67476),
)
SOURCE_HASHES = (
    reference_value(__name__, 'SOURCE_HASHES'),
    reference_value(__name__, 'SOURCE_HASHES_2'),
    reference_value(__name__, 'SOURCE_HASHES_3'),
    reference_value(__name__, 'SOURCE_HASHES_4'),
    reference_value(__name__, 'SOURCE_HASHES_5'),
    reference_value(__name__, 'SOURCE_HASHES_6'),
    reference_value(__name__, 'SOURCE_HASHES_7'),
)
CONSUMERS = (
    (0x30EB4, 0x30ED8, reference_value(__name__, 'CONSUMERS')),
    (0x399F8, 0x39A82, reference_value(__name__, 'CONSUMERS_2')),
    (0x39BC0, 0x39BEC, reference_value(__name__, 'CONSUMERS_3')),
    (0x39DCA, 0x39E26, reference_value(__name__, 'CONSUMERS_4')),
    (0x3A372, 0x3A3B2, reference_value(__name__, 'CONSUMERS_5')),
    (0x6746A, 0x6747E, reference_value(__name__, 'CONSUMERS_6')),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def image_bytes(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("complete bytes image required")


def verify_rom(rom):
    image_bytes(rom)
    if sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM SHA-256 required")
    for start, end, digest in CONSUMERS:
        if sha(rom[start:end]) != digest:
            raise ValueError("original consumer body differs")
    for (start, count, width, _, _), digest in zip(GROUPS, SOURCE_HASHES):
        if sha(rom[start:start + count * width]) != digest:
            raise ValueError("original typed source differs")


def metadata():
    return dict(format="g5510-display-motion-literal-sources-v1", confidence="candidate",
        source_format_confidence="confirmed", canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        evidence=dict(accepted_raw_layout=LAYOUT_ID, accepted_raw_BYTES=46619,
            admitted_raw_BYTES=168, older_typed_overlap_BYTES=0,
            consumers=[dict(start=s, end=e, sha256=h) for s, e, h in CONSUMERS],
            scene_seed=dict(LEA_PC=0x30EB8, source=0x30ED8, count_WORD=15,
                DBRA_PC=0x30EC4, BYTE_read=0x30EC2, original_reads=16, RAM_destination=0xFFF714),
            motion_threshold=dict(LEA_PC=0x399FE, index="signed fetched FF7026.W byte offset",
                read_PC=0x39A04, unsigned_CMP_BYTE=0x39A0E, unsigned_BHI=0x39A10),
            coordinate_pair=dict(selector_load=0x39BC0, ASL_WORD_1=0x39BC6,
                first_LEA=0x39BC8, second_LEA=0x39BCE, reads=[0x39BD4, 0x39BD8],
                RAM_write_PCs=[0x39BDC, 0x39BE2], RAM_destinations=[0xFF7028, 0xFF702A]),
            motion_directories=dict(index="FF703C.W already a signed byte offset, not a host slot",
                reads=[0x39DEE, 0x3A37E], source_pointers_full_BE32=True,
                following_copy_LONG_count=8, pointer_target_copy_simulated=False),
            display_colors=dict(selector_load=0x6746A, LSL_WORD_2=0x6746E,
                LEA_PC=0x67470, MOVEM_WORD_read=0x67476, WORD_count_per_read=2,
                original_MOVEM_WORD_sign_extension=True,
                rendering_uses_low_BYTE_but_full_source_WORD_is_editable=True)),
        claims=dict(physical_counts_are_CPU_clamps=False, pointer_targets_followed=False,
            complete_CPU_or_RAM_VDP_execution=False, independent_CPU_comparison=False,
            recovered_functions_added=0, high_level_compiler_coverage_added=0),
        natural_selector_domains="unknown", edited_gameplay_safety="unknown",
        business_scene_names="unknown")


def fixed_group(index):
    start, count, width, role, read = GROUPS[index]
    return dict(id=f"rom_{start:06X}_{role}", start=start, end=start + count * width,
                item_count=count, item_BYTES=width, byte_order="big", role=role, read_PC=read)


def pinned(value, fixed, mutable, label):
    keys(value, set(fixed) | set(mutable), label)
    for key, expected in fixed.items():
        same(value[key], expected, label + "." + key)


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(), groups=[dict(**fixed_group(i), values=[
        int.from_bytes(rom[p:p + width], "big")
        for p in range(start, start + count * width, width)])
        for i, (start, count, width, _, _) in enumerate(GROUPS)])


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {"groups"}, "display motion package")
    rows = []
    for i, group in enumerate(exact_list(fields["groups"], len(GROUPS), "physical groups")):
        fixed = fixed_group(i)
        pinned(group, fixed, {"values"}, "source group")
        width = fixed["item_BYTES"]
        data = b"".join(uint(value, (1 << (8 * width)) - 1, "full source bits").to_bytes(width, "big")
            for value in exact_list(group["values"], fixed["item_count"], "fixed source cost"))
        rows.append(dict(id=group["id"], start=group["start"], end=group["end"],
                         data=data, role=group["role"]))
    if sum(len(row["data"]) for row in rows) != EDITABLE_BYTES:
        raise ValueError("fixed source cost differs")
    return rows


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def signed_WORD(value):
    return value - 65536 if value & 32768 else value


def read(image, start, width, offset_WORD, read_PC):
    """Local bus address/value diagnostic; odd WORD/LONG reads stay boundaries."""
    address = (start + signed_WORD(offset_WORD)) & 0xFFFFFFFF
    result = dict(read_address=address, read_PC=read_PC, item_BYTES=width,
                  source_only=True, CPU_execution=False)
    if width > 1 and address & 1:
        return dict(**result, status="odd_address_exception_boundary")
    if not 0 <= address <= ROM_SIZE - width:
        return dict(**result, status="outside_ROM_read_boundary")
    return dict(**result, status="source_read", value=int.from_bytes(image[address:address + width], "big"))


def source_view(image, role, fetched_WORD=0):
    """Project only original source reads with an already fetched WORD input.

    Coordinate/color roles apply the original WORD shift once; pointer and
    threshold roles take byte offsets directly. The seed role always has the
    original DBRA count. Guards preceding these local readers are not executed.
    """
    image_bytes(image)
    value = uint(fetched_WORD, 65535, "fetched WORD")
    if role == "seed":
        return [read(image, 0x30ED8, 1, offset, 0x30EC2) for offset in range(16)]
    if role == "threshold":
        return [read(image, 0x39A82, 1, value, 0x39A04)]
    if role == "coordinates":
        offset = (value << 1) & 65535
        return [read(image, base, 2, offset, pc) for base, pc in
                ((0x39BEC, 0x39BD4), (0x39C1C, 0x39BD8))]
    if role in ("motion", "alternate_motion"):
        start, pc = (0x39E26, 0x39DEE) if role == "motion" else (0x3A3B2, 0x3A37E)
        return [read(image, start, 4, value, pc)]
    if role == "colors":
        offset = (value << 2) & 65535
        # MOVEM calculates one signed indexed EA, then increments that EA.
        first = read(image, 0x6747E, 2, offset, 0x67476)
        second = read(image, 0x67480, 2, offset, 0x67476)
        return [first, second]
    raise ValueError("unknown local source role")


def witnesses(image):
    rows = source_view(image, "seed")
    for i in range(36):
        rows += source_view(image, "threshold", i)
    for i in range(12):
        rows += source_view(image, "coordinates", i)
    for role, count in (("motion", 6), ("alternate_motion", 7)):
        for i in range(count):
            rows += source_view(image, role, i * 4)
    for i in range(4):
        rows += source_view(image, "colors", i)
    return rows


def render_bundle(rom):
    fields = extract(rom)
    encoded = blocks(rom, fields)
    image = rebuild(rom, load_fields(dump(fields)))
    views = witnesses(image)
    reads = {p for row in views for p in range(row["read_address"], row["read_address"] + row["item_BYTES"])}
    authored = {p for row in encoded for p in range(row["start"], row["end"])}
    if image != rom or reads != authored or len(reads) != EDITABLE_BYTES:
        raise ValueError("whole-ROM roundtrip or source-read union differs")
    report = dict(**metadata(), editable_bytes=168, physical_blocks=7,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), constructed_local_read_union_BYTES=168,
        read_witnesses=views, blocks=[{k:v for k,v in row.items() if k != "data"} |
            dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json":dump(fields), "validation.json":dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=168,
        members={name:dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("dedicated fresh output or exact formal bundle required")
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
            raise ValueError("export needs fresh output only")
        target = fresh_output(args.output, True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None:
            raise ValueError("import needs fields and fresh output")
        target = fresh_output(args.output)
        if target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError("verify is read-only")
    rom = read_bounded(args.rom, ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            put(target / name, data)
        result = dict(path=str(target), editable_bytes=168, members={name:sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact three-member bundle required")
        for name, data in render_bundle(rom).items():
            if read_bounded(bundle / name, MAX_JSON) != data:
                raise ValueError("canonical bundle differs: " + name)
        result = dict(verified=True, editable_bytes=168, whole_ROM_exact=True)
    else:
        image = rebuild(rom, load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON)))
        if target is not None:
            put(target, image)
        result = dict(exact_canonical=image == rom, bytes=len(image), sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
