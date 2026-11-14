"""1320 source bytes witnessed by original18080/18084 full-WORD indexed reads."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
import json
from tools.direct_code import direct_code as d
f,ROOT=d.f,d.ROOT
FORMAT='g5510-roster-conditional-pointer-source-aliases-v1'
EDITABLE_BYTES=1320
FORMAL_ROOT=ROOT/'analysis/roster_pointer_source_alias_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
OUTPUT_ROOT=ROOT/'build/roster_pointer_source_alias_fields'
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_MANIFEST_SHA=reference_value(__name__, 'LAYOUT_MANIFEST_SHA')
BODY_SHA=reference_value(__name__, 'BODY_SHA')
SPANS=(
    (0x1008C,0x1009C),(0x103E8,0x103EA),(0x10A06,0x10A34),(0x10A4C,0x10A58),
    (0x10D0C,0x10D14),(0x10D36,0x10D64),(0x10E38,0x10E8A),(0x10F88,0x10F92),
    (0x111A6,0x111AC),(0x125D0,0x125D8),(0x12872,0x12878),(0x12A90,0x12A98),
    (0x1343C,0x1344C),(0x13464,0x1347C),(0x13B80,0x13B86),(0x13F66,0x13F6C),
    (0x14334,0x1433C),(0x15BD2,0x15C1A),(0x15EB8,0x15ED0),(0x15F6A,0x15F84),
    (0x16670,0x16678),(0x16A78,0x16A98),(0x16DE4,0x16DE8),(0x174F0,0x17514),
    (0x17C7A,0x17C8A),(0x17F18,0x17F30),(0x1805A,0x1807A),(0x18196,0x181A6),
    (0x183BE,0x183F8),(0x185AE,0x185E4),(0x18D6A,0x18D72),(0x190C2,0x190C6),
    (0x192BA,0x192C0),(0x1966C,0x19674),(0x19900,0x19908),(0x19974,0x1997A),
    (0x19F66,0x19F6E),(0x19FBC,0x19FC2),(0x1A3AA,0x1A3B2),(0x1A430,0x1A438),
    (0x1A9AA,0x1A9B0),(0x1AC1E,0x1AC26),(0x1AF4C,0x1AF5C),(0x1AF78,0x1AF80),
    (0x1B128,0x1B138),(0x1B18C,0x1B19C),(0x1C1A6,0x1C1C2),(0x1CC26,0x1CC76),
    (0x1D644,0x1D658),(0x1D6A4,0x1D6AC),(0x1D91A,0x1D936),(0x1D9AC,0x1D9BE),
    (0x1DA7C,0x1DAD0),(0x1DC10,0x1DC58),(0x1E09E,0x1E0AE),(0x1E23E,0x1E24C),
    (0x1E4F2,0x1E4F8),(0x1E566,0x1E56E),(0x1E5F6,0x1E5FE),(0x1E670,0x1E690),
    (0x1EF8A,0x1EF98),(0x1F8CC,0x1F8D4),(0x1FAA0,0x1FAA8),(0x1FAFC,0x1FB08),
    (0x20010,0x20014),
)
ALIAS_SPANS=tuple(row for row in SPANS if row!=(0x1805A,0x1807A))
sha,dump,load_fields=f.sha,f.dump,f.load_json


def metadata():
    return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
        confidence='confirmed_conditional_source_reads_unknown_natural_domain',
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        executable_code_added=0,recovered_functions_added=0,
        raw_authority_snapshot=dict(layout_id=LAYOUT_ID,manifest_sha256=LAYOUT_MANIFEST_SHA))


def verify_rom(rom):
    if type(rom)is not bytes:raise ValueError('immutable original ROM bytes required')
    f.verify_rom(rom)
    if sha(rom[0x1807A:0x18158])!=BODY_SHA:raise ValueError('complete original body differs')
    if rom[0x1807A:0x18088]!=bytes.fromhex('3038f6d6e548227b00d8247b00e4'):
        raise ValueError('original liveWORD/shift/twoLONG prefix differs')
    if 0x18082+int.from_bytes(rom[0x18083:0x18084],'big',signed=True)!=0x1805A or 0x18086+int.from_bytes(rom[0x18087:0x18088],'big',signed=True)!=0x1806A:
        raise ValueError('encoded signed PC bases differ')


def witness(address):
    # Deterministic smallest selector representative for the four equivalent
    # fullWORD inputs. This is a source witness, not a natural-domain assertion.
    base,pc=(0x1805A,0x18080) if address<0x2005A else (0x1806A,0x18084)
    window=address-((address-base)%4);selector=((window-base)&65535)>>2
    return dict(selector_WORD=selector,original_read_PC=pc,source_LONG=window,byte_index=address-window)


def byte_topology(address):
    return dict(id=f'rom_{address:06X}_conditional_pointer_source_BYTE',address=address,**witness(address))


def span_topology(span):
    start,end=span
    return dict(id=f'rom_{start:06X}_{end:06X}_conditional_source_fragment',start=start,end=end,
                role='conditional_pointer_read_source_BYTEs_original_business_role_unknown')


def pointer_topology(index):return dict(id=f'rom_{0x1805A+4*index:06X}_original_pointer_LONG',address=0x1805A+4*index,encoding='BE32')


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),pointers=[dict(**pointer_topology(index),value=int.from_bytes(rom[0x1805A+4*index:0x1805E+4*index],'big')) for index in range(8)],
        fragments=[dict(**span_topology(span),bytes=[dict(**byte_topology(p),value=rom[p]) for p in range(*span)]) for span in ALIAS_SPANS])


def fixed(value,expected,mutable,label):
    f.keys(value,set(expected)|set(mutable),label)
    for key,item in expected.items():f.same(value[key],item,label+'.'+key)


def blocks(rom,fields):
    verify_rom(rom);fixed(fields,metadata(),{'pointers','fragments'},'source alias package')
    pointers=fields['pointers'];fragments=fields['fragments']
    if type(pointers)is not list or len(pointers)!=8 or type(fragments)is not list or len(fragments)!=64:raise ValueError('fixed eightLONG/64fragment topology required')
    data=bytearray();result=[]
    for index,row in enumerate(pointers):
        fixed(row,pointer_topology(index),{'value'},'original pointer')
        data.extend(f.uint(row['value'],0xFFFFFFFF,'full original pointer LONG').to_bytes(4,'big'))
    result.append(dict(id='rom_01805A_pointer_LONGs',start=0x1805A,end=0x1807A,data=bytes(data),role='original_eight_full_pointer_LONGs'))
    for row,span in zip(fragments,ALIAS_SPANS):
        fixed(row,span_topology(span),{'bytes'},'conditional source fragment');values=row['bytes']
        if type(values)is not list or len(values)!=span[1]-span[0]:raise ValueError('fixed BYTE authority allocation differs')
        data=bytearray()
        for item,address in zip(values,range(*span)):
            fixed(item,byte_topology(address),{'value'},'witnessed source BYTE');data.append(f.uint(item['value'],255,'full conditional source BYTE'))
        result.append(dict(id=row['id'],start=span[0],end=span[1],data=bytes(data),role=row['role']))
    return sorted(result,key=lambda row:row['start'])


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def flags():return dict(CPU_executed=False,hardware_executed=False,true_call_RTS_executed=False,
    independent_CPU_comparison=False,complete_entry=False,natural_domain_complete=False,pointers_followed=False)


def view_image(image,selector_WORD):
    """Pure original prefix projection: no reads through fetched A1 or A2."""
    f.uint(selector_WORD,65535,'F6D6 fullWORD');offset=(selector_WORD<<2)&65535
    signed=offset-65536 if offset&0x8000 else offset
    events=[dict(kind='supplied_RAM_read_projection',pc=0x1807A,logical_address=0xFFFFF6D6,address=0xFFF6D6,size=2,value=selector_WORD)]
    targets=[]
    for base,pc in ((0x1805A,0x18080),(0x1806A,0x18084)):
        logical=(base+signed)&0xFFFFFFFF;address=logical&0xFFFFFF
        value=int.from_bytes(image[address:address+4],'big');targets.append(value)
        events.append(dict(kind='source_read_projection',pc=pc,logical_address=logical,address=address,size=4,value=value))
    return dict(**flags(),status='before_original18088_pointer_follow_boundary',events=events,
                shifted_D0_WORD=offset,signed_index=signed,A1_LONG=targets[0],A2_LONG=targets[1],
                target_bus_addresses=[value&0xFFFFFF for value in targets])


def pointer_preview(rom,fields,selector_WORD):return view_image(rebuild(rom,fields),selector_WORD)


def raw_guard(base):
    raw=d.raw_positions(base);actual={p for p in raw if 0x1005A<=p<0x2006A};expected={p for span in SPANS for p in range(*span)}
    if actual!=expected:raise ValueError('fixed81 raw-only source authority intersection differs')
    return dict(guarded_raw_bytes=len(expected),physical_spans=len(SPANS),layout_remaining_raw=len(raw))


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('serialized whole-ROM roundtrip differs')
    proofs=[]
    for span in SPANS:
        for address in range(*span):
            w=witness(address);view=view_image(image,w['selector_WORD'])
            read=next(e for e in view['events'] if e['pc']==w['original_read_PC'])
            if read['address']+w['byte_index']!=address or read['value'].to_bytes(4,'big')[w['byte_index']]!=image[address]:raise ValueError('perBYTE original input witness differs')
            proofs.append(dict(address=address,**w,original_BYTE=image[address]))
    offsets={(value<<2)&65535 for value in range(65536)}
    if len(offsets)!=16384 or sum(z-a for a,z in SPANS)!=1320:raise ValueError('original WORDshift/image scope differs')
    report=dict(**metadata(),editable_bytes=1320,pointer_LONG_bytes=32,conditional_alias_BYTEs=1288,physical_blocks=65,
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),**flags(),every_new_BYTE_witness_count=len(proofs),new_BYTE_witnesses=proofs,
        original_body=dict(start=0x1807A,end=0x18158,sha256=BODY_SHA,physical_emit=False),
        full_supplied_WORD_distinct_windows=16384,source_unions=[[0x1005A,0x2005A],[0x1006A,0x2006A]],
        source_union=[0x1005A,0x2006A],source_union_is_natural_domain=False,
        canonical_catalog=[view_image(image,index) for index in range(4)],
        limitations=['All witnesses use the actual F6D6 WORD producer and original LSL.W2 plus two encoded PC bases, not invented RAM addresses.',
            'Source classification is conditional pointer-read bytes only. Original fragment business/code purpose and natural F6D6 input domain remain unknown.',
            'TwoLONG reads complete before18088 followsA1. This model stops before pointer following and does not execute the original business function.',
            'Old typed neighbors are read from the edited whole image but not emitted; each new physicalBYTE has one edit authority.',
            'The32-byte local directory has eight fullLONG fields. All other1288 bytes are editable perBYTE fields with immutable input/read witnesses, not gaphex/padding.',
            'FullWORD selector high bits alias after lowWORD shift; no four-slot clamp or pointer-target validation is imposed.'])
    members={'fields.json':dump(fields),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=1320,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value):
    path=f.safe_path(value)
    if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh formal directory or dedicated roster-source build output required')
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
        result=dict(path=str(target),editable_bytes=1320,members={name:sha(data) for name,data in members.items()})
    else:
        image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
