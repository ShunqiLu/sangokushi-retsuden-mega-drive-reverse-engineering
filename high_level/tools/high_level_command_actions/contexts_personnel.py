"""Named fixed-width results used by the personnel command rules.

The score retains its division remainder in the upper WORD because later
partial-WORD operations do not erase it.  This is a value compatibility
contract, not a processor register or a claim about natural input domains.
"""
from dataclasses import dataclass
from .domain import Long, Word, uint


@dataclass(frozen=True)
class RecruitmentScore:
    score: Long
    probability_threshold: Word
    resource_bucket: Word

    def __post_init__(self):
        uint(self.score, 32)
        uint(self.probability_threshold, 16)
        uint(self.resource_bucket, 16)

"""Complete personnel-command carriers over the independent command RAM domain.

confirmed: the entry contains all sixteen LONG registers, full SR/X and actual
physical SP. The Scene port only aliases the same live RAM, readonly allocations,
read budget and ordered events; neither checked_state nor its union is widened.
"""
from dataclasses import replace
from .domain import GameState, checked_state, uint, u8, u16, u32, s8, s16, Boundary
from ..high_level_player_commands.contexts_command_fields import (
    CommandFrame, _command_test_fields, _command_load_fields,
    _command_binary_fields, _command_store_fields, _command_shift_fields,
    _command_product_fields, _command_quotient_fields, _command_bit_fields,
    _command_dbra_fields,
)
from ..high_level_battle_ai.contexts_first_deployment import (
    FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace,
)
from ..high_level_battle_ai.business_formation import (
    _first_word, _first_shift_word, _first_right_word,
)


class PersonnelMemory:
    """A sealed same-state port, not a fabricated CPU or readonly provider."""
    def __init__(self, state):
        from ..high_level_scene_flows.domain import SceneState, ReadOnlyData
        checked_state(state)
        self.source = state
        self.state = SceneState(state.ram, data=ReadOnlyData(state.data.segments),
            max_reads=state.max_reads, sr=state.sr)
        self.state.events = state.events
        self.state.reads = state.reads

    def cursor_at(self, address):
        return self.state.table_at(u32(address)).cursor()

    def enter(self, frame):
        if type(self) is not PersonnelMemory or type(frame) is not CommandFrame:
            raise ValueError('actual complete personnel memory and entry carriers required')
        self.state.sr = frame.status_word
        return frame

    def first_fields(self, frame):
        from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
        return FirstDeploymentFrame(*frame.data,
            *(self.cursor_at(address) for address in frame.addresses),
            frame.status_word & 31)

    def from_first(self, frame):
        from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
        from ..high_level_scene_flows.domain import Cursor, checked_table
        if type(frame) is not FirstDeploymentFrame:
            raise ValueError('actual named child frame required')
        names = ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')
        views = (frame.roster,frame.candidates,frame.controller,frame.scan,
            frame.opponent,frame.scratch,frame.auxiliary,frame.stack_cursor)
        for view in views:
            checked_table(view,self.state)
        if type(frame.stack_cursor) is not Cursor:
            raise ValueError('actual A7 postincrement cursor required')
        uint(frame.status,8)
        if frame.status > 31:
            raise ValueError('actual low-five-bit CCR required')
        self.state.sr = (self.state.sr & 0xFFE0) | frame.status
        self.source.reads,self.source.sr = self.state.reads,self.state.sr
        return CommandFrame(tuple(frame.carrier(name) for name in names),
            tuple(view.base for view in views),self.state.sr)

    def finish(self, frame):
        self.state.sr = frame.status_word
        self.source.reads,self.source.sr = self.state.reads,frame.status_word
        return frame

    def stop(self, frame, target, reason):
        from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
        self.finish(frame)
        raise MovementContinuationBoundary(target,self.first_fields(frame),reason)


def _personnel_load_fields(memory, frame, index, value, width=16):
    return _command_load_fields(memory,frame,index,value,width)


def _personnel_read_fields(memory, frame, index, address, width=16):
    value = memory.state.read(u32(address),width//8)
    return _command_load_fields(memory,frame,index,value,width)


def _personnel_test_fields(memory, frame, value, width=16):
    return _command_test_fields(memory,frame,value,width)


def _personnel_store_fields(memory, frame, address, value, width=16, clear=False):
    return _command_store_fields(memory,frame,u32(address),value,width,clear)


def _personnel_indexed_address(frame, address_register, data_register, displacement=0):
    """Bare indexed EA extends the supplied low WORD, never a typed-view double sign."""
    return u32(frame.addresses[address_register]+s16(frame.data[data_register]&0xFFFF)+displacement)


def _personnel_arithmetic_fields(memory, frame, index, operand, width=16, subtract=False):
    mask = (1<<width)-1
    frame,value = _command_binary_fields(memory,frame,frame.data[index]&mask,operand,width,subtract)
    return frame.with_data(index,value,width)


def _personnel_memory_arithmetic_fields(memory, frame, address, operand, width=16, subtract=False):
    actual = memory.state.read(u32(address),width//8)
    frame,value = _command_binary_fields(memory,frame,actual,operand,width,subtract)
    # A read-modify-write arithmetic instruction does not add MOVE flags.
    memory.state.write(u32(address),width//8,value)
    return frame


def _personnel_compare_fields(memory, frame, left, right, width=16):
    frame,ignored = _command_binary_fields(memory,frame,left,right,width,True,True)
    return frame


def _personnel_shift_fields(memory, frame, index, amount, width=16, right=False):
    if width == 16:
        return _command_shift_fields(memory,frame,index,amount,width,right)
    if width != 32 or right or amount not in (1,2,3):
        raise ValueError('one original personnel LONG left-shift role required')
    from ..high_level_scene_flows.business_scene import _glyph_shift_long_fields
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    names = ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')
    return memory.from_first(_glyph_shift_long_fields(SceneRefreshMemory(memory.state),
        memory.first_fields(frame),names[index],amount))


def _personnel_swap_fields(memory, frame, index):
    original = frame.data[index]
    value = u32((original<<16)|(original>>16))
    return _command_load_fields(memory,frame,index,value,32)


def _personnel_ext_word_fields(memory, frame, index):
    return _command_load_fields(memory,frame,index,u16(s8(frame.data[index]&255)),16)


def _personnel_and_fields(memory, frame, index, mask, width=16):
    return _command_load_fields(memory,frame,index,(frame.data[index]&mask)&((1<<width)-1),width)


def _personnel_product_fields(memory, frame, index, source, signed=False):
    if not signed:
        return _command_product_fields(memory,frame,index,source)
    value = u32(s16(frame.data[index]&0xFFFF)*s16(source))
    return _command_load_fields(memory,frame,index,value,32)


def _personnel_quotient_fields(memory, frame, index, divisor, instruction):
    return _command_quotient_fields(memory,frame,index,divisor,instruction)


def _personnel_bit_set_fields(memory, frame, index, bit):
    value = frame.data[index]
    frame = _command_bit_fields(memory,frame,value,bit&31)
    return frame.with_data(index,value|(1<<(bit&31)))


def _personnel_db_fields(frame, index):
    return _command_dbra_fields(frame,index)


def _personnel_child_fields(memory, frame, target):
    """Only genuinely complete named children; no partial scalar return is promoted."""
    from .business_personnel import (
        reduce_selected_officer_disposition_randomly_frame_fields,
        reduce_chosen_force_head_disposition_randomly_frame_fields,
        credit_selected_officer_policy_progress_frame_fields,
        score_selected_officer_recruitment_frame_fields,
        bucket_recruitment_score_frame_fields,
        apply_recruited_officer_roster_transition_frame_fields,
        apply_recruitment_city_resource_losses_frame_fields,
        reduce_recruitment_city_food_frame_fields,
        reduce_recruitment_city_gold_frame_fields,
        reduce_recruitment_city_state_parameter_frame_fields,
        draw_recruitment_probability_frame_fields,
    )
    from .business_reuse import (
        debit_city_gold_frame_fields, education_factor_frame_fields,
        commit_mutual_relationship_frame_fields, add_progress_be_frame_fields,
        split_progress_frame_fields, prepare_scene_message_frame_fields,
    )
    if target == 0xE70A:
        return debit_city_gold_frame_fields(memory,frame)
    if target == 0xE71E:
        return education_factor_frame_fields(memory,frame)
    if target == 0xEC16:
        return commit_mutual_relationship_frame_fields(memory,frame)
    if target == 0xEF60:
        return add_progress_be_frame_fields(memory,frame)
    if target == 0xEF80:
        return reduce_selected_officer_disposition_randomly_frame_fields(memory,frame)
    if target == 0xEFA4:
        return reduce_chosen_force_head_disposition_randomly_frame_fields(memory,frame)
    if target == 0xEFE2:
        return credit_selected_officer_policy_progress_frame_fields(memory,frame)
    if target == 0xF7DA:
        return score_selected_officer_recruitment_frame_fields(memory,frame)
    if target == 0xF82C:
        return bucket_recruitment_score_frame_fields(memory,frame)
    if target == 0xF896:
        return apply_recruited_officer_roster_transition_frame_fields(memory,frame)
    if target == 0xF990:
        return split_progress_frame_fields(memory,frame)
    if target == 0xF9D0:
        return apply_recruitment_city_resource_losses_frame_fields(memory,frame)
    if target == 0xF9EA:
        return reduce_recruitment_city_food_frame_fields(memory,frame)
    if target == 0xFA3A:
        return reduce_recruitment_city_gold_frame_fields(memory,frame)
    if target == 0xFA8A:
        return reduce_recruitment_city_state_parameter_frame_fields(memory,frame)
    if target == 0xFAE0:
        return draw_recruitment_probability_frame_fields(memory,frame)
    if target in (0x83D4,0x5F48,0xE1F6):
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        from ..high_level_gameplay_flow.business_battle import (
            _presentation_random_fields,build_roster_fields,choose_city_head_fields,
        )
        actual = memory.first_fields(frame)
        port = BattlePresentationMemory(memory.state)
        if target == 0x83D4:
            actual = _presentation_random_fields(port,actual)
        elif target == 0x5F48:
            actual = build_roster_fields(port,actual)
        else:
            actual = choose_city_head_fields(port,actual)
        return memory.from_first(actual)
    if target == 0x676F2:
        return memory.from_first(prepare_scene_message_frame_fields(memory.state,memory.first_fields(frame)))
    memory.stop(frame,target,'personnel child lacks a real complete-field continuation')


def _personnel_call_fields(memory, frame, target, continuation):
    """One original BSR/JSR slot; nested children own only their own real slots."""
    uint(target,32);uint(continuation,32)
    frame = frame.with_address(7,frame.addresses[7]-4)
    memory.state.write(frame.addresses[7],4,continuation)
    actual = _personnel_child_fields(memory,frame,target)
    returned = memory.state.read(actual.addresses[7],4)
    if returned != continuation:
        memory.stop(actual,returned,'actual personnel return LONG was modified')
    return actual.with_address(7,actual.addresses[7]+4)


def _personnel_legacy_entry(state, entry_frame, target):
    checked_state(state)
    uint(target,32)
    if entry_frame is None:
        raise Boundary('historical personnel scalar API lacks complete D/A/SR-X/SP; supply entry_frame')
    memory = PersonnelMemory(state)
    return memory,memory.enter(entry_frame)


def _personnel_existing_fields(memory, frame, target):
    """Outcome/deployment compatibility only; retained sole children own the algorithm."""
    from ..high_level_remaining_flows.business_city import execute_deployment_menu_fields
    from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
    from ..high_level_gameplay_flow.business_battle import (
        compute_outcome_force_ratio_fields,
        apply_battlefield_ratio_losses_fields,apply_city_assigned_heavy_losses_fields,
        consume_city_battle_resources_fields,apply_battlefield_heavy_losses_and_detach_fields,
    )
    from ..high_level_gameplay_flow.business_reuse import (
        settle_duel_training_and_troops_fields,settle_duel_packets_fields,
        apply_duel_disposition_fields,detach_zero_readiness_duelists_fields,
    )
    frame = memory.enter(frame)
    actual = memory.first_fields(frame)
    port = BattlePresentationMemory(memory.state)
    if target == 0x188A6:
        actual = settle_duel_training_and_troops_fields(port,actual)
    elif target == 0x18B00:
        actual = settle_duel_packets_fields(port,actual)
    elif target == 0x18B94:
        actual = apply_duel_disposition_fields(port,actual)
    elif target == 0x18C56:
        actual = detach_zero_readiness_duelists_fields(port,actual)
    elif target == 0x1C1C2:
        actual = compute_outcome_force_ratio_fields(port,actual)
    elif target == 0x1C2FC:
        actual = apply_battlefield_ratio_losses_fields(port,actual)
    elif target == 0x1C39C:
        actual = apply_city_assigned_heavy_losses_fields(port,actual)
    elif target == 0x1C466:
        actual = consume_city_battle_resources_fields(port,actual)
    elif target == 0x1C5EE:
        actual = apply_battlefield_heavy_losses_and_detach_fields(port,actual)
    elif target in (0x1B246,0x1B2BC,0x1B448,0x1B472):
        actual = execute_deployment_menu_fields(memory.state,target,actual)
    else:
        memory.stop(frame,target,'closed outcome or deployment owner required')
    return memory.finish(memory.from_first(actual))


def execute_personnel_command_fields(state: GameState, frame: CommandFrame, target: int) -> CommandFrame:
    """Closed named owner entry; the real caller already owns its outer LONG."""
    uint(target,32)
    memory = PersonnelMemory(state)
    frame = memory.enter(frame)
    from .business_personnel import (
        execute_officer_loyalty_reward_frame_fields,
        execute_mutual_officer_relationship_reward_frame_fields,
        execute_officer_policy_outcome_frame_fields,
        execute_officer_recruitment_outcome_frame_fields,
    )
    if target == 0xE592:
        return execute_officer_loyalty_reward_frame_fields(memory,frame)
    if target == 0xEA38:
        return execute_mutual_officer_relationship_reward_frame_fields(memory,frame)
    if target == 0xEE16:
        return execute_officer_policy_outcome_frame_fields(memory,frame)
    if target == 0xF778:
        return execute_officer_recruitment_outcome_frame_fields(memory,frame)
    if target in (0x188A6,0x18B00,0x18B94,0x18C56,0x1C1C2,0x1C2FC,
            0x1C39C,0x1C466,0x1C5EE,0x1B246,0x1B2BC,0x1B448,0x1B472):
        return _personnel_existing_fields(memory,frame,target)
    return memory.finish(_personnel_child_fields(memory,frame,target))


def execute_personnel_scene_fields(state, target: int, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Scene-specific same-state adapter, not a new accepted GameState union.

    Only explicit typed readonly segments/RAM/events/read-budget are aliased.
    All live sixteen LONGs and full SR are captured, and the callee never pushes
    a duplicate outer CALL token. Unknown child/hardware exceptions stay real.
    """
    from ..high_level_scene_flows.domain import SceneState
    from .domain import ReadOnlyData
    if type(state) is not SceneState or type(frame) is not FirstDeploymentFrame:
        raise ValueError('actual complete Scene-specific personnel entry required')
    frame.validate(state,True)
    source = GameState(state.ram,data=ReadOnlyData(state.data.segments),
        max_reads=state.max_reads,sr=(state.sr&0xFFE0)|frame.status)
    source.events = state.events
    source.reads = state.reads
    names = ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')
    views = (frame.roster,frame.candidates,frame.controller,frame.scan,
        frame.opponent,frame.scratch,frame.auxiliary,frame.stack_cursor)
    entered = CommandFrame(tuple(frame.carrier(name) for name in names),
        tuple(view.base for view in views),source.sr)
    try:
        actual = execute_personnel_command_fields(source,entered,target)
    finally:
        state.reads,state.sr = source.reads,source.sr
    return FirstDeploymentFrame(*actual.data,
        *(state.table_at(address).cursor() for address in actual.addresses),
        actual.status_word&31)
