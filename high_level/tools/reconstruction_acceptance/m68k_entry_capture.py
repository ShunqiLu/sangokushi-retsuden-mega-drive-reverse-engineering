"""Opt-in M68000 body-entry inputs and an optional same-monitor pre-CALL peer.

The observer borrows the actual Python callee and its existing Scene/Frame.
It copies RAM and plain carrier storage, never calls a business method, reads
the modeled bus, manufactures a CALL, or promotes a snapshot to acceptance.
The independent pre-CALL observer has its own explicit capture format; it
never reinterprets or repairs a body-entry snapshot. Both use the same store.
"""
from __future__ import annotations

import os
from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, FunctionType

from .entry_capture_catalog import CaptureTarget
from .entry_capture_store import EntryCaptureStore, M68K_CAPTURE_FORMAT
from .entry_monitor import EntryMonitor
from .entry_source_context import ReadonlySourceContext


D_FIELDS = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', 'choice')
A_FIELDS = ('roster', 'candidates', 'controller', 'scan', 'opponent', 'scratch', 'auxiliary', 'stack_cursor')
SCENE_TYPE = 'tools.high_level_scene_flows.domain:SceneState'
MEMORY_TYPE = 'tools.high_level_gameplay_flow.contexts_services:SceneRefreshMemory'
VIEW_TYPES = (
    'tools.high_level_scene_flows.domain:Table',
    'tools.high_level_scene_flows.domain:Cursor',
    'tools.high_level_battle_ai.domain:Table',
    'tools.high_level_battle_ai.domain:Cursor',
)
STACK_TYPES = (VIEW_TYPES[1], VIEW_TYPES[3])


class M68KEntryCaptureError(ValueError):
    """A live snapshot must not hide a changed owner or pretend input proof."""


def _loaded_type(name):
    """Consult already-loaded exact classes, with no import in the callback."""
    module_name, class_name = name.split(':', 1)
    module = sys.modules.get(module_name)
    value = None if module is None else vars(module).get(class_name)
    return value if isinstance(value, type) else None


def _exact_loaded(value, name):
    expected = _loaded_type(name)
    return expected is not None and type(value) is expected


def _path_key(path):
    # All supplied sources are resolved before monitoring. Code filenames are
    # compared lexically only: no source/directory I/O on an entry callback.
    return os.path.normcase(os.path.normpath(str(path)))


def _code_observation(code):
    return dict(filename=code.co_filename, name=code.co_name,
        qualname=code.co_qualname, first_line=code.co_firstlineno,
        flags=code.co_flags, in_process_identity=id(code))


def _object_observation(value):
    actual = type(value)
    return dict(module=actual.__module__, type=actual.__qualname__,
        in_process_identity=id(value))


def _uint_or_missing(value, bits, name, missing):
    if type(value) is int and 0 <= value < 1 << bits:
        return value
    missing.append(name)
    return None


def _carriers(state, frame, missing):
    storage = vars(frame)
    numeric = [_uint_or_missing(storage.get(name), 32, 'initial.D' + str(index), missing)
        for index, name in enumerate(D_FIELDS)]
    addresses, views = [], []
    for index, name in enumerate(A_FIELDS):
        value = storage.get(name)
        allowed = STACK_TYPES if index == 7 else VIEW_TYPES
        if not any(_exact_loaded(value, kind) for kind in allowed):
            missing.append('initial.A' + str(index) + '.actual_same_Scene_view')
            addresses.append(None)
            continue
        view = vars(value)
        if view.get('state') is not state:
            missing.append('initial.A' + str(index) + '.actual_same_Scene_view')
            addresses.append(None)
            continue
        base = _uint_or_missing(view.get('base'), 32, 'initial.A' + str(index), missing)
        addresses.append(base)
        views.append((name, value, base))
    status = _uint_or_missing(storage.get('status'), 5, 'initial.CCR_X', missing)
    return numeric, addresses, status, views


def _outer_slot(raw, stack, missing):
    if stack is None:
        missing.append('original_outer_slot.actual_stack_cursor')
        return dict(source='not_observed_missing_actual_stack_cursor', value=None)
    physical = stack & 0xFFFFFF
    if stack & 1 or not 0xFF0000 <= physical <= 0xFFFFFC:
        missing.append('original_outer_slot.aligned_LONG_in_actual_RAM')
        return dict(source='outside_aligned_RAM_no_bus_read', address=stack, value=None)
    offset = physical - 0xFF0000
    return dict(source='the_same_copied_RAM_without_DATA_event', address=stack,
        byte_offset=offset, value=int.from_bytes(raw[offset:offset + 4], 'big'),
        original_CALL_source_proved=False, continuation_proved=False,
        stack_adjusted_or_consumed=False)


def _scene_counters(storage):
    names = ('reads', 'max_reads', 'samples', 'max_samples', 'sr')
    events = storage.get('events')
    if type(events) is not list:
        raise M68KEntryCaptureError('actual Scene event list is required for a non-mutating snapshot')
    values = tuple(storage.get(name) for name in names)
    if any(type(value) is not int or value < 0 for value in values):
        raise M68KEntryCaptureError('actual finite Scene counters/status are required')
    return values, events, len(events)


def _target_context(target, local):
    """Return only the original normal-Scene owner, not a legacy surrogate."""
    argument = local.get(target.argument_name)
    if target.argument_name == 'memory':
        if not _exact_loaded(argument, MEMORY_TYPE):
            return None
        state = vars(argument).get('state')
    else:
        state = argument
    frame = local.get('frame')
    if not _exact_loaded(state, SCENE_TYPE) or not _exact_loaded(frame, target.frame_type):
        return None
    return state, frame


def _snapshot(target, code, live, instruction_offset, state, frame, source_context=None):
    """Serialize an actual body entry; do not relabel it a pre-CALL fixture."""
    storage = vars(state)
    ram = storage.get('ram')
    if type(ram) is not bytearray or len(ram) != 65536:
        raise M68KEntryCaptureError('actual same-Scene64KiB bytearray required')
    before, events, event_count = _scene_counters(storage)
    data, hardware, services = (storage.get(name) for name in ('data', 'hardware', 'services'))
    missing = [
        'original_CALL_or_tail_entry_protocol',
        'independent_original_execution_reference',
        'actual_hardware_initial_state_and_finite_input_sequence',
        'all_required_own_alias_reachability',
        'all_original_output_observations',
        'atomic_cross_thread_snapshot_proof',
    ]
    if source_context is None:
        missing.append('readonly_DATA_source_artifact_binding')
        source_observation = dict(status='not_attached_at_this_actual_entry',
            source_files_or_bytes_inferred=False)
    else:
        source_observation = source_context.observation(state)
        missing.append('readonly_DATA_source_artifact_files_frozen_and_replay_qualification')
    numeric, addresses, status, views = _carriers(state, frame, missing)
    sr = _uint_or_missing(storage.get('sr'), 16, 'initial.full_SR', missing)
    matches_status = None if sr is None or status is None else status == (sr & 31)
    if matches_status is not True:
        missing.append('initial.full_SR_matches_Frame_CCR_X')
    module = sys.modules.get(target.module)
    function = None if module is None else vars(module).get(target.function)
    public_identity = type(function) is FunctionType and function.__code__ is code
    public_globals = module is not None and live.f_globals is vars(module)
    if not public_identity or not public_globals:
        missing.append('runtime_private_view_to_complete_public_source_CodeType_qualification')
    raw = bytes(ram)
    outer = _outer_slot(raw, addresses[7], missing)
    caller = live.f_back
    try:
        caller_code = None if caller is None else _code_observation(caller.f_code)
    finally:
        del caller
    after, after_events, after_count = _scene_counters(storage)
    if (storage.get('ram') is not ram or bytes(ram) != raw or before != after
            or after_events is not events or after_count != event_count
            or any(storage.get(name) is not value for name, value in
                (('data', data), ('hardware', hardware), ('services', services)))
            or any(vars(frame).get(name) is not value or vars(value).get('state') is not state
                or vars(value).get('base') != base for name, value, base in views)):
        raise M68KEntryCaptureError('live Scene/RAM/carriers changed during entry snapshot; no retry')
    metadata = dict(
        format=M68K_CAPTURE_FORMAT,
        capture_position='actual_PY_START_before_first_Python_body_instruction',
        initial_state_protocol='observed_body_entry_not_historical_pre_CALL',
        entry=target.entry, alias=target.alias, owner=target.owner,
        binding=dict(batch=str(target.binding_batch), pointer=target.source_binding_pointer,
            module=target.module, function=target.function, source=str(target.source_path),
            argument_name=target.argument_name, frame_type=target.frame_type,
            keywords={name: value for name, value in target.keywords},
            qualification='source_catalog_candidate_not_execution_qualification'),
        initial=dict(D=numeric, A=addresses, full_SR=sr, CCR_X=status,
            full_SR_matches_Frame_CCR_X=matches_status,
            RAM_bytes=65536, RAM_source='the_same_existing_Scene_bytearray'),
        runtime=dict(code=_code_observation(code), instruction_offset=instruction_offset,
            public_function_code_identity_matches=public_identity,
            public_module_globals_identity_matches=public_globals,
            caller_Python_code=caller_code, state=_object_observation(state),
            frame=_object_observation(frame),
            data=_object_observation(data), hardware=_object_observation(hardware),
            services=_object_observation(services),
            Scene_reads=before[0], Scene_read_limit=before[1],
            RNG_samples=before[2], RNG_sample_limit=before[3], Scene_events=event_count),
        outer_slot_observation=outer, readonly_DATA_source=source_observation, missing=missing,
        observations=dict(snapshot_stability_checked=True, CPU_DATA_events_added=0,
            CPU_STACK_events_added=0, business_or_device_methods_called=False,
            input_registers_or_RAM_modified=False, original_CALL_undone=False,
            device_clock_or_capacity_refilled=False, private_view_rewritten=False),
        directly_assemblable=False, saved_initial_input_complete=False,
        strict_acceptance_status='not_evaluated', strict_credit=0)
    return metadata, raw


class M68KEntryCapture:
    """Finite optional observer for an existing normal application's lifetime.

    Source preparation and store creation happen before start. The callback
    performs no source import, source read, CPU step or game/device operation.
    Successful storage is candidate input evidence, never acceptance credit.
    """

    def __init__(self, targets, store, *, tool_id: int, max_captures_per_entry: int,
            audio_observer=None, pre_call_observer=None, persist_readonly_DATA=False):
        if (type(targets) is not tuple or not targets
                or any(type(target) is not CaptureTarget for target in targets)):
            raise TypeError('a nonempty explicit tuple of prepared CaptureTarget values is required')
        if type(store) is not EntryCaptureStore:
            raise TypeError('one exact explicitly budgeted EntryCaptureStore required')
        if type(max_captures_per_entry) is not int or max_captures_per_entry <= 0:
            raise ValueError('an explicit positive capture limit per entry required')
        if type(persist_readonly_DATA) is not bool:
            raise TypeError('explicit boolean readonly DATA persistence selection required')
        self._persist_readonly_DATA = persist_readonly_DATA
        if audio_observer is not None:
            from .z80_entry_capture import Z80EntryObserver
            if type(audio_observer) is not Z80EntryObserver or audio_observer.store is not store:
                raise TypeError('the optional exact audio observer must share this same capture store')
        if pre_call_observer is not None:
            from .m68k_pre_call_capture import M68KPreCallObserver
            if type(pre_call_observer) is not M68KPreCallObserver or pre_call_observer.store is not store:
                raise TypeError('the optional exact pre-CALL observer must share this same capture store')
        self._audio_observer = audio_observer
        self._pre_call_observer = pre_call_observer
        self._targets = targets
        self._store = store
        self._maximum = max_captures_per_entry
        self._indices = {}
        identities = set()
        for index, target in enumerate(targets):
            identity = target.owner, target.entry, target.alias
            if identity in identities:
                raise ValueError('duplicate source entry identity cannot receive duplicate credit or inputs')
            identities.add(identity)
            if target.argument_name not in ('state', 'memory'):
                raise ValueError('only explicit state/frame and memory/frame source signatures are supported')
            if not target.source_path.is_absolute():
                raise ValueError('capture source paths must be resolved before monitor startup')
            key = _path_key(target.source_path), target.function
            self._indices.setdefault(key, []).append(index)
        self._counts = [0] * len(targets)
        self._matched_calls = self._ambiguous_calls = self._non_Scene_calls = 0
        self._written = 0
        self._exhausted = False
        self._budget_reason = None
        self._started = self._closed = self._failed = False
        self._close_attempted = False
        self._close_outcome = None
        self._receipt = None
        self._thread = threading.current_thread()
        self._source_context = None
        self._source_context_attachment_attempted = False
        self._monitor = EntryMonitor(self._on_entry, tool_id=tool_id)

    def attach_source_context(self, source, scene):
        """Bind the actual App's selected DATA once, after its successful open.

        Earlier snapshots stay unchanged and missing. Optional persistence
        writes the same immutable DATA once within the existing store budget;
        no old input is read, rewritten or promoted to independent evidence.
        """
        if (threading.current_thread() is not self._thread or not self._started
                or not self._monitor.active or self._closed or self._failed
                or self._close_attempted or self._source_context_attachment_attempted):
            raise M68KEntryCaptureError('one live same-thread post-open source attachment required')
        self._source_context_attachment_attempted = True
        try:
            self._source_context = ReadonlySourceContext(source, scene,
                project_root=self._store.project_root)
            if self._persist_readonly_DATA:
                result = self._source_context.persist_payload(scene, self._store)
                if result['status'] == 'budget_exhausted':
                    self._exhausted = True
                    self._budget_reason = result['reason']
        except BaseException:
            self._failed = True
            raise

    def start(self):
        if self._started or self._close_attempted:
            raise M68KEntryCaptureError('entry capture is single-use')
        self._started = True
        try:
            self._monitor.start()
        except BaseException:
            self._failed = True
            raise
        return self

    def _needed(self, indices):
        return not self._exhausted and any(self._counts[index] < self._maximum for index in indices)

    def _on_entry(self, code: CodeType, live: FrameType, instruction_offset: int):
        if self._exhausted or self._closed:
            return False
        if self._pre_call_observer is not None and self._pre_call_observer.handles(code):
            try:
                keep = self._pre_call_observer.on_entry(code, live, instruction_offset,
                    source_context=self._source_context)
                pre_call = self._pre_call_observer.summary()
                if pre_call['exhausted']:
                    self._exhausted = True
                    self._budget_reason = pre_call['budget_reason']
                    return False
                return keep
            except BaseException:
                self._failed = True
                raise
        if self._audio_observer is not None and self._audio_observer.handles(code):
            try:
                return self._audio_observer.on_entry(code, live, instruction_offset)
            except BaseException:
                self._failed = True
                raise
        if code.co_qualname != code.co_name or not os.path.isabs(code.co_filename):
            return False
        indices = self._indices.get((_path_key(code.co_filename), code.co_name))
        if indices is None or not self._needed(indices):
            return False
        local = live.f_locals
        matches = []
        for index in indices:
            target = self._targets[index]
            if all(type(local.get(name)) is type(expected) and local[name] == expected
                    for name, expected in target.keywords):
                matches.append(index)
        if len(matches) != 1:
            if matches:
                self._ambiguous_calls += 1
            return True
        index = matches[0]
        if self._counts[index] >= self._maximum:
            return self._needed(indices)
        target = self._targets[index]
        context = _target_context(target, local)
        if context is None:
            # A legacy call through the same business function is not a
            # normal Scene input and must not disable later genuine entries.
            self._non_Scene_calls += 1
            return True
        self._matched_calls += 1
        try:
            metadata, raw = _snapshot(target, code, live, instruction_offset, *context,
                source_context=self._source_context)
            key = 'm68000_' + format(target.entry, '06x') + '_' + format(index, '03d')
            key += '_' + format(self._counts[index] + 1, '04d')
            result = self._store.write_case(key, metadata, raw)
            if result['status'] == 'budget_exhausted':
                self._exhausted = True
                self._budget_reason = result['reason']
                return False
            if result['status'] != 'written':
                raise M68KEntryCaptureError('unknown explicit capture writer outcome')
            self._counts[index] += 1
            self._written += 1
            return self._needed(indices)
        except BaseException:
            self._failed = True
            raise

    def summary(self):
        audio = None if self._audio_observer is None else self._audio_observer.summary()
        pre_call = None if self._pre_call_observer is None else self._pre_call_observer.summary()
        return dict(input_collection_only=True, source_entry_candidates=len(self._targets),
            entries_with_written_inputs=sum(count > 0 for count in self._counts),
            written_cases=self._written, matched_calls=self._matched_calls,
            ambiguous_calls_not_captured=self._ambiguous_calls,
            legacy_or_foreign_state_calls_not_captured=self._non_Scene_calls,
            exhausted=self._exhausted, budget_reason=self._budget_reason,
            started=self._started, closed=self._closed,
            failed=self._failed or self._monitor.failed,
            post_open_readonly_source_attached=self._source_context is not None,
            audio=audio, pre_call=pre_call,
            total_written_cases=self._written + (0 if audio is None else audio['written_cases'])
                + (0 if pre_call is None else pre_call['written_cases']),
            directly_assemblable=False, strict_credit=0)

    def close(self, *, outcome: str) -> Path:
        """Try both cleanup stages, including a partially failed startup."""
        if self._closed:
            if outcome != self._close_outcome:
                raise M68KEntryCaptureError('a closed input collection outcome cannot be rewritten')
            return self._receipt
        if self._close_attempted:
            raise M68KEntryCaptureError('failed entry capture cleanup cannot be replayed')
        self._close_attempted = True
        error = None
        try:
            self._monitor.close()
        except BaseException as failure:
            error = failure
        try:
            self._receipt = self._store.close(outcome)
        except BaseException as failure:
            if error is None:
                error = failure
            else:
                error.add_note('Entry capture store close also failed: ' + str(failure))
        if error is not None:
            self._failed = True
            raise error
        self._closed = True
        self._close_outcome = outcome
        return self._receipt
