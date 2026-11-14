"""Editable campaign marching groups over the sole existing save-stream codec.

The view contains saved coordinates, force code, resource codes and officer
rosters, not an invented RAM image. Packet/member geometry stays bound to the
explicit original save; no file, ROM, App or emulated device is accessed here.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from . import save_format


FORMAT = 'g5510-campaign-packets-v2'
EDIT_FORMAT = 'g5510-campaign-packet-edits-v2'
LEGACY_FORMAT = 'g5510-campaign-packets-v1'
LEGACY_EDIT_FORMAT = 'g5510-campaign-packet-edits-v1'
# Widths describe saved codes in the original 8946/9036 stream, not RAM caps.
_RESOURCE_FIELDS = {
    'force_index_code': ('field_4', 4),
    'gold_saved_code': ('value_18', 18),
    'rice_saved_code': ('value_20', 20),
}
FIELD_SPECS = {'map_x': ('field_7b', 7), 'map_y': ('field_7a', 7), **_RESOURCE_FIELDS}
_LEGACY_FIELD_SPECS = {
    'map_x': ('field_7a', 7),
    'map_y': ('field_7b', 7),
    **_RESOURCE_FIELDS,
}
_SCHEMAS = {FORMAT: (FIELD_SPECS, EDIT_FORMAT), LEGACY_FORMAT: (_LEGACY_FIELD_SPECS, LEGACY_EDIT_FORMAT)}


class CampaignPacketError(save_format.SaveFormatError):
    """An explicit saved packet view or batch edit violates its source contract."""


def _keys(value: Any, expected: Any, context: str) -> None:
    if type(value) is not dict or set(value) != set(expected):
        raise CampaignPacketError(context + ': exact object fields required')


def _uint(value: Any, width: int, context: str) -> int:
    if type(value) is not int or not 0 <= value < (1 << width):
        raise CampaignPacketError(context + f': unsigned {width}-bit integer required')
    return value


def _same(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(_same(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    return left == right


def _decode(logical: bytes) -> tuple[list, int, int]:
    if type(logical) is not bytes:
        raise CampaignPacketError('an explicit immutable logical save is required')
    save_format.validate_logical(logical)
    return save_format.unpack_variable_records(
        logical[save_format.VARIABLE_OFFSET:save_format.CHECKSUM_REGION_END])


def _storage(records: list, length: int, bits: int) -> dict:
    return {
        'stream': 'ram9000_variable',
        'logical_offset': save_format.VARIABLE_OFFSET,
        'original_encoded_length': length,
        'original_meaningful_bits': bits,
        'original_member_counts': [record['count_u4'] for record in records],
    }


def from_logical(logical: bytes) -> dict:
    """Expose every saved marching group from one explicit valid 8 KiB save."""
    records, length, bits = _decode(logical)
    packets = []
    for index, record in enumerate(records):
        packets.append({
            'record_index': index,
            **{name: record[source] for name, (source, _) in FIELD_SPECS.items()},
            'officer_ids': list(record['items_u8']),
        })
    return {
        'format': FORMAT,
        'source': {'logical_hex': logical.hex()},
        'storage': _storage(records, length, bits),
        'packets': packets,
    }


def _schema(named):
    label = named.get('format') if type(named) is dict else None
    if type(label) is not str or label not in _SCHEMAS:
        raise CampaignPacketError('explicit campaign packet format required')
    return _SCHEMAS[label]


def edit_format_for(named):
    """A batch must use the axis convention of its own saved view."""
    return _schema(named)[1]


def _baseline(named: dict) -> tuple[bytes, list, int]:
    _keys(named, ('format', 'source', 'storage', 'packets'), 'packet document')
    _keys(named['source'], ('logical_hex',), 'packet source')
    text = named['source']['logical_hex']
    if (type(text) is not str or len(text) != save_format.LOGICAL_SIZE * 2
            or any(character not in '0123456789abcdef' for character in text)):
        raise CampaignPacketError('packet source: exact canonical logical-image hex required')
    logical = bytes.fromhex(text)
    records, length, bits = _decode(logical)
    if not _same(named['storage'], _storage(records, length, bits)):
        raise CampaignPacketError('packet stream placement or original geometry changed')
    return logical, records, length


def _roster(value: Any, count: int) -> list[int]:
    if type(value) is not list or len(value) != count:
        raise CampaignPacketError('officer_ids: preserve the original member count')
    return [_uint(item, 8, 'officer id') for item in value]


def _records(named: dict) -> tuple[bytes, list, int]:
    field_specs, _ = _schema(named)
    logical, original, length = _baseline(named)
    packets = named['packets']
    if type(packets) is not list or len(packets) != len(original):
        raise CampaignPacketError('preserve every original packet and its order')
    result = []
    for index, (packet, prior) in enumerate(zip(packets, original)):
        _keys(packet, ('record_index', 'officer_ids', *field_specs), 'packet')
        if type(packet['record_index']) is not int or packet['record_index'] != index:
            raise CampaignPacketError('packet storage record order changed')
        officers = _roster(packet['officer_ids'], prior['count_u4'])
        # Count is derived from the one editable roster, never a second input.
        result.append({
            'record_index': index,
            'count_u4': len(officers),
            **{source: _uint(packet[name], width, name)
               for name, (source, width) in field_specs.items()},
            'items_u8': officers,
            'derived_runtime_byte_at_offset3': None,
            'runtime_record_length': 13 + len(officers),
        })
    return logical, result, length


def to_records(named: dict) -> list[dict]:
    """Recover the existing codec's records; no second bit-stream is produced."""
    return _records(named)[1]


def with_edits(named: dict, edits: list[dict]) -> dict:
    """Check all old values first, then edit an independent complete view.

    Each edit has packet_index/field/expected_value/value. Scalar fields use
    stored widths. The officer_ids field replaces a same-length ordered list;
    no membership, city ownership or other save state is implicitly repaired.
    """
    field_specs, _ = _schema(named)
    _, records, _ = _records(named)
    if type(edits) is not list:
        raise CampaignPacketError('an explicit edit list is required')
    prepared, seen = [], set()
    for edit in edits:
        _keys(edit, ('packet_index', 'field', 'expected_value', 'value'), 'packet edit')
        index, field = edit['packet_index'], edit['field']
        if type(index) is not int or not 0 <= index < len(records):
            raise CampaignPacketError('packet edit: storage record index out of range')
        if type(field) is not str or field not in (*field_specs, 'officer_ids'):
            raise CampaignPacketError('packet edit: a known editable field is required')
        target = (index, field)
        if target in seen:
            raise CampaignPacketError('packet edit: duplicate target in one batch')
        seen.add(target)
        if field == 'officer_ids':
            expected = _roster(edit['expected_value'], records[index]['count_u4'])
            value = _roster(edit['value'], records[index]['count_u4'])
        else:
            width = field_specs[field][1]
            expected = _uint(edit['expected_value'], width, 'packet edit.expected_value')
            value = _uint(edit['value'], width, 'packet edit.value')
        if not _same(named['packets'][index][field], expected):
            raise CampaignPacketError(f'packet edit: original value differs at {target!r}')
        prepared.append((index, field, value))
    result = deepcopy(named)
    for index, field, value in prepared:
        result['packets'][index][field] = value
    return result


def to_logical(named: dict, original_logical: bytes) -> bytes:
    """Overlay only the same-length packet stream and original checksum field.

    Fixed segments, metadata, CE00 orders and all unused bytes remain exact.
    Packet resizing is not implicit; the original raw importer supplies an
    explicit different workflow for that operation. This function writes no file.
    """
    baseline, records, original_length = _records(named)
    if type(original_logical) is not bytes or original_logical != baseline:
        raise CampaignPacketError('explicit logical baseline differs from the source save')
    encoded = save_format.pack_variable_records(records)
    if len(encoded) != original_length:
        raise CampaignPacketError('packet stream encoded length changed')
    result = bytearray(original_logical)
    start = save_format.VARIABLE_OFFSET
    result[start:start + original_length] = encoded
    save_format.write_checksum(result)
    output = bytes(result)
    save_format.validate_logical(output)
    return output
