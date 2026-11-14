#!/usr/bin/env python3
"""Merge enriched MAME trace summaries while preserving path provenance."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path
import sys


def continuous_ranges(addresses: set[int]) -> list[dict[str, int | str]]:
    if not addresses:
        return []
    result: list[dict[str, int | str]] = []
    ordered = sorted(addresses)
    start = previous = ordered[0]
    for address in ordered[1:]:
        if address != previous + 1:
            result.append(
                {
                    "start": f"0x{start:06x}",
                    "end": f"0x{previous + 1:06x}",
                    "length": previous + 1 - start,
                }
            )
            start = address
        previous = address
    result.append(
        {
            "start": f"0x{start:06x}",
            "end": f"0x{previous + 1:06x}",
            "length": previous + 1 - start,
        }
    )
    return result


def merge(summaries: dict[str, dict]) -> dict:
    pc_records: dict[int, dict] = {}
    scenario_pc_sets: dict[str, set[int]] = {}
    conflicts: list[dict[str, str]] = []

    for label, summary in summaries.items():
        scenario_pc_sets[label] = set()
        for source in summary["pcs"]:
            pc = int(source["pc"], 16)
            scenario_pc_sets[label].add(pc)
            record = pc_records.setdefault(
                pc,
                {
                    "pc": source["pc"],
                    "size": source.get("size"),
                    "bytes": source.get("bytes"),
                    "capstone": source.get("capstone"),
                    "scenarios": [],
                },
            )
            if (
                record["size"] != source.get("size")
                or record["bytes"] != source.get("bytes")
            ):
                conflicts.append(
                    {
                        "pc": source["pc"],
                        "scenario": label,
                        "first_bytes": str(record["bytes"]),
                        "other_bytes": str(source.get("bytes")),
                    }
                )
            record["scenarios"].append(label)

    covered_bytes: set[int] = set()
    for pc, record in pc_records.items():
        size = record["size"]
        if size is None:
            continue
        covered_bytes.update(range(pc, pc + int(size)))

    labels = list(summaries)
    pairwise = []
    for first, second in itertools.combinations(labels, 2):
        first_set = scenario_pc_sets[first]
        second_set = scenario_pc_sets[second]
        pairwise.append(
            {
                "first": first,
                "second": second,
                "intersection_pcs": len(first_set & second_set),
                "first_only_pcs": len(first_set - second_set),
                "second_only_pcs": len(second_set - first_set),
            }
        )

    records = [pc_records[pc] for pc in sorted(pc_records)]
    for record in records:
        record["scenarios"] = sorted(record["scenarios"])

    return {
        "scenarios": {
            label: {
                "unique_pcs": len(scenario_pc_sets[label]),
                "runtime_confirmed_instruction_bytes": summaries[label].get(
                    "runtime_confirmed_instruction_bytes"
                ),
                "source": summaries[label].get("trace"),
            }
            for label in labels
        },
        "union_unique_pcs": len(pc_records),
        "union_runtime_confirmed_instruction_bytes": len(covered_bytes),
        "coverage_ranges": continuous_ranges(covered_bytes),
        "pairwise": pairwise,
        "decode_conflicts": conflicts,
        "pcs": records,
    }


def parse_label_path(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("summary must be LABEL=PATH")
    label, path = value.split("=", 1)
    if not label:
        raise argparse.ArgumentTypeError("summary label is empty")
    return label, Path(path)


def write_csv(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("pc", "size", "bytes", "capstone", "scenarios"),
        )
        writer.writeheader()
        for record in report["pcs"]:
            row = dict(record)
            row["scenarios"] = ";".join(record["scenarios"])
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=parse_label_path, nargs="+")
    parser.add_argument("--json", type=Path, required=True, dest="json_path")
    parser.add_argument("--csv", type=Path, required=True, dest="csv_path")
    args = parser.parse_args()

    summaries: dict[str, dict] = {}
    try:
        for label, path in args.summary:
            if label in summaries:
                raise ValueError(f"duplicate label: {label}")
            summaries[label] = json.loads(path.read_text(encoding="utf-8"))
        report = merge(summaries)
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        write_csv(args.csv_path, report)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"trace merge failed: {error}", file=sys.stderr)
        return 1

    print(
        f"scenarios={len(summaries)} union_pcs={report['union_unique_pcs']} "
        "union_instruction_bytes="
        f"{report['union_runtime_confirmed_instruction_bytes']} "
        f"decode_conflicts={len(report['decode_conflicts'])}"
    )
    for comparison in report["pairwise"]:
        print(
            f"{comparison['first']} vs {comparison['second']}: "
            f"shared={comparison['intersection_pcs']} "
            f"first_only={comparison['first_only_pcs']} "
            f"second_only={comparison['second_only_pcs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

