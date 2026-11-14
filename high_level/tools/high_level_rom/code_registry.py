"""Aggregate explicit logical M68K sources, not reference assembly or ROMs.

Each historical compiler remains its own authority and its own native group.
Adapters normalize metadata and add *real* labels on both sides of ordinary
instructions. They never create bytes, use a reference census, or invoke GNU.
This registry includes strict and intermediate/draft compilers; byte coverage
does not imply behavioral acceptance or a general Python-to-68000 compiler.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, is_dataclass
from importlib import import_module
from pathlib import Path
import re
import traceback


class RegistryError(ValueError):
    """A missing source, unsupported adapter or conflicting authority."""


class SourcePreparationError(RegistryError):
    """All failures from one current-source preparation, never partial code."""

    def __init__(self, failures):
        self.source_failures = tuple(failures)
        super().__init__('current logical source preparation failed in ' + str(len(failures))
            + ' group(s): ' + '; '.join(row['group'] + ': ' + row['error'] for row in failures))


@dataclass(frozen=True)
class SourceGroup:
    name: str
    package: str
    source_files: tuple[str, ...]
    adapter: str = 'modern'
    expected_owned_bytes: int = 0


def _files(package, *names):
    return tuple('tools/high_level_' + package + '/' + name + '.py' for name in names)


EVENT_MATH = _files('city_event', 'arithmetic')[0]
CYCLE = _files('city_cycle', 'business')[0]
OFFICER = _files('city_officer', 'business_officer')[0]
HEADS = _files('diplomacy_forces', 'business_shared')[0]

# Ordered authority is explicit. A group's reused units are not new ownership.
# Old movement / ai_policy variants are deliberately excluded in favor of v2.
SOURCE_GROUPS = (
    SourceGroup('pilot', 'high_level_pilot', _files('pilot', 'business'), 'pilot', 24),
    SourceGroup('control_primary', 'high_level_control', _files('control', 'business'), 'control0', 42),
    SourceGroup('control_secondary', 'high_level_control', _files('control', 'business'), 'control1', 42),
    SourceGroup('finance', 'high_level_finance', _files('finance', 'business'), 'finance', 70),
    SourceGroup('city_event', 'high_level_city_event', _files('city_event', 'business', 'arithmetic'), 'event', 804),
    SourceGroup('city_cycle', 'high_level_city_cycle', (CYCLE,), 'cycle', 708),
    SourceGroup('debt_cleanup', 'high_level_debt_cleanup', _files('debt_cleanup', 'business'), 'debt', 164),
    SourceGroup('battle_settlement', 'high_level_battle_settlement', _files('battle_settlement', 'business_numeric', 'business_members') + (EVENT_MATH,), expected_owned_bytes=1656),
    SourceGroup('battle_preparation', 'high_level_battle_preparation', _files('battle_preparation', 'business_selection', 'business_descriptor', 'business_result') + _files('remaining_flows', 'business_city'), 'preparation_fields', 1466),
    SourceGroup('ai_decision', 'high_level_ai_decision', _files('ai_decision', 'business_selection', 'business_policy', 'business_officer', 'business_commit') + (EVENT_MATH,), expected_owned_bytes=2036),
    SourceGroup('city_officer', 'high_level_city_officer', _files('city_officer', 'business_city', 'business_officer', 'business_roster') + _files('remaining_flows', 'business_city'), expected_owned_bytes=2896),
    SourceGroup('army_groups', 'high_level_army_groups', _files('army_groups', 'business_disposition', 'business_members', 'business_arrival') + (EVENT_MATH, OFFICER) + _files('remaining_flows', 'business_city'), expected_owned_bytes=2620),
    SourceGroup('diplomacy_forces', 'high_level_diplomacy_forces', _files('diplomacy_forces', 'business_shared', 'business_stratagem', 'business_personnel', 'business_forces') + (CYCLE, OFFICER, _files('debt_cleanup', 'business')[0], _files('army_groups', 'business_arrival')[0]) + _files('remaining_flows', 'business_city'), expected_owned_bytes=5492),
    SourceGroup('movement_v2', 'high_level_movement_v2', _files('movement_v2', 'business_path', 'business_arrival', 'business_campaign') + (CYCLE, HEADS, _files('city_officer', 'business_city')[0]) + _files('remaining_flows', 'business_city'), expected_owned_bytes=3394),
    SourceGroup('ai_policy_v2', 'high_level_ai_policy_v2', _files('ai_policy_v2', 'business_economy', 'business_routes', 'business_actions') + (CYCLE, _files('ai_decision', 'business_selection')[0], _files('ai_decision', 'business_commit')[0], _files('city_officer', 'business_roster')[0], _files('movement_v2', 'business_path')[0], _files('movement_v2', 'business_campaign')[0], HEADS, EVENT_MATH), expected_owned_bytes=7696),
    SourceGroup('battle_ai', 'high_level_battle_ai', _files('battle_ai', 'business_geometry', 'business_formation', 'business_actions') + (CYCLE,), expected_owned_bytes=7070),
    SourceGroup('player_commands', 'high_level_player_commands', _files('player_commands', 'business_budget', 'business_recruitment', 'business_display', 'business_reuse'), expected_owned_bytes=9320),
    SourceGroup('command_actions', 'high_level_command_actions', _files('command_actions', 'business_personnel', 'business_outcomes', 'business_logistics', 'business_reuse'), expected_owned_bytes=4296),
    SourceGroup('storage', 'high_level_storage', _files('storage', 'business_save', 'business_load', 'business_streams'), expected_owned_bytes=3858),
    SourceGroup('gameplay_flow', 'high_level_gameplay_flow', _files('gameplay_flow', 'business_calendar', 'business_battle', 'business_services', 'business_reuse'), expected_owned_bytes=8294),
    SourceGroup('scene_flows', 'high_level_scene_flows', _files('scene_flows', 'business_scene', 'business_duel', 'business_objects', 'business_reuse'), expected_owned_bytes=14260),
    SourceGroup('dynamic_flows', 'high_level_dynamic_flows', _files('dynamic_flows', 'business_duel', 'business_actions', 'business_early_phase', 'business_late_phase'), expected_owned_bytes=13132),
    SourceGroup('main_flows', 'high_level_main_flows', _files('main_flows', 'business_boot', 'business_commands', 'business_gameplay', 'business_highbank', 'business_lowbank', 'business_main', 'business_map', 'business_scene_support', 'business_title'), 'modules', 37498),
    SourceGroup('remaining_flows', 'high_level_remaining_flows', _files('remaining_flows', 'business_city', 'business_highbank', 'business_lowbank'), 'modules', 73684),
)


def _plain(value):
    return asdict(value) if is_dataclass(value) else value


def _spans(positions):
    ordered = sorted(positions)
    result = []
    for position in ordered:
        if result and result[-1]['end'] == position:
            result[-1]['end'] += 1
        else:
            result.append(dict(start=position, end=position + 1))
    return result


def _ea_bytes(operand, bits):
    operand = operand.strip()
    if operand.startswith('#'):
        return 4 if bits == 32 else 2
    if re.fullmatch(r'%[da][0-7]|%sp|%sr|%ccr', operand):
        return 0
    if re.fullmatch(r'\(%(?:a[0-7]|sp)\)\+?|\-\(%(?:a[0-7]|sp)\)', operand):
        return 0
    if '(' in operand:
        return 2
    if operand.endswith(':w'):
        return 2
    if operand.endswith(':l'):
        return 4
    raise RegistryError('early adapter cannot infer EA width: ' + operand)


def _operands(text):
    parts, start, depth = [], 0, 0
    for index, char in enumerate(text):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif char == ',' and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    if text:
        parts.append(text[start:].strip())
    return parts


def _early_width(operation, operands):
    """Encoding hints for early event output; native labels remain the proof."""
    base, _, suffix = operation.partition('.')
    bits = dict(b=8, w=16, l=32).get(suffix, 16)
    args = _operands(operands)
    if base.startswith('b') and base not in ('btst', 'bset', 'bclr', 'bchg'):
        return 4 if suffix == 'w' else 2
    if base in ('dbra', 'dbf'):
        return 4
    if base in ('rts', 'nop', 'swap', 'ext', 'moveq'):
        return 2
    if base in ('movem',):
        ea = args[-1] if not args[-1].startswith('%d') and not args[-1].startswith('%a') else args[0]
        return 4 + _ea_bytes(ea, bits)
    if base in ('jsr', 'jmp'):
        return 2 + _ea_bytes(args[0], bits)
    if base in ('move', 'movea'):
        return 2 + sum(_ea_bytes(arg, bits) for arg in args)
    if base in ('addi', 'subi', 'andi', 'ori', 'eori', 'cmpi'):
        return 2 + (4 if bits == 32 else 2) + _ea_bytes(args[-1], bits)
    if base in ('btst', 'bset', 'bclr', 'bchg'):
        return 2 + (2 if args[0].startswith('#') else 0) + _ea_bytes(args[-1], 32 if re.fullmatch(r'%d[0-7]', args[-1]) else 8)
    if base in ('addq', 'subq', 'asl', 'asr', 'lsl', 'lsr', 'rol', 'ror'):
        return 2 + _ea_bytes(args[-1], bits)
    if base in ('lea', 'pea', 'tst', 'clr', 'neg', 'not'):
        return 2 + _ea_bytes(args[0], bits)
    if base in ('add', 'sub', 'and', 'or', 'eor', 'cmp', 'cmpa', 'adda', 'suba', 'mulu', 'muls', 'divu', 'divs'):
        return 2 + sum(_ea_bytes(arg, bits) for arg in args)
    raise RegistryError('unsupported early operation: ' + operation)


def _row(pc, width, operation, operands='', **extra):
    if type(pc) is not int or type(width) is not int or width not in (2, 4, 6, 8, 10):
        raise RegistryError('strict M68K instruction placement/width required')
    return dict(physical_pc=pc, logical_pc=pc, width=width,
                operation=operation, operands=operands, **extra)


def _units_rows(units):
    result = []
    for unit in units:
        binding = _plain(unit['binding'])
        pc = binding['entry']
        for item in unit['instructions']:
            pc = item.get('target_PC', pc)
            width = item['encoding_bytes']
            result.append(_row(pc, width, item['operation'], item.get('operands', ''), unit=binding['name']))
            pc += width
    return sorted(result, key=lambda row: row['physical_pc'])


def _binding_positions(bindings):
    result = set()
    for value in bindings:
        b = _plain(value)
        spans = b.get('segments') or ((b['entry'], b.get('end', b['entry'] + b.get('size', b.get('allocated_bytes', 0)))),)
        for start, end in spans:
            if type(start) is not int or type(end) is not int or start >= end:
                raise RegistryError('nonempty strict binding interval required')
            for position in range(start, end):
                if position in result:
                    raise RegistryError('overlapping primary bindings')
                result.add(position)
    return result


def _instruction_lines(assembly):
    for line in assembly.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith(('.', '|', '#')) and not stripped.endswith(':'):
            yield stripped


def _place_early(assembly, entry):
    lines = assembly.splitlines()
    for index, line in enumerate(lines):
        if line.strip().endswith(':') and not line.strip().startswith('.L'):
            lines.insert(index, f'.org 0x{entry:x}')
            return '\n'.join(lines) + '\n'
    raise RegistryError('early generated entry label missing')


def _compile(spec, texts):
    prefix = 'tools.' + spec.package
    target = None
    if spec.adapter in ('modern', 'modules', 'preparation_fields'):
        compiler = import_module(prefix + '.compiler_common')
        target = import_module(prefix + '.target')
        if spec.adapter == 'preparation_fields':
            value = compiler.compile_complete_frame_modules(*texts)
        else:
            value = compiler.compile_modules(dict(zip(target.MODULE_ROLES, texts))) if spec.adapter == 'modules' else compiler.compile_modules(*texts)
        primary = getattr(target, 'NEW_BINDINGS', target.BINDINGS)
        return value['assembly'], _units_rows(value['units']), _binding_positions(primary)
    compiler = import_module(prefix + '.compiler')
    if spec.adapter == 'debt':
        value = compiler.compile_source(texts[0])
        return value['assembly'], _units_rows(value['units']), _binding_positions([u['binding'] for u in value['units']])
    if spec.adapter in ('pilot', 'finance', 'control0', 'control1'):
        if spec.adapter.startswith('control'):
            target = import_module(prefix + '.target')
            value = compiler.compile_python(texts[0], target.BINDINGS[int(spec.adapter[-1])])
        else:
            value = compiler.compile_python(texts[0])
        entry = value.get('entry')
        if entry is None and spec.adapter == 'finance':
            entry = import_module(prefix + '.target').BINDING.entry
        extent = value['bytes']
        assembly = _place_early(value['assembly'], entry)
        statements = list(_instruction_lines(assembly))
        mappings = value['source_mapping']
        if len(statements) != len(mappings):
            raise RegistryError('early mapping/instruction count differs')
        rows = []
        for statement, item in zip(statements, mappings):
            operation, _, operands = statement.partition(' ')
            rows.append(_row(entry + item['offset'], item.get('bytes', item.get('size')), operation, operands.strip()))
        return assembly, rows, set(range(entry, entry + extent))
    if spec.adapter == 'event':
        value = compiler.compile_modules(*texts)
        rows = []
        for binding in value['bindings']:
            pc = binding.entry
            for item in value['mappings'][binding.name]:
                width = _early_width(item['mnemonic'], item['operands'])
                rows.append(_row(pc, width, item['mnemonic'], item['operands'], unit=binding.name))
                pc += width
            if pc != binding.end:
                raise RegistryError('early event width hints disagree with complete extent: ' + binding.name)
        return value['assembly'], sorted(rows, key=lambda row: row['physical_pc']), _binding_positions(value['bindings'])
    if spec.adapter == 'cycle':
        target = import_module(prefix + '.target')
        value = compiler.compile_python(texts[0])
        assembly, rows = ['.cpu 68000', '.text'], []
        for function in sorted(value['functions'], key=lambda item: item['entry']):
            text = re.sub(r'^\.section[^\n]+', f".org 0x{function['entry']:x}", function['assembly'])
            # The old compiler emitted separate sections + linker data symbols.
            # Relocate its *generated* PC operand from typed data binding + PC,
            # avoiding an assembler-time absolute .set treated as displacement.
            for item in function['mapping']:
                pc = function['entry'] + item['offset']
                statement = item['mnemonic']
                for name, address in target.TABLES.items():
                    if name + '(%pc)' in statement:
                        displacement = address - (pc + 2)
                        if not -32768 <= displacement <= 32767:
                            raise RegistryError('typed cycle PC data displacement out of WORD')
                        changed = statement.replace(name + '(%pc)', str(displacement) + '(%pc)')
                        text = text.replace(statement, changed)
                        statement = changed
                operation, _, operands = statement.partition(' ')
                rows.append(_row(pc, item['size'], operation, operands))
            assembly.append(text)
        # Same RNG physical body, separately source-generated and verified by
        # root native byte comparison, has canonical owner city_event.
        primary = tuple(b for b in target.BINDINGS if b.name != 'step_random')
        return '\n'.join(assembly) + '\n', rows, _binding_positions(primary)
    raise RegistryError('unsupported declared source adapter: ' + spec.adapter)


def _instrument(name, assembly, rows):
    """Insert labels adjacent to real instructions, never .set start+width."""
    output, index, expected = [], 0, {}
    for line in assembly.splitlines():
        stripped = line.strip()
        ordinary = stripped and not stripped.startswith(('.', '|', '#')) and not stripped.endswith(':')
        if not ordinary:
            if re.match(r'^\s*\.(byte|word|long|incbin|ascii|asciz)\b', line):
                raise RegistryError('opaque or data directive in a code group')
            output.append(line)
            continue
        if index >= len(rows):
            raise RegistryError(name + ': generated instruction without metadata')
        row = rows[index]
        operation = stripped.split(None, 1)[0]
        if operation != row['operation']:
            raise RegistryError(name + ': generated instruction/mapping operation differs')
        first = f'registry_{name}_{index}_start'
        last = f'registry_{name}_{index}_end'
        output.extend(('.global ' + first, first + ':', line, '.global ' + last, last + ':'))
        row.update(start_symbol=first, end_symbol=last)
        expected[first] = row['logical_pc']
        expected[last] = row['logical_pc'] + row['width']
        index += 1
    if index != len(rows):
        raise RegistryError(name + ': declared instruction not emitted')
    return '\n'.join(output) + '\n', expected


def compile_code(project_root: Path | str) -> dict:
    """Read declared semantic texts once and compile all M68K source groups.

    No reference inputs, subprocesses, object/ASM reads, or evidence files.
    The returned snapshots are the exact strings passed to every compiler.
    Source failures/conflicts are explicit errors, never silent omission.
    Alias equality is intentionally left for the caller's actual native layer.
    """
    root = Path(project_root).resolve(strict=True)
    groups, owners, cache, failures = [], {}, {}, []
    for spec in SOURCE_GROUPS:
        try:
            texts, snapshots = [], {}
            for relative in spec.source_files:
                path = root / relative
                if relative not in cache:
                    if not path.is_file() or path.stat().st_size > 4_000_000:
                        raise RegistryError('bounded declared logical source missing: ' + relative)
                    cache[relative] = path.read_text(encoding='utf-8')
                texts.append(cache[relative])
                snapshots[relative.replace('/', '__')] = cache[relative]
            assembly, rows, primary = _compile(spec, texts)
            present = set()
            for row in rows:
                extent = set(range(row['physical_pc'], row['physical_pc'] + row['width']))
                if extent & present:
                    raise RegistryError(spec.name + ': duplicate physical instruction authority')
                present |= extent
            if not primary <= present or len(primary) != spec.expected_owned_bytes:
                raise RegistryError(spec.name + ': primary source scope is incomplete or changed')
            for position in primary:
                if position in owners:
                    raise RegistryError(f'conflicting canonical ownership at {position:x}: {owners[position]} / {spec.name}')
            assembly, expected = _instrument(spec.name, assembly, rows)
        except Exception as error:
            # Finish this one source-generation pass so a later repair does
            # not have to repeat successful prefixes merely to see the next
            # unsupported group. No partial result or native build escapes.
            failures.append(dict(group=spec.name, source_files=list(spec.source_files),
                error_type=type(error).__name__, error=str(error), traceback=traceback.format_exc()))
            continue
        for position in primary:
            owners[position] = spec.name
        groups.append(dict(name=spec.name, cpu='m68k', physical_base=0,
                           assembly=assembly, instruction_rows=rows,
                           expected_symbols=expected, sources=snapshots,
                           owned_spans=_spans(primary), alias_spans=[],
                           primary_source_files=list(spec.source_files),
                           behavioral_acceptance='mixed strict and intermediate; not upgraded here'))
    if failures:
        raise SourcePreparationError(failures)
    aliases = []
    for group in groups:
        by_owner = {}
        owned = set(position for span in group['owned_spans'] for position in range(span['start'], span['end']))
        for row in group['instruction_rows']:
            for position in range(row['physical_pc'], row['physical_pc'] + row['width']):
                if position not in owners:
                    raise RegistryError(f'alias has no canonical source owner at {position:x}')
                if position not in owned:
                    by_owner.setdefault(owners[position], set()).add(position)
        for owner, positions in by_owner.items():
            for span in _spans(positions):
                alias = dict(span, owner=owner, alias=group['name'])
                aliases.append(alias)
                group['alias_spans'].append(alias)
    ownership = []
    for group in groups:
        ownership.extend(dict(span, owner=group['name']) for span in group['owned_spans'])
    ownership.sort(key=lambda span: span['start'])
    if len(owners) != 200522:
        raise RegistryError('honest unique M68K source coverage differs: ' + str(len(owners)))
    return dict(groups=groups, ownership=ownership, aliases=aliases,
                coverage=dict(cpu='m68k', unique_code_bytes=len(owners),
                              source_groups=len(groups), semantic_source_files=len(cache),
                              unique_instruction_count=len({r['physical_pc'] for g in groups for r in g['instruction_rows']}),
                              source_generation_only=True, native_verified_here=False,
                              sparse_padding_counted=False, new_strictly_accepted_bytes=0),
                unavailable=[], original_generation_input=False,
                precompiled_generation_input=False, complete_CPU=False)
