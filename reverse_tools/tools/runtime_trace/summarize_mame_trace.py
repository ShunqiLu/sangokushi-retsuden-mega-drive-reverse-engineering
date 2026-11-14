#!/usr/bin/env python3
"""Extract executed 68000 PCs from a MAME debugger trace."""

from __future__ import annotations

import argparse
import bisect
import csv
import json
from pathlib import Path
import re
import sys


TRACE_LINE = re.compile(r"^([0-9A-Fa-f]{6,8}):\s+(.*)$")


def parse_trace(path: Path) -> dict:
    counts: dict[int, int] = {}
    first_seen: dict[int, int] = {}
    examples: dict[int, str] = {}
    trace_instruction_lines = 0

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_number, line in enumerate(handle, 1):
            match = TRACE_LINE.match(line.rstrip("\r\n"))
            if not match:
                continue
            pc = int(match.group(1), 16)
            instruction = match.group(2)
            trace_instruction_lines += 1
            counts[pc] = counts.get(pc, 0) + 1
            first_seen.setdefault(pc, line_number)
            examples.setdefault(pc, instruction)

    ordered = sorted(counts)
    return {
        "trace": path.name,
        "instruction_lines": trace_instruction_lines,
        "unique_pcs": len(ordered),
        "min_pc": f"0x{ordered[0]:06x}" if ordered else None,
        "max_pc": f"0x{ordered[-1]:06x}" if ordered else None,
        "pcs": [
            {
                "pc": f"0x{pc:06x}",
                "logged_occurrences": counts[pc],
                "first_trace_line": first_seen[pc],
                "example": examples[pc],
            }
            for pc in ordered
        ],
        "note": (
            "Logged occurrences count visible trace lines. MAME loop condensation "
            "affects those counts. Each listed PC records an observed execution."
        ),
    }


def write_csv(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "pc",
                "logged_occurrences",
                "first_trace_line",
                "size",
                "bytes",
                "capstone",
                "example",
            ),
        )
        writer.writeheader()
        writer.writerows(report["pcs"])


def _continuous_ranges(addresses: set[int]) -> list[dict[str, int | str]]:
    if not addresses:
        return []
    ordered = sorted(addresses)
    ranges: list[dict[str, int | str]] = []
    start = previous = ordered[0]
    for address in ordered[1:]:
        if address != previous + 1:
            ranges.append(
                {
                    "start": f"0x{start:06x}",
                    "end": f"0x{previous + 1:06x}",
                    "length": previous + 1 - start,
                }
            )
            start = address
        previous = address
    ranges.append(
        {
            "start": f"0x{start:06x}",
            "end": f"0x{previous + 1:06x}",
            "length": previous + 1 - start,
        }
    )
    return ranges


def enrich_with_rom(report: dict, rom_path: Path) -> None:
    try:
        from capstone import CS_ARCH_M68K, CS_MODE_BIG_ENDIAN, CS_MODE_M68K_000, Cs
    except ImportError as error:
        raise RuntimeError(
            "--rom requires Capstone; add the pinned package directory to PYTHONPATH"
        ) from error

    rom = rom_path.read_bytes()
    decoder = Cs(CS_ARCH_M68K, CS_MODE_BIG_ENDIAN | CS_MODE_M68K_000)
    starts = sorted(int(item["pc"], 16) for item in report["pcs"])
    covered: set[int] = set()
    failures: list[str] = []
    overlaps: list[dict[str, str]] = []

    for item in report["pcs"]:
        pc = int(item["pc"], 16)
        if pc >= len(rom):
            failures.append(f"0x{pc:06x}: outside ROM")
            continue
        instructions = list(decoder.disasm(rom[pc : pc + 12], pc, count=1))
        if not instructions or instructions[0].address != pc:
            failures.append(f"0x{pc:06x}: Capstone decode failed")
            continue
        instruction = instructions[0]
        item["size"] = instruction.size
        item["bytes"] = instruction.bytes.hex()
        item["capstone"] = f"{instruction.mnemonic} {instruction.op_str}".rstrip()
        for address in range(pc, pc + instruction.size):
            covered.add(address)
        first_interior = bisect.bisect_right(starts, pc)
        after_instruction = bisect.bisect_left(starts, pc + instruction.size)
        interior_starts = starts[first_interior:after_instruction]
        for other in interior_starts:
            overlaps.append(
                {"instruction": f"0x{pc:06x}", "interior_pc": f"0x{other:06x}"}
            )

    report["rom"] = rom_path.name
    report["decoded_unique_pcs"] = len(report["pcs"]) - len(failures)
    report["runtime_confirmed_instruction_bytes"] = len(covered)
    report["coverage_ranges"] = _continuous_ranges(covered)
    report["decode_failures"] = failures
    report["interior_pc_overlaps"] = overlaps


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    parser.add_argument("--json", type=Path, dest="json_path")
    parser.add_argument("--csv", type=Path, dest="csv_path")
    parser.add_argument(
        "--rom",
        type=Path,
        help="use Capstone to calculate exact instruction-byte coverage",
    )
    args = parser.parse_args()

    try:
        report = parse_trace(args.trace)
        if args.rom:
            enrich_with_rom(report, args.rom)
        if args.json_path:
            args.json_path.parent.mkdir(parents=True, exist_ok=True)
            args.json_path.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        if args.csv_path:
            write_csv(args.csv_path, report)
    except (OSError, RuntimeError) as error:
        print(f"trace summary failed: {error}", file=sys.stderr)
        return 1

    print(
        f"trace={args.trace} instruction_lines={report['instruction_lines']} "
        f"unique_pcs={report['unique_pcs']} range={report['min_pc']}..{report['max_pc']}"
    )
    if args.rom:
        print(
            "runtime-confirmed instruction bytes="
            f"{report['runtime_confirmed_instruction_bytes']} "
            f"decode_failures={len(report['decode_failures'])} "
            f"interior_overlaps={len(report['interior_pc_overlaps'])}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
