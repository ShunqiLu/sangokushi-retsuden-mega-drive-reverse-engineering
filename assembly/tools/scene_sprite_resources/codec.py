"""Source fields for sprite-scene parameters, palette staging and one WORD row.

The catalog contains40 physical slots, not a natural scene/selector clamp.
03983C..039850 reads signed-positive frame bytes or a negative control plus
reset BYTE. Resets may cross a local animation allocation; original42 is kept.
Only first-control framing is emitted, leaving six unread tails unknown. The
three unreferenced palette banks are excluded. 0044B2 -> 03AAB6 uploads exactly
32 BE16 WORDs from05CDE2, with row-count1, not an inferred entire nearby asset.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.vdp_word_streams import format as f
from tools.graphics_build import graphics_build as gb
DEFAULT_ROM=f.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/scene_sprite_resources/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/scene_sprite_resources'
FORMAT='candidate-sprite-scene-source-fields-v1'
EDITABLE_BYTES=2832
PAL_UNKNOWN=(0x38F18,0x39198,0x391B8)
PAL_STARTS=tuple(p for p in range(0x38E78,0x39658,32) if p not in PAL_UNKNOWN)
ANIM_STARTS=(0x38AB2,0x38AC8,0x38ACC,0x38AF0,0x38AF8,0x38B00,0x38B42,0x38B4C,0x38B68,0x38B6C)
PARAMS=(('dual_stream_flags',0x3899A,1),('duration_words',0x389C2,2),
        ('initial_d1_words',0x38B88,2),('initial_d2_words',0x38BD8,2),('motion_controls',0x38E50,1))
sha=f.sha;dump=f.dump;uint=f.uint;keys=f.keys

def ident(start,kind):return f'rom_{start:06X}_{kind}'
def metadata():return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
    confidence='candidate',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def exact_list(value,count,label):
    if type(value) is not list or len(value)!=count:raise ValueError(label+': physical count differs')
    return value
def colour(word):return dict(red=(word>>1)&7,green=(word>>5)&7,blue=(word>>9)&7,reserved=word&0xF111)
def colour_word(row):
    keys(row,{'red','green','blue','reserved'},'colour');reserved=uint(row['reserved'],65535,'reserved WORD bits')
    if reserved&~0xF111:raise ValueError('reserved bits overlap accepted colour channel encoding')
    return reserved|(uint(row['red'],7,'red')<<1)|(uint(row['green'],7,'green')<<5)|(uint(row['blue'],7,'blue')<<9)
def motion(byte):return dict(speed=byte&15,subtract_d0=(byte>>4)&1,add_d0=(byte>>5)&1,subtract_d1=(byte>>6)&1,add_d1=(byte>>7)&1)
def motion_byte(row):
    keys(row,{'speed','subtract_d0','add_d0','subtract_d1','add_d1'},'motion control')
    return uint(row['speed'],15,'speed')|sum(uint(row[key],1,key)<<bit for key,bit in
        (('subtract_d0',4),('add_d0',5),('subtract_d1',6),('add_d1',7)))
def animation_layout(rom):
    f.verify_rom(rom);rows=[]
    for start,end in zip(ANIM_STARTS,ANIM_STARTS[1:]+(0x38B88,)):
        marker=next((p for p in range(start,end) if rom[p]>=128),None)
        if marker is None or marker+2>end:raise ValueError('original signed-control framing differs')
        rows.append(dict(start=start,end=marker+2,allocation_end=end,frames=marker-start))
    if sum(row['end']-row['start'] for row in rows)!=208:raise ValueError('original208 animation source bytes differ')
    return rows

def extract(rom):
    rows=animation_layout(rom);result=metadata()
    result['palettes']=[dict(id=ident(p,'palette'),start=p,colours=[colour(int.from_bytes(rom[q:q+2],'big')) for q in range(p,p+32,2)]) for p in PAL_STARTS]
    result['palette_directory']=[ident(int.from_bytes(rom[p:p+4],'big'),'palette') for p in range(0x388FA,0x3899A,4)]
    result['animation_directory']=[ident(int.from_bytes(rom[p:p+4],'big'),'animation') for p in range(0x38A12,0x38AB2,4)]
    result['animations']=[dict(id=ident(row['start'],'animation'),start=row['start'],end=row['end'],
        frames=list(rom[row['start']:row['end']-2]),negative_control=rom[row['end']-2],reset_byte=rom[row['end']-1]) for row in rows]
    result['parameters']={name:([motion(v) for v in rom[start:start+40]] if name=='motion_controls' else
        [int.from_bytes(rom[p:p+width],'big') for p in range(start,start+40*width,width)]) for name,start,width in PARAMS}
    result['WORD_row']=[gb.cell(int.from_bytes(rom[p:p+2],'big')) for p in range(0x5CDE2,0x5CE22,2)]
    blocks(rom,result);return result

def blocks(rom,fields):
    rows=animation_layout(rom);keys(fields,set(metadata())|{'palettes','palette_directory','animation_directory','animations','parameters','WORD_row'},'package')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    result=[]
    def add(name,start,data,role):result.append(dict(id=name,start=start,end=start+len(data),data=data,role=role))
    for row,start in zip(exact_list(fields['palettes'],60,'palettes'),PAL_STARTS):
        keys(row,{'id','start','colours'},'palette');f.same(row['id'],ident(start,'palette'),'palette id');f.same(row['start'],start,'palette start')
        add(row['id'],start,b''.join(colour_word(col).to_bytes(2,'big') for col in exact_list(row['colours'],16,'colours')),'candidate_palette_staging_WORDs')
    for field,start,catalog in (('palette_directory',0x388FA,{ident(p,'palette'):p for p in PAL_STARTS}),
                                ('animation_directory',0x38A12,{ident(p,'animation'):p for p in ANIM_STARTS})):
        targets=exact_list(fields[field],40,field)
        if any(type(target) is not str or target not in catalog for target in targets):raise ValueError(field+': target outside original physical catalog')
        add(field,start,b''.join(catalog[target].to_bytes(4,'big') for target in targets),'candidate_scene_pointer_directory')
    for row,layout in zip(exact_list(fields['animations'],10,'animations'),rows):
        fixed=dict(id=ident(layout['start'],'animation'),start=layout['start'],end=layout['end'])
        keys(row,set(fixed)|{'frames','negative_control','reset_byte'},'animation')
        for key,value in fixed.items():f.same(row[key],value,'animation.'+key)
        frames=bytes(uint(value,127,'positive frame BYTE') for value in exact_list(row['frames'],layout['frames'],'frames'))
        control=uint(row['negative_control'],255,'negative control BYTE')
        if control<128:raise ValueError('signed-negative control required')
        add(row['id'],layout['start'],frames+bytes((control,uint(row['reset_byte'],255,'reset BYTE'))),'candidate_signed_frame_reset_stream')
    keys(fields['parameters'],{name for name,_,_ in PARAMS},'parameters')
    for name,start,width in PARAMS:
        values=exact_list(fields['parameters'][name],40,name)
        if name=='motion_controls':data=bytes(motion_byte(row) for row in values)
        else:data=b''.join(uint(value,(1<<(8*width))-1,name).to_bytes(width,'big') for value in values)
        add(name,start,data,'candidate_scene_'+name)
    add('raw_WORD_row',0x5CDE2,b''.join(gb.cell_word(row).to_bytes(2,'big') for row in exact_list(fields['WORD_row'],32,'WORD row')),'candidate_single_uploaded_WORD_row')
    result.sort(key=lambda row:row['start'])
    if sum(len(row['data']) for row in result)!=EDITABLE_BYTES or any(a['end']>b['start'] for a,b in zip(result,result[1:])):
        raise ValueError('nonoverlapping physical scope differs')
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
    def array(n,item):return dict(type='array',minItems=n,maxItems=n,items=item)
    colour_schema=obj(dict(red=number(0,7),green=number(0,7),blue=number(0,7),reserved=number(0,65535)))
    motion_schema=obj(dict(speed=number(0,15),**{name:number(0,1) for name in ('subtract_d0','add_d0','subtract_d1','add_d1')}))
    properties={key:fixed(value) for key,value in metadata().items()}
    properties['palettes']=array(60,obj(dict(id=dict(type='string'),start=number(0,f.ROM_SIZE),colours=array(16,colour_schema))))
    properties['palette_directory']=array(40,dict(type='string',enum=[ident(p,'palette') for p in PAL_STARTS]))
    properties['animation_directory']=array(40,dict(type='string',enum=[ident(p,'animation') for p in ANIM_STARTS]))
    properties['animations']=array(10,obj(dict(id=dict(type='string'),start=number(0,f.ROM_SIZE),end=number(0,f.ROM_SIZE),
        frames=dict(type='array',maxItems=63,items=number(0,127)),negative_control=number(128,255),reset_byte=number(0,255))))
    properties['parameters']=obj({name:array(40,motion_schema if name=='motion_controls' else number(0,(1<<(8*width))-1)) for name,_,width in PARAMS})
    properties['WORD_row']=array(32,obj(dict(tile=number(0,2047),hflip=number(0,1),vflip=number(0,1),palette=number(0,3),priority=number(0,1))))
    result=obj(properties);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='Runtime adds fixed-address/cost and reserved-bit checks. Physical catalog is not a CPU bound.'
    return result
def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('whole-ROM source-field roundtrip differs')
    rows=animation_layout(rom)
    report=dict(confidence='confirmed_source_encoding_candidate_visual_roles',editable_bytes=EDITABLE_BYTES,physical_blocks=78,
        palettes=60,palette_bytes=1920,animation_source_bytes=208,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        consumers=dict(palette_directory=0x397AA,palette_copy=0x397B8,palette_cycle_copies=[0x3987E,0x399A0,0x399C2],
                       flag=0x3977C,duration=0x397EC,animation_lookup=0x3982E,animation_read=0x3983C,animation_reset=0x39848,
                       initial_coordinates=[0x39722,0x39726],motion=0x39740,motion_handler=0x399D8,
                       WORD_row_source=0x44B2,WORD_row_call=0x44C8,WORD_row_reader=0x3AAB6),
        unknown_unreferenced_palettes=[[p,p+32] for p in PAL_UNKNOWN],
        unknown_animation_tails=[[row['end'],row['allocation_end']] for row in rows if row['end']<row['allocation_end']],
        original_cross_allocation_reset=dict(source=0x38B00,reset_byte=66,next_address=0x38B42),
        original_WORD_row=dict(start=0x5CDE2,end=0x5CE22,source_WORDs=32,row_count=1,purpose='candidate'),
        sole_authority_exclusions=['vdp_word_streams 0387BA..0388FA','compact_sprite_records descriptors and038C28..038E50'],
        reused_implementation=['graphics_build.cell','graphics_build.cell_word','accepted CRAM F111 reserved-bit convention'],
        natural_selector_domain_complete=False,independent_CPU_comparison=False,port_timing_proven=False,
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(format=FORMAT,confidence='candidate',editable_bytes=EDITABLE_BYTES,
        canonical_source=metadata()['canonical_source'],members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0))
    return members
def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/scene_sprite_resources')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output')
    args=p.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output) # output authority BEFORE reads
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
