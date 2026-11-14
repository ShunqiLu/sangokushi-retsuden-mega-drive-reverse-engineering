"""从 GNU 汇编和外部数据资源构建 Mega Drive 卡带。"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path

from .sources import load_layout, native_group, ordinary_root, member, read_text


def _summary(receipt):
    return {key: receipt[key] for key in ('name', 'cpu', 'parent_exit', 'instruction_count',
        'instruction_bytes', 'sparse_bytes_excluded', 'actual_boundaries_verified') if key in receipt}


def build_assembly(source_root: Path, layout_root: Path, resource_root: Path, output: Path,
        m68k_tools: Path, z80_tools: Path, *, workers: int = 2, copier_header_fields: Path | None = None) -> dict:
    """校验地址覆盖和指令宽度，写入新的构建目录。"""
    from ..high_level_rom.native import Toolchains, assemble_group, fresh_output, NativeBuildError
    from ..high_level_rom.resource_registry import RESOURCE_SPECS, load_resources
    from ..high_level_rom.image import ImageBlock, assemble_complete, interleave_smd, find_gaps
    if type(workers) is not int or not 1 <= workers <= 4:
        raise ValueError('one to four explicit native workers required')
    sources = ordinary_root(source_root, 'source_root')
    layouts = ordinary_root(layout_root, 'layout_root')
    resources_root = ordinary_root(resource_root, 'resource_root')
    tools = Toolchains(ordinary_root(m68k_tools, 'm68k_tools'), ordinary_root(z80_tools, 'z80_tools'))
    units, resource_ids = load_layout(layouts)
    if resource_ids != tuple(spec.id for spec in RESOURCE_SPECS):
        raise ValueError('the complete current explicit registered 128 typed DATA owners are required')
    target = fresh_output(output)
    if not target.is_relative_to(sources):
        raise ValueError('assembly output must remain inside the explicit source workspace')
    resource_protected = resources_root / 'resources' if resources_root == sources else resources_root
    for protected in (layouts, resource_protected, tools.m68k_bin, tools.z80_bin, sources / 'src', sources / 'tools'):
        if target == protected or target.is_relative_to(protected) or protected.is_relative_to(target):
            raise ValueError('fresh build output must not contain or overwrite source/resource/tool inputs')
    groups, source_origins = [], []
    for unit in units:
        group, origins = native_group(sources, unit)
        groups.append(group)
        source_origins.append(dict(group=unit.name, cpu=unit.cpu, files=origins,
            instructions=len(unit.rows), instruction_bytes=unit.instruction_bytes))
    # 从指定素材根读取 128 个登记资源，编码为卡带数据块。
    resource_result = load_resources(source_root=resources_root, ids=resource_ids, allow_unavailable=False)
    copier_header = None
    if copier_header_fields is not None:
        from ..high_level_rom.copier_header import encode
        fields_path = copier_header_fields.absolute()
        for ancestor in (fields_path, *fields_path.parents):
            if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
                raise ValueError('copier metadata through reparse point refused')
        copier_header = encode(json.loads(read_text(fields_path, 100_000)))
    target.mkdir(parents=True)
    report = dict(format='g5510-independent-assembly-build-v1', status='building', parent_exit=None,
        source_root=str(sources), layout_root=str(layouts), resource_root=str(resources_root),
        source_groups=source_origins, native_groups=[], failures=[],
        resource_coverage=resource_result['coverage'], complete_ROM=False, complete_CPU=False,
        source_edition='editable M68000/Z80 assembly', high_level_business_compiler_used=False,
        original_ROM_read=False, whole_bank_read=False, prior_native_product_read=False,
        source_opcode_comments_used=False, sparse_padding_selected=False,
        checksum_modified=False, canonical_comparison_performed=False)
    try:
        results = {}
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(assemble_group, group, target / group['name'], tools): group['name']
                for group in groups}
            for future in as_completed(futures):
                name = futures[future]
                try:
                    result = future.result()
                    results[name] = result
                    report['native_groups'].append(_summary(result['receipt']))
                except NativeBuildError as error:
                    report['failures'].append(dict(group=name, error=str(error), directory=str(error.directory)))
                except Exception as error:
                    report['failures'].append(dict(group=name, error=str(error)))
        if report['failures']:
            report.update(status='native_failed', parent_exit=1)
            return report
        blocks = []
        for unit in units:
            for row in results[unit.name]['blocks']:
                blocks.append(ImageBlock(row['start'], row['data'], row['owner'], row['role']))
        for row in resource_result['blocks']:
            if row['end'] != row['start'] + len(row['data']):
                raise ValueError('actual typed resource block extent differs')
            blocks.append(ImageBlock(row['start'], row['data'], row['owner'], row['role']))
        # 完整镜像要求整个地址空间连续覆盖，并为每个地址指定唯一来源。
        gaps = find_gaps(blocks)
        report['uncovered'] = [dict(start=gap.start, end=gap.end) for gap in gaps]
        if gaps:
            report.update(status='incomplete', parent_exit=2)
            return report
        image = assemble_complete(blocks)
        with (target / 'SANGO.bin').open('xb') as stream:
            stream.write(image)
        report.update(status='BIN_generated', parent_exit=0, complete_ROM=True, image_bytes=len(image),
            code_bytes=sum(unit.instruction_bytes for unit in units),
            typed_DATA_bytes=resource_result['coverage']['generated_bytes'],
            instruction_count=sum(len(unit.rows) for unit in units), physical_owner_blocks=len(blocks))
        if copier_header is not None:
            packed = interleave_smd(image, copier_header)
            with (target / 'SANGO.smd').open('xb') as stream:
                stream.write(packed)
            report.update(status='BIN_and_SMD_generated', smd_bytes=len(packed))
        else:
            report['SMD_boundary'] = 'provide copier-header fields to generate an SMD image'
        return report
    except Exception as error:
        report.update(status='integration_failed', parent_exit=1, error=str(error))
        raise
    finally:
        with (target / 'receipt.json').open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write('\n')


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True,
        help='assembly source directory containing src/m68k and src/z80')
    parser.add_argument('--layout-root', type=Path, required=True,
        help='pure geometry directory with manifest.json and fourteen address/size layout files')
    parser.add_argument('--resource-root', type=Path, required=True,
        help='explicit sole owned resources/{images,audio,data} root for all 128 typed source IDs')
    parser.add_argument('--m68k-tools', type=Path, required=True)
    parser.add_argument('--z80-tools', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='absent dedicated directory inside source workspace')
    parser.add_argument('--copier-header-fields', type=Path,
        help='optional JSON fields for the 512-byte SMD file header')
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args(argv)
    try:
        report = build_assembly(args.source_root, args.layout_root, args.resource_root, args.output,
            args.m68k_tools, args.z80_tools, workers=args.workers, copier_header_fields=args.copier_header_fields)
    except (OSError, ValueError, TypeError, KeyError, RuntimeError) as error:
        parser.exit(1, 'Assembly build stopped: ' + str(error) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report['parent_exit']


if __name__ == '__main__':
    raise SystemExit(main())
