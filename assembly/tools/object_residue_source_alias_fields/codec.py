"""Lossless BYTE fields from the real frame-counter-selected object source.

Original3D810 builds its object list; F320.W0010 selects ordinary source
residue2 while preserving that list producer. This is a conditional source
projection, not a new CPU, natural gameplay domain or allocation owner.
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
OUTPUT_ROOT=ROOT/'build/object_residue_source_alias_fields'
FORMAL_ROOT=ROOT/'analysis/object_residue_source_alias_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
FORMAT='g5510-conditional-frame-counter-object-source-BYTEs-v1'
MEMBERS=obj.MEMBERS
MAX_JSON=16*1024*1024
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256=reference_value(__name__, 'LAYOUT_SHA256')
EDITABLE_BYTES,PHYSICAL_BLOCKS=195,103
WITNESS_STATES=(2822,1270,1268)
SOURCE_SPANS=(
    (0xF4E0D,0xF4E0F),
    (0xF4E13,0xF4E16),
    (0xF4E19,0xF4E1B),
    (0xF4E1C,0xF4E23),
    (0xF4E27,0xF4E2A),
    (0xF4E2C,0xF4E2D),
    (0xF4E2F,0xF4E30),
    (0xF4E32,0xF4E36),
    (0xF4E3E,0xF4E3F),
    (0xF4E41,0xF4E46),
    (0xF4E4B,0xF4E4D),
    (0xF4E4F,0xF4E50),
    (0xF4E55,0xF4E56),
    (0xF4E5B,0xF4E5E),
    (0xF4E60,0xF4E61),
    (0xF4E64,0xF4E69),
    (0xF4E6B,0xF4E6C),
    (0xF4E6E,0xF4E6F),
    (0xF4E71,0xF4E72),
    (0xF4E74,0xF4E76),
    (0xF4E78,0xF4E7A),
    (0xF4E7B,0xF4E7D),
    (0xF4E7E,0xF4E80),
    (0xF4E84,0xF4E86),
    (0xF4E88,0xF4E89),
    (0xF4E8A,0xF4E8B),
    (0xF4E8D,0xF4E8F),
    (0xF4E93,0xF4E94),
    (0xF4E9E,0xF4E9F),
    (0xF4EA2,0xF4EA5),
    (0xF4EA6,0xF4EA7),
    (0xF4EAF,0xF4EB0),
    (0xF4EB1,0xF4EB3),
    (0xF4EB7,0xF4EB9),
    (0xF4EBA,0xF4EBC),
    (0xF4EBE,0xF4EC0),
    (0xF4EC2,0xF4EC6),
    (0xF4ECB,0xF4ECC),
    (0xF4ECE,0xF4ECF),
    (0xF4ED1,0xF4ED2),
    (0xF4ED3,0xF4ED5),
    (0xF4ED6,0xF4ED7),
    (0xF4EDC,0xF4EDD),
    (0xF4EED,0xF4EEE),
    (0xF4EF8,0xF4EF9),
    (0xF4EFB,0xF4EFC),
    (0xF4EFE,0xF4EFF),
    (0xF4F04,0xF4F06),
    (0xF4F0B,0xF4F0E),
    (0xF4F0F,0xF4F10),
    (0xF4F14,0xF4F16),
    (0xF4F19,0xF4F1B),
    (0xF4F1D,0xF4F1E),
    (0xF4F22,0xF4F24),
    (0xF6449,0xF644C),
    (0xF644E,0xF644F),
    (0xF6450,0xF6451),
    (0xF6457,0xF6459),
    (0xF645A,0xF645C),
    (0xF645D,0xF6461),
    (0xF6468,0xF6469),
    (0xF646B,0xF646D),
    (0xF646F,0xF6471),
    (0xF6474,0xF6475),
    (0xF6477,0xF647B),
    (0xF648D,0xF648E),
    (0xF648F,0xF6492),
    (0xF6494,0xF6495),
    (0xF6497,0xF6498),
    (0xF64BA,0xF64BB),
    (0xF64BD,0xF64BF),
    (0xF64C1,0xF64C3),
    (0xF64C7,0xF64C8),
    (0xF64C9,0xF64CB),
    (0xF64CF,0xF64D1),
    (0xF64D6,0xF64D7),
    (0xF64DA,0xF64DC),
    (0xF64DE,0xF64DF),
    (0xF64E2,0xF64E3),
    (0xF64E5,0xF64E6),
    (0xF64EB,0xF64EE),
    (0xF64F0,0xF64F1),
    (0xF64F9,0xF64FA),
    (0xF64FB,0xF64FC),
    (0xF64FF,0xF6500),
    (0xF6504,0xF6505),
    (0xF6507,0xF6509),
    (0xF6510,0xF6511),
    (0xF651F,0xF6521),
    (0xF6532,0xF6533),
    (0xF6534,0xF6535),
    (0xF6536,0xF6538),
    (0xF6542,0xF6543),
    (0xF6548,0xF654A),
    (0xF654D,0xF654F),
    (0xF6551,0xF6552),
    (0xF6557,0xF6558),
    (0xF6559,0xF655B),
    (0xF655E,0xF655F),
    (0xF6573,0xF6574),
    (0xF657D,0xF657E),
    (0xF65EC,0xF65EF),
    (0xF65F0,0xF6600),
)
SOURCE_POSITIONS=frozenset(p for a,z in SOURCE_SPANS for p in range(a,z))
BODIES=obj.BODIES
ROLES=obj.ROLES
sha,dump,keys,same,uint,exact_list=obj.sha,obj.dump,obj.keys,obj.same,obj.uint,obj.exact_list
safe_path,read_bounded,put,load_fields=obj.safe_path,obj.read_bounded,obj.put,obj.load_fields
verify_rom=obj.verify_rom


def default_RAM():
    """Complete disclosed conditional entry RAM; never a mid-execution patch."""
    ram=bytearray(65536)
    for address,value in ((0x816A,0x8000),(0x813E,1),(0xF320,0x10)):
        ram[address:address+2]=value.to_bytes(2,'big')
    return bytes(ram)


def source_view(image,state_WORD,instruction_budget=50000,RAM_before=None,include_prefix_events=False):
    """Run frozen original3D810 caller with the live complete supplied WORD.

    The shared original operand engine is not copied. Complete RAM is supplied
    once; only FF8172.W is set by its existing explicit entry parameter. The
    list, A6, index, source pointer and return stack are produced by original
    instructions, not injected. Changed gates may stop before the source.
    """
    view=obj.source_view(image,state_WORD,instruction_budget,
        default_RAM() if RAM_before is None else RAM_before,include_prefix_events)
    view.update(managed_source_reached=sorted(set(view['physical_source'])&SOURCE_POSITIONS),
        RAM_frame_default='zero64KiB+FF816A.W8000/FF813E.W1/F320.W0010+FF8172.Winput'
            if RAM_before is None else 'complete supplied64KiB+FF8172.Winput',
        natural_F320_and_fullWORD_frame='unknown',source_selection='live ordinary4049A frame-counter residue',
        complete_function_recovery=False,allocation_owner='unknown',natural_domain='unknown')
    return view


@lru_cache(maxsize=2)
def _catalog(rom):
    verify_rom(rom);found={}
    for state in WITNESS_STATES:
        v=source_view(rom,state)
        if v['result']!='actual_JSR_4033C_RTS_to_3D814' or v['final_SP']!=0xFFFFFD00:
            raise ValueError('canonical conditional caller no longer returns')
        for order,event in enumerate(v['source_events']):
            for lane,p in enumerate(event['physical_addresses']):
                if p in SOURCE_POSITIONS and p not in found:
                    if event['PC'] not in ROLES or event['width']!=1:
                        raise ValueError('unrecognized admitted compact sprite source role')
                    found[p]=dict(address=p,state_WORD=state,F320_WORD=0x10,read_PC=event['PC'],
                        source_role=ROLES[event['PC']],read_width=1,source_address=event['address'],
                        bus_address=event['bus_address'],unit_BYTE_lane=lane,source_event_index=order,
                        canonical_read_value=event['value'],true_caller_PC=0x3D810,
                        actual_list_producer=0x4040A,actual_render_JSR=0x40354,
                        actual_return_PC=0x3D814,actual_final_SP=v['final_SP'])
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
    return dict(format=FORMAT,confidence='confirmed_conditional_original_counter_selected_sprite_source_reads',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),source_union_BYTES=EDITABLE_BYTES,
        source_union_sha256=sha(bytes(rom[p] for p in positions)),physical_blocks=PHYSICAL_BLOCKS,
        physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in SOURCE_SPANS],
        raw_baseline=dict(layout_id=LAYOUT_ID,manifest_sha256=LAYOUT_SHA256,raw_BYTES=10182,resources=105),
        source_roles=dict(resource='conditional_compact_sprite_record_components',
            BYTE='full0..255; first80h marker/X,Y,size/attributes,tilelow keepallbits',
            old_neighbors='live wholeimage only; no second physical editing authority',
            zero='actual conditional source reads, not padding or free space'),
        evidence=dict(entry_JSR_PC=0x3D810,entry_target=0x4033C,list_producer=0x4040A,
            list_gate='F320.W AND000F equals0; real31descending X bins/32RAMobjects with activeBIT7',
            original_list='actualLONG writeFF836A and CLRLFF836E before render; no suppliedlist orA6',
            render_JSR_PC=0x40354,old_helper_gate='813E.W1 bypasses40C94 by originalBNE40452',
            input_full_WORD='live8(A6).W ASL.W2 wraps toWORD; never catalog-clamped',
            counter='4049A liveF320.W0010→LSR.W3→ANDI.W0003 produces2',
            pointer='404AA LONG404D4+s16(ASL.W2(live404CC BYTE+ASL.W2(state)+counter))',
            attribute='404C4 WORD407D4+s16(ASL.W1(same intermediateindex))',
            source='404C8 originaltailJMP3B13C; F300 BYTE unsigned50h capacity, signedX clip, first80h',
            read_order='X(+0),Y(+3),size(+1),repeatedattribute(+1),tilelow(+2); thenA0+=4',
            original_return='3B23A RTS40358; originalMOVEM restoreA5;40364 BEQ40408 RTS3D814/SPFFFFFD00',
            witness_states=list(WITNESS_STATES),original_whole_controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES]),
        conditional_frame='zero64KiB+816A.W8000/813E.W1/F320.W0010/8172.Winput;D/A0exceptSPFFFFFD00;SR2500/CCR0',
        canonical_scope=dict(BYTEs=195,bankC=0,bankF=195,Ffront=179,Ftail=16,baseline_raw_subset=True),
        unknowns=['natural completeRAM frame','natural fullWORD actorstate','allocation/asset owner',
            'earlier3D810 battle/UI closure','edited gameplay safety','original hardware equivalence'],
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
    fixed=metadata(rom);keys(fields,set(fixed)|{'source_BYTEs'},'counter-selected source package')
    for k,v in fixed.items():same(fields[k],v,'package.'+k)
    values={}
    for expected,row in zip(_catalog(rom),exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'source BYTEs')):
        keys(row,set(_fixed(expected))|{'BYTE'},'source component')
        for k,v in _fixed(expected).items():same(row[k],v,'source.'+k)
        values[expected['address']]=uint(row['BYTE'],255,'full source BYTE')
    return [dict(id=f'rom_{a:06X}_counter_selected_source_BYTEs',start=a,end=z,
        data=bytes(values[p] for p in range(a,z)),role='conditional_counter_selected_compact_sprite_source_BYTEs')
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
        description='195 unique physical conditional source BYTEs; witness catalog is not a CPU selector clamp.')


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('wholeROM serialized roundtrip differs')
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema(rom)),
        'validation.json':dump(dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
            whole_ROM_sha256=sha(image),canonical_BYTE_witnesses=list(_catalog(rom)),
            limitations=['CompleteconditionalinitialRAM, notnaturalproducer/owner.',
                'Sharedoriginaloperandengine; noindependentCPU/fullgameplayclaim.',
                'Alloldpointer/attribute/sourceBYTEneighborslive; editscanstoporchangeconsumption.']))}
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
        if not path.is_dir() or {p.name for p in path.iterdir()}!=MEMBERS:raise ValueError('exactfourmembers required')
        for name,data in render_bundle(rom).items():
            if read_bounded(path/name,MAX_JSON)!=data:raise ValueError('bundle drift:'+name)
        result=dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:put(target,image)
        result=dict(exact_canonical=image==rom,sha256=sha(image),editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
