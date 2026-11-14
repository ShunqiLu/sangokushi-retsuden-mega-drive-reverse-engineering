"""Keep the Scene's ordered events accessible without holding them all in RAM."""

from __future__ import annotations

import marshal
from operator import index as as_index
from pathlib import Path
import struct
import zlib


_MAGIC = b'G5510 scene event journal v1\n'
_PAGE = struct.Struct('<III')  # Event count, expanded bytes, compressed bytes.
_PAGE_EVENTS = 8192
_MAX_PAGE_BYTES = 4 << 20
MAX_JOURNAL_BYTES = 512 << 20
_PAGE_RESERVE = _PAGE.size + _MAX_PAGE_BYTES + 4096  # Safe bound for zlib framing.


class SceneEventJournal:
    """One append-only event sequence with stable absolute indices and a small cache."""

    def __init__(self, path: Path):
        self.path = path
        self._file = path.open('x+b')
        self._tail = []
        self._count = 0
        self._offsets = []
        self._cached_index, self._cached_page = -1, ()
        self._extent = 0
        self._failed = False
        try:
            self._write(_MAGIC)
        except BaseException:
            self._file.close()
            raise

    def _write(self, data):
        if self._file.write(data) != len(data):
            raise OSError('Short write to the Scene event journal')
        self._extent += len(data)

    def _seal_tail(self):
        if not self._tail:
            return
        offset = self._extent
        try:
            raw = marshal.dumps(self._tail, 4)
            if len(raw) > _MAX_PAGE_BYTES:
                raise OSError('A Scene event page exceeded its storage limit')
            compressed = zlib.compress(raw, level=1)
            if self._extent + _PAGE.size + len(compressed) > MAX_JOURNAL_BYTES:
                raise OSError('The Scene event journal reached its 512 MiB limit')
            self._file.seek(offset)
            self._write(_PAGE.pack(len(self._tail), len(raw), len(compressed)))
            self._write(compressed)
        except BaseException:
            self._failed = True
            raise
        self._offsets.append(offset)
        self._tail.clear()

    def append(self, event):
        if self._file.closed:
            raise ValueError('The Scene event journal is closed')
        if self._failed:
            raise OSError('The Scene event journal could not finish its previous page')
        if type(event) is not tuple:
            raise TypeError('A Scene event must be a tuple')
        if len(self._tail) == _PAGE_EVENTS:
            self._seal_tail()
        if not self._tail and self._extent + _PAGE_RESERVE > MAX_JOURNAL_BYTES:
            raise OSError('The Scene event journal cannot reserve another page within its 512 MiB limit')
        self._tail.append(event)
        self._count += 1

    def __len__(self):
        return self._count

    def _page(self, number):
        if number == len(self._offsets):
            return self._tail
        if number != self._cached_index:
            self._file.seek(self._offsets[number])
            header = self._file.read(_PAGE.size)
            if len(header) != _PAGE.size:
                raise OSError('Truncated Scene event page header')
            count, expanded, compressed = _PAGE.unpack(header)
            if not (0 < count <= _PAGE_EVENTS and 0 < expanded <= _MAX_PAGE_BYTES
                    and 0 < compressed <= _MAX_PAGE_BYTES + 4096):
                raise OSError('Invalid Scene event page extents')
            payload = self._file.read(compressed)
            inflater = zlib.decompressobj()
            raw = inflater.decompress(payload, expanded + 1)
            if len(payload) != compressed or len(raw) != expanded or not inflater.eof or inflater.unused_data:
                raise OSError('Scene event page cannot be read completely')
            page = marshal.loads(raw)
            if type(page) is not list or len(page) != count:
                raise OSError('Invalid Scene event page content')
            self._cached_index, self._cached_page = number, page
        return self._cached_page

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(self._count))]
        i = as_index(key)
        if i < 0:
            i += self._count
        if not 0 <= i < self._count:
            raise IndexError('Scene event index is out of range')
        page, position = divmod(i, _PAGE_EVENTS)
        return self._page(page)[position]

    def __iter__(self):
        # Like a list iterator, see appends made before reaching the current end.
        i = 0
        while i < self._count:
            yield self[i]
            i += 1

    def close(self):
        if self._file.closed:
            return
        try:
            if not self._failed:
                self._seal_tail()
        finally:
            self._file.close()
            self._cached_index, self._cached_page = -1, ()
