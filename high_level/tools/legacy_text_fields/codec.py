"""Editable WORD fields for 94 original legacy text records and 52 BE32 slots.

FF streams terminate in FFFF; 80 streams terminate in 8000. Neither uses the
main dialogue grammar. Physical slots, control positions, original terminators
and direct MOVE.L xrefs are fixed. A directory slot may alias any of the 52
original FF table records. Full glyph WORDs retain their attribute/alias bits.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from tools.text_font import text_font_assets as legacy
from tools.vdp_word_streams import format as shared

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = legacy.default_rom_path()
DEFAULT_FIELDS = ROOT / "analysis/legacy_text_fields/generated/fields.json"
DEFAULT_CATALOG = ROOT / "analysis/text_encoding/generated/catalog.json"
OUTPUT_ROOT = ROOT / "build/legacy_text_fields"
FORMAL_ROOT = DEFAULT_FIELDS.parent
FORMAT = "g5510-legacy-ff80-fixed-WORD-fields-v1"
EDITABLE_BYTES = 2856
CONTROLS = {
    "ff_control_stream": frozenset((0xFF00, 0xFF01, 0xFF02, 0xFF03, 0xFF0A, 0xFF20)),
    "80_control_stream": frozenset((0x8002, 0x8008, 0x800A, 0x800E, 0x8010, 0x8011, 0x8012)),
}
TERMINATORS = {"ff_control_stream": 0xFFFF, "80_control_stream": 0x8000}
sha = shared.sha
dump = shared.dump
load_fields = shared.load_json


def metadata():
    return dict(format=FORMAT,
                canonical_source=dict(size=legacy.EXPECTED_ROM_SIZE,
                                      sha256=legacy.EXPECTED_ROM_SHA256),
                confidence="confirmed", owner_bytes_added=0,
                natural_domains_added=0, complete_domains_added=0)


def verify_rom(rom):
    if type(rom) is not bytes:
        raise ValueError("canonical ROM must be bytes")
    legacy.validate_rom(rom)


def ident(start):
    return f"rom_{start:06X}_legacy_text"


def exact_list(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ": fixed physical count differs")
    return value


def original_records(rom):
    """Reuse only the old physical discovery, never its editable end inference."""
    pointers = legacy.parse_pointer_table(rom)
    table = legacy.table_records(rom, pointers)
    direct = legacy.discover_direct_records(rom)
    if len(table) != 52 or len(direct) != 42:
        raise ValueError("original legacy record catalog differs")
    if sum(row["end"] - row["start"] for row in direct) != 1198:
        raise ValueError("original direct record extent differs")
    records = [*table, *direct]
    observed = {dialect: set() for dialect in CONTROLS}
    for record in records:
        for word in record["tokens"][:-1]:
            item = token(word, record["dialect"])
            if item["kind"] == "control":
                observed[record["dialect"]].add(word)
        if record["tokens"][-1] != TERMINATORS[record["dialect"]]:
            raise ValueError("original legacy terminator differs")
    if observed != {key: set(value) for key, value in CONTROLS.items()}:
        raise ValueError("observed control vocabulary differs")
    return records


def token(word, dialect):
    shared.uint(word, 0xFFFF, "legacy full WORD")
    if type(dialect) is not str or dialect not in CONTROLS:
        raise ValueError("unknown legacy dialect")
    if word in TERMINATORS.values():
        raise ValueError("terminator is forbidden inside the record body")
    if word & 0x8000:
        if word not in CONTROLS[dialect]:
            raise ValueError("unknown or cross-dialect legacy control WORD")
        return dict(kind="control", WORD=word)
    legacy.font16_row_column(word)
    index = legacy.font16_index(word)
    if index >= legacy.FONT16_GLYPH_COUNT:
        raise ValueError("legacy glyph WORD resolves beyond the original font")
    return dict(kind="glyph", WORD=word)


def record_metadata(record):
    return dict(id=ident(record["start"]), group=record["group"],
                index=record["index"], start=record["start"], end=record["end"],
                dialect=record["dialect"], terminator_WORD=record["terminator"],
                reference_offsets=list(record.get("reference_offsets", [])))


def extract(rom):
    verify_rom(rom)
    records = original_records(rom)
    result = metadata()
    result["directory"] = [dict(id=f"legacy_pointer_{index:02d}",
                                address=legacy.POINTER_TABLE_START + 4 * index,
                                source=ident(record["start"]))
                           for index, record in enumerate(records[:52])]
    result["records"] = [dict(**record_metadata(record),
                              tokens=[token(word, record["dialect"])
                                      for word in record["tokens"][:-1]])
                         for record in records]
    blocks(rom, result)
    return result


def _encode_record(row, original):
    fixed = record_metadata(original)
    shared.keys(row, set(fixed) | {"tokens"}, "legacy record")
    for key, value in fixed.items():
        shared.same(row[key], value, "record." + key)
    items = exact_list(row["tokens"], len(original["tokens"]) - 1, "legacy body WORDs")
    words = []
    for item, old_word in zip(items, original["tokens"][:-1]):
        shared.keys(item, {"kind", "WORD"}, "legacy token")
        validated = token(item["WORD"], row["dialect"])
        shared.same(item["kind"], validated["kind"], "legacy token kind")
        # Retain control positions, while allowing observed same-dialect control
        # values and complete, address-validated glyph WORD edits.
        shared.same(item["kind"], token(old_word, row["dialect"])["kind"],
                    "original control/glyph position")
        words.append(item["WORD"])
    words.append(row["terminator_WORD"])
    data = b"".join(word.to_bytes(2, "big") for word in words)
    if len(data) != row["end"] - row["start"]:
        raise ValueError("fixed legacy slot width differs")
    return data


def blocks(rom, fields):
    verify_rom(rom)
    shared.keys(fields, set(metadata()) | {"directory", "records"}, "legacy package")
    for key, value in metadata().items():
        shared.same(fields[key], value, "package." + key)
    originals = original_records(rom)
    catalog = {ident(row["start"]): row["start"] for row in originals[:52]}
    directory = bytearray()
    for index, row in enumerate(exact_list(fields["directory"], 52, "BE32 directory")):
        shared.keys(row, {"id", "address", "source"}, "legacy pointer")
        shared.same(row["id"], f"legacy_pointer_{index:02d}", "pointer id")
        shared.same(row["address"], legacy.POINTER_TABLE_START + 4 * index, "pointer address")
        if type(row["source"]) is not str or row["source"] not in catalog:
            raise ValueError("pointer must target an existing physical FF table record")
        directory.extend(catalog[row["source"]].to_bytes(4, "big"))
    result = [dict(id="rom_028240_legacy_directory", start=legacy.POINTER_TABLE_START,
                   end=legacy.POINTER_TABLE_END, data=bytes(directory),
                   role="confirmed_legacy_BE32_record_directory")]
    for row, original in zip(exact_list(fields["records"], 94, "physical records"), originals):
        result.append(dict(id=ident(original["start"]), start=original["start"],
                           end=original["end"], data=_encode_record(row, original),
                           role="confirmed_legacy_" + original["dialect"] + "_WORDs"))
    result.sort(key=lambda row: row["start"])
    if (sum(len(row["data"]) for row in result) != EDITABLE_BYTES
            or any(left["end"] > right["start"] for left, right in zip(result, result[1:]))):
        raise ValueError("legacy nonoverlapping physical scope differs")
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def _catalog_rows(rom, catalog):
    """Preview-only labels tied to each actual font bitmap, never a text codec."""
    if catalog is None:
        return None
    if type(catalog) is not dict:
        raise ValueError("preview catalog must be an object")
    shared.same(catalog.get("rom_sha256"), legacy.EXPECTED_ROM_SHA256, "catalog ROM")
    shared.same(catalog.get("font_sha256"), sha(rom[legacy.FONT16_START:legacy.FONT16_END]),
                "catalog font")
    rows = exact_list(catalog.get("glyphs"), legacy.FONT16_GLYPH_COUNT, "catalog glyphs")
    for index, row in enumerate(rows):
        if type(row) is not dict:
            raise ValueError("preview glyph label must be an object")
        address = legacy.FONT16_START + index * 32
        for key, value in dict(glyph_index=index, address=address,
                               bitmap_sha256=sha(rom[address:address + 32])).items():
            shared.same(row.get(key), value, "catalog glyph." + key)
        if row.get("confidence") not in ("confirmed", "probable", "unknown"):
            raise ValueError("preview glyph confidence differs")
        label = row.get("unicode")
        if label is not None and (type(label) is not str or len(label) != 1):
            raise ValueError("preview glyph must have one manual character or null")
        if (row["confidence"] == "unknown") != (label is None):
            raise ValueError("unknown preview reading must remain null")
    return rows


def preview(rom, fields, catalog=None):
    blocks(rom, fields)
    labels = _catalog_rows(rom, catalog)
    result = dict(confidence="confirmed", editing_authority="fields.json full WORDs only",
                  Unicode_role="individually graded manual bitmap labels",
                  catalog_sha256=None if catalog is None else sha(dump(catalog)), records=[])
    for row in fields["records"]:
        items = []
        text = []
        for item in [*row["tokens"], dict(kind="terminator", WORD=row["terminator_WORD"])]:
            word = item["WORD"]
            view = dict(**item, escape=f"⟦{word:04X}⟧", unicode=None, confidence="unknown")
            if item["kind"] == "glyph":
                index = legacy.font16_index(word)
                view.update(glyph_index=index, glyph_ROM=legacy.FONT16_START + index * 32,
                            attribute_bits_WORD=word & 0xE000)
                if labels is not None:
                    view.update(unicode=labels[index]["unicode"], confidence=labels[index]["confidence"])
            else:
                view.update(control_name=legacy.CONTROL_NAMES[word], confidence="confirmed")
            text.append(view["unicode"] if item["kind"] == "glyph"
                        and view["confidence"] == "confirmed" else view["escape"])
            items.append(view)
        result["records"].append(dict(id=row["id"], dialect=row["dialect"],
                                      text="".join(text), WORDs=items))
    return result


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
        return dict(type={str: "string", int: "integer", bool: "boolean"}[type(value)], const=value)
    def exact_array(rows):
        return dict(type="array", prefixItems=rows, items=False, minItems=len(rows), maxItems=len(rows))
    catalog = [ident(row["start"]) for row in fields["records"][:52]]
    directory = [obj(dict(id=fixed(row["id"]), address=fixed(row["address"]),
                          source=dict(type="string", enum=catalog))) for row in fields["directory"]]
    records = []
    for row in fields["records"]:
        properties = {key: fixed(value) for key, value in row.items() if key != "tokens"}
        properties["tokens"] = exact_array([obj(dict(kind=fixed(item["kind"]),
            WORD=dict(type="integer", minimum=0, maximum=65535))) for item in row["tokens"]])
        records.append(obj(properties))
    properties = {key: fixed(value) for key, value in metadata().items()}
    properties.update(directory=exact_array(directory), records=exact_array(records))
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Runtime additionally validates per-dialect controls, glyph addresses and exact pinned slot topology."
    return result


def render_bundle(rom, catalog=None):
    fields = extract(rom)
    data = dump(fields)
    image = rebuild(rom, load_fields(data))
    rows = blocks(rom, fields)
    if image != rom:
        raise ValueError("entire-ROM serialized WORD roundtrip differs")
    controls = Counter(f"{item['WORD']:04X}" for row in fields["records"]
                       for item in row["tokens"] if item["kind"] == "control")
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=len(rows),
                  BE32_directory_bytes=208, table_record_bytes=1450, direct_record_bytes=1198,
                  table_records=52, direct_records=42, direct_MOVE_LONG_xrefs=50,
                  ff_records=56, control80_records=38, full_WORDs_including_terminators=1324,
                  control_histogram=dict(sorted(controls.items())),
                  whole_ROM_exact=True, whole_ROM_sha256=sha(image),
                  allowed_pointer_catalog="52 original physical FF table records; aliases allowed",
                  font_offset_formula="(((WORD & FF00) << 3) & FFFF) | ((WORD & 00FF) << 5)",
                  direct_xref_source="tools.text_font.text_font_assets.discover_direct_records",
                  evidence=dict(directory_consumer=0x28228, legacy_font_reader=0xAE8A,
                                direct_destination_RAM=0xFF700E),
                  original_control_positions_and_terminators_pinned=True,
                  natural_selection="unknown", edited_gameplay_safety="unknown",
                  independent_CPU_comparison=False,
                  blocks=[{key: value for key, value in row.items() if key != "data"}
                          | dict(sha256=sha(row["data"])) for row in rows])
    view = preview(rom, fields, catalog)
    lines = ["Legacy FF/80 text; preview labels are not an editable encoding.",
             "Full WORDs in fields.json retain controls, attributes and terminators.", ""]
    lines.extend(row["id"] + "\t" + json.dumps(row["text"], ensure_ascii=False) for row in view["records"])
    members = {"fields.json": data, "fields.schema.json": dump(schema(rom)),
               "validation.json": dump(report), "preview.json": dump(view),
               "preview.txt": ("\n".join(lines) + "\n").encode("utf-8")}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        members={name: dict(bytes=len(payload), sha256=sha(payload)) for name, payload in members.items()},
        independent_CPU_comparison=False))
    return members


def fresh_output(value):
    path = shared.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError("output must stay in build/legacy_text_fields or be the fresh formal generated directory")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "import", "verify"))
    parser.add_argument("--rom", default=str(DEFAULT_ROM))
    parser.add_argument("--fields", default=str(DEFAULT_FIELDS))
    parser.add_argument("--catalog", default=str(DEFAULT_CATALOG))
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    target = None
    if args.command != "verify":
        if args.output is None:
            raise ValueError("fresh output required")
        target = fresh_output(args.output)
        if args.command == "import" and target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin required")
    elif args.output is not None:
        raise ValueError("verify does not write")
    rom = shared.read_bounded(args.rom, legacy.EXPECTED_ROM_SIZE)
    if args.command == "export":
        catalog = load_fields(shared.read_bounded(args.catalog, shared.MAX_JSON))
        members = render_bundle(rom, catalog)
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
