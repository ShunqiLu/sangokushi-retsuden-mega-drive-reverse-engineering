"""Same-state packet and palette bridges for a complete current duel frame.

26BFA/3AB94 already have unique algorithms. These adapters project their true
returns, not entry snapshots. A3/A6, X/full SR and return-token DATA remain
outside the selected frame ABI; no additional RAM observation supplies them.
"""
from dataclasses import replace
from .contexts_duel import DuelTurnFrame, DuelConditionObservation, checked_duel_turn
from .contexts_reuse import SpritePacketContext
from .domain import low16


def stage_duel_turn_packet(state, frame):
    """26BFA: current D5/A2 and function-entry SP, with complete packet return."""
    from .business_reuse import stage_sprite_word_packet
    checked_duel_turn(frame, state)
    source = frame.actor.cursor()
    context = SpritePacketContext(frame.command, frame.comparison, frame.distance,
        frame.factor, frame.weapon_difference, frame.working_value, frame.response,
        frame.variation, source, frame.opponent.cursor(), frame.lookup, frame.stack,
        frame.conditions.carry, frame.conditions.zero, frame.conditions.negative,
        frame.conditions.overflow).validate(state)
    actual = stage_sprite_word_packet(state, source, frame.command,
        low16(frame.comparison), low16(frame.distance), context)
    if type(actual) is not SpritePacketContext:
        raise ValueError('complete true packet return required')
    actual.validate(state)
    return DuelTurnFrame(actual.command, actual.rows, actual.row_command,
        actual.remaining, actual.token, actual.run_count, actual.response,
        actual.rows_remaining, actual.source, actual.destination, actual.glyph_source,
        actual.stack, DuelConditionObservation(actual.carry, actual.zero,
            actual.negative, actual.overflow)).validate(state)


def copy_duel_turn_palette(state, frame):
    """3AB94: A0 preserved; A1 directory, A2 source; A3 not renamed to A1."""
    from .business_scene import copy_scene_palette_variant_complete
    checked_duel_turn(frame, state)
    actual = copy_scene_palette_variant_complete(state, frame.command, frame.variation)
    actual.validate(state)
    return replace(frame, command=actual.index_carrier, variation=actual.count_carrier,
        opponent=actual.directory, lookup=actual.source,
        conditions=DuelConditionObservation(actual.carry, actual.zero,
            actual.negative, actual.overflow)).validate(state)


def duel_packet_bindings():
    """Only the two real full-frame targets; label remains its original owner."""
    from ..high_level_main_flows.services import ServiceBinding
    return (ServiceBinding(0x26BFA, DuelTurnFrame, DuelTurnFrame, stage_duel_turn_packet),
            ServiceBinding(0x3AB94, DuelTurnFrame, DuelTurnFrame, copy_duel_turn_palette))
