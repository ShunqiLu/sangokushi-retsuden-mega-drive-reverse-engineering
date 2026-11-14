"""Read lossless external PNG/JSON authorities for registered typed resources.

The small file graph is transport, not a second pixel/audio payload. Decoded
indices become the existing typed fields and are passed to their normal codec.
No reference ROM, prior JSON, cached encoding, creative quantization or hash
is read. A PNG's display palette is not the game's CRAM colour authority.
"""
from __future__ import annotations

from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import re

from PIL import Image
from .media_word_rle import resolve_title_tiles
from .readable_text import FORMAT as READABLE_TEXT_FORMAT, from_readable
from .scenario_sources import FORMAT as NAMED_SCENARIO_FORMAT, from_named as scenario_from_named
from .ai_policy_sources import (FORMAT as NAMED_AI_CUTOFF_FORMAT,
    RESOURCE_ID as AI_CUTOFF_RESOURCE_ID, from_named as ai_cutoffs_from_named)
from .ai_selection_sources import (FORMAT as NAMED_AI_SELECTION_FORMAT,
    RESOURCE_ID as AI_SELECTION_RESOURCE_ID, from_named as ai_selection_from_named)
from .audio_sequence_sources import (FORMAT as NAMED_AUDIO_SEQUENCE_FORMAT,
    RESOURCE_ID as AUDIO_SEQUENCE_RESOURCE_ID, from_named as audio_sequences_from_named)


FORMAT = 'g5510-owned-external-media-graph-v1'
REFERENCE = '$owned_media'
MAX_JSON = 20_000_000
MAX_PNG = 1_000_000


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def loads(raw: bytes):
    if type(raw) is not bytes or len(raw) > MAX_JSON:
        raise ValueError('bounded immutable UTF8 JSON source required')
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError('duplicate JSON source key: ' + key)
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('nonfinite source number: ' + value)
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=invalid)


def _member_parts(relative: str) -> tuple[str, ...]:
    if type(relative) is not str or '\\' in relative:
        raise ValueError('plain registered relative media path required')
    parts = PurePosixPath(relative).parts
    if (not parts or '/'.join(parts) != relative or relative.startswith('/') or
            any(part in ('.', '..') or part.endswith('.') or not re.fullmatch(r'[A-Za-z0-9_.-]+', part) or
                re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part)
                for part in parts)):
        raise ValueError('unsafe media member path')
    return parts


def member_path(root: Path, relative: str) -> Path:
    """Resolve one declared ordinary member without following reparse points."""
    parts = _member_parts(relative)
    root = root.absolute()
    path = root.joinpath(*parts)
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ValueError('media member through reparse point refused')
    path = path.resolve(strict=False)
    if not path.is_relative_to(root.resolve(strict=True)):
        raise ValueError('media member leaves explicit own source root')
    return path


def _read(path: Path, maximum: int) -> bytes:
    if not path.is_file() or path.stat().st_size > maximum:
        raise ValueError('bounded ordinary media source file required: ' + str(path))
    with path.open('rb') as stream:
        raw = stream.read(maximum + 1)
    if len(raw) > maximum:
        raise ValueError('media source grew past format limit')
    return raw


def indexed_png(pixels: list[int], width: int, height: int, bits: int) -> bytes:
    """Encode exact indices with neutral colours; never infer a CRAM palette."""
    if (type(width) is not int or type(height) is not int or
            not 1 <= width <= 32 or not 1 <= height <= 32 or bits not in (1, 4) or
            type(pixels) is not list or len(pixels) != width * height or
            any(type(value) is not int or not 0 <= value < 1 << bits for value in pixels)):
        raise ValueError('fixed one/four-bit pixel geometry required')
    picture = Image.frombytes('P', (width, height), bytes(pixels))
    maximum = (1 << bits) - 1
    picture.putpalette(bytes(channel for index in range(256)
                             for channel in (min(index, maximum) * 255 // maximum,) * 3))
    stream = BytesIO()
    picture.save(stream, format='PNG', bits=bits, optimize=False)
    return stream.getvalue()


def png_pixels(raw: bytes, width: int, height: int, bits: int) -> list[int]:
    if (type(raw) is not bytes or len(raw) > MAX_PNG or
            type(width) is not int or type(height) is not int or
            not 1 <= width <= 32 or not 1 <= height <= 32 or bits not in (1, 4)):
        raise ValueError('bounded fixed indexed PNG geometry required')
    with Image.open(BytesIO(raw)) as picture:
        if (picture.format != 'PNG' or picture.mode != 'P' or picture.size != (width, height) or
                getattr(picture, 'n_frames', 1) != 1 or 'transparency' in picture.info):
            raise ValueError('single opaque P-mode PNG with original dimensions required')
        pixels = list(picture.tobytes())
    if len(pixels) != width * height or any(value >= 1 << bits for value in pixels):
        raise ValueError('pixel index exceeds original bit width')
    return pixels


def describe(wrapper: dict, resource_id: str) -> list[dict]:
    """Validate the finite transport declaration; used by staging as well."""
    if type(wrapper) is not dict or set(wrapper) != {
            'format', 'resource_id', 'source_format', 'graph', 'members', 'limits'}:
        raise ValueError('exact external-media source declaration required')
    if wrapper['format'] != FORMAT or wrapper['resource_id'] != resource_id:
        raise ValueError('external-media format/registered resource identity differs')
    if type(wrapper['source_format']) is not str or type(wrapper['members']) is not list:
        raise ValueError('typed source format and fixed member list required')
    ids, paths = set(), set()
    for row in wrapper['members']:
        if type(row) is not dict or set(row) != {'id', 'file', 'codec', 'width', 'height', 'bit_order', 'source_locator'}:
            raise ValueError('fixed media member declaration differs')
        if (type(row['id']) is not str or not row['id'] or row['id'] in ids or
                type(row['file']) is not str or row['file'].casefold() in paths or
                type(row['source_locator']) is not list or
                any(type(key) not in (str, int) for key in row['source_locator'])):
            raise ValueError('unique member ID/file/typed locator required')
        _member_parts(row['file'])
        ids.add(row['id']); paths.add(row['file'].casefold())
        codec = row['codec']
        if codec in ('typed_json', 'word_rle_commands', 'tile_word_rle_commands'):
            if any(row[key] is not None for key in ('width', 'height', 'bit_order')) or not row['file'].endswith('.json'):
                raise ValueError('typed media JSON metadata differs')
        elif codec in ('tile4_rows', 'tile4_pixels', 'mono_rows', 'word_pixels', 'pixel_pair4'):
            if (type(row['width']) is not int or type(row['height']) is not int or
                    not 1 <= row['width'] <= 32 or not 1 <= row['height'] <= 32 or
                    not row['file'].endswith('.png') or row['bit_order'] not in ('msb', 'lsb') or
                    codec in ('tile4_rows', 'tile4_pixels') and (row['width'], row['height'], row['bit_order']) != (8, 8, 'msb') or
                    codec == 'word_pixels' and (row['width'], row['bit_order']) != (4, 'msb') or
                    codec == 'pixel_pair4' and (row['width'], row['height'], row['bit_order']) != (2, 1, 'msb')):
                raise ValueError('indexed pixel geometry/order differs')
        else:
            raise ValueError('unregistered external-media codec')
    return wrapper['members']


def resolve(wrapper: dict, root: Path, resource_id: str) -> dict:
    """Read every sole member authority once; reject unused/duplicate references."""
    declarations = {row['id']: row for row in describe(wrapper, resource_id)}
    used = set()
    def visit(value):
        if type(value) is dict and REFERENCE in value:
            if set(value) != {REFERENCE} or type(value[REFERENCE]) is not str:
                raise ValueError('exact media reference required')
            ident = value[REFERENCE]
            if ident not in declarations or ident in used:
                raise ValueError('unknown or duplicate media edit authority')
            used.add(ident)
            row = declarations[ident]
            path = member_path(root, row['file'])
            if row['codec'] == 'typed_json':
                return visit(loads(_read(path, MAX_JSON)))
            if row['codec'] == 'tile_word_rle_commands':
                return resolve_title_tiles(loads(_read(path, MAX_JSON)), visit, declarations, reference_key=REFERENCE)
            if row['codec'] == 'word_rle_commands':
                # The PNG strip owns one decoded BE WORD per original command;
                # controls retain the original literal/repeat partition and cost.
                source = loads(_read(path, MAX_JSON))
                if (type(source) is not dict or set(source) != {'format', 'controls', 'word_strips'} or
                        source['format'] != 'g5510-word-rle-command-pixels-v1' or
                        type(source['controls']) is not list or not 1 <= len(source['controls']) <= 4096 or
                        type(source['word_strips']) is not list or not source['word_strips']):
                    raise ValueError('fixed word RLE control/pixel source required')
                if any(type(reference) is not dict or set(reference) != {REFERENCE} or
                       type(reference[REFERENCE]) is not str or
                       reference[REFERENCE] not in declarations or
                       declarations[reference[REFERENCE]]['codec'] != 'word_pixels'
                       for reference in source['word_strips']):
                    raise ValueError('each compressed pixel strip must reference its sole PNG authority')
                strips = visit(source['word_strips'])
                if any(type(strip) is not list or not 1 <= len(strip) <= 32 or
                       any(type(word) is not int or not 0 <= word <= 65535 for word in strip) for strip in strips):
                    raise ValueError('complete WORD pixel strips required')
                words = [word for strip in strips for word in strip]
                if len(words) != len(source['controls']):
                    raise ValueError('one sole pixel WORD per compression command required')
                commands = []
                for control, word in zip(source['controls'], words):
                    if type(control) is not dict:
                        raise ValueError('RLE control object required')
                    if control.get('op') == 'literal' and set(control) == {'op'}:
                        pass
                    elif (control.get('op') == 'repeat' and set(control) == {'op', 'count'} and
                          type(control['count']) is int and 2 <= control['count'] <= 256):
                        pass
                    else:
                        raise ValueError('original literal/repeat control required, no pixel backup')
                    commands.append(dict(control, word=word))
                return commands
            bits = 4 if row['codec'] in ('tile4_rows', 'tile4_pixels', 'word_pixels', 'pixel_pair4') else 1
            pixels = png_pixels(_read(path, MAX_PNG), row['width'], row['height'], bits)
            if bits == 4:
                if row['codec'] == 'pixel_pair4':
                    return pixels
                if row['codec'] == 'tile4_pixels':
                    return [pixels[index:index + 8] for index in range(0, 64, 8)]
                if row['codec'] == 'word_pixels':
                    return [sum(pixel << ((3 - column) * 4) for column, pixel in enumerate(pixels[index:index + 4]))
                            for index in range(0, len(pixels), 4)]
                return [''.join(f'{pixel:X}' for pixel in pixels[index:index + 8]) for index in range(0, 64, 8)]
            result = []
            for index in range(0, len(pixels), row['width']):
                result.append(sum(pixel << (column if row['bit_order'] == 'lsb' else row['width'] - column - 1)
                                  for column, pixel in enumerate(pixels[index:index + row['width']])))
            return result
        if type(value) is dict:
            return {key: visit(inner) for key, inner in value.items()}
        if type(value) is list:
            return [visit(inner) for inner in value]
        return value
    fields = visit(wrapper['graph'])
    if used != set(declarations) or type(fields) is not dict or fields.get('format') != wrapper['source_format']:
        raise ValueError('complete typed media graph/format required')
    return fields


def resolve_source_document(fields: dict, root: Path | None, resource_id: str) -> dict:
    """Decode one captured source document; no second read or typed fallback."""
    if type(fields) is not dict:
        raise ValueError('registered typed resource object required')
    if fields.get('format') == FORMAT:
        if root is None:
            raise ValueError('external media requires explicit own source root; no fallback')
        # Resolve the sole external member graph first. A named audio graph
        # uses the same paths/member authority as its typed predecessor; only
        # the resulting complete document is converted for the normal codec.
        fields = resolve(fields, root, resource_id)
    if fields.get('format') == READABLE_TEXT_FORMAT:
        if resource_id != 'dialogue_text':
            raise ValueError('readable main text can only supply its registered dialogue resource')
        return from_readable(fields)
    if fields.get('format') == NAMED_SCENARIO_FORMAT:
        if resource_id != 'scenario_build':
            raise ValueError('named scenario source can only supply its registered scenario resource')
        return scenario_from_named(fields)
    if fields.get('format') == NAMED_AI_CUTOFF_FORMAT:
        if resource_id != AI_CUTOFF_RESOURCE_ID:
            raise ValueError('named AI cutoff source can only supply its registered cutoff-pair resource')
        return ai_cutoffs_from_named(fields)
    if fields.get('format') == NAMED_AI_SELECTION_FORMAT:
        if resource_id != AI_SELECTION_RESOURCE_ID:
            raise ValueError('named AI candidate gates can only supply their registered selection resource')
        return ai_selection_from_named(fields)
    if fields.get('format') == NAMED_AUDIO_SEQUENCE_FORMAT:
        if resource_id != AUDIO_SEQUENCE_RESOURCE_ID:
            raise ValueError('named audio commands can only supply their registered audio resource')
        return audio_sequences_from_named(fields)
    return fields


def load_source(path: Path, root: Path | None, resource_id: str) -> dict:
    """Plain registered JSON remains valid; external graphs require own root."""
    return resolve_source_document(loads(_read(path, MAX_JSON)), root, resource_id)
