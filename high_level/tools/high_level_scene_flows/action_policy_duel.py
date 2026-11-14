"""Source-policy lowering of the complete 316-byte duel action menu.

Only explicit roles vary inside the complete supplied action/highlight bodies.
The composing admission layer consumes every surrounding AST effect; this
module supplies path-specific role metadata, strict owner constraints and the
ordinary native instruction selection.  It never reads old source, assembly,
ROM, objects, or private evidence at generation time.
"""
from __future__ import annotations

from .compiler_common import CompileError
from .menu_policy_duel import MenuRole


ROLE_SPECS = (
    MenuRole('action_restricted_relation', 'choose_duel_action_menu_complete', (
        ('body', 5, 'value', 'ops', 0),
    ), 'unsigned_relation', '==', (0x27EE6, 0x27EF8)),
    MenuRole('action_direction_mask', 'choose_duel_action_menu_complete', (
        ('body', 6, 'orelse', 1, 'value', 'keywords', 1, 'value', 'args', 1, 'right'),
    ), 'nonzero_word', 15, (0x27F02,)),
    # Both ordinary and restricted paths really test the same supplied bit.
    MenuRole('action_vertical_forward_mask', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 1, 'test', 'right'),
        ('body', 6, 'orelse', 2, 'body', 1, 'test', 'operand', 'right'),
    ), 'long_bit', 8, (0x27F0C, 0x27F94)),
    MenuRole('action_vertical_backward_mask', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 2, 'test', 'right'),
        ('body', 6, 'orelse', 2, 'body', 1, 'body', 1, 'test', 'operand', 'right'),
    ), 'long_bit', 4, (0x27F14, 0x27FAC)),
    MenuRole('action_horizontal_forward_mask', 'choose_duel_action_menu_complete', (
        ('body', 6, 'orelse', 2, 'body', 1, 'body', 1, 'body', 0, 'value', 'test', 'right'),
    ), 'long_bit', 2, (0x27F1E,)),
    MenuRole('action_vertical_step', 'choose_duel_action_menu_complete', (
        ('body', 6, 'orelse', 2, 'body', 0, 'value'),
        ('body', 6, 'orelse', 2, 'body', 1, 'body', 0, 'value'),
    ), 'signed_word_pair', 1, (0x27F08,)),
    MenuRole('action_horizontal_step', 'choose_duel_action_menu_complete', (
        ('body', 6, 'orelse', 2, 'body', 1, 'body', 1, 'body', 0, 'value', 'body'),
        ('body', 6, 'orelse', 2, 'body', 1, 'body', 1, 'body', 0, 'value', 'orelse'),
    ), 'signed_word_pair', 2, (0x27F1A,)),
    MenuRole('action_unrestricted_bound', 'choose_duel_action_menu_complete', (
        ('body', 6, 'orelse', 2, 'body', 5, 'test', 'comparators', 0),
    ), 'byte', 4, (0x27F28,)),
    MenuRole('action_unrestricted_relation', 'choose_duel_action_menu_complete', (
        ('body', 6, 'orelse', 2, 'body', 5, 'test', 'ops', 0),
    ), 'unsigned_relation', '<', (0x27F2C,)),
    MenuRole('action_restricted_forward_step', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 1, 'body', 0, 'value', 'args', 0, 'right'),
    ), 'quick', 1, (0x27F9A,)),
    MenuRole('action_restricted_forward_skip_value', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 1, 'body', 1, 'test', 'comparators', 0),
    ), 'word', 2, (0x27F9C,)),
    MenuRole('action_restricted_forward_skip_relation', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 1, 'body', 1, 'test', 'ops', 0),
    ), 'unsigned_relation', '==', (0x27FA0,)),
    MenuRole('action_restricted_forward_skip_step', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 1, 'body', 1, 'body', 0, 'value', 'args', 0, 'right'),
    ), 'quick', 1, (0x27FA2,)),
    MenuRole('action_restricted_forward_bound', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 1, 'body', 3, 'test', 'comparators', 0),
    ), 'nonzero_word', 4, (0x27FA4,)),
    MenuRole('action_restricted_forward_relation', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 1, 'body', 3, 'test', 'ops', 0),
    ), 'unsigned_relation', '>=', (0x27FA8,)),
    MenuRole('action_restricted_forward_wrap', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 1, 'body', 3, 'body', 0, 'value', 'keywords', 0, 'value'),
    ), 'byte', 0, (0x27FAA,)),
    MenuRole('action_restricted_backward_skip_value', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 2, 'body', 1, 'test', 'comparators', 0),
    ), 'word', 3, (0x27FB2,)),
    MenuRole('action_restricted_backward_skip_relation', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 2, 'body', 1, 'test', 'ops', 0),
    ), 'unsigned_relation', '==', (0x27FB6,)),
    MenuRole('action_restricted_backward_skip_step', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 2, 'body', 1, 'body', 0, 'value', 'args', 0, 'right'),
    ), 'quick', 1, (0x27FB8,)),
    MenuRole('action_restricted_backward_step', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 2, 'body', 2, 'value', 'args', 0, 'right'),
    ), 'quick', 1, (0x27FBA,)),
    MenuRole('action_restricted_backward_wrap', 'choose_duel_action_menu_complete', (
        ('body', 6, 'body', 2, 'body', 4, 'body', 0, 'value', 'keywords', 0, 'value'),
    ), 'byte', 3, (0x27FBE,)),
    MenuRole('action_confirm_mask', 'choose_duel_action_menu_complete', (
        ('body', 8, 'test', 'operand', 'right'),
    ), 'long_bit', 32, (0x27F38, 0x27FCA)),
    MenuRole('action_timer_step', 'choose_duel_action_menu_complete', (
        ('body', 10, 'value', 'args', 1, 'args', 0, 'right'),
        ('body', 11, 'value', 'func', 'value', 'args', 2),
    ), 'quick', 1, (0x27F84, 0x28006)),
    MenuRole('action_cursor_direction_mask', '_duel_menu_highlight', (
        ('body', 0, 'value', 'keywords', 0, 'value', 'args', 1, 'right'),
    ), 'nonzero_word', 15, (0x27F40, 0x27FD2)),
    MenuRole('action_cursor_blink_mask', '_duel_menu_highlight', (
        ('body', 1, 'body', 1, 'value', 'keywords', 0, 'value', 'args', 1, 'right'),
    ), 'nonzero_word', 8, (0x27F4E, 0x27FE0)),
    MenuRole('action_cursor_x_mask', '_duel_menu_highlight', (
        ('body', 2, 'orelse', 0, 'value', 'left', 'right'),
    ), 'word', 2, (0x27F5A,)),
    MenuRole('action_cursor_x_stride', '_duel_menu_highlight', (
        ('body', 2, 'orelse', 0, 'value', 'right'),
    ), 'word', 12, (0x27F5E,)),
    MenuRole('action_cursor_x_bias', '_duel_menu_highlight', (
        ('body', 2, 'orelse', 1, 'value', 'keywords', 0, 'value', 'args', 1, 'args', 0, 'right'),
    ), 'word', 176, (0x27F62,)),
    MenuRole('action_cursor_y_mask', '_duel_menu_highlight', (
        ('body', 2, 'orelse', 2, 'value', 'left', 'right'),
    ), 'word', 1, (0x27F6C,)),
    MenuRole('action_cursor_y_stride', '_duel_menu_highlight', (
        ('body', 2, 'orelse', 2, 'value', 'right'),
    ), 'word', 48, (0x27F70,)),
    MenuRole('action_cursor_y_bias', '_duel_menu_highlight', (
        ('body', 2, 'orelse', 3, 'value', 'keywords', 0, 'value', 'args', 1, 'args', 0, 'right'),
    ), 'word', 136, (0x27F74,)),
    MenuRole('action_restricted_cursor_index_mask', '_duel_menu_highlight', (
        ('body', 2, 'body', 0, 'value', 'right'),
    ), 'word', 3, (0x27FEC,)),
    MenuRole('action_restricted_cursor_x', '_duel_menu_highlight', (
        ('body', 2, 'body', 1, 'value', 'keywords', 1, 'value', 'args', 1),
    ), 'word', 200, (0x27FF0,)),
    MenuRole('action_cursor_pattern', '_duel_menu_highlight', (
        ('body', 3, 'value', 'keywords', 0, 'value', 'args', 1),
    ), 'word', 67, (0x27F78, 0x27FFA)),
    MenuRole('action_cursor_attributes', '_duel_menu_highlight', (
        ('body', 3, 'value', 'keywords', 1, 'value', 'args', 1),
    ), 'word', 32768, (0x27F7C, 0x27FFE)),
)

_FALSE_BRANCH = {'<': 'bcc', '<=': 'bhi', '>': 'bls', '>=': 'bcs',
                 '==': 'bne', '!=': 'beq'}
_TRUE_BRANCH = {'<': 'bcs', '<=': 'bls', '>': 'bhi', '>=': 'bcc',
                '==': 'beq', '!=': 'bne'}


def owner_rules(values):
    """Turn extracted actual source roles into the one physical owner's rules.

    The common path grammar validates literals/relations and couples repeated
    nodes.  Constraints specific to the native BYTE, MOVEQ and four-byte table
    stay here; nothing truncates an unsupported input into an admitted value.
    """
    rules = {}
    for role in ROLE_SPECS:
        if role.name not in values:
            raise CompileError('complete action-menu source roles required')
        value = values[role.name]
        if role.kind == 'unsigned_relation':
            if type(value) is not str or value not in _FALSE_BRANCH:
                raise CompileError(role.name + ': supported unsigned relation required')
        else:
            if type(value) is not int:
                raise CompileError(role.name + ': strict integer role required')
            maximum = 255 if role.kind == 'byte' else 65535
            minimum = 0
            if role.kind == 'quick':
                minimum, maximum = 1, 8
            elif role.kind in ('nonzero_word', 'signed_word_pair'):
                minimum = 1
            elif role.kind == 'long_bit':
                minimum, maximum = 1, 0x80000000
            if not minimum <= value <= maximum:
                raise CompileError(role.name + ': native width/range exceeded')
            if role.kind == 'long_bit' and value & (value - 1):
                raise CompileError(role.name + ': exactly one LONG bit required')
        rules[role.name.removeprefix('action_')] = value
    if rules['unrestricted_bound'] == 0:
        raise CompileError('action unrestricted bound must be a nonzero BYTE')
    for name in ('restricted_forward_wrap', 'restricted_backward_wrap'):
        if rules[name] > 127:
            raise CompileError(name + ': nonnegative signed MOVEQ immediate 0..127 required')
    if rules['restricted_cursor_index_mask'] > 3:
        raise CompileError('restricted cursor mask must stay in the existing four-byte table')
    for name in ('vertical_forward_mask', 'vertical_backward_mask',
                 'horizontal_forward_mask', 'confirm_mask'):
        rules[name.removesuffix('_mask') + '_bit'] = rules[name].bit_length() - 1
    rules['restricted_branch'] = _TRUE_BRANCH[rules['restricted_relation']]
    for prefix in ('unrestricted', 'restricted_forward_skip',
                   'restricted_forward', 'restricted_backward_skip'):
        rules[prefix + '_branch'] = _FALSE_BRANCH[rules[prefix + '_relation']]
    return {'choose_duel_action_menu': rules}


def lower_action_menu(emitter, rules):
    """Complete native selection; every variable operand comes from source.

    Fixed operations are the admitted body's width/allocation/call structure.
    In particular ADD.B retains the side byte, each MOVEQ clears the full LONG,
    MULU creates full products, and each ADDI.W retains their high WORD.  Both
    paths query first controls, consume the actual sprite return, then reach
    their timer; the special-selector path is not normalized to the ordinary
    four-direction policy.
    """
    emitter.segment(0x27ED2, 0x2800E)
    emitter.ins('tst.w', '0xff7018:l', 6)
    emitter.ins('bmi.b', 'scene_pc_027eec', 2)
    emitter.ins('move.w', '0xff706a:l,%d1', 6)
    emitter.ins('cmp.w', '0xff7070:l,%d1', 6)
    emitter.ins(rules['restricted_branch'] + '.w', 'scene_pc_027f8c', 4)
    emitter.ins('bra.b', 'scene_pc_027efc', 2)
    emitter.ins('move.w', '0xff70ba:l,%d1', 6)
    emitter.ins('cmp.w', '0xff70c0:l,%d1', 6)
    emitter.ins(rules['restricted_branch'] + '.w', 'scene_pc_027f8c', 4)
    emitter.ins('move.w', '0xff7018:l,%d1', 6)
    emitter.ins('andi.w', f'#0x{rules["direction_mask"]:x},%d0', 4)
    emitter.ins('beq.b', 'scene_pc_027f34', 2)
    emitter.ins('move.w', f'#0x{rules["vertical_step"]:x},%d2', 4)
    emitter.ins('btst.l', f'#0x{rules["vertical_forward_bit"]:x},%d0', 4)
    emitter.ins('bne.b', 'scene_pc_027f26', 2)
    emitter.ins('neg.w', '%d2', 2)
    emitter.ins('btst.l', f'#0x{rules["vertical_backward_bit"]:x},%d0', 4)
    emitter.ins('bne.b', 'scene_pc_027f26', 2)
    emitter.ins('move.w', f'#0x{rules["horizontal_step"]:x},%d2', 4)
    emitter.ins('btst.l', f'#0x{rules["horizontal_forward_bit"]:x},%d0', 4)
    emitter.ins('bne.b', 'scene_pc_027f26', 2)
    emitter.ins('neg.w', '%d2', 2)
    emitter.ins('add.b', '%d2,%d1', 2)
    emitter.ins('cmpi.b', f'#0x{rules["unrestricted_bound"]:x},%d1', 4)
    emitter.ins(rules['unrestricted_branch'] + '.b', 'scene_pc_027f34', 2)
    emitter.ins('move.w', '%d1,0xff7018:l', 6)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('btst.l', f'#0x{rules["confirm_bit"]:x},%d0', 4)
    emitter.ins('bne.w', 'scene_pc_027f84', 4)
    emitter.ins('andi.w', f'#0x{rules["cursor_direction_mask"]:x},%d0', 4)
    emitter.ins('bne.w', 'scene_pc_027f54', 4)
    emitter.ins('move.w', '0xff7008:l,%d0', 6)
    emitter.ins('andi.w', f'#0x{rules["cursor_blink_mask"]:x},%d0', 4)
    emitter.ins('beq.b', 'scene_pc_027f84', 2)
    emitter.ins('move.w', '0xff7018:l,%d0', 6)
    emitter.ins('andi.w', f'#0x{rules["cursor_x_mask"]:x},%d0', 4)
    emitter.ins('mulu.w', f'#0x{rules["cursor_x_stride"]:x},%d0', 4)
    emitter.ins('addi.w', f'#0x{rules["cursor_x_bias"]:x},%d0', 4)
    emitter.ins('move.w', '0xff7018:l,%d1', 6)
    emitter.ins('andi.w', f'#0x{rules["cursor_y_mask"]:x},%d1', 4)
    emitter.ins('mulu.w', f'#0x{rules["cursor_y_stride"]:x},%d1', 4)
    emitter.ins('addi.w', f'#0x{rules["cursor_y_bias"]:x},%d1', 4)
    emitter.ins('move.w', f'#0x{rules["cursor_pattern"]:x},%d2', 4)
    emitter.ins('move.w', f'#0x{rules["cursor_attributes"]:x},%d3', 4)
    emitter.ins('bsr.w', 'scene_pc_028f9c', 4)
    emitter.ins('subq.w', f'#0x{rules["timer_step"]:x},0xff70fa:l', 6)
    emitter.ins('rts', '', 2)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('move.b', '0xff7019:l,%d1', 6)
    emitter.ins('btst.l', f'#0x{rules["vertical_forward_bit"]:x},%d0', 4)
    emitter.ins('beq.b', 'scene_pc_027fac', 2)
    emitter.ins('addq.w', f'#0x{rules["restricted_forward_step"]:x},%d1', 2)
    emitter.ins('cmpi.w', f'#0x{rules["restricted_forward_skip_value"]:x},%d1', 4)
    emitter.ins(rules['restricted_forward_skip_branch'] + '.b', 'scene_pc_027fa4', 2)
    emitter.ins('addq.w', f'#0x{rules["restricted_forward_skip_step"]:x},%d1', 2)
    emitter.ins('cmpi.w', f'#0x{rules["restricted_forward_bound"]:x},%d1', 4)
    emitter.ins(rules['restricted_forward_branch'] + '.b', 'scene_pc_027fac', 2)
    emitter.ins('moveq', f'#{rules["restricted_forward_wrap"]},%d1', 2)
    emitter.ins('btst.l', f'#0x{rules["vertical_backward_bit"]:x},%d0', 4)
    emitter.ins('beq.b', 'scene_pc_027fc0', 2)
    emitter.ins('cmpi.w', f'#0x{rules["restricted_backward_skip_value"]:x},%d1', 4)
    emitter.ins(rules['restricted_backward_skip_branch'] + '.b', 'scene_pc_027fba', 2)
    emitter.ins('subq.w', f'#0x{rules["restricted_backward_skip_step"]:x},%d1', 2)
    emitter.ins('subq.w', f'#0x{rules["restricted_backward_step"]:x},%d1', 2)
    emitter.ins('bpl.b', 'scene_pc_027fc0', 2)
    emitter.ins('moveq', f'#{rules["restricted_backward_wrap"]},%d1', 2)
    emitter.ins('move.b', '%d1,0xff7019:l', 6)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('btst.l', f'#0x{rules["confirm_bit"]:x},%d0', 4)
    emitter.ins('bne.w', 'scene_pc_028006', 4)
    emitter.ins('andi.w', f'#0x{rules["cursor_direction_mask"]:x},%d0', 4)
    emitter.ins('bne.w', 'scene_pc_027fe6', 4)
    emitter.ins('move.w', '0xff7008:l,%d0', 6)
    emitter.ins('andi.w', f'#0x{rules["cursor_blink_mask"]:x},%d0', 4)
    emitter.ins('beq.b', 'scene_pc_028006', 2)
    emitter.ins('move.w', '0xff7018:l,%d2', 6)
    emitter.ins('andi.w', f'#0x{rules["restricted_cursor_index_mask"]:x},%d2', 4)
    emitter.ins('move.w', f'#0x{rules["restricted_cursor_x"]:x},%d0', 4)
    emitter.ins('moveq', '#0,%d1', 2)
    emitter.ins('move.b', '22(%pc, %d2.w),%d1', 4)
    emitter.ins('move.w', f'#0x{rules["cursor_pattern"]:x},%d2', 4)
    emitter.ins('move.w', f'#0x{rules["cursor_attributes"]:x},%d3', 4)
    emitter.ins('bsr.w', 'scene_pc_028f9c', 4)
    emitter.ins('subq.w', f'#0x{rules["timer_step"]:x},0xff70fa:l', 6)
    emitter.ins('rts', '', 2)


LOWERERS = {'choose_duel_action_menu': lower_action_menu}


# Complete actual Duel fields role topology125; fixed real current business paths, no source fallback.
_ORIGINAL_NATIVE_ROLE_SPECS125 = ROLE_SPECS
_CURRENT_DUEL_ROLE_BINDINGS125 = {'action_restricted_relation': {'function': 'choose_duel_action_menu_fields', 'paths': (('body', 6, 'value', 'args', 0),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'action_direction_mask': {'function': 'choose_duel_action_menu_fields', 'paths': (('body', 7, 'orelse', 1, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'action_vertical_forward_mask': {'function': '_duel_action_direction_fields', 'paths': (('body', 1, 'value', 'args', 2),), 'coupled_uses': (('_duel_action_restricted_choice_fields', ('body', 2, 'value', 'args', 2)),), 'kind': 'long_bit_index'}, 'action_vertical_backward_mask': {'function': '_duel_action_direction_fields', 'paths': (('body', 2, 'body', 1, 'value', 'args', 2),), 'coupled_uses': (('_duel_action_restricted_choice_fields', ('body', 4, 'value', 'args', 2)),), 'kind': 'long_bit_index'}, 'action_horizontal_forward_mask': {'function': '_duel_action_direction_fields', 'paths': (('body', 2, 'body', 2, 'body', 1, 'value', 'args', 2),), 'coupled_uses': (), 'kind': 'long_bit_index'}, 'action_vertical_step': {'function': '_duel_action_direction_fields', 'paths': (('body', 0, 'value', 'args', 3),), 'coupled_uses': (), 'kind': 'nonzero_word'}, 'action_horizontal_step': {'function': '_duel_action_direction_fields', 'paths': (('body', 2, 'body', 2, 'body', 0, 'value', 'args', 3),), 'coupled_uses': (), 'kind': 'nonzero_word'}, 'action_unrestricted_bound': {'function': 'choose_duel_action_menu_fields', 'paths': (('body', 7, 'orelse', 2, 'body', 2, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_unrestricted_relation': {'function': 'choose_duel_action_menu_fields', 'paths': (('body', 7, 'orelse', 2, 'body', 3, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'action_restricted_forward_step': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 3, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_restricted_forward_skip_value': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 3, 'body', 1, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_restricted_forward_skip_step': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 3, 'body', 2, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_restricted_forward_bound': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 3, 'body', 3, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_restricted_forward_wrap': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 3, 'body', 4, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_restricted_backward_skip_value': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 5, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_restricted_backward_skip_step': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 5, 'body', 1, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_restricted_backward_step': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 5, 'body', 2, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_restricted_backward_wrap': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 5, 'body', 3, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_restricted_forward_skip_relation': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 3, 'body', 2, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'action_restricted_forward_relation': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 3, 'body', 4, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'action_restricted_backward_skip_relation': {'function': '_duel_action_restricted_choice_fields', 'paths': (('body', 5, 'body', 1, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'action_confirm_mask': {'function': 'choose_duel_action_menu_fields', 'paths': (('body', 9, 'value', 'args', 2),), 'coupled_uses': (), 'kind': 'long_bit_index'}, 'action_cursor_direction_mask': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 1, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'action_cursor_blink_mask': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 2, 'body', 1, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'action_restricted_cursor_index_mask': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 3, 'body', 1, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'action_restricted_cursor_x': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 3, 'body', 2, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_cursor_x_mask': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 3, 'orelse', 1, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'action_cursor_x_stride': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 3, 'orelse', 2, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_cursor_x_bias': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 3, 'orelse', 3, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_cursor_y_mask': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 3, 'orelse', 5, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'action_cursor_y_stride': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 3, 'orelse', 6, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_cursor_y_bias': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 3, 'orelse', 7, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_cursor_pattern': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 4, 'value', 'args', 3),), 'coupled_uses': ()}, 'action_cursor_attributes': {'function': '_duel_action_menu_highlight_fields', 'paths': (('body', 5, 'value', 'args', 3),), 'coupled_uses': ()}}
_CURRENT_SHARED_ROLE_ALIASES125 = {'action_timer_step': 'timer_step'}
ROLE_SPECS = tuple(MenuRole(role.name, _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('function', role.function), _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('paths', role.paths), _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('kind', role.kind), role.default, _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('physical_pcs', role.physical_pcs), coupled_uses=_CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('coupled_uses', role.coupled_uses)) for role in ROLE_SPECS if role.name not in _CURRENT_SHARED_ROLE_ALIASES125)

def owner_rules(values):
    """Turn extracted actual source roles into the one physical owner's rules.

    The common path grammar validates literals/relations and couples repeated
    nodes.  Constraints specific to the native BYTE, MOVEQ and four-byte table
    stay here; nothing truncates an unsupported input into an admitted value.
    """
    values = dict(values)
    for _alias, _authority in _CURRENT_SHARED_ROLE_ALIASES125.items():
        if _authority not in values:
            raise CompileError('actual shared current source role authority required')
        values[_alias] = values[_authority]
    rules = {}
    for role in _ORIGINAL_NATIVE_ROLE_SPECS125:
        if role.name not in values:
            raise CompileError('complete action-menu source roles required')
        value = values[role.name]
        if role.kind == 'unsigned_relation':
            if type(value) is not str or value not in _FALSE_BRANCH:
                raise CompileError(role.name + ': supported unsigned relation required')
        else:
            if type(value) is not int:
                raise CompileError(role.name + ': strict integer role required')
            maximum = 255 if role.kind == 'byte' else 65535
            minimum = 0
            if role.kind == 'quick':
                minimum, maximum = (1, 8)
            elif role.kind in ('nonzero_word', 'signed_word_pair'):
                minimum = 1
            elif role.kind == 'long_bit':
                minimum, maximum = (1, 2147483648)
            if not minimum <= value <= maximum:
                raise CompileError(role.name + ': native width/range exceeded')
            if role.kind == 'long_bit' and value & value - 1:
                raise CompileError(role.name + ': exactly one LONG bit required')
        rules[role.name.removeprefix('action_')] = value
    if rules['unrestricted_bound'] == 0:
        raise CompileError('action unrestricted bound must be a nonzero BYTE')
    for name in ('restricted_forward_wrap', 'restricted_backward_wrap'):
        if rules[name] > 127:
            raise CompileError(name + ': nonnegative signed MOVEQ immediate 0..127 required')
    if rules['restricted_cursor_index_mask'] > 3:
        raise CompileError('restricted cursor mask must stay in the existing four-byte table')
    for name in ('vertical_forward_mask', 'vertical_backward_mask', 'horizontal_forward_mask', 'confirm_mask'):
        rules[name.removesuffix('_mask') + '_bit'] = rules[name].bit_length() - 1
    rules['restricted_branch'] = _TRUE_BRANCH[rules['restricted_relation']]
    for prefix in ('unrestricted', 'restricted_forward_skip', 'restricted_forward', 'restricted_backward_skip'):
        rules[prefix + '_branch'] = _FALSE_BRANCH[rules[prefix + '_relation']]
    return {'choose_duel_action_menu': rules}
