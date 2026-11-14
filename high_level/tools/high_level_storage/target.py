"""Storage physical bindings; no encoded code or image payload."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    end: int
    completion: str = 'return'

SAVE_BINDINGS = (
    Binding('write_saved_game_state',0x83fa,0x8866),
    Binding('stage_saved_officer_positions',0x8866,0x8888),
    Binding('stage_saved_city_orders',0x8888,0x88c6),
    Binding('stage_scaled_officer_parameter_words',0x892a,0x8946),
    Binding('stage_saved_force_record_columns',0x8a3e,0x8a60),
)

LOAD_BINDINGS = (
    Binding('restore_saved_game_state',0x8a60,0x8eea),
    Binding('restore_saved_officer_positions',0x8eea,0x8f0c),
    Binding('restore_city_orders_and_action_flags',0x8f0c,0x8fb4),
    Binding('restore_scaled_officer_parameter_words',0x901c,0x9036),
    Binding('normalize_saved_force_head_sentinels',0x9148,0x9166),
    Binding('normalize_saved_city_head_sentinels',0x9166,0x9184),
    Binding('normalize_saved_city_owner_sentinels',0x9184,0x91a2),
    Binding('restore_saved_force_record_columns',0x91a2,0x91c4),
    Binding('refresh_loaded_group_attributes',0x91f8,0x922a),
)

STREAMS_BINDINGS = (
    Binding('write_packed_transport_orders',0x88c6,0x892a),
    Binding('write_packed_group_stream',0x8946,0x89e0),
    Binding('append_little_endian_bitfield',0x89e0,0x89fe),
    Binding('write_saved_state_checksum',0x89fe,0x8a22),
    Binding('checksum_saved_payload',0x8a22,0x8a3e),
    Binding('read_packed_transport_orders',0x8fb4,0x8ffe),
    Binding('read_buffered_low_word_bitfield',0x8ffe,0x901c),
    Binding('read_packed_group_stream',0x9036,0x90d8),
    Binding('validate_saved_header_and_checksum',0x90d8,0x9148),
    Binding('read_buffered_long_bitfield',0x91c4,0x91f8),
    Binding('write_masked_fixed_count_fields',0x922a,0x929a),
    Binding('read_masked_fixed_count_fields',0x931e,0x9390),
)

NEW_BINDINGS = tuple(sorted(SAVE_BINDINGS+LOAD_BINDINGS+STREAMS_BINDINGS,key=lambda b:b.entry))
REUSED_BINDINGS = ()
BINDINGS = NEW_BINDINGS
BY_NAME = {b.name:b for b in BINDINGS}
BY_ENTRY = {b.entry:b for b in BINDINGS}

def validate_binding(binding):
    if type(binding) is not Binding or BY_NAME.get(binding.name)!=binding:
        raise ValueError('declared complete target Binding required')
    if (type(binding.entry) is not int or type(binding.end) is not int or
        not 0<=binding.entry<binding.end<=0x100000 or binding.entry&1 or binding.end&1
        or binding.completion!='return'):
        raise ValueError('whole returning original extent required')
    return binding

if (len(NEW_BINDINGS),sum(b.end-b.entry for b in NEW_BINDINGS))!=(26,3858):
    raise ValueError('26 complete new bodies required')
if len(BY_NAME)!=26 or len(BY_ENTRY)!=26 or any(a.end>b.entry for a,b in zip(BINDINGS,BINDINGS[1:])):
    raise ValueError('nonoverlapping unique physical/semantic authorities required')

