"""Original scope and ABI allocations. No encoded instruction payload."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    end: int
    completion: str = 'return'


NUMERIC_BINDINGS = (
    Binding('settle_battle', 0x1B968, 0x1B99C), Binding('loss_ratio', 0x1B99C, 0x1B9D6),
    Binding('defender_scaled_loss', 0x1B9D6, 0x1BA50), Binding('attacker_heavy_loss', 0x1BB82, 0x1BC24),
    Binding('settle_awards', 0x1BC24, 0x1BC66), Binding('defender_heavy_loss', 0x1BED4, 0x1BF68),
    Binding('attacker_light_loss', 0x1BF68, 0x1BFE0),
)
MEMBER_BINDINGS = (
    Binding('remove_member', 0x1BA50, 0x1BB1C, 'context_remove'),
    Binding('finish_removal', 0x1BB1C, 0x1BB82, 'abandon_two_calls'),
    Binding('transfer_attacker', 0x1BC66, 0x1BCD4), Binding('transfer_defender', 0x1BCD4, 0x1BD42),
    Binding('transfer_members', 0x1BD42, 0x1BE62), Binding('sync_queues', 0x1BE62, 0x1BED4),
)
BINDINGS = tuple(sorted(NUMERIC_BINDINGS + MEMBER_BINDINGS, key=lambda b: b.entry))
HELPERS = {'random_sample': 0x83D4, 'signed_divmod': 0x35760}
MEMBER_REGISTERS = {
    'remove_member': {'officer': 'd0', 'award': 'd1', 'count': 'd2', 'owner': 'd3', 'member_index': 'd3',
                      'capacity': 'a0', 'owners': 'a0', 'leaders': 'a0', 'officer_flags': 'a0',
                      'assignments': 'a1', 'object_view': 'a2', 'copy_source': 'a3'},
    'finish_removal': {'officer': 'd0', 'award': 'd1', 'queue': 'a0'},
    'transfer_attacker': {'selector': 'd0', 'doubled_officer': 'd1', 'remaining': 'd2',
                          'assignments': 'a0', 'owners': 'a0', 'leaders': 'a0', 'destination': 'a0',
                          'source': 'a1', 'offsets': 'a2', 'troops': 'a2'},
    'transfer_defender': {'selector': 'd0', 'doubled_officer': 'd1', 'remaining': 'd2',
                          'assignments': 'a0', 'owners': 'a0', 'leaders': 'a0', 'destination': 'a0',
                          'source': 'a1', 'offsets': 'a2', 'troops': 'a2'},
    'transfer_members': {'count': 'd0', 'officer': 'd1', 'doubled_officer': 'd1', 'average_index': 'd1',
                         'carry': 'd2', 'remaining_count': 'd2', 'attribute': 'd2', 'record_size': 'd3',
                         'search_index': 'd3', 'total': 'd3', 'saved_byte': 'd4', 'deleted': 'd7',
                         'destination': 'a0', 'source': 'a1', 'insertion': 'a2', 'copy_source': 'a2',
                         'attributes': 'a2', 'copy_target': 'a3'},
    'sync_queues': {'officer': 'd0', 'deleted': 'd7', 'queue': 'a0'},
}
VIEW_BASES = {'capacity_parameters': 0xC000, 'assignments': 0xCC00, 'city_owners': 0xF427,
              'force_leaders': 0xE640, 'officer_flags': 0xC700, 'troops': 0xB200,
              'average_attributes': 0xC400, 'packed_offsets': 0xEFBE, 'packed_entities': 0x9000,
              'capacity_fields': 0xC800, 'ratio_attributes': 0xB400}
SCALARS = {'attacker_officer': (0xF3A6, 16), 'defender_officer': (0xF3F2, 16), 'object_index': (0xEFC6, 16),
           'opposing_object': (0x00FF382C, 32), 'first_marker': (0xF744, 16), 'second_marker': (0xF746, 16),
           'first_marker_tail': (0xF745, 8), 'second_marker_tail': (0xF747, 8),
           'pair_queue_offset': (0x00FF3BB2, 16), 'first_loss_award': (0xEFB8, 16), 'second_loss_award': (0xEFBA, 16)}
TABLE_BINDINGS = {name: dict(address=address, suffix='w') for name, address in VIEW_BASES.items()}
TABLE_BINDINGS.update(pair_queue=dict(address=0x00FF39B2, suffix='l'), active_queue=dict(address=0x00FF3000, suffix='l'))
SCALAR_BINDINGS = {name: dict(address=address, width=width, suffix='l' if address > 65535 else 'w')
                   for name, (address, width) in SCALARS.items()}
SCALAR_BINDINGS['second_marker_header'] = dict(address=0xF746, width=8, suffix='w')
NUMERIC_REGISTERS = {
    'settle_battle': {'quotient': 'd1', 'remainder': 'd2', 'ratio': 'd2'},
    'loss_ratio': {'parameters': 'a0', 'attributes': 'a1', 'selected': 'd0', 'offset': 'd0',
                   'first': 'd1', 'first_product': 'd1', 'numerator': 'd1', 'denominator_attribute': 'd2',
                   'index_product': 'd0', 'denominator': 'd2'},
    'settle_awards': {'awards': 'a0', 'selected': 'd0', 'offset': 'd0', 'previous': 'd1', 'updated': 'd1'},
}
for name in ('defender_scaled_loss', 'attacker_heavy_loss', 'defender_heavy_loss', 'attacker_light_loss'):
    defender = name.startswith('defender')
    NUMERIC_REGISTERS[name] = {
        'sample': 'd0', 'rate': 'd0', 'product': 'd0', 'loss': 'd0', 'award': 'd0', 'officer': 'd0', 'object_index': 'd0',
        'parameters': 'a0', 'troops': 'a0', 'parameter_selector': 'd1', 'parameter_offset': 'd1',
        'capacity': 'd3', 'remaining_capacity': 'd3', 'troop_selector': 'd3' if defender else 'd1',
        'troop_offset': 'd3' if defender else 'd1', 'previous_troops': 'd1' if defender else 'd3',
        'remaining_troops': 'd1' if defender else 'd3', 'owner_hint': 'd3', 'count_hint': 'd2', 'ratio': 'd2',
        'object_view': 'a2', 'offsets': 'a3', 'outcome': 'd1',
    }


def validate_binding(value):
    if (type(value) is not Binding or type(value.name) is not str or type(value.entry) is not int or
            type(value.end) is not int or type(value.completion) is not str or value not in BINDINGS):
        raise ValueError('strict explicit battle settlement binding required')
