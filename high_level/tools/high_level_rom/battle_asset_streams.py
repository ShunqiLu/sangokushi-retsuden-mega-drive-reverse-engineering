"""Shared fixed-slot battle tile and map stream access for the asset editors."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tools.battle_graphics import battle_graphics as battle
from tools.graphics_build import rle_fields as rle

from . import media_sources as media
from .native import fresh_output


RESOURCE_ID = 'battle_graphics'
SOURCE = 'resources/images/battle_graphics.json'


@dataclass(frozen=True)
class WordStrip:
    file: str
    first_command: int
    end_command: int


@dataclass(frozen=True)
class WordStream:
    stream: battle.Stream
    marker: int
    commands: tuple[tuple[int, int], ...]  # output count, stored word
    strips: tuple[WordStrip, ...]
    encoded: bytes
    decoded: bytes
    typed_fields_file: str | None = None


@dataclass(frozen=True)
class BattleAssets:
    streams: tuple[WordStream, ...]
    directories: tuple[tuple[str, tuple[str, ...]], ...]


def read_json(root: Path, relative: str):
    return media.loads(media._read(media.member_path(root, relative), media.MAX_JSON))


def _member(reference, declarations, locator, codec):
    if type(reference) is not dict or set(reference) != {media.REFERENCE}:
        raise ValueError('expected one registered battle asset member')
    member = declarations.get(reference[media.REFERENCE])
    if member is None or member['source_locator'] != locator or member['codec'] != codec:
        raise ValueError('battle asset member does not match its declared stream and role')
    return member


def _stream(root, wrapper, declarations, source, stream_id):
    stream = battle.BY_ID[stream_id]
    index = battle.STREAMS.index(stream)
    resolved = source['streams'][index]
    if {key: value for key, value in resolved.items() if key != 'fields'} != battle.metadata(stream):
        raise ValueError('battle stream identity, extent or byte order differs')
    fields = resolved['fields']
    encoded, decoded = rle.pack_word(fields, stream.order, stream.words)
    if len(encoded) != stream.end - stream.start:
        raise ValueError('battle stream no longer fits its original slot')

    commands = tuple((row.get('count', 1), row['word']) for row in fields['commands'])
    locator = ['streams', index, 'fields']
    registered_fields = wrapper['graph']['streams'][index]['fields']
    if stream.vram is None:
        member = _member(registered_fields, declarations, locator, 'typed_json')
        if read_json(root, member['file']) != fields:
            raise ValueError('the map needs one direct typed JSON authority')
        return WordStream(stream, fields['marker'], commands, (), encoded, decoded, member['file'])

    locator.append('commands')
    reference = registered_fields['commands']
    member = _member(reference, declarations, locator, 'word_rle_commands')
    controls = read_json(root, member['file'])
    strips = []
    next_command = 0
    for reference in controls['word_strips']:
        member = _member(reference, declarations, [*locator, next_command, 'word'], 'word_pixels')
        end_command = next_command + member['height']
        strips.append(WordStrip(member['file'], next_command, end_command))
        next_command = end_command
    if next_command != len(fields['commands']):
        raise ValueError('declared asset strips do not exactly cover the original commands')
    return WordStream(stream, fields['marker'], commands, tuple(strips), encoded, decoded)


def load_assets(root: Path, stream_ids: tuple[str, ...]) -> BattleAssets:
    """Resolve one edition's actual asset graph without an original ROM."""
    if (not stream_ids or any(type(stream_id) is not str or stream_id not in battle.BY_ID for stream_id in stream_ids)
            or len(set(stream_ids)) != len(stream_ids)):
        raise ValueError('choose distinct registered battle map or tile streams')
    wrapper = read_json(root, SOURCE)
    declarations = {row['id']: row for row in media.describe(wrapper, RESOURCE_ID)}
    source = media.resolve(wrapper, root, RESOURCE_ID)
    if source['format'] != battle.FORMAT or len(source['streams']) != len(battle.STREAMS):
        raise ValueError('complete original battle resource catalog required')
    directories = []
    for row, (expected, _) in zip(source['directories'], battle.DIRECTORIES, strict=True):
        if (type(row) is not dict or set(row) != {'id', 'targets'} or row['id'] != expected
                or type(row['targets']) is not list or len(row['targets']) != 4
                or any(type(target) is not str or target not in battle.BY_ID or battle.BY_ID[target].vram is not None
                       for target in row['targets'])):
            raise ValueError('battle map directory differs from the registered resource structure')
        directories.append((expected, tuple(row['targets'])))
    return BattleAssets(tuple(_stream(root, wrapper, declarations, source, stream_id) for stream_id in stream_ids),
                        tuple(directories))


def nibbles(word: int) -> tuple[int, int, int, int]:
    return tuple((word >> shift) & 15 for shift in (12, 8, 4, 0))


def word_replacements(asset: WordStream, words: tuple[int, ...]) -> tuple[dict[str, bytes], dict]:
    """Return only changed registered members, retaining the exact controls and slot."""
    if len(words) != asset.stream.words or any(type(word) is not int or not 0 <= word <= 65535 for word in words):
        raise ValueError('complete decoded WORDs for the original stream are required')
    commands, changed_words = [], set()
    next_word = 0
    for index, (count, before) in enumerate(asset.commands):
        end_word = next_word + count
        after = words[next_word]
        if any(word != after for word in words[next_word:end_word]):
            raise ValueError(f'command {index} shares decoded WORDs {next_word}..{end_word - 1}; edit all copies alike')
        if after != before:
            changed_words.add(index)
        if count == 1 and after.to_bytes(2, asset.stream.order)[0] == asset.marker:
            raise ValueError(f'command {index} would make a literal start with the original escape byte')
        commands.append(dict(op='literal', word=after) if count == 1 else dict(op='repeat', word=after, count=count))
        next_word = end_word
    encoded, decoded = rle.pack_word(dict(marker=asset.marker, commands=commands), asset.stream.order, asset.stream.words)
    if len(encoded) != len(asset.encoded) or decoded != b''.join(word.to_bytes(2, 'big') for word in words):
        raise ValueError('edited stream cannot preserve the original slot and command partition')

    files = {}
    if changed_words and asset.typed_fields_file is not None:
        files[asset.typed_fields_file] = media.json_bytes(dict(marker=asset.marker, commands=commands))
    for strip in asset.strips:
        start, end = strip.first_command, strip.end_command
        if any(index in changed_words for index in range(start, end)):
            pixels = [pixel for command in commands[start:end] for pixel in nibbles(command['word'])]
            files[strip.file] = media.indexed_png(pixels, 4, end - start, 4)
    edits = [dict(address=asset.stream.start + index, before=before, after=after)
             for index, (before, after) in enumerate(zip(asset.encoded, encoded)) if before != after]
    return files, dict(stream=asset.stream.id, replacement_files=list(files),
                       changed_commands=sorted(changed_words), physical_byte_changes=edits)


def publish_files(source: Path, output: Path, files: dict[str, bytes]) -> Path:
    target = fresh_output(output)
    if target.is_relative_to(source.resolve(strict=True)) or not target.parent.is_dir():
        raise ValueError('choose a fresh directory outside the source edition with an existing parent')
    target.mkdir()
    for name, raw in files.items():
        path = media.member_path(target, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
    return target
