"""Candidate typed FE/FF counted dictionary codec and fixed tail fields.

Tokens retain their original WORD class and every physical slot. Operational
interpretation is contextual: FF dictionary payloads are not recursively decoded,
and direct FE->FE takes the original special literal branch without a count test.
This is a producer's bounded data projection, not an independent CPU reference.
"""

from tools.resource_reference import reference_value
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.audio_formats import audio_formats as af

OUTPUT_ROOT=ROOT/'build/dictionary_streams'
FORMAT='candidate-counted-FE-FF-dictionary-tail-v1'
ROM_SHA=reference_value(__name__, 'ROM_SHA')
DEFAULT_ROM=ROOT.parent/'work/original_g5510.bin'
START=0xCE49A;END=0xD374A;EDITABLE_BYTES=END-START
CONSUMER=(0xADFC,0xAE8A)
CONSUMER_SHA=reference_value(__name__, 'CONSUMER_SHA')
SETS=((0xCE49A,0xCE61E,0xCFA12,0xD34C2),(0xCFA12,0xCFAE2,0xD1256,0xD34C4),
      (0xD12F6,0xD139E,0xD323A,0xD34C8))
COUNT_START=0xD34C2;COUNT_END=0xD34CA
RECORD_START=0xD323A;RECORD_END=0xD34C2
RAW_START=0xD1256;RAW_END=0xD12F6
TILE_START=0xD34CA;TILE_END=0xD374A
MAX_JSON=8*1024*1024
keys=af._keys;uint=af._integer;same=af._same
def sha(data):return hashlib.sha256(data).hexdigest()
def dump(value):return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
def words(raw):return [int.from_bytes(raw[i:i+2],'big') for i in range(0,len(raw),2)]
def word_bytes(values):return b''.join(value.to_bytes(2,'big') for value in values)
def token(value):
    if value<0xFE00:return dict(op='literal',word=value)
    if value<0xFF00:return dict(op='dictionary_word',index=value&255)
    return dict(op='repeat_word',count_minus_one=value&255)
def token_word(value):
    if type(value) is not dict or type(value.get('op')) is not str:raise ValueError('typed WORD token required')
    op=value['op']
    if op=='literal':keys(value,{'op','word'},'literal');return uint(value['word'],0xFDFF,'literal WORD')
    if op=='dictionary_word':keys(value,{'op','index'},'FE WORD');return 0xFE00|uint(value['index'],255,'FE index')
    if op=='repeat_word':keys(value,{'op','count_minus_one'},'FF WORD');return 0xFF00|uint(value['count_minus_one'],255,'FF encoded count')
    raise ValueError('unknown WORD token kind')
def exact_list(value,count,label):
    if type(value) is not list or len(value)!=count:raise ValueError(label+': fixed list size differs')
    return value
def metadata():return dict(format=FORMAT,source=dict(size=1048576,sha256=ROM_SHA),confidence='candidate',
    owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,start=START,end=END)
def set_metadata(base,source,end,count):return dict(id=f'rom_{base:06X}_dictionary_stream',dictionary_start=base,
    dictionary_end=source,source_start=source,source_end=end,count_address=count)
def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=1048576 or sha(rom)!=ROM_SHA:raise ValueError('canonical ROM identity/type/size required')
    if sha(rom[CONSUMER[0]:CONSUMER[1]])!=CONSUMER_SHA:raise ValueError('original consumer byte pin differs')

def evaluate(source,dictionary,count,maximum_output=262144,maximum_iterations=65536):
    """Original branch ordering as a bounded data projection, never CPU coverage."""
    if type(source) is not bytes or not source or len(source)%2 or len(source)>16384:raise ValueError('bounded even source required')
    if type(dictionary) is not bytes or not dictionary or len(dictionary)%4 or len(dictionary)>1024:raise ValueError('bounded2-WORD dictionary required')
    uint(count,65535,'D0 WORD');uint(maximum_output,262144,'resource output bound');uint(maximum_iterations,65536,'resource iterations')
    cursor=0;d0=count;pending=0;pointer=0;output=bytearray();source_reads=[];dictionary_reads=[];branches={}
    def branch(name):branches[name]=branches.get(name,0)+1
    def read_dict(at,peek=False):
        if at<0 or at+2>len(dictionary):raise ValueError('dictionary read out of fixed allocation')
        dictionary_reads.append(dict(offset=at,peek=peek));return int.from_bytes(dictionary[at:at+2],'big')
    def read_source():
        nonlocal cursor,d0
        if cursor+2>len(source):raise ValueError('source read beyond fixed allocation')
        value=int.from_bytes(source[cursor:cursor+2],'big');source_reads.append(cursor);cursor+=2;d0=(d0-1)&65535;return value
    def emit(value,n=1):
        output.extend(value.to_bytes(2,'big')*n)
        if len(output)>maximum_output:raise ValueError('decoded resource bound exceeded')
    def ended():return pending==0 and d0>=0x8000
    for _ in range(maximum_iterations):
        if pending:value=read_dict(pointer);pointer+=2;pending=(pending-1)&255;origin='dictionary'
        else:value=read_source();origin='source'
        if value<0xFE00:
            branch('literal_'+origin);emit(value)
            if ended():break
        elif value<0xFF00:
            pointer=4*(value&255);first=read_dict(pointer,True)
            if 0xFE00<=first<0xFF00:
                branch('direct_FE_to_FE_literal_without_count_test');emit(first)
                # 00AE42 BRA 00AE04: do NOT decrement pending or test D0 here.
            else:branch('dictionary_pair');pending=2
        else:
            n=(value&255)+1
            if pending:
                following=read_dict(pointer);pointer+=2;pending=(pending-1)&255
                branch('FF_payload_from_dictionary_no_FE_recursion')
            else:
                following=read_source();branch('FF_payload_from_source')
                if 0xFE00<=following<0xFF00:
                    pointer=4*(following&255);following=read_dict(pointer);pointer+=2;pending=1
                    branch('FF_source_FE_first_repeat_second_pending')
            emit(following,n)
            if ended():break
    else:raise ValueError('bounded iteration limit reached')
    return dict(decoded=bytes(output),source_bytes_read=cursor,count_final_word=d0,pending_final_byte=pending,
        source_read_offsets=source_reads,dictionary_reads=dictionary_reads,branches=branches,
        independent_CPU_comparison=False)

def extract(rom):
    verify_rom(rom);fields=metadata();sets=[]
    for base,source,end,count in SETS:
        row=set_metadata(base,source,end,count);table=words(rom[base:source])
        row['dictionary_entries']=[[token(table[i]),token(table[i+1])] for i in range(0,len(table),2)]
        row['source_tokens']=[token(value) for value in words(rom[source:end])];sets.append(row)
    fields['datasets']=sets
    fields['count_fields']=[dict(address=address,value=int.from_bytes(rom[address:address+2],'big')) for address in range(COUNT_START,COUNT_END,2)]
    fields['records']=dict(start=RECORD_START,end=RECORD_END,
        records=[dict(id=f'rom_{RECORD_START+i*36:06X}_record',words=words(rom[RECORD_START+i*36:RECORD_START+(i+1)*36])) for i in range(18)])
    fields['raw_transfer']=dict(start=RAW_START,end=RAW_END,longs=[int.from_bytes(rom[a:a+4],'big') for a in range(RAW_START,RAW_END,4)])
    fields['raw_tiles']=dict(start=TILE_START,end=TILE_END,tiles=[])
    for tile in range(20):
        raw=rom[TILE_START+tile*32:TILE_START+(tile+1)*32]
        pixels=[[(raw[y*4+x//2]>>(4 if x%2==0 else 0))&15 for x in range(8)] for y in range(8)]
        fields['raw_tiles']['tiles'].append(dict(id=f'rom_{TILE_START+tile*32:06X}_tile',pixels=pixels))
    return fields

def _pack_tokens(values,canonical,label):
    exact_list(values,len(canonical),label);output=[]
    for value,original in zip(values,canonical):
        word=token_word(value)
        if value['op']!=original['op']:raise ValueError(label+': original token WORD kind changed')
        output.append(word)
    return word_bytes(output)

def pack(rom,fields):
    verify_rom(rom);original=extract(rom);fixed=metadata();keys(fields,set(original),'tail fields')
    for key,value in fixed.items():same(fields[key],value,key)
    count_fields=exact_list(fields['count_fields'],4,'count fields');counts={};chunks=[]
    for row,old in zip(count_fields,original['count_fields']):
        keys(row,{'address','value'},'count WORD');same(row['address'],old['address'],'count address');counts[row['address']]=uint(row['value'],65535,'count WORD')
    chunks.append((COUNT_START,COUNT_END,word_bytes([counts[address] for address in range(COUNT_START,COUNT_END,2)]),'count_fields'))
    projections=[]
    for row,old,(base,source,end,count_address) in zip(exact_list(fields['datasets'],3,'datasets'),original['datasets'],SETS):
        keys(row,set(old),'dataset')
        for key,value in set_metadata(base,source,end,count_address).items():same(row[key],value,'dataset.'+key)
        table=[]
        for pair,old_pair in zip(exact_list(row['dictionary_entries'],len(old['dictionary_entries']),'dictionary'),old['dictionary_entries']):
            table.append(_pack_tokens(pair,old_pair,'dictionary pair'))
        dictionary=b''.join(table);commands=_pack_tokens(row['source_tokens'],old['source_tokens'],'source tokens')
        count=counts[count_address]
        if count>=len(commands)//2:raise ValueError('count exceeds fixed source allocation')
        result=evaluate(commands,dictionary,count)
        # Editing policy: end a complete count-delimited prefix; preserve suffix fields.
        if result['count_final_word']!=65535 or result['pending_final_byte']!=0 or result['source_bytes_read']!=2*(count+1):raise ValueError('count does not end a complete packet/dictionary prefix')
        projections.append(dict(id=row['id'],source_start=source,source_end=source+result['source_bytes_read'],
            decoded_bytes=len(result['decoded']),decoded_sha256=sha(result['decoded']),branches=result['branches'],
            dictionary_offsets_unique=sorted({entry['offset'] for entry in result['dictionary_reads']}),independent_CPU_comparison=False))
        chunks.extend(((base,source,dictionary,'dictionary'),(source,end,commands,'commands')))
    records=fields['records'];keys(records,{'start','end','records'},'records');same(records['start'],RECORD_START,'record start');same(records['end'],RECORD_END,'record end')
    record_bytes=[]
    for row,old in zip(exact_list(records['records'],18,'records'),original['records']['records']):
        keys(row,{'id','words'},'record');same(row['id'],old['id'],'record id')
        record_bytes.append(word_bytes([uint(value,65535,'record BE16') for value in exact_list(row['words'],18,'record WORDs')]))
    chunks.append((RECORD_START,RECORD_END,b''.join(record_bytes),'records'))
    raw=fields['raw_transfer'];keys(raw,{'start','end','longs'},'transfer');same(raw['start'],RAW_START,'transfer start');same(raw['end'],RAW_END,'transfer end')
    if counts[0xD34C6]>=40:raise ValueError('raw LONG count exceeds fixed slot')
    chunks.append((RAW_START,RAW_END,b''.join(uint(value,0xFFFFFFFF,'raw BE32').to_bytes(4,'big') for value in exact_list(raw['longs'],40,'raw LONGs')),'transfer'))
    tiles=fields['raw_tiles'];keys(tiles,{'start','end','tiles'},'tiles');same(tiles['start'],TILE_START,'tile start');same(tiles['end'],TILE_END,'tile end');tile_bytes=bytearray()
    for row,old in zip(exact_list(tiles['tiles'],20,'tiles'),original['raw_tiles']['tiles']):
        keys(row,{'id','pixels'},'tile');same(row['id'],old['id'],'tile id')
        for pixels in exact_list(row['pixels'],8,'pixel rows'):
            pixels=exact_list(pixels,8,'pixel columns')
            for x in range(0,8,2):tile_bytes.append(uint(pixels[x],15,'pixel')<<4|uint(pixels[x+1],15,'pixel'))
    chunks.append((TILE_START,TILE_END,bytes(tile_bytes),'raw_tiles'))
    cursor=START
    for first,last,data,kind in sorted(chunks):
        if first!=cursor or len(data)!=last-first:raise ValueError('physical gap/overlap/width in typed field plan')
        cursor=last
    if cursor!=END:raise ValueError('tail plan incomplete')
    return chunks,projections

def rebuild(rom,fields):
    chunks,projections=pack(rom,fields);image=bytearray(rom)
    for first,last,data,kind in chunks:image[first:last]=data
    if image[:START]!=rom[:START] or image[END:]!=rom[END:]:raise ValueError('escaped physical write plan')
    return bytes(image)

def blocks(rom,fields):
    """Explicit additive-layout blocks, all rebuilt from true typed fields.

    No code, preceding unknown gaps, rawhex blobs or independently duplicated
    authority is emitted. Stable IDs identify physical ROM slots, not purposes.
    """
    chunks,projections=pack(rom,fields)
    roles={'dictionary':'dictionary_pair_WORDs','commands':'FE_FF_command_WORDs',
        'records':'record_BE16_WORDs','transfer':'raw_transfer_BE32_LONGs',
        'raw_tiles':'raw_4bpp_pixel_tiles','count_fields':'count_BE16_WORDs'}
    return [dict(id=f'rom_{first:06X}_{roles[kind]}',start=first,end=last,data=data,role=roles[kind])
        for first,last,data,kind in sorted(chunks)]

def load_json(data):
    if type(data) is not bytes or len(data)>MAX_JSON:raise ValueError('bounded UTF8 JSON required')
    def pairs(items):
        out={}
        for key,value in items:
            if key in out:raise ValueError('duplicate JSON key')
            out[key]=value
        return out
    def nonfinite(value):raise ValueError('nonfinite JSON')
    try:return json.loads(data.decode('utf-8'),object_pairs_hook=pairs,parse_constant=nonfinite)
    except (UnicodeError,json.JSONDecodeError,RecursionError) as exc:raise ValueError('invalid JSON') from exc

def safe(value,regular=False):
    text=str(value).replace('/',chr(92))
    if text.startswith(chr(92)*2) or text.startswith(chr(92)+'??'+chr(92)) or text.upper().startswith('\\DEVICE\\'):raise ValueError('UNC/device rejected before resolve/read')
    return af.safe_path(value,regular_input=regular)
def output_path(value):
    path=safe(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT.resolve() not in path.parents or path.exists() or not path.parent.is_dir():raise ValueError('fresh dedicated build/dictionary_streams output required')
    return path
def read(value,maximum):return af._read(safe(value,True),maximum)
def write(path,data):
    with path.open('xb') as stream:stream.write(data)

def render(rom):
    fields=extract(rom);raw=dump(fields);parsed=load_json(raw);image=rebuild(rom,parsed);chunks,projections=pack(rom,parsed)
    if image!=rom:raise ValueError('whole ROM roundtrip failed')
    report=dict(format=FORMAT,confidence='candidate',whole_ROM_roundtrip=True,ROM_sha256=sha(image),
        new_field_bytes=EDITABLE_BYTES,code_emitted_bytes=0,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        fields_by_kind={kind:sum(last-first for first,last,data,item_kind in chunks if item_kind==kind) for kind in {row[3] for row in chunks}},
        understood_layout_gap_bytes=0,unknown_previous_interval=dict(start=0xCE31A,end=START,bytes=START-0xCE31A,confidence='unknown'),
        projections=projections,independent_CPU_comparison=False,promotion=True)
    members={'fields.json':raw,'validation.json':dump(report)}
    members['manifest.json']=dump(dict(format=FORMAT,confidence='candidate',members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},
        new_field_bytes=EDITABLE_BYTES,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,independent_CPU_comparison=False,promotion=True))
    return members

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('export','import','verify'));parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--output');parser.add_argument('--fields');parser.add_argument('--bundle');args=parser.parse_args(argv)
    target=None
    if args.command in ('export','import'):
        if args.output is None:raise ValueError('fresh output required')
        target=output_path(args.output)
    if args.command=='export' and (args.fields is not None or args.bundle is not None):raise ValueError('export output only')
    if args.command=='import' and (args.fields is None or args.bundle is not None or target.suffix.lower()!='.bin'):raise ValueError('import fields/fresh bin required')
    if args.command=='verify' and (args.output is not None or args.fields is not None or args.bundle is None):raise ValueError('verify bundle only')
    rom=read(args.rom,1048576)
    if args.command=='export':
        bundle=render(rom);target.mkdir()
        for name,data in bundle.items():write(target/name,data)
        print(json.dumps(dict(path=str(target),members={name:sha(data) for name,data in bundle.items()}),sort_keys=True))
    elif args.command=='import':
        image=rebuild(rom,load_json(read(args.fields,MAX_JSON)));write(target,image);print(json.dumps(dict(path=str(target),bytes=len(image),sha256=sha(image)),sort_keys=True))
    else:
        directory=safe(args.bundle);expected=render(rom)
        if not directory.is_dir() or {path.name for path in directory.iterdir()}!=set(expected):raise ValueError('bundle members differ')
        for name,data in expected.items():
            if read(directory/name,MAX_JSON)!=data:raise ValueError('canonical bundle drift')
        print('candidate dictionary format verify PASS; independent_CPU_comparison=false promotion=false')
    return 0

if __name__=='__main__':raise SystemExit(main())
