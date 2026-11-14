"""Original BE16 literal/repeat/increment columns and indexed chunk directory.

00A0D2/A112/A2EE -> 00AF6A uses directory 08155A; 00B0DE reads each
container's BE32 data base and indexed BE16 column boundary. 00B106/B1DA use
low11 command bits, preserving all sixteen output WORD bits. The fixed 24x40
allocation and 29 physical directory slots are editor contracts, not CPU index
clamps. First-command low11=06FF has inconsistent first/continuing handling and
is deliberately rejected by the editor. Natural selector domains remain unknown.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.vdp_word_streams import format as f

DEFAULT_ROM=f.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/world_tile_chunks/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/world_tile_chunks'
START,DIR,END=0x789D6,0x8155A,0x8159C
EDITABLE_BYTES=END-START
FORMAT='candidate-world-column-tile-chunks-v1'
sha=f.sha;dump=f.dump;uint=f.uint;keys=f.keys

def exact_list(value,count,label):
    if type(value) is not list or len(value)!=count:raise ValueError(label+': physical count differs')
    return value
def ident(start):return f'rom_{start:06X}_tilechunk'
def metadata():return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
    confidence='candidate',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)

def layout(rom):
    f.verify_rom(rom)
    if rom[DIR:DIR+8]!=bytes.fromhex('00041828000789d6'):raise ValueError('original directory header identity differs')
    targets=[START+int.from_bytes(rom[p:p+2],'big') for p in range(DIR+8,DIR+56,2)]
    starts=sorted(set(targets))
    if len(starts)!=24 or starts[0]!=START or rom[DIR+56:END]!=b'\xff'*10:raise ValueError('original directory partition differs')
    rows=[]
    for start,end in zip(starts,starts[1:]+[DIR]):
        base=int.from_bytes(rom[start:start+4],'big')
        offsets=[int.from_bytes(rom[start+4+2*i:start+6+2*i],'big') for i in range(25)]
        if base!=start+54 or offsets[0]!=0 or base+offsets[-1]!=end or any(a>=b for a,b in zip(offsets,offsets[1:])):
            raise ValueError('original 24-column physical partition differs')
        rows.append(dict(start=start,end=end,base=base,offsets=offsets))
    return targets,rows

def parse_column(data):
    if type(data) is not bytes or len(data)%2:raise ValueError('even immutable column source required')
    commands=[];p=0;decoded=0
    while p<len(data):
        word=int.from_bytes(data[p:p+2],'big');p+=2;code=word&0x7FF
        if code==0x6FF:raise ValueError('ambiguous original first/continuing low11=06FF')
        if code<0x700:row=dict(op='literal',word=word);decoded+=1
        else:
            if p+2>len(data):raise ValueError('truncated command payload WORD')
            payload=int.from_bytes(data[p:p+2],'big');p+=2
            count=((code-0x700)&127)+1
            row=dict(op='increment' if code&128 else 'repeat',word=payload,count=count,control_high_bits=word>>11)
            decoded+=count
        commands.append(row)
        if decoded>40:raise ValueError('column exceeds editing allocation')
    if decoded!=40:raise ValueError('column decoded allocation differs')
    return commands

def pack_column(commands):
    if type(commands) is not list or not 1<=len(commands)<=40:raise ValueError('bounded column commands required')
    encoded=bytearray();decoded=[]
    for row in commands:
        if type(row) is not dict:raise ValueError('command object required')
        if row.get('op')=='literal':
            keys(row,{'op','word'},'literal');word=uint(row['word'],65535,'literal WORD')
            if (word&0x7FF)>=0x6FF:raise ValueError('literal WORD has original command/ambiguous low11 bits')
            encoded.extend(word.to_bytes(2,'big'));decoded.append(word)
        elif row.get('op') in ('repeat','increment'):
            keys(row,{'op','word','count','control_high_bits'},'run')
            word=uint(row['word'],65535,'payload WORD');count=uint(row['count'],128,'run count')
            if count<1:raise ValueError('positive run count required')
            high=uint(row['control_high_bits'],31,'ignored control high bits')
            code=0x700+(count-1)+(128 if row['op']=='increment' else 0)
            encoded.extend(((high<<11)|code).to_bytes(2,'big'));encoded.extend(word.to_bytes(2,'big'))
            decoded.extend((word+(i if row['op']=='increment' else 0))&65535 for i in range(count))
        else:raise ValueError('unsupported column operation')
        if len(decoded)>40:raise ValueError('column exceeds editing allocation')
    if len(decoded)!=40:raise ValueError('column decoded allocation differs')
    return bytes(encoded),b''.join(word.to_bytes(2,'big') for word in decoded)

def extract(rom):
    targets,rows=layout(rom);result=metadata()
    result['directory']=dict(start=DIR,index_stride_word=4,width_byte=24,height_byte=40,base=START,
                             targets=[ident(p) for p in targets]+[None]*5)
    result['chunks']=[]
    for row in rows:
        columns=[parse_column(rom[row['base']+a:row['base']+b]) for a,b in zip(row['offsets'],row['offsets'][1:])]
        result['chunks'].append(dict(id=ident(row['start']),start=row['start'],end=row['end'],columns=columns))
    blocks(rom,result);return result

def blocks(rom,fields):
    _,rows=layout(rom);keys(fields,set(metadata())|{'directory','chunks'},'package')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    directory=fields['directory'];fixed=dict(start=DIR,index_stride_word=4,width_byte=24,height_byte=40,base=START)
    keys(directory,set(fixed)|{'targets'},'directory')
    for key,value in fixed.items():f.same(directory[key],value,'directory.'+key)
    catalog={ident(row['start']):row['start'] for row in rows};offsets=[]
    for target in exact_list(directory['targets'],29,'directory targets'):
        if target is None:offsets.append(65535)
        elif type(target) is str and target in catalog:offsets.append(catalog[target]-START)
        else:raise ValueError('directory target outside physical chunk catalog')
    directory_data=b'\x00\x04\x18\x28'+START.to_bytes(4,'big')+b''.join(n.to_bytes(2,'big') for n in offsets)
    result=[]
    for chunk,row in zip(exact_list(fields['chunks'],24,'chunks'),rows):
        keys(chunk,{'id','start','end','columns'},'chunk')
        for key,value in dict(id=ident(row['start']),start=row['start'],end=row['end']).items():f.same(chunk[key],value,'chunk.'+key)
        data=bytearray(row['base'].to_bytes(4,'big')+b''.join(n.to_bytes(2,'big') for n in row['offsets']))
        for commands,(a,b) in zip(exact_list(chunk['columns'],24,'columns'),zip(row['offsets'],row['offsets'][1:])):
            source,_=pack_column(commands)
            if len(source)!=b-a or parse_column(source)!=commands:raise ValueError('fixed column source cost/representation differs')
            data.extend(source)
        if len(data)!=row['end']-row['start']:raise ValueError('fixed chunk extent differs')
        result.append(dict(id=ident(row['start']),start=row['start'],end=row['end'],data=bytes(data),role='candidate_world_tile_column_chunk'))
    result.append(dict(id='world_chunk_directory',start=DIR,end=END,data=directory_data,role='candidate_world_tile_chunk_directory'))
    if sum(len(row['data']) for row in result)!=EDITABLE_BYTES or any(a['end']!=b['start'] for a,b in zip(result,result[1:])):
        raise ValueError('continuous physical partition differs')
    return result

def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)
def load_fields(data):return f.load_json(data)

def schema():
    def obj(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def fixed(value):
        if type(value) is dict:return obj({key:fixed(item) for key,item in value.items()})
        return dict(type={str:'string',int:'integer'}[type(value)],const=value)
    def number(maximum,minimum=0):return dict(type='integer',minimum=minimum,maximum=maximum)
    literal=obj(dict(op=fixed('literal'),word=number(65535)))
    run=obj(dict(op=dict(enum=['repeat','increment']),word=number(65535),count=number(128,1),control_high_bits=number(31)))
    column=dict(type='array',minItems=1,maxItems=40,items=dict(oneOf=[literal,run]))
    properties={key:fixed(value) for key,value in metadata().items()}
    properties['directory']=obj(dict(start=fixed(DIR),index_stride_word=fixed(4),width_byte=fixed(24),height_byte=fixed(40),base=fixed(START),
        targets=dict(type='array',minItems=29,maxItems=29,items=dict(type=['string','null']))))
    properties['chunks']=dict(type='array',minItems=24,maxItems=24,items=obj(dict(id=dict(type='string'),start=number(f.ROM_SIZE),end=number(f.ROM_SIZE),
        columns=dict(type='array',minItems=24,maxItems=24,items=column))))
    result=obj(properties);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='Runtime additionally validates fixed identities, source costs and low11 classification. Allocation is not a CPU clamp.'
    return result

def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('whole-ROM exact field roundtrip differs')
    chunks=[];counts=dict(literal=0,repeat=0,increment=0)
    for chunk in fields['chunks']:
        decoded=b''.join(pack_column(column)[1] for column in chunk['columns'])
        for column in chunk['columns']:
            for command in column:counts[command['op']]+=1
        chunks.append(dict(id=chunk['id'],start=chunk['start'],end=chunk['end'],decoded_words=960,decoded_sha256=sha(decoded),
                           source_sha256=sha(rom[chunk['start']:chunk['end']])))
    report=dict(confidence='confirmed_column_encoding_candidate_world_purpose',editable_bytes=EDITABLE_BYTES,physical_blocks=25,
                chunks=chunks,physical_columns=576,commands=counts,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
                consumers=dict(directory=[0xA0D2,0xA112,0xA2EE],lookup=0xAF6A,column_lookup=0xB0DE,first=0xB106,next=0xB1DA),
                decoded_allocation_not_CPU_hardware_limit=True,natural_selector_domain_complete=False,independent_CPU_comparison=False,
                original_first_continuing_boundary_06FF_editor_rejected=True,
                unknowns=['Natural coordinate/index domains; purpose labels are candidate.',
                          '29 physical directory slots are not a demonstrated natural selector domain.',
                          'AFBA tests the sign of its secondary offset, unlike A1 FFFF-only check; full WORD offsets retained.',
                          'Encoded editing does not prove resulting visible map/gameplay correctness.'],
                owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(format=FORMAT,confidence='candidate',editable_bytes=EDITABLE_BYTES,
        canonical_source=metadata()['canonical_source'],members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0))
    return members

def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/world_tile_chunks')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--fields',default=str(DEFAULT_FIELDS));parser.add_argument('--output')
    args=parser.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output) # reject unauthorized output BEFORE input reads
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
    elif args.output is not None:raise ValueError('verify writes no output')
    rom=f.read_bounded(args.rom,f.ROM_SIZE)
    if args.command=='export':
        bundle=render_bundle(rom);target.mkdir()
        for name,data in bundle.items():f.put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES)
    else:
        image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),sha256=sha(image),editable_bytes=EDITABLE_BYTES,exact_canonical=image==rom)
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
