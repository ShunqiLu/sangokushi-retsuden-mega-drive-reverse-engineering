"""Own typed duel-sprite and palette-copy encoders, independent of ROM input.

Each physical record/bank is emitted once; redirected pointers share that
authority. Fixed capacities are editor policy, not original CPU clamps.
Pure record/color metadata helpers remain explicit delivery dependencies.
"""
from __future__ import annotations

from tools.resource_metadata import compare_fixed_fields

from tools.sprite_records import sprite_records as sprites
from tools.palette_copy_fields import codec as palette_copy
from tools.battle_palette_transfers import codec as battle_palette
from tools.vdp_word_streams import format as fmt
from .resource_adapters import block, coalesced_spans, fixed_list, uint


def _fixed(row, fixed, editable, label):
    compare_fixed_fields(row, fixed, editable, label)


def _finish(rows, contract, expected):
    rows.sort(key=lambda row: row['start'])
    spans = coalesced_spans(rows)
    if sum(len(row['data']) for row in rows) != expected:
        raise ValueError('fixed sprite/palette encoded extent differs')
    if 'spans' in contract and spans != contract['spans']:
        raise ValueError('persisted sprite/palette geometry differs')
    return rows


def sprite_records(fields, contract):
    """71 directories and full six-BYTE SAT descriptors with final terminator."""
    c = sprites
    fixed = dict(format='g5510-duel-sprite-records-v1', canonical_rom_sha256=c.ROM_SHA256,
                 directory_start=c.TABLE_START, directory_end=c.TABLE_END, payload_end=c.DATA_END)
    _fixed(fields, fixed, ('pointers', 'descriptors'), 'duel sprite package')
    topology = fixed_list(contract['descriptors'], 71, 'fixed duel descriptor topology')
    catalog = {row['start'] for row in topology}
    pointers = fixed_list(fields['pointers'], 71, 'duel directory references')
    if any(type(value) is not int or value not in catalog for value in pointers):
        raise ValueError('duel pointer must address an owned complete descriptor')
    rows = [block(c.TABLE_START, b''.join(value.to_bytes(4, 'big') for value in pointers),
                  'duel_sprite_directory', 'duel_sprite_BE32_directory')]
    for row, allocation in zip(fixed_list(fields['descriptors'], 71, 'duel descriptors'), topology):
        _fixed(row, dict(start=allocation['start']), ('records',), 'duel descriptor')
        records = fixed_list(row['records'], allocation['record_count'], 'duel record capacity')
        raw = b''.join(c.encode_record(record) for record in records)
        if any(record['end'] for record in records[:-1]) or not records[-1]['end']:
            raise ValueError('first descriptor terminator must remain at its fixed final record')
        if len(raw) != allocation['end'] - allocation['start']:
            raise ValueError('duel descriptor extent differs')
        rows.append(block(allocation['start'], raw, 'duel_sprite_' + format(allocation['start'], '06x'),
                          'duel_sprite_full_six_BYTE_records'))
    return _finish(rows, contract, 4598)


def _palette(fields, contract, codec, banks, count, *, battle):
    _fixed(fields, codec.metadata(), ('transfers', 'palettes'), 'palette-copy package')
    catalog = {codec.ident(start): (start, end) for start, end in banks}
    directory = bytearray()
    for row, start in zip(fixed_list(fields['transfers'], count, 'palette transfer records'),
                          range(codec.DIRECTORY_START, codec.DIRECTORY_END, 8)):
        _fixed(row, dict(id=f'rom_{start:06X}_transfer'),
               ('source', 'destination_WORD', 'LONG_count_minus_one'), 'palette transfer')
        source = row['source']
        if type(source) is not str or source not in catalog:
            raise ValueError('palette transfer source outside existing physical editor catalog')
        begin, end = catalog[source]
        destination = uint(row['destination_WORD'], 65535, 'MOVEA.W full destination')
        counter = uint(row['LONG_count_minus_one'], 65535, 'DBRA full counter WORD')
        cost = 4 * (counter + 1)
        if cost > end - begin:
            raise ValueError('edited palette copy exceeds fixed source allocation')
        if battle and (destination not in (0xFB00, 0xFB20) or destination + cost > 0xFB80):
            raise ValueError('edited battle palette copy exceeds fixed staging capacity')
        directory.extend(begin.to_bytes(4, 'big') + destination.to_bytes(2, 'big') + counter.to_bytes(2, 'big'))
    rows = [block(codec.DIRECTORY_START, bytes(directory), 'palette_transfers_' + format(codec.DIRECTORY_START, '06x'),
                  'candidate_BE32_MOVEAWORD_DBRALONG_transfers')]
    for row, (start, end) in zip(fixed_list(fields['palettes'], len(banks), 'palette banks'), banks):
        _fixed(row, dict(id=codec.ident(start), start=start, end=end), ('colours',), 'palette bank')
        data = b''.join(codec.colour_word(colour).to_bytes(2, 'big')
                        for colour in fixed_list(row['colours'], (end - start) // 2, 'full CRAM WORDs'))
        rows.append(block(start, data, row['id'], 'candidate_palette_staging_CRAM_reserved_bits'))
    return _finish(rows, contract, codec.EDITABLE_BYTES)


def palette_copy_fields(fields, contract):
    return _palette(fields, contract, palette_copy, palette_copy.BANKS, 7, battle=False)


def battle_palette_transfers(fields, contract):
    """17 copy records; the eighteenth code-as-data alias is not duplicated."""
    return _palette(fields, contract, battle_palette, battle_palette.PALETTES, 17, battle=True)


ENCODERS = dict(sprite_records=sprite_records, palette_copy_fields=palette_copy_fields,
                battle_palette_transfers=battle_palette_transfers)


def geometry_contract(resource_id, canonical_fields):
    """Persist editor topology once; later edits cannot silently resize slots."""
    if resource_id not in ENCODERS:
        raise ValueError('explicit own sprite/palette resource ID required')
    contract = dict(adapter=resource_id, adapter_module=__name__, format=canonical_fields['format'],
                    confidence='preserved_original_source_classification',
                    semantic_meaning='encoding_not_CPU_SAT_or_natural_rendering_acceptance',
                    limits=['editor catalogs and capacities do not clamp the original CPU',
                            'pure record/color helpers remain disclosed delivery dependencies'])
    if resource_id == 'sprite_records':
        contract['descriptors'] = []
        for row in fixed_list(canonical_fields['descriptors'], 71, 'canonical duel descriptors'):
            records = row['records']
            if type(records) is not list or not records:
                raise ValueError('nonempty original duel descriptor required')
            start = uint(row['start'], sprites.ROM_SIZE - 1, 'duel descriptor start')
            contract['descriptors'].append(dict(start=start, end=start + len(records) * 6, record_count=len(records)))
        topology = contract['descriptors']
        if (topology[0]['start'] != sprites.TABLE_END or topology[-1]['end'] != sprites.DATA_END or
                any(a['end'] != b['start'] for a, b in zip(topology, topology[1:]))):
            raise ValueError('duel physical descriptor partition differs')
    if resource_id == 'battle_palette_transfers':
        contract['excluded_alias'] = dict(start=0x3AC34, end=0x3AC3C, source=0x3B0BC,
                                         role='existing_executable_code_as_data', physical_emit=False,
                                         natural_selector17='unknown')
        contract['limits'].append('eighteenth descriptor remains another owner; no new code/palette bank')
    rows = ENCODERS[resource_id](canonical_fields, contract)
    contract.update(spans=coalesced_spans(rows), bytes=sum(len(row['data']) for row in rows), physical_blocks=len(rows))
    return contract
