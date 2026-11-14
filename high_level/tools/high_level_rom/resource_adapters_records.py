"""Pure encoders for fixed-layout scenario, text and selection records.

Confirmed: only the explicit typed fields and a separately supplied, frozen
topology contract generate bytes. No ROM, old serializer, file, preview text,
native build or cached block is consulted. The contract holds identities,
widths, extents and grammar positions, not replacement payloads.

Candidate/unknown: address-based scenario labels and candidate rule meanings
retain the source classifications. Fixed-shape editor policies are not claims
about natural gameplay inputs. Unknown holes stay unowned; no encoder fills
them. Shared personnel terminator/offset storage has one physical authority.
"""
from __future__ import annotations

import re


_DIGEST_TEXT = re.compile(r'[0-9a-f]{64}')
_PATH_PART = re.compile(r'[A-Za-z0-9_][A-Za-z0-9_.-]*')
_LEGACY_PACKAGE_DIGEST_PATHS = {
    'world_resources': (('canonical_rom_sha256',),),
    'scenario_build': (('canonical_rom_sha256',),),
    'legacy_text_fields': (('canonical_source', 'sha256'),),
    'personnel_flow': (('candidate_block', 'sha256'), ('canonical_source', 'sha256')),
}


def _uint(value, maximum, label):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError(f'{label}: strict unsigned integer outside 0..{maximum}')
    return value


def _metadata_text(value, shape, label, *, suffix=None):
    """Validate the representation of metadata that supplies no encoded value."""
    if type(value) is not str:
        raise ValueError(f'{label}: metadata text required')
    if shape == 'hex64':
        if not _DIGEST_TEXT.fullmatch(value):
            raise ValueError(f'{label}: 64 lowercase hexadecimal characters required')
    elif shape == 'relative_path':
        parts = value.split('/')
        if (len(value) > 512 or len(parts) < 2 or
                any(not _PATH_PART.fullmatch(part) or part.endswith('.') for part in parts)):
            raise ValueError(f'{label}: ordinary relative metadata path required')
        final = parts[-1]
        if (suffix is None and '.' in final) or (suffix is not None and not final.endswith(suffix)):
            raise ValueError(f'{label}: metadata path kind differs')
    else:
        raise ValueError(f'{label}: unknown metadata text shape')


def _nested_digests(paths, key):
    return tuple(path[1:] for path in paths if len(path) > 1 and path[0] == key) if paths else ()


def _same(value, expected, label, *, legacy_digest_paths=()):
    """Compare the fixed shape, including types and all ordinary values."""
    if type(value) is not type(expected):
        raise ValueError(f'{label}: fixed field type differs')
    if type(expected) is dict:
        _keys(value, expected, label, legacy_digest_paths=legacy_digest_paths)
        for key in expected:
            _same(value[key], expected[key], f'{label}.{key}',
                  legacy_digest_paths=_nested_digests(legacy_digest_paths, key))
    elif type(expected) is list:
        _list(value, len(expected), label)
        for index, (item, old) in enumerate(zip(value, expected)):
            _same(item, old, f'{label}[{index}]',
                  legacy_digest_paths=_nested_digests(legacy_digest_paths, index))
    elif value != expected:
        raise ValueError(f'{label}: fixed topology differs')


def _keys(value, expected, label, *, legacy_digest_paths=()):
    if type(value) is not dict:
        raise ValueError(f'{label}: object fields differ')
    keys = set(expected)
    extra = value.keys() - keys
    optional = {path[0] for path in legacy_digest_paths if len(path) == 1}
    if keys - value.keys() or extra - optional:
        raise ValueError(f'{label}: object fields differ')
    for key in extra:
        _metadata_text(value[key], 'hex64', f'{label}.{key}')


def _list(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(f'{label}: fixed physical count differs')
    return value


def _fixed(value, metadata, mutable, label, *, legacy_digest_paths=()):
    _keys(value, set(metadata) | set(mutable), label, legacy_digest_paths=legacy_digest_paths)
    for key, expected in metadata.items():
        _same(value[key], expected, f'{label}.{key}',
              legacy_digest_paths=_nested_digests(legacy_digest_paths, key))


def _begin(fields, contract, ident):
    if type(contract) is not dict or contract.get('adapter') != ident:
        raise ValueError('wrong independent resource contract')
    topology = contract['topology']
    _fixed(fields, topology['metadata'], topology['mutable'], ident,
           legacy_digest_paths=_LEGACY_PACKAGE_DIGEST_PATHS.get(ident, ()))
    return topology


def _pack(value, width, label):
    return _uint(value, (1 << (8 * width)) - 1, label).to_bytes(width, 'big')


def _block(start, data, ident, role):
    _uint(start, 0xFFFFF, ident + '.start')
    if type(data) is not bytes or not data or start + len(data) > 0x100000:
        raise ValueError(f'{ident}: nonempty bytes within linear ROM required')
    return dict(id=ident, start=start, end=start + len(data), data=data, role=role)


def _spans(rows):
    merged = []
    previous = None
    for row in sorted(rows, key=lambda item: item['start']):
        if previous is not None and row['start'] < previous['end']:
            raise ValueError(f"physical overlap: {previous['id']} and {row['id']}")
        if merged and row['start'] == merged[-1][1]:
            merged[-1][1] = row['end']
        else:
            merged.append([row['start'], row['end']])
        previous = row
    return merged


def _finish(rows, contract):
    rows.sort(key=lambda item: item['start'])
    _same(_spans(rows), contract['spans'], 'independent geometry')
    _same(sum(len(row['data']) for row in rows), contract['encoded_bytes'], 'byte total')
    return rows


def _glyph(value, *, signed_window):
    """The existing 16-bit shift/OR font geometry, with no bitmap dependency."""
    _uint(value, 0xFFFF, 'glyph WORD')
    if value & 255 > 63:
        raise ValueError('glyph column exceeds fixed editor vocabulary')
    offset = (((value & 0xFF00) << 3) & 0xFFFF) | (((value & 255) << 5) & 0xFFFF)
    if offset // 32 >= 1034 or signed_window and offset >= 0x8000:
        raise ValueError('glyph outside the confirmed editor font window')


def _dialogue_token(word):
    _uint(word, 0xFFFF, 'main-dialogue WORD')
    if word == 0:
        return 'special_fixed_bitmap'
    if word & 0x8000:
        if word & 255 not in range(0, 22, 2):
            raise ValueError('unresolved main-dialogue control selector')
        return 'control'
    _glyph(word, signed_window=True)
    return 'glyph'


def dialogue_text(fields, contract):
    """Two page directories, 275 messages and separate raw name glyph WORDs."""
    top = _begin(fields, contract, 'dialogue_text')
    _same(fields['directory'], top['directory'], 'main directory')
    directory = fields['directory']
    raw = bytearray(_pack(directory['page_base'], 4, 'page base'))
    for target in directory['page_targets']:
        delta = target - directory['page_base']
        if type(target) is not int or not -32768 <= delta <= 32767:
            raise ValueError('signed directory offset outside WORD')
        raw.extend(delta.to_bytes(2, 'big', signed=True))
    result = [_block(directory['address'], bytes(raw), 'main_directory', 'directory')]
    known = {row['metadata']['id']: row['metadata']['start'] for row in top['records']}
    for page, frozen in zip(_list(fields['pages'], len(top['pages']), 'pages'), top['pages']):
        _fixed(page, frozen['metadata'], ('entries',), 'page')
        raw = bytearray(_pack(page['text_base'], 4, 'text base'))
        for target in _list(page['entries'], frozen['count'], 'page entries'):
            if type(target) is not str or target not in known:
                raise ValueError('page must reference an existing physical message')
            delta = known[target] - page['text_base']
            if not -32768 <= delta <= 32767:
                raise ValueError('signed message offset outside WORD')
            raw.extend(delta.to_bytes(2, 'big', signed=True))
        result.append(_block(page['start'], bytes(raw), f"page_{page['index']}", 'page_offsets'))
    for row, frozen in zip(_list(fields['records'], len(top['records']), 'messages'), top['records']):
        _fixed(row, frozen['metadata'], ('tokens',), 'message')
        words = []
        for item in _list(row['tokens'], frozen['count'], 'message WORDs'):
            _keys(item, ('type', 'word'), 'main token')
            _same(item['type'], _dialogue_token(item['word']), 'token kind')
            words.append(item['word'])
        # The original grammar identifies restore by the low control selector;
        # attribute bits are not silently normalized to a canonical 8000.
        is_restore = lambda value: bool(value & 0x8000) and value & 255 == 0
        if not words or not is_restore(words[-1]) or any(is_restore(v) for v in words[:-1]):
            raise ValueError('one final restore-saved-mode token required')
        result.append(_block(row['start'], b''.join(_pack(v, 2, 'message WORD') for v in words), row['id'], 'message_words'))
    for section in ('officer_names', 'city_names'):
        for row, frozen in zip(_list(fields[section], len(top[section]), section), top[section]):
            _fixed(row, frozen['metadata'], ('words',), section)
            words = _list(row['words'], frozen['count'], section + '.words')
            for word in words:
                _uint(word, 0x1FFF, 'raw name glyph')
                if _dialogue_token(word | 0x4000) != 'glyph':
                    raise ValueError('name WORD must insert a glyph')
            if section == 'officer_names' and all(v == 63 for v in words):
                raise ValueError('all-blank officer name trims into unmodelled preceding RAM')
            result.append(_block(row['start'], b''.join(_pack(v, 2, 'name WORD') for v in words), row['id'], section))
    return _finish(result, contract)


def _legacy_kind(word, dialect):
    _uint(word, 0xFFFF, 'legacy WORD')
    vocabularies = {
        'ff_control_stream': (0xFF00, 0xFF01, 0xFF02, 0xFF03, 0xFF0A, 0xFF20),
        '80_control_stream': (0x8002, 0x8008, 0x800A, 0x800E, 0x8010, 0x8011, 0x8012),
    }
    if dialect not in vocabularies or word in (0xFFFF, 0x8000):
        raise ValueError('unknown dialect or a terminator inside the legacy body')
    if word & 0x8000:
        if word not in vocabularies[dialect]:
            raise ValueError('unknown or cross-dialect legacy control')
        return 'control'
    _glyph(word, signed_window=False)
    return 'glyph'


def legacy_text_fields(fields, contract):
    """Keep FF/80 dialects separate and preserve every control position."""
    top = _begin(fields, contract, 'legacy_text_fields')
    known = {row['metadata']['id']: row['metadata']['start'] for row in top['records'][:52]}
    raw = bytearray()
    for row, frozen in zip(_list(fields['directory'], 52, 'legacy directory'), top['directory']):
        _fixed(row, frozen, ('source',), 'legacy pointer')
        if type(row['source']) is not str or row['source'] not in known:
            raise ValueError('legacy pointer must target one of the 52 physical FF records')
        raw.extend(_pack(known[row['source']], 4, 'legacy pointer'))
    result = [_block(top['directory_start'], bytes(raw), 'legacy_directory', 'confirmed_legacy_BE32_directory')]
    for row, frozen in zip(_list(fields['records'], len(top['records']), 'legacy records'), top['records']):
        _fixed(row, frozen['metadata'], ('tokens',), 'legacy record')
        words = []
        for item, kind in zip(_list(row['tokens'], len(frozen['kinds']), 'legacy body'), frozen['kinds']):
            _keys(item, ('kind', 'WORD'), 'legacy token')
            _same(item['kind'], _legacy_kind(item['WORD'], row['dialect']), 'legacy kind')
            _same(item['kind'], kind, 'original control/glyph position')
            words.append(item['WORD'])
        words.append(row['terminator_WORD'])
        result.append(_block(row['start'], b''.join(_pack(v, 2, 'legacy WORD') for v in words), row['id'], 'confirmed_legacy_' + row['dialect']))
    return _finish(result, contract)


def scenario_build(fields, contract):
    """Encode full source fields, not derived loader RAM or invented names."""
    top = _begin(fields, contract, 'scenario_build')
    _list(fields['directory_targets'], 3, 'scenario directory')
    starts = {row['id']: row['start'] for row in top['scenarios']}
    addresses = {f"{row['id']}.{spec['id']}": row['start'] + spec['offset']
                 for row in top['scenarios'] for spec in top['tables']}
    raw = bytearray()
    for target in fields['directory_targets']:
        if type(target) is not str or target not in starts:
            raise ValueError('scenario directory target not in fixed physical catalog')
        raw.extend(_pack(starts[target], 4, 'scenario target'))
    result = [_block(top['directory_start'], bytes(raw), 'scenario_directory', 'scenario_directory')]
    for scenario, frozen in zip(_list(fields['scenarios'], 3, 'scenarios'), top['scenarios']):
        _keys(scenario, ('id', 'descriptor_targets', 'cities', 'forces', 'officers'), 'scenario')
        _same(scenario['id'], frozen['id'], 'scenario id')
        _keys(scenario['descriptor_targets'], (spec['id'] for spec in top['tables']), 'descriptor')
        descriptor = bytearray()
        for spec in top['tables']:
            target = scenario['descriptor_targets'][spec['id']]
            allowed = {f"{ident}.{spec['id']}" for ident in starts}
            if type(target) is not str or target not in allowed:
                raise ValueError('descriptor may alias only the same typed table in another scenario')
            descriptor.extend(_pack(addresses[target], 4, 'descriptor target'))
        result.append(_block(frozen['start'], bytes(descriptor), frozen['id'] + '.descriptor', 'scenario_descriptor'))
        for group in top['groups']:
            specs = [spec for spec in top['tables'] if spec['group'] == group['name']]
            rows = _list(scenario[group['name']], group['count'], group['name'])
            for index, row in enumerate(rows):
                _keys(row, {'id'} | {spec['id'] for spec in specs}, 'scenario record')
                _same(row['id'], index + group['first'], 'record id')
            for spec in specs:
                raw = bytearray()
                for row in rows:
                    value = row[spec['id']]
                    if spec['encoding'] == 'split_long':
                        _keys(value, ('unknown_high_word', 'value_low_word'), 'split source LONG')
                        raw.extend(_pack(value['unknown_high_word'], 2, 'unknown high WORD'))
                        raw.extend(_pack(value['value_low_word'], 2, 'value low WORD'))
                    elif spec['encoding'] == 'equipment_bytes':
                        _keys(value, ('source_byte0', 'source_byte1', 'source_byte2'), 'equipment source')
                        for slot in range(3):
                            raw.extend(_pack(value[f'source_byte{slot}'], 1, 'equipment BYTE'))
                    else:
                        raw.extend(_pack(value, spec['width'], spec['id']))
                ident = frozen['id'] + '.' + spec['id']
                result.append(_block(addresses[ident], bytes(raw), ident, 'scenario_source_' + spec['id']))
    return _finish(result, contract)


def world_resources(fields, contract):
    """Ordered candidate rows and mask bytes are not inferred as graph rules."""
    top = _begin(fields, contract, 'world_resources')
    streams = {'terrain_costs': bytes(_uint(v, 255, 'terrain cost') for v in _list(fields['terrain_costs'], 6, 'terrain costs'))}
    coordinates, availability, candidates = bytearray(), bytearray(), bytearray()
    for index, row in enumerate(_list(fields['cities'], 40, 'cities'), start=1):
        _keys(row, ('id', 'x_fixed16', 'y_fixed16', 'availability', 'candidates', 'terminator', 'padding'), 'city')
        _same(row['id'], index, 'city id')
        x, y = _uint(row['x_fixed16'], 65535, 'city x'), _uint(row['y_fixed16'], 65535, 'city y')
        if not 1 <= x >> 4 < 72 or not 0 <= y >> 4 < 72:
            raise ValueError('city coordinate outside existing fixed editor footprint')
        coordinates.extend(_pack(x, 2, 'city x') + _pack(y, 2, 'city y'))
        availability.extend(_uint(v, 255, 'city mask') for v in _list(row['availability'], 3, 'city masks'))
        values = row['candidates']
        if type(values) is not list or len(values) > 7:
            raise ValueError('at most seven ordered city candidates fit the fixed slot')
        for value in values:
            _uint(value, 40, 'candidate city')
            if value == 0:
                raise ValueError('city candidate editor ID must be 1..40')
        terminator = _uint(row['terminator'], 255, 'candidate terminator')
        if terminator < 128:
            raise ValueError('candidate terminator must keep its negative BYTE')
        candidates.extend(values)
        candidates.append(terminator)
        candidates.extend(_uint(v, 255, 'candidate padding') for v in _list(row['padding'], 7 - len(values), 'candidate padding'))
    streams.update(city_coordinates=bytes(coordinates), city_availability=bytes(availability), city_candidates=bytes(candidates))
    coordinates, availability = bytearray(), bytearray()
    for index, row in enumerate(_list(fields['points'], 6, 'points')):
        _keys(row, ('index', 'x', 'y', 'availability'), 'point')
        _same(row['index'], index, 'point index')
        coordinates.extend((_uint(row['x'], 127, 'point x'), _uint(row['y'], 255, 'point y')))
        availability.extend(_uint(v, 255, 'point mask') for v in _list(row['availability'], 3, 'point masks'))
    terminator = _uint(fields['point_terminator'], 255, 'point terminator')
    if terminator < 128:
        raise ValueError('point terminator must keep its negative BYTE')
    coordinates.append(terminator)
    streams.update(point_coordinates=bytes(coordinates), point_availability=bytes(availability))
    terrain = bytearray()
    for row in _list(fields['terrain_rows'], 72, 'terrain rows'):
        terrain.extend(_uint(v, 5, 'terrain code') for v in _list(row, 72, 'terrain columns'))
    streams['terrain_codes'] = bytes(terrain)
    return _finish([_block(item['start'], streams[item['id']], item['id'], 'world_source_' + item['id']) for item in top['allocations']], contract)


def _fixed_word_tables(fields, contract, ident):
    top = _begin(fields, contract, ident)
    result = []
    for spec in top['tables']:
        values = _list(fields[spec['id']], spec['count'], spec['id'])
        raw = b''.join(_pack(value, spec['width'], spec['id']) for value in values)
        result.append(_block(spec['start'], raw, spec['id'], 'candidate_fixed_width_' + spec['id']))
    return _finish(result, contract)


def candidate_tables(fields, contract):
    """Unsigned offset WORDs and threshold LONG/seed WORD pairs stay raw."""
    top = _begin(fields, contract, 'candidate_tables')
    result = []
    for section, start in (('filter_dispatch_offsets', top['filter_start']), ('action_dispatch_offsets', top['action_start'])):
        raw = b''.join(_pack(v, 2, section) for v in _list(fields[section], 6, section))
        result.append(_block(start, raw, section, 'candidate_dispatch_words'))
    raw = bytearray()
    for row in _list(fields['numeric_records'], 39, 'numeric records'):
        _keys(row, ('threshold_long', 'seed_word'), 'numeric record')
        raw.extend(_pack(row['threshold_long'], 4, 'threshold LONG') + _pack(row['seed_word'], 2, 'seed WORD'))
    result.append(_block(top['numeric_start'], bytes(raw), 'numeric_records', 'candidate_threshold_seed_pairs'))
    return _finish(result, contract)


def candidate_action_tables(fields, contract):
    return _fixed_word_tables(fields, contract, 'candidate_action_tables')


def candidate_handler_tables(fields, contract):
    return _fixed_word_tables(fields, contract, 'candidate_handler_tables')


def _qualifier(raw):
    _uint(raw, 65535, 'personnel qualifier WORD')
    if raw & 0x8000:
        return 'unconditional_flagged', raw & 0x7FFF
    if raw & 0x4000:
        return 'literal_force_code', raw & 255
    return 'reference_officer_id', raw


def personnel_flow(fields, contract):
    """Pack variable-list contents within frozen physical shapes, without ROM.

    The fourth force-list terminator and city-offset WORD zero are one storage
    location. Conflicting edits are refused; it is emitted only once. Historical
    Record and layout fields determine byte placement. Optional source digests are metadata.
    """
    top = _begin(fields, contract, 'personnel_flow')
    pointers, result = bytearray(), []
    for scenario, frozen in zip(_list(fields['scenarios'], 3, 'personnel scenarios'), top['scenarios']):
        _fixed(scenario, frozen['metadata'], ('force_year_lists', 'city_rules', 'city_offset_words'),
               'personnel scenario', legacy_digest_paths=(('scenario_sha256',),))
        start = scenario['descriptor_rom_offset']
        pointers.extend(_pack(start, 4, 'external personnel pointer'))
        descriptor = bytearray()
        body = bytearray()
        for slot, (row, force) in enumerate(zip(_list(scenario['force_year_lists'], 4, 'force lists'), frozen['forces'])):
            _fixed(row, force['metadata'], ('entries', 'terminator_raw'), 'force list')
            _same(start + 24 + len(body), force['metadata']['rom_offset'], 'force stream position')
            descriptor.extend(_pack(force['metadata']['rom_offset'], 4, 'force pointer'))
            for entry in _list(row['entries'], force['count'], 'force records'):
                _keys(entry, ('year_threshold_raw', 'officer_id'), 'force record')
                body.extend(_pack(entry['year_threshold_raw'], 2, 'force year WORD'))
                body.extend(_pack(entry['officer_id'], 2, 'force officer WORD'))
            terminator = _uint(row['terminator_raw'], 65535, 'force terminator')
            if not terminator & 0x8000:
                raise ValueError('force terminator must retain bit 15')
            _same(start + 24 + len(body), force['metadata']['terminator_rom_offset'], 'force terminator position')
            if slot < 3:
                body.extend(_pack(terminator, 2, 'force terminator'))
        offsets = _list(scenario['city_offset_words'], 41, 'city offsets')
        for value in offsets:
            _uint(value, 65535, 'city offset WORD')
        _same(offsets[0], scenario['force_year_lists'][3]['terminator_raw'], 'one shared terminator/offset WORD')
        _same(start + 24 + len(body), scenario['city_offset_table_rom_offset'], 'city-offset position')
        descriptor.extend(_pack(scenario['city_offset_table_rom_offset'], 4, 'city-offset pointer'))
        raw_rules = bytearray()
        for index, (row, city) in enumerate(zip(_list(scenario['city_rules'], 40, 'city rules'), frozen['cities']), start=1):
            _fixed(row, city['metadata'], ('entries', 'terminator_raw'), 'city rule')
            _same(offsets[index], len(raw_rules), 'city-offset stream relationship')
            _same(row['relative_offset'], len(raw_rules), 'city relative offset')
            _same(row['rom_offset'], scenario['city_rule_stream_rom_offset'] + len(raw_rules), 'city rule position')
            for entry in _list(row['entries'], city['count'], 'city rule records'):
                _keys(entry, ('year_threshold_raw', 'candidate_officer_id', 'qualifier_raw', 'qualifier_kind', 'qualifier_value'), 'city rule record')
                year = _uint(entry['year_threshold_raw'], 0x7FFF, 'nonterminator city year')
                kind, value = _qualifier(entry['qualifier_raw'])
                _same(entry['qualifier_kind'], kind, 'qualifier kind')
                _same(entry['qualifier_value'], value, 'qualifier value')
                raw_rules.extend(_pack(year, 2, 'city year') + _pack(entry['candidate_officer_id'], 2, 'candidate officer') + _pack(entry['qualifier_raw'], 2, 'raw qualifier'))
            terminator = _uint(row['terminator_raw'], 65535, 'city terminator')
            if not terminator & 0x8000:
                raise ValueError('city terminator must retain bit 15')
            raw_rules.extend(_pack(terminator, 2, 'city terminator'))
        body.extend(b''.join(_pack(value, 2, 'city offset') for value in offsets))
        _same(start + 24 + len(body), scenario['city_rule_stream_rom_offset'], 'rule stream position')
        descriptor.extend(_pack(scenario['city_rule_stream_rom_offset'], 4, 'rule-stream pointer'))
        _same([int.from_bytes(descriptor[i:i + 4], 'big') for i in range(0, 24, 4)], scenario['descriptor_pointers'], 'descriptor topology')
        raw = bytes(descriptor + body + raw_rules)
        _same(len(raw), scenario['scenario_length'], 'personnel scenario extent')
        result.append(_block(start, raw, f"personnel_scenario_{scenario['scenario_index']}", 'candidate_personnel_records'))
    result.append(_block(top['directory_start'], bytes(pointers), 'personnel_directory', 'candidate_personnel_descriptor_pointers'))
    return _finish(result, contract)
