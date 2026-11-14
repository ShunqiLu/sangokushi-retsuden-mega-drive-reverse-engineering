"""Edit a few original audio event fields and verify the actual shared byte views."""

from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path
import sys


if __name__ == '__main__':
    # Run in the edition being edited, including its own codecs and geometry.
    sys.path.insert(0, str(Path.cwd().resolve()))


from tools.audio_sequences import audio_sequences
from tools.high_level_rom import audio_sequence_sources, media_sources
from tools.high_level_rom import resource_adapters, resource_registry


RESOURCE = 'audio_build'
MEMBER = 'assets/audio/shared/stateful_event_views.json'
EDIT_FORMAT = 'g5510-audio-sequence-field-edits-v1'
VIEW_IDENTITY = ('id', 'address', 'rom_offset', 'reader', 'raw_frequency', 'slide')
# These affect a sound field, not the bytecode parser's mode, control flow or
# record width. Keep the driver's native scale and unsigned byte semantics.
SOUND_PARAMETERS = {
    'fm_attenuation': 'attenuation_byte',
    'fine_detune': 'fine_detune_byte',
    'pan': 'pan_byte',
}


@dataclass(frozen=True)
class FieldEdit:
    view_id: str
    field: str
    expected: int
    value: int


class AudioSourceMemory(audio_sequences.Memory):
    """Z80 sequence reads backed only by the edition's encoded audio assets."""

    def __init__(self, physical):
        self.physical = physical
        self.read_offsets = set()

    def read(self, address, count=1):
        if type(count) is not int or count < 0 or address + count > 0x10000:
            raise audio_sequences.SequenceError('wrapped_or_oversize_read')
        offsets = tuple(self.offset(address + i) for i in range(count))
        if offsets and offsets != tuple(range(offsets[0], offsets[0] + count)):
            raise audio_sequences.SequenceError('copy_alias_boundary_read')
        self.read_offsets.update(offsets)
        try:
            return bytes(self.physical[offset] for offset in offsets)
        except KeyError as error:
            raise audio_sequences.SequenceError(
                f'no encoded audio source byte at ROM {error.args[0]:06X}') from error


def _checked_edit_rows(document):
    if type(document) is not dict or set(document) != {'format', 'edits'} or document['format'] != EDIT_FORMAT:
        raise ValueError(f'expected a complete {EDIT_FORMAT} document')
    if type(document['edits']) is not list or not document['edits']:
        raise ValueError('at least one explicit field edit is required')
    rows = []
    seen = set()
    for edit in document['edits']:
        if type(edit) is not dict or set(edit) != {'view_id', 'field', 'expected', 'value'}:
            raise ValueError('each edit needs view_id, field, expected and value')
        view_id, field, old, new = (edit[key] for key in ('view_id', 'field', 'expected', 'value'))
        if (type(view_id) is not str or not view_id or view_id in seen or type(field) is not str
                or type(old) is not int or type(new) is not int or not 0 <= old <= 255
                or not 0 <= new <= 255 or old == new):
            raise ValueError('use unique view IDs and distinct unsigned BYTE values')
        rows.append(FieldEdit(view_id, field, old, new))
        seen.add(view_id)
    return tuple(rows)


def _edit_views(fields, edits):
    original = {row['id']: row for row in fields['sequences']['views']}
    commands, notes = [], []
    for edit in edits:
        if edit.view_id not in original:
            raise ValueError('unknown view: ' + edit.view_id)
        view = original[edit.view_id]
        event = view['event']
        if event['type'] == 'note' and edit.field == 'note':
            if not 0x80 <= edit.value < 0xE0 or event['note'] != edit.expected:
                raise ValueError('old or replacement note does not match the timed note: ' + edit.view_id)
            notes.append(edit)
        elif event['type'] == 'command' and SOUND_PARAMETERS.get(event['command']) == edit.field:
            old_parameters = event['parameters']
            if old_parameters[edit.field] != edit.expected:
                raise ValueError('old command parameter no longer matches: ' + edit.view_id)
            commands.append(dict(view={key: view[key] for key in VIEW_IDENTITY},
                expected_parameters=old_parameters,
                parameters=dict(old_parameters, **{edit.field: edit.value})))
        else:
            raise ValueError('field is not an editable note or sound parameter: ' + edit.view_id)
    result = (audio_sequence_sources.with_command_parameters(fields, commands)
        if commands else deepcopy(fields))
    changed = {row['id']: row for row in result['sequences']['views']}
    for edit in notes:
        changed[edit.view_id]['event']['note'] = edit.value
    return result


def _source(root):
    spec, = (row for row in resource_registry.RESOURCE_SPECS if row.id == RESOURCE)
    wrapper_path = media_sources.member_path(root, spec.own_source)
    wrapper = media_sources.loads(media_sources._read(wrapper_path, media_sources.MAX_JSON))
    if (wrapper.get('format') != media_sources.FORMAT
            or wrapper.get('source_format') != audio_sequence_sources.FORMAT):
        raise ValueError('the edition must own the split named audio resource')
    members = [row['id'] for row in media_sources.describe(wrapper, RESOURCE) if row['file'] == MEMBER]
    if (len(members) != 1 or wrapper['graph']['sequences']['views'] != {media_sources.REFERENCE: members[0]}):
        raise ValueError('one declared member must own the editable sequence views')
    return media_sources.resolve(wrapper, root, RESOURCE)


def _encode_audio(typed, contract):
    rows = resource_adapters.audio_build(typed, contract)
    if resource_adapters.coalesced_spans(rows) != contract['spans']:
        raise ValueError('the standard audio encoder changed the fixed allocation')
    return rows


def _physical(rows):
    result = {}
    for row in rows:
        for offset, value in enumerate(row['data'], row['start']):
            if offset in result:
                raise ValueError(f'physical audio data overlaps at ROM {offset:06X}')
            result[offset] = value
    return result


def _edit_byte_offsets(before, after, edits):
    originals = {row['id']: row for row in before}
    changed = {row['id']: row for row in after}
    result = {}
    for edit in edits:
        old, new = originals[edit.view_id], changed[edit.view_id]
        old_event, new_event = old['event'], new['event']
        original_bytes = audio_sequences.encode_event(old_event, old_event)
        replacement = audio_sequences.encode_event(new_event, old_event)
        difference = [(index, left, right)
            for index, (left, right) in enumerate(zip(original_bytes, replacement, strict=True)) if left != right]
        if len(difference) != 1 or difference[0][1:] != (edit.expected, edit.value):
            raise ValueError('each selected original field must encode as one changed byte: ' + edit.view_id)
        index, left, right = difference[0]
        offset = old['rom_offset'] + index
        if offset in result:
            raise ValueError(f'two edits select the same physical byte {offset:06X}')
        result[offset] = (left, right, edit.view_id)
    return result


def _validate_decoded_views(views, physical, changed_offsets):
    memory = AudioSourceMemory(physical)
    dependencies = defaultdict(list)
    for view in views:
        memory.read_offsets.clear()
        mode = audio_sequences.Mode(view['reader'], view['raw_frequency'], view['slide'])
        if audio_sequences.decode(memory, view['address'], mode) != view['event']:
            raise ValueError('encoded data changes retained sequence interpretation: ' + view['id'])
        for offset in sorted(memory.read_offsets & changed_offsets):
            start, size = view['rom_offset'], view['event']['size']
            kind = 'consumed' if start <= offset < start + size else 'lookahead'
            dependencies[offset].append((view['id'], kind))
    return dict(dependencies)


def edit_sequence_member(root: Path, edits):
    """Return one complete external member and its actual physical edit evidence."""
    fields = _source(root)
    edited = _edit_views(fields, edits)
    before, after = (audio_sequence_sources.from_named(value) for value in (fields, edited))
    original_views, edited_views = (value['sequences']['views'] for value in (before, after))
    changed = _edit_byte_offsets(original_views, edited_views, edits)
    geometry = json.loads(resource_registry.GEOMETRY.read_text(encoding='utf-8'))
    if geometry['format'] != 'g5510-ROM-independent-resource-geometry-v1':
        raise ValueError('the edition must supply the original audio geometry contract')
    contract = geometry['contracts'][RESOURCE]
    aux_ids = tuple(row.id for row in resource_registry.RESOURCE_SPECS if row.role == 'audio' and row.id != RESOURCE)
    auxiliary = resource_registry.load_resources(root, ids=aux_ids)
    if auxiliary['unavailable'] or auxiliary['conflicts']:
        raise ValueError('all of the edition’s auxiliary audio resources must encode without conflicts')
    before_bytes, after_bytes = (_physical((*_encode_audio(value, contract), *auxiliary['blocks']))
        for value in (before, after))
    if before_bytes.keys() != after_bytes.keys():
        raise ValueError('the encoded audio allocation changed')
    actual = {offset: (value, after_bytes[offset]) for offset, value in before_bytes.items()
        if after_bytes[offset] != value}
    if actual != {offset: record[:2] for offset, record in changed.items()}:
        raise ValueError('encoded audio changes differ from the selected original fields')
    before_dependencies, after_dependencies = (_validate_decoded_views(views, values, changed.keys())
        for views, values in ((original_views, before_bytes), (edited_views, after_bytes)))
    if before_dependencies != after_dependencies or before_dependencies.keys() != changed.keys():
        raise ValueError('the changed byte has a new read path or lost an existing read path')
    return edited['sequences']['views'], dict(format='g5510-audio-sequence-field-edit-receipt-v1',
        confidence='confirmed_encoded_bytes_and_declared_sequence_views',
        source_member=MEMBER, encoded_audio_bytes=len(before_bytes),
        decoded_views_before=len(original_views), decoded_views_after=len(edited_views),
        changes=[dict(rom_offset=f'{offset:06X}', old=f'{old:02X}', new=f'{new:02X}', edited_view=view,
            reading_views=[dict(id=ident, role=role) for ident, role in after_dependencies[offset]])
            for offset, (old, new, view) in sorted(changed.items())],
        original_ROM_read=False, full_ROM_built=False, playback_verified=False)


def _fresh_output(path):
    path = path.absolute()
    if (not path.parent.is_dir() or path.exists()
            or any(item.is_symlink() or getattr(item, 'is_junction', lambda: False)()
                for item in (path, *path.parents))):
        raise ValueError('output must be a new ordinary file in an existing directory')
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--edits', required=True, type=Path, help='JSON file of explicitly reviewed field changes')
    parser.add_argument('--output', required=True, type=Path, help='new stateful_event_views.json path')
    args = parser.parse_args(argv)
    root = Path.cwd().resolve()
    if not all(Path(module.__file__).resolve().is_relative_to(root) for module in
            (audio_sequences, audio_sequence_sources, media_sources, resource_registry, resource_adapters)):
        raise ValueError('run from the edition root so only its own codecs are used')
    destination = _fresh_output(args.output)
    receipt_path = _fresh_output(destination.with_name(destination.stem + '.edit-receipt.json'))
    edits = _checked_edit_rows(media_sources.loads(media_sources._read(args.edits, 64 << 10)))
    member, receipt = edit_sequence_member(root, edits)
    with destination.open('xb') as stream:
        stream.write(media_sources.json_bytes(member))
    with receipt_path.open('xb') as stream:
        stream.write(media_sources.json_bytes(receipt))
    print(json.dumps(dict(receipt, output=str(destination), receipt=str(receipt_path)), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

