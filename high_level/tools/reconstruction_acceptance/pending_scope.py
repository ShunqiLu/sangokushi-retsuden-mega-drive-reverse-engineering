"""Assemble an explicit pending whole-owner scope without executing game code.

All authority paths are caller inputs. Only JSON and current Python ASTs are
read. This is a scope/input-requirement assembler, not a compiler, state oracle,
CPU runner, ledger writer or behavioral acceptance gate.
"""
import argparse
import ast
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re


FORMAT = 'g5510-pending-whole-acceptance-scope-v1'
MAX_TEXT_BYTES = 40_000_000
BASELINE = (1904, 157898, 46004, 203902)
ORDINARY = (403, 42624, 444, 591)
SELECTIONS = (('narrative', (34, 10164, 41, 79)),
    ('remaining', (139, 12098, 157, 188)),
    ('mainlogic', (138, 10654, 150, 216)), ('tail', (92, 9708, 96, 108)))


class ScopeError(ValueError):
    """An authority, geometry or current-source ambiguity must remain visible."""


def _require(condition, message):
    if not condition:
        raise ScopeError(message)


def _integer(value, label, minimum=0, maximum=0x100000):
    _require(type(value) is int and minimum <= value <= maximum, 'invalid exact integer: ' + label)
    return value


def _name(value, label):
    _require(type(value) is str and re.fullmatch(r'[A-Za-z_]\w*', value) is not None,
        'invalid Python identifier: ' + label)
    return value


def _text(path):
    path = Path(path).resolve(strict=True)
    _require(path.is_file() and path.stat().st_size <= MAX_TEXT_BYTES,
        'bounded explicit source/JSON file required: ' + str(path))
    return path.read_text(encoding='utf-8-sig')


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def _json(path):
    value = json.loads(_text(path), object_pairs_hook=_unique_object)
    _require(type(value) is dict, 'explicit JSON object required: ' + str(path))
    return value


@dataclass(frozen=True, order=True)
class Span:
    """A half-open physical CODE interval, never a whole-owner envelope."""
    start: int
    end: int

    def __post_init__(self):
        _integer(self.start, 'span.start')
        _integer(self.end, 'span.end')
        _require(self.start < self.end, 'nonempty physical interval required')


def _spans(rows):
    _require(type(rows) in (list, tuple) and rows, 'all explicit physical spans required')
    result = tuple(Span(*row) for row in rows
        if type(row) in (list, tuple) and len(row) == 2)
    _require(len(result) == len(rows), 'exact start/end pairs required')
    ordered = sorted(result)
    _require(all(left.end <= right.start for left, right in zip(ordered, ordered[1:])),
        'physical spans overlap within one declared owner')
    return result


def _merge(rows, *, disjoint=False):
    result = []
    for row in sorted(rows):
        if result and row.start < result[-1].end:
            _require(not disjoint, 'different declared owners claim overlapping physical CODE')
            result[-1] = Span(result[-1].start, max(result[-1].end, row.end))
        elif result and row.start == result[-1].end:
            result[-1] = Span(result[-1].start, row.end)
        else:
            result.append(row)
    return tuple(result)


def _bytes(rows):
    return sum(row.end - row.start for row in rows)


def _subtract(rows, covered):
    result = []
    for row in rows:
        cursor = row.start
        for old in covered:
            if old.end <= cursor:
                continue
            if old.start >= row.end:
                break
            if cursor < old.start:
                result.append(Span(cursor, old.start))
            cursor = max(cursor, old.end)
            if cursor >= row.end:
                break
        if cursor < row.end:
            result.append(Span(cursor, row.end))
    return tuple(result)


@dataclass(frozen=True)
class EvidenceRef:
    path: str
    pointer: str
    role: str


@dataclass(frozen=True)
class CurrentFunction:
    key: str
    module: str
    field: str
    source: str
    line: int
    end_line: int
    signature: str
    returns: str | None
    frame_named_argument: bool
    frame_annotated_argument: bool
    non_doc_statements: int
    source_status: str = 'confirmed_current_AST_FunctionDef_only'
    callable_CodeType_identity: str = 'unknown_not_loaded'
    complete_logic_and_call_closure: str = 'unknown_not_proved_by_AST_presence'


@dataclass(frozen=True)
class EntryRequirement:
    physical_address: int
    alias: str
    logical_address: int | None
    current_function_candidates: tuple[str, ...]
    selected_current_function: str | None
    mapping_basis: str
    field_hint: str | None
    explicit_state_input_status: str = 'unknown_not_supplied'
    original_caller_return_and_full_frame_proof: str = 'unknown_not_executed'
    required_result_status: str = 'pending_no_expected_registers_or_RAM_fabricated'


@dataclass(frozen=True)
class PendingOwner:
    key: str
    architecture: str
    family: str
    name: str
    start: int
    whole_spans: tuple[Span, ...]
    pending_spans: tuple[Span, ...]
    accepted_overlap_spans: tuple[Span, ...]
    entries: tuple[EntryRequirement, ...]
    source_module: str | None
    geometry_origin: EvidenceRef
    current_geometry_refs: tuple[EvidenceRef, ...]
    whole_status: str
    instruction_rows: int | None = None
    source_functions: tuple[str, ...] = ()
    dependency_proof: str = 'unknown_current_callee_and_device_closure_not_executed'
    behavioral_acceptance: str = 'pending_no_runtime_claim'


@dataclass(frozen=True)
class ScopeInputs:
    project_root: Path
    ledger: Path
    narrative_selection: Path
    remaining_selection: Path
    mainlogic_selection: Path
    tail_selection: Path
    audio_mapping: Path
    audio_target: Path
    entry_hints: Path | None = None


@dataclass(frozen=True)
class PendingScope:
    format: str
    authority: EvidenceRef
    authority_counts: tuple[int, int, int, int]
    input_references: tuple[EvidenceRef, ...]
    owners: tuple[PendingOwner, ...]
    current_functions: tuple[CurrentFunction, ...]
    unresolved_entry_count: int
    named_candidate_only_entry_count: int
    current_source_files: tuple[str, ...]

    def summary(self):
        ordinary = tuple(row for row in self.owners if row.architecture == 'm68000')
        audio = tuple(row for row in self.owners if row.architecture == 'z80')
        groups = {}
        for owner in self.owners:
            count = groups.setdefault(owner.family, [0, 0, 0, 0])
            count[0] += 1
            count[1] += _bytes(owner.pending_spans)
            count[2] += len(owner.entries)
            count[3] += len(owner.whole_spans)
        return dict(format=self.format, confidence='confirmed_scope_geometry_and_current_AST_locations_only',
            strict_authority_counts=list(self.authority_counts),
            ordinary_geometry=[len(ordinary), sum(_bytes(row.pending_spans) for row in ordinary),
                sum(len(row.entries) for row in ordinary), sum(len(row.whole_spans) for row in ordinary)],
            audio_geometry=[len(audio), sum(_bytes(row.pending_spans) for row in audio),
                sum(len(row.entries) for row in audio), sum(len(row.whole_spans) for row in audio)],
            pending_CODE_bytes=sum(_bytes(row.pending_spans) for row in self.owners),
            partially_accepted_owners=sum(row.whole_status == 'partially_accepted_requires_whole_reconciliation'
                for row in self.owners), current_function_records=len(self.current_functions),
            unresolved_entry_count=self.unresolved_entry_count,
            named_candidate_only_entry_count=self.named_candidate_only_entry_count,
            family_geometry=groups, complete_initial_state_inputs=False,
            current_call_closure='unknown', executable_CasePlan='not_yet_supplied',
            game=False, fixture=False, normal_compiler_API=False, native=False,
            CPU=False, hash=False, old_success_replay=False, ledger_modified=False,
            formal_new_CODE_bytes=0, strict_pending_unchanged=self.authority_counts[2])

    def to_dict(self):
        return dict(summary=self.summary(), scope=asdict(self))


class _SourceIndex:
    """A current-source locator. It never imports or evaluates a source file."""
    def __init__(self, project):
        self.project = project.resolve(strict=True)
        self.trees, self.functions, self.records = {}, {}, {}

    def module_path(self, module):
        _require(type(module) is str and re.fullmatch(r'tools(?:\.[A-Za-z_]\w*)+', module),
            'explicit project module name required')
        path = (self.project / (module.replace('.', '/') + '.py')).resolve(strict=True)
        _require(path.is_relative_to(self.project), 'current source escaped explicit project root')
        return path

    def tree(self, module):
        if module not in self.trees:
            path = self.module_path(module)
            tree = ast.parse(_text(path), filename=str(path))
            functions = {}
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    _require(node.name not in functions, 'duplicate top-level source callable: ' + module + ':' + node.name)
                    functions[node.name] = node
            self.trees[module], self.functions[module] = tree, functions
        return self.trees[module]

    def locate(self, module, field, trail=()):
        _name(field, 'field')
        if (module, field) in trail or len(trail) >= 16:
            return None
        try:
            tree = self.tree(module)
        except FileNotFoundError:
            return None
        if field in self.functions[module]:
            node = self.functions[module][field]
            key = module + ':' + field
            if key not in self.records:
                args = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
                body = [row for row in node.body if not (isinstance(row, ast.Expr)
                    and isinstance(row.value, ast.Constant) and type(row.value.value) is str)]
                self.records[key] = CurrentFunction(key, module, field,
                    self.module_path(module).relative_to(self.project).as_posix(),
                    node.lineno, node.end_lineno, ast.unparse(node.args),
                    ast.unparse(node.returns) if node.returns else None,
                    any(arg.arg in ('frame', 'fields') for arg in args),
                    any(arg.annotation is not None and 'Frame' in ast.unparse(arg.annotation) for arg in args),
                    len(body))
            return key
        imports = []
        for node in tree.body:
            if not isinstance(node, ast.ImportFrom) or node.module is None:
                continue
            for alias in node.names:
                if (alias.asname or alias.name) != field or alias.name == '*':
                    continue
                if node.level:
                    parts = module.split('.')[:-1]
                    if node.level > len(parts):
                        continue
                    dependency = '.'.join(parts[:len(parts)-node.level+1] + node.module.split('.'))
                else:
                    dependency = node.module
                if dependency.startswith('tools.'):
                    imports.append((dependency, alias.name))
        _require(len(imports) <= 1, 'ambiguous static reexport: ' + module + ':' + field)
        if not imports:
            return None
        return self.locate(*imports[0], trail=trail + ((module, field),))


def _literal_assignment(tree, name):
    rows = [node.value for node in tree.body if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)]
    _require(rows, 'explicit literal target assignment required: ' + name)
    # Python's last top-level assignment is the current value; no code is run.
    return rows[-1]


def _current_bindings(index, module, owner):
    target_module = module.rsplit('.', 1)[0] + '.target'
    tree = index.tree(target_module)
    matches = []
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        tables = [item.id for item in node.targets if isinstance(item, ast.Name)]
        for call in ast.walk(node.value):
            if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Name) or call.func.id != 'Binding':
                continue
            if call.keywords:
                continue
            try:
                row = [ast.literal_eval(item) for item in call.args]
            except (ValueError, TypeError):
                continue
            if len(row) in (3, 4):
                name, start, end = row[:3]
                entries, spans = ((start, name),), ((start, end),)
            elif len(row) == 6:
                name, start, entries, spans = row[:4]
            else:
                continue
            if name != owner['name'] or start != owner['start']:
                continue
            _require(sorted(tuple(item) for item in entries) == sorted(owner['entries'])
                and sorted(_spans(spans)) == sorted(owner['spans']),
                'historical whole geometry differs from the current literal Binding: ' + name)
            matches.append(EvidenceRef(str(index.module_path(target_module)),
                ':'.join(tables) + ':' + name + '@line' + str(call.lineno),
                'confirmed_current_literal_Binding_geometry_not_behavior'))
    _require(matches, 'whole owner lacks a matching current literal Binding: ' + owner['name'])
    return tuple(matches)


def _read_hints(path):
    if path is None:
        return {}
    document = _json(path)
    rows = []
    if document.get('format') == 'g5510-pending-entry-hints-v1':
        _require(type(document.get('entries')) is list, 'explicit entry hints list required')
        rows = [(row['module'], row['entry'], row['field']) for row in document['entries']]
    elif type(document.get('candidates')) is list:
        # Historical inventories contribute names only; no cached rows or old
        # source text becomes a current function, geometry or native authority.
        rows = [(owner['module'], row['entry'], row['field'])
            for owner in document['candidates'] for row in owner.get('fields', ())]
    else:
        raise ScopeError('explicit entry-hints schema or historical candidate-name inventory required')
    result = {}
    for module, entry, field in rows:
        _integer(entry, 'hint.entry')
        _name(field, 'hint.field')
        key = module, entry
        _require(key not in result or result[key] == field, 'conflicting explicit entry field hints')
        result[key] = field
    return result


def _entry(index, module, address, alias, hints, explicit_field=None, logical=None, source_candidates=()):
    _integer(address, 'entry.address')
    _name(alias, 'entry.alias')
    hint = hints.get((module, address)) if module else None
    hinted = hint or explicit_field
    names = list(dict.fromkeys([name for name in (hinted, alias + '_fields',
        alias + '_frame_fields', alias + '_complete', alias) if name is not None]))
    candidates = []
    if module:
        for name in names:
            key = index.locate(module, name)
            if key and key not in candidates:
                candidates.append(key)
    for source_module, field in source_candidates:
        key = index.locate(source_module, field)
        if key and key not in candidates:
            candidates.append(key)
    selected = index.locate(module, hinted) if module and hinted else None
    if selected:
        basis = 'explicit_or_historical_field_name_resolved_in_current_AST_not_ABI_proof'
    elif len(candidates) == 1:
        selected, basis = candidates[0], 'single_named_current_AST_candidate_not_entry_ABI_proof'
    elif candidates:
        basis = 'ambiguous_current_AST_candidates_require_explicit_entry_mapping'
    else:
        basis = 'unknown_no_matching_current_AST_FunctionDef'
    return EntryRequirement(address, alias, logical, tuple(candidates), selected, basis, hinted)


def _owner(raw, family, module, evidence):
    _require(type(raw) is dict, 'one explicit complete whole-owner row required')
    name = _name(raw['name'], 'owner.name')
    start = _integer(raw.get('start', raw.get('entry')), 'owner.start')
    entries = tuple((int(row[0]), _name(row[1], 'alias')) for row in raw['entries'])
    _require(entries and len(set(entries)) == len(entries)
        and all(type(row[0]) is int for row in raw['entries']), 'all unique exact own aliases required')
    spans = _spans(raw.get('spans', raw.get('segments')))
    _require(all(any(span.start <= address < span.end for span in spans) for address, alias in entries),
        'own entry lies outside its actual owner CODE spans')
    _require(any(span.start <= start < span.end for span in spans), 'whole start lies outside CODE spans')
    if 'bytes' in raw:
        _require(type(raw['bytes']) is int and raw['bytes'] == _bytes(spans), 'declared whole CODE size differs')
    return dict(name=name, start=start, family=family, module=module, entries=entries,
        spans=spans, evidence=evidence, field=raw.get('field'))


def _selection(path, kind):
    document = _json(path)
    absolute = str(Path(path).resolve(strict=True))
    result = []
    if kind == 'narrative':
        for fi, family in enumerate(document['family_results']):
            module = family.get('business') or family.get('source_path', '').removesuffix('.py').replace('/', '.')
            if not module:
                module = family['compiler'].replace('.compiler_', '.business_')
            for oi, row in enumerate(family['selected_owners']):
                binding = row.get('binding', row)
                result.append(_owner(binding, family['family'], module,
                    EvidenceRef(absolute, '/family_results/' + str(fi) + '/selected_owners/' + str(oi),
                        'historical_whole_geometry_only_not_current_source_evidence')))
    elif kind in ('remaining', 'mainlogic'):
        for oi, row in enumerate(document['selected_whole_owners']):
            result.append(_owner(row, row['family'], row['module'], EvidenceRef(absolute,
                '/selected_whole_owners/' + str(oi), 'historical_ledger_difference_whole_geometry_only')))
    elif kind == 'tail':
        for fi, family in enumerate(document['families']):
            for oi, row in enumerate(family['selected_owners']):
                result.append(_owner(row, family['family'], row['module'], EvidenceRef(absolute,
                    '/families/' + str(fi) + '/selected_owners/' + str(oi), 'historical_ledger_difference_whole_geometry_only')))
    else:
        raise ScopeError('one of the four explicit complete selection schemas required')
    geometry = (len(result), sum(_bytes(row['spans']) for row in result),
        sum(len(row['entries']) for row in result), sum(len(row['spans']) for row in result))
    expected = dict(SELECTIONS)[kind]
    _require(geometry == expected, 'complete selection geometry differs: ' + kind)
    return result


def _ledger(path):
    document = _json(path)
    actual = tuple(document[name] for name in ('registered_physical_units', 'strict_BYTES',
        'remaining_strict_BYTES', 'denominator_CODE_BYTES'))
    _require(actual == BASELINE and len(document['units']) == actual[0],
        'the exact explicitly supplied106 authority is required, not a historical replacement')
    raw = tuple(Span(_integer(row['entry'], 'registered.start'), _integer(row['end'], 'registered.end'))
        for row in document['units'])
    covered = _merge(raw, disjoint=True)
    _require(_bytes(covered) == actual[1] and actual[1] + actual[2] == actual[3],
        'authority physical union or declared denominator differs')
    return actual, covered


def _pending_owner(row, covered, index, hints):
    whole = row['spans']
    pending = _subtract(whole, covered)
    overlap = _subtract(whole, pending)
    status = 'whole_unaccepted' if not overlap else 'partially_accepted_requires_whole_reconciliation'
    if not pending:
        return None
    entries = tuple(_entry(index, row['module'], address, alias, hints,
        explicit_field=row['field'] if len(row['entries']) == 1 else None)
        for address, alias in row['entries'])
    return PendingOwner('m68000:' + row['module'] + ':' + row['name'], 'm68000', row['family'],
        row['name'], row['start'], whole, pending, overlap, entries, row['module'], row['evidence'],
        _current_bindings(index, row['module'], row), status)


def _dictionary_literal_fields(node, names):
    _require(isinstance(node, ast.Dict), 'literal source-operation dictionary required')
    result = {}
    for key, value in zip(node.keys, node.values):
        if isinstance(key, ast.Constant) and key.value in names:
            result[key.value] = ast.literal_eval(value)
    _require(set(result) == set(names), 'complete source-operation identity fields required')
    return result


def _audio(inputs, covered, index, hints):
    target_path = Path(inputs.audio_target).resolve(strict=True)
    _require(target_path.is_relative_to(index.project), 'explicit current audio target must be inside project')
    target_module = '.'.join(target_path.relative_to(index.project).with_suffix('').parts)
    tree = index.tree(target_module)
    units = ast.literal_eval(_literal_assignment(tree, 'UNITS'))
    _require(set(units) == {'startup', 'driver'}, 'two distinct complete current Z80 units required')
    document = _json(inputs.audio_mapping)
    _require(document.get('generated_target_bytes') == 3380 and document.get('parent_exit') == 0,
        'the explicit saved3380 instruction mapping is required, not an image or current behavior proof')
    sites_node = _literal_assignment(tree, 'OPERATION_SITES')
    _require(isinstance(sites_node, (ast.Tuple, ast.List)), 'literal actual operation-site directory required')
    sites = [_dictionary_literal_fields(node, ('unit', 'address', 'source', 'function')) for node in sites_node.elts]
    function_addresses = ast.literal_eval(_literal_assignment(tree, 'CALLEE_ADDRESSES'))
    audio_package = target_module.rsplit('.', 1)[0]
    result = []
    for name in ('startup', 'driver'):
        unit = units[name]
        base, extent = _integer(unit['rom_base'], 'audio.rom_base'), _integer(unit['extent'], 'audio.extent')
        rows = unit['rows']
        saved = document['actual_units'][name]
        mapping = saved['actual_instruction_mapping']
        _require(len(rows) == len(mapping) == saved['instructions'], 'all saved/current Z80 instructions required')
        instruction_spans = []
        for current, old in zip(rows, mapping):
            address = _integer(current['address'], 'audio.logical_address')
            width = _integer(current['size'], 'audio.instruction_size', 1, extent)
            _require(address + width <= extent and old['logical_pc'] == address and old['width'] == width
                and old['rom_pc'] == base + address and old['actual_start'] == address
                and old['actual_end'] == address + width, 'saved mapping differs from current literal CODE rows')
            instruction_spans.append(Span(base + address, base + address + width))
        whole = _merge(instruction_spans, disjoint=True)
        expected = (38, 1, 25) if name == 'startup' else (3342, 17, 1687)
        _require((_bytes(whole), len(whole), len(rows)) == expected
            and saved['instruction_bytes'] == expected[0], 'complete Z80 CODE geometry differs')
        pending = _subtract(whole, covered)
        overlap = _subtract(whole, pending)
        _require(pending, 'audio unit already accepted; this fixed remaining scope must be revised explicitly')
        unit_sites = [row for row in sites if row['unit'] == name]
        site_points = {(row['address']) for row in unit_sites}
        _require(site_points == {row['address'] for row in rows}, 'source-operation sites omit or invent CODE rows')
        locations = sorted({(audio_package + '.' + row['source'].removesuffix('.py'), row['function'])
            for row in unit_sites})
        functions = tuple(sorted({key for module, field in locations
            if (key := index.locate(module, field)) is not None}))
        entries = []
        for alias, address in function_addresses.items():
            if (name == 'startup') != (alias == 'initialize_audio_workspace'):
                continue
            _integer(address, 'Z80 callee address')
            _require(any(span.start <= base + address < span.end for span in whole),
                'named Z80 original entry lies outside actual CODE')
            candidates = tuple((module, field) for module, field in locations if field == alias)
            entry = _entry(index, None, base + address, alias, hints, logical=address,
                source_candidates=candidates)
            entries.append(entry)
        _require(entries, 'all declared named Z80 function entries required')
        result.append(PendingOwner('z80:' + name, 'z80', 'audio_' + name, name, base, whole, pending, overlap,
            tuple(entries), None, EvidenceRef(str(Path(inputs.audio_mapping).resolve(strict=True)),
                '/actual_units/' + name + '/actual_instruction_mapping',
                'saved_instruction_geometry_only_old_source_and_native_claims_not_relabelled'),
            (EvidenceRef(str(target_path), '/UNITS/' + name,
                'confirmed_current_literal_instruction_geometry_not_CPU_or_native_acceptance'),
             EvidenceRef(str(target_path), '/OPERATION_SITES', 'source_name_locator_only_normalization_not_executed')),
            'whole_unaccepted' if not overlap else 'partially_accepted_requires_whole_reconciliation',
            len(rows), functions))
    return tuple(result)


def build_pending_scope(inputs):
    """Return immutable scope plus unsatisfied case requirements, never run them.

    The input schema is intentionally tied to the declared106 baseline and its
    four complete remaining selections. Every path, including optional name
    hints, is supplied by the caller; there is no private-machine fallback.
    """
    _require(type(inputs) is ScopeInputs, 'exact explicit ScopeInputs required')
    index = _SourceIndex(Path(inputs.project_root))
    counts, covered = _ledger(inputs.ledger)
    hints = _read_hints(inputs.entry_hints)
    owners, raw_rows, references = [], [], []
    for kind, expected in SELECTIONS:
        path = getattr(inputs, kind + '_selection')
        rows = _selection(path, kind)
        raw_rows.extend(rows)
        references.append(EvidenceRef(str(Path(path).resolve(strict=True)), '',
            'historical_selection_geometry_not_current_source_or_behavior'))
        for row in rows:
            owner = _pending_owner(row, covered, index, hints)
            if owner is not None:
                owners.append(owner)
    # Prove finite declared geometry is disjoint. Preserve the original591
    # owner spans separately, not only this merged physical set.
    raw_union = _merge([span for row in raw_rows for span in row['spans']], disjoint=True)
    pending_union = _subtract(raw_union, covered)
    ordinary_geometry = (len(owners), _bytes(pending_union), sum(len(row.entries) for row in owners),
        sum(len(row.whole_spans) for row in owners))
    _require(ordinary_geometry == ORDINARY, 'current ledger difference is not the complete403/42624/444/591 scope')
    audio = _audio(inputs, covered, index, hints)
    owners.extend(audio)
    all_pending = _merge([span for owner in owners for span in owner.pending_spans], disjoint=True)
    _require(_bytes(all_pending) == counts[2], 'pending physical difference does not cover exactly46004 CODE bytes')
    _require(_bytes(_subtract(all_pending, covered)) == _bytes(all_pending), 'already accepted CODE entered pending output')
    references.extend((EvidenceRef(str(Path(inputs.audio_mapping).resolve(strict=True)), '', 'saved_mapping_only'),
        EvidenceRef(str(Path(inputs.audio_target).resolve(strict=True)), '', 'current_literal_audio_target_AST')))
    if inputs.entry_hints is not None:
        references.append(EvidenceRef(str(Path(inputs.entry_hints).resolve(strict=True)), '',
            'names_only_every_match_checked_in_current_AST'))
    entries = [entry for owner in owners for entry in owner.entries]
    return PendingScope(FORMAT, EvidenceRef(str(Path(inputs.ledger).resolve(strict=True)), '/units',
        'read_only_strict_authority_no_registration'), counts, tuple(references), tuple(owners),
        tuple(index.records[key] for key in sorted(index.records)),
        sum(not entry.current_function_candidates for entry in entries),
        sum(entry.mapping_basis in ('single_named_current_AST_candidate_not_entry_ABI_proof',
            'ambiguous_current_AST_candidates_require_explicit_entry_mapping') for entry in entries),
        tuple(sorted(index.module_path(module).relative_to(index.project).as_posix() for module in index.trees)))


def argument_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('project-root', 'ledger', 'narrative-selection', 'remaining-selection',
            'mainlogic-selection', 'tail-selection', 'audio-mapping', 'audio-target'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--entry-hints', type=Path)
    return parser


def main():
    parser = argument_parser()
    parser.add_argument('--emit', choices=('summary', 'json'), default='summary',
        help='JSON stdout only; summary avoids a large scope dump by default')
    args = parser.parse_args()
    scope = build_pending_scope(ScopeInputs(**{name: getattr(args, name)
        for name in ScopeInputs.__dataclass_fields__}))
    print(json.dumps(scope.summary() if args.emit == 'summary' else scope.to_dict(),
        ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
