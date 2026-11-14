"""1864 source bytes for the actual40446→3B13C battle-effect sprite consumer.

Eight base BYTEs,192 BE32 pointers,192 full attribute WORDs,128 descriptors.
128 unread one-BYTE tails remain raw. No physical selector clamp is invented.
"""
import argparse,json
from pathlib import Path
from tools.vdp_word_streams import format as f
from tools.battle_scene_sprites import codec as sprite

ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=f.DEFAULT_ROM;FORMAL_ROOT=ROOT/'analysis/battle_effect_sprites/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json';OUTPUT_ROOT=ROOT/'build/battle_effect_sprites'
FORMAT='candidate-battle-effect-indexed-sprite-source-v1'
BASES,POINTERS,ATTRIBUTES,DESCRIPTORS,END=0x404CC,0x404D4,0x407D4,0x40954,0x40C94
EDITABLE_BYTES=1864
sha,dump,keys,uint,load_fields=f.sha,f.dump,f.keys,f.uint,f.load_json
ANCHORS={0x4045A:'41fa00704e7112300000',0x40464:'0c38000380db660412300004',
         0x40492:'302e0008e540d2403038f320e64802400003d0413800e540207b0028',
         0x404AE:'302e0002322e0004343c00057600e34443fa03144e71383140004efaac72'}

def ident(a):return f'rom_{a:06X}_effect_sprite'
def metadata():return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
    confidence='confirmed_encoding_candidate_effect_role',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def exact(value,count,label):
    if type(value)is not list or len(value)!=count:raise ValueError(label+': fixed allocation differs')
    return value
def verify_rom(rom):
    if type(rom)is not bytes or len(rom)!=f.ROM_SIZE or sha(rom)!=f.ROM_SHA:raise ValueError('canonical immutable ROM required')
    for pc,raw in ANCHORS.items():
        if rom[pc:pc+len(raw)//2]!=bytes.fromhex(raw):raise ValueError('original indexed effect consumer differs')
    if sha(rom[sprite.READER_START:sprite.READER_END])!=sprite.READER_SHA:raise ValueError('original complete sprite reader differs')
def topology(rom):
    verify_rom(rom);targets=[int.from_bytes(rom[p:p+4],'big') for p in range(POINTERS,ATTRIBUTES,4)]
    starts=sorted(set(targets))
    if len(starts)!=128 or starts[0]!=DESCRIPTORS or starts[-1]!=0x40C8A:raise ValueError('original physical sprite catalog differs')
    rows=[]
    for a,z in zip(starts,starts[1:]+[END]):
        p=a
        while p<z and rom[p]!=128:
            if p+4>z:raise ValueError('partial original sprite record')
            p+=4
        if p>=z or p==a:raise ValueError('original first80 source terminal differs')
        rows.append(dict(id=ident(a),start=a,end=p+1,unread_interval=[p+1,z],count=(p-a)//4))
    if sum(r['end']-r['start'] for r in rows)!=704 or sum(r['count'] for r in rows)!=144:raise ValueError('original descriptor count differs')
    return targets,rows
def extract(rom):
    targets,rows=topology(rom);fields=metadata()
    fields.update(base_selector_BYTES=list(rom[BASES:POINTERS]),directory_targets=[ident(t) for t in targets],
        attribute_WORDs=[int.from_bytes(rom[p:p+2],'big') for p in range(ATTRIBUTES,DESCRIPTORS,2)],
        descriptors=[dict(**row,records=[sprite.record(rom[p:p+4]) for p in range(row['start'],row['end']-1,4)]) for row in rows])
    blocks(rom,fields);return fields
def blocks(rom,fields):
    _,rows=topology(rom);fixed=metadata();keys(fields,set(fixed)|{'base_selector_BYTES','directory_targets','attribute_WORDs','descriptors'},'package')
    for key,value in fixed.items():f.same(fields[key],value,'package.'+key)
    selectors=bytes(uint(v,255,'base selector BYTE') for v in exact(fields['base_selector_BYTES'],8,'base BYTEs'))
    catalog={r['id']:r['start'] for r in rows};refs=exact(fields['directory_targets'],192,'pointer slots')
    if any(type(ref)is not str or ref not in catalog for ref in refs):raise ValueError('pointer must name existing complete effect source')
    pointers=b''.join(catalog[ref].to_bytes(4,'big') for ref in refs)
    attributes=b''.join(uint(v,65535,'full source attribute WORD').to_bytes(2,'big') for v in exact(fields['attribute_WORDs'],192,'attribute WORDs'))
    result=[dict(id='effect_base_selectors',start=BASES,end=POINTERS,data=selectors,role='effect_base_selector_BYTEs'),
        dict(id='effect_directory',start=POINTERS,end=ATTRIBUTES,data=pointers,role='effect_BE32_pointer_directory'),
        dict(id='effect_attributes',start=ATTRIBUTES,end=DESCRIPTORS,data=attributes,role='effect_full_source_attribute_WORDs')]
    for descriptor,row in zip(exact(fields['descriptors'],128,'descriptors'),rows):
        keys(descriptor,set(row)|{'records'},'descriptor')
        for key,value in row.items():f.same(descriptor[key],value,'descriptor.'+key)
        data=b''.join(sprite.record_bytes(v) for v in exact(descriptor['records'],row['count'],'source records'))+b'\x80'
        result.append(dict(id=row['id'],start=row['start'],end=row['end'],data=data,role='effect_four_BYTE_sprite_source'))
    if sum(len(r['data']) for r in result)!=EDITABLE_BYTES:raise ValueError('fixed effect source bytes differ')
    return result
def rebuild(rom,fields):
    image=bytearray(rom)
    for r in blocks(rom,fields):image[r['start']:r['end']]=r['data']
    return bytes(image)
def signed(word):return word-65536 if word&32768 else word
def original_plan(rom,type_byte,mode_byte,side_swap_word,record_address,state_word,tick_word):
    """Original WORD shifts/sign-indexed reads; arbitrary indices are not clamped."""
    verify_rom(rom)
    for value,bits,label in ((type_byte,8,'type BYTE'),(mode_byte,8,'mode BYTE'),(side_swap_word,16,'swap WORD'),
        (record_address,32,'A6 LONG'),(state_word,16,'state WORD'),(tick_word,16,'tick WORD')):uint(value,(1<<bits)-1,label)
    selector_address=BASES+type_byte+(4 if mode_byte==3 else 0);base=rom[selector_address]
    adjustment=96 if ((record_address>=0xFFFF826A) if not side_swap_word else (record_address<0xFFFF826A)) else 0
    index=(base+adjustment+((state_word<<2)&65535)+((tick_word>>3)&3))&65535
    pointer_address=POINTERS+signed((index<<2)&65535);attribute_address=ATTRIBUTES+signed((index<<1)&65535)
    if pointer_address<0 or pointer_address+4>len(rom) or attribute_address<0 or attribute_address+2>len(rom):raise ValueError('indexed source read outside mapped ROM')
    return dict(selector_address=selector_address,index_word=index,pointer_address=pointer_address,
        source_pointer=int.from_bytes(rom[pointer_address:pointer_address+4],'big'),attribute_address=attribute_address,
        source_attribute_word=int.from_bytes(rom[attribute_address:attribute_address+2],'big'),
        in_physical_editor_catalog=index<192)
def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('whole ROM serialized source roundtrip differs')
    _,rows=topology(rom)
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=131,base_BYTEs=8,
        pointer_slots=192,pointer_bytes=768,attribute_WORDs=192,attribute_bytes=384,
        descriptors=128,source_records=144,descriptor_bytes=704,first80_terminal_BYTEs=128,
        unread_bytes_excluded=128,unknown_intervals=[r['unread_interval'] for r in rows],
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),source_consumers=[dict(pc=pc,bytes=raw) for pc,raw in ANCHORS.items()],
        source_record_grammar_reused='compact_sprite_records via battle_scene_sprites',
        original_index_expression='zeroextended BYTE base + conditional96 + lowWORD(state<<2) + ((tick>>3)&3), wrapsWORD; pointer/attribute shifts wrap separately then signextend',
        physical_catalog_is_not_CPU_clamp=True,independent_CPU_comparison=False,
        complete_SAT_writer_reimplemented=False,natural_selector_domain_complete=False,edited_gameplay_safety='unknown')
    members={'fields.json':dump(fields),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members
def fresh_output(value):
    path=f.safe_path(value)
    if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh output outside effect build/formal scope')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output')
    args=p.parse_args(argv);target=None
    if args.command!='verify':
        if not args.output:raise ValueError('fresh output required')
        target=fresh_output(args.output)
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
    elif args.output is not None:raise ValueError('verify must not write')
    rom=f.read_bounded(args.rom,f.ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():f.put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={name:sha(data) for name,data in members.items()})
    else:
        image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),sha256=sha(image),exact_canonical=image==rom,editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
