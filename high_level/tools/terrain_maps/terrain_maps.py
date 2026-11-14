"""Forty full-width BE16 maps and the biased 512-byte terrain type allocation.

Fixed editor allocation is not a CPU clamp. Every u16 map word and u8 type value
is accepted; cross-allocation/type-domain inconsistencies are reported, not fixed.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import groupby
from pathlib import Path
import struct
import zlib

from tools.graphics_build import graphics_build as gb

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = ROOT.parent/'work/original_g5510.bin'
DEFAULT_ASSETS = ROOT/'analysis/terrain_maps/generated/assets.json'
FORMAT = 'g5510-full-width-terrain-maps-v1'
MAP_BIAS = 0x945E8
MAP_START, MAP_END = 0x94EA8, 0xAACA8
MAP_COUNT, ROWS, COLUMNS, MAP_SIZE = 40, 28, 40, 0x8C0
TYPE_BIAS, TYPE_START, TYPE_END = 0x6C0B4, 0x6C1B4, 0x6C3B4
TYPE_COUNT = TYPE_END-TYPE_START
EDITABLE_BYTES = MAP_END-MAP_START+TYPE_COUNT
sha, dump = gb.sha, gb.dump
ANCHORS = {
    'full_map_reader':(0x17776,'243c5000000341f9000945e83038f68ac0fc08c0d1c0323c001b23c200c00004303c0027361808030008670000060043070033c300c0000051c8ffea06820080000051c9ffd64e75'),
    'map_base_and_type_reader':(0x1A438,'2f0441f9000945e83838f68ac8fc08c0d1c4281f4e7548e77080e6493601e549d243e749e64ad242e34930301000024003ff41f90006c0b4103000004cdf010e4e75'),
    'left_type_boundary':(0x178C8,'43f90006c174363c' '000f23d900c0000051cbfff8'),
    'right_type_boundary':(0x26EA0,'41f90006c3b44df900c00000303c2fff2c9851c8fffc'),
    'pair_terrain_selector':(0x1F886,'4eb90001a43843f8a1503638f702e54b3838f706e54c32313000ee4930314000ee48d240e24934313002ee4a30314002ee48d440e24a4eb90001a44e024000ff103b00044e750003020102020200'),
    'alternate_type_reader':(0x1E04E,'2f043838f68ac8fc08c04bf9000945e8dbc4281f3801ee4c024400f83a04e54cd8453a02ee4de64dd845e34c3a354000024503ff4bf90006c0b41a355000024500ff3805e34d3a3b50084ebb50144e75'),
}


def check_anchors(rom):
    for name,(start,raw) in ANCHORS.items():
        if rom[start:start+len(raw)//2] != bytes.fromhex(raw):
            raise ValueError('original consumer/boundary anchor changed: '+name)


def verify_rom(rom):
    gb.af.verify_rom(rom)
    check_anchors(rom)


def map_id(number): return f'terrain_map_{number:02d}'


def extract(rom):
    verify_rom(rom)
    maps=[]
    for number in range(1,MAP_COUNT+1):
        start=MAP_BIAS+number*MAP_SIZE
        words=struct.unpack_from('>1120H',rom,start)
        maps.append({'id':map_id(number),'map_id':number,
                     'rows':[list(words[y*COLUMNS:(y+1)*COLUMNS]) for y in range(ROWS)]})
    return {'schema_version':1,'format':FORMAT,'maps':maps,
            'type_values':list(rom[TYPE_START:TYPE_END])}


def blocks(rom,assets):
    verify_rom(rom)
    gb.af._keys(assets,{'schema_version','format','maps','type_values'},'terrain source')
    if type(assets['schema_version']) is not int or assets['schema_version']!=1 or assets['format']!=FORMAT:
        raise ValueError('fixed schema/format changed')
    types=bytes(gb.rf.integer(v,255,'type byte') for v in gb.exact_list(assets['type_values'],TYPE_COUNT,'type allocation'))
    result=[{'id':'terrain_types','start':TYPE_START,'end':TYPE_END,'role':'terrain_type_bytes','data':types}]
    for number,record in enumerate(gb.exact_list(assets['maps'],MAP_COUNT,'map catalog'),1):
        gb.af._keys(record,{'id','map_id','rows'},'map source')
        if type(record['id']) is not str or record['id']!=map_id(number) or type(record['map_id']) is not int or record['map_id']!=number:
            raise ValueError('fixed map order/identity changed')
        words=[]
        for row in gb.exact_list(record['rows'],ROWS,'map rows'):
            words.extend(gb.rf.integer(w,65535,'full map word') for w in gb.exact_list(row,COLUMNS,'map columns'))
        start=MAP_BIAS+number*MAP_SIZE
        result.append({'id':record['id'],'start':start,'end':start+MAP_SIZE,
                       'role':'terrain_map_words','data':struct.pack('>1120H',*words)})
    return result


def rebuild(rom,assets):
    result=bytearray(rom)
    for row in blocks(rom,assets): result[row['start']:row['end']]=row['data']
    return bytes(result)


def canonical_usage(rom):
    """Static references from all physical maps, not natural execution counts."""
    verify_rom(rom)
    return Counter(w&0x3FF for w in struct.unpack_from('>44800H',rom,MAP_START))


def inspect(rom,assets):
    """Report-only relation checks; no value, high bit or reference is normalized.

    Outside-allocation lookup bytes are disclosed original-ROM bytes. They are
    not silently supplied by type_values, clamped, or classified as owned data.
    """
    intervals=blocks(rom,assets); image=bytearray(rom)
    for row in intervals: image[row['start']:row['end']]=row['data']
    summaries=[]; outside=Counter(); bad_types=Counter(); high_changed=0
    for interval in intervals[1:]:
        words=struct.unpack('>1120H',interval['data']); indices=Counter(w&0x3FF for w in words)
        type_counts=Counter()
        for index,count in indices.items():
            address=TYPE_BIAS+index; value=image[address]; type_counts[value]+=count
            if not TYPE_START<=address<TYPE_END: outside[index]+=count
            if value>7: bad_types[value]+=count
        high_changed+=sum((word&0xFC00)!=0x2000 for word in words)
        summaries.append({'id':interval['id'],'map_id':int(interval['id'][-2:]),
            'start':interval['start'],'end':interval['end'],'rows':ROWS,'columns':COLUMNS,
            'sha256':sha(interval['data']),'used_type_indices':sorted(indices),
            'type_counts':{f'{k:02X}':v for k,v in sorted(type_counts.items())}})
    warnings=[]
    if outside: warnings.append({'code':'type_lookup_outside_allocation','word_count':sum(outside.values()),
        'indices':sorted(outside),'meaning':'CPU lookup is not clamped; these bytes are outside the editable type allocation.'})
    if bad_types: warnings.append({'code':'referenced_type_outside_eight_entry_mapping',
        'word_count':sum(bad_types.values()),'values':sorted(bad_types),
        'meaning':'A downstream byte-indexed eight-entry mapping is not proved safe for these values.'})
    if high_changed: warnings.append({'code':'map_high_bits_differ_from_canonical','word_count':high_changed,
        'meaning':'All full u16 values are allowed; high bits are preserved and their edited display behavior is not validated.'})
    unusual=[i+0x100 for i,v in enumerate(assets['type_values']) if v>7 and v!=255]
    if unusual: warnings.append({'code':'type_values_outside_canonical_value_set','indices':unusual,
        'meaning':'Complete u8 values remain editable; this allocation originally contained only 0..7 and FF.'})
    selected=canonical_usage(rom)
    unselected_edits=[i+0x100 for i,v in enumerate(assets['type_values'])
                      if i+0x100 not in selected and v!=rom[TYPE_START+i]]
    if unselected_edits: warnings.append({'code':'canonical_unselected_type_entries_edited','indices':unselected_edits,
        'meaning':'Editing an unselected allocation does not promote its canonical ownership confidence.'})
    return {'schema_version':1,'format':FORMAT,'canonical_exact':bytes(image)==rom,'sha256':sha(image),
            'changed_bytes':sum(a!=b for a,b in zip(image,rom)),'editable_bytes':EDITABLE_BYTES,
            'warning_policy':'report_only_no_normalization','warnings':warnings,'maps':summaries,
            'natural_selection_domain_complete':False,'edited_gameplay_validated':False}


def manifest(rom):
    assets=extract(rom); intervals=blocks(rom,assets); usage=canonical_usage(rom); owners=[]
    # Confidence runs are sealed from canonical references, not editable values.
    for selected,items in groupby(range(TYPE_COUNT),key=lambda n:n+0x100 in usage):
        run=list(items); start=TYPE_START+run[0]; end=TYPE_START+run[-1]+1
        owners.append({'id':f'terrain_type_{run[0]+0x100:04X}_{run[-1]+0x101:04X}',
            'start':start,'end':end,'size':end-start,'role':'terrain_type_bytes',
            'confidence':'confirmed' if selected else 'probable','sha256':sha(rom[start:end]),
            'static_reference_count':sum(usage[n+0x100] for n in run),
            'evidence':['map_base_and_type_reader','left_type_boundary','right_type_boundary']})
    for row in intervals[1:]:
        owners.append({k:row[k] for k in ('id','start','end','role')}|
            {'size':row['end']-row['start'],'confidence':'confirmed','sha256':sha(row['data']),
             'evidence':['full_map_reader','map_base_and_type_reader']})
    confirmed=sum(row['size'] for row in owners if row['confidence']=='confirmed')
    return {'schema_version':1,'format':FORMAT,'canonical_rom_sha256':sha(rom),
        'source_fields_sha256':sha(dump(assets)),'editable_bytes':EDITABLE_BYTES,'build_block_count':len(intervals),
        'confirmed_bytes':confirmed,'probable_bytes':EDITABLE_BYTES-confirmed,
        'map_source_bytes':MAP_END-MAP_START,'selected_type_bytes':len(usage),
        'unselected_type_bytes':TYPE_COUNT-len(usage),'owners':owners,
        'maps':inspect(rom,assets)['maps'],
        'type_allocation':{'id':'terrain_types','start':TYPE_START,'end':TYPE_END,'size':TYPE_COUNT,
            'confidence':'probable','biased_base':TYPE_BIAS,'first_index':0x100,'last_index':0x2FF,
            'sha256':sha(rom[TYPE_START:TYPE_END]),'static_selected_indices':sorted(usage),
            'canonical_ff_entries':assets['type_values'].count(255),
            'reference_counts':[usage[n+0x100] for n in range(TYPE_COUNT)],
            'meaning':'Whole allocation shape probable; individual referenced runs carry confirmed relationships.'},
        'consumer_anchors':[{'id':name,'start':start,'end':start+len(raw)//2,
                             'bytes':raw,'sha256':sha(bytes.fromhex(raw))}
                            for name,(start,raw) in ANCHORS.items()],
        'natural_selection_domain_complete':False,'runtime_validation_added':False,
        'complete_indirect_domains_added':0,
        'boundaries':['physical map catalog IDs 1..40 are editor allocation, not a CPU F68A clamp',
            'all 16 map bits and all 8 type bits are authoritative; no inferred palette normalization',
            '394 distinct type bytes are statically referenced, not naturally exercised by this package',
            '118 unselected type bytes remain probable; FF meaning and their natural use are unknown',
            'biased map slot0 overlaps unrelated text/pixels; slot41 begins unrelated fields',
            'valid map ID does not prove coordinate bounds, interrupt lifetime or downstream type-index validity']}


def schema():
    return {'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Full-width terrain map source',
        'type':'object','additionalProperties':False,'required':['schema_version','format','maps','type_values'],
        'properties':{'schema_version':{'const':1,'type':'integer'},'format':{'const':FORMAT},
            'type_values':{'type':'array','minItems':512,'maxItems':512,'items':{'type':'integer','minimum':0,'maximum':255}},
            'maps':{'type':'array','minItems':40,'maxItems':40,'items':False,
                'prefixItems':[{'type':'object','additionalProperties':False,'required':['id','map_id','rows'],
                    'properties':{'id':{'const':map_id(n)},'map_id':{'const':n,'type':'integer'},
                                  'rows':{'$ref':'#/$defs/rows'}}} for n in range(1,41)]}},
        '$defs':{'rows':{'type':'array','minItems':28,'maxItems':28,'items':{
            'type':'array','minItems':40,'maxItems':40,'items':{'type':'integer','minimum':0,'maximum':65535}}}},
        '$comment':'Runtime validation also rejects booleans/floats as integers, duplicate JSON keys, and non-finite values. Relation warnings never normalize source fields.'}


def render_bundle(rom):
    info=manifest(rom)
    report=('# Full-width terrain maps and biased type allocation\n\n'
        'assets.json is the sole editable authority; schema/manifest/report are derived.\n\n'
        '- 40 maps, each 28 rows x 40 BE16 words; IDs 1..40 occupy 094EA8..0AACA8 (89,600 B).\n'
        '- Complete 512-byte type allocation occupies 06C1B4..06C3B4; biased base is 06C0B4.\n'
        '- 90,112 editable bytes / 41 build blocks.\n'
        f"- {info['confirmed_bytes']:,} confirmed bytes: 89,600 map bytes and 394 statically referenced type bytes.\n"
        '- 118 unselected type bytes remain probable, including retained FF entries.\n'
        '- All u16/u8 field values may be edited; inconsistencies generate warnings, not silent repairs.\n'
        '- Static full-catalog enumeration is not natural selection, coordinate or IRQ-lifetime closure.\n'
        '- No runtime validation or complete indirect domain is added by this package.\n')
    return {'assets.json':dump(extract(rom)),'schema.json':dump(schema()),
            'manifest.json':dump(info),'README.md':report.encode()}


TYPE_COLOURS = ((30,30,30),(60,130,60),(200,190,110),(70,120,190),
                (170,100,60),(190,70,70),(160,100,190),(70,190,190))


def preview(rom,assets):
    """40x28 categorical diagrams, one square per source word; NOT game pixels."""
    report=inspect(rom,assets); image=rebuild(rom,assets); bundle={}
    for record in assets['maps']:
        pixels=[]
        for row in record['rows']:
            line=bytearray()
            for word in row:
                value=image[TYPE_BIAS+(word&0x3FF)]
                line.extend(TYPE_COLOURS[value] if value<8 else (255,0,255))
            pixels.append(b'\0'+bytes(line))
        bundle[record['id']+'.png']=(b'\x89PNG\r\n\x1a\n'+
            gb.title.png_chunk(b'IHDR',struct.pack('>IIBBBBB',40,28,8,2,0,0,0))+
            gb.title.png_chunk(b'IDAT',zlib.compress(b''.join(pixels),9))+gb.title.png_chunk(b'IEND',b''))
    bundle['preview.json']=dump({'representation':'categorical type diagram; not original pixels or palette',
        'legend':{f'{i:02X}':list(rgb) for i,rgb in enumerate(TYPE_COLOURS)},
        'other_type_colour':[255,0,255],'source_fields_sha256':sha(dump(assets)),
        'warnings':report['warnings'],'editable_authority':False})
    return bundle


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','verify','import','preview'))
    parser.add_argument('--rom',type=Path,default=DEFAULT_ROM)
    parser.add_argument('--assets',type=Path,default=DEFAULT_ASSETS)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    read=lambda p:gb.af._read(gb.af.safe_path(p,regular_input=True),4*1024*1024)
    rom=read(args.rom); verify_rom(rom)
    if args.command=='export': bundle=render_bundle(rom); inputs=[args.rom]
    else:
        assets=gb.af.load_assets(read(args.assets)); info=inspect(rom,assets)
        if args.command=='verify': print(dump(info).decode(),end=''); return
        bundle=preview(rom,assets) if args.command=='preview' else {
            'rebuilt.bin':rebuild(rom,assets),'validation.json':dump(info)}
        inputs=[args.rom,args.assets]
    if args.output is None: raise ValueError('--output required')
    print(gb.publish(bundle,args.output,inputs))


if __name__=='__main__': main()
