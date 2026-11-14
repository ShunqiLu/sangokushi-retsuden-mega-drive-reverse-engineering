"""Recruitment capacity, equipment menus and selected-officer preparation.

These functions separate the numeric rules, live candidate lists, input state
and RAM display packets. They do not implement a hardware renderer or pretend
the menu preparation is an already executed domestic command. All resource
shapes and step tables come from named data views supplied to GameState.
Original fixed-width arithmetic, queue aliases and asymmetric input flow are
preserved; compatibility defects are not silently repaired.
"""
from .domain import (GameState, Word, Long, Cursor, Boundary, checked_state,
                     uint, u16, u32, low16, high16, replace_word, swap_words,
                     negative_word, descending_inclusive, divu_retained)
from .contexts_recruitment import (TilePairContext, TilePairResult,
    SeparatorRowContext, SeparatorRowResult, checked_context)
from .business_budget import append_six_place_decimal_value
from .business_display import append_live_command_string_words


from .contexts_equipment import EquipmentMenuMemory, EquipmentMenuFields

from .business_budget import _six_place_decimal_fields

from .contexts_command_fields import CommandMenuMemory, CommandFrame, _command_load_fields, _command_test_fields, _command_binary_fields, _command_store_fields, _command_shift_fields, _command_product_fields, _command_quotient_fields, _command_bit_fields, _command_dbra_fields, _command_call_fields, _command_tail_fields, _command_numbered_pair_fields, _command_decimal_transaction_fields, _command_decimal_place_fields
from .domain import u16, u32, s16
from .business_budget import _command_legacy_entry

def _queue_cursor(state: GameState) -> Cursor:
    return state.display_queue.cursor(state.scalar('queue_offset'))


def _finish_queue(state: GameState, destination: Cursor, length: Word) -> None:
    """Legacy no-return projection of the sole actual queue transaction."""
    checked_state(state)
    _finish_queue_fields(EquipmentMenuMemory(state), destination, length)


def _finish_queue_fields(memory: EquipmentMenuMemory, destination: Cursor, length: Word) -> tuple:
    """Original memory CLR read/write and live queue ADD, including wrapping."""
    if type(memory) is not EquipmentMenuMemory:
        raise ValueError('sealed equipment-menu memory required')
    memory.check_cursor(destination)
    uint(length, 16)
    destination.word()
    destination.put_word(0)
    previous = memory.scalar('queue_offset')
    current = u16(previous + length)
    memory.set_scalar('queue_offset', current)
    return (previous + length > 65535, current == 0, bool(current & 32768),
        bool((~(previous ^ length) & (previous ^ current)) & 32768))


def _paired_tiles(state: GameState, context: TilePairContext, row_stride: Word) -> TilePairResult:
    """Strict actual retained high WORDs over the single paired-tile core."""
    context = checked_context(context, TilePairContext, state)
    fields = _paired_tiles_fields(EquipmentMenuMemory(state), context.destination,
        low16(context.tile), low16(context.counter), row_stride)
    return TilePairResult(fields.destination, replace_word(context.tile, fields.value),
        replace_word(context.counter, fields.field_if_written))


def _paired_tiles_fields(memory: EquipmentMenuMemory, destination: Cursor, tile: Word, counter: Word, row_stride: Word) -> EquipmentMenuFields:
    """Sole original two-row tile algorithm over one real live destination."""
    if type(memory) is not EquipmentMenuMemory:
        raise ValueError('sealed equipment-menu memory required')
    memory.check_cursor(destination)
    uint(tile, 16)
    uint(counter, 16)
    uint(row_stride, 16)
    for _ in descending_inclusive(counter):
        destination.put_word(tile)
        old_tile = tile
        tile = u16(tile + 1)
        destination.set_word(0, tile, row_stride)
        old_tile = tile
        tile = u16(tile + 1)
        destination.base = u32(destination.base + 2)
        counter = u16(counter - 1)
    return EquipmentMenuFields(destination, None, tile, counter, None, None, None,
        old_tile + 1 > 65535, tile == 0, bool(tile & 32768),
        bool((~(old_tile ^ 1) & (old_tile ^ tile)) & 32768)).validate(memory)


def append_recruitment_paired_tiles(state: GameState,
        context: TilePairContext) -> TilePairResult:
    """Two live rows, 34 bytes apart, with sequential WORD tile identifiers."""
    state = checked_state(state)
    return _paired_tiles(state, context, 34)


def append_equipment_paired_tiles(state: GameState,
        context: TilePairContext) -> TilePairResult:
    state = checked_state(state)
    return _paired_tiles(state, context, 34)


def append_candidate_paired_tiles(state: GameState,
        context: TilePairContext) -> TilePairResult:
    state = checked_state(state)
    return _paired_tiles(state, context, 20)


def append_candidate_separator_row(state: GameState, context: SeparatorRowContext, *, entry_frame: CommandFrame | None=None) -> SeparatorRowResult:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 80534)
    context = checked_context(context, SeparatorRowContext, state)
    if context.destination.base != entered.addresses[0] or context.coordinate != entered.data[0]:
        raise ValueError('separator context must match real A0/D0 entry')
    actual = append_candidate_separator_row_frame_fields(memory, entered)
    return SeparatorRowResult(memory.cursor_at(actual.addresses[0]), actual.data[0])


def _append_large_dialog(state: GameState, first_labels: tuple, second_labels: tuple) -> None:
    """Legacy no-return projection over one real shared field core."""
    checked_state(state)
    _append_large_dialog_fields(EquipmentMenuMemory(state), first_labels, second_labels)

def _append_large_dialog_fields(memory: EquipmentMenuMemory, first_labels: tuple, second_labels: tuple, first_continuations: tuple | None=None, second_continuations: tuple | None=None, *, entry_frame: CommandFrame | None=None) -> EquipmentMenuFields:
    """Honest partial projection of the unique complete owner."""
    if (first_labels, second_labels) == (((49181, 3), (49157, 1)), ((49161, 3),)):
        target = 77930
    elif (first_labels, second_labels) == (((49169, 3), (49185, 1)), ((49177, 1), (49189, 1), (49185, 1))):
        target = 79300
    else:
        raise ValueError('only original closed dialog label plans required')
    return _equipment_complete_projection(memory, entry_frame, target)


def append_recruitment_dialog_frame(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 77930)
    actual = append_recruitment_dialog_frame_frame_fields(memory, entered)
    return None


def append_equipment_dialog_frame(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 79300)
    actual = append_equipment_dialog_frame_frame_fields(memory, entered)
    return None


def prepare_player_recruitment_capacity(state: GameState, *, entry_frame: CommandFrame | None=None) -> Word:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 78216)
    actual = prepare_player_recruitment_capacity_frame_fields(memory, entered)
    return actual.data[1] & 65535


def _update_blink_cursor(state: GameState, x: Word) -> None:
    count = state.scalar('cursor_blink_counter')
    if count >= 24:
        state.set_scalar('cursor_blink_counter', 24)
    state.set_scalar('cursor_blink_counter',
                     u16(state.scalar('cursor_blink_counter') - 1))
    if state.scalar('cursor_blink_counter') >= 12:
        y = u16(u16(state.scalar('amount_digit_position') << 3) + 248)
        append_live_command_string_words(state, state.amount_cursor_shape, x, y)


def update_recruitment_input_cursor(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 77656)
    actual = update_recruitment_input_cursor_frame_fields(memory, entered)
    return None


def update_recruitment_total_cursor(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 77876)
    actual = update_recruitment_total_cursor_frame_fields(memory, entered)
    return None


def _append_input_digits(state: GameState, scalar_name: str) -> None:
    """Legacy no-return projection over one real shared field core."""
    checked_state(state)
    _append_input_digits_fields(EquipmentMenuMemory(state), scalar_name)

def _append_input_digits_fields(memory: EquipmentMenuMemory, scalar_name: str, numeric_continuation: Long | None=None, *, entry_frame: CommandFrame | None=None) -> EquipmentMenuFields:
    """Honest partial projection of the unique complete owner."""
    if scalar_name == 'recruitment_input':
        target = 78364
    elif scalar_name == 'equipment_input':
        target = 79604
    else:
        raise ValueError('only original input rows required')
    return _equipment_complete_projection(memory, entry_frame, target)


def append_recruitment_input_digits(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 78364)
    actual = append_recruitment_input_digits_frame_fields(memory, entered)
    return None


def append_equipment_input_digits(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 79604)
    actual = append_equipment_input_digits_frame_fields(memory, entered)
    return None


def _append_total_digits(state: GameState, value: Long) -> None:
    """Legacy no-return projection over one real shared field core."""
    checked_state(state)
    _append_total_digits_fields(EquipmentMenuMemory(state), value)

def _append_total_digits_fields(memory: EquipmentMenuMemory, value: Long, numeric_continuation: Long | None=None, *, entry_frame: CommandFrame | None=None) -> EquipmentMenuFields:
    """Honest partial projection of the unique complete owner."""
    if numeric_continuation == 78470:
        target = 78448
    elif numeric_continuation == 79730:
        target = 79690
    else:
        raise Boundary('partial total row lacks its actual original role')
    return _equipment_complete_projection(memory, entry_frame, target)


def append_recruitment_total_digits(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 78448)
    actual = append_recruitment_total_digits_frame_fields(memory, entered)
    return None


def append_equipment_total_digits(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 79690)
    actual = append_equipment_total_digits_frame_fields(memory, entered)
    return None


def _append_amount_cursor(state: GameState, y_base: Word) -> None:
    y = u16(u16(state.scalar('amount_digit_position') << 3) + y_base)
    append_live_command_string_words(state, state.amount_cursor_shape, 88, y)


def append_equipment_amount_cursor(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 79120)
    actual = append_equipment_amount_cursor_frame_fields(memory, entered)
    return None


def append_candidate_amount_cursor(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 80180)
    actual = append_candidate_amount_cursor_frame_fields(memory, entered)
    return None


def clear_equipment_dialog_rows(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 79166)
    actual = clear_equipment_dialog_rows_frame_fields(memory, entered)
    return None


def _append_candidate_row_pair(state: GameState, destination: Cursor,
        coordinate: Word, labels: tuple) -> tuple[Cursor, Word]:
    destination.set_word(0, 8, 20)
    destination.append_word(8)
    destination.set_word(0, coordinate, 20)
    destination.append_word(u16(coordinate - 128))
    coordinate = u16(coordinate + 128)
    destination.set_word(0, 0xC382, 20)
    destination.append_word(0xC382)
    for tile, counter in labels:
        destination = _paired_tiles(state,
            TilePairContext(destination, tile, counter), 20).destination
    destination.set_word(0, 0xCB82, 20)
    destination.append_word(0xCB82)
    destination.base = u32(destination.base + 20)
    return destination, coordinate


def append_candidate_dialog_frame(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 80216)
    actual = append_candidate_dialog_frame_frame_fields(memory, entered)
    return None


def clear_candidate_dialog_rows(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 81022)
    actual = clear_candidate_dialog_rows_frame_fields(memory, entered)
    return None


def update_equipment_category(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 80774)
    actual = update_equipment_category_frame_fields(memory, entered)
    return None


def append_equipment_category_cursor(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 80858)
    actual = append_equipment_category_cursor_frame_fields(memory, entered)
    return None


def prepare_selected_training_cost_steps(state: GameState, *, entry_frame: CommandFrame | None=None) -> Long:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 81398)
    actual = prepare_selected_training_cost_steps_frame_fields(memory, entered)
    return actual.data[0]


def update_selected_training_amount(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 81554)
    actual = update_selected_training_amount_frame_fields(memory, entered)
    return None


def append_training_cost_digits(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 81772)
    actual = append_training_cost_digits_frame_fields(memory, entered)
    return None


def append_training_amount_cursor(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 81834)
    actual = append_training_amount_cursor_frame_fields(memory, entered)
    return None


def prepare_selected_training_origin_and_speed(state: GameState, *, entry_frame: CommandFrame | None=None) -> Word:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 81892)
    actual = prepare_selected_training_origin_and_speed_frame_fields(memory, entered)
    return actual.data[0] & 65535

def append_equipment_dialog_frame_fields(memory: EquipmentMenuMemory, *, entry_frame: CommandFrame | None=None) -> EquipmentMenuFields:
    """Honest partial projection of the unique complete owner."""
    return _equipment_complete_projection(memory, entry_frame, 79300)


def append_equipment_input_digits_fields(memory: EquipmentMenuMemory, *, entry_frame: CommandFrame | None=None) -> EquipmentMenuFields:
    """Honest partial projection of the unique complete owner."""
    return _equipment_complete_projection(memory, entry_frame, 79604)


def append_equipment_total_digits_fields(memory: EquipmentMenuMemory, *, entry_frame: CommandFrame | None=None) -> EquipmentMenuFields:
    """Honest partial projection of the unique complete owner."""
    return _equipment_complete_projection(memory, entry_frame, 79690)

def _equipment_complete_projection(memory, entry_frame, target):
    """Old subset views project the unique full algorithm, never a second loop."""
    if type(memory) is not EquipmentMenuMemory:
        raise ValueError('actual equipment memory required')
    if entry_frame is None:
        raise Boundary('historical partial equipment fields did not observe full D/A/SR-X/SP')
    complete = CommandMenuMemory(memory.state)
    actual = _recruitment_known_fields(complete,complete.enter(entry_frame),target)
    if actual is None:
        complete.stop(entry_frame,target,'unknown legacy equipment role')
    memory.numeric.stack_cursor = complete.cursor_at(actual.addresses[7])
    status = actual.status_word
    return EquipmentMenuFields(complete.cursor_at(actual.addresses[0]),
        complete.cursor_at(actual.addresses[1]),actual.data[0] & 0xFFFF,
        actual.data[1] & 0xFFFF,actual.data[2] & 0xFFFF,
        actual.data[3] & 0xFFFF,actual.data[0],bool(status & 1),
        bool(status & 4),bool(status & 8),bool(status & 2)).validate(memory)

def update_recruitment_input_cursor_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12F58..12F8E: update recruitment input cursor."""
    frame = memory.enter(frame)
    destination = memory.state.read(4294964124, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 24, 16, True, True)
    if not bool(frame.status_word & 1):
        frame = _command_store_fields(memory, frame, 4294964124, 24, 16)
    destination = memory.state.read(4294964124, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
    memory.state.write(4294964124, 2, result)
    destination = memory.state.read(4294964124, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 12, 16, True, True)
    if not bool(frame.status_word & 1):
        frame = frame.with_address(0, u32(77684 + -1252))
        frame = _command_load_fields(memory, frame, 0, 80, 16)
        value = memory.state.read(4294964122, 2)
        frame = _command_load_fields(memory, frame, 1, value, 16)
        frame = _command_shift_fields(memory, frame, 1, 3, 16, False)
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 248, 16, False, False)
        frame = frame.with_data(1, result, 16)
        frame = _command_load_fields(memory, frame, 2, 0, 16)
        frame = _command_call_fields(memory, frame, 44040, 77708)
    return frame

def update_recruitment_total_cursor_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13034..1306A: update recruitment total cursor."""
    frame = memory.enter(frame)
    destination = memory.state.read(4294964124, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 24, 16, True, True)
    if not bool(frame.status_word & 1):
        frame = _command_store_fields(memory, frame, 4294964124, 24, 16)
    destination = memory.state.read(4294964124, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
    memory.state.write(4294964124, 2, result)
    destination = memory.state.read(4294964124, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 12, 16, True, True)
    if not bool(frame.status_word & 1):
        frame = frame.with_address(0, u32(77904 + -1472))
        frame = _command_load_fields(memory, frame, 0, 104, 16)
        value = memory.state.read(4294964122, 2)
        frame = _command_load_fields(memory, frame, 1, value, 16)
        frame = _command_shift_fields(memory, frame, 1, 3, 16, False)
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 248, 16, False, False)
        frame = frame.with_data(1, result, 16)
        frame = _command_load_fields(memory, frame, 2, 0, 16)
        frame = _command_call_fields(memory, frame, 44040, 77928)
    return frame

def append_recruitment_dialog_frame_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """1306A..13176: append recruitment dialog frame."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50324, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 12, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 15, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50580, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50452, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49181, 16)
    frame = _command_load_fields(memory, frame, 1, 3, 16)
    frame = _command_call_fields(memory, frame, 78198, 78008)
    frame = _command_load_fields(memory, frame, 0, 49157, 16)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_call_fields(memory, frame, 78198, 78020)
    frame = _command_load_fields(memory, frame, 0, 6, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 49153, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(34))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50708, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 12, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 15, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50964, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50836, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49161, 16)
    frame = _command_load_fields(memory, frame, 1, 3, 16)
    frame = _command_call_fields(memory, frame, 78198, 78122)
    frame = _command_load_fields(memory, frame, 0, 8, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 49153, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(34))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 51092, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 12, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 238, 16, False, False)
    memory.state.write(4294963994, 2, result)
    tested = memory.state.read(4294964132, 1)
    frame = _command_bit_fields(memory, frame, tested, 0 % 8)
    memory.state.write(4294964132, 1, tested | 1 << 0 % 8)
    return frame

def append_recruitment_paired_tiles_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13176..13188: append recruitment paired tiles."""
    frame = memory.enter(frame)
    return _command_numbered_pair_fields(memory, frame, 'recruitment_equipment')

def prepare_player_recruitment_capacity_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13188..1321C: prepare player recruitment capacity."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, 4294964196, 0, 32, True)
    frame = _command_store_fields(memory, frame, 4294964126, 0, 32, True)
    frame = _command_store_fields(memory, frame, 4294964122, 3, 16)
    value = memory.state.read(4294964068, 2)
    frame = _command_load_fields(memory, frame, 0, value, 16)
    frame = _command_shift_fields(memory, frame, 0, 2, 16, False)
    frame = frame.with_address(0, 4294959100)
    value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)
    frame = _command_store_fields(memory, frame, 4294964200, value, 32)
    value = memory.state.read(4294964200, 4)
    frame = _command_load_fields(memory, frame, 2, value, 32)
    frame = _command_quotient_fields(memory, frame, 2, 100, 78250)
    frame = frame.with_address(1, 4294959420)
    value = memory.state.read(u32(frame.addresses[1] + s16(frame.data[0] & 65535)), 4)
    frame = _command_load_fields(memory, frame, 3, value, 32)
    frame = _command_load_fields(memory, frame, 4, frame.data[3], 32)
    frame = _command_product_fields(memory, frame, 3, 10)
    value = frame.data[4]
    frame = _command_load_fields(memory, frame, 4, (value & 65535) << 16 | value >> 16, 32)
    frame = _command_product_fields(memory, frame, 4, 10)
    value = frame.data[4]
    frame = _command_load_fields(memory, frame, 4, (value & 65535) << 16 | value >> 16, 32)
    frame, result = _command_binary_fields(memory, frame, frame.data[3], frame.data[4], 32, False, False)
    frame = frame.with_data(3, result, 32)
    frame = frame.with_address(1, 4294961012)
    frame = _command_load_fields(memory, frame, 4, 100000, 32)
    source = memory.state.read(u32(frame.addresses[1] + s16(frame.data[0] & 65535)), 4)
    frame, result = _command_binary_fields(memory, frame, frame.data[4], source, 32, True, False)
    frame = frame.with_data(4, result, 32)
    frame = _command_quotient_fields(memory, frame, 4, 100, 78292)
    result = frame.data[4] & 65535
    frame = _command_load_fields(memory, frame, 4, result, 32)
    frame, result = _command_binary_fields(memory, frame, frame.data[4], frame.data[3], 32, True, True)
    if not not frame.status_word & 1:
        frame = _command_load_fields(memory, frame, 3, frame.data[4], 32)
    result = frame.data[2] & 65535
    frame = _command_load_fields(memory, frame, 2, result, 32)
    frame, result = _command_binary_fields(memory, frame, frame.data[2], frame.data[3], 32, True, True)
    if not bool(frame.status_word & 5):
        frame = _command_load_fields(memory, frame, 2, frame.data[3] & 65535, 16)
        frame = _command_product_fields(memory, frame, 3, 100)
        frame = _command_store_fields(memory, frame, 4294964200, frame.data[3], 32)
    frame = _command_load_fields(memory, frame, 1, 3, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 10, 16, True, True)
    if not bool(frame.status_word & 1):
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, True, False)
        frame = frame.with_data(1, result, 16)
        frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 100, 16, True, True)
        if not bool(frame.status_word & 1):
            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, True, False)
            frame = frame.with_data(1, result, 16)
            frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 1000, 16, True, True)
            if not bool(frame.status_word & 1):
                frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, True, False)
                frame = frame.with_data(1, result, 16)
    frame = _command_store_fields(memory, frame, 4294964204, frame.data[1] & 65535, 16)
    return frame

def append_recruitment_input_digits_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """1321C..13270: append recruitment input digits."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964196, 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 0, 16)
    frame = frame.with_address(6, 4294962944)
    frame = _command_call_fields(memory, frame, 75530, 78384)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50596, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(1, 4294962944)
    frame = _command_load_fields(memory, frame, 0, 0, 16)
    frame = _command_load_fields(memory, frame, 1, 5, 16)
    while True:
        value = memory.state.read(u32(frame.addresses[1]), 2)
        frame = frame.with_address(1, frame.addresses[1] + 2)
        frame = _command_load_fields(memory, frame, 2, value, 16)
        if not not frame.status_word & 4:
            source = memory.state.read(4294964122, 2)
            frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, True, True)
            if not frame.status_word & 1:
                frame = _command_load_fields(memory, frame, 2, 50054, 16)
            else:
                frame = _command_load_fields(memory, frame, 2, 49153, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
        frame = frame.with_data(0, result, 16)
        frame, repeat = _command_dbra_fields(frame, 1)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_recruitment_total_digits_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13270..132AE: append recruitment total digits."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964126, 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 49153, 16)
    frame = frame.with_address(6, 4294962956)
    frame = _command_call_fields(memory, frame, 75530, 78470)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50980, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(1, 4294962956)
    frame = _command_load_fields(memory, frame, 0, 2, 16)
    while True:
        value = memory.state.read(u32(frame.addresses[1]), 4)
        frame = frame.with_address(1, frame.addresses[1] + 4)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), value, 32)
        frame = frame.with_address(0, frame.addresses[0] + 4)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_equipment_amount_cursor_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13510..1353E: append equipment amount cursor."""
    frame = memory.enter(frame)
    tested = memory.state.read(4294964739, 1)
    frame = _command_bit_fields(memory, frame, tested, 5 % 8)
    if not not frame.status_word & 4:
        tested = memory.state.read(4294964001, 1)
        frame = _command_bit_fields(memory, frame, tested, 3 % 8)
        if not not frame.status_word & 4:
            frame = frame.with_address(0, u32(79140 + -2708))
            frame = _command_load_fields(memory, frame, 0, 88, 16)
            value = memory.state.read(4294964122, 2)
            frame = _command_load_fields(memory, frame, 1, value, 16)
            frame = _command_shift_fields(memory, frame, 1, 3, 16, False)
            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 144, 16, False, False)
            frame = frame.with_data(1, result, 16)
            frame = _command_load_fields(memory, frame, 2, 0, 16)
            frame = _command_call_fields(memory, frame, 44040, 79164)
    return frame

def clear_equipment_dialog_rows_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """1353E..135C4: clear equipment dialog rows."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 204), 15, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 170), 15, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 136), 15, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 102), 15, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 68), 15, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 15, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 204), 51092, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 170), 50964, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 136), 50836, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 102), 50708, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 68), 50580, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50452, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50324, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 14, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 204), 0, 16, True)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 170), 0, 16, True)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 136), 0, 16, True)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 102), 0, 16, True)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 68), 0, 16, True)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 0, 16, True)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 204), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 238, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_equipment_dialog_frame_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """135C4..136E2: append equipment dialog frame."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50324, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 12, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 15, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50580, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50452, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49169, 16)
    frame = _command_load_fields(memory, frame, 1, 3, 16)
    frame = _command_call_fields(memory, frame, 79586, 79378)
    frame = _command_load_fields(memory, frame, 0, 49185, 16)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_call_fields(memory, frame, 79586, 79390)
    frame = _command_load_fields(memory, frame, 0, 6, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 49153, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(34))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50708, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 12, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 15, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50964, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50836, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49177, 16)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_call_fields(memory, frame, 79586, 79492)
    frame = _command_load_fields(memory, frame, 0, 49189, 16)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_call_fields(memory, frame, 79586, 79504)
    frame = _command_load_fields(memory, frame, 0, 49185, 16)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_call_fields(memory, frame, 79586, 79516)
    frame = _command_load_fields(memory, frame, 0, 6, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 49153, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 34), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(34))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 15, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 51092, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 12, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 238, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_equipment_paired_tiles_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """136E2..136F4: append equipment paired tiles."""
    frame = memory.enter(frame)
    return _command_numbered_pair_fields(memory, frame, 'recruitment_equipment')

def append_equipment_input_digits_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """136F4..1374A: append equipment input digits."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964206, 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 0, 16)
    frame = frame.with_address(6, 4294962944)
    frame = _command_call_fields(memory, frame, 75530, 79624)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50596, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 1, 0, 16)
    frame = frame.with_address(1, 4294962944)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    while True:
        value = memory.state.read(u32(frame.addresses[1]), 2)
        frame = frame.with_address(1, frame.addresses[1] + 2)
        frame = _command_load_fields(memory, frame, 2, value, 16)
        if not not frame.status_word & 4:
            source = memory.state.read(4294964122, 2)
            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, source, 16, True, True)
            if bool(frame.status_word & 1):
                frame = _command_load_fields(memory, frame, 2, 49153, 16)
            else:
                frame = _command_load_fields(memory, frame, 2, 50054, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)
        frame = frame.with_data(1, result, 16)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_equipment_total_digits_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """1374A..1379A: append equipment total digits."""
    frame = memory.enter(frame)
    destination = memory.state.read(4294964066, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 27, 16, True, True)
    if bool(frame.status_word & 4):
        value = memory.state.read(4294954926, 4)
        frame = _command_load_fields(memory, frame, 0, value, 32)
    else:
        value = memory.state.read(4294964196, 4)
        frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 49153, 16)
    frame = frame.with_address(6, 4294962956)
    frame = _command_call_fields(memory, frame, 75530, 79730)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50980, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(1, 4294962956)
    frame = _command_load_fields(memory, frame, 0, 2, 16)
    while True:
        value = memory.state.read(u32(frame.addresses[1]), 4)
        frame = frame.with_address(1, frame.addresses[1] + 4)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), value, 32)
        frame = frame.with_address(0, frame.addresses[0] + 4)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_candidate_amount_cursor_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13934..13958: append candidate amount cursor."""
    frame = memory.enter(frame)
    tested = memory.state.read(4294964001, 1)
    frame = _command_bit_fields(memory, frame, tested, 3 % 8)
    if not not frame.status_word & 4:
        frame = frame.with_address(0, u32(80190 + -3758))
        frame = _command_load_fields(memory, frame, 0, 88, 16)
        value = memory.state.read(4294964122, 2)
        frame = _command_load_fields(memory, frame, 1, value, 16)
        frame = _command_shift_fields(memory, frame, 1, 3, 16, False)
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 144, 16, False, False)
        frame = frame.with_data(1, result, 16)
        frame = _command_load_fields(memory, frame, 2, 0, 16)
        frame = _command_call_fields(memory, frame, 44040, 80214)
    return frame

def append_candidate_dialog_frame_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13958..13A84: append candidate dialog frame."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50208, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 2, 50464, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), frame.data[2] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 128, 16, True, False)
    frame = frame.with_data(2, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 256, 16, False, False)
    frame = frame.with_data(2, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49157, 16)
    frame = _command_load_fields(memory, frame, 1, 5, 16)
    frame = _command_call_fields(memory, frame, 80516, 80302)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(20))
    frame = _command_call_fields(memory, frame, 80534, 80320)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), frame.data[2] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 128, 16, True, False)
    frame = frame.with_data(2, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 256, 16, False, False)
    frame = frame.with_data(2, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49169, 16)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_call_fields(memory, frame, 80516, 80366)
    frame = _command_load_fields(memory, frame, 0, 49161, 16)
    frame = _command_load_fields(memory, frame, 1, 3, 16)
    frame = _command_call_fields(memory, frame, 80516, 80378)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(20))
    frame = _command_call_fields(memory, frame, 80534, 80396)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), frame.data[2] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 128, 16, True, False)
    frame = frame.with_data(2, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 256, 16, False, False)
    frame = frame.with_data(2, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49157, 16)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_call_fields(memory, frame, 80516, 80442)
    frame = _command_load_fields(memory, frame, 0, 49173, 16)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_call_fields(memory, frame, 80516, 80454)
    frame = _command_load_fields(memory, frame, 0, 49169, 16)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_call_fields(memory, frame, 80516, 80466)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(20))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 200, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_candidate_paired_tiles_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13A84..13A96: append candidate paired tiles."""
    frame = memory.enter(frame)
    return _command_numbered_pair_fields(memory, frame, 'candidate')

def append_candidate_separator_row_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13A96..13AB6: append candidate separator row."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 256, 16, False, False)
    frame = frame.with_data(2, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    return frame

def update_equipment_category_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13B86..13BDA: update equipment category."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964738, 1)
    frame = _command_load_fields(memory, frame, 0, value, 8)
    result = frame.data[0] & 65535 & 3
    frame = _command_load_fields(memory, frame, 0, result, 16)
    if bool(frame.status_word & 4):
        frame = _command_store_fields(memory, frame, 4294964744, 1, 16)
    else:
        destination = memory.state.read(4294964744, 2)
        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
        memory.state.write(4294964744, 2, result)
        if not not frame.status_word & 4:
            frame = _command_store_fields(memory, frame, 4294964744, 12, 16)
            frame = _command_bit_fields(memory, frame, frame.data[0], 1 % 32)
            if not frame.status_word & 4:
                destination = memory.state.read(4294964872, 2)
                frame, result = _command_binary_fields(memory, frame, destination, 2, 16, True, True)
                if bool(frame.status_word & 1):
                    destination = memory.state.read(4294964872, 2)
                    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, False, False)
                    memory.state.write(4294964872, 2, result)
                else:
                    frame = _command_store_fields(memory, frame, 4294964872, 0, 16, True)
            else:
                value = memory.state.read(4294964872, 2)
                frame = _command_test_fields(memory, frame, value, 16)
                if not frame.status_word & 4:
                    destination = memory.state.read(4294964872, 2)
                    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
                    memory.state.write(4294964872, 2, result)
                else:
                    frame = _command_store_fields(memory, frame, 4294964872, 2, 16)
    return frame

def append_equipment_category_cursor_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13BDA..13C1C: append equipment category cursor."""
    frame = memory.enter(frame)
    tested = memory.state.read(4294964739, 1)
    frame = _command_bit_fields(memory, frame, tested, 5 % 8)
    if not not frame.status_word & 4:
        value = memory.state.read(4294964738, 1)
        frame = _command_load_fields(memory, frame, 0, value, 8)
        result = frame.data[0] & 65535 & 3
        frame = _command_load_fields(memory, frame, 0, result, 16)
        if not frame.status_word & 4:
            frame = frame.with_address(0, u32(80890 + 34))
            value = memory.state.read(4294964872, 2)
            frame = _command_load_fields(memory, frame, 0, value, 16)
            frame = _command_shift_fields(memory, frame, 0, 1, 16, False)
            source = memory.state.read(4294964872, 2)
            frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, False, False)
            frame = frame.with_data(0, result, 16)
            frame = _command_shift_fields(memory, frame, 0, 3, 16, False)
            frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 64, 16, False, False)
            frame = frame.with_data(0, result, 16)
            frame = _command_load_fields(memory, frame, 1, 128, 16)
            frame = _command_load_fields(memory, frame, 2, 0, 16)
            frame = _command_call_fields(memory, frame, 44040, 80922)
        else:
            tested = memory.state.read(4294964001, 1)
            frame = _command_bit_fields(memory, frame, tested, 4 % 8)
            if not not frame.status_word & 4:
                frame = frame.with_address(0, u32(80890 + 34))
                value = memory.state.read(4294964872, 2)
                frame = _command_load_fields(memory, frame, 0, value, 16)
                frame = _command_shift_fields(memory, frame, 0, 1, 16, False)
                source = memory.state.read(4294964872, 2)
                frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, False, False)
                frame = frame.with_data(0, result, 16)
                frame = _command_shift_fields(memory, frame, 0, 3, 16, False)
                frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 64, 16, False, False)
                frame = frame.with_data(0, result, 16)
                frame = _command_load_fields(memory, frame, 1, 128, 16)
                frame = _command_load_fields(memory, frame, 2, 0, 16)
                frame = _command_call_fields(memory, frame, 44040, 80922)
    return frame

def clear_candidate_dialog_rows_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13C7E..13D48: clear candidate dialog rows."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 180), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 160), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 140), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 120), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 100), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 80), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 40), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 180), 51360, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 160), 51232, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 140), 51104, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 120), 50976, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 100), 50848, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 80), 50720, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 50592, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 40), 50464, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50336, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50208, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 7, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 180), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 160), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 140), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 120), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 100), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 80), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 40), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 32768, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 180), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 200, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def prepare_selected_training_cost_steps_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13DF6..13E42: prepare selected training cost steps."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294964480)
    frame = frame.with_address(1, 4294952960)
    frame = _command_load_fields(memory, frame, 0, 0, 32)
    while True:
        value = memory.state.read(u32(frame.addresses[0]), 2)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame = _command_load_fields(memory, frame, 1, value, 16)
        if bool(frame.status_word & 8):
            break
        frame = _command_bit_fields(memory, frame, frame.data[1], 14 % 32)
        if bool(frame.status_word & 4):
            continue
        frame = _command_shift_fields(memory, frame, 1, 2, 16, False)
        source = memory.state.read(u32(frame.addresses[1] + s16(frame.data[1] & 65535)), 4)
        frame, result = _command_binary_fields(memory, frame, frame.data[0], source, 32, False, False)
        frame = frame.with_data(0, result, 32)
        frame, result = _command_binary_fields(memory, frame, frame.data[0], 100, 32, False, False)
        frame = frame.with_data(0, result, 32)
        continue
    frame = _command_quotient_fields(memory, frame, 0, 100, 81434)
    if not not frame.status_word & 4:
        frame = _command_load_fields(memory, frame, 0, 1, 16)
    result = frame.data[0] & 65535
    frame = _command_load_fields(memory, frame, 0, result, 32)
    frame = _command_store_fields(memory, frame, 4294965070, frame.data[0], 32)
    frame = _command_product_fields(memory, frame, 0, 10)
    frame = _command_store_fields(memory, frame, 4294965074, frame.data[0], 32)
    frame = _command_product_fields(memory, frame, 0, 10)
    frame = _command_store_fields(memory, frame, 4294965078, frame.data[0], 32)
    return frame

def update_selected_training_amount_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13E92..13F66: update selected training amount."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964738, 1)
    frame = _command_load_fields(memory, frame, 0, value, 8)
    result = frame.data[0] & 65535 & 12
    frame = _command_load_fields(memory, frame, 0, result, 16)
    if bool(frame.status_word & 4):
        value = memory.state.read(4294964738, 1)
        frame = _command_load_fields(memory, frame, 0, value, 8)
        result = frame.data[0] & 255 & 3
        frame = _command_load_fields(memory, frame, 0, result, 8)
        if bool(frame.status_word & 4):
            frame = _command_store_fields(memory, frame, 4294964744, 1, 16)
        else:
            destination = memory.state.read(4294964744, 2)
            frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
            memory.state.write(4294964744, 2, result)
            if not not frame.status_word & 4:
                frame = _command_store_fields(memory, frame, 4294964744, 12, 16)
                frame = _command_load_fields(memory, frame, 1, 2, 16)
                source = memory.state.read(4294964122, 2)
                frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, source, 16, True, False)
                frame = frame.with_data(1, result, 16)
                frame = _command_shift_fields(memory, frame, 1, 2, 16, False)
                frame = frame.with_address(0, 4294965070)
                value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[1] & 65535)), 4)
                frame = _command_load_fields(memory, frame, 2, value, 32)
                frame = _command_shift_fields(memory, frame, 1, 1, 16, True)
                value = memory.state.read(u32(81686 + 80 + s16(frame.data[1] & 65535)), 2)
                frame = _command_load_fields(memory, frame, 4, value, 16)
                frame = _command_bit_fields(memory, frame, frame.data[0], 1 % 32)
                if not frame.status_word & 4:
                    value = memory.state.read(4294964154, 4)
                    frame = _command_load_fields(memory, frame, 3, value, 32)
                    frame, result = _command_binary_fields(memory, frame, frame.data[3], frame.data[2], 32, True, False)
                    frame = frame.with_data(3, result, 32)
                    if not bool(frame.status_word & 1):
                        frame = _command_store_fields(memory, frame, 4294964154, frame.data[3], 32)
                        destination = memory.state.read(4294964848, 2)
                        frame, result = _command_binary_fields(memory, frame, destination, frame.data[4] & 65535, 16, True, False)
                        memory.state.write(4294964848, 2, result)
                else:
                    value = memory.state.read(4294964154, 4)
                    frame = _command_load_fields(memory, frame, 3, value, 32)
                    frame, result = _command_binary_fields(memory, frame, frame.data[3], frame.data[2], 32, False, False)
                    frame = frame.with_data(3, result, 32)
                    source = memory.state.read(4294964216, 4)
                    frame, result = _command_binary_fields(memory, frame, frame.data[3], source, 32, True, True)
                    if not not frame.status_word & 5:
                        value = memory.state.read(4294964848, 2)
                        frame = _command_load_fields(memory, frame, 5, value, 16)
                        frame, result = _command_binary_fields(memory, frame, frame.data[5] & 65535, frame.data[4] & 65535, 16, False, False)
                        frame = frame.with_data(5, result, 16)
                        frame, result = _command_binary_fields(memory, frame, frame.data[5] & 65535, 1000, 16, True, True)
                        if not not frame.status_word & 1:
                            frame = _command_store_fields(memory, frame, 4294964154, frame.data[3], 32)
                            frame = _command_store_fields(memory, frame, 4294964848, frame.data[5] & 65535, 16)
    else:
        destination = memory.state.read(4294964744, 2)
        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
        memory.state.write(4294964744, 2, result)
        if not not frame.status_word & 4:
            frame = _command_store_fields(memory, frame, 4294964744, 12, 16)
            frame = _command_bit_fields(memory, frame, frame.data[0], 3 % 32)
            if not frame.status_word & 4:
                destination = memory.state.read(4294964122, 2)
                frame, result = _command_binary_fields(memory, frame, destination, 2, 16, True, True)
                if not not frame.status_word & 1:
                    destination = memory.state.read(4294964122, 2)
                    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, False, False)
                    memory.state.write(4294964122, 2, result)
                    value = memory.state.read(4294964738, 1)
                    frame = _command_load_fields(memory, frame, 0, value, 8)
                    result = frame.data[0] & 255 & 3
                    frame = _command_load_fields(memory, frame, 0, result, 8)
                    if bool(frame.status_word & 4):
                        frame = _command_store_fields(memory, frame, 4294964744, 1, 16)
                    else:
                        destination = memory.state.read(4294964744, 2)
                        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
                        memory.state.write(4294964744, 2, result)
                        if not not frame.status_word & 4:
                            frame = _command_store_fields(memory, frame, 4294964744, 12, 16)
                            frame = _command_load_fields(memory, frame, 1, 2, 16)
                            source = memory.state.read(4294964122, 2)
                            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, source, 16, True, False)
                            frame = frame.with_data(1, result, 16)
                            frame = _command_shift_fields(memory, frame, 1, 2, 16, False)
                            frame = frame.with_address(0, 4294965070)
                            value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[1] & 65535)), 4)
                            frame = _command_load_fields(memory, frame, 2, value, 32)
                            frame = _command_shift_fields(memory, frame, 1, 1, 16, True)
                            value = memory.state.read(u32(81686 + 80 + s16(frame.data[1] & 65535)), 2)
                            frame = _command_load_fields(memory, frame, 4, value, 16)
                            frame = _command_bit_fields(memory, frame, frame.data[0], 1 % 32)
                            if not frame.status_word & 4:
                                value = memory.state.read(4294964154, 4)
                                frame = _command_load_fields(memory, frame, 3, value, 32)
                                frame, result = _command_binary_fields(memory, frame, frame.data[3], frame.data[2], 32, True, False)
                                frame = frame.with_data(3, result, 32)
                                if not bool(frame.status_word & 1):
                                    frame = _command_store_fields(memory, frame, 4294964154, frame.data[3], 32)
                                    destination = memory.state.read(4294964848, 2)
                                    frame, result = _command_binary_fields(memory, frame, destination, frame.data[4] & 65535, 16, True, False)
                                    memory.state.write(4294964848, 2, result)
                            else:
                                value = memory.state.read(4294964154, 4)
                                frame = _command_load_fields(memory, frame, 3, value, 32)
                                frame, result = _command_binary_fields(memory, frame, frame.data[3], frame.data[2], 32, False, False)
                                frame = frame.with_data(3, result, 32)
                                source = memory.state.read(4294964216, 4)
                                frame, result = _command_binary_fields(memory, frame, frame.data[3], source, 32, True, True)
                                if not not frame.status_word & 5:
                                    value = memory.state.read(4294964848, 2)
                                    frame = _command_load_fields(memory, frame, 5, value, 16)
                                    frame, result = _command_binary_fields(memory, frame, frame.data[5] & 65535, frame.data[4] & 65535, 16, False, False)
                                    frame = frame.with_data(5, result, 16)
                                    frame, result = _command_binary_fields(memory, frame, frame.data[5] & 65535, 1000, 16, True, True)
                                    if not not frame.status_word & 1:
                                        frame = _command_store_fields(memory, frame, 4294964154, frame.data[3], 32)
                                        frame = _command_store_fields(memory, frame, 4294964848, frame.data[5] & 65535, 16)
            else:
                value = memory.state.read(4294964122, 2)
                frame = _command_test_fields(memory, frame, value, 16)
                if not bool(frame.status_word & 4):
                    frame = _command_load_fields(memory, frame, 0, 1, 16)
                    source = memory.state.read(4294964122, 2)
                    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, True, False)
                    frame = frame.with_data(0, result, 16)
                    frame = _command_shift_fields(memory, frame, 0, 2, 16, False)
                    frame = frame.with_address(0, 4294965074)
                    value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)
                    frame = _command_load_fields(memory, frame, 0, value, 32)
                    source = memory.state.read(4294964216, 4)
                    frame, result = _command_binary_fields(memory, frame, frame.data[0], source, 32, True, True)
                    if not not frame.status_word & 5:
                        destination = memory.state.read(4294964122, 2)
                        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
                        memory.state.write(4294964122, 2, result)
    return frame

def append_training_cost_digits_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13F6C..13FAA: append training cost digits."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    value = memory.state.read(4294964154, 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 49153, 16)
    frame = frame.with_address(6, 4294955776)
    frame = _command_call_fields(memory, frame, 75530, 81802)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50860, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(1, 4294955776)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    while True:
        value = memory.state.read(u32(frame.addresses[1]), 2)
        frame = frame.with_address(1, frame.addresses[1] + 2)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), value, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_training_amount_cursor_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13FAA..13FDC: append training amount cursor."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964738, 2)
    frame = _command_load_fields(memory, frame, 0, value, 16)
    result = frame.data[0] & 65535 & 48
    frame = _command_load_fields(memory, frame, 0, result, 16)
    if not not frame.status_word & 4:
        tested = memory.state.read(4294964001, 1)
        frame = _command_bit_fields(memory, frame, tested, 3 % 8)
        if not not frame.status_word & 4:
            frame = frame.with_address(0, u32(81858 + 26))
            frame = _command_load_fields(memory, frame, 0, 88, 16)
            value = memory.state.read(4294964122, 2)
            frame = _command_load_fields(memory, frame, 1, value, 16)
            frame = _command_shift_fields(memory, frame, 1, 3, 16, False)
            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 168, 16, False, False)
            frame = frame.with_data(1, result, 16)
            frame = _command_load_fields(memory, frame, 2, 0, 16)
            frame = _command_call_fields(memory, frame, 44040, 81882)
    return frame

def prepare_selected_training_origin_and_speed_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """13FE4..14050: prepare selected training origin and speed."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294964480)
    frame = frame.with_address(1, 4294951936)
    frame = _command_load_fields(memory, frame, 0, 0, 32)
    frame = _command_load_fields(memory, frame, 1, 0, 16)
    value = memory.state.read(4294964068, 2)
    frame = _command_load_fields(memory, frame, 2, value, 16)
    frame = _command_shift_fields(memory, frame, 2, 2, 16, False)
    frame = frame.with_address(5, 871110)
    value = memory.state.read(u32(frame.addresses[5] + 2 + s16(frame.data[2] & 65535)), 2)
    frame = _command_load_fields(memory, frame, 3, value, 16)
    result = frame.data[3] & 65535 & 65520
    frame = _command_load_fields(memory, frame, 3, result, 16)
    frame = _command_store_fields(memory, frame, 16726050, frame.data[3] & 65535, 16)
    frame = _command_shift_fields(memory, frame, 3, 4, 16, False)
    result = frame.data[3] & 65535 & 65280
    frame = _command_load_fields(memory, frame, 3, result, 16)
    value = memory.state.read(u32(frame.addresses[5] + s16(frame.data[2] & 65535)), 2)
    frame = _command_load_fields(memory, frame, 4, value, 16)
    result = frame.data[4] & 65535 & 65520
    frame = _command_load_fields(memory, frame, 4, result, 16)
    frame = _command_store_fields(memory, frame, 16726052, frame.data[4] & 65535, 16)
    frame = _command_shift_fields(memory, frame, 4, 4, 16, True)
    result = frame.data[4] & 65535 | frame.data[3] & 65535
    frame = _command_load_fields(memory, frame, 4, result, 16)
    frame = _command_store_fields(memory, frame, 16726056, frame.data[4] & 65535, 16)
    while True:
        value = memory.state.read(u32(frame.addresses[0]), 2)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame = _command_load_fields(memory, frame, 2, value, 16)
        if bool(frame.status_word & 8):
            break
        frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 16384, 16, True, True)
        if bool(frame.status_word & 1):
            continue
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)
        frame = frame.with_data(1, result, 16)
        result = frame.data[2] & 65535 & 255
        frame = _command_load_fields(memory, frame, 2, result, 16)
        frame = _command_load_fields(memory, frame, 3, 0, 16)
        value = memory.state.read(u32(frame.addresses[1] + s16(frame.data[2] & 65535)), 1)
        frame = _command_load_fields(memory, frame, 3, value, 8)
        frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, frame.data[3] & 65535, 16, False, False)
        frame = frame.with_data(0, result, 16)
        continue
    frame = _command_store_fields(memory, frame, 16726058, frame.data[1] & 65535, 16)
    frame = _command_quotient_fields(memory, frame, 0, frame.data[1] & 65535, 81992)
    frame = _command_store_fields(memory, frame, 4294964850, frame.data[0] & 65535, 16)
    return frame

def _recruitment_known_fields(memory, frame, target):
    if target == 77656:
        return update_recruitment_input_cursor_frame_fields(memory, frame)
    if target == 77876:
        return update_recruitment_total_cursor_frame_fields(memory, frame)
    if target == 77930:
        return append_recruitment_dialog_frame_frame_fields(memory, frame)
    if target == 78198:
        return append_recruitment_paired_tiles_frame_fields(memory, frame)
    if target == 78216:
        return prepare_player_recruitment_capacity_frame_fields(memory, frame)
    if target == 78364:
        return append_recruitment_input_digits_frame_fields(memory, frame)
    if target == 78448:
        return append_recruitment_total_digits_frame_fields(memory, frame)
    if target == 79120:
        return append_equipment_amount_cursor_frame_fields(memory, frame)
    if target == 79166:
        return clear_equipment_dialog_rows_frame_fields(memory, frame)
    if target == 79300:
        return append_equipment_dialog_frame_frame_fields(memory, frame)
    if target == 79586:
        return append_equipment_paired_tiles_frame_fields(memory, frame)
    if target == 79604:
        return append_equipment_input_digits_frame_fields(memory, frame)
    if target == 79690:
        return append_equipment_total_digits_frame_fields(memory, frame)
    if target == 80180:
        return append_candidate_amount_cursor_frame_fields(memory, frame)
    if target == 80216:
        return append_candidate_dialog_frame_frame_fields(memory, frame)
    if target == 80516:
        return append_candidate_paired_tiles_frame_fields(memory, frame)
    if target == 80534:
        return append_candidate_separator_row_frame_fields(memory, frame)
    if target == 80774:
        return update_equipment_category_frame_fields(memory, frame)
    if target == 80858:
        return append_equipment_category_cursor_frame_fields(memory, frame)
    if target == 81022:
        return clear_candidate_dialog_rows_frame_fields(memory, frame)
    if target == 81398:
        return prepare_selected_training_cost_steps_frame_fields(memory, frame)
    if target == 81554:
        return update_selected_training_amount_frame_fields(memory, frame)
    if target == 81772:
        return append_training_cost_digits_frame_fields(memory, frame)
    if target == 81834:
        return append_training_amount_cursor_frame_fields(memory, frame)
    if target == 81892:
        return prepare_selected_training_origin_and_speed_frame_fields(memory, frame)
    return None
