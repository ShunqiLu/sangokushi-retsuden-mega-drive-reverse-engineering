"""Build explicit generated code, verify actual boundaries, select code only.

The assembler's sparse zero-fill never becomes an image block. Original ROMs,
reference assembly and prebuilt objects are not inputs. Tool/output locations
are supplied by the caller, rather than tied to a private research directory.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import struct
import subprocess
import time
from typing import Mapping


@dataclass(frozen=True)
class Toolchains:
    m68k_bin: Path
    z80_bin: Path


class NativeBuildError(RuntimeError):
    """A failed native attempt is retained at its fresh output directory."""

    def __init__(self, directory: Path, receipt: dict):
        super().__init__(f'native attempt failed; evidence retained at {directory}')
        self.directory = directory
        self.receipt = receipt


def fresh_output(path: Path) -> Path:
    """Reject existing targets/reparse ancestors; never remove or overwrite."""
    raw = str(path)
    if raw.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in raw[2:]:
        raise ValueError('UNC, device and alternate-stream paths are refused')
    absolute = path.absolute()
    for ancestor in (absolute, *absolute.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ValueError('output through a reparse point is refused')
    resolved = absolute.resolve(strict=False)
    if resolved == Path(resolved.anchor) or resolved.exists():
        raise ValueError('an absent, dedicated output directory is required')
    return resolved


def _wsl_path(path: Path) -> str:
    resolved = path.resolve()
    if len(resolved.drive) != 2 or resolved.drive[1] != ':':
        raise ValueError('local absolute Windows drive paths required by WSL')
    return '/mnt/' + resolved.drive[0].lower() + '/' + '/'.join(resolved.parts[1:])


def _elf_symbols(data: bytes, image: bytes) -> tuple[dict[str, tuple[int, int]], int]:
    """Read linked ELF32 big-endian M68K text/symbols, without subprocesses."""
    if type(data) is not bytes or not 52 <= len(data) <= 16_000_000:
        raise ValueError('bounded actual ELF bytes required')
    if data[:7] != b'\x7fELF\x01\x02\x01':
        raise ValueError('ELF32 big-endian version1 required')
    header = struct.unpack_from('>HHIIIIIHHHHHH', data, 16)
    if header[:3] != (2, 4, 1) or header[7] != 52 or header[10] != 40:
        raise ValueError('linked M68K ELF identity differs')
    offset, count, names_index = header[5], header[11], header[12]
    if not 1 <= count <= 64 or names_index >= count or offset + count * 40 > len(data):
        raise ValueError('ELF section table is outside the object')
    sections = [struct.unpack_from('>IIIIIIIIII', data, offset + i * 40) for i in range(count)]

    def content(section):
        start, size = section[4:6]
        if start + size > len(data):
            raise ValueError('ELF section contents are outside the object')
        return data[start:start + size]

    def string(table, start):
        end = table.find(b'\0', start)
        if not 0 <= start < len(table) or end < 0:
            raise ValueError('ELF string bounds/termination differ')
        return table[start:end].decode('ascii')

    names = content(sections[names_index])
    named = {string(names, section[0]): (i, section) for i, section in enumerate(sections)}
    if len(named) != count or '.text' not in named or '.symtab' not in named:
        raise ValueError('distinct text/symbol sections required')
    text_index, text = named['.text']
    if text[3] != 0 or content(text) != image:
        raise ValueError('ELF text address or objcopy image differs')
    if any(section[1] in (4, 9) and section[5] for section in sections):
        raise ValueError('unresolved ELF relocation section')
    if any(name in named and named[name][1][5] for name in ('.data', '.bss')):
        raise ValueError('nonempty data/BSS is not code image authority')
    table = named['.symtab'][1]
    if table[9] != 16 or table[5] % 16 or table[6] >= count:
        raise ValueError('malformed ELF symbol table')
    strings, entries, result = content(sections[table[6]]), content(table), {}
    for start in range(0, len(entries), 16):
        name, value, size, info, other, section = struct.unpack_from('>IIIBBH', entries, start)
        label = string(strings, name)
        if not label:
            continue
        if section == 0:
            raise ValueError('undefined native symbol: ' + label)
        identity = (value, section)
        if label in result and result[label] != identity:
            raise ValueError('conflicting native symbol: ' + label)
        result[label] = identity
    return result, text_index


def _validate_group(group: Mapping) -> list[dict]:
    if not isinstance(group, Mapping) or group.get('cpu') not in ('m68k', 'z80'):
        raise ValueError('an explicit supported CPU group is required')
    if type(group.get('name')) is not str or not re.fullmatch(r'[a-z][a-z0-9_]{0,100}', group['name']):
        raise ValueError('a simple stable code-group ID is required')
    assembly = group.get('assembly')
    if type(assembly) is not str or not 1 <= len(assembly) <= 8_000_000:
        raise ValueError('bounded explicit generated assembly required')
    assembly.encode('ascii')
    rows = group.get('instruction_rows')
    if type(rows) not in (list, tuple) or not rows:
        raise ValueError('complete explicit instruction rows are required')
    logical_end = 0
    positions = set()
    for row in rows:
        logical, physical, width = (row[key] for key in ('logical_pc', 'physical_pc', 'width'))
        if (any(type(value) is not int for value in (logical, physical, width)) or
                logical < logical_end or not 0 <= physical < physical + width <= 0x100000 or
                not 1 <= width <= (10 if group['cpu'] == 'm68k' else 4)):
            raise ValueError('invalid/overlapping instruction extent')
        if group['cpu'] == 'm68k' and (width % 2 or logical % 2 or physical % 2):
            raise ValueError('unaligned M68K instruction extent')
        for key in ('start_symbol', 'end_symbol'):
            if type(row.get(key)) is not str or not re.fullmatch(r'[A-Za-z_.][A-Za-z0-9_.$]*', row[key]):
                raise ValueError('actual start/end symbols required')
        extent = set(range(physical, physical + width))
        if extent & positions:
            raise ValueError('a code group repeats a physical authority')
        positions |= extent
        logical_end = logical + width
    if type(group.get('expected_symbols')) is not dict:
        raise ValueError('explicit expected native symbol map required')
    return list(rows)


def assemble_group(group: Mapping, directory: Path, tools: Toolchains) -> dict:
    """Return verified instruction blocks and a retained actual-native receipt."""
    rows = _validate_group(group)
    output = fresh_output(directory)
    output.mkdir(parents=True)
    assembly, obj, elf, binary = [output / name for name in ('generated.s', 'code.o', 'code.elf', 'code.bin')]
    assembly.write_text(group['assembly'], encoding='ascii', newline='\n')
    for name, source in group.get('sources', {}).items():
        if type(name) is not str or Path(name).name != name or type(source) is not str:
            raise ValueError('simple source-snapshot keys and explicit text required')
        (output / ('source-' + name)).write_text(source, encoding='utf-8', newline='\n')
    receipt = dict(name=group['name'], cpu=group['cpu'], commands=[], child_exits=[],
                   parent_exit=None, original_generation_input=False,
                   precompiled_generation_input=False, complete_ROM=False, complete_CPU=False)

    def execute(argv):
        began = time.monotonic()
        process = subprocess.run(argv, capture_output=True, text=True, encoding='utf-8')
        receipt['commands'].append(dict(command=argv, exit_code=process.returncode,
                                       stdout=process.stdout, stderr=process.stderr,
                                       elapsed_seconds=time.monotonic() - began))
        receipt['child_exits'].append(process.returncode)
        if process.returncode:
            raise RuntimeError('native child failed: ' + process.stderr)

    try:
        if group['cpu'] == 'm68k':
            prefix = _wsl_path(tools.m68k_bin)
            execute(['wsl.exe', '--exec', prefix + '/m68k-elf-as', '-m68000', '-o', _wsl_path(obj), _wsl_path(assembly)])
            execute(['wsl.exe', '--exec', prefix + '/m68k-elf-ld', '-Ttext=0', '--entry=0', '-o', _wsl_path(elf), _wsl_path(obj)])
            execute(['wsl.exe', '--exec', prefix + '/m68k-elf-objcopy', '-O', 'binary', '-j', '.text', _wsl_path(elf), _wsl_path(binary)])
            image = binary.read_bytes()
            symbols, section = _elf_symbols(elf.read_bytes(), image)
            for label, address in group['expected_symbols'].items():
                if type(address) is not int or symbols.get(label) != (address, section):
                    raise ValueError('actual expected boundary differs: ' + label)
            for row in rows:
                if (symbols.get(row['start_symbol']) != (row['logical_pc'], section) or
                        symbols.get(row['end_symbol']) != (row['logical_pc'] + row['width'], section)):
                    raise ValueError('actual instruction placement/width differs')
            receipt['unresolved_relocations'] = 0
        else:
            prefix = _wsl_path(tools.z80_bin)
            execute(['wsl.exe', '--exec', prefix + '/z80-unknown-coff-as', '-march=z80', '-o', _wsl_path(obj), _wsl_path(assembly)])
            execute(['wsl.exe', '--exec', prefix + '/z80-unknown-coff-objcopy', '-O', 'binary', '-j', '.text', _wsl_path(obj), _wsl_path(binary)])
            image = binary.read_bytes()
            # Existing pure COFF reader is shared platform verification, not a
            # code/ROM generator. It checks actual start/end labels and gaps.
            from .z80_coff import verify_object
            actual = verify_object(group['audio_unit'], group['descriptor'], obj.read_bytes(), image)
            receipt['unresolved_relocations'] = actual['unresolved_relocations']
        logical_positions = {pc for row in rows for pc in range(row['logical_pc'], row['logical_pc'] + row['width'])}
        if len(image) != max(logical_positions) + 1:
            raise ValueError('actual code image extent differs')
        if any(value for pc, value in enumerate(image) if pc not in logical_positions):
            raise ValueError('sparse gap contains undeclared noninstruction bytes')
        blocks = [dict(start=row['physical_pc'], end=row['physical_pc'] + row['width'],
                       data=image[row['logical_pc']:row['logical_pc'] + row['width']],
                       owner=group['name'], role=group['cpu'] + '_code') for row in rows]
        receipt.update(parent_exit=0, instruction_count=len(rows),
                       instruction_bytes=sum(row['width'] for row in rows),
                       sparse_bytes_excluded=len(image) - len(logical_positions),
                       actual_boundaries_verified=True)
        return dict(blocks=blocks, receipt=receipt)
    except Exception as error:
        receipt.update(parent_exit=1, error=str(error))
        raise NativeBuildError(output, receipt) from error
    finally:
        (output / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
