"""Source-only officer-to-portrait editing directory for the proven F372 UI.

B31A..B338 uses F372.W to select the fixed name at 8A504+6*F372.
B5B8..B5C0 passes that same WORD directly to 661D4. This establishes a
selector link, not recognition of a painted face or natural-display proof.
Only explicit name indexes, scenario record IDs and owned-media locators
are joined. No ROM, PNG pixels, game object or executable is read or run.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from .media_sources import (FORMAT as MEDIA_FORMAT, _member_parts, loads,
    member_path, json_bytes)
from .readable_text import FORMAT as NAMES_FORMAT, _load
from .scenario_sources import FORMAT as NAMED_SCENARIO_FORMAT, TYPED_FORMAT


FORMAT = 'g5510-officer-portrait-editing-directory-v1'
PORTRAIT_FORMAT = 'g5510-indexed-image-fields-v1'
TILE_BASE = 0xB649A
TOKEN_TABLES = (('primary', 0xAE39A, 48),
                ('secondary8', 0xB439A, 8),
                ('secondary4', 0xB539A, 4))
UNRESOLVED_NAME = re.compile(r'\u27e6[0-9A-F]{4}\u27e7|\ufffd')


def _uint(value, bits):
    if type(value) is not int or not 0 <= value < 1 << bits:
        raise ValueError('explicit unsigned source field required')
    return value


def _signed_word(value):
    value &= 65535
    return value - 65536 if value & 32768 else value


def _source_records(authority):
    """Keep declared scenario officer IDs; position never supplies identity."""
    if authority.get('format') not in (TYPED_FORMAT, NAMED_SCENARIO_FORMAT):
        raise ValueError('explicit existing typed/named scenario authority required')
    result, seen_scenarios = {}, set()
    for scenario in authority['scenarios']:
        ident = scenario['id']
        if type(ident) is not str or ident in seen_scenarios:
            raise ValueError('unique explicit scenario identity required')
        seen_scenarios.add(ident)
        seen_officers = set()
        for officer in scenario['officers']:
            officer_id = _uint(officer['id'], 16)
            if officer_id in seen_officers:
                raise ValueError('duplicate officer identity in scenario authority')
            seen_officers.add(officer_id)
            result.setdefault(officer_id, []).append(
                dict(scenario_id=ident, officer_record_id=officer_id))
    if not seen_scenarios:
        raise ValueError('at least one explicit scenario authority required')
    return result


def _source_names(names):
    if names.get('format') != NAMES_FORMAT:
        raise ValueError('explicit existing readable officer-name source required')
    result = {}
    for row in names['officer_names']:
        index = _uint(row['index'], 16)
        if index in result:
            raise ValueError('duplicate explicit officer-name index')
        # Retain incomplete readings verbatim instead of inventing characters.
        text = row.get('text')
        if text is not None and type(text) is not str:
            raise ValueError('officer name must be text or explicitly unknown')
        if index < 256 and row.get('start') != 0x8A504 + index * 6:
            raise ValueError('name index contradicts the fixed original record address')
        result[index] = dict(id=row.get('id'), index=index,
            start=row.get('start'), text=text,
            name_status=('unknown_missing_reading' if not text or not text.strip()
                else 'unknown_glyph_reading' if UNRESOLVED_NAME.search(text)
                else 'readable_source_label'))
    return result


def _media_members(document):
    if (document.get('format') != MEDIA_FORMAT
            or document.get('resource_id') != 'portrait_graphics'
            or document.get('source_format') != PORTRAIT_FORMAT
            or document.get('graph', {}).get('format') != PORTRAIT_FORMAT):
        raise ValueError('explicit existing owned portrait-graphics source required')
    result = {}
    for member in document['members']:
        ident = member['id']
        if type(ident) is not str or ident in result:
            raise ValueError('unique owned portrait member required')
        result[ident] = member
    return result


def _member(reference, members, codec):
    if type(reference) is not dict or set(reference) != {'$owned_media'}:
        raise ValueError('one explicit owned-media reference required')
    member = members.get(reference['$owned_media'])
    if member is None:
        return None
    if member['codec'] != codec:
        raise ValueError('portrait member codec contradicts its declared role')
    return member


class _PortraitMembers:
    """One explicit disk or captured-byte source, never a fallback search."""

    def __init__(self, *, source_root=None, source_files=None):
        if (source_root is None) == (source_files is None):
            raise ValueError('choose one explicit portrait root or captured member map')
        if source_files is not None and type(source_files) is not dict:
            raise ValueError('one captured relative-path to immutable-bytes map required')
        self.root = None if source_root is None else Path(source_root).resolve(strict=True)
        self.files = source_files
        self.json_documents = {}

    def exists(self, relative):
        _member_parts(relative)
        if self.root is not None:
            return member_path(self.root, relative).is_file()
        if relative not in self.files:
            return False
        if type(self.files[relative]) is not bytes or not self.files[relative]:
            raise ValueError('captured portrait member must contain immutable source bytes')
        return True

    def json_or_none(self, relative):
        if relative not in self.json_documents:
            if not self.exists(relative):
                return None
            self.json_documents[relative] = (_load(member_path(self.root, relative))
                if self.root is not None else loads(self.files[relative]))
        return self.json_documents[relative]


def _json_member(reference, members, sources):
    member = _member(reference, members, 'typed_json')
    if member is None:
        return None, None
    return member, sources.json_or_none(member['file'])


def _layouts(document, members, sources):
    """Check both exporter locators and image IDs; neither alone is guessed."""
    result = {}
    for position, reference in enumerate(document['graph']['images']):
        member, image = _json_member(reference, members, sources)
        if member is None or image is None:
            continue
        match = re.fullmatch(r'image_([0-9]{3})', image.get('id', ''))
        if match is None:
            raise ValueError('original explicit portrait image identity required')
        selector = int(match[1])
        if (selector != position or member.get('source_locator') != ['images', selector]
                or selector in result):
            raise ValueError('portrait ID, graph slot and owned locator disagree')
        result[selector] = (member, image)
    return result


def _tile_sources(document, members, sources):
    result = {}
    for tile in document['graph']['tiles']:
        start = _uint(tile['start'], 32)
        member = _member(tile['rows'], members, 'tile4_rows')
        if member is None:
            continue
        # Path validation and existence only: PNG contents are never opened.
        if start in result:
            raise ValueError('competing physical portrait-tile authorities')
        result[start] = dict(id=tile['id'], file=member['file'], start=start,
            status='existing_shared_png' if sources.exists(member['file']) else 'unknown_missing_png')
    return result


def _palette_sources(document, members, sources):
    result = {}
    for reference in document['graph']['palettes']:
        member, palette = _json_member(reference, members, sources)
        if member is None or palette is None:
            continue
        selector = _uint(palette['selector'], 8)
        if selector in result:
            raise ValueError('competing portrait-palette authorities')
        result[selector] = dict(file=member['file'], selector=selector,
            source_start=0xB599A + selector * 32)
    return result


def _tile_read_addresses(token, role):
    """Original primary LONG shift versus each secondary signed-WORD read."""
    token = _uint(token, 16)
    if role == 'primary':
        return [TILE_BASE + token * 32 + step * 4 for step in range(8)]
    base = TILE_BASE + (65536 if token >= 0x800 else 0)
    return [(base + _signed_word(token * 32 + step * 4)) & 0xFFFFFFFF
        for step in range(8)]


def _portrait_entry(selector, selected, tiles, palettes, shared):
    member, image = selected
    groups = {}
    for role, base, count in TOKEN_TABLES:
        tokens = image[role]
        if type(tokens) is not list or len(tokens) != count:
            raise ValueError('original portrait token-role count changed')
        uses = []
        for slot, token in enumerate(tokens):
            addresses = _tile_read_addresses(token, role)
            tile = tiles.get(addresses[0])
            contiguous = addresses == list(range(addresses[0], addresses[0] + 32, 4))
            if tile is not None and contiguous:
                shared[tile['id']] = tile
                uses.append(dict(slot=slot, original_token=token, tile_ref=tile['id'],
                    status=tile['status']))
            else:
                uses.append(dict(slot=slot, original_token=token, tile_ref=None,
                    status='unknown_unmapped_source', source_long_addresses=addresses))
        groups[role] = dict(source_start=base + _signed_word(selector * count * 2),
            tile_uses=uses)
    palette_selector = _uint(image['palette_selector'], 8)
    return dict(status='confirmed_selector_layout_link',
        layout_id=image['id'], layout_file=member['file'],
        original_selector_word=selector,
        palette_selector_source=0xB639A + _signed_word(selector),
        palette_selector_byte=palette_selector,
        palette=palettes.get(palette_selector),
        palette_status=('existing_palette_json' if palette_selector in palettes
                        else 'unknown_unmapped_palette'),
        tile_groups=groups, natural_display_acceptance='not_verified',
        painted_person_recognition='unknown')


def build_catalog(names, portraits, record_authority, *, source_root=None, source_files=None):
    """Join explicit source identities, producing metadata only, with no encoding."""
    records = _source_records(record_authority)
    names_by_index = _source_names(names)
    members = _media_members(portraits)
    sources = _PortraitMembers(source_root=source_root, source_files=source_files)
    layouts = _layouts(portraits, members, sources)
    tiles = _tile_sources(portraits, members, sources)
    palettes = _palette_sources(portraits, members, sources)
    shared, people = {}, []
    for selector in sorted(set(records) | set(names_by_index)):
        name = names_by_index.get(selector)
        entry = dict(officer_record_id=selector, name=name,
            scenario_records=records.get(selector, []), original_selector_word=selector,
            selector_protocol='B31A_name_and_B5B8_portrait_share_F372_WORD')
        if selector >= 256:
            entry['portrait'] = dict(status='unknown_outside_declared_256_layouts')
        elif selector not in records:
            entry['portrait'] = dict(status='unknown_missing_record_authority')
        elif name is None or name['name_status'] == 'unknown_missing_reading':
            entry['portrait'] = dict(status='unknown_missing_name_source')
        elif selector not in layouts:
            entry['portrait'] = dict(status='unknown_missing_layout')
        else:
            entry['portrait'] = _portrait_entry(selector, layouts[selector],
                tiles, palettes, shared)
        people.append(entry)
    return dict(format=FORMAT, role='derived_editing_directory_not_game_input',
        mapping_scope='F372 officer-details/city-head UI only',
        evidence=dict(name_source='8A504+signed16(F372.W*6), original B31A..B338',
            portrait_call='B5B8..B5C0: D0.W=F372.W,D1.W=5,JSR661D4',
            image_source='661D4: signed16(selector*96/16/8) token tables; no255 clamp',
            palette_source='B639A+signed16(selector), BYTE selector; B599A+selector*32',
            record_identity='explicit scenario officers[].id; not record order'),
        officers=people, shared_tiles=list(shared.values()),
        limits=['Names retain unresolved glyph escapes; no Unicode reading is invented.',
            'Selector association is source evidence, not natural execution or face recognition.',
            'Other portrait callers, high-WORD aliases and selectors beyond this allocation remain unknown.',
            'Palette JSON is the colour authority; PNG preview colours are not substituted.',
            'Shared PNG edits may affect multiple portraits; no private duplicate is generated.',
            'This metadata is derived, not a second editable game/resource authority.'])


def catalog_from_resource_snapshot(resource_files: dict[str, bytes],
        resource_paths: dict[str, str]) -> tuple[dict, str]:
    """Derive a local editing directory from the edition's exact captured source.

    No old catalog, input-root path, PNG pixel, codec or filesystem is read.
    The caller passes its actual registered ID-to-source paths; the directory
    cannot silently substitute an older name, scenario or portrait authority.
    """
    if type(resource_paths) is not dict:
        raise ValueError('explicit captured resource ID-to-source path map required')
    ids = ('dialogue_text', 'portrait_graphics', 'scenario_build')
    if any(ident not in resource_paths for ident in ids):
        raise ValueError('captured names, portrait and scenario source paths required')
    paths = {ident: resource_paths[ident] for ident in ids}
    if any(type(path) is not str for path in paths.values()):
        raise ValueError('explicit captured relative source path strings required')
    if len(set(paths.values())) != len(paths):
        raise ValueError('the three captured portrait input authorities must be distinct')
    sources = _PortraitMembers(source_files=resource_files)
    documents = {ident: sources.json_or_none(path) for ident, path in paths.items()}
    if any(type(document) is not dict for document in documents.values()):
        raise ValueError('all three captured portrait input documents must exist')
    catalog = build_catalog(documents['dialogue_text'], documents['portrait_graphics'],
        documents['scenario_build'], source_files=resource_files)
    catalog['inputs'] = dict(names_source=paths['dialogue_text'],
        portrait_source=paths['portrait_graphics'], record_authority=paths['scenario_build'],
        source_root='.')
    catalog['member_paths_relative_to'] = 'this edition root'
    catalog['derived_from_actual_captured_resource_files'] = True
    if len(json_bytes(catalog)) > 20_000_000:
        raise ValueError('local portrait metadata exceeds the existing explicit JSON limit')
    guide = '\n'.join(('# 人物头像的本地编辑入口', '',
        'OFFICER_PORTRAITS.json 是从本版实际资源快照生成的查找索引，不是另一份游戏输入。',
        '其中所有路径都相对本版根目录；不依赖原工作区、旧 build 或另一个版本。', '',
        '在 officers 中按 name.text 或 officer_record_id 查找；未知字形转义保持原样。',
        'portrait.layout_file 指向布局 JSON，portrait.palette.file 指向调色 JSON；',
        'tile_groups 的 tile_ref 对应 shared_tiles 中的本地 PNG。共享 PNG 可能影响多人。', '',
        '唯一姓名源：`' + paths['dialogue_text'] + '`。',
        '唯一头像图源：`' + paths['portrait_graphics'] + '`。',
        '唯一剧本记录源：`' + paths['scenario_build'] + '`。', '',
        '只修改这些实际资源／成员，不把索引内容当作可编辑参数备份。资源变化后，',
        '可重新生成衍生索引；索引不参与编码，也不会覆盖或补造缺失资源。',
        'selector-layout 源码连接不等于画中人物识别或自然显示通过；unknown 仍保留。',
        '详细合同见 tools/high_level_rom/README_PORTRAIT_CATALOG.md。', ''))
    return catalog, guide


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--names-source', type=Path, required=True)
    parser.add_argument('--portrait-source', type=Path, required=True)
    parser.add_argument('--record-authority', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    from .native import fresh_output
    project = args.project_root.resolve(strict=True)
    output = fresh_output(args.output)
    if (not output.is_relative_to(project / 'build') or output == project / 'build'
            or not output.parent.is_dir() or output.suffix != '.json'):
        raise ValueError('explicit fresh JSON file under project build required')
    result = build_catalog(_load(args.names_source), _load(args.portrait_source),
        _load(args.record_authority), source_root=args.source_root)
    result['inputs'] = {name:str(getattr(args, name).resolve(strict=True)) for name in
        ('names_source', 'portrait_source', 'record_authority', 'source_root')}
    raw = json_bytes(result)
    if len(raw) > 20_000_000:
        raise ValueError('portrait metadata exceeds the explicit JSON limit')
    with output.open('xb') as destination:
        destination.write(raw)
    linked = sum(row['portrait']['status'] == 'confirmed_selector_layout_link'
        for row in result['officers'])
    print(json.dumps(dict(output=str(output), officers=len(result['officers']),
        confirmed_selector_links=linked, unknown_links=len(result['officers']) - linked,
        shared_png_refs=len(result['shared_tiles']), metadata_bytes=len(raw),
        PNG_read=False, original_ROM_read=False, game_or_native_run=False,
        strict_acceptance_added=0), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
