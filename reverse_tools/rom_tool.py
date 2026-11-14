#!/usr/bin/env python3
"""Convert between SMD and linear Mega Drive images using separate files."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from tools.rom_layout import MEGA_DRIVE_ID, require_g5510_rom


SMD_HEADER_SIZE = 0x200
SMD_BLOCK_SIZE = 0x4000
SMD_HALF_BLOCK = SMD_BLOCK_SIZE // 2

def smd_to_bin(smd: bytes) -> tuple[bytes, bytes]:
    if len(smd) < SMD_HEADER_SIZE or (len(smd) - SMD_HEADER_SIZE) % SMD_BLOCK_SIZE:
        raise ValueError("not a 512-byte-headered, 16 KiB-block SMD image")

    copier_header = smd[:SMD_HEADER_SIZE]
    payload = smd[SMD_HEADER_SIZE:]
    output = bytearray(len(payload))

    for block_start in range(0, len(payload), SMD_BLOCK_SIZE):
        block = payload[block_start : block_start + SMD_BLOCK_SIZE]
        odd = block[:SMD_HALF_BLOCK]
        even = block[SMD_HALF_BLOCK:]
        linear = output[block_start : block_start + SMD_BLOCK_SIZE]
        linear[0::2] = even
        linear[1::2] = odd
        output[block_start : block_start + SMD_BLOCK_SIZE] = linear

    return bytes(output), copier_header


def bin_to_smd(linear: bytes, copier_header: bytes) -> bytes:
    if len(copier_header) != SMD_HEADER_SIZE:
        raise ValueError("copier header must be exactly 512 bytes")
    if len(linear) % SMD_BLOCK_SIZE:
        raise ValueError("linear ROM size must be a multiple of 16 KiB")

    payload = bytearray(len(linear))
    for block_start in range(0, len(linear), SMD_BLOCK_SIZE):
        block = linear[block_start : block_start + SMD_BLOCK_SIZE]
        odd = block[1::2]
        even = block[0::2]
        payload[block_start : block_start + SMD_HALF_BLOCK] = odd
        payload[
            block_start + SMD_HALF_BLOCK : block_start + SMD_BLOCK_SIZE
        ] = even
    return copier_header + bytes(payload)


def genesis_checksum(linear: bytes) -> int:
    """Return the standard 16-bit Mega Drive checksum over ROM[0x200:]."""
    checksum = 0
    body = linear[0x200:]
    if len(body) & 1:
        body += b"\x00"
    for offset in range(0, len(body), 2):
        checksum = (checksum + int.from_bytes(body[offset : offset + 2], "big")) & 0xFFFF
    return checksum


def stored_checksum(linear: bytes) -> int:
    if len(linear) < 0x190:
        raise ValueError("ROM is too small to contain a Mega Drive header")
    return int.from_bytes(linear[0x18E:0x190], "big")


def fix_checksum(linear: bytes) -> bytes:
    output = bytearray(linear)
    output[0x18E:0x190] = genesis_checksum(linear).to_bytes(2, "big")
    return bytes(output)


def write_new(path: Path, data: bytes, *, force: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb" if force else "xb") as handle:
        handle.write(data)


def require_separate_paths(*paths: Path) -> None:
    """Reject path aliases, even when overwriting a separate output is allowed."""
    for index, path in enumerate(paths):
        for other in paths[:index]:
            if path.resolve() == other.resolve() or (
                path.exists() and other.exists() and path.samefile(other)
            ):
                raise ValueError("input, output and copier header must be separate files")


def command_unpack(args: argparse.Namespace) -> None:
    require_separate_paths(args.input, args.output, args.header)
    if not args.force:
        for destination in (args.output, args.header):
            if destination.exists() or destination.is_symlink():
                raise FileExistsError(f"refusing to overwrite existing file: {destination}")
    smd = args.input.read_bytes()
    linear, copier_header = smd_to_bin(smd)
    if not args.allow_unknown:
        require_g5510_rom(linear)
    if linear[0x100:0x110] != MEGA_DRIVE_ID:
        raise ValueError("a linear Mega Drive header at 0x100 is required")
    write_new(args.output, linear, force=args.force)
    write_new(args.header, copier_header, force=args.force)
    print(f"wrote {args.output} ({len(linear)} bytes)")
    print(f"wrote {args.header} ({len(copier_header)} bytes)")
    print(f"stored checksum:   {stored_checksum(linear):04X}")
    print(f"computed checksum: {genesis_checksum(linear):04X}")


def command_pack(args: argparse.Namespace) -> None:
    require_separate_paths(args.input, args.header, args.output)
    linear = args.input.read_bytes()
    copier_header = args.header.read_bytes()
    if args.fix_checksum:
        linear = fix_checksum(linear)
    smd = bin_to_smd(linear, copier_header)
    write_new(args.output, smd, force=args.force)
    print(f"wrote {args.output} ({len(smd)} bytes)")
    print(f"stored checksum:   {stored_checksum(linear):04X}")
    print(f"computed checksum: {genesis_checksum(linear):04X}")


def command_info(args: argparse.Namespace) -> None:
    data = args.input.read_bytes()
    print(f"size: {len(data)}")
    linear = data
    image_format = "linear BIN"
    if linear[0x100:0x110] != MEGA_DRIVE_ID:
        try:
            linear, _header = smd_to_bin(data)
        except ValueError:
            linear = b""
        image_format = "interleaved SMD"
    if linear[0x100:0x110] == MEGA_DRIVE_ID:
        print(f"format: {image_format}")
        print(f"product: {linear[0x180:0x18E].decode('ascii', errors='replace').strip()}")
        print(f"stored_checksum: {stored_checksum(linear):04X}")
        print(f"computed_checksum: {genesis_checksum(linear):04X}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    unpack = subparsers.add_parser("unpack", help="convert SMD to linear BIN")
    unpack.add_argument("input", type=Path)
    unpack.add_argument("output", type=Path)
    unpack.add_argument("header", type=Path, help="where to preserve the copier header")
    unpack.add_argument("--allow-unknown", action="store_true")
    unpack.add_argument("--force", action="store_true")
    unpack.set_defaults(func=command_unpack)

    pack = subparsers.add_parser("pack", help="convert linear BIN back to SMD")
    pack.add_argument("input", type=Path)
    pack.add_argument("header", type=Path)
    pack.add_argument("output", type=Path)
    pack.add_argument("--fix-checksum", action="store_true")
    pack.add_argument("--force", action="store_true")
    pack.set_defaults(func=command_pack)

    info = subparsers.add_parser("info", help="show size, format, product and cartridge checksum")
    info.add_argument("input", type=Path)
    info.set_defaults(func=command_info)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

