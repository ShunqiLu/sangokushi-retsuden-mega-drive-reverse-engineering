"""ROM-independent encoders for four candidate tile/sprite resource families.

The input is typed editable JSON plus explicit fixed editor geometry. No ROM,
reference assembly, opaque binary input, filesystem access or legacy whole-ROM
validator is used. Pure legacy field serializers are disclosed dependencies;
the allocations below are editor contracts, never natural CPU selector bounds.
"""
from __future__ import annotations

from tools.resource_metadata import compare_fixed_fields

from tools.sprite_word_resources import codec as sprite_words
from tools.battle_variant_tiles import codec as variants
from tools.world_tile_chunks import codec as world
from tools.compact_sprite_records import codec as compact
from tools.graphics_build import rle_fields as rle
from tools.dictionary_streams import codec as dictionary
from tools.vdp_word_streams import format as fmt
from .resource_adapters import block, coalesced_spans, fixed_list, uint


def _package(fields, codec, collections):
    compare_fixed_fields(fields, codec.metadata(), collections, 'typed tile/sprite package')


def _fixed_row(row, fixed, editable, label):
    compare_fixed_fields(row, fixed, editable, label)


def _add(rows, start, end, data, ident, role):
    if type(data) is not bytes or len(data) != end - start:
        raise ValueError('fixed resource encoded allocation differs')
    rows.append(block(start, data, ident, role))


def _finish(rows, contract, expected):
    rows.sort(key=lambda row: row['start'])
    actual = coalesced_spans(rows)  # Also rejects duplicate physical authority.
    if sum(len(row['data']) for row in rows) != expected:
        raise ValueError('fixed physical resource byte count differs')
    if 'spans' in contract and actual != contract['spans']:
        raise ValueError('independent fixed resource geometry differs')
    return rows


def _word_rle(fields, start, end, ident, role):
    fmt.strict_commands(fields)
    encoded, decoded = rle.pack_word(fields, 'little', 4096)
    if len(encoded) != end - start or len(decoded) != 8192:
        raise ValueError('fixed little-WORD RLE cost or decoded allocation differs')
    if rle.parse_word(encoded, 'little', 4096) != fields:
        raise ValueError('RLE command representation/termination differs')
    return block(start, encoded, ident, role)


def sprite_word_resources(fields, contract):
    """32 fixed sprites, live catalogs, little-WORD RLE and two FE/FF sets."""
    c = sprite_words
    _package(fields, c, ('sprite_directory', 'sprites', 'tile_stream',
                         'dictionary_directories', 'dictionary_streams'))
    rows = []
    sprite_catalog = {c.ident(p): p for p in range(c.SPRITE_START, c.SPRITE_END, 8)}
    targets = fixed_list(fields['sprite_directory'], 32, 'sprite directory')
    if any(type(target) is not str or target not in sprite_catalog for target in targets):
        raise ValueError('sprite target outside fixed editor catalog')
    _add(rows, c.SPRITE_DIRECTORY, c.SPRITE_START,
         b''.join(sprite_catalog[target].to_bytes(4, 'big') for target in targets),
         c.ident(c.SPRITE_DIRECTORY), 'candidate_sprite_directory')
    source_sprites = fixed_list(fields['sprites'], 32, 'fixed sprite slots')
    raw = b''.join(c.sprite_bytes(row, start) for row, start in
                   zip(source_sprites, range(c.SPRITE_START, c.SPRITE_END, 8)))
    _add(rows, c.SPRITE_START, c.SPRITE_END, raw, c.ident(c.SPRITE_START),
         'candidate_packed_sprite_descriptors')
    rows.append(_word_rle(fields['tile_stream'], c.SPRITE_END, c.RLE_END,
                          c.ident(c.SPRITE_END), 'candidate_little_word_rle_tiles'))
    dirs = fields['dictionary_directories']
    fmt.keys(dirs, {'source_targets', 'dictionary_targets'}, 'dictionary directories')
    catalog = {c.ident(base): (base, source) for base, source, _, _ in c.SETS}
    directory = []
    for key, lane in (('source_targets', 1), ('dictionary_targets', 0)):
        for target in fixed_list(dirs[key], 2, key):
            if type(target) is not str or target not in catalog:
                raise ValueError('dictionary target outside fixed editor catalog')
            directory.append(catalog[target][lane].to_bytes(4, 'big'))
    _add(rows, 0x68C14, 0x68C24, b''.join(directory), c.ident(0x68C14),
         'candidate_word_resource_directories')
    sets = fixed_list(fields['dictionary_streams'], 2, 'dictionary sets')
    encoded_sets, counts = {}, bytearray()
    for index, (row, (base, source, end, count_at)) in enumerate(zip(sets, c.SETS)):
        fixed = c.set_metadata(index)
        _fixed_row(row, fixed, ('dictionary_pairs', 'source_tokens'), 'dictionary set')
        pairs = fixed_list(row['dictionary_pairs'], (source - base) // 4, 'dictionary pairs')
        dict_raw = b''.join(uint(word, 65535, 'dictionary WORD').to_bytes(2, 'big')
                            for pair in pairs for word in fixed_list(pair, 2, 'dictionary pair'))
        tokens = fixed_list(row['source_tokens'], (end - source) // 2, 'counted source tokens')
        source_raw = b''.join(dictionary.token_word(token).to_bytes(2, 'big') for token in tokens)
        _add(rows, base, source, dict_raw, c.ident(base), 'candidate_two_word_dictionary')
        _add(rows, source, end, source_raw, c.ident(source), 'candidate_counted_fe_ff_source')
        encoded_sets[row['id']] = (dict_raw, source_raw)
        counts.extend(uint(row['count_word'], 65535, 'slot source count').to_bytes(2, 'big'))
    _add(rows, 0x6BF06, 0x6BF0A, bytes(counts), c.ident(0x6BF06), 'candidate_source_count_words')
    for slot in range(2):
        # Original count is tied to the caller slot, not the redirected source.
        dict_raw = encoded_sets[dirs['dictionary_targets'][slot]][0]
        source_raw = encoded_sets[dirs['source_targets'][slot]][1]
        result = dictionary.evaluate(source_raw, dict_raw, sets[slot]['count_word'])
        if (result['source_bytes_read'] != len(source_raw) or
                result['pending_final_byte'] != 0 or len(result['decoded']) != 8192):
            raise ValueError('edited dictionary pairing violates fixed decoding contract')
    return _finish(rows, contract, c.EDITABLE_BYTES)


def battle_variant_tiles(fields, contract):
    """12 physical little-WORD streams; 3 live aliased five-entry catalogs."""
    c = variants
    _package(fields, c, ('directories', 'streams'))
    rows, catalog = [], {c.ident(start): start for start in c.STARTS}
    for row, (name, start, _) in zip(fixed_list(fields['directories'], 3, 'directories'), c.DIRECTORIES):
        _fixed_row(row, dict(id=name, start=start), ('targets',), 'variant directory')
        targets = fixed_list(row['targets'], 5, 'variant targets')
        if any(type(target) is not str or target not in catalog for target in targets):
            raise ValueError('variant target outside fixed physical editor catalog')
        _add(rows, start, start + 20,
             b''.join(catalog[target].to_bytes(4, 'big') for target in targets),
             name, 'candidate_variant_tile_directory')
    for row, (start, end) in zip(fixed_list(fields['streams'], 12, 'streams'), zip(c.STARTS, c.ENDS)):
        _fixed_row(row, c.stream_metadata(start, end), ('fields',), 'variant stream')
        rows.append(_word_rle(row['fields'], start, end, c.ident(start),
                              'candidate_little_word_variant_tiles'))
    return _finish(rows, contract, c.EDITABLE_BYTES)


def _world_topology(fields):
    chunks = []
    for chunk in fixed_list(fields['chunks'], 24, 'world chunks'):
        fmt.keys(chunk, {'id', 'start', 'end', 'columns'}, 'world chunk')
        start, end = uint(chunk['start'], fmt.ROM_SIZE - 1), uint(chunk['end'], fmt.ROM_SIZE)
        fmt.same(chunk['id'], world.ident(start), 'world chunk id')
        costs = [len(world.pack_column(column)[0]) for column in
                 fixed_list(chunk['columns'], 24, 'world columns')]
        if start + 54 + sum(costs) != end:
            raise ValueError('world header + column costs do not fill declared chunk')
        chunks.append(dict(id=chunk['id'], start=start, end=end, column_source_bytes=costs))
    if (chunks[0]['start'] != world.START or chunks[-1]['end'] != world.DIR or
            any(a['end'] != b['start'] for a, b in zip(chunks, chunks[1:]))):
        raise ValueError('continuous 24-chunk physical partition differs')
    return chunks


def world_tile_chunks(fields, contract):
    """BE column grammar; preserve each fixed column cost, ignored high bits."""
    c = world
    _package(fields, c, ('directory', 'chunks'))
    topology = fixed_list(contract['chunks'], 24, 'fixed world chunk geometry')
    rows, catalog = [], {row['id']: row['start'] for row in topology}
    fixed_dir = dict(start=c.DIR, index_stride_word=4, width_byte=24, height_byte=40, base=c.START)
    directory = fields['directory']
    _fixed_row(directory, fixed_dir, ('targets',), 'world directory')
    offsets = []
    for target in fixed_list(directory['targets'], 29, 'world directory targets'):
        if target is None:
            offsets.append(65535)
        elif type(target) is str and target in catalog:
            offsets.append(uint(catalog[target] - c.START, 65535, 'directory relative WORD'))
        else:
            raise ValueError('world target outside fixed physical chunk catalog')
    for chunk, fixed in zip(fixed_list(fields['chunks'], 24, 'world chunks'), topology):
        _fixed_row(chunk, {key: fixed[key] for key in ('id', 'start', 'end')}, ('columns',), 'world chunk')
        costs = fixed_list(fixed['column_source_bytes'], 24, 'fixed column costs')
        encoded_columns, boundaries = [], [0]
        for commands, cost in zip(fixed_list(chunk['columns'], 24, 'columns'), costs):
            uint(cost, 80, 'column source cost')
            source, _ = c.pack_column(commands)
            if len(source) != cost or c.parse_column(source) != commands:
                raise ValueError('fixed column source cost/representation differs')
            encoded_columns.append(source)
            boundaries.append(uint(boundaries[-1] + cost, 65535, 'column boundary WORD'))
        data_base = uint(fixed['start'] + 54, fmt.ROM_SIZE - 1, 'column data base')
        raw = data_base.to_bytes(4, 'big') + b''.join(n.to_bytes(2, 'big') for n in boundaries)
        raw += b''.join(encoded_columns)
        _add(rows, fixed['start'], fixed['end'], raw, fixed['id'], 'candidate_world_tile_column_chunk')
    directory_data = b''.join((n.to_bytes(width, 'big') for n, width in
                              ((4, 2), (24, 1), (40, 1), (c.START, 4))))
    directory_data += b''.join(n.to_bytes(2, 'big') for n in offsets)
    _add(rows, c.DIR, c.END, directory_data, 'world_chunk_directory', 'candidate_world_tile_chunk_directory')
    if any(a['end'] != b['start'] for a, b in zip(rows, rows[1:])):
        raise ValueError('continuous world partition differs')
    return _finish(rows, contract, c.EDITABLE_BYTES)


def _compact_topology(fields):
    rows = []
    for descriptor in fixed_list(fields['descriptors'], 93, 'compact descriptors'):
        fmt.keys(descriptor, {'id', 'start', 'end', 'terminator_byte', 'records'}, 'descriptor')
        start, end = uint(descriptor['start'], fmt.ROM_SIZE - 1), uint(descriptor['end'], fmt.ROM_SIZE)
        fmt.same(descriptor['id'], compact.ident(start), 'compact descriptor id')
        records = descriptor['records']
        if type(records) is not list or not 1 <= len(records) <= 127 or end != start + 4 * len(records) + 1:
            raise ValueError('compact record count/terminator geometry differs')
        rows.append(dict(id=descriptor['id'], start=start, end=end, record_count=len(records)))
    if (rows[0]['start'] != compact.START or rows[-1]['end'] + 1 != compact.END or
            any(a['end'] + 1 != b['start'] for a, b in zip(rows, rows[1:])) or
            sum(row['record_count'] for row in rows) != 3010):
        raise ValueError('93 descriptors + excluded unread BYTE gaps differ')
    return rows


def compact_sprite_records(fields, contract):
    """Four-BYTE records plus 80 terminator; two-level live BE32 catalogs."""
    c = compact
    _package(fields, c, ('descriptors', 'directories'))
    geometry = fixed_list(contract['descriptors'], 93, 'fixed descriptor geometry')
    catalog = {row['id']: row['start'] for row in geometry}
    pointer_slots = {c.pointer_id(p): p for _, start, end, kind in c.DIRS
                     if kind == 'descriptor' for p in range(start, end, 4)}
    rows = []
    for descriptor, fixed in zip(fixed_list(fields['descriptors'], 93, 'descriptors'), geometry):
        identity = {key: fixed[key] for key in ('id', 'start', 'end')}
        _fixed_row(descriptor, dict(identity, terminator_byte=128), ('records',), 'descriptor')
        records = fixed_list(descriptor['records'], fixed['record_count'], 'fixed sprite record slots')
        data = b''.join(c.record_bytes(row) for row in records) + bytes((128,))
        _add(rows, fixed['start'], fixed['end'], data, fixed['id'], 'candidate_compact_sprite_records')
    for row, (name, start, end, kind) in zip(fixed_list(fields['directories'], 4, 'directories'), c.DIRS):
        _fixed_row(row, dict(id=name, start=start, end=end, target_kind=kind), ('targets',), 'sprite directory')
        valid = pointer_slots if kind == 'secondary' else catalog
        targets = fixed_list(row['targets'], (end - start) // 4, 'sprite pointer targets')
        if any(type(target) is not str or target not in valid for target in targets):
            raise ValueError('sprite pointer outside fixed existing editor catalog')
        data = b''.join(valid[target].to_bytes(4, 'big') for target in targets)
        _add(rows, start, end, data, name, 'candidate_compact_sprite_pointer_directory')
    return _finish(rows, contract, c.EDITABLE_BYTES)


def geometry_contract(resource_id, canonical_fields):
    """Pure one-time fixed geometry projection from the declared typed source.

    The delivery registry persists this output; edits are encoded against that
    persisted geometry, not used to silently recalculate new slot capacities.
    The canonical argument is JSON fields, not ROM bytes or a binary capture.
    """
    encoders = dict(sprite_word_resources=sprite_word_resources,
                    battle_variant_tiles=battle_variant_tiles,
                    world_tile_chunks=world_tile_chunks,
                    compact_sprite_records=compact_sprite_records)
    if type(resource_id) is not str or resource_id not in encoders:
        raise ValueError('one of the four explicitly owned tile/sprite families required')
    contract = dict(adapter=resource_id, adapter_module=__name__,
                    format=canonical_fields['format'], confidence='candidate',
                    semantic_meaning='preserved_source_classification_not_promoted',
                    limits=['fixed editor allocation is not a CPU selector clamp',
                            'encoding does not prove natural gameplay/VDP/SAT behavior',
                            'old pure pack helpers remain disclosed dependencies'])
    if resource_id == 'world_tile_chunks':
        contract['chunks'] = _world_topology(canonical_fields)
        contract['limits'].append('original first/continuing low11=06FF inconsistency is preserved by rejecting ambiguous editor input')
    if resource_id == 'compact_sprite_records':
        contract['descriptors'] = _compact_topology(canonical_fields)
        contract['limits'].append('one unread BYTE after each 80 terminator is excluded')
    rows = encoders[resource_id](canonical_fields, contract)
    contract['spans'] = coalesced_spans(rows)
    contract['bytes'] = sum(len(row['data']) for row in rows)
    contract['physical_blocks'] = len(rows)
    return contract
