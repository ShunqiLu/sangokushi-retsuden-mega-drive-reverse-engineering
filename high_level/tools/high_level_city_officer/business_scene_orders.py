"""Complete city-order and relationship-credit owners on one live Scene.

Original E0EE/E3FA share only their record layout; partial register writes,
read-after-clear early return, live rereads and actual flag residues are kept.
No gate, city selection, seed, resource authority or return slot is supplied.
"""
from ..high_level_scene_flows.domain import SceneState,low8,low16
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame,first_replace
from ..high_level_main_flows.business_movement_support import (
    _movement_frame,_movement_move,_movement_move_long,_movement_compare,
    _movement_fixed_shift_word,_movement_arithmetic_long,_movement_test,
)
from ..high_level_battle_ai.business_formation import _first_compare_long
from ..high_level_remaining_flows.business_lowbank import (
    _economy_delta_fields,_economy_memory_delta_fields,_lowbank_ui_store_fields,
)


def _queue_city_order_fields(state: SceneState,frame: FirstDeploymentFrame,
        displacement: int,action: int) -> FirstDeploymentFrame:
    """The two original 70-byte bodies differ only in slot0/4 and action2/3."""
    if (displacement,action) not in ((0,2),(4,3)):
        raise ValueError('only original development/welfare record lanes required')
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=_economy_delta_fields(state,frame,'target_x',state.read(0xFFFFF364,2))
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE80C).cursor(),
        candidates=state.table_at(0xFFFFCD00).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x),displacement),16)
    if not frame.status&8:
        frame=_lowbank_ui_store_fields(state,frame,frame.candidates.address(low16(frame.target_y)),0,1,True)
        frame=_lowbank_ui_store_fields(state,frame,frame.roster.address(low16(frame.target_x),displacement),65535)
        frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF3A6,2),16)
        if frame.status&4:
            return frame
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.address(low16(frame.target_x),displacement),state.read(0xFFFFF3A6,2))
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.address(low16(frame.target_x),displacement+2),state.read(0xFFFFF3A0,2))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    return _lowbank_ui_store_fields(state,frame,frame.roster.address(low16(frame.target_x)),action,1)


def queue_development_order_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E0EE..E134: actual city record slot0 and action BYTE2, no nested CALL."""
    return _queue_city_order_fields(state,frame,0,2)


def queue_welfare_order_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E3FA..E440: actual city record slot4 and action BYTE3, no nested CALL."""
    return _queue_city_order_fields(state,frame,4,3)


def commit_tax_rate_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E57C..E592: true CLR prior WORD read then live tax-rate WORD store."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE3BC).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.address(low16(frame.target_x)),0,2,True)
    return _lowbank_ui_store_fields(state,frame,frame.roster.address(low16(frame.target_x),2),state.read(0xFFFFF3B6,2))


def commit_recruitment_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FBF4..FC16: original wrapping LONG debit and E774 ordered LONG payload."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
    frame=_economy_delta_fields(state,frame,'target_y',state.read(0xFFFFF39E,4),32,True)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.address(low16(frame.target_x)),frame.target_y,4)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE774).cursor())
    return _lowbank_ui_store_fields(state,frame,frame.roster.address(low16(frame.target_x)),state.read(0xFFFFF3E4,4),4)


def commit_equipment_purchase_fields(state: SceneState,frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FC16..FC80: ordered price debit, three-BYTE officer equipment and notice."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3F0,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFEF6A).cursor())
    frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF392,2),16)
    frame=_movement_fixed_shift_word(state,frame,'unit',2)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFDFFC).cursor())
    frame=_economy_memory_delta_fields(state,frame,frame.candidates.address(low16(frame.unit)),frame.target_y,32,True)
    frame=first_replace(frame,roster=state.table_at(0xFFFFEA88).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=_economy_delta_fields(state,frame,'target_x',state.read(0xFFFFF3A6,2))
    frame=_economy_delta_fields(state,frame,'target_x',state.read(0xFFFFF3F0,2))
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3F0,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFEF64).cursor())
    frame=_movement_move(state,frame,'unit',frame.candidates.word(low16(frame.target_y)),16)
    frame=_economy_delta_fields(state,frame,'unit',1)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.address(low16(frame.target_x)),low8(frame.unit),1)
    for address,value in ((0xFFFFF612,state.read(0xFFFFF38A,2)),(0xFFFFF362,40),(0xFFFFF3FE,98)):
        frame=_lowbank_ui_store_fields(state,frame,address,value)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF774,1)
    return _lowbank_ui_store_fields(state,frame,0x00FF7026,9)


def _relationship_register_bit_fields(state: SceneState,
        frame: FirstDeploymentFrame, bit_number: int) -> FirstDeploymentFrame:
    """The two dynamic BSET.L operations change D2 and only the Z flag."""
    mask = 1 << (bit_number & 31)
    previous = frame.unit
    status = (frame.status & 27) | (4 if not previous & mask else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, unit=previous | mask, status=status)


def _register_relationship_pair_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """318AC..318D2: record both directed relationship bits in their real order.

    The original WORD shifts, signed indexed addresses and LONG bit numbers
    are kept. In particular the first left/right shift pair discards bit15;
    the reciprocal bit does not use a cached, unshifted actor identity.
    """
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF376, 2), 16)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF3A6, 2), 16)
    frame = first_replace(frame, roster=state.table_at(0xFFFFE710).cursor())
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = _movement_move(state, frame, 'unit', frame.roster.word(low16(frame.target_x)), 16)
    frame = _relationship_register_bit_fields(state, frame, frame.target_y)
    frame = _lowbank_ui_store_fields(state, frame,
        frame.roster.address(low16(frame.target_x)), low16(frame.unit))
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1, True)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = _movement_move(state, frame, 'unit', frame.roster.word(low16(frame.target_y)), 16)
    frame = _relationship_register_bit_fields(state, frame, frame.target_x)
    return _lowbank_ui_store_fields(state, frame,
        frame.roster.address(low16(frame.target_y)), low16(frame.unit))


def _credit_relationship_city_resources_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """318D2..3191C: credit the current head's actual city, preserving wrap.

    F376 is reread after both relationship writes. The head WORD remains in
    D1 while its low BYTE is replaced by the live assignment; ANDI.W then
    chooses the six-bit city index. ADD.L wraps before the unsigned cap.
    """
    frame = _movement_move_long(state, frame, 'target_x', state.read(0xFFFFF3C8, 4))
    frame = first_replace(frame, roster=state.table_at(0xFFFFDFFC).cursor())
    frame = _movement_test(state, frame, state.read(0xFFFFF742, 2), 16)
    if not frame.status & 4:
        frame = first_replace(frame, roster=state.table_at(0xFFFFE09C).cursor())
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF376, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFE640).cursor())
    frame = _movement_move(state, frame, 'target_y', frame.candidates.word(low16(frame.target_y)), 16)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFCC00).cursor())
    frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(low16(frame.target_y)), 8)
    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 63, 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
    frame = _movement_move_long(state, frame, 'unit', frame.roster.long(low16(frame.target_y)))
    frame = _movement_arithmetic_long(state, frame, 'unit', frame.target_x)
    frame = _first_compare_long(frame, frame.unit, 999999)
    state.sr = (state.sr & 65504) | frame.status
    if not frame.status & 5:
        frame = _movement_move_long(state, frame, 'unit', 999999)
    # The final MOVE.L clears V/C but retains the real ADD.L carry in X,
    # including an addition that wrapped below the unsigned resource cap.
    return _lowbank_ui_store_fields(state, frame,
        frame.roster.address(low16(frame.target_y)), frame.unit, 4)


def commit_relationship_resource_credit_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """318AC..3191E: one whole relationship agreement and city-resource credit.

    The supplied Scene, its live RAM, all full carriers and full SR remain
    authoritative. No nested CALL or stack access exists in this body; the
    incoming return LONG belongs to the actual 317AE/317B2 caller. This API
    returns before original3191C RTS and never manufactures that return.
    """
    frame = _movement_frame(state, frame)
    if frame.status != state.sr & 31:
        raise ValueError('relationship-credit entry Frame and full Scene SR disagree')
    frame = _register_relationship_pair_fields(state, frame)
    return _credit_relationship_city_resources_fields(state, frame)
