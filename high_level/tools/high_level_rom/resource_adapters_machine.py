"""Independent fields for audio machine tables and seven LSB-first bitmaps.

Source arrays contain data, not executable instruction dumps. Fixed metadata
helpers from existing schemas are disclosed dependencies; their ROM validators
and extract/rebuild entry points are never called. Catalog limits apply to the
editor only and must not be mistaken for original CPU selector clamps.
"""
from __future__ import annotations

from tools.resource_metadata import compare_fixed_fields

from tools.audio_frequency_fields import codec as frequency
from tools.fm_instrument_alias_fields import codec as fm_alias
from tools.audio_root_resources import codec as audio_root
from tools.audio_dispatch_fields import codec as dispatch
from tools.z80_startup_seed_fields import codec as startup
from tools.scaled_bitmaps import scaled_bitmaps as bitmap
from tools.vdp_word_streams import format as fmt
from .resource_adapters import block, coalesced_spans, fixed_list, uint


def _fixed(row, fixed, editable, label):
    compare_fixed_fields(row, fixed, editable, label)


def _finish(rows, contract, expected):
    rows.sort(key=lambda row: row['start'])
    spans = coalesced_spans(rows)
    if sum(len(row['data']) for row in rows) != expected:
        raise ValueError('independent machine-data allocation differs')
    if 'spans' in contract and spans != contract['spans']:
        raise ValueError('persisted machine-data geometry differs')
    return rows


def audio_frequency_fields(fields, contract):
    """Full PSG/FM LE16 WORDs; no chip-range normalization or note clamp."""
    _fixed(fields, frequency.metadata(), ('tables',), 'frequency package')
    rows = []
    for row, spec in zip(fixed_list(fields['tables'], 2, 'frequency tables'), frequency.TABLES):
        fixed = frequency.topology(spec)
        _fixed(row, fixed, ('WORDs',), 'frequency table')
        data = b''.join(uint(value, 65535, 'full frequency WORD').to_bytes(2, 'little')
                        for value in fixed_list(row['WORDs'], spec[2], 'frequency entries'))
        rows.append(block(fixed['physical_ROM_start'], data, fixed['id'],
                          'conditional_Z80_frequency_full_LE16_WORDs'))
    return _finish(rows, contract, frequency.EDITABLE_BYTES)


def fm_instrument_alias_fields(fields, contract):
    """126 conditional FM records; preserve full register and TL BYTE bits."""
    _fixed(fields, fm_alias.metadata(), ('records',), 'FM alias package')
    data = bytearray()
    for row, index in zip(fixed_list(fields['records'], 126, 'conditional FM records'), range(2, 128)):
        _fixed(row, fm_alias.record_fixed(index),
               ('register_payload_BYTEs', 'total_level_source_BYTEs'), 'FM record')
        for key, count in (('register_payload_BYTEs', 21), ('total_level_source_BYTEs', 4)):
            data.extend(uint(value, 255, 'full FM source BYTE')
                        for value in fixed_list(row[key], count, key))
    rows = [block(fm_alias.START, bytes(data), 'rom_FE31D_conditional_FM_source_aliases',
                  'conditional_25_BYTE_FM_register_source_aliases')]
    return _finish(rows, contract, fm_alias.EDITABLE_BYTES)


def audio_root_resources(fields, contract):
    """Six roots, a shared SFX reference and 63 priority bit-field records."""
    c = audio_root
    _fixed(fields, c.metadata(), ('roots', 'secondary_sfx_pointer', 'priorities'), 'audio roots')
    roots = bytearray()
    for index, (row, role, canonical) in enumerate(zip(
            fixed_list(fields['roots'], 6, 'root catalog'), c.ROLES, c.TARGETS)):
        fixed = dict(id=c.ident(c.ROOT_START + 2 * index), slot=2 * index, role=role)
        _fixed(row, fixed, ('z80_target',), 'root record')
        target = uint(row['z80_target'], 65535, 'LE16 root target')
        if target not in ((0x1000, 0x1020) if index in (1, 3) else (canonical,)):
            raise ValueError('root reference leaves existing same-reader editor catalog')
        roots.extend(target.to_bytes(2, 'little'))
    row = fields['secondary_sfx_pointer']
    _fixed(row, dict(id=c.ident(c.SECONDARY_START), z80_address=0x1020), ('target',), 'secondary SFX')
    catalog = contract['sfx_header_catalog']
    if type(row['target']) is not str or row['target'] not in catalog:
        raise ValueError('secondary SFX target lacks an owned header ID')
    pointer = uint(catalog[row['target']], 65535, 'SFX logical address').to_bytes(2, 'little')
    priorities = bytearray()
    for index, row in enumerate(fixed_list(fields['priorities'], 63, 'priority allocation')):
        _fixed(row, dict(id=c.ident(c.PRIORITY_START + index), command=0x81 + index),
               ('unconditional_selection', 'priority'), 'priority record')
        flag = row['unconditional_selection']
        if type(flag) is not bool:
            raise ValueError('priority flag must be an exact Boolean')
        priorities.append(uint(row['priority'], 127, 'priority low seven bits') | (int(flag) << 7))
    rows = [block(c.SECONDARY_START, pointer, c.ident(c.SECONDARY_START), 'candidate_local_z80_secondary_sfx_LE16'),
            block(c.ROOT_START, bytes(roots), c.ident(c.ROOT_START), 'candidate_banked_z80_root_LE16'),
            block(c.PRIORITY_START, bytes(priorities), c.ident(c.PRIORITY_START), 'candidate_command_arbitration_priority')]
    return _finish(rows, contract, c.EDITABLE_BYTES)


def audio_dispatch_fields(fields, contract):
    """LE16 code references checked against persisted own-source boundaries."""
    _fixed(fields, dispatch.metadata(), ('tables',), 'audio dispatch')
    boundaries = {uint(value, 65535, 'owned Z80 instruction boundary')
                  for value in contract['owned_driver_instruction_boundaries']}
    if not boundaries:
        raise ValueError('dispatch requires explicit owned code-source boundaries')
    rows = []
    for row, spec in zip(fixed_list(fields['tables'], 3, 'dispatch tables'), dispatch.TABLES):
        fixed = dispatch.table_meta(*spec)
        _fixed(row, fixed, ('target_RAM_WORDs',), 'dispatch table')
        raw = bytearray()
        for target in fixed_list(row['target_RAM_WORDs'], spec[2], 'dispatch entries'):
            target = uint(target, 65535, 'Z80 code target')
            if target not in boundaries:
                raise ValueError('dispatch target lacks a declared own instruction boundary')
            raw.extend(target.to_bytes(2, 'little'))
        rows.append(block(fixed['physical_ROM_start'], bytes(raw), fixed['id'],
                          'Z80_RAM_handler_pointer_LE16_' + spec[3]))
    return _finish(rows, contract, dispatch.EDITABLE_BYTES)


def z80_startup_seed_fields(fields, contract):
    """The actual 13-BYTE copy source; retain unknown field and complete bits."""
    _fixed(fields, startup.metadata(), ('seeds',), 'startup seeds')
    data = bytearray()
    for row, spec in zip(fixed_list(fields['seeds'], len(startup.FIELDS), 'seed fields'), startup.FIELDS):
        _fixed(row, startup.topology(spec), ('value',), 'seed')
        width = spec[1]
        data.extend(uint(row['value'], (1 << (8 * width)) - 1, 'full seed scalar').to_bytes(width, 'little'))
    rows = [block(startup.START, bytes(data), 'rom_0069AA_Z80_startup_RAM_seeds',
                  'original_copied_Z80_RAM_startup_seed_scalars')]
    return _finish(rows, contract, startup.EDITABLE_BYTES)


def scaled_bitmaps(fields, contract):
    """Seven editable 32x32 one-bit images: row WORDs are little-endian."""
    c = bitmap
    _fixed(fields, dict(schema_version=1, format=c.FORMAT), ('directory', 'bitmaps'), 'scaled bitmap package')
    directory = fields['directory']
    _fixed(directory, dict(address=c.DIRECTORY), ('targets',), 'bitmap directory')
    catalog = dict(zip(c.IDS, c.SOURCES))
    targets = fixed_list(directory['targets'], 7, 'bitmap references')
    if any(type(target) is not str or target not in catalog for target in targets):
        raise ValueError('bitmap reference outside physical source catalog')
    rows = [block(c.DIRECTORY, b''.join(catalog[target].to_bytes(4, 'big') for target in targets),
                  'scaled_bitmap_directory', 'absolute_long_bitmap_directory')]
    for row, ident, start in zip(fixed_list(fields['bitmaps'], 7, 'bitmap sources'), c.IDS, c.SOURCES):
        _fixed(row, dict(id=ident, start=start), ('rows',), 'bitmap')
        data = b''.join(uint(bits, 0xFFFFFFFF, 'full row bitfield').to_bytes(4, 'little')
                        for bits in fixed_list(row['rows'], 32, 'bitmap bit rows'))
        rows.append(block(start, data, ident, 'bitmap_32x32_1bpp_lsb_rows'))
    return _finish(rows, contract, 924)


ENCODERS = dict(audio_frequency_fields=audio_frequency_fields,
                fm_instrument_alias_fields=fm_instrument_alias_fields,
                audio_root_resources=audio_root_resources,
                audio_dispatch_fields=audio_dispatch_fields,
                z80_startup_seed_fields=z80_startup_seed_fields,
                scaled_bitmaps=scaled_bitmaps)


def geometry_contract(resource_id, canonical_fields, *, sfx_header_catalog=None, driver_boundaries=None):
    """Offline topology from own typed source and code-source metadata only."""
    if resource_id not in ENCODERS:
        raise ValueError('explicit independently owned machine-data resource required')
    contract = dict(adapter=resource_id, adapter_module=__name__, format=canonical_fields['format'],
                    confidence='preserved_original_role_confidence',
                    semantic_meaning='field_encoding_not_natural_domain_acceptance',
                    limits=['fixed editor geometry is not an original CPU selector clamp',
                            'legacy pure metadata helpers remain disclosed dependencies',
                            'no hardware, playback, scale or natural-gameplay acceptance'])
    if resource_id == 'audio_root_resources':
        if type(sfx_header_catalog) is not dict or not sfx_header_catalog:
            raise ValueError('owned typed-audio SFX header catalog required')
        contract['sfx_header_catalog'] = {ident: uint(address, 65535, 'SFX header logical address')
                                          for ident, address in sfx_header_catalog.items()}
        contract['catalog_provenance'] = 'own audio_build.definitions.sfx IDs/z80_address; no ROM extraction'
    if resource_id == 'audio_dispatch_fields':
        if type(driver_boundaries) is not list or not driver_boundaries:
            raise ValueError('owned business-source driver instruction boundaries required')
        contract['owned_driver_instruction_boundaries'] = sorted(set(
            uint(value, 65535, 'own-source boundary') for value in driver_boundaries))
        contract['catalog_provenance'] = 'high_level_audio_engine generated driver instruction_rows; no ROM/census'
        contract['limits'].append('64 confirmed dispatch bytes and24 probable prefix bytes retain separate table confidence')
    if resource_id == 'fm_instrument_alias_fields':
        contract['limits'].append('first two FM records remain shared audio_build authority; FE F6B tail stays unknown, not padding')
    if resource_id == 'scaled_bitmaps':
        contract['limits'].append('LE32 LSB-first pixels preserved; zero scale trap and nonideal fixed-point resampling remain in code')
    rows = ENCODERS[resource_id](canonical_fields, contract)
    contract.update(spans=coalesced_spans(rows), bytes=sum(len(row['data']) for row in rows), physical_blocks=len(rows))
    return contract
