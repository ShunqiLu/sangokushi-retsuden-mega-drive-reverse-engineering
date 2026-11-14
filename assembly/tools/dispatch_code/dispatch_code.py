"""Editable conditional dispatch descendants of the eight prior mnemonic sources."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse,csv,io,json,re
from collections import defaultdict,deque,Counter
from pathlib import Path
from tools.direct_code import direct_code as d
from tools.m68k_build.elf_verify import verify_object

ROOT=d.ROOT;m=d.m;f=d.f
LEDGER=ROOT/'analysis/dispatch_code/generated/instructions.json'
SOURCE=ROOT/'src/m68k/dispatch_descendants.s'
LEDGER_SHA=reference_value(__name__, 'LEDGER_SHA')
SEEDS=(*d.SEEDS,'direct_descendants')
EVIDENCE=ROOT/'analysis/code/phase3_indirect/generated/indirect_evidence.json'
MAP_ROOT=ROOT/'analysis/code/phase3_indirect/generated/enhanced_map'
FORBIDDEN=((0x3DC54,0x3DC90),(0x4FBE4,0x51BBB),(0x51BBC,0x53421),
    (0x53422,0x5415F),(0x54160,0x546DF),(0x546E0,0x55FA5),
    (0x55FA6,0x57579),(0x5757A,0x58A5F),(0x58A60,0x59E03),
    (0x59E04,0x5A2B3),(0x5A2B4,0x5B99B),(0x5B99C,0x5CA95),(0x5CA96,0x5CDE1))
MNEMONICS=d.MNEMONICS|{'seq','sne','scc','scs','sge','sgt','sle','slt','shi','sls','smi','spl','svc','svs','negx','tas','bge','bgt','ble','blt','divs'}
COUNT=18137;BYTES=69156
def validate_source(source,records):return m.validate_source(source,records,allowed_mnemonics=MNEMONICS)
def base_layout(rom):
    base=d.add_to_layout(rom,m.read(d.SOURCE),d.base_layout(rom))
    path=ROOT/'analysis/sprite_word_resources/generated/fields.json'
    if path.exists():
        from tools.sprite_word_resources import codec as sprite
        base=d.add_sprite_resources(rom,sprite.load_fields(m.read(path)),base)
    return base
def forbidden(a,z):return any(a<last and first<z for first,last in FORBIDDEN)
def signed(value,bits):return value-(1<<bits) if value&(1<<(bits-1)) else value
def word(rom,a):return int.from_bytes(rom[a:a+2],'big')
def byte_row(rom,rows,address):
    row=rows.get(address)
    if row is None or bytes.fromhex(row['bytes'])!=rom[address:address+int(row['size'])]:raise ValueError('consumer/target original instruction mismatch')
    return row
def brief_pc(rom,address):
    extension=word(rom,address+2)
    if extension&0x8F00:raise ValueError('only original 68000 Dn.W brief index supported')
    return address+2+signed(extension&255,8),(extension>>12)&7
def verify_site(rom,site,rows,prior):
    """Recheck the table-read xref and target arithmetic from original words."""
    source=site['source'];row=byte_row(rom,rows,source)
    if source not in prior or rom[source:source+int(row['size'])].hex()!=site['source_bytes']:raise ValueError('dispatch source not in original eight-source scope')
    op=word(rom,source);table=site['table'];kind=table['kind'];context=[]
    if op&0xFFC0 not in (0x4E80,0x4EC0):raise ValueError('source is not JSR/JMP')
    if kind in ('bra_w_trampoline_table','signed_word_relative_offset_table'):
        mode,reg=(op>>3)&7,op&7
        if (mode,reg)==(7,3):base,index=brief_pc(rom,source)
        elif mode==6:
            extension=word(rom,source+2)
            if extension&0x8FFF:raise ValueError('unsupported address-register indexed dispatch')
            index=(extension>>12)&7;base=table['dispatch_base'];areg=reg
            candidates=[]
            for a in sorted(rows):
                if not source-96<=a<source or a not in prior:continue
                if word(rom,a)&0xF1FF==0x41FA and (word(rom,a)>>9)&7==areg and a+2+signed(word(rom,a+2),16)==base:candidates.append(a)
            if not candidates:raise ValueError('missing original PC-relative LEA consumer base xref')
            context.append(candidates[-1])
        else:raise ValueError('unsupported dispatch effective address')
        if base!=table['dispatch_base']:raise ValueError('raw PC base differs from table metadata')
        if kind=='signed_word_relative_offset_table':
            load=table['offset_load_address'];byte_row(rom,rows,load);loadop=word(rom,load)
            if load not in prior or loadop&0xF1FF!=0x303B or (loadop>>9)&7!=index:raise ValueError('original WORD offset reader/destination differs')
            nominal,reader_index=brief_pc(rom,load)
            if nominal!=table['nominal_table_base'] or table['index_register']!=f'd{index}':raise ValueError('raw table-read base/index differs')
            context.append(load)
        else:reader_index=index
    elif kind=='absolute_long_function_pointer_table':
        load=table['pointer_load_address'];byte_row(rom,rows,load);loadop=word(rom,load)
        if source not in prior or load not in prior or op&0xFFF8!=0x4E90 or loadop&0xF1FF!=0x207B or (loadop>>9)&7!=op&7:raise ValueError('original MOVEA.L pointer consumer differs')
        nominal,reader_index=brief_pc(rom,load)
        if nominal!=table['table_start'] or table['index_register']!=f'd{reader_index}':raise ValueError('original pointer-reader base/index differs')
        context.append(load);base=None
    else:raise ValueError('unsupported encoded table kind')
    expected_width=4 if kind!='signed_word_relative_offset_table' else 2
    entries=table['entries']
    if table['entry_width']!=expected_width or len(entries)!=table['entry_count'] or table['end_exclusive']-table['table_start']!=expected_width*len(entries):raise ValueError('table extent/width differs')
    members=defaultdict(list)
    for index,entry in enumerate(entries):
        a=table['table_start']+expected_width*index;raw=rom[a:a+expected_width]
        if entry['index']!=index or entry['entry_address']!=a or raw.hex()!=entry['entry_bytes']:raise ValueError('original encoded table slot differs')
        if kind=='bra_w_trampoline_table':
            if raw[:2]!=b'\x60\x00':raise ValueError('slot is not original BRA.W')
            target=a
            if a+2+signed(int.from_bytes(raw[2:],'big'),16)!=entry['branch_target']:raise ValueError('original BRA.W target differs')
        elif kind=='signed_word_relative_offset_table':target=base+signed(int.from_bytes(raw,'big'),16)
        else:target=int.from_bytes(raw,'big')
        if target!=entry['effective_target'] or target&1 or target<0x200 or target>=len(rom):raise ValueError('original table arithmetic target differs')
        target_row=byte_row(rom,rows,target)
        if rom[target:target+int(target_row['size'])].hex()!=entry['target_bytes']:raise ValueError('table target original word differs')
        members[target].append(index)
    # Actual local scale instructions are recorded, never converted to a natural
    # index-domain proof. Some consumers receive already-computed byte offsets.
    scale=[];limit=context[-1] if kind!='bra_w_trampoline_table' else source
    for a in sorted(rows):
        if not limit-96<=a<limit or a not in prior:continue
        raw=word(rom,a)
        if raw in (0xE340+reader_index,0xE348+reader_index,0xE540+reader_index,0xE548+reader_index):scale.append(dict(address=a,bytes=rows[a]['bytes'],shift_count=1 if raw&0xF00==0x300 else 2))
    return members,dict(source=source,source_bytes=site['source_bytes'],kind=kind,table_start=table['table_start'],table_end=table['end_exclusive'],
        entry_width=expected_width,entries=len(entries),consumer_context=[dict(address=a,bytes=rows[a]['bytes']) for a in context],
        encoded_index_scale=scale,index_register=f'd{reader_index}',natural_index_domain='unknown',confidence='candidate')
def export_bundle(rom):
    from tools.code_analysis.m68k_code_map import load_capstone
    from tools.m68k_build.source import format_instruction
    m.af.verify_rom(rom);base=base_layout(rom);raw=d.raw_positions(base)
    for a,z in FORBIDDEN:raw.difference_update(range(a,z))
    prior=set();pins={}
    for name in SEEDS:
        data=m.read(ROOT/f'src/m68k/{name}.s');pins[name]=m.sha(data)
        prior.update(int(a,16) for a in re.findall(r'^m68k_([0-9a-f]{6}):$',data.decode(),re.M))
    if len(prior)!=20877:raise ValueError('prior eight-source topology changed')
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
    if sum(prior_sizes.values())!=77504:raise ValueError('prior code byte count changed')
    evidence_data=m.read(EVIDENCE);document=json.loads(evidence_data)
    if document['rom']['sha256'].lower()!=f.ROM_SHA:raise ValueError('indirect evidence ROM differs')
    members={};tables=[]
    for site in document['sites']:
        if site['source'] not in prior:continue
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
    records=[];lines=['| Candidate conditional table-dispatch descendants of the prior eight sources.',
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
    info=dict(format='g5510-dispatch-code-v1',confidence='candidate',instructions=COUNT,bytes=BYTES,conditional_seed_instructions=len(seeds),
        table_proofs=tables,prior_instructions=20877,prior_code_bytes=77504,compiled_instruction_union=20877+COUNT,compiled_code_union_bytes=77504+BYTES,
        ranges=m.coalesce(records),instructions_sha256=m.sha(ledger),canonical_source_sha256=m.sha(source),prior_source_sha256=pins,
        original_rom_sha256=f.ROM_SHA,instruction_map_sha256=m.sha(map_data),edges_sha256=m.sha(edge_data),indirect_evidence_sha256=m.sha(evidence_data),
        raw_bytes_before=len(raw),blocked=blocked,forbidden_asset_directories=FORBIDDEN,remaining_heuristic_instruction_bytes=119586-BYTES,
        ownership_bytes_added=0,natural_entries_added=0,complete_indirect_domains_added=0,
        statement='Conditional original-table code only; eight-source-external nested dispatches are not followed; no natural index-domain proof.')
    return {'instructions.json':ledger,'manifest.json':m.dump(info),'dispatch_descendants.s':source}
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
                lines.append(f'        .incbin "m68k_dispatch_code.bin", 0x{first_piece:X}, 0x{last_piece-first_piece:X}')
                consumed.extend(range(first_piece,last_piece));cursor=last_piece
            if cursor<last:lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{last-cursor:X}')
        result[f'm68k_bank{bank:02x}.s']=('\n'.join(lines)+'\n').encode()
    if len(consumed)!=BYTES or set(consumed)!=positions:raise ValueError('dispatch code omitted/duplicated')
    info=json.loads(base['manifest.json']);info.update(dispatch_code_bytes=BYTES,dispatch_code_instructions=COUNT,dispatch_code_ledger_sha256=LEDGER_SHA,
        dispatch_code_source_sha256=m.sha(source),dispatch_code_confidence='candidate',compiled_instruction_union=20877+COUNT,compiled_code_union_bytes=77504+BYTES,
        compiled_or_typed_bytes=info['compiled_or_typed_bytes']+BYTES,remaining_raw_slice_bytes=info['remaining_raw_slice_bytes']-BYTES,dispatch_code_owner_bytes_added=0)
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
