"""Fixed-layout, editable world coordinates, ordered candidates, terrain and masks.

Static consumer proofs are not proofs that all selectors arise naturally. Editor
limits are stated explicitly; raw lookup helpers deliberately retain CPU wrapping.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

from tools.audio_formats import audio_formats as af
from tools.world_map import world_map as wm

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = af.DEFAULT_ROM
DEFAULT_ASSETS = ROOT/'analysis/world_resources/generated/assets.json'
FORMAT = 'g5510_world_fixed_layout'
# Half-open linear BIN intervals. No address is supplied by editable JSON.
LAYOUT = (
    ('terrain_costs', 0x00670A, 0x006710, False),
    ('city_coordinates', 0x0D4ACA, 0x0D4B6A, False),
    ('city_availability', 0x0D4B6A, 0x0D4BE2, True),
    ('city_candidates', 0x0D4BE2, 0x0D4D22, False),
    ('point_coordinates', 0x0D4D22, 0x0D4D2F, True),
    ('point_availability', 0x0D4D2F, 0x0D4D41, True),
    ('terrain_codes', 0x0EE5F0, 0x0EFA30, False),
)
ANCHORS = {
    0x00078A: '4241030066000006524160f64e753038f364e348d078f36441f9000d4b6711f00000efb311f00001efb511f00002efb74e75',
    0x011F90: '424243f9000d4d22b0116600000ab2290001670000085449524260ec3002e348d04241f9000d4d2f11f00000efb311f00001efb511f00002efb708380000f3a4660000263038efb26100002031c1ef643038efb46100001431c1ef663038efb66100000831c1ef684e75',
    0x034314: '41f9000d4d22424418106b00005031c4f6409800640000044404b8026200003242451a28000131c5f6429a01640000044445d805b8026200001848e7e0804eb90000651c4cdf0107b478f64463000006548860b2027cfffe60000006007c00014e75',
    0x006562: '41f900ff000043f9000ee5f045fa019a4e71303c143f4241424212191432100030c251c8fff6',
    0x0065F4: '43f9000d4aca303c00273219e8493419e84a3602e74ad443e74ad441e34a31bc00ff20fe31bc00ff200051c8ffde4e75',
    0x031A74: '41f9000d4bda45f8ea37e748d0c03638f37643f8f42742413a3cffff424214186b1a',
    0x00D3CE: '41f8ef6443f8efb23238f3f0e3493430100036311000080000036600001853426a000006343c0002050367f2318210006000001652420c420003650000044242050367f031821000',
    0x00FC36: '3038f3a6e348d078f3a6d078f3f03238f3f0e34943f8ef6434311000524211820000',
}
EVIDENCE = {
    'terrain_costs': '00656E/00657E six-entry LUT indexed by static terrain; 0142BA/0142C2 second reader',
    'city_coordinates': '0065F4..006622: 40 BE16 x/y pairs; logical shifts by four; two grid footprint words',
    'city_availability': '000798..0007BA: signed word index from 3*one-based city; three low-byte writes to EFB3/5/7; D3CE..D416 quality-bit consumer',
    'city_candidates': '031A74..031AB4: biased base D4BDA+8*city; ordered byte stream ends on any signed-negative byte; fixed physical stride8',
    'point_coordinates': '034314..034374: six x/y pairs and negative x terminator; 011F98 exact-match search uses the same list WITHOUT a terminator check',
    'point_availability': '011FAC..011FC4: matched point index*3 at D4D2F, three low-byte writes; 012168..0121AC quality-bit consumer',
    'terrain_codes': '006568..006584: 0x1440 byte reads and zero-extended BE16 LUT writes to FF0000',
}


def sha(data): return hashlib.sha256(data).hexdigest()
def dump(value): return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode()
def integer(value, maximum, name, minimum=0):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f'{name}: strict integer outside {minimum}..{maximum}')
    return value
def keys(value, expected):
    if type(value) is not dict or set(value) != set(expected): raise ValueError('object fields changed')
def sequence(value, count):
    if type(value) is not list or len(value) != count: raise ValueError('fixed sequence length changed')
def s16(value): return value if value < 0x8000 else value-0x10000


def check_anchors(rom):
    for address, raw in ANCHORS.items():
        if rom[address:address+len(raw)//2] != bytes.fromhex(raw):
            raise ValueError(f'consumer instruction changed at {address:06X}')


def city_mask_address(city_word):
    """000798 arithmetic; no CPU check that city is in the editor catalog 1..40."""
    integer(city_word, 65535, 'city register low word')
    return 0x0D4B67+s16((3*city_word)&65535)


def merge_mask_bytes(previous_words, source_bytes):
    """MOVE.B into EFB3/5/7 preserves the high byte of EFB2/4/6."""
    sequence(previous_words, 3); sequence(source_bytes, 3)
    return [(integer(old, 65535, 'previous mask')&0xFF00)|integer(new, 255, 'source mask')
            for old, new in zip(previous_words, source_bytes)]


def lowest_set_bit_raw(d0):
    """00078A: dynamic register BTST tests bit D1 modulo32, starting at low word0.

    Input is the entire D0, not an imagined zero-extended mask word. MOVE.W into
    D0 preserves its old high word. A zero D0 never returns (BTST repeats forever).
    """
    integer(d0, 0xFFFFFFFF, 'D0')
    return None if d0 == 0 else (d0 & -d0).bit_length()-1


def scan_signed_bytes(memory, start, max_reads):
    """Raw ordered-candidate termination. External budget, NOT a CPU stride bound."""
    integer(start, 0xFFFFFF, 'address'); integer(max_reads, 0x1000000, 'budget', 1)
    values=[]
    for offset in range(max_reads):
        address=(start+offset)&0xFFFFFF
        if address >= len(memory): return {'stop':'outside_supplied_memory', 'values':values, 'address':address}
        value=memory[address]
        if value&0x80: return {'stop':'negative_byte', 'values':values, 'address':address, 'terminator':value}
        values.append(value)
    return {'stop':'external_budget', 'values':values, 'address':(start+max_reads)&0xFFFFFF}


def find_point_raw(memory, x, y, max_pairs=64):
    """011F98 exact pair search; deliberately does NOT stop at the FF sentinel.

    Only supplied mapped ROM is read; a budget exhaustion is unknown, not an
    original-code failure return. D2.W and the index*3 both wrap at 16 bits.
    """
    integer(x, 255, 'x'); integer(y, 255, 'y'); integer(max_pairs, 0x800000, 'budget', 1)
    for count in range(max_pairs):
        address=(0x0D4D22+2*count)&0xFFFFFF
        if address+1 >= len(memory): return {'stop':'outside_supplied_memory', 'pairs_read':count}
        if memory[address]==x and memory[address+1]==y:
            index=count&65535
            return {'stop':'match', 'index_word':index, 'pairs_read':count+1,
                    'mask_address':0x0D4D2F+s16((3*index)&65535)}
    return {'stop':'external_budget', 'pairs_read':max_pairs}


def scan_points_raw(memory, max_pairs=64):
    """03431A/034334 list framing only; NOT the intervening route/geometry code.

    Test x's sign before reading y. Budget is external; no six-entry CPU clamp.
    """
    integer(max_pairs,0x800000,'budget',1); points=[]
    for index in range(max_pairs):
        address=(0x0D4D22+2*index)&0xFFFFFF
        if address>=len(memory): return {'stop':'outside_supplied_memory','points':points}
        x=memory[address]
        if x&128: return {'stop':'negative_x','points':points,'address':address,'terminator':x}
        if address+1>=len(memory): return {'stop':'outside_supplied_memory','points':points}
        points.append([x,memory[address+1]])
    return {'stop':'external_budget','points':points}


def extract(rom):
    af.verify_rom(rom); check_anchors(rom)
    cities=[]
    for i in range(40):
        c=0x0D4ACA+4*i; n=0x0D4BE2+8*i
        row=rom[n:n+8]; stop=next((j for j,b in enumerate(row) if b&128), None)
        if stop is None: raise ValueError('canonical candidate record has no local terminator')
        cities.append({'id':i+1, 'x_fixed16':int.from_bytes(rom[c:c+2],'big'),
            'y_fixed16':int.from_bytes(rom[c+2:c+4],'big'),
            'availability':list(rom[0x0D4B6A+3*i:0x0D4B6D+3*i]),
            'candidates':list(row[:stop]), 'terminator':row[stop], 'padding':list(row[stop+1:])})
    points=[{'index':i, 'x':rom[0x0D4D22+2*i], 'y':rom[0x0D4D23+2*i],
             'availability':list(rom[0x0D4D2F+3*i:0x0D4D32+3*i])} for i in range(6)]
    assets={'schema_version':1, 'format':FORMAT, 'canonical_rom_sha256':af.ROM_SHA256,
            'terrain_costs':list(rom[0x00670A:0x006710]),
            'terrain_rows':[list(rom[0x0EE5F0+72*i:0x0EE638+72*i]) for i in range(72)],
            'cities':cities, 'points':points, 'point_terminator':rom[0x0D4D2E]}
    _encode(assets)
    return assets


def _encode(assets):
    keys(assets, ('schema_version','format','canonical_rom_sha256','terrain_costs',
                  'terrain_rows','cities','points','point_terminator'))
    if type(assets['schema_version']) is not int or assets['schema_version']!=1 or assets['format']!=FORMAT:
        raise ValueError('asset format changed')
    if assets['canonical_rom_sha256']!=af.ROM_SHA256: raise ValueError('source identity changed')
    sequence(assets['terrain_costs'],6); sequence(assets['terrain_rows'],72)
    result={'terrain_costs':bytes(integer(v,255,'cost') for v in assets['terrain_costs'])}
    terrain=bytearray()
    for row in assets['terrain_rows']:
        sequence(row,72); terrain.extend(integer(v,5,'terrain code') for v in row)
    result['terrain_codes']=bytes(terrain)
    sequence(assets['cities'],40); coords=bytearray(); masks=bytearray(); candidates=bytearray()
    for index,row in enumerate(assets['cities'],1):
        keys(row, ('id','x_fixed16','y_fixed16','availability','candidates','terminator','padding'))
        if integer(row['id'],40,'city id',1)!=index: raise ValueError('fixed city order changed')
        coords.extend(integer(row['x_fixed16'],65535,'city x').to_bytes(2,'big'))
        coords.extend(integer(row['y_fixed16'],65535,'city y').to_bytes(2,'big'))
        sequence(row['availability'],3); masks.extend(integer(v,255,'mask') for v in row['availability'])
        if type(row['candidates']) is not list or len(row['candidates'])>7: raise ValueError('candidate capacity changed')
        # IDs1..40 are an explicit editor safety policy. Duplicates/self references
        # are representable and preserved; the CPU does not reject them.
        candidates.extend(integer(v,40,'candidate id',1) for v in row['candidates'])
        candidates.append(integer(row['terminator'],255,'negative terminator',128))
        sequence(row['padding'],7-len(row['candidates']))
        candidates.extend(integer(v,255,'unread padding byte') for v in row['padding'])
    # Explicit editor footprint policy; raw CPU code has no such range check.
    wm.parse_city_coordinates(bytes(coords))
    result.update(city_coordinates=bytes(coords),city_availability=bytes(masks),city_candidates=bytes(candidates))
    sequence(assets['points'],6); coords=bytearray(); masks=bytearray()
    for index,row in enumerate(assets['points']):
        keys(row, ('index','x','y','availability'))
        if integer(row['index'],5,'point index')!=index: raise ValueError('fixed point order changed')
        # A high-bit x would prematurely terminate the scan. The y reader does
        # not test its sign; accepting all byte values is not a route guarantee.
        coords.extend((integer(row['x'],127,'point x'),integer(row['y'],255,'point y')))
        sequence(row['availability'],3); masks.extend(integer(v,255,'mask') for v in row['availability'])
    coords.append(integer(assets['point_terminator'],255,'negative point terminator',128))
    result.update(point_coordinates=bytes(coords),point_availability=bytes(masks))
    return result


def blocks(rom, assets):
    af.verify_rom(rom); check_anchors(rom); payloads=_encode(assets); result=[]
    for name,start,end,new in LAYOUT:
        data=payloads[name]
        if len(data)!=end-start: raise ValueError('encoded extent changed')
        result.append({'id':name,'role':name,'start':start,'end':end,'data':data})
    if any(a['end']>b['start'] for a,b in zip(result,result[1:])): raise ValueError('overlapping fixed fields')
    return result


def rebuild(rom, assets):
    result=bytearray(rom)
    for row in blocks(rom,assets): result[row['start']:row['end']]=row['data']
    return bytes(result)


def warnings(assets):
    _encode(assets)
    result=['Structural editing does not prove route reachability, natural selector bounds or edited gameplay correctness.',
            '011F98 exact-point search has no sentinel check; unmatched coordinates may read subsequent resources indefinitely.',
            'Mask byte loads preserve pre-existing high mask bytes and MOVE.W into D0 preserves its high word.']
    for kind in ('cities','points'):
        for i,row in enumerate(assets[kind]):
            for category,mask in enumerate(row['availability']):
                if not mask&7: result.append(f'{kind}[{i}] category{category}: no quality0..2 bit; ordinary quality cycling can fail to terminate.')
    if 0 in assets['terrain_costs']: result.append('Zero terrain cost takes 256 decrement ticks, not zero ticks.')
    if any(p['x']>=72 or p['y']>=72 for p in assets['points']):
        result.append('A point is outside the nominal72x72 grid; raw byte coordinates remain representable.')
    return result


def manifest(rom, assets):
    rows=blocks(rom,assets)
    if rebuild(rom,assets)!=rom: raise ValueError('evidence manifest requires canonical field values')
    return {'schema_version':1,'canonical_source':{'size':len(rom),'sha256':sha(rom)},
        'asset_sha256':sha(dump(assets)), 'editable_bytes':5821, 'previously_owned_bytes':5670,
        'proposed_new_owner_bytes':151, 'owner_count':7,
        'natural_selection_domain_complete':False,'complete_indirect_domains_added':0,
        'runtime_validation_added':False,'confidence':'confirmed_static_consumer_and_physical_partition',
        'counts':{'cities':40,'directed_candidate_entries':sum(len(c['candidates']) for c in assets['cities']),
                  'points':6,'categories':3,'terrain_cells':5184,'terrain_costs':6},
        'unknowns':['Equipment category and quality display names are not assigned here.',
                    'Candidate padding is preserved, not interpreted as additional edges.',
                    'All natural city/point selectors and mask high-byte lifetimes remain unproved.',
                    'No route termination guarantee; static resource sizes are not CPU bounds.'],
        'owners':[{'id':r['id'],'start':r['start'],'end':r['end'],'size':len(r['data']),
                   'sha256':sha(r['data']),'status':'confirmed','evidence':EVIDENCE[r['id']],
                   'previously_owned':not new} for r,(_,_,_,new) in zip(rows,LAYOUT)],
        'consumer_anchors':[{'start':a,'end':a+len(raw)//2,'bytes':raw,'ownership':False}
                            for a,raw in sorted(ANCHORS.items())],
        'warnings':warnings(assets)}


def render_bundle(rom):
    from tools.world_resources.schema import asset_schema
    assets=extract(rom); info=manifest(rom,assets)
    report=['# Typed world resource evidence','',
        'Status: confirmed static consumer/partition; no new runtime or natural-domain proof.','',
        'Seven disjoint regions / 5821 B; 5670 B already owned, 151 B newly proposed static ownership.','',
        '| Resource | Half-open BIN interval | Bytes | Existing owner |',
        '| --- | --- | ---: | --- |']
    for row in info['owners']:
        report.append(f"| {row['id']} | {row['start']:06X}..{row['end']:06X} | {row['size']} | {row['previously_owned']} |")
    report+=['','The sole editable authority is assets.json; schema and manifest are evidence, not editable payload seals.',
        'All seven regions are encoded from typed fields. No source BIN or raw ROM slice is used as a build payload.',
        'City coordinates are BE16 fixed/16. Candidate order, signed terminator aliases and unread padding are lossless.',
        'City masks are three bytes indexed by one-based city; six point masks follow a six-pair coordinate list.',
        '034314 scans until ANY negative x; 011F98 exact-match search ignores that terminator entirely.',
        '00078A scans a full32-bit register; zero never returns, and surviving high bits are not discarded.',
        'The editor allows zero masks and all mask bits; warnings are not invented CPU rejections.',
        'Terrain codes0..5 and city footprint bounds are editor constraints. Costs retain all256 byte patterns.',
        'No geographical label, category name, global initialization or route-termination proof is inferred.','']
    validation={'schema_version':1,'canonical_roundtrip_exact':rebuild(rom,assets)==rom,
        'encoded_bytes':sum(r['end']-r['start'] for r in blocks(rom,assets)),
        'region_count':7,'source_sha256':sha(rom),'manifest_sha256':sha(dump(info)),
        'anchor_range_count':len(ANCHORS),'anchor_bytes':sum(len(s)//2 for s in ANCHORS.values()),
        'canonical_point_searches':[find_point_raw(rom,p['x'],p['y'],6) for p in assets['points']],
        'canonical_city_masks_nonzero_low_three_bits':all(v&7 for c in assets['cities'] for v in c['availability']),
        'natural_selection':False}
    return {'assets.json':dump(assets),'assets.schema.json':dump(asset_schema()),'manifest.json':dump(info),
            'validation.json':dump(validation),'README.md':('\n'.join(report)).encode()}


def export_files(rom_path, output):
    source=af.safe_path(rom_path,regular_input=True); target=af.safe_path(output)
    af._separate(target,[source])
    if target.exists() or not target.parent.is_dir(): raise ValueError('fresh output directory with existing parent required')
    bundle=render_bundle(af._read(source,af.ROM_SIZE))
    staging=Path(tempfile.mkdtemp(prefix='.world-resources-',dir=target.parent)); identity=staging.stat(); produced={}
    target_identity=None; linked={}; published=False
    try:
        for name,data in bundle.items():
            with (staging/name).open('xb') as stream: stream.write(data)
            produced[name]=data
        af.safe_path(output)
        # An exclusive mkdir refuses even an empty concurrently created target.
        # POSIX rename would replace that empty directory. Each complete prepared
        # file is published without clobbering; the directory is visible while
        # links are added. Only successful return promises a complete bundle.
        target.mkdir(); target_identity=target.stat()
        for name,data in bundle.items():
            af.safe_path(target); current=target.stat()
            if (current.st_dev,current.st_ino)!=(target_identity.st_dev,target_identity.st_ino):
                raise ValueError('output directory identity changed during publication')
            os.link(staging/name,target/name); linked[name]=data
        published=True
    finally:
        try:
            if target_identity is not None and not published:
                af._cleanup_stage(target,linked,target_identity)
        finally: af._cleanup_stage(staging,produced,identity)
    return {'output':str(target),'files':sorted(bundle)}


def import_files(rom_path, asset_path, output):
    source=af.safe_path(rom_path,regular_input=True); asset=af.safe_path(asset_path,regular_input=True)
    target=af.safe_path(output); af._separate(target,[source,asset])
    if target.exists() or not target.parent.is_dir(): raise ValueError('fresh output file with existing parent required')
    rom=af._read(source,af.ROM_SIZE); assets=af.load_assets(af._read(asset,8*1024*1024)); result=rebuild(rom,assets)
    descriptor,name=tempfile.mkstemp(prefix='.world-resources-',dir=target.parent)
    temporary=Path(name); identity=temporary.stat(); complete=False
    try:
        with os.fdopen(descriptor,'wb') as stream:
            stream.write(result); stream.flush(); os.fsync(stream.fileno())
        complete=True; af.safe_path(output); os.link(temporary,target)
    finally:
        if temporary.exists():
            af.safe_path(temporary,regular_input=True); current=temporary.stat()
            if complete and (current.st_dev,current.st_ino)==(identity.st_dev,identity.st_ino) and af._read(temporary,len(result))==result:
                temporary.unlink()
            else: raise ValueError('incomplete/modified temporary file retained for inspection')
    return {'output':str(target),'sha256':sha(result),'canonical_exact':result==rom,
            'changed_bytes':sum(a!=b for a,b in zip(rom,result)),'warnings':warnings(assets)}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',type=Path,default=DEFAULT_ROM)
    parser.add_argument('--assets',type=Path,default=DEFAULT_ASSETS)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args(argv)
    try:
        if args.command in ('export','import'):
            if args.output is None: raise ValueError('--output required')
            result=export_files(args.rom,args.output) if args.command=='export' else import_files(args.rom,args.assets,args.output)
        else:
            rom=af._read(af.safe_path(args.rom,regular_input=True),af.ROM_SIZE)
            assets=af.load_assets(af._read(af.safe_path(args.assets,regular_input=True),8*1024*1024))
            rebuilt=rebuild(rom,assets)
            result={'canonical_exact':rebuilt==rom,'sha256':sha(rebuilt),'editable_bytes':5821,'warnings':warnings(assets)}
    except (ValueError,OSError) as error: parser.exit(2,f'world_resources: {error}\n')
    print(json.dumps(result,ensure_ascii=False,indent=2)); return 0


if __name__=='__main__': raise SystemExit(main())
