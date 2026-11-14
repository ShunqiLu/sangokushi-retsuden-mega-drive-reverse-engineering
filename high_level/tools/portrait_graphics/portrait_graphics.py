"""Indexed-image mechanics at 0661D4; physical allocations remain probable.

The package name is a candidate purpose, not a natural-use or identity claim.
Canonical evidence is separate from the one editable field source. The pure
address model accepts the complete machine word domain, while the editor only
allows references to the fixed, originally selected physical resources.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from tools.audio_formats import audio_formats as af
from tools.graphics_build import graphics_build as gb

DEFAULT_ROM=af.DEFAULT_ROM
DEFAULT_ASSETS=ROOT/'analysis/portrait_graphics/generated/assets.json'
FORMAT='g5510-indexed-image-fields-v1'
TABLES=(('primary',0xAE39A,48),('secondary8',0xB439A,8),('secondary4',0xB539A,4))
SELECTORS=0xB639A
PALETTE_BIAS=0xB599A
TILES=0xB649A
EDITABLE_BYTES=126400
CONSUMER_SHA=reference_value(__name__, 'CONSUMER_SHA')
# Canonical holes, independently re-derived and checked by _topology. These
# support safe field-renderer validation without reading any file implicitly.
UNSELECTED_TILE_RANGES=((1,7),(255,263),(511,519),(767,768),(836,840),(1024,1025),
    (1061,1062),(1278,1282),(1404,1420),(1536,1537),(1667,1689),(1690,1697),
    (1727,1751),(1792,1793),(1930,1936),(1956,1957),(2021,2025),(2116,2120),
    (2167,2168),(2304,2305),(2426,2427),(2559,2561),(2816,2817),(2845,2846),
    (2856,2866),(3035,3036))
SELECTED_TILES=frozenset(TILES+32*i for i in range(0xBF4)
    if not any(a<=i<b for a,b in UNSELECTED_TILE_RANGES))
CALLERS=(
    (0x94C,'46fc27003038f3a6323c00054eb9000661d4','FF F3A6 word; no local index clamp'),
    (0xB5B8,'3038f372323c00054eb9000661d4','FF F372 word; no local index clamp'),
    (0x355DA,'3038f348103b005e31c0f34a323c00054eb9000661d4','FF F348 word indexes 03563E; MOVE.B preserves D0 bits8..31'),
    (0x3DE10,'303880e0323c04804eb9000661d4','FF 80E0 word; no local index clamp'),
    (0x3DFF0,'303880e0323c04804eb9000661d4','FF 80E0 word; no local index clamp'),
    (0x3E0AA,'303880e0323c04804eb9000661d4','FF 80E0 word; no local index clamp'),
)


def sha(data): return hashlib.sha256(data).hexdigest()
def dump(value): return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def integer(value,maximum,label): return af._integer(value,maximum,label)
def signed_word(value):
    value=integer(value,65535,'word')
    return value if value<0x8000 else value-0x10000


def verify_rom(rom):
    if type(rom) is not bytes: raise ValueError('canonical ROM bytes required')
    af.verify_rom(rom)
    if sha(rom[0x661D4:0x662E4])!=CONSUMER_SHA: raise ValueError('indexed reader changed')
    for start,raw,_ in CALLERS:
        if rom[start:start+len(bytes.fromhex(raw))]!=bytes.fromhex(raw): raise ValueError('caller changed')


def address_plan(d0,d1=5,f6c4=0):
    """Exact local address arithmetic, not CPU execution or scheduler emulation.

    D0 and D1 are full register inputs. Only their low words affect addresses.
    All additions are 32-bit address arithmetic; no emulated 24-bit bus mapping.
    No caller-domain clamp is added. Reads outside the chosen allocations are
    represented as addresses, not silently redirected to a valid image.
    """
    index=integer(d0,0xFFFFFFFF,'D0')&65535
    source=(integer(d1,0xFFFFFFFF,'D1')&65535)<<7
    source=(source&0xFFFF0000)|((source&65535)>>2)|0x4000
    command=((source<<16)|(source>>16))&0xFFFFFFFF
    flag=integer(f6c4,65535,'F6C4')
    return {'index_word':index,'tables':{kind:(base+signed_word((index*count*2)&65535))&0xFFFFFFFF
            for kind,base,count in TABLES},
        'selector_address':(SELECTORS+signed_word(index))&0xFFFFFFFF,
        'vdp_control_long':command,'palette_destination':0xFFFFFB20 if flag==2 else 0xFFFFFB00,
        'palette_copy_longs':8,'final_F31E_word':1}


def token_reads(token,path):
    """Eight real source-long addresses, preserving secondary word aliases."""
    token=integer(token,65535,'tile token')
    if path=='primary': return [TILES+token*32+4*i for i in range(8)]
    if path not in ('secondary8','secondary4'): raise ValueError('unknown token path')
    base=TILES+(0x10000 if token>=0x800 else 0)
    offset=(token<<5)&65535
    return [(base+signed_word((offset+i*4)&65535))&0xFFFFFFFF for i in range(8)]


def mapped_caller_index(rom,f348):
    """0355DA..E2 only; word high byte survives the LUT byte replacement."""
    verify_rom(rom); f348=integer(f348,65535,'F348')
    address=0x3563E+signed_word(f348)
    if not 0<=address<len(rom): raise ValueError('caller LUT read outside canonical ROM')
    return (f348&0xFF00)|rom[address]


def _words(rom,start,count):
    return [int.from_bytes(rom[start+2*i:start+2*i+2],'big') for i in range(count)]


def _topology(rom):
    # Callers do not prove this domain. It is the audited probable physical
    # allocation, bounded by the next table and by the actual palette selectors.
    tile_starts=set()
    for path,base,count in TABLES:
        for token in _words(rom,base,256*count):
            addresses=token_reads(token,path)
            if addresses!=list(range(addresses[0],addresses[0]+32,4)):
                raise ValueError('canonical token unexpectedly crosses a signed discontinuity')
            tile_starts.add(addresses[0])
    selectors=sorted(set(rom[SELECTORS:SELECTORS+256]))
    if tile_starts!=SELECTED_TILES or len(selectors)!=59 or min(selectors)!=16 or max(selectors)!=75 or 36 in selectors:
        raise ValueError('canonical physical topology changed')
    return sorted(tile_starts),selectors


def colour(word):
    return {'red':(word>>1)&7,'green':(word>>5)&7,'blue':(word>>9)&7,'reserved':word&0xF111}


def colour_word(value):
    af._keys(value,{'red','green','blue','reserved'},'palette colour')
    reserved=integer(value['reserved'],65535,'reserved')
    if reserved&~0xF111: raise ValueError('reserved bits overlap channels')
    return reserved|(integer(value['red'],7,'red')<<1)|(integer(value['green'],7,'green')<<5)|(integer(value['blue'],7,'blue')<<9)


def exact_list(value,count,label):
    if type(value) is not list or len(value)!=count: raise ValueError(label+' fixed count changed')
    return value


def extract(rom):
    verify_rom(rom); tile_starts,selectors=_topology(rom)
    images=[]
    for index in range(256):
        images.append({'id':f'image_{index:03d}',**{kind:_words(rom,base+index*count*2,count)
            for kind,base,count in TABLES},'palette_selector':rom[SELECTORS+index]})
    return {'schema_version':1,'format':FORMAT,'images':images,
        'palettes':[{'selector':selector,'colours':[colour(w) for w in _words(rom,PALETTE_BIAS+selector*32,16)]}
            for selector in selectors],
        'tiles':[{'id':f'tile_{(start-TILES)//32:04X}','start':start,
            'rows':[rom[start+y*4:start+(y+1)*4].hex().upper() for y in range(8)]} for start in tile_starts]}


def blocks(rom,assets):
    verify_rom(rom); af._keys(assets,{'schema_version','format','images','palettes','tiles'},'image assets')
    if type(assets['schema_version']) is not int or assets['schema_version']!=1 or assets['format']!=FORMAT:
        raise ValueError('schema/format changed')
    tile_starts,selectors=_topology(rom); allowed_tiles=set(tile_starts); allowed_palettes=set(selectors)
    rows=[]
    for index,value in enumerate(exact_list(assets['images'],256,'images')):
        af._keys(value,{'id','primary','secondary8','secondary4','palette_selector'},'image')
        if type(value['id']) is not str or value['id']!=f'image_{index:03d}': raise ValueError('image identity/order changed')
        for kind,base,count in TABLES:
            values=exact_list(value[kind],count,kind)
            for token in values:
                addresses=token_reads(token,kind)
                if addresses[0] not in allowed_tiles or addresses!=list(range(addresses[0],addresses[0]+32,4)):
                    raise ValueError('editor reference leaves the fixed selected tile allocation')
            raw=b''.join(token.to_bytes(2,'big') for token in values); start=base+index*count*2
            rows.append({'id':f'pg_{kind}_{index:03d}','start':start,'end':start+len(raw),'data':raw,'role':'tile_tokens_'+kind})
        selector=integer(value['palette_selector'],255,'palette selector')
        if selector not in allowed_palettes: raise ValueError('editor reference leaves the fixed selected palettes')
        rows.append({'id':f'pg_selector_{index:03d}','start':SELECTORS+index,'end':SELECTORS+index+1,
            'data':bytes([selector]),'role':'palette_selector'})
    for selector,value in zip(selectors,exact_list(assets['palettes'],59,'palettes')):
        af._keys(value,{'selector','colours'},'palette')
        if type(value['selector']) is not int or value['selector']!=selector: raise ValueError('palette identity/order changed')
        raw=b''.join(colour_word(c).to_bytes(2,'big') for c in exact_list(value['colours'],16,'colours'))
        start=PALETTE_BIAS+selector*32
        rows.append({'id':f'pg_palette_{selector:03d}','start':start,'end':start+32,'data':raw,'role':'palette_channels'})
    for start,value in zip(tile_starts,exact_list(assets['tiles'],2923,'tiles')):
        af._keys(value,{'id','start','rows'},'tile')
        ident=f'tile_{(start-TILES)//32:04X}'
        if type(value['id']) is not str or value['id']!=ident or type(value['start']) is not int or value['start']!=start:
            raise ValueError('tile identity/order changed')
        raw=bytearray()
        for bits in exact_list(value['rows'],8,'tile rows'):
            if type(bits) is not str or not re.fullmatch('[0-9A-F]{8}',bits): raise ValueError('eight uppercase pixel nibbles required')
            raw.extend(bytes.fromhex(bits))
        rows.append({'id':'pg_'+ident,'start':start,'end':start+32,'data':bytes(raw),'role':'tile_pixel_rows'})
    rows.sort(key=lambda r:r['start'])
    if any(a['end']>b['start'] for a,b in zip(rows,rows[1:])): raise ValueError('typed blocks overlap')
    if sum(r['end']-r['start'] for r in rows)!=EDITABLE_BYTES: raise ValueError('typed extent changed')
    return rows


def rebuild(rom,assets):
    result=bytearray(rom)
    for row in blocks(rom,assets): result[row['start']:row['end']]=row['data']
    return bytes(result)


def conditional_read(rom,d0,d1=5,f6c4=0):
    """Canonical-ROM static read projection. No RAM/IRQ/VDP-side simulation.

    Reads through any in-ROM arithmetic result, even outside editor allocations;
    an out-of-ROM request fails explicitly. Palette writes/flag writes are only
    reported, not applied to invented hardware or CPU stack state.
    """
    verify_rom(rom); plan=address_plan(d0,d1,f6c4); transfers=[]
    def read(address,size):
        if not 0<=address<=len(rom)-size: raise ValueError(f'conditional read outside ROM: {address:08X}')
        return rom[address:address+size]
    for path,_,count in TABLES:
        start=plan['tables'][path]
        for i in range(count):
            address=start+i*2; token=int.from_bytes(read(address,2),'big')
            sources=token_reads(token,path); data=b''.join(read(p,4) for p in sources)
            transfers.append({'path':path,'token_address':address,'token':token,'source_longs':sources,'data_hex':data.hex().upper()})
    selector=read(plan['selector_address'],1)[0]; palette_source=PALETTE_BIAS+selector*32
    return {**plan,'tiles':transfers,'palette_selector':selector,'palette_source':palette_source,
        'palette_hex':read(palette_source,32).hex().upper(),'projection_kind':'conditional_static_rom_reads',
        'natural_execution':False,'unmodelled':['CPU stack and register lifetime','asynchronous writes/IRQ','VDP configuration and presentation']}


def _block_shape(row):
    af._keys(row,{'id','start','end','data','role'},'derived block')
    if type(row['id']) is not str or not re.fullmatch('pg_[A-Za-z0-9_]+',row['id']): raise ValueError('block symbol changed')
    if type(row['start']) is not int or type(row['end']) is not int or type(row['data']) is not bytes:
        raise ValueError('block field types changed')
    role=row['role']; start=row['start']; end=row['end']; valid=False
    if type(role) is not str: raise ValueError('block role changed')
    for kind,base,count in TABLES:
        index=(start-base)//(count*2)
        if role=='tile_tokens_'+kind and 0<=index<256 and start==base+index*count*2:
            valid=end==start+count*2 and row['id']==f'pg_{kind}_{index:03d}'
    if role=='palette_selector': valid=SELECTORS<=start<SELECTORS+256 and end==start+1 and row['id']==f'pg_selector_{start-SELECTORS:03d}'
    if role=='palette_channels':
        selector=(start-PALETTE_BIAS)//32
        valid=16<=selector<=75 and selector!=36 and start==PALETTE_BIAS+selector*32 and end==start+32 and row['id']==f'pg_palette_{selector:03d}'
    if role=='tile_pixel_rows':
        index=(start-TILES)//32
        valid=start in SELECTED_TILES and start==TILES+index*32 and end==start+32 and row['id']==f'pg_tile_{index:04X}'
    if not valid or len(row['data'])!=end-start: raise ValueError('derived block topology changed')


def block_lines(row,origin):
    """Typed inline fields; origin denotes the bank containing the block.

    A bank-crossing primary header and tile have explicit per-field fragments;
    use block_fragments first for bank output or a combined caller layout.
    """
    _block_shape(row)
    if type(origin) is not str or not re.fullmatch('[A-Za-z_][A-Za-z0-9_]*',origin): raise ValueError('bad origin symbol')
    if row['start']//65536!=(row['end']-1)//65536: raise ValueError('cross-bank block requires block_fragments')
    offset=row['start']&65535; raw=row['data']; width=1 if row['role']=='palette_selector' else 2
    if row['role']=='tile_pixel_rows': width=1
    lines=[f'        .if (. - {origin}) != 0x{offset:X}','        .error "indexed field offset changed"','        .endif',row['id']+':']
    for p in range(0,len(raw),16):
        values=[int.from_bytes(raw[q:q+width],'big') for q in range(p,min(p+16,len(raw)),width)]
        lines.append('        '+('.byte' if width==1 else '.word')+' '+', '.join(f'0x{x:0{width*2}X}' for x in values))
    return lines


def block_fragments(row,bank,origin):
    """Render one block's intersection with a bank, using typed row bytes.

    Fragments are derived only, never competing editable pixel authorities.
    """
    _block_shape(row); integer(bank,15,'bank')
    if type(origin) is not str or not re.fullmatch('[A-Za-z_][A-Za-z0-9_]*',origin): raise ValueError('bad origin symbol')
    start=max(row['start'],bank*65536); end=min(row['end'],(bank+1)*65536)
    if start>=end: return []
    if start==row['start'] and end==row['end']: return block_lines(row,origin)
    if row['role'] not in ('tile_pixel_rows','tile_tokens_primary'): raise ValueError('unexpected cross-bank field')
    raw=row['data'][start-row['start']:end-row['start']]
    width=2 if row['role']=='tile_tokens_primary' else 1
    if len(raw)%width: raise ValueError('field fragment splits a word')
    return [f'        .if (. - {origin}) != 0x{start-bank*65536:X}',
        '        .error "indexed pixel fragment offset changed"','        .endif',
        f"{row['id']}_bank{bank:02x}:",
        '        '+('.word' if width==2 else '.byte')+' '+', '.join(
            f'0x{int.from_bytes(raw[p:p+width],"big"):0{width*2}X}' for p in range(0,len(raw),width))]


def bank_source(bank,rows):
    integer(bank,15,'bank')
    if type(rows) is not list: raise ValueError('derived blocks list required')
    for row in rows: _block_shape(row)
    if any(a['start']>=b['start'] or a['end']>b['start'] for a,b in zip(rows,rows[1:])): raise ValueError('blocks unordered/overlapping')
    if len(rows)!=4006 or sum(r['end']-r['start'] for r in rows)!=EDITABLE_BYTES:
        raise ValueError('complete derived field set required')
    origin=f'portrait_bank_{bank:02x}'; cursor=bank*65536; end=(bank+1)*65536; lines=[origin+':']
    for row in rows:
        lo=max(cursor,row['start']); hi=min(end,row['end'])
        if lo>=hi: continue
        if cursor<lo: lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{lo-cursor:X}')
        lines.extend(block_fragments(row,bank,origin)); cursor=hi
    if cursor<end: lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{end-cursor:X}')
    lines += [f'        .if (. - {origin}) != 0x10000','        .error "indexed bank size changed"','        .endif']
    return ('\n'.join(lines)+'\n').encode()


def asset_schema(rom):
    verify_rom(rom)
    tile_starts,selectors=_topology(rom)
    def obj(props): return {'type':'object','additionalProperties':False,'required':list(props),'properties':props}
    def array(items,count): return {'type':'array','minItems':count,'maxItems':count,'items':items}
    def fixed(items): return {'type':'array','minItems':len(items),'maxItems':len(items),'prefixItems':items,'items':False}
    uint={'type':'integer','minimum':0,'maximum':65535}
    image_props={kind:array(uint,count) for kind,_,count in TABLES}
    colours=obj({**{key:{'type':'integer','minimum':0,'maximum':7} for key in ('red','green','blue')},
        'reserved':{'type':'integer','minimum':0,'maximum':65535,'description':'only F111 mask bits; enforced by importer'}})
    return {'$schema':'https://json-schema.org/draft/2020-12/schema',**obj({'schema_version':{'type':'integer','const':1},
        'format':{'const':FORMAT},'images':fixed([obj({'id':{'const':f'image_{i:03d}'},**image_props,
            'palette_selector':{'type':'integer','enum':selectors}}) for i in range(256)]),
        'palettes':fixed([obj({'selector':{'type':'integer','const':s},'colours':array(colours,16)}) for s in selectors]),
        'tiles':fixed([obj({'id':{'const':f'tile_{(start-TILES)//32:04X}'},'start':{'type':'integer','const':start},
            'rows':array({'type':'string','pattern':'^[0-9A-F]{8}$'},8)}) for start in tile_starts])})}


def manifest(rom):
    assets=extract(rom); rows=blocks(rom,assets)
    intervals=[{key:row[key] for key in ('id','start','end','role')}|{'sha256':sha(row['data']),
        'allocation_confidence':'probable','mechanics_confidence':'confirmed'} for row in rows]
    gaps=[]; cursor=TABLES[0][1]
    for row in rows:
        if cursor<row['start']: gaps.append({'start':cursor,'end':row['start'],'confidence':'unknown','reason':'not a selected physical field'})
        cursor=row['end']
    return {'schema_version':1,'format':FORMAT,'canonical_source':{'size':len(rom),'sha256':sha(rom)},
        'editable_bytes':EDITABLE_BYTES,'header_palette_bytes':32864,'tile_bytes':93536,'blocks':len(rows),
        'image_allocations':256,'selected_tile_allocations':2923,'selected_palette_allocations':59,
        'owners':[],'ownership_bytes_added':0,'confirmed_ownership_intervals':[],
        'purpose_confidence':'candidate','natural_execution':False,'all_id_domain_proven':False,
        'consumer':{'start':0x661D4,'end':0x662E4,'sha256':CONSUMER_SHA,'bytes':rom[0x661D4:0x662E4].hex(),
            'confidence':'confirmed','claim':'instruction bytes and conditional mechanics, not natural execution'},
        'callers':[{'start':start,'bytes':raw,'claim':claim,'confidence':'confirmed','global_domain':'unknown'} for start,raw,claim in CALLERS],
        'conditional_intro_lut':{'start':0x3563E,'bytes':rom[0x3563E:0x35644].hex(),'indices':[mapped_caller_index(rom,i) for i in range(6)],
            'confidence':'confirmed','precondition':'F348.word is 0..5 at 0355DA; reset/IRQ/alias lifetime not closed'},
        'source_fields_sha256':sha(dump(assets)),'intervals':intervals,'gaps':gaps,
        'boundaries':['all 256 image allocations probable; six caller word domains not globally closed',
            'B599A is a biased palette base inside the third table, not its end; third table ends B5B9A',
            'selected palette36 absent; unselected palette and raw tile holes remain untouched/unknown',
            'primary long offset and secondary signed-word alias formulas are intentionally distinct',
            'importer selected-resource restriction is editing policy, not a CPU bounds check',
            'no identity/portrait business label, natural rendering, ownership or complete indirect-site promotion']}


def render_bundle(rom):
    assets=extract(rom); rows=blocks(rom,assets)
    return {'assets.json':dump(assets),'assets.schema.json':dump(asset_schema(rom)),'manifest.json':dump(manifest(rom)),
        **{f'bank{bank:02x}.s':bank_source(bank,rows) for bank in (10,11,12)},
        'README.md':('# Indexed image fields\n\n'
            'Confirmed conditional mechanics; probable allocations; candidate portrait purpose.\n\n'
            '- 256 image slots: primary48, secondary8, secondary4 BE16 tokens and byte palette selector.\n'
            '- 59 selected 16-colour records, preserving F111 reserved bits; 2923 unique32-byte pixel tiles.\n'
            '- 126400 editable bytes /4006 blocks; new ownership0. Physical unselected gaps remain unknown.\n'
            '- assets.json alone is editable. Shared palettes/tiles have one authoritative field record.\n'
            '- Palette base B599A is biased; the third table has256 slots ending B5B9A.\n'
            '- Actual secondary arithmetic uses unsigned0800 comparison followed by signed WORD shift5.\n'
            '- Address model accepts full machine inputs, importer requires fixed selected resources.\n'
            '- No natural runtime capture, all-ID domain, image identity or edited display guarantee.\n'
            '- Derived bank0A/0B/0C field assembly retains explicit raw gaps; primary075 and tile04DB cross banks.\n').encode()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','verify','import'))
    parser.add_argument('--rom',type=Path,default=DEFAULT_ROM)
    parser.add_argument('--assets',type=Path,default=DEFAULT_ASSETS)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    source=af.safe_path(args.rom,regular_input=True); rom=af._read(source,af.ROM_SIZE); verify_rom(rom)
    if args.command=='export':
        if args.output is None: raise ValueError('--output required')
        print(gb.publish(render_bundle(rom),args.output,[source])); return
    source_assets=af.safe_path(args.assets,regular_input=True)
    assets=af.load_assets(af._read(source_assets,16*1024*1024)); image=rebuild(rom,assets)
    result={'sha256':sha(image),'canonical_exact':image==rom,'editable_bytes':EDITABLE_BYTES,
        'changed_bytes':sum(a!=b for a,b in zip(image,rom))}
    if args.command=='verify': print(json.dumps(result)); return
    if args.output is None: raise ValueError('--output required')
    print(gb.publish({'rebuilt.bin':image,'validation.json':dump(result)},args.output,[source,source_assets]))


if __name__=='__main__': main()
