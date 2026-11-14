"""Build the complete scripted-scene and scene-object physical families.

Both supplied business modules are required. Inline data gaps remain excluded,
and seven external symbols name actual call interfaces without emitting their
callees. This is a finite source-policy build, not a console or whole ROM.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import re

from .compiler_common import CompileError, render_physical
from .compiler_scene import compile_scene
from .compiler_objects import compile_objects
from .target import SCENE_BINDINGS, OBJECTS_BINDINGS
from ..high_level_rom.code_registry import _instrument
from ..high_level_rom.native import Toolchains, assemble_group


FAMILY_BINDINGS = SCENE_BINDINGS + OBJECTS_BINDINGS
FAMILY_BYTES = 8806
FAMILY_SPANS = 67
EXTERNAL_SYMBOL_TARGETS = frozenset({
    0x68CE, 0x808A, 0x83C8, 0x83D4, 0xAF04, 0x1C2C8, 0x1C586,
})


def compile_scene_objects(scene_source: str, objects_source: str) -> tuple[dict, dict]:
    """Generate all 44 owners once from the two explicit complete modules."""
    scene = compile_scene(scene_source)
    objects = compile_objects(objects_source)
    policies = {
        'scene': scene.get('source_policy'),
        'objects': objects.get('source_policy'),
    }
    if any(type(policy) is not dict for policy in policies.values()):
        raise CompileError('both complete families need supplied-source policy provenance')
    units = scene['units'] + objects['units']
    expected = {binding.name: asdict(binding) for binding in FAMILY_BINDINGS}
    actual = {unit['binding']['name']: unit['binding'] for unit in units}
    if len(actual) != len(units) or actual != expected:
        raise CompileError('all 44 declared physical owners are required')
    instructions = sorted(
        (row for unit in units for row in unit['instructions']),
        key=lambda row: row['target_PC'],
    )
    segments = sorted((start, end) for binding in FAMILY_BINDINGS
                      for start, end in binding.segments)
    if (len(segments) != FAMILY_SPANS
            or sum(end - start for start, end in segments) != FAMILY_BYTES
            or any(left[1] > right[0] for left, right in zip(segments, segments[1:]))):
        raise CompileError('complete disjoint scene/object allocations are required')
    rows, targets, index = [], set(), 0
    for start, end in segments:
        cursor = start
        while index < len(instructions) and instructions[index]['target_PC'] < end:
            row = instructions[index]
            pc, width = row['target_PC'], row['encoding_bytes']
            if (type(pc) is not int or type(width) is not int or pc != cursor
                    or width not in (2, 4, 6, 8, 10) or pc + width > end):
                raise CompileError('actual contiguous instruction geometry is required')
            rows.append(dict(logical_pc=pc, physical_pc=pc, width=width,
                             operation=row['operation'], operands=row['operands']))
            targets.update(int(value, 16) for value in
                           re.findall(r'\bscene_pc_([0-9a-f]{6})\b', row['operands']))
            cursor += width
            index += 1
        if cursor != end:
            raise CompileError('scene/object code segment contains an executable gap')
    if index != len(instructions):
        raise CompileError('instruction outside the complete family allocations')
    instruction_pcs = {row['physical_pc'] for row in rows}
    if len(instruction_pcs) != len(rows):
        raise CompileError('each physical instruction needs one source authority')
    outside = targets - instruction_pcs
    if outside != EXTERNAL_SYMBOL_TARGETS:
        raise CompileError('only the seven declared external symbols are permitted')
    assembly = render_physical(units)
    assembly += ''.join(f'.set scene_pc_{pc:06x},0x{pc:x}\n'
                        for pc in sorted(outside))
    assembly, symbols = _instrument('scene_objects', assembly, rows)
    compiled = dict(units=units, source_policy=policies,
                    allocated_bytes=FAMILY_BYTES, instructions=len(rows),
                    original_generation_input=False, whole_closed_workflow=False)
    group = dict(name='scene_objects', cpu='m68k', assembly=assembly,
                 instruction_rows=rows, expected_symbols=symbols,
                 sources={'business_scene.py': scene_source,
                          'business_objects.py': objects_source})
    return compiled, group


def assemble_scene_objects(scene_source: str, objects_source: str,
                           output: Path, m68k_bin: Path) -> dict:
    """Build the existing complete family; an absent output path is required."""
    compiled, group = compile_scene_objects(scene_source, objects_source)
    policy = json.dumps(compiled['source_policy'], ensure_ascii=False, indent=2) + '\n'
    built = assemble_group(group, output, Toolchains(m68k_bin, m68k_bin))
    (output / 'source-policy.json').write_text(policy, encoding='utf-8')
    return dict(status='BUILT_SCENE_OBJECT_FAMILIES_ONLY',
                owners=[binding.name for binding in FAMILY_BINDINGS],
                physical_segments=sorted((start, end) for binding in FAMILY_BINDINGS
                                         for start, end in binding.segments),
                instruction_bytes=built['receipt']['instruction_bytes'],
                instruction_count=built['receipt']['instruction_count'],
                child_exits=built['receipt']['child_exits'],
                original_ROM_input=False, precompiled_input=False,
                complete_ROM=False, complete_CPU=False,
                new_matching_BYTES=0, new_strict_BYTES=0)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene-source', type=Path, required=True)
    parser.add_argument('--objects-source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--m68k-bin', type=Path, required=True)
    args = parser.parse_args(argv)
    for path in (args.scene_source, args.objects_source):
        if not path.is_file() or path.stat().st_size > 1_200_000:
            raise ValueError('bounded explicit UTF-8 business modules are required')
    print(json.dumps(assemble_scene_objects(
        args.scene_source.read_text(encoding='utf-8'),
        args.objects_source.read_text(encoding='utf-8'),
        args.output, args.m68k_bin), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
