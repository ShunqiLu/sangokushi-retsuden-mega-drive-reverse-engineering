"""Prepare a bounded own-source project, not a final delivery or native build.

The source authority is the fixed code/resource/runtime registrations, followed by
recursive Python AST imports. No directory-wide copy, test discovery, private
census, reference ROM, assembly, object, or compilation output is an input.
An explicit host-chip source/license allowlist accompanies the runtime as an
external dependency; it is not reconstructed original game CODE.
Resources require an explicit own resource root; research analysis defaults
are deliberately absent from the staged project and never used as fallback.
"""
from __future__ import annotations

import argparse
import ast
from collections import deque
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys

from .scene_manifest import SCENE_SOURCE_MANIFEST, scene_source_manifest_bytes


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FORMAT = 'g5510-independent-high-level-source-staging-v1'
ENGINE_MODULES = (
    'tools.reconstruction_delivery.media_catalog',
    'tools.high_level_rom.portrait_catalog',
    'tools.high_level_rom.stage_sources', 'tools.high_level_rom.build',
    'tools.high_level_rom.native', 'tools.high_level_rom.image',
    'tools.high_level_rom.code_registry', 'tools.high_level_rom.resource_registry',
    'tools.high_level_rom.resource_adapters', 'tools.high_level_rom.copier_header',
    'tools.high_level_rom.export_media',
    'tools.high_level_rom.publish_readable_overlay',
    'tools.reconstructed_game.hardware_profile',
    'tools.reconstructed_game.local_config',
    'tools.save_data.save_format',
    'tools.save_data.named_campaign', 'tools.save_data.campaign_cli',
    'tools.save_data.campaign_packets',
    'tools.save_data.campaign_orders',
    'tools.high_level_rom.runtime_source_catalog',
    'tools.high_level_audio_engine.compiler', 'tools.high_level_audio_engine.target',
    'tools.high_level_audio_engine.build_ymfm',
    'tools.high_level_scene_flows.menu_build',
    'tools.high_level_scene_flows.decision_build',
    'tools.high_level_scene_flows.lifecycle_build',
    'tools.high_level_scene_flows.scene_object_build',
)
# Independent reference/case-preparation development APIs stay in the working
# project, not the product seed set. Actual optional App capture dependencies
# still enter through their real imports; unknown dynamic loaders stay refused.
HOST_RUNTIME_MODULES = ('tools.high_level_main_flows.runtime',
                        'tools.reconstructed_game.__main__')
RUNTIME_SOURCE_CATALOG = 'tools/high_level_rom/runtime_source_catalog.py'
STATIC_DATA = (
    'tools/high_level_rom/text_sources/glyphs_lower.json',
    'tools/high_level_rom/text_sources/glyphs_upper.json',
    'tools/high_level_rom/resource_geometry.json',
    'tools/high_level_rom/resource_sources/copier_header.json',
    'tools/reconstructed_game/config.schema.json',
    'tools/reconstructed_game/physical_inputs.schema.json',
    'tools/reconstructed_game/examples/application_hardware_inputs.json',
    'tools/reconstructed_game/examples/hardware_capacity_8192.json',
    'tools/reconstructed_game/examples/input_menu_to_campaign140.json',
    'tools/reconstructed_game/runtime.example.json',
    'tools/reconstructed_game/runtime.high-level.example.json',
    'tools/reconstructed_game/examples/ordered_restart_plan.example.json',
    'tools/reconstructed_game/examples/ordered_restart_cold_plan.example.json',
    'tools/reconstructed_game/examples/entry_capture.example.json',
    'tools/reconstructed_game/examples/entry_capture.audio.example.json',
    'tools/reconstructed_game/examples/entry_capture.pre-call.example.json',
)
STATIC_DOCUMENTATION = (
    'tools/high_level_scene_flows/README_SOURCE_ARTIFACT_CACHE.md',
    'docs/README_BATTLE_ENTRY_STEPS.md',
    'docs/README_CAMPAIGN_CONTROLS.md',
    'tools/high_level_gameplay_flow/README_SELECTED_COMMANDS.md',
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
    'docs/README_CAMPAIGN_MENU_STEPS.md',
    'docs/README_CONTROLLER_MENU_STEPS.md',
    'tools/reconstructed_game/README_SPEAKERS.md',
    'tools/high_level_rom/README_BUILD.md',
    'tools/reconstruction_delivery/README_MEDIA_CATALOG.md',
    'tools/high_level_rom/README_MEDIA_ALIASES.md',
    'tools/high_level_rom/README_GAME_SOURCE_STAGE.md',
    'tools/high_level_audio_engine/README_PORTABLE_BUILD.md',
    'tools/high_level_audio_engine/README_YMFM.md',
    'tools/high_level_audio_engine/README_RHYTHM_WZ.md',
    'tools/reconstructed_game/README.md',
    'tools/reconstructed_game/README_APPLICATION.md',
    'tools/reconstructed_game/README_CONSOLE.md',
    'tools/reconstructed_game/README_FRAME_PLAN.md',
    'tools/reconstructed_game/README_HARDWARE_INPUTS.md',
    'tools/reconstructed_game/README_HARDWARE_PROFILE.md',
    'tools/reconstructed_game/README_ORDERED_RESTARTS.md',
    'tools/reconstructed_game/README_ORDERED_COLD_PLAN.md',
    'tools/high_level_rom/README_TITLE_TILE_MEDIA.md',
    'tools/high_level_gameplay_flow/README_BATTLE_LIFECYCLE_STEPS.md',
    'tools/high_level_rom/README_SCENE_SOURCE_PUBLICATION.md',
    'tools/high_level_rom/README_COMPILED_CODE_DATA.md',
    'tools/high_level_rom/README_SOURCE_SNAPSHOTS.md',
    'tools/reconstructed_game/README_HIGH_LEVEL_NATIVE_ENTRY.md',
    'tools/reconstructed_game/README_LOCAL_CONFIG.md',
    'tools/reconstruction_acceptance/README_ENTRY_MONITOR.md',
    'tools/reconstruction_acceptance/README_ENTRY_CAPTURE_STORE.md',
    'tools/reconstruction_acceptance/README_AUDIO_ENTRY_CAPTURE.md',
    'tools/reconstruction_acceptance/README_Z80_ENTRY_CAPTURE.md',
    'tools/reconstruction_acceptance/README_ENTRY_CAPTURE_CATALOG.md',
    'tools/reconstruction_acceptance/README_M68K_ENTRY_CAPTURE.md',
    'tools/reconstruction_acceptance/README_PRE_CALL_CAPTURE_CATALOG.md',
    'tools/reconstruction_acceptance/README_PRE_CALL_SOURCE_VIEWS.md',
    'tools/reconstruction_acceptance/README_M68K_PRE_CALL_CAPTURE.md',
    'tools/reconstructed_game/README_ENTRY_CAPTURE.md',
)
# The host bridge is a separate chip dependency, not original game CODE.
# Preserve this fixed source/license set verbatim; never scan a vendor tree,
# copy a host binary, synthesize notices or replace the pinned provenance.
HOST_AUDIO_SOURCES = (
    'src/host_audio/ymfm_bridge.cpp',
    'src/third_party/ymfm/src/ymfm.h',
    'src/third_party/ymfm/src/ymfm_opn.h',
    'src/third_party/ymfm/src/ymfm_opn.cpp',
    'src/third_party/ymfm/src/ymfm_adpcm.h',
    'src/third_party/ymfm/src/ymfm_adpcm.cpp',
    'src/third_party/ymfm/src/ymfm_ssg.h',
    'src/third_party/ymfm/src/ymfm_ssg.cpp',
    'src/third_party/ymfm/src/ymfm_fm.h',
    'src/third_party/ymfm/src/ymfm_fm.ipp',
    'src/third_party/ymfm/LICENSE',
    'src/third_party/ymfm/README_G5510.md',
)
# A frozen legacy pure helper imports this sibling through its own sys.path.
# The mapping preserves that real layout without inventing a third-party dep.
BARE_IMPORT_ALIASES = {
    'tools.audio_sequences.rhythm': {'audio_formats': 'tools.audio_formats.audio_formats'},
}
EXCLUDED_COMPONENTS = {'analysis', 'build', 'generated', 'tests', '__pycache__',
                       'private', 'evidence', 'draft', 'source_snapshots'}
LIMITS = (
    'staging is not final delivery, native acceptance, CPU execution or natural behavior proof',
    'high-level runtime v2 requires a fresh own native build; legacy v1 authorities are not copied',
    'finite AST/intermediate business compilers are preserved, not upgraded to general Python compilers',
    'only registered typed JSON resources are staged; further friendly media/source organization remains work',
    'legacy pure helper dependencies retain dormant reference/default APIs; those are not build inputs',
    'analysis/reference/default resource paths are absent; builds must explicitly use this own resource root',
    'GNU toolchains and Python/declared third-party dependencies are external prerequisites, not copied objects',
    'host runtime linkage is staged as source; its finite caller proofs are not CPU or whole-game acceptance',
)


class StagingError(ValueError):
    """A registration, source dependency or fresh-path constraint failed."""


def _reparse(path):
    return (path.is_symlink() or getattr(path, 'is_junction', lambda: False)() or
            (path.exists() and bool(getattr(path.stat(), 'st_file_attributes', 0) &
                                   stat.FILE_ATTRIBUTE_REPARSE_POINT)))


def _root(value):
    path = Path(value).absolute()
    if not path.is_dir() or _reparse(path):
        raise StagingError('existing ordinary source directory required')
    return path.resolve(strict=True)


def _relative(value, suffix):
    if type(value) is not str or '\\' in value:
        raise StagingError('registered POSIX relative path required')
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ('', '.', '..') for part in path.parts) or path.suffix != suffix:
        raise StagingError('bounded registered relative source path required: ' + value)
    if any(part in EXCLUDED_COMPONENTS for part in path.parts[:-1]):
        raise StagingError('historical/research directory is not a staged authority: ' + value)
    if suffix == '.py' and (path.name.startswith(('test', 'validate', 'accept_')) or path.name == 'conftest.py'):
        raise StagingError('test/acceptance source is not a staged runtime authority: ' + value)
    return path.as_posix()


def _read(root, relative, suffix):
    relative = _relative(relative, suffix)
    path = root.joinpath(*PurePosixPath(relative).parts)
    if not path.is_file() or path.stat().st_size > 20_000_000:
        raise StagingError('bounded declared source missing: ' + relative)
    for ancestor in (path, *path.parents):
        if _reparse(ancestor):
            raise StagingError('source through reparse point refused: ' + relative)
        if ancestor == root:
            break
    if not path.resolve(strict=True).is_relative_to(root):
        raise StagingError('source leaves declared project root')
    return path.read_bytes()


def _tree(data, name):
    try:
        return ast.parse(data.decode('utf-8-sig'), filename=name)
    except (UnicodeError, SyntaxError, ValueError) as error:
        raise StagingError('source AST cannot be read: ' + name) from error


def _eval_registration(node, values):
    """Evaluate only the small fixed declaration syntax, never module code."""
    if isinstance(node, ast.Constant) and type(node.value) in (str, int, bool, type(None)):
        return node.value
    if isinstance(node, (ast.Tuple, ast.List)):
        items = [_eval_registration(item, values) for item in node.elts]
        return tuple(items) if isinstance(node, ast.Tuple) else items
    if isinstance(node, ast.Name) and node.id in values:
        return values[node.id]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _eval_registration(node.left, values) + _eval_registration(node.right, values)
    if isinstance(node, ast.Subscript):
        return _eval_registration(node.value, values)[_eval_registration(node.slice, values)]
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        args = [_eval_registration(arg, values) for arg in node.args]
        kwargs = {arg.arg: _eval_registration(arg.value, values) for arg in node.keywords if arg.arg is not None}
        if len(kwargs) != len(node.keywords):
            raise StagingError('expanded source registration is not supported')
        if node.func.id == '_files' and not kwargs and all(type(arg) is str for arg in args):
            return tuple('tools/high_level_' + args[0] + '/' + name + '.py' for name in args[1:])
        if node.func.id == 'SourceGroup':
            keys = ('name', 'package', 'source_files', 'adapter', 'expected_owned_bytes')
            row = dict(adapter='modern', expected_owned_bytes=0)
        elif node.func.id == 'ResourceSpec':
            keys = ('id', 'codec', 'source', 'own_source', 'role', 'chain')
            row = {}
        else:
            raise StagingError('unexpected registration constructor')
        if len(args) > len(keys) or set(kwargs) - set(keys) or set(keys[:len(args)]) & set(kwargs):
            raise StagingError('source registration arguments differ')
        row.update(zip(keys, args))
        row.update(kwargs)
        if set(row) != set(keys):
            raise StagingError('complete source registration required')
        return row
    raise StagingError('unsupported fixed registration expression: ' + type(node).__name__)


def _declarations(root):
    groups, resources, audio = None, None, None
    values = {}
    tree = _tree(_read(root, 'tools/high_level_rom/code_registry.py', '.py'), 'code_registry')
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ('EVENT_MATH', 'CYCLE', 'OFFICER', 'HEADS', 'SOURCE_GROUPS'):
                values[name] = _eval_registration(node.value, values)
    groups = values.get('SOURCE_GROUPS')
    for relative, wanted in (('tools/high_level_rom/resource_registry.py', 'RESOURCE_SPECS'),
                             ('tools/high_level_audio_engine/target.py', 'BUSINESS_MODULES')):
        for node in _tree(_read(root, relative, '.py'), relative).body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id == wanted:
                result = _eval_registration(node.value, {})
                if wanted == 'RESOURCE_SPECS':
                    resources = result
                else:
                    audio = result
    if not groups or not resources or not audio or len({row['name'] for row in groups}) != len(groups) or len({row['id'] for row in resources}) != len(resources):
        raise StagingError('unique complete fixed registrations required')
    # Optional glyph templates may precede geometry in the publication list.
    # The resource contract must not depend on that list's presentation order.
    geometry = json.loads(_read(root, 'tools/high_level_rom/resource_geometry.json', '.json').decode('utf-8'))
    if geometry.get('format') != 'g5510-ROM-independent-resource-geometry-v1' or set(geometry['contracts']) != {row['id'] for row in resources}:
        raise StagingError('resource registration/geometry IDs differ')
    return list(groups), list(resources), list(audio), geometry


def _module_name(relative):
    path = PurePosixPath(relative)
    parts = list(path.with_suffix('').parts)
    if parts[-1] == '__init__':
        parts.pop()
    return '.'.join(parts)


def _locate(root, module):
    if type(module) is not str or not re.fullmatch(r'tools(?:\.[A-Za-z_]\w*)*', module):
        raise StagingError('explicit tools module name required: ' + repr(module))
    base = root.joinpath(*module.split('.'))
    if base.with_suffix('.py').is_file():
        return base.with_suffix('.py').relative_to(root).as_posix(), False
    if (base / '__init__.py').is_file():
        return (base / '__init__.py').relative_to(root).as_posix(), True
    if base.is_dir():
        return None, True  # Namespace package; do not invent source.
    return None, False


def _imports(root, module, is_package, tree):
    local, external, unresolved, dynamic = set(), set(), [], []
    package = module if is_package else module.rpartition('.')[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            requested = [item.name for item in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                parts = package.split('.')
                if node.level > len(parts):
                    unresolved.append(dict(line=node.lineno, reason='relative import escapes source package'))
                    continue
                base = '.'.join(parts[:len(parts) - node.level + 1])
                base += ('.' + node.module) if node.module else ''
            else:
                base = node.module or ''
            requested = [base]
            if base.startswith('tools'):
                for item in node.names:
                    if item.name != '*':
                        child = base + '.' + item.name
                        relative, exists = _locate(root, child)
                        if relative is not None or exists:
                            requested.append(child)
        else:
            requested = []
        for name in requested:
            if name == 'tools' or name.startswith('tools.'):
                relative, exists = _locate(root, name)
                if relative is None and not exists:
                    unresolved.append(dict(line=node.lineno, module=name, reason='declared local import missing'))
                else:
                    local.add(name)
            elif name in BARE_IMPORT_ALIASES.get(module, {}):
                local.add(BARE_IMPORT_ALIASES[module][name])
            elif name and name != '__future__':
                external.add(name.split('.')[0])
        if isinstance(node, ast.Call):
            function = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else None
            if function in ('import_module', '__import__'):
                dynamic.append(dict(line=node.lineno, call=ast.unparse(node)))
    return sorted(local), sorted(external), unresolved, dynamic


def _module_reference(value):
    """One literal source-module identity, never embedded source or a glob."""
    if type(value) is not str:
        return None
    if re.fullmatch(r'tools(?:\.[A-Za-z_]\w*)+', value):
        return value
    if re.fullmatch(r'tools(?:/[A-Za-z_]\w*)+\.py', value):
        return _module_name(value)
    return None


def _path_declarations(tree):
    """Record literal module identities only; do not evaluate provider code."""
    declarations = {'__module_literals__': tuple(sorted(
        {_module_reference(part.value) for part in ast.walk(tree)
         if isinstance(part, ast.Constant)} - {None}))}
    for node in tree.body:
        if (not isinstance(node, ast.Assign) or len(node.targets) != 1
                or not isinstance(node.targets[0], ast.Name)):
            continue
        names = {_module_reference(part.value) for part in ast.walk(node.value)
                 if isinstance(part, ast.Constant)} - {None}
        if names:
            declarations[node.targets[0].id] = tuple(sorted(names))
    return declarations


def _runtime_contracts(root):
    """Read the finite reviewed provider catalog as data, without imports."""
    parsed = _tree(_read(root, RUNTIME_SOURCE_CATALOG, '.py'), RUNTIME_SOURCE_CATALOG)
    rows = [node for node in parsed.body if isinstance(node, ast.Assign)
            and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == 'DYNAMIC_IMPORT_CONTRACTS']
    if len(rows) != 1:
        raise StagingError('one explicit runtime source catalog is required')
    contracts = ast.literal_eval(rows[0].value)
    if type(contracts) is not dict:
        raise StagingError('finite runtime module contracts are required')
    for module, contract in contracts.items():
        if (_module_reference(module) != module or type(contract) is not dict
                or set(contract) != {'calls', 'targets', 'declarations', 'external_declarations'}
                or type(contract['calls']) is not tuple or not contract['calls']
                or any(type(call) is not str for call in contract['calls'])
                or type(contract['targets']) is not tuple or not contract['targets']
                or len(set(contract['targets'])) != len(contract['targets'])
                or any(_module_reference(target) != target for target in contract['targets'])
                or type(contract['declarations']) is not dict
                or type(contract['external_declarations']) is not dict):
            raise StagingError('complete literal runtime import contract differs: ' + str(module))
        for owner, declarations in contract['external_declarations'].items():
            if _module_reference(owner) != owner or type(declarations) is not dict:
                raise StagingError('explicit imported source-table owner required: ' + str(owner))
    return contracts


def _registered_audio_dynamic_targets(contracts, audio_sources):
    """Keep the typed Z80 adapter bound to the actual finite audio directory."""
    module = 'tools.reconstruction_acceptance.z80_case_inputs'
    if module not in contracts:
        return
    targets = {'tools.high_level_audio_engine.contexts'}
    for filename in audio_sources:
        relative = _relative('tools/high_level_audio_engine/' + filename, '.py')
        if filename.startswith('business_'):
            targets.add(_module_name(relative))
    if contracts[module]['targets'] != tuple(sorted(targets)):
        raise StagingError('reviewed typed Z80 dynamic targets differ from the actual audio registration')


def _snapshot_plan(project_root):
    root = _root(project_root)
    groups, resources, audio, geometry = _declarations(root)
    runtime_contracts = _runtime_contracts(root)
    _registered_audio_dynamic_targets(runtime_contracts, audio)
    seeds = set(ENGINE_MODULES) | set(HOST_RUNTIME_MODULES)
    source_files, dynamic_contracts = set(), {}
    for group in groups:
        package = 'tools.' + group['package']
        if group['adapter'] != 'pilot':
            seeds.add(package + '.target')
        compiler = package + ('.compiler_common'
            if group['adapter'] in ('modern', 'modules', 'preparation_fields') else '.compiler')
        seeds.add(compiler)
        for relative in group['source_files']:
            source_files.add(_relative(relative, '.py'))
            seeds.add(_module_name(relative))
        if group['adapter'] == 'modules':
            declared = []
            for relative in group['source_files']:
                leaf = PurePosixPath(relative).stem
                if not leaf.startswith('business_') or _module_name(relative).rpartition('.')[0] != package:
                    raise StagingError('dynamic family must have explicit own business source')
                declared.append(package + '.compiler_' + leaf.removeprefix('business_'))
            seeds.update(declared)
            dynamic_contracts[compiler] = declared
    dynamic_contracts['tools.high_level_rom.code_registry'] = sorted(seed for seed in seeds if seed.rsplit('.', 1)[-1] in ('compiler', 'compiler_common', 'target'))
    for name in audio:
        relative = _relative('tools/high_level_audio_engine/' + name, '.py')
        source_files.add(relative)
        seeds.add(_module_name(relative))
    for spec in resources:
        seeds.add(spec['codec'])
        adapter = geometry['contracts'][spec['id']].get('adapter_module')
        if adapter:
            seeds.add(adapter)
    queued = deque(sorted(seeds))
    seen, files, modules, external, unresolved, namespaces = set(), {}, [], set(), [], set()
    while queued:
        module = queued.popleft()
        if module in seen:
            continue
        seen.add(module)
        relative, is_package = _locate(root, module)
        if relative is None:
            if not is_package:
                unresolved.append(dict(module=module, reason='fixed seed module missing'))
            else:
                namespaces.add(module)
            continue
        try:
            raw = _read(root, relative, '.py')
        except StagingError as error:
            unresolved.append(dict(module=module, reason=str(error)))
            continue
        files[relative] = raw
        parsed = _tree(raw, relative)
        local, other, problems, dynamic = _imports(root, module, is_package, parsed)
        external.update(other)
        unresolved.extend(dict(problem, importer=module) for problem in problems)
        if module in runtime_contracts:
            contract = runtime_contracts[module]
            external_changed = []
            for owner, declarations in contract['external_declarations'].items():
                owner_relative, unused_is_package = _locate(root, owner)
                if owner_relative is None:
                    external_changed.append(owner)
                    continue
                owner_tree = _tree(_read(root, owner_relative, '.py'), owner_relative)
                if _path_declarations(owner_tree) != declarations:
                    external_changed.append(owner)
                local.append(owner)
            if (tuple(row['call'] for row in dynamic) != contract['calls']
                    or _path_declarations(parsed) != contract['declarations'] or external_changed):
                unresolved.append(dict(module=module,
                    reason='reviewed dynamic import calls/literal module declarations changed',
                    changed_imported_source_tables=external_changed))
            else:
                dynamic_contracts[module] = list(contract['targets'])
        if dynamic and module not in dynamic_contracts:
            unresolved.append(dict(module=module, reason='runtime dynamic import has no fixed declaration', calls=dynamic))
        modules.append(dict(module=module, path=relative, bytes=len(raw), imports=local,
                            external_imports=other, runtime_dynamic_imports=dynamic,
                            explicit_dynamic_targets=dynamic_contracts.get(module, [])))
        queued.extend(local)
        queued.extend(dynamic_contracts.get(module, []))
        # A package initializer can itself import required runtime helpers.
        for n in range(1, len(module.split('.'))):
            parent = '.'.join(module.split('.')[:n])
            parent_relative, package_exists = _locate(root, parent)
            if parent_relative is not None or package_exists:
                queued.append(parent)
    for relative in STATIC_DATA:
        files[relative] = _read(root, relative, '.json')
    for relative in STATIC_DOCUMENTATION:
        files[relative] = _read(root, relative, '.md')
    for relative in HOST_AUDIO_SOURCES:
        if relative in files:
            raise StagingError('host audio source competes with an existing authority: ' + relative)
        files[relative] = _read(root, relative, PurePosixPath(relative).suffix)
    stdlib = set(sys.stdlib_module_names) | {'__future__'}
    plan = dict(format=FORMAT, status='source_closure_planned_not_compiled',
                source_groups=groups, source_group_count=len(groups),
                declared_m68k_BYTES=sum(group['expected_owned_bytes'] for group in groups),
                audio_business_sources=audio, resource_registration=resources,
                host_runtime_entry_points=list(HOST_RUNTIME_MODULES),
                runtime_dynamic_source_catalog=RUNTIME_SOURCE_CATALOG,
                runtime_catalog_validation='exact call shapes and literal module identities; no provider execution',
                fixed_seeds=sorted(seeds), modules=sorted(modules, key=lambda row: row['module']),
                namespace_packages=sorted(namespaces), source_file_count=len(files),
                source_file_BYTES=sum(len(raw) for raw in files.values()),
                static_data=list(STATIC_DATA), registered_own_resources=len(resources),
                static_documentation=list(STATIC_DOCUMENTATION),
                static_host_audio_sources=[dict(path=relative, bytes=len(files[relative]))
                    for relative in HOST_AUDIO_SOURCES],
                host_audio_source_role='third_party_chip_and_host_bridge_not_original_game_CODE',
                host_audio_dependency_source_only_not_built_or_installed=True,
                host_audio_native_binary_copied=False, host_audio_build_tools_installed=False,
                declared_legacy_bare_import_aliases=BARE_IMPORT_ALIASES,
                external_stdlib=sorted(external & stdlib),
                external_third_party=sorted(external - stdlib), unresolved=unresolved,
                own_source_closure_complete=not unresolved,
                generation_authority='fixed code/resource/runtime registrations and recursive source AST imports',
                no_directory_wide_copy=True, analysis_not_staged=True,
                resource_root_required=True, original_ROM_read=False, native_run=False,
                CPU_run=False, final_delivery=False, new_behavioral_acceptance_BYTES=0,
                limits=list(LIMITS))
    return plan, files


def plan_sources(project_root=PROJECT_ROOT):
    """Read declared sources/data and the host allowlist; never compile or run GNU."""
    return _snapshot_plan(project_root)[0]


def _fresh(value, inputs):
    path = Path(value).absolute()
    raw = str(path)
    if raw.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in raw[2:]:
        raise StagingError('UNC/device/alternate-stream output refused')
    for ancestor in (path, *path.parents):
        if _reparse(ancestor):
            raise StagingError('output through reparse point refused')
    path = path.resolve(strict=False)
    if path == Path(path.anchor) or path.exists() or any(path.is_relative_to(root) or root.is_relative_to(path) for root in inputs):
        raise StagingError('fresh dedicated staging output, separate from inputs, required')
    return path


def _snapshot_registration(resource_registration):
    if type(resource_registration) not in (list, tuple) or len(resource_registration) != 128:
        raise StagingError('all128 explicit own-resource registrations required')
    rows, ids = [], set()
    for row in resource_registration:
        if (type(row) is not dict or set(row) != {'id', 'codec', 'source', 'own_source', 'role', 'chain'}
                or any(type(value) is not str or not value for value in row.values())
                or row['id'] in ids):
            raise StagingError('unique complete explicit own-resource registration required')
        _relative(row['own_source'], '.json')
        ids.add(row['id'])
        rows.append(dict(row))
    return rows


def _snapshot_resource_roots(resource_root, registration, source_manifest):
    """Select one explicit payload root per ID; never assign overlay priority."""
    from .media_sources import loads
    if (resource_root is None) == (source_manifest is None):
        raise StagingError('choose exactly one explicit resource root or Scene source manifest')
    expected = {row['id'] for row in registration}
    if source_manifest is None:
        own = _root(resource_root)
        return {ident: own for ident in expected}, None
    path = Path(source_manifest).absolute()
    parent = _root(path.parent)
    fields = loads(_read(parent, _relative(path.name, '.json'), '.json'))
    if (type(fields) is not dict or set(fields) != {'format', 'roots'}
            or fields['format'] != 'g5510-explicit-scene-source-roots-v1'
            or type(fields['roots']) is not list or not fields['roots']):
        raise StagingError('exact explicit multi-root Scene source manifest required')
    selected = {}
    for row in fields['roots']:
        if (type(row) is not dict or set(row) != {'path', 'ids'}
                or type(row['path']) is not str or not row['path']
                or type(row['ids']) is not list or not row['ids']):
            raise StagingError('explicit root path and nonempty resource ID list required')
        source = Path(row['path'])
        own = _root(source if source.is_absolute() else parent / source)
        for ident in row['ids']:
            if type(ident) is not str or ident not in expected or ident in selected:
                raise StagingError('unknown or competing multi-root resource authority')
            selected[ident] = own
    if set(selected) != expected:
        raise StagingError('all128 registered IDs must have exactly one explicit source root')
    return selected, str((parent / path.name).resolve(strict=True))


def _snapshot_asset_metadata(path, registration, resource_rows):
    """Read explicit geometry/member metadata, never an alternative payload."""
    from .media_sources import loads
    path = Path(path).absolute()
    parent = _root(path.parent)
    raw = _read(parent, _relative(path.name, '.json'), '.json')
    fields = loads(raw)
    if (type(fields) is not dict
            or fields.get('format') != 'g5510-build-connected-media-publication-v1'
            or type(fields.get('resources')) is not list
            or fields.get('registered_resources') != len(registration)):
        raise StagingError('explicit complete asset metadata manifest required')
    by_id = {}
    required = {'id', 'source', 'role', 'external_graph', 'members',
        'physical_spans', 'confidence', 'physical_BYTES'}
    for row in fields['resources']:
        if (type(row) is not dict or set(row) != required or type(row['id']) is not str
                or row['id'] in by_id):
            raise StagingError('one complete asset metadata row per registered ID required')
        by_id[row['id']] = row
    if set(by_id) != {row['id'] for row in registration}:
        raise StagingError('asset metadata and selected resource IDs differ')
    for spec, captured in zip(registration, resource_rows):
        row = by_id[spec['id']]
        spans = row['physical_spans']
        if (row['source'] != spec['own_source'] or row['role'] != spec['role']
                or type(row['external_graph']) is not bool
                or row['external_graph'] != bool(captured['external_media_members'])
                or row['members'] != captured['external_media_members']
                or type(row['confidence']) is not str or not row['confidence']
                or type(spans) is not list
                or any(type(span) not in (list, tuple) or len(span) != 2
                    or any(type(value) is not int for value in span)
                    or not 0 <= span[0] < span[1] <= 0x100000 for span in spans)
                or type(row['physical_BYTES']) is not int
                or row['physical_BYTES'] != sum(end-start for start, end in spans)):
            raise StagingError('explicit asset metadata differs from actual selected resource: ' + spec['id'])
    return fields, raw, str((parent / path.name).resolve(strict=True))


def snapshot_resources(resource_root: Path | None, resource_registration: list | tuple, *,
        source_manifest: Path | None = None,
        asset_metadata_manifest: Path | None = None) -> tuple[dict, dict[str, bytes]]:
    """Read each registered own resource/member once, without publishing.

    Returned paths are relative to a future package root. The same immutable
    bytes objects can be shared by high-level and assembly source snapshots.
    This preserves staging's transport/path checks, not codec/game acceptance.
    """
    registration = _snapshot_registration(resource_registration)
    roots, manifest_source = _snapshot_resource_roots(resource_root, registration, source_manifest)
    if source_manifest is not None and asset_metadata_manifest is None:
        raise StagingError('multi-root publication needs an explicit asset metadata manifest; no lookup fallback')
    from .media_sources import FORMAT as MEDIA_FORMAT, describe, loads, member_path
    files, resource_rows, authority_paths = {}, [], set()
    external_member_count = 0
    for spec in registration:
        own = roots[spec['id']]
        relative = _relative(spec['own_source'], '.json')
        if relative.casefold() in authority_paths:
            raise StagingError('duplicate staging path authority: ' + relative)
        raw = _read(own, relative, '.json')
        try:
            fields = loads(raw)
        except (UnicodeError, ValueError) as error:
            raise StagingError('own typed resource JSON malformed: ' + relative) from error
        if type(fields) is not dict:
            raise StagingError('own typed resource object required: ' + relative)
        files[relative] = raw
        authority_paths.add(relative.casefold())
        external_members = describe(fields, spec['id']) if fields.get('format') == MEDIA_FORMAT else []
        for member in external_members:
            # Preserve the existing generator's canonical Windows-safe member
            # declaration check. No PNG pixels or typed payload is decoded.
            member_path(own, member['file'])
            member_relative = _relative(member['file'], Path(member['file']).suffix)
            if member_relative.casefold() in authority_paths:
                raise StagingError('duplicate external-media staging authority: ' + member_relative)
            files[member_relative] = _read(own, member_relative, Path(member_relative).suffix)
            authority_paths.add(member_relative.casefold())
            external_member_count += 1
        resource_rows.append(dict(id=spec['id'], path=relative, bytes=len(raw),
            external_media_members=external_members,
            authority='explicit own resource root, no research-path fallback'))
    asset_manifest = None
    metadata_source = None
    if external_member_count:
        asset_manifest = 'asset-source-manifest.json'
        if asset_manifest.casefold() in authority_paths:
            raise StagingError('external asset manifest competes with an existing authority')
        selected_metadata = (asset_metadata_manifest if asset_metadata_manifest is not None
            else next(iter(roots.values())) / asset_manifest)
        declarations, raw, metadata_source = _snapshot_asset_metadata(
            selected_metadata, registration, resource_rows)
        if manifest_source is not None:
            # This is a current composition manifest, not the old metadata
            # file pretending to own the new readable dialogue payload.
            by_id = {row['id']: row for row in declarations['resources']}
            declarations = dict(declarations,
                resources=[by_id[row['id']] for row in registration],
                scene_source_manifest=SCENE_SOURCE_MANIFEST, scene_source_root='.',
                source_composition=dict(
                    payload_authority='one explicit Scene-manifest root per registered ID',
                    input_scene_manifest=manifest_source,
                    input_asset_metadata_manifest=metadata_source,
                    metadata_not_payload_fallback=True),
                edited_display_audio_proven=False, final_delivery=False,
                build_requirement='Use this independent edition root; all128 resource payloads are captured locally')
            raw = (json.dumps(declarations, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
        files[asset_manifest] = raw
        authority_paths.add(asset_manifest.casefold())
    if SCENE_SOURCE_MANIFEST.casefold() in authority_paths:
        raise StagingError('Scene entry competes with an existing staged authority')
    resource_ids = [row['id'] for row in registration]
    files[SCENE_SOURCE_MANIFEST] = scene_source_manifest_bytes(tuple(resource_ids))
    return dict(resource_snapshot_format='g5510-explicit-own-resource-snapshot-v1',
        resource_ids=resource_ids, resources=resource_rows, registered_own_resources=len(resource_ids),
        external_media_member_count=external_member_count, asset_source_manifest=asset_manifest,
        scene_source_manifest=SCENE_SOURCE_MANIFEST, scene_source_root='.',
        input_scene_source_manifest=manifest_source,
        input_asset_metadata_manifest=metadata_source,
        resource_source_roots={row['id']:str(roots[row['id']]) for row in registration},
        media_member_paths_validated=True, media_graph_topology_validated=False,
        media_graph_validation='Complete references/pixels/typed fields are validated by resource generation, not staging'), files


def _resource_snapshot_parts(resource_snapshot, registration):
    """Check an in-memory transport contract, never reread resource files."""
    if (type(resource_snapshot) is not tuple or len(resource_snapshot) != 2
            or type(resource_snapshot[0]) is not dict or type(resource_snapshot[1]) is not dict):
        raise StagingError('explicit resource metadata/files snapshot tuple required')
    metadata, files = resource_snapshot
    expected_keys = {'resource_snapshot_format', 'resource_ids', 'resources', 'registered_own_resources',
        'external_media_member_count', 'asset_source_manifest', 'scene_source_manifest', 'scene_source_root',
        'input_scene_source_manifest', 'input_asset_metadata_manifest', 'resource_source_roots',
        'media_member_paths_validated', 'media_graph_topology_validated', 'media_graph_validation'}
    if (set(metadata) != expected_keys
            or metadata['resource_snapshot_format'] != 'g5510-explicit-own-resource-snapshot-v1'
            or metadata['resource_ids'] != [row['id'] for row in registration]
            or metadata['registered_own_resources'] != 128
            or metadata['scene_source_manifest'] != SCENE_SOURCE_MANIFEST
            or metadata['scene_source_root'] != '.'
            or metadata['media_member_paths_validated'] is not True
            or metadata['media_graph_topology_validated'] is not False
            or metadata['media_graph_validation'] != 'Complete references/pixels/typed fields are validated by resource generation, not staging'
            or type(metadata['resources']) is not list or len(metadata['resources']) != len(registration)):
        raise StagingError('complete resource snapshot metadata/ordered registration differs')
    if (type(metadata['resource_source_roots']) is not dict
            or set(metadata['resource_source_roots']) != {row['id'] for row in registration}
            or any(type(value) is not str or not Path(value).is_absolute()
                for value in metadata['resource_source_roots'].values())
            or any(value is not None and (type(value) is not str or not Path(value).is_absolute())
                for value in (metadata['input_scene_source_manifest'], metadata['input_asset_metadata_manifest']))):
        raise StagingError('complete explicit input root/metadata provenance required')
    paths, expected_files, count = set(), set(), 0
    for relative, raw in files.items():
        if type(relative) is not str or type(raw) is not bytes or not 0 < len(raw) <= 20_000_000:
            raise StagingError('bounded immutable resource snapshot member required')
        suffix = PurePosixPath(relative).suffix
        if suffix not in ('.json', '.png') or _relative(relative, suffix) != relative:
            raise StagingError('registered JSON/PNG resource snapshot member required')
        if relative.casefold() in paths:
            raise StagingError('duplicate case-insensitive resource snapshot authority')
        paths.add(relative.casefold())
    for spec, row in zip(registration, metadata['resources']):
        if (type(row) is not dict or set(row) != {'id', 'path', 'bytes', 'external_media_members', 'authority'}
                or row['id'] != spec['id'] or row['path'] != spec['own_source']
                or row['authority'] != 'explicit own resource root, no research-path fallback'
                or type(row['external_media_members']) is not list
                or row['path'] not in files or type(row['bytes']) is not int
                or row['bytes'] != len(files[row['path']])):
            raise StagingError('resource snapshot row/current explicit registration differs')
        if row['path'] in expected_files:
            raise StagingError('duplicate resource snapshot row authority')
        expected_files.add(row['path'])
        for member in row['external_media_members']:
            if (type(member) is not dict or type(member.get('file')) is not str
                    or member['file'] not in files or member['file'] in expected_files):
                raise StagingError('unique declared external-media snapshot member required')
            expected_files.add(member['file'])
            count += 1
    if type(metadata['external_media_member_count']) is not int or metadata['external_media_member_count'] != count:
        raise StagingError('resource snapshot external member count differs')
    manifest = 'asset-source-manifest.json' if count else None
    if metadata['asset_source_manifest'] != manifest:
        raise StagingError('resource snapshot external manifest contract differs')
    if manifest:
        if manifest in expected_files:raise StagingError('external manifest ownership conflict')
        expected_files.add(manifest)
    if SCENE_SOURCE_MANIFEST in expected_files:raise StagingError('Scene manifest ownership conflict')
    expected_files.add(SCENE_SOURCE_MANIFEST)
    if files.get(SCENE_SOURCE_MANIFEST) != scene_source_manifest_bytes(tuple(metadata['resource_ids'])):
        raise StagingError('captured Scene entry must refer only to this independent edition root')
    if set(files) != expected_files:
        raise StagingError('complete resource snapshot member set differs')
    return metadata, files


def _merge_resource_snapshot(plan, source_files, resource_snapshot):
    """Merge only already-read immutable authorities; never overwrite or fill."""
    if plan['unresolved']:
        raise StagingError('source closure has explicit unresolved dependencies: ' + json.dumps(plan['unresolved'], ensure_ascii=False))
    registration = _snapshot_registration(plan['resource_registration'])
    metadata, resource_files = _resource_snapshot_parts(resource_snapshot, registration)
    files, paths = {}, set()
    for original in (source_files, resource_files):
        for relative, raw in original.items():
            if type(relative) is not str or type(raw) is not bytes:
                raise StagingError('relative source name and immutable snapshot bytes required')
            if relative.casefold() in paths:
                raise StagingError('duplicate staging path authority: ' + relative)
            paths.add(relative.casefold())
            files[relative] = raw
    merged = dict(plan, **metadata, snapshot_file_count=len(files),
        snapshot_BYTES=sum(len(raw) for raw in files.values()))
    return merged, files


def snapshot_source_tree(project_root: Path, *, resource_snapshot: tuple[dict, dict[str, bytes]]) -> tuple[dict, dict[str, bytes]]:
    """Return current source AST closure plus one supplied resource snapshot.

    No media is reread, decoded or re-encoded. No directory is created. The
    caller can publish both source versions from the exact same resource bytes.
    """
    plan, source_files = _snapshot_plan(project_root)
    return _merge_resource_snapshot(plan, source_files, resource_snapshot)


def stage_sources(project_root, output, resource_root=None, *, source_manifest=None,
        asset_metadata_manifest=None):
    """Publish the same bounded source/resource authority from pure snapshots."""
    project = _root(project_root)
    plan, source_files = _snapshot_plan(project)
    if plan['unresolved']:
        raise StagingError('source closure has explicit unresolved dependencies: ' + json.dumps(plan['unresolved'], ensure_ascii=False))
    resources = snapshot_resources(resource_root, plan['resource_registration'],
        source_manifest=source_manifest, asset_metadata_manifest=asset_metadata_manifest)
    inputs = tuple({_root(value) for value in resources[0]['resource_source_roots'].values()})
    metadata_parent = resources[0]['input_asset_metadata_manifest']
    protected = (project, *inputs)
    if metadata_parent is not None:
        protected += (_root(Path(metadata_parent).parent),)
    target = _fresh(output, protected)
    plan, files = _merge_resource_snapshot(plan, source_files, resources)
    target.mkdir(parents=True)
    # Both source and media inputs were read before publication, once per
    # authority. The writer uses only the prepared immutable snapshots.
    for relative, raw in sorted(files.items()):
        path = target.joinpath(*PurePosixPath(relative).parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
    manifest = dict(plan, status='source_staged_not_native_not_final', stage_root=str(target),
        staged_files=[dict(path=name, bytes=len(raw)) for name, raw in sorted(files.items())],
        staged_file_count=len(files), staged_BYTES=sum(len(raw) for raw in files.values()),
        build_requirement='Run from stage root; pass --project-root stage_root and --resource-root stage_root explicitly',
        copier_header_fields='tools/high_level_rom/resource_sources/copier_header.json',
        no_reference_tree_present=True, no_old_binary_or_object_copied=True)
    with (target / 'source-stage-manifest.json').open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(manifest, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('plan', 'stage'))
    parser.add_argument('--project-root', type=Path, default=PROJECT_ROOT)
    resources = parser.add_mutually_exclusive_group()
    resources.add_argument('--resource-root', type=Path)
    resources.add_argument('--source-manifest', type=Path,
        help='explicit complete Scene multi-root manifest; no overlay precedence')
    parser.add_argument('--asset-metadata-manifest', type=Path,
        help='explicit registered geometry/member metadata; required with --source-manifest')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    if args.mode == 'stage':
        if (args.resource_root is None) == (args.source_manifest is None):
            parser.error('stage requires exactly one --resource-root or --source-manifest')
        if args.source_manifest is not None and args.asset_metadata_manifest is None:
            parser.error('--source-manifest requires explicit --asset-metadata-manifest')
        result = stage_sources(args.project_root, args.output, args.resource_root,
            source_manifest=args.source_manifest, asset_metadata_manifest=args.asset_metadata_manifest)
    else:
        if any(value is not None for value in (args.resource_root, args.source_manifest, args.asset_metadata_manifest)):
            parser.error('plan does not read resource source files')
        target = _fresh(args.output, (_root(args.project_root),))
        result = plan_sources(args.project_root)
        target.mkdir(parents=True)
        with (target / 'source-plan.json').open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
    print(json.dumps({key: result[key] for key in ('status', 'source_group_count', 'declared_m68k_BYTES', 'source_file_count', 'source_file_BYTES', 'registered_own_resources', 'own_source_closure_complete', 'unresolved', 'external_third_party', 'final_delivery')}, ensure_ascii=False))
    return 0 if result['own_source_closure_complete'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
