"""Typed272-byte render-source batch; original EA widths, not CPU execution."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
import json
from tools.direct_code import direct_code as d

f, ROOT = d.f, d.ROOT
FORMAL_ROOT = ROOT / 'analysis/render_selector_source_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/render_selector_source_fields'
FORMAT = 'g5510-render-selector-source-fields-v1'
EDITABLE_BYTES = 272
# Each physical role is explicit. No byte blob or inferred alignment is emitted.
SPECS = (
    (0x30456, 0x3045C, 'XY_BYTES', (0x302E4,)),
    (0x3045C, 0x30462, 'XY_BYTES', (0x30314,)),
    (0x30462, 0x30466, 'XY_BYTES', (0x30344,)),
    (0x30466, 0x3046C, 'XY_BYTES', (0x30374,)),
    (0x3046C, 0x3047C, 'BE16_Y_PARAMETER', (0x303B0, 0x3048A)),
    (0x3047C, 0x30484, 'BE16_X_PARAMETER', (0x306D8,)),
    (0x307E0, 0x307E4, 'BYTE_MODE_PARAMETER', (0x30784,)),
    (0x307E4, 0x3080E, 'BE16_CONFIGURATION_WORD', (0x307D6,)),
    (0x39CB8, 0x39CC8, 'BE32_SOURCE_ADDRESS', (0x39C64,)),
    (0x39CC8, 0x39CD8, 'BE32_SOURCE_ADDRESS', (0x39C96,)),
    (0x39CD8, 0x39CEC, 'BYTE_SELECTOR', (0x39C5A,)),
    (0x3A06A, 0x3A07A, 'BE32_SOURCE_ADDRESS', (0x3A096,)),
    (0x3A07A, 0x3A08A, 'BE32_SOURCE_ADDRESS', (0x3A0DE,)),
    (0x3A0E4, 0x3A114, 'BYTE_CYCLE_RESET', (0x3A0C4,)),
    (0x6749A, 0x674AA, 'BE32_FILL_PATTERN', (0x67494,)),
    (0x674AA, 0x674CA, 'MONO_ROW_BITS', (0xAF06,)),
)
GUARDS = (
    (0x39B10,0x39B1C,reference_value(__name__, 'GUARDS')),
    (0x39C4C,0x39CB8,reference_value(__name__, 'GUARDS_2')),
    (0x3A08A,0x3A0E4,reference_value(__name__, 'GUARDS_3')),
    (0x3A114,0x3A11C,reference_value(__name__, 'GUARDS_4')),
    (0x67216,0x67220,reference_value(__name__, 'GUARDS_5')),
    (0x673A6,0x6746A,reference_value(__name__, 'GUARDS_6')),
    (0x6746A,0x6747E,reference_value(__name__, 'GUARDS_7')),
    (0x6748E,0x6749A,reference_value(__name__, 'GUARDS_8')),
    (0xAF04,0xAF1E,reference_value(__name__, 'GUARDS_9')),
    (0x302AC,0x302C2,reference_value(__name__, 'GUARDS_10')),
    (0x302D6,0x30380,reference_value(__name__, 'GUARDS_11')),
    (0x303A2,0x303BE,reference_value(__name__, 'GUARDS_12')),
    (0x30484,0x3049C,reference_value(__name__, 'GUARDS_13')),
    (0x306CC,0x306EE,reference_value(__name__, 'GUARDS_14')),
    (0x3076E,0x307E0,reference_value(__name__, 'GUARDS_15')),
    (0x3080E,0x30818,reference_value(__name__, 'GUARDS_16')),
)
sha, dump, load_fields = f.sha, f.dump, f.load_json


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=f.ROM_SIZE, sha256=f.ROM_SHA),
                confidence='confirmed_original_read_types_probable_render_selector_roles',
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def topology(spec):
    a,z,kind,pcs=spec
    width = 4 if kind.startswith('BE32') else 1 if kind.startswith('BYTE') else 2
    return dict(id=f'rom_{a:06X}_{kind}', start=a, end=z, kind=kind,
                element_bytes=width, physical_elements=(z-a)//width,
                original_read_PCs=list(pcs), editor_count_is_CPU_clamp=False,
                framing_marker_fixed=kind=='BYTE_CYCLE_RESET')


def verify_rom(rom):
    if type(rom) is not bytes:
        raise ValueError('immutable original ROM bytes required')
    f.verify_rom(rom)
    for a,z,h in GUARDS:
        if sha(rom[a:z])!=h:
            raise ValueError('original consumer/producer/boundary differs')
    for pc,target in ((0x39C54,0x39CD8),(0x3A0BE,0x3A0E4),(0x67216,0x674AA),
                      (0x302DE,0x30456),(0x3030E,0x3045C),(0x3033E,0x30462),
                      (0x3036E,0x30466),(0x303AA,0x3046C),(0x306D4,0x3047C),(0x307B6,0x307E4)):
        if pc+2+int.from_bytes(rom[pc+2:pc+4],'big',signed=True)!=target:
            raise ValueError('original LEA displacement differs')
    for pc,target in ((0x39C64,0x39CB8),(0x39C96,0x39CC8),(0x3A096,0x3A06A),
                      (0x3A0DE,0x3A07A),(0x67494,0x6749A),(0x30784,0x307E0)):
        if pc+2+int.from_bytes(rom[pc+3:pc+4],'big',signed=True)!=target:
            raise ValueError('original brief indexed PC source differs')


def extract(rom):
    verify_rom(rom)
    sources=[]
    for spec in SPECS:
        top=topology(spec);a,z=spec[:2];width=top['element_bytes']
        values=[dict(X_BYTE=rom[p],Y_BYTE=rom[p+1]) if spec[2]=='XY_BYTES'
                else int.from_bytes(rom[p:p+width],'big') for p in range(a,z,width)]
        sources.append(dict(**top, values=values))
    return dict(**metadata(), sources=sources)


def fixed(value, expected, mutable, label):
    f.keys(value,set(expected)|set(mutable),label)
    for key,item in expected.items():
        f.same(value[key],item,label+'.'+key)


def exact_list(value,count,label):
    if type(value)is not list or len(value)!=count:
        raise ValueError(label+': fixed physical allocation differs')
    return value


def blocks(rom,fields):
    verify_rom(rom);fixed(fields,metadata(),{'sources'},'render-source package')
    result=[]
    for source,spec in zip(exact_list(fields['sources'],len(SPECS),'sources'),SPECS):
        top=topology(spec);fixed(source,top,{'values'},'source');width=top['element_bytes']
        values=exact_list(source['values'],top['physical_elements'],'physical elements')
        data=bytearray()
        for value in values:
            if spec[2]=='XY_BYTES':
                f.keys(value,{'X_BYTE','Y_BYTE'},'packed coordinate')
                data.extend((f.uint(value['X_BYTE'],255,'X BYTE'),f.uint(value['Y_BYTE'],255,'Y BYTE')))
            else:
                data.extend(f.uint(value,(1<<(8*width))-1,'full original scalar field').to_bytes(width,'big'))
        if spec[2]=='BYTE_CYCLE_RESET' and values[-1]!=255:
            raise ValueError('fixed last FF reset framing marker differs')
        result.append(dict(id=top['id'],start=spec[0],end=spec[1],data=bytes(data),role=spec[2]))
    if sum(len(x['data']) for x in result)!=EDITABLE_BYTES:
        raise ValueError('272-byte physical cost differs')
    return result


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def s16(word):return word-65536 if word&32768 else word


def read(image,logical,size,pc):
    logical&=0xFFFFFFFF;address=logical&0xFFFFFF
    event=dict(kind='source_read_projection',pc=pc,logical_address=logical,address=address,size=size)
    if (size>1 and address&1) or address+size>len(image):
        return dict(**event,fault='address_error' if address&1 else 'unmapped_source')
    return dict(**event,value=int.from_bytes(image[address:address+size],'big'))


def flags():
    return dict(CPU_executed=False,hardware_executed=False,true_call_RTS_executed=False,
                independent_CPU_comparison=False,complete_entry=False,natural_domain_complete=False)


def scene_choice_preview(rom,fields,phase_WORD):
    f.uint(phase_WORD,65535,'FF7026 WORD at39B10');image=rebuild(rom,fields)
    if phase_WORD>19:
        return dict(**flags(),status='original_BHI_handoff_39CF0',events=[])
    select=read(image,0x39CD8+s16(phase_WORD),1,0x39C5A);events=[select]
    index=(select['value']<<2)&65535
    for base,pc in ((0x39CB8,0x39C64),(0x39CC8,0x39C96)):
        if pc==0x39C96 and phase_WORD==12:continue  # real BEQ39CB4 skips second render
        item=read(image,base+s16(index),4,pc);events.append(item)
        if 'fault'in item:return dict(**flags(),status='source_read_boundary',events=events)
    return dict(**flags(),status='source_pointers_projected',events=events,index_WORD=index,target_followed=False)


def frame_directory_preview(rom,fields,directory,offset_WORD):
    f.uint(offset_WORD,65535,'D1 WORD byte offset')
    if type(directory)is not str or directory not in ('first','second'):
        raise ValueError('explicit original directory required')
    base,pc=(0x3A06A,0x3A096) if directory=='first' else (0x3A07A,0x3A0DE)
    item=read(rebuild(rom,fields),base+s16(offset_WORD),4,pc)
    return dict(**flags(),status='source_read_boundary' if 'fault'in item else 'pointer_projected',
                events=[item],target_followed=False,host_scaling_applied=False)


def frame_cycle_preview(rom,fields,cursor_first_WORD,clock_WORD,*,cursor_after_increment_WORD=None):
    f.uint(cursor_first_WORD,65535,'FF703C first read');f.uint(clock_WORD,65535,'D0 WORD atANDI7')
    image=rebuild(rom,fields);increment=(clock_WORD&7)==0
    if not increment and cursor_after_increment_WORD is not None:
        raise ValueError('original branch has no second cursor read')
    index=cursor_first_WORD
    if increment:
        index=(cursor_first_WORD+1)&65535 if cursor_after_increment_WORD is None else f.uint(cursor_after_increment_WORD,65535,'second live cursor read')
    command=read(image,0x3A0E4+s16(index),1,0x3A0C4);events=[command]
    reset=command['value']==255;offset=0 if reset else command['value']&15
    pointer=read(image,0x3A07A+s16(offset),4,0x3A0DE);events.append(pointer)
    return dict(**flags(),status='source_read_boundary' if 'fault'in pointer else 'cycle_pointer_projected',
                cursor_incremented=increment,source_index_WORD=index,reset_on_FF=reset,
                resulting_cursor_WORD=0 if reset else index,D1_WORD_byte_offset=offset,
                events=events,target_followed=False)


def coordinate_preview(rom,fields,group,selector_WORD):
    f.uint(group,3,'original coordinate reader group');f.uint(selector_WORD,65535,'original selector WORD')
    base,pc=((0x30456,0x302E4),(0x3045C,0x30314),(0x30462,0x30344),(0x30466,0x30374))[group]
    item=read(rebuild(rom,fields),base+s16((selector_WORD<<1)&65535),2,pc)
    if 'fault'in item:return dict(**flags(),status='source_read_boundary',events=[item])
    # Original ASR.W8 then ANDI.WFF; low BYTE is Y, without signed-coordinate normalization.
    return dict(**flags(),status='packed_XY_projected',events=[item],X_WORD=item['value']>>8,Y_WORD=item['value']&255)


def parameter_preview(rom,fields,axis,selector_WORD):
    f.uint(selector_WORD,65535,'original selector WORD')
    if type(axis)is not str or axis not in ('X','Y'):
        raise ValueError('original parameter reader required')
    base,pc=(0x3047C,0x306D8) if axis=='X' else (0x3046C,0x3048A)
    item=read(rebuild(rom,fields),base+s16((selector_WORD<<1)&65535),2,pc)
    return dict(**flags(),status='parameter_WORD_projected' if 'fault'not in item else 'source_read_boundary',events=[item])


def monochrome_preview(rom,fields,scheme_WORD):
    f.uint(scheme_WORD,65535,'F6C4 WORD');image=rebuild(rom,fields);index=s16((scheme_WORD<<2)&65535)
    events=[read(image,0x6747E+index,2,0x67476),read(image,0x67480+index,2,0x67476),read(image,0x6749A+index,4,0x67494)]
    if any('fault'in e for e in events):return dict(**flags(),status='source_read_boundary',events=events)
    colors=[events[0]['value']&255,events[1]['value']&255];rows=[];pixels=[]
    for row in range(16):
        longs=[];bits=[]
        for half in range(2):
            item=read(image,0x674AA+2*row+half,1,0xAF06);events.append(item);value=0
            for shift in range(7,-1,-1):
                bit=(item['value']>>shift)&1;bits.append(bit)
                value=((value<<4)|colors[bit])&0xFFFFFFFF  # true OR.B accepts full BYTE, not a fake nibble clamp
            longs.append(value)
        rows.append(longs);pixels.append(bits)
    return dict(**flags(),status='sixteen_1bpp_rows_projected',events=events,
                fill_pattern_LONG=events[2]['value'],row_LONGs=rows,pixels=pixels,
                old_color_table_reused=True,new_color_table_emit_bytes=0)


def configuration_preview(rom,fields,mode_first_WORD,source_index_WORDs,count_WORD,*,mode_add_WORDs=None,read_budget=64):
    f.uint(mode_first_WORD,65535,'EFD4 first read');f.uint(count_WORD,65535,'original DBRA D0 WORD')
    f.uint(read_budget,65536,'projection read budget')
    if read_budget==0:raise ValueError('positive budget required')
    if type(source_index_WORDs)is not list or len(source_index_WORDs)>65536:
        raise ValueError('supplied queue WORD prefix required')
    for word in source_index_WORDs:f.uint(word,65535,'queue index WORD')
    adds=[mode_first_WORD,mode_first_WORD] if mode_add_WORDs is None else exact_list(mode_add_WORDs,2,'two live EFD4 ADD reads')
    for value in adds:f.uint(value,65535,'live EFD4 ADD WORD')
    index=(mode_first_WORD<<1)&65535
    for value in adds:index=((((index+value)&65535)<<1)&65535)
    source_base=(0x307E4+s16(index))&0xFFFFFFFF
    image=rebuild(rom,fields);events=[];values=[];needed=count_WORD+1
    status='DBRA_copy_projected'
    for step in range(needed):
        if step>=read_budget:status='instruction_budget_boundary';break
        if step>=len(source_index_WORDs):status='supplied_queue_prefix_boundary';break
        queue_logical=(0xFF702C+2*step)&0xFFFFFFFF;destination=(0xFFFFF67A+2*step)&0xFFFFFFFF
        if not 0xFF0000<=queue_logical&0xFFFFFF<=0xFFFFFE or not 0xFF0000<=destination&0xFFFFFF<=0xFFFFFE:
            status='RAM_address_boundary';break
        word=source_index_WORDs[step]
        events.append(dict(kind='supplied_RAM_WORD_read_projection',pc=0x307D2,logical_address=queue_logical,address=queue_logical&0xFFFFFF,size=2,value=word))
        source=read(image,source_base+s16((word<<1)&65535),2,0x307D6);events.append(source)
        if 'fault'in source:status='source_read_boundary';break
        events.append(dict(kind='RAM_WORD_write_projection',pc=0x307D6,logical_address=destination,address=destination&0xFFFFFF,size=2,value=source['value']))
        values.append(source['value'])
    return dict(**flags(),status=status,events=events,copied_WORDs=values,
                mode_index_WORD=index,source_base_logical=source_base,
                requested_original_DBRA_iterations=needed,final_D0_WORD=(count_WORD-len(values))&65535)


def mode_preview(rom,fields,selector_WORD):
    f.uint(selector_WORD,65535,'FF7026 WORD at30784')
    item=read(rebuild(rom,fields),0x307E0+s16(selector_WORD),1,0x30784)
    return dict(**flags(),status='mode_BYTE_projected',events=[item])


def raw_guard(base):
    raw=d.raw_positions(base);positions={p for a,z,_,_ in SPECS for p in range(a,z)}
    if not positions<=raw:raise ValueError('all272 positions must remain sole raw authority')
    return dict(guarded_raw_bytes=len(positions),layout_remaining_raw=len(raw),
                excluded_unknown_tail_bytes=4,excluded_tail_raw_bytes=len(set(range(0x39CEC,0x39CF0))&raw))


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('whole-ROM serialized roundtrip differs')
    views=[scene_choice_preview(rom,fields,i) for i in range(20)]
    views += [frame_directory_preview(rom,fields,which,i*4) for which in ('first','second') for i in range(4)]
    views += [frame_cycle_preview(rom,fields,i,1) for i in range(48)]
    views += [coordinate_preview(rom,fields,g,i) for g,n in enumerate((3,3,2,3)) for i in range(n)]
    views += [parameter_preview(rom,fields,axis,i) for axis,n in (('Y',8),('X',4)) for i in range(n)]
    views += [monochrome_preview(rom,fields,i) for i in range(4)]
    views += [configuration_preview(rom,fields,i,list(range(7)),6) for i in range(3)]
    views += [mode_preview(rom,fields,i) for i in range(4)]
    positions={p for a,z,_,_ in SPECS for p in range(a,z)}
    union={p for view in views for e in view['events'] if e['kind']=='source_read_projection' and 'fault'not in e
           for p in range(e['address'],e['address']+e['size'])}&positions
    if union!=positions:raise ValueError('constructed original read projection union differs from272')
    report=dict(**metadata(),editable_bytes=272,physical_blocks=len(SPECS),whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),constructed_read_projections=len(views),
        constructed_source_union_bytes=len(union),**flags(),
        source_guards=[dict(start=a,end=z,sha256=h,physical_emit=False) for a,z,h in GUARDS],
        excluded_unknown_tail=dict(start=0x39CEC,end=0x39CF0,bytes=4,physical_emit=False,confidence='unknown'),
        fixed_framing_marker=dict(address=0x3A113,value=255,role='FF_reset_marker'),
        live_configuration_selector_reads=3,stable_configuration_stride_bytes=14,
        limitations=['Constructed address/value projections are not actual CPU/stack/VDP execution.',
            'Physical catalogs do not clamp full WORD selectors, count, offsets or pointer values.',
            '39B10 unsigned19 guard is real; unknown4 tail bytes are not padding or fields.',
            'Cycle has fixed lastFF framing marker; earlier editableFF can cause earlier original reset.',
            '3A directories use D1.W byte offsets without host multiplication.',
            'Configuration uses three independent live EFD4 reads; default stable example is not lifetime proof.',
            'Existing6747E color words and originalAF04 code are reused, never re-emitted.',
            'FFFF parameter words retain all bits and are not invented editor/CPU terminators.'])
    members={'fields.json':dump(fields),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=272,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value):
    path=f.safe_path(value)
    if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('fresh formal directory or dedicated build/render_selector_source_fields required')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'));parser.add_argument('--rom',default=str(f.DEFAULT_ROM))
    parser.add_argument('--fields',default=str(DEFAULT_FIELDS));parser.add_argument('--output')
    args=parser.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output)
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
    elif args.output is not None:raise ValueError('verify does not write')
    rom=f.read_bounded(args.rom,f.ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():f.put(target/name,data)
        result=dict(path=str(target),editable_bytes=272,members={name:sha(data) for name,data in members.items()})
    else:
        image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
