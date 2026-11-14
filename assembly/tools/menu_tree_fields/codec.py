"""187 original prompt slots and179 physical two-header menu records.

The physical allocation ends at the next explicitly referenced glyph source.
Choice lengths are an editor allocation, never a newly invented CPU bound.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from tools.vdp_word_streams import format as f

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = f.DEFAULT_ROM
FORMAL_ROOT = ROOT/'analysis/menu_tree_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT/'fields.json'
OUTPUT_ROOT = ROOT/'build/menu_tree_fields'
FORMAT = 'g5510-physical-prompt-menu-tree-fields-v1'
DIRECTORY, RECORD_BASE, END = 0x92878, 0x929F2, 0x92C0A
EDITABLE_BYTES = END-DIRECTORY
sha, dump, keys, uint, load_fields = f.sha, f.dump, f.keys, f.uint, f.load_json
ANCHORS = {
    0xBB3C:'43f9000928782451e34f3e317004d4c7',
    0xBB4C:'42471e2a000131c7f3800c47006064000042',
    0xBE66:'43f9000928782051e34830310004d0c04240101031c0f38c',
    0xBF6A:'43f9000928782051e34830310004d0c011e80001f381',
    0xC0D4:'43f9000928783238f38ce349245132311004d4c1103200020c0000ff6726',
    0x4A66:'41f900092c0a43f8' 'd300363c000f4eb90000ae8a',
}

def ident(start): return f'rom_{start:06X}_menu'

def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
                confidence='confirmed_encoding_candidate_physical_catalog',
                owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)

def verify_rom(rom):
    if type(rom)is not bytes or len(rom)!=f.ROM_SIZE or sha(rom)!=f.ROM_SHA:
        raise ValueError('canonical immutable ROM identity required')
    for pc, encoded in ANCHORS.items():
        data=bytes.fromhex(encoded)
        if rom[pc:pc+len(data)]!=data: raise ValueError('original menu reader differs')

def signed_word(word): return word-65536 if word&32768 else word

def topology(rom):
    verify_rom(rom)
    base=int.from_bytes(rom[DIRECTORY:DIRECTORY+4],'big')
    if base!=RECORD_BASE: raise ValueError('original prompt root differs')
    targets=[base+int.from_bytes(rom[p:p+2],'big',signed=True)
             for p in range(DIRECTORY+4,RECORD_BASE,2)]
    starts=sorted(set(targets))
    if len(targets)!=187 or len(starts)!=179 or starts[0]!=RECORD_BASE or starts[-1]!=0x92C06:
        raise ValueError('fixed physical prompt catalog differs')
    rows=[dict(id=ident(a),start=a,end=z,prompt_aliases=[i for i,t in enumerate(targets) if t==a])
          for a,z in zip(starts,starts[1:]+[END])]
    if any(row['end']-row['start']<2 for row in rows): raise ValueError('incomplete menu headers')
    return targets,rows

def exact_list(value,count,label):
    if type(value)is not list or len(value)!=count: raise ValueError(label+': fixed allocation differs')
    return value

def extract(rom):
    targets,rows=topology(rom)
    fields=metadata()
    fields['directory']=dict(start=DIRECTORY,end=RECORD_BASE,record_base=RECORD_BASE,
                              targets=[ident(t) for t in targets])
    fields['records']=[dict(**row,parent_prompt_byte=rom[row['start']],
        title_selector_byte=rom[row['start']+1],
        choice_prompt_bytes=list(rom[row['start']+2:row['end']])) for row in rows]
    blocks(rom,fields)
    return fields

def blocks(rom,fields):
    _,rows=topology(rom)
    fixed=metadata();keys(fields,set(fixed)|{'directory','records'},'package')
    for key,value in fixed.items():f.same(fields[key],value,'package.'+key)
    directory=fields['directory'];keys(directory,{'start','end','record_base','targets'},'directory')
    for key,value in dict(start=DIRECTORY,end=RECORD_BASE,record_base=RECORD_BASE).items():
        f.same(directory[key],value,'directory.'+key)
    catalog={row['id']:row['start'] for row in rows}
    refs=exact_list(directory['targets'],187,'directory slots')
    if any(type(ref)is not str or ref not in catalog for ref in refs):
        raise ValueError('directory must reference an existing complete physical record')
    raw=RECORD_BASE.to_bytes(4,'big')+b''.join((catalog[ref]-RECORD_BASE).to_bytes(2,'big',signed=True) for ref in refs)
    result=[dict(id='prompt_directory',start=DIRECTORY,end=RECORD_BASE,data=raw,
                 role='BE32_root_and_signed_WORD_menu_offsets')]
    for record,row in zip(exact_list(fields['records'],179,'records'),rows):
        keys(record,set(row)|{'parent_prompt_byte','title_selector_byte','choice_prompt_bytes'},'record')
        for key,value in row.items(): f.same(record[key],value,'record.'+key)
        data=bytes([uint(record['parent_prompt_byte'],255,'parent prompt BYTE'),
                    uint(record['title_selector_byte'],255,'title selector BYTE')]+[
            uint(v,255,'choice prompt BYTE') for v in exact_list(record['choice_prompt_bytes'],row['end']-row['start']-2,'choice allocation')])
        result.append(dict(id=row['id'],start=row['start'],end=row['end'],data=data,
                           role='menu_parent_title_and_choice_BYTE_fields'))
    if sum(len(row['data']) for row in result)!=EDITABLE_BYTES: raise ValueError('physical scope differs')
    return result

def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)

def resolve_original(rom,prompt_word):
    """Original lowWORD shift then signed WORD offset; no187-slot CPU clamp."""
    verify_rom(rom);uint(prompt_word,65535,'prompt WORD')
    offset=signed_word((prompt_word*2)&65535)
    address=DIRECTORY+4+offset
    if address<0 or address+2>len(rom):raise ValueError('directory read outside supplied ROM')
    displacement=int.from_bytes(rom[address:address+2],'big',signed=True)
    pointer=(RECORD_BASE+displacement)&0xFFFFFFFF
    bus=pointer&0xFFFFFF
    if bus+2>len(rom):raise ValueError('record header outside supplied ROM')
    return dict(offset_address=address,record_address=pointer,parent_prompt_byte=rom[bus],
                title_selector_byte=rom[bus+1],in_physical_editor_catalog=0<=prompt_word<187)

def original_choice(rom,prompt_word,cell_offset_word):
    """C0E8 BYTE read at record+2+signed D0.W, including allocation-external reads."""
    row=resolve_original(rom,prompt_word);uint(cell_offset_word,65535,'cell offset WORD')
    address=(row['record_address']+2+signed_word(cell_offset_word))&0xFFFFFFFF
    bus=address&0xFFFFFF
    if bus>=len(rom):raise ValueError('choice read outside supplied ROM')
    value=rom[bus]
    return dict(address=address,prompt_byte=value,disabled_by_original_FF_check=value==255)

def render_bundle(rom):
    fields=extract(rom);data=dump(fields);image=rebuild(rom,load_fields(data))
    if image!=rom:raise ValueError('whole ROM serialized roundtrip differs')
    targets,rows=topology(rom)
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,directory_bytes=378,record_bytes=536,
        pointer_slots=187,physical_records=179,header_BYTEs=358,choice_BYTEs=178,
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),independent_CPU_comparison=False,
        source_consumers=[dict(pc=pc,bytes=raw) for pc,raw in ANCHORS.items()],
        physical_end_evidence='004A66 points to next glyph source092C0A; last record has two choice BYTEs',
        original_parent_read=0xBE78,original_title_read=0xBB4E,original_choice_read=0xC0E8,
        original_disabled_choice_value=255,original_title_no_upload_threshold=96,
        choice_lengths_are_physical_editor_allocations_not_CPU_bounds=True,
        natural_prompt_domain_complete=False,edited_gameplay_safety='unknown',
        shared_aliases=[dict(id=row['id'],prompt_ids=row['prompt_aliases']) for row in rows if len(row['prompt_aliases'])>1],
        unknowns=['Original CPU does not clamp prompt indices to187 physical slots.',
                  'Record lengths are not a FF terminator grammar: FF title and empty choices are meaningful.',
                  'Menu geometry and state can cause choice reads outside one physical allocation.',
                  'Changing command bytes does not update glyph labels or establish a safe natural UI route.'])
    graph=dict(physical_records=[dict(id=row['id'],prompt_aliases=row['prompt_aliases'],
        parent_prompt_byte=record['parent_prompt_byte'],title_selector_byte=record['title_selector_byte'],
        choices=[dict(cell=i,prompt_byte=v,disabled=v==255) for i,v in enumerate(record['choice_prompt_bytes'])])
        for row,record in zip(rows,fields['records'])],derived_only=True)
    members={'fields.json':data,'validation.json':dump(report),'menu_graph.json':dump(graph)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(value),sha256=sha(value)) for name,value in members.items()}))
    return members

def fresh_output(value):
    path=f.safe_path(value)
    if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('fresh output must stay in build/menu_tree_fields or formal generated')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--fields',default=str(DEFAULT_FIELDS))
    parser.add_argument('--output');args=parser.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
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
