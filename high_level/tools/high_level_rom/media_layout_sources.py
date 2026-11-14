"""Publish complete sprite/layout and audio-table definitions as own files.

Layouts, sprite attributes and command targets are not four-bit pixels. Their
complete typed records stay JSON, including reserved bits and physical aliases.
Confirmed tile pixel sources remain in the separate image converters. Fixed
capacity/schema checks belong to the existing pure resource encoders.
"""
from __future__ import annotations

from .media_package import Package


def map_layout_package(ident, fields):
    """WORD tile-map commands keep priority/palette/flip/index in one field."""
    package = Package(ident, fields)
    base = 'assets/images/backgrounds/' + ident
    for index, row in enumerate(fields['maps']):
        package.replace(('maps', index), base + '/layouts/' + row['id'] + '.json')
    if 'directories' in fields:
        for index, row in enumerate(fields['directories']):
            package.replace(('directories', index), base + '/directories/' + row['id'] + '.json')
    return package


def ui_layout_package(ident, fields):
    """Externalize physical UI stream/row definitions without grammar guesses."""
    package = Package(ident, fields)
    base = 'assets/images/ui/' + ident
    collection = {'menu_tile_streams': 'streams', 'ui_layouts': 'blocks',
                  'ui_fixed_records': 'groups'}[ident]
    for index, row in enumerate(fields[collection]):
        package.replace((collection, index), base + '/' + row['id'] + '.json')
    if 'directory' in fields:
        package.replace(('directory',), base + '/directory.json')
    return package


def duel_sprite_package(fields):
    """71 physical six-BYTE descriptor files, not duplicated per selector."""
    package = Package('sprite_records', fields)
    base = 'assets/images/characters/duel_sprite_records'
    package.replace(('pointers',), base + '/directory.json')
    for index, row in enumerate(fields['descriptors']):
        name = 'rom_' + format(row['start'], '06X') + '_descriptor'
        package.replace(('descriptors', index), base + '/descriptors/' + name + '.json')
    return package


def battle_sprite_package(ident, fields):
    """One authority per physical descriptor, preserving first-80 tail policy."""
    package = Package(ident, fields)
    base = 'assets/images/shared/' + ident
    for index, row in enumerate(fields['descriptors']):
        package.replace(('descriptors', index), base + '/descriptors/' + row['id'] + '.json')
    if 'directories' in fields:
        for index, row in enumerate(fields['directories']):
            package.replace(('directories', index), base + '/directories/' + row['id'] + '.json')
    for key in ('directory', 'base_selector_BYTES', 'directory_targets', 'attribute_WORDs'):
        if key in fields:
            package.replace((key,), base + '/' + key + '.json')
    return package


def palette_package(ident, fields):
    """Keep complete CRAM fields; colour previews never replace reserved bits."""
    package = Package(ident, fields)
    base = 'assets/images/shared/' + ident
    for collection in ('palettes', 'transfers'):
        for index, row in enumerate(fields[collection]):
            package.replace((collection, index), base + '/' + collection + '/' + row['id'] + '.json')
    return package


def audio_tables_package(ident, fields):
    """Full LE16 tables/references and conditional FM fields, not new songs."""
    package = Package(ident, fields)
    base = 'assets/audio/shared/' + ident
    if ident == 'audio_root_resources':
        for collection in ('roots', 'priorities'):
            for index, row in enumerate(fields[collection]):
                package.replace((collection, index), base + '/' + collection + '/' + row['id'] + '.json')
        package.replace(('secondary_sfx_pointer',), base + '/secondary_sfx_pointer.json')
    elif ident == 'fm_instrument_alias_fields':
        for index, row in enumerate(fields['records']):
            package.replace(('records', index), base + '/conditional_records/' +
                            f"instrument_index_{row['instrument_index']:03d}.json")
    else:
        for index, row in enumerate(fields['tables']):
            package.replace(('tables', index), base + '/tables/' + row['id'] + '.json')
    return package


CONVERTERS = {
    'sprite_records': duel_sprite_package,
    **{ident: (lambda fields, ident=ident: map_layout_package(ident, fields))
       for ident in ('battle_overlay_maps', 'title_overlay_maps')},
    **{ident: (lambda fields, ident=ident: ui_layout_package(ident, fields))
       for ident in ('menu_tile_streams', 'ui_layouts', 'ui_fixed_records')},
    **{ident: (lambda fields, ident=ident: battle_sprite_package(ident, fields))
       for ident in ('battle_scene_sprites', 'battle_effect_sprites',
                     'battle_command_sprites', 'battle_marker_sprites')},
    **{ident: (lambda fields, ident=ident: palette_package(ident, fields))
       for ident in ('battle_palette_transfers', 'palette_copy_fields')},
    **{ident: (lambda fields, ident=ident: audio_tables_package(ident, fields))
       for ident in ('audio_root_resources', 'fm_instrument_alias_fields',
                     'audio_frequency_fields', 'audio_dispatch_fields')},
}
