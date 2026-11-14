"""Lossless, fixed-layout scenario fields, distinct from derived RAM tables.

This is a bounded editor, not a whole-loader CPU emulator or a proof of natural
selector/field domains. Address-based names deliberately retain uncertain roles.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from tools.audio_formats import audio_formats as af
from tools.graphics_build.graphics_build import publish
from tools.static_data import scenario_static_data as legacy

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = af.DEFAULT_ROM
DEFAULT_ASSETS = ROOT/'analysis/scenario_build/generated/assets.json'
FORMAT = 'g5510_scenario_fixed_fields'
EDITABLE_BYTES = 31872
BASES = (0x08AC04, 0x08D580, 0x08FEFC)
IDS = ('scenario_0', 'scenario_1', 'scenario_2')
DIRECTORY = 0x003E48
BLOCK_SIZE = 0x297C
DESCRIPTOR_SIZE = 0x84
SPECS = legacy.TABLE_SPECS
# Descriptor order, intentionally NOT physical order (E710 is out of order).
OFFSETS = (0x84, 0xAC, 0xFC, 0x11C, 0x1BC, 0x25C, 0x2FC, 0x39C,
           0x43C, 0x4DC, 0x57C, 0x61C, 0x6DC, 0x77C, 0x97C, 0xB7C,
           0xD7C, 0xF7C, 0x117C, 0x137C, 0x157C, 0x177C, 0x197C,
           0x1A7C, 0x1B7C, 0x1C7C, 0x1D7C, 0x1E7C, 0x1F7C, 0x237C,
           0x6BC, 0x247C, 0x277C)
TABLE_IDS = tuple(s.table_id for s in SPECS)
SPLIT_WORDS = frozenset(('ram_e1e0', 'ram_e320', 'ram_e5a0'))
GROUPS = (('cities', 40, 1), ('forces', 16, 0), ('officers', 256, 0))
GROUP_SPECS = {name: tuple(s for s in SPECS if s.record_count == count)
               for name, count, _ in GROUPS}
ADDRESSES = {f'{ident}.{s.table_id}': base+offset
             for ident, base in zip(IDS, BASES) for s, offset in zip(SPECS, OFFSETS)}

# Canonical raw instructions, independently disassembled as M68000. Every byte
# in the loader and helper interval is guarded, not just a convenient prefix.
ANCHORS = {
    0x003E54: (
        '3038efd4e548247b00ec' '205243f8f428610001c0206a000443f8f460610001f0'
        '206a000843f8e640303c000722d851c8fffc206a000c43f8e000610001a2'
        '206a001043f8e0a06100' '0196206a001443f8e1406100018a206a001843f8e1e0'
        '6100017e206a001c43f8' 'e28061000172206a002043f8e32061000166206a0024'
        '43f8e3c06100015a206a' '002843f8e4606100014e206a002c43f8e50061000142'
        '206a003043f8e5a06100' '0136206a003443f8b00061000136206a003843f8b200'
        '6100012a206a003c43f8' 'b4006100011e206a004043f8b60061000112206a0044'
        '43f8b80061000106206a' '004843f8ba00610000fa206a004c43f8bc00610000ee'
        '206a005043f8be006100' '00e2206a005443f8c000610000d6206a005843f8c200'
        '610000d6206a005c43f8' 'c300610000ca206a006043f8c400610000be206a0064'
        '43f8c500610000b2206a' '006843f8c600610000a6206a006c43f8c7006100009a'
        '206a007043f8c8006100' '009a206a007443f8cc0061000082206a007843f8e710'
        '6100009a4278e70041f8e818303c007720fcffffffff51c8fff8206a007c43f8ea88'
        '61000084206a008043f8f0006100009431fc00fff37631fc0000efd431fcffff9f00'
        '303c00ff41f8a150429851c8fffc4e75'),
    0x004026: (
        '303c000922d851c8fffc4e75303c002722d851c8fffc4e75'
        '303c007f22d851c8fffc4e75303c003f22d851c8fffc4e75'
        '303c00ff22d851c8fffc4e75303c001322d851c8fffc4e75'
        '303c000722d851c8fffc4e75303c00ff12a8000113500001136800020002'
        '5648564951c8ffec4e75303c00ff32180c41ffff67000006044100b812c151c8ffee4e75'),
    0x009390: '41f8c60043f8c00045f8be00303c00ff3219d25a343c000147fa0014b25b65000006524260f610c251c8ffe64e75',
}

# Labels are evidence, not extra editable fields. Widths and unknown bits are
# never inferred from these human-facing aliases or canonical value statistics.
MEANINGS = {
    'ram_f428': ('probable', 'city force ID', '003E5E..003E66; prior static-data report'),
    'ram_f460': ('probable', 'city primary officer ID', '003E68..003E72; prior static-data report'),
    'ram_e640': ('probable', 'force primary officer ID', '003E74..003E84; prior static-data report'),
    'ram_e000': ('confirmed', 'city gold', 'transport_flow; 00E790..00E822'),
    'ram_e0a0': ('confirmed', 'city food/rice', 'transport_flow; 00E790..00E822'),
    'ram_e1e0': ('confirmed', 'low word development; high word unknown', 'static_data; domestic_flow'),
    'ram_e320': ('confirmed', 'low word welfare; high word unknown', 'static_data; domestic_flow'),
    'ram_e5a0': ('confirmed', 'low word defense; high word unknown', 'static_data; domestic_flow'),
    'ram_e460': ('confirmed', 'city long used by count consumer; formal label unknown', 'domestic_remaining; 00A72A'),
    'ram_b400': ('confirmed', 'training arithmetic input; formal label unknown', 'gameplay_rules'),
    'ram_b600': ('confirmed', 'intelligence word', 'static_data; domestic_flow'),
    'ram_b800': ('confirmed', 'troop capacity base, multiplied by 100 by consumer', 'gameplay_rules'),
    'ram_be00': ('confirmed', 'progression input word', '009398..0093A2'),
    'ram_c000': ('confirmed', 'progression/growth word', '009394..0093A2; gameplay_rules'),
    'ram_c200': ('confirmed', 'virtue byte', 'static_data; domestic_flow'),
    'ram_c300': ('confirmed', 'education-grown byte; formal label unknown', 'domestic_extended; 00E592..00E78F'),
    'ram_c400': ('confirmed', 'aggregate/average input byte; formal label unknown', 'save_data'),
    'ram_c500': ('confirmed', 'training-grown byte; formal label unknown', 'gameplay_rules'),
    'ram_c600': ('confirmed', 'source byte later replaceable by threshold-derived value', '009390..0093BC'),
    'ram_c700': ('confirmed', 'low 3 bits class/office; bit 4 command-set; remaining bits unknown', 'domestic_remaining; 00E4A4'),
    'ram_c800': ('confirmed', 'actual troop count', 'gameplay_rules'),
    'ram_cc00': ('confirmed', 'assigned city ID', 'static_data; gameplay_rules'),
    'ram_e710': ('confirmed', 'relationship bit row; source need not be symmetric', 'diplomacy_flow; 00EC16..00EC5A'),
    'ram_ea88': ('confirmed', '3 equipment category source bytes; category names unknown', '00407A..004094; 00FC36..00FC54'),
    'ram_f000': ('unknown', 'full source word; human-facing purpose unproved', '004096..0040AE confirms transform only'),
}
UNKNOWN_COMPONENTS = {
    **{name: ('unknown_high_word',) for name in SPLIT_WORDS},
    **{name: ('formal gameplay/UI field name',) for name in
       ('ram_e460','ram_b400','ram_be00','ram_c000','ram_c300','ram_c400','ram_c500','ram_c600')},
    'ram_c700': ('bit 3 and bits 5..7', 'formal gameplay/UI field name'),
    'ram_ea88': ('equipment category names',),
}


def sha(data): return hashlib.sha256(data).hexdigest()
def dump(value): return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode()
def keys(value, wanted):
    if type(value) is not dict or set(value) != set(wanted): raise ValueError('object fields changed')
def integer(value, maximum, name='field'):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError(f'{name}: strict unsigned integer outside 0..{maximum}')
    return value
def fixed_list(value, count):
    if type(value) is not list or len(value) != count: raise ValueError('fixed record count changed')
    return value
def exact(value, expected):
    if type(value) is not type(expected) or value != expected: raise ValueError('fixed identity changed')


def check_anchors(rom):
    for address, raw in ANCHORS.items():
        if rom[address:address+len(raw)//2] != bytes.fromhex(raw):
            raise ValueError(f'consumer instruction changed at {address:06X}')


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != legacy.CANONICAL_SIZE or sha(rom) != legacy.CANONICAL_SHA256:
        raise ValueError('canonical ROM identity mismatch')
    check_anchors(rom)


def selector_address_raw(index_word):
    """003E54..003E5A effective bus address, not a 0..2 runtime domain proof.

    LSL.W wraps; D0.W indexing sign-extends. The original CPU reads a long at
    this address without checking that it is in the three-entry directory.
    """
    word = (integer(index_word, 65535, 'selector low word') << 2) & 65535
    return (DIRECTORY + (word if word < 32768 else word-65536)) & 0xFFFFFF


def decode_field(spec, raw):
    if spec.table_id in SPLIT_WORDS:
        return {'unknown_high_word': int.from_bytes(raw[:2], 'big'),
                'value_low_word': int.from_bytes(raw[2:], 'big')}
    if spec.table_id == 'ram_ea88':
        return {f'source_byte{i}': raw[i] for i in range(3)}
    return int.from_bytes(raw, 'big')


def encode_field(spec, value):
    if spec.table_id in SPLIT_WORDS:
        keys(value, ('unknown_high_word', 'value_low_word'))
        return b''.join(integer(value[k], 65535, k).to_bytes(2, 'big')
                        for k in ('unknown_high_word', 'value_low_word'))
    if spec.table_id == 'ram_ea88':
        names = tuple(f'source_byte{i}' for i in range(3)); keys(value, names)
        return bytes(integer(value[k], 255, k) for k in names)
    return integer(value, (1 << (8*spec.source_record_width))-1, spec.table_id).to_bytes(spec.source_record_width, 'big')


def extract(rom):
    verify_rom(rom)
    if rom[DIRECTORY:DIRECTORY+12] != b''.join(b.to_bytes(4, 'big') for b in BASES):
        raise ValueError('canonical directory changed')
    scenarios = []
    for ident, base in zip(IDS, BASES):
        wanted = b''.join(ADDRESSES[f'{ident}.{s.table_id}'].to_bytes(4, 'big') for s in SPECS)
        if rom[base:base+DESCRIPTOR_SIZE] != wanted: raise ValueError('canonical descriptor changed')
        scenario = {'id': ident, 'descriptor_targets': {s.table_id: f'{ident}.{s.table_id}' for s in SPECS}}
        for group, count, first in GROUPS:
            scenario[group] = [{'id': i+first, **{
                s.table_id: decode_field(s, rom[ADDRESSES[f'{ident}.{s.table_id}']+i*s.source_record_width:
                    ADDRESSES[f'{ident}.{s.table_id}']+(i+1)*s.source_record_width])
                for s in GROUP_SPECS[group]}} for i in range(count)]
        scenarios.append(scenario)
    return {'schema_version': 1, 'format': FORMAT, 'canonical_rom_sha256': legacy.CANONICAL_SHA256,
            'directory_targets': list(IDS), 'scenarios': scenarios}


def encode_blocks(assets):
    """Encode all 103 physical intervals from fields alone: no ROM/file fallback.

    Known descriptor aliases and SAME-KIND table aliases are editor-supported.
    This restriction is not an original CPU pointer-domain check. Even unselected
    physical records remain represented once, with stable IDs and fixed addresses.
    """
    keys(assets, ('schema_version', 'format', 'canonical_rom_sha256', 'directory_targets', 'scenarios'))
    exact(assets['schema_version'], 1); exact(assets['format'], FORMAT)
    exact(assets['canonical_rom_sha256'], legacy.CANONICAL_SHA256)
    directory = bytearray()
    for target in fixed_list(assets['directory_targets'], 3):
        if type(target) is not str or target not in IDS: raise ValueError('unknown directory target')
        directory.extend(BASES[IDS.index(target)].to_bytes(4, 'big'))
    result = [{'id': 'scenario_directory', 'start': DIRECTORY, 'end': DIRECTORY+12,
               'role': 'scenario_descriptor_pointers', 'data': bytes(directory)}]
    for ident, base, scenario in zip(IDS, BASES, fixed_list(assets['scenarios'], 3)):
        keys(scenario, ('id', 'descriptor_targets', 'cities', 'forces', 'officers')); exact(scenario['id'], ident)
        targets = scenario['descriptor_targets']; keys(targets, TABLE_IDS)
        pointer_bytes = bytearray()
        for spec in SPECS:
            target = targets[spec.table_id]
            if type(target) is not str or target not in tuple(f'{i}.{spec.table_id}' for i in IDS):
                raise ValueError('unknown or cross-kind table target')
            pointer_bytes.extend(ADDRESSES[target].to_bytes(4, 'big'))
        result.append({'id': ident+'_descriptor', 'start': base, 'end': base+DESCRIPTOR_SIZE,
                       'role': 'scenario_table_pointers', 'data': bytes(pointer_bytes)})
        encoded = {s.table_id: bytearray() for s in SPECS}
        for group, count, first in GROUPS:
            specs = GROUP_SPECS[group]
            for i, record in enumerate(fixed_list(scenario[group], count)):
                keys(record, ('id', *(s.table_id for s in specs))); exact(record['id'], i+first)
                for spec in specs: encoded[spec.table_id].extend(encode_field(spec, record[spec.table_id]))
        for spec in SPECS:
            raw = bytes(encoded[spec.table_id]); start = ADDRESSES[f'{ident}.{spec.table_id}']
            if len(raw) != spec.source_length: raise AssertionError('fixed table length changed')
            result.append({'id': ident+'_'+spec.table_id, 'start': start, 'end': start+len(raw),
                           'role': 'scenario_'+spec.table_id, 'data': raw})
    result.sort(key=lambda r:r['start'])
    if len(result) != 103 or sum(r['end']-r['start'] for r in result) != EDITABLE_BYTES:
        raise AssertionError('physical source inventory changed')
    if any(a['end'] > b['start'] for a, b in zip(result, result[1:])): raise AssertionError('source overlap')
    return result


def blocks(rom, assets):
    """Integration API: identity-guard the base, then encode fields independently."""
    verify_rom(rom)
    return encode_blocks(assets)


def rebuild(rom, assets):
    verify_rom(rom); result = bytearray(rom)
    for row in encode_blocks(assets): result[row['start']:row['end']] = row['data']
    return bytes(result)


def runtime_tables(assets, slot):
    """Pure table projection for a supported directory slot; NOT full RAM state.

    Does not simulate stack, IRQs, other clears, EFD4 reset, later 009390 C600
    derivation, or edited gameplay. The original helpers are shared pure code.
    """
    encoded = {r['id']: r for r in encode_blocks(assets)}
    integer(slot, 2, 'editor directory slot')
    scenario = assets['scenarios'][IDS.index(assets['directory_targets'][slot])]
    result = []
    for spec in SPECS:
        source = scenario['descriptor_targets'][spec.table_id]
        row = encoded[source.replace('.', '_')]
        result.append({'table_id': spec.table_id, 'source_target': source, 'ram_start': spec.ram_start,
            'ram_end': spec.ram_start+spec.runtime_length, 'transform': spec.transform,
            'data': legacy.runtime_bytes(spec, row['data'])})
    return result


def field_semantics():
    return {s.table_id: {'layout_confidence': 'confirmed', 'purpose_confidence': MEANINGS.get(s.table_id,
        ('unknown',))[0], 'meaning': MEANINGS.get(s.table_id, ('unknown', 'unknown field; address-based source'))[1],
        'evidence': MEANINGS.get(s.table_id, ('unknown', '', '003E54..0040AE loader only'))[2],
        'purpose_scope': 'Only the described subfield or consumer relation; not unknown components.',
        'unknown_components': list(UNKNOWN_COMPONENTS.get(s.table_id,
            ('human-facing purpose',) if s.table_id not in MEANINGS or MEANINGS[s.table_id][0]=='unknown' else ())),
        'source_width': s.source_record_width, 'runtime_width': s.runtime_record_width,
        'record_count': s.record_count, 'transform': s.transform} for s in SPECS}


def runtime_preview(assets):
    return {'observation_only': True, 'natural_selection': False, 'full_ram_state': False,
        'later_c600_derivation_included': False,
        'slots': [{'slot': slot, 'descriptor_target': assets['directory_targets'][slot], 'tables': [
            {k:v for k,v in row.items() if k != 'data'} | {'sha256': sha(row['data']), 'byte_length':len(row['data'])}
            for row in runtime_tables(assets, slot)]} for slot in range(3)]}


def manifest(rom, assets=None):
    """Canonical evidence seal, deliberately separate from editable validation."""
    canonical = extract(rom)
    if assets is not None:
        encode_blocks(assets)
        if assets != canonical: raise ValueError('canonical manifest cannot seal edited assets')
    rows = encode_blocks(canonical)
    return {'schema_version': 1, 'format': FORMAT, 'canonical_rom_sha256': sha(rom),
        'editable_bytes': EDITABLE_BYTES, 'physical_intervals': 103, 'scenario_count': 3,
        'source_tables': 99, 'descriptor_bytes': 396, 'directory_bytes': 12, 'table_bytes': 31464,
        'owners': [], 'ownership_bytes_added': 0, 'complete_indirect_domains_added': 0,
        'source_fields_sha256': sha(dump(canonical)), 'field_semantics': field_semantics(),
        'anchors': [{'start': a, 'end': a+len(raw)//2, 'raw_hex': raw, 'sha256': sha(bytes.fromhex(raw))}
                    for a, raw in ANCHORS.items()],
        'intervals': [{k:r[k] for k in ('id','start','end','role')} | {'sha256':sha(r['data']),
            'previously_owned': True, 'layout_confidence': 'confirmed'} for r in rows],
        'boundaries': [
            'All 31872 bytes already owned as scenario_data; no new primary ownership.',
            'assets.json alone is editable; schema, manifest and runtime preview are derived evidence.',
            'Full u8/u16/u32 source fields retained; no canonical-value or gameplay-cap clamp.',
            'Directory and same-kind table aliases are bounded editor policy, not CPU pointer domains.',
            'EA88 source triples map to RAM [source_byte1, source_byte0, source_byte2].',
            'F000 source FFFF maps to FF; other words map to u8(word-B8); all source bits retained.',
            'C600 source exists despite later threshold derivation at 009390..0093BC.',
            'Runtime preview is a static table projection, not full RAM or natural execution proof.',
            'E710 physical order differs from descriptor order; scenario_2 E640 crosses bank08/09.',
            'Unknown field purposes and unknown high words are not zero padding or invented labels.',
            'Byte-exact edited encoding does not establish playable or display-safe edited data.']}


def render_bundle(rom):
    from .schema import schema
    assets = extract(rom)
    return {'assets.json': dump(assets), 'assets.schema.json': dump(schema()),
            'manifest.json': dump(manifest(rom)), 'runtime_preview.json': dump(runtime_preview(assets)),
            'README.md': (
                '# Scenario fixed-field source\n\n'
                'Confirmed layout: 3 scenarios, 99 tables, 103 physical intervals, 31872 bytes.\n'
                'New primary ownership: 0. Complete indirect domains added: 0.\n\n'
                'Only assets.json is editable. IDs, row order, addresses and widths are fixed.\n'
                'City IDs are 1..40; force IDs 0..15; officer IDs 0..255. These are record\n'
                'identities, not CPU-imposed value bounds. All numeric fields retain full width.\n'
                'Three city long fields split unknown_high_word and value_low_word.\n'
                'EA88 preserves source_byte0/1/2; runtime order is 1/0/2. F000 preserves\n'
                'all 16 source bits: FFFF -> FF, otherwise (word-B8)&FF.\n'
                'Directory targets and same-kind table targets may alias existing stable IDs.\n'
                'Physical source tables remain singly represented even when not selected.\n'
                'Runtime preview contains derived table hashes, not a second source or full RAM.\n'
                'It excludes other loader clears, later C600 derivation and natural-path claims.\n'
                'Field purpose confidence is separate from confirmed representation layout.\n'
                'See ../SCENARIO_BUILD.md for consumer anchors, source policy and limits.\n'
            ).encode()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('export', 'verify', 'import'))
    parser.add_argument('--rom', type=Path, default=DEFAULT_ROM)
    parser.add_argument('--assets', type=Path, default=DEFAULT_ASSETS)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    read = lambda p: af._read(af.safe_path(p, regular_input=True), 16*1024*1024)
    rom = read(args.rom); verify_rom(rom)
    if args.command == 'export':
        if args.output is None: raise ValueError('--output required')
        print(publish(render_bundle(rom), args.output, [args.rom])); return
    assets = af.load_assets(read(args.assets)); image = rebuild(rom, assets)
    summary = {'canonical_exact':image == rom, 'sha256':sha(image), 'editable_bytes':EDITABLE_BYTES,
               'changed_bytes':sum(a != b for a,b in zip(image,rom))}
    if args.command == 'verify': print(json.dumps(summary)); return
    if args.output is None: raise ValueError('--output required')
    print(publish({'rebuilt.bin':image, 'manifest.json':dump(summary)}, args.output, [args.rom,args.assets]))


if __name__ == '__main__': main()
