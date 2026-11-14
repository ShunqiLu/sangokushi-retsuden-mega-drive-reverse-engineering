"""Encode seventeen palette transfer descriptors and their shared color banks.

Selector 17 uses the descriptor at 0x03AC34 and the title palette at 0x03B0BC.
The command and title graphics modules own those two records.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from tools.audio_formats import audio_formats as af
from tools.vdp_word_streams import format as f
from tools.scene_tile_resources.codec import colour,colour_word
ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=af.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/battle_palette_transfers/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/battle_palette_transfers'
FORMAT='candidate-battle-palette-copy-fields-v1'
EDITABLE_BYTES=1288
DIRECTORY_START=0x3ABAC;DIRECTORY_END=0x3AC34
PALETTES=tuple((a,a+128) for a in range(0x3AC3C,0x3AFBC,128))+tuple((a,a+32) for a in range(0x3AFBC,0x3B0BC,32))
keys=f.keys;uint=f.uint;sha=f.sha;dump=f.dump;load_fields=f.load_json
def ident(start):return f'rom_{start:06X}_palette'
def metadata():return dict(format=FORMAT,source=dict(size=af.ROM_SIZE,sha256=af.ROM_SHA256),confidence='candidate',
    owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def exact_list(value,count,label):
    if type(value)is not list or len(value)!=count:raise ValueError(label+': fixed allocation differs')
    return value
def check_consumer(rom):
    if rom[0x3AB94:0x3ABAC]!=bytes.fromhex('43fa00164e71e748d2c0245936593e1926da51cffffc4e75'):
        raise ValueError('original8B selector/copy consumer differs')
def extract(rom):
    af.verify_rom(rom);check_consumer(rom);result=metadata()
    result['transfers']=[dict(id=f'rom_{p:06X}_transfer',source=ident(int.from_bytes(rom[p:p+4],'big')),
        destination_WORD=int.from_bytes(rom[p+4:p+6],'big'),LONG_count_minus_one=int.from_bytes(rom[p+6:p+8],'big'))
        for p in range(DIRECTORY_START,DIRECTORY_END,8)]
    result['palettes']=[dict(id=ident(a),start=a,end=z,colours=[colour(int.from_bytes(rom[p:p+2],'big')) for p in range(a,z,2)]) for a,z in PALETTES]
    blocks(rom,result);return result
def blocks(rom,fields):
    af.verify_rom(rom);keys(fields,set(metadata())|{'transfers','palettes'},'package')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    catalog={ident(a):(a,z) for a,z in PALETTES};raw=bytearray()
    for row,p in zip(exact_list(fields['transfers'],17,'17 editor transfer records'),range(DIRECTORY_START,DIRECTORY_END,8)):
        keys(row,{'id','source','destination_WORD','LONG_count_minus_one'},'transfer')
        f.same(row['id'],f'rom_{p:06X}_transfer','transfer id')
        if type(row['source'])is not str or row['source'] not in catalog:raise ValueError('source leaves existing palette catalog; shared code is not a new bank')
        a,z=catalog[row['source']];destination=uint(row['destination_WORD'],65535,'MOVEA.W destination');count=uint(row['LONG_count_minus_one'],65535,'DBRA WORD')
        if destination not in (0xFB00,0xFB20) or 4*(count+1)>z-a or destination+4*(count+1)>0xFB80:
            raise ValueError('transfer leaves fixed palette source/staging capacity; not a CPU clamp')
        raw.extend(a.to_bytes(4,'big'));raw.extend(destination.to_bytes(2,'big'));raw.extend(count.to_bytes(2,'big'))
    rows=[dict(id='rom_03ABAC_transfers',start=DIRECTORY_START,end=DIRECTORY_END,data=bytes(raw),role='candidate_BE32_MOVEAWORD_DBRALONG_transfers')]
    for row,(a,z) in zip(exact_list(fields['palettes'],15,'15 shared palette banks'),PALETTES):
        keys(row,{'id','start','end','colours'},'palette')
        for key,value in dict(id=ident(a),start=a,end=z).items():f.same(row[key],value,'palette.'+key)
        raw=b''.join(colour_word(v).to_bytes(2,'big') for v in exact_list(row['colours'],(z-a)//2,'palette colours'))
        rows.append(dict(id=ident(a),start=a,end=z,data=raw,role='candidate_palette_staging_CRAM_channels'))
    if sum(len(r['data']) for r in rows)!=EDITABLE_BYTES:raise ValueError('physical field scope differs')
    return rows
def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)
def render_bundle(rom):
    fields=extract(rom);data=dump(fields);image=rebuild(rom,load_fields(data));rows=blocks(rom,fields)
    if image!=rom:raise ValueError('whole-ROM roundtrip differs')
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,directory_bytes=136,palette_bytes=1152,
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        blocks=[{k:v for k,v in row.items() if k!='data'}|{'sha256':sha(row['data'])} for row in rows],
        original_consumer=dict(start=0x3AB94,end=0x3ABAC,bytes=rom[0x3AB94:0x3ABAC].hex(),selector='LSL.W3 then ADDA.W signextends lowWORD',
                              fields='BE32 source, MOVEA.W signextended destination, DBRA LONG_count_minus_one WORD'),
        foreign_code_alias=dict(record_start=0x3AC34,record_end=0x3AC3C,source=0x3B0BC,destination_WORD=0xFB00,LONG_count_minus_one=31,
            bytes=rom[0x3AC34:0x3AC3C].hex(),purpose='unknown',physical_emit=False,old_code_authority_unchanged=True),
        original_aliases={'record1_and2':ident(0x3ACBC),'record5_and8':ident(0x3AE3C)},
        physical_catalog_is_not_natural_index_clamp=True,independent_CPU_comparison=False,promotion=True)
    members={'fields.json':data,'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},independent_CPU_comparison=False,promotion=True))
    return members
def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/battle_palette_transfers')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--fields',default=str(DEFAULT_FIELDS));parser.add_argument('--output');args=parser.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output)
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
    elif args.output is not None:raise ValueError('verify does not write')
    rom=f.read_bounded(args.rom,af.ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():f.put(target/name,data)
        result=dict(path=str(target),members={name:sha(data) for name,data in members.items()},editable_bytes=EDITABLE_BYTES)
    else:
        fields=load_fields(f.read_bounded(args.fields,f.MAX_JSON));image=rebuild(rom,fields)
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),sha256=sha(image),exact_canonical=image==rom,editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
