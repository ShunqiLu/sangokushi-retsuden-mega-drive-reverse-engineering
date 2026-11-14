"""Iteration three: final conditional descendants of the ten prior sources."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse,csv,io,json,re
from collections import defaultdict,deque,Counter
from pathlib import Path
from tools.direct_code import direct_code as d
from tools.nested_dispatch_code import nested_dispatch_code as previous
from tools.m68k_build.elf_verify import verify_object

ROOT=d.ROOT;m=d.m;f=d.f
LEDGER=ROOT/'analysis/final_dispatch_code/generated/instructions.json'
SOURCE=ROOT/'src/m68k/final_dispatch_descendants.s'
LEDGER_SHA=reference_value(__name__, 'LEDGER_SHA')
SEEDS=(*previous.SEEDS,'nested_dispatch_descendants')
EVIDENCE=ROOT/'analysis/code/phase3_indirect/generated/indirect_evidence.json'
MAP_ROOT=ROOT/'analysis/code/phase3_indirect/generated/enhanced_map'
FORBIDDEN=(*previous.FORBIDDEN,(0x357F8,0x387BA),(0x38C28,0x38E50))
MNEMONICS=previous.MNEMONICS
COUNT=1202;BYTES=5206
def validate_source(source,records):return m.validate_source(source,records,allowed_mnemonics=MNEMONICS)
def base_layout(rom):
    return previous.add_to_layout(rom,m.read(previous.SOURCE),previous.base_layout(rom))
def forbidden(a,z):return any(a<last and first<z for first,last in FORBIDDEN)
byte_row=previous.byte_row
verify_site=previous.verify_site
def export_bundle(rom):
    from tools.code_analysis.m68k_code_map import load_capstone
    from tools.m68k_build.source import format_instruction
    m.af.verify_rom(rom);base=base_layout(rom);raw=d.raw_positions(base)
    for a,z in FORBIDDEN:raw.difference_update(range(a,z))
    prior=set();pins={}
    for name in SEEDS:
        data=m.read(ROOT/f'src/m68k/{name}.s');pins[name]=m.sha(data)
        prior.update(int(a,16) for a in re.findall(r'^m68k_([0-9a-f]{6}):$',data.decode(),re.M))
    if len(prior)!=50898:raise ValueError('prior ten-source topology changed')
    map_data=m.read(m.INSTRUCTIONS)
    if m.sha(map_data)!=m.INSTRUCTIONS_HASH:raise ValueError('instruction map changed')
    rows={int(r['address']):r for r in csv.DictReader(io.StringIO(map_data.decode('utf-8-sig')))}
    cap=load_capstone()
    if cap.__version__!='5.0.6':raise ValueError('explicit export requires Capstone 5.0.6')
    decoder=cap.Cs(cap.CS_ARCH_M68K,cap.CS_MODE_BIG_ENDIAN|cap.CS_MODE_M68K_000);decoder.detail=True
    # Existing candidate sources include a few accepted original instructions
    # absent from this earlier enhanced map. They are not new dispatch seeds.
    prior_sizes={a:int(rows[a]['size']) for a in prior if a in rows}
    for a in prior:
        if a in rows:byte_row(rom,rows,a)
        else:
            ins=next(decoder.disasm(rom[a:a+10],a,count=1),None)
            if ins is None:raise ValueError('prior original instruction cannot decode')
            prior_sizes[a]=ins.size
    if sum(prior_sizes.values())!=191884:raise ValueError('prior code byte count changed')
    evidence_data=m.read(EVIDENCE);document=json.loads(evidence_data)
    if document['rom']['sha256'].lower()!=f.ROM_SHA:raise ValueError('indirect evidence ROM differs')
    earlier={int(a,16) for name in previous.SEEDS for a in re.findall(r'^m68k_([0-9a-f]{6}):$',m.read(ROOT/f'src/m68k/{name}.s').decode(),re.M)}
    members={};tables=[]
    for site in document['sites']:
        if site['source'] not in prior or site['source'] in earlier:continue
        table_members,proof=verify_site(rom,site,rows,prior);tables.append(proof)
        for target,indices in table_members.items():members[(site['source'],target)]=indices
    seeds={}
    for a,row in rows.items():
        if not all(p in raw for p in range(a,a+int(row['size']))):continue
        for e in json.loads(row['discovery_evidence']):
            if e['type'] not in ('static_indirect_table_member','pc_indexed_dispatch_slot') or e['source_address'] not in prior:continue
            key=(e['source_address'],a)
            if key not in members:raise ValueError('discovery seed lacks validated encoded table membership')
            seeds.setdefault(a,[]).append(dict(type=e['type'],source_address=e['source_address'],table_indices=members[key]))
    edge_data=m.read(MAP_ROOT/'edges.csv');edges=defaultdict(list)
    for e in csv.DictReader(io.StringIO(edge_data.decode('utf-8-sig'))):
        if e['direct']=='True' and e['target'] and e['evidence_type']=='direct_control_flow':edges[int(e['source'])].append(e)
    queue=deque(sorted(seeds));seen=set(seeds);parent={};origin={a:a for a in seeds};blocked=[]
    while queue:
        a=queue.popleft()
        for e in edges[a]:
            d.raw_edge(rom,rows[a],e);target=int(e['target'])
            if target in prior or target in seen:continue
            r=rows.get(target)
            if r and all(p in raw for p in range(target,target+int(r['size']))):seen.add(target);parent[target]=e;origin[target]=origin[a];queue.append(target)
            else:blocked.append(e)
    records=[];lines=['| Candidate conditional table-dispatch descendants of the prior ten sources.',
        '| Encoded table membership is checked; natural index domain remains unknown.','.cpu 68000','.section .text','_start:']
    for a in sorted(seen):
        r=rows[a];size=int(r['size']);data=bytes.fromhex(r['bytes']);ins=next(decoder.disasm(rom[a:a+size],a,count=1),None)
        if ins is None or ins.size!=size or bytes(ins.bytes)!=data or data!=rom[a:a+size] or forbidden(a,a+size):raise ValueError('decoded instruction extent/identity/authority mismatch')
        p=parent.get(a)
        records.append(dict(address=a,size=size,bytes=data.hex(),original_mnemonic=r['mnemonic'],original_operand=r['operand'],
            discovery_confidence=r['confidence'],confidence='candidate',conditional_seed=origin[a],seed_evidence=seeds.get(a,[]),
            direct_parent=int(p['source']) if p else None,edge_type=p['type'] if p else 'conditional_table_member'))
        lines.extend([f'.org 0x{a:X}',f'| {data.hex()} conditional seed {origin[a]:06X}',f'm68k_{a:06x}:','        '+format_instruction(ins),f'm68k_{a:06x}_end:'])
    source=('\n'.join(lines)+'\n').encode();validate_source(source,records)
    if len(records)!=COUNT or sum(r['size'] for r in records)!=BYTES:raise ValueError('conditional batch fixed scope changed')
    ledger=m.dump(records)
    info=dict(format='g5510-final-dispatch-code-v1',confidence='candidate',instructions=COUNT,bytes=BYTES,conditional_seed_instructions=len(seeds),
        table_proofs=tables,prior_instructions=50898,prior_code_bytes=191884,compiled_instruction_union=50898+COUNT,compiled_code_union_bytes=191884+BYTES,
        ranges=m.coalesce(records),instructions_sha256=m.sha(ledger),canonical_source_sha256=m.sha(source),prior_source_sha256=pins,
        original_rom_sha256=f.ROM_SHA,instruction_map_sha256=m.sha(map_data),edges_sha256=m.sha(edge_data),indirect_evidence_sha256=m.sha(evidence_data),
        raw_bytes_before=len(raw),blocked=blocked,forbidden_data_spans=FORBIDDEN,iteration=3,remaining_heuristic_instruction_bytes=5206-BYTES,
        ownership_bytes_added=0,natural_entries_added=0,complete_indirect_domains_added=0,
        statement='Conditional original-table code only; ten-source-external nested dispatches are not followed; no natural index-domain proof.')
    return {'instructions.json':ledger,'manifest.json':m.dump(info),'final_dispatch_descendants.s':source}
def inventory(rom):
    m.af.verify_rom(rom);data=m.read(LEDGER)
    if m.sha(data)!=LEDGER_SHA:raise ValueError('dispatch ledger changed')
    rows=json.loads(data);end=0
    for r in rows:
        a,size=r['address'],r['size']
        if type(a)is not int or type(size)is not int or a&1 or not 2<=size<=10 or size&1 or a<end or a+size>f.ROM_SIZE or forbidden(a,a+size):raise ValueError('bad instruction extent/asset overlap')
        if bytes.fromhex(r['bytes'])!=rom[a:a+size] or r['confidence']!='candidate':raise ValueError('instruction identity/classification differs')
        end=a+size
    if len(rows)!=COUNT or sum(r['size'] for r in rows)!=BYTES:raise ValueError('scope differs')
    return rows
def verify_image(rom,source,object_data,image,canonical=False):
    rows=inventory(rom);validate_source(source,rows)
    if verify_object(object_data,rows)!=image or len(image)!=rows[-1]['address']+rows[-1]['size']:raise ValueError('ELF/image extent differ')
    positions={p for r in rows for p in range(r['address'],r['address']+r['size'])}
    for row in rows:
        a,z=row['address'],row['address']+row['size']
        if canonical and image[a:z]!=rom[a:z]:raise ValueError('canonical mnemonic bytes differ')
    if any(value for a,value in enumerate(image) if a not in positions):raise ValueError('sparse padding changed')
    return dict(instructions=len(rows),compiled_bytes=len(positions),elf_labels=len(rows)*2,canonical=canonical,ownership_bytes_added=0,complete_indirect_domains_added=0)
def add_to_layout(rom,source,base):
    rows=inventory(rom);validate_source(source,rows);raw=d.raw_positions(base)
    positions={p for r in rows for p in range(r['address'],r['address']+r['size'])}
    if not positions<=raw:raise ValueError('dispatch instructions overlap existing authority')
    ranges=m.coalesce(rows);consumed=[];result=dict(base)
    for bank in range(16):
        lines=[]
        for line in base[f'm68k_bank{bank:02x}.s'].decode().splitlines():
            match=re.fullmatch(d.PATTERN,line)
            if not match:lines.append(line);continue
            first=bank*65536+int(match[2],16);last=first+int(match[3],16);cursor=first
            for a,z in ranges:
                if z<=first or a>=last:continue
                # CPU instruction extents remain whole in source/ELF. Only the
                # physical ROM-bank output slices are split at raw boundaries.
                first_piece,last_piece=max(a,first),min(z,last)
                if cursor<first_piece:lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{first_piece-cursor:X}')
                lines.append(f'        .incbin "m68k_final_dispatch_code.bin", 0x{first_piece:X}, 0x{last_piece-first_piece:X}')
                consumed.extend(range(first_piece,last_piece));cursor=last_piece
            if cursor<last:lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{last-cursor:X}')
        result[f'm68k_bank{bank:02x}.s']=('\n'.join(lines)+'\n').encode()
    if len(consumed)!=BYTES or set(consumed)!=positions:raise ValueError('dispatch code omitted/duplicated')
    info=json.loads(base['manifest.json']);info.update(final_dispatch_code_bytes=BYTES,final_dispatch_code_instructions=COUNT,final_dispatch_code_ledger_sha256=LEDGER_SHA,
        final_dispatch_code_source_sha256=m.sha(source),final_dispatch_code_confidence='candidate',compiled_instruction_union=50898+COUNT,compiled_code_union_bytes=191884+BYTES,
        compiled_or_typed_bytes=info['compiled_or_typed_bytes']+BYTES,remaining_raw_slice_bytes=info['remaining_raw_slice_bytes']-BYTES,final_dispatch_code_owner_bytes_added=0)
    result['manifest.json']=m.dump(info);return result
def overlay(rom,baseline,image):
    if type(baseline)is not bytes or len(baseline)!=f.ROM_SIZE:raise ValueError('full baseline required')
    rows=inventory(rom)
    if len(image)!=rows[-1]['address']+rows[-1]['size']:raise ValueError('compiled image extent differs')
    output=bytearray(baseline)
    for r in rows:
        a,z=r['address'],r['address']+r['size'];output[a:z]=image[a:z]
    return bytes(output)
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('export','prepare','verify-object'))
    parser.add_argument('--rom',default=str(f.DEFAULT_ROM));parser.add_argument('--source',default=str(SOURCE));parser.add_argument('--output-root')
    parser.add_argument('--object');parser.add_argument('--image');parser.add_argument('--canonical',action='store_true');args=parser.parse_args(argv)
    rom=m.read(args.rom,f.ROM_SIZE)
    if args.command=='export':
        if not args.output_root:raise ValueError('fresh output-root required')
        target=m.af.safe_path(args.output_root);m.af._separate(target,[m.af.safe_path(args.rom,regular_input=True)])
        if target.exists():raise ValueError('fresh directory required')
        bundle=export_bundle(rom);target.mkdir(parents=True)
        for name,data in bundle.items():
            with (target/name).open('xb') as stream:stream.write(data)
        print(m.sha(bundle['instructions.json']))
    elif args.command=='prepare':
        if not args.output_root:raise ValueError('output-root required')
        result=add_to_layout(rom,m.read(args.source),base_layout(rom))
        print(m.publish_content_addressed(result,args.output_root,[args.rom,args.source,LEDGER]))
    else:
        if not args.object or not args.image:raise ValueError('actual object/image required')
        print(json.dumps(verify_image(rom,m.read(args.source),m.read(args.object),m.read(args.image),args.canonical)))
    return 0
if __name__=='__main__':raise SystemExit(main())
