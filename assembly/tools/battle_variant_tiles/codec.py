"""Twelve original tile streams and three aliased pointer catalogs.

Source grammar is confirmed by 03DB84..03DBD8 -> 03AB52. The fixed five-slot
catalogs and 4096 decoded WORDs are editor allocations, not CPU index clamps or
hardware limits. Natural selector domains and detailed visual purposes remain
unknown. Eleven intervening bytes, the last byte and earlier gaps stay opaque.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.vdp_word_streams import format as f
from tools.graphics_build import rle_fields as rle
from tools.battle_graphics import battle_graphics as battle

DEFAULT_ROM=f.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/battle_variant_tiles/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/battle_variant_tiles'
FORMAT='candidate-aliased-battle-variant-little-word-tiles-v1'
STARTS=(0x4FBE4,0x51BBC,0x53422,0x54160,0x546E0,0x55FA6,0x5757A,0x58A60,
        0x59E04,0x5A2B4,0x5B99C,0x5CA96)
ENDS=tuple(start-1 for start in STARTS[1:])+(0x5CDE1,)
DIRECTORIES=(('vram_0000',0x3DC54,(0x546E0,0x5757A,0x51BBC,0x5A2B4,0x5757A)),
             ('vram_2000',0x3DC68,(0x55FA6,0x58A60,0x53422,0x5B99C,0x58A60)),
             ('vram_4000',0x3DC7C,(0x51BBC,0x59E04,0x54160,0x5CA96,0x59E04)))
EDITABLE_BYTES=53806
UNKNOWN_GAPS=((0x4FBE3,0x4FBE4),)+tuple((end,start) for end,start in zip(ENDS[:-1],STARTS[1:]))+((0x5CDE1,0x5CDE2),)
keys=f.keys;uint=f.uint;sha=f.sha;dump=f.dump

def ident(start):return f'rom_{start:06X}_varianttiles'
def metadata():return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
    confidence='candidate',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def stream_metadata(start,end):return dict(id=ident(start),start=start,end=end,byte_order='little',decoded_words=4096)
def exact_list(value,count,label):
    if type(value) is not list or len(value)!=count:raise ValueError(label+': fixed physical count differs')
    return value

def extract(rom):
    f.verify_rom(rom);result=metadata();result['directories']=[]
    for name,start,targets in DIRECTORIES:
        if [int.from_bytes(rom[p:p+4],'big') for p in range(start,start+20,4)]!=list(targets):
            raise ValueError('original BE32 catalog identity differs')
        result['directories'].append(dict(id=name,start=start,targets=[ident(target) for target in targets]))
    result['streams']=[]
    for start,end in zip(STARTS,ENDS):
        result['streams'].append({**stream_metadata(start,end),'fields':rle.parse_word(rom[start:end],'little',4096)})
    blocks(rom,result)
    return result

def blocks(rom,fields):
    f.verify_rom(rom);keys(fields,set(metadata())|{'directories','streams'},'package')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    catalog={ident(start):start for start in STARTS};result=[]
    for row,(name,start,_) in zip(exact_list(fields['directories'],3,'directories'),DIRECTORIES):
        keys(row,{'id','start','targets'},'directory');f.same(row['id'],name,'directory id');f.same(row['start'],start,'directory start')
        targets=exact_list(row['targets'],5,'targets')
        if any(type(target) is not str or target not in catalog for target in targets):raise ValueError('pointer outside existing physical tile catalog')
        result.append(dict(id=name,start=start,end=start+20,
                           data=b''.join(catalog[target].to_bytes(4,'big') for target in targets),role='candidate_variant_tile_directory'))
    for row,(start,end) in zip(exact_list(fields['streams'],12,'streams'),zip(STARTS,ENDS)):
        fixed=stream_metadata(start,end);keys(row,set(fixed)|{'fields'},'stream')
        for key,value in fixed.items():f.same(row[key],value,'stream.'+key)
        f.strict_commands(row['fields']);encoded,decoded=rle.pack_word(row['fields'],'little',4096)
        if len(encoded)!=end-start:raise ValueError('fixed encoded tile slot cost differs')
        if rle.parse_word(encoded,'little',4096)!=row['fields']:raise ValueError('original command representation/termination differs')
        result.append(dict(id=ident(start),start=start,end=end,data=encoded,role='candidate_little_word_variant_tiles'))
    result.sort(key=lambda row:row['start'])
    if any(a['end']>b['start'] for a,b in zip(result,result[1:])) or sum(row['end']-row['start'] for row in result)!=EDITABLE_BYTES:
        raise ValueError('physical emit overlap/scope differs')
    return result

def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)

def resolve_original_catalog(rom,directory,index_word):
    """Original full WORD*4, signed indexed addressing; no five-slot CPU clamp."""
    f.verify_rom(rom);uint(index_word,65535,'index WORD')
    names={name:start for name,start,_ in DIRECTORIES}
    if type(directory) is not str or directory not in names:raise ValueError('original directory required')
    offset=(index_word<<2)&65535;offset=offset if offset<32768 else offset-65536
    address=names[directory]+offset
    if address<0 or address+4>len(rom):raise ValueError('pointer read outside supplied ROM')
    return dict(address=address,target=int.from_bytes(rom[address:address+4],'big'),in_editor_catalog=index_word<5)

def load_fields(data):return f.load_json(data)
def schema():
    def obj(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def fixed(value):
        if type(value) is dict:return obj({key:fixed(item) for key,item in value.items()})
        return dict(type={str:'string',int:'integer'}[type(value)],const=value)
    def uint_schema(maximum):return dict(type='integer',minimum=0,maximum=maximum)
    literal=obj(dict(op=fixed('literal'),word=uint_schema(65535)))
    repeat=obj(dict(op=fixed('repeat'),word=uint_schema(65535),count=dict(type='integer',minimum=2,maximum=256)))
    stream=obj(dict(marker=uint_schema(255),commands=dict(type='array',maxItems=4096,items=dict(oneOf=[literal,repeat]))))
    properties={key:fixed(value) for key,value in metadata().items()};directories=[];streams=[]
    for name,start,_ in DIRECTORIES:
        directories.append(obj(dict(id=fixed(name),start=fixed(start),targets=dict(type='array',minItems=5,maxItems=5,
            items=dict(type='string',enum=[ident(p) for p in STARTS])))))
    for start,end in zip(STARTS,ENDS):streams.append(obj({**{key:fixed(value) for key,value in stream_metadata(start,end).items()},'fields':stream}))
    properties['directories']=dict(type='array',minItems=3,maxItems=3,prefixItems=directories,items=False)
    properties['streams']=dict(type='array',minItems=12,maxItems=12,prefixItems=streams,items=False)
    result=obj(properties);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='Runtime validator additionally enforces source costs and editing decoded extent. This is not a CPU selector/hardware clamp.'
    return result

def render_bundle(rom):
    fields=extract(rom);encoded=dump(fields);image=rebuild(rom,load_fields(encoded))
    if image!=rom:raise ValueError('whole-ROM field roundtrip differs')
    streams=[]
    for row in fields['streams']:
        consumed=battle.consume(rom[row['start']:row['end']],'little')
        if consumed['stop']!='marker_zero' or consumed['consumed']!=row['end']-row['start'] or len(consumed['output'])!=8192:
            raise ValueError('existing original consumer projection differs')
        streams.append({key:row[key] for key in ('id','start','end')}|dict(encoded_bytes=consumed['consumed'],
            decoded_bytes=len(consumed['output']),decoded_sha256=sha(consumed['output']),source_sha256=sha(rom[row['start']:row['end']]),
            aliases=[dict(directory=name,index=i) for name,_,targets in DIRECTORIES for i,target in enumerate(targets) if target==row['start']]))
    report=dict(confidence='confirmed_encoding_candidate_purpose',editable_bytes=EDITABLE_BYTES,encoded_stream_bytes=53746,
                directories_bytes=60,physical_streams=12,physical_blocks=15,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
                streams=streams,unknown_gaps=[list(pair) for pair in UNKNOWN_GAPS],
                original_consumers=dict(directory_calls=[0x3DB8C,0x3DBA4,0x3DBBC],direct_call=0x3DBD8,word_RLE=0x3AB52),
                reused_old_authority=dict(start=0x4E090,end=0x4FBE3,call=0x3DBCA,owner='battle_graphics',new_emit_bytes=0),
                decoded_sizes_are_editor_contract_not_hardware_limits=True,natural_selector_domain_complete=False,
                reused_implementation=['graphics_build.rle_fields','battle_graphics.consume'],
                independent_CPU_comparison=False,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
    members={'fields.json':encoded,'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(format=FORMAT,confidence='candidate',editable_bytes=EDITABLE_BYTES,
        canonical_source=metadata()['canonical_source'],members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0))
    return members

def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/battle_variant_tiles')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'));parser.add_argument('--rom',default=str(DEFAULT_ROM))
    parser.add_argument('--fields',default=str(DEFAULT_FIELDS));parser.add_argument('--output');args=parser.parse_args(argv)
    target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output) # output authority BEFORE any input resolution/read
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin output required')
    elif args.output is not None:raise ValueError('verify writes no output')
    rom=f.read_bounded(args.rom,f.ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():f.put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES)
    else:
        fields=load_fields(f.read_bounded(args.fields,f.MAX_JSON));image=rebuild(rom,fields)
        if args.command=='import':f.put(target,image)
        result=dict(path=None if target is None else str(target),bytes=len(image),sha256=sha(image),editable_bytes=EDITABLE_BYTES,exact_canonical=image==rom)
    print(json.dumps(result,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
