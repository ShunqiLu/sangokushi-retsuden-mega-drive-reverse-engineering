"""Compose recovered scene services over one caller-owned live state.

This is an intermediate execution integration, not a console emulator or a
finished independent game. Business algorithms remain in their own modules.
The composition never reads source/ROM/media files, copies RAM, interprets PC
values, replaces missing inputs, or silently completes a hardware boundary.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

from .domain import HardwareBus, ReadOnlyData, SceneState
from .services import LogicalServices, ServiceBinding


_scene_log = ContextVar('new_scene_event_log', default=None)


@contextmanager
def use_new_scene_event_log(events):
    """Give a new cold Scene an initially empty log before it starts running."""
    if len(events) or _scene_log.get() is not None:
        raise ValueError('An empty event log and a new cold Scene are required')
    selection = [events]
    token = _scene_log.set(selection)
    try:
        yield
        if selection:
            raise RuntimeError('The cold Scene did not attach its event log')
    finally:
        _scene_log.reset(token)


def combine_service_bindings(*groups: tuple[ServiceBinding, ...]) -> LogicalServices:
    """Compose explicit ABI authorities and reject duplicate exact signatures.

    Several callers of one original function may have different validated input
    contracts. Replacing an existing adapter is not an implicit override: the
    caller must supply an unambiguous set of (target, exact input type) pairs.
    """
    if any(type(group) is not tuple for group in groups):
        raise ValueError('explicit tuples of service ABI bindings required')
    bindings = tuple(binding for group in groups for binding in group)
    return LogicalServices(bindings)


def recovered_scene_services() -> LogicalServices:
    """Link recovered scene algorithms over exact caller contracts, without I/O.

    Imports are local because these families already reuse each other's domain
    and business functions. Their binding providers declare ordinary callable
    adapters; an unlinked target or unsupported input contract still stops.
    """
    from .linkage_campaign_tick import campaign_tick_bindings
    from .linkage_map import map_menu_bindings
    from ..high_level_dynamic_flows.linkage_duel import duel_bindings
    from ..high_level_remaining_flows.linkage_city import city_service_bindings
    from ..high_level_scene_flows.linkage_duel_panels import duel_panel_bindings
    from .linkage_commands import command_label_bindings
    from .linkage_roster_names import roster_name_bindings
    from ..high_level_scene_flows.linkage_duel_transfers import sprite_packet_bindings
    from .linkage_world_tick import world_tick_bindings
    from .linkage_render import render_bindings
    from .linkage_input_reset import input_marker_bindings
    from ..high_level_scene_flows.linkage_duel_round import duel_packet_bindings
    from ..high_level_dynamic_flows.linkage_scene_phase import scene_phase_bindings
    from ..high_level_dynamic_flows.linkage_scene_objects import scene_object_bindings

    return combine_service_bindings(
        map_menu_bindings(), duel_bindings(), city_service_bindings(),
        duel_panel_bindings(),
        command_label_bindings(), roster_name_bindings(),
        sprite_packet_bindings(),
        world_tick_bindings(), render_bindings(), input_marker_bindings(),
        duel_packet_bindings(),
        scene_phase_bindings(), scene_object_bindings(),
        campaign_tick_bindings(),
    )


def create_linked_scene_state(
    ram: bytearray,
    *,
    data: ReadOnlyData,
    hardware: HardwareBus,
    services: LogicalServices,
    max_reads: int,
    max_samples: int,
    sr: int,
) -> SceneState:
    """Attach explicit resources, hardware and services to the same live RAM.

    Initial status and diagnostic budgets are required, not guessed cartridge
    values. Default hardware methods may remain explicit boundaries. The caller
    retains the original bytearray; all linked Tables/Cursors use this exact
    SceneState. No second state, RAM snapshot or register/PC dictionary exists.
    """
    if type(services) is not LogicalServices:
        raise ValueError('explicit linked logical services required')
    state = SceneState(
        ram, data=data, hardware=hardware, services=services,
        max_reads=max_reads, max_samples=max_samples, sr=sr,
    )
    selection = _scene_log.get()
    if selection is not None:
        if not selection or state.events:
            raise RuntimeError('One event log belongs to exactly one new Scene')
        state.events = selection.pop()
    return state


def create_scene_state_from_sources(
    ram: bytearray,
    *,
    source_root: Path,
    resource_ids: tuple[str, ...],
    hardware: HardwareBus,
    services: LogicalServices,
    max_reads: int,
    max_samples: int,
    sr: int,
) -> SceneState:
    """Connect owned resource files and real supplied devices to one live RAM.

    Resource encoding belongs to the loading layer, not the gameplay modules.
    This factory never chooses a reference ROM, copies the caller's RAM, creates
    SRAM, or fills missing device/service implementations with successful ACKs.
    """
    from .runtime_resources import load_scene_resources
    resources = load_scene_resources(source_root, resource_ids)
    return create_linked_scene_state(
        ram, data=resources.data, hardware=hardware, services=services,
        max_reads=max_reads, max_samples=max_samples, sr=sr,
    )
