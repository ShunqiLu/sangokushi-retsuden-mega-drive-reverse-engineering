"""Own graph/member publication, separated from individual asset families.

Members are the sole editable authority. The graph retains references and
fixed schema metadata; no cached pixel or record copy is an importer fallback.
"""
from __future__ import annotations

import copy

from .media_sources import FORMAT, REFERENCE, indexed_png, json_bytes


LIMITS = [
    'external files are actual build inputs, not a claim of edited natural display/playback correctness',
    'physical IDs and prior candidate/unknown identities are retained; no officer/object identity guessed',
    'indexed PNG colours are neutral; complete original CRAM fields remain independent JSON authority',
    'compressed command fields remain source; no decoded-picture recompression or size relocation implied',
    'this selected media publication is not all-image/audio identity recovery or final dual-project delivery',
]


class Package:
    """One typed source graph, one file per editable declared component."""

    def __init__(self, ident, fields):
        self.ident, self.graph = ident, copy.deepcopy(fields)
        self.members, self.files = [], {}

    def replace(self, locator, filename, *, codec='typed_json', width=None, height=None, bit_order=None):
        container = self.graph
        for key in locator[:-1]:
            container = container[key]
        value = container[locator[-1]]
        container[locator[-1]] = self.add(value, filename, codec=codec, width=width, height=height,
                                         bit_order=bit_order, source_locator=locator)

    def add(self, value, filename, *, codec='typed_json', width=None, height=None, bit_order=None, source_locator=()):
        """Add one sole source authority and return its graph reference."""
        ident = self.ident + ':' + str(len(self.members))
        if filename in self.files:
            raise ValueError('duplicate external media file authority')
        if codec == 'tile4_rows':
            if (type(value) is not list or len(value) != 8 or
                    any(type(row) is not str or len(row) != 8 or any(ch not in '0123456789ABCDEF' for ch in row)
                        for row in value)):
                raise ValueError('original tile rows must be exact four-bit indices')
            raw = indexed_png([int(ch, 16) for row in value for ch in row], width, height, 4)
        elif codec == 'tile4_pixels':
            if (type(value) is not list or len(value) != 8 or
                    any(type(row) is not list or len(row) != 8 or
                        any(type(pixel) is not int or not 0 <= pixel <= 15 for pixel in row) for row in value)):
                raise ValueError('complete eight-row numeric four-bit tile required')
            raw = indexed_png([pixel for row in value for pixel in row], width, height, 4)
        elif codec == 'pixel_pair4':
            if ((width, height, bit_order) != (2, 1, 'msb') or type(value) is not list or len(value) != 2
                    or any(type(pixel) is not int or not 0 <= pixel <= 15 for pixel in value)):
                raise ValueError('one exact high/low nibble pixel pair required')
            raw = indexed_png(value, width, height, 4)
        elif codec == 'mono_rows':
            if (type(value) is not list or len(value) != height or
                    any(type(row) is not int or not 0 <= row < 1 << width for row in value)):
                raise ValueError('complete fixed monochrome rows required')
            pixels = [(row >> (column if bit_order == 'lsb' else width - column - 1)) & 1
                      for row in value for column in range(width)]
            raw = indexed_png(pixels, width, height, 1)
        elif codec == 'word_pixels':
            if (type(value) is not list or len(value) != height or width != 4 or bit_order != 'msb' or
                    any(type(word) is not int or not 0 <= word <= 65535 for word in value)):
                raise ValueError('one exact decoded BE WORD per four-index PNG row required')
            raw = indexed_png([(word >> shift) & 15 for word in value for shift in (12, 8, 4, 0)], 4, height, 4)
        elif codec in ('typed_json', 'word_rle_commands', 'tile_word_rle_commands'):
            raw = json_bytes(value)
        else:
            raise ValueError('unregistered publication codec')
        self.files[filename] = raw
        self.members.append(dict(id=ident, file=filename, codec=codec, width=width, height=height,
                                 bit_order=bit_order, source_locator=list(source_locator)))
        return {REFERENCE: ident}

    def wrapper(self):
        return dict(format=FORMAT, resource_id=self.ident, source_format=self.graph['format'],
                    graph=self.graph, members=self.members, limits=list(LIMITS))
