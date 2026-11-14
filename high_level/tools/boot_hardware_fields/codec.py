"""70 original WORD/LONG/BYTE initialization sources at fixed A5 read sites.

The intervening38-BYTE startup Z80 program is explicitly excluded. All source
bits are editable; previews do not execute hardware or prove edited boot safety.
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
OUTPUT_ROOT=ROOT/'build/boot_hardware_fields'
FORMAL_ROOT=ROOT/'analysis/boot_hardware_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
FORMAT='g5510-fixed-boot-hardware-source-fields-v1'
EDITABLE_BYTES=70
MAX_JSON=1024*1024
MEMBERS=frozenset(('fields.json','fields.schema.json','validation.json','manifest.json'))
CONSUMER_START,CONSUMER_END=0x200,0x294
CONSUMER_SHA256=reference_value(__name__, 'CONSUMER_SHA256')
ENHANCED_PATH='analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv'
ENHANCED_SHA256=reference_value(__name__, 'ENHANCED_SHA256')
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH='build/direct_code/layout/'+LAYOUT_ID+'/m68k_bank00.s'
LAYOUT_SHA256=reference_value(__name__, 'LAYOUT_SHA256')
INSTRUCTIONS=(
    (0x206,'4ab900a10008'),(0x20C,'6606'),(0x20E,'4a7900a1000c'),(0x214,'667c'),
    (0x216,'4bfa007c'),(0x21A,'4c9d00e0'),(0x21E,'4cdd1f00'),
    (0x23C,'7217'),(0x23E,'1a1d'),(0x240,'3885'),(0x242,'da47'),(0x244,'51c9fff8'),
    (0x248,'289d'),(0x254,'7425'),(0x256,'10dd'),(0x258,'51cafffc'),
    (0x268,'289d'),(0x26A,'289d'),(0x274,'289d'),
    (0x27E,'7a03'),(0x280,'175d0011'),(0x284,'51cdfffa'),(0x292,'606c'),
)
PACKETS=(
    ('seed_WORDs',0x294,0x29A,'boot_MOVEM_WORD_register_seeds'),
    ('address_register_LONGs',0x29A,0x2AE,'boot_MOVEM_LONG_hardware_addresses'),
    ('vdp_register_payload_BYTEs',0x2AE,0x2C6,'boot_full_BYTE_VDP_register_sources'),
    ('initial_vdp_control_LONG',0x2C6,0x2CA,'boot_full_LONG_VDP_control_source'),
    ('later_vdp_control_LONGs',0x2F0,0x2FC,'boot_three_full_LONG_VDP_control_sources'),
    ('psg_source_BYTEs',0x2FC,0x300,'boot_four_full_BYTE_PSG_sources'),
)
sha,dump=shared.sha,shared.dump
keys,same,uint,exact_list=shared.keys,shared.same,shared.uint,shared.exact_list
load_fields,safe_path=shared.load_fields,shared.safe_path
read_bounded,put=shared.read_bounded,shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE or sha(rom)!=ROM_SHA256:
        raise ValueError('canonical ROM bytes, size and SHA required')
    if sha(rom[CONSUMER_START:CONSUMER_END])!=CONSUMER_SHA256:
        raise ValueError('pinned original boot consumer differs')
    for PC,raw in INSTRUCTIONS:
        if rom[PC:PC+len(raw)//2].hex()!=raw:raise ValueError('pinned boot source read instruction differs')


def metadata():
    return dict(format=FORMAT,confidence='candidate',source_confidence='confirmed',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        evidence=dict(source='fixed original A5 postincrement reads, explicit MOVEM widths and DBRA counts',
            consumer=dict(start=CONSUMER_START,end=CONSUMER_END,bytes=148,sha256=CONSUMER_SHA256),
            older_ledger=dict(path=ENHANCED_PATH,sha256=ENHANCED_SHA256,read_site_confidence='confirmed'),
            instructions=[dict(PC=pc,bytes=raw) for pc,raw in INSTRUCTIONS],
            frozen_raw_layout=dict(id=LAYOUT_ID,path=LAYOUT_PATH,sha256=LAYOUT_SHA256,
                all_emitted_bytes_raw=True,old_typed_overlap_bytes=0),
            initialization_gate=dict(start=0x206,end=0x216,may_branch_over_sources=True,
                hardware_read_conditions_not_modeled=True,source_path_entry=0x216),
            A5_read_sequence=[
                dict(PC=0x21A,width_BITS=16,count=3,start=0x294,end=0x29A,kind='MOVEM.W D5-D7'),
                dict(PC=0x21E,width_BITS=32,count=5,start=0x29A,end=0x2AE,kind='MOVEM.L A0-A4'),
                dict(PC=0x23E,width_BITS=8,count=24,start=0x2AE,end=0x2C6,kind='VDP register source BYTEs'),
                dict(PC=0x248,width_BITS=32,count=1,start=0x2C6,end=0x2CA,kind='VDP control source LONG'),
                dict(PC=0x256,width_BITS=8,count=38,start=0x2CA,end=0x2F0,kind='startup Z80 program copy, excluded'),
                dict(PC=0x268,width_BITS=32,count=1,start=0x2F0,end=0x2F4,kind='VDP control source LONG'),
                dict(PC=0x26A,width_BITS=32,count=1,start=0x2F4,end=0x2F8,kind='VDP control source LONG'),
                dict(PC=0x274,width_BITS=32,count=1,start=0x2F8,end=0x2FC,kind='VDP control source LONG'),
                dict(PC=0x280,width_BITS=8,count=4,start=0x2FC,end=0x300,kind='PSG source BYTEs')],
            seed_rule='MOVEM.W source WORDs sign-extend into D5-D7; full original source WORD remains authority',
            vdp_register_rule='MOVE.B replaces D5 low BYTE, retaining high WORD BYTE; output WORD then ADD.W D7 with16-bit wrap',
            vdp_source_count_rule='MOVEQ23 D1 then DBRA gives24 BYTEs',
            psg_source_count_rule='MOVEQ3 D5 then DBRA gives4 BYTEs',
            address_roles=dict(A0='original Z80 copy destination',A1='original bus request address',
                A2='original Z80 reset address',A3='original VDP data base and PSG base+11',A4='original VDP control address')),
        excluded_program_source=dict(start=0x2CA,end=0x2F0,bytes=38,emitted=False,
            classification='real separately loaded Z80 startup program, not opaque hardware data',
            Z80_destination_original_start=0,Z80_destination_original_end=38,padding_claim=False),
        editor_policy=dict(fixed_physical_source_extents=True,seed_WORD_range=[0,65535],
            address_and_control_LONG_range=[0,0xFFFFFFFF],VDP_and_PSG_BYTE_range=[0,255],
            hardware_addresses_not_clamped=True,payload_BITS_not_normalized=True,
            diagnostics_read_edited_image=True),
        initialization_hardware_state='unknown',edited_boot_safety='unknown',hardware_effects='unknown',
        independent_CPU_comparison=False,source_projection_not_CPU=True,padding_claim=False)


def fixed_packet(name,start,end,role):
    return dict(id=f'rom_{start:06X}_{name}',start=start,end=end,source_role=role)


def pinned(value,fixed,mutable,label):
    keys(value,set(fixed)|set(mutable),label)
    for key,expected in fixed.items():same(value[key],expected,label+'.'+key)


def source_view(image):
    """Live source decoding and narrow register-WORD preview, not boot execution."""
    if type(image) is not bytes or len(image)!=ROM_SIZE:raise ValueError('complete bytes image required')
    seeds={name:int.from_bytes(image[0x294+2*i:0x296+2*i],'big') for i,name in enumerate(('D5','D6','D7'))}
    payload=list(image[0x2AE:0x2C6]);words=[];d5=seeds['D5']
    for value in payload:
        d5=(d5&0xFF00)|value;words.append(d5);d5=(d5+seeds['D7'])&65535
    return dict(seed_WORDs=seeds,seed_LONGs_after_MOVEM_WORD={k:v|(0xFFFF0000 if v&0x8000 else 0) for k,v in seeds.items()},
        address_register_LONGs={name:int.from_bytes(image[0x29A+4*i:0x29E+4*i],'big') for i,name in enumerate(('A0','A1','A2','A3','A4'))},
        vdp_register_payload_BYTEs=payload,vdp_register_written_WORD_preview=words,
        initial_vdp_control_LONG=int.from_bytes(image[0x2C6:0x2CA],'big'),
        later_vdp_control_LONGs=[int.from_bytes(image[a:a+4],'big') for a in (0x2F0,0x2F4,0x2F8)],
        psg_source_BYTEs=list(image[0x2FC:0x300]),source_projection_not_CPU=True,
        initialization_gate_taken_not_asserted=True,hardware_effects='unknown')


def extract(rom):
    verify_rom(rom);fields=metadata();view=source_view(rom)
    for name,start,end,role in PACKETS:
        fields[name]=dict(**fixed_packet(name,start,end,role),values=view[name])
    return fields


def blocks(rom,fields):
    verify_rom(rom);pinned(fields,metadata(),{p[0] for p in PACKETS},'boot source package');rows=[]
    for name,start,end,role in PACKETS:
        row=fields[name];info=fixed_packet(name,start,end,role);pinned(row,info,{'values'},'fixed boot source packet')
        value=row['values']
        if name=='seed_WORDs':
            keys(value,{'D5','D6','D7'},'fixed MOVEM seed registers')
            data=b''.join(uint(value[k],65535,'seed WORD').to_bytes(2,'big') for k in ('D5','D6','D7'))
        elif name=='address_register_LONGs':
            keys(value,{'A0','A1','A2','A3','A4'},'fixed MOVEM address registers')
            data=b''.join(uint(value[k],0xFFFFFFFF,'full address LONG').to_bytes(4,'big') for k in ('A0','A1','A2','A3','A4'))
        elif name=='initial_vdp_control_LONG':data=uint(value,0xFFFFFFFF,'full VDP control LONG').to_bytes(4,'big')
        elif name=='later_vdp_control_LONGs':data=b''.join(uint(v,0xFFFFFFFF,'full VDP control LONG').to_bytes(4,'big') for v in exact_list(value,3,'three VDP control LONGs'))
        else:
            count=24 if name=='vdp_register_payload_BYTEs' else 4
            data=bytes(uint(v,255,'complete hardware source BYTE') for v in exact_list(value,count,name))
        if len(data)!=end-start:raise ValueError('fixed boot field width differs')
        rows.append(dict(id=info['id'],start=start,end=end,data=data,role=role))
    if sum(len(r['data']) for r in rows)!=70 or any(a['end']>b['start'] for a,b in zip(rows,rows[1:])):
        raise ValueError('fixed70-byte hardware source scope differs')
    return rows


def rebuild(rom,fields):
    rows=blocks(rom,fields);image=bytearray(rom)
    for row in rows:image[row['start']:row['end']]=row['data']
    return bytes(image)


def schema():
    def obj(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def exact(items):return dict(type='array',prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def constant(value):
        if type(value) is dict:return obj({k:constant(v) for k,v in value.items()})
        if type(value) is list:return exact([constant(v) for v in value])
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(value)],const=value)
    def integer(maximum):return dict(type='integer',minimum=0,maximum=maximum)
    def values(count,item):return dict(type='array',minItems=count,maxItems=count,items=item)
    types=dict(seed_WORDs=obj({k:integer(65535) for k in ('D5','D6','D7')}),
        address_register_LONGs=obj({k:integer(0xFFFFFFFF) for k in ('A0','A1','A2','A3','A4')}),
        vdp_register_payload_BYTEs=values(24,integer(255)),initial_vdp_control_LONG=integer(0xFFFFFFFF),
        later_vdp_control_LONGs=values(3,integer(0xFFFFFFFF)),psg_source_BYTEs=values(4,integer(255)))
    properties={k:constant(v) for k,v in metadata().items()}
    for name,start,end,role in PACKETS:
        properties[name]=obj({**{k:constant(v) for k,v in fixed_packet(name,start,end,role).items()},'values':types[name]})
    result=obj(properties);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='70 fixed boot hardware WORD/LONG/BYTE sources; all original bits retained. The38-BYTE startup Z80 program is excluded, not disguised as opaque data.'
    return result


def render_bundle(rom):
    fields=extract(rom);serialized=dump(fields);image=rebuild(rom,load_fields(serialized))
    if image!=rom:raise ValueError('serialized whole-ROM boot source roundtrip differs')
    rows=blocks(rom,fields)
    report=dict(**metadata(),editable_bytes=70,physical_blocks=6,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        source_union_sha256=sha(b''.join(row['data'] for row in rows)),source_preview_is_editor_authority=False,
        original_source_preview=source_view(rom),
        blocks=[{k:v for k,v in row.items() if k!='data'}|dict(bytes=len(row['data']),sha256=sha(row['data'])) for row in rows])
    members={'fields.json':serialized,'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=70,physical_blocks=6,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError('output must stay in boot hardware fields build scope or exact formal bundle')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'));parser.add_argument('--rom',default=str(DEFAULT_ROM))
    parser.add_argument('--fields');parser.add_argument('--bundle');parser.add_argument('--output')
    args=parser.parse_args(argv);target=None
    if args.command=='export':
        if args.output is None or args.fields is not None or args.bundle is not None:raise ValueError('export requires fresh output only')
        target=fresh_output(args.output,bundle=True)
    elif args.command=='import':
        if args.output is None or args.bundle is not None:raise ValueError('import requires fields and fresh output')
        target=fresh_output(args.output)
        if target.suffix.lower()!='.bin':raise ValueError('fresh .bin output required')
    elif args.output is not None or (args.fields is not None and args.bundle is not None):raise ValueError('verify accepts fields or bundle and writes nothing')
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=70,members={name:sha(data) for name,data in members.items()})
    elif args.command=='verify' and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS:raise ValueError('exact four-member bundle required')
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data:raise ValueError('canonical bundle drift: '+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=70,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON));image=rebuild(rom,fields)
        if target is not None:put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=70,bytes=len(image),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
