"""Already recovered display rules on the main family's same live state.

These adapt established semantic algorithms, not incompatible old State
objects. Their physical code is previous coverage, never candidate17 credit.
Glyphs and decimal catalogs stay external read-only data; only original tile
IDs, geometry limits and fixed-width compatibility occur in these functions.
"""
from .domain import (
    SceneState, Cursor, Long, Word, checked_state, checked_cursor, uint,
    u8, u16, u32, low16, s16, replace_word, divu_retained,
)
from .contexts_display_reuse import MapSpriteResult, DecimalPlaceResult


from .contexts_display_reuse import MapSpriteTransaction, MapSpriteFields

from .contexts_display_reuse import SpritePacketMemory, append_live_command_sprite_packet_fields, FirstDeploymentFrame, first_replace

def append_map_sprites(state: SceneState, source: Cursor,
        x: Long, y: Long, attributes: Long, *, reset_scroll: bool,
        initialize_clip: bool) -> MapSpriteResult:
    """Legacy projection of the one actual sprite transaction authority."""
    result=append_map_sprite_transaction(state,source,x,y,attributes,
        reset_scroll=reset_scroll,initialize_clip=initialize_clip)
    return MapSpriteResult(result.source,result.x,result.y,result.attributes)


def append_decimal_value_place(state: SceneState, value: Long,
        divisor: Word, digit_tile: Word, blank_tile: Word,
        started: Word, destination: Cursor) -> DecimalPlaceResult:
    """Existing12760 packed-DIVU digit step, preserving overflow/zero boundary."""
    checked_state(state)
    checked_cursor(destination, state)
    uint(value, 32)
    for item in (divisor, digit_tile, blank_tile, started):
        uint(item, 16)
    from ..high_level_player_commands.business_budget import _decimal_value_place_fields
    from ..high_level_player_commands.contexts_numeric import DecimalMemory
    result = _decimal_value_place_fields(DecimalMemory(state), value, divisor,
        digit_tile, blank_tile, started, destination)
    return DecimalPlaceResult(result.remainder, result.started)


def append_six_place_decimal_value(state: SceneState, value: Long,
        digit_tile: Word, blank_tile: Word, destination: Cursor) -> Cursor:
    """Existing1270A six-cell decimal packet; no host-formatting substitution."""
    return append_six_place_decimal_fields(state, value, digit_tile,
        blank_tile, destination).destination


def append_six_place_decimal_fields(state: SceneState, value: Long,
        digit_tile: Word, blank_tile: Word, destination: Cursor):
    """True1270A numeric fields and ordered cells, on the original SceneState.

    Field WORDs do not invent incoming D3/D4/D5 high halves. The strict city
    caller owns those live inputs and combines them at its real return ABI.
    """
    from ..high_level_player_commands.business_budget import _six_place_decimal_fields
    from ..high_level_player_commands.contexts_numeric import DecimalMemory
    checked_state(state)
    return _six_place_decimal_fields(DecimalMemory(state), value,
        digit_tile, blank_tile, destination).validate(state)




def append_map_sprite_transaction(state: SceneState, source: Cursor,
        x: Long, y: Long, attributes: Long, *, reset_scroll: bool,
        initialize_clip: bool) -> MapSpriteTransaction:
    """Legacy actual high halves projected over the unique WORD algorithm."""
    checked_state(state)
    checked_cursor(source, state)
    uint(x, 32)
    uint(y, 32)
    uint(attributes, 32)
    fields = append_map_sprite_fields(state, source, low16(x), low16(y),
        low16(attributes), reset_scroll=reset_scroll, initialize_clip=initialize_clip)
    return MapSpriteTransaction(fields.source, replace_word(x, fields.x),
        replace_word(y, fields.y), replace_word(attributes, fields.attributes),
        fields.carry, fields.zero, fields.negative, fields.overflow).validate(state)


def append_map_sprite_fields(state: SceneState, source: Cursor,
        x: Word, y: Word, attributes: Word, *, reset_scroll: bool,
        initialize_clip: bool) -> MapSpriteFields:
    """WORD-only main API projects the sole complete player sprite algorithm."""
    checked_state(state)
    checked_cursor(source,state)
    frame = first_replace(FirstDeploymentFrame.unobserved(),roster=source)
    result = append_live_command_sprite_packet_fields(SpritePacketMemory(state),frame,
        x,y,attributes,reset_scroll=reset_scroll,initialize_clip=initialize_clip)
    # Preserve this historical facade's mutable input-cursor observation.
    source.base = result.frame.roster.base
    return MapSpriteFields(source,result.x,result.y,result.attributes,
        result.carry,result.zero,result.negative,result.overflow).validate(state)
