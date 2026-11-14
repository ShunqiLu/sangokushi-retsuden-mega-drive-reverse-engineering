"""Sealed probable 01A9B0 sixth mnemonic source; only new182 instructions /622 original B.

The normal inventory/load/source/image APIs never decode, regenerate a fallback
or read/reset older editable assembly. Explicit canonical exports alone admit
raw opcode lengths and Capstone spellings. No consumer, oracle, GNU or CPU is
implemented here. All paths remain configurable; product promotion adds no semantic ownership.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import csv
from dataclasses import dataclass
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.graphics_build import graphics_build as gb

SOURCE=ROOT/'src/m68k/candidate_handler_9b0.s'
GENERATED=ROOT/'analysis/candidate_handler_9b0_source/generated'
LEDGER=GENERATED/'instructions.csv'
ENHANCED=ROOT/'analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv'
ENHANCED_SHA=reference_value(__name__, 'ENHANCED_SHA')
LEDGER_SHA=reference_value(__name__, 'LEDGER_SHA')
ROM_SHA=reference_value(__name__, 'ROM_SHA')
SPANS=((0x1A9B0,0x1AC1E,182,reference_value(__name__, 'SPANS')),)
EXCLUDED_TABLES=((0x1A1DC,0x1A200),(0x1A492,0x1A49E),(0x1A808,0x1A818))
UNKNOWN_NEIGHBOURS=((0x1A9AA,0x1A9B0,reference_value(__name__, 'UNKNOWN_NEIGHBOURS')),
                    (0x1AC1E,0x1AC26,reference_value(__name__, 'UNKNOWN_NEIGHBOURS_2')))
REUSED_CODE=((0x83D4,0x83FA,15,38,'src/m68k/candidate_action.s'),
             (0x1A438,0x1A44E,7,22,'src/m68k/candidate_handler_49e.s'),
             (0x1A44E,0x1A47A,15,44,'src/m68k/candidate_filter.s'),
             (0x1A706,0x1A808,83,258,'src/m68k/candidate_handler_818.s'))
REUSED_RNG=(0x83D4,0x83FA)
PRIOR_LEDGERS=(
    ('analysis/m68k_build/generated/instructions.csv',reference_value(__name__, 'PRIOR_LEDGERS'),11671,42752),
    ('analysis/candidate_source/generated/instructions.csv',reference_value(__name__, 'PRIOR_LEDGERS_2'),184,624),
    ('analysis/candidate_action_source/generated/instructions.csv',reference_value(__name__, 'PRIOR_LEDGERS_3'),241,910),
    ('analysis/candidate_handler_source/generated/instructions.csv',reference_value(__name__, 'PRIOR_LEDGERS_4'),196,660),
    ('analysis/candidate_handler_49e_source/generated/instructions.csv',reference_value(__name__, 'PRIOR_LEDGERS_5'),183,638),
)
PRIOR_SOURCE_SEALS=(
    ('src/m68k/recovered_code.s',reference_value(__name__, 'PRIOR_SOURCE_SEALS')),
    ('src/m68k/candidate_filter.s',reference_value(__name__, 'PRIOR_SOURCE_SEALS_2')),
    ('src/m68k/candidate_action.s',reference_value(__name__, 'PRIOR_SOURCE_SEALS_3')),
    ('src/m68k/candidate_handler_818.s',reference_value(__name__, 'PRIOR_SOURCE_SEALS_4')),
    ('src/m68k/candidate_handler_49e.s',reference_value(__name__, 'PRIOR_SOURCE_SEALS_5')),
)
PRIOR_SOURCES=tuple(p for p,_ in PRIOR_SOURCE_SEALS)
FIELDS=('address','size','bytes','original_mnemonic','original_operand','discovery_confidence','decoder_origin','source_confidence','evidence_id')
EVIDENCE='phase28-fixed-handler-9b0-source-draft-v1'
sha,dump=gb.sha,gb.dump

@dataclass(frozen=True)
class Paths:
    project_root:Path=ROOT
    source:Path=SOURCE
    generated:Path=GENERATED
    enhanced:Path=ENHANCED
    @property
    def ledger(self):return self.generated/'instructions.csv'

DEFAULT_PATHS=Paths()
def config(paths):return DEFAULT_PATHS if paths is None else paths
def read(path):return gb.af._read(gb.af.safe_path(path,regular_input=True),16*1024*1024)
def _rows(raw):return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
def verify_rom(rom):
    gb.af.verify_rom(rom)
    for a,z,_,h in SPANS:
        if sha(rom[a:z])!=h:raise ValueError('handler9b0 original-code identity changed')
    for a,z,h in UNKNOWN_NEIGHBOURS:
        if sha(rom[a:z])!=h:raise ValueError('unknown neighbouring original bytes changed')
def legacy_map(*,paths=None):
    raw=read(config(paths).enhanced)
    if sha(raw)!=ENHANCED_SHA:raise ValueError('sealed legacy enhanced map changed')
    result={}
    for row in _rows(raw):
        pc=int(row['address'])
        if pc in result:raise ValueError('duplicate legacy instruction start')
        result[pc]=row
    return result
def csv_bytes(records):
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=FIELDS,lineterminator='\n')
    writer.writeheader();writer.writerows(records);return stream.getvalue().encode()

def excluded_coverage(*,paths=None):
    """Only pinned five old ledgers; never inspect global build allocation."""
    p=config(paths);positions=set();by_source={}
    for (name,h,count,width),(source,_) in zip(PRIOR_LEDGERS,PRIOR_SOURCE_SEALS):
        raw=read(p.project_root/name)
        if sha(raw)!=h:raise ValueError('prior compiled instruction ledger changed')
        rows=_rows(raw);covered=[b for r in rows for b in range(int(r['address']),int(r['address'])+int(r['size']))]
        if len(rows)!=count or len(covered)!=len(set(covered)) or len(covered)!=width:raise ValueError('prior compiled allocation changed')
        if positions.intersection(covered):raise ValueError('prior compiled instruction ledgers overlap')
        positions.update(covered);by_source[source]=rows
    if len(positions)!=45584:raise ValueError('five-source baseline byte union changed')
    for a,z,count,width,source in REUSED_CODE:
        rows=[r for r in by_source[source] if a<=int(r['address'])<z]
        if len(rows)!=count or sum(int(r['size']) for r in rows)!=width or not set(range(a,z))<=positions:
            raise ValueError('reused guards are missing from sole prior source')
    for a,z in EXCLUDED_TABLES:positions.update(range(a,z))
    for a,z,_ in UNKNOWN_NEIGHBOURS:positions.update(range(a,z))
    return positions

def validate_records(rom,records,*,paths=None):
    verify_rom(rom)
    if type(records) is not list or len(records)!=182:raise ValueError('handler9b0 instruction count changed')
    previous=legacy_map(paths=paths);covered=[]
    for row in records:
        if type(row) is not dict or set(row)!=set(FIELDS):raise ValueError('handler9b0 provenance fields changed')
        a,size=row['address'],row['size']
        if type(a) is not int or type(size) is not int or a&1 or size not in (2,4,6,8,10) or not any(x<=a and a+size<=z for x,z,_,_ in SPANS):
            raise ValueError('invalid handler9b0 instruction extent')
        if row['bytes']!=rom[a:a+size].hex():raise ValueError('handler9b0 original bytes changed')
        if row['source_confidence']!='probable' or row['evidence_id']!=EVIDENCE or row['decoder_origin']!='phase3-enhanced':raise ValueError('handler9b0 source evidence changed')
        old=previous.get(a)
        if old is None or (int(old['size']),old['bytes'],old['mnemonic'],old['operand'],old['confidence'])!=(size,row['bytes'],row['original_mnemonic'],row['original_operand'],row['discovery_confidence']):
            raise ValueError('handler9b0 sealed old decode provenance changed')
        covered.extend(range(a,a+size))
    expected=[b for a,z,_,_ in SPANS for b in range(a,z)]
    if covered!=expected or len(covered)!=622:raise ValueError('handler9b0 instruction order or coverage changed')
    if set(covered)&excluded_coverage(paths=paths):raise ValueError('handler9b0 overlaps prior source/table/unknown neighbour')
    return dict(selected_instructions=182,selected_code_bytes=622,legacy_decoder_rows=182,new_decoder_rows=0,
                source_confidence='probable',ownership_bytes_added=0,complete_indirect_domains_added=0,
                natural_runtime_observations_added=0,reused_RNG_bytes_not_emitted=38,
                reused_shared_instructions_not_emitted=120,reused_shared_code_bytes_not_emitted=362)
def inventory(rom,*,paths=None):
    raw=read(config(paths).ledger)
    if sha(raw)!=LEDGER_SHA:raise ValueError('handler9b0 ledger changed; independent re-audit required')
    rows=_rows(raw)
    for row in rows:row['address']=int(row['address']);row['size']=int(row['size'])
    return rows,validate_records(rom,rows,paths=paths)
def verify_source(rom,source,*,paths=None):
    from tools.m68k_build.m68k_build import validate_source
    records,info=inventory(rom,paths=paths);return {**info,**validate_source(source,records)}
def load_source(rom,source_path=None,*,paths=None):
    from tools.m68k_build.m68k_build import validate_source
    p=config(paths);records,info=inventory(rom,paths=p);data=read(p.source if source_path is None else source_path)
    return data,records,{**info,**validate_source(data,records)}

def ea_extra(mode,reg,width):
    """Raw base68000 EA extension width; no semantic interpreter is provided."""
    if mode in (0,1,2,3,4):return 0
    if mode in (5,6):return 2
    if mode==7:
        if reg in (0,2,3):return 2
        if reg==1:return 4
        if reg==4:return 4 if width==4 else 2
    raise ValueError('unsupported raw EA encoding')
def raw_shape(word):
    """Independent admission of name/data-width/instruction-length from bits."""
    high,mode,reg=word>>12,(word>>3)&7,word&7
    if high in (1,2,3):
        width={1:1,2:4,3:2}[high];dm,dr=(word>>6)&7,(word>>9)&7
        if dm==1 and width==1:raise ValueError('invalid raw MOVEA.B')
        return ('movea' if dm==1 else 'move'),width,2+ea_extra(mode,reg,width)+ea_extra(dm,dr,width)
    if word==0x4E75:return 'rts',4,2
    if word&0xFFF8==0x4840:return 'swap',4,2
    if word&0xF100==0x7000:return 'moveq',4,2
    if high==6:
        names={0:'bra',1:'bsr',3:'bls',4:'bcc',5:'bcs',6:'bne',7:'beq'}
        if (word>>8)&15 not in names:raise ValueError('unadmitted raw branch condition')
        return names[(word>>8)&15],2,4 if word&255==0 else 2
    if word&0xFFC0==0x4E80:return 'jsr',4,2+ea_extra(mode,reg,4)
    if word&0xF1C0==0x41C0:return 'lea',4,2+ea_extra(mode,reg,4)
    if word in (0x007C,0x027C):return ('ori' if word==0x007C else 'andi'),2,4
    if word&0xFF00 in (0x0200,0x0600,0x0C00):
        width=1<<((word>>6)&3)
        if width not in (1,2,4):raise ValueError('invalid raw immediate width')
        return {2:'andi',6:'addi',12:'cmpi'}[word>>8],width,2+(4 if width==4 else 2)+ea_extra(mode,reg,width)
    if word&0xFF00 in (0x4200,0x4A00):
        width=1<<((word>>6)&3)
        if width not in (1,2,4):raise ValueError('invalid raw unary width')
        return ('clr' if word&0xFF00==0x4200 else 'tst'),width,2+ea_extra(mode,reg,width)
    if high==5 and not word&0x0100:
        width=1<<((word>>6)&3)
        if width not in (1,2,4) or mode==1:raise ValueError('unadmitted raw quick form')
        return 'addq',width,2+ea_extra(mode,reg,width)
    if high==14 and not word&0x20 and (word>>3)&3==1:
        width=1<<((word>>6)&3)
        if width not in (1,2,4):raise ValueError('invalid raw shift width')
        return ('lsl' if word&0x100 else 'lsr'),width,2
    if word&0xF1C0 in (0xC0C0,0x80C0):return ('mulu' if high==12 else 'divu'),2,2+ea_extra(mode,reg,2)
    direction=(word>>6)&7
    if high in (9,13) and direction in (0,1,2):
        width=1<<direction;return ('sub' if high==9 else 'add'),width,2+ea_extra(mode,reg,width)
    raise ValueError(f'unadmitted raw opcode{word:04X}')
def signed(value,bits):return value-(1<<bits) if value&(1<<(bits-1)) else value
def raw_inventory(rom):
    """No map, Capstone, old consumer or old oracle supplies raw expectations."""
    verify_rom(rom);rows=[]
    for a,z,count,_ in SPANS:
        pc=a
        while pc<z:
            word=int.from_bytes(rom[pc:pc+2],'big');name,width,length=raw_shape(word)
            if pc+length>z:raise ValueError('raw admission crosses fixed source span')
            target=None;flow='linear';target_width=None
            if word>>12==6:
                delta=signed(word&255,8) if word&255 else signed(int.from_bytes(rom[pc+2:pc+4],'big'),16)
                target=(pc+2+delta)&0xFFFFFFFF;flow='direct_call' if name=='bsr' else 'direct_branch';target_width=8 if word&255 else 16
            elif name=='jsr':
                mode,reg=(word>>3)&7,word&7
                if mode==7 and reg==1:target=int.from_bytes(rom[pc+2:pc+6],'big');target_width=32
                elif mode==7 and reg==0:target=signed(int.from_bytes(rom[pc+2:pc+4],'big'),16)&0xFFFFFFFF;target_width=16
                elif mode==7 and reg==2:target=(pc+2+signed(int.from_bytes(rom[pc+2:pc+4],'big'),16))&0xFFFFFFFF;target_width=16
                flow='direct_call' if target is not None else 'unknown_indirect_call'
            elif name=='rts':flow='unknown_live_return'
            rows.append(dict(address=pc,size=length,bytes=rom[pc:pc+length].hex(),raw_opcode=f'{word:04x}',raw_family=name,data_width_bytes=width,flow=flow,direct_target=target,encoded_target_width_bits=target_width))
            pc+=length
        if sum(a<=r['address']<z for r in rows)!=count:raise ValueError('raw per-span instruction count changed')
    if len(rows)!=182 or sum(r['size'] for r in rows)!=622:raise ValueError('raw182/622 admission changed')
    return rows
def decode(rom,*,paths=None):
    """Explicit original export; raw lengths and pinned Capstone must agree."""
    from tools.code_analysis.m68k_code_map import load_capstone,M68KCodeMap
    raw_rows=raw_inventory(rom);previous=legacy_map(paths=paths);cap=load_capstone()
    if cap.__version__!='5.0.6':raise ValueError('explicit handler9b0 export requires pinned Capstone5.0.6')
    decoder=cap.Cs(cap.CS_ARCH_M68K,cap.CS_MODE_BIG_ENDIAN|cap.CS_MODE_M68K_000);decoder.detail=True
    parser=object.__new__(M68KCodeMap);parser.capstone=cap
    records,instructions=[],[]
    for raw in raw_rows:
        pc=raw['address'];ins=next(decoder.disasm(rom[pc:pc+raw['size']],pc,count=1),None)
        if ins is None or (ins.size,bytes(ins.bytes).hex(),ins.mnemonic.split('.')[0])!=(raw['size'],raw['bytes'],raw['raw_family']):
            raise ValueError(f'raw/Capstone admission conflict at{pc:06X}')
        if raw['flow'] in ('direct_call','direct_branch'):
            target=parser._transfer_target(ins)[0] if raw['raw_family']=='jsr' else parser._branch_target(ins)
            if target!=raw['direct_target']:raise ValueError('raw/Capstone direct target conflict')
        old=previous.get(pc)
        if old is None:raise ValueError('instruction lacks sealed old provenance')
        records.append(dict(zip(FIELDS,(pc,ins.size,bytes(ins.bytes).hex(),ins.mnemonic,ins.op_str,old['confidence'],'phase3-enhanced','probable',EVIDENCE))))
        instructions.append(ins)
    validate_records(rom,records,paths=paths);return records,instructions
def assembly(rom,*,paths=None):
    from tools.m68k_build.source import format_instruction
    from tools.m68k_build.m68k_build import validate_source
    records,instructions=decode(rom,paths=paths)
    lines=['| Probable fixed01A9B0 sixth mnemonic source; zero new primary ownership.',
           '| Prior120/362B helper/terrain/RNG bytes and old tables are never emitted.',
           '| Unknown neighbouring6B/8B are excluded; sparse zero gaps are not ROM content.',
           '.cpu 68000','.section .text','_start:']
    for ins in instructions:
        lines.extend([f'.org 0x{ins.address:X}',f'| {bytes(ins.bytes).hex()} {ins.op_str}'.rstrip(),f'm68k_{ins.address:06x}:','        '+format_instruction(ins),f'm68k_{ins.address:06x}_end:'])
    result=('\n'.join(lines)+'\n').encode();validate_source(result,records);return result
def verify_image(rom,object_data,image,*,paths=None):
    """Only actual ELF labels prove assembled widths; synthetic tests are limited."""
    from tools.m68k_build.elf_verify import verify_object
    records,info=inventory(rom,paths=paths)
    if type(image) is not bytes or len(image)!=0x1AC1E:raise ValueError('handler9b0 sparse image extent changed')
    if verify_object(object_data,records)!=image:raise ValueError('objcopy image differs from ELF text')
    if any(value for pc,value in enumerate(image) if not 0x1A9B0<=pc<0x1AC1E):raise ValueError('padding outside exact handler9b0 extent is not zero')
    return info
def render_bundle(rom,*,paths=None):
    records,_=decode(rom,paths=paths);raw=csv_bytes(records);source=assembly(rom,paths=paths);raw_rows=raw_inventory(rom)
    if sha(raw)!=LEDGER_SHA:raise ValueError('exported handler9b0 ledger disagrees with fixed seal')
    info=validate_records(rom,records,paths=paths)
    info.update(format='g5510-candidate-handler-9b0-source-v1',canonical_rom_sha256=ROM_SHA,
        enhanced_sha256=ENHANCED_SHA,instructions_sha256=sha(raw),canonical_source_sha256=sha(source),
        raw_admissions_sha256=sha(dump(raw_rows)),evidence_id=EVIDENCE,entry=0x1A9B0,sparse_extent=0x1AC1E,
        source_authority='src/m68k/candidate_handler_9b0.s',
        spans=[dict(start=a,end=z,instructions=n,sha256=h) for a,z,n,h in SPANS],
        excluded_prior_ledgers=[dict(path=p,sha256=h,instructions=n,bytes=b) for p,h,n,b in PRIOR_LEDGERS],
        baseline_prior_canonical_sources=[dict(path=p,sha256=h) for p,h in PRIOR_SOURCE_SEALS],
        reused_shared_code=[dict(start=a,end=z,instructions=n,bytes=b,sole_existing_physical_source=p,new_emitted_bytes=0) for a,z,n,b,p in REUSED_CODE],
        excluded_table_ranges=[list(x) for x in EXCLUDED_TABLES],excluded_table_bytes=64,newly_emitted_table_bytes=0,
        existing_dispatch_authority='analysis/candidate_tables/generated/assets.json:action_dispatch_offsets',
        unknown_neighbours=[dict(start=a,end=z,sha256=h,bytes=rom[a:z].hex(),confidence='unknown',new_emitted_bytes=0) for a,z,h in UNKNOWN_NEIGHBOURS],
        raw_direct_calls=[r for r in raw_rows if r['flow']=='direct_call'],
        unknown_live_return_pcs=[r['address'] for r in raw_rows if r['flow']=='unknown_live_return'],
        conflicts=[],decode_failures=[],confirmed_natural_entry=False,gnu_compilation_verified=False,
        scope='Conditional original sixth source; normal loads preserve edited source. No natural-entry, full CPU-domain or primary ownership proof.')
    report=(
        '# Fixed01A9B0 sixth mnemonic source\n\n'
        'probable:182 mnemonic instructions /622B only in [01A9B0,01AC1E).\n'
        'confirmed: all182 original enhanced-map spellings and discovery grades are preserved.\n'
        'confirmed: independently written raw opcode shape/length/target admission agrees with pinned Capstone5.0.6.\n'
        'confirmed: prior five compiled ledgers12475/45584B are sealed and excluded; no old source is regenerated.\n'
        'confirmed: prior120/362B guards remain solely in RNG/action, terrain/filter, setup/D and shared/C assembly.\n'
        'confirmed: old dispatch/coefficient/debit64B remain excluded; no second table editor is introduced.\n'
        'unknown: neighbouring6B/8B, natural entries/actor/origin/list/bank/state/RNG domains, actual live RTS target domain.\n'
        'confirmed: no new primary owner, complete indirect domain or natural observation; this is not a GNU build.\n'
        'confirmed: normal build requires actual GNU ELF verification of364 fixed labels before overlay; this export is not GNU execution proof.\n'
    ).encode()
    return {'instructions.csv':raw,'manifest.json':dump(info),'README.md':report,'raw_admissions.json':dump(raw_rows),'admission_status.json':dump(dict(raw_instructions=182,raw_bytes=622,capstone_version='5.0.6',conflicts=[],decode_failures=[],ownership_bytes_added=0,natural_runtime_observations_added=0))}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    for command in ('export','export-source','verify-source','verify-object','verify-image'):
        item=sub.add_parser(command);item.add_argument('--rom',type=Path,default=gb.DEFAULT_ROM)
        item.add_argument('--project-root',type=Path,default=ROOT);item.add_argument('--enhanced',type=Path,default=ENHANCED)
        item.add_argument('--generated',type=Path,default=GENERATED)
        if command.startswith('export'):item.add_argument('--output',type=Path,required=True)
        elif command=='verify-source':item.add_argument('--source',type=Path,default=SOURCE)
        else:item.add_argument('--object',type=Path,required=True);item.add_argument('--image',type=Path,required=True)
    args=parser.parse_args(argv);p=Paths(project_root=args.project_root,enhanced=args.enhanced,generated=args.generated)
    rom=read(args.rom);verify_rom(rom)
    if args.command=='verify-source':print(dump(load_source(rom,args.source,paths=p)[2]).decode(),end='');return 0
    if args.command in ('verify-object','verify-image'):print(dump(verify_image(rom,read(args.object),read(args.image),paths=p)).decode(),end='');return 0
    inputs=[args.rom,p.enhanced,*(p.project_root/x for x in PRIOR_SOURCES),*(p.project_root/x for x,_,_,_ in PRIOR_LEDGERS)]
    if args.command=='export':print(gb.publish(render_bundle(rom,paths=p),args.output,[*inputs,p.source]));return 0
    target=gb.af.safe_path(args.output);gb.af._separate(target,[gb.af.safe_path(x,regular_input=True) for x in inputs])
    if target.exists() or not target.parent.is_dir():raise ValueError('fresh source file with existing parent required')
    data=assembly(rom,paths=p)
    with target.open('xb') as stream:stream.write(data)
    print(target);return 0

if __name__=='__main__':raise SystemExit(main())
