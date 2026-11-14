"""Independent encoders for fixed scene/display resources.

Only supplied typed fields and persisted editor geometry generate bytes. No
ROM, old bank, compiled blob, source-reader execution or legacy whole-image
validator is used. Pure color/pixel/RLE helpers are disclosed dependencies.
Unknown animation tails, palette slots and font-read gaps are not emitted;
full frame/reset operands and counted procedural font WORDs remain intact.
"""
from __future__ import annotations

from tools.resource_metadata import compare_fixed_fields

from tools.vdp_word_streams import format as fmt
from tools.graphics_build import rle_fields as rle
from tools.graphics_build import graphics_build as graphics
from tools.scene_tile_resources import codec as scene_tiles
from tools.scene_sprite_resources import codec as scene_sprites
from tools.display_tile_resources import codec as display_tiles
from tools.bank08_display_resources import codec as bank08
from tools.bank06_display_tail import codec as bank06
from .resource_adapters import block, coalesced_spans, fixed_list, uint


def _fixed(row, fixed, editable, label):
    compare_fixed_fields(row, fixed, editable, label)


def _package(fields, codec, editable):
    _fixed(fields, codec.metadata(), editable, 'scene/display package')


def _add(rows, start, end, data, ident, role):
    if type(data) is not bytes or len(data) != end - start:
        raise ValueError('complete fixed source cost differs')
    rows.append(block(start, data, ident, role))


def _finish(rows, contract, expected):
    rows.sort(key=lambda row: row['start'])
    spans = coalesced_spans(rows)
    if sum(len(row['data']) for row in rows) != expected:
        raise ValueError('declared resource physical byte count differs')
    if 'spans' in contract and spans != contract['spans']:
        raise ValueError('persisted independent source geometry differs')
    return rows


def _pixel_tiles(tiles, start, count, ident):
    raw = bytearray()
    for tile, address in zip(fixed_list(tiles, count, 'physical tile slots'), range(start, start + count * 32, 32)):
        _fixed(tile, dict(id=ident(address)), {'pixels'}, '4bpp tile')
        raw.extend(bank08.tile_bytes(tile['pixels']))
    return bytes(raw)


def scene_tile_resources(fields, contract):
    """One palette, two 256-tile banks, six scene-specific BE WORD-RLE maps."""
    c, rows = scene_tiles, []
    _package(fields, c, {'palette', 'tile_banks', 'maps'})
    start, end = c.PALETTE
    palette = fields['palette']
    _fixed(palette, c.topology(start, end, 'palette'), {'colours'}, 'scene palette')
    raw = b''.join(c.colour_word(colour).to_bytes(2, 'big')
                   for colour in fixed_list(palette['colours'], 64, 'CRAM colours'))
    _add(rows, start, end, raw, c.ident(start, 'palette'), 'candidate_scene_CRAM_RGB3_reserved')
    for bank, (start, end) in zip(fixed_list(fields['tile_banks'], 2, 'scene tile banks'), c.TILES):
        _fixed(bank, c.topology(start, end, 'tiles'), {'tiles'}, 'scene tile bank')
        raw = _pixel_tiles(bank['tiles'], start, 256, lambda address: c.ident(address, 'tile'))
        _add(rows, start, end, raw, bank['id'], 'candidate_scene_VDP_4bpp_tiles')
    for row, (start, end) in zip(fixed_list(fields['maps'], 6, 'scene map streams'), c.MAPS):
        _fixed(row, dict(c.topology(start, end, 'map'), decoded_words=1024), {'fields'}, 'scene map')
        fmt.strict_commands(row['fields'])
        encoded, _ = rle.pack_word(row['fields'], 'big', 1024)
        if len(encoded) != end-start or rle.parse_word(encoded, 'big', 1024) != row['fields']:
            raise ValueError('scene map source cost/control representation differs')
        _add(rows, start, end, encoded, row['id'], 'candidate_scene_big_WORD_RLE_map')
    return _finish(rows, contract, c.EDITABLE_BYTES)


def scene_sprite_resources(fields, contract):
    """Scene animation resets stay full BYTE, including original reset42."""
    c, rows = scene_sprites, []
    _package(fields, c, {'palettes', 'palette_directory', 'animation_directory',
                         'animations', 'parameters', 'WORD_row'})
    for row, start in zip(fixed_list(fields['palettes'], 60, 'scene palettes'), c.PAL_STARTS):
        _fixed(row, dict(id=c.ident(start, 'palette'), start=start), {'colours'}, 'palette')
        raw = b''.join(c.colour_word(colour).to_bytes(2, 'big')
                       for colour in fixed_list(row['colours'], 16, 'palette WORDs'))
        _add(rows, start, start+32, raw, row['id'], 'candidate_scene_palette_staging_WORDs')
    for name, start, catalog in (
            ('palette_directory', 0x388FA, {c.ident(p, 'palette'): p for p in c.PAL_STARTS}),
            ('animation_directory', 0x38A12, {c.ident(p, 'animation'): p for p in c.ANIM_STARTS})):
        targets = fixed_list(fields[name], 40, name)
        if any(type(target) is not str or target not in catalog for target in targets):
            raise ValueError('scene pointer outside fixed physical catalog')
        raw = b''.join(catalog[target].to_bytes(4, 'big') for target in targets)
        _add(rows, start, start+160, raw, name, 'candidate_scene_pointer_directory')
    geometry = fixed_list(contract['animations'], 10, 'fixed first-control animation geometry')
    for row, fixed in zip(fixed_list(fields['animations'], 10, 'animations'), geometry):
        _fixed(row, {key: fixed[key] for key in ('id', 'start', 'end')},
               {'frames', 'negative_control', 'reset_byte'}, 'animation')
        frames = bytes(uint(value, 127, 'signed-positive frame BYTE')
                       for value in fixed_list(row['frames'], fixed['frame_count'], 'frame slots'))
        control = uint(row['negative_control'], 255, 'negative animation control')
        if control < 128: raise ValueError('signed-negative animation control required')
        raw = frames + bytes([control, uint(row['reset_byte'], 255, 'unclamped reset BYTE')])
        _add(rows, fixed['start'], fixed['end'], raw, row['id'], 'candidate_signed_frame_reset_stream')
    fmt.keys(fields['parameters'], {name for name, _, _ in c.PARAMS}, 'scene parameters')
    for name, start, width in c.PARAMS:
        values = fixed_list(fields['parameters'][name], 40, name)
        raw = (bytes(c.motion_byte(value) for value in values) if name == 'motion_controls' else
               b''.join(uint(value, (1 << (8*width))-1, name).to_bytes(width, 'big') for value in values))
        _add(rows, start, start+40*width, raw, name, 'candidate_scene_' + name)
    raw = b''.join(graphics.cell_word(cell).to_bytes(2, 'big')
                   for cell in fixed_list(fields['WORD_row'], 32, 'single uploaded WORD row'))
    _add(rows, 0x5CDE2, 0x5CE22, raw, 'scene_single_WORD_row', 'candidate_single_uploaded_WORD_row')
    return _finish(rows, contract, c.EDITABLE_BYTES)


def display_tile_resources(fields, contract):
    c, rows = display_tiles, []
    _package(fields, c, {'banks'})
    for bank, (start, end, count) in zip(fixed_list(fields['banks'], 2, 'display tile banks'), c.SPANS):
        _fixed(bank, dict(id=c.ident(start), start=start, end=end), {'tiles'}, 'display tile bank')
        raw = _pixel_tiles(bank['tiles'], start, count, c.ident)
        _add(rows, start, end, raw, bank['id'], 'candidate_direct_uploaded_4bpp_tiles')
    return _finish(rows, contract, c.EDITABLE_BYTES)


def _counted_display(fields, contract, codec, byte_group):
    rows = []
    mutable = {'tile_uploads', 'font_WORD_sources'} | ({'font_BYTE_source'} if byte_group else set())
    _package(fields, codec, mutable)
    for row, spec in zip(fixed_list(fields['tile_uploads'], len(codec.TILES), 'tile uploads'), codec.TILES):
        fixed = codec.tile_topology(spec)
        _fixed(row, fixed, {'tiles'}, 'tile upload')
        raw = _pixel_tiles(row['tiles'], spec[0], fixed['physical_tiles'], lambda p: codec.ident(p, 'tile'))
        _add(rows, spec[0], spec[1], raw, row['id'], 'candidate_fixed_VDP_4bpp_tile_upload')
    for row, (start, end) in zip(fixed_list(fields['font_WORD_sources'], len(codec.WORD_GROUPS),
                                          'counted font WORD groups'), codec.WORD_GROUPS):
        _fixed(row, codec.word_topology(start, end), {'cells'}, 'counted font WORD group')
        # AE8A negative WORDs select procedural cells, not terminators. The
        # original helper preserves their full16 bits and positive aliases.
        raw = b''.join(codec.glyph_word(cell).to_bytes(2, 'big')
                       for cell in fixed_list(row['cells'], (end-start)//2, 'counted font cells'))
        _add(rows, start, end, raw, row['id'], 'candidate_counted_font16_source_WORDs')
    if byte_group:
        row = fields['font_BYTE_source']
        start, end = codec.BYTE_GROUP
        _fixed(row, codec.byte_topology(), {'glyph_indices'}, 'counted font BYTE group')
        raw = bytes(uint(value, 255, 'font8 glyph index BYTE')
                    for value in fixed_list(row['glyph_indices'], end-start, 'font8 source BYTEs'))
        _add(rows, start, end, raw, row['id'], 'candidate_counted_font8_source_BYTEs')
    return _finish(rows, contract, codec.EDITABLE_BYTES)


def bank08_display_resources(fields, contract):
    return _counted_display(fields, contract, bank08, True)


def bank06_display_tail(fields, contract):
    return _counted_display(fields, contract, bank06, False)


ENCODERS = {
    'scene_tile_resources': scene_tile_resources,
    'scene_sprite_resources': scene_sprite_resources,
    'display_tile_resources': display_tile_resources,
    'bank08_display_resources': bank08_display_resources,
    'bank06_display_tail': bank06_display_tail,
}


def geometry_contract(resource_id, canonical_fields):
    """Explicit one-time typed-source geometry; no runtime capacity recalc."""
    if resource_id not in ENCODERS:
        raise ValueError('one registered scene/display family required')
    contract = dict(adapter=resource_id, adapter_module=__name__, format=canonical_fields['format'],
        confidence=canonical_fields['confidence'], semantic_meaning='preserved_source_classification_not_promoted',
        limits=['fixed source allocations are not natural CPU selector bounds',
                'pure field encoding does not execute VDP/CPU/IRQ or prove natural gameplay',
                'old pure color/pixel/RLE helpers remain disclosed delivery dependencies'])
    if resource_id == 'scene_sprite_resources':
        contract['animations'] = []
        for value, start, allocation_end in zip(fixed_list(canonical_fields['animations'], 10, 'animations'),
                scene_sprites.ANIM_STARTS, scene_sprites.ANIM_STARTS[1:] + (0x38B88,)):
            frames = value['frames']
            if type(frames) is not list or value['start'] != start or value['end'] != start+len(frames)+2:
                raise ValueError('declared original first-control animation geometry differs')
            if value['end'] > allocation_end: raise ValueError('animation framing crosses old editor allocation')
            contract['animations'].append(dict(id=value['id'], start=start, end=value['end'], frame_count=len(frames),
                                                unread_tail_end=allocation_end))
        contract['limits'] += ['six unread animation tail BYTEs and three unreferenced palettes not emitted',
                               'reset BYTE is not clamped to its local allocation; original42 retained']
    if resource_id in ('bank08_display_resources', 'bank06_display_tail'):
        codec = bank08 if resource_id == 'bank08_display_resources' else bank06
        contract['excluded_original_gaps'] = [list(span) for span in codec.UNKNOWN]
        contract['limits'] += ['counted negative WORDs are procedural cells, not terminators',
                               'unproved gaps outside actual source reads are not emitted by this owner']
    rows = ENCODERS[resource_id](canonical_fields, contract)
    contract.update(spans=coalesced_spans(rows), bytes=sum(len(row['data']) for row in rows), physical_blocks=len(rows))
    return contract
