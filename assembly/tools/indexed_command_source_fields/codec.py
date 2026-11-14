"""274 editable original bytes in command-offset and parameter WORD sources."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
import json
from tools.direct_code import direct_code as d

f, ROOT = d.f, d.ROOT
EDITABLE_BYTES = 274
FORMAL_ROOT = ROOT/'analysis/indexed_command_source_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT/'fields.json'
OUTPUT_ROOT = ROOT/'build/indexed_command_source_fields'
FORMAT = 'g5510-indexed-command-source-WORDs-v1'
# start,end,readPC,JSRPC,RAM selector fetchPC,WORD address,BMI thenSUBQ1.
DISPATCH = (
    (0x31006,0x3100C,0x30FCE,0x30FD2,0x30FC8,0xF726,False),
    (0x312D8,0x312F8,0x312CE,0x312D2,0x312C8,0xF362,False),
    (0x3155C,0x31562,0x31552,0x31556,0x3154C,0xF710,False),
    (0x31A24,0x31A42,0x31A18,0x31A1C,0x31A0C,0xF728,True),
    (0x32582,0x32592,0x32576,0x3257A,0x3256A,0xF728,True),
    (0x33058,0x3306E,0x3304C,0x33050,0x33040,0xF728,True),
    (0x338DA,0x338EC,0x338CE,0x338D2,0x338C2,0xF728,True),
    (0x34110,0x34140,0x34104,0x34108,0x340F8,0xF728,True),
    (0x34F7C,0x34F94,0x34F70,0x34F74,0x34F64,0xF728,True),
)
PARAMETERS = (
    (0x3B788,0x3B794,'parameter_WORDs',0x3B758),
    (0x3FCC4,0x3FCE0,'paired_parameter_WORDs',0x3FCBA),
    (0x415E8,0x41608,'paired_parameter_WORDs',0x415B0),
)
SPECS = tuple((row[0],row[1],'conditional_call_offset_WORDs',row[2]) for row in DISPATCH)+PARAMETERS
GUARDS = (
    (0x30FC8,0x31006,reference_value(__name__, 'GUARDS')),
    (0x312C8,0x312D8,reference_value(__name__, 'GUARDS_2')),
    (0x3154C,0x3155C,reference_value(__name__, 'GUARDS_3')),
    (0x31A0C,0x31A24,reference_value(__name__, 'GUARDS_4')),
    (0x3256A,0x32582,reference_value(__name__, 'GUARDS_5')),
    (0x33040,0x33058,reference_value(__name__, 'GUARDS_6')),
    (0x338C2,0x338DA,reference_value(__name__, 'GUARDS_7')),
    (0x340F8,0x34110,reference_value(__name__, 'GUARDS_8')),
    (0x34F64,0x34F7C,reference_value(__name__, 'GUARDS_9')),
    (0x3B752,0x3B762,reference_value(__name__, 'GUARDS_10')),
    (0x3FC96,0x3FCC4,reference_value(__name__, 'GUARDS_11')),
    (0x415A2,0x415E2,reference_value(__name__, 'GUARDS_12')),
    (0x41608,0x41636,reference_value(__name__, 'GUARDS_13')),
)
sha, dump, load_fields = f.sha, f.dump, f.load_json


def metadata():
    return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
                source_consumption_confidence='confirmed_original_indexed_WORD_reads',
                owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
                executable_code_added=0,recovered_functions_added=0)


def ident(start):return f'rom_{start:06X}_indexed_WORD_source'


def topology(spec):
    start,end,role,pc=spec
    return dict(id=ident(start),start=start,end=end,element_BYTES=2,encoding='BE16',
                physical_WORDs=(end-start)//2,role=role,original_read_PC=pc,
                physical_slot_count_is_CPU_clamp=False)


def signed_WORD(value):return value-65536 if value&0x8000 else value


def indexed_base(rom,pc):
    return (pc+2+int.from_bytes(rom[pc+3:pc+4],'big',signed=True))&0xFFFFFFFF


def verify_rom(rom):
    if type(rom)is not bytes:raise ValueError('immutable canonical ROM bytes required')
    f.verify_rom(rom)
    for start,end,digest in GUARDS:
        if sha(rom[start:end])!=digest:raise ValueError('complete original read/producer prefix differs')
    for start,end,read,call,*_ in DISPATCH:
        if rom[read:read+3]!=bytes.fromhex('303b00') or indexed_base(rom,read)!=start:
            raise ValueError('original PC-indexed WORD read encoding differs')
        if rom[call:call+3]!=bytes.fromhex('4ebb00') or indexed_base(rom,call)!=end:
            raise ValueError('original PC-indexed JSR base differs')
    for read,start in ((0x3B758,0x3B788),(0x3FCBA,0x3FCC4),(0x3FCBE,0x3FCC6),
                       (0x415B0,0x415E8),(0x415B4,0x415EA),(0x41616,0x415E8),(0x4161A,0x415EA)):
        if indexed_base(rom,read)!=start:raise ValueError('original parameter read base differs')


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),sources=[dict(**topology(spec),values=[int.from_bytes(rom[p:p+2],'big')
        for p in range(spec[0],spec[1],2)]) for spec in SPECS])


def fixed(value,expected,mutable,label):
    f.keys(value,set(expected)|set(mutable),label)
    for key,item in expected.items():f.same(value[key],item,label+'.'+key)


def blocks(rom,fields):
    verify_rom(rom);fixed(fields,metadata(),{'sources'},'indexed source package')
    sources=fields['sources']
    if type(sources)is not list or len(sources)!=len(SPECS):raise ValueError('fixed twelve source allocations required')
    result=[]
    for row,spec in zip(sources,SPECS):
        fixed(row,topology(spec),{'values'},'WORD source');values=row['values']
        if type(values)is not list or len(values)!=(spec[1]-spec[0])//2:raise ValueError('fixed physical WORD count differs')
        result.append(dict(id=row['id'],start=spec[0],end=spec[1],role=spec[2],
            data=b''.join(f.uint(value,65535,'full source WORD').to_bytes(2,'big') for value in values)))
    return sorted(result,key=lambda row:row['start'])


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def flags():
    return dict(CPU_executed=False,hardware_executed=False,true_call_RTS_executed=False,
                callback_executed=False,independent_CPU_comparison=False,
                complete_entry=False,natural_domain_complete=False)


def event(kind,pc,logical,size,value):
    return dict(kind=kind,pc=pc,logical_address=logical&0xFFFFFFFF,address=logical&0xFFFFFF,size=size,value=value)


def take(image,pc,logical,events):
    address=logical&0xFFFFFF
    if logical&1:raise ValueError('odd source WORD read')
    if address+2>len(image):return None
    value=int.from_bytes(image[address:address+2],'big')
    events.append(event('source_read_projection',pc,logical,2,value));return value


def dispatch_preview(rom,fields,source_start,selector_WORD):
    """One supplied live WORD fetch through the original indexedJSR boundary."""
    f.uint(source_start,f.ROM_SIZE-1,'physical dispatch source');f.uint(selector_WORD,65535,'live selector WORD')
    matches=[spec for spec in DISPATCH if spec[0]==source_start]
    if len(matches)!=1:raise ValueError('one original dispatch source required')
    start,end,read,call,fetch,ram,subtract_one=matches[0];image=rebuild(rom,fields)
    events=[event('supplied_RAM_read_projection',fetch,0xFFFF0000|ram,2,selector_WORD)]
    if subtract_one and selector_WORD&0x8000:
        return dict(**flags(),status='original_BMI_return_boundary',events=events,source_read_performed=False)
    value=(selector_WORD-1)&65535 if subtract_one else selector_WORD
    offset=(value<<1)&65535;logical=(start+signed_WORD(offset))&0xFFFFFFFF
    relative=take(image,read,logical,events)
    if relative is None:return dict(**flags(),status='unmapped_source_read_boundary',events=events,source_LONG=logical,index_WORD=offset)
    target=(end+signed_WORD(relative))&0xFFFFFFFF
    return dict(**flags(),status='original_indexed_JSR_not_executed_boundary',events=events,
                source_LONG=logical,index_WORD=offset,relative_WORD=relative,
                signed_relative=signed_WORD(relative),target_LONG=target,target_bus_address=target&0xFFFFFF,
                target_is_odd=bool(target&1),JSR_PC=call,original_JSR_PC_base=end,
                source_catalog_alias=not(start<=logical<end))


def parameter_preview(rom,fields,selector_WORD):
    """3B752 supplied80DA.W -> ASL.W1 -> fullWORD -> unexecuted808A."""
    f.uint(selector_WORD,65535,'80DA selector WORD');image=rebuild(rom,fields)
    events=[event('supplied_RAM_read_projection',0x3B752,0xFFFF80DA,2,selector_WORD)]
    offset=(selector_WORD<<1)&65535;logical=(0x3B788+signed_WORD(offset))&0xFFFFFFFF
    value=take(image,0x3B758,logical,events)
    return dict(**flags(),status='808A_JSR_not_executed_boundary' if value is not None else 'unmapped_source_read_boundary',
                events=events,index_WORD=offset,source_LONG=logical,parameter_WORD=value,
                original_JSR_PC=0x3B75C,original_target_LONG=0x808A,parameter_not_pointer=True,
                source_catalog_alias=not(0x3B788<=logical<0x3B794))


def paired_preview(rom,fields,source_start,selector_WORD,*,second_reader=False):
    """ASL.W2 then two independent PC-indexed WORD reads; +2 is after sign EA."""
    f.uint(source_start,f.ROM_SIZE-1,'physical paired source');f.uint(selector_WORD,65535,'supplied D2 WORD')
    if type(second_reader)is not bool:raise ValueError('exact bool reader selector required')
    if source_start==0x3FCC4:
        if second_reader:raise ValueError('single original3FCB8 reader')
        first,second,fetch=0x3FCBA,0x3FCBE,None
    elif source_start==0x415E8:first,second,fetch=(0x41616,0x4161A,0x41610) if second_reader else (0x415B0,0x415B4,0x415AA)
    else:raise ValueError('one original paired source required')
    image=rebuild(rom,fields);events=[]
    if fetch is not None:events.append(event('supplied_RAM_read_projection',fetch,0xFFFF8158,2,selector_WORD))
    offset=(selector_WORD<<2)&65535;ea=signed_WORD(offset)
    logical=(source_start+ea)&0xFFFFFFFF;value0=take(image,first,logical,events)
    if value0 is None:return dict(**flags(),status='unmapped_first_read_boundary',events=events,index_WORD=offset)
    logical1=(source_start+2+ea)&0xFFFFFFFF;value1=take(image,second,logical1,events)
    return dict(**flags(),status='later_consumer_not_executed_boundary' if value1 is not None else 'unmapped_second_read_boundary',
                events=events,index_WORD=offset,signed_index=ea,parameter_WORDs=[value0,value1],
                source_LONGs=[logical,logical1],source_catalog_alias=not(source_start<=logical<source_start+(28 if source_start==0x3FCC4 else 32)))


def raw_guard(base):
    raw=d.raw_positions(base);positions={p for a,z,*_ in SPECS for p in range(a,z)}
    if not positions<=raw:raise ValueError('all274 source positions require sole existing raw authority')
    return dict(guarded_raw_bytes=len(positions),layout_remaining_raw=len(raw))


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('serialized whole-ROM roundtrip differs')
    views=[];dispatch_catalogs=[]
    for start,end,*rest in DISPATCH:
        subtract_one=rest[-1];local=[dispatch_preview(rom,fields,start,index+int(subtract_one)) for index in range((end-start)//2)]
        views.extend(local);dispatch_catalogs.append(dict(start=start,end=end,physical_slots=len(local),
            encoded_conditional_target_LONGs=[row['target_LONG'] for row in local],natural_domain_complete=False))
    views.extend(parameter_preview(rom,fields,index) for index in range(6))
    views.extend(paired_preview(rom,fields,0x3FCC4,index) for index in range(7))
    views.extend(paired_preview(rom,fields,0x415E8,index) for index in range(8))
    second=[paired_preview(rom,fields,0x415E8,index,second_reader=True) for index in range(8)];views.extend(second)
    union={p for view in views for e in view['events'] if e['kind']=='source_read_projection' for p in range(e['address'],e['address']+e['size'])}
    expected={p for a,z,*_ in SPECS for p in range(a,z)}
    if union!=expected:raise ValueError('constructed original source-read union differs from274')
    report=dict(**metadata(),editable_bytes=274,physical_blocks=len(SPECS),dispatch_offset_bytes=202,
        parameter_WORD_bytes=12,paired_parameter_WORD_bytes=60,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        constructed_projections=len(views),constructed_source_read_union_bytes=len(union),**flags(),
        source_guards=[dict(start=a,end=z,sha256=h,physical_emit=False) for a,z,h in GUARDS],
        conditional_dispatch_catalogs=dispatch_catalogs,constructed_read_projections=views,
        unknown_business_meanings=['Command business labels are not guessed; encoded call offsets and RAM selector sources are confirmed.',
            '3B788 is a scalar passed to808A, not a pointer table. Paired render/position roles are probable.'],
        limitations=['This is a lossless source editor and local read/EA projection, not full CPU, stack, callback or hardware execution.',
            'Six F728-based loops test the original WORD sign before SUBQ1 and LSL1. Zero is not rejected; it reads prior code.',
            'Other dispatch sources use live F726/F362/F710 WORDs without new physical-slot clamps.',
            'All offsets and parameter WORDs remain fullbits. Shift wraps inWORD before sign extension; JSR uses the fetched signedWORD.',
            'Paired parameters use two original PC-relative bases; second read is base+2 after signed EA, not a second masked selector.',
            'Catalog counts follow exact raw allocations and original next-source boundaries, not proven natural domains.',
            'Alias diagnostics read the entire serialized edited image; no neighboring typed bytes or raw gaps are emitted.',
            '05CE22..05D5E4 remains unknown. Existing44B2 caller reads32WORDs with rowcount1 only to05CE22.'])
    members={'fields.json':dump(fields),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=274,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value):
    path=f.safe_path(value)
    if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh formal directory or dedicated indexed-source build output required')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(f.DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output')
    args=p.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output)
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh.bin required')
    elif args.output is not None:raise ValueError('verify does not write')
    rom=f.read_bounded(args.rom,f.ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():f.put(target/name,data)
        result=dict(path=str(target),editable_bytes=274,members={name:sha(data) for name,data in members.items()})
    else:
        image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
