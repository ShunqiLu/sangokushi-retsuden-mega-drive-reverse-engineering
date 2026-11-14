"""23 physical big-endian WORD-RLE maps and two five-pointer directories.

03AAC2/03AACE reset D6 to32; 03AAD6 retains the caller's D6. Some original
calls therefore stop after10/18 rows, sometimes within a repeat. The physical
streams independently end at marker/zero and encode1024 WORDs. This editor's
fixed allocation is not a CPU clamp or a proof of natural selector domains.
The final BYTE0473E3 and every older graphics authority remain excluded.
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.vdp_word_streams import format as f
from tools.graphics_build import rle_fields as rf
DEFAULT_ROM=f.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/battle_overlay_maps/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/battle_overlay_maps'
FORMAT='candidate-battle-overlay-map-WORD-rle-v1'
EDITABLE_BYTES=10655
STARTS=(0x44A6C,0x44C6F,0x44DC6,0x44EF5,0x45098,0x45127,0x45246,
        0x4529B,0x4539C,0x45413,0x456EC,0x4583F,0x45920,0x45AE1,
        0x45D70,0x46067,0x4632A,0x465C5,0x467F4,0x4696B,0x46E10,0x46FCD,0x47248)
LAYOUT=tuple(zip(STARTS,STARTS[1:]+(0x473E3,)))
DIRECTORIES=(('directory_E000',0x3DC90),('directory_F000',0x3DCA4))
# Source LEA, map start, destination VRAM, caller-loaded D6, reader entry.
DIRECT_CALLS=((0x3B914,0x4632A,0xE000,18,0x3AACE),(0x3B9E4,0x465C5,0xE000,18,0x3AACE),
 (0x3C418,0x46FCD,0xE000,18,0x3AACE),(0x3C4DA,0x47248,0xE000,18,0x3AACE),
 (0x3CBF4,0x45AE1,0xE000,18,0x3AAC2),(0x3CCC0,0x45D70,0xE000,18,0x3AACE),
 (0x3D2B2,0x4696B,0xE000,18,0x3AACE),(0x3DC1C,0x45413,0xC000,None,0x3AAC2),
 (0x3DC32,0x456EC,0xC040,None,0x3AAC2),(0x3DD98,0x4539C,0xC000,18,0x3AAD6),
 (0x3DE28,0x4539C,0xC000,18,0x3AAD6),(0x3DEAA,0x4539C,0xC000,18,0x3AAD6),
 (0x3E138,0x4539C,0xC000,18,0x3AAD6),(0x3E492,0x4583F,0xC000,18,0x3AAD6),
 (0x3EA66,0x44C6F,0xC000,18,0x3AAD6),(0x3EAE2,0x44EF5,0xC980,10,0x3AAD6),
 (0x3EB02,0x45098,0xC9C0,10,0x3AAD6),(0x3EB72,0x44DC6,0xC000,18,0x3AAD6),
 (0x3EDAE,0x4529B,0xC000,32,0x3AAD6),(0x3EDD6,0x45127,0xC000,32,0x3AAD6),
 (0x3EDF6,0x45246,0xC040,32,0x3AAD6),(0x3EECE,0x44A6C,0xC000,32,0x3AAD6))
sha=f.sha;dump=f.dump;uint=f.uint;keys=f.keys

def ident(start):return f'rom_{start:06X}_map'
BY_ID={ident(start):(start,end) for start,end in LAYOUT}
def metadata():return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
    confidence='candidate',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def exact_list(value,count,label):
    if type(value) is not list or len(value)!=count:raise ValueError(label+': physical count differs')
    return value
def fixed_map(start,end):return dict(id=ident(start),start=start,end=end,byte_order='big',physical_WORDs=1024)

def extract(rom):
    f.verify_rom(rom);fields=metadata()
    fields['directories']=[dict(id=name,start=start,targets=[ident(int.from_bytes(rom[p:p+4],'big'))
        for p in range(start,start+20,4)]) for name,start in DIRECTORIES]
    fields['maps']=[dict(**fixed_map(start,end),fields=rf.parse_word(rom[start:end],'big',1024)) for start,end in LAYOUT]
    blocks(rom,fields);return fields

def blocks(rom,fields):
    f.verify_rom(rom);keys(fields,set(metadata())|{'directories','maps'},'package')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    result=[]
    for row,(name,start) in zip(exact_list(fields['directories'],2,'directories'),DIRECTORIES):
        keys(row,{'id','start','targets'},'directory');f.same(row['id'],name,'directory id');f.same(row['start'],start,'directory start')
        targets=exact_list(row['targets'],5,'physical directory slots')
        if any(type(target) is not str or target not in BY_ID for target in targets):raise ValueError('target outside physical map catalog')
        data=b''.join(BY_ID[target][0].to_bytes(4,'big') for target in targets)
        result.append(dict(id=name,start=start,end=start+20,data=data,role='candidate_map_pointer_directory'))
    for row,(start,end) in zip(exact_list(fields['maps'],23,'maps'),LAYOUT):
        fixed=fixed_map(start,end);keys(row,set(fixed)|{'fields'},'map')
        for key,value in fixed.items():f.same(row[key],value,'map.'+key)
        raw,decoded=rf.pack_word(row['fields'],'big',1024)
        if len(raw)!=end-start:raise ValueError('fixed physical encoded cost differs; no blob fallback')
        if rf.parse_word(raw,'big',1024)!=row['fields']:raise ValueError('source field roundtrip differs')
        result.append(dict(id=row['id'],start=start,end=end,data=raw,role='candidate_big_WORD_rle_map'))
    result.sort(key=lambda row:row['start'])
    if sum(len(row['data']) for row in result)!=EDITABLE_BYTES or any(a['end']>b['start'] for a,b in zip(result,result[1:])):
        raise ValueError('nonoverlapping physical scope differs')
    return result
def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)
def decode(rom,fields,map_id):
    blocks(rom,fields)
    if type(map_id) is not str or map_id not in BY_ID:raise ValueError('unknown physical map')
    row=fields['maps'][STARTS.index(BY_ID[map_id][0])]
    return rf.pack_word(row['fields'],'big',1024)[1]
def replace_decoded(rom,fields,map_id,decoded):
    old=decode(rom,fields,map_id)
    if type(decoded) is not bytes or len(decoded)!=2048:raise ValueError('editor requires1024 WORDs')
    result=copy.deepcopy(fields)
    if decoded==old:return result
    i=STARTS.index(BY_ID[map_id][0]);row=result['maps'][i];start,end=BY_ID[map_id]
    row['fields']=rf.encode_word_exact(decoded,'big',row['fields']['marker'],end-start)
    blocks(rom,result);return result

def project_map(data,rows,or_mask=0,output_budget=65536):
    """Guarded source-read/WORD-write projection, NOT a full CPU reference.

    Mirrors03AB32's32-WORD row exit, including a partial final repeat. It does
    not model RAM aliases, return frames, IRQs, timing or the VDP device. The
    external budget is a failure guard, not an original termination condition.
    """
    if type(data) is not bytes or not data:raise ValueError('nonempty byte source required')
    uint(rows,65535,'D6 row count');uint(or_mask,65535,'output OR WORD');uint(output_budget,65536,'external budget')
    if not rows or not output_budget:raise ValueError('zero count/budget unsupported by this bounded projection')
    cursor=1;marker=data[0];output=bytearray();commands=0
    def take():
        nonlocal cursor
        if cursor>=len(data):raise ValueError('source read outside supplied bytes')
        v=data[cursor];cursor+=1;return v
    def finish(stop,remaining=0):return dict(stop=stop,consumed=cursor,output=bytes(output),
        remaining_repeat_WORDs=remaining,commands_read=commands)
    while True:
        first=take()
        if first==marker:
            count=take()
            if not count:return finish('marker_zero')
            count+=1;first=take();second=take()
        else:count=1;second=take()
        word=(first<<8|second)|or_mask;commands+=1
        for i in range(count):
            if len(output)//2>=output_budget:return finish('external_budget',count-i)
            output.extend(word.to_bytes(2,'big'))
            if len(output)//2==rows*32:return finish('row_limit',count-i-1)

def call_profile(source,start,vram,loaded,entry):
    rows=32 if entry in (0x3AAC2,0x3AACE) else loaded
    return dict(source_LEA=source,map_id=ident(start),entry=entry,loaded_D6=loaded,effective_D6=rows,
        vram_target=vram,row_stride=128,output_OR=0 if entry==0x3AACE else 0x8000)
def load_fields(data):return f.load_json(data)
def schema():
    def obj(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def fixed(value):
        if type(value) is dict:return obj({key:fixed(item) for key,item in value.items()})
        return dict(type={str:'string',int:'integer'}[type(value)],const=value)
    def number(high):return dict(type='integer',minimum=0,maximum=high)
    def array(n,item):return dict(type='array',minItems=n,maxItems=n,items=item)
    literal=obj(dict(op=dict(const='literal'),word=number(65535)))
    repeat=obj(dict(op=dict(const='repeat'),count=dict(type='integer',minimum=2,maximum=256),word=number(65535)))
    word_stream=obj(dict(marker=number(255),commands=dict(type='array',maxItems=1024,items=dict(oneOf=[literal,repeat]))))
    properties={key:fixed(value) for key,value in metadata().items()}
    properties['directories']=array(2,obj(dict(id=dict(type='string'),start=number(f.ROM_SIZE),
        targets=array(5,dict(type='string',enum=list(BY_ID))))))
    properties['maps']=array(23,obj(dict(id=dict(type='string'),start=number(f.ROM_SIZE),end=number(f.ROM_SIZE),
        byte_order=dict(const='big'),physical_WORDs=dict(const=1024),fields=word_stream)))
    result=obj(properties);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='Runtime additionally checks fixed addresses, encoded costs and exact1024 physical WORDs. Not a CPU domain.'
    return result
def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('whole-ROM physical grammar differs')
    calls=[]
    for args in DIRECT_CALLS:
        profile=call_profile(*args);start,end=BY_ID[profile['map_id']]
        run=project_map(rom[start:end],profile['effective_D6'],profile['output_OR'])
        calls.append(dict(**profile,source_read_end=start+run['consumed'],source_read_bytes=run['consumed'],
            unread_physical_bytes=end-start-run['consumed'],stop=run['stop'],WORD_writes=len(run['output'])//2,
            output_WORDs_sha256=sha(run['output']),remaining_repeat_WORDs=run['remaining_repeat_WORDs']))
    directory_calls=[]
    for i,(name,start) in enumerate(DIRECTORIES):
        for slot,target in enumerate(fields['directories'][i]['targets']):
            a,b=BY_ID[target];run=project_map(rom[a:b],32)
            directory_calls.append(dict(directory=name,slot=slot,map_id=target,source_read_end=a+run['consumed'],
                source_read_bytes=run['consumed'],stop=run['stop'],WORD_writes=len(run['output'])//2,
                remaining_repeat_WORDs=run['remaining_repeat_WORDs']))
    report=dict(confidence='confirmed_physical_encoding_candidate_visual_role',editable_bytes=EDITABLE_BYTES,
        physical_maps=23,physical_map_bytes=10615,directory_bytes=40,physical_blocks=25,
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),physical_WORDs_per_map=1024,
        fixed_extent_is_editor_contract=True,original_entries=[0x3AAC2,0x3AACE,0x3AAD6],
        original_WORD_reader=0x3AAF2,original_repeat_reader=0x3AB12,original_row_return=0x3AB32,
        direct_calls=calls,directory_calls=directory_calls,directory_consumers=[0x3DBF8,0x3DC18],
        directory_pointer_reads=[0x3DBE8,0x3DC08],selector_source_WORD=0xFF80DA,
        selector_semantics='WORD<<2 wraps16, sign-extended indexed offset; five editor slots are not a CPU clamp',
        unknown_intervals=[[0x473E3,0x473E4]],
        sole_authority_exclusions=['battle_graphics maps ending044A6C and tiles starting0473E4',
            'battle_variant_tiles directories ending03DC90'],
        reused_implementation=['graphics_build.rle_fields.parse_word','pack_word','encode_word_exact'],
        CPU_reference_from_zero=False,independent_CPU_comparison=False,natural_selector_domain_complete=False,
        output_OR_not_baked_into_source=True,port_timing_proven=False,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(format=FORMAT,confidence='candidate',editable_bytes=EDITABLE_BYTES,
        canonical_source=metadata()['canonical_source'],members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0))
    return members
def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/battle_overlay_maps')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify','decode','replace-decoded'))
    p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output')
    p.add_argument('--map-id');p.add_argument('--decoded');args=p.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output) # output authority BEFORE input reads
        if args.command in ('import','decode') and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
        if args.command=='replace-decoded' and target.suffix.lower()!='.json':raise ValueError('fresh fields .json required')
    elif args.output is not None:raise ValueError('verify writes no output')
    rom=f.read_bounded(args.rom,f.ROM_SIZE)
    if args.command=='export':
        bundle=render_bundle(rom);target.mkdir()
        for name,data in bundle.items():f.put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES)
    else:
        fields=load_fields(f.read_bounded(args.fields,f.MAX_JSON))
        if args.command=='decode':data=decode(rom,fields,args.map_id)
        elif args.command=='replace-decoded':
            if args.decoded is None:raise ValueError('--decoded required')
            data=dump(replace_decoded(rom,fields,args.map_id,f.read_bounded(args.decoded,2048)))
        else:data=rebuild(rom,fields)
        if target is not None:f.put(target,data)
        result=dict(path=None if target is None else str(target),sha256=sha(data),
            exact_canonical=data==rom,editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
