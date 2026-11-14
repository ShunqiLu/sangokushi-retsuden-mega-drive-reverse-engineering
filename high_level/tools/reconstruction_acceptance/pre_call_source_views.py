"""Prepare exact public/private helper source forms, without running a helper.

Preparation may read sources, import definition modules and compile definitions.
The matching path only inspects already prepared objects and a real live frame.
It does not qualify a private namespace, execute a callee or grant strict credit.
"""
from __future__ import annotations

import ast
import copy
from dataclasses import dataclass, field
from pathlib import Path
import stat
import struct
import sys
from types import CodeType, FrameType, FunctionType, ModuleType

from .entry_capture_catalog import MAX_SOURCE_BYTES, _bounded_text, _dump
from .pre_call_capture_catalog import (
    CURRENT_HELPERS, HELPERS, MISSING_QUALIFICATION, PreCallHelper, PreparedPreCallIndex,
)


class PreCallSourceViewError(ValueError):
    """Changed source/owners are preparation boundaries, never cache hits."""


_EXECUTION_FIELDS = (
    'co_name', 'co_qualname', 'co_argcount', 'co_posonlyargcount',
    'co_kwonlyargcount', 'co_nlocals', 'co_stacksize', 'co_flags', 'co_code',
    'co_names', 'co_varnames', 'co_freevars', 'co_cellvars', 'co_exceptiontable',
)
PUBLIC_FORM = 'public_original'
PRIVATE_FORM = 'source_derived_private'
_COMMAND_MODULE = 'tools.high_level_main_flows.command_message_steps'
_CITY_MODULE = 'tools.high_level_main_flows.city_scene_steps'
_PREPARATION_MODULE = 'tools.high_level_gameplay_flow.battle_preparation_steps'


def _require(condition, message):
    if not condition:
        raise PreCallSourceViewError(message)


def _constant_shape(value):
    if type(value) is CodeType:
        return ('code', _code_shape(value))
    if type(value) is tuple:
        return ('tuple', tuple(_constant_shape(item) for item in value))
    if type(value) is frozenset:
        return ('frozenset', frozenset(_constant_shape(item) for item in value))
    if type(value) is float:
        return ('float', struct.pack('>d', value))
    if type(value) is complex:
        return ('complex', struct.pack('>dd', value.real, value.imag))
    if value is Ellipsis:
        return ('ellipsis',)
    _require(type(value) in (str, bytes, int, bool, type(None)),
        'unsupported executable constant in an actual helper CodeType')
    return (type(value).__name__, value)


def _code_shape(code):
    """All executable fields, recursively; filename/line tables are not identity."""
    _require(type(code) is CodeType, 'an actual immutable CodeType is required')
    return (tuple((name, getattr(code, name)) for name in _EXECUTION_FIELDS),
        tuple(_constant_shape(value) for value in code.co_consts))


def _top_code(compiled, function):
    found = tuple(value for value in compiled.co_consts if type(value) is CodeType
        and value.co_name == function and value.co_qualname == function)
    _require(len(found) == 1, 'one complete top-level helper CodeType required: ' + function)
    return found[0]


@dataclass(frozen=True)
class PreparedHelperForm:
    helper: PreCallHelper
    original: FunctionType
    original_code: CodeType
    candidate_code: CodeType
    source_form: str
    source_transformer: str | None
    candidate_shape: tuple = field(init=False, repr=False)
    expected_provenance: tuple[tuple[str, str], ...] = field(init=False, repr=False)
    _module: ModuleType = field(init=False, repr=False, compare=False)
    _package: str = field(init=False, repr=False)

    def __post_init__(self):
        _require(type(self.helper) is PreCallHelper and type(self.original) is FunctionType,
            'one prepared helper source and its actual public FunctionType are required')
        module = sys.modules.get(self.helper.module)
        _require(type(module) is ModuleType, 'actual helper definition module is not loaded')
        _require(self.source_form in (PUBLIC_FORM, PRIVATE_FORM)
            and (self.source_transformer is None) == (self.source_form == PUBLIC_FORM),
            'explicit public or named source-derived helper form required')
        _require(type(self.original_code) is CodeType and type(self.candidate_code) is CodeType
            and self.candidate_code.co_name == self.helper.function
            and self.candidate_code.co_qualname == self.helper.function,
            'the candidate must retain the complete original helper name/qualname')
        package = self.helper.module.rpartition('.')[0]
        _require(module.__package__ == package, 'actual helper package differs')
        object.__setattr__(self, '_module', module)
        object.__setattr__(self, '_package', package)
        object.__setattr__(self, 'candidate_shape', _code_shape(self.candidate_code))
        object.__setattr__(self, 'expected_provenance', (
            ('helper', self.helper.key), ('source_path', str(self.helper.source_path)),
            ('complete_source_AST', self.helper.complete_source_AST),
            ('source_form', self.source_form),
            ('source_transformer', self.source_transformer or 'none_public_original'),
        ))
        _require_current_original(self)

    @property
    def missing_qualification(self):
        missing = MISSING_QUALIFICATION
        if self.source_form == PRIVATE_FORM:
            missing += ('actual_private_namespace_bindings_and_execution_closure_not_qualified',)
        if self.helper.function in ('_highbank_recovery_call_fields', '_city_ui_child_fields'):
            missing += ('private_source_form_unknown_no_actual_derived_owner_prepared',)
        return missing


def _require_current_original(form):
    module, owner = form._module, form.original
    _require(sys.modules.get(form.helper.module) is module
        and vars(module).get(form.helper.function) is owner
        and owner.__code__ is form.original_code
        and owner.__globals__ is vars(module)
        and owner.__module__ == form.helper.module
        and owner.__name__ == form.helper.function
        and owner.__qualname__ == form.helper.function
        and owner.__closure__ is None,
        'actual public helper module/owner/CodeType changed: ' + form.helper.key)


def _read_tree(path, cache):
    path = Path(path)
    _require(path.is_absolute() and path.suffix == '.py', 'explicit absolute Python source path required')
    for member in (path, *path.parents):
        info = member.lstat()
        _require(not stat.S_ISLNK(info.st_mode)
            and not getattr(info, 'st_file_attributes', 0) & 0x400,
            'helper source cannot traverse a reparse path')
    path = path.resolve(strict=True)
    if path not in cache:
        cache[path] = ast.parse(_bounded_text(path, MAX_SOURCE_BYTES,
            'pre-CALL helper source'), filename=str(path))
    return cache[path]


def _definition(tree, function):
    nodes = tuple(node for node in tree.body
        if type(node) is ast.FunctionDef and node.name == function)
    _require(len(nodes) == 1 and not nodes[0].decorator_list,
        'one complete undecorated helper definition required: ' + function)
    return nodes[0]


def _definition_code(node, filename):
    # Compile, never exec: no annotations/defaults or business body are evaluated.
    tree = ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(node)], type_ignores=[]))
    return _top_code(compile(tree, filename, 'exec', dont_inherit=True), node.name)


def _public_owner(helper, tree, modules):
    node = _definition(tree, helper.function)
    _require(_dump(node) == helper.complete_source_AST,
        'current complete helper source differs from catalog pin: ' + helper.key)
    module = modules[helper.module]
    _require(Path(module.__file__).resolve(strict=True) == helper.source_path.resolve(strict=True),
        'loaded helper module comes from another source path: ' + helper.key)
    owner = vars(module).get(helper.function)
    _require(type(owner) is FunctionType and owner.__globals__ is vars(module)
        and owner.__module__ == helper.module and owner.__name__ == helper.function
        and owner.__qualname__ == helper.function and owner.__closure__ is None,
        'actual complete public helper FunctionType required: ' + helper.key)
    plain = _top_code(compile(tree, str(helper.source_path), 'exec',
        dont_inherit=True), helper.function)
    _require(_code_shape(plain) == _code_shape(owner.__code__),
        'loaded helper executable fields differ from complete pinned source: ' + helper.key)
    return owner, node


def _transformer(module, function, cache):
    module_name = module.__name__
    tree = _read_tree(Path(module.__file__), cache)
    node = _definition(tree, function)
    owner = vars(module).get(function)
    _require(type(owner) is FunctionType and owner.__globals__ is vars(module)
        and owner.__module__ == module_name and owner.__name__ == function
        and owner.__qualname__ == function and owner.__closure__ is None
        and _code_shape(owner.__code__) == _code_shape(_top_code(
            compile(tree, module.__file__, 'exec', dont_inherit=True), function)),
        'the actual runtime transformer differs from its current complete source')
    return owner


def prepare_helper_forms(index: PreparedPreCallIndex) -> tuple[PreparedHelperForm, ...]:
    """Prepare legacy five or current ten forms; no Programs/state/monitor/case."""
    _require(type(index) is PreparedPreCallIndex
        and tuple((row.module, row.function) for row in index.helpers) in (HELPERS, CURRENT_HELPERS),
        'the actual explicit legacy-three or current-six pre-CALL catalog is required')
    from ..high_level_remaining_flows import business_lowbank, business_highbank
    from ..high_level_main_flows import command_message_steps, city_scene_steps
    modules = {
        'tools.high_level_remaining_flows.business_lowbank': business_lowbank,
        'tools.high_level_remaining_flows.business_highbank': business_highbank,
    }
    if tuple((row.module, row.function) for row in index.helpers) == CURRENT_HELPERS:
        from ..high_level_main_flows import business_main, business_gameplay, business_commands
        from ..high_level_gameplay_flow import battle_preparation_steps
        modules.update({
            'tools.high_level_main_flows.business_main': business_main,
            'tools.high_level_main_flows.business_gameplay': business_gameplay,
            'tools.high_level_main_flows.business_commands': business_commands,
        })
    cache, forms = {}, []
    for helper in index.helpers:
        tree = _read_tree(helper.source_path, cache)
        owner, node = _public_owner(helper, tree, modules)
        forms.append(PreparedHelperForm(helper, owner, owner.__code__, owner.__code__,
            PUBLIC_FORM, None))
        if helper.function == '_command_policy_call_fields':
            transform = _transformer(command_message_steps, '_cooperative_tree', cache)
            derived, _ = transform('highbank', copy.deepcopy(node))
            candidate = _definition_code(derived, '<finite command message continuation>')
            transformer_name = _COMMAND_MODULE + ':_cooperative_tree'
        elif helper.function == '_lowbank_ui_call_fields':
            transform = _transformer(city_scene_steps, '_cooperative_module', cache)
            derived, _ = transform('lowbank', copy.deepcopy(tree))
            candidate = _top_code(compile(derived, str(helper.source_path), 'exec',
                dont_inherit=True), helper.function)
            transformer_name = _CITY_MODULE + ':_cooperative_module'
        elif helper.function == '_campaign_call_fields':
            transform = _transformer(command_message_steps, '_cooperative_tree', cache)
            derived, _ = transform('main', copy.deepcopy(node))
            candidate = _definition_code(derived, '<finite command message continuation>')
            transformer_name = _COMMAND_MODULE + ':_cooperative_tree'
        elif helper.function == '_game_text_call_fields':
            transform = _transformer(battle_preparation_steps, '_cooperative_preparation_tree', cache)
            derived = transform('gameplay', copy.deepcopy(tree))
            candidate = _top_code(compile(derived, str(helper.source_path), 'exec',
                dont_inherit=True), helper.function)
            transformer_name = _PREPARATION_MODULE + ':_cooperative_preparation_tree'
        else:
            # Recovery/Commands child have no proven derived form here.
            continue
        forms.append(PreparedHelperForm(helper, owner, owner.__code__, candidate,
            PRIVATE_FORM, transformer_name))
    return tuple(forms)


def match_helper_form(forms: tuple[PreparedHelperForm, ...], code: CodeType,
        live: FrameType) -> PreparedHelperForm | None:
    """Identify an actual frame using prepared forms only; no I/O/import/compile.

    A private match proves a source-derived code shape and module/package labels,
    not that its private aliases, namespace or callee execution closure qualify.
    """
    _require(type(forms) is tuple and all(type(row) is PreparedHelperForm for row in forms)
        and type(code) is CodeType and type(live) is FrameType and live.f_code is code,
        'actual prepared forms, live Python frame and identical CodeType required')
    possible = tuple(form for form in forms if form.helper.function == code.co_name)
    for form in possible:
        _require_current_original(form)
    if not possible:
        return None
    shape = _code_shape(code)
    matches = tuple(form for form in possible if shape == form.candidate_shape
        and live.f_globals.get('__name__') == form.helper.module
        and live.f_globals.get('__package__') == form._package
        and (form.source_form == PRIVATE_FORM or
            code is form.original_code and live.f_globals is vars(form._module)))
    _require(len(matches) <= 1, 'ambiguous prepared actual helper source form')
    return matches[0] if matches else None
