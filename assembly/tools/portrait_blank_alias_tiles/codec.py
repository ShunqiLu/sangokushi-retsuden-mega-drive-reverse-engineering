"""Nine original all-zero tiles with complete original alias read witnesses.

The zero bits encode actual editable pixel indices. They are not declared
padding/free space. This independent288-byte catalog never changes the frozen
54-tile catalog. All diagnostics use its shared live-image source projection.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.portrait_alias_tiles import codec as base

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = base.DEFAULT_ROM
ROM_SIZE, ROM_SHA256 = base.ROM_SIZE, base.ROM_SHA256
OUTPUT_ROOT = ROOT / 'build/portrait_blank_alias_tiles'
FORMAL_ROOT = ROOT / 'analysis/portrait_blank_alias_tiles/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
FORMAT = 'g5510-constructed-portrait-blank-alias-pixel-fields-v1'
EDITABLE_BYTES = 288
MAX_JSON = 1024 * 1024
MEMBERS = base.MEMBERS
WITNESSES = (
    (0xBA49A, 0x2E5, 'secondary8', 0, 0xB71EA, 0x200),
    (0xBE49A, 0x14B, 'primary', 43, 0xB6010, 0x400),
    (0xC049A, 0x26B, 'secondary8', 5, 0xB6A54, 0xDD00),
    (0xC249A, 0x18E, 'secondary4', 1, 0xB600C, 0xE00),
    (0xC449A, 0x2CE, 'secondary8', 5, 0xB7084, 0x6700),
    (0xC737A, 0x51A, 'secondary8', 0, 0xB953A, 0x8077),
    (0xC849A, 0x48E, 'secondary8', 7, 0xB8C88, 0xE100),
    (0xCA49A, 0x263, 'secondary4', 3, 0xB66B8, 0xBA00),
    (0xCC49A, 0x262, 'secondary4', 3, 0xB66B0, 0xAB00),
)
sha, dump = base.sha, base.dump
uint, same, exact_list = base.uint, base.same, base.exact_list
load_fields, safe_path = base.load_fields, base.safe_path
read_bounded, put, pinned = base.read_bounded, base.put, base.pinned
tile_pixels, tile_bytes, read_plan = base.tile_pixels, base.tile_bytes, base.read_plan


def verify_rom(rom):
    base.verify_rom(rom)


def metadata():
    return dict(format=FORMAT, confidence='candidate', source_confidence='confirmed',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        evidence=dict(source='original full-WORD alias source reads, not zero-byte appearance',
            consumer=dict(start=0x661D4,end=0x662E4,bytes=272,sha256=base.original_format.CONSUMER_SHA),
            original_callers=[dict(start=pc,bytes=raw,precondition=claim)
                for pc,raw,claim in base.original_format.CALLERS],
            older_ledger=dict(path=base.ENHANCED_PATH,sha256=base.ENHANCED_SHA256),
            frozen_raw_layout=dict(id=base.LAYOUT_ID,all_emitted_bytes_raw=True,old_typed_overlap_bytes=0),
            addressing='primary LONG token*32; secondary unsigned0800 bias then signed wrapped WORD token*32+4*k',
            whole60_tile_and_selector_palette_sources_in_ROM=True,
            witnesses_constructed_not_natural=True,physical_tiles=9,bytes_per_tile=32,
            pixel_encoding=dict(width=8,height=8,bits_per_pixel=4,first_pixel='high nibble',bytes_per_row=4),
            original_pixels_all_zero=True,zero_pixels_are_real_source_data=True),
        editor_policy=dict(pixels_only=True,fixed_original_witnesses=True,
            frozen54tile_catalog_unchanged=True,old256image_editor_unchanged=True,
            live_token_alias_diagnostics=True),
        padding_claim=False,free_space_claim=False,blank_visual_purpose='unknown',
        natural_domain='unknown',image_identity='unknown',edited_display_safety='unknown',
        independent_CPU_comparison=False)


def fixed(spec):
    row = base.fixed(spec)
    row['id'] = f'rom_{spec[0]:06X}_portrait_blank_alias_tile'
    return row


def verify_witness(rom,spec):
    tile,index,path,item,address,token = spec
    plan = read_plan(rom,index)
    if plan['status'] != 'complete_ROM_source_plan' or len(plan['records']) != 60:
        raise ValueError('blank tile witness has an external original source boundary')
    row = next(row for row in plan['records'] if row['path']==path and row['item']==item)
    if (row['token_address'],row['token_WORD'],row['source_LONG_addresses']) != (address,token,list(range(tile,tile+32,4))):
        raise ValueError('complete original blank-tile source witness differs')
    if rom[tile:tile+32] != bytes(32) or tile in base.original_format.SELECTED_TILES:
        raise ValueError('original blank tile bytes or old editor exclusion differs')
    return fixed(spec)['original_witness']


def extract(rom):
    verify_rom(rom)
    fields = metadata(); fields['tiles'] = []
    for spec in WITNESSES:
        verify_witness(rom,spec)
        fields['tiles'].append(dict(**fixed(spec),pixels=tile_pixels(rom[spec[0]:spec[0]+32])))
    return fields


def blocks(rom,fields):
    verify_rom(rom); pinned(fields,metadata(),{'tiles'},'blank alias pixel package')
    rows = []
    for row,spec in zip(exact_list(fields['tiles'],9,'real blank source tile catalog'),WITNESSES):
        info = fixed(spec); pinned(row,info,{'pixels'},'physical blank alias tile')
        data = tile_bytes(row['pixels'])
        rows.append(dict(id=info['id'],start=info['start'],end=info['end'],data=data,
            role='confirmed_original_WORD_alias_blank_4bpp_pixel_source'))
    if sum(len(row['data']) for row in rows)!=288 or any(a['end']>b['start'] for a,b in zip(rows,rows[1:])):
        raise ValueError('fixed nonoverlapping288-byte source scope differs')
    return rows


def rebuild(rom,fields):
    rows = blocks(rom,fields); image = bytearray(rom)
    for row in rows: image[row['start']:row['end']] = row['data']
    return bytes(image)


def schema():
    def obj(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def exact(items):return dict(type='array',prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def constant(value):
        if type(value) is dict:return obj({k:constant(v) for k,v in value.items()})
        if type(value) is list:return exact([constant(v) for v in value])
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(value)],const=value)
    grid = dict(type='array',minItems=8,maxItems=8,items=dict(type='array',minItems=8,maxItems=8,
        items=dict(type='integer',minimum=0,maximum=15)))
    result = obj({**{k:constant(v) for k,v in metadata().items()},
        'tiles':exact([obj({**{k:constant(v) for k,v in fixed(spec).items()},'pixels':grid}) for spec in WITNESSES])})
    result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='Nine proven original alias-selected blank tile sources. Pixels are mutable0..15, not pinned zero filler; no padding/free-space or natural domain claim.'
    return result


def render_bundle(rom):
    fields = extract(rom); serialized = dump(fields)
    image = rebuild(rom,load_fields(serialized))
    if image != rom:raise ValueError('serialized entire-ROM pixel roundtrip differs')
    rows = blocks(rom,fields)
    report = dict(**metadata(),editable_bytes=288,physical_blocks=9,
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),all_original_witnesses_verified=True,
        source_union_sha256=sha(b''.join(row['data'] for row in rows)),
        blocks=[{k:v for k,v in row.items() if k!='data'}|dict(bytes=32,sha256=sha(row['data'])) for row in rows],
        source_projection_not_CPU=True)
    members = {'fields.json':serialized,'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=288,physical_blocks=9,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError('output must stay in blank alias tile build scope or exact formal bundle')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'));parser.add_argument('--rom',default=str(DEFAULT_ROM))
    parser.add_argument('--fields');parser.add_argument('--bundle');parser.add_argument('--output')
    args=parser.parse_args(argv);target=None
    if args.command=='export':
        if args.output is None or args.fields is not None or args.bundle is not None:raise ValueError('export requires fresh output only')
        target=fresh_output(args.output,bundle=True)
    elif args.command=='import':
        if args.output is None or args.bundle is not None:raise ValueError('import requires fields and fresh output')
        target=fresh_output(args.output)
        if target.suffix.lower()!='.bin':raise ValueError('fresh .bin output required')
    elif args.output is not None or (args.fields is not None and args.bundle is not None):raise ValueError('verify accepts fields or bundle and writes nothing')
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=288,members={name:sha(data) for name,data in members.items()})
    elif args.command=='verify' and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS:raise ValueError('exact four-member bundle required')
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data:raise ValueError('canonical bundle drift: '+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=288,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON));image=rebuild(rom,fields)
        if target is not None:put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=288,bytes=len(image),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
