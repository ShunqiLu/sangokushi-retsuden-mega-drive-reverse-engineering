"""Prepare an immutable original-CALL directory; never hook or run an entry.

Retained source proofs are re-read once per explicit assembly file. Current
Python definitions share one source cache. The result describes possible
future pre-CALL observations, not saved inputs or executable acceptance cases.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
import json
from pathlib import Path
import stat

from .entry_capture_catalog import (
    FORMAT, MAX_BATCH_BYTES, CaptureCatalogError, CaptureTarget, _CurrentSources,
    _bounded_text, _dump, _finite_float, _module_name, _name, _nonfinite, _unique_object,
    _complete_target, _early_target, _source_pins, _import_target,
)
from .original_call_sources import read_original_call_sources as _call_sources


HELPERS = (
    ('tools.high_level_remaining_flows.business_lowbank', '_lowbank_ui_call_fields'),
    ('tools.high_level_remaining_flows.business_highbank', '_command_policy_call_fields'),
    ('tools.high_level_remaining_flows.business_highbank', '_highbank_recovery_call_fields'),
)
CURRENT_HELPERS = HELPERS + (
    ('tools.high_level_main_flows.business_main', '_campaign_call_fields'),
    ('tools.high_level_main_flows.business_gameplay', '_game_text_call_fields'),
    ('tools.high_level_main_flows.business_commands', '_city_ui_child_fields'),
)
CURRENT_HELPER_EXCLUSIONS = {
    'tools.high_level_main_flows.business_main:_campaign_call_fields':
        (0x676F2, 0x26BFA, 0xAC08, 0xA3DA, 0xDEA6),
    'tools.high_level_main_flows.business_commands:_city_ui_child_fields':
        (0x676F2, 0x1270A),
}
MAX_BINDINGS = 4096
MAX_ORIGINAL_SOURCES = 32
MAX_TEXT = 4096
MISSING_QUALIFICATION = (
    'actual_same_thread_public_helper_CodeType_globals_and_pre_body_observation',
    'helper_to_complete_actual_callee_execution_closure',
    'actual_pre_CALL_16_LONGs_full_SR_CCR_and_complete_64KiB_RAM',
    'explicit_stack_window_and_independent_finite_execution_budgets',
    'required_own_aliases_selected_and_actually_reached_for_this_live_input',
    'readonly_DATA_artifact_freeze_and_device_initial_state_and_supplies',
    'independent_original_reference_and_complete_output_observations',
)


class PreCallCatalogError(ValueError):
    """Malformed preparation inputs are not silently turned into runtime state."""


def _require(condition, message):
    if not condition:
        raise PreCallCatalogError(message)


def _integer(value, context, *, maximum=0xFFFFFF):
    _require(type(value) is int and 0 <= value <= maximum,
        context + ': an explicit unsigned integer is required')
    return value


def _text(value, context):
    _require(type(value) is str and 0 < len(value) <= MAX_TEXT, context + ': bounded text required')
    return value


@dataclass(frozen=True)
class PreCallHelper:
    module: str
    function: str
    source_path: Path
    complete_source_AST: str
    excluded_targets: tuple[int, ...] = ()

    @property
    def key(self):
        return self.module + ':' + self.function


@dataclass(frozen=True)
class OriginalCallProof:
    source: Path
    line: int
    statement: str
    caller: int
    target: int
    continuation: int


@dataclass(frozen=True)
class ActualCalleeSource:
    actual_entry: int
    module: str
    function: str
    argument_name: str
    keywords: tuple[tuple[str, int | bool], ...]
    source_path: Path
    complete_source_AST: str
    matching_capture_owner: str | None


@dataclass(frozen=True)
class RequiredAliasReference:
    """A retained case requirement, not an alias already reached in a new run."""
    case: str
    batch_pointer: str
    required_aliases: tuple[int, ...]


@dataclass(frozen=True)
class SourceEntryReference:
    """Current source evidence, never a retained case or reached own alias."""
    owner: str
    entry: int
    alias: str
    batch_pointer: str
    required_aliases: tuple[int, ...]
    callee_pin_pointer: str
    caller_module: str
    caller_function: str
    caller_source: Path
    caller_complete_source_AST: str
    helper_reference: str
    helper_call_AST: str
    caller_pin_pointer: str | None
    caller_source_qualification: str


def source_entry_reference_observation(row):
    """Small metadata only; retain the complete caller AST in its index."""
    _require(type(row) is SourceEntryReference, 'exact prepared SourceEntryReference required')
    return dict(owner=row.owner, entry=row.entry, alias=row.alias,
        batch_pointer=row.batch_pointer, required_aliases=list(row.required_aliases),
        callee_pin_pointer=row.callee_pin_pointer, caller_module=row.caller_module,
        caller_function=row.caller_function, caller_source=str(row.caller_source),
        helper_reference=row.helper_reference, helper_call_AST=row.helper_call_AST,
        caller_pin_pointer=row.caller_pin_pointer,
        caller_source_qualification=row.caller_source_qualification,
        caller_complete_AST_retained_in_prepared_index=True,
        source_files_frozen=False, actually_reached_here=False)


@dataclass(frozen=True)
class PreCallGap:
    case: str | None
    target: int | None
    continuation: int | None
    reason: str
    source_pointer: str | None = None


@dataclass(frozen=True)
class PreparedPreCallRoute:
    helper: str
    original_call: OriginalCallProof
    actual_callee: ActualCalleeSource
    retained_requirements: tuple[RequiredAliasReference, ...]
    source_entry_references: tuple[SourceEntryReference, ...] = ()


@dataclass(frozen=True)
class PreCallLookup:
    status: str
    candidates: tuple[PreparedPreCallRoute, ...]
    missing: tuple[str, ...]


@dataclass(frozen=True)
class PreparedPreCallIndex:
    binding_batch: Path
    helpers: tuple[PreCallHelper, ...]
    routes: tuple[PreparedPreCallRoute, ...]
    gaps: tuple[PreCallGap, ...]
    parsed_original_sources: tuple[Path, ...]

    def lookup(self, helper: str, target: int, continuation: int, *, entry_kind: str) -> PreCallLookup:
        """Pure finite lookup; no caller arithmetic, files, hooks or state access."""
        if entry_kind != 'direct_CALL':
            return PreCallLookup('missing', (), ('indirect_tail_IRQ_or_unknown_entry_is_not_a_direct_CALL',))
        if helper not in tuple(row.key for row in self.helpers):
            reason = ('helper_is_not_in_the_explicit_three_helper_directory' if len(self.helpers) == len(HELPERS)
                else 'helper_is_not_in_the_explicit_current_helper_directory')
            return PreCallLookup('missing', (), (reason,))
        descriptor = next(row for row in self.helpers if row.key == helper)
        if target in descriptor.excluded_targets:
            return PreCallLookup('missing', (), ('helper_delegates_this_target_before_its_own_CALL_stack_decrement',))
        _integer(target, 'observed helper target')
        _integer(continuation, 'observed helper continuation')
        found = tuple(row for row in self.routes if row.helper == helper
            and row.original_call.target == target and row.original_call.continuation == continuation)
        if len(found) != 1:
            reason = 'no_explicit_original_CALL_and_actual_parent_mapping' if not found else 'ambiguous_original_CALL_or_parent_mapping'
            return PreCallLookup('missing', found, (reason,))
        return PreCallLookup('unique_source_candidate_not_runtime_or_input_qualification',
            found, MISSING_QUALIFICATION)


def _assembly_path(project, value):
    supplied = Path(_text(value, 'original assembly source'))
    path = supplied if supplied.is_absolute() else project / supplied
    _require(not str(path).startswith(('\\\\', '//', '\\?\\', '\\.\\'))
        and ':' not in str(path)[2:], 'UNC/device/ADS original source paths are refused')
    for member in (path, *path.parents):
        info = member.lstat()
        _require(not stat.S_ISLNK(info.st_mode) and not getattr(info, 'st_file_attributes', 0) & 0x400,
            'original source cannot traverse a reparse path')
        if member == project:
            break
    resolved = path.resolve(strict=True)
    _require(resolved.is_relative_to(project / 'src' / 'm68k') and resolved.suffix == '.s'
        and resolved.is_file() and resolved.stat().st_size <= 16_000_000,
        'explicit bounded editable original m68k assembly source required')
    return resolved


def _helper_directory(sources, directory=HELPERS):
    result = []
    stack = ast.parse('stack = frame.stack_cursor.advance(-4)\n').body[0]
    for module, function in directory:
        node = sources.definition(module, function)
        _require(type(node) is ast.FunctionDef and not node.decorator_list
            and not node.args.posonlyargs and not node.args.kwonlyargs
            and node.args.vararg is None and node.args.kwarg is None and not node.args.defaults
            and tuple(arg.arg for arg in node.args.args) == ('state', 'frame', 'target', 'continuation'),
            'the helper must retain its complete explicit four-argument source ABI: ' + function)
        _require(sum(_dump(statement) == _dump(stack) for statement in node.body) == 1,
            'the helper must retain its one explicit original stack decrement: ' + function)
        key = module + ':' + function
        exclusions = CURRENT_HELPER_EXCLUSIONS.get(key, ()) if directory == CURRENT_HELPERS else ()
        result.append(PreCallHelper(module, function, sources.module(module)[0], _dump(node), exclusions))
    return tuple(result)


def _callee_source(row, sources, prepared_targets):
    entry = _integer(row.get('actual_entry'), 'actual original parent entry')
    module = _module_name(row.get('actual_module'), 'actual parent module')
    function = _name(row.get('actual_function'), 'actual parent function')
    node = sources.definition(module, function)
    _require(type(node) is ast.FunctionDef and not node.decorator_list,
        'the actual parent requires one complete ordinary source function')
    args = node.args.args
    _require(not node.args.posonlyargs and len(args) >= 2 and args[0].arg in ('state', 'memory')
        and args[1].arg == 'frame' and ast.unparse(args[1].annotation) == 'FirstDeploymentFrame'
        and node.returns is not None and ast.unparse(node.returns) == 'FirstDeploymentFrame',
        'unmapped_parent_no_complete_state_or_memory_Frame_ABI')
    spec = row.get('entry_spec', {})
    _require(type(spec) is dict, 'actual saved entry specification must remain explicit')
    keywords = spec.get('keywords', [])
    _require(type(keywords) is list and all(type(pair) is list and len(pair) == 2
        and type(pair[0]) is str and type(pair[1]) in (int, bool) for pair in keywords),
        'only retained explicit integer/bool entry keywords are supported')
    keywords = tuple((name, value) for name, value in keywords)
    _require(len({name for name, _ in keywords}) == len(keywords), 'duplicate actual parent keyword')
    matches = tuple(target for target in prepared_targets if target.entry == entry)
    _require(len(matches) <= 1, 'ambiguous prepared actual parent target')
    owner = None
    if matches:
        target = matches[0]
        _require((target.module, target.function, target.argument_name, target.keywords)
            == (module, function, args[0].arg, keywords),
            'an internal captured alias must not replace the actual original parent')
        owner = target.owner
    return ActualCalleeSource(entry, module, function, args[0].arg, keywords,
        sources.module(module)[0], _dump(node), owner)


def _seed_rows(document):
    result = []
    for section in ('complete_frame_bindings', 'early_frame_bindings'):
        value = document.get(section)
        _require(type(value) is dict and type(value.get('cases')) is list,
            'the explicit complete/early original-CALL binding sections are required')
        for index, row in enumerate(value['cases']):
            _require(type(row) is dict, 'one retained source binding object required')
            result.append((row, '/' + section + '/cases/' + str(index)))
    _require(len(result) <= MAX_BINDINGS, 'retained original-CALL directory exceeds its explicit limit')
    return result


def _current_entry_directory(document, project, batch, cache, gaps):
    """Reuse the existing pinned entry/Binding rules, not a second mapper."""
    pins, pointers = {}, {}
    for section_name in ('complete_frame_bindings', 'early_frame_bindings'):
        section = document[section_name]
        for key, value in _source_pins(section, section_name).items():
            _require(key not in pins or pins[key] == value, 'competing current source pin: ' + key)
            pins[key] = value
        for index, row in enumerate(section['source_pins']):
            pointers.setdefault(row[0], '/' + section_name + '/source_pins/' + str(index))
    early = document['early_frame_bindings']
    names = early.get('source_binding_names')
    _require(type(names) is list and names and len(set(names)) == len(names),
        'explicit selected early Binding names required')
    sources = _CurrentSources(project, pins, tuple(_name(name, 'early Binding') for name in names))
    sources.modules = cache.modules  # one parse cache; caller-owned pins are not mutated
    try:
        bindings = sources.selected_early_bindings()
    except (CaptureCatalogError, OSError, ValueError, TypeError) as error:
        bindings = None
        gaps.append(PreCallGap(None, None, None, str(error)[:MAX_TEXT], '/early_frame_bindings/entries'))
    targets = []
    for section_name in ('complete_frame_bindings', 'early_frame_bindings'):
        rows = document[section_name].get('entries')
        _require(type(rows) is list and len(rows) <= MAX_BINDINGS, 'explicit bounded current entry directory required')
        for index, row in enumerate(rows):
            pointer = '/' + section_name + '/entries/' + str(index)
            try:
                if section_name == 'complete_frame_bindings':
                    target = _complete_target(row, index, sources, batch)
                else:
                    if bindings is None:
                        continue
                    target = _early_target(row, index, sources, batch, bindings)
                targets.append(target)
            except (CaptureCatalogError, OSError, ValueError, TypeError, KeyError, AttributeError) as error:
                gaps.append(PreCallGap(None, None, None, str(error)[:MAX_TEXT], pointer))
    _require(len(targets) <= MAX_BINDINGS, 'current entry directory exceeds its explicit limit')
    return sources, tuple(targets), pointers


def _scope_nodes(nodes):
    """Visit this lexical body only, not nested function/class/lambda bodies."""
    for node in nodes:
        yield node
        if type(node) not in (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda):
            yield from _scope_nodes(ast.iter_child_nodes(node))


def _bound_names(nodes):
    names = set()
    for node in nodes:
        if type(node) is ast.Name and type(node.ctx) in (ast.Store, ast.Del):
            names.add(node.id)
        elif type(node) in (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef):
            names.add(node.name)
        elif type(node) in (ast.Import, ast.ImportFrom):
            names.update(alias.asname or alias.name.split('.')[0] for alias in node.names)
        elif type(node) in (ast.Global, ast.Nonlocal):
            names.update(node.names)
        elif type(node) is ast.ExceptHandler and node.name is not None:
            names.add(node.name)
        elif type(node) in (ast.MatchAs, ast.MatchStar) and node.name is not None:
            names.add(node.name)
        elif type(node) is ast.MatchMapping and node.rest is not None:
            names.add(node.rest)
    return names


def _helper_references(module, tree, helpers):
    """Resolve only the own definition or a unique direct top-level import."""
    references = {helper.function: [] for helper in helpers}
    accepted = set()
    for statement in tree.body:
        if type(statement) is ast.FunctionDef:
            for helper in helpers:
                if (module, statement.name) == (helper.module, helper.function):
                    references.setdefault(statement.name, []).append(helper)
                    accepted.add((id(statement), statement.name))
        elif type(statement) is ast.ImportFrom and statement.module is not None:
            for alias in statement.names:
                if alias.name not in {helper.function for helper in helpers}:
                    continue
                imported, name = _import_target(module, statement, alias)
                for helper in helpers:
                    if (imported, name) == (helper.module, helper.function):
                        reference = alias.asname or alias.name
                        references.setdefault(reference, []).append(helper)
                        accepted.add((id(statement), reference))
    blocked = set()
    for statement in tree.body:
        for name in _bound_names(_scope_nodes((statement,))):
            if name in references and (id(statement), name) not in accepted:
                blocked.add(name)
    return {name: (values[0] if len(values) == 1 and name not in blocked else None)
        for name, values in references.items()}


def _current_literal_calls(sources, targets, helpers, pin_pointers, gaps):
    """Only explicitly mapped modules are searched; no transitive module walk."""
    result, examined = [], 0
    for module in sorted({target.module for target in targets}):
        path, tree = sources.module(module)
        references = _helper_references(module, tree, helpers)
        for function in tree.body:
            if type(function) is not ast.FunctionDef:
                continue
            nodes = tuple(_scope_nodes(function.body))
            calls = [node for node in nodes if type(node) is ast.Call
                and type(node.func) is ast.Name and node.func.id in references]
            if not calls:
                continue
            key = module + ':' + function.name
            pointer = str(path) + ':' + str(function.lineno)
            expected = sources.pins.get(key)
            if expected is not None and expected != _dump(function):
                gaps.append(PreCallGap(None, None, None, 'current_caller_differs_from_explicit_batch_pin', pointer))
                continue
            arguments = function.args.posonlyargs + function.args.args + function.args.kwonlyargs
            local = _bound_names(nodes) | {arg.arg for arg in arguments}
            local.update(arg.arg for arg in (function.args.vararg, function.args.kwarg) if arg is not None)
            for call in calls:
                examined += 1
                _require(examined <= MAX_BINDINGS, 'current helper CALL directory exceeds its explicit limit')
                target = continuation = None
                origin = str(path) + ':' + str(call.lineno)
                helper = references[call.func.id]
                try:
                    _require(helper is not None and call.func.id not in local,
                        'helper_reference_is_ambiguous_locally_shadowed_or_rebound')
                    _require(len(call.args) == 4 and not call.keywords
                        and all(type(arg) is ast.Constant and type(arg.value) is int for arg in call.args[2:]),
                        'current_helper_CALL_requires_literal_target_and_continuation')
                    target = _integer(call.args[2].value, 'current literal target')
                    continuation = _integer(call.args[3].value, 'current literal continuation')
                    _require(not target & 1 and not continuation & 1, 'even literal original PCs required')
                    _require(target not in helper.excluded_targets,
                        'helper_delegates_this_target_before_its_own_CALL_stack_decrement')
                    result.append((helper, target, continuation, module, function, call,
                        path, pin_pointers.get(key)))
                except (PreCallCatalogError, ValueError, TypeError) as error:
                    gaps.append(PreCallGap(None, target, continuation, str(error)[:MAX_TEXT], origin))
    return tuple(result)


def _source_routes(calls, targets, sources, pin_pointers, found, rejected, failed_sources, gaps):
    entries, originals, grouped = {}, {}, {}
    for target in targets:
        entries.setdefault(target.entry, []).append(target)
    for values in found.values():
        for proof in values:
            if proof.source not in failed_sources and not rejected.get(proof.caller):
                originals.setdefault((proof.target, proof.continuation), []).append(proof)
    for helper, target, continuation, module, function, call, path, pin_pointer in calls:
        origin = str(path) + ':' + str(call.lineno)
        candidates, proofs = entries.get(target, ()), originals.get((target, continuation), ())
        if len(candidates) != 1 or len(proofs) != 1:
            gaps.append(PreCallGap(None, target, continuation,
                'current_literal_CALL_requires_one_exact_entry_mapping_and_original_direct_CALL', origin))
            continue
        captured, proof = candidates[0], proofs[0]
        if len(found.get(proof.caller, ())) != 1:
            gaps.append(PreCallGap(None, target, continuation, 'ambiguous_original_CALL_source', origin))
            continue
        callee = _callee_source(dict(actual_entry=captured.entry, actual_module=captured.module,
            actual_function=captured.function, entry_spec=dict(keywords=[list(pair) for pair in captured.keywords])),
            sources, (captured,))
        ref = SourceEntryReference(captured.owner, captured.entry, captured.alias,
            captured.source_binding_pointer, (captured.entry,),
            pin_pointers[captured.module + ':' + captured.function], module, function.name,
            path, _dump(function), call.func.id, _dump(call), pin_pointer,
            'exact_current_source_matches_explicit_batch_pin' if pin_pointer is not None
                else 'fresh_current_source_not_old_batch_pin')
        grouped.setdefault((helper.key, proof, callee), []).append(ref)
    return grouped


def prepare_pre_call_index(batch: Path, project_root: Path, *,
        prepared_targets: tuple[CaptureTarget, ...] = (), source_cache=None,
        include_current_source_calls: bool = False) -> PreparedPreCallIndex:
    """Prepare metadata only; existing capture/runtime owners are untouched.

    A caller may pass its already-loaded CaptureTarget tuple and _CurrentSources
    cache. No existing loader, binder, business import or case API is invoked.
    The default uses retained proofs only. The explicit current-source mode
    additionally matches real literal helper calls to exact current entries and
    independently enumerated original CALLs; it never derives a caller address.
    """
    project, batch = Path(project_root).resolve(strict=True), Path(batch).resolve(strict=True)
    _require(project.is_dir() and batch.is_file(), 'explicit existing project and binding batch required')
    _require(type(include_current_source_calls) is bool, 'explicit current-source CALL mode must be bool')
    document = json.loads(_bounded_text(batch, MAX_BATCH_BYTES, 'pre-CALL source batch'),
        object_pairs_hook=_unique_object, parse_constant=_nonfinite, parse_float=_finite_float)
    _require(type(document) is dict and document.get('format') == FORMAT, 'explicit concentrated input batch required')
    declared = document.get('explicit_input_sources', {}).get('scope', {}).get('project_root')
    _require(type(declared) is str and Path(declared).resolve(strict=True) == project,
        'pre-CALL binding batch belongs to another source project')
    _require(type(prepared_targets) is tuple and all(type(row) is CaptureTarget for row in prepared_targets),
        'only an already-prepared immutable CaptureTarget tuple may be reused')
    sources = _CurrentSources(project, {}, ()) if source_cache is None else source_cache
    _require(isinstance(sources, _CurrentSources) and sources.project == project,
        'one current source cache belonging to this explicit project required')
    helpers = _helper_directory(sources, CURRENT_HELPERS if include_current_source_calls else HELPERS)
    original_paths = document.get('explicit_input_sources', {}).get('original_call_sources')
    _require(type(original_paths) is list and 0 < len(original_paths) <= MAX_ORIGINAL_SOURCES,
        'a bounded explicit original assembly-source list is required')
    paths = tuple(dict.fromkeys(_assembly_path(project, value) for value in original_paths))
    seeds, gaps = [], []
    for row, pointer in _seed_rows(document):
        case = _text(row.get('case'), 'retained case key')
        target = continuation = None
        try:
            target = _integer(row.get('actual_entry'), 'actual original parent entry')
            continuation = _integer(row.get('continuation'), 'actual original continuation')
            caller = _integer(row.get('caller'), 'actual original caller')
            raw = row.get('original_call_source')
            _require(type(raw) is dict, 'missing explicit original_CALL proof')
            source = _assembly_path(project, raw.get('source'))
            _require(source in paths, 'original_CALL source is outside the batch explicit source list')
            proof = OriginalCallProof(source, _integer(raw.get('line'), 'original source line', maximum=16_000_000),
                _text(raw.get('statement'), 'original CALL statement'), _integer(raw.get('caller'), 'proof caller'),
                _integer(raw.get('target'), 'proof target'), _integer(raw.get('continuation'), 'proof continuation'))
            _require((proof.caller, proof.target, proof.continuation) == (caller, target, continuation),
                'actual parent/caller/continuation differ from retained original source proof')
            aliases = row.get('required_aliases')
            aliases = [row.get('required_alias')] if aliases is None else aliases
            _require(type(aliases) is list and aliases, 'explicit required own aliases are missing')
            aliases = tuple(_integer(value, 'required own alias') for value in aliases)
            _require(len(set(aliases)) == len(aliases), 'duplicate required own alias')
            callee = _callee_source(row, sources, prepared_targets)
            seeds.append((proof, callee, RequiredAliasReference(case, pointer, aliases)))
        except (PreCallCatalogError, CaptureCatalogError, OSError, ValueError, TypeError, AttributeError) as error:
            gaps.append(PreCallGap(case, target, continuation, str(error)[:MAX_TEXT]))
    source_calls, source_targets, pin_pointers = (), (), {}
    if include_current_source_calls:
        sources, source_targets, pin_pointers = _current_entry_directory(document, project, batch, sources, gaps)
        source_calls = _current_literal_calls(sources, source_targets, helpers, pin_pointers, gaps)
    wanted = None if include_current_source_calls else {proof.caller for proof, _, _ in seeds}
    found, rejected, failed_sources = {}, {}, set()
    for path in paths:
        try:
            # Exactly one existing parser call per file; it also retains
            # unsupported direct cells instead of guessing an instruction width.
            calls, refused = _call_sources((path,), wanted)
            for caller, value in calls.items():
                found.setdefault(caller, []).append(OriginalCallProof(Path(value['source']), value['line'],
                    value['statement'], value['caller'], value['target'], value['continuation']))
            for caller, value in refused.items():
                rejected.setdefault(caller, []).append(value['reason'])
                if include_current_source_calls:
                    gaps.append(PreCallGap(None, None, None,
                        ('unsupported_original_CALL: ' + value['reason'])[:MAX_TEXT],
                        str(path) + ':' + str(value['line'])))
        except (OSError, ValueError, TypeError) as error:
            failed_sources.add(path)
            gaps.append(PreCallGap(None, None, None, ('original_source_parser_boundary: ' + str(error))[:MAX_TEXT]))
    source_grouped = (_source_routes(source_calls, source_targets, sources, pin_pointers,
        found, rejected, failed_sources, gaps) if include_current_source_calls else {})
    grouped = {key: [] for key in source_grouped}
    for proof, callee, requirement in seeds:
        actual = found.get(proof.caller, [])
        if proof.source in failed_sources or rejected.get(proof.caller) or len(actual) != 1 or actual[0] != proof:
            gaps.append(PreCallGap(requirement.case, proof.target, proof.continuation,
                'absent_ambiguous_indirect_tail_IRQ_or_changed_original_CALL_proof'))
            continue
        if include_current_source_calls:
            linked = [key for key in grouped if key[1] == proof
                and (key[2].actual_entry, key[2].module, key[2].function, key[2].argument_name,
                    key[2].keywords, key[2].source_path, key[2].complete_source_AST)
                == (callee.actual_entry, callee.module, callee.function, callee.argument_name,
                    callee.keywords, callee.source_path, callee.complete_source_AST)]
            if not linked:
                gaps.append(PreCallGap(requirement.case, proof.target, proof.continuation,
                    'retained_CALL_has_no_exact_current_literal_helper_association', requirement.batch_pointer))
            for key in linked:
                grouped[key].append(requirement)
        else:
            for helper in helpers:
                grouped.setdefault((helper.key, proof, callee), []).append(requirement)
    routes = tuple(PreparedPreCallRoute(helper, proof, callee, tuple(dict.fromkeys(requirements)),
        tuple(dict.fromkeys(source_grouped.get((helper, proof, callee), ()))))
        for (helper, proof, callee), requirements in grouped.items())
    return PreparedPreCallIndex(batch, helpers, routes, tuple(gaps), paths)
