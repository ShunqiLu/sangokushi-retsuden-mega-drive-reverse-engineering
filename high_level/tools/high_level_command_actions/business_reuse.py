"""Shared command helpers adapted to this package's one live data domain.

The source algorithms were previously reconstructed in city-cycle, city-event,
city-officer, diplomacy, army-group and battle-preparation modules. This module
adapts their real logical operations, rather than importing incompatible state
types or duplicating target instruction payloads. Partial-width calculations,
repeated live reads, overlap and original exceptions remain deliberate.

These 30 existing physical bodies are reused, not newly accepted target bytes.
Their source-review binding list lives outside the executable product module.
"""
from .domain import (
    GameState, Table, Word, Long, RandomSample, checked_state, checked_table,
    uint, u8, u16, u32, s8, s16, low8, low16, high16, replace_word,
    swap_words, negative_byte, negative_word, negative_long, divu_retained,
    descending_inclusive,
)
from .contexts_reuse import ForceHeadMatch, RosterMemory
from .contexts_message import (MessageMemory, MessagePointerFields,
    MessagePreparation, SceneState, SceneMessageInput, SceneMessageResult,
    checked_scene_state)


from .contexts_personnel import CommandFrame, FirstDeploymentFrame, FirstDeploymentReturnBoundary, PersonnelMemory, _first_right_word, _first_shift_word, _first_word, _personnel_and_fields, _personnel_arithmetic_fields, _personnel_bit_set_fields, _personnel_compare_fields, _personnel_ext_word_fields, _personnel_indexed_address, _personnel_legacy_entry, _personnel_load_fields, _personnel_memory_arithmetic_fields, _personnel_quotient_fields, _personnel_read_fields, _personnel_shift_fields, _personnel_store_fields, first_replace
from .domain import Boundary

def build_roster(state: GameState, city: Word) -> Word:
    """Prefer the nominated head, then scan all 256 live city assignments."""
    checked_state(state)
    return _build_roster_fields(RosterMemory(state), city)


def _build_roster_fields(memory: RosterMemory, city: Word) -> Word:
    """One ordered roster algorithm; callers observe only actual needed fields."""
    if type(memory) is not RosterMemory:
        raise ValueError('sealed live roster endpoint required')
    uint(city, 16)
    assignments = 0xFFFFCC00
    destination = 0xFFFFF500
    count = 0
    head = memory.read(0xFFFFF630, 2)
    if not negative_word(head):
        memory.write(destination, 2, head)
        destination = u32(destination + 2)
        count = u16(count + 1)
    for officer in range(256):
        assigned = memory.read(assignments, 1)
        assignments = u32(assignments + 1)
        if assigned == low8(city) and officer != memory.read(0xFFFFF630, 2):
            memory.write(destination, 2, officer)
            destination = u32(destination + 2)
            count = u16(count + 1)
    memory.write(destination, 2, 65535)
    return count


def build_scene_roster(state: SceneState, city: Word) -> Word:
    """Scene projection of the sole roster core on the same live state."""
    checked_scene_state(state)
    return _build_roster_fields(RosterMemory(state), city)


def _advance_random_pair(state: GameState) -> RandomSample:
    checked_state(state)
    original = state.scalar('random_seed')
    if original == 0:
        original = 0x2A6D365A
    mixed = u32(u32(u32(u32(original << 2) + original) << 3) + original)
    sample = replace_word(original, low16(mixed))
    mixed = swap_words(mixed)
    sample = replace_word(sample, u16(low16(sample) + low16(mixed)))
    mixed = swap_words(replace_word(mixed, low16(sample)))
    state.set_scalar('random_seed', mixed)
    return RandomSample(sample, mixed)


def step_random(state: GameState) -> Long:
    """Return full original sample carrier; its upper WORD is the old seed's."""
    return _advance_random_pair(state).sample


def choose_city_head(state: GameState, city: Word) -> Word:
    checked_state(state)
    uint(city, 16)
    source = state.candidate_roster.cursor()
    head = source.next_word()
    if negative_word(head):
        state.city_owner_bytes.set_byte(city, 255)
        offset = u16(u16(u16(city << 1) + city) << 2)
        state.city_orders.set_word(offset, 65535)
        state.city_orders.set_word(offset, 65535, 4)
        state.city_orders.set_word(offset, 65535, 8)
    else:
        match = roster_contains_force_head_carry(state, city, head)
        head = match.head
        if match.carry == 0:
            head = low8(head)
            highest = state.officer_status_rating.byte(head)
            while True:
                candidate = source.next_word()
                if negative_word(candidate):
                    break
                candidate = low8(candidate)
                rating = state.officer_status_rating.byte(candidate)
                if rating > highest:
                    head, highest = candidate, rating
    state.city_head_words.set_word(u16(city << 1), head)
    return head


def roster_contains_force_head_carry(state: GameState, city: Word,
                                    head: Word) -> ForceHeadMatch:
    checked_state(state)
    uint(city, 16)
    uint(head, 16)
    owner = state.city_owner_bytes.byte(city)
    force_head = state.force_heads.word(u16(owner << 1))
    source = state.candidate_roster.cursor()
    # The test and postincrement comparison are distinct original DATA reads.
    while not negative_word(source.word()):
        if source.next_word() == force_head:
            return ForceHeadMatch(force_head, state.carry_result(1))
    return ForceHeadMatch(head, state.carry_result(0))


def debit_city_gold(state: GameState, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 59146)
    actual = debit_city_gold_frame_fields(memory, entered)
    return None


def education_factor(state: GameState, teacher: Word, target: Word, entry_frame: CommandFrame | None=None) -> Word:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 59166)
    uint(teacher, 16)
    uint(target, 16)
    if teacher != entered.data[0] & 65535 or target != entered.data[1] & 65535:
        raise ValueError('teacher/target must match actual incoming D0/D1 WORDs')
    actual = education_factor_frame_fields(memory, entered)
    return actual.data[2] & 65535


def commit_mutual_relationship(state: GameState, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 60438)
    actual = commit_mutual_relationship_frame_fields(memory, entered)
    return None




def add_progress_be(state: GameState, gain: Word, entry_frame: CommandFrame | None=None) -> None:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 61280)
    uint(gain, 16)
    if gain != entered.data[2] & 65535:
        raise ValueError('compatibility score/gain must match real incoming D2')
    actual = add_progress_be_frame_fields(memory, entered)
    return None


def split_progress(state: GameState, gain: Long, entry_frame: CommandFrame | None=None) -> Word:
    """Compatibility projection of the sole complete field algorithm."""
    memory, entered = _personnel_legacy_entry(state, entry_frame, 63888)
    uint(gain, 32)
    if gain != entered.data[2]:
        raise ValueError('compatibility score/gain must match real incoming D2')
    actual = split_progress_frame_fields(memory, entered)
    return actual.data[2] & 65535


def grant_duel_fallback_progress(state: GameState, receiver_offset: Word,
        donor: Word, progress: Table) -> Long:
    """Retain the packed donor division through both low-WORD bonuses."""
    checked_state(state)
    uint(receiver_offset, 16)
    uint(donor, 16)
    checked_table(progress, state)
    donor_offset = u16(donor << 1)
    raw = progress.word(donor_offset)
    gain = divu_retained(u32(s16(raw)), 40)
    donor = donor_offset >> 1
    scene_offset = u16(state.scalar('battle_scene') << 1)
    if donor == state.city_head_words.word(scene_offset):
        gain = replace_word(gain, u16(low16(gain) + 30))
    elif donor == state.alternate_heads.word(scene_offset):
        gain = replace_word(gain, u16(low16(gain) + 30))
    if state.officer_status.byte(donor) & 16:
        gain = replace_word(gain, u16(low16(gain) + 20))
    updated = u16(progress.word(receiver_offset) + low16(gain))
    if updated > 999:
        updated = 999
    progress.set_word(receiver_offset, updated)
    return gain


def grant_duel_troop_difference_progress(state: GameState, receiver: Word,
        troop_difference: Long, progress: Table) -> Long:
    checked_state(state)
    uint(receiver, 16)
    uint(troop_difference, 32)
    checked_table(progress, state)
    gain = divu_retained(low16(troop_difference), 100)
    offset = u16(receiver << 1)
    updated = u16(progress.word(offset) + low16(gain))
    if updated > 999:
        updated = 999
    progress.set_word(offset, updated)
    return gain


def _active_duel_roster(state: GameState, officer: Word):
    if officer == state.scalar('roster_side_owner'):
        return state.battle_primary_roster.cursor()
    return state.battle_secondary_roster.cursor()


def _compact_after_match(source):
    while True:
        member = source.next_word()
        source.set_word(0, member, -4)
        if negative_word(member):
            return


def remove_zero_readiness_duelist(state: GameState, officer: Word) -> None:
    checked_state(state)
    uint(officer, 16)
    if state.scalar('battle_active') == 0:
        return
    state.officer_city_assignment.set_byte(officer, 255)
    source = _active_duel_roster(state, officer)
    while True:
        member = source.next_word()
        if negative_word(member):
            return
        if low8(member) == officer:
            break
    _compact_after_match(source)


def settle_duel_result_roster(state: GameState) -> None:
    checked_state(state)
    if state.scalar('battle_active') == 0:
        return
    result = state.scalar('duel_result')
    if result < 6:
        return
    if result == 6:
        transfer_battle_roster(state, state.scalar('duel_primary_officer'))
    else:
        transfer_battle_roster(state, state.scalar('duel_secondary_officer'))


def transfer_battle_roster(state: GameState, officer: Word) -> None:
    checked_state(state)
    uint(officer, 16)
    source = state.battle_secondary_roster.cursor()
    destination = state.battle_secondary_retired_roster.cursor()
    if officer == state.scalar('roster_side_owner'):
        source = state.battle_primary_roster.cursor()
        destination = state.battle_primary_retired_roster.cursor()
    while True:
        member = source.next_word()
        if negative_word(member):
            return
        if low8(member) == officer:
            break
    _compact_after_match(source)
    while not negative_word(destination.next_word()):
        pass
    destination.set_word(0, officer, -2)
    destination.put_word(65535)


def detach_defeated_duelist(state: GameState, officer: Word) -> None:
    """Keep the older masked-ID search with no terminator escape."""
    checked_state(state)
    uint(officer, 16)
    state.officer_city_assignment.set_byte(officer, 255)
    source = _active_duel_roster(state, officer)
    while low8(source.next_word()) != officer:
        pass
    _compact_after_match(source)


def count_selected_deployment(state: GameState) -> Word:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_deployment_command_fields(state, 0x1B262)
    return u16(frame.choice)


def initialize_selected_assignment(state: GameState, group: Table) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_deployment_command_fields(state, 0x1B27A, group)


def selected_troop_weights(state: GameState) -> tuple[Long, Long]:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    frame = project_deployment_command_fields(state, 0x1B40E)
    return frame.offset_x, frame.offset_y


def refresh_object_attribute_average(state: GameState, group: Table, divisor: Word) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    uint(divisor, 16)
    project_deployment_command_fields(state, 0x1B4EA, group)


def submit_deployment_queue(state: GameState, group: Table) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_deployment_command_fields(state, 0x1B512, group)


def clear_original_tail_coordinate(state: GameState) -> None:
    """Historical projection of one Scene rule; unknown CPU fields stay a boundary."""
    project_deployment_command_fields(state, 0x1B578)


def build_city_assigned_outcome_candidates(state: GameState) -> Word:
    checked_state(state)
    destination = state.action_candidates.cursor()
    city = state.scalar('battle_scene')
    count = 0
    for officer in descending_inclusive(255):
        if state.officer_city_assignment.byte(officer) == low8(city):
            destination.append_word(officer)
            count = u16(count + 1)
    destination.put_word(65535)
    return count


def build_battlefield_outcome_candidates(state: GameState) -> Word:
    checked_state(state)
    destination = state.action_candidates.cursor()
    city = state.scalar('battle_scene')
    count = 0
    for officer in descending_inclusive(255):
        if state.battlefield_city_assignment.byte(officer) == low8(city):
            if not negative_byte(state.officer_city_assignment.byte(officer)):
                destination.append_word(officer)
                count = u16(count + 1)
    destination.put_word(65535)
    return count


def signed_divmod(state: GameState, numerator: Long,
                  denominator: Long) -> tuple[Long, Long]:
    checked_state(state)
    uint(numerator, 32)
    uint(denominator, 32)
    if negative_long(denominator):
        quotient, remainder = positive_denominator(state, numerator, u32(-denominator))
        return u32(-quotient), remainder
    return positive_denominator(state, numerator, denominator)


def positive_denominator(state: GameState, numerator: Long,
                         denominator: Long) -> tuple[Long, Long]:
    """Do not retest negated 80000000; preserve the original shared tail."""
    checked_state(state)
    uint(numerator, 32)
    uint(denominator, 32)
    if negative_long(numerator):
        quotient, remainder = unsigned_divmod(state, u32(-numerator), denominator)
        return u32(-quotient), u32(-remainder)
    return unsigned_divmod(state, numerator, denominator)


def unsigned_divmod(state: GameState, numerator: Long,
                     denominator: Long) -> tuple[Long, Long]:
    """Accepted two-stage estimate and wrapped-product correction algorithm."""
    checked_state(state)
    uint(numerator, 32)
    uint(denominator, 32)
    if denominator <= 65535:
        return word_pair_divmod(state, numerator, denominator)
    if denominator == numerator:
        return 1, 0
    if denominator > numerator:
        return 0, numerator
    divisor_high = u32(high16(denominator) + 1)
    quotient, remainder = word_pair_divmod(state, numerator, divisor_high)
    denominator_part = divu_retained(denominator, low16(divisor_high))
    quotient = low16(divu_retained(quotient, low16(denominator_part)))
    while True:
        product = u32(low16(denominator) * low16(quotient))
        upper_product = u32(high16(denominator) * low16(quotient))
        product = u32(product + swap_words(upper_product))
        if product > numerator:
            quotient = u32(quotient - 1)
            continue
        remainder = u32(numerator - product)
        if denominator <= remainder:
            quotient = u32(quotient + 1)
            continue
        return quotient, remainder


def word_pair_divmod(state: GameState, numerator: Long,
                      denominator: Long) -> tuple[Long, Long]:
    checked_state(state)
    uint(numerator, 32)
    uint(denominator, 32)
    divisor = low16(denominator)
    upper_division = divu_retained(high16(numerator), divisor)
    upper_quotient = low16(upper_division)
    lower_dividend = u32((high16(upper_division) << 16) | low16(numerator))
    lower_division = divu_retained(lower_dividend, divisor)
    return u32((upper_quotient << 16) | low16(lower_division)), high16(lower_division)


def _resolve_message_fields(memory: MessageMemory, message: Word) -> MessagePointerFields:
    """679D2 sole bank/item algorithm, now also observing its actual full fields."""
    uint(message,16)
    bank = memory.read(0x92C4A,4)
    _message_address_fields(memory,'candidates',bank)
    _message_word_fields(memory,'target_y',message)
    bank_high = message >> 8
    _message_shift_fields(memory,'target_y',message,8,True)
    bank_offset = u16(bank_high << 1)
    _message_shift_fields(memory,'target_y',bank_high,1)
    _message_address_fields(memory,'roster',0x92C4E)
    bank_delta = memory.read(u32(0x92C4E+s16(bank_offset)),2)
    _message_word_fields(memory,'target_y',bank_delta)
    descriptor = u32(bank+s16(bank_delta))
    _message_address_fields(memory,'candidates',descriptor)
    pointer = memory.read(descriptor,4)
    _message_address_fields(memory,'roster',pointer)
    _message_word_fields(memory,'target_y',message)
    item_byte = low8(message)
    _message_word_fields(memory,'target_y',item_byte)
    item = u16(item_byte << 1)
    _message_shift_fields(memory,'target_y',item_byte,1)
    item_delta = memory.read(u32(descriptor+s16(item)+4),2)
    _message_word_fields(memory,'target_y',item_delta)
    pointer = u32(pointer+s16(item_delta))
    _message_address_fields(memory,'roster',pointer)
    return MessagePointerFields(pointer,descriptor,item_delta)


def _select_message_fields(memory: MessageMemory) -> Word:
    """67728 sole live layout selection, with retained D0 and actual shift X."""
    layout = memory.read(0xFFFFF6C4,2)
    _message_word_fields(memory,'target_x',layout)
    offset = u16(layout << 2)
    _message_shift_fields(memory,'target_x',layout,2)
    scene = memory.read(u32(0x6773C+s16(offset)),2)
    memory.write(0xFFFFF612,2,scene)
    _message_memory_flags(memory,scene)
    stage = memory.read(u32(0x6773C+s16(offset)+2),2)
    memory.write(0xFFFFF362,2,stage)
    _message_memory_flags(memory,stage)
    return offset


def _prepare_message_fields(memory: MessageMemory, message: Word) -> MessagePreparation:
    """676F2 sole transaction; no input/IRQ wait exists in this original body."""
    uint(message,16)
    _message_memory_flags(memory,message)
    if negative_word(message):
        return MessagePreparation(None,None,False,False,True,False)
    memory.read(0xFFFFF652,2)
    memory.write(0xFFFFF652,2,0)
    _message_memory_flags(memory,0)
    resolved = _message_call_fields(memory,0x679D2,0x676FE,message)
    memory.write(0xFFFFF3BE,4,resolved.pointer)
    _message_memory_flags(memory,resolved.pointer,32)
    scene = memory.read(0xFFFFF612,2)
    memory.write(0xFFFFF3C2,2,scene)
    _message_memory_flags(memory,scene)
    stage = memory.read(0xFFFFF362,2)
    memory.write(0xFFFFF3C4,2,stage)
    _message_memory_flags(memory,stage)
    memory.read(0xFFFFF36A,2)
    memory.write(0xFFFFF36A,2,0)
    _message_memory_flags(memory,0)
    memory.read(0xFFFFF3C6,2)
    memory.write(0xFFFFF3C6,2,0)
    _message_memory_flags(memory,0)
    memory.write(0xFFFFF600,2,40)
    _message_memory_flags(memory,40)
    layout_offset = _message_call_fields(memory,0x67728,0x67720)
    memory.write(0xFFFFEFDA,2,1)
    _message_memory_flags(memory,1)
    return MessagePreparation(resolved,layout_offset,False,False,False,False)


def prepare_message(state: GameState, message: Word) -> None:
    """Legacy observed writes only; unavailable high carriers are not invented."""
    checked_state(state)
    _prepare_message_fields(MessageMemory(state), message)


def select_message_layout(state: GameState) -> None:
    checked_state(state)
    _select_message_fields(MessageMemory(state))


def resolve_message_pointer(state: GameState, message: Word) -> Table:
    checked_state(state)
    resolved = _resolve_message_fields(MessageMemory(state), message)
    return state.table(resolved.pointer)


def prepare_scene_message(state: SceneState, inputs: SceneMessageInput) -> SceneMessageResult:
    """Complete observed city ABI on the caller's actual SceneState."""
    checked_scene_state(state)
    if type(inputs) is not SceneMessageInput:
        raise ValueError('explicit scene message input required')
    inputs.validate(state)
    observed = _prepare_message_fields(MessageMemory(state), low16(inputs.value))
    if observed.resolved is None:
        destination = inputs.destination
        source = inputs.source
        value = inputs.value
        field = inputs.field
    else:
        destination = state.table_at(observed.resolved.pointer)
        source = state.table_at(observed.resolved.descriptor)
        value = replace_word(inputs.value, observed.layout_offset)
        field = replace_word(inputs.field, observed.resolved.item_offset)
    result = SceneMessageResult(destination, source, value, field,
        observed.carry, observed.zero, observed.negative, observed.overflow)
    return result.validate(state)


def prepare_scene_message_fields(state: SceneState, message: Word) -> MessagePreparation:
    """Actual WORD-driven transaction, not a fabricated full CPU projection.

    The complete SceneMessageInput API and old GameState API consume this same
    field core. Absent fields describe the real negative-message early RTS;
    they are not input pointers or replacements for unknown current carriers.
    """
    checked_scene_state(state)
    uint(message, 16)
    return _prepare_message_fields(MessageMemory(state), message)

from .contexts_logistics import project_deployment_command_fields

from .contexts_personnel import FirstDeploymentFrame, FirstDeploymentReturnBoundary, first_replace
from .contexts_personnel import _first_word, _first_shift_word, _first_right_word


def _message_word_fields(memory: MessageMemory, name: str, value: Word) -> None:
    """Observe one actual message WORD carrier; partial old APIs omit the frame."""
    if memory.frame is not None:
        memory.observe(_first_word(memory.frame, name, value))


def _message_shift_fields(memory: MessageMemory, name: str, value: Word,
        amount: int, right: bool=False) -> None:
    """The message phases' two carrier roles and fixed1/2/8-bit shifts only."""
    if name not in ('target_x','target_y') or amount not in (1,2,8) or type(right) is not bool:
        raise ValueError('closed message WORD shift role required')
    if memory.frame is not None:
        frame = _first_right_word(memory.frame,name,value,amount) if right else _first_shift_word(memory.frame,name,value,amount)
        memory.observe(frame)


def _message_memory_flags(memory: MessageMemory, value, bits: int=16) -> None:
    """Memory MOVE/TST/CLR changes NZVC, never a message D carrier or X."""
    uint(value,bits)
    if bits not in (16,32):
        raise ValueError('original message WORD/LONG memory width required')
    if memory.frame is not None:
        status = (memory.frame.status & 16) | (8 if value & (1 << (bits-1)) else 0) | (4 if value == 0 else 0)
        memory.observe(first_replace(memory.frame,status=status))


def _message_address_fields(memory: MessageMemory, name: str, address: Long) -> None:
    """Actual A0 text pointer / A1 descriptor; address moves do not change flags."""
    uint(address,32)
    if name not in ('roster','candidates'):
        raise ValueError('closed message pointer role required')
    if memory.frame is not None:
        memory.observe(first_replace(memory.frame,**{name:memory.state.table_at(address).cursor()}))


def _message_call_fields(memory: MessageMemory, target: int, continuation: Long,
        message: Word=0):
    """Two genuine message child calls; partial APIs make no full-stack claim."""
    uint(continuation,32)
    if target not in (0x679D2,0x67728):
        raise ValueError('closed message child required')
    if memory.frame is not None:
        stack = memory.frame.stack_cursor.advance(-4)
        stack.set_long(0,continuation)
        memory.observe(first_replace(memory.frame,stack_cursor=stack))
    result = _resolve_message_fields(memory,message) if target == 0x679D2 else _select_message_fields(memory)
    if memory.frame is not None:
        actual = memory.frame.stack_cursor.long()
        if actual != continuation:
            raise FirstDeploymentReturnBoundary(actual,memory.frame,continuation)
        memory.observe(first_replace(memory.frame,stack_cursor=memory.frame.stack_cursor.advance(4)))
    return result


def prepare_scene_message_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Complete actual Scene676F2 entry; caller owns its outer JSR/RTS slot."""
    checked_scene_state(state)
    if type(frame) is not FirstDeploymentFrame:
        raise ValueError('complete actual message frame required')
    frame.validate(state,True)
    memory = MessageMemory(state,frame)
    _prepare_message_fields(memory,low16(frame.target_x))
    return memory.frame


def resolve_scene_message_pointer_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Complete actual679D2 entry, projecting the existing unique bank/item phase."""
    checked_scene_state(state)
    if type(frame) is not FirstDeploymentFrame:
        raise ValueError('complete actual message frame required')
    frame.validate(state,True)
    memory = MessageMemory(state,frame)
    _resolve_message_fields(memory,low16(frame.target_x))
    return memory.frame


def select_scene_message_layout_frame_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Complete actual67728 entry; physical outer token remains caller-owned."""
    checked_scene_state(state)
    if type(frame) is not FirstDeploymentFrame:
        raise ValueError('complete actual message frame required')
    frame.validate(state,True)
    memory = MessageMemory(state,frame)
    _select_message_fields(memory)
    return memory.frame

def debit_city_gold_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """E70A chosen-city ledger debit, retaining D0/D1 high halves and SUB.L CCR."""
    frame = memory.enter(frame)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF392)
    frame = _personnel_shift_fields(memory,frame,0,2)
    frame = frame.with_address(0,0xFFFFDFFC)
    frame = _personnel_read_fields(memory,frame,1,0xFFFFF39E,32)
    frame = _personnel_memory_arithmetic_fields(memory,frame,
        _personnel_indexed_address(frame,0,0),frame.data[1],32,True)
    return memory.finish(frame)

def education_factor_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """E71E target row then teacher column, with each real comparison and ADDQ."""
    frame = memory.enter(frame)
    frame = _personnel_load_fields(memory,frame,3,0)
    for threshold,row in ((20,5),(40,10),(60,15),(80,20)):
        frame = _personnel_compare_fields(memory,frame,frame.data[1]&0xFFFF,threshold)
        if frame.status_word&1:
            break
        frame = _personnel_load_fields(memory,frame,3,row)
    for threshold in (20,40,60,80):
        frame = _personnel_compare_fields(memory,frame,frame.data[0]&0xFFFF,threshold)
        if frame.status_word&1:
            break
        frame = _personnel_arithmetic_fields(memory,frame,3,1)
    frame = frame.with_address(0,0xE776)
    frame = _personnel_read_fields(memory,frame,2,_personnel_indexed_address(frame,0,3),8)
    frame = _personnel_ext_word_fields(memory,frame,2)
    return memory.finish(frame)

def commit_mutual_relationship_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """EC16 two ordered live directions; BSET acts on the full D2 LONG."""
    frame = memory.enter(frame)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3E0)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = frame.with_address(0,0xFFFFE730)
    frame = _personnel_read_fields(memory,frame,1,_personnel_indexed_address(frame,0,0))
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF376)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = frame.with_address(0,0xFFFFE710)
    frame = _personnel_read_fields(memory,frame,2,_personnel_indexed_address(frame,0,0))
    frame = _personnel_bit_set_fields(memory,frame,2,frame.data[1])
    frame = _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,0),frame.data[2]&0xFFFF)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3E0)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = frame.with_address(0,0xFFFFE730)
    frame = _personnel_read_fields(memory,frame,0,_personnel_indexed_address(frame,0,0))
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = _personnel_read_fields(memory,frame,1,0xFFFFF376)
    frame = frame.with_address(0,0xFFFFE710)
    frame = _personnel_read_fields(memory,frame,2,_personnel_indexed_address(frame,0,0))
    frame = _personnel_bit_set_fields(memory,frame,2,frame.data[1])
    frame = _personnel_store_fields(memory,frame,_personnel_indexed_address(frame,0,0),frame.data[2]&0xFFFF)
    return memory.finish(frame)

def _personnel_progress_cap_fields(memory, frame, address, gain):
    """The shared ADD.W/RMW, distinct CMPI memory read and optional MOVE cap."""
    frame = _personnel_memory_arithmetic_fields(memory,frame,address,gain)
    value = memory.state.read(address,2)
    frame = _personnel_compare_fields(memory,frame,value,999)
    if not frame.status_word&5:
        frame = _personnel_store_fields(memory,frame,address,999)
    return frame

def add_progress_be_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """EF60 D2 low-WORD gain; no copied scalar cap loop."""
    frame = memory.enter(frame)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = frame.with_address(0,0xFFFFBE00)
    frame = _personnel_progress_cap_fields(memory,frame,
        _personnel_indexed_address(frame,0,0),frame.data[2]&0xFFFF)
    return memory.finish(frame)

def split_progress_frame_fields(memory: PersonnelMemory, frame: CommandFrame) -> CommandFrame:
    """F990 full packed DIVU retained through first cap then low-WORD halving."""
    frame = memory.enter(frame)
    frame = _personnel_read_fields(memory,frame,0,0xFFFFF3A6)
    frame = _personnel_shift_fields(memory,frame,0,1)
    frame = _personnel_and_fields(memory,frame,2,0xFFFF,32)
    frame = _personnel_quotient_fields(memory,frame,2,10,0xF99C)
    frame = frame.with_address(0,0xFFFFBE00)
    frame = _personnel_progress_cap_fields(memory,frame,
        _personnel_indexed_address(frame,0,0),frame.data[2]&0xFFFF)
    frame = _personnel_shift_fields(memory,frame,2,1,16,True)
    frame = frame.with_address(0,0xFFFFC000)
    frame = _personnel_progress_cap_fields(memory,frame,
        _personnel_indexed_address(frame,0,0),frame.data[2]&0xFFFF)
    return memory.finish(frame)
