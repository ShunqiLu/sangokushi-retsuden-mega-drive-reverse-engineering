"""Force eligibility and live city-count selection, independent of rendering."""
from .domain import AiState, Word, descending_inclusive, low8, negative_word, u16


def count_force_cities(state: AiState, selector: Word) -> Word:
    selector = u16(selector)
    assignments = state.force_city_assignments.cursor()
    count = u16(0)
    for remaining in descending_inclusive(39):
        if assignments.next_byte() == low8(selector):
            count = u16(count + 1)
    return count


def select_force_by_city_count(state: AiState) -> tuple[Word, Word]:
    heads = state.force_heads
    row = state.force_rows.cursor()
    row_offset = u16(state.force_selector() << 4)
    row = row.at(row_offset)
    best = u16(0)
    selected = u16(65535)
    remaining = u16(13)
    mask_offset = u16(state.force_selector() << 1)
    masks = state.force_masks
    mask = masks.word(mask_offset)
    for candidate in descending_inclusive(remaining):
        value = row.previous_byte()
        if value > 1:
            continue
        if mask & (1 << candidate):
            continue
        head_offset = u16(candidate << 1)
        if negative_word(heads.word(head_offset)):
            continue
        count = count_force_cities(state, candidate)
        if count > best:
            best = count
            selected = candidate
    return best, selected
