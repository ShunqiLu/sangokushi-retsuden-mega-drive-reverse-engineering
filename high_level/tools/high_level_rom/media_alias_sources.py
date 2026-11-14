"""External edit authorities for proven portrait aliases, UI and audio fields.

Physical aliases remain shared source allocations. A sparse pixel pair owns
only its original BYTE, never the neighbouring pixels in an imagined tile.
Witnesses, reserved fields and uncertain visual/audio identities stay metadata.
"""
from __future__ import annotations

from .media_package import Package


def portrait_tiles_package(ident, fields):
    """Each already-owned complete tile has one editable indexed PNG."""
    package = Package(ident, fields)
    base = 'assets/images/portraits/' + ident
    for index, tile in enumerate(fields['tiles']):
        package.replace(('tiles', index, 'pixels'), base + '/tiles/' + tile['id'] + '.png',
                        codec='tile4_pixels', width=8, height=8, bit_order='msb')
    return package


def portrait_external_package(fields):
    """Preserve two complete tiles and each separately owned sparse BYTE."""
    package = Package('portrait_external_alias_pixels', fields)
    base = 'assets/images/portraits/portrait_external_alias_pixels'
    for index, tile in enumerate(fields['full_tiles']):
        package.replace(('full_tiles', index, 'pixels'), base + '/tiles/' + tile['id'] + '.png',
                        codec='tile4_pixels', width=8, height=8, bit_order='msb')
    for tile_index, tile in enumerate(fields['sparse_tiles']):
        for pair_index, pair in enumerate(tile['pixel_pairs']):
            package.replace(('sparse_tiles', tile_index, 'pixel_pairs', pair_index, 'pixels'),
                            base + '/pixel_pairs/' + tile['id'] + '/' + pair['id'] + '.png',
                            codec='pixel_pair4', width=2, height=1, bit_order='msb')
    return package


def portrait_metadata_package(fields):
    """Palette WORD fields and token references are data, not new pixels."""
    package = Package('portrait_alias_metadata', fields)
    base = 'assets/images/portraits/portrait_alias_metadata'
    for index, palette in enumerate(fields['palette_sources']):
        package.replace(('palette_sources', index, 'colours'),
                        base + '/palettes/' + palette['id'] + '.json')
    for index, tokens in enumerate(fields['token_sources']):
        package.replace(('token_sources', index, 'WORDs'),
                        base + '/layouts/' + tokens['id'] + '.json')
    return package


def ui_templates_package(ident, fields):
    """Keep full sprite attributes/terminators; do not rasterize layout WORDs."""
    package = Package(ident, fields)
    base = 'assets/images/ui/' + ident
    for index, template in enumerate(fields['templates']):
        package.replace(('templates', index, 'records'),
                        base + '/templates/' + template['id'] + '.json')
    if ident == 'setup_ui_sprite_fields':
        for index, coordinates in enumerate(fields['coordinate_lists']):
            package.replace(('coordinate_lists', index, 'coordinates'),
                            base + '/coordinates/' + coordinates['id'] + '.json')
        package.replace(('selector_coordinates',), base + '/selector_coordinates.json')
    return package


def audio_alias_package(ident, fields):
    """Each physical sound source owns one file, never one copy per witness."""
    package = Package(ident, fields)
    base = 'assets/audio/shared/' + ident
    if ident == 'fm_external_alias_fields':
        # The allocation is not 25-BYTE aligned. Keeping the one physical
        # vector avoids conflicting copies for its many conditional views.
        package.replace(('source_BYTEs',), base + '/source_BYTEs.json')
    elif ident == 'fm_sparse_alias_fields':
        for index, record in enumerate(fields['source_fields']):
            package.replace(('source_fields', index), base + '/fields/' + record['id'] + '.json')
    elif ident == 'z80_startup_seed_fields':
        for index, seed in enumerate(fields['seeds']):
            package.replace(('seeds', index, 'value'), base + '/seeds/' + seed['id'] + '.json')
    elif ident == 'scene_audio_command_word_fields':
        package.replace(('table', 'WORDs'), base + '/' + fields['table']['id'] + '.json')
    else:
        raise ValueError('only the four declared physical audio source families are supported')
    return package


CONVERTERS = {
    **{ident: (lambda fields, ident=ident: portrait_tiles_package(ident, fields))
       for ident in ('portrait_alias_tiles', 'portrait_blank_alias_tiles')},
    'portrait_external_alias_pixels': portrait_external_package,
    'portrait_alias_metadata': portrait_metadata_package,
    **{ident: (lambda fields, ident=ident: ui_templates_package(ident, fields))
       for ident in ('setup_ui_sprite_fields', 'compact_ui_sprite_fields')},
    **{ident: (lambda fields, ident=ident: audio_alias_package(ident, fields))
       for ident in ('fm_external_alias_fields', 'fm_sparse_alias_fields',
                     'z80_startup_seed_fields', 'scene_audio_command_word_fields')},
}
