"""Print Capstone M68000 disassembly for one or more ROM ranges."""

from __future__ import annotations

import argparse
from pathlib import Path

def parse_range(value: str) -> tuple[int, int]:
    try:
        start_text, end_text = value.split(":", 1)
        start, end = int(start_text, 0), int(end_text, 0)
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected START:END") from error
    if not 0 <= start < end:
        raise argparse.ArgumentTypeError("expected 0 <= START < END")
    return start, end


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path)
    parser.add_argument("ranges", type=parse_range, nargs="+", metavar="START:END")
    args = parser.parse_args(argv)
    try:
        from capstone import CS_ARCH_M68K, CS_MODE_BIG_ENDIAN, CS_MODE_M68K_000, Cs
    except ImportError as error:
        parser.error(f"install Capstone 5 or newer: {error}")
    rom = args.rom.read_bytes()
    decoder = Cs(CS_ARCH_M68K, CS_MODE_BIG_ENDIAN | CS_MODE_M68K_000)
    for start, end in args.ranges:
        if end > len(rom):
            parser.error(f"range {start:#x}:{end:#x} lies past the end of the ROM")
        print(f"\n--- {start:#08x}:{end:#08x}")
        for instruction in decoder.disasm(rom[start:end], start):
            print(
                f"{instruction.address:06X}: {instruction.bytes.hex():<16} "
                f"{instruction.mnemonic:<9} {instruction.op_str}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
