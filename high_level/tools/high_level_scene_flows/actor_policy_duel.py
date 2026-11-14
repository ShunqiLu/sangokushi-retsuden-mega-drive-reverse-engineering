"""Finite source-role lowering for complete duel actor/display families.

Supplied business Python is the sole policy authority. These exact AST paths
address functions after their optional first docstring is removed. Shared
helper uses have one coupled role; all other effects retain the parent's full
finite matcher. Generation reads no old business, instruction inventory, ASM,
ROM or object. This is not a general Python compiler or a gameplay proof.

Record sizes, resource pointers, live memory ordering, saved slots, fixed state
bit encodings, SUB borrow observations and multiple-entry/shared-tail layouts
stay fixed. Editable pattern arithmetic does not prove resources exist for all
results. BYTE/WORD partial writes and original exceptional behavior are kept.
"""
from .menu_policy_duel import MenuRole
from .compiler_common import CompileError


ROLE_SPECS = (
    MenuRole('name_default_rows', 'upload_duel_officer_name', (('body', 4, 'value', 'args', 1),), 'word', 2, (163114,), ()),
    MenuRole('name_terminator_rows', 'upload_duel_officer_name', (('body', 5, 'body', 0, 'value', 'args', 1),), 'word', 1, (163126,), ()),
    MenuRole('name_shade_shift', 'upload_duel_officer_name', (('body', 5, 'body', 1, 'value', 'args', 0, 'left', 'args', 0, 'right'), ('body', 5, 'body', 4, 'body', 1, 'value', 'args', 1, 'args', 0, 'left', 'right')), 'shift', 4, (163132,), ()),
    MenuRole('name_buffer_bytes', 'upload_duel_officer_name', (('body', 5, 'body', 3, 'iter', 'args', 0),), 'nonzero_word', 64, (163136,), ()),
    MenuRole('name_upload_count', '_expand_and_upload_duel_glyphs', (('body', 6, 'value', 'args', 2),), 'word', 95, (163178,), ()),
    MenuRole('text_clear_fill', 'clear_duel_text_plane', (('body', 3, 'body', 0, 'value', 'args', 2), ('body', 4, 'body', 0, 'value', 'func', 'value', 'args', 1)), 'long', 286331153, (163210,), (('clear_duel_text_complete', ('body', 3, 'value', 'args', 1)),)),
    MenuRole('text_clear_words', 'clear_duel_text_plane', (('body', 3, 'iter', 'args', 0),), 'nonzero_word', 640, (163216,), ()),
    MenuRole('lane_ramp_step', 'decode_duel_byte_lane', (('body', 7, 'body', 1, 'orelse', 0, 'orelse', 0, 'orelse', 2, 'body', 3, 'value', 'args', 1, 'args', 0, 'right'),), 'quick', 1, (163960,), ()),
    MenuRole('actor_timer_step', 'update_duel_actor', (('body', 5, 'body', 0, 'body', 0, 'value', 'args', 1, 'args', 0, 'right'),), 'quick', 1, (166816, 166826, 166836, 166846), ()),
    MenuRole('actor_flash_mask', 'update_duel_actor', (('body', 8, 'body', 2, 'value', 'args', 1, 'right'), ('body', 8, 'body', 3, 'test', 'operand', 'right'), ('body', 16, 'body', 4, 'value', 'args', 1, 'right'), ('body', 16, 'body', 5, 'test', 'operand', 'right')), 'word', 1, (166884, 167348), ()),
    MenuRole('actor_palette_words', '_copy_duel_palette', (('body', 2, 'iter', 'args', 0),), 'nonzero_word', 8, (166880, 167364), ()),
    MenuRole('actor_left_command_bit', 'update_duel_actor', (('body', 12, 'body', 2, 'test', 'operand', 'right'),), 'long_bit', 256, (166910,), ()),
    MenuRole('actor_right_command_bit', 'update_duel_actor', (('body', 12, 'body', 2, 'body', 1, 'test', 'right'),), 'long_bit', 512, (166918,), ()),
    MenuRole('actor_attack_command_bit', 'update_duel_actor', (('body', 12, 'body', 5, 'test', 'right'),), 'long_bit', 16, (166930,), ()),
    MenuRole('actor_special_command_bit', 'update_duel_actor', (('body', 12, 'body', 5, 'orelse', 1, 'test', 'right'),), 'long_bit', 8192, (166966,), ()),
    MenuRole('actor_attack_phase', 'update_duel_actor', (('body', 12, 'orelse', 1, 'body', 0, 'test', 'comparators', 0),), 'word', 4, (166996,), ()),
    MenuRole('actor_attack_phase_relation', 'update_duel_actor', (('body', 12, 'orelse', 1, 'body', 0, 'test', 'ops', 0),), 'unsigned_relation', '==', (167000,), ()),
    MenuRole('actor_clash_kind_mask', 'update_duel_actor', (('body', 12, 'orelse', 1, 'body', 0, 'body', 2, 'body', 0, 'body', 0, 'value', 'args', 1, 'right'), ('body', 12, 'orelse', 1, 'body', 0, 'body', 2, 'body', 0, 'body', 1, 'value', 'right')), 'word', 3, (167028, 167032), ()),
    MenuRole('actor_clash_relation', 'update_duel_actor', (('body', 12, 'orelse', 1, 'body', 0, 'body', 2, 'body', 0, 'body', 3, 'test', 'ops', 0),), 'unsigned_relation', '==', (167038,), ()),
    MenuRole('actor_clash_sound', 'update_duel_actor', (('body', 12, 'orelse', 1, 'body', 0, 'body', 2, 'body', 0, 'body', 3, 'body', 1, 'value', 'args', 1),), 'byte', 160, (167044,), ()),
    MenuRole('actor_attack_delay', 'update_duel_actor', (('body', 13, 'body', 0, 'value', 'args', 1),), 'word', 4, (167284,), ()),
    MenuRole('actor_attack_cycle_step', 'update_duel_actor', (('body', 13, 'body', 1, 'value', 'args', 1, 'args', 0, 'right'),), 'quick', 1, (167290,), ()),
    MenuRole('actor_attack_cycle_bound', 'update_duel_actor', (('body', 13, 'body', 2, 'test', 'comparators', 0),), 'word', 5, (167292,), ()),
    MenuRole('actor_attack_cycle_relation', 'update_duel_actor', (('body', 13, 'body', 2, 'test', 'ops', 0),), 'unsigned_relation', '>=', (167296,), ()),
    MenuRole('actor_glow_first', 'update_duel_actor', (('body', 16, 'body', 2, 'value', 'body'),), 'word', 1024, (167316,), ()),
    MenuRole('actor_glow_second', 'update_duel_actor', (('body', 16, 'body', 2, 'value', 'orelse'),), 'word', 2048, (167336,), ()),
    MenuRole('actor_palette_keep_mask', 'update_duel_actor', (('body', 16, 'body', 6, 'value', 'args', 1, 'left', 'right'),), 'word', 62451, (167358,), ()),
    MenuRole('actor_motion_request_mask', 'update_duel_actor', (('body', 17, 'orelse', 2, 'value', 'right'),), 'word', 12, (167404,), ()),
    MenuRole('actor_motion_first_direction', 'update_duel_actor', (('body', 17, 'orelse', 5, 'body', 0, 'value', 'body'),), 'word', 4, (167422,), ()),
    MenuRole('actor_motion_second_direction', 'update_duel_actor', (('body', 17, 'orelse', 5, 'body', 0, 'value', 'orelse'),), 'word', 8, (167410,), ()),
    MenuRole('actor_motion_tick_mask', 'update_duel_actor', (('body', 17, 'orelse', 5, 'body', 4, 'body', 0, 'value', 'right'),), 'word', 15, (167436,), ()),
    MenuRole('actor_motion_delay', 'update_duel_actor', (('body', 17, 'orelse', 5, 'body', 4, 'body', 2, 'body', 1, 'value', 'args', 1),), 'word', 48, (167448,), ()),
    MenuRole('actor_motion_mode_mask', 'update_duel_actor', (('body', 17, 'orelse', 6, 'test', 'values', 1, 'right'), ('body', 17, 'orelse', 6, 'body', 0, 'value', 'args', 1, 'right'), ('body', 17, 'orelse', 6, 'orelse', 0, 'body', 0, 'value', 'args', 1, 'right')), 'word', 3072, (167458, 167672), (('_render_duel_movement_overlay', ('body', 2, 'body', 2, 'body', 1, 'value', 'right')),)),
    MenuRole('actor_motion_boost', 'update_duel_actor', (('body', 17, 'orelse', 6, 'body', 6, 'body', 0, 'value', 'args', 0, 'right'),), 'long', 32768, (167486,), ()),
    MenuRole('actor_motion_reverse_mask', 'update_duel_actor', (('body', 17, 'orelse', 6, 'body', 7, 'test', 'operand', 'right'), ('body', 17, 'orelse', 6, 'body', 8, 'value', 'args', 1, 'right')), 'word', 2048, (167492,), ()),
    MenuRole('actor_motion_minimum', 'update_duel_actor', (('body', 17, 'orelse', 6, 'body', 14, 'test', 'left'),), 'word', 16, (167522,), ()),
    MenuRole('actor_motion_maximum', 'update_duel_actor', (('body', 17, 'orelse', 6, 'body', 14, 'test', 'comparators', 1),), 'word', 224, (167516,), ()),
    MenuRole('actor_motion_minimum_relation', 'update_duel_actor', (('body', 17, 'orelse', 6, 'body', 14, 'test', 'ops', 0),), 'unsigned_relation', '<=', (167526,), ()),
    MenuRole('actor_motion_maximum_relation', 'update_duel_actor', (('body', 17, 'orelse', 6, 'body', 14, 'test', 'ops', 1),), 'unsigned_relation', '<', (167520,), ()),
    MenuRole('strike_sound', '_apply_duel_strike', (('body', 1, 'value', 'args', 1),), 'byte', 167, (167066,), ()),
    MenuRole('strike_recovery_delay', '_apply_duel_strike', (('body', 2, 'value', 'args', 1),), 'word', 60, (167076,), ()),
    MenuRole('strike_random_mask', '_apply_duel_strike', (('body', 3, 'value', 'right'),), 'word', 7, (167088,), ()),
    MenuRole('strike_random_bound', '_apply_duel_strike', (('body', 4, 'test', 'comparators', 0),), 'word', 6, (167092,), ()),
    MenuRole('strike_random_relation', '_apply_duel_strike', (('body', 4, 'test', 'ops', 0),), 'unsigned_relation', '>=', (167096,), ()),
    MenuRole('strike_random_fold', '_apply_duel_strike', (('body', 4, 'body', 0, 'value', 'args', 0, 'right'),), 'quick', 4, (167098,), ()),
    MenuRole('strike_zero_weapon_relation', '_apply_duel_strike', (('body', 11, 'test', 'ops', 0),), 'unsigned_relation', '==', (167128,), ()),
    MenuRole('strike_second_weapon_bound', '_apply_duel_strike', (('body', 11, 'orelse', 0, 'test', 'comparators', 0),), 'word', 1, (167146,), ()),
    MenuRole('strike_second_weapon_relation', '_apply_duel_strike', (('body', 11, 'orelse', 0, 'test', 'ops', 0),), 'unsigned_relation', '<=', (167150,), ()),
    MenuRole('render_skip_bit', 'render_duel_actor', (('body', 4, 'test', 'right'),), 'long_bit', 8, (167532,), ()),
    MenuRole('render_defeated_relation', 'render_duel_actor', (('body', 5, 'test', 'ops', 0),), 'unsigned_relation', '==', (167546,), ()),
    MenuRole('render_injured_x', 'render_duel_actor', (('body', 5, 'body', 5, 'value', 'body'), ('body', 5, 'orelse', 11, 'value', 'body')), 'word', 84, (167604, 167804), ()),
    MenuRole('render_baseline_x', 'render_duel_actor', (('body', 5, 'body', 5, 'value', 'orelse'), ('body', 5, 'orelse', 11, 'value', 'orelse')), 'word', 88, (167590, 167790, 167690), (('_render_duel_movement_overlay', ('body', 8, 'value', 'args', 1, 'args', 1)), ('_render_duel_movement_overlay', ('body', 11, 'value', 'args', 1)))),
    MenuRole('render_mode_stride', 'render_duel_actor', (('body', 5, 'orelse', 0, 'value', 'args', 0, 'right'),), 'word', 18, (167556,), ()),
    MenuRole('render_direction_stride', 'render_duel_actor', (('body', 5, 'orelse', 3, 'value', 'args', 0, 'right'),), 'word', 6, (167566,), ()),
    MenuRole('render_special_pattern', 'render_duel_actor', (('body', 5, 'orelse', 7, 'body', 0, 'value'),), 'word', 5, (167584,), ()),
    MenuRole('overlay_frame_delay', '_render_duel_movement_overlay', (('body', 2, 'body', 0, 'value', 'args', 1),), 'word', 10, (167648,), ()),
    MenuRole('overlay_animation_step', '_render_duel_movement_overlay', (('body', 2, 'body', 1, 'value', 'args', 0, 'right'),), 'quick', 1, (167658,), ()),
    MenuRole('overlay_animation_bound', '_render_duel_movement_overlay', (('body', 2, 'body', 2, 'test', 'comparators', 0),), 'word', 5, (167660,), ()),
    MenuRole('overlay_animation_relation', '_render_duel_movement_overlay', (('body', 2, 'body', 2, 'test', 'ops', 0),), 'unsigned_relation', '>=', (167664,), ()),
    MenuRole('overlay_animation_restart', '_render_duel_movement_overlay', (('body', 2, 'body', 2, 'body', 0, 'value'),), 'word', 1, (167666,), ()),
    MenuRole('overlay_plain_pattern', '_render_duel_movement_overlay', (('body', 4, 'value', 'body'),), 'word', 62, (167714,), ()),
    MenuRole('overlay_armed_pattern', '_render_duel_movement_overlay', (('body', 4, 'value', 'orelse'),), 'word', 54, (167704,), ()),
    MenuRole('overlay_blink_shift', '_render_duel_movement_overlay', (('body', 6, 'body', 0, 'value', 'args', 0, 'left', 'left', 'right'),), 'shift', 4, (167736,), ()),
    MenuRole('overlay_blink_mask', '_render_duel_movement_overlay', (('body', 6, 'body', 0, 'value', 'args', 0, 'left', 'right'),), 'word', 1, (167738,), ()),
    MenuRole('overlay_blink_pattern', '_render_duel_movement_overlay', (('body', 6, 'body', 0, 'value', 'args', 0, 'right'),), 'word', 60, (167742,), ()),
    MenuRole('threshold_relation', 'scan_duel_thresholds', (('body', 3, 'body', 2, 'test', 'ops', 0),), 'unsigned_relation', '<', (167832,), ()),
    MenuRole('sprite_index_step', 'append_duel_sprite', (('body', 12, 'value', 'args', 0, 'right'), ('body', 18, 'body', 11, 'value', 'args', 0, 'right'), ('body', 21, 'value', 'args', 0, 'right')), 'quick', 1, (167874, 167908, 167978), ()),
    MenuRole('sprite_vertical_origin', 'append_duel_sprite', (('body', 18, 'body', 3, 'value', 'args', 0, 'right'),), 'word', 128, (167894,), ()),
    MenuRole('sprite_size_shift', 'append_duel_sprite', (('body', 18, 'body', 8, 'value', 'body', 'args', 1, 'args', 0, 'right'), ('body', 18, 'body', 9, 'value', 'left', 'args', 0, 'right')), 'shift', 8, (167904,), ()),
    MenuRole('sprite_extent_shift', 'append_duel_sprite', (('body', 18, 'body', 13, 'value', 'args', 0, 'left', 'left', 'right'),), 'shift', 7, (167912,), ()),
    MenuRole('sprite_extent_mask', 'append_duel_sprite', (('body', 18, 'body', 13, 'value', 'args', 0, 'left', 'right'),), 'word', 24, (167914,), ()),
    MenuRole('sprite_extent_bias', 'append_duel_sprite', (('body', 18, 'body', 13, 'value', 'args', 0, 'right'),), 'quick', 8, (167918,), ()),
    MenuRole('sprite_horizontal_origin', 'append_duel_sprite', (('body', 18, 'body', 23, 'value', 'args', 0, 'right'),), 'word', 128, (167950,), ()),
    MenuRole('contact_facing_bit', 'measure_duel_weapon_contact', (('body', 7, 'test', 'operand', 'right'), ('body', 10, 'value', 'test', 'right')), 'long_bit', 8, (172600, 172624), ()),
)


_OWNER_ROLE_NAMES = {'append_duel_sprite': ('sprite_index_step', 'sprite_vertical_origin', 'sprite_size_shift', 'sprite_extent_shift', 'sprite_extent_mask', 'sprite_extent_bias', 'sprite_horizontal_origin'), 'clear_duel_text_plane': ('text_clear_fill', 'text_clear_words'), 'decode_duel_byte_lanes': ('lane_ramp_step',), 'measure_duel_weapon_contact': ('contact_facing_bit',), 'scan_duel_thresholds': ('threshold_relation',), 'update_duel_actor': ('actor_timer_step', 'actor_flash_mask', 'actor_palette_words', 'actor_left_command_bit', 'actor_right_command_bit', 'actor_attack_command_bit', 'actor_special_command_bit', 'actor_attack_phase', 'actor_attack_phase_relation', 'actor_clash_kind_mask', 'actor_clash_relation', 'actor_clash_sound', 'actor_attack_delay', 'actor_attack_cycle_step', 'actor_attack_cycle_bound', 'actor_attack_cycle_relation', 'actor_glow_first', 'actor_glow_second', 'actor_palette_keep_mask', 'actor_motion_request_mask', 'actor_motion_first_direction', 'actor_motion_second_direction', 'actor_motion_tick_mask', 'actor_motion_delay', 'actor_motion_mode_mask', 'actor_motion_boost', 'actor_motion_reverse_mask', 'actor_motion_minimum', 'actor_motion_maximum', 'actor_motion_minimum_relation', 'actor_motion_maximum_relation', 'strike_sound', 'strike_recovery_delay', 'strike_random_mask', 'strike_random_bound', 'strike_random_relation', 'strike_random_fold', 'strike_zero_weapon_relation', 'strike_second_weapon_bound', 'strike_second_weapon_relation', 'render_skip_bit', 'render_defeated_relation', 'render_injured_x', 'render_baseline_x', 'render_mode_stride', 'render_direction_stride', 'render_special_pattern', 'overlay_frame_delay', 'overlay_animation_step', 'overlay_animation_bound', 'overlay_animation_relation', 'overlay_animation_restart', 'overlay_plain_pattern', 'overlay_armed_pattern', 'overlay_blink_shift', 'overlay_blink_mask', 'overlay_blink_pattern'), 'upload_duel_officer_name': ('name_default_rows', 'name_terminator_rows', 'name_shade_shift', 'name_buffer_bytes', 'name_upload_count')}

_RELATION_OWNERS = {'actor_attack_phase_relation': 'update_duel_actor', 'actor_clash_relation': 'update_duel_actor', 'actor_attack_cycle_relation': 'update_duel_actor', 'actor_motion_minimum_relation': 'update_duel_actor', 'actor_motion_maximum_relation': 'update_duel_actor', 'strike_random_relation': 'update_duel_actor', 'strike_zero_weapon_relation': 'update_duel_actor', 'strike_second_weapon_relation': 'update_duel_actor', 'render_defeated_relation': 'update_duel_actor', 'overlay_animation_relation': 'update_duel_actor', 'threshold_relation': 'scan_duel_thresholds'}

_COUNTER_OWNERS = {'actor_palette_words': 'update_duel_actor', 'name_buffer_bytes': 'upload_duel_officer_name', 'text_clear_words': 'clear_duel_text_plane'}

_BIT_OWNERS = {'actor_attack_command_bit': 'update_duel_actor', 'actor_left_command_bit': 'update_duel_actor', 'actor_right_command_bit': 'update_duel_actor', 'actor_special_command_bit': 'update_duel_actor', 'contact_facing_bit': 'measure_duel_weapon_contact', 'render_skip_bit': 'update_duel_actor'}

_BIT_LIMITS = {'actor_attack_command_bit': 32768, 'actor_left_command_bit': 32768, 'actor_right_command_bit': 32768, 'actor_special_command_bit': 32768, 'contact_facing_bit': 128, 'render_skip_bit': 128}

_FALSE_BRANCH = {'<': 'bcc', '<=': 'bhi', '>': 'bls', '>=': 'bcs', '==': 'bne', '!=': 'beq'}
# The source minimum comparison puts its bound on the left: bound OP distance.
# Native CMP.W bound,distance therefore observes the reverse relation.
_REVERSED_FALSE_BRANCH = {'<': 'bls', '<=': 'bcs', '>': 'bcc', '>=': 'bhi', '==': 'bne', '!=': 'beq'}


def owner_rules(values):
    """Map all admitted semantic roles to seven existing physical allocations.

BIT roles must remain inside the original BYTE/WORD observation; carrier-wide
bits outside that width would be ignored by native BTST and are refused. Quick
steps and shifts are checked by the parent finite grammar. No natural resource
domain, threshold termination or arbitrary stack-alias closure is implied.
    """
    for name, maximum in _BIT_LIMITS.items():
        value = values[name]
        if type(value) is not int or value < 1 or value > maximum or value & (value - 1):
            raise CompileError(name + ': one bit within the original observation width required')
    result = {owner: {name: values[name] for name in names}
              for owner, names in _OWNER_ROLE_NAMES.items()}
    for name, owner in _RELATION_OWNERS.items():
        relation = values[name]
        branches = _REVERSED_FALSE_BRANCH if name == 'actor_motion_minimum_relation' else _FALSE_BRANCH
        if type(relation) is not str or relation not in branches:
            raise CompileError(name + ': declared unsigned WORD relation required')
        result[owner][name + '_branch'] = branches[relation]
    for name, owner in _COUNTER_OWNERS.items():
        # DBRA uses an inclusive WORD counter, not the source iteration count.
        result[owner][name + '_counter'] = values[name] - 1
    for name, owner in _BIT_OWNERS.items():
        result[owner][name + '_index'] = values[name].bit_length() - 1
    return result


def _lower_actor_family_upload_duel_officer_name(emitter, rules):
    emitter.segment(163100, 163190)
    emitter.ins('mulu.w', '#0x6,%d7', 4)
    emitter.ins('lea.l', '0x8a504:l,%a0', 6)
    emitter.ins('lea.l', '(%a0, %d7.w),%a0', 4)
    emitter.ins('move.w', f"#0x{rules['name_default_rows']:x},%d3", 4)
    emitter.ins('cmpi.w', '#0x3f,0x4(%a0)', 6)
    emitter.ins('bne.b', 'scene_pc_027d56', 2)
    emitter.ins('move.w', f"#0x{rules['name_terminator_rows']:x},%d3", 4)
    emitter.ins('move.w', '%d0,%d4', 2)
    emitter.ins('asl.w', f"#0x{rules['name_shade_shift']:x},%d4", 2)
    emitter.ins('or.w', '%d0,%d4', 2)
    emitter.ins('move.w', f"#0x{rules['name_buffer_bytes_counter']:x},%d5", 4)
    emitter.ins('lea.l', '0xd300:w,%a1', 4)
    emitter.ins('lea.l', '0xd440:w,%a2', 4)
    emitter.ins('move.b', '%d4,(%a1)+', 2)
    emitter.ins('move.b', '%d4,(%a2)+', 2)
    emitter.ins('dbra', '%d5,scene_pc_027d4c', 4)
    emitter.ins('bra.b', 'scene_pc_027d5a', 2)
    emitter.ins('lea.l', '0xd300:w,%a1', 4)
    emitter.ins('jsr', 'scene_pc_00ae8a:l', 6)
    emitter.ins('lea.l', '0xd300:w,%a0', 4)
    emitter.ins('lea.l', '0xc00000:l,%a6', 6)
    emitter.ins('move.w', f"#0x{rules['name_upload_count']:x},%d0", 4)
    emitter.ins('move.l', '(%a0)+,(%a6)', 2)
    emitter.ins('dbra', '%d0,scene_pc_027d6e', 4)
    emitter.ins('rts', '', 2)
def _lower_actor_family_clear_duel_text_plane(emitter, rules):
    emitter.segment(163190, 163228)
    emitter.ins('clr.w', '0xd100:w', 4)
    emitter.ins('move.l', '#0x46000003,0xc00004:l', 10)
    emitter.ins('lea.l', '0xc00000:l,%a6', 6)
    emitter.ins('move.l', f"#0x{rules['text_clear_fill']:x},%d0", 6)
    emitter.ins('move.w', f"#0x{rules['text_clear_words_counter']:x},%d1", 4)
    emitter.ins('move.l', '%d0,(%a6)', 2)
    emitter.ins('dbra', '%d1,scene_pc_027d94', 4)
    emitter.ins('rts', '', 2)
def _lower_actor_family_decode_duel_byte_lanes(emitter, rules):
    emitter.segment(163858, 163968)
    emitter.ins('movem.l', '%d0/%a1,-(%a7)', 4)
    emitter.ins('bsr.b', 'scene_pc_02801e', 2)
    emitter.ins('movem.l', '(%a7)+,%d0/%a1', 4)
    emitter.ins('addq.w', '#0x1,%a1', 2)
    emitter.ins('tst.w', '%d0', 2)
    emitter.ins('bne.b', 'scene_pc_028024', 2)
    emitter.ins('rts', '', 2)
    emitter.ins('clr.w', '%d1', 2)
    emitter.ins('move.b', '(%a0)+,%d1', 2)
    emitter.ins('bmi.b', 'scene_pc_028036', 2)
    emitter.ins('move.b', '(%a0)+,(%a1)', 2)
    emitter.ins('addq.w', '#0x2,%a1', 2)
    emitter.ins('subq.w', '#0x1,%d0', 2)
    emitter.ins('dbra', '%d1,scene_pc_02802a', 4)
    emitter.ins('bra.b', 'scene_pc_02801e', 2)
    emitter.ins('btst.l', '#0x6,%d1', 4)
    emitter.ins('bne.b', 'scene_pc_02804e', 2)
    emitter.ins('andi.w', '#0x3f,%d1', 4)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('move.b', '%d2,(%a1)', 2)
    emitter.ins('addq.w', '#0x2,%a1', 2)
    emitter.ins('subq.w', '#0x1,%d0', 2)
    emitter.ins('dbra', '%d1,scene_pc_028042', 4)
    emitter.ins('bra.b', 'scene_pc_02801e', 2)
    emitter.ins('btst.l', '#0x5,%d1', 4)
    emitter.ins('bne.b', 'scene_pc_02806c', 2)
    emitter.ins('andi.w', '#0x1f,%d1', 4)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('move.b', '(%a0)+,%d3', 2)
    emitter.ins('move.b', '%d2,(%a1)', 2)
    emitter.ins('addq.w', '#0x2,%a1', 2)
    emitter.ins('move.b', '%d3,(%a1)', 2)
    emitter.ins('addq.w', '#0x2,%a1', 2)
    emitter.ins('subq.w', '#0x2,%d0', 2)
    emitter.ins('dbra', '%d1,scene_pc_02805c', 4)
    emitter.ins('bra.b', 'scene_pc_02801e', 2)
    emitter.ins('andi.w', '#0x1f,%d1', 4)
    emitter.ins('move.b', '(%a0)+,%d2', 2)
    emitter.ins('move.b', '%d2,(%a1)', 2)
    emitter.ins('addq.w', '#0x2,%a1', 2)
    emitter.ins('subq.w', '#0x1,%d0', 2)
    emitter.ins('addq.w', f"#0x{rules['lane_ramp_step']:x},%d2", 2)
    emitter.ins('dbra', '%d1,scene_pc_028072', 4)
    emitter.ins('bra.b', 'scene_pc_02801e', 2)
def _lower_actor_family_update_duel_actor(emitter, rules):
    emitter.segment(166810, 167218)
    emitter.ins('tst.w', '0x8(%a0)', 4)
    emitter.ins('beq.b', 'scene_pc_028ba4', 2)
    emitter.ins('subq.w', f"#0x{rules['actor_timer_step']:x},0x8(%a0)", 4)
    emitter.ins('tst.w', '0xa(%a0)', 4)
    emitter.ins('beq.b', 'scene_pc_028bae', 2)
    emitter.ins('subq.w', f"#0x{rules['actor_timer_step']:x},0xa(%a0)", 4)
    emitter.ins('tst.w', '0x26(%a0)', 4)
    emitter.ins('beq.b', 'scene_pc_028bb8', 2)
    emitter.ins('subq.w', f"#0x{rules['actor_timer_step']:x},0x26(%a0)", 4)
    emitter.ins('tst.w', '0x28(%a0)', 4)
    emitter.ins('beq.b', 'scene_pc_028bc2', 2)
    emitter.ins('subq.w', f"#0x{rules['actor_timer_step']:x},0x28(%a0)", 4)
    emitter.ins('move.w', '0x28(%a0),%d1', 4)
    emitter.ins('beq.b', 'scene_pc_028bf4', 2)
    emitter.ins('lea.l', '-2890(%pc),%a2', 4)
    emitter.ins('lea.l', '0xfb00:w,%a3', 4)
    emitter.ins('cmpa.l', '#0xff7050,%a0', 6)
    emitter.ins('beq.b', 'scene_pc_028be0', 2)
    emitter.ins('lea.l', '-2874(%pc),%a2', 4)
    emitter.ins('lea.l', '0xfb20:w,%a3', 4)
    emitter.ins('move.w', f"#0x{rules['actor_palette_words_counter']:x},%d7", 4)
    emitter.ins('andi.w', f"#0x{rules['actor_flash_mask']:x},%d1", 4)
    emitter.ins('bne.b', 'scene_pc_028bee', 2)
    emitter.ins('lea.l', '-2780(%pc),%a2', 4)
    emitter.ins('move.w', '(%a2)+,(%a3)+', 2)
    emitter.ins('dbra', '%d7,scene_pc_028bee', 4)
    emitter.ins('move.w', '(%a0),%d0', 2)
    emitter.ins('tst.w', '0x2(%a0)', 4)
    emitter.ins('bmi.b', 'scene_pc_028c48', 2)
    emitter.ins('clr.w', '%d1', 2)
    emitter.ins('btst.l', f"#0x{rules['actor_left_command_bit_index']:x},%d0", 4)
    emitter.ins('bne.b', 'scene_pc_028c0e', 2)
    emitter.ins('addq.w', '#0x1,%d1', 2)
    emitter.ins('btst.l', f"#0x{rules['actor_right_command_bit_index']:x},%d0", 4)
    emitter.ins('beq.b', 'scene_pc_028c0e', 2)
    emitter.ins('addq.w', '#0x1,%d1', 2)
    emitter.ins('move.b', '%d1,0x3(%a0)', 4)
    emitter.ins('btst.l', f"#0x{rules['actor_attack_command_bit_index']:x},%d0", 4)
    emitter.ins('beq.b', 'scene_pc_028c30', 2)
    emitter.ins('bset.b', '#0x7,0x2(%a0)', 6)
    emitter.ins('bclr.b', '#0x6,0x2(%a0)', 6)
    emitter.ins('clr.w', '0x4(%a0)', 4)
    emitter.ins('move.w', '0x16(%a0),0x8(%a0)', 6)
    emitter.ins('bra.b', 'scene_pc_028c48', 2)
    emitter.ins('andi.w', '#0x3fff,0x2(%a0)', 6)
    emitter.ins('btst.l', f"#0x{rules['actor_special_command_bit_index']:x},%d0", 4)
    emitter.ins('beq.w', 'scene_pc_028d8e', 4)
    emitter.ins('bset.b', '#0x6,0x2(%a0)', 6)
    emitter.ins('bra.w', 'scene_pc_028d8e', 4)
    emitter.ins('move.w', '0x4(%a0),%d0', 4)
    emitter.ins('tst.w', '0x8(%a0)', 4)
    emitter.ins('bne.w', 'scene_pc_028d8e', 4)
    emitter.ins('cmpi.w', f"#0x{rules['actor_attack_phase']:x},%d0", 4)
    emitter.ins(rules['actor_attack_phase_relation_branch'] + '.w', 'scene_pc_028d74', 4)
    emitter.ins('bsr.w', 'scene_pc_02a22e', 4)
    emitter.ins('bcc.w', 'scene_pc_028d74', 4)
    emitter.ins('btst.b', '#0x6,0x2(%a1)', 6)
    emitter.ins('beq.b', 'scene_pc_028c96', 2)
    emitter.ins('move.w', '0x2(%a0),%d1', 4)
    emitter.ins('move.w', '0x2(%a1),%d2', 4)
    emitter.ins('andi.w', f"#0x{rules['actor_clash_kind_mask']:x},%d1", 4)
    emitter.ins('andi.w', f"#0x{rules['actor_clash_kind_mask']:x},%d2", 4)
    emitter.ins('cmp.w', '%d1,%d2', 2)
    emitter.ins(rules['actor_clash_relation_branch'] + '.b', 'scene_pc_028c96', 2)
    emitter.ins('movem.w', '%d0-%d1,-(%a7)', 4)
    emitter.ins('move.w', f"#0x{rules['actor_clash_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('movem.w', '(%a7)+,%d0-%d1', 4)
    emitter.ins('bra.w', 'scene_pc_028d74', 4)
    emitter.ins('movem.w', '%d0-%d1,-(%a7)', 4)
    emitter.ins('move.w', f"#0x{rules['strike_sound']:x},%d0", 4)
    emitter.ins('jsr', 'scene_pc_00808a:l', 6)
    emitter.ins('move.w', f"#0x{rules['strike_recovery_delay']:x},0x26(%a1)", 6)
    emitter.ins('jsr', 'scene_pc_0083d4:l', 6)
    emitter.ins('andi.w', f"#0x{rules['strike_random_mask']:x},%d0", 4)
    emitter.ins('cmpi.w', f"#0x{rules['strike_random_bound']:x},%d0", 4)
    emitter.ins(rules['strike_random_relation_branch'] + '.b', 'scene_pc_028cbc', 2)
    emitter.ins('subq.w', f"#0x{rules['strike_random_fold']:x},%d0", 2)
    emitter.ins('move.w', '%d0,%d7', 2)
    emitter.ins('move.w', '0x1e(%a0),%d0', 4)
    emitter.ins('lea.l', '110(%pc),%a2', 4)
    emitter.ins('bsr.w', 'scene_pc_028f90', 4)
    emitter.ins('add.w', '114(%pc, %d1.w),%d7', 4)
    emitter.ins('move.w', '0x1e(%a0),%d0', 4)
    emitter.ins('move.w', '0xc(%a0),%d1', 4)
    emitter.ins('tst.w', '%d1', 2)
    emitter.ins(rules['strike_zero_weapon_relation_branch'] + '.w', 'scene_pc_028cea', 4)
    emitter.ins('move.w', '0x2c(%a0),%d2', 4)
    emitter.ins('asl.w', '#0x1,%d2', 2)
    emitter.ins('add.w', '102(%pc, %d2.w),%d0', 4)
    emitter.ins('bra.w', 'scene_pc_028d0a', 4)
    emitter.ins('cmpi.w', f"#0x{rules['strike_second_weapon_bound']:x},%d1", 4)
    emitter.ins(rules['strike_second_weapon_relation_branch'] + '.w', 'scene_pc_028d00', 4)
    emitter.ins('move.w', '0x2a(%a0),%d2', 4)
    emitter.ins('asl.w', '#0x1,%d2', 2)
    emitter.ins('add.w', '88(%pc, %d2.w),%d0', 4)
    emitter.ins('bra.w', 'scene_pc_028d0a', 4)
    emitter.ins('move.w', '0x2e(%a0),%d2', 4)
    emitter.ins('asl.w', '#0x1,%d2', 2)
    emitter.ins('add.w', '82(%pc, %d2.w),%d0', 4)
    emitter.ins('mulu.w', '%d0,%d7', 2)
    emitter.ins('move.w', '0x2(%a0),%d2', 4)
    emitter.ins('andi.w', '#0x3,%d2', 4)
    emitter.ins('asl.w', '#0x1,%d2', 2)
    emitter.ins('divu.w', '86(%pc, %d2.w),%d7', 4)
    emitter.ins('movem.w', '(%a7)+,%d0-%d1', 4)
    emitter.ins('tst.w', '0x1c(%a0)', 4)
    emitter.ins('beq.w', 'scene_pc_028d74', 4)
    emitter.ins('sub.w', '%d7,0x1c(%a1)', 4)
    emitter.ins('bpl.b', 'scene_pc_028d74', 2)
    emitter.ins('clr.w', '0x1c(%a1)', 4)
    emitter.ins('bra.b', 'scene_pc_028d74', 2)
    emitter.segment(167284, 167820)
    emitter.ins('move.w', f"#0x{rules['actor_attack_delay']:x},0x8(%a0)", 6)
    emitter.ins('addq.w', f"#0x{rules['actor_attack_cycle_step']:x},%d0", 2)
    emitter.ins('cmpi.w', f"#0x{rules['actor_attack_cycle_bound']:x},%d0", 4)
    emitter.ins(rules['actor_attack_cycle_relation_branch'] + '.b', 'scene_pc_028d8a', 2)
    emitter.ins('clr.w', '%d0', 2)
    emitter.ins('bclr.b', '#0x7,0x2(%a0)', 6)
    emitter.ins('move.w', '%d0,0x4(%a0)', 4)
    emitter.ins('move.w', '0x26(%a0),%d0', 4)
    emitter.ins('beq.b', 'scene_pc_028dce', 2)
    emitter.ins('move.w', f"#0x{rules['actor_glow_first']:x},%d1", 4)
    emitter.ins('lea.l', '-3354(%pc),%a2', 4)
    emitter.ins('lea.l', '0xfb00:w,%a3', 4)
    emitter.ins('cmpa.l', '#0xff7050,%a0', 6)
    emitter.ins('beq.b', 'scene_pc_028db4', 2)
    emitter.ins('move.w', f"#0x{rules['actor_glow_second']:x},%d1", 4)
    emitter.ins('lea.l', '-3342(%pc),%a2', 4)
    emitter.ins('lea.l', '0xfb20:w,%a3', 4)
    emitter.ins('andi.w', f"#0x{rules['actor_flash_mask']:x},%d0", 4)
    emitter.ins('bne.b', 'scene_pc_028dbe', 2)
    emitter.ins('lea.l', '-3260(%pc),%a2', 4)
    emitter.ins('andi.w', f"#0x{rules['actor_palette_keep_mask']:x},(%a0)", 4)
    emitter.ins('or.w', '%d1,(%a0)', 2)
    emitter.ins('move.w', f"#0x{rules['actor_palette_words_counter']:x},%d3", 4)
    emitter.ins('move.w', '(%a2)+,(%a3)+', 2)
    emitter.ins('dbra', '%d3,scene_pc_028dc8', 4)
    emitter.ins('btst.b', '#0x4,0x2(%a0)', 6)
    emitter.ins('beq.b', 'scene_pc_028de8', 2)
    emitter.ins('tst.w', '0xa(%a0)', 4)
    emitter.ins('bne.w', 'scene_pc_028e6c', 4)
    emitter.ins('bclr.b', '#0x4,0x2(%a0)', 6)
    emitter.ins('bra.w', 'scene_pc_028e6c', 4)
    emitter.ins('move.w', '(%a0),%d0', 2)
    emitter.ins('move.w', '%d0,%d1', 2)
    emitter.ins('andi.w', f"#0x{rules['actor_motion_request_mask']:x},%d0", 4)
    emitter.ins('beq.b', 'scene_pc_028e22', 2)
    emitter.ins('move.w', f"#0x{rules['actor_motion_second_direction']:x},%d3", 4)
    emitter.ins('btst.b', '#0x3,0x18(%a0)', 6)
    emitter.ins('beq.b', 'scene_pc_028e02', 2)
    emitter.ins('move.w', f"#0x{rules['actor_motion_first_direction']:x},%d3", 4)
    emitter.ins('and.w', '%d3,%d0', 2)
    emitter.ins('beq.b', 'scene_pc_028e22', 2)
    emitter.ins('move.w', '0xff7008:l,%d0', 6)
    emitter.ins('andi.w', f"#0x{rules['actor_motion_tick_mask']:x},%d0", 4)
    emitter.ins('bne.b', 'scene_pc_028e22', 2)
    emitter.ins('bset.b', '#0x4,0x2(%a0)', 6)
    emitter.ins('move.w', f"#0x{rules['actor_motion_delay']:x},0xa(%a0)", 6)
    emitter.ins('bra.w', 'scene_pc_028e6c', 4)
    emitter.ins('andi.w', f"#0x{rules['actor_motion_mode_mask']:x},%d1", 4)
    emitter.ins('beq.w', 'scene_pc_028e6c', 4)
    emitter.ins('bset.b', '#0x5,0x2(%a0)', 6)
    emitter.ins('move.l', '0x12(%a0),%d2', 4)
    emitter.ins('move.w', '0x28(%a0),%d3', 4)
    emitter.ins('or.w', '0x26(%a0),%d3', 4)
    emitter.ins('beq.b', 'scene_pc_028e44', 2)
    emitter.ins('addi.l', f"#0x{rules['actor_motion_boost']:x},%d2", 6)
    emitter.ins('andi.w', f"#0x{rules['actor_motion_reverse_mask']:x},%d1", 4)
    emitter.ins('bne.b', 'scene_pc_028e4c', 2)
    emitter.ins('neg.l', '%d2', 2)
    emitter.ins('add.l', '0xe(%a0),%d2', 4)
    emitter.ins('move.l', '%d2,%d1', 2)
    emitter.ins('sub.l', '0xe(%a1),%d1', 4)
    emitter.ins('bpl.b', 'scene_pc_028e5a', 2)
    emitter.ins('neg.l', '%d1', 2)
    emitter.ins('swap', '%d1', 2)
    emitter.ins('cmpi.w', f"#0x{rules['actor_motion_maximum']:x},%d1", 4)
    emitter.ins(rules['actor_motion_maximum_relation_branch'] + '.b', 'scene_pc_028e6c', 2)
    emitter.ins('cmpi.w', f"#0x{rules['actor_motion_minimum']:x},%d1", 4)
    emitter.ins(rules['actor_motion_minimum_relation_branch'] + '.b', 'scene_pc_028e6c', 2)
    emitter.ins('move.l', '%d2,0xe(%a0)', 4)
    emitter.ins('btst.b', f"#0x{rules['render_skip_bit_index']:x},0x2(%a0)", 6)
    emitter.ins('beq.b', 'scene_pc_028e76', 2)
    emitter.ins('rts', '', 2)
    emitter.ins('tst.w', '0x1c(%a0)', 4)
    emitter.ins(rules['render_defeated_relation_branch'] + '.b', 'scene_pc_028e80', 2)
    emitter.ins('bra.w', 'scene_pc_028f50', 4)
    emitter.ins('move.w', '0xc(%a0),%d7', 4)
    emitter.ins('mulu.w', f"#0x{rules['render_mode_stride']:x},%d7", 4)
    emitter.ins('clr.w', '%d2', 2)
    emitter.ins('move.b', '0x3(%a0),%d2', 4)
    emitter.ins('mulu.w', f"#0x{rules['render_direction_stride']:x},%d2", 4)
    emitter.ins('add.w', '%d7,%d2', 2)
    emitter.ins('move.w', '0x4(%a0),%d7', 4)
    emitter.ins('btst.b', '#0x6,0x2(%a0)', 6)
    emitter.ins('beq.b', 'scene_pc_028ea4', 2)
    emitter.ins('move.w', f"#0x{rules['render_special_pattern']:x},%d7", 4)
    emitter.ins('add.w', '%d7,%d2', 2)
    emitter.ins('move.w', f"#0x{rules['render_baseline_x']:x},%d0", 4)
    emitter.ins('btst.b', '#0x4,0x2(%a0)', 6)
    emitter.ins('beq.w', 'scene_pc_028eb8', 4)
    emitter.ins('move.w', f"#0x{rules['render_injured_x']:x},%d0", 4)
    emitter.ins('move.w', '0xe(%a0),%d1', 4)
    emitter.ins('sub.w', '0xff7006:l,%d1', 6)
    emitter.ins('move.w', '0x18(%a0),%d3', 4)
    emitter.ins('movem.l', '%a0-%a1,-(%a7)', 4)
    emitter.ins('bsr.w', 'scene_pc_028f9c', 4)
    emitter.ins('movem.l', '(%a7)+,%a0-%a1', 4)
    emitter.ins('btst.b', '#0x5,0x2(%a0)', 6)
    emitter.ins('beq.b', 'scene_pc_028f0a', 2)
    emitter.ins('tst.w', '0xa(%a0)', 4)
    emitter.ins('bne.b', 'scene_pc_028f0a', 2)
    emitter.ins('move.w', f"#0x{rules['overlay_frame_delay']:x},0xa(%a0)", 6)
    emitter.ins('move.w', '0x6(%a0),%d0', 4)
    emitter.ins('addq.w', f"#0x{rules['overlay_animation_step']:x},%d0", 2)
    emitter.ins('cmpi.w', f"#0x{rules['overlay_animation_bound']:x},%d0", 4)
    emitter.ins(rules['overlay_animation_relation_branch'] + '.b', 'scene_pc_028f06', 2)
    emitter.ins('move.w', f"#0x{rules['overlay_animation_restart']:x},%d0", 4)
    emitter.ins('move.w', '(%a0),%d1', 2)
    emitter.ins('andi.w', f"#0x{rules['actor_motion_mode_mask']:x},%d1", 4)
    emitter.ins('bne.b', 'scene_pc_028f06', 2)
    emitter.ins('bclr.b', '#0x5,0x2(%a0)', 6)
    emitter.ins('clr.w', '%d0', 2)
    emitter.ins('move.w', '%d0,0x6(%a0)', 4)
    emitter.ins('move.w', f"#0x{rules['render_baseline_x']:x},%d0", 4)
    emitter.ins('move.w', '0xe(%a0),%d1', 4)
    emitter.ins('sub.w', '0xff7006:l,%d1', 6)
    emitter.ins('move.w', f"#0x{rules['overlay_armed_pattern']:x},%d2", 4)
    emitter.ins('tst.w', '0xc(%a0)', 4)
    emitter.ins('bne.b', 'scene_pc_028f26', 2)
    emitter.ins('move.w', f"#0x{rules['overlay_plain_pattern']:x},%d2", 4)
    emitter.ins('add.w', '0x6(%a0),%d2', 4)
    emitter.ins('btst.b', '#0x4,0x2(%a0)', 6)
    emitter.ins('beq.b', 'scene_pc_028f42', 2)
    emitter.ins('move.w', '0xff7008:l,%d2', 6)
    emitter.ins('lsr.w', f"#0x{rules['overlay_blink_shift']:x},%d2", 2)
    emitter.ins('andi.w', f"#0x{rules['overlay_blink_mask']:x},%d2", 4)
    emitter.ins('addi.w', f"#0x{rules['overlay_blink_pattern']:x},%d2", 4)
    emitter.ins('move.w', '0x18(%a0),%d3', 4)
    emitter.ins('move.l', '%a0,-(%a7)', 2)
    emitter.ins('bsr.w', 'scene_pc_028f9c', 4)
    emitter.ins('movea.l', '(%a7)+,%a0', 2)
    emitter.ins('rts', '', 2)
    emitter.ins('movem.l', '%d0-%d3/%a0-%a1,-(%a7)', 4)
    emitter.ins('move.w', '0xc(%a0),%d0', 4)
    emitter.ins('move.b', '50(%pc, %d0.w),%d2', 4)
    emitter.ins('andi.w', '#0xff,%d2', 4)
    emitter.ins('move.w', '0x18(%a0),%d3', 4)
    emitter.ins('move.w', '0xe(%a0),%d1', 4)
    emitter.ins('sub.w', '0xff7006:l,%d1', 6)
    emitter.ins('move.w', f"#0x{rules['render_baseline_x']:x},%d0", 4)
    emitter.ins('btst.b', '#0x4,0x2(%a0)', 6)
    emitter.ins('beq.w', 'scene_pc_028f80', 4)
    emitter.ins('move.w', f"#0x{rules['render_injured_x']:x},%d0", 4)
    emitter.ins('bsr.w', 'scene_pc_028f9c', 4)
    emitter.ins('movem.l', '(%a7)+,%d0-%d3/%a0-%a1', 4)
    emitter.ins('bra.w', 'scene_pc_028ed2', 4)
def _lower_actor_family_scan_duel_thresholds(emitter, rules):
    emitter.segment(167824, 167836)
    emitter.ins('move.w', '#0xfffe,%d1', 4)
    emitter.ins('addq.w', '#0x2,%d1', 2)
    emitter.ins('cmp.w', '(%a2)+,%d0', 2)
    emitter.ins(rules['threshold_relation_branch'] + '.b', 'scene_pc_028f94', 2)
    emitter.ins('rts', '', 2)
def _lower_actor_family_append_duel_sprite(emitter, rules):
    emitter.segment(167836, 167992)
    emitter.ins('movem.l', '%d0-%d3,-(%a7)', 4)
    emitter.ins('movea.l', '0xff7002:l,%a0', 6)
    emitter.ins('lea.l', '144(%pc),%a1', 4)
    emitter.ins('asl.w', '#0x2,%d2', 2)
    emitter.ins('movea.l', '(%a1, %d2.w),%a1', 4)
    emitter.ins('move.w', '0xff7000:l,%d2', 6)
    emitter.ins('cmpa.l', '#0xfffff800,%a0', 6)
    emitter.ins('beq.b', 'scene_pc_028fc2', 2)
    emitter.ins('move.b', '%d2,-0x5(%a0)', 4)
    emitter.ins('addq.w', f"#0x{rules['sprite_index_step']:x},%d2", 2)
    emitter.ins('move.w', '%d3,%d4', 2)
    emitter.ins('andi.w', '#0xe7ff,%d3', 4)
    emitter.ins('andi.w', '#0x1800,%d4', 4)
    emitter.ins('move.b', '0x2(%a1),%d7', 4)
    emitter.ins('ext.w', '%d7', 2)
    emitter.ins('add.w', '%d0,%d7', 2)
    emitter.ins('addi.w', f"#0x{rules['sprite_vertical_origin']:x},%d7", 4)
    emitter.ins('move.w', '%d7,(%a0)+', 2)
    emitter.ins('move.b', '0x1(%a1),%d7', 4)
    emitter.ins('asl.w', f"#0x{rules['sprite_size_shift']:x},%d7", 2)
    emitter.ins('or.w', '%d2,%d7', 2)
    emitter.ins('addq.w', f"#0x{rules['sprite_index_step']:x},%d2", 2)
    emitter.ins('move.w', '%d7,(%a0)+', 2)
    emitter.ins('asr.w', f"#0x{rules['sprite_extent_shift']:x},%d7", 2)
    emitter.ins('andi.w', f"#0x{rules['sprite_extent_mask']:x},%d7", 4)
    emitter.ins('addq.w', f"#0x{rules['sprite_extent_bias']:x},%d7", 2)
    emitter.ins('move.w', '%d7,%d5', 2)
    emitter.ins('move.w', '0x4(%a1),%d7', 4)
    emitter.ins('add.w', '%d3,%d7', 2)
    emitter.ins('eor.w', '%d4,%d7', 2)
    emitter.ins('move.w', '%d7,(%a0)+', 2)
    emitter.ins('move.b', '0x3(%a1),%d7', 4)
    emitter.ins('ext.w', '%d7', 2)
    emitter.ins('btst.l', '#0xb,%d4', 4)
    emitter.ins('beq.b', 'scene_pc_02900c', 2)
    emitter.ins('neg.w', '%d7', 2)
    emitter.ins('sub.w', '%d5,%d7', 2)
    emitter.ins('add.w', '%d1,%d7', 2)
    emitter.ins('addi.w', f"#0x{rules['sprite_horizontal_origin']:x},%d7", 4)
    emitter.ins('move.w', '%d7,(%a0)+', 2)
    emitter.ins('addq.w', '#0x6,%a1', 2)
    emitter.ins('btst.b', '#0x7,-0x6(%a1)', 6)
    emitter.ins('beq.b', 'scene_pc_028fce', 2)
    emitter.ins('move.b', '#0x0,-0x5(%a0)', 6)
    emitter.ins('move.l', '%a0,0xff7002:l', 6)
    emitter.ins('subq.w', f"#0x{rules['sprite_index_step']:x},%d2", 2)
    emitter.ins('move.w', '%d2,0xff7000:l', 6)
    emitter.ins('movem.l', '(%a7)+,%d0-%d3', 4)
    emitter.ins('rts', '', 2)
def _lower_actor_family_measure_duel_weapon_contact(emitter, rules):
    emitter.segment(172590, 172640)
    emitter.ins('move.w', '0xc(%a0),%d1', 4)
    emitter.ins('asl.w', '#0x1,%d1', 2)
    emitter.ins('move.w', '42(%pc, %d1.w),%d2', 4)
    emitter.ins('btst.b', f"#0x{rules['contact_facing_bit_index']:x},0x18(%a0)", 6)
    emitter.ins('bne.b', 'scene_pc_02a242', 2)
    emitter.ins('neg.w', '%d2', 2)
    emitter.ins('add.w', '0xe(%a0),%d2', 4)
    emitter.ins('sub.w', '0xe(%a1),%d2', 4)
    emitter.ins('move.w', '%d2,%d3', 2)
    emitter.ins('bpl.b', 'scene_pc_02a250', 2)
    emitter.ins('neg.w', '%d2', 2)
    emitter.ins('btst.b', f"#0x{rules['contact_facing_bit_index']:x},0x18(%a0)", 6)
    emitter.ins('beq.b', 'scene_pc_02a25a', 2)
    emitter.ins('neg.w', '%d3', 2)
    emitter.ins('sub.w', '10(%pc, %d1.w),%d2', 4)
    emitter.ins('rts', '', 2)

LOWERERS = {
    'append_duel_sprite': _lower_actor_family_append_duel_sprite,
    'clear_duel_text_plane': _lower_actor_family_clear_duel_text_plane,
    'decode_duel_byte_lanes': _lower_actor_family_decode_duel_byte_lanes,
    'measure_duel_weapon_contact': _lower_actor_family_measure_duel_weapon_contact,
    'scan_duel_thresholds': _lower_actor_family_scan_duel_thresholds,
    'update_duel_actor': _lower_actor_family_update_duel_actor,
    'upload_duel_officer_name': _lower_actor_family_upload_duel_officer_name,
}


# Root49 relocates only these two changed actor roles.
_STRATEGY_ACTOR_ROLES = {'threshold_relation': {'function': 'scan_duel_thresholds_fields', 'paths': (('body', 2, 'body', 4, 'test', 'ops', 0),), 'coupled_uses': ()}, 'contact_facing_bit': {'function': 'measure_duel_weapon_contact_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_STRATEGY_ACTOR_ROLES[role.name]['function'],_STRATEGY_ACTOR_ROLES[role.name]['paths'],role.kind,role.default,role.physical_pcs,coupled_uses=_STRATEGY_ACTOR_ROLES[role.name]['coupled_uses']) if role.name in _STRATEGY_ACTOR_ROLES else role for role in ROLE_SPECS)


# Root51 seven sprite roles now address the sole complete field algorithm.
_SPRITE_FIELD_ROLES = {'sprite_index_step': {'function': 'append_duel_sprite_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'sprite_vertical_origin': {'function': 'append_duel_sprite_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'sprite_size_shift': {'function': 'append_duel_sprite_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'sprite_extent_shift': {'function': 'append_duel_sprite_fields', 'paths': (('body', 3, 'value'),), 'coupled_uses': ()}, 'sprite_extent_mask': {'function': 'append_duel_sprite_fields', 'paths': (('body', 4, 'value'),), 'coupled_uses': ()}, 'sprite_extent_bias': {'function': 'append_duel_sprite_fields', 'paths': (('body', 5, 'value'),), 'coupled_uses': ()}, 'sprite_horizontal_origin': {'function': 'append_duel_sprite_fields', 'paths': (('body', 6, 'value'),), 'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_SPRITE_FIELD_ROLES[role.name]['function'],_SPRITE_FIELD_ROLES[role.name]['paths'],role.kind,role.default,role.physical_pcs,coupled_uses=_SPRITE_FIELD_ROLES[role.name]['coupled_uses']) if role.name in _SPRITE_FIELD_ROLES else role for role in ROLE_SPECS)


# Root52 relocates every actor phase role to the unique complete field source.
_ACTOR_FIELDS_ROLES = {'actor_timer_step': {'function': 'update_duel_actor_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'actor_flash_mask': {'function': '_duel_actor_palette_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'actor_palette_words': {'function': '_duel_actor_palette_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'actor_left_command_bit': {'function': '_duel_actor_attack_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'actor_right_command_bit': {'function': '_duel_actor_attack_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'actor_attack_command_bit': {'function': '_duel_actor_attack_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'actor_special_command_bit': {'function': '_duel_actor_attack_fields', 'paths': (('body', 3, 'value'),), 'coupled_uses': ()}, 'actor_attack_phase': {'function': '_duel_actor_attack_fields', 'paths': (('body', 4, 'value'),), 'coupled_uses': ()}, 'actor_attack_phase_relation': {'function': '_duel_actor_attack_fields', 'paths': (('body', 18, 'test', 'ops', 0),), 'coupled_uses': ()}, 'actor_clash_kind_mask': {'function': '_duel_actor_attack_fields', 'paths': (('body', 5, 'value'),), 'coupled_uses': ()}, 'actor_clash_relation': {'function': '_duel_actor_attack_fields', 'paths': (('body', 18, 'body', 1, 'body', 2, 'body', 6, 'test', 'ops', 0),), 'coupled_uses': ()}, 'actor_clash_sound': {'function': '_duel_actor_attack_fields', 'paths': (('body', 6, 'value'),), 'coupled_uses': ()}, 'actor_attack_delay': {'function': '_duel_actor_attack_fields', 'paths': (('body', 7, 'value'),), 'coupled_uses': ()}, 'actor_attack_cycle_step': {'function': '_duel_actor_attack_fields', 'paths': (('body', 8, 'value'),), 'coupled_uses': ()}, 'actor_attack_cycle_bound': {'function': '_duel_actor_attack_fields', 'paths': (('body', 9, 'value'),), 'coupled_uses': ()}, 'actor_attack_cycle_relation': {'function': '_duel_actor_attack_fields', 'paths': (('body', 23, 'test', 'ops', 0),), 'coupled_uses': ()}, 'actor_glow_first': {'function': '_duel_actor_palette_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'actor_glow_second': {'function': '_duel_actor_palette_fields', 'paths': (('body', 3, 'value'),), 'coupled_uses': ()}, 'actor_palette_keep_mask': {'function': '_duel_actor_palette_fields', 'paths': (('body', 4, 'value'),), 'coupled_uses': ()}, 'actor_motion_request_mask': {'function': '_duel_actor_motion_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'actor_motion_first_direction': {'function': '_duel_actor_motion_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'actor_motion_second_direction': {'function': '_duel_actor_motion_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'actor_motion_tick_mask': {'function': '_duel_actor_motion_fields', 'paths': (('body', 3, 'value'),), 'coupled_uses': ()}, 'actor_motion_delay': {'function': '_duel_actor_motion_fields', 'paths': (('body', 4, 'value'),), 'coupled_uses': ()}, 'actor_motion_mode_mask': {'function': '_duel_actor_motion_mode_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'actor_motion_boost': {'function': '_duel_actor_motion_fields', 'paths': (('body', 5, 'value'),), 'coupled_uses': ()}, 'actor_motion_reverse_mask': {'function': '_duel_actor_motion_fields', 'paths': (('body', 6, 'value'),), 'coupled_uses': ()}, 'actor_motion_minimum': {'function': '_duel_actor_motion_fields', 'paths': (('body', 7, 'value'),), 'coupled_uses': ()}, 'actor_motion_maximum': {'function': '_duel_actor_motion_fields', 'paths': (('body', 8, 'value'),), 'coupled_uses': ()}, 'actor_motion_minimum_relation': {'function': '_duel_actor_motion_fields', 'paths': (('body', 33, 'body', 1, 'test', 'ops', 0),), 'coupled_uses': ()}, 'actor_motion_maximum_relation': {'function': '_duel_actor_motion_fields', 'paths': (('body', 33, 'test', 'ops', 0),), 'coupled_uses': ()}, 'strike_sound': {'function': '_duel_actor_strike_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'strike_recovery_delay': {'function': '_duel_actor_strike_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'strike_random_mask': {'function': '_duel_actor_strike_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'strike_random_bound': {'function': '_duel_actor_strike_fields', 'paths': (('body', 3, 'value'),), 'coupled_uses': ()}, 'strike_random_relation': {'function': '_duel_actor_strike_fields', 'paths': (('body', 14, 'test', 'ops', 0),), 'coupled_uses': ()}, 'strike_random_fold': {'function': '_duel_actor_strike_fields', 'paths': (('body', 4, 'value'),), 'coupled_uses': ()}, 'strike_zero_weapon_relation': {'function': '_duel_actor_strike_fields', 'paths': (('body', 24, 'test', 'ops', 0),), 'coupled_uses': ()}, 'strike_second_weapon_bound': {'function': '_duel_actor_strike_fields', 'paths': (('body', 5, 'value'),), 'coupled_uses': ()}, 'strike_second_weapon_relation': {'function': '_duel_actor_strike_fields', 'paths': (('body', 24, 'orelse', 1, 'test', 'ops', 0),), 'coupled_uses': ()}, 'render_skip_bit': {'function': 'render_duel_actor_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'render_defeated_relation': {'function': 'render_duel_actor_fields', 'paths': (('body', 10, 'test', 'ops', 0),), 'coupled_uses': ()}, 'render_injured_x': {'function': '_duel_actor_render_positions_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'render_baseline_x': {'function': '_duel_actor_render_positions_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'render_mode_stride': {'function': 'render_duel_actor_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'render_direction_stride': {'function': 'render_duel_actor_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'render_special_pattern': {'function': 'render_duel_actor_fields', 'paths': (('body', 3, 'value'),), 'coupled_uses': ()}, 'overlay_frame_delay': {'function': '_duel_actor_overlay_fields', 'paths': (('body', 0, 'value'),), 'coupled_uses': ()}, 'overlay_animation_step': {'function': '_duel_actor_overlay_fields', 'paths': (('body', 1, 'value'),), 'coupled_uses': ()}, 'overlay_animation_bound': {'function': '_duel_actor_overlay_fields', 'paths': (('body', 2, 'value'),), 'coupled_uses': ()}, 'overlay_animation_relation': {'function': '_duel_actor_overlay_fields', 'paths': (('body', 10, 'body', 1, 'body', 5, 'test', 'ops', 0),), 'coupled_uses': ()}, 'overlay_animation_restart': {'function': '_duel_actor_overlay_fields', 'paths': (('body', 3, 'value'),), 'coupled_uses': ()}, 'overlay_plain_pattern': {'function': '_duel_actor_overlay_fields', 'paths': (('body', 4, 'value'),), 'coupled_uses': ()}, 'overlay_armed_pattern': {'function': '_duel_actor_overlay_fields', 'paths': (('body', 5, 'value'),), 'coupled_uses': ()}, 'overlay_blink_shift': {'function': '_duel_actor_overlay_fields', 'paths': (('body', 6, 'value'),), 'coupled_uses': ()}, 'overlay_blink_mask': {'function': '_duel_actor_overlay_fields', 'paths': (('body', 7, 'value'),), 'coupled_uses': ()}, 'overlay_blink_pattern': {'function': '_duel_actor_overlay_fields', 'paths': (('body', 8, 'value'),), 'coupled_uses': ()}}
ROLE_SPECS = tuple(MenuRole(role.name,_ACTOR_FIELDS_ROLES[role.name]['function'],_ACTOR_FIELDS_ROLES[role.name]['paths'],role.kind,role.default,role.physical_pcs,coupled_uses=_ACTOR_FIELDS_ROLES[role.name]['coupled_uses']) if role.name in _ACTOR_FIELDS_ROLES else role for role in ROLE_SPECS)


# Complete actual Duel fields role topology125; fixed real current business paths, no source fallback.
_ORIGINAL_NATIVE_ROLE_SPECS125 = ROLE_SPECS
_CURRENT_DUEL_ROLE_BINDINGS125 = {'name_default_rows': {'function': 'upload_duel_officer_name_fields', 'paths': (('body', 4, 'value', 'args', 3),), 'coupled_uses': ()}, 'name_terminator_rows': {'function': 'upload_duel_officer_name_fields', 'paths': (('body', 7, 'value', 'args', 3),), 'coupled_uses': ()}, 'name_shade_shift': {'function': 'upload_duel_officer_name_fields', 'paths': (('body', 9, 'value', 'args', 4),), 'coupled_uses': ()}, 'name_upload_count': {'function': '_upload_duel_glyph_buffers_fields', 'paths': (('body', 2, 'value', 'args', 3),), 'coupled_uses': ()}, 'text_clear_fill': {'function': 'clear_duel_text_plane_fields', 'paths': (('body', 4, 'value', 'args', 3),), 'coupled_uses': ()}, 'lane_ramp_step': {'function': 'decode_duel_byte_lane_fields', 'paths': (('body', 1, 'body', 7, 'body', 3, 'body', 0, 'value', 'args', 3),), 'coupled_uses': ()}, 'name_buffer_bytes': {'function': 'upload_duel_officer_name_fields', 'paths': (('body', 11, 'value', 'args', 3),), 'coupled_uses': (), 'kind': 'dbra_word_count'}, 'text_clear_words': {'function': 'clear_duel_text_plane_fields', 'paths': (('body', 5, 'value', 'args', 3),), 'coupled_uses': (), 'kind': 'dbra_word_count'}}
_CURRENT_SHARED_ROLE_ALIASES125 = {}
ROLE_SPECS = tuple(MenuRole(role.name, _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('function', role.function), _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('paths', role.paths), _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('kind', role.kind), role.default, _CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('physical_pcs', role.physical_pcs), coupled_uses=_CURRENT_DUEL_ROLE_BINDINGS125.get(role.name, {}).get('coupled_uses', role.coupled_uses)) for role in ROLE_SPECS if role.name not in _CURRENT_SHARED_ROLE_ALIASES125)
