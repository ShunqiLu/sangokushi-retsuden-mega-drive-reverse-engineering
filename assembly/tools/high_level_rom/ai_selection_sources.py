"""Editable first-gate BYTEs for the original 325FC AI candidate selector.

The gate name describes only CMPI.B #1 / BHI at32626. It does not identify
the physical row as a difficulty/personality, nor make a passing candidate
survive the later relation, ruler-head and strict city-count gates.
"""
from __future__ import annotations

from copy import deepcopy


FORMAT = 'g5510-named-ai-candidate-first-gates-v1'
TYPED_FORMAT = 'g5510-ai-selection-fixed-reverse-BYTE-rows-v1'
EDIT_FORMAT = 'g5510-ai-candidate-first-gate-edits-v1'
RESOURCE_ID = 'ai_selection_fields'
_FIRST_GATE = 'first_gate_byte'
_ROW_COUNT = 14
_ROW_BYTES = 14
_ROW_STRIDE = 16
_START = 0x32652
_SOURCE_KEYS = frozenset((
    'canonical_source', 'complete_RAM_algorithm', 'complete_domains_added',
    'confidence', 'consumer_reachability_confidence', 'edited_gameplay_safety',
    'evidence', 'format', 'independent_CPU_comparison', 'natural_domains_added',
    'owner_bytes_added', 'parameter_business_meaning', 'physical_format_confidence',
    'physical_scope', 'policy_interpretation_confidence', 'rows',
))
_ROW_KEYS = frozenset(('id', 'physical_row', 'start', 'end', 'candidates'))
_CANDIDATE_KEYS = frozenset(('id', 'candidate_index', 'address'))
_EDIT_KEYS = frozenset(('row_id', 'candidate_index', 'expected_gate_byte', 'gate_byte'))


def _object(value, keys, label):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError(label + ': complete exact fields required')


def _byte(value):
    if type(value) is not int or not 0 <= value <= 255:
        raise ValueError('one complete unsigned gate BYTE required, never bool')
    return value


def _fixed(value, expected, label):
    if type(value) is not type(expected) or value != expected:
        raise ValueError('original candidate geometry changed: ' + label)


def _validate_candidate(candidate, row, index, *, named):
    field = _FIRST_GATE if named else 'BYTE'
    _object(candidate, _CANDIDATE_KEYS | {field}, 'candidate')
    _fixed(candidate['id'], f'ai_selection_r{row:02d}_candidate_{index:02d}', 'candidate id')
    _fixed(candidate['candidate_index'], index, 'candidate index')
    _fixed(candidate['address'], _START + _ROW_STRIDE * row + index, 'candidate address')
    _byte(candidate[field])


def _validate_row(row, index, *, named):
    _object(row, _ROW_KEYS, 'physical row')
    start = _START + _ROW_STRIDE * index
    for name, value in (('id', f'rom_{start:06X}_ai_selection_row_{index:02d}'),
            ('physical_row', index), ('start', start), ('end', start + _ROW_BYTES)):
        _fixed(row[name], value, name)
    candidates = row['candidates']
    if type(candidates) is not list or len(candidates) != _ROW_BYTES:
        raise ValueError('all fourteen physical candidate BYTEs required')
    for candidate_index, candidate in enumerate(candidates):
        _validate_candidate(candidate, index, candidate_index, named=named)


def _validate(fields, *, named):
    _object(fields, _SOURCE_KEYS, 'AI candidate source')
    _fixed(fields['format'], FORMAT if named else TYPED_FORMAT, 'format')
    rows = fields['rows']
    if type(rows) is not list or len(rows) != _ROW_COUNT:
        raise ValueError('all fourteen original physical rows required')
    for index, row in enumerate(rows):
        _validate_row(row, index, named=named)


def _convert(fields, *, named_output):
    _validate(fields, named=not named_output)
    result = deepcopy(fields)
    result['format'] = FORMAT if named_output else TYPED_FORMAT
    old, new = ('BYTE', _FIRST_GATE) if named_output else (_FIRST_GATE, 'BYTE')
    for row in result['rows']:
        for candidate in row['candidates']:
            candidate[new] = candidate.pop(old)
    return result


def to_named(fields: dict) -> dict:
    """Name all196 BYTEs; preserve metadata, full values and unowned gaps."""
    return _convert(fields, named_output=True)


def from_named(fields: dict) -> dict:
    """Restore the sole typed authority for the unchanged registered encoder."""
    return _convert(fields, named_output=False)


def _review_edits(fields, edits):
    if type(edits) is not list or not edits:
        raise ValueError('one explicit nonempty list of candidate edits required')
    rows = {row['id']: row for row in fields['rows']}
    reviewed, seen = [], set()
    for edit in edits:
        _object(edit, _EDIT_KEYS, 'candidate edit')
        row_id, index = edit['row_id'], edit['candidate_index']
        if type(row_id) is not str or row_id not in rows:
            raise ValueError('edit must name one existing physical row id')
        if type(index) is not int or not 0 <= index < _ROW_BYTES:
            raise ValueError('edit must name a physical candidate index0..13, never bool')
        key = row_id, index
        if key in seen:
            raise ValueError('duplicate candidate edit; no implicit last-write priority')
        seen.add(key)
        before, after = _byte(edit['expected_gate_byte']), _byte(edit['gate_byte'])
        if rows[row_id]['candidates'][index][_FIRST_GATE] != before:
            raise ValueError('candidate gate changed from explicit expected value')
        reviewed.append((row_id, index, after))
    return reviewed


def with_candidate_gates(fields: dict, edits: list[dict]) -> dict:
    """Apply a checked explicit batch without mutating either input.

    Every edit names a real physical row/candidate and its exact previous BYTE.
    Values0/1 remain distinct, values2..255 remain legal, and no later gameplay
    gate, selector arithmetic, stride gap or original bug is normalized.
    """
    _validate(fields, named=True)
    reviewed = _review_edits(fields, edits)
    result = deepcopy(fields)
    rows = {row['id']: row for row in result['rows']}
    for row_id, index, value in reviewed:
        rows[row_id]['candidates'][index][_FIRST_GATE] = value
    return result


def main(argv=None):
    """Convert or explicitly edit fresh own JSON, never read a ROM or encode."""
    import argparse
    import json
    from pathlib import Path
    from .media_sources import MAX_JSON, json_bytes
    from .native import fresh_output
    from .readable_text import _load

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('direction', choices=('export', 'import', 'edit'))
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--edits', type=Path, help='explicit edit document; required only for edit')
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True,
        help='new project/build .json with an existing parent; never overwrite')
    args = parser.parse_args(argv)
    project, output = args.project_root.resolve(strict=True), fresh_output(args.output)
    if (not project.is_dir() or not output.is_relative_to(project / 'build')
            or output == project / 'build' or not output.parent.is_dir()
            or output.suffix != '.json'):
        raise ValueError('explicit fresh JSON under project/build with existing parent required')
    if (args.direction == 'edit') != (args.edits is not None):
        raise ValueError('only edit requires one explicit edits document')
    fields = _load(args.source, MAX_JSON)
    if args.direction == 'edit':
        document = _load(args.edits, MAX_JSON)
        _object(document, {'format', 'edits'}, 'candidate edit document')
        _fixed(document['format'], EDIT_FORMAT, 'edit format')
        result = with_candidate_gates(fields, document['edits'])
    else:
        result = to_named(fields) if args.direction == 'export' else from_named(fields)
    raw = json_bytes(result)
    if len(raw) > MAX_JSON:
        raise ValueError('named candidate source exceeds the existing JSON bound')
    with output.open('xb') as stream:
        stream.write(raw)
    print(json.dumps(dict(output=str(output), bytes=len(raw), format=result['format'],
        source_conversion_or_edit_only=True, original_ROM_read=False,
        resource_encoding_run=False, game_run=False, native_run=False,
        hash_run=False, strict_acceptance=False), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
