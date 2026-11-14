"""Live player command amounts, repeat controls and queued UI rows.

Queue tile words are format/content values, not processor instructions. This
module does not draw to VDP or open original files. Named ports share the live
state with recruitment and display rules. Original wrapping, aliases and
unbounded searches are retained rather than cleaned up into new game rules.
"""
from .domain import (
    Boundary, Cursor, GameState, Long, Table, Word, checked_cursor, checked_state,
    checked_table, descending_inclusive, divu_retained, low16, negative_word,
    replace_byte, replace_word, swap_words, u8, u16, u32, uint,
)
from .contexts_budget import (
    CommandColumns, DecimalPlaceResult, ResourceRowInput,
    CommittedResourceRowInput, ResourceRowsInput, ResourceRowsResult,
)
from .contexts_numeric import DecimalMemory, DecimalPlaceFields, DecimalTransactionFields


from .contexts_command_fields import CommandMenuMemory, CommandFrame, _command_load_fields, _command_test_fields, _command_binary_fields, _command_store_fields, _command_shift_fields, _command_product_fields, _command_quotient_fields, _command_bit_fields, _command_dbra_fields, _command_call_fields, _command_tail_fields, _command_numbered_pair_fields, _command_decimal_transaction_fields, _command_decimal_place_fields
from .domain import u16, u32, s16

def prepare_budget_summary_panel(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 72946)
    actual = prepare_budget_summary_panel_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def append_numbered_budget_columns(state: GameState, out: Cursor, tile: Word, latch: Word, *, entry_frame: CommandFrame | None=None) -> Word:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 73258)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    uint(tile, 16)
    if tile != entered.data[1] & 65535:
        raise ValueError('actual numbered tile WORD required')
    uint(latch, 16)
    if latch != entered.data[2] & 65535:
        raise ValueError('actual loop counter WORD required')
    actual = append_numbered_budget_columns_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return actual.data[1] & 65535


def prepare_compact_budget_summary_panel(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 73276)
    actual = prepare_compact_budget_summary_panel_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def select_descriptor_portrait_parts(state: GameState, retained_mask_high: Word=0, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 73602)
    actual = select_descriptor_portrait_parts_frame_fields(memory, entered)
    return None


def find_first_set_mask_bit(state: GameState, mask: Long, *, entry_frame: CommandFrame | None=None) -> Word:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 73722)
    uint(mask, 32)
    if mask != entered.data[0]:
        raise ValueError('actual original mask LONG required')
    actual = find_first_set_mask_bit_frame_fields(memory, entered)
    return actual.data[1] & 65535


def prepare_command_amount_modal(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 73736)
    actual = prepare_command_amount_modal_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def append_amount_modal_frame(state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 73764)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    actual = append_amount_modal_frame_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return None


def append_amount_modal_descriptor_limit(state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 73828)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    actual = append_amount_modal_descriptor_limit_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return None


def append_selected_command_row_label(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 74268)
    actual = append_selected_command_row_label_frame_fields(memory, entered)
    return None


def clear_command_amount_page(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 74386)
    actual = clear_command_amount_page_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def prepare_budget_amount_page(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 74516)
    actual = prepare_budget_amount_page_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def step_budget_amount_controls(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 74776)
    actual = step_budget_amount_controls_frame_fields(memory, entered)
    return None


def append_budget_cost_and_amount_values(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 75052)
    actual = append_budget_cost_and_amount_values_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def append_budget_place_highlight(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 75180)
    actual = append_budget_place_highlight_frame_fields(memory, entered)
    return None


def append_budget_header_row(state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 75266)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    actual = append_budget_header_row_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return None


def append_budget_first_detail_rows(state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 75296)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    actual = append_budget_first_detail_rows_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return None


def append_budget_second_detail_row(state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 75404)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    actual = append_budget_second_detail_row_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return None


def append_budget_footer_row(state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 75474)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    actual = append_budget_footer_row_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return None


def append_four_budget_numbered_tiles(state: GameState, out: Cursor, tile: Word, *, entry_frame: CommandFrame | None=None) -> Word:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 75504)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    uint(tile, 16)
    if tile != entered.data[0] & 65535:
        raise ValueError('actual numbered tile WORD required')
    actual = append_four_budget_numbered_tiles_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return actual.data[0] & 65535


def append_six_place_decimal_value(state: GameState, value: Long, digit_tile: Word, blank_tile: Word, destination: Cursor) -> Cursor:
    checked_state(state); uint(value, 32); uint(digit_tile, 16); uint(blank_tile, 16); checked_cursor(destination, state)
    return _six_place_decimal_fields(DecimalMemory(state), value, digit_tile, blank_tile, destination).destination


def _six_place_decimal_fields(memory: DecimalMemory, value: Long, digit_tile: Word, blank_tile: Word, destination: Cursor) -> DecimalTransactionFields:
    """Single 1270A algorithm: ordered cells and actual final numeric fields."""
    if type(memory) is not DecimalMemory:
        raise ValueError('sealed decimal memory required')
    memory.check_cursor(destination)
    uint(value, 32); uint(digit_tile, 16); uint(blank_tile, 16)
    leading = u16(0); started = u16(0)
    while True:
        previous = value
        value = u32(value - 100000)
        if previous < 100000: break
        leading = u16(leading + 1)
    value = u32(value + 100000)
    if leading == 0: destination.append_word(blank_tile)
    else:
        glyph = memory.glyph(leading)
        destination.append_word(u16(digit_tile + glyph)); started = u16(started + 1)
    for divisor, continuation in ((10000, 0x1273C), (1000, 0x12744), (100, 0x1274C), (10, 0x12754)):
        memory.enter_call(continuation)
        result = _decimal_value_place_fields(memory, value, divisor, digit_tile, blank_tile, started, destination)
        memory.leave_call(continuation)
        value, started = result.remainder, result.started
    glyph = u16(digit_tile + memory.glyph(low16(value)))
    destination.append_word(glyph)
    return DecimalTransactionFields(destination, value, divisor, started, glyph)


def append_decimal_value_place(state: GameState, value: Long, divisor: Word, tile_base: Word, blank: Word, started: Word, out: Cursor) -> DecimalPlaceResult:
    checked_state(state); uint(value, 32); uint(divisor, 16); uint(tile_base, 16); uint(blank, 16); uint(started, 16); checked_cursor(out, state)
    result = _decimal_value_place_fields(DecimalMemory(state), value, divisor, tile_base, blank, started, out)
    return DecimalPlaceResult(result.remainder, result.started)


def _decimal_value_place_fields(memory: DecimalMemory, value: Long, divisor: Word, tile_base: Word, blank: Word, started: Word, out: Cursor) -> DecimalPlaceFields:
    """12760 packed DIVU, including overflow retention and blank-cell D5=0."""
    if type(memory) is not DecimalMemory:
        raise ValueError('sealed decimal memory required')
    memory.check_cursor(out)
    uint(value, 32); uint(divisor, 16); uint(tile_base, 16); uint(blank, 16); uint(started, 16)
    packed = divu_retained(value, divisor)
    quotient = low16(packed)
    glyph = u16(0)
    if started != 0 or quotient != 0:
        glyph = u16(tile_base + memory.glyph(quotient))
        out.append_word(glyph); started = u16(1)
    else: out.append_word(blank)
    return DecimalPlaceFields(packed >> 16, started, glyph)


def prepare_command_amount_limit(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 75660)
    actual = prepare_command_amount_limit_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def limit_live_command_amount_by_price_record(state: GameState, records: Cursor, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 75896)
    checked_cursor(records, state)
    if records.base != entered.addresses[0]:
        raise ValueError('legacy records must be the actual A0 entry')
    actual = limit_live_command_amount_by_price_record_frame_fields(memory, entered)
    return None


def update_player_command_amount(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76002)
    actual = update_player_command_amount_frame_fields(memory, entered)
    return None


def append_selected_command_amount(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76076)
    actual = append_selected_command_amount_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def step_live_command_amount_controls(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76160)
    actual = step_live_command_amount_controls_frame_fields(memory, entered)
    return None


def select_previous_amount_place(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76254)
    actual = select_previous_amount_place_frame_fields(memory, entered)
    return None


def select_next_amount_place(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76280)
    actual = select_next_amount_place_frame_fields(memory, entered)
    return None


def decrement_live_command_amount_small(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76334)
    actual = decrement_live_command_amount_small_frame_fields(memory, entered)
    return None


def append_blinking_amount_place(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76366)
    actual = append_blinking_amount_place_frame_fields(memory, entered)
    return None


def prepare_percentage_panel(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76440)
    actual = prepare_percentage_panel_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def append_percentage_header_row(state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76470)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    actual = append_percentage_header_row_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return None


def append_percentage_value_rows(state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76500)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    actual = append_percentage_value_rows_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return None


def append_percentage_footer_row(state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76620)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    actual = append_percentage_footer_row_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return None


def clear_percentage_panel(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76650)
    actual = clear_percentage_panel_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def append_percentage_value(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76736)
    actual = append_percentage_value_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def step_percentage_controls(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76812)
    actual = step_percentage_controls_frame_fields(memory, entered)
    return None


def append_percentage_place_highlight(state: GameState, *, entry_frame: CommandFrame | None=None) -> None:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76932)
    actual = append_percentage_place_highlight_frame_fields(memory, entered)
    return None


def prepare_resource_amount_panel(state: GameState, *, entry_frame: CommandFrame | None=None) -> Cursor:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 76990)
    actual = prepare_resource_amount_panel_frame_fields(memory, entered)
    return memory.cursor_at(actual.addresses[0])


def append_city_resource_amount_rows(state: GameState, out: Cursor, *, entry_frame: CommandFrame | None=None) -> ResourceRowsResult:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 77044)
    checked_cursor(out, state)
    if out.base != entered.addresses[0]:
        raise ValueError('legacy output must be the actual A0 entry')
    actual = append_city_resource_amount_rows_frame_fields(memory, entered)
    out.base = actual.addresses[0]
    return ResourceRowsResult(memory.cursor_at(actual.addresses[0]), actual.data[0])


def append_live_resource_value_row(state: GameState, context: ResourceRowInput, *, entry_frame: CommandFrame | None=None) -> ResourceRowsResult:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 77186)
    context.validate(state)
    if context.destination.base != entered.addresses[0]:
        raise ValueError('resource context must match real A0 entry')
    if context.tile_carrier != entered.data[0]:
        raise ValueError('actual resource LONG required')
    actual = append_live_resource_value_row_frame_fields(memory, entered)
    return ResourceRowsResult(memory.cursor_at(actual.addresses[0]), actual.data[0])


def append_committed_resource_amount_rows(state: GameState, context: ResourceRowsInput, *, entry_frame: CommandFrame | None=None) -> ResourceRowsResult:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 77308)
    context.validate(state)
    if context.destination.base != entered.addresses[0]:
        raise ValueError('resource context must match real A0 entry')
    if context.numeric_carrier != entered.data[0]:
        raise ValueError('actual resource LONG required')
    actual = append_committed_resource_amount_rows_frame_fields(memory, entered)
    return ResourceRowsResult(memory.cursor_at(actual.addresses[0]), actual.data[0])


def append_committed_resource_value_row(state: GameState, context: CommittedResourceRowInput, *, entry_frame: CommandFrame | None=None) -> ResourceRowsResult:
    """Legacy projection of the sole actual complete menu algorithm."""
    memory, entered = _command_legacy_entry(state, entry_frame, 77428)
    context.validate(state)
    if context.destination.base != entered.addresses[0]:
        raise ValueError('resource context must match real A0 entry')
    if context.tile_carrier != entered.data[0]:
        raise ValueError('actual resource LONG required')
    actual = append_committed_resource_value_row_frame_fields(memory, entered)
    return ResourceRowsResult(memory.cursor_at(actual.addresses[0]), actual.data[0])

def _command_legacy_entry(state, entry_frame, original_entry):
    """Never infer absent full LONGs, high WORDs, SR-X or physical SP."""
    checked_state(state)
    if entry_frame is None:
        raise Boundary('historical scalar menu API lacks actual complete entry carriers; use its named frame core')
    if type(entry_frame) is not CommandFrame:
        raise ValueError('actual complete CommandFrame required')
    uint(original_entry,32)
    memory = CommandMenuMemory(state)
    return memory, memory.enter(entry_frame)

def prepare_budget_summary_panel_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """11CF2..11E2A: prepare budget summary panel."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50082, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49954, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 32768, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = frame.with_address(0, frame.addresses[0] + s16(16))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50210, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 3, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50466, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50338, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 1, 49269, 16)
    frame = _command_load_fields(memory, frame, 2, 3, 16)
    frame = _command_call_fields(memory, frame, 73258, 73066)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(16))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50594, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 3, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50850, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50722, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 1, 49277, 16)
    frame = _command_load_fields(memory, frame, 2, 3, 16)
    frame = _command_call_fields(memory, frame, 73258, 73150)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(16))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50978, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 3, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 32), 6, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 32), 51362, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 51234, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 51106, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 32), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 32768, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 192, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_numbered_budget_columns_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """11E2A..11E3C: append numbered budget columns."""
    frame = memory.enter(frame)
    return _command_numbered_pair_fields(memory, frame, 'budget')

def prepare_compact_budget_summary_panel_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """11E3C..11F1C: prepare compact budget summary panel."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50210, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 3, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50466, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50338, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 2, 3, 16)
    frame = _command_load_fields(memory, frame, 1, 49285, 16)
    frame = _command_call_fields(memory, frame, 73258, 73352)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(16))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50594, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 3, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 6, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50850, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50722, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 2, 1, 16)
    frame = _command_load_fields(memory, frame, 1, 49293, 16)
    frame = _command_call_fields(memory, frame, 73258, 73436)
    frame = _command_load_fields(memory, frame, 2, 1, 16)
    frame = _command_load_fields(memory, frame, 1, 49153, 16)
    frame = _command_call_fields(memory, frame, 73258, 73448)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 16), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(16))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50978, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 3, 16)
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
    frame, result = _command_binary_fields(memory, frame, destination, 112, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def select_descriptor_portrait_parts_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """11F82..11FFA: select descriptor portrait parts."""
    frame = memory.enter(frame)
    value = memory.state.read(16726060, 4)
    frame = frame.with_address(0, value)
    value = memory.state.read(u32(frame.addresses[0] + 1), 1)
    frame = _command_load_fields(memory, frame, 0, value, 8)
    value = memory.state.read(u32(frame.addresses[0] + 2), 1)
    frame = _command_load_fields(memory, frame, 1, value, 8)
    frame = _command_load_fields(memory, frame, 2, 0, 16)
    frame = frame.with_address(1, 871714)
    while True:
        source = memory.state.read(u32(frame.addresses[1]), 1)
        frame, result = _command_binary_fields(memory, frame, frame.data[0] & 255, source, 8, True, True)
        if not frame.status_word & 4:
            frame = frame.with_address(1, frame.addresses[1] + 2)
            frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 1, 16, False, False)
            frame = frame.with_data(2, result, 16)
            continue
        source = memory.state.read(u32(frame.addresses[1] + 1), 1)
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 255, source, 8, True, True)
        if bool(frame.status_word & 4):
            break
        frame = frame.with_address(1, frame.addresses[1] + 2)
        frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 1, 16, False, False)
        frame = frame.with_data(2, result, 16)
        continue
    frame = _command_load_fields(memory, frame, 0, frame.data[2] & 65535, 16)
    frame = _command_shift_fields(memory, frame, 0, 1, 16, False)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, frame.data[2] & 65535, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = frame.with_address(0, 871727)
    value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 1)
    frame = _command_store_fields(memory, frame, 4294963123, value, 8)
    value = memory.state.read(u32(frame.addresses[0] + 1 + s16(frame.data[0] & 65535)), 1)
    frame = _command_store_fields(memory, frame, 4294963125, value, 8)
    value = memory.state.read(u32(frame.addresses[0] + 2 + s16(frame.data[0] & 65535)), 1)
    frame = _command_store_fields(memory, frame, 4294963127, value, 8)
    tested = memory.state.read(4294964132, 1)
    frame = _command_bit_fields(memory, frame, tested, 0 % 8)
    if not not frame.status_word & 4:
        value = memory.state.read(4294963122, 2)
        frame = _command_load_fields(memory, frame, 0, value, 16)
        frame = _command_call_fields(memory, frame, 73722, 73692)
        frame = _command_store_fields(memory, frame, 4294963044, frame.data[1] & 65535, 16)
        value = memory.state.read(4294963124, 2)
        frame = _command_load_fields(memory, frame, 0, value, 16)
        frame = _command_call_fields(memory, frame, 73722, 73704)
        frame = _command_store_fields(memory, frame, 4294963046, frame.data[1] & 65535, 16)
        value = memory.state.read(4294963126, 2)
        frame = _command_load_fields(memory, frame, 0, value, 16)
        frame = _command_call_fields(memory, frame, 73722, 73716)
        frame = _command_store_fields(memory, frame, 4294963048, frame.data[1] & 65535, 16)
    return frame

def find_first_set_mask_bit_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """11FFA..12008: find first set mask bit."""
    frame = memory.enter(frame)
    frame = _command_load_fields(memory, frame, 1, 0, 16)
    while True:
        frame = _command_bit_fields(memory, frame, frame.data[0], frame.data[1] % 32)
        if not frame.status_word & 4:
            break
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)
        frame = frame.with_data(1, result, 16)
        continue
    return frame

def prepare_command_amount_modal_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12008..12024: prepare command amount modal."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_call_fields(memory, frame, 73764, 73748)
    frame = _command_call_fields(memory, frame, 73828, 73754)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 120, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_amount_modal_frame_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12024..12064: append amount modal frame."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 13, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 13, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 49716, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49332, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 54144, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 10, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 54145, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 56192, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(30))
    return frame

def append_amount_modal_descriptor_limit_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12064..12102: append amount modal descriptor limit."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 13, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 13, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 49588, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49460, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49233, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 49234, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 2), 49235, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 32), 49236, 16)
    frame = frame.with_address(0, frame.addresses[0] + 4)
    frame = _command_load_fields(memory, frame, 0, 2, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 49153, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    value = memory.state.read(16726060, 4)
    frame = frame.with_address(1, value)
    value = memory.state.read(u32(frame.addresses[1] + 5), 1)
    frame = _command_load_fields(memory, frame, 0, value, 8)
    frame = _command_shift_fields(memory, frame, 0, 8, 16, False)
    value = memory.state.read(u32(frame.addresses[1] + 6), 1)
    frame = _command_load_fields(memory, frame, 0, value, 8)
    frame = _command_shift_fields(memory, frame, 0, 8, 32, False)
    value = memory.state.read(u32(frame.addresses[1] + 7), 1)
    frame = _command_load_fields(memory, frame, 0, value, 8)
    frame = _command_shift_fields(memory, frame, 0, 8, 32, False)
    value = memory.state.read(u32(frame.addresses[1] + 8), 1)
    frame = _command_load_fields(memory, frame, 0, value, 8)
    frame = _command_store_fields(memory, frame, 4294964216, frame.data[0], 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 49153, 16)
    frame = frame.with_address(6, 4294955776)
    frame = _command_call_fields(memory, frame, 75530, 73950)
    frame = frame.with_address(1, 4294955776)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    while True:
        value = memory.state.read(u32(frame.addresses[1]), 2)
        frame = frame.with_address(1, frame.addresses[1] + 2)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), value, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 0, 16, True)
    return frame

def append_selected_command_row_label_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """1221C..12248: append selected command row label."""
    frame = memory.enter(frame)
    tested = memory.state.read(4294964001, 1)
    frame = _command_bit_fields(memory, frame, tested, 3 % 8)
    if not not frame.status_word & 4:
        frame = frame.with_address(0, u32(74278 + 34))
        value = memory.state.read(4294964208, 2)
        frame = _command_load_fields(memory, frame, 0, value, 16)
        frame = _command_shift_fields(memory, frame, 0, 1, 16, False)
        source = memory.state.read(4294964208, 2)
        frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, False, False)
        frame = frame.with_data(0, result, 16)
        frame = _command_shift_fields(memory, frame, 0, 3, 16, False)
        frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 56, 16, False, False)
        frame = frame.with_data(0, result, 16)
        frame = _command_load_fields(memory, frame, 1, 200, 16)
        frame = _command_load_fields(memory, frame, 2, 0, 16)
        frame = _command_call_fields(memory, frame, 44040, 74310)
    return frame

def clear_command_amount_page_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12292..12314: clear command amount page."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 90), 13, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 13, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 13, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 13, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 90), 49716, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 49588, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 49460, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49332, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 12, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 90), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 60), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 30), 32768, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 32768, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = frame.with_address(0, frame.addresses[0] + s16(90))
    frame = _command_load_fields(memory, frame, 0, 9, 16)
    frame = _command_load_fields(memory, frame, 1, 50098, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 14, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 128, 16, False, False)
        frame = frame.with_data(1, result, 16)
        frame = _command_load_fields(memory, frame, 2, 13, 16)
        while True:
            frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 32768, 16)
            frame = frame.with_address(0, frame.addresses[0] + 2)
            frame, repeat = _command_dbra_fields(frame, 2)
            if repeat:
                continue
            break
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 440, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def prepare_budget_amount_page_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12314..12418: prepare budget amount page."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 11, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50610, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 8, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 11, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 11, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 50866, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50738, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 8, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 49153, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(26))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 11, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 11, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 51122, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50994, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49233, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 49234, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 2), 49235, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 49236, 16)
    frame = frame.with_address(0, frame.addresses[0] + 4)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 49153, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    value = memory.state.read(4294964212, 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 49153, 16)
    frame = frame.with_address(6, 4294955776)
    frame = _command_call_fields(memory, frame, 75530, 74700)
    frame = frame.with_address(1, 4294955776)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    while True:
        value = memory.state.read(u32(frame.addresses[1]), 2)
        frame = frame.with_address(1, frame.addresses[1] + 2)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), value, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 26), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(26))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 11, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 51250, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 8, 16)
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
    frame, result = _command_binary_fields(memory, frame, destination, 156, 16, False, False)
    memory.state.write(4294963994, 2, result)
    frame = _command_call_fields(memory, frame, 73736, 74774)
    return frame

def step_budget_amount_controls_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12418..124FC: step budget amount controls."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964738, 1)
    frame = _command_load_fields(memory, frame, 0, value, 8)
    result = frame.data[0] & 65535 & 12
    frame = _command_load_fields(memory, frame, 0, result, 16)
    if bool(frame.status_word & 4):
        value = memory.state.read(4294964738, 1)
        frame = _command_load_fields(memory, frame, 0, value, 8)
        result = frame.data[0] & 65535 & 3
        frame = _command_load_fields(memory, frame, 0, result, 16)
        if bool(frame.status_word & 4):
            frame = _command_store_fields(memory, frame, 4294964744, 1, 16)
            frame = _command_call_fields(memory, frame, 75052, 75002)
        else:
            destination = memory.state.read(4294964744, 2)
            frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
            memory.state.write(4294964744, 2, result)
            if not not frame.status_word & 4:
                frame = _command_store_fields(memory, frame, 4294964744, 12, 16)
                frame = _command_bit_fields(memory, frame, frame.data[0], 1 % 32)
                if not frame.status_word & 4:
                    frame = _command_load_fields(memory, frame, 0, 5, 16)
                    source = memory.state.read(4294964122, 2)
                    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, True, False)
                    frame = frame.with_data(0, result, 16)
                    frame = _command_shift_fields(memory, frame, 0, 2, 16, False)
                    frame = frame.with_address(0, u32(74954 + 50))
                    value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)
                    frame = _command_load_fields(memory, frame, 1, value, 32)
                    value = memory.state.read(4294964212, 4)
                    frame = _command_load_fields(memory, frame, 2, value, 32)
                    frame, result = _command_binary_fields(memory, frame, frame.data[2], frame.data[1], 32, True, False)
                    frame = frame.with_data(2, result, 32)
                    if not bool(frame.status_word & 1):
                        frame = _command_store_fields(memory, frame, 4294964212, frame.data[2], 32)
                        frame = frame.with_address(0, u32(74976 + 52))
                        value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)
                        frame = _command_load_fields(memory, frame, 1, value, 32)
                        destination = memory.state.read(4294964154, 4)
                        frame, result = _command_binary_fields(memory, frame, destination, frame.data[1], 32, True, False)
                        memory.state.write(4294964154, 4, result)
                        frame = _command_call_fields(memory, frame, 75052, 75002)
                else:
                    frame = _command_load_fields(memory, frame, 0, 5, 16)
                    source = memory.state.read(4294964122, 2)
                    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, True, False)
                    frame = frame.with_data(0, result, 16)
                    frame = _command_shift_fields(memory, frame, 0, 2, 16, False)
                    frame = frame.with_address(0, u32(74906 + 98))
                    value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)
                    frame = _command_load_fields(memory, frame, 1, value, 32)
                    source = memory.state.read(4294964212, 4)
                    frame, result = _command_binary_fields(memory, frame, frame.data[1], source, 32, False, False)
                    frame = frame.with_data(1, result, 32)
                    source = memory.state.read(4294964216, 4)
                    frame, result = _command_binary_fields(memory, frame, frame.data[1], source, 32, True, True)
                    if not not frame.status_word & 5:
                        frame = _command_store_fields(memory, frame, 4294964212, frame.data[1], 32)
                        frame = frame.with_address(0, u32(74930 + 98))
                        value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 4)
                        frame = _command_load_fields(memory, frame, 1, value, 32)
                        destination = memory.state.read(4294964154, 4)
                        frame, result = _command_binary_fields(memory, frame, destination, frame.data[1], 32, False, False)
                        memory.state.write(4294964154, 4, result)
                        frame = _command_call_fields(memory, frame, 75052, 75002)
    else:
        destination = memory.state.read(4294964744, 2)
        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
        memory.state.write(4294964744, 2, result)
        if not not frame.status_word & 4:
            frame = _command_store_fields(memory, frame, 4294964744, 12, 16)
            frame = _command_bit_fields(memory, frame, frame.data[0], 3 % 32)
            if not frame.status_word & 4:
                value = memory.state.read(4294964122, 2)
                frame = _command_load_fields(memory, frame, 1, value, 16)
                frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)
                frame = frame.with_data(1, result, 16)
                frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 5, 16, True, True)
                if not not frame.status_word & 5:
                    frame = _command_store_fields(memory, frame, 4294964122, frame.data[1] & 65535, 16)
                    frame = _command_call_fields(memory, frame, 75052, 75002)
            else:
                frame = _command_load_fields(memory, frame, 1, 5, 16)
                source = memory.state.read(4294964122, 2)
                frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, source, 16, True, False)
                frame = frame.with_data(1, result, 16)
                frame = _command_shift_fields(memory, frame, 1, 2, 16, False)
                frame = frame.with_address(0, u32(74818 + 190))
                value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[1] & 65535)), 4)
                frame = _command_load_fields(memory, frame, 2, value, 32)
                source = memory.state.read(4294964216, 4)
                frame, result = _command_binary_fields(memory, frame, frame.data[2], source, 32, True, True)
                if not not frame.status_word & 5:
                    destination = memory.state.read(4294964122, 2)
                    frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
                    memory.state.write(4294964122, 2, result)
                    frame = _command_call_fields(memory, frame, 75052, 75002)
    return frame

def append_budget_cost_and_amount_values_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """1252C..125AC: append budget cost and amount values."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    value = memory.state.read(4294964154, 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 49153, 16)
    frame = frame.with_address(6, 4294962944)
    frame = _command_call_fields(memory, frame, 75530, 75082)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50874, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(1, 4294962944)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    frame = _command_load_fields(memory, frame, 1, 0, 16)
    while True:
        value = memory.state.read(u32(frame.addresses[1]), 2)
        frame = frame.with_address(1, frame.addresses[1] + 2)
        frame = _command_load_fields(memory, frame, 2, value, 16)
        frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 49153, 16, True, True)
        if not not frame.status_word & 4:
            source = memory.state.read(4294964122, 2)
            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, source, 16, True, True)
            if not bool(frame.status_word & 1):
                frame = _command_load_fields(memory, frame, 2, 50054, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[2] & 65535, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)
        frame = frame.with_data(1, result, 16)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    value = memory.state.read(4294964212, 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 49153, 16)
    frame = frame.with_address(6, 4294962944)
    frame = _command_call_fields(memory, frame, 75530, 75148)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 51130, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(1, 4294962944)
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
    frame, result = _command_binary_fields(memory, frame, destination, 32, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_budget_place_highlight_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """125AC..125D0: append budget place highlight."""
    frame = memory.enter(frame)
    tested = memory.state.read(4294964001, 1)
    frame = _command_bit_fields(memory, frame, tested, 4 % 8)
    if not not frame.status_word & 4:
        frame = frame.with_address(0, u32(75190 + 26))
        frame = _command_load_fields(memory, frame, 0, 104, 16)
        value = memory.state.read(4294964122, 2)
        frame = _command_load_fields(memory, frame, 1, value, 16)
        frame = _command_shift_fields(memory, frame, 1, 3, 16, False)
        frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 232, 16, False, False)
        frame = frame.with_data(1, result, 16)
        frame = _command_load_fields(memory, frame, 2, 0, 16)
        frame = _command_call_fields(memory, frame, 44040, 75214)
    return frame

def append_budget_header_row_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12602..12620: append budget header row."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50210, 16)
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
    return frame

def append_budget_first_detail_rows_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12620..1268C: append budget first detail rows."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50466, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50338, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49297, 16)
    frame = _command_call_fields(memory, frame, 75504, 75334)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 4, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = _command_call_fields(memory, frame, 75504, 75340)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 49153, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 49153, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(20))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50594, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
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

def append_budget_second_detail_row_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """1268C..126D2: append budget second detail row."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 8, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50850, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50722, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49297, 16)
    frame = _command_call_fields(memory, frame, 75504, 75442)
    frame = _command_load_fields(memory, frame, 0, 49305, 16)
    frame = _command_call_fields(memory, frame, 75504, 75450)
    frame = _command_load_fields(memory, frame, 0, 49297, 16)
    frame = _command_call_fields(memory, frame, 75504, 75458)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(20))
    return frame

def append_budget_footer_row_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """126D2..126F0: append budget footer row."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 8, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50978, 16)
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
    return frame

def append_four_budget_numbered_tiles_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """126F0..1270A: append four budget numbered tiles."""
    frame = memory.enter(frame)
    frame = _command_load_fields(memory, frame, 1, frame.data[0] & 65535, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)
    frame = frame.with_data(1, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), frame.data[1] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)
    frame = frame.with_data(1, result, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 1, 16, False, False)
    frame = frame.with_data(1, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), frame.data[1] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    return frame

def append_six_place_decimal_value_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """1270A..12760: append six place decimal value."""
    frame = memory.enter(frame)
    return _command_decimal_transaction_fields(memory, frame)

def append_decimal_value_place_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12760..12782: append decimal value place."""
    frame = memory.enter(frame)
    return _command_decimal_place_fields(memory, frame)

def prepare_command_amount_limit_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """1278C..12840: prepare command amount limit."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 9, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 9, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 9, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 50364, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 50236, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50108, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 54144, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 6, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 54145, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 49153, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 20), 50054, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 56192, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 66, 16, False, False)
    memory.state.write(4294963994, 2, result)
    value = memory.state.read(4294964068, 2)
    frame = _command_load_fields(memory, frame, 0, value, 16)
    frame = _command_shift_fields(memory, frame, 0, 2, 16, False)
    frame = frame.with_address(1, 4294959100)
    value = memory.state.read(u32(frame.addresses[1] + s16(frame.data[0] & 65535)), 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_store_fields(memory, frame, 4294964216, frame.data[0], 32)
    frame = frame.with_address(0, u32(75792 + 48))
    frame = _command_call_fields(memory, frame, 75896, 75800)
    value = memory.state.read(4294964216, 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 0, 16)
    frame = frame.with_address(6, 4294962944)
    frame = _command_call_fields(memory, frame, 75530, 75820)
    frame = _command_store_fields(memory, frame, 4294964744, 1, 16)
    destination = memory.state.read(4294964132, 2)
    result = destination | 32832
    frame = _command_store_fields(memory, frame, 4294964132, result, 16)
    destination = memory.state.read(4294964132, 2)
    result = destination & 63999
    frame = _command_store_fields(memory, frame, 4294964132, result, 16)
    return frame

def limit_live_command_amount_by_price_record_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12878..128E2: limit live command amount by price record."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964108, 2)
    frame = _command_load_fields(memory, frame, 7, value, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[7] & 65535, 147, 16, True, True)
    if bool(frame.status_word & 4):
        frame = frame.with_address(7, frame.addresses[7] - 4)
        frame = _command_store_fields(memory, frame, frame.addresses[7], frame.data[6], 32)
        frame = frame.with_address(1, 4294964480)
        frame = _command_load_fields(memory, frame, 7, 0, 16)
        while True:
            value = memory.state.read(u32(frame.addresses[1]), 2)
            frame = frame.with_address(1, frame.addresses[1] + 2)
            frame = _command_load_fields(memory, frame, 6, value, 16)
            if bool(frame.status_word & 8):
                break
            frame = _command_bit_fields(memory, frame, frame.data[6], 14 % 32)
            if bool(frame.status_word & 4):
                continue
            frame, result = _command_binary_fields(memory, frame, frame.data[7] & 65535, 1, 16, False, False)
            frame = frame.with_data(7, result, 16)
            continue
        frame = _command_product_fields(memory, frame, 7, 25000)
        source = memory.state.read(4294964216, 4)
        frame, result = _command_binary_fields(memory, frame, frame.data[7], source, 32, True, True)
        if not not frame.status_word & 1:
            frame = _command_store_fields(memory, frame, 4294964216, frame.data[7], 32)
        frame = _command_store_fields(memory, frame, 4294964122, 5, 16)
        frame = _command_store_fields(memory, frame, 4294964220, 5, 16)
        value = memory.state.read(u32(frame.addresses[7]), 4)
        frame = frame.with_address(7, frame.addresses[7] + 4)
        frame = _command_load_fields(memory, frame, 6, value, 32)
    else:
        while True:
            source = memory.state.read(u32(frame.addresses[0]), 2)
            frame, result = _command_binary_fields(memory, frame, frame.data[7] & 65535, source, 16, True, True)
            if bool(frame.status_word & 4):
                break
            frame = frame.with_address(0, frame.addresses[0] + 8)
            continue
        value = memory.state.read(u32(frame.addresses[0] + 2), 4)
        frame = _command_load_fields(memory, frame, 7, value, 32)
        source = memory.state.read(4294964216, 4)
        frame, result = _command_binary_fields(memory, frame, frame.data[7], source, 32, True, True)
        if not not frame.status_word & 1:
            frame = _command_store_fields(memory, frame, 4294964216, frame.data[7], 32)
        value = memory.state.read(u32(frame.addresses[0] + 6), 2)
        frame = _command_load_fields(memory, frame, 7, value, 16)
        frame = _command_store_fields(memory, frame, 4294964122, frame.data[7] & 65535, 16)
        frame = _command_store_fields(memory, frame, 4294964220, frame.data[7] & 65535, 16)
    return frame

def update_player_command_amount_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """128E2..1292C: update player command amount."""
    frame = memory.enter(frame)
    frame = _command_call_fields(memory, frame, 76076, 76006)
    frame = _command_call_fields(memory, frame, 76160, 76010)
    frame = _command_call_fields(memory, frame, 76366, 76014)
    tested = memory.state.read(4294964739, 1)
    frame = _command_bit_fields(memory, frame, tested, 5 % 8)
    if bool(frame.status_word & 4):
        tested = memory.state.read(4294964739, 1)
        frame = _command_bit_fields(memory, frame, tested, 4 % 8)
        if not bool(frame.status_word & 4):
            frame = _command_store_fields(memory, frame, 4294964754, 520, 16)
            frame = _command_store_fields(memory, frame, 4294964066, 2, 16)
            frame = _command_store_fields(memory, frame, 4294964074, 18, 16)
    else:
        value = memory.state.read(4294964212, 4)
        frame = _command_store_fields(memory, frame, 4294964126, value, 32)
        value = memory.state.read(4294964212, 4)
        frame = _command_test_fields(memory, frame, value, 32)
        if not bool(frame.status_word & 4):
            frame = _command_store_fields(memory, frame, 4294964754, 520, 16)
            frame = _command_store_fields(memory, frame, 4294964066, 4, 16)
    return frame

def append_selected_command_amount_frame_fields(memory: CommandMenuMemory, frame: CommandFrame, entry: int=0x1292C) -> CommandFrame:
    """1292C whole; 1293C shares digits/RTS without executing the header prefix."""
    if type(entry) is not int or entry not in (0x1292C, 0x1293C):
        raise ValueError('only actual selected-amount entry or middle entry required')
    frame = memory.enter(frame)
    if entry == 0x1292C:
        frame = frame.with_address(0, 4294955264)
        value = memory.state.read(4294963994, 2)
        frame = frame.with_address(0, frame.addresses[0] + s16(value))
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 6, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50240, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
    value = memory.state.read(4294964212, 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 0, 16)
    frame = frame.with_address(6, 4294962956)
    frame = _command_call_fields(memory, frame, 75530, 76112)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    frame = frame.with_address(1, 4294962956)
    frame = _command_load_fields(memory, frame, 2, 0, 16)
    while True:
        value = memory.state.read(u32(frame.addresses[1]), 2)
        frame = frame.with_address(1, frame.addresses[1] + 2)
        frame = _command_load_fields(memory, frame, 1, value, 16)
        if not not frame.status_word & 4:
            source = memory.state.read(4294964122, 2)
            frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, source, 16, True, True)
            if bool(frame.status_word & 1):
                frame = _command_load_fields(memory, frame, 1, 49153, 16)
            else:
                frame = _command_load_fields(memory, frame, 1, 50054, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, result = _command_binary_fields(memory, frame, frame.data[2] & 65535, 1, 16, False, False)
        frame = frame.with_data(2, result, 16)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 16, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def step_live_command_amount_controls_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12980..129DE: step live command amount controls."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964738, 1)
    frame = _command_load_fields(memory, frame, 0, value, 8)
    result = frame.data[0] & 65535 & 12
    frame = _command_load_fields(memory, frame, 0, result, 16)
    if bool(frame.status_word & 4):
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
                    frame = _command_call_fields(memory, frame, 76334, 76244)
                else:
                    frame = _command_call_fields(memory, frame, 76300, 76238)
    else:
        destination = memory.state.read(4294964744, 2)
        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
        memory.state.write(4294964744, 2, result)
        if not not frame.status_word & 4:
            frame = _command_store_fields(memory, frame, 4294964744, 12, 16)
            frame = _command_bit_fields(memory, frame, frame.data[0], 3 % 32)
            if not frame.status_word & 4:
                frame = _command_call_fields(memory, frame, 76280, 76202)
            else:
                frame = _command_call_fields(memory, frame, 76254, 76196)
    return frame

def select_previous_amount_place_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """129DE..129F8: select previous amount place."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964122, 2)
    frame = _command_load_fields(memory, frame, 0, value, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, True, False)
    frame = frame.with_data(0, result, 16)
    if not bool(frame.status_word & 1):
        frame = _command_shift_fields(memory, frame, 0, 1, 16, False)
        frame = frame.with_address(0, 4294962944)
        value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[0] & 65535)), 2)
        frame = _command_test_fields(memory, frame, value, 16)
        if not bool(frame.status_word & 4):
            destination = memory.state.read(4294964122, 2)
            frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
            memory.state.write(4294964122, 2, result)
    return frame

def select_next_amount_place_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """129F8..12A0C: select next amount place."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964122, 2)
    frame = _command_load_fields(memory, frame, 0, value, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    source = memory.state.read(4294964220, 2)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, source, 16, True, True)
    if not not frame.status_word & 5:
        destination = memory.state.read(4294964122, 2)
        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, False, False)
        memory.state.write(4294964122, 2, result)
    return frame

def add_selected_cost_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12A0C..12A2E: add this decimal place without exceeding the live limit.

    The real D1 WORD shift selects a signed indexed LONG at1344C. ADD.L
    wraps before CMP.L; CMP retains that ADD's X. The rejected branch keeps
    CMP's NZVC, while the accepted MOVE.L clears V/C and retains the same X.
    The actual parent owns its CALL/RTS slot; this leaf does not touch A7.
    """
    frame = memory.enter(frame)
    value = memory.state.read(0xFFFFF39A, 2)
    frame = _command_load_fields(memory, frame, 1, value, 16)
    frame = _command_shift_fields(memory, frame, 1, 2, 16)
    frame = frame.with_address(0, 0x1344C)
    value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[1] & 65535)), 4)
    frame = _command_load_fields(memory, frame, 1, value, 32)
    source = memory.state.read(0xFFFFF3F4, 4)
    frame, result = _command_binary_fields(memory, frame, frame.data[1], source, 32)
    frame = frame.with_data(1, result, 32)
    source = memory.state.read(0xFFFFF3F8, 4)
    frame, ignored = _command_binary_fields(memory, frame, frame.data[1], source, 32, True, True)
    if not frame.status_word & 5:
        return frame
    return _command_store_fields(memory, frame, 0xFFFFF3F4, frame.data[1], 32)


def decrement_live_command_amount_small_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12A2E..12A4E: decrement live command amount small."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964122, 2)
    frame = _command_load_fields(memory, frame, 1, value, 16)
    frame = _command_shift_fields(memory, frame, 1, 2, 16, False)
    frame = frame.with_address(0, u32(76342 + 2582))
    value = memory.state.read(u32(frame.addresses[0] + s16(frame.data[1] & 65535)), 4)
    frame = _command_load_fields(memory, frame, 1, value, 32)
    value = memory.state.read(4294964212, 4)
    frame = _command_load_fields(memory, frame, 2, value, 32)
    frame, result = _command_binary_fields(memory, frame, frame.data[2], frame.data[1], 32, True, False)
    frame = frame.with_data(2, result, 32)
    if not bool(frame.status_word & 1):
        frame = _command_store_fields(memory, frame, 4294964212, frame.data[2], 32)
    return frame

def append_blinking_amount_place_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12A4E..12A90: append blinking amount place."""
    frame = memory.enter(frame)
    destination = memory.state.read(4294964124, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 24, 16, True, True)
    if not bool(frame.status_word & 1):
        frame = _command_store_fields(memory, frame, 4294964124, 24, 16)
    value = memory.state.read(4294964738, 2)
    frame = _command_load_fields(memory, frame, 0, value, 16)
    result = frame.data[0] & 65535 & 48
    frame = _command_load_fields(memory, frame, 0, result, 16)
    if not not frame.status_word & 4:
        destination = memory.state.read(4294964124, 2)
        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
        memory.state.write(4294964124, 2, result)
        destination = memory.state.read(4294964124, 2)
        frame, result = _command_binary_fields(memory, frame, destination, 12, 16, True, True)
        if not bool(frame.status_word & 1):
            frame = frame.with_address(0, u32(76406 + 26))
            frame = _command_load_fields(memory, frame, 0, 64, 16)
            value = memory.state.read(4294964122, 2)
            frame = _command_load_fields(memory, frame, 1, value, 16)
            frame = _command_shift_fields(memory, frame, 1, 3, 16, False)
            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 256, 16, False, False)
            frame = frame.with_data(1, result, 16)
            frame = _command_load_fields(memory, frame, 2, 0, 16)
            frame = _command_call_fields(memory, frame, 44040, 76430)
    return frame

def prepare_percentage_panel_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12A98..12AB6: prepare percentage panel."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_call_fields(memory, frame, 76470, 76452)
    frame = _command_call_fields(memory, frame, 76500, 76456)
    frame = _command_call_fields(memory, frame, 76620, 76460)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 88, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_percentage_header_row_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12AB6..12AD4: append percentage header row."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 9, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50332, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 6, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    return frame

def append_percentage_value_rows_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12AD4..12B4C: append percentage value rows."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 9, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 9, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 50588, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50460, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49193, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49201, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 2, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 49153, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(22))
    return frame

def append_percentage_footer_row_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12B4C..12B6A: append percentage footer row."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 9, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50716, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 6, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    return frame

def clear_percentage_panel_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12B6A..12BC0: clear percentage panel."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 66), 9, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 9, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 9, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 9, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 66), 50716, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 50588, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 50460, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50332, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 8, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 66), 0, 16, True)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 44), 0, 16, True)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 22), 0, 16, True)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 66), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 88, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def append_percentage_value_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12BC0..12C0C: append percentage value."""
    frame = memory.enter(frame)
    frame = frame.with_address(6, 4294962944)
    frame = _command_load_fields(memory, frame, 0, 0, 32)
    value = memory.state.read(4294964150, 2)
    frame = _command_load_fields(memory, frame, 0, value, 16)
    frame = _command_load_fields(memory, frame, 1, 50054, 16)
    frame = _command_load_fields(memory, frame, 2, 49153, 16)
    frame = _command_call_fields(memory, frame, 75530, 76760)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 2, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50600, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    value = memory.state.read(4294962952, 2)
    frame = _command_load_fields(memory, frame, 0, value, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 49153, 16, True, True)
    if not not frame.status_word & 4:
        value = memory.state.read(4294964152, 2)
        frame = _command_test_fields(memory, frame, value, 16)
        if not not frame.status_word & 4:
            frame = _command_load_fields(memory, frame, 0, 50054, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    value = memory.state.read(4294962954, 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), value, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 0, 16, True)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 8, 16, False, False)
    memory.state.write(4294963994, 2, result)
    return frame

def step_percentage_controls_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12C0C..12C84: step percentage controls."""
    frame = memory.enter(frame)
    value = memory.state.read(4294964738, 1)
    frame = _command_load_fields(memory, frame, 0, value, 8)
    result = frame.data[0] & 255 & 12
    frame = _command_load_fields(memory, frame, 0, result, 8)
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
                frame = _command_load_fields(memory, frame, 1, 1, 16)
                value = memory.state.read(4294964152, 2)
                frame = _command_test_fields(memory, frame, value, 16)
                if not not frame.status_word & 4:
                    frame = _command_load_fields(memory, frame, 1, 10, 16)
                tested = memory.state.read(4294964738, 1)
                frame = _command_bit_fields(memory, frame, tested, 1 % 8)
                if not frame.status_word & 4:
                    destination = memory.state.read(4294964150, 2)
                    frame, result = _command_binary_fields(memory, frame, destination, frame.data[1] & 65535, 16, True, False)
                    memory.state.write(4294964150, 2, result)
                    if not not frame.status_word & 8:
                        destination = memory.state.read(4294964150, 2)
                        frame, result = _command_binary_fields(memory, frame, destination, frame.data[1] & 65535, 16, False, False)
                        memory.state.write(4294964150, 2, result)
                else:
                    destination = memory.state.read(4294964150, 2)
                    frame, result = _command_binary_fields(memory, frame, destination, frame.data[1] & 65535, 16, False, False)
                    memory.state.write(4294964150, 2, result)
                    destination = memory.state.read(4294964150, 2)
                    frame, result = _command_binary_fields(memory, frame, destination, 99, 16, True, True)
                    if not bool(frame.status_word & 5):
                        destination = memory.state.read(4294964150, 2)
                        frame, result = _command_binary_fields(memory, frame, destination, frame.data[1] & 65535, 16, True, False)
                        memory.state.write(4294964150, 2, result)
    else:
        destination = memory.state.read(4294964744, 2)
        frame, result = _command_binary_fields(memory, frame, destination, 1, 16, True, False)
        memory.state.write(4294964744, 2, result)
        if not not frame.status_word & 4:
            frame = _command_bit_fields(memory, frame, frame.data[0], 3 % 32)
            if not frame.status_word & 4:
                frame = _command_store_fields(memory, frame, 4294964152, 1, 16)
            else:
                frame = _command_store_fields(memory, frame, 4294964152, 0, 16, True)
    return frame

def append_percentage_place_highlight_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12C84..12CB6: append percentage place highlight."""
    frame = memory.enter(frame)
    tested = memory.state.read(4294964739, 1)
    frame = _command_bit_fields(memory, frame, tested, 5 % 8)
    if not not frame.status_word & 4:
        tested = memory.state.read(4294964001, 1)
        frame = _command_bit_fields(memory, frame, tested, 3 % 8)
        if not not frame.status_word & 4:
            frame = frame.with_address(0, u32(76952 + 30))
            frame = _command_load_fields(memory, frame, 0, 88, 16)
            frame = _command_load_fields(memory, frame, 1, 160, 16)
            value = memory.state.read(4294964152, 2)
            frame = _command_test_fields(memory, frame, value, 16)
            if not bool(frame.status_word & 4):
                frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 8, 16, False, False)
                frame = frame.with_data(1, result, 16)
            frame = _command_load_fields(memory, frame, 2, 0, 16)
            frame = _command_call_fields(memory, frame, 44040, 76980)
    return frame

def prepare_resource_amount_panel_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12CBE..12CF4: prepare resource amount panel."""
    frame = memory.enter(frame)
    frame = frame.with_address(0, 4294955264)
    value = memory.state.read(4294963994, 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(value))
    frame = _command_call_fields(memory, frame, 77044, 77002)
    frame = _command_call_fields(memory, frame, 77308, 77006)
    destination = memory.state.read(4294963994, 2)
    frame, result = _command_binary_fields(memory, frame, destination, 364, 16, False, False)
    memory.state.write(4294963994, 2, result)
    frame = _command_store_fields(memory, frame, 4294964122, 5, 16)
    frame = _command_store_fields(memory, frame, 4294964744, 1, 16)
    frame = _command_store_fields(memory, frame, 4294964744, 1, 16)
    destination = memory.state.read(4294964132, 2)
    result = destination | 32832
    frame = _command_store_fields(memory, frame, 4294964132, result, 16)
    destination = memory.state.read(4294964132, 2)
    result = destination & 63999
    frame = _command_store_fields(memory, frame, 4294964132, result, 16)
    return frame

def append_city_resource_amount_rows_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12CF4..12D82: append city resource amount rows."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49332, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 9, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    value = memory.state.read(4294964068, 2)
    frame = _command_load_fields(memory, frame, 0, value, 16)
    frame = _command_shift_fields(memory, frame, 0, 2, 16, False)
    frame = frame.with_address(1, 4294959100)
    value = memory.state.read(u32(frame.addresses[1] + s16(frame.data[0] & 65535)), 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_load_fields(memory, frame, 2, 0, 16)
    frame = frame.with_address(6, 4294962968)
    frame = _command_call_fields(memory, frame, 75530, 77102)
    frame = _command_load_fields(memory, frame, 0, 49229, 16)
    frame = _command_load_fields(memory, frame, 1, 49588, 16)
    frame = _command_call_fields(memory, frame, 77186, 77114)
    value = memory.state.read(4294964068, 2)
    frame = _command_load_fields(memory, frame, 0, value, 16)
    frame = _command_shift_fields(memory, frame, 0, 2, 16, False)
    frame = frame.with_address(1, 4294959260)
    value = memory.state.read(u32(frame.addresses[1] + s16(frame.data[0] & 65535)), 4)
    frame = _command_load_fields(memory, frame, 0, value, 32)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_load_fields(memory, frame, 2, 0, 16)
    frame = frame.with_address(6, 4294962968)
    frame = _command_call_fields(memory, frame, 75530, 77144)
    frame = _command_load_fields(memory, frame, 0, 49233, 16)
    frame = _command_load_fields(memory, frame, 1, 49844, 16)
    frame = _command_call_fields(memory, frame, 77186, 77156)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49972, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 9, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54145, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 56192, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    return frame

def append_live_resource_value_row_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12D82..12DFC: append live resource value row."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 12, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[1] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 128, 16, True, False)
    frame = frame.with_data(1, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[0] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 49153, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 49153, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 5, 16)
    frame = frame.with_address(1, 4294962968)
    while True:
        value = memory.state.read(u32(frame.addresses[1]), 2)
        frame = frame.with_address(1, frame.addresses[1] + 2)
        frame = _command_load_fields(memory, frame, 1, value, 16)
        if bool(frame.status_word & 4):
            frame = _command_load_fields(memory, frame, 1, 49153, 16)
        else:
            frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 50053, 16, False, False)
            frame = frame.with_data(1, result, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[1] & 65535, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(28))
    return frame

def append_committed_resource_amount_rows_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12DFC..12E74: append committed resource amount rows."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50228, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50048, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 9, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50049, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52096, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49229, 16)
    frame = _command_load_fields(memory, frame, 1, 50484, 16)
    value = memory.state.read(4294964126, 4)
    frame = _command_load_fields(memory, frame, 2, value, 32)
    frame = _command_call_fields(memory, frame, 77428, 77352)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50612, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 9, 16)
    while True:
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 49233, 16)
    frame = _command_load_fields(memory, frame, 1, 50868, 16)
    value = memory.state.read(4294964154, 4)
    frame = _command_load_fields(memory, frame, 2, value, 32)
    frame = _command_call_fields(memory, frame, 77428, 77396)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50996, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 54144, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, 9, 16)
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
    return frame

def append_committed_resource_value_row_frame_fields(memory: CommandMenuMemory, frame: CommandFrame) -> CommandFrame:
    """12E74..12EF2: append committed resource value row."""
    frame = memory.enter(frame)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 12, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 12, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[1] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[1] & 65535, 128, 16, True, False)
    frame = frame.with_data(1, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[1] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 50050, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 50050, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), frame.data[0] & 65535, 16)
    frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 1, 16, False, False)
    frame = frame.with_data(0, result, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[0] & 65535, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = _command_load_fields(memory, frame, 0, frame.data[2] & 65535, 16)
    frame = _command_load_fields(memory, frame, 1, 1, 16)
    frame = _command_load_fields(memory, frame, 2, 0, 16)
    frame = frame.with_address(6, 4294962968)
    frame = _command_call_fields(memory, frame, 75530, 77498)
    frame = frame.with_address(6, 4294962968)
    frame = _command_load_fields(memory, frame, 0, 7, 16)
    while True:
        frame, result = _command_binary_fields(memory, frame, frame.data[0] & 65535, 5, 16, True, True)
        if not frame.status_word & 5:
            frame = _command_load_fields(memory, frame, 3, 49153, 16)
        else:
            value = memory.state.read(u32(frame.addresses[6]), 2)
            frame = frame.with_address(6, frame.addresses[6] + 2)
            frame = _command_load_fields(memory, frame, 3, value, 16)
            if bool(frame.status_word & 4):
                frame = _command_load_fields(memory, frame, 3, 49153, 16)
            else:
                frame, result = _command_binary_fields(memory, frame, frame.data[3] & 65535, 50053, 16, False, False)
                frame = frame.with_data(3, result, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), frame.data[3] & 65535, 16)
        frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 49153, 16)
        frame = frame.with_address(0, frame.addresses[0] + 2)
        frame, repeat = _command_dbra_fields(frame, 0)
        if repeat:
            continue
        break
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0] + 28), 52098, 16)
    frame = _command_store_fields(memory, frame, u32(frame.addresses[0]), 52098, 16)
    frame = frame.with_address(0, frame.addresses[0] + 2)
    frame = frame.with_address(0, frame.addresses[0] + s16(28))
    return frame

def _budget_known_fields(memory, frame, target):
    if target == 72946:
        return prepare_budget_summary_panel_frame_fields(memory, frame)
    if target == 73258:
        return append_numbered_budget_columns_frame_fields(memory, frame)
    if target == 73276:
        return prepare_compact_budget_summary_panel_frame_fields(memory, frame)
    if target == 73602:
        return select_descriptor_portrait_parts_frame_fields(memory, frame)
    if target == 73722:
        return find_first_set_mask_bit_frame_fields(memory, frame)
    if target == 73736:
        return prepare_command_amount_modal_frame_fields(memory, frame)
    if target == 73764:
        return append_amount_modal_frame_frame_fields(memory, frame)
    if target == 73828:
        return append_amount_modal_descriptor_limit_frame_fields(memory, frame)
    if target == 74268:
        return append_selected_command_row_label_frame_fields(memory, frame)
    if target == 74386:
        return clear_command_amount_page_frame_fields(memory, frame)
    if target == 74516:
        return prepare_budget_amount_page_frame_fields(memory, frame)
    if target == 74776:
        return step_budget_amount_controls_frame_fields(memory, frame)
    if target == 75052:
        return append_budget_cost_and_amount_values_frame_fields(memory, frame)
    if target == 75180:
        return append_budget_place_highlight_frame_fields(memory, frame)
    if target == 75266:
        return append_budget_header_row_frame_fields(memory, frame)
    if target == 75296:
        return append_budget_first_detail_rows_frame_fields(memory, frame)
    if target == 75404:
        return append_budget_second_detail_row_frame_fields(memory, frame)
    if target == 75474:
        return append_budget_footer_row_frame_fields(memory, frame)
    if target == 75504:
        return append_four_budget_numbered_tiles_frame_fields(memory, frame)
    if target == 75530:
        return append_six_place_decimal_value_frame_fields(memory, frame)
    if target == 75616:
        return append_decimal_value_place_frame_fields(memory, frame)
    if target == 75660:
        return prepare_command_amount_limit_frame_fields(memory, frame)
    if target == 75896:
        return limit_live_command_amount_by_price_record_frame_fields(memory, frame)
    if target == 76002:
        return update_player_command_amount_frame_fields(memory, frame)
    if target == 76076:
        return append_selected_command_amount_frame_fields(memory, frame)
    if target == 76092:
        return append_selected_command_amount_frame_fields(memory, frame, 0x1293C)
    if target == 76160:
        return step_live_command_amount_controls_frame_fields(memory, frame)
    if target == 76254:
        return select_previous_amount_place_frame_fields(memory, frame)
    if target == 76280:
        return select_next_amount_place_frame_fields(memory, frame)
    if target == 76300:
        return add_selected_cost_frame_fields(memory, frame)
    if target == 76334:
        return decrement_live_command_amount_small_frame_fields(memory, frame)
    if target == 76366:
        return append_blinking_amount_place_frame_fields(memory, frame)
    if target == 76440:
        return prepare_percentage_panel_frame_fields(memory, frame)
    if target == 76470:
        return append_percentage_header_row_frame_fields(memory, frame)
    if target == 76500:
        return append_percentage_value_rows_frame_fields(memory, frame)
    if target == 76620:
        return append_percentage_footer_row_frame_fields(memory, frame)
    if target == 76650:
        return clear_percentage_panel_frame_fields(memory, frame)
    if target == 76736:
        return append_percentage_value_frame_fields(memory, frame)
    if target == 76812:
        return step_percentage_controls_frame_fields(memory, frame)
    if target == 76932:
        return append_percentage_place_highlight_frame_fields(memory, frame)
    if target == 76990:
        return prepare_resource_amount_panel_frame_fields(memory, frame)
    if target == 77044:
        return append_city_resource_amount_rows_frame_fields(memory, frame)
    if target == 77186:
        return append_live_resource_value_row_frame_fields(memory, frame)
    if target == 77308:
        return append_committed_resource_amount_rows_frame_fields(memory, frame)
    if target == 77428:
        return append_committed_resource_value_row_frame_fields(memory, frame)
    return None
