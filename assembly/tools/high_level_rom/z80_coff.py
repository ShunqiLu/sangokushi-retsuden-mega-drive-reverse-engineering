"Pure GNU Z80 COFF validation: the sole executable algorithm authority.\n\nBoth native assembly builds and the old audio-build compatibility functions\ndelegate here. No compiler, game source, ROM, filesystem or native cache is\nowned by this module. Original validation rules and result shapes are retained.\n\nProvenance: B130 extracted these complete functions verbatim from the then\naudio build source. B131 replaced that donor's duplicate bodies with wrappers;\nthe earlier private B130 source/proposal remain historical evidence.\n"
from __future__ import annotations

import struct
from typing import Mapping

MAX_OBJECT_SIZE = 2_000_000


def _unit_shape(unit: str, descriptor: Mapping) -> tuple[list[dict], int, dict[str, int]]:
    if unit not in ('driver', 'startup') or type(descriptor) is not dict:
        raise ValueError('only the separate driver/startup image descriptors are admitted')
    rows = descriptor['rows']
    extent = descriptor['extent']
    if type(rows) not in (list, tuple) or type(extent) is not int:
        raise ValueError('explicit instruction boundaries and image extent are required')
    supplement = unit == 'driver' and len(rows) == 1687
    wanted_count, wanted_bytes, wanted_extent, wanted_base = (
        (1687 if supplement else 1683, 3342 if supplement else 3334, 0x0FCA, 0x69D2)
        if unit == 'driver' else (25, 38, 38, 0x2CA)
    )
    if len(rows) != wanted_count or extent != wanted_extent or descriptor['rom_base'] != wanted_base:
        raise ValueError('the complete original code scope and physical mapping are required')
    previous_end = 0
    width_sum = 0
    symbols = {}
    prefix = 'z80_' if unit == 'driver' else 'boot_z80_'
    for row in rows:
        address, size = row['address'], row['size']
        if (type(address) is not int or type(size) is not int or
                address < previous_end or not 1 <= size <= 4 or address + size > extent):
            raise ValueError('overlapping, out-of-image or malformed instruction extent')
        name = prefix + f'{address:04x}'
        symbols[name], symbols[name + '_end'] = address, address + size
        previous_end = address + size
        width_sum += size
    if previous_end != extent or width_sum != wanted_bytes:
        raise ValueError('an instruction is omitted or the complete code byte count differs')
    if unit == 'driver':
        continuation_ranges = ((0x0A42, 0x0A46), (0x0B84, 0x0B88))
        continuation_rows = [(row['address'], row['size']) for row in rows
                             if any(start <= row['address'] < end for start, end in continuation_ranges)]
        wanted = [(0x0A42, 1), (0x0A43, 3), (0x0B84, 1), (0x0B85, 3)] if supplement else []
        if continuation_rows != wanted:
            raise ValueError('the optional eight-byte continuation supplement must have its exact four boundaries')
    return list(rows), extent, symbols


def verify_object(unit: str, descriptor: dict, object_data: bytes, image: bytes) -> dict:
    """Verify actual bounded GNU little-endian Z80 COFF, not declared placement alone."""
    rows, extent, expected = _unit_shape(unit, descriptor)
    if type(object_data) is not bytes or not 20 <= len(object_data) <= MAX_OBJECT_SIZE:
        raise ValueError('bounded actual COFF bytes are required')
    if type(image) is not bytes or len(image) != extent:
        raise ValueError('the actual binary image must have its exact logical extent')
    magic, sections, timestamp, symptr, symcount, optional, flags = struct.unpack_from(
        '<HHIIIHH', object_data
    )
    header_end = 20 + 40 * sections
    if (magic != 0x805A or sections != 3 or timestamp != 0 or optional != 0 or
            flags != 0x3105 or header_end > len(object_data)):
        raise ValueError('unexpected GNU Z80 COFF identity/header')
    text = None
    text_index = None
    section_names = set()
    for index in range(sections):
        (raw_name, physical, virtual, size, offset, reloc_ptr, line_ptr,
         reloc_count, line_count, section_flags) = struct.unpack_from(
            '<8sIIIIIIHHI', object_data, 20 + 40 * index
        )
        name = raw_name.rstrip(b'\0').decode('ascii')
        if (name not in ('.text', '.data', '.bss') or name in section_names or
                physical or virtual or reloc_ptr or line_ptr or reloc_count or line_count):
            raise ValueError('unexpected section or unresolved relocation/line record')
        section_names.add(name)
        if section_flags != {'.text': 0x20, '.data': 0x40, '.bss': 0x80}[name]:
            raise ValueError('unexpected GNU section flags')
        if size and (offset < header_end or offset + size > symptr):
            raise ValueError('COFF section contents are outside their admitted region')
        if name == '.text':
            text, text_index = object_data[offset:offset + size], index + 1
        elif size:
            raise ValueError('audio code output contains a nonempty non-code section')
    if text != image or len(text) != extent:
        raise ValueError('actual COFF text and actual binary image differ')
    strings_start = symptr + 18 * symcount
    if symptr < header_end or strings_start + 4 > len(object_data):
        raise ValueError('COFF symbol table is outside the object')
    strings_size = struct.unpack_from('<I', object_data, strings_start)[0]
    if strings_size < 4 or strings_start + strings_size != len(object_data):
        raise ValueError('COFF string table bounds differ')
    strings = object_data[strings_start:]
    entry_name = '_start' if unit == 'driver' else '_boot_start'
    seen, entry_seen, index = set(), False, 0
    while index < symcount:
        raw_name, value, section, kind, storage, auxiliaries = struct.unpack_from(
            '<8sIhHBB', object_data, symptr + 18 * index
        )
        if raw_name[:4] == b'\0' * 4:
            offset = struct.unpack_from('<I', raw_name, 4)[0]
            if not 4 <= offset < len(strings) or b'\0' not in strings[offset:]:
                raise ValueError('invalid COFF symbol-name offset/termination')
            name = strings[offset:strings.index(0, offset)].decode('ascii')
        else:
            name = raw_name.rstrip(b'\0').decode('ascii')
        if name in expected:
            if name in seen or section != text_index or value != expected[name] or kind or auxiliaries:
                raise ValueError('actual instruction start/end moved, duplicated or malformed')
            seen.add(name)
        elif name == entry_name:
            if entry_seen or value or section != text_index or kind or auxiliaries:
                raise ValueError('actual image-entry symbol differs')
            entry_seen = True
        elif section == 0:
            raise ValueError('an undefined symbol remains in the actual object')
        elif name not in ('.file', '.text', '.data', '.bss'):
            raise ValueError('unexpected symbol; additional aliases require an explicit contract')
        if index + 1 + auxiliaries > symcount:
            raise ValueError('COFF auxiliary symbol extends past the table')
        index += 1 + auxiliaries
    if seen != set(expected) or not entry_seen:
        raise ValueError('actual object omits an instruction boundary or the image entry')
    positions = {address for row in rows for address in range(row['address'], row['address'] + row['size'])}
    if any(value for address, value in enumerate(image) if address not in positions):
        raise ValueError('sparse noninstruction gaps contain undeclared output')
    return {
        'instructions': len(rows), 'instruction_bytes': len(positions),
        'actual_boundary_symbols': len(seen), 'actual_instruction_mapping': [
            {'logical_pc': row['address'], 'rom_pc': descriptor['rom_base'] + row['address'],
             'width': row['size'], 'actual_start': expected[('z80_' if unit == 'driver' else 'boot_z80_') + f'{row["address"]:04x}'],
             'actual_end': expected[('z80_' if unit == 'driver' else 'boot_z80_') + f'{row["address"]:04x}_end']}
            for row in rows
        ],
        'image_extent': extent, 'sparse_gap_bytes_excluded': extent - len(positions),
        'continuation_supplement_bytes': 8 if unit == 'driver' and len(rows) == 1687 else 0,
        'unresolved_relocations': 0, 'actual_COFF_equals_image': True,
    }


