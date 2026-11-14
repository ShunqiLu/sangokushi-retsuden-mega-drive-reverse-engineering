"""读取汇编指令与布局，按标签生成供交叉工具使用的源码。"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import re


FORMAT = 'g5510-owned-assembly-layout-v1'
UNIT_FORMAT = 'g5510-owned-instruction-extents-v1'
MAX_TEXT = 8_000_000
M68K_MNEMONICS = frozenset(('abcd add adda addi addq addx and andi asl asr bchg bclr '
    'bra bset bsr btst chk clr cmp cmpa cmpi cmpm dbra divs divu eor eori exg ext '
    'illegal jmp jsr lea link lsl lsr move movea movem movep moveq muls mulu nbcd '
    'neg negx nop not or ori pea reset rol ror roxl roxr rte rtr rts sbcd stop sub '
    'suba subi subq subx swap tas trap trapv tst unlk').split()) | frozenset(
    stem + condition for stem in ('b', 'db', 's')
    for condition in ('t', 'f', 'hi', 'ls', 'cc', 'hs', 'cs', 'lo', 'ne', 'eq',
        'vc', 'vs', 'pl', 'mi', 'ge', 'lt', 'gt', 'le'))
Z80_MNEMONICS = frozenset(('adc add and bit call ccf cp cpd cpdr cpi cpir cpl daa dec '
    'di djnz ei ex exx halt im in inc ind indr ini inir jp jr ld ldd lddr ldi ldir '
    'neg nop or otdr otir out outd outi pop push res ret reti retn rl rla rlc rlca '
    'rld rr rra rrc rrca rrd rst sbc scf set sla sll sra srl sub xor').split())


def integer(value, minimum, maximum, label):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError('exact bounded integer required: ' + label)
    return value


def ordinary_root(path: Path, label: str) -> Path:
    if not isinstance(path, Path):
        raise ValueError('explicit Path required: ' + label)
    raw = str(path)
    if raw.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in raw[2:]:
        raise ValueError('UNC/device/alternate-stream path refused: ' + label)
    absolute = path.absolute()
    for ancestor in (absolute, *absolute.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ValueError('source through reparse point refused: ' + label)
    root = absolute.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('existing explicit source directory required: ' + label)
    return root


def member(root: Path, name: str) -> Path:
    if type(name) is not str or '\\' in name:
        raise ValueError('plain relative source member required')
    parts = PurePosixPath(name).parts
    if (not parts or '/'.join(parts) != name or name.startswith('/')
            or any(part in ('.', '..') or part.endswith('.')
                or not re.fullmatch(r'[A-Za-z0-9_.-]+', part)
                or re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part)
                for part in parts)):
        raise ValueError('unsafe source member path')
    path = root.joinpath(*parts)
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ValueError('source member through reparse point refused')
    path = path.resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('ordinary source member leaves explicit root')
    return path


def read_text(path: Path, limit: int = MAX_TEXT) -> str:
    if not path.is_file() or path.stat().st_size > limit:
        raise ValueError('bounded ordinary source file required: ' + str(path))
    with path.open('rb') as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise ValueError('source grew beyond declared bound')
    return raw.decode('utf-8-sig')


def load_json(path: Path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate layout JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(read_text(path), object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError('nonfinite layout value: ' + value)))


@dataclass(frozen=True)
class AssemblyUnit:
    name: str
    cpu: str
    sources: tuple[str, ...]
    rom_base: int
    extent: int
    entry_symbol: str
    label_prefix: str
    rows: tuple[tuple[int, int], ...]

    @property
    def instruction_bytes(self):
        return sum(width for _, width in self.rows)

    def symbols(self, pc):
        width = 6 if self.cpu == 'm68k' else 4
        start = self.label_prefix + format(pc, '0' + str(width) + 'x')
        return start, start + '_end'


def load_layout(layout_root: Path) -> tuple[tuple[AssemblyUnit, ...], tuple[str, ...]]:
    """从布局清单读取指令地址、宽度、字节范围和源码标签。"""
    root = ordinary_root(layout_root, 'layout_root')
    declaration = load_json(member(root, 'manifest.json'))
    if (type(declaration) is not dict or set(declaration) != {'format', 'image_size', 'groups', 'resource_ids'}
            or declaration['format'] != FORMAT or declaration['image_size'] != 0x100000
            or type(declaration['groups']) is not list or len(declaration['groups']) != 14
            or type(declaration['resource_ids']) is not list or len(declaration['resource_ids']) != 128
            or any(type(name) is not str or not name for name in declaration['resource_ids'])
            or len(set(declaration['resource_ids'])) != 128):
        raise ValueError('complete fourteen-group/128-resource assembly layout required')
    units, names, files, physical = [], set(), set(), []
    for group in declaration['groups']:
        if type(group) is not dict or set(group) != {'name', 'cpu', 'sources', 'layout', 'rom_base',
                'extent', 'entry_symbol', 'label_prefix'}:
            raise ValueError('pure fixed assembly group declaration required')
        name, cpu = group['name'], group['cpu']
        if (type(name) is not str or not re.fullmatch(r'[a-z][a-z0-9_]{0,100}', name)
                or name in names or cpu not in ('m68k', 'z80')
                or type(group['sources']) is not list or not group['sources']
                or any(type(value) is not str for value in group['sources'])
                or len(set(group['sources'])) != len(group['sources'])):
            raise ValueError('explicit unique assembly group and source members required')
        names.add(name)
        if group['layout'] in files:
            raise ValueError('one sole extent file per assembly group required')
        files.add(group['layout'])
        base = integer(group['rom_base'], 0, 0xFFFFF, 'physical base')
        extent = integer(group['extent'], 1, 0x100000, 'logical extent')
        if cpu == 'm68k':
            wanted = (0, '_start', 'm68k_')
        elif name == 'z80_driver':
            wanted = (0x69D2, '_start', 'z80_')
            if extent != 0xFCA:
                raise ValueError('complete driver logical extent required')
        elif name == 'z80_startup':
            wanted = (0x2CA, '_boot_start', 'boot_z80_')
            if extent != 38:
                raise ValueError('complete startup logical extent required')
        else:
            raise ValueError('only the actual independent driver/startup mappings are defined')
        if (base, group['entry_symbol'], group['label_prefix']) != wanted:
            raise ValueError('actual CPU source labels/physical mapping required')
        fields = load_json(member(root, group['layout']))
        if (type(fields) is not dict or set(fields) != {'format', 'name', 'rows'}
                or fields['format'] != UNIT_FORMAT or fields['name'] != name
                or type(fields['rows']) is not list or not fields['rows']):
            raise ValueError('instruction address/size-only layout required')
        rows, previous_end = [], 0
        for row in fields['rows']:
            if type(row) is not list or len(row) != 2:
                raise ValueError('one [logical address,instruction size] row required')
            pc = integer(row[0], previous_end, extent - 1, 'instruction address')
            size = integer(row[1], 1, 10 if cpu == 'm68k' else 4, 'instruction size')
            if pc + size > extent or base + pc + size > 0x100000:
                raise ValueError('instruction extent leaves its declared image')
            if cpu == 'm68k' and (pc & 1 or size & 1):
                raise ValueError('actual 68000 WORD alignment required')
            rows.append((pc, size))
            physical.append((base + pc, base + pc + size, name))
            previous_end = pc + size
        if previous_end != extent:
            raise ValueError('last real instruction must end at its declared logical extent')
        unit = AssemblyUnit(name, cpu, tuple(group['sources']), base, extent,
            group['entry_symbol'], group['label_prefix'], tuple(rows))
        if cpu == 'z80' and (len(rows), unit.instruction_bytes) != (
                (1687, 3342) if name == 'z80_driver' else (25, 38)):
            raise ValueError('the full independent driver/startup instruction scope is required')
        units.append(unit)
    if sum(unit.cpu == 'm68k' for unit in units) != 12:
        raise ValueError('twelve distinct owned 68000 groups required')
    ordered = sorted(physical)
    for before, after in zip(ordered, ordered[1:]):
        if before[1] > after[0]:
            raise ValueError('competing assembly instruction authority: ' + repr((before, after)))
    return tuple(units), tuple(declaration['resource_ids'])


def source_instructions(source_root: Path, unit: AssemblyUnit) -> tuple[dict[int, str], list[dict]]:
    """按起止标签读取单条助记符，合并同组中的独立源文件。

    布局约定宽度，交叉工具生成的起止符号供后续校验。
    """
    root = ordinary_root(source_root, 'source_root')
    extents = dict(unit.rows)
    output, origins, entry_count = {}, [], 0
    for relative in unit.sources:
        path = member(root, relative)
        lines = read_text(path).splitlines()
        position, active, instruction, count = 0, None, None, 0
        for number, original in enumerate(lines, 1):
            line = original.split('|' if unit.cpu == 'm68k' else ';', 1)[0].strip()
            if not line:
                continue
            if active is None and line in (('.cpu 68000', '.section .text') if unit.cpu == 'm68k' else ('.text',)):
                continue
            if active is None and line == unit.entry_symbol + ':':
                if position != 0:
                    raise ValueError('entry symbol must remain at logical zero')
                entry_count += 1
                continue
            origin = re.fullmatch(r'\.org (0x[0-9A-Fa-f]+|[0-9]+)', line)
            if active is None and origin:
                position = int(origin[1], 0)
                continue
            if active is None:
                match = re.fullmatch(re.escape(unit.label_prefix) + r'([0-9a-f]+):', line)
                if match:
                    pc = int(match[1], 16)
                    if pc != position or pc not in extents or unit.symbols(pc)[0] + ':' != line or pc in output:
                        raise ValueError('unknown/moved/duplicated real instruction label: ' + relative + ':' + str(number))
                    active, instruction = pc, None
                    continue
                raise ValueError('undeclared source directive/label: ' + relative + ':' + str(number))
            if line == unit.symbols(active)[1] + ':':
                if instruction is None:
                    raise ValueError('one actual instruction per start/end pair required')
                output[active] = instruction
                position = active + extents[active]
                active, instruction, count = None, None, count + 1
                continue
            if instruction is not None or len(line) > 256:
                raise ValueError('one bounded instruction without embedded extra statements required')
            if unit.cpu == 'm68k':
                valid = re.fullmatch(r'[A-Za-z][A-Za-z0-9.]*([ \t]+[A-Za-z0-9_.$%#():,+*/ <>\-]+)?', line)
                token = line.split()[0].split('.')[0].lower()
                no_widths = re.sub(r'\b0x[0-9a-fA-F]+:[wWlL]\b', '', line)
                if (not valid or token not in M68K_MNEMONICS or ':' in no_widths
                        or '/*' in line or '*/' in line):
                    raise ValueError('one 68000 mnemonic, not an opaque/data directive, required')
            else:
                valid = re.fullmatch(r"[A-Za-z][A-Za-z0-9]*([ \t]+[A-Za-z0-9_.$'()+, \-]+)?", line)
                if not valid or line.split()[0].lower() not in Z80_MNEMONICS:
                    raise ValueError('one Z80 mnemonic, not an opaque/data directive, required')
            instruction = ' '.join(line.split())
        if active is not None:
            raise ValueError('unterminated source instruction: ' + relative)
        origins.append(dict(source=relative, instructions=count))
    if entry_count != 1 or set(output) != set(extents):
        raise ValueError('complete source instruction set and sole actual entry symbol required: ' + unit.name)
    return output, origins


def native_group(source_root: Path, unit: AssemblyUnit) -> tuple[dict, list[dict]]:
    instructions, origins = source_instructions(source_root, unit)
    header = ['.cpu 68000', '.section .text'] if unit.cpu == 'm68k' else ['.text']
    assembly = header + [unit.entry_symbol + ':']
    rows, expected = [], {unit.entry_symbol: 0}
    for pc, size in unit.rows:
        begin, end = unit.symbols(pc)
        assembly.extend(('.org 0x' + format(pc, 'X'), begin + ':', '        ' + instructions[pc], end + ':'))
        expected[begin], expected[end] = pc, pc + size
        rows.append(dict(logical_pc=pc, physical_pc=unit.rom_base + pc, width=size,
            start_symbol=begin, end_symbol=end))
    group = dict(name=unit.name, cpu=unit.cpu, assembly='\n'.join(assembly) + '\n',
        instruction_rows=rows, expected_symbols=expected, sources={})
    if unit.cpu == 'z80':
        group['audio_unit'] = 'driver' if unit.name == 'z80_driver' else 'startup'
        # Native's existing COFF verifier consumes only these geometry fields;
        # no high-level audio generator/UNITS source is imported or invoked.
        group['descriptor'] = dict(rom_base=unit.rom_base, extent=unit.extent,
            rows=[dict(address=pc, size=size) for pc, size in unit.rows])
    return group, origins
