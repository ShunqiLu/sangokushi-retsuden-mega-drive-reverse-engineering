"""Thirteen word-RLE streams and two four-pointer map catalogs.

The physical grammar includes marker/zero tails. The 03AACE map consumer exits
at 1024 words BEFORE those tails, even in the middle of a repeated run. Static
catalog membership is not a proof of a global FF80DB selector domain.
"""
from __future__ import annotations
import argparse
import copy
from dataclasses import dataclass
from pathlib import Path
import struct
import zlib

from tools.graphics_build import graphics_build as g
from tools.graphics_build import rle_fields as rf

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = g.DEFAULT_ROM
DEFAULT_ASSETS = ROOT/'analysis/battle_graphics/generated/assets.json'
FORMAT = 'g5510-battle-mode-word-rle-v1'


@dataclass(frozen=True)
class Stream:
    id: str
    start: int
    end: int
    order: str
    words: int
    call: int | None
    vram: int | None


STREAMS = (
    Stream('tiles_0',0x473E4,0x492E7,'little',4096,0x3DA12,0x0000),
    Stream('tiles_1',0x492E8,0x4A9A1,'little',4096,0x3DA20,0x2000),
    Stream('tiles_2',0x4A9A2,0x4C5AB,'little',4096,0x3DA2E,0x4000),
    Stream('tiles_3',0x4C5AC,0x4E08F,'little',4096,0x3DA3C,0x6000),
    Stream('tiles_4',0x4E090,0x4FBE3,'little',4096,0x3DA4A,0x8000),
    Stream('map_a_0',0x41FF0,0x427F1,'big',1024,None,None),
    Stream('map_a_1',0x42AF4,0x432F7,'big',1024,None,None),
    Stream('map_a_2',0x4357A,0x43D67,'big',1024,None,None),
    Stream('map_a_3',0x43FE6,0x447E9,'big',1024,None,None),
    Stream('map_b_0',0x427F1,0x42AF4,'big',1024,None,None),
    Stream('map_b_1',0x432F7,0x4357A,'big',1024,None,None),
    Stream('map_b_2',0x43D67,0x43FE6,'big',1024,None,None),
    Stream('map_b_3',0x447E9,0x44A6C,'big',1024,None,None),
)
BY_ID = {a.id:a for a in STREAMS}
DIRECTORIES = (('directory_a',0x3DACC),('directory_b',0x3DADC))
MAP_CALLS = ((0x3DA50,0x3DA5C,'directory_a',0xE000),
             (0x3DA72,0x3DA7E,'directory_b',0xE040),
             (0x3DA94,0x3DA9A,'directory_a',0xF000),
             (0x3DAB0,0x3DAB6,'directory_b',0xF040))
EDITABLE_BYTES = sum(a.end-a.start for a in STREAMS)+32
ANCHORS = {
    0x3AACE: '427880003c3c00204278800233fc8f0200c000043009610007ca78004a7880026602121814184a7880026606b20267000014e14214188478800033c200c00000612260e076001618670000381418e14214188478800033c200c00000610651cbfff260c052440c04002065000016534666064cdf00014e75d3c530096100076478004e7533fc8f0200c000046100075412181418b202670000101818e144180233c400c0000060ea760016186700001614181818e144180233c400c0000051cbfff860ce4e75',
    0x3DA08: '41f9000473e4303c00006100d13e41f9000492e8303c20006100d13041f90004a9a2303c40006100d12241f90004c5ac303c60006100d11441f90004e090303c80006100d1067000103880dbe54041fa00744e712070000043f90000e0002a3c000000804ebad0607000103880dbe54041fa00624e712070000043f90000e0402a3c000000804ebad03e7000103880dbe540207b003043f90000f0002a3c000000804ebad0227000103880dbe540207b002443f90000f0402a3c000000804ebad0064e75',
}


def check_anchors(rom):
    for start, raw in ANCHORS.items():
        if rom[start:start+len(raw)//2] != bytes.fromhex(raw):
            raise ValueError(f'consumer identity changed at {start:06X}')


def verify_rom(rom):
    if type(rom) is not bytes: raise ValueError('canonical ROM bytes required')
    g.af.verify_rom(rom)
    check_anchors(rom)


def metadata(a):
    return {'id':a.id,'start':a.start,'end':a.end,'byte_order':a.order,'decoded_words':a.words}


def consume(data, order, *, map_entry=False, output_budget=65536):
    """Read-only projection of guarded 03AB52 / full 03AACE entry.

    This models ROM byte consumption and word writes, not IRQ timing, VDP device
    behavior or arbitrary RAM/stack aliases. 03AACE clears its OR and raw flags.
    An external budget is not an original-code termination condition.
    """
    if type(data) is not bytes or not data or order not in ('big','little'):
        raise ValueError('nonempty source bytes and byte order required')
    if type(map_entry) is not bool or map_entry and order!='big':
        raise ValueError('map entry is the big-byte reader')
    rf.integer(output_budget,65536,'external output budget')
    if output_budget==0: raise ValueError('positive budget required')
    cursor=1; marker=data[0]; decoded=bytearray(); commands=[]
    def finish(stop,remaining=0):
        return {'stop':stop,'consumed':cursor,'output':bytes(decoded),
                'remaining_repeat_words':remaining,'commands':commands}
    def take():
        nonlocal cursor
        if cursor>=len(data): raise ValueError('consumer attempted source read outside supplied bytes')
        value=data[cursor]; cursor+=1; return value
    while True:
        start=cursor; first=take()
        if first==marker:
            count=take()
            if not count: return finish('marker_zero')
            count+=1; first=take(); second=take(); op='repeat'
        else:
            count=1; second=take(); op='literal'
        word=(first<<8|second) if order=='big' else (second<<8|first)
        commands.append({'start':start,'end':cursor,'op':op,'word':word,'count':count})
        for i in range(count):
            if len(decoded)//2>=output_budget: return finish('external_budget',count-i)
            decoded.extend(word.to_bytes(2,'big'))
            if map_entry and len(decoded)==2048: return finish('row_limit',count-i-1)


def pointer_lookup(memory, directory, selector):
    """Actual zero-extended byte *4 lookup, with NO four-slot CPU clamp."""
    if type(memory) is not bytes: raise ValueError('read-only memory bytes required')
    starts=dict(DIRECTORIES)
    if directory not in starts: raise ValueError('unknown physical directory')
    rf.integer(selector,255,'selector byte')
    address=starts[directory]+selector*4
    if address+4>len(memory): raise ValueError('pointer read outside supplied memory')
    return {'address':address,'pointer':int.from_bytes(memory[address:address+4],'big'),
            'in_catalog':selector<4}


def extract(rom):
    verify_rom(rom)
    id_at={a.start:a.id for a in STREAMS if a.order=='big'}
    return {'schema_version':1,'format':FORMAT,
        'directories':[{'id':ident,'targets':[id_at[int.from_bytes(rom[p:p+4],'big')]
            for p in range(start,start+16,4)]} for ident,start in DIRECTORIES],
        'streams':[{**metadata(a),'fields':rf.parse_word(rom[a.start:a.end],a.order,a.words)} for a in STREAMS]}


def blocks(rom,assets):
    verify_rom(rom)
    g.af._keys(assets,{'schema_version','format','directories','streams'},'battle graphics')
    if type(assets['schema_version']) is not int or assets['schema_version']!=1 or assets['format']!=FORMAT:
        raise ValueError('fixed schema/format changed')
    result=[]
    for (ident,start),row in zip(DIRECTORIES,g.exact_list(assets['directories'],2,'directories')):
        g.af._keys(row,{'id','targets'},'directory')
        if row['id']!=ident: raise ValueError('directory order/id changed')
        targets=g.exact_list(row['targets'],4,'directory slots'); raw=bytearray()
        for target in targets:
            if type(target) is not str or target not in BY_ID or BY_ID[target].order!='big':
                raise ValueError('editor target must be an existing 32x32 map ID')
            raw.extend(BY_ID[target].start.to_bytes(4,'big'))
        result.append({'id':ident,'start':start,'end':start+16,'role':'map_pointer_directory','data':bytes(raw)})
    for a,row in zip(STREAMS,g.exact_list(assets['streams'],13,'streams')):
        g.af._keys(row,set(metadata(a))|{'fields'},'stream')
        for key,value in metadata(a).items():
            if type(row[key]) is not type(value) or row[key]!=value: raise ValueError('fixed stream metadata changed')
        raw,decoded=rf.pack_word(row['fields'],a.order,a.words)
        if len(raw)!=a.end-a.start: raise ValueError('encoded fixed slot changed')
        consumed=consume(raw,a.order,map_entry=a.order=='big')
        if consumed['output']!=decoded: raise ValueError('consumer differs from physical codec')
        if consumed['stop']!=('row_limit' if a.order=='big' else 'marker_zero'):
            raise ValueError('unexpected consumer stop')
        expected=len(raw)-(2 if a.order=='big' else 0)
        if consumed['consumed']!=expected or consumed['remaining_repeat_words']:
            raise ValueError('editor requires exact command boundary at output extent')
        result.append({'id':a.id,'start':a.start,'end':a.end,
                       'role':'word_rle_tilemap' if a.order=='big' else 'word_rle_tiles','data':raw})
    return sorted(result,key=lambda r:r['start'])


def rebuild(rom,assets):
    image=bytearray(rom)
    for row in blocks(rom,assets): image[row['start']:row['end']]=row['data']
    return bytes(image)


def replace_decoded(rom,assets,ident,decoded):
    blocks(rom,assets)
    if ident not in BY_ID: raise ValueError('unknown stream')
    a=BY_ID[ident]; index=STREAMS.index(a); fields=assets['streams'][index]['fields']
    raw,old=rf.pack_word(fields,a.order,a.words)
    if type(decoded) is not bytes or len(decoded)!=len(old): raise ValueError('decoded fixed extent changed')
    result=copy.deepcopy(assets)
    if decoded==old: return result
    result['streams'][index]['fields']=rf.encode_word_exact(decoded,a.order,fields['marker'],len(raw))
    blocks(rom,result)
    return result


def manifest(rom):
    assets=extract(rom); rows=blocks(rom,assets); sources=[]
    for a,row in zip(STREAMS,assets['streams']):
        raw=rom[a.start:a.end]; runtime=consume(raw,a.order,map_entry=a.order=='big')
        sources.append({**metadata(a),'layout_confidence':'confirmed','purpose_confidence':'probable',
            'sha256':g.sha(raw),'decoded_sha256':g.sha(runtime['output']),
            'static_consumer':0x3AACE if a.order=='big' else 0x3AB52,
            'direct_call':a.call,'vram_target':a.vram,'consumer_read_end':a.start+runtime['consumed'],
            'consumer_read_bytes':runtime['consumed'],'unread_physical_tail_bytes':len(raw)-runtime['consumed'],
            'consumer_stop':runtime['stop'],'command_count':len(runtime['commands']),
            'natural_execution_proved':False})
    return {'schema_version':1,'format':FORMAT,'canonical_rom_sha256':g.sha(rom),
        'editable_bytes':EDITABLE_BYTES,'physical_stream_bytes':EDITABLE_BYTES-32,
        'map_physical_tail_bytes_not_read':16,'source_fields_sha256':g.sha(g.dump(assets)),
        'ownership_basis':'guarded static consumers and exact physical grammar, not global selector closure',
        'owners':[{k:r[k] for k in ('id','start','end','role')} for r in rows],
        'assets':sources,'directories':[{'id':ident,'start':start,'end':start+16,'width':4,'byte_order':'big',
             'targets':assets['directories'][i]['targets'],'global_selector_domain_complete':False}
             for i,(ident,start) in enumerate(DIRECTORIES)],
        'map_calls':[{'selector_read':read,'pointer_read':pointer,'directory':ident,'vram_target':vram,'row_stride':128}
                     for read,pointer,ident,vram in MAP_CALLS],
        'consumer_anchors':[{'start':start,'end':start+len(raw)//2,'bytes':raw,'sha256':g.sha(bytes.fromhex(raw))}
                            for start,raw in ANCHORS.items()],
        'excluded_alignment_bytes':[a.end for a in STREAMS if a.order=='little'],
        'boundaries':['two catalogs of four slots; each of four render calls re-reads FF80DB',
            '03AACE exits at 1024 words and does not read the physical marker/zero tail',
            'raw consumer model permits partial final repeats; editor policy requires exactly1024 physical outputs',
            'alignment bytes, other graphic sources and arbitrary selector lookups are not owned',
            'cross-mode FF80DA word4 is an alias, not a naturally reached out-of-catalog map call',
            'battle-mode label probable; all-catalog natural reachability and edited gameplay unknown',
            'preview uses grayscale colour indices, not a recovered palette or screenshot']}


def preview_tiles(decoded):
    """Derived 16x16-tile grayscale atlas; no RGB palette claim."""
    if type(decoded) is not bytes or len(decoded)!=8192: raise ValueError('256 complete MD tiles required')
    width=height=128; rows=[bytearray(width*3) for _ in range(height)]
    for tile in range(256):
        for y in range(8):
            for x in range(8):
                v=decoded[tile*32+y*4+x//2]
                level=((v>>4) if not x%2 else (v&15))*17
                p=((tile%16)*8+x)*3
                rows[(tile//16)*8+y][p:p+3]=bytes([level])*3
    pixels=b''.join(b'\0'+row for row in rows)
    return (b'\x89PNG\r\n\x1a\n'+g.title.png_chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,2,0,0,0))+
            g.title.png_chunk(b'IDAT',zlib.compress(pixels,9))+g.title.png_chunk(b'IEND',b''))


def preview_maps(rom,assets):
    """Derived map atlas using only the five reconstructed VRAM uploads.

    Known tiles use grayscale indices with real flips. Unloaded indices use
    a conspicuous magenta/black checker, NEVER invented zero-filled VRAM art.
    Palette selection/priority remain in source words but do not affect this
    grayscale projection. No emulator-frame or actual-palette claim is made.
    """
    blocks(rom,assets); decoded={a.id:rf.pack_word(row['fields'],a.order,a.words)[1]
                                for a,row in zip(STREAMS,assets['streams'])}
    tiles={}
    for a in STREAMS[:5]:
        for n in range(256): tiles[a.vram//32+n]=decoded[a.id][n*32:(n+1)*32]
    bundle={}; info={}
    for a in STREAMS[5:]:
        raw=decoded[a.id]; pixels=bytearray(256*256*3); missing=set()
        for n in range(1024):
            word=int.from_bytes(raw[n*2:n*2+2],'big'); cell=g.cell(word); tile=tiles.get(cell['tile'])
            if tile is None: missing.add(cell['tile'])
            for y in range(8):
                for x in range(8):
                    sx=7-x if cell['hflip'] else x; sy=7-y if cell['vflip'] else y
                    if tile is None: rgb=bytes([255,0,255]) if (x+y)%2 else bytes(3)
                    else:
                        v=tile[sy*4+sx//2]; level=(v&15 if sx%2 else v>>4)*17; rgb=bytes([level])*3
                    p=(((n//32)*8+y)*256+(n%32)*8+x)*3; pixels[p:p+3]=rgb
        data=b''.join(b'\0'+pixels[y*768:(y+1)*768] for y in range(256))
        bundle[a.id+'.png']=(b'\x89PNG\r\n\x1a\n'+g.title.png_chunk(b'IHDR',struct.pack('>IIBBBBB',256,256,8,2,0,0,0))+
             g.title.png_chunk(b'IDAT',zlib.compress(data,9))+g.title.png_chunk(b'IEND',b''))
        info[a.id]={'unloaded_tile_indices':sorted(missing),'palette_policy':'grayscale index; not original RGB',
                    'unknown_tile_policy':'magenta/black checker, not inferred game pixels'}
    bundle['map_preview.json']=g.dump(info)
    return bundle


def render_bundle(rom):
    assets=extract(rom); info=manifest(rom)
    return {'assets.json':g.dump(assets),'manifest.json':g.dump(info),
        'README.md':('# Battle-mode graphics: fixed field source\n\n'
          'Confirmed: five little-byte RLE tile streams, eight big-byte RLE32x32 maps, two4xBE32 catalogs.\n\n'
          '- 45,719 editable physical bytes; all fields reside in assets.json only.\n'
          '- Map read bytes10,860; physical bytes10,876:16 marker/zero tail bytes are not read at full-entry03AACE.\n'
          '- Tile read bytes34,811 include terminators. Five following alignment bytes remain excluded.\n'
          '- Every map call re-reads FF80DB; the global selector domain is NOT proved to be0..3.\n'
          '- Physical commands and map targets are editable; fixed layout and no-op roundtrip are enforced.\n'
          '- Editor catalog restrictions are not CPU bounds. Aliases across the eight existing maps are permitted.\n'
          '- Purpose probable; static catalog evaluation is not natural execution evidence.\n'
          '- Preview command emits derived grayscale colour-index atlases, not authoritative palette data.\n'
          '- Consumer model excludes interrupts, shared-stack mutation and the external VDP device.\n').encode()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','verify','import','replace-decoded','preview'))
    parser.add_argument('--rom',type=Path,default=DEFAULT_ROM)
    parser.add_argument('--assets',type=Path,default=DEFAULT_ASSETS)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--asset-id'); parser.add_argument('--decoded',type=Path)
    args=parser.parse_args()
    read=lambda p:g.af._read(g.af.safe_path(p,regular_input=True),16*1024*1024)
    rom=read(args.rom); verify_rom(rom)
    if args.command=='export': bundle=render_bundle(rom); inputs=[args.rom]
    else:
        assets=g.af.load_assets(read(args.assets)); image=rebuild(rom,assets); inputs=[args.rom,args.assets]
        if args.command=='verify':
            print({'canonical_exact':image==rom,'sha256':g.sha(image),'editable_bytes':EDITABLE_BYTES}); return
        if args.command=='replace-decoded':
            if args.decoded is None or args.asset_id is None: raise ValueError('--decoded and --asset-id required')
            bundle={'assets.json':g.dump(replace_decoded(rom,assets,args.asset_id,read(args.decoded)))}; inputs.append(args.decoded)
        elif args.command=='preview':
            bundle={a.id+'.png':preview_tiles(rf.pack_word(row['fields'],a.order,a.words)[1])
                    for a,row in zip(STREAMS,assets['streams']) if a.order=='little'}
            bundle.update(preview_maps(rom,assets))
        else: bundle={'rebuilt.bin':image,'validation.json':g.dump({'sha256':g.sha(image),
                     'canonical_exact':image==rom,'changed_bytes':sum(a!=b for a,b in zip(image,rom))})}
    if args.output is None: raise ValueError('--output required')
    print(g.publish(bundle,args.output,inputs))


if __name__=='__main__': main()
