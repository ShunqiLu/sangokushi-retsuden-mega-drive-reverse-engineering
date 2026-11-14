"""One fixed raw palette view over the same application's live backings.

No Scene, bus, DATA owner, renderer or clock is called. This is not a generic
memory dump, a second game state, a colour repair or a CPU-equivalence claim.
"""


def _raw_word(backing, offset):
    return (backing[offset] << 8) | backing[offset + 1]


def _palette_words(backing, start):
    """Exactly64 original big-endian WORDs; never mask or convert colours."""
    return [_raw_word(backing, offset) for offset in range(start, start + 128, 2)]


def observe_palette_backings(cram, registers, ram):
    """Read only the three fixed palette regions and six control WORDs."""
    for label, backing, size in (('CRAM', cram, 128),
            ('VDP registers', registers, 32), ('Scene RAM', ram, 65536)):
        if type(backing) is not bytearray or len(backing) != size:
            raise ValueError('the same actual ' + label + ' bytearray of ' + str(size) + ' bytes is required')
    controls = (0x7026, 0xF600, 0xF612, 0xF352, 0xF32C, 0xF32E)
    return dict(source='raw_same_App_reads', raw_same_App_reads=True,
        confidence='confirmed_RAW_reads_not_CPU_or_original_equivalence',
        WORD_order='big_endian_raw_no_mask_or_RGB_conversion',
        CRAM_WORDs=_palette_words(cram, 0),
        RAM_FB00_WORDs=_palette_words(ram, 0xFB00),
        RAM_FB80_WORDs=_palette_words(ram, 0xFB80),
        VDP_register_BYTES=list(registers),
        RAM_WORDs={format(offset, '04X'): _raw_word(ram, offset) for offset in controls},
        Scene_DATA_read_performed=False, renderer_or_bus_called=False,
        software_device_clock_or_operations_advanced=False,
        state_or_capacity_modified=False, CPU_or_original_equivalence_claimed=False,
        cross_thread_atomic_snapshot_claimed=False)
