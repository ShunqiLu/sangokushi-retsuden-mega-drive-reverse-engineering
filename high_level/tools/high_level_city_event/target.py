"""Explicit original compatibility ABI and allocation; never code payloads."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Binding:
    name: str
    rule: str
    entry: int
    end: int
    field: str | None = None


BINDINGS = (
    Binding('reset_queue', 'reset_queue', 0x17016, 0x17026),
    Binding('append_queue', 'append_queue', 0x17026, 0x17058),
    Binding('submit_three_fields', 'submit_three_fields', 0x171A6, 0x171FC),
    Binding('submit_four_fields', 'submit_four_fields', 0x17342, 0x173A6),
    Binding('submit_classified_fields', 'submit_classified_fields', 0x17474, 0x174F0),
    *(Binding('scale_' + field, 'scale_field', 0x17514 + i * 22, 0x1752A + i * 22, field)
      for i, field in enumerate(('e1e0', 'e140', 'e320', 'e000', 'e0a0', 'e5a0'))),
    Binding('sample_once', 'sample_once', 0x17598, 0x175A8),
    Binding('sample_small', 'sample_small', 0x175A8, 0x175C2),
    Binding('sample_wide', 'sample_wide', 0x175C2, 0x175DC),
    Binding('wrapped_product', 'wrapped_product', 0x175DC, 0x175EC),
    Binding('divide_percent', 'divide_percent', 0x175EC, 0x17602),
    Binding('random_sample', 'random_sample', 0x83D4, 0x83FA),
    Binding('signed_divmod', 'signed_divmod', 0x35760, 0x3576C),
    Binding('positive_denominator', 'positive_denominator', 0x3576C, 0x3577A),
    Binding('unsigned_divmod', 'unsigned_divmod', 0x3577A, 0x357DA),
    Binding('word_pair_divmod', 'word_pair_divmod', 0x357DA, 0x357F8),
)
FIELD_BASES = {'e1e0': 0xE1E0, 'e140': 0xE140, 'e320': 0xE320,
               'e000': 0xE000, 'e0a0': 0xE0A0, 'e5a0': 0xE5A0}
PARAMETERS = {'mask': 0x174F0, 'factor': 0x174FC}
REGISTERS = {
    'reset_queue': {'queue': 'a0', 'slot': 'd0'},
    'append_queue': {'city': 'd7', 'incoming_owner': 'd0', 'owner': 'd0', 'queue': 'a0'},
    'submit_three_fields': {'city': 'd0', 'incoming_owner': 'd7', 'owner': 'd7', 'saved_city': 'd7', 'sample': 'd0', 'offset': 'd7', 'factor': 'd0'},
    'submit_four_fields': {'city': 'd0', 'incoming_owner': 'd7', 'owner': 'd7', 'saved_city': 'd7', 'sample': 'd0', 'offset': 'd7', 'factor': 'd0'},
    'submit_classified_fields': {'city': 'd0', 'saved_city': 'd7', 'offset': 'd0', 'field': 'a0', 'mask': 'd3', 'classified': 'd2', 'sample': 'd0', 'base_factor': 'd3', 'factor': 'd0'},
    'scale_field': {'offset': 'd7', 'factor': 'd0', 'field': 'a0', 'previous': 'd2', 'product': 'd2', 'result': 'd2'},
    'random_sample': {'seed': 'd1', 'original': 'd0', 'mixed': 'd1', 'sample': 'd0'},
    'sample_once': {}, 'sample_small': {'sample': 'd0'}, 'sample_wide': {'sample': 'd0'},
    'wrapped_product': {'value': 'd2', 'factor': 'd0'},
    'divide_percent': {'product': 'd2', 'quotient': 'd1', 'remainder': 'd2'},
    'signed_divmod': {'numerator': 'd1', 'denominator': 'd2', 'quotient': 'd1', 'remainder': 'd2'},
    'positive_denominator': {'numerator': 'd1', 'denominator': 'd2', 'quotient': 'd1', 'remainder': 'd2'},
    'unsigned_divmod': {'numerator': 'd1', 'denominator': 'd2', 'divisor_high': 'd3', 'saved_numerator': 'd4', 'saved_denominator': 'd5', 'quotient': 'd1', 'remainder': 'd2', 'denominator_part': 'd2', 'product': 'd2', 'high_product': 'd3'},
    'word_pair_divmod': {'numerator': 'd1', 'denominator': 'd2', 'high_division': 'd1', 'high_quotient': 'd3', 'low_division': 'd1', 'quotient': 'd1', 'remainder': 'd2'},
}
PRESERVED = {'sample_once': ('d1',), 'sample_small': ('d1',), 'sample_wide': ('d1',),
             'divide_percent': ('d1',)}
LOCAL_PRESERVED = {'unsigned_divmod': ('d3', 'd4', 'd5')}
CALL_STYLE = {'random_sample': 'absolute', 'signed_divmod': 'absolute',
              'sample_once': 'pc_jsr_nop', 'sample_small': 'pc_jsr_nop', 'sample_wide': 'pc_jsr_nop',
              'positive_denominator': 'short_bsr', 'unsigned_divmod': 'short_bsr', 'word_pair_divmod': 'short_bsr'}
RETURN_REGISTER = {'reset_queue': None, 'append_queue': 'd0', 'scale_field': 'd2',
                   'wrapped_product': 'd2', 'divide_percent': 'd2', 'random_sample': 'd0',
                   'sample_once': 'd0', 'sample_small': 'd0', 'sample_wide': 'd0',
                   'signed_divmod': ('d1', 'd2'), 'positive_denominator': ('d1', 'd2'),
                   'unsigned_divmod': ('d1', 'd2'), 'word_pair_divmod': ('d1', 'd2')}


def validate_binding(binding):
    if type(binding) is not Binding or any(type(getattr(binding, field)) is not int for field in ('entry', 'end')):
        raise ValueError('strict typed target binding required')
    if type(binding.name) is not str or type(binding.rule) is not str or (binding.field is not None and type(binding.field) is not str):
        raise ValueError('strict binding names required')
    if binding not in BINDINGS:
        raise ValueError('only explicit original compatibility allocations supported')
