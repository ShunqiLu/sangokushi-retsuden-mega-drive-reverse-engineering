"""Original four-BYTE sprite records and their two-level BE32 directories.

03A5A0 and 03A7A2 step four bytes, stop when source byte0 equals80, copy byte1
to the SAT size byte and combine its high nibble with caller D2/D3/D4 for the
attribute WORD. Source byte0/3 become signed deltas for SAT WORD0/3. This codec
preserves source fields, not a claim about all resulting SAT/RAM states. The
unread byte after each80 terminator stays unknown and is NOT emitted.
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
DEFAULT_FIELDS=ROOT/'analysis/compact_sprite_records/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/compact_sprite_records'
START,END=0x357F8,0x387BA
DIRS=(('primary_selector',0x38C28,0x38CC8,'secondary'),
      ('primary_sprite_pointers',0x38CC8,0x38D94,'descriptor'),
      ('secondary_selector',0x38D94,0x38E34,'secondary'),
      ('secondary_sprite_pointers',0x38E34,0x38E50,'descriptor'))
EDITABLE_BYTES=12685
FORMAT='candidate-compact-four-byte-sprite-records-v1'
sha=f.sha;dump=f.dump;uint=f.uint;keys=f.keys

def ident(start):return f'rom_{start:06X}_compact_sprite'
def pointer_id(start):return f'rom_{start:06X}_sprite_pointer_slot'
def metadata():return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
    confidence='candidate',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def exact_list(value,count,label):
    if type(value) is not list or len(value)!=count:raise ValueError(label+': physical count differs')
    return value
def signed(value,minimum,maximum,label):
    if type(value) is not int or not minimum<=value<=maximum:raise ValueError(label+': strict signed integer outside source range')
    return value

def layout(rom):
    f.verify_rom(rom);rows=[];p=START
    while p<END:
        start=p;count=0
        while p<END and rom[p]!=128:
            p+=4;count+=1
            if count>127:raise ValueError('bounded original descriptor allocation differs')
        if p>=END or count==0:raise ValueError('original descriptor lacks terminal byte')
        rows.append(dict(start=start,end=p+1,count=count));p+=2
    if p!=END or len(rows)!=93 or sum(row['count'] for row in rows)!=3010:raise ValueError('original93 descriptor partition differs')
    starts={row['start'] for row in rows}
    secondary={p for _,start,end,kind in DIRS if kind=='descriptor' for p in range(start,end,4)}
    for _,start,end,kind in DIRS:
        valid=secondary if kind=='secondary' else starts
        if any(int.from_bytes(rom[p:p+4],'big') not in valid for p in range(start,end,4)):
            raise ValueError('original two-level directory target differs')
    return rows

def record(raw):
    if type(raw) is not bytes or len(raw)!=4 or raw[0]==128:raise ValueError('complete nonterminal four-BYTE record required')
    return dict(sat_y_delta=raw[0] if raw[0]<128 else raw[0]-256,
                sat_x_delta=raw[3] if raw[3]<128 else raw[3]-256,
                width_tiles=((raw[1]>>2)&3)+1,height_tiles=(raw[1]&3)+1,
                attribute_nibble=raw[1]>>4,tile_low_byte=raw[2])
def record_bytes(row):
    keys(row,{'sat_y_delta','sat_x_delta','width_tiles','height_tiles','attribute_nibble','tile_low_byte'},'record')
    y=signed(row['sat_y_delta'],-127,127,'SAT y source delta');x=signed(row['sat_x_delta'],-128,127,'SAT x source delta')
    width=uint(row['width_tiles'],4,'width tiles');height=uint(row['height_tiles'],4,'height tiles')
    if width<1 or height<1:raise ValueError('positive source size required')
    attribute=uint(row['attribute_nibble'],15,'source attribute nibble');tile=uint(row['tile_low_byte'],255,'source tile BYTE')
    return bytes((y&255,(attribute<<4)|((width-1)<<2)|(height-1),tile,x&255))

def source_attribute_word(row,d2,d3,d4):
    """Narrow03A870..03A884 field transform; not the surrounding SAT writer."""
    record_bytes(row);uint(d2,65535,'D2.W');uint(d3,65535,'D3.W');uint(d4,65535,'D4.W')
    lane=(((row['attribute_nibble']<<4)+(d3&255))&255)^(d2&0xFFF8)
    return ((((lane<<7)&65535)|row['tile_low_byte'])+d4)&65535

def extract(rom):
    rows=layout(rom);result=metadata();result['descriptors']=[]
    for row in rows:
        result['descriptors'].append(dict(id=ident(row['start']),start=row['start'],end=row['end'],terminator_byte=128,
            records=[record(rom[p:p+4]) for p in range(row['start'],row['end']-1,4)]))
    result['directories']=[]
    for name,start,end,kind in DIRS:
        result['directories'].append(dict(id=name,start=start,end=end,target_kind=kind,
            targets=[(pointer_id if kind=='secondary' else ident)(int.from_bytes(rom[p:p+4],'big')) for p in range(start,end,4)]))
    blocks(rom,result);return result

def blocks(rom,fields):
    rows=layout(rom);keys(fields,set(metadata())|{'descriptors','directories'},'package')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    catalog={ident(row['start']):row['start'] for row in rows}
    pointers={pointer_id(p):p for _,start,end,kind in DIRS if kind=='descriptor' for p in range(start,end,4)}
    result=[]
    for descriptor,row in zip(exact_list(fields['descriptors'],93,'descriptors'),rows):
        fixed=dict(id=ident(row['start']),start=row['start'],end=row['end'],terminator_byte=128)
        keys(descriptor,set(fixed)|{'records'},'descriptor')
        for key,value in fixed.items():f.same(descriptor[key],value,'descriptor.'+key)
        data=b''.join(record_bytes(record) for record in exact_list(descriptor['records'],row['count'],'records'))+b'\x80'
        if len(data)!=row['end']-row['start']:raise ValueError('fixed descriptor extent differs')
        result.append(dict(id=descriptor['id'],start=row['start'],end=row['end'],data=data,role='candidate_compact_sprite_records'))
    for directory,(name,start,end,kind) in zip(exact_list(fields['directories'],4,'directories'),DIRS):
        fixed=dict(id=name,start=start,end=end,target_kind=kind);keys(directory,set(fixed)|{'targets'},'directory')
        for key,value in fixed.items():f.same(directory[key],value,'directory.'+key)
        valid=pointers if kind=='secondary' else catalog;targets=exact_list(directory['targets'],(end-start)//4,'targets')
        if any(type(target) is not str or target not in valid for target in targets):raise ValueError('directory target outside existing source catalog')
        data=b''.join(valid[target].to_bytes(4,'big') for target in targets)
        result.append(dict(id=name,start=start,end=end,data=data,role='candidate_compact_sprite_pointer_directory'))
    result.sort(key=lambda row:row['start'])
    if sum(len(row['data']) for row in result)!=EDITABLE_BYTES or any(a['end']>b['start'] for a,b in zip(result,result[1:])):
        raise ValueError('nonoverlapping physical source scope differs')
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
    def number(low,high):return dict(type='integer',minimum=low,maximum=high)
    source_record=obj(dict(sat_y_delta=number(-127,127),sat_x_delta=number(-128,127),width_tiles=number(1,4),height_tiles=number(1,4),
                           attribute_nibble=number(0,15),tile_low_byte=number(0,255)))
    properties={key:fixed(value) for key,value in metadata().items()}
    properties['descriptors']=dict(type='array',minItems=93,maxItems=93,items=obj(dict(id=dict(type='string'),start=number(0,f.ROM_SIZE),
        end=number(0,f.ROM_SIZE),terminator_byte=fixed(128),records=dict(type='array',minItems=1,maxItems=127,items=source_record))))
    properties['directories']=dict(type='array',minItems=4,maxItems=4,items=obj(dict(id=dict(type='string'),start=number(0,f.ROM_SIZE),end=number(0,f.ROM_SIZE),
        target_kind=dict(enum=['secondary','descriptor']),targets=dict(type='array',minItems=1,maxItems=51,items=dict(type='string')))))
    result=obj(properties);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='Runtime checks exact source identities and capacities. Editor domains are not CPU selector/SAT clamps.'
    return result

def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('whole-ROM source-field roundtrip differs')
    rows=layout(rom)
    report=dict(confidence='confirmed_source_fields_candidate_visual_roles',editable_bytes=EDITABLE_BYTES,physical_blocks=97,
        descriptors=93,records=3010,descriptor_bytes=12133,directory_bytes=552,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        consumers=dict(primary_directory=0x398A0,secondary_directory=0x398EA,clipped_writer=0x3A5A0,unclipped_writer=0x3A7A2,
                       record_step=[0x3A704,0x3A88A],terminator_check=[0x3A600,0x3A7FC]),
        source_regions=[dict(start=row['start'],end=row['end'],records=row['count'],sha256=sha(rom[row['start']:row['end']])) for row in rows],
        unknown_unread_bytes=[[row['end'],row['end']+1] for row in rows],reused_old_authority_excluded=[0x387BA,0x388FA],
        natural_selector_domain_complete=False,independent_CPU_comparison=False,source_field_editing_not_full_SAT_or_RAM_proof=True,
        unknowns=['93 physical descriptors/40 selector slots are not natural frame/character bounds.',
                  'Attribute nibble is combined with surviving caller values; not an absolute final palette/flip label.',
                  'Clipping, prior SAT linkage, sprite counter and gameplay lifetimes are not newly validated.'],
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(format=FORMAT,confidence='candidate',editable_bytes=EDITABLE_BYTES,
        canonical_source=metadata()['canonical_source'],members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0))
    return members
def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/compact_sprite_records')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output')
    args=p.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output) # BEFORE any input read
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
        result=dict(path=None if target is None else str(target),sha256=sha(image),exact_canonical=image==rom,editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
