"""Scoped typed audio continuations over real shared-stack returns.

Intermediate runtime binding only: fixed semantic callees are temporarily
wrapped inside a locked session so the unchanged exact-build sources can keep
their compiler ABI. No opcode image, CPU loop, fake RET or silent stop exists.
"""
from dataclasses import dataclass, fields, is_dataclass, replace
from functools import wraps
import threading
from types import FunctionType

from tools.high_level_audio_engine.domain import AudioBoundary, AudioState, Continuation, word
from tools.high_level_audio_engine.hardware_scene import SoundDevice
from tools.high_level_audio_engine.owned_runtime import DriverFrame, ExplicitAudioPlatform


_SESSION_LOCK = threading.RLock()
_ACTIVE_SESSION = None

# Only these named business owners may be temporarily rebound. Calls to other
# AudioState objects execute their exact original callable without this router.
_OWNER_NAMES = {
    'business_notes': ('read_note_or_duration', 'read_rhythm_note',
        'resume_rhythm_parameter_stream', 'resume_note_parameter_stream'),
    'business_mailbox': ('update_rhythm_countdown', 'dispatch_extended_sequence_command'),
    'business_channel_update': ('update_fm_channel',),
    'business_hardware': ('update_audio_driver', 'update_sfx_channel_groups', 'update_channel_group'),
}

# A target is an existing recovered function, not an instruction/opcode. Its
# selection still comes from the game's actual owned LE16 command pointer table.
_SEQUENCE_TARGETS = {
    3440: 'set_stereo_pan', 3197: 'set_pitch_offset', 3218: 'set_misc_driver_field',
    3271: 'stop_channel_after_operator_reset', 3287: 'load_pan_pattern',
    3497: 'adjust_channel_volume', 3505: 'adjust_fm_channel_volume',
    3306: 'mark_note_continuation', 3277: 'set_note_release_duration',
    3457: 'set_lfo_and_stereo_pan', 3083: 'load_timer_reloads',
    3096: 'adjust_timer_reloads', 3222: 'adjust_psg_volume',
    3241: 'write_sequence_channel_register', 3246: 'write_sequence_port_zero_register',
    3373: 'select_instrument', 3257: 'set_pitch_modulation', 3569: 'set_pitch_envelope',
    3623: 'stop_and_release_channel', 3529: 'set_psg_noise', 3577: 'store_pitch_envelope',
    3560: 'set_psg_envelope', 3581: 'jump_sequence_pointer', 3822: 'repeat_sequence_section',
    3777: 'call_sequence_subroutine', 3803: 'return_sequence_subroutine',
    3525: 'set_duration_multiplier', 3518: 'adjust_note_transpose',
    3587: 'set_pitch_slide_mode', 3609: 'set_raw_frequency_mode',
    3312: 'set_special_channel_frequency', 2952: 'dispatch_extended_sequence_command',
    3079: 'set_driver_mode', 3210: 'adjust_note_divider',
    3116: 'dispatch_preserving_channel', 3124: 'set_all_channel_activity',
    3183: 'copy_sequence_block', 3064: 'set_all_duration_multipliers',
    3039: 'store_fm_parameters', 3201: 'set_voice_envelope',
}


@dataclass(frozen=True)
class _CallBoundary:
    name: str
    expected_return: int
    entered_stack: int
    frame: DriverFrame


class AudioReturnedContinuation(AudioBoundary):
    """A real already-consumed return, with every live returned carrier."""

    def __init__(self, target, frame):
        word(target)
        if type(frame) is not DriverFrame:
            raise ValueError('complete live nonlocal-return frame required')
        self.target, self.frame = target, frame
        super().__init__('real audio return to ' + hex(target))


def install_channel_view_data(scene, sound, fields_source):
    """Install the three original 8×LE16 channel-view tables as editable DATA."""
    if type(sound) is not SoundDevice or sound.scene is not scene:
        raise ValueError('one exact bound sound/Scene owner required')
    sound.require_m68k_owner()
    tables = fields_source.get('channel_view_tables') if type(fields_source) is dict else None
    if type(tables) is not list or len(tables) != 3:
        raise ValueError('three explicit original channel view tables required')
    for table, address, role in zip(tables, (0x06DC, 0x06EC, 0x06FC),
            ('paired_effect_views', 'active_effect_views', 'music_views')):
        if type(table) is not dict or set(table) != {'address', 'role', 'targets'}:
            raise ValueError('named complete channel view table required')
        if table['address'] != address or table['role'] != role:
            raise ValueError('original channel view table identity differs')
        targets = table['targets']
        if type(targets) is not list or len(targets) != 8:
            raise ValueError('eight complete LE16 view references required')
        for index, target in enumerate(targets):
            word(target)
            scene.write(0xA00000 + address + index * 2, 1, target & 255)
            scene.write(0xA00000 + address + index * 2 + 1, 1, target >> 8)


class AudioContinuationSession:
    """Per-AudioState injection with locked, strictly scoped callee adapters.

    Every replacement has an original callable identity guard. Finally restores
    exact originals and the AudioState's original indirect method. This transitional
    binding is deliberately opt-in and cannot overlap or cross owner threads.
    """

    def __init__(self, sound, frame):
        if type(sound) is not SoundDevice or type(frame) is not DriverFrame:
            raise ValueError('exact sound owner and full initial frame required')
        if type(sound.audio_state.platform) is not ExplicitAudioPlatform:
            raise ValueError('current unbound explicit platform owner required')
        from tools.high_level_audio_engine import (
            business_notes, business_mailbox, business_channel_update, business_hardware,
        )
        modules = {module.__name__.rsplit('.', 1)[-1]: module for module in
            (business_notes, business_mailbox, business_channel_update, business_hardware)}
        originals = []
        for module_name, names in _OWNER_NAMES.items():
            module = modules[module_name]
            for name in names:
                function = getattr(module, name)
                if type(function) is not FunctionType or function.__module__ != module.__name__:
                    raise ValueError('original finite callee identity required: ' + name)
                if function.__name__ != name or getattr(function, '_audio_session_proxy', False):
                    raise ValueError('callee already rebound: ' + name)
                if not isinstance(function.__annotations__.get('inputs'), type):
                    raise ValueError('actual immutable input ABI required: ' + name)
                originals.append((module, name, function))
        self.mailbox_wz = getattr(sound.audio_state, 'mailbox_wz_service', None)
        if self.mailbox_wz is not None:
            from tools.high_level_audio_engine.mailbox_wz import MailboxWzService, OWNERS
            if type(self.mailbox_wz) is not MailboxWzService:
                raise AudioBoundary('actual explicit mailbox WZ service type required')
            self.mailbox_wz.require_bound(sound)
            for name in OWNERS:
                module = modules['business_mailbox']
                original = getattr(module, name)
                if (type(original) is not FunctionType or original.__name__ != name
                        or original.__module__ != module.__name__
                        or getattr(original, '_audio_session_proxy', False)
                        or not isinstance(original.__annotations__.get('inputs'), type)):
                    raise AudioBoundary('original finite mailbox WZ owner required')
                self.mailbox_wz.view_for(original)  # Full-source and inverse guard before binding.
                originals.append((module, name, original))
        self.sound, self.state, self.frame = sound, sound.audio_state, frame
        self.originals, self.replacements = tuple(originals), []
        self.scopes, self.events = [], []
        self.entered, self.thread, self.old_indirect = False, None, None

    def _owner(self):
        if not self.entered or threading.get_ident() != self.thread:
            raise AudioBoundary('audio continuation session belongs to another execution thread')
        if self.sound.audio_state is not self.state or not self.sound.executing:
            raise AudioBoundary('continuation requires same active sound execution ownership')

    def _adopt(self, context, base=None):
        base = self.frame if base is None else base
        values = {field.name: getattr(context, field.name) for field in fields(context)
                  if field.name in DriverFrame.__dataclass_fields__}
        return replace(base, **values)

    def _proxy(self, original):
        execute = original if self.mailbox_wz is None else self.mailbox_wz.view_for(original)
        @wraps(original)
        def call(state, inputs):
            if state is not self.state:
                return original(state, inputs)
            self._owner()
            input_type = original.__annotations__['inputs']
            result_type = original.__annotations__['return']
            if type(inputs) is not input_type:
                return original(state, inputs)  # Retain original typed error.
            inputs.validate(state)
            actual = state.read_word_le(inputs.stack_cursor)
            if actual != inputs.continuation.expected_return_word:
                raise AudioBoundary('callee does not own its actual input return word')
            frame = self._adopt(inputs)
            scope = _CallBoundary(original.__name__, actual, inputs.stack_cursor, frame)
            self.scopes.append(scope)
            self.frame = frame
            try:
                try:
                    result = execute(state, inputs)
                except AudioReturnedContinuation as outcome:
                    if (outcome.target != actual or
                            outcome.frame.stack_cursor != (inputs.stack_cursor + 2) & 65535):
                        raise
                    result = result_type(**{field.name: getattr(outcome.frame, field.name)
                                            for field in fields(result_type)}).validate(state)
                    self.events.append(('caught_actual_return', original.__name__, actual,
                                        outcome.frame.stack_cursor))
                self.frame = self._adopt(result)
                return result
            finally:
                if not self.scopes or self.scopes[-1] is not scope:
                    raise AudioBoundary('continuation scope ownership was corrupted')
                self.scopes.pop()
        call._audio_session_proxy = True
        return call

    def __enter__(self):
        global _ACTIVE_SESSION
        _SESSION_LOCK.acquire()
        try:
            if self.entered or _ACTIVE_SESSION is not None:
                raise AudioBoundary('nested audio continuation bindings are not allowed')
            platform = self.state.platform
            if getattr(platform.indirect_transfer, '__func__', None) is not ExplicitAudioPlatform.indirect_transfer:
                raise AudioBoundary('cannot replace a supplied indirect continuation owner')
            indirect = self.state.indirect_transfer
            if (getattr(indirect, '__func__', None) is not AudioState.indirect_transfer
                    or 'indirect_transfer' in self.state.__dict__):
                raise AudioBoundary('cannot replace a supplied AudioState continuation binding')
            for module, name, original in self.originals:
                if getattr(module, name) is not original:
                    raise AudioBoundary('original callee changed before session: ' + name)
            self.old_indirect, self.thread = indirect, threading.get_ident()
            if self.mailbox_wz is not None:
                self.mailbox_wz.begin_scope(self)
            for module, name, original in self.originals:
                proxy = self._proxy(original)
                setattr(module, name, proxy)
                self.replacements.append((module, name, original, proxy))
            # Inject only this exact AudioState. A second AudioState sharing a
            # platform retains its original platform semantics unchanged.
            self.state.indirect_transfer = self.transfer
            self.entered, _ACTIVE_SESSION = True, self
            return self
        except BaseException:
            for module, name, original, proxy in reversed(self.replacements):
                if getattr(module, name) is proxy:
                    setattr(module, name, original)
            self.replacements.clear()
            try:
                if self.mailbox_wz is not None and self.mailbox_wz.session is self:
                    self.mailbox_wz.end_scope(self)
            finally:
                _SESSION_LOCK.release()
            raise

    def __exit__(self, error_type, error, traceback):
        global _ACTIVE_SESSION
        if (not self.entered or _ACTIVE_SESSION is not self
                or threading.get_ident() != self.thread):
            raise AudioBoundary('only the owning session/thread may restore audio bindings')
        changed = []
        try:
            for module, name, original, proxy in reversed(self.replacements):
                if getattr(module, name) is not proxy:
                    changed.append(name)
                else:
                    setattr(module, name, original)
            if getattr(self.state.indirect_transfer, '__self__', None) is not self:
                changed.append('AudioState.indirect_transfer')
            else:
                del self.state.indirect_transfer
            self.replacements.clear()
            try:
                if self.mailbox_wz is not None:
                    self.mailbox_wz.end_scope(self)
            finally:
                self.entered, _ACTIVE_SESSION = False, None
        finally:
            _SESSION_LOCK.release()
        if changed:
            raise AudioBoundary('callee changed inside session; foreign changes preserved: ' + ','.join(changed))
        return False

    def _handler(self, target):
        from tools.high_level_audio_engine import business_sequence, business_voice, business_mailbox, business_loaders
        name = _SEQUENCE_TARGETS.get(target)
        if name is None:
            raise AudioBoundary('unbound original sequence target: ' + hex(target))
        module = (business_voice if name in ('adjust_channel_volume', 'adjust_fm_channel_volume')
                  else business_mailbox if name == 'dispatch_extended_sequence_command'
                  else business_loaders if name == 'set_all_channel_activity'
                  else business_sequence)
        function = getattr(module, name)
        return function, function.__annotations__['inputs']

    def _tail_call(self, function, input_type, frame, continuation):
        values = {field.name: getattr(frame, field.name) for field in fields(input_type)
                  if field.name != 'continuation'}
        values['continuation'] = continuation
        self.frame = frame
        result = function(self.state, input_type(**values))
        self.frame = self._adopt(result)
        return self.frame

    def _stop_tail(self, target, frame):
        from tools.high_level_audio_engine.contexts_lifecycle import DriverLifecycle
        from tools.high_level_audio_engine.business_lifecycle_stopping import (
            run_stop_and_release_channel, run_stop_channel_after_operator_reset,
        )
        # The original handler discards two words, not two imaginary Python
        # frames. Its third real WORD must be a registered live outer boundary.
        first = self.state.read_word_le(frame.stack_cursor)
        second = self.state.read_word_le((frame.stack_cursor + 2) & 65535)
        outer = self.state.read_word_le((frame.stack_cursor + 4) & 65535)
        outer_stack = (frame.stack_cursor + 4) & 65535
        if first not in (0x0A42, 0x0B84):
            raise AudioBoundary('stop tail lacks original parameter-stream return word')
        owner = next((scope for scope in reversed(self.scopes)
                      if scope.entered_stack == outer_stack and scope.expected_return == outer), None)
        if owner is None:
            raise AudioBoundary('stop tail outer return has no actual registered caller')
        lifecycle = DriverLifecycle(frame.auxiliary_cursor, frame.channel_cursor,
            frame.conditions, frame.count_and_data, frame.lookup_cursor,
            frame.parameter_cursor, frame.sample, frame.stack_cursor)
        function = run_stop_and_release_channel if target == 0x0E27 else run_stop_channel_after_operator_reset
        function(self.state, lifecycle, Continuation('driver', outer))
        returned = DriverFrame(lifecycle.paired_channel_address, lifecycle.channel_address,
            lifecycle.condition_bits, lifecycle.transfer_word, lifecycle.source_cursor,
            lifecycle.secondary_cursor, lifecycle.working_byte, lifecycle.return_stack)
        if returned.stack_cursor != (frame.stack_cursor + 6) & 65535:
            raise AudioBoundary('original stop did not consume its three real continuation words')
        self.frame = returned
        self.events.append(('stop_tail', target, first, second, outer, frame.stack_cursor,
                            returned.stack_cursor, owner.name))
        raise AudioReturnedContinuation(outer, returned)

    def transfer(self, image, target, context):
        self._owner()
        word(target)
        if image != 'driver' or not self.scopes:
            raise AudioBoundary('unbound sound-image transfer or absent semantic owner')
        if isinstance(context, type) or not is_dataclass(context):
            raise ValueError('typed actual transfer context required')
        context.validate(self.state)
        frame = self._adopt(context)
        if target in (0x0E27, 0x0CC7):
            return self._stop_tail(target, frame)
        if type(context).__name__ not in ('ReadNoteOrDurationInput', 'ReadRhythmNoteInput',
                'ResumeRhythmParameterStreamInput', 'ResumeNoteParameterStreamInput',
                'DispatchExtendedSequenceCommandInput'):
            raise AudioBoundary('unbound typed sequence continuation: ' + type(context).__name__)
        resume = self.state.read_word_le(frame.stack_cursor)
        if resume not in (0x0A42, 0x0B84):
            raise AudioBoundary('sequence handler lacks actual original resume return')
        function, input_type = self._handler(target)
        handled = self._tail_call(function, input_type, frame, Continuation('driver', resume))
        if handled.stack_cursor != (frame.stack_cursor + 2) & 65535:
            raise AudioBoundary('sequence handler did not consume its actual resume return')
        self.events.append(('sequence_command', target, resume, frame.channel_cursor,
                            frame.parameter_cursor, handled.parameter_cursor))
        if type(context).__name__ == 'DispatchExtendedSequenceCommandInput':
            raise AudioReturnedContinuation(resume, handled)
        from tools.high_level_audio_engine import business_notes
        name = 'resume_rhythm_parameter_stream' if resume == 0x0A42 else 'resume_note_parameter_stream'
        continuation = getattr(business_notes, name)
        resumed = self._tail_call(continuation, continuation.__annotations__['inputs'],
                                  handled, context.continuation)
        raise AudioReturnedContinuation(context.continuation.expected_return_word, resumed)
