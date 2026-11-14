"""Explicit offline editing of an existing 8 KiB logical campaign save.

Export reads --source as a logical save and writes a fresh named JSON file.
Edit reads complete named JSON plus an explicit formatted --edits document.
Import requires named JSON and --original-logical, then writes a fresh .srm.
The packets-export/packets-edit/packets-import modes use the same file boundary
for the separate marching-group view; fixed-field export/edit/import stay intact.
The orders-export/orders-edit/orders-import modes select CE00 transport orders.
MAME's 16 KiB duplicated container belongs to save_format, not this interface.
No command changes an App configuration, live save medium or input file.

Examples (all output parents must already exist):
  python -m tools.save_data.campaign_cli export --project-root PROJECT \
      --source ORIGINAL.srm --output PROJECT/build/campaign.json
  python -m tools.save_data.campaign_cli edit --project-root PROJECT \
      --source PROJECT/build/campaign.json --edits EDITS.json \
      --output PROJECT/build/campaign-edited.json
  python -m tools.save_data.campaign_cli import --project-root PROJECT \
      --source PROJECT/build/campaign-edited.json --original-logical ORIGINAL.srm \
      --output PROJECT/build/campaign-edited.srm
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


MODE_VIEWS = {
    'export': ('fixed', 'export'),
    'edit': ('fixed', 'edit'),
    'import': ('fixed', 'import'),
    'packets-export': ('packets', 'export'),
    'packets-edit': ('packets', 'edit'),
    'packets-import': ('packets', 'import'),
    'orders-export': ('orders', 'export'),
    'orders-edit': ('orders', 'edit'),
    'orders-import': ('orders', 'import'),
}


def _input_file(path: Path, context: str) -> Path:
    """Use the normal lexical reparse/UNC/device/stream path boundary."""
    from ..high_level_rom.scene_manifest import _ordinary_path

    try:
        return _ordinary_path(path, directory=False)
    except (OSError, ValueError) as error:
        raise ValueError(context + ': an explicit existing ordinary file is required') from error


def _logical_input(path: Path, context: str) -> bytes:
    """Read exactly the logical size, with no container decoding or repair."""
    from .save_format import LOGICAL_SIZE, MAME_CONTAINER_SIZE

    source = _input_file(path, context)
    size = source.stat().st_size
    if size == MAME_CONTAINER_SIZE:
        raise ValueError('MAME 16 KiB containers are refused; use save_format explicitly')
    if size != LOGICAL_SIZE:
        raise ValueError(context + ': an explicit 8 KiB logical save is required')
    with source.open('rb') as stream:
        logical = stream.read(LOGICAL_SIZE + 1)
    if len(logical) != LOGICAL_SIZE:
        raise ValueError(context + ': logical save size changed during the bounded read')
    return logical


def _edit_list(path: Path, expected_format: str) -> list:
    """Unwrap the selected view's edit document; its pure adapter owns values."""
    from ..high_level_rom.readable_text import _load

    edits = _load(_input_file(path, '--edits'))
    if type(edits) is not dict or set(edits) != {'format', 'edits'}:
        raise ValueError('exact campaign edit document fields required')
    if type(edits['format']) is not str or edits['format'] != expected_format:
        raise ValueError('the selected campaign view edit format is required')
    if type(edits['edits']) is not list or not edits['edits']:
        raise ValueError('a nonempty explicit campaign edit list is required')
    return edits['edits']


def _output_file(project_path: Path, output_path: Path, mode: str) -> Path:
    """A new file inside this explicit project's existing build tree only."""
    from ..high_level_rom.native import fresh_output
    from ..high_level_rom.scene_manifest import _ordinary_path

    project = _ordinary_path(project_path, directory=True)
    build = _ordinary_path(project / 'build', directory=True)
    output = fresh_output(output_path)
    suffix = '.srm' if MODE_VIEWS[mode][1] == 'import' else '.json'
    if (not build.is_dir() or output == build or not output.is_relative_to(build)
            or not output.parent.is_dir() or output.suffix != suffix):
        raise ValueError('fresh ' + suffix + ' output inside project build with existing parent required')
    return output


def _result_bytes(args) -> bytes:
    """Delegate save semantics and encoding to the sole existing API chain."""
    from ..high_level_rom.media_sources import json_bytes, MAX_JSON
    from ..high_level_rom.readable_text import _load
    from . import named_campaign, campaign_packets, campaign_orders
    from .save_format import LOGICAL_SIZE

    view, operation = MODE_VIEWS[args.mode]
    adapter = {'fixed': named_campaign, 'packets': campaign_packets,
        'orders': campaign_orders}[view]
    if operation == 'export':
        result = adapter.from_logical(_logical_input(args.source, '--source'))
    else:
        named = _load(_input_file(args.source, '--source'))
        if operation == 'import':
            original = _logical_input(args.original_logical, '--original-logical')
            raw = adapter.to_logical(named, original)
            if type(raw) is not bytes or len(raw) != LOGICAL_SIZE:
                raise ValueError('campaign view API must return exactly 8 KiB logical bytes')
            return raw
        edit_format = adapter.edit_format_for(named) if view == 'packets' else adapter.EDIT_FORMAT
        result = adapter.with_edits(named, _edit_list(args.edits, edit_format))
    raw = json_bytes(result)
    if len(raw) > MAX_JSON:
        raise ValueError('campaign source exceeds the existing explicit JSON bound')
    return raw


def main(argv=None):
    """Reserve no directories; write one explicit fresh result after validation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=tuple(MODE_VIEWS))
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True,
        help='8 KiB logical input for export modes; complete selected-view JSON for edit/import')
    parser.add_argument('--edits', type=Path,
        help='selected-view edit document; required only for the three edit modes')
    parser.add_argument('--original-logical', type=Path,
        help='exact original 8 KiB logical baseline; required only for the three import modes')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    operation = MODE_VIEWS[args.mode][1]
    if (operation == 'edit') != (args.edits is not None):
        parser.error('--edits is required only for edit, packets-edit or orders-edit')
    if (operation == 'import') != (args.original_logical is not None):
        parser.error('--original-logical is required only for import, packets-import or orders-import')
    output = _output_file(args.project_root, args.output, args.mode)
    raw = _result_bytes(args)
    with output.open('xb') as destination:
        destination.write(raw)
    print(json.dumps(dict(output=str(output), mode=args.mode, bytes=len(raw),
        offline_campaign_save_only=True, live_save_replaced=False,
        original_ROM_read=False, hash_run=False, native_run=False,
        CPU_run=False, game_run=False, strict_acceptance=False), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
