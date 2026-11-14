"""Human-editable confirmed scenario fields over the sole typed scenario codec.

This module renames source fields, not gameplay values or loader RAM. Unknown
fields/bits, source sentinels, three equipment bytes, fixed table aliases and
all33 original source columns stay explicit. It never reads a ROM or encodes
machine bytes; the registered scenario encoder remains the layout authority.
"""
from __future__ import annotations

import copy


FORMAT = 'g5510-owned-named-scenario-source-v1'
TYPED_FORMAT = 'g5510_scenario_fixed_fields'
SCENARIO_IDS = ('scenario_0', 'scenario_1', 'scenario_2')
SPLIT_FIELDS = frozenset(('ram_e1e0', 'ram_e320', 'ram_e5a0'))

# Source widths/counts, not derived RAM widths or guessed gameplay ranges.
CITY_FIELDS = (
    ('ram_f428', 1), ('ram_f460', 2), ('ram_e000', 4), ('ram_e0a0', 4),
    ('ram_e140', 4), ('ram_e1e0', 4), ('ram_e280', 4), ('ram_e320', 4),
    ('ram_e3c0', 4), ('ram_e460', 4), ('ram_e500', 4), ('ram_e5a0', 4),
)
FORCE_FIELDS = (('ram_e640', 2), ('ram_e710', 2))
OFFICER_FIELDS = (
    ('ram_b000', 2), ('ram_b200', 2), ('ram_b400', 2), ('ram_b600', 2),
    ('ram_b800', 2), ('ram_ba00', 2), ('ram_bc00', 2), ('ram_be00', 2),
    ('ram_c000', 2), ('ram_c200', 1), ('ram_c300', 1), ('ram_c400', 1),
    ('ram_c500', 1), ('ram_c600', 1), ('ram_c700', 1), ('ram_c800', 4),
    ('ram_cc00', 1), ('ram_ea88', 3), ('ram_f000', 2),
)
GROUPS = (('cities', 40, 1, CITY_FIELDS), ('forces', 16, 0, FORCE_FIELDS),
          ('officers', 256, 0, OFFICER_FIELDS))
TABLE_IDS = tuple(name for _, _, _, fields in GROUPS for name, _ in fields)

# The original eleven labels are confirmed in scenario_build.MEANINGS. The
# later B161/B162 roles have separate original-consumer evidence. Their
# neutral internal names are not confirmed game/UI attribute labels;
# combat_rating_word is a candidate name for the confirmed operation role.
# Representative-officer indices do not assert a formal office/title.
# Unproved columns stay address-keyed; named flag bytes retain all unknown bits.
NAMED_FIELDS = {
    'ram_f428': 'force_index_byte',
    'ram_f460': 'representative_officer_word',
    'ram_e000': 'gold',
    'ram_e0a0': 'rice',
    'ram_e140': 'income_base_long',
    'ram_e1e0': 'development',
    'ram_e280': 'income_split_long',
    'ram_e320': 'welfare',
    'ram_e3c0': 'income_rate_long',
    'ram_e460': 'assigned_officer_tally_long',
    'ram_e500': 'troop_total_long',
    'ram_e5a0': 'defense',
    'ram_b000': 'readiness_capacity_word',
    'ram_b200': 'readiness_current_word',
    'ram_b400': 'combat_rating_word',
    'ram_b600': 'intelligence_word',
    'ram_b800': 'troop_capacity_base_word',
    'ram_be00': 'intelligence_growth_score_word',
    'ram_c000': 'combat_growth_score_word',
    'ram_c200': 'virtue_byte',
    'ram_c300': 'education_rating_byte',
    'ram_c400': 'movement_factor_byte',
    'ram_c500': 'training_percent_byte',
    'ram_c600': 'growth_threshold_tier_byte',
    'ram_c700': 'class_status_flags_byte',
    'ram_c800': 'troop_count_long',
    'ram_cc00': 'assigned_city_byte',
    'ram_e640': 'representative_officer_word',
    'ram_e710': 'relationship_bits_word',
}

# confirmed source geometry: TABLE_SPECS descriptor +0x34/+0x38 each supplies
# 256 original WORDs. confirmed operational role, formal UI label unknown:
# recovered_code.s E83A/E83E select B200/B000, E878/E87C/E880 derive 15% of
# B000, E884/E888 add to B200 as a wrapping WORD, E88A/E892 cap against B000,
# and E896 writes B200. The complete current consumer is
# high_level_main_flows.business_scene_support.recover_unacted_officer_b200_fields.
# direct_descendants.s 30F58..30FA0 independently repeats the same recovery;
# nested_dispatch_descendants.s 351E8..35200 tests the B000 > B200 shortfall.
# B400's original WORD role is independently read by BAD6/BADC/BAE0 as the
# C500-weighted factor /100, FD2C..FD52 as the 5*B400 training-growth input,
# and 1B9A0..1B9CC as a battle-loss-ratio input. Those consumers do not prove
# its formal UI name. The normal 66370..6639C growth writes a WORD, but the
# original 34ECC/34EE4/34EE6 equipment path also writes BYTE 4 at B400+3*id;
# do not assume all accesses are aligned WORDs or repair that retained path.
# confirmed B162 operational roles, formal UI names unknown:
# 9394/9398/93A0/93A2 sum C000/BE00 with original WORD wrapping; 93B6 writes
# the threshold tier C600. 662E4..66344 consumes that same sum/tier; 66370 and
# 663A2 weight the B400/B600 gains by C000/BE00 respectively. FDD2..FDE2 adds
# C000 with its original post-add 999 cap; E68C..E6A2 similarly rewards BE00.
# E596/E5AA/E5BC/E63C..E65C read and grow C300 through the actual education
# rule, with signed BYTE extension and a later 100 comparison. FD58..FD76 and
# BACC..BAE0 establish C500's percentage role; source values are not clamped.
# City/force indices: 325E4 scans F428; 320D4..32138 reads/writes F460 and
# compares E640; A466..A47E resolves E640's officer-name record. 666C4..66712
# retains actual FF/FFFF removal sentinels, not guessed office names.
# E57C..E58A and 16C76..16C94 establish the rate/base income operands; 16C2C..
# 16C52/16D10..16D36 use E280 versus 100-E280 for rice/gold. Their source
# columns stay LONGs even where only a low WORD is consumed. A72A..A756
# rebuilds E460 from CC00; 57AC..57DA rebuilds E500 from C800 plus E774.
# Those recomputed columns are editable initial slots, not permanent totals.
# C400 is read by 17AAA..17AB8 for a 9-times candidate radius, 1DD0A..1DD14
# as the movement DIVU divisor, and 33C12..33C32 for a two-officer march mean.
# Preserve its complete BYTE, ADD.B wrap before averaging and zero divisors.
# C700's low three bits are read at 31C2C/31C30, while 31C5A tests bit 4;
# 321FE..32208 retains bit 4 while writing computed status. Other bits remain
# unknown. Do not normalize the distinct 16D92 mask 5 into mask 7, restrict
# the source BYTE to 0..31 or repair 321DE's original moving-roster read.
# Existing v1 sources keep the later named values under unresolved_fields. Accept
# exactly one representation per newly named field; never both or a default.
_LEGACY_UNRESOLVED_NAMED_FIELDS = frozenset((
    'ram_b000', 'ram_b200', 'ram_b400',
    'ram_be00', 'ram_c000', 'ram_c300', 'ram_c400', 'ram_c500', 'ram_c600',
    'ram_c700',
    'ram_f428', 'ram_f460', 'ram_e140', 'ram_e280', 'ram_e3c0',
    'ram_e460', 'ram_e500', 'ram_e640',
))


def _keys(value, expected):
    if type(value) is not dict or set(value) != set(expected):
        raise ValueError('exact scenario source fields required')


def _uint(value, bits):
    if type(value) is not int or not 0 <= value < (1 << bits):
        raise ValueError('strict unsigned scenario source value outside its original width')
    return value


def _fixed(value, count):
    if type(value) is not list or len(value) != count:
        raise ValueError('fixed original scenario source count changed')
    return value


def _field_value(field, width, value):
    if field in SPLIT_FIELDS:
        _keys(value, ('unknown_high_word', 'value_low_word'))
        return {name:_uint(value[name], 16) for name in ('unknown_high_word', 'value_low_word')}
    if field == 'ram_ea88':
        names = tuple('source_byte' + str(index) for index in range(3))
        _keys(value, names)
        return {name:_uint(value[name], 8) for name in names}
    return _uint(value, width * 8)


def _directory(values):
    result = []
    for value in _fixed(values, 3):
        if type(value) is not str or value not in SCENARIO_IDS:
            raise ValueError('scenario directory must retain a named existing source target')
        result.append(value)
    return result


def _descriptors(values):
    _keys(values, TABLE_IDS)
    result = {}
    for field in TABLE_IDS:
        target = values[field]
        if type(target) is not str or target not in {ident + '.' + field for ident in SCENARIO_IDS}:
            raise ValueError('descriptor alias must retain the same original source column kind')
        result[field] = target
    return result


def _metadata(values):
    _keys(values, ('schema_version', 'source_format', 'canonical_rom_sha256'))
    if type(values['schema_version']) is not int or values['schema_version'] != 1:
        raise ValueError('scenario source schema version changed')
    if (values['source_format'] != TYPED_FORMAT
            or type(values['canonical_rom_sha256']) is not str
            or not values['canonical_rom_sha256']):
        raise ValueError('original typed scenario provenance fields required')
    # The historical identity string is retained metadata, not a ROM lookup or
    # newly performed digest comparison. The normal typed encoder checks its
    # own complete fixed source contract after this field conversion.
    return copy.deepcopy(values)


def _to_named_record(row, fields, identity):
    _keys(row, {'id'} | {name for name, _ in fields})
    if type(row['id']) is not int or row['id'] != identity:
        raise ValueError('original scenario record identity changed')
    result = dict(id=identity)
    unresolved = {}
    for field, width in fields:
        value = _field_value(field, width, row[field])
        if field in NAMED_FIELDS:
            result[NAMED_FIELDS[field]] = value
        else:
            unresolved[field] = value
    result['unresolved_fields'] = unresolved
    return result


def _from_named_record(row, fields, identity):
    if type(row) is not dict or type(row.get('unresolved_fields')) is not dict:
        raise ValueError('exact scenario record and unresolved field mapping required')
    legacy = {field for field, _ in fields
        if field in _LEGACY_UNRESOLVED_NAMED_FIELDS and field in row['unresolved_fields']}
    names = {NAMED_FIELDS[field] for field, _ in fields
        if field in NAMED_FIELDS and field not in legacy}
    unresolved = {field for field, _ in fields if field not in NAMED_FIELDS} | legacy
    _keys(row, {'id', 'unresolved_fields'} | names)
    _keys(row['unresolved_fields'], unresolved)
    if type(row['id']) is not int or row['id'] != identity:
        raise ValueError('original scenario record identity changed')
    result = dict(id=identity)
    for field, width in fields:
        value = (row[NAMED_FIELDS[field]] if field in NAMED_FIELDS and field not in legacy
            else row['unresolved_fields'][field])
        result[field] = _field_value(field, width, value)
    return result


def _scenarios(values, convert_record):
    result = []
    for ident, scenario in zip(SCENARIO_IDS, _fixed(values, 3)):
        _keys(scenario, ('id', 'descriptor_targets', 'cities', 'forces', 'officers'))
        if scenario['id'] != ident or type(scenario['id']) is not str:
            raise ValueError('fixed original scenario ordering changed')
        selected = dict(id=ident, descriptor_targets=_descriptors(scenario['descriptor_targets']))
        for group, count, first, fields in GROUPS:
            selected[group] = [convert_record(row, fields, index + first)
                for index, row in enumerate(_fixed(scenario[group], count))]
        result.append(selected)
    return result


def to_named(fields):
    """Convert complete typed sources to one named authority without encoding.

    Integer values are never clamped, scaled or copied into a hidden raw-value
    fallback. Every unknown field stays once under its original address key.
    """
    _keys(fields, ('schema_version', 'format', 'canonical_rom_sha256',
        'directory_targets', 'scenarios'))
    metadata = _metadata(dict(schema_version=fields['schema_version'],
        source_format=fields['format'], canonical_rom_sha256=fields['canonical_rom_sha256']))
    return dict(format=FORMAT, metadata=metadata,
        directory_targets=_directory(fields['directory_targets']),
        scenarios=_scenarios(fields['scenarios'], _to_named_record))


def from_named(document):
    """Restore typed input; recovered names and their old v1 keys are exclusive.

    Every later-named value must occur exactly once. Its legacy unresolved key
    and corresponding new name may not coexist or both be absent. Other unknown
    fields retain their complete original address-key contract unchanged.
    """
    _keys(document, ('format', 'metadata', 'directory_targets', 'scenarios'))
    if document['format'] != FORMAT:
        raise ValueError('named scenario source format changed')
    metadata = _metadata(document['metadata'])
    return dict(schema_version=metadata['schema_version'], format=metadata['source_format'],
        canonical_rom_sha256=metadata['canonical_rom_sha256'],
        directory_targets=_directory(document['directory_targets']),
        scenarios=_scenarios(document['scenarios'], _from_named_record))


def _edit_group(name):
    if type(name) is not str:
        raise ValueError('named scenario edit group must be a string')
    for group, count, first, fields in GROUPS:
        if name == group:
            return count, first, fields
    raise ValueError('named scenario edit group must be cities, forces or officers')


def _edit_field(fields, name):
    if type(name) is not str:
        raise ValueError('named scenario edit field must be a confirmed field name')
    for source_field, width in fields:
        if NAMED_FIELDS.get(source_field) == name:
            return source_field in SPLIT_FIELDS, 16 if source_field in SPLIT_FIELDS else width * 8
    raise ValueError('only confirmed named fields in the selected scenario group are editable')


def _checked_scenario_edit(document, edit):
    _keys(edit, ('scenario_id', 'group', 'record_id', 'field', 'expected_value', 'value'))
    ident = edit['scenario_id']
    if type(ident) is not str or ident not in SCENARIO_IDS:
        raise ValueError('named scenario edit requires an existing explicit scenario_id')
    count, first, fields = _edit_group(edit['group'])
    record_id = edit['record_id']
    if type(record_id) is not int or not first <= record_id < first + count:
        raise ValueError('named scenario edit record_id outside the original group identities')
    split, bits = _edit_field(fields, edit['field'])
    expected = _uint(edit['expected_value'], bits)
    value = _uint(edit['value'], bits)
    scenario_index, record_index = SCENARIO_IDS.index(ident), record_id - first
    stored = document['scenarios'][scenario_index][edit['group']][record_index][edit['field']]
    observed = stored['value_low_word'] if split else stored
    if observed != expected:
        raise ValueError('named scenario edit expected_value does not match the physical source record')
    return scenario_index, edit['group'], record_index, edit['field'], split, value


def with_scenario_fields(named_document, edits):
    """Return a copy with one fully validated batch of confirmed source edits.

    Each edit names a physical scenario/group/record/field and its expected old
    integer. Split city values select only value_low_word, never the unknown
    high WORD. Descriptor/directory aliases are retained, not followed. No
    game state, codec, file, inferred range or original bug is changed here.
    Pure conversion first canonicalizes the explicitly listed later-named v1
    keys. That may reorder the representation, never the source values;
    all unknown fields, sentinels and unknown high WORDs remain unchanged.
    """
    if type(edits) is not list or not edits:
        raise ValueError('a nonempty explicit list of named scenario edits is required')
    normalized = to_named(from_named(named_document))
    selected, targets = [], set()
    for edit in edits:
        selection = _checked_scenario_edit(normalized, edit)
        target = selection[:4]
        if target in targets:
            raise ValueError('duplicate physical scenario/group/record/field edit target')
        targets.add(target)
        selected.append(selection)
    result = copy.deepcopy(normalized)
    for scenario_index, group, record_index, field, split, value in selected:
        records = list(result['scenarios'][scenario_index][group])
        record = dict(records[record_index])
        if split:
            record[field] = dict(record[field], value_low_word=value)
        else:
            record[field] = value
        records[record_index] = record
        result['scenarios'][scenario_index][group] = records
    return result


def _checked_equipment_source_edit(document, edit):
    _keys(edit, ('scenario_id', 'officer_id', 'source_byte_index', 'expected_value', 'value'))
    ident = edit['scenario_id']
    if type(ident) is not str or ident not in SCENARIO_IDS:
        raise ValueError('equipment source edit requires an existing explicit scenario_id')
    officer_id = _uint(edit['officer_id'], 8)
    byte_index = edit['source_byte_index']
    if type(byte_index) is not int or not 0 <= byte_index < 3:
        raise ValueError('equipment source_byte_index must be the original integer 0, 1 or 2')
    expected = _uint(edit['expected_value'], 8)
    value = _uint(edit['value'], 8)
    scenario_index = SCENARIO_IDS.index(ident)
    equipment = document['scenarios'][scenario_index]['officers'][officer_id]['unresolved_fields']['ram_ea88']
    if equipment['source_byte' + str(byte_index)] != expected:
        raise ValueError('equipment expected_value does not match the physical source BYTE')
    return scenario_index, officer_id, byte_index, value


def with_equipment_source_bytes(named_document, edits):
    """Return a copy with one fully checked batch of initial EA88 source edits.

    Each edit selects a physical scenario/officer/source_byte_index, not a
    named runtime equipment category or a saved-game value. The original
    407A..4094 loader maps source indices 0/1/2 to runtime indices 1/0/2;
    this source editor never swaps bytes or follows descriptor aliases.
    Pure from_named/to_named normalization may reorder representation and
    canonicalize old v1 keys, but preserves all source values before editing.
    """
    if type(edits) is not list or not edits:
        raise ValueError('a nonempty explicit list of equipment source BYTE edits is required')
    normalized = to_named(from_named(named_document))
    selected, targets = [], set()
    for edit in edits:
        selection = _checked_equipment_source_edit(normalized, edit)
        target = selection[:3]
        if target in targets:
            raise ValueError('duplicate physical scenario/officer/source BYTE edit target')
        targets.add(target)
        selected.append(selection)
    result = copy.deepcopy(normalized)
    for scenario_index, officer_id, byte_index, value in selected:
        equipment = result['scenarios'][scenario_index]['officers'][officer_id]['unresolved_fields']['ram_ea88']
        equipment['source_byte' + str(byte_index)] = value
    return result


def main(argv=None):
    """Explicit fresh-file source conversion/editing, never game execution."""
    import argparse
    import json
    from pathlib import Path
    from .media_sources import json_bytes, MAX_JSON
    from .native import fresh_output
    from .readable_text import _load

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('export', 'import', 'edit', 'edit-equipment'))
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--edits', type=Path)
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    if (args.mode in ('edit', 'edit-equipment')) != (args.edits is not None):
        parser.error('--edits is required only for edit and edit-equipment modes')
    project = args.project_root.resolve(strict=True)
    output = fresh_output(args.output)
    if (not project.is_dir() or not output.is_relative_to(project / 'build')
            or output == project / 'build' or not output.parent.is_dir()
            or output.suffix != '.json'):
        raise ValueError('explicit fresh JSON file in this project build with existing parent required')
    source = _load(args.source)
    if args.mode == 'edit':
        result = with_scenario_fields(source, _load(args.edits))
    elif args.mode == 'edit-equipment':
        result = with_equipment_source_bytes(source, _load(args.edits))
    else:
        result = to_named(source) if args.mode == 'export' else from_named(source)
    raw = json_bytes(result)
    if len(raw) > MAX_JSON:
        raise ValueError('named scenario source exceeds explicit JSON bound')
    with output.open('xb') as destination:
        destination.write(raw)
    report = dict(output=str(output), source_format=result['format'], bytes=len(raw),
        source_conversion_only=True, original_ROM_read=False, resource_encoding_run=False,
        game_run=False, native_run=False, hash_run=False, strict_acceptance=False)
    if args.mode in ('edit', 'edit-equipment'):
        report.update(source_conversion_only=False, source_edit_only=True)
    if args.mode == 'edit-equipment':
        report['equipment_source_byte_edit_only'] = True
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
