"""Monthly city work, officer mortality and the three original event schedules.

Names for the event categories are deliberately neutral: their exact field
effects and messages are known, but interpreting all three as named disasters
would add unproved meaning. This is a source draft, not complete hardware/CPU
execution. Known subrules share live views; unresolved services stop explicitly.
"""
from .domain import (
    GameplayState, Word, Table, uint, u8, u16, low8, low16,
    replace_byte, negative_byte, descending_inclusive, checked_state,
)
from .contexts_calendar import CalendarContext, MortalityContext, EventContext


def process_calendar_city_cycle(state: GameplayState, retained: CalendarContext=CalendarContext()) -> CalendarContext:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_context_fields(state,retained,'calendar')
    actual=process_calendar_city_cycle_fields(memory,entered)
    return retained


def scan_calendar_officer_mortality(state: GameplayState, retained: MortalityContext=MortalityContext()) -> MortalityContext:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_context_fields(state,retained,'mortality')
    actual=scan_calendar_officer_mortality_fields(memory,entered)
    return retained


def remove_mortal_officer_with_message(state: GameplayState, officer: Word, assignments: Table, retained_owner_lookup: Word=0) -> Word:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_entry_fields(state,(officer,retained_owner_lookup),(),(('candidates',assignments),))
    actual=remove_mortal_officer_with_message_fields(memory,entered)
    return low16(actual.target_y)


def choose_city_head_after_mortality(state: GameplayState, city: Word, assignments: Table) -> Word:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_entry_fields(state,(city,),(),(('candidates',assignments),))
    actual=choose_city_head_after_mortality_fields(memory,entered)
    return low16(actual.target_x)


def process_calendar_event_schedulers(state: GameplayState, retained: EventContext=EventContext()) -> EventContext:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_context_fields(state,retained,'event')
    actual=process_calendar_event_schedulers_fields(memory,entered)
    return retained


def show_calendar_event_message(state: GameplayState, message: Word) -> None:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_entry_fields(state,(message,),(),())
    actual=show_calendar_event_message_fields(memory,entered)


def process_first_calendar_event(state: GameplayState, retained: EventContext=EventContext()) -> EventContext:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_context_fields(state,retained,'event')
    actual=process_first_calendar_event_fields(memory,entered)
    return retained


def show_first_calendar_event_values(state: GameplayState, owner: Word) -> None:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_entry_fields(state,(owner,),(),())
    actual=show_first_calendar_event_values_fields(memory,entered)


def process_second_calendar_event(state: GameplayState, retained: EventContext=EventContext()) -> EventContext:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_context_fields(state,retained,'event')
    actual=process_second_calendar_event_fields(memory,entered)
    return retained


def show_second_calendar_event_values(state: GameplayState, owner: Word) -> None:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_entry_fields(state,(owner,),(),())
    actual=show_second_calendar_event_values_fields(memory,entered)


def process_third_calendar_event(state: GameplayState, retained: EventContext=EventContext()) -> EventContext:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_context_fields(state,retained,'event')
    actual=process_third_calendar_event_fields(memory,entered)
    return retained


def show_third_calendar_event_values(state: GameplayState, owner: Word) -> None:
    """Historical observations project the sole core; absent full CPU/SP/X remains a true boundary."""
    from .business_reuse import _calendar_legacy_entry_fields
    memory,entered=_calendar_legacy_entry_fields(state,(owner,),(),())
    actual=show_third_calendar_event_values_fields(memory,entered)


def _show_event_values(state: GameplayState, owner: Word, message: Word) -> None:
    queue = state.ram_d420
    owners = state.ram_f428
    index = u16(0)
    has_heading = False
    while True:
        city = queue.byte(index)
        if city == 255:
            return None
        selected_owner = owners.byte(city)
        if selected_owner == owner:
            state.set_scalar('ram_f646_word', city)
            state.set_scalar('ram_f646_word', u16(state.scalar('ram_f646_word') + 1))
            state.set_scalar('ram_f376_word', selected_owner)
            if not has_heading:
                show_calendar_event_message(state, 178)
                has_heading = True
            show_calendar_event_message(state, message)
        index = u16(index + 1)


def _clear_calendar_message_plane(state: GameplayState) -> None:
    state.mmio_write(0xC00004, 4, 0x4A000003)
    for remaining in descending_inclusive(511):
        state.mmio_write(0xC00000, 2, 0)

# D52 sole full calendar/economy fields; frozen historical owners remain untouched.
from .business_reuse import (
    _calendar_frame_fields,_calendar_move_fields,_calendar_test_fields,
    _calendar_write_fields,_calendar_compare_fields,_calendar_arithmetic_fields,
    _calendar_shift_fields,_calendar_bit_fields,_calendar_db_fields,
    _calendar_save_fields,_calendar_restore_fields,_calendar_push_word_fields,
    _calendar_pop_word_fields,_calendar_call_fields,
)
from .contexts_services import SceneRefreshMemory,SceneRefreshBoundary
from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame,first_replace
from ..high_level_scene_flows.domain import low8,low16
def process_calendar_city_cycle_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    """Run the actual monthly income/payroll phase, then mortality and events."""
    frame=_calendar_frame_fields(memory,frame,0x16B3A)
    memory.state.sr=0x2700
    frame=first_replace(frame,status=0)
    frame=_calendar_push_word_fields(memory,frame,memory.state.read(0xFFFFF376,2))
    frame=_calendar_move_fields(memory,frame,'target_x',39)
    frame=_calendar_move_fields(memory,frame,'target_y',memory.state.read(0xFFFFF375,1),1)
    frame=first_replace(frame,auxiliary=memory.cursor_at(0xFFFFF450))
    frame=_calendar_test_fields(memory,frame,low8(frame.target_y),1)
    if frame.status&4:
        frame=first_replace(frame,roster=memory.cursor_at(0xFFFFE1DC))
        while True:
            frame=first_replace(frame,auxiliary=frame.auxiliary.advance(-1))
            frame=_calendar_test_fields(memory,frame,frame.auxiliary.byte(),1)
            if not frame.status&8:frame=_calendar_call_fields(memory,frame,0x16C0A,0x16B5E)
            frame=first_replace(frame,roster=frame.roster.advance(-4))
            frame,again=_calendar_db_fields(frame,'target_x')
            if not again:break
    else:
        frame=_calendar_compare_fields(memory,frame,low8(frame.target_y),3,1)
        if frame.status&4:
            phases=((0x16C2C,0x16B76),(0x16D10,0x16B7A))
        else:
            frame=_calendar_compare_fields(memory,frame,low8(frame.target_y),9,1)
            phases=((0x16C46,0x16B8E),(0x16D2A,0x16B92)) if frame.status&4 else ()
        if phases:
            while True:
                frame=first_replace(frame,auxiliary=frame.auxiliary.advance(-1))
                frame=_calendar_test_fields(memory,frame,frame.auxiliary.byte(),1)
                if not frame.status&8:
                    for target,token in phases:frame=_calendar_call_fields(memory,frame,target,token)
                frame,again=_calendar_db_fields(frame,'target_x')
                if not again:break
    frame=_calendar_bit_fields(memory,frame,memory.state.read(0xFFFFF375,1),1)
    if frame.status&4:frame=_calendar_call_fields(memory,frame,0x16BB8,0x16BA4)
    frame=_calendar_call_fields(memory,frame,0x16EDA,0x16BA8)
    frame=_calendar_call_fields(memory,frame,0x16FFC,0x16BAC)
    frame=_calendar_pop_word_fields(memory,frame,0xFFFFF376)
    return _calendar_call_fields(memory,frame,0xAF48,0x16BB6)
def scan_calendar_officer_mortality_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    """Scan birth/assignment records in descending actual officer order."""
    frame=_calendar_frame_fields(memory,frame,0x16EDA)
    frame=first_replace(frame,roster=memory.cursor_at(0xFFFFF100),candidates=memory.cursor_at(0xFFFFCC00),
        controller=memory.cursor_at(0xFFFFEA37))
    frame=_calendar_move_fields(memory,frame,'offset_y',255)
    while True:
        frame=first_replace(frame,roster=frame.roster.advance(-1))
        frame=_calendar_move_fields(memory,frame,'offset_x',frame.roster.byte(),1)
        frame=_calendar_compare_fields(memory,frame,low8(frame.offset_x),255,1)
        eligible=not frame.status&4
        if eligible:
            frame=_calendar_move_fields(memory,frame,'distance',frame.candidates.byte(low16(frame.offset_y)),1)
            negative=bool(frame.status&8)
            if not negative:
                frame=_calendar_bit_fields(memory,frame,frame.distance,64)
                eligible=bool(frame.status&4)
                if eligible:
                    frame=_calendar_test_fields(memory,frame,frame.controller.byte(low16(frame.distance)),1)
                    eligible=bool(frame.status&4)
            if eligible:
                frame=_calendar_compare_fields(memory,frame,low8(frame.distance),255,1)
                eligible=not frame.status&4
        if eligible:
            frame=_calendar_move_fields(memory,frame,'choice',memory.state.read(0xFFFFF374,1),1)
            frame=_calendar_arithmetic_fields(memory,frame,'choice',low8(frame.offset_x),1,True)
            if not frame.status&1:
                frame=_calendar_move_fields(memory,frame,'offset_x',1)
                frame=_calendar_move_fields(memory,frame,'choice',low16(frame.choice)&4)
                frame=_calendar_shift_fields(memory,frame,'offset_x',low16(frame.choice))
                frame=_calendar_call_fields(memory,frame,0x83D4,0x16F2E)
                frame=_calendar_move_fields(memory,frame,'target_x',low16(frame.target_x)&15)
                frame=_calendar_compare_fields(memory,frame,low16(frame.target_x),low16(frame.offset_x))
                if frame.status&(1|4):frame=_calendar_call_fields(memory,frame,0x16F42,0x16F3C)
        frame,again=_calendar_db_fields(frame,'offset_y')
        if not again:return frame
def remove_mortal_officer_with_message_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    """Erase a mortal officer, optionally show the player notice, replace city head."""
    frame=_calendar_frame_fields(memory,frame,0x16F42)
    frame=_calendar_save_fields(memory,frame,('scan','opponent'))
    frame=_calendar_move_fields(memory,frame,'target_x',frame.candidates.byte(low16(frame.offset_y)),1)
    frame=first_replace(frame,opponent=memory.cursor_at(0xFFFFF427))
    frame=_calendar_move_fields(memory,frame,'target_y',0)
    frame=_calendar_move_fields(memory,frame,'target_y',frame.opponent.byte(low16(frame.target_x)),1)
    player=False
    for address in (0xFFFFF67B,0xFFFFF67D,0xFFFFF67F):
        frame=_calendar_compare_fields(memory,frame,low8(frame.target_y),memory.state.read(address,1),1)
        if frame.status&4:
            player=True
            break
    if player:
        frame=first_replace(frame,opponent=memory.cursor_at(0xFFFFE640))
        frame=_calendar_shift_fields(memory,frame,'target_y',1)
        frame=_calendar_compare_fields(memory,frame,low16(frame.offset_y),frame.opponent.word(low16(frame.target_y)))
        if not frame.status&4:
            saved=('target_x','target_y','unit','count','distance','offset_x','offset_y','choice',
                'roster','candidates','controller','scan','opponent','scratch','auxiliary')
            frame=_calendar_save_fields(memory,frame,saved)
            frame=_calendar_push_word_fields(memory,frame,memory.state.read(0xFFFFF376,2))
            frame=_calendar_push_word_fields(memory,frame,memory.state.read(0xFFFFF362,2))
            frame=_calendar_write_fields(memory,frame,0xFFFFF376,0,clear=True)
            frame=_calendar_shift_fields(memory,frame,'target_y',1,right=True)
            frame=_calendar_write_fields(memory,frame,0xFFFFF377,low8(frame.target_y),1)
            frame=_calendar_write_fields(memory,frame,0xFFFFF3D0,low16(frame.offset_y))
            frame=_calendar_write_fields(memory,frame,0xFFFFF740,205)
            frame=_calendar_write_fields(memory,frame,0xFFFFF362,0,clear=True)
            frame=_calendar_call_fields(memory,frame,0x30A74,0x16FA4)
            frame=_calendar_pop_word_fields(memory,frame,0xFFFFF362)
            frame=_calendar_pop_word_fields(memory,frame,0xFFFFF376)
            frame=_calendar_restore_fields(memory,frame,saved)
    frame=_calendar_write_fields(memory,frame,frame.candidates.address(low16(frame.offset_y)),255,1)
    frame=first_replace(frame,scan=memory.cursor_at(0xFFFFF460))
    frame=_calendar_move_fields(memory,frame,'target_y',39)
    found=False
    while True:
        frame=_calendar_compare_fields(memory,frame,low16(frame.offset_y),frame.scan.word())
        frame=first_replace(frame,scan=frame.scan.advance(2))
        if frame.status&4:
            found=True
            break
        frame,again=_calendar_db_fields(frame,'target_y')
        if not again:break
    if found:
        frame=_calendar_move_fields(memory,frame,'target_x',low16(frame.target_x)&255)
        frame=_calendar_call_fields(memory,frame,0x16FDA,0x16FD4)
    return _calendar_restore_fields(memory,frame,('scan','opponent'))
def choose_city_head_after_mortality_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16FDA)
    frame=first_replace(frame,scan=memory.cursor_at(0xFFFFF500))
    frame=_calendar_move_fields(memory,frame,'target_y',255)
    while True:
        frame=_calendar_compare_fields(memory,frame,low8(frame.target_x),frame.candidates.byte(low16(frame.target_y)),1)
        if frame.status&4:
            frame=_calendar_write_fields(memory,frame,frame.scan.base,low16(frame.target_y))
            frame=first_replace(frame,scan=frame.scan.advance(2))
        frame,again=_calendar_db_fields(frame,'target_y')
        if not again:break
    frame=_calendar_write_fields(memory,frame,frame.scan.base,65535)
    return _calendar_call_fields(memory,frame,0xE1F6,0x16FFA)
def process_calendar_event_schedulers_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x16FFC)
    for target,token in ((0x17016,0x17000),(0x1707E,0x17004),(0x17016,0x17008),
            (0x171FC,0x1700C),(0x17016,0x17010),(0x173A6,0x17014)):
        frame=_calendar_call_fields(memory,frame,target,token)
    return frame
def show_calendar_event_message_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x17058)
    saved=('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')
    frame=_calendar_save_fields(memory,frame,saved)
    frame=_calendar_write_fields(memory,frame,0xFFFFF740,low16(frame.unit))
    frame=_calendar_write_fields(memory,frame,0xFFFFF608,128)
    frame=_calendar_write_fields(memory,frame,0xFFFFF362,0,clear=True)
    frame=_calendar_push_word_fields(memory,frame,memory.state.read(0xFFFFF612,2))
    frame=_calendar_call_fields(memory,frame,0x30A74,0x17074)
    frame=_calendar_pop_word_fields(memory,frame,0xFFFFF612)
    return _calendar_restore_fields(memory,frame,saved)
def _calendar_device_store_fields(memory,frame,pc,address,value,width):
    """Six original event-plane MOVEs use the same live VDP, not fake RAM.

    The original control LONG is followed by 512 data WORDs in its existing
    DBRA loop. Device readiness, writes and failures belong to SceneState's
    explicitly supplied hardware; this bridge grants no device progress.
    """
    if not 0xFFFF0000 <= address <= 0xFFFFFFFF:
        if (pc,address,width) not in (
                (0x17138,0xC00004,4),(0x17150,0xC00000,2),
                (0x172D4,0xC00004,4),(0x172EC,0xC00000,2),
                (0x17406,0xC00004,4),(0x1741E,0xC00000,2)):
            raise SceneRefreshBoundary(pc,frame,None)
        frame = _calendar_frame_fields(memory,frame,pc)
    return _calendar_write_fields(memory,frame,address,value,width)
def _calendar_clear_event_plane_fields(memory,frame,pc):
    frame=_calendar_device_store_fields(memory,frame,pc,0x00C00004,0x4A000003,4)
    frame=first_replace(frame,scratch=memory.cursor_at(0x00C00000))
    frame=_calendar_move_fields(memory,frame,'offset_y',0)
    frame=_calendar_move_fields(memory,frame,'choice',511)
    while True:
        frame=_calendar_device_store_fields(memory,frame,pc+24,frame.scratch.base,low16(frame.offset_y),2)
        frame,again=_calendar_db_fields(frame,'choice')
        if not again:return frame
def _calendar_event_owner_values_fields(memory,frame,entry,heading_token,detail_token,detail_message):
    frame=_calendar_frame_fields(memory,frame,entry)
    frame=_calendar_move_fields(memory,frame,'target_x',0,4)
    frame=_calendar_move_fields(memory,frame,'count',0,4)
    while True:
        # Message children may change A0/A1; both original LEAs run each iteration.
        frame=first_replace(frame,roster=memory.cursor_at(0xFFFFD420),candidates=memory.cursor_at(0xFFFFF428))
        frame=_calendar_move_fields(memory,frame,'target_y',0,4)
        frame=_calendar_move_fields(memory,frame,'target_y',frame.roster.byte(low16(frame.target_x)),1)
        frame=_calendar_compare_fields(memory,frame,low8(frame.target_y),255,1)
        if frame.status&4:return frame
        frame=_calendar_move_fields(memory,frame,'unit',0,4)
        frame=_calendar_move_fields(memory,frame,'unit',frame.candidates.byte(low16(frame.target_y)),1)
        frame=_calendar_compare_fields(memory,frame,low16(frame.unit),low16(frame.distance))
        if frame.status&4:
            frame=_calendar_write_fields(memory,frame,0xFFFFF646,low16(frame.target_y))
            from .business_reuse import _calendar_memory_arithmetic_fields
            frame=_calendar_memory_arithmetic_fields(memory,frame,0xFFFFF646,1)
            frame=_calendar_write_fields(memory,frame,0xFFFFF376,low16(frame.unit))
            frame=_calendar_test_fields(memory,frame,low16(frame.count))
            if frame.status&4:
                frame=_calendar_move_fields(memory,frame,'unit',178)
                frame=_calendar_call_fields(memory,frame,0x17058,heading_token)
                frame=_calendar_move_fields(memory,frame,'count',1,4)
            frame=_calendar_move_fields(memory,frame,'unit',detail_message)
            frame=_calendar_call_fields(memory,frame,0x17058,detail_token)
        frame=_calendar_arithmetic_fields(memory,frame,'target_x',1)
def show_first_calendar_event_values_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_event_owner_values_fields(memory,frame,0x17158,0x17196,0x171A0,174)
def show_second_calendar_event_values_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_event_owner_values_fields(memory,frame,0x172F4,0x17332,0x1733C,175)
def show_third_calendar_event_values_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    return _calendar_event_owner_values_fields(memory,frame,0x17426,0x17464,0x1746E,179)
def _calendar_seasonal_submission_fields(memory,frame,entry,blocks,target):
    """Read each original month comparison live, including the repeated month 6."""
    frame=_calendar_frame_fields(memory,frame,entry)
    frame=_calendar_move_fields(memory,frame,'target_x',0,4)
    frame=_calendar_move_fields(memory,frame,'target_y',0,4)
    while True:
        for month,cities in blocks:
            frame=_calendar_compare_fields(memory,frame,memory.state.read(0xFFFFF375,1),month,1)
            if frame.status&4:
                for city,token in cities:
                    frame=_calendar_compare_fields(memory,frame,low16(frame.target_x),city)
                    if frame.status&4:frame=_calendar_call_fields(memory,frame,target,token)
        frame=_calendar_arithmetic_fields(memory,frame,'target_x',1)
        frame=_calendar_compare_fields(memory,frame,low16(frame.target_x),39)
        if not frame.status&1:return frame
def _calendar_event_display_fields(memory,frame,scene,load_token,message,message_token,
        values_target,value_tokens,clear_pc):
    frame=_calendar_compare_fields(memory,frame,memory.state.read(0xFFFFD420,1),255,1)
    if frame.status&4:return frame
    frame=_calendar_write_fields(memory,frame,0x00FF7026,scene)
    frame=_calendar_call_fields(memory,frame,0x1072C,load_token)
    frame=_calendar_move_fields(memory,frame,'unit',message)
    frame=_calendar_call_fields(memory,frame,0x17058,message_token)
    frame=_calendar_test_fields(memory,frame,memory.state.read(0xFFFFD448,2))
    if frame.status&4:
        for address,token in ((0xFFFFF67A,value_tokens[0]),(0xFFFFF67C,value_tokens[1]),(0xFFFFF67E,value_tokens[2])):
            frame=_calendar_move_fields(memory,frame,'distance',memory.state.read(address,2))
            frame=_calendar_call_fields(memory,frame,values_target,token)
    return _calendar_clear_event_plane_fields(memory,frame,clear_pc)
def process_first_calendar_event_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    """Original schedule has two separate month-6 blocks; both remain in order."""
    blocks=((5,((5,0x17094),(8,0x1709E),(14,0x170A8))),
        (6,((5,0x170BA),(8,0x170C4),(14,0x170CE))),
        (6,((5,0x170E0),(8,0x170EA),(14,0x170F4))))
    frame=_calendar_seasonal_submission_fields(memory,frame,0x1707E,blocks,0x171A6)
    return _calendar_event_display_fields(memory,frame,35,0x17112,176,0x1711A,0x17158,
        (0x17128,0x17130,0x17138),0x17138)
def process_second_calendar_event_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    blocks=((9,((4,0x17212),(6,0x1721C),(7,0x17226))),
        (8,((13,0x17238),(16,0x17242),(17,0x1724C))),
        (4,((18,0x1725E),(21,0x17268),(22,0x17272))),
        (3,((26,0x17284),(31,0x1728E))))
    frame=_calendar_seasonal_submission_fields(memory,frame,0x171FC,blocks,0x17342)
    return _calendar_event_display_fields(memory,frame,37,0x172AE,177,0x172B6,0x172F4,
        (0x172C4,0x172CC,0x172D4),0x172D4)
def process_third_calendar_event_fields(memory: SceneRefreshMemory,frame: FirstDeploymentFrame)->FirstDeploymentFrame:
    frame=_calendar_frame_fields(memory,frame,0x173A6)
    frame=_calendar_move_fields(memory,frame,'target_x',0,4)
    frame=_calendar_move_fields(memory,frame,'target_y',0,4)
    while True:
        frame=_calendar_bit_fields(memory,frame,memory.state.read(0xFFFFF375,1),1)
        if frame.status&4:
            frame=first_replace(frame,roster=memory.cursor_at(0xFFFFF428))
            frame=_calendar_move_fields(memory,frame,'choice',frame.roster.byte(low16(frame.target_x)),1)
            if not frame.status&8:
                for address in (0xFFFFF67A,0xFFFFF67C,0xFFFFF67E):
                    frame=_calendar_compare_fields(memory,frame,low16(frame.choice),memory.state.read(address,2))
                    if frame.status&4:
                        frame=_calendar_call_fields(memory,frame,0x17474,0x173D2)
                        break
        frame=_calendar_arithmetic_fields(memory,frame,'target_x',1)
        frame=_calendar_compare_fields(memory,frame,low16(frame.target_x),39)
        if not frame.status&1:break
    frame=_calendar_test_fields(memory,frame,memory.state.read(0xFFFFD448,2))
    if not frame.status&4:return frame
    frame=_calendar_write_fields(memory,frame,0x00FF7026,39)
    frame=_calendar_call_fields(memory,frame,0x1072C,0x173EE)
    for address,token in ((0xFFFFF67A,0x173F6),(0xFFFFF67C,0x173FE),(0xFFFFF67E,0x17406)):
        frame=_calendar_move_fields(memory,frame,'distance',memory.state.read(address,2))
        frame=_calendar_call_fields(memory,frame,0x17426,token)
    return _calendar_clear_event_plane_fields(memory,frame,0x17406)

def _calendar_legacy_context_fields(state,retained,kind):
    checked_state(state)
    if kind=='calendar':
        if type(retained) is not CalendarContext:raise ValueError('original calendar context required')
    elif kind=='mortality':
        if type(retained) is not MortalityContext:raise ValueError('original mortality context required')
    elif kind=='event':
        if type(retained) is not EventContext:raise ValueError('original event context required')
    else:raise ValueError('closed historical calendar context role required')
    from .business_reuse import _calendar_legacy_entry_fields
    return _calendar_legacy_entry_fields(state)
