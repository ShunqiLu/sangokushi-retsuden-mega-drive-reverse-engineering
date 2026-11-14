#!/usr/bin/env python3
"""Conservative Motorola 68000 recursive code discovery for a linear ROM.

The analyser deliberately follows only architecturally direct control-flow
targets.  Dynamic register/indexed transfers are retained as unresolved facts;
they are not guessed.  This makes the initial map incomplete by design, but it
also prevents a disassembler-valid data table from silently becoming code.
"""

from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import csv
import hashlib
import heapq
import json
import os
import struct
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def portable_path(path: Path) -> str:
    """Return a stable project-relative evidence label, never an absolute path."""

    try:
        relative = os.path.relpath(path.resolve(), PROJECT_ROOT)
    except ValueError:
        # Different Windows drives cannot be expressed with relpath.  The file
        # content hash remains authoritative; retain only a stable label.
        return f"external/{path.name}"
    return Path(relative).as_posix()


SCHEMA_VERSION = "1.1"
DEFAULT_EXPECTED_SHA256 = (
    reference_value(__name__, 'DEFAULT_EXPECTED_SHA256')
)
MAX_M68K_INSTRUCTION_BYTES = 22
CONFIDENCE_RANK = {
    "heuristic": 0,
    "runtime_reachable": 1,
    "runtime_confirmed": 2,
    "confirmed": 3,
}

VECTOR_NAMES = [
    "initial_supervisor_stack_pointer",
    "reset",
    "bus_error",
    "address_error",
    "illegal_instruction",
    "zero_divide",
    "chk",
    "trapv",
    "privilege_violation",
    "trace",
    "line_1010_emulator",
    "line_1111_emulator",
    "reserved_12",
    "reserved_13",
    "reserved_14",
    "uninitialized_interrupt",
    *[f"reserved_{index}" for index in range(16, 24)],
    "spurious_interrupt",
    *[f"autovector_level_{level}" for level in range(1, 8)],
    *[f"trap_{number}" for number in range(16)],
    *[f"reserved_{index}" for index in range(48, 64)],
]


def _default_capstone_candidates() -> list[Path]:
    script = Path(__file__).resolve()
    workspace = script.parents[3]
    candidates: list[Path] = []
    if os.environ.get("CAPSTONE_PYTHONPATH"):
        candidates.append(Path(os.environ["CAPSTONE_PYTHONPATH"]))
    candidates.extend(
        [
            workspace / "tools" / "python_packages",
            workspace / "reverse_lab" / "_vendor",
        ]
    )
    return candidates


def load_capstone(explicit_path: Path | None = None) -> Any:
    """Import Capstone, optionally bootstrapping a local vendored package."""

    search_paths = [explicit_path] if explicit_path else []
    search_paths.extend(_default_capstone_candidates())
    for candidate in search_paths:
        if candidate and candidate.is_dir():
            candidate_text = str(candidate.resolve())
            if candidate_text not in sys.path:
                sys.path.insert(0, candidate_text)
    try:
        import capstone  # type: ignore

        return capstone
    except ImportError as exc:
        checked = ", ".join(str(path) for path in search_paths if path)
        raise RuntimeError(
            "Capstone is required. Install capstone>=5 or pass "
            f"--capstone-path. Checked: {checked or '(Python environment only)'}"
        ) from exc


def be32(data: bytes, offset: int) -> int:
    return struct.unpack_from(">I", data, offset)[0]


def s8(value: int) -> int:
    return value - 0x100 if value & 0x80 else value


def s16_bytes(value: bytes) -> int:
    return struct.unpack(">h", value)[0]


def hex_address(value: int | None, width: int = 6) -> str:
    if value is None:
        return ""
    if value < 0:
        return f"-{abs(value):0{width}X}"
    return f"{value:0{width}X}"


def parse_int(value: str) -> int:
    return int(value, 0)


def load_runtime_trace_summary(path: Path, rom: bytes) -> dict[str, Any]:
    """Load and byte-validate the merged runtime-PC summary."""

    raw = path.read_bytes()
    document = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(document.get("pcs"), list):
        raise ValueError(f"runtime trace summary has no pcs array: {path}")
    records: dict[int, dict[str, Any]] = {}
    default_scenario = Path(str(document.get("trace", path))).stem
    for index, item in enumerate(document["pcs"]):
        if not isinstance(item, dict):
            raise ValueError(f"runtime pcs[{index}] is not an object")
        pc_value = item.get("pc")
        pc = int(pc_value, 0) if isinstance(pc_value, str) else int(pc_value)
        size = int(item.get("size", 0))
        byte_text = str(item.get("bytes", "")).lower()
        if pc & 1 or pc < 0x200 or pc >= len(rom):
            raise ValueError(f"runtime PC is not a valid even ROM address: 0x{pc:X}")
        if size <= 0 or len(byte_text) != size * 2:
            raise ValueError(
                f"runtime PC 0x{pc:X} has invalid size/bytes: size={size}, bytes={byte_text!r}"
            )
        try:
            trace_bytes = bytes.fromhex(byte_text)
        except ValueError as exc:
            raise ValueError(f"runtime PC 0x{pc:X} has non-hex bytes") from exc
        if rom[pc:pc + size] != trace_bytes:
            raise ValueError(
                f"runtime PC 0x{pc:X} bytes do not match canonical ROM: "
                f"trace={byte_text}, rom={rom[pc:pc + size].hex()}"
            )
        record = {
            "pc": pc,
            "size": size,
            "bytes": byte_text,
            "capstone": item.get("capstone", ""),
            "scenarios": sorted(
                str(value)
                for value in item.get("scenarios", [default_scenario])
            ),
        }
        if pc in records and records[pc] != record:
            raise ValueError(f"conflicting duplicate runtime PC record: 0x{pc:X}")
        records[pc] = record
    reported_count = int(
        document.get("union_unique_pcs", document.get("unique_pcs", len(records)))
    )
    if reported_count != len(records):
        raise ValueError(
            f"runtime PC count mismatch: report={reported_count}, parsed={len(records)}"
        )
    validated_bytes = {
        address
        for record in records.values()
        for address in range(record["pc"], record["pc"] + record["size"])
    }
    return {
        "metadata": {
            "path": portable_path(path),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "reported_union_unique_pcs": reported_count,
            "reported_runtime_instruction_bytes": int(
                document.get(
                    "union_runtime_confirmed_instruction_bytes",
                    document.get("runtime_confirmed_instruction_bytes", len(validated_bytes)),
                )
            ),
            "validated_unique_instruction_bytes": len(validated_bytes),
            "scenario_names": sorted(
                document.get("scenarios", {}).keys()
                or {scenario for record in records.values() for scenario in record["scenarios"]}
            ),
            "validation": "all PC addresses, lengths, and bytes match the canonical ROM",
        },
        "records": [records[pc] for pc in sorted(records)],
    }


def load_runtime_trace_summaries(
    paths: Sequence[Path], rom: bytes
) -> dict[str, Any] | None:
    """Load one or more trace summaries and merge their validated PC sets."""

    if not paths:
        return None
    loaded = [load_runtime_trace_summary(path, rom) for path in paths]
    records: dict[int, dict[str, Any]] = {}
    for summary in loaded:
        for item in summary["records"]:
            pc = int(item["pc"])
            existing = records.get(pc)
            if existing is None:
                records[pc] = dict(item)
                continue
            if (
                existing["size"] != item["size"]
                or existing["bytes"] != item["bytes"]
            ):
                raise ValueError(f"conflicting runtime summaries at PC 0x{pc:X}")
            existing["scenarios"] = sorted(
                set(existing.get("scenarios", [])) | set(item.get("scenarios", []))
            )
            if not existing.get("capstone") and item.get("capstone"):
                existing["capstone"] = item["capstone"]
    validated_bytes = {
        address
        for record in records.values()
        for address in range(record["pc"], record["pc"] + record["size"])
    }
    metadata_items = [summary["metadata"] for summary in loaded]
    return {
        "metadata": {
            "path": " + ".join(item["path"] for item in metadata_items),
            "paths": [item["path"] for item in metadata_items],
            "sha256": hashlib.sha256(
                "\n".join(item["sha256"] for item in metadata_items).encode("ascii")
            ).hexdigest(),
            "input_sha256": [item["sha256"] for item in metadata_items],
            "inputs": [
                {
                    "path": item["path"],
                    "sha256": item["sha256"],
                    "reported_unique_pcs": item["reported_union_unique_pcs"],
                    "reported_instruction_bytes": item[
                        "reported_runtime_instruction_bytes"
                    ],
                    "scenario_names": item["scenario_names"],
                }
                for item in metadata_items
            ],
            "reported_union_unique_pcs": len(records),
            "reported_runtime_instruction_bytes": len(validated_bytes),
            "validated_unique_instruction_bytes": len(validated_bytes),
            "scenario_names": sorted(
                {scenario for record in records.values() for scenario in record["scenarios"]}
            ),
            "validation": (
                "all input PC addresses, lengths, and bytes match the canonical ROM; "
                "duplicate PCs agree exactly"
            ),
        },
        "records": [records[pc] for pc in sorted(records)],
    }


def load_indirect_evidence(path: Path, rom: bytes) -> dict[str, Any]:
    """Load and byte-validate phase-3 indirect-transfer evidence.

    The evidence file is intentionally independent from the recursive mapper.
    It may contain confirmed runtime transitions and probable table members, but
    it must never be able to silently substitute bytes from another ROM build.
    """

    raw = path.read_bytes()
    document = json.loads(raw.decode("utf-8-sig"))
    if document.get("schema_version") != "1.0":
        raise ValueError(
            f"unsupported indirect evidence schema: {document.get('schema_version')!r}"
        )
    actual_rom_sha256 = hashlib.sha256(rom).hexdigest()
    evidence_rom_sha256 = str(document.get("rom", {}).get("sha256", "")).lower()
    if evidence_rom_sha256 != actual_rom_sha256:
        raise ValueError(
            "indirect evidence ROM hash mismatch: "
            f"evidence={evidence_rom_sha256 or '(missing)'}, rom={actual_rom_sha256}"
        )
    if not isinstance(document.get("sites"), list):
        raise ValueError(f"indirect evidence has no sites array: {path}")

    sites: dict[int, dict[str, Any]] = {}
    for index, raw_site in enumerate(document["sites"]):
        if not isinstance(raw_site, dict):
            raise ValueError(f"indirect evidence sites[{index}] is not an object")
        site = dict(raw_site)
        source = int(site["source"])
        source_bytes = bytes.fromhex(str(site.get("source_bytes", "")))
        if (
            source & 1
            or source < 0x200
            or not source_bytes
            or rom[source:source + len(source_bytes)] != source_bytes
        ):
            raise ValueError(
                f"indirect evidence source bytes do not match ROM at 0x{source:X}"
            )
        if source in sites:
            raise ValueError(f"duplicate indirect evidence source: 0x{source:X}")

        static_targets: set[int] = set()
        for entry_index, entry in enumerate(site.get("table", {}).get("entries", [])):
            entry_address = int(entry["entry_address"])
            entry_bytes = bytes.fromhex(str(entry.get("entry_bytes", "")))
            effective_target = int(entry["effective_target"])
            if not entry_bytes or rom[
                entry_address:entry_address + len(entry_bytes)
            ] != entry_bytes:
                raise ValueError(
                    "indirect table entry bytes do not match ROM: "
                    f"source=0x{source:X}, entry={entry_index}"
                )
            if (
                effective_target & 1
                or effective_target < 0x200
                or effective_target >= len(rom)
            ):
                raise ValueError(
                    f"invalid indirect effective target 0x{effective_target:X} "
                    f"at source 0x{source:X}"
                )
            static_targets.add(effective_target)

        observed_targets: set[int] = set()
        for observed in site.get("observed_targets", []):
            target = int(observed["target"])
            if target not in static_targets:
                raise ValueError(
                    f"runtime target 0x{target:X} at source 0x{source:X} "
                    "is not corroborated by the serialized table shape"
                )
            target_bytes = bytes.fromhex(str(observed.get("target_bytes", "")))
            if not target_bytes or rom[target:target + len(target_bytes)] != target_bytes:
                raise ValueError(
                    f"runtime target bytes do not match ROM at 0x{target:X}"
                )
            observed_targets.add(target)

        site["_static_targets"] = sorted(static_targets)
        site["_observed_targets"] = sorted(observed_targets)
        sites[source] = site

    return {
        "metadata": {
            "path": portable_path(path),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "site_count": len(sites),
            "validation": (
                "ROM hash, source bytes, table bytes, effective targets, and "
                "runtime-target bytes validated"
            ),
        },
        "sites": [sites[source] for source in sorted(sites)],
    }


def merge_byte_ranges(statuses: Sequence[str]) -> list[dict[str, Any]]:
    """Run-length encode a complete byte classification map."""

    if not statuses:
        return []
    ranges: list[dict[str, Any]] = []
    start = 0
    current = statuses[0]
    for offset in range(1, len(statuses) + 1):
        next_status = statuses[offset] if offset < len(statuses) else None
        if next_status != current:
            ranges.append(
                {
                    "start": start,
                    "start_hex": hex_address(start),
                    "end_exclusive": offset,
                    "end_exclusive_hex": hex_address(offset),
                    "length": offset - start,
                    "classification": current,
                }
            )
            start = offset
            current = next_status
    return ranges


class M68KCodeMap:
    """A conservative, work-list-driven 68000 code discovery engine."""

    def __init__(
        self,
        rom: bytes,
        *,
        capstone_module: Any,
        analyst_seeds: Iterable[int] = (),
        max_instructions: int | None = None,
        infer_bra_tables: bool = True,
        runtime_trace: dict[str, Any] | None = None,
        indirect_evidence: dict[str, Any] | None = None,
    ) -> None:
        if len(rom) < 0x200:
            raise ValueError("ROM is too small to contain vectors and a Mega Drive header")
        self.rom = rom
        self.capstone = capstone_module
        self.max_instructions = max_instructions or (len(rom) // 2)
        self.infer_bra_tables = infer_bra_tables
        self.runtime_trace = runtime_trace or {"metadata": None, "records": []}
        self.runtime_pcs = {
            int(record["pc"]): dict(record)
            for record in self.runtime_trace.get("records", [])
        }
        self.indirect_evidence = indirect_evidence or {
            "metadata": None,
            "sites": [],
        }
        self.indirect_sites = {
            int(site["source"]): dict(site)
            for site in self.indirect_evidence.get("sites", [])
        }

        mode = capstone_module.CS_MODE_BIG_ENDIAN | capstone_module.CS_MODE_M68K_000
        self.disassembler = capstone_module.Cs(capstone_module.CS_ARCH_M68K, mode)
        self.disassembler.detail = True

        self.instructions: dict[int, dict[str, Any]] = {}
        self.byte_owner: list[int] = [-1] * len(rom)
        self.functions: dict[int, dict[str, Any]] = {}
        self.edges: list[dict[str, Any]] = []
        self.unresolved: list[dict[str, Any]] = []
        self.conflicts: list[dict[str, Any]] = []
        self.decode_failures: list[dict[str, Any]] = []
        self.heuristic_tables: list[dict[str, Any]] = []
        self.discovery_evidence: dict[int, list[dict[str, Any]]] = defaultdict(list)
        self._edge_keys: set[tuple[Any, ...]] = set()
        self._unresolved_keys: set[tuple[Any, ...]] = set()
        self._conflict_keys: set[tuple[Any, ...]] = set()
        self._failure_keys: set[tuple[Any, ...]] = set()
        self._queue: list[int] = []
        self._queued: set[int] = set()
        self._processed_table_sources: set[int] = set()
        self._applied_indirect_sources: set[int] = set()
        self._runtime_seeded = False
        self.static_baseline_instruction_addresses: set[int] = set()
        self.static_baseline_code_bytes: set[int] = set()

        self.vectors = self._parse_vectors()
        self._seed_vectors()
        for seed in analyst_seeds:
            evidence = {
                "type": "analyst_seed",
                "source_address": None,
                "detail": "explicit CLI seed",
                "confidence": "confirmed",
            }
            self._add_function(seed, "confirmed", evidence)
            self._schedule(seed, evidence)

    def _seed_runtime_trace(self) -> None:
        if self._runtime_seeded:
            return
        self._runtime_seeded = True
        for pc, record in sorted(self.runtime_pcs.items()):
            evidence = {
                "type": "runtime_trace_pc",
                "source_address": None,
                "detail": ",".join(record.get("scenarios", [])),
                "confidence": "runtime_confirmed",
                "trace_size": record["size"],
                "trace_bytes": record["bytes"],
            }
            self._schedule(pc, evidence)

    def _parse_vectors(self) -> list[dict[str, Any]]:
        vectors: list[dict[str, Any]] = []
        for index, name in enumerate(VECTOR_NAMES):
            value = be32(self.rom, index * 4)
            if index == 0:
                status = "stack_pointer"
            elif value == 0:
                status = "null"
            elif value & 1:
                status = "invalid_odd"
            elif 0x200 <= value < len(self.rom):
                status = "rom_target"
            elif 0 <= value < len(self.rom):
                status = "reserved_metadata_target"
            else:
                status = "external_target"
            vectors.append(
                {
                    "index": index,
                    "vector_address": index * 4,
                    "vector_address_hex": hex_address(index * 4),
                    "name": name,
                    "value": value,
                    "value_hex": hex_address(value, 8),
                    "status": status,
                }
            )
        return vectors

    def _seed_vectors(self) -> None:
        for vector in self.vectors[1:]:
            if vector["status"] != "rom_target":
                continue
            evidence_type = "reset_vector" if vector["index"] == 1 else "cpu_vector"
            evidence = {
                "type": evidence_type,
                "source_address": vector["vector_address"],
                "detail": f"vector_{vector['index']:02d}_{vector['name']}",
                "confidence": "confirmed",
            }
            target = vector["value"]
            self._add_function(target, "confirmed", evidence)
            self._schedule(target, evidence)

    def _valid_code_target_status(self, target: int) -> str:
        if target & 1:
            return "invalid_odd"
        if target < 0 or target >= len(self.rom):
            return "outside_rom"
        if target < 0x200:
            return "reserved_metadata"
        return "candidate"

    def _schedule(self, address: int, evidence: dict[str, Any]) -> None:
        evidence = dict(evidence)
        evidence.setdefault("confidence", "confirmed")
        self.discovery_evidence[address].append(evidence)
        if self._valid_code_target_status(address) != "candidate":
            self._add_failure(
                address,
                "invalid_code_target",
                evidence.get("source_address"),
                self._valid_code_target_status(address),
            )
            return
        if address in self.instructions:
            record = self.instructions[address]
            record["discovery_evidence"] = sorted(
                self.discovery_evidence[address],
                key=lambda item: (
                    item.get("type", ""),
                    item.get("source_address")
                    if item.get("source_address") is not None
                    else -1,
                    item.get("detail", ""),
                ),
            )
            record["confidence"] = max(
                (
                    item.get("confidence", "confirmed")
                    for item in record["discovery_evidence"]
                ),
                key=lambda value: CONFIDENCE_RANK[value],
            )
            return
        if address not in self._queued:
            heapq.heappush(self._queue, address)
            self._queued.add(address)

    def _add_function(
        self, address: int, classification: str, evidence: dict[str, Any]
    ) -> None:
        if self._valid_code_target_status(address) != "candidate":
            return
        evidence = dict(evidence)
        evidence.setdefault("confidence", "confirmed")
        evidence_confidence = evidence["confidence"]
        if classification == "confirmed" and evidence_confidence != "confirmed":
            classification = (
                "runtime_confirmed"
                if address in self.runtime_pcs
                else "runtime_reachable"
                if evidence_confidence in {"runtime_confirmed", "runtime_reachable"}
                else "heuristic"
            )
        entry = self.functions.setdefault(
            address,
            {
                "address": address,
                "address_hex": hex_address(address),
                "classification": classification,
                "evidence": [],
            },
        )
        if CONFIDENCE_RANK[classification] > CONFIDENCE_RANK[entry["classification"]]:
            entry["classification"] = classification
        evidence_key = (
            evidence.get("type"),
            evidence.get("source_address"),
            evidence.get("detail"),
            evidence.get("confidence"),
        )
        if evidence_key not in {
            (
                item.get("type"),
                item.get("source_address"),
                item.get("detail"),
                item.get("confidence"),
            )
            for item in entry["evidence"]
        }:
            entry["evidence"].append(evidence)

    def _add_edge(
        self,
        source: int,
        target: int | None,
        edge_type: str,
        *,
        direct: bool,
        operand: str,
        base_hint: int | None = None,
        evidence_level: str | None = None,
        evidence_type: str | None = None,
        observation_count: int | None = None,
    ) -> None:
        target_status = "dynamic" if target is None else self._valid_code_target_status(target)
        key = (
            source,
            target,
            edge_type,
            direct,
            operand,
            base_hint,
            evidence_level,
            evidence_type,
        )
        if key in self._edge_keys:
            return
        self._edge_keys.add(key)
        self.edges.append(
            {
                "source": source,
                "source_hex": hex_address(source),
                "target": target,
                "target_hex": hex_address(target),
                "type": edge_type,
                "direct": direct,
                "operand": operand,
                "base_hint": base_hint,
                "base_hint_hex": hex_address(base_hint),
                "evidence_level": evidence_level or "architectural",
                "evidence_type": evidence_type or "direct_control_flow",
                "observation_count": observation_count,
                "status": target_status,
            }
        )

    def _add_unresolved(
        self,
        source: int,
        transfer_type: str,
        operand: str,
        reason: str,
        base_hint: int | None = None,
    ) -> None:
        key = (source, transfer_type, operand, reason, base_hint)
        if key in self._unresolved_keys:
            return
        self._unresolved_keys.add(key)
        self.unresolved.append(
            {
                "source": source,
                "source_hex": hex_address(source),
                "type": transfer_type,
                "operand": operand,
                "reason": reason,
                "base_hint": base_hint,
                "base_hint_hex": hex_address(base_hint),
            }
        )

    def _add_conflict(
        self,
        target: int,
        conflict_type: str,
        existing_instruction: int | None,
        evidence: dict[str, Any] | None,
    ) -> None:
        source = evidence.get("source_address") if evidence else None
        key = (target, conflict_type, existing_instruction, source)
        if key in self._conflict_keys:
            return
        self._conflict_keys.add(key)
        self.conflicts.append(
            {
                "target": target,
                "target_hex": hex_address(target),
                "type": conflict_type,
                "existing_instruction": existing_instruction,
                "existing_instruction_hex": hex_address(existing_instruction),
                "source": source,
                "source_hex": hex_address(source),
                "evidence": evidence or {},
            }
        )

    def _add_failure(
        self,
        address: int,
        failure_type: str,
        source: int | None,
        detail: str,
    ) -> None:
        key = (address, failure_type, source, detail)
        if key in self._failure_keys:
            return
        self._failure_keys.add(key)
        self.decode_failures.append(
            {
                "address": address,
                "address_hex": hex_address(address),
                "type": failure_type,
                "source": source,
                "source_hex": hex_address(source),
                "detail": detail,
            }
        )

    @staticmethod
    def _mnemonic_base(instruction: Any) -> str:
        return instruction.mnemonic.lower().split(".", 1)[0]

    def _branch_target(self, instruction: Any) -> int | None:
        branch_mode = self.capstone.m68k_const.M68K_AM_BRANCH_DISPLACEMENT
        operand = next(
            (
                candidate
                for candidate in instruction.operands
                if int(candidate.address_mode) == branch_mode
            ),
            None,
        )
        if operand is None:
            return None
        displacement = int(operand.br_disp.disp)
        # All 68000 branch displacements are relative to the PC immediately
        # after the opcode word, not after a possible extension word.
        return instruction.address + 2 + displacement

    def _transfer_target(self, instruction: Any) -> tuple[int | None, int | None, str]:
        """Return (direct target, dynamic base hint, resolution reason)."""

        if not instruction.operands:
            return None, None, "missing_operand"
        operand = instruction.operands[0]
        try:
            mode = int(operand.address_mode)
        except (AttributeError, TypeError, ValueError):
            return None, None, "missing_address_mode"

        constants = self.capstone.m68k_const
        raw = bytes(instruction.bytes)
        if mode == constants.M68K_AM_ABSOLUTE_DATA_LONG:
            return int(operand.imm) & 0xFFFFFFFF, None, "absolute_long"
        if mode == constants.M68K_AM_ABSOLUTE_DATA_SHORT and len(raw) >= 4:
            target = s16_bytes(raw[-2:]) & 0xFFFFFFFF
            return target, None, "absolute_short"
        if mode == constants.M68K_AM_PCI_DISP and len(raw) >= 4:
            target = instruction.address + 2 + s16_bytes(raw[2:4])
            return target, None, "pc_relative_displacement"
        if mode == constants.M68K_AM_PCI_INDEX_8_BIT_DISP and len(raw) >= 4:
            base_hint = instruction.address + 2 + s8(raw[3])
            return None, base_hint, "pc_relative_indexed"
        if mode in {
            constants.M68K_AM_PCI_INDEX_BASE_DISP,
            constants.M68K_AM_PC_MEMI_POST_INDEX,
            constants.M68K_AM_PC_MEMI_PRE_INDEX,
        }:
            return None, None, "pc_relative_dynamic"
        return None, None, "register_or_memory_indirect"

    def _decode_one(self, address: int) -> Any | None:
        end = min(len(self.rom), address + MAX_M68K_INSTRUCTION_BYTES)
        return next(
            self.disassembler.disasm(self.rom[address:end], address, count=1), None
        )

    def _accept_instruction(self, instruction: Any) -> bool:
        address = int(instruction.address)
        end = address + int(instruction.size)
        if instruction.size <= 0 or end > len(self.rom):
            return False
        owners = {owner for owner in self.byte_owner[address:end] if owner != -1}
        if owners and owners != {address}:
            evidence = self.discovery_evidence.get(address, [None])[0]
            self._add_conflict(
                address,
                "instruction_overlap",
                min(owners),
                evidence,
            )
            return False
        for byte_address in range(address, end):
            self.byte_owner[byte_address] = address
        return True

    def _record_instruction(self, instruction: Any, flow_type: str) -> None:
        address = int(instruction.address)
        evidence = sorted(
            self.discovery_evidence.get(address, []),
            key=lambda item: (
                item.get("type", ""),
                item.get("source_address")
                if item.get("source_address") is not None
                else -1,
                item.get("detail", ""),
            ),
        )
        confidence = max(
            (item.get("confidence", "confirmed") for item in evidence),
            key=lambda value: CONFIDENCE_RANK[value],
            default="confirmed",
        )
        self.instructions[address] = {
            "address": address,
            "address_hex": hex_address(address),
            "size": int(instruction.size),
            "bytes": bytes(instruction.bytes).hex(),
            "mnemonic": instruction.mnemonic,
            "operand": instruction.op_str,
            "flow_type": flow_type,
            "confidence": confidence,
            "discovery_evidence": evidence,
        }

    def _schedule_edge_target(
        self,
        source: int,
        target: int,
        edge_type: str,
        operand: str,
        *,
        evidence_type: str,
        function_classification: str | None = None,
        confidence: str | None = None,
    ) -> None:
        self._add_edge(source, target, edge_type, direct=True, operand=operand)
        if self._valid_code_target_status(target) == "candidate":
            if confidence is None:
                source_confidence = self.instructions.get(source, {}).get(
                    "confidence", "confirmed"
                )
                confidence = (
                    "runtime_reachable"
                    if source_confidence
                    in {"runtime_confirmed", "runtime_reachable"}
                    else source_confidence
                )
            evidence = {
                "type": evidence_type,
                "source_address": source,
                "detail": operand,
                "confidence": confidence,
            }
            if function_classification:
                self._add_function(target, function_classification, evidence)
            self._schedule(target, evidence)

    def _apply_indirect_evidence(
        self,
        source: int,
        transfer_type: str,
        operand: str,
        base_hint: int | None,
    ) -> None:
        """Attach byte-validated phase-3 targets without claiming completeness."""

        if source in self._applied_indirect_sources:
            return
        site = self.indirect_sites.get(source)
        if site is None:
            return
        self._applied_indirect_sources.add(source)
        if site.get("transfer_type") != transfer_type:
            raise ValueError(
                f"indirect evidence type mismatch at 0x{source:X}: "
                f"map={transfer_type}, evidence={site.get('transfer_type')}"
            )
        if str(site.get("operand")) != operand:
            raise ValueError(
                f"indirect evidence operand mismatch at 0x{source:X}: "
                f"map={operand!r}, evidence={site.get('operand')!r}"
            )

        observed_by_target = {
            int(item["target"]): item for item in site.get("observed_targets", [])
        }
        entries_by_target: dict[int, list[int]] = defaultdict(list)
        for entry in site.get("table", {}).get("entries", []):
            entries_by_target[int(entry["effective_target"])].append(int(entry["index"]))

        for target in sorted(entries_by_target):
            observed = observed_by_target.get(target)
            is_observed = observed is not None
            confidence = "runtime_confirmed" if is_observed else "heuristic"
            evidence_level = "confirmed" if is_observed else "probable"
            evidence_type = (
                "runtime_indirect_transition"
                if is_observed
                else "static_indirect_table_member"
            )
            detail = (
                f"{site.get('mechanism', 'indirect_dispatch')} entries "
                + ",".join(str(value) for value in entries_by_target[target])
            )
            evidence = {
                "type": evidence_type,
                "source_address": source,
                "detail": detail,
                "confidence": confidence,
                "target_set_complete": False,
            }
            edge_type = (
                f"indirect_{transfer_type}_runtime"
                if is_observed
                else f"indirect_{transfer_type}_probable"
            )
            self._add_edge(
                source,
                target,
                edge_type,
                direct=False,
                operand=operand,
                base_hint=base_hint,
                evidence_level=evidence_level,
                evidence_type=evidence_type,
                observation_count=(int(observed["observation_count"]) if observed else None),
            )
            if transfer_type == "call":
                self._add_function(
                    target,
                    "confirmed" if is_observed else "heuristic",
                    evidence,
                )
            elif transfer_type == "jump":
                self._add_function(target, "heuristic", evidence)
            self._schedule(target, evidence)

        for unresolved in self.unresolved:
            if unresolved["source"] != source or unresolved["type"] != transfer_type:
                continue
            unresolved.update(
                {
                    "mechanism": site.get("mechanism", "unproved"),
                    "classification_confidence": site.get(
                        "classification_confidence", "unknown"
                    ),
                    "resolution_status": site.get(
                        "resolution_status", "unknown_target_set"
                    ),
                    "confirmed_target_count": len(observed_by_target),
                    "probable_target_count": len(entries_by_target),
                    "target_set_complete": bool(site.get("target_set_complete", False)),
                    "indirect_evidence_source": self.indirect_evidence.get(
                        "metadata", {}
                    ).get("path"),
                }
            )
            break

    def _handle_instruction(self, instruction: Any) -> None:
        address = int(instruction.address)
        fallthrough = address + int(instruction.size)
        mnemonic = self._mnemonic_base(instruction)
        operand_text = instruction.op_str

        if mnemonic in {"bsr", "jsr"}:
            if mnemonic == "bsr":
                target = self._branch_target(instruction)
                base_hint = None
                reason = "branch_displacement"
            else:
                target, base_hint, reason = self._transfer_target(instruction)
            self._record_instruction(
                instruction, "direct_call" if target is not None else "indirect_call"
            )
            if target is not None:
                self._schedule_edge_target(
                    address,
                    target,
                    "call",
                    operand_text,
                    evidence_type=f"direct_{mnemonic}",
                    function_classification="confirmed",
                )
            else:
                self._add_edge(
                    address,
                    None,
                    "call",
                    direct=False,
                    operand=operand_text,
                    base_hint=base_hint,
                )
                self._add_unresolved(
                    address, "call", operand_text, reason, base_hint=base_hint
                )
                self._apply_indirect_evidence(
                    address, "call", operand_text, base_hint
                )
            self._schedule_edge_target(
                address,
                fallthrough,
                "call_fallthrough",
                "",
                evidence_type="fallthrough_after_call",
            )
            return

        if mnemonic == "jmp":
            target, base_hint, reason = self._transfer_target(instruction)
            self._record_instruction(
                instruction, "direct_jump" if target is not None else "indirect_jump"
            )
            if target is not None:
                self._schedule_edge_target(
                    address,
                    target,
                    "jump",
                    operand_text,
                    evidence_type="direct_jmp_target",
                    function_classification="heuristic",
                )
            else:
                self._add_edge(
                    address,
                    None,
                    "jump",
                    direct=False,
                    operand=operand_text,
                    base_hint=base_hint,
                )
                self._add_unresolved(
                    address, "jump", operand_text, reason, base_hint=base_hint
                )
                self._apply_indirect_evidence(
                    address, "jump", operand_text, base_hint
                )
            return

        if mnemonic == "bra":
            target = self._branch_target(instruction)
            self._record_instruction(instruction, "unconditional_branch")
            if target is None:
                self._add_unresolved(address, "branch", operand_text, "missing_displacement")
            else:
                self._schedule_edge_target(
                    address,
                    target,
                    "branch_taken",
                    operand_text,
                    evidence_type="direct_branch_target",
                )
            return

        # Capstone marks Bcc and DBcc as jumps.  Testing the instruction group
        # is essential: bit-manipulation instructions such as BTST/BCLR/BSET
        # also begin with "b" but have no control-flow target.
        if self.capstone.CS_GRP_JUMP in instruction.groups:
            target = self._branch_target(instruction)
            self._record_instruction(instruction, "conditional_branch")
            if target is None:
                self._add_unresolved(address, "branch", operand_text, "missing_displacement")
            else:
                self._schedule_edge_target(
                    address,
                    target,
                    "branch_taken",
                    operand_text,
                    evidence_type="direct_branch_target",
                )
            self._schedule_edge_target(
                address,
                fallthrough,
                "branch_fallthrough",
                "",
                evidence_type="conditional_fallthrough",
            )
            return

        if mnemonic in {"rts", "rte", "rtr", "stop", "illegal"}:
            self._record_instruction(instruction, "terminator")
            return

        if mnemonic == "trap":
            self._record_instruction(instruction, "software_trap")
            trap_number: int | None = None
            if instruction.operands:
                try:
                    trap_number = int(instruction.operands[0].imm)
                except (AttributeError, TypeError, ValueError):
                    trap_number = None
            if trap_number is not None and 0 <= trap_number <= 15:
                handler = self.vectors[32 + trap_number]["value"]
                self._add_edge(
                    address,
                    handler,
                    "trap_handler",
                    direct=True,
                    operand=operand_text,
                )
            self._schedule_edge_target(
                address,
                fallthrough,
                "exception_return_fallthrough",
                "",
                evidence_type="trap_return_fallthrough",
            )
            return

        self._record_instruction(instruction, "linear")
        self._schedule_edge_target(
            address,
            fallthrough,
            "fallthrough",
            "",
            evidence_type="linear_fallthrough",
        )

    def _drain_queue(self) -> bool:
        """Decode all currently scheduled addresses; return False at safety limit."""

        while self._queue:
            if len(self.instructions) >= self.max_instructions:
                self._add_failure(
                    -1,
                    "analysis_limit",
                    None,
                    f"max_instructions={self.max_instructions}",
                )
                return False
            address = heapq.heappop(self._queue)
            self._queued.discard(address)
            if address in self.instructions:
                continue
            owner = self.byte_owner[address]
            if owner != -1 and owner != address:
                evidence = self.discovery_evidence.get(address, [None])[0]
                self._add_conflict(address, "target_inside_instruction", owner, evidence)
                continue
            instruction = self._decode_one(address)
            if instruction is None:
                evidence = self.discovery_evidence.get(address, [{}])[0]
                self._add_failure(
                    address,
                    "decode_failed",
                    evidence.get("source_address"),
                    "Capstone returned no 68000 instruction",
                )
                continue
            if not self._accept_instruction(instruction):
                continue
            self._handle_instruction(instruction)
        return True

    def _bra_table_run(self, base_hint: int, first_offset: int) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        for slot_index in range(256):
            slot = base_hint + first_offset + slot_index * 4
            if self._valid_code_target_status(slot) != "candidate":
                break
            instruction = self._decode_one(slot)
            if instruction is None:
                break
            raw = bytes(instruction.bytes)
            # A four-byte BRA.W is an executable trampoline with the same width
            # as the index mask/stride used by this ROM's dispatchers.
            if (
                self._mnemonic_base(instruction) != "bra"
                or int(instruction.size) != 4
                or raw[:2] != b"\x60\x00"
            ):
                break
            target = self._branch_target(instruction)
            if target is None or self._valid_code_target_status(target) != "candidate":
                break
            entries.append(
                {
                    "index": slot_index,
                    "slot": slot,
                    "slot_hex": hex_address(slot),
                    "target": target,
                    "target_hex": hex_address(target),
                    "bytes": raw.hex(),
                }
            )
        return entries

    def _infer_new_bra_tables(self) -> bool:
        """Promote only strong, fixed-stride BRA.W table shapes as heuristics."""

        added = False
        for transfer in list(self.unresolved):
            source = transfer["source"]
            if source in self._processed_table_sources:
                continue
            self._processed_table_sources.add(source)
            if (
                transfer["reason"] != "pc_relative_indexed"
                or transfer["base_hint"] is None
            ):
                continue
            base_hint = int(transfer["base_hint"])
            candidates = [
                (self._bra_table_run(base_hint, offset), offset)
                for offset in range(0, 18, 2)
            ]
            entries, first_offset = max(
                candidates, key=lambda item: (len(item[0]), -item[1])
            )
            # Four consecutive aligned BRA.W trampolines are required.  A
            # shorter sequence remains unresolved and is never promoted.
            if len(entries) < 4:
                continue
            table = {
                "source": source,
                "source_hex": hex_address(source),
                "transfer_type": transfer["type"],
                "operand": transfer["operand"],
                "base_hint": base_hint,
                "base_hint_hex": hex_address(base_hint),
                "first_slot_offset": first_offset,
                "first_slot": entries[0]["slot"],
                "first_slot_hex": entries[0]["slot_hex"],
                "stride": 4,
                "entry_count": len(entries),
                "classification": "probable_bra_w_dispatch_table",
                "promotion": "heuristic_only",
                "entries": entries,
            }
            self.heuristic_tables.append(table)
            for entry in entries:
                slot = entry["slot"]
                target = entry["target"]
                slot_evidence = {
                    "type": "pc_indexed_dispatch_slot",
                    "source_address": source,
                    "detail": f"{transfer['operand']} slot {entry['index']}",
                    "confidence": "heuristic",
                }
                target_evidence = {
                    "type": "dispatch_bra_target",
                    "source_address": slot,
                    "detail": f"PC-indexed table at {base_hint:06X}",
                    "confidence": "heuristic",
                }
                self._add_edge(
                    source,
                    slot,
                    "heuristic_dispatch_slot",
                    direct=False,
                    operand=transfer["operand"],
                    base_hint=base_hint,
                )
                self._add_function(slot, "heuristic", slot_evidence)
                self._add_function(target, "heuristic", target_evidence)
                self._schedule(slot, slot_evidence)
                added = True
        return added

    def analyse(self) -> None:
        # Phase A is preserved as an exact static baseline before runtime PCs
        # are allowed to add independent evidence roots.
        while True:
            if not self._drain_queue():
                break
            if not self.infer_bra_tables or not self._infer_new_bra_tables():
                break

        self.static_baseline_instruction_addresses = set(self.instructions)
        self.static_baseline_code_bytes = {
            address for address, owner in enumerate(self.byte_owner) if owner != -1
        }

        # Phase B seeds every byte-validated executed PC. Static descendants
        # that were not themselves observed receive runtime_reachable rather
        # than runtime_confirmed confidence.
        if self.runtime_pcs:
            self._seed_runtime_trace()
            while True:
                if not self._drain_queue():
                    break
                if not self.infer_bra_tables or not self._infer_new_bra_tables():
                    break

        self._finalise()

    def _finalise(self) -> None:
        for edge in self.edges:
            target = edge["target"]
            if target is None:
                site = self.indirect_sites.get(edge["source"])
                if site and site.get("observed_targets"):
                    edge["status"] = "dynamic_partially_runtime_resolved"
                elif site:
                    edge["status"] = "dynamic_probable_table_only"
                else:
                    edge["status"] = "dynamic_unresolved"
            elif target in self.instructions:
                edge["status"] = "resolved_code"
            elif 0 <= target < len(self.rom) and self.byte_owner[target] != -1:
                edge["status"] = "conflict_inside_instruction"
            else:
                base_status = self._valid_code_target_status(target)
                edge["status"] = (
                    "unresolved_candidate" if base_status == "candidate" else base_status
                )

        for address, function in self.functions.items():
            evidence = sorted(
                function["evidence"],
                key=lambda item: (
                    item.get("type", ""),
                    item.get("source_address")
                    if item.get("source_address") is not None
                    else -1,
                    item.get("detail", ""),
                ),
            )
            function["evidence"] = evidence
            evidence_types = {item["type"] for item in evidence}
            if "reset_vector" in evidence_types:
                name = "reset"
            elif "cpu_vector" in evidence_types:
                vector_count = sum(item["type"] == "cpu_vector" for item in evidence)
                name = (
                    f"vector_handler_shared_{address:06X}"
                    if vector_count > 1
                    else f"vector_handler_{address:06X}"
                )
            elif function["classification"] == "confirmed":
                name = f"sub_{address:06X}"
            elif function["classification"] == "runtime_confirmed":
                name = f"runtime_sub_{address:06X}"
            elif function["classification"] == "runtime_reachable":
                name = f"runtime_reachable_sub_{address:06X}"
            elif "pc_indexed_dispatch_slot" in evidence_types:
                name = f"dispatch_slot_{address:06X}"
            elif "dispatch_bra_target" in evidence_types:
                name = f"dispatch_candidate_{address:06X}"
            else:
                name = f"tail_candidate_{address:06X}"
            function["name"] = name
            function["decoded"] = address in self.instructions

        self.edges.sort(key=lambda item: (item["source"], item["type"], item["target"] or -1))
        self.unresolved.sort(key=lambda item: (item["source"], item["type"]))
        self.conflicts.sort(key=lambda item: (item["target"], item["type"]))
        self.decode_failures.sort(key=lambda item: (item["address"], item["type"]))
        self.heuristic_tables.sort(key=lambda item: item["source"])

    def byte_ranges(self) -> list[dict[str, Any]]:
        statuses: list[str] = []
        for address, owner in enumerate(self.byte_owner):
            if address < 0x100:
                statuses.append("metadata_vector_table")
            elif address < 0x200:
                statuses.append("metadata_mega_drive_header")
            elif owner != -1:
                confidence = self.instructions[owner]["confidence"]
                statuses.append(
                    {
                        "confirmed": "confirmed_reachable_code",
                        "runtime_confirmed": "runtime_confirmed_code",
                        "runtime_reachable": "runtime_reachable_code",
                        "heuristic": "heuristic_reachable_code",
                    }[confidence]
                )
            else:
                statuses.append("unknown")
        return merge_byte_ranges(statuses)

    def coverage(self) -> dict[str, Any]:
        code_bytes = sum(owner != -1 for owner in self.byte_owner)
        confidence_bytes = Counter(
            self.instructions[owner]["confidence"]
            for owner in self.byte_owner
            if owner != -1
        )
        trace_decoded_pcs = sum(pc in self.instructions for pc in self.runtime_pcs)
        trace_static_overlap_pcs = sum(
            pc in self.static_baseline_instruction_addresses for pc in self.runtime_pcs
        )
        trace_bytes = {
            address
            for record in self.runtime_pcs.values()
            for address in range(record["pc"], record["pc"] + record["size"])
        }
        metadata_bytes = min(len(self.rom), 0x200)
        analysable_bytes = max(0, len(self.rom) - metadata_bytes)
        function_counts = Counter(
            entry["classification"] for entry in self.functions.values()
        )
        edge_counts = Counter(edge["type"] for edge in self.edges)
        highest_end = max(
            (
                instruction["address"] + instruction["size"]
                for instruction in self.instructions.values()
            ),
            default=0,
        )
        indirect_sites = [
            site
            for source, site in sorted(self.indirect_sites.items())
            if source in self.instructions
        ]
        indirect_runtime_edges = sum(
            len(site.get("observed_targets", [])) for site in indirect_sites
        )
        indirect_probable_edges = sum(
            len(
                {
                    int(entry["effective_target"])
                    for entry in site.get("table", {}).get("entries", [])
                }
            )
            for site in indirect_sites
        )
        return {
            "instruction_count": len(self.instructions),
            "reachable_code_bytes": code_bytes,
            "confirmed_code_bytes": confidence_bytes.get("confirmed", 0),
            "runtime_confirmed_code_bytes": confidence_bytes.get(
                "runtime_confirmed", 0
            ),
            "runtime_reachable_code_bytes": confidence_bytes.get(
                "runtime_reachable", 0
            ),
            "heuristic_code_bytes": confidence_bytes.get("heuristic", 0),
            "static_baseline_instruction_count": len(
                self.static_baseline_instruction_addresses
            ),
            "static_baseline_code_bytes": len(self.static_baseline_code_bytes),
            "runtime_trace_pc_count": len(self.runtime_pcs),
            "runtime_trace_pc_decoded_count": trace_decoded_pcs,
            "runtime_trace_pc_static_overlap_count": trace_static_overlap_pcs,
            "runtime_trace_pc_added_count": len(self.runtime_pcs)
            - trace_static_overlap_pcs,
            "runtime_trace_unique_instruction_bytes": len(trace_bytes),
            "rom_bytes": len(self.rom),
            "rom_coverage_percent": round(code_bytes * 100.0 / len(self.rom), 6),
            "metadata_bytes": metadata_bytes,
            "post_header_bytes": analysable_bytes,
            "post_header_coverage_percent": round(
                code_bytes * 100.0 / analysable_bytes, 6
            )
            if analysable_bytes
            else 0.0,
            "unknown_bytes": len(self.rom) - metadata_bytes - code_bytes,
            "highest_reachable_code_end_exclusive": highest_end,
            "highest_reachable_code_end_exclusive_hex": hex_address(highest_end),
            "function_entries": dict(sorted(function_counts.items())),
            "edges": dict(sorted(edge_counts.items())),
            "unresolved_transfer_count": len(self.unresolved),
            "indirect_evidence_site_count": len(indirect_sites),
            "indirect_runtime_observed_site_count": sum(
                bool(site.get("observed_targets")) for site in indirect_sites
            ),
            "indirect_no_confirmed_target_site_count": sum(
                not site.get("observed_targets") for site in indirect_sites
            ),
            "indirect_runtime_confirmed_edge_count": indirect_runtime_edges,
            "indirect_probable_unique_target_count": indirect_probable_edges,
            "indirect_fully_resolved_site_count": sum(
                bool(site.get("target_set_complete")) for site in indirect_sites
            ),
            "indirect_target_domain_unknown_site_count": sum(
                not site.get("target_set_complete", False) for site in indirect_sites
            ),
            "probable_bra_table_count": len(self.heuristic_tables),
            "probable_bra_table_entry_count": sum(
                table["entry_count"] for table in self.heuristic_tables
            ),
            "conflict_count": len(self.conflicts),
            "decode_failure_count": len(self.decode_failures),
        }

    def validation(self, ranges: Sequence[dict[str, Any]]) -> dict[str, Any]:
        checks: list[dict[str, Any]] = []

        def add(name: str, passed: bool, detail: str) -> None:
            checks.append({"name": name, "passed": passed, "detail": detail})

        instruction_bytes_match = all(
            self.rom[address:address + instruction["size"]].hex()
            == instruction["bytes"]
            for address, instruction in self.instructions.items()
        )
        add(
            "instruction_bytes_match_rom",
            instruction_bytes_match,
            f"checked {len(self.instructions)} decoded instructions",
        )
        even_addresses = all(address % 2 == 0 for address in self.instructions)
        add(
            "all_instruction_addresses_even",
            even_addresses,
            "68000 instruction fetch addresses must be even",
        )
        outside_metadata = all(address >= 0x200 for address in self.instructions)
        add(
            "metadata_not_decoded_as_code",
            outside_metadata,
            "vector table and Mega Drive header are reserved",
        )
        owners_valid = all(
            owner == -1
            or (
                owner in self.instructions
                and owner <= byte_address
                < owner + self.instructions[owner]["size"]
            )
            for byte_address, owner in enumerate(self.byte_owner)
        )
        add(
            "byte_ownership_consistent",
            owners_valid,
            "every claimed byte belongs to exactly one decoded instruction",
        )
        ranges_contiguous = bool(ranges) and ranges[0]["start"] == 0
        expected_start = 0
        for item in ranges:
            if item["start"] != expected_start or item["end_exclusive"] < item["start"]:
                ranges_contiguous = False
                break
            expected_start = item["end_exclusive"]
        ranges_contiguous = ranges_contiguous and expected_start == len(self.rom)
        add(
            "ranges_cover_rom_exactly_once",
            ranges_contiguous,
            f"range map ends at 0x{expected_start:X}; ROM ends at 0x{len(self.rom):X}",
        )
        coverage_consistent = (
            sum(item["length"] for item in ranges) == len(self.rom)
            and sum(owner != -1 for owner in self.byte_owner)
            == self.coverage()["reachable_code_bytes"]
        )
        add(
            "coverage_counts_consistent",
            coverage_consistent,
            "range lengths, byte ownership, and coverage summary agree",
        )
        return {
            "all_passed": all(item["passed"] for item in checks),
            "check_count": len(checks),
            "checks": checks,
        }

    def result(self, rom_path: Path) -> dict[str, Any]:
        sha256 = hashlib.sha256(self.rom).hexdigest()
        sha1 = hashlib.sha1(self.rom).hexdigest()
        md5 = hashlib.md5(self.rom).hexdigest()
        ranges = self.byte_ranges()
        validation = self.validation(ranges)
        return {
            "schema_version": SCHEMA_VERSION,
            "rom": {
                "path": portable_path(rom_path),
                "size": len(self.rom),
                "sha256": sha256,
                "sha1": sha1,
                "md5": md5,
                "stored_mega_drive_checksum": self.rom[0x18E:0x190].hex(),
            },
            "architecture": {
                "cpu": "Motorola 68000",
                "endianness": "big",
                "rom_base": 0,
                "linear_file_offset_equals_cpu_rom_address": True,
            },
            "analysis_policy": {
                "claim_level": "confirmed and heuristic reachable code are separated",
                "recursive_seeds": [
                    "reset vector",
                    "valid CPU exception/interrupt vectors",
                    "explicit analyst seeds",
                    "byte-validated executed PCs from an optional runtime trace summary",
                    "byte-validated phase-3 indirect targets with independent confidence",
                ],
                "followed": [
                    "direct BSR/JSR calls",
                    "direct JMP",
                    "BRA and conditional branch targets",
                    "architectural fallthrough",
                    "probable fixed-stride BRA.W dispatch tables as heuristic-only roots",
                    "runtime-observed indirect targets as runtime-confirmed roots",
                    "probable indirect table members as heuristic-only roots",
                ],
                "not_promoted": [
                    "register-indirect calls/jumps",
                    "PC-indexed calls/jumps without at least four consecutive aligned BRA.W trampolines",
                    "unreferenced disassembler-valid byte sequences",
                ],
                "function_entry_confidence": {
                    "confirmed": "CPU vector or direct BSR/JSR destination reached without an inferred dispatch edge",
                    "runtime_confirmed": "direct-call destination independently present in the executed-PC set",
                    "runtime_reachable": "direct-call destination statically reached from runtime-confirmed code but not itself observed",
                    "heuristic": "direct JMP boundary candidate or any entry whose only path descends from an inferred dispatch table",
                },
            },
            "coverage": self.coverage(),
            "validation": validation,
            "runtime_trace_summary": self.runtime_trace,
            "indirect_evidence_summary": {
                "metadata": self.indirect_evidence.get("metadata"),
                "site_count": len(self.indirect_sites),
                "applied_site_count": len(self._applied_indirect_sources),
                "policy": (
                    "observed targets are confirmed edges; static table members are "
                    "probable roots; every target domain remains incomplete unless "
                    "an independent index-range proof says otherwise"
                ),
            },
            "vectors": self.vectors,
            "function_entries": sorted(self.functions.values(), key=lambda item: item["address"]),
            "instructions": [self.instructions[key] for key in sorted(self.instructions)],
            "edges": self.edges,
            "heuristic_dispatch_tables": self.heuristic_tables,
            "unresolved_transfers": self.unresolved,
            "conflicts": self.conflicts,
            "decode_failures": self.decode_failures,
            "ranges": ranges,
        }


def write_csv(path: Path, fields: Sequence[str], rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            normalised = {}
            for field in fields:
                value = row.get(field, "")
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False, sort_keys=True)
                normalised[field] = value
            writer.writerow(normalised)


def write_text_lf(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


def markdown_report(result: dict[str, Any]) -> str:
    coverage = result["coverage"]
    vectors = result["vectors"]
    functions = result["function_entries"]
    unresolved = result["unresolved_transfers"]
    heuristic_tables = result["heuristic_dispatch_tables"]
    conflicts = result["conflicts"]
    failures = result["decode_failures"]
    validation = result["validation"]
    runtime_summary = result["runtime_trace_summary"]
    unique_handlers: dict[int, list[dict[str, Any]]] = defaultdict(list)
    instruction_confidence = {
        instruction["address"]: instruction["confidence"]
        for instruction in result["instructions"]
    }
    for vector in vectors[1:]:
        if vector["status"] == "rom_target":
            unique_handlers[vector["value"]].append(vector)

    edge_counts = Counter(edge["type"] for edge in result["edges"])
    direct_call_edges = sum(
        1 for edge in result["edges"] if edge["type"] == "call" and edge["direct"]
    )
    direct_jump_edges = sum(
        1 for edge in result["edges"] if edge["type"] == "jump" and edge["direct"]
    )
    branch_edges = sum(
        1 for edge in result["edges"] if edge["type"] == "branch_taken"
    )
    confirmed_source_edges = sum(
        1
        for edge in result["edges"]
        if instruction_confidence.get(edge["source"]) == "confirmed"
    )
    runtime_confirmed_source_edges = sum(
        1
        for edge in result["edges"]
        if instruction_confidence.get(edge["source"]) == "runtime_confirmed"
    )
    runtime_reachable_source_edges = sum(
        1
        for edge in result["edges"]
        if instruction_confidence.get(edge["source"]) == "runtime_reachable"
    )
    heuristic_source_edges = sum(
        1
        for edge in result["edges"]
        if instruction_confidence.get(edge["source"]) == "heuristic"
    )

    lines = [
        "# Motorola 68000 code-discovery coverage report",
        "",
        "> This file is generated by `tools/code_analysis/m68k_code_map.py`. Do not hand-edit it.",
        "",
        "## Identity and scope",
        "",
        f"- **[confirmed]** Input: `{result['rom']['path']}`",
        f"- **[confirmed]** Size: `{result['rom']['size']}` bytes (`0x{result['rom']['size']:X}`)",
        f"- **[confirmed]** SHA-256: `{result['rom']['sha256']}`",
        f"- **[confirmed]** Stored Mega Drive checksum: `0x{result['rom']['stored_mega_drive_checksum'].upper()}`",
        "- **[confirmed]** Address convention: linear BIN offset equals 68000 cartridge ROM address.",
        "- **[confirmed]** `0x000000–0x0000FF` is the CPU vector table and `0x000100–0x0001FF` is the Mega Drive header; neither was decoded as code.",
        f"- **[confirmed]** Runtime trace import: {coverage['runtime_trace_pc_count']:,} byte-validated executed PCs from `{runtime_summary['metadata']['path'] if runtime_summary.get('metadata') else '(none)'}`.",
        "",
        "## Conservative discovery policy",
        "",
        "**[confirmed]** Recursive traversal starts only at valid ROM targets in the reset/CPU vector table and any explicit analyst seeds. It follows direct `BSR`, `JSR`, `JMP`, `BRA`, conditional branches, and architectural fallthrough.",
        "",
        "**[unknown]** Register-indirect and PC-indexed transfers are emitted as unresolved records. A PC-indexed site is additionally promoted as **heuristic only** when its base contains at least four consecutive, aligned, in-ROM `BRA.W` trampolines. The table and every descendant retain heuristic confidence; no isolated disassembler-valid sequence is promoted.",
        "",
        "**[confirmed]** Imported executed PCs carry a separate `runtime_confirmed` evidence class. Static successors not explicitly present in the trace carry `runtime_reachable`; neither class is collapsed into `heuristic`.",
        "",
        "## Vector table",
        "",
        f"- **[confirmed]** Initial supervisor SP: `0x{vectors[0]['value_hex']}`.",
        f"- **[confirmed]** Reset PC: `0x{vectors[1]['value_hex']}`.",
        f"- **[confirmed]** Valid ROM vector targets collapse to {len(unique_handlers)} unique handlers.",
        "",
        "| Handler | Vector indices and names |",
        "|---:|---|",
    ]
    for address, items in sorted(unique_handlers.items()):
        description = ", ".join(
            f"{item['index']}:{item['name']}" for item in items
        )
        lines.append(f"| `0x{address:06X}` | {description} |")

    lines.extend(
        [
            "",
            "## Coverage",
            "",
            "| Metric | Result | Meaning |",
            "|---|---:|---|",
            f"| Reachable instructions | {coverage['instruction_count']:,} | Successfully decoded from conservative roots |",
            f"| Reachable code bytes | {coverage['reachable_code_bytes']:,} | Union of decoded instruction bytes |",
            f"| Confirmed code bytes | {coverage['confirmed_code_bytes']:,} | Vector/direct-flow paths without heuristic dispatch |",
            f"| Runtime-confirmed code bytes | {coverage['runtime_confirmed_code_bytes']:,} | Instructions directly present in executed-PC traces, excluding stronger static-confirmed overlap |",
            f"| Runtime-reachable code bytes | {coverage['runtime_reachable_code_bytes']:,} | Static descendants of trace PCs not themselves observed |",
            f"| Heuristic code bytes | {coverage['heuristic_code_bytes']:,} | Descendants of probable BRA.W dispatch tables |",
            f"| Static baseline | {coverage['static_baseline_instruction_count']:,} instructions / {coverage['static_baseline_code_bytes']:,} bytes | Captured before runtime seeds are imported |",
            f"| Runtime PC import | {coverage['runtime_trace_pc_decoded_count']:,}/{coverage['runtime_trace_pc_count']:,} decoded | All trace records are byte-validated against ROM |",
            f"| Runtime PCs already in static map | {coverage['runtime_trace_pc_static_overlap_count']:,} | Static/trace intersection |",
            f"| Runtime PCs added to static map | {coverage['runtime_trace_pc_added_count']:,} | Independent executed-PC roots |",
            f"| Whole-ROM coverage | {coverage['rom_coverage_percent']:.6f}% | Code bytes / all 1 MiB ROM bytes |",
            f"| Post-header coverage | {coverage['post_header_coverage_percent']:.6f}% | Code bytes / bytes at `0x200+` |",
            f"| Unknown post-header bytes | {coverage['unknown_bytes']:,} | May contain data, assets, tables, dead code, or code behind unresolved dispatch |",
            f"| Highest reachable code end | `0x{coverage['highest_reachable_code_end_exclusive']:06X}` | Not evidence that all lower bytes are code |",
            f"| Confirmed function entries | {coverage['function_entries'].get('confirmed', 0):,} | Vector/direct-call destinations |",
            f"| Runtime-confirmed function entries | {coverage['function_entries'].get('runtime_confirmed', 0):,} | Direct-call destinations also present in trace |",
            f"| Runtime-reachable function entries | {coverage['function_entries'].get('runtime_reachable', 0):,} | Calls discovered from runtime-rooted static traversal |",
            f"| Heuristic function entries | {coverage['function_entries'].get('heuristic', 0):,} | Direct-JMP or inferred dispatch destinations; boundary not proven |",
            f"| Probable BRA.W tables | {coverage['probable_bra_table_count']:,} ({coverage['probable_bra_table_entry_count']:,} entries) | Shape-validated, still heuristic |",
            f"| Unresolved indirect transfers | {coverage['unresolved_transfer_count']:,} | Preserved for later jump-table/register analysis |",
            f"| Decode/target conflicts | {coverage['conflict_count']:,} | Never hidden or overwritten |",
            f"| Decode failures | {coverage['decode_failure_count']:,} | Includes invalid targets and undecodable reachable bytes |",
            f"| Internal validation | {'PASS' if validation['all_passed'] else 'FAIL'} ({validation['check_count']} checks) | Bytes, alignment, ownership, ranges, and totals |",
            "",
            "## Direct control-flow inventory",
            "",
            f"- **[confirmed]** Direct call edge records (`BSR`/`JSR`): {direct_call_edges:,}.",
            f"- **[confirmed]** Direct `JMP` edge records: {direct_jump_edges:,}.",
            f"- **[confirmed]** Direct taken-branch edge records: {branch_edges:,}.",
            f"- **[confirmed]** Edges whose source instruction is confirmed: {confirmed_source_edges:,}.",
            f"- **[confirmed]** Edges whose source instruction is runtime-confirmed: {runtime_confirmed_source_edges:,}.",
            f"- **[probable]** Edges whose source instruction is runtime-reachable: {runtime_reachable_source_edges:,}.",
            f"- **[probable]** Edges whose source instruction is heuristic: {heuristic_source_edges:,}.",
            f"- **[confirmed]** Total serialized edge records: {sum(edge_counts.values()):,}.",
            "",
            "## Function-entry evidence",
            "",
            "A `confirmed` entry proves a vector/direct-call path containing no inferred dispatch edge. `runtime_confirmed` is independently observed as an executed PC; `runtime_reachable` descends statically from such a PC. None of these labels alone proves a C-like signature, unique ownership, or source-level boundary. A `heuristic` entry is a direct-`JMP` boundary candidate or a destination descended only from a probable PC-indexed dispatch table.",
            "",
            "| Address | Generated name | Class | Evidence count | Decoded |",
            "|---:|---|---|---:|---|",
        ]
    )
    for function in functions[:250]:
        lines.append(
            f"| `0x{function['address']:06X}` | `{function['name']}` | {function['classification']} | {len(function['evidence'])} | {'yes' if function['decoded'] else 'no'} |"
        )
    if len(functions) > 250:
        lines.append(
            f"| … | {len(functions) - 250:,} additional entries | see `function_entries.csv` |  |  |"
        )

    lines.extend(["", "## Probable PC-indexed dispatch tables", ""])
    if heuristic_tables:
        lines.extend(
            [
                "| Call site | Base hint | First slot | Stride | BRA.W entries | Promotion |",
                "|---:|---:|---:|---:|---:|---|",
            ]
        )
        for table in heuristic_tables:
            lines.append(
                f"| `0x{table['source']:06X}` | `0x{table['base_hint']:06X}` | `0x{table['first_slot']:06X}` | {table['stride']} | {table['entry_count']} | heuristic only |"
            )
        lines.append("")
        lines.append(
            "**[probable]** Each row is backed by at least four consecutive `BRA.W` slots of identical four-byte width with even in-ROM targets. The analysis does not claim that every slot is reachable at runtime; an index range proof or trace is still required."
        )
    else:
        lines.append("- **[unknown]** No PC-indexed site met the conservative BRA.W-table threshold.")

    lines.extend(
        [
            "",
            "## Unresolved transfers",
            "",
        ]
    )
    if unresolved:
        lines.extend(
            [
                "| Source | Type | Operand | Base hint | Reason |",
                "|---:|---|---|---:|---|",
            ]
        )
        for item in unresolved[:100]:
            base_hint = (
                f"`0x{item['base_hint']:06X}`" if item["base_hint"] is not None else ""
            )
            lines.append(
                f"| `0x{item['source']:06X}` | {item['type']} | `{item['operand']}` | {base_hint} | {item['reason']} |"
            )
        if len(unresolved) > 100:
            lines.append(
                f"| … | {len(unresolved) - 100:,} additional records | see `unresolved_transfers.csv` |  |  |"
            )
    else:
        lines.append("- **[confirmed]** None in the currently reachable code set.")

    lines.extend(["", "## Conflicts and failures", ""])
    if conflicts:
        lines.append(
            f"- **[candidate]** {len(conflicts):,} overlapping/inside-instruction targets were retained in `conflicts.csv`; no prior instruction was overwritten."
        )
    else:
        lines.append("- **[confirmed]** No overlapping instruction claims were observed.")
    if failures:
        failure_counts = Counter(item["type"] for item in failures)
        lines.append(
            "- **[unknown]** Decode/target failures: "
            + ", ".join(f"{key}={value}" for key, value in sorted(failure_counts.items()))
            + "."
        )
    else:
        lines.append("- **[confirmed]** No decode failures were observed.")

    lines.extend(
        [
            "",
            "## Risk interpretation",
            "",
            "- **[confirmed]** Every `confirmed_reachable_code` byte has a recursive path from a vector/explicit seed without crossing an inferred dispatch edge.",
            "- **[confirmed]** Every `runtime_confirmed_code` instruction starts at a byte-validated PC observed by MAME; overlap with stronger static-confirmed evidence is retained in the evidence array.",
            "- **[probable]** `runtime_reachable_code` is a static successor of trace-confirmed code but was not itself necessarily executed.",
            "- **[probable]** Every `heuristic_reachable_code` byte descends from a shape-validated BRA.W table or another explicitly heuristic boundary; it is kept separate in JSON/CSV/range metrics.",
            "- **[probable]** Direct-call destinations are genuine callable routines, but shared tails, thunk entries, and assembly-local helper conventions can make source-level function boundaries differ.",
            "- **[candidate]** Direct-`JMP` destinations are useful tail-function candidates only. They must not be renamed as independent functions without more xref or trace evidence.",
            "- **[unknown]** Bytes behind unresolved indirect dispatch, copied-to-RAM code, Z80 upload payloads, dormant code, and data-referenced callbacks are not recovered by this pass.",
            "- **[unknown]** The large unknown set is intentionally not called data. It includes every byte for which this pass has not proved reachable 68000 execution.",
            "",
            "## Recommended next steps",
            "",
            "1. Resolve each PC-indexed call/jump by recovering its range check and table element width; promote only targets validated by table shape and runtime traces.",
            "2. Collect MAME execution traces and merge executed PCs as a separate `trace-confirmed` evidence class.",
            "3. Find data-stored callback pointers using xrefs from already confirmed code; keep pointer-table candidates separate until at least two independent checks agree.",
            "4. Partition the global CFG into routine candidates, preserving shared blocks and tail calls rather than forcing non-overlapping source-like functions.",
            "5. Classify remaining ranges with independent asset/text/audio analyses; never infer `data` solely from the absence of a static code path.",
            "",
            "## Generated files",
            "",
            "- `code_map.json`: complete machine-readable result.",
            "- `vectors.csv`, `function_entries.csv`, `instructions.csv`, `edges.csv`: primary tables.",
            "- `heuristic_dispatch_tables.csv`: shape-validated PC-indexed BRA.W table candidates.",
            "- `ranges.csv`: exhaustive non-overlapping byte classification.",
            "- `unresolved_transfers.csv`, `conflicts.csv`, `decode_failures.csv`: retained uncertainty.",
            "- `reachable_disassembly.lst`: address-sorted conservative disassembly.",
            "",
        ]
    )
    return "\n".join(lines)


def disassembly_listing(result: dict[str, Any]) -> str:
    function_names = {
        entry["address"]: entry["name"] for entry in result["function_entries"]
    }
    incoming: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for edge in result["edges"]:
        if edge["target"] is not None:
            incoming[edge["target"]].append(edge)
    lines = [
        f"; ROM SHA-256: {result['rom']['sha256']}",
        "; Conservative reachable M68000 listing; unknown bytes are omitted.",
        "; Generated by m68k_code_map.py; do not hand-edit.",
        "",
    ]
    for instruction in result["instructions"]:
        address = instruction["address"]
        if address in function_names:
            lines.extend(["", f"{function_names[address]}:"])
        elif incoming.get(address):
            lines.append(f"loc_{address:06X}:")
        operand = f" {instruction['operand']}" if instruction["operand"] else ""
        lines.append(
            f"{address:06X}: [{instruction['confidence'][0].upper()}] "
            f"{instruction['bytes']:<44} "
            f"{instruction['mnemonic']}{operand}"
        )
    lines.append("")
    return "\n".join(lines)


def write_outputs(output_dir: Path, result: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_text_lf(
        output_dir / "code_map.json",
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
    )
    write_csv(
        output_dir / "vectors.csv",
        [
            "index",
            "vector_address",
            "vector_address_hex",
            "name",
            "value",
            "value_hex",
            "status",
        ],
        result["vectors"],
    )
    function_rows = []
    for entry in result["function_entries"]:
        row = dict(entry)
        row["evidence_count"] = len(entry["evidence"])
        row["evidence_types"] = sorted({item["type"] for item in entry["evidence"]})
        function_rows.append(row)
    write_csv(
        output_dir / "function_entries.csv",
        [
            "address",
            "address_hex",
            "name",
            "classification",
            "decoded",
            "evidence_count",
            "evidence_types",
            "evidence",
        ],
        function_rows,
    )
    write_csv(
        output_dir / "instructions.csv",
        [
            "address",
            "address_hex",
            "size",
            "bytes",
            "mnemonic",
            "operand",
            "flow_type",
            "confidence",
            "discovery_evidence",
        ],
        result["instructions"],
    )
    write_csv(
        output_dir / "edges.csv",
        [
            "source",
            "source_hex",
            "target",
            "target_hex",
            "type",
            "direct",
            "status",
            "operand",
            "base_hint",
            "base_hint_hex",
            "evidence_level",
            "evidence_type",
            "observation_count",
        ],
        result["edges"],
    )
    write_csv(
        output_dir / "heuristic_dispatch_tables.csv",
        [
            "source",
            "source_hex",
            "transfer_type",
            "operand",
            "base_hint",
            "base_hint_hex",
            "first_slot_offset",
            "first_slot",
            "first_slot_hex",
            "stride",
            "entry_count",
            "classification",
            "promotion",
            "entries",
        ],
        result["heuristic_dispatch_tables"],
    )
    write_csv(
        output_dir / "ranges.csv",
        [
            "start",
            "start_hex",
            "end_exclusive",
            "end_exclusive_hex",
            "length",
            "classification",
        ],
        result["ranges"],
    )
    write_csv(
        output_dir / "unresolved_transfers.csv",
        [
            "source",
            "source_hex",
            "type",
            "operand",
            "reason",
            "base_hint",
            "base_hint_hex",
            "mechanism",
            "classification_confidence",
            "resolution_status",
            "confirmed_target_count",
            "probable_target_count",
            "target_set_complete",
            "indirect_evidence_source",
        ],
        result["unresolved_transfers"],
    )
    write_csv(
        output_dir / "conflicts.csv",
        [
            "target",
            "target_hex",
            "type",
            "existing_instruction",
            "existing_instruction_hex",
            "source",
            "source_hex",
            "evidence",
        ],
        result["conflicts"],
    )
    write_csv(
        output_dir / "decode_failures.csv",
        [
            "address",
            "address_hex",
            "type",
            "source",
            "source_hex",
            "detail",
        ],
        result["decode_failures"],
    )
    write_text_lf(output_dir / "coverage_report.md", markdown_report(result))
    write_text_lf(output_dir / "reachable_disassembly.lst", disassembly_listing(result))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Conservative recursive Motorola 68000 code discovery"
    )
    parser.add_argument("rom", type=Path, help="linear big-endian Mega Drive ROM")
    parser.add_argument(
        "--output-dir", type=Path, required=True, help="directory for generated reports"
    )
    parser.add_argument(
        "--capstone-path",
        type=Path,
        help="directory containing the capstone Python package",
    )
    parser.add_argument(
        "--expected-sha256",
        default=None,
        help="abort unless the input SHA-256 matches this value",
    )
    parser.add_argument(
        "--seed",
        type=parse_int,
        action="append",
        default=[],
        help="additional confirmed code seed (repeatable; e.g. 0x11BC6)",
    )
    parser.add_argument(
        "--trace-summary",
        type=Path,
        action="append",
        default=[],
        help=(
            "runtime coverage JSON whose PCs are imported as runtime_confirmed "
            "evidence (repeatable; duplicate PCs must agree)"
        ),
    )
    parser.add_argument(
        "--indirect-evidence",
        type=Path,
        help=(
            "phase-3 indirect-transfer JSON; every source/table/target byte is "
            "validated before use"
        ),
    )
    parser.add_argument(
        "--max-instructions",
        type=int,
        default=None,
        help="safety ceiling; default is half the ROM byte size",
    )
    parser.add_argument(
        "--no-heuristic-bra-tables",
        action="store_true",
        help="disable promotion of shape-validated PC-indexed BRA.W tables",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rom = args.rom.read_bytes()
    actual_sha256 = hashlib.sha256(rom).hexdigest()
    if args.expected_sha256 and actual_sha256.lower() != args.expected_sha256.lower():
        raise SystemExit(
            "Input hash mismatch: "
            f"expected {args.expected_sha256.lower()}, got {actual_sha256.lower()}"
        )
    capstone_module = load_capstone(args.capstone_path)
    runtime_trace = load_runtime_trace_summaries(args.trace_summary, rom)
    indirect_evidence = (
        load_indirect_evidence(args.indirect_evidence, rom)
        if args.indirect_evidence
        else None
    )
    analysis = M68KCodeMap(
        rom,
        capstone_module=capstone_module,
        analyst_seeds=args.seed,
        max_instructions=args.max_instructions,
        infer_bra_tables=not args.no_heuristic_bra_tables,
        runtime_trace=runtime_trace,
        indirect_evidence=indirect_evidence,
    )
    analysis.analyse()
    result = analysis.result(args.rom)
    if not result["validation"]["all_passed"]:
        failed = [
            item["name"] for item in result["validation"]["checks"] if not item["passed"]
        ]
        raise RuntimeError("Internal validation failed: " + ", ".join(failed))
    write_outputs(args.output_dir, result)
    coverage = result["coverage"]
    print(
        "M68000 code map complete: "
        f"{coverage['instruction_count']} instructions, "
        f"{coverage['reachable_code_bytes']} bytes, "
        f"{coverage['rom_coverage_percent']:.6f}% of ROM, "
        f"{coverage['unresolved_transfer_count']} unresolved transfers, "
        f"{coverage['conflict_count']} conflicts"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
