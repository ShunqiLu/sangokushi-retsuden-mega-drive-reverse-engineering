"""收集汇编、布局、资源编码器及调用方传入的资源文件快照。"""
from __future__ import annotations

import argparse
import ast
from collections import deque
import json
from pathlib import Path, PurePosixPath
import re
import sys

from .sources import ordinary_root
from ..high_level_rom.stage_sources import _snapshot_registration, _resource_snapshot_parts


FORMAT = 'g5510-independent-assembly-source-snapshot-v1'
LAYOUT_FORMAT = 'g5510-owned-assembly-layout-v1'
SEEDS = (
    'tools.reconstruction_delivery.media_catalog',
    'tools.high_level_rom.portrait_catalog',
    'tools.reconstructed_assembly', 'tools.reconstructed_assembly.__main__',
    'tools.reconstructed_assembly.build', 'tools.reconstructed_assembly.sources',
    'tools.reconstructed_assembly.stage_sources',
    'tools.high_level_rom.native', 'tools.high_level_rom.z80_coff',
    'tools.high_level_rom.image', 'tools.high_level_rom.resource_registry',
    'tools.high_level_rom.copier_header',
    'tools.save_data.save_format',
    'tools.save_data.named_campaign', 'tools.save_data.campaign_cli',
    'tools.save_data.campaign_packets',
    'tools.save_data.campaign_orders',
)
# 这里列出构建和公开工具共享的配置与说明。
STATIC_DATA = ('tools/high_level_rom/resource_geometry.json',
    'tools/high_level_rom/text_sources/glyphs_lower.json',
    'tools/high_level_rom/text_sources/glyphs_upper.json',
    'tools/high_level_rom/resource_sources/copier_header.json',
    'tools/reconstructed_game/examples/entry_capture.example.json',
    'tools/reconstructed_game/examples/entry_capture.audio.example.json')
STATIC_DOCS = ('tools/reconstructed_assembly/README.md',
    'tools/high_level_rom/README_READABLE_TEXT.md',
    'tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.md',
    'tools/high_level_rom/README_AI_POLICY_SOURCES.md',
    'tools/high_level_rom/README_AI_SELECTION_SOURCES.md',
    'tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.md',
    'tools/high_level_rom/README_PORTRAIT_CATALOG.md',
    'tools/high_level_city_officer/README_SCENE_ORDERS.md',
    'tools/high_level_city_officer/README_SCENE_TRANSPORT.md',
    'tools/save_data/README.md',
    'tools/save_data/README_NAMED_CAMPAIGN.md',
    'tools/save_data/README_CAMPAIGN_PACKETS.md',
    'tools/save_data/README_CAMPAIGN_ORDERS.md',
    'tools/reconstruction_delivery/README_MEDIA_CATALOG.md',
    'tools/reconstructed_assembly/README_SOURCE_SNAPSHOT.md',
    'tools/high_level_rom/README_TITLE_TILE_MEDIA.md',
    'tools/reconstruction_acceptance/README_ENTRY_MONITOR.md',
    'tools/reconstruction_acceptance/README_ENTRY_CAPTURE_STORE.md',
    'tools/reconstruction_acceptance/README_AUDIO_ENTRY_CAPTURE.md',
    'tools/reconstruction_acceptance/README_Z80_ENTRY_CAPTURE.md',
    'tools/reconstruction_acceptance/README_ENTRY_CAPTURE_CATALOG.md',
    'tools/reconstruction_acceptance/README_M68K_ENTRY_CAPTURE.md',
    'tools/reconstruction_acceptance/README_PRE_CALL_CAPTURE_CATALOG.md',
    'tools/reconstruction_acceptance/README_PRE_CALL_SOURCE_VIEWS.md',
    'tools/reconstruction_acceptance/README_M68K_PRE_CALL_CAPTURE.md',
    'tools/reconstructed_game/README_ENTRY_CAPTURE.md')
BARE_IMPORT_ALIASES = {
    'tools.audio_sequences.rhythm': {'audio_formats': 'tools.audio_formats.audio_formats'},
}
EXCLUDED_COMPONENTS = frozenset(('analysis', 'build', 'generated', 'tests', '__pycache__',
    'private', 'evidence', 'draft', 'source_snapshots'))
RESOURCE_KEYS = ('id', 'codec', 'source', 'own_source', 'role', 'chain')
ROOT_README = '''# 汇编源码

本版使用 GNU 68000 和 Z80 汇编描述程序，地址布局定义各组指令范围。
构建参数见 tools/reconstructed_assembly/README.md，编辑入口见 EDITING.md。
素材来自构建时指定的目录；PNG 和结构化 JSON 由登记的编码器处理。
'''


class AssemblySnapshotError(ValueError):
    """An explicit source/snapshot boundary could not be satisfied."""


def _relative(value, suffix=None):
    if type(value) is not str or '\\' in value:
        raise AssemblySnapshotError('plain relative source path required')
    path = PurePosixPath(value)
    if (not path.parts or path.is_absolute() or '/'.join(path.parts) != value
            or any(part in ('.', '..') or part.endswith('.')
                or not re.fullmatch(r'[A-Za-z0-9_.-]+', part)
                or re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part)
                for part in path.parts)
            or suffix is not None and path.suffix != suffix
            or any(part in EXCLUDED_COMPONENTS for part in path.parts[:-1])):
        raise AssemblySnapshotError('unsafe/historical source path refused: ' + value)
    if path.suffix == '.py' and (path.name.startswith(('test', 'validate', 'accept_')) or path.name == 'conftest.py'):
        raise AssemblySnapshotError('test source is not assembly build authority')
    return path.as_posix()


def _read(root, relative, suffix=None):
    relative = _relative(relative, suffix)
    path = root.joinpath(*PurePosixPath(relative).parts)
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise AssemblySnapshotError('source through reparse point refused: ' + relative)
        if ancestor == root:
            break
    if not path.is_file() or not path.resolve(strict=True).is_relative_to(root) or path.stat().st_size > 20_000_000:
        raise AssemblySnapshotError('bounded ordinary declared source required: ' + relative)
    with path.open('rb') as stream:
        raw = stream.read(20_000_001)
    if len(raw) > 20_000_000:
        raise AssemblySnapshotError('source grew past declared bound: ' + relative)
    return raw


def _tree(raw, path):
    try:
        return ast.parse(raw.decode('utf-8-sig'), filename=path)
    except (ValueError, SyntaxError, UnicodeError) as error:
        raise AssemblySnapshotError('declared source cannot be parsed: ' + path) from error


def _registration(root):
    relative = 'tools/high_level_rom/resource_registry.py'
    assignments = [node for node in _tree(_read(root, relative, '.py'), relative).body
        if isinstance(node, ast.Assign) and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'RESOURCE_SPECS']
    if len(assignments) != 1 or not isinstance(assignments[0].value, ast.Tuple):
        raise AssemblySnapshotError('one fixed resource registration is required')
    result = []
    for node in assignments[0].value.elts:
        if (not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name)
                or node.func.id != 'ResourceSpec' or len(node.args) != len(RESOURCE_KEYS) or node.keywords):
            raise AssemblySnapshotError('literal complete resource declaration required')
        row = dict(zip(RESOURCE_KEYS, (ast.literal_eval(value) for value in node.args)))
        if any(type(value) is not str or not value for value in row.values()):
            raise AssemblySnapshotError('nonempty literal resource fields required')
        result.append(row)
    if len(result) != 128 or len({row['id'] for row in result}) != len(result):
        raise AssemblySnapshotError('all 128 unique registered resources required')
    return tuple(result)


def _locate(root, module):
    if type(module) is not str or not re.fullmatch(r'tools(?:\.[A-Za-z_]\w*)*', module):
        raise AssemblySnapshotError('explicit tools source module required')
    path = root.joinpath(*module.split('.'))
    if path.with_suffix('.py').is_file():
        return path.with_suffix('.py').relative_to(root).as_posix(), False
    if (path / '__init__.py').is_file():
        return (path / '__init__.py').relative_to(root).as_posix(), True
    return None, path.is_dir()


def _imports(root, module, is_package, tree):
    package = module if is_package else module.rpartition('.')[0]
    local, external, unresolved = set(), set(), []
    for node in ast.walk(tree):
        requested = []
        if isinstance(node, ast.Import):
            requested = [item.name for item in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                parts = package.split('.')
                if node.level > len(parts):
                    unresolved.append(dict(importer=module, line=node.lineno, reason='relative import escapes source'))
                    continue
                base = '.'.join(parts[:len(parts) - node.level + 1])
                base += ('.' + node.module) if node.module else ''
            else:
                base = node.module or ''
            requested = [base]
            if base == 'tools' or base.startswith('tools.'):
                for item in node.names:
                    if item.name != '*':
                        child = base + '.' + item.name
                        relative, exists = _locate(root, child)
                        if relative is not None or exists:
                            requested.append(child)
        elif isinstance(node, ast.Call):
            name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else None
            if name in ('import_module', '__import__'):
                if node.args and isinstance(node.args[0], ast.Constant) and type(node.args[0].value) is str:
                    requested = [node.args[0].value]
                else:
                    unresolved.append(dict(importer=module, line=node.lineno,
                        reason='nonliteral dynamic import has no independent assembly authority'))
        for name in requested:
            if name == 'tools' or name.startswith('tools.'):
                relative, exists = _locate(root, name)
                if relative is None and not exists:
                    unresolved.append(dict(importer=module, line=node.lineno, module=name,
                        reason='actual declared assembly/codec import missing'))
                else:
                    local.add(name)
            elif name in BARE_IMPORT_ALIASES.get(module, {}):
                local.add(BARE_IMPORT_ALIASES[module][name])
            elif name and name != '__future__':
                external.add(name.split('.')[0])
    return sorted(local), sorted(external), unresolved


def _forbidden(module):
    if module == 'tools.reconstructed_game' or module.startswith('tools.reconstructed_game.'):
        return True
    if module in ('tools.high_level_rom.build', 'tools.high_level_rom.code_registry',
            'tools.high_level_rom.runtime_source_catalog') or module.startswith('tools.high_level_audio_engine'):
        return True
    leaf = module.rsplit('.', 1)[-1]
    return module.startswith('tools.high_level_') and (leaf.startswith(('business_', 'compiler_'))
        or leaf in ('compiler', 'compiler_common', 'target'))


def _add(files, authority, relative, raw):
    relative = _relative(relative)
    if type(raw) is not bytes or relative.casefold() in authority:
        raise AssemblySnapshotError('duplicate or non-byte source authority: ' + relative)
    files[relative] = raw
    authority.add(relative.casefold())


def snapshot_assembly_tree(project_root, *, resource_snapshot: tuple[dict, dict]) -> tuple[dict, dict[str, bytes]]:
    """返回源码清单及文件内容，资源沿用调用方提供的字节。"""
    root = ordinary_root(Path(project_root), 'project_root')
    registration = _snapshot_registration(_registration(root))
    metadata, resource_files = _resource_snapshot_parts(resource_snapshot, registration)
    resource_ids = [row['id'] for row in registration]
    files, authority = {}, set()
    for relative, raw in resource_files.items():
        _add(files, authority, relative, raw)
    if 'scene-sources.json' not in files:
        raise AssemblySnapshotError('the same shared relocatable Scene manifest bytes are required')
    for row in metadata['resources']:
        if row.get('path') not in files or row.get('bytes') != len(files[row['path']]):
            raise AssemblySnapshotError('resource metadata must name its same captured bytes')
    resource_paths = tuple(files)
    geometry = json.loads(_read(root, 'tools/high_level_rom/resource_geometry.json', '.json').decode('utf-8-sig'))
    if (geometry.get('format') != 'g5510-ROM-independent-resource-geometry-v1'
            or set(geometry.get('contracts', {})) != set(resource_ids)):
        raise AssemblySnapshotError('registered typed resource geometry required')
    seeds = set(SEEDS) | {row['codec'] for row in registration}
    for contract in geometry['contracts'].values():
        if contract.get('adapter_module'):
            seeds.add(contract['adapter_module'])
    queue = deque(sorted(seeds))
    visited, modules, external, unresolved, namespaces = set(), [], set(), [], set()
    while queue:
        module = queue.popleft()
        if module in visited:
            continue
        visited.add(module)
        if _forbidden(module):
            unresolved.append(dict(module=module,
                reason='high-level business/compiler/runtime is not an assembly dependency; pure COFF extraction is mandatory'))
            continue
        relative, is_package = _locate(root, module)
        if relative is None:
            if is_package:
                namespaces.add(module)
            else:
                unresolved.append(dict(module=module, reason='fixed assembly/registered codec seed missing'))
            continue
        raw = _read(root, relative, '.py')
        _add(files, authority, relative, raw)
        local, third_party, problems = _imports(root, module, is_package, _tree(raw, relative))
        external.update(third_party)
        unresolved.extend(problems)
        modules.append(dict(module=module, path=relative, bytes=len(raw), imports=local,
            external_imports=third_party))
        queue.extend(local)
        for position in range(1, len(module.split('.'))):
            parent = '.'.join(module.split('.')[:position])
            relative_parent, exists = _locate(root, parent)
            if relative_parent is not None or exists:
                queue.append(parent)
    layout_path = 'tools/reconstructed_assembly/layout/manifest.json'
    layout_raw = _read(root, layout_path, '.json')
    layout = json.loads(layout_raw.decode('utf-8-sig'))
    if (layout.get('format') != LAYOUT_FORMAT or layout.get('image_size') != 0x100000
            or layout.get('resource_ids') != resource_ids or type(layout.get('groups')) is not list
            or len(layout['groups']) != 14):
        raise AssemblySnapshotError('complete independent assembly layout declaration required')
    _add(files, authority, layout_path, layout_raw)
    layout_files, assembly_files = [], []
    for row in layout['groups']:
        relative = 'tools/reconstructed_assembly/layout/' + _relative(row['layout'], '.json')
        _add(files, authority, relative, _read(root, relative, '.json'))
        layout_files.append(relative)
        for relative in row['sources']:
            if relative not in assembly_files:
                _add(files, authority, relative, _read(root, relative, '.s'))
                assembly_files.append(relative)
    if len(layout_files) != 14 or len(set(layout_files)) != 14 or len(assembly_files) != 15:
        raise AssemblySnapshotError('fourteen pure layouts and fifteen actual assembly sources required')
    for relative in STATIC_DATA:
        _add(files, authority, relative, _read(root, relative, '.json'))
    for relative in STATIC_DOCS:
        _add(files, authority, relative, _read(root, relative, '.md'))
    _add(files, authority, 'README.md', ROOT_README.encode('utf-8'))
    # 清单同时记录找到的依赖和需要调用方处理的缺项。
    standard = set(sys.stdlib_module_names) | {'__future__'}
    manifest = dict(metadata, format=FORMAT, status='assembly_source_snapshot_not_built_not_accepted',
        resource_snapshot_reused=True, resource_bytes_reread=False, resource_encoding_performed=False,
        own_source_closure_complete=not unresolved, unresolved=unresolved,
        fixed_seeds=sorted(seeds), modules=sorted(modules, key=lambda row: row['module']),
        namespace_packages=sorted(namespaces), source_file_count=len(files) - len(resource_files),
        source_file_BYTES=sum(len(raw) for name, raw in files.items() if name not in resource_files),
        captured_file_count=len(files), captured_BYTES=sum(map(len, files.values())),
        assembly_sources=assembly_files, instruction_layouts=layout_files, layout_manifest=layout_path,
        copier_header_fields='tools/high_level_rom/resource_sources/copier_header.json', scene_source_root='.',
        external_stdlib=sorted(external & standard), external_third_party=sorted(external - standard),
        resource_snapshot_paths=list(resource_paths), original_ROM_read=False, old_native_read=False,
        high_level_business_copied=False, high_level_runtime_catalog_copied=False,
        native_Z80_validator='tools.high_level_rom.z80_coff', compatible_validator_duplicate_retained=False,
        native_run=False, compiler_run=False, normal_API=False, game=False, fixture=False,
        test=False, hash=False, source_admission=False, syntax_check=False, final_delivery=False,
        )
    return manifest, files


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, required=True)
    resources = parser.add_mutually_exclusive_group(required=True)
    resources.add_argument('--resource-root', type=Path,
        help='local resource directory with resources and assets')
    resources.add_argument('--source-manifest', type=Path,
        help='scene manifest listing each resource root and its resource IDs')
    parser.add_argument('--asset-metadata-manifest', type=Path,
        help='explicit registered metadata required with --source-manifest')
    args = parser.parse_args(argv)
    if args.source_manifest is not None and args.asset_metadata_manifest is None:
        parser.error('--source-manifest requires explicit --asset-metadata-manifest')
    # 命令行从一个显式的本地资源入口生成快照。
    from ..high_level_rom.stage_sources import snapshot_resources
    registration = _registration(ordinary_root(args.project_root, 'project_root'))
    shared = snapshot_resources(args.resource_root, registration,
        source_manifest=args.source_manifest, asset_metadata_manifest=args.asset_metadata_manifest)
    manifest, unused_files = snapshot_assembly_tree(args.project_root, resource_snapshot=shared)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0 if manifest['own_source_closure_complete'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
