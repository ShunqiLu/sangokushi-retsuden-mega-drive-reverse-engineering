"""16 physical BYTEs read by original duel-record WORD-indexed source paths.

Natural action writers cover class 0/1/2. The fourth class BYTE and six WORDs
have conditional witnesses, not a claim that the natural game selects them.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared

ROOT=Path(__file__).resolve().parents[2]
ROM_SIZE=0x100000
ROM_SHA256=reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM=ROOT.parent/'work/original_g5510.bin'
OUTPUT_ROOT=ROOT/'build/duel_record_source_alias_fields'
FORMAL_ROOT=ROOT/'analysis/duel_record_source_alias_fields/generated'
DEFAULT_BUNDLE=FORMAL_ROOT
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
FORMAT="g5510-duel-record-conditional-indexed-source-BYTE-fields-v1"
EDITABLE_BYTES=16
MAX_JSON=1024*1024
MEMBERS=frozenset(('fields.json','fields.schema.json','validation.json','manifest.json'))
RANGES=((0x28D62,0x28D6E,reference_value(__name__, 'RANGES')),
    (0x28F8C,0x28F90,reference_value(__name__, 'RANGES_2')))
SOURCE_SHA256=reference_value(__name__, 'SOURCE_SHA256')
SPATIAL_CODE_SHA256=reference_value(__name__, 'SPATIAL_CODE_SHA256')
CONSUMERS=((0x27368,0x273C4,reference_value(__name__, 'CONSUMERS')),
    (0x26E4E,0x26E96,reference_value(__name__, 'CONSUMERS_2')),
    (0x27BCC,0x27C7C,reference_value(__name__, 'CONSUMERS_3')),
    (0x28B9A,0x28D32,reference_value(__name__, 'CONSUMERS_4')),
    (0x28D74,0x28F8C,reference_value(__name__, 'CONSUMERS_5')),
    (0x28F90,0x29038,reference_value(__name__, 'CONSUMERS_6')),
    (0x2A22E,0x2A26C,reference_value(__name__, 'CONSUMERS_7')))
# Diagnostic-only controls: no new editable source or serialized authority.
# Each exclusive end follows its original RTS; 27A3A starts a different leaf.
EXTERNAL_HELPER_CONTROLS=((0x808A,0x80D0,reference_value(__name__, 'EXTERNAL_HELPER_CONTROLS')),
    (0x83D4,0x83FA,reference_value(__name__, 'EXTERNAL_HELPER_CONTROLS_2')),
    (0x279E6,0x27A10,reference_value(__name__, 'EXTERNAL_HELPER_CONTROLS_3')),
    (0x27A10,0x27A3A,reference_value(__name__, 'EXTERNAL_HELPER_CONTROLS_4')))
INSTRUCTIONS=((0x27392,'61001806'),(0x273C0,'610017d8'),
    (0x27BDC,'317c0002000c'),(0x27C38,'317c0000000c'),(0x27C4E,'317c0001000c'),(0x27C6C,'317c0002000c'),
    (0x26E54,'383900ff706a'),(0x26E5A,'c8fc0003'),(0x26E5E,'dac4'),
    (0x26E60,'13dd00ff707b'),(0x26E66,'13dd00ff707d'),(0x26E6C,'13d500ff707f'),
    (0x26E84,'13dd00ff70cb'),(0x26E8A,'13dd00ff70cd'),(0x26E90,'13d500ff70cf'),
    (0x28BF6,'4a680002'),(0x28BFA,'6b4c'),(0x28C48,'30280004'),
    (0x28C4C,'4a680008'),(0x28C54,'0c400004'),(0x28C5C,'610015d0'),(0x28C60,'64000112'),
    (0x28C64,'082900060002'),(0x28C6A,'672a'),(0x28CC6,'610002c8'),
    (0x28D00,'3428002e'),(0x28D04,'e342'),(0x28D06,'d07b2052'),
    (0x28E76,'4a68001c'),(0x28E7C,'600000d2'),(0x28F54,'3028000c'),
    (0x28F58,'143b0032'),(0x28F5C,'024200ff'),(0x28F80,'6100001a'),
    (0x28FAA,'e542'),(0x28FAC,'22712000'),(0x2A234,'343b102a'),(0x2A25A,'947b100a'))
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH='build/direct_code/layout/'+LAYOUT_ID+'/m68k_bank02.s'
LAYOUT_SHA256=reference_value(__name__, 'LAYOUT_SHA256')
MAP_PATH='analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv'
MAP_SHA256=reference_value(__name__, 'MAP_SHA256')
OLD_EVIDENCE=(('tools/duel_flow/duel_flow.py',reference_value(__name__, 'OLD_EVIDENCE')),
    ('analysis/duel_flow/DUEL_FLOW.md',reference_value(__name__, 'OLD_EVIDENCE_2')))
sha,dump=shared.sha,shared.dump
keys,same,uint,exact_list=shared.keys,shared.same,shared.uint,shared.exact_list
load_fields=shared.load_fields
safe_path,read_bounded,put=shared.safe_path,shared.read_bounded,shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE or sha(rom)!=ROM_SHA256:
        raise ValueError('canonical complete ROM bytes, size and SHA-256 required')
    for a,z,h in (*CONSUMERS,*EXTERNAL_HELPER_CONTROLS,*RANGES):
        if sha(rom[a:z])!=h:
            raise ValueError('original producer/caller/reader/source pin differs')


def _image(image):
    if type(image) is not bytes or len(image)!=ROM_SIZE:
        raise ValueError('diagnostic requires complete bytes image; edited images are allowed')


def _gate_control_contract(image):
    for a,z,h in (*CONSUMERS,*EXTERNAL_HELPER_CONTROLS):
        if a==0x2A22E:
            z,h=0x2A260,SPATIAL_CODE_SHA256  # The last 12 BYTEs are live old data, not controls.
        if sha(image[a:z])!=h:
            raise ValueError('original control bytes changed; conditional frame/damage reachability is not proven')


def _s16(word):
    return word if word<0x8000 else word-65536


def _inside(address):
    return any(a<=address<z for a,z,_ in RANGES)


def index_WORD_from_BYTE(source_BYTE,preserved_high_BYTE):
    low=uint(source_BYTE,255,'complete EA88 producer BYTE')
    high=uint(preserved_high_BYTE,255,'unchanged destination WORD high BYTE')
    return (high<<8)|low


def producer_RAM_start(officer_WORD):
    value=uint(officer_WORD,65535,'complete original officer WORD')
    return 0xFFEA88+_s16((value*3)&65535)


def bonus_lookup(image,action_class_WORD,index_WORD):
    """One original ADD.W source read; no table-domain or stat normalization."""
    _image(image)
    action=uint(action_class_WORD,65535,'complete record action class WORD')
    index=uint(index_WORD,65535,'complete record bonus index WORD')
    if action==0:
        base,PC,field=0x28D4A,0x28CE2,0x2C
    elif action==1:
        base,PC,field=0x28D52,0x28CF8,0x2A
    else:
        base,PC,field=0x28D5A,0x28D06,0x2E
    shifted=(index<<1)&65535
    address=base+_s16(shifted)
    data=image[address:address+2]
    return dict(action_class_WORD=action,index_WORD=index,record_field_offset=field,
        base=base,source_PC=PC,shifted_offset_WORD=shifted,signed_offset=_s16(shifted),
        address=address,end=address+2,source_BYTEs=list(data),source_WORD=int.from_bytes(data,'big'),
        editable_BYTE_mask=[_inside(address),_inside(address+1)],
        physical_catalog_CPU_clamp=False,diagnostic_is_complete_CPU=False)


def class_lookup(image,record_class_WORD):
    """Original zero-HP BYTE read and subsequent live BE32 directory read only.

The actual frame records/output renderer and object state gates are not emulated.
FF is source data, not an invented table terminator or host rejection.
"""
    _image(image)
    value=uint(record_class_WORD,65535,'complete original record class WORD')
    address=0x28F8C+_s16(value)
    byte=image[address]
    offset=(byte<<2)&65535
    pointer_address=0x29038+_s16(offset)
    return dict(record_class_WORD=value,address=address,end=address+1,source_PC=0x28F58,
        source_BYTE=byte,AND_WORD=byte,editable_source=_inside(address),
        frame_BSR_PC=0x28F80,frame_directory_READ_PC=0x28FAC,
        frame_directory_offset_WORD=offset,frame_pointer_address=pointer_address,
        frame_pointer_BE32=int.from_bytes(image[pointer_address:pointer_address+4],'big'),
        frame_pointer_read_BYTES=4,frame_pointer_is_not_executed=True,
        requires_record_HP_WORD_zero=True,requires_record_flag3_clear=True,
        physical_catalog_CPU_clamp=False,diagnostic_is_complete_CPU=False)


def damage_gate_witness(image,index_BYTE,preserved_high_BYTE=0):
    """Conditional prefix with original controls, not whole CPU execution.

The fixed witness assumes the 808A hardware acknowledgement BIT0 read is 0
(otherwise its original wait loop has not returned) and F61C seed 76A263E7,
whose original 83D4 calculation returns D0.W=0. Neither hardware progress nor
natural RAM/seed reachability is established by this source diagnostic.
"""
    _image(image)
    _gate_control_contract(image)
    word=index_WORD_from_BYTE(index_BYTE,preserved_high_BYTE)
    center=int.from_bytes(image[0x2A264:0x2A266],'big')
    radius=int.from_bytes(image[0x2A26A:0x2A26C],'big')
    # Original class2 tables: direction bit3=1, own x=0, target x=center.
    distance=abs(_s16((center+0-center)&65535))
    spatial_passes=distance<radius
    thresholds=[int.from_bytes(image[a:a+2],'big') for a in range(0x28D32,0x28D3E,2)]
    normal_offset=next((i*2 for i,value in enumerate(thresholds) if 1<value),None)
    # Only prove an in-table return. Failure of this proof is not a CPU stop:
    # original postincrement scanning continues into live neighboring source.
    passes=spatial_passes and normal_offset is not None
    return dict(caller_PCs=[0x27392,0x273C0],callee=0x28B9A,
        source_record_fixed_RAM=0xFF7050,alternate_record_RAM=0xFF70A0,
        source_state_WORD=0x8000,source_frame_WORD=4,source_timer8_WORD=0,
        source_action_class_WORD=2,source_direction_WORD=0x0800,source_x_WORD=0,target_x_WORD=center,
        target_state_WORD=0,source_HP_WORD=1,source_primary_WORD=1,
        source_index_producer_BYTE=index_BYTE,preserved_record_index_high_BYTE=preserved_high_BYTE,
        resulting_index_WORD=word,spatial_BSR_PC=0x28C5C,spatial_callee=0x2A22E,
        spatial_distance_WORD=distance,spatial_radius_WORD=radius,
        spatial_SUB_WORD_CARRY=spatial_passes,block_branch_28C60_taken=not spatial_passes,
        target_flag6_is_clear=True,primary1_threshold_helper_returns_normally=normal_offset is not None,
        threshold_helper_offset_WORD=normal_offset,
        no_in_table_threshold_return_means_outside_proof_not_CPU_stop=True,
        assumed_supplied_RNG_WORD=0,RNG_natural_distribution='unknown',
        conditional_prefix_reaches_bonus_read=False if not spatial_passes else True if passes else None,
        source=bonus_lookup(image,2,word) if passes else None,natural_state_reachability='unknown',
        independent_CPU_comparison=False,diagnostic_is_complete_CPU=False)


def source_fixed(a,z):
    return dict(id=f'rom_{a:06X}_duel_record_source_BYTEs',start=a,end=z,bytes=z-a)


def witnesses_for_source(address):
    address=uint(address,ROM_SIZE-1,'physical source BYTE address')
    if 0x28D62<=address<0x28D6E:
        slot=(address-0x28D62)//2
        return dict(kind='bonus_WORD',action_class_WORD=2,index_WORD=4+slot,
            producer_source_BYTE=4+slot,preserved_high_BYTE=0,
            WORD_address=0x28D62+slot*2,BYTE_in_WORD=(address-0x28D62)%2,
            natural_selection='unknown')
    if 0x28F8C<=address<0x28F90:
        value=address-0x28F8C
        return dict(kind='class_BYTE',record_class_WORD=value,source_address=address,
            natural_writer_present=value<3,conditional_witness=True,natural_complete_domain='unknown')
    raise ValueError('address outside the unique 16 physical source BYTEs')


def metadata():
    return dict(format=FORMAT,source_confidence='confirmed',confidence='candidate',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        physical_scope=[dict(**source_fixed(a,z),source_sha256=h) for a,z,h in RANGES],
        source_union_BYTES=16,source_union_sha256=SOURCE_SHA256,
        serialization='physical full BYTE sole authority; complete bonus WORD and frame LONG views are read-only',
        evidence=dict(original_envelopes=[dict(start=a,end=z,bytes=z-a,sha256=h) for a,z,h in CONSUMERS],
            instructions=[dict(address=a,bytes=b) for a,b in INSTRUCTIONS],
            original_map=dict(path=MAP_PATH,sha256=MAP_SHA256),
            frozen_raw_layout=dict(id=LAYOUT_ID,path=LAYOUT_PATH,sha256=LAYOUT_SHA256,
                snapshot_resources=93,snapshot_raw_BYTES=24594,raw_difference_BYTES=16,typed_overlap_emitted_BYTES=0),
            old_evidence=[dict(path=p,sha256=h) for p,h in OLD_EVIDENCE],
            bonus_producer=dict(entry=0x26E4E,base_RAM=0xFFEA88,officer_WORD_reads=[0x26E54,0x26E78],
                address_formula='FFEA88 + s16((officer_WORD * 3) & FFFF)',
                source_BYTE_domain=[0,255],WORD_high_BYTE_preserved=True,
                record_low_BYTE_offsets=[0x2B,0x2D,0x2F],record_WORD_offsets=[0x2A,0x2C,0x2E],
                first_low_BYTE_destinations=[0xFF707B,0xFF707D,0xFF707F],
                second_low_BYTE_destinations=[0xFF70CB,0xFF70CD,0xFF70CF],
                no_consumer_index_mask_or_catalog_clamp=True,natural_EA88_content_domain='unknown'),
            bonus_reader=dict(class0=dict(base=0x28D4A,field=0x2C,PC=0x28CE2),
                class1=dict(base=0x28D52,field=0x2A,PC=0x28CF8),
                other=dict(base=0x28D5A,field=0x2E,PC=0x28D06),
                source_WORD_read_BYTES=2,index_formula='base + s16((record_index_WORD << 1) & FFFF)',
                source_WORD_all_bits_preserved=True,original_new_WORDs=[0,44,0,42,0,46],
                source_is_not_padding=True,old_verified_index_domain=[0,3],old_normal_domain_not_changed=True,
                other_class_conditional_indices=[4,5,6,7,8,9]),
            damage_prefix_gate=dict(true_callers=[0x27392,0x273C0],entry=0x28B9A,
                state_sign_test=0x28BF6,state_negative_skips_input_rewrite=True,frame_compare=0x28C54,
                required_frame_WORD=4,required_timer8_WORD=0,spatial_BSR=0x28C5C,spatial_callee=0x2A22E,
                required_spatial_CARRY=True,target_bit6_test=0x28C64,target_bit6_clear_bypasses_block=True,
                constructed_action_class_WORD=2,constructed_primary_WORD=1,
                helper_primary1_returns_inside_original_thresholds=True,
                complete_movement_damage_state_algorithm=False,natural_frame_reachability='unknown'),
            class_reader=dict(source_base=0x28F8C,input_field_WORD=0x0C,source_PC=0x28F58,
                input_formula='28F8C + s16(record_class_WORD)',source_BYTE_read_BYTES=1,
                HP_zero_test=0x28E76,true_zero_HP_branch=0x28E7C,flag3_clear_required=True,
                ANDI_WORD=0x28F5C,frame_BSR=0x28F80,frame_entry=0x28F9C,
                frame_directory_base=0x29038,frame_directory_shift_PC=0x28FAA,
                frame_directory_read_PC=0x28FAC,frame_directory_read_BYTES=4,big_endian_LONG=True,
                original_source_BYTEs=[0x44,0x45,0x46,0xFF],BYTE_FF_is_not_source_terminator=True,
                known_natural_writer_values=[0,1,2],conditional_class3_not_new_natural_class=True,
                natural_writers=[dict(PC=p,value=v) for p,v in ((0x27BDC,2),(0x27C38,0),(0x27C4E,1),(0x27C6C,2))],
                physical_catalog_not_CPU_clamp=True,frame_objects_not_emitted=True),
            per_BYTE_witnesses=[dict(address=a,**witnesses_for_source(a)) for s,e,_ in RANGES for a in range(s,e)],
            edited_image_live_neighbors=True,no_typed_neighbor_original_value_replacement=True,
            excluded_BE93A_BE95A_BYTES=32,excluded_BE_source_evidence='unknown'),
        natural_selection='unknown',bonus_business_identity='unknown',class3_business_identity='unknown',
        complete_duel_algorithm=False,independent_CPU_comparison=False)


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),sources=[dict(**source_fixed(a,z),source_BYTEs=list(rom[a:z])) for a,z,_ in RANGES])


def blocks(rom,fields):
    verify_rom(rom)
    fixed=metadata()
    keys(fields,set(fixed)|{'sources'},'conditional duel record source fields')
    for key,value in fixed.items():same(fields[key],value,'fixed fields.'+key)
    result=[]
    for row,(a,z,_) in zip(exact_list(fields['sources'],2,'fixed physical source count'),RANGES):
        expected=source_fixed(a,z)
        keys(row,set(expected)|{'source_BYTEs'},'fixed source')
        for key,value in expected.items():same(row[key],value,'fixed source.'+key)
        data=bytes(uint(v,255,'full source BYTE') for v in exact_list(row['source_BYTEs'],z-a,'fixed source BYTE count'))
        result.append(dict(id=expected['id'],start=a,end=z,data=data,
            role='conditional_duel_record_WORD_indexed_source_BYTE_alias'))
    if sum(len(row['data']) for row in result)!=EDITABLE_BYTES:raise ValueError('fixed source cost differs')
    return result


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def schema():
    def obj(properties):
        return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def fixed(value):
        if type(value) is dict:return obj({k:fixed(v) for k,v in value.items()})
        if type(value) is list:return dict(type='array',prefixItems=[fixed(v) for v in value],items=False,minItems=len(value),maxItems=len(value))
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(value)],const=value)
    rows=[obj({**{k:fixed(v) for k,v in source_fixed(a,z).items()},
        'source_BYTEs':dict(type='array',minItems=z-a,maxItems=z-a,items=dict(type='integer',minimum=0,maximum=255))}) for a,z,_ in RANGES]
    result=obj({**{k:fixed(v) for k,v in metadata().items()},
        'sources':dict(type='array',prefixItems=rows,items=False,minItems=2,maxItems=2)})
    result['$schema']='https://json-schema.org/draft/2020-12/schema'
    return result


def render_bundle(rom):
    fields=extract(rom); serialized=dump(fields)
    image=rebuild(rom,load_fields(serialized))
    if image!=rom:raise ValueError('serialized complete ROM roundtrip differs')
    encoded=blocks(rom,fields)
    report=dict(**metadata(),editable_bytes=16,physical_blocks=2,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        bonus_conditional_gate_witnesses=[damage_gate_witness(rom,v) for v in range(4,10)],
        class_read_witnesses=[class_lookup(rom,v) for v in range(4)],
        retained_high_BYTE_example=damage_gate_witness(rom,4,0x80),
        signed_and_code_alias_examples=dict(bonus=[bonus_lookup(rom,2,v) for v in (0x8000,0xFFFF,0x000C)],
            class_BYTE=[class_lookup(rom,v) for v in (4,0xFFFF,0x8000)]),
        all16_physical_BYTES_witnessed=True,
        blocks=[{k:v for k,v in row.items() if k!='data'}|dict(bytes=len(row['data']),sha256=sha(row['data'])) for row in encoded])
    members={'fields.json':serialized,'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=16,physical_blocks=2,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not(path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not(bundle and path==FORMAL_ROOT):
        raise ValueError('fresh output must stay in scoped duel record build or exact formal bundle')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields');p.add_argument('--bundle');p.add_argument('--output')
    args=p.parse_args(argv);target=None
    if args.command=='export':
        if args.output is None or args.fields is not None or args.bundle is not None:raise ValueError('export requires fresh output only')
        target=fresh_output(args.output,bundle=True)
    elif args.command=='import':
        if args.output is None or args.bundle is not None:raise ValueError('import requires fields and fresh output')
        target=fresh_output(args.output)
        if target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
    elif args.output is not None or(args.fields is not None and args.bundle is not None):raise ValueError('verify accepts fields or bundle without writes')
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=16,members={name:sha(data) for name,data in members.items()})
    elif args.command=='verify' and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS:raise ValueError('exact four-member bundle required')
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data:raise ValueError('canonical bundle drift: '+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=16,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON));image=rebuild(rom,fields)
        if target is not None:put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=16,bytes=len(image),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True))
    return 0
