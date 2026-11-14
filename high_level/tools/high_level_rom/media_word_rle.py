"""Lossless title word-RLE pixels as complete editable eight-by-eight tiles.

PNG tiles are the only pixel authority. The existing marker and fixed source
slot remain the original typed resource metadata; the separate command member
contains only literal/repeat topology. No encoded-word fallback is retained.
"""
from __future__ import annotations


FORMAT = 'g5510-title-word-rle-tile-pixels-v1'
CODEC = 'tile_word_rle_commands'
TITLE_STREAM_IDS = (
    'title_tiles_rle_0','title_tiles_rle_1','title_tiles_rle_2',
    'title_tiles_rle_3','title_tiles_rle_4',
)
DECODED_WORDS = 4096
WORDS_PER_TILE = 16
TILE_COUNT = DECODED_WORDS // WORDS_PER_TILE


def _count(control):
    """Keep the original literal/repeat grammar, not a new RLE encoder."""
    if type(control) is not dict:
        raise ValueError('one explicit word-RLE control object required')
    if control.get('op')=='literal' and set(control)=={'op'}:
        return 1
    if (control.get('op')=='repeat' and set(control)=={'op','count'}
            and type(control['count']) is int and 2<=control['count']<=256):
        return control['count']
    raise ValueError('original literal or 2..256 WORD repeat control required')


def _controls(values):
    if type(values) is not list or not 1<=len(values)<=DECODED_WORDS:
        raise ValueError('bounded explicit title word-RLE controls required')
    counts = [_count(value) for value in values]
    if sum(counts)!=DECODED_WORDS:
        raise ValueError('the original4096-WORD extent must remain exact; no tile padding or truncation')
    return counts


def externalize_title_tiles(package,locator,directory):
    """Publish all known pixels; Package owns encoding and one-time members.

    This helper is called only for the five proven title pixel streams. It
    neither opens the ROM nor decodes a map WORD as a four-index pixel row.
    """
    container = package.graph
    for key in locator[:-1]:
        container = container[key]
    if set(container)!= {'marker','commands'} or locator[-1]!='commands':
        raise ValueError('the actual marker/command title source object required')
    marker = container['marker']
    if type(marker) is not int or not 0<=marker<=255:
        raise ValueError('one actual source marker BYTE required')
    commands = container['commands']
    if type(commands) is not list or not 1<=len(commands)<=DECODED_WORDS:
        raise ValueError('bounded explicit original title commands required')
    controls,words = [],[]
    for command in commands:
        if type(command) is not dict or 'word' not in command:
            raise ValueError('one actual original title WORD command required')
        value = command['word']
        if type(value) is not int or not 0<=value<=65535:
            raise ValueError('one complete original WORD pixel value required')
        control = {key:item for key,item in command.items() if key!='word'}
        count = _count(control)
        if control['op']=='literal' and value.to_bytes(2,'little')[0]==marker:
            raise ValueError('literal source low BYTE cannot be the original escape marker')
        controls.append(control)
        words.extend([value]*count)
        if len(words)>DECODED_WORDS:
            raise ValueError('original title stream exceeds its complete4096-WORD extent')
    _controls(controls)
    tiles = []
    for start in range(0,DECODED_WORDS,WORDS_PER_TILE):
        pixels = [(word>>shift)&15 for word in words[start:start+WORDS_PER_TILE]
            for shift in (12,8,4,0)]
        tile = [pixels[row:row+8] for row in range(0,64,8)]
        tiles.append(package.add(tile,directory+'/tiles/tile_'+format(start//16,'04d')+'.png',
            codec='tile4_pixels',width=8,height=8,bit_order='msb',source_locator=locator))
    topology = dict(format=FORMAT,decoded_words=DECODED_WORDS,word_order='little',
        controls=controls,tiles=tiles)
    # The graph loses its old numeric command WORDs here. The only persisted
    # values are the PNGs; topology contains no backup word or encoded bytes.
    container['commands'] = package.add(topology,directory+'/commands.json',
        codec=CODEC,source_locator=locator)


def resolve_title_tiles(source,visit,declarations,*,reference_key):
    """Reconstruct original command WORDs from sole PNGs, or reject conflicts.

    Repeated output crosses tile and row boundaries naturally. Every WORD in
    an original repeat must agree. Taking only its first edited occurrence
    would hide conflicting editing authorities and is deliberately forbidden.
    """
    if (type(source) is not dict or set(source)!= {'format','decoded_words','word_order','controls','tiles'}
            or source['format']!=FORMAT or type(source['decoded_words']) is not int
            or source['decoded_words']!=DECODED_WORDS or source['word_order']!='little'
            or type(source['tiles']) is not list or len(source['tiles'])!=TILE_COUNT):
        raise ValueError('the complete original title4096-WORD/256-tile source declaration required')
    counts = _controls(source['controls'])
    for reference in source['tiles']:
        if (type(reference) is not dict or set(reference)!={reference_key}
                or type(reference[reference_key]) is not str or reference[reference_key] not in declarations):
            raise ValueError('each title tile must reference one declared PNG authority')
        row = declarations[reference[reference_key]]
        if (row['codec'],row['width'],row['height'],row['bit_order'])!=('tile4_pixels',8,8,'msb'):
            raise ValueError('each title tile must be the actual complete8x8 indexed PNG kind')
    tiles = visit(source['tiles'])
    words = []
    for tile in tiles:
        if (type(tile) is not list or len(tile)!=8 or any(type(row) is not list or len(row)!=8
                or any(type(pixel) is not int or not 0<=pixel<=15 for pixel in row) for row in tile)):
            raise ValueError('complete title tile indices required; no invented neighbours or colour conversion')
        for row in tile:
            for start in (0,4):
                words.append(sum(row[start+column]<<((3-column)*4) for column in range(4)))
    commands,cursor = [],0
    for control,count in zip(source['controls'],counts):
        run = words[cursor:cursor+count]
        if len(run)!=count or any(word!=run[0] for word in run):
            raise ValueError('conflicting PNG pixels in original repeated WORD run '+str(cursor)+':'+str(cursor+count)
                +'; keep every repeat occurrence equal or explicitly edit the fixed-cost command topology')
        commands.append(dict(control,word=run[0]))
        cursor += count
    if cursor!=len(words) or len(words)!=DECODED_WORDS:
        raise ValueError('the complete title tile pixel authority must be consumed exactly once')
    return commands
