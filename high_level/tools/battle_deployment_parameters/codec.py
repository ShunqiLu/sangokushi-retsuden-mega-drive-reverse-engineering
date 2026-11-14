"""Lossless fixed BYTE fields for two original deployment parameter ranges.

The 15 pairs and six directory bytes are physical editor allocations. They do
not impose a CPU selector clamp or describe a complete natural parameter domain.
Data APIs are pure; only the CLI opens files. The original ROM is hash gated.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
OUTPUT_ROOT = ROOT / "build/battle_deployment_parameters"
DEFAULT_BUNDLE = ROOT / "analysis/battle_deployment_parameters/generated"
FORMAL_ROOT = DEFAULT_BUNDLE
DEFAULT_FIELDS = DEFAULT_BUNDLE / "fields.json"
EDITABLE_BYTES = 36
FORMAT = "g5510-battle-deployment-fixed-BYTE-fields-v1"
MAX_JSON = 1024 * 1024
PAIR_START, PAIR_END = 0x01B832, 0x01B850
DIRECTORY_START, DIRECTORY_END = 0x01B890, 0x01B896
PAIR_ID = "rom_01B832_deployment_pairs"
DIRECTORY_ID = "rom_01B890_deployment_terrain_directory"
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
SEALED_PATH = "analysis/secondary_dispatch_code/generated/instructions.json"
SEALED_SHA256 = reference_value(__name__, 'SEALED_SHA256')
# The existing sealed source grades these instructions candidate. Exact source
# bytes and 68000 addressing mechanics do not promote their runtime reachability.
CONSUMERS = (
    (0x01B7DC, "4243"),
    (0x01B7E6, "5043"), (0x01B7F0, "5043"), (0x01B7FA, "5043"),
    (0x01B804, "5443"), (0x01B80E, "5443"), (0x01B818, "5443"),
    (0x01B81A, "13fb3016ffff80da"),
    (0x01B822, "4239ffff8124"),
    (0x01B828, "13fb3009ffff8125"),
    (0x01B850, "41f89000"),
    (0x01B87C, "4241"), (0x01B87E, "12300000"),
    (0x01B882, "41fa000c"), (0x01B886, "13f01000ffff80db"),
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def keys(value, expected, label):
    if type(value) is not dict or set(value) != set(expected):
        raise ValueError(label + ": missing or unknown fields")


def same(value, expected, label):
    if type(value) is not type(expected) or value != expected:
        raise ValueError(label + ": pinned metadata or type differs")
    if type(expected) is dict:
        for key in expected:
            same(value[key], expected[key], label + "." + key)
    elif type(expected) is list:
        for index, item in enumerate(expected):
            same(value[index], item, label + f"[{index}]")


def uint(value, maximum, label):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError(label + ": strict unsigned integer required")
    return value


def exact_list(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ": fixed physical count differs")
    return value


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    for address, raw in CONSUMERS:
        if rom[address:address + len(raw) // 2] != bytes.fromhex(raw):
            raise ValueError("pinned consumer source bytes differ")


def metadata():
    return dict(
        format=FORMAT, confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        physical_scope=[dict(id=PAIR_ID, start=PAIR_START, end=PAIR_END, bytes=30),
                        dict(id=DIRECTORY_ID, start=DIRECTORY_START, end=DIRECTORY_END, bytes=6)],
        evidence=dict(
            confidence="confirmed", source="canonical bytes + existing sealed instruction rows",
            sealed_instructions=dict(path=SEALED_PATH, sha256=SEALED_SHA256,
                                     consumer_reachability_confidence="candidate"),
            instructions=[dict(address=address, bytes=raw, source_confidence="candidate")
                          for address, raw in CONSUMERS],
            pair_consumers=[dict(address=0x01B81A, extension_WORD=0x3016,
                                 PC_base=0x01B81C, effective_base=PAIR_START,
                                 index="signed D3.W", destination_RAM=0xFF80DA),
                            dict(address=0x01B828, extension_WORD=0x3009,
                                 PC_base=0x01B82A, effective_base=PAIR_START + 1,
                                 index="signed D3.W", destination_RAM=0xFF8125)],
            pair_index=dict(formula="D3.W = 8*row + 2*column", comparison_outcomes_per_axis=4,
                            maximum_on_this_comparison_path=30, CPU_clamp=False,
                            maximum_reads=[0x01B850, 0x01B851],
                            maximum_read_original_hex="41f8", maximum_reads_are_code=True),
            terrain_consumer=dict(LEA_address=0x01B882, PC_base=0x01B884,
                                  displacement_WORD=0x000C, effective_base=DIRECTORY_START,
                                  read_address=0x01B886, index="D1.W after CLR.W then MOVE.B",
                                  selector_BYTE_min=0, selector_BYTE_max=255,
                                  destination_RAM=0xFF80DB, CPU_clamp=False,
                                  six_entries_are_physical_edit_scope=True)),
        natural_parameter_semantics="unknown", edited_gameplay_safety="unknown",
        independent_CPU_comparison=False,
    )


def pair_read_addresses(d3_WORD):
    """Diagnostic address arithmetic for signed WORD indexing, without a clamp."""
    uint(d3_WORD, 0xFFFF, "D3.W")
    signed = d3_WORD - 0x10000 if d3_WORD & 0x8000 else d3_WORD
    return (PAIR_START + signed, PAIR_START + 1 + signed)


def terrain_read_address(selector_BYTE):
    """Diagnostic zero-extended BYTE selector address, including outside six slots."""
    return DIRECTORY_START + uint(selector_BYTE, 255, "selector BYTE")


def lookup_pair(image, d3_WORD):
    """Read the actual two BYTEs from an original or edited image, without clamping."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires a complete bytes image")
    first, second = pair_read_addresses(d3_WORD)
    return (image[first], image[second])


def lookup_terrain(image, selector_BYTE):
    """Read the actual directory-indexed BYTE, even outside the editor allocation."""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("diagnostic lookup requires a complete bytes image")
    return image[terrain_read_address(selector_BYTE)]


def pair_fixed(index):
    return dict(id=f"deployment_pair_{index:02d}", index=index,
                address=PAIR_START + index * 2,
                first_destination_RAM=0xFF80DA, second_destination_RAM=0xFF8125)


def terrain_fixed(index):
    return dict(id=f"terrain_parameter_{index:02d}", index=index,
                address=DIRECTORY_START + index, destination_RAM=0xFF80DB)


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result["pairs"] = [dict(**pair_fixed(index), first_BYTE=rom[PAIR_START + 2 * index],
                            second_BYTE=rom[PAIR_START + 2 * index + 1]) for index in range(15)]
    result["terrain_directory"] = [dict(**terrain_fixed(index), BYTE=rom[DIRECTORY_START + index])
                                   for index in range(6)]
    return result


def blocks(rom, fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields, set(fixed) | {"pairs", "terrain_directory"}, "deployment package")
    for key, value in fixed.items():
        same(fields[key], value, "package." + key)
    pairs = bytearray()
    for index, row in enumerate(exact_list(fields["pairs"], 15, "physical pairs")):
        pinned = pair_fixed(index)
        keys(row, set(pinned) | {"first_BYTE", "second_BYTE"}, "pair")
        for key, value in pinned.items():
            same(row[key], value, "pair." + key)
        pairs.extend((uint(row["first_BYTE"], 255, "first BYTE"),
                      uint(row["second_BYTE"], 255, "second BYTE")))
    directory = bytearray()
    for index, row in enumerate(exact_list(fields["terrain_directory"], 6, "physical terrain bytes")):
        pinned = terrain_fixed(index)
        keys(row, set(pinned) | {"BYTE"}, "terrain item")
        for key, value in pinned.items():
            same(row[key], value, "terrain." + key)
        directory.append(uint(row["BYTE"], 255, "terrain BYTE"))
    result = [dict(id=PAIR_ID, start=PAIR_START, end=PAIR_END, data=bytes(pairs),
                   role="confirmed_physical_deployment_BYTE_pairs"),
              dict(id=DIRECTORY_ID, start=DIRECTORY_START, end=DIRECTORY_END, data=bytes(directory),
                   role="confirmed_physical_terrain_parameter_BYTE_directory")]
    if [len(row["data"]) for row in result] != [30, 6] or result[0]["end"] > result[1]["start"]:
        raise ValueError("fixed physical byte costs or nonoverlap differs")
    return result


def rebuild(rom, fields):
    encoded = blocks(rom, fields)
    image = bytearray(rom)
    for row in encoded:
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def load_fields(data):
    if type(data) is not bytes or len(data) > MAX_JSON:
        raise ValueError("bounded JSON bytes required")
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError("nonfinite JSON number: " + value)
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=nonfinite)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError("invalid bounded UTF-8 JSON") from exc


def schema():
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({key: fixed(item) for key, item in value.items()})
        if type(value) is list:
            return exact([fixed(item) for item in value])
        return dict(type={str: "string", int: "integer", bool: "boolean"}[type(value)], const=value)
    def exact(items):
        return dict(type="array", prefixItems=items, items=False, minItems=len(items), maxItems=len(items))
    byte = dict(type="integer", minimum=0, maximum=255)
    properties = {key: fixed(value) for key, value in metadata().items()}
    properties["pairs"] = exact([obj({**{key: fixed(value) for key, value in pair_fixed(index).items()},
                                      "first_BYTE": byte, "second_BYTE": byte}) for index in range(15)])
    properties["terrain_directory"] = exact([obj({**{key: fixed(value) for key, value in terrain_fixed(index).items()},
                                                  "BYTE": byte}) for index in range(6)])
    result = obj(properties)
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "Fixed 30+6 physical BYTE costs; editor counts do not clamp CPU selectors or prove natural domains."
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom:
        raise ValueError("whole-ROM serialized field roundtrip differs")
    encoded = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=36, physical_blocks=2, pair_count=15,
                  pair_bytes=30, terrain_directory_items=6, terrain_directory_bytes=6,
                  whole_ROM_exact=True, whole_ROM_sha256=sha(image),
                  original_pairs_hex=rom[PAIR_START:PAIR_END].hex(),
                  original_terrain_directory_hex=rom[DIRECTORY_START:DIRECTORY_END].hex(),
                  CPU_pair_D3_30_addresses=list(pair_read_addresses(30)),
                  CPU_terrain_selector_6_address=terrain_read_address(6),
                  CPU_terrain_selector_255_address=terrain_read_address(255),
                  blocks=[{key: value for key, value in row.items() if key != "data"}
                          | dict(bytes=len(row["data"]), sha256=sha(row["data"])) for row in encoded])
    members = {"fields.json": serialized, "fields.schema.json": dump(schema()),
               "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(
        **metadata(), editable_bytes=36, physical_blocks=2,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def safe_path(value, regular_input=False):
    if not isinstance(value, (str, Path)) or not str(value) or "\x00" in str(value):
        raise ValueError("plain local path required")
    text = str(value).replace("/", "\\")
    if text.startswith("\\\\") or text.startswith("\\??\\") or text.upper().startswith(("\\DEVICE\\", "\\DOSDEVICES\\", "\\GLOBALROOT\\")):
        raise ValueError("UNC/device namespace rejected before file access")
    win = PureWindowsPath(text)
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
    for part in win.parts:
        if part in (win.anchor, win.drive, "\\", ".", ".."):
            continue
        if ":" in part or part.rstrip(" .").split(".")[0].rstrip(" ").upper() in reserved:
            raise ValueError("device or ADS component rejected")
    source = Path(value)
    if source.is_symlink():
        raise ValueError("symlink path rejected")
    path = source.resolve()
    if regular_input and not path.is_file():
        raise ValueError("regular local input required")
    return path


def fresh_output(value, bundle=False):
    path = safe_path(value)
    in_build = path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents
    if not in_build and not (bundle and path == DEFAULT_BUNDLE):
        raise ValueError("output must stay in battle_deployment_parameters build scope or the exact formal bundle")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def read_bounded(value, maximum):
    path = safe_path(value, regular_input=True)
    if path.stat().st_size > maximum:
        raise ValueError("input exceeds byte bound")
    with path.open("rb") as stream:
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        raise ValueError("input grew beyond byte bound")
    return data


def put(path, data):
    with path.open("xb") as stream:
        stream.write(data)


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
            raise ValueError("export requires a fresh output only")
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
        result = dict(path=str(target), editable_bytes=36,
                      members={name: sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        members = render_bundle(rom)
        for name, data in members.items():
            if read_bounded(bundle / name, MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=36, whole_ROM_exact=True,
                      whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            put(target, image)
        result = dict(path=None if target is None else str(target), editable_bytes=36,
                      exact_canonical=image == rom, bytes=len(image), sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
