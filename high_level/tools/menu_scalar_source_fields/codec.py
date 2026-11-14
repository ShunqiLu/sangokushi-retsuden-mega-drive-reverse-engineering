"""Five original read-defined allocations, 224 bytes, with bounded projections."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
import json
from tools.direct_code import direct_code as d
from tools.ui_layouts import ui_layouts as grammar

f, ROOT = d.f, d.ROOT
FORMAL_ROOT = ROOT / 'analysis/menu_scalar_source_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/menu_scalar_source_fields'
FORMAT = 'g5510-menu-scalar-source-fields-v1'
EDITABLE_BYTES = 224
SPECS = (
    (0x62D2,0x62FA,'BE16_KEY_VALUE',10,(0x62B6,0x62C2)),
    (0x11842,0x11874,'BYTE_FACTOR_BIAS',25,(0x1182E,0x1183A)),
    (0x1AE6E,0x1AEA0,'BYTE_FACTOR_BIAS',25,(0x1AE5A,0x1AE66)),
    (0x20532,0x2055A,'COUNTED_REPEAT_WORD',10,(0x26C10,0x26C5E)),
    (0x39964,0x39990,'BE32_SOURCE_ADDRESS',11,(0x39950,)),
)
GUARDS = (
    (0x62A2,0x62D2,reference_value(__name__, 'GUARDS')),
    (0x117F0,0x11842,reference_value(__name__, 'GUARDS_2')),
    (0x1AE1C,0x1AE6E,reference_value(__name__, 'GUARDS_3')),
    (0x204EC,0x20532,reference_value(__name__, 'GUARDS_4')),
    (0x26BFA,0x26C8E,reference_value(__name__, 'GUARDS_5')),
    (0x3991C,0x39964,reference_value(__name__, 'GUARDS_6')),
    (0x62FA,0x6308,reference_value(__name__, 'GUARDS_7')),
    (0x11874,0x11882,reference_value(__name__, 'GUARDS_8')),
    (0x1AEA0,0x1AEAC,reference_value(__name__, 'GUARDS_9')),
    (0x2055A,0x20566,reference_value(__name__, 'GUARDS_10')),
)
sha, dump, load_fields = f.sha, f.dump, f.load_json


def metadata():
    return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
                confidence='confirmed_original_reads_probable_menu_scalar_roles',
                owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)


def topology(spec):
    a,z,kind,count,pcs=spec
    return dict(id=f'rom_{a:06X}_{kind}',start=a,end=z,kind=kind,physical_elements=count,
                original_read_PCs=list(pcs),editor_count_is_CPU_clamp=False,
                framing_control_fixed=kind=='COUNTED_REPEAT_WORD')


def verify_rom(rom):
    if type(rom)is not bytes:raise ValueError('immutable canonical ROM bytes required')
    f.verify_rom(rom)
    for a,z,h in GUARDS:
        if sha(rom[a:z])!=h:raise ValueError('original read/producer/boundary differs')
    for pc,target in ((0x62B2,0x62D2),(0x11828,0x11842),(0x1AE54,0x1AE6E),
                      (0x20506,0x20532),(0x3994A,0x39964)):
        if rom[pc:pc+2] not in (b'\x41\xfa',b'\x43\xfa') or pc+2+int.from_bytes(rom[pc+2:pc+4],'big',signed=True)!=target:
            raise ValueError('original PC-relative LEA base differs')
    if rom[0x11822:0x11824]!=b'\x96\x04' or rom[0x1AE4E:0x1AE50]!=b'\x96\x41':
        raise ValueError('distinct SUB.B/SUB.W producers differ')
    if rom[0x20518:0x2051E]!=bytes.fromhex('4eb900026bfa'):
        raise ValueError('original true reader JSR differs')


def row_view(image):
    view=grammar.walk_rows(image,0x20532,6,10,command_budget=40)
    if view['status']!='complete' or view['end']!=0x2055A or view['output_words']!=60:
        raise ValueError('ten six-cell rows must consume exactly40 bytes')
    if len(view['commands'])!=10 or any(x['kind']!='word_command' or x['operation']!='repeat' or x['control_word']!=0x8006 for x in view['commands']):
        raise ValueError('fixed original repeat framing differs')
    return view


def extract(rom):
    verify_rom(rom);row_view(rom);sources=[]
    for spec in SPECS:
        a,z,kind,_,_=spec;values=[]
        for p in range(a,z,2 if kind=='BYTE_FACTOR_BIAS' else 4):
            if kind=='BE16_KEY_VALUE':values.append(dict(key_WORD=int.from_bytes(rom[p:p+2],'big'),value_WORD=int.from_bytes(rom[p+2:p+4],'big')))
            elif kind=='BYTE_FACTOR_BIAS':values.append(dict(factor_BYTE=rom[p],bias_BYTE=rom[p+1]))
            elif kind=='COUNTED_REPEAT_WORD':values.append(dict(control_WORD=0x8006,payload_WORD=int.from_bytes(rom[p+2:p+4],'big')))
            else:values.append(int.from_bytes(rom[p:p+4],'big'))
        sources.append(dict(**topology(spec),values=values))
    return dict(**metadata(),sources=sources)


def fixed(value,expected,mutable,label):
    f.keys(value,set(expected)|set(mutable),label)
    for key,item in expected.items():f.same(value[key],item,label+'.'+key)


def exact(value,count,label):
    if type(value)is not list or len(value)!=count:raise ValueError(label+': fixed physical allocation differs')
    return value


def blocks(rom,fields):
    verify_rom(rom);fixed(fields,metadata(),{'sources'},'source package');out=[]
    for source,spec in zip(exact(fields['sources'],5,'sources'),SPECS):
        top=topology(spec);fixed(source,top,{'values'},'source');data=bytearray()
        for value in exact(source['values'],top['physical_elements'],'physical elements'):
            kind=spec[2]
            if kind=='BE32_SOURCE_ADDRESS':data.extend(f.uint(value,0xFFFFFFFF,'full source LONG').to_bytes(4,'big'))
            else:
                keys=('key_WORD','value_WORD') if kind=='BE16_KEY_VALUE' else ('factor_BYTE','bias_BYTE') if kind=='BYTE_FACTOR_BIAS' else ('control_WORD','payload_WORD')
                f.keys(value,set(keys),'source record')
                for key in keys:
                    width=1 if kind=='BYTE_FACTOR_BIAS' else 2
                    word=f.uint(value[key],(1<<(width*8))-1,'full original '+key)
                    if key=='control_WORD' and word!=0x8006:raise ValueError('fixed count/dispatch control8006 differs')
                    data.extend(word.to_bytes(width,'big'))
        if len(data)!=spec[1]-spec[0]:raise ValueError('physical allocation cost differs')
        out.append(dict(id=top['id'],start=spec[0],end=spec[1],data=bytes(data),role=spec[2]))
    if sum(len(x['data']) for x in out)!=224:raise ValueError('224-byte source union differs')
    return out


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def flags():
    return dict(CPU_executed=False,hardware_executed=False,true_call_RTS_executed=False,
                independent_CPU_comparison=False,complete_entry=False,natural_domain_complete=False)


def s16(value):return value-65536 if value&32768 else value


def read(image,logical,size,pc):
    logical&=0xFFFFFFFF;address=logical&0xFFFFFF
    event=dict(kind='source_read_projection',pc=pc,logical_address=logical,address=address,size=size)
    if (size>1 and address&1) or address+size>len(image):
        return dict(**event,fault='address_error' if size>1 and address&1 else 'unmapped_source')
    return dict(**event,value=int.from_bytes(image[address:address+size],'big'))


def budget(value):
    f.uint(value,65536,'projection budget')
    if value==0:raise ValueError('positive projection budget required')
    return value


def key_lookup_preview(rom,fields,query_WORD,active_WORD=1,*,query_reads_WORDs=None,read_budget=32):
    """Original ordered key reads. Missing key is not a ten-element terminator."""
    f.uint(query_WORD,65535,'F38C entry WORD');f.uint(active_WORD,65535,'F36C WORD');budget(read_budget)
    if query_reads_WORDs is not None:
        if type(query_reads_WORDs)is not list or len(query_reads_WORDs)>65536:raise ValueError('explicit live query prefix required')
        for word in query_reads_WORDs:f.uint(word,65535,'live F38C comparison WORD')
    image=rebuild(rom,fields);events=[];address=0x62D2
    if query_WORD!=0x81 and active_WORD==0:return dict(**flags(),status='original_BEQ62CA_skip',events=events)
    for step in range(read_budget):
        key=read(image,address,2,0x62B6);events.append(key);address=(address+2)&0xFFFFFFFF
        if 'fault'in key:return dict(**flags(),status='source_read_boundary',events=events)
        if query_reads_WORDs is not None and step>=len(query_reads_WORDs):
            return dict(**flags(),status='supplied_live_query_prefix_boundary',events=events)
        query=query_WORD if query_reads_WORDs is None else query_reads_WORDs[step]
        events.append(dict(kind='supplied_RAM_WORD_read_projection',pc=0x62B8,logical_address=0xFFFFF38C,address=0xFFF38C,size=2,value=query))
        if key['value']==query:
            value=read(image,address,2,0x62C2);events.append(value);address=(address+2)&0xFFFFFFFF
            return dict(**flags(),status='source_read_boundary' if 'fault'in value else 'original_JSR676F2_boundary',events=events,
                        final_A0_LONG=address,selected_value_WORD=value.get('value'),helper_executed=False)
        address=(address+2)&0xFFFFFFFF  # ADDQ.W #2,An changes full address register.
    return dict(**flags(),status='projection_budget_boundary',events=events,final_A0_LONG=address)


def factor_bias_preview(rom,fields,source,own_class_BYTE,other_class_BYTE,seed_WORD):
    """Supplied live C700 class bytes/F61C seed; original RNG is not re-executed."""
    if type(source)is not str or source not in ('11842','1AE6E'):raise ValueError('explicit original factor reader required')
    f.uint(own_class_BYTE,255,'own class BYTE');f.uint(other_class_BYTE,255,'other class BYTE');f.uint(seed_WORD,65535,'F61C seed WORD')
    image=rebuild(rom,fields);own=(4-(own_class_BYTE&7))&65535
    other=(4-(other_class_BYTE&7))&(255 if source=='11842' else 65535)
    index=((((own<<2)&65535)+own+other)&65535)<<1&65535
    base,pc=(0x11842,0x1182E) if source=='11842' else (0x1AE6E,0x1AE5A)
    logical=(base+s16(index))&0xFFFFFFFF
    factor=read(image,logical,1,pc);events=[factor]
    if 'fault'in factor:return dict(**flags(),status='source_read_boundary',events=events,index_WORD=index)
    product=factor['value']*seed_WORD
    bias=read(image,logical+1,1,pc+12);events.append(bias)
    if 'fault'in bias:return dict(**flags(),status='source_read_boundary',events=events,index_WORD=index)
    low=((product>>16)+bias['value'])&65535
    return dict(**flags(),status='factor_bias_projected',events=events,index_WORD=index,
                other_subtract_width='BYTE' if source=='11842' else 'WORD',product_LONG=product,
                resulting_D1_WORD=low,resulting_D1_LONG=((product&65535)<<16)|low,
                RNG_executed=False,own_source_RAM=0xF3A6 if source=='11842' else 0xF3F2,
                other_source_RAM=0xF3F2 if source=='11842' else 0xF3A6)


def counted_rows_preview(rom,fields):
    image=rebuild(rom,fields);view=row_view(image);events=[]
    for command in view['commands']:
        events.append(read(image,command['start'],2,0x26C10))
        events.append(read(image,command['start']+2,2,0x26C5E))
    return dict(**flags(),status='ten_six_cell_rows_projected',events=events,
                source_end=view['end'],source_bytes=40,output_words=60,
                row_payload_WORDs=[x['operand_word'] for x in view['commands']],
                projected_row_WORDs=[[x['operand_word']|0xC000]*6 for x in view['commands']],queue_writes_executed=False)


def pointer_sequence_preview(rom,fields,distance_WORD,clock_WORD,counter_before_WORD,*,counter_at_load_WORD=None,follow_target=True):
    """EQ40 precedes ADDQ4; later counter read is independently live."""
    for label,value in (('D1 distance',distance_WORD),('F320 clock',clock_WORD),('FF703C first counter',counter_before_WORD)):
        f.uint(value,65535,label+' WORD')
    if counter_at_load_WORD is not None:f.uint(counter_at_load_WORD,65535,'FF703C later counter WORD')
    if type(follow_target)is not bool:raise ValueError('explicit follow-target bool required')
    image=rebuild(rom,fields);events=[]
    if distance_WORD<3:return dict(**flags(),status='original_BCS39960_skip',events=events)
    advances=(clock_WORD&7)==0
    if advances and counter_before_WORD==0x28:return dict(**flags(),status='original_EQ40_skip',events=events)
    index=((counter_before_WORD+4)&65535) if advances else counter_before_WORD
    if counter_at_load_WORD is not None:index=counter_at_load_WORD
    pointer=read(image,0x39964+s16(index),4,0x39950);events.append(pointer)
    if 'fault'in pointer:return dict(**flags(),status='source_read_boundary',events=events,index_WORD=index)
    status='pointer_projected';copied=[]
    if follow_target:
        status='eight_LONG_source_copy_projected'
        for step in range(8):
            item=read(image,pointer['value']+4*step,4,0x3995A);events.append(item)
            if 'fault'in item:status='source_read_boundary';break
            copied.append(item['value']);destination=(0xFFFFFB00+4*step)&0xFFFFFFFF
            events.append(dict(kind='RAM_LONG_write_projection',pc=0x3995A,logical_address=destination,address=destination&0xFFFFFF,size=4,value=item['value']))
    return dict(**flags(),status=status,events=events,index_WORD=index,counter_incremented=advances,
                loaded_source_LONG=pointer['value'],copied_LONGs=copied,target_followed=follow_target)


def raw_guard(base):
    raw=d.raw_positions(base);positions={p for a,z,_,_,_ in SPECS for p in range(a,z)}
    if not positions<=raw:raise ValueError('all224 positions require sole existing raw authority')
    return dict(guarded_raw_bytes=len(positions),layout_remaining_raw=len(raw),
                excluded_unknown_tail_bytes=4,excluded_tail_raw_bytes=len(set(range(0x39990,0x39994))&raw))


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('whole-ROM serialized roundtrip differs')
    views=[key_lookup_preview(rom,fields,x['key_WORD']) for x in fields['sources'][0]['values']]
    views += [factor_bias_preview(rom,fields,source,own,other,0xFFFF) for source in ('11842','1AE6E') for own in range(5) for other in range(5)]
    views += [counted_rows_preview(rom,fields)]
    views += [pointer_sequence_preview(rom,fields,3,1,i*4,follow_target=False) for i in range(11)]
    positions={p for a,z,_,_,_ in SPECS for p in range(a,z)}
    union={p for view in views for e in view['events'] if e['kind']=='source_read_projection' and 'fault'not in e for p in range(e['address'],e['address']+e['size'])}&positions
    if union!=positions:raise ValueError('constructed original read-address union differs from224')
    report=dict(**metadata(),editable_bytes=224,mutable_value_bytes=204,fixed_framing_bytes=20,physical_blocks=5,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),constructed_read_projections=len(views),constructed_source_union_bytes=len(union),**flags(),
        source_guards=[dict(start=a,end=z,sha256=h,physical_emit=False) for a,z,h in GUARDS],
        source_consumption=[dict(start=a,end=z,bytes=z-a,kind=kind) for a,z,kind,_,_ in SPECS],
        excluded_unknown_tail=dict(start=0x39990,end=0x39994,bytes=4,confidence='unknown',physical_emit=False),
        original_JSRs=[dict(pc=pc,target=target,executed=False,physical_emit=False) for pc,target in ((0x62C4,0x676F2),(0x117F0,0x83D4),(0x1AE1C,0x83D4),(0x20518,0x26BFA))],
        limitations=['Read-address/value projections do not execute a CPU, true stack/RTS, RNG, shared RAM lifetime or hardware.',
            'All mutable WORD/BYTE/LONG payload bits are retained. Ten row controls8006 are original fixed grammar.',
            'Physical counts10/25/11 are editor allocations, not CPU selector clamps or terminators.',
            'Missing lookup keys continue beyond the physical ten pairs; budgets explicitly stop only this preview.',
            'The factor readers differ at SUB.B versus SUB.W and have reversed own/other RAM origins.',
            'The pointer EQ40-before-increment guard does not prove arbitrary live counter domains; later reads can alias.',
            '039990..039994 remains unknown and is never emitted even when counterfactual preview reads it.',
            'Existing RNG/UI helpers and source targets are reused without duplicated physical emission.'])
    members={'fields.json':dump(fields),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=224,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value):
    path=f.safe_path(value)
    if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh formal directory or dedicated build/menu_scalar_source_fields required')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(f.DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output')
    args=p.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output)
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
    elif args.output is not None:raise ValueError('verify does not write')
    rom=f.read_bounded(args.rom,f.ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():f.put(target/name,data)
        result=dict(path=str(target),editable_bytes=224,members={name:sha(data) for name,data in members.items()})
    else:
        image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
