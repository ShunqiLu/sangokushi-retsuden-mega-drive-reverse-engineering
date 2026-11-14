"""142 actual source bytes from complete original portrait alias plans.

Two whole8x8 tiles(64B) and78 sparse pixel-pair BYTEs are separate authoring
fields. Neighbouring typed bytes are visible in edited-image source views,
never reauthored. Constructed witnesses do not prove a natural input domain.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import copy
from functools import lru_cache
import json
from pathlib import Path

from tools.portrait_alias_tiles import codec as base

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = base.DEFAULT_ROM
ROM_SIZE, ROM_SHA256 = base.ROM_SIZE, base.ROM_SHA256
OUTPUT_ROOT = ROOT / 'build/portrait_external_alias_pixels'
FORMAL_ROOT = ROOT / 'analysis/portrait_external_alias_pixels/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
FORMAT = 'g5510-external-portrait-alias-pixel-source-fields-v1'
EDITABLE_BYTES = 142
MAX_JSON = 2 * 1024 * 1024
MEMBERS = base.MEMBERS
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_BANKS = (
    ('m68k_bank0c.s',reference_value(__name__, 'LAYOUT_BANKS')),
    ('m68k_bank0f.s',reference_value(__name__, 'LAYOUT_BANKS_2')),
)
FULL_TILE_STARTS = (0xCE43A,0xCE47A)
SPARSE_ADDRESSES = (
    0xF84CC,0xF8667,0xF86F7,0xF86F8,0xF86F9,0xF86FA,0xF86FB,0xF86FC,
    0xF86FD,0xF86FE,0xF86FF,0xF8700,0xF8701,0xF8702,0xF8703,0xF8704,
    0xF8705,0xF8706,0xF8707,0xF8708,0xF8709,0xF870A,0xF870B,0xF870C,
    0xF870D,0xF8724,0xF8725,0xF8726,0xF8727,0xF8728,0xF8729,0xF872A,
    0xF872B,0xF872C,0xF872D,0xF872E,0xF88EB,0xF8A26,0xF8D4E,0xF8DB2,
    0xF8E31,0xF8ED7,0xF9025,0xF9298,0xF92E3,0xF9431,0xF94A2,0xF94EA,
    0xF9536,0xF957D,0xF95EE,0xF973E,0xF9799,0xF97FF,0xF98BD,0xF98F1,
    0xF9A75,0xF9B05,0xF9B8B,0xF9BF1,0xF9C5E,0xF9CE8,0xFA720,0xFA81D,
    0xFA98F,0xFA9D4,0xFAC3E,0xFAC92,0xFACCA,0xFAD8E,0xFAE4E,0xFAEA8,
    0xFAED9,0xFAF63,0xFB0AC,0xFB3CA,0xFB457,0xFB65F,
)
WITNESS_SHA = reference_value(__name__, 'WITNESS_SHA')
sha, dump = base.sha, base.dump
uint, same, exact_list, pinned = base.uint, base.same, base.exact_list, base.pinned
load_fields, safe_path = base.load_fields, base.safe_path
read_bounded, put = base.read_bounded, base.put
tile_pixels, tile_bytes, read_plan = base.tile_pixels, base.tile_bytes, base.read_plan


def tile_start(address):
    return base.original_format.TILES+(address-base.original_format.TILES)//32*32


SPARSE_TILE_STARTS = tuple(sorted({tile_start(a) for a in SPARSE_ADDRESSES}))
CATALOG_TILE_STARTS = tuple(sorted(set(FULL_TILE_STARTS)|set(SPARSE_TILE_STARTS)))


def verify_rom(rom):
    base.verify_rom(rom)


@lru_cache(maxsize=1)
def _witness_catalog(rom):
    verify_rom(rom)
    result={}
    for index in range(8192):
        plan=read_plan(rom,index)
        if plan['status']!='complete_ROM_source_plan':continue
        for row in plan['records']:
            start=row['source_LONG_addresses'][0]
            if start in CATALOG_TILE_STARTS and row['source_LONG_addresses']==list(range(start,start+32,4)):
                result.setdefault(start,dict(tile_start=start,D0_WORD=index,path=row['path'],item=row['item'],
                    token_address=row['token_address'],token_WORD=row['token_WORD'],
                    source_LONG_addresses=row['source_LONG_addresses']))
    if tuple(sorted(result))!=CATALOG_TILE_STARTS:
        raise ValueError('a source pixel fragment has no complete original plan witness')
    same(sha(dump([result[a] for a in CATALOG_TILE_STARTS])),WITNESS_SHA,'49 full original tile witnesses')
    return result


def witness_catalog(rom):
    verify_rom(rom)
    return copy.deepcopy(_witness_catalog(rom))


def metadata():
    return dict(format=FORMAT,confidence='candidate',source_confidence='confirmed',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        evidence=dict(source='original source LONGs in complete48+8+4 tile, selector and palette ROM plans',
            consumer=dict(start=0x661D4,end=0x662E4,bytes=272,sha256=base.original_format.CONSUMER_SHA),
            older_ledger=dict(path=base.ENHANCED_PATH,sha256=base.ENHANCED_SHA256,consumer_confidence='heuristic'),
            frozen_raw_layout=dict(id=LAYOUT_ID,banks=[dict(name=n,sha256=s) for n,s in LAYOUT_BANKS],
                all_emitted_bytes_raw=True,old_typed_overlap_bytes=0),
            canonical_complete_ROM_source_plan_indices=58912,tile_address_period=8192,
            witness_sha256=WITNESS_SHA,constructed_witnesses_not_natural=True,
            source_LONGs_per_tile=8,source_LONGs_cover_every_sparse_BYTE=True,
            pixel_encoding=dict(width=8,height=8,bits_per_pixel=4,bytes_per_row=4,first_pixel='high nibble'),
            primary_rule='B649A + zeroextended full token WORD*32 + 4*k, LONG arithmetic',
            secondary_rule='B649A + unsigned0800 bias10000 + signed16(wrapped WORD token*32+4*k)',
            raw_union=dict(bytes=142,nonzero_BYTEs=85,zero_BYTEs=57,
                complete_tiles=2,complete_tile_bytes=64,sparse_PIXEL_PAIR_BYTEs=78,sparse_original_tiles=47),
            exclusions=dict(existing_pixel_fields=True,portrait_alias_metadata1010=True,
                FM_tail_start=0xFE31D,FM_tail_end=0xFEF6B,
                raw_F0000_F8000_source_union_bytes=0)),
        editor_policy=dict(full_tiles_only_for_two_complete_raw_sources=True,
            sparse_pairs_only_at_fixed_BYTE_addresses=True,neighbouring_typed_bytes_not_reauthored=True,
            diagnostics_assemble_current_whole_image=True,original_witnesses_not_editable=True,
            pixel_index_range=[0,15],palette_identity='unknown',source_read_domain_not_CPU_clamp=True),
        padding_claim=False,free_space_claim=False,natural_domain='unknown',image_identity='unknown',
        edited_display_safety='unknown',independent_CPU_comparison=False,source_projection_not_CPU=True)


def full_fixed(rom,start):
    return dict(id=f'rom_{start:06X}_external_alias_full_tile',start=start,end=start+32,
        original_complete_witness=witness_catalog(rom)[start])


def sparse_fixed(rom,start):
    return dict(id=f'rom_{start:06X}_external_alias_sparse_tile',tile_start=start,tile_end=start+32,
        original_complete_witness=witness_catalog(rom)[start],
        neighbouring_bytes_display_only=True)


def pair_fixed(address):
    start=tile_start(address);offset=address-start
    return dict(id=f'rom_{address:06X}_source_pixel_pair',address=address,
        row=offset//4,first_column=2*(offset%4),source_LONG_address=start+4*(offset//4),
        source_LONG_byte_index=offset%4)


def extract(rom):
    verify_rom(rom);fields=metadata()
    fields['full_tiles']=[dict(**full_fixed(rom,a),pixels=tile_pixels(rom[a:a+32])) for a in FULL_TILE_STARTS]
    fields['sparse_tiles']=[dict(**sparse_fixed(rom,start),pixel_pairs=[dict(**pair_fixed(a),
        pixels=[rom[a]>>4,rom[a]&15]) for a in SPARSE_ADDRESSES if tile_start(a)==start]) for start in SPARSE_TILE_STARTS]
    return fields


def blocks(rom,fields):
    verify_rom(rom);pinned(fields,metadata(),{'full_tiles','sparse_tiles'},'external alias pixel package')
    rows=[]
    for row,start in zip(exact_list(fields['full_tiles'],2,'two complete raw tiles'),FULL_TILE_STARTS):
        info=full_fixed(rom,start);pinned(row,info,{'pixels'},'complete source tile')
        rows.append(dict(id=info['id'],start=start,end=start+32,data=tile_bytes(row['pixels']),
            role='confirmed_complete_external_alias_4bpp_pixel_source'))
    for row,start in zip(exact_list(fields['sparse_tiles'],47,'fixed sparse source tiles'),SPARSE_TILE_STARTS):
        pinned(row,sparse_fixed(rom,start),{'pixel_pairs'},'sparse source tile')
        addresses=[a for a in SPARSE_ADDRESSES if tile_start(a)==start]
        for pair,address in zip(exact_list(row['pixel_pairs'],len(addresses),'fixed actually read pixel pairs'),addresses):
            info=pair_fixed(address);pinned(pair,info,{'pixels'},'two source pixel indices')
            pixels=exact_list(pair['pixels'],2,'high then low source pixel')
            data=bytes([(uint(pixels[0],15,'high pixel')<<4)|uint(pixels[1],15,'low pixel')])
            rows.append(dict(id=info['id'],start=address,end=address+1,data=data,
                role='confirmed_original_LONG_read_sparse_4bpp_pixel_pair'))
    rows.sort(key=lambda row:row['start'])
    if len(rows)!=80 or sum(len(row['data']) for row in rows)!=142 or any(a['end']>b['start'] for a,b in zip(rows,rows[1:])):
        raise ValueError('fixed nonoverlapping142-byte source scope differs')
    return rows


def rebuild(rom,fields):
    rows=blocks(rom,fields);image=bytearray(rom)
    for row in rows:image[row['start']:row['end']]=row['data']
    return bytes(image)


def source_view(image,start):
    """Physical alias tile assembled from current authored AND display-only bytes.

    The49-entry editor directory is not a CPU-domain restriction. Use shared
    read_plan(image,D0_LONG) for the actual ordered conditional source projection.
    """
    if type(image) is not bytes or len(image)!=ROM_SIZE:raise ValueError('complete bytes image required')
    uint(start,ROM_SIZE-32,'physical tile source start')
    if start not in CATALOG_TILE_STARTS:raise ValueError('physical source is outside this diagnostic editor catalog')
    owned=set(range(start,start+32)) if start in FULL_TILE_STARTS else {a for a in SPARSE_ADDRESSES if tile_start(a)==start}
    return dict(tile_start=start,tile_end=start+32,pixels=tile_pixels(image[start:start+32]),
        editable_pixel_pairs=[dict(address=a,row=(a-start)//4,first_column=2*((a-start)%4)) for a in sorted(owned)],
        display_only_BYTE_addresses=[a for a in range(start,start+32) if a not in owned],
        bytes_are_live_current_image=True,neighbouring_typed_bytes_reauthored=False,
        source_projection_not_CPU=True,natural_domain='unknown')


def schema(rom):
    def obj(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def exact(items):return dict(type='array',prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def constant(value):
        if type(value) is dict:return obj({k:constant(v) for k,v in value.items()})
        if type(value) is list:return exact([constant(v) for v in value])
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(value)],const=value)
    def values(count,item):return dict(type='array',minItems=count,maxItems=count,items=item)
    pixel=dict(type='integer',minimum=0,maximum=15)
    properties={k:constant(v) for k,v in metadata().items()}
    properties['full_tiles']=exact([obj({**{k:constant(v) for k,v in full_fixed(rom,a).items()},
        'pixels':values(8,values(8,pixel))}) for a in FULL_TILE_STARTS])
    properties['sparse_tiles']=exact([obj({**{k:constant(v) for k,v in sparse_fixed(rom,start).items()},
        'pixel_pairs':exact([obj({**{k:constant(v) for k,v in pair_fixed(a).items()},'pixels':values(2,pixel)})
            for a in SPARSE_ADDRESSES if tile_start(a)==start])}) for start in SPARSE_TILE_STARTS])
    result=obj(properties);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='Two full8x8 source grids plus78 sparse high/low4-bit pixel pairs only. Neighbouring typed bytes are live diagnostic display, not editor authority.'
    return result


def render_bundle(rom):
    fields=extract(rom);serialized=dump(fields);image=rebuild(rom,load_fields(serialized))
    if image!=rom:raise ValueError('serialized whole-ROM source pixel roundtrip differs')
    rows=blocks(rom,fields)
    report=dict(**metadata(),editable_bytes=142,physical_blocks=80,all_original_witnesses_verified=True,
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        source_union_sha256=sha(b''.join(row['data'] for row in rows)),
        blocks=[{k:v for k,v in row.items() if k!='data'}|dict(bytes=len(row['data']),sha256=sha(row['data'])) for row in rows])
    members={'fields.json':serialized,'fields.schema.json':dump(schema(rom)),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=142,physical_blocks=80,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError('output must stay in external alias pixels build scope or exact formal bundle')
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
        result=dict(path=str(target),editable_bytes=142,members={name:sha(data) for name,data in members.items()})
    elif args.command=='verify' and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS:raise ValueError('exact four-member bundle required')
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data:raise ValueError('canonical bundle drift: '+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=142,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON));image=rebuild(rom,fields)
        if target is not None:put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=142,bytes=len(image),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
