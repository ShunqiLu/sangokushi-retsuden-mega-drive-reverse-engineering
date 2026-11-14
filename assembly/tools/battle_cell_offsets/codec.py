"""54 original two-WORD cell offsets, physical catalog not CPU-domain clamp."""
import argparse,json
from pathlib import Path
from tools.vdp_word_streams import format as shared

ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=shared.DEFAULT_ROM
FORMAL_ROOT=ROOT/'analysis/battle_cell_offsets/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
OUTPUT_ROOT=ROOT/'build/battle_cell_offsets'
START,END,COUNT=0x21F82,0x2205A,54
EDITABLE_BYTES=END-START
FORMAT='g5510-battle-candidate-cell-signed-WORD-offsets-v1'
CONSUMER=bytes.fromhex('4dfa00824bf90000670a49f9000ee5f03038f68ae54843f9000d4ac63e310002e84f3c310000e84e3007d0560c4000486400004a3206d26e00020c4100486400003c3400e74ad440e74ad4414243163420004a3530006b2443f8900014110242000f6700001eb02900016600000ab22900026700000843f1200d60e0dcfc000460a64e75')
sha,dump,load_fields=shared.sha,shared.dump,shared.load_json

def metadata():
 return dict(format=FORMAT,canonical_source=dict(size=shared.ROM_SIZE,sha256=shared.ROM_SHA),confidence='confirmed_encoding_probable_candidate_cell_order',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def topology():return dict(id='rom_021F82_cell_offsets',start=START,end=END,records=COUNT,record_bytes=4,original_source_LEA=0x21EFE,original_read_PCs=[0x21F28,0x21F34],original_advance_PC=0x21F7A)
def verify_rom(rom):
 if type(rom) is not bytes or len(rom)!=shared.ROM_SIZE or sha(rom)!=shared.ROM_SHA:raise ValueError('canonical ROM identity required')
 if rom[0x21EFE:0x21EFE+len(CONSUMER)]!=CONSUMER:raise ValueError('original candidate-cell consumer differs')
 if 0x21F00+int.from_bytes(CONSUMER[2:4],'big',signed=True)!=START:raise ValueError('original PC-relative table base differs')
def signed(value,label):
 if type(value) is not int or not -32768<=value<=32767:raise ValueError(label+': strict signed WORD integer required')
 return value
def exact(value,count,label):
 if type(value) is not list or len(value)!=count:raise ValueError(label+': fixed physical count differs')
 return value
def extract(rom):
 verify_rom(rom);result=dict(**metadata(),table=dict(**topology(),rows=[dict(row_delta_signed_WORD=int.from_bytes(rom[p:p+2],'big',signed=True),column_delta_signed_WORD=int.from_bytes(rom[p+2:p+4],'big',signed=True)) for p in range(START,END,4)]));blocks(rom,result);return result
def blocks(rom,fields):
 verify_rom(rom);shared.keys(fields,set(metadata())|{'table'},'package')
 for key,value in metadata().items():shared.same(fields[key],value,'package.'+key)
 table=fields['table'];shared.keys(table,set(topology())|{'rows'},'table')
 for key,value in topology().items():shared.same(table[key],value,'table.'+key)
 data=bytearray()
 for row in exact(table['rows'],COUNT,'offset rows'):
  shared.keys(row,{'row_delta_signed_WORD','column_delta_signed_WORD'},'row')
  for key in ('row_delta_signed_WORD','column_delta_signed_WORD'):data.extend(signed(row[key],key).to_bytes(2,'big',signed=True))
 if len(data)!=EDITABLE_BYTES:raise ValueError('216-byte allocation differs')
 return [dict(id=table['id'],start=START,end=END,data=bytes(data),role='candidate_cell_signed_WORD_offsets')]
def rebuild(rom,fields):
 image=bytearray(rom)
 for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
 return bytes(image)
def valid_cell_candidates(rom,fields,d7_row_WORD,d6_column_WORD):
 """Only original ADD.W/CMP.W coordinate projection, no occupancy/UI shortcut.

 Enumerates the fixed editor catalog. Original CPU has no54-entry clamp and
 may advance beyond it if runtime occupancy never selects a usable candidate.
 """
 blocks(rom,fields);y=shared.uint(d7_row_WORD,65535,'D7 row WORD');x=shared.uint(d6_column_WORD,65535,'D6 column WORD');result=[]
 for slot,item in enumerate(fields['table']['rows']):
  row=(y+item['row_delta_signed_WORD'])&65535;column=(x+item['column_delta_signed_WORD'])&65535
  if row<72 and column<72:result.append(dict(editor_slot=slot,source=START+slot*4,row_WORD=row,column_WORD=column,terrain_index_WORD=row*72+column))
 return result
def render_bundle(rom):
 fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
 if image!=rom:raise ValueError('whole-ROM roundtrip differs')
 report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,record_count=COUNT,signed_WORD_fields=108,whole_ROM_exact=True,whole_ROM_sha256=sha(image),consumer=dict(start=0x21EFE,end=0x21F82,bytes=CONSUMER.hex(),source_reads=[0x21F28,0x21F34],advance=4),physical_boundary='next compiled instruction at02205A; editor allocation only',natural_index_domain='unknown',CPU_has_fixed54_limit=False,complete_entry_projection=False,independent_CPU_comparison=False,limitations=['Original runtime may keep walking past the54 physical rows.','Terrain LUT/occupancy and full21EFE entry behavior not replaced by coordinate projection.','No runtime ownership or natural-domain promotion.'])
 members={'fields.json':dump(fields),'validation.json':dump(report)};members['manifest.json']=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}));return members
def fresh_output(value):
 path=shared.safe_path(value)
 if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh formal directory or beneath build/battle_cell_offsets required')
 if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
 return path
def main(argv=None):
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'));p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output');args=p.parse_args(argv);target=None
 if args.command!='verify':
  if args.output is None:raise ValueError('fresh output required')
  target=fresh_output(args.output)
  if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
 elif args.output is not None:raise ValueError('verify does not write')
 rom=shared.read_bounded(args.rom,shared.ROM_SIZE)
 if args.command=='export':
  members=render_bundle(rom);target.mkdir()
  for name,data in members.items():shared.put(target/name,data)
  result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={name:sha(data) for name,data in members.items()})
 else:
  image=rebuild(rom,load_fields(shared.read_bounded(args.fields,shared.MAX_JSON)))
  if target is not None:shared.put(target,image)
  result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
 print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
