"""Live city equipment and troop resupply, preserving original quirks.

confirmed: whole3363C..33764,33770..338C2 owners in recovered_code.s and
direct_descendants.s. Names follow mature economy/roster business policies;
every live carrier, memory access and real CALL slot is additionally retained.
Equipment category/price bytes are supplied as external owned source data.
"""
from ..high_level_scene_flows.domain import SceneState, low8, low16, divu_retained
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test,
    _movement_compare, _movement_fixed_shift_word, _movement_multiply_word,
    _movement_binary_flags, _path_carry_fields,
)
from ..high_level_ai_decision.scene_fields import (
    store_ai_value_fields, adjust_ai_carrier_fields, compare_ai_long_fields,
)


def _resupply_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """Six original nested calls, never an extra dispatcher return slot."""
    if (target, continuation) not in (
            (0x33666,0x3365A),(0x336D6,0x3365E),(0x33790,0x33774),
            (0x33666,0x3377C),(0x337C6,0x33780),(0x3382E,0x33788)):
        raise ValueError('actual city resupply CALL pair required')
    frame = _movement_frame(state,frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0,continuation)
    entered = first_replace(frame,stack_cursor=stack)
    if target == 0x33666:
        result = sort_equipment_roster_fields(state,entered)
    elif target == 0x336D6:
        result = purchase_roster_equipment_fields(state,entered)
    elif target == 0x33790:
        result = ai_recruitment_capacity_gate_fields(state,entered)
    elif target == 0x337C6:
        result = distribute_existing_troop_pool_fields(state,entered)
    else:
        result = buy_and_distribute_troops_fields(state,entered)
    result = _movement_frame(state,result)
    returned = result.stack_cursor.long()
    if returned != continuation:
        raise FirstDeploymentReturnBoundary(returned,result,continuation)
    return first_replace(result,stack_cursor=result.stack_cursor.advance(4))


def _resupply_add_memory_long_fields(state: SceneState,frame: FirstDeploymentFrame,
        address: int,value: int) -> FirstDeploymentFrame:
    """Original ADD.L memory RMW, including its fresh destination read/X."""
    previous = state.read(address,4)
    frame,result = _movement_binary_flags(state,frame,previous,value,32,False)
    state.write(address,4,result)
    return frame


def plan_equipment_action_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3363C: only an unacted live city head starts sort/purchase; advance10."""
    frame = _movement_frame(state,frame)
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame = _movement_fixed_shift_word(state,frame,'target_x',1)
    frame = first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
    frame = _movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
    frame = first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame = _movement_test(state,frame,frame.roster.byte(low16(frame.target_x)),8)
    if frame.status & 4:
        frame = _resupply_call_fields(state,frame,0x33666,0x3365A)
        frame = _resupply_call_fields(state,frame,0x336D6,0x3365E)
    return store_ai_value_fields(state,frame,0xFFFFF728,10,16)


def sort_equipment_roster_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33666: live descending-attribute bubble sort of WORD roster/work pairs.

    Exactly count==1 returns early. The original empty-roster behavior is not
    changed into a <=1 guard. Every swap rereads source operands in order.
    """
    frame = _movement_frame(state,frame)
    frame = first_replace(frame,roster=state.table_at(0xFFFFF72A).cursor())
    frame = first_replace(frame,candidates=state.table_at(0xFFFFB400).cursor())
    frame = first_replace(frame,controller=state.table_at(0xFFFFD300))
    frame = _movement_move(state,frame,'target_x',0,16)
    while True:
        officer = frame.roster.word()
        frame = first_replace(frame,roster=frame.roster.advance(2))
        frame = _movement_move(state,frame,'target_y',officer,16)
        if frame.status & 8:
            break
        frame = _movement_move(state,frame,'target_y',low16(frame.target_y)&255,16)
        frame = _movement_fixed_shift_word(state,frame,'target_y',1)
        value = frame.candidates.word(low16(frame.target_y))
        frame = store_ai_value_fields(state,frame,frame.controller.base,value,16)
        frame = first_replace(frame,controller=frame.controller.advance(2))
        frame = adjust_ai_carrier_fields(state,frame,'target_x',1)
    frame = _movement_compare(state,frame,low16(frame.target_x),1,16)
    if frame.status & 4:
        return frame
    frame = _movement_fixed_shift_word(state,frame,'target_x',1)
    frame = first_replace(frame,controller=state.table_at(0xFFFFD300))
    frame = first_replace(frame,roster=state.table_at(0xFFFFF72A).cursor())
    while True:
        frame = _movement_move(state,frame,'target_y',2,16)
        while True:
            index = low16(frame.target_y)
            frame = _movement_move(state,frame,'unit',frame.controller.word(index,-2),16)
            frame = _movement_compare(state,frame,low16(frame.unit),frame.controller.word(index),16)
            if frame.status & 1:
                frame = _movement_move(state,frame,'unit',frame.controller.word(index),16)
                frame = store_ai_value_fields(state,frame,frame.controller.address(index),frame.controller.word(index,-2),16)
                frame = store_ai_value_fields(state,frame,frame.controller.address(index,-2),low16(frame.unit),16)
                frame = _movement_move(state,frame,'unit',frame.roster.word(index),16)
                frame = store_ai_value_fields(state,frame,frame.roster.address(index),frame.roster.word(index,-2),16)
                frame = store_ai_value_fields(state,frame,frame.roster.address(index,-2),low16(frame.unit),16)
            frame = adjust_ai_carrier_fields(state,frame,'target_y',2)
            frame = _movement_compare(state,frame,low16(frame.target_y),low16(frame.target_x),16)
            if not frame.status & 1:
                break
        frame = adjust_ai_carrier_fields(state,frame,'target_x',2,subtract=True)
        frame = _movement_compare(state,frame,low16(frame.target_x),2,16)
        if frame.status & 5:
            return frame


def purchase_roster_equipment_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """336D6: per-member first quote, retained level prefix, final gold write.

    Original33758 writes category-only EA88+category, not member-row+category.
    A rejected quote skips to the next member, not a later category. D5.W's
    upper BYTE persists across every category/member; it is not normalized.
    """
    frame = _movement_frame(state,frame)
    frame = first_replace(frame,roster=state.table_at(0xFFFFF72A).cursor())
    frame = first_replace(frame,candidates=state.table_at(0xFFFFB400).cursor())
    frame = first_replace(frame,controller=state.table_at(0xFFFFDFFC))
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame = _movement_fixed_shift_word(state,frame,'target_x',2)
    frame = _movement_move_long(state,frame,'target_y',frame.controller.long(low16(frame.target_x)))
    frame = first_replace(frame,opponent=state.table_at(0xFFFFEA88))
    while True:
        officer = frame.roster.word()
        frame = first_replace(frame,roster=frame.roster.advance(2))
        frame = _movement_move(state,frame,'unit',officer,16)
        if frame.status & 8:
            break
        frame = _movement_move(state,frame,'unit',low16(frame.unit)&255,16)
        frame = _movement_fixed_shift_word(state,frame,'unit',1)
        frame = _movement_move(state,frame,'count',frame.candidates.word(low16(frame.unit)),16)
        frame = _movement_move(state,frame,'distance',0,16)
        frame = _movement_compare(state,frame,low16(frame.count),100,16)
        if frame.status & 1:
            frame = adjust_ai_carrier_fields(state,frame,'distance',4)
            frame = _movement_compare(state,frame,low16(frame.count),60,16)
            if frame.status & 1:
                frame = adjust_ai_carrier_fields(state,frame,'distance',4)
        frame = first_replace(frame,scan=state.table_at(0x33764).cursor())
        frame = first_replace(frame,scan=frame.scan.at(low16(frame.distance)).cursor())
        frame = _movement_move(state,frame,'count',low16(frame.unit),16)
        frame = _movement_fixed_shift_word(state,frame,'count',1,True)
        frame = adjust_ai_carrier_fields(state,frame,'count',low16(frame.unit))
        frame = _movement_move(state,frame,'distance',0,16)
        while True:
            category = frame.scan.byte()
            frame = first_replace(frame,scan=frame.scan.advance(1))
            frame = _movement_move(state,frame,'distance',category,8)
            if frame.status & 8:
                break
            frame = _movement_move(state,frame,'choice',low16(frame.distance),16)
            frame = adjust_ai_carrier_fields(state,frame,'choice',low16(frame.count))
            frame = _movement_move(state,frame,'offset_x',frame.opponent.byte(low16(frame.choice)),8)
            frame = _movement_compare(state,frame,low16(frame.offset_x),3,16)
            if not frame.status & 1:
                continue
            frame = _movement_move(state,frame,'offset_y',low16(frame.distance),16)
            frame = _movement_fixed_shift_word(state,frame,'offset_y',1)
            frame = adjust_ai_carrier_fields(state,frame,'offset_y',low16(frame.distance))
            frame = adjust_ai_carrier_fields(state,frame,'offset_y',low16(frame.offset_x))
            frame = adjust_ai_carrier_fields(state,frame,'offset_x',1)
            frame = _movement_fixed_shift_word(state,frame,'offset_y',2)
            frame = first_replace(frame,scratch=state.table_at(0xD2CA))
            frame = _movement_move_long(state,frame,'offset_y',frame.scratch.long(low16(frame.offset_y)))
            frame = _movement_move_long(state,frame,'choice',frame.target_y)
            # This original LSR.L #2 also changes X/C, not only the quotient.
            frame = _resupply_shift_two_long_fields(state,frame,'choice')
            frame = compare_ai_long_fields(state,frame,frame.offset_y,frame.choice)
            if not frame.status & 5:
                break
            frame = adjust_ai_carrier_fields(state,frame,'target_y',frame.offset_y,32,True)
            frame = store_ai_value_fields(state,frame,frame.opponent.address(low16(frame.distance)),low8(frame.offset_x),8)
            break
    return store_ai_value_fields(state,frame,frame.controller.address(low16(frame.target_x)),frame.target_y,32)


def _resupply_shift_two_long_fields(state: SceneState,frame: FirstDeploymentFrame,
        carrier: str) -> FirstDeploymentFrame:
    """Original33750 LSR.L #2: full LONG lanes and last shifted-out bit."""
    if carrier != 'choice':
        raise ValueError('actual equipment-budget LONG carrier required')
    original = frame.choice
    value = original >> 2
    carry = bool(original & 2)
    status = (17 if carry else 0) | (8 if value & 0x80000000 else 0) | (4 if value == 0 else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame,choice=value,status=status)


def plan_troop_purchase_action_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33770: original moving-EA gate, equipment sort, pool then purchase."""
    frame = _movement_frame(state,frame)
    frame = _resupply_call_fields(state,frame,0x33790,0x33774)
    if not frame.status & 1:
        frame = _resupply_call_fields(state,frame,0x33666,0x3377C)
        frame = _resupply_call_fields(state,frame,0x337C6,0x33780)
        if not frame.status & 1:
            frame = _resupply_call_fields(state,frame,0x3382E,0x33788)
    return store_ai_value_fields(state,frame,0xFFFFF728,11,16)


def ai_recruitment_capacity_gate_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """33790: preserve original337B2 moving roster EA, not the loaded C800."""
    frame = _movement_frame(state,frame)
    frame = first_replace(frame,roster=state.table_at(0xFFFFF72A).cursor())
    frame = first_replace(frame,candidates=state.table_at(0xFFFFC800).cursor())
    frame = first_replace(frame,controller=state.table_at(0xFFFFB800))
    while True:
        officer = frame.roster.word()
        frame = first_replace(frame,roster=frame.roster.advance(2))
        frame = _movement_move(state,frame,'target_x',officer,16)
        if frame.status & 8:
            return _path_carry_fields(state,frame,1,0x337C0)
        frame = _movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
        frame = _movement_fixed_shift_word(state,frame,'target_x',1)
        frame = _movement_move(state,frame,'target_y',frame.controller.word(low16(frame.target_x)),16)
        frame = _movement_multiply_word(state,frame,'target_y',100)
        frame = _movement_fixed_shift_word(state,frame,'target_x',1)
        frame = compare_ai_long_fields(state,frame,frame.target_y,frame.roster.long(low16(frame.target_x)))
        if not frame.status & 5:
            return _path_carry_fields(state,frame,0,0x337B8)


def distribute_existing_troop_pool_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """337C6: distribute live pool, clamp borrowed capacity, exact C outcome."""
    frame = _movement_frame(state,frame)
    frame = first_replace(frame,roster=state.table_at(0xFFFFE774).cursor())
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame = _movement_fixed_shift_word(state,frame,'target_x',2)
    frame = _movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
    exhausted_roster = False
    if not frame.status & 4:
        frame = first_replace(frame,candidates=state.table_at(0xFFFFF72A).cursor())
        frame = first_replace(frame,controller=state.table_at(0xFFFFC800))
        frame = first_replace(frame,scan=state.table_at(0xFFFFB800).cursor())
        while True:
            officer = frame.candidates.word()
            frame = first_replace(frame,candidates=frame.candidates.advance(2))
            frame = _movement_move(state,frame,'unit',officer,16)
            if frame.status & 8:
                exhausted_roster = True
                break
            frame = _movement_move(state,frame,'unit',low16(frame.unit)&255,16)
            frame = _movement_fixed_shift_word(state,frame,'unit',1)
            frame = _movement_move(state,frame,'count',frame.scan.word(low16(frame.unit)),16)
            frame = _movement_multiply_word(state,frame,'count',100)
            frame = _movement_fixed_shift_word(state,frame,'unit',1)
            frame = adjust_ai_carrier_fields(state,frame,'count',frame.controller.long(low16(frame.unit)),32,True)
            if frame.status & 1:
                frame = _movement_move_long(state,frame,'count',0)
            frame = compare_ai_long_fields(state,frame,frame.count,frame.target_y)
            if not frame.status & 5:
                frame = _movement_move_long(state,frame,'count',frame.target_y)
            frame = _resupply_add_memory_long_fields(state,frame,frame.controller.address(low16(frame.unit)),frame.count)
            frame = adjust_ai_carrier_fields(state,frame,'target_y',frame.count,32,True)
            if frame.status & 4:
                break
    frame = store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),frame.target_y,32)
    return _path_carry_fields(state,frame,1 if exhausted_roster else 0,0x33828 if exhausted_roster else 0x3381C)


def buy_and_distribute_troops_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3382E: live gold purchase and original unclamped borrowed deficit.

    DIVU overflow retains D1; the immediately following MOVE.W defines NZVC.
    If its quantity WORD is zero, incoming D4's high WORD remains in the pool.
    Unlike337C6, this original owner does not clamp an overcapacity subtraction.
    """
    frame = _movement_frame(state,frame)
    frame = first_replace(frame,roster=state.table_at(0xFFFFF72A).cursor())
    frame = first_replace(frame,scan=state.table_at(0xFFFFB800).cursor())
    frame = first_replace(frame,candidates=state.table_at(0xFFFFDFFC).cursor())
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame = _movement_fixed_shift_word(state,frame,'target_x',2)
    frame = _movement_move_long(state,frame,'count',frame.candidates.long(low16(frame.target_x)))
    frame = compare_ai_long_fields(state,frame,frame.count,3000)
    if frame.status & 1:
        return frame
    frame = _movement_move_long(state,frame,'target_y',frame.count)
    frame = first_replace(frame,target_y=divu_retained(frame.target_y,200))
    frame = _movement_move(state,frame,'distance',low16(frame.target_y),16)
    if not frame.status & 4:
        frame = _movement_multiply_word(state,frame,'distance',100)
        frame = compare_ai_long_fields(state,frame,frame.distance,100000)
        if not frame.status & 5:
            frame = _movement_move_long(state,frame,'distance',100000)
            frame = _movement_move(state,frame,'target_y',1000,16)
        frame = _movement_multiply_word(state,frame,'target_y',100)
        frame = adjust_ai_carrier_fields(state,frame,'count',frame.target_y,32,True)
        frame = store_ai_value_fields(state,frame,frame.candidates.address(low16(frame.target_x)),frame.count,32)
        frame = first_replace(frame,controller=state.table_at(0xFFFFC800))
        while True:
            officer = frame.roster.word()
            frame = first_replace(frame,roster=frame.roster.advance(2))
            frame = _movement_move(state,frame,'target_x',officer,16)
            if frame.status & 8:
                break
            frame = _movement_move(state,frame,'target_x',low16(frame.target_x)&255,16)
            frame = _movement_fixed_shift_word(state,frame,'target_x',1)
            frame = _movement_move(state,frame,'target_y',frame.scan.word(low16(frame.target_x)),16)
            frame = _movement_multiply_word(state,frame,'target_y',100)
            frame = _movement_fixed_shift_word(state,frame,'target_x',1)
            frame = adjust_ai_carrier_fields(state,frame,'target_y',frame.controller.long(low16(frame.target_x)),32,True)
            frame = compare_ai_long_fields(state,frame,frame.target_y,frame.distance)
            if not frame.status & 5:
                frame = _movement_move_long(state,frame,'target_y',frame.distance)
            frame = _resupply_add_memory_long_fields(state,frame,frame.controller.address(low16(frame.target_x)),frame.target_y)
            frame = adjust_ai_carrier_fields(state,frame,'distance',frame.target_y,32,True)
            if frame.status & 4:
                break
    frame = first_replace(frame,roster=state.table_at(0xFFFFE774).cursor())
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame = _movement_fixed_shift_word(state,frame,'target_x',2)
    return store_ai_value_fields(state,frame,frame.roster.address(low16(frame.target_x)),frame.distance,32)


def clear_equipment_command_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """338BA: original negative phase exit marker, no invented cleanup."""
    frame = _movement_frame(state,frame)
    return store_ai_value_fields(state,frame,0xFFFFF728,65535,16)
