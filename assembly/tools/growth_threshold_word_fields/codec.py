"""52 lossless threshold bytes for the original 662E4/66326 reader."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
import json
from tools.direct_code import direct_code as d

f, ROOT = d.f, d.ROOT
START, END = 0x66478, 0x664AC
EDITABLE_BYTES = END-START
FORMAL_ROOT = ROOT/'analysis/growth_threshold_word_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT/'fields.json'
OUTPUT_ROOT = ROOT/'build/growth_threshold_word_fields'
FORMAT = 'g5510-growth-threshold-source-WORDs-v1'
GUARDS = (
    (0x662E4,0x66332,reference_value(__name__, 'GUARDS')),
    (0x66332,0x66478,reference_value(__name__, 'GUARDS_2')),
    (0x664AC,0x664C0,reference_value(__name__, 'GUARDS_3')),
)
sha,dump,load_fields = f.sha,f.dump,f.load_json


def metadata():
    return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
                confidence='confirmed_original_threshold_read_probable_growth_role',
                owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)


def topology():
    return dict(id='rom_066478_growth_threshold_WORDs',start=START,end=END,element_BYTES=2,
                WORD_order='big',physical_WORDs=26,original_read_PC=0x66326,
                editor_count_is_CPU_level_clamp=False,terminator_present=False)


def verify_rom(rom):
    if type(rom)is not bytes:raise ValueError('immutable canonical ROM bytes required')
    f.verify_rom(rom)
    for a,z,h in GUARDS:
        if sha(rom[a:z])!=h:raise ValueError('original consumer/helper/boundary differs')
    if rom[0x662F0:0x662F4]!=bytes.fromhex('47fa0186') or 0x662F2+int.from_bytes(rom[0x662F2:0x662F4],'big',signed=True)!=START:
        raise ValueError('original encoded PC-relative threshold base differs')
    for pc,raw in ((0x66314,'4242'),(0x66316,'14320000'),(0x6631A,'e34a'),
                   (0x6631E,'32300000'),(0x66322,'d2710000'),(0x66326,'b2732000'),(0x6632A,'64000008')):
        if rom[pc:pc+len(raw)//2]!=bytes.fromhex(raw):raise ValueError('original fixed-width source producer differs')


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),source=dict(**topology(),values=[int.from_bytes(rom[p:p+2],'big') for p in range(START,END,2)]))


def fixed(value,expected,mutable,label):
    f.keys(value,set(expected)|set(mutable),label)
    for key,item in expected.items():f.same(value[key],item,label+'.'+key)


def blocks(rom,fields):
    verify_rom(rom);fixed(fields,metadata(),{'source'},'growth source package')
    source=fields['source'];fixed(source,topology(),{'values'},'threshold source')
    values=source['values']
    if type(values)is not list or len(values)!=26:raise ValueError('fixed physical26-WORD allocation differs')
    data=b''.join(f.uint(value,65535,'full threshold WORD').to_bytes(2,'big') for value in values)
    return [dict(id=source['id'],start=START,end=END,data=data,role='original_growth_comparison_threshold_WORDs')]


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def flags():
    return dict(CPU_executed=False,hardware_executed=False,true_call_RTS_executed=False,
                independent_CPU_comparison=False,complete_entry=False,natural_domain_complete=False)


def supplied_read(pc,logical,size,value):
    return dict(kind='supplied_RAM_read_projection',pc=pc,logical_address=logical,
                address=logical&0xFFFFFF,size=size,value=value)


def comparison_preview(rom,fields,level_BYTE,primary_WORD,secondary_WORD,*,slot_WORD=0,marker_BYTE=0):
    """One original loop-read iteration, before unexecuted growth helpers.

    The caller's slot >=256 and marker FF guards are real; the 26-field catalog
    is not a guard on the zero-extended level BYTE, whose entire range is kept.
    """
    f.uint(level_BYTE,255,'C600 level BYTE');f.uint(marker_BYTE,255,'CC00 marker BYTE')
    f.uint(primary_WORD,65535,'C000 primary WORD');f.uint(secondary_WORD,65535,'BE00 secondary WORD')
    f.uint(slot_WORD,65535,'fetched EF78 slot WORD');image=rebuild(rom,fields);events=[]
    if slot_WORD>=256:return dict(**flags(),status='original_BCC66364_slot_boundary',events=events)
    events.append(supplied_read(0x6630A,0xFFFFCC00+slot_WORD,1,marker_BYTE))
    if marker_BYTE==255:return dict(**flags(),status='original_BEQ6632E_marker_skip',events=events)
    events.append(supplied_read(0x66316,0xFFFFC600+slot_WORD,1,level_BYTE))
    offset=(slot_WORD<<1)&65535;index=(level_BYTE<<1)&65535
    events.append(supplied_read(0x6631E,0xFFFFC000+offset,2,primary_WORD))
    events.append(supplied_read(0x66322,0xFFFFBE00+offset,2,secondary_WORD))
    logical=(START+index)&0xFFFFFFFF;address=logical&0xFFFFFF
    threshold=int.from_bytes(image[address:address+2],'big')
    events.append(dict(kind='source_read_projection',pc=0x66326,logical_address=logical,address=address,size=2,value=threshold))
    total=(primary_WORD+secondary_WORD)&65535;carry=total<threshold
    return dict(**flags(),status='original_BCC66334_helper_boundary' if not carry else 'original_BCS6632E_next_slot',
                events=events,index_WORD=index,threshold_WORD=threshold,sum_WORD=total,
                unsigned_comparison_carry=carry,original_branch_target=0x66334 if not carry else 0x6632E,
                helper_executed=False,next_slot_WORD=(slot_WORD+1)&65535 if carry else None)


def raw_guard(base):
    raw=d.raw_positions(base)
    if not set(range(START,END))<=raw:raise ValueError('all52 positions require sole existing raw authority')
    return dict(guarded_raw_bytes=52,layout_remaining_raw=len(raw))


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('serialized whole-ROM roundtrip differs')
    views=[comparison_preview(rom,fields,level,0,0) for level in range(26)]
    union={p for view in views for e in view['events'] if e['kind']=='source_read_projection' for p in range(e['address'],e['address']+e['size'])}
    if union!=set(range(START,END)):raise ValueError('constructed original read union differs from52')
    report=dict(**metadata(),editable_bytes=52,physical_blocks=1,whole_ROM_exact=True,
                whole_ROM_sha256=sha(image),constructed_local_read_union_bytes=len(union),constructed_read_projections=26,
                **flags(),source_guards=[dict(start=a,end=z,sha256=h,physical_emit=False) for a,z,h in GUARDS],
                original_threshold_source=topology(),source_WORDs=fields['source']['values'],
                limitations=['This is a source editor and bounded one-iteration read/comparison projection, not complete CPU/RAM/stack execution.',
                    'Slot>=256 and markerFF guards precede source reads; the full levelBYTE is zero-extended then shifted, without a26 clamp.',
                    'Primary+secondary is low-WORD wrap before unsignedCMP/BCC; edited FFFF is a full threshold, not a terminator.',
                    'Level26 reads next code4240 from the live image. Neighbors are not new fields and are never emitted.',
                    'All growth/stat/RNG helpers remain existing compiled authority; none are run or emitted twice.'])
    members={'fields.json':dump(fields),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=52,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value):
    path=f.safe_path(value)
    if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh formal directory or dedicated growth build output required')
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
        result=dict(path=str(target),editable_bytes=52,members={name:sha(data) for name,data in members.items()})
    else:
        image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
