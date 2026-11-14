"""Prepare the finite public Z80 capture directory without loading business.

The explicit batch supplies the existing 109 entry descriptions. Current
source geometry, two-argument functions and immutable context schemas are
read as ASTs only. This is candidate mapping, not loaded-CodeType admission.
"""
from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path

from .entry_capture_catalog import (
    FORMAT, MAX_BATCH_BYTES, CaptureCatalogError, _CurrentSources,
    _bounded_text, _finite_float, _nonfinite, _unique_object,
)
from .z80_case_inputs import (
    FORMAT as Z80_INPUT_FORMAT, CARRIERS, PACKAGE, Z80EntryBinding,
    _context_schema,
)


BINDING_FIELDS = ('owner', 'alias', 'logical_address', 'physical_address', 'module',
    'function', 'source', 'source_line', 'input_module', 'input_class', 'input_fields',
    'result_module', 'result_class', 'result_fields', 'invocation', 'qualification')
EXPECTED_ENTRIES = 109


class Z80CaptureCatalogError(ValueError):
    """A current public entry cannot be inferred from a stale/ambiguous row."""


@dataclass(frozen=True)
class Z80CaptureTarget:
    binding: Z80EntryBinding
    source_path: Path
    source_binding_pointer: str
    binding_batch: Path
    current_source_line: int
    qualification: str = 'current_source_candidate_not_loaded_CodeType_or_behavioral_proof'


def _require(condition, message):
    if not condition:
        raise Z80CaptureCatalogError(message)


def _identifier(value, context):
    _require(type(value) is str and value.isidentifier() and value.isascii(),
        context + ': one explicit ASCII identifier required')
    return value


def _integer(value, bits, context):
    _require(type(value) is int and 0 <= value < 1 << bits,
        context + ': exact unsigned integer required')
    return value


def _literal(tree, name):
    values = [row.value for row in tree.body if type(row) is ast.Assign
        and any(type(target) is ast.Name and target.id == name for target in row.targets)]
    _require(values, 'one current literal target directory required: ' + name)
    decoded = [ast.literal_eval(value) for value in values]
    _require(all(value == decoded[0] for value in decoded),
        'conflicting current literal target directories: ' + name)
    return decoded[0]


def _schema(value, context):
    _require(type(value) is list and value, context + ': explicit nonempty context schema required')
    rows, names = [], set()
    for row in value:
        _require(type(row) is list and len(row) == 2 and row[1] in ('Byte', 'Word', 'Continuation'),
            context + ': actual context name/type pairs required')
        name = _identifier(row[0], context)
        _require(name not in names, context + ': duplicate context field')
        names.add(name)
        rows.append((name, row[1]))
    return tuple(rows)


def _direct_type(tree, name, module):
    imports = [(row, item) for row in tree.body if type(row) is ast.ImportFrom
        for item in row.names if (item.asname or item.name) == name]
    _require(len(imports) == 1 and imports[0][0].level == 1
        and imports[0][0].module == module and imports[0][1].name == name
        and imports[0][1].asname is None,
        'actual direct ' + module + ' type import required: ' + name)


def _source_functions(sources, modules, aliases):
    _require(type(modules) is tuple and modules and len(set(modules)) == len(modules),
        'finite unique audio source module directory required')
    found = {}
    for filename in modules:
        _require(type(filename) is str and '/' not in filename and '\\' not in filename
            and filename.endswith('.py'), 'one actual local audio source filename required')
        if not filename.startswith('business_'):
            continue
        module = PACKAGE + '.' + filename[:-3]
        path, tree = sources.module(module)
        for node in tree.body:
            if type(node) is not ast.FunctionDef or node.name not in aliases:
                continue
            _require(node.name not in found, 'audio alias has competing public definitions: ' + node.name)
            args = node.args
            _require(not node.decorator_list and not args.posonlyargs and not args.kwonlyargs
                and args.vararg is None and args.kwarg is None and not args.defaults
                and len(args.args) == 2 and tuple(row.arg for row in args.args) == ('state', 'inputs')
                and type(args.args[0].annotation) is ast.Name
                and args.args[0].annotation.id == 'AudioState'
                and type(args.args[1].annotation) is ast.Name and type(node.returns) is ast.Name,
                'complete ordinary (AudioState, typed inputs) ABI required: ' + node.name)
            _require(not any(type(child) in (ast.Yield, ast.YieldFrom, ast.AsyncFunctionDef)
                for child in ast.walk(node)), 'private cooperative views are not public capture entries')
            input_name, result_name = args.args[1].annotation.id, node.returns.id
            _direct_type(tree, 'AudioState', 'domain')
            _direct_type(tree, input_name, 'contexts')
            _direct_type(tree, result_name, 'contexts')
            found[node.name] = module, path, node, input_name, result_name
    _require(set(found) == set(aliases), 'all and only declared public audio aliases must have actual definitions')
    return found


def _scope_entries(value):
    wrapper = value.get('scope')
    scope = wrapper.get('scope') if type(wrapper) is dict else None
    _require(type(scope) is dict and type(scope.get('owners')) is list,
        'the explicit current whole-owner scope must accompany its Z80 input directory')
    owners = [row for row in scope['owners'] if type(row) is dict and row.get('architecture') == 'z80']
    _require({row.get('key') for row in owners} == {'z80:startup', 'z80:driver'} and len(owners) == 2,
        'exactly the two distinct pending Z80 images required')
    result = set()
    for owner in owners:
        _require(type(owner.get('entries')) is list and owner['entries'], 'explicit owned aliases required')
        for row in owner['entries']:
            _require(type(row) is dict, 'one actual Z80 scope entry required')
            identity = (owner['key'], _identifier(row.get('alias'), 'scope alias'),
                _integer(row.get('logical_address'), 16, 'scope logical entry'),
                _integer(row.get('physical_address'), 20, 'scope physical source'))
            _require(identity not in result, 'duplicate Z80 scope entry')
            result.add(identity)
    return result


def load_z80_capture_targets(batch: Path, project_root: Path) -> tuple[Z80CaptureTarget, ...]:
    """Prepare public targets before monitoring; never import/execute a callee.

    No original ROM, case result, saved RAM or reference runner is consulted.
    The batch's source-definition descriptions are checked against today's
    source, but this does not prove the loaded function equals its file AST.
    """
    try:
        project, batch_path = Path(project_root).resolve(strict=True), Path(batch).resolve(strict=True)
        _require(project.is_dir() and batch_path.is_file(), 'explicit existing project and batch required')
        value = json.loads(_bounded_text(batch_path, MAX_BATCH_BYTES, 'Z80 capture binding batch'),
            object_pairs_hook=_unique_object, parse_constant=_nonfinite, parse_float=_finite_float)
        _require(type(value) is dict and value.get('format') == FORMAT,
            'the explicit concentrated input batch format is required')
        declared = value.get('explicit_input_sources', {}).get('scope', {}).get('project_root')
        _require(type(declared) is str and Path(declared).is_absolute()
            and Path(declared).resolve(strict=True) == project, 'batch belongs to a different source project')
        section = value.get('z80_inputs')
        _require(type(section) is dict and section.get('format') == Z80_INPUT_FORMAT
            and section.get('owners') == 2 and type(section.get('entries')) is list,
            'the explicit two-owner Z80 input directory is required')
        rows = section['entries']
        _require(len(rows) == EXPECTED_ENTRIES and section.get('named_entries') == EXPECTED_ENTRIES,
            'all109 existing named Z80 source entries are required')
        sources = _CurrentSources(project, {}, ())
        _, target = sources.module(PACKAGE + '.target')
        aliases, units = _literal(target, 'CALLEE_ADDRESSES'), _literal(target, 'UNITS')
        _require(type(aliases) is dict and len(aliases) == EXPECTED_ENTRIES
            and type(units) is dict and set(units) == {'driver', 'startup'},
            'current explicit logical aliases and separate source images required')
        for name, address in aliases.items():
            _identifier(name, 'current alias')
            _integer(address, 16, 'current logical entry')
        found = _source_functions(sources, _literal(target, 'BUSINESS_MODULES'), aliases)
        _, contexts = sources.module(PACKAGE + '.contexts')
        expected_scope, selected, seen = _scope_entries(value), [], set()
        for index, row in enumerate(rows):
            pointer = '/z80_inputs/entries/' + str(index) + '/binding'
            _require(type(row) is dict and type(row.get('binding')) is dict
                and set(row['binding']) == set(BINDING_FIELDS), pointer + ': complete source binding required')
            binding = dict(row['binding'])
            owner, alias = binding['owner'], _identifier(binding['alias'], pointer)
            _require(owner in ('z80:driver', 'z80:startup') and alias in found,
                pointer + ': entry outside actual declared audio images')
            logical = _integer(binding['logical_address'], 16, pointer + '.logical')
            physical = _integer(binding['physical_address'], 20, pointer + '.physical')
            identity = owner, alias, logical, physical
            _require(identity in expected_scope and identity not in seen and logical == aliases[alias],
                pointer + ': actual alias/owner/logical/physical identity differs or repeats')
            seen.add(identity)
            unit = units[owner.removeprefix('z80:')]
            _require(type(unit) is dict and type(unit.get('rom_base')) is int
                and type(unit.get('extent')) is int and 0 <= logical < unit['extent']
                and physical == unit['rom_base'] + logical, pointer + ': current source geometry differs')
            module, path, node, input_name, result_name = found[alias]
            _require((binding['module'], binding['function'], binding['source'], binding['source_line'])
                == (module, alias, path.relative_to(project).as_posix(), node.lineno)
                and (binding['input_module'], binding['input_class'], binding['result_module'], binding['result_class'])
                == (PACKAGE + '.contexts', input_name, PACKAGE + '.contexts', result_name),
                pointer + ': current exact public source/context identity differs')
            binding['input_fields'] = _schema(binding['input_fields'], pointer + '.input_fields')
            binding['result_fields'] = _schema(binding['result_fields'], pointer + '.result_fields')
            _require(binding['input_fields'] == _context_schema(contexts, input_name)
                and binding['result_fields'] == _context_schema(contexts, result_name),
                pointer + ': complete current immutable context schema differs')
            _require(all(name in CARRIERS or (name, kind) == ('continuation', 'Continuation')
                for name, kind in binding['input_fields'])
                and ('continuation', 'Continuation') in binding['input_fields'],
                pointer + ': only actual input carriers and its own continuation are supported')
            kind = {'initialize_audio_workspace': 'cold_workspace_session',
                'initialize_audio_driver': 'driver_startup_session'}.get(alias, 'typed_context')
            invocation = binding['invocation']
            _require(type(invocation) is dict and invocation.get('kind') == kind
                and type(invocation.get('raw_entry_call_permitted')) is bool
                and invocation['raw_entry_call_permitted'] is (kind == 'typed_context'),
                pointer + ': special nonreturning/startup entry protocol must not become ordinary RET')
            _require(binding['qualification'] ==
                'confirmed_current_source_definition_not_loaded_CodeType_or_reference_execution',
                pointer + ': a source description cannot claim runtime/reference qualification')
            binding['invocation'] = deepcopy(invocation)
            selected.append(Z80CaptureTarget(Z80EntryBinding(**binding), path, pointer, batch_path, node.lineno))
        _require(seen == expected_scope and len({row.binding.alias for row in selected}) == EXPECTED_ENTRIES,
            'the prepared public directory must cover each declared source alias exactly once')
        return tuple(selected)
    except Z80CaptureCatalogError:
        raise
    except (CaptureCatalogError, OSError, UnicodeError, ValueError, TypeError, KeyError,
            AttributeError, RecursionError) as error:
        raise Z80CaptureCatalogError('cannot prepare current public Z80 capture targets: ' + str(error)) from error
