#!/usr/bin/env python3
"""Small, dependency-free Z80 decoder used by the conservative CFG mapper.

The decoder deliberately exposes structured control-flow and memory-reference
metadata.  It is not a linear-sweep disassembler and it does not decide which
bytes are code; callers must provide independently justified entry points.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class DecodeError(ValueError):
    """Raised when an instruction would extend beyond the supplied image."""


@dataclass(frozen=True)
class Instruction:
    address: int
    size: int
    raw: bytes
    mnemonic: str
    operand: str = ""
    flow_type: str = "linear"
    target: int | None = None
    conditional: bool = False
    terminates_block: bool = False
    memory_refs: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    io_refs: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def text(self) -> str:
        return f"{self.mnemonic} {self.operand}".rstrip()


REG = ("b", "c", "d", "e", "h", "l", "(hl)", "a")
RP = ("bc", "de", "hl", "sp")
RP2 = ("bc", "de", "hl", "af")
CC = ("nz", "z", "nc", "c", "po", "pe", "p", "m")
ALU = ("add a", "adc a", "sub", "sbc a", "and", "xor", "or", "cp")
ROT = ("rlc", "rrc", "rl", "rr", "sla", "sra", "sll", "srl")


def _need(data: bytes, start: int, count: int) -> None:
    if start < 0 or start + count > len(data):
        raise DecodeError(
            f"truncated Z80 instruction at 0x{start:04X}: need {count} byte(s)"
        )


def _u16(data: bytes, offset: int) -> int:
    _need(data, offset, 2)
    return data[offset] | (data[offset + 1] << 8)


def _s8(value: int) -> int:
    return value - 0x100 if value & 0x80 else value


def _hex8(value: int) -> str:
    return f"${value & 0xFF:02x}"


def _hex16(value: int) -> str:
    return f"${value & 0xFFFF:04x}"


def _index_disp(index: str, displacement: int) -> str:
    signed = _s8(displacement)
    if signed < 0:
        return f"({index}-${-signed:02x})"
    return f"({index}+${signed:02x})"


def _reg(code: int, index: str | None, displacement: int | None) -> str:
    if index is None:
        return REG[code]
    if code == 4:
        return f"{index}h"
    if code == 5:
        return f"{index}l"
    if code == 6:
        if displacement is None:
            return f"({index})"
        return _index_disp(index, displacement)
    return REG[code]


def _rp(code: int, index: str | None) -> str:
    if code == 2 and index:
        return index
    return RP[code]


def _rp2(code: int, index: str | None) -> str:
    if code == 2 and index:
        return index
    return RP2[code]


def _uses_index_displacement(opcode: int) -> bool:
    x = opcode >> 6
    y = (opcode >> 3) & 7
    z = opcode & 7
    if x == 0:
        return (z in (4, 5) and y == 6) or (z == 6 and y == 6)
    if x == 1:
        return opcode != 0x76 and (y == 6 or z == 6)
    if x == 2:
        return z == 6
    return False


def _base_immediate_count(opcode: int) -> int:
    """Return operand bytes after the opcode, excluding IX/IY displacement."""
    x = opcode >> 6
    y = (opcode >> 3) & 7
    z = opcode & 7
    q = y & 1
    if x == 0:
        if z == 0 and y >= 2:
            return 1
        if z == 1 and q == 0:
            return 2
        if z == 2 and (y >> 1) >= 2:
            return 2
        if z == 6:
            return 1
        return 0
    if x in (1, 2):
        return 0
    if z == 2:
        return 2
    if z == 3:
        if y == 0:
            return 2
        if y in (2, 3):
            return 1
        return 0
    if z == 4:
        return 2
    if z == 5 and q == 1 and (y >> 1) == 0:
        return 2
    if z == 6:
        return 1
    return 0


def _decode_cb(
    data: bytes,
    start: int,
    cursor: int,
    index: str | None,
    prefix_count: int,
) -> Instruction:
    if index:
        _need(data, cursor, 3)
        displacement = data[cursor + 1]
        opcode = data[cursor + 2]
        end = cursor + 3
        indexed_operand = _index_disp(index, displacement)
    else:
        _need(data, cursor, 2)
        displacement = None
        opcode = data[cursor + 1]
        end = cursor + 2
        indexed_operand = ""
    x = opcode >> 6
    y = (opcode >> 3) & 7
    z = opcode & 7
    if index:
        if x == 0:
            operand = indexed_operand
            if z != 6:
                operand += f",{REG[z]}"
            mnemonic = ROT[y]
        elif x == 1:
            mnemonic = "bit"
            operand = f"{y},{indexed_operand}"
        else:
            mnemonic = "res" if x == 2 else "set"
            operand = f"{y},{indexed_operand}"
            if z != 6:
                operand += f",{REG[z]}"
    else:
        if x == 0:
            mnemonic = ROT[y]
            operand = REG[z]
        elif x == 1:
            mnemonic = "bit"
            operand = f"{y},{REG[z]}"
        else:
            mnemonic = "res" if x == 2 else "set"
            operand = f"{y},{REG[z]}"
    return Instruction(
        address=start,
        size=end - start,
        raw=data[start:end],
        mnemonic=mnemonic,
        operand=operand,
        details={
            "opcode": opcode,
            "prefix": "cb",
            "index": index,
            "prefix_count": prefix_count,
            "displacement": _s8(displacement) if displacement is not None else None,
        },
    )

def _decode_ed(
    data: bytes,
    start: int,
    cursor: int,
    index: str | None,
    prefix_count: int,
) -> Instruction:
    _need(data, cursor, 2)
    opcode = data[cursor + 1]
    x = opcode >> 6
    y = (opcode >> 3) & 7
    z = opcode & 7
    p = y >> 1
    q = y & 1
    size_after_ed = 2
    mnemonic = "nop"
    operand = ""
    flow_type = "linear"
    terminates = False
    refs: list[dict[str, Any]] = []
    io_refs: list[dict[str, Any]] = []
    immediate16: int | None = None

    if x == 1:
        if z == 0:
            mnemonic = "in"
            operand = f"{REG[y] if y != 6 else 'f'},(c)"
            io_refs.append({"direction": "read", "port": None, "addressing": "c"})
        elif z == 1:
            mnemonic = "out"
            operand = f"(c),{REG[y] if y != 6 else '$00'}"
            io_refs.append({"direction": "write", "port": None, "addressing": "c"})
        elif z == 2:
            mnemonic = "adc" if q else "sbc"
            operand = f"hl,{RP[p]}"
        elif z == 3:
            _need(data, cursor, 4)
            size_after_ed = 4
            immediate16 = _u16(data, cursor + 2)
            mnemonic = "ld"
            if q:
                operand = f"{RP[p]},({_hex16(immediate16)})"
                direction = "read"
            else:
                operand = f"({_hex16(immediate16)}),{RP[p]}"
                direction = "write"
            refs.append(
                {
                    "address": immediate16,
                    "direction": direction,
                    "width": 2,
                    "addressing": "absolute16",
                }
            )
        elif z == 4:
            mnemonic = "neg"
        elif z == 5:
            mnemonic = "reti" if y == 1 else "retn"
            flow_type = "interrupt_return"
            terminates = True
        elif z == 6:
            mnemonic = "im"
            operand = str((0, 0, 1, 2, 0, 0, 1, 2)[y])
        else:
            operations = (
                ("ld", "i,a"),
                ("ld", "r,a"),
                ("ld", "a,i"),
                ("ld", "a,r"),
                ("rrd", ""),
                ("rld", ""),
                ("nop", ""),
                ("nop", ""),
            )
            mnemonic, operand = operations[y]
    elif x == 2 and y >= 4 and z <= 3:
        rows = (
            ("ldi", "cpi", "ini", "outi"),
            ("ldd", "cpd", "ind", "outd"),
            ("ldir", "cpir", "inir", "otir"),
            ("lddr", "cpdr", "indr", "otdr"),
        )
        mnemonic = rows[y - 4][z]
        if z in (2, 3):
            io_refs.append(
                {
                    "direction": "read" if z == 2 else "write",
                    "port": None,
                    "addressing": "c_block",
                }
            )
    else:
        mnemonic = "db"
        operand = f"$ed,{_hex8(opcode)}"

    end = cursor + size_after_ed
    return Instruction(
        address=start,
        size=end - start,
        raw=data[start:end],
        mnemonic=mnemonic,
        operand=operand,
        flow_type=flow_type,
        terminates_block=terminates,
        memory_refs=tuple(refs),
        io_refs=tuple(io_refs),
        details={
            "opcode": opcode,
            "prefix": "ed",
            "index_prefix_ignored": index,
            "prefix_count": prefix_count,
            "immediate16": immediate16,
        },
    )


def decode_instruction(data: bytes, address: int) -> Instruction:
    """Decode one Z80 instruction at *address* without classifying it as code."""
    _need(data, address, 1)
    cursor = address
    index: str | None = None
    prefix_count = 0
    while cursor < len(data) and data[cursor] in (0xDD, 0xFD):
        index = "ix" if data[cursor] == 0xDD else "iy"
        prefix_count += 1
        cursor += 1
        if prefix_count > 16:
            raise DecodeError(f"excessive DD/FD prefix run at 0x{address:04X}")
    _need(data, cursor, 1)
    opcode = data[cursor]
    if opcode == 0xCB:
        return _decode_cb(data, address, cursor, index, prefix_count)
    if opcode == 0xED:
        return _decode_ed(data, address, cursor, index, prefix_count)

    x = opcode >> 6
    y = (opcode >> 3) & 7
    z = opcode & 7
    p = y >> 1
    q = y & 1
    uses_displacement = index is not None and _uses_index_displacement(opcode)
    displacement: int | None = None
    operands_at = cursor + 1
    if uses_displacement:
        _need(data, operands_at, 1)
        displacement = data[operands_at]
        operands_at += 1
    immediate_count = _base_immediate_count(opcode)
    _need(data, operands_at, immediate_count)
    end = operands_at + immediate_count
    raw = data[address:end]
    imm8 = data[operands_at] if immediate_count >= 1 else None
    imm16 = _u16(data, operands_at) if immediate_count == 2 else None

    mnemonic = "db"
    operand = _hex8(opcode)
    flow_type = "linear"
    target: int | None = None
    conditional = False
    terminates = False
    refs: list[dict[str, Any]] = []
    io_refs: list[dict[str, Any]] = []
    immediate_kind: str | None = None

    if x == 0:
        if z == 0:
            if y == 0:
                mnemonic, operand = "nop", ""
            elif y == 1:
                mnemonic, operand = "ex", "af,af'"
            else:
                assert imm8 is not None
                target = (end + _s8(imm8)) & 0xFFFF
                if y == 2:
                    mnemonic, operand = "djnz", _hex16(target)
                    flow_type, conditional = "djnz", True
                elif y == 3:
                    mnemonic, operand = "jr", _hex16(target)
                    flow_type, terminates = "relative_jump", True
                else:
                    mnemonic, operand = "jr", f"{CC[y - 4]},{_hex16(target)}"
                    flow_type, conditional = "conditional_relative", True
        elif z == 1:
            if q == 0:
                assert imm16 is not None
                mnemonic, operand = "ld", f"{_rp(p, index)},{_hex16(imm16)}"
                immediate_kind = "pointer_or_value"
            else:
                mnemonic, operand = "add", f"{_rp(2, index)},{_rp(p, index)}"
        elif z == 2:
            if q == 0:
                if p == 0:
                    mnemonic, operand = "ld", "(bc),a"
                elif p == 1:
                    mnemonic, operand = "ld", "(de),a"
                elif p == 2:
                    assert imm16 is not None
                    mnemonic, operand = "ld", f"({_hex16(imm16)}),{_rp(2, index)}"
                    refs.append({"address": imm16, "direction": "write", "width": 2, "addressing": "absolute16"})
                else:
                    assert imm16 is not None
                    mnemonic, operand = "ld", f"({_hex16(imm16)}),a"
                    refs.append({"address": imm16, "direction": "write", "width": 1, "addressing": "absolute16"})
            else:
                if p == 0:
                    mnemonic, operand = "ld", "a,(bc)"
                elif p == 1:
                    mnemonic, operand = "ld", "a,(de)"
                elif p == 2:
                    assert imm16 is not None
                    mnemonic, operand = "ld", f"{_rp(2, index)},({_hex16(imm16)})"
                    refs.append({"address": imm16, "direction": "read", "width": 2, "addressing": "absolute16"})
                else:
                    assert imm16 is not None
                    mnemonic, operand = "ld", f"a,({_hex16(imm16)})"
                    refs.append({"address": imm16, "direction": "read", "width": 1, "addressing": "absolute16"})
        elif z == 3:
            mnemonic = "dec" if q else "inc"
            operand = _rp(p, index)
        elif z == 4:
            mnemonic, operand = "inc", _reg(y, index, displacement)
        elif z == 5:
            mnemonic, operand = "dec", _reg(y, index, displacement)
        elif z == 6:
            assert imm8 is not None
            mnemonic, operand = "ld", f"{_reg(y, index, displacement)},{_hex8(imm8)}"
        else:
            mnemonic, operand = (
                ("rlca", ""), ("rrca", ""), ("rla", ""), ("rra", ""),
                ("daa", ""), ("cpl", ""), ("scf", ""), ("ccf", ""),
            )[y]
    elif x == 1:
        if opcode == 0x76:
            mnemonic, operand = "halt", ""
            flow_type, terminates = "halt", True
        else:
            mnemonic = "ld"
            # DD/FD 66/6E/74/75 use ordinary H/L alongside indexed memory.
            # Index halves substitute H/L only in register-only LD forms.
            # Zilog UM0080, LD r,(IX/IY+d) and LD (IX/IY+d),r.
            destination_index = None if index and z == 6 and y != 6 else index
            source_index = None if index and y == 6 and z != 6 else index
            operand = (
                f"{_reg(y, destination_index, displacement)},"
                f"{_reg(z, source_index, displacement)}"
            )
    elif x == 2:
        mnemonic = ALU[y]
        operand = _reg(z, index, displacement)
    else:
        if z == 0:
            mnemonic, operand = "ret", CC[y]
            flow_type, conditional = "conditional_return", True
        elif z == 1:
            if q == 0:
                mnemonic, operand = "pop", _rp2(p, index)
            elif p == 0:
                mnemonic, operand = "ret", ""
                flow_type, terminates = "return", True
            elif p == 1:
                mnemonic, operand = "exx", ""
            elif p == 2:
                mnemonic, operand = "jp", f"({_rp(2, index)})"
                flow_type, terminates = "indirect_jump", True
            else:
                mnemonic, operand = "ld", f"sp,{_rp(2, index)}"
        elif z == 2:
            assert imm16 is not None
            mnemonic, operand = "jp", f"{CC[y]},{_hex16(imm16)}"
            flow_type, target, conditional = "conditional_jump", imm16, True
        elif z == 3:
            if y == 0:
                assert imm16 is not None
                mnemonic, operand = "jp", _hex16(imm16)
                flow_type, target, terminates = "jump", imm16, True
            elif y == 2:
                assert imm8 is not None
                mnemonic, operand = "out", f"({_hex8(imm8)}),a"
                io_refs.append({"direction": "write", "port": imm8, "addressing": "immediate_low_dynamic_high"})
            elif y == 3:
                assert imm8 is not None
                mnemonic, operand = "in", f"a,({_hex8(imm8)})"
                io_refs.append({"direction": "read", "port": imm8, "addressing": "immediate_low_dynamic_high"})
            elif y == 4:
                mnemonic, operand = "ex", f"(sp),{_rp(2, index)}"
            elif y == 5:
                mnemonic, operand = "ex", "de,hl"
            elif y == 6:
                mnemonic, operand = "di", ""
            elif y == 7:
                mnemonic, operand = "ei", ""
            else:  # CB is handled before reaching this branch.
                mnemonic, operand = "db", _hex8(opcode)
        elif z == 4:
            assert imm16 is not None
            mnemonic, operand = "call", f"{CC[y]},{_hex16(imm16)}"
            flow_type, target, conditional = "conditional_call", imm16, True
        elif z == 5:
            if q == 0:
                mnemonic, operand = "push", _rp2(p, index)
            elif p == 0:
                assert imm16 is not None
                mnemonic, operand = "call", _hex16(imm16)
                flow_type, target = "call", imm16
            else:  # DD/ED/FD are handled before reaching this branch.
                mnemonic, operand = "db", _hex8(opcode)
        elif z == 6:
            assert imm8 is not None
            mnemonic, operand = ALU[y], _hex8(imm8)
        else:
            target = y * 8
            mnemonic, operand = "rst", _hex16(target)
            flow_type = "rst"

    return Instruction(
        address=address,
        size=end - address,
        raw=raw,
        mnemonic=mnemonic,
        operand=operand,
        flow_type=flow_type,
        target=target,
        conditional=conditional,
        terminates_block=terminates,
        memory_refs=tuple(refs),
        io_refs=tuple(io_refs),
        details={
            "opcode": opcode,
            "prefix": None,
            "index": index,
            "prefix_count": prefix_count,
            "displacement": _s8(displacement) if displacement is not None else None,
            "immediate8": imm8 if immediate_count == 1 else None,
            "immediate16": imm16,
            "immediate_kind": immediate_kind,
        },
    )
