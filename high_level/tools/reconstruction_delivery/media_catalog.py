"""Build an editable asset index using publication JSON metadata only.

No image, audio, ROM, source codec or game module is imported or read. The
catalog preserves declared identities/confidence without inventing character
names, image roles, CRAM colours, playable audio or successful round trips.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import stat


MANIFEST_FORMAT = 'g5510-build-connected-media-publication-v1'
INDEX_FORMAT = 'g5510-editable-media-catalog-v1'
MAX_MANIFEST_BYTES = 20_000_000
MAX_INDEX_BYTES = 4_000_000
MAX_MARKDOWN_BYTES = 2_000_000
GROUPS = {'images':'图像', 'audio':'声音定义与参数', 'data':'数据', 'unknown':'未识别角色'}
RESOURCE_FIELDS = {'id', 'source', 'role', 'external_graph', 'members',
    'physical_spans', 'confidence', 'physical_BYTES'}
MEMBER_FIELDS = {'id', 'file', 'codec', 'width', 'height', 'bit_order', 'source_locator'}


class CatalogError(ValueError):
    """Publication metadata cannot be represented honestly or safely."""


def _relative(value):
    if type(value) is not str or not value or '\\' in value:
        raise CatalogError('plain manifest-relative media path required')
    parts = PurePosixPath(value).parts
    if (not parts or '/'.join(parts) != value or value.startswith('/')
            or any(part in ('.', '..') or part.endswith('.')
                or re.fullmatch(r'[A-Za-z0-9_.-]+', part) is None
                or re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part)
                for part in parts)):
        raise CatalogError('canonical portable manifest-relative media path required')
    return value


def _text(value, name):
    if type(value) is not str or not value or len(value) > 1024:
        raise CatalogError('bounded explicit ' + name + ' required')
    return value


def _json_clone(value):
    try:
        encoded = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
        return json.loads(encoded)
    except (ValueError, TypeError, RecursionError) as error:
        raise CatalogError('finite JSON metadata required') from error


def _encoded_index(index):
    raw = (json.dumps(index, ensure_ascii=False, allow_nan=False, separators=(',', ':')) + '\n').encode('utf-8')
    if len(raw) > MAX_INDEX_BYTES:
        raise CatalogError('complete media index exceeds the explicit4MB guide budget')
    return raw


def _display(value):
    # JSON escaping keeps arbitrary declared text on one Markdown line. The
    # two HTML characters are escaped instead of interpreted as guide markup.
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;')


def _locator(value):
    return '$' + ''.join('[' + _display(part) + ']' for part in value)


def _markdown(index):
    lines = ['# 可编辑素材索引', '',
        '本指南只根据导出清单生成；没有读取图片、音频或原 ROM，也没有重新编码或验收素材。', '',
        '所有文件路径相对于 `asset-source-manifest.json` 所在的素材根，不是相对于本指南目录。',
        '完整“文件 → 资源 → 原字段定位”在 `ASSET_INDEX.json` 的 `files` 与 `resources` 中；',
        '下文逐资源列出概况与最多3个成员示例，避免数千个像素块淹没人工指南。', '',
        'PNG 保存的是原像素索引；显示用灰度 palette 不等于游戏 CRAM。调色板／布局／压缩控制仍以各自 JSON 来源为准。',
        '声音组包含曲目、音色、包络、事件等清单所声明的可编辑来源；JSON 参数不是已经渲染／听验的 WAV。',
        '资源身份与字段语义的 confidence 原样保留；未给出的人物、背景或物件名称不在此猜测。', '',
        '## 概况', '',
        '- 资源：' + str(index['counts']['resources']),
        '- 文件：' + str(index['counts']['files']),
        '- 外置成员：' + str(index['counts']['members']),
        '- 清单自身声明的状态：' + _display(index['manifest_declarations']), '']
    for group, heading in GROUPS.items():
        ids = index['groups'][group]
        lines.extend(['## ' + heading, ''])
        if not ids:
            lines.extend(['无此类清单声明。', ''])
            continue
        for ident in ids:
            resource = index['resources'][ident]
            lines.extend(['### ' + _display(ident), '',
                '- 来源：`' + resource['source'] + '`',
                '- 清单角色：' + _display(resource['role']),
                '- 置信度原文：' + _display(resource['confidence']),
                '- 物理范围（原清单，半开区间）：' + _display(resource['physical_spans']),
                '- 外置成员：' + str(resource['member_count'])])
            for path, member in resource['_examples']:
                dimensions = '' if member['width'] is None else '；' + str(member['width']) + '×' + str(member['height'])
                lines.append('- 成员示例：`' + path + '`；codec=' + _display(member['codec'])
                    + dimensions + '；原字段 `' + _locator(member['source_locator']) + '`')
            if resource['member_count'] > len(resource['_examples']):
                lines.append('- 其余成员的完整字段定位见 `ASSET_INDEX.json`，没有从机器索引省略。')
            if not resource['member_count']:
                lines.append('- 本包没有外置成员；编辑入口就是上面的完整 typed JSON，不虚构 PNG／音频文件。')
            lines.append('')
    lines.extend(['## 修改时的边界', '',
        '先按文件键定位资源，再按该成员 `source_locator` 找回逻辑字段。locator 是原逻辑数据中的路径，',
        '不是把 PNG 当成 JSON 的路径，也不意味着可以任意改图块尺寸、目录、压缩拓扑或共享引用。',
        '本工具不重命名、不搬移、不复制媒体；改变结构或共享素材可能影响多个实际使用处。',
        '索引与指南不构成“修改已生效”“构建通过”或“与原版完全一致”的验收证据。', ''])
    markdown = '\n'.join(lines)
    if len(markdown.encode('utf-8')) > MAX_MARKDOWN_BYTES:
        raise CatalogError('complete resource guide exceeds the explicit2MB budget')
    return markdown


def catalog_from_manifest(manifest: dict) -> tuple[dict, str]:
    """Return a JSON-compatible index and bounded guide, without file reads."""
    if type(manifest) is not dict or manifest.get('format') != MANIFEST_FORMAT:
        raise CatalogError('actual build-connected media publication manifest required')
    rows = manifest.get('resources')
    if type(rows) is not list or not 1 <= len(rows) <= 512:
        raise CatalogError('bounded explicit resource declaration list required')
    if type(manifest.get('registered_resources')) is not int or manifest['registered_resources'] != len(rows):
        raise CatalogError('actual registered resource count differs')
    index = dict(format=INDEX_FORMAT, manifest_format=MANIFEST_FORMAT,
        paths_relative_to='asset-source-manifest.json parent directory',
        resource_order=[], groups={group:[] for group in GROUPS}, resources={}, files={},
        counts=dict(resources=len(rows), files=0, members=0),
        manifest_declarations={key:_json_clone(manifest[key]) for key in (
            'edited_display_audio_proven', 'all_asset_identities_known', 'final_delivery') if key in manifest},
        limits=['metadata-only navigation, not asset identity discovery or build/behavior acceptance',
            'indexed PNG display palette is not a CRAM authority',
            'audio definitions/events are not claimed to be rendered PCM'])
    seen_paths = set()

    def add_file(path, entry):
        path = _relative(path)
        if path.casefold() in seen_paths:
            raise CatalogError('competing case-insensitive manifest file authority: ' + path)
        seen_paths.add(path.casefold())
        index['files'][path] = entry

    for row in rows:
        if type(row) is not dict or set(row) != RESOURCE_FIELDS:
            raise CatalogError('complete actual resource publication row required')
        ident, source, role = _text(row['id'], 'resource ID'), _relative(row['source']), _text(row['role'], 'declared role')
        if ident in index['resources']:
            raise CatalogError('duplicate resource identity: ' + ident)
        members = row['members']
        if (type(members) is not list or len(members) > 50000
                or type(row['external_graph']) is not bool or row['external_graph'] != bool(members)):
            raise CatalogError('actual finite external member declaration differs')
        spans = row['physical_spans']
        if (type(spans) is not list or any(type(span) not in (list, tuple) or len(span) != 2
                or any(type(value) is not int for value in span) or not 0 <= span[0] < span[1] <= 0x100000 for span in spans)
                or type(row['physical_BYTES']) is not int
                or row['physical_BYTES'] != sum(end - start for start, end in spans)):
            raise CatalogError('actual declared physical resource geometry differs')
        group = role if role in ('images', 'audio', 'data') else 'unknown'
        resource = {key:_json_clone(value) for key,value in row.items() if key != 'members'}
        resource.update(group=group, member_count=len(members), _examples=[])
        index['resources'][ident] = resource
        index['resource_order'].append(ident)
        index['groups'][group].append(ident)
        add_file(source, dict(resource_id=ident, kind='resource_source', source_locator=None))
        seen_member_ids = set()
        for member in members:
            if type(member) is not dict or set(member) != MEMBER_FIELDS:
                raise CatalogError('complete actual external member metadata required')
            member_id = _text(member['id'], 'member ID')
            if member_id in seen_member_ids:raise CatalogError('duplicate per-resource member ID')
            seen_member_ids.add(member_id)
            _text(member['codec'], 'declared member codec')
            if (not (member['width'] is None and member['height'] is None)
                    and not (type(member['width']) is int and type(member['height']) is int
                        and 1 <= member['width'] <= 65536 and 1 <= member['height'] <= 65536)):
                raise CatalogError('explicit paired member dimensions required')
            if member['bit_order'] is not None and member['bit_order'] not in ('msb', 'lsb'):
                raise CatalogError('actual declared bit order required')
            locator = member['source_locator']
            if type(locator) is not list or len(locator) > 128 or any(type(part) not in (str, int) for part in locator):
                raise CatalogError('actual logical-field locator list required')
            entry = {key:_json_clone(value) for key,value in member.items() if key != 'file'}
            entry.update(resource_id=ident, kind='external_member')
            path = _relative(member['file'])
            add_file(path, entry)
            if len(resource['_examples']) < 3:resource['_examples'].append((path, entry))
            index['counts']['members'] += 1
    index['counts']['files'] = len(index['files'])
    markdown = _markdown(index)
    for resource in index['resources'].values():
        del resource['_examples']
    _encoded_index(index)
    return index, markdown


def _reparse(path):
    return (path.is_symlink() or getattr(path, 'is_junction', lambda: False)()
        or path.exists() and bool(getattr(path.stat(), 'st_file_attributes', 0)
            & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0)))


def _manifest(path):
    path = path.absolute()
    if path.suffix.lower() != '.json' or any(_reparse(value) for value in (path, *path.parents)) or not path.is_file():
        raise CatalogError('ordinary explicit manifest file required')
    if not 0 < path.stat().st_size <= MAX_MANIFEST_BYTES:
        raise CatalogError('bounded media publication manifest required')
    with path.open('rb') as stream:raw = stream.read(MAX_MANIFEST_BYTES + 1)
    if len(raw) > MAX_MANIFEST_BYTES:raise CatalogError('manifest grew past explicit budget')
    def pairs(rows):
        result = {}
        for key,value in rows:
            if key in result:raise CatalogError('duplicate manifest JSON key')
            result[key] = value
        return result
    def invalid(value):raise CatalogError('nonfinite manifest number: ' + value)
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=invalid)


def _fresh(path):
    path = path.absolute()
    raw = str(path)
    if raw.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in raw[2:]:
        raise CatalogError('UNC/device/alternate-stream output refused')
    if any(_reparse(value) for value in (path, *path.parents)):
        raise CatalogError('output through a reparse point refused')
    path = path.resolve(strict=False)
    if path.exists() or path == Path(path.anchor):
        raise CatalogError('a new dedicated guide directory is required; overwriting is refused')
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    target = _fresh(args.output)
    index, markdown = catalog_from_manifest(_manifest(args.manifest))
    payloads = {'ASSET_INDEX.json':_encoded_index(index), 'ASSETS.md':markdown.encode('utf-8')}
    target.mkdir(parents=True)
    try:
        for name, raw in payloads.items():
            with (target / name).open('xb') as stream:stream.write(raw)
    except OSError as error:
        raise CatalogError('guide publication incomplete; partial new output retained, not accepted: ' + str(target)) from error
    print(json.dumps(dict(status='metadata_guides_written_not_verified', output=str(target),
        **index['counts'], guide_bytes=sum(map(len, payloads.values())),
        media_files_read=0, media_files_copied=0, native_run=False, test_run=False), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
