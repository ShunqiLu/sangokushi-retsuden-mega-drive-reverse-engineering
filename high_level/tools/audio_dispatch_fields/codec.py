"""Lossless LE16 Z80 dispatch fields with original confidence and unclamped reads.

Only the proved 32-entry sequence table and two previously recognized physical
prefixes are editable. Their catalogs do not restrict the original CPU index.
Targets are RAM code addresses, not physical ROM addresses.
"""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
import csv
import io
from pathlib import Path
from tools.direct_code import direct_code as d
from tools.z80_code import z80_code as z
f=d.f
ROOT=d.ROOT
DEFAULT_FIELDS=ROOT/'analysis/audio_dispatch_fields/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/audio_dispatch_fields'
EVIDENCE=ROOT/'analysis/audio/generated/dispatch_table_entries.csv'
EVIDENCE_SHA=reference_value(__name__, 'EVIDENCE_SHA')
EDITABLE_BYTES=88
FORMAT='original-z80-dispatch-source-fields-v1'
sha=f.sha;dump=f.dump
TABLES=(('sequence_command_e0_ff',0xB8F,32,'confirmed',0xE0),
        ('external_control_command_valid_prefix',0x52D,4,'probable',0xE0),
        ('sequence_ff_subcommand_prefix',0xBCF,8,'probable',None))

def metadata():
    return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
                evidence_sha256=EVIDENCE_SHA,owner_bytes_added=0,natural_domains_added=0)

def proofs(rom):
    f.verify_rom(rom)
    evidence=d.m.read(EVIDENCE)
    if sha(evidence)!=EVIDENCE_SHA:raise ValueError('dispatch evidence changed')
    byname={name:[] for name,*_ in TABLES}
    for row in csv.DictReader(io.StringIO(evidence.decode('utf-8-sig'))):
        if row['table'] not in byname:raise ValueError('unexpected dispatch evidence table')
        byname[row['table']].append(row)
    boundaries={r['address'] for r in z.inventory(rom)}
    # RST28: C=A, B=0, ADD HL,BC twice. No byte-overflow or catalog clamp.
    if rom[z.ROM_BASE+0x28:z.ROM_BASE+0x2D]!=bytes.fromhex('4f06000909'):
        raise ValueError('original indexed pointer arithmetic changed')
    for name,start,count,confidence,_ in TABLES:
        rows=byname[name]
        if len(rows)!=count:raise ValueError('physical dispatch extent changed')
        for i,row in enumerate(rows):
            at=start+2*i
            value=int.from_bytes(rom[z.ROM_BASE+at:z.ROM_BASE+at+2],'little')
            if (int(row['index'])!=i or int(row['entry_address'])!=at or
                    int(row['target'])!=value or row['table_confidence']!=confidence or
                    row['target_valid']!='True' or value not in boundaries):
                raise ValueError('dispatch row disagrees with original bytes/boundary')
    return boundaries

def table_meta(name,start,count,confidence,command):
    return dict(id=name,logical_RAM_start=start,physical_ROM_start=z.ROM_BASE+start,
                entry_count=count,confidence=confidence,command_base=command)

def extract(rom):
    proofs(rom)
    result=metadata()
    result['tables']=[dict(**table_meta(*t),target_RAM_WORDs=[int.from_bytes(
        rom[z.ROM_BASE+t[1]+2*i:z.ROM_BASE+t[1]+2*i+2],'little') for i in range(t[2])]) for t in TABLES]
    blocks(rom,result)
    return result

def blocks(rom,fields):
    boundaries=proofs(rom)
    f.keys(fields,set(metadata())|{'tables'},'audio dispatch')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    tables=fields['tables']
    if type(tables)is not list or len(tables)!=3:raise ValueError('three physical dispatch tables required')
    out=[]
    for spec,row in zip(TABLES,tables):
        fixed=table_meta(*spec)
        f.keys(row,set(fixed)|{'target_RAM_WORDs'},'dispatch table')
        for key,value in fixed.items():f.same(row[key],value,'dispatch.'+key)
        targets=row['target_RAM_WORDs']
        if type(targets)is not list or len(targets)!=spec[2]:raise ValueError('dispatch table width changed')
        data=bytearray()
        for value in targets:
            f.uint(value,65535,'Z80 RAM target')
            if value not in boundaries:raise ValueError('editable target lacks recovered instruction boundary')
            data.extend(value.to_bytes(2,'little'))
        start=fixed['physical_ROM_start']
        out.append(dict(id=fixed['id'],start=start,end=start+len(data),data=bytes(data),
                        role='Z80_RAM_handler_pointer_LE16_'+spec[3]))
    if sum(b['end']-b['start'] for b in out)!=EDITABLE_BYTES:raise ValueError('dispatch byte count')
    return out

def rebuild(rom,fields):
    out=bytearray(rom)
    for b in blocks(rom,fields):out[b['start']:b['end']]=b['data']
    return bytes(out)

def indexed_target(rom,fields,table_id,index_BYTE):
    """Original RST28 address/read projection, including outside edited prefixes.

    No JP execution or natural runtime-domain claim. Indexes beyond the editable
    catalog deliberately read original neighboring bytes instead of being clamped.
    """
    f.uint(index_BYTE,255,'original A index')
    selected=next((t for t in TABLES if t[0]==table_id),None)
    if selected is None:raise ValueError('unknown dispatch table')
    logical=(selected[1]+2*index_BYTE)&65535
    physical=z.ROM_BASE+logical
    image=rebuild(rom,fields)
    return dict(logical_RAM_address=logical,physical_source_address=physical,
                target_RAM_WORD=int.from_bytes(image[physical:physical+2],'little'),
                in_editable_catalog=index_BYTE<selected[2],JP_execution_proven=False)

def load_fields(data):return f.load_json(data)

def render_bundle(rom,fields):
    rows=blocks(rom,fields);rebuilt=rebuild(rom,fields)
    manifest=dict(editable_bytes=EDITABLE_BYTES,tables=3,confirmed_pointer_bytes=64,
        probable_prefix_bytes=24,fields_sha256=sha(dump(fields)),rebuilt_sha256=sha(rebuilt),
        natural_domains_added=0,owner_bytes_added=0,independent_CPU_comparison=False)
    return {'fields.json':dump(fields),'manifest.json':dump(manifest),
            'validation.json':dump(dict(roundtrip_exact=rebuilt==rom,blocks=len(rows)))}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(f.DEFAULT_ROM))
    parser.add_argument('--fields',default=str(DEFAULT_FIELDS))
    parser.add_argument('--output-root')
    args=parser.parse_args(argv);rom=d.m.read(args.rom,f.ROM_SIZE)
    fields=extract(rom) if args.command=='export' else load_fields(d.m.read(args.fields))
    bundle=render_bundle(rom,fields)
    if args.command=='verify':print(bundle['manifest.json'].decode());return 0
    if not args.output_root:raise ValueError('fresh dedicated output required')
    target=d.m.af.safe_path(args.output_root)
    if target==OUTPUT_ROOT or not target.is_relative_to(OUTPUT_ROOT) or target.exists():raise ValueError('fresh build/audio_dispatch_fields output required')
    target.mkdir(parents=True)
    if args.command=='import':bundle['rebuilt.bin']=rebuild(rom,fields)
    for name,data in bundle.items():
        with (target/name).open('xb') as stream:stream.write(data)
    print(sha(bundle['fields.json']));return 0

if __name__=='__main__':raise SystemExit(main())
