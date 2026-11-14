"""Bounded raw command-order observations over the application's same RAM.

This module only reads a supplied bytearray. It owns no Scene, device, clock,
business model or cached game state, and never infers that an order succeeded.
"""

CITY_SOURCE_IDS = range(1, 41)
PROJECT_RECORD_BASE = 0xE80C
PROJECT_RECORD_BYTES = 12
PROJECT_WORD_OFFSETS = (0, 2, 4, 6, 8, 10)


def observe_command_order_records(ram):
    """Return explicit raw slots and one valid selected-officer task BYTE."""
    if type(ram) is not bytearray or len(ram) != 65536:
        raise ValueError('the same actual64KiB application RAM bytearray is required')
    return dict(
        source='actual_current_same_App_RAM_direct_bytearray_reads',
        confidence='confirmed_RAW_reads_not_order_submission_or_equivalence',
        address_space='64KiB RAM offsets; original bus address is FFFF0000 + offset',
        amount_WORD_sources=_amount_word_sources(),
        city_projects=_city_project_records(ram),
        selected_officer_task=_selected_officer_task(ram),
        Scene_DATA_read_performed=False,
        software_device_clock_or_operations_advanced=False,
        state_or_capacity_modified=False,
        order_success_inferred=False)


def _raw_word(ram, address):
    return (ram[address] << 8) | ram[address + 1]


def _city_project_records(ram):
    return dict(
        source='original E0EE..E102 city*12 and E80C indexed WORD record',
        source_references=[
            'src/m68k/recovered_code.s: original E0EE..E102',
            'tools/high_level_main_flows/business_gameplay.py:_city_project_begin_fields'],
        source_city_ids_inclusive=[1, 40],
        record_RAM_offset_formula='E80C + 12 * source_city_id; no minus-one conversion',
        WORD_offsets_BYTES=list(PROJECT_WORD_OFFSETS),
        raw_WORD_roles=['slot0_officer', 'slot0_payload', 'slot1_officer',
            'slot1_payload', 'slot2_officer', 'slot2_payload'],
        payload_meaning='raw WORD only; third-slot payload is not labelled an amount',
        rows=[_city_project_row(ram, city) for city in CITY_SOURCE_IDS])


def _city_project_row(ram, city):
    address = PROJECT_RECORD_BASE + PROJECT_RECORD_BYTES * city
    return dict(source_city_id=city, RAM_base_offset=format(address, '04X'),
        raw_WORDs=[_raw_word(ram, address + offset) for offset in PROJECT_WORD_OFFSETS])


def _selected_officer_task(ram):
    raw_id = _raw_word(ram, 0xF3A6)
    valid = 0 <= raw_id <= 255
    address = 0xCD00 + raw_id if valid else None
    return dict(source='original selected officer F3A6.W and CD00[id] task BYTE',
        source_references=['src/m68k/recovered_code.s: original E0FE..E108',
            'tools/high_level_remaining_flows/business_lowbank.py:lowbank_calculate_live_quotient_2_fields'],
        selector_RAM_WORD_offset='F3A6', raw_selector_WORD=raw_id,
        valid_officer_BYTE_id=valid,
        RAM_BYTE_offset=format(address, '04X') if valid else None,
        raw_task_BYTE=ram[address] if valid else None,
        status='confirmed_raw_task_BYTE' if valid else 'unknown_outside_0_to_255_no_task_read',
        task_meaning='raw BYTE; no guessed uniform task code or submission verdict')


def _amount_word_sources():
    return dict(
        source='business_budget full-Frame amount controls; no register reconstruction',
        source_references=[
            'tools/high_level_player_commands/business_budget.py:add_selected_cost_frame_fields',
            'tools/high_level_player_commands/business_budget.py:select_next_amount_place_frame_fields'],
        RAM_WORD_roles={'F39A': 'raw selected decimal-place WORD',
            'F3F4': 'raw current amount high WORD', 'F3F6': 'raw current amount low WORD',
            'F3F8': 'raw live limit high WORD', 'F3FA': 'raw live limit low WORD',
            'F3FC': 'raw amount-control WORD', 'F3A4': 'raw command flags WORD'},
        combined_LONG_or_registers_inferred=False)
