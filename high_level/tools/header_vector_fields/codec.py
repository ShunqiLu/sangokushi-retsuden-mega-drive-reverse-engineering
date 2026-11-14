"""Literal 64 BE32 vectors plus fixed 256-byte cartridge-header fields.

All source bits, space-filled reserved literals and checksum are preserved.
Text BYTE arrays are authoritative; reversible charset previews are not. Full
vector LONGs are editable without inventing interrupt domains or target clamps.
This linear-ROM header is not the separate 512-byte SMD copier header.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared
from tools.code_analysis.m68k_code_map import VECTOR_NAMES

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
OUTPUT_ROOT = ROOT / "build/header_vector_fields"
FORMAL_ROOT = ROOT / "analysis/header_vector_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 512
FORMAT = "g5510-literal-header-and-vector-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
VECTOR_ID, HEADER_ID = "rom_000000_CPU_vector_BE32s", "rom_000100_cartridge_header_literals"
# Where no local parser establishes a business meaning, retain a neutral
# address-based field name. Every fixed-width literal remains a typed field.
LITERALS = (
    ("identity_literal_100", 0x100, 16, "confirmed SEGA signature literal", "ascii"),
    ("literal_110", 0x110, 16, "literal with visible copyright/year text; further semantics unknown", "ascii"),
    ("literal_120", 0x120, 48, "space-filled header literal; business role unknown", "ascii"),
    ("literal_150", 0x150, 48, "non-ASCII header text; charset interpretation candidate", "shift_jis_candidate"),
    ("literal_180", 0x180, 14, "literal containing GM G-5510 -00; business role not enforced", "ascii"),
    ("literal_190", 0x190, 16, "literal J and spaces; flag interpretation unknown", "ascii"),
    ("literal_1B0", 0x1B0, 2, "literal RA marker; further interpretation not enforced", "ascii"),
    ("reserved_literal_1BC", 0x1BC, 12, "reserved header literal, not free-space claim", "ascii"),
    ("reserved_literal_1C8", 0x1C8, 40, "reserved header literal, not free-space claim", "ascii"),
    ("literal_1F0", 0x1F0, 16, "literal C and spaces; regional mapping unknown", "ascii"),
)
NUMBERS = (
    ("checksum_WORD_18E", 0x18E, 2, "confirmed stored BE16 Mega Drive checksum"),
    ("literal_LONG_1A0", 0x1A0, 4, "neutral literal BE32; address semantics not enforced"),
    ("literal_LONG_1A4", 0x1A4, 4, "neutral literal BE32; address semantics not enforced"),
    ("literal_LONG_1A8", 0x1A8, 4, "neutral literal BE32; address semantics not enforced"),
    ("literal_LONG_1AC", 0x1AC, 4, "neutral literal BE32; address semantics not enforced"),
    ("literal_WORD_1B2", 0x1B2, 2, "neutral literal BE16; flags unknown"),
    ("literal_LONG_1B4", 0x1B4, 4, "neutral literal BE32; address semantics not enforced"),
    ("literal_LONG_1B8", 0x1B8, 4, "neutral literal BE32; address semantics not enforced"),
)
EVIDENCE = (
    ("toolchain/rom_rebuild.py", reference_value(__name__, 'EVIDENCE'), "canonical image identity and separate SMD copier-header distinction"),
    ("tools/code_analysis/m68k_code_map.py", reference_value(__name__, 'EVIDENCE_2'), "64 BE32 vector parsing/names; ROM 000..200 reserved metadata"),
    ("analysis/code/generated/vectors.csv", reference_value(__name__, 'EVIDENCE_3'), "existing original-vector values and names"),
    ("../tools/rom_tool.py", reference_value(__name__, 'EVIDENCE_4'), "SEGA16 signature; 18E stored checksum; 200+ BE16 checksum sum"),
    ("config/rom_identity.json", reference_value(__name__, 'EVIDENCE_5'), "original identity/checksum observation"),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    if len(VECTOR_NAMES) != 64 or rom[0x100:0x110] != b"SEGA MEGA DRIVE ":
        raise ValueError("pinned vector-name count or original signature differs")


def metadata():
    return dict(
        format=FORMAT, confidence="confirmed", canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        coordinate_system="linear BIN ROM offsets; not SMD file offsets or copier header",
        physical_scope=[dict(id=VECTOR_ID, start=0, end=0x100, bytes=256, slots=64, width_BYTES=4, endianness="big"),
                        dict(id=HEADER_ID, start=0x100, end=0x200, bytes=256,
                             fixed_literal_fields=10, BE16_fields=2, BE32_fields=6)],
        evidence=[dict(path=path, sha256=digest, role=role, runtime_file_read=False) for path, digest, role in EVIDENCE],
        checksum_contract=dict(stored_address=0x18E, width_BYTES=2, endianness="big",
                               body_start=0x200, formula="sum of complete image body BE16 WORDs modulo 65536",
                               automatic_repair=False, checksum_is_an_editable_literal=True),
        text_contract=dict(authority="fixed BYTE arrays, complete 0..255 values",
                           auto_trim=False, auto_pad=False, automatic_charset_transcode=False,
                           charset_preview_is_authority=False, candidate_charset="Shift-JIS only when reversible",
                           spaces_and_reserved_literals_preserved=True, reserved_means_free_space=False),
        vector_contract=dict(full_LONG_min=0, full_LONG_max=0xFFFFFFFF, automatic_target_normalisation=False,
                             CPU_target_clamp=False, natural_interrupt_target_domains_added=0,
                             target_classification_is_diagnostic_not_execution_proof=True),
        unknown_header_field_semantics="neutral literal/address/flag fields are not interpreted beyond documented local parser evidence",
        edited_boot_gameplay_safety="unknown", independent_CPU_comparison=False,
    )


def vector_fixed(index):
    return dict(id=f"CPU_vector_{index:02d}", index=index, address=4*index,
                architectural_name=VECTOR_NAMES[index])


def literal_fixed(spec):
    name, address, size, role, charset = spec
    return dict(id=name, address=address, fixed_BYTES=size, role=role, original_charset_observation=charset)


def number_fixed(spec):
    name, address, size, role = spec
    return dict(id=name, address=address, width_BYTES=size, endianness="big", role=role)


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result["vectors"] = [dict(**vector_fixed(index), LONG=int.from_bytes(rom[4*index:4*index+4], "big")) for index in range(64)]
    result["header_literals"] = [dict(**literal_fixed(spec), BYTEs=list(rom[spec[1]:spec[1]+spec[2]])) for spec in LITERALS]
    result["header_numbers"] = [dict(**number_fixed(spec), value=int.from_bytes(rom[spec[1]:spec[1]+spec[2]], "big")) for spec in NUMBERS]
    return result


def pinned(row, fixed, mutable, label):
    keys(row, set(fixed) | set(mutable), label)
    for key, value in fixed.items():
        same(row[key], value, label + "." + key)


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {"vectors", "header_literals", "header_numbers"}, "header/vector package")
    vectors = bytearray()
    for index, item in enumerate(exact_list(fields["vectors"], 64, "fixed CPU vector slots")):
        pinned(item, vector_fixed(index), {"LONG"}, "vector")
        vectors.extend(uint(item["LONG"], 0xFFFFFFFF, "full vector LONG").to_bytes(4, "big"))
    header, covered = bytearray(256), set()
    def place(address, data):
        scope = set(range(address, address+len(data)))
        if not scope <= set(range(0x100, 0x200)) or scope.intersection(covered):
            raise ValueError("header literal field overlap or outside extent")
        covered.update(scope)
        header[address-0x100:address-0x100+len(data)] = data
    for spec, item in zip(LITERALS, exact_list(fields["header_literals"], len(LITERALS), "fixed literal fields")):
        pinned(item, literal_fixed(spec), {"BYTEs"}, "literal")
        data = bytes(uint(value, 255, "full literal BYTE") for value in exact_list(item["BYTEs"], spec[2], "fixed literal BYTE cost"))
        place(spec[1], data)
    for spec, item in zip(NUMBERS, exact_list(fields["header_numbers"], len(NUMBERS), "fixed number fields")):
        pinned(item, number_fixed(spec), {"value"}, "number")
        place(spec[1], uint(item["value"], (1 << (8*spec[2])) - 1, "complete unsigned header number").to_bytes(spec[2], "big"))
    if len(vectors) != 256 or covered != set(range(0x100, 0x200)):
        raise ValueError("exact 256+256-byte structured coverage required")
    return [dict(id=VECTOR_ID, start=0, end=0x100, data=bytes(vectors), role="confirmed_CPU_vector_full_BE32_fields"),
            dict(id=HEADER_ID, start=0x100, end=0x200, data=bytes(header), role="confirmed_fixed_cartridge_header_literal_fields")]


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def require_image(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic requires a complete bytes image")


def vector_views(image):
    """Same value classes as the old parser, not a CPU interrupt-domain expansion."""
    require_image(image)
    result = []
    for index in range(64):
        value = int.from_bytes(image[4*index:4*index+4], "big")
        if index == 0: status = "stack_pointer"
        elif value == 0: status = "null"
        elif value & 1: status = "invalid_odd"
        elif 0x200 <= value < ROM_SIZE: status = "rom_target"
        elif value < ROM_SIZE: status = "reserved_metadata_target"
        else: status = "external_target"
        result.append(dict(**vector_fixed(index), LONG=value, diagnostic_status=status))
    return result


def checksum_view(image):
    """Report the stored literal and computed checksum without fixing either."""
    require_image(image)
    stored = int.from_bytes(image[0x18E:0x190], "big")
    computed = sum((image[a] << 8) | image[a+1] for a in range(0x200, len(image), 2)) & 0xFFFF
    return dict(stored_WORD=stored, computed_WORD=computed, matches=stored == computed, automatic_repair=False)


def literal_preview(data):
    """Reversible observed text view only; unknown bytes remain explicit BYTE escapes."""
    if type(data) is not bytes:
        raise ValueError("literal preview requires bytes")
    if all(0x20 <= value <= 0x7E for value in data):
        return dict(charset="ascii", confidence="confirmed", text=data.decode("ascii"), editing_authority=False)
    if any(value < 0x20 or value == 0x7F for value in data):
        return dict(charset="unknown", confidence="unknown", text="".join(f"[BYTE:{value:02X}]" for value in data), editing_authority=False)
    try:
        text = data.decode("shift_jis")
        if text.encode("shift_jis") == data:
            return dict(charset="shift_jis", confidence="candidate", text=text, editing_authority=False)
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass
    return dict(charset="unknown", confidence="unknown", text="".join(f"[BYTE:{value:02X}]" for value in data), editing_authority=False)


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
    properties["vectors"] = exact([obj({**{key: fixed(value) for key, value in vector_fixed(index).items()},
        "LONG": dict(type="integer", minimum=0, maximum=0xFFFFFFFF)}) for index in range(64)])
    properties["header_literals"] = exact([obj({**{key: fixed(value) for key, value in literal_fixed(spec).items()},
        "BYTEs": dict(type="array", items=dict(type="integer", minimum=0, maximum=255), minItems=spec[2], maxItems=spec[2])}) for spec in LITERALS])
    properties["header_numbers"] = exact([obj({**{key: fixed(value) for key, value in number_fixed(spec).items()},
        "value": dict(type="integer", minimum=0, maximum=(1 << (8*spec[2]))-1)}) for spec in NUMBERS])
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "64 complete BE32 vectors and fixed 256-byte header literals/numbers; no target clamp, charset conversion or checksum repair."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("whole-ROM serialized field roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=512, physical_blocks=2,
                  whole_ROM_exact=True, whole_ROM_sha256=sha(image), checksum=checksum_view(image),
                  original_vector_views=vector_views(image),
                  literal_previews=[dict(id=spec[0], address=spec[1], **literal_preview(rom[spec[1]:spec[1]+spec[2]])) for spec in LITERALS],
                  blocks=[{key: value for key, value in row.items() if key != "data"}
                          | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=512, physical_blocks=2,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in header_vector_fields build scope or exact formal bundle")
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
        result = dict(path=str(target), editable_bytes=512, members={name: sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name, data in render_bundle(rom).items():
            if read_bounded(bundle / name, MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=512,
                      whole_ROM_exact=True, whole_ROM_sha256=ROM_SHA256)
    else:
        image = rebuild(rom, load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON)))
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=512,
                      exact_canonical=image == rom, bytes=len(image), sha256=sha(image), checksum=checksum_view(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
