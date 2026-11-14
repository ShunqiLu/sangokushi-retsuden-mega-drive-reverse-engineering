"""Six physically adjacent, full-width battlefield resource families.

The fixed forty-record editor catalog is not a CPU selector clamp. Physical
fields have one editable authority, including pre-record and cross-family reads.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import struct

from tools.graphics_build import graphics_build as gb

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = ROOT.parent/'work/original_g5510.bin'
DEFAULT_ASSETS = ROOT/'analysis/battlefield_resources/generated/assets.json'
FORMAT = 'g5510-full-width-battlefield-resources-v1'
COUNT = 40
START, END = 0xABDCA, 0xAE39A
EDITABLE_BYTES = END-START
sha, dump = gb.sha, gb.dump
# Names of selection fields describe source grouping, not officer/AI semantics.
FAMILIES = (
    ('coordinates_a',0xABDCA,32,(('words',16),),'confirmed',('coordinate_a_copy','coordinate_a_variable','coordinate_a_variable_alt')),
    ('coordinates_b',0xAC2CA,32,(('words',16),),'confirmed',('coordinate_b_first','coordinate_b_copy')),
    ('selection_108',0xAC7CA,108,(('header_words',2),('candidate_groups',(8,6)),('tail_words',4)),'confirmed',('selection_108_entry','selection_108_tail','selection_108_pool')),
    ('selection_58',0xAD8AA,58,(('leading_word',1),('prefix_words',5),('secondary_words',3),('candidate_groups',(4,5))),'confirmed',('selection_58_entry','selection_58_pool','selection_58_alias')),
    ('rectangles',0xAE1BA,8,(('bounds_words',4),),'confirmed',('rectangle_inclusive','rectangle_strict')),
    ('centers',0xAE2FA,4,(('center_words',2),),'confirmed',('center_reader',)),
)
ANCHORS = {
    'coordinate_a_copy':(0x1E8C6,'3038f68aeb4841f9000abdaad0c043f8afaa323c000f32d851c9fffc4e75'),
    'coordinate_a_variable':(0x1A20A,'3438f68a41f89fff4241123020006728e349eb4ad44143f9000abda8424010312000e748424112312001e749'),
    'coordinate_a_variable_alt':(0x25C02,'47f89fff3038f68a42421433000047f9000abda8eb48e34ad440424010332000424112332001'),
    'coordinate_b_first':(0x1ED44,'41f9000ac2aa3038f68aeb4843f8a1503238a5a4e549424214300000e74aef4a33821000424214300001e74aef4a338210024e75'),
    'coordinate_b_copy':(0x1ED9A,'41f9000ac2ac3038f68aeb48d0c043f8afaa32fcffff303c000e32d851c8fffc4e75'),
    'selection_108_entry':(0x25AB2,'41f9000ac75e3038f68a3200e348d041e548d041e348d041e548d0c043f8d3103038f61c0240000232f000004a406600000452403238f68a4df89fff1d80100058482449303c0007425a51c8fffc61000086610000826100007e6100007a61000076610000726100006e6100006a'),
    'selection_108_tail':(0x25B20,'0c780017f68a6700001c45f8d300303c0003426a000834d851c8fff86100f7bc6000002c45f8d300303c0007425251c8fffc0c380014d31165000006d0fc000431d0d30031e80002d3026100f78e32f8d30033f8d30000ff3eca32b8d30233f8d30200ff3ecc4e75'),
    'selection_108_pool':(0x25B88,'45f8d300303c000534d851c8fffc425a42526100f75e45f8d300301ab078d31267f8b078d31467f2b078d31667ecb078d31867e6b078d31a67e0b078d31c67dab078d31e67d4b078d32067ce32c04e75'),
    'selection_58_entry':(0x25246,'41f9000ad8703038f68a3200e348d041e348d041e548d041e348d0c043f8d31032d845f8d300303c000434d851c8fffc425a425a425a6100007c45f8d300303c000432da51c8fffc45f8d300303c000234d851c8fffc425a425a425a425a425a6100005245f8d300303c000232da51c8fffc4278f7444278f7464278f7486100007231c0f74433c000ff3ec26100006431c0f74633c000ff3ec46100005631c0f74833c000ff3ec66100004833c000ff3ec84e75'),
    'selection_shuffle':(0x252FA,'45f8d300343c000f4eb9000083d432000240000ee8490241000e4a720000670000184a721000670000103632000035b2100000003583100051caffce4e75'),
    'selection_58_pool':(0x25338,'45f8d300303c000434d851c8fffc425a425a425a61ac45f8d300301ab078f74467f8b078f74667f2b078f74867ec32c04e75'),
    'selection_58_alias':(0x25F66,'41f9000ad86e3438f68a3602e34ad443e34ad443e54ad443e34a43f900ff2c00e548424316302000e74bef4b33830000424316302001e74bef4b33830002'),
    'rectangle_inclusive':(0x1E254,'3038f68ae74845f9000ae1b23232000034320002363200043832000645f8a15047f900ff3cc230186b2c0c40010064f63a00e54db272500062ecb472500065e6b672500262e0b872500265da'),
    'rectangle_strict':(0x1FD4A,'43f9000ae1b23438f68ae74ab671200063000020b671200264000018b871200463000010b871200664000008'),
    'center_reader':(0x22544,'41f9000ae2f63038f68ae54843f900ff2c003207e54934300000ee4a3382100034300002ee4a33821002'),
}


def check_anchors(rom):
    for name,(start,raw) in ANCHORS.items():
        if rom[start:start+len(raw)//2] != bytes.fromhex(raw):
            raise ValueError('original consumer anchor changed: '+name)


def verify_rom(rom):
    gb.af.verify_rom(rom)
    check_anchors(rom)


def record_id(family,number): return f'battlefield_{family}_{number:02d}'


def _group_words(record,groups):
    words=[]
    for key,shape in groups:
        if key=='leading_word':
            words.append(gb.rf.integer(record[key],65535,key))
        elif isinstance(shape,tuple):
            for row in gb.exact_list(record[key],shape[0],key):
                words.extend(gb.rf.integer(w,65535,key) for w in gb.exact_list(row,shape[1],key+' row'))
        else:
            words.extend(gb.rf.integer(w,65535,key) for w in gb.exact_list(record[key],shape,key))
    return words


def extract(rom):
    verify_rom(rom)
    assets={'schema_version':1,'format':FORMAT}
    for family,start,size,groups,_,_ in FAMILIES:
        records=[]
        for number in range(1,COUNT+1):
            words=list(struct.unpack_from(f'>{size//2}H',rom,start+(number-1)*size))
            record={'id':record_id(family,number),'map_id':number}; cursor=0
            for key,shape in groups:
                if key=='leading_word': record[key]=words[cursor]; cursor+=1
                elif isinstance(shape,tuple):
                    record[key]=[words[cursor+i*shape[1]:cursor+(i+1)*shape[1]] for i in range(shape[0])]
                    cursor+=shape[0]*shape[1]
                else: record[key]=words[cursor:cursor+shape]; cursor+=shape
            assert cursor==size//2
            records.append(record)
        assets[family]=records
    return assets


def blocks(rom,assets):
    verify_rom(rom)
    gb.af._keys(assets,{'schema_version','format'}|{f[0] for f in FAMILIES},'battlefield source')
    if type(assets['schema_version']) is not int or assets['schema_version']!=1 or assets['format']!=FORMAT:
        raise ValueError('fixed schema/format changed')
    result=[]
    for family,start,size,groups,_,_ in FAMILIES:
        for number,record in enumerate(gb.exact_list(assets[family],COUNT,family+' catalog'),1):
            gb.af._keys(record,{'id','map_id'}|{g[0] for g in groups},family+' record')
            if type(record['id']) is not str or record['id']!=record_id(family,number) or type(record['map_id']) is not int or record['map_id']!=number:
                raise ValueError('fixed record order/identity changed')
            data=struct.pack(f'>{size//2}H',*_group_words(record,groups)); address=start+(number-1)*size
            result.append({'id':record['id'],'start':address,'end':address+size,
                           'role':f'battlefield_{family}_words','data':data})
    return result


def rebuild(rom,assets):
    image=bytearray(rom)
    for row in blocks(rom,assets): image[row['start']:row['end']]=row['data']
    return bytes(image)


def _signed_word(value):
    value&=65535
    return value-65536 if value&0x8000 else value


def selection_alias_address(map_word):
    """Pure address arithmetic of 025F66, not a consumer/CPU execution model."""
    number=gb.rf.integer(map_word,65535,'full F68A word')
    return 0xAD86E+_signed_word(58*number)


def coordinate_a_point_address(map_word,point_byte):
    """025C02 arithmetic; point 0 and point >16 are deliberately not clamped."""
    number=gb.rf.integer(map_word,65535,'full F68A word')
    point=gb.rf.integer(point_byte,255,'point selector byte')
    return 0xABDA8+_signed_word(32*number+2*point)


def source_location(address):
    """Read-only physical locator; never another editable field representation."""
    for family,start,size,groups,_,_ in FAMILIES:
        if start<=address<start+COUNT*size:
            index,offset=divmod(address-start,size); word=offset//2; cursor=0
            for key,shape in groups:
                count=shape[0]*shape[1] if isinstance(shape,tuple) else shape
                if cursor<=word<cursor+count:
                    within=word-cursor
                    field=key if key=='leading_word' else (
                        f'{key}[{within//shape[1]}][{within%shape[1]}]' if isinstance(shape,tuple) else f'{key}[{within}]')
                    return {'family':family,'map_id':index+1,'record_id':record_id(family,index+1),
                            'field':field,'byte_lane':offset%2}
                cursor+=count
    return None


def _alias_rows(image):
    return [{'map_id':n,'address':selection_alias_address(n),
             'word':int.from_bytes(image[selection_alias_address(n):selection_alias_address(n)+2],'big'),
             'source':source_location(selection_alias_address(n))} for n in range(1,COUNT+1)]


def inspect(rom,assets):
    intervals=blocks(rom,assets); image=bytearray(rom)
    for row in intervals: image[row['start']:row['end']]=row['data']
    warnings=[]; families=[]
    for family,start,size,groups,confidence,evidence in FAMILIES:
        values=[word for r in assets[family] for word in _group_words(r,groups)]
        families.append({'id':family,'start':start,'end':start+COUNT*size,'record_size':size,
                         'record_count':COUNT,'sha256':sha(image[start:start+COUNT*size]),
                         'zero_words':values.count(0),'ffff_words':values.count(65535)})
        if family in ('coordinates_a','coordinates_b'):
            unusual=[{'map_id':n,'word_index':i,'word':word} for n,r in enumerate(assets[family],1)
                     for i,word in enumerate(r['words']) if word!=65535 and (word>>8>=28 or word&255>=40)]
            if unusual: warnings.append({'code':'coordinate_outside_canonical_grid','family':family,'fields':unusual,
                'meaning':'Full u16 source retained; no CPU point-domain or edited gameplay validity is inferred.'})
    geometry=[]; nonmid=[]
    for n,(rect,center) in enumerate(zip(assets['rectangles'],assets['centers']),1):
        a,b,c,d=rect['bounds_words']; x,y=center['center_words']
        if b-a!=0x1F00 or d-c!=0x1F00: geometry.append(n)
        if 2*x!=a+b or 2*y!=c+d: nonmid.append(n)
    if geometry: warnings.append({'code':'rectangle_differs_from_canonical_extent','map_ids':geometry,
        'meaning':'Canonical extents are 1F00; limits remain independent full-width source words.'})
    if nonmid: warnings.append({'code':'center_not_rectangle_midpoint','map_ids':nonmid,
        'meaning':'Midpoint is a canonical data relation, not a forced derivation or import constraint.'})
    return {'schema_version':1,'format':FORMAT,'canonical_exact':bytes(image)==rom,'sha256':sha(image),
            'changed_bytes':sum(a!=b for a,b in zip(image,rom)),'editable_bytes':EDITABLE_BYTES,
            'warning_policy':'report_only_no_normalization','warnings':warnings,'families':families,
            'selection_aliases':_alias_rows(image),'natural_selection_domain_complete':False,
            'edited_gameplay_validated':False}


def manifest(rom):
    assets=extract(rom); intervals=blocks(rom,assets); owners=[]
    for family,start,size,groups,confidence,evidence in FAMILIES:
        for row in intervals:
            if not start<=row['start']<start+COUNT*size: continue
            owners.append({k:row[k] for k in ('id','start','end','role')}|{
                'size':size,'confidence':confidence,'sha256':sha(row['data']),'evidence':list(evidence),
                'purpose_scope':'Full-width source words and conditional reader grouping; physical catalog is not natural selector coverage.',
                'unknown_components':['all-caller F68A domain','natural lifetime','edited gameplay validity']+
                    (['selection field business meaning','complete RNG/selection behavior'] if family.startswith('selection_') else [])})
    report=inspect(rom,assets)
    return {'schema_version':1,'format':FORMAT,'canonical_rom_sha256':sha(rom),
        'source_fields_sha256':sha(dump(assets)),'editable_bytes':EDITABLE_BYTES,'build_block_count':len(intervals),
        'confirmed_bytes':sum(r['size'] for r in owners if r['confidence']=='confirmed'),
        'probable_bytes':sum(r['size'] for r in owners if r['confidence']=='probable'),
        'owners':owners,'families':report['families'],'selection_aliases':report['selection_aliases'],
        'consumer_anchors':[{'id':name,'start':start,'end':start+len(raw)//2,'bytes':raw,
                             'sha256':sha(bytes.fromhex(raw))} for name,(start,raw) in ANCHORS.items()],
        'aliases':[
            {'id':'selection_pre_record_word','reader':'selection_58_alias','confidence':'confirmed',
             'formula':'0AD86E + signed16(u16(58 * F68A.w))',
             'meaning':'Two byte reads alias the word preceding each formal 58-byte record; map 1 aliases selection_108 map 40 tail_words[3].'},
            {'id':'coordinate_a_variable_point','reader':'coordinate_a_variable_alt','confidence':'confirmed',
             'formula':'0ABDA8 + signed16(u16(32 * F68A.w + 2 * zero_extended(point_byte)))',
             'meaning':'point_byte at FF9FFF + signed16(F68A.w); point 1 selects first formal word, point 0 is before the record; no point clamp.'},
            {'id':'center_biased_base','reader':'center_reader','confidence':'confirmed',
             'formula':'0AE2F6 + signed16(u16(F68A.w << 2))',
             'meaning':'Biased base lies in the last rectangle; physical centers start AE2FA. A selector-zero read is not a second source.'}],
        'existing_owner_overlap':{'start':0xAE1C2,'end':0xAE1CA,'size':8,
             'confidence':'confirmed','meaning':'Existing map-2 rectangle ownership; global integration must deduplicate these same physical fields.'},
        'natural_selection_domain_complete':False,'runtime_validation_added':False,
        'complete_indirect_domains_added':0,
        'boundaries':['Forty physical records per family are editor allocation, not CPU F68A clamping.',
            'All 16 bits of every source word are editable; FFFF and zero are not normalized.',
            'selection_108 special branch tests 0017 hexadecimal (decimal 23), not decimal 17.',
            'Selection source grouping and conditional reference union are confirmed; field business names remain candidate and complete behavior is not established by this codec.',
            'Original rectangle readers distinguish unsigned inclusive bounds and strict interior.',
            'Centers are independent words; canonical midpoint equality is a report-only relation.',
            'Preceding AACA8..ABDCA bytes and following portrait bytes are not owned or edited.',
            'Anchor spans identify original instructions, not new CPU primary ownership or complete instruction emulation.']}


def schema():
    word={'type':'integer','minimum':0,'maximum':65535}
    def array(length,item): return {'type':'array','minItems':length,'maxItems':length,'items':item}
    properties={'schema_version':{'type':'integer','const':1},'format':{'const':FORMAT}}
    for family,start,size,groups,confidence,evidence in FAMILIES:
        records=[]
        for n in range(1,COUNT+1):
            fields={'id':{'const':record_id(family,n)},'map_id':{'type':'integer','const':n}}
            for key,shape in groups:
                fields[key]=(word if key=='leading_word' else array(shape[0],array(shape[1],word))
                             if isinstance(shape,tuple) else array(shape,word))
            records.append({'type':'object','additionalProperties':False,'required':list(fields),'properties':fields})
        properties[family]={'type':'array','minItems':COUNT,'maxItems':COUNT,'items':False,'prefixItems':records}
    return {'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Full-width battlefield source',
        'type':'object','additionalProperties':False,'required':list(properties),'properties':properties,
        '$comment':'Runtime also rejects bool/float integers, duplicate JSON keys, nonfinite values. Fixed catalog and warning-only relations do not clamp original CPU inputs.'}


def render_bundle(rom):
    info=manifest(rom)
    report=('# Battlefield resource source fields\n\n'
        'confirmed: assets.json is the sole editable authority; all other files are derived.\n\n'
        '- confirmed: six adjacent allocations ABDCA..AE39A, 9,680 B, 240 physical records; full BE16 values round-trip exactly.\n'
        '- confirmed: coordinate arrays are 40 x 16 words each. A is copied in full; B first word is read as two bytes and remaining 15 words are copied.\n'
        '- confirmed: selection source grouping is 2 + 8x6 + 4 words, and 1 + 5 + 3 + 4x5 words.\n'
        '- confirmed: both selection tables have full conditional source-reference coverage; field business names remain candidate and this codec does not establish complete selection behavior.\n'
        '- confirmed: rectangles are four full words; one reader uses unsigned inclusive bounds, another strict interior.\n'
        '- confirmed: centers are two independent words. Canonical rectangles have 1F00 extents and centers equal midpoints; editing need not preserve either relation.\n'
        '- confirmed: the 025F66 read precedes the formal 58-byte record by two bytes. Map 1 aliases the preceding 108-byte table last word; map 2 aliases selection_58 map 1 last word.\n'
        '- confirmed: the A variable-byte reader uses ABDA8, not the full-copy biased base ABDAA; point 1 reaches the first physical word, point 0 does not.\n'
        '- confirmed: the selection_108 special branch uses F68A == 0x0017 (decimal 23), whose original header low bytes 03/25 select both tail pairs conditionally; other records copy all four tail words.\n'
        '- unknown: natural F68A/point domains, complete caller/IRQ lifetime and edited gameplay validity. The catalog never proves a CPU clamp.\n'
        f"- confirmed: this package currently exposes {info['confirmed_bytes']} confirmed-role bytes and {info['probable_bytes']} probable-role bytes; global ownership must deduplicate the existing 8-byte map-2 rectangle.\n"
        '- confirmed: no new runtime observation or complete indirect domain is claimed.\n')
    return {'assets.json':dump(extract(rom)),'schema.json':dump(schema()),
            'manifest.json':dump(info),'README.md':report.encode()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','verify','import'))
    parser.add_argument('--rom',type=Path,default=DEFAULT_ROM)
    parser.add_argument('--assets',type=Path,default=DEFAULT_ASSETS)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    read=lambda p:gb.af._read(gb.af.safe_path(p,regular_input=True),4*1024*1024)
    rom=read(args.rom); verify_rom(rom)
    if args.command=='export': bundle=render_bundle(rom); inputs=[args.rom]
    else:
        assets=gb.af.load_assets(read(args.assets)); report=inspect(rom,assets)
        if args.command=='verify': print(dump(report).decode(),end=''); return
        bundle={'rebuilt.bin':rebuild(rom,assets),'validation.json':dump(report)}; inputs=[args.rom,args.assets]
    if args.output is None: raise ValueError('--output required')
    print(gb.publish(bundle,args.output,inputs))


if __name__=='__main__': main()
