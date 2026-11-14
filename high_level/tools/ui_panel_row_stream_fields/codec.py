"""180 actual source bytes in four width11/rows4 UI command streams."""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse,json
from pathlib import Path
from tools.direct_code import direct_code as d
from tools.ui_layouts import ui_layouts as grammar
f=d.f
ROOT=d.ROOT
FORMAL_ROOT=ROOT/'analysis/ui_panel_row_stream_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
OUTPUT_ROOT=ROOT/'build/ui_panel_row_stream_fields'
FORMAT='g5510-counted-panel-UI-source-WORD-fields-v1'
EDITABLE_BYTES=180
STREAMS=((0x5BE4,0x5C0C,(0x5AEE,),(0x5B18,)),(0x5C0C,0x5C38,(0x5B60,0x5BD2),(0x5B72,0x5BD6)),(0x5C38,0x5C68,(0x5B84,),(0x5BD6,)),(0x5C68,0x5C98,(0x5B6E,0x5BA6),(0x5B72,0x5BD6)))
CALLER_SHA=reference_value(__name__, 'CALLER_SHA')
READER_SHA=reference_value(__name__, 'READER_SHA')
sha,dump,load_fields=f.sha,f.dump,f.load_json
def metadata():
 return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),confidence='confirmed_counted_source_candidate_UI_role',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def topology(spec):
 start,end,leas,calls=spec
 return dict(id=f'rom_{start:06X}_counted_panel_rows',start=start,end=end,source_LEAs=list(leas),source_calls=list(calls),reader=0x26BFA,original_D0_LONG=0xC000000B,columns=11,rows_count=4,original_D1_WORD=4,WORD_order='big')
def verify_rom(rom):
 if type(rom)is not bytes:raise ValueError('immutable canonical ROM bytes required')
 f.verify_rom(rom)
 if sha(rom[0x5AC6:0x5BE4])!=CALLER_SHA or sha(rom[0x26BFA:0x26C8E])!=READER_SHA:raise ValueError('original panel consumer/reader differs')
 if rom[0x5AC6:0x5AD0]!=bytes.fromhex('203cc000000b323c0004'):raise ValueError('original width/rows registers differ')
 if rom[0x5AD6:0x5ADE]!=bytes.fromhex('3e3b700e4ebb7012'):raise ValueError('original directory/JSR indexed words differ')
 offsets=[int.from_bytes(rom[p:p+2],'big',signed=True) for p in range(0x5AE6,0x5AEE,2)]
 if [0x5AEE+value for value in offsets]!=[0x5AEE,0x5B5C,0x5B48,0x5B80]:raise ValueError('original signed WORD directory targets differ')
 for start,end,leas,calls in STREAMS:
  for pc in leas:
   if rom[pc:pc+2]!=bytes.fromhex('41fa') or pc+2+int.from_bytes(rom[pc+2:pc+4],'big',signed=True)!=start:raise ValueError('original PC-relative source LEA differs')
  for pc in calls:
   if rom[pc:pc+6]!=bytes.fromhex('4eb900026bfa'):raise ValueError('original true renderer JSR differs')
def parse_stream(image,spec):
 """Reuse the accepted reader grammar; prove exact count and consumption end."""
 if type(image)is not bytes or len(image)!=f.ROM_SIZE:raise ValueError('complete immutable image required')
 fixed=topology(spec);view=grammar.walk_rows(image,fixed['start'],11,4,command_budget=180)
 if view['status']!='complete' or view['end']!=fixed['end'] or view['output_words']!=44:raise ValueError('four exact11-cell rows do not close at the fixed stream end')
 rows=[]
 for i in range(4):
  commands=[x for x in view['commands'] if x['row']==i];ops=[]
  if not commands:raise ValueError('empty original row')
  for command in commands:
   fixed_op=dict(start=command['start'],end=command['end'],emitted_cells=command['output_words'])
   if command['kind']=='literal':ops.append(dict(**fixed_op,kind='direct_WORD',WORD=command['word']))
   elif command['kind']=='word_command' and command['operation'] in ('repeat','increment_by_two'):
    ops.append(dict(**fixed_op,kind='repeat_WORD' if command['operation']=='repeat' else 'ascending_WORD',control_WORD=command['control_word'],payload_WORD=command['operand_word']))
   else:raise ValueError('unsupported original panel source handler')
  if sum(op['emitted_cells'] for op in ops)!=11:raise ValueError('original row counter closure differs')
  rows.append(dict(row_index=i,start=commands[0]['start'],end=commands[-1]['end'],cell_count=11,operations=ops))
 return dict(**fixed,rows=rows)
def extract(rom):
 verify_rom(rom);out=metadata();out['streams']=[parse_stream(rom,spec) for spec in STREAMS];return out
def exact(value,count,label):
 if type(value)is not list or len(value)!=count:raise ValueError(label+': fixed physical count differs')
 return value
def pinned(value,original,mutable,label):
 f.keys(value,set(original),label)
 for key,x in original.items():
  if key not in mutable:f.same(value[key],x,label+'.'+key)
def blocks(rom,fields):
 verify_rom(rom);f.keys(fields,set(metadata())|{'streams'},'panel package')
 for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
 out=[]
 for stream,spec in zip(exact(fields['streams'],4,'streams'),STREAMS):
  original=parse_stream(rom,spec);pinned(stream,original,{'rows'},'stream');data=bytearray()
  for row,oldrow in zip(exact(stream['rows'],4,'rows'),original['rows']):
   pinned(row,oldrow,{'operations'},'row')
   for op,old in zip(exact(row['operations'],len(oldrow['operations']),'operations'),oldrow['operations']):
    key='WORD' if old['kind']=='direct_WORD' else 'payload_WORD';pinned(op,old,{key},'operation');value=f.uint(op[key],65535,'full source WORD')
    if key=='WORD':
     if value&0x8000:raise ValueError('direct source WORD must retain original positive sign branch')
    else:data.extend(op['control_WORD'].to_bytes(2,'big'))
    data.extend(value.to_bytes(2,'big'))
  if len(data)!=spec[1]-spec[0]:raise ValueError('fixed encoded panel cost differs')
  out.append(dict(id=stream['id'],start=spec[0],end=spec[1],data=bytes(data),role='actual_counted_UI_panel_WORD_stream'))
 if sum(len(r['data']) for r in out)!=180 or any(a['end']!=b['start'] for a,b in zip(out,out[1:])):raise ValueError('180-byte source closure differs')
 return out
def rebuild(rom,fields):
 image=bytearray(rom)
 for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
 return bytes(image)
def source_views(rom,fields):
 image=rebuild(rom,fields);return [parse_stream(image,spec) for spec in STREAMS]
def schema(rom):
 def obj(props):return dict(type='object',required=list(props),properties=props,additionalProperties=False)
 def fixed(value):
  if type(value)is dict:return obj({key:fixed(x) for key,x in value.items()})
  if type(value)is list:return dict(type='array',prefixItems=[fixed(x) for x in value],items=False,minItems=len(value),maxItems=len(value))
  return dict(type={int:'integer',str:'string',bool:'boolean'}[type(value)],const=value)
 result=fixed(extract(rom));result['$schema']='https://json-schema.org/draft/2020-12/schema'
 for stream in result['properties']['streams']['prefixItems']:
  for row in stream['properties']['rows']['prefixItems']:
   for op in row['properties']['operations']['prefixItems']:
    for key,maxval in (('WORD',32767),('payload_WORD',65535)):
     if key in op['properties']:op['properties'][key]=dict(type='integer',minimum=0,maximum=maxval)
 return result
def render_bundle(rom):
 fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
 if image!=rom:raise ValueError('whole-ROM source roundtrip differs')
 view=source_views(rom,fields);ops=[op for s in view for row in s['rows'] for op in row['operations']]
 report=dict(**metadata(),editable_bytes=180,streams=4,rows=16,consumed_cells=176,source_WORDs=90,editable_value_WORDs=len(ops),pinned_control_WORDs=sum('control_WORD'in op for op in ops),whole_ROM_exact=True,whole_ROM_sha256=sha(image),consumer=dict(start=0x5AC6,end=0x5BE4,sha256=CALLER_SHA),reader=dict(start=0x26BFA,end=0x26C8E,sha256=READER_SHA),directory=dict(start=0x5AE6,end=0x5AEE,WORD_offsets=[0,110,90,146],target_base=0x5AEE,targets=[0x5AEE,0x5B5C,0x5B48,0x5B80],physical_emit=False),source_consumption=[dict(start=s['start'],end=s['end'],source_bytes=s['end']-s['start'],rows=4,columns=11) for s in view],natural_input_domains='unknown',independent_CPU_comparison=False,complete_CPU_entry=False,limitations=['Counts and operation topology are original fixed codec constraints, not a complete renderer model.','All repeat/ascending payload bits remain editable; positive direct WORDs retain the original sign branch.','Directory source is guarded/reused, never emitted twice.','Shared RAM queue/CCR/stack/device/UI business behavior is outside this format.'])
 members={'fields.json':dump(fields),'fields.schema.json':dump(schema(rom)),'validation.json':dump(report)};members['manifest.json']=dump(dict(**metadata(),editable_bytes=180,members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}));return members
def fresh_output(value):
 path=f.safe_path(value)
 if path!=FORMAL_ROOT and (path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):raise ValueError('fresh formal directory or beneath dedicated build/ui_panel_row_stream_fields required')
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
  result=dict(path=str(target),editable_bytes=180,members={name:sha(data) for name,data in members.items()})
 else:
  image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
  if target is not None:f.put(target,image)
  result=dict(path=None if target is None else str(target),exact_canonical=image==rom,sha256=sha(image))
 print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
