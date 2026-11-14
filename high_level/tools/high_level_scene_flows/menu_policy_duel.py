"""Finite, source-driven policy grammar for complete duel decision families.

The business source remains the algorithm authority.  A role is identified by a
function and an exact AST path, never by a literal's value.  Only those leaves
are variable: the surrounding reads, calls, arithmetic widths, returns and
effects still pass the complete semantic-functions matcher.  This is not a
general Python compiler, and an admitted edit does not prove a natural menu
input or an eventual hardware acknowledgement.
"""
from __future__ import annotations

from .compiler_common import CompileError
from .policy_common import SourceRole as MenuRole, admit_policy_source, _RELATIONS
from .target import DUEL_BINDINGS


# Paths address the function after its optional first docstring is removed.
# They identify a semantic use, not every occurrence of the same integer.
ROLE_SPECS = (
    MenuRole('timer_step', '_finish_duel_loadout_menu', (
        ('body', 1, 'value', 'args', 1, 'args', 0, 'right'),
        ('body', 2, 'value', 'func', 'value', 'args', 2),
    ), 'quick', 1, (0x27DF4, 0x27ECA)),
    MenuRole('cursor_direction_mask', '_highlight_duel_loadout_choice', (
        ('body', 0, 'value', 'keywords', 0, 'value', 'args', 1, 'right'),
    ), 'direction_mask', 12, (0x27DC6, 0x27E9C)),
    MenuRole('cursor_blink_mask', '_highlight_duel_loadout_choice', (
        ('body', 1, 'body', 1, 'value', 'keywords', 0, 'value', 'args', 1, 'right'),
    ), 'nonzero_word', 8, (0x27DD4, 0x27EAA)),
    MenuRole('cursor_stride', '_highlight_duel_loadout_choice', (
        ('body', 3, 'value', 'args', 0, 'right'),
    ), 'word', 56, (0x27DE0, 0x27EB6)),
    MenuRole('cursor_coordinate', '_highlight_duel_loadout_choice', (
        ('body', 4, 'value', 'keywords', 0, 'value', 'args', 1),
    ), 'word', 200, (0x27DDA, 0x27EB0)),
    MenuRole('cursor_pattern', '_highlight_duel_loadout_choice', (
        ('body', 4, 'value', 'keywords', 2, 'value', 'args', 1),
    ), 'word', 67, (0x27DE8, 0x27EBE)),
    MenuRole('cursor_attributes', '_highlight_duel_loadout_choice', (
        ('body', 4, 'value', 'keywords', 3, 'value', 'args', 1),
    ), 'word', 32768, (0x27DEC, 0x27EC2)),
    MenuRole('two_option_direction_mask', 'choose_duel_two_option_menu_complete', (
        ('body', 1, 'value', 'keywords', 1, 'value', 'args', 1, 'right'),
    ), 'direction_mask', 12, (0x27D9E,)),
    MenuRole('two_option_direction_step', 'choose_duel_two_option_menu_complete', (
        ('body', 2, 'body', 0, 'value', 'keywords', 0, 'value', 'args', 1),
        ('body', 2, 'body', 1, 'body', 0, 'value', 'keywords', 0, 'value', 'args', 1),
    ), 'signed_word_pair', 1, (0x27DA4, 0x27DAE)),
    MenuRole('two_option_positive_mask', 'choose_duel_two_option_menu_complete', (
        ('body', 2, 'body', 0, 'value', 'keywords', 1, 'value', 'args', 1, 'right'),
    ), 'direction_bit', 8, (0x27DA8,)),
    MenuRole('two_option_bound', 'choose_duel_two_option_menu_complete', (
        ('body', 2, 'body', 4, 'test', 'comparators', 0),
    ), 'nonzero_word', 2, (0x27DB2,)),
    MenuRole('two_option_accept_relation', 'choose_duel_two_option_menu_complete', (
        ('body', 2, 'body', 4, 'test', 'ops', 0),
    ), 'unsigned_relation', '<', (0x27DB6,)),
    MenuRole('two_option_confirm_mask', 'choose_duel_two_option_menu_complete', (
        ('body', 4, 'test', 'operand', 'right'),
    ), 'long_bit', 32, (0x27DBE,)),
    MenuRole('two_option_cursor_bias', 'choose_duel_two_option_menu_complete', (
        ('body', 4, 'body', 0, 'value', 'args', 2),
    ), 'word', 121, (0x27DE4,)),
    MenuRole('equipment_repair_step', '_choose_duel_equipment_complete', (
        ('body', 2, 'body', 3, 'value', 'args', 1, 'args', 0, 'right'),
    ), 'quick', 1, (0x27E18,)),
    MenuRole('equipment_direction_mask', '_choose_duel_equipment_complete', (
        ('body', 3, 'value', 'keywords', 1, 'value', 'args', 1, 'right'),
    ), 'direction_mask', 12, (0x27E3E,)),
    MenuRole('equipment_direction_step', '_choose_duel_equipment_complete', (
        ('body', 4, 'body', 0, 'value', 'keywords', 0, 'value', 'args', 1),
        ('body', 4, 'body', 1, 'body', 0, 'value', 'keywords', 0, 'value', 'args', 1),
    ), 'signed_word_pair', 1, (0x27E44, 0x27E4E)),
    MenuRole('equipment_positive_mask', '_choose_duel_equipment_complete', (
        ('body', 4, 'body', 0, 'value', 'keywords', 1, 'value', 'args', 1, 'right'),
    ), 'direction_bit', 8, (0x27E48,)),
    MenuRole('equipment_confirm_mask', '_choose_duel_equipment_complete', (
        ('body', 6, 'test', 'operand', 'right'),
    ), 'long_bit', 32, (0x27E94,)),
    MenuRole('equipment_cursor_bias', '_choose_duel_equipment_complete', (
        ('body', 6, 'body', 0, 'value', 'args', 2),
    ), 'word', 104, (0x27EBA,)),
)

_SOURCE_FUNCTIONS = frozenset(role.function for role in ROLE_SPECS)
_SHARED_ROLES = frozenset(role.name for role in ROLE_SPECS
                          if role.function in ('_finish_duel_loadout_menu',
                                               '_highlight_duel_loadout_choice'))


def _owner_rules(values, prefix):
    rules = {name: values[name] for name in _SHARED_ROLES}
    for short in ('direction_mask', 'direction_step', 'positive_mask',
                  'confirm_mask', 'cursor_bias'):
        rules[short] = values[prefix + '_' + short]
    rules['confirm_bit'] = rules['confirm_mask'].bit_length() - 1
    if prefix == 'two_option':
        rules['accept_bound'] = values['two_option_bound']
        rules['accept_relation'] = values['two_option_accept_relation']
        rules['accept_branch'] = next(branch for relation, branch in _RELATIONS.values()
                                      if relation == rules['accept_relation'])
    else:
        rules['repair_step'] = values['equipment_repair_step']
    return rules


def _menu_constraints(values):
    for prefix in ('two_option', 'equipment'):
        if values[prefix + '_positive_mask'] & values[prefix + '_direction_mask'] == 0:
            raise CompileError(prefix + ': positive direction bit must belong to the selection mask')


def _menu_owner_rules(values):
    return {
        'choose_duel_two_option_menu': _owner_rules(values, 'two_option'),
        'choose_first_duel_equipment': _owner_rules(values, 'equipment'),
    }


def admit_menu_source(source, declarations, approved, *, extra_roles=(),
                      extra_rule_builders=()):
    """Duel adapter over the shared complete-body source-policy grammar."""
    return admit_policy_source(
        source, declarations, approved,
        role_specs=ROLE_SPECS + tuple(extra_roles),
        rule_builders=(_menu_owner_rules,) + tuple(extra_rule_builders),
        bindings=DUEL_BINDINGS,
        grammar=('duel-policy-path-roles-v2' if extra_roles
                 else 'duel-menu-path-roles-v1'),
        constraints=(_menu_constraints,),
    )


# Complete actual Duel fields role topology125; fixed real current business paths, no source fallback.
_ORIGINAL_NATIVE_ROLE_SPECS125 = ROLE_SPECS
_CURRENT_DUEL_ROLE_BINDINGS125 = {'timer_step': {'function': '_duel_menu_adjust_memory_word_fields', 'paths': (('body', 3, 'value', 'args', 3),), 'coupled_uses': (), 'physical_pcs': (163316, 163530, 163352, 163716, 163846)}, 'cursor_direction_mask': {'function': '_duel_menu_loadout_highlight_fields', 'paths': (('body', 1, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'cursor_blink_mask': {'function': '_duel_menu_loadout_highlight_fields', 'paths': (('body', 2, 'body', 1, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'cursor_stride': {'function': '_duel_menu_loadout_highlight_fields', 'paths': (('body', 5, 'value', 'args', 3),), 'coupled_uses': ()}, 'cursor_coordinate': {'function': '_duel_menu_loadout_highlight_fields', 'paths': (('body', 3, 'value', 'args', 3),), 'coupled_uses': ()}, 'cursor_pattern': {'function': '_duel_menu_loadout_highlight_fields', 'paths': (('body', 7, 'value', 'args', 3),), 'coupled_uses': ()}, 'cursor_attributes': {'function': '_duel_menu_loadout_highlight_fields', 'paths': (('body', 8, 'value', 'args', 3),), 'coupled_uses': ()}, 'two_option_direction_mask': {'function': 'choose_duel_two_option_menu_fields', 'paths': (('body', 2, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'two_option_direction_step': {'function': 'choose_duel_two_option_menu_fields', 'paths': (('body', 3, 'body', 0, 'value', 'args', 3),), 'coupled_uses': (), 'kind': 'nonzero_word'}, 'two_option_positive_mask': {'function': 'choose_duel_two_option_menu_fields', 'paths': (('body', 3, 'body', 1, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'two_option_confirm_mask': {'function': 'choose_duel_two_option_menu_fields', 'paths': (('body', 5, 'value', 'args', 2),), 'coupled_uses': (), 'kind': 'long_bit_index'}, 'two_option_cursor_bias': {'function': 'choose_duel_two_option_menu_fields', 'paths': (('body', 6, 'body', 0, 'value', 'args', 2),), 'coupled_uses': ()}, 'equipment_direction_mask': {'function': 'choose_duel_equipment_fields', 'paths': (('body', 5, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'equipment_direction_step': {'function': 'choose_duel_equipment_fields', 'paths': (('body', 6, 'body', 0, 'value', 'args', 3),), 'coupled_uses': (), 'kind': 'nonzero_word'}, 'equipment_positive_mask': {'function': 'choose_duel_equipment_fields', 'paths': (('body', 6, 'body', 1, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'equipment_confirm_mask': {'function': 'choose_duel_equipment_fields', 'paths': (('body', 8, 'value', 'args', 2),), 'coupled_uses': (), 'kind': 'long_bit_index'}, 'equipment_cursor_bias': {'function': 'choose_duel_equipment_fields', 'paths': (('body', 9, 'body', 0, 'value', 'args', 2),), 'coupled_uses': ()}, 'two_option_bound': {'function': 'choose_duel_two_option_menu_fields', 'paths': (('body', 3, 'body', 4, 'value', 'args', 3),), 'coupled_uses': ()}, 'two_option_accept_relation': {'function': 'choose_duel_two_option_menu_fields', 'paths': (('body', 3, 'body', 5, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}}
_CURRENT_SHARED_ROLE_ALIASES125 = {'equipment_repair_step': 'timer_step'}
ROLE_SPECS = tuple(MenuRole(role.name, _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('function', role.function), _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('paths', role.paths), _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('kind', role.kind), role.default, _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('physical_pcs', role.physical_pcs), coupled_uses=_CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('coupled_uses', role.coupled_uses)) for role in ROLE_SPECS if role.name not in _CURRENT_SHARED_ROLE_ALIASES125)

_pre_fields_menu_owner_rules125 = _menu_owner_rules
def _menu_owner_rules(values):
    values = dict(values)
    for _alias, _authority in _CURRENT_SHARED_ROLE_ALIASES125.items():
        if _authority not in values:
            raise CompileError('actual shared menu source authority required')
        values[_alias] = values[_authority]
    return _pre_fields_menu_owner_rules125(values)
