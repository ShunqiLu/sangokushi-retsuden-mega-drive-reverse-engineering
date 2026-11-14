"""Lossless UI source fields; physical allocation is not a CPU length clamp.

Editable fragments preserve complete words/LONGs. Their packing kind is not a
promise about edited CPU interpretation: views decode the serialized bytes.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import struct

from tools.graphics_build import graphics_build as gb

ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=ROOT.parent/'work/original_g5510.bin'
DEFAULT_ASSETS=ROOT/'analysis/ui_layouts/generated/assets.json'
FORMAT='g5510-ui-layout-source-v1'
START,END=0xAB8C4,0xABDCA
EDITABLE_BYTES=END-START
sha,dump=gb.sha,gb.dump
# id, start, end, packing format, confidence, width/rows/calls, evidence
REGIONS=(
    ('panel_25',0xAB8C4,0xABA0E,'ui_stream','confirmed',(25,2,10),('panel25_init','panel25_loop','panel25_caller','panel25_store')),
    ('clear_25',0xABA0E,0xABA16,'ui_stream','confirmed',(25,2,1),('clear25_caller',)),
    ('clear_38',0xABA16,0xABA1E,'ui_stream','confirmed',(38,2,1),('clear38_caller',)),
    ('vdp_pattern_transfer',0xABA1E,0xABA7E,'vdp_longwords','confirmed',None,('vdp_transfer',)),
    ('shared_panel_6',0xABA7E,0xABB26,'ui_stream','confirmed',(6,2,10),('shared_init','shared_condition','shared_skip','shared_caller','shared_normal_init_loop','shared_normal_caller')),
    ('candidate_panel_6',0xABB26,0xABBC2,'ui_stream','candidate',(6,20,1),('renderer','dispatch_table')),
    ('panel_8',0xABBC2,0xABC02,'ui_stream','confirmed',(8,7,1),('panel8_caller',)),
    ('clear_8',0xABC02,0xABC1E,'ui_stream','confirmed',(8,7,1),('clear8_caller',)),
    ('panel_6',0xABC1E,0xABC6E,'ui_stream','confirmed',(6,10,1),('panel6_caller',)),
    ('glyph_pair_descriptors',0xABC6E,0xABC72,'glyph_words','confirmed',None,('glyph_pair_caller','glyph_descriptor_read','glyph_descriptor_loop')),
    ('panel_12x6',0xABC72,0xABCBE,'ui_stream','confirmed',(12,6,1),('panel12x6_caller',)),
    ('panel_12x7',0xABCBE,0xABD12,'ui_stream','confirmed',(12,7,1),('panel12x7_caller',)),
    ('panel_10',0xABD12,0xABDCA,'ui_stream','confirmed',(10,2,9),('panel10_init','panel10_init_alt','panel10_init_third','panel10_loop','panel10_caller')),
)
ANCHORS={
    'renderer':(0x26BFA,'43f8d100d2f8f31a3e01534732c032c206420080360038186b0e4840884032c448405343600000163a0402447fffee4c08840000383b401c4ebb40244a4366d651cfffca42515440c0c1e348d178f31a4e75'),
    'dispatch_table':(0x26C4C,'0000001a0036007e00c400d8'),
    'repeat_handler':(0x26C58,'024500ff4840381888403c05534632c451cefffc964548404e75'),
    'increment_handler':(0x26C72,'024500ff4840381888403c05534632c4544451cefffa964548404e75'),
    'decimal_word_handler':(0x26C8E,'024500ff245848e7fc00700030123238f6923438f6944df8d3004eb90001270a4cdf003f383c00069845e34c45f8d300d4c43805534448403c1a8c4032c651ccfff8484096454e75'),
    'decimal_long_handler':(0x26CD6,'024500ff245848e7fc0020123238f6923438f6944df8d3004eb90001270a4cdf003f383c00069845e34c45f8d300d4c43805534448403c1a8c4032c651ccfff8484096454e75'),
    'glyph_even_handler':(0x26D1C,'24583a12e54dda78' 'ef7632c5544532c555434e75'),
    'glyph_odd_handler':(0x26D30,'24583a12e54dda78ef76524532c5544532c555434e75'),
    'panel25_init':(0x18ED4,'41f9000ab8c421c8f6c0'),
    'panel25_loop':(0x190C6,'0c78000af36a640c' '6100001e5278f36a60000014'),
    'panel25_caller':(0x190EE,'2078f6c0203cc0000019323c00023438f36ae14a0642c08e31fcc386f69231fcc401f6944eb900026bfa'),
    'panel25_store':(0x19118,'21c8f6c04e75'),
    'clear25_caller':(0x1913E,'41f9000aba0e203cc0000019323c00023638f36ae14b343cc98e94434eb900026bfa'),
    'clear38_caller':(0x19276,'41f9000aba16203cc0000026323c00023638f36ae14b343ccd0294434eb900026bfa'),
    'vdp_transfer':(0x17932,'23fc6000000200c0000443f9000aba1e303c001723d900c0000051c8fff8'),
    'shared_init':(0x196C4,'21fc000aba7ef6c04e75'),
    'shared_condition':(0x196E2,'0c78000af36a650e5278f36231fc0008cfd26000004408380001f6d7670000140c780004f36a6600000a'),
    'shared_skip':(0x1970C,'06b800000018f6c0'),
    'shared_caller':(0x19714,'2078f6c0203cc0000006323c00023438f36ae14a0642c0404eb900026bfa21c8f6c0'),
    'shared_normal_caller':(0x19B96,'2078f6c0203cc0000006323c00023438f36ae14a0642c0404eb900026bfa21c8f6c0'),
    'shared_normal_init_loop':(0x19B72,'21fc000aba7ef6c04278f6d44e750c78000af36a650e5278f36231fc0008cfd260000028'),
    'panel8_caller':(0x1D73E,'203cc0000008323c0007343cc4a241f9000abbc24eb900026bfa'),
    'clear8_caller':(0x1D890,'203cc0000008323c0007343cc4a241f9000abc024eb900026bfa'),
    'panel6_caller':(0x20488,'41f9000abc1e203cc0000006323c000a343cc3a24eb900026bfa'),
    'glyph_pair_caller':(0x20E88,'363c000141f9000a' 'bc6e43f8d3004eb90000ae8a'),
    'glyph_descriptor_read':(0xAE8A,'48e70f2038186b46'),
    'glyph_descriptor_loop':(0xAECE,'51cbffbe4cdf04f04e75'),
    'panel12x6_caller':(0x20EE6,'41f9000abc72203cc000000c323c0006343cc19c4eb900026bfa'),
    'panel12x7_caller':(0x20F08,'41f9000abcbe203cc000000c323c0007343cc51c4eb900026bfa'),
    'panel10_init':(0x211FE,'21fc000abd12f6c0'),
    'panel10_init_alt':(0x21BF6,'21fc000abd12f6c0'),
    'panel10_init_third':(0x21E3A,'21fc000abd12f6c0'),
    'panel10_loop':(0x212DA,'0c780009f36a6400003a4a78f36a6600000831fc00acf600'),
    'panel10_caller':(0x212F2,'2078f6c0203cc000000a323c00023438f36ae14a0642c0b64eb900026bfa21c8f6c0'),
    'geometry_point_zero_reader':(0x25C02,'47f89fff3038f68a42421433000047f9000abda8eb48e34ad440424010332000424112332001'),
}
OPERATIONS=('repeat','increment_by_two','decimal_from_word','decimal_from_long','glyph_pair_even','glyph_pair_odd')


def check_anchors(rom):
    for name,(start,raw) in ANCHORS.items():
        if rom[start:start+len(raw)//2]!=bytes.fromhex(raw):
            raise ValueError('original UI consumer anchor changed: '+name)


def verify_rom(rom):
    gb.af.verify_rom(rom); check_anchors(rom)


def _integer(value,bits,label): return gb.rf.integer(value,(1<<bits)-1,label)


def _command(image,address,limit):
    """Decode one immutable-source command, never dereference a runtime pointer."""
    if address<0 or address+2>limit: return {'status':'source_boundary','address':address}
    word=int.from_bytes(image[address:address+2],'big')
    if word<0x8000:
        return {'status':'decoded','start':address,'end':address+2,'kind':'literal',
                'word':word,'operation':'literal_or_attribute','output_words':1,'column_decrement':1}
    index=((word&0x7FFF)>>7)&0xFFFE; opcode=index//2
    if opcode>=6:
        return {'status':'unknown_dispatch','start':address,'end':address+2,
                'control_word':word,'dispatch_index':index,'dispatch_table_address':0x26C4C+index,
                'meaning':'Original CPU has no opcode<6 check; this format view cannot predict the external handler.'}
    size=4 if opcode<2 else 6
    if address+size>limit: return {'status':'operand_boundary','address':address,'control_word':word,'required_bytes':size}
    count=(word&255) if opcode<4 else 2
    result={'status':'decoded','start':address,'end':address+size,'operation':OPERATIONS[opcode],
            'control_word':word,'dispatch_index':index,'handler':0x26C58+(0,0x1A,0x36,0x7E,0xC4,0xD8)[opcode],
            'output_words':count if count else 65536,'column_decrement':count}
    if opcode<2: result.update(kind='word_command',operand_word=int.from_bytes(image[address+2:address+4],'big'))
    else: result.update(kind='pointer_command',pointer_long=int.from_bytes(image[address+2:address+6],'big'),target_read_bytes=4 if opcode==3 else 2)
    return result


def decode_view(data,start=0):
    """Physical fragment view; stopping at a block end is an editor boundary."""
    if type(data) is not bytes or len(data)%2: raise ValueError('even immutable source bytes required')
    records=[]; cursor=0
    while cursor<len(data):
        row=_command(data,cursor,len(data))
        if row['status']!='decoded':
            if 'start' in row: row['start']+=start; row['end']+=start
            if 'address' in row: row['address']+=start
            return {'status':row['status'],'commands':records,'boundary':row,
                    'decoded_bytes':cursor,'unresolved_bytes':len(data)-cursor}
        cursor=row['end']; row['start']+=start; row['end']+=start; records.append(row)
    return {'status':'decoded','commands':records,'decoded_bytes':cursor,'unresolved_bytes':0}


def _fragment(row):
    if row['kind']=='literal': return {'kind':'literal','word':row['word']}
    if row['kind']=='word_command': return {key:row[key] for key in ('kind','control_word','operand_word')}
    return {key:row[key] for key in ('kind','control_word','pointer_long')}


def extract(rom):
    verify_rom(rom); result=[]
    for name,start,end,kind,_,_,_ in REGIONS:
        row={'id':name,'kind':kind}
        if kind=='ui_stream':
            view=decode_view(rom[start:end],start)
            if view['status']!='decoded': raise ValueError('canonical UI fragment grammar changed: '+name)
            row['tokens']=[_fragment(token) for token in view['commands']]
        elif kind=='vdp_longwords': row['longwords']=list(struct.unpack_from('>24I',rom,start))
        else: row['words']=list(struct.unpack_from('>2H',rom,start))
        result.append(row)
    return {'schema_version':1,'format':FORMAT,'blocks':result}


def _encode_tokens(tokens):
    if type(tokens) is not list: raise ValueError('UI tokens must be a list')
    result=bytearray()
    for row in tokens:
        if type(row) is not dict: raise ValueError('UI fragment must be an object')
        kind=row.get('kind')
        if kind=='literal':
            gb.af._keys(row,{'kind','word'},'word fragment'); result.extend(struct.pack('>H',_integer(row['word'],16,'full word')))
        elif kind=='word_command':
            gb.af._keys(row,{'kind','control_word','operand_word'},'word command fragment')
            result.extend(struct.pack('>2H',_integer(row['control_word'],16,'full control word'),_integer(row['operand_word'],16,'full operand word')))
        elif kind=='pointer_command':
            gb.af._keys(row,{'kind','control_word','pointer_long'},'pointer command fragment')
            result.extend(struct.pack('>HI',_integer(row['control_word'],16,'full control word'),_integer(row['pointer_long'],32,'full pointer LONG')))
        else: raise ValueError('unknown packing fragment kind')
    return bytes(result)


def blocks(rom,assets):
    verify_rom(rom); gb.af._keys(assets,{'schema_version','format','blocks'},'UI source')
    if type(assets['schema_version']) is not int or assets['schema_version']!=1 or assets['format']!=FORMAT:
        raise ValueError('fixed schema/format changed')
    result=[]
    for row,(name,start,end,kind,_,_,_) in zip(gb.exact_list(assets['blocks'],len(REGIONS),'physical blocks'),REGIONS):
        field='tokens' if kind=='ui_stream' else 'longwords' if kind=='vdp_longwords' else 'words'
        gb.af._keys(row,{'id','kind',field},'physical UI block')
        if type(row['id']) is not str or row['id']!=name or row['kind']!=kind: raise ValueError('fixed physical identity/order changed')
        if kind=='ui_stream': data=_encode_tokens(row[field])
        elif kind=='vdp_longwords': data=struct.pack('>24I',*[_integer(v,32,'full transfer LONG') for v in gb.exact_list(row[field],24,field)])
        else: data=struct.pack('>2H',*[_integer(v,16,'full glyph descriptor') for v in gb.exact_list(row[field],2,field)])
        if len(data)!=end-start: raise ValueError('fixed physical source size changed: '+name)
        result.append({'id':name,'start':start,'end':end,'role':'ui_'+kind,'data':data})
    return result


def rebuild(rom,assets):
    image=bytearray(rom)
    for row in blocks(rom,assets): image[row['start']:row['end']]=row['data']
    return bytes(image)


def walk_rows(image,start,width,rows,*,command_budget=4096):
    """Source-format projection only: does not model queue writes or shared RAM.

    Source may cross authoring blocks. Zero widths/counts are not no-ops; WORD
    decrement wrap is retained. The external command budget is not a CPU clamp.
    """
    if type(image) is not bytes: raise ValueError('immutable source image required')
    _integer(start,32,'source address'); _integer(width,16,'row width'); _integer(rows,16,'row count')
    if type(command_budget) is not int or command_budget<1: raise ValueError('positive format-view budget required')
    cursor=start; commands=[]; row=0; remaining=width; outputs=0; total_rows=rows or 65536
    while row<total_rows and len(commands)<command_budget:
        token=_command(image,cursor,len(image))
        if token['status']!='decoded':
            return {'status':token['status'],'start':start,'end':cursor,'rows_completed':row,
                    'remaining_word':remaining,'commands':commands,'boundary':token,'output_words':outputs}
        token['row']=row; commands.append(token); cursor=token['end']; outputs+=token['output_words']
        remaining=(remaining-token['column_decrement'])&65535
        if remaining==0: row+=1; remaining=width
    return {'status':'complete' if row==total_rows else 'command_budget','start':start,'end':cursor,
            'rows_completed':row,'remaining_word':remaining,'commands':commands,'output_words':outputs}


def conditional_views(rom,assets):
    image=rebuild(rom,assets); paths=[]
    for name,start,end,kind,confidence,shape,evidence in REGIONS:
        if shape is None: continue
        width,rows,calls=shape
        for special in ((False,True) if name=='shared_panel_6' else (False,)):
            pointer=start; frames=[]; ranges=[]
            for call in range(calls):
                if special and call==4: pointer+=24
                frame=walk_rows(image,pointer,width,rows); frames.append(frame)
                for command in frame['commands']: ranges.append((command['start'],command['end']))
                pointer=frame['end']
                if frame['status']!='complete': break
            referenced={p for a,z in ranges for p in range(a,z)}
            paths.append({'id':name+('_skip24' if special else ''),'block_id':name,'confidence':confidence,
                'known_caller':confidence=='confirmed','shape':{'width_word':width,'rows_word':rows,'calls':calls},
                'skip24_before_call':4 if special else None,'frames':frames,'final_source':pointer,
                'unique_source_bytes':len(referenced),'reference_ranges':_ranges(referenced),
                'status':'complete' if len(frames)==calls and all(f['status']=='complete' for f in frames) else 'boundary'})
    return {'format':FORMAT,'source_model':'immutable source-format projection only; not full CPU execution',
            'natural_selection':False,'pointers_dereferenced':False,'paths':paths}


def _ranges(values):
    result=[]
    for value in sorted(values):
        if result and result[-1]['end']==value: result[-1]['end']+=1
        else: result.append({'start':value,'end':value+1})
    return result


def inspect(rom,assets):
    intervals=blocks(rom,assets); image=rebuild(rom,assets); warnings=[]; views=[]
    for source,row in zip(assets['blocks'],intervals):
        if source['kind']!='ui_stream': continue
        view=decode_view(row['data'],row['start']); views.append({'id':row['id'],**view})
        if view['status']!='decoded': warnings.append({'code':'format_view_boundary','id':row['id'],'status':view['status']})
        decoded=[_fragment(token) for token in view['commands']]
        if decoded!=source['tokens']: warnings.append({'code':'edited_packing_kind_differs_from_decoded_grammar','id':row['id'],
            'meaning':'Packing fragments preserve bytes; actual control bits decide CPU interpretation, not the JSON kind label.'})
        for token in view['commands']:
            if token.get('column_decrement')==0:
                warnings.append({'code':'zero_count_is_65536_outputs_not_noop','address':token['start']})
            if token['operation'] in OPERATIONS[2:4] and token['column_decrement']>6:
                warnings.append({'code':'numeric_count_exceeds_six_word_scratch','address':token['start'],'count':token['column_decrement']})
            if token.get('pointer_long',0)&1:
                warnings.append({'code':'odd_pointer_word_or_long_read','address':token['start'],'pointer_long':token['pointer_long']})
    paths=conditional_views(rom,assets)
    for path in paths['paths']:
        if path['status']!='complete': warnings.append({'code':'conditional_layout_projection_boundary','id':path['id']})
        region=next(r for r in REGIONS if r[0]==path['block_id'])
        if any(r['start']<region[1] or r['end']>region[2] for r in path['reference_ranges']):
            warnings.append({'code':'layout_reads_outside_physical_block','id':path['id']})
    return {'format':FORMAT,'canonical_exact':image==rom,'sha256':sha(image),
        'changed_bytes':sum(a!=b for a,b in zip(rom,image)),'editable_bytes':EDITABLE_BYTES,
        'warning_policy':'report_only_no_normalization','warnings':warnings,'command_views':views,
        'conditional_paths':paths['paths'],'geometry_point_zero_alias':{'address':0xABDC8,'word':int.from_bytes(image[0xABDC8:0xABDCA],'big'),
            'meaning':'Same physical last panel_10 word; no independent coordinate source.'},
        'edited_gameplay_validated':False,'natural_selection_domain_complete':False}


def manifest(rom):
    assets=extract(rom); intervals=blocks(rom,assets); paths=conditional_views(rom,assets); owners=[]; union=set()
    for path in paths['paths']:
        if path['status']!='complete': raise ValueError('canonical conditional grammar drift')
        if path['known_caller']:
            union.update(p for row in path['reference_ranges'] for p in range(row['start'],row['end']))
    if len(union)!=1030: raise ValueError('known caller UI reference union changed')
    for row,region in zip(intervals,REGIONS):
        name,start,end,kind,confidence,shape,evidence=region
        if kind=='ui_stream' and confidence=='confirmed' and not set(range(start,end))<=union:
            raise ValueError('declared UI field lacks conditional source reference')
        owners.append({key:row[key] for key in ('id','start','end','role')}|{
            'size':end-start,'confidence':confidence,'sha256':sha(row['data']),'evidence':list(evidence),
            'purpose_scope':'Original command/source fields and conditional readers, not complete UI behavior or natural reachability.',
            'unknown_components':['natural caller domain','shared queue lifetime','edited gameplay validity']+
                (['actual caller for this candidate allocation'] if confidence=='candidate' else [])})
    return {'format':FORMAT,'schema_version':1,'canonical_rom_sha256':sha(rom),'source_fields_sha256':sha(dump(assets)),
        'editable_bytes':EDITABLE_BYTES,'build_block_count':len(intervals),'confirmed_bytes':1130,'candidate_bytes':156,
        'known_caller_ui_reference_bytes':len(union),'independent_transfer_bytes':96,'independent_glyph_descriptor_bytes':4,
        'owners':owners,'conditional_reference_ranges':_ranges(union),
        'conditional_paths':[{key:path[key] for key in ('id','block_id','confidence','known_caller','shape','skip24_before_call','final_source','unique_source_bytes','reference_ranges')} for path in paths['paths']],
        'consumer_anchors':[{'id':name,'start':a,'end':a+len(raw)//2,'bytes':raw,'sha256':sha(bytes.fromhex(raw)),
            'kind':'relative_dispatch_words' if name=='dispatch_table' else 'original_instruction_anchor'} for name,(a,raw) in ANCHORS.items()],
        'aliases':[{'id':'shared_panel_condition_paths','confidence':'confirmed','start':0xABA7E,'end':0xABB26,
                   'meaning':'Two caller paths share one source. Ordinary reads156B; skip24 before call4 reads144B; their union168B is not one contiguous execution.'},
                  {'id':'geometry_point_zero','confidence':'confirmed','start':0xABDC8,'end':0xABDCA,
                   'reader_start':0x25C02,'reader_end':0x25C28,'meaning':'F68A=1/point=0 reads the same final UI word 1B80; no duplicated editable coordinate.'}],
        'natural_selection_domain_complete':False,'runtime_validation_added':False,'complete_indirect_domains_added':0,
        'boundaries':['Physical block lengths and packing kinds are editor layout, not CPU semantic clamps.',
            'Commands are literal words or control plus WORD/LONG pointer; all source bits remain editable.',
            'Fragment kind chooses serialized widths only. Changed control bits are decoded again from bytes and never normalized.',
            'Six known handlers do not bound the original computed dispatch; unsupported opcodes stop this format view only.',
            'ABB26..ABBC2 is candidate: 6x20 syntax has no confirmed caller and adds no primary ownership.',
            'Row and run zero counts use real WORD/DBRA behavior; numeric width above6 is not clipped.',
            'Source-format views never read dynamic pointer targets, precompute numeric results, or model shared queue/stack side effects.',
            '96B transfer and4B glyph descriptor are different formats from the UI command streams.',
            'This codec adds no natural runtime evidence or complete indirect domain.']}


def schema():
    word={'type':'integer','minimum':0,'maximum':65535}; long={'type':'integer','minimum':0,'maximum':4294967295}
    def obj(fields): return {'type':'object','additionalProperties':False,'required':list(fields),'properties':fields}
    variants=[obj({'kind':{'const':'literal'},'word':word}),
              obj({'kind':{'const':'word_command'},'control_word':word,'operand_word':word}),
              obj({'kind':{'const':'pointer_command'},'control_word':word,'pointer_long':long})]
    records=[]
    for name,start,end,kind,_,_,_ in REGIONS:
        fields={'id':{'const':name},'kind':{'const':kind}}
        if kind=='ui_stream': fields['tokens']={'type':'array','minItems':1,'maxItems':(end-start)//2,'items':{'oneOf':variants}}
        else:
            key,count,item=('longwords',24,long) if kind=='vdp_longwords' else ('words',2,word)
            fields[key]={'type':'array','minItems':count,'maxItems':count,'items':item}
        records.append(obj(fields))
    return {'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Full-width UI source fragments',
        **obj({'schema_version':{'type':'integer','const':1},'format':{'const':FORMAT},
               'blocks':{'type':'array','minItems':len(REGIONS),'maxItems':len(REGIONS),'items':False,'prefixItems':records}}),
        '$comment':'Runtime enforces exact byte extent per block, rejects bool/float integers/duplicate keys/nonfinite values. Packing labels do not constrain changed CPU control bits; format warnings never rewrite source.'}


def render_bundle(rom):
    info=manifest(rom)
    report=('# UI source fields and conditional command layouts\n\n'
        'confirmed: assets.json is the sole editable source. All other files are derived.\n\n'
        '- confirmed: 13 physical blocks, AB8C4..ABDCA, 1286 editable bytes; 1030 known-caller UI bytes plus 96 transfer bytes and 4 glyph descriptor bytes.\n'
        '- candidate: ABB26..ABBC2 (156 bytes) parses as 6x20 but has no confirmed caller; it is not an owner.\n'
        '- confirmed: commands retain full control WORDs, operand WORDs and pointer LONGs. The six known operations are repeat, increment by2, decimal from WORD/LONG, and two glyph-pair variants.\n'
        '- confirmed: editable packing labels choose representation widths; actual control bits are re-decoded from serialized bytes. Modified labels/controls can diverge and produce warnings, never hidden normalization.\n'
        '- confirmed: both ABA7E paths share one physical source. Reads156B versus144B produce union168B; the skip path omits24B before call4.\n'
        '- confirmed: the last UI word ABDC8 is also geometry map1/point0 source; only one editable word exists.\n'
        '- confirmed: format walks are immutable-source views, not CPU execution, and do not dereference live pointers or snapshot stack aliases.\n'
        '- unknown: natural domains, shared queue/stack lifetime and edited gameplay validity. Zero/run/row and numeric-overwidth conditions are not clamped.\n'
        '- confirmed: no new natural runtime observation or complete indirect domain is claimed.\n')
    return {'assets.json':dump(extract(rom)),'schema.json':dump(schema()),'manifest.json':dump(info),
            'command_views.json':dump(conditional_views(rom,extract(rom))),'README.md':report.encode()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','verify','import')); parser.add_argument('--rom',type=Path,default=DEFAULT_ROM)
    parser.add_argument('--assets',type=Path,default=DEFAULT_ASSETS); parser.add_argument('--output',type=Path)
    args=parser.parse_args(); read=lambda p:gb.af._read(gb.af.safe_path(p,regular_input=True),4*1024*1024)
    rom=read(args.rom); verify_rom(rom)
    if args.command=='export': bundle=render_bundle(rom); inputs=[args.rom]
    else:
        assets=gb.af.load_assets(read(args.assets)); report=inspect(rom,assets)
        if args.command=='verify': print(dump(report).decode(),end=''); return
        bundle={'rebuilt.bin':rebuild(rom,assets),'validation.json':dump(report)}; inputs=[args.rom,args.assets]
    if args.output is None: raise ValueError('--output required')
    print(gb.publish(bundle,args.output,inputs))


if __name__=='__main__': main()
