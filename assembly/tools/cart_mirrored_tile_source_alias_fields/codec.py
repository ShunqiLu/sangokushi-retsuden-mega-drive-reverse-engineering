"""Lossless conditional tile-pixel source BYTEs under measured MAME cart aliases.

The original supplied WORD selects counted tokens, not an editor slot. Every
diagnostic source is read from the complete live image in original order.
This intermediate compatibility projection is not a full CPU/VDP or natural
domain recovery. The measurement dump is never a source/build dependency.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
from functools import lru_cache
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent/'work/original_g5510.bin'
OUTPUT_ROOT = ROOT/'build/cart_mirrored_tile_source_alias_fields'
FORMAL_ROOT = ROOT/'analysis/cart_mirrored_tile_source_alias_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT/'fields.json'
DEFAULT_BUNDLE = FORMAL_ROOT
FORMAT = 'g5510-counted-tile-mirrored-cart-source-BYTE-alias-v1'
EDITABLE_BYTES, PHYSICAL_BLOCKS = 90, 14
MAX_JSON = 8*1024*1024
MEMBERS = frozenset(('fields.json','fields.schema.json','validation.json','manifest.json'))
SPANS = ((0xBE93A,0xBE95A),(0xF475C,0xF475D),(0xF4760,0xF4761),
    (0xF476A,0xF476F),(0xF4770,0xF4772),(0xF4773,0xF4776),(0xF4779,0xF477A),
    (0xF649C,0xF649D),(0xF649E,0xF649F),(0xF64A1,0xF64A2),(0xF64A4,0xF64AA),
    (0xF64B2,0xF64B4),(0xF64B5,0xF64B7),(0xF749A,0xF74BA))
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
BODIES = ((0x94C,0x95E,reference_value(__name__, 'BODIES')),
    (0x661D4,0x662E4,reference_value(__name__, 'BODIES_2')))
ROM_REGIONS = ((0,0x200000),(0x204000,0x400000))
SRAM_APERTURE = (0x200000,0x204000)
MAPPER_HEADER_START, MAPPER_HEADER_END = 0x1A0, 0x1BC
MAPPER_HEADER_HEX = '00000000000fffff00ff000000ffffff5241f8200020000100203fff'
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
BANK_SHA256 = {'0b':reference_value(__name__, 'BANK_SHA256'),
    '0c':reference_value(__name__, 'BANK_SHA256_2'),
    '0f':reference_value(__name__, 'BANK_SHA256_3')}
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put
load_fields = shared.load_fields


def _s16(value):
    value &= 0xFFFF
    return value-0x10000 if value&0x8000 else value


def _image(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError('complete live 1MiB bytes image required')
    if image[MAPPER_HEADER_START:MAPPER_HEADER_END] != bytes.fromhex(MAPPER_HEADER_HEX):
        raise ValueError('original ROM/RAM/SRAM mapper geometry header changed')


def verify_rom(rom):
    _image(rom)
    if sha(rom) != ROM_SHA256:
        raise ValueError('canonical original ROM SHA-256 differs')
    _controls(rom)


def _controls(image):
    for start, end, digest in BODIES:
        if sha(image[start:end]) != digest:
            raise ValueError('original caller/control/helper bytes changed')


def cart_read(image, address, size, PC):
    """Measured profile only; SRAM, other devices and unmeasured ranges reject.

    The original CPU address is 32-bit; the bus address is 24-bit. Masking to
    physical ROM happens only after membership in an actual measured ROM region.
    """
    _image(image)
    address = uint(address,0xFFFFFFFF,'CPU address')
    PC = uint(PC,0xFFFFFFFF,'original read PC')
    if type(size) is not int or size not in (1,2,4):
        raise ValueError('original BYTE/WORD/LONG width required')
    bus = address&0xFFFFFF
    if size > 1 and bus&1:
        raise ValueError(f'original WORD alignment boundary at {bus:06X}')
    if not any(first <= bus and bus+size <= end for first,end in ROM_REGIONS):
        if SRAM_APERTURE[0] <= bus < SRAM_APERTURE[1]:
            raise ValueError(f'SRAM aperture is not ROM source at {bus:06X}')
        raise ValueError(f'unmeasured or mixed cart/device boundary at {bus:06X}')
    positions = [(bus+i)&0xFFFFF for i in range(size)]
    value = int.from_bytes(bytes(image[p] for p in positions),'big')
    return dict(PC=PC,address=address,bus_address=bus,bytes=size,value=value,
        memory='ROM_identity' if bus < ROM_SIZE else 'measured_ROM_alias',
        physical_addresses=positions)


def _requests(selector):
    """Original source read requests; every next address uses live read values."""
    for role,base,count,stride,tpc,ppc in (
        ('primary',0xAE39A,48,96,0x662B8,0x662D8),
        ('secondary8',0xB439A,8,16,0x66214,0x6622A),
        ('secondary4',0xB539A,4,8,0x66252,0x66268)):
        first = base+_s16((selector*stride)&0xFFFF)
        for item in range(count):
            token = yield dict(PC=tpc,address=first+2*item,bytes=2,
                role=role+'_token',token_index=item)
            if role == 'primary':
                tile = 0xB649A+(token&0xFFFF)*32
            else:
                tile = 0xB649A+(0x10000 if token >= 0x800 else 0)
            for lane in range(8):
                address = tile+4*lane if role == 'primary' else tile+_s16(((token<<5)+4*lane)&0xFFFF)
                yield dict(PC=ppc,address=address&0xFFFFFFFF,bytes=4,
                    role=role+'_pixels',token_index=item,lane=lane,token_WORD=token)
    selected = yield dict(PC=0x66288,address=0xB639A+_s16(selector),bytes=1,
        role='palette_selector',token_index=None)
    for lane in range(8):
        yield dict(PC=0x662A6,address=0xB599A+(selected<<5)+4*lane,bytes=4,
            role='palette',token_index=None,lane=lane,selector_BYTE=selected)


def source_view(image, selector_WORD, source_read_budget=549, ram_f6c4_WORD=0):
    """Conditional real 94C caller/read/call prefix; no host token injection.

    The source budget is diagnostic, not an original CPU terminator. VDP writes
    are a declared sink; unused CPU flags and interrupts are not simulated.
    """
    _image(image);_controls(image)
    selector = uint(selector_WORD,0xFFFF,'supplied complete F3A6 WORD')
    budget = uint(source_read_budget,549,'diagnostic source read budget')
    f6c4 = uint(ram_f6c4_WORD,0xFFFF,'live palette destination WORD')
    ram = bytearray(65536)
    ram[0xF3A6:0xF3A8]=selector.to_bytes(2,'big');ram[0xF6C4:0xF6C6]=f6c4.to_bytes(2,'big')
    sp=0xFFFFFE80;frames=[];stack=[];pairs=[];reads=[];writes=[];vdp=[];ordered=[]
    def write(pc,address,size,value,role):
        ram[address&0xFFFF:(address&0xFFFF)+size]=value.to_bytes(size,'big')
        event=dict(PC=pc,address=address,bus_address=address&0xFFFFFF,bytes=size,value=value,role=role)
        writes.append(event);ordered.append(dict(kind='RAM_write',**event));return event
    def call(pc,target,return_pc):
        nonlocal sp
        sp=(sp-4)&0xFFFFFFFF
        event=write(pc,sp,4,return_pc,'actual_call_return_LONG')
        frame=dict(call_PC=pc,target=target,return_PC=return_pc,SP=sp)
        frames.append(frame);stack.append(dict(kind='call',**frame,write=event))
    def ret(pc):
        nonlocal sp
        value=int.from_bytes(ram[sp&0xFFFF:(sp&0xFFFF)+4],'big')
        frame=frames.pop()
        if value != frame['return_PC']:
            raise ValueError('live original stack return differs')
        event=dict(PC=pc,address=sp,bus_address=sp&0xFFFFFF,bytes=4,value=value,role='actual_RTS_return_LONG')
        ordered.append(dict(kind='RAM_read',**event));stack.append(dict(kind='RTS',**event))
        pairs.append(dict(**frame,actual_RTS_PC=pc));sp=(sp+4)&0xFFFFFFFF
    result=dict(selector_WORD=selector,natural_domain='unknown',source_read_budget=budget,
        budget_is_original_CPU_stop=False,caller_entry=0x94C,true_JSR_PC=0x958,
        caller_RAM_read=dict(PC=0x950,address=0xFFFFF3A6,WORD=selector),
        RAM_BYTES=65536,ram_f6c4_WORD=f6c4,source_reads=reads,stack_events=stack,
        actual_call_RTS_pairs=pairs,RAM_writes=writes,VDP_writes=vdp,ordered_events=ordered,
        initial_SP=sp,complete_CPU=False,complete_VDP=False,
        condition='constructed RAM, conditional VDP write sink, no interrupt/async mutation')
    ordered.append(dict(kind='RAM_read',PC=0x950,address=0xFFFFF3A6,bus_address=0xFFF3A6,
        bytes=2,value=int.from_bytes(ram[0xF3A6:0xF3A8],'big'),role='caller_live_selector_WORD'))
    call(0x958,0x661D4,0x95E)
    command=(((5<<7)>>2)|0x4000)<<16
    vdp.append(dict(PC=0x661E4,address=0xC00004,bytes=4,value=command))
    ordered.append(dict(kind='conditional_VDP_write',**vdp[-1]))
    call(0x661FA,0x662B4,0x661FE)
    requests=_requests(selector);request=next(requests)
    try:
        while True:
            if request['role']=='primary_pixels' and request['lane']==0:
                call(0x662BA,0x662C4,0x662BE)
            if request['role']=='palette' and request['lane']==0:
                f6c4=int.from_bytes(ram[0xF6C4:0xF6C6],'big')
                ordered.append(dict(kind='RAM_read',PC=0x66298,address=0xFFFFF6C4,bus_address=0xFFF6C4,
                    bytes=2,value=f6c4,role='live_palette_destination_WORD'))
            if len(reads)>=budget:
                result.update(status='diagnostic_source_read_budget_exhausted',boundary_PC=request['PC'])
                break
            event=cart_read(image,request['address'],request['bytes'],request['PC'])
            event.update({key:value for key,value in request.items() if key not in ('PC','address','bytes')})
            reads.append(event);ordered.append(dict(kind='ROM_read',**event))
            if request['role'].endswith('_pixels'):
                target=dict(PC=request['PC'],address=0xC00000,bytes=4,value=event['value'])
                vdp.append(target);ordered.append(dict(kind='conditional_VDP_write',**target))
            if request['role']=='primary_pixels' and request['lane']==7:
                ret(0x662E2)
                if request['token_index']==47:ret(0x662C2)
            if request['role']=='palette':
                write(0x662A6,0xFFFFFB20+4*request['lane'] if f6c4==2 else 0xFFFFFB00+4*request['lane'],
                    4,event['value'],'palette_copy')
            request=requests.send(event['value'])
    except StopIteration:
        write(0x662AC,0xFFFFF31E,2,1,'palette_pending_WORD');ret(0x662B2)
        result.update(status='all60_tokens_and_palette_returned',final_PC=0x95E)
    except ValueError as error:
        result.update(status='mapping_read_boundary',boundary=str(error),boundary_PC=request['PC'],
            boundary_address=request['address'],boundary_bytes=request['bytes'])
    result.update(source_read_count=len(reads),complete_token_count=sum(row['role'].endswith('_token') for row in reads),
        final_SP=sp,unreturned_calls=list(frames),real_call_RTS_pair_count=len(pairs))
    return result


@lru_cache(maxsize=2)
def _catalog(rom):
    verify_rom(rom)
    wanted={p for start,end in SPANS for p in range(start,end)}
    if len(wanted)!=EDITABLE_BYTES or len(SPANS)!=PHYSICAL_BLOCKS:
        raise ValueError('unique fixed physical costs differ')
    selected={}
    for selector in range(8192):
        requests=_requests(selector);request=next(requests);ordinal=0;token=None
        try:
            while True:
                event=cart_read(rom,request['address'],request['bytes'],request['PC'])
                if request['role'].endswith('_token'):
                    token=dict(PC=request['PC'],address=request['address'],WORD=event['value'])
                for position in set(event['physical_addresses'])&wanted:
                    selected.setdefault(position,dict(address=position,selector_WORD=selector,
                        pixel_selector_aliases=[selector+8192*k for k in range(8)],read_PC=request['PC'],
                        source_event_ordinal=ordinal,source_bus_address=event['bus_address'],
                        source_LONG_value=event['value'],mapping=event['memory'],original_token_read=token))
                ordinal+=1;request=requests.send(event['value'])
        except StopIteration:
            pass
        if set(selected)==wanted:break
    if set(selected)!=wanted or sha(bytes(rom[p] for p in sorted(wanted)))!=SOURCE_SHA256:
        raise ValueError('fixed canonical source cost/digest or original prefix witness differs')
    return tuple(selected[p] for p in sorted(wanted))


def physical_positions(rom):
    verify_rom(rom)
    return tuple(row['address'] for row in _catalog(rom))


def witness(rom,address):
    verify_rom(rom)
    address=uint(address,ROM_SIZE-1,'physical source BYTE')
    for row in _catalog(rom):
        if row['address']==address:return load_fields(dump(row))
    raise ValueError('outside unique physical BYTE allocation')


def metadata(rom):
    physical_positions(rom)
    return dict(format=FORMAT,confidence='confirmed_conditional_source_encoding',
        resource_role='candidate_counted_tile_pixel_LONG_source_BYTE_alias',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),source_union_BYTES=EDITABLE_BYTES,
        source_union_sha256=SOURCE_SHA256,physical_blocks=PHYSICAL_BLOCKS,
        physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in SPANS],
        raw_baseline=dict(layout_id=LAYOUT_ID,manifest_sha256=LAYOUT_SHA256,raw_BYTES=14329,
            source_all_fixed_raw=True,bank_sha256=BANK_SHA256),
        cart_profile=dict(emulator='MAME 0.289 (mame0289)',driver='megadrij',
            original_cart_SMD_sha256=reference_value(__name__, 'metadata'),
            executable_sha256=reference_value(__name__, 'metadata_2'),
            measured_ROM_regions=[list(row) for row in ROM_REGIONS],physical_rule='bus24 & 0FFFFF only inside measured ROM regions',
            SRAM_aperture=list(SRAM_APERTURE),initial_SRAM_BYTE=255,SRAM_is_not_ROM=True,
            geometry_header=dict(start=MAPPER_HEADER_START,end=MAPPER_HEADER_END,bytes=MAPPER_HEADER_HEX),
            full_ROM_mapped_BYTEs_measured=4177920,measurement_dump_sha256=reference_value(__name__, 'metadata_3'),
            measurement_dump_build_dependency=False,outside4M='unmeasured reject',original_hardware_equivalence='unknown'),
        evidence=dict(controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES],
            supplied_RAM_WORD=0xFFFFF3A6,caller_read_PC=0x950,true_JSR_PC=0x958,return_PC=0x95E,
            primary=dict(base=0xAE39A,count=48,WORD_stride=96,token_read_PC=0x662B8,
                unsigned_token_LONG_shift=5,pixel_base=0xB649A,pixel_read_PC=0x662D8),
            secondary=[dict(base=0xB439A,count=8,WORD_stride=16,read_PC=0x66214,pixel_PC=0x6622A),
                dict(base=0xB539A,count=4,WORD_stride=8,read_PC=0x66252,pixel_PC=0x66268)],
            secondary_rule='live WORD >=0800 adds10000; LSL.W5 then signedWORD EA, ADDQ.W4 per LONG',
            LONG_reads_per_token=8,complete_source_reads=549,real_call_RTS_pairs=50,
            pixel_WORD_period=8192,pixel_fullWORD_aliases=8,palette_periodic=False,
            palette_selector_base=0xB639A,palette_base=0xB599A,live_palette_RAM_WORD=0xFFFFF6C4,
            counted_termination='original DBRA 48/8/4 tokens and8 palette LONGs; no token marker'),
        editing_authority='unique physical BYTE; old token/control/palette neighbours remain live views',
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        complete_function_recovery=False,independent_CPU_comparison=False,
        primary_atlas_owner='unknown',natural_selector_domain='unknown',edited_gameplay_safety='unknown',
        full_4bpp_tile_ownership_claimed=False,padding_or_free_space_claimed=False)


def extract(rom):
    return dict(**metadata(rom),source_BYTEs=[dict(address=a,BYTE=rom[a]) for a in physical_positions(rom)])


def blocks(rom,fields):
    fixed=metadata(rom);keys(fields,set(fixed)|{'source_BYTEs'},'mirrored cart source package')
    for key,value in fixed.items():same(fields[key],value,'package.'+key)
    data={}
    for address,row in zip(physical_positions(rom),exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'source BYTEs')):
        keys(row,{'address','BYTE'},'source BYTE');same(row['address'],address,'physical address/order')
        data[address]=uint(row['BYTE'],255,'all source BYTE bits')
    return [dict(id=f'rom_{a:06X}_mirrored_tile_source_BYTEs',start=a,end=z,
        data=bytes(data[p] for p in range(a,z)),role='candidate_conditional_tile_pixel_LONG_source_BYTE_alias') for a,z in SPANS]


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def schema(rom):
    def obj(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def fixed(value):
        if type(value)is dict:return obj({k:fixed(v) for k,v in value.items()})
        if type(value)is list:return dict(type='array',prefixItems=[fixed(v) for v in value],items=False,minItems=len(value),maxItems=len(value))
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(value)],const=value)
    props={key:fixed(value) for key,value in metadata(rom).items()}
    props['source_BYTEs']=dict(type='array',minItems=EDITABLE_BYTES,maxItems=EDITABLE_BYTES,
        prefixItems=[obj(dict(address=fixed(a),BYTE=dict(type='integer',minimum=0,maximum=255))) for a in physical_positions(rom)],items=False)
    return dict(**obj(props),**{'$schema':'https://json-schema.org/draft/2020-12/schema'},
        description='Exact90 unique physicalBYTEs; cartaliases never duplicate physical emission or clamp CPU input.')


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('serialized complete ROM roundtrip differs')
    entries=sorted({row['selector_WORD'] for row in _catalog(rom)})
    views=[source_view(rom,index) for index in entries]
    if any(view['status']!='all60_tokens_and_palette_returned' or view['real_call_RTS_pair_count']!=50 for view in views):
        raise ValueError('canonical complete original source prefix differs')
    validation=dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),canonical_BYTE_witnesses=list(_catalog(rom)),
        canonical_prefixes=[dict(selector_WORD=view['selector_WORD'],source_reads=view['source_read_count'],
            tokens=view['complete_token_count'],real_call_RTS_pairs=view['real_call_RTS_pair_count'],status=view['status']) for view in views],
        limitations=['Conditional complete source/call prefix, not natural input domain or full CPU/VDP.',
            'Original hardware equivalence and primary atlas ownership remain unknown.',
            'Measured aliases are ROM windows only; SRAM/other devices never contribute source authority.'])
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema(rom)),'validation.json':dump(validation)}
    members['manifest.json']=dump(dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    if any(len(data)>MAX_JSON for data in members.values()):raise ValueError('bounded JSON bundle cost exceeded')
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    for ancestor in (path,*path.parents):
        if ancestor.is_symlink() or getattr(ancestor,'is_junction',lambda:False)():raise ValueError('reparse output refused')
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError('dedicated fresh build output or exact fresh formal bundle required')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'));parser.add_argument('--rom',default=str(DEFAULT_ROM))
    parser.add_argument('--fields');parser.add_argument('--bundle');parser.add_argument('--output');args=parser.parse_args(argv)
    target=None
    if args.command=='export':
        if args.output is None or args.fields is not None or args.bundle is not None:raise ValueError('export requires output only')
        target=fresh_output(args.output,bundle=True)
    elif args.command=='import':
        if args.output is None or args.bundle is not None:raise ValueError('import requires fresh .bin output')
        target=fresh_output(args.output)
        if target.suffix.lower()!='.bin':raise ValueError('fresh .bin output required')
    elif args.output is not None or args.fields is not None and args.bundle is not None:raise ValueError('verify takes fields or bundle, writes nothing')
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={name:sha(data) for name,data in members.items()})
    elif args.command=='verify' and args.bundle is not None:
        path=safe_path(args.bundle)
        if not path.is_dir() or {p.name for p in path.iterdir()}!=MEMBERS:raise ValueError('exact four bundle members required')
        for name,data in render_bundle(rom).items():
            if read_bounded(path/name,MAX_JSON)!=data:raise ValueError('generated member drift: '+name)
        result=dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:put(target,image)
        result=dict(exact_canonical=image==rom,sha256=sha(image),editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
