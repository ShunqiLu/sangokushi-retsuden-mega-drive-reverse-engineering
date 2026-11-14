"""Lossless editable 1bpp physical font rows and fixed-bank GNU assembly."""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from tools.audio_formats import audio_formats as af

DEFAULT_ROM = af.DEFAULT_ROM
DEFAULT_ASSETS = ROOT/'analysis/font_build/generated/assets.json'
FORMAT = 'g5510-fixed-physical-font-rows-v1'
# Physical allocations are not token domains or evidence of natural use.
FONTS = (
    {'id':'font16','start':0x08159C,'end':0x0896DC,'width':16,'height':16,'count':1034,
     'role':'font16_1bpp_rows','allocation_confidence':'probable',
     'sha256':reference_value(__name__, 'FONTS')},
    {'id':'font8','start':0x0896DC,'end':0x089EDC,'width':8,'height':8,'count':256,
     'role':'font8_1bpp_rows','allocation_confidence':'confirmed',
     'sha256':reference_value(__name__, 'FONTS_2')},
)
ANCHORS = (
    (0x00AEA2,'02840000ffff','shared 16x16 reader zero-extends the computed offset'),
    (0x00AEA8,'45f90008159c','shared 16x16 physical base'),
    (0x00AEAE,'45f24800','shared reader uses D4.L, unlike the main dialogue word-index reader'),
    (0x00AEB2,'3a3c000f','16 source rows; each iteration calls AF04 twice'),
    (0x00AF06,'1c1a','one source byte is consumed'),
    (0x00AF0C,'e98fe3166404','output shifts four bits; source rotates MSB through carry'),
    (0x00AF22,'42441818e74c','byte index, zero-extended word, multiplied by eight'),
    (0x00AF28,'45f9000896dc','8x8 physical base'),
    (0x00AF2E,'45f24000','8x8 word index remains nonnegative in the byte-index domain'),
    (0x00AF32,'3a3c0007','eight source rows'),
)


def sha(data): return hashlib.sha256(data).hexdigest()
def dump(value): return (json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8')


def verify_rom(rom):
    if type(rom) is not bytes: raise ValueError('canonical ROM must be bytes')
    af.verify_rom(rom)
    for font in FONTS:
        if sha(rom[font['start']:font['end']]) != font['sha256']:
            raise ValueError('physical font identity changed')
    for address,raw,_ in ANCHORS:
        if rom[address:address+len(bytes.fromhex(raw))] != bytes.fromhex(raw):
            raise ValueError('font consumer bytes changed')


def _metadata(font):
    return {key:font[key] for key in ('id','start','end','width','height')}


def extract(rom):
    verify_rom(rom)
    fonts=[]
    for font in FONTS:
        size=font['width']//8
        glyphs=[]
        for index in range(font['count']):
            start=font['start']+index*size*font['height']
            values=[int.from_bytes(rom[start+r*size:start+(r+1)*size],'big') for r in range(font['height'])]
            glyphs.append({'id':f"{font['id']}_{index:04d}",'rows':values})
        fonts.append({**_metadata(font),'glyphs':glyphs})
    return {'schema_version':1,'format':FORMAT,'fonts':fonts}


def blocks(rom,assets):
    verify_rom(rom)
    af._keys(assets,{'schema_version','format','fonts'},'font assets')
    if type(assets['schema_version']) is not int or assets['schema_version'] != 1 or assets['format'] != FORMAT:
        raise ValueError('font schema/format changed')
    if type(assets['fonts']) is not list or len(assets['fonts']) != 2:
        raise ValueError('exactly two physical fonts required')
    result=[]
    for value,font in zip(assets['fonts'],FONTS):
        af._keys(value,set(_metadata(font))|{'glyphs'},'font')
        for key,wanted in _metadata(font).items():
            if type(value[key]) is not type(wanted) or value[key] != wanted:
                raise ValueError('fixed font metadata changed')
        if type(value['glyphs']) is not list or len(value['glyphs']) != font['count']:
            raise ValueError('physical glyph count changed')
        size=font['width']//8; stride=size*font['height']
        for index,glyph in enumerate(value['glyphs']):
            af._keys(glyph,{'id','rows'},'glyph')
            ident=f"{font['id']}_{index:04d}"
            if type(glyph['id']) is not str or glyph['id'] != ident: raise ValueError('glyph id/order changed')
            if type(glyph['rows']) is not list or len(glyph['rows']) != font['height']:
                raise ValueError('fixed glyph row count changed')
            data=b''.join(af._integer(row,(1<<font['width'])-1,'bit row').to_bytes(size,'big') for row in glyph['rows'])
            start=font['start']+index*stride
            result.append({'id':ident,'start':start,'end':start+stride,'data':data,'role':font['role']})
    return result


def rebuild(rom,assets):
    rows=blocks(rom,assets)
    result=bytearray(rom)
    for row in rows: result[row['start']:row['end']]=row['data']
    return bytes(result)


def _block_font(row):
    af._keys(row,{'id','start','end','data','role'},'derived glyph block')
    font=next((f for f in FONTS if row['role']==f['role']),None)
    if font is None or type(row['start']) is not int or type(row['end']) is not int or type(row['data']) is not bytes:
        raise ValueError('invalid derived glyph block type')
    stride=font['height']*font['width']//8
    index=(row['start']-font['start'])//stride
    if (not 0<=index<font['count'] or row['start']!=font['start']+index*stride
        or row['end']!=row['start']+stride or len(row['data'])!=stride
        or row['id']!=f"{font['id']}_{index:04d}"):
        raise ValueError('derived glyph topology changed')
    return font


def block_lines(row,origin='font_bank_08'):
    """Inline row fields; origin labels the start of ROM bank08 in a caller's layout."""
    font=_block_font(row)
    if type(origin) is not str or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',origin):
        raise ValueError('invalid bank-origin symbol')
    size=font['width']//8
    values=[int.from_bytes(row['data'][r:r+size],'big') for r in range(0,len(row['data']),size)]
    directive='.word' if size==2 else '.byte'
    return [f"        .if (. - {origin}) != 0x{row['start']-0x80000:X}",
            '        .error "font glyph offset changed"','        .endif',f"{row['id']}:",
            f"        {directive} "+', '.join(f'0x{value:0{size*2}X}' for value in values)]


def bank_source(bank,rows):
    if type(bank) is not int or bank != 8 or type(rows) is not list or len(rows)!=1290:
        raise ValueError('complete bank08 font block list required')
    lines=['font_bank_08:']; cursor=0x80000
    for index,row in enumerate(rows):
        font=_block_font(row)
        expected=FONTS[0]['start']+index*32 if index<1034 else FONTS[1]['start']+(index-1034)*8
        if row['start']!=expected: raise ValueError('glyph blocks missing, duplicated or reordered')
        if cursor<row['start']:
            lines.append(f'        .incbin "segments/bank08.bin", 0x{cursor-0x80000:X}, 0x{row["start"]-cursor:X}')
        lines.extend(block_lines(row)); cursor=row['end']
    lines += [f'        .incbin "segments/bank08.bin", 0x{cursor-0x80000:X}, 0x{0x90000-cursor:X}',
              '        .if (. - font_bank_08) != 0x10000','        .error "font bank size changed"','        .endif']
    return ('\n'.join(lines)+'\n').encode('utf-8')


def asset_schema():
    def obj(properties): return {'type':'object','additionalProperties':False,'required':list(properties),'properties':properties}
    fonts=[]
    for font in FONTS:
        glyphs=[obj({'id':{'const':f"{font['id']}_{index:04d}"},'rows':{'type':'array',
            'minItems':font['height'],'maxItems':font['height'],'items':{'type':'integer','minimum':0,'maximum':(1<<font['width'])-1}}})
            for index in range(font['count'])]
        fonts.append(obj({**{key:{'const':value} for key,value in _metadata(font).items()},
            'glyphs':{'type':'array','minItems':font['count'],'maxItems':font['count'],'prefixItems':glyphs,'items':False}}))
    return {'$schema':'https://json-schema.org/draft/2020-12/schema',**obj({'schema_version':{'const':1},
        'format':{'const':FORMAT},'fonts':{'type':'array','minItems':2,'maxItems':2,'prefixItems':fonts,'items':False}})}


def manifest(rom):
    verify_rom(rom)
    return {'schema_version':1,'format':FORMAT,'canonical_source':{'size':af.ROM_SIZE,'sha256':af.ROM_SHA256},
        'editable_bytes':35136,'glyph_blocks':1290,'row_bitfields':18592,
        'owners':[],'ownership_bytes_added':0,'natural_use':'unknown','unicode_mapping':'unknown',
        'regions':[{**font,'layout_confidence':'confirmed','row_order':'top_to_bottom',
            'bit_order':'MSB_left','row_endianness':'big' if font['width']==16 else 'single_byte',
            'evidence':'analysis/text_font/TEXT_FONT_PIPELINE.md section3; canonical bytes and static consumer anchors'} for font in FONTS],
        'consumer_anchors':[{'address':address,'bytes':raw,'confidence':'confirmed','role':role} for address,raw,role in ANCHORS],
        'boundaries':['font16 end is inferred from the next font8 base; all1034 slots are not proved naturally consumed',
            'physical glyph IDs are NOT token values or Unicode characters',
            'main dialogue signed-word indexing differs from shared AE8A longword indexing; this codec maps neither',
            'new font data can be encoded exactly without proving edited display or gameplay correctness']}


def render_bundle(rom):
    assets=extract(rom)
    readme=('# Physical 1bpp font row source\n\n'
        'Confirmed row encoding and byte-exact fixed-layout codec; not a token/Unicode map.\n\n'
        '- font16: 1034 physical slots x16 big-endian16-bit rows =33088 bytes, 08159C..0896DC.\n'
        '- font8: 256 physical slots x8 byte rows =2048 bytes, 0896DC..089EDC.\n'
        '- Rows are top-to-bottom; most-significant bit is the leftmost pixel.\n'
        '- font16 layout/base confirmed; allocation end probable. font8 allocation/layout confirmed.\n'
        '- 1290 glyph blocks /18592 row bitfields /35136 editable bytes; owners added0.\n'
        '- assets.json is the sole row-bitfield authority. bank08.s is derived, not a second editable source.\n'
        '- Manifest records canonical evidence separately; editable rows are not sealed to original values.\n'
        '- Physical tail slots are retained without asserting Unicode or natural usage.\n'
        '- Shared AE8A uses a longword offset; main dialogue uses a signed word. No token resolver is provided.\n'
        '- The generated bank08 assembly contains explicit raw gaps and only typed .word/.byte glyph fields.\n')
    return {'assets.json':dump(assets),'assets.schema.json':dump(asset_schema()),'manifest.json':dump(manifest(rom)),
            'bank08.s':bank_source(8,blocks(rom,assets)),'README.md':readme.encode('utf-8')}


def export_files(rom_path,output):
    source=af.safe_path(rom_path,regular_input=True); target=af.safe_path(output)
    af._separate(target,[source])
    if target.exists() or not target.parent.is_dir(): raise ValueError('fresh output directory with existing parent required')
    bundle=render_bundle(af._read(source,af.ROM_SIZE))
    staging=Path(tempfile.mkdtemp(prefix='.font-build-',dir=target.parent)); identity=staging.stat(); produced={}
    try:
        for name,data in bundle.items():
            with (staging/name).open('xb') as stream: stream.write(data)
            produced[name]=data
        af.safe_path(output)
        if target.exists(): raise ValueError('output appeared during generation')
        os.rename(staging,target)
    finally: af._cleanup_stage(staging,produced,identity)
    return {'output':str(target),'files':sorted(bundle),'ownership_bytes_added':0}


def import_files(rom_path,asset_path,output):
    source=af.safe_path(rom_path,regular_input=True); asset=af.safe_path(asset_path,regular_input=True)
    target=af.safe_path(output); af._separate(target,[source,asset])
    if target.exists() or not target.parent.is_dir(): raise ValueError('fresh output file with existing parent required')
    rom=af._read(source,af.ROM_SIZE); result=rebuild(rom,af.load_assets(af._read(asset,8*1024*1024)))
    descriptor,name=tempfile.mkstemp(prefix='.font-build-',dir=target.parent)
    temporary=Path(name); identity=temporary.stat(); complete=False
    try:
        with os.fdopen(descriptor,'wb') as stream:
            stream.write(result); stream.flush(); os.fsync(stream.fileno())
        complete=True
        af.safe_path(output)
        os.link(temporary,target)  # Atomic no-clobber publication of the new image.
    finally:
        if temporary.exists():
            af.safe_path(temporary,regular_input=True); current=temporary.stat()
            if complete and (current.st_dev,current.st_ino)==(identity.st_dev,identity.st_ino) and af._read(temporary,len(result))==result:
                temporary.unlink()
            else: raise ValueError('incomplete or modified temporary image retained')
    return {'output':str(target),'sha256':sha(result),'canonical_exact':result==rom,
            'changed_bytes':sum(a!=b for a,b in zip(result,rom))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','verify','import'))
    parser.add_argument('--rom',type=Path,default=DEFAULT_ROM)
    parser.add_argument('--assets',type=Path,default=DEFAULT_ASSETS)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.command=='export':
        if args.output is None: raise ValueError('--output required')
        result=export_files(args.rom,args.output)
    elif args.command=='import':
        if args.output is None: raise ValueError('--output required')
        result=import_files(args.rom,args.assets,args.output)
    else:
        rom=af._read(af.safe_path(args.rom,regular_input=True),af.ROM_SIZE)
        assets=af.load_assets(af._read(af.safe_path(args.assets,regular_input=True),8*1024*1024))
        image=rebuild(rom,assets)
        result={'sha256':sha(image),'canonical_exact':image==rom,'editable_bytes':35136}
    print(json.dumps(result))


if __name__=='__main__': main()
