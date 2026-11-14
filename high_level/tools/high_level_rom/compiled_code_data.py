"""Load M68K instruction DATA from a current high-level local native build.

The original game may copy or checksum CODE as data. No instruction is run
here. Generated source, full logical snapshots, ELF labels, decoded operands,
sparse extents and canonical/alias ownership are independently checked. The
old assembly/analysis-based cartridge loader is deliberately unchanged.
"""
from __future__ import annotations

from pathlib import Path

from . import code_registry
from .build import select_code
from .native import _elf_symbols, _validate_group
from .m68k_correspondence import verify_current_instructions
from ..code_analysis.m68k_code_map import load_capstone
from ..high_level_scene_flows.domain import ReadOnlyData


M68K_CODE_BYTES = 200522


def _root(value, name):
    if not isinstance(value, Path) or not value.is_dir():
        raise ValueError('explicit existing ' + name + ' Path required')
    value = value.absolute()
    for member in (value, *value.parents):
        if member.is_symlink() or getattr(member, 'is_junction', lambda: False)():
            raise ValueError(name + ' through a reparse point is refused')
    return value.resolve(strict=True)


def _member(root, relative, maximum):
    if type(relative) is not str or not relative or Path(relative).is_absolute():
        raise ValueError('explicit relative build/source member required')
    candidate = root / relative
    for member in (candidate, *candidate.parents):
        if member == root:break
        if member.is_symlink() or getattr(member, 'is_junction', lambda: False)():
            raise ValueError('source/build member through a reparse point is refused')
    path = candidate.resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file() or not 0 < path.stat().st_size <= maximum:
        raise ValueError('bounded ordinary own build/source member required: ' + relative)
    return path


def _group_data(group, native_root, decoder):
    rows = _validate_group(group)
    if group['cpu'] != 'm68k' or any(row['logical_pc'] != row['physical_pc'] for row in rows):
        raise ValueError('same-address explicit M68K code group required')
    name = group['name']
    directory = native_root / name
    if not directory.is_dir() or directory.is_symlink() or getattr(directory, 'is_junction', lambda: False)():
        raise ValueError('actual ordinary code group directory required: ' + name)
    sources = group.get('sources')
    if type(sources) is not dict or not sources:
        raise ValueError('complete current logical source snapshots required')
    expected = set()
    for key, text in sources.items():
        if (type(key) is not str or Path(key).name != key or type(text) is not str
                or not key or '/' in key or '\\' in key or ':' in key):
            raise ValueError('simple complete source snapshot name/text required')
        snapshot = 'source-' + key
        expected.add(snapshot)
        path = _member(native_root, name + '/' + snapshot, 4_000_000)
        if path.read_text(encoding='utf-8') != text:
            raise ValueError('complete current logical source/build snapshot differs: ' + name + '/' + key)
    actual = {path.name for path in directory.iterdir() if path.name.startswith('source-')}
    if actual != expected:
        raise ValueError('complete source snapshot member set differs: ' + name)
    assembly = _member(native_root, name + '/generated.s', 8_000_000)
    if assembly.read_text(encoding='ascii') != group['assembly']:
        raise ValueError('whole current generated assembly/build source differs: ' + name)
    elf = _member(native_root, name + '/code.elf', 16_000_000)
    binary = _member(native_root, name + '/code.bin', 0x100000)
    image = binary.read_bytes()
    symbols, section = _elf_symbols(elf.read_bytes(), image)
    for label, address in group['expected_symbols'].items():
        if type(address) is not int or symbols.get(label) != (address, section):
            raise ValueError('actual current group boundary differs: ' + label)
    for row in rows:
        if (symbols.get(row['start_symbol']) != (row['logical_pc'], section)
                or symbols.get(row['end_symbol']) != (row['logical_pc'] + row['width'], section)):
            raise ValueError('actual whole instruction placement/width differs: ' + name)
    positions = {pc for row in rows for pc in range(row['logical_pc'], row['logical_pc'] + row['width'])}
    if len(image) != max(positions) + 1:
        raise ValueError('actual current group image extent differs: ' + name)
    if any(value for pc, value in enumerate(image) if pc not in positions):
        raise ValueError('undeclared noninstruction content in sparse image: ' + name)
    correspondence = verify_current_instructions(group, image, decoder)
    blocks = [dict(start=row['physical_pc'], end=row['physical_pc'] + row['width'],
        data=image[row['logical_pc']:row['logical_pc'] + row['width']],
        owner=name, role='m68k_code') for row in rows]
    return dict(blocks=blocks), dict(name=name, native_build_directory=str(directory),
        current_source_files=list(group['primary_source_files']), source_snapshot_members=sorted(expected),
        generated_source=str(assembly), native_elf=str(elf), native_image=str(binary),
        instructions=len(rows), CODE_bytes=sum(row['width'] for row in rows),
        complete_current_source_snapshots_match=True, complete_current_generated_source_match=True,
        complete_source_topology_and_object_labels_match=True,
        complete_current_mnemonics_and_operands_match=True, decoded_correspondence=correspondence,
        unresolved_relocations=0, sparse_bytes_excluded=len(image) - len(positions),
        sparse_padding_selected=False)


def _readonly(blocks):
    segments = []
    start, payload = None, bytearray()
    for block in sorted(blocks, key=lambda value: value.start):
        if start is not None and start + len(payload) != block.start:
            segments.append((start, bytes(payload)))
            start, payload = None, bytearray()
        if start is None:start = block.start
        # Only actual canonical instruction bytes are appended. Gaps are not
        # represented by a zero-filled buffer or even selected temporarily.
        payload.extend(block.data)
    if start is not None:segments.append((start, bytes(payload)))
    return ReadOnlyData(tuple(segments))


def load_high_level_m68k_copy_data(project_root: Path, native_build_root: Path) -> tuple[ReadOnlyData, dict]:
    """Verify current Python-generated M68K builds, then select canonical CODE.

    Runtime regenerates ordinary assembly/rows from the registered complete
    current Python texts, but never invokes GNU or reads old src/m68k files,
    analysis ledgers, original ROMs, receipts, hashes or a prebuilt bank.
    The supplied native root must be an actual high_level_rom.build output.
    Same-width wrong instructions are rejected by decoded source matching.
    Source coverage/correspondence does not grant behavioral acceptance.
    """
    project = _root(project_root, 'current high-level source root')
    native = _root(native_build_root, 'local high-level native build root')
    if Path(code_registry.__file__).resolve() != project / 'tools/high_level_rom/code_registry.py':
        raise ValueError('current imported source registry must belong to the explicit project root')
    for spec in code_registry.SOURCE_GROUPS:
        for relative in spec.source_files:
            _member(project, relative, 4_000_000)
    generated = code_registry.compile_code(project)
    if (generated.get('unavailable') or generated.get('original_generation_input') is not False
            or generated.get('precompiled_generation_input') is not False
            or generated['coverage']['unique_code_bytes'] != M68K_CODE_BYTES):
        raise ValueError('complete current high-level M68K source ownership required')
    capstone = load_capstone()
    decoder = capstone.Cs(capstone.CS_ARCH_M68K, capstone.CS_MODE_BIG_ENDIAN | capstone.CS_MODE_M68K_000)
    decoder.detail = True
    results, evidence = {}, []
    for group in generated['groups']:
        if group['name'] in results:
            raise ValueError('one current source/build per code group required')
        try:
            results[group['name']], row = _group_data(group, native, decoder)
            evidence.append(row)
        except (ValueError, TypeError, KeyError, OSError) as error:
            raise ValueError('current high-level M68K group ' + group['name'] + ': ' + str(error)) from error
    blocks, accounting = select_code(results, generated['ownership'], generated['aliases'])
    data = _readonly(blocks)
    total = sum(len(raw) for _, raw in data.segments)
    if total != M68K_CODE_BYTES or accounting['unique_code_bytes'] != M68K_CODE_BYTES:
        raise ValueError('canonical complete current M68K CODE must be200522 bytes')
    return data, dict(authorities=evidence, instructions=sum(row['instructions'] for row in evidence),
        CODE_bytes=total, source_root=str(project), native_build_root=str(native),
        source_groups=len(results), registry_coverage=generated['coverage'],
        instructions_include_aliases=True,
        unique_instruction_count=generated['coverage']['unique_instruction_count'],
        alias_declarations=len(generated['aliases']), canonical_selection=accounting,
        disassembler='Capstone ' + capstone.__version__,
        confidence='current_high_level_source_native_correspondence_not_behavioral_acceptance',
        original_ROM_or_bank_input=False, original_assembly_or_analysis_input=False,
        receipts_used_as_authority=False, sparse_padding_selected=False,
        native_rebuilds=0, hashes_computed=0, new_formal_CODE_bytes=0,
        runtime_source_generation=True, instruction_execution=False,
        limits=['complete current source/native CODE correspondence only',
            'Capstone plus its current existing formatter is an explicit runtime dependency',
            'no CPU/IRQ/reset/checksum/gameplay execution or semantic acceptance',
            'resources and Z80 CODE must still have separate explicit authorities'])
