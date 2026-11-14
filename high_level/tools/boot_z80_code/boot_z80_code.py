"""38 transported startup code bytes from25 editable GNU Z80 mnemonics.

Source boundary labels and real GNU COFF are checked without simulating CPU,
RAM/stack, LDIR effects, hardware gating or a natural indirect-jump domain.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
import re
import struct
from pathlib import Path

from tools.audio_analysis import z80_decoder as decoder
from tools.m68k_build import m68k_build as m
from tools.direct_code import direct_code as d

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'src/z80/startup_clear.s'
LEDGER=ROOT/'analysis/boot_z80_code/generated/instructions.json'
FORMAL_ROOT=LEDGER.parent
OUTPUT_ROOT=ROOT/'build/boot_z80_code'
TOOL_BIN=ROOT/'build/z80_code/toolchain/prefix/bin'
ROM_BASE,END,COUNT,BYTES=0x2CA,0x2F0,25,38
ROM_SHA256=reference_value(__name__, 'ROM_SHA256')
CONSUMER_SHA256=reference_value(__name__, 'CONSUMER_SHA256')
LEDGER_SHA=reference_value(__name__, 'LEDGER_SHA')
SPECS=(
    (0x00,'af'),(0x01,'01d91f'),(0x04,'112700'),(0x07,'212600'),(0x0A,'f9'),
    (0x0B,'77'),(0x0C,'edb0'),(0x0E,'dde1'),(0x10,'fde1'),(0x12,'ed47'),
    (0x14,'ed4f'),(0x16,'d1'),(0x17,'e1'),(0x18,'f1'),(0x19,'08'),(0x1A,'d9'),
    (0x1B,'c1'),(0x1C,'d1'),(0x1D,'e1'),(0x1E,'f1'),(0x1F,'f9'),(0x20,'f3'),
    (0x21,'ed56'),(0x23,'36e9'),(0x25,'e9'),
)
COMMENTS={0:'Entry0 is the statically justified reset-loaded source.',
    0x0B:'Explicit zero at26 supplies overlapping LDIR source26/destination27.',
    0x0C:'Original BC1FD9 propagates zero through1FFF; do not infer RAM/CPU state.',
    0x0E:'POPs use SP26 and the previously written RAM, not additional ROM source.',
    0x23:'Final write is self-modification of RAM through HL, not a ROM byte patch.',
    0x25:'Keep the indirect target unknown here; no invented natural jump domain.'}
MNEMONICS={'xor','ld','ldir','pop','ex','exx','di','ei','im','jp','nop','or','and','inc','dec'}


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=m.af.ROM_SIZE or m.sha(rom)!=ROM_SHA256:
        raise ValueError('canonical full ROM bytes, size and SHA required')
    if m.sha(rom[0x200:0x294])!=CONSUMER_SHA256:
        raise ValueError('original boot transport consumer differs')
    # The original copy destination is A0 loaded by MOVEM.L, not driver69D2.
    if rom[0x29A:0x29E]!=bytes.fromhex('00a00000') or rom[0x216:0x222].hex()!='4bfa007c4c9d00e04cdd1f00':
        raise ValueError('original ROM-to-Z80 destination or source progression differs')
    if rom[0x254:0x25A].hex()!='742510dd51ca':
        raise ValueError('original38-BYTE copy count/read opcode differs')


def original_records(rom):
    verify_rom(rom);program=rom[ROM_BASE:END];rows=[];cursor=0
    for address,raw in SPECS:
        ins=decoder.decode_instruction(program,address)
        if address!=cursor or ins.raw.hex()!=raw or ins.mnemonic=='db':
            raise ValueError('pinned original startup instruction boundary differs')
        rows.append(dict(address=address,rom_address=ROM_BASE+address,size=ins.size,bytes=raw,
            original_mnemonic=ins.mnemonic,original_operand=ins.operand,flow_type=ins.flow_type,
            target=ins.target,confidence='confirmed_static_transport',
            discovery_evidence=dict(kind='boot_reset_loaded_entry' if address==0 else 'original_linear_fallthrough',
                predecessor=None if not rows else rows[-1]['address'],source_M68K_copy_PC=0x256,
                Z80_entry=0,source_ROM_start=ROM_BASE,indirect_target_not_exhausted=True)))
        cursor+=ins.size
    if cursor!=BYTES or len(rows)!=COUNT or rows[-1]['flow_type']!='indirect_jump' or rows[-1]['target'] is not None:
        raise ValueError('fixed25-instruction38-BYTE indirect-ended source differs')
    return rows


def canonical_source(rows):
    lines=['; Original boot copy at M68K 0256 loads these38 bytes to Z80 RAM0000.',
        '; Separate from recovered_driver.s. Source encoding, not a full CPU proof.',
        '.text','_boot_start:','.org 0x0']
    for row in rows:
        address=row['address']
        if address in COMMENTS:lines.append('; '+COMMENTS[address])
        lines.extend([f'boot_z80_{address:04x}:','        '+row['original_mnemonic']+
            (' '+row['original_operand'] if row['original_operand'] else ''),f'boot_z80_{address:04x}_end:'])
    return ('\n'.join(lines)+'\n').encode('ascii')


def validate_source(source,records):
    if type(records) is not list or len(records)!=COUNT:raise ValueError('fixed25-instruction catalog required')
    if type(source) is not bytes or len(source)>2_000_000:raise ValueError('bounded bytes instruction source required')
    try:text=source.decode('ascii')
    except UnicodeDecodeError as error:raise ValueError('ASCII mnemonic source required') from error
    lines=[line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith(';')]
    if lines[:3]!=['.text','_boot_start:','.org 0x0'] or len(lines)!=3+3*COUNT:
        raise ValueError('single fixed origin/header and exactly25 mnemonic statements required')
    for row,offset in zip(records,range(3,len(lines),3)):
        label,instruction,end=lines[offset:offset+3];address=row['address']
        if label!=f'boot_z80_{address:04x}:' or end!=f'boot_z80_{address:04x}_end:':
            raise ValueError('fixed logical instruction labels changed')
        if instruction.split(' ',1)[0] not in MNEMONICS or any(c in instruction for c in (';',':','#','\x00')):
            raise ValueError('one admitted instruction, no byte/include/directive/extra statement required')


def export_bundle(rom):
    rows=original_records(rom);source=canonical_source(rows);validate_source(source,rows);ledger=m.dump(rows)
    info=dict(format='g5510-boot-Z80-mnemonic-source-v1',instructions=COUNT,bytes=BYTES,
        instructions_sha256=m.sha(ledger),canonical_source_sha256=m.sha(source),rom_sha256=ROM_SHA256,
        logical_start=0,logical_end=BYTES,physical_start=ROM_BASE,physical_end=END,
        boot_copy_PC=0x256,boot_copy_count_WORD=37,original_destination_A0_LONG=0xA00000,
        original_boot_consumer_sha256=CONSUMER_SHA256,confidence='confirmed_static_transport',
        final_instruction=dict(address=0x25,mnemonic='jp',operand='(hl)',target=None),
        excluded_driver_physical_start=0x69D2,old_driver_unchanged=True,
        ownership_bytes_added=0,natural_entries_added=0,complete_indirect_domains_added=0,
        independent_CPU_comparison=False,CPU_or_RAM_execution=False,
        statement='Reset-loaded entry0 and exact static fallthrough/source boundaries only; LDIR/RAM/stack/self-modification not simulated; no opaque byte emission or natural jump-domain claim.')
    return {'instructions.json':ledger,'manifest.json':m.dump(info),'startup_clear.s':source}


def inventory(rom):
    expected=original_records(rom);data=m.read(LEDGER)
    if m.sha(data)!=LEDGER_SHA or data!=m.dump(expected):raise ValueError('sealed startup instruction ledger changed')
    return expected


def verify_object(data,records):
    """Bounded actual GNU Z80 little-endian COFF, all50 boundary labels."""
    if type(records) is not list or len(records)!=COUNT or sum(r['size'] for r in records)!=BYTES:
        raise ValueError('fixed25-instruction38-BYTE boundary catalog required')
    if type(data) is not bytes or not 20<=len(data)<=2_000_000:raise ValueError('bounded COFF bytes required')
    magic,sections,timestamp,symptr,symcount,optional,flags=struct.unpack_from('<HHIIIHH',data)
    if magic!=0x805A or sections!=3 or timestamp or optional or flags!=0x3105 or 20+40*sections>len(data):
        raise ValueError('expected GNU Z80 COFF header')
    expected={f'boot_z80_{r["address"]:04x}'+suffix:r['address']+(r['size'] if suffix else 0) for r in records for suffix in ('','_end')}
    section_names=set();text=None;text_index=None
    for index in range(sections):
        name,paddr,vaddr,size,offset,relptr,lineptr,relcount,linecount,sflags=struct.unpack_from('<8sIIIIIIHHI',data,20+40*index)
        name=name.rstrip(b'\0').decode('ascii')
        if name not in ('.text','.data','.bss') or name in section_names or paddr or vaddr or relcount or linecount or relptr or lineptr:
            raise ValueError('unexpected section or unresolved relocation')
        section_names.add(name)
        if sflags!={'.text':0x20,'.data':0x40,'.bss':0x80}[name]:raise ValueError('unexpected GNU section flags')
        if size and (offset<20+40*sections or offset+size>symptr):raise ValueError('COFF section content outside object')
        if name=='.text':text=data[offset:offset+size];text_index=index+1
        elif size:raise ValueError('nonempty noncode section')
    if text is None or len(text)!=BYTES or max(expected.values())!=BYTES:raise ValueError('fixed38-BYTE text extent differs')
    strings_start=symptr+18*symcount
    if symptr<20+40*sections or strings_start+4>len(data):raise ValueError('COFF symbols outside object')
    strings_size=struct.unpack_from('<I',data,strings_start)[0]
    if strings_size<4 or strings_start+strings_size!=len(data):raise ValueError('COFF string table extent differs')
    strings=data[strings_start:];seen=set();index=0;entry=False
    while index<symcount:
        raw,value,section,kind,storage,aux=struct.unpack_from('<8sIhHBB',data,symptr+18*index)
        if raw[:4]==b'\0'*4:
            offset=struct.unpack_from('<I',raw,4)[0]
            if not 4<=offset<len(strings) or b'\0' not in strings[offset:]:raise ValueError('invalid symbol name extent')
            name=strings[offset:strings.index(0,offset)].decode('ascii')
        else:name=raw.rstrip(b'\0').decode('ascii')
        if name.startswith('boot_z80_'):
            if name not in expected or name in seen or section!=text_index or value!=expected[name] or kind or aux:
                raise ValueError('instruction boundary moved/duplicated/malformed')
            seen.add(name)
        elif name=='_boot_start':
            if entry or value or section!=text_index or kind or aux:raise ValueError('startup entry label changed')
            entry=True
        elif section==0:raise ValueError('undefined COFF symbol')
        elif name not in ('.file','.text','.data','.bss'):raise ValueError('unexpected noninstruction symbol')
        if index+1+aux>symcount:raise ValueError('COFF auxiliary symbol outside table')
        index+=1+aux
    if seen!=set(expected) or not entry:raise ValueError('missing source boundary or entry label')
    return text


def verify_image(rom,source,object_data,image,canonical=False):
    rows=inventory(rom);validate_source(source,rows)
    if type(image) is not bytes or len(image)!=BYTES or verify_object(object_data,rows)!=image:
        raise ValueError('COFF/image or fixed38-BYTE program extent differs')
    if canonical and image!=rom[ROM_BASE:END]:raise ValueError('canonical GNU startup bytes differ')
    return dict(instructions=COUNT,compiled_bytes=BYTES,coff_labels=50,canonical=canonical,
        ownership_bytes_added=0,natural_entries_added=0,complete_indirect_domains_added=0,independent_CPU_comparison=False)


def add_to_layout(rom,source,base):
    rows=inventory(rom);validate_source(source,rows);positions=set(range(ROM_BASE,END))
    if not positions<=d.raw_positions(base):raise ValueError('startup code overlaps an existing physical authority')
    result=dict(base);lines=[];consumed=[]
    for line in base['m68k_bank00.s'].decode().splitlines():
        match=re.fullmatch(d.PATTERN,line)
        if not match:lines.append(line);continue
        first=int(match[2],16);last=first+int(match[3],16)
        if last<=ROM_BASE or first>=END:lines.append(line);continue
        lo,hi=max(first,ROM_BASE),min(last,END)
        if first<lo:lines.append(f'        .incbin "segments/bank00.bin", 0x{first:X}, 0x{lo-first:X}')
        lines.append(f'        .incbin "boot_z80_code.bin", 0x{lo-ROM_BASE:X}, 0x{hi-lo:X}')
        consumed.extend(range(lo,hi))
        if hi<last:lines.append(f'        .incbin "segments/bank00.bin", 0x{hi:X}, 0x{last-hi:X}')
    if len(consumed)!=BYTES or set(consumed)!=positions:raise ValueError('boot code physical slice omitted/duplicated')
    result['m68k_bank00.s']=('\n'.join(lines)+'\n').encode()
    info=json.loads(base['manifest.json']);info.update(boot_z80_code_bytes=BYTES,boot_z80_code_instructions=COUNT,
        boot_z80_code_ledger_sha256=LEDGER_SHA,boot_z80_code_source_sha256=m.sha(source),
        boot_z80_code_confidence='confirmed_static_transport',boot_z80_code_owner_bytes_added=0,
        boot_z80_code_natural_entries_added=0,compiled_or_typed_bytes=info['compiled_or_typed_bytes']+BYTES,
        remaining_raw_slice_bytes=info['remaining_raw_slice_bytes']-BYTES)
    result['manifest.json']=m.dump(info);return result


def overlay(rom,baseline,image):
    inventory(rom)
    if type(baseline) is not bytes or len(baseline)!=m.af.ROM_SIZE or type(image) is not bytes or len(image)!=BYTES:
        raise ValueError('fixed full baseline and38-BYTE code image required')
    out=bytearray(baseline);out[ROM_BASE:END]=image;return bytes(out)


def fresh_output(value,bundle=False):
    path=m.af.safe_path(value)
    if not (path.is_relative_to(OUTPUT_ROOT) and path!=OUTPUT_ROOT) and not (bundle and path==FORMAL_ROOT):
        raise ValueError('dedicated boot-code output or exact formal bundle required')
    if path.exists():raise ValueError('fresh dedicated boot-code output required')
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('export','verify-object'))
    parser.add_argument('--rom',default=str(m.af.DEFAULT_ROM));parser.add_argument('--source',default=str(SOURCE))
    parser.add_argument('--output-root');parser.add_argument('--object');parser.add_argument('--image');parser.add_argument('--canonical',action='store_true')
    args=parser.parse_args(argv);target=None
    if args.command=='export':
        if args.output_root is None:raise ValueError('fresh output-root required')
        target=fresh_output(args.output_root,bundle=True)
    rom=m.read(args.rom,m.af.ROM_SIZE)
    if target is not None:
        bundle=export_bundle(rom);target.mkdir(parents=True)
        for name,data in bundle.items():
            with (target/name).open('xb') as stream:stream.write(data)
        print(json.dumps(dict(instructions=COUNT,bytes=BYTES,ledger_sha256=m.sha(bundle['instructions.json']))))
    else:
        if args.object is None or args.image is None:raise ValueError('actual COFF/image required')
        print(json.dumps(verify_image(rom,m.read(args.source),m.read(args.object),m.read(args.image),args.canonical)))
    return 0


if __name__=='__main__':raise SystemExit(main())
