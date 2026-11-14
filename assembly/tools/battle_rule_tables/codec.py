"""Lossless rule fields from actual WORD/LONG consumers, not numeric blobs.

024BB4/025438 use a class WORD and D2 to choose a32B-stride vector, then copy
exactly10 WORDs. This package owns only those20B, leaving12B per row unknown.
Three classes and16 rows are a physical editing catalog, not CPU index clamps.
00D270/011F20 read the3x3 LONG equipment-price matrix. Recruitment reads the
four budget and six troop denomination LONGs independently; their neighbouring
mirror-looking arrays remain unknown. Full source WORD/LONG bits are retained.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.vdp_word_streams import format as f
DEFAULT_ROM=f.DEFAULT_ROM
DEFAULT_FIELDS=ROOT/'analysis/battle_rule_tables/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/battle_rule_tables'
FORMAT='candidate-battle-equipment-recruitment-source-rules-v1'
EDITABLE_BYTES=2024
SIDES=(('ram_AF96',0x24C00),('ram_AF82',0x2546C))
DENOMINATIONS=(('recruitment_budget',0x1342C,4),('recruitment_troops',0x1344C,6))
sha=f.sha;dump=f.dump;uint=f.uint;keys=f.keys
def metadata():return dict(format=FORMAT,canonical_source=dict(size=f.ROM_SIZE,sha256=f.ROM_SHA),
    confidence='candidate',owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
def exact_list(value,count,label):
    if type(value) is not list or len(value)!=count:raise ValueError(label+': fixed physical count differs')
    return value
def vector_meta(side,base,group,count):return dict(id=f'{side}_class{group}_count{count:02d}',
    destination_RAM=int(side[4:],16)|0xFF0000,selector_class=group,list_count_slot=count,start=base+(group*16+count)*32)
def numbers(rom,start,count,width):return [int.from_bytes(rom[p:p+width],'big') for p in range(start,start+count*width,width)]
def encode_numbers(values,count,width,label):return b''.join(uint(value,(1<<(8*width))-1,label).to_bytes(width,'big')
    for value in exact_list(values,count,label))
def extract(rom):
    f.verify_rom(rom);fields=metadata()
    fields['battle_selector_classes']=numbers(rom,0x24BE4,14,2)
    fields['battle_vectors']=[dict(**vector_meta(side,base,group,count),position_index_WORDs=numbers(rom,base+(group*16+count)*32,10,2))
        for side,base in SIDES for group in range(3) for count in range(16)]
    fields['equipment_prices']=[dict(category=category,price_by_quality=numbers(rom,0xD2CA+category*12,3,4)) for category in range(3)]
    fields['denominations']=[dict(id=name,start=start,step_LONGs=numbers(rom,start,count,4)) for name,start,count in DENOMINATIONS]
    blocks(rom,fields);return fields
def blocks(rom,fields):
    f.verify_rom(rom);keys(fields,set(metadata())|{'battle_selector_classes','battle_vectors','equipment_prices','denominations'},'rule package')
    for key,value in metadata().items():f.same(fields[key],value,'package.'+key)
    result=[]
    def add(ident,start,data,role):result.append(dict(id=ident,start=start,end=start+len(data),data=data,role=role))
    add('battle_selector_classes',0x24BE4,encode_numbers(fields['battle_selector_classes'],14,2,'selector class WORD'),'candidate_battle_class_lookup_WORDs')
    rows=exact_list(fields['battle_vectors'],96,'battle vectors');i=0
    for side,base in SIDES:
        for group in range(3):
            for count in range(16):
                fixed=vector_meta(side,base,group,count);row=rows[i];i+=1
                keys(row,set(fixed)|{'position_index_WORDs'},'battle vector')
                for key,value in fixed.items():f.same(row[key],value,'vector.'+key)
                add(row['id'],row['start'],encode_numbers(row['position_index_WORDs'],10,2,'position index WORD'),
                    'candidate_battle_rank_to_position_WORDs')
    prices=exact_list(fields['equipment_prices'],3,'equipment categories');data=bytearray()
    for category,row in enumerate(prices):
        keys(row,{'category','price_by_quality'},'equipment category');f.same(row['category'],category,'category id')
        data.extend(encode_numbers(row['price_by_quality'],3,4,'price LONG'))
    add('equipment_prices',0xD2CA,bytes(data),'confirmed_equipment_price_LONGs')
    for row,(name,start,count) in zip(exact_list(fields['denominations'],2,'denomination tables'),DENOMINATIONS):
        keys(row,{'id','start','step_LONGs'},'denomination');f.same(row['id'],name,'denomination id');f.same(row['start'],start,'denomination start')
        add(name,start,encode_numbers(row['step_LONGs'],count,4,'step LONG'),'confirmed_'+name+'_denomination_LONGs')
    result.sort(key=lambda row:row['start'])
    if sum(len(row['data']) for row in result)!=EDITABLE_BYTES or any(a['end']>b['start'] for a,b in zip(result,result[1:])):
        raise ValueError('fixed nonoverlapping field scope differs')
    return result
def rebuild(rom,fields):
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)
def equipment_price(rom,fields,category,quality):
    """Bounded source catalog helper; its3x3 policy is NOT a CPU guard."""
    blocks(rom,fields);uint(category,2,'editor category');uint(quality,2,'editor quality')
    return fields['equipment_prices'][category]['price_by_quality'][quality]
def denomination(rom,fields,name,slot):
    blocks(rom,fields)
    if type(name) is not str or name not in {row[0] for row in DENOMINATIONS}:raise ValueError('unknown denomination table')
    row=next(row for row in fields['denominations'] if row['id']==name)
    uint(slot,len(row['step_LONGs'])-1,'editor denomination slot');return row['step_LONGs'][slot]
def _s16(value):return value-65536 if value&32768 else value
def assignment_lookup(memory,side,selector_WORD,count_WORD):
    """Original indexed source reads, not a CPU/RAM execution reference.

    Original shift/add operations wrap WORD, each address offset sign-extends.
    Out-of-catalog source reads are permitted if supplied memory contains them;
    outside supplied memory fails. No natural formation/count domain is claimed.
    """
    if type(memory) is not bytes:raise ValueError('read-only memory bytes required')
    if type(side) is not str or side not in dict(SIDES):raise ValueError('unknown source side')
    uint(selector_WORD,65535,'selector WORD');uint(count_WORD,65535,'count WORD')
    selector_address=0x24BE4+_s16((selector_WORD<<1)&65535)
    if selector_address<0 or selector_address+2>len(memory):raise ValueError('selector read outside memory')
    group=int.from_bytes(memory[selector_address:selector_address+2],'big')
    offset=((((group<<4)&65535)+count_WORD)&65535)<<5&65535
    address=dict(SIDES)[side]+_s16(offset)
    if address<0 or address+20>len(memory):raise ValueError('vector read outside memory')
    return dict(selector_address=selector_address,selector_class_WORD=group,address=address,
        position_index_WORDs=numbers(memory,address,10,2),in_editor_catalog=selector_WORD<14 and group<3 and count_WORD<16)
def load_fields(data):return f.load_json(data)
def schema():
    def obj(properties):return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def fixed(value):
        if type(value) is dict:return obj({key:fixed(item) for key,item in value.items()})
        return dict(type={str:'string',int:'integer'}[type(value)],const=value)
    def number(high):return dict(type='integer',minimum=0,maximum=high)
    def array(n,item):return dict(type='array',minItems=n,maxItems=n,items=item)
    props={key:fixed(value) for key,value in metadata().items()}
    props['battle_selector_classes']=array(14,number(65535))
    props['battle_vectors']=array(96,obj(dict(id=dict(type='string'),destination_RAM=number(0xFFFFFF),
        selector_class=number(2),list_count_slot=number(15),start=number(f.ROM_SIZE),position_index_WORDs=array(10,number(65535)))))
    props['equipment_prices']=array(3,obj(dict(category=number(2),price_by_quality=array(3,number(0xFFFFFFFF)))))
    props['denominations']=array(2,obj(dict(id=dict(type='string',enum=[row[0] for row in DENOMINATIONS]),start=number(f.ROM_SIZE),
        step_LONGs=dict(type='array',minItems=4,maxItems=6,items=number(0xFFFFFFFF)))))
    result=obj(props);result['$schema']='https://json-schema.org/draft/2020-12/schema'
    result['description']='Runtime enforces physical metadata/order/counts; full numeric bits are source fields, not natural CPU domains.'
    return result
def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('whole-ROM field roundtrip differs')
    unknown=[[base+(group*16+count)*32+20,base+(group*16+count+1)*32]
        for side,base in SIDES for group in range(3) for count in range(16)]
    report=dict(editable_bytes=EDITABLE_BYTES,physical_blocks=100,whole_ROM_exact=True,whole_ROM_sha256=sha(image),
        confidence='confirmed_read_widths_candidate_battle_role_confirmed_equipment_and_recruitment_rules',
        battle_vectors=dict(source_bases=[0x24C00,0x2546C],destination_RAM=[0xFFAF96,0xFFAF82],physical_classes=3,
            physical_rows_per_class=16,stride_bytes=32,read_WORDs_per_row=10,owned_bytes=1920,
            class_selector_table=[0x24BE4,0x24C00],selector_readers=[0x24BBA,0x25442],
            first_WORD_reads=[0x24BCE,0x25456],last_WORD_reads=[0x24BE0,0x25468],
            downstream_position_index_reads=[0x2521C,0x25A88],position_pair_BYTE_reads=[0x25228,0x25238,0x25A94,0x25AA4],
            unknown_unread_row_tails=unknown,unknown_unread_bytes=1152,original_count_source='D2.W list count',
            index_semantics='WORD shifts/adds wrap16, signed WORD address offsets; no3-class/16-count CPU clamp'),
        equipment_prices=dict(start=0xD2CA,end=0xD2EE,source_shape='3 categories x3 qualities xBE32',
            LONG_readers=[0xD27A,0xD286,0xD292,0x11F2C,0x11F38,0x11F44],price_loader_destination=[0xFFEF6A,0xFFEF6E,0xFFEF72]),
        recruitment_budget=dict(start=0x1342C,end=0x1343C,source_shape='4xBE32',LONG_readers=[0x1333A,0x1336C]),
        recruitment_troops=dict(start=0x1344C,end=0x13464,source_shape='6xBE32',LONG_readers=[0x12A18,0x12A3A,0x13354,0x13384,0x13822,0x13870]),
        unknown_neighbor_arrays=[[0x1343C,0x1344C],[0x13464,0x1347C]],
        reused_semantic_evidence=['weapon_extended 00D2CA price schema','gameplay_rules recruitment denomination consumers'],
        source_numeric_bits_preserved=True,edited_gameplay_safety_proven=False,independent_CPU_comparison=False,
        natural_selector_domain_complete=False,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0)
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(format=FORMAT,confidence='candidate',editable_bytes=EDITABLE_BYTES,
        canonical_source=metadata()['canonical_source'],members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()},
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0))
    return members
def fresh_output(value):
    path=f.safe_path(value)
    if path==OUTPUT_ROOT or OUTPUT_ROOT not in path.parents:raise ValueError('output must stay in build/battle_rule_tables')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output')
    args=p.parse_args(argv);target=None
    if args.command!='verify':
        if args.output is None:raise ValueError('fresh output required')
        target=fresh_output(args.output) # output authority BEFORE input reads
        if args.command=='import' and target.suffix.lower()!='.bin':raise ValueError('fresh .bin required')
    elif args.output is not None:raise ValueError('verify writes no output')
    rom=f.read_bounded(args.rom,f.ROM_SIZE)
    if args.command=='export':
        bundle=render_bundle(rom);target.mkdir()
        for name,data in bundle.items():f.put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES)
    else:
        image=rebuild(rom,load_fields(f.read_bounded(args.fields,f.MAX_JSON)))
        if target is not None:f.put(target,image)
        result=dict(path=None if target is None else str(target),sha256=sha(image),exact_canonical=image==rom,editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
