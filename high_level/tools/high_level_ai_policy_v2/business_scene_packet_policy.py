"""Live packed-group supply, destinations, staging and contact policies.

confirmed: complete editable original owners34140..3471A. Every policy uses
the same actual Scene, full carrier frame and physical caller stack.
"""
from ..high_level_scene_flows.domain import SceneState, low8, low16, s16, u8, u16, u32, replace_byte, replace_word, swap_words
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test, _movement_test_long,
    _movement_compare, _movement_fixed_shift_word, _movement_shift_long,
    _movement_binary_flags, _movement_arithmetic_long, _movement_multiply_word,
    _movement_divu_word, _movement_save_longs, _movement_restore_longs, _path_carry_fields,
)
from ..high_level_ai_decision.scene_fields import (
    store_ai_value_fields, adjust_ai_carrier_fields, compare_ai_long_fields,
    shift_ai_long_fields, set_ai_flag_byte_fields, test_ai_register_bit_fields, step_ai_count_fields,
)


def _packet_policy_neg_fields(state, frame, carrier, width=16):
    """One real NEG, retaining lanes above its exact BYTE/WORD destination."""
    previous = low8(frame.carrier(carrier)) if width == 8 else low16(frame.carrier(carrier))
    frame, value = _movement_binary_flags(state, frame, 0, previous, width, True)
    return first_replace(frame, **{carrier: replace_byte(frame.carrier(carrier), value) if width == 8 else replace_word(frame.carrier(carrier), value)})


def _packet_policy_group_fields(state, frame, base=0xFFFF9000):
    """Original address-only LEA/ADDA.W; neither changes CCR."""
    return first_replace(frame, roster=state.table_at(base).cursor().advance(s16(state.read(0xFFFFF75A, 2))))


def _packet_policy_packed_long_fields(state, frame, carrier, first):
    """Original first WORD shift then two LONG shifts and three BYTE loads."""
    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first), 8)
    frame = _movement_fixed_shift_word(state, frame, carrier, 8)
    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first + 1), 8)
    for displacement in (first + 2, first + 3):
        frame = _movement_shift_long(state, frame, carrier)
        frame = _movement_move(state, frame, carrier, frame.roster.byte(0, displacement), 8)
    return frame


def evaluate_packed_group_supply_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34140: quote before the four live food BYTE reads; phase2 or6."""
    frame = _packet_policy_group_fields(state, _movement_frame(state, frame))
    frame = _packet_policy_call_fields(state, frame, 0x3417A, 0x3414C)
    frame = _packet_policy_packed_long_fields(state, frame, 'target_x', 9)
    frame = compare_ai_long_fields(state, frame, frame.target_x, frame.unit)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 2 if frame.status & 1 else 6, 16)


def price_packed_group_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3417A: reverse nibble roster, real DIVU and WORD-only triple product."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', 1, subtract=True)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move_long(state, frame, 'unit', 0)
    while True:
        frame = _movement_move(state, frame, 'target_y', 0, 16)
        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x), 13), 8)
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
        frame = _movement_arithmetic_long(state, frame, 'unit', frame.candidates.long(low16(frame.target_y)))
        frame = _movement_arithmetic_long(state, frame, 'unit', 100)
        frame = step_ai_count_fields(frame, 'target_x')
        if low16(frame.target_x) == 65535:
            break
    frame = _movement_divu_word(state, frame, 'unit', 10, 0x3419E)
    frame = _movement_move(state, frame, 'target_y', low16(frame.unit), 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', low16(frame.target_y))
    return _movement_move_long(state, frame, 'unit', frame.unit & 65535)


def choose_group_destination_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """341B0: use the complete destination search, then its live RAM result."""
    frame = _packet_policy_call_fields(state, _movement_frame(state, frame), 0x341CE, 0x341B4)
    frame = _movement_test(state, frame, state.read(0xFFFFF392, 2), 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 3 if frame.status & 8 else 4, 16)


def choose_ai_destination_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """341CE: owned cities, roster capacity, Manhattan prefilter and real path."""
    frame = _packet_policy_group_fields(state, _movement_frame(state, frame))
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 3), 8)
    for carrier, slot, destination in (('target_y', 1, 0xFFFFF63C), ('unit', 2, 0xFFFFF63E)):
        frame = _movement_move(state, frame, carrier, 0, 16)
        frame = _movement_move(state, frame, carrier, frame.roster.byte(0, slot), 8)
        frame = _movement_fixed_shift_word(state, frame, carrier, 4)
        frame = store_ai_value_fields(state, frame, destination, low16(frame.carrier(carrier)), 16)
        frame = _movement_fixed_shift_word(state, frame, carrier, 4, True)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFF428).cursor(), controller=state.table_at(0xD4ACA))
    frame = _movement_move(state, frame, 'count', 39, 16)
    frame = _movement_move(state, frame, 'choice', 65535, 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF392, 65535, 16)
    while True:
        frame = _movement_move(state, frame, 'distance', 0, 16)
        frame = _movement_move(state, frame, 'distance', frame.candidates.byte(low16(frame.count)), 8)
        frame = _movement_compare(state, frame, low16(frame.distance), state.read(0xFFFFF376, 2), 16)
        eligible = bool(frame.status & 4)
        if eligible:
            frame = _packet_policy_call_fields(state, frame, 0x34280, 0x34222)
            eligible = not bool(frame.status & 1)
        if eligible:
            frame = _movement_move(state, frame, 'distance', low16(frame.count), 16)
            frame = _movement_fixed_shift_word(state, frame, 'distance', 2)
            frame = _movement_move(state, frame, 'offset_x', frame.controller.word(low16(frame.distance), 2), 16)
            frame = store_ai_value_fields(state, frame, 0xFFFFF640, low16(frame.offset_x), 16)
            frame = _movement_fixed_shift_word(state, frame, 'offset_x', 4, True)
            frame = adjust_ai_carrier_fields(state, frame, 'offset_x', low16(frame.target_y), subtract=True)
            if frame.status & 1:
                frame = _packet_policy_neg_fields(state, frame, 'offset_x')
            frame = _movement_compare(state, frame, low16(frame.offset_x), low16(frame.target_x), 16)
            eligible = bool(frame.status & 5)
        if eligible:
            frame = _movement_move(state, frame, 'offset_y', frame.controller.word(low16(frame.distance)), 16)
            frame = store_ai_value_fields(state, frame, 0xFFFFF642, low16(frame.offset_y), 16)
            frame = _movement_fixed_shift_word(state, frame, 'offset_y', 4, True)
            frame = adjust_ai_carrier_fields(state, frame, 'offset_y', low16(frame.unit), subtract=True)
            if frame.status & 1:
                frame = _packet_policy_neg_fields(state, frame, 'offset_y')
            frame = adjust_ai_carrier_fields(state, frame, 'offset_x', low16(frame.offset_y))
            frame = _movement_compare(state, frame, low16(frame.offset_x), low16(frame.target_x), 16)
            eligible = bool(frame.status & 5)
        if eligible:
            saved = ('target_x', 'target_y', 'unit', 'count', 'choice')
            frame = _movement_save_longs(state, frame, saved)
            frame = _packet_policy_call_fields(state, frame, 0x6518, 0x34266)
            frame = _movement_restore_longs(state, frame, saved)
            frame = _movement_compare(state, frame, low16(frame.choice), state.read(0xFFFFF644, 2), 16)
            if not frame.status & 5:
                frame = _movement_move(state, frame, 'choice', state.read(0xFFFFF644, 2), 16)
                frame = store_ai_value_fields(state, frame, 0xFFFFF392, low16(frame.count), 16)
        frame = step_ai_count_fields(frame, 'count')
        if low16(frame.count) == 65535:
            return frame


def city_roster_full_carry_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34280: saved D0-D2/A0, original city+1 membership and ten-member gate."""
    frame = _movement_frame(state, frame)
    saved = ('target_x', 'target_y', 'unit', 'roster')
    frame = _movement_save_longs(state, frame, saved)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCC00).cursor())
    frame = _movement_move(state, frame, 'target_x', low16(frame.count), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', 1)
    frame = _movement_move(state, frame, 'target_y', 255, 16)
    frame = _movement_move(state, frame, 'unit', 0, 16)
    while True:
        frame = _movement_compare(state, frame, low8(frame.target_x), frame.roster.byte(low16(frame.target_y)), 8)
        if frame.status & 4:
            frame = adjust_ai_carrier_fields(state, frame, 'unit', 1)
        frame = step_ai_count_fields(frame, 'target_y')
        if low16(frame.target_y) == 65535:
            break
    frame = _movement_compare(state, frame, low16(frame.unit), 10, 16)
    full = not bool(frame.status & 1)
    frame = _movement_restore_longs(state, frame, saved)
    return _path_carry_fields(state, frame, int(full), 0x342B8 if full else 0x342AC)


def evaluate_transport_supply_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """342BE: original A050-based packed supply and actual coordinate reachability."""
    frame = _packet_policy_group_fields(state, _movement_frame(state, frame), 0xFFFFA050)
    frame = _packet_policy_packed_long_fields(state, frame, 'target_x', 5)
    frame = compare_ai_long_fields(state, frame, frame.target_x, 500)
    allows = not bool(frame.status & 1)
    if allows:
        frame = _packet_policy_call_fields(state, frame, 0x34300, 0x342EA)
        allows = not bool(frame.status & 1)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 5 if allows else 4, 16)


def reachable_transport_coordinate_carry_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34300: preserve NEG.B vs NEG.W and the original reversed BLS path gate."""
    frame = _movement_frame(state, frame)
    for carrier, source, destination in (('target_x', 0xFFFFF75C, 0xFFFFF63C), ('target_y', 0xFFFFF75E, 0xFFFFF63E)):
        frame = _movement_move(state, frame, carrier, state.read(source, 2), 16)
        frame = store_ai_value_fields(state, frame, destination, low16(frame.carrier(carrier)), 16)
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFF760, 2), 16)
    frame = first_replace(frame, roster=state.table_at(0xD4D22).cursor())
    while True:
        frame = _movement_move(state, frame, 'distance', 0, 16)
        frame = _movement_move(state, frame, 'distance', frame.roster.byte(), 8)
        if frame.status & 8:
            return _path_carry_fields(state, frame, 1, 0x34370)
        frame = store_ai_value_fields(state, frame, 0xFFFFF640, low16(frame.distance), 16)
        frame = adjust_ai_carrier_fields(state, frame, 'distance', low8(frame.target_x), 8, True)
        if frame.status & 1:
            frame = _packet_policy_neg_fields(state, frame, 'distance', 8)
        frame = _movement_compare(state, frame, low8(frame.distance), low8(frame.unit), 8)
        eligible = bool(frame.status & 5)
        if eligible:
            frame = _movement_move(state, frame, 'offset_x', 0, 16)
            frame = _movement_move(state, frame, 'offset_x', frame.roster.byte(0, 1), 8)
            frame = store_ai_value_fields(state, frame, 0xFFFFF642, low16(frame.offset_x), 16)
            frame = adjust_ai_carrier_fields(state, frame, 'offset_x', low8(frame.target_y), 8, True)
            if frame.status & 1:
                frame = _packet_policy_neg_fields(state, frame, 'offset_x')
            frame = adjust_ai_carrier_fields(state, frame, 'distance', low8(frame.offset_x), 8)
            frame = _movement_compare(state, frame, low8(frame.distance), low8(frame.unit), 8)
            eligible = bool(frame.status & 5)
        if eligible:
            saved = ('target_x', 'target_y', 'unit', 'roster')
            frame = _movement_save_longs(state, frame, saved)
            frame = _packet_policy_call_fields(state, frame, 0x651C, 0x34358)
            frame = _movement_restore_longs(state, frame, saved)
            frame = _movement_compare(state, frame, low16(frame.unit), state.read(0xFFFFF644, 2), 16)
            if frame.status & 5:
                return _path_carry_fields(state, frame, 0, 0x34368)
        frame = first_replace(frame, roster=frame.roster.advance(2))


def commit_staging_city_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34376: retain the search's live A0, commit only a nonnegative city."""
    frame = _packet_policy_call_fields(state, _movement_frame(state, frame), 0x343B0, 0x3437A)
    frame = _movement_test(state, frame, state.read(0xFFFFF392, 2), 16)
    if not frame.status & 8:
        address = 0xFFFFF392
        frame, value = _movement_binary_flags(state, frame, state.read(address, 2), 1, 16)
        state.write(address, 2, value)
        for slot, destination in ((3, 0xFFFFF744), (13, 0xFFFFF74A)):
            frame = _movement_move(state, frame, 'target_x', 0, 16)
            frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, slot), 8)
            frame = store_ai_value_fields(state, frame, destination, low16(frame.target_x), 16)
        frame = _packet_policy_call_fields(state, frame, 0x33CC8, 0x3439E)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 22, 16)


def choose_nearest_staging_city_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """343B0: first strictly-nearer owned nonfull city, original zero-based table."""
    frame = _packet_policy_group_fields(state, _movement_frame(state, frame))
    for carrier, slot, addresses in (('target_x', 1, (0xFFFFF63C,0xFFFFF746)), ('target_y', 2, (0xFFFFF63E,0xFFFFF748))):
        frame = _movement_move(state, frame, carrier, 0, 16)
        frame = _movement_move(state, frame, carrier, frame.roster.byte(0, slot), 8)
        frame = _movement_fixed_shift_word(state, frame, carrier, 4)
        for address in addresses:
            frame = store_ai_value_fields(state, frame, address, low16(frame.carrier(carrier)), 16)
        frame = _movement_fixed_shift_word(state, frame, carrier, 4, True)
    frame = _movement_move(state, frame, 'unit', 65535, 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF392, 65535, 16)
    frame = first_replace(frame, candidates=state.table_at(0xD4ACA).cursor(), controller=state.table_at(0xFFFFF428))
    frame = _movement_move(state, frame, 'count', 39, 16)
    while True:
        frame = _movement_move(state, frame, 'distance', 0, 16)
        frame = _movement_move(state, frame, 'distance', frame.controller.byte(low16(frame.count)), 8)
        frame = _movement_compare(state, frame, low8(frame.distance), state.read(0xFFFFF377, 1), 8)
        eligible = bool(frame.status & 4)
        if eligible:
            frame = _packet_policy_call_fields(state, frame, 0x34280, 0x34406)
            eligible = not bool(frame.status & 1)
        if eligible:
            frame = _movement_move(state, frame, 'offset_x', low16(frame.count), 16)
            frame = _movement_fixed_shift_word(state, frame, 'offset_x', 2)
            for carrier, displacement, source in (('offset_y',2,'target_x'), ('choice',0,'target_y')):
                frame = _movement_move(state, frame, carrier, frame.candidates.word(low16(frame.offset_x), displacement), 16)
                frame = _movement_fixed_shift_word(state, frame, carrier, 4, True)
                frame = adjust_ai_carrier_fields(state, frame, carrier, low16(frame.carrier(source)), subtract=True)
                if frame.status & 1:
                    frame = _packet_policy_neg_fields(state, frame, carrier)
            frame = adjust_ai_carrier_fields(state, frame, 'choice', low16(frame.offset_y))
            frame = _movement_compare(state, frame, low16(frame.choice), low16(frame.unit), 16)
            if frame.status & 1:
                frame = _movement_move(state, frame, 'unit', low16(frame.choice), 16)
                frame = store_ai_value_fields(state, frame, 0xFFFFF392, low16(frame.count), 16)
        frame = step_ai_count_fields(frame, 'count')
        if low16(frame.count) == 65535:
            return frame


def choose_destination_progress_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3443E: exact two independent coordinate comparisons, phase21 or20."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF640, 2), 16)
    frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF63C, 2), 16)
    reached = bool(frame.status & 4)
    if reached:
        frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF642, 2), 16)
        frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF63E, 2), 16)
        reached = bool(frame.status & 4)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 21 if reached else 20, 16)


def choose_terrain_exit_phase_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34468: four terrain reads short-circuit in original order before contact."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF75C, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', state.read(0xFFFFF75C, 2))
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', state.read(0xFFFFF75E, 2))
    frame = first_replace(frame, roster=state.table_at(0xEE5F0).cursor())
    near_water = False
    for displacement in (-72,-1,1,72):
        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x), displacement), 8)
        frame = _movement_compare(state, frame, low8(frame.target_y), 1, 8)
        if frame.status & 4:
            near_water = True
            break
    if near_water:
        frame = _packet_policy_call_fields(state, frame, 0x344C6, 0x344BC)
        if not frame.status & 1:
            return store_ai_value_fields(state, frame, 0xFFFFF728, 24, 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 13, 16)


def locate_packet_contact_city_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """344C6: backward rectangle search; original owner read even after exhaustion."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF75C, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', 8, subtract=True)
    frame = adjust_ai_carrier_fields(state, frame, 'target_y', 24)
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFF75E, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 4)
    frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', 16, subtract=True)
    frame = adjust_ai_carrier_fields(state, frame, 'count', 32)
    frame = first_replace(frame, roster=state.table_at(0xD4B66).cursor())
    frame = _movement_move(state, frame, 'distance', 39, 16)
    while True:
        frame = _movement_compare(state, frame, low16(frame.target_x), frame.roster.word(0,2), 16)
        in_rectangle = bool(frame.status & 5)
        if in_rectangle:
            frame = _movement_compare(state, frame, low16(frame.target_y), frame.roster.word(0,2), 16)
            in_rectangle = not bool(frame.status & 1)
        if in_rectangle:
            frame = _movement_compare(state, frame, low16(frame.unit), frame.roster.word(), 16)
            in_rectangle = bool(frame.status & 5)
        if in_rectangle:
            frame = _movement_compare(state, frame, low16(frame.count), frame.roster.word(), 16)
            if not frame.status & 1:
                break
        frame = first_replace(frame, roster=frame.roster.advance(-4))
        frame = step_ai_count_fields(frame, 'distance')
        if low16(frame.distance) == 65535:
            break
    frame = first_replace(frame, roster=state.table_at(0xFFFFF428).cursor())
    frame = _movement_move(state, frame, 'offset_x', frame.roster.byte(low16(frame.distance)), 8)
    frame = _movement_compare(state, frame, low8(frame.offset_x), state.read(0xFFFFF377,1), 8)
    if frame.status & 4:
        return _path_carry_fields(state, frame, 1, 0x34522)
    frame = _path_carry_fields(state, frame, 0, 0x3452A)
    frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 255, 16)
    frame = adjust_ai_carrier_fields(state, frame, 'distance', 1)
    return store_ai_value_fields(state, frame, 0xFFFFF392, low16(frame.distance), 16)


def choose_city_assault_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3453A: compare the actual second child's strength and readiness results."""
    frame = _packet_policy_call_fields(state, _movement_frame(state,frame), 0x34564, 0x3453E)
    frame = _packet_policy_call_fields(state, frame, 0x345C2, 0x34542)
    frame = compare_ai_long_fields(state, frame, frame.target_y, state.read(0xFFFFF744,4))
    retreat = not bool(frame.status & 1)
    if not retreat:
        frame = _movement_compare(state,frame,low16(frame.unit),state.read(0xFFFFF748,2),16)
        retreat = not bool(frame.status & 5)
    return store_ai_value_fields(state,frame,0xFFFFF728,13 if retreat else 12,16)


def measure_packet_ready_strength_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34564: two live troop reads per member, real MOVEM and capacity test."""
    frame = _movement_frame(state,frame)
    saved=('distance','controller','scan')
    frame = _movement_save_longs(state,frame,saved)
    frame = _packet_policy_group_fields(state,frame)
    frame = _movement_move(state,frame,'unit',frame.roster.byte(),8)
    frame = _movement_move(state,frame,'unit',low16(frame.unit)&15,16)
    frame = adjust_ai_carrier_fields(state,frame,'unit',1,subtract=True)
    frame = _movement_move_long(state,frame,'target_x',0)
    frame = _movement_move(state,frame,'target_y',0,16)
    frame = first_replace(frame,candidates=state.table_at(0xFFFFC800).cursor(),controller=state.table_at(0xFFFFB200),scan=state.table_at(0xFFFFB000).cursor())
    while True:
        frame = _movement_move(state,frame,'count',0,16)
        frame = _movement_move(state,frame,'count',frame.roster.byte(low16(frame.unit),13),8)
        frame = _movement_fixed_shift_word(state,frame,'count',2)
        frame = _movement_arithmetic_long(state,frame,'target_x',frame.candidates.long(low16(frame.count)))
        frame = compare_ai_long_fields(state,frame,frame.candidates.long(low16(frame.count)),5000)
        if not frame.status&1:
            frame = _movement_fixed_shift_word(state,frame,'count',1,True)
            frame = _movement_move(state,frame,'distance',frame.controller.word(low16(frame.count)),16)
            frame = _movement_compare(state,frame,low16(frame.distance),frame.scan.word(low16(frame.count)),16)
            if not frame.status&1:
                frame = adjust_ai_carrier_fields(state,frame,'target_y',1)
        frame = step_ai_count_fields(frame,'unit')
        if low16(frame.unit)==65535:
            break
    frame = store_ai_value_fields(state,frame,0xFFFFF744,frame.target_x,32)
    frame = store_ai_value_fields(state,frame,0xFFFFF748,low16(frame.target_y),16)
    return _movement_restore_longs(state,frame,saved)


def measure_chosen_city_strength_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """345C2: predecrement assignments from CD00; no preserved-register shortcut."""
    frame = _movement_frame(state,frame)
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame = first_replace(frame,roster=state.table_at(0xFFFFC800).cursor(),candidates=state.table_at(0xFFFFCD00).cursor())
    frame = _movement_move_long(state,frame,'target_y',0)
    frame = _movement_move(state,frame,'unit',0,16)
    frame = _movement_move(state,frame,'count',255,16)
    while True:
        frame = first_replace(frame,candidates=frame.candidates.advance(-1))
        frame = _movement_compare(state,frame,low8(frame.target_x),frame.candidates.byte(),8)
        if frame.status&4:
            frame = _movement_move(state,frame,'distance',low16(frame.count),16)
            frame = _movement_fixed_shift_word(state,frame,'distance',2)
            frame = _movement_arithmetic_long(state,frame,'target_y',frame.roster.long(low16(frame.distance)))
            frame = compare_ai_long_fields(state,frame,frame.roster.long(low16(frame.distance)),5000)
            if not frame.status&1:
                frame = adjust_ai_carrier_fields(state,frame,'unit',1)
        frame = step_ai_count_fields(frame,'count')
        if low16(frame.count)==65535:
            return frame


def choose_city_mask_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """345F8: original retained mask high WORD and WORD-shift/SWAP random gate."""
    frame = _movement_frame(state,frame)
    frame = first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame = _movement_move(state,frame,'target_y',0,16)
    frame = _movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    if not frame.status&8:
        frame = _movement_fixed_shift_word(state,frame,'target_y',1)
        frame = first_replace(frame,roster=state.table_at(0xFFFFE710).cursor())
        frame = _movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
        frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
        frame = adjust_ai_carrier_fields(state,frame,'target_x',1,subtract=True)
        frame = test_ai_register_bit_fields(state,frame,frame.target_y,frame.target_x)
        if not frame.status&4:
            frame = _packet_policy_call_fields(state,frame,0x83D4,0x34626)
            frame = _movement_move_long(state,frame,'target_x',frame.target_x&65535)
            frame = _movement_fixed_shift_word(state,frame,'target_x',2)
            frame = _movement_move_long(state,frame,'target_x',swap_words(frame.target_x))
            frame = _movement_test(state,frame,low16(frame.target_x),16)
            if not frame.status&4:
                return store_ai_value_fields(state,frame,0xFFFFF728,16,16)
    return store_ai_value_fields(state,frame,0xFFFFF728,9,16)


def choose_processed_city_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34648: live processed BYTE, phase10 when nonzero, otherwise7."""
    frame = _movement_frame(state,frame)
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame = first_replace(frame,roster=state.table_at(0xFFFFEA37).cursor())
    frame = _movement_test(state,frame,frame.roster.byte(low16(frame.target_x)),8)
    return store_ai_value_fields(state,frame,0xFFFFF728,10 if not frame.status&4 else 7,16)


def choose_linked_city_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3466A: exhaustive original search retains a genuine nonreturning boundary."""
    from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
    frame = _movement_frame(state,frame)
    frame = first_replace(frame,roster=state.table_at(0xFFFFA150).cursor())
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame = _movement_move(state,frame,'target_y',255,16)
    while True:
        frame = first_replace(frame,roster=frame.roster.advance(-1))
        frame = _movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(),8)
        if frame.status&4:
            break
        frame = step_ai_count_fields(frame,'target_y')
        if low16(frame.target_y)==65535:
            raise MovementContinuationBoundary(0x34680,frame,'original linked-city search exhausted into BRA self')
    frame = first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame = _movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_y)),8)
    frame = _movement_move(state,frame,'unit',low16(frame.unit)&63,16)
    frame = first_replace(frame,roster=state.table_at(0xFFFFF427).cursor())
    frame = _movement_move(state,frame,'unit',frame.roster.byte(low16(frame.unit)),8)
    frame = _movement_compare(state,frame,low8(frame.unit),state.read(0xFFFFF377,1),8)
    return store_ai_value_fields(state,frame,0xFFFFF728,11 if frame.status&4 else 13,16)


def choose_packet_resource_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """346B0: retain the original unconditional second MOVE that overwrites12."""
    frame = _packet_policy_call_fields(state,_movement_frame(state,frame),0x346C6,0x346B4)
    if not frame.status&1:
        frame = store_ai_value_fields(state,frame,0xFFFFF728,12,16)
    return store_ai_value_fields(state,frame,0xFFFFF728,13,16)


def packet_resource_shortfall_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """346C6: BYTE decrement then WORD DBRA; original capacity comparison order."""
    frame = _packet_policy_group_fields(state,_movement_frame(state,frame))
    frame = _movement_move(state,frame,'target_x',frame.roster.byte(),8)
    frame = _movement_move(state,frame,'target_x',low16(frame.target_x)&15,16)
    frame = adjust_ai_carrier_fields(state,frame,'target_x',1,8,True)
    frame = _movement_move_long(state,frame,'target_y',0)
    frame = first_replace(frame,candidates=state.table_at(0xFFFFB000).cursor(),controller=state.table_at(0xFFFFB200),scan=state.table_at(0xFFFFC800).cursor())
    while True:
        frame = _movement_move(state,frame,'unit',0,16)
        frame = _movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_x),13),8)
        frame = _movement_fixed_shift_word(state,frame,'unit',2)
        frame = _movement_arithmetic_long(state,frame,'target_y',frame.scan.long(low16(frame.unit)))
        frame = _movement_fixed_shift_word(state,frame,'unit',1,True)
        frame = _movement_move(state,frame,'count',frame.candidates.word(low16(frame.unit)),16)
        frame = _movement_compare(state,frame,low16(frame.count),frame.controller.word(low16(frame.unit)),16)
        if not frame.status&5:
            return _path_carry_fields(state,frame,1,0x34714)
        frame = step_ai_count_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame = compare_ai_long_fields(state,frame,frame.target_y,10000)
    return _path_carry_fields(state,frame,1 if frame.status&1 else 0,0x34714 if frame.status&1 else 0x3470C)


def choose_adjacent_group_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3487E: actual candidate list chooses phase14 or16."""
    frame = _packet_policy_call_fields(state,_movement_frame(state,frame),0x3489C,0x34882)
    frame = _movement_test(state,frame,state.read(0xFFFFD300,2),16)
    return store_ai_value_fields(state,frame,0xFFFFF728,16 if frame.status&8 else 14,16)


def collect_adjacent_hostile_groups_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3489C: retain the original per-record SWAP and its unusual D0 middle test."""
    frame = _movement_frame(state,frame)
    frame = first_replace(frame,roster=state.table_at(0xFFFF9000).cursor())
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF75A,2),16)
    frame = _movement_move(state,frame,'count',frame.roster.byte(low16(frame.target_x),2),8)
    frame = _movement_move(state,frame,'distance',low8(frame.count),8)
    frame = adjust_ai_carrier_fields(state,frame,'distance',1,8,True)
    frame = _movement_move(state,frame,'offset_x',low8(frame.count),8)
    frame = adjust_ai_carrier_fields(state,frame,'offset_x',1,8)
    frame = _movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_x),1),8)
    frame = _movement_move(state,frame,'target_y',low8(frame.target_x),8)
    frame = adjust_ai_carrier_fields(state,frame,'target_y',1,8,True)
    frame = _movement_move(state,frame,'unit',low8(frame.target_x),8)
    frame = adjust_ai_carrier_fields(state,frame,'unit',1,8)
    frame = first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame = _movement_move(state,frame,'choice',0,16)
    while True:
        frame = _movement_move(state,frame,'offset_y',frame.roster.byte(),8)
        frame = _movement_move(state,frame,'offset_y',low16(frame.offset_y)&15,16)
        if frame.status&4:
            return store_ai_value_fields(state,frame,frame.candidates.base,65535,16)
        frame = _movement_move_long(state,frame,'target_x',swap_words(frame.target_x))
        frame = _movement_move(state,frame,'target_x',frame.roster.byte(0,4),8)
        frame = _movement_compare(state,frame,low8(frame.target_x),state.read(0xFFFFF377,1),8)
        matched = False
        if not frame.status&4:
            frame = _movement_compare(state,frame,low8(frame.target_y),frame.roster.byte(0,1),8)
            if frame.status&4:
                frame = _movement_compare(state,frame,low8(frame.count),frame.roster.byte(0,2),8)
                matched = bool(frame.status&4)
            if not matched:
                frame = _movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(0,1),8)
                if frame.status&4:
                    frame = _movement_compare(state,frame,low8(frame.distance),frame.roster.byte(0,2),8)
                    matched = bool(frame.status&4)
                    if not matched:
                        frame = _movement_compare(state,frame,low8(frame.offset_x),frame.roster.byte(0,2),8)
                        matched = bool(frame.status&4)
            if not matched:
                frame = _movement_compare(state,frame,low8(frame.unit),frame.roster.byte(0,1),8)
                if frame.status&4:
                    frame = _movement_compare(state,frame,low8(frame.count),frame.roster.byte(0,2),8)
                    matched = bool(frame.status&4)
            if matched:
                frame = store_ai_value_fields(state,frame,frame.candidates.base,low16(frame.choice),16)
                frame = first_replace(frame,candidates=frame.candidates.advance(2))
        frame = first_replace(frame,roster=frame.roster.advance(s16(low16(frame.offset_y))+13))
        frame = adjust_ai_carrier_fields(state,frame,'offset_y',13)
        frame = adjust_ai_carrier_fields(state,frame,'choice',low16(frame.offset_y))


def choose_adjacent_strength_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3492E: original negative-selection and unsigned-strength gates."""
    frame = _packet_policy_call_fields(state,_movement_frame(state,frame),0x3495A,0x34932)
    frame = _packet_policy_call_fields(state,frame,0x34986,0x34936)
    frame = _movement_test(state,frame,low16(frame.target_x),16)
    selected = not bool(frame.status&8)
    if selected:
        frame = compare_ai_long_fields(state,frame,frame.target_y,state.read(0xFFFFF744,4))
        selected = bool(frame.status&1)
    if selected:
        frame = store_ai_value_fields(state,frame,0xFFFFF744,low16(frame.target_x),16)
        return store_ai_value_fields(state,frame,0xFFFFF728,15,16)
    return store_ai_value_fields(state,frame,0xFFFFF728,16,16)


def store_packet_strength_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3495A: reverse packet member sum, including zero-count DBRA underflow."""
    frame = _packet_policy_group_fields(state,_movement_frame(state,frame))
    frame = _movement_move_long(state,frame,'target_x',0)
    frame = _movement_move(state,frame,'target_y',frame.roster.byte(),8)
    frame = _movement_move(state,frame,'target_y',low16(frame.target_y)&15,16)
    frame = adjust_ai_carrier_fields(state,frame,'target_y',1,subtract=True)
    frame = first_replace(frame,candidates=state.table_at(0xFFFFC800).cursor())
    while True:
        frame = _movement_move(state,frame,'unit',0,16)
        frame = _movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_y),13),8)
        frame = _movement_fixed_shift_word(state,frame,'unit',2)
        frame = _movement_arithmetic_long(state,frame,'target_x',frame.candidates.long(low16(frame.unit)))
        frame = step_ai_count_fields(frame,'target_y')
        if low16(frame.target_y)==65535:
            return store_ai_value_fields(state,frame,0xFFFFF744,frame.target_x,32)


def select_largest_hostile_candidate_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34986: retain original -1 maximum seed and live alliance-mask high WORD."""
    frame = _movement_frame(state,frame)
    frame = first_replace(frame,roster=state.table_at(0xFFFFD300).cursor())
    frame = _movement_move(state,frame,'target_x',65535,16)
    frame = _movement_move_long(state,frame,'target_y',0xFFFFFFFF)
    frame = first_replace(frame,candidates=state.table_at(0xFFFFC800).cursor(),controller=state.table_at(0xFFFFE710))
    frame = _movement_move(state,frame,'choice',state.read(0xFFFFF376,2),16)
    frame = _movement_fixed_shift_word(state,frame,'choice',1)
    frame = _movement_move(state,frame,'choice',frame.controller.word(low16(frame.choice)),16)
    while True:
        value = frame.roster.word()
        frame = first_replace(frame,roster=frame.roster.advance(2))
        frame = _movement_move(state,frame,'unit',value,16)
        if frame.status&8:
            return frame
        frame = _packet_policy_call_fields(state,frame,0x349BA,0x349AC)
        if frame.status&1:
            continue
        frame = compare_ai_long_fields(state,frame,frame.distance,frame.target_y)
        if frame.status&5:
            continue
        frame = _movement_move_long(state,frame,'target_y',frame.distance)
        frame = _movement_move(state,frame,'target_x',low16(frame.unit),16)


def measure_unmasked_candidate_strength_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """349BA: dynamic register BTST followed by original packet sum and SR clear."""
    frame = _movement_frame(state,frame)
    frame = first_replace(frame,scan=state.table_at(0xFFFF9000).cursor().advance(s16(low16(frame.unit))))
    frame = _movement_move(state,frame,'count',frame.scan.byte(0,4),8)
    frame = test_ai_register_bit_fields(state,frame,frame.choice,frame.count)
    if not frame.status&4:
        return _path_carry_fields(state,frame,1,0x349EC)
    frame = _movement_move(state,frame,'count',frame.scan.byte(),8)
    frame = _movement_move(state,frame,'count',low16(frame.count)&15,16)
    frame = adjust_ai_carrier_fields(state,frame,'count',1,subtract=True)
    frame = _movement_move_long(state,frame,'distance',0)
    while True:
        frame = _movement_move(state,frame,'offset_x',0,16)
        frame = _movement_move(state,frame,'offset_x',frame.scan.byte(low16(frame.count),13),8)
        frame = _movement_fixed_shift_word(state,frame,'offset_x',2)
        frame = _movement_arithmetic_long(state,frame,'distance',frame.candidates.long(low16(frame.offset_x)))
        frame = step_ai_count_fields(frame,'count')
        if low16(frame.count)==65535:
            return _path_carry_fields(state,frame,0,0x349E4)


def queue_packet_stationary_command_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """349F2: original six-byte command packet, terminalFF and live queue WORD."""
    frame = _packet_policy_group_fields(state,_movement_frame(state,frame))
    frame = first_replace(frame,candidates=state.table_at(0x00FF3000).cursor().advance(s16(state.read(0x00FF3826,2))))
    for displacement in (None,13,3):
        value = 0 if displacement is None else frame.roster.byte(0,displacement)
        frame = store_ai_value_fields(state,frame,frame.candidates.base,value,8,displacement is None)
        frame = first_replace(frame,candidates=frame.candidates.advance(1))
    for value,clear in ((0x90,False),(0x32,False),(0,True)):
        frame = store_ai_value_fields(state,frame,frame.candidates.base,value,8,clear)
        frame = first_replace(frame,candidates=frame.candidates.advance(1))
    frame = store_ai_value_fields(state,frame,frame.candidates.base,255,8)
    frame,value = _movement_binary_flags(state,frame,state.read(0x00FF3826,2),6,16)
    state.write(0x00FF3826,2,value)
    return store_ai_value_fields(state,frame,0xFFFFF728,65535,16)


def choose_reachable_city_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34A2C: range, reachable candidates, complete readiness and lightest city."""
    frame = _packet_policy_call_fields(state,_movement_frame(state,frame),0x34A64,0x34A30)
    frame = _packet_policy_call_fields(state,frame,0x34AD0,0x34A34)
    frame = _movement_test(state,frame,state.read(0xFFFFD300,2),16)
    available = not bool(frame.status&8)
    if available:
        frame = _packet_policy_call_fields(state,frame,0x34564,0x34A40)
        frame = _movement_test(state,frame,low16(frame.target_y),16)
        available = not bool(frame.status&4)
    if available:
        frame = _packet_policy_call_fields(state,frame,0x34B58,0x34A4A)
        frame = _movement_test(state,frame,state.read(0xFFFFF392,2),16)
        available = not bool(frame.status&8)
    return store_ai_value_fields(state,frame,0xFFFFF728,17 if available else 18,16)


def packet_resource_range_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34A64: retained WORD price, packed food DIVU and original two-step cap."""
    frame = _packet_policy_group_fields(state,_movement_frame(state,frame))
    frame = _movement_move(state,frame,'target_x',frame.roster.byte(),8)
    frame = _movement_move(state,frame,'target_x',low16(frame.target_x)&15,16)
    frame = adjust_ai_carrier_fields(state,frame,'target_x',1,subtract=True)
    frame = _movement_move_long(state,frame,'target_y',0)
    frame = first_replace(frame,candidates=state.table_at(0xFFFFC800).cursor())
    while True:
        frame = _movement_move(state,frame,'unit',0,16)
        frame = _movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_x),13),8)
        frame = _movement_fixed_shift_word(state,frame,'unit',2)
        frame = _movement_arithmetic_long(state,frame,'target_y',frame.candidates.long(low16(frame.unit)))
        frame = _movement_arithmetic_long(state,frame,'target_y',100)
        frame = step_ai_count_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame = _movement_divu_word(state,frame,'target_y',10,0x34A90)
    frame = _movement_move(state,frame,'unit',low16(frame.target_y),16)
    frame = _movement_fixed_shift_word(state,frame,'target_y',1)
    frame = adjust_ai_carrier_fields(state,frame,'target_y',low16(frame.unit))
    frame = _packet_policy_packed_long_fields(state,frame,'target_x',9)
    frame = _movement_divu_word(state,frame,'target_x',low16(frame.target_y),0x34AB0)
    frame = _movement_test(state,frame,low16(frame.target_x),16)
    if frame.status&4:
        return frame
    frame = adjust_ai_carrier_fields(state,frame,'target_x',1,subtract=True)
    frame = _movement_compare(state,frame,low16(frame.target_x),2,16)
    if not frame.status&5:
        frame = _movement_move(state,frame,'target_x',2,16)
    frame = _movement_move(state,frame,'target_y',0,16)
    frame = _movement_move(state,frame,'target_y',frame.roster.byte(0,3),8)
    return _movement_multiply_word(state,frame,'target_x',low16(frame.target_y))


def _packet_candidate_negate_word_fields(state, frame, carrier):
    frame, value = _movement_binary_flags(state, frame, 0, low16(frame.carrier(carrier)), 16, True)
    return first_replace(frame, **{carrier: replace_word(frame.carrier(carrier), value)})


def collect_reachable_hostile_cities_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34AD0: descending city scan, eight-LONG path save and strict path range."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xD4B66).cursor())
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF75C, 2), 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF63C, low16(frame.target_y), 16)
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFF75E, 2), 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF63E, low16(frame.unit), 16)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFF450).cursor(),
        controller=state.table_at(0xFFFFD300).cursor(), scan=state.table_at(0xFFFFD400).cursor())
    frame = _movement_move(state, frame, 'count', 39, 16)
    while True:
        frame = first_replace(frame, candidates=frame.candidates.advance(-1))
        frame = _movement_move(state, frame, 'distance', frame.candidates.byte(), 8)
        frame = _movement_compare(state, frame, low8(frame.distance), state.read(0xFFFFF377, 1), 8)
        eligible = not bool(frame.status & 4)
        if eligible:
            frame = _movement_move(state, frame, 'distance', frame.roster.word(0, 2), 16)
            frame = _movement_fixed_shift_word(state, frame, 'distance', 4, True)
            frame = store_ai_value_fields(state, frame, 0xFFFFF640, low16(frame.distance), 16)
            frame = adjust_ai_carrier_fields(state, frame, 'distance', low16(frame.target_y), subtract=True)
            if frame.status & 1:
                frame = _packet_candidate_negate_word_fields(state, frame, 'distance')
            frame = _movement_compare(state, frame, low16(frame.distance), low16(frame.target_x), 16)
            eligible = bool(frame.status & 5)
        if eligible:
            frame = _movement_move(state, frame, 'offset_x', frame.roster.word(), 16)
            frame = _movement_fixed_shift_word(state, frame, 'offset_x', 4, True)
            frame = store_ai_value_fields(state, frame, 0xFFFFF642, low16(frame.offset_x), 16)
            frame = adjust_ai_carrier_fields(state, frame, 'offset_x', low16(frame.unit), subtract=True)
            if frame.status & 1:
                frame = _packet_candidate_negate_word_fields(state, frame, 'offset_x')
            frame = adjust_ai_carrier_fields(state, frame, 'distance', low16(frame.offset_x))
            frame = _movement_compare(state, frame, low16(frame.distance), low16(frame.target_x), 16)
            eligible = bool(frame.status & 5)
        if eligible:
            saved = ('target_x', 'target_y', 'unit', 'count', 'roster', 'candidates', 'controller', 'scan')
            frame = _movement_save_longs(state, frame, saved)
            frame = _packet_policy_call_fields(state, frame, 0x651C, 0x34B3A)
            frame = _movement_restore_longs(state, frame, saved)
            frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF644, 2), 16)
            if not frame.status & 5:
                frame = store_ai_value_fields(state, frame, frame.controller.base, low16(frame.count), 16)
                frame = first_replace(frame, controller=frame.controller.advance(2))
                frame = store_ai_value_fields(state, frame, frame.scan.base, state.read(0xFFFFF644, 2), 16)
                frame = first_replace(frame, scan=frame.scan.advance(2))
        frame = first_replace(frame, roster=frame.roster.advance(-4))
        frame = step_ai_count_fields(frame, 'count')
        if low16(frame.count) == 65535:
            return store_ai_value_fields(state, frame, frame.controller.base, 65535, 16)


def select_lightest_reachable_city_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34B58: strength minimum with a live distance tie-break and real city+1."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD300).cursor(),
        candidates=state.table_at(0xFFFFC800).cursor(), opponent=state.table_at(0xFFFFD3FE).cursor())
    frame = _movement_move_long(state, frame, 'choice', 0xFFFFFFFF)
    frame = store_ai_value_fields(state, frame, 0xFFFFF392, 65535, 16)
    frame = _movement_move(state, frame, 'offset_y', 65535, 16)
    while True:
        frame = first_replace(frame, opponent=frame.opponent.advance(2))
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'unit', value, 16)
        if frame.status & 8:
            return frame
        frame = _packet_policy_call_fields(state, frame, 0x34B98, 0x34B7C)
        frame = _movement_compare(state, frame, low16(frame.distance), low16(frame.target_y), 16)
        if not frame.status & 5:
            continue
        frame = compare_ai_long_fields(state, frame, frame.count, frame.choice)
        if not frame.status & 5:
            continue
        if frame.status & 4:
            frame = _movement_compare(state, frame, low16(frame.offset_y), frame.opponent.word(), 16)
            if frame.status & 5:
                continue
        frame = _movement_move(state, frame, 'offset_y', frame.opponent.word(), 16)
        frame = _movement_move_long(state, frame, 'choice', frame.count)
        frame = store_ai_value_fields(state, frame, 0xFFFFF392, low16(frame.unit), 16)


def measure_indexed_city_strength_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34B98: only D6.W is saved; its current high WORD must survive the pop."""
    frame = _movement_frame(state, frame)
    stack = frame.stack_cursor.advance(-2)
    frame = first_replace(frame, stack_cursor=stack)
    frame = store_ai_value_fields(state, frame, stack.base, low16(frame.offset_y), 16)
    frame = first_replace(frame, controller=state.table_at(0xFFFFC800).cursor())
    frame = _movement_move_long(state, frame, 'count', 0)
    frame = _movement_move(state, frame, 'distance', 0, 16)
    frame = first_replace(frame, scan=state.table_at(0xFFFFCD00).cursor())
    frame = _movement_move(state, frame, 'offset_x', 255, 16)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', 1)
    while True:
        frame = first_replace(frame, scan=frame.scan.advance(-1))
        frame = _movement_compare(state, frame, low8(frame.unit), frame.scan.byte(), 8)
        if frame.status & 4:
            frame = _movement_move(state, frame, 'offset_y', low16(frame.offset_x), 16)
            frame = _movement_fixed_shift_word(state, frame, 'offset_y', 2)
            frame = _movement_move_long(state, frame, 'offset_y', frame.controller.long(low16(frame.offset_y)))
            frame = _movement_arithmetic_long(state, frame, 'count', frame.offset_y)
            frame = compare_ai_long_fields(state, frame, frame.offset_y, 5000)
            if not frame.status & 1:
                frame = adjust_ai_carrier_fields(state, frame, 'distance', 1)
        frame = step_ai_count_fields(frame, 'offset_x')
        if low16(frame.offset_x) == 65535:
            break
    value = frame.stack_cursor.word()
    frame = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))
    return _movement_move(state, frame, 'offset_y', value, 16)


def queue_packet_march_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34BD0: retain the origin's high BYTE when loading the first member BYTE."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFF9000).cursor().advance(s16(state.read(0xFFFFF75A, 2))))
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 3), 8)
    frame = store_ai_value_fields(state, frame, 0xFFFFF744, low16(frame.target_x), 16)
    for source, destination in ((0xFFFFF75C, 0xFFFFF746), (0xFFFFF75E, 0xFFFFF748)):
        frame = _movement_move(state, frame, 'target_x', state.read(source, 2), 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)
        frame = store_ai_value_fields(state, frame, destination, low16(frame.target_x), 16)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 13), 8)
    frame = store_ai_value_fields(state, frame, 0xFFFFF74A, low16(frame.target_x), 16)
    frame = _packet_policy_call_fields(state, frame, 0x33CC8, 0x34C02)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 22, 16)


def choose_reachable_group_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34C0A: actual strength/list children choose phase19 unless no weaker group."""
    frame = _movement_frame(state, frame)
    frame = _packet_policy_call_fields(state, frame, 0x34C3E, 0x34C0E)
    frame = _movement_move(state, frame, 'target_x', 0, 16)
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 3), 8)
    frame = _packet_policy_call_fields(state, frame, 0x34C6A, 0x34C18)
    frame = _movement_test(state, frame, state.read(0xFFFFD300, 2), 16)
    if frame.status & 8:
        return store_ai_value_fields(state, frame, 0xFFFFF728, 4, 16)
    frame = _packet_policy_call_fields(state, frame, 0x34D0C, 0x34C24)
    frame = compare_ai_long_fields(state, frame, frame.target_x, state.read(0xFFFFF744, 4))
    return store_ai_value_fields(state, frame, 0xFFFFF728, 19 if frame.status & 5 else 4, 16)


def store_packet_comparison_strength_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34C3E: original inclusive wrapped roster sum and live LONG result slot."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFF9000).cursor().advance(s16(state.read(0xFFFFF75A, 2))))
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', 1, subtract=True)
    frame = _movement_move_long(state, frame, 'target_y', 0)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFC800).cursor())
    while True:
        frame = _movement_move(state, frame, 'unit', 0, 16)
        frame = _movement_move(state, frame, 'unit', frame.roster.byte(low16(frame.target_x), 13), 8)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
        frame = _movement_arithmetic_long(state, frame, 'target_y', frame.candidates.long(low16(frame.unit)))
        frame = step_ai_count_fields(frame, 'target_x')
        if low16(frame.target_x) == 65535:
            return store_ai_value_fields(state, frame, 0xFFFFF744, frame.target_y, 32)


def collect_reachable_hostile_groups_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34C6A: dynamic relation bits, BYTE-first delta and ten-LONG path save."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFF9000).cursor(),
        candidates=state.table_at(0xFFFFE710).cursor())
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF376, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_y)), 16)
    frame = _movement_move(state, frame, 'offset_x', state.read(0xFFFFF75C, 2), 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF63C, low16(frame.offset_x), 16)
    frame = _movement_move(state, frame, 'offset_y', state.read(0xFFFFF75E, 2), 16)
    frame = store_ai_value_fields(state, frame, 0xFFFFF63E, low16(frame.offset_y), 16)
    frame = _movement_move(state, frame, 'choice', 0, 16)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFD300).cursor())
    while True:
        frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)
        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 15, 16)
        if frame.status & 4:
            return store_ai_value_fields(state, frame, frame.candidates.base, 65535, 16)
        frame = _movement_move(state, frame, 'count', 0, 16)
        frame = _movement_move(state, frame, 'count', frame.roster.byte(0, 4), 8)
        frame = _movement_compare(state, frame, low16(frame.count), state.read(0xFFFFF376, 2), 16)
        eligible = not bool(frame.status & 4)
        if eligible:
            frame = test_ai_register_bit_fields(state, frame, frame.target_y, frame.count)
            eligible = bool(frame.status & 4)
        if eligible:
            frame = _movement_move(state, frame, 'count', 0, 16)
            frame = _movement_move(state, frame, 'count', frame.roster.byte(0, 1), 8)
            frame = store_ai_value_fields(state, frame, 0xFFFFF640, low16(frame.count), 16)
            frame = adjust_ai_carrier_fields(state, frame, 'count', low8(frame.offset_x), 8, True)
            if frame.status & 1:
                frame = _packet_candidate_negate_word_fields(state, frame, 'count')
            frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_x), 16)
            eligible = bool(frame.status & 5)
        if eligible:
            frame = _movement_move(state, frame, 'distance', 0, 16)
            frame = _movement_move(state, frame, 'distance', frame.roster.byte(0, 2), 8)
            frame = store_ai_value_fields(state, frame, 0xFFFFF642, low16(frame.distance), 16)
            frame = adjust_ai_carrier_fields(state, frame, 'distance', low16(frame.offset_y), subtract=True)
            if frame.status & 1:
                frame = _packet_candidate_negate_word_fields(state, frame, 'distance')
            frame = adjust_ai_carrier_fields(state, frame, 'count', low16(frame.distance))
            frame = _movement_compare(state, frame, low16(frame.count), low16(frame.target_x), 16)
            eligible = bool(frame.status & 5)
        if eligible:
            saved = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', 'choice', 'roster', 'candidates')
            frame = _movement_save_longs(state, frame, saved)
            frame = _packet_policy_call_fields(state, frame, 0x651C, 0x34CEC)
            frame = _movement_restore_longs(state, frame, saved)
            frame = _movement_compare(state, frame, low16(frame.target_x), state.read(0xFFFFF644, 2), 16)
            if not frame.status & 1:
                frame = store_ai_value_fields(state, frame, frame.candidates.base, low16(frame.choice), 16)
                frame = first_replace(frame, candidates=frame.candidates.advance(2))
        frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.unit)) + 13))
        frame = adjust_ai_carrier_fields(state, frame, 'unit', 13)
        frame = adjust_ai_carrier_fields(state, frame, 'choice', low16(frame.unit))


def select_lightest_group_candidate_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34D0C: ties retain the first choice; empty input retains incoming D5.W."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFFD300).cursor())
    frame = _movement_move_long(state, frame, 'target_x', 0xFFFFFFFF)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFC800).cursor())
    while True:
        value = frame.roster.word()
        frame = first_replace(frame, roster=frame.roster.advance(2))
        frame = _movement_move(state, frame, 'target_y', value, 16)
        if frame.status & 8:
            return store_ai_value_fields(state, frame, 0xFFFFF748, low16(frame.offset_x), 16)
        frame = _packet_policy_call_fields(state, frame, 0x34D30, 0x34D20)
        frame = compare_ai_long_fields(state, frame, frame.distance, frame.target_x)
        if frame.status & 1:
            frame = _movement_move_long(state, frame, 'target_x', frame.distance)
            frame = _movement_move(state, frame, 'offset_x', low16(frame.target_y), 16)


def measure_group_candidate_strength_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34D30: ANDI.B deliberately retains D2's high BYTE before WORD DBRA."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, controller=state.table_at(0xFFFF9000).cursor().advance(s16(low16(frame.target_y))))
    frame = _movement_move(state, frame, 'unit', frame.controller.byte(), 8)
    frame = _movement_move(state, frame, 'unit', low8(frame.unit) & 15, 8)
    frame = adjust_ai_carrier_fields(state, frame, 'unit', 1, subtract=True)
    frame = _movement_move_long(state, frame, 'distance', 0)
    while True:
        frame = _movement_move(state, frame, 'count', 0, 16)
        frame = _movement_move(state, frame, 'count', frame.controller.byte(low16(frame.unit), 13), 8)
        frame = _movement_fixed_shift_word(state, frame, 'count', 2)
        frame = _movement_arithmetic_long(state, frame, 'distance', frame.candidates.long(low16(frame.count)))
        frame = step_ai_count_fields(frame, 'unit')
        if low16(frame.unit) == 65535:
            return frame


def _packet_supply_load_amount_fields(state, frame, carrier, first_slot):
    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first_slot), 8)
    frame = _movement_fixed_shift_word(state, frame, carrier, 8)
    frame = _movement_move(state, frame, carrier, frame.roster.byte(0, first_slot + 1), 8)
    for slot in (first_slot + 2, first_slot + 3):
        frame = _movement_shift_long(state, frame, carrier)
        frame = _movement_move(state, frame, carrier, frame.roster.byte(0, slot), 8)
    return frame


def _packet_supply_store_amount_fields(state, frame, carrier, first_slot):
    frame = store_ai_value_fields(state, frame, frame.roster.address(0, first_slot + 3), low8(frame.carrier(carrier)), 8)
    for slot in (first_slot + 2, first_slot + 1):
        frame = _movement_shift_long(state, frame, carrier, True)
        frame = store_ai_value_fields(state, frame, frame.roster.address(0, slot), low8(frame.carrier(carrier)), 8)
    frame = _movement_fixed_shift_word(state, frame, carrier, 8, True)
    return store_ai_value_fields(state, frame, frame.roster.address(0, first_slot), low8(frame.carrier(carrier)), 8)


def _packet_supply_shift_two_fields(state, frame, carrier):
    """Actual LSL.L #2, including the second outgoing bit and full LONG lane."""
    original = frame.carrier(carrier)
    value = u32(original << 2)
    status = (17 if original & 0x40000000 else 0) | (8 if value & 0x80000000 else 0) | (4 if value == 0 else 0)
    state.sr = state.sr & 65504 | status
    return first_replace(frame, **{carrier: value}, status=status)


def purchase_packet_supplies_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34DCE: four real purchases followed by original reverse cash writeback."""
    frame = _movement_frame(state, frame)
    for target, continuation in ((0x34DFC, 0x34DD2), (0x34E1C, 0x34DD6),
            (0x34E5C, 0x34DDA), (0x34EB6, 0x34DDE)):
        frame = _packet_policy_call_fields(state, frame, target, continuation)
    frame = _packet_supply_store_amount_fields(state, frame, 'choice', 5)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 65535, 16)


def load_packet_cash_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34DFC: signed active packet displacement and W8/L8/L8 cash loading."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0xFFFF9000).cursor())
    frame = first_replace(frame, roster=frame.roster.advance(s16(state.read(0xFFFFF75A, 2))))
    return _packet_supply_load_amount_fields(state, frame, 'choice', 5)


def fill_packet_troop_deficits_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34E1C: backward inclusive member loop, immediate debit and exact refund."""
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFB000).cursor(),
        controller=state.table_at(0xFFFFB200).cursor())
    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_y', 1, subtract=True)
    while True:
        frame = _movement_move(state, frame, 'unit', 0, 16)
        frame = _movement_move(state, frame, 'unit', frame.roster.byte(low16(frame.target_y), 13), 8)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
        frame = _movement_move(state, frame, 'count', frame.candidates.word(low16(frame.unit)), 16)
        frame = adjust_ai_carrier_fields(state, frame, 'count', frame.controller.word(low16(frame.unit)), subtract=True)
        if not frame.status & 4:
            frame = _movement_move(state, frame, 'distance', low16(frame.count), 16)
            frame = _movement_multiply_word(state, frame, 'distance', 50)
            frame = _movement_arithmetic_long(state, frame, 'choice', frame.distance, True)
            if frame.status & 1:
                return _movement_arithmetic_long(state, frame, 'choice', frame.distance)
            address = frame.controller.address(low16(frame.unit))
            previous = state.read(address, 2)
            frame, increased = _movement_binary_flags(state, frame, previous, low16(frame.count), 16)
            state.write(address, 2, increased)
        frame = step_ai_count_fields(frame, 'target_y')
        if low16(frame.target_y) == 65535:
            return frame


def buy_packet_food_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34E5C: current group quote, signed-divmod child and retained DIVU lanes."""
    frame = _movement_frame(state, frame)
    frame = _packet_policy_call_fields(state, frame, 0x3417A, 0x34E60)
    frame = _movement_move_long(state, frame, 'count', frame.unit)
    frame = _movement_move_long(state, frame, 'distance', frame.unit)
    frame = _packet_supply_shift_two_fields(state, frame, 'count')
    frame = _movement_arithmetic_long(state, frame, 'count', frame.unit)
    frame = _packet_supply_shift_two_fields(state, frame, 'count')
    frame = _movement_move_long(state, frame, 'target_y', frame.choice)
    frame = shift_ai_long_fields(state, frame, 'target_y', 3)
    frame = _movement_move_long(state, frame, 'unit', 10)
    frame = _packet_policy_call_fields(state, frame, 0x35760, 0x34E76)
    frame = _movement_divu_word(state, frame, 'target_y', low16(frame.count), 0x34E76)
    frame = _movement_test(state, frame, low16(frame.target_y), 16)
    if frame.status & 4:
        return frame
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_y), 16)
    frame = _movement_multiply_word(state, frame, 'target_y', low16(frame.distance))
    frame = _packet_supply_load_amount_fields(state, frame, 'unit', 9)
    frame = _movement_arithmetic_long(state, frame, 'unit', frame.target_y)
    frame = _packet_supply_store_amount_fields(state, frame, 'unit', 9)
    frame = _movement_multiply_word(state, frame, 'target_x', low16(frame.count))
    return _movement_arithmetic_long(state, frame, 'choice', frame.target_x, True)


def buy_packet_equipment_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34EB6: keep the original B400 destination even though A1 selects EA88.

    Price is a live original D2EA LONG source and is independently reread for
    each subtraction and admission comparison. No corrected item table is used.
    """
    frame = _movement_frame(state, frame)
    frame = compare_ai_long_fields(state, frame, frame.choice, state.read(0xD2EA, 4))
    if frame.status & 1:
        return frame
    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = adjust_ai_carrier_fields(state, frame, 'target_x', 1, subtract=True)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFEA88).cursor(),
        controller=state.table_at(0xFFFFB400).cursor())
    while True:
        frame = _movement_move(state, frame, 'target_y', 0, 16)
        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x), 13), 8)
        frame = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)
        frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
        frame = _movement_compare(state, frame, frame.controller.word(low16(frame.target_y)), 100, 16)
        if not frame.status & 1:
            frame = adjust_ai_carrier_fields(state, frame, 'target_y', low16(frame.unit))
            frame = store_ai_value_fields(state, frame, frame.controller.address(low16(frame.target_y)), 4, 8)
            frame = _movement_arithmetic_long(state, frame, 'choice', state.read(0xD2EA, 4), True)
            frame = compare_ai_long_fields(state, frame, frame.choice, state.read(0xD2EA, 4))
            if frame.status & 1:
                return frame
        frame = step_ai_count_fields(frame, 'target_x')
        if low16(frame.target_x) == 65535:
            return frame


def clear_packet_supply_command_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34F02: the original WORD phase terminator without other field changes."""
    frame = _movement_frame(state, frame)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 65535, 16)


def choose_packet_readiness_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """34F0A: real strength child and low-WORD TST select phase4 or8."""
    frame = _movement_frame(state, frame)
    frame = _packet_policy_call_fields(state, frame, 0x34564, 0x34F0E)
    frame = _movement_test(state, frame, low16(frame.target_y), 16)
    return store_ai_value_fields(state, frame, 0xFFFFF728, 4 if frame.status & 4 else 8, 16)


REAL_CALL_PAIRS = ((213370, 213324), (213454, 213428), (213632, 213538), (25880, 213606), (213760, 213738), (25884, 213848), (213936, 213882), (212168, 213918), (213632, 214022), (214214, 214204), (214372, 214334), (214466, 214338), (33748, 214566), (214726, 214708), (215196, 215170), (215386, 215346), (215430, 215350), (215482, 215468), (215652, 215600), (215760, 215604), (214372, 215616), (215896, 215626), (25884, 215866), (215960, 215932), (212168, 216066), (216126, 216078), (216170, 216088), (216332, 216100), (25884, 216300), (216368, 216352), (216572, 216530), (216604, 216534), (216668, 216538), (216758, 216542), (213370, 216672), (218976, 216694), (214372, 216846))



def _packet_policy_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Only original second-family CALLs own a real LONG; no outer slot added."""
    if (target, continuation) not in REAL_CALL_PAIRS:
        raise ValueError('actual complete packet-policy CALL/return pair required')
    frame = _movement_frame(state, frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target == 0x83D4:
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        returned = first_deployment_random_fields(BattlePolicyMemory(state), entered)
    elif target in (0x6518, 0x651C, 0x35760):
        from ..high_level_main_flows.business_movement_support import build_path_fields, build_path_from_cells_fields, signed_divmod_fields
        child = {0x6518: build_path_fields, 0x651C: build_path_from_cells_fields, 0x35760: signed_divmod_fields}[target]
        returned = child(state, entered)
    elif target == 0x33CC8:
        from .business_scene_routes import build_ai_movement_packet_fields
        returned = build_ai_movement_packet_fields(state, entered)
    else:
        returned = execute_packet_policy_fields(state, entered, target)
    returned = _movement_frame(state, returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, returned, continuation)
    state.sr = state.sr & 65504 | returned.status
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))


def execute_packet_policy_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int) -> FirstDeploymentFrame:
    """Closed named second-directory owners; existing mature cores stay unique."""
    frame = _movement_frame(state, frame)
    if target == 214810:
        from ..high_level_remaining_flows.business_highbank import remove_command_object_members_fields
        return remove_command_object_members_fields(state, frame)
    if target == 214842:
        from ..high_level_remaining_flows.business_highbank import count_linked_force_officers_fields
        return count_linked_force_officers_fields(state, frame)
    if target == 214906:
        from ..high_level_remaining_flows.business_highbank import build_limited_packet_roster_fields
        return build_limited_packet_roster_fields(state, frame)
    if target == 215006:
        from ..high_level_remaining_flows.business_highbank import rank_packet_roster_fields
        return rank_packet_roster_fields(state, frame)
    if target == 215124:
        from ..high_level_remaining_flows.business_highbank import partition_ranked_packet_roster_fields
        return partition_ranked_packet_roster_fields(state, frame)
    if target == 215152:
        from ..high_level_remaining_flows.business_highbank import tail_remove_selected_object_member_fields
        return tail_remove_selected_object_member_fields(state, frame)
    if target == 216402:
        from ..high_level_remaining_flows.business_highbank import load_command_object_route_fields
        return load_command_object_route_fields(state, frame)
    if target == 216482:
        from ..high_level_remaining_flows.business_highbank import load_command_object_status_fields
        return load_command_object_status_fields(state, frame)
    owners = {213312: evaluate_packed_group_supply_phase_fields, 213370: price_packed_group_fields, 213424: choose_group_destination_phase_fields, 213454: choose_ai_destination_fields, 213632: city_roster_full_carry_fields, 213694: evaluate_transport_supply_phase_fields, 213760: reachable_transport_coordinate_carry_fields, 213878: commit_staging_city_phase_fields, 213936: choose_nearest_staging_city_fields, 214078: choose_destination_progress_phase_fields, 214120: choose_terrain_exit_phase_fields, 214214: locate_packet_contact_city_fields, 214330: choose_city_assault_action_fields, 214372: measure_packet_ready_strength_fields, 214466: measure_chosen_city_strength_fields, 214520: choose_city_mask_action_fields, 214600: choose_processed_city_action_fields, 214634: choose_linked_city_action_fields, 214704: choose_packet_resource_action_fields, 214726: packet_resource_shortfall_fields, 215166: choose_adjacent_group_action_fields, 215196: collect_adjacent_hostile_groups_fields, 215342: choose_adjacent_strength_action_fields, 215386: store_packet_strength_fields, 215430: select_largest_hostile_candidate_fields, 215482: measure_unmasked_candidate_strength_fields, 215538: queue_packet_stationary_command_fields, 215596: choose_reachable_city_action_fields, 215652: packet_resource_range_fields, 215760: collect_reachable_hostile_cities_fields, 215896: select_lightest_reachable_city_fields, 215960: measure_indexed_city_strength_fields, 216016: queue_packet_march_action_fields, 216074: choose_reachable_group_action_fields, 216126: store_packet_comparison_strength_fields, 216170: collect_reachable_hostile_groups_fields, 216332: select_lightest_group_candidate_fields, 216368: measure_group_candidate_strength_fields, 216526: purchase_packet_supplies_fields, 216572: load_packet_cash_fields, 216604: fill_packet_troop_deficits_fields, 216668: buy_packet_food_fields, 216758: buy_packet_equipment_fields, 216834: clear_packet_supply_command_fields, 216842: choose_packet_readiness_action_fields}
    if target not in owners:
        raise ValueError('target outside complete second packet-policy family')
    return owners[target](state, frame)
