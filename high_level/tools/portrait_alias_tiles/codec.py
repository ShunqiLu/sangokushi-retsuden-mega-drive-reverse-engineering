"""54 nonzero tiles actually selected by original full-WORD index aliases.

Original source plans, not pixel resemblance, establish this 1728-byte scope.
Witnesses have all60 tile reads inside ROM, but their natural entry domain is
unknown. Pixels alone are editable; original token aliases are evidence, not
duplicated source authority. Diagnostics always read the current whole image.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared
from tools.bank08_display_resources import codec as pixels_format
from tools.portrait_graphics import portrait_graphics as original_format

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
OUTPUT_ROOT = ROOT / "build/portrait_alias_tiles"
FORMAL_ROOT = ROOT / "analysis/portrait_alias_tiles/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
EDITABLE_BYTES = 1728
FORMAT = "g5510-constructed-portrait-WORD-alias-pixel-fields-v1"
MAX_JSON = 2 * 1024 * 1024
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
ENHANCED_PATH = "analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv"
ENHANCED_SHA256 = reference_value(__name__, 'ENHANCED_SHA256')
# Physical tile, first all60-ROM-valid original D0.W witness, path, item,
# original token address and full original token WORD (never normalized).
WITNESSES = (
    (0xB64BA, 0x5D3, "secondary8", 6, 0xBA0D6, 0x1),
    (0xB64DA, 0x10A, "secondary4", 2, 0xB5BEE, 0x2),
    (0xB64FA, 0x247, "secondary8", 4, 0xB6812, 0x3),
    (0xB651A, 0x103, "secondary4", 1, 0xB5BB4, 0x4),
    (0xB653A, 0x600, "secondary8", 6, 0xBA3A6, 0x5),
    (0xB655A, 0x107, "secondary4", 0, 0xB5BD2, 0x6),
    (0xB847A, 0x527, "secondary8", 0, 0xB960A, 0xFF),
    (0xBA51A, 0x10B, "secondary4", 1, 0xB5BF4, 0x204),
    (0xBCD1A, 0x349, "secondary8", 6, 0xB7836, 0x344),
    (0xC047A, 0x267, "secondary8", 3, 0xB6A10, 0xDCFF),
    (0xC141A, 0x219, "primary", 21, 0xAAD24, 0x57C),
    (0xC145A, 0x218, "primary", 33, 0xAACDC, 0x57E),
    (0xC147A, 0x218, "primary", 34, 0xAACDE, 0x57F),
    (0xC14BA, 0x218, "primary", 10, 0xAACAE, 0x581),
    (0xC14FA, 0x21A, "primary", 41, 0xAADAC, 0x583),
    (0xC151A, 0x52C, "secondary8", 1, 0xB965C, 0xE584),
    (0xC153A, 0x21A, "primary", 31, 0xAAD98, 0x585),
    (0xC155A, 0x312, "secondary8", 6, 0xB74C6, 0x8586),
    (0xC157A, 0x525, "secondary8", 1, 0xB95EC, 0xCD87),
    (0xC159A, 0x39B, "secondary8", 5, 0xB7D54, 0x8588),
    (0xC15BA, 0x306, "secondary8", 7, 0xB7408, 0x8589),
    (0xC353A, 0x459, "secondary8", 2, 0xB892E, 0xEE85),
    (0xC355A, 0x145, "primary", 12, 0xB5D92, 0x686),
    (0xC359A, 0x2FE, "secondary8", 3, 0xB7380, 0xEE88),
    (0xC35BA, 0x458, "secondary8", 6, 0xB8926, 0xEE89),
    (0xC35DA, 0x1AA, "secondary4", 0, 0xB60EA, 0xE8A),
    (0xC361A, 0x140, "primary", 1, 0xB5B9C, 0x68C),
    (0xC365A, 0x1CE, "secondary4", 0, 0xB620A, 0xE8E),
    (0xC367A, 0x3F9, "secondary8", 1, 0xB832C, 0x568F),
    (0xC369A, 0x2F7, "secondary8", 6, 0xB7316, 0xEE90),
    (0xC373A, 0x313, "secondary8", 2, 0xB74CE, 0x5695),
    (0xC375A, 0x2AF, "secondary8", 2, 0xB6E8E, 0xFE96),
    (0xC377A, 0x34E, "secondary8", 5, 0xB7884, 0x6697),
    (0xC379A, 0x2AF, "secondary8", 0, 0xB6E8A, 0xFE98),
    (0xC37DA, 0x261, "secondary4", 0, 0xB66A2, 0xFE9A),
    (0xC387A, 0x399, "secondary8", 5, 0xB7D34, 0x969F),
    (0xC3D5A, 0x150, "primary", 24, 0xB61CA, 0x6C6),
    (0xC3D9A, 0x566, "secondary8", 6, 0xB9A06, 0xEEC8),
    (0xC3E1A, 0x46C, "secondary8", 2, 0xB8A5E, 0xC6CC),
    (0xC3E3A, 0x3E4, "secondary8", 4, 0xB81E2, 0xEECD),
    (0xC3E5A, 0x14B, "primary", 33, 0xB5FFC, 0x6CE),
    (0xC3F3A, 0x346, "secondary8", 6, 0xB7806, 0xEED5),
    (0xC55DA, 0x46A, "secondary8", 4, 0xB8A42, 0x878A),
    (0xC615A, 0x650, "secondary8", 6, 0xBA8A6, 0x77E6),
    (0xC6D1A, 0x6B4, "secondary8", 7, 0xBAEE8, 0x3044),
    (0xC6D5A, 0x14A, "primary", 44, 0xB5FB2, 0x846),
    (0xCA47A, 0x7EA, "secondary8", 6, 0xBC246, 0x21FF),
    (0xCC83A, 0x20F, "secondary8", 0, 0xB648A, 0x1B1D),
    (0xCC9FA, 0x20B, "secondary8", 5, 0xB6454, 0x1B2B),
    (0xCCA5A, 0x4A0, "secondary8", 0, 0xB8D9A, 0x432E),
    (0xCCA7A, 0x7E7, "secondary8", 7, 0xBC218, 0x232F),
    (0xCCA9A, 0x262, "secondary8", 3, 0xB69C0, 0x3330),
    (0xCCABA, 0x337, "secondary8", 0, 0xB770A, 0xE331),
    (0xCDFFA, 0x3F0, "secondary8", 3, 0xB82A0, 0xDBDB),
)
ZERO_READ_TILES = (0xBA49A, 0xBE49A, 0xC049A, 0xC249A, 0xC449A, 0xC737A, 0xC849A, 0xCA49A, 0xCC49A)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields, safe_path = shared.load_fields, shared.safe_path
read_bounded, put = shared.read_bounded, shared.put
tile_pixels, tile_bytes = pixels_format.tile_pixels, pixels_format.tile_bytes


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical bytes, size and ROM SHA required")
    original_format.verify_rom(rom)


def read_plan(image, D0_LONG):
    """Ordered original ROM source projection, from original or edited image.

    No RAM/stack, 24-bit bus, VDP presentation or natural-domain simulation.
    First unknown external source stops explicitly rather than supplying zeros.
    """
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("complete bytes image required for alias source reads")
    uint(D0_LONG, 0xFFFFFFFF, "full D0 register bits")
    layout = original_format.address_plan(D0_LONG)
    records = []
    for path, _, count in original_format.TABLES:
        for item in range(count):
            address = layout['tables'][path] + item * 2
            if not 0 <= address <= ROM_SIZE - 2:
                return dict(status="out_of_ROM_token", D0_WORD=D0_LONG & 65535, records=records, boundary=address)
            token = int.from_bytes(image[address:address + 2], "big")
            sources = original_format.token_reads(token, path)
            if any(not 0 <= source <= ROM_SIZE - 4 for source in sources):
                return dict(status="out_of_ROM_tile_source", D0_WORD=D0_LONG & 65535, records=records,
                    boundary=dict(path=path, item=item, token_address=address, token_WORD=token, source_LONG_addresses=sources))
            records.append(dict(path=path, item=item, token_address=address, token_WORD=token,
                source_LONG_addresses=sources,
                source_LONGs=[int.from_bytes(image[p:p + 4], "big") for p in sources]))
    selector_address = layout['selector_address']
    if not 0 <= selector_address < ROM_SIZE:
        return dict(status="out_of_ROM_selector", D0_WORD=D0_LONG & 65535, records=records, boundary=selector_address)
    selector = image[selector_address]
    palette = original_format.PALETTE_BIAS + selector * 32
    if not 0 <= palette <= ROM_SIZE - 32:
        return dict(status="out_of_ROM_palette", D0_WORD=D0_LONG & 65535, records=records, boundary=palette)
    return dict(status="complete_ROM_source_plan", D0_WORD=D0_LONG & 65535, records=records,
        selector_address=selector_address, selector_BYTE=selector, palette_start=palette,
        palette_LONGs=[int.from_bytes(image[p:p + 4], "big") for p in range(palette, palette + 32, 4)],
        natural_execution=False, CPU_execution=False)


def verified_witness(rom, spec):
    tile, index, path, item, token_address, token = spec
    plan = read_plan(rom, index)
    if plan['status'] != 'complete_ROM_source_plan' or len(plan['records']) != 60:
        raise ValueError("original witness has an earlier or later external ROM source boundary")
    row = next(record for record in plan['records'] if record['path'] == path and record['item'] == item)
    if row['token_address'] != token_address or row['token_WORD'] != token or row['source_LONG_addresses'] != list(range(tile, tile + 32, 4)):
        raise ValueError("pinned full-token original alias witness differs")
    if not any(rom[tile:tile + 32]) or tile in original_format.SELECTED_TILES:
        raise ValueError("new catalog contains a zero tile or old editor source")
    return dict(D0_WORD=index, path=path, item=item, token_address=token_address,
        token_WORD=token, source_LONG_addresses=row['source_LONG_addresses'],
        complete60_ROM_sources=True, natural_domain="unknown", original_ROM_only=True)


def metadata():
    return dict(format=FORMAT, confidence="candidate", source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        evidence=dict(source="full-WORD original indexed ROM reads, not unreferenced pixel resemblance",
            consumer=dict(start=0x661D4, end=0x662E4, bytes=272, sha256=original_format.CONSUMER_SHA),
            older_ledger=dict(path=ENHANCED_PATH, sha256=ENHANCED_SHA256),
            frozen_raw_layout=dict(id=LAYOUT_ID, all_emitted_bytes_raw=True, old_typed_overlap_bytes=0),
            callers=[dict(start=pc, bytes=raw, precondition=claim, natural_full_WORD_domain="unknown")
                     for pc, raw, claim in original_format.CALLERS],
            token_table_reads=dict(primary_base=0xAE39A, primary_stride_WORD_wrapped=96,
                primary_count=48, primary_read_PC=0x662B8,
                secondary8_base=0xB439A, secondary8_stride_WORD_wrapped=16,
                secondary8_count=8, secondary8_read_PC=0x66214,
                secondary4_base=0xB539A, secondary4_stride_WORD_wrapped=8,
                secondary4_count=4, secondary4_read_PC=0x66252,
                address_rule="base + signed16(WORD(index*stride)); full D0.W, no255 clamp"),
            tile_reads=dict(base=0xB649A, LONGs_per_tile=8, bytes_per_tile=32,
                primary_rule="base + zeroextended_token_WORD*32 + 4*k; LONG shift",
                primary_read_PC=0x662D8,
                secondary_rule="base + (10000h if u16(token)>=0800h else0) + signed16(WORD(token*32+4*k))",
                secondary_read_PCs=[0x6622A, 0x66268], normalized_tokens=False),
            enumerated_WORD_domain=dict(min=0, max=65535, tile_address_period=8192,
                complete60_ROM_source_indices=58912, old_unselected_tiles=137,
                all60_valid_alias_tiles=63, all_zero_alias_tiles_excluded=9,
                nonzero_alias_tiles_emitted=54, prefix_only_alias_not_emitted=True,
                constructed_domain_not_natural=True),
            pixel_encoding=dict(width=8, height=8, bits_per_pixel=4,
                first_pixel="high nibble", source_rows=8, bytes_per_row=4,
                palettes_not_reauthored=True, image_identity="unknown")),
        editor_policy=dict(fixed_physical_tiles=54, pixels_only=True, original_witnesses_not_editable=True,
            old256_image_editor_unchanged=True, diagnostic_reads_edited_token_aliases_live=True,
            edited_source_plan_or_display_safety="unknown"),
        excluded_all_zero_read_tiles=list(ZERO_READ_TILES),
        remaining_old_holes_not_emitted=True, independent_CPU_comparison=False)


def fixed(spec):
    tile, index, path, item, token_address, token = spec
    return dict(id=f"rom_{tile:06X}_portrait_alias_tile", start=tile, end=tile + 32,
        original_witness=dict(D0_WORD=index, path=path, item=item, token_address=token_address,
            token_WORD=token, source_LONG_addresses=list(range(tile, tile + 32, 4)),
            complete60_ROM_sources=True, natural_domain="unknown", original_ROM_only=True))


def pinned(row, expected, mutable, label):
    keys(row, set(expected) | set(mutable), label)
    for key, value in expected.items(): same(row[key], value, label + "." + key)


def extract(rom):
    verify_rom(rom)
    result = metadata()
    result['tiles'] = []
    for spec in WITNESSES:
        same(verified_witness(rom, spec), fixed(spec)['original_witness'], 'verified original witness')
        result['tiles'].append(dict(**fixed(spec), pixels=tile_pixels(rom[spec[0]:spec[0] + 32])))
    return result


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {'tiles'}, 'portrait alias source package')
    rows = []
    for row, spec in zip(exact_list(fields['tiles'], 54, 'fixed alias tile catalog'), WITNESSES):
        info = fixed(spec)
        pinned(row, info, {'pixels'}, 'physical alias tile')
        data = tile_bytes(row['pixels'])
        rows.append(dict(id=info['id'], start=info['start'], end=info['end'], data=data,
            role='confirmed_original_WORD_alias_4bpp_pixel_source'))
    if sum(len(row['data']) for row in rows) != EDITABLE_BYTES or any(a['end'] > b['start'] for a, b in zip(rows, rows[1:])):
        raise ValueError('fixed nonoverlapping1728-byte source scope differs')
    return rows


def rebuild(rom, fields):
    rows = blocks(rom, fields)
    image = bytearray(rom)
    for row in rows: image[row['start']:row['end']] = row['data']
    return bytes(image)


def enumerate_alias_catalog(rom):
    """Repeatable canonical-domain scan with its proven8192 tile-address period.

    The palette selector is not period8192; this scan checks its complete ROM
    source containment for every WORD separately. No natural domain is inferred.
    """
    verify_rom(rom)
    holes = {original_format.TILES + 32 * i for lo, hi in original_format.UNSELECTED_TILE_RANGES for i in range(lo, hi)}
    valid = []
    witnesses = {}
    for index in range(8192):
        plan = read_plan(rom, index)
        valid.append(plan['status'] == 'complete_ROM_source_plan')
        if not valid[-1]: continue
        for record in plan['records']:
            tile = record['source_LONG_addresses'][0]
            if tile in holes and record['source_LONG_addresses'] == list(range(tile, tile + 32, 4)):
                witnesses.setdefault(tile, (tile, index, record['path'], record['item'], record['token_address'], record['token_WORD']))
    complete = 0
    for index in range(65536):
        if not valid[index & 8191]: continue
        selector_address = original_format.SELECTORS + original_format.signed_word(index)
        palette = original_format.PALETTE_BIAS + rom[selector_address] * 32
        if not 0 <= palette <= ROM_SIZE - 32:
            raise ValueError('palette source reaches external ROM boundary')
        complete += 1
    nonzero = tuple(witnesses[tile] for tile in sorted(witnesses) if any(rom[tile:tile + 32]))
    zero = tuple(tile for tile in sorted(witnesses) if not any(rom[tile:tile + 32]))
    return dict(complete_WORD_indices=complete, alias_tiles=len(witnesses), nonzero=nonzero, zero=zero)


def schema():
    def obj(properties): return dict(type='object', properties=properties, required=list(properties), additionalProperties=False)
    def exact(items): return dict(type='array', prefixItems=items, items=False, minItems=len(items), maxItems=len(items))
    def constant(value):
        if type(value) is dict: return obj({k: constant(v) for k, v in value.items()})
        if type(value) is list: return exact([constant(v) for v in value])
        return dict(type={str:'string', int:'integer', bool:'boolean'}[type(value)], const=value)
    pixel = dict(type='integer', minimum=0, maximum=15)
    grid = dict(type='array', minItems=8, maxItems=8, items=dict(type='array', minItems=8, maxItems=8, items=pixel))
    properties = {k: constant(v) for k, v in metadata().items()}
    properties['tiles'] = exact([obj({**{k: constant(v) for k, v in fixed(spec).items()}, 'pixels':grid}) for spec in WITNESSES])
    result = obj(properties)
    result['$schema'] = 'https://json-schema.org/draft/2020-12/schema'
    result['description'] = 'Only54 original nonzero alias-selected8x8 4bpp pixel tiles are editable. Witnesses concern original ROM, not safe edited execution or naturally reached full-WORD indices.'
    return result


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom, load_fields(serialized))
    if image != rom: raise ValueError('serialized whole-ROM pixel roundtrip differs')
    rows = blocks(rom, fields)
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=54,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        source_union_sha256=sha(b''.join(row['data'] for row in rows)),
        original_nonzero_source_BYTEs=sum(bool(v) for row in rows for v in row['data']),
        all_original_witnesses_verified=True,
        blocks=[{k:v for k,v in row.items() if k != 'data'} | dict(bytes=len(row['data']), sha256=sha(row['data'])) for row in rows],
        edited_source_alias_example=dict(D0_WORD=0x218, path='secondary8', item=0,
            token_address=0xB651A, same_physical_bytes_also_pixels=True, second_authority=False))
    members = {'fields.json':serialized, 'fields.schema.json':dump(schema()), 'validation.json':dump(report)}
    members['manifest.json'] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES, physical_blocks=54,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError('output must stay in portrait_alias_tiles build scope or exact formal bundle')
    if path.exists() or not path.parent.is_dir(): raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('export','import','verify'))
    parser.add_argument('--rom', default=str(DEFAULT_ROM)); parser.add_argument('--fields')
    parser.add_argument('--bundle'); parser.add_argument('--output')
    args = parser.parse_args(argv); target = None
    if args.command == 'export':
        if args.output is None or args.fields is not None or args.bundle is not None: raise ValueError('export requires fresh output only')
        target = fresh_output(args.output, bundle=True)
    elif args.command == 'import':
        if args.output is None or args.bundle is not None: raise ValueError('import requires fields and fresh output')
        target = fresh_output(args.output)
        if target.suffix.lower() != '.bin': raise ValueError('fresh .bin output required')
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError('verify accepts fields or bundle and writes nothing')
    rom = read_bounded(args.rom, ROM_SIZE)
    if args.command == 'export':
        members = render_bundle(rom); target.mkdir()
        for name,data in members.items(): put(target / name, data)
        result = dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={name:sha(data) for name,data in members.items()})
    elif args.command == 'verify' and args.bundle is not None:
        bundle = safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS: raise ValueError('exact four-member bundle required')
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle / name, MAX_JSON) != data: raise ValueError('canonical bundle drift: ' + name)
        result = dict(path=str(bundle),verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields = load_fields(read_bounded(args.fields or DEFAULT_FIELDS, MAX_JSON)); image = rebuild(rom,fields)
        if target is not None: put(target,image)
        result = dict(path=None if target is None else str(target),editable_bytes=EDITABLE_BYTES,bytes=len(image),exact_canonical=image == rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True)); return 0


if __name__ == '__main__': raise SystemExit(main())
