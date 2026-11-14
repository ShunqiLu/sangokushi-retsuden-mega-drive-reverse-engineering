"""Build the whole manual-action and AI decision family from business source.

The five existing physical owners include noncontiguous AI code. Original
embedded-table gaps are not selected as instructions or declared as recovered
data by this leaf build. External calls bind their existing interfaces; this
is neither a full ROM builder nor an emulated console.
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


DECISION_OWNERS = frozenset({
    'choose_duel_action_menu',
    'choose_duel_ai_command',
    'choose_duel_ai_override',
    'sample_duel_probability',
    'choose_duel_ai_timeout',
})
EXTERNAL_CALL_TARGETS = frozenset({0x279E6, 0x28F9C, 0x83D4, 0x28F90})
DECISION_BYTES = 1180


def compile_duel_action_ai(source: str) -> tuple[dict, dict]:
    """Compile once, then select complete declared action/AI physical owners."""
    compiled = compile_duel(source)
    units = compiled['units']
    expected = {binding.name: asdict(binding) for binding in DUEL_BINDINGS}
    actual = {unit['binding']['name']: unit['binding'] for unit in units}
    if len(actual) != len(units) or actual != expected:
        raise CompileError('complete declared duel ownership is required')
    decisions = [unit for unit in units
                 if unit['binding']['name'] in DECISION_OWNERS]
    if len(decisions) != len(DECISION_OWNERS):
        raise CompileError('complete five-owner decision family required')
    instructions = sorted(
        (row for unit in decisions for row in unit['instructions']),
        key=lambda row: row['target_PC'],
    )
    segments = sorted((start, end) for unit in decisions
                      for start, end in unit['binding']['segments'])
    if (sum(end - start for start, end in segments) != DECISION_BYTES or
            any(left[1] > right[0] for left, right in zip(segments, segments[1:]))):
        raise CompileError('disjoint complete decision physical extents required')
    rows, targets, index = [], set(), 0
    for start, end in segments:
        cursor = start
        while index < len(instructions) and instructions[index]['target_PC'] < end:
            row = instructions[index]
            pc, width = row['target_PC'], row['encoding_bytes']
            if (type(pc) is not int or type(width) is not int or pc != cursor
                    or width not in (2, 4, 6, 8, 10) or pc + width > end):
                raise CompileError('exact contiguous instruction authority within each segment required')
            rows.append(dict(logical_pc=pc, physical_pc=pc, width=width,
                             operation=row['operation'], operands=row['operands']))
            targets.update(int(value, 16) for value in
                           re.findall(r'\bscene_pc_([0-9a-f]{6})\b', row['operands']))
            cursor += width
            index += 1
        if cursor != end:
            raise CompileError('decision segment cannot contain an executable gap')
    if index != len(instructions):
        raise CompileError('instruction outside the declared decision segments')
    instruction_pcs = {row['physical_pc'] for row in rows}
    outside = targets - instruction_pcs
    if outside != EXTERNAL_CALL_TARGETS:
        raise CompileError('only declared decision call interfaces may be unresolved')
    assembly = render_physical(decisions)
    # Interface symbols do not emit the called algorithms or fill table gaps.
    assembly += ''.join(f'.set scene_pc_{pc:06x},0x{pc:x}\n'
                        for pc in sorted(outside))
    assembly, symbols = _instrument('duel_action_ai', assembly, rows)
    group = dict(name='duel_action_ai', cpu='m68k', assembly=assembly,
                 instruction_rows=rows, expected_symbols=symbols,
                 sources={'business_duel.py': source})
    return compiled, group


def assemble_duel_action_ai(source: str, output: Path, m68k_bin: Path) -> dict:
    """Generate and assemble only the existing 1,180-byte decision family."""
    compiled, group = compile_duel_action_ai(source)
    policy = compiled.get('source_policy')
    if type(policy) is not dict:
        raise CompileError('actual source-policy provenance is required')
    rendered_policy = json.dumps(policy, ensure_ascii=False, indent=2) + '\n'
    built = assemble_group(group, output, Toolchains(m68k_bin, m68k_bin))
    (output / 'source-policy.json').write_text(rendered_policy, encoding='utf-8')
    return dict(status='BUILT_DECISION_FAMILY_ONLY', owners=sorted(DECISION_OWNERS),
                physical_segments=sorted((start, end) for unit in compiled['units']
                                         if unit['binding']['name'] in DECISION_OWNERS
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
        raise ValueError('bounded explicit UTF-8 business source is required')
    source = args.duel_source.read_text(encoding='utf-8')
    print(json.dumps(assemble_duel_action_ai(source, args.output, args.m68k_bin),
                     ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
