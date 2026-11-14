"""The actual six-position formatter and dialogue insertion, not a decimal clamp.

Only the listed instructions execute. ROM is immutable; explicit 64 KiB RAM,
68000 big-endian stack accesses and the 24-bit bus share one address space.
No IRQ, device, renderer, cycle timing or full condition-register model is added.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass

from tools.audio_formats import audio_formats as af


TABLE = 0x012782
BUFFER = 0xFFFFD300
FORMATTER = 0x01270A
TIMED_READER = 0x0671B6
INSTRUCTIONS = {
    0x1270A:'4243', 0x1270C:'4244', 0x1270E:'0480000186a0',
    0x12714:'6504', 0x12716:'5243', 0x12718:'60f4',
    0x1271A:'0680000186a0', 0x12720:'4a43', 0x12722:'6604',
    0x12724:'3cc2', 0x12726:'600c', 0x12728:'4245',
    0x1272A:'1a3b3056', 0x1272E:'da41', 0x12730:'3cc5',
    0x12732:'5244', 0x12734:'363c2710', 0x12738:'61000026',
    0x1273C:'363c03e8', 0x12740:'6100001e', 0x12744:'363c0064',
    0x12748:'61000016', 0x1274C:'363c000a', 0x12750:'6100000e',
    0x12754:'4245', 0x12756:'1a3b002a', 0x1275A:'da41',
    0x1275C:'3cc5', 0x1275E:'4e75', 0x12760:'4245',
    0x12762:'80c3', 0x12764:'4a44', 0x12766:'6604',
    0x12768:'4a40', 0x1276A:'670e', 0x1276C:'1a3b0014',
    0x12770:'da41', 0x12772:'3cc5', 0x12774:'383c0001',
    0x12778:'6002', 0x1277A:'3cc2', 0x1277C:'4240',
    0x1277E:'4840', 0x12780:'4e75',
    0x67268:'2038f3c8', 0x6726C:'223c00004100', 0x67272:'4242',
    0x67274:'4df8d300', 0x67278:'4eb90001270a', 0x6727E:'31fc800cd30c',
    0x67284:'4df8d300', 0x67288:'4a5e', 0x6728A:'67fc',
    0x6728C:'554e', 0x6728E:'21f8f3bef3d4', 0x67294:'21cef3be',
    0x67298:'6000ff1c', 0x6729C:'2038f3cc', 0x672A0:'60ca',
    0x672EC:'21f8f3d4f3be', 0x672F2:'6000fec2',
    0x67338:'7000', 0x6733A:'1038f374', 0x6733E:'064000b8',
    0x67342:'6000ff28', 0x67346:'7000', 0x67348:'1038f375',
    0x6734C:'06400001', 0x67350:'6000ff1a',
}


def uint(value, bits, name):
    if type(value) is not int or not 0 <= value < 1 << bits:
        raise ValueError(f'{name}: strict unsigned {bits}-bit integer required')
    return value


def signed16(value):
    value &= 0xFFFF
    return value if value < 0x8000 else value - 0x10000


def check_code(rom):
    for pc, text in INSTRUCTIONS.items():
        raw = bytes.fromhex(text)
        if rom[pc:pc + len(raw)] != raw:
            raise ValueError(f'original numeric instruction changed at {pc:06x}')


class Boundary(ValueError):
    """Execution stopped; already committed RAM/register effects are retained."""


@dataclass
class Registers:
    d0: int = 0
    d1: int = 0x4100
    d2: int = 0
    d3: int = 0
    d4: int = 0
    d5: int = 0
    a6: int = BUFFER
    a7: int = 0xFFFFFE00
    pc: int = FORMATTER

    def validate(self):
        for name, value in asdict(self).items():
            uint(value, 32, name)

    def word(self, name, value):
        setattr(self, name, (getattr(self, name) & 0xFFFF0000) | (value & 0xFFFF))


class Bus:
    def __init__(self, rom, ram):
        af.verify_rom(rom)
        check_code(rom)
        if type(ram) is not bytearray or len(ram) != 65536:
            raise ValueError('explicit writable 65536-byte RAM required')
        self.rom, self.ram = rom, ram
        self.events = []
        self.pc = None

    def read8(self, address, *, kind='read'):
        physical = address & 0xFFFFFF
        if physical < len(self.rom):
            value = self.rom[physical]
        elif physical >= 0xFF0000:
            value = self.ram[physical - 0xFF0000]
        else:
            raise Boundary(f'unmapped_read:{physical:06x}')
        if kind != 'fetch':
            self.events.append({'pc': self.pc, 'kind': kind, 'address': physical, 'value': value})
        return value

    def read(self, address, size, *, kind='read'):
        if size not in (2, 4) or address & 1:
            raise Boundary(f'address_error_read:{address & 0xFFFFFF:06x}')
        return int.from_bytes(bytes(self.read8(address + i, kind=kind) for i in range(size)), 'big')

    def write(self, address, value, size):
        if size not in (2, 4) or address & 1:
            raise Boundary(f'address_error_write:{address & 0xFFFFFF:06x}')
        uint(value, size * 8, 'write value')
        for i, octet in enumerate(value.to_bytes(size, 'big')):
            physical = (address + i) & 0xFFFFFF
            if physical < 0xFF0000:
                raise Boundary(f'unmapped_or_readonly_write:{physical:06x}')
            self.ram[physical - 0xFF0000] = octet
            self.events.append({'pc': self.pc, 'kind': 'write', 'address': physical, 'value': octet})


class Executor:
    """Instruction-local translation with a real shared RAM stack.

Carry and zero are refreshed by every listed instruction that changes them,
including unusual returns into this region caused by shared-stack aliasing.
Undefined DIVU overflow zero stays unknown. Other CCR bits are not modelled.
A boundary is not a resumable microcycle state.
"""
    def __init__(self, bus, registers):
        if type(bus) is not Bus or type(registers) is not Registers:
            raise ValueError('explicit numeric Bus and Registers required')
        registers.validate()
        self.bus, self.cpu = bus, registers
        self.zero = self.carry = None
        self.executed = Counter()
        self.divisions = []
        self.table_reads = []

    def push(self, value):
        self.cpu.a7 = (self.cpu.a7 - 4) & 0xFFFFFFFF
        self.bus.write(self.cpu.a7, value, 4)

    def pop(self):
        value = self.bus.read(self.cpu.a7, 4)
        self.cpu.a7 = (self.cpu.a7 + 4) & 0xFFFFFFFF
        return value

    def emit(self, name):
        value = getattr(self.cpu, name) & 0xFFFF
        self.bus.write(self.cpu.a6, value, 2)
        self.cpu.a6 = (self.cpu.a6 + 2) & 0xFFFFFFFF
        self.logic_flags(value, 16)

    def logic_flags(self, value, bits):
        """MOVE/CLR/TST/SWAP: C=0, Z according to the operation's width."""
        self.carry = False
        self.zero = (value & ((1 << bits) - 1)) == 0

    def add(self, name, operand, bits=16):
        mask = (1 << bits) - 1
        value = (getattr(self.cpu, name) & mask) + (operand & mask)
        self.carry = value > mask
        self.zero = (value & mask) == 0
        if bits == 16: self.cpu.word(name, value)
        else: setattr(self.cpu, name, value & mask)

    def lookup(self, name):
        index = getattr(self.cpu, name) & 0xFFFF
        address = TABLE + signed16(index)
        value = self.bus.read8(address, kind='digit_lookup')
        self.table_reads.append({'pc': self.cpu.pc, 'word_index': index,
                                 'signed_index': signed16(index), 'address': address,
                                 'value': value, 'inside_digit_table': TABLE <= address < TABLE + 10})
        self.cpu.d5 = (self.cpu.d5 & 0xFFFFFF00) | value
        self.logic_flags(value, 8)

    def condition(self, name):
        value = getattr(self, name)
        if type(value) is not bool:
            raise Boundary(f'unknown_branch_condition:{self.cpu.pc:06x}:{name}')
        return value

    def step(self):
        c, b, pc = self.cpu, self.bus, self.cpu.pc
        b.pc = pc
        if pc not in INSTRUCTIONS:
            raise Boundary(f'unmodelled_instruction:{pc:08x}')
        expected = bytes.fromhex(INSTRUCTIONS[pc])
        if pc & 1:
            raise Boundary(f'address_error_fetch:{pc:08x}')
        actual = bytes(b.read8(pc + i, kind='fetch') for i in range(len(expected)))
        if actual != expected:
            raise Boundary(f'changed_instruction:{pc:06x}')
        following = (pc + len(expected)) & 0xFFFFFFFF
        clears = {0x1270A:'d3', 0x1270C:'d4', 0x12728:'d5', 0x12754:'d5',
                  0x12760:'d5', 0x1277C:'d0', 0x67272:'d2'}
        tests = {0x12720:'d3', 0x12764:'d4', 0x12768:'d0'}
        if pc in clears:
            c.word(clears[pc], 0)
            self.logic_flags(0, 16)
        elif pc == 0x1270E:
            self.carry = c.d0 < 100000
            c.d0 = (c.d0 - 100000) & 0xFFFFFFFF
            self.zero = c.d0 == 0
        elif pc == 0x12714:
            if self.condition('carry'): following = 0x1271A
        elif pc in (0x12716, 0x12732):
            name = 'd3' if pc == 0x12716 else 'd4'
            self.add(name, 1)
        elif pc == 0x1271A:
            self.add('d0', 100000, 32)
        elif pc in tests:
            self.logic_flags(getattr(c, tests[pc]), 16)
        elif pc in (0x12722, 0x12766):
            if not self.condition('zero'): following = 0x12728 if pc == 0x12722 else 0x1276C
        elif pc == 0x1276A:
            if self.condition('zero'): following = 0x1277A
        elif pc in (0x12724, 0x1277A): self.emit('d2')
        elif pc in (0x12730, 0x1275C, 0x12772): self.emit('d5')
        elif pc in (0x1272A, 0x12756, 0x1276C):
            self.lookup('d3' if pc == 0x1272A else 'd0')
        elif pc in (0x1272E, 0x1275A, 0x12770): self.add('d5', c.d1)
        elif pc in (0x12734, 0x1273C, 0x12744, 0x1274C):
            c.word('d3', {0x12734:10000, 0x1273C:1000, 0x12744:100, 0x1274C:10}[pc])
            self.logic_flags(c.d3, 16)
        elif pc in (0x12738, 0x12740, 0x12748, 0x12750, 0x67278):
            self.push(following)
            following = FORMATTER if pc == 0x67278 else 0x12760
        elif pc in (0x1275E, 0x12780): following = self.pop()
        elif pc == 0x12762:
            divisor = c.d3 & 0xFFFF
            if not divisor: raise Boundary('divide_by_zero_vector5_not_executed')
            quotient, remainder = divmod(c.d0, divisor)
            self.divisions.append({'dividend': c.d0, 'divisor': divisor,
                                   'quotient': quotient, 'remainder': remainder,
                                   'overflow': quotient > 0xFFFF})
            # DIVU.W overflow leaves D0 unchanged and Z undefined, not stale.
            # C is always cleared; the ordinary next TST establishes Z again.
            self.carry = False
            self.zero = quotient == 0 if quotient <= 0xFFFF else None
            if quotient <= 0xFFFF: c.d0 = remainder << 16 | quotient
        elif pc == 0x12774:
            c.word('d4', 1)
            self.logic_flags(1, 16)
        elif pc == 0x1277E:
            c.d0 = ((c.d0 << 16) | (c.d0 >> 16)) & 0xFFFFFFFF
            self.logic_flags(c.d0, 32)
        elif pc in (0x67268, 0x6729C):
            c.d0 = b.read(0xFFFFF3C8 if pc == 0x67268 else 0xFFFFF3CC, 4)
            self.logic_flags(c.d0, 32)
        elif pc == 0x6726C:
            c.d1 = 0x4100
            self.logic_flags(c.d1, 32)
        elif pc in (0x67274, 0x67284): c.a6 = BUFFER
        elif pc == 0x6727E:
            b.write(0xFFFFD30C, 0x800C, 2)
            self.logic_flags(0x800C, 16)
        elif pc == 0x67288:
            self.logic_flags(b.read(c.a6, 2), 16)
            c.a6 = (c.a6 + 2) & 0xFFFFFFFF
        elif pc == 0x6728A:
            if self.condition('zero'): following = 0x67288
        elif pc == 0x6728C:
            # Address-register SUBQ updates all 32 bits even with .W spelling.
            c.a6 = (c.a6 - 2) & 0xFFFFFFFF
        elif pc in (0x6728E, 0x672EC):
            value = b.read(0xFFFFF3BE if pc == 0x6728E else 0xFFFFF3D4, 4)
            b.write(0xFFFFF3D4 if pc == 0x6728E else 0xFFFFF3BE, value, 4)
            self.logic_flags(value, 32)
        elif pc == 0x67294:
            b.write(0xFFFFF3BE, c.a6, 4)
            self.logic_flags(c.a6, 32)
        elif pc in (0x67338, 0x67346):
            c.d0 = 0
            self.logic_flags(0, 32)
        elif pc in (0x6733A, 0x67348):
            c.d0 = (c.d0 & 0xFFFFFF00) | b.read8(0xFFFFF374 if pc == 0x6733A else 0xFFFFF375)
            self.logic_flags(c.d0, 8)
        elif pc in (0x6733E, 0x6734C): self.add('d0', 0xB8 if pc == 0x6733E else 1)
        else:
            branches = {0x12718:0x1270E, 0x12726:0x12734, 0x12778:0x1277C,
                        0x67298:TIMED_READER, 0x672A0:0x6726C, 0x672F2:TIMED_READER,
                        0x67342:0x6726C, 0x67350:0x6726C}
            if pc not in branches: raise AssertionError(f'unimplemented guarded position {pc:06x}')
            following = branches[pc]
        c.pc = following
        self.executed[pc] += 1

    def run(self, *, stop=(TIMED_READER, 0x000206), max_steps=200000):
        uint(max_steps, 32, 'step budget')
        if not 0 < max_steps <= 1000000 or type(stop) is not tuple:
            raise ValueError('bounded positive budget and explicit stop tuple required')
        for pc in stop: uint(pc, 32, 'stop PC')
        status, reason = 'boundary', 'step_budget_not_closure'
        for _ in range(max_steps):
            if self.cpu.pc in stop:
                status, reason = 'requested_boundary', 'cpu_reached_requested_boundary'
                break
            try: self.step()
            except Boundary as error:
                reason = str(error)
                break
        else:
            if self.cpu.pc in stop:
                status, reason = 'requested_boundary', 'cpu_reached_requested_boundary'
        return {'status': status, 'reason': reason, 'registers': asdict(self.cpu),
                'executed_instructions': dict(sorted(self.executed.items())),
                'digit_reads': self.table_reads.copy(), 'divisions': self.divisions.copy(),
                'natural_use_confirmed': False, 'global_numeric_input_domain_closed': False,
                'ownership_bytes_added': 0, 'full_ccr_modelled': False}


def formula(rom, value, *, glyph_base=0x4100, blank=0):
    """Independent full-entry formula; no 999999 clamp, no shortened-entry claim.

    Caller provides unchanged canonical ROM data. D3's maximum quotient is42949,
    so it never wraps its word, but its signed table index can be negative.
    """
    uint(value, 32, 'value'); uint(glyph_base, 16, 'glyph base'); uint(blank, 16, 'blank')
    if type(rom) is not bytes or len(rom) != af.ROM_SIZE:
        raise ValueError('explicit 1 MiB ROM bytes required')
    first, rest = divmod(value, 100000)
    started = first != 0
    words = [((rom[TABLE + signed16(first)] + glyph_base) & 0xFFFF) if started else blank]
    for divisor in (10000, 1000, 100, 10):
        digit, rest = divmod(rest, divisor)
        started |= digit != 0
        words.append(((rom[TABLE + digit] + glyph_base) & 0xFFFF) if started else blank)
    words.append((rom[TABLE + rest] + glyph_base) & 0xFFFF)
    return words


def fixture(rom, value, *, entry=FORMATTER, d1=0x4100, d2=0, d3=0, d4=0, d5=0,
            outer_cursor=0x00092E86):
    """Disclosed zero-RAM fixture; not a natural-game capture or selector proof."""
    uint(value, 32, 'value'); uint(outer_cursor, 32, 'outer cursor')
    bus = Bus(rom, bytearray(65536))
    cpu = Registers(d0=value, d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, pc=entry)
    cpu.validate()
    bus.write(cpu.a7, 0x000206, 4)
    bus.write(0xFFFFF3C8, value, 4); bus.write(0xFFFFF3CC, value, 4)
    bus.write(0xFFFFF3BE, outer_cursor, 4)
    if entry in (0x67338, 0x67346):
        uint(value, 8, 'year/month byte')
        bus.ram[0xF374 if entry == 0x67338 else 0xF375] = value
    bus.events.clear()
    return Executor(bus, cpu), bus, cpu
