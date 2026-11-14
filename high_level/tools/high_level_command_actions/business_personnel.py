"""Personnel command outcomes and live city-resource consequences.

Roles such as recruitment and policy are probable from the original callers;
the named storage, read/write widths, conditional paths and arithmetic below
are confirmed source behavior.  No rule repairs original wrapping, division
overflow, live aliases, or unusual reads of a parameter source's neighbours.
"""
from .domain import (
    GameState, Long, Word, checked_state, descending_inclusive,
    divu_retained, high16, low8, low16, negative_word, replace_byte,
    replace_word, s8, s16, swap_words, u8, u16, u32, uint,
)
from .contexts_personnel import RecruitmentScore
from .business_reuse import (
    add_progress_be, build_roster, choose_city_head,
    commit_mutual_relationship, debit_city_gold, education_factor,
    prepare_message, split_progress, step_random,
)


from .contexts_personnel import CommandFrame, PersonnelMemory, _command_binary_fields, _personnel_and_fields, _personnel_arithmetic_fields, _personnel_call_fields, _personnel_compare_fields, _personnel_db_fields, _personnel_ext_word_fields, _personnel_indexed_address, _personnel_legacy_entry, _personnel_load_fields, _personnel_memory_arithmetic_fields, _personnel_product_fields, _personnel_quotient_fields, _personnel_read_fields, _personnel_shift_fields, _personnel_store_fields, _personnel_swap_fields, _personnel_test_fields
from .domain import Boundary
from .business_reuse import _personnel_progress_cap_fields

def execute_officer_loyalty_reward(state: GameState, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 58770)
    actual = execute_officer_loyalty_reward_frame_fields(memory, entered)
    return None


def execute_mutual_officer_relationship_reward(state: GameState, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 59960)
    actual = execute_mutual_officer_relationship_reward_frame_fields(memory, entered)
    return None


def execute_officer_policy_outcome(state: GameState, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 60950)
    actual = execute_officer_policy_outcome_frame_fields(memory, entered)
    return None


def reduce_selected_officer_disposition_randomly(state: GameState, entry_frame: CommandFrame | None=None) -> Word:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 61312)
    actual = reduce_selected_officer_disposition_randomly_frame_fields(memory, entered)
    return actual.data[0] & 65535


def reduce_chosen_force_head_disposition_randomly(state: GameState, entry_frame: CommandFrame | None=None) -> Word:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 61348)
    actual = reduce_chosen_force_head_disposition_randomly_frame_fields(memory, entered)
    return actual.data[0] & 65535


def credit_selected_officer_policy_progress(state: GameState, entry_frame: CommandFrame | None=None) -> Word:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 61410)
    actual = credit_selected_officer_policy_progress_frame_fields(memory, entered)
    return actual.data[0] & 65535


def execute_officer_recruitment_outcome(state: GameState, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 63352)
    actual = execute_officer_recruitment_outcome_frame_fields(memory, entered)
    return None


def score_selected_officer_recruitment(state: GameState, entry_frame: CommandFrame | None=None) -> Long:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 63450)
    actual = score_selected_officer_recruitment_frame_fields(memory, entered)
    return actual.data[2]


def bucket_recruitment_score(score: Long, entry_frame: CommandFrame | None=None, state: GameState | None=None) -> RecruitmentScore:
    """Compatibility projection of the sole complete field algorithm."""
    if state is None:
        raise Boundary('historical value-only score API lacks actual memory/full carriers; supply state and entry_frame')
    memory, entered = _personnel_legacy_entry(state, entry_frame, 63532)
    uint(score, 32)
    if score != entered.data[2]:
        raise ValueError('compatibility score/gain must match real incoming D2')
    actual = bucket_recruitment_score_frame_fields(memory, entered)
    return RecruitmentScore(actual.data[2], actual.data[3] & 65535, actual.data[4] & 65535)


def apply_recruited_officer_roster_transition(state: GameState, score: Long, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 63638)
    uint(score, 32)
    if score != entered.data[2]:
        raise ValueError('compatibility score/gain must match real incoming D2')
    actual = apply_recruited_officer_roster_transition_frame_fields(memory, entered)
    return None


def apply_recruitment_city_resource_losses(state: GameState, bucket: Word, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 63952)
    uint(bucket, 16)
    if bucket != entered.data[4] & 65535:
        raise ValueError('compatibility bucket must match real incoming D4 WORD')
    actual = apply_recruitment_city_resource_losses_frame_fields(memory, entered)
    return None


def reduce_recruitment_city_food(state: GameState, city_offset: Word, bucket: Word, entry_frame: CommandFrame | None=None) -> Long:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 63978)
    uint(bucket, 16)
    if bucket != entered.data[4] & 65535:
        raise ValueError('compatibility bucket must match real incoming D4 WORD')
    uint(city_offset, 16)
    if city_offset != entered.data[2] & 65535:
        raise ValueError('compatibility city offset must match real incoming D2 WORD')
    actual = reduce_recruitment_city_food_frame_fields(memory, entered)
    return actual.data[3]


def reduce_recruitment_city_gold(state: GameState, city_offset: Word, bucket: Word, entry_frame: CommandFrame | None=None) -> Long:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 64058)
    uint(bucket, 16)
    if bucket != entered.data[4] & 65535:
        raise ValueError('compatibility bucket must match real incoming D4 WORD')
    uint(city_offset, 16)
    if city_offset != entered.data[2] & 65535:
        raise ValueError('compatibility city offset must match real incoming D2 WORD')
    actual = reduce_recruitment_city_gold_frame_fields(memory, entered)
    return actual.data[3]


def reduce_recruitment_city_state_parameter(state: GameState, city_offset: Word, bucket: Word, entry_frame: CommandFrame | None=None) -> Long:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 64138)
    uint(bucket, 16)
    if bucket != entered.data[4] & 65535:
        raise ValueError('compatibility bucket must match real incoming D4 WORD')
    uint(city_offset, 16)
    if city_offset != entered.data[2] & 65535:
        raise ValueError('compatibility city offset must match real incoming D2 WORD')
    actual = reduce_recruitment_city_state_parameter_frame_fields(memory, entered)
    return actual.data[3]


def draw_recruitment_probability(state: GameState, entry_frame: CommandFrame | None=None) -> Word:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 64224)
    actual = draw_recruitment_probability_frame_fields(memory, entered)
    return actual.data[0] & 65535

def _personnel_visible_force_fields(memory, frame):
    """All three parents use the same ordered comparison short-circuit."""
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF376)
    for address in (0xFFFFF67A,0xFFFFF67C,0xFFFFF67E):
        frame = _personnel_compare_fields(memory,frame,frame.data[0]&0xFFFF,
            memory.state.read(address,2))
        if frame.status_word&4:
            return frame,True
    return frame,False

def execute_officer_loyalty_reward_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """E592 complete education, capped loyalty/disposition/progress and result packet."""
    frame = memory.enter(frame)
    frame = _personnel_call_fields(memory,frame,0xE70A,0xE596)
    frame = frame.with_address(0,0xFFFFC300)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF630)
    frame = _personnel_compare_fields(memory,frame,frame.data[0]&0xFFFF,
        memory.state.read(0xFFFFF3A6,2))
    special_teacher = bool(frame.status_word&4)
    if not special_teacher:
        frame = _personnel_compare_fields(memory,frame,frame.data[0]&0xFFFF,
            memory.state.read(0xFFFFF634,2))
        special_teacher = bool(frame.status_word&4)
    if special_teacher:
        frame = _personnel_load_fields(memory,frame,0,100)
    else:
        frame = _personnel_read_fields(memory,frame,0,_personnel_indexed_address(frame,0,0),8)
        frame = _personnel_ext_word_fields(memory,frame,0)
    frame = _personnel_read_fields(memory,frame,1,0xFFFFF3A6)
    frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,1),8)
    frame = _personnel_ext_word_fields(memory,frame,1)
    frame = _personnel_call_fields(memory,frame,0xE71E,0xE5C6)
    frame = _personnel_read_fields(memory,frame,3,0xFFFFF39E,32)
    frame = _personnel_shift_fields(memory,frame,3,1,32)
    frame = _personnel_read_fields(memory,frame,4,0xFFFFF3A6)
    frame = _personnel_shift_fields(memory,frame,4,1)
    frame = frame.with_address(0,0xFFFFB600)
    frame = _personnel_read_fields(memory,frame,5,_personnel_indexed_address(frame,0,4))
    frame = _personnel_product_fields(memory,frame,5,10)
    frame = _personnel_arithmetic_fields(memory,frame,3,frame.data[5],32)
    frame = frame.with_address(0,0xFFFFBE00)
    frame = _personnel_read_fields(memory,frame,4,_personnel_indexed_address(frame,0,4))
    frame = _personnel_product_fields(memory,frame,4,5)
    frame = _personnel_arithmetic_fields(memory,frame,3,frame.data[4],32)
    frame = _personnel_read_fields(memory,frame,4,0xFFFFF3A6)
    frame = frame.with_address(0,0xFFFFC200)
    frame = _personnel_load_fields(memory,frame,7,0)
    frame = _personnel_read_fields(memory,frame,7,_personnel_indexed_address(frame,0,4),8)
    frame = _personnel_compare_fields(memory,frame,frame.data[7]&0xFFFF,30)
    if frame.status_word&5:
        frame = _personnel_shift_fields(memory,frame,3,1,16,True)
    frame = _personnel_load_fields(memory,frame,4,0,32)
    frame = _personnel_read_fields(memory,frame,4,0xFFFFF61C)
    frame = _personnel_load_fields(memory,frame,5,frame.data[4],32)
    frame = _personnel_shift_fields(memory,frame,4,1,32)
    frame = _personnel_arithmetic_fields(memory,frame,4,frame.data[5],32)
    frame = _personnel_swap_fields(memory,frame,4)
    frame = _personnel_arithmetic_fields(memory,frame,4,frame.data[2]&0xFFFF)
    frame = _personnel_product_fields(memory,frame,4,frame.data[7]&0xFFFF)
    frame = _personnel_load_fields(memory,frame,5,frame.data[3]&0xFFFF)
    frame = _personnel_product_fields(memory,frame,5,frame.data[4]&0xFFFF)
    frame = _personnel_swap_fields(memory,frame,3)
    frame = _personnel_product_fields(memory,frame,3,frame.data[4]&0xFFFF)
    frame = _personnel_swap_fields(memory,frame,3)
    frame = _personnel_arithmetic_fields(memory,frame,3,frame.data[5],32)
    frame = _personnel_quotient_fields(memory,frame,3,10000,0xE622)
    frame = _personnel_and_fields(memory,frame,3,0xFFFF,32)
    frame = _personnel_quotient_fields(memory,frame,3,60,0xE62C)
    frame = _personnel_store_fields(memory,frame,0xFFFFF3C8,0,16,True)
    frame = _personnel_store_fields(memory,frame,0xFFFFF3CA,frame.data[3]&0xFFFF)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
    frame = frame.with_address(0,0xFFFFC300)
    frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,0),8)
    frame = _personnel_ext_word_fields(memory,frame,1)
    frame = _personnel_arithmetic_fields(memory,frame,1,frame.data[3]&0xFFFF)
    frame = _personnel_compare_fields(memory,frame,frame.data[1]&0xFFFF,100)
    if not frame.status_word&5:
        frame = _personnel_load_fields(memory,frame,2,frame.data[1]&0xFFFF)
        frame = _personnel_arithmetic_fields(memory,frame,2,100,16,True)
        frame = _personnel_memory_arithmetic_fields(memory,frame,0xFFFFF3CA,frame.data[2]&0xFFFF,16,True)
        frame = _personnel_load_fields(memory,frame,1,100)
    frame = _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,0),frame.data[1]&255,8)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF630)
    frame = _personnel_compare_fields(memory,frame,frame.data[0]&0xFFFF,
        memory.state.read(0xFFFFF3A6,2))
    if frame.status_word&4:
        frame = _personnel_read_fields(memory,frame,0,0xFFFFF634)
    frame = frame.with_address(0,0xFFFFC200)
    frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,0),8)
    frame = _personnel_arithmetic_fields(memory,frame,1,1,8)
    frame = _personnel_compare_fields(memory,frame,frame.data[1]&255,100,8)
    if not frame.status_word&5:
        frame = _personnel_load_fields(memory,frame,1,100,8)
    frame = _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,0),frame.data[1]&255,8)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = frame.with_address(0,0xFFFFBE00)
    frame = _personnel_shift_fields(memory,frame,3,1,16,True)
    frame = _personnel_arithmetic_fields(memory,frame,3,
        memory.state.read(_personnel_indexed_address(frame,0,0),2))
    frame = _personnel_compare_fields(memory,frame,frame.data[3]&0xFFFF,999)
    if not frame.status_word&5:
        frame = _personnel_load_fields(memory,frame,3,999)
    frame = _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,0),frame.data[3]&0xFFFF)
    frame = frame.with_address(0,0xFFFFCD00)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
    frame = _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,0),1,8)
    frame,visible = _personnel_visible_force_fields(memory,frame)
    if visible:
        frame = _personnel_store_fields(memory,frame,0x00FF7026,22)
        value = memory.state.read(0xFFFFF3CA,2)
        frame = _personnel_test_fields(memory,frame,value)
        frame = _personnel_load_fields(memory,frame,0,168 if frame.status_word&4 else 167)
        frame = _personnel_store_fields(memory,frame,0xFFFFF3FE,frame.data[0]&0xFFFF)
        frame = _personnel_store_fields(memory,frame,0xFFFFF612,memory.state.read(0xFFFFF38A,2))
        frame = _personnel_store_fields(memory,frame,0xFFFFF612,memory.state.read(0xFFFFF38A,2))
        frame = _personnel_store_fields(memory,frame,0xFFFFF362,40)
        frame = _personnel_store_fields(memory,frame,0xFFFFF3D0,memory.state.read(0xFFFFF3A6,2))
    return memory.finish(frame)

def _personnel_relationship_progress_fields(memory, frame, carrier, bonus, head, random_token):
    """One repeated RNG/seed-times-three stage; real callers choose carrier/bonus."""
    frame = _personnel_call_fields(memory,frame,0x83D4,random_token)
    frame = _personnel_load_fields(memory,frame,carrier,0,32)
    frame = _personnel_read_fields(memory,frame,carrier,0xFFFFF61C)
    frame = _personnel_load_fields(memory,frame,1,frame.data[carrier],32)
    frame = _personnel_shift_fields(memory,frame,carrier,1,32)
    frame = _personnel_arithmetic_fields(memory,frame,carrier,frame.data[1],32)
    if bonus in (5,10):
        frame = _personnel_shift_fields(memory,frame,carrier,1,32)
    frame = _personnel_swap_fields(memory,frame,carrier)
    frame = _personnel_arithmetic_fields(memory,frame,carrier,bonus)
    if head:
        frame = _personnel_read_fields(memory,frame,1,0xFFFFF376)
        frame = _personnel_shift_fields(memory,frame,1,1)
        frame = frame.with_address(0,0xFFFFE640)
        frame = _personnel_read_fields(memory,frame,0 if carrier==2 else 2,
            _personnel_indexed_address(frame,0,1))
        slot = 0 if carrier==2 else 2
        frame = _personnel_shift_fields(memory,frame,slot,1)
    else:
        slot = 2
        frame = _personnel_read_fields(memory,frame,slot,0xFFFFF3A6)
        frame = _personnel_shift_fields(memory,frame,slot,1)
    frame = frame.with_address(0,0xFFFFBE00)
    frame = _personnel_arithmetic_fields(memory,frame,carrier,
        memory.state.read(_personnel_indexed_address(frame,0,slot),2))
    frame = _personnel_compare_fields(memory,frame,frame.data[carrier]&0xFFFF,999)
    if not frame.status_word&5:
        frame = _personnel_load_fields(memory,frame,carrier,999)
    return _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,slot),frame.data[carrier]&0xFFFF)

def execute_mutual_officer_relationship_reward_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """EA38 actual mutual bit commit or disposition loss, then result message."""
    frame = memory.enter(frame)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
    frame = frame.with_address(0,0xFFFFC700)
    frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,0),8)
    frame = _personnel_and_fields(memory,frame,1,7,8)
    frame = _personnel_ext_word_fields(memory,frame,1)
    frame = _personnel_load_fields(memory,frame,3,frame.data[1]&0xFFFF)
    frame = _personnel_arithmetic_fields(memory,frame,3,2)
    frame = frame.with_address(0,0xEC5C)
    frame = _personnel_read_fields(memory,frame,2,_personnel_indexed_address(frame,0,1),8)
    frame = _personnel_ext_word_fields(memory,frame,2)
    frame = _personnel_load_fields(memory,frame,1,0,32)
    frame = _personnel_read_fields(memory,frame,1,0xFFFFF61C)
    frame = _personnel_product_fields(memory,frame,1,frame.data[3]&0xFFFF)
    frame = _personnel_swap_fields(memory,frame,1)
    frame = _personnel_arithmetic_fields(memory,frame,1,frame.data[2]&0xFFFF)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = frame.with_address(0,0xFFFFB600)
    frame = _personnel_read_fields(memory,frame,2,_personnel_indexed_address(frame,0,0))
    frame = _personnel_product_fields(memory,frame,1,frame.data[2]&0xFFFF)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF376)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = frame.with_address(0,0xFFFFE640)
    frame = _personnel_read_fields(memory,frame,2,_personnel_indexed_address(frame,0,0))
    frame = frame.with_address(0,0xFFFFC200)
    frame = _personnel_load_fields(memory,frame,3,0)
    frame = _personnel_read_fields(memory,frame,3,_personnel_indexed_address(frame,0,2),8)
    frame = _personnel_load_fields(memory,frame,2,120)
    frame = _personnel_arithmetic_fields(memory,frame,2,frame.data[3]&0xFFFF,16,True)
    frame = _personnel_quotient_fields(memory,frame,1,frame.data[2]&0xFFFF,0xEA90)
    frame = _personnel_compare_fields(memory,frame,frame.data[1]&0xFFFF,10)
    if not frame.status_word&1:
        frame = _personnel_call_fields(memory,frame,0xEC16,0xEA9E)
        frame = _personnel_store_fields(memory,frame,0xFFFFF3FE,38)
        frame = _personnel_store_fields(memory,frame,0xFFFFF3D0,memory.state.read(0xFFFFF3A6,2))
        frame = _personnel_relationship_progress_fields(memory,frame,0,5,True,0xEAB0)
        frame = _personnel_relationship_progress_fields(memory,frame,0,10,False,0xEAF0)
    else:
        frame = _personnel_store_fields(memory,frame,0xFFFFF3FE,40)
        frame = _personnel_relationship_progress_fields(memory,frame,2,1,True,0xEB32)
        frame = _personnel_call_fields(memory,frame,0x83D4,0xEB70)
        frame = _personnel_load_fields(memory,frame,2,0,32)
        frame = _personnel_read_fields(memory,frame,2,0xFFFFF61C)
        frame = _personnel_load_fields(memory,frame,1,frame.data[2],32)
        frame = _personnel_shift_fields(memory,frame,2,1,32)
        frame = _personnel_arithmetic_fields(memory,frame,2,frame.data[1],32)
        frame = _personnel_swap_fields(memory,frame,2)
        frame = _personnel_arithmetic_fields(memory,frame,2,1)
        frame = _personnel_call_fields(memory,frame,0x83D4,0xEB86)
        frame = _personnel_load_fields(memory,frame,3,0,32)
        frame = _personnel_read_fields(memory,frame,3,0xFFFFF61C)
        frame = _personnel_load_fields(memory,frame,1,frame.data[3],32)
        frame = _personnel_shift_fields(memory,frame,3,1,32)
        frame = _personnel_arithmetic_fields(memory,frame,3,frame.data[1],32)
        frame = _personnel_swap_fields(memory,frame,3)
        frame = _personnel_read_fields(memory,frame,1,0xFFFFF3A6)
        frame = frame.with_address(0,0xFFFFC200)
        address = _personnel_indexed_address(frame,0,1)
        frame = _personnel_memory_arithmetic_fields(memory,frame,address,frame.data[3]&255,8,True)
        if frame.status_word&1:
            frame = _personnel_store_fields(memory,frame,address,0,8,True)
        frame = _personnel_shift_fields(memory,frame,1,1)
        frame = frame.with_address(0,0xFFFFBE00)
        frame = _personnel_arithmetic_fields(memory,frame,2,
            memory.state.read(_personnel_indexed_address(frame,0,1),2))
        frame = _personnel_compare_fields(memory,frame,frame.data[2]&0xFFFF,999)
        if not frame.status_word&5:
            frame = _personnel_load_fields(memory,frame,2,999)
        frame = _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,1),frame.data[2]&0xFFFF)
    frame,visible = _personnel_visible_force_fields(memory,frame)
    if visible:
        frame = _personnel_store_fields(memory,frame,0x00FF7026,12)
        frame = _personnel_store_fields(memory,frame,0xFFFFF612,520)
        frame = _personnel_store_fields(memory,frame,0xFFFFF362,40)
        frame = _personnel_load_fields(memory,frame,0,37)
        frame = _personnel_store_fields(memory,frame,0xFFFFF3D0,memory.state.read(0xFFFFF3A6,2))
        frame = _personnel_call_fields(memory,frame,0x676F2,0xEC00)
        # The original EBD8 branch skips this action-byte update when no notice is visible.
        frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
        frame = frame.with_address(0,0xFFFFCD00)
        frame = _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,0),1,8)
    frame = _personnel_store_fields(memory,frame,0xFFFFF608,120)
    return memory.finish(frame)

def execute_officer_policy_outcome_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """EE16 live target head exclusion, signed policy score, ordered failure children."""
    frame = memory.enter(frame)
    frame = _personnel_store_fields(memory,frame,0xFFFFF3C8,0,32,True)
    frame = frame.with_address(0,0xFFFFCC00)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3F2)
    frame = _personnel_read_fields(memory,frame,0,_personnel_indexed_address(frame,0,0),8)
    frame = frame.with_address(0,0xFFFFF427)
    frame = _personnel_read_fields(memory,frame,0,_personnel_indexed_address(frame,0,0),8)
    frame = frame.with_address(0,0xFFFFE640)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = _personnel_read_fields(memory,frame,0,_personnel_indexed_address(frame,0,0))
    frame = _personnel_compare_fields(memory,frame,frame.data[0]&0xFFFF,
        memory.state.read(0xFFFFF3F2,2))
    failed = bool(frame.status_word&4)
    if not failed:
        frame = _personnel_read_fields(memory,frame,0,0xFFFFF3F2)
        frame = frame.with_address(0,0xFFFFC300)
        frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,0),8)
        failed = bool(frame.status_word&4)
    if not failed:
        frame = _personnel_ext_word_fields(memory,frame,1)
        frame = _personnel_arithmetic_fields(memory,frame,1,50,16,True)
        if frame.status_word&1:
            frame,absolute = _command_binary_fields(memory,frame,0,frame.data[1]&0xFFFF,16,True)
            frame = frame.with_data(1,absolute,16)
        frame = _personnel_load_fields(memory,frame,2,60)
        frame = _personnel_arithmetic_fields(memory,frame,2,frame.data[1]&0xFFFF,16,True)
        frame = _personnel_read_fields(memory,frame,1,0xFFFFF3A6)
        frame = frame.with_address(1,0xFFFFC700)
        frame = _personnel_read_fields(memory,frame,3,_personnel_indexed_address(frame,1,1),8)
        frame = _personnel_and_fields(memory,frame,3,7)
        frame = _personnel_read_fields(memory,frame,3,u32(0xEE11+s16(frame.data[3]&0xFFFF)),8)
        frame = _personnel_load_fields(memory,frame,4,0,32)
        frame = _personnel_read_fields(memory,frame,4,0xFFFFF61C)
        frame = _personnel_load_fields(memory,frame,5,frame.data[4],32)
        frame = _personnel_shift_fields(memory,frame,4,2,32)
        frame = _personnel_arithmetic_fields(memory,frame,4,frame.data[5],32)
        frame = _personnel_shift_fields(memory,frame,4,2,32)
        frame = _personnel_swap_fields(memory,frame,4)
        frame = _personnel_arithmetic_fields(memory,frame,4,frame.data[3]&0xFFFF)
        frame = _personnel_shift_fields(memory,frame,1,1)
        frame = frame.with_address(0,0xFFFFB600)
        frame = _personnel_read_fields(memory,frame,3,_personnel_indexed_address(frame,0,1))
        frame = _personnel_arithmetic_fields(memory,frame,3,frame.data[4]&0xFFFF)
        frame = _personnel_read_fields(memory,frame,0,0xFFFFF3F2)
        frame = frame.with_address(0,0xFFFFC700)
        frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,0),8)
        frame = _personnel_and_fields(memory,frame,1,7)
        frame = frame.with_address(1,0xEE0C)
        frame = _personnel_read_fields(memory,frame,4,_personnel_indexed_address(frame,1,1),8)
        frame = _personnel_shift_fields(memory,frame,0,1)
        frame = frame.with_address(1,0xFFFFB600)
        frame = _personnel_arithmetic_fields(memory,frame,4,
            memory.state.read(_personnel_indexed_address(frame,1,0),2))
        frame = _personnel_arithmetic_fields(memory,frame,3,frame.data[4]&0xFFFF,16,True)
        failed = bool(frame.status_word&1)
    if not failed:
        frame = _personnel_product_fields(memory,frame,2,frame.data[3]&0xFFFF,True)
        frame = frame.with_address(1,0xDF08)
        frame = _personnel_read_fields(memory,frame,3,0xFFFFEFD2)
        frame = _personnel_shift_fields(memory,frame,3,1)
        frame = _personnel_quotient_fields(memory,frame,2,
            memory.state.read(_personnel_indexed_address(frame,1,3),2),0xEEC6)
        frame = _personnel_test_fields(memory,frame,frame.data[2]&0xFFFF)
        failed = bool(frame.status_word&4)
    if failed:
        frame = _personnel_call_fields(memory,frame,0xEF80,0xEF0C)
        frame = _personnel_call_fields(memory,frame,0xEFA4,0xEF10)
        frame = _personnel_call_fields(memory,frame,0xEFE2,0xEF14)
        frame = _personnel_store_fields(memory,frame,0xFFFFF3FE,58)
    else:
        frame = _personnel_compare_fields(memory,frame,frame.data[2]&0xFFFF,40)
        if not frame.status_word&5:
            frame = _personnel_load_fields(memory,frame,2,40)
        frame = _personnel_store_fields(memory,frame,0xFFFFF3C8,0,16,True)
        frame = _personnel_store_fields(memory,frame,0xFFFFF3CA,frame.data[2]&0xFFFF)
        frame = _personnel_read_fields(memory,frame,0,0xFFFFF3F2)
        frame = frame.with_address(0,0xFFFFC300)
        address = _personnel_indexed_address(frame,0,0)
        frame = _personnel_memory_arithmetic_fields(memory,frame,address,frame.data[2]&255,8,True)
        if frame.status_word&1:
            frame = _personnel_store_fields(memory,frame,address,0,8,True)
        frame = _personnel_call_fields(memory,frame,0xEF60,0xEEF8)
        frame = _personnel_store_fields(memory,frame,0xFFFFF3D2,memory.state.read(0xFFFFF3F2,2))
        frame = _personnel_store_fields(memory,frame,0xFFFFF3FE,57)
    frame,visible = _personnel_visible_force_fields(memory,frame)
    if visible:
        frame = _personnel_store_fields(memory,frame,0xFFFFF38A,520)
        frame = _personnel_store_fields(memory,frame,0xFFFFF362,40)
        frame = _personnel_store_fields(memory,frame,0xFFFFF608,120)
        frame = _personnel_store_fields(memory,frame,0xFFFFF612,520)
        frame = _personnel_store_fields(memory,frame,0xFFFFF3D0,memory.state.read(0xFFFFF3A6,2))
        frame = _personnel_load_fields(memory,frame,0,9)
        frame = _personnel_call_fields(memory,frame,0x676F2,0xEF5E)
    return memory.finish(frame)

def reduce_selected_officer_disposition_randomly_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """EF80 subtract the actual RNG-derived low BYTE, then original CLR on borrow."""
    frame = memory.enter(frame)
    frame = _personnel_call_fields(memory,frame,0x83D4,0xEF86)
    frame = _personnel_and_fields(memory,frame,0,0xFFFF,32)
    frame = _personnel_shift_fields(memory,frame,0,2,32)
    frame = _personnel_swap_fields(memory,frame,0)
    frame = _personnel_read_fields(memory,frame,1,0xFFFFF3A6)
    frame = frame.with_address(0,0xFFFFC200)
    address = _personnel_indexed_address(frame,0,1)
    frame = _personnel_memory_arithmetic_fields(memory,frame,address,frame.data[0]&255,8,True)
    if frame.status_word&1:
        frame = _personnel_store_fields(memory,frame,address,0,8,True)
    return memory.finish(frame)

def reduce_chosen_force_head_disposition_randomly_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """EFA4 the chosen city's owner selects a live head; full carriers remain visible."""
    frame = memory.enter(frame)
    frame = _personnel_call_fields(memory,frame,0x83D4,0xEFAA)
    frame = _personnel_and_fields(memory,frame,0,0xFFFF,32)
    frame = _personnel_load_fields(memory,frame,1,frame.data[0],32)
    frame = _personnel_shift_fields(memory,frame,0,1,32)
    frame = _personnel_arithmetic_fields(memory,frame,0,frame.data[1],32)
    frame = _personnel_swap_fields(memory,frame,0)
    frame = _personnel_read_fields(memory,frame,1,0xFFFFF392)
    frame = frame.with_address(0,0xFFFFF427)
    frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,1),8)
    frame = _personnel_and_fields(memory,frame,1,15)
    frame = _personnel_shift_fields(memory,frame,1,1)
    frame = frame.with_address(0,0xFFFFE640)
    frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,1))
    frame = frame.with_address(0,0xFFFFC200)
    address = _personnel_indexed_address(frame,0,1)
    frame = _personnel_memory_arithmetic_fields(memory,frame,address,frame.data[0]&255,8,True)
    if frame.status_word&1:
        frame = _personnel_store_fields(memory,frame,address,0,8,True)
    return memory.finish(frame)

def credit_selected_officer_policy_progress_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """EFE2 original fresh seed draw, low-WORD progress RMW and distinct cap read."""
    frame = memory.enter(frame)
    frame = _personnel_call_fields(memory,frame,0x83D4,0xEFE8)
    frame = _personnel_load_fields(memory,frame,0,0,32)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF61C)
    frame = _personnel_load_fields(memory,frame,1,frame.data[0],32)
    frame = _personnel_shift_fields(memory,frame,0,1,32)
    frame = _personnel_arithmetic_fields(memory,frame,0,frame.data[1],32)
    frame = _personnel_swap_fields(memory,frame,0)
    frame = _personnel_arithmetic_fields(memory,frame,0,1)
    frame = _personnel_read_fields(memory,frame,1,0xFFFFF3A6)
    frame = _personnel_shift_fields(memory,frame,1,1)
    frame = frame.with_address(0,0xFFFFBE00)
    frame = _personnel_progress_cap_fields(memory,frame,
        _personnel_indexed_address(frame,0,1),frame.data[0]&0xFFFF)
    return memory.finish(frame)

def score_selected_officer_recruitment_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """F7DA ability/strength plus the live policy sample minus the selected city head."""
    frame = memory.enter(frame)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = frame.with_address(0,0xFFFFC000)
    frame = _personnel_load_fields(memory,frame,2,0,32)
    frame = _personnel_read_fields(memory,frame,2,_personnel_indexed_address(frame,0,0))
    frame = _personnel_quotient_fields(memory,frame,2,10,0xF7EA)
    frame = frame.with_address(0,0xFFFFB600)
    frame = _personnel_arithmetic_fields(memory,frame,2,
        memory.state.read(_personnel_indexed_address(frame,0,0),2))
    frame = _personnel_call_fields(memory,frame,0x83D4,0xF7FC)
    frame = frame.with_address(0,0xDF0E)
    frame = _personnel_read_fields(memory,frame,1,0xFFFFEFD2)
    frame = _personnel_shift_fields(memory,frame,1,2)
    frame = _personnel_product_fields(memory,frame,0,
        memory.state.read(_personnel_indexed_address(frame,0,1),2))
    frame = _personnel_swap_fields(memory,frame,0)
    frame = _personnel_arithmetic_fields(memory,frame,0,
        memory.state.read(_personnel_indexed_address(frame,0,1,2),2))
    frame = _personnel_arithmetic_fields(memory,frame,2,frame.data[0]&0xFFFF)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A8)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = frame.with_address(0,0xFFFFF45E)
    frame = _personnel_read_fields(memory,frame,0,_personnel_indexed_address(frame,0,0))
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = frame.with_address(0,0xFFFFB600)
    frame = _personnel_arithmetic_fields(memory,frame,2,
        memory.state.read(_personnel_indexed_address(frame,0,0),2),16,True)
    return memory.finish(frame)

def bucket_recruitment_score_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """F82C the sole eight score bands; high-WORD residue is never rebuilt."""
    frame = memory.enter(frame)
    frame = _personnel_load_fields(memory,frame,3,0)
    frame = _personnel_load_fields(memory,frame,4,0)
    frame = _personnel_test_fields(memory,frame,frame.data[2]&0xFFFF)
    if frame.status_word&12:
        return memory.finish(frame)
    for cutoff,threshold in ((50,10),(100,30),(150,50),(200,60),
            (250,70),(300,80),(350,80)):
        frame = _personnel_load_fields(memory,frame,3,threshold)
        frame = _personnel_arithmetic_fields(memory,frame,4,1)
        frame = _personnel_compare_fields(memory,frame,frame.data[2]&0xFFFF,cutoff)
        if frame.status_word&5:
            return memory.finish(frame)
    frame = _personnel_load_fields(memory,frame,3,85)
    frame = _personnel_arithmetic_fields(memory,frame,4,1)
    frame = _personnel_load_fields(memory,frame,2,351)
    return memory.finish(frame)

def draw_recruitment_probability_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """FAE0 actual repeated shifts/adds retain final SWAP flags and D1 LONG."""
    frame = memory.enter(frame)
    frame = _personnel_call_fields(memory,frame,0x83D4,0xFAE6)
    frame = _personnel_and_fields(memory,frame,0,0xFFFF,32)
    frame = _personnel_load_fields(memory,frame,1,frame.data[0],32)
    frame = _personnel_shift_fields(memory,frame,0,1,32)
    frame = _personnel_arithmetic_fields(memory,frame,0,frame.data[1],32)
    frame = _personnel_shift_fields(memory,frame,0,3,32)
    frame = _personnel_arithmetic_fields(memory,frame,0,frame.data[1],32)
    frame = _personnel_shift_fields(memory,frame,0,2,32)
    frame = _personnel_swap_fields(memory,frame,0)
    return memory.finish(frame)

def _personnel_recruitment_resource_fields(memory, frame, resource):
    """Three original resource roles; food/gold finish the real DIVU/MULU pair.

    FA0E/FA5E DIVU preserves the dividend on overflow. Its undefined
    intermediate N/Z is neither branched on nor exposed: the immediate
    original FA12/FA62 MULU defines NZVC and preserves X before any
    subsequent DATA or return. divu_retained is the existing sole
    division authority; the state-role FAB0/ANDI path stays unchanged.
    """
    if resource == 'food':
        parameter,ledger,continuation = 0xFA16,0xFFFFE0A0,0xF9FC
    elif resource == 'gold':
        parameter,ledger,continuation = 0xFA66,0xFFFFE000,0xFA4C
    elif resource == 'state':
        parameter,ledger,continuation = 0xFABC,0xFFFFE1E0,0xFA9C
    else:
        raise ValueError('original three recruitment resource roles required')
    frame = _personnel_load_fields(memory,frame,5,frame.data[4]&0xFFFF)
    frame = _personnel_shift_fields(memory,frame,5,2)
    frame = frame.with_address(0,parameter)
    frame = _personnel_read_fields(memory,frame,6,_personnel_indexed_address(frame,0,5))
    frame = _personnel_call_fields(memory,frame,0x83D4,continuation)
    frame = _personnel_product_fields(memory,frame,0,frame.data[6]&0xFFFF)
    frame = _personnel_swap_fields(memory,frame,0)
    frame = _personnel_arithmetic_fields(memory,frame,0,
        memory.state.read(_personnel_indexed_address(frame,0,5,2),2))
    frame = frame.with_address(0,ledger)
    frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,2),32)
    if resource == 'state':
        frame = _personnel_load_fields(memory,frame,3,frame.data[1]&0xFFFF)
        frame = _personnel_product_fields(memory,frame,3,frame.data[0]&0xFFFF)
        frame = _personnel_quotient_fields(memory,frame,3,100,0xFAB0)
        frame = _personnel_and_fields(memory,frame,3,0xFFFF,32)
    else:
        frame = _personnel_load_fields(memory,frame,3,frame.data[1],32)
        frame = frame.with_data(3,divu_retained(frame.data[3],100))
        frame = _personnel_product_fields(memory,frame,3,frame.data[0]&0xFFFF)
    return _personnel_memory_arithmetic_fields(memory,frame,
        _personnel_indexed_address(frame,0,2),frame.data[3],32,True)

def reduce_recruitment_city_food_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    frame = memory.enter(frame)
    return memory.finish(_personnel_recruitment_resource_fields(memory,frame,'food'))

def reduce_recruitment_city_gold_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    frame = memory.enter(frame)
    return memory.finish(_personnel_recruitment_resource_fields(memory,frame,'gold'))

def reduce_recruitment_city_state_parameter_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    frame = memory.enter(frame)
    return memory.finish(_personnel_recruitment_resource_fields(memory,frame,'state'))

def apply_recruitment_city_resource_losses_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """F9D0 zero bucket returns; otherwise food, gold then state in original order."""
    frame = memory.enter(frame)
    frame = _personnel_test_fields(memory,frame,frame.data[4]&0xFFFF)
    if frame.status_word&4:
        return memory.finish(frame)
    frame = _personnel_read_fields(memory,frame,2,0xFFFFF3A8)
    frame = _personnel_arithmetic_fields(memory,frame,2,1,16,True)
    frame = _personnel_shift_fields(memory,frame,2,2)
    frame = _personnel_call_fields(memory,frame,0xF9EA,0xF9E0)
    frame = _personnel_call_fields(memory,frame,0xFA3A,0xF9E4)
    frame = _personnel_call_fields(memory,frame,0xFA8A,0xF9E8)
    return memory.finish(frame)

def apply_recruited_officer_roster_transition_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """F896 actual force-head scan, leave-city selection or capped ability progress."""
    frame = memory.enter(frame)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
    frame = frame.with_address(0,0xFFFFE640)
    frame = _personnel_load_fields(memory,frame,3,21)
    force_head_found = False
    while True:
        value = memory.state.read(frame.addresses[0],2)
        frame = frame.with_address(0,frame.addresses[0]+2)
        frame = _personnel_compare_fields(memory,frame,frame.data[0]&0xFFFF,value)
        if frame.status_word&4:
            force_head_found = True
            break
        frame,more_heads = _personnel_db_fields(frame,3)
        if not more_heads:
            break
    award_progress = force_head_found
    if not force_head_found:
        frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
        frame = _personnel_shift_fields(memory,frame,0,1)
        frame = frame.with_address(0,0xFFFFB400)
        frame = _personnel_read_fields(memory,frame,3,_personnel_indexed_address(frame,0,0))
        frame = _personnel_shift_fields(memory,frame,3,1,16,True)
        frame = _personnel_call_fields(memory,frame,0xFAE0,0xF8C0)
        frame = _personnel_compare_fields(memory,frame,frame.data[0]&0xFFFF,frame.data[3]&0xFFFF)
        award_progress = bool(frame.status_word&1)
    if award_progress:
        frame = _personnel_test_fields(memory,frame,frame.data[2]&0xFFFF)
        if frame.status_word&8:
            return memory.finish(frame)
        frame = _personnel_and_fields(memory,frame,2,0xFFFF,32)
        frame = _personnel_quotient_fields(memory,frame,2,10,0xF96C)
        frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
        frame = _personnel_shift_fields(memory,frame,0,1)
        frame = frame.with_address(0,0xFFFFC000)
        frame = _personnel_read_fields(memory,frame,3,_personnel_indexed_address(frame,0,0))
        frame = _personnel_arithmetic_fields(memory,frame,3,frame.data[2]&0xFFFF)
        frame = _personnel_compare_fields(memory,frame,frame.data[3]&0xFFFF,999)
        if not frame.status_word&5:
            frame = _personnel_load_fields(memory,frame,3,999)
        frame = _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,0),frame.data[3]&0xFFFF)
        return memory.finish(frame)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A8)
    frame = _personnel_store_fields(memory,frame,0xFFFFF630,0xFFFF)
    frame = _personnel_call_fields(memory,frame,0x5F48,0xF8D6)
    frame = _personnel_compare_fields(memory,frame,frame.data[3]&0xFFFF,10)
    leave_city = not bool(frame.status_word&1)
    if not leave_city:
        frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
        frame = frame.with_address(0,0xFFFFC300)
        frame = _personnel_load_fields(memory,frame,1,0)
        frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,0),8)
        frame = _personnel_load_fields(memory,frame,2,100)
        frame = _personnel_arithmetic_fields(memory,frame,2,frame.data[1]&0xFFFF,16,True)
        frame = _personnel_read_fields(memory,frame,1,0xFFFFF3A8)
        frame = _personnel_shift_fields(memory,frame,1,1)
        frame = frame.with_address(0,0xFFFFF45E)
        frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,1))
        frame = _personnel_load_fields(memory,frame,0,0)
        frame = frame.with_address(0,0xFFFFC200)
        frame = _personnel_read_fields(memory,frame,0,_personnel_indexed_address(frame,0,1),8)
        frame = _personnel_arithmetic_fields(memory,frame,2,frame.data[0]&0xFFFF)
        frame = _personnel_compare_fields(memory,frame,frame.data[2]&0xFFFF,100)
        if not frame.status_word&1:
            return memory.finish(frame)
        frame = _personnel_call_fields(memory,frame,0xFAE0,0xF914)
        frame = _personnel_compare_fields(memory,frame,frame.data[0]&0xFFFF,frame.data[2]&0xFFFF)
        if frame.status_word&1:
            return memory.finish(frame)
    frame = _personnel_store_fields(memory,frame,0xFFFFF3FE,93)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
    frame = frame.with_address(0,0xFFFFCC00)
    frame = _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,0),255,8)
    frame = frame.with_address(0,0xFFFFF45E)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF392)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = _personnel_read_fields(memory,frame,1,0xFFFFF3A6)
    frame = _personnel_compare_fields(memory,frame,frame.data[1]&0xFFFF,
        memory.state.read(_personnel_indexed_address(frame,0,0),2))
    if not frame.status_word&4:
        return memory.finish(frame)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF392)
    frame = _personnel_store_fields(memory,frame,0xFFFFF630,0xFFFF)
    frame = _personnel_call_fields(memory,frame,0x5F48,0xF952)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF392)
    frame = _personnel_call_fields(memory,frame,0xE1F6,0xF95A)
    return memory.finish(frame)

def execute_officer_recruitment_outcome_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """F778 score/bucket/sample, original unsigned threshold direction and message."""
    frame = memory.enter(frame)
    frame = _personnel_call_fields(memory,frame,0xF7DA,0xF77C)
    frame = _personnel_call_fields(memory,frame,0xF82C,0xF780)
    frame = _personnel_call_fields(memory,frame,0xFAE0,0xF784)
    frame = _personnel_compare_fields(memory,frame,frame.data[0]&0xFFFF,frame.data[3]&0xFFFF)
    if not frame.status_word&1:
        frame = _personnel_store_fields(memory,frame,0xFFFFF3FE,58)
        frame = _personnel_call_fields(memory,frame,0xF896,0xF792)
        frame = _personnel_store_fields(memory,frame,0xFFFFF608,120)
        frame = _personnel_store_fields(memory,frame,0xFFFFF362,31)
    else:
        frame = _personnel_store_fields(memory,frame,0xFFFFF3FE,60)
        frame = _personnel_call_fields(memory,frame,0xF990,0xF7AA)
        frame = _personnel_call_fields(memory,frame,0xF9D0,0xF7AE)
        frame = _personnel_store_fields(memory,frame,0x00FF7026,3)
        frame = _personnel_store_fields(memory,frame,0xFFFFF362,40)
    frame = _personnel_store_fields(memory,frame,0xFFFFF612,520)
    frame = _personnel_load_fields(memory,frame,0,9)
    frame = _personnel_store_fields(memory,frame,0xFFFFF3D0,memory.state.read(0xFFFFF3A6,2))
    frame = _personnel_call_fields(memory,frame,0x676F2,0xF7D2)
    frame = _personnel_store_fields(memory,frame,0xFFFFF608,120)
    return memory.finish(frame)
