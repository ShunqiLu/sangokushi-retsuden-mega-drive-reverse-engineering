#!/usr/bin/env python3
"""Compose all recovered audio fields into editable, nonopaque GNU sources.

The formats package is the sole source of shared FM records. Sequence evidence
references those records instead of keeping a second editable copy. The three
original evidence manifests retain their confidence boundaries unchanged.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.audio_formats import audio_formats as af
from tools.audio_envelopes import audio_envelopes as ae
from tools.audio_sequences import audio_sequences as sq
from tools.audio_sequences import rhythm

DEFAULT_ROM = af.DEFAULT_ROM
DEFAULT_ASSETS = ROOT / "analysis/audio_build/generated/assets.json"
FORMAT = "g5510-unified-typed-audio-v1"


def extract(rom: bytes) -> dict[str, Any]:
    sequences = sq.extract(rom)
    # Selected records are references to the formats bank, not independent data.
    sequences.pop("selected_instruments")
    return {"format": FORMAT, "source": {"size": af.ROM_SIZE, "sha256": af.ROM_SHA256},
            "definitions": af.extract(rom), "sequences": sequences, "envelopes": ae.extract(rom)}


def sequence_assets(rom: bytes, assets: dict[str, Any]) -> dict[str, Any]:
    expected = sq.extract(rom)
    af._keys(assets["sequences"], set(expected) - {"selected_instruments"}, "unified sequence source")
    banks = {bank["id"]: bank for bank in assets["definitions"]["instrument_banks"]}
    records = [{**ref, "record": banks[ref["bank"]]["records"][ref["index"]]}
               for ref in expected["selected_instruments"]]
    return {**assets["sequences"], "selected_instruments": records}


@dataclass(frozen=True)
class Block:
    start: int
    raw: bytes
    label: str
    kind: str
    source: str
    assembly: tuple[str, ...]

    @property
    def end(self) -> int:
        return self.start + len(self.raw)


def _hex(value: int) -> str:
    return f"0x{value:X}" if value >= 0 else str(value)


def call(name: str, *values: int) -> str:
    return "        AUDIO_" + name.upper() + (" " + ", ".join(_hex(v) for v in values) if values else "")


def fm_lines(record: dict[str, Any]) -> list[str]:
    result = [call("FM_HEADER", record["feedback_algorithm"])]
    for key in af.REGISTER_FIELDS:
        result += ["        | " + key + "; register offsets 0,8,4,12",
                   call("FM_REGISTER_ROW", *(op[key] for op in record["operators"]))]
    result.append(call("FM_TOTAL_LEVELS", *(v for op in record["operators"]
                         for v in (op["total_level"], int(op["channel_attenuation_enabled"])))))
    return result


def event_lines(event: dict[str, Any]) -> list[str]:
    kind = event["type"]
    if kind == "command":
        opcode, args = event["opcode"], event["arguments"]
        if opcode in (0xF6, 0xF8):
            return [call("CMD_" + sq.NAMES[opcode-0xE0], args[0] | args[1] << 8)]
        if opcode == 0xF7:
            return [call("CMD_LOOP", args[0], args[1], args[2] | args[3] << 8)]
        if opcode == 0xFF:
            return [call(f"EXTENDED_{event['subcommand']}", *args)]
        return [call("CMD_" + sq.NAMES[opcode-0xE0], *args)]
    if kind == "duration":
        return [call("DURATION", event["duration"])]
    if kind == "raw_frequency":
        return [call("SLIDE_FREQUENCY", event["frequency"], event["detune"], event["duration"])
                if event["detune"] is not None else call("FREQUENCY", event["frequency"], event["duration"])]
    if kind == "rhythm":
        return [call("RHYTHM", *([event["mask"]] + ([] if event["duration"] is None else [event["duration"]])))]
    if event["detune"] is not None:
        return [call("SLIDE_NOTE", event["note"], event["detune"], event["duration"])]
    return [call("NOTE", *([event["note"]] + ([] if event["duration"] is None else [event["duration"]])))]


def envelope_lines(family: str, tokens: list[dict[str, Any]]) -> list[str]:
    result = []
    for token in tokens:
        kind = token["kind"]
        if kind in ("delta", "value"):
            result.append(call("PITCH_DELTA" if kind == "delta" else "ATTENUATION_VALUE", token["value"]))
        elif kind == "reset":
            result.append(call("ENV_RESET"))
        elif kind in ("hold_81", "hold_83", "keyoff_83"):
            result.append(call("ENV_" + kind))
        elif kind == "jump":
            result.append(call("PITCH_JUMP", token["cursor"]))
        elif kind == "add_scale":
            result.append(call("PITCH_SCALE", token["increment"]))
        elif kind == "redirect":
            result.append(call("ATTENUATION_REDIRECT", token["opcode"], token["cursor"]))
        else:
            raise ValueError("unknown validated envelope token: " + kind)
    return result


def blocks(rom: bytes, assets: Any) -> list[Block]:
    """Validate full typed source, merge shared records, emit each byte once."""
    af.verify_rom(rom)
    af._keys(assets, {"format", "source", "definitions", "sequences", "envelopes"}, "unified audio")
    af._same(assets["format"], FORMAT, "format")
    af._same(assets["source"], {"size": af.ROM_SIZE, "sha256": af.ROM_SHA256}, "source")
    definition_writes = af.encode_edits(rom, assets["definitions"])
    envelope_writes = ae.encode_edits(rom, assets["envelopes"])
    expanded_sequence = sequence_assets(rom, assets)
    # Reuse the original full event/alias/lookahead validator; no identity bypass.
    sq.rebuild(rom, expanded_sequence)
    result = []
    def add(start: int, raw: bytes, kind: str, source: str, lines: list[str]) -> None:
        label = f"audio_{start:06x}_{kind}"
        result.append(Block(start, raw, label, kind, source, tuple(lines)))
    definitions = assets["definitions"]
    for table_name in ("music_pointer_table", "sfx_pointer_table"):
        table = definitions[table_name]
        add(table["rom_offset"], struct.pack("<" + "H" * len(table["pointers"]), *table["pointers"]),
            table_name, "definitions." + table_name, [call("LE16", p) for p in table["pointers"]])
    raw_definitions = {name: (start, raw) for start, raw, name in definition_writes}
    for group in ("music", "sfx"):
        for definition in definitions[group]:
            head = definition["header"]
            if group == "music":
                lines = [call("MUSIC_HEADER", head["instrument_base"], head["driver_slot_count"], head["psg_slot_count"],
                              head["duration_multiplier"], head["tempo_reload"])]
                for slot in definition["ordinary_slots"]:
                    lines.append(call("FM_SLOT", slot["sequence_ptr"], slot["transpose"], slot["attenuation"]))
                for slot in definition["psg_slots"]:
                    lines.append(call("PSG_SLOT", slot["sequence_ptr"], slot["transpose"], slot["attenuation"],
                                      slot["modulation_selector"], slot["envelope_selector"]))
            else:
                lines = [call("SFX_HEADER", head["instrument_base"], head["duration_multiplier"], head["channel_count"])]
                for slot in definition["slots"]:
                    lines.append(call("SFX_SLOT", slot["flags"], slot["channel_id"], slot["sequence_ptr"], slot["transpose"], slot["attenuation"]))
            start, raw = raw_definitions[definition["id"]]
            add(start, raw, definition["id"], "definitions." + definition["id"], lines)
    for bank in definitions["instrument_banks"]:
        for record in bank["records"]:
            start, raw = raw_definitions[f"{bank['id']}[{record['index']}]"]
            add(start, raw, "fm_record", f"definitions.{bank['id']}.records[{record['index']}]", fm_lines(record))
    raw_envelopes = dict(envelope_writes)
    for table in assets["envelopes"]["tables"]:
        start = ae.rom_offset(table["z80_pointer_start"])
        add(start, raw_envelopes[start], table["family"] + "_pointers", "envelopes." + table["family"],
            [call("LE16", p) for p in table["pointers"]])
        for allocation in table["allocations"]:
            start = ae.rom_offset(allocation["z80_start"])
            add(start, raw_envelopes[start], table["family"] + "_envelope", f"envelopes.{table['family']}.{allocation['z80_start']:04x}",
                envelope_lines(table["family"], allocation["tokens"]))
    # Canonical event views are nonoverlapping. Keep a conflict check anyway;
    # the source compiler refuses to choose a hidden last-writer for new aliases.
    for view in assets["sequences"]["views"]:
        add(view["rom_offset"], sq.encode_event(view["event"], view["event"]), "event",
            "sequences." + view["id"], event_lines(view["event"]))
    embedded = assets["sequences"]["rhythm"]
    raw_rhythm = {label: (start, raw, kind) for start, raw, kind, label in rhythm._encoded(rom, embedded)}
    for table in embedded["pointer_tables"]:
        start, raw, kind = raw_rhythm[table["id"]]
        add(start, raw, kind, "rhythm." + table["id"], [call("LE16", p) for p in table["pointers"]])
    for header in embedded["channel_headers"]:
        start, raw, kind = raw_rhythm["rhythm_" + header["family"] + "_header"]
        add(start, raw, kind, "rhythm." + header["family"] + "_header",
            [call("RHYTHM_HEADER", header["flags"], header["channel_id"], header["duration_multiplier"])])
    for descriptor in embedded["descriptors"]:
        start, raw, kind = raw_rhythm[descriptor["id"]]
        fields = descriptor["fields"]
        selector = fields["voice_index"] if descriptor["family"] == "fm" else fields["envelope_selector"]
        add(start, raw, kind, "rhythm." + descriptor["id"],
            [call("RHYTHM_DESCRIPTOR", fields["sequence_ptr"], fields["transpose"], fields["attenuation"], fields["modulation_selector"], selector)])
    for voice in embedded["voice_records"]:
        start, raw, kind = raw_rhythm[voice["id"]]
        add(start, raw, kind, "rhythm." + voice["id"], fm_lines(voice["fields"]))
    result.sort(key=lambda block: (block.start, block.end, block.label))
    for left, right in zip(result, result[1:]):
        if left.end > right.start:
            raise ValueError(f"typed source blocks overlap: {left.source} / {right.source}")
    if any(block.start // 0x10000 != (block.end - 1) // 0x10000 or block.start // 0x10000 not in (0, 15) for block in result):
        raise ValueError("audio block outside its proven bank")
    rebuilt = apply_blocks(rom, result)
    memory = sq.Memory(rebuilt)
    for view in assets["sequences"]["views"]:
        if sq.decode(memory, view["address"], sq.Mode(view["reader"], view["raw_frequency"], view["slide"])) != view["event"]:
            raise ValueError("cross-package edit changes retained sequence view: " + view["id"])
    return result


def apply_blocks(rom: bytes, rows: list[Block]) -> bytes:
    output = bytearray(rom)
    for row in rows:
        output[row.start:row.end] = row.raw
    return bytes(output)


def rebuild(rom: bytes, assets: Any) -> bytes:
    return apply_blocks(rom, blocks(rom, assets))


def macros() -> bytes:
    """Macros encode actual endian/field layout, not host-endian .word blobs."""
    lines = ["| Generated G-5510 audio field macros; no section/data emitted here."]
    def macro(name: str, parameters: str, body: list[str]) -> None:
        lines.extend(["        .macro AUDIO_" + name + (" " + parameters if parameters else "")]
                     + ["        " + line for line in body] + ["        .endm", ""])
    macro("LE16", "value", [r".byte ((\value) & 255), (((\value) >> 8) & 255)"])
    macro("MUSIC_HEADER", "bank, fm, psg, multiplier, tempo", [r"AUDIO_LE16 \bank", r".byte \fm, \psg, \multiplier, \tempo"])
    macro("SFX_HEADER", "bank, multiplier, count", [r"AUDIO_LE16 \bank", r".byte \multiplier, \count"])
    macro("FM_SLOT", "sequence, transpose, attenuation", [r"AUDIO_LE16 \sequence", r".byte \transpose, \attenuation"])
    macro("PSG_SLOT", "sequence, transpose, attenuation, modulation, envelope", [r"AUDIO_LE16 \sequence", r".byte \transpose, \attenuation, \modulation, \envelope"])
    macro("SFX_SLOT", "flags, channel, sequence, transpose, attenuation", [r".byte \flags, \channel", r"AUDIO_FM_SLOT \sequence, \transpose, \attenuation"])
    macro("RHYTHM_HEADER", "flags, channel, multiplier", [r".byte \flags, \channel, \multiplier"])
    macro("RHYTHM_DESCRIPTOR", "sequence, transpose, attenuation, modulation, selector", [r"AUDIO_PSG_SLOT \sequence, \transpose, \attenuation, \modulation, \selector"])
    macro("FM_HEADER", "feedback_algorithm", [r".byte \feedback_algorithm"])
    macro("FM_REGISTER_ROW", "offset0, offset8, offset4, offset12", [r".byte \offset0, \offset8, \offset4, \offset12"])
    macro("FM_TOTAL_LEVELS", "tl0, flag0, tl8, flag8, tl4, flag4, tl12, flag12", [
        # On GNU m68k, '|' begins a comment. Addition is exact for these
        # disjoint validated 7-bit levels and 1-bit flags and emits all 4 bytes.
        r".byte (\tl0)+((\flag0)<<7), (\tl8)+((\flag8)<<7), (\tl4)+((\flag4)<<7), (\tl12)+((\flag12)<<7)"])
    for name in ("NOTE", "RHYTHM"):
        macro(name, "value, duration=", [r".byte \value", r".ifnb \duration", r".byte \duration", ".endif"])
    macro("SLIDE_NOTE", "note, detune, duration", [r".byte \note, \detune, \duration"])
    macro("DURATION", "duration", [r".byte \duration"])
    macro("FREQUENCY", "frequency, duration", [r".byte ((\frequency)>>8)&255, (\frequency)&255, \duration"])
    macro("SLIDE_FREQUENCY", "frequency, detune, duration", [r".byte ((\frequency)>>8)&255, (\frequency)&255, \detune, \duration"])
    for opcode, name in enumerate(sq.NAMES, 0xE0):
        if opcode == 0xFF:
            continue
        if opcode in (0xF6, 0xF8):
            macro("CMD_" + name.upper(), "target", [f".byte 0x{opcode:02X}", r"AUDIO_LE16 \target"])
        elif opcode == 0xF7:
            macro("CMD_LOOP", "index, count, target", [r".byte 0xF7, \index, \count", r"AUDIO_LE16 \target"])
        else:
            macro("CMD_" + name.upper(), "arguments:vararg", [f".byte 0x{opcode:02X}", r".ifnb \arguments", r".byte \arguments", ".endif"])
    for subcommand in range(8):
        macro(f"EXTENDED_{subcommand}", "arguments:vararg", [f".byte 0xFF, {subcommand}", r".ifnb \arguments", r".byte \arguments", ".endif"])
    macro("PITCH_DELTA", "delta", [r".byte (\delta)&255"])
    macro("ATTENUATION_VALUE", "value", [r".byte \value"])
    for name, value in (("ENV_RESET", 0x80), ("ENV_HOLD_81", 0x81), ("ENV_HOLD_83", 0x83), ("ENV_KEYOFF_83", 0x83)):
        macro(name, "", [f".byte 0x{value:02X}"])
    macro("PITCH_JUMP", "cursor", [r".byte 0x82, \cursor"])
    macro("PITCH_SCALE", "increment", [r".byte 0x84, \increment"])
    macro("ATTENUATION_REDIRECT", "opcode, cursor", [r".byte \opcode, \cursor"])
    return ("\n".join(lines).rstrip("\n") + "\n").encode("utf-8")


def bank_source(bank: int, rows: list[Block]) -> bytes:
    origin = bank * 0x10000
    cursor = origin
    label = f"audio_bank_{bank:02x}_start"
    lines = [f"| Generated typed audio in bank{bank:02x}; untouched gaps remain explicit incbin.", label + ":"]
    for row in rows:
        if row.start // 0x10000 != bank:
            continue
        if cursor < row.start:
            lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-origin:X}, 0x{row.start-cursor:X}')
        lines += [f"        .if (. - {label}) != 0x{row.start-origin:X}", '        .error "typed audio block offset mismatch"',
                  "        .endif", "        | " + row.source, row.label + ":", *row.assembly,
                  f"        .if (. - {row.label}) != {len(row.raw)}", '        .error "typed audio block width mismatch"', "        .endif"]
        cursor = row.end
    if cursor < origin + 0x10000:
        lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-origin:X}, 0x{origin+0x10000-cursor:X}')
    lines += [f"        .if (. - {label}) != 0x10000", '        .error "audio bank size mismatch"', "        .endif"]
    return ("\n".join(lines) + "\n").encode("utf-8")


def manifest(rom: bytes, assets: Any, rows: list[Block]) -> dict[str, Any]:
    semantic = [af.build_map(rom, af.extract(rom)), ae.build_manifest(rom), sq.build_manifest(rom)]
    owned = {address for evidence in semantic for owner in evidence["owners"] for address in range(owner["start"], owner["end"])}
    typed = {address for row in rows for address in range(row.start, row.end)}
    return {"format": "g5510-typed-audio-build-manifest-v1", "source": assets["source"],
        "scope": "Typed source/build footprint; does not promote semantic ownership, runtime reachability or playback",
        "summary": {"blocks": len(rows), "typed_bytes": len(typed), "semantic_owner_bytes": len(typed & owned),
            "typed_probable_bytes": len(typed - owned), "bank00_typed_bytes": sum(len(r.raw) for r in rows if r.start < 0x10000),
            "bank0f_typed_bytes": sum(len(r.raw) for r in rows if r.start >= 0xF0000),
            "deduplicated_selected_fm_bytes": 3000,
            "canonical_roundtrip": apply_blocks(rom, rows) == rom,
            "image_sha256": hashlib.sha256(apply_blocks(rom, rows)).hexdigest()},
        "blocks": [{"start": row.start, "end": row.end, "label": row.label, "kind": row.kind, "source": row.source,
                    "confirmed_semantic_bytes": sum(i in owned for i in range(row.start, row.end)),
                    "sha256": hashlib.sha256(row.raw).hexdigest()} for row in rows],
        "unknowns": ["All non-audio and unparsed audio gaps remain explicit opaque slices.",
            "Typed probable resources retain their previous confidence; build source is not a new ownership proof.",
            "Edited modes/branches/headers are not certified to preserve scheduling or musical validity.",
            "Global driver state, bare F9, cross-allocation envelopes and natural playback remain separate tasks."]}


def render(rom: bytes, assets: Any, *, include_image: bool = False) -> dict[str, bytes]:
    rows = blocks(rom, assets)
    info = manifest(rom, assets, rows)
    s = info["summary"]
    report = ["# 类型化音频实际重建", "", "本包将三份恢复结果合并为单一可编辑构建源，不新增语义归属或自然播放声明。", "",
        f"- {s['blocks']} 个结构块，{s['typed_bytes']} 字节替代实际 bank00/bank0f 不透明切片。",
        f"- bank00：{s['bank00_typed_bytes']}；bank0f：{s['bank0f_typed_bytes']}。",
        f"- 三包静态语义 owner 范围内 {s['semantic_owner_bytes']} 字节；其余 {s['typed_probable_bytes']} 字节保持 probable。",
        "- 120 个已选 FM 记录的3000重复字节改为引用定义包中的唯一音色字段；不需要编辑两份数据。", "",
        "## 构建", "", "assets.json 是可编辑源；bank00.s/bank0f.s/audio_macros.s 来自字段编码。",
        "命令、大小端指针、音符、包络与音色寄存器均用类型化宏表达；每个结构有位置/长度断言。",
        "未恢复区间明确引用原分段，不把字节列表换一个名字就算作已恢复。",
        "默认重建脚本从该 assets.json 生成 build/out/audio_build，再实际汇编这两个 bank；Python字段回装另生成独立镜像供差分。", "",
        "## 边界", "", *["- " + item for item in info["unknowns"]]]
    output = {"assets.json": af._json(assets), "manifest.json": af._json(info), "audio_macros.s": macros(),
              "bank00.s": bank_source(0, rows), "bank0f.s": bank_source(15, rows),
              "README.md": ("\n".join(report) + "\n").encode("utf-8")}
    if include_image:
        output["rebuilt_typed_audio.bin"] = apply_blocks(rom, rows)
    return output


def publish(bundle: dict[str, bytes], output: str | Path, inputs: list[Path], *, replace: bool = False) -> None:
    """Publish fresh bundles, or replace only an intact previously emitted bundle."""
    target = af.safe_path(output)
    for source in inputs:
        af._separate(target, [source])
    if not target.parent.is_dir():
        raise ValueError("output parent must exist")
    known_names = {"assets.json", "manifest.json", "audio_macros.s", "bank00.s", "bank0f.s", "README.md"}
    if set(bundle) not in (known_names, known_names | {"rebuilt_typed_audio.bin"}):
        raise ValueError("unexpected generated bundle names")
    bundle = dict(bundle)
    bundle["publication.json"] = af._json({"format": "g5510-derived-audio-files-v1",
        "files": {name: hashlib.sha256(data).hexdigest() for name,data in sorted(bundle.items())}})
    old_bundle = None
    old_identity = None
    if target.exists():
        if not replace or not target.is_dir():
            raise ValueError("output must be fresh unless replace-derived is explicit")
        # Only this exact runtime directory may be replaced by the build wrapper.
        expected_target = af.safe_path(ROOT / "build/out/audio_build")
        if target != expected_target:
            raise ValueError("replace-derived is limited to this project's build/out/audio_build")
        children = list(target.iterdir())
        if {child.name for child in children} != set(bundle):
            raise ValueError("derived output contains unexpected or missing files")
        old_bundle = {child.name: af._read(af.safe_path(child, regular_input=True), 8 * 1024 * 1024) for child in children}
        record = af.load_assets(old_bundle["publication.json"])
        expected_record = {"format": "g5510-derived-audio-files-v1", "files": {
            name: hashlib.sha256(data).hexdigest() for name,data in sorted(old_bundle.items()) if name != "publication.json"}}
        af._same(record, expected_record, "intact previous derived output")
        old_identity = target.stat()
    staging = Path(tempfile.mkdtemp(prefix=".audio-build-", dir=target.parent))
    identity, produced = staging.stat(), {}
    try:
        for name, data in bundle.items():
            with (staging / name).open("xb") as stream:
                stream.write(data)
            produced[name] = data
        af.safe_path(output)
        if old_bundle is None:
            if target.exists():
                raise ValueError("output appeared during publication")
            os.rename(staging, target)
        else:
            current = target.stat()
            if (current.st_dev, current.st_ino) != (old_identity.st_dev, old_identity.st_ino):
                raise ValueError("derived output identity changed")
            if {child.name for child in target.iterdir()} != set(old_bundle):
                raise ValueError("derived output contents changed")
            for name, data in old_bundle.items():
                if af._read(af.safe_path(target / name, regular_input=True), 8 * 1024 * 1024) != data:
                    raise ValueError("derived output modified during render")
            backup = Path(tempfile.mkdtemp(prefix=".audio-build-backup-", dir=target.parent))
            backup.rmdir()  # Remove only the new empty reservation, never a tree.
            os.rename(target, backup)
            try:
                os.rename(staging, target)
            except BaseException:
                if target.exists():
                    raise ValueError(f"new target appeared; previous output retained at {backup}")
                os.rename(backup, target)
                raise
            try:
                af._cleanup_stage(backup, old_bundle, old_identity)
            except (ValueError, OSError) as error:
                raise OSError(
                    f"new output published at {target}; old output retained at {backup}; "
                    f"backup cleanup failed: {error}"
                ) from error
    finally:
        af._cleanup_stage(staging, produced, identity)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "render", "verify"))
    parser.add_argument("--rom", type=Path, default=DEFAULT_ROM)
    parser.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--include-image", action="store_true")
    parser.add_argument("--replace-derived", action="store_true")
    args = parser.parse_args(argv)
    try:
        source = af.safe_path(args.rom, regular_input=True)
        rom = af._read(source, af.ROM_SIZE)
        inputs = [source]
        if args.command == "export":
            assets = extract(rom)
        else:
            asset_path = af.safe_path(args.assets, regular_input=True)
            inputs.append(asset_path)
            assets = af.load_assets(af._read(asset_path, 8 * 1024 * 1024))
        bundle = render(rom, assets, include_image=args.include_image)
        if args.command != "verify":
            if args.output is None:
                raise ValueError("--output required")
            publish(bundle, args.output, inputs, replace=args.replace_derived)
        print(json.dumps(json.loads(bundle["manifest.json"])["summary"], ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as error:
        parser.exit(2, f"audio_build: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
