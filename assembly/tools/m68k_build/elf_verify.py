"""Read-only validation of the bounded, fixed-origin GNU 68000 object format.

This is intentionally not a general ELF loader. It accepts the ET_REL format
emitted for this project's mnemonic source, without relocation or extra code
sections. Record metadata other than address/size is ignored. It validates
layout, not opcode semantics: an edited instruction may have different bytes
while retaining its independently supplied start and end addresses.
"""

from __future__ import annotations

import re
import struct

ROM_SIZE = 0x100000
HEADER = struct.Struct(">16sHHIIIIIHHHHHH")
SECTION = struct.Struct(">IIIIIIIIII")
SYMBOL = struct.Struct(">IIIBBH")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _records(records: list) -> dict[str, int]:
    _require(type(records) is list and bool(records), "records must be a nonempty list")
    expected: dict[str, int] = {}
    previous_end = 0
    for record in records:
        _require(type(record) is dict and 'address' in record and 'size' in record,
                 "each record must supply address and size")
        address, size = record['address'], record['size']
        _require(type(address) is int and type(size) is int, "record numbers must be strict integers")
        _require(0 <= address < ROM_SIZE and address % 2 == 0,
                 "record address must be an even ROM offset")
        _require(2 <= size <= 22 and size % 2 == 0 and address + size <= ROM_SIZE,
                 "record size must be a bounded whole-instruction width")
        _require(address >= previous_end, "records must be ordered and nonoverlapping")
        previous_end = address + size
        expected[f'm68k_{address:06x}'] = address
        expected[f'm68k_{address:06x}_end'] = previous_end
    return expected


def _string(table: bytes, offset: int, context: str) -> str:
    _require(0 <= offset < len(table), f"{context}: string offset outside table")
    end = table.find(b'\0', offset)
    _require(end >= 0, f"{context}: unterminated string")
    try:
        return table[offset:end].decode('utf-8')
    except UnicodeDecodeError as error:
        raise ValueError(f"{context}: invalid UTF-8 name") from error


def verify_object(data: bytes, records: list) -> bytes:
    """Validate GNU ELF32/MSB/EM_68K ET_REL and return its raw .text bytes.

    Raises ValueError for malformed input, relocation, unexpected sections,
    missing/duplicate/extra instruction labels, or any changed label extent.
    No filesystem access, external process, disassembler or canonical-byte
    comparison is performed. Callers remain responsible for checking that
    the source is instruction-only and for splicing only record extents.
    """
    expected = _records(records)
    _require(type(data) is bytes, "ELF input must be bytes")
    _require(HEADER.size <= len(data) <= 32 * ROM_SIZE, "ELF size outside bounded format")
    (ident, kind, machine, version, entry, phoff, shoff, flags, ehsize,
     phentsize, phnum, shentsize, shnum, shstrndx) = HEADER.unpack_from(data)
    _require(ident == b'\x7fELF\x01\x02\x01' + b'\0' * 9,
             "expected ELF32 big-endian version 1 System V identity")
    _require((kind, machine, version) == (1, 4, 1), "expected ET_REL / EM_68K / version 1")
    _require(entry == phoff == phentsize == phnum == 0,
             "relocatable object must not have entry or program headers")
    # Current GNU -m68000 emits EF_M68K_M68000; older generic m68k objects
    # may leave flags unset. Other CPU/ColdFire flags are not this format.
    _require(flags in (0, 0x01000000), "object processor flags are not base m68k/68000")
    _require(ehsize == HEADER.size and shentsize == SECTION.size,
             "invalid ELF or section header width")
    _require(2 <= shnum <= 4096 and 0 < shstrndx < shnum, "invalid section count or name-table index")
    _require(shoff >= HEADER.size and shoff % 4 == 0 and shoff + shnum * SECTION.size <= len(data),
             "section header table outside ELF")

    names = ('name_offset', 'type', 'flags', 'address', 'offset', 'size',
             'link', 'info', 'alignment', 'entry_size')
    sections = [dict(zip(names, SECTION.unpack_from(data, shoff + index * SECTION.size)))
                for index in range(shnum)]
    _require(not any(sections[0].values()), "section zero must be the null section")
    occupied = [(0, HEADER.size), (shoff, shoff + shnum * SECTION.size)]
    for index, section in enumerate(sections[1:], 1):
        offset, size, alignment = section['offset'], section['size'], section['alignment']
        _require(section['type'] not in (4, 9), "relocation sections are forbidden, including empty ones")
        _require(section['address'] == 0, "ET_REL section has a nonzero load address")
        _require(alignment == 0 or (alignment <= ROM_SIZE and alignment & (alignment - 1) == 0),
                 "invalid section alignment")
        _require(offset <= len(data), "section offset outside ELF")
        if section['type'] != 8:  # SHT_NOBITS has no file-backed payload.
            _require(offset + size <= len(data), "section contents outside ELF")
            if size:
                _require(alignment <= 1 or offset % alignment == 0, "misaligned section payload")
                occupied.append((offset, offset + size))
        _require(section['link'] < shnum, "section link outside section table")
    occupied.sort()
    _require(all(left[1] <= right[0] for left, right in zip(occupied, occupied[1:])),
             "ELF headers or section payloads overlap")

    def payload(section: dict) -> bytes:
        return data[section['offset']:section['offset'] + section['size']]

    name_section = sections[shstrndx]
    _require(name_section['type'] == 3, "section-name table is not SHT_STRTAB")
    name_table = payload(name_section)
    _require(bool(name_table) and name_table[0] == name_table[-1] == 0,
             "section-name table must be NUL-framed")
    by_name: dict[str, tuple[int, dict]] = {}
    allowed = {'.text', '.data', '.bss', '.symtab', '.strtab', '.shstrtab', '.note.GNU-stack'}
    for index, section in enumerate(sections[1:], 1):
        name = _string(name_table, section['name_offset'], 'section')
        _require(name in allowed and name not in by_name, "unexpected or duplicate ELF section")
        by_name[name] = (index, section)
    _require({'.text', '.symtab', '.strtab', '.shstrtab'} <= by_name.keys(),
             "missing required text or symbol metadata section")
    _require(by_name['.shstrtab'][0] == shstrndx, "wrong section-name table identity")
    for name, (_, section) in by_name.items():
        if name == '.text':
            _require(section['type'] == 1 and section['flags'] == 6,
                     ".text must be allocated executable PROGBITS")
        elif name == '.symtab':
            _require(section['type'] == 2 and section['flags'] == 0,
                     "symbol table has invalid type or flags")
        elif name in ('.strtab', '.shstrtab'):
            _require(section['type'] == 3 and section['flags'] == 0,
                     "string table has invalid type or flags")
        else:
            _require(section['size'] == 0, "unexpected nonempty non-text section")
            expected_type = 8 if name == '.bss' else 1
            expected_flags = 3 if name in ('.bss', '.data') else 0
            _require(section['type'] == expected_type and section['flags'] == expected_flags,
                     "invalid empty auxiliary section")
        if name != '.symtab':
            _require(section['link'] == section['info'] == section['entry_size'] == 0,
                     "unexpected auxiliary section linkage")

    text_index, text_section = by_name['.text']
    text = payload(text_section)
    _require(max(expected.values()) <= len(text) <= ROM_SIZE,
             ".text does not contain all record extents or exceeds ROM")
    symbol_section = by_name['.symtab'][1]
    _require(symbol_section['entry_size'] == SYMBOL.size and symbol_section['size'] % SYMBOL.size == 0,
             "invalid symbol table entry width")
    _require(symbol_section['link'] == by_name['.strtab'][0], "symbol table has wrong string-table link")
    symbols = payload(symbol_section)
    count = len(symbols) // SYMBOL.size
    _require(count > 0 and 1 <= symbol_section['info'] <= count, "invalid local-symbol boundary")
    _require(symbols[:SYMBOL.size] == b'\0' * SYMBOL.size, "symbol zero must be null")
    strings = payload(by_name['.strtab'][1])
    _require(bool(strings) and strings[0] == strings[-1] == 0, "symbol strings must be NUL-framed")
    seen: set[str] = set()
    for index in range(1, count):
        name_offset, value, size, info, other, section_index = SYMBOL.unpack_from(symbols, index * SYMBOL.size)
        name = _string(strings, name_offset, 'symbol')
        binding, symbol_type = info >> 4, info & 15
        _require(binding in (0, 1) and symbol_type in (0, 1, 2, 3, 4) and other == 0,
                 "unsupported symbol binding, type or visibility")
        _require((index < symbol_section['info']) == (binding == 0), "incorrect local/global symbol ordering")
        _require(0 < section_index < shnum or section_index == 0xFFF1,
                 "undefined, common or extended-index symbols are forbidden")
        if section_index != 0xFFF1:
            section_size = sections[section_index]['size']
            _require(value <= section_size and size <= section_size - value, "symbol extent outside its section")
        if name.startswith('m68k_'):
            _require(re.fullmatch(r'm68k_[0-9a-f]{6}(?:_end)?', name) is not None and name in expected,
                     "unexpected instruction label")
            _require(name not in seen, "duplicate instruction label")
            _require(section_index == text_index and value == expected[name], "instruction label moved or wrong section")
            _require(symbol_type == 0 and size == 0, "instruction labels must be zero-sized NOTYPE symbols")
            seen.add(name)
    _require(seen == expected.keys(), "missing instruction start/end label")
    return text
