"""Finite real-helper pre-CALL inputs, borrowing one existing monitor/store.

Only prepared helper forms may supply actual locals. The helper has not yet
decremented A7 or written its target continuation. Snapshots neither undo a
CALL nor become SavedInputCase values or independent behavioral evidence.
"""
from __future__ import annotations

import sys
import threading
from types import CodeType, FrameType, FunctionType
import weakref

from .entry_capture_store import EntryCaptureStore, M68K_PRE_CALL_CAPTURE_FORMAT
from .entry_source_context import ReadonlySourceContext
from .m68k_entry_capture import (
    SCENE_TYPE, _carriers, _code_observation, _loaded_type, _object_observation,
    _outer_slot, _scene_counters, _uint_or_missing,
)
from .pre_call_capture_catalog import PreparedPreCallIndex, source_entry_reference_observation
from .pre_call_source_views import PreparedHelperForm, match_helper_form


FRAME_TYPE = 'tools.high_level_battle_ai.contexts_first_deployment:FirstDeploymentFrame'
UNSUPPLIED_QUALIFICATION = (
    'actual_hardware_initial_state_and_finite_input_sequence',
    'readonly_DATA_artifact_files_frozen_and_replay_qualification',
    'actual_caller_CodeType_to_original_CALL_source_qualification',
    'current_complete_callee_CodeType_globals_and_execution_closure',
    'private_globals_and_transitive_callee_qualification',
    'all_required_own_aliases_actually_reached_for_this_input',
    'explicit_future_stack_window_and_independent_instruction_DATA_budgets',
    'independent_original_M68K_execution_reference',
    'all_original_output_observations',
    'atomic_cross_thread_snapshot_proof',
)


class M68KPreCallCaptureError(ValueError):
    """A changed live owner or failed snapshot is not retried or repaired."""


def _route_identity(route):
    """One physical CALL/callee identity, independent of helper or source view."""
    call, callee = route.original_call, route.actual_callee
    return (call.caller, call.target, call.continuation, callee.actual_entry,
        callee.module, callee.function, callee.argument_name, callee.keywords)


def _same_storage(value, before):
    """Compare existing plain member identities without invoking their methods."""
    after = vars(value)
    return after.keys() == before.keys() and all(after[name] is member for name, member in before.items())


def _route_observation(index, route):
    call, callee = route.original_call, route.actual_callee
    observation = dict(batch=str(index.binding_batch),
        original_call=dict(source=str(call.source), line=call.line, statement=call.statement,
            caller=call.caller, target=call.target, continuation=call.continuation,
            proof_kind='prepared_explicit_original_direct_CALL_not_continuation_arithmetic'),
        actual_callee=dict(entry=callee.actual_entry, module=callee.module,
            function=callee.function, argument_name=callee.argument_name,
            keywords={name: value for name, value in callee.keywords},
            source=str(callee.source_path), matching_capture_owner=callee.matching_capture_owner,
            qualification='prepared_complete_source_reference_not_loaded_callee_qualification'),
        retained_requirements=[dict(case=row.case, batch_pointer=row.batch_pointer,
            required_aliases=list(row.required_aliases), actually_reached_here=False)
            for row in route.retained_requirements],
        complete_helper_and_callee_ASTs_retained_in_prepared_index=True,
        source_files_frozen=False, actual_entry_not_replaced_by_required_alias=True)
    if route.source_entry_references:
        observation['source_entry_references'] = [source_entry_reference_observation(row)
            for row in route.source_entry_references]
    return observation


def _readonly_source(source_context, state, missing):
    if source_context is None:
        missing.append('readonly_DATA_source_artifact_binding')
        return dict(status='not_attached_at_this_actual_entry', source_files_or_bytes_inferred=False)
    if type(source_context) is not ReadonlySourceContext:
        raise M68KPreCallCaptureError('only the actual same-App readonly source context is accepted')
    return source_context.observation(state)


def _prepare_vdp_capture():
    """Import the explicit codec before monitoring, never from its callback."""
    from ..high_level_scene_flows.domain import HardwareBus
    from ..high_level_video.hardware_vdp import (
        SceneVdpHardwareBus, VdpController, VdpMemory, SceneRamDmaSource, SceneDataDmaSource,
    )
    from ..high_level_video.vdp_state import FORMAT, snapshot_vdp_state, encode_vdp_state
    if FORMAT != 'g5510-vdp-command-memory-state-v1':
        raise M68KPreCallCaptureError('the explicit VDP command/memory codec format differs')
    types = (HardwareBus, SceneVdpHardwareBus, VdpController, VdpMemory, SceneRamDmaSource, SceneDataDmaSource)
    functions = []
    for function in (snapshot_vdp_state, encode_vdp_state):
        if type(function) is not FunctionType:
            raise M68KPreCallCaptureError('actual unwrapped VDP snapshot/codec source functions required')
        module = sys.modules.get(function.__module__)
        if (module is None or function.__globals__ is not vars(module)
                or vars(module).get(function.__name__) is not function):
            raise M68KPreCallCaptureError('actual unwrapped VDP snapshot/codec source owners required')
        functions.append((function, function.__code__, module))
    return types, tuple(functions)


def _require_vdp_capture_sources(support):
    types, functions = support
    for actual in types:
        if _loaded_type(actual.__module__ + ':' + actual.__qualname__) is not actual:
            raise M68KPreCallCaptureError('a prepared VDP capture class owner changed')
    for function, code, module in functions:
        if (sys.modules.get(function.__module__) is not module or function.__code__ is not code
                or function.__globals__ is not vars(module)
                or vars(module).get(function.__name__) is not function):
            raise M68KPreCallCaptureError('a prepared VDP snapshot/codec owner changed')


def _snapshot_vdp_source(state, support):
    """Read only the actual same-Scene chain; identity alone gives no credit."""
    _require_vdp_capture_sources(support)
    bus_type, vdp_bus_type, controller_type, memory_type, ram_dma_type, data_dma_type = support[0]
    owner, seen, chain, candidates = vars(state).get('hardware'), set(), [], []
    while owner is not None:
        actual = type(owner)
        if (len(chain) >= 64 or id(owner) in seen or not isinstance(owner, bus_type)
                or _loaded_type(actual.__module__ + ':' + actual.__qualname__) is not actual):
            raise M68KPreCallCaptureError('unsupported, cyclic or non-public actual Scene hardware chain')
        seen.add(id(owner))
        members = dict(vars(owner))
        chain.append((owner, members))
        if actual is vdp_bus_type:
            candidates.append(owner)
        owner = members.get('devices')
    if len(candidates) != 1:
        raise M68KPreCallCaptureError('one unique actual SceneVdpHardwareBus owner required')
    bus = candidates[0]
    members = vars(bus)
    controller = members.get('controller')
    if members.get('scene') is not state or type(controller) is not controller_type:
        raise M68KPreCallCaptureError('the actual VDP bus/controller must belong to this same Scene')
    stalled = members.get('_cpu_dma_stall_active')
    if type(stalled) is not bool or stalled:
        raise M68KPreCallCaptureError('pre-CALL VDP capture cannot reconstruct an active/unknown CPU DMA hold')
    controller_members = dict(vars(controller))
    dma_source = controller_members.get('dma_source')
    if type(dma_source) not in (ram_dma_type, data_dma_type) or vars(dma_source).get('state') is not state:
        raise M68KPreCallCaptureError('actual VDP DMA source must retain this same Scene, not a copied bus')
    memory = controller_members.get('memory')
    if type(memory) is not memory_type:
        raise M68KPreCallCaptureError('the actual controller must retain its exact complete VdpMemory backing owner')
    memory_members, dma_members = dict(vars(memory)), dict(vars(dma_source))
    snapshotter, encoder = (row[0] for row in support[1])
    snapshot = snapshotter(controller)
    metadata, payload = encoder(snapshot)
    if (type(metadata) is not dict or type(payload) is not bytes or len(payload) != 65776
            or metadata.get('format') != 'g5510-vdp-command-memory-state-v1'
            or metadata.get('scope') != 'vdp_command_memory_effects_only'
            or metadata.get('external_timing_FIFO_IRQ_included') is not False):
        raise M68KPreCallCaptureError('the explicit complete command/memory snapshot codec differs')
    return dict(snapshot=snapshot, metadata=metadata, payload=payload, chain=tuple(chain),
        bus=bus, controller=controller, controller_members=controller_members,
        memory=memory, memory_members=memory_members, dma_source=dma_source, dma_members=dma_members,
        cpu_hold=stalled)


def _require_vdp_source_stable(state, support, captured):
    """The copied command/memory state and every actual owner must stay put."""
    _require_vdp_capture_sources(support)
    chain = captured['chain']
    if (not chain or vars(state).get('hardware') is not chain[0][0]
            or any(not _same_storage(owner, members) for owner, members in chain)
            or not _same_storage(captured['controller'], captured['controller_members'])
            or not _same_storage(captured['memory'], captured['memory_members'])
            or not _same_storage(captured['dma_source'], captured['dma_members'])
            or support[1][0][0](captured['controller']) != captured['snapshot']):
        raise M68KPreCallCaptureError('live VDP ownership/command/memory changed during the pre-CALL snapshot; no retry')


def _vdp_observation(captured):
    return dict(status='captured_command_memory_scope_only',
        actual_same_Scene_hardware_chain=True,
        owner_chain=[_object_observation(owner) for owner, _ in captured['chain']],
        actual_VDP_bus=_object_observation(captured['bus']),
        controller=_object_observation(captured['controller']),
        memory=_object_observation(captured['memory']),
        dma_source=_object_observation(captured['dma_source']),
        status_provider=_object_observation(captured['controller_members'].get('status')),
        CPU_DMA_hold_active=captured['cpu_hold'], snapshot_stability_checked=True,
        command_memory_state_captured=True, device_state_qualified=False,
        complete_device_state=False, external_timing_FIFO_IRQ_captured=False,
        other_hardware_owners_captured=False, future_device_sequence_supplied=False,
        missing=['VDP_status_HV_FIFO_open_bus_timing_and_IRQ_state',
            'all_other_device_states_and_explicit_finite_future_events',
            'independent_reference_device_execution_and_full_output_observations'])


def _snapshot(index, route, form, code, live, instruction_offset, state, frame, source_context):
    """Read plain storage only; current A7 still belongs to the original caller."""
    storage, frame_storage = vars(state), dict(vars(frame))
    ram = storage.get('ram')
    if type(ram) is not bytearray or len(ram) != 65536:
        raise M68KPreCallCaptureError('actual same-Scene64KiB RAM bytearray required')
    before, events, event_count = _scene_counters(storage)
    owners = {name: storage.get(name) for name in ('data', 'hardware', 'services')}
    missing = list(UNSUPPLIED_QUALIFICATION)
    source = _readonly_source(source_context, state, missing)
    numeric, addresses, status, views = _carriers(state, frame, missing)
    view_storage = [(view, dict(vars(view))) for _, view, _ in views]
    sr = _uint_or_missing(storage.get('sr'), 16, 'initial.full_SR', missing)
    matches_status = None if sr is None or status is None else status == (sr & 31)
    if matches_status is not True:
        missing.append('initial.full_SR_matches_Frame_CCR_X')
    raw = bytes(ram)
    caller_slot = _outer_slot(raw, addresses[7], missing)
    caller_slot.update(role='caller_existing_current_A7_slot_not_target_callee_continuation',
        target_callee_CALL_executed=False, target_continuation_written=False)
    caller = live.f_back
    try:
        caller_code = None if caller is None else _code_observation(caller.f_code)
    finally:
        del caller
    if caller_code is None:
        missing.append('runtime_actual_Python_caller_code_observation')
    after, after_events, after_count = _scene_counters(storage)
    if (storage.get('ram') is not ram or len(ram) != 65536 or bytes(ram) != raw
            or before != after or after_events is not events or after_count != event_count
            or any(storage.get(name) is not owner for name, owner in owners.items())
            or not _same_storage(frame, frame_storage)
            or any(not _same_storage(view, saved) for view, saved in view_storage)
            or type(state) is not _loaded_type(SCENE_TYPE)
            or type(frame) is not _loaded_type(FRAME_TYPE)):
        raise M68KPreCallCaptureError('live pre-CALL RAM/counters/frame/view ownership changed; no retry')
    call, callee = route.original_call, route.actual_callee
    metadata = dict(format=M68K_PRE_CALL_CAPTURE_FORMAT,
        capture_position='actual_helper_PY_START_before_first_body_instruction_and_original_CALL_stack_decrement',
        initial_state_protocol='actual_original_caller_pre_CALL_no_stack_undo_or_reconstruction',
        entry=callee.actual_entry, owner=callee.matching_capture_owner,
        original_caller=call.caller, target=call.target, continuation=call.continuation,
        binding=_route_observation(index, route),
        initial=dict(D=numeric, A=addresses, full_SR=sr, CCR_X=status,
            full_SR_matches_Frame_CCR_X=matches_status, RAM_bytes=65536,
            RAM_source='the_same_existing_Scene_bytearray_before_original_CALL',
            A7_role='original_caller_current_stack_before_target_CALL'),
        helper=dict(key=form.helper.key, module=form.helper.module,
            function=form.helper.function, source=str(form.helper.source_path),
            source_form=form.source_form, source_transformer=form.source_transformer,
            prepared_form_CodeType_identity_matches=code is form.candidate_code,
            original_public_code=_code_observation(form.original_code),
            executing_code=_code_observation(code),
            original_owner=_object_observation(form.original),
            executing_globals_is_original_globals=live.f_globals is form.original.__globals__,
            match_helper_form_qualified=True),
        runtime=dict(instruction_offset=instruction_offset, caller_Python_code=caller_code,
            state=_object_observation(state), frame=_object_observation(frame),
            data=_object_observation(owners['data']), hardware=_object_observation(owners['hardware']),
            services=_object_observation(owners['services']),
            Scene_reads=before[0], Scene_read_limit=before[1],
            RNG_samples=before[2], RNG_sample_limit=before[3], Scene_events=event_count),
        caller_existing_slot_observation=caller_slot, readonly_DATA_source=source,
        observations=dict(snapshot_stability_checked=True, CPU_DATA_events_added=0,
            CPU_STACK_events_added=0, business_or_device_methods_called=False,
            helper_or_callee_executed_by_observer=False, original_CALL_executed=False,
            original_CALL_undone=False, input_registers_or_RAM_modified=False,
            device_clock_or_capacity_refilled=False, private_view_rewritten=False),
        missing=missing, saved_initial_input_complete=False, directly_assemblable=False,
        strict_acceptance_status='not_evaluated', strict_credit=0)
    return metadata, raw


class M68KPreCallObserver:
    """One same-thread/App component; the root collector owns monitor/cleanup."""

    def __init__(self, index, forms, store, *, max_captures_per_entry, capture_vdp_state=False):
        if type(index) is not PreparedPreCallIndex:
            raise TypeError('one exact immutable PreparedPreCallIndex required')
        if (type(forms) is not tuple or not forms
                or any(type(form) is not PreparedHelperForm for form in forms)):
            raise TypeError('a nonempty tuple of prepared exact helper forms required')
        if type(store) is not EntryCaptureStore:
            raise TypeError('the root collector same exact finite EntryCaptureStore required')
        if type(max_captures_per_entry) is not int or max_captures_per_entry <= 0:
            raise ValueError('an explicit positive capture limit per original CALL/callee required')
        if type(capture_vdp_state) is not bool:
            raise TypeError('explicit boolean pre-CALL VDP command/memory capture selection required')
        if any(form.helper not in index.helpers or type(form.candidate_code) is not CodeType
                or type(form.original_code) is not CodeType for form in forms):
            raise TypeError('helper forms must belong to this prepared source directory')
        self._index, self._forms, self._store = index, forms, store
        self._vdp_capture = _prepare_vdp_capture() if capture_vdp_state else None
        self._maximum = max_captures_per_entry
        self._names = frozenset(form.candidate_code.co_name for form in forms)
        helper_keys = {form.helper.key for form in forms}
        identities = dict.fromkeys(_route_identity(route) for route in index.routes if route.helper in helper_keys)
        self._numbers = {key: number for number, key in enumerate(identities)}
        self._counts = dict.fromkeys(identities, 0)
        self._written = self._matched = self._unqualified = self._foreign = self._unmapped = 0
        self._exhausted = self._failed = False
        self._budget_reason = None
        self._thread, self._scene = threading.current_thread(), None

    @property
    def store(self):
        """Exact shared-store identity; no new store or budget is allocated."""
        return self._store

    def handles(self, code):
        """Coarse prepared co_name selection only, not source qualification."""
        return type(code) is CodeType and code.co_name in self._names

    def _needed(self):
        return not self._exhausted and any(count < self._maximum for count in self._counts.values())

    def on_entry(self, code, live, instruction_offset, *, source_context=None):
        if not self.handles(code) or self._exhausted:
            return False
        try:
            return self._capture_entry(code, live, instruction_offset, source_context)
        except BaseException:
            self._failed = True
            raise

    def _capture_entry(self, code, live, instruction_offset, source_context):
        if (threading.current_thread() is not self._thread or type(live) is not FrameType
                or live.f_code is not code or type(instruction_offset) is not int or instruction_offset < 0):
            raise M68KPreCallCaptureError('one actual same-thread helper PY_START frame required')
        form = match_helper_form(self._forms, code, live)
        if form is None:
            self._unqualified += 1
            return self._needed()
        local = live.f_locals
        state, frame = local.get('state'), local.get('frame')
        if (type(state) is not _loaded_type(SCENE_TYPE) or type(frame) is not _loaded_type(FRAME_TYPE)
                or (self._scene is not None and self._scene() is not state)):
            self._foreign += 1
            return self._needed()
        target, continuation = local.get('target'), local.get('continuation')
        if any(type(value) is not int or not 0 <= value <= 0xFFFFFF for value in (target, continuation)):
            self._unmapped += 1
            return self._needed()
        lookup = self._index.lookup(form.helper.key, target, continuation, entry_kind='direct_CALL')
        if (lookup.status != 'unique_source_candidate_not_runtime_or_input_qualification'
                or len(lookup.candidates) != 1):
            self._unmapped += 1
            return self._needed()
        route = lookup.candidates[0]
        identity = _route_identity(route)
        if identity not in self._counts:
            raise M68KPreCallCaptureError('a live source lookup escaped its prepared capture identities')
        if self._counts[identity] >= self._maximum:
            return self._needed()
        if self._scene is None:
            self._scene = weakref.ref(state)
        self._matched += 1
        vdp = None if self._vdp_capture is None else _snapshot_vdp_source(state, self._vdp_capture)
        metadata, raw = _snapshot(self._index, route, form, code, live,
            instruction_offset, state, frame, source_context)
        if vdp is not None:
            _require_vdp_source_stable(state, self._vdp_capture, vdp)
            metadata['VDP_state_capture'] = _vdp_observation(vdp)
            metadata['missing'].extend(metadata['VDP_state_capture']['missing'])
        key = 'm68000_precall_' + format(route.original_call.caller, '06x')
        key += '_' + format(target, '06x') + '_' + format(self._numbers[identity], '03d')
        key += '_' + format(self._counts[identity] + 1, '04d')
        if vdp is None:
            result = self._store.write_case(key, metadata, raw)
        else:
            result = self._store.write_vdp_state(key, metadata, raw,
                vdp_metadata=vdp['metadata'], vdp_payload=vdp['payload'])
        if result['status'] == 'budget_exhausted':
            self._exhausted, self._budget_reason = True, result['reason']
            return False
        if result['status'] != 'written':
            raise M68KPreCallCaptureError('unknown explicit shared capture writer outcome')
        self._counts[identity] += 1
        self._written += 1
        return self._needed()

    def summary(self):
        result = dict(input_collection_only=True, prepared_helper_forms=len(self._forms),
            original_CALL_callee_candidates=len(self._counts),
            entries_with_written_inputs=sum(count > 0 for count in self._counts.values()),
            written_cases=self._written, matched_calls=self._matched,
            unqualified_helper_calls_not_captured=self._unqualified,
            foreign_or_legacy_context_calls_not_captured=self._foreign,
            missing_or_ambiguous_original_CALL_calls_not_captured=self._unmapped,
            exhausted=self._exhausted, budget_reason=self._budget_reason, failed=self._failed,
            observer_owns_monitor_or_store_lifecycle=False, original_CALL_undone=False,
            saved_initial_input_complete=False, directly_assemblable=False, strict_credit=0)
        if self._vdp_capture is not None:
            result['VDP_command_memory_capture'] = dict(enabled=True, payload_bytes_per_case=65776,
                scope='vdp_command_memory_effects_only', device_state_qualified=False,
                external_timing_FIFO_IRQ_captured=False, shares_existing_case_and_store_budget=True)
        return result
