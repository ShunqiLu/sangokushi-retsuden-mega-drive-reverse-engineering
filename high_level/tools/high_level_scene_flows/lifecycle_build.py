"""Build complete duel lifecycle/actor owners from explicit business source.

These fourteen physical owners complement the menu/action/AI decision families.
Inline table gaps and sparse output padding are not selected as code. External
symbols bind actual interfaces, never emit missing callees or invent a console.
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


LIFECYCLE_OWNERS = frozenset({
    'advance_duel_entry_palette', 'run_duel_scene',
    'show_active_duel_turn_label', 'wait_active_duel_action',
    'configure_duel_weapon_motion', 'refresh_duel_actors',
    'upload_duel_officer_name', 'clear_duel_text_plane',
    'decode_duel_byte_lanes', 'choose_duel_status_text',
    'update_duel_actor', 'scan_duel_thresholds',
    'append_duel_sprite', 'measure_duel_weapon_contact',
})
# Original external symbolic interfaces. PC-relative and indexed calls retain
# their real instruction shape; this list is not their valid target-set proof.
EXTERNAL_SYMBOL_TARGETS = frozenset({
    0x68ce, 0x808a, 0x83d4, 0xad06, 0xae8a, 0xaf1e, 0xdea6,
    0x26bfa, 0x279e6, 0x27a10, 0x27d9c, 0x27dfc, 0x27e06,
    0x27ed2, 0x2a29a,
})
LIFECYCLE_BYTES = 3964
LIFECYCLE_ROWS = 957
LIFECYCLE_SPANS = 20


def compile_duel_lifecycle(source: str) -> tuple[dict, dict]:
    """Compile once and select the complete declared fourteen-owner family."""
    compiled = compile_duel(source)
    units = compiled['units']
    expected = {binding.name: asdict(binding) for binding in DUEL_BINDINGS}
    actual = {unit['binding']['name']: unit['binding'] for unit in units}
    if len(actual) != len(units) or actual != expected:
        raise CompileError('complete declared duel ownership is required')
    selected = [unit for unit in units
                if unit['binding']['name'] in LIFECYCLE_OWNERS]
    if len(selected) != len(LIFECYCLE_OWNERS):
        raise CompileError('all fourteen lifecycle owners are required')
    instructions = sorted(
        (row for unit in selected for row in unit['instructions']),
        key=lambda row: row['target_PC'],
    )
    segments = sorted((start, end) for unit in selected
                      for start, end in unit['binding']['segments'])
    if (len(segments) != LIFECYCLE_SPANS or
            sum(end - start for start, end in segments) != LIFECYCLE_BYTES or
            any(left[1] > right[0] for left, right in zip(segments, segments[1:]))):
        raise CompileError('complete disjoint lifecycle allocations required')
    rows, targets, index = [], set(), 0
    for start, end in segments:
        cursor = start
        while index < len(instructions) and instructions[index]['target_PC'] < end:
            row = instructions[index]
            pc, width = row['target_PC'], row['encoding_bytes']
            if (type(pc) is not int or type(width) is not int or pc != cursor
                    or width not in (2, 4, 6, 8, 10) or pc + width > end):
                raise CompileError('actual contiguous instruction geometry required')
            rows.append(dict(logical_pc=pc, physical_pc=pc, width=width,
                             operation=row['operation'], operands=row['operands']))
            targets.update(int(value, 16) for value in
                           re.findall(r'\bscene_pc_([0-9a-f]{6})\b', row['operands']))
            cursor += width
            index += 1
        if cursor != end:
            raise CompileError('lifecycle physical segment contains a code gap')
    if index != len(instructions) or len(rows) != LIFECYCLE_ROWS:
        raise CompileError('complete lifecycle instruction authority required')
    instruction_pcs = {row['physical_pc'] for row in rows}
    outside = targets - instruction_pcs
    if outside != EXTERNAL_SYMBOL_TARGETS:
        raise CompileError('only declared external lifecycle symbols are permitted')
    assembly = render_physical(selected)
    assembly += ''.join(f'.set scene_pc_{pc:06x},0x{pc:x}\n'
                        for pc in sorted(outside))
    assembly, symbols = _instrument('duel_lifecycle', assembly, rows)
    group = dict(name='duel_lifecycle', cpu='m68k', assembly=assembly,
                 instruction_rows=rows, expected_symbols=symbols,
                 sources={'business_duel.py': source})
    return compiled, group


def assemble_duel_lifecycle(source: str, output: Path, m68k_bin: Path) -> dict:
    """Generate and assemble this existing family, not a whole game image."""
    compiled, group = compile_duel_lifecycle(source)
    policy = compiled.get('source_policy')
    if type(policy) is not dict:
        raise CompileError('actual supplied-source policy provenance required')
    rendered_policy = json.dumps(policy, ensure_ascii=False, indent=2) + '\n'
    built = assemble_group(group, output, Toolchains(m68k_bin, m68k_bin))
    (output / 'source-policy.json').write_text(rendered_policy, encoding='utf-8')
    return dict(status='BUILT_LIFECYCLE_FAMILY_ONLY', owners=sorted(LIFECYCLE_OWNERS),
                physical_segments=sorted((start, end) for unit in compiled['units']
                                         if unit['binding']['name'] in LIFECYCLE_OWNERS
                                         for start, end in unit['binding']['segments']),
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
                        help='Local Windows path to the configured GNU M68K tools')
    args = parser.parse_args(argv)
    if not args.duel_source.is_file() or args.duel_source.stat().st_size > 1_200_000:
        raise ValueError('bounded explicit UTF-8 business source required')
    source = args.duel_source.read_text(encoding='utf-8')
    print(json.dumps(assemble_duel_lifecycle(source, args.output, args.m68k_bin),
                     ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
