"""Read current AST-pinned capture candidates before monitoring is enabled.

This module uses only the standard library. It does not import business owners,
entry-binding APIs, a compiler or a runtime, and never calls a capture target.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import stat


FORMAT = 'g5510-concentrated-explicit-input-batch-v1'
MAX_BATCH_BYTES = 8 * 1024 * 1024
MAX_SOURCE_BYTES = 40_000_000
MAX_TYPE_IMPORT_DEPTH = 12
MODULE_PATTERN = re.compile(r'tools(?:\.[A-Za-z_][A-Za-z_0-9]*)+')
NAME_PATTERN = re.compile(r'[A-Za-z_][A-Za-z_0-9]*')
EARLY_TARGET = 'tools.high_level_dynamic_flows.target'
FRAME_TYPE = 'tools.high_level_battle_ai.contexts_first_deployment:FirstDeploymentFrame'


class CaptureCatalogError(ValueError):
    """The supplied batch or its current source evidence is not usable."""


@dataclass(frozen=True)
class CaptureTarget:
    owner: str
    entry: int
    alias: str
    module: str
    function: str
    argument_name: str
    frame_type: str
    keywords: tuple[tuple[str, int | bool], ...]
    source_path: Path
    source_binding_pointer: str
    binding_batch: Path


def _require(condition, message):
    if not condition:
        raise CaptureCatalogError(message)


def _dump(node):
    return ast.dump(node, include_attributes=False)


def _name(value, context):
    _require(type(value) is str and NAME_PATTERN.fullmatch(value) is not None,
        context + ': one explicit identifier is required')
    return value


def _module_name(value, context):
    _require(type(value) is str and MODULE_PATTERN.fullmatch(value) is not None,
        context + ': an explicit tools.* source module is required')
    return value


def _address(value, context):
    _require(type(value) is int and 0 <= value <= 0xFFFFFF and not value & 1,
        context + ': an even physical M68000 entry is required')
    return value


def _bounded_text(path, limit, context):
    try:
        with path.open('rb') as stream:
            raw = stream.read(limit + 1)
        _require(len(raw) <= limit, context + ': byte limit exceeded')
        return raw.decode('utf-8-sig')
    except (OSError, UnicodeError) as error:
        raise CaptureCatalogError(context + ': ' + str(error)) from error


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, 'batch JSON contains a duplicate key: ' + key)
        result[key] = value
    return result


def _nonfinite(value):
    raise CaptureCatalogError('batch JSON contains a non-finite number: ' + value)


def _finite_float(value):
    number = float(value)
    _require(math.isfinite(number), 'batch JSON number overflows the finite range: ' + value)
    return number


def _import_target(module, statement, alias):
    parent = module.split('.')[:-1]
    if statement.level:
        _require(statement.level <= len(parent), 'relative type import escapes tools source root')
        parent = parent[:len(parent) - statement.level + 1]
    else:
        parent = []
    _require(statement.module is not None, 'type reexport needs an explicit source module')
    target = '.'.join(parent + statement.module.split('.'))
    return _module_name(target, 'type reexport'), alias.name


class _CurrentSources:
    """Bounded source cache and exact AST pins; no runtime module loading."""

    def __init__(self, project, pins, early_names):
        self.project = project
        self.pins = pins
        self.early_names = early_names
        self.modules = {}

    def module(self, name):
        _module_name(name, 'source module')
        if name not in self.modules:
            path = self.project.joinpath(*name.split('.')).with_suffix('.py')
            # Reject symlinks/junctions before resolving: an ordinary source
            # file inside tools is required, not an indirect external owner.
            for candidate in (path, *path.parents):
                if candidate == self.project:
                    break
                try:
                    info = candidate.lstat()
                except OSError as error:
                    raise CaptureCatalogError('source path unavailable: ' + str(candidate)) from error
                _require(not stat.S_ISLNK(info.st_mode)
                    and not getattr(info, 'st_file_attributes', 0) & 0x400,
                    'source path must not traverse a symlink/reparse point: ' + str(candidate))
                if candidate == path:
                    _require(stat.S_ISREG(info.st_mode), 'source must be an ordinary .py file: ' + str(path))
            resolved = path.resolve(strict=True)
            _require(resolved.is_relative_to(self.project / 'tools'),
                'source module escapes the current project tools directory')
            text = _bounded_text(resolved, MAX_SOURCE_BYTES, 'source ' + name)
            try:
                tree = ast.parse(text, filename=str(resolved))
            except (SyntaxError, ValueError, RecursionError) as error:
                raise CaptureCatalogError('cannot parse current source ' + name + ': ' + str(error)) from error
            self.modules[name] = resolved, tree
        return self.modules[name]

    def definition(self, module, name, *, class_only=False):
        _name(name, 'source definition')
        _, tree = self.module(module)
        kinds = (ast.ClassDef,) if class_only else (ast.FunctionDef, ast.ClassDef)
        found = [node for node in tree.body if type(node) in kinds and node.name == name]
        _require(len(found) == 1, 'one complete current definition is required: ' + module + ':' + name)
        return found[0]

    def type_imports(self, module, name):
        _, tree = self.module(module)
        return [node for node in tree.body if type(node) is ast.ImportFrom
            and any((alias.asname or alias.name) == name for alias in node.names)]

    def require_pin(self, key, node):
        _require(key in self.pins, 'missing source pin: ' + key)
        _require(_dump(node) == self.pins[key], 'current source AST differs from pin: ' + key)

    def selected_early_bindings(self):
        _, tree = self.module(EARLY_TARGET)
        declarations = [node.value for node in tree.body if type(node) is ast.Assign
            and any(type(target) is ast.Name and target.id == 'EARLY_PHASE_BINDINGS'
                for target in node.targets)]
        _require(len(declarations) == 1 and type(declarations[0]) is ast.Tuple,
            'one literal current EARLY_PHASE_BINDINGS tuple is required')
        rows = {}
        for node in declarations[0].elts:
            values = _binding_values(node, 'early target declaration')
            _require(values[0] not in rows, 'early Binding owner name is repeated')
            rows[values[0]] = node
        _require(all(name in rows for name in self.early_names),
            'a selected early whole owner is absent from the current target tuple')
        selected = ast.Tuple(elts=[rows[name] for name in self.early_names], ctx=ast.Load())
        self.require_pin(EARLY_TARGET + ':selected_EARLY_PHASE_BINDINGS', selected)
        return rows

    def verify_pins(self):
        for key in self.pins:
            parts = key.split(':')
            _require(len(parts) in (2, 3), 'unsupported source-pin key: ' + key)
            module = _module_name(parts[0], 'source pin')
            if len(parts) == 3:
                _require(parts[1] == 'type_import', 'unsupported source-pin kind: ' + key)
                name = _name(parts[2], 'source type import')
                imports = self.type_imports(module, name)
                _require(imports, 'pinned type import is absent: ' + key)
                node = imports[0] if len(imports) == 1 else ast.Module(body=imports, type_ignores=[])
                self.require_pin(key, node)
            elif parts[1] == 'selected_EARLY_PHASE_BINDINGS':
                _require(module == EARLY_TARGET, 'selected early tuple has an unexpected module')
                self.selected_early_bindings()
            else:
                self.require_pin(key, self.definition(module, parts[1]))

    def symbol(self, module, name, trail=()):
        _require((module, name) not in trail and len(trail) < MAX_TYPE_IMPORT_DEPTH,
            'type reexports must form finite noncyclic source paths')
        _, tree = self.module(module)
        classes = [node for node in tree.body if type(node) is ast.ClassDef and node.name == name]
        if classes:
            _require(len(classes) == 1, 'type source definition is ambiguous: ' + module + ':' + name)
            self.require_pin(module + ':' + name, classes[0])
            return module + ':' + name
        imports = self.type_imports(module, name)
        _require(imports, 'type has no explicit pinned class/reexport: ' + module + ':' + name)
        node = imports[0] if len(imports) == 1 else ast.Module(body=imports, type_ignores=[])
        self.require_pin(module + ':type_import:' + name, node)
        resolved = set()
        for statement in imports:
            for alias in statement.names:
                if (alias.asname or alias.name) == name:
                    target, original_name = _import_target(module, statement, alias)
                    resolved.add(self.symbol(target, original_name, trail + ((module, name),)))
        _require(len(resolved) == 1, 'repeated type reexports resolve to competing classes: ' + module + ':' + name)
        return next(iter(resolved))

    def function(self, module, name):
        node = self.definition(module, name)
        _require(type(node) is ast.FunctionDef, 'capture entry must be a complete ordinary source function')
        self.require_pin(module + ':' + name, node)
        return node

    def binding(self, module, expected, owner_name, entry, alias):
        _, tree = self.module(module)
        found = {}
        for statement in tree.body:
            if type(statement) is not ast.Assign:
                continue
            for node in ast.walk(statement.value):
                if (type(node) is ast.Call and type(node.func) is ast.Name
                        and node.func.id == 'Binding' and _dump(node) == expected):
                    found[_dump(node)] = node
        _require(len(found) == 1, 'complete binding_AST is absent from the current target source: ' + owner_name)
        _require_binding_alias(next(iter(found.values())), owner_name, entry, alias)


def _binding_values(node, context):
    _require(type(node) is ast.Call and type(node.func) is ast.Name
        and node.func.id == 'Binding' and not node.keywords and len(node.args) in (3, 4, 6),
        context + ': literal Binding declaration required')
    try:
        values = tuple(ast.literal_eval(value) for value in node.args)
    except (ValueError, TypeError, RecursionError) as error:
        raise CaptureCatalogError(context + ': nonliteral Binding operands') from error
    _name(values[0], context + '.name')
    _address(values[1], context + '.start')
    return values


def _require_binding_alias(node, owner_name, entry, alias):
    values = _binding_values(node, 'target binding')
    _require(values[0] == owner_name, 'target Binding belongs to another whole owner')
    aliases = values[2] if len(values) == 6 else ((values[1], values[0]),)
    _require(type(aliases) is tuple and all(type(row) is tuple and len(row) == 2 for row in aliases)
        and (entry, alias) in aliases, 'physical alias is not owned by the complete target Binding')


def _source_pins(section, context):
    rows = section.get('source_pins')
    _require(type(rows) is list and rows, context + ': source pins are required')
    pins = {}
    for row in rows:
        _require(type(row) is list and len(row) == 2 and all(type(value) is str and value for value in row),
            context + ': each source pin must be a nonempty key/AST pair')
        _require(row[0] not in pins, context + ': duplicate source pin: ' + row[0])
        pins[row[0]] = row[1]
    return pins


def _keywords(rows, context):
    _require(type(rows) is list, context + ': explicit keyword list is required')
    result = []
    for row in rows:
        _require(type(row) is list and len(row) == 2 and type(row[1]) in (int, bool),
            context + ': keyword must be an explicit integer/bool pair')
        result.append((_name(row[0], context), row[1]))
    _require(len({name for name, _ in result}) == len(result), context + ': duplicate keyword')
    return tuple(result)


def _signature(sources, module, function, argument_name, argument_types, return_type, keywords):
    node = sources.function(module, function)
    args = node.args.posonlyargs + node.args.args
    annotation = 'SceneState' if argument_name == 'state' else 'SceneRefreshMemory'
    _require(len(args) >= 2 and [item.arg for item in args[:2]] == [argument_name, 'frame']
        and [ast.unparse(item.annotation) if item.annotation is not None else None for item in args[:2]]
            == [annotation, 'FirstDeploymentFrame']
        and node.returns is not None and ast.unparse(node.returns) == 'FirstDeploymentFrame'
        and not node.decorator_list and node.args.vararg is None and node.args.kwarg is None,
        'entry is not the declared complete Frame source ABI: ' + module + ':' + function)
    optional = {item.arg for item in args[len(args) - len(node.args.defaults):]} if node.args.defaults else set()
    required = {item.arg for item in args[2:] if item.arg not in optional}
    required.update(item.arg for item, default in zip(node.args.kwonlyargs, node.args.kw_defaults) if default is None)
    allowed = {item.arg for item in args[2:] + node.args.kwonlyargs}
    supplied = {name for name, _ in keywords}
    _require(required <= supplied <= allowed
        and not supplied & {item.arg for item in node.args.posonlyargs},
        'entry keyword contract differs from actual source parameters: ' + function)
    actual_types = (sources.symbol(module, annotation), sources.symbol(module, 'FirstDeploymentFrame'))
    _require(type(argument_types) is list and tuple(argument_types) == actual_types
        and return_type == actual_types[1] == FRAME_TYPE,
        'pinned source type identities differ from entry argument/return metadata: ' + function)
    return node, actual_types[1]


def _complete_target(row, index, sources, batch):
    pointer = '/complete_frame_bindings/entries/' + str(index)
    _require(type(row) is dict and type(row.get('spec')) is dict, pointer + ': complete entry spec required')
    spec = row['spec']
    owner_module = _module_name(spec.get('owner_module'), pointer)
    owner_name = _name(spec.get('owner_name'), pointer)
    _require(row.get('owner') == 'm68000:' + owner_module + ':' + owner_name,
        pointer + ': owner key and explicit source spec differ')
    entry = _address(spec.get('address'), pointer)
    alias = _name(spec.get('alias'), pointer)
    module = _module_name(spec.get('module'), pointer)
    function = _name(spec.get('function'), pointer)
    _require(spec.get('argument_style') in ('state_frame', 'memory_frame'), pointer + ': unsupported argument style')
    argument = 'state' if spec['argument_style'] == 'state_frame' else 'memory'
    keywords = _keywords(spec.get('keywords'), pointer)
    _, frame_type = _signature(sources, module, function, argument,
        row.get('argument_types'), row.get('return_type'), keywords)
    evidence = spec.get('evidence')
    _require(type(evidence) is list and evidence, pointer + ': actual source evidence is required')
    for pair in evidence:
        _require(type(pair) is list and len(pair) == 2, pointer + ': invalid source evidence pair')
        sources.function(_module_name(pair[0], pointer), _name(pair[1], pointer))
    target_module = _module_name(row.get('target_module'), pointer)
    _require(target_module == owner_module.rsplit('.', 1)[0] + '.target', pointer + ': wrong target owner module')
    binding_ast = row.get('binding_AST')
    _require(type(binding_ast) is str and binding_ast, pointer + ': complete target binding_AST is required')
    sources.binding(target_module, binding_ast, owner_name, entry, alias)
    return CaptureTarget(row['owner'], entry, alias, module, function, argument, frame_type,
        keywords, sources.module(module)[0], pointer, batch)


def _early_target(row, index, sources, batch, bindings):
    pointer = '/early_frame_bindings/entries/' + str(index)
    _require(type(row) is dict and type(row.get('owner')) is str, pointer + ': early entry required')
    owner_parts = row['owner'].split(':')
    _require(len(owner_parts) == 3 and owner_parts[0] == 'm68000', pointer + ': invalid M68000 owner key')
    owner_module = _module_name(owner_parts[1], pointer)
    owner_name = _name(owner_parts[2], pointer)
    _require(owner_module == 'tools.high_level_dynamic_flows.business_early_phase'
        and owner_name in sources.early_names, pointer + ': entry is outside the explicitly selected early owners')
    entry = _address(row.get('address'), pointer)
    alias = _name(row.get('alias'), pointer)
    module = _module_name(row.get('module'), pointer)
    function = _name(row.get('function'), pointer)
    _require(module == owner_module and row.get('arguments') == ['memory', 'frame'],
        pointer + ': actual early memory/frame source arguments required')
    node, frame_type = _signature(sources, module, function, 'memory',
        row.get('argument_types'), row.get('return_type'), ())
    _require(row.get('complete_source_AST') == _dump(node), pointer + ': complete early function AST differs')
    entry_calls = [call for call in ast.walk(node) if type(call) is ast.Call
        and type(call.func) is ast.Name and call.func.id in ('_scene_rule_frame_fields', '_allocation_phase_fields')
        and len(call.args) >= 3 and type(call.args[2]) is ast.Constant and call.args[2].value == entry]
    _require(len(entry_calls) == 1, pointer + ': actual early entry literal is not present in its full Frame owner')
    _require_binding_alias(bindings[owner_name], owner_name, entry, alias)
    return CaptureTarget(row['owner'], entry, alias, module, function, 'memory', frame_type,
        (), sources.module(module)[0], pointer, batch)


def load_capture_targets(batch: Path, project_root: Path) -> tuple[CaptureTarget, ...]:
    """Read every current pinned candidate, before any monitor is started."""
    try:
        project = Path(project_root).resolve(strict=True)
        batch_path = Path(batch).resolve(strict=True)
        _require(project.is_dir() and batch_path.is_file(), 'explicit existing project and batch file required')
        text = _bounded_text(batch_path, MAX_BATCH_BYTES, 'capture binding batch')
        value = json.loads(text, object_pairs_hook=_unique_object,
            parse_constant=_nonfinite, parse_float=_finite_float)
        _require(type(value) is dict and value.get('format') == FORMAT, 'unsupported capture binding batch format')
        declared = value.get('explicit_input_sources', {}).get('scope', {}).get('project_root')
        _require(type(declared) is str and Path(declared).is_absolute()
            and Path(declared).resolve(strict=True) == project,
            'binding batch must declare the supplied current project root')
        complete, early = value.get('complete_frame_bindings'), value.get('early_frame_bindings')
        _require(type(complete) is dict and type(early) is dict, 'both complete and early binding sections are required')
        pins = _source_pins(complete, 'complete_frame_bindings')
        for key, expected in _source_pins(early, 'early_frame_bindings').items():
            _require(key not in pins or pins[key] == expected, 'binding sections have competing source pins: ' + key)
            pins[key] = expected
        names = early.get('source_binding_names')
        _require(type(names) is list and names and len(set(names)) == len(names)
            and all(type(name) is str and NAME_PATTERN.fullmatch(name) for name in names),
            'explicit unique selected early Binding names are required')
        sources = _CurrentSources(project, pins, tuple(names))
        sources.verify_pins()
        bindings = sources.selected_early_bindings()
        _require(type(complete.get('entries')) is list and complete['entries']
            and type(early.get('entries')) is list and early['entries'], 'complete nonempty entry directories are required')
        targets = tuple(_complete_target(row, index, sources, batch_path)
            for index, row in enumerate(complete['entries'])) + tuple(
                _early_target(row, index, sources, batch_path, bindings)
                for index, row in enumerate(early['entries']))
        _require(len({(target.owner, target.entry, target.alias) for target in targets}) == len(targets),
            'capture directories contain duplicate owner/entry/alias tuples')
        _require(len({target.entry for target in targets}) == len(targets),
            'capture directories contain competing physical entry addresses')
        return targets
    except CaptureCatalogError:
        raise
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError, RecursionError) as error:
        raise CaptureCatalogError('cannot read current entry capture catalog: ' + str(error)) from error
