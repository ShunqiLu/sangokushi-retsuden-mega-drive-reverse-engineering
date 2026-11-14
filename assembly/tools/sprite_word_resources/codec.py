"""Editable 067B10 resources: sprite slots, WORD RLE and counted FE/FF streams.

Allocation/counts and decoded sizes are editing contracts for these original
resources, never CPU selector clamps or hardware limits. Source fields remain
the sole authority. The existing dictionary codec is reused, not a new CPU.
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
from tools.dictionary_streams import codec as dictionary

DEFAULT_ROM=f.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/sprite_word_resources/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/sprite_word_resources'
FORMAT='candidate-sprite-and-counted-word-resources-v1'
EDITABLE_BYTES=17401
SPRITE_DIRECTORY=0x67B10
SPRITE_START=0x67B90
SPRITE_END=0x67C90
RLE_END=0x68C13
SETS=((0x68C24,0x68CE8,0x6A616,0x6BF06),(0x6A616,0x6A692,0x6BF06,0x6BF08))
keys=f.keys;uint=f.uint;sha=f.sha;dump=f.dump

def ident(start):return f'rom_{start:06X}_spritewords'
def exact_list(value,count,label):
    if type(value) is not list or len(value)!=count:raise ValueError(label+': fixed allocation differs')
    return value
def same(value,wanted,label):return f.same(value,wanted,label)
def word(raw):return int.from_bytes(raw,'big')
def signed(value,bits):return value if value<(1<<(bits-1)) else value-(1<<bits)

def metadata():
    return dict(format=FORMAT,source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),confidence='candidate',
                owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)

def sprite(raw,start):
    x,attribute,shape_y=(word(raw[i:i+2]) for i in (0,2,4))
    if x==0x8000:raise ValueError('sprite body must precede its terminator')
    if raw[6:]!=b'\x80\0':raise ValueError('single-record fixed sprite terminator differs')
    return dict(id=ident(start),x_offset=signed(x,16),tile_index=attribute&0x7FF,
                horizontal_flip=bool(attribute&0x800),vertical_flip=bool(attribute&0x1000),
                palette=(attribute>>13)&3,priority=bool(attribute&0x8000),
                width_tiles=((shape_y>>14)&3)+1,height_tiles=((shape_y>>12)&3)+1,
                y_offset=signed(shape_y&0xFFF,12))

def sprite_bytes(row,start):
    keys(row,set(sprite(b'\0\0\0\0\0\0\x80\0',start)),'sprite descriptor')
    same(row['id'],ident(start),'sprite id')
    def flag(key):
        if type(row[key]) is not bool:raise ValueError(key+': boolean required')
        return int(row[key])
    def offset(key,lo,hi):
        value=row[key]
        if type(value) is not int or not lo<=value<=hi:raise ValueError(key+': signed offset out of range')
        return value
    x=offset('x_offset',-32767,32767)&65535 # 8000 is the consumer's terminator, not a descriptor
    y=offset('y_offset',-2048,2047)&4095
    width=uint(row['width_tiles'],4,'width_tiles');height=uint(row['height_tiles'],4,'height_tiles')
    if width<1 or height<1:raise ValueError('sprite shape requires1..4 tiles')
    attribute=uint(row['tile_index'],2047,'tile_index')|flag('horizontal_flip')<<11|flag('vertical_flip')<<12
    attribute|=uint(row['palette'],3,'palette')<<13|flag('priority')<<15
    shape_y=((width-1)<<14)|((height-1)<<12)|y
    return b''.join(v.to_bytes(2,'big') for v in (x,attribute,shape_y,0x8000))

def set_metadata(index):
    base,source,end,count=SETS[index]
    return dict(id=ident(base),dictionary_start=base,dictionary_end=source,source_start=source,
                source_end=end,count_address=count,source_words=(end-source)//2,
                count_word=(end-source)//2-1,decoded_bytes=8192)

def extract(rom):
    f.verify_rom(rom);result=metadata()
    starts=list(range(SPRITE_START,SPRITE_END,8))
    pointers=[word(rom[p:p+4]) for p in range(SPRITE_DIRECTORY,SPRITE_START,4)]
    if pointers!=starts:raise ValueError('original32 sprite physical slots differ')
    result['sprite_directory']=[ident(start) for start in pointers]
    result['sprites']=[sprite(rom[start:start+8],start) for start in starts]
    result['tile_stream']=rle.parse_word(rom[SPRITE_END:RLE_END],'little',4096)
    expected=[SETS[0][1],SETS[1][1],SETS[0][0],SETS[1][0]]
    if [word(rom[p:p+4]) for p in range(0x68C14,0x68C24,4)]!=expected:
        raise ValueError('original two source/dictionary directories differ')
    result['dictionary_directories']=dict(source_targets=[ident(row[0]) for row in SETS],
                                           dictionary_targets=[ident(row[0]) for row in SETS])
    result['dictionary_streams']=[]
    for index,(base,source,end,count) in enumerate(SETS):
        if word(rom[count:count+2])!=(end-source)//2-1:raise ValueError('original source count differs')
        result['dictionary_streams'].append({**set_metadata(index),
            'dictionary_pairs':[[word(rom[p:p+2]),word(rom[p+2:p+4])] for p in range(base,source,4)],
            'source_tokens':[dictionary.token(word(rom[p:p+2])) for p in range(source,end,2)]})
    blocks(rom,result)
    return result

def blocks(rom,fields):
    f.verify_rom(rom)
    keys(fields,set(metadata())|{'sprite_directory','sprites','tile_stream','dictionary_directories','dictionary_streams'},'package')
    for key,value in metadata().items():same(fields[key],value,'package.'+key)
    result=[]
    def add(start,end,data,role):
        if type(data) is not bytes or len(data)!=end-start:raise ValueError('fixed byte allocation differs')
        result.append(dict(id=ident(start),start=start,end=end,data=data,role=role))
    sprite_ids={ident(start):start for start in range(SPRITE_START,SPRITE_END,8)}
    targets=exact_list(fields['sprite_directory'],32,'sprite directory')
    if any(type(target) is not str or target not in sprite_ids for target in targets):raise ValueError('sprite directory target outside editor catalog')
    add(SPRITE_DIRECTORY,SPRITE_START,b''.join(sprite_ids[target].to_bytes(4,'big') for target in targets),'candidate_sprite_directory')
    rows=exact_list(fields['sprites'],32,'sprite slots')
    add(SPRITE_START,SPRITE_END,b''.join(sprite_bytes(row,start) for row,start in zip(rows,range(SPRITE_START,SPRITE_END,8))),
        'candidate_packed_sprite_descriptors')
    f.strict_commands(fields['tile_stream'])
    encoded,decoded=rle.pack_word(fields['tile_stream'],'little',4096)
    if rle.parse_word(encoded,'little',4096)!=fields['tile_stream']:raise ValueError('RLE representation differs')
    add(SPRITE_END,RLE_END,encoded,'candidate_little_word_rle_tiles')
    dirs=fields['dictionary_directories'];keys(dirs,{'source_targets','dictionary_targets'},'dictionary directories')
    catalog={ident(base):(base,source) for base,source,_,_ in SETS}
    raw_dirs=[]
    for key,lane in (('source_targets',1),('dictionary_targets',0)):
        values=exact_list(dirs[key],2,key)
        for value in values:
            if type(value) is not str or value not in catalog:raise ValueError('dictionary target outside editor catalog')
            raw_dirs.append(catalog[value][lane].to_bytes(4,'big'))
    add(0x68C14,0x68C24,b''.join(raw_dirs),'candidate_word_resource_directories')
    sets=exact_list(fields['dictionary_streams'],2,'dictionary sets');encoded_sets={}
    counts=bytearray()
    for index,(row,(base,source,end,count)) in enumerate(zip(sets,SETS)):
        keys(row,set(set_metadata(index))|{'dictionary_pairs','source_tokens'},'dictionary set')
        for key,value in set_metadata(index).items():same(row[key],value,'set.'+key)
        pairs=exact_list(row['dictionary_pairs'],(source-base)//4,'dictionary pairs')
        values=[]
        for pair in pairs:values.extend(uint(v,65535,'dictionary WORD') for v in exact_list(pair,2,'dictionary pair'))
        dict_raw=b''.join(v.to_bytes(2,'big') for v in values)
        tokens=exact_list(row['source_tokens'],(end-source)//2,'source tokens')
        source_raw=b''.join(dictionary.token_word(token).to_bytes(2,'big') for token in tokens)
        add(base,source,dict_raw,'candidate_two_word_dictionary')
        add(source,end,source_raw,'candidate_counted_fe_ff_source')
        encoded_sets[row['id']]=(dict_raw,source_raw,row['count_word'])
        counts.extend(row['count_word'].to_bytes(2,'big'))
    add(0x6BF06,0x6BF0A,bytes(counts),'candidate_source_count_words')
    # Validate the actual catalog pairing. This is a bounded codec projection,
    # not full CPU/VDP execution or a clamp of original selectors/counts.
    for index in range(2):
        dict_raw=encoded_sets[dirs['dictionary_targets'][index]][0]
        source_raw=encoded_sets[dirs['source_targets'][index]][1]
        count=sets[index]['count_word'] # original caller count belongs to the slot, not a redirected source
        decoded=dictionary.evaluate(source_raw,dict_raw,count)
        if decoded['source_bytes_read']!=len(source_raw) or decoded['pending_final_byte']!=0 or len(decoded['decoded'])!=8192:
            raise ValueError('edited stream violates fixed source/decoded allocation contract')
    result.sort(key=lambda row:row['start'])
    if any(a['end']>b['start'] for a,b in zip(result,result[1:])) or sum(row['end']-row['start'] for row in result)!=EDITABLE_BYTES:
        raise ValueError('physical scope overlap/size differs')
    return result

def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)

def load_fields(data):return f.load_json(data)
def schema():
    def obj(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def integer(low,high):return dict(type='integer',minimum=low,maximum=high)
    def fixed(value):
        if type(value) is dict:return obj({key:fixed(item) for key,item in value.items()})
        return dict(type={str:'string',int:'integer'}[type(value)],const=value)
    def array(count,item):return dict(type='array',minItems=count,maxItems=count,items=item)
    boolean=dict(type='boolean')
    properties={key:fixed(value) for key,value in metadata().items()}
    properties['sprite_directory']=array(32,dict(type='string',enum=[ident(p) for p in range(SPRITE_START,SPRITE_END,8)]))
    sprites=[]
    for p in range(SPRITE_START,SPRITE_END,8):
        sprites.append(obj(dict(id=fixed(ident(p)),x_offset=integer(-32767,32767),y_offset=integer(-2048,2047),
            tile_index=integer(0,2047),horizontal_flip=boolean,vertical_flip=boolean,palette=integer(0,3),priority=boolean,
            width_tiles=integer(1,4),height_tiles=integer(1,4))))
    properties['sprites']=dict(type='array',minItems=32,maxItems=32,prefixItems=sprites,items=False)
    literal=obj(dict(op=fixed('literal'),word=integer(0,65535)))
    repeat=obj(dict(op=fixed('repeat'),word=integer(0,65535),count=integer(2,256)))
    properties['tile_stream']=obj(dict(marker=integer(0,255),commands=dict(type='array',maxItems=4096,items=dict(oneOf=[literal,repeat]))))
    target=array(2,dict(type='string',enum=[ident(row[0]) for row in SETS]))
    properties['dictionary_directories']=obj(dict(source_targets=target,dictionary_targets=target))
    token=dict(oneOf=[obj(dict(op=fixed('literal'),word=integer(0,0xFDFF))),
                      obj(dict(op=fixed('dictionary_word'),index=integer(0,255))),
                      obj(dict(op=fixed('repeat_word'),count_minus_one=integer(0,255)))])
    sets=[]
    for index,(base,source,end,_) in enumerate(SETS):
        props={key:fixed(value) for key,value in set_metadata(index).items()}
        props.update(dictionary_pairs=array((source-base)//4,array(2,integer(0,65535))),
                     source_tokens=array((end-source)//2,token))
        sets.append(obj(props))
    properties['dictionary_streams']=dict(type='array',minItems=2,maxItems=2,prefixItems=sets,items=False)
    result=obj(properties);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='Runtime validator additionally checks encoded costs, original caller counts and bounded decoder outcomes; no natural selector clamp.'
    return result

def render_bundle(rom):
    fields=extract(rom);encoded=dump(fields);image=rebuild(rom,load_fields(encoded))
    if image!=rom:raise ValueError('entire-ROM field roundtrip differs')
    report=dict(confidence='confirmed_encoding_candidate_purpose',whole_ROM_exact=True,whole_ROM_sha256=sha(image),
                editable_bytes=EDITABLE_BYTES,blocks=[{k:v for k,v in row.items() if k!='data'}|{'sha256':sha(row['data'])} for row in blocks(rom,fields)],
                observed_decoded_bytes=[8192,8192,8192],decoded_sizes_are_editor_contract_not_hardware_limits=True,
                unknown_retained=[[0x68C13,0x68C14],[0x6BF0A,0x6C1B4],[0x50000,0x5D5E4]],
                original_consumers={'sprite_lookup':[0x67ACA,0x67AD0],'sprite_reader':[0xAC10,0xAD00],
                                    'word_RLE':[0x67A1C,0x67A26,0x3AB52],
                                    'dictionary_calls':[0x1771A,0x17734,0x17744,0x17764,0xADFC]},
                reused_implementation=['graphics_build.rle_fields','dictionary_streams.codec'],
                no_new_independent_CPU_reference=True,natural_domains_added=0,owner_bytes_added=0)
    members={'fields.json':encoded,'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(format=FORMAT,confidence='candidate',editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},
        source=metadata()['source'],owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0))
    return members

def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in owned resource build directory')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--fields',default=str(DEFAULT_FIELDS))
    parser.add_argument('--output');args=parser.parse_args(argv)
    target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output) # authority BEFORE input resolution/read
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin output required')
    elif args.output is not None:raise ValueError('verify does not write an output')
    rom=f.read_bounded(args.rom,f.ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():f.put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members=list(members))
    else:
        fields=load_fields(f.read_bounded(args.fields,f.MAX_JSON));image=rebuild(rom,fields)
        if args.command=='import':f.put(target,image)
        result=dict(path=None if target is None else str(target),sha256=sha(image),bytes=len(image),
                    editable_bytes=EDITABLE_BYTES,exact_canonical=image==rom)
    print(json.dumps(result,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
