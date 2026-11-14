"""Small explicit JSON entry for separately owned editable resource roots."""
import json
from pathlib import Path

from .resource_roots import load_scene_resource_roots


def read_scene_source_manifest(path: Path) -> tuple[tuple[Path, tuple[str, ...]], ...]:
    """Resolve only the named source roots relative to this supplied entry.

    No default path, research tree, ROM, reference result or environment path
    is selected. The manifest declares ownership, not encoded asset payloads.
    The existing per-package loader performs its original source/member checks.
    """
    if not isinstance(path, Path) or not path.is_file():
        raise ValueError('one explicit existing own-source manifest required')
    fields = json.loads(path.read_text(encoding='utf-8'))
    if (type(fields) is not dict or set(fields) != {'format', 'roots'}
            or fields['format'] != 'g5510-explicit-scene-source-roots-v1'
            or type(fields['roots']) is not list or not fields['roots']):
        raise ValueError('complete explicit scene-source root manifest required')
    roots = []
    for row in fields['roots']:
        if (type(row) is not dict or set(row) != {'path', 'ids'}
                or type(row['path']) is not str or not row['path']
                or type(row['ids']) is not list or not row['ids']
                or any(type(ident) is not str for ident in row['ids'])):
            raise ValueError('each root requires its named path and registered ID list')
        source = Path(row['path'])
        roots.append(((source if source.is_absolute() else path.parent / source).resolve(),
                      tuple(row['ids'])))
    return tuple(roots)


def load_scene_source_manifest(path: Path):
    """Encode the declared own roots into the existing SceneResourceBundle."""
    return load_scene_resource_roots(read_scene_source_manifest(path))
