"""Find possible M68000 instructions that reference a requested address.

This intentionally decodes from every even ROM offset.  It is a candidate
finder rather than a proof that every hit belongs to reachable code.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path)
    parser.add_argument("target", type=lambda value: int(value, 0))
    parser.add_argument("--end", type=lambda value: int(value, 0), default=0x40000)
    args = parser.parse_args(argv)
    if args.end < 0:
        parser.error("--end must be nonnegative")
    try:
        from capstone import CS_ARCH_M68K, CS_MODE_BIG_ENDIAN, CS_MODE_M68K_000, Cs
    except ImportError as error:
        parser.error(f"install Capstone 5 or newer: {error}")

    rom = args.rom.read_bytes()
    decoder = Cs(CS_ARCH_M68K, CS_MODE_BIG_ENDIAN | CS_MODE_M68K_000)
    stop = min(len(rom), args.end)
    for offset in range(0, stop - 1, 2):
        decoded = next(decoder.disasm(rom[offset : min(offset + 10, stop)], offset, count=1), None)
        if decoded is None:
            continue
        numbers = [int(item, 16) for item in re.findall(r"\$([0-9a-f]+)", decoded.op_str, re.I)]
        if args.target in numbers:
            print(
                f"{decoded.address:06X}: {decoded.bytes.hex():<16} "
                f"{decoded.mnemonic:<9} {decoded.op_str}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
