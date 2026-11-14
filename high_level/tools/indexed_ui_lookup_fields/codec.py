"""Lossless command/state WORDs and digit BYTEs omitted by earlier builders."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from tools.direct_code import direct_code as d
from tools.candidate_selector import anchors
from tools.dialogue_numeric import numeric
f=d.f
ROOT=d.ROOT
FORMAL_ROOT=ROOT/'analysis/indexed_ui_lookup_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
OUTPUT_ROOT=ROOT/'build/indexed_ui_lookup_fields'
FORMAT='g5510-indexed-UI-lookup-source-fields-v1'
EDITABLE_BYTES=36
TABLES=(('digit_glyph_BYTES',0x12782,10,1),('flagged_state_offset_WORDs',0x19698,7,2),('commit_command_WORDs',0x19944,6,2))
sha,dump,load_fields=f.sha,f.dump,f.load_json

def metadata():
 return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),confidence='confirmed_encoding_conditional_original_consumers',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def topology(spec):
 name,start,count,width=spec
 return dict(id=name,start=start,end=start+count*width,entries=count,entry_bytes=width,endianness='big',editor_count_is_CPU_clamp=False)
def verify_rom(rom):
 if type(rom)is not bytes:raise ValueError('immutable canonical ROM bytes required')
 f.verify_rom(rom);numeric.check_code(rom)
 for name,start,end,raw,kind in anchors.ANCHORS:
  if name in ('commit','menu_state_flagged','command_codes','flagged_states') and rom[start:end]!=bytes.fromhex(raw):raise ValueError('original UI lookup consumer differs')
 # PC base is the extension-word address, not the following instruction.
 if 0x1968A+int.from_bytes(rom[0x1968B:0x1968C],'big',signed=True)!=0x19698:raise ValueError('flagged source displacement differs')
 if 0x1968E+int.from_bytes(rom[0x1968F:0x19690],'big',signed=True)!=0x196A6:raise ValueError('flagged target displacement differs')
 if 0x1993A+int.from_bytes(rom[0x1993B:0x1993C],'big',signed=True)!=0x19944:raise ValueError('commit source displacement differs')
def extract(rom):
 verify_rom(rom);out=metadata();out['tables']=[dict(**topology(spec),values=[int.from_bytes(rom[spec[1]+spec[3]*i:spec[1]+spec[3]*(i+1)],'big') for i in range(spec[2])]) for spec in TABLES];blocks(rom,out);return out
def blocks(rom,fields):
 verify_rom(rom);f.keys(fields,set(metadata())|{'tables'},'UI lookup package')
 for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
 tables=fields['tables']
 if type(tables)is not list or len(tables)!=3:raise ValueError('three physical source tables required')
 out=[]
 for table,spec in zip(tables,TABLES):
  fixed=topology(spec);f.keys(table,set(fixed)|{'values'},'lookup table')
  for key,value in fixed.items():f.same(table[key],value,'table.'+key)
  values=table['values'];width=spec[3]
  if type(values)is not list or len(values)!=spec[2]:raise ValueError('fixed physical table count differs')
  data=b''.join(f.uint(value,(1<<(width*8))-1,'full original source field').to_bytes(width,'big') for value in values)
  out.append(dict(id=fixed['id'],start=fixed['start'],end=fixed['end'],data=data,role='conditional_UI_full_'+('BYTE' if width==1 else 'BE16_WORD')+'_lookup_fields'))
 if sum(len(row['data']) for row in out)!=36:raise ValueError('36-byte physical allocation differs')
 return out
def rebuild(rom,fields):
 image=bytearray(rom)
 for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
 return bytes(image)
def signed_WORD(value):return value-65536 if value&32768 else value
def _read(image,spec,index_WORD):
 start=spec[1];address=start+signed_WORD(index_WORD);width=spec[3]
 return dict(address=address,size=width,value=int.from_bytes(image[address:address+width],'big'),index_WORD=index_WORD,signed_index=signed_WORD(index_WORD),inside_editor_catalog=start<=address and address+width<=start+spec[2]*width)
def glyph_lookup(rom,fields,index_WORD):
 """Original1272A/12756/1276C BYTE lookup; no decimal/glyph-domain clamp."""
 f.uint(index_WORD,65535,'original low WORD index');return _read(rebuild(rom,fields),TABLES[0],index_WORD)
def state_dispatch(rom,fields,state_WORD):
 """Original19686 WORD shift/read and1968C signed-WORD target arithmetic only."""
 f.uint(state_WORD,65535,'original F362 WORD');row=_read(rebuild(rom,fields),TABLES[1],(state_WORD<<1)&65535)
 target=(0x196A6+signed_WORD(row['value']))&0xFFFFFFFF
 return dict(**row,relative_target_base=0x196A6,logical_target=target,bus_target=target&0xFFFFFF,odd_target=bool(target&1),JSR_executed=False)
def commit_lookup(rom,fields,selector_WORD,flag_bit1):
 """19922..1993D data projection, not a snapshot of a live-RAM CPU entry.

 Explicit parameters are values at the original reads. With bit1 set, original
 unsigned CMP2 skips slot2 by ADDQ.W1 before the WORD left shift. No6-entry clamp.
 """
 f.uint(selector_WORD,65535,'original F6D4 WORD')
 if type(flag_bit1)is not bool:raise ValueError('explicit original flag-bit1 boolean required')
 adjusted=(selector_WORD+1)&65535 if flag_bit1 and selector_WORD>=2 else selector_WORD
 return dict(**_read(rebuild(rom,fields),TABLES[2],(adjusted<<1)&65535),adjusted_selector_WORD=adjusted,destination_logical_RAM=0xFFFFF612,destination_bus_RAM=0xFFF612,complete_CPU_entry=False)
def render_bundle(rom):
 fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
 if image!=rom:raise ValueError('whole-ROM source roundtrip differs')
 report=dict(**metadata(),editable_bytes=36,full_BYTE_fields=10,full_BE16_fields=13,whole_ROM_exact=True,whole_ROM_sha256=sha(image),consumer_PCs=[0x1272A,0x12756,0x1276C,0x19688,0x1968C,0x19938],prior_read_only_evidence=['tools/candidate_selector/anchors.py:command_codes/flagged_states','tools/dialogue_numeric/numeric.py:TABLE/INSTRUCTIONS'],natural_input_domains='unknown',independent_CPU_comparison=False,complete_CPU_entry=False,limitations=['Physical allocations are not original CPU selector/glyph bounds.','The14-entry six_states table19B42..19B5E is already emitted and excluded here.','The numeric formatter may index original neighboring code for large values; no extra overread bytes are admitted.','State WORD edits can yield odd or unsupported targets; projection never executes them.','Prior read-only guards are evidence, not a second editable table authority.'])
 members={'fields.json':dump(fields),'validation.json':dump(report)};members['manifest.json']=dump(dict(**metadata(),editable_bytes=36,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}));return members
def fresh_output(value):
 path=f.safe_path(value)
 if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh formal directory or beneath dedicated build/indexed_ui_lookup_fields required')
 if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
 return path
def main(argv=None):
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'));p.add_argument('--rom',default=str(f.DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output');args=p.parse_args(argv);target=None
 if args.command!='verify':
  if args.output is None:raise ValueError('fresh output required')
  target=fresh_output(args.output)
  if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
 elif args.output is not None:raise ValueError('verify does not write')
 rom=f.read_bounded(args.rom,f.ROM_SIZE)
 if args.command=='export':
  members=render_bundle(rom);target.mkdir()
  for name,data in members.items():f.put(target/name,data)
  result=dict(path=str(target),editable_bytes=36,members={name:sha(data) for name,data in members.items()})
 else:
  image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
  if target is not None:f.put(target,image)
  result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
 print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
