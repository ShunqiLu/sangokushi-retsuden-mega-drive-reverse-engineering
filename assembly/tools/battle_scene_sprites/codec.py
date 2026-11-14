"""Three BE32 catalogs and36 first-80-terminated four-BYTE sprite sources.

03BBC2/03C6CC/03CE08 resolve indexed pointers and enter03B13C. The reader's
record grammar is shared with compact_sprite_records, but source ownership is
disjoint. Only144 pointer bytes and2544 descriptor bytes are emitted. The294
bytes following first80 terminators remain unknown, including one259-byte gap.
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

DEFAULT_ROM = shared.DEFAULT_ROM
FORMAL_ROOT = ROOT / "analysis/battle_scene_sprites/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
OUTPUT_ROOT = ROOT / "build/battle_scene_sprites"
FORMAT = "candidate-battle-scene-four-byte-sprite-fields-v1"
EDITABLE_BYTES = 2688
# id, directory start/end, candidate source allocation end, original entry.
DIRECTORIES = (("directory_03BBD6", 0x03BBD6, 0x03BC0A, 0x03C192, 0x03BBC2),
               ("directory_03C6DC", 0x03C6DC, 0x03C714, 0x03C970, 0x03C6CC),
               ("directory_03CE1C", 0x03CE1C, 0x03CE40, 0x03D172, 0x03CE08))
ENTRY_BYTES = {0x03BBC2: bytes.fromhex("e542207b2010343c" "00057600383c01004efaf568"),
               0x03C6CC: bytes.fromhex("e542207b200c343c000576004efaea62"),
               0x03CE08: bytes.fromhex("e542207b2010343c" "00057600383c02004efae322")}
READER_START = 0x03B13C
READER_END = 0x03B23C
READER_SHA = reference_value(__name__, 'READER_SHA')
CALLERS = {"directory_03BBD6": [0x03B8DC, 0x03BAD2, 0x03BAE0],
           "directory_03C6DC": [0x03C3C0, 0x03C3E0, 0x03C400, 0x03C4C2, 0x03C5EE,
                                0x03C618, 0x03C638, 0x03C658, 0x03C678],
           "directory_03CE1C": [0x03CBDC, 0x03CC9A, 0x03CCA8, 0x03CDB8]}
sha = shared.sha
dump = shared.dump
keys = shared.keys
uint = shared.uint
record = compact.record
record_bytes = compact.record_bytes
source_attribute_word = compact.source_attribute_word


def ident(start):
    return f"rom_{start:06X}_scene_sprite"


def metadata():
    return dict(format=FORMAT,
                canonical_source=dict(size=shared.ROM_SIZE, sha256=shared.ROM_SHA),
                confidence="confirmed_source_encoding_candidate_visual_role",
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def exact_list(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ": exact physical source count required")
    return value


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != shared.ROM_SIZE or sha(rom) != shared.ROM_SHA:
        raise ValueError("canonical ROM bytes/size/identity required")
    if sha(rom[READER_START:READER_END]) != READER_SHA:
        raise ValueError("original complete sprite reader differs")
    for start, raw in ENTRY_BYTES.items():
        if rom[start:start + len(raw)] != raw:
            raise ValueError("original indexed directory entry differs")
    for name, _, _, _, entry in DIRECTORIES:
        for pc in CALLERS[name]:
            if rom[pc:pc + 2] != bytes.fromhex("6100"):
                raise ValueError("original direct BSR opcode differs")
            if pc + 2 + int.from_bytes(rom[pc + 2:pc + 4], "big", signed=True) != entry:
                raise ValueError("original direct caller target differs")


def directory_topology(spec):
    name, start, end, _, entry = spec
    return dict(id=name, start=start, end=end, LONG_order="big",
                source_entry=entry, pointer_read=entry + 2, reader=READER_START,
                direct_callers=CALLERS[name])


def descriptor_topology(row):
    return dict(id=ident(row["start"]), directory_catalog=row["directory"],
                start=row["start"], end=row["end"], terminator_byte=128,
                source_record_bytes=4, excluded_unread_interval=[row["end"], row["allocation_end"]])


def layout(rom):
    """Use actual pointers and first80 markers, never the full pointer stride."""
    verify_rom(rom)
    descriptors = []
    directory_targets = {}
    for name, start, end, allocation_end, _ in DIRECTORIES:
        targets = [int.from_bytes(rom[p:p + 4], "big") for p in range(start, end, 4)]
        ordered = sorted(set(targets))
        if len(ordered) != len(targets) or not ordered or ordered[0] != end:
            raise ValueError("original directory uniqueness/source start differs")
        if any(p < end or p >= allocation_end or p & 1 for p in ordered):
            raise ValueError("original source pointer outside candidate allocation")
        directory_targets[name] = targets
        for source_start, limit in zip(ordered, ordered[1:] + [allocation_end]):
            cursor = source_start
            count = 0
            while cursor < limit and rom[cursor] != 128:
                if cursor + 4 > limit or count >= 80:
                    raise ValueError("original bounded complete source records differ")
                cursor += 4
                count += 1
            if cursor >= limit or not count:
                raise ValueError("original descriptor lacks first80 terminal BYTE")
            descriptors.append(dict(directory=name, start=source_start, end=cursor + 1,
                                    allocation_end=limit, count=count))
    if (len(descriptors) != 36 or sum(row["count"] for row in descriptors) != 627
            or sum(row["end"] - row["start"] for row in descriptors) != 2544):
        raise ValueError("original36/627/2544 source partition differs")
    return descriptors, directory_targets


def extract(rom):
    rows, targets = layout(rom)
    fields = metadata()
    fields["directories"] = [dict(**directory_topology(spec),
        targets=[ident(start) for start in targets[spec[0]]]) for spec in DIRECTORIES]
    fields["descriptors"] = [dict(**descriptor_topology(row),
        records=[record(rom[p:p + 4]) for p in range(row["start"], row["end"] - 1, 4)]) for row in rows]
    blocks(rom, fields)
    return fields


def blocks(rom, fields):
    rows, _ = layout(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"directories", "descriptors"}, "package")
    for key, value in fixed.items():
        shared.same(fields[key], value, "package." + key)
    result = []
    catalogs = {name: {ident(row["start"]): row["start"] for row in rows if row["directory"] == name}
                for name, _, _, _, _ in DIRECTORIES}
    for directory, spec in zip(exact_list(fields["directories"], 3, "directories"), DIRECTORIES):
        fixed = directory_topology(spec)
        keys(directory, set(fixed) | {"targets"}, "directory")
        for key, value in fixed.items():
            shared.same(directory[key], value, "directory." + key)
        name, start, end, _, _ = spec
        targets = exact_list(directory["targets"], (end - start) // 4, "pointer slots")
        catalog = catalogs[name]
        if any(type(target) is not str or target not in catalog for target in targets):
            raise ValueError("pointer must name an existing complete source in its physical editor catalog")
        data = b"".join(catalog[target].to_bytes(4, "big") for target in targets)
        result.append(dict(id=name, start=start, end=end, data=data,
                           role="candidate_scene_sprite_BE32_directory"))
    for descriptor, row in zip(exact_list(fields["descriptors"], 36, "descriptors"), rows):
        fixed = descriptor_topology(row)
        keys(descriptor, set(fixed) | {"records"}, "descriptor")
        for key, value in fixed.items():
            shared.same(descriptor[key], value, "descriptor." + key)
        records = exact_list(descriptor["records"], row["count"], "source records")
        data = b"".join(record_bytes(value) for value in records) + b"\x80"
        if len(data) != row["end"] - row["start"]:
            raise ValueError("fixed first-terminal source cost differs")
        result.append(dict(id=descriptor["id"], start=row["start"], end=row["end"], data=data,
                           role="candidate_scene_four_BYTE_sprite_records"))
    result.sort(key=lambda row: row["start"])
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES:
        raise ValueError("physical source emit scope differs")
    if any(a["end"] > b["start"] for a, b in zip(result, result[1:])):
        raise ValueError("overlapping physical source fields")
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def resolve_original_directory(rom, directory_id, selector_word):
    """Original WORD<<2 wraps16 then signed PC indexing; no slot-count clamp."""
    verify_rom(rom)
    uint(selector_word, 65535, "original selector WORD")
    if type(directory_id) is not str or directory_id not in {spec[0] for spec in DIRECTORIES}:
        raise ValueError("unknown original directory")
    _, start, end, _, _ = next(spec for spec in DIRECTORIES if spec[0] == directory_id)
    offset = (selector_word << 2) & 65535
    if offset >= 32768:
        offset -= 65536
    address = start + offset
    if address < 0 or address + 4 > len(rom):
        raise ValueError("original pointer read outside supplied ROM")
    return dict(address=address, target=int.from_bytes(rom[address:address + 4], "big"),
                in_physical_editor_catalog=start <= address < end)


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
            return dict(type="array", prefixItems=[fixed(item) for item in value],
                        items=False, minItems=len(value), maxItems=len(value))
        return dict(type={str: "string", int: "integer"}[type(value)], const=value)
    def integer(low, high):
        return dict(type="integer", minimum=low, maximum=high)
    record_schema = obj(dict(sat_y_delta=integer(-127, 127), sat_x_delta=integer(-128, 127),
        width_tiles=integer(1, 4), height_tiles=integer(1, 4), attribute_nibble=integer(0, 15),
        tile_low_byte=integer(0, 255)))
    directories = []
    for row in fields["directories"]:
        properties = {key: fixed(value) for key, value in row.items() if key != "targets"}
        properties["targets"] = dict(type="array", minItems=len(row["targets"]), maxItems=len(row["targets"]),
                                    items=dict(type="string", enum=row["targets"]))
        directories.append(obj(properties))
    descriptors = []
    for row in fields["descriptors"]:
        properties = {key: fixed(value) for key, value in row.items() if key != "records"}
        properties["records"] = dict(type="array", minItems=len(row["records"]), maxItems=len(row["records"]),
                                    items=record_schema)
        descriptors.append(obj(properties))
    properties = {key: fixed(value) for key, value in metadata().items()}
    for key, rows in (("directories", directories), ("descriptors", descriptors)):
        properties[key] = dict(type="array", prefixItems=rows, items=False, minItems=len(rows), maxItems=len(rows))
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Source fields only. Runtime enforces pinned addresses, physical catalogs and first-terminal boundaries. No unread tail or global selector/SAT domain is owned."
    return result


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError("whole-ROM serialized source-field roundtrip differs")
    rows, _ = layout(rom)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=39,
        pointer_bytes=144, physical_pointer_slots=36, directory_slot_counts=[13, 14, 9],
        descriptor_bytes=2544, descriptors=36, four_BYTE_records=627, terminal_BYTEs=36,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        original_reader=dict(start=READER_START, end=READER_END, sha256=READER_SHA,
            terminal_check=0x03B19C, record_step=0x03B22A, attribute_transform=[0x03B210, 0x03B224],
            original_initial_and_each_record_sprite_count_check=[0x03B140, 0x03B22C],
            original_count_limit=80, source_BYTE0_to_SAT_WORD0=0x03B19C,
            source_BYTE3_to_SAT_WORD3=0x03B1C2),
        pointer_consumer_entries=[spec[4] for spec in DIRECTORIES],
        selector_semantics="D2.W<<2 wraps16; signed indexed offset from extension WORD PC; no catalog-count CPU clamp",
        source_profiles=[dict(id=ident(row["start"]), start=row["start"], end=row["end"],
            complete_records=row["count"], source_sha256=sha(rom[row["start"]:row["end"]])) for row in rows],
        unknown_intervals=[[row["end"], row["allocation_end"]] for row in rows], unread_bytes_excluded=294,
        terminator_is_one_BYTE_not_full_stride=True,
        reused_implementation=["compact_sprite_records.codec.record", "record_bytes", "source_attribute_word"],
        source_encoding_confidence="confirmed", visual_role_confidence="candidate",
        attribute_nibble_is_source_not_absolute_palette_flip=True,
        natural_selector_domain_complete=False, independent_CPU_comparison=False,
        complete_SAT_writer_reimplemented=False, edited_gameplay_safety="unknown",
        unknowns=["Physical editor catalogs are not natural frame/selector domains.",
            "Initial sprite count, origin/clipping, RAM linkage and caller attributes affect writes.",
            "Unread terminator tails and the259-byte gap are not padding or additional records here."])
    members = {"fields.json": dump(fields), "fields.schema.json": dump(schema(rom)),
               "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()},
        independent_CPU_comparison=False))
    return members


def fresh_output(value):
    path = shared.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError("output must stay in build/battle_scene_sprites or be the fresh formal generated directory")
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
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES,
                      members={name: sha(data) for name, data in members.items()})
    else:
        fields = load_fields(shared.read_bounded(args.fields, shared.MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            shared.put(target, image)
        result = dict(path=None if target is None else str(target), sha256=sha(image),
                      exact_canonical=image == rom, editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
