"""Build the two loadout menus from explicit semantic Python source.

This deliberately small build entry uses the ordinary duel compiler, then
selects the two existing physical owners. It does not read a reference ROM,
old assembly or a prebuilt object. The surrounding game and console hardware
are outside this leaf build; external calls retain their real target addresses.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import re

from .compiler_common import CompileError, render_physical
from .compiler_duel import compile_duel
from .target import DUEL_BINDINGS
from ..high_level_rom.code_registry import _instrument
from ..high_level_rom.native import Toolchains, assemble_group


MENU_OWNERS = frozenset({
    'choose_duel_two_option_menu',
    'choose_first_duel_equipment',
})
MENU_START = 0x27D9C
MENU_END = 0x27ED2
EXTERNAL_CALL_TARGETS = frozenset({0x279E6, 0x28F9C})


def compile_duel_menus(source: str) -> tuple[dict, dict]:
    """Compile once, returning the complete duel result and one native leaf.

    The equipment owner already contains both first/second entries. Selecting
    it twice would double-count the same physical code. Original instruction
    widths and real start/end symbols are checked again by the native builder.
    """
    compiled = compile_duel(source)
    units = compiled['units']
    expected = {binding.name: asdict(binding) for binding in DUEL_BINDINGS}
    actual = {unit['binding']['name']: unit['binding'] for unit in units}
    if len(actual) != len(units) or actual != expected:
        raise CompileError('complete declared duel ownership is required')
    menus = [unit for unit in units if unit['binding']['name'] in MENU_OWNERS]
    instructions = sorted(
        (row for unit in menus for row in unit['instructions']),
        key=lambda row: row['target_PC'],
    )
    cursor = MENU_START
    rows = []
    targets = set()
    for row in instructions:
        pc, width = row['target_PC'], row['encoding_bytes']
        if type(pc) is not int or type(width) is not int or pc != cursor:
            raise CompileError('one contiguous menu instruction authority is required')
        rows.append(dict(logical_pc=pc, physical_pc=pc, width=width,
                         operation=row['operation'], operands=row['operands']))
        targets.update(int(value, 16) for value in
                       re.findall(r'\bscene_pc_([0-9a-f]{6})\b', row['operands']))
        cursor += width
    if cursor != MENU_END or len(menus) != len(MENU_OWNERS):
        raise CompileError('complete two-menu physical scope is required')
    outside = {target for target in targets if not MENU_START <= target < MENU_END}
    if outside != EXTERNAL_CALL_TARGETS:
        raise CompileError('explicit menu control/sprite call targets are required')
    assembly = render_physical(menus)
    # Absolute symbols bind existing call interfaces, not emitted callee bodies.
    assembly += ''.join(f'.set scene_pc_{pc:06x},0x{pc:x}\n'
                        for pc in sorted(outside))
    assembly, expected_symbols = _instrument('duel_loadout_menus', assembly, rows)
    group = dict(name='duel_loadout_menus', cpu='m68k', assembly=assembly,
                 instruction_rows=rows, expected_symbols=expected_symbols,
                 sources={'business_duel.py': source})
    return compiled, group


def assemble_duel_menus(source: str, output: Path, m68k_bin: Path) -> dict:
    """Generate and assemble only the 310-byte menu family in a fresh target."""
    compiled, group = compile_duel_menus(source)
    policy = compiled.get('source_policy')
    if type(policy) is not dict:
        raise CompileError('explicit source-policy provenance is required')
    rendered_policy = json.dumps(policy, ensure_ascii=False, indent=2) + '\n'
    # The native interface also has a Z80 path; this M68K-only group never uses it.
    built = assemble_group(group, output, Toolchains(m68k_bin, m68k_bin))
    (output / 'source-policy.json').write_text(
        rendered_policy, encoding='utf-8',
    )
    return dict(status='BUILT_MENUS_ONLY', owners=sorted(MENU_OWNERS),
                physical_start=MENU_START, physical_end=MENU_END,
                instruction_bytes=built['receipt']['instruction_bytes'],
                instruction_count=built['receipt']['instruction_count'],
                child_exits=built['receipt']['child_exits'],
                original_ROM_input=False, precompiled_input=False,
                complete_ROM=False, complete_CPU=False,
                new_matching_BYTES=0, new_strict_BYTES=0)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--duel-source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True,
                        help='Absent dedicated output directory; never overwritten')
    parser.add_argument('--m68k-bin', type=Path, required=True,
                        help='Local Windows path to the configured WSL GNU M68K tools')
    args = parser.parse_args(argv)
    if not args.duel_source.is_file() or args.duel_source.stat().st_size > 1_200_000:
        raise ValueError('bounded explicit UTF-8 business source is required')
    source = args.duel_source.read_text(encoding='utf-8')
    print(json.dumps(assemble_duel_menus(source, args.output, args.m68k_bin),
                     ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
