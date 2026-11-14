"""13 original copied startup-seed bytes at ROM0069AA, with typed scalar edits."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
import json
from tools.direct_code import direct_code as d

f,ROOT=d.f,d.ROOT
START,END=0x69AA,0x69B7
EDITABLE_BYTES=13
FORMAL_ROOT=ROOT/'analysis/z80_startup_seed_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
OUTPUT_ROOT=ROOT/'build/z80_startup_seed_fields'
FORMAT='g5510-z80-startup-RAM-seed-scalars-v1'
# RAM offset, width, stable role, confidence of role (copy itself is confirmed).
FIELDS=(
    (0,1,'bank_serial_low_BYTE','confirmed'),
    (1,1,'bank_serial_ninth_source_BYTE','confirmed'),
    (2,2,'banked_root_address_LE16','confirmed'),
    (4,2,'YM_timer_A_reload_LE16','probable'),
    (6,1,'YM_timer_B_reload_BYTE','probable'),
    (7,1,'driver_active_or_mode_BYTE','probable'),
    (8,1,'copied_seed_1C08_BYTE','unknown'),
    (9,1,'selected_command_seed_BYTE','probable'),
    (10,1,'primary_mailbox_seed_BYTE','confirmed'),
    (11,1,'secondary_mailbox_seed_BYTE','confirmed'),
    (12,1,'internal_command_seed_BYTE','probable'),
)
GUARDS=(
    (0x6950,0x69AA,reference_value(__name__, 'GUARDS')),
    (0x69B8,0x69D2,reference_value(__name__, 'GUARDS_2')),
    (0x69D2,0x69D8,reference_value(__name__, 'GUARDS_3')),
)
Z80_INSTRUCTION_PINS=((0x20,'2a021c'),(0x46,'3a071c'),(0xB9,'2a041c'),
    (0xD3,'3a061c'),(0x70C,'3a011c'),(0x70F,'07'),(0x710,'320060'),
    (0x715,'3a001c'),(0x718,'320060'),(0x71B,'0f'),(0x71C,'10fa'),
    (0x7E7,'21091c'),(0x7EA,'110a1c'),(0x7ED,'019603'),(0x7F0,'3600'),(0x7F2,'edb0'))
sha,dump,load_fields=f.sha,f.dump,f.load_json


def metadata():
    return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
                source_format_confidence='confirmed_original_copy_and_scalar_reads',
                executable_code_added=0,recovered_functions_added=0,owner_bytes_added=0,
                natural_domains_added=0,complete_domains_added=0)


def topology(spec):
    offset,width,role,confidence=spec
    return dict(id=f'rom_{START+offset:06X}_{role}',start=START+offset,end=START+offset+width,
                Z80_RAM_start=0x1C00+offset,element_BYTES=width,encoding='LE16' if width==2 else 'BYTE',
                role=role,role_confidence=confidence,source_copy_confirmed=True)


def verify_rom(rom):
    if type(rom)is not bytes:raise ValueError('immutable canonical ROM bytes required')
    f.verify_rom(rom)
    for a,z,h in GUARDS:
        if sha(rom[a:z])!=h:raise ValueError('original startup/reset/driver entry differs')
    if rom[0x38C:0x392]!=bytes.fromhex('4eb900006950'):raise ValueError('original boot caller differs')
    if rom[0x698C:0x699E]!=bytes.fromhex('41fa001c43f900a01c00700c12d851c8fffc'):
        raise ValueError('original13 BYTE copy source/destination/DBRA differs')
    for pc,raw in Z80_INSTRUCTION_PINS:
        a=0x69D2+pc
        if rom[a:a+len(raw)//2]!=bytes.fromhex(raw):raise ValueError('original existing Z80 data consumer differs')


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),seeds=[dict(**topology(spec),value=int.from_bytes(rom[START+spec[0]:START+spec[0]+spec[1]],'little')) for spec in FIELDS])


def fixed(value,expected,mutable,label):
    f.keys(value,set(expected)|set(mutable),label)
    for key,item in expected.items():f.same(value[key],item,label+'.'+key)


def blocks(rom,fields):
    verify_rom(rom);fixed(fields,metadata(),{'seeds'},'startup seed package')
    seeds=fields['seeds']
    if type(seeds)is not list or len(seeds)!=len(FIELDS):raise ValueError('fixed physical seed fields required')
    data=bytearray()
    for row,spec in zip(seeds,FIELDS):
        fixed(row,topology(spec),{'value'},'seed');width=spec[1]
        data.extend(f.uint(row['value'],(1<<(8*width))-1,'full original seed scalar').to_bytes(width,'little'))
    if len(data)!=13:raise ValueError('fixed13-byte copy allocation differs')
    return [dict(id='rom_0069AA_Z80_startup_RAM_seeds',start=START,end=END,data=bytes(data),role='original_copied_Z80_RAM_startup_seed_scalars')]


def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def flags():
    return dict(CPU_executed=False,Z80_executed=False,hardware_executed=False,
                true_call_RTS_executed=False,independent_CPU_comparison=False,
                complete_entry=False,natural_domain_complete=False)


def copy_preview(rom,fields):
    """Each original MOVE.B source read and Z80-RAM destination write, in order."""
    image=rebuild(rom,fields);events=[]
    for index in range(13):
        value=image[START+index]
        events.append(dict(kind='ROM_BYTE_read_projection',pc=0x6998,logical_address=START+index,address=START+index,size=1,value=value))
        events.append(dict(kind='Z80_RAM_BYTE_write_projection',pc=0x6998,logical_address=0xA01C00+index,address=0xA01C00+index,
                           Z80_RAM_address=0x1C00+index,size=1,value=value))
    return dict(**flags(),events=events,copied_BYTES=13,source_end=END,Z80_RAM_end=0x1C0D,
                final_D0_WORD=65535,final_A0_LONG=END,final_A1_LONG=0xA01C0D)


def seed_views(rom,fields):
    """Existing bank/timer instruction arithmetic only; no chip or Z80 execution."""
    image=rebuild(rom,fields);data=image[START:END]
    first=((data[1]<<1)|(data[1]>>7))&255;writes=[first];value=data[0]
    for _ in range(8):
        writes.append(value);value=((value>>1)|((value&1)<<7))&255
    bits=[value&1 for value in writes];bank=sum(bit<<i for i,bit in enumerate(bits))
    reload=int.from_bytes(data[4:6],'little')
    return dict(**flags(),bank_write_BYTEs=writes,bank_serial_bits=bits,bank_register_9bit=bank,
                M68K_bank_window_base=bank<<15,root_address_LE16=int.from_bytes(data[2:4],'little'),
                timer_A_register25_BYTE=reload&3,timer_A_register24_BYTE=(reload>>2)&255,
                timer_B_register26_BYTE=data[6],driver_mode_seed_BYTE=data[7],unknown_1C08_seed_BYTE=data[8],
                command_seed_BYTEs=list(data[9:13]),pointer_targets_followed=False,edited_audio_safety='unknown')


def raw_guard(base):
    raw=d.raw_positions(base)
    if not set(range(START,END))<=raw:raise ValueError('all13 positions require sole existing raw authority')
    return dict(guarded_raw_bytes=13,layout_remaining_raw=len(raw),excluded_next_BYTE_raw=END in raw)


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('serialized whole-ROM roundtrip differs')
    view=copy_preview(rom,fields)
    union={e['address'] for e in view['events'] if e['kind']=='ROM_BYTE_read_projection'}
    if union!=set(range(START,END)):raise ValueError('original13-BYTE copy read union differs')
    report=dict(**metadata(),editable_bytes=13,physical_blocks=1,scalar_fields=len(FIELDS),
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),constructed_source_read_union_bytes=len(union),
        **flags(),copy=view,seed_arithmetic=seed_views(rom,fields),
        source_guards=[dict(start=a,end=z,sha256=h,physical_emit=False) for a,z,h in GUARDS],
        hardware_order=dict(boot_caller=0x38C,entry=0x6950,bus_request=dict(pc=0x6950,address=0xA11100,WORD=0x100),
            reset_calls=[0x6958,0x699E],reset_helper=0x69B8,
            reset_helper_writes=[dict(pc=0x69B8,address=0xA11200,WORD=0),dict(pc=0x69C8,address=0xA11200,WORD=0x100)],
            bus_release=dict(pc=0x69A0,address=0xA11100,WORD=0),source_entry_RTS=0x69A8,
            actual_execution=False),
        old_Z80_driver_reset_entry=dict(logical_address=0,physical_source=0x69D2,physical_emit=False),
        unknown_business_seed=dict(ROM_address=0x69B2,Z80_RAM_address=0x1C08,copy_confirmed=True,role_confidence='unknown'),
        excluded_unknown_next_BYTE=dict(start=END,end=END+1,bytes=1,physical_emit=False,confidence='unknown'),
        limitations=['These are source data seeds, not newly recovered Z80 instructions or a CPU/function domain.',
            'The actual original13-byte copy overlays secondary Z80 destination1C00..1C0D; original secondary source/shadow bytes are not emitted here.',
            'Old Z80 bank/root/timer/mailbox consumers establish scalar widths; their existing compiled source is guarded and reused.',
            '07E7 zero-fill covers1C09..1F9F later. Copied command seeds may be overwritten; no lifetime or full startup execution claim.',
            '1C08 business meaning remains unknown despite confirmed copy. Next69B7 BYTE is not read and is not padding or a field.',
            'All BYTE/LE16 seed bits remain editable, including unused serial bits and timer high bits; no hardware/game-safety normalization.'])
    members={'fields.json':dump(fields),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=13,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value):
    path=f.safe_path(value)
    if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh formal directory or dedicated startup-seed build output required')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(f.DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output')
    args=p.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output)
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
    elif args.output is not None:raise ValueError('verify does not write')
    rom=f.read_bounded(args.rom,f.ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():f.put(target/name,data)
        result=dict(path=str(target),editable_bytes=13,members={name:sha(data) for name,data in members.items()})
    else:
        image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
