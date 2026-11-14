"""ROM-independent editable main dialogue and fixed officer/city names.

Manual glyph readings are source labels, not evidence of Big5/Unicode bytes.
Uncertain, duplicate, control and noncanonical words keep exact escapes. The
normal registered dialogue encoder remains the final layout authority.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import copy
import json
from pathlib import Path
import re

from .resource_adapters_records import _dialogue_token


FORMAT = 'g5510-owned-main-text-unicode-source-v1'
EDIT_FORMAT = 'g5510-main-text-record-edits-v1'
OPEN, CLOSE = '\u27e6', '\u27e7'
ESCAPE = re.compile(r'\u27e6([0-9A-F]{4})\u27e7')
UNKNOWN = '\ufffd'
COLLECTIONS = (('records', 275, 'main'), ('officer_names', 256, 'name'),
               ('city_names', 40, 'name'))
MAX_JSON_BYTES = 20_000_000


def _keys(value, names):
    if type(value) is not dict or set(value) != set(names):
        raise ValueError('exact editable text source fields required')


def _list(value, count):
    if type(value) is not list or len(value) != count:
        raise ValueError('fixed physical text/glyph count differs')
    return value


def _integer(value, maximum, label):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError('strict unsigned ' + label + ' outside its physical width')
    return value


def parse_manual_sources(documents):
    """The historical two-document manual grammar, without ROM or hashes."""
    _list(documents, 2)
    result = []
    for doc, begin, end in zip(documents, (0, 512), (512, 1034)):
        _keys(doc, ('schema_version', 'evidence', 'pages', 'overrides'))
        if type(doc['schema_version']) is not int or doc['schema_version'] != 1:
            raise ValueError('transcription schema changed')
        if doc['evidence'] != 'manual_numbered_bitmap_review':
            raise ValueError('unsupported evidence type')
        firsts = list(range(begin, end, 64))
        _list(doc['pages'], len(firsts))
        if type(doc['overrides']) is not dict:
            raise ValueError('overrides must be an object')
        for page, first in zip(doc['pages'], firsts):
            _keys(page, ('first_glyph', 'rows'))
            if type(page['first_glyph']) is not int or page['first_glyph'] != first:
                raise ValueError('page identity/order changed')
            count = min(64, end - first)
            _list(page['rows'], (count + 7) // 8)
            chars = []
            for row_no, row in enumerate(page['rows']):
                if type(row) is not str or len(row) != min(8, count - row_no * 8):
                    raise ValueError('transcription row width changed')
                for char in row:
                    if char in (OPEN, CLOSE) or ord(char) < 32 or 0xD800 <= ord(char) <= 0xDFFF:
                        raise ValueError('reserved/control/surrogate transcription character')
                    chars.append(char)
            for offset, char in enumerate(chars):
                index, key = first + offset, f'{first + offset:04x}'
                confidence = 'unknown' if char == UNKNOWN else 'confirmed'
                note = ('No reliable Unicode reading.' if char == UNKNOWN
                    else 'Manual numbered bitmap reading; not a ROM Unicode value.')
                if key in doc['overrides']:
                    item = doc['overrides'][key]
                    _keys(item, ('confidence', 'note'))
                    if item['confidence'] not in ('confirmed', 'probable', 'unknown'):
                        raise ValueError('invalid transcription confidence')
                    if type(item['note']) is not str or not item['note'].strip():
                        raise ValueError('override requires evidence note')
                    confidence, note = item['confidence'], item['note']
                if (char == UNKNOWN) != (confidence == 'unknown'):
                    raise ValueError('unknown readings must use U+FFFD, never a candidate Unicode assignment')
                result.append(dict(glyph_index=index, unicode=None if char == UNKNOWN else char,
                    confidence=confidence, note=note, source_page=first))
        if set(doc['overrides']) - {f'{index:04x}' for index in range(begin, end)}:
            raise ValueError('override outside source glyph range')
    return result


class MainTextWordCodec:
    """Unique confirmed glyph labels plus exact, non-normalizing WORD escapes."""
    def __init__(self, documents):
        self.glyphs = parse_manual_sources(documents)
        self.by_character = defaultdict(list)
        for item in self.glyphs[:1024]:
            if item['unicode'] is not None:
                self.by_character[item['unicode']].append(item)

    @staticmethod
    def glyph_word(index, context):
        if context not in ('main', 'name'):
            raise ValueError('unsupported text context')
        _integer(index, 1023, 'main glyph index')
        return ((index // 64) << 8) | (index % 64) | (0x4000 if context == 'main' else 0)

    def validate_word(self, value, context):
        if context == 'main':
            return dict(type=_dialogue_token(value), word=value)
        if context == 'name':
            _integer(value, 0x1FFF, 'name glyph')
            if _dialogue_token(value | 0x4000) != 'glyph':
                raise ValueError('name must insert a glyph')
            return dict(type='glyph', word=value)
        raise ValueError('unsupported text context')

    def plain_word(self, char, context):
        items = self.by_character.get(char, [])
        if len(items) != 1:
            raise ValueError(f'unknown or ambiguous Unicode {char!r}; use an exact word escape')
        if items[0]['confidence'] != 'confirmed':
            raise ValueError(f'probable Unicode {char!r}; use an exact word escape')
        return self.glyph_word(items[0]['glyph_index'], context)

    def decode(self, values, context='main'):
        if type(values) is not list:
            raise ValueError('word sequence must be a list')
        if context not in ('main', 'name'):
            raise ValueError('unsupported text context')
        result = []
        for value in values:
            item = self.validate_word(value, context)
            char = None
            if item['type'] == 'glyph':
                offset = (((value & 0xFF00) << 3) & 0xFFFF) | (((value & 255) << 5) & 0xFFFF)
                index = offset // 32
                row = self.glyphs[index]
                candidate = row['unicode']
                if (row['confidence'] == 'confirmed' and candidate is not None
                        and len(self.by_character[candidate]) == 1
                        and value == self.glyph_word(index, context)):
                    char = candidate
            result.append(char if char is not None else f'{OPEN}{value:04X}{CLOSE}')
        return ''.join(result)

    def encode(self, text, context='main'):
        if type(text) is not str:
            raise ValueError('text must be a string')
        if context not in ('main', 'name'):
            raise ValueError('unsupported text context')
        result, offset = [], 0
        while offset < len(text):
            char = text[offset]
            if char == OPEN:
                match = ESCAPE.match(text, offset)
                if match is None:
                    raise ValueError('escape must be exactly U+27E6, four uppercase hex digits, U+27E7')
                value, offset = int(match[1], 16), match.end()
                self.validate_word(value, context)
            else:
                if char == CLOSE:
                    raise ValueError('unmatched closing word escape')
                value, offset = self.plain_word(char, context), offset + 1
            result.append(value)
        return result


def _source_values(row, context, codec):
    if type(row) is not dict:
        raise ValueError('complete physical text record required')
    if context == 'name':
        values = row['words']
    else:
        values = []
        if type(row['tokens']) is not list:
            raise ValueError('complete main token list required')
        for token in row['tokens']:
            _keys(token, ('type', 'word'))
            if token != codec.validate_word(token['word'], 'main'):
                raise ValueError('actual main token type and WORD must agree')
            values.append(token['word'])
    if type(values) is not list or not 1 <= len(values) <= 512:
        raise ValueError('bounded nonempty physical text record required')
    return values


def to_readable(fields, glyph_sources):
    """Convert explicit typed fields to their sole editable Unicode authority."""
    if type(fields) is not dict or type(fields.get('format')) is not str or fields['format'] == FORMAT:
        raise ValueError('registered plain dialogue fields required, not another readable wrapper')
    codec = MainTextWordCodec(glyph_sources)
    names = {name for name, _, _ in COLLECTIONS}
    metadata = copy.deepcopy({key: value for key, value in fields.items() if key not in names})
    result = dict(format=FORMAT, glyph_sources=copy.deepcopy(glyph_sources), metadata=metadata)
    for name, count, context in COLLECTIONS:
        result[name] = []
        for row in _list(fields[name], count):
            if 'text' in row or 'word_count' in row:
                raise ValueError('reserved readable fields collide with original metadata')
            values = _source_values(row, context, codec)
            payload = 'tokens' if context == 'main' else 'words'
            entry = copy.deepcopy({key: value for key, value in row.items() if key != payload})
            entry.update(word_count=len(values), text=codec.decode(values, context))
            result[name].append(entry)
    return result


def _readable_words(text, word_count, name, context, codec):
    """The shared existing per-record WORD/restore/name-slot authority."""
    size = _integer(word_count, 512, 'fixed WORD count')
    values = codec.encode(text, context)
    if not size or len(values) != size:
        raise ValueError('edited text must preserve its physical WORD slot')
    if context == 'main':
        is_restore = lambda value: bool(value & 0x8000) and value & 255 == 0
        if not is_restore(values[-1]) or any(is_restore(value) for value in values[:-1]):
            raise ValueError('one final original restore control required')
    else:
        if len(values) != (3 if name == 'officer_names' else 2):
            raise ValueError('original three/two-WORD fixed name slot required')
        if name == 'officer_names' and all(value == 63 for value in values):
            raise ValueError('all-blank officer-name trim remains outside the editor domain')
    return values


def from_readable(document):
    """Restore existing fields; the normal resource encoder enforces topology."""
    names = {name for name, _, _ in COLLECTIONS}
    _keys(document, {'format', 'glyph_sources', 'metadata'} | names)
    if document['format'] != FORMAT or type(document['metadata']) is not dict:
        raise ValueError('explicit readable text format and original metadata required')
    if (names & document['metadata'].keys() or type(document['metadata'].get('format')) is not str
            or document['metadata']['format'] == FORMAT):
        raise ValueError('original typed text metadata must not duplicate text authority')
    codec = MainTextWordCodec(document['glyph_sources'])
    result = copy.deepcopy(document['metadata'])
    for name, count, context in COLLECTIONS:
        result[name] = []
        seen = set()
        for row in _list(document[name], count):
            if type(row) is not dict or 'tokens' in row or 'words' in row:
                raise ValueError('readable text is the only WORD authority')
            if type(row.get('id')) is not str or not row['id'] or row['id'] in seen:
                raise ValueError('unique stable physical text ID required')
            seen.add(row['id'])
            values = _readable_words(row.get('text'), row.get('word_count'), name, context, codec)
            restored = copy.deepcopy({key: value for key, value in row.items()
                if key not in ('text', 'word_count')})
            if context == 'main':
                restored['tokens'] = [codec.validate_word(value, context) for value in values]
            else:
                restored['words'] = values
            result[name].append(restored)
    return result


def with_text_edits(document, edits):
    """Return one fully checked batch of text edits over stable physical IDs.

    The existing readable decoder validates the complete input. Each requested
    replacement reuses its exact WORD/glyph/name grammar and retains every
    main control/fixed-bitmap WORD at the same position. Only text is replaced
    after the whole batch passes; metadata, identities and glyph sources remain
    independent copies of the original, never a second raw text authority.
    """
    if type(edits) is not list or not edits:
        raise ValueError('a nonempty explicit list of readable text edits is required')
    original = from_readable(document)
    codec = MainTextWordCodec(document['glyph_sources'])
    contexts = {name: context for name, _, context in COLLECTIONS}
    records = {name: {row['id']: (index, row) for index, row in enumerate(document[name])}
        for name in contexts}
    selected, targets = [], set()
    for edit in edits:
        _keys(edit, ('collection', 'id', 'expected_text', 'text'))
        name, ident = edit['collection'], edit['id']
        if type(name) is not str or name not in contexts:
            raise ValueError('explicit records/officer_names/city_names collection required')
        if type(ident) is not str or not ident or ident not in records[name]:
            raise ValueError('edit must name an existing stable physical text id, not a list ordinal')
        target = name, ident
        if target in targets:
            raise ValueError('duplicate physical text edit target; no implicit last-write priority')
        targets.add(target)
        if type(edit['expected_text']) is not str or type(edit['text']) is not str:
            raise ValueError('expected_text and text must be explicit strings')
        index, row = records[name][ident]
        if edit['expected_text'] != row['text']:
            raise ValueError('expected_text differs from the exact current readable source text')
        values = _readable_words(edit['text'], row['word_count'], name, contexts[name], codec)
        if contexts[name] == 'main':
            for old, word in zip(original[name][index]['tokens'], values):
                kind = codec.validate_word(word, 'main')['type']
                if kind != old['type'] or old['type'] != 'glyph' and word != old['word']:
                    raise ValueError('main control/fixed-bitmap positions and exact WORDs must remain unchanged')
        selected.append((name, index, edit['text']))
    result = copy.deepcopy(document)
    for name, index, text in selected:
        result[name][index]['text'] = text
    return result


def _load(path, maximum=MAX_JSON_BYTES):
    # Reuse the ordinary strict JSON reader; the local import avoids a cycle
    # with load_source's optional readable-format dispatch.
    from .media_sources import loads, _read
    return loads(_read(Path(path).resolve(strict=True), maximum))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('export', 'import', 'edit'))
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--glyph-sources', type=Path, nargs=2)
    parser.add_argument('--edits', type=Path,
        help='explicit checked text edit document; required only for edit mode')
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    if (args.mode == 'edit') != (args.edits is not None):
        parser.error('--edits is required only for edit mode')
    from .media_sources import json_bytes
    from .native import fresh_output
    project = args.project_root.resolve(strict=True)
    output = fresh_output(args.output)
    if (not output.is_relative_to(project / 'build') or output == project / 'build'
            or not output.parent.is_dir() or output.suffix != '.json'):
        raise ValueError('explicit fresh JSON file in this project build with existing parent required')
    if args.mode == 'export':
        if args.glyph_sources is None:
            raise ValueError('export requires both explicitly supplied manual glyph documents')
        # This CLI source is one plain typed file, not a hidden ROM/default
        # resource tree. Full graph imports belong to the normal loader.
        result = to_readable(_load(args.source), [_load(path, 1_000_000) for path in args.glyph_sources])
    elif args.mode == 'import':
        if args.glyph_sources is not None:
            raise ValueError('readable source already owns its explicit manual glyph documents')
        result = from_readable(_load(args.source))
    else:
        if args.glyph_sources is not None:
            raise ValueError('readable source already owns its explicit manual glyph documents')
        edits = _load(args.edits)
        _keys(edits, ('format', 'edits'))
        if type(edits['format']) is not str or edits['format'] != EDIT_FORMAT:
            raise ValueError('explicit readable text record edit document format required')
        result = with_text_edits(_load(args.source), edits['edits'])
    raw = json_bytes(result)
    if len(raw) > MAX_JSON_BYTES:
        raise ValueError('readable source exceeds its explicit JSON bound')
    with output.open('xb') as destination:
        destination.write(raw)
    print(json.dumps(dict(output=str(output), source_format=result['format'],
        bytes=len(raw), original_ROM_read=False, hash_run=False,
        native_run=False, resource_or_game_acceptance=False,
        source_edit_only=args.mode == 'edit'), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
