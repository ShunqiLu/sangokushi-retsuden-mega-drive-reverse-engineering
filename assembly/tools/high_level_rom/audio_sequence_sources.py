"""Named editing of the complete existing audio command-view resource.

This changes representation, not playback, allocation or the event grammar.
The existing sequence codec supplies command names and all operand widths.
Each command has one editable parameter authority; unknown argument meanings
remain explicitly ordered bytes instead of invented musical instructions.
"""
from __future__ import annotations

from copy import deepcopy

from ..audio_sequences.audio_sequences import FF_WIDTHS, NAMES, WIDTHS


RESOURCE_ID = 'audio_build'
FORMAT = 'g5510-named-audio-sequence-commands-v1'
EDIT_FORMAT = 'g5510-named-audio-command-parameter-edits-v1'
TYPED_FORMAT = 'g5510-unified-typed-audio-v1'
SEQUENCE_FORMAT = 'g5510-named-stateful-sequence-views-v1'
TYPED_SEQUENCE_FORMAT = 'g5510_stateful_sequence_views'
_DOCUMENT_KEYS = frozenset(('format', 'source', 'definitions', 'sequences', 'envelopes'))
_SEQUENCE_KEYS = frozenset(('schema_version', 'format', 'source', 'views', 'rhythm'))
_VIEW_KEYS = frozenset(('id', 'address', 'rom_offset', 'reader', 'raw_frequency', 'slide', 'event'))
_VIEW_IDENTITY_KEYS = _VIEW_KEYS - {'event'}
_EDIT_KEYS = frozenset(('view', 'expected_parameters', 'parameters'))

# (parameter name, representation, serialized BYTE count). Names narrower
# than a raw operand are used only where current recovered consumers establish
# them. In particular, this table assigns no note/octave names or milliseconds.
_PARAMETERS = {
    0xE0: (('pan_byte', 'byte', 1),),
    0xE1: (('fine_detune_byte', 'byte', 1),),
    0xE3: (),
    0xE6: (('attenuation_byte', 'byte', 1),),
    0xE7: (),
    0xE8: (('note_off_delay_byte', 'byte', 1),),
    0xE9: (('lfo_register_byte', 'byte', 1), ('pan_byte', 'byte', 1)),
    0xEA: (('timer_a_reload_low_byte', 'byte', 1),
           ('timer_a_reload_high_byte', 'byte', 1), ('timer_b_reload_byte', 'byte', 1)),
    0xEB: (('timer_a_delta_low_byte', 'byte', 1),
           ('timer_a_delta_high_byte', 'byte', 1), ('timer_b_delta_byte', 'byte', 1)),
    0xEC: (('attenuation_delta_byte', 'byte', 1),),
    0xED: (('register_selector_byte', 'byte', 1), ('register_value_byte', 'byte', 1)),
    0xEE: (('register_selector_byte', 'byte', 1), ('register_value_byte', 'byte', 1)),
    0xF2: (),
    0xF3: (('noise_control_byte', 'byte', 1),),
    0xF4: (('modulation_selector_byte', 'byte', 1),),
    0xF5: (('envelope_selector_byte', 'byte', 1),),
    0xF6: (('target_z80_address', 'le16', 2),),
    0xF7: (('counter_index_byte', 'byte', 1), ('repeat_count_byte', 'byte', 1),
           ('target_z80_address', 'le16', 2)),
    0xF8: (('target_z80_address', 'le16', 2),),
    0xF9: (),
    0xFA: (('duration_multiplier_byte', 'byte', 1),),
    0xFB: (('transpose_delta_byte', 'byte', 1),),
    0xFC: (('mode_byte', 'byte', 1),),
    0xFD: (('mode_byte', 'byte', 1),),
    0xFE: (('frequency_selector_bytes', 'bytes', 4),),
}


def _object(value, keys, context):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError(context + ': complete exact fields required; no raw/parameter backup')


def _uint(value, maximum, context):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError(context + ': unsigned integer required; bool is not a BYTE/WORD')
    return value


def _bytes(value, context):
    if type(value) is not list:
        raise ValueError(context + ': an explicit ordered BYTE list is required')
    return [_uint(item, 255, context) for item in value]


def _layout(opcode, selector=None):
    if opcode == 0xEF:
        first = (('selector_byte', 'byte', 1),)
        return first + ((('external_music_command_byte', 'byte', 1),) if selector & 0x80 else ())
    return _PARAMETERS.get(opcode)


def _validate_typed_command(event):
    if type(event) is not dict:
        raise ValueError('a complete typed sequence command is required')
    opcode = _uint(event.get('opcode'), 255, 'command opcode')
    if opcode < 0xE0 or len(NAMES) != 32 or len(WIDTHS) != 32:
        raise ValueError('command must use the current complete E0..FF grammar')
    keys = {'type', 'opcode', 'arguments', 'size'}
    if opcode == 0xFF:
        keys.add('subcommand')
    _object(event, keys, 'typed sequence command')
    if event['type'] != 'command':
        raise ValueError('command type must remain explicit')
    arguments = _bytes(event['arguments'], 'command arguments')
    prefix = 1
    expected_width = WIDTHS[opcode - 0xE0]
    if opcode == 0xEF:
        if not arguments:
            raise ValueError('instrument command requires its original selector BYTE')
        expected_width = 2 if arguments[0] & 0x80 else 1
    elif opcode == 0xFF:
        subcommand = _uint(event['subcommand'], len(FF_WIDTHS) - 1, 'extended subcommand')
        prefix = 2
        expected_width = FF_WIDTHS[subcommand]
        if subcommand == 4:
            if len(arguments) < 3 or arguments[2] == 0:
                raise ValueError('FF04 requires the existing nonzero inline-count framing; no wrap is invented')
            expected_width = 3 + arguments[2]
    if type(expected_width) is not int or len(arguments) != expected_width:
        raise ValueError('operand count differs from the existing stateful sequence grammar')
    if type(event['size']) is not int or event['size'] != prefix + expected_width:
        raise ValueError('command size differs from its original serialized extent')
    return opcode, arguments


def _named_parameters(opcode, arguments):
    layout = _layout(opcode, arguments[0] if opcode == 0xEF else None)
    if layout is None:
        # E2, E4, E5, F0, F1 and FF retain their exact original argument
        # positions. A handler/name alone does not prove every operand's role.
        return {'unknown_argument_bytes': list(arguments)}
    result, cursor = {}, 0
    for name, kind, width in layout:
        values = arguments[cursor:cursor + width]
        if len(values) != width:
            raise ValueError('named operand layout disagrees with the current sequence grammar')
        if kind == 'le16':
            result[name] = values[0] | values[1] << 8
        else:
            result[name] = values[0] if kind == 'byte' else list(values)
        cursor += width
    if cursor != len(arguments):
        raise ValueError('the complete command argument extent must have one named authority')
    return result


def _typed_parameters(opcode, parameters):
    if type(parameters) is not dict:
        raise ValueError('one complete parameter object is required')
    selector = _uint(parameters.get('selector_byte'), 255, 'instrument selector') if opcode == 0xEF else None
    layout = _layout(opcode, selector)
    if layout is None:
        _object(parameters, {'unknown_argument_bytes'}, 'unknown command operands')
        return _bytes(parameters['unknown_argument_bytes'], 'unknown argument bytes')
    _object(parameters, {name for name, _, _ in layout}, 'named command parameters')
    arguments = []
    for name, kind, width in layout:
        if kind == 'le16':
            value = _uint(parameters[name], 65535, name)
            arguments.extend((value & 255, value >> 8))
        elif kind == 'byte':
            arguments.append(_uint(parameters[name], 255, name))
        else:
            values = _bytes(parameters[name], name)
            if len(values) != width:
                raise ValueError(name + ': original ordered selector count must remain unchanged')
            arguments.extend(values)
    return arguments


def _to_named_command(event):
    opcode, arguments = _validate_typed_command(event)
    result = dict(type='command', command=NAMES[opcode - 0xE0],
        parameters=_named_parameters(opcode, arguments), size=event['size'])
    if opcode == 0xFF:
        result['subcommand'] = event['subcommand']
    return result


def _from_named_command(event):
    if type(event) is not dict or type(event.get('command')) is not str or event['command'] not in NAMES:
        raise ValueError('one existing named E0..FF command is required')
    opcode = 0xE0 + NAMES.index(event['command'])
    keys = {'type', 'command', 'parameters', 'size'} | ({'subcommand'} if opcode == 0xFF else set())
    _object(event, keys, 'named sequence command')
    result = dict(type=event['type'], opcode=opcode,
        arguments=_typed_parameters(opcode, event['parameters']), size=event['size'])
    if opcode == 0xFF:
        result['subcommand'] = event['subcommand']
    _validate_typed_command(result)
    return result


def _views(fields, *, named):
    _object(fields, _DOCUMENT_KEYS, 'complete audio_build document')
    if fields['format'] != (FORMAT if named else TYPED_FORMAT):
        raise ValueError('explicit complete audio_build source format required')
    if any(type(fields[key]) is not dict for key in ('source', 'definitions', 'sequences', 'envelopes')):
        raise ValueError('complete resolved audio source sections are required')
    sequences = fields['sequences']
    _object(sequences, _SEQUENCE_KEYS, 'complete audio sequence section')
    if (type(sequences['schema_version']) is not int or sequences['schema_version'] != 1
            or sequences['format'] != (SEQUENCE_FORMAT if named else TYPED_SEQUENCE_FORMAT)
            or type(sequences['views']) is not list or not sequences['views']
            or type(sequences['rhythm']) is not dict or type(sequences['source']) is not dict):
        raise ValueError('resolved original sequence views, rhythm and metadata are required; no graph fallback')
    seen = set()
    for view in sequences['views']:
        _object(view, _VIEW_KEYS, 'stateful sequence view')
        if type(view['id']) is not str or not view['id'] or view['id'] in seen:
            raise ValueError('each existing stateful view requires a unique physical/mode identity')
        seen.add(view['id'])
        _uint(view['address'], 65535, 'view Z80 address')
        _uint(view['rom_offset'], 0xFFFFF, 'view physical source offset')
        if (view['reader'] not in ('ordinary', 'rhythm') or type(view['raw_frequency']) is not bool
                or type(view['slide']) is not bool or type(view['event']) is not dict
                or view['event'].get('type') not in ('command', 'note', 'duration', 'rhythm', 'raw_frequency')):
            raise ValueError('the existing reader/mode/event identity must remain explicit')
    return sequences['views']


def _convert(fields, *, named):
    views = _views(fields, named=not named)
    # Convert only actual command views. Existing note/duration/rhythm/frequency
    # fields and all header/voice/envelope metadata remain structurally intact.
    commands = {index: (_to_named_command(view['event']) if named else _from_named_command(view['event']))
        for index, view in enumerate(views) if view['event']['type'] == 'command'}
    result = deepcopy(fields)
    result['format'] = FORMAT if named else TYPED_FORMAT
    result['sequences']['format'] = SEQUENCE_FORMAT if named else TYPED_SEQUENCE_FORMAT
    for index, event in commands.items():
        result['sequences']['views'][index]['event'] = event
    return result


def to_named(fields: dict) -> dict:
    """Replace the complete typed audio document's opcode/argument pairs.

    No ROM, encoder, source file, alias baseline or playback owner is read.
    A physical view remains shared rather than copied into each song/channel.
    """
    return _convert(fields, named=True)


def from_named(fields: dict) -> dict:
    """Restore the sole typed authority consumed by the unchanged audio codec.

    This representation check is not a substitute for the normal resource
    geometry, cross-view alias/lookahead or actual playback checks. Changing a
    command's size does not allocate new space or relocate any following view.
    """
    return _convert(fields, named=False)


def _review_command_edit(view, edit):
    identity = edit['view']
    _object(identity, _VIEW_IDENTITY_KEYS, 'complete command view identity')
    if any(type(identity[name]) is not type(view[name]) or identity[name] != view[name]
            for name in _VIEW_IDENTITY_KEYS):
        raise ValueError('command view address/reader/mode identity differs from its explicit source')
    event = view['event']
    if event['type'] != 'command':
        raise ValueError('parameter edits require one existing command, not a timed event')
    before = _from_named_command(event)
    expected_event = dict(event, parameters=edit['expected_parameters'])
    _from_named_command(expected_event)
    if edit['expected_parameters'] != event['parameters']:
        raise ValueError('command parameters changed from their complete explicit expected values')
    replacement = dict(event, parameters=edit['parameters'])
    after = _from_named_command(replacement)
    if (set(edit['parameters']) != set(event['parameters'])
            or len(after['arguments']) != len(before['arguments'])):
        raise ValueError('parameter edit cannot change command operand shape or serialized extent')
    if (before['opcode'] == 0xFF and before['subcommand'] == 4
            and after['arguments'][2] != before['arguments'][2]):
        raise ValueError('FF04 inline count cannot change its existing physical allocation')
    # Normalize through the same sole typed authority, not an edit-only grammar.
    return _to_named_command(after)['parameters']


def _review_command_edits(fields, edits):
    if type(edits) is not list or not edits:
        raise ValueError('one explicit nonempty command parameter edit list required')
    views = {view['id']: view for view in fields['sequences']['views']}
    reviewed, seen = [], set()
    for edit in edits:
        _object(edit, _EDIT_KEYS, 'command parameter edit')
        identity = edit['view']
        if type(identity) is not dict or type(identity.get('id')) is not str or identity['id'] not in views:
            raise ValueError('edit must select an existing complete command view identity')
        view_id = identity['id']
        if view_id in seen:
            raise ValueError('duplicate command view edit; no implicit last-write priority')
        seen.add(view_id)
        reviewed.append((view_id, _review_command_edit(views[view_id], edit)))
    return reviewed


def with_command_parameters(fields: dict, edits: list[dict]) -> dict:
    """Return a checked full named document; never mutate either input.

    Each edit names the exact existing physical/reader/mode view, its complete
    previous parameters and a same-command/same-size replacement. Shared views
    remain in their existing section, rather than copied into songs/channels.
    This is not relocation, alias/lookahead proof or playback qualification.
    """
    from_named(fields)
    reviewed = _review_command_edits(fields, edits)
    result = deepcopy(fields)
    views = {view['id']: view for view in result['sequences']['views']}
    for view_id, parameters in reviewed:
        views[view_id]['event']['parameters'] = parameters
    return result


def main(argv=None):
    """Convert or batch-edit one explicit audio source to a fresh JSON."""
    import argparse
    import json
    from pathlib import Path
    from .media_sources import (FORMAT as GRAPH_FORMAT, MAX_JSON, json_bytes,
        resolve_source_document)
    from .native import fresh_output
    from .readable_text import _load

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('direction', choices=('export', 'import', 'edit'))
    parser.add_argument('--source', type=Path, required=True,
        help='one complete typed/named audio JSON, or an explicitly rooted external graph for export')
    parser.add_argument('--source-root', type=Path,
        help='export only: explicit existing own media root for an external graph; no inferred root')
    parser.add_argument('--edits', type=Path,
        help='edit only: explicit complete command parameter edits document')
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True,
        help='new JSON in project/build with an existing parent; no overwrite or media copy')
    args = parser.parse_args(argv)
    project = args.project_root.resolve(strict=True)
    output = fresh_output(args.output)
    if (not project.is_dir() or not output.is_relative_to(project / 'build')
            or output == project / 'build' or not output.parent.is_dir()
            or output.suffix != '.json'):
        raise ValueError('explicit fresh project/build JSON and an existing parent are required')
    if args.direction != 'export' and args.source_root is not None:
        raise ValueError('import/edit consume one complete named JSON, not an external graph/root')
    if (args.direction == 'edit') != (args.edits is not None):
        raise ValueError('only edit requires one explicit --edits document')
    document = _load(args.source, MAX_JSON)
    if args.direction == 'export':
        graph = type(document) is dict and document.get('format') == GRAPH_FORMAT
        if graph != (args.source_root is not None):
            raise ValueError('only external graph export requires an explicit --source-root')
        root = None if args.source_root is None else args.source_root.absolute()
        if root is not None and not root.is_dir():
            raise ValueError('explicit existing own media root is required')
        fields = resolve_source_document(document, root, RESOURCE_ID)
        result = to_named(fields)
    elif args.direction == 'import':
        result = from_named(document)
    else:
        edits = _load(args.edits, MAX_JSON)
        _object(edits, {'format', 'edits'}, 'command parameter edits document')
        if edits['format'] != EDIT_FORMAT:
            raise ValueError('explicit named audio command parameter edit format required')
        result = with_command_parameters(document, edits['edits'])
    encoded = json_bytes(result)
    if len(encoded) > MAX_JSON:
        raise ValueError('complete converted audio JSON exceeds the existing bounded JSON limit')
    with output.open('xb') as stream:
        stream.write(encoded)
    print(json.dumps(dict(output=str(output), resource_id=RESOURCE_ID,
        source_format=result['format'], bytes=len(encoded), source_conversion_only=True,
        parameter_edit_only=args.direction == 'edit',
        original_ROM_read=False, resource_encoding_run=False, native_run=False,
        game_run=False, hash_run=False, strict_acceptance=False), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
