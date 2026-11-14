"""Independent transport, formation-rule and physical menu data encoders.

Supplied typed fields plus separately frozen identities/geometry are the only
byte inputs. No ROM, old blocks/topology/extract/serializer or compiled payload
is consulted. Physical editor shapes do not constrain original CPU indices.
"""
from __future__ import annotations

from tools.resource_metadata import compare_fixed_fields

from tools.battle_rule_tables import codec as rules
from tools.menu_tree_fields import codec as menus
from .resource_adapters import block, coalesced_spans, fixed_list, uint
from .resource_adapters_records import _fixed, _same


def _numbers(values, count, width, label):
    return b''.join(uint(value, (1 << (8 * width)) - 1, label).to_bytes(width, 'big')
                    for value in fixed_list(values, count, label))


def _finish(rows, contract, expected):
    rows.sort(key=lambda row: row['start'])
    spans = coalesced_spans(rows)
    if sum(len(row['data']) for row in rows) != expected:
        raise ValueError('complete fixed structure byte cost differs')
    if 'spans' in contract and spans != contract['spans']:
        raise ValueError('persisted independent structure geometry differs')
    return rows


def transport_cargo_build(fields, contract):
    """Three BE32 gold/food pairs; labels are not editable UI text.

    The historical 0..999999 editor policy is retained, not a claim that the
    game's source LONG reads normalize or clamp arbitrary table values.
    """
    top = contract['topology']
    _fixed(fields, top['metadata'], {'entries'}, 'cargo package',
           legacy_digest_paths=(('source', 'sha256'), ('resource', 'canonical_sha256')))
    data = bytearray()
    for row, fixed in zip(fixed_list(fields['entries'], 3, 'cargo choices'), top['entries']):
        _fixed(row, fixed, {'gold', 'food'}, 'cargo record')
        for name in ('gold', 'food'):
            data.extend(uint(row[name], 999999, 'historical cargo editor ' + name).to_bytes(4, 'big'))
    rows = [block(0x13B68, bytes(data), 'transport_cargo_table', 'original_transport_gold_food_BE32')]
    return _finish(rows, contract, 24)


def battle_rule_tables(fields, contract):
    """96x10 WORD vectors, with each 12-BYTE stride tail left unowned."""
    c, rows = rules, []
    compare_fixed_fields(fields, c.metadata(), {'battle_selector_classes', 'battle_vectors',
                                 'equipment_prices', 'denominations'}, 'battle rules')
    rows.append(block(0x24BE4, _numbers(fields['battle_selector_classes'], 14, 2, 'class WORD'),
                      'battle_selector_classes', 'candidate_battle_class_lookup_WORDs'))
    vectors = iter(fixed_list(fields['battle_vectors'], 96, 'physical battle vectors'))
    for side, base in c.SIDES:
        for group in range(3):
            for count in range(16):
                fixed = c.vector_meta(side, base, group, count)
                row = next(vectors)
                _fixed(row, fixed, {'position_index_WORDs'}, 'battle vector')
                rows.append(block(fixed['start'], _numbers(row['position_index_WORDs'], 10, 2, 'position WORD'),
                                  fixed['id'], 'candidate_battle_rank_to_position_WORDs'))
    data = bytearray()
    for category, row in enumerate(fixed_list(fields['equipment_prices'], 3, 'equipment categories')):
        _fixed(row, dict(category=category), {'price_by_quality'}, 'price row')
        data.extend(_numbers(row['price_by_quality'], 3, 4, 'full price LONG'))
    rows.append(block(0xD2CA, bytes(data), 'equipment_prices', 'confirmed_equipment_price_LONGs'))
    for row, (name, start, count) in zip(fixed_list(fields['denominations'], 2, 'denominations'), c.DENOMINATIONS):
        _fixed(row, dict(id=name, start=start), {'step_LONGs'}, 'denomination')
        rows.append(block(start, _numbers(row['step_LONGs'], count, 4, 'full denomination LONG'),
                          name, 'confirmed_' + name + '_denomination_LONGs'))
    return _finish(rows, contract, c.EDITABLE_BYTES)


def menu_tree_fields(fields, contract):
    """187 signed-WORD references and 179 two-header physical records.

    FF headers/choices are meaningful data, not a terminator grammar. Choice
    lengths reflect the editor's physical partition, not a CPU read bound.
    """
    c, top = menus, contract['topology']
    compare_fixed_fields(fields, c.metadata(), {'directory', 'records'}, 'menu package')
    directory = fields['directory']
    _fixed(directory, dict(start=c.DIRECTORY, end=c.RECORD_BASE, record_base=c.RECORD_BASE),
           {'targets'}, 'menu directory')
    geometry = fixed_list(top['records'], 179, 'menu physical partition')
    catalog = {row['id']: row['start'] for row in geometry}
    refs = fixed_list(directory['targets'], 187, 'menu prompt slots')
    if any(type(target) is not str or target not in catalog for target in refs):
        raise ValueError('prompt reference outside complete physical menu catalog')
    data = c.RECORD_BASE.to_bytes(4, 'big') + b''.join(
        (catalog[target] - c.RECORD_BASE).to_bytes(2, 'big', signed=True) for target in refs)
    rows = [block(c.DIRECTORY, data, 'prompt_directory', 'BE32_root_signed_WORD_menu_offsets')]
    for row, fixed in zip(fixed_list(fields['records'], 179, 'menu records'), geometry):
        _fixed(row, fixed, {'parent_prompt_byte', 'title_selector_byte', 'choice_prompt_bytes'}, 'menu record')
        data = bytes([uint(row['parent_prompt_byte'], 255, 'parent prompt BYTE'),
                      uint(row['title_selector_byte'], 255, 'title selector BYTE')]) + bytes(
            uint(value, 255, 'choice prompt BYTE') for value in fixed_list(
                row['choice_prompt_bytes'], fixed['end']-fixed['start']-2, 'physical menu choices'))
        rows.append(block(fixed['start'], data, fixed['id'], 'menu_parent_title_choice_BYTE_fields'))
    return _finish(rows, contract, c.EDITABLE_BYTES)


ENCODERS = dict(transport_cargo_build=transport_cargo_build,
                battle_rule_tables=battle_rule_tables, menu_tree_fields=menu_tree_fields)


def geometry_contract(resource_id, canonical_fields):
    """Offline structural metadata only; no editable numeric payload is held."""
    if resource_id not in ENCODERS: raise ValueError('registered structure resource required')
    contract = dict(adapter=resource_id, adapter_module=__name__, format=canonical_fields['format'],
                    confidence='preserved_original_resource_classification',
                    semantic_meaning='independent_encoding_not_natural_CPU_domain',
                    limits=['physical editor catalogs do not clamp original CPU selectors',
                            'generation does not establish edited gameplay/menu/formation safety',
                            'pure old metadata helpers remain disclosed delivery dependencies'])
    if resource_id == 'transport_cargo_build':
        contract['topology'] = dict(metadata={key: canonical_fields[key] for key in ('format', 'source', 'resource')},
            entries=[{key: row[key] for key in ('choice_index', 'record_type', 'label_zh')}
                     for row in fixed_list(canonical_fields['entries'], 3, 'cargo choices')])
        _same(canonical_fields['format'], 'g5510-transport-cargo-v1', 'cargo format')
        for index, row in enumerate(contract['topology']['entries']):
            _same(row['choice_index'], index, 'cargo index')
            _same(row['record_type'], index+1, 'cargo record type')
        contract['limits'].append('999999 is preserved legacy editor policy, not full-LONG CPU clamp')
    if resource_id == 'battle_rule_tables':
        contract['unowned_row_tails'] = [[base+(group*16+count)*32+20, base+(group*16+count+1)*32]
            for _, base in rules.SIDES for group in range(3) for count in range(16)]
        contract['unowned_neighbor_arrays'] = [[0x1343C, 0x1344C], [0x13464, 0x1347C]]
        contract['limits'].append('1152 stride-tail BYTEs remain unknown; WORD shift/add indices remain wrapping and signed')
    if resource_id == 'menu_tree_fields':
        rows = fixed_list(canonical_fields['records'], 179, 'menu records')
        fixed = [{key: row[key] for key in ('id', 'start', 'end', 'prompt_aliases')} for row in rows]
        if (fixed[0]['start'] != menus.RECORD_BASE or fixed[-1]['end'] != menus.END or
                any(a['end'] != b['start'] for a,b in zip(fixed,fixed[1:])) or
                any(row['end']-row['start'] < 2 for row in fixed)):
            raise ValueError('menu physical partition differs')
        contract['topology'] = dict(records=fixed)
        contract['limits'].append('FF title and empty choices retained; physical END is next referenced glyph source')
    rows = ENCODERS[resource_id](canonical_fields, contract)
    contract.update(spans=coalesced_spans(rows), bytes=sum(len(row['data']) for row in rows), physical_blocks=len(rows))
    return contract
