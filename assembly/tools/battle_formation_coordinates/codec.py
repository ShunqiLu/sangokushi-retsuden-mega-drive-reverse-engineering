"""Five BE32 formation pointers and80 pairs of complete source WORDs.

The340-byte physical source is not a natural selector/count clamp. Two original
object loops limit reads to16 pairs but may stop earlier after copying coordinates;
the4197A conditional reader has no16-pair guard and can read following sources.
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
from tools.battle_scene_sprites import codec as scene

DEFAULT_ROM = shared.DEFAULT_ROM
FORMAL_ROOT = ROOT / "analysis/battle_formation_coordinates/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
OUTPUT_ROOT = ROOT / "build/battle_formation_coordinates"
FORMAT = "candidate-battle-formation-full-WORD-coordinate-fields-v1"
EDITABLE_BYTES = 340
DIR_START, DIR_END, END = 0x041A58, 0x041A6C, 0x041BAC
TARGETS = (0x041A6C, 0x041AAC, 0x041AEC, 0x041B2C, 0x041B6C)
# Original selector/read-stop regions, independently pinned canonical bytes.
CONSUMER_SPANS = ((0x03F630, 0x03F6C2, reference_value(__name__, 'CONSUMER_SPANS')),
                  (0x03F6C2, 0x03F760, reference_value(__name__, 'CONSUMER_SPANS_2')),
                  (0x04194E, 0x0419D0, reference_value(__name__, 'CONSUMER_SPANS_3')))
# ASL.W2, PC-relative LEA, LONG pointer read.
DIRECTORY_READS = ((0x03F64C, 0x03F64E, 0x2408, 0x03F654),
                   (0x03F6F2, 0x03F6F4, 0x2362, 0x03F6FA),
                   (0x04195C, 0x04195E, 0x00F8, 0x041964))
sha, dump, keys, uint = shared.sha, shared.dump, shared.keys, shared.uint
exact_list = scene.exact_list


def ident(start):
    return f"rom_{start:06X}_formation"


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=shared.ROM_SIZE, sha256=shared.ROM_SHA),
                confidence="confirmed_source_encoding_conditional_reads_candidate_visual_role",
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != shared.ROM_SIZE or sha(rom) != shared.ROM_SHA:
        raise ValueError("canonical ROM bytes/size/identity required")
    for start, end, digest in CONSUMER_SPANS:
        if sha(rom[start:end]) != digest:
            raise ValueError("original conditional reader/stop region differs")
    for shift, lea, displacement, read in DIRECTORY_READS:
        if (rom[shift:shift + 2] != bytes.fromhex("e540") or
            rom[lea:lea + 4] != bytes.fromhex("41fa") + displacement.to_bytes(2, "big") or
            lea + 2 + displacement != DIR_START or rom[read:read + 4] != bytes.fromhex("2a700000")):
            raise ValueError("original indexed directory address calculation differs")
    targets = tuple(int.from_bytes(rom[p:p + 4], "big") for p in range(DIR_START, DIR_END, 4))
    if targets != TARGETS or TARGETS[-1] + 64 != END:
        raise ValueError("original five-slot/16-pair physical source partition differs")


def directory_topology():
    return dict(id="directory_041A58", start=DIR_START, end=DIR_END, LONG_order="big",
        physical_slots=5, pointer_reads=[dict(shift=shift, LEA=lea, PC_base=lea + 2,
            displacement_WORD=disp, pointer_read=read) for shift, lea, disp, read in DIRECTORY_READS])


def template_topology(start):
    return dict(id=ident(start), start=start, end=start + 64, physical_pairs=16,
                source_pair_bytes=4, WORD_order="big", termination="caller_control_not_source_marker")


def pair_topology(start, index):
    return dict(id=f"rom_{start + 4 * index:06X}_coordinate_pair", index=index, address=start + 4 * index)


def fixed_row(row, fixed, mutable, label):
    keys(row, set(fixed) | set(mutable), label)
    for key, value in fixed.items():
        shared.same(row[key], value, label + "." + key)


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["directory"] = dict(**directory_topology(), targets=[ident(start) for start in TARGETS])
    fields["templates"] = [dict(**template_topology(start), pairs=[dict(**pair_topology(start, i),
        X_source_WORD=int.from_bytes(rom[start + 4 * i:start + 4 * i + 2], "big"),
        Y_source_WORD=int.from_bytes(rom[start + 4 * i + 2:start + 4 * i + 4], "big"))
        for i in range(16)]) for start in TARGETS]
    blocks(rom, fields)
    return fields


def blocks(rom, fields):
    verify_rom(rom)
    fixed_row(fields, metadata(), {"directory", "templates"}, "package")
    directory = fields["directory"]
    fixed_row(directory, directory_topology(), {"targets"}, "directory")
    catalog = {ident(start): start for start in TARGETS}
    targets = exact_list(directory["targets"], 5, "physical pointer slots")
    if any(type(target) is not str or target not in catalog for target in targets):
        raise ValueError("pointer must name an existing complete physical coordinate template")
    result = [dict(id=directory["id"], start=DIR_START, end=DIR_END,
        data=b"".join(catalog[target].to_bytes(4, "big") for target in targets),
        role="candidate_formation_BE32_directory")]
    for template, start in zip(exact_list(fields["templates"], 5, "physical templates"), TARGETS):
        fixed_row(template, template_topology(start), {"pairs"}, "template")
        data = bytearray()
        for index, pair in enumerate(exact_list(template["pairs"], 16, "physical source pairs")):
            fixed_row(pair, pair_topology(start, index), {"X_source_WORD", "Y_source_WORD"}, "coordinate pair")
            for key in ("X_source_WORD", "Y_source_WORD"):
                data.extend(uint(pair[key], 65535, key).to_bytes(2, "big"))
        result.append(dict(id=template["id"], start=start, end=start + 64,
            data=bytes(data), role="candidate_full_WORD_formation_coordinates"))
    if (sum(len(row["data"]) for row in result) != EDITABLE_BYTES or
        any(len(row["data"]) != row["end"] - row["start"] for row in result) or
        any(a["end"] > b["start"] for a, b in zip(result, result[1:]))):
        raise ValueError("fixed nonoverlapping340-byte source cost differs")
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def complete_image(image):
    if type(image) is not bytes or len(image) != shared.ROM_SIZE:
        raise ValueError("diagnostic read requires a complete bytes image")


def resolve_original_directory(image, selector_WORD):
    """Full original WORD<<2 wrap and signed indexing; accepts edited images."""
    complete_image(image)
    offset = (uint(selector_WORD, 65535, "selector WORD") << 2) & 65535
    if offset >= 32768:
        offset -= 65536
    address = DIR_START + offset
    return dict(address=address, target=int.from_bytes(image[address:address + 4], "big"),
                in_physical_editor_catalog=DIR_START <= address < DIR_END)


def lookup_pair(image, selector_WORD, source_pair_index):
    """Actual source addressing beyond16 is diagnostic, not newly owned data."""
    pointer = resolve_original_directory(image, selector_WORD)["target"]
    if type(source_pair_index) is not int or source_pair_index < 0:
        raise ValueError("nonnegative diagnostic pair index required")
    address = pointer + 4 * source_pair_index
    if not 0 <= address <= len(image) - 4:
        raise ValueError("coordinate source read outside supplied ROM")
    return tuple(int.from_bytes(image[p:p + 2], "big") for p in (address, address + 2))


def project_pair(X_source_WORD, Y_source_WORD, mirrored=False):
    """Narrow source-WORD transform, not the surrounding object/RAM writer."""
    x = uint(X_source_WORD, 65535, "X source WORD")
    y = uint(Y_source_WORD, 65535, "Y source WORD")
    if type(mirrored) is not bool:
        raise ValueError("strict mirrored flag required")
    return ((0x0160 - x) & 65535 if mirrored else x, y)


def bounded_source_pair_reads(count_WORDs):
    """Two bounded loops pre-read the next pair before their zero-count stop."""
    counts = exact_list(count_WORDs, 3, "three caller count WORDs")
    return min(16, 2 + sum(uint(value, 65535, "caller count WORD") for value in counts))


def load_fields(data):
    return shared.load_json(data)


def schema(rom):
    fields = extract(rom)
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def array(rows):
        return dict(type="array", prefixItems=rows, items=False, minItems=len(rows), maxItems=len(rows))
    def fixed(value):
        if type(value) is dict:
            return obj({key: fixed(item) for key, item in value.items()})
        if type(value) is list:
            return array([fixed(item) for item in value])
        return dict(type={str: "string", int: "integer"}[type(value)], const=value)
    directory = fields["directory"]
    dir_properties = {key: fixed(value) for key, value in directory.items() if key != "targets"}
    dir_properties["targets"] = dict(type="array", minItems=5, maxItems=5, items=dict(type="string", enum=directory["targets"]))
    word = dict(type="integer", minimum=0, maximum=65535)
    templates = []
    for row in fields["templates"]:
        properties = {key: fixed(value) for key, value in row.items() if key != "pairs"}
        properties["pairs"] = array([obj({**{key: fixed(value) for key, value in pair.items()
            if key not in ("X_source_WORD", "Y_source_WORD")}, "X_source_WORD": word, "Y_source_WORD": word}) for pair in row["pairs"]])
        templates.append(obj(properties))
    result = obj({**{key: fixed(value) for key, value in metadata().items()},
        "directory": obj(dir_properties), "templates": array(templates)})
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Runtime pins original physical capacities, full WORD costs and evidence. Caller-dependent stops and out-of-catalog source reads are not editor clamps."
    return result


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError("whole-ROM serialized coordinate-source roundtrip differs")
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=6, pointer_bytes=20,
        physical_slots=5, coordinate_bytes=320, source_pairs=80, full_source_WORDs=160,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), scope_container=[DIR_START, END],
        consumer_spans=[dict(start=a, end=b, sha256=digest) for a, b, digest in CONSUMER_SPANS],
        bounded_readers=[dict(pointer_read=0x03F654, pair_read_start=0x03F66A, mirrored_X_base_WORD=0x0160,
            object_start=0xFFFF826A, object_stop=0xFFFF836A, stride=16, maximum_pair_reads=16,
            copy_X=0x03F66E, copy_Y=0x03F674, count_stop_branch=0x03F6AA, object_stop_compare=0x03F6B6),
            dict(pointer_read=0x03F6FA, pair_read_start=0x03F710, object_start=0xFFFF816A,
            object_stop=0xFFFF826A, stride=16, maximum_pair_reads=16,
            copy_X=0x03F710, copy_Y=0x03F714, count_stop_branch=0x03F74A, object_stop_compare=0x03F756)],
        bounded_read_stop="source pair copied before remaining-count zero stop; counts0/0/0 read2 pairs; min(16,2+sum(count WORDs))",
        additional_conditional_reader=dict(pointer_read=0x041964, loop=0x04197A, count_stop=0x0419B6,
            loop_back=0x0419CC, object_stride=16, sixteen_pair_guard_present=False,
            following_source_or_code_alias_possible=True, valid_runtime_count_domain="unknown"),
        source_pair_16_diagnostic=dict(first_template=list(lookup_pair(rom, 0, 16)),
            last_template=list(lookup_pair(rom, 4, 16)), last_read_address=END, owned=False),
        template_source_profiles=[dict(start=start, end=start + 64, pairs=16, sha256=sha(rom[start:start + 64])) for start in TARGETS],
        negative_or_FFFF_WORDs_are_not_source_terminators=True, coordinate_semantics="full source WORDs; mirrored X subtraction wraps16",
        unknown_bytes_adopted=0, natural_selector_domain_complete=False, independent_CPU_comparison=False,
        complete_object_writer_reimplemented=False, edited_gameplay_safety="unknown")
    members = {"fields.json": dump(fields), "fields.schema.json": dump(schema(rom)), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}, independent_CPU_comparison=False))
    return members


def fresh_output(value):
    path = shared.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError("output must stay in build/battle_formation_coordinates or be the fresh formal generated directory")
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
