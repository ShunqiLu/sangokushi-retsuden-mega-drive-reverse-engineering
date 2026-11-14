"""Pure typed encoders for UI layouts and first-80 sprite source families.

Generation takes only editable fields and persisted editor geometry. It does
not read ROM/files, call old blocks/pack/extract/rebuild APIs, or supply unknown
gaps. Fixed catalogs are editor allocations, not natural CPU index limits.
All visual purposes keep their existing candidate/probable classifications.
"""
from __future__ import annotations

from tools.resource_metadata import compare_fixed_fields

from tools.title_overlay_maps import codec as title
from tools.battle_overlay_maps import codec as overlay
from tools.menu_tile_streams import codec as menu
from tools.ui_layouts import ui_layouts as layout
from tools.battlefield_resources import battlefield_resources as battlefield
from tools.ui_fixed_records import codec as fixed_ui
from tools.battle_effect_sprites import codec as effect
from tools.battle_scene_sprites import codec as scene
from tools.battle_command_sprites import codec as command
from tools.battle_marker_sprites import codec as marker
from tools.vdp_word_streams import format as shape
from .resource_adapters import block, coalesced_spans, fixed_list, integer, uint


def _fixed(row, fixed, editable, label):
    compare_fixed_fields(row, fixed, editable, label)


def _add(rows, start, end, raw, ident, role):
    if type(raw) is not bytes or len(raw) != end - start:
        raise ValueError('fixed UI encoded extent differs')
    rows.append(block(start, raw, ident, role))


def _finish(rows, contract, expected):
    rows.sort(key=lambda row: row['start'])
    spans = coalesced_spans(rows)
    if sum(len(row['data']) for row in rows) != expected:
        raise ValueError('fixed UI physical byte count differs')
    if 'spans' in contract:
        shape.same(spans, contract['spans'], 'persisted UI geometry')
    return rows


def _words(values, count, label, maximum=65535):
    return b''.join(uint(value, maximum, label).to_bytes(2, 'big')
                    for value in fixed_list(values, count, label))


def _pointers(refs, count, catalog):
    refs = fixed_list(refs, count, 'physical pointer slots')
    if any(type(ref) is not str or ref not in catalog for ref in refs):
        raise ValueError('pointer must name an existing complete source in its editor catalog')
    return b''.join(catalog[ref].to_bytes(4, 'big') for ref in refs)


def _word_rle(fields, output_words, *, prefix=False):
    """Serialize marker, literal/repeat WORD fields without an old pack API.

    Prefix mode keeps the last repeat's complete count but emits no fabricated
    marker-zero. Commands after the row exit are not admitted. Complete mode
    preserves the physical marker-zero even if a CPU row limit stops sooner.
    """
    shape.keys(fields, {'marker', 'commands'}, 'WORD RLE fields')
    escape = uint(fields['marker'], 255, 'RLE marker BYTE')
    commands = fields['commands']
    if type(commands) is not list or not 1 <= len(commands) <= output_words:
        raise ValueError('bounded nonempty WORD command list required')
    raw, emitted = bytearray((escape,)), 0
    for row in commands:
        if prefix and emitted >= output_words:
            raise ValueError('command follows actual prefix row exit')
        if type(row) is not dict:
            raise ValueError('WORD command object required')
        op = row.get('op')
        shape.keys(row, {'op', 'word'} | ({'count'} if op == 'repeat' else set()), 'WORD command')
        word = uint(row['word'], 65535, 'full source WORD').to_bytes(2, 'big')
        if op == 'literal':
            if word[0] == escape:
                raise ValueError('literal high BYTE collides with live marker')
            raw.extend(word)
            emitted += 1
        elif op == 'repeat':
            count = uint(row['count'], 256, 'repeat WORD count')
            if count < 2:
                raise ValueError('repeat count must encode 2..256 WORDs')
            raw.extend((escape, count - 1))
            raw.extend(word)
            emitted += count
        else:
            raise ValueError('unknown WORD command operation')
        if not prefix and emitted > output_words:
            raise ValueError('complete physical WORD output overrun')
    if emitted < output_words or (not prefix and emitted != output_words):
        raise ValueError('fixed WORD output extent differs')
    if not prefix:
        raw.extend((escape, 0))
    return bytes(raw)


def title_overlay_maps(fields, contract):
    """Two actual 16-row read prefixes, excluding both unread ten-BYTE tails."""
    _fixed(fields, title.metadata(), ('maps',), 'title package')
    rows = []
    for row, bounds, call in zip(fixed_list(fields['maps'], 2, 'title prefixes'), title.LAYOUT, title.CALLERS):
        fixed = title.topology(*bounds, call)
        _fixed(row, fixed, ('fields',), 'title prefix')
        raw = _word_rle(row['fields'], title.OUTPUT_WORDS, prefix=True)
        _add(rows, bounds[0], bounds[1], raw, row['id'], 'candidate_title_WORD_rle_read_prefix')
    return _finish(rows, contract, title.EDITABLE_BYTES)


def battle_overlay_maps(fields, contract):
    """23 full physical 1024-WORD streams plus two editable BE32 catalogs."""
    _fixed(fields, overlay.metadata(), ('directories', 'maps'), 'battle map package')
    rows = []
    catalog = {overlay.ident(start): start for start, _ in overlay.LAYOUT}
    for row, (ident, start) in zip(fixed_list(fields['directories'], 2, 'map directories'), overlay.DIRECTORIES):
        _fixed(row, dict(id=ident, start=start), ('targets',), 'map directory')
        _add(rows, start, start + 20, _pointers(row['targets'], 5, catalog), ident, 'candidate_map_BE32_directory')
    for row, (start, end) in zip(fixed_list(fields['maps'], 23, 'battle maps'), overlay.LAYOUT):
        _fixed(row, overlay.fixed_map(start, end), ('fields',), 'battle map')
        _add(rows, start, end, _word_rle(row['fields'], 1024), row['id'], 'candidate_overlay_WORD_rle')
    return _finish(rows, contract, overlay.EDITABLE_BYTES)


def menu_tile_streams(fields, contract):
    """Three BE32 slots, two rows each, with all original FFFF sentinels."""
    _fixed(fields, menu.metadata(), ('directory', 'streams'), 'menu tiles package')
    catalog = {menu.ident(start): start for start, _ in menu.STREAMS}
    rows = []
    _add(rows, menu.START, menu.DIR_END, _pointers(fields['directory'], 3, catalog),
         'menu_tile_directory', 'candidate_menu_BE32_directory')
    for row, (start, end) in zip(fixed_list(fields['streams'], 3, 'menu streams'), menu.STREAMS):
        _fixed(row, dict(id=menu.ident(start), start=start, end=end, stream_terminator_WORD=65535), ('rows',), 'menu stream')
        raw = bytearray()
        for line in fixed_list(row['rows'], 2, 'menu rows'):
            _fixed(line, dict(row_terminator_WORD=65535), ('command_WORD', 'tile_WORDs'), 'menu row')
            raw.extend(uint(line['command_WORD'], 65534, 'nonterminal command WORD').to_bytes(2, 'big'))
            raw.extend(_words(line['tile_WORDs'], 35, 'full menu tile WORDs', 65534))
            raw.extend(b'\xff\xff')
        raw.extend(b'\xff\xff')
        _add(rows, start, end, bytes(raw), row['id'], 'candidate_menu_full_WORD_rows')
    return _finish(rows, contract, menu.EDITABLE_BYTES)


def _ui_tokens(tokens):
    if type(tokens) is not list:
        raise ValueError('UI fragment list required')
    raw = bytearray()
    for row in tokens:
        if type(row) is not dict:
            raise ValueError('UI fragment object required')
        kind = row.get('kind')
        if kind == 'literal':
            shape.keys(row, {'kind', 'word'}, 'literal fragment')
            raw.extend(uint(row['word'], 65535, 'full fragment WORD').to_bytes(2, 'big'))
        elif kind in ('word_command', 'pointer_command'):
            key, width, maximum = ('operand_word', 2, 65535) if kind == 'word_command' else ('pointer_long', 4, 0xFFFFFFFF)
            shape.keys(row, {'kind', 'control_word', key}, 'command fragment')
            raw.extend(uint(row['control_word'], 65535, 'full command WORD').to_bytes(2, 'big'))
            raw.extend(uint(row[key], maximum, 'full command operand').to_bytes(width, 'big'))
        else:
            raise ValueError('unknown UI packing kind')
    return bytes(raw)


def ui_layouts(fields, contract):
    """Full-width physical fragments; edited kind is not CPU grammar proof."""
    _fixed(fields, dict(schema_version=1, format=layout.FORMAT), ('blocks',), 'UI layout package')
    rows = []
    for row, (ident, start, end, kind, _, _, _) in zip(fixed_list(fields['blocks'], len(layout.REGIONS), 'layout blocks'), layout.REGIONS):
        key = 'tokens' if kind == 'ui_stream' else 'longwords' if kind == 'vdp_longwords' else 'words'
        _fixed(row, dict(id=ident, kind=kind), (key,), 'layout block')
        if kind == 'ui_stream':
            raw = _ui_tokens(row[key])
        elif kind == 'vdp_longwords':
            raw = b''.join(uint(value, 0xFFFFFFFF, 'transfer LONG').to_bytes(4, 'big') for value in fixed_list(row[key], 24, 'transfer LONGs'))
        else:
            raw = _words(row[key], 2, 'glyph descriptor WORDs')
        _add(rows, start, end, raw, ident, 'ui_' + kind)
    return _finish(rows, contract, layout.EDITABLE_BYTES)


def battlefield_resources(fields, contract):
    """Six contiguous full-WORD families; aliases never duplicate authority."""
    _fixed(fields, dict(schema_version=1, format=battlefield.FORMAT),
           [spec[0] for spec in battlefield.FAMILIES], 'battlefield package')
    rows = []
    for family, start, size, groups, _, _ in battlefield.FAMILIES:
        for number, row in enumerate(fixed_list(fields[family], battlefield.COUNT, 'battlefield records'), 1):
            _fixed(row, dict(id=battlefield.record_id(family, number), map_id=number), [item[0] for item in groups], 'battlefield record')
            raw = bytearray()
            for key, dimensions in groups:
                if key == 'leading_word':
                    raw.extend(uint(row[key], 65535, 'leading WORD').to_bytes(2, 'big'))
                elif type(dimensions) is tuple:
                    for line in fixed_list(row[key], dimensions[0], 'candidate groups'):
                        raw.extend(_words(line, dimensions[1], 'candidate group WORDs'))
                else:
                    raw.extend(_words(row[key], dimensions, 'full battlefield WORDs'))
            address = start + (number - 1) * size
            _add(rows, address, address + size, bytes(raw), row['id'], 'battlefield_' + family + '_words')
    return _finish(rows, contract, battlefield.EDITABLE_BYTES)


def ui_fixed_records(fields, contract):
    _fixed(fields, fixed_ui.metadata(), ('groups',), 'fixed UI package')
    rows = []
    for row, spec in zip(fixed_list(fields['groups'], 4, 'fixed UI groups'), fixed_ui.SPECS):
        fixed = fixed_ui.topology(spec)
        _fixed(row, fixed, ('rows',), 'fixed UI group')
        raw = bytearray()
        for record in fixed_list(row['rows'], spec[1], 'three-WORD records'):
            shape.keys(record, {'source_WORD0', 'source_WORD1', 'source_WORD2'}, 'source record')
            raw.extend(_words([record['source_WORD' + str(n)] for n in range(3)], 3, 'full source WORDs'))
        _add(rows, fixed['start'], fixed['end'], bytes(raw), fixed['id'], fixed['kind'])
    return _finish(rows, contract, fixed_ui.EDITABLE_BYTES)


def _sprite_record(row):
    shape.keys(row, {'sat_y_delta', 'sat_x_delta', 'width_tiles', 'height_tiles', 'attribute_nibble', 'tile_low_byte'}, 'four-BYTE source record')
    y = integer(row['sat_y_delta'], -127, 127, 'nonterminal signed Y delta')
    x = integer(row['sat_x_delta'], -128, 127, 'signed X delta')
    width = integer(row['width_tiles'], 1, 4, 'tile width')
    height = integer(row['height_tiles'], 1, 4, 'tile height')
    attribute = uint(row['attribute_nibble'], 15, 'source attribute nibble')
    tile = uint(row['tile_low_byte'], 255, 'source tile BYTE')
    return bytes((y & 255, attribute << 4 | (width - 1) << 2 | height - 1, tile, x & 255))


def _emit_descriptors(fields, contract, rows, role):
    plans = contract['descriptors']
    for row, plan in zip(fixed_list(fields['descriptors'], len(plans), 'sprite descriptors'), plans):
        fixed = plan['fixed']
        _fixed(row, fixed, ('records',), 'sprite descriptor')
        raw = b''.join(_sprite_record(record) for record in fixed_list(row['records'], plan['record_count'], 'sprite records')) + b'\x80'
        _add(rows, fixed['start'], fixed['end'], raw, fixed['id'], role)


def battle_effect_sprites(fields, contract):
    _fixed(fields, effect.metadata(), ('base_selector_BYTES', 'directory_targets', 'attribute_WORDs', 'descriptors'), 'effect sprite package')
    catalog = {plan['fixed']['id']: plan['fixed']['start'] for plan in contract['descriptors']}
    rows = []
    _add(rows, effect.BASES, effect.POINTERS, bytes(uint(value, 255, 'base selector BYTE') for value in fixed_list(fields['base_selector_BYTES'], 8, 'base selector BYTEs')), 'effect_base_selectors', 'effect_selector_BYTEs')
    _add(rows, effect.POINTERS, effect.ATTRIBUTES, _pointers(fields['directory_targets'], 192, catalog), 'effect_directory', 'effect_BE32_directory')
    _add(rows, effect.ATTRIBUTES, effect.DESCRIPTORS, _words(fields['attribute_WORDs'], 192, 'full source attribute WORDs'), 'effect_attributes', 'effect_attribute_WORDs')
    _emit_descriptors(fields, contract, rows, 'candidate_effect_four_BYTE_sources')
    return _finish(rows, contract, effect.EDITABLE_BYTES)


def battle_scene_sprites(fields, contract):
    _fixed(fields, scene.metadata(), ('directories', 'descriptors'), 'scene sprite package')
    rows = []
    for row, spec in zip(fixed_list(fields['directories'], 3, 'scene directories'), scene.DIRECTORIES):
        _fixed(row, scene.directory_topology(spec), ('targets',), 'scene directory')
        catalog = {plan['fixed']['id']: plan['fixed']['start'] for plan in contract['descriptors'] if plan['fixed']['directory_catalog'] == spec[0]}
        _add(rows, spec[1], spec[2], _pointers(row['targets'], (spec[2] - spec[1]) // 4, catalog), row['id'], 'candidate_scene_BE32_directory')
    _emit_descriptors(fields, contract, rows, 'candidate_scene_four_BYTE_sources')
    return _finish(rows, contract, scene.EDITABLE_BYTES)


def _single_sprite_directory(fields, contract, codec, count, catalog_starts=None):
    _fixed(fields, codec.metadata(), ('directory', 'descriptors'), 'single-directory sprite package')
    directory = fields['directory']
    _fixed(directory, codec.directory_topology(), ('targets',), 'sprite directory')
    catalog = {plan['fixed']['id']: plan['fixed']['start'] for plan in contract['descriptors']
               if catalog_starts is None or plan['fixed']['start'] in catalog_starts}
    rows = []
    _add(rows, codec.DIR_START, codec.DIR_END, _pointers(directory['targets'], count, catalog), directory['id'], 'candidate_sprite_BE32_directory')
    _emit_descriptors(fields, contract, rows, 'candidate_first80_four_BYTE_sources')
    return _finish(rows, contract, codec.EDITABLE_BYTES)


def battle_command_sprites(fields, contract):
    return _single_sprite_directory(fields, contract, command, 8)


def battle_marker_sprites(fields, contract):
    return _single_sprite_directory(fields, contract, marker, 4, marker.INDEXED_TARGETS)


def _descriptor_plan(resource_id, fields):
    """Persist typed noneditable catalog geometry, never original record bytes."""
    count, records, source_bytes = {'battle_scene_sprites': (36, 627, 2544),
                                  'battle_effect_sprites': (128, 144, 704),
                                  'battle_command_sprites': (8, 109, 444),
                                  'battle_marker_sprites': (7, 25, 107)}[resource_id]
    plans = []
    for row in fixed_list(fields['descriptors'], count, 'canonical descriptor catalog'):
        if type(row) is not dict or type(row.get('records')) is not list:
            raise ValueError('typed descriptor records required')
        n = len(row['records'])
        if not 1 <= n <= 80:
            raise ValueError('existing complete first80 record count differs')
        fixed = {key: value for key, value in row.items() if key != 'records'}
        start = uint(fixed['start'], 0xFFFFF, 'descriptor start')
        if fixed['end'] != start + 4 * n + 1:
            raise ValueError('first80 descriptor extent differs')
        plans.append(dict(fixed=fixed, record_count=n))
    if (sum(plan['record_count'] for plan in plans) != records or
            sum(plan['fixed']['end'] - plan['fixed']['start'] for plan in plans) != source_bytes or
            len({plan['fixed']['id'] for plan in plans}) != count):
        raise ValueError('complete descriptor partition differs')
    if resource_id == 'battle_effect_sprites':
        starts = [plan['fixed']['start'] for plan in plans]
        if starts != sorted(set(starts)) or starts[0] != effect.DESCRIPTORS or starts[-1] != 0x40C8A:
            raise ValueError('effect physical catalog differs')
        for plan, limit in zip(plans, starts[1:] + [effect.END]):
            fixed = plan['fixed']
            shape.keys(fixed, {'id', 'start', 'end', 'unread_interval', 'count'}, 'effect topology')
            expected = dict(id=effect.ident(fixed['start']), start=fixed['start'], end=fixed['end'], unread_interval=[fixed['end'], limit], count=plan['record_count'])
            shape.same(fixed, expected, 'effect first-terminal topology')
            if fixed['end'] > limit:
                raise ValueError('effect first-terminal topology differs')
    elif resource_id == 'battle_scene_sprites':
        for spec in scene.DIRECTORIES:
            members = [plan for plan in plans if plan['fixed']['directory_catalog'] == spec[0]]
            starts = [plan['fixed']['start'] for plan in members]
            if len(starts) != (spec[2] - spec[1]) // 4 or starts != sorted(set(starts)) or starts[0] != spec[2]:
                raise ValueError('scene physical catalog differs')
            for plan, limit in zip(members, starts[1:] + [spec[3]]):
                fixed = plan['fixed']
                expected = scene.descriptor_topology(dict(directory=spec[0], start=fixed['start'], end=fixed['end'], allocation_end=limit))
                shape.same(fixed, expected, 'scene first-terminal topology')
                if fixed['end'] > limit:
                    raise ValueError('scene descriptor crosses allocation')
    else:
        codec = command if resource_id == 'battle_command_sprites' else marker
        specs = [(start, limit, n) for start, limit, n in marker.SOURCES] if codec is marker else list(zip(command.ORIGINAL_TARGETS, command.ORIGINAL_TARGETS[1:] + (command.ALLOCATION_END,), command.ORIGINAL_COUNTS))
        for plan, (start, limit, n) in zip(plans, specs):
            shape.same(plan['fixed'], codec.descriptor_topology(dict(start=start, end=start + 4 * n + 1, allocation_end=limit)), 'fixed first-terminal topology')
            if plan['record_count'] != n:
                raise ValueError('fixed sprite record count differs')
    return plans


ENCODERS = {name: globals()[name] for name in (
    'title_overlay_maps', 'battle_overlay_maps', 'menu_tile_streams', 'ui_layouts',
    'battlefield_resources', 'ui_fixed_records', 'battle_effect_sprites',
    'battle_scene_sprites', 'battle_command_sprites', 'battle_marker_sprites')}


def geometry_contract(resource_id, canonical_fields):
    """Offline typed topology projection; persist this before editable encode."""
    if type(resource_id) is not str or resource_id not in ENCODERS:
        raise ValueError('explicit independently owned UI resource ID required')
    contract = dict(adapter=resource_id, adapter_module=__name__, format=canonical_fields['format'],
                    confidence='preserved_original_resource_classification',
                    semantic_meaning='confirmed_encoding_not_natural_behavior',
                    limits=['fixed physical editor catalogs are not natural CPU selector bounds',
                            'pure serialization is not edited CPU/SAT/VDP timing or natural-path validation',
                            'original full-width values, aliases and unknown gaps are not normalized'])
    if resource_id.startswith('battle_') and resource_id.endswith('_sprites'):
        contract['descriptors'] = _descriptor_plan(resource_id, canonical_fields)
        contract['limits'].append('only first80 terminal BYTE emitted; unread record stride/tail remains unknown')
    if resource_id == 'title_overlay_maps':
        contract['limits'].append('row-limit prefix without invented terminator; last repeat count retained; two unread ten-BYTE tails excluded')
    if resource_id == 'battle_overlay_maps':
        contract['limits'].append('complete physical 1024-WORD allocation differs from conditional 10/18/32-row source consumption; final473E3 BYTE excluded')
    if resource_id == 'ui_layouts':
        contract['limits'].append('156B candidate panel retained; packing kind does not constrain edited control dispatch; zero counts still wrap in original CPU')
    if resource_id == 'battlefield_resources':
        contract['limits'].append('biased/pre-record/point-zero and cross-family aliases share single physical authority; old AE1C2..AE1CA eight-BYTE author must be recorded as alias')
    if resource_id == 'ui_fixed_records':
        contract['limits'].append('only20 fill rows read; B6E2..B724 unknown66-BYTE tail excluded')
    rows = ENCODERS[resource_id](canonical_fields, contract)
    contract.update(spans=coalesced_spans(rows), bytes=sum(len(row['data']) for row in rows), physical_blocks=len(rows))
    return contract
