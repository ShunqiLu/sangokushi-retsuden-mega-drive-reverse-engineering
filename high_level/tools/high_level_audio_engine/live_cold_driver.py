"""Reversible whole195 live factory; no old runner invocation or prefix replay.

Only build_live_cold_driver executes a new cold path. Importing this candidate
does not run it. The same successful body is retained at one added yield, so
its original finally/close is deferred until the explicit live rig finish.
"""
import ast
import copy
from dataclasses import dataclass
import inspect
import json
from pathlib import Path
import threading
from types import FunctionType, CodeType

from tools.high_level_audio_engine import run_unified_cold_driver_fixture as original195
from tools.high_level_audio_engine.domain import AudioBoundary, byte
from tools.high_level_scene_flows.domain import Boundary, HardwareBus
from tools.high_level_video.finite_edges import FiniteVideoEdgeSchedule, SuppliedVideoEdge
from tools.high_level_video.frame_interrupts import VideoBusState, OriginalInterruptRuntime
from tools.high_level_video.hardware_vdp import SceneDataDmaSource


def _dump(node):
    return ast.dump(node, include_attributes=False)


def _one(nodes, description):
    if len(nodes) != 1:
        raise Boundary('one exact195 '+description+' required')
    return nodes[0]


def _read_refresh(control, providers, counts, previous):
    """Same finite reader from initial cold platform through later driver polls.

    Values are external observations. The actual known IFF2 supplies PV; the
    explicit probable register X/Y rule is separate from any M1-cycle model.
    """
    byte(previous)
    ordinal = counts['refresh']
    observations = providers['refresh_observations']
    if ordinal >= len(observations):
        raise AudioBoundary('live rig finite externally supplied R observations exhausted')
    observation = observations[ordinal]
    if type(observation) is not dict or set(observation) != {'value'}:
        raise ValueError('one explicit R value, not precomputed conditions or inferred M1 history, required')
    value = byte(observation['value'])
    iff2 = control.control.iff2
    if type(iff2) is not bool:
        raise AudioBoundary('real IFF2 must be known for the supplied LD A,R observation')
    counts['refresh'] += 1
    flags = (previous & 1) | (value & 0xA8) | (0x40 if value == 0 else 0) | (4 if iff2 else 0)
    return value, flags


def _base_bus():
    """Reserve only the not-yet-owned PSG aperture, before creating any device.

    These are the actual HardwareBus default ranges, minus C00010..C00018.
    No actual device, mapping or prior Scene is removed or mutated.
    """
    expected_default = ((0xA00000,0xA20000),(0xC00000,0xC00020))
    if HardwareBus().ranges != expected_default:
        raise Boundary('public bare HardwareBus default range contract changed')
    return HardwareBus(((0xA00000,0xA20000),(0xC00000,0xC00010),(0xC00018,0xC00020)))


def _edges(video_events, devices, extension):
    if any(start < 0xC00018 and 0xC00010 < end for start,end in devices.ranges):
        raise Boundary('PSG must remain an unmapped aperture before its actual first mapping')
    edges = tuple(SuppliedVideoEdge(row['reason'], VideoBusState(**row['bus_state']))
        for row in extension['video_edges'])
    return FiniteVideoEdgeSchedule(video_events, edges, devices)


def _bind_data_dma(controller, state):
    # This is before the original initial video.bind_scene, not a hot swap of
    # an existing RAM or source owner after cold startup has begun.
    if controller.dma_source is not None:
        raise Boundary('fresh factory controller already owns an unexpected DMA source')
    controller.dma_source = SceneDataDmaSource(state)


@dataclass
class LiveColdDriverRig:
    """Retained real entry points; caller supplies every next input/event.

    No title, IRQ, mailbox, timer loop or CPU instruction is run by this object.
    parent_program is held privately and resumed only for its original finally.
    """
    scene: object
    pads: tuple
    memory: object
    vdp: object
    video_events: object
    edge_schedule: object
    write_events: object
    psg_hardware: object
    stacks: object
    reset: object
    main_session: object
    main_waiting: object
    startup: object
    audio_point: object
    sound: object
    audio: object
    control: object
    fm: object
    psg: object
    devices: object
    source: object
    hardware_schedule: object
    interrupt_runtime: object
    boot_checkpoint: dict
    receipt: dict
    source_contract: dict
    counts: dict
    thread: int
    _parent_program: object = None
    closed: bool = False

    def require_live(self):
        if (self.closed or threading.get_ident() != self.thread or self._parent_program is None
                or self._parent_program.gi_running or self.sound.scene is not self.scene
                or self.sound.audio_state is not self.audio or self.audio.bus.devices is not self.devices
                or self.devices.fm is not self.fm or self.devices.psg_write.__self__ is not self.psg
                or self.reset.main_session is not self.main_session):
            raise Boundary('live cold-to-driver rig owner/thread/Scene is no longer available')
        return self

    def finish(self, *, outcome, evidence):
        """Explicit end of the caller scope; no old game prefix is replayed.

        Caller closes any transferred AudioDriverLoopSession/WZ service first.
        The retained generator is resumed after its sole yield, entering only
        the original finally and original return. Never close it by throwing
        GeneratorExit into the original broad business-boundary catcher.
        """
        self.require_live()
        if type(outcome) is not str or not outcome or type(evidence) is not dict:
            raise ValueError('explicit final caller outcome and compact evidence required')
        if self.control._frame_session is not None or getattr(self.audio,'mailbox_wz_service',None) is not None:
            raise Boundary('caller must release its actual loop/WZ ownership before finishing the live fixture')
        self.receipt.update(status=outcome, stage='caller_live_scope_finished',
            live_scope_evidence=evidence, original195_checkpoint_is_historical_entry_not_final_state=True)
        try:
            next(self._parent_program)
        except StopIteration as completed:
            if completed.value is not self.receipt:
                raise Boundary('derived whole195 final return changed')
        else:
            raise Boundary('derived whole195 has an unexpected second yield')
        self.closed = True
        return self.receipt


def _capture(values, extension, contract, expected_profile):
    if values['profile'] != expected_profile:
        raise Boundary('explicit live profile changed during source-derived cold construction')
    startup, reset, state = values['startup'], values['reset'], values['state']
    events, schedule, hardware = values['video_events'], values['schedule'], values['hardware']
    edges = hardware.devices
    if (type(edges) is not FiniteVideoEdgeSchedule or edges.devices is not values['write_events']
            or hardware.psg is not values['psg'] or not startup.main_loop_points
            or not startup.timer_b_continuation or startup.closed or startup.program is None
            or startup.waiting.pc != 0x6F or reset.main_session.waiting.poll != 0x3BC
            or values['provider_counts']['refresh'] != 0
            or values['audio'].platform.refresh_reader is not values['refresh']
            or values['handoff'].refresh_provider_retained is not True):
        raise Boundary('exact same-reader/device live006F plus true main3BC checkpoint required')
    if events.dma_slots or edges.consumed:
        raise Boundary('original195 prefix DMA must finish while future VBlank edge plan remains unconsumed')
    dma_units = tuple(extension['future_DMA_units'])
    permits = tuple(extension['future_bus_transfer_permits'])
    if any(type(value) is not int or not 0 <= value <= 65536 for value in dma_units):
        raise ValueError('explicit finite future DMA transfer-unit grants required')
    if any(type(value) is not bool for value in permits):
        raise ValueError('explicit finite future bus-transfer permit sequence required')
    if schedule._permit_index != len(schedule.bus_transfer_permits):
        raise Boundary('all declared cold-prefix bus permits must have been consumed before the new event phase')
    # Publish only the caller-declared next finite phase, after every original
    # 195 prefix check has run unchanged. This grants no current transfer/ACK,
    # advances no chip, clears no busy bit and performs no software write.
    events.dma_slots.extend(dma_units)
    schedule.bus_transfer_permits = schedule.bus_transfer_permits + permits
    checkpoint = copy.deepcopy(values['receipt'])
    values['receipt'].update(status='live_cold_driver_rig_retained_at_actual_first3BC_and006F',
        live_factory_source_contract=contract, live_boot_checkpoint=checkpoint,
        explicit_next_event_phase=dict(DMA_units=list(dma_units), bus_transfer_permits=list(permits),
            video_edges=extension['video_edges']), no_current_transfer_or_IRQ_granted_by_phase_publication=True)
    return LiveColdDriverRig(state,values['inputs_bus'].ports,values['memory'],values['vdp'],events,
        edges,values['write_events'],hardware,values['stacks'],reset,reset.main_session,
        reset.main_session.waiting,startup,startup.waiting,values['sound'],values['audio'],values['control'],
        values['fm'],values['psg'],values['devices'],values['source'],schedule,OriginalInterruptRuntime(state),
        checkpoint,values['receipt'],contract,
        dict(transfers=values['transfer_counts'],FM_busy=values['busy_grants'],providers=values['provider_counts']),
        threading.get_ident())


def _derived_factory(profile):
    original = original195.run
    if (type(original) is not FunctionType or original.__module__ != original195.__name__
            or original.__name__ != 'run' or inspect.isgeneratorfunction(original)):
        raise Boundary('exact actual public195 whole runner function required')
    source_lines, source_line = inspect.getsourcelines(original)
    parsed = ast.parse(''.join(source_lines))
    ast.increment_lineno(parsed, source_line-1)
    function = _one(parsed.body, 'complete source function')
    if type(function) is not ast.FunctionDef:
        raise Boundary('one ordinary whole195 source function required')
    # CPython3.13 records module-import knowledge in some global/attribute
    # encodings. Compile the complete current module without executing it,
    # so both nested source locations AND the actual symbol context remain.
    module_source = ast.parse(inspect.getsource(original195))
    source_run = _one([node for node in module_source.body
        if type(node) is ast.FunctionDef and node.name=='run'], 'module-context run owner')
    if (_dump(source_run)!=_dump(function) or source_run.lineno!=source_line
            or source_line!=original.__code__.co_firstlineno):
        raise Boundary('complete module and actual function source locations differ')
    compiled_module = compile(module_source, original.__code__.co_filename, 'exec')
    plain = _one([value for value in compiled_module.co_consts
        if type(value) is CodeType and value.co_name=='run'], 'compiled module-context run code')
    for field in ('co_code','co_consts','co_names','co_varnames','co_argcount','co_kwonlyargcount'):
        if getattr(plain,field) != getattr(original.__code__,field):
            raise Boundary('public195 loaded runner differs from its complete current source')
    if any(type(node) is ast.Name and node.id.startswith('_live_') for node in ast.walk(function)):
        raise Boundary('original195 competes with private live-view names')
    view = copy.deepcopy(function)
    undo = {}

    def replace_record(node, change):
        before = copy.deepcopy(node)
        change(node)
        key = _dump(node)
        if key in undo:
            raise Boundary('nonunique live-view inverse replacement')
        undo[key] = before

    calls = lambda name: [node for node in ast.walk(view) if type(node) is ast.Call
        and type(node.func) is ast.Name and node.func.id == name]
    vdp_call = _one(calls('SceneVdpHardwareBus'), 'VDP construction')
    if _dump(vdp_call.args[1]) != _dump(ast.parse('HardwareBus()',mode='eval').body):
        raise Boundary('exact195 bare default bus construction changed')
    replace_record(vdp_call, lambda node: node.args.__setitem__(1,ast.parse('_live_base_bus()',mode='eval').body))
    psg_call = _one(calls('ScenePsgHardwareBus'), 'outer PSG construction')
    if (_dump(psg_call.args[1]) != _dump(ast.Name(id='write_events',ctx=ast.Load()))
            or [(item.arg,ast.literal_eval(item.value)) for item in psg_call.keywords] != [('replace_psg_mapping',True)]):
        raise Boundary('exact195 PSG construction changed')

    def compose(node):
        node.args[1] = ast.parse('_live_edges(video_events,write_events,_live_extension)',mode='eval').body
        node.keywords[0].value = ast.Constant(value=False)
    replace_record(psg_call, compose)
    refresh = _one([node for node in ast.walk(view) if type(node) is ast.FunctionDef and node.name=='refresh'],
        'initial shared finite refresh-reader function')
    replace_record(refresh, lambda node: setattr(node,'body',ast.parse(
        'return _live_read_refresh(control,provider_input,provider_counts,previous)').body))
    startup_call = _one(calls('AudioDriverStartupSession'), 'actual startup Session construction')
    if [item.arg for item in startup_call.keywords] != ['irq_clock_hz','initial_irq_clock']:
        raise Boundary('exact195 startup keyword contract changed')
    replace_record(startup_call,lambda node: node.keywords.extend([
        ast.keyword(arg='main_loop_points',value=ast.Constant(value=True)),
        ast.keyword(arg='timer_b_continuation',value=ast.Constant(value=True))]))
    owner_try = _one([node for node in view.body if type(node) is ast.Try], 'full construction/execution try')
    bind = _one([node for node in owner_try.body
        if _dump(node)==_dump(ast.parse('video.bind_scene(state)').body[0])], 'initial Scene VDP bind')
    dma_statement = ast.parse('_live_bind_data_dma(vdp,state)').body[0]
    owner_try.body.insert(owner_try.body.index(bind),dma_statement)
    yielding = ast.parse('yield _live_capture(locals(),_live_extension,_live_contract,_live_profile)').body[0]
    last = owner_try.body[-1]
    if not (type(last) is ast.Expr and type(last.value) is ast.Call
            and _dump(last.value.func)==_dump(ast.parse('receipt.update',mode='eval').body)
            and any(item.arg=='status' and type(item.value) is ast.Constant
                and item.value.value=='passed_new_sameScene_cold38_actual_reset_install_handoff_driver_three_IM1_006F'
                for item in last.value.keywords)):
        raise Boundary('exact195 last success checkpoint before original finally changed')
    owner_try.body.append(yielding)
    removed = {_dump(dma_statement),_dump(yielding)}
    seen = dict.fromkeys(undo,0)
    removed_seen = dict.fromkeys(removed,0)

    class Inverse(ast.NodeTransformer):
        def visit(self,node):
            key = _dump(node)
            if key in undo:
                seen[key] += 1
                return copy.deepcopy(undo[key])
            if key in removed:
                removed_seen[key] += 1
                return None
            return super().visit(node)

    inverse = Inverse().visit(copy.deepcopy(view))
    if (any(value!=1 for value in seen.values()) or any(value!=1 for value in removed_seen.values())
            or _dump(inverse) != _dump(function)):
        raise Boundary('live view inverse must restore every complete original195 function AST node')
    derived_module = copy.deepcopy(module_source)
    module_index = derived_module.body.index(_one([node for node in derived_module.body
        if type(node) is ast.FunctionDef and node.name=='run'], 'derived module run owner'))
    derived_module.body[module_index] = copy.deepcopy(view)
    restored_module = copy.deepcopy(derived_module)
    restored_module.body[module_index] = copy.deepcopy(inverse)
    if _dump(restored_module) != _dump(module_source):
        raise Boundary('full module inverse must retain every other current module AST node')
    contract = dict(confidence='confirmed_complete_public195_FN_inverse_AST_identity',
        original_module=original.__module__, original_function=original.__name__,
        original_top_level_statements=len(function.body), whole_FN_inverse=True, whole_module_inverse=True,
        module_import_symbol_context_preserved=True, module_body_or_imports_executed_by_compile=False,
        replaced_exact_nodes=4, inserted_statements=2, unchanged_original_finally_and_return=True,
        precise_deltas=['bare default ranges minus unowned PSG aperture from creation',
            'exact finite edge delegator below outermost PSG first mapping; replacement=False',
            'same initial finite R-reader computes real IFF2 flags; no later provider replacement',
            'startup main_loop_points=True and timer_b_continuation=True',
            'same SceneDataDmaSource before initial video.bind_scene',
            'one final success yield before original finally; no game prefix replay'],
        existing_business_compiler_or_device_guards_changed=False)
    namespace = dict(vars(original195))
    namespace.update(_live_base_bus=_base_bus,_live_edges=_edges,_live_read_refresh=_read_refresh,
        _live_bind_data_dma=_bind_data_dma,_live_capture=_capture,_live_extension=profile['live_extension'],
        _live_contract=contract,_live_profile=profile)
    compiled_view = compile(ast.fix_missing_locations(derived_module), original.__code__.co_filename, 'exec')
    view_code = _one([value for value in compiled_view.co_consts
        if type(value) is CodeType and value.co_name=='run'], 'derived module-context run code')
    if original.__code__.co_freevars or original.__closure__ is not None or view_code.co_freevars:
        raise Boundary('top-level run must not acquire an implicit closure')
    program = FunctionType(view_code,namespace,original.__name__,original.__defaults__,original.__closure__)
    program.__kwdefaults__ = None if original.__kwdefaults__ is None else dict(original.__kwdefaults__)
    if not inspect.isgeneratorfunction(program):
        raise Boundary('derived whole-module run lacks its sole actual live yield')
    return program


def build_live_cold_driver(project_root, sound_native_root, sources, audio_root, chip_library, inputs, output):
    """Run ONLY a new combined caller scope; return live real first3BC/006F.

    Never call this to replay195 by itself. All paths remain explicit. The
    caller must finish the returned rig after its new finite title/timer scope.
    """
    profile = json.loads(Path(inputs).read_text(encoding='utf-8'))
    extension = profile['live_extension']
    if (extension.get('format')!='g5510-live-cold-driver-extension-v1'
            or extension.get('main_loop_points') is not True
            or extension.get('timer_b_continuation') is not True
            or extension.get('reserved_PSG_window') != [0xC00010,0xC00018]):
        raise ValueError('explicit fresh live extension with exact opt-ins/reserved PSG window required')
    program = _derived_factory(profile)(project_root,sound_native_root,sources,audio_root,chip_library,inputs,output)
    try:
        rig = next(program)
    except StopIteration as error:
        raise Boundary('derived195 did not retain its actual live success checkpoint') from error
    if type(rig) is not LiveColdDriverRig:
        raise Boundary('derived195 yielded a foreign live ownership record')
    rig._parent_program = program
    return rig.require_live()
