"""Explicit own compiled sound programs used only as 68000 copy/checksum DATA.

No opcode is fetched or interpreted by this module. Game/audio execution stays
in the recovered Python functions. The original 68000 still reads its sound
program bytes as DATA when copying them to shared RAM, so those bytes must have
an explicit source-built authority rather than a ROM or zero-filled fallback.
"""
import ast
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Mapping

from . import compiler, target
from .build import verify_object
from .domain import word
from .owned_runtime import driver_static_data
from ..high_level_scene_flows.domain import ReadOnlyData


@dataclass(frozen=True)
class CompiledSoundCopyData:
    data: ReadOnlyData
    instruction_bytes: int
    admitted_source_modules: tuple[str, ...]
    native_source_root: Path


def _joined(segments):
    joined = []
    for base, payload in sorted(segments):
        if joined:
            previous, raw = joined[-1]
            end = previous + len(raw)
            if base < end:
                raise ValueError('competing physical program-copy DATA authority')
            if base == end:
                joined[-1] = previous, raw + payload
                continue
        joined.append((base, payload))
    return ReadOnlyData(tuple(joined))


def load_compiled_sound_copy_data(native_source_root: Path,
                                 logical_sources: Mapping[str, str]):
    """Consume an explicitly supplied own build whose complete source matches.

    Current original-source admission runs without generating assembly or
    invoking a compiler. Every normalized module must match this build's full
    source snapshot, not just a name/signature. The bounded native object reader
    checks actual boundaries and its text/image relationship. Sparse non-code
    gaps are excluded entirely; independent resource owners still supply them.
    No original ROM, old execution trace, default path or reference byte input
    is selected. A changed source requires a corresponding source-built product.
    """
    if not isinstance(native_source_root, Path) or not native_source_root.is_dir():
        raise ValueError('explicit own native source-build directory required')
    trees, unused_count = compiler._admit(logical_sources)
    for name, tree in trees.items():
        snapshot = native_source_root / ('source-' + name)
        old = ast.parse(snapshot.read_text(encoding='utf-8'), filename=str(snapshot))
        if compiler._stable_ast_dump(tree) != compiler._stable_ast_dump(old):
            raise ValueError('compiled program copy has different complete source: ' + name)
    chunks, total = [], 0
    for unit in ('startup', 'driver'):
        descriptor = target.UNITS[unit]
        image = (native_source_root / (unit + '.bin')).read_bytes()
        native_object = (native_source_root / (unit + '.o')).read_bytes()
        checked = verify_object(unit, descriptor, native_object, image)
        total += checked['instruction_bytes']
        for row in descriptor['rows']:
            offset, width = row['address'], row['size']
            chunks.append((descriptor['rom_base'] + offset, image[offset:offset + width]))
    data = _joined(chunks)
    if sum(len(payload) for base, payload in data.segments) != total:
        raise ValueError('owned program-copy extent differs from actual instruction bytes')
    return CompiledSoundCopyData(data, total, tuple(trees), native_source_root)


def combine_program_copy_data(*authorities: ReadOnlyData):
    """Join explicit code-copy and independent asset DATA without overriding.

    This view is for original software reads only. It grants no execution or
    missing-byte authority, and does not turn program bytes into asset ownership.
    """
    if not authorities or any(type(data) is not ReadOnlyData for data in authorities):
        raise ValueError('explicit nonoverlapping readonly source authorities required')
    return _joined([segment for data in authorities for segment in data.segments])


def driver_field_copy_data(driver_fields: dict, channel_view_fields: dict):
    """Encode external named driver tables at their actual physical sources.

    These are DATA, not compiled instructions. Earlier explicit audio-only
    preparation installed the same fields in sound RAM; the whole original
    bootstrap instead must read their source bytes and perform its own copies.
    No sound RAM, mailbox, register or Scene is written by this encoder.
    """
    segments = [(0x69D2 + base, raw) for base, raw in driver_static_data(driver_fields)]
    if (type(channel_view_fields) is not dict or channel_view_fields.get('format')
            != 'g5510-original-Z80-channel-view-tables-v1'):
        raise ValueError('explicit named original channel-view DATA required')
    tables = channel_view_fields.get('channel_view_tables')
    if type(tables) is not list or len(tables) != 3:
        raise ValueError('three explicit original channel-view tables required')
    for table, address, role in zip(tables, (0x6DC,0x6EC,0x6FC),
            ('paired_effect_views','active_effect_views','music_views')):
        if (type(table) is not dict or set(table) != {'address','role','targets'}
                or table['address'] != address or table['role'] != role):
            raise ValueError('complete original channel-view table identity required')
        targets = table['targets']
        if type(targets) is not list or len(targets) != 8:
            raise ValueError('eight explicitly named view references required')
        payload = b''.join(word(target).to_bytes(2,'little') for target in targets)
        segments.append((0x69D2 + address, payload))
    return _joined(segments)
