"""Complete retained storage ABI, separate from Scene and cartridge payloads.

D0..D7 and A0..A6 name the physical carriers at this boundary. Business cores
give their local roles readable names; no unobserved register or SP is filled
with zero. The caller owns its outer return LONG. Child calls own only their
original internal continuation slots. SRAM remains the existing StorageState
odd-BYTE cartridge bus and is never merged into ordinary main RAM.
"""
from dataclasses import dataclass, replace
from .domain import StorageState, Long, Word, Boundary, checked_state, uint, u32, low16, s16


@dataclass(frozen=True)
class StorageFrame:
    d0: Long
    d1: Long
    d2: Long
    d3: Long
    d4: Long
    d5: Long
    d6: Long
    d7: Long
    a0: Long
    a1: Long
    a2: Long
    a3: Long
    a4: Long
    a5: Long
    a6: Long
    stack_cursor: Long
    status_word: Word

    def validate(self, state: StorageState):
        checked_state(state)
        for name in ('d0','d1','d2','d3','d4','d5','d6','d7',
                     'a0','a1','a2','a3','a4','a5','a6','stack_cursor'):
            uint(getattr(self, name), 32, 'complete storage ' + name)
        uint(self.status_word, 16, 'complete storage SR-X')
        if self.stack_cursor & 1:
            raise Boundary('original even storage stack cursor required')
        return self


def storage_entry(state: StorageState, frame: StorageFrame) -> StorageFrame:
    if type(frame) is not StorageFrame:
        raise Boundary('complete explicit StorageFrame required; no synthetic zero entry')
    frame.validate(state)
    state.sr = frame.status_word
    return frame


def storage_replace(frame: StorageFrame, **values) -> StorageFrame:
    return replace(frame, **values)


def storage_logic(state: StorageState, frame: StorageFrame, value: Long,
                  bits: int) -> StorageFrame:
    mask = (1 << bits) - 1
    value &= mask
    flags = (8 if value & (1 << (bits - 1)) else 0) | (4 if value == 0 else 0)
    status = (frame.status_word & 0xFFF0) | flags
    state.sr = status
    return replace(frame, status_word=status)


def storage_move(state: StorageState, frame: StorageFrame, role: str,
                 value: Long, bits: int) -> StorageFrame:
    mask = (1 << bits) - 1
    retained = (getattr(frame, role) & ~mask) | (value & mask)
    frame = replace(frame, **{role: retained})
    return storage_logic(state, frame, value, bits)


def storage_address(frame: StorageFrame, role: str, address: Long) -> StorageFrame:
    return replace(frame, **{role: u32(address)})


def storage_address_step(frame: StorageFrame, role: str, amount: int) -> StorageFrame:
    # MOVEA/LEA/ADDA and ADDQ to An do not alter the condition codes.
    return storage_address(frame, role, getattr(frame, role) + amount)


def storage_read_next(state: StorageState, frame: StorageFrame, role: str,
                      size: int) -> tuple:
    value = state.read(getattr(frame, role), size)
    return storage_address_step(frame, role, size), value


def storage_write(state: StorageState, frame: StorageFrame, address: Long,
                  size: int, value: Long) -> StorageFrame:
    state.write(u32(address), size, value & ((1 << (size * 8)) - 1))
    return storage_logic(state, frame, value, size * 8)


def storage_write_next(state: StorageState, frame: StorageFrame, role: str,
                       size: int, value: Long) -> StorageFrame:
    address = getattr(frame, role)
    frame = storage_write(state, frame, address, size, value)
    return storage_address_step(frame, role, size)


def storage_clear_memory(state: StorageState, frame: StorageFrame,
                         address: Long, size: int) -> StorageFrame:
    # 68000 CLR has a real prior DATA read, including on the SRAM lane.
    state.read(u32(address), size)
    return storage_write(state, frame, address, size, 0)


def storage_binary(state: StorageState, frame: StorageFrame, role: str,
                   value: Long, bits: int, operation: str) -> StorageFrame:
    current = getattr(frame, role)
    if operation == 'and':
        result = current & value
    elif operation == 'or':
        result = current | value
    else:
        raise ValueError('closed original storage AND/OR operation required')
    return storage_move(state, frame, role, result, bits)


def storage_arithmetic(state: StorageState, frame: StorageFrame, role: str,
                       value: Long, bits: int, subtract: bool = False,
                       compare: bool = False) -> StorageFrame:
    mask = (1 << bits) - 1
    left, right = getattr(frame, role) & mask, value & mask
    result = (left - right if subtract else left + right) & mask
    sign = 1 << (bits - 1)
    carry = right > left if subtract else left + right > mask
    overflow = bool(((left ^ right) if subtract else ~(left ^ right))
                    & (left ^ result) & sign)
    flags = (8 if result & sign else 0) | (4 if result == 0 else 0)
    flags |= (2 if overflow else 0) | int(carry)
    status = ((frame.status_word & 0xFFF0) if compare else
              (frame.status_word & 0xFFE0) | (16 if carry else 0)) | flags
    state.sr = status
    values = dict(status_word=status)
    if not compare:
        values[role] = (getattr(frame, role) & ~mask) | result
    return replace(frame, **values)


def storage_compare_value(state: StorageState, frame: StorageFrame, left: Long,
                          right: Long, bits: int) -> StorageFrame:
    # Memory comparisons must not overwrite any observed data carrier.
    original = frame.d0
    frame = replace(frame, d0=left)
    frame = storage_arithmetic(state, frame, 'd0', right, bits, True, True)
    return replace(frame, d0=original)


def storage_shift(state: StorageState, frame: StorageFrame, role: str,
                  count: int, bits: int, right: bool = False,
                  rotate: bool = False) -> StorageFrame:
    mask = (1 << bits) - 1
    initial = getattr(frame, role) & mask
    steps = count & 63
    value, carry = initial, 0
    for _ in range(steps):
        if right:
            carry = value & 1
            value >>= 1
            if rotate:
                value |= carry << (bits - 1)
        else:
            carry = (value >> (bits - 1)) & 1
            value = (value << 1) & mask
    frame = storage_move(state, frame, role, value, bits)
    status = frame.status_word | carry
    if steps and not rotate:
        status = (status & 0xFFEF) | (carry << 4)
    state.sr = status
    return replace(frame, status_word=status)


def storage_swap(state: StorageState, frame: StorageFrame,
                 role: str) -> StorageFrame:
    value = getattr(frame, role)
    return storage_move(state, frame, role, u32((value << 16) | (value >> 16)), 32)


def storage_multiply(state: StorageState, frame: StorageFrame, role: str,
                     factor: Word) -> StorageFrame:
    return storage_move(state, frame, role, low16(getattr(frame, role)) * low16(factor), 32)


def storage_divide(state: StorageState, frame: StorageFrame, role: str,
                   divisor: Word) -> StorageFrame:
    divisor = low16(divisor)
    if divisor == 0:
        raise Boundary('original storage DIVU zero-divisor exception, no fake quotient')
    numerator = getattr(frame, role)
    quotient, remainder = divmod(numerator, divisor)
    if quotient > 0xFFFF:
        # The original overflow leaves the carrier unchanged. Undefined N/Z
        # cannot be invented as a successful complete observation.
        raise Boundary('original storage DIVU overflow has unobserved N/Z')
    frame = replace(frame, **{role: (remainder << 16) | quotient})
    return storage_logic(state, frame, quotient, 16)


def storage_dbra(frame: StorageFrame, role: str) -> tuple:
    value = (low16(getattr(frame, role)) - 1) & 0xFFFF
    frame = replace(frame, **{role: (getattr(frame, role) & 0xFFFF0000) | value})
    return frame, value != 0xFFFF


def storage_call(state: StorageState, frame: StorageFrame, callee,
                 continuation: Long) -> StorageFrame:
    frame = storage_entry(state, frame)
    entered = replace(frame, stack_cursor=u32(frame.stack_cursor - 4))
    state.write(entered.stack_cursor, 4, uint(continuation, 32, 'actual storage continuation'))
    returned = storage_entry(state, callee(state, entered))
    observed = state.read(returned.stack_cursor, 4)
    if observed != continuation:
        raise Boundary('actual storage child RTS target differs; no host-stack restoration')
    return replace(returned, stack_cursor=u32(returned.stack_cursor + 4))


def storage_legacy_entry(state: StorageState, entry_frame) -> StorageFrame:
    """Old scalar arguments cannot supply missing upper carriers, SR or SP."""
    return storage_entry(state, entry_frame)
