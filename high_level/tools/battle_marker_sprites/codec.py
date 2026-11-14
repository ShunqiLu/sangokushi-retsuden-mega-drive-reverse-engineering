"""Seven first-80 source descriptors and one four-slot BE32 marker directory.

Only123 bytes are typed:25 complete four-BYTE records, seven80 terminal BYTEs
and16 pointer bytes. The81 unread bytes after first terminals stay unknown.
Source grammar helpers reuse frozen codecs; their scopes/files do not change.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

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
from tools.battle_command_sprites import codec as command

DEFAULT_ROM = shared.DEFAULT_ROM
FORMAL_ROOT = ROOT / "analysis/battle_marker_sprites/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
OUTPUT_ROOT = ROOT / "build/battle_marker_sprites"
FORMAT = "candidate-battle-marker-first80-sprite-fields-v1"
EDITABLE_BYTES = 123
DIR_START, DIR_END = 0x0417CE, 0x0417DE
DIRECT_TARGETS = (0x03E28E, 0x03E396, 0x0415E2)
INDEXED_TARGETS = (0x0417DE, 0x0417E4, 0x0417EA, 0x0417F0)
# Physical source start, allocation end, expected nonterminal record count.
SOURCES = ((0x03E28E, 0x03E298, 2), (0x03E396, 0x03E42A, 18), (0x0415E2, 0x0415E8, 1),
           (0x0417DE, 0x0417E4, 1), (0x0417E4, 0x0417EA, 1),
           (0x0417EA, 0x0417F0, 1), (0x0417F0, 0x0417F6, 1))
CONSUMER_BYTES = (
    (0x03E276, "41fa00164e71323c008c343c01047600383c04004efaceb0"),
    (0x03E37A, "41fa001a4e71343c" "01047600383c04004efacdb0"),
    (0x0415C4, "343c00047600383c" "010041fa00124e714eba9b66"),
    (0x0417AE, reference_value(__name__, 'CONSUMER_BYTES')))
BSR_CALLERS = ((0x03E2A4, 0x03E37A), (0x03E326, 0x03E37A),
               (0x03E35E, 0x03E37A), (0x03E2B0, 0x03E254))
READER_START, READER_END, READER_SHA = scene.READER_START, scene.READER_END, scene.READER_SHA
sha, dump, keys, uint = shared.sha, shared.dump, shared.keys, shared.uint
record, record_bytes, source_attribute_word = compact.record, compact.record_bytes, compact.source_attribute_word
exact_list, fixed_row = scene.exact_list, command.fixed_row


def ident(start):
    return f"rom_{start:06X}_marker_sprite"


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=shared.ROM_SIZE, sha256=shared.ROM_SHA),
                confidence="confirmed_source_encoding_candidate_visual_role",
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != shared.ROM_SIZE or sha(rom) != shared.ROM_SHA:
        raise ValueError("canonical ROM bytes/size/identity required")
    if sha(rom[READER_START:READER_END]) != READER_SHA:
        raise ValueError("original complete marker sprite reader differs")
    for address, raw in CONSUMER_BYTES:
        data = bytes.fromhex(raw)
        if rom[address:address + len(data)] != data:
            raise ValueError("original direct/indexed consumer bytes differ")
    for pc, target in BSR_CALLERS:
        if rom[pc:pc + 2] != bytes.fromhex("6100") or pc + 2 + int.from_bytes(rom[pc + 2:pc + 4], "big", signed=True) != target:
            raise ValueError("original direct marker caller differs")
    if tuple(int.from_bytes(rom[p:p + 4], "big") for p in range(DIR_START, DIR_END, 4)) != INDEXED_TARGETS:
        raise ValueError("original four-slot directory differs")


def layout(rom):
    verify_rom(rom)
    rows = []
    for start, limit, expected in SOURCES:
        cursor, count = start, 0
        while cursor < limit and rom[cursor] != 128:
            if cursor + 4 > limit or count >= 80:
                raise ValueError("bounded complete original records differ")
            cursor += 4
            count += 1
        if cursor >= limit or count != expected:
            raise ValueError("original first80 terminal/count differs")
        rows.append(dict(start=start, end=cursor + 1, allocation_end=limit, count=count))
    if sum(row["end"] - row["start"] for row in rows) != 107:
        raise ValueError("original107 record/terminal-byte source cost differs")
    return rows


def directory_topology():
    return dict(id="directory_0417CE", start=DIR_START, end=DIR_END, LONG_order="big",
                selector_shift=0x0417B2, pointer_read=0x0417B4, indexed_PC_base=0x0417B6,
                signed_BYTE_displacement=24, reader=READER_START, reader_tail_JMP=0x0417CA)


def descriptor_topology(row):
    return dict(id=ident(row["start"]), start=row["start"], end=row["end"], terminator_byte=128,
                source_record_bytes=4, source_pointer_kind="direct_PC_LEA" if row["start"] in DIRECT_TARGETS else "indexed_BE32",
                excluded_unread_interval=[row["end"], row["allocation_end"]])


def extract(rom):
    rows = layout(rom)
    fields = metadata()
    fields["directory"] = dict(**directory_topology(), targets=[ident(start) for start in INDEXED_TARGETS])
    fields["descriptors"] = [dict(**descriptor_topology(row), records=[record(rom[p:p + 4])
        for p in range(row["start"], row["end"] - 1, 4)]) for row in rows]
    blocks(rom, fields)
    return fields


def blocks(rom, fields):
    rows = layout(rom)
    fixed_row(fields, metadata(), {"directory", "descriptors"}, "package")
    directory = fields["directory"]
    fixed_row(directory, directory_topology(), {"targets"}, "directory")
    catalog = {ident(start): start for start in INDEXED_TARGETS}
    targets = exact_list(directory["targets"], 4, "physical pointer slots")
    if any(type(target) is not str or target not in catalog for target in targets):
        raise ValueError("pointer must name an existing complete source in its physical indexed catalog")
    result = [dict(id=directory["id"], start=DIR_START, end=DIR_END,
        data=b"".join(catalog[target].to_bytes(4, "big") for target in targets), role="candidate_marker_sprite_BE32_directory")]
    for descriptor, row in zip(exact_list(fields["descriptors"], 7, "descriptors"), rows):
        fixed_row(descriptor, descriptor_topology(row), {"records"}, "descriptor")
        data = b"".join(record_bytes(value) for value in exact_list(descriptor["records"], row["count"], "records")) + b"\x80"
        if len(data) != row["end"] - row["start"]:
            raise ValueError("fixed first-terminal source cost differs")
        result.append(dict(id=descriptor["id"], start=row["start"], end=row["end"], data=data,
            role="candidate_marker_sprite_four_BYTE_records"))
    result.sort(key=lambda row: row["start"])
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES or any(a["end"] > b["start"] for a, b in zip(result, result[1:])):
        raise ValueError("fixed nonoverlapping123-byte physical emit scope differs")
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def resolve_original_directory(image, selector_WORD):
    """Full original WORD wrap and signed indexing; accepts edited images."""
    if type(image) is not bytes or len(image) != shared.ROM_SIZE:
        raise ValueError("diagnostic read requires a complete bytes image")
    offset = (uint(selector_WORD, 65535, "selector WORD") << 2) & 65535
    if offset >= 32768:
        offset -= 65536
    address = DIR_START + offset
    return dict(address=address, target=int.from_bytes(image[address:address + 4], "big"),
                in_physical_editor_catalog=DIR_START <= address < DIR_END)


def load_fields(data):
    return shared.load_json(data)


def schema(rom):
    fields = extract(rom)
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def exact(rows):
        return dict(type="array", prefixItems=rows, items=False, minItems=len(rows), maxItems=len(rows))
    def fixed(value):
        if type(value) is dict:
            return obj({key: fixed(item) for key, item in value.items()})
        if type(value) is list:
            return exact([fixed(item) for item in value])
        return dict(type={str: "string", int: "integer"}[type(value)], const=value)
    def number(low, high):
        return dict(type="integer", minimum=low, maximum=high)
    source_record = obj(dict(sat_y_delta=number(-127, 127), sat_x_delta=number(-128, 127),
        width_tiles=number(1, 4), height_tiles=number(1, 4), attribute_nibble=number(0, 15), tile_low_byte=number(0, 255)))
    directory = fields["directory"]
    dir_properties = {key: fixed(value) for key, value in directory.items() if key != "targets"}
    dir_properties["targets"] = dict(type="array", minItems=4, maxItems=4,
        items=dict(type="string", enum=directory["targets"]))
    descriptors = []
    for row in fields["descriptors"]:
        properties = {key: fixed(value) for key, value in row.items() if key != "records"}
        properties["records"] = dict(type="array", minItems=len(row["records"]), maxItems=len(row["records"]), items=source_record)
        descriptors.append(obj(properties))
    result = obj({**{key: fixed(value) for key, value in metadata().items()},
                  "directory": obj(dir_properties), "descriptors": exact(descriptors)})
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Runtime pins original consumer metadata, physical catalogs, record capacities and first80 BYTEs. Unread tails and natural selector/SAT domains are not adopted."
    return result


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError("whole-ROM serialized marker-source roundtrip differs")
    rows = layout(rom)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=8, pointer_bytes=16,
        physical_pointer_slots=4, descriptors=7, four_BYTE_records=25, record_bytes=100, terminal_BYTEs=7,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        original_reader=dict(start=READER_START, end=READER_END, sha256=READER_SHA,
            terminal_check=0x03B19C, record_step=0x03B22A, attribute_transform=[0x03B210, 0x03B224], original_count_limit=80),
        original_consumers=[dict(start=pc, end=pc + len(raw) // 2, bytes=raw) for pc, raw in CONSUMER_BYTES],
        original_direct_LEAs=[dict(address=0x03E276, PC_base=0x03E278, displacement_WORD=0x0016, target=0x03E28E),
            dict(address=0x03E37A, PC_base=0x03E37C, displacement_WORD=0x001A, target=0x03E396),
            dict(address=0x0415CE, PC_base=0x0415D0, displacement_WORD=0x0012, target=0x0415E2)],
        original_attribute_profiles=[dict(sources=[0x03E28E, 0x03E396], D2_WORD=0x0104, D3_BYTE=0, D4_WORD=0x0400),
            dict(sources=[0x0415E2], D2_WORD=4, D3_BYTE=0, D4_WORD=0x0100),
            dict(sources=list(INDEXED_TARGETS), D2_WORD=4, D3_BYTE=0, D4_WORD=0x0300)],
        original_BSR_callers=[dict(address=pc, target=target) for pc, target in BSR_CALLERS],
        source_profiles=[dict(id=ident(row["start"]), start=row["start"], end=row["end"], records=row["count"],
            sha256=sha(rom[row["start"]:row["end"]])) for row in rows],
        unknown_intervals=[[row["end"], row["allocation_end"]] for row in rows], unread_bytes_excluded=81,
        other_unadopted_before_source=[0x03E38E, 0x03E396], other_direction_WORD_table_not_adopted=[0x0415E8, 0x041608],
        terminator_is_one_BYTE_not_full_stride=True, attribute_nibble_is_source_not_absolute_palette_flip=True,
        selector_semantics="D0.W<<2 wraps16 then signed index from PC extension; four slots are not a CPU clamp",
        reused_implementation=["compact_sprite_records.record", "record_bytes", "source_attribute_word", "battle_command_sprites.fixed_row"],
        natural_selector_domain_complete=False, independent_CPU_comparison=False,
        complete_SAT_writer_reimplemented=False, edited_gameplay_safety="unknown")
    members = {"fields.json": dump(fields), "fields.schema.json": dump(schema(rom)), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}, independent_CPU_comparison=False))
    return members


def fresh_output(value):
    path = shared.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError("output must stay in build/battle_marker_sprites or be the fresh formal generated directory")
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
