"""Pure editable CE00 transport-order views over the existing save codec.

All values are saved codes, not complete runtime BYTEs or a synthesized RAM
image. The original 40-record bitstream is owned by save_format. This adapter
reads no file, ROM or device, supplies no default order, and changes no game rule.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from . import save_format


FORMAT = 'g5510-campaign-orders-v1'
EDIT_FORMAT = 'g5510-campaign-order-edits-v1'
# Validation widths are the saved low bits from 88C6/8FB4, not RAM limits.
# Consumers: 16ACC/16748 route coordinates; 168C8..16916 kind/arrival credit.
FIELD_SPECS = {
    'transport_kind_code': ('ram_ce00_field0_u2', 2),
    'route_x': ('ram_ce00_field1_u7', 7),
    'route_y': ('ram_ce00_field2_u7', 7),
    'destination_city_code': ('ram_ce00_field3_u6', 6),
}


class CampaignOrderError(save_format.SaveFormatError):
    """An explicit saved transport-order view or edit violates its contract."""


def _keys(value: Any, expected: Any, context: str) -> None:
    if type(value) is not dict or set(value) != set(expected):
        raise CampaignOrderError(context + ': exact object fields required')


def _uint(value: Any, width: int, context: str) -> int:
    if type(value) is not int or not 0 <= value < (1 << width):
        raise CampaignOrderError(context + f': unsigned {width}-bit integer required')
    return value


def _same(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(_same(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    return left == right


def _decode(logical: bytes) -> list[dict]:
    if type(logical) is not bytes:
        raise CampaignOrderError('an explicit immutable logical save is required')
    save_format.validate_logical(logical)
    start = save_format.CE00_OFFSET
    return save_format.unpack_ce00(logical[start:start + save_format.CE00_LENGTH])


def _storage(records: list) -> dict:
    return {
        'stream': 'ce00_transport_orders',
        'logical_offset': save_format.CE00_OFFSET,
        'encoded_length': save_format.CE00_LENGTH,
        'record_count': len(records),
        'stored_field_widths': {name: width for name, (_, width) in FIELD_SPECS.items()},
    }


def from_logical(logical: bytes) -> dict:
    """Expose every CE00 record from one explicitly supplied valid 8 KiB save."""
    records = _decode(logical)
    return {
        'format': FORMAT,
        'source': {'logical_hex': logical.hex()},
        'storage': _storage(records),
        'orders': [
            {'record_index': index,
             **{name: record[source] for name, (source, _) in FIELD_SPECS.items()}}
            for index, record in enumerate(records)
        ],
    }


def _baseline(named: dict) -> tuple[bytes, list]:
    _keys(named, ('format', 'source', 'storage', 'orders'), 'order document')
    if type(named['format']) is not str or named['format'] != FORMAT:
        raise CampaignOrderError('explicit campaign order format required')
    _keys(named['source'], ('logical_hex',), 'order source')
    text = named['source']['logical_hex']
    if (type(text) is not str or len(text) != save_format.LOGICAL_SIZE * 2
            or any(character not in '0123456789abcdef' for character in text)):
        raise CampaignOrderError('order source: exact canonical logical-image hex required')
    logical = bytes.fromhex(text)
    records = _decode(logical)
    if not _same(named['storage'], _storage(records)):
        raise CampaignOrderError('CE00 placement or original record geometry changed')
    return logical, records


def _records(named: dict) -> tuple[bytes, list]:
    logical, original = _baseline(named)
    orders = named['orders']
    if type(orders) is not list or len(orders) != len(original):
        raise CampaignOrderError('preserve every original CE00 record and its order')
    records = []
    for index, order in enumerate(orders):
        _keys(order, ('record_index', *FIELD_SPECS), 'order')
        if type(order['record_index']) is not int or order['record_index'] != index:
            raise CampaignOrderError('CE00 storage record order changed')
        records.append({
            'record_index': index,
            **{source: _uint(order[name], width, name)
               for name, (source, width) in FIELD_SPECS.items()},
        })
    return logical, records


def to_records(named: dict) -> list[dict]:
    """Recover the sole codec's complete records, including inactive-slot values."""
    return _records(named)[1]


def with_edits(named: dict, edits: list[dict]) -> dict:
    """Validate the whole explicit old-value batch before copying or changing it.

    Each edit has order_index/field/expected_value/value. Only the four stored
    codes are editable; no ownership, route, amount or runtime flag is derived.
    """
    _, records = _records(named)
    if type(edits) is not list:
        raise CampaignOrderError('an explicit order edit list is required')
    prepared, seen = [], set()
    for edit in edits:
        _keys(edit, ('order_index', 'field', 'expected_value', 'value'), 'order edit')
        index, field = edit['order_index'], edit['field']
        if type(index) is not int or not 0 <= index < len(records):
            raise CampaignOrderError('order edit: storage record index out of range')
        if type(field) is not str or field not in FIELD_SPECS:
            raise CampaignOrderError('order edit: a known stored field is required')
        target = (index, field)
        if target in seen:
            raise CampaignOrderError('order edit: duplicate target in one batch')
        seen.add(target)
        width = FIELD_SPECS[field][1]
        expected = _uint(edit['expected_value'], width, 'order edit.expected_value')
        value = _uint(edit['value'], width, 'order edit.value')
        if named['orders'][index][field] != expected:
            raise CampaignOrderError(f'order edit: original value differs at {target!r}')
        prepared.append((index, field, value))
    result = deepcopy(named)
    for index, field, value in prepared:
        result['orders'][index][field] = value
    return result


def to_logical(named: dict, original_logical: bytes) -> bytes:
    """Replace only CE00 and the existing checksum in the exact original image.

    Fixed segments, metadata, marching groups and all unused bytes are retained.
    The return value is new bytes; this function writes no file or live medium.
    """
    baseline, records = _records(named)
    if type(original_logical) is not bytes or original_logical != baseline:
        raise CampaignOrderError('explicit logical baseline differs from the source save')
    encoded = save_format.pack_ce00(records)
    if len(encoded) != save_format.CE00_LENGTH:
        raise CampaignOrderError('CE00 encoded length changed')
    result = bytearray(original_logical)
    start = save_format.CE00_OFFSET
    result[start:start + save_format.CE00_LENGTH] = encoded
    save_format.write_checksum(result)
    output = bytes(result)
    save_format.validate_logical(output)
    return output
