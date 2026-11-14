"""Load explicitly owned editable resources into the recovered Scene runtime.

The existing independent encoders own the file formats. This layer gives their
selected output to the actual business memory interface, without a reference
ROM, native code, workspace-analysis fallback, or embedded media payload.
Missing sources, code intersections and competing owners remain errors.
"""
from dataclasses import dataclass
from pathlib import Path

from .domain import ReadOnlyData
from ..high_level_rom.media_sources import member_path
from ..high_level_rom.resource_registry import RESOURCE_SPECS, load_resources


@dataclass(frozen=True)
class SceneResourceBundle:
    """One loaded DATA view and the selected source authorities behind it."""

    data: ReadOnlyData
    resource_ids: tuple[str, ...]
    encoded_bytes: int
    package_confidence: tuple[tuple[str, str], ...]


def load_scene_resources(source_root: Path, resource_ids: tuple[str, ...]) -> SceneResourceBundle:
    """Encode caller-selected own resource files, then expose their DATA only.

    Plain typed JSON and the existing external PNG/member graphs share the same
    encoders. Adjacent physical DATA blocks are joined so WORD/LONG reads can
    cross a source-block boundary. Overlap is never merged or silently clipped;
    editable files retain their separate ownership in the existing registry.
    """
    if not isinstance(source_root, Path) or not source_root.is_dir():
        raise ValueError('explicit existing own resource directory required')
    if (type(resource_ids) is not tuple or not resource_ids
            or any(type(ident) is not str for ident in resource_ids)
            or len(resource_ids) != len(set(resource_ids))):
        raise ValueError('explicit nonempty unique resource ID tuple required')
    known = {spec.id: spec for spec in RESOURCE_SPECS}
    if any(ident not in known for ident in resource_ids):
        raise ValueError('only registered own resource IDs may supply Scene DATA')
    # Check the supplied path before resolving it; primary JSON may not hide a
    # reparse point any more than an external graph member may.
    for ident in resource_ids:
        member_path(source_root, known[ident].own_source)
    encoded = load_resources(source_root=source_root, ids=resource_ids,
                             allow_unavailable=False)
    if not encoded['coverage']['complete_selected_resources']:
        raise ValueError('selected Scene resource ownership is incomplete')
    segments = []
    for row in encoded['blocks']:
        start, payload = row['start'], row['data']
        if segments and start < segments[-1][0] + len(segments[-1][1]):
            raise ValueError('competing Scene resource DATA ownership')
        if segments and start == segments[-1][0] + len(segments[-1][1]):
            base, previous = segments[-1]
            segments[-1] = (base, previous + payload)
        else:
            segments.append((start, payload))
    data = ReadOnlyData(tuple(segments))
    return SceneResourceBundle(
        data=data, resource_ids=resource_ids,
        encoded_bytes=sum(len(payload) for start, payload in segments),
        package_confidence=tuple((row['id'], row['confidence'])
                                 for row in encoded['packages']),
    )
