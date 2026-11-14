"""Finite source-driven lowering of the complete duel lifecycle family.

Seven physical owners retain their original spans, call allocation, WORD and
BYTE partial writes, live waits and nonlocal continuation. Named role values
come from the complete supplied business source; no original/source/IR/object
fallback exists here. Resource layout, dynamic target domain, IRQ/full CPU and
unregistered structural changes are deliberately not inferred.
"""
from __future__ import annotations

from .compiler_common import CompileError
from .menu_policy_duel import MenuRole


ROLE_SPECS = (
    MenuRole('flow_entry_palette_bound', 'advance_duel_entry_palette', (('body', 2, 'test', 'comparators', 0),),
        'word', 16, (159110,),
        coupled_uses=()),
    MenuRole('flow_entry_palette_relation', 'advance_duel_entry_palette', (('body', 2, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (159118,),
        coupled_uses=()),
    MenuRole('flow_entry_palette_complement', 'advance_duel_entry_palette', (('body', 3, 'value', 'args', 0, 'left'),),
        'word', 15, (159122,),
        coupled_uses=()),
    MenuRole('flow_entry_palette_count', 'advance_duel_entry_palette', (('body', 4, 'body', 0, 'value', 'args', 2), ('body', 4, 'orelse', 1, 'value', 'args', 2), ('body', 4, 'orelse', 1, 'value', 'keywords', 0, 'value', 'args', 1)),
        'word', 64, (159132,),
        coupled_uses=()),
    MenuRole('flow_entry_palette_step', 'advance_duel_entry_palette', (('body', 5, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (159148,),
        coupled_uses=()),
    MenuRole('flow_fade_bound', 'finish_duel_turn_scene', (('body', 2, 'body', 3, 'value', 'args', 2), ('body', 2, 'body', 4, 'test', 'comparators', 0)),
        'word', 16, (159066,),
        coupled_uses=()),
    MenuRole('flow_fade_relation', 'finish_duel_turn_scene', (('body', 2, 'body', 4, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (159074,),
        coupled_uses=()),
    MenuRole('flow_fade_count', 'finish_duel_turn_scene', (('body', 2, 'body', 5, 'value', 'keywords', 1, 'value', 'args', 1),),
        'word', 64, (159084,),
        coupled_uses=()),
    MenuRole('flow_fade_step', 'finish_duel_turn_scene', (('body', 2, 'body', 8, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (159100,),
        coupled_uses=()),
    MenuRole('flow_initial_display_mask', '_initialize_duel_scene', (('body', 9, 'value', 'args', 1, 'right'),),
        'byte', 191, (159164,),
        coupled_uses=()),
    MenuRole('flow_first_initial_position', '_initialize_duel_scene', (('body', 17, 'value', 'args', 1),),
        'long', 4194304, (159240,),
        coupled_uses=()),
    MenuRole('flow_second_initial_position', '_initialize_duel_scene', (('body', 20, 'value', 'args', 1),),
        'long', 16777216, (159266,),
        coupled_uses=()),
    MenuRole('flow_first_initial_attributes', '_initialize_duel_scene', (('body', 18, 'value', 'args', 1),),
        'word', 34816, (159250,),
        coupled_uses=()),
    MenuRole('flow_second_initial_attributes', '_initialize_duel_scene', (('body', 21, 'value', 'args', 1),),
        'word', 40960, (159276,),
        coupled_uses=()),
    MenuRole('flow_initial_actor_state', '_initialize_duel_scene', (('body', 19, 'value', 'args', 1), ('body', 22, 'value', 'args', 1)),
        'word', 1, (159258, 159284),
        coupled_uses=()),
    MenuRole('flow_initial_glyph_background', '_initialize_duel_scene', (('body', 39, 'value', 'args', 1, 'args', 1), ('body', 48, 'body', 1, 'value', 'args', 1, 'args', 1), ('body', 50, 'value', 'args', 1, 'args', 1)),
        'word', 1, (159450, 159524, 159542, 159560),
        coupled_uses=()),
    MenuRole('flow_initial_glyph_foreground', '_initialize_duel_scene', (('body', 39, 'value', 'args', 2, 'args', 1), ('body', 48, 'body', 1, 'value', 'args', 2, 'args', 1), ('body', 50, 'value', 'args', 2, 'args', 1)),
        'word', 2, (159454, 159528, 159546, 159564),
        coupled_uses=()),
    MenuRole('flow_initial_map_variant', '_initialize_duel_scene', (('body', 61, 'test', 'comparators', 0),),
        'word', 3, (159612,),
        coupled_uses=()),
    MenuRole('flow_initial_map_relation', '_initialize_duel_scene', (('body', 61, 'test', 'ops', 0),),
        'unsigned_relation', '==', (159620,),
        coupled_uses=()),
    MenuRole('flow_loadout_dialog_position', 'choose_duel_loadout_complete', (('body', 3, 'body', 0, 'value', 'args', 1), ('body', 6, 'body', 20, 'value', 'args', 1)),
        'word', 50688, (159798, 159962, 160112, 160274),
        coupled_uses=()),
    MenuRole('flow_second_loadout_acknowledgement', 'choose_duel_loadout_complete', (('body', 3, 'body', 1, 'body', 0, 'value', 'args', 1),),
        'word', 1, (160146,),
        coupled_uses=()),
    MenuRole('flow_automatic_mode', 'choose_duel_loadout_complete', (('body', 3, 'test', 'comparators', 0), ('body', 6, 'body', 4, 'test', 'comparators', 0), ('body', 6, 'body', 18, 'test', 'comparators', 0), ('body', 6, 'body', 28, 'body', 0, 'value', 'args', 1)),
        'byte', 3, (159786, 159866, 159946, 160074, 160100, 160178, 160258, 160386, 160638, 160684, 160822, 160852, 161720, 161732),
        coupled_uses=(('_begin_duel_combat_frame', ('body', 8, 'value', 'args', 2)), ('_begin_duel_combat_frame', ('body', 9, 'test', 'comparators', 0)), ('continue_after_first_duel_actor', ('body', 5, 'value', 'args', 2)), ('continue_after_first_duel_actor', ('body', 6, 'test', 'comparators', 0)), ('choose_duel_turn_action_complete', ('body', 9, 'value', 'args', 2)), ('choose_duel_turn_action_complete', ('body', 10, 'test', 'comparators', 0)), ('wait_either_duel_action_complete', ('body', 1, 'test', 'comparators', 0)), ('wait_either_duel_action_complete', ('body', 2, 'test', 'comparators', 0)))),
    MenuRole('flow_loadout_pending_relation', 'choose_duel_loadout_complete', (('body', 6, 'body', 10, 'test', 'ops', 0), ('body', 6, 'body', 22, 'body', 8, 'test', 'ops', 0)),
        'unsigned_relation', '!=', (159898, 160040, 160210, 160352),
        coupled_uses=()),
    MenuRole('flow_preparation_confirm_mask', 'choose_duel_loadout_complete', (('body', 6, 'body', 13, 'value', 'keywords', 0, 'value', 'args', 1, 'right'), ('body', 6, 'body', 22, 'body', 10, 'value', 'keywords', 0, 'value', 'args', 1, 'right')),
        'word', 240, (159930, 160046, 160242, 160358, 160488, 160576),
        coupled_uses=(('_wait_complete_status', ('body', 5, 'body', 5, 'value', 'keywords', 0, 'value', 'args', 1, 'right')),)),
    MenuRole('flow_loadout_equipment_confirm_relation', 'choose_duel_loadout_complete', (('body', 6, 'body', 15, 'test', 'ops', 0),),
        'unsigned_relation', '==', (159934, 160246),
        coupled_uses=()),
    MenuRole('flow_loadout_option_confirm_relation', 'choose_duel_loadout_complete', (('body', 6, 'body', 22, 'body', 12, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (160050, 160362),
        coupled_uses=()),
    MenuRole('flow_loadout_auto_choice_relation', 'choose_duel_loadout_complete', (('body', 6, 'body', 28, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (160070, 160382),
        coupled_uses=()),
    MenuRole('flow_loadout_accept_sound', 'choose_duel_loadout_complete', (('body', 6, 'body', 16, 'value', 'keywords', 0, 'value', 'args', 1), ('body', 6, 'body', 23, 'value', 'keywords', 0, 'value', 'args', 1), ('body', 6, 'body', 17, 'value', 'args', 1), ('body', 6, 'body', 24, 'value', 'args', 1)),
        'byte', 172, (159936, 160052, 160248, 160364, 161076),
        coupled_uses=(('perform_selected_duel_action_complete', ('body', 1, 'value', 'keywords', 0, 'value', 'args', 1)), ('perform_selected_duel_action_complete', ('body', 2, 'value', 'args', 1)))),
    MenuRole('flow_status_random_mask', '_prepare_complete_first_status', (('body', 3, 'value', 'right'),),
        'word', 3, (160418, 160508),
        coupled_uses=(('_prepare_complete_second_status', ('body', 3, 'value', 'right')),)),
    MenuRole('flow_status_wrap_bound', '_prepare_complete_first_status', (('body', 4, 'test', 'comparators', 0),),
        'word', 3, (160422, 160512),
        coupled_uses=(('_prepare_complete_second_status', ('body', 4, 'test', 'comparators', 0)),)),
    MenuRole('flow_status_wrap_relation', '_prepare_complete_first_status', (('body', 4, 'test', 'ops', 0),),
        'unsigned_relation', '==', (160426, 160516),
        coupled_uses=(('_prepare_complete_second_status', ('body', 4, 'test', 'ops', 0)),)),
    MenuRole('flow_second_status_bias', '_prepare_complete_second_status', (('body', 5, 'value', 'args', 0, 'right'),),
        'quick', 3, (160520,),
        coupled_uses=()),
    MenuRole('flow_status_sound', '_prepare_complete_first_status', (('body', 7, 'value', 'keywords', 0, 'value', 'args', 1), ('body', 8, 'value', 'args', 1)),
        'byte', 165, (160436, 160528),
        coupled_uses=(('_prepare_complete_second_status', ('body', 8, 'value', 'keywords', 0, 'value', 'args', 1)), ('_prepare_complete_second_status', ('body', 9, 'value', 'args', 1)))),
    MenuRole('flow_combat_begin_sound', '_prepare_complete_second_status', (('body', 11, 'value', 'keywords', 0, 'value', 'args', 1), ('body', 12, 'value', 'args', 1)),
        'byte', 139, (160582,),
        coupled_uses=()),
    MenuRole('flow_status_pending_relation', '_wait_complete_status', (('body', 5, 'body', 3, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (160482, 160570),
        coupled_uses=()),
    MenuRole('flow_status_confirm_relation', '_wait_complete_status', (('body', 5, 'body', 6, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (160492, 160580),
        coupled_uses=()),
    MenuRole('flow_first_ai_relation', '_begin_duel_combat_frame', (('body', 9, 'test', 'ops', 0),),
        'unsigned_relation', '==', (160646,),
        coupled_uses=()),
    MenuRole('flow_second_ai_relation', 'continue_after_first_duel_actor', (('body', 6, 'test', 'ops', 0),),
        'unsigned_relation', '==', (160692,),
        coupled_uses=()),
    MenuRole('flow_first_terminal_relation', 'continue_after_first_duel_actor', (('body', 12, 'test', 'ops', 0),),
        'unsigned_relation', '==', (160724,),
        coupled_uses=()),
    MenuRole('flow_second_terminal_relation', 'continue_after_first_duel_actor', (('body', 16, 'test', 'ops', 0),),
        'unsigned_relation', '==', (160742,),
        coupled_uses=()),
    MenuRole('flow_pending_action_mask', 'continue_after_first_duel_actor', (('body', 21, 'value'),),
        'word', 53248, (160758,),
        coupled_uses=()),
    MenuRole('flow_action_request_mask', 'continue_after_first_duel_actor', (('body', 26, 'value', 'right'), ('body', 29, 'body', 1, 'value', 'right')),
        'word', 64, (160778, 160798),
        coupled_uses=()),
    MenuRole('flow_manual_mode_relation', 'choose_duel_turn_action_complete', (('body', 10, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (160830, 160860),
        coupled_uses=()),
    MenuRole('flow_same_officer_dialog_relation', 'choose_duel_turn_action_complete', (('body', 10, 'body', 4, 'value', 'ops', 0),),
        'unsigned_relation', '==', (160894, 160910),
        coupled_uses=()),
    MenuRole('flow_same_officer_dialog_position', 'choose_duel_turn_action_complete', (('body', 10, 'body', 5, 'value', 'args', 1, 'body'),),
        'word', 52096, (160914,),
        coupled_uses=()),
    MenuRole('flow_different_officer_dialog_position', 'choose_duel_turn_action_complete', (('body', 10, 'body', 5, 'value', 'args', 1, 'orelse'),),
        'word', 51008, (160934,),
        coupled_uses=()),
    MenuRole('flow_manual_dialog_sound', 'choose_duel_turn_action_complete', (('body', 10, 'body', 6, 'value', 'keywords', 0, 'value', 'args', 1), ('body', 10, 'body', 7, 'value', 'args', 1)),
        'byte', 173, (160952,),
        coupled_uses=()),
    MenuRole('flow_manual_pending_relation', 'continue_manual_duel_action', (('body', 2, 'body', 16, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (161012,),
        coupled_uses=()),
    MenuRole('flow_manual_confirm_bit', 'continue_manual_duel_action', (('body', 2, 'body', 17, 'value', 'args', 2),),
        'word', 5, (161014,),
        coupled_uses=()),
    MenuRole('flow_manual_cancel_bit', 'continue_manual_duel_action', (('body', 2, 'body', 19, 'value', 'args', 2),),
        'word', 4, (161020,),
        coupled_uses=()),
    MenuRole('flow_first_terminal_message', 'show_terminal_duel_result_complete', (('body', 7, 'value', 'keywords', 0, 'value', 'args', 1),),
        'word', 31, (162224,),
        coupled_uses=()),
    MenuRole('flow_second_terminal_message', 'show_terminal_duel_result_complete', (('body', 10, 'body', 0, 'value', 'keywords', 0, 'value', 'args', 1),),
        'word', 34, (162236,),
        coupled_uses=()),
    MenuRole('flow_terminal_followup_message', 'show_terminal_duel_result_complete', (('body', 14, 'value', 'keywords', 0, 'value', 'args', 1),),
        'word', 32, (162252,),
        coupled_uses=()),
    MenuRole('flow_second_terminal_followup_step', 'show_terminal_duel_result_complete', (('body', 16, 'body', 0, 'value', 'keywords', 0, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (162264,),
        coupled_uses=()),
    MenuRole('flow_label_tick_mask', 'show_active_duel_turn_label_complete', (('body', 4, 'test', 'right'),),
        'word', 1, (161046,),
        coupled_uses=()),
    MenuRole('flow_first_label_position', 'show_active_duel_turn_label_complete', (('body', 2, 'value', 'args', 1),),
        'word', 60424, (161036,),
        coupled_uses=()),
    MenuRole('flow_second_label_position', 'show_active_duel_turn_label_complete', (('body', 4, 'body', 1, 'value', 'args', 1),),
        'word', 60484, (161058,),
        coupled_uses=()),
    MenuRole('flow_active_wait_timer_step', 'wait_active_duel_action_complete', (('body', 1, 'body', 1, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (161674,),
        coupled_uses=()),
    MenuRole('flow_either_wait_timer_step', 'wait_either_duel_action_complete', (('body', 3, 'body', 1, 'value', 'args', 1, 'args', 0, 'right'),),
        'quick', 1, (161760,),
        coupled_uses=()),
    MenuRole('flow_active_wait_accept_mask', 'wait_active_duel_action_complete', (('body', 1, 'body', 10, 'value', 'args', 1, 'right'),),
        'word', 112, (161708,),
        coupled_uses=()),
    MenuRole('flow_either_wait_accept_mask', 'wait_either_duel_action_complete', (('body', 3, 'body', 13, 'value', 'args', 1, 'right'),),
        'word', 112, (161798,),
        coupled_uses=()),
    MenuRole('flow_active_wait_pending_relation', 'wait_active_duel_action_complete', (('body', 1, 'body', 5, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (161690,),
        coupled_uses=()),
    MenuRole('flow_either_wait_pending_relation', 'wait_either_duel_action_complete', (('body', 3, 'body', 5, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (161776,),
        coupled_uses=()),
    MenuRole('flow_active_wait_confirm_relation', 'wait_active_duel_action_complete', (('body', 1, 'body', 12, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (161712,),
        coupled_uses=()),
    MenuRole('flow_either_wait_confirm_relation', 'wait_either_duel_action_complete', (('body', 3, 'body', 15, 'test', 'ops', 0),),
        'unsigned_relation', '!=', (161802,),
        coupled_uses=()),
    MenuRole('flow_motion_borrow_relation', 'configure_duel_weapon_motion', (('body', 6, 'test', 'ops', 0),),
        'unsigned_relation', '<', (162376,),
        coupled_uses=()),
    MenuRole('flow_motion_bound', 'configure_duel_weapon_motion', (('body', 6, 'orelse', 0, 'test', 'comparators', 0), ('body', 7, 'value', 'args', 0, 'left'), ('body', 6, 'orelse', 0, 'body', 0, 'value')),
        'word', 80, (162384, 162390, 162394),
        coupled_uses=()),
    MenuRole('flow_motion_cap_relation', 'configure_duel_weapon_motion', (('body', 6, 'orelse', 0, 'test', 'ops', 0),),
        'unsigned_relation', '>=', (162388,),
        coupled_uses=()),
    MenuRole('flow_motion_scale', 'configure_duel_weapon_motion', (('body', 8, 'value', 'args', 0, 'left', 'right'),),
        'word', 1792, (162400,),
        coupled_uses=()),
    MenuRole('flow_motion_bias', 'configure_duel_weapon_motion', (('body', 8, 'value', 'args', 0, 'right'),),
        'long', 24576, (162404,),
        coupled_uses=()),
    MenuRole('flow_motion_divisor', 'configure_duel_weapon_motion', (('body', 10, 'value', 'args', 1),),
        'nonzero_word', 2, (162420,),
        coupled_uses=()),
    MenuRole('flow_status_text_command', 'choose_duel_status_text', (('body', 5, 'value', 'args', 1),),
        'word', 50688, (164406,),
        coupled_uses=(('choose_duel_status_text_complete', ('body', 4, 'value', 'args', 1)),)),
)

_TRUE_BRANCH = {'<': 'bcs', '<=': 'bls', '>': 'bhi', '>=': 'bcc', '==': 'beq', '!=': 'bne'}
_FALSE_BRANCH = {'<': 'bcc', '<=': 'bhi', '>': 'bls', '>=': 'bcs', '==': 'bne', '!=': 'beq'}

_OWNER_ROLES = {'run_duel_scene': ('flow_fade_bound', 'flow_fade_relation', 'flow_fade_count', 'flow_fade_step', 'flow_initial_display_mask', 'flow_first_initial_position', 'flow_second_initial_position', 'flow_first_initial_attributes', 'flow_second_initial_attributes', 'flow_initial_actor_state', 'flow_initial_glyph_background', 'flow_initial_glyph_foreground', 'flow_initial_map_variant', 'flow_initial_map_relation', 'flow_loadout_dialog_position', 'flow_second_loadout_acknowledgement', 'flow_automatic_mode', 'flow_loadout_pending_relation', 'flow_preparation_confirm_mask', 'flow_loadout_equipment_confirm_relation', 'flow_loadout_option_confirm_relation', 'flow_loadout_auto_choice_relation', 'flow_loadout_accept_sound', 'flow_status_random_mask', 'flow_status_wrap_bound', 'flow_status_wrap_relation', 'flow_second_status_bias', 'flow_status_sound', 'flow_combat_begin_sound', 'flow_status_pending_relation', 'flow_status_confirm_relation', 'flow_first_ai_relation', 'flow_second_ai_relation', 'flow_first_terminal_relation', 'flow_second_terminal_relation', 'flow_pending_action_mask', 'flow_action_request_mask', 'flow_manual_mode_relation', 'flow_same_officer_dialog_relation', 'flow_same_officer_dialog_position', 'flow_different_officer_dialog_position', 'flow_manual_dialog_sound', 'flow_manual_pending_relation', 'flow_manual_confirm_bit', 'flow_manual_cancel_bit', 'flow_first_terminal_message', 'flow_second_terminal_message', 'flow_terminal_followup_message', 'flow_second_terminal_followup_step'), 'advance_duel_entry_palette': ('flow_entry_palette_bound', 'flow_entry_palette_relation', 'flow_entry_palette_complement', 'flow_entry_palette_count', 'flow_entry_palette_step'), 'show_active_duel_turn_label': ('flow_label_tick_mask', 'flow_first_label_position', 'flow_second_label_position'), 'wait_active_duel_action': ('flow_automatic_mode', 'flow_active_wait_timer_step', 'flow_either_wait_timer_step', 'flow_active_wait_accept_mask', 'flow_either_wait_accept_mask', 'flow_active_wait_pending_relation', 'flow_either_wait_pending_relation', 'flow_active_wait_confirm_relation', 'flow_either_wait_confirm_relation'), 'configure_duel_weapon_motion': ('flow_motion_borrow_relation', 'flow_motion_bound', 'flow_motion_cap_relation', 'flow_motion_scale', 'flow_motion_bias', 'flow_motion_divisor'), 'refresh_duel_actors': (), 'choose_duel_status_text': ('flow_status_text_command',)}
_CONSTRAINTS = {'flow_manual_confirm_bit': 'bit_index', 'flow_manual_cancel_bit': 'bit_index'}

def owner_rules(values):
    """Validate all actual role values and give every owner its real rules.

    No rule is read by numeric value or falls back to a canonical literal.
    Refresh has no mutable policy: its complete save/clear/render/restore is
    still lowered, but RAM layout and reset semantics are not fabricated slots.
    """
    checked = {}
    limits = {'word': (0, 65535), 'byte': (0, 255), 'long': (0, 0xffffffff),
              'nonzero_word': (1, 65535), 'quick': (1, 8)}
    for role in ROLE_SPECS:
        if role.name not in values:
            raise CompileError('all complete duel lifecycle source roles required')
        value = values[role.name]
        if role.kind == 'unsigned_relation':
            if type(value) is not str or value not in _TRUE_BRANCH:
                raise CompileError(role.name + ': supported unsigned relation required')
        else:
            low, high = limits[role.kind]
            if type(value) is not int or not low <= value <= high:
                raise CompileError(role.name + ': strict bounded source integer required')
            if _CONSTRAINTS.get(role.name) == 'bit_index' and value > 31:
                raise CompileError(role.name + ': actual LONG bit index must be 0..31')
        checked[role.name] = value
    owners = {}
    for owner, names in _OWNER_ROLES.items():
        rules = {name: checked[name] for name in names}
        for role in ROLE_SPECS:
            if role.name in rules and role.kind == 'unsigned_relation':
                rules[role.name + '_true_branch'] = _TRUE_BRANCH[rules[role.name]]
                rules[role.name + '_false_branch'] = _FALSE_BRANCH[rules[role.name]]
        owners[owner] = rules
    return owners


def lower_run_duel_scene(emitter, rules):
    emitter.segment(159046, 159110)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_026d50', 2)
    emitter.ins('bsr.w', 'scene_pc_027a84', 4)
    emitter.ins('cmpi.w', f"#0x{rules['flow_fade_bound']:x},0xff70f6:l", 8)
    emitter.ins(rules['flow_fade_relation_true_branch'] + '.w', 'scene_pc_026d84', 4)
    emitter.ins('move.w', '0xff70f6:l,%d0', 6)
    emitter.ins('move.w', f"#0x{rules['flow_fade_count']:x},%d1", 4)
    emitter.ins('lea.l', '4878(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('jsr', 'scene_pc_00dea6:l', 6)
    emitter.ins('addq.w', f"#0x{rules['flow_fade_step']:x},0xff70f6:l", 6)
    emitter.ins('bra.b', 'scene_pc_026d4a', 2)
    emitter.ins('rts', '', 2)
    emitter.segment(159156, 161030)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('move.w', '0xf606:w,%d0', 4)
    emitter.ins('andi.b', f"#0x{rules['flow_initial_display_mask']:x},%d0", 4)
    emitter.ins('move.w', '%d0,0xc00004:l', 6)
    emitter.ins('clr.w', '0xf612:w', 4)
    emitter.ins('jsr', 'scene_pc_0068ce:l', 6)
    emitter.ins('move.w', '#0x8338,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8238,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8407,0xc00004:l', 8)
    emitter.ins('move.w', '#0x856c,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8d37,0xc00004:l', 8)
    emitter.ins('move.w', '#0x9294,0xc00004:l', 8)
    emitter.ins('move.w', '#0x8b03,0xc00004:l', 8)
    emitter.ins('move.l', f"#0x{rules['flow_first_initial_position']:x},0xff705e:l", 10)
    emitter.ins('move.w', f"#0x{rules['flow_first_initial_attributes']:x},0xff7068:l", 8)
    emitter.ins('move.w', f"#0x{rules['flow_initial_actor_state']:x},0xff7052:l", 8)
    emitter.ins('move.l', f"#0x{rules['flow_second_initial_position']:x},0xff70ae:l", 10)
    emitter.ins('move.w', f"#0x{rules['flow_second_initial_attributes']:x},0xff70b8:l", 8)
    emitter.ins('move.w', f"#0x{rules['flow_initial_actor_state']:x},0xff70a2:l", 8)
    emitter.ins('clr.w', '0xff70f0:l', 6)
    emitter.ins('clr.w', '0xff70f6:l', 6)
    emitter.ins('clr.w', '0xff70f8:l', 6)
    emitter.ins('moveq', '#0,%d4', 2)
    emitter.ins('lea.l', '0xea88:w,%a5', 4)
    emitter.ins('move.w', '0xff706a:l,%d4', 6)
    emitter.ins('mulu.w', '#0x3,%d4', 4)
    emitter.ins('adda.w', '%d4,%a5', 2)
    emitter.ins('move.b', '(%a5)+,0xff707b:l', 6)
    emitter.ins('move.b', '(%a5)+,0xff707d:l', 6)
    emitter.ins('move.b', '(%a5),0xff707f:l', 6)
    emitter.ins('moveq', '#0,%d4', 2)
    emitter.ins('lea.l', '0xea88:w,%a5', 4)
    emitter.ins('move.w', '0xff70ba:l,%d4', 6)
    emitter.ins('mulu.w', '#0x3,%d4', 4)
    emitter.ins('adda.w', '%d4,%a5', 2)
    emitter.ins('move.b', '(%a5)+,0xff70cb:l', 6)
    emitter.ins('move.b', '(%a5)+,0xff70cd:l', 6)
    emitter.ins('move.b', '(%a5),0xff70cf:l', 6)
    emitter.ins('move.l', '#0x40000000,0xc00004:l', 10)
    emitter.ins('lea.l', '0x6c3b4:l,%a0', 6)
    emitter.ins('lea.l', '0xc00000:l,%a6', 6)
    emitter.ins('move.w', '#0x2fff,%d0', 4)
    emitter.ins('move.l', '(%a0)+,(%a6)', 2)
    emitter.ins('dbra', '%d0,scene_pc_026eb0', 4)
    emitter.ins('move.l', '#0x40000003,0xc00004:l', 10)
    emitter.ins('lea.l', '0x89ddc:l,%a0', 6)
    emitter.ins('move.w', '#0x1f,%d0', 4)
    emitter.ins('move.l', '(%a0)+,(%a6)', 2)
    emitter.ins('dbra', '%d0,scene_pc_026eca', 4)
    emitter.ins('lea.l', '0x8a426:l,%a0', 6)
    emitter.ins('lea.l', '0xd300:w,%a1', 4)
    emitter.ins('move.w', f"#0x{rules['flow_initial_glyph_background']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['flow_initial_glyph_foreground']:x},%d1", 4)
    emitter.ins('move.w', '#0x9,%d3', 4)
    emitter.ins('jsr', 'scene_pc_00af1e:l', 6)
    emitter.ins('lea.l', '0xd300:w,%a0', 4)
    emitter.ins('move.w', '#0x4f,%d0', 4)
    emitter.ins('move.l', '(%a0)+,(%a6)', 2)
    emitter.ins('dbra', '%d0,scene_pc_026ef4', 4)
    emitter.ins('move.l', '#0x50000003,0xc00004:l', 10)
    emitter.ins('lea.l', '0x783b4:l,%a0', 6)
    emitter.ins('move.w', '#0x2f,%d0', 4)
    emitter.ins('move.l', '(%a0)+,(%a6)', 2)
    emitter.ins('dbra', '%d0,scene_pc_026f0e', 4)
    emitter.ins('move.l', '#0x42000003,0xc00004:l', 10)
    emitter.ins('move.w', '0xff706a:l,%d7', 6)
    emitter.ins('move.w', f"#0x{rules['flow_initial_glyph_background']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['flow_initial_glyph_foreground']:x},%d1", 4)
    emitter.ins('bsr.w', 'scene_pc_027d1c', 4)
    emitter.ins('move.w', '0xff70ba:l,%d7', 6)
    emitter.ins('move.w', f"#0x{rules['flow_initial_glyph_background']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['flow_initial_glyph_foreground']:x},%d1", 4)
    emitter.ins('bsr.w', 'scene_pc_027d1c', 4)
    emitter.ins('lea.l', '6518(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['flow_initial_glyph_background']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['flow_initial_glyph_foreground']:x},%d1", 4)
    emitter.ins('move.w', '#0x1,%d3', 4)
    emitter.ins('bsr.w', 'scene_pc_027d56', 4)
    emitter.ins('bsr.w', 'scene_pc_027d76', 4)
    emitter.ins('lea.l', '4386(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('lea.l', '0xfb00:w,%a1', 4)
    emitter.ins('move.w', '#0x1f,%d0', 4)
    emitter.ins('move.l', '(%a0)+,(%a1)+', 2)
    emitter.ins('dbra', '%d0,scene_pc_026f6a', 4)
    emitter.ins('move.w', '#0x1,0xf31e:w', 6)
    emitter.ins('lea.l', '0x78474:l,%a0', 6)
    emitter.ins('cmpi.w', f"#0x{rules['flow_initial_map_variant']:x},0xff70f2:l", 8)
    emitter.ins(rules['flow_initial_map_relation_false_branch'] + '.w', 'scene_pc_026f8e', 4)
    emitter.ins('lea.l', '0x78656:l,%a0', 6)
    emitter.ins('lea.l', '0xff6000:l,%a1', 6)
    emitter.ins('move.w', '#0x500,%d0', 4)
    emitter.ins('bsr.w', 'scene_pc_028012', 4)
    emitter.ins('move.l', '#0x60000003,0xc00004:l', 10)
    emitter.ins('lea.l', '0xff6000:l,%a0', 6)
    emitter.ins('move.w', '#0x4ff,%d0', 4)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('dbra', '%d0,scene_pc_026fb0', 4)
    emitter.ins('lea.l', '0x7883e:l,%a0', 6)
    emitter.ins('lea.l', '0xff6000:l,%a1', 6)
    emitter.ins('move.w', '#0x500,%d0', 4)
    emitter.ins('bsr.w', 'scene_pc_028012', 4)
    emitter.ins('move.l', '#0x70000003,0xc00004:l', 10)
    emitter.ins('lea.l', '0xff6000:l,%a0', 6)
    emitter.ins('move.w', '#0x4ff,%d0', 4)
    emitter.ins('move.w', '(%a0)+,(%a6)', 2)
    emitter.ins('dbra', '%d0,scene_pc_026fde', 4)
    emitter.ins('move.w', '#0x603,0xf694:w', 6)
    emitter.ins('move.w', '#0x604,0xf692:w', 6)
    emitter.ins('lea.l', '4398(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.l', '#0x60000028,%d0', 6)
    emitter.ins('move.w', '#0x3,%d1', 4)
    emitter.ins('move.w', '#0xea00,%d2', 4)
    emitter.ins('jsr', 'scene_pc_026bfa:l', 6)
    emitter.ins('jsr', 'scene_pc_00ad06:l', 6)
    emitter.ins('lea.l', '4450(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.l', '#0x60000028,%d0', 6)
    emitter.ins('move.w', '#0x5,%d1', 4)
    emitter.ins('move.w', '#0xeb80,%d2', 4)
    emitter.ins('jsr', 'scene_pc_026bfa:l', 6)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700a:l", 8)
    emitter.ins('beq.w', 'scene_pc_027058', 4)
    emitter.ins('move.w', f"#0x{rules['flow_loadout_dialog_position']:x},0xff700c:l", 8)
    emitter.ins('move.l', '#0x288be,0xff700e:l', 10)
    emitter.ins('move.w', '#0x1,0xff7014:l', 8)
    emitter.ins('move.w', '#0x2,0xff7016:l', 8)
    emitter.ins('jsr', '-724(%pc)', 4)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_027066', 2)
    emitter.ins('jsr', '-744(%pc)', 4)
    emitter.ins('bsr.w', 'scene_pc_027a84', 4)
    emitter.ins('clr.w', '0xff708a:l', 6)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700a:l", 8)
    emitter.ins('beq.w', 'scene_pc_027b58', 4)
    emitter.ins('lea.l', '0xff705c:l,%a0', 6)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('bsr.w', 'scene_pc_027dfc', 4)
    emitter.ins('tst.w', '0xff700c:l', 6)
    emitter.ins(rules['flow_loadout_pending_relation_true_branch'] + '.b', 'scene_pc_027060', 2)
    emitter.ins('lea.l', '4430(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '#0xed08,%d2', 4)
    emitter.ins('move.l', '#0x60000004,%d0', 6)
    emitter.ins('move.w', '#0x1,%d1', 4)
    emitter.ins('jsr', 'scene_pc_026bfa:l', 6)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('andi.w', f"#0x{rules['flow_preparation_confirm_mask']:x},%d0", 4)
    emitter.ins(rules['flow_loadout_equipment_confirm_relation_true_branch'] + '.b', 'scene_pc_027060', 2)
    emitter.ins('move.w', f"#0x{rules['flow_loadout_accept_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700a:l", 8)
    emitter.ins('beq.w', 'scene_pc_027152', 4)
    emitter.ins('bsr.w', 'scene_pc_027d76', 4)
    emitter.ins('move.w', f"#0x{rules['flow_loadout_dialog_position']:x},0xff700c:l", 8)
    emitter.ins('move.l', '#0x2890a,0xff700e:l', 10)
    emitter.ins('move.w', '#0x1,0xff7014:l', 8)
    emitter.ins('move.w', '#0x2,0xff7016:l', 8)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_027106', 2)
    emitter.ins('jsr', '-904(%pc)', 4)
    emitter.ins('bsr.w', 'scene_pc_027a84', 4)
    emitter.ins('lea.l', '0xff7092:l,%a0', 6)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('bsr.w', 'scene_pc_027d9c', 4)
    emitter.ins('tst.w', '0xff700c:l', 6)
    emitter.ins(rules['flow_loadout_pending_relation_true_branch'] + '.b', 'scene_pc_027100', 2)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('andi.w', f"#0x{rules['flow_preparation_confirm_mask']:x},%d0", 4)
    emitter.ins(rules['flow_loadout_option_confirm_relation_false_branch'] + '.b', 'scene_pc_027100', 2)
    emitter.ins('move.w', f"#0x{rules['flow_loadout_accept_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('lea.l', '0xff7092:l,%a0', 6)
    emitter.ins('tst.w', '(%a0)', 2)
    emitter.ins(rules['flow_loadout_auto_choice_relation_false_branch'] + '.w', 'scene_pc_027152', 4)
    emitter.ins('move.b', f"#0x{rules['flow_automatic_mode']:x},0xff700a:l", 8)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('lea.l', '0xff7050:l,%a0', 6)
    emitter.ins('bsr.w', 'scene_pc_027a3a', 4)
    emitter.ins('bsr.w', 'scene_pc_027d76', 4)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700b:l", 8)
    emitter.ins('beq.w', 'scene_pc_02719a', 4)
    emitter.ins('move.w', f"#0x{rules['flow_loadout_dialog_position']:x},0xff700c:l", 8)
    emitter.ins('move.l', '#0x288be,0xff700e:l', 10)
    emitter.ins('move.w', '#0x1,0xff7014:l', 8)
    emitter.ins('move.w', '#0x2,0xff7016:l', 8)
    emitter.ins('move.w', f"#0x{rules['flow_second_loadout_acknowledgement']:x},0xff70da:l", 8)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_0271a4', 2)
    emitter.ins('jsr', '-1062(%pc)', 4)
    emitter.ins('bsr.w', 'scene_pc_027a84', 4)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700b:l", 8)
    emitter.ins('beq.w', 'scene_pc_027b62', 4)
    emitter.ins('lea.l', '0xff70ac:l,%a0', 6)
    emitter.ins('bsr.w', 'scene_pc_027a10', 4)
    emitter.ins('bsr.w', 'scene_pc_027e06', 4)
    emitter.ins('tst.w', '0xff700c:l', 6)
    emitter.ins(rules['flow_loadout_pending_relation_true_branch'] + '.b', 'scene_pc_02719e', 2)
    emitter.ins('lea.l', '4140(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', '#0xed44,%d2', 4)
    emitter.ins('move.l', '#0x60000004,%d0', 6)
    emitter.ins('move.w', '#0x1,%d1', 4)
    emitter.ins('jsr', 'scene_pc_026bfa:l', 6)
    emitter.ins('bsr.w', 'scene_pc_027a10', 4)
    emitter.ins('andi.w', f"#0x{rules['flow_preparation_confirm_mask']:x},%d0", 4)
    emitter.ins(rules['flow_loadout_equipment_confirm_relation_true_branch'] + '.b', 'scene_pc_02719e', 2)
    emitter.ins('move.w', f"#0x{rules['flow_loadout_accept_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700b:l", 8)
    emitter.ins('beq.w', 'scene_pc_02728a', 4)
    emitter.ins('bsr.w', 'scene_pc_027d76', 4)
    emitter.ins('move.w', f"#0x{rules['flow_loadout_dialog_position']:x},0xff700c:l", 8)
    emitter.ins('move.l', '#0x2890a,0xff700e:l', 10)
    emitter.ins('move.w', '#0x1,0xff7014:l', 8)
    emitter.ins('move.w', '#0x2,0xff7016:l', 8)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_02723e', 2)
    emitter.ins('jsr', '-1216(%pc)', 4)
    emitter.ins('bsr.w', 'scene_pc_027a84', 4)
    emitter.ins('lea.l', '0xff70e2:l,%a0', 6)
    emitter.ins('bsr.w', 'scene_pc_027a10', 4)
    emitter.ins('bsr.w', 'scene_pc_027d9c', 4)
    emitter.ins('tst.w', '0xff700c:l', 6)
    emitter.ins(rules['flow_loadout_pending_relation_true_branch'] + '.b', 'scene_pc_027238', 2)
    emitter.ins('bsr.w', 'scene_pc_027a10', 4)
    emitter.ins('andi.w', f"#0x{rules['flow_preparation_confirm_mask']:x},%d0", 4)
    emitter.ins(rules['flow_loadout_option_confirm_relation_false_branch'] + '.b', 'scene_pc_027238', 2)
    emitter.ins('move.w', f"#0x{rules['flow_loadout_accept_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('lea.l', '0xff70e2:l,%a0', 6)
    emitter.ins('tst.w', '(%a0)', 2)
    emitter.ins(rules['flow_loadout_auto_choice_relation_false_branch'] + '.w', 'scene_pc_02728a', 4)
    emitter.ins('move.b', f"#0x{rules['flow_automatic_mode']:x},0xff700b:l", 8)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('lea.l', '0xff70a0:l,%a0', 6)
    emitter.ins('bsr.w', 'scene_pc_027a3a', 4)
    emitter.ins('bsr.w', 'scene_pc_027d76', 4)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('andi.w', f"#0x{rules['flow_status_random_mask']:x},%d0", 4)
    emitter.ins('cmpi.w', f"#0x{rules['flow_status_wrap_bound']:x},%d0", 4)
    emitter.ins(rules['flow_status_wrap_relation_false_branch'] + '.b', 'scene_pc_0272ae', 2)
    emitter.ins('clr.w', '%d0', 2)
    emitter.ins('jsr', '3960(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['flow_status_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('clr.w', '0xff7052:l', 6)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_0272ce', 2)
    emitter.ins('jsr', '-1360(%pc)', 4)
    emitter.ins('bsr.w', 'scene_pc_027a84', 4)
    emitter.ins('tst.w', '0xff700c:l', 6)
    emitter.ins(rules['flow_status_pending_relation_true_branch'] + '.b', 'scene_pc_0272c8', 2)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('andi.w', f"#0x{rules['flow_preparation_confirm_mask']:x},%d0", 4)
    emitter.ins(rules['flow_status_confirm_relation_false_branch'] + '.b', 'scene_pc_0272c8', 2)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('bsr.w', 'scene_pc_027d76', 4)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('andi.w', f"#0x{rules['flow_status_random_mask']:x},%d0", 4)
    emitter.ins('cmpi.w', f"#0x{rules['flow_status_wrap_bound']:x},%d0", 4)
    emitter.ins(rules['flow_status_wrap_relation_false_branch'] + '.b', 'scene_pc_027308', 2)
    emitter.ins('clr.w', '%d0', 2)
    emitter.ins('addq.w', f"#0x{rules['flow_second_status_bias']:x},%d0", 2)
    emitter.ins('jsr', '3868(%pc)', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['flow_status_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('clr.w', '0xff70a2:l', 6)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_02732a', 2)
    emitter.ins('bsr.w', 'scene_pc_027a84', 4)
    emitter.ins('tst.w', '0xff700c:l', 6)
    emitter.ins(rules['flow_status_pending_relation_true_branch'] + '.b', 'scene_pc_027324', 2)
    emitter.ins('bsr.w', 'scene_pc_027a10', 4)
    emitter.ins('andi.w', f"#0x{rules['flow_preparation_confirm_mask']:x},%d0", 4)
    emitter.ins(rules['flow_status_confirm_relation_false_branch'] + '.b', 'scene_pc_027324', 2)
    emitter.ins('move.w', f"#0x{rules['flow_combat_begin_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('bsr.w', 'scene_pc_027d76', 4)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_027362', 2)
    emitter.ins('lea.l', '0xff7050:l,%a0', 6)
    emitter.ins('lea.l', '0xff70a0:l,%a1', 6)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('move.w', '%d0,0xff7050:l', 6)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700a:l", 8)
    emitter.ins(rules['flow_first_ai_relation_false_branch'] + '.b', 'scene_pc_027392', 2)
    emitter.ins('bsr.w', 'scene_pc_02a29a', 4)
    emitter.ins('move.w', '%d0,0xff7050:l', 6)
    emitter.ins('bsr.w', 'scene_pc_028b9a', 4)
    emitter.ins('lea.l', '0xff70a0:l,%a0', 6)
    emitter.ins('lea.l', '0xff7050:l,%a1', 6)
    emitter.ins('bsr.w', 'scene_pc_027a10', 4)
    emitter.ins('move.w', '%d0,0xff70a0:l', 6)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700b:l", 8)
    emitter.ins(rules['flow_second_ai_relation_false_branch'] + '.b', 'scene_pc_0273c0', 2)
    emitter.ins('bsr.w', 'scene_pc_02a29a', 4)
    emitter.ins('move.w', '%d0,0xff70a0:l', 6)
    emitter.ins('bsr.w', 'scene_pc_028b9a', 4)
    emitter.ins('bsr.w', 'scene_pc_027506', 4)
    emitter.ins('clr.w', '0xff7018:l', 6)
    emitter.ins('tst.w', '0xff706c:l', 6)
    emitter.ins(rules['flow_first_terminal_relation_true_branch'] + '.w', 'scene_pc_027990', 4)
    emitter.ins('move.w', '#0x8000,0xff7018:l', 8)
    emitter.ins('tst.w', '0xff70bc:l', 6)
    emitter.ins(rules['flow_second_terminal_relation_true_branch'] + '.w', 'scene_pc_027990', 4)
    emitter.ins('move.w', '0xff7052:l,%d1', 6)
    emitter.ins('or.w', '0xff70a2:l,%d1', 6)
    emitter.ins('andi.w', f"#0x{rules['flow_pending_action_mask']:x},%d1", 4)
    emitter.ins('bne.w', 'scene_pc_02735c', 4)
    emitter.ins('clr.w', '0xff7018:l', 6)
    emitter.ins('move.w', '0xff7050:l,%d0', 6)
    emitter.ins('andi.w', f"#0x{rules['flow_action_request_mask']:x},%d0", 4)
    emitter.ins('bne.b', 'scene_pc_027426', 2)
    emitter.ins('move.w', '#0x8000,0xff7018:l', 8)
    emitter.ins('move.w', '0xff70a0:l,%d0', 6)
    emitter.ins('andi.w', f"#0x{rules['flow_action_request_mask']:x},%d0", 4)
    emitter.ins('beq.w', 'scene_pc_02735c', 4)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('clr.w', '0xd100:w', 4)
    emitter.ins('tst.w', '0xff7018:l', 6)
    emitter.ins('bmi.b', 'scene_pc_027454', 2)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700a:l", 8)
    emitter.ins(rules['flow_manual_mode_relation_true_branch'] + '.b', 'scene_pc_027472', 2)
    emitter.ins('move.w', '0xff7050:l,%d0', 6)
    emitter.ins('andi.w', '#0x3,%d0', 4)
    emitter.ins('move.b', '%d0,0xff7019:l', 6)
    emitter.ins('bra.w', 'scene_pc_027534', 4)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700b:l", 8)
    emitter.ins(rules['flow_manual_mode_relation_true_branch'] + '.b', 'scene_pc_027482', 2)
    emitter.ins('move.w', '0xff70a0:l,%d0', 6)
    emitter.ins('andi.w', '#0x3,%d0', 4)
    emitter.ins('move.b', '%d0,0xff7019:l', 6)
    emitter.ins('bra.w', 'scene_pc_027534', 4)
    emitter.ins('move.w', '0xff706a:l,%d1', 6)
    emitter.ins('cmp.w', '0xff7070:l,%d1', 6)
    emitter.ins(rules['flow_same_officer_dialog_relation_true_branch'] + '.b', 'scene_pc_027492', 2)
    emitter.ins('bra.b', 'scene_pc_0274a6', 2)
    emitter.ins('move.w', '0xff70ba:l,%d1', 6)
    emitter.ins('cmp.w', '0xff70c0:l,%d1', 6)
    emitter.ins(rules['flow_same_officer_dialog_relation_true_branch'] + '.b', 'scene_pc_027492', 2)
    emitter.ins('bra.b', 'scene_pc_0274a6', 2)
    emitter.ins('move.w', f"#0x{rules['flow_same_officer_dialog_position']:x},0xff700c:l", 8)
    emitter.ins('move.l', '#0x28924,0xff700e:l', 10)
    emitter.ins('bra.b', 'scene_pc_0274b8', 2)
    emitter.ins('move.w', f"#0x{rules['flow_different_officer_dialog_position']:x},0xff700c:l", 8)
    emitter.ins('move.l', '#0x288ea,0xff700e:l', 10)
    emitter.ins('move.w', f"#0x{rules['flow_manual_dialog_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_0274cc', 2)
    emitter.ins('bsr.w', 'scene_pc_027a84', 4)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('tst.w', '0xff7018:l', 6)
    emitter.ins('bpl.b', 'scene_pc_0274e6', 2)
    emitter.ins('bsr.w', 'scene_pc_027a10', 4)
    emitter.ins('move.w', '%d0,-(%a7)', 2)
    emitter.ins('bsr.w', 'scene_pc_027ed2', 4)
    emitter.ins('move.w', '(%a7)+,%d0', 2)
    emitter.ins('tst.w', '0xff700c:l', 6)
    emitter.ins(rules['flow_manual_pending_relation_true_branch'] + '.b', 'scene_pc_0274c6', 2)
    emitter.ins('btst.l', f"#0x{rules['flow_manual_confirm_bit']:x},%d0", 4)
    emitter.ins('bne.b', 'scene_pc_027534', 2)
    emitter.ins('btst.l', f"#0x{rules['flow_manual_cancel_bit']:x},%d0", 4)
    emitter.ins('beq.b', 'scene_pc_0274c6', 2)
    emitter.ins('bra.w', 'scene_pc_027350', 4)
    emitter.segment(161076, 161142)
    emitter.ins('move.w', f"#0x{rules['flow_loadout_accept_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('bsr.w', 'scene_pc_027d76', 4)
    emitter.ins('lea.l', '0xff7050:l,%a0', 6)
    emitter.ins('lea.l', '0xff70a0:l,%a1', 6)
    emitter.ins('tst.w', '0xff7018:l', 6)
    emitter.ins('bpl.b', 'scene_pc_027566', 2)
    emitter.ins('lea.l', '0xff70a0:l,%a0', 6)
    emitter.ins('lea.l', '0xff7050:l,%a1', 6)
    emitter.ins('move.w', '0xff7018:l,%d0', 6)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('jsr', '6(%pc, %d0.w)', 4)
    emitter.ins('bra.w', 'scene_pc_027350', 4)
    emitter.segment(162192, 162278)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_027996', 2)
    emitter.ins('bsr.w', 'scene_pc_027506', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_0279a6', 2)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('move.w', f"#0x{rules['flow_first_terminal_message']:x},%d0", 4)
    emitter.ins('tst.w', '0xff7018:l', 6)
    emitter.ins('bpl.b', 'scene_pc_0279c0', 2)
    emitter.ins('move.w', f"#0x{rules['flow_second_terminal_message']:x},%d0", 4)
    emitter.ins('bsr.w', 'scene_pc_028228', 4)
    emitter.ins('bsr.w', 'scene_pc_02777a', 4)
    emitter.ins('bsr.w', 'scene_pc_027d76', 4)
    emitter.ins('move.w', f"#0x{rules['flow_terminal_followup_message']:x},%d0", 4)
    emitter.ins('tst.w', '0xff7018:l', 6)
    emitter.ins('bpl.b', 'scene_pc_0279da', 2)
    emitter.ins('addq.w', f"#0x{rules['flow_second_terminal_followup_step']:x},%d0", 2)
    emitter.ins('bsr.w', 'scene_pc_028228', 4)
    emitter.ins('bsr.w', 'scene_pc_0277b8', 4)
    emitter.ins('bra.w', 'scene_pc_026d46', 4)
    emitter.segment(162648, 162710)
    emitter.ins('lea.l', '0xff7050:l,%a0', 6)
    emitter.ins('bra.w', 'scene_pc_027b68', 4)
    emitter.ins('lea.l', '0xff70a0:l,%a0', 6)
    emitter.ins('move.w', '0x1e(%a0),%d0', 4)
    emitter.ins('lea.l', '40(%pc),%a2', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('bsr.w', 'scene_pc_028f90', 4)
    emitter.ins('asl.w', '#0x1,%d1', 2)
    emitter.ins('movea.l', '40(%pc, %d1.w),%a3', 4)
    emitter.ins('jsr', '(%a3)', 2)
    emitter.ins('tst.w', '%d6', 2)
    emitter.ins('bne.w', 'scene_pc_027bba', 4)
    emitter.ins('cmpa.l', '#0xff7050,%a0', 6)
    emitter.ins('bne.w', 'scene_pc_027b92', 4)
    emitter.ins('bra.w', 'scene_pc_027060', 4)
    emitter.ins('bra.w', 'scene_pc_02728a', 4)
    emitter.segment(162746, 162764)
    emitter.ins('cmpa.l', '#0xff7050,%a0', 6)
    emitter.ins('bne.w', 'scene_pc_027bc8', 4)
    emitter.ins('bra.w', 'scene_pc_027152', 4)
    emitter.ins('bra.w', 'scene_pc_02728a', 4)

def lower_advance_duel_entry_palette(emitter, rules):
    emitter.segment(159110, 159156)
    emitter.ins('cmpi.w', f"#0x{rules['flow_entry_palette_bound']:x},0xff70f8:l", 8)
    emitter.ins(rules['flow_entry_palette_relation_true_branch'] + '.w', 'scene_pc_026db2', 4)
    emitter.ins('move.w', f"#0x{rules['flow_entry_palette_complement']:x},%d0", 4)
    emitter.ins('sub.w', '0xff70f8:l,%d0', 6)
    emitter.ins('move.w', f"#0x{rules['flow_entry_palette_count']:x},%d1", 4)
    emitter.ins('lea.l', '4830(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('jsr', 'scene_pc_00dea6:l', 6)
    emitter.ins('addq.w', f"#0x{rules['flow_entry_palette_step']:x},0xff70f8:l", 6)
    emitter.ins('rts', '', 2)

def lower_show_active_duel_turn_label(emitter, rules):
    emitter.segment(161030, 161076)
    emitter.ins('lea.l', '3224(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['flow_first_label_position']:x},%d2", 4)
    emitter.ins('move.w', '0xff7008:l,%d0', 6)
    emitter.ins('andi.w', f"#0x{rules['flow_label_tick_mask']:x},%d0", 4)
    emitter.ins('beq.b', 'scene_pc_027526', 2)
    emitter.ins('lea.l', '3224(%pc),%a0', 4)
    emitter.ins('nop', '', 2)
    emitter.ins('move.w', f"#0x{rules['flow_second_label_position']:x},%d2", 4)
    emitter.ins('move.l', '#0x60000004,%d0', 6)
    emitter.ins('move.w', '#0x1,%d1', 4)
    emitter.ins('bra.w', 'scene_pc_026bfa', 4)

def lower_wait_active_duel_action(emitter, rules):
    emitter.segment(161658, 161810)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_027784', 2)
    emitter.ins('subq.w', f"#0x{rules['flow_active_wait_timer_step']:x},0xff70fa:l", 6)
    emitter.ins('bsr.w', 'scene_pc_027a84', 4)
    emitter.ins('tst.w', '0xff700c:l', 6)
    emitter.ins(rules['flow_active_wait_pending_relation_true_branch'] + '.b', 'scene_pc_02777e', 2)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('tst.w', '0xff7018:l', 6)
    emitter.ins('bpl.b', 'scene_pc_0277ac', 2)
    emitter.ins('bsr.w', 'scene_pc_027a10', 4)
    emitter.ins('andi.w', f"#0x{rules['flow_active_wait_accept_mask']:x},%d0", 4)
    emitter.ins(rules['flow_active_wait_confirm_relation_false_branch'] + '.b', 'scene_pc_02777e', 2)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('rts', '', 2)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700a:l", 8)
    emitter.ins('beq.w', 'scene_pc_02777a', 4)
    emitter.ins('cmpi.b', f"#0x{rules['flow_automatic_mode']:x},0xff700b:l", 8)
    emitter.ins('beq.w', 'scene_pc_02777a', 4)
    emitter.ins('move.w', '#0x2500,%sr', 4)
    emitter.ins('move.w', '#0x700,0xf612:w', 6)
    emitter.ins('tst.b', '0xf612:w', 4)
    emitter.ins('bne.b', 'scene_pc_0277da', 2)
    emitter.ins('subq.w', f"#0x{rules['flow_either_wait_timer_step']:x},0xff70fa:l", 6)
    emitter.ins('bsr.w', 'scene_pc_027a84', 4)
    emitter.ins('tst.w', '0xff700c:l', 6)
    emitter.ins(rules['flow_either_wait_pending_relation_true_branch'] + '.b', 'scene_pc_0277d4', 2)
    emitter.ins('bsr.w', 'scene_pc_0279e6', 4)
    emitter.ins('move.w', '%d0,%d1', 2)
    emitter.ins('movem.l', '%d1,-(%a7)', 4)
    emitter.ins('bsr.w', 'scene_pc_027a10', 4)
    emitter.ins('movem.l', '(%a7)+,%d1', 4)
    emitter.ins('or.w', '%d1,%d0', 2)
    emitter.ins('andi.w', f"#0x{rules['flow_either_wait_accept_mask']:x},%d0", 4)
    emitter.ins(rules['flow_either_wait_confirm_relation_false_branch'] + '.b', 'scene_pc_0277d4', 2)
    emitter.ins('move.w', '#0x2700,%sr', 4)
    emitter.ins('rts', '', 2)

def lower_configure_duel_weapon_motion(emitter, rules):
    emitter.segment(162362, 162430)
    emitter.ins('move.w', '0x1e(%a0),%d0', 4)
    emitter.ins('move.w', '0xc(%a0),%d1', 4)
    emitter.ins('asl.w', '#0x1,%d1', 2)
    emitter.ins('sub.w', '56(%pc, %d1.w),%d0', 4)
    emitter.ins(rules['flow_motion_borrow_relation_false_branch'] + '.b', 'scene_pc_027a50', 2)
    emitter.ins('clr.w', '%d0', 2)
    emitter.ins('bra.w', 'scene_pc_027a5a', 4)
    emitter.ins('cmpi.w', f"#0x{rules['flow_motion_bound']:x},%d0", 4)
    emitter.ins(rules['flow_motion_cap_relation_false_branch'] + '.b', 'scene_pc_027a5a', 2)
    emitter.ins('move.w', f"#0x{rules['flow_motion_bound']:x},%d0", 4)
    emitter.ins('move.w', f"#0x{rules['flow_motion_bound']:x},%d1", 4)
    emitter.ins('sub.w', '%d0,%d1', 2)
    emitter.ins('mulu.w', f"#0x{rules['flow_motion_scale']:x},%d0", 4)
    emitter.ins('addi.l', f"#0x{rules['flow_motion_bias']:x},%d0", 6)
    emitter.ins('move.l', '%d0,0x12(%a0)', 4)
    emitter.ins('andi.l', '#0xffff,%d1', 6)
    emitter.ins('divu.w', f"#0x{rules['flow_motion_divisor']:x},%d1", 4)
    emitter.ins('move.w', '%d1,0x16(%a0)', 4)
    emitter.ins('rts', '', 2)

def lower_refresh_duel_actors(emitter, rules):
    emitter.segment(162436, 162494)
    emitter.ins('movem.l', '%a0-%a1,-(%a7)', 4)
    emitter.ins('move.w', '#0x0,0xff7050:l', 8)
    emitter.ins('lea.l', '0xff7050:l,%a0', 6)
    emitter.ins('lea.l', '0xff70a0:l,%a1', 6)
    emitter.ins('bsr.w', 'scene_pc_028e6c', 4)
    emitter.ins('move.w', '#0x0,0xff70a0:l', 8)
    emitter.ins('lea.l', '0xff70a0:l,%a0', 6)
    emitter.ins('lea.l', '0xff7050:l,%a1', 6)
    emitter.ins('bsr.w', 'scene_pc_028e6c', 4)
    emitter.ins('movem.l', '(%a7)+,%a0-%a1', 4)
    emitter.ins('rts', '', 2)

def lower_choose_duel_status_text(emitter, rules):
    emitter.segment(164392, 164416)
    emitter.ins('lea.l', '22(%pc),%a2', 4)
    emitter.ins('asl.w', '#0x2,%d0', 2)
    emitter.ins('move.l', '(%a2, %d0.w),0xff700e:l', 8)
    emitter.ins('move.w', f"#0x{rules['flow_status_text_command']:x},0xff700c:l", 8)
    emitter.ins('rts', '', 2)

LOWERERS = {
    'run_duel_scene': lower_run_duel_scene,
    'advance_duel_entry_palette': lower_advance_duel_entry_palette,
    'show_active_duel_turn_label': lower_show_active_duel_turn_label,
    'wait_active_duel_action': lower_wait_active_duel_action,
    'configure_duel_weapon_motion': lower_configure_duel_weapon_motion,
    'refresh_duel_actors': lower_refresh_duel_actors,
    'choose_duel_status_text': lower_choose_duel_status_text,
}



# Complete actual Duel fields role topology125; fixed real current business paths, no source fallback.
_ORIGINAL_NATIVE_ROLE_SPECS125 = ROLE_SPECS
_CURRENT_DUEL_ROLE_BINDINGS125 = {'flow_entry_palette_bound': {'function': 'advance_duel_entry_palette_fields', 'paths': (('body', 2, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_entry_palette_complement': {'function': 'advance_duel_entry_palette_fields', 'paths': (('body', 4, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_entry_palette_count': {'function': 'advance_duel_entry_palette_fields', 'paths': (('body', 6, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_entry_palette_step': {'function': 'advance_duel_entry_palette_fields', 'paths': (('body', 9, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_fade_bound': {'function': 'finish_duel_scene_fields', 'paths': (('body', 2, 'body', 3, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_fade_count': {'function': 'finish_duel_scene_fields', 'paths': (('body', 2, 'body', 6, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_fade_step': {'function': 'finish_duel_scene_fields', 'paths': (('body', 2, 'body', 10, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_initial_display_mask': {'function': 'initialize_duel_scene_fields', 'paths': (('body', 3, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'flow_initial_map_variant': {'function': 'initialize_duel_scene_fields', 'paths': (('body', 35, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_loadout_dialog_position': {'function': 'prepare_duel_loadout_fields', 'paths': (('body', 8, 'body', 0, 'value', 'args', 3), ('body', 13, 'body', 1, 'value', 'args', 3)), 'coupled_uses': ()}, 'flow_second_loadout_acknowledgement': {'function': 'prepare_duel_loadout_fields', 'paths': (('body', 8, 'body', 1, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_status_random_mask': {'function': 'prepare_duel_readiness_fields', 'paths': (('body', 0, 'body', 2, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'flow_status_wrap_bound': {'function': 'prepare_duel_readiness_fields', 'paths': (('body', 0, 'body', 3, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_second_status_bias': {'function': 'prepare_duel_readiness_fields', 'paths': (('body', 0, 'body', 5, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_status_sound': {'function': 'prepare_duel_readiness_fields', 'paths': (('body', 0, 'body', 7, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_combat_begin_sound': {'function': 'prepare_duel_readiness_fields', 'paths': (('body', 1, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_pending_action_mask': {'function': 'continue_after_first_duel_actor_fields', 'paths': (('body', 11, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'flow_manual_dialog_sound': {'function': 'choose_duel_turn_action_fields', 'paths': (('body', 12, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_manual_confirm_bit': {'function': 'continue_manual_duel_action_fields', 'paths': (('body', 2, 'body', 15, 'value', 'args', 2),), 'coupled_uses': ()}, 'flow_manual_cancel_bit': {'function': 'continue_manual_duel_action_fields', 'paths': (('body', 2, 'body', 17, 'value', 'args', 2),), 'coupled_uses': ()}, 'flow_first_terminal_message': {'function': 'show_terminal_duel_result_fields', 'paths': (('body', 5, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_second_terminal_message': {'function': 'show_terminal_duel_result_fields', 'paths': (('body', 7, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_terminal_followup_message': {'function': 'show_terminal_duel_result_fields', 'paths': (('body', 11, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_second_terminal_followup_step': {'function': 'show_terminal_duel_result_fields', 'paths': (('body', 13, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_label_tick_mask': {'function': 'show_active_duel_turn_label_fields', 'paths': (('body', 4, 'value', 'args', 3, 'right'),), 'coupled_uses': ()}, 'flow_first_label_position': {'function': 'show_active_duel_turn_label_fields', 'paths': (('body', 2, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_second_label_position': {'function': 'show_active_duel_turn_label_fields', 'paths': (('body', 5, 'body', 1, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_active_wait_timer_step': {'function': '_wait_duel_action_fields', 'paths': (('body', 3, 'body', 3, 'value', 'args', 3),), 'coupled_uses': (), 'physical_pcs': (161674, 161760)}, 'flow_active_wait_accept_mask': {'function': '_wait_duel_action_fields', 'paths': (('body', 3, 'body', 10, 'value', 'args', 3, 'right'),), 'coupled_uses': (), 'physical_pcs': (161708, 161798)}, 'flow_motion_divisor': {'function': 'configure_duel_weapon_motion_fields', 'paths': (('body', 17, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_status_text_command': {'function': 'choose_duel_status_text_fields', 'paths': (('body', 7, 'value', 'args', 3),), 'coupled_uses': ()}, 'flow_preparation_confirm_mask': {'function': 'prepare_duel_loadout_fields', 'paths': (('body', 12, 'body', 13, 'value', 'args', 3, 'right'), ('body', 13, 'body', 3, 'body', 9, 'value', 'args', 3, 'right')), 'coupled_uses': (('prepare_duel_readiness_fields', ('body', 0, 'body', 11, 'body', 6, 'value', 'args', 3, 'right')),)}, 'flow_loadout_accept_sound': {'function': 'prepare_duel_loadout_fields', 'paths': (('body', 12, 'body', 15, 'value', 'args', 3), ('body', 13, 'body', 3, 'body', 11, 'value', 'args', 3)), 'coupled_uses': (('perform_selected_duel_action_result_fields', ('body', 1, 'value', 'args', 3)),)}, 'flow_automatic_mode': {'function': 'prepare_duel_loadout_fields', 'paths': (('body', 7, 'value', 'args', 3), ('body', 12, 'body', 4, 'value', 'args', 3), ('body', 12, 'body', 17, 'value', 'args', 3), ('body', 13, 'body', 3, 'body', 15, 'body', 0, 'value', 'args', 3)), 'coupled_uses': (('_duel_scene_actor_fields', ('body', 5, 'value', 'args', 3)), ('choose_duel_turn_action_fields', ('body', 6, 'value', 'args', 3)), ('wait_either_duel_action_fields', ('body', 1, 'value', 'args', 3)), ('wait_either_duel_action_fields', ('body', 3, 'value', 'args', 3)))}, 'flow_first_initial_position': {'function': 'initialize_duel_scene_fields', 'paths': (('body', 8, 'iter', 'elts', 0, 'elts', 1),), 'coupled_uses': ()}, 'flow_first_initial_attributes': {'function': 'initialize_duel_scene_fields', 'paths': (('body', 8, 'iter', 'elts', 1, 'elts', 1),), 'coupled_uses': ()}, 'flow_second_initial_position': {'function': 'initialize_duel_scene_fields', 'paths': (('body', 8, 'iter', 'elts', 3, 'elts', 1),), 'coupled_uses': ()}, 'flow_second_initial_attributes': {'function': 'initialize_duel_scene_fields', 'paths': (('body', 8, 'iter', 'elts', 4, 'elts', 1),), 'coupled_uses': ()}, 'flow_initial_actor_state': {'function': 'initialize_duel_scene_fields', 'paths': (('body', 8, 'iter', 'elts', 2, 'elts', 1), ('body', 8, 'iter', 'elts', 5, 'elts', 1)), 'coupled_uses': ()}, 'flow_initial_glyph_background': {'function': 'initialize_duel_scene_fields', 'paths': (('body', 17, 'value', 'args', 3), ('body', 25, 'body', 1, 'value', 'args', 3), ('body', 27, 'value', 'args', 3)), 'coupled_uses': ()}, 'flow_initial_glyph_foreground': {'function': 'initialize_duel_scene_fields', 'paths': (('body', 18, 'value', 'args', 3), ('body', 25, 'body', 2, 'value', 'args', 3), ('body', 28, 'value', 'args', 3)), 'coupled_uses': ()}, 'flow_action_request_mask': {'function': 'continue_after_first_duel_actor_fields', 'paths': (('body', 15, 'value', 'args', 3, 'right'), ('body', 16, 'body', 2, 'value', 'args', 3, 'right')), 'coupled_uses': ()}, 'flow_same_officer_dialog_position': {'function': 'choose_duel_turn_action_fields', 'paths': (('body', 11, 'value', 'args', 3, 'body'),), 'coupled_uses': ()}, 'flow_different_officer_dialog_position': {'function': 'choose_duel_turn_action_fields', 'paths': (('body', 11, 'value', 'args', 3, 'orelse'),), 'coupled_uses': ()}, 'flow_motion_bound': {'function': 'configure_duel_weapon_motion_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'flow_motion_scale': {'function': 'configure_duel_weapon_motion_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'flow_motion_bias': {'function': 'configure_duel_weapon_motion_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'flow_entry_palette_relation': {'function': 'advance_duel_entry_palette_fields', 'paths': (('body', 3, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_fade_relation': {'function': 'finish_duel_scene_fields', 'paths': (('body', 2, 'body', 4, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_initial_map_relation': {'function': 'initialize_duel_scene_fields', 'paths': (('body', 36, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_status_wrap_relation': {'function': 'prepare_duel_readiness_fields', 'paths': (('body', 0, 'body', 4, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_status_pending_relation': {'function': 'prepare_duel_readiness_fields', 'paths': (('body', 0, 'body', 11, 'body', 4, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_status_confirm_relation': {'function': 'prepare_duel_readiness_fields', 'paths': (('body', 0, 'body', 11, 'body', 7, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_first_ai_relation': {'function': '_duel_scene_actor_fields', 'paths': (('body', 6, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation', 'physical_pcs': (160646, 160692)}, 'flow_first_terminal_relation': {'function': 'continue_after_first_duel_actor_fields', 'paths': (('body', 5, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_second_terminal_relation': {'function': 'continue_after_first_duel_actor_fields', 'paths': (('body', 8, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_manual_mode_relation': {'function': 'choose_duel_turn_action_fields', 'paths': (('body', 7, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_inverse_relation'}, 'flow_manual_pending_relation': {'function': 'continue_manual_duel_action_fields', 'paths': (('body', 2, 'body', 14, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_active_wait_pending_relation': {'function': '_wait_duel_action_fields', 'paths': (('body', 3, 'body', 7, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation', 'physical_pcs': (161690, 161776)}, 'flow_active_wait_confirm_relation': {'function': '_wait_duel_action_fields', 'paths': (('body', 3, 'body', 11, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation', 'physical_pcs': (161712, 161802)}, 'flow_motion_borrow_relation': {'function': 'configure_duel_weapon_motion_fields', 'paths': (('body', 9, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_motion_cap_relation': {'function': 'configure_duel_weapon_motion_fields', 'paths': (('body', 9, 'orelse', 1, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_loadout_pending_relation': {'function': 'prepare_duel_loadout_fields', 'paths': (('body', 12, 'body', 10, 'test'), ('body', 13, 'body', 3, 'body', 7, 'test')), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_loadout_equipment_confirm_relation': {'function': 'prepare_duel_loadout_fields', 'paths': (('body', 12, 'body', 14, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_loadout_option_confirm_relation': {'function': 'prepare_duel_loadout_fields', 'paths': (('body', 13, 'body', 3, 'body', 10, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_inverse_relation'}, 'flow_loadout_auto_choice_relation': {'function': 'prepare_duel_loadout_fields', 'paths': (('body', 13, 'body', 3, 'body', 15, 'test'),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}, 'flow_same_officer_dialog_relation': {'function': 'choose_duel_turn_action_fields', 'paths': (('body', 10, 'value', 'args', 0),), 'coupled_uses': (), 'kind': 'frame_ccr_relation'}}
_CURRENT_SHARED_ROLE_ALIASES125 = {'flow_second_ai_relation': 'flow_first_ai_relation', 'flow_either_wait_timer_step': 'flow_active_wait_timer_step', 'flow_either_wait_accept_mask': 'flow_active_wait_accept_mask', 'flow_either_wait_pending_relation': 'flow_active_wait_pending_relation', 'flow_either_wait_confirm_relation': 'flow_active_wait_confirm_relation'}
ROLE_SPECS = tuple(MenuRole(role.name, _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('function', role.function), _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('paths', role.paths), _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('kind', role.kind), role.default, _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('physical_pcs', role.physical_pcs), coupled_uses=_CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('coupled_uses', role.coupled_uses)) for role in ROLE_SPECS if role.name not in _CURRENT_SHARED_ROLE_ALIASES125)

def owner_rules(values):
    """Validate all actual role values and give every owner its real rules.

    No rule is read by numeric value or falls back to a canonical literal.
    Refresh has no mutable policy: its complete save/clear/render/restore is
    still lowered, but RAM layout and reset semantics are not fabricated slots.
    """
    values = dict(values)
    for _alias, _authority in _CURRENT_SHARED_ROLE_ALIASES125.items():
        if _authority not in values:
            raise CompileError('actual shared current source role authority required')
        values[_alias] = values[_authority]
    checked = {}
    limits = {'word': (0, 65535), 'byte': (0, 255), 'long': (0, 4294967295), 'nonzero_word': (1, 65535), 'quick': (1, 8)}
    for role in _ORIGINAL_NATIVE_ROLE_SPECS125:
        if role.name not in values:
            raise CompileError('all complete duel lifecycle source roles required')
        value = values[role.name]
        if role.kind == 'unsigned_relation':
            if type(value) is not str or value not in _TRUE_BRANCH:
                raise CompileError(role.name + ': supported unsigned relation required')
        else:
            low, high = limits[role.kind]
            if type(value) is not int or not low <= value <= high:
                raise CompileError(role.name + ': strict bounded source integer required')
            if _CONSTRAINTS.get(role.name) == 'bit_index' and value > 31:
                raise CompileError(role.name + ': actual LONG bit index must be 0..31')
        checked[role.name] = value
    owners = {}
    for owner, names in _OWNER_ROLES.items():
        rules = {name: checked[name] for name in names}
        for role in _ORIGINAL_NATIVE_ROLE_SPECS125:
            if role.name in rules and role.kind == 'unsigned_relation':
                rules[role.name + '_true_branch'] = _TRUE_BRANCH[rules[role.name]]
                rules[role.name + '_false_branch'] = _FALSE_BRANCH[rules[role.name]]
        owners[owner] = rules
    return owners
