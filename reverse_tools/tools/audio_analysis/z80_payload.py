#!/usr/bin/env python3
"""Validated extraction and lossless rebuilding of the game's Z80 payload.

The 68000 copies three ROM ranges into Z80 RAM.  Two source ranges overlap by
0x36 bytes and the final 13-byte copy overwrites part of the second range in
Z80 RAM.  A flattened runtime image therefore needs a 13-byte shadow sidecar
to be a lossless representation of the ROM sources.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


RUNTIME_SIZE = 0x1E00
Z80_RAM_SIZE = 0x2000


@dataclass(frozen=True)
class Transfer:
    name: str
    rom_start: int
    length: int
    z80_destination: int

    @property
    def rom_end(self) -> int:
        return self.rom_start + self.length

    @property
    def z80_end(self) -> int:
        return self.z80_destination + self.length


TRANSFERS = (
    Transfer("primary", 0x0069D2, 0x1000, 0x0000),
    Transfer("secondary", 0x00799C, 0x0E00, 0x1000),
    Transfer("overlay_1c00", 0x0069AA, 0x000D, 0x1C00),
)

COPY_SIGNATURES = (
    (
        "primary_copy",
        0x006966,
        bytes.fromhex("41fa 006a 4e71 43f9 00a0 0000 303c 0fff 12d8 51c8 fffc"),
    ),
    (
        "secondary_copy",
        0x00697C,
        bytes.fromhex("41fa 101e 4e71 303c 0dff 12d8 51c8 fffc"),
    ),
    (
        "overlay_copy",
        0x00698C,
        bytes.fromhex("41fa 001c 43f9 00a0 1c00 700c 12d8 51c8 fffc"),
    ),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_rom(rom: bytes) -> None:
    for name, offset, signature in COPY_SIGNATURES:
        actual = rom[offset : offset + len(signature)]
        if actual != signature:
            raise ValueError(
                f"validated 68000 transfer signature {name} is absent at "
                f"ROM linear 0x{offset:06X}"
            )
    for transfer in TRANSFERS:
        if transfer.rom_end > len(rom):
            raise ValueError(f"{transfer.name} source extends beyond ROM")


def extract_components(rom: bytes) -> dict[str, bytes]:
    validate_rom(rom)
    return {
        transfer.name: rom[transfer.rom_start : transfer.rom_end]
        for transfer in TRANSFERS
    }


def compose_runtime(components: dict[str, bytes]) -> tuple[bytes, bytes]:
    for transfer in TRANSFERS:
        blob = components.get(transfer.name)
        if blob is None:
            raise ValueError(f"missing payload component {transfer.name}")
        if len(blob) != transfer.length:
            raise ValueError(
                f"component {transfer.name} has {len(blob):#x} bytes; "
                f"expected {transfer.length:#x}"
            )
    primary = components["primary"]
    secondary = components["secondary"]
    overlap_length = TRANSFERS[0].rom_end - TRANSFERS[1].rom_start
    if overlap_length <= 0:
        raise AssertionError("expected source overlap is missing")
    if primary[-overlap_length:] != secondary[:overlap_length]:
        raise ValueError(
            "primary/secondary disagree in their shared 0x36-byte ROM source; "
            "a single rebuilt ROM cannot represent both edits"
        )

    runtime = bytearray(RUNTIME_SIZE)
    runtime[0x0000:0x1000] = primary
    runtime[0x1000:0x1E00] = secondary
    shadow = bytes(runtime[0x1C00:0x1C0D])
    runtime[0x1C00:0x1C0D] = components["overlay_1c00"]
    return bytes(runtime), shadow


def components_from_runtime(runtime: bytes, shadow_1c00: bytes) -> dict[str, bytes]:
    if len(runtime) != RUNTIME_SIZE:
        raise ValueError(
            f"flattened runtime has {len(runtime):#x} bytes; expected {RUNTIME_SIZE:#x}"
        )
    if len(shadow_1c00) != 0x0D:
        raise ValueError("secondary 0x1C00 shadow sidecar must contain exactly 13 bytes")
    primary = bytes(runtime[0x0000:0x1000])
    secondary = bytearray(runtime[0x1000:0x1E00])
    secondary[0x0C00:0x0C0D] = shadow_1c00
    overlap_length = 0x36
    if primary[-overlap_length:] != secondary[:overlap_length]:
        raise ValueError(
            "flattened runtime contains inconsistent copies of the shared ROM "
            "source at Z80 0x0FCA and 0x1000"
        )
    return {
        "primary": primary,
        "secondary": bytes(secondary),
        "overlay_1c00": bytes(runtime[0x1C00:0x1C0D]),
    }


def rebuild_rom(base_rom: bytes, components: dict[str, bytes]) -> bytes:
    validate_rom(base_rom)
    # compose_runtime performs all size and shared-source consistency checks.
    compose_runtime(components)
    rebuilt = bytearray(base_rom)
    for transfer in TRANSFERS:
        rebuilt[transfer.rom_start : transfer.rom_end] = components[transfer.name]
    return bytes(rebuilt)


def build_manifest(rom: bytes, components: dict[str, bytes]) -> dict[str, Any]:
    runtime, shadow = compose_runtime(components)
    return {
        "schema_version": 1,
        "address_spaces": {
            "rom": "linear deinterleaved Mega Drive ROM byte offsets",
            "z80": "Z80 RAM logical addresses",
        },
        "source_rom": {"size": len(rom), "sha256": sha256(rom)},
        "copy_signatures": [
            {
                "name": name,
                "rom_offset": offset,
                "bytes": signature.hex(),
                "status": "confirmed",
                "evidence": "exact 68000 copy-loop signature",
            }
            for name, offset, signature in COPY_SIGNATURES
        ],
        "transfers": [
            {
                "name": transfer.name,
                "rom_start": transfer.rom_start,
                "rom_end_exclusive": transfer.rom_end,
                "z80_destination": transfer.z80_destination,
                "z80_end_exclusive": transfer.z80_end,
                "length": transfer.length,
                "sha256": sha256(components[transfer.name]),
                "status": "confirmed",
            }
            for transfer in TRANSFERS
        ],
        "source_overlap": {
            "rom_start": 0x00799C,
            "rom_end_exclusive": 0x0079D2,
            "length": 0x36,
            "z80_copies": [
                {"start": 0x0FCA, "end_exclusive": 0x1000},
                {"start": 0x1000, "end_exclusive": 0x1036},
            ],
            "byte_equal": runtime[0x0FCA:0x1000] == runtime[0x1000:0x1036],
            "status": "confirmed",
        },
        "destination_overlay": {
            "z80_start": 0x1C00,
            "z80_end_exclusive": 0x1C0D,
            "length": 0x0D,
            "shadow_sha256": sha256(shadow),
            "flattened_runtime_requires_shadow_for_lossless_rebuild": True,
            "status": "confirmed",
        },
        "runtime": {
            "size": len(runtime),
            "sha256": sha256(runtime),
            "uninitialised_top_ram": {
                "start": RUNTIME_SIZE,
                "end_exclusive": Z80_RAM_SIZE,
                "length": Z80_RAM_SIZE - RUNTIME_SIZE,
            },
        },
    }


def write_extraction(output: Path, rom: bytes, components: dict[str, bytes]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    runtime, shadow = compose_runtime(components)
    filenames = {
        "primary": "z80_source_primary.bin",
        "secondary": "z80_source_secondary.bin",
        "overlay_1c00": "z80_source_overlay_1c00.bin",
    }
    for name, filename in filenames.items():
        (output / filename).write_bytes(components[name])
    (output / "z80_runtime_expected.bin").write_bytes(runtime)
    (output / "z80_runtime_shadow_1c00.bin").write_bytes(shadow)
    (output / "payload_manifest.json").write_text(
        json.dumps(build_manifest(rom, components), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_component_directory(directory: Path) -> dict[str, bytes]:
    return {
        "primary": (directory / "z80_source_primary.bin").read_bytes(),
        "secondary": (directory / "z80_source_secondary.bin").read_bytes(),
        "overlay_1c00": (directory / "z80_source_overlay_1c00.bin").read_bytes(),
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    unpack = sub.add_parser("unpack", help="extract all three sources and runtime+shadow")
    unpack.add_argument("--rom", type=Path, required=True)
    unpack.add_argument("--output", type=Path, required=True)

    pack = sub.add_parser("pack", help="rebuild from the three source components")
    pack.add_argument("--base-rom", type=Path, required=True)
    pack.add_argument("--payload-dir", type=Path, required=True)
    pack.add_argument("--output", type=Path, required=True)

    pack_runtime = sub.add_parser(
        "pack-runtime", help="rebuild from flattened runtime plus 13-byte shadow"
    )
    pack_runtime.add_argument("--base-rom", type=Path, required=True)
    pack_runtime.add_argument("--runtime", type=Path, required=True)
    pack_runtime.add_argument("--shadow", type=Path, required=True)
    pack_runtime.add_argument("--output", type=Path, required=True)

    verify = sub.add_parser("verify", help="perform both exact round trips in memory")
    verify.add_argument("--rom", type=Path, required=True)

    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.command == "unpack":
        rom = args.rom.read_bytes()
        components = extract_components(rom)
        args.output.mkdir(parents=True)
        write_extraction(args.output, rom, components)
        return 0
    if args.command == "pack":
        base = args.base_rom.read_bytes()
        components = read_component_directory(args.payload_dir)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as output:
            output.write(rebuild_rom(base, components))
        return 0
    if args.command == "pack-runtime":
        base = args.base_rom.read_bytes()
        components = components_from_runtime(
            args.runtime.read_bytes(), args.shadow.read_bytes()
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as output:
            output.write(rebuild_rom(base, components))
        return 0
    if args.command == "verify":
        rom = args.rom.read_bytes()
        components = extract_components(rom)
        runtime, shadow = compose_runtime(components)
        rebuilt_components = rebuild_rom(rom, components)
        rebuilt_runtime = rebuild_rom(rom, components_from_runtime(runtime, shadow))
        if rebuilt_components != rom or rebuilt_runtime != rom:
            raise SystemExit("round-trip mismatch")
        print(
            json.dumps(
                {
                    "status": "exact",
                    "rom_bytes": len(rom),
                    "component_roundtrip": True,
                    "runtime_shadow_roundtrip": True,
                },
                indent=2,
            )
        )
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
