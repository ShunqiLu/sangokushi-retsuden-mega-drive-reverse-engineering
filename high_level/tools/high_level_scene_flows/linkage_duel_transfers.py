"""Six true packet handlers sharing the current scene state and live stack.

The source routines in remaining_flows are the sole formatter/repeat authority.
This is a typed caller adapter, not a decoder or a copy of their algorithms.
The native WORD table may leave these six targets: that stays an unbound call.
"""
from .contexts_reuse import SpritePacketContext
from .domain import low16


SPRITE_PACKET_TARGETS = (
    (0x26C58, 'highbank_process_counted_records_11', 'HighbankProcessCountedRecords11Input'),
    (0x26C72, 'highbank_process_counted_records_12', 'HighbankProcessCountedRecords12Input'),
    (0x26C8E, 'highbank_process_counted_records_13', 'HighbankProcessCountedRecords13Input'),
    (0x26CD6, 'highbank_process_counted_records_14', 'HighbankProcessCountedRecords14Input'),
    (0x26D1C, 'highbank_update_live_fields_8', 'HighbankUpdateLiveFields8Input'),
    (0x26D30, 'highbank_update_live_fields_9', 'HighbankUpdateLiveFields9Input'),
)


def _sprite_handler(target, name, kind_name):
    def invoke(state, context):
        from ..high_level_remaining_flows import business_highbank, contexts_highbank
        if type(context) is not SpritePacketContext:
            raise ValueError('exact current packet context required')
        context.validate(state)
        # 26C2E MOVE.W of the actual fetched relative target is the last
        # flag-writing operation before 26C32 JSR. It is not the earlier LSR.
        relative_target = low16(context.token)
        flags = (False, relative_target == 0, bool(relative_target & 32768), False)
        kind = getattr(contexts_highbank, kind_name)
        if target in (0x26D1C, 0x26D30):
            actual = kind(context.source, context.destination, context.remaining,
                          context.run_count, *flags)
        elif target in (0x26C8E, 0x26CD6):
            actual = kind(context.source, context.destination, context.command,
                context.rows, context.row_command, context.remaining, context.token,
                context.run_count, context.response, context.stack, *flags)
        else:
            actual = kind(context.source, context.destination, context.command,
                context.remaining, context.token, context.run_count, context.response, *flags)
        result = getattr(business_highbank, name)(state, actual)
        result.validate(state)
        command = context.command if target in (0x26D1C, 0x26D30) else result.value
        rows = result.field if target in (0x26C8E, 0x26CD6) else context.rows
        row_command = result.tile if target in (0x26C8E, 0x26CD6) else context.row_command
        token = context.token if target in (0x26D1C, 0x26D30) else result.offset
        response = context.response if target in (0x26D1C, 0x26D30) else result.member
        glyph_source = result.descriptor if target in (0x26C8E, 0x26CD6, 0x26D1C, 0x26D30) else context.glyph_source
        return SpritePacketContext(command, rows, row_command, result.row, token,
            result.limit, response, context.rows_remaining, result.destination.cursor(),
            result.source.cursor(), glyph_source, context.stack,
            result.carry, result.zero, result.negative, result.overflow).validate(state)
    return invoke


def sprite_packet_bindings():
    """Six exact same-state current-packet→current-packet ServiceBinding."""
    from ..high_level_main_flows.services import ServiceBinding
    return tuple(ServiceBinding(target, SpritePacketContext, SpritePacketContext,
        _sprite_handler(target, name, kind)) for target, name, kind in SPRITE_PACKET_TARGETS)
