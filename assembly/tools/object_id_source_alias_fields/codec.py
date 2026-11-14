"""Lossless BYTE fields read by the original actor-ID/counter source path.

The complete conditional entry RAM selects actor WORD800A. Original3D810
builds the list, reads the live selector BYTE and follows the live source.
This reuses a bounded original operand engine, not a new full CPU or owner.
"""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
from functools import lru_cache
import json
from pathlib import Path
from tools.scene_object_source_alias_fields import codec as obj

ROOT=Path(__file__).resolve().parents[2]
ROM_SIZE,ROM_SHA256,DEFAULT_ROM=obj.ROM_SIZE,obj.ROM_SHA256,obj.DEFAULT_ROM
OUTPUT_ROOT=ROOT/'build/object_id_source_alias_fields'
FORMAL_ROOT=ROOT/'analysis/object_id_source_alias_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
FORMAT='g5510-conditional-actor-ID-counter-object-source-BYTEs-v1'
MEMBERS=obj.MEMBERS
MAX_JSON=16*1024*1024
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256=reference_value(__name__, 'LAYOUT_SHA256')
EDITABLE_BYTES,PHYSICAL_BLOCKS=200,49
WITNESS_FRAMES=((16,3998),(16,1189),(16,1291),(0,2844),(0,2838))
SOURCE_SPANS=(
    (0xCC99A,0xCC9F2),
    (0xF459A,0xF459B),
    (0xF45A3,0xF45A6),
    (0xF45A9,0xF45AB),
    (0xF45AD,0xF45AE),
    (0xF45B0,0xF45B6),
    (0xF45B7,0xF45B9),
    (0xF45BA,0xF45BF),
    (0xF45C1,0xF45C3),
    (0xF45C4,0xF45C6),
    (0xF45C7,0xF45C8),
    (0xF45CA,0xF45CF),
    (0xF45D3,0xF45D4),
    (0xF45DA,0xF45DD),
    (0xF45DE,0xF45DF),
    (0xF45E3,0xF45E6),
    (0xF45EA,0xF45EE),
    (0xF45EF,0xF45F1),
    (0xF45F7,0xF45F8),
    (0xF45FC,0xF45FF),
    (0xF4603,0xF4605),
    (0xF4607,0xF460C),
    (0xF460F,0xF4610),
    (0xF4613,0xF4616),
    (0xF461D,0xF461E),
    (0xF4620,0xF4622),
    (0xF4623,0xF4626),
    (0xF462B,0xF462F),
    (0xF4633,0xF4637),
    (0xF4639,0xF463A),
    (0xF4A23,0xF4A24),
    (0xF4C5B,0xF4C5D),
    (0xF6589,0xF658B),
    (0xF6592,0xF6599),
    (0xF659E,0xF65A1),
    (0xF65A3,0xF65A6),
    (0xF65A7,0xF65A8),
    (0xF65AF,0xF65B0),
    (0xF65B1,0xF65B2),
    (0xF65BA,0xF65BB),
    (0xF65C3,0xF65C4),
    (0xF65C6,0xF65C7),
    (0xF65C9,0xF65CA),
    (0xF65D0,0xF65D1),
    (0xF65D2,0xF65D3),
    (0xF65D9,0xF65DA),
    (0xF65DB,0xF65DE),
    (0xF65E2,0xF65E3),
    (0xF65E4,0xF65EA),
)
SOURCE_POSITIONS=frozenset(p for a,z in SOURCE_SPANS for p in range(a,z))
BODIES=obj.BODIES
ROLES=obj.ROLES
sha,dump,keys,same,uint,exact_list=obj.sha,obj.dump,obj.keys,obj.same,obj.uint,obj.exact_list
safe_path,read_bounded,put,load_fields=obj.safe_path,obj.read_bounded,obj.put,obj.load_fields
verify_rom=obj.verify_rom


def default_RAM():
    """Complete disclosed conditional entry packet, not mid-run state repair."""
    ram=bytearray(65536)
    for address,value in ((0x816A,0x800A),(0x813E,1),(0xF320,0x10)):
        ram[address:address+2]=value.to_bytes(2,'big')
    return bytes(ram)


def source_view(image,state_WORD,instruction_budget=50000,RAM_before=None,
                include_prefix_events=False,*,frame_counter_WORD=None):
    """Run the frozen real3D810 caller on a complete live initial RAM packet.

    Only explicit entry parameters FF8172.W and optional F320.W are applied
    once before original instructions. Supplied RAM keeps its F320 when no
    override is requested. No list, A6, pointer, index or return is injected.
    """
    if RAM_before is not None and (type(RAM_before) is not bytes or len(RAM_before)!=65536):
        raise ValueError('complete immutable64KiB initial RAM required')
    ram=default_RAM() if RAM_before is None else RAM_before
    if frame_counter_WORD is not None:
        counter=uint(frame_counter_WORD,65535,'full initial frame counter WORD')
        initial=bytearray(ram);initial[0xF320:0xF322]=counter.to_bytes(2,'big');ram=bytes(initial)
    view=obj.source_view(image,state_WORD,instruction_budget,ram,include_prefix_events)
    view.update(managed_source_reached=sorted(set(view['physical_source'])&SOURCE_POSITIONS),
        RAM_frame_default='base snapshot zero64KiB+FF816A.W800A/FF813E.W1/F320.W0010; explicit counter may override before entry; FF8172.Winput'
            if RAM_before is None else 'base snapshot complete supplied64KiB; explicit counter may override before entry; FF8172.Winput',
        initial_frame_counter_WORD=int.from_bytes(ram[0xF320:0xF322],'big'),
        initial_frame_counter_override=frame_counter_WORD is not None,
        natural_actor_ID_and_fullWORD_frame='unknown',
        source_selection='live40452 actorWORD ANDFF,40460 selectorBYTE,4049A counter WORD',
        complete_function_recovery=False,allocation_owner='unknown',natural_domain='unknown')
    return view


@lru_cache(maxsize=2)
def _catalog(rom):
    verify_rom(rom);found={}
    for counter,state in WITNESS_FRAMES:
        v=source_view(rom,state,frame_counter_WORD=counter)
        if v['result']!='actual_JSR_4033C_RTS_to_3D814' or v['final_SP']!=0xFFFFFD00:
            raise ValueError('canonical conditional caller no longer returns')
        for order,event in enumerate(v['source_events']):
            for lane,p in enumerate(event['physical_addresses']):
                if p in SOURCE_POSITIONS and p not in found:
                    if event['PC'] not in ROLES or event['width']!=1:
                        raise ValueError('unrecognized compact object source role')
                    found[p]=dict(address=p,state_WORD=state,F320_WORD=counter,actor_WORD=0x800A,
                        read_PC=event['PC'],source_role=ROLES[event['PC']],read_width=1,
                        source_address=event['address'],bus_address=event['bus_address'],
                        unit_BYTE_lane=lane,source_event_index=order,canonical_read_value=event['value'],
                        true_caller_PC=0x3D810,actual_list_producer=0x4040A,
                        actual_render_JSR=0x40354,actual_return_PC=0x3D814,actual_final_SP=v['final_SP'])
    if set(found)!=SOURCE_POSITIONS or len(found)!=EDITABLE_BYTES or len(obj._coalesce(found))!=PHYSICAL_BLOCKS:
        raise ValueError('canonical original source scope differs')
    return tuple(found[p] for p in sorted(found))


def physical_positions(rom):
    verify_rom(rom);return tuple(r['address'] for r in _catalog(rom))


def witness(rom,address):
    verify_rom(rom);address=uint(address,ROM_SIZE-1,'physical source BYTE address')
    for row in _catalog(rom):
        if row['address']==address:return load_fields(dump(row))
    raise ValueError('outside single source authority')


def metadata(rom):
    positions=physical_positions(rom)
    return dict(format=FORMAT,confidence='confirmed_conditional_original_actor_ID_counter_selected_source_reads',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),source_union_BYTES=EDITABLE_BYTES,
        source_union_sha256=sha(bytes(rom[p] for p in positions)),physical_blocks=PHYSICAL_BLOCKS,
        physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in SOURCE_SPANS],
        raw_baseline=dict(layout_id=LAYOUT_ID,manifest_sha256=LAYOUT_SHA256,raw_BYTES=9987,resources=106),
        source_roles=dict(resource='conditional_compact_sprite_record_components',
            BYTE='full0..255; first80h marker/X,Y,size/attributes,tilelow keep all bits',
            old_neighbors='live wholeimage only; no second physical editing authority',
            zero='actual conditional source reads, not padding or free space'),
        evidence=dict(entry_JSR_PC=0x3D810,entry_target=0x4033C,list_producer=0x4040A,
            list_gate='F320.W AND000F equals0; real31descending X bins/32RAMobjects with activeBIT7',
            original_list='actualLONG writeFF836A and CLRLFF836E before render; no supplied list orA6',
            render_JSR_PC=0x40354,old_helper_gate='813E.W1 originalBNE40452 bypasses40C94',
            actor_ID='40452 liveobjectWORD800A ANDI.W00FF gives0A;40460 liveBYTE404CC+0A=404D6 gives9',
            input_full_WORD='live8(A6).W ASL.W2 wraps toWORD; never catalog-clamped',
            counter='4040A low4bits gates list rebuild;4049A liveF320 LSR.W3 ANDI.W3 gives0or2',
            pointer='404AA LONG404D4+s16(ASL.W2(liveBYTE[404CC+(actorWORD AND00FF)]+ASL.W2(state)+counter))',
            attribute='404C4 WORD407D4+s16(ASL.W1(same intermediateindex))',
            source='404C8 originaltailJMP3B13C; unsigned F300 BYTE50h capacity, signedX clip, first80h',
            read_order='X(+0),Y(+3),size(+1),repeatedattribute(+1),tilelow(+2); thenA0+=4',
            original_return='3B23A RTS40358; MOVEM restoresA5;40364 BEQ40408 RTS3D814/SPFFFFFD00',
            witness_frames=[dict(F320_WORD=n,state_WORD=s) for n,s in WITNESS_FRAMES],
            original_whole_controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES]),
        conditional_frame='zero64KiB+816A.W800A/813E.W1/F320.W0000or0010/8172.Winput;D/A0exceptSPFFFFFD00;SR2500/CCR0',
        canonical_scope=dict(BYTEs=200,bankC=88,bankF=112,Ffront=112,Ftail=0,baseline_raw_subset=True),
        unknowns=['natural completeRAM frame','natural fullWORD actorstate/actorID/counter',
            'allocation/asset owner','earlier3D810 battle/UI closure','edited gameplay safety',
            'original hardware equivalence'],
        owner_bytes_added=0,functions_added=0,natural_domains_added=0,complete_domains_added=0,
        complete_function_recovery=False,independent_CPU_comparison=False,padding_or_free_space_claimed=False,
        instrumentation_budget_is_original_CPU_stop=False,final_semantic_high_level_recovery=False,
        cart_profile='MAME0.289 measured24bus ROM0..200000/204000..400000; SRAM200000..204000 rejected;4M+unknown',
        diagnostic_scope='successful operands/calls only, not completeexceptionframes; failedread addsnobytes; stoppedpostincrement maydifferfromsuccess-firstreference')


def _fixed(row):
    return {k:row[k] for k in ('address','source_role','read_width','unit_BYTE_lane')}


def extract(rom):
    return dict(**metadata(rom),source_BYTEs=[dict(**_fixed(r),BYTE=rom[r['address']]) for r in _catalog(rom)])


def blocks(rom,fields):
    fixed=metadata(rom);keys(fields,set(fixed)|{'source_BYTEs'},'actor-ID counter source package')
    for k,v in fixed.items():same(fields[k],v,'package.'+k)
    values={}
    for expected,row in zip(_catalog(rom),exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'source BYTEs')):
        keys(row,set(_fixed(expected))|{'BYTE'},'source component')
        for k,v in _fixed(expected).items():same(row[k],v,'source.'+k)
        values[expected['address']]=uint(row['BYTE'],255,'full source BYTE')
    return [dict(id=f'rom_{a:06X}_actor_ID_counter_source_BYTEs',start=a,end=z,
        data=bytes(values[p] for p in range(a,z)),role='conditional_actor_ID_counter_compact_sprite_source_BYTEs')
        for a,z in SOURCE_SPANS]


def rebuild(rom,fields):
    verify_rom(rom);image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def schema(rom):
    def object_schema(p):return dict(type='object',properties=p,required=list(p),additionalProperties=False)
    def fixed(value):
        if type(value) is dict:return object_schema({k:fixed(v) for k,v in value.items()})
        if type(value) is list:return dict(type='array',prefixItems=[fixed(v) for v in value],items=False,minItems=len(value),maxItems=len(value))
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(value)],const=value)
    props={k:fixed(v) for k,v in metadata(rom).items()}
    props['source_BYTEs']=dict(type='array',minItems=EDITABLE_BYTES,maxItems=EDITABLE_BYTES,items=False,
        prefixItems=[object_schema(dict(**{k:fixed(v) for k,v in _fixed(r).items()},BYTE=dict(type='integer',minimum=0,maximum=255))) for r in _catalog(rom)])
    return dict(**object_schema(props),**{'$schema':'https://json-schema.org/draft/2020-12/schema'},
        description='200 unique physical conditional source BYTEs; witnesses are not a CPU selector clamp.')


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('wholeROM serialized roundtrip differs')
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema(rom)),
        'validation.json':dump(dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
            whole_ROM_sha256=sha(image),canonical_BYTE_witnesses=list(_catalog(rom)),
            limitations=['Complete conditional initial RAM, not natural producer/owner.',
                'Shared original operand engine; no independent CPU/full gameplay claim.',
                'All old pointer/attribute/source BYTE neighbors live; edits can stop or change consumption.']))}
    members['manifest.json']=dump(dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,
        members={k:dict(bytes=len(v),sha256=sha(v)) for k,v in members.items()}))
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
    parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--fields')
    parser.add_argument('--bundle');parser.add_argument('--output')
    args=parser.parse_args(argv);target=None
    if args.command=='export':
        if args.output is None or args.fields is not None or args.bundle is not None:raise ValueError('export needs output only')
        target=fresh_output(args.output,True)
    elif args.command=='import':
        if args.output is None or args.bundle is not None:raise ValueError('import needs freshBIN')
        target=fresh_output(args.output)
        if target.suffix.lower()!='.bin':raise ValueError('freshBIN required')
    elif args.output is not None or args.fields is not None and args.bundle is not None:
        raise ValueError('verify accepts fields or bundle and writes nothing')
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={k:sha(v) for k,v in members.items()})
    elif args.command=='verify' and args.bundle is not None:
        path=safe_path(args.bundle)
        if not path.is_dir() or {p.name for p in path.iterdir()}!=MEMBERS:raise ValueError('exact four members required')
        for name,data in render_bundle(rom).items():
            if read_bounded(path/name,MAX_JSON)!=data:raise ValueError('bundle drift:'+name)
        result=dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:put(target,image)
        result=dict(exact_canonical=image==rom,sha256=sha(image),editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
