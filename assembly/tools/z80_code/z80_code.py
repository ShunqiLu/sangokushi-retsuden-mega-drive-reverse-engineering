"""Editable fixed-boundary GNU Z80 source; logical RAM and physical ROM differ."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse,csv,io,json,re,struct
from pathlib import Path
from tools.audio_analysis import z80_decoder as decoder,z80_payload as payload
from tools.m68k_build import m68k_build as m
from tools.direct_code import direct_code as d

ROOT=Path(__file__).resolve().parents[2]
MAP=ROOT/'analysis/audio/generated/instructions.csv'
MAP_SHA=reference_value(__name__, 'MAP_SHA')
LEDGER=ROOT/'analysis/z80_code/generated/instructions.json'
SOURCE=ROOT/'src/z80/recovered_driver.s'
OUTPUT_ROOT=ROOT/'build/z80_code'
TOOL_BIN=OUTPUT_ROOT/'toolchain/prefix/bin'
LEDGER_SHA=reference_value(__name__, 'LEDGER_SHA')
COUNT=1683;BYTES=3334;ROM_BASE=0x69D2
MNEMONICS={'di','im','jr','ld','bit','ret','jp','add','nop','inc','push','or','dec','call',
    'pop','ei','and','rst','srl','rr','xor','djnz','cp','exx','ex','sub','res','sra','ldi',
    'rlca','neg','set','sbc','ldir','rrca'}

def format_instruction(ins):
    mnemonic,operand=ins.mnemonic,ins.operand
    if mnemonic in ('add a','adc a','sbc a'):
        mnemonic,operand=mnemonic.split()[0],'a,'+operand
    if ins.flow_type in ('relative_jump','conditional_relative','djnz') or mnemonic=='djnz':
        if ins.target is None:raise ValueError('relative instruction without target')
        pieces=operand.split(',');pieces[-1]=f'z80_{ins.target:04x}';operand=','.join(pieces)
    return mnemonic+(' '+operand if operand else '')

def validate_source(source,records):
    if type(source)is not bytes or len(source)>2_000_000:raise ValueError('bounded bytes source required')
    try:text=source.decode('ascii')
    except UnicodeDecodeError as e:raise ValueError('ASCII instruction source required') from e
    lines=[line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith(';')]
    if lines[:2]!=['.text','_start:']:raise ValueError('fixed text section/header required')
    lines=lines[2:]
    if len(lines)!=4*len(records):raise ValueError('exactly one mnemonic per instruction required')
    for row,offset in zip(records,range(0,len(lines),4)):
        a=row['address'];org,label,instruction,end=lines[offset:offset+4]
        if org!=f'.org 0x{a:X}' or label!=f'z80_{a:04x}:' or end!=f'z80_{a:04x}_end:':raise ValueError('fixed instruction labels/origin changed')
        if instruction.split(' ',1)[0] not in MNEMONICS:raise ValueError('not an admitted Z80 mnemonic')
        if any(c in instruction for c in (';', '\n', '\r', ':', '#')) or '\x00' in instruction:raise ValueError('extra directive/comment/statement forbidden')

def export_bundle(rom):
    payload.validate_rom(rom);data=m.read(MAP)
    if m.sha(data)!=MAP_SHA:raise ValueError('original control-flow instruction map changed')
    runtime,_=payload.compose_runtime(payload.extract_components(rom))
    rows=[];lines=['; Original CFG boundaries, GNU mnemonics, no original-byte emission.',
        '; z80_NNNN labels are logical RAM addresses; physical ROM = 0069D2 + NNNN.','.text','_start:']
    previous_end=0
    for row in csv.DictReader(io.StringIO(data.decode('utf-8-sig'))):
        a,size=int(row['address']),int(row['size']);raw=bytes.fromhex(row['bytes'])
        if a<previous_end or not 1<=size<=4 or a+size>0xFCA or len(raw)!=size or raw!=rom[ROM_BASE+a:ROM_BASE+a+size]:raise ValueError('original instruction map extent/identity differs')
        ins=decoder.decode_instruction(runtime,a)
        if (ins.raw,ins.size,ins.mnemonic,ins.operand)!=(raw,size,row['mnemonic'],row['operand']):raise ValueError('decoder and original control-flow map disagree')
        if row['confidence'] not in ('confirmed','probable'):raise ValueError('unjustified heuristic is not source code')
        proof=json.loads(row['discovery_evidence'])
        if not proof or any(p.get('type') in ('linear_sweep','heuristic') for p in proof):raise ValueError('missing control-flow evidence')
        rows.append(dict(address=a,rom_address=ROM_BASE+a,size=size,bytes=raw.hex(),confidence=row['confidence'],
            original_mnemonic=ins.mnemonic,original_operand=ins.operand,flow_type=ins.flow_type,target=ins.target,
            function_owners=json.loads(row['function_owners']),discovery_evidence=proof))
        lines.extend([f'.org 0x{a:X}',f'z80_{a:04x}:','        '+format_instruction(ins),f'z80_{a:04x}_end:'])
        previous_end=a+size
    if len(rows)!=COUNT or sum(r['size'] for r in rows)!=BYTES:raise ValueError('fixed original CFG scope changed')
    source=('\n'.join(lines)+'\n').encode();validate_source(source,rows);ledger=m.dump(rows)
    confirmed=[r for r in rows if r['confidence']=='confirmed'];probable=[r for r in rows if r['confidence']=='probable']
    info=dict(format='g5510-z80-mnemonic-source-v1',instructions=COUNT,bytes=BYTES,
        confirmed_instructions=len(confirmed),confirmed_bytes=sum(r['size'] for r in confirmed),
        probable_instructions=len(probable),probable_bytes=sum(r['size'] for r in probable),
        original_map_sha256=MAP_SHA,instructions_sha256=m.sha(ledger),canonical_source_sha256=m.sha(source),
        rom_sha256=payload.EXPECTED_ROM_SHA256,address_spaces=dict(address='Z80 RAM logical',rom_address='linear ROM physical'),
        mapping=dict(rom_base=ROM_BASE,z80_destination=0,end_exclusive=0xFCA),
        ranges=m.coalesce(rows),excluded_instructions=[],ownership_bytes_added=0,natural_entries_added=0,
        complete_indirect_domains_added=0,independent_CPU_comparison=False,
        statement='CFG justified original instructions only; original probable confidence retained; no byte directives, new index-domain proof, or full Z80 execution claim.')
    return {'instructions.json':ledger,'manifest.json':m.dump(info),'recovered_driver.s':source}

def inventory(rom):
    payload.validate_rom(rom);data=m.read(LEDGER)
    if m.sha(data)!=LEDGER_SHA:raise ValueError('Z80 ledger changed')
    rows=json.loads(data);end=0
    for r in rows:
        a,size=r['address'],r['size']
        if type(a)is not int or type(size)is not int or a<end or not 1<=size<=4 or a+size>0xFCA or r['rom_address']!=ROM_BASE+a:raise ValueError('logical/physical instruction extent differs')
        if bytes.fromhex(r['bytes'])!=rom[ROM_BASE+a:ROM_BASE+a+size] or r['confidence'] not in ('confirmed','probable'):raise ValueError('original byte or evidence differs')
        end=a+size
    if len(rows)!=COUNT or sum(r['size'] for r in rows)!=BYTES:raise ValueError('fixed instruction scope differs')
    return rows

def verify_object(data,records):
    """Read bounded GNU Z80 little-endian COFF; no execution, decoder or files."""
    if type(data)is not bytes or not 20<=len(data)<=2_000_000:raise ValueError('bounded COFF bytes required')
    magic,sections,timestamp,symptr,symcount,optional,flags=struct.unpack_from('<HHIIIHH',data)
    if magic!=0x805A or sections!=3 or timestamp or optional or flags!=0x3105 or 20+40*sections>len(data):raise ValueError('expected bounded GNU Z80 COFF header')
    expected={f'z80_{r["address"]:04x}'+suffix:r['address']+(r['size'] if suffix else 0) for r in records for suffix in ('','_end')}
    section_rows=[];text=None;text_index=None;section_names=set()
    for i in range(sections):
        name,paddr,vaddr,size,offset,relptr,lineptr,relcount,linecount,sflags=struct.unpack_from('<8sIIIIIIHHI',data,20+40*i)
        name=name.rstrip(b'\0').decode('ascii')
        if name not in ('.text','.data','.bss') or name in section_names or paddr or vaddr or relcount or linecount or relptr or lineptr:raise ValueError('unexpected section or unresolved relocation')
        section_names.add(name)
        if sflags!={'.text':0x20,'.data':0x40,'.bss':0x80}[name]:raise ValueError('unexpected GNU Z80 section flags')
        if size and (offset<20+40*sections or offset+size>symptr):raise ValueError('section outside COFF content')
        if name=='.text':
            if text is not None or not sflags&0x20:raise ValueError('duplicate/noncode text section')
            text=data[offset:offset+size];text_index=i+1
        elif size:raise ValueError('nonempty noncode section')
        section_rows.append((name,size))
    if text is None or len(text)!=max(expected.values()):raise ValueError('compiled logical text extent differs')
    strings_start=symptr+18*symcount
    if symptr<20+40*sections or strings_start+4>len(data):raise ValueError('COFF symbols outside object')
    strings_size=struct.unpack_from('<I',data,strings_start)[0]
    if strings_size<4 or strings_start+strings_size!=len(data):raise ValueError('COFF string table extent differs')
    strings=data[strings_start:];seen=set();index=0
    while index<symcount:
        raw,value,section,kind,storage,aux=struct.unpack_from('<8sIhHBB',data,symptr+18*index)
        if raw[:4]==b'\0'*4:
            offset=struct.unpack_from('<I',raw,4)[0]
            if not 4<=offset<len(strings) or b'\0' not in strings[offset:]:raise ValueError('invalid COFF symbol string')
            name=strings[offset:strings.index(0,offset)].decode('ascii')
        else:name=raw.rstrip(b'\0').decode('ascii')
        if name.startswith('z80_'):
            if name not in expected or name in seen or section!=text_index or value!=expected[name] or kind or aux:raise ValueError('instruction label moved/duplicated/malformed')
            seen.add(name)
        elif section==0:raise ValueError('undefined COFF symbol')
        elif name not in ('_start','.file','.text','.data','.bss'):raise ValueError('unexpected noninstruction symbol')
        if index+1+aux>symcount:raise ValueError('COFF auxiliary symbol outside table')
        index+=1+aux
    if seen!=set(expected):raise ValueError('missing instruction boundary label')
    return text

def verify_image(rom,source,object_data,image,canonical=False):
    rows=inventory(rom);validate_source(source,rows)
    if verify_object(object_data,rows)!=image:raise ValueError('COFF and image differ')
    positions={p for r in rows for p in range(r['address'],r['address']+r['size'])}
    if any(value for a,value in enumerate(image) if a not in positions):raise ValueError('noninstruction sparse padding changed')
    if canonical and any(image[r['address']:r['address']+r['size']]!=bytes.fromhex(r['bytes']) for r in rows):raise ValueError('canonical GNU instruction bytes differ')
    return dict(instructions=len(rows),compiled_bytes=len(positions),coff_labels=2*len(rows),canonical=canonical,
        ownership_bytes_added=0,natural_entries_added=0,complete_indirect_domains_added=0)

def add_to_layout(rom,source,base):
    rows=inventory(rom);validate_source(source,rows);raw=d.raw_positions(base)
    physical=[dict(address=r['rom_address'],size=r['size']) for r in rows]
    positions={p for r in physical for p in range(r['address'],r['address']+r['size'])}
    if not positions<=raw:raise ValueError('Z80 instructions overlap an existing physical authority')
    ranges=m.coalesce(physical);consumed=[];result=dict(base)
    for bank in range(16):
        lines=[]
        for line in base[f'm68k_bank{bank:02x}.s'].decode().splitlines():
            match=re.fullmatch(d.PATTERN,line)
            if not match:lines.append(line);continue
            first=bank*65536+int(match[2],16);last=first+int(match[3],16);cursor=first
            for a,z in ranges:
                if z<=first or a>=last:continue
                lo,hi=max(a,first),min(z,last)
                if cursor<lo:lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{lo-cursor:X}')
                lines.append(f'        .incbin "z80_driver_code.bin", 0x{lo-ROM_BASE:X}, 0x{hi-lo:X}')
                consumed.extend(range(lo,hi));cursor=hi
            if cursor<last:lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{last-cursor:X}')
        result[f'm68k_bank{bank:02x}.s']=('\n'.join(lines)+'\n').encode()
    if len(consumed)!=BYTES or set(consumed)!=positions:raise ValueError('Z80 physical code omitted/duplicated')
    info=json.loads(base['manifest.json']);info.update(z80_code_bytes=BYTES,z80_code_instructions=COUNT,z80_code_ledger_sha256=LEDGER_SHA,
        z80_code_source_sha256=m.sha(source),z80_code_confidence='original CFG confirmed/probable retained',
        compiled_or_typed_bytes=info['compiled_or_typed_bytes']+BYTES,remaining_raw_slice_bytes=info['remaining_raw_slice_bytes']-BYTES,
        z80_code_owner_bytes_added=0,z80_code_natural_entries_added=0)
    result['manifest.json']=m.dump(info);return result

def overlay(rom,baseline,image):
    rows=inventory(rom)
    if type(baseline)is not bytes or len(baseline)!=m.af.ROM_SIZE or len(image)!=0xFCA:raise ValueError('fixed full baseline and logical code extent required')
    out=bytearray(baseline)
    for r in rows:
        a,z=r['address'],r['address']+r['size'];out[ROM_BASE+a:ROM_BASE+z]=image[a:z]
    return bytes(out)

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','verify-object'))
    p.add_argument('--rom',default=str(m.af.DEFAULT_ROM));p.add_argument('--source',default=str(SOURCE));p.add_argument('--output-root')
    p.add_argument('--object');p.add_argument('--image');p.add_argument('--canonical',action='store_true');a=p.parse_args(argv)
    rom=m.read(a.rom,m.af.ROM_SIZE)
    if a.command=='export':
        if not a.output_root:raise ValueError('fresh output-root required')
        target=m.af.safe_path(a.output_root)
        if not target.is_relative_to(OUTPUT_ROOT) or target==OUTPUT_ROOT or target.exists():raise ValueError('fresh dedicated build directory required')
        bundle=export_bundle(rom);target.mkdir(parents=True)
        for name,data in bundle.items():
            with (target/name).open('xb') as s:s.write(data)
        print(m.sha(bundle['instructions.json']))
    else:
        if not a.object or not a.image:raise ValueError('actual COFF/image required')
        print(json.dumps(verify_image(rom,m.read(a.source),m.read(a.object),m.read(a.image),a.canonical)))
    return 0
if __name__=='__main__':raise SystemExit(main())
