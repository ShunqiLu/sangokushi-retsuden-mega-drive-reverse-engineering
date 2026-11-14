"""One editable authority for the complete AI command cutoff-pair resource.

The names describe proven compare operands, not guessed difficulty levels,
officer identities or natural selector bounds. The first primary WORD is also
read as a defense-plan base; that alias is not duplicated into a second value.
All provenance, unknown-index meanings and unowned-gap metadata are retained.
"""
from __future__ import annotations

from copy import deepcopy


FORMAT = 'g5510-named-ai-command-cutoffs-v1'
TYPED_FORMAT = 'g5510-AI-threshold-literal-WORD-pair-fields-v1'
EDIT_FORMAT = 'g5510-ai-command-cutoff-pair-edits-v1'
RESOURCE_ID = 'ai_threshold_pair_fields'
_SOURCE_KEYS = frozenset((
    'business_meanings', 'canonical_source', 'complete_domains_added',
    'confidence', 'edited_gameplay_safety', 'evidence', 'format',
    'independent_CPU_comparison', 'natural_domains_added', 'owner_bytes_added',
    'physical_scope', 'preserved_raw_gaps', 'primary_groups', 'secondary',
    'source_confidence',
))
_GROUP_KEYS = frozenset(('WORD_order', 'end', 'group_index', 'pair_count', 'pairs', 'start'))
_SECONDARY_KEYS = _GROUP_KEYS - {'group_index'}
_PAIR_METADATA = frozenset(('end', 'pair_index', 'start'))
_NAMED_WORDS = ('first_cutoff_word', 'second_cutoff_word')
_EDIT_KEYS = frozenset(('table', 'pair_index', 'field', 'expected_word', 'word'))


def _object(value, keys, context):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError(context + ': complete exact source fields are required')


def _word(value):
    if type(value) is not int or not 0 <= value <= 65535:
        raise ValueError('cutoff must be a complete unsigned WORD, not bool')
    return value


def _pair_values(pair, *, named):
    _object(pair, _PAIR_METADATA | (set(_NAMED_WORDS) if named else {'WORDs'}), 'cutoff pair')
    if named:
        return [_word(pair[name]) for name in _NAMED_WORDS]
    values = pair['WORDs']
    if type(values) is not list or len(values) != 2:
        raise ValueError('one complete ordered pair of WORDs is required')
    return [_word(value) for value in values]


def _validate_group(group, start, count, *, named, group_index=None):
    _object(group, _SECONDARY_KEYS if group_index is None else _GROUP_KEYS, 'cutoff group')
    expected = {'WORD_order': 'big', 'start': start, 'end': start + count * 4, 'pair_count': count}
    if group_index is not None:
        expected['group_index'] = group_index
    for name, value in expected.items():
        if type(group[name]) is not type(value) or group[name] != value:
            raise ValueError('original cutoff-group placement changed: ' + name)
    pairs = group['pairs']
    if type(pairs) is not list or len(pairs) != count:
        raise ValueError('complete original physical cutoff-pair count required')
    for index, pair in enumerate(pairs):
        _pair_values(pair, named=named)
        for name, value in (('pair_index', index), ('start', start + index * 4),
                ('end', start + (index + 1) * 4)):
            if type(pair[name]) is not int or pair[name] != value:
                raise ValueError('original pair position/index changed: ' + name)


def _validate(fields, *, named):
    _object(fields, _SOURCE_KEYS, 'AI command cutoff source')
    if fields['format'] != (FORMAT if named else TYPED_FORMAT):
        raise ValueError('explicit complete AI cutoff source format required')
    groups = fields['primary_groups']
    if type(groups) is not list or len(groups) != 3:
        raise ValueError('all three physical primary groups are required')
    for index, group in enumerate(groups):
        _validate_group(group, 0x311FC + index * 64, 15, named=named, group_index=index)
    _validate_group(fields['secondary'], 0x312BC, 3, named=named)


def _convert(fields, *, to_named_form):
    _validate(fields, named=not to_named_form)
    result = deepcopy(fields)
    result['format'] = FORMAT if to_named_form else TYPED_FORMAT
    for group in (*result['primary_groups'], result['secondary']):
        for pair in group['pairs']:
            if to_named_form:
                first, second = pair.pop('WORDs')
                pair['first_cutoff_word'], pair['second_cutoff_word'] = first, second
            else:
                pair['WORDs'] = [pair.pop(name) for name in _NAMED_WORDS]
    return result


def to_named(fields: dict) -> dict:
    """Replace every physical WORD pair with its two proven cutoff names.

    This pure operation reads no file and changes no number, order, physical
    allocation or metadata. It does not invoke an encoder or infer probabilities.
    """
    return _convert(fields, to_named_form=True)


def from_named(fields: dict) -> dict:
    """Restore the sole legacy typed authority for the unchanged resource codec.

    The normal codec still owns its complete schema and physical allocations.
    No missing metadata, gap, WORD, fallback source or alternate value is made.
    """
    return _convert(fields, to_named_form=False)


def _review_cutoff_edits(named, edits):
    if type(edits) is not list or not edits:
        raise ValueError('one explicit nonempty list of cutoff edits required')
    reviewed, seen = [], set()
    for edit in edits:
        if type(edit) is not dict or type(edit.get('table')) is not str:
            raise ValueError('cutoff edit must explicitly select primary or secondary table')
        table = edit['table']
        if table == 'primary':
            _object(edit, _EDIT_KEYS | {'group_index'}, 'primary cutoff edit')
            group_index = edit['group_index']
            if type(group_index) is not int or not 0 <= group_index < 3:
                raise ValueError('primary cutoff group_index must be0..2, never bool')
            group = named['primary_groups'][group_index]
        elif table == 'secondary':
            _object(edit, _EDIT_KEYS, 'secondary cutoff edit')
            group_index = None
            group = named['secondary']
        else:
            raise ValueError('cutoff edit table must be primary or secondary')
        pair_index, field = edit['pair_index'], edit['field']
        if type(pair_index) is not int or not 0 <= pair_index < group['pair_count']:
            raise ValueError('explicit physical cutoff pair_index required, never bool')
        if type(field) is not str or field not in _NAMED_WORDS:
            raise ValueError('cutoff edit must select first_cutoff_word or second_cutoff_word')
        target = table, group_index, pair_index, field
        if target in seen:
            raise ValueError('duplicate cutoff WORD edit; no implicit last-write priority')
        seen.add(target)
        before, after = _word(edit['expected_word']), _word(edit['word'])
        if group['pairs'][pair_index][field] != before:
            raise ValueError('cutoff WORD changed from explicit expected value')
        reviewed.append((*target, after))
    return reviewed


def with_cutoff_pairs(named: dict, edits: list[dict]) -> dict:
    """Apply one checked physical-WORD edit batch without mutating either input.

    Primary edits name group_index; secondary edits must not supply one. Every
    edit supplies its pair, named field and exact previous WORD. The complete
    batch is validated before making an independent copy. In particular, the
    first primary WORD's real defense alias remains the same single authority.
    No cutoff ordering, natural selector bounds or original rule is repaired.
    """
    _validate(named, named=True)
    reviewed = _review_cutoff_edits(named, edits)
    result = deepcopy(named)
    for table, group_index, pair_index, field, value in reviewed:
        group = result['primary_groups'][group_index] if table == 'primary' else result['secondary']
        group['pairs'][pair_index][field] = value
    return result


def main(argv=None):
    """Convert or explicitly edit strict fresh own JSON, never invoke a codec."""
    import argparse
    import json
    from pathlib import Path
    from .media_sources import json_bytes, MAX_JSON
    from .native import fresh_output
    from .readable_text import _load

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('direction', choices=('export', 'import', 'edit'),
        help='export/import the sole named authority, or apply one explicit checked edit batch')
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--edits', type=Path, help='explicit edit document; required only for edit')
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True,
        help='new project/build JSON file with an existing parent; no overwrite or media copy')
    args = parser.parse_args(argv)
    project = args.project_root.resolve(strict=True)
    output = fresh_output(args.output)
    if (not project.is_dir() or not output.is_relative_to(project / 'build')
            or output == project / 'build' or not output.parent.is_dir()
            or output.suffix != '.json'):
        raise ValueError('explicit fresh JSON file in this project build with existing parent required')
    if (args.direction == 'edit') != (args.edits is not None):
        raise ValueError('only edit requires one explicit edits document')
    fields = _load(args.source, MAX_JSON)
    if args.direction == 'edit':
        document = _load(args.edits, MAX_JSON)
        _object(document, {'format', 'edits'}, 'cutoff edit document')
        if type(document['format']) is not str or document['format'] != EDIT_FORMAT:
            raise ValueError('explicit complete cutoff edit document format required')
        result = with_cutoff_pairs(fields, document['edits'])
    else:
        result = to_named(fields) if args.direction == 'export' else from_named(fields)
    encoded = json_bytes(result)
    if len(encoded) > MAX_JSON:
        raise ValueError('named AI cutoff source exceeds explicit JSON bound')
    with output.open('xb') as stream:
        stream.write(encoded)
    print(json.dumps(dict(output=str(output), source_format=result['format'], bytes=len(encoded),
        source_conversion_only=args.direction != 'edit', source_edit_only=args.direction == 'edit',
        original_ROM_read=False, resource_encoding_run=False,
        game_run=False, native_run=False, hash_run=False, strict_acceptance=False), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
