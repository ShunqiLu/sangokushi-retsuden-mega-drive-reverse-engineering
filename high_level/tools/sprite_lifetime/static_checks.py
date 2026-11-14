"""Read-only Phase 16 anchors; not an emulator or a whole-program proof.

Run from the project root: python -m tools.sprite_lifetime.static_checks
The default input is the canonical external BIN, never a generated bank.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import hashlib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = PROJECT_ROOT.parent / "work" / "original_g5510.bin"
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
ACTOR_WORDS = (0xFF7054, 0xFF7056, 0xFF705C, 0xFF70A4, 0xFF70A6, 0xFF70AC)

# These are complete instructions, not disassembly text or address-only seals.
ANCHORS = {
    0x00DF6E: "46fc2700", 0x00E05E: "303b0064",
    0x00E062: "41fa1da2", 0x00E068: "4eb00000",
    0x010A3C: "4eb90001b604", 0x010A42: "4e75",
    0x01BFE0: "0c3800b8f579", 0x01BFE6: "6600f61c",
    0x01B604: "61000306", 0x01B608: "65000036",
    0x01B60C: "303c07ff", 0x01B610: "41f900ff7000",
    0x01B616: "4298", 0x01B618: "51c8fffc",
    0x01B61C: "610000a4", 0x01B626: "31fc0209f612",
    0x01B62C: "31fc000df362", 0x01B632: "4278f352",
    0x01B95A: "007c0001", 0x01B962: "027cfffe",
    0x01B8E6: "41f900ff39b2", 0x01B8EC: "d0f900ff3bb2",
    0x01B8FC: "1158fffd", 0x01B904: "1158fffd",
    0x00E09C: "31f8f612f3c2", 0x00E0A2: "31f8f362f3c4",
    0x00E0A8: "31fc0208f612", 0x00E0AE: "31fc0013f362",
    0x003282: "3038f36a", 0x00328A: "6400004e",
    0x0032DA: "31f8f3c4f362", 0x0032E0: "31f8f3c2f612",
    0x00493A: "4eb90000ad06", 0x00AD12: "4278f31a",
    0x0150BE: "31fc0013f65a", 0x0150CA: "31fc0208f612",
    0x0150D0: "31fc0004f362", 0x015D0C: "31fc00c4f600",
    0x015DDA: "31fc000df362", 0x01F77A: "31fc00c4f600",
    0x02381E: "4eb9000260e4", 0x0260F6: "4278f600",
    0x0260FA: "46fc2500", 0x02611E: "46fc2700",
    0x026122: "31dff362", 0x026126: "31dff612", 0x02612A: "4e75",
    0x023844: "31fc0407f612", 0x02384A: "31fc0003f362",
    0x023850: "4278f352", 0x023854: "46fc2500",
    0x023858: "0c7800c4f600", 0x02385E: "66f8",
    0x023860: "46fc2700", 0x023864: "4eb900000dc0",
    0x019FC6: "3038f740", 0x01A006: "31fc00b8f600",
    0x0676F6: "4278f652", 0x067716: "31fc0028f600",
    0x067A2C: "46fc2500",
}

MODE_0209_WRITERS = (
    0x000B2A, 0x001176, 0x002B76, 0x002BA4, 0x002BDA, 0x002C8C,
    0x002CC6, 0x002CF2, 0x002D9E, 0x010562, 0x01507C, 0x01B626, 0x030B0A,
)
STATE_000D_WRITERS = (0x00C4A4, 0x015DDA, 0x01B62C)
C4_WRITERS = (0x015D0C, 0x01F77A)
SECONDARY_TARGETS = (
    0x00FE06, 0x00FF58, 0x00FF98, 0x010224, 0x01022C, 0x010234, 0x0103E8,
    *([0x00FE06] * 9), 0x0103EA, 0x010694, 0x010A34, 0x010A3C, 0x010A44,
)


def u16(rom: bytes, address: int) -> int:
    if address < 0 or address + 2 > len(rom):
        raise ValueError("word outside ROM")
    return int.from_bytes(rom[address:address + 2], "big")


def signed_word(value: int) -> int:
    return value if value < 0x8000 else value - 0x10000


def signed_table(rom: bytes, start: int, count: int, base: int) -> tuple[int, ...]:
    if count < 0:
        raise ValueError("negative table count")
    return tuple(base + signed_word(u16(rom, start + 2 * n)) for n in range(count))


def aligned_occurrences(rom: bytes, pattern: bytes) -> tuple[int, ...]:
    if not pattern:
        raise ValueError("empty opcode pattern")
    return tuple(n for n in range(0, len(rom) - len(pattern) + 1, 2)
                 if rom[n:n + len(pattern)] == pattern)


def check_anchors(rom: bytes) -> None:
    for address, encoded in ANCHORS.items():
        expected = bytes.fromhex(encoded)
        if rom[address:address + len(expected)] != expected:
            raise ValueError(f"instruction mismatch at {address:06X}")


def message_0114(rom: bytes) -> dict:
    """Resolve actual two-level text offsets and inspect the fixed name records.

    This does not execute the message engine or prove its RAM cursor lifetime.
    All name IDs 0..255 are checked as a conditional input domain, not promoted
    to a claim that every producer stays inside that domain.
    """
    directory = int.from_bytes(rom[0x092C4A:0x092C4E], "big")
    page = directory + signed_word(u16(rom, 0x092C4E + 2))
    base = int.from_bytes(rom[page:page + 4], "big")
    start = base + signed_word(u16(rom, page + 4 + 2 * 0x14))
    words = tuple(u16(rom, start + 2 * n) for n in range(15))
    expected = (0x8008, 0x4C1B, 0x4512, 0x4C12, 0x800A, 0x4C1B, 0x4512,
                0x4132, 0x4322, 0x4438, 0x4D11, 0x4727, 0x403D, 0x403D, 0x8000)
    if page != 0x092DF8 or start != 0x094268 or words != expected:
        raise ValueError("message 0114 topology/content mismatch")
    for index in range(256):
        name = tuple(u16(rom, 0x08A504 + 6 * index + 2 * n) | 0x4000 for n in range(3))
        if any(word & 0x8000 for word in name) or all(word == 0x403F for word in name):
            raise ValueError(f"name record {index} violates checked insertion premise")
    return {"start": start, "end_exclusive": start + 30, "word_count": 15,
            "control_words": [word for word in words if word & 0x8000],
            "checked_name_records": 256}


def inspect_rom(rom: bytes) -> dict:
    digest = hashlib.sha256(rom).hexdigest()
    if len(rom) != 0x100000 or digest != ROM_SHA256:
        raise ValueError("not the canonical 1048576-byte original BIN")
    check_anchors(rom)
    scans = (
        ("literal_0209_f612", "31fc0209f612", MODE_0209_WRITERS),
        ("literal_000d_f362", "31fc000df362", STATE_000D_WRITERS),
        ("literal_00c4_f600", "31fc00c4f600", C4_WRITERS),
    )
    scan_results = {}
    for name, encoded, expected in scans:
        actual = aligned_occurrences(rom, bytes.fromhex(encoded))
        if actual != expected:
            raise ValueError(f"aligned literal inventory changed: {name}")
        scan_results[name] = list(actual)
    secondary = signed_table(rom, 0x00E0C4, 21, 0x00FE06)
    if secondary != SECONDARY_TARGETS:
        raise ValueError("secondary command table mismatch")
    mode13 = signed_table(rom, 0x013D58, 17, 0x013D7A)[13]
    restore = signed_table(rom, 0x002438, 20, 0x002490)[19]
    if mode13 != 0x015CC4 or restore != 0x003282:
        raise ValueError("alternate state/restore selection mismatch")
    iterations = u16(rom, 0x01B60E) + 1
    clear_start = int.from_bytes(rom[0x01B612:0x01B616], "big")
    clear_end = clear_start + 4 * iterations
    if (clear_start, clear_end, iterations) != (0xFF7000, 0xFF9000, 2048):
        raise ValueError("alternate clear extent mismatch")
    if not all(clear_start <= word and word + 2 <= clear_end for word in ACTOR_WORDS):
        raise ValueError("actor word not covered by clear")
    slices = [(0x00E050, 0x00E0EE), (0x010A34, 0x010A4C),
              (0x01B604, 0x01B968), (0x003282, 0x00330C),
              (0x023806, 0x023870), (0x0260E4, 0x02612C),
              (0x019FA6, 0x01A00E), (0x094268, 0x094286)]
    return {
        "status": "confirmed static anchors; conditional lifetime only",
        "rom_sha256": digest, "instruction_anchors": len(ANCHORS),
        "aligned_literal_inventory": scan_results,
        "inventory_is_all_writers_proof": False,
        "secondary_table": {"start": 0x00E0C4, "end_exclusive": 0x00E0EE,
                            "targets": list(secondary), "slot6_bypassed": True,
                            "runtime_selector_domain_closed": False},
        "alternate_state_target": mode13, "restore_window_target": restore,
        "new_clear": {"instruction": 0x01B616, "iterations": iterations,
                      "start": clear_start, "end_exclusive": clear_end,
                      "bytes": clear_end - clear_start, "actor_words": list(ACTOR_WORDS)},
        "old_c4_kill_instruction": 0x0260F6,
        "message_0114": message_0114(rom),
        "slice_sha256": {f"{lo:06X}..{hi:06X}": hashlib.sha256(rom[lo:hi]).hexdigest()
                         for lo, hi in slices},
        "natural_runtime_claimed": False, "ownership_bytes_added": 0,
        "global_frame_bound_proved": False, "complete_indirect_domains_added": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, default=DEFAULT_ROM)
    args = parser.parse_args()
    # No output path, mutations, external processes, or publication lifecycle.
    print(json.dumps(inspect_rom(args.rom.read_bytes()), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
