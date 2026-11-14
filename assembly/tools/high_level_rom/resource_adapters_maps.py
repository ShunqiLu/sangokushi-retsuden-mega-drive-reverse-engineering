"""Independent typed encoders for the large WORD-stream/map authorities.

Only supplied editable fields and persisted editor geometry are generation
inputs. Legacy pure serializers/grammar projections are explicit dependencies;
no ROM, legacy blocks/extract/rebuild/verify API or filesystem read is used.
Editor capacities and count policies are not natural CPU/VDP bounds. Original
anomalies, unread tails, candidate purposes and probable allocations stay so.
"""
from __future__ import annotations

from tools.resource_metadata import compare_fixed_fields

from tools.terrain_maps import terrain_maps as terrain
from tools.battle_graphics import battle_graphics as battle
from tools.dictionary_streams import codec as dictionary
from tools.vdp_word_streams import format as vdp
from tools.vdp_empty_marker_fields import codec as empty_marker
from tools.graphics_build import rle_fields as rle
from .resource_adapters import block, coalesced_spans, fixed_list, uint


def _fixed(row, fixed, editable, label):
    compare_fixed_fields(row, fixed, editable, label)


def _package(fields, fixed, editable):
    _fixed(fields, fixed, editable, 'typed WORD/map package')


def _add(rows, start, end, raw, ident, role):
    if type(raw) is not bytes or len(raw) != end - start:
        raise ValueError('fixed WORD/map encoded extent differs')
    rows.append(block(start, raw, ident, role))


def _finish(rows, contract, expected):
    rows.sort(key=lambda row: row['start'])
    spans = coalesced_spans(rows)
    if sum(len(row['data']) for row in rows) != expected:
        raise ValueError('fixed WORD/map physical byte count differs')
    if 'spans' in contract and spans != contract['spans']:
        raise ValueError('persisted WORD/map geometry differs')
    return rows


def terrain_maps(fields, contract):
    """40x28x40 full BE16 maps plus the entire biased 512-BYTE allocation.

    All u16/u8 values remain editable, including unreferenced/probable entries.
    Lookups outside that allocation are not supplied, clipped or normalized.
    """
    c = terrain
    _package(fields, dict(schema_version=1, format=c.FORMAT), ('maps', 'type_values'))
    rows = []
    types = fixed_list(fields['type_values'], c.TYPE_COUNT, 'terrain type allocation')
    _add(rows, c.TYPE_START, c.TYPE_END,
         bytes(uint(value, 255, 'terrain type BYTE') for value in types),
         'terrain_types', 'terrain_type_bytes')
    for number, record in enumerate(fixed_list(fields['maps'], c.MAP_COUNT, 'map catalog'), 1):
        _fixed(record, dict(id=c.map_id(number), map_id=number), ('rows',), 'map')
        raw = bytearray()
        for row in fixed_list(record['rows'], c.ROWS, 'map rows'):
            for word in fixed_list(row, c.COLUMNS, 'map columns'):
                raw.extend(uint(word, 65535, 'full map WORD').to_bytes(2, 'big'))
        start = c.MAP_BIAS + number * c.MAP_SIZE
        _add(rows, start, start + c.MAP_SIZE, bytes(raw), record['id'], 'terrain_map_words')
    return _finish(rows, contract, c.EDITABLE_BYTES)


def vdp_word_streams(fields, contract):
    """19 fixed big-WORD RLE slots; empty marker/terrain are not re-emitted.

    validate_fields is a pure field serializer/read-boundary projection. Its
    canonical empty-stream dependency constraint is retained, not a ROM read.
    Directory targets are pinned by this old schema and emitted separately.
    """
    rows = []
    for row in vdp.validate_fields(fields):
        if row['physical_emit']:
            _add(rows, row['start'], row['end'], row['encoded'], vdp.ident(row['start']),
                 'candidate_vdp_word_packets')
    return _finish(rows, contract, 104621)


def vdp_directory_fields(fields, contract):
    """80 pinned BE32 metadata pointers, same typed author as the streams."""
    _package(fields, vdp.metadata(), ('blocks',))
    raw = b''.join(uint(row['target'], vdp.ROM_SIZE - 1, 'directory LONG').to_bytes(4, 'big')
                   for row in fields['directory']['entries'])
    rows = []
    _add(rows, vdp.DIRECTORY_START, vdp.DIRECTORY_END, raw,
         'rom_0387BA_vdp_directory', 'old_author_VDP_BE32_directory')
    return _finish(rows, contract, 320)


def vdp_empty_marker_fields(fields, contract):
    """Only the editable EE5EF marker; neighboring terrain remains live.

    Encoding is independent of the two neighboring values. Changing the marker
    can change grammar/termination; no canonical three-BYTE stop is imposed by
    this one-BYTE serializer, and edited gameplay safety remains unknown.
    """
    _package(fields, empty_marker.metadata(), ('marker',))
    marker = fields['marker']
    _fixed(marker, empty_marker.marker_fixed(), ('BYTE',), 'empty-stream marker')
    rows = [block(empty_marker.START, bytes((uint(marker['BYTE'], 255, 'marker BYTE'),)),
                  empty_marker.BLOCK_ID, 'confirmed_WORD_RLE_marker_BYTE_source')]
    return _finish(rows, contract, 1)


def battle_graphics(fields, contract):
    """Five little-WORD tile streams and eight big-WORD maps plus catalogs.

    Physical marker/zero map tails are preserved despite the original map
    consumer exiting before them. The editor still requires a complete run at
    1024 outputs; it does not alter the original raw consumer's partial-repeat
    behavior or declare a natural selector domain.
    """
    c = battle
    _package(fields, dict(schema_version=1, format=c.FORMAT), ('directories', 'streams'))
    rows = []
    for row, (ident, start) in zip(fixed_list(fields['directories'], 2, 'map directories'), c.DIRECTORIES):
        _fixed(row, dict(id=ident), ('targets',), 'map directory')
        raw = bytearray()
        for target in fixed_list(row['targets'], 4, 'map targets'):
            if type(target) is not str or target not in c.BY_ID or c.BY_ID[target].order != 'big':
                raise ValueError('map target outside the existing physical editor catalog')
            raw.extend(c.BY_ID[target].start.to_bytes(4, 'big'))
        _add(rows, start, start + 16, bytes(raw), ident, 'map_pointer_directory')
    for row, stream in zip(fixed_list(fields['streams'], 13, 'battle streams'), c.STREAMS):
        _fixed(row, c.metadata(stream), ('fields',), 'battle stream')
        vdp.strict_commands(row['fields'])
        raw, decoded = rle.pack_word(row['fields'], stream.order, stream.words)
        if len(raw) != stream.end - stream.start or rle.parse_word(raw, stream.order, stream.words) != row['fields']:
            raise ValueError('fixed battle stream representation/extent differs')
        projection = c.consume(raw, stream.order, map_entry=stream.order == 'big')
        if (projection['output'] != decoded or
                projection['stop'] != ('row_limit' if stream.order == 'big' else 'marker_zero') or
                projection['consumed'] != len(raw) - (2 if stream.order == 'big' else 0) or
                projection['remaining_repeat_words'] != 0):
            raise ValueError('edited battle stream violates original fixed editor boundary policy')
        _add(rows, stream.start, stream.end, raw, stream.id,
             'word_rle_tilemap' if stream.order == 'big' else 'word_rle_tiles')
    return _finish(rows, contract, c.EDITABLE_BYTES)


def _token_plan(fields):
    """Persist only token classes, never original WORD values/opaque bytes."""
    result = []
    for row, (base, source, end, count) in zip(fixed_list(fields['datasets'], 3, 'datasets'), dictionary.SETS):
        _fixed(row, dictionary.set_metadata(base, source, end, count),
               ('dictionary_entries', 'source_tokens'), 'dictionary dataset')
        pairs = fixed_list(row['dictionary_entries'], (source - base) // 4, 'dictionary pairs')
        pair_ops = []
        for pair in pairs:
            pair = fixed_list(pair, 2, 'dictionary pair')
            for token in pair:
                dictionary.token_word(token)
            pair_ops.append([token['op'] for token in pair])
        tokens = fixed_list(row['source_tokens'], (end - source) // 2, 'source tokens')
        for token in tokens:
            dictionary.token_word(token)
        result.append(dict(id=row['id'], dictionary_ops=pair_ops,
                           source_ops=[token['op'] for token in tokens]))
    return result


def _tokens(tokens, operations, label):
    values = []
    for token, op in zip(fixed_list(tokens, len(operations), label), operations):
        value = dictionary.token_word(token)
        if token['op'] != op:
            raise ValueError(label + ': fixed original token class changed')
        values.append(value.to_bytes(2, 'big'))
    return b''.join(values)


def dictionary_streams(fields, contract):
    """FE/FF data projection, fixed token classes, counts/records/4bpp tiles.

    Source suffixes stay authoritative even when a count chooses a shorter
    complete prefix. Original FE-to-FE special ordering is the pure evaluator's
    existing behavior; no recursive normalization or natural CPU claim is made.
    """
    c = dictionary
    _package(fields, c.metadata(), ('datasets', 'count_fields', 'records', 'raw_transfer', 'raw_tiles'))
    plans = fixed_list(contract['datasets'], 3, 'fixed dictionary token topology')
    rows, counts, count_raw = [], {}, bytearray()
    for row, address in zip(fixed_list(fields['count_fields'], 4, 'count fields'),
                            range(c.COUNT_START, c.COUNT_END, 2)):
        _fixed(row, dict(address=address), ('value',), 'count WORD')
        counts[address] = uint(row['value'], 65535, 'count WORD')
        count_raw.extend(counts[address].to_bytes(2, 'big'))
    _add(rows, c.COUNT_START, c.COUNT_END, bytes(count_raw), 'dictionary_count_fields', 'count_BE16_WORDs')
    for row, plan, (base, source, end, count_at) in zip(fixed_list(fields['datasets'], 3, 'datasets'), plans, c.SETS):
        _fixed(row, c.set_metadata(base, source, end, count_at),
               ('dictionary_entries', 'source_tokens'), 'dictionary dataset')
        vdp.same(row['id'], plan['id'], 'dataset geometry identity')
        pairs = fixed_list(row['dictionary_entries'], (source - base) // 4, 'dictionary pairs')
        table = b''.join(_tokens(pair, ops, 'dictionary pair') for pair, ops in
                         zip(pairs, fixed_list(plan['dictionary_ops'], len(pairs), 'fixed dictionary classes')))
        commands = _tokens(row['source_tokens'], plan['source_ops'], 'source tokens')
        count = counts[count_at]
        if count >= len(commands) // 2:
            raise ValueError('count exceeds fixed source allocation')
        projection = c.evaluate(commands, table, count)
        if (projection['count_final_word'] != 65535 or projection['pending_final_byte'] != 0 or
                projection['source_bytes_read'] != 2 * (count + 1)):
            raise ValueError('count does not end a complete packet/dictionary prefix')
        _add(rows, base, source, table, row['id'] + '_dictionary', 'dictionary_pair_WORDs')
        _add(rows, source, end, commands, row['id'] + '_commands', 'FE_FF_command_WORDs')
    record_set = fields['records']
    _fixed(record_set, dict(start=c.RECORD_START, end=c.RECORD_END), ('records',), 'record set')
    record_raw = bytearray()
    for index, row in enumerate(fixed_list(record_set['records'], 18, 'records')):
        _fixed(row, dict(id=f'rom_{c.RECORD_START + index * 36:06X}_record'), ('words',), 'record')
        for word in fixed_list(row['words'], 18, 'record WORDs'):
            record_raw.extend(uint(word, 65535, 'record BE16').to_bytes(2, 'big'))
    _add(rows, c.RECORD_START, c.RECORD_END, bytes(record_raw), 'dictionary_records', 'record_BE16_WORDs')
    transfer = fields['raw_transfer']
    _fixed(transfer, dict(start=c.RAW_START, end=c.RAW_END), ('longs',), 'raw transfer')
    if counts[0xD34C6] >= 40:
        raise ValueError('raw LONG count exceeds fixed slot')
    raw = b''.join(uint(value, 0xFFFFFFFF, 'transfer LONG').to_bytes(4, 'big')
                   for value in fixed_list(transfer['longs'], 40, 'raw LONGs'))
    _add(rows, c.RAW_START, c.RAW_END, raw, 'dictionary_raw_transfer', 'raw_transfer_BE32_LONGs')
    tile_set = fields['raw_tiles']
    _fixed(tile_set, dict(start=c.TILE_START, end=c.TILE_END), ('tiles',), 'raw tile set')
    raw = bytearray()
    for index, tile in enumerate(fixed_list(tile_set['tiles'], 20, 'raw tiles')):
        _fixed(tile, dict(id=f'rom_{c.TILE_START + index * 32:06X}_tile'), ('pixels',), 'raw tile')
        for line in fixed_list(tile['pixels'], 8, 'pixel rows'):
            pixels = [uint(value, 15, 'pixel nibble') for value in fixed_list(line, 8, 'pixel columns')]
            raw.extend(pixels[x] << 4 | pixels[x + 1] for x in range(0, 8, 2))
    _add(rows, c.TILE_START, c.TILE_END, bytes(raw), 'dictionary_raw_tiles', 'raw_4bpp_pixel_tiles')
    if any(a['end'] != b['start'] for a, b in zip(sorted(rows, key=lambda x: x['start']),
                                               sorted(rows, key=lambda x: x['start'])[1:])):
        raise ValueError('dictionary tail contains a gap or overlap')
    return _finish(rows, contract, c.EDITABLE_BYTES)


def geometry_contract(resource_id, canonical_fields):
    """Offline typed-topology projection; persist before encoding later edits."""
    encoders = dict(terrain_maps=terrain_maps, vdp_word_streams=vdp_word_streams,
                    battle_graphics=battle_graphics, dictionary_streams=dictionary_streams,
                    vdp_directory_fields=vdp_directory_fields,
                    vdp_empty_marker_fields=vdp_empty_marker_fields)
    if type(resource_id) is not str or resource_id not in encoders:
        raise ValueError('explicit independently owned WORD/map resource ID required')
    contract = dict(adapter=resource_id, adapter_module=__name__, format=canonical_fields['format'],
                    confidence='preserved_original_resource_classification',
                    semantic_meaning='confirmed_encoding_not_natural_behavior',
                    limits=['fixed editor allocation is not a CPU selector/coordinate clamp',
                            'ROM-independent encoding is not edited CPU/VDP/gameplay validation',
                            'legacy pure field serializers and projections are disclosed dependencies'])
    if resource_id == 'dictionary_streams':
        contract['datasets'] = _token_plan(canonical_fields)
        contract['limits'].append('fixed token classes and complete count-delimited prefixes retained; unread suffix fields still encoded')
    if resource_id == 'terrain_maps':
        contract['limits'].append('394 canonical type references confirmed; 118 unreferenced type BYTEs remain probable; outside biased allocation not supplied')
    if resource_id == 'vdp_word_streams':
        contract['dependencies'] = dict(empty_marker_authority='vdp_empty_marker_fields',
                                       terrain_authority='world_resources.terrain_codes',
                                       directory_authority='vdp_directory_fields', duplicate_emission=False)
        contract['limits'].append('19 nonempty streams only; unknown D4D41, EE5EF marker and EE5F0..EE5F2 terrain are excluded')
    if resource_id == 'vdp_directory_fields':
        contract['limits'].append('same old vdp_word_streams typed author; 80 targets pinned by its schema, not new editable fields')
    if resource_id == 'vdp_empty_marker_fields':
        contract['limits'].append('marker full-BYTE editing can change live neighboring-source grammar; not an enforced empty three-BYTE allocation')
    if resource_id == 'battle_graphics':
        contract['limits'].append('16 physical marker/zero tail BYTEs retained although full-entry map consumer does not read them; alignment BYTEs excluded')
    rows = encoders[resource_id](canonical_fields, contract)
    contract.update(spans=coalesced_spans(rows), bytes=sum(len(row['data']) for row in rows),
                    physical_blocks=len(rows))
    return contract
