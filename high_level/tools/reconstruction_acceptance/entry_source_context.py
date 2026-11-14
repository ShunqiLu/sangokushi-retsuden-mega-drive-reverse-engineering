"""Bounded provenance for the existing App's actual readonly DATA owner.

The default context copies provenance and extents only. An explicit one-shot
attachment may also persist the existing immutable bytes in the same finite
store. Neither path reloads artifacts or proves their files remain frozen.
"""
from __future__ import annotations

import json
import os
import sys
import weakref

from .entry_capture_store import EntryCaptureStore, READONLY_DATA_CAPTURE_FORMAT


FORMAT = 'g5510-post-open-readonly-source-context-v1'
MAX_CONTEXT_JSON_BYTES = 32768
MAX_SEGMENTS = 4096
MAX_AUTHORITIES = 128
MAX_RESOURCES = 128
MAX_TEXT = 4096


class SourceContextError(ValueError):
    """An absent, competing or changed source owner is not substituted."""


def _require(value, message):
    if not value:
        raise SourceContextError(message)


def _exact_loaded(value, qualified):
    module_name, name = qualified.split(':', 1)
    module = sys.modules.get(module_name)
    expected = None if module is None else vars(module).get(name)
    return isinstance(expected, type) and type(value) is expected


def _object(value, label):
    _require(type(value) is dict, 'actual plain source evidence object required: ' + label)
    return value


def _text(value):
    _require(type(value) is str and 0 < len(value) <= MAX_TEXT
        and all(ord(character) >= 32 for character in value), 'bounded explicit source text required')
    return value


def _integer(value):
    _require(type(value) is int and 0 <= value < 1 << 63, 'explicit unsigned source integer required')
    return value


def _boolean(value):
    _require(type(value) is bool, 'explicit source evidence boolean required')
    return value


def _path(value):
    value = _text(value)
    _require(os.path.isabs(value), 'the selected artifact path must already be absolute')
    return value


def _select(row, *, integers=(), texts=(), paths=(), booleans=()):
    row = _object(row, 'selected evidence')
    result = {}
    for names, check in ((integers, _integer), (texts, _text),
            (paths, _path), (booleans, _boolean)):
        for name in names:
            if name in row:
                result[name] = check(row[name])
    return result


def _extent(row):
    result = _select(row, integers=('start', 'end', 'bytes', 'holes', 'competing_bytes'),
        booleans=('exact_partition',))
    _require(all(name in result for name in ('start', 'end', 'bytes')),
        'the complete selected cartridge extent is required')
    _require(result['end'] > result['start'] and result['end'] - result['start'] == result['bytes'],
        'selected cartridge extent and byte count differ')
    return result


def _evidence(source, project_root):
    evidence = _object(vars(source).get('evidence'), 'cartridge source')
    _require(evidence.get('format') == 'g5510-explicit-complete-cartridge-source-DATA-v1',
        'the actual complete cartridge source evidence format is required')
    selected = _select(evidence, texts=('format', 'confidence'),
        paths=('source_root', 'resource_manifest', 'm68k_native_root'),
        integers=('selected_authority_intervals',),
        booleans=('original_ROM_or_bank_input', 'analysis_opcode_payload_input',
            'sparse_padding_selected', 'legacy_M68K_assembly_authorities_selected'))
    _require(all(name in selected for name in ('source_root', 'resource_manifest')),
        'actual source root and resource manifest references are required')
    _require(os.path.normcase(os.path.normpath(selected['source_root']))
        == os.path.normcase(os.path.normpath(str(project_root))),
        'readonly source context belongs to another explicit project')
    selected['whole_cartridge'] = _extent(evidence.get('whole_cartridge'))
    m68k = _object(evidence.get('m68k'), 'M68K source')
    selected['m68k'] = _select(m68k,
        integers=('CODE_bytes', 'instructions', 'source_groups', 'unique_instruction_count'),
        paths=('source_root', 'native_build_root'), texts=('confidence',))
    authorities = m68k.get('authorities')
    _require(type(authorities) is list and 0 < len(authorities) <= MAX_AUTHORITIES,
        'bounded actual M68K authority references required')
    selected_authorities = []
    for authority in authorities:
        item = _select(authority, texts=('name',), integers=('instructions', 'CODE_bytes'),
            paths=('source', 'ledger', 'layout_ledger', 'elf', 'binary', 'native_object',
                'native_build_directory', 'generated_source', 'native_elf', 'native_image'),
            booleans=('complete_current_source_snapshots_match',
                'complete_current_generated_source_match',
                'complete_source_topology_and_object_labels_match',
                'complete_current_mnemonics_and_operands_match'))
        _require(any(name in item for name in ('source', 'native_build_directory', 'native_elf')),
            'an actual source/native artifact reference is required for every M68K authority')
        selected_authorities.append(item)
    selected['m68k']['authorities'] = selected_authorities
    selected['z80'] = _select(evidence.get('z80'), paths=('native_source_root',),
        integers=('CODE_bytes', 'current_whole_normalized_modules'))
    registered = _object(evidence.get('registered_DATA'), 'registered DATA')
    selected['registered_DATA'] = _select(registered, integers=('packages', 'bytes'))
    resources = registered.get('resource_ids')
    _require(type(resources) is list and 0 < len(resources) <= MAX_RESOURCES,
        'bounded actual registered resource identities required')
    selected['registered_DATA']['resource_ids'] = [_text(name) for name in resources]
    return selected


class ReadonlySourceContext:
    """One post-open same-Scene/source binding, without filesystem access.

    Every observation requires the same actual data/segment tuple, not equal
    replacement bytes. Optional persistence borrows those immutable bytes once;
    it neither reads the bus nor creates a runtime dependency on the capsule.
    """

    def __init__(self, source, scene, *, project_root):
        _require(_exact_loaded(source,
            'tools.high_level_main_flows.cartridge_source_data:CartridgeSourceData'),
            'the already-loaded actual CartridgeSourceData is required')
        _require(_exact_loaded(scene, 'tools.high_level_scene_flows.domain:SceneState'),
            'the actual normal App Scene is required')
        data = vars(source).get('data')
        _require(_exact_loaded(data, 'tools.high_level_scene_flows.domain:ReadOnlyData')
            and vars(scene).get('data') is data, 'App Scene and cartridge must use the same DATA owner')
        segments = vars(data).get('segments')
        _require(type(segments) is tuple and 0 < len(segments) <= MAX_SEGMENTS,
            'bounded actual readonly segment tuple required')
        extents, following = [], 0
        for segment in segments:
            _require(type(segment) is tuple and len(segment) == 2,
                'actual (base, immutable bytes) segment required')
            base, raw = segment
            _require(type(base) is int and base >= following and type(raw) is bytes
                and raw and base + len(raw) <= 0x1000000,
                'nonoverlapping immutable actual readonly segments required')
            following = base + len(raw)
            extents.append(dict(base=base, bytes=len(raw), end=following))
        selected = _evidence(source, project_root)
        whole = selected['whole_cartridge']
        _require(extents[0]['base'] == whole['start'] and following == whole['end']
            and sum(row['bytes'] for row in extents) == whole['bytes'],
            'actual readonly segment extents do not cover the declared selected cartridge')
        document = dict(format=FORMAT, context_key='same_App_post_open_readonly_source',
            selected_at='after_App_open_on_the_existing_owner_thread',
            same_Scene_cartridge_DATA_identity=True, segments=extents,
            selected_source_evidence=selected, DATA_payload_copied=False,
            artifact_files_read_or_hashed_here=False, artifact_files_frozen_proved=False,
            independent_reference_qualified=False, complete_device_state_qualified=False,
            strict_credit=0)
        encoded = json.dumps(document, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
        _require(len(encoded.encode('utf-8')) <= MAX_CONTEXT_JSON_BYTES,
            'selected source context exceeds its explicit32KiB JSON limit; not truncated')
        self._source = weakref.ref(source)
        self._scene = weakref.ref(scene)
        self._data, self._segments, self._encoded = data, segments, encoded
        self._payload_attempted = False
        self._payload_reference = None

    def _require_owner(self, scene):
        source = self._source()
        _require(source is not None and self._scene() is scene
            and vars(source).get('data') is self._data and vars(scene).get('data') is self._data
            and vars(self._data).get('segments') is self._segments,
            'post-open same-App readonly source ownership changed; no fallback')

    def persist_payload(self, scene, store):
        """Write one shared observed DATA capsule, not one ROM per case.

        Called only by the explicit post-open attachment, never from a live
        entry callback. The existing store owns every byte/case/disk budget and
        failure receipt. A budget stop is returned, not repaired or retried.
        """
        _require(type(store) is EntryCaptureStore and not self._payload_attempted,
            'one explicit same-store readonly DATA persistence attempt required')
        self._payload_attempted = True
        self._require_owner(scene)
        document = json.loads(self._encoded)
        expected_root = document['selected_source_evidence']['source_root']
        _require(os.path.normcase(os.path.normpath(str(store.project_root)))
            == os.path.normcase(os.path.normpath(expected_root)),
            'readonly DATA capsule store belongs to another project')
        segments, offset = [], 0
        for base, raw in self._segments:
            segments.append(dict(base=base, bytes=len(raw), end=base + len(raw),
                payload_offset=offset))
            offset += len(raw)
        payload = b''.join(raw for _, raw in self._segments)
        _require(len(payload) == offset == document['selected_source_evidence']['whole_cartridge']['bytes'],
            'complete actual immutable DATA payload geometry differs')
        metadata = dict(format=READONLY_DATA_CAPTURE_FORMAT,
            role='actual_same_App_readonly_DATA_not_original_reference_or_game_entry',
            source_context=document, segments=segments, DATA_bytes=len(payload),
            same_App_immutable_segment_bytes=True, original_ROM_read=False,
            DATA_bus_reads_added=0, artifact_files_read_or_hashed_here=False,
            runtime_source_modified=False, independent_reference_qualified=False,
            saved_initial_input_complete=False, directly_assemblable=False,
            strict_acceptance_status='not_evaluated', strict_credit=0)
        reference = dict(format=READONLY_DATA_CAPTURE_FORMAT,
            store_output=str(store.output), receipt='capture-receipt.json',
            receipt_key='readonly_data', metadata='readonly_data/input.json',
            path='readonly_data/source.data', bytes=len(payload),
            same_App_immutable_segment_bytes=True, independent_replay_qualified=False)
        # Reject an oversized final descriptor before writing its capsule, not
        # later from a live entry callback after attachment appeared to succeed.
        self._observation_document(reference)
        self._require_owner(scene)
        result = store.write_readonly_source(metadata, payload)
        self._require_owner(scene)
        if result['status'] == 'written':
            self._payload_reference = reference
        else:
            _require(result['status'] == 'budget_exhausted',
                'unknown shared readonly DATA writer outcome')
        return result

    def _observation_document(self, reference):
        document = json.loads(self._encoded)
        if reference is not None:
            document['DATA_payload_copied'] = True
            document['captured_DATA_payload'] = dict(reference)
        encoded = json.dumps(document, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
        _require(len(encoded.encode('utf-8')) <= MAX_CONTEXT_JSON_BYTES,
            'complete observed source context exceeds its32KiB bound; not truncated')
        return document

    def observation(self, scene):
        """Return a fresh descriptor; no source files, source writes or bus reads."""
        self._require_owner(scene)
        return self._observation_document(self._payload_reference)
