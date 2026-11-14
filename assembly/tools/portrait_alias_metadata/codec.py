"""1010 bytes of complete-plan original portrait alias metadata sources.

One physical authority preserves425 full tile-token WORDs and80 full colour
WORDs. Token/selector/palette overlaps are live read aliases, never duplicate
editor fields. Constructed complete-ROM witnesses are not natural domains.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
from functools import lru_cache
import json
from pathlib import Path

from tools.portrait_alias_tiles import codec as base

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = base.DEFAULT_ROM
ROM_SIZE, ROM_SHA256 = base.ROM_SIZE, base.ROM_SHA256
OUTPUT_ROOT = ROOT / 'build/portrait_alias_metadata'
FORMAL_ROOT = ROOT / 'analysis/portrait_alias_metadata/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
FORMAT = 'g5510-constructed-portrait-alias-metadata-fields-v1'
EDITABLE_BYTES = 1010
MAX_JSON = 2 * 1024 * 1024
MEMBERS = base.MEMBERS
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_BANKS = (
    ('m68k_bank0a.s', reference_value(__name__, 'LAYOUT_BANKS')),
    ('m68k_bank0b.s', reference_value(__name__, 'LAYOUT_BANKS_2')),
)
TOKEN_SCOPES = (
    (0xAACA8, 0xAADDA), (0xB849A, 0xB857A), (0xBA47A, 0xBA49A),
    (0xBA4BA, 0xBA51A), (0xBA53A, 0xBA57A), (0xBC47A, 0xBC49A),
    (0xBCD3A, 0xBCD9A),
)
PALETTE_STARTS = (0xB5E1A, 0xB631A, 0xB633A, 0xB635A, 0xB637A)
TOKEN_WITNESS_SHA = reference_value(__name__, 'TOKEN_WITNESS_SHA')
PALETTE_WITNESS_SHA = reference_value(__name__, 'PALETTE_WITNESS_SHA')
INSTRUCTIONS = (
    (0x661EA, '3200'), (0x661EC, 'e349'), (0x661EE, 'd240'), (0x661F0, 'eb49'),
    (0x661F2, '41f9000ae39a'), (0x661F8, 'd0c1'), (0x662B8, '3418'),
    (0x66200, 'e949'), (0x66202, '41f9000b439a'), (0x66208, 'd0c1'),
    (0x66214, '3618'), (0x66216, '0c430800'), (0x6621E, 'd3fc00010000'),
    (0x66224, 'eb4b'), (0x6622A, '23f1300000c00000'), (0x66232, '5843'),
    (0x6623E, 'e749'), (0x66240, '41f9000b539a'), (0x66246, 'd0c1'),
    (0x66252, '3618'), (0x66268, '23f1300000c00000'),
    (0x6627A, '43f9000b599a'), (0x66280, '45f9000b639a'),
    (0x66286, '7200'), (0x66288, '12320000'), (0x6628C, 'eb89'),
    (0x6628E, 'd3c1'), (0x66290, '343c0007'), (0x662A6, '24d9'),
    (0x662A8, '51cafffc'), (0x662CA, '02820000ffff'), (0x662D0, 'eb8a'),
)
sha, dump = base.sha, base.dump
uint, same, exact_list, pinned = base.uint, base.same, base.exact_list, base.pinned
load_fields, safe_path = base.load_fields, base.safe_path
read_bounded, put = base.read_bounded, base.put
colour, colour_word = base.original_format.colour, base.original_format.colour_word
read_plan = base.read_plan


def verify_rom(rom):
    base.verify_rom(rom)
    for address, raw in INSTRUCTIONS:
        if rom[address:address + len(raw) // 2].hex() != raw:
            raise ValueError('pinned original source instruction differs')


@lru_cache(maxsize=1)
def _source_catalog(rom):
    """Derive first canonical complete witnesses without reading external files.

    Every WORD-index tile address has the proven8192 period; the selector has
    no such period. All65536 selector/palette containment tests are separate.
    These are original source plans, not CPU or natural reachability results.
    """
    verify_rom(rom)
    required = {a for start, end in TOKEN_SCOPES for a in range(start, end, 2)}
    tokens, palettes, complete_period = {}, {}, []
    token_bytes, selector_bytes, palette_bytes = set(), set(), set()
    for index in range(8192):
        plan = read_plan(rom, index)
        complete = plan['status'] == 'complete_ROM_source_plan'
        complete_period.append(complete)
        if not complete:
            continue
        for row in plan['records']:
            address = row['token_address']
            token_bytes.update(range(address, address + 2))
            if address in required:
                tokens.setdefault(address, dict(D0_WORD=index, path=row['path'], item=row['item'],
                    address=address, original_TOKEN_WORD=row['token_WORD']))
    total = 0
    for index in range(65536):
        if not complete_period[index & 8191]:
            continue
        address = base.original_format.SELECTORS + base.original_format.signed_word(index)
        if not 0 <= address < ROM_SIZE:
            raise ValueError('original selector source is external')
        selector = rom[address]
        palette = base.original_format.PALETTE_BIAS + selector * 32
        if not 0 <= palette <= ROM_SIZE - 32:
            raise ValueError('original palette source is external')
        total += 1
        selector_bytes.add(address)
        palette_bytes.update(range(palette, palette + 32))
        if palette in PALETTE_STARTS:
            palettes.setdefault(palette, dict(D0_WORD=index, selector_address=address,
                original_selector_BYTE=selector, palette_start=palette))
    if total != 58912 or set(tokens) != required or set(palettes) != set(PALETTE_STARTS):
        raise ValueError('canonical complete source union or witness catalog differs')
    same(sha(dump([tokens[a] for a in sorted(tokens)])), TOKEN_WITNESS_SHA, '425 token witnesses')
    same(sha(dump([palettes[a] for a in PALETTE_STARTS])), PALETTE_WITNESS_SHA, '5 palette witnesses')
    return dict(tokens=tokens, palettes=palettes, complete_WORD_indices=total,
        token_bytes=frozenset(token_bytes), selector_bytes=frozenset(selector_bytes),
        palette_bytes=frozenset(palette_bytes))


def source_catalog(rom):
    """A detached diagnostic catalog; callers cannot alter the pinned cache."""
    verify_rom(rom)
    result=_source_catalog(rom)
    return dict(**{k:v for k,v in result.items() if k not in ('tokens','palettes')},
        tokens={a:dict(witness) for a,witness in result['tokens'].items()},
        palettes={a:dict(witness) for a,witness in result['palettes'].items()})


def metadata():
    return dict(format=FORMAT, confidence='candidate', source_confidence='confirmed',
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        evidence=dict(source='actual token WORD, selector BYTE and palette LONG reads from complete original alias plans',
            consumer=dict(start=0x661D4, end=0x662E4, bytes=272, sha256=base.original_format.CONSUMER_SHA),
            source_instruction_pins=[dict(PC=pc, bytes=raw) for pc, raw in INSTRUCTIONS],
            older_ledger=dict(path=base.ENHANCED_PATH, sha256=base.ENHANCED_SHA256,
                consumer_confidence='heuristic'),
            frozen_raw_layout=dict(id=LAYOUT_ID, banks=[dict(name=n,sha256=s) for n,s in LAYOUT_BANKS],
                all_emitted_bytes_raw=True, old_typed_overlap_bytes=0),
            full_WORD_constructed_domain=dict(min=0,max=65535, complete_ROM_source_plans=58912,
                tile_address_period=8192, selector_period_not_assumed=True, natural_domain='unknown'),
            original_read_order=['48 primary tokens and sources','8 secondary tokens and sources',
                '4 secondary tokens and sources','selector BYTE','8 palette LONGs'],
            token_rule='base + s16(WORD(index*96,16,8)), then separately advanced token WORD addresses',
            tile_rule='primary token zeroextend LONG*32; secondary unsigned0800 bias plus signed wrapped WORD offset per LONG',
            selector_rule='B639A + signed16(full input WORD), without255 clamp',
            palette_rule='B599A + zeroextended selector BYTE*32, eight consecutive source LONGs',
            raw_read_union=dict(bytes=1010, token_WORD_read_bytes=1010,
                selector_BYTE_read_bytes=651,palette_LONG_read_bytes=160, nonzero_BYTEs=810, zero_BYTEs=200),
            token_witness_sha256=TOKEN_WITNESS_SHA,palette_witness_sha256=PALETTE_WITNESS_SHA,
            excluded_frozen_pixel_bytes=2016, frozen54_and9_tile_packages_unchanged=True),
        editor_policy=dict(physical_token_WORDs=425, physical_colour_WORDs=80,
            full_token_range=[0,65535],full_colour_WORD_bits_preserved=True,
            palette_channels='red bits1..3, green5..7, blue9..11; all other bits retained',
            single_physical_authority=True, selector_aliases_not_reemitted=True,
            palette_token_aliases_not_reemitted=True, diagnostics_read_edited_image=True,
            no_reference_clamp=True, no_original_complete_plan_safety_requirement=True),
        preserved_unknown=dict(start=0xAADDA,end=0xAADE2,bytes=8,emitted=False,
            reason='no complete original plan witness in this scan',padding_claim=False),
        padding_claim=False, free_space_claim=False, image_identity='unknown',
        natural_domain='unknown', edited_display_safety='unknown',
        source_projection_not_CPU=True, independent_CPU_comparison=False)


def token_fixed(rom,start,end):
    catalog = source_catalog(rom)
    return dict(id=f'rom_{start:06X}_alias_token_WORDs',start=start,end=end,WORD_count=(end-start)//2,
        original_complete_witnesses=[catalog['tokens'][a] for a in range(start,end,2)])


def palette_fixed(rom,start):
    return dict(id=f'rom_{start:06X}_alias_palette',start=start,end=start+32,
        original_selector=(start-base.original_format.PALETTE_BIAS)//32, colour_WORD_count=16,
        original_complete_witness=source_catalog(rom)['palettes'][start])


def extract(rom):
    verify_rom(rom)
    fields = metadata()
    fields['token_sources'] = [dict(**token_fixed(rom,start,end),
        WORDs=[int.from_bytes(rom[a:a+2],'big') for a in range(start,end,2)]) for start,end in TOKEN_SCOPES]
    fields['palette_sources'] = [dict(**palette_fixed(rom,start),
        colours=[colour(int.from_bytes(rom[a:a+2],'big')) for a in range(start,start+32,2)]) for start in PALETTE_STARTS]
    return fields


def blocks(rom,fields):
    verify_rom(rom)
    pinned(fields,metadata(),{'token_sources','palette_sources'},'portrait alias metadata package')
    rows = []
    for row,(start,end) in zip(exact_list(fields['token_sources'],7,'fixed token source spans'),TOKEN_SCOPES):
        info = token_fixed(rom,start,end)
        pinned(row,info,{'WORDs'},'physical token source')
        values=exact_list(row['WORDs'],info['WORD_count'],'full token WORDs')
        data=b''.join(uint(value,65535,'full token WORD').to_bytes(2,'big') for value in values)
        rows.append(dict(id=info['id'],start=start,end=end,data=data,role='confirmed_original_full_WORD_alias_tile_token_source'))
    for row,start in zip(exact_list(fields['palette_sources'],5,'fixed palette sources'),PALETTE_STARTS):
        info = palette_fixed(rom,start)
        pinned(row,info,{'colours'},'physical palette source')
        data=b''.join(colour_word(value).to_bytes(2,'big') for value in exact_list(row['colours'],16,'fullbits colour WORDs'))
        rows.append(dict(id=info['id'],start=start,end=start+32,data=data,role='confirmed_original_palette_colour_WORD_source'))
    rows.sort(key=lambda row:row['start'])
    if sum(len(row['data']) for row in rows)!=1010 or any(a['end']>b['start'] for a,b in zip(rows,rows[1:])):
        raise ValueError('fixed nonoverlapping1010-byte source union differs')
    return rows


def rebuild(rom,fields):
    rows=blocks(rom,fields);image=bytearray(rom)
    for row in rows:image[row['start']:row['end']]=row['data']
    return bytes(image)


def metadata_view(image,D0_LONG):
    """Conditional source projection from any complete original/edited image.

    An edited token may make the plan external before later metadata reads.
    No original-60-source safety condition, bus mirroring or255 clamp is added.
    """
    plan=read_plan(image,D0_LONG)
    result=dict(status=plan['status'],D0_WORD=plan['D0_WORD'],
        tokens=[{k:row[k] for k in ('path','item','token_address','token_WORD')} for row in plan['records']],
        source_projection_not_CPU=True,natural_domain='unknown')
    if plan['status']!='complete_ROM_source_plan':
        result['boundary']=plan['boundary']
        return result
    result.update(selector_address=plan['selector_address'],selector_BYTE=plan['selector_BYTE'],
        palette_start=plan['palette_start'],palette_LONGs=plan['palette_LONGs'],
        colour_WORDs=[int.from_bytes(image[a:a+2],'big') for a in range(plan['palette_start'],plan['palette_start']+32,2)])
    return result


def schema(rom):
    def obj(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def exact(items):return dict(type='array',prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def constant(value):
        if type(value) is dict:return obj({k:constant(v) for k,v in value.items()})
        if type(value) is list:return exact([constant(v) for v in value])
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(value)],const=value)
    def values(count,item):return dict(type='array',minItems=count,maxItems=count,items=item)
    WORD=dict(type='integer',minimum=0,maximum=65535)
    channel=dict(type='integer',minimum=0,maximum=7)
    color=obj(dict(red=channel,green=channel,blue=channel,
        reserved=dict(type='integer',enum=[i for i in range(65536) if i&~0xF111==0])))
    properties={k:constant(v) for k,v in metadata().items()}
    properties['token_sources']=exact([obj({**{k:constant(v) for k,v in token_fixed(rom,s,e).items()},
        'WORDs':values((e-s)//2,WORD)}) for s,e in TOKEN_SCOPES])
    properties['palette_sources']=exact([obj({**{k:constant(v) for k,v in palette_fixed(rom,s).items()},
        'colours':values(16,color)}) for s in PALETTE_STARTS])
    result=obj(properties);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='One editable physical authority:425 full tile-token WORDs and80 fullbits palette colours. Original witnesses are not unchanged edited safety or a natural index domain.'
    return result


def render_bundle(rom):
    fields=extract(rom);serialized=dump(fields);image=rebuild(rom,load_fields(serialized))
    if image!=rom:raise ValueError('serialized entire-ROM metadata roundtrip differs')
    rows=blocks(rom,fields)
    report=dict(**metadata(),editable_bytes=1010,physical_blocks=12,all_original_witnesses_verified=True,
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        source_union_sha256=sha(b''.join(row['data'] for row in rows)),
        blocks=[{k:v for k,v in row.items() if k!='data'}|dict(bytes=len(row['data']),sha256=sha(row['data'])) for row in rows])
    members={'fields.json':serialized,'fields.schema.json':dump(schema(rom)),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=1010,physical_blocks=12,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError('output must stay in portrait alias metadata build scope or exact formal bundle')
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
        result=dict(path=str(target),editable_bytes=1010,members={name:sha(data) for name,data in members.items()})
    elif args.command=='verify' and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS:raise ValueError('exact four-member bundle required')
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data:raise ValueError('canonical bundle drift: '+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=1010,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON));image=rebuild(rom,fields)
        if target is not None:put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=1010,bytes=len(image),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
