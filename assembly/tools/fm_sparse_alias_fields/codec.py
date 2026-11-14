"""Twenty physical FM source BYTEs with complete conditional 25-BYTE witnesses.

The source fields are sparse, not an aligned instrument allocation. Previously
typed neighbours are read live for diagnostics and are never emitted again.
Negative EF's complete BYTE inputs are retained; natural playback is unknown.
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
OUTPUT_ROOT = ROOT / "build/fm_sparse_alias_fields"
FORMAL_ROOT = ROOT / "analysis/fm_sparse_alias_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-sparse-conditional-FM-source-BYTE-fields-v1"
EDITABLE_BYTES = 20
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
Z80_ROM_BASE = 0x69D2
BANK_Z80_START, BANK_Z80_END, BANK_ROM_START = 0x8000, 0x10000, 0xF8000
MAP_PATH = "analysis/audio/generated/instructions.csv"
MAP_SHA256 = reference_value(__name__, 'MAP_SHA256')
DRIVER_PATH = "src/z80/recovered_driver.s"
DRIVER_SHA256 = reference_value(__name__, 'DRIVER_SHA256')
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = "build/direct_code/layout/" + LAYOUT_ID + "/m68k_bank0f.s"
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
REGISTER_MAP = (0xB0, 0x30, 0x38, 0x34, 0x3C, 0x50, 0x58, 0x54, 0x5C,
                0x60, 0x68, 0x64, 0x6C, 0x70, 0x78, 0x74, 0x7C,
                0x80, 0x88, 0x84, 0x8C, 0x40, 0x48, 0x44, 0x4C)
# Selector, original pointer address, header pointer, header's first LE16 WORD.
PATHS = ((0x67, 0x840B, 0x890C, 0x8008),
         (0x81, 0x823F, 0x827D, 0x8A29),
         (0x29, 0x838F, 0xB3B6, 0xA509),
         (0x07, 0x834B, 0xB1AC, 0xACAC),
         (0x91, 0x825F, 0xBA3B, 0xC6D0),
         (0x97, 0x826B, 0xD0A6, 0xD1F4))
# Physical start/end, complete negative-EF selector/index witness. Each range
# is exactly an accepted81 raw slice; all adjacent source bytes stay elsewhere.
SPECS = ((0xF800C, 0xF800E, 0x67, 0),
         (0xF83B7, 0xF83B8, 0x67, 37), (0xF8492, 0xF8493, 0x67, 46),
         (0xF8768, 0xF8769, 0x67, 75), (0xF8F7E, 0xF8F7F, 0x81, 54),
         (0xF915D, 0xF915E, 0x81, 73), (0xF91B1, 0xF91B2, 0x81, 77),
         (0xF9209, 0xF920A, 0x81, 80), (0xFA920, 0xFA921, 0x29, 41),
         (0xFA9DE, 0xFA9DF, 0x29, 49), (0xFAD06, 0xFAD08, 0x07, 3),
         (0xFAD3A, 0xFAD3B, 0x07, 5), (0xFAF09, 0xFAF0A, 0x07, 24),
         (0xFB27A, 0xFB27B, 0x07, 59), (0xFB57F, 0xFB580, 0x07, 90),
         (0xFD133, 0xFD134, 0x91, 106), (0xFD1F0, 0xFD1F1, 0x91, 113),
         (0xFDB2A, 0xFDB2B, 0x97, 94))
UNWITNESSED_RAW = ((0xEE5EF, 0xEE5F0), (0xEFA30, 0xF8000))
PHYSICAL_CONSUMERS = ((0x698C, "41fa001c"), (0x6990, "43f900a01c00"),
                      (0x6996, "700c"), (0x6998, "12d8"), (0x699A, "51c8fffc"))
CONSUMERS = (
    (0x23, "0600"), (0x25, "c37804"), (0x28, "4f"), (0x29, "0600"),
    (0x2B, "09"), (0x2C, "09"), (0x30, "7e"), (0x31, "23"), (0x32, "66"), (0x33, "6f"),
    (0x66, "cd0c07"), (0x478, "09"), (0x479, "08"), (0x47A, "f7"), (0x47B, "08"),
    (0x493, "af"), (0x494, "b0"), (0x495, "2806"), (0x497, "111900"),
    (0x49A, "19"), (0x49B, "10fd"), (0x4EE, "cd0405"), (0x4F4, "0614"),
    (0x4F6, "cd0405"), (0x4F9, "10fb"), (0x4FB, "dd751c"), (0x4FE, "dd741d"),
    (0x506, "4e"), (0x507, "23"), (0x70C, "3a011c"), (0x70F, "07"),
    (0x710, "320060"), (0x713, "0608"), (0x715, "3a001c"), (0x718, "320060"),
    (0x71B, "0f"), (0x71C, "10fa"),
    (0xB78, "21840b"), (0xB7B, "e5"), (0xB7C, "d6e0"),
    (0xB7E, "218f0b"), (0xB81, "ef"), (0xB82, "1a"), (0xB83, "e9"),
    (0xD2D, "ddcb017e"), (0xD31, "2038"),
    (0xD36, "1a"), (0xD37, "dd7708"), (0xD3B, "13"), (0xD3C, "1a"),
    (0xD3D, "dd770f"), (0xD41, "b7"), (0xD42, "f2600d"), (0xD46, "210080"),
    (0xD49, "0e04"), (0xD4B, "dd7e0f"), (0xD4E, "d681"), (0xD50, "cd2300"),
    (0xD53, "ef"), (0xD54, "f7"), (0xD55, "dd7e08"), (0xD58, "e67f"),
    (0xD5A, "47"), (0xD5B, "cd9304"), (0xD66, "cde504"),
    (0xD8E, "dd6e1c"), (0xD91, "dd661d"), (0xD94, "0604"), (0xD96, "7e"),
    (0xD98, "f29e0d"), (0xD9B, "dd8606"), (0xD9E, "e67f"),
    (0xDA4, "23"), (0xDA5, "10ef"))
sha, dump, keys, same, uint = shared.sha, shared.dump, shared.keys, shared.same, shared.uint
exact_list, load_fields = shared.exact_list, shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def witness_id(selector, index):
    return f"negative_EF_{0x80 | index:02X}_{selector:02X}"


def original_witnesses():
    bases = {selector: base for selector, _, _, base in PATHS}
    return [dict(id=witness_id(selector, index), parameter_BYTE=0x80 | index,
                 external_selector_BYTE=selector, instrument_index=index,
                 Z80_start=bases[selector] + 25 * index,
                 Z80_end=bases[selector] + 25 * (index + 1),
                 start=0xF0000 + bases[selector] + 25 * index,
                 end=0xF0000 + bases[selector] + 25 * (index + 1))
            for _, _, selector, index in SPECS]


def field_descriptors():
    rows = []
    for spec, witness in zip(SPECS, original_witnesses()):
        start, end, _, _ = spec
        for address in range(start, end):
            slot = address - witness["start"]
            rows.append(dict(id=f"rom_{address:06X}_FM_source", ROM_address=address,
                             witness_id=witness["id"], source_slot=slot,
                             role="register_payload" if slot < 21 else "total_level_source",
                             YM_register_base=REGISTER_MAP[slot]))
    return rows


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=[dict(start=a, end=b, bytes=b-a) for a, b, _, _ in SPECS],
        physical_source_sha256=SOURCE_SHA256,
        evidence=dict(original_map=dict(path=MAP_PATH, sha256=MAP_SHA256),
            frozen_driver=dict(path=DRIVER_PATH, sha256=DRIVER_SHA256),
            accepted81_raw_layout=dict(id=LAYOUT_ID, path=LAYOUT_PATH, sha256=LAYOUT_SHA256),
            instructions=[dict(Z80_PC=pc, physical_ROM_PC=Z80_ROM_BASE+pc, bytes=raw)
                          for pc, raw in CONSUMERS],
            original_overlay_copier=[dict(physical_ROM_PC=pc, bytes=raw)
                                     for pc, raw in PHYSICAL_CONSUMERS],
            EF_dispatch=dict(command_BYTE=0xEF, pointer_table_Z80_address=0xB8F,
                stride_BYTES=2, pointer_Z80_address=0xBAD, pointer_LE16=0xD2D,
                target_kind="original JP(HL), no new executable-source admission"),
            bank=dict(value_9bits=0x01F, overlay_ROM_start=0x69AA,
                original_overlay_hex="0f800080b400cb800000000000",
                Z80_window=[BANK_Z80_START, BANK_Z80_END],
                physical_ROM_window=[BANK_ROM_START, ROM_SIZE], serial_write_PCs=[0x710, 0x718],
                serial_bits_first_then_RRCA=[1,1,1,1,1,0,0,0,0]),
            lookup=dict(condition="IX+01 bit7 clear and EF parameter bit7 set",
                selector_BYTE_complete=True, parameter_BYTE_complete=True,
                index_formula="(selector-81) modulo256, zero-extended then times2",
                root_LE16_ROM_address=0xF8004, original_root_LE16=0x823F,
                header_dereference_LE16=True, index_formula_after_mask="parameter & 7F",
                instrument_stride_BYTES=25, ADD_HL_width="WORD modulo65536",
                source_read_register_BYTES=21, source_read_TL_BYTES=4,
                read_stop="after twenty-one register reads and four TL reads",
                physical_editor_is_CPU_clamp=False),
            original_paths=[dict(external_selector_BYTE=s, index_after_SUB81=(s-0x81)&255,
                pointer_Z80_address=p, pointer_LE16=h, header_Z80_address=h,
                header_first_LE16=base, inferred_definition_identity="unknown")
                for s, p, h, base in PATHS],
            original_complete_25_BYTE_witnesses=original_witnesses(),
            raw_difference_BYTES=20, sparse_source_not_aligned_allocation=True,
            F800C_root_slot_not_claimed_consumed=True),
        source_values_original_role="conditional FM read aliases; not newly identified songs/instruments",
        source_view_is_edit_authority=False, typed_neighbours_reemitted=False,
        natural_selection="unknown", playback_safety="unknown",
        independent_CPU_comparison=False, complete_audio_algorithm=False,
        excluded_unknown_raw=[dict(start=a, end=b, bytes=b-a, padding_claim=False)
                              for a, b in UNWITNESSED_RAW])


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical whole ROM bytes, size and SHA-256 required")
    for pc, raw in CONSUMERS:
        if rom[Z80_ROM_BASE+pc:Z80_ROM_BASE+pc+len(raw)//2] != bytes.fromhex(raw):
            raise ValueError("original Z80 consumer bytes changed")
    for pc, raw in PHYSICAL_CONSUMERS:
        if rom[pc:pc+len(raw)//2] != bytes.fromhex(raw):
            raise ValueError("original overlay copier bytes changed")
    if rom[0x69AA:0x69B7] != bytes.fromhex("0f800080b400cb800000000000"):
        raise ValueError("original fixed bank overlay changed")
    if tuple(rom[Z80_ROM_BASE+0x4C8:Z80_ROM_BASE+0x4E1]) != REGISTER_MAP:
        raise ValueError("original YM source-register map changed")
    if rom[Z80_ROM_BASE+0xBAD:Z80_ROM_BASE+0xBAF] != bytes.fromhex("2d0d"):
        raise ValueError("original EF indirect-handler pointer changed")
    if rom[0xF8004:0xF8006] != bytes.fromhex("3f82"):
        raise ValueError("original root04 LE16 changed")
    for _, pointer, header, base in PATHS:
        if int.from_bytes(rom[0xF0000+pointer:0xF0000+pointer+2], "little") != header:
            raise ValueError("original conditional pointer source changed")
        if int.from_bytes(rom[0xF0000+header:0xF0000+header+2], "little") != base:
            raise ValueError("original conditional header source changed")
    if sha(b"".join(rom[a:b] for a, b, _, _ in SPECS)) != SOURCE_SHA256:
        raise ValueError("original sparse source changed")


def _image(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic needs a complete bytes image")


def _bank_word(image, address):
    if not BANK_Z80_START <= address < BANK_Z80_END - 1:
        raise ValueError("read needs non-bank RAM/device state; not a CPU clamp")
    return int.from_bytes(image[0xF0000+address:0xF0000+address+2], "little")


def source_view(image, parameter_BYTE, external_selector_BYTE):
    """Project the original negative-EF source reads, following edited pointers.

    This does not execute channels, chip writes, stack, interrupts or synthesis.
    Positive EF's current RAM/SFX base is outside this particular diagnostic.
    """
    _image(image)
    parameter = uint(parameter_BYTE, 255, "EF parameter BYTE")
    selector = uint(external_selector_BYTE, 255, "external selector BYTE")
    if not parameter & 128:
        raise ValueError("positive EF uses a different live current-base path")
    directory = _bank_word(image, 0x8004)
    pointer_address = (directory + 2 * ((selector-0x81) & 255)) & 65535
    header = _bank_word(image, pointer_address)
    base = _bank_word(image, header)
    index = parameter & 127
    start = (base + 25 * index) & 65535
    logical_addresses = [(start + slot) & 65535 for slot in range(25)]
    if any(not BANK_Z80_START <= a < BANK_Z80_END for a in logical_addresses):
        raise ValueError("complete 21+4 read needs non-bank state; no false fixed-scope clamp")
    owned = {row["ROM_address"] for row in field_descriptors()}
    slots = [dict(source_slot=i, Z80_address=a, ROM_address=0xF0000+a,
                  role="register_payload" if i < 21 else "total_level_source",
                  YM_register_base=REGISTER_MAP[i], BYTE=image[0xF0000+a],
                  this_package_edit_authority=0xF0000+a in owned)
             for i, a in enumerate(logical_addresses)]
    return dict(parameter_BYTE=parameter, external_selector_BYTE=selector,
                root_LE16=directory, pointer_Z80_address=pointer_address,
                header_pointer_LE16=header, instrument_base_LE16=base, instrument_index=index,
                Z80_start=start, Z80_end=start+25, start=0xF0000+start, end=0xF0000+start+25,
                complete_source_reads=25, slots=slots,
                register_payload_BYTEs=[row["BYTE"] for row in slots[:21]],
                total_level_source_BYTEs=[row["BYTE"] for row in slots[21:]],
                editable_source_BYTES=sum(row["this_package_edit_authority"] for row in slots),
                natural_selection="unknown", alias_view_is_edit_authority=False)


def audit_original_witnesses(rom):
    verify_rom(rom)
    witnessed = set()
    views = []
    for row in original_witnesses():
        view = source_view(rom, row["parameter_BYTE"], row["external_selector_BYTE"])
        for key in ("start", "end", "Z80_start", "Z80_end", "instrument_index"):
            same(view[key], row[key], "original full witness " + key)
        witnessed.update(slot["ROM_address"] for slot in view["slots"]
                         if slot["this_package_edit_authority"])
        views.append(view)
    expected = {row["ROM_address"] for row in field_descriptors()}
    if witnessed != expected or len(expected) != EDITABLE_BYTES:
        raise ValueError("complete witness reads do not cover exact sparse authority")
    return dict(complete_25_BYTE_witnesses=len(views), source_read_visits=25*len(views),
                witnessed_physical_BYTES=len(witnessed), missing_physical_BYTES=0,
                unknown_raw_bytes_not_emitted=sum(b-a for a, b in UNWITNESSED_RAW))


def scan_original_alias_raw_union(rom):
    """Repeat the accepted81 raw difference for all negative-EF input BYTEs.

    Invalid bank-only diagnostics are counted, not declared CPU-invalid.
    No arbitrary HL, bank replacement or unbounded sequence path is introduced.
    """
    verify_rom(rom)
    raw = {a for start, end in (*UNWITNESSED_RAW, *((a,b) for a,b,_,_ in SPECS))
           for a in range(start, end)}
    union = set()
    complete = 0
    for selector in range(256):
        pointer = 0x823F + 2 * ((selector-0x81) & 255)
        header = _bank_word(rom, pointer)
        if not BANK_Z80_START <= header < BANK_Z80_END-1:
            continue
        base = _bank_word(rom, header)
        for index in range(128):
            start = (base + 25 * index) & 65535
            if not BANK_Z80_START <= start <= BANK_Z80_END-25:
                continue
            complete += 1
            union.update(a for a in range(0xF0000+start, 0xF0000+start+25) if a in raw)
    return dict(input_BYTE_pairs=256*128, complete_bank_only_plans=complete,
                external_state_boundary_pairs=256*128-complete,
                accepted81_raw_BYTES_in_owned_investigation_scope=len(raw),
                raw_source_read_union_BYTES=len(union), raw_source_read_union=sorted(union),
                natural_domain_proven=False, bank01E_producer_found=False,
                zero_region_ownership_added=0)


def extract(rom):
    verify_rom(rom)
    audit_original_witnesses(rom)
    return dict(**metadata(), source_fields=[dict(**row, BYTE=rom[row["ROM_address"]])
                                             for row in field_descriptors()])


def blocks(rom, fields):
    verify_rom(rom)
    pinned = metadata()
    keys(fields, set(pinned) | {"source_fields"}, "FM sparse package")
    for key, value in pinned.items():
        same(fields[key], value, "package." + key)
    values = {}
    for row, expected in zip(exact_list(fields["source_fields"], EDITABLE_BYTES, "source fields"),
                             field_descriptors()):
        keys(row, set(expected) | {"BYTE"}, "FM source field")
        for key, value in expected.items():
            same(row[key], value, "source field." + key)
        values[expected["ROM_address"]] = uint(row["BYTE"], 255, "complete source BYTE")
    return [dict(id=f"rom_{a:06X}_sparse_FM_source", start=a, end=b,
                 data=bytes(values[address] for address in range(a, b)),
                 role="confirmed_conditional_FM_source_register_BYTES")
            for a, b, _, _ in SPECS]


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


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
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)], const=value)
    properties = {key: fixed(value) for key, value in metadata().items()}
    properties["source_fields"] = exact([obj({**{key:fixed(value) for key,value in row.items()},
        "BYTE":dict(type="integer", minimum=0, maximum=255)}) for row in field_descriptors()])
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "20 full source BYTEs; complete 25-BYTE alias views do not own adjacent data."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("whole-ROM serialized roundtrip differs")
    scan = scan_original_alias_raw_union(rom)
    expected = [row["ROM_address"] for row in field_descriptors()]
    same(scan["raw_source_read_union"], expected, "exact accepted81 raw source difference")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=len(encoded),
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), focused_read_audit=audit_original_witnesses(rom),
        original_alias_raw_scan=scan,
        blocks=[{key:value for key,value in row.items() if key != "data"}
                | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json":serialized, "fields.schema.json":dump(schema()), "validation.json":dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        physical_blocks=len(encoded), complete_source_witnesses=18,
        members={name:dict(bytes=len(data), sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in own build scope or exact formal bundle")
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
            raise ValueError("export requires only a fresh output")
        target = fresh_output(args.output, bundle=True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None:
            raise ValueError("import requires fields and a fresh .bin output")
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
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES,
                      members={name:sha(data) for name,data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name, data in render_bundle(rom).items():
            if read_bounded(bundle/name, MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=EDITABLE_BYTES,
                      whole_ROM_exact=True, whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=EDITABLE_BYTES,
                      bytes=len(image), sha256=sha(image), exact_canonical=image == rom)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
