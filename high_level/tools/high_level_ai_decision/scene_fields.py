"""Complete live Scene carriers shared by strategic AI business modules.

No convenience GameState is promoted to a frame. The caller supplies every
D/A LONG, actual entry SP and complete Scene SR; each real CALL owns one live
LONG slot. Arithmetic helpers retain the original narrow-register lanes.
"""
from ..high_level_scene_flows.domain import SceneState, uint, u8, u16, u32, low8, low16, replace_byte, replace_word, s16
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, first_replace, FirstDeploymentReturnBoundary
from ..high_level_main_flows.business_movement_support import _movement_frame, _movement_test, _movement_test_long, _movement_binary_flags


def store_ai_value_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, value: int, width: int, clear: bool = False) -> FirstDeploymentFrame:
    """A live AI RAM MOVE/CLR; CLR observes its real destination first."""
    if width not in (8, 16, 32) or type(clear) is not bool:
        raise ValueError('actual AI RAM operation width required')
    value = uint(value, width)
    if clear:
        state.read(address, width // 8)
    state.write(address, width // 8, value)
    return _movement_test_long(state, frame, value) if width == 32 else _movement_test(state, frame, value, width)


def adjust_ai_carrier_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, source: int, width: int = 16, subtract: bool = False) -> FirstDeploymentFrame:
    """Keep both original flags and untouched register lanes after arithmetic."""
    old = frame.carrier(name)
    value = low8(old) if width == 8 else low16(old) if width == 16 else old
    frame, result = _movement_binary_flags(state, frame, value, source, width, subtract)
    retained = replace_byte(old, result) if width == 8 else replace_word(old, result) if width == 16 else result
    return first_replace(frame, **{name: retained})


def compare_ai_long_fields(state: SceneState, frame: FirstDeploymentFrame,
        destination: int, source: int) -> FirstDeploymentFrame:
    """Unsigned LONG comparison, preserving incoming X rather than SUB flags."""
    destination, source = uint(destination, 32), uint(source, 32)
    result = u32(destination - source)
    overflow = bool((destination ^ source) & (destination ^ result) & 0x80000000)
    status = frame.status & 16 | (8 if result & 0x80000000 else 0) | (4 if result == 0 else 0) | (2 if overflow else 0) | (1 if destination < source else 0)
    state.sr = state.sr & 65504 | status
    return first_replace(frame, status=status)


def shift_ai_long_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, amount: int, right: bool = False) -> FirstDeploymentFrame:
    """Only the original one/three-bit logical LONG shifts in this group."""
    if amount not in (1, 3) or type(right) is not bool:
        raise ValueError('actual strategic AI LONG shift required')
    original = frame.carrier(name)
    value = original >> amount if right else u32(original << amount)
    carry = bool(original & (1 << (amount - 1 if right else 32 - amount)))
    status = (17 if carry else 0) | (8 if value & 0x80000000 else 0) | (4 if value == 0 else 0)
    state.sr = state.sr & 65504 | status
    return first_replace(frame, **{name: value}, status=status)


def test_ai_register_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, bit: int) -> FirstDeploymentFrame:
    """Dynamic register BTST uses bit modulo32 and changes only Z."""
    bit = uint(bit, 32) & 31
    status = frame.status & ~4 | (0 if uint(value, 32) & 1 << bit else 4)
    state.sr = state.sr & 65504 | status
    return first_replace(frame, status=status)


def set_ai_flag_byte_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, bit: int) -> FirstDeploymentFrame:
    """Real memory BSET BYTE read/modify/write; no MOVE-like flag reset."""
    value = state.read(address, 1)
    frame = test_ai_register_bit_fields(state, frame, value, uint(bit, 8) & 7)
    state.write(address, 1, u8(value | 1 << (bit & 7)))
    return frame


def step_ai_count_fields(frame: FirstDeploymentFrame, name: str) -> FirstDeploymentFrame:
    """The original DBRA changes only the low WORD, not CCR or upper WORD."""
    return first_replace(frame, **{name: replace_word(frame.carrier(name), u16(low16(frame.carrier(name)) - 1))})


def call_scene_ai_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """One original nested BSR/JSR slot, checked and popped by its real caller."""
    if (target, continuation) not in ((205012, 204996), (205118, 205000), (205202, 205004), (205996, 205960), (33748, 206232), (206308, 206240), (206332, 206246), (206308, 206402), (209554, 209528), (210122, 210050), (210168, 210062), (204960, 210114), (218976, 210190), (210292, 210216), (210350, 210228), (210376, 210266), (204960, 210284), (33748, 210382)):
        raise ValueError('actual strategic AI CALL/continuation pair required')
    frame = _movement_frame(state, frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, uint(continuation, 32))
    entered = first_replace(frame, stack_cursor=stack)
    result = execute_scene_ai_fields(state, entered, target)
    result = _movement_frame(state, result)
    returned = result.stack_cursor.long()
    if returned != continuation:
        raise FirstDeploymentReturnBoundary(returned, result, continuation)
    return first_replace(result, stack_cursor=result.stack_cursor.advance(4))


def execute_scene_ai_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int) -> FirstDeploymentFrame:
    """Named whole-core dispatch, without creating a second outer CALL slot."""
    frame = _movement_frame(state, frame)
    from .business_scene_commit import commit_roster_city_assignments_fields, choose_city_head_from_roster_fields, flag_roster_b600_candidate_fields, update_roster_c700_status_fields, commit_city_field_order_fields, select_order_officer_b600_fields, prepare_city_order_amount_fields, commit_officer_training_fields, select_training_officer_c500_fields, prepare_officer_training_cost_fields, apply_officer_training_growth_fields, count_force_cities_fields, select_force_by_city_count_fields
    from ..high_level_ai_policy_v2.business_scene_economy import select_resource_support_city_fields, estimate_city_troop_requirement_fields, plan_force_support_action_fields, choose_resource_action_fields, choose_training_action_fields, select_roster_training_min_fields
    cores = {204992: commit_roster_city_assignments_fields, 205012: choose_city_head_from_roster_fields, 205118: flag_roster_b600_candidate_fields, 205202: update_roster_c700_status_fields, 210026: commit_city_field_order_fields, 210122: select_order_officer_b600_fields, 210168: prepare_city_order_amount_fields, 210212: commit_officer_training_fields, 210292: select_training_officer_c500_fields, 210350: prepare_officer_training_cost_fields, 210376: apply_officer_training_growth_fields, 206308: count_force_cities_fields, 206332: select_force_by_city_count_fields, 205898: select_resource_support_city_fields, 205996: estimate_city_troop_requirement_fields, 206226: plan_force_support_action_fields, 209484: choose_resource_action_fields, 209524: choose_training_action_fields, 209554: select_roster_training_min_fields}
    if target in cores:
        return cores[target](state, frame)
    # Reuse the sole existing complete algorithms by their named real ABI.
    # None creates a second CALL slot or promotes an unobserved scalar state.
    if target == 0x83D4:
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        return first_deployment_random_fields(BattlePolicyMemory(state), frame)
    if target == 0x320A0:
        from ..high_level_remaining_flows.business_highbank import mark_selected_roster_bit14_fields
        return mark_selected_roster_bit14_fields(state, frame)
    if target == 0x35760:
        from ..high_level_main_flows.business_movement_support import signed_divmod_fields
        return signed_divmod_fields(state, frame)
    raise ValueError('target outside the complete strategic AI core vocabulary')
