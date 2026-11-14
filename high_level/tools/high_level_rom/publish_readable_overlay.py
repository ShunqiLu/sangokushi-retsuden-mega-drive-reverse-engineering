"""Publish explicit editable sources over one complete media resource root.

This is source publication, not resource encoding, a ROM build or a test. The
existing Scene multi-root protocol assigns every registered ID exactly once:
dialogue_text is copied, with optional named scenario, AI-cutoff and AI-selection
sources. Every other resource remains at the supplied base; no media tree is copied.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .ai_policy_sources import (FORMAT as AI_CUTOFFS_FORMAT,
    RESOURCE_ID as AI_CUTOFFS_ID, from_named as ai_cutoffs_from_named)
from .ai_selection_sources import (FORMAT as AI_SELECTION_FORMAT,
    RESOURCE_ID as AI_SELECTION_ID, from_named as ai_selection_from_named)
from .media_sources import MAX_JSON, _read, loads
from .native import fresh_output
from .readable_text import FORMAT as READABLE_FORMAT, COLLECTIONS
from .resource_registry import RESOURCE_SPECS
from .scenario_sources import FORMAT as SCENARIO_FORMAT, from_named as scenario_from_named
from .scene_manifest import SCENE_SOURCE_FORMAT, SCENE_SOURCE_MANIFEST


def _ordinary(path: Path, *, directory=False) -> Path:
    raw = str(path)
    if raw.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in raw[2:]:
        raise ValueError('UNC, device and alternate-stream source paths refused')
    path = Path(path).absolute()
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ValueError('source publication through reparse points refused')
    path = path.resolve(strict=True)
    if not (path.is_dir() if directory else path.is_file()):
        raise ValueError('explicit ordinary source file/root required')
    return path


def _json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def _source_payload(path: Path, resource_id: str) -> tuple[Path, bytes, str]:
    """Validate the same bounded bytes that will be copied, without a codec."""
    source = _ordinary(path)
    raw = _read(source, MAX_JSON)
    fields = loads(raw)
    if type(fields) is not dict:
        raise ValueError('complete editable resource source object required')
    if resource_id == 'dialogue_text':
        if fields.get('format') != READABLE_FORMAT:
            raise ValueError('explicit owned Unicode dialogue source required')
        for name, count, _ in COLLECTIONS:
            if type(fields.get(name)) is not list or len(fields[name]) != count:
                raise ValueError('complete readable collection required: ' + name)
    elif resource_id == 'scenario_build':
        if fields.get('format') != SCENARIO_FORMAT:
            raise ValueError('explicit named scenario source required')
        scenario_from_named(fields)
    elif resource_id == AI_CUTOFFS_ID:
        if fields.get('format') != AI_CUTOFFS_FORMAT:
            raise ValueError('explicit named AI cutoff source required')
        ai_cutoffs_from_named(fields)
    elif resource_id == AI_SELECTION_ID:
        if fields.get('format') != AI_SELECTION_FORMAT:
            raise ValueError('explicit named AI candidate first-gate source required')
        ai_selection_from_named(fields)
    else:
        raise ValueError('resource is not one of the finite editable overlay owners')
    return source, raw, fields['format']


def _complete_base(path: Path) -> tuple[Path, tuple[str, ...]]:
    """Read the sole complete base using the existing Scene manifest shape."""
    fields = loads(_read(path, MAX_JSON))
    if (type(fields) is not dict or set(fields) != {'format', 'roots'}
            or fields['format'] != SCENE_SOURCE_FORMAT
            or type(fields['roots']) is not list or len(fields['roots']) != 1):
        raise ValueError('one explicit complete128-package base source root required')
    row = fields['roots'][0]
    if (type(row) is not dict or set(row) != {'path', 'ids'}
            or type(row['path']) is not str or not row['path']
            or type(row['ids']) is not list
            or any(type(ident) is not str for ident in row['ids'])):
        raise ValueError('base root requires its explicit path and complete registered IDs')
    known = tuple(spec.id for spec in RESOURCE_SPECS)
    ids = tuple(row['ids'])
    if (len(known) != 128 or len(set(known)) != len(known)
            or len(ids) != len(known) or set(ids) != set(known)):
        raise ValueError('one explicit complete128-package base source root required')
    base = Path(row['path'])
    return _ordinary(base if base.is_absolute() else path.parent / base,
        directory=True), ids


def publish(readable_source: Path, base_manifest: Path, output: Path, *,
        scenario_source: Path | None = None, ai_cutoffs_source: Path | None = None,
        ai_selection_source: Path | None = None) -> dict:
    """Create a fresh small source overlay; no codec, CPU or native invocation.

    The original three positional arguments still publish only dialogue. Each
    supplied optional named JSON moves only its exact registered ID. Supplied
    source bytes are preserved exactly; normal resource encoding occurs only
    when the application actually consumes this manifest. There is no fallback.
    """
    base_manifest = _ordinary(base_manifest)
    target = fresh_output(output)
    inputs = [('dialogue_text', readable_source)]
    if scenario_source is not None:
        inputs.append(('scenario_build', scenario_source))
    if ai_cutoffs_source is not None:
        inputs.append((AI_CUTOFFS_ID, ai_cutoffs_source))
    if ai_selection_source is not None:
        inputs.append((AI_SELECTION_ID, ai_selection_source))
    payloads = [(ident, *_source_payload(path, ident)) for ident, path in inputs]
    base, ids = _complete_base(base_manifest)
    if target == base or target.is_relative_to(base) or base.is_relative_to(target):
        raise ValueError('fresh overlay must not contain or modify its frozen base root')
    input_files = [base_manifest, *(source for _, source, _, _ in payloads)]
    if any(target == path or target.is_relative_to(path) or path.is_relative_to(target)
            for path in input_files):
        raise ValueError('fresh overlay must not overlap any explicit input source')
    if any(path.drive.casefold() != target.drive.casefold() for path in (base, *input_files)):
        raise ValueError('source overlay must stay on the explicit inputs same drive')
    relative_base = Path(os.path.relpath(base, target)).as_posix()
    overlay_ids = [ident for ident, _, _, _ in payloads]
    retained = [ident for ident in ids if ident not in overlay_ids]
    if (len(set(overlay_ids)) != len(overlay_ids)
            or len(retained) + len(overlay_ids) != len(ids)):
        raise ValueError('each selected registered resource must move exactly once')
    manifest = dict(format=SCENE_SOURCE_FORMAT, roots=[
        dict(path=relative_base, ids=retained), dict(path='.', ids=overlay_ids)])
    own_sources = {spec.id: spec.own_source for spec in RESOURCE_SPECS}
    expected_paths = dict(dialogue_text='resources/data/dialogue_text.json',
        scenario_build='resources/data/scenario_build.json',
        ai_threshold_pair_fields='resources/data/ai_threshold_pair_fields.json',
        ai_selection_fields='resources/data/ai_selection_fields.json')
    if any(own_sources[ident] != expected_paths[ident] for ident in overlay_ids):
        raise ValueError('current registered editable own-source path changed')
    copied_sources = [dict(id=ident, source=str(source), own_source=own_sources[ident],
        format=source_format, source_bytes=len(raw), copied_bytes=0)
        for ident, source, raw, source_format in payloads]
    source = payloads[0][1]
    receipt = dict(format='g5510-readable-dialogue-overlay-publication-v1', status='publishing',
        source=str(source), base_manifest=str(base_manifest), base_root=str(base),
        output=str(target), scene_source_manifest=SCENE_SOURCE_MANIFEST,
        readable_dialogue_source=own_sources['dialogue_text'], copied_dialogue_bytes=0,
        readable_items=sum(count for _, count, _ in COLLECTIONS),
        copied_sources=copied_sources, copied_resource_ids=[], copied_source_bytes=0,
        selected_resource_ids=overlay_ids,
        base_resource_ids=len(retained), overlay_resource_ids=len(overlay_ids),
        complete_unique_resource_ids=len(ids),
        audio_root=str(base), image_sources_copied=0, base_modified=False,
        resource_encoding_run=False, game_run=False, CPU_run=False, native_run=False,
        original_ROM_read=False, comparison_run=False, hash_run=False,
        source_publication_not_runtime_or_strict_acceptance=True,
        strict_pending_unchanged=46004, files_written=[])
    target.mkdir(parents=True, exist_ok=False)
    try:
        for index, (ident, _, raw, _) in enumerate(payloads):
            payload = target / own_sources[ident]
            payload.parent.mkdir(parents=True, exist_ok=True)
            with payload.open('xb') as stream:
                stream.write(raw)
            receipt['files_written'].append(own_sources[ident])
            receipt['copied_sources'][index]['copied_bytes'] = len(raw)
            receipt['copied_resource_ids'].append(ident)
            receipt['copied_source_bytes'] += len(raw)
            if ident == 'dialogue_text':
                receipt['copied_dialogue_bytes'] = len(raw)
        with (target / SCENE_SOURCE_MANIFEST).open('xb') as stream:
            stream.write(_json_bytes(manifest))
        receipt['files_written'].append(SCENE_SOURCE_MANIFEST)
        receipt['status'] = 'published'
    except (OSError, ValueError) as error:
        receipt.update(status='publication_failed', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        with (target / 'publication-receipt.json').open('xb') as stream:
            stream.write(_json_bytes(receipt))
    return receipt


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--readable-source', type=Path, required=True)
    parser.add_argument('--base-manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--scenario-source', type=Path,
        help='可选明确的具名scenario_build JSON；只替换该登记资源')
    parser.add_argument('--ai-cutoffs-source', type=Path,
        help='可选明确的具名AI比较WORD JSON；只替换ai_threshold_pair_fields')
    parser.add_argument('--ai-selection-source', type=Path,
        help='可选明确的具名AI候选首道资格BYTE JSON；只替换ai_selection_fields')
    args = parser.parse_args(argv)
    print(json.dumps(publish(args.readable_source, args.base_manifest, args.output,
        scenario_source=args.scenario_source, ai_cutoffs_source=args.ai_cutoffs_source,
        ai_selection_source=args.ai_selection_source),
        ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
