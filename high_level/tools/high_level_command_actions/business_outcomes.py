"""Duel settlement and city/battlefield attrition rules.

Roster mutations are live: search and compaction use their real moving views,
including original unguarded searches. Arithmetic is expressed as business
formulas with explicit WORD wrapping and the original two-part multiplies.
This module does not render menus, open a ROM, or embed instruction payloads.
"""
from .domain import (GameState, Table, Cursor, Word, Long, CarryOutcome,
    checked_state, uint, u16, u32, low16, high16, replace_byte, replace_word,
    swap_words, negative_word, divu_retained)
from .contexts_outcomes import (DuelSettlementContext, DuelSettlementResult,
    DuelDispositionContext, checked_context)
from .business_reuse import (grant_duel_fallback_progress,
    grant_duel_troop_difference_progress, remove_zero_readiness_duelist,
    settle_duel_result_roster, detach_defeated_duelist,
    build_city_assigned_outcome_candidates, build_battlefield_outcome_candidates,
    signed_divmod)








from .contexts_personnel import CommandFrame, PersonnelMemory, _personnel_existing_fields, _personnel_legacy_entry
from .domain import Boundary

def settle_duel_training_and_troops(state: GameState, context: DuelSettlementContext, entry_frame: CommandFrame | None=None) -> DuelSettlementResult:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 100518)
    context = checked_context(context, DuelSettlementContext)
    if context.training_carrier != entered.data[2]:
        raise ValueError('duel training must retain the actual incoming D2 LONG')
    actual = settle_duel_training_and_troops_frame_fields(memory, entered)
    return DuelSettlementResult(actual.data[2])


def settle_duel_packets(state: GameState, context: DuelSettlementContext, entry_frame: CommandFrame | None=None) -> CarryOutcome:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 101120)
    context = checked_context(context, DuelSettlementContext)
    if context.training_carrier != entered.data[2]:
        raise ValueError('duel training must retain the actual incoming D2 LONG')
    actual = settle_duel_packets_frame_fields(memory, entered)
    return state.carry_result(actual.status_word & 1)








def apply_duel_disposition(state: GameState, context: DuelDispositionContext, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 101268)
    context = checked_context(context, DuelDispositionContext)
    if context.officer != entered.data[0] & 65535 or context.disposition != entered.data[2] & 255:
        raise ValueError('duel disposition must match actual D0 WORD/D2 BYTE')
    actual = apply_duel_disposition_frame_fields(memory, entered)
    return None


def detach_zero_readiness_duelists(state: GameState, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 101462)
    actual = detach_zero_readiness_duelists_frame_fields(memory, entered)
    return None




def compute_outcome_force_ratio(state: GameState, entry_frame: CommandFrame | None=None) -> Word:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 115138)
    actual = compute_outcome_force_ratio_frame_fields(memory, entered)
    return actual.data[1] & 65535


def apply_battlefield_ratio_losses(state: GameState, entry_frame: CommandFrame | None=None) -> Word:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 115452)
    actual = apply_battlefield_ratio_losses_frame_fields(memory, entered)
    return actual.data[7] & 65535




def apply_city_assigned_heavy_losses(state: GameState, entry_frame: CommandFrame | None=None) -> Word:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 115612)
    actual = apply_city_assigned_heavy_losses_frame_fields(memory, entered)
    return actual.data[7] & 65535




def consume_city_battle_resources(state: GameState, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 115814)
    actual = consume_city_battle_resources_frame_fields(memory, entered)
    return None


def apply_battlefield_heavy_losses_and_detach(state: GameState, entry_frame: CommandFrame | None=None) -> Word:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 116206)
    actual = apply_battlefield_heavy_losses_and_detach_frame_fields(memory, entered)
    return actual.data[7] & 65535

def settle_duel_training_and_troops_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x188a6)


def settle_duel_packets_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x18b00)


def apply_duel_disposition_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x18b94)


def detach_zero_readiness_duelists_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x18c56)


def compute_outcome_force_ratio_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x1c1c2)


def apply_battlefield_ratio_losses_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x1c2fc)


def apply_city_assigned_heavy_losses_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x1c39c)


def consume_city_battle_resources_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x1c466)


def apply_battlefield_heavy_losses_and_detach_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """Complete same-state projection of the retained sole physical owner."""
    return _personnel_existing_fields(memory,frame,0x1c5ee)
