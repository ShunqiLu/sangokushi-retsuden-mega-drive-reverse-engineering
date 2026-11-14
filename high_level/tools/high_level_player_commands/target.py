"""Complete player command bindings: physical layout only, never opcode data."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    end: int
    completion: str = 'return'

BUDGET_BINDINGS = (
    Binding('prepare_budget_summary_panel', 0x11cf2, 0x11e2a),
    Binding('append_numbered_budget_columns', 0x11e2a, 0x11e3c),
    Binding('prepare_compact_budget_summary_panel', 0x11e3c, 0x11f1c),
    Binding('select_descriptor_portrait_parts', 0x11f82, 0x11ffa),
    Binding('find_first_set_mask_bit', 0x11ffa, 0x12008),
    Binding('prepare_command_amount_modal', 0x12008, 0x12024),
    Binding('append_amount_modal_frame', 0x12024, 0x12064),
    Binding('append_amount_modal_descriptor_limit', 0x12064, 0x12102),
    Binding('append_selected_command_row_label', 0x1221c, 0x12248),
    Binding('clear_command_amount_page', 0x12292, 0x12314),
    Binding('prepare_budget_amount_page', 0x12314, 0x12418),
    Binding('step_budget_amount_controls', 0x12418, 0x124fc),
    Binding('append_budget_cost_and_amount_values', 0x1252c, 0x125ac),
    Binding('append_budget_place_highlight', 0x125ac, 0x125d0),
    Binding('append_budget_header_row', 0x12602, 0x12620),
    Binding('append_budget_first_detail_rows', 0x12620, 0x1268c),
    Binding('append_budget_second_detail_row', 0x1268c, 0x126d2),
    Binding('append_budget_footer_row', 0x126d2, 0x126f0),
    Binding('append_four_budget_numbered_tiles', 0x126f0, 0x1270a),
    Binding('append_six_place_decimal_value', 0x1270a, 0x12760),
    Binding('append_decimal_value_place', 0x12760, 0x12782),
    Binding('prepare_command_amount_limit', 0x1278c, 0x12840),
    Binding('limit_live_command_amount_by_price_record', 0x12878, 0x128e2),
    Binding('update_player_command_amount', 0x128e2, 0x1292c),
    Binding('append_selected_command_amount', 0x1292c, 0x12980),
    Binding('step_live_command_amount_controls', 0x12980, 0x129de),
    Binding('select_previous_amount_place', 0x129de, 0x129f8),
    Binding('select_next_amount_place', 0x129f8, 0x12a0c),
    Binding('decrement_live_command_amount_small', 0x12a2e, 0x12a4e),
    Binding('append_blinking_amount_place', 0x12a4e, 0x12a90),
    Binding('prepare_percentage_panel', 0x12a98, 0x12ab6),
    Binding('append_percentage_header_row', 0x12ab6, 0x12ad4),
    Binding('append_percentage_value_rows', 0x12ad4, 0x12b4c),
    Binding('append_percentage_footer_row', 0x12b4c, 0x12b6a),
    Binding('clear_percentage_panel', 0x12b6a, 0x12bc0),
    Binding('append_percentage_value', 0x12bc0, 0x12c0c),
    Binding('step_percentage_controls', 0x12c0c, 0x12c84),
    Binding('append_percentage_place_highlight', 0x12c84, 0x12cb6),
    Binding('prepare_resource_amount_panel', 0x12cbe, 0x12cf4),
    Binding('append_city_resource_amount_rows', 0x12cf4, 0x12d82),
    Binding('append_live_resource_value_row', 0x12d82, 0x12dfc),
    Binding('append_committed_resource_amount_rows', 0x12dfc, 0x12e74),
    Binding('append_committed_resource_value_row', 0x12e74, 0x12ef2),
)

RECRUITMENT_BINDINGS = (
    Binding('update_recruitment_input_cursor', 0x12f58, 0x12f8e),
    Binding('update_recruitment_total_cursor', 0x13034, 0x1306a),
    Binding('append_recruitment_dialog_frame', 0x1306a, 0x13176),
    Binding('append_recruitment_paired_tiles', 0x13176, 0x13188),
    Binding('prepare_player_recruitment_capacity', 0x13188, 0x1321c),
    Binding('append_recruitment_input_digits', 0x1321c, 0x13270),
    Binding('append_recruitment_total_digits', 0x13270, 0x132ae),
    Binding('append_equipment_amount_cursor', 0x13510, 0x1353e),
    Binding('clear_equipment_dialog_rows', 0x1353e, 0x135c4),
    Binding('append_equipment_dialog_frame', 0x135c4, 0x136e2),
    Binding('append_equipment_paired_tiles', 0x136e2, 0x136f4),
    Binding('append_equipment_input_digits', 0x136f4, 0x1374a),
    Binding('append_equipment_total_digits', 0x1374a, 0x1379a),
    Binding('append_candidate_amount_cursor', 0x13934, 0x13958),
    Binding('append_candidate_dialog_frame', 0x13958, 0x13a84),
    Binding('append_candidate_paired_tiles', 0x13a84, 0x13a96),
    Binding('append_candidate_separator_row', 0x13a96, 0x13ab6),
    Binding('update_equipment_category', 0x13b86, 0x13bda),
    Binding('append_equipment_category_cursor', 0x13bda, 0x13c1c),
    Binding('clear_candidate_dialog_rows', 0x13c7e, 0x13d48),
    Binding('prepare_selected_training_cost_steps', 0x13df6, 0x13e42),
    Binding('update_selected_training_amount', 0x13e92, 0x13f66),
    Binding('append_training_cost_digits', 0x13f6c, 0x13faa),
    Binding('append_training_amount_cursor', 0x13faa, 0x13fdc),
    Binding('prepare_selected_training_origin_and_speed', 0x13fe4, 0x14050),
)

DISPLAY_BINDINGS = (
    Binding('append_live_command_string_words', 0xac08, 0xad06),
    Binding('append_route_selection_pair', 0x14106, 0x14120),
    Binding('append_route_cursor_sprite', 0x14120, 0x14150),
    Binding('step_world_route_cursor', 0x1416a, 0x14294),
    Binding('query_scaled_route_terrain', 0x14294, 0x142a2),
    Binding('query_route_move_cost', 0x142ca, 0x142d0),
    Binding('append_candidate_member_panel', 0x14494, 0x14562),
    Binding('append_short_paired_tiles', 0x14562, 0x14574),
    Binding('append_selected_group_panel', 0x14574, 0x14778),
    Binding('append_wide_paired_tiles', 0x14778, 0x1478a),
    Binding('step_candidate_selection_cursor', 0x148a4, 0x14914),
    Binding('append_candidate_selection_sprite', 0x14914, 0x14956),
    Binding('collect_group_members_below_capacity', 0x149a0, 0x149e4),
    Binding('clear_world_group_selection_marks', 0x14c7c, 0x14ca4),
    Binding('select_world_group_or_city_at_marker', 0x14ca4, 0x14d34),
    Binding('find_world_marker_record', 0x14d34, 0x14d64),
    Binding('test_selected_group_enemy_contacts', 0x14e20, 0x14e58),
    Binding('set_pending_group_move_position', 0x150de, 0x1512e),
    Binding('merge_compatible_world_groups', 0x1512e, 0x15186),
    Binding('merge_world_group_records', 0x15186, 0x152be),
    Binding('test_pending_group_destination', 0x152be, 0x15384),
    Binding('encode_live_group_coordinate_packet', 0x1cea0, 0x1cf58),
)

REUSED_BINDINGS = (
    Binding('add_selected_cost', 0x12a0c, 0x12a2e),
    Binding('terrain_cell_query', 0x142a2, 0x142ca),
    Binding('collect_blocked_cargo', 0x154c8, 0x15572),
)

NEW_BINDINGS = tuple(sorted(BUDGET_BINDINGS + RECRUITMENT_BINDINGS + DISPLAY_BINDINGS, key=lambda b:b.entry))
BINDINGS = tuple(sorted(NEW_BINDINGS + REUSED_BINDINGS, key=lambda b:b.entry))
BY_NAME = {b.name:b for b in BINDINGS}
BY_ENTRY = {b.entry:b for b in BINDINGS}
ALTERNATE_ENTRY = {0xac10:0xac08, 0x12744:0x1270a, 0x1274c:0x1270a}

def validate_binding(binding):
    if type(binding) is not Binding or BY_NAME.get(binding.name) != binding:
        raise ValueError('declared complete semantic Binding required')
    if (type(binding.entry) is not int or type(binding.end) is not int or not 0 <= binding.entry < binding.end <= 0x100000 or binding.entry & 1 or binding.end & 1 or binding.completion != 'return'):
        raise ValueError('strict complete original returning extent required')
    return binding

if (len(NEW_BINDINGS),sum(b.end-b.entry for b in NEW_BINDINGS)) != (90,9320):
    raise ValueError('exact new candidate scope required')
if len(BY_NAME) != len(BINDINGS) or len(BY_ENTRY) != len(BINDINGS) or any(a.end>b.entry for a,b in zip(BINDINGS,BINDINGS[1:])):
    raise ValueError('unique non-overlapping complete bindings required')
