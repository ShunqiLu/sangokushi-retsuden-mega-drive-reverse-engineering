"""Read-only capture of actual retained Z80 entry inputs and shared sound RAM.

This is a snapshot port, not a runner, CPU, state initializer or device owner.
No AudioState read, platform callback, control method, lease, IRQ or clock is
invoked. Unknown and stale-only observations remain explicit missing proof.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import fields, is_dataclass
import threading

from .z80_case_inputs import (
    ALTERNATE, CARRIERS, CONTROL, STATE_FORMAT, Z80EntryBinding,
)


Z80_CAPTURE_FORMAT = 'g5510-actual-z80-entry-capture-v1'
RAM_BYTES = 8192


class AudioEntryCaptureError(ValueError):
    """A foreign or ambiguous observation cannot become a captured initial state."""


def _require(condition, message):
    if not condition:
        raise AudioEntryCaptureError(message)


def _uint(value, bits, context):
    _require(type(value) is int and 0 <= value < 1 << bits,
        context + ': complete unsigned integer required, not bool')
    return value


def _shared_views(state):
    from ..high_level_audio_engine.domain import AudioState
    from ..high_level_audio_engine.hardware_scene import SharedSoundAudioBus, SoundDevice
    _require(type(state) is AudioState and type(state.bus) is SharedSoundAudioBus,
        'one actual AudioState and its exact SharedSoundAudioBus are required')
    bus = state.bus
    sound, ram = bus.device, bus.ram
    _require(type(sound) is SoundDevice and sound.audio_state is state
        and type(ram) is bytearray and len(ram) == RAM_BYTES and sound.ram is ram,
        'the attached SoundDevice must own this same live8192-byte array')
    return bus, sound, ram


def _binding(binding, continuation):
    from ..high_level_audio_engine.domain import Continuation
    _require(type(binding) is Z80EntryBinding and binding.owner in ('z80:startup', 'z80:driver'),
        'one actual source-derived Z80EntryBinding is required')
    _require(type(continuation) is Continuation
        and continuation.image == binding.owner.removeprefix('z80:'),
        'the caller must supply the actual image-qualified Continuation')
    _uint(binding.logical_address, 16, 'binding logical entry')
    _uint(binding.physical_address, 20, 'binding physical source')
    _uint(continuation.expected_return_word, 16, 'actual continuation word')


def _carriers(frame, binding, continuation, missing):
    from ..high_level_audio_engine.domain import Continuation
    from ..high_level_audio_engine.owned_runtime import DriverFrame
    if type(frame) is DriverFrame:
        _require(tuple(field.name for field in fields(DriverFrame)) == CARRIERS,
            'the actual complete DriverFrame layout has changed')
        storage = vars(frame)
        source = 'actual_complete_DriverFrame'
    else:
        from ..high_level_audio_engine import contexts
        _require(binding.input_module == contexts.__name__,
            'typed inputs must belong to their actual registered contexts module')
        input_type = getattr(contexts, binding.input_class, None)
        _require(type(frame) is input_type and is_dataclass(frame)
            and not isinstance(frame, type) and input_type.__module__ == contexts.__name__
            and input_type.__dataclass_params__.frozen is True,
            'only the selected actual immutable input type or a complete DriverFrame is accepted')
        expected = tuple((name, Continuation if kind == 'Continuation' else int)
            for name, kind in binding.input_fields)
        _require(tuple((field.name, field.type) for field in fields(input_type)) == expected
            and all(name in CARRIERS or (name, kind) == ('continuation', 'Continuation')
                for name, kind in binding.input_fields),
            'typed input fields differ from the actual source binding')
        storage = vars(frame)
        if 'continuation' in storage:
            _require(storage['continuation'] is continuation,
                'the supplied continuation must be this typed input\'s actual object')
        source = contexts.__name__ + '.' + binding.input_class
    result = {}
    for name in CARRIERS:
        if name not in storage:
            result[name] = None
            missing.append('initial.frame.' + name)
        else:
            result[name] = _uint(storage[name], 8 if name in ('sample', 'conditions') else 16,
                'actual frame.' + name)
    return result, source


def _control(control, state, sound, platform, missing):
    from ..high_level_audio_engine.control_reset import AudioControlOwner, AudioControlState
    result = dict.fromkeys(CONTROL)
    stored = None
    if control is None:
        missing.extend('initial.control.' + name for name in CONTROL)
        source = 'not_supplied_no_implicit_platform_lookup'
    else:
        _require(type(control) is AudioControlOwner and control.sound is sound
            and sound.audio_state is state and vars(platform).get('control_owner') is control,
            'an explicitly supplied exact same-sound/platform AudioControlOwner is required')
        stored = control.control
        _require(type(stored) is AudioControlState,
            'the current owner must retain its exact actual AudioControlState')
        for name in CONTROL:
            value = getattr(stored, name)
            if value is None:
                missing.append('initial.control.' + name)
            elif name in ('pc_entry', 'interrupt_vector', 'refresh'):
                _uint(value, 16 if name == 'pc_entry' else 8, 'stored control.' + name)
            elif name == 'interrupt_mode':
                _require(type(value) is int and value in (0, 1, 2), 'actual stored interrupt mode required')
            else:
                _require(type(value) is bool, 'actual stored IFF/EI boolean required: ' + name)
            result[name] = value
        session = control._frame_session
        if session is not None and type(vars(session).get('thread')) is int:
            _require(vars(session)['thread'] == threading.get_ident(),
                'snapshot must run on the actual managed audio session thread')
        source = 'caller_supplied_same_bound_AudioControlOwner.control'
    # pc_entry names the last authorized semantic entry, not the current
    # per-instruction PC. refresh records reset/LD R,A writes, not all M1s.
    # Neither value is silently replaced by the selected alias or a pattern.
    missing.extend(('initial.control.pc_entry_current_entry_proof',
                    'initial.control.refresh_current_instruction_proof'))
    return result, stored, source


def _alternates(platform, alternate_AF, alternate_group, missing):
    from ..high_level_audio_engine.domain import AlternateGroup
    result = dict.fromkeys(ALTERNATE)
    platform_storage = vars(platform)
    if alternate_AF is None:
        missing.append('initial.alternate_AF')
        af_source = 'not_supplied_no_alternate_exchange_or_default'
    else:
        _uint(alternate_AF, 16, 'explicit alternate AF')
        if 'alternate_accumulator' in platform_storage:
            _require(type(platform_storage['alternate_accumulator']) is int
                and platform_storage['alternate_accumulator'] == alternate_AF,
                'explicit alternate AF disagrees with actual platform storage')
            af_source = 'caller_explicit_WORD_matches_platform.alternate_accumulator'
        else:
            af_source = 'caller_explicit_WORD_without_platform_storage_witness'
            missing.append('initial.alternate_AF_same_platform_storage')
    if alternate_group is None:
        missing.extend('initial.alternate_group.' + name for name in ALTERNATE)
        group_source = 'not_supplied_no_EXX_or_default'
    else:
        _require(type(alternate_group) is AlternateGroup,
            'the caller must explicitly supply the actual complete AlternateGroup')
        _require(tuple(field.name for field in fields(AlternateGroup)) == ALTERNATE,
            'the actual alternate group layout has changed')
        result = {name: _uint(getattr(alternate_group, name), 16, 'explicit alternate.' + name)
            for name in ALTERNATE}
        stored_group = platform_storage.get('alternate_group')
        if type(stored_group) is AlternateGroup:
            _require(all(type(getattr(stored_group, name)) is int
                and getattr(stored_group, name) == result[name] for name in ALTERNATE),
                'explicit alternate group disagrees with actual platform storage')
            group_source = 'caller_explicit_AlternateGroup_matches_platform.alternate_group'
        else:
            group_source = 'caller_explicit_AlternateGroup_without_platform_storage_witness'
            missing.append('initial.alternate_group_same_platform_storage')
    return result, dict(alternate_AF=af_source, alternate_group=group_source)


def _stack_word(raw, frame, continuation, binding, missing):
    cursor = frame['stack_cursor']
    if cursor is None:
        return dict(source='unavailable_missing_actual_stack_cursor', observed_word=None)
    following = (cursor + 1) & 0xFFFF
    if cursor >= 0x4000 or following >= 0x4000:
        missing.append('initial.continuation_stack_outside_shared_RAM')
        return dict(source='outside_actual_shared_RAM_no_device_read', observed_word=None,
            logical_stack_cursor=cursor)
    actual = raw[cursor & 0x1FFF] | raw[following & 0x1FFF] << 8
    ordinary = binding.invocation.get('kind') == 'typed_context'
    if ordinary and actual != continuation.expected_return_word:
        missing.append('initial.actual_stack_word_matches_declared_continuation')
    return dict(source='the_same_copied_RAM_no_DATA_event', logical_stack_cursor=cursor,
        mirrored_byte_offsets=[cursor & 0x1FFF, following & 0x1FFF], observed_word=actual,
        matches_declared_word=actual == continuation.expected_return_word,
        ordinary_return_claimed=ordinary, stack_pushed_or_consumed=False)


def snapshot_audio_entry(state, frame, *, binding, continuation, control=None,
        alternate_AF=None, alternate_group=None, memptr=None, max_DATA_operations):
    """Return (capture DTO, immutable actual8192 RAM) without entering software.

    Controls/alternates/WZ require explicit caller evidence. Stored-only PC/R
    retain their honest freshness gaps. This capture is not directly a complete
    assemble_z80_specs input: the writer must name the saved RAM and unresolved
    source/reference/device facts must still be supplied independently.
    """
    _binding(binding, continuation)
    _require(type(max_DATA_operations) is int and max_DATA_operations > 0,
        'an explicit positive future-case DATA budget is required; no refill is applied')
    bus, sound, ram = _shared_views(state)
    platform = state.platform
    before_operations = state.data_operations
    actual_limit = state.max_data_operations
    _require(type(actual_limit) is int and actual_limit > 0
        and type(before_operations) is int and 0 <= before_operations <= actual_limit,
        'actual finite AudioState DATA counters are required')
    lines = tuple(getattr(sound, name) for name in
        ('reset_epoch', 'reset_asserted', 'bus_requested', 'm68k_granted', 'executing'))
    missing = ['initial.sound_RAM.path']
    carriers, frame_source = _carriers(frame, binding, continuation, missing)
    controls, stored_control, control_source = _control(control, state, sound, platform, missing)
    control_identity = None if control is None else (
        control.generation, control.reset_asserted, control.phase, control._frame_session)
    alternate_identity = (vars(platform).get('alternate_accumulator'),
        vars(platform).get('alternate_group'))
    alternates, alternate_sources = _alternates(platform, alternate_AF, alternate_group, missing)
    if memptr is None:
        missing.append('initial.memptr_WZ')
    else:
        _uint(memptr, 16, 'caller explicit current memptr/WZ')
    # This is the sole actual output payload, read directly from the shared
    # bytearray. A second transient equality read detects concurrent changes;
    # neither access traverses AudioState/bus or emits DATA/stack events.
    raw = bytes(ram)
    stack = _stack_word(raw, carriers, continuation, binding, missing)
    _require(state.bus is bus and state.platform is platform and bus.device is sound
        and bus.ram is ram and sound.ram is ram and sound.audio_state is state
        and state.data_operations == before_operations and state.max_data_operations == actual_limit
        and tuple(getattr(sound, name) for name in
            ('reset_epoch', 'reset_asserted', 'bus_requested', 'm68k_granted', 'executing')) == lines
        and (control is None or (control.control is stored_control
            and (control.generation, control.reset_asserted, control.phase,
                control._frame_session) == control_identity))
        and vars(platform).get('alternate_accumulator') == alternate_identity[0]
        and vars(platform).get('alternate_group') is alternate_identity[1]
        and bytes(ram) == raw,
        'audio ownership/counters/control/RAM changed during snapshot; no mixed epoch is published')
    if not lines[4] or lines[1] or lines[3]:
        missing.append('runtime.actual_active_audio_execution_grant')
    initial = dict(format=STATE_FORMAT, frame=carriers, alternate_AF=alternate_AF,
        alternate_group=alternates, control=controls, memptr=memptr,
        sound_RAM=dict(path=None, bytes=RAM_BYTES), max_DATA_operations=max_DATA_operations)
    capture = dict(format=Z80_CAPTURE_FORMAT,
        binding=dict(owner=binding.owner, alias=binding.alias,
            logical_address=binding.logical_address, physical_address=binding.physical_address,
            module=binding.module, function=binding.function,
            input_module=binding.input_module, input_class=binding.input_class,
            input_fields=[list(row) for row in binding.input_fields],
            invocation=deepcopy(binding.invocation)),
        initial_state=initial,
        continuation=dict(image=continuation.image, expected_return_word=continuation.expected_return_word),
        missing=missing, saved_initial_input_complete=False,
        observations=dict(frame_source=frame_source, control_source=control_source,
            alternate_sources=alternate_sources,
            memptr_source='not_supplied' if memptr is None else 'caller_explicit_WORD_not_inferred_or_sampled',
            pc_entry_role='stored_semantic_entry_not_current_alias_PC',
            refresh_role='stored_reset_or_LD_R_A_value_not_current_instruction_R',
            continuation_stack=stack, capture_thread=threading.get_ident(),
            same_shared_sound_RAM=True, RAM_bytes=RAM_BYTES,
            reset_epoch=lines[0], reset_asserted=lines[1], bus_requested=lines[2],
            m68k_granted=lines[3], sound_executing=lines[4],
            audio_DATA_operations_before=before_operations,
            audio_DATA_operations_after=state.data_operations,
            actual_audio_DATA_limit=actual_limit,
            actual_audio_DATA_remaining=actual_limit - before_operations,
            declared_future_case_DATA_budget=max_DATA_operations,
            future_budget_is_not_a_runtime_grant=True,
            runtime_counters_changed=False, platform_or_device_callbacks_called=False,
            actual_current_binding_CodeType_proven=False,
            external_supplies_or_reference_captured=False,
            automatic_PC_R_WZ_or_alternate_values=False),
        directly_assemblable=False, audio_execution=False, CPU=False,
        lease_or_reset_or_IRQ_or_clock_changed=False, ledger_modified=False,
        formal_new_CODE_bytes=0)
    return capture, raw
