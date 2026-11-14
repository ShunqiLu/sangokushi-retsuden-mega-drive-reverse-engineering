"""ROM-independent typed resource encoders.

These functions accept editable JSON, never a ROM image or an opcode blob.
They preserve the recorded physical format. Encoding is not CPU execution,
natural-path proof, or a claim that an allocation is free space. Legacy pure
token serializers are reused where stated; their ROM验收 entry points are not.
"""
from __future__ import annotations

import struct

ROM_SIZE = 0x100000


def uint(value, maximum, label='integer'):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError(label + ': strict unsigned integer outside width')
    return value


def integer(value, minimum, maximum, label='integer'):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(label + ': strict integer outside width')
    return value


def fixed_list(value, count, label):
    if type(value) is not list or len(value) != count:
        raise ValueError(label + ': fixed list shape differs')
    return value


def block(start, raw, ident, role):
    uint(start, ROM_SIZE - 1, 'resource address')
    if type(raw) is not bytes or not raw or start + len(raw) > ROM_SIZE:
        raise ValueError('nonempty bounded resource bytes required')
    return dict(id=ident, start=start, end=start + len(raw), data=raw, role=role)


def coalesced_spans(rows):
    result = []
    for row in sorted(rows, key=lambda item: (item['start'], item['end'])):
        start, end = row['start'], row['end']
        if result and start < result[-1][1]:
            raise ValueError('resource authorities overlap')
        if result and start == result[-1][1]:
            result[-1][1] = end
        else:
            result.append([start, end])
    return result


def sparse_byte_fields(fields, contract):
    """Encode explicitly named source BYTE fields; leave source roles unknown.

    Witnesses and physical scope are evidence, not duplicate editable bytes.
    This adapter does not execute the source readers or discover new owners.
    """
    mode = contract['mode']
    values = {}
    def put(address, value):
        uint(address, ROM_SIZE - 1, 'source BYTE address')
        if address in values:
            raise ValueError('duplicate physical source BYTE authority')
        values[address] = uint(value, 255, 'complete source BYTE')
    if mode == 'addressed_bytes':
        for row in fields[contract['collection']]:
            put(row[contract.get('address_key', 'address')], row['BYTE'])
    elif mode == 'source_arrays':
        for row in fields[contract['collection']]:
            data = row[contract['value_key']]
            start, end = row['start'], row['end']
            fixed_list(data, end - start, 'source BYTE array')
            for address, value in enumerate(data, start): put(address, value)
    elif mode == 'contiguous_bytes':
        start, end = contract['spans'][0]
        for address, value in enumerate(fixed_list(fields[contract['collection']], end-start,
                                                 'source BYTE array'), start):
            put(address, value)
    else:
        raise ValueError('unimplemented source BYTE representation')
    expected = {address for start, end in contract['spans'] for address in range(start, end)}
    if set(values) != expected:
        raise ValueError('fixed independent source BYTE geometry differs')
    return [block(start, bytes(values[address] for address in range(start, end)),
                  'source_' + format(start, '06x'), 'conditional_source_BYTE_fields')
            for start, end in contract['spans']]


def header_vector_fields(fields, contract):
    """All 64 vectors and header literal fields; no automatic checksum repair."""
    vectors = bytearray()
    for index, item in enumerate(fixed_list(fields['vectors'], 64, 'CPU vectors')):
        if item['index'] != index or item['address'] != 4 * index:
            raise ValueError('fixed CPU vector position differs')
        vectors.extend(uint(item['LONG'], 0xFFFFFFFF, 'vector LONG').to_bytes(4, 'big'))
    header = bytearray(256)
    covered = set()
    def place(address, raw):
        positions = set(range(address, address + len(raw)))
        if not positions <= set(range(0x100, 0x200)) or positions & covered:
            raise ValueError('cartridge header field extent/overlap differs')
        covered.update(positions)
        header[address-0x100:address-0x100+len(raw)] = raw
    for collection, value_key in (('header_literals', 'BYTEs'), ('header_numbers', 'value')):
        declarations = contract[collection]
        for item, declaration in zip(fixed_list(fields[collection], len(declarations), collection), declarations):
            for key, value in declaration.items():
                if type(item.get(key)) is not type(value) or item[key] != value:
                    raise ValueError('fixed header declaration differs: ' + key)
            width = item['fixed_BYTES'] if collection == 'header_literals' else item['width_BYTES']
            if collection == 'header_literals':
                raw = bytes(uint(value, 255, 'literal BYTE')
                            for value in fixed_list(item[value_key], width, 'literal width'))
            else:
                raw = uint(item[value_key], (1 << (8 * width)) - 1, 'literal number').to_bytes(width, 'big')
            place(item['address'], raw)
    if covered != set(range(0x100, 0x200)):
        raise ValueError('complete structured cartridge header required')
    return [block(0, bytes(vectors), 'CPU_vectors', 'confirmed_CPU_vector_full_BE32_fields'),
            block(0x100, bytes(header), 'cartridge_header', 'confirmed_fixed_header_literal_fields')]


def fm_record(record):
    """25-byte YM2612 register order, preserving every register bit."""
    fields = ('detune_multiple', 'rate_scale_attack', 'amplitude_decay', 'sustain_rate', 'sustain_release')
    raw = bytearray(25)
    raw[0] = uint(record['feedback_algorithm'], 255, 'feedback/algorithm')
    for column, operator in enumerate(fixed_list(record['operators'], 4, 'FM operators')):
        if operator['register_offset'] != (0, 8, 4, 12)[column]:
            raise ValueError('fixed FM register column differs')
        for row, field in enumerate(fields):
            raw[1 + 4 * row + column] = uint(operator[field], 255, field)
        flag = operator['channel_attenuation_enabled']
        if type(flag) is not bool: raise ValueError('FM attenuation flag must be Boolean')
        raw[21 + column] = uint(operator['total_level'], 127, 'total level') | (0x80 if flag else 0)
    return bytes(raw)


def envelope_token(family, token):
    """Original linear envelope grammar, not selector/cursor execution."""
    kind = token['kind']
    singles = {'reset': 0x80, 'hold_81': 0x81,
               'hold_83' if family == 'pitch' else 'keyoff_83': 0x83}
    if kind in singles: return bytes([singles[kind]])
    if kind == ('delta' if family == 'pitch' else 'value'):
        return bytes([integer(token['value'], -123 if family == 'pitch' else 0, 127, 'envelope value') & 255])
    if family == 'pitch' and kind in ('jump', 'add_scale'):
        key, opcode = ('cursor', 0x82) if kind == 'jump' else ('increment', 0x84)
        return bytes([opcode, uint(token[key], 255, key)])
    if family == 'attenuation' and kind == 'redirect':
        opcode = integer(token['opcode'], 128, 255, 'redirect opcode')
        if opcode in (0x80, 0x81, 0x83): raise ValueError('special envelope control cannot be redirect')
        return bytes([opcode, uint(token['cursor'], 255, 'redirect cursor')])
    raise ValueError('token kind outside declared envelope family')


def sequence_event(event):
    """Serialize a declared stateful event without reading neighbouring ROM."""
    kind = event['type']
    raw = []
    if kind == 'command':
        raw = [uint(event['opcode'], 255, 'command opcode')]
        if 'subcommand' in event: raw.append(uint(event['subcommand'], 255, 'subcommand'))
        raw += [uint(value, 255, 'command operand') for value in event['arguments']]
    elif kind == 'duration':
        raw = [uint(event['duration'], 127, 'standalone duration')]
    else:
        if kind == 'raw_frequency':
            frequency = uint(event['frequency'], 0xDFFF, 'raw frequency')
            raw = [frequency >> 8, frequency & 255]
        elif kind in ('rhythm', 'note'):
            raw = [integer(event['mask' if kind == 'rhythm' else 'note'], 0x80, 0xDF, 'note/rhythm')]
        else:
            raise ValueError('unknown declared sequence event type')
        if event.get('detune') is not None: raw.append(uint(event['detune'], 255, 'detune'))
        if event['duration'] is not None:
            maximum = 255 if kind == 'raw_frequency' or event.get('detune') is not None else 127
            raw.append(uint(event['duration'], maximum, 'duration'))
    if len(raw) != uint(event['size'], 255, 'event size'):
        raise ValueError('declared sequence event encoding width differs')
    return bytes(raw)


def audio_build(fields, contract):
    """Independent music/SFX, instruments, envelopes, events and rhythm bytes.

    The old whole-ROM alias/lookahead/reachability validators are intentionally
    not called. Their missing proof is an explicit registry limit, not a pass.
    Fixed physical scope and per-definition/token framing remain enforced.
    """
    rows = []
    def add(start, raw, ident, role): rows.append(block(start, raw, ident, role))
    definitions = fields['definitions']
    for key in ('music_pointer_table', 'sfx_pointer_table'):
        table = definitions[key]
        raw = b''.join(uint(pointer, 65535, 'audio pointer').to_bytes(2, 'little') for pointer in table['pointers'])
        add(table['rom_offset'], raw, key, 'audio_pointer_LE16')
    for group in ('music', 'sfx'):
        for definition in definitions[group]:
            header = definition['header']
            base = uint(header['instrument_base'], 65535, 'instrument base')
            multiplier = uint(header['duration_multiplier'], 255, 'duration multiplier')
            if group == 'music':
                driver_count = uint(header['driver_slot_count'], 255, 'driver slots')
                psg_count = uint(header['psg_slot_count'], 255, 'PSG slots')
                fixed_list(definition['ordinary_slots'], driver_count, 'ordinary slots')
                fixed_list(definition['psg_slots'], psg_count, 'PSG slots')
                raw = bytearray(struct.pack('<H4B', base, driver_count, psg_count, multiplier,
                                            uint(header['tempo_reload'], 255, 'tempo reload')))
                collections = ('ordinary_slots', 'psg_slots')
            else:
                count = uint(header['channel_count'], 255, 'SFX channels')
                fixed_list(definition['slots'], count, 'SFX slots')
                raw = bytearray(struct.pack('<H2B', base, multiplier, count))
                collections = ('slots',)
            for collection in collections:
                for slot in definition[collection]:
                    pointer = uint(slot['sequence_ptr'], 65535, 'sequence pointer')
                    minimum, maximum = (0x827D, 0xE31D) if definition['space'] == 'banked' else (0x1022, 0x16ED)
                    if not minimum <= pointer < maximum:
                        raise ValueError('edited sequence reference outside source format allocation')
                    transpose, attenuation = (uint(slot[key], 255, key) for key in ('transpose', 'attenuation'))
                    if collection == 'slots':
                        raw.extend(struct.pack('<BBHBB', uint(slot['flags'], 255, 'flags'),
                                               uint(slot['channel_id'], 255, 'channel ID'), pointer, transpose, attenuation))
                    elif collection == 'ordinary_slots':
                        raw.extend(struct.pack('<H2B', pointer, transpose, attenuation))
                    else:
                        raw.extend(struct.pack('<H4B', pointer, transpose, attenuation,
                                               uint(slot['modulation_selector'], 255, 'modulation selector'),
                                               uint(slot['envelope_selector'], 255, 'envelope selector')))
            add(definition['rom_offset'], bytes(raw), definition['id'], 'audio_' + group + '_definition')
    for bank in definitions['instrument_banks']:
        for index, record in enumerate(fixed_list(bank['records'], bank['record_count'], 'FM record count')):
            if record['index'] != index: raise ValueError('FM index/order differs')
            add(bank['rom_offset'] + index * 25, fm_record(record), bank['id'] + '_' + str(index), 'audio_FM_registers')
    for table in fields['envelopes']['tables']:
        family = table['family']
        if family not in ('pitch', 'attenuation'): raise ValueError('unknown envelope family')
        pointer_start = table['z80_pointer_start']
        pointer_raw = b''.join(uint(value, 65535, 'envelope pointer').to_bytes(2, 'little') for value in table['pointers'])
        add(0xF8000 + pointer_start - 0x8000, pointer_raw, family + '_pointers', 'audio_envelope_LE16_pointers')
        starts = table['pointers']
        for index, allocation in enumerate(fixed_list(table['allocations'], len(starts), 'envelope allocations')):
            start = allocation['z80_start']
            if start != starts[index]: raise ValueError('envelope allocation pointer differs')
            end = starts[index + 1] if index + 1 < len(starts) else table['z80_allocation_end']
            raw = b''.join(envelope_token(family, token) for token in allocation['tokens'])
            if len(raw) != end - start: raise ValueError('envelope token framing differs')
            add(0xF8000 + start - 0x8000, raw, family + '_' + format(start, '04x'), 'audio_envelope_tokens')
    for view in fields['sequences']['views']:
        address = view['address']
        if address >= 0x8000:
            physical = 0xF0000 + address
        elif address < 0x1000:
            physical = 0x69D2 + address
        elif address < 0x1C00:
            physical = 0x699C + address
        else:
            raise ValueError('sequence address is unbacked runtime RAM')
        if view['rom_offset'] != physical: raise ValueError('sequence logical/physical mapping differs')
        add(physical, sequence_event(view['event']), view['id'], 'audio_declared_stateful_sequence_event')
    rhythm = fields['sequences']['rhythm']
    for table in rhythm['pointer_tables']:
        add(table['rom_offset'], b''.join(uint(p, 65535, 'rhythm pointer').to_bytes(2, 'little')
                                          for p in table['pointers']), table['id'], 'audio_rhythm_LE16_pointers')
    for header in rhythm['channel_headers']:
        add(header['rom_offset'], bytes(uint(header[key], 255, key) for key in
                                        ('flags', 'channel_id', 'duration_multiplier')),
            'rhythm_' + header['family'] + '_header', 'audio_rhythm_channel_header')
    for descriptor in rhythm['descriptors']:
        values = descriptor['fields']
        selector = 'voice_index' if descriptor['family'] == 'fm' else 'envelope_selector'
        raw = struct.pack('<H4B', uint(values['sequence_ptr'], 65535, 'rhythm sequence pointer'),
                          uint(values['transpose'], 255, 'transpose'), uint(values['attenuation'], 255, 'attenuation'),
                          uint(values['modulation_selector'], 255, 'modulation selector'),
                          uint(values[selector], 5 if selector == 'voice_index' else 255, selector))
        add(descriptor['rom_offset'], raw, descriptor['id'], 'audio_rhythm_descriptor')
    for voice in rhythm['voice_records']:
        add(voice['rom_offset'], fm_record(voice['fields']), voice['id'], 'audio_rhythm_FM_voice')
    coalesced_spans(rows)
    if any(row['start'] // 65536 not in (0, 15) or
           row['start'] // 65536 != (row['end'] - 1) // 65536 for row in rows):
        raise ValueError('audio source block outside its fixed bank')
    return rows


def font_build(fields, contract):
    rows = []
    for value, declaration in zip(fixed_list(fields['fonts'], len(contract['fonts']), 'fonts'), contract['fonts']):
        for key in ('id', 'start', 'end', 'width', 'height'):
            if value[key] != declaration[key]: raise ValueError('fixed font geometry differs')
        size = value['width'] // 8
        stride = size * value['height']
        count = (value['end'] - value['start']) // stride
        for index, glyph in enumerate(fixed_list(value['glyphs'], count, 'font glyphs')):
            if glyph['id'] != value['id'] + '_' + format(index, '04d'): raise ValueError('glyph order differs')
            raw = b''.join(uint(word, (1 << value['width']) - 1, 'font row').to_bytes(size, 'big')
                           for word in fixed_list(glyph['rows'], value['height'], 'glyph rows'))
            rows.append(block(value['start'] + index * stride, raw, glyph['id'], value['id'] + '_1bpp_rows'))
    return rows


def graphics_build(fields, contract):
    """Reuse only the old pure field serializer, never its ROM blocks/validator."""
    from tools.graphics_build import graphics_build as codec
    rows = []
    for asset, value in zip(codec.ASSETS, fixed_list(fields['assets'], len(codec.ASSETS), 'graphics assets')):
        if {key: value[key] for key in codec.metadata(asset)} != codec.metadata(asset):
            raise ValueError('fixed graphics geometry differs')
        raw, _ = codec.pack_fields(asset, value['fields'])
        rows.append(block(asset.start, raw, asset.name, codec.kind(asset)))
    return rows


def portrait_graphics(fields, contract):
    """Physical tile/layout/palette encoder; original token arithmetic retained."""
    from tools.portrait_graphics import portrait_graphics as codec
    rows = []
    allowed_tiles = set(contract['tile_starts'])
    allowed_palettes = set(contract['palette_selectors'])
    for index, image in enumerate(fixed_list(fields['images'], 256, 'portrait layouts')):
        if image['id'] != 'image_' + format(index, '03d'): raise ValueError('portrait identity differs')
        for kind, base, count in codec.TABLES:
            tokens = fixed_list(image[kind], count, kind)
            for token in tokens:
                addresses = codec.token_reads(token, kind)
                if addresses[0] not in allowed_tiles or addresses != list(range(addresses[0], addresses[0]+32, 4)):
                    raise ValueError('portrait token leaves retained physical allocation')
            rows.append(block(base + index * count * 2, b''.join(token.to_bytes(2, 'big') for token in tokens),
                              'portrait_' + kind + '_' + str(index), 'portrait_tile_tokens_' + kind))
        selector = uint(image['palette_selector'], 255, 'palette selector')
        if selector not in allowed_palettes: raise ValueError('portrait palette reference differs')
        rows.append(block(codec.SELECTORS + index, bytes([selector]), 'portrait_selector_' + str(index), 'portrait_palette_selector'))
    for tile, start in zip(fixed_list(fields['tiles'], len(contract['tile_starts']), 'physical portrait tiles'),
                           contract['tile_starts']):
        if tile['start'] != start: raise ValueError('physical portrait tile order differs')
        lines = fixed_list(tile['rows'], 8, '4bpp tile rows')
        if any(type(line) is not str or len(line) != 8 or any(ch not in '0123456789ABCDEF' for ch in line)
               for line in lines): raise ValueError('tile row must be eight uppercase pixel nibbles')
        rows.append(block(start, bytes.fromhex(''.join(lines)), tile['id'], 'portrait_4bpp_tile'))
    for palette, selector in zip(fixed_list(fields['palettes'], len(contract['palette_selectors']), 'palettes'),
                                 contract['palette_selectors']):
        if palette['selector'] != selector: raise ValueError('palette order differs')
        raw = b''.join(codec.colour_word(colour).to_bytes(2, 'big') for colour in fixed_list(palette['colours'], 16, 'CRAM colours'))
        rows.append(block(codec.PALETTE_BIAS + selector * 32, raw, 'portrait_palette_' + str(selector), 'portrait_CRAM_RGB3_reserved'))
    return rows


def indexed_lowbank_source_alias_fields(fields, contract):
    """Use the explicit v2 1162B declaration, not a filtered legacy input.

    The dedicated encoder rejects old-format documents and resource payload
    attached to the 8B audio-code references. There is no runtime clipping.
    """
    from .indexed_lowbank_source_alias_fields import encode
    return [dict(id='source_' + format(row.start, '06x'), start=row.start,
                 end=row.end, data=row.data, owner=row.owner, role=row.role)
            for row in encode(fields)]


def scalar_sources(fields, contract):
    """Fixed primitive arrays, retaining full operand bits and source labels."""
    rows = []
    for source in fields[contract['collection']]:
        width = source.get('width_BYTES', source.get('element_BYTES', source.get('element_bytes')))
        if width not in (1, 2, 4, 6): raise ValueError('unsupported scalar source width')
        order = 'little' if source.get('encoding') == 'LE16' else 'big'
        if width == 6:
            raw = b''.join(uint(value['pointer_LONG'], 0xFFFFFFFF, 'source pointer LONG').to_bytes(4, 'big') +
                           uint(value['counter_WORD'], 65535, 'source counter WORD').to_bytes(2, 'big')
                           for value in source['records'])
        elif source.get('kind') == 'XY_BYTES':
            raw = bytes(uint(value[key], 255, key) for value in source['values'] for key in ('X_BYTE', 'Y_BYTE'))
        else:
            raw = b''.join(uint(value, (1 << (8 * width))-1, 'complete scalar operand').to_bytes(width, order)
                           for value in source['values'])
        if source.get('kind') == 'BYTE_CYCLE_RESET' and source['values'][-1] != 255:
            raise ValueError('fixed last FF reset framing marker differs')
        if source['end'] - source['start'] != len(raw): raise ValueError('scalar source width differs')
        rows.append(block(source['start'], raw, source['id'], 'conditional_scalar_source_fields'))
    return rows
