"""Canonical mnemonic extraction; Capstone is used only for explicit source export."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.code_analysis.m68k_code_map import load_capstone
from tools.m68k_build.m68k_build import inventory


def operands(text):
    depth, start, result = 0, 0, []
    for index, char in enumerate(text):
        if char == "(": depth += 1
        elif char == ")": depth -= 1
        elif char == "," and depth == 0:
            result.append(text[start:index].strip()); start = index + 1
    if text: result.append(text[start:].strip())
    return result


def format_instruction(instruction):
    pieces = operands(instruction.op_str)
    for index, (piece, operand) in enumerate(zip(pieces, instruction.operands)):
        if instruction.mnemonic == "moveq" and index == 0:
            value = operand.imm & 255
            piece = f"#{value if value < 128 else value - 256}"
        elif operand.address_mode == 19:
            piece = f"(. + {2 + operand.br_disp.disp})"
        elif operand.address_mode in (11, 12):
            # GAS numeric PC-relative operands are encoded displacements.
            piece = re.sub(r"^[^\(]+", str(operand.mem.disp), piece)
        piece = re.sub(r"\$([0-9a-fA-F]+)\.(w|l)", r"0x\1:\2", piece)
        piece = re.sub(r"\$([0-9a-fA-F]+)", r"0x\1", piece)
        piece = re.sub(r"\b(d[0-7]|a[0-7]|pc|sr|ccr|usp)\b", r"%\1", piece)
        pieces[index] = piece
    mnemonic = "exg" if instruction.mnemonic == "exg.l" else instruction.mnemonic
    if mnemonic.split('.')[0] in {"btst", "bset", "bclr", "bchg"} and instruction.operands[-1].address_mode == 1:
        mnemonic = mnemonic.split('.')[0] + '.l'
    return mnemonic + (" " + ",".join(pieces) if pieces else "")


def selected(rom):
    rows, _ = inventory(rom)
    c = load_capstone()
    decoder = c.Cs(c.CS_ARCH_M68K, c.CS_MODE_BIG_ENDIAN | c.CS_MODE_M68K_000)
    decoder.detail = True
    result = []
    for row in rows:
        address, size = int(row["address"]), int(row["size"])
        raw = bytes.fromhex(row["bytes"])
        decoded = list(decoder.disasm(raw, address, count=1))
        if len(decoded) != 1 or decoded[0].size != size:
            raise ValueError('canonical decoder no longer agrees with pinned instruction extent')
        instruction = decoded[0]
        result.append(instruction)
    return result


def assembly(rom):
    instructions = selected(rom)
    lines = ['| Canonical mnemonic reconstruction; fixed addresses and instruction extents.',
             '| Editable instructions; no original-ROM bytes are emitted by directives.',
             '.cpu 68000', '.section .text', '_start:']
    for instruction in instructions:
        lines.extend([f'.org 0x{instruction.address:X}', f'| {instruction.bytes.hex()} {instruction.op_str}'.rstrip(),
                      f'm68k_{instruction.address:06x}:', '        ' + format_instruction(instruction),
                      f'm68k_{instruction.address:06x}_end:'])
    return ('\n'.join(lines)+'\n').encode('utf-8')
