"""Encode separately owned SMD container metadata, never cartridge payload.

The original 16 leading bytes and 496 equal trailing metadata bytes have been
observed directly. Neutral fields avoid guessing flag meanings. The complete
512-byte original copier header remains unchanged; it is not ROM free space.
"""
from __future__ import annotations

import json
from pathlib import Path

from .resource_adapters import fixed_list, uint


DEFAULT_FIELDS = Path(__file__).with_name('resource_sources') / 'copier_header.json'


def encode(fields: dict) -> bytes:
    """Encode the complete explicit 512-byte metadata field representation."""
    if type(fields) is not dict or fields.get('format') != 'g5510-owned-SMD-copier-metadata-v1':
        raise ValueError('explicit owned SMD metadata format required')
    if type(fields.get('header_size_BYTES')) is not int or fields['header_size_BYTES'] != 512:
        raise ValueError('SMD container requires exactly512 copier-header bytes')
    leading = bytes(uint(value, 255, 'copier metadata BYTE')
                    for value in fixed_list(fields['leading_metadata_BYTEs'], 16, 'leading copier metadata'))
    tail = fields['preserved_tail']
    if type(tail) is not dict or set(tail) != {'count_BYTES', 'value_BYTE'}:
        raise ValueError('explicit equal-BYTE copier metadata tail required')
    if type(tail['count_BYTES']) is not int or tail['count_BYTES'] != 496:
        raise ValueError('complete496-byte trailing copier metadata required')
    return leading + bytes((uint(tail['value_BYTE'], 255, 'copier metadata tail BYTE'),)) * 496


def load(path: Path = DEFAULT_FIELDS) -> bytes:
    """Read this project's own JSON metadata only, not an external SMD file."""
    return encode(json.loads(path.read_text(encoding='utf-8')))
