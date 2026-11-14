"""Two actually-read big-endian WORD-RLE prefixes, not complete streams.

The original title callers load D6=16 before entry03AAD6, which retains D6.
03AB32 returns to the caller after32 WORDs per row, even during a repeat.
Only409+49 source bytes belong to this editor. The two unread10-byte tails
are excluded; neither invented terminators nor raw/padding fields are emitted.
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
from tools.graphics_build import rle_fields as rle
from tools.battle_overlay_maps.codec import project_map

DEFAULT_ROM = shared.DEFAULT_ROM
FORMAL_ROOT = ROOT / "analysis/title_overlay_maps/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
OUTPUT_ROOT = ROOT / "build/title_overlay_maps"
FORMAT = "candidate-title-overlay-read-prefix-WORD-rle-v1"
EDITABLE_BYTES = 458
ROWS = 16
WORDS_PER_ROW = 32
OUTPUT_WORDS = ROWS * WORDS_PER_ROW
# Actually-read end followed by an excluded physical candidate slot end.
LAYOUT = ((0x065FF6, 0x06618F, 0x066199), (0x066199, 0x0661CA, 0x0661D4))
CALLERS = ((0x00423C, 0x004256, 0x0042C6, 0x0042E0, 0xC000),
           (0x00425C, 0x004276, 0x0042E6, 0x004300, 0xC040))
CALL_PAIR_BYTES = bytes.fromhex(
    "41f900065ff643f90000" "c0002a3c00000080427880003c3c00104eb90003aad6"
    "41f90006619943f90000" "c0402a3c00000080427880003c3c00104eb90003aad6")
READER_BYTES = bytes.fromhex(
    "4278800233fc8f0200c000043009610007ca78004a7880026602121814184a788002"
    "6606b20267000014e14214188478800033c200c00000612260e07600161867000038"
    "1418e14214188478800033c200c00000610651cbfff260c052440c04002065000016"
    "534666064cdf00014e75d3c530096100076478004e75")
sha = shared.sha
dump = shared.dump
keys = shared.keys
uint = shared.uint


def ident(start):
    return f"rom_{start:06X}_map_prefix"


BY_ID = {ident(start): (start, end, physical_end) for start, end, physical_end in LAYOUT}


def metadata():
    return dict(format=FORMAT,
                canonical_source=dict(size=shared.ROM_SIZE, sha256=shared.ROM_SHA),
                confidence="confirmed_read_encoding_candidate_visual_role",
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != shared.ROM_SIZE or sha(rom) != shared.ROM_SHA:
        raise ValueError("canonical ROM bytes/size/identity required")
    for start in (0x00423C, 0x0042C6):
        if rom[start:start + len(CALL_PAIR_BYTES)] != CALL_PAIR_BYTES:
            raise ValueError("original source/D6/call/output-OR anchor differs")
    if rom[0x03AAD6:0x03AAD6 + len(READER_BYTES)] != READER_BYTES:
        raise ValueError("original marker/WORD/row-return reader anchor differs")


def topology(start, end, physical_end, call):
    first_lea, first_jsr, second_lea, second_jsr, vram = call
    return dict(id=ident(start), start=start, end=end, byte_order="big",
                output_rows=ROWS, WORDs_per_row=WORDS_PER_ROW, output_WORDs=OUTPUT_WORDS,
                stop="row_limit_not_marker_zero", source_LEAs=[first_lea, second_lea],
                source_JSRs=[first_jsr, second_jsr], reader_entry=0x03AAD6,
                output_OR_WORD=0, VRAM_target=vram, row_stride_bytes=128,
                excluded_unread_interval=[end, physical_end])


def parse_prefix(data, words=OUTPUT_WORDS):
    """Parse only bytes actually consumed before the D6/32-WORD row exit."""
    uint(words, OUTPUT_WORDS, "bounded row output WORDs")
    if not words or type(data) is not bytes or not 3 <= len(data) <= 2049:
        raise ValueError("bounded nonempty read prefix required")
    marker = data[0]
    cursor = 1
    commands = []
    emitted = 0
    while emitted < words:
        if cursor >= len(data):
            raise ValueError("row limit not reached before source end")
        first = data[cursor]
        cursor += 1
        if first == marker:
            if cursor >= len(data):
                raise ValueError("short escape count")
            count = data[cursor] + 1
            cursor += 1
            if count == 1:
                raise ValueError("marker-zero terminates before required row exit")
            if cursor + 2 > len(data):
                raise ValueError("short repeat WORD")
            word = int.from_bytes(data[cursor:cursor + 2], "big")
            cursor += 2
            commands.append(dict(op="repeat", count=count, word=word))
        else:
            if cursor >= len(data):
                raise ValueError("short literal WORD")
            word = first << 8 | data[cursor]
            cursor += 1
            count = 1
            commands.append(dict(op="literal", word=word))
        emitted += count
    if cursor != len(data):
        raise ValueError("unread source bytes cannot become prefix fields")
    return dict(marker=marker, commands=commands)


def pack_prefix(fields, words=OUTPUT_WORDS):
    """Retain the final command's full count; project only actual WORD writes.

    The existing encoder is reused for complete command encoding. Its temporary
    marker-zero suffix is removed, never written into the original prefix.
    """
    uint(words, OUTPUT_WORDS, "bounded row output WORDs")
    if not words:
        raise ValueError("nonzero row output required")
    shared.strict_commands(fields)
    commands = fields["commands"]
    if not 1 <= len(commands) <= words:
        raise ValueError("bounded nonempty prefix command list required")
    emitted = 0
    for command in commands:
        if emitted >= words:
            raise ValueError("command after original row exit is unread")
        emitted += command["count"] if command["op"] == "repeat" else 1
    if emitted < words:
        raise ValueError("prefix commands do not reach original row exit")
    raw, expanded = rle.pack_word(fields, "big", emitted)
    prefix = raw[:-2]
    if parse_prefix(prefix, words) != fields:
        raise ValueError("read-prefix grammar roundtrip differs")
    return prefix, expanded[:2 * words]


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields["maps"] = [dict(**topology(start, end, physical_end, call),
                           fields=parse_prefix(rom[start:end]))
                      for (start, end, physical_end), call in zip(LAYOUT, CALLERS)]
    blocks(rom, fields)
    return fields


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"maps"}, "package")
    for key, value in fixed.items():
        shared.same(fields[key], value, "package." + key)
    maps = fields["maps"]
    if type(maps) is not list or len(maps) != 2:
        raise ValueError("exactly two physical source prefixes required")
    result = []
    for row, (start, end, physical_end), call in zip(maps, LAYOUT, CALLERS):
        fixed = topology(start, end, physical_end, call)
        keys(row, set(fixed) | {"fields"}, "map")
        for key, value in fixed.items():
            shared.same(row[key], value, "map." + key)
        raw, decoded = pack_prefix(row["fields"])
        if len(raw) != end - start:
            raise ValueError("fixed actually-read source cost differs; no blob/growth fallback")
        projection = project_map(raw, ROWS)
        if (projection["stop"] != "row_limit" or projection["consumed"] != len(raw)
                or projection["output"] != decoded):
            raise ValueError("original row/source-prefix projection differs")
        result.append(dict(id=row["id"], start=start, end=end, data=raw,
                           role="candidate_title_overlay_big_WORD_rle_read_prefix"))
    if sum(len(row["data"]) for row in result) != EDITABLE_BYTES:
        raise ValueError("physical read-prefix scope differs")
    if any(a["end"] > b["start"] for a, b in zip(result, result[1:])):
        raise ValueError("overlapping read-prefix blocks")
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def decode(rom, fields, map_id):
    blocks(rom, fields)
    if type(map_id) is not str or map_id not in BY_ID:
        raise ValueError("unknown physical prefix")
    row = next(row for row in fields["maps"] if row["id"] == map_id)
    return pack_prefix(row["fields"])[1]


def load_fields(data):
    return shared.load_json(data)


def schema():
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({key: fixed(item) for key, item in value.items()})
        if type(value) is list:
            return dict(type="array", prefixItems=[fixed(item) for item in value],
                        items=False, minItems=len(value), maxItems=len(value))
        return dict(type={str: "string", int: "integer"}[type(value)], const=value)
    integer = lambda maximum: dict(type="integer", minimum=0, maximum=maximum)
    literal = obj(dict(op=dict(type="string", const="literal"), word=integer(65535)))
    repeat = obj(dict(op=dict(type="string", const="repeat"), word=integer(65535),
                      count=dict(type="integer", minimum=2, maximum=256)))
    stream = obj(dict(marker=integer(255), commands=dict(type="array", minItems=1,
        maxItems=OUTPUT_WORDS, items=dict(oneOf=[literal, repeat]))))
    rows = []
    for layout, call in zip(LAYOUT, CALLERS):
        properties = {key: fixed(value) for key, value in topology(*layout, call).items()}
        properties["fields"] = stream
        rows.append(obj(properties))
    properties = {key: fixed(value) for key, value in metadata().items()}
    properties["maps"] = dict(type="array", prefixItems=rows, items=False, minItems=2, maxItems=2)
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Runtime additionally enforces fixed consumed byte costs and original row exit within the final command. No stream terminator or unread tail is owned."
    return result


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError("whole-ROM serialized read-prefix roundtrip differs")
    runs = []
    for row, (start, end, physical_end) in zip(fields["maps"], LAYOUT):
        original = project_map(rom[start:physical_end], ROWS)
        source, decoded = pack_prefix(row["fields"])
        prefix = project_map(source, ROWS)
        if original != prefix or original["output"] != decoded:
            raise ValueError("full old source and new prefix projections differ")
        runs.append(dict(id=row["id"], source_read_start=start, source_read_end=end,
            source_read_bytes=len(source), output_WORDs=len(decoded) // 2,
            commands_read=prefix["commands_read"], remaining_repeat_WORDs=prefix["remaining_repeat_WORDs"],
            stop=prefix["stop"], output_WORDs_sha256=sha(decoded), source_sha256=sha(source),
            excluded_unread_interval=[end, physical_end]))
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=2,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), decoded_WORDs_per_map=OUTPUT_WORDS,
        original_reader_entry=0x03AAD6, original_WORD_reader=0x03AAF2,
        original_repeat_reader=0x03AB12, original_row_return=0x03AB32,
        caller_D6=16, WORDs_per_row=32, output_OR_WORD=0, original_row_stride_bytes=128,
        original_call_pair_anchors=[0x00423C, 0x0042C6],
        command_count_plus_one_preserved=True, terminator_emitted=False,
        unread_bytes_excluded=20, unknown_intervals=[[end, physical_end] for _, end, physical_end in LAYOUT],
        maps=runs, reused_implementation=["graphics_build.rle_fields.pack_word",
            "battle_overlay_maps.codec.project_map"],
        source_read_encoding_confidence="confirmed", visual_role_confidence="candidate",
        edited_gameplay_safety="unknown", independent_CPU_comparison=False,
        CPU_reference_from_zero=False, port_timing_proven=False,
        natural_selector_domain_complete=False)
    members = {"fields.json": dump(fields), "fields.schema.json": dump(schema()),
               "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()},
        independent_CPU_comparison=False))
    return members


def fresh_output(value):
    path = shared.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError("output must stay in build/title_overlay_maps or be the fresh formal generated directory")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "import", "verify", "decode"))
    parser.add_argument("--rom", default=str(DEFAULT_ROM))
    parser.add_argument("--fields", default=str(DEFAULT_FIELDS))
    parser.add_argument("--output")
    parser.add_argument("--map-id")
    args = parser.parse_args(argv)
    if (args.command == "decode") != (args.map_id is not None):
        raise ValueError("--map-id is required only for decode")
    target = None
    if args.command != "verify":
        if args.output is None:
            raise ValueError("fresh output required")
        target = fresh_output(args.output)  # Output authority checked BEFORE input reads.
        if args.command in ("import", "decode") and target.suffix.lower() != ".bin":
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
        data = decode(rom, fields, args.map_id) if args.command == "decode" else rebuild(rom, fields)
        if target is not None:
            shared.put(target, data)
        result = dict(path=None if target is None else str(target), sha256=sha(data),
                      exact_canonical=data == rom, editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
