"""Finite fresh-file storage for actual entry inputs, not behavioral results.

The caller supplies metadata and already-observed bytes. Entry RAM and the
optional one-store readonly DATA capsule remain distinct artifact formats.
This writer never reads a Scene, decodes RAM, constructs a Frame or changes a CALL.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil

from ..high_level_rom.native import fresh_output


M68K_CAPTURE_FORMAT = 'g5510-actual-m68k-entry-capture-v1'
M68K_PRE_CALL_CAPTURE_FORMAT = 'g5510-actual-m68k-pre-CALL-capture-v1'
Z80_CAPTURE_FORMAT = 'g5510-actual-z80-entry-capture-v1'
READONLY_DATA_CAPTURE_FORMAT = 'g5510-actual-readonly-DATA-capture-v1'
RECEIPT_FORMAT = 'g5510-finite-entry-capture-store-v1'
RAM_CAPTURE_FORMATS = (M68K_CAPTURE_FORMAT, M68K_PRE_CALL_CAPTURE_FORMAT, Z80_CAPTURE_FORMAT)
CAPTURE_FORMATS = RAM_CAPTURE_FORMATS + (READONLY_DATA_CAPTURE_FORMAT,)
RAM_FIELD = 'captured_ram'
VDP_FIELD = 'captured_vdp_state'
VDP_STATE_FORMAT = 'g5510-vdp-command-memory-state-v1'
VDP_PAYLOAD_BYTES = 65776
RECEIPT_NAME = 'capture-receipt.json'
MAX_KEY = 80
MAX_OUTCOME = 128
MAX_ERROR = 512
MAX_ERROR_TYPE = 96
MAX_STAGE = 64
MAX_INTEGER = (1 << 63) - 1


class EntryCaptureWriteError(OSError):
    """An I/O/path failure poisons this store; artifacts are never retried."""

    def __init__(self, output: Path, failure: dict):
        super().__init__('entry input storage stopped; partial files retained at ' + str(output))
        self.output = output
        self.failure = dict(failure)


class _JsonBudgetExceeded(ValueError):
    pass


def _integer(value, label, *, minimum=0):
    if type(value) is not int or not minimum <= value <= MAX_INTEGER:
        raise ValueError('explicit finite integer required: ' + label)
    return value


def _ordinary_directory(path: Path) -> Path:
    raw = str(path)
    if raw.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in raw[2:]:
        raise ValueError('UNC, device and alternate-stream capture paths refused')
    absolute = path.absolute()
    for ancestor in (absolute, *absolute.parents):
        if ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)():
            raise ValueError('capture paths through a reparse point refused')
    resolved = absolute.resolve(strict=True)
    if not resolved.is_dir():
        raise ValueError('ordinary existing capture parent/project directory required')
    return resolved


def _safe_key(key: str) -> str:
    if (type(key) is not str or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', key) is None
            or re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])', key)):
        raise ValueError('one safe ASCII capture directory ID, at most80 characters, required')
    return key


def _json_bytes(document: dict, maximum: int) -> bytes:
    """Bound the serialized artifact, not an estimate of its input objects."""
    pending, seen = [document], set()
    while pending:
        value = pending.pop()
        if type(value) in (dict, list, tuple):
            if id(value) in seen:
                continue
            seen.add(id(value))
            if type(value) is dict:
                if any(type(key) is not str for key in value):
                    raise ValueError('capture JSON object keys must already be strings')
                pending.extend(value.values())
            else:
                pending.extend(value)
        elif value is not None and type(value) not in (str, int, float, bool):
            raise ValueError('capture JSON must contain only explicit plain serializable values')
    encoder = json.JSONEncoder(ensure_ascii=False, allow_nan=False, indent=2)
    chunks, size = [], 0
    for text in encoder.iterencode(document):
        raw = text.encode('utf-8')
        size += len(raw)
        if size + 1 > maximum:
            raise _JsonBudgetExceeded('capture JSON exceeds its explicit byte budget')
        chunks.append(raw)
    return b''.join(chunks) + b'\n'


def _record_payload(record):
    """Only the two fixed internal layouts; never a caller-selected filename."""
    if record['format'] == READONLY_DATA_CAPTURE_FORMAT:
        if (record['key'] != 'readonly_data' or record.get('payload_filename') != 'source.data'
                or record.get('input_DATA') != 'readonly_data/source.data'):
            raise ValueError('readonly DATA receipt row lost its fixed payload ownership')
        return 'DATA', 'source.data'
    return 'ram', 'input.ram'


def _record_artifacts(record):
    """Every file in one case is charged, observed and poisoned together."""
    artifacts = [('json', 'input.json'), _record_payload(record)]
    if 'input_VDP' in record:
        if (record['format'] != M68K_PRE_CALL_CAPTURE_FORMAT
                or record['input_VDP'] != record['key'] + '/vdp.data'
                or record['VDP_bytes'] != VDP_PAYLOAD_BYTES):
            raise ValueError('VDP receipt row lost its fixed same-case payload ownership')
        artifacts.append(('VDP', 'vdp.data'))
    return tuple(artifacts)


class EntryCaptureStore:
    """One bounded output directory; no deletion, overwrite, refill or replay."""

    def __init__(self, project_root, output, *, max_cases: int, max_total_bytes: int,
            max_case_json_bytes: int, min_free_bytes: int):
        self.project_root = _ordinary_directory(Path(project_root))
        build = _ordinary_directory(self.project_root / 'build')
        self.output = fresh_output(Path(output))
        if self.output == build or not self.output.is_relative_to(build):
            raise ValueError('a dedicated fresh directory inside the explicit project build required')
        _ordinary_directory(self.output.parent)
        self.max_cases = _integer(max_cases, 'max_cases', minimum=1)
        self.max_total_bytes = _integer(max_total_bytes, 'max_total_bytes', minimum=1)
        self.max_case_json_bytes = _integer(max_case_json_bytes, 'max_case_json_bytes', minimum=1)
        self.min_free_bytes = _integer(min_free_bytes, 'min_free_bytes')
        self._records = []
        self._keys = set()
        self._charged_payload_bytes = 0
        self._budget_stop = None
        self._failure = None
        self._closed = False
        self._close_attempted = False
        self._closed_outcome = None
        self._receipt_reserve = self._reserve_receipt([])
        if self._receipt_reserve > self.max_total_bytes:
            raise ValueError('max_total_bytes cannot reserve even the bounded final receipt')
        if shutil.disk_usage(self.output.parent).free < self.min_free_bytes + self._receipt_reserve:
            raise ValueError('insufficient free bytes for the explicit reserve and final receipt')
        self.output.mkdir(exist_ok=False)

    def _receipt_document(self, outcome, records, *, failure, budget_stop, reserve):
        return dict(format=RECEIPT_FORMAT, outcome=outcome, input_collection_only=True,
            acceptance_status='not_evaluated', strict_credit=0,
            project_root=str(self.project_root), output=str(self.output),
            limits=dict(max_cases=self.max_cases, max_total_bytes=self.max_total_bytes,
                max_case_json_bytes=self.max_case_json_bytes, min_free_bytes=self.min_free_bytes),
            cases=records, completed_cases=sum(row['status'] == 'written' for row in records),
            charged_payload_bytes=self._charged_payload_bytes,
            known_written_payload_bytes=sum((row[kind + '_bytes_written'] or 0)
                for row in records for kind, _ in _record_artifacts(row)),
            partial_size_unknown=any(row[kind + '_bytes_written'] is None
                for row in records for kind, _ in _record_artifacts(row)),
            receipt_budget_reserved_bytes=reserve,
            budget_exhausted=budget_stop, write_failure=failure,
            deletion_run=False, overwrite_run=False, writer_modified_original_RAM_or_CALL=False)

    def _reserve_receipt(self, records) -> int:
        # JSON control characters require six bytes, at least as many as any
        # UTF8 scalar here. Fixed integer padding covers four <=63-bit fields
        # whose digit count can grow before close. No RAM/metadata is embedded.
        failure = dict(stage='\x00' * MAX_STAGE, key='\x00' * MAX_KEY,
            error_type='\x00' * MAX_ERROR_TYPE, message='\x00' * MAX_ERROR)
        document = self._receipt_document('\x00' * MAX_OUTCOME, records,
            failure=failure, budget_stop='\x00' * MAX_STAGE, reserve=0)
        raw = _json_bytes(document, MAX_INTEGER)
        return len(raw) + 128

    def _budget_exhausted(self, reason):
        self._budget_stop = reason
        return dict(status='budget_exhausted', reason=reason,
            completed_cases=sum(row['status'] == 'written' for row in self._records),
            charged_payload_bytes=self._charged_payload_bytes,
            max_cases=self.max_cases, max_total_bytes=self.max_total_bytes,
            strict_credit=0)

    def _require_writable(self):
        if self._failure is not None:
            raise EntryCaptureWriteError(self.output, self._failure)
        if self._closed or self._close_attempted:
            raise ValueError('a closed capture store cannot accept more cases')

    def _failure_record(self, error, stage, key):
        return dict(stage=stage[:MAX_STAGE], key=key[:MAX_KEY],
            error_type=type(error).__name__[:MAX_ERROR_TYPE], message=str(error)[:MAX_ERROR])

    def _observe_partial(self, record):
        for kind, filename in _record_artifacts(record):
            if not record[kind + '_created']:
                continue
            path = self.output / record['key'] / filename
            try:
                _ordinary_directory(path.parent)
                if path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
                    raise ValueError('partial capture path changed ownership')
                size = path.stat().st_size
                if not path.is_file() or not 0 <= size <= record[kind + '_bytes']:
                    raise ValueError('partial capture size exceeds the reserved artifact')
                record[kind + '_bytes_written'] = size
            except (OSError, ValueError):
                record[kind + '_bytes_written'] = None

    @staticmethod
    def _write_file(path, raw, record, kind):
        with path.open('xb') as stream:
            record[kind + '_created'] = True
            if stream.write(raw) != len(raw):
                raise OSError('short write in a newly created capture artifact')
        record[kind + '_bytes_written'] = len(raw)

    def write_case(self, key: str, metadata: dict, ram: bytes) -> dict:
        """Write caller-observed inputs once; return a finite budget stop."""
        return self._write_payload(key, metadata, ram, formats=RAM_CAPTURE_FORMATS,
            descriptor=RAM_FIELD, filename='input.ram', kind='ram')

    def write_vdp_state(self, key: str, metadata: dict, ram: bytes, *,
            vdp_metadata: dict, vdp_payload: bytes) -> dict:
        """Retain observed pre-CALL RAM and complete command/memory in one slot.

        The codec, not this storage layer, qualifies device values. This writer
        accepts only its explicit fixed format and never invents device state.
        """
        if (type(vdp_metadata) is not dict or vdp_metadata.get('format') != VDP_STATE_FORMAT
                or vdp_metadata.get('scope') != 'vdp_command_memory_effects_only'
                or vdp_metadata.get('external_timing_FIFO_IRQ_included') is not False
                or type(vdp_payload) is not bytes or len(vdp_payload) != VDP_PAYLOAD_BYTES):
            raise ValueError('explicit complete immutable VDP command/memory codec payload required')
        return self._write_payload(key, metadata, ram,
            formats=(M68K_PRE_CALL_CAPTURE_FORMAT,), descriptor=RAM_FIELD,
            filename='input.ram', kind='ram', vdp=(vdp_metadata, vdp_payload))

    def write_readonly_source(self, metadata: dict, data: bytes) -> dict:
        """Write at most one shared source artifact, not an entry/RAM witness.

        It consumes one of this same store's case slots and the same JSON,
        total-byte, final-receipt and disk-reserve budgets. No extra allowance,
        filename choice, source loader, overwrite or post-failure retry exists.
        """
        return self._write_payload('readonly_data', metadata, data,
            formats=(READONLY_DATA_CAPTURE_FORMAT,), descriptor='captured_DATA',
            filename='source.data', kind='DATA')

    def _write_payload(self, key, metadata, payload, *, formats, descriptor, filename, kind, vdp=None):
        """One existing budget/write/failure lifecycle for both fixed payloads."""
        self._require_writable()
        if self._budget_stop is not None:
            return self._budget_exhausted(self._budget_stop)
        if len(self._records) >= self.max_cases:
            return self._budget_exhausted('max_cases')
        key = _safe_key(key)
        if key.casefold() in self._keys:
            raise ValueError('a capture key cannot be reused, including case aliases')
        if (type(metadata) is not dict or type(metadata.get('format')) is not str
                or metadata['format'] not in formats or descriptor in metadata
                or VDP_FIELD in metadata
                or (kind == 'DATA' and RAM_FIELD in metadata)
                or any(type(name) is not str for name in metadata)):
            if kind == 'ram':
                raise ValueError('explicit new M68K/Z80 capture metadata without captured_ram required')
            raise ValueError('explicit readonly DATA source metadata without captured_DATA/captured_ram required')
        if type(payload) is not bytes or not payload:
            if kind == 'ram':
                raise ValueError('explicit nonempty immutable observed RAM bytes required')
            raise ValueError('explicit nonempty immutable readonly source bytes required')
        document = dict(metadata)
        document[descriptor] = dict(path=filename, bytes=len(payload))
        if vdp is not None:
            vdp_metadata, vdp_payload = vdp
            document[VDP_FIELD] = dict(format=VDP_STATE_FORMAT, file='vdp.data',
                bytes=VDP_PAYLOAD_BYTES, state=vdp_metadata)
        try:
            raw = _json_bytes(document, self.max_case_json_bytes)
        except _JsonBudgetExceeded:
            return self._budget_exhausted('max_case_json_bytes')
        record = dict(key=key, format=metadata['format'], status='written', input_json=key + '/input.json')
        record.update({'input_' + kind: key + '/' + filename,
            'json_bytes': len(raw), kind + '_bytes': len(payload),
            'json_created': False, kind + '_created': False,
            'json_bytes_written': len(raw), kind + '_bytes_written': len(payload)})
        if kind == 'DATA':
            record.update(payload_filename='source.data',
                payload_role='shared_readonly_source_not_entry_or_RAM_evidence')
        if vdp is not None:
            record.update(input_VDP=key + '/vdp.data', VDP_bytes=VDP_PAYLOAD_BYTES,
                VDP_created=False, VDP_bytes_written=VDP_PAYLOAD_BYTES)
        reserve = self._reserve_receipt(self._records + [record])
        payload_bytes = len(raw) + len(payload) + (0 if vdp is None else VDP_PAYLOAD_BYTES)
        if self._charged_payload_bytes + payload_bytes + reserve > self.max_total_bytes:
            return self._budget_exhausted('max_total_bytes')
        try:
            _ordinary_directory(self.output)
            free_bytes = shutil.disk_usage(self.output).free
        except (OSError, ValueError) as error:
            self._failure = self._failure_record(error, 'check_case_disk_reserve', key)
            raise EntryCaptureWriteError(self.output, self._failure) from error
        if free_bytes < self.min_free_bytes + payload_bytes + reserve:
            return self._budget_exhausted('min_free_bytes')
        self._receipt_reserve = reserve
        self._charged_payload_bytes += payload_bytes
        self._keys.add(key.casefold())
        record.update({'status': 'partial', 'json_bytes_written': 0, kind + '_bytes_written': 0})
        if vdp is not None:
            record['VDP_bytes_written'] = 0
        self._records.append(record)
        stage = 'create_case_directory'
        try:
            _ordinary_directory(self.output)
            directory = fresh_output(self.output / key)
            directory.mkdir(exist_ok=False)
            stage = 'write_input_json'
            self._write_file(directory / 'input.json', raw, record, 'json')
            stage = 'write_input_ram' if kind == 'ram' else 'write_source_DATA'
            self._write_file(directory / filename, payload, record, kind)
            if vdp is not None:
                stage = 'write_vdp_state'
                self._write_file(directory / 'vdp.data', vdp_payload, record, 'VDP')
            record['status'] = 'written'
        except (OSError, ValueError) as error:
            self._observe_partial(record)
            self._failure = self._failure_record(error, stage, key)
            raise EntryCaptureWriteError(self.output, self._failure) from error
        return dict(status='written', **{name: value for name, value in record.items() if name != 'status'},
            charged_payload_bytes=self._charged_payload_bytes, strict_credit=0)

    def close(self, outcome: str) -> Path:
        """Write one reserved receipt; an I/O failure is retained, not retried."""
        if type(outcome) is not str or not 1 <= len(outcome) <= MAX_OUTCOME:
            raise ValueError('an explicit bounded collection outcome string required')
        receipt = self.output / RECEIPT_NAME
        if self._closed:
            if outcome != self._closed_outcome:
                raise ValueError('a closed capture outcome cannot be rewritten')
            return receipt
        if self._close_attempted:
            raise EntryCaptureWriteError(self.output, self._failure)
        self._close_attempted = True
        try:
            document = self._receipt_document(outcome, self._records, failure=self._failure,
                budget_stop=self._budget_stop, reserve=self._receipt_reserve)
            raw = _json_bytes(document, self._receipt_reserve)
            if self._charged_payload_bytes + len(raw) > self.max_total_bytes:
                raise ValueError('reserved final capture receipt exceeds the explicit total budget')
            _ordinary_directory(self.output)
            if shutil.disk_usage(self.output).free < self.min_free_bytes + len(raw):
                raise OSError('free bytes fell below the explicit final-receipt reserve')
            with receipt.open('xb') as stream:
                if stream.write(raw) != len(raw):
                    raise OSError('short write in the final capture receipt')
        except (OSError, ValueError) as error:
            failure = self._failure_record(error, 'write_final_receipt', '')
            if self._failure is not None:
                failure['prior_write_failure'] = dict(self._failure)
            self._failure = failure
            raise EntryCaptureWriteError(self.output, self._failure) from error
        self._closed = True
        self._closed_outcome = outcome
        return receipt
