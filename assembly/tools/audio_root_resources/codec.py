"""77 original audio table bytes, without duplicating old audio authorities."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from tools.audio_formats import audio_formats as af
from tools.vdp_word_streams import format as f
ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=af.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/audio_root_resources/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/audio_root_resources'
FORMAT='candidate-z80-root-and-command-priority-fields-v1'
EDITABLE_BYTES=77
ROOT_START=0xF8000;ROOT_END=0xF800C
PRIORITY_START=0xF8200;PRIORITY_END=0xF823F
SECONDARY_START=0x79BC;SECONDARY_END=0x79BE
ROLES=('command_priority','secondary_sfx_directory','music_directory','local_sfx_directory',
       'pitch_envelope_directory','attenuation_envelope_directory')
TARGETS=(0x8200,0x1020,0x823F,0x1000,0x800E,0x815D)
ROOT_SITES=((0x089E,0),(0x060A,2),(0x0560,4),(0x060A,6),(0x03BB,8),(0x0315,10),(0x0F4E,10))
keys=f.keys;uint=f.uint;sha=f.sha;dump=f.dump;load_fields=f.load_json
def ident(start):return f'rom_{start:06X}_audio'
def metadata():return dict(format=FORMAT,source=dict(size=af.ROM_SIZE,sha256=af.ROM_SHA256),
    confidence='candidate',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def exact_list(value,count,label):
    if type(value)is not list or len(value)!=count:raise ValueError(label+': fixed list allocation differs')
    return value
def sfx_catalog(rom):
    assets=af.extract(rom)
    return {row['id']:row['z80_address'] for row in assets['sfx']}
def evidence(rom):
    if rom[0x69D2+0x0020:0x69D2+0x0023]!=bytes.fromhex('2a021c'):raise ValueError('original RAM root lookup changed')
    if rom[0x69D2+0x0030:0x69D2+0x0035]!=bytes.fromhex('7e23666fc9'):raise ValueError('original LE16 pointer reader changed')
    for z80,slot in ROOT_SITES:
        if rom[0x69D2+z80]!=0xE7:raise ValueError('original RST20 consumer changed')
    if rom[0x69D2+0x0897:0x69D2+0x08A5]!=bytes.fromhex('d6812a021c0e00e74f060009cb7e'):raise ValueError('original command-priority index changed')
    return [dict(z80_pc=pc,rom_pc=0x69D2+pc,slot=slot,confidence='confirmed') for pc,slot in ROOT_SITES]
def extract(rom):
    af.verify_rom(rom);evidence(rom);result=metadata()
    result['roots']=[dict(id=ident(ROOT_START+2*i),slot=2*i,role=role,z80_target=target)
                     for i,(role,target) in enumerate(zip(ROLES,TARGETS))]
    if rom[ROOT_START:ROOT_END]!=b''.join(v.to_bytes(2,'little') for v in TARGETS):raise ValueError('original root pointers differ')
    catalog=sfx_catalog(rom);pointer=int.from_bytes(rom[SECONDARY_START:SECONDARY_END],'little')
    target=next((name for name,value in catalog.items() if value==pointer),None)
    if target is None:raise ValueError('secondary pointer leaves proven SFX headers')
    result['secondary_sfx_pointer']=dict(id=ident(SECONDARY_START),z80_address=0x1020,target=target)
    result['priorities']=[dict(id=ident(PRIORITY_START+i),command=0x81+i,
        unconditional_selection=bool(value&0x80),priority=value&0x7F) for i,value in enumerate(rom[PRIORITY_START:PRIORITY_END])]
    blocks(rom,result);return result
def blocks(rom,fields):
    af.verify_rom(rom);keys(fields,set(metadata())|{'roots','secondary_sfx_pointer','priorities'},'package')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    roots=exact_list(fields['roots'],6,'six consumed roots');raw=bytearray()
    for i,(row,role,target) in enumerate(zip(roots,ROLES,TARGETS)):
        keys(row,{'id','slot','role','z80_target'},'root')
        for key,value in dict(id=ident(ROOT_START+2*i),slot=2*i,role=role).items():f.same(row[key],value,'root.'+key)
        value=uint(row['z80_target'],65535,'LE16 root target')
        allowed=(0x1000,0x1020) if i in (1,3) else (target,)
        if value not in allowed:raise ValueError('root target leaves its proven same-reader catalog')
        raw.extend(value.to_bytes(2,'little'))
    roots_raw=bytes(raw);row=fields['secondary_sfx_pointer']
    keys(row,{'id','z80_address','target'},'secondary SFX pointer')
    f.same(row['id'],ident(SECONDARY_START),'secondary id');f.same(row['z80_address'],0x1020,'secondary Z80 address')
    catalog=sfx_catalog(rom)
    if type(row['target'])is not str or row['target'] not in catalog:raise ValueError('secondary pointer leaves existing SFX header catalog')
    pointer_raw=catalog[row['target']].to_bytes(2,'little');raw=bytearray()
    for i,row in enumerate(exact_list(fields['priorities'],63,'priority allocation')):
        keys(row,{'id','command','unconditional_selection','priority'},'priority')
        f.same(row['id'],ident(PRIORITY_START+i),'priority id');f.same(row['command'],0x81+i,'command allocation')
        if type(row['unconditional_selection'])is not bool:raise ValueError('selection flag must be Boolean')
        raw.append(uint(row['priority'],127,'7-bit priority')|int(row['unconditional_selection'])<<7)
    return [dict(id=ident(SECONDARY_START),start=SECONDARY_START,end=SECONDARY_END,data=pointer_raw,role='candidate_local_z80_secondary_sfx_LE16'),
        dict(id=ident(ROOT_START),start=ROOT_START,end=ROOT_END,data=roots_raw,role='candidate_banked_z80_root_LE16'),
        dict(id=ident(PRIORITY_START),start=PRIORITY_START,end=PRIORITY_END,data=bytes(raw),role='candidate_command_arbitration_priority')]
def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)
def priority_projection(rom,fields,command,current_priority):
    """Bounded 0893..08C7 table branch projection; not a whole Z80 tick.

    Out-of-allocation index reports a model boundary, not a hardware clamp.
    The original driver does not clamp its modulo256 subtraction to63 entries.
    """
    uint(command,255,'command BYTE');uint(current_priority,255,'current priority BYTE')
    rows=blocks(rom,fields);table=rows[-1]['data'];index=(command-0x81)&255
    if command<128:return dict(outcome='ignored_nonnegative_command',accepted=False,read_rom=None,current_priority=current_priority)
    address=PRIORITY_START+index
    if index>=len(table):return dict(outcome='outside_fixed_priority_allocation',accepted=None,read_rom=address,index=index,current_priority=current_priority)
    value=table[index]
    if value&128:return dict(outcome='unconditional_selection',accepted=True,read_rom=address,index=index,
        current_priority=current_priority,clear_all_three_mailboxes=True)
    accepted=current_priority<=value
    return dict(outcome='selected' if accepted else 'rejected',accepted=accepted,read_rom=address,index=index,
        current_priority=value if accepted else current_priority,clear_all_three_mailboxes=False)
def render_bundle(rom):
    fields=extract(rom);data=dump(fields);image=rebuild(rom,load_fields(data));rows=blocks(rom,fields)
    if image!=rom:raise ValueError('entire-ROM roundtrip differs')
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        blocks=[{k:v for k,v in row.items() if k!='data'}|{'sha256':sha(row['data'])} for row in rows],
        mappings=dict(local_secondary='Z80 1020 -> ROM699C+1020 =0079BC',banked_root='Z808000 -> ROMF8000'),
        root_consumers=evidence(rom),priority_consumer=dict(z80_start=0x0893,z80_end=0x08C8,arithmetic='SUB81 BYTE modulo256'),
        unknown_retained=[[0xF800C,0xF800E]],old_authorities_reused=['audio_formats SFX headers/music directory','audio_envelopes pointer tables'],
        independent_CPU_comparison=False,promotion=True)
    members={'fields.json':data,'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},independent_CPU_comparison=False,promotion=True))
    return members
def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/audio_root_resources')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--fields',default=str(DEFAULT_FIELDS));parser.add_argument('--output');args=parser.parse_args(argv)
    target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output)
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
    elif args.output is not None:raise ValueError('verify does not write')
    rom=f.read_bounded(args.rom,af.ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():f.put(target/name,data)
        result=dict(path=str(target),members={name:sha(data) for name,data in members.items()},editable_bytes=EDITABLE_BYTES)
    else:
        fields=load_fields(f.read_bounded(args.fields,f.MAX_JSON));image=rebuild(rom,fields)
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),bytes=len(image),sha256=sha(image),exact_canonical=image==rom,editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
