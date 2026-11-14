"""Emit the old sealed80-LONG VDP directory without a second fields author."""

from tools.resource_reference import reference_value
import argparse,json,sys
from pathlib import Path
from tools.vdp_word_streams import format as author

ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=author.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/vdp_word_streams/generated/fields.json'
FORMAL_ROOT=ROOT/'analysis/vdp_directory_fields/generated'
OUTPUT_ROOT=ROOT/'build/vdp_directory_fields'
FORMAT='g5510-existing-VDP-directory-physical-emission-adapter-v1'
EDITABLE_BYTES=320
AUTHOR_CANONICAL_SHA=reference_value(__name__, 'AUTHOR_CANONICAL_SHA')
AUTHOR_SOURCE_SHA=reference_value(__name__, 'AUTHOR_SOURCE_SHA')
GUARDS=((0x39764,bytes.fromhex('e54343faf052207130006100fee8')),
        (0x3978E,bytes.fromhex('5243e54343faf026' '20713000303c20006100feb8')))
sha,dump,load_fields=author.sha,author.dump,author.load_json

def blocks(rom,fields):
 """Only old directory fields are read; old schema remains sole authority."""
 author.verify_rom(rom);author.validate_fields(fields,rom[author.REUSE_START:author.REUSE_END])
 for pc,raw in GUARDS:
  if rom[pc:pc+len(raw)]!=raw:raise ValueError('original directory indexed reader differs')
 table=fields['directory'];data=b''.join(row['target'].to_bytes(4,'big') for row in table['entries'])
 if (table['start'],table['end'],len(data))!=(0x387BA,0x388FA,EDITABLE_BYTES):raise ValueError('old directory physical allocation differs')
 return [dict(id='rom_0387BA_vdp_directory',start=table['start'],end=table['end'],data=data,role='old_author_VDP_BE32_directory')]
def rebuild(rom,fields):
 image=bytearray(rom)
 for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
 return bytes(image)
def LONG_lines(rom,fields):
 blocks(rom,fields);targets=[row['target'] for row in fields['directory']['entries']]
 return ['        .long '+','.join(f'0x{target:08X}' for target in targets[p:p+4]) for p in range(0,len(targets),4)]
def directory_source(rom,fields):
 lines=['| Existing vdp_word_streams author; no copied fields authority.',
        '| Original ASL.W2/LEA/MOVEA.L reader; natural D3.W index domain unknown.',
        '.cpu 68000','.section .rodata','vdp_directory_0387ba:']+LONG_lines(rom,fields)
 lines+=['vdp_directory_0387ba_end:',
         '        .if (vdp_directory_0387ba_end-vdp_directory_0387ba) != 320',
         '        .error "VDP directory source length changed"','        .endif']
 return ('\n'.join(lines)+'\n').encode()
def add_to_layout(rom,fields,base):
 """Use normal raw-only accounting, emitting actual LONG directives in bank03."""
 from tools.direct_code import direct_code as d
 row=blocks(rom,fields)[0];result=d.add_resource_fields(rom,fields,base,sys.modules[__name__],'vdp_directory',EDITABLE_BYTES)
 data=row['data'];old='\n'.join('        .byte '+','.join(f'0x{v:02X}' for v in data[p:p+16]) for p in range(0,len(data),16))
 text=result['m68k_bank03.s'].decode()
 if text.count(old)!=1:raise ValueError('directory typed block omitted/duplicated before LONG conversion')
 result['m68k_bank03.s']=text.replace(old,'\n'.join(LONG_lines(rom,fields)),1).encode()
 return result
def render_bundle(rom,fields):
 row=blocks(rom,fields)[0];image=rebuild(rom,fields)
 if image!=rom:raise ValueError('canonical directory rebuild differs')
 report=dict(format=FORMAT,physical_bytes=320,physical_start=row['start'],physical_end=row['end'],LONG_fields=80,sole_author=str(DEFAULT_FIELDS.relative_to(ROOT)),sole_author_schema='tools/vdp_word_streams/format.py',author_fields_sha256=sha(dump(fields)),canonical_author_fields_sha256=AUTHOR_CANONICAL_SHA,canonical_author_source_sha256=AUTHOR_SOURCE_SHA,directory_metadata_pinned_by_old_schema=True,editable_through_old_author=False,physical_directory_aliases_preserved=80,distinct_targets=len(set(x['target'] for x in fields['directory']['entries'])),whole_ROM_exact=True,whole_ROM_sha256=sha(image),original_readers=[dict(pc=pc,bytes=raw.hex()) for pc,raw in GUARDS],leading_unknown_excluded=[0x387B9,0x387BA],old_stream_bytes_reemitted=0,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,confidence='confirmed_encoding_candidate_index_domain',independent_CPU_comparison=False,limitations=['No new fields.json; old directory metadata stays the only author.','The current old schema pins directory targets; adapter cannot unpin them.','Valid edits to old command fields remain allowed but are emitted only by the old stream builder.','Physical80-slot catalog is not a natural D3.W clamp.'])
 members={'directory.s':directory_source(rom,fields),'validation.json':dump(report)}
 members['manifest.json']=dump(dict(format=FORMAT,physical_bytes=320,source_fields_path=str(DEFAULT_FIELDS.relative_to(ROOT)),source_fields_sha256=sha(dump(fields)),new_field_author_count=0,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}));return members
def fresh_output(value):
 path=author.safe_path(value)
 if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh adapter directory or dedicated build output required')
 if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
 return path
def main(argv=None):
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'));p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output');args=p.parse_args(argv);target=None
 if args.command!='verify':
  if args.output is None:raise ValueError('fresh output required')
  target=fresh_output(args.output)
  if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
 elif args.output is not None:raise ValueError('verify does not write')
 rom=author.read_bounded(args.rom,author.ROM_SIZE);fields=load_fields(author.read_bounded(args.fields,author.MAX_JSON))
 if args.command=='export':
  members=render_bundle(rom,fields);target.mkdir()
  for name,data in members.items():author.put(target/name,data)
  result=dict(path=str(target),physical_bytes=320,source_fields_sha256=sha(dump(fields)),members={name:sha(data) for name,data in members.items()})
 else:
  image=rebuild(rom,fields)
  if target is not None:author.put(target,image)
  result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
 print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
