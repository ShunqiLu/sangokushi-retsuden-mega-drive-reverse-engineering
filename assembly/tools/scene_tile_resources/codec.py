"""Fixed palette, 4bpp tiles and six map-RLE streams; purpose is candidate.

Source fields are the sole editable authority. 256 tiles/bank and 1024 map
WORDs are original allocation contracts, not limits on the original CPU.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from tools.audio_formats import audio_formats as af
from tools.vdp_word_streams import format as f
from tools.graphics_build import rle_fields as rle

ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=af.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/scene_tile_resources/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/scene_tile_resources'
FORMAT='candidate-fixed-vdp-scene-fields-v1'
PALETTE=(0x2B46E,0x2B4EE)
TILES=((0x2B4EE,0x2D4EE),(0x2D4EE,0x2F4EE))
MAPS=((0x2F4EE,0x2FA03),(0x2FA03,0x2FB8E),(0x2FB8E,0x2FDEF),
      (0x2FDEF,0x2FF1A),(0x2FF1A,0x2FFB9),(0x2FFB9,0x30088))
MAP_LOADS=(0x2B240,0x2B256,0x2B270,0x2B286,0x2B29C,0x2B2C2)
EDITABLE_BYTES=19482
keys=f.keys;uint=f.uint;sha=f.sha;dump=f.dump;load_fields=f.load_json

def exact_list(value,count,label):
    if type(value)is not list or len(value)!=count:raise ValueError(label+': fixed list allocation differs')
    return value
def ident(start,role):return f'rom_{start:06X}_{role}'
def metadata():return dict(format=FORMAT,source=dict(size=af.ROM_SIZE,sha256=af.ROM_SHA256),
    confidence='candidate',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def topology(start,end,role):return dict(id=ident(start,role),start=start,end=end)
def colour(word):return dict(red=(word>>1)&7,green=(word>>5)&7,blue=(word>>9)&7,reserved=word&0xF111)
def colour_word(row):
    keys(row,{'red','green','blue','reserved'},'CRAM colour')
    reserved=uint(row['reserved'],65535,'reserved')
    if reserved&~0xF111:raise ValueError('reserved bits overlap colour channels')
    return reserved|uint(row['red'],7,'red')<<1|uint(row['green'],7,'green')<<5|uint(row['blue'],7,'blue')<<9
def check_row(row,fixed,mutable,label):
    keys(row,set(fixed)|set(mutable),label)
    for key,value in fixed.items():f.same(row[key],value,label+'.'+key)
def evidence(rom):
    # Each PC-relative displacement is evaluated from its original extension
    # WORD address, rather than accepted because a disassembler names a target.
    loads=[(0x2B2E8,PALETTE[0])]+list(zip((0x2B208,0x2B224),(a for a,z in TILES)))+list(zip(MAP_LOADS,(a for a,z in MAPS)))
    result=[]
    for pc,target in loads:
        raw=rom[pc:pc+4]
        if raw[:2]!=b'\x41\xfa':raise ValueError('original LEA opcode changed')
        delta=int.from_bytes(raw[2:],'big',signed=True)
        if pc+2+delta!=target:raise ValueError('original PC-relative resource xref differs')
        result.append(dict(pc=pc,bytes=raw.hex(),target=target,confidence='confirmed'))
    for pc in (0x2B20E,0x2B22A):
        if rom[pc:pc+12]!=bytes.fromhex('203c000007ff2c9851c8fffc'):raise ValueError('original2048 LONG VDP upload changed')
    if rom[0x2B2EE:0x2B2FC]!=bytes.fromhex('43f8fb00303c001f22d851c8fffc'):raise ValueError('original32 LONG palette copy changed')
    return result

def extract(rom):
    af.verify_rom(rom);evidence(rom);result=metadata()
    a,z=PALETTE;result['palette']={**topology(a,z,'palette'),
        'colours':[colour(int.from_bytes(rom[p:p+2],'big')) for p in range(a,z,2)]}
    result['tile_banks']=[]
    for a,z in TILES:
        tiles=[]
        for p in range(a,z,32):
            pixels=[[n for value in rom[p+4*y:p+4*y+4] for n in (value>>4,value&15)] for y in range(8)]
            tiles.append(dict(id=ident(p,'tile'),pixels=pixels))
        result['tile_banks'].append({**topology(a,z,'tiles'),'tiles':tiles})
    result['maps']=[{**topology(a,z,'map'),'decoded_words':1024,'fields':rle.parse_word(rom[a:z],'big',1024)} for a,z in MAPS]
    blocks(rom,result)
    return result

def blocks(rom,fields):
    af.verify_rom(rom);keys(fields,set(metadata())|{'palette','tile_banks','maps'},'package')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    result=[]
    def add(a,z,data,role):
        if type(data)is not bytes or len(data)!=z-a:raise ValueError('fixed encoded slot differs')
        result.append(dict(id=ident(a,role),start=a,end=z,data=data,role=role))
    a,z=PALETTE;row=fields['palette'];check_row(row,topology(a,z,'palette'),{'colours'},'palette')
    raw=b''.join(colour_word(v).to_bytes(2,'big') for v in exact_list(row['colours'],64,'palette colours'))
    add(a,z,raw,'candidate_cram_channels')
    for row,(a,z) in zip(exact_list(fields['tile_banks'],2,'tile banks'),TILES):
        check_row(row,topology(a,z,'tiles'),{'tiles'},'tile bank');raw=bytearray()
        for tile,p in zip(exact_list(row['tiles'],256,'256 tile allocations'),range(a,z,32)):
            keys(tile,{'id','pixels'},'tile');f.same(tile['id'],ident(p,'tile'),'tile id')
            for pixel_row in exact_list(tile['pixels'],8,'tile rows'):
                values=exact_list(pixel_row,8,'8 pixel indices')
                n=[uint(v,15,'4bpp palette index') for v in values]
                raw.extend((n[x]<<4)|n[x+1] for x in range(0,8,2))
        add(a,z,bytes(raw),'candidate_vdp_4bpp_tiles')
    for row,(a,z) in zip(exact_list(fields['maps'],6,'map streams'),MAPS):
        check_row(row,{**topology(a,z,'map'),'decoded_words':1024},{'fields'},'map')
        f.strict_commands(row['fields']);encoded,decoded=rle.pack_word(row['fields'],'big',1024)
        if len(encoded)!=z-a or rle.parse_word(encoded,'big',1024)!=row['fields']:raise ValueError('map allocation/read boundary differs')
        add(a,z,encoded,'candidate_big_word_rle_map')
    if sum(r['end']-r['start'] for r in result)!=EDITABLE_BYTES or any(l['end']!=r['start'] for l,r in zip(result,result[1:])):
        raise ValueError('fixed physical scope/contiguity differs')
    return result

def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)
def render_bundle(rom):
    fields=extract(rom);encoded=dump(fields);image=rebuild(rom,load_fields(encoded))
    if image!=rom:raise ValueError('entire-ROM export/import differs')
    rows=blocks(rom,fields)
    report=dict(format=FORMAT,confidence='confirmed_encoding_candidate_purpose',editable_bytes=EDITABLE_BYTES,
        palette_bytes=128,tile_bytes=16384,map_encoded_bytes=2970,map_decoded_words=[1024]*6,
        blocks=[{k:v for k,v in row.items() if k!='data'}|{'sha256':sha(row['data'])} for row in rows],
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),original_resource_xrefs=evidence(rom),
        original_consumers=dict(palette_copy=[0x2B2E8,0x2B2F6],tile_uploads=[0x2B214,0x2B230],
                               map_reader=[0x2B3C4,0x2B3D4,0x2B444],palette_fade=0xDEA6),
        alias_read=dict(palette_fade_D1=64,actual_WORD_reads=65,last_WORD_start=TILES[0][0],
                        reused_field=ident(TILES[0][0],'tile'),physical_emit_again=False),
        original_CPU_domains_are_not_editor_counts=True,independent_CPU_comparison=False,
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,promotion=True)
    members={'fields.json':encoded,'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},
        independent_CPU_comparison=False,promotion=True))
    return members
def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/scene_tile_resources')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
    return path
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--fields',default=str(DEFAULT_FIELDS));parser.add_argument('--output')
    args=parser.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output)
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin output required')
    elif args.output is not None:raise ValueError('verify does not write output')
    rom=f.read_bounded(args.rom,af.ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():f.put(target/name,data)
        result=dict(path=str(target),members={name:sha(data) for name,data in members.items()},editable_bytes=EDITABLE_BYTES)
    else:
        fields=load_fields(f.read_bounded(args.fields,f.MAX_JSON));image=rebuild(rom,fields)
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),bytes=len(image),sha256=sha(image),exact_canonical=image==rom,editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
