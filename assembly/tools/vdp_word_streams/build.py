"""Add fixed VDP WORD fields to the existing compiled/typed ROM layout.

The legacy layout remains reproducible. This additive build consumes only
previously opaque slices, never code, terrain or another typed authority.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.vdp_word_streams import format as f
from tools.m68k_build import m68k_build as m

DEFAULT_FIELDS=ROOT/'analysis/vdp_word_streams/generated/fields.json'

def blocks(rom,fields):
    f.verify_rom(rom)
    return [dict(id=f.ident(row['start']),start=row['start'],end=row['end'],
                 data=row['encoded'],role='candidate_vdp_word_packets')
            for row in f.validate_fields(fields,rom[f.REUSE_START:f.REUSE_END])
            if row['physical_emit']]

def add_to_layout(rom,fields,base,dictionary_fields=None):
    rows=blocks(rom,fields)
    dictionary_bytes=0
    if dictionary_fields is not None:
        from tools.dictionary_streams import codec as dictionary
        extra=dictionary.blocks(rom,dictionary_fields)
        if sum(row['end']-row['start'] for row in extra)!=21168:raise ValueError('dictionary field scope changed')
        rows=sorted(rows+extra,key=lambda row:row['start']);dictionary_bytes=21168
    if any(a['end']>c['start'] for a,c in zip(rows,rows[1:])):raise ValueError('new resource sources overlap')
    expected={p for row in rows for p in range(row['start'],row['end'])}
    if len(expected)!=104621+dictionary_bytes:raise ValueError('resource source scope changed')
    names={f'm68k_bank{bank:02x}.s' for bank in range(16)}|{'m68k_layout.s','manifest.json'}
    if type(base) is not dict or set(base)!=names or any(type(v) is not bytes for v in base.values()):
        raise ValueError('complete legacy byte layout required')
    result=dict(base);consumed=[]
    pattern=r'\s*\.incbin "segments/bank([0-9a-f]{2})\.bin", 0x([0-9A-F]+), 0x([0-9A-F]+)'
    for bank in range(16):
        name=f'm68k_bank{bank:02x}.s';lines=[]
        for line in base[name].decode('utf-8').splitlines():
            match=re.fullmatch(pattern,line)
            if match:
                if int(match[1],16)!=bank:raise ValueError('legacy raw bank mismatch')
                lines.extend(m.typed_gap(bank,int(match[2],16),int(match[3],16),[],[],rows,consumed))
            else:lines.append(line)
        result[name]=('\n'.join(lines)+'\n').encode()
    if len(consumed)!=len(expected) or set(consumed)!=expected:
        raise ValueError('VDP source overlaps another authority or is omitted/duplicated')
    info=json.loads(base['manifest.json'])
    info.update(typed_vdp_word_stream_bytes=104621,vdp_word_fields_sha256=f.sha(f.dump(fields)),
                vdp_word_confidence='candidate',vdp_word_reused_terrain_bytes=2,
                vdp_word_empty_prefix_retained_bytes=1,vdp_word_unknown_leading_byte=0xD4D41,
                vdp_word_owner_bytes_added=0,vdp_word_natural_domains_added=0,
                legacy_compiled_or_typed_bytes=info['compiled_or_typed_bytes'],
                compiled_or_typed_bytes=info['compiled_or_typed_bytes']+104621+dictionary_bytes,
                remaining_raw_slice_bytes=info['remaining_raw_slice_bytes']-104621-dictionary_bytes,
                typed_dictionary_stream_tail_bytes=dictionary_bytes)
    if dictionary_fields is not None:info['dictionary_fields_sha256']=f.sha(dictionary.dump(dictionary_fields))
    result['manifest.json']=m.dump(info)
    return result

def render_layout(rom,fields,dictionary_fields=None):
    return add_to_layout(rom,fields,m.render_layout(rom,m.read(m.SOURCE),
                         m.af.load_assets(m.read(m.audio.DEFAULT_ASSETS))),dictionary_fields)

def expected_image(rom,fields,legacy_image,dictionary_fields=None):
    if type(legacy_image) is not bytes or len(legacy_image)!=f.ROM_SIZE:
        raise ValueError('complete legacy image bytes required')
    image=bytearray(legacy_image)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    if dictionary_fields is not None:
        from tools.dictionary_streams import codec as dictionary
        for row in dictionary.blocks(rom,dictionary_fields):image[row['start']:row['end']]=row['data']
    if image[f.REUSE_START:f.REUSE_END]!=f.REUSE_BYTES or image[f.EMPTY_START]!=0:
        raise ValueError('legacy image conflicts with terrain/empty prefix')
    return bytes(image)

def read_fields(path):return f.load_json(f.read_bounded(path,f.MAX_JSON))

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('prepare','verify-image'))
    parser.add_argument('--rom',default=str(f.DEFAULT_ROM))
    parser.add_argument('--fields',default=str(DEFAULT_FIELDS))
    parser.add_argument('--dictionary-fields')
    parser.add_argument('--output-root');parser.add_argument('--image');parser.add_argument('--legacy-image')
    args=parser.parse_args(argv)
    if args.command=='prepare':
        if args.output_root is None or args.image or args.legacy_image:raise ValueError('prepare requires output-root only')
        target=f.safe_path(args.output_root)
        if target==f.OUTPUT_ROOT or f.OUTPUT_ROOT not in target.parents:raise ValueError('layout output must stay in build/vdp_word_streams')
        rom=f.read_bounded(args.rom,f.ROM_SIZE);fields=read_fields(args.fields)
        dictionaries=None if args.dictionary_fields is None else read_fields(args.dictionary_fields)
        bundle=render_layout(rom,fields,dictionaries)
        print(m.publish_content_addressed(bundle,target,[args.rom,args.fields,m.SOURCE]))
    else:
        if not args.image or not args.legacy_image or args.output_root:raise ValueError('verify-image requires actual and legacy image')
        rom=f.read_bounded(args.rom,f.ROM_SIZE);fields=read_fields(args.fields)
        dictionaries=None if args.dictionary_fields is None else read_fields(args.dictionary_fields)
        expected=expected_image(rom,fields,f.read_bounded(args.legacy_image,f.ROM_SIZE),dictionaries)
        actual=f.read_bounded(args.image,f.ROM_SIZE)
        if actual!=expected:raise ValueError('actual GNU image differs from typed fields/legacy image')
        print(json.dumps(dict(exact=True,sha256=f.sha(actual),new_typed_bytes=104621+(21168 if dictionaries is not None else 0),
                              owner_bytes_added=0,natural_domains_added=0)))
    return 0

if __name__=='__main__':raise SystemExit(main())
