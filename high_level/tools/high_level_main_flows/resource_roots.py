"""Compose explicit editable resource roots without duplicating source trees.

No path or package is selected implicitly. Existing independent encoders still
own every byte; duplicate IDs, overlapping physical DATA and missing sources
are errors even when competing bytes happen to match. This is not a ROM view.
"""
from pathlib import Path

from .domain import ReadOnlyData
from .runtime_resources import SceneResourceBundle, load_scene_resources


def load_scene_resource_roots(roots: tuple[tuple[Path, tuple[str, ...]], ...]) -> SceneResourceBundle:
    """Encode selected own packages from caller-named roots into one DATA view.

    The order of roots never grants override priority. Adjacent independently
    owned DATA segments may be joined so an original WORD/LONG read can cross
    their shared boundary; gaps are not filled and overlaps are not clipped.
    The live Scene/RAM/device object is created by the caller, not copied here.
    """
    if type(roots) is not tuple or not roots:
        raise ValueError('explicit nonempty tuple of own source roots required')
    selected, packages, segments = [], [], []
    for item in roots:
        if type(item) is not tuple or len(item) != 2:
            raise ValueError('each resource root requires its explicit selected ID tuple')
        source_root, ids = item
        if not isinstance(source_root, Path) or type(ids) is not tuple or not ids:
            raise ValueError('explicit Path and nonempty registered IDs required')
        if any(ident in selected for ident in ids):
            raise ValueError('one own resource package cannot be supplied by two roots')
        bundle = load_scene_resources(source_root, ids)
        selected.extend(bundle.resource_ids)
        packages.extend(bundle.package_confidence)
        segments.extend(bundle.data.segments)
    segments.sort(key=lambda row: row[0])
    joined = []
    for base, payload in segments:
        if joined:
            previous, data = joined[-1]
            end = previous + len(data)
            if base < end:
                raise ValueError('competing physical DATA ownership across explicit own roots')
            if base == end:
                joined[-1] = previous, data + payload
                continue
        joined.append((base, payload))
    return SceneResourceBundle(
        data=ReadOnlyData(tuple(joined)), resource_ids=tuple(selected),
        encoded_bytes=sum(len(data) for base, data in joined),
        package_confidence=tuple(packages),
    )
