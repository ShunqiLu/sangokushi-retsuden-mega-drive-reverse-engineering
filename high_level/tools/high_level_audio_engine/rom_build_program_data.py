"""Use the current whole-ROM Z80 build in the original sound-copy lifetime.

This is a readonly program-DATA loader, not a Z80 interpreter or an audio
renderer. Original 68000 copy/reset and Python audio execution remain their
actual owners. No build is triggered and no ready bit, RAM, clock or PCM is
invented when a product is missing or stale.
"""
from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import stat

from . import compiler, target
from .compiled_program_data import (
    CompiledSoundCopyData, _joined, load_compiled_sound_copy_data,
)
from ..high_level_rom.z80_coff import MAX_OBJECT_SIZE, verify_object


_GROUPS = {'startup':'audio_startup', 'driver':'audio_driver'}
_FLAT_FILES = frozenset(('startup.o', 'startup.bin', 'driver.o', 'driver.bin'))
_FLAT_MARKERS = _FLAT_FILES | frozenset(('startup.s', 'driver.s'))


def _reparse(path):
    return (path.is_symlink() or getattr(path, 'is_junction', lambda: False)()
        or path.exists() and bool(getattr(path.stat(), 'st_file_attributes', 0)
            & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0)))


def _native_root(value):
    if not isinstance(value, Path):
        raise ValueError('explicit own sound native-build Path required')
    path = value.absolute()
    if any(_reparse(member) for member in (path, *path.parents)) or not path.is_dir():
        raise ValueError('ordinary existing own sound native-build root required')
    return path.resolve(strict=True)


def _member(root, relative, maximum):
    path = root / relative
    for member in (path, *path.parents):
        if member == root:break
        if _reparse(member):
            raise ValueError('sound build member through a reparse point refused: ' + relative)
    resolved = path.resolve(strict=True)
    if (not resolved.is_relative_to(root) or not resolved.is_file()
            or not 0 < resolved.stat().st_size <= maximum):
        raise ValueError('bounded ordinary sound build member required: ' + relative)
    with resolved.open('rb') as stream:
        raw = stream.read(maximum + 1)
    if len(raw) > maximum:
        raise ValueError('sound build member grew past the explicit bound: ' + relative)
    return raw


def _text_member(root, relative, maximum, encoding):
    # Builders publish LF, while read_text() inputs already use universal
    # newlines. Match those complete logical strings without hiding content.
    return _member(root, relative, maximum).decode(encoding).replace('\r\n', '\n').replace('\r', '\n')


def load_rom_build_sound_copy_data(native_build_root: Path,
        logical_sources: Mapping[str, str]) -> CompiledSoundCopyData:
    """Load complete current audio_driver/audio_startup high_level_rom groups.

    The explicit current logical sources are frozen once. Their existing
    whole-source admission and generation produce the same complete two
    assembly strings used by high_level_rom.build.audio_groups. Every actual
    group snapshot and generated.s must match, not a receipt or a digest.
    The existing pure COFF validator then proves actual labels, instruction
    widths, unresolved-relocation absence, image identity and sparse gaps.

    Assembly generation at future runtime uses Python only; GNU is not run.
    This function does not install code into live RAM, fetch opcodes, create
    hardware, advance time, enqueue a sound, or claim behavioral acceptance.
    """
    root = _native_root(native_build_root)
    if not isinstance(logical_sources, Mapping):
        raise ValueError('explicit complete current logical audio source mapping required')
    sources = dict(logical_sources)
    if (set(sources) != set(target.BUSINESS_MODULES)
            or any(type(name) is not str or Path(name).name != name
                or '/' in name or '\\' in name or ':' in name
                or type(source) is not str or not source
                for name, source in sources.items())):
        raise ValueError('complete current declared logical audio module texts required')
    # Keep the actual existing normalization/admission. A raw facade snapshot
    # is not allowed to stand in for the normalized source contract.
    trees, unused_count = compiler._admit(sources)
    assembly = compiler.generate(sources)
    if type(assembly) is not dict or set(assembly) != set(_GROUPS):
        raise ValueError('both complete current generated sound programs required')
    chunks, total = [], 0
    expected_snapshots = {'source-' + name for name in sources}
    for unit in ('startup', 'driver'):
        group = _GROUPS[unit]
        directory = root / group
        if _reparse(directory) or not directory.is_dir():
            raise ValueError('complete actual whole-build sound group required: ' + group)
        snapshots = {path.name for path in directory.iterdir() if path.name.startswith('source-')}
        if snapshots != expected_snapshots:
            raise ValueError('whole current logical sound snapshot set differs: ' + group)
        for name, source in sources.items():
            actual = _text_member(root, group + '/source-' + name, 4_000_000, 'utf-8')
            if actual != source:
                raise ValueError('complete current logical sound source differs: ' + group + '/' + name)
        if type(assembly[unit]) is not str or not 0 < len(assembly[unit]) <= 1_000_000:
            raise ValueError('bounded complete generated sound source required')
        actual_assembly = _text_member(root, group + '/generated.s', 1_000_000, 'ascii')
        if actual_assembly != assembly[unit]:
            raise ValueError('complete current generated sound assembly differs: ' + group)
        descriptor = target.UNITS[unit]
        image = _member(root, group + '/code.bin', 65536)
        native_object = _member(root, group + '/code.o', MAX_OBJECT_SIZE)
        checked = verify_object(unit, descriptor, native_object, image)
        total += checked['instruction_bytes']
        for row in descriptor['rows']:
            address, width = row['address'], row['size']
            chunks.append((descriptor['rom_base'] + address, image[address:address + width]))
    data = _joined(chunks)
    if total != 3380 or sum(len(raw) for _, raw in data.segments) != total:
        raise ValueError('whole current driver3342/startup38 CODE authority required')
    return CompiledSoundCopyData(data, total, tuple(trees), root)


def load_current_sound_copy_data(native_build_root: Path,
        logical_sources: Mapping[str, str]) -> CompiledSoundCopyData:
    """Select one actual build format, never recover from a failed authority.

    The root is always the caller's choice. Only two concrete source-built
    formats are supported: the original flat standalone audio builder and
    the whole-ROM builder's audio_driver/audio_startup groups. Mixed layouts,
    incomplete pairs and unknown roots stop; validation failure never falls
    back to another loader or invokes a native rebuild.
    """
    root = _native_root(native_build_root)
    names = {path.name for path in root.iterdir()}
    flat = bool(names & _FLAT_MARKERS)
    grouped = bool(names & set(_GROUPS.values()))
    if flat and grouped:
        raise ValueError('competing standalone/grouped sound build authorities at the same root')
    if grouped:
        if not set(_GROUPS.values()) <= names:
            raise ValueError('both explicitly named whole-build sound groups are required')
        return load_rom_build_sound_copy_data(root, logical_sources)
    if flat:
        if not _FLAT_FILES <= names:
            raise ValueError('both complete standalone sound program/image pairs are required')
        # The unchanged legacy contract still checks all seven complete
        # normalized source snapshots and the actual COFF/image geometry.
        return load_compiled_sound_copy_data(root, logical_sources)
    raise ValueError('no supported complete current-source sound build format at the explicit root')
