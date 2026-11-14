"""Explicit inputs for the two pending Z80 owners, never a CPU/test runner.

Source ASTs determine the real public entry and immutable context class. Saved
initial states and external/reference contracts remain caller-owned evidence.
No old fixture recipe is expanded, RAM filled, device made ready, or case run.
"""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass
import importlib
import json
from pathlib import Path
from types import FunctionType

from .pending_scope import PendingScope


FORMAT = 'g5510-z80-explicit-case-input-plan-v1'
SPEC_FORMAT = 'g5510-z80-case-specifications-v1'
STATE_FORMAT = 'g5510-z80-complete-initial-state-v1'
PACKAGE = 'tools.high_level_audio_engine'
CARRIERS = ('auxiliary_cursor', 'channel_cursor', 'conditions', 'count_and_data',
    'lookup_cursor', 'parameter_cursor', 'sample', 'stack_cursor')
CONTROL = ('pc_entry', 'interrupt_vector', 'refresh', 'iff1', 'iff2',
    'interrupt_mode', 'ei_deferred')
ALTERNATE = ('count_and_data', 'parameter_cursor', 'lookup_cursor')
MAX_TEXT_BYTES = 40_000_000


class Z80InputError(ValueError):
    """Explicit input/source ambiguity; not a recovered game result."""


def _require(condition, message):
    if not condition:
        raise Z80InputError(message)


def _uint(value, bits):
    _require(type(value) is int and 0 <= value < (1 << bits),
        'explicit unsigned ' + str(bits) + '-bit value required')
    return value


def _text(path):
    path = Path(path).resolve(strict=True)
    _require(path.is_file() and path.stat().st_size <= MAX_TEXT_BYTES,
        'bounded caller-named text file required: ' + str(path))
    return path.read_text(encoding='utf-8-sig')


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def _json(path):
    return json.loads(_text(path), object_pairs_hook=_pairs)


def _literal(tree, name):
    nodes = [row.value for row in tree.body if type(row) is ast.Assign
        and any(type(target) is ast.Name and target.id == name for target in row.targets)]
    _require(nodes, 'actual literal source directory missing: ' + name)
    values = [ast.literal_eval(node) for node in nodes]
    _require(all(value == values[0] for value in values),
        'conflicting source directory assignments: ' + name)
    return values[0]


def _module_path(project, module):
    _require(module.startswith(PACKAGE + '.') and all(part.isidentifier()
        for part in module.split('.')), 'only explicit audio package modules permitted')
    path = (project / (module.replace('.', '/') + '.py')).resolve(strict=True)
    _require(path.is_relative_to(project), 'source module escaped explicit project')
    return path


@dataclass(frozen=True)
class Z80EntryBinding:
    owner: str
    alias: str
    logical_address: int
    physical_address: int
    module: str
    function: str
    source: str
    source_line: int
    input_module: str
    input_class: str
    input_fields: tuple[tuple[str, str], ...]
    result_module: str
    result_class: str
    result_fields: tuple[tuple[str, str], ...]
    invocation: dict
    qualification: str = 'confirmed_current_source_definition_not_loaded_CodeType_or_reference_execution'


@dataclass(frozen=True)
class Z80InputPlan:
    entries: tuple[dict, ...]
    cases: tuple[dict, ...]
    excluded: tuple[dict, ...]
    authority_counts: tuple[int, ...]

    def to_dict(self):
        return dict(format=FORMAT, confidence='source_input_assembly_only_not_strict_acceptance',
            authority_counts=list(self.authority_counts),
            owners=2, named_entries=len(self.entries),
            supplied_cases=len(self.cases),
            cases_with_complete_saved_initial_inputs=sum(row['saved_initial_input_complete']
                for row in self.cases),
            entries=list(self.entries), cases=list(self.cases), excluded=list(self.excluded),
            game=False, audio_execution=False, CPU=False, fixture=False, compiler_API=False,
            native=False, hash=False, reference_executed=False, formal_new_CODE_bytes=0,
            strict_pending_unchanged=self.authority_counts[2])


def _context_schema(tree, name):
    classes = [row for row in tree.body if type(row) is ast.ClassDef and row.name == name]
    _require(len(classes) == 1, 'one actual immutable context class required: ' + name)
    node = classes[0]
    _require(any(type(row) is ast.Call and type(row.func) is ast.Name
        and row.func.id == 'dataclass' and any(key.arg == 'frozen'
            and type(key.value) is ast.Constant and key.value.value is True
            for key in row.keywords) for row in node.decorator_list),
        'actual frozen dataclass interface required: ' + name)
    result = []
    for row in node.body:
        if type(row) is ast.AnnAssign:
            _require(type(row.target) is ast.Name and type(row.annotation) is ast.Name
                and row.value is None and row.annotation.id in ('Byte', 'Word', 'Continuation'),
                'unsupported context field; no inferred ABI: ' + name)
            result.append((row.target.id, row.annotation.id))
    _require(result, 'actual context fields required: ' + name)
    return tuple(result)


def _entry_bindings(scope, project):
    """Read only the declared audio sources, not an all-project name search."""
    target_path = _module_path(project, PACKAGE + '.target')
    target = ast.parse(_text(target_path), filename=str(target_path))
    aliases = _literal(target, 'CALLEE_ADDRESSES')
    sources = _literal(target, 'BUSINESS_MODULES')
    _require(type(aliases) is dict and type(sources) is tuple,
        'current explicit audio alias/module directories required')
    contexts_path = _module_path(project, PACKAGE + '.contexts')
    contexts = ast.parse(_text(contexts_path), filename=str(contexts_path))
    found = {}
    for filename in sources:
        _require(type(filename) is str and '/' not in filename and '\\' not in filename
            and filename.endswith('.py'), 'literal local source filename required')
        if not filename.startswith('business_'):
            continue
        module = PACKAGE + '.' + filename[:-3]
        path = _module_path(project, module)
        tree = ast.parse(_text(path), filename=str(path))
        for node in tree.body:
            if type(node) is not ast.FunctionDef or node.name not in aliases:
                continue
            args = node.args
            _require(not args.posonlyargs and not args.kwonlyargs and args.vararg is None
                and args.kwarg is None and not args.defaults and len(args.args) == 2
                and tuple(row.arg for row in args.args) == ('state', 'inputs')
                and type(args.args[0].annotation) is ast.Name
                and args.args[0].annotation.id == 'AudioState'
                and type(args.args[1].annotation) is ast.Name
                and type(node.returns) is ast.Name,
                'entry ABI is not the actual two-argument typed audio contract: ' + node.name)
            input_name, result_name = args.args[1].annotation.id, node.returns.id
            for name in (input_name, result_name):
                imports = [alias for row in tree.body if type(row) is ast.ImportFrom
                    and row.module == 'contexts' and row.level == 1 for alias in row.names
                    if (alias.asname or alias.name) == name and alias.name == name]
                _require(len(imports) == 1, 'context must resolve to its actual direct owner: ' + name)
            _require(node.name not in found, 'ambiguous actual alias function: ' + node.name)
            found[node.name] = (module, path, node, input_name, result_name)
    rows = []
    audio = tuple(owner for owner in scope.owners if owner.architecture == 'z80')
    _require({row.key for row in audio} == {'z80:startup', 'z80:driver'},
        'the two distinct pending Z80 owner images required')
    for owner in audio:
        for entry in owner.entries:
            _require(entry.alias in found and entry.alias in aliases
                and entry.logical_address == aliases[entry.alias]
                and entry.physical_address == owner.start + entry.logical_address,
                'scope alias differs from current actual target/source: ' + entry.alias)
            module, path, node, input_name, result_name = found[entry.alias]
            if entry.alias == 'initialize_audio_workspace':
                invocation = dict(kind='cold_workspace_session',
                    module=PACKAGE + '.cold_workspace', owner='ColdWorkspaceSession', method='start',
                    requires=('same_Scene_SoundDevice', 'bound_AudioControlOwner',
                        'ColdWorkspacePlatform', 'actual_startup_kind_AudioFrameLease',
                        'original_38_byte_copy_authority'),
                    return_protocol='nonreturning_original_JP_HL_idle_not_RET',
                    raw_entry_call_permitted=False)
            elif entry.alias == 'initialize_audio_driver':
                invocation = dict(kind='driver_startup_session',
                    module=PACKAGE + '.driver_startup', owner='AudioDriverStartupSession', method='start',
                    requires=('same_Scene_SoundDevice', 'bound_AudioControlOwner',
                        'actual_installed_driver_kind_AudioFrameLease',
                        'explicit_irq_clock_hz_and_initial_timestamp', 'actual_finite_Im1ClockGrants'),
                    return_protocol='real_005F_wait_and_006F_boundary_not_ordinary_RET',
                    raw_entry_call_permitted=False)
            else:
                invocation = dict(kind='typed_context', module=module, owner=node.name,
                    parameters=('AudioState', input_name),
                    shared_stack='caller_supplied_actual_continuation_and_stack_bytes_no_host_push',
                    external_IM1_acceptance_required=(entry.alias == 'service_im1_interrupt'),
                    result_protocol='actual_context_result_or_original_Boundary_nonlocal_return',
                    raw_entry_call_permitted=True)
            input_fields = _context_schema(contexts, input_name)
            result_fields = _context_schema(contexts, result_name)
            _require(all(name in CARRIERS or (name, kind) == ('continuation', 'Continuation')
                for name, kind in input_fields), 'unmapped live input cell; no guessed carrier')
            rows.append(Z80EntryBinding(owner.key, entry.alias, entry.logical_address,
                entry.physical_address, module, node.name,
                path.relative_to(project).as_posix(), node.lineno, PACKAGE + '.contexts',
                input_name, input_fields, PACKAGE + '.contexts', result_name, result_fields, invocation))
    _require(len(rows) == len(aliases) == 109, 'all109 original named entries required')
    return tuple(rows)


def _path(value, base):
    _require(type(value) is str and value, 'explicit evidence path required')
    path = Path(value)
    _require(path.is_absolute() or base is not None,
        'relative evidence requires a caller-named specification file')
    return (path if path.is_absolute() else base / path).resolve(strict=True)


def _evidence(row, base):
    _require(type(row) is dict and set(row) == {'path', 'pointer', 'role'}
        and type(row['pointer']) is str and (not row['pointer'] or row['pointer'].startswith('/'))
        and type(row['role']) is str and row['role'], 'explicit path/pointer/role evidence required')
    path = _path(row['path'], base)
    _require(path.is_file(), 'evidence must be an existing caller-named file')
    return dict(path=str(path), pointer=row['pointer'], role=row['role'])


def _selected_json(evidence):
    value = _json(evidence['path'])
    for token in evidence['pointer'].split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        if type(value) is list:
            _require(token.isdecimal() and str(int(token)) == token, 'actual JSON array selector required')
            value = value[int(token)]
        else:
            _require(type(value) is dict and token in value, 'saved JSON selector does not exist')
            value = value[token]
    return value


def _initial(snapshot, snapshot_path):
    """Validate saved values only; never expand a fill/pattern recipe."""
    _require(type(snapshot) is dict and set(snapshot) == {'format', 'frame', 'alternate_AF',
        'alternate_group', 'control', 'memptr', 'sound_RAM', 'max_DATA_operations'}
        and snapshot['format'] == STATE_FORMAT, 'complete saved Z80 snapshot format required')
    frame = snapshot['frame']
    _require(type(frame) is dict and set(frame) == set(CARRIERS), 'all8 actual live Z80 carriers required')
    for name, value in frame.items():
        _uint(value, 8 if name in ('sample', 'conditions') else 16)
    _uint(snapshot['alternate_AF'], 16)
    alternate = snapshot['alternate_group']
    _require(type(alternate) is dict and set(alternate) == set(ALTERNATE), 'all3 actual alternate WORDs required')
    for value in alternate.values():
        _uint(value, 16)
    control = snapshot['control']
    _require(type(control) is dict and set(control) == set(CONTROL), 'all7 explicit audio control fields required')
    missing = ['initial.control.' + name for name, value in control.items() if value is None]
    for name in ('pc_entry', 'interrupt_vector', 'refresh'):
        if control[name] is not None:
            _uint(control[name], 16 if name == 'pc_entry' else 8)
    for name in ('iff1', 'iff2', 'ei_deferred'):
        _require(control[name] is None or type(control[name]) is bool, 'actual IFF/EI booleans required')
    _require(control['interrupt_mode'] is None or (type(control['interrupt_mode']) is int
        and control['interrupt_mode'] in (0, 1, 2)), 'actual interrupt mode required')
    if snapshot['memptr'] is None:
        missing.append('initial.memptr_WZ')
    else:
        _uint(snapshot['memptr'], 16)
    ram = snapshot['sound_RAM']
    _require(type(ram) is dict and set(ram) == {'path', 'bytes'} and ram['bytes'] == 8192,
        'one full8192-byte saved RAM file required, not a fill/patch recipe')
    ram_path = _path(ram['path'], Path(snapshot_path).parent)
    _require(ram_path.is_file() and ram_path.stat().st_size == 8192,
        'complete saved actual sound RAM must contain exactly8192 bytes')
    _require(type(snapshot['max_DATA_operations']) is int and snapshot['max_DATA_operations'] > 0,
        'explicit finite DATA operation budget required')
    return dict(snapshot, sound_RAM=dict(path=str(ram_path), bytes=8192)), missing


def assemble_z80_specs(scope, document=None, *, project_root):
    """Return serializable source bindings/real saved inputs without execution.

    ``document`` is None, an explicit manifest Path, or a dictionary whose
    evidence paths are absolute. Unavailable/partial states become named gaps;
    historical successes, recipes or a guessed ready device never fill them.
    """
    _require(type(scope) is PendingScope, 'exact pending scope required')
    project = Path(project_root).resolve(strict=True)
    _require(project.is_dir(), 'explicit current source project required')
    bindings = _entry_bindings(scope, project)
    by_key = {(row.owner, row.alias): row for row in bindings}
    base = None
    if document is None:
        specs = []
    else:
        if isinstance(document, (str, Path)):
            path = Path(document).resolve(strict=True)
            document, base = _json(path), path.parent
        _require(type(document) is dict and set(document) == {'format', 'cases'}
            and document['format'] == SPEC_FORMAT and type(document['cases']) is list,
            'explicit Z80 specification manifest required')
        specs = document['cases']
    cases, excluded, linked, identifiers = [], [], {}, set()
    for position, spec in enumerate(specs):
        try:
            _require(type(spec) is dict and set(spec) == {'id', 'owner', 'alias', 'logical_address',
                'invocation', 'initial_state', 'continuation', 'physical_stack', 'external_supplies',
                'independent_reference'}, 'complete explicit case specification fields required')
            identity = spec['id']
            _require(type(identity) is str and identity and identity not in identifiers, 'unique case id required')
            identifiers.add(identity)
            key = (spec['owner'], spec['alias'])
            _require(key in by_key, 'named entry outside current Z80 scope')
            binding = by_key[key]
            _require(type(spec['logical_address']) is int and spec['logical_address'] == binding.logical_address
                and spec['invocation'] == binding.invocation['kind'], 'actual entry/session invocation differs')
            initial_ref = _evidence(spec['initial_state'], base)
            snapshot, missing = _initial(_selected_json(initial_ref), initial_ref['path'])
            _require(snapshot['control']['pc_entry'] is None
                or snapshot['control']['pc_entry'] == binding.logical_address,
                'saved semantic entry is not the requested original alias')
            continuation = spec['continuation']
            _require(type(continuation) is dict and set(continuation) == {'image', 'expected_return_word'}
                and continuation['image'] == binding.owner.removeprefix('z80:'), 'actual named image continuation required')
            _uint(continuation['expected_return_word'], 16)
            stack_ref = _evidence(spec['physical_stack'], base)
            supplies = _evidence(spec['external_supplies'], base)
            reference = _evidence(spec['independent_reference'], base)
            if binding.invocation['kind'] != 'typed_context':
                missing.append('runtime.same_owner_actual_AudioFrameLease_and_source_copy_or_installation_proof')
            if binding.alias == 'service_im1_interrupt':
                missing.append('runtime.actual_IM1_acceptance_generation_epoch_and_interrupt_frame_owner')
            inputs = {name: continuation if kind == 'Continuation' else snapshot['frame'][name]
                for name, kind in binding.input_fields}
            cases.append(dict(id=identity, owner=binding.owner, alias=binding.alias,
                logical_address=binding.logical_address, initial_state_source=initial_ref,
                initial_state=snapshot, actual_input=inputs, physical_stack_source=stack_ref,
                external_supplies_source=supplies, independent_reference_source=reference,
                saved_initial_input_complete=not any(row.startswith('initial.') for row in missing),
                missing=missing, current_callable_CodeType='unknown_not_loaded',
                reference_qualification='contract_file_present_not_executed_or_independently_qualified',
                execution_status='not_run_no_scope_credit'))
            linked.setdefault(key, []).append(identity)
        except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
            excluded.append(dict(position=position, id=spec.get('id') if type(spec) is dict else None,
                reason='missing_or_ambiguous_explicit_Z80_input_not_repaired',
                error_type=type(error).__name__, error=str(error)))
    entries = []
    for binding in bindings:
        ids = tuple(linked.get((binding.owner, binding.alias), ()))
        missing = ['current_loaded_CodeType_and_complete_actual_callee_closure',
            'independent_reference_Z80_flags_R_WZ_control_and_device_observer_qualification',
            'new_whole_owner_all_aliases_full_state_stack_ordered_DATA_device_observations']
        if not ids:
            missing.insert(0, 'complete_saved_initial_state_and_explicit_supplies_for_this_alias')
        entries.append(dict(binding=asdict(binding), case_ids=ids, missing=missing,
            acceptance_status='pending_not_accepted'))
    return Z80InputPlan(tuple(entries), tuple(cases), tuple(excluded), tuple(scope.authority_counts))


def construct_typed_context(binding, *, frame, continuation):
    """Explicit future parameter adapter; no business invocation or stack write.

    Use only the ordinary ``typed_context`` entries. The two original PC0
    lifetimes must use their existing authority/lease/session APIs instead.
    Caller still owns actual execution, full state, devices and reference.
    """
    _require(type(binding) is Z80EntryBinding and binding.invocation['kind'] == 'typed_context',
        'ordinary source-bound typed entry required; PC0 needs its real session')
    from tools.high_level_audio_engine.domain import Continuation
    from tools.high_level_audio_engine.owned_runtime import DriverFrame
    _require(type(frame) is DriverFrame and type(continuation) is Continuation,
        'actual complete DriverFrame and explicit Continuation required')
    continuation.validate()
    _require(continuation.image == binding.owner.removeprefix('z80:'), 'source image continuation differs')
    module = importlib.import_module(binding.module)
    context_module = importlib.import_module(binding.input_module)
    function = getattr(module, binding.function)
    input_type = getattr(context_module, binding.input_class)
    result_module = importlib.import_module(binding.result_module)
    result_type = getattr(result_module, binding.result_class)
    _require(type(function) is FunctionType and function.__module__ == binding.module
        and function.__name__ == binding.function
        and function.__annotations__.get('inputs') is input_type
        and function.__annotations__.get('return') is result_type
        and tuple((name, field.type.__name__) for name, field in input_type.__dataclass_fields__.items())
            == tuple((name, 'int' if kind in ('Byte', 'Word') else kind)
                for name, kind in binding.input_fields), 'actual callable/context binding changed')
    values = {name: continuation if kind == 'Continuation' else getattr(frame, name)
        for name, kind in binding.input_fields}
    return function, input_type(**values)
