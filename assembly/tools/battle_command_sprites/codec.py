"""Eight BE32 pointers and109 first-80-terminated four-BYTE sprite records.

The original03D460 entry indexes03D470 and enters03B13C. Only476 bytes of the
484-byte source allocation are emitted:32 pointer bytes,436 record bytes and
eight terminal BYTEs. Eight unread tail BYTEs remain unknown, not padding.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.vdp_word_streams import format as shared
from tools.compact_sprite_records import codec as compact
from tools.battle_scene_sprites import codec as scene

DEFAULT_ROM = shared.DEFAULT_ROM
FORMAL_ROOT = ROOT / "analysis/battle_command_sprites/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
OUTPUT_ROOT = ROOT / "build/battle_command_sprites"
FORMAT = "candidate-battle-command-four-byte-sprite-fields-v1"
EDITABLE_BYTES = 476
DIR_START, DIR_END, ALLOCATION_END = 0x03D470, 0x03D490, 0x03D654
ENTRY = 0x03D460
ENTRY_BYTES = bytes.fromhex("e542207b200c343c000576004efadcce")
CALLERS = ((0x03D29A, 0x03D45C), (0x03D36C, 0x03D45C), (0x03D440, ENTRY))
ORIGINAL_TARGETS = (0x03D490, 0x03D4CE, 0x03D508, 0x03D58E,
                    0x03D614, 0x03D622, 0x03D634, 0x03D646)
ORIGINAL_COUNTS = (15, 14, 33, 33, 3, 4, 4, 3)
READER_START, READER_END, READER_SHA = scene.READER_START, scene.READER_END, scene.READER_SHA
sha, dump, keys, uint = shared.sha, shared.dump, shared.keys, shared.uint
record, record_bytes = compact.record, compact.record_bytes
source_attribute_word = compact.source_attribute_word
exact_list = scene.exact_list


def ident(start):
    return f"rom_{start:06X}_command_sprite"


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=shared.ROM_SIZE, sha256=shared.ROM_SHA),
                confidence="confirmed_source_encoding_candidate_visual_role",
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != shared.ROM_SIZE or sha(rom) != shared.ROM_SHA:
        raise ValueError("canonical ROM bytes/size/identity required")
    if sha(rom[READER_START:READER_END]) != READER_SHA:
        raise ValueError("original complete sprite reader differs")
    if rom[ENTRY:DIR_START] != ENTRY_BYTES or rom[0x03D45C:ENTRY] != bytes.fromhex("383c0100"):
        raise ValueError("original indexed directory entry/wrapper differs")
    if rom[0x03D43C:0x03D440] != bytes.fromhex("383c0200"):
        raise ValueError("original alternate caller attribute offset differs")
    for pc, entry in CALLERS:
        if rom[pc:pc + 2] != bytes.fromhex("6100") or pc + 2 + int.from_bytes(rom[pc + 2:pc + 4], "big", signed=True) != entry:
            raise ValueError("original direct BSR caller differs")


def layout(rom):
    """Bound discovery by physical targets, but stop at first BYTE0=80."""
    verify_rom(rom)
    targets = tuple(int.from_bytes(rom[p:p + 4], "big") for p in range(DIR_START, DIR_END, 4))
    if targets != ORIGINAL_TARGETS:
        raise ValueError("original eight-slot physical directory differs")
    rows = []
    for start, limit, expected in zip(targets, targets[1:] + (ALLOCATION_END,), ORIGINAL_COUNTS):
        cursor, count = start, 0
        while cursor < limit and rom[cursor] != 128:
            if cursor + 4 > limit or count >= 80:
                raise ValueError("original complete record source differs")
            cursor += 4
            count += 1
        if cursor >= limit or count != expected:
            raise ValueError("original first80 terminal/record count differs")
        rows.append(dict(start=start, end=cursor + 1, allocation_end=limit, count=count))
    if sum(row["end"] - row["start"] for row in rows) != 444:
        raise ValueError("original444 descriptor-byte source cost differs")
    return rows


def directory_topology():
    return dict(id="directory_03D470", start=DIR_START, end=DIR_END, LONG_order="big",
                source_entry=ENTRY, pointer_read=0x03D462, indexed_PC_base=0x03D464,
                reader=READER_START, direct_callers=[dict(pc=pc, target=entry) for pc, entry in CALLERS])


def descriptor_topology(row):
    return dict(id=ident(row["start"]), start=row["start"], end=row["end"],
                terminator_byte=128, source_record_bytes=4,
                excluded_unread_interval=[row["end"], row["allocation_end"]])


def fixed_row(row, fixed, mutable, label):
    keys(row, set(fixed) | set(mutable), label)
    for key, value in fixed.items():
        shared.same(row[key], value, label + "." + key)


def extract(rom):
    rows = layout(rom)
    fields = metadata()
    fields["directory"] = dict(**directory_topology(), targets=[ident(start) for start in ORIGINAL_TARGETS])
    fields["descriptors"] = [dict(**descriptor_topology(row), records=[record(rom[p:p + 4])
        for p in range(row["start"], row["end"] - 1, 4)]) for row in rows]
    blocks(rom, fields)
    return fields


def blocks(rom, fields):
    rows = layout(rom)
    fixed_row(fields, metadata(), {"directory", "descriptors"}, "package")
    directory = fields["directory"]
    fixed_row(directory, directory_topology(), {"targets"}, "directory")
    catalog = {ident(row["start"]): row["start"] for row in rows}
    targets = exact_list(directory["targets"], 8, "pointer slots")
    if any(type(target) is not str or target not in catalog for target in targets):
        raise ValueError("pointer must name an existing complete source in this physical editor catalog")
    result = [dict(id=directory["id"], start=DIR_START, end=DIR_END,
        data=b"".join(catalog[target].to_bytes(4, "big") for target in targets),
        role="candidate_battle_command_BE32_directory")]
    for descriptor, row in zip(exact_list(fields["descriptors"], 8, "descriptors"), rows):
        fixed_row(descriptor, descriptor_topology(row), {"records"}, "descriptor")
        data = b"".join(record_bytes(value) for value in exact_list(descriptor["records"], row["count"], "records")) + b"\x80"
        if len(data) != row["end"] - row["start"]:
            raise ValueError("fixed first-terminal source cost differs")
        result.append(dict(id=descriptor["id"], start=row["start"], end=row["end"],
            data=data, role="candidate_battle_command_four_BYTE_sprite_records"))
    result.sort(key=lambda row: row["start"])
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES or any(a["end"] > b["start"] for a, b in zip(result, result[1:])):
        raise ValueError("nonoverlapping physical476-byte emit scope differs")
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def resolve_original_directory(rom, selector_word):
    """Original WORD<<2 wrap then signed index, without a physical-slot clamp."""
    verify_rom(rom)
    uint(selector_word, 65535, "original selector WORD")
    offset = (selector_word << 2) & 65535
    if offset >= 32768:
        offset -= 65536
    address = DIR_START + offset
    if address < 0 or address + 4 > len(rom):
        raise ValueError("original pointer read outside supplied ROM")
    return dict(address=address, target=int.from_bytes(rom[address:address + 4], "big"),
                in_physical_editor_catalog=DIR_START <= address < DIR_END)


def load_fields(data):
    return shared.load_json(data)


def schema(rom):
    fields = extract(rom)
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({key: fixed(item) for key, item in value.items()})
        if type(value) is list:
            return dict(type="array", prefixItems=[fixed(item) for item in value], items=False, minItems=len(value), maxItems=len(value))
        return dict(type={str: "string", int: "integer"}[type(value)], const=value)
    def integer(low, high):
        return dict(type="integer", minimum=low, maximum=high)
    row_schema = obj(dict(sat_y_delta=integer(-127, 127), sat_x_delta=integer(-128, 127),
        width_tiles=integer(1, 4), height_tiles=integer(1, 4), attribute_nibble=integer(0, 15), tile_low_byte=integer(0, 255)))
    directory = fields["directory"]
    properties = {key: fixed(value) for key, value in directory.items() if key != "targets"}
    properties["targets"] = dict(type="array", minItems=8, maxItems=8, items=dict(type="string", enum=directory["targets"]))
    descriptors = []
    for row in fields["descriptors"]:
        row_properties = {key: fixed(value) for key, value in row.items() if key != "records"}
        row_properties["records"] = dict(type="array", minItems=len(row["records"]), maxItems=len(row["records"]), items=row_schema)
        descriptors.append(obj(row_properties))
    properties = {key: fixed(value) for key, value in metadata().items()} | dict(directory=obj(properties),
        descriptors=dict(type="array", prefixItems=descriptors, items=False, minItems=8, maxItems=8))
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Runtime additionally pins physical targets, costs, first80 BYTE boundaries and consumer bytes. No unread tail, natural selector clamp or full SAT writer is adopted."
    return result


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError("whole-ROM serialized source-field roundtrip differs")
    rows = layout(rom)
    unknown = [[row["end"], row["allocation_end"]] for row in rows]
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=9, pointer_bytes=32,
        physical_pointer_slots=8, descriptor_bytes=444, descriptors=8, four_BYTE_records=109, terminal_BYTEs=8,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), scope_container=[DIR_START, ALLOCATION_END],
        original_entry=dict(start=ENTRY, end=DIR_START, bytes=ENTRY_BYTES.hex(), pointer_read=0x03D462,
            indexed_PC_base=0x03D464, signed_BYTE_displacement=12, resolved_directory=DIR_START,
            caller_attribute_D2_WORD=5, caller_attribute_D3_BYTE=0, reader_tail_JMP=0x03D46C),
        original_reader=dict(start=READER_START, end=READER_END, sha256=READER_SHA,
            terminal_check=0x03B19C, record_step=0x03B22A, attribute_transform=[0x03B210, 0x03B224],
            original_initial_and_each_record_sprite_count_check=[0x03B140, 0x03B22C], original_count_limit=80),
        direct_callers=[dict(pc=pc, target=entry) for pc, entry in CALLERS],
        original_D4_profiles=[dict(wrapper=0x03D45C, D4_WORD=0x0100), dict(load=0x03D43C, D4_WORD=0x0200)],
        source_profiles=[dict(id=ident(row["start"]), start=row["start"], end=row["end"],
            complete_records=row["count"], source_sha256=sha(rom[row["start"]:row["end"]])) for row in rows],
        unknown_intervals=unknown, unread_bytes_excluded=8, terminator_is_one_BYTE_not_full_stride=True,
        selector_semantics="D2.W<<2 wraps16; signed indexed offset from extension WORD PC; no catalog-count CPU clamp",
        reused_implementation=["compact_sprite_records.record", "record_bytes", "source_attribute_word"],
        source_encoding_confidence="confirmed", visual_role_confidence="candidate",
        attribute_nibble_is_source_not_absolute_palette_flip=True, independent_CPU_comparison=False,
        natural_selector_domain_complete=False, complete_SAT_writer_reimplemented=False, edited_gameplay_safety="unknown")
    members = {"fields.json": dump(fields), "fields.schema.json": dump(schema(rom)), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}, independent_CPU_comparison=False))
    return members


def fresh_output(value):
    path = shared.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError("output must stay in build/battle_command_sprites or be the fresh formal generated directory")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "import", "verify"))
    parser.add_argument("--rom", default=str(DEFAULT_ROM))
    parser.add_argument("--fields", default=str(DEFAULT_FIELDS))
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    target = None
    if args.command != "verify":
        if args.output is None:
            raise ValueError("fresh output required")
        target = fresh_output(args.output)  # Output authority BEFORE input reads.
        if args.command == "import" and target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin required")
    elif args.output is not None:
        raise ValueError("verify does not write")
    rom = shared.read_bounded(args.rom, shared.ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            shared.put(target / name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES, members={name: sha(data) for name, data in members.items()})
    else:
        image = rebuild(rom, load_fields(shared.read_bounded(args.fields, shared.MAX_JSON)))
        if target is not None:
            shared.put(target, image)
        result = dict(path=None if target is None else str(target), sha256=sha(image), exact_canonical=image == rom, editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
