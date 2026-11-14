"""Explicit optional entry-input capture configuration; no monitor on import.

The normal runtime schema and its budgets are unchanged. This separate opt-in
file only selects a current target catalog and a fresh finite input store.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from .config import ConfigurationError, _boolean, _integer, _no_duplicate_keys, _object, _text

if TYPE_CHECKING:
    from ..reconstruction_acceptance.m68k_entry_capture import M68KEntryCapture


FORMAT = 'g5510-entry-capture-config-v1'
AUDIO_FORMAT = 'g5510-entry-capture-config-v2'
PRE_CALL_FORMAT = 'g5510-entry-capture-config-v3'
CURRENT_PRE_CALL_FORMAT = 'g5510-entry-capture-config-v4'
READONLY_PAYLOAD_FORMAT = 'g5510-entry-capture-config-v5'
VDP_STATE_FORMAT = 'g5510-entry-capture-config-v6'
MAX_JSON_BYTES = 65536
MAX_CASES = 4096
MAX_CAPTURES_PER_ENTRY = 64
MAX_TOTAL_BYTES = 512 * 1024 * 1024
MAX_CASE_JSON_BYTES = 1024 * 1024
MAX_FREE_RESERVE_BYTES = (1 << 63) - 1
MAX_AUDIO_CASE_DATA_OPERATIONS = (1 << 63) - 1
FIELDS = ('format', 'batch', 'output', 'tool_id', 'max_cases', 'max_captures_per_entry',
    'max_total_bytes', 'max_case_json_bytes', 'min_free_bytes')


def _explicit_path(value, directory: Path, context: str) -> Path:
    text = _text(value, context)
    if text.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in text[2:]:
        raise ConfigurationError(context + '拒绝UNC、device或ADS路径。')
    path = Path(text)
    if (path.drive or path.root) and not path.is_absolute():
        raise ConfigurationError(context + '必须是完整绝对路径或相对本配置目录的普通路径。')
    path = (path if path.is_absolute() else directory / path).absolute()
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ConfigurationError(context + '不能通过reparse路径。')
    return path


def _existing_file(path: Path, context: str) -> Path:
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise ConfigurationError(context + '必须是调用方明确提供的现有文件：' + str(path)) from error
    if not resolved.is_file():
        raise ConfigurationError(context + '必须是现有普通文件：' + str(path))
    return resolved


def _nonfinite(value):
    raise ConfigurationError('入口捕获配置不允许非有限数：' + value)


def _read_config(path: Path):
    source = _existing_file(_explicit_path(str(path), Path.cwd(), 'capture_entries'),
        'capture_entries')
    try:
        with source.open('rb') as stream:
            raw = stream.read(MAX_JSON_BYTES + 1)
        if len(raw) > MAX_JSON_BYTES:
            raise ConfigurationError('入口捕获配置超过明确64KiB文件上限。')
        document = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_no_duplicate_keys,
            parse_constant=_nonfinite)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ConfigurationError('无法读取入口捕获配置：' + str(source)) from error
    version = document.get('format') if type(document) is dict else None
    if version in (READONLY_PAYLOAD_FORMAT, VDP_STATE_FORMAT):
        keys = FIELDS + ('audio', 'pre_call', 'readonly_DATA')
    elif version in (PRE_CALL_FORMAT, CURRENT_PRE_CALL_FORMAT):
        keys = FIELDS + ('audio', 'pre_call')
    else:
        keys = FIELDS + ('audio',) if version == AUDIO_FORMAT else FIELDS
    row = _object(document, keys, 'capture_entries')
    if row['format'] not in (FORMAT, AUDIO_FORMAT, PRE_CALL_FORMAT, CURRENT_PRE_CALL_FORMAT,
            READONLY_PAYLOAD_FORMAT, VDP_STATE_FORMAT):
        raise ConfigurationError('入口捕获配置format不匹配，不能猜测其它输入格式。')
    audio = None
    if version in (AUDIO_FORMAT, PRE_CALL_FORMAT, CURRENT_PRE_CALL_FORMAT, READONLY_PAYLOAD_FORMAT, VDP_STATE_FORMAT):
        audio_row = _object(row['audio'], ('max_DATA_operations',), 'capture_entries.audio')
        audio = dict(max_DATA_operations=_integer(audio_row['max_DATA_operations'],
            'capture_entries.audio.max_DATA_operations', 1, MAX_AUDIO_CASE_DATA_OPERATIONS))
    pre_call = None
    if version in (PRE_CALL_FORMAT, CURRENT_PRE_CALL_FORMAT, READONLY_PAYLOAD_FORMAT, VDP_STATE_FORMAT):
        pre_call_keys = (('enabled', 'include_current_source_calls', 'capture_vdp_state')
            if version == VDP_STATE_FORMAT else ('enabled', 'include_current_source_calls')
            if version in (CURRENT_PRE_CALL_FORMAT, READONLY_PAYLOAD_FORMAT) else ('enabled',))
        pre_call_row = _object(row['pre_call'], pre_call_keys, 'capture_entries.pre_call')
        pre_call = dict(enabled=_boolean(pre_call_row['enabled'],
            'capture_entries.pre_call.enabled'))
        if version in (CURRENT_PRE_CALL_FORMAT, READONLY_PAYLOAD_FORMAT, VDP_STATE_FORMAT):
            pre_call['include_current_source_calls'] = _boolean(
                pre_call_row['include_current_source_calls'],
                'capture_entries.pre_call.include_current_source_calls')
        if version == VDP_STATE_FORMAT:
            pre_call['capture_vdp_state'] = _boolean(pre_call_row['capture_vdp_state'],
                'capture_entries.pre_call.capture_vdp_state')
            if pre_call['capture_vdp_state'] and not pre_call['enabled']:
                raise ConfigurationError('VDP状态采集必须明确启用同一pre-CALL采集。')
    batch = _existing_file(_explicit_path(row['batch'], source.parent, 'capture_entries.batch'),
        'capture_entries.batch')
    output = _explicit_path(row['output'], source.parent, 'capture_entries.output')
    limits = dict(
        tool_id=_integer(row['tool_id'], 'capture_entries.tool_id', 0, 5),
        max_cases=_integer(row['max_cases'], 'capture_entries.max_cases', 1, MAX_CASES),
        max_captures_per_entry=_integer(row['max_captures_per_entry'],
            'capture_entries.max_captures_per_entry', 1, MAX_CAPTURES_PER_ENTRY),
        max_total_bytes=_integer(row['max_total_bytes'],
            'capture_entries.max_total_bytes', 1, MAX_TOTAL_BYTES),
        max_case_json_bytes=_integer(row['max_case_json_bytes'],
            'capture_entries.max_case_json_bytes', 1, MAX_CASE_JSON_BYTES),
        min_free_bytes=_integer(row['min_free_bytes'],
            'capture_entries.min_free_bytes', 0, MAX_FREE_RESERVE_BYTES))
    if version in (READONLY_PAYLOAD_FORMAT, VDP_STATE_FORMAT):
        data_row = _object(row['readonly_DATA'], ('persist_payload',), 'capture_entries.readonly_DATA')
        limits['persist_readonly_DATA'] = _boolean(data_row['persist_payload'],
            'capture_entries.readonly_DATA.persist_payload')
    if limits['max_case_json_bytes'] > limits['max_total_bytes']:
        raise ConfigurationError('单case JSON上限不能大于总捕获文件预算。')
    return batch, output, limits, audio, pre_call


def load_configured_entry_capture(path: Path, *, project_root: Path) -> M68KEntryCapture:
    """Construct once without starting a monitor or reading live game state.

    Source qualification happens before the store creates its fresh directory.
    Constructor failure still attempts one failure receipt and preserves the
    original exception, including cancellation, if receipt cleanup also fails.
    """
    if not isinstance(path, Path) or not isinstance(project_root, Path):
        raise ConfigurationError('必须明确提供Path类型的捕获配置及当前runtime工程根。')
    batch, output, limits, audio, pre_call = _read_config(path)
    from ..reconstruction_acceptance.entry_capture_catalog import load_capture_targets
    from ..reconstruction_acceptance.m68k_entry_capture import M68KEntryCapture
    targets = load_capture_targets(batch, project_root)
    audio_targets = None
    if audio is not None:
        from ..reconstruction_acceptance.z80_entry_capture_catalog import load_z80_capture_targets
        audio_targets = load_z80_capture_targets(batch, project_root)
    pre_call_index = helper_forms = None
    if pre_call is not None and pre_call['enabled']:
        from ..reconstruction_acceptance.pre_call_capture_catalog import prepare_pre_call_index
        from ..reconstruction_acceptance.pre_call_source_views import prepare_helper_forms
        pre_call_index = prepare_pre_call_index(batch, project_root, prepared_targets=targets,
            include_current_source_calls=pre_call.get('include_current_source_calls', False))
        helper_forms = prepare_helper_forms(pre_call_index)
    from ..reconstruction_acceptance.entry_capture_store import EntryCaptureStore
    store = EntryCaptureStore(project_root, output,
        max_cases=limits['max_cases'], max_total_bytes=limits['max_total_bytes'],
        max_case_json_bytes=limits['max_case_json_bytes'], min_free_bytes=limits['min_free_bytes'])
    try:
        observer = None
        if audio is not None:
            from ..reconstruction_acceptance.z80_entry_capture import Z80EntryObserver
            observer = Z80EntryObserver(audio_targets, store,
                max_captures_per_entry=limits['max_captures_per_entry'],
                max_DATA_operations=audio['max_DATA_operations'])
        if pre_call_index is not None:
            from ..reconstruction_acceptance.m68k_pre_call_capture import M68KPreCallObserver
            preobserver = M68KPreCallObserver(pre_call_index, helper_forms, store,
                max_captures_per_entry=limits['max_captures_per_entry'],
                capture_vdp_state=pre_call.get('capture_vdp_state', False))
            return M68KEntryCapture(targets, store, tool_id=limits['tool_id'],
                max_captures_per_entry=limits['max_captures_per_entry'],
                audio_observer=observer, pre_call_observer=preobserver,
                persist_readonly_DATA=limits.get('persist_readonly_DATA', False))
        if observer is not None:
            return M68KEntryCapture(targets, store, tool_id=limits['tool_id'],
                max_captures_per_entry=limits['max_captures_per_entry'], audio_observer=observer,
                persist_readonly_DATA=limits.get('persist_readonly_DATA', False))
        return M68KEntryCapture(targets, store, tool_id=limits['tool_id'],
            max_captures_per_entry=limits['max_captures_per_entry'],
            persist_readonly_DATA=limits.get('persist_readonly_DATA', False))
    except BaseException as error:
        try:
            store.close('monitor_construction_failed')
        except BaseException as cleanup_error:
            error.add_note('入口捕获构造失败后的收据关闭也失败，未覆盖或重试：'
                + type(cleanup_error).__name__ + '：' + str(cleanup_error))
        raise
