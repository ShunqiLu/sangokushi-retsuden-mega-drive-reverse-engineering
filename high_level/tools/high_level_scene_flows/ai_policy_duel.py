"""Source-role allocation and ordinary native lowering for the complete duel AI.

The business Python supplied to the parent compiler is the policy authority.
These exact paths address functions after the first optional docstring is
removed. All other effects remain subject to the parent's complete finite AST
matcher. No function body, ROM, object or old assembly is read at generation.

Widths, live reads, genuine random-pair calls, shared returns and indexed
control boundaries keep their existing native allocations. The probability
borrow observation remains the original CMP.W carry ABI; its relation is not
an independently editable branch. This is not a general Python compiler or a
natural gameplay proof.
"""
from .menu_policy_duel import MenuRole
from .compiler_common import CompileError


ROLE_SPECS = (
    MenuRole('ai_command_cooldown_step', 'choose_duel_ai_command', (('body', 13, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),), 'quick', 1, (172704,)),
    MenuRole('ai_command_cooldown_mask', 'choose_duel_ai_command', (('body', 22, 'body', 0, 'value', 'args', 2),), 'word', 31, (172748,)),
    MenuRole('ai_command_cooldown_bias', 'choose_duel_ai_command', (('body', 22, 'body', 1, 'value', 'keywords', 0, 'value', 'args', 1, 'args', 0, 'right'),), 'word', 30, (172752,)),
    MenuRole('ai_command_opponent_zero_command', 'choose_duel_ai_command', (('body', 21, 'body', 0, 'value', 'keywords', 0, 'value', 'args', 1),), 'word', 256, (172730,)),
    MenuRole('ai_command_profile_shift', 'choose_duel_ai_command', (('body', 22, 'body', 17, 'value', 'args', 0, 'right'),), 'shift', 1, (172792,)),
    MenuRole('ai_command_executor_shift', 'choose_duel_ai_command', (('body', 24, 'value', 'args', 0, 'right'),), 'shift', 2, (172802,)),
    MenuRole('ai_override_tick_mask', '_choose_duel_ai_override_current', (('body', 5, 'value', 'right'),), 'word', 7, (173564,)),
    MenuRole('ai_override_first_opponent_bound', '_choose_duel_ai_override_current', (('body', 8, 'body', 1, 'test', 'comparators', 0),), 'word', 51, (173584,)),
    MenuRole('ai_override_first_opponent_relation', '_choose_duel_ai_override_current', (('body', 8, 'body', 1, 'test', 'ops', 0),), 'unsigned_relation', '<', (173590,)),
    MenuRole('ai_override_first_low_bound', '_choose_duel_ai_override_current', (('body', 8, 'body', 8, 'test', 'comparators', 0),), 'word', 40, (173640,)),
    MenuRole('ai_override_first_low_relation', '_choose_duel_ai_override_current', (('body', 8, 'body', 8, 'test', 'ops', 0),), 'unsigned_relation', '<', (173644,)),
    MenuRole('ai_override_first_high_bound', '_choose_duel_ai_override_current', (('body', 8, 'body', 9, 'test', 'comparators', 0),), 'word', 70, (173648,)),
    MenuRole('ai_override_first_high_relation', '_choose_duel_ai_override_current', (('body', 8, 'body', 9, 'test', 'ops', 0),), 'unsigned_relation', '>=', (173652,)),
    MenuRole('ai_override_first_high_strength_relation', '_choose_duel_ai_override_current', (('body', 8, 'body', 9, 'body', 0, 'test', 'ops', 0),), 'unsigned_relation', '>=', (173658,)),
    MenuRole('ai_override_first_mid_strength_relation', '_choose_duel_ai_override_current', (('body', 8, 'body', 10, 'test', 'ops', 0),), 'unsigned_relation', '<', (173700,)),
    MenuRole('ai_override_first_low_opponent_mask', '_choose_duel_ai_override_current', (('body', 8, 'body', 1, 'body', 0, 'value', 'args', 2),), 'word', 1, (173600,)),
    MenuRole('ai_override_first_high_opponent_mask', '_choose_duel_ai_override_current', (('body', 8, 'body', 1, 'orelse', 0, 'value', 'args', 2),), 'word', 3, (173620,)),
    MenuRole('ai_override_first_low_or_mid_mask', '_choose_duel_ai_override_current', (('body', 8, 'body', 8, 'body', 0, 'value', 'args', 2), ('body', 8, 'body', 10, 'orelse', 0, 'value', 'args', 2)), 'word', 3, (173708,)),
    MenuRole('ai_override_first_high_or_mid_mask', '_choose_duel_ai_override_current', (('body', 8, 'body', 9, 'body', 0, 'body', 0, 'value', 'args', 2), ('body', 8, 'body', 10, 'body', 0, 'value', 'args', 2)), 'word', 1, (173668,)),
    MenuRole('ai_override_first_high_weak_mask', '_choose_duel_ai_override_current', (('body', 8, 'body', 9, 'body', 1, 'value', 'args', 2),), 'word', 3, (173690,)),
    MenuRole('ai_override_command_40', '_choose_duel_ai_override_current', (('body', 8, 'body', 1, 'body', 1, 'body', 0, 'value', 'args', 1), ('body', 8, 'body', 1, 'orelse', 1, 'value', 'args', 1, 'body'), ('body', 13, 'body', 2, 'body', 0, 'value', 'args', 1), ('body', 15, 'body', 9, 'value', 'args', 1, 'body')), 'word', 64, (173608,)),
    MenuRole('ai_override_command_43', '_choose_duel_ai_override_current', (('body', 8, 'body', 8, 'body', 1, 'value', 'args', 1, 'body'), ('body', 8, 'body', 9, 'body', 0, 'body', 1, 'value', 'args', 1, 'body'), ('body', 8, 'body', 9, 'body', 2, 'value', 'args', 1, 'body'), ('body', 8, 'body', 11, 'value', 'args', 1, 'body'), ('body', 15, 'body', 7, 'body', 0, 'value', 'args', 1), ('body', 25, 'body', 0, 'value', 'args', 1)), 'word', 67, (173678,)),
    MenuRole('ai_override_command_42', '_choose_duel_ai_override_current', (('body', 27, 'value', 'args', 1, 'body'),), 'word', 66, (174034,)),
    MenuRole('ai_override_command_21', '_choose_duel_ai_override_current', (('body', 13, 'body', 4, 'value', 'args', 1, 'body'),), 'word', 33, (174586,)),
    MenuRole('ai_override_second_readiness_relation', '_choose_duel_ai_override_current', (('body', 13, 'test', 'ops', 0),), 'unsigned_relation', '<', (173726,)),
    MenuRole('ai_override_second_high_bound', '_choose_duel_ai_override_current', (('body', 14, 'test', 'comparators', 0),), 'word', 80, (173738,)),
    MenuRole('ai_override_second_mid_bound', '_choose_duel_ai_override_current', (('body', 15, 'test', 'comparators', 0),), 'word', 50, (173730,)),
    MenuRole('ai_override_second_strength_relation', '_choose_duel_ai_override_current', (('body', 15, 'body', 4, 'value', 'test', 'ops', 0),), 'unsigned_relation', '>=', (173782,)),
    MenuRole('ai_override_offset_low_bound', '_choose_duel_ai_override_current', (('body', 22, 'test', 'comparators', 0),), 'word', 4, (173848,)),
    MenuRole('ai_override_offset_low_relation', '_choose_duel_ai_override_current', (('body', 22, 'test', 'ops', 0),), 'unsigned_relation', '<', (173852,)),
    MenuRole('ai_override_offset_high_bound', '_choose_duel_ai_override_current', (('body', 22, 'orelse', 0, 'test', 'comparators', 0), ('body', 22, 'orelse', 0, 'orelse', 0, 'test', 'comparators', 0)), 'word', 8, (173856,)),
    MenuRole('ai_override_offset_mid_relation', '_choose_duel_ai_override_current', (('body', 22, 'orelse', 0, 'test', 'ops', 0),), 'unsigned_relation', '<', (173860,)),
    MenuRole('ai_override_offset_equal_relation', '_choose_duel_ai_override_current', (('body', 22, 'orelse', 0, 'orelse', 0, 'test', 'ops', 0),), 'unsigned_relation', '==', (173864,)),
    MenuRole('ai_override_live_mode_selector', '_sample_duel_live_mode_values', (('body', 1, 'orelse', 0, 'value', 'test', 'comparators', 0),), 'word', 2, (173884, 173930, 174056, 174102, 174220, 174266, 174386, 174432)),
    MenuRole('ai_probability_mask', 'sample_duel_probability', (('body', 4, 'value', 'right'),), 'word', 7, (174594,)),
    MenuRole('ai_probability_shift', 'sample_duel_probability', (('body', 5, 'value', 'right'),), 'shift', 4, (174598,)),
    MenuRole('ai_timeout_timer_bound', 'choose_duel_ai_timeout', (('body', 8, 'test', 'comparators', 0),), 'word', 6144, (174688,)),
    MenuRole('ai_timeout_timer_relation', 'choose_duel_ai_timeout', (('body', 8, 'test', 'ops', 0),), 'unsigned_relation', '>', (174696,)),
    MenuRole('ai_timeout_mode_bound', 'choose_duel_ai_timeout', (('body', 8, 'body', 0, 'test', 'comparators', 0),), 'word', 771, (174700,)),
    MenuRole('ai_timeout_mode_relation', 'choose_duel_ai_timeout', (('body', 8, 'body', 0, 'test', 'ops', 0),), 'unsigned_relation', '==', (174708,)),
    MenuRole('ai_timeout_readiness_relation', 'choose_duel_ai_timeout', (('body', 8, 'body', 0, 'body', 2, 'test', 'ops', 0),), 'unsigned_relation', '<=', (174720,)),
    MenuRole('ai_timeout_command', 'choose_duel_ai_timeout', (('body', 8, 'body', 0, 'body', 2, 'body', 0, 'value'),), 'word', 67, (174724,)),
)


_OWNER_ROLE_NAMES = {'choose_duel_ai_command': ('ai_command_cooldown_step', 'ai_command_cooldown_mask', 'ai_command_cooldown_bias', 'ai_command_opponent_zero_command', 'ai_command_profile_shift', 'ai_command_executor_shift'), 'choose_duel_ai_override': ('ai_override_tick_mask', 'ai_override_first_opponent_bound', 'ai_override_first_opponent_relation', 'ai_override_first_low_bound', 'ai_override_first_low_relation', 'ai_override_first_high_bound', 'ai_override_first_high_relation', 'ai_override_first_high_strength_relation', 'ai_override_first_mid_strength_relation', 'ai_override_first_low_opponent_mask', 'ai_override_first_high_opponent_mask', 'ai_override_first_low_or_mid_mask', 'ai_override_first_high_or_mid_mask', 'ai_override_first_high_weak_mask', 'ai_override_command_40', 'ai_override_command_43', 'ai_override_command_42', 'ai_override_command_21', 'ai_override_second_readiness_relation', 'ai_override_second_high_bound', 'ai_override_second_mid_bound', 'ai_override_second_strength_relation', 'ai_override_offset_low_bound', 'ai_override_offset_low_relation', 'ai_override_offset_high_bound', 'ai_override_offset_mid_relation', 'ai_override_offset_equal_relation', 'ai_override_live_mode_selector'), 'sample_duel_probability': ('ai_probability_mask', 'ai_probability_shift'), 'choose_duel_ai_timeout': ('ai_timeout_timer_bound', 'ai_timeout_timer_relation', 'ai_timeout_mode_bound', 'ai_timeout_mode_relation', 'ai_timeout_readiness_relation', 'ai_timeout_command')}

_RELATION_OWNERS = {'ai_override_first_opponent_relation': ('choose_duel_ai_override', False), 'ai_override_first_low_relation': ('choose_duel_ai_override', True), 'ai_override_first_high_relation': ('choose_duel_ai_override', False), 'ai_override_first_high_strength_relation': ('choose_duel_ai_override', False), 'ai_override_first_mid_strength_relation': ('choose_duel_ai_override', True), 'ai_override_second_readiness_relation': ('choose_duel_ai_override', True), 'ai_override_second_strength_relation': ('choose_duel_ai_override', False), 'ai_override_offset_low_relation': ('choose_duel_ai_override', True), 'ai_override_offset_mid_relation': ('choose_duel_ai_override', True), 'ai_override_offset_equal_relation': ('choose_duel_ai_override', True), 'ai_timeout_timer_relation': ('choose_duel_ai_timeout', False), 'ai_timeout_mode_relation': ('choose_duel_ai_timeout', False), 'ai_timeout_readiness_relation': ('choose_duel_ai_timeout', False)}

_TRUE_BRANCH = {'<': 'bcs', '<=': 'bls', '>': 'bhi', '>=': 'bcc', '==': 'beq', '!=': 'bne'}
_FALSE_BRANCH = {'<': 'bcc', '<=': 'bhi', '>': 'bls', '>=': 'bcs', '==': 'bne', '!=': 'beq'}


def owner_rules(values):
    """Allocate admitted actual role values to four unique physical owners.

    The second-side source checks its high cutoff before its middle cutoff;
    the native schedule checks middle first. The two schedules are equivalent
    only while middle <= high. Other topology changes remain rejected by the
    parent's full supplied-body matcher rather than silently discarded.
    """
    if values['ai_override_second_mid_bound'] > values['ai_override_second_high_bound']:
        raise CompileError('AI second readiness middle cutoff must not exceed its high cutoff')
    result = {}
    for owner, names in _OWNER_ROLE_NAMES.items():
        result[owner] = {name: values[name] for name in names}
    for name, (owner, when_true) in _RELATION_OWNERS.items():
        relation = values[name]
        branches = _TRUE_BRANCH if when_true else _FALSE_BRANCH
        if type(relation) is not str or relation not in branches:
            raise CompileError(name + ': declared unsigned WORD relation required')
        result[owner][name + '_branch'] = branches[relation]
    return result


def _lower_ai_command(emitter, rules):
    emitter.segment(172698, 172808)
    emitter.ins('tst.w', '0x22(%a0)', 4)
    emitter.ins('beq.b', 'scene_pc_02a2a4', 2)
    emitter.ins('subq.w', f"#0x{rules['ai_command_cooldown_step']:x},0x22(%a0)", 4)
    emitter.ins('move.w', '0x1c(%a0),%d0', 4)
    emitter.ins('bne.b', 'scene_pc_02a2b4', 2)
    emitter.ins('move.w', '%d0,0x2(%a0)', 4)
    emitter.ins('move.w', '%d0,0x4(%a0)', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('move.w', '0x1c(%a1),%d0', 4)
    emitter.ins('bne.b', 'scene_pc_02a2c0', 2)
    emitter.ins('move.w', f"#0x{rules['ai_command_opponent_zero_command']:x},%d0", 4)
    emitter.ins('rts', '', 2)
    emitter.ins('tst.w', '0x22(%a0)', 4)
    emitter.ins('bne.b', 'scene_pc_02a2fe', 2)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('andi.w', f"#0x{rules['ai_command_cooldown_mask']:x},%d0", 4)
    emitter.ins('addi.w', f"#0x{rules['ai_command_cooldown_bias']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0x22(%a0)', 4)
    emitter.ins('move.w', '0x1e(%a0),%d0', 4)
    emitter.ins('lea.l', '42(%pc),%a2', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bsr.w', 'scene_pc_028f90', 4)
    emitter.ins('move.w', '%d1,%d6', 2)
    emitter.ins('bsr.w', 'scene_pc_02a5f4', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa60', 4)
    emitter.ins('move.w', '%d7,%d0', 2)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.b', 'scene_pc_02a2b2', 2)
    emitter.ins('move.w', '%d6,%d1', 2)
    emitter.ins('asl.w', f"#0x{rules['ai_command_profile_shift']:x},%d1", 2)
    emitter.ins('jsr', '24(%pc, %d1.w)', 4)
    emitter.ins('move.w', '0x24(%a0),%d0', 4)
    emitter.ins('asl.w', f"#0x{rules['ai_command_executor_shift']:x},%d0", 2)
    emitter.ins('jmp', '38(%pc, %d0.w)', 4)
def _lower_ai_override(emitter, rules):
    emitter.segment(173556, 173748)
    emitter.ins('clr.w', '%d7', 2)
    emitter.ins('move.w', '0xff7008:l,%d1', 6)
    emitter.ins('andi.w', f"#0x{rules['ai_override_tick_mask']:x},%d1", 4)
    emitter.ins('beq.w', 'scene_pc_02a606', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('cmpa.l', '#0xff7050,%a0', 6)
    emitter.ins('bne.w', 'scene_pc_02a694', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_first_opponent_bound']:x},0x1c(%a1)", 6)
    emitter.ins(rules['ai_override_first_opponent_relation_branch'] + '.w', 'scene_pc_02a62e', 4)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('andi.w', f"#0x{rules['ai_override_first_low_opponent_mask']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_02a63c', 4)
    emitter.ins('move.w', f"#0x{rules['ai_override_command_40']:x},%d7", 4)
    emitter.ins('rts', '', 2)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('andi.w', f"#0x{rules['ai_override_first_high_opponent_mask']:x},%d0", 4)
    emitter.ins('beq.b', 'scene_pc_02a628', 2)
    emitter.ins('rts', '', 2)
    emitter.ins('move.w', '0x1e(%a1),%d2', 4)
    emitter.ins('move.w', '0x1e(%a0),%d3', 4)
    emitter.ins('move.w', '0x1c(%a0),%d1', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_first_low_bound']:x},%d1", 4)
    emitter.ins(rules['ai_override_first_low_relation_branch'] + '.w', 'scene_pc_02a686', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_first_high_bound']:x},%d1", 4)
    emitter.ins(rules['ai_override_first_high_relation_branch'] + '.w', 'scene_pc_02a682', 4)
    emitter.ins('cmp.w', '%d3,%d2', 2)
    emitter.ins(rules['ai_override_first_high_strength_relation_branch'] + '.w', 'scene_pc_02a674', 4)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('andi.w', f"#0x{rules['ai_override_first_high_or_mid_mask']:x},%d0", 4)
    emitter.ins('bne.w', 'scene_pc_02a66e', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('move.w', f"#0x{rules['ai_override_command_43']:x},%d7", 4)
    emitter.ins('rts', '', 2)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('andi.w', f"#0x{rules['ai_override_first_high_weak_mask']:x},%d0", 4)
    emitter.ins('beq.b', 'scene_pc_02a66e', 2)
    emitter.ins('rts', '', 2)
    emitter.ins('cmp.w', '%d3,%d2', 2)
    emitter.ins(rules['ai_override_first_mid_strength_relation_branch'] + '.b', 'scene_pc_02a65e', 2)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('andi.w', f"#0x{rules['ai_override_first_low_or_mid_mask']:x},%d0", 4)
    emitter.ins('bne.b', 'scene_pc_02a66e', 2)
    emitter.ins('rts', '', 2)
    emitter.ins('move.w', '0x1c(%a1),%d2', 4)
    emitter.ins('move.w', '0x1c(%a0),%d3', 4)
    emitter.ins('cmp.w', '%d3,%d2', 2)
    emitter.ins(rules['ai_override_second_readiness_relation_branch'] + '.w', 'scene_pc_02a9c8', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_second_mid_bound']:x},%d3", 4)
    emitter.ins('bcs.w', 'scene_pc_02a70c', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_second_high_bound']:x},%d3", 4)
    emitter.ins('bcs.w', 'scene_pc_02a6cc', 4)
    emitter.ins('rts', '', 2)
    emitter.segment(173772, 173810)
    emitter.ins('move.w', '0x1e(%a1),%d2', 4)
    emitter.ins('move.w', '0x1e(%a0),%d3', 4)
    emitter.ins('cmp.w', '%d3,%d2', 2)
    emitter.ins(rules['ai_override_second_strength_relation_branch'] + '.w', 'scene_pc_02a6fe', 4)
    emitter.ins('move.w', '-40(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.b', 'scene_pc_02a66e', 2)
    emitter.ins('move.w', '-38(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a628', 4)
    emitter.ins('rts', '', 2)
    emitter.segment(173822, 173962)
    emitter.ins('move.w', '-14(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a66e', 4)
    emitter.ins('bra.b', 'scene_pc_02a6e4', 2)
    emitter.ins('move.w', '0x1e(%a1),%d0', 4)
    emitter.ins('lea.l', '-1034(%pc),%a2', 4)
    emitter.ins('bsr.w', 'scene_pc_028f90', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_offset_low_bound']:x},%d1", 4)
    emitter.ins(rules['ai_override_offset_low_relation_branch'] + '.w', 'scene_pc_02a922', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_offset_high_bound']:x},%d1", 4)
    emitter.ins(rules['ai_override_offset_mid_relation_branch'] + '.w', 'scene_pc_02a87c', 4)
    emitter.ins(rules['ai_override_offset_equal_relation_branch'] + '.w', 'scene_pc_02a7d8', 4)
    emitter.ins('tst.w', '0xefd2:w', 4)
    emitter.ins('bne.w', 'scene_pc_02a73c', 4)
    emitter.ins('move.w', '84(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a752', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_live_mode_selector']:x},0xefd2:w", 6)
    emitter.ins('beq.w', 'scene_pc_02a74e', 4)
    emitter.ins('move.w', '90(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a752', 4)
    emitter.ins('move.w', '106(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a66e', 4)
    emitter.ins('tst.w', '0xefd2:w', 4)
    emitter.ins('bne.w', 'scene_pc_02a76a', 4)
    emitter.ins('move.w', '50(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a780', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_live_mode_selector']:x},0xefd2:w", 6)
    emitter.ins('beq.w', 'scene_pc_02a77c', 4)
    emitter.ins('move.w', '56(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a780', 4)
    emitter.ins('move.w', '72(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a7d2', 4)
    emitter.ins('rts', '', 2)
    emitter.segment(174034, 174132)
    emitter.ins('move.w', f"#0x{rules['ai_override_command_42']:x},%d7", 4)
    emitter.ins('rts', '', 2)
    emitter.ins('tst.w', '0xefd2:w', 4)
    emitter.ins('bne.w', 'scene_pc_02a7e8', 4)
    emitter.ins('move.w', '82(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a7fe', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_live_mode_selector']:x},0xefd2:w", 6)
    emitter.ins('beq.w', 'scene_pc_02a7fa', 4)
    emitter.ins('move.w', '88(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a7fe', 4)
    emitter.ins('move.w', '104(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a66e', 4)
    emitter.ins('tst.w', '0xefd2:w', 4)
    emitter.ins('bne.w', 'scene_pc_02a816', 4)
    emitter.ins('move.w', '48(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a82c', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_live_mode_selector']:x},0xefd2:w", 6)
    emitter.ins('beq.w', 'scene_pc_02a828', 4)
    emitter.ins('move.w', '54(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a82c', 4)
    emitter.ins('move.w', '70(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.b', 'scene_pc_02a7d2', 2)
    emitter.ins('rts', '', 2)
    emitter.segment(174204, 174298)
    emitter.ins('tst.w', '0xefd2:w', 4)
    emitter.ins('bne.w', 'scene_pc_02a88c', 4)
    emitter.ins('move.w', '84(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a8a2', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_live_mode_selector']:x},0xefd2:w", 6)
    emitter.ins('beq.w', 'scene_pc_02a89e', 4)
    emitter.ins('move.w', '90(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a8a2', 4)
    emitter.ins('move.w', '106(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a66e', 4)
    emitter.ins('tst.w', '0xefd2:w', 4)
    emitter.ins('bne.w', 'scene_pc_02a8ba', 4)
    emitter.ins('move.w', '50(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a8d0', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_live_mode_selector']:x},0xefd2:w", 6)
    emitter.ins('beq.w', 'scene_pc_02a8cc', 4)
    emitter.ins('move.w', '56(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a8d0', 4)
    emitter.ins('move.w', '72(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a7d2', 4)
    emitter.ins('rts', '', 2)
    emitter.segment(174370, 174464)
    emitter.ins('tst.w', '0xefd2:w', 4)
    emitter.ins('bne.w', 'scene_pc_02a932', 4)
    emitter.ins('move.w', '84(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a948', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_live_mode_selector']:x},0xefd2:w", 6)
    emitter.ins('beq.w', 'scene_pc_02a944', 4)
    emitter.ins('move.w', '90(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a948', 4)
    emitter.ins('move.w', '106(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a66e', 4)
    emitter.ins('tst.w', '0xefd2:w', 4)
    emitter.ins('bne.w', 'scene_pc_02a960', 4)
    emitter.ins('move.w', '50(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a976', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_override_live_mode_selector']:x},0xefd2:w", 6)
    emitter.ins('beq.w', 'scene_pc_02a972', 4)
    emitter.ins('move.w', '56(%pc, %d6.w),%d2', 4)
    emitter.ins('bra.w', 'scene_pc_02a976', 4)
    emitter.ins('move.w', '72(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a7d2', 4)
    emitter.ins('rts', '', 2)
    emitter.segment(174536, 174562)
    emitter.ins('move.w', '24(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a628', 4)
    emitter.ins('move.w', '24(%pc, %d6.w),%d2', 4)
    emitter.ins('bsr.w', 'scene_pc_02aa00', 4)
    emitter.ins('bcs.w', 'scene_pc_02a9fa', 4)
    emitter.ins('rts', '', 2)
    emitter.segment(174586, 174592)
    emitter.ins('move.w', f"#0x{rules['ai_override_command_21']:x},%d7", 4)
    emitter.ins('rts', '', 2)
def _lower_ai_probability(emitter, rules):
    emitter.segment(174592, 174612)
    emitter.ins('move.w', '%d2,%d3', 2)
    emitter.ins('andi.w', f"#0x{rules['ai_probability_mask']:x},%d2", 4)
    emitter.ins('lsr.w', f"#0x{rules['ai_probability_shift']:x},%d3", 2)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('and.w', '%d2,%d0', 2)
    emitter.ins('cmp.w', '%d3,%d0', 2)
    emitter.ins('rts', '', 2)
def _lower_ai_timeout(emitter, rules):
    emitter.segment(174688, 174734)
    emitter.ins('cmpi.w', f"#0x{rules['ai_timeout_timer_bound']:x},0xff70fa:l", 8)
    emitter.ins(rules['ai_timeout_timer_relation_branch'] + '.w', 'scene_pc_02aa8a', 4)
    emitter.ins('cmpi.w', f"#0x{rules['ai_timeout_mode_bound']:x},0xff700a:l", 8)
    emitter.ins(rules['ai_timeout_mode_relation_branch'] + '.w', 'scene_pc_02aa8a', 4)
    emitter.ins('move.w', '0x1c(%a0),%d0', 4)
    emitter.ins('cmp.w', '0x1c(%a1),%d0', 4)
    emitter.ins(rules['ai_timeout_readiness_relation_branch'] + '.w', 'scene_pc_02aa8a', 4)
    emitter.ins('move.w', f"#0x{rules['ai_timeout_command']:x},%d7", 4)
    emitter.ins('rts', '', 2)
    emitter.ins('clr.l', '%d0', 2)
    emitter.ins('rts', '', 2)

LOWERERS = {'choose_duel_ai_command': _lower_ai_command,
            'choose_duel_ai_override': _lower_ai_override,
            'sample_duel_probability': _lower_ai_probability,
            'choose_duel_ai_timeout': _lower_ai_timeout}


# Root49 relocates all AI source authority, ordinary native allocation unchanged.
_STRATEGY_FIELDS_ROLES = {'ai_command_cooldown_step': {'function': 'choose_duel_ai_command_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'ai_command_cooldown_mask': {'function': 'choose_duel_ai_command_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'ai_command_cooldown_bias': {'function': 'choose_duel_ai_command_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'ai_command_opponent_zero_command': {'function': 'choose_duel_ai_command_fields', 'paths': (('body', 3, 'value'),), 'coupled_uses': ()}, 'ai_command_profile_shift': {'function': 'choose_duel_ai_command_fields', 'paths': (('body', 4, 'value'),), 'coupled_uses': ()}, 'ai_command_executor_shift': {'function': 'choose_duel_ai_command_fields', 'paths': (('body', 5, 'value'),), 'coupled_uses': ()}, 'ai_override_tick_mask': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'ai_override_first_opponent_bound': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'ai_override_first_low_bound': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'ai_override_first_high_bound': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 3, 'value'),), 'coupled_uses': ()}, 'ai_override_first_low_opponent_mask': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 8, 'value'),), 'coupled_uses': ()}, 'ai_override_first_high_opponent_mask': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 9, 'value'),), 'coupled_uses': ()}, 'ai_override_first_low_or_mid_mask': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 10, 'value'),), 'coupled_uses': ()}, 'ai_override_first_high_or_mid_mask': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 11, 'value'),), 'coupled_uses': ()}, 'ai_override_first_high_weak_mask': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 12, 'value'),), 'coupled_uses': ()}, 'ai_override_command_40': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 13, 'value'),), 'coupled_uses': ()}, 'ai_override_command_43': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 14, 'value'),), 'coupled_uses': ()}, 'ai_override_command_42': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 15, 'value'),), 'coupled_uses': ()}, 'ai_override_command_21': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 16, 'value'),), 'coupled_uses': ()}, 'ai_override_second_high_bound': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 5, 'value'),), 'coupled_uses': ()}, 'ai_override_second_mid_bound': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 4, 'value'),), 'coupled_uses': ()}, 'ai_override_offset_low_bound': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 6, 'value'),), 'coupled_uses': ()}, 'ai_override_offset_high_bound': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 7, 'value'),), 'coupled_uses': ()}, 'ai_override_live_mode_selector': {'function': '_duel_strategy_live_mode_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'ai_probability_mask': {'function': 'sample_duel_probability_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'ai_probability_shift': {'function': 'sample_duel_probability_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'ai_timeout_timer_bound': {'function': 'choose_duel_ai_timeout_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'ai_timeout_mode_bound': {'function': 'choose_duel_ai_timeout_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'ai_timeout_command': {'function': 'choose_duel_ai_timeout_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'ai_override_first_opponent_relation': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 23, 'body', 2, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_override_first_low_relation': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 23, 'body', 9, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_override_first_high_relation': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 23, 'body', 11, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_override_first_high_strength_relation': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 23, 'body', 11, 'body', 1, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_override_first_mid_strength_relation': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 23, 'body', 11, 'orelse', 1, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_override_second_readiness_relation': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 28, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_override_second_strength_relation': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 30, 'body', 6, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_override_offset_low_relation': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 36, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_override_offset_mid_relation': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 36, 'orelse', 1, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_override_offset_equal_relation': {'function': 'choose_duel_ai_override_fields', 'paths': (('body', 36, 'orelse', 1, 'orelse', 0, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_timeout_timer_relation': {'function': 'choose_duel_ai_timeout_fields', 'paths': (('body', 6, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_timeout_mode_relation': {'function': 'choose_duel_ai_timeout_fields', 'paths': (('body', 6, 'body', 2, 'test', 'ops', 0),), 'coupled_uses': ()}, 'ai_timeout_readiness_relation': {'function': 'choose_duel_ai_timeout_fields', 'paths': (('body', 6, 'body', 2, 'body', 4, 'test', 'ops', 0),), 'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_STRATEGY_FIELDS_ROLES[role.name]['function'],_STRATEGY_FIELDS_ROLES[role.name]['paths'],role.kind,role.default,role.physical_pcs,coupled_uses=_STRATEGY_FIELDS_ROLES[role.name]['coupled_uses']) for role in ROLE_SPECS)
