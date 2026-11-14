"""Lossless, fixed-layout main-dialogue resources and the original lookup formula."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from tools.audio_formats import audio_formats as af
from tools.text_font import text_font_assets as font

DEFAULT_ROM = af.DEFAULT_ROM
DEFAULT_ASSETS = ROOT/'analysis/dialogue_text/generated/assets.json'
DIRECTORY = 0x092C4A
PAGE_LAYOUT = ((0x092C56,0x092DF8,0x092E84),(0x092DF8,0x092E84,0x094094))
TEXT_END = 0x094728
NAME_LAYOUT = {'officer_names':(0x08A504,256,3,0), 'city_names':(0x08A216,40,2,1)}
OPERATIONS = ('restore_saved_mode','advance_line','insert_u32_f3c8','insert_u32_f3cc',
              'insert_officer_f3d0','insert_officer_f3d2','restore_text_cursor_f3d4',
              'insert_force_leader_name','insert_city_name','insert_year','insert_month')
ANCHORS = {
    0x0676F2:'4a40', 0x0676F4:'6b30', 0x0676FA:'610002d6', 0x0676FE:'21c8f3be',
    0x0679D2:'227900092c4a', 0x0679D8:'3200', 0x0679DA:'e049', 0x0679DC:'e349',
    0x0679DE:'41f900092c4e', 0x0679E4:'32301000', 0x0679E8:'d2c1',
    0x0679EA:'2051', 0x0679EC:'3200', 0x0679EE:'024100ff', 0x0679F2:'e349',
    0x0679F4:'32311004', 0x0679F8:'d0c1', 0x0679FA:'4e75',
    0x0671CA:'2078f3be', 0x0671CE:'54b8f3be', 0x0671D2:'3010',
    0x0671D8:'6730', 0x0671DA:'6b4e', 0x06722A:'024000ff',
    0x06722E:'303b0008', 0x067232:'4efb001a', 0x067216:'45fa0292',
    0x00543A:'024500ff', 0x00543E:'41f90008a504', 0x005444:'3c05',
    0x005446:'e34d', 0x005448:'da46', 0x00544A:'e34d', 0x00544C:'d0c5',
    0x0672A2:'3038f3d0', 0x0672A6:'3200', 0x0672A8:'e348', 0x0672AA:'d041',
    0x0672AC:'e348', 0x0672AE:'41f90008a504', 0x0672B4:'d0c0',
    0x0672BA:'303c0002', 0x0672BE:'3218', 0x0672C0:'00414000',
    0x0672C4:'32c1', 0x0672C6:'51c8fff6', 0x0672CA:'32bc800c',
    0x0672CE:'0c61403f', 0x0672D2:'67f6', 0x0672D4:'21f8f3bef3d4',
    0x0672DA:'21fcffffd300f3be', 0x0672EC:'21f8f3d4f3be',
    0x067306:'3038f646', 0x06730A:'e548', 0x06730C:'41f90008a212',
    0x067312:'d0c0', 0x067318:'2018', 0x06731A:'008040004000',
    0x067320:'22c0', 0x067322:'32bc800c',
    0x00A8BA:'41f90008a216', 0x00A8CA:'383c0003', 0x00A8CE:'363c0013',
    0x00A8D6:'4eb90000ae8a', 0x00A8EE:'51ccffde',
    0x00AE8E:'3818', 0x00AECE:'51cbffbe',
    0x0187C2:'024200ff', 0x0187C8:'e34a', 0x0187CA:'d443', 0x0187CC:'e34a',
    0x0187CE:'41f90008a504', 0x0187D4:'d0c2', 0x0187DA:'363c0002', 0x0187DE:'4eb90000ae8a',
    0x06738E:'0241ff00', 0x067392:'e749', 0x067394:'024000ff',
    0x067398:'eb48', 0x06739A:'8041', 0x06739C:'45f90008159c', 0x0673A2:'45f20000',
}


def sha(data): return hashlib.sha256(data).hexdigest()
def dump(value): return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def integer(value,maximum,name):
    if type(value) is not int or not 0 <= value <= maximum: raise ValueError(f'{name}: strict integer out of range')
    return value
def word(data,address):
    if type(address) is not int or address < 0 or address&1 or address+2 > len(data): raise ValueError('word outside input or unaligned')
    return int.from_bytes(data[address:address+2],'big')
def longword(data,address):
    if type(address) is not int or address < 0 or address&1 or address+4 > len(data): raise ValueError('long outside input or unaligned')
    return int.from_bytes(data[address:address+4],'big')
def signed(value): return value if value < 0x8000 else value-0x10000
def keys(value,expected):
    if type(value) is not dict or set(value) != set(expected): raise ValueError('object fields changed')
def sequence(value,length):
    if type(value) is not list or len(value) != length: raise ValueError('fixed sequence length changed')


def check_anchors(rom):
    for address,encoded in ANCHORS.items():
        raw = bytes.fromhex(encoded)
        if rom[address:address+len(raw)] != raw: raise ValueError(f'consumer instruction changed at {address:06x}')


def resolve_raw(rom,message_id):
    """Original 0679D2 arithmetic, NOT an original-game validity check.

    Reads require mapped ROM input here; the original CPU can proceed into other
    address spaces. Return the 32-bit pointer and actual 24-bit bus address.
    The separate 0676F2 wrapper rejects signed-negative IDs before calling this.
    """
    integer(message_id,65535,'message id')
    page_word = DIRECTORY+4+2*(message_id>>8)
    page_offset = signed(word(rom,page_word))
    page = (longword(rom,DIRECTORY)+page_offset)&0xffffffff
    offset_address = (page+4+2*(message_id&255))&0xffffffff
    record_offset = signed(word(rom,offset_address&0xffffff))
    pointer = (longword(rom,page&0xffffff)+record_offset)&0xffffffff
    return {'page_offset_address':page_word,'page_offset':page_offset,'page':page,
            'record_offset_address':offset_address,'record_offset':record_offset,
            'pointer':pointer,'bus_address':pointer&0xffffff,
            'wrapper_accepts_signed_id':message_id < 0x8000}


def token(value):
    integer(value,65535,'token word')
    if value == 0: return {'type':'special_fixed_bitmap','word':0}
    if value & 0x8000:
        if value&255 not in range(0,22,2): raise ValueError('unresolved main-dialogue control selector')
        return {'type':'control','word':value}
    font.font16_row_column(value)
    # 0673A2 uses a signed WORD index. Offsets >=8000 address BEFORE the font,
    # even though the independently exported physical font spans 1034 glyphs.
    if font.font16_offset(value) >= 0x8000 or font.font16_index(value) >= font.FONT16_GLYPH_COUNT:
        raise ValueError('glyph outside confirmed signed-index font window')
    return {'type':'glyph','word':value}


def operation(value):
    item = token(value)
    return OPERATIONS[(value&255)//2] if item['type']=='control' else item['type']


def insertion_address(kind,index):
    """Raw main-consumer arithmetic, not an assertion of a valid gameplay ID."""
    integer(index,65535,'insertion index')
    if kind not in NAME_LAYOUT: raise ValueError('unknown insertion resource')
    base,multiplier=(0x08A504,6) if kind=='officer_names' else (0x08A212,4)
    return base+signed((index*multiplier)&65535)


def name_word(value):
    # Fixed editor policy for raw, uncoloured glyph IDs; not a CPU range check.
    integer(value,0x1fff,'name glyph')
    if token(value|0x4000)['type']!='glyph': raise ValueError('name must insert a glyph')
    return value


def insertion_stream(values,trim):
    sequence(values,3 if trim else 2)
    result=[name_word(v)|0x4000 for v in values]
    if trim:
        while result and result[-1]==0x403f: result.pop()
        if not result: raise ValueError('all-blank officer name would trim into unmodelled preceding RAM')
    return result+[0x800c]


def extract(rom):
    af.verify_rom(rom); check_anchors(rom)
    if longword(rom,DIRECTORY)!=PAGE_LAYOUT[0][0] or [word(rom,DIRECTORY+4+2*i) for i in range(2)] != [0,0x1A2]:
        raise ValueError('canonical directory topology changed')
    pages,targets = [],[]
    for index,(start,end,base) in enumerate(PAGE_LAYOUT):
        if longword(rom,start)!=base: raise ValueError('canonical page base changed')
        entries=[]
        for slot in range((end-start-4)//2):
            target=resolve_raw(rom,(index<<8)|slot)['pointer']
            entries.append(f'message_{target:06x}'); targets.append(target)
        pages.append({'index':index,'start':start,'end':end,'text_base':base,'entries':entries})
    if len(targets)!=275 or len(set(targets))!=275: raise ValueError('canonical target set changed')
    starts=sorted(targets)
    records=[]
    for start,end in zip(starts,starts[1:]+[TEXT_END]):
        if start&1 or end<=start or end-start>1024: raise ValueError('record extent invalid')
        values=[word(rom,p) for p in range(start,end,2)]
        if values[-1]!=0x8000 or 0x8000 in values[:-1]: raise ValueError('canonical record terminator changed')
        records.append({'id':f'message_{start:06x}','start':start,'end':end,'tokens':[token(v) for v in values]})
    if starts[0]!=0x92E84 or sum(row['end']-row['start'] for row in records)!=6308:
        raise ValueError('canonical text partition changed')
    names={kind:[{'id':f'{kind}_{i+first:03d}','index':i+first,'start':start+i*width*2,
                  'words':[name_word(word(rom,start+2*(i*width+j))) for j in range(width)]}
                 for i in range(count)] for kind,(start,count,width,first) in NAME_LAYOUT.items()}
    return {'schema_version':1,'format':'g5510_main_dialogue_fixed_layout',
            'directory':{'address':DIRECTORY,'page_base':PAGE_LAYOUT[0][0],'page_targets':[p['start'] for p in pages]},
            'pages':pages,'records':records,**names}


def blocks(rom,assets):
    """Validate editable fields and return disjoint field-encoded intervals."""
    expected=extract(rom)
    keys(assets,expected)
    for name in ('schema_version','format'):
        if type(assets[name]) is not type(expected[name]) or assets[name]!=expected[name]: raise ValueError('asset format changed')
    if assets['directory']!=expected['directory']: raise ValueError('directory topology changed')
    # Equality alone accepts bool as int; validate the immutable nested numbers too.
    keys(assets['directory'],expected['directory'])
    for name in ('address','page_base'): integer(assets['directory'][name],0xfffff,name)
    sequence(assets['directory']['page_targets'],2)
    for value in assets['directory']['page_targets']: integer(value,0xfffff,'page target')
    sequence(assets['records'],len(expected['records'])); sequence(assets['pages'],2)
    result=[]
    allowed={row['id']:row['start'] for row in expected['records']}
    def add(start,data,role,label): result.append({'start':start,'end':start+len(data),'data':data,'role':role,'id':label})
    add(DIRECTORY,PAGE_LAYOUT[0][0].to_bytes(4,'big')+bytes.fromhex('000001a2'),'directory','main_directory')
    for page,original in zip(assets['pages'],expected['pages']):
        keys(page,original)
        for name in ('index','start','end','text_base'):
            integer(page[name],0xfffff,name)
            if page[name]!=original[name]: raise ValueError('page metadata moved')
        sequence(page['entries'],len(original['entries']))
        data=bytearray(page['text_base'].to_bytes(4,'big'))
        for target in page['entries']:
            if type(target) is not str or target not in allowed: raise ValueError('unknown stable message target')
            delta=allowed[target]-page['text_base']
            if not -32768<=delta<=32767: raise ValueError('signed page offset overflow')
            data.extend(delta.to_bytes(2,'big',signed=True))
        add(page['start'],bytes(data),'page_offsets',f"page_{page['index']}")
    for record,original in zip(assets['records'],expected['records']):
        keys(record,original)
        for name in ('id','start','end'):
            if type(record[name]) is not type(original[name]) or record[name]!=original[name]: raise ValueError('record metadata moved')
        sequence(record['tokens'],len(original['tokens']))
        values=[]
        for item in record['tokens']:
            keys(item,('type','word'))
            if item != token(item['word']): raise ValueError('token kind does not match its word')
            values.append(item['word'])
        if operation(values[-1])!='restore_saved_mode' or any(operation(v)=='restore_saved_mode' for v in values[:-1]):
            raise ValueError('root stream must retain exactly one final mode-restore terminator')
        add(record['start'],b''.join(v.to_bytes(2,'big') for v in values),'message_tokens',record['id'])
    for kind,(_,count,width,_) in NAME_LAYOUT.items():
        sequence(assets[kind],count)
        for row,original in zip(assets[kind],expected[kind]):
            keys(row,original)
            for name in ('id','index','start'):
                if type(row[name]) is not type(original[name]) or row[name]!=original[name]:
                    raise ValueError('name record metadata moved')
            sequence(row['words'],width)
            insertion_stream(row['words'],kind=='officer_names')
            add(row['start'],b''.join(name_word(v).to_bytes(2,'big') for v in row['words']),
                'officer_name' if kind=='officer_names' else 'city_name',row['id'])
    result.sort(key=lambda row:row['start'])
    if any(a['end']>b['start'] for a,b in zip(result,result[1:])): raise ValueError('overlapping dialogue blocks')
    return result


def rebuild(rom,assets):
    result=bytearray(rom)
    for row in blocks(rom,assets): result[row['start']:row['end']]=row['data']
    return bytes(result)


def bank_source(bank,rows):
    integer(bank,15,'bank')
    for i,row in enumerate(rows):
        if row['start']<0 or row['start']&1 or row['end']<=row['start'] or row['end']&1:
            raise ValueError('invalid dialogue block extent')
        if row['end']-row['start']!=len(row['data']): raise ValueError('dialogue block width mismatch')
        if i and rows[i-1]['end']>row['start']: raise ValueError('unsorted or overlapping dialogue blocks')
    label=f'dialogue_bank_{bank:02x}'
    cursor=bank*65536; end=cursor+65536
    lines=[f'{label}:']
    for row in rows:
        if row['end']<=cursor or row['start']>=end: continue
        if row['start']<cursor or row['end']>end: raise ValueError('dialogue block crosses bank boundary')
        if cursor<row['start']:
            lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{row["start"]-cursor:X}')
        lines.extend([f'        .if (. - {label}) != 0x{row["start"]-bank*65536:X}',
                      '        .error "dialogue field offset changed"','        .endif',
                      f'        | {row["id"]}: {row["role"]}'])
        data=row['data']
        # Explicit BE32 pointer headers and BE16 signed offsets/token words.
        if row['role'] in ('directory','page_offsets'):
            lines.append(f'        .long 0x{int.from_bytes(data[:4],"big"):08X}'); data=data[4:]
        for offset in range(0,len(data),24):
            lines.append('        .word '+','.join(f'0x{word(data,p):04X}' for p in range(offset,min(offset+24,len(data)),2)))
        cursor=row['end']
    if cursor<end: lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{end-cursor:X}')
    lines.extend([f'        .if (. - {label}) != 0x10000','        .error "dialogue bank size changed"','        .endif'])
    return ('\n'.join(lines)+'\n').encode()


def manifest(rom,assets):
    rows=blocks(rom,assets)
    if rebuild(rom,assets)!=rom: raise ValueError('evidence must describe canonical assets')
    return {'schema_version':1,'canonical_source':{'size':len(rom),'sha256':sha(rom)},
            'confidence':'confirmed_static_consumer_and_physical_format',
            'page_counts':[len(p['entries']) for p in assets['pages']],
            'message_count':len(assets['records']),'message_bytes':6308,'editable_bytes':sum(r['end']-r['start'] for r in rows),
            'officer_name_count':256,'officer_name_bytes':1536,'city_name_count':40,'city_name_bytes':160,
            'city_id_catalog':[1,40],'city_index_zero_is_name_record':False,
            'unicode_mapping_complete':False,'natural_message_domain_complete':False,'complete_indirect_domains_added':0,
            'unresolved_ranges':[{'start':0x92C52,'end':0x92C56,'bytes':rom[0x92C52:0x92C56].hex(),
                'status':'unknown','reason':'Physical words alias group2 and point group3 into payload; not proven normal directory slots or length metadata.'}],
            'controls':dict(sorted(Counter(f'{t["word"]:04X}' for r in assets['records'] for t in r['tokens'] if t['type']=='control').items())),
            'owners':[{'id':r['id'],'start':r['start'],'end':r['end'],'role':r['role'],'status':'confirmed',
                       'sha256':sha(r['data']),'evidence':
                       ('00543A 8-bit masked index and 00543E..00544C stride6; 0672A2..0672DA insertion/trim' if r['role']=='officer_name' else
                        '00A8BA base08A216; 00A8CE/00A8EE 4x20-word consumer; 067306 biased ID1..40 insertion' if r['role']=='city_name' else
                        '0679D2 two-level signed lookup; 0671CA main token consumer; physical fixed record partition')} for r in rows],
            'consumer_anchors':[{'start':a,'end':a+len(bytes.fromhex(raw)),'bytes':raw,'ownership':False} for a,raw in sorted(ANCHORS.items())]}


def render_bundle(rom):
    from tools.dialogue_text.schema import asset_schema
    assets=extract(rom); info=manifest(rom,assets)
    stream=io.StringIO(newline=''); writer=csv.writer(stream,lineterminator='\n')
    writer.writerow(('message_id','page','slot','offset_address','signed_offset','record_id','record_start'))
    for page in assets['pages']:
        for slot,target in enumerate(page['entries']):
            message_id=page['index']*256+slot; lookup=resolve_raw(rom,message_id)
            writer.writerow((message_id,page['index'],slot,lookup['record_offset_address'],lookup['record_offset'],target,lookup['pointer']))
    report=(f'# Main-dialogue resource evidence\n\n'
        f'Status: confirmed static format and consumers, not natural selection of all messages.\n\n'
        f'{info["message_count"]} messages / 6308 token bytes; two physical pages with 207 and 68 entries.\n'
        f'{info["editable_bytes"]} fixed-layout editable bytes. The four bytes at 092C52..092C56 remain unknown.\n'
        '256 three-word officer names (1536 B) and 40 two-word city names (160 B) are editable.\n'
        'City IDs1..40 start at08A216; biased base08A212 points to two different preceding resources, NOT city0.\n'
        'All ordinary roots end in main-dialect mode-restore8000. 800C is a single saved-cursor return,\n'
        'not a general string terminator; FFFF is outside the confirmed control table.\n'
        'Token0000 selects a fixed border bitmap, not an empty string or a space.\n'
        'Name/city/numeric insertion parameters come from RAM, not inline command operands.\n'
        'Preserve signed offsets and the nonmonotonic second-page order. Rebinding page entries\n'
        'or changing same-width tokens does not establish edited-gameplay correctness.\n'
        'The raw resolver has no page/slot bounds checks; catalog bounds are editor constraints only.\n'
        'Glyph word indexing is signed; the editor rejects offsets8000..FFFF (addresses before the font).\n'
        'Unicode mapping and all natural message/return-cursor lifetimes remain unknown.\n')
    return {'assets.json':dump(assets),'assets.schema.json':dump(asset_schema()),'manifest.json':dump(info),
            'message_index.csv':stream.getvalue().encode(),'README.md':report.encode()}


def export_files(rom_path,output):
    source=af.safe_path(rom_path,regular_input=True); target=af.safe_path(output)
    af._separate(target,[source])
    if target.exists() or not target.parent.is_dir(): raise ValueError('fresh output directory with existing parent required')
    bundle=render_bundle(af._read(source,af.ROM_SIZE))
    staging=Path(tempfile.mkdtemp(prefix='.dialogue-text-',dir=target.parent)); state=staging.stat(); produced={}
    try:
        for name,data in bundle.items():
            with (staging/name).open('xb') as f: f.write(data)
            produced[name]=data
        af.safe_path(target)
        if target.exists(): raise ValueError('output appeared during generation')
        os.rename(staging,target)
    finally: af._cleanup_stage(staging,produced,state)
    return {'output':str(target),'files':sorted(bundle)}


def import_files(rom_path,asset_path,output):
    source=af.safe_path(rom_path,regular_input=True); asset=af.safe_path(asset_path,regular_input=True)
    target=af.safe_path(output); af._separate(target,[source,asset])
    if target.exists() or not target.parent.is_dir(): raise ValueError('fresh output file with existing parent required')
    rom=af._read(source,af.ROM_SIZE)
    result=rebuild(rom,af.load_assets(af._read(asset,8*1024*1024)))
    descriptor,tempname=tempfile.mkstemp(prefix='.dialogue-text-',dir=target.parent)
    temporary=Path(tempname); identity=temporary.stat(); complete=False
    try:
        with os.fdopen(descriptor,'wb') as stream:
            stream.write(result); stream.flush(); os.fsync(stream.fileno())
        complete=True
        af.safe_path(output)
        os.link(temporary,target)  # Atomic no-clobber publication; no input is overwritten.
    finally:
        if temporary.exists():
            af.safe_path(temporary,regular_input=True); current=temporary.stat()
            if complete and (current.st_dev,current.st_ino)==(identity.st_dev,identity.st_ino) and af._read(temporary,len(result))==result:
                temporary.unlink()
            else: raise ValueError('incomplete/modified temporary file retained for inspection')
    return {'output':str(target),'sha256':sha(result),'canonical_exact':result==rom,
            'changed_bytes':sum(a!=b for a,b in zip(rom,result))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','verify','import'))
    parser.add_argument('--rom',type=Path,default=DEFAULT_ROM)
    parser.add_argument('--assets',type=Path,default=DEFAULT_ASSETS)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.command=='export':
        if args.output is None: raise ValueError('--output required')
        print(json.dumps(export_files(args.rom,args.output))); return
    if args.command=='import':
        if args.output is None: raise ValueError('--output required')
        print(json.dumps(import_files(args.rom,args.assets,args.output))); return
    source=af.safe_path(args.rom,regular_input=True); assets_path=af.safe_path(args.assets,regular_input=True)
    rom=af._read(source,af.ROM_SIZE); assets=af.load_assets(af._read(assets_path,8*1024*1024))
    result=rebuild(rom,assets)
    print(json.dumps({'sha256':sha(result),'canonical_exact':result==rom,'editable_bytes':sum(r['end']-r['start'] for r in blocks(rom,assets))}))


if __name__=='__main__': main()
