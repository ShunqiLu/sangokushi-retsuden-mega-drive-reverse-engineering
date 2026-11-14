"""A relocatable Scene entry for one already-published own resource tree.

The publishers supply their registered IDs after preparing the corresponding
sources. This module records references only: it does not encode, copy, merge
or fill DATA, and it never selects a research or machine-specific source root.
"""
from __future__ import annotations

import json
import os
from pathlib import Path


SCENE_SOURCE_MANIFEST = 'scene-sources.json'
SCENE_SOURCE_FORMAT = 'g5510-explicit-scene-source-roots-v1'


def scene_source_manifest_bytes(resource_ids: tuple[str, ...]) -> bytes:
    """Describe exactly the publisher's named packages under this same root.

    Whole-tree publishers pass every current registered ID exactly once.
    A deliberately selected typed-source publication passes only its actual
    subset. Neither case grants an additional resource ID or byte authority.
    The unchanged Scene loader still checks every registered source/member.
    """
    if (type(resource_ids) is not tuple or not resource_ids
            or any(type(ident) is not str or not ident for ident in resource_ids)
            or len(resource_ids) != len(set(resource_ids))):
        raise ValueError('explicit nonempty unique published resource IDs required')
    fields = dict(format=SCENE_SOURCE_FORMAT,
                  roots=[dict(path='.', ids=list(resource_ids))])
    return (json.dumps(fields, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def _unique_ids(value, context: str) -> tuple[str, ...]:
    if (type(value) not in (list, tuple) or not value
            or any(type(ident) is not str or not ident for ident in value)
            or len(value) != len(set(value))):
        raise ValueError(context + ': explicit nonempty unique resource IDs required')
    return tuple(value)


def _absolute_root(path: Path, directory: Path) -> Path:
    """Normalize explicit path syntax only; this pure step does not read files."""
    return Path(os.path.normpath(str(path if path.is_absolute() else directory / path)))


def _relocated_root(root: Path, directory: Path) -> str:
    try:
        return Path(os.path.relpath(root, directory)).as_posix()
    except ValueError:
        # A caller-named root on another drive has no relative representation.
        # Keep that same explicit absolute owner, never select another source.
        return root.as_posix()


def reassign_scene_source_manifest(fields: dict, *, source_directory: Path,
        output_directory: Path, resource_root: Path, resource_ids: tuple[str, ...],
        registered_resource_ids: tuple[str, ...]) -> dict:
    """Relocate a complete manifest while transferring only selected IDs.

    All input ownership is checked before removing anything: a duplicate ID,
    missing registration or unknown ID cannot disappear through reassignment.
    Other root/ID associations and their order are preserved. Empty old roots
    are omitted and the explicitly supplied replacement root is appended once.
    This pure function neither resolves filesystem links nor reads, encodes,
    copies or validates resource payloads; the normal loader still owns them.
    """
    if any(not isinstance(path, Path) or not path.is_absolute()
            for path in (source_directory, output_directory, resource_root)):
        raise ValueError('explicit absolute source/output directories and resource root required')
    registered = _unique_ids(registered_resource_ids, 'complete registration')
    selected = _unique_ids(resource_ids, 'reassignment')
    known, moved = set(registered), set(selected)
    if not moved <= known:
        raise ValueError('reassignment contains an unregistered resource ID')
    if (type(fields) is not dict or set(fields) != {'format', 'roots'}
            or fields['format'] != SCENE_SOURCE_FORMAT
            or type(fields['roots']) is not list or not fields['roots']):
        raise ValueError('complete explicit scene-source manifest required')
    original, seen = [], set()
    for row in fields['roots']:
        if (type(row) is not dict or set(row) != {'path', 'ids'}
                or type(row['path']) is not str or not row['path']
                or '\x00' in row['path']):
            raise ValueError('each original root requires its explicit path and resource IDs')
        ids = _unique_ids(row['ids'], 'original root')
        if any(ident not in known or ident in seen for ident in ids):
            raise ValueError('original manifest has an unknown or multiply owned resource ID')
        seen.update(ids)
        original.append((_absolute_root(Path(row['path']), source_directory), ids))
    if seen != known:
        raise ValueError('original manifest must own every registered resource exactly once')
    roots = []
    for root, ids in original:
        remaining = [ident for ident in ids if ident not in moved]
        if remaining:
            roots.append(dict(path=_relocated_root(root, output_directory), ids=remaining))
    roots.append(dict(path=_relocated_root(_absolute_root(resource_root, source_directory),
                                          output_directory), ids=list(selected)))
    return dict(format=SCENE_SOURCE_FORMAT, roots=roots)


def _ordinary_path(path: Path, *, directory: bool) -> Path:
    """Resolve a supplied existing local source without reparse traversal."""
    raw = str(path)
    if raw.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in raw[2:]:
        raise ValueError('UNC, device and alternate-stream source paths refused')
    absolute = path.absolute()
    for ancestor in (absolute, *absolute.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ValueError('source through a reparse point refused')
    resolved = absolute.resolve(strict=True)
    valid = resolved.is_dir() if directory else resolved.is_file()
    if not valid:
        raise ValueError('explicit existing source directory/file required')
    return resolved


def main(argv=None) -> int:
    """Publish one fresh complete ownership manifest, never asset payloads."""
    import argparse
    from .media_sources import _read, json_bytes, loads, member_path
    from .native import fresh_output
    from .resource_registry import RESOURCE_SPECS

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--source-manifest', type=Path, required=True)
    parser.add_argument('--resource-root', type=Path, required=True)
    parser.add_argument('--ids', nargs='+', required=True,
        help='registered IDs whose unique ownership moves to the explicit resource root')
    parser.add_argument('--output', type=Path, required=True,
        help='fresh project/build JSON with an existing parent; no source/member copying')
    args = parser.parse_args(argv)
    project = _ordinary_path(args.project_root, directory=True)
    source = _ordinary_path(args.source_manifest, directory=False)
    resource_root = _ordinary_path(args.resource_root, directory=True)
    output = fresh_output(args.output)
    if (not output.is_relative_to(project / 'build') or output == project / 'build'
            or output.suffix != '.json' or not output.parent.is_dir()):
        raise ValueError('fresh project/build JSON with an existing parent required')
    known = {spec.id: spec for spec in RESOURCE_SPECS}
    fields = reassign_scene_source_manifest(loads(_read(source, 131072)),
        source_directory=source.parent, output_directory=output.parent,
        resource_root=resource_root, resource_ids=tuple(args.ids),
        registered_resource_ids=tuple(known))
    # These are reference/path checks only. In particular no old payload is
    # reread and no selected codec, graph resolver or resource API is called.
    for row in fields['roots']:
        _ordinary_path(output.parent / row['path'], directory=True)
    for ident in args.ids:
        _ordinary_path(member_path(resource_root, known[ident].own_source), directory=False)
    raw = json_bytes(fields)
    if len(raw) > 131072:
        raise ValueError('relocated manifest exceeds the bounded source-manifest limit')
    with output.open('xb') as stream:
        stream.write(raw)
    print(json.dumps(dict(format='g5510-scene-source-reassignment-publication-v1',
        output=str(output), source_manifest=str(source), resource_root=str(resource_root),
        registered_resources=len(known), reassigned_resources=len(args.ids),
        reassigned_ids=args.ids, roots=len(fields['roots']), bytes=len(raw),
        complete_source_registration=True, resource_files_copied=0,
        resource_encoding_run=False, original_ROM_read=False, native_run=False,
        game_run=False, hash_run=False, new_strict_BYTES=0), ensure_ascii=False), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
