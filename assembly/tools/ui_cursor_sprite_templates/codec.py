"""Twenty-one original AC08 sprite templates, retaining every source bit.

The editor owns exactly 320 six-byte records and 21 first-8000 WORDs.
Physical counts are editing contracts, not CPU clamps. The diagnostic is only
the D2=0 immutable-ROM source-read projection, not a renderer or RAM/CPU model.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared
from tools.sprite_word_resources import codec as sprite_format

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
OUTPUT_ROOT = ROOT / "build/ui_cursor_sprite_templates"
FORMAL_ROOT = ROOT / "analysis/ui_cursor_sprite_templates/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-UI-cursor-sprite-template-source-fields-v1"
EDITABLE_BYTES = 1962
MAX_JSON = 2 * 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
CONSUMER = (0xAC08, 0xAD06, reference_value(__name__, 'CONSUMER'))
# start, exclusive source end, original A0 LEA, actual JSR, LEA-through-JSR SHA
SPECS = (
    (0x1392, 0x13DC, 0x1386, 0x138A, reference_value(__name__, 'SPECS')),
    (0x4DD6, 0x4E50, 0x4DB6, 0x4DCE, reference_value(__name__, 'SPECS_2')),
    (0x6452, 0x64CC, 0x63FE, 0x6402, reference_value(__name__, 'SPECS_3')),
    (0xAB82, 0xAC08, 0xAB76, 0xAB7A, reference_value(__name__, 'SPECS_4')),
    (0xC19A, 0xC1E4, 0xC56E, 0xC588, reference_value(__name__, 'SPECS_5')),
    (0xC7D0, 0xC832, 0xC7AE, 0xC7C8, reference_value(__name__, 'SPECS_6')),
    (0xCC9A, 0xCD20, 0xCC02, 0xCC20, reference_value(__name__, 'SPECS_7')),
    (0xD1F6, 0xD270, 0xD1D2, 0xD1EE, reference_value(__name__, 'SPECS_8')),
    (0xD4DC, 0xD526, 0xD4B8, 0xD4D4, reference_value(__name__, 'SPECS_9')),
    (0xD700, 0xD74A, 0xD6DC, 0xD6F8, reference_value(__name__, 'SPECS_10')),
    (0x12248, 0x12292, 0x12224, 0x12240, reference_value(__name__, 'SPECS_11')),
    (0x13C1C, 0x13C7E, 0x13BF8, 0x13C14, reference_value(__name__, 'SPECS_12')),
    (0x14956, 0x149A0, 0x14932, 0x1494E, reference_value(__name__, 'SPECS_13')),
    (0x15B2C, 0x15B76, 0x15B08, 0x15B24, reference_value(__name__, 'SPECS_14')),
    (0x19520, 0x19582, 0x194FA, 0x19518, reference_value(__name__, 'SPECS_15')),
    (0x1986A, 0x198B4, 0x1985C, 0x19862, reference_value(__name__, 'SPECS_16')),
    (0x1D82E, 0x1D890, 0x1D80A, 0x1D826, reference_value(__name__, 'SPECS_17')),
    (0x20644, 0x2068E, 0x20622, 0x2063C, reference_value(__name__, 'SPECS_18')),
    (0x2146A, 0x214CC, 0x21442, 0x21462, reference_value(__name__, 'SPECS_19')),
    (0x31502, 0x3154C, 0x314DE, 0x314FA, reference_value(__name__, 'SPECS_20')),
    (0x3184A, 0x318AC, 0x31828, 0x31842, reference_value(__name__, 'SPECS_21')),
)
UNION_SHA256 = reference_value(__name__, 'UNION_SHA256')
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    start, end, expected = CONSUMER
    if sha(rom[start:end]) != expected:
        raise ValueError("complete original AC08 consumer differs")
    for _, _, lea, call, expected in SPECS:
        if sha(rom[lea:call + 6]) != expected or rom[call:call + 6] != bytes.fromhex("4eb90000ac08"):
            raise ValueError("pinned original pointer/call prefix differs")


def identifier(start):
    return f"rom_{start:06X}_UI_sprite_template"


def template_fixed(spec):
    start, end, _, _, _ = spec
    return dict(id=identifier(start), start=start, end=end,
                record_count=(end - start - 2) // 6, terminator_WORD=0x8000)


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        evidence=dict(source="canonical original pointers/calls and AC08 six-byte read grammar",
            enhanced_ledger=dict(path=ENHANCED_PATH, sha256=ENHANCED_SHA256,
                                 original_reachability_confidence="mixed_older_runtime_confirmed_and_heuristic_not_new_natural_proof"),
            frozen_raw_layout=dict(id=LAYOUT_ID, all_emitted_bytes_raw=True,
                                   older_typed_overlap_bytes=0),
            consumer=dict(start=CONSUMER[0], end=CONSUMER[1], sha256=CONSUMER[2]),
            callers=[dict(source=start, source_end=end, A0_LEA=lea, JSR=call,
                          prefix_end=call + 6, sha256=digest,
                          older_LEA_JSR_confidence="runtime_confirmed" if call in (0xC7C8, 0x31842) else "heuristic")
                     for start, end, lea, call, digest in SPECS],
            framing=dict(stride_bytes=6, X_WORD_offset=0, attribute_WORD_offset=2,
                         packed_shape_Y_WORD_offset=4, WORD_order="big",
                         first_8000_only=True, term_read_address=0xAC5E,
                         term_compare_address=0xAC60, source_advance=0xACF4),
            source_reads=dict(X_WORD=0xAC5E, horizontal_path_shape_WORD=0xAC6E,
                              clipped_X_before_shape=True, shape_WORD=0xAC9C,
                              clipped_Y_before_attribute=True, attribute_WORD=0xACE8),
            read_stop=dict(F300_BYTE_unsigned_limit=80, entry_compare=0xAC2C,
                           post_record_compare=0xACF6, accepted_increment=0xACE4,
                           clipped_records_do_not_increment=True,
                           physical_record_count_not_CPU_clamp=True,
                           term_may_not_be_read_if_state_limit_reached=True),
            packed_fields=dict(X="complete signed-WORD bit representation; 8000 reserved for framing",
                attribute="11 tile bits + H/V bits + 2 palette bits + priority bit",
                shape_Y="2 width bits + 2 height bits + signed 12-bit Y; all bits retained",
                size_field_names_are_packing_not_a_mirror_algorithm=True),
            immutable_source_projection=dict(D2_WORD=0, natural_state=False,
                full_source_reference_union="constructed origin WORDs per record, not natural caller-domain proof",
                no_RAM_writes_stack_bus_or_renderer=True)),
        template_business_names="unknown", edited_gameplay_safety="unknown",
        independent_CPU_comparison=False,
        exclusions=dict(unreferenced_map_tail=[0x5CE22, 0x5D5E4],
            unreferenced_portrait_gaps=[[0xC3C7A, 0xC3F7A], [0xC34FA, 0xC37BA], [0xC141A, 0xC161A]],
            shape_only_other_templates_not_emitted=True))


def pinned(row, fixed, mutable, label):
    keys(row, set(fixed) | set(mutable), label)
    for key, value in fixed.items():
        same(row[key], value, label + "." + key)


def record(raw, address):
    if type(raw) is not bytes or len(raw) != 6:
        raise ValueError("complete six-byte sprite record required")
    return sprite_format.sprite(raw + b"\x80\x00", address)


def record_bytes(row, address):
    return sprite_format.sprite_bytes(row, address)[:6]


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result["templates"] = []
    for spec in SPECS:
        start, end, _, _, _ = spec
        if rom[end - 2:end] != b"\x80\x00":
            raise ValueError("first terminator WORD differs")
        rows = [record(rom[p:p + 6], p) for p in range(start, end - 2, 6)]
        result["templates"].append(dict(**template_fixed(spec), records=rows))
    blocks(rom, result)
    return result


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {"templates"}, "UI sprite source package")
    result = []
    for row, spec in zip(exact_list(fields["templates"], len(SPECS), "physical templates"), SPECS):
        fixed = template_fixed(spec)
        pinned(row, fixed, {"records"}, "template")
        records = exact_list(row["records"], fixed["record_count"], "fixed source record count")
        data = b"".join(record_bytes(item, fixed["start"] + 6 * index) for index, item in enumerate(records))
        data += fixed["terminator_WORD"].to_bytes(2, "big")
        if len(data) != fixed["end"] - fixed["start"]:
            raise ValueError("fixed template cost differs")
        result.append(dict(id=fixed["id"], start=fixed["start"], end=fixed["end"], data=data,
                           role="confirmed_source_packed_sprite_records_and_first_WORD_term"))
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES or any(a["end"] > b["start"] for a, b in zip(result, result[1:])):
        raise ValueError("non-overlapping 1962-byte scope differs")
    return result


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def source_view(image, start, x_origin_WORD, y_origin_WORD, sprite_count_BYTE=0, *, record_budget=256):
    """D2=0 local immutable-source read plan, including clipping and cap stops.

    x/y inputs are already computed D3/D4 WORDs (D0-F60A+80, D1-F60E+80).
    This accepts edited-image/source aliases, not only the editing catalog.
    Original queue/RAM alias writes, interrupts, flips and bus faults are not
    simulated. A diagnostic budget is an external boundary, never a CPU clamp.
    """
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("complete bytes image required for source diagnostic")
    uint(start, 0xFFFFFFFF, "logical source address")
    if start & 1:
        raise ValueError("odd WORD reads/address exception are not modeled")
    x_origin_WORD = uint(x_origin_WORD, 65535, "already computed X origin WORD")
    y_origin_WORD = uint(y_origin_WORD, 65535, "already computed Y origin WORD")
    count = uint(sprite_count_BYTE, 255, "already fetched F300 BYTE")
    if type(record_budget) is not int or record_budget < 1:
        raise ValueError("positive external diagnostic budget required")
    reads, records = [], []
    cursor = start
    def take(address, pc, role):
        if not 0 <= address <= ROM_SIZE - 2:
            raise ValueError("source diagnostic reached an out-of-ROM boundary")
        value = int.from_bytes(image[address:address + 2], "big")
        reads.append(dict(address=address, bytes=2, WORD=value, PC=pc, role=role))
        return value
    status = "state_limit"
    while count < 80 and len(records) < record_budget:
        x = take(cursor, 0xAC5E, "first_X_or_term_WORD")
        if x == 0x8000:
            status = "first_8000_TERM"
            break
        placed_x = (x + x_origin_WORD) & 65535
        entry = dict(start=cursor, X_WORD=x, x_after_WORD_add=placed_x, accepted=False)
        if 0x70 <= placed_x < 0x160:
            packed = take(cursor + 4, 0xAC9C, "packed_shape_Y_WORD")
            y = sprite_format.signed(packed & 0xFFF, 12)
            placed_y = (y + y_origin_WORD) & 65535
            entry.update(packed_shape_Y_WORD=packed, y_after_WORD_add=placed_y)
            if 0x70 <= placed_y < 0x1C0:
                entry["attribute_WORD"] = take(cursor + 2, 0xACE8, "full_attribute_WORD")
                entry["accepted"] = True
                count = (count + 1) & 255
        records.append(entry)
        cursor += 6
    if count < 80 and len(records) == record_budget and status != "first_8000_TERM":
        status = "external_record_budget"
    return dict(status=status, next_source=cursor, F300_BYTE_after_local_projection=count,
                read_events=reads, records=records, D2_WORD=0,
                source_only=True, natural_execution=False, CPU_execution=False)


def source_reference_union(image):
    """Actual nonflip source-address union under disclosed constructed origins."""
    addresses = set()
    for start, end, _, _, _ in SPECS:
        for p in range(start, end - 2, 6):
            x = int.from_bytes(image[p:p + 2], "big")
            y = sprite_format.signed(int.from_bytes(image[p + 4:p + 6], "big") & 4095, 12)
            view = source_view(image, start, (0x80 - x) & 65535, (0x80 - y) & 65535)
            if view["status"] != "first_8000_TERM" or view["next_source"] != end - 2:
                raise ValueError("constructed original read path did not stop at the first term")
            for event in view["read_events"]:
                addresses.update(range(event["address"], event["address"] + 2))
    return addresses


def schema():
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def exact(items):
        return dict(type="array", prefixItems=items, items=False, minItems=len(items), maxItems=len(items))
    def fixed(value):
        if type(value) is dict: return obj({key: fixed(item) for key, item in value.items()})
        if type(value) is list: return exact([fixed(item) for item in value])
        return dict(type={str: "string", int: "integer", bool: "boolean"}[type(value)], const=value)
    def number(lo, hi): return dict(type="integer", minimum=lo, maximum=hi)
    def cell(address):
        return obj(dict(id=fixed(sprite_format.ident(address)), x_offset=number(-32767, 32767),
            tile_index=number(0, 2047), horizontal_flip=dict(type="boolean"), vertical_flip=dict(type="boolean"),
            palette=number(0, 3), priority=dict(type="boolean"), width_tiles=number(1, 4),
            height_tiles=number(1, 4), y_offset=number(-2048, 2047)))
    properties = {key: fixed(value) for key, value in metadata().items()}
    templates = []
    for spec in SPECS:
        row = template_fixed(spec)
        props = {key: fixed(value) for key, value in row.items()}
        props["records"] = exact([cell(row["start"] + 6 * i) for i in range(row["record_count"])])
        templates.append(obj(props))
    properties["templates"] = exact(templates)
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Full-bit packed sprite source fields with fixed first-8000 framing. Allocation counts are editor contracts; source diagnostics retain state/clipping stops and do not execute CPU or draw frames."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    rows = blocks(rom, fields)
    expected = {p for row in rows for p in range(row["start"], row["end"])}
    actual = source_reference_union(rom)
    if image != rom or actual != expected:
        raise ValueError("serialized whole-ROM roundtrip or conditional source union differs")
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=len(rows),
        record_count=320, first_terminator_WORDs=21, constructed_source_union_bytes=len(actual),
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), source_union_sha256=sha(b"".join(row["data"] for row in rows)),
        blocks=[{key: value for key, value in row.items() if key != "data"}
                | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in rows],
        code_and_other_typed_resources_emitted=False,
        source_read_projection_not_independent_CPU=True)
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=len(rows),
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in UI sprite-template build scope or exact formal bundle")
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
        for name, data in members.items(): put(target / name, data)
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
        if target is not None: put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=EDITABLE_BYTES,
                      exact_canonical=image == rom, bytes=len(image), sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
