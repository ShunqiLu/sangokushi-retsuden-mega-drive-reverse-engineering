"""Explicit existing 68000 source builds read only as original copy CODE.

No instruction is executed. The original 006950 software copies some physical
68000 instructions into its sound workspace, so these bytes retain their code
authority instead of becoming art/audio resources. No implicit root, original
ROM, bank input, analysis-byte payload, hash or native rebuild is selected.
"""
import csv
from dataclasses import dataclass
import io
import json
from pathlib import Path
import re

from tools.m68k_build.elf_verify import verify_object
from tools.m68k_build.source import format_instruction
from tools.code_analysis.m68k_code_map import load_capstone
from ..high_level_scene_flows.domain import ReadOnlyData


SOUND_COPY_CODE_RANGES = ((0x808A, 0x80D0), (0x80F4, 0x812C), (0x83C8, 0x879C))


@dataclass(frozen=True)
class M68kCopyAuthority:
    """One explicit editable source, layout-only ledger and existing build.

    Paths resolve against the caller's source_root. They may be absolute only
    when they still name files inside that same supplied root. A ledger owns
    no byte payload here: only address and size are consumed.
    """
    source: Path
    layout_ledger: Path
    native_object: Path
    native_image: Path


def project_sound_copy_authorities():
    """Return three relative layout descriptions, without reading any files.

    There is no implicit project location. Callers must still pass their own
    source_root and all three returned descriptions to the explicit loader.
    """
    return (
        M68kCopyAuthority(Path('src/m68k/direct_descendants.s'),
            Path('analysis/direct_code/generated/instructions.json'),
            Path('build/m68k_direct_code.o'), Path('build/m68k_direct_code.bin')),
        M68kCopyAuthority(Path('src/m68k/dispatch_descendants.s'),
            Path('analysis/dispatch_code/generated/instructions.json'),
            Path('build/m68k_dispatch_code.o'), Path('build/m68k_dispatch_code.bin')),
        M68kCopyAuthority(Path('src/m68k/candidate_action.s'),
            Path('analysis/candidate_action_source/generated/instructions.csv'),
            Path('build/m68k_action_code.o'), Path('build/m68k_action_code.bin')),
    )


def _owned_member(source_root, member):
    if not isinstance(member, Path):
        raise ValueError('an explicit source/build Path is required')
    path = (source_root / member).resolve()
    if not path.is_relative_to(source_root):
        raise ValueError('copy authority leaves the explicitly supplied source root')
    return path


def _layout_records(path):
    text = path.read_text(encoding='utf-8-sig')
    if path.suffix == '.json':
        rows = json.loads(text)
    elif path.suffix == '.csv':
        rows = list(csv.DictReader(io.StringIO(text)))
    else:
        raise ValueError('explicit JSON or CSV instruction layout ledger required')
    # Byte values, source opcode comments and historical hashes are deliberately
    # discarded. They never supply bytes or instruction semantics to this view.
    return [dict(address=int(row['address']), size=int(row['size'])) for row in rows]


def _source_instructions(path, records):
    lines = [line.split('|', 1)[0].strip() for line in path.read_text(encoding='utf-8').splitlines()]
    lines = [line for line in lines if line]
    if lines[:3] != ['.cpu 68000', '.section .text', '_start:'] or len(lines) != 3 + 4 * len(records):
        raise ValueError('complete instruction-only source topology differs')
    instructions = {}
    for index, row in enumerate(records):
        group = lines[3 + 4 * index:7 + 4 * index]
        address = row['address']
        if (group[0] != f'.org 0x{address:X}' or group[1] != f'm68k_{address:06x}:'
                or group[3] != f'm68k_{address:06x}_end:'):
            raise ValueError('source address/start/end labels differ from object authority')
        instruction = group[2]
        if (len(instruction) > 256
                or not re.fullmatch(r'[A-Za-z][A-Za-z0-9.]*([ \t]+[A-Za-z0-9_.$%#():,+*/ <>\-]+)?', instruction)
                or ':' in re.sub(r'\b0x[0-9a-fA-F]+:[wWlL]\b', '', instruction)
                or '/*' in instruction or '*/' in instruction):
            raise ValueError('one real mnemonic without embedded directives required')
        instructions[address] = ' '.join(instruction.split())
    return instructions


def load_m68k_sound_copy_data(source_root: Path, *, direct: M68kCopyAuthority,
        dispatch: M68kCopyAuthority, action: M68kCopyAuthority):
    """Return exact original copy CODE and provenance from three own builds.

    The existing bounded ELF reader validates every actual instruction label
    and the object .text/image relationship. Each selected compiled instruction
    is decoded by Capstone only for current-source correspondence: the normal
    mnemonic formatter must reproduce its current editable source instruction.
    No decoded instruction is run, and no original/reference bytes are read.
    """
    if not isinstance(source_root, Path) or not source_root.is_dir():
        raise ValueError('an explicit existing own source root is required')
    source_root = source_root.resolve()
    if any(type(authority) is not M68kCopyAuthority for authority in (direct, dispatch, action)):
        raise ValueError('all three explicit typed source/build authorities are required')
    capstone = load_capstone()
    decoder = capstone.Cs(capstone.CS_ARCH_M68K, capstone.CS_MODE_BIG_ENDIAN | capstone.CS_MODE_M68K_000)
    decoder.detail = True
    chunks, evidence = [], []
    for name, authority in (('direct', direct), ('dispatch', dispatch), ('action', action)):
        source = _owned_member(source_root, authority.source)
        ledger = _owned_member(source_root, authority.layout_ledger)
        object_path = _owned_member(source_root, authority.native_object)
        image_path = _owned_member(source_root, authority.native_image)
        records = _layout_records(ledger)
        instructions = _source_instructions(source, records)
        image = image_path.read_bytes()
        actual_text = verify_object(object_path.read_bytes(), records)
        if actual_text != image or len(image) != records[-1]['address'] + records[-1]['size']:
            raise ValueError('supplied source-built object and binary text differ')
        selected = []
        for row in records:
            address, width = row['address'], row['size']
            if not any(start < address + width and address < end for start, end in SOUND_COPY_CODE_RANGES):
                continue
            if not any(start <= address and address + width <= end for start, end in SOUND_COPY_CODE_RANGES):
                raise ValueError('reviewed copy range must contain the complete selected instruction')
            raw = image[address:address + width]
            decoded = list(decoder.disasm(raw, address, count=1))
            if len(decoded) != 1 or decoded[0].size != width:
                raise ValueError('cached executable instruction boundary differs from current source')
            canonical = ' '.join(format_instruction(decoded[0]).split())
            if canonical != instructions[address]:
                raise ValueError('source-built cache differs from current editable mnemonic at ' + hex(address)
                    + ': source=' + instructions[address] + ' cache=' + canonical)
            chunks.append((address, raw))
            selected.append(row)
        evidence.append(dict(authority=name, source=str(source), layout_ledger=str(ledger),
            layout_ledger_fields_read=['address', 'size'], object=str(object_path), image=str(image_path),
            whole_source_topology_and_object_labels=True, current_selected_mnemonics_match=True,
            selected_instructions=len(selected), selected_CODE_bytes=sum(row['size'] for row in selected)))
    joined = []
    for address, raw in sorted(chunks):
        if joined:
            previous, data = joined[-1]
            end = previous + len(data)
            if address < end:
                raise ValueError('two code sources compete for the same physical byte')
            if address == end:
                joined[-1] = previous, data + raw
                continue
        joined.append((address, raw))
    if [(base, base + len(raw)) for base, raw in joined] != list(SOUND_COPY_CODE_RANGES):
        raise ValueError('three complete reviewed copy-CODE intervals required without padding')
    return ReadOnlyData(tuple(joined)), dict(format='g5510-existing-m68k-copy-CODE-authority-v1',
        source_root=str(source_root), authorities=evidence, CODE_bytes=sum(len(raw) for base, raw in joined),
        ranges=[dict(start=start, end=end, bytes=end - start) for start, end in SOUND_COPY_CODE_RANGES],
        instruction_disassembler='Capstone ' + capstone.__version__, native_rebuilds=0, hashes_computed=0,
        original_ROM_or_analysis_byte_input=False, source_comment_opcode_input=False,
        resource_DATA_ownership_added=False, new_formal_CODE_bytes=0,
        limit='copy/checksum DATA only; execution remains recovered Python business functions')
