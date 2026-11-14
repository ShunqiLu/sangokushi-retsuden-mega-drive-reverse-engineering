"""Editable LE16 PSG/FM frequency tables; this is not a Z80 CPU or player."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from tools.direct_code import direct_code as d
from tools.audio_analysis import z80_payload as payload
f=d.f
ROOT=d.ROOT
FORMAL_ROOT=ROOT/'analysis/audio_frequency_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
OUTPUT_ROOT=ROOT/'build/audio_frequency_fields'
FORMAT='g5510-Z80-frequency-LE16-fields-v1'
ROM_BASE=0x69D2
EDITABLE_BYTES=162
TABLES=(('PSG_period_WORDs',0x8E6,69),('FM_semitone_WORDs',0x970,12))
CONSUMERS=((0x28,'4f060009090000007e23666fc9'),
 (0x208,'dd860521e608f5eff1ddcb017e2019d516081e0c08af08933805088218f80883217009ef08b467d1dd750ddd740e'))
sha,dump,load_fields=f.sha,f.dump,f.load_json

def metadata():
 return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),confidence='confirmed_encoding_probable_frequency_role',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def topology(spec):
 name,logical,count=spec
 return dict(id=name,logical_Z80_RAM_start=logical,physical_ROM_start=ROM_BASE+logical,entries=count,entry_bytes=2,endianness='little',editor_count_is_CPU_clamp=False)
def verify_rom(rom):
 if type(rom)is not bytes:raise ValueError('immutable canonical ROM bytes required')
 f.verify_rom(rom);payload.validate_rom(rom)
 for logical,raw in CONSUMERS:
  if rom[ROM_BASE+logical:ROM_BASE+logical+len(raw)//2]!=bytes.fromhex(raw):raise ValueError('original Z80 frequency reader differs')
 if ROM_BASE+0x8E6!=0x72B8 or ROM_BASE+0x970!=0x7342:raise ValueError('primary ROM/RAM mapping differs')
def extract(rom):
 verify_rom(rom);out=metadata();out['tables']=[dict(**topology(spec),WORDs=[int.from_bytes(rom[ROM_BASE+spec[1]+2*i:ROM_BASE+spec[1]+2*i+2],'little') for i in range(spec[2])]) for spec in TABLES];blocks(rom,out);return out
def blocks(rom,fields):
 verify_rom(rom);f.keys(fields,set(metadata())|{'tables'},'frequency package')
 for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
 tables=fields['tables']
 if type(tables)is not list or len(tables)!=2:raise ValueError('two physical frequency tables required')
 out=[]
 for table,spec in zip(tables,TABLES):
  fixed=topology(spec);f.keys(table,set(fixed)|{'WORDs'},'frequency table')
  for key,value in fixed.items():f.same(table[key],value,'table.'+key)
  words=table['WORDs']
  if type(words)is not list or len(words)!=spec[2]:raise ValueError('fixed physical frequency count differs')
  data=b''.join(f.uint(value,65535,'full source WORD').to_bytes(2,'little') for value in words);start=fixed['physical_ROM_start']
  out.append(dict(id=fixed['id'],start=start,end=start+len(data),data=data,role='conditional_Z80_frequency_full_LE16_WORDs'))
 if sum(len(row['data']) for row in out)!=EDITABLE_BYTES:raise ValueError('162-byte physical allocation differs')
 return out
def rebuild(rom,fields):
 image=bytearray(rom)
 for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
 return bytes(image)
def _lookup(image,spec,index):
 name,logical,count=spec;at=(logical+index+index)&65535;physical=ROM_BASE+at
 # RST28 reads low at0030 and high at0032; the catalog does not clamp A.
 low,high=image[physical],image[physical+1]
 return dict(table=name,index_BYTE=index,logical_Z80_RAM_address=at,physical_ROM_address=physical,value_WORD=low|(high<<8),inside_editor_catalog=index<count,
  ordered_reads=[dict(logical_PC=0x30,logical_RAM_address=at,physical_ROM_address=physical,size=1,value=low),dict(logical_PC=0x32,logical_RAM_address=(at+1)&65535,physical_ROM_address=physical+1,size=1,value=high)])
def lookup(rom,fields,table_id,index_BYTE):
 f.uint(index_BYTE,255,'full original A BYTE');spec=next((s for s in TABLES if s[0]==table_id),None)
 if spec is None:raise ValueError('unknown frequency table')
 return _lookup(rebuild(rom,fields),spec,index_BYTE)
def note_frequency(rom,fields,transposed_index_BYTE,PSG_channel):
 """020B..0235 frequency/data-read projection, no stack, CCR or device writes.

 The transposed A is the *result* of0208 BYTE addition, not a natural note ID.
 0211 tests channel bit7. FM retains the first PSG lookup, then uses the real
 SUB12 loop/ADD8 octave accumulator and OR H, not a host hardware-range clamp.
 """
 f.uint(transposed_index_BYTE,255,'full transposed A BYTE')
 if type(PSG_channel)is not bool:raise ValueError('explicit channel-bit7 boolean required')
 image=rebuild(rom,fields);first=_lookup(image,TABLES[0],transposed_index_BYTE)
 if PSG_channel:return dict(frequency_WORD=first['value_WORD'],lookups=[first],ordered_reads=first['ordered_reads'],complete_CPU_entry=False)
 remainder=transposed_index_BYTE;octave=0
 while remainder>=12:remainder-=12;octave=(octave+8)&255
 second=_lookup(image,TABLES[1],remainder);value=second['value_WORD']|((octave&255)<<8)
 return dict(frequency_WORD=value,semitone_BYTE=remainder,octave_bits_BYTE=octave,lookups=[first,second],ordered_reads=first['ordered_reads']+second['ordered_reads'],complete_CPU_entry=False)
def render_bundle(rom):
 fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
 if image!=rom:raise ValueError('whole-ROM field roundtrip differs')
 report=dict(**metadata(),editable_bytes=162,full_LE16_fields=81,PSG_entries=69,FM_entries=12,whole_ROM_exact=True,whole_ROM_sha256=sha(image),primary_mapping='physical0069D2 + logicalRAM; never bankedF0000 + logicalRAM',consumer_anchors=[dict(logical_RAM_start=a,physical_ROM_start=ROM_BASE+a,bytes=b) for a,b in CONSUMERS],PSG_physical_end='next explicit FM base0970',FM_physical_end='next compiled original function0988',natural_note_domain='unknown',independent_CPU_comparison=False,complete_CPU_entry=False,limitations=['No full Z80 stack/register/interrupt/device model.','69 and12 are physical editor counts only; RST28 has no such clamp.','Full source WORDs retain edits outside usual chip frequency ranges.'])
 members={'fields.json':dump(fields),'validation.json':dump(report)};members['manifest.json']=dump(dict(**metadata(),editable_bytes=162,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}));return members
def fresh_output(value):
 path=f.safe_path(value)
 if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh formal directory or beneath dedicated build/audio_frequency_fields required')
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
  result=dict(path=str(target),editable_bytes=162,members={name:sha(data) for name,data in members.items()})
 else:
  image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
  if target is not None:f.put(target,image)
  result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
 print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
