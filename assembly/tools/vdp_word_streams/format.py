"""Candidate fixed-allocation VDP WORD streams; no owner or CPU admission.

This reuses the accepted graphics_build WORD-RLE grammar. 4096 decoded WORDs
is an editing-package contract for these19 datasets, not a CPU/hardware limit.
All data APIs take explicit byte arguments; files are opened only by CLI APIs.
"""
from __future__ import annotations

from tools.resource_metadata import compare_fixed_fields

from tools.resource_reference import reference_value
import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUTPUT_ROOT=ROOT/'build/vdp_word_streams'
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.graphics_build import rle_fields as rle

ROM_SHA=reference_value(__name__, 'ROM_SHA')
ROM_SIZE=1048576
DEFAULT_ROM=ROOT.parent/'work/original_g5510.bin'
FORMAT='candidate-rom-vdpword-fixed-fields-v1'
DIRECTORY_START=0x387BA
DIRECTORY_END=0x388FA
TARGETS=(871746,871746,876995,881408,881408,876995,888847,895916,901943,901943,
 888847,895916,907562,881408,907562,881408,907562,881408,907562,881408,901943,895916,
 913271,913271,919254,919254,913271,924073,929126,929126,932865,937912,942941,959340,
 952549,965263,971628,965263,971628,971628,876995,876995,881408,888847,888847,881408,
 895916,901943,907562,907562,895916,901943,913271,888847,913271,888847,913271,888847,
 913271,888847,907562,901943,919254,919254,924073,924073,919254,929126,932865,932865,
 937912,942941,946626,965263,959340,971628,976367,971628,976367,976367)
STARTS=tuple(sorted(set(TARGETS)))
ENDS=STARTS[1:]+(0xEE5F2,)
ALLOCATIONS=tuple(zip(STARTS,ENDS))
EMPTY_START=0xEE5EF
REUSE_START=0xEE5F0
REUSE_END=0xEE5F2
REUSE_BYTES=bytes.fromhex('0000')
CONSUMER_START=0x39658
CONSUMER_END=0x3969A
CONSUMER_SHA=reference_value(__name__, 'CONSUMER_SHA')
MAX_JSON=16*1024*1024
MAX_PACKET_BYTES=8192
MAX_PACKAGE_WORDS=65536

def sha(data):return hashlib.sha256(data).hexdigest()
def dump(value):return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def keys(value,expected,label):
    if type(value) is not dict or set(value)!=set(expected):raise ValueError(label+': missing/unknown fields')
def same(value,expected,label):
    if type(value) is not type(expected) or value!=expected:raise ValueError(label+': canonical topology/type differs')
    if type(expected) is dict:
        for key in expected:same(value[key],expected[key],label+'.'+key)
    elif type(expected) is list:
        for i,item in enumerate(expected):same(value[i],item,label+'['+str(i)+']')
def uint(value,maximum,label):
    if type(value) is not int or not 0<=value<=maximum:raise ValueError(label+': strict unsigned integer required')
    return value
def ident(start):return f'rom_{start:06X}_vdpword'
def directory():return [dict(index=i,address=DIRECTORY_START+4*i,target=target,block=ident(target)) for i,target in enumerate(TARGETS)]
def reuse():return dict(start=REUSE_START,end=REUSE_END,bytes=2,expected_hex='0000',
    owner_package='world_resources',owner_field='terrain_codes',physical_emit=False)
def metadata():return dict(format=FORMAT,canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA),
    confidence='candidate',owner_admission=False,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
    directory=dict(start=DIRECTORY_START,end=DIRECTORY_END,LONG_order='big',entries=directory()),
    reused_terrain_dependency=reuse())
def topology(start,end):return dict(id=ident(start),start=start,end=end,
    decoded_words=0 if start==EMPTY_START else 4096,
    physical_emit_bytes=0 if start==EMPTY_START else end-start,
    read_boundary=end,aliases=[i for i,target in enumerate(TARGETS) if target==start])

def verify_rom(rom,terrain_dependency=None):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE:raise ValueError('canonical ROM bytes/size required')
    if rom[REUSE_START:REUSE_END]!=REUSE_BYTES:raise ValueError('reused terrain conflict in base ROM')
    if terrain_dependency is not None:
        if type(terrain_dependency) is not bytes or terrain_dependency!=REUSE_BYTES:raise ValueError('reused terrain dependency conflict')
    if sha(rom)!=ROM_SHA:raise ValueError('forged/noncanonical ROM identity')
    table=b''.join(target.to_bytes(4,'big') for target in TARGETS)
    if rom[DIRECTORY_START:DIRECTORY_END]!=table:raise ValueError('original directory drift')
    if sha(rom[CONSUMER_START:CONSUMER_END])!=CONSUMER_SHA:raise ValueError('original consumer byte identity drift')
    return rom

def strict_commands(fields):
    keys(fields,{'marker','commands'},'stream fields');uint(fields['marker'],255,'marker')
    commands=fields['commands']
    if type(commands) is not list or len(commands)>MAX_PACKAGE_WORDS:raise ValueError('bounded command list required')
    for command in commands:
        if type(command) is not dict or type(command.get('op')) is not str:raise ValueError('command object/op type')
        op=command['op']
        if op=='literal':keys(command,{'op','word'},'literal')
        elif op=='repeat':
            keys(command,{'op','word','count'},'repeat');uint(command['count'],256,'repeat count')
            if command['count']<2:raise ValueError('repeat emits2..256 WORDs')
        else:raise ValueError('unknown command operation')
        uint(command['word'],65535,'WORD')

def encode_stream(fields,expected_words):
    uint(expected_words,MAX_PACKAGE_WORDS,'bounded package WORD count');strict_commands(fields)
    encoded,decoded=rle.pack_word(fields,'big',expected_words)
    if len(encoded)>MAX_PACKET_BYTES:raise ValueError('bounded packet bytes exceeded')
    return encoded,decoded

def parse_stream(data,expected_words):
    uint(expected_words,MAX_PACKAGE_WORDS,'bounded package WORD count')
    if type(data) is not bytes or not 3<=len(data)<=MAX_PACKET_BYTES:raise ValueError('bounded complete stream bytes required')
    result=rle.parse_word(data,'big',expected_words)
    encoded,decoded=encode_stream(result,expected_words)
    if encoded!=data:raise ValueError('packet representation failed exact roundtrip')
    return result

def extract(rom,terrain_dependency=None):
    verify_rom(rom,terrain_dependency);result=metadata();blocks=[]
    for start,end in ALLOCATIONS:
        row=topology(start,end);row['fields']=parse_stream(rom[start:end],row['decoded_words']);blocks.append(row)
    result['blocks']=blocks
    return result

def validate_fields(value,terrain_dependency=REUSE_BYTES):
    compare_fixed_fields(value, metadata(), ('blocks',), 'package')
    if type(terrain_dependency) is not bytes or terrain_dependency!=REUSE_BYTES:raise ValueError('reused terrain dependency conflict')
    blocks=value['blocks']
    if type(blocks) is not list or len(blocks)!=20:raise ValueError('exact20physical blocks required, no collapse')
    packed=[]
    for row,(start,end) in zip(blocks,ALLOCATIONS):
        fixed_row=topology(start,end);keys(row,set(fixed_row)|{'fields'},'block')
        for key,expected in fixed_row.items():same(row[key],expected,'block.'+key)
        encoded,decoded=encode_stream(row['fields'],fixed_row['decoded_words'])
        if len(encoded)!=end-start:raise ValueError('fixed encoded slot allocation differs')
        # Reparse checks termination/read boundary and repeat marker consistency.
        if parse_stream(encoded,fixed_row['decoded_words'])!=row['fields']:raise ValueError('packet/read boundary drift')
        if start==EMPTY_START and encoded!=bytes([0])+terrain_dependency:raise ValueError('empty stream terrain conflict/read boundary')
        packed.append(dict(start=start,end=end,encoded=encoded,decoded=decoded,physical_emit=start!=EMPTY_START))
    return packed

def import_fields(rom,fields,terrain_dependency=None):
    verify_rom(rom,terrain_dependency)
    dependency=rom[REUSE_START:REUSE_END] if terrain_dependency is None else terrain_dependency
    packed=validate_fields(fields,dependency);image=bytearray(rom)
    for block in packed:
        # The empty stream's1B prefix is immutable; terrain2B is reused only.
        # Neither this package nor the directory performs a second physical emit.
        if block['physical_emit']:image[block['start']:block['end']]=block['encoded']
    if image[REUSE_START:REUSE_END]!=dependency or image[EMPTY_START]!=0:raise ValueError('terrain/prefix changed')
    return bytes(image)

def projection(fields):
    packed=validate_fields(fields)
    return [dict(id=ident(row['start']),start=row['start'],end=row['end'],encoded_bytes=len(row['encoded']),
        decoded_bytes=len(row['decoded']),encoded_sha256=sha(row['encoded']),decoded_sha256=sha(row['decoded']),
        physical_emit=row['physical_emit'],actual_CPU_comparison=False) for row in packed]

def load_json(data):
    if type(data) is not bytes or len(data)>MAX_JSON:raise ValueError('bounded JSON bytes required')
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('duplicate JSON key: '+key)
            result[key]=value
        return result
    def nonfinite(value):raise ValueError('nonfinite JSON number: '+value)
    try:return json.loads(data.decode('utf-8'),object_pairs_hook=pairs,parse_constant=nonfinite)
    except (UnicodeError,json.JSONDecodeError,RecursionError) as exc:raise ValueError('invalid bounded UTF8 JSON') from exc

def safe_path(value,regular_input=False):
    if not isinstance(value,(str,Path)) or not str(value) or '\x00' in str(value):raise ValueError('plain local path required')
    text=str(value);normalized=text.replace('/',chr(92))
    if normalized.startswith(chr(92)*2) or normalized.startswith(chr(92)+'??'+chr(92)) or normalized.upper().startswith(('\\DEVICE\\','\\DOSDEVICES\\','\\GLOBALROOT\\')):raise ValueError('UNC/device namespace rejected before resolve/read')
    reserved={'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(1,10)),*(f'LPT{i}' for i in range(1,10))}
    win=PureWindowsPath(normalized)
    for part in win.parts:
        if part in (win.anchor,win.drive,chr(92),'.','..'):continue
        if ':' in part or part.rstrip(' .').split('.')[0].rstrip(' ').upper() in reserved:raise ValueError('device/ADS component rejected')
    path=Path(value).resolve()
    if regular_input and (not path.is_file() or path.is_symlink()):raise ValueError('regular local input required')
    return path

def fresh_output(value):
    path=safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/vdp_word_streams')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path

def read_bounded(value,maximum):
    path=safe_path(value,True)
    if path.stat().st_size>maximum:raise ValueError('file input exceeds bound')
    with path.open('rb') as stream:data=stream.read(maximum+1)
    if len(data)>maximum:raise ValueError('input grew beyond bound')
    return data

def put(path,data):
    with path.open('xb') as stream:stream.write(data)

def schema():
    integer=lambda maximum:dict(type='integer',minimum=0,maximum=maximum)
    def object_schema(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def constant(value):
        if type(value) is dict:return object_schema({key:constant(item) for key,item in value.items()})
        if type(value) is list:return dict(type='array',prefixItems=[constant(item) for item in value],items=False,minItems=len(value),maxItems=len(value))
        return dict(type={bool:'boolean',int:'integer',str:'string'}[type(value)],const=value)
    literal=object_schema(dict(op=dict(type='string',const='literal'),word=integer(65535)))
    repeat=object_schema(dict(op=dict(type='string',const='repeat'),word=integer(65535),count=dict(type='integer',minimum=2,maximum=256)))
    stream=object_schema(dict(marker=integer(255),commands=dict(type='array',maxItems=MAX_PACKAGE_WORDS,items=dict(oneOf=[literal,repeat]))))
    fixed=metadata();properties={key:constant(value) for key,value in fixed.items()};block_schemas=[]
    for start,end in ALLOCATIONS:
        row={key:constant(value) for key,value in topology(start,end).items()};row['fields']=stream;block_schemas.append(object_schema(row))
    properties['blocks']=dict(type='array',prefixItems=block_schemas,items=False,minItems=20,maxItems=20)
    result=object_schema(properties);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='Candidate only. Runtime validator additionally enforces encoded slot costs, literal marker constraint, exact dataset WORDs and terrain dependency.'
    return result

def render_bundle(rom):
    fields=extract(rom);encoded_fields=dump(fields);schema_bytes=dump(schema());rows=projection(fields)
    image=import_fields(rom,load_json(encoded_fields))
    if image!=rom:raise ValueError('entire-ROM serialized export/import not exact')
    report=dict(format=FORMAT,confidence='candidate',whole_ROM_exact=image==rom,whole_ROM_sha256=sha(image),
        directory_slots=80,distinct_physical_blocks=20,nonempty_physical_blocks=19,
        physical_stream_emit_bytes=104621,terrain_reused_bytes=2,empty_prefix_retained_bytes=1,
        unknown_leading_byte=0xD4D41,decoded_dataset_WORDs=4096,decoded_extent_is_package_contract_not_hardware_limit=True,
        blocks=rows,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        independent_CPU_comparison=False,promotion=True)
    report_bytes=dump(report)
    members={'fields.json':encoded_fields,'fields.schema.json':schema_bytes,'validation.json':report_bytes}
    manifest=dict(format=FORMAT,confidence='candidate',canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA),
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},
        physical_owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        repeated_physical_contents_retained=['rom_0E71C2_vdpword','rom_0EA36C_vdpword'],
        terrain_reuse=reuse(),independent_CPU_comparison=False,promotion=True)
    members['manifest.json']=dump(manifest)
    return members

def export_bundle(rom_path,output):
    target=fresh_output(output) # fail closed BEFORE input resolution/read
    rom=read_bounded(rom_path,ROM_SIZE);bundle=render_bundle(rom)
    target.mkdir()
    for name,data in bundle.items():put(target/name,data)
    return dict(path=str(target),members={name:sha(data) for name,data in bundle.items()},owner_bytes_added=0)

def import_file(rom_path,fields_path,output,terrain_path=None):
    target=fresh_output(output) # fail closed BEFORE input resolution/read
    if target.suffix.lower()!='.bin':raise ValueError('fresh .bin output required')
    rom=read_bounded(rom_path,ROM_SIZE);fields=load_json(read_bounded(fields_path,MAX_JSON))
    terrain=None if terrain_path is None else read_bounded(terrain_path,2)
    image=import_fields(rom,fields,terrain);put(target,image)
    return dict(path=str(target),bytes=len(image),sha256=sha(image),owner_bytes_added=0)

def verify_bundle(rom_path,bundle_path):
    target=safe_path(bundle_path)
    if not target.is_dir():raise ValueError('bundle directory required')
    expected=render_bundle(read_bounded(rom_path,ROM_SIZE))
    if {path.name for path in target.iterdir()}!=set(expected):raise ValueError('bundle member drift')
    for name,data in expected.items():
        if read_bounded(target/name,MAX_JSON)!=data:raise ValueError('canonical bundle drift: '+name)
    return dict(path=str(target),verified_candidate_bundle=True,independent_CPU_comparison=False,promotion=True)

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--output');parser.add_argument('--fields');parser.add_argument('--bundle');parser.add_argument('--terrain')
    args=parser.parse_args(argv)
    if args.command=='export':
        if args.output is None or any(value is not None for value in (args.fields,args.bundle,args.terrain)):raise ValueError('export requires output only')
        result=export_bundle(args.rom,args.output)
    elif args.command=='import':
        if args.output is None or args.fields is None or args.bundle is not None:raise ValueError('import requires fields/fresh output')
        result=import_file(args.rom,args.fields,args.output,args.terrain)
    else:
        if args.bundle is None or any(value is not None for value in (args.output,args.fields,args.terrain)):raise ValueError('verify requires bundle only')
        result=verify_bundle(args.rom,args.bundle)
    print(json.dumps(result,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
