"""4245 original source BYTEs reached by three conditional external FM aliases.

Each physical BYTE is serialized once. Fixed complete 25-BYTE witnesses are
read-only views, not an invented aligned record allocation or a natural song
domain. The diagnostic follows live pointers in an edited complete image.
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
OUTPUT_ROOT = ROOT / "build/fm_external_alias_fields"
FORMAL_ROOT = ROOT / "analysis/fm_external_alias_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-external-FM-alias-physical-source-BYTE-fields-v1"
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
START, END, EDITABLE_BYTES = 0xFEF6B, 0x100000, 4245
ALIAS_COUNT, RECORD_BYTES = 257, 25
Z80_ROM_BASE = 0x69D2
BANK_ROM_START, BANK_Z80_START, BANK_Z80_END = 0xF8000, 0x8000, 0x10000
REGISTER_MAP = (0xB0, 0x30, 0x38, 0x34, 0x3C, 0x50, 0x58, 0x54, 0x5C,
                0x60, 0x68, 0x64, 0x6C, 0x70, 0x78, 0x74, 0x7C,
                0x80, 0x88, 0x84, 0x8C, 0x40, 0x48, 0x44, 0x4C)
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
MAP_PATH = "analysis/audio/generated/instructions.csv"
MAP_SHA256 = reference_value(__name__, 'MAP_SHA256')
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = "build/direct_code/layout/" + LAYOUT_ID + "/m68k_bank0f.s"
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
# Selector, original index after SUB81, pointer-table WORD location, header
# pointer, first header WORD (instrument base), and complete witness indices.
PATHS = (
    (0x06, 0x85, 0x8349, 0xAAA5, 0xE624, 95, 127),
    (0xA3, 0x22, 0x8283, 0x82AB, 0xEFF2, 0, 127),
    (0x7E, 0xFD, 0x8439, 0x9795, 0xF6A0, 0, 95),
)
CONSUMERS = (
    (0x69AA, 0x69B7, reference_value(__name__, 'CONSUMERS')),
    (0x69F2, 0x6A07, reference_value(__name__, 'CONSUMERS_2')),
    (0x6E56, 0x6E70, reference_value(__name__, 'CONSUMERS_3')),
    (0x6E9A, 0x6EB3, reference_value(__name__, 'CONSUMERS_4')),
    (0x6EB7, 0x6EDC, reference_value(__name__, 'CONSUMERS_5')),
    (0x70DE, 0x70F1, reference_value(__name__, 'CONSUMERS_6')),
    (0x76FF, 0x7742, reference_value(__name__, 'CONSUMERS_7')),
    (0x775C, 0x777B, reference_value(__name__, 'CONSUMERS_8')),
    (0xF8004, 0xF8006, reference_value(__name__, 'CONSUMERS_9')),
    (0xF8349, 0xF834B, reference_value(__name__, 'CONSUMERS_10')),
    (0xFAAA5, 0xFAAA7, reference_value(__name__, 'CONSUMERS_11')),
    (0xF8283, 0xF8285, reference_value(__name__, 'CONSUMERS_12')),
    (0xF82AB, 0xF82AD, reference_value(__name__, 'CONSUMERS_13')),
    (0xF8439, 0xF843B, reference_value(__name__, 'CONSUMERS_14')),
    (0xF9795, 0xF9797, reference_value(__name__, 'CONSUMERS_15')),
)
INSTRUCTIONS = (
    (0x23, "0600"), (0x25, "c37804"), (0x28, "4f"), (0x29, "0600"),
    (0x2B, "09"), (0x2C, "09"), (0x30, "7e"), (0x31, "23"), (0x32, "66"), (0x33, "6f"),
    (0x478, "09"), (0x479, "08"), (0x47A, "f7"), (0x47B, "08"), (0x47C, "c9"),
    (0x493, "af"), (0x494, "b0"), (0x495, "2806"), (0x497, "111900"), (0x49A, "19"), (0x49B, "10fd"),
    (0x4EE, "cd0405"), (0x4F4, "0614"), (0x4F6, "cd0405"), (0x4F9, "10fb"),
    (0x4FB, "dd751c"), (0x4FE, "dd741d"), (0x506, "4e"), (0x507, "23"),
    (0x70C, "3a011c"), (0x70F, "07"), (0x710, "320060"), (0x713, "0608"),
    (0x715, "3a001c"), (0x718, "320060"), (0x71B, "0f"), (0x71C, "10fa"),
    (0xD2D, "ddcb017e"), (0xD31, "2038"), (0xD36, "1a"), (0xD37, "dd7708"),
    (0xD3B, "13"), (0xD3C, "1a"), (0xD3D, "dd770f"), (0xD41, "b7"), (0xD42, "f2600d"),
    (0xD46, "210080"), (0xD49, "0e04"), (0xD4B, "dd7e0f"), (0xD4E, "d681"),
    (0xD50, "cd2300"), (0xD53, "ef"), (0xD54, "f7"), (0xD55, "dd7e08"),
    (0xD58, "e67f"), (0xD5A, "47"), (0xD5B, "cd9304"), (0xD66, "cde504"),
    (0xD8E, "dd6e1c"), (0xD91, "dd661d"), (0xD94, "0604"), (0xD96, "7e"),
    (0xD98, "f29e0d"), (0xD9B, "dd8606"), (0xD9E, "e67f"), (0xDA4, "23"), (0xDA5, "10ef"),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical complete ROM bytes, size and SHA-256 required")
    for start, end, expected in CONSUMERS:
        if sha(rom[start:end]) != expected:
            raise ValueError("pinned original FM bank/pointer/header/consumer differs")
    if sha(rom[START:END]) != SOURCE_SHA256:
        raise ValueError("pinned physical source differs")


def alias_witnesses():
    return [dict(id=f"EF_{0x80 | index:02X}_{selector:02X}",
                 parameter_BYTE=0x80 | index, external_selector_BYTE=selector, instrument_index=index,
                 Z80_start=base + 25 * index, Z80_end=base + 25 * (index + 1),
                 start=0xF0000 + base + 25 * index, end=0xF0000 + base + 25 * (index + 1))
            for selector, _, _, _, base, first, last in PATHS for index in range(first, last + 1)]


def source_slots():
    return [dict(source_slot=i, role="register_payload" if i < 21 else "TL_source",
                 register_base=register, read_order=i, source_BYTES=1)
            for i, register in enumerate(REGISTER_MAP)]


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=dict(start=START, end=END, bytes=EDITABLE_BYTES,
            serialization="one full BYTE per physical source address", aligned_record_allocation=False,
            source_sha256=SOURCE_SHA256),
        prior_authorities_not_emitted=[dict(start=0xFE2EB, end=0xFE31D, bytes=50, authority="original_two_FM_records"),
            dict(start=0xFE31D, end=START, bytes=3150, authority="frozen_fm_instrument_alias_fields")],
        evidence=dict(original_map=dict(path=MAP_PATH, sha256=MAP_SHA256, confidence="confirmed_static_CFG_not_executed_PC"),
            frozen_raw_layout=dict(id=LAYOUT_ID, path=LAYOUT_PATH, sha256=LAYOUT_SHA256, line=88952,
                bank=15, offset=0xE31D, length=0x1CE3, previous_package_BYTES=3150, this_package_BYTES=4245,
                previous_typed_overlap_BYTES=0),
            consumers=[dict(start=s, end=e, bytes=e-s, sha256=h) for s, e, h in CONSUMERS],
            instructions=[dict(Z80_address=a, ROM_address=Z80_ROM_BASE+a, bytes=b, confidence="confirmed") for a, b in INSTRUCTIONS],
            bank=dict(value_9bits=0x01F, ROM_start=BANK_ROM_START, ROM_end=ROM_SIZE,
                Z80_start=BANK_Z80_START, Z80_end=BANK_Z80_END, overlay_ROM_start=0x69AA,
                overlay_hex="0f800080b400cb800000000000", serial_writes_Z80=[0x710, 0x718], all_banks_exhausted=False),
            lookup=dict(FM_condition="IX+01 bit7 clear", negative_condition="EF parameter BYTE bit7 set",
                selector_read_Z80=0xD3C, SUB81_Z80=0xD4E, SUB81_width="BYTE wrap modulo256",
                root_LE_WORD_ROM_address=0xF8004, root_LE_WORD=0x823F,
                index_A_zero_extended=True, table_stride_BYTES=2, RST28_Z80=0xD53,
                header_pointer_LE_WORD=True, second_header_dereference_Z80=0xD54,
                parameter_AND7F_Z80=0xD58, actual_instrument_index_domain=[0, 127],
                index_stride_BYTES=25, index_loop_Z80=[0x497, 0x49A, 0x49B],
                ADD_HL_width="WORD wrap modulo65536", zero_index_skips_DJNZ=True,
                external_selector_music_catalog_CPU_clamp=False, new_source_physical_CPU_clamp=False,
                sequence_operand_BYTES=2, including_command_BYTE=3,
                diagnostic_boundary="current-base positive EF, non-bank pointers or wrap into RAM require external state"),
            external_paths=[dict(external_selector_BYTE=s, index_after_SUB81=i, pointer_Z80_address=t,
                pointer_ROM_address=0xF0000+t, header_pointer_LE_WORD=h, header_ROM_address=0xF0000+h,
                header_first_LE_WORD_instrument_base=b, first_witness_index=first, last_witness_index=last,
                witnesses=last-first+1, start=0xF0000+b+25*first, end=0xF0000+b+25*(last+1),
                actual_definition_or_song_identity="unknown_source_alias_not_declared_music")
                for s, i, t, h, b, first, last in PATHS],
            original_source_is_zero=True, zero_content_is_padding=False,
            full_record_contract=dict(register_payload_BYTES=21, TL_source_BYTES=4, total_BYTES=25,
                first_register_read_Z80=0x506, first_calls=1, additional_DJNZ_calls=20,
                saved_TL_pointer_Z80=[0x4FB, 0x4FE], TL_read_Z80=0xD96, TL_DJNZ_Z80=0xDA5,
                source_slots=source_slots(), TL_source_is_full_BYTE=True,
                TL_hardware_rule="bit7 set: ADD8 attenuation then AND7F; original BYTE remains unnormalized")),
        alias_witnesses=alias_witnesses(), alias_view_is_editing_authority=False,
        conditional_source_union_not_natural=True, original_song_selection="unknown",
        playback_safety="unknown", target_hardware_effects="unknown",
        independent_CPU_comparison=False, complete_audio_algorithm=False)


def _image(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic requires a complete bytes image")


def _bank_word(image, address, label):
    if not BANK_Z80_START <= address < BANK_Z80_END - 1:
        raise ValueError(label + ": original read leaves fixed ROM bank; RAM/device state unknown")
    offset = 0xF0000 + address
    return int.from_bytes(image[offset:offset+2], "little")


def lookup(image, parameter_BYTE, external_selector_BYTE):
    """Original negative-EF pointer/read diagnostic, not natural playback.

    Full input BYTEs are retained. Positive EF depends on current RAM base and
    is explicitly outside this external path, not silently forced negative.
    Image contents, including pointer/header aliases, are read live.
    """
    _image(image)
    parameter = uint(parameter_BYTE, 255, "complete EF parameter BYTE")
    selector = uint(external_selector_BYTE, 255, "complete external selector BYTE")
    if parameter < 128:
        raise ValueError("positive EF uses current RAM/SFX instrument base, outside external diagnostic")
    directory = _bank_word(image, 0x8004, "root04 LE WORD")
    pointer_index = (selector - 0x81) & 255
    pointer_address = (directory + 2 * pointer_index) & 65535
    header = _bank_word(image, pointer_address, "external pointer LE WORD")
    base = _bank_word(image, header, "header instrument-base LE WORD")
    index = parameter & 127
    z80_start = (base + 25 * index) & 65535
    addresses = [(z80_start + slot) & 65535 for slot in range(25)]
    if any(not BANK_Z80_START <= address < BANK_Z80_END for address in addresses):
        raise ValueError("complete original 21+4 source read crosses fixed ROM bank; RAM/device state unknown")
    start, end = 0xF0000 + z80_start, 0xF0000 + z80_start + 25
    return dict(parameter_BYTE=parameter, external_selector_BYTE=selector, instrument_index=index,
        root04_LE_WORD=directory, index_after_SUB81=pointer_index, pointer_Z80_address=pointer_address,
        header_pointer_LE_WORD=header, instrument_base_LE_WORD=base, Z80_start=z80_start, Z80_end=z80_start+25,
        start=start, end=end, register_payload_BYTEs=list(image[start:start+21]),
        total_level_source_BYTEs=list(image[start+21:end]), inside_edit_scope=START <= start and end <= END,
        editable_source_BYTES=sum(START <= address < END for address in range(start, end)),
        full_original_record_in_bank=True, natural_selection="unknown")


def witnesses_for_source(ROM_address):
    """Each alias of one physical BYTE: parameter, selector, index and slot."""
    address = uint(ROM_address, ROM_SIZE-1, "physical ROM address")
    if not START <= address < END:
        raise ValueError("address outside this unique editable physical source")
    result = []
    for row in alias_witnesses():
        if row["start"] <= address < row["end"]:
            slot = address-row["start"]
            result.append(dict(alias_id=row["id"], parameter_BYTE=row["parameter_BYTE"],
                external_selector_BYTE=row["external_selector_BYTE"], instrument_index=row["instrument_index"],
                source_slot=slot, role="register_payload" if slot < 21 else "TL_source",
                register_base=REGISTER_MAP[slot], ROM_address=address))
    return result


def audit_witness_union(rom):
    verify_rom(rom)
    counts = [0] * EDITABLE_BYTES
    rows = alias_witnesses()
    for row in rows:
        view = lookup(rom, row["parameter_BYTE"], row["external_selector_BYTE"])
        for key in ("instrument_index", "start", "end", "Z80_start", "Z80_end"):
            same(view[key], row[key], "original closed alias " + key)
        if row["end"]-row["start"] != 25 or not view["inside_edit_scope"]:
            raise ValueError("witness is not a complete 25-BYTE in-scope source read")
        for address in range(row["start"], row["end"]):
            counts[address-START] += 1
    if len(rows) != ALIAS_COUNT or not all(counts):
        raise ValueError("fixed complete witnesses fail the exact physical BYTE union")
    return dict(closed_25_BYTE_witnesses=len(rows), physical_BYTES_witnessed=len(counts),
        physical_missing_BYTES=0, source_read_visits=sum(counts), minimum_BYTE_witnesses=min(counts),
        maximum_BYTE_witnesses=max(counts), source_scope_exact=True, aliases_emitted_again=False,
        all_257_witnesses_in_original_bank=True)


def extract(rom):
    verify_rom(rom)
    audit_witness_union(rom)
    return dict(**metadata(), source_BYTEs=list(rom[START:END]))


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"source_BYTEs"}, "physical FM source fields")
    for key, value in fixed.items():
        same(fields[key], value, "physical FM source fields." + key)
    data = bytes(uint(value, 255, "complete physical source BYTE")
                 for value in exact_list(fields["source_BYTEs"], EDITABLE_BYTES, "fixed physical source BYTE count"))
    if END-START != len(data):
        raise ValueError("fixed physical source union width differs")
    return [dict(id="rom_FEF6B_external_FM_physical_source_BYTEs", start=START, end=END, data=data,
                 role="conditionally_read_FM_source_BYTE_union")]


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def schema():
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({k: fixed(v) for k, v in value.items()})
        if type(value) is list:
            return dict(type="array", prefixItems=[fixed(v) for v in value], items=False,
                        minItems=len(value), maxItems=len(value))
        return dict(type={str: "string", int: "integer", bool: "boolean"}[type(value)], const=value)
    result = obj({**{k: fixed(v) for k, v in metadata().items()},
        "source_BYTEs": dict(type="array", minItems=EDITABLE_BYTES, maxItems=EDITABLE_BYTES,
                            items=dict(type="integer", minimum=0, maximum=255))})
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "One complete editable BYTE per physical address; fixed 257 alias witnesses are read-only metadata."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("serialized whole-ROM roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), witness_union=audit_witness_union(rom),
        alias_view_examples=[lookup(rom, 0x80|index, selector) for selector, index in ((6, 95), (6, 127), (0xA3, 0), (0xA3, 127), (0x7E, 0), (0x7E, 95))],
        physical_edge_witnesses={str(address): witnesses_for_source(address) for address in (START, END-1)},
        blocks=[{k: v for k, v in row.items() if k != "data"} | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=1,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    if any(len(data) > MAX_JSON for data in members.values()):
        raise ValueError("bundle exceeds the bounded JSON member size")
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in fm_external_alias_fields build scope or exact formal bundle")
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
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom = read_bounded(args.rom, ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            put(target/name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES, members={name: sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name, data in render_bundle(rom).items():
            if read_bounded(bundle/name, MAX_JSON) != data:
                raise ValueError("canonical bundle drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=EDITABLE_BYTES, whole_ROM_exact=True, whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=EDITABLE_BYTES,
                      bytes=len(image), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
