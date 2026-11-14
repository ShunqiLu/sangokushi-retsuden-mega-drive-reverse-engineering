"""142 lossless original source bytes, with separate boot/queue/dispatch roles."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
import json
from tools.direct_code import direct_code as d

f, ROOT = d.f, d.ROOT
EDITABLE_BYTES = 142
FORMAL_ROOT = ROOT/'analysis/boot_queue_dispatch_source_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT/'fields.json'
OUTPUT_ROOT = ROOT/'build/boot_queue_dispatch_source_fields'
FORMAT = 'g5510-boot-queue-dispatch-source-scalars-v1'
# Allocation sizes follow actual original read loops, not a global CPU domain.
SPECS = (
    (0x68A8,0x68CE,2,'boot_VDP_control_WORDs',0x6838),
    (0x4378,0x43A0,2,'queue_ten_pairs_WORDs',0x43D0),
    (0x43A0,0x43BC,2,'queue_seven_pairs_WORDs',0x4320),
    (0x27B96,0x27BA2,2,'comparison_threshold_WORDs',0x28F96),
    (0x27BA2,0x27BBA,4,'conditional_call_target_LONGs',0x27B78),
)
GUARDS = (
    (0x6826,0x68A8,reference_value(__name__, 'GUARDS')),
    (0x430E,0x4336,reference_value(__name__, 'GUARDS_2')),
    (0x43BC,0x4400,reference_value(__name__, 'GUARDS_3')),
    (0x27B58,0x27B96,reference_value(__name__, 'GUARDS_4')),
    (0x28F90,0x28F9C,reference_value(__name__, 'GUARDS_5')),
)
sha, dump, load_fields = f.sha, f.dump, f.load_json


def metadata():
    return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
                source_consumption_confidence='confirmed_original_instruction_reads',
                owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
                executable_code_added=0,recovered_functions_added=0)


def topology(spec):
    start,end,width,role,pc=spec
    return dict(id=f'rom_{start:06X}_{role}',start=start,end=end,element_BYTES=width,
                encoding='BE16' if width==2 else 'BE32',physical_elements=(end-start)//width,
                role=role,original_read_PC=pc,editor_count_is_CPU_clamp=False)


def verify_rom(rom):
    if type(rom)is not bytes:raise ValueError('immutable canonical ROM bytes required')
    f.verify_rom(rom)
    for start,end,digest in GUARDS:
        if sha(rom[start:end])!=digest:raise ValueError('original consumer/producer bytes differ')
    for pc,target in ((0x6832,0x68A8),(0x430E,0x43A0),(0x43BC,0x4378),(0x27B6C,0x27B96)):
        if pc+2+int.from_bytes(rom[pc+2:pc+4],'big',signed=True)!=target:
            raise ValueError('original encoded PC-relative source base differs')
    if rom[0x386:0x38C]!=bytes.fromhex('4eb900006826'):raise ValueError('original boot caller differs')
    if rom[0x27B78:0x27B7C]!=bytes.fromhex('267b1028') or 0x27B7A+0x28!=0x27BA2:
        raise ValueError('original PC-indexed LONG source differs')
    if rom[0x68CE:0x68D4]!=bytes.fromhex('4df900c00004') or rom[0x27BBA:0x27BC0]!=bytes.fromhex('b1fc00ff7050'):
        raise ValueError('next compiled source boundary differs')


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),sources=[dict(**topology(spec),values=[int.from_bytes(rom[p:p+spec[2]],'big')
        for p in range(spec[0],spec[1],spec[2])]) for spec in SPECS])


def fixed(value,expected,mutable,label):
    f.keys(value,set(expected)|set(mutable),label)
    for key,item in expected.items():f.same(value[key],item,label+'.'+key)


def blocks(rom,fields):
    verify_rom(rom);fixed(fields,metadata(),{'sources'},'source package')
    sources=fields['sources']
    if type(sources)is not list or len(sources)!=len(SPECS):raise ValueError('fixed five physical source roles required')
    result=[]
    for source,spec in zip(sources,SPECS):
        fixed(source,topology(spec),{'values'},'source');start,end,width,role,_=spec
        values=source['values']
        if type(values)is not list or len(values)!=(end-start)//width:raise ValueError('fixed physical element allocation differs')
        data=b''.join(f.uint(value,(1<<(width*8))-1,'full source scalar').to_bytes(width,'big') for value in values)
        result.append(dict(id=source['id'],start=start,end=end,data=data,role=role))
    # Existing additive-layout consumers traverse physical allocation order.
    # Fields remain grouped by responsibility; emission never revisits an EA.
    return sorted(result,key=lambda row:row['start'])


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def flags():
    return dict(CPU_executed=False,hardware_executed=False,true_call_RTS_executed=False,
                independent_CPU_comparison=False,complete_entry=False,natural_domain_complete=False)


def event(kind,pc,logical,size,value):
    return dict(kind=kind,pc=pc,logical_address=logical&0xFFFFFFFF,
                address=logical&0xFFFFFF,size=size,value=value)


def source_read(image,pc,logical,size,events):
    address=logical&0xFFFFFF
    if logical&1:raise ValueError('unaligned source access')
    if address+size>len(image):return None
    value=int.from_bytes(image[address:address+size],'big')
    events.append(event('source_read_projection',pc,logical,size,value));return value


def boot_preview(rom,fields):
    """Original nineteen source WORDs and the separate live68AA reread only."""
    image=rebuild(rom,fields);events=[]
    for index in range(19):
        value=source_read(image,0x6838,0x68A8+2*index,2,events)
        events.append(event('hardware_write_projection',0x6838,0xC00004,2,value))
    value=source_read(image,0x683E,0x68AA,2,events)
    events.append(event('RAM_write_projection',0x683E,0xFFFFF606,2,value))
    return dict(**flags(),status='remaining_hardware_sequence_not_executed',events=events,
                final_A2_LONG=0x68CE,final_D7_WORD=65535,saved_F606_WORD=value,
                read_WORDs=20,unique_source_bytes=38)


def queue_preview(rom,fields,*,seven_pairs=False,destination_LONG=0xFFFFF800):
    """Ordered original source reads and writes, including overwritten first WORDs.

    The seven-pair entry430E inherits A1; destination_LONG is supplied rather
    than guessed. Only the source-driven prefix is projected, not later helpers.
    """
    if type(seven_pairs)is not bool:raise ValueError('exact bool source selector required')
    f.uint(destination_LONG,0xFFFFFFFF,'supplied queue A1 LONG')
    image=rebuild(rom,fields);events=[];pointer=destination_LONG
    start,count,first_pc,second_pc=(0x43A0,7,0x4320,0x432A) if seven_pairs else (0x4378,10,0x43D0,0x43DA)
    generated=0xF0B if seven_pairs else 0xD01;attribute=0xE300 if seven_pairs else 0xE370
    for index in range(count):
        value=source_read(image,first_pc,start+4*index,2,events)
        if pointer&1:return dict(**flags(),status='odd_destination_write_boundary',events=events,completed_rows=index)
        events.append(event('RAM_write_projection',first_pc,pointer,2,value))
        # Original3298/3298 has no destination postincrement. The following
        #32FC overwrites that same WORD before incrementing A1 by two.
        events.append(event('RAM_write_projection',first_pc+2,pointer,2,0x200));pointer=(pointer+2)&0xFFFFFFFF
        events.append(event('RAM_write_projection',first_pc+6,pointer,2,generated));pointer=(pointer+2)&0xFFFFFFFF
        events.append(event('RAM_write_projection',first_pc+8,pointer,2,attribute));pointer=(pointer+2)&0xFFFFFFFF
        value=source_read(image,second_pc,start+4*index+2,2,events)
        events.append(event('RAM_write_projection',second_pc,pointer,2,value));pointer=(pointer+2)&0xFFFFFFFF
        generated=(generated+1)&65535;attribute=(attribute+(0x10 if seven_pairs else 8))&65535
        remaining=count-1-index
        if not seven_pairs:
            if remaining<6:attribute=(attribute+8)&65535
            if remaining<7:generated|=0x200
    return dict(**flags(),status='source_prefix_complete_helpers_not_executed' if seven_pairs else 'source_loop_RTS_not_executed',
                events=events,completed_rows=count,final_A0_LONG=start+count*4,final_A1_LONG=pointer,
                final_D7_WORD=65535,final_generated_WORD=generated,final_attribute_WORD=attribute,
                first_source_WORD_overwritten=True)


def signed_WORD(value):
    return value-65536 if value&0x8000 else value


def dispatch_preview(rom,fields,input_WORD,*,actor_LONG=0xFF7050,budget=64):
    """Original threshold search then signed-WORD PC-indexed LONG fetch.

    No six-bucket clamp and no fabricatedFFFF terminator. Crossing either
    editable allocation reads the serialized whole image, including code aliases.
    The selected target is returned, never executed or claimed as a safe pointer.
    """
    f.uint(input_WORD,65535,'actor1E source WORD');f.uint(actor_LONG,0xFFFFFFFF,'supplied actor A0 LONG')
    f.uint(budget,256,'bounded threshold reads')
    if budget==0:raise ValueError('positive read budget required')
    image=rebuild(rom,fields);events=[event('supplied_RAM_read_projection',0x27B68,actor_LONG+0x1E,2,input_WORD)]
    offset=65534;pointer=0x27B96
    for index in range(budget):
        offset=(offset+2)&65535
        value=source_read(image,0x28F96,pointer,2,events)
        if value is None:return dict(**flags(),status='unmapped_source_read_boundary',events=events,next_threshold_LONG=pointer,D1_WORD=offset)
        pointer=(pointer+2)&0xFFFFFFFF
        if input_WORD>=value:continue
        scaled=(offset<<1)&65535;logical=(0x27BA2+signed_WORD(scaled))&0xFFFFFFFF
        target=source_read(image,0x27B78,logical,4,events)
        if target is None:return dict(**flags(),status='unmapped_target_read_boundary',events=events,target_source_LONG=logical,D1_WORD=scaled)
        return dict(**flags(),status='callback_JSR_not_executed_boundary',events=events,threshold_reads=index+1,
                    helper_final_D1_WORD=offset,D1_WORD=scaled,final_A2_LONG=pointer,
                    target_source_LONG=logical,target_LONG=target,target_bus_address=target&0xFFFFFF,
                    target_is_odd=bool(target&1),source_catalog_alias=not(0x27BA2<=logical<0x27BBA))
    return dict(**flags(),status='threshold_read_budget_boundary',events=events,next_threshold_LONG=pointer,D1_WORD=offset,
                threshold_reads=budget,callback_executed=False)


def raw_guard(base):
    raw=d.raw_positions(base);positions={p for a,z,*_ in SPECS for p in range(a,z)}
    if not positions<=raw:raise ValueError('all142 source positions require sole existing raw authority')
    return dict(guarded_raw_bytes=len(positions),layout_remaining_raw=len(raw))


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('serialized whole-ROM roundtrip differs')
    boot=boot_preview(rom,fields);ten=queue_preview(rom,fields);seven=queue_preview(rom,fields,seven_pairs=True)
    inputs=(0,40,60,80,100,120)
    dispatch=[dict(input_WORD=value,projection=dispatch_preview(rom,fields,value)) for value in inputs]
    views=[boot,ten,seven]+[row['projection'] for row in dispatch]
    union={p for view in views for e in view['events'] if e['kind']=='source_read_projection' for p in range(e['address'],e['address']+e['size'])}
    positions={p for a,z,*_ in SPECS for p in range(a,z)}
    if union!=positions:raise ValueError('constructed actual-format source-read union differs from142')
    report=dict(**metadata(),editable_bytes=142,physical_blocks=5,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        constructed_read_union_bytes=len(union),constructed_projections=len(views),**flags(),
        source_guards=[dict(start=a,end=z,sha256=h,physical_emit=False) for a,z,h in GUARDS],
        boot=boot,queue_ten=ten,queue_seven=seven,conditional_dispatch=dispatch,
        unknown_business_meanings=['Queue pair business coordinates/roles are probable; original WORD widths and ordered reads are confirmed.',
            'Actor1E threshold meaning is unknown here; original comparison and encoded conditional callback addresses are confirmed.'],
        limitations=['No CPU, VDP, callback, nested frame, helper or natural-input-domain execution is claimed.',
            '6826 has hardware polling and later writes outside this source prefix; it is not a newly completed function.',
            '430E is an internal inherited-A1 prefix, not counted as an independent function; subsequent4480/UI helpers are not executed.',
            'The first queue sourceWORD write is overwritten by0200 at the same address; both writes remain ordered.',
            'Six editable thresholds and six editable fullLONG targets are physical catalogs only. No sentinel/clamp is imposed.',
            'Threshold equality continues; ADDQ.W2 precedesCMP, helperD1 is ASL.W1 then signed-WORD indexed LONG EA.',
            'Diagnostic2047/FFFF may read edited directory/code aliases or end at an absolute read budget; no neighboring bytes are emitted.'])
    members={'fields.json':dump(fields),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=142,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value):
    path=f.safe_path(value)
    if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh formal directory or dedicated source build output required')
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
        result=dict(path=str(target),editable_bytes=142,members={name:sha(data) for name,data in members.items()})
    else:
        image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
