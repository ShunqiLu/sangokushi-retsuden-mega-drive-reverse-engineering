"""Two independent live debt cleanup policies, not mirror entry bindings."""
from .domain import DebtState, u16, low8, negative_byte, update_flag


def clear_unowned_records(state: DebtState) -> None:
    records = state.records_reverse()
    owners = state.owners()
    for index in records.reverse_slots(16):
        city = u16(0)
        city = records.first_city()
        if city != 0:
            if negative_byte(owners.read(city)):
                records.clear()
                flags = state.flags()
                flags = update_flag(flags, index, 'clear')
                state.store_flags(flags)
            else:
                city = records.second_city()
                if negative_byte(owners.read(city)):
                    records.clear()
                    flags = state.flags()
                    flags = update_flag(flags, index, 'clear')
                    state.store_flags(flags)


def clear_selected_links(state: DebtState) -> None:
    selected_principal = state.principals()
    selected_before_clear = state.selected_word()
    initial_offset = u16(selected_before_clear << 2)
    selected_principal.clear(initial_offset)
    records = state.records_forward()
    owners = state.owners()
    linked_principal = state.principals()
    index = u16(0)
    selected = state.selected_word()
    for index in records.forward_slots(16):
        if records.first_city() == low8(selected):
            other = u16(0)
            other = records.second_city()
            offset = u16(other << 2)
            linked_principal.clear(offset)
        else:
            if records.second_city() != low8(selected):
                continue
        records.clear()
        flags = state.flags()
        flags = update_flag(flags, index, 'clear')
        state.store_flags(flags)
