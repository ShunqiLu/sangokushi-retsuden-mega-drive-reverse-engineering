"""Integrate own high-level code and independently encoded resources.

Incomplete attempts retain explicit gaps/conflicts and never emit a pretend
complete ROM. There is no original-ROM option, bank fallback or patching path.
Acceptance comparison belongs to a separate command after generation.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, is_dataclass
import json
from pathlib import Path
import traceback
from typing import Mapping

from .native import Toolchains, NativeBuildError, assemble_group, fresh_output


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def audio_groups(project_root: Path) -> list[dict]:
    """Generate separate audio code images from explicit own business texts."""
    from ..high_level_audio_engine.compiler import generate
    from ..high_level_audio_engine.target import BUSINESS_MODULES, UNITS

    directory = project_root / 'tools/high_level_audio_engine'
    sources = {name: (directory / name).read_text(encoding='utf-8') for name in BUSINESS_MODULES}
    generated = generate(sources)
    result = []
    for unit in ('driver', 'startup'):
        descriptor = UNITS[unit]
        prefix = 'z80_' if unit == 'driver' else 'boot_z80_'
        rows, expected = [], {}
        for row in descriptor['rows']:
            address, width = row['address'], row['size']
            start, end = prefix + f'{address:04x}', prefix + f'{address:04x}_end'
            expected[start], expected[end] = address, address + width
            rows.append(dict(logical_pc=address, physical_pc=descriptor['rom_base'] + address,
                             width=width, start_symbol=start, end_symbol=end))
        result.append(dict(name='audio_' + unit, cpu='z80', audio_unit=unit,
                           descriptor=descriptor, physical_base=descriptor['rom_base'],
                           assembly=generated[unit], sources=sources,
                           instruction_rows=rows, expected_symbols=expected))
    return result


def _mapping(value) -> dict:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, Mapping):
        return dict(value)
    raise ValueError('explicit group/ownership mappings required')


def _intervals(positions: set[int]) -> list[dict]:
    result = []
    for position in sorted(positions):
        if result and result[-1]['end'] == position:
            result[-1]['end'] += 1
        else:
            result.append(dict(start=position, end=position + 1))
    return result


def _strip_bytes(value):
    if type(value) is bytes:
        return dict(byte_count=len(value))
    if isinstance(value, Mapping):
        return {key: _strip_bytes(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return [_strip_bytes(item) for item in value]
    if is_dataclass(value) and not isinstance(value, type):
        return _strip_bytes(asdict(value))
    return value


def prepare(project_root: Path, resource_root: Path | None = None) -> dict:
    """Prepare the full registered source scope; no native tool or ROM reads."""
    if resource_root is None:
        raise ValueError('an explicit independently owned resource_root is required; no legacy source fallback')
    from .code_registry import compile_code
    from .resource_registry import load_resources

    code = compile_code(project_root)
    groups = [_mapping(group) for group in code['groups']]
    groups.extend(audio_groups(project_root))
    names = [group['name'] for group in groups]
    if len(names) != len(set(names)):
        raise ValueError('one stable ID per native source group required')
    resources = load_resources(source_root=resource_root, allow_unavailable=True)
    ownership = list(code['ownership'])
    for group in groups:
        if group['cpu'] == 'z80':
            ownership.extend(dict(start=row['physical_pc'], end=row['physical_pc'] + row['width'],
                                  owner=group['name']) for row in group['instruction_rows'])
    positions = {pc for row in ownership for pc in range(row['start'], row['end'])}
    return dict(groups=groups, ownership=ownership, aliases=code.get('aliases', []),
                code_unavailable=code.get('unavailable', []), resources=resources,
                declared_code_bytes=len(positions), original_generation_input=False,
                complete_ROM=False, complete_CPU=False)


def select_code(results: dict[str, dict], ownership: list[dict], aliases: list[dict]) -> tuple[list, dict]:
    """Choose explicitly registered authorities and verify every reused byte.

    Equal bytes alone do not permit two editable owners. A non-owner's extent
    must have an explicit alias declaration and match actual canonical code.
    """
    from .image import ImageBlock

    owners = {}
    for raw in ownership:
        row = _mapping(raw)
        start, end, owner = row['start'], row['end'], row['owner']
        if (type(start) is not int or type(end) is not int or
                not 0 <= start < end <= 0x100000 or owner not in results):
            raise ValueError('invalid registered code authority')
        for position in range(start, end):
            if position in owners:
                raise ValueError(f'duplicate canonical code authority at {position:06X}')
            owners[position] = owner
    declared_aliases = {}
    for raw in aliases:
        row = _mapping(raw)
        start, end, owner, alias = row['start'], row['end'], row['owner'], row['alias']
        if (type(start) is not int or type(end) is not int or not 0 <= start < end <= 0x100000 or
                owner not in results or alias not in results or alias == owner):
            raise ValueError('invalid explicit code alias')
        for position in range(start, end):
            if owners.get(position) != owner or (alias, position) in declared_aliases:
                raise ValueError('conflicting or repeated code alias declaration')
            declared_aliases[alias, position] = owner
    canonical, output = {}, []
    for name, native in results.items():
        for block in native['blocks']:
            extent = range(block['start'], block['end'])
            assigned = {owners.get(position) for position in extent}
            if None in assigned or len(assigned) != 1:
                raise ValueError('instruction crosses a missing/mixed authority boundary')
            owner = assigned.pop()
            if owner == name:
                output.append(ImageBlock(block['start'], block['data'], name, block['role']))
                for offset, value in enumerate(block['data']):
                    position = block['start'] + offset
                    if position in canonical:
                        raise ValueError('canonical native byte emitted twice')
                    canonical[position] = value
    if set(canonical) != set(owners):
        raise ValueError('a declared canonical code extent was not actually generated')
    verified_aliases = set()
    for name, native in results.items():
        for block in native['blocks']:
            for offset, value in enumerate(block['data']):
                position = block['start'] + offset
                owner = owners[position]
                if owner != name:
                    if declared_aliases.get((name, position)) != owner:
                        raise ValueError('undeclared reused source authority')
                    if canonical[position] != value:
                        raise ValueError(f'actual reused source differs at {position:06X}: {name}/{owner}')
                    verified_aliases.add((name, position))
    if verified_aliases != set(declared_aliases):
        raise ValueError('a declared alias extent was not actually generated')
    return output, dict(unique_code_bytes=len(canonical),
                        actual_reuse_bytes_verified=len(verified_aliases),
                        code_intervals=_intervals(set(canonical)))


def _prepared_report(prepared: dict) -> dict:
    return dict(source_groups=[dict(name=group['name'], cpu=group['cpu'],
                                   source_modules=len(group.get('sources', {})),
                                   instructions=len(group['instruction_rows']),
                                   instruction_bytes=sum(row['width'] for row in group['instruction_rows']))
                               for group in prepared['groups']],
                declared_code_bytes=prepared['declared_code_bytes'],
                code_unavailable=prepared['code_unavailable'],
                resource_coverage=prepared['resources'].get('coverage'),
                resource_unavailable=prepared['resources'].get('unavailable', []),
                resource_conflicts=prepared['resources'].get('conflicts', []),
                resource_limits=prepared['resources'].get('limits', []),
                original_generation_input=False, complete_ROM=False, complete_CPU=False)


def build(prepared: dict, output: Path, tools: Toolchains, *, copier_header: bytes | None = None,
          workers: int = 2) -> dict:
    """One full integration attempt; no full image is emitted with gaps/conflicts."""
    from .image import ImageBlock, assemble_complete, find_gaps, interleave_smd

    if type(workers) is not int or not 1 <= workers <= 4:
        raise ValueError('one to four native workers required')
    target = fresh_output(output)
    target.mkdir(parents=True)
    report = _prepared_report(prepared)
    report.update(status='running', native_groups=[], conflicts=[], gaps=[], parent_exit=None,
                  new_matching_bytes=0, new_strict_bytes=0)
    results, failures = {}, []
    try:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pending = {pool.submit(assemble_group, group, target / group['name'], tools): group['name']
                       for group in prepared['groups']}
            for future in as_completed(pending):
                name = pending[future]
                try:
                    result = future.result()
                    results[name] = result
                    report['native_groups'].append(result['receipt'])
                    print(json.dumps(dict(group=name, native_exit=0,
                                          instruction_bytes=result['receipt']['instruction_bytes'])), flush=True)
                except NativeBuildError as error:
                    failures.append(dict(group=name, error=str(error)))
                    report['native_groups'].append(error.receipt)
                except Exception as error:
                    failures.append(dict(group=name, error=str(error)))
        if failures:
            report.update(status='native_failed', failures=failures, parent_exit=1)
            return report
        blocks, accounting = select_code(results, prepared['ownership'], prepared['aliases'])
        report.update(accounting)
        for raw in prepared['resources']['blocks']:
            row = _mapping(raw)
            if row['end'] != row['start'] + len(row['data']):
                raise ValueError('resource block extent differs from encoded data')
            blocks.append(ImageBlock(row['start'], row['data'], row['owner'], row['role']))
        # Preserve all overlap exceptions and resource-level unavailability. No
        # clipping of code operands or unknown payloads is done at this layer.
        try:
            gaps = find_gaps(blocks)
        except ValueError as error:
            report.update(status='conflicting_authorities', conflicts=[str(error)], parent_exit=2)
            return report
        report['gaps'] = [asdict(gap) for gap in gaps]
        report['missing_image_bytes'] = sum(gap.end - gap.start for gap in gaps)
        report['integrated_unique_bytes'] = 0x100000 - report['missing_image_bytes']
        report['image_blocks'] = [dict(start=block.start, end=block.start + len(block.data),
                                      owner=block.owner, role=block.role) for block in blocks]
        unavailable = prepared['code_unavailable'] or prepared['resources'].get('unavailable')
        conflicts = prepared['resources'].get('conflicts')
        if gaps or unavailable or conflicts:
            report.update(status='incomplete', parent_exit=2)
            return report
        image = assemble_complete(blocks)
        (target / 'SANGO.bin').write_bytes(image)
        report.update(status='BIN_generated', parent_exit=0, complete_ROM=True, image_bytes=len(image))
        if copier_header is not None:
            packed = interleave_smd(image, copier_header)
            (target / 'SANGO.smd').write_bytes(packed)
            report.update(status='BIN_and_SMD_generated', smd_bytes=len(packed))
        else:
            report['SMD_limit'] = 'a separately owned512-byte copier header is still required'
        # complete_ROM describes image coverage/generation only, never final
        # semantic/dual-source completion or external canonical acceptance.
        return report
    except Exception as error:
        report.update(status='integration_failed', error=str(error), parent_exit=1)
        raise
    finally:
        (target / 'receipt.json').write_text(json.dumps(_strip_bytes(report), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('plan', 'build'))
    parser.add_argument('--project-root', type=Path, default=PROJECT_ROOT)
    parser.add_argument('--resource-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--m68k-tools', type=Path)
    parser.add_argument('--z80-tools', type=Path)
    headers = parser.add_mutually_exclusive_group()
    headers.add_argument('--copier-header', type=Path)
    headers.add_argument('--copier-header-fields', type=Path,
                         help='own typed SMD metadata JSON; no external SMD payload read')
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args(argv)
    try:
        prepared = prepare(args.project_root.resolve(), args.resource_root)
    except Exception as error:
        # Source preparation can fail before build() owns its output. Retain
        # that real failure too, rather than leaving an apparently unstarted
        # attempt or silently trying an older compiler/source epoch.
        target = fresh_output(args.output)
        build_root = args.project_root.resolve() / 'build'
        if not target.is_relative_to(build_root):
            error.add_note('preparation evidence not written: output must be inside this project/build')
            raise
        target.mkdir(parents=True)
        failure = dict(status='source_preparation_failed', phase='prepare', parent_exit=1,
            error_type=type(error).__name__, error=str(error), traceback=traceback.format_exc(),
            source_failures=list(getattr(error, 'source_failures', ())),
            project_root=str(args.project_root.resolve()), resource_root=str(args.resource_root.resolve()),
            native_groups=[], complete_ROM=False, complete_CPU=False, new_strict_bytes=0,
            original_generation_input=False, precompiled_generation_input=False)
        (target / 'receipt.json').write_text(json.dumps(failure, ensure_ascii=False, indent=2) + '\n',
                                           encoding='utf-8')
        print(json.dumps(dict(status=failure['status'], parent_exit=1,
                              error=failure['error'], evidence=str(target / 'receipt.json')),
                         ensure_ascii=False), flush=True)
        return 1
    if args.mode == 'plan':
        output = fresh_output(args.output)
        output.mkdir(parents=True)
        report = _prepared_report(prepared)
        report['status'] = 'source_prepared_not_native'
        (output / 'receipt.json').write_text(json.dumps(_strip_bytes(report), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    else:
        if args.m68k_tools is None or args.z80_tools is None:
            parser.error('build requires both declared tool directories')
        header = args.copier_header.read_bytes() if args.copier_header else None
        if args.copier_header_fields is not None:
            from .copier_header import load
            header = load(args.copier_header_fields)
        if header is not None and len(header) != 512:
            raise ValueError('a512-byte independently owned copier header is required')
        report = build(prepared, args.output, Toolchains(args.m68k_tools, args.z80_tools),
                       copier_header=header, workers=args.workers)
    print(json.dumps({key: _strip_bytes(value) for key, value in report.items()
                      if key not in ('native_groups', 'image_blocks', 'source_groups', 'code_intervals')},
                     ensure_ascii=False), flush=True)
    return report.get('parent_exit', 0)


if __name__ == '__main__':
    raise SystemExit(main())
