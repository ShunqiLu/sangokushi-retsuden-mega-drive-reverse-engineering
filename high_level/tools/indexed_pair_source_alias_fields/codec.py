"""321 unique original raw BYTEs read by the 0008E6 indexed WORD-pair prefix.

Complete supplied RAM WORD inputs construct a signed, shifted-WORD source
read. They do not establish the natural RAM selection domain or a pixel owner.
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
OUTPUT_ROOT = ROOT / "build/indexed_pair_source_alias_fields"
FORMAL_ROOT = ROOT / "analysis/indexed_pair_source_alias_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
FORMAT = "g5510-indexed-pair-physical-BYTE-alias-fields-v1"
EDITABLE_BYTES = 321
SOURCE_BASE, UNION_START, UNION_END = 0xD4AC6, 0xCCAC6, 0xDCAC6
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
RANGES = ((0xCE31A, 0xCE43A, reference_value(__name__, 'RANGES')),
    (0xCE45A, 0xCE47A, reference_value(__name__, 'RANGES_2')),
    (0xD4D41, 0xD4D42, reference_value(__name__, 'RANGES_3')))
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
CONSUMERS = ((0x86C, 0x878, reference_value(__name__, 'CONSUMERS')),
    (0x8E6, 0x94C, reference_value(__name__, 'CONSUMERS_2')))
PREFIX_SHA256 = reference_value(__name__, 'PREFIX_SHA256')
INSTRUCTIONS = ((0x86C, "0c780027f38c"), (0x872, "663c"), (0x874, "61000070"),
    (0x8E6, "3038f3ae"), (0x8EA, "e548"), (0x8EC, "41f9000d4ac6"),
    (0x8F2, "31f00000f63e"), (0x8F8, "31f00002f63c"), (0x8FE, "3038f364"),
    (0x902, "e548"), (0x904, "31f00000f642"), (0x90A, "31f00002f640"),
    (0x910, "4eb900006518"), (0x94A, "4e75"))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_FILES = (("m68k_bank0c.s", reference_value(__name__, 'LAYOUT_FILES')),
    ("m68k_bank0d.s", reference_value(__name__, 'LAYOUT_FILES_2')))
MAP_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
MAP_SHA256 = reference_value(__name__, 'MAP_SHA256')
HELPER_SHA256 = reference_value(__name__, 'HELPER_SHA256')
PRODUCERS = {
    "F3AE": dict(RAM_WORD=0xFFF3AE, input_read=0x8E6, shift_WORD=0x8EA,
        source_read_PCs=[0x8F2, 0x8F8], destination_RAM_WORDs=[0xFFF63E, 0xFFF63C]),
    "F364": dict(RAM_WORD=0xFFF364, input_read=0x8FE, shift_WORD=0x902,
        source_read_PCs=[0x904, 0x90A], destination_RAM_WORDs=[0xFFF642, 0xFFF640]),
}
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical complete ROM bytes, size and SHA-256 required")
    for start, end, expected in (*CONSUMERS, *RANGES):
        if sha(rom[start:end]) != expected:
            raise ValueError("pinned original caller/consumer/source differs")


def _image(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic requires complete bytes image; edited images are allowed")


def source_start(input_WORD):
    value = uint(input_WORD, 65535, "complete supplied RAM input WORD")
    shifted = (value << 2) & 65535
    return SOURCE_BASE + (shifted if shifted < 0x8000 else shifted-65536)


def _inside(address):
    return any(start <= address < end for start, end, _ in RANGES)


def lookup(image, input_WORD, producer="F3AE"):
    """One original prefix's two WORD reads, not the complete 8E6 algorithm.

The supplied producer WORD is conditional. No catalog bound, semantic value
mask, canonical-extract gate, or original-value replacement is applied.
"""
    _image(image)
    value = uint(input_WORD, 65535, "complete supplied RAM input WORD")
    if type(producer) is not str or producer not in PRODUCERS:
        raise ValueError("producer must be original F3AE or F364 RAM WORD")
    shifted = (value << 2) & 65535
    start = source_start(value)
    info = PRODUCERS[producer]
    reads = []
    for slot in range(2):
        address = start+2*slot
        data = image[address:address+2]
        reads.append(dict(slot=slot, PC=info["source_read_PCs"][slot], address=address,
            bytes=2, source_BYTEs=list(data), source_WORD=int.from_bytes(data, "big"),
            destination_RAM_WORD=info["destination_RAM_WORDs"][slot],
            editable_BYTE_mask=[_inside(address), _inside(address+1)]))
    return dict(input_WORD=value, producer=producer, producer_RAM_WORD=info["RAM_WORD"],
        shift_WORD_PC=info["shift_WORD"], shifted_offset_WORD=shifted,
        signed_offset=shifted if shifted < 0x8000 else shifted-65536,
        start=start, end=start+4, reads=reads, source_WORDs=[row["source_WORD"] for row in reads],
        source_BYTE_reads=4, source_WORD_reads=2, source_BYTEs=list(image[start:start+4]),
        editable_source_BYTES=sum(_inside(a) for a in range(start, start+4)),
        complete_reads_in_ROM=True, physical_catalog_CPU_clamp=False,
        original_call_gate_is_assumed_not_emulated=True, diagnostic_is_complete_CPU=False)


def witnesses_for_source(ROM_address):
    address = uint(ROM_address, ROM_SIZE-1, "physical source BYTE address")
    if not _inside(address):
        raise ValueError("address outside unique new physical source ranges")
    start = SOURCE_BASE + ((address-SOURCE_BASE)//4)*4
    index = ((start-SOURCE_BASE) & 65535)//4
    return dict(input_WORD=index, input_WORD_aliases=[index+i*0x4000 for i in range(4)],
        producer="F3AE", also_valid_producer="F364", start=start, end=start+4,
        source_BYTE_index=address-start, source_WORD_slot=(address-start)//2,
        BYTE_in_WORD=(address-start) % 2, all_complete_reads_in_ROM=True,
        constructed_input_not_natural_domain=True)


def audit_witness_union(rom):
    verify_rom(rom)
    starts = {source_start(word) for word in range(65536)}
    if starts != set(range(UNION_START, UNION_END, 4)):
        raise ValueError("complete supplied WORD source read union differs")
    source = {a for start, end, _ in RANGES for a in range(start, end)}
    if len(source) != EDITABLE_BYTES or sum(e-s for s, e, _ in RANGES) != EDITABLE_BYTES:
        raise ValueError("physical source union must be disjoint and exact")
    if min(starts) < 0 or max(starts)+4 > len(rom):
        raise ValueError("complete pair read crosses original ROM boundary")
    for address in source:
        witness = witnesses_for_source(address)
        for producer in PRODUCERS:
            view = lookup(rom, witness["input_WORD"], producer)
            if view["source_BYTEs"][witness["source_BYTE_index"]] != rom[address]:
                raise ValueError("source BYTE witness position/read differs")
        if any(source_start(word) != witness["start"] for word in witness["input_WORD_aliases"]):
            raise ValueError("WORD-width high-bit aliases differ")
    return dict(physical_editable_BYTES=EDITABLE_BYTES, supplied_WORD_inputs=65536,
        distinct_complete_pair_windows=16384, WORD_reads_per_window=2, window_BYTES=4,
        read_union_BYTES=65536, all_complete_reads_in_ROM=True, physical_unwitnessed_BYTES=0,
        input_aliases_per_source_window=4, both_original_producers_witnessed=True,
        unique_editing_authority=True, typed_neighbors_emitted_again=False)


def source_fixed(start, end):
    return dict(id=f"rom_{start:06X}_indexed_pair_source_BYTEs", start=start, end=end, bytes=end-start)


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=[dict(**source_fixed(s, e), source_sha256=h) for s, e, h in RANGES],
        source_union_BYTES=EDITABLE_BYTES, source_union_sha256=SOURCE_SHA256,
        serialization="one complete physical source BYTE; complete source WORD pairs are live read-only views",
        evidence=dict(consumers=[dict(start=s, end=e, bytes=e-s, sha256=h) for s, e, h in CONSUMERS],
            prefix=dict(start=0x8E6, end=0x910, bytes=42, sha256=PREFIX_SHA256),
            instructions=[dict(address=a, bytes=b) for a, b in INSTRUCTIONS],
            original_map=dict(path=MAP_PATH, sha256=MAP_SHA256),
            frozen_raw_layout=dict(id=LAYOUT_ID, snapshot_resources=87, snapshot_raw_BYTES=42494,
                files=[dict(path="build/direct_code/layout/"+LAYOUT_ID+"/"+name, sha256=h)
                    for name, h in LAYOUT_FILES], raw_difference_BYTES=EDITABLE_BYTES,
                emitted_already_typed_overlap_BYTES=0),
            shared_pure_helpers=dict(path="tools/battle_deployment_parameters/codec.py", sha256=HELPER_SHA256),
            caller=dict(gate_COMPARE_PC=0x86C, gate_RAM_WORD=0xFFF38C, gate_equal_WORD=0x27,
                bypass_BNE_PC=0x872, bypass_target=0x8B0, true_BSR_PC=0x874, true_target=0x8E6,
                return_RTS_PC=0x94A, complete_consumer_end=0x94C,
                supplied_RAM_WORDs_are_not_claimed_natural=True),
            producers={name: dict(RAM_WORD=info["RAM_WORD"], input_read=info["input_read"],
                shift_WORD=info["shift_WORD"], source_read_PCs=list(info["source_read_PCs"]),
                destination_RAM_WORDs=list(info["destination_RAM_WORDs"])) for name, info in PRODUCERS.items()},
            reader=dict(base_LEA_PC=0x8EC, base=SOURCE_BASE, WORD_shift_count=2,
                formula="D4AC6 + s16((input_WORD << 2) & FFFF)",
                sign_extension_after_WORD_shift=True, two_WORD_displacements=[0, 2],
                big_endian_source_WORD=True, retain_all_source_WORD_bits=True,
                read_union_start=UNION_START, read_union_end=UNION_END, read_union_BYTES=65536,
                distinct_complete_pair_windows=16384, supplied_WORD_domain=[0, 65535],
                all_complete_reads_in_ROM=True, physical_catalog_not_CPU_clamp=True,
                constructed_not_natural_selection=True, no_source_value_terminator=True),
            partial_WORD_alias=dict(start=0xD4D3E, end=0xD4D42, input_WORD=0x009E,
                edited_BYTE=0xD4D41, complete_second_WORD_start=0xD4D40,
                old_typed_BYTEs=[0xD4D3E, 0xD4D3F, 0xD4D40], emitted_again=False,
                neighbor_WORD_high_BYTE_is_live=True),
            per_BYTE_witnesses=[dict(address=a, **witnesses_for_source(a))
                for s, e, _ in RANGES for a in range(s, e)],
            original_zero_BYTEs_are_read_source_not_padding=True,
            original_source_contents=dict(zero_BYTEs=281, nonzero_BYTEs=40,
                nonzero_value_counts=[dict(BYTE=15, count=20), dict(BYTE=240, count=20)]),
            no_bitmap_font_code_or_typed_neighbor_emitted=True),
        natural_RAM_selection="unknown", pair_business_identity="unknown", pixel_owner="unknown",
        complete_0008E6_RAM_algorithm=False, independent_CPU_comparison=False)


def extract(rom):
    verify_rom(rom)
    audit_witness_union(rom)
    return dict(**metadata(), sources=[dict(**source_fixed(s, e), source_BYTEs=list(rom[s:e])) for s, e, _ in RANGES])


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"sources"}, "indexed pair source fields")
    for key, expected in fixed.items():
        same(fields[key], expected, "indexed pair source fields."+key)
    result=[]
    for value, (start, end, _) in zip(exact_list(fields["sources"], 3, "fixed source range count"), RANGES):
        row=source_fixed(start, end)
        keys(value, set(row) | {"source_BYTEs"}, "fixed physical source")
        for key, expected in row.items():
            same(value[key], expected, "fixed physical source."+key)
        data=bytes(uint(v, 255, "complete source BYTE") for v in
            exact_list(value["source_BYTEs"], end-start, "fixed source BYTE count"))
        result.append(dict(id=row["id"], start=start, end=end, data=data,
            role="conditional_signed_WORD_indexed_pair_source_BYTE_alias"))
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES:
        raise ValueError("fixed source union length differs")
    return result


def rebuild(rom, fields):
    image=bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]]=row["data"]
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
    rows=[obj({**{k: fixed(v) for k, v in source_fixed(s, e).items()},
        "source_BYTEs": dict(type="array", minItems=e-s, maxItems=e-s,
            items=dict(type="integer", minimum=0, maximum=255))}) for s, e, _ in RANGES]
    result=obj({**{k: fixed(v) for k, v in metadata().items()},
        "sources": dict(type="array", prefixItems=rows, items=False, minItems=3, maxItems=3)})
    result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="321 unique physical source BYTEs; complete indexed WORD-pair views are diagnostic only."
    return result


def render_bundle(rom):
    fields=extract(rom)
    serialized=dump(fields)
    image=rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("serialized whole-ROM roundtrip differs")
    encoded=blocks(rom, fields)
    witnesses=sorted({witnesses_for_source(a)["input_WORD"] for s, e, _ in RANGES for a in range(s, e)})
    report=dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=3,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), witness_union=audit_witness_union(rom),
        complete_witness_views=[lookup(rom, value) for value in witnesses],
        second_producer_example=lookup(rom, 0x009E, "F364"),
        wrap_and_signed_examples=[lookup(rom, value) for value in (0, 0x1FFF, 0x2000, 0x3FFF, 0x4000, 0x8000, 0xFFFF)],
        blocks=[{k:v for k,v in row.items() if k != "data"} |
            dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members={"fields.json": serialized, "fields.schema.json": dump(schema()), "validation.json": dump(report)}
    members["manifest.json"]=dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=3,
        members={name:dict(bytes=len(data), sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path=safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("output must stay in indexed_pair_source_alias_fields build scope or exact formal bundle")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "import", "verify"))
    parser.add_argument("--rom", default=str(DEFAULT_ROM))
    parser.add_argument("--fields")
    parser.add_argument("--bundle")
    parser.add_argument("--output")
    args=parser.parse_args(argv)
    target=None
    if args.command == "export":
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError("export requires fresh output only")
        target=fresh_output(args.output, bundle=True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None:
            raise ValueError("import requires fields and fresh output")
        target=fresh_output(args.output)
        if target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom=read_bounded(args.rom, ROM_SIZE)
    if args.command == "export":
        members=render_bundle(rom)
        target.mkdir()
        for name,data in members.items():
            put(target/name, data)
        result=dict(path=str(target), editable_bytes=EDITABLE_BYTES, members={name:sha(data) for name,data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name, MAX_JSON) != data:
                raise ValueError("canonical bundle drift: "+name)
        result=dict(path=str(bundle), verified=True, editable_bytes=EDITABLE_BYTES,
            whole_ROM_exact=True, whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON))
        image=rebuild(rom, fields)
        if target is not None:
            put(target, image)
        result=dict(path=None if target is None else str(target), editable_bytes=EDITABLE_BYTES,
            bytes=len(image), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0
