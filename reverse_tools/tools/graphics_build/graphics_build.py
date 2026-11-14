"""Edit pixel rows, tile attributes, CRAM channels and fixed graphics commands."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from tools.audio_formats import audio_formats as af
from tools.graphics_vdp import graphics_assets as title
from tools.duel_graphics import duel_graphics as duel
from tools.graphics_build import rle_fields as rf

FORMAT='g5510-fixed-graphics-fields-v1'
ASSETS=tuple(title.ASSETS)+tuple(duel.ASSETS)
EDITABLE_BYTES=sum(a.end-a.start for a in ASSETS)


def sha(data): return hashlib.sha256(data).hexdigest()
def dump(value): return (json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()


def kind(asset):
    if asset.kind.startswith('word_rle'): return 'word_rle'
    if asset.kind.startswith('lane_interleaved'): return 'lane_rle'
    if asset.name=='title_plane_b_left': return 'tilemap'
    if asset.name=='title_palette': return 'cram'
    if asset.name in ('duel_aux_raw_tiles','duel_palette_staging_candidate'): return 'transfer_longs'
    return 'tile_rows'


def metadata(asset): return {'id':asset.name,'start':asset.start,'end':asset.end,'kind':kind(asset)}


def verify_rom(rom):
    af.verify_rom(rom)
    title.validate_rom(rom)
    duel.validate_rom(rom)


def cell(word):
    rf.integer(word,65535,'tile word')
    return {'tile':word&2047,'hflip':(word>>11)&1,'vflip':(word>>12)&1,
            'palette':(word>>13)&3,'priority':word>>15}


def cell_word(fields):
    af._keys(fields,{'tile','hflip','vflip','palette','priority'},'tile attributes')
    return (rf.integer(fields['tile'],2047,'tile')|rf.integer(fields['hflip'],1,'hflip')<<11|
        rf.integer(fields['vflip'],1,'vflip')<<12|rf.integer(fields['palette'],3,'palette')<<13|
        rf.integer(fields['priority'],1,'priority')<<15)


def parse_fields(asset,raw):
    form=kind(asset)
    if form=='word_rle': return rf.parse_word(raw,asset.byte_order,asset.decoded_words)
    if form=='lane_rle': return rf.parse_lanes(raw)
    if form=='tilemap': return {'cells':[cell(int.from_bytes(raw[p:p+2],'big')) for p in range(0,len(raw),2)]}
    if form=='cram':
        return {'colours':[{'red':(w>>1)&7,'green':(w>>5)&7,'blue':(w>>9)&7,'reserved':w&0xF111}
            for w in (int.from_bytes(raw[p:p+2],'big') for p in range(0,len(raw),2))]}
    if form=='transfer_longs': return {'longs':[int.from_bytes(raw[p:p+4],'big') for p in range(0,len(raw),4)]}
    return {'tiles':[[raw[p+y*4:p+y*4+4].hex().upper() for y in range(8)] for p in range(0,len(raw),32)]}


def exact_list(value,count,label):
    if type(value) is not list or len(value)!=count: raise ValueError(label+' fixed count changed')
    return value


def pack_fields(asset,fields):
    form=kind(asset); size=asset.end-asset.start
    if form=='word_rle': raw,decoded=rf.pack_word(fields,asset.byte_order,asset.decoded_words)
    elif form=='lane_rle':
        raw,decoded=rf.pack_lanes(fields)
        duel.validate_tilemap(decoded,name=asset.name)
    elif form=='tilemap':
        af._keys(fields,{'cells'},'map fields')
        raw=b''.join(cell_word(c).to_bytes(2,'big') for c in exact_list(fields['cells'],size//2,'cells')); decoded=raw
    elif form=='cram':
        af._keys(fields,{'colours'},'CRAM fields'); raw=bytearray()
        for colour in exact_list(fields['colours'],64,'CRAM colours'):
            af._keys(colour,{'red','green','blue','reserved'},'CRAM colour')
            reserved=rf.integer(colour['reserved'],65535,'reserved')
            if reserved&~0xF111: raise ValueError('reserved bits overlap colour channels')
            word=reserved|rf.integer(colour['red'],7,'red')<<1|rf.integer(colour['green'],7,'green')<<5|rf.integer(colour['blue'],7,'blue')<<9
            raw.extend(word.to_bytes(2,'big'))
        raw=bytes(raw); decoded=raw
    elif form=='transfer_longs':
        af._keys(fields,{'longs'},'transfer fields')
        raw=b''.join(rf.integer(v,0xFFFFFFFF,'transfer long').to_bytes(4,'big') for v in exact_list(fields['longs'],size//4,'longs')); decoded=raw
    else:
        af._keys(fields,{'tiles'},'tile fields'); raw=bytearray()
        for tile in exact_list(fields['tiles'],size//32,'tiles'):
            for row in exact_list(tile,8,'tile rows'):
                if type(row) is not str or len(row)!=8 or any(c not in '0123456789ABCDEF' for c in row):
                    raise ValueError('pixel row requires eight uppercase colour-index nibbles')
                raw.extend(bytes.fromhex(row))
        raw=bytes(raw); decoded=raw
    if len(raw)!=size: raise ValueError(asset.name+' encoded fixed slot changed')
    return raw,decoded


def extract(rom):
    verify_rom(rom)
    return {'schema_version':1,'format':FORMAT,'assets':[
        {**metadata(a),'fields':parse_fields(a,rom[a.start:a.end])} for a in ASSETS]}


def blocks(rom,assets):
    verify_rom(rom); af._keys(assets,{'schema_version','format','assets'},'graphics assets')
    if type(assets['schema_version']) is not int or assets['schema_version']!=1 or assets['format']!=FORMAT:
        raise ValueError('graphics schema/format changed')
    result=[]
    for asset,value in zip(ASSETS,exact_list(assets['assets'],len(ASSETS),'assets')):
        af._keys(value,set(metadata(asset))|{'fields'},'graphics asset')
        for key,wanted in metadata(asset).items():
            if type(value[key]) is not type(wanted) or value[key]!=wanted: raise ValueError('fixed graphics metadata changed')
        raw,_=pack_fields(asset,value['fields'])
        result.append({'id':asset.name,'start':asset.start,'end':asset.end,'data':raw,'role':kind(asset)})
    return sorted(result,key=lambda r:r['start'])


def rebuild(rom,assets):
    result=bytearray(rom)
    for row in blocks(rom,assets): result[row['start']:row['end']]=row['data']
    return bytes(result)


def replace_decoded(rom,assets,ident,decoded):
    """Encode a decoded edit within its original slot and RLE grammar."""
    blocks(rom,assets)
    index=next((i for i,a in enumerate(ASSETS) if a.name==ident),None)
    if index is None: raise ValueError('unknown graphics asset')
    asset=ASSETS[index]; fields=assets['assets'][index]['fields']; raw,original=pack_fields(asset,fields)
    if type(decoded) is not bytes or len(decoded)!=len(original): raise ValueError('decoded extent changed')
    result=copy.deepcopy(assets)
    if decoded==original: return result
    if kind(asset)=='word_rle': new=rf.encode_word_exact(decoded,asset.byte_order,fields['marker'],len(raw))
    elif kind(asset)=='lane_rle':
        duel.validate_tilemap(decoded,name=ident)
        # The lane codec checks the exact-cost encoder output.
        encoded=duel.encode_lane_rle_exact(decoded,len(raw))
        new=rf.parse_lanes(encoded)
    else: new=parse_fields(asset,decoded)
    result['assets'][index]['fields']=new
    check=pack_fields(asset,new)[1]
    if check!=decoded: raise AssertionError('decoded edit failed verification')
    blocks(rom,result)
    return result


def manifest(rom):
    rows=blocks(rom,extract(rom))
    return {'schema_version':1,'format':FORMAT,'canonical_rom_sha256':sha(rom),
        'editable_bytes':EDITABLE_BYTES,'format_typed_bytes':EDITABLE_BYTES-320,
        'candidate_purpose_transfer_bytes':320,'owners':[],'ownership_bytes_added':0,
        'assets':[{**metadata(a),'sha256':sha(rom[a.start:a.end]),
            'layout_confidence':'confirmed','purpose_confidence':'candidate' if kind(a)=='transfer_longs' else
                ('confirmed' if a in title.ASSETS else 'probable'),
            'evidence':a.evidence,'decoded_sha256':sha(pack_fields(a,parse_fields(a,rom[a.start:a.end]))[1])} for a in ASSETS],
        'source_fields_sha256':sha(dump(extract(rom))),
        'boundaries':['title 065DF1..065DF3 remains outside every asset',
            'duel auxiliary and palette staging have transfer-long fields; purpose still candidate',
            'command fields preserve original representation; decoded re-encoding requires fixed slot fit',
            'tile rows contain eight colour-index nibbles',
            'resource writes use fixed cartridge offsets'],
        'intervals':[{k:r[k] for k in ('id','start','end','role')} for r in rows]}


def render_bundle(rom):
    return {'assets.json':dump(extract(rom)),'manifest.json':dump(manifest(rom)),
        'README.md':('# Fixed graphics field source\n\n'
        'Edit pixel and command fields in assets.json. The manifest describes their fixed slots.\n\n'
        '- Raw tiles: eight rows of eight hexadecimal pixel indices per tile, high nibble left.\n'
        '- Tilemaps: tile/hflip/vflip/palette/priority cover all16 bits. CRAM keeps reserved F111 bits.\n'
        '- Word RLE: explicit marker and literal/repeat commands; terminator derived.\n'
        '- Lane RLE: ordered high and low lanes; literal/repeat/pair/increment commands; 1280 outputs per lane.\n'
        '- Candidate duel transfers use big-endian 32-bit words.\n').encode()}


def publish(bundle,output,inputs):
    target=af.safe_path(output); af._separate(target,[af.safe_path(p,regular_input=True) for p in inputs])
    if target.exists() or not target.parent.is_dir(): raise ValueError('fresh output directory with existing parent required')
    reserved={'CON','PRN','AUX','NUL'}|{f'{p}{i}' for p in ('COM','LPT') for i in range(1,10)}
    if type(bundle) is not dict or not bundle or any(type(n) is not str or
        not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}',n) or n.endswith('.') or
        n.split('.')[0].upper() in reserved or type(d) is not bytes for n,d in bundle.items()):
        raise ValueError('flat byte bundle required')
    staging=Path(tempfile.mkdtemp(prefix='.graphics-fields-',dir=target.parent)); identity=staging.stat(); produced={}
    target_identity=None; linked={}; complete=False
    try:
        for name,data in bundle.items():
            with (staging/name).open('xb') as stream: stream.write(data)
            produced[name]=data
        af.safe_path(target)
        # mkdir is exclusive even against an empty concurrent target on POSIX.
        # Individual files are no-clobber links; only successful return promises
        # Files become visible individually inside the new directory.
        target.mkdir(); target_identity=target.stat()
        for name,data in bundle.items():
            af.safe_path(target); current=target.stat()
            if (current.st_dev,current.st_ino)!=(target_identity.st_dev,target_identity.st_ino):
                raise ValueError('output directory identity changed')
            os.link(staging/name,target/name); linked[name]=data
        complete=True
    finally:
        try:
            if target_identity is not None and not complete: af._cleanup_stage(target,linked,target_identity)
        finally: af._cleanup_stage(staging,produced,identity)
    return target


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','verify','import','replace-decoded'))
    parser.add_argument('--rom',type=Path,required=True,help='linear G-5510 BIN')
    parser.add_argument('--assets',type=Path,help='assets.json from a previous export')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--asset-id'); parser.add_argument('--decoded',type=Path)
    args=parser.parse_args()
    if args.command!='export' and args.assets is None:
        parser.error('--assets is required for verify, import and replace-decoded')
    read=lambda p: af._read(af.safe_path(p,regular_input=True),16*1024*1024)
    rom=read(args.rom); verify_rom(rom)
    if args.command=='export':
        if args.output is None: raise ValueError('--output required')
        print(publish(render_bundle(rom),args.output,[args.rom])); return
    assets=af.load_assets(read(args.assets)); image=rebuild(rom,assets)
    if args.command=='verify': print(json.dumps({'canonical_exact':image==rom,'sha256':sha(image),'editable_bytes':EDITABLE_BYTES})); return
    if args.output is None: raise ValueError('--output required')
    if args.command=='replace-decoded':
        if args.decoded is None or args.asset_id is None: raise ValueError('--asset-id and --decoded required')
        changed=replace_decoded(rom,assets,args.asset_id,read(args.decoded))
        print(publish({'assets.json':dump(changed)},args.output,[args.rom,args.assets,args.decoded])); return
    # Import publishes to a fresh output directory.
    print(publish({'rebuilt.bin':image,'manifest.json':dump({'sha256':sha(image),
        'canonical_exact':image==rom,'changed_bytes':sum(a!=b for a,b in zip(image,rom))})},args.output,[args.rom,args.assets]))


if __name__=='__main__': main()
