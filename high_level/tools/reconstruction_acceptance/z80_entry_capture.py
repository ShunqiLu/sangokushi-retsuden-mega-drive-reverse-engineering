"""Optional public Z80 entry observer, sharing its caller's monitor and store.

Only an actually executing public named function is observed. Private startup
and WZ views are explicit coverage gaps; filename/name guesses never qualify a
CodeType. The observer owns no monitor, sound execution, clock or file store.
"""
from __future__ import annotations

import os
import sys
from types import CodeType, FrameType, FunctionType

from .audio_entry_capture import snapshot_audio_entry
from .entry_capture_store import EntryCaptureStore
from .z80_entry_capture_catalog import Z80CaptureTarget


TYPE_NAMES = {
    'state': 'tools.high_level_audio_engine.domain:AudioState',
    'platform': 'tools.high_level_audio_engine.domain:AudioPlatform',
    'continuation': 'tools.high_level_audio_engine.domain:Continuation',
    'alternate': 'tools.high_level_audio_engine.domain:AlternateGroup',
    'bus': 'tools.high_level_audio_engine.hardware_scene:SharedSoundAudioBus',
    'sound': 'tools.high_level_audio_engine.hardware_scene:SoundDevice',
    'control': 'tools.high_level_audio_engine.control_reset:AudioControlOwner',
    'scene': 'tools.high_level_scene_flows.domain:SceneState',
}
COVERAGE_LIMITS = (
    'only exact public function CodeType plus same module globals are captured',
    'private reversible driver-startup suspension view is not captured',
    'private mailbox WZ views are not captured or inferred from filenames',
    'temporarily rebound public owners are not unwrapped; their later genuine public entries remain eligible',
    'partial immutable inputs stay partial; no outer DriverFrame supplies absent carriers',
    'current refresh R and WZ are unknown; stored refresh is observation only',
    'captured source mapping is not file-AST-to-CodeType or full-callee qualification',
    'captured input is not a historical pre-CALL or independent original reference',
)


class Z80EntryCaptureError(ValueError):
    """Capture cannot repair an unknown owner or hide a failed write."""


def _path_key(path):
    return os.path.normcase(os.path.normpath(str(path)))


def _loaded_type(name):
    module, member = name.split(':', 1)
    namespace = sys.modules.get(module)
    value = None if namespace is None else vars(namespace).get(member)
    return value if isinstance(value, type) else None


def _exact(value, name):
    actual = _loaded_type(name)
    return actual is not None and type(value) is actual


def _normal_sound(state):
    """Filter foreign/fixture buses without consuming any sound/device API."""
    if not _exact(state, TYPE_NAMES['state']):
        return None
    platform_type = _loaded_type(TYPE_NAMES['platform'])
    if platform_type is None or not isinstance(vars(state).get('platform'), platform_type):
        return None
    bus = vars(state).get('bus')
    if not _exact(bus, TYPE_NAMES['bus']):
        return None
    storage = vars(bus)
    sound, ram = storage.get('device'), storage.get('ram')
    if not _exact(sound, TYPE_NAMES['sound']):
        return None
    actual = vars(sound)
    if (actual.get('audio_state') is not state or actual.get('ram') is not ram
            or type(ram) is not bytearray or len(ram) != 8192
            or not _exact(actual.get('scene'), TYPE_NAMES['scene'])):
        return None
    return sound


def _stored_platform_inputs(state, sound):
    """Pass only directly retained same-platform values, never call providers."""
    platform = vars(state).get('platform')
    storage = vars(platform)
    control = storage.get('control_owner')
    if not (_exact(control, TYPE_NAMES['control']) and vars(control).get('sound') is sound):
        control = None
    alternate_AF = storage.get('alternate_accumulator')
    if type(alternate_AF) is not int or not 0 <= alternate_AF <= 0xFFFF:
        alternate_AF = None
    alternate_group = storage.get('alternate_group')
    if not _exact(alternate_group, TYPE_NAMES['alternate']):
        alternate_group = None
    elif any(type(vars(alternate_group).get(name)) is not int
            or not 0 <= vars(alternate_group)[name] <= 0xFFFF
            for name in ('count_and_data', 'parameter_cursor', 'lookup_cursor')):
        alternate_group = None
    return control, alternate_AF, alternate_group


class Z80EntryObserver:
    """Public callback component; its parent owns one monitor/store lifetime.

    handles() is lexical and side-effect free. An identity/legacy mismatch in
    on_entry() returns True: it must not DISABLE a later genuine call through
    the same CodeType after the application's temporary bindings have ended.
    """

    def __init__(self, targets, store, *, max_captures_per_entry: int, max_DATA_operations: int):
        if (type(targets) is not tuple or not targets
                or any(type(target) is not Z80CaptureTarget for target in targets)):
            raise TypeError('an explicit nonempty tuple of prepared public Z80 targets required')
        if type(store) is not EntryCaptureStore:
            raise TypeError('the same explicitly budgeted EntryCaptureStore required')
        if type(max_captures_per_entry) is not int or max_captures_per_entry <= 0:
            raise ValueError('explicit positive capture limit per audio entry required')
        if type(max_DATA_operations) is not int or not 0 < max_DATA_operations <= (1 << 63) - 1:
            raise ValueError('explicit positive future-case DATA budget required; no runtime refill')
        self._targets, self._store = targets, store
        self._maximum, self._future_DATA_limit = max_captures_per_entry, max_DATA_operations
        self._indices = {}
        identities = set()
        for index, target in enumerate(targets):
            binding = target.binding
            identity = binding.owner, binding.alias, binding.physical_address
            key = _path_key(target.source_path), binding.function
            if (not target.source_path.is_absolute() or identity in identities or key in self._indices):
                raise ValueError('each public audio source/alias must have exactly one pre-resolved target')
            identities.add(identity)
            self._indices[key] = index
        self._counts = [0] * len(targets)
        self._written = self._matched_calls = 0
        self._unqualified_calls = self._foreign_context_calls = 0
        self._exhausted = self._failed = False
        self._budget_reason = None

    @property
    def store(self):
        """Read-only identity witness for the parent collector's one store."""
        return self._store

    def handles(self, code: CodeType) -> bool:
        """No import, source read, owner lookup or runtime operation here."""
        return (type(code) is CodeType and code.co_qualname == code.co_name
            and os.path.isabs(code.co_filename)
            and (_path_key(code.co_filename), code.co_name) in self._indices)

    def _public_context(self, target, code, live):
        binding = target.binding
        module = sys.modules.get(binding.module)
        function = None if module is None else vars(module).get(binding.function)
        if not (type(function) is FunctionType and function.__code__ is code
                and function.__module__ == binding.module and function.__name__ == binding.function
                and function.__qualname__ == binding.function and function.__closure__ is None
                and function.__globals__ is vars(module) and live.f_globals is vars(module)):
            self._unqualified_calls += 1
            return None
        local = live.f_locals
        state, inputs = local.get('state'), local.get('inputs')
        sound = _normal_sound(state)
        if sound is None or not _exact(inputs, binding.input_module + ':' + binding.input_class):
            self._foreign_context_calls += 1
            return None
        continuation = vars(inputs).get('continuation')
        if (not _exact(continuation, TYPE_NAMES['continuation'])
                or vars(continuation).get('image') != binding.owner.removeprefix('z80:')):
            self._foreign_context_calls += 1
            return None
        return state, inputs, sound, continuation

    def on_entry(self, code: CodeType, live: FrameType, instruction_offset: int) -> bool:
        if not self.handles(code):
            return False
        if self._exhausted:
            return False
        index = self._indices[(_path_key(code.co_filename), code.co_name)]
        if self._counts[index] >= self._maximum:
            return False
        target = self._targets[index]
        context = self._public_context(target, code, live)
        if context is None:
            return True
        state, inputs, sound, continuation = context
        self._matched_calls += 1
        try:
            control, alternate_AF, alternate_group = _stored_platform_inputs(state, sound)
            metadata, raw = snapshot_audio_entry(state, inputs, binding=target.binding,
                continuation=continuation, control=control, alternate_AF=alternate_AF,
                alternate_group=alternate_group, memptr=None,
                max_DATA_operations=self._future_DATA_limit)
            # RESET/LD R,A's retained value is not current M1-counted R.
            stored_refresh = metadata['initial_state']['control']['refresh']
            metadata['observations']['stored_control_refresh_not_current_R'] = stored_refresh
            metadata['initial_state']['control']['refresh'] = None
            if 'initial.control.refresh' not in metadata['missing']:
                metadata['missing'].append('initial.control.refresh')
            metadata['missing'].extend((
                'current_file_AST_to_loaded_CodeType_and_complete_callee_qualification',
                'independent_original_Z80_execution_reference',
                'actual_external_supplies_and_device_initial_state_artifacts',
                'whole_owner_all_alias_reachability_and_output_observations',
                'original_CALL_or_interrupt_entry_protocol',
            ))
            metadata['capture_position'] = 'actual_public_PY_START_before_first_Python_body_instruction'
            metadata['initial_state_protocol'] = 'observed_body_entry_not_historical_pre_CALL'
            metadata['source_binding'] = dict(batch=str(target.binding_batch),
                pointer=target.source_binding_pointer, source=str(target.source_path),
                current_source_line=target.current_source_line, qualification=target.qualification)
            metadata['runtime'] = dict(code=dict(filename=code.co_filename,
                name=code.co_name, qualname=code.co_qualname, first_line=code.co_firstlineno,
                flags=code.co_flags, in_process_identity=id(code)),
                instruction_offset=instruction_offset, public_function_code_identity_matches=True,
                public_module_globals_identity_matches=True,
                file_AST_to_loaded_CodeType_qualification='not_evaluated',
                state_identity=id(state), inputs_identity=id(inputs), sound_identity=id(sound))
            metadata['observations']['actual_current_binding_CodeType_proven'] = True
            metadata['observations']['CodeType_proof_scope'] = 'exact_public_function_identity_only_not_file_AST_or_callee_closure'
            metadata['strict_acceptance_status'] = 'not_evaluated'
            metadata['strict_credit'] = 0
            binding = target.binding
            key = 'z80_' + binding.owner.removeprefix('z80:') + '_'
            key += format(binding.physical_address, '06x') + '_' + format(index, '03d')
            key += '_' + format(self._counts[index] + 1, '04d')
            result = self._store.write_case(key, metadata, raw)
            if result['status'] == 'budget_exhausted':
                self._exhausted, self._budget_reason = True, result['reason']
                return False
            if result['status'] != 'written':
                raise Z80EntryCaptureError('unknown shared capture writer outcome')
            self._counts[index] += 1
            self._written += 1
            return self._counts[index] < self._maximum
        except BaseException:
            self._failed = True
            raise

    def summary(self):
        return dict(input_collection_only=True, source_entry_candidates=len(self._targets),
            entries_with_written_inputs=sum(count > 0 for count in self._counts),
            written_cases=self._written, matched_public_calls=self._matched_calls,
            nonpublic_or_rebound_CodeTypes_not_captured=self._unqualified_calls,
            foreign_or_legacy_context_calls_not_captured=self._foreign_context_calls,
            exhausted=self._exhausted, budget_reason=self._budget_reason, failed=self._failed,
            shared_monitor=True, shared_store_budget=True, owns_monitor_or_store=False,
            current_R_or_WZ_supplied=False, private_views_captured=False,
            coverage_limits=list(COVERAGE_LIMITS), directly_assemblable=False, strict_credit=0)
