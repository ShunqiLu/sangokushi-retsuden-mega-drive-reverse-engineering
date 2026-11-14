"""Publish build-connected external image, layout and audio source files.

Only the explicit own source authorities are read. An optional complete named
audio document replaces only audio_build; it is never a fallback sidecar.
Selected publication does not read or publish omitted resources. Other resources
are copied as their own typed JSON, not guessed into pictures or music. Fixed
compression controls remain JSON authorities while supported pixel values
live only in indexed PNG members; decoded previews are not a second importer.
This intermediate does not claim all asset identities known.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .media_sources import FORMAT as EXTERNAL_MEDIA_FORMAT, REFERENCE, json_bytes, load_source, member_path
from .readable_text import (FORMAT as READABLE_TEXT_FORMAT, to_readable,
                            parse_manual_sources, _load as load_text_document)
from .scenario_sources import FORMAT as NAMED_SCENARIO_FORMAT, to_named as scenario_to_named
from .ai_policy_sources import (FORMAT as NAMED_AI_CUTOFF_FORMAT,
                                RESOURCE_ID as AI_CUTOFF_RESOURCE_ID,
                                to_named as ai_cutoffs_to_named)
from .ai_selection_sources import (FORMAT as NAMED_AI_SELECTION_FORMAT,
                                   RESOURCE_ID as AI_SELECTION_RESOURCE_ID,
                                   to_named as ai_selection_to_named)
from .audio_sequence_sources import (FORMAT as NAMED_AUDIO_SEQUENCE_FORMAT,
                                    RESOURCE_ID as AUDIO_SEQUENCE_RESOURCE_ID,
                                    to_named as audio_sequences_to_named)
from .media_word_rle import TITLE_STREAM_IDS, externalize_title_tiles
from .media_package import LIMITS, Package
from .media_layout_sources import CONVERTERS as LAYOUT_CONVERTERS
from .media_alias_sources import CONVERTERS as ALIAS_CONVERTERS
from .native import fresh_output
from .resource_registry import GEOMETRY, RESOURCE_SPECS
from .scene_manifest import SCENE_SOURCE_MANIFEST, scene_source_manifest_bytes


SUPPORTED = ('font_build', 'portrait_graphics', 'graphics_build', 'audio_build', 'scaled_bitmaps',
             'sprite_word_resources', 'battle_variant_tiles', 'world_tile_chunks', 'compact_sprite_records')
SUPPORTED += ('scene_tile_resources', 'scene_sprite_resources', 'display_tile_resources',
              'bank08_display_resources', 'bank06_display_tail')
SUPPORTED += ('terrain_maps', 'battlefield_resources', 'battle_graphics',
              'vdp_word_streams', 'dictionary_streams')
SUPPORTED += tuple(LAYOUT_CONVERTERS)
SUPPORTED += tuple(ALIAS_CONVERTERS)


def font_package(fields):
    package = Package('font_build', fields)
    for font_index, font in enumerate(fields['fonts']):
        for glyph_index, glyph in enumerate(font['glyphs']):
            package.replace(('fonts', font_index, 'glyphs', glyph_index, 'rows'),
                            'assets/images/fonts/' + font['id'] + '/' + glyph['id'] + '.png',
                            codec='mono_rows', width=font['width'], height=font['height'], bit_order='msb')
    return package


def portrait_package(fields):
    package = Package('portrait_graphics', fields)
    for index, tile in enumerate(fields['tiles']):
        package.replace(('tiles', index, 'rows'),
                        'assets/images/portraits/shared_tiles/' + tile['id'] + '.png',
                        codec='tile4_rows', width=8, height=8, bit_order='msb')
    for index, image in enumerate(fields['images']):
        package.replace(('images', index), 'assets/images/portraits/layouts/' + image['id'] + '.json')
    for index, palette in enumerate(fields['palettes']):
        package.replace(('palettes', index), f"assets/images/portraits/palettes/palette_{palette['selector']:03d}.json")
    return package


def graphics_package(fields):
    package = Package('graphics_build', fields)
    for index, asset in enumerate(fields['assets']):
        family = 'title' if asset['id'].startswith('title_') else 'duel'
        if asset['id'] in TITLE_STREAM_IDS:
            if asset['kind'] != 'word_rle':
                raise ValueError('the registered title pixel stream must retain its original word-RLE kind')
            externalize_title_tiles(package, ('assets', index, 'fields', 'commands'),
                                    'assets/images/title/rle_tiles/' + asset['id'])
        elif 'tiles' in asset['fields'] and set(asset['fields']) == {'tiles'}:
            for tile_index, tile in enumerate(asset['fields']['tiles']):
                package.replace(('assets', index, 'fields', 'tiles', tile_index),
                                f"assets/images/{family}/tiles/{asset['id']}/tile_{tile_index:04d}.png",
                                codec='tile4_rows', width=8, height=8, bit_order='msb')
        else:
            # Map attributes, lane-RLE maps, CRAM and candidate transfer WORDs
            # stay typed data. They are never interpreted as fake tile pixels.
            package.replace(('assets', index, 'fields'), f"assets/images/{family}/fields/{asset['id']}.json")
    return package


def audio_package(fields):
    package = Package('audio_build', fields)
    definitions = fields['definitions']
    for group in ('music', 'sfx'):
        for index, definition in enumerate(definitions[group]):
            package.replace(('definitions', group, index), 'assets/audio/' + group + '/' + definition['id'] + '.json')
        package.replace(('definitions', group + '_pointer_table'), 'assets/audio/' + group + '/directory.json')
    for bank_index, bank in enumerate(definitions['instrument_banks']):
        for index, record in enumerate(bank['records']):
            package.replace(('definitions', 'instrument_banks', bank_index, 'records', index),
                            f"assets/audio/instruments/{bank['id']}/instrument_{index:03d}.json")
    for index, table in enumerate(fields['envelopes']['tables']):
        package.replace(('envelopes', 'tables', index), 'assets/audio/envelopes/' + table['family'] + '.json')
    # Event views retain source modes and physical aliases. They are not
    # relabelled as independent notes or copied into each music definition.
    package.replace(('sequences', 'views'), 'assets/audio/shared/stateful_event_views.json')
    for index, voice in enumerate(fields['sequences']['rhythm']['voice_records']):
        package.replace(('sequences', 'rhythm', 'voice_records', index),
                        f'assets/audio/instruments/rhythm/voice_{index:03d}.json')
    # Remaining rhythm directories/fields contain the unique voice references.
    # The recursive reader resolves those files, not an embedded backup.
    package.replace(('sequences', 'rhythm'), 'assets/audio/shared/rhythm.json')
    return package


def scaled_package(fields):
    package = Package('scaled_bitmaps', fields)
    for index, bitmap in enumerate(fields['bitmaps']):
        package.replace(('bitmaps', index, 'rows'),
                        'assets/images/shared/scaled_bitmaps/' + bitmap['id'] + '.png',
                        codec='mono_rows', width=32, height=32, bit_order='lsb')
    return package


def word_commands(package, locator, directory):
    """Externalize original RLE values without recompressing a decoded picture.

    A strip row has exactly four nibble indices: one original command's WORD.
    Run controls/counts and marker stay source metadata. Editing a repeated row
    affects its complete original run; changing run topology is not inferred.
    """
    container = package.graph
    for key in locator[:-1]:
        container = container[key]
    commands = container[locator[-1]]
    if (type(commands) is not list or not 1 <= len(commands) <= 4096 or
            any(type(command) is not dict or 'word' not in command for command in commands)):
        raise ValueError('bounded original word commands required')
    strips = []
    for start in range(0, len(commands), 32):
        words = [command['word'] for command in commands[start:start + 32]]
        strips.append(package.add(words, f'{directory}/word_strip_{start // 32:04d}.png',
                                  codec='word_pixels', width=4, height=len(words), bit_order='msb',
                                  source_locator=(*locator, start, 'word')))
    controls = [{key: value for key, value in command.items() if key != 'word'} for command in commands]
    source = dict(format='g5510-word-rle-command-pixels-v1', controls=controls, word_strips=strips)
    container[locator[-1]] = package.add(source, directory + '/commands.json', codec='word_rle_commands',
                                        source_locator=locator)


def sprite_words_package(fields):
    package = Package('sprite_word_resources', fields)
    base = 'assets/images/shared/sprite_word_resources'
    word_commands(package, ('tile_stream', 'commands'), base + '/tile_stream')
    for key in ('sprites', 'sprite_directory', 'dictionary_directories'):
        package.replace((key,), base + '/' + key + '.json')
    for index, row in enumerate(fields['dictionary_streams']):
        package.replace(('dictionary_streams', index), base + '/dictionary_streams/' + row['id'] + '.json')
    return package


def variants_package(fields):
    package = Package('battle_variant_tiles', fields)
    base = 'assets/images/shared/battle_variant_tiles'
    package.replace(('directories',), base + '/directories.json')
    for index, stream in enumerate(fields['streams']):
        word_commands(package, ('streams', index, 'fields', 'commands'), base + '/' + stream['id'])
    return package


def world_chunks_package(fields):
    package = Package('world_tile_chunks', fields)
    base = 'assets/images/backgrounds/world_tile_chunks'
    package.replace(('directory',), base + '/directory.json')
    for index, chunk in enumerate(fields['chunks']):
        # These WORDs are map grammar/attributes, not necessarily tile pixels.
        # Keep original column command JSON; never paint them as a fake image.
        package.replace(('chunks', index, 'columns'), base + '/' + chunk['id'] + '/columns.json')
    return package


def compact_sprites_package(fields):
    package = Package('compact_sprite_records', fields)
    base = 'assets/images/shared/compact_sprite_records'
    for index, descriptor in enumerate(fields['descriptors']):
        package.replace(('descriptors', index, 'records'), base + '/layouts/' + descriptor['id'] + '.json')
    for index, directory in enumerate(fields['directories']):
        package.replace(('directories', index, 'targets'), base + '/directories/' + directory['id'] + '.json')
    return package


def pixel_banks(package, collection, base):
    for bank_index, bank in enumerate(package.graph[collection]):
        for tile_index, tile in enumerate(bank['tiles']):
            package.replace((collection, bank_index, 'tiles', tile_index, 'pixels'),
                            base + '/tiles/' + bank['id'] + '/' + tile['id'] + '.png',
                            codec='tile4_pixels', width=8, height=8, bit_order='msb')


def scene_tiles_package(fields):
    package = Package('scene_tile_resources', fields)
    base = 'assets/images/shared/scene_tile_resources'
    pixel_banks(package, 'tile_banks', base)
    package.replace(('palette',), base + '/palette.json')
    for index, layout in enumerate(fields['maps']):
        # These WORDs are map attributes/indices, not four-index pixel rows.
        package.replace(('maps', index, 'fields'), base + '/maps/' + layout['id'] + '.json')
    return package


def scene_sprites_package(fields):
    package = Package('scene_sprite_resources', fields)
    base = 'assets/images/shared/scene_sprite_resources'
    for collection in ('palettes', 'animations'):
        for index, row in enumerate(fields[collection]):
            package.replace((collection, index), base + '/' + collection + '/' + row['id'] + '.json')
    for name in fields['parameters']:
        package.replace(('parameters', name), base + '/parameters/' + name + '.json')
    for name in ('palette_directory', 'animation_directory', 'WORD_row'):
        package.replace((name,), base + '/' + name + '.json')
    return package


def display_package(ident, fields):
    package = Package(ident, fields)
    base = 'assets/images/shared/' + ident
    collection = 'banks' if ident == 'display_tile_resources' else 'tile_uploads'
    pixel_banks(package, collection, base)
    for index, row in enumerate(fields.get('font_WORD_sources', [])):
        package.replace(('font_WORD_sources', index, 'cells'), base + '/font_sources/' + row['id'] + '.json')
    if 'font_BYTE_source' in fields:
        package.replace(('font_BYTE_source', 'glyph_indices'), base + '/font_sources/glyph_indices.json')
    return package


def terrain_package(fields):
    """Full map WORD grids and terrain types, never fake four-bit pixels."""
    package = Package('terrain_maps', fields)
    base = 'assets/images/backgrounds/terrain_maps'
    package.replace(('type_values',), base + '/type_values.json')
    for index, record in enumerate(fields['maps']):
        package.replace(('maps', index, 'rows'), base + '/' + record['id'] + '/rows.json')
    return package


def battlefield_package(fields):
    """Keep full selection, coordinate and rectangle WORDs per physical map."""
    package = Package('battlefield_resources', fields)
    base = 'assets/images/backgrounds/battlefield_resources'
    for family in ('selection_108', 'selection_58', 'coordinates_a',
                   'coordinates_b', 'rectangles', 'centers'):
        for index, record in enumerate(fields[family]):
            package.replace((family, index), base + '/' + family + '/' + record['id'] + '.json')
    return package


def battle_graphics_package(fields):
    """Tile command WORDs own pixels; big-WORD maps own only layout grammar."""
    package = Package('battle_graphics', fields)
    base = 'assets/images/backgrounds/battle_graphics'
    package.replace(('directories',), base + '/directories.json')
    for index, stream in enumerate(fields['streams']):
        if stream['byte_order'] == 'little':
            word_commands(package, ('streams', index, 'fields', 'commands'),
                          base + '/tiles/' + stream['id'])
        elif stream['byte_order'] == 'big':
            package.replace(('streams', index, 'fields'), base + '/maps/' + stream['id'] + '.json')
        else:
            raise ValueError('original battle tile/map word order required')
    return package


def vdp_streams_package(fields):
    """Externalize command fields without guessing their visual identities.

    The final empty stream remains validation-only dependency context: its
    physical marker belongs to the existing distinct marker owner, not here.
    Directory metadata is still pinned by this schema and emitted separately.
    """
    package = Package('vdp_word_streams', fields)
    base = 'assets/images/shared/vdp_word_streams'
    for index, record in enumerate(fields['blocks']):
        package.replace(('blocks', index, 'fields'), base + '/' + record['id'] + '.json')
    return package


def dictionary_package(fields):
    """FE/FF grammar stays typed JSON; only proven raw tile pixels become PNG."""
    package = Package('dictionary_streams', fields)
    base = 'assets/images/shared/dictionary_streams'
    for index, dataset in enumerate(fields['datasets']):
        for key in ('dictionary_entries', 'source_tokens'):
            package.replace(('datasets', index, key), base + '/' + dataset['id'] + '/' + key + '.json')
    package.replace(('count_fields',), base + '/count_fields.json')
    for index, record in enumerate(fields['records']['records']):
        package.replace(('records', 'records', index, 'words'), base + '/records/' + record['id'] + '.json')
    package.replace(('raw_transfer', 'longs'), base + '/raw_transfer.json')
    for index, tile in enumerate(fields['raw_tiles']['tiles']):
        package.replace(('raw_tiles', 'tiles', index, 'pixels'), base + '/tiles/' + tile['id'] + '.png',
                        codec='tile4_pixels', width=8, height=8, bit_order='msb')
    return package


CONVERTERS = dict(font_build=font_package, portrait_graphics=portrait_package,
                  graphics_build=graphics_package, audio_build=audio_package, scaled_bitmaps=scaled_package,
                  sprite_word_resources=sprite_words_package, battle_variant_tiles=variants_package,
                  world_tile_chunks=world_chunks_package, compact_sprite_records=compact_sprites_package,
                  scene_tile_resources=scene_tiles_package, scene_sprite_resources=scene_sprites_package,
                  display_tile_resources=lambda fields: display_package('display_tile_resources', fields),
                  bank08_display_resources=lambda fields: display_package('bank08_display_resources', fields),
                  bank06_display_tail=lambda fields: display_package('bank06_display_tail', fields),
                  terrain_maps=terrain_package, battlefield_resources=battlefield_package,
                  battle_graphics=battle_graphics_package, vdp_word_streams=vdp_streams_package,
                  dictionary_streams=dictionary_package)
CONVERTERS.update(LAYOUT_CONVERTERS)
CONVERTERS.update(ALIAS_CONVERTERS)


def _selected_specs(ids: list[str] | tuple[str, ...] | None):
    """Resolve one explicit unique selection, retaining the full-tree default."""
    known = {spec.id: spec for spec in RESOURCE_SPECS}
    if ids is not None and type(ids) not in (list, tuple):
        raise ValueError('nonempty explicit unique registered IDs required')
    selected = tuple(known) if ids is None else tuple(ids)
    if (not selected or any(type(ident) is not str for ident in selected)
            or len(selected) != len(set(selected))
            or any(ident not in known for ident in selected)):
        raise ValueError('nonempty explicit unique registered IDs required')
    return tuple(known[ident] for ident in selected)


def _named_audio_source(path: Path) -> tuple[Path, dict]:
    """Read exactly one ordinary complete named audio authority, not a graph.

    The existing resolver validates its complete schema and command fields.
    This input never searches an old root when a name, member or field is bad.
    """
    if not isinstance(path, Path):
        raise ValueError('one explicit named audio JSON path required')
    absolute = path.absolute()
    for ancestor in (absolute, *absolute.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ValueError('named audio source through a reparse point refused')
    document = load_text_document(absolute)
    if type(document) is not dict or document.get('format') != NAMED_AUDIO_SEQUENCE_FORMAT:
        raise ValueError('audio-source requires one complete named audio_build document')
    return absolute.resolve(strict=True), document


def export(source_root: Path, output: Path, *, glyph_sources: list[dict] | None = None,
        named_scenarios: bool = False, named_ai_cutoffs: bool = False,
        named_ai_selection: bool = False,
        named_audio_sequences: bool = False,
        ids: list[str] | tuple[str, ...] | None = None,
        audio_source: Path | None = None) -> dict:
    """Publish selected own packages, optionally from one named audio document.

    With no selection or audio override the original full-tree path is kept.
    A selected root owns only its listed IDs; it cannot replace omitted owners
    in a full-game source manifest. No resource codec or game owner is run.
    """
    selected_specs = _selected_specs(ids)
    if audio_source is not None and not any(
            spec.id == AUDIO_SEQUENCE_RESOURCE_ID for spec in selected_specs):
        raise ValueError('audio-source requires audio_build in the selected resource IDs')
    source_root = source_root.resolve(strict=True)
    target = fresh_output(output)
    if target.is_relative_to(source_root) or source_root.is_relative_to(target):
        raise ValueError('new media source tree must be separate from input')
    geometry = json.loads(GEOMETRY.read_text(encoding='utf-8'))
    if type(named_scenarios) is not bool:
        raise ValueError('explicit named-scenario source publication choice required')
    if type(named_ai_cutoffs) is not bool:
        raise ValueError('explicit named-AI-cutoff source publication choice required')
    if type(named_ai_selection) is not bool:
        raise ValueError('explicit named-AI-candidate source publication choice required')
    if type(named_audio_sequences) is not bool:
        raise ValueError('explicit named-audio-command source publication choice required')
    if glyph_sources is not None:
        parse_manual_sources(glyph_sources)
    audio_document = None
    if audio_source is not None:
        audio_source, audio_document = _named_audio_source(audio_source)
    files, records = {}, []
    for spec in selected_specs:
        readable_source = None
        named_scenario_source = None
        named_ai_source = None
        preserve_named_ai_selection = False
        preserve_named_audio = False
        use_named_audio = spec.id == AUDIO_SEQUENCE_RESOURCE_ID and audio_document is not None
        source_path = audio_source if use_named_audio else member_path(source_root, spec.own_source)
        if spec.id in ('dialogue_text', 'scenario_build', AI_CUTOFF_RESOURCE_ID,
                AI_SELECTION_RESOURCE_ID, AUDIO_SEQUENCE_RESOURCE_ID):
            from .media_sources import resolve_source_document
            source_document = audio_document if use_named_audio else load_text_document(source_path)
            fields = resolve_source_document(source_document, source_root, spec.id)
            if spec.id == 'dialogue_text' and source_document.get('format') == READABLE_TEXT_FORMAT:
                readable_source = source_document
            if spec.id == 'scenario_build' and source_document.get('format') == NAMED_SCENARIO_FORMAT:
                named_scenario_source = source_document
            if spec.id == AI_CUTOFF_RESOURCE_ID and source_document.get('format') == NAMED_AI_CUTOFF_FORMAT:
                named_ai_source = source_document
            if spec.id == AI_SELECTION_RESOURCE_ID:
                preserve_named_ai_selection = (source_document.get('format') == NAMED_AI_SELECTION_FORMAT
                    or (source_document.get('format') == EXTERNAL_MEDIA_FORMAT
                        and source_document.get('source_format') == NAMED_AI_SELECTION_FORMAT))
            if spec.id == AUDIO_SEQUENCE_RESOURCE_ID:
                preserve_named_audio = (source_document.get('format') == NAMED_AUDIO_SEQUENCE_FORMAT
                    or (source_document.get('format') == EXTERNAL_MEDIA_FORMAT
                        and source_document.get('source_format') == NAMED_AUDIO_SEQUENCE_FORMAT))
        else:
            fields = load_source(source_path, source_root, spec.id)
        if fields['format'] != geometry['contracts'][spec.id]['format']:
            raise ValueError('registered source format differs: ' + spec.id)
        if spec.id == AUDIO_SEQUENCE_RESOURCE_ID and (named_audio_sequences or preserve_named_audio):
            # Transform before externalization: the shared event member is the
            # only editable command authority, never a named sidecar over raw
            # opcode/argument bytes. Keep all existing audio paths and aliases.
            fields = audio_sequences_to_named(fields)
        if spec.id == AI_SELECTION_RESOURCE_ID and (named_ai_selection or preserve_named_ai_selection):
            # Keep one full-BYTE authority, including already-named graphs;
            # no positional backup or guessed personality/difficulty mapping.
            fields = ai_selection_to_named(fields)
        if spec.id in CONVERTERS:
            package = CONVERTERS[spec.id](fields)
            for filename, raw in package.files.items():
                if filename in files:
                    raise ValueError('cross-package duplicate external media path')
                files[filename] = raw
            fields = package.wrapper()
            members = package.members
        else:
            members = []
        if spec.id == 'dialogue_text':
            if glyph_sources is not None:
                fields = to_readable(fields, glyph_sources)
            elif readable_source is not None:
                # Preserve the same captured sole text authority. Do not
                # silently replace an editable Unicode source with raw WORDs.
                fields = readable_source
        if spec.id == 'scenario_build':
            if named_scenarios:
                fields = scenario_to_named(fields)
            elif named_scenario_source is not None:
                # Preserve the sole editable named source after normal typed
                # validation; do not republish an old raw-address duplicate.
                fields = named_scenario_source
        if spec.id == AI_CUTOFF_RESOURCE_ID:
            if named_ai_cutoffs:
                fields = ai_cutoffs_to_named(fields)
            elif named_ai_source is not None:
                fields = named_ai_source
        if spec.own_source in files:
            raise ValueError('duplicate resource graph source path')
        files[spec.own_source] = json_bytes(fields)
        contract = geometry['contracts'][spec.id]
        records.append(dict(id=spec.id, source=spec.own_source, role=spec.role,
                            external_graph=bool(members), members=members,
                            physical_spans=contract['spans'], confidence=contract['confidence'],
                            physical_BYTES=sum(end - start for start, end in contract['spans'])))
    if SCENE_SOURCE_MANIFEST in files:
        raise ValueError('Scene entry competes with an external media member')
    files[SCENE_SOURCE_MANIFEST] = scene_source_manifest_bytes(tuple(row['id'] for row in records))
    target.mkdir(parents=True)
    for relative, raw in sorted(files.items()):
        path = member_path(target, relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
    complete_registration = len(records) == len(RESOURCE_SPECS)
    manifest = dict(format='g5510-build-connected-media-publication-v1', resources=records,
                    scene_source_manifest=SCENE_SOURCE_MANIFEST, scene_source_root='.',
                    registered_resources=len(records), available_registered_resources=len(RESOURCE_SPECS),
                    complete_source_registration=complete_registration,
                    publication_scope='complete_registration' if complete_registration else 'selected_subset',
                    input_source_root=str(source_root),
                    named_audio_source=None if audio_source is None else str(audio_source),
                    external_packages=sum(spec.id in SUPPORTED for spec in selected_specs),
                    externalized_physical_BYTES=sum(row['physical_BYTES'] for row in records if row['external_graph']),
                    PNG_sources=sum(name.endswith('.png') for name in files),
                    external_JSON_sources=sum(name.startswith('assets/') and name.endswith('.json') for name in files),
                    files=len(files), original_ROM_read=False, native_run=False, hash_run=False,
                    edited_display_audio_proven=False, all_asset_identities_known=False,
                    final_delivery=False, new_matching_BYTES=0, new_strict_BYTES=0,
                    build_requirement=('Use --resource-root this directory; original typed JSON is not a fallback'
                        if complete_registration else
                        'Owns only listed IDs; omitted resources require separate explicit source roots'),
                    limits=list(LIMITS))
    (target / 'asset-source-manifest.json').write_bytes(json_bytes(manifest))
    print(json.dumps({key: value for key, value in manifest.items() if key != 'resources'}, ensure_ascii=False), flush=True)
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--ids', nargs='+',
        help='仅发布明确的唯一注册ID；不指定时保持全部注册资源的原行为')
    parser.add_argument('--audio-source', type=Path,
        help='可选完整具名audio_build JSON，取代该ID的输入；不接受graph或typed备份，不回退')
    parser.add_argument('--glyph-sources', type=Path, nargs=2,
                        help='可选明确的两份人工字形标注；主对话/武将/城市名输出为独立可读源')
    parser.add_argument('--named-scenarios', action='store_true',
        help='按已确证字段输出具名剧本；未知位及原数值宽度不变')
    parser.add_argument('--named-ai-cutoffs', action='store_true',
        help='将整组48对AI比较WORD输出为具名字段；原共享别名和未知分组不变')
    parser.add_argument('--named-ai-selection', action='store_true',
        help='将196个AI候选首道资格BYTE输出为具名gate；原0/1区别、未知行身份和间隙不变')
    parser.add_argument('--named-audio-sequences', action='store_true',
        help='将有状态音频控制命令输出为具名编辑源；原模式、参数宽度和共享位置不变')
    args = parser.parse_args(argv)
    documents = (None if args.glyph_sources is None else
        [load_text_document(path, 1_000_000) for path in args.glyph_sources])
    export(args.source_root, args.output, glyph_sources=documents,
        named_scenarios=args.named_scenarios, named_ai_cutoffs=args.named_ai_cutoffs,
        named_ai_selection=args.named_ai_selection,
        named_audio_sequences=args.named_audio_sequences, ids=args.ids,
        audio_source=args.audio_source)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
