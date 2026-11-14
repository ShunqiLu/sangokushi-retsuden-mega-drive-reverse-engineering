"""Transfer selected group resources and compact the live deployment records.

The resource split keeps the original low-WORD shift and residual rounding,
not a clean percentage formula. Every scan/copy operates on shared live RAM;
in particular compaction can alias unread input and is never snapshot-copied.
This is a semantic source draft, not complete CPU or natural-input acceptance.
"""
from .domain import (
    GameState, Table, Word, Long, checked_state, checked_table, uint,
    u8, u16, u32, low16, high16, replace_word, negative_word, swap_words,
    descending_inclusive, read_packed_long, store_packed_long_reverse,
)
from .contexts_logistics import ResourceShare, DeploymentResult
from .business_reuse import (
    submit_deployment_queue, count_selected_deployment,
    initialize_selected_assignment, selected_troop_weights,
    refresh_object_attribute_average, signed_divmod,
)


from .contexts_personnel import CommandFrame, PersonnelMemory, _personnel_existing_fields, _personnel_legacy_entry
from .domain import Boundary

def deploy_selected_group(state: GameState, entry_frame: CommandFrame | None=None) -> DeploymentResult:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 111174)
    actual = deploy_selected_group_frame_fields(memory, entered)
    return DeploymentResult(state.table(actual.addresses[0]), actual.data[7] & 65535)


def transfer_selected_group_resources(state: GameState, group: Table, selected_count: Word, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 111292)
    checked_table(group, state)
    if group.base != entered.addresses[0]:
        raise ValueError('group must be the actual incoming A0 view')
    uint(selected_count, 16)
    if selected_count != entered.data[7] & 65535:
        raise ValueError('selected count must match actual incoming D7 WORD')
    actual = transfer_selected_group_resources_frame_fields(memory, entered)
    return None


def split_group_resource_share(state: GameState, amount: Long, selected_weight: Long, total_weight: Long, entry_frame: CommandFrame | None=None) -> ResourceShare:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 111688)
    uint(amount, 32)
    uint(selected_weight, 32)
    uint(total_weight, 32)
    if (amount, selected_weight, total_weight) != (entered.data[2], entered.data[5], entered.data[6]):
        raise ValueError('resource share must match actual D2/D5/D6 LONGs')
    actual = split_group_resource_share_frame_fields(memory, entered)
    return ResourceShare(actual.data[1], actual.data[3])


def remove_deployed_group_members(state: GameState, group: Table, selected_count: Word, entry_frame: CommandFrame | None=None) -> Table:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 111730)
    checked_table(group, state)
    if group.base != entered.addresses[0]:
        raise ValueError('group must be the actual incoming A0 view')
    uint(selected_count, 16)
    if selected_count != entered.data[7] & 65535:
        raise ValueError('selected count must match actual incoming D7 WORD')
    actual = remove_deployed_group_members_frame_fields(memory, entered)
    return state.table(actual.addresses[0])

from .contexts_logistics import project_deployment_command_fields

def deploy_selected_group_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x1b246)


def transfer_selected_group_resources_frame_fields(memory: PersonnelMemory, frame: CommandFrame, resource_cap: Long=999999) -> CommandFrame:
    """Fixed original cap invariant; only the existing sole City core mutates resources."""
    uint(resource_cap,32)
    if resource_cap != 999999:
        raise ValueError('only the original fixed City resource-cap default is admitted')
    return _personnel_existing_fields(memory,frame,0x1b2bc)


def split_group_resource_share_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x1b448)


def remove_deployed_group_members_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x1b472)
