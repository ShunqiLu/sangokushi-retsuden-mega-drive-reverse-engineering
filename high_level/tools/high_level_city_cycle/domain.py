"""Fixed-width arithmetic and live semantic memory interfaces, not a CPU."""
from dataclasses import dataclass

Word = int
Long = int
Byte = int

def integer(value):
    if type(value) is not int:raise ValueError('strict integer, not bool/float, required')
    return value
def unsigned(value,bits):
    integer(value);integer(bits)
    if not 1<=bits<=32:raise ValueError('explicit width1..32 required')
    if not 0<=value<(1<<bits):raise ValueError('complete unsigned field required')
    return value
def word(value): return integer(value) & 65535
def long(value): return integer(value) & 0xFFFFFFFF
def byte(value): return integer(value) & 255
def low_word(value): return integer(value) & 65535
def low_byte(value): return integer(value) & 255
def signed_word(value): return (integer(value) & 32767) - (value & 32768)
def add16(left, right): return word(integer(left) + integer(right))
def sub16(left, right): return word(integer(left) - integer(right))
def add32(left, right): return long(integer(left) + integer(right))
def sub32(left, right): return long(integer(left) - integer(right))
def sub8(left, right): return (integer(left) & ~255) | byte(left - integer(right))
def shl16(value, count): return word(integer(value) << integer(count))
def shl32(value, count): return long(integer(value) << integer(count))
def mask16(value, mask): return word(integer(value) & integer(mask))
def mask32(value, mask): return long(integer(value) & integer(mask))
def clear_low_word(value): return integer(value) & 0xFFFF0000
def negate32(value): return long(-integer(value))
def swap_words(value): return long(integer(value) << 16 | value >> 16)
def replace_low_word(value, low): return integer(value) & 0xFFFF0000 | word(low)
def mulu16(left, right): return word(left) * word(right)
def divu16(value, divisor):
    if type(divisor) is not int or not 1 <= divisor <= 65535: raise ValueError('nonzero WORD divisor required')
    quotient, remainder = divmod(long(value), divisor)
    return long(value) if quotient > 65535 else remainder << 16 | quotient
def stitched_product(value, factor):
    """Two low-WORD products; swapped high product is not ordinary multiplication."""
    return add32(mulu16(value, factor), swap_words(mulu16(swap_words(value), factor)))
def saturating_add32(left, right): return min(long(left) + long(right), 0xFFFFFFFF)
def subtract_borrow32(left, right): return sub32(left, right), long(left) < long(right)
def minimum32(value, ceiling): return min(long(value), long(ceiling))

@dataclass
class Table:
    memory: object
    address: int
    cursor: int | None = None
    def __post_init__(self):
        unsigned(self.address,32)
        if self.cursor is not None:unsigned(self.cursor,32)
    def ea(self, offset=0, displacement=0):
        unsigned(offset,16);integer(displacement)
        return long(self.address + signed_word(offset) + displacement)
    def _read(self, offset, displacement, size): return unsigned(self.memory.read(self.ea(offset, displacement), size),size*8)
    def word(self, offset=0, displacement=0): return self._read(offset, displacement, 2)
    def long(self, offset=0, displacement=0): return self._read(offset, displacement, 4)
    def byte(self, offset=0, displacement=0): return self._read(offset, displacement, 1)
    def set_word(self, offset, value, displacement=0): self.memory.write(self.ea(offset, displacement),2,word(value))
    def set_long(self, offset, value, displacement=0): self.memory.write(self.ea(offset, displacement),4,long(value))
    def set_byte(self, offset, value, displacement=0): self.memory.write(self.ea(offset, displacement),1,byte(value))
    def next_word(self): return self._next(2)
    def next_byte(self): return self._next(1)
    def _next(self, size):
        if self.cursor is None: self.cursor=self.address
        value=unsigned(self.memory.read(self.cursor,size),size*8); self.cursor=long(self.cursor+size); return value
    def append_word(self,value): self._append(value,2)
    def append_long(self,value): self._append(value,4)
    def _append(self,value,size):
        if self.cursor is None: self.cursor=self.address
        self.memory.write(self.cursor,size,integer(value) & ((1<<(size*8))-1)); self.cursor=long(self.cursor+size)
    def put_word(self,value): self.memory.write(self.address if self.cursor is None else self.cursor,2,word(value))
    def subtract_word(self,offset,value,displacement=0): self.set_word(offset,sub16(self.word(offset,displacement),value),displacement)
    def subtract_byte(self,offset,value):
        integer(value);previous=self.byte(offset);self.set_byte(offset,byte(previous-value));return previous<byte(value)

class CityState:
    """All table/scalar bindings supplied explicitly; every request is a live read."""
    def __init__(self,memory,tables,scalars):
        self.memory=memory;self.tables=dict(tables);self.scalars=dict(scalars)
        for key,address in self.tables.items():
            if type(key) is not str:raise ValueError('stable semantic table name required')
            unsigned(address,32)
        for key,(address,size) in self.scalars.items():
            if type(key) is not str or type(size) is not int or size not in (1,2,4):raise ValueError('typed semantic scalar required')
            unsigned(address,32)
    def __getattr__(self,name):
        if name in self.tables:return Table(self.memory,self.tables[name])
        if name.startswith('set_') and name[4:] in self.scalars:
            address,size=self.scalars[name[4:]]
            return lambda value:self.memory.write(address,size,integer(value) & ((1<<(size*8))-1))
        if name in self.scalars:
            address,size=self.scalars[name]
            return lambda:unsigned(self.memory.read(address,size),size*8)
        raise AttributeError(name)
