"""Explicitly export original secondary-command code, then build sealed mnemonics.

Original compiled00E068 consumes21 signed WORD slots atE0C4 relativeFE06;
slot6 is bypassed. Physical membership is not a natural F65A domain proof.
"""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse,json,re
from collections import deque
from tools.direct_code import direct_code as d
from tools.final_dispatch_code import final_dispatch_code as final
from tools.m68k_build.elf_verify import verify_object
from tools.sprite_lifetime import static_checks as proof

ROOT=d.ROOT;m=d.m;f=d.f
LEDGER=ROOT/'analysis/secondary_dispatch_code/generated/instructions.json'
SOURCE=ROOT/'src/m68k/secondary_dispatch_descendants.s'
BASE_LAYOUT=ROOT/('build/direct_code/layout/' + reference_value(__name__, 'BASE_LAYOUT'))
COUNT=944;BYTES=3432;LEDGER_SHA=reference_value(__name__, 'LEDGER_SHA')
MNEMONICS=final.MNEMONICS
CONSUMER={0xE050:'3038f65a',0xE054:'0c400006',0xE058:'67000062',0xE05C:'e348',
          0xE05E:'303b0064',0xE062:'41fa1da2',0xE066:'4e71',0xE068:'4eb00000'}

def validate_source(source,records):return m.validate_source(source,records,allowed_mnemonics=MNEMONICS)

def base_layout():
    return {path.name:m.read(path) for path in BASE_LAYOUT.iterdir() if path.is_file()}

def table_proof(rom,prior):
    m.af.verify_rom(rom)
    for pc,raw in CONSUMER.items():
        if pc not in prior or rom[pc:pc+len(raw)//2]!=bytes.fromhex(raw):raise ValueError('original compiled secondary consumer differs')
    targets=proof.signed_table(rom,0xE0C4,21,0xFE06)
    if targets!=proof.SECONDARY_TARGETS:raise ValueError('original secondary table differs')
    # PC-relative extension is atE060;0064 resolves tableE0C4. LEA extension
    # atE064 +1DA2 resolvesFE06. Actual selector6 branchE05A+62 resolvesE0BC.
    if 0xE060+int.from_bytes(rom[0xE060:0xE062],'big',signed=True)!=0xE0C4:raise ValueError('table PC arithmetic differs')
    if 0xE064+int.from_bytes(rom[0xE064:0xE066],'big',signed=True)!=0xFE06:raise ValueError('target base PC arithmetic differs')
    if 0xE05A+int.from_bytes(rom[0xE05A:0xE05C],'big',signed=True)!=0xE0BC:raise ValueError('selector6 bypass differs')
    return dict(consumer=0xE068,table_start=0xE0C4,table_end=0xE0EE,target_base=0xFE06,
        entries=[dict(index=i,word_address=0xE0C4+2*i,target=t,bypassed=i==6) for i,t in enumerate(targets)],
        consumer_instructions=[dict(pc=pc,bytes=raw) for pc,raw in CONSUMER.items()],
        confidence='confirmed_encoding_conditional_targets',natural_selector_domain_complete=False,
        CPU_upper_bound_check=False,source_reference='tools/sprite_lifetime/static_checks.py; ALTERNATE_INIT_LIFETIME_SCOUT.md')

def direct_edges(rom,a,size):
    """Decode direct control operands from original words, never operand strings."""
    op=int.from_bytes(rom[a:a+2],'big');following=a+size
    if op>>12==6:
        byte=op&255;delta=(byte-256 if byte&128 else byte) if byte else int.from_bytes(rom[a+2:a+4],'big',signed=True)
        kind='call' if op>>8==0x61 else 'branch_taken'
        rows=[(kind,a+2+delta)]
        if op>>8!=0x60:rows.append(('call_fallthrough' if kind=='call' else 'branch_fallthrough',following))
        return rows
    if op&0xF0F8==0x50C8:
        return [('branch_taken',a+2+int.from_bytes(rom[a+2:a+4],'big',signed=True)),('branch_fallthrough',following)]
    if op&0xFFC0 in (0x4E80,0x4EC0):
        call=op&0xFFC0==0x4E80;mode,reg=(op>>3)&7,op&7
        if (mode,reg)==(7,1):target=int.from_bytes(rom[a+2:a+6],'big')
        elif (mode,reg)==(7,0):target=int.from_bytes(rom[a+2:a+4],'big',signed=True)&0xFFFFFFFF
        elif (mode,reg)==(7,2):target=a+2+int.from_bytes(rom[a+2:a+4],'big',signed=True)
        else:target=None
        rows=[('call' if call else 'jump',target)]
        if call:rows.append(('call_fallthrough',following))
        return rows
    if op in (0x4E75,0x4E73,0x4E77,0x4E72,0x4AFC):return []
    if op&0xFFF0==0x4E40:
        p=(32+(op&15))*4
        return [('trap_handler',int.from_bytes(rom[p:p+4],'big')),('exception_return_fallthrough',following)]
    return [('fallthrough',following)]

def export_bundle(rom):
    from tools.code_analysis.m68k_code_map import load_capstone
    from tools.m68k_build.source import format_instruction
    m.af.verify_rom(rom);base=base_layout();raw=d.raw_positions(base)
    info=json.loads(base['manifest.json'])
    if info['compiled_instruction_union']!=52100 or info['compiled_or_typed_bytes']!=973939:raise ValueError('fixed prior layout differs')
    prior=set();pins={}
    for path in sorted((ROOT/'src/m68k').glob('*.s')):
        if path==SOURCE:continue
        data=m.read(path);pins[path.name]=m.sha(data)
        prior.update(int(a,16) for a in re.findall(r'^m68k_([0-9a-f]{6}):$',data.decode(),re.M))
    if len(prior)!=52100:raise ValueError('prior eleven-source topology differs')
    table=table_proof(rom,prior)
    seeds={}
    for entry in table['entries']:
        if not entry['bypassed'] and entry['target'] not in prior:
            seeds.setdefault(entry['target'],[]).append(entry['index'])
    cap=load_capstone()
    if cap.__version__!='5.0.6':raise ValueError('explicit export requires Capstone5.0.6')
    decoder=cap.Cs(cap.CS_ARCH_M68K,cap.CS_MODE_BIG_ENDIAN|cap.CS_MODE_M68K_000)
    decoder.detail=True
    queue=deque((a,None,'conditional_table_member',a) for a in sorted(seeds))
    instructions={};owners={};blocked=[];conflicts=[]
    while queue:
        a,parent,edge,seed=queue.popleft()
        if a in prior or a in instructions:continue
        if a is None or type(a)is not int or a&1 or a<0x200 or a>=len(rom):
            blocked.append(dict(address=a,parent=parent,edge=edge,reason='indirect_or_invalid_target'));continue
        if a not in raw:
            blocked.append(dict(address=a,parent=parent,edge=edge,reason='outside_remaining_raw'));continue
        if a in owners:
            conflicts.append(dict(address=a,owner=owners[a],parent=parent,edge=edge));continue
        ins=next(decoder.disasm(rom[a:a+10],a,count=1),None)
        if ins is None or ins.size<2 or ins.size>10 or ins.size&1 or ins.mnemonic.split('.')[0] not in MNEMONICS:
            blocked.append(dict(address=a,parent=parent,edge=edge,reason='unsupported_decode'));continue
        span=set(range(a,a+ins.size))
        if not span<=raw or span&set(owners):
            conflicts.append(dict(address=a,size=ins.size,parent=parent,edge=edge,reason='instruction_extent_overlap'));continue
        instructions[a]=(ins,parent,edge,seed)
        owners.update({p:a for p in span})
        for kind,target in direct_edges(rom,a,ins.size):
            if target is None:blocked.append(dict(address=None,parent=a,edge=kind,reason='unknown_indirect_target'))
            else:queue.append((target,a,kind,seed))
    if conflicts:raise ValueError('instruction conflicts: '+json.dumps(conflicts))
    records=[];lines=['| Original secondary-command conditional descendants omitted by the old decoder map.',
        '| E068 original signed table membership, then raw-opcode direct CFG; no natural domain claim.',
        '.cpu 68000','.section .text','_start:']
    for a,(ins,parent,edge,seed) in sorted(instructions.items()):
        records.append(dict(address=a,size=ins.size,bytes=bytes(ins.bytes).hex(),original_mnemonic=ins.mnemonic,
            original_operand=ins.op_str,confidence='candidate',conditional_seed=seed,
            table_indices=seeds.get(a,[]),direct_parent=parent,edge_type=edge))
        lines.extend([f'.org 0x{a:X}',f'| {bytes(ins.bytes).hex()} conditional seed {seed:06X}',
            f'm68k_{a:06x}:','        '+format_instruction(ins),f'm68k_{a:06x}_end:'])
    source=('\n'.join(lines)+'\n').encode();validate_source(source,records)
    ledger=m.dump(records);size=sum(r['size'] for r in records)
    manifest=dict(format='g5510-secondary-dispatch-code-v1',confidence='candidate',
        instructions=len(records),bytes=size,table_proof=table,seeds=seeds,
        ranges=m.coalesce(records),instructions_sha256=m.sha(ledger),canonical_source_sha256=m.sha(source),
        prior_source_sha256=pins,prior_instructions=52100,prior_code_bytes=197090,
        original_rom_sha256=f.ROM_SHA,baseline_layout=str(BASE_LAYOUT.relative_to(ROOT)).replace('\\','/'),
        blocked=blocked,conflicts=conflicts,unknown_indirect_target_count=sum(row['reason']=='unknown_indirect_target' for row in blocked),
        ownership_bytes_added=0,natural_entries_added=0,complete_indirect_domains_added=0,
        statement='Physical original21-slot secondary table, excluding bypassed6, followed only by direct opcode edges. Not a closed F65A domain, natural runtime trace or semantic completion.')
    return {'instructions.json':ledger,'manifest.json':m.dump(manifest),'secondary_dispatch_descendants.s':source}

def inventory(rom):
    m.af.verify_rom(rom);data=m.read(LEDGER)
    if m.sha(data)!=LEDGER_SHA:raise ValueError('secondary ledger differs')
    rows=json.loads(data);end=0
    for row in rows:
        a,size=row['address'],row['size']
        if type(a)is not int or type(size)is not int or a&1 or size&1 or not 2<=size<=10 or a<end or a+size>f.ROM_SIZE:raise ValueError('secondary instruction extent differs')
        if bytes.fromhex(row['bytes'])!=rom[a:a+size] or row['confidence']!='candidate':raise ValueError('original secondary instruction differs')
        end=a+size
    if len(rows)!=COUNT or sum(r['size'] for r in rows)!=BYTES:raise ValueError('sealed secondary count differs')
    return rows

def verify_image(rom,source,object_data,image,canonical=False):
    rows=inventory(rom);validate_source(source,rows)
    if verify_object(object_data,rows)!=image or len(image)!=rows[-1]['address']+rows[-1]['size']:raise ValueError('secondary ELF/image differs')
    positions={p for row in rows for p in range(row['address'],row['address']+row['size'])}
    if any(value for p,value in enumerate(image) if p not in positions):raise ValueError('secondary sparse padding changed')
    if canonical and any(image[r['address']:r['address']+r['size']]!=rom[r['address']:r['address']+r['size']] for r in rows):raise ValueError('canonical secondary opcodes differ')
    return dict(instructions=COUNT,compiled_bytes=BYTES,elf_labels=2*COUNT,canonical=canonical,
        ownership_bytes_added=0,complete_indirect_domains_added=0)

def add_to_layout(rom,source,base):
    rows=inventory(rom);validate_source(source,rows)
    positions={p for row in rows for p in range(row['address'],row['address']+row['size'])}
    if not positions<=d.raw_positions(base):raise ValueError('secondary code overlaps existing authority')
    ranges=m.coalesce(rows);result=dict(base);consumed=[]
    for bank in range(16):
        lines=[]
        for line in base[f'm68k_bank{bank:02x}.s'].decode().splitlines():
            match=re.fullmatch(d.PATTERN,line)
            if not match:lines.append(line);continue
            first=bank*65536+int(match[2],16);last=first+int(match[3],16);cursor=first
            for a,z in ranges:
                if z<=first or a>=last:continue
                left,right=max(a,first),min(z,last)
                if cursor<left:lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{left-cursor:X}')
                lines.append(f'        .incbin "m68k_secondary_dispatch_code.bin", 0x{left:X}, 0x{right-left:X}')
                consumed.extend(range(left,right));cursor=right
            if cursor<last:lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{last-cursor:X}')
        result[f'm68k_bank{bank:02x}.s']=('\n'.join(lines)+'\n').encode()
    if len(consumed)!=BYTES or set(consumed)!=positions:raise ValueError('secondary code omitted/duplicated')
    info=json.loads(base['manifest.json'])
    if info['compiled_instruction_union']!=52100 or info['compiled_code_union_bytes']!=197090:raise ValueError('prior code union differs')
    info.update(secondary_dispatch_code_bytes=BYTES,secondary_dispatch_code_instructions=COUNT,
        secondary_dispatch_code_ledger_sha256=LEDGER_SHA,secondary_dispatch_code_source_sha256=m.sha(source),
        secondary_dispatch_code_confidence='candidate',compiled_instruction_union=52100+COUNT,
        compiled_code_union_bytes=197090+BYTES,compiled_or_typed_bytes=info['compiled_or_typed_bytes']+BYTES,
        remaining_raw_slice_bytes=info['remaining_raw_slice_bytes']-BYTES,secondary_dispatch_code_owner_bytes_added=0)
    result['manifest.json']=m.dump(info);return result

def overlay(rom,baseline,image):
    if type(baseline)is not bytes or len(baseline)!=f.ROM_SIZE:raise ValueError('full baseline required')
    rows=inventory(rom)
    if len(image)!=rows[-1]['address']+rows[-1]['size']:raise ValueError('secondary image extent differs')
    result=bytearray(baseline)
    for row in rows:
        a,z=row['address'],row['address']+row['size'];result[a:z]=image[a:z]
    return bytes(result)

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','verify-object'))
    p.add_argument('--rom',default=str(f.DEFAULT_ROM));p.add_argument('--source',default=str(SOURCE))
    p.add_argument('--output-root');p.add_argument('--object');p.add_argument('--image');p.add_argument('--canonical',action='store_true')
    args=p.parse_args(argv);rom=m.read(args.rom,f.ROM_SIZE)
    if args.command=='export':
        if not args.output_root:raise ValueError('fresh output root required')
        target=m.af.safe_path(args.output_root);m.af._separate(target,[m.af.safe_path(args.rom,regular_input=True)])
        if target.exists():raise ValueError('fresh output directory required')
        bundle=export_bundle(rom);target.mkdir(parents=True)
        for name,data in bundle.items():
            with (target/name).open('xb') as stream:stream.write(data)
        info=json.loads(bundle['manifest.json']);print(json.dumps({k:info[k] for k in ('instructions','bytes','instructions_sha256','canonical_source_sha256','ranges','blocked','seeds')}))
    else:
        if not args.object or not args.image:raise ValueError('actual GNU object/image required')
        print(json.dumps(verify_image(rom,m.read(args.source),m.read(args.object),m.read(args.image),args.canonical)))
    return 0

if __name__=='__main__':raise SystemExit(main())
