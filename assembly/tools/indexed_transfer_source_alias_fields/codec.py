"""Lossless conditional transfer source aliases, with the original read prefix.

The 017F30 roster/packet prefix and 01807A first pointed LONG are projected
from live memory. The original ROM destination write is an explicit boundary,
not an ignored write, a manufactured return, or permission to read A2 later.
This compatibility/data projection is not final semantic high-level recovery.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
from functools import lru_cache
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared
from tools.cart_mirrored_tile_source_alias_fields import codec as cart

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = cart.ROM_SHA256
DEFAULT_ROM = ROOT.parent / 'work/original_g5510.bin'
OUTPUT_ROOT = ROOT / 'build/indexed_transfer_source_alias_fields'
FORMAL_ROOT = ROOT / 'analysis/indexed_transfer_source_alias_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
DEFAULT_BUNDLE = FORMAL_ROOT
FORMAT = 'g5510-indexed-transfer-conditional-source-BYTE-alias-v1'
EDITABLE_BYTES, PHYSICAL_BLOCKS = 78, 26
MAX_JSON = 8 * 1024 * 1024
MEMBERS = frozenset(('fields.json', 'fields.schema.json', 'validation.json', 'manifest.json'))
SPANS = ((0xC1612, 0xC1616), (0xC363C, 0xC3640), (0xF30FC, 0xF3100),
    (0xF317C, 0xF317E), (0xF31C0, 0xF31C4), (0xF3604, 0xF3605),
    (0xF4000, 0xF4002), (0xF41F0, 0xF41F1), (0xF41F3, 0xF41F4),
    (0xF41F8, 0xF41FA), (0xF4298, 0xF4299), (0xF43F0, 0xF43F3),
    (0xF43F8, 0xF43FC), (0xF45FA, 0xF45FC), (0xF5314, 0xF5316),
    (0xF5342, 0xF5346), (0xF6022, 0xF6024), (0xF6303, 0xF6304),
    (0xF6306, 0xF6308), (0xF6600, 0xF6608), (0xF6666, 0xF666A),
    (0xF6700, 0xF6704), (0xF670C, 0xF6710), (0xF6716, 0xF671A),
    (0xF672C, 0xF6730), (0xF6740, 0xF6744))
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
BODIES = ((0xD0A, 0xD14, reference_value(__name__, 'BODIES')),
    (0x17D10, 0x17D3C, reference_value(__name__, 'BODIES_2')),
    (0x17F30, 0x1805A, reference_value(__name__, 'BODIES_3')),
    (0x1807A, 0x18196, reference_value(__name__, 'BODIES_4')),
    (0x181A6, 0x181E8, reference_value(__name__, 'BODIES_5')),
    (0x35760, 0x357F8, reference_value(__name__, 'BODIES_6')))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
BANK_SHA256 = {'0c': reference_value(__name__, 'BANK_SHA256'),
    '0f': reference_value(__name__, 'BANK_SHA256_2')}
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
safe_path, read_bounded, put, load_fields = shared.safe_path, shared.read_bounded, shared.put, shared.load_fields
cart_read = cart.cart_read


def _s16(value):
    value &= 65535
    return value - 65536 if value & 32768 else value


def _image(image):
    cart._image(image)


def _controls(image):
    for first, end, digest in BODIES:
        if sha(image[first:end]) != digest:
            raise ValueError('original transfer caller/control/helper bytes changed')


def verify_rom(rom):
    _image(rom)
    if sha(rom) != ROM_SHA256:
        raise ValueError('canonical original ROM SHA-256 differs')
    _controls(rom)


class _PrefixBoundary(ValueError):
    def __init__(self, reason, PC, address=None):
        self.PC, self.address = PC, address
        super().__init__(reason)


def source_view(image, supplied_F6D6_WORD, source_read_budget=7, RAM_before=None):
    """Real original caller/data/stack prefix, bounded before the A2 follow.

    Default RAM is a disclosed constructed frame: F3A6=1, empty packet at9000,
    owner0 and roster[1,FFFF]. It is not a natural game-state assertion. An
    optional complete RAM frame is consumed live; F6D6 is supplied explicitly.
    The source budget is a diagnostic stop, never an original CPU terminator.
    """
    _image(image); _controls(image)
    word = uint(supplied_F6D6_WORD, 65535, 'complete supplied F6D6 WORD')
    budget = uint(source_read_budget, 7, 'diagnostic ROM source read budget')
    if RAM_before is not None and (type(RAM_before) is not bytes or len(RAM_before) != 65536):
        raise ValueError('complete live64KiB RAM bytes required')
    ram = bytearray(65536) if RAM_before is None else bytearray(RAM_before)
    if RAM_before is None:
        ram[0xF3A6:0xF3A8] = b'\x00\x01'
        start = 0xA550 if not word & 2 else 0xA5A4
        ram[start:start + 4] = b'\x00\x01\xff\xff'
    ram[0xF6D6:0xF6D8] = word.to_bytes(2, 'big')
    initial_ram = bytes(ram)
    ordered, reads, writes, source_reads, frames, pairs = [], [], [], [], [], []
    sp = 0xFFFFFE80
    visits = 0
    result = dict(supplied_F6D6_WORD=word, caller_entry=0xD0A, caller_JSR_PC=0xD0E,
        helper_BSR_PC=0x17FA8, natural_domain='unknown', complete_CPU=False,
        complete_function=False, source_read_budget=budget, budget_is_original_CPU_stop=False,
        initial_SP=sp, ordered_events=ordered, source_reads=source_reads, RAM_writes=writes,
        actual_call_RTS_pairs=pairs, original_A2_dereference_executed=False,
        RAM_before=initial_ram.hex(), condition='constructed/live RAM; no interrupt or async mutation')

    def tick(PC):
        nonlocal visits
        visits += 1
        if visits > 4096:
            raise _PrefixBoundary('diagnostic data-loop budget', PC)

    def read(PC, address, size, role='data'):
        tick(PC); address &= 0xFFFFFFFF; bus = address & 0xFFFFFF
        if size > 1 and bus & 1:
            raise _PrefixBoundary('odd WORD/LONG source address', PC, address)
        if 0xFF0000 <= bus and bus + size <= 0x1000000:
            value = int.from_bytes(ram[bus & 65535:(bus & 65535) + size], 'big')
            event = dict(PC=PC, address=address, bus_address=bus, bytes=size, value=value,
                         role=role, memory='work_RAM', physical_addresses=[])
        else:
            if len(source_reads) >= budget:
                raise _PrefixBoundary('diagnostic ROM source read budget', PC, address)
            try:
                event = cart_read(image, address, size, PC)
            except ValueError as error:
                raise _PrefixBoundary(str(error), PC, address) from error
            event['role'] = role
            source_reads.append(event)
            value = event['value']
        reads.append(event); ordered.append(dict(kind='read', **event))
        return value

    def write(PC, address, size, value, role='data'):
        tick(PC); address &= 0xFFFFFFFF; bus = address & 0xFFFFFF
        if size > 1 and bus & 1:
            raise _PrefixBoundary('odd WORD/LONG write address', PC, address)
        if not (0xFF0000 <= bus and bus + size <= 0x1000000):
            is_rom = any(a <= bus and bus + size <= z for a, z in cart.ROM_REGIONS)
            raise _PrefixBoundary('ROM write architecture boundary' if is_rom else 'unsupported write destination', PC, address)
        value &= (1 << (size * 8)) - 1
        ram[bus & 65535:(bus & 65535) + size] = value.to_bytes(size, 'big')
        event = dict(PC=PC, address=address, bus_address=bus, bytes=size, value=value,
                     role=role, memory='work_RAM')
        writes.append(event); ordered.append(dict(kind='write', **event))

    def call(PC, target, return_PC):
        nonlocal sp
        sp = (sp - 4) & 0xFFFFFFFF
        write(PC, sp, 4, return_PC, 'actual_call_return_LONG')
        frames.append(dict(call_PC=PC, target=target, return_PC=return_PC, SP=sp))

    def ret(PC):
        nonlocal sp
        target = read(PC, sp, 4, 'actual_RTS_return_LONG')
        if not frames or frames[-1]['return_PC'] != target:
            raise _PrefixBoundary('corrupted/unmatched actual return', PC, sp)
        pairs.append(dict(**frames.pop(), actual_RTS_PC=PC)); sp = (sp + 4) & 0xFFFFFFFF

    try:
        call(0xD0E, 0x17F30, 0xD14)
        selected = (read(0x17F30, 0xFFFFF6D6, 2, 'live_F6D6_WORD') & 2) << 1
        roster = read(0x17F3A, 0x17F18 + selected, 4, 'masked_roster_directory_LONG')
        roster_head = roster
        counter = read(0x17F40, 0x17F20 + selected, 4, 'masked_roster_directory_LONG')
        coordinates = read(0x17F44, 0x17F28 + selected, 4, 'masked_roster_directory_LONG')
        write(0x17F48, counter, 2, read(0x17F48, counter, 2) - 1)
        unit = read(0x17F4A, 0xFFFFF3A6, 2, 'live_F3A6_WORD')
        call(0x17F4E, 0x181A6, 0x17F52)
        secondary_owner = bool(read(0x181A6, 0xFFFFF6D7, 1) & 2)
        owner_index = read(0x181CC if secondary_owner else 0x181B4, 0xFFFFF68A, 2)
        owner_width = 2 if secondary_owner else 1
        owner = read(0x181D2 if secondary_owner else 0x181B8,
                     (0xFFFFF45E if secondary_owner else 0xFFFFA027) +
                     _s16((owner_index << 1) if secondary_owner else owner_index), owner_width)
        ret(0x181E6)
        if (unit & ((1 << (owner_width * 8)) - 1)) == owner:
            raise _PrefixBoundary('original owner CARRY path outside this bounded transfer prefix', 0x17F52)
        while True:
            item = read(0x17F56, roster, 2); roster = (roster + 2) & 0xFFFFFFFF
            if item == unit: break
        while True:
            item = read(0x17F5C, roster, 2); roster = (roster + 2) & 0xFFFFFFFF
            write(0x17F5C, roster - 4, 2, item)
            if item & 0x8000: break
        coord = read(0x17F62, coordinates, 2)
        call(0x17F64, 0x17D10, 0x17F68)
        x, y = (coord >> 8) & 255, coord & 255
        packet = 0xFFFF9000
        while True:
            count = read(0x17D1A, packet, 1) & 15
            if count == 0: break
            old_x = read(0x17D24, packet + 1, 1)
            if old_x == x and read(0x17D2C, packet + 2, 1) == y: break
            packet = (packet + 13 + count) & 0xFFFFFFFF
        ret(0x17D3A)
        write(0x17F68, packet + 1, 1, x); write(0x17F6C, packet + 2, 1, y)
        old_count = read(0x17F70, packet, 1) & 15
        if old_count == 0:
            for lane in range(9): write(0x17F78 + 4 * lane, packet + 5 + lane, 1, 0)
        write(0x17F9C, packet, 1, read(0x17F9C, packet, 1) + 1)
        call(0x17FA0, 0x1802A, 0x17FA4)
        insert = (packet + 13 + old_count) & 0xFFFFFFFF
        scan = insert
        if old_count == 0: write(0x18036, scan, 1, 0)
        while True:
            count = read(0x18038, scan, 1) & 15
            if count == 0: break
            scan = (scan + 13 + count) & 0xFFFFFFFF
        destination = (scan + 1) & 0xFFFFFFFF
        write(0x1804C, destination, 1, 0)
        while scan > insert:
            scan = (scan - 1) & 0xFFFFFFFF; destination = (destination - 1) & 0xFFFFFFFF
            write(0x18054, destination, 1, read(0x18054, scan, 1))
        ret(0x18058)
        # 1802A really replaces A2 with the insert pointer before 17FA4.
        write(0x17FA4, insert, 1, read(0x17FA4, 0xFFFFF3A7, 1))
        call(0x17FA8, 0x1807A, 0x17FAC)
        live_word = read(0x1807A, 0xFFFFF6D6, 2, 'live_full_F6D6_WORD')
        offset = _s16(live_word << 2)
        pointer1 = read(0x18080, 0x1805A + offset, 4, 'live_fullWORD_pointer_slot_LONG')
        pointer2 = read(0x18084, 0x1806A + offset, 4, 'live_fullWORD_pointer_slot_LONG')
        result.update(shifted_signed_WORD=offset, pointer_slot1=0x1805A + offset,
                      pointer_slot2=0x1806A + offset, encoded_A1=pointer1, encoded_A2=pointer2)
        first = read(0x18088, pointer1, 4, 'first_pointed_LONG')
        result['first_pointed_LONG'] = first
        participant = read(0x18090, 0xFFFFF3A6, 2)
        table = 0xFFFFC800
        participant_value = (read(0x18096, table + _s16(participant << 2), 4) + 100) & 0xFFFFFFFF
        numerator = ((first & 65535) >> 8) * (participant_value & 65535)
        denominator = participant_value & 65535
        while True:
            other = read(0x180A6, roster_head, 2); roster_head = (roster_head + 2) & 0xFFFFFFFF
            if other & 0x8000: break
            denominator = (denominator + read(0x180B0, table + _s16((other & 255) << 2), 4) + 100) & 0xFFFFFFFF
        call(0x180BE, 0x35760, 0x180C4)
        if numerator & 0x80000000 or denominator == 0 or denominator > 65535:
            raise _PrefixBoundary('original division branch outside bounded small unsigned path', 0x35760)
        saved_D3 = participant_value & 65535
        saved_D1 = numerator & 65535
        for value in (saved_D3, saved_D1):
            sp = (sp - 2) & 0xFFFFFFFF; write(0x357DA, sp, 2, value, 'actual_MOVEM_WORD')
        high_q, high_r = divmod(numerator >> 16, denominator)
        if high_q > 65535: raise _PrefixBoundary('original DIVU overflow', 0x357E2)
        low = read(0x357E6, sp, 2, 'actual_MOVEM_WORD_restore'); sp = (sp + 2) & 0xFFFFFFFF
        low_q, remainder = divmod((high_r << 16) | low, denominator)
        if low_q > 65535: raise _PrefixBoundary('original DIVU overflow', 0x357E8)
        restored_D3 = read(0x357F4, sp, 2, 'actual_MOVEM_WORD_restore'); sp = (sp + 2) & 0xFFFFFFFF
        ret(0x357F6)
        amount = (((high_q << 16) | low_q) << 8) & 0xFFFFFFFF
        result.update(original_division=dict(quotient=(high_q << 16) | low_q, remainder=remainder,
                      restored_D3_WORD=restored_D3), first_SUB_LONG_amount=amount)
        destination_value = read(0x180C6, pointer1, 4, 'RMW_destination_LONG')
        write(0x180C6, pointer1, 4, destination_value - amount, 'RMW_SUB_LONG')
        result.update(status='diagnostic_stop_after_RAM_RMW', boundary_PC=0x180C8,
                      boundary='A2 dereference not part of this bounded first-source projection')
    except _PrefixBoundary as error:
        result.update(status='boundary', boundary=str(error), boundary_PC=error.PC,
                      boundary_address=error.address)
    result.update(source_read_count=len(source_reads), final_SP=sp,
                  unreturned_calls=list(frames), real_call_RTS_pair_count=len(pairs),
                  RAM_after=bytes(ram).hex(), ROM_write_skipped=False,
                  physical_source=sorted({p for row in source_reads for p in row['physical_addresses']}))
    return result


@lru_cache(maxsize=2)
def _catalog(rom):
    verify_rom(rom)
    wanted = {p for first, end in SPANS for p in range(first, end)}
    if len(wanted) != EDITABLE_BYTES or len(SPANS) != PHYSICAL_BLOCKS:
        raise ValueError('fixed unique physical costs differ')
    selected = {}
    for word in range(16384):
        slot = 0x1805A + _s16(word << 2)
        pointer = int.from_bytes(rom[slot:slot + 4], 'big')
        try: event = cart_read(rom, pointer, 4, 0x18088)
        except ValueError: continue
        new = set(event['physical_addresses']) & wanted
        if not new: continue
        view = source_view(rom, word)
        if view['boundary_PC'] != 0x180C6 or view['boundary'] != 'ROM write architecture boundary':
            raise ValueError('canonical true prefix/destination boundary differs')
        first = next(row for row in view['source_reads'] if row['PC'] == 0x18088)
        for position in new:
            selected.setdefault(position, dict(address=position, supplied_F6D6_WORD=word,
                fullWORD_aliases=[word + 16384 * k for k in range(4)], read_PC=0x18088,
                pointer_slot1=view['pointer_slot1'], pointer_slot2=view['pointer_slot2'],
                encoded_A1=view['encoded_A1'], encoded_A2=view['encoded_A2'],
                bus_address=first['bus_address'], physical_addresses=first['physical_addresses'],
                true_caller_JSR_PC=0xD0E, true_helper_BSR_PC=0x17FA8,
                original_boundary_PC=0x180C6, helper_returned=False))
    if set(selected) != wanted or sha(bytes(rom[p] for p in sorted(wanted))) != SOURCE_SHA256:
        raise ValueError('canonical source digest or true-prefix coverage differs')
    return tuple(selected[p] for p in sorted(wanted))


def physical_positions(rom):
    verify_rom(rom)
    return tuple(row['address'] for row in _catalog(rom))


def witness(rom, address):
    verify_rom(rom); address = uint(address, ROM_SIZE - 1, 'physical source BYTE')
    for row in _catalog(rom):
        if row['address'] == address: return load_fields(dump(row))
    raise ValueError('outside fixed physical BYTE allocation')


def metadata(rom):
    physical_positions(rom)
    return dict(format=FORMAT, confidence='confirmed_conditional_source_encoding',
        resource_role='candidate_indexed_transfer_first_LONG_source_BYTE_alias',
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256), source_union_BYTES=EDITABLE_BYTES,
        source_union_sha256=SOURCE_SHA256, physical_blocks=PHYSICAL_BLOCKS,
        physical_scope=[dict(start=a, end=z, bytes=z-a) for a, z in SPANS],
        raw_baseline=dict(layout_id=LAYOUT_ID, manifest_sha256=LAYOUT_SHA256, raw_BYTES=14239,
                          source_all_fixed_raw=True, bank_sha256=BANK_SHA256),
        cart_profile=dict(emulator='MAME0.289 megadrij fresh original cart',
            measured_ROM_regions=[list(row) for row in cart.ROM_REGIONS], SRAM_aperture=list(cart.SRAM_APERTURE),
            geometry_header=dict(start=cart.MAPPER_HEADER_START, end=cart.MAPPER_HEADER_END, bytes=cart.MAPPER_HEADER_HEX),
            measurement_SHA=reference_value(__name__, 'metadata'),
            measurement_dump_build_dependency=False, outside4M='unmeasured reject', original_hardware_equivalence='unknown'),
        evidence=dict(controls=[dict(start=a, end=z, sha256=h) for a, z, h in BODIES],
            caller_entry=0xD0A, true_JSR_PC=0xD0E, supplied_RAM_WORD=0xFFFFF6D6,
            live_WORD_read_PC=0x1807A, LSL_WORD_shift=2, signed_WORD_EA=True,
            pointer_bases=[0x1805A, 0x1806A], pointer_read_order=[0x18080, 0x18084, 0x18088],
            supplied_WORD_diagnostic_domain=65536, offset_period=16384, WORD_aliases=4,
            matched_canonical_WORD_inputs=260, first_pointed_read_PC=0x18088,
            ROM_write_boundary_PC=0x180C6, A2_dereference_PC=0x18106, A2_dereference_admitted=False,
            division_JSR_PC=0x180BE, division_return_PC=0x180C4, MOVEM_WORD_bytes=4,
            default_frame='F3A6=1; owner0; F68A0; roster[1,FFFF]; empty packet9000; conditional, not natural'),
        editing_authority='unique physical BYTE; pointer-slot/code/old typed neighbors are live read views, not second emission',
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        functions_added=0, complete_function_recovery=False, independent_CPU_comparison=False,
        pointer_target_owner='unknown', natural_selector_domain='unknown', edited_gameplay_safety='unknown',
        padding_or_free_space_claimed=False)


def extract(rom):
    return dict(**metadata(rom), source_BYTEs=[dict(address=a, BYTE=rom[a]) for a in physical_positions(rom)])


def blocks(rom, fields):
    fixed = metadata(rom); keys(fields, set(fixed) | {'source_BYTEs'}, 'indexed transfer source package')
    for key, value in fixed.items(): same(fields[key], value, 'package.' + key)
    values = {}
    for address, row in zip(physical_positions(rom), exact_list(fields['source_BYTEs'], EDITABLE_BYTES, 'source BYTEs')):
        keys(row, {'address', 'BYTE'}, 'source BYTE'); same(row['address'], address, 'physical address/order')
        values[address] = uint(row['BYTE'], 255, 'all source BYTE bits')
    return [dict(id=f'rom_{a:06X}_indexed_transfer_source_BYTEs', start=a, end=z,
        data=bytes(values[p] for p in range(a, z)), role='candidate_conditional_transfer_first_LONG_source_BYTE_alias')
        for a, z in SPANS]


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields): image[row['start']:row['end']] = row['data']
    return bytes(image)


def schema(rom):
    def obj(properties):
        return dict(type='object', properties=properties, required=list(properties), additionalProperties=False)
    def fixed(value):
        if type(value) is dict: return obj({k: fixed(v) for k, v in value.items()})
        if type(value) is list: return dict(type='array', prefixItems=[fixed(v) for v in value],
                                           items=False, minItems=len(value), maxItems=len(value))
        return dict(type={str: 'string', int: 'integer', bool: 'boolean'}[type(value)], const=value)
    properties = {key: fixed(value) for key, value in metadata(rom).items()}
    properties['source_BYTEs'] = dict(type='array', minItems=EDITABLE_BYTES, maxItems=EDITABLE_BYTES,
        prefixItems=[obj(dict(address=fixed(a), BYTE=dict(type='integer', minimum=0, maximum=255)))
                     for a in physical_positions(rom)], items=False)
    return dict(**obj(properties), **{'$schema': 'https://json-schema.org/draft/2020-12/schema'},
                description='78 unique complete BYTE authorities; full WORD input is not an editor slot clamp.')


def render_bundle(rom):
    fields = extract(rom); image = rebuild(rom, load_fields(dump(fields)))
    if image != rom: raise ValueError('serialized whole ROM roundtrip differs')
    validation = dict(**metadata(rom), editable_bytes=EDITABLE_BYTES, whole_ROM_exact=True,
        whole_ROM_sha256=sha(image), canonical_BYTE_witnesses=list(_catalog(rom)),
        limitations=['Source-prefix only; ROM write stops before helper RTS and A2 dereference.',
                     'Conditional constructed frame, not natural selector/owner/fullCPU/VDP.'])
    members = {'fields.json': dump(fields), 'fields.schema.json': dump(schema(rom)), 'validation.json': dump(validation)}
    members['manifest.json'] = dump(dict(**metadata(rom), editable_bytes=EDITABLE_BYTES,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ValueError('reparse output refused')
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError('dedicated fresh build output or exact fresh formal bundle required')
    if path.exists() or not path.parent.is_dir(): raise ValueError('fresh output and existing parent required')
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('export', 'import', 'verify'))
    parser.add_argument('--rom', default=str(DEFAULT_ROM)); parser.add_argument('--fields')
    parser.add_argument('--bundle'); parser.add_argument('--output'); args = parser.parse_args(argv)
    target = None
    if args.command == 'export':
        if args.output is None or args.fields is not None or args.bundle is not None: raise ValueError('export requires output only')
        target = fresh_output(args.output, bundle=True)
    elif args.command == 'import':
        if args.output is None or args.bundle is not None: raise ValueError('import requires fresh .bin output')
        target = fresh_output(args.output)
        if target.suffix.lower() != '.bin': raise ValueError('fresh .bin output required')
    elif args.output is not None or args.fields is not None and args.bundle is not None:
        raise ValueError('verify takes fields or bundle and writes nothing')
    rom = read_bounded(args.rom, ROM_SIZE)
    if args.command == 'export':
        members = render_bundle(rom); target.mkdir()
        for name, data in members.items(): put(target / name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES, members={name: sha(data) for name, data in members.items()})
    elif args.command == 'verify' and args.bundle is not None:
        path = safe_path(args.bundle)
        if not path.is_dir() or {p.name for p in path.iterdir()} != MEMBERS: raise ValueError('exact four bundle members required')
        for name, data in render_bundle(rom).items():
            if read_bounded(path / name, MAX_JSON) != data: raise ValueError('generated member drift: ' + name)
        result = dict(verified=True, editable_bytes=EDITABLE_BYTES, whole_ROM_exact=True)
    else:
        image = rebuild(rom, load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON)))
        if target is not None: put(target, image)
        result = dict(exact_canonical=image == rom, sha256=sha(image), editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result, sort_keys=True)); return 0


if __name__ == '__main__': raise SystemExit(main())
