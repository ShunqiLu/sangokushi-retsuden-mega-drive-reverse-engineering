"""Whole force reassignment/disbanding over the actual live Scene Frame.

Original 66616..66BF4 owns fifteen functions; the foreign6683E..6689E gap
is not copied here. Scalar rules remain independently editable and unchanged.
No natural bounds, inactive-city cleanup or malformed-list escape is invented.
"""
from ..high_level_scene_flows.domain import SceneState, low8, low16, s16
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_main_flows.business_movement_support import (
    _movement_frame, _movement_move, _movement_move_long, _movement_test,
    _movement_compare, _movement_fixed_shift_word, _movement_multiply_word,
    _movement_divu_word, _movement_save_longs, _movement_restore_longs,
)
from ..high_level_remaining_flows.business_lowbank import (
    _economy_delta_fields, _economy_logic_fields, _economy_long_shift_fields,
    _economy_swap_fields, _lowbank_ui_store_fields,
)


REAL_CALL_PAIRS = (
    (0x66724,0x6665E),(0x668FC,0x66662),(0x6694C,0x66668),(0x66B54,0x66670),
    (0x667F6,0x6667C),(0x66724,0x666A2),(0x668FC,0x666A6),(0x6694C,0x666AC),
    (0x66B54,0x666B4),(0x667F6,0x666C0),(0x669FE,0x666F8),(0x66AD8,0x666FC),
    (0x66B54,0x66700),(0x66A22,0x66708),(0x208CE,0x66756),(0xE1F6,0x6677E),
    (0x6679E,0x66784),(0x6679E,0x6679C),(0x668BE,0x66830),(0x6689E,0x66834),
    (0x83D4,0x66916),(0x669D0,0x669C6),(0x66A9E,0x66A78),(0x66BB0,0x66B64),
)


def _force_call_fields(state, frame, target, continuation):
    """Every finite original BSR/JSR retains its actual physical LONG slot."""
    if (target,continuation) not in REAL_CALL_PAIRS:
        raise ValueError('one actual whole force-family CALL pair is required')
    frame = _movement_frame(state,frame)
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0,continuation)
    entered = first_replace(frame,stack_cursor=stack)
    if target == 0x208CE:
        from ..high_level_gameplay_flow.business_reuse import apply_returning_officer_loyalty_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        returned = apply_returning_officer_loyalty_fields(BattlePresentationMemory(state),entered)
    elif target == 0xE1F6:
        from ..high_level_gameplay_flow.business_battle import choose_city_head_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        returned = choose_city_head_fields(BattlePresentationMemory(state),entered)
    elif target == 0x83D4:
        from ..high_level_battle_ai.business_formation import first_deployment_random_fields
        from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory
        returned = first_deployment_random_fields(BattlePolicyMemory(state),entered)
    else:
        owners = {
            0x66724:reassign_city_officers_fields,0x6679E:clear_transferred_city_orders_fields,
            0x667F6:remove_force_group_packets_fields,0x6689E:compact_following_packets_fields,
            0x668BE:remove_packet_pair_reference_fields,0x668FC:reduce_city_reserve_fields,
            0x6694C:return_temporary_city_assignments_fields,0x669D0:remove_officer_pair_reference_fields,
            0x669FE:mark_city_assignments_inactive_fields,0x66A22:disband_force_group_packets_fields,
            0x66A9E:remove_disbanded_packet_reference_fields,
            0x66AD8:clear_disbanded_temporary_assignments_fields,
            0x66B54:clear_disbanded_city_orders_fields,0x66BB0:clear_city_queue_principals_fields,
        }
        returned = owners[target](state,entered)
    returned = _movement_frame(state,returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual,returned,continuation)
    return first_replace(returned,stack_cursor=returned.stack_cursor.advance(4))


def _force_address(frame, carrier, index, displacement=0):
    return getattr(frame,carrier).address(low16(frame.carrier(index)),displacement)


def _force_pointer(state, frame, carrier, address):
    """LEA/MOVEA/ADDA retain the current CCR rather than inventing MOVE flags."""
    return first_replace(frame,**{carrier:state.table_at(address).cursor()})


def _force_memory_bit_fields(state, frame, address, bit, clear=False):
    value = state.read(address,1)
    mask = 1 << (bit & 7)
    status = (frame.status & 27) | (4 if not value & mask else 0)
    state.sr = (state.sr & 65504) | status
    state.write(address,1,value & (255 ^ mask) if clear else value | mask)
    return first_replace(frame,status=status)


def _force_register_bit_fields(state, frame, name, bit, clear=False):
    value = frame.carrier(name)
    mask = 1 << (bit & 31)
    status = (frame.status & 27) | (4 if not value & mask else 0)
    state.sr = (state.sr & 65504) | status
    changed = value & (0xFFFFFFFF ^ mask) if clear else value | mask
    return first_replace(frame,status=status,**{name:changed})


def _force_push_fields(state, frame, name, size):
    stack = frame.stack_cursor.advance(-size)
    value = frame.carrier(name) & ((1 << (size*8))-1)
    frame = _lowbank_ui_store_fields(state,frame,stack.base,value,size)
    return first_replace(frame,stack_cursor=stack)


def _force_pop_fields(state, frame, name, size):
    value = state.read(frame.stack_cursor.base,size)
    frame = first_replace(frame,stack_cursor=frame.stack_cursor.advance(size))
    return (_movement_move_long(state,frame,name,value) if size == 4
        else _movement_move(state,frame,name,value,16))


def _force_dbra_fields(frame, name):
    """DBRA changes only the low WORD, never CCR or X."""
    value = (low16(frame.carrier(name))-1) & 65535
    frame = first_replace(frame,**{name:(frame.carrier(name)&0xFFFF0000)|value})
    return frame,value != 65535


def resolve_force_reassignment_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66616: merge/remove both force roles, or disband the original 56 slots."""
    frame = _movement_frame(state,frame)
    for name,address in (('roster',0xFFFFE640),('candidates',0xFFFFF427),
            ('controller',0xFFFFCC00),('scan',0xFFFFC300)):
        frame = _force_pointer(state,frame,name,address)
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFA622,2),16)
    if not frame.status & 8:
        frame = _movement_move(state,frame,'target_y',0,16)
        frame = _movement_move(state,frame,'target_y',low8(frame.target_x),8)
        frame = _movement_fixed_shift_word(state,frame,'target_x',8,True)
        frame = _movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFEFB0,2),16)
        same_removed = bool(frame.status & 4)
        selected = 'target_y' if same_removed else 'target_x'
        frame = _movement_fixed_shift_word(state,frame,selected,1)
        frame = _movement_move(state,frame,'unit',frame.roster.word(low16(frame.carrier(selected))),16)
        frame = _movement_fixed_shift_word(state,frame,selected,1,True)
        frame = _lowbank_ui_store_fields(state,frame,0xFFFFF3F2,low16(frame.unit))
        frame = _movement_move(state,frame,'count',50 if same_removed else 90,16)
        frame = _movement_move(state,frame,'unit',56,16)
        tokens = (0x6665E,0x66662,0x66668,0x66670,0x6667C) if same_removed else (
            0x666A2,0x666A6,0x666AC,0x666B4,0x666C0)
        while True:
            owner = low8(frame.target_x if same_removed else frame.target_y)
            frame = _movement_compare(state,frame,owner,frame.candidates.byte(low16(frame.unit)),8)
            if frame.status & 4:
                frame = _movement_move(state,frame,'choice',low16(frame.carrier(selected)),16)
                frame = _force_call_fields(state,frame,0x66724,tokens[0])
                frame = _force_call_fields(state,frame,0x668FC,tokens[1])
                frame = _movement_move(state,frame,'choice',low16(frame.target_x if same_removed else frame.target_y),16)
                frame = _force_call_fields(state,frame,0x6694C,tokens[2])
                frame = _force_push_fields(state,frame,'target_y',4)
                frame = _movement_move(state,frame,'target_y',low16(frame.target_x),16)
                frame = _force_call_fields(state,frame,0x66B54,tokens[3])
                frame = _force_pop_fields(state,frame,'target_y',4)
            frame = _economy_delta_fields(state,frame,'unit',1,16,True)
            if frame.status & 4:
                break
        frame = _movement_move(state,frame,'choice',low16(frame.target_x if same_removed else frame.target_y),16)
        frame = _force_call_fields(state,frame,0x667F6,tokens[4])
    else:
        frame = _force_pointer(state,frame,'roster',0xFFFFF428)
        frame = _force_pointer(state,frame,'candidates',0xFFFFF460)
        frame = _movement_move(state,frame,'target_x',state.read(0xFFFFEFB0,2),16)
        frame = _movement_move(state,frame,'target_y',55,16)
        while True:
            frame = _movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(low16(frame.target_y)),8)
            if frame.status & 4:
                frame = _movement_compare(state,frame,low16(frame.target_y),40,16)
                if frame.status & 1:
                    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'roster','target_y'),255,1)
                    frame = _movement_move(state,frame,'unit',low16(frame.target_y),16)
                    frame = _movement_fixed_shift_word(state,frame,'unit',1)
                    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'candidates','unit'),65535)
                frame = _force_call_fields(state,frame,0x669FE,0x666F8)
                frame = _force_call_fields(state,frame,0x66AD8,0x666FC)
                frame = _force_call_fields(state,frame,0x66B54,0x66700)
            frame,again = _force_dbra_fields(frame,'target_y')
            if not again:
                break
        frame = _force_call_fields(state,frame,0x66A22,0x66708)
    frame = _force_pointer(state,frame,'roster',0xFFFFE640)
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFEFB0,2),16)
    frame = _movement_fixed_shift_word(state,frame,'target_x',1)
    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'roster','target_x'),65535)
    frame = _lowbank_ui_store_fields(state,frame,0xFFFFA622,0,2,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF612,0x20C)


def reassign_city_officers_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66724: original41 gate, descending roster, loyalty and real head choice."""
    frame = _movement_frame(state,frame)
    frame = _movement_compare(state,frame,low16(frame.unit),41,16)
    if not frame.status & 1:
        return frame
    frame = _force_pointer(state,frame,'opponent',0xFFFFF500)
    frame = _force_pointer(state,frame,'scratch',0xFFFFF45E)
    frame = _movement_move(state,frame,'distance',255,16)
    frame = _movement_move(state,frame,'offset_x',0,16)
    while True:
        frame = _movement_compare(state,frame,low8(frame.unit),frame.controller.byte(low16(frame.distance)),8)
        if frame.status & 4:
            frame = _movement_compare(state,frame,low8(frame.count),frame.scan.byte(low16(frame.distance)),8)
            if frame.status & 5:
                frame = _force_memory_bit_fields(state,frame,_force_address(frame,'controller','distance'),7)
            else:
                frame = _lowbank_ui_store_fields(state,frame,frame.opponent.base,low16(frame.distance))
                frame = first_replace(frame,opponent=frame.opponent.advance(2))
                frame = _lowbank_ui_store_fields(state,frame,0xFFFFF3A6,low16(frame.distance))
                frame = _force_call_fields(state,frame,0x208CE,0x66756)
                frame = _economy_delta_fields(state,frame,'offset_x',1)
        frame,again = _force_dbra_fields(frame,'distance')
        if not again:
            break
    frame = _lowbank_ui_store_fields(state,frame,frame.opponent.base,65535)
    frame = _movement_test(state,frame,low16(frame.offset_x),16)
    if not frame.status & 4:
        frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'candidates','unit'),low8(frame.choice),1)
        frame = _force_push_fields(state,frame,'target_x',2)
        frame = _movement_move(state,frame,'target_x',low16(frame.unit),16)
        frame = _force_call_fields(state,frame,0xE1F6,0x6677E)
        frame = _force_pop_fields(state,frame,'target_x',2)
        return _force_call_fields(state,frame,0x6679E,0x66784)
    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'candidates','unit'),255,1)
    frame = _movement_move(state,frame,'offset_y',low16(frame.unit),16)
    frame = _movement_fixed_shift_word(state,frame,'offset_y',1)
    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'scratch','offset_y'),65535)
    return _force_call_fields(state,frame,0x6679E,0x6679C)


def clear_transferred_city_orders_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6679E: saved D0/D1/A0/A1 and three original E80C-column sentinels."""
    frame = _movement_frame(state,frame)
    saved = ('target_x','target_y','roster','candidates')
    frame = _movement_save_longs(state,frame,saved)
    frame = _movement_compare(state,frame,low16(frame.unit),41,16)
    if frame.status & 1:
        frame = _movement_move(state,frame,'target_x',low16(frame.unit),16)
        frame = _movement_fixed_shift_word(state,frame,'target_x',1)
        frame = _economy_delta_fields(state,frame,'target_x',low16(frame.unit))
        frame = _movement_fixed_shift_word(state,frame,'target_x',2)
        frame = _force_pointer(state,frame,'roster',0xFFFFE80C)
        frame = _force_pointer(state,frame,'candidates',0xFFFFCD00)
        for displacement in (0,4,8):
            frame = _movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x),displacement),16)
            if not frame.status & 8:
                frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'candidates','target_y'),0,1,True)
                frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'roster','target_x',displacement),65535)
    return _movement_restore_longs(state,frame,saved)


def remove_force_group_packets_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """667F6: retained D0 high BYTE, original packet compaction and alias marks."""
    frame = _movement_frame(state,frame)
    frame = _force_pointer(state,frame,'opponent',0xFFFF9000)
    frame = _force_pointer(state,frame,'scratch',0xFFFFD300)
    while True:
        frame = _movement_move(state,frame,'target_x',frame.opponent.byte(),8)
        frame = _economy_logic_fields(state,frame,'target_x',15,8)
        if frame.status & 4:
            return frame
        frame = _movement_compare(state,frame,low8(frame.choice),frame.opponent.byte(0,4),8)
        if not frame.status & 4:
            frame = _force_pointer(state,frame,'opponent',frame.opponent.address(low16(frame.target_x),13))
            continue
        frame = _movement_move(state,frame,'target_y',low16(frame.target_x),16)
        frame = _economy_delta_fields(state,frame,'target_y',1,16,True)
        frame = _movement_move(state,frame,'distance',0,16)
        frame = _movement_move(state,frame,'unit',0,16)
        while True:
            frame = _movement_move(state,frame,'unit',frame.opponent.byte(low16(frame.target_y),13),8)
            frame = _force_memory_bit_fields(state,frame,_force_address(frame,'controller','unit'),7)
            frame = _force_memory_bit_fields(state,frame,_force_address(frame,'controller','unit'),6,True)
            frame,again = _force_dbra_fields(frame,'target_y')
            if not again:
                break
        frame = _force_call_fields(state,frame,0x668BE,0x66830)
        frame = _force_call_fields(state,frame,0x6689E,0x66834)


def compact_following_packets_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6689E: complete following packets and only one terminal BYTE clear."""
    frame = _movement_frame(state,frame)
    frame = _force_pointer(state,frame,'scratch',frame.opponent.address(low16(frame.target_x),13))
    frame = _force_pointer(state,frame,'auxiliary',frame.opponent.base)
    while True:
        frame = _movement_move(state,frame,'target_x',frame.scratch.byte(),8)
        frame = _economy_logic_fields(state,frame,'target_x',15,16)
        if frame.status & 4:
            return _lowbank_ui_store_fields(state,frame,frame.auxiliary.base,0,1,True)
        frame = _economy_delta_fields(state,frame,'target_x',12)
        while True:
            value = frame.scratch.byte()
            frame = first_replace(frame,scratch=frame.scratch.advance(1))
            frame = _lowbank_ui_store_fields(state,frame,frame.auxiliary.base,value,1)
            frame = first_replace(frame,auxiliary=frame.auxiliary.advance(1))
            frame,again = _force_dbra_fields(frame,'target_x')
            if not again:
                break


def remove_packet_pair_reference_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """668BE: first-member reference; A5/A6 clobbers remain genuine."""
    frame = _movement_frame(state,frame)
    saved = ('target_x','target_y')
    frame = _movement_save_longs(state,frame,saved)
    frame = _movement_move(state,frame,'target_x',0,16)
    frame = _movement_move(state,frame,'target_x',frame.opponent.byte(0,13),8)
    frame = _force_pointer(state,frame,'scratch',0x00FF39B2)
    frame = first_replace(frame,scratch=frame.scratch.advance(s16(state.read(0x00FF3BB2,2))))
    while True:
        frame = _movement_test(state,frame,frame.scratch.byte(),8)
        if frame.status & 4:
            break
        frame = _movement_compare(state,frame,low8(frame.target_x),frame.scratch.byte(0,1),8)
        if frame.status & 4:
            frame = _force_pointer(state,frame,'auxiliary',frame.scratch.base+2)
            while True:
                value = frame.auxiliary.byte()
                frame = first_replace(frame,auxiliary=frame.auxiliary.advance(1))
                frame = _lowbank_ui_store_fields(state,frame,frame.scratch.base,value,1)
                frame = first_replace(frame,scratch=frame.scratch.advance(1))
                if frame.status & 4:
                    break
                value = frame.auxiliary.byte()
                frame = first_replace(frame,auxiliary=frame.auxiliary.advance(1))
                frame = _lowbank_ui_store_fields(state,frame,frame.scratch.base,value,1)
                frame = first_replace(frame,scratch=frame.scratch.advance(1))
            break
        frame = first_replace(frame,scratch=frame.scratch.advance(2))
    return _movement_restore_longs(state,frame,saved)


def reduce_city_reserve_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """668FC: exact RNG scaling, low-WORD reserve subtraction and DIVU stop."""
    frame = _movement_frame(state,frame)
    frame = _movement_compare(state,frame,low16(frame.unit),41,16)
    if not frame.status & 1:
        return frame
    frame = _movement_test(state,frame,frame.candidates.byte(low16(frame.unit)),8)
    if frame.status & 8:
        return frame
    saved = ('target_x','target_y','opponent')
    frame = _movement_save_longs(state,frame,saved)
    frame = _force_call_fields(state,frame,0x83D4,0x66916)
    frame = _economy_logic_fields(state,frame,'target_x',65535,32)
    frame = _movement_move_long(state,frame,'target_y',frame.target_x)
    frame = _economy_long_shift_fields(state,frame,'target_x',2)
    frame = _economy_delta_fields(state,frame,'target_x',frame.target_y,32)
    frame = _economy_long_shift_fields(state,frame,'target_x',2)
    frame = _economy_delta_fields(state,frame,'target_x',frame.target_y,32)
    frame = _economy_swap_fields(state,frame,'target_x')
    frame = _economy_delta_fields(state,frame,'target_x',10)
    frame = _force_pointer(state,frame,'opponent',0xFFFFE31C)
    frame = _movement_move(state,frame,'target_y',low16(frame.unit),16)
    frame = _movement_fixed_shift_word(state,frame,'target_y',2)
    frame = _movement_move_long(state,frame,'distance',frame.opponent.long(low16(frame.target_y)))
    frame = _movement_move_long(state,frame,'offset_x',frame.distance)
    frame = _movement_multiply_word(state,frame,'offset_x',low16(frame.target_x))
    frame = _movement_divu_word(state,frame,'offset_x',100,0x6693C)
    frame = _economy_delta_fields(state,frame,'distance',low16(frame.offset_x),16,True)
    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'opponent','target_y'),frame.distance,4)
    return _movement_restore_longs(state,frame,saved)


def return_temporary_city_assignments_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """6694C: live alias assignments, original bit indices and pair removal."""
    frame = _movement_frame(state,frame)
    saved = ('count','distance','offset_x','offset_y','choice','roster','candidates','controller','scan','opponent')
    frame = _movement_save_longs(state,frame,saved)
    for name,address in (('roster',0xFFFFCC00),('candidates',0xFFFFA050),
            ('controller',0xFFFFEA37),('scan',0xFFFF9FFF),('opponent',0xFFFFEFAA)):
        frame = _force_pointer(state,frame,name,address)
    frame = _movement_move(state,frame,'distance',low16(frame.unit),16)
    frame = _economy_logic_fields(state,frame,'distance',64,8,'or')
    frame = _movement_move(state,frame,'offset_x',255,16)
    while True:
        frame = _movement_move(state,frame,'offset_y',frame.roster.byte(low16(frame.offset_x)),8)
        frame = _movement_compare(state,frame,low8(frame.offset_y),low8(frame.distance),8)
        selected = bool(frame.status & 4)
        if not selected:
            frame = _economy_logic_fields(state,frame,'offset_y',63,16)
            frame = _movement_compare(state,frame,low16(frame.offset_y),41,16)
            if not frame.status & 1:
                frame = _economy_logic_fields(state,frame,'offset_y',64,16,'or')
                frame = _movement_compare(state,frame,low8(frame.offset_y),low8(frame.distance),8)
                selected = bool(frame.status & 4)
        if selected:
            frame = _movement_move(state,frame,'offset_y',frame.candidates.byte(low16(frame.offset_x)),8)
            if not frame.status & 4:
                frame = _economy_logic_fields(state,frame,'offset_y',63,16)
                frame = _movement_move(state,frame,'choice',low16(frame.offset_y),16)
                frame = _force_register_bit_fields(state,frame,'offset_y',7)
                frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'roster','offset_x'),low8(frame.offset_y),1)
                frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'candidates','offset_x'),0,1,True)
                frame = _force_register_bit_fields(state,frame,'offset_y',7,True)
                frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'controller','offset_y'),0,1,True)
                frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'scan','offset_y'),0,1,True)
                frame = _economy_delta_fields(state,frame,'offset_y',1,16,True)
                frame = _movement_move(state,frame,'count',low16(frame.offset_y),16)
                frame = _movement_fixed_shift_word(state,frame,'offset_y',3,True)
                frame = _economy_logic_fields(state,frame,'count',7,16)
                frame = _force_memory_bit_fields(state,frame,_force_address(frame,'opponent','offset_y'),frame.count,True)
                frame = _force_call_fields(state,frame,0x669D0,0x669C6)
        frame,again = _force_dbra_fields(frame,'offset_x')
        if not again:
            return _movement_restore_longs(state,frame,saved)


def remove_officer_pair_reference_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """669D0: original double postincrement and -3 write alias are retained."""
    frame = _movement_frame(state,frame)
    frame = _movement_save_longs(state,frame,('roster',))
    frame = _force_pointer(state,frame,'roster',0x00FF39B2)
    frame = first_replace(frame,roster=frame.roster.advance(s16(state.read(0x00FF3BB2,2))))
    while True:
        value = frame.roster.byte()
        frame = first_replace(frame,roster=frame.roster.advance(1))
        frame = _movement_test(state,frame,value,8)
        if frame.status & 4:
            break
        value = frame.roster.byte()
        frame = first_replace(frame,roster=frame.roster.advance(1))
        frame = _movement_compare(state,frame,low8(frame.offset_x),value,8)
        if not frame.status & 4:
            continue
        while True:
            value = frame.roster.byte()
            frame = first_replace(frame,roster=frame.roster.advance(1))
            frame = _lowbank_ui_store_fields(state,frame,frame.roster.base-3,value,1)
            if frame.status & 4:
                break
            value = frame.roster.byte()
            frame = first_replace(frame,roster=frame.roster.advance(1))
            frame = _lowbank_ui_store_fields(state,frame,frame.roster.base-3,value,1)
        break
    return _movement_restore_longs(state,frame,('roster',))


def mark_city_assignments_inactive_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """669FE: index+1 compares against all256 raw assignment BYTEs."""
    frame = _movement_frame(state,frame)
    saved = ('target_x','target_y','roster')
    frame = _movement_save_longs(state,frame,saved)
    frame = _economy_delta_fields(state,frame,'target_y',1)
    frame = _force_pointer(state,frame,'roster',0xFFFFCC00)
    frame = _movement_move(state,frame,'target_x',255,16)
    while True:
        value = frame.roster.byte()
        frame = first_replace(frame,roster=frame.roster.advance(1))
        frame = _movement_compare(state,frame,low8(frame.target_y),value,8)
        if frame.status & 4:
            frame = _force_memory_bit_fields(state,frame,frame.roster.base-1,7)
        frame,again = _force_dbra_fields(frame,'target_x')
        if not again:
            return _movement_restore_longs(state,frame,saved)


def disband_force_group_packets_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66A22: all matching packed groups, exact inline following-packet loop."""
    frame = _movement_frame(state,frame)
    saved = ('target_x','target_y','unit','count','distance','roster','candidates','controller','scan')
    frame = _movement_save_longs(state,frame,saved)
    frame = _force_pointer(state,frame,'roster',0xFFFF9000)
    frame = _force_pointer(state,frame,'candidates',0xFFFFCC00)
    frame = _movement_move(state,frame,'target_x',state.read(0xFFFFEFB0,2),16)
    while True:
        frame = _movement_move(state,frame,'target_y',frame.roster.byte(),8)
        frame = _economy_logic_fields(state,frame,'target_y',15,16)
        if frame.status & 4:
            return _movement_restore_longs(state,frame,saved)
        frame = _movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(0,4),8)
        if not frame.status & 4:
            frame = _force_pointer(state,frame,'roster',frame.roster.address(low16(frame.target_y),13))
            continue
        frame = _movement_move(state,frame,'unit',low16(frame.target_y),16)
        frame = _economy_delta_fields(state,frame,'unit',1,16,True)
        frame = _movement_move(state,frame,'count',0,16)
        while True:
            frame = _movement_move(state,frame,'count',frame.roster.byte(low16(frame.unit),13),8)
            frame = _movement_move(state,frame,'distance',frame.candidates.byte(low16(frame.count)),8)
            frame = _economy_logic_fields(state,frame,'distance',63,16)
            if not frame.status & 4:
                frame = _force_register_bit_fields(state,frame,'distance',7)
            else:
                frame = _movement_move(state,frame,'distance',129,8)
            frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'candidates','count'),low8(frame.distance),1)
            frame,again = _force_dbra_fields(frame,'unit')
            if not again:
                break
        frame = _force_call_fields(state,frame,0x66A9E,0x66A78)
        frame = _force_pointer(state,frame,'controller',frame.roster.address(low16(frame.target_y),13))
        frame = _force_pointer(state,frame,'scan',frame.roster.base)
        while True:
            frame = _movement_move(state,frame,'target_y',frame.controller.byte(),8)
            frame = _economy_logic_fields(state,frame,'target_y',15,16)
            if frame.status & 4:
                frame = _lowbank_ui_store_fields(state,frame,frame.scan.base,0,1,True)
                break
            frame = _economy_delta_fields(state,frame,'target_y',12)
            while True:
                value = frame.controller.byte()
                frame = first_replace(frame,controller=frame.controller.advance(1))
                frame = _lowbank_ui_store_fields(state,frame,frame.scan.base,value,1)
                frame = first_replace(frame,scan=frame.scan.advance(1))
                frame,again = _force_dbra_fields(frame,'target_y')
                if not again:
                    break


def remove_disbanded_packet_reference_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66A9E: preserve D0/A1/A2, while comparison keeps D0's other bytes."""
    frame = _movement_frame(state,frame)
    saved = ('target_x','candidates','controller')
    frame = _movement_save_longs(state,frame,saved)
    frame = _force_pointer(state,frame,'candidates',0x00FF39B2)
    frame = first_replace(frame,candidates=frame.candidates.advance(s16(state.read(0x00FF3BB2,2))))
    frame = _movement_move(state,frame,'target_x',frame.roster.byte(0,13),8)
    while True:
        frame = _movement_test(state,frame,frame.candidates.byte(),8)
        if frame.status & 4:
            break
        frame = _movement_compare(state,frame,low8(frame.target_x),frame.candidates.byte(0,1),8)
        if frame.status & 4:
            frame = _force_pointer(state,frame,'controller',frame.candidates.base+2)
            while True:
                value = frame.controller.byte()
                frame = first_replace(frame,controller=frame.controller.advance(1))
                frame = _lowbank_ui_store_fields(state,frame,frame.candidates.base,value,1)
                frame = first_replace(frame,candidates=frame.candidates.advance(1))
                if frame.status & 4:
                    break
                value = frame.controller.byte()
                frame = first_replace(frame,controller=frame.controller.advance(1))
                frame = _lowbank_ui_store_fields(state,frame,frame.candidates.base,value,1)
                frame = first_replace(frame,candidates=frame.candidates.advance(1))
            break
        frame = first_replace(frame,candidates=frame.candidates.advance(2))
    return _movement_restore_longs(state,frame,saved)


def clear_disbanded_temporary_assignments_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66AD8: original 41 BYTE check vs WORD63 mask and live temporary bits."""
    frame = _movement_frame(state,frame)
    saved = ('target_x','target_y','unit','count','roster','candidates','controller','scan','opponent','scratch')
    frame = _movement_save_longs(state,frame,saved)
    frame = _economy_delta_fields(state,frame,'target_y',1)
    frame = _economy_logic_fields(state,frame,'target_y',64,16,'or')
    for name,address in (('roster',0xFFFFCC00),('candidates',0xFFFFA050),
            ('scan',0xFFFFEA37),('opponent',0xFFFF9FFF),('scratch',0xFFFFEFAA)):
        frame = _force_pointer(state,frame,name,address)
    frame = _movement_move(state,frame,'target_x',255,16)
    while True:
        frame = _movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_x)),8)
        status = (frame.status & 27) | (4 if not frame.unit & 64 else 0)
        state.sr = (state.sr & 65504) | status
        frame = first_replace(frame,status=status)
        compare = not bool(frame.status & 4)
        if not compare:
            frame = _movement_compare(state,frame,low8(frame.unit),41,8)
            if not frame.status & 1:
                frame = _force_register_bit_fields(state,frame,'unit',6)
                compare = True
        if compare:
            frame = _movement_compare(state,frame,low8(frame.unit),low8(frame.target_y),8)
            if frame.status & 4:
                frame = _movement_move(state,frame,'unit',frame.candidates.byte(low16(frame.target_x)),8)
                if not frame.status & 4:
                    frame = _economy_logic_fields(state,frame,'unit',63,16)
                    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'scan','unit'),0,1,True)
                    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'candidates','target_x'),0,1,True)
                    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'opponent','unit'),0,1,True)
                    frame = _force_register_bit_fields(state,frame,'unit',7)
                    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'roster','target_x'),low8(frame.unit),1)
                    frame = _force_register_bit_fields(state,frame,'unit',7,True)
                    frame = _economy_delta_fields(state,frame,'unit',1,16,True)
                    frame = _movement_move(state,frame,'count',low16(frame.unit),16)
                    frame = _movement_fixed_shift_word(state,frame,'unit',3,True)
                    frame = _economy_logic_fields(state,frame,'count',7,16)
                    frame = _force_memory_bit_fields(state,frame,_force_address(frame,'scratch','unit'),frame.count,True)
        frame,again = _force_dbra_fields(frame,'target_x')
        if not again:
            return _movement_restore_longs(state,frame,saved)


def clear_disbanded_city_orders_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66B54: forty-only gate before MOVEM, then queue and three order columns."""
    frame = _movement_frame(state,frame)
    frame = _movement_compare(state,frame,low16(frame.target_y),40,16)
    if not frame.status & 1:
        return frame
    saved = ('target_x','target_y','roster','candidates')
    frame = _movement_save_longs(state,frame,saved)
    frame = _force_call_fields(state,frame,0x66BB0,0x66B64)
    frame = _force_pointer(state,frame,'roster',0xFFFFE818)
    frame = _force_pointer(state,frame,'candidates',0xFFFFCD00)
    frame = _movement_move(state,frame,'target_x',low16(frame.target_y),16)
    frame = _movement_fixed_shift_word(state,frame,'target_x',1)
    frame = _economy_delta_fields(state,frame,'target_x',low16(frame.target_y))
    frame = _movement_fixed_shift_word(state,frame,'target_x',2)
    for displacement in (0,4,8):
        frame = _movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x),displacement),16)
        if not frame.status & 8:
            frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'candidates','target_y'),0,1,True)
            frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'roster','target_x',displacement),65535)
    return _movement_restore_longs(state,frame,saved)


def clear_city_queue_principals_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """66BB0: exact D2 LONG save/restore, sixteen queue slots, dynamic LONG bits."""
    frame = _movement_frame(state,frame)
    frame = _force_push_fields(state,frame,'unit',4)
    frame = _force_pointer(state,frame,'roster',0xFFFFE65C)
    frame = _movement_move(state,frame,'target_x',low16(frame.target_y),16)
    frame = _movement_fixed_shift_word(state,frame,'target_x',2)
    frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'roster','target_x'),0,4,True)
    frame = _force_pointer(state,frame,'roster',0xFFFFE9F8)
    frame = _force_pointer(state,frame,'candidates',0xFFFFE65C)
    frame = _movement_move(state,frame,'target_x',0,16)
    while True:
        frame = _movement_compare(state,frame,low8(frame.target_y),frame.roster.byte(),8)
        if frame.status & 4:
            frame = _movement_move(state,frame,'unit',0,16)
            frame = _movement_move(state,frame,'unit',frame.roster.byte(0,1),8)
            frame = _movement_fixed_shift_word(state,frame,'unit',2)
            frame = _lowbank_ui_store_fields(state,frame,_force_address(frame,'candidates','unit'),0,4,True)
            frame = _movement_move(state,frame,'unit',state.read(0xFFFFE700,2),16)
            frame = _force_register_bit_fields(state,frame,'unit',frame.target_x,True)
            frame = _lowbank_ui_store_fields(state,frame,0xFFFFE700,low16(frame.unit))
            frame = _lowbank_ui_store_fields(state,frame,frame.roster.base,0,4,True)
        frame = first_replace(frame,roster=frame.roster.advance(4))
        frame = _economy_delta_fields(state,frame,'target_x',1)
        frame = _movement_compare(state,frame,low16(frame.target_x),16,16)
        if not frame.status & 1:
            return _force_pop_fields(state,frame,'unit',4)
