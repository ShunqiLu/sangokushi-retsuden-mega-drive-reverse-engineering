"""Lossless editable4bpp pixels for original direct VDP uploads.

The128B catalog contains15 fixed physical groups, not a CPU selector clamp.
Zero pixels actually read by the55-tile upload are pixels, not padding claims.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from tools.audio_formats import audio_formats as af
from tools.vdp_word_streams import format as f
ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=af.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/display_tile_resources/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/display_tile_resources'
FORMAT='candidate-fixed-display-vdp-tiles-v1'
SPANS=((0x9556,0x9C36,55),(0x94728,0x94EA8,60))
EDITABLE_BYTES=3680
keys=f.keys;uint=f.uint;sha=f.sha;dump=f.dump;load_fields=f.load_json
def ident(start):return f'rom_{start:06X}_tile'
def metadata():return dict(format=FORMAT,source=dict(size=af.ROM_SIZE,sha256=af.ROM_SHA256),confidence='candidate',
    owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def exact_list(value,count,label):
    if type(value)is not list or len(value)!=count:raise ValueError(label+': fixed allocation differs')
    return value
def check_consumers(rom):
    if rom[0x9412:0x9424]!=bytes.fromhex('41fa0142303c01b723d800c0000051c8fff8'):raise ValueError('original440 LONG VDP upload differs')
    if rom[0xC93C:0xC95E]!=bytes.fromhex('301b6b1eef4841f900094728d0c0303c001f23d800c0000051c8fff8524151cfffe0'):
        raise ValueError('original signed-WORD128B catalog upload differs')
def extract(rom):
    af.verify_rom(rom);check_consumers(rom);fields=metadata();fields['banks']=[]
    for a,z,n in SPANS:
        tiles=[dict(id=ident(p),pixels=[[x for b in rom[p+4*y:p+4*y+4] for x in (b>>4,b&15)] for y in range(8)]) for p in range(a,z,32)]
        fields['banks'].append(dict(id=ident(a),start=a,end=z,tiles=tiles))
    blocks(rom,fields);return fields
def blocks(rom,fields):
    af.verify_rom(rom);keys(fields,set(metadata())|{'banks'},'package')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    rows=[]
    for bank,(a,z,n) in zip(exact_list(fields['banks'],2,'two banks'),SPANS):
        keys(bank,{'id','start','end','tiles'},'bank')
        for key,value in dict(id=ident(a),start=a,end=z).items():f.same(bank[key],value,'bank.'+key)
        raw=bytearray()
        for tile,p in zip(exact_list(bank['tiles'],n,'tile allocations'),range(a,z,32)):
            keys(tile,{'id','pixels'},'tile');f.same(tile['id'],ident(p),'tile id')
            for row in exact_list(tile['pixels'],8,'eight pixel rows'):
                values=[uint(v,15,'4bpp pixel') for v in exact_list(row,8,'eight pixels')]
                raw.extend((values[i]<<4)|values[i+1] for i in range(0,8,2))
        if len(raw)!=z-a:raise ValueError('fixed physical tile size differs')
        rows.append(dict(id=ident(a),start=a,end=z,data=bytes(raw),role='candidate_direct_uploaded_4bpp_tiles'))
    return rows
def rebuild(rom,fields):
    result=bytearray(rom)
    for row in blocks(rom,fields):result[row['start']:row['end']]=row['data']
    return bytes(result)
def render_bundle(rom):
    fields=extract(rom);data=dump(fields);image=rebuild(rom,load_fields(data));rows=blocks(rom,fields)
    if image!=rom:raise ValueError('whole-ROM roundtrip differs')
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        blocks=[{k:v for k,v in row.items() if k!='data'}|{'sha256':sha(row['data'])} for row in rows],
        original_consumers=[dict(start=0x9412,end=0x9424,bytes=rom[0x9412:0x9424].hex(),LONG_reads=440,source_bytes=1760),
                            dict(start=0xC93C,end=0xC95E,bytes=rom[0xC93C:0xC95E].hex(),LONG_reads_per_catalog_group=32,group_bytes=128)],
        second_physical_catalog_groups=15,selector_expression='LSL.W7 then ADDA.W signextends lowWORD; original negative selector exits first',
        physical_catalog_is_not_natural_index_clamp=True,zero_pixels_are_consumed_upload_data_not_padding=True,
        independent_CPU_comparison=False,promotion=True)
    members={'fields.json':data,'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},independent_CPU_comparison=False,promotion=True))
    return members
def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/display_tile_resources')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--fields',default=str(DEFAULT_FIELDS));parser.add_argument('--output');args=parser.parse_args(argv)
    target=None
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
