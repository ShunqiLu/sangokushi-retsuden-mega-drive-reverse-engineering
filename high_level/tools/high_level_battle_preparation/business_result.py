"""Battle timers, result routing and pair separation over live game state.

These six rules are separate from UI, rendering and battle preparation. Table
offsets retain the original WORD widths and live rereads; no catalog clamp or
snapshot is inserted. The target compiler preserves the original fixed ABI.
Privileged carry is an explicit domain effect, not a full CPU/SR emulator.
"""
from .domain import PreparationState, u8, u16
from .contexts_counter import CounterMemory, CounterFields, SceneCounterInput, SceneCounterResult


def decrement_battle_3cc2_counters(state: PreparationState):
    """Tick every counter, including a write-back for unchanged zero bytes."""
    _tick_single_counter_fields(CounterMemory(state))


def _tick_single_counter_fields(memory):
    if type(memory) is not CounterMemory:
        raise ValueError('sealed counter memory required')
    counters = memory.table(0x00FF3CC2)
    for offset in range(256):
        value = counters.byte(0)
        if value != 0:
            value = u8(value - 1)
        counters.set_byte(0, value)
        counters = counters.advance(1)
    return CounterFields(counters.base, None, value, 65535)


def decrement_battle_status_counters(state: PreparationState):
    """Tick three live arrays; the first uses the original 0x81 -> 0 rule."""
    _tick_status_counter_fields(CounterMemory(state))


def _tick_status_counter_fields(memory):
    if type(memory) is not CounterMemory:
        raise ValueError('sealed counter memory required')
    primary = memory.table(0xFFFFA654)
    secondary = memory.table(0x00FF3DC2)
    for offset in range(256):
        value = primary.byte(0)
        if value != 0:
            value = u8(value - 1)
            if value & 128:
                if value == 128:
                    value = 0
        primary.set_byte(0, value)
        primary = primary.advance(1)
        value = secondary.byte(0)
        if value != 0:
            value = u8(value - 1)
        secondary.set_byte(0, value)
        secondary = secondary.advance(1)
    tertiary = memory.table(0xFFFFA754)
    for offset in range(256):
        value = tertiary.byte(0)
        if value != 0:
            value = u8(value - 1)
        tertiary.set_byte(0, value)
        tertiary = tertiary.advance(1)
    return CounterFields(tertiary.base, secondary.base, value, 65535)


def tick_scene_single_counters(state, inputs):
    from ..high_level_scene_flows.domain import Boundary, replace_byte, replace_word
    if type(inputs) is not SceneCounterInput:
        raise ValueError('actual Scene counter input required')
    inputs.validate(state)
    if inputs.source is None:
        raise Boundary('1F13C retains actual incoming A1; missing live source')
    fields = _tick_single_counter_fields(CounterMemory(state))
    return SceneCounterResult(state.table_at(fields.destination), inputs.source,
        replace_byte(inputs.value, fields.last_byte), replace_word(inputs.field, fields.loop_word),
        False, fields.last_byte == 0, bool(fields.last_byte & 128), False)


def tick_scene_status_counters(state, inputs):
    from ..high_level_scene_flows.domain import replace_byte, replace_word
    if type(inputs) is not SceneCounterInput:
        raise ValueError('actual Scene counter input required')
    inputs.validate(state)
    fields = _tick_status_counter_fields(CounterMemory(state))
    return SceneCounterResult(state.table_at(fields.destination), state.table_at(fields.source),
        replace_byte(inputs.value, fields.last_byte), replace_word(inputs.field, fields.loop_word),
        False, fields.last_byte == 0, bool(fields.last_byte & 128), False)


def select_battle_outcome_side(state: PreparationState):
    """Route a result; outcomes 6/7 intentionally leave F6D6 untouched."""
    outcome = state.table(0xFFFF8114).word(0)
    if outcome == 2 or outcome == 5:
        officer = state.table(0xFFFF80E0).word(0)
    elif outcome == 6 or outcome == 7:
        state.table(0xFFFFF362).set_word(0, 5)
        return
    else:
        officer = state.table(0xFFFF80E2).word(0)
    state.table(0xFFFFF6D6).set_word(0, 0)
    if officer == state.table(0xFFFFF702).word(0):
        state.table(0xFFFFF6D6).set_word(0, 2)


def adjust_battle_pair_spacing(state: PreparationState, officer: int):
    """Separate on one axis only, preserving unsigned deficits and X ties."""
    officer = u16(officer)
    if officer == state.table(0xFFFFF702).word(0):
        other = state.table(0xFFFFF706).word(0)
    else:
        other = state.table(0xFFFFF702).word(0)
    coordinates = state.table(0xFFFFA150)
    own_offset = u16(officer * 4)
    other_offset = u16(other * 4)
    own_x = coordinates.word(own_offset)
    other_x = coordinates.word(other_offset)
    x_negative = own_x < other_x
    x_gap = u16(own_x - other_x)
    if x_negative:
        x_gap = u16(-x_gap)
    if x_gap >= 2304:
        return
    x_deficit = u16(x_gap - 2304)
    own_y = coordinates.word(own_offset, 2)
    other_y = coordinates.word(other_offset, 2)
    y_negative = own_y < other_y
    y_gap = u16(own_y - other_y)
    if y_negative:
        y_gap = u16(-y_gap)
    if y_gap >= 2304:
        return
    y_deficit = u16(y_gap - 2304)
    if y_deficit > x_deficit:
        if not y_negative:
            y_deficit = u16(-y_deficit)
        previous = coordinates.word(own_offset, 2)
        coordinates.set_word(own_offset, u16(previous + y_deficit), 2)
    else:
        if not x_negative:
            x_deficit = u16(-x_deficit)
        previous = coordinates.word(own_offset)
        coordinates.set_word(own_offset, u16(previous + x_deficit))


def battle_pair_removed_carry(state: PreparationState):
    """Return the privileged carry effect after a live, short-circuit query."""
    membership = state.table(0xFFFFCC00)
    first = state.table(0xFFFFF702).word(0)
    if membership.byte(first) == 255:
        return state.set_carry(True)
    second = state.table(0xFFFFF706).word(0)
    if membership.byte(second) == 255:
        return state.set_carry(True)
    return state.set_carry(False)


def selected_battle_roster_carry(state: PreparationState, record):
    """Search complete requested WORDs; a negative WORD is the terminator."""
    requested = record.word(0)
    if state.table(0xFFFFF6D7).byte(0) & 2:
        roster = state.table(0xFFFFA5A4).cursor()
    else:
        roster = state.table(0xFFFFA550).cursor()
    while True:
        member = roster.next_word()
        if member & 32768:
            return state.set_carry(True)
        if member == requested:
            return state.set_carry(False)
