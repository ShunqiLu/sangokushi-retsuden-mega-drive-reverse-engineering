"""ROM-independent typed field serialization for small, related resources.

The frozen contract is a data-format schema: fixed metadata, editable leaf
types, explicit field order/bit packing and disjoint physical allocations.
It is not an instruction program or a cached binary. Every emitted value is
read from the supplied own typed source; unknown gaps are never materialized.

Confirmed: full WORD/LONG values, packed sprite bits, 4bpp pixels and reserved
palette bits have separate, lossless representations. Candidate/unknown:
conditional source aliases and original business meanings retain their input
classifications; fixed editor shapes are not natural CPU-domain clamps.
"""
from __future__ import annotations

from .resource_adapters_records import _block, _finish, _metadata_text, _same


def _get(fields, path):
    value = fields
    for key in path:
        value = value[key]
    return value


def _validate(value, schema, path=()):
    kind = schema['kind']
    if kind == 'fixed':
        _same(value, schema['value'], str(path))
    elif kind == 'metadata_text':
        _metadata_text(value, schema['shape'], str(path), suffix=schema.get('suffix'))
    elif kind == 'object':
        if type(value) is not dict or set(value) != set(schema['fields']):
            raise ValueError(f'{path}: fixed typed object keys differ')
        for key, inner in schema['fields'].items():
            _validate(value[key], inner, path + (key,))
    elif kind == 'array':
        if type(value) is not list or len(value) != len(schema['items']):
            raise ValueError(f'{path}: fixed physical list count differs')
        for index, inner in enumerate(schema['items']):
            _validate(value[index], inner, path + (index,))
    elif kind == 'integer':
        if type(value) is not int or not schema['minimum'] <= value <= schema['maximum']:
            raise ValueError(f'{path}: strict original field width differs')
        if 'mask' in schema and value & ~schema['mask']:
            raise ValueError(f'{path}: reserved bits overlap named channels')
    elif kind == 'boolean':
        if type(value) is not bool:
            raise ValueError(f'{path}: actual boolean field required')
    elif kind == 'choice':
        if type(value) is not str or value not in schema['values']:
            raise ValueError(f'{path}: unknown physical reference or derived kind')
    else:
        raise ValueError('unknown independent field schema kind')


def _value(fields, element):
    if 'parts' in element:
        result = 0
        for part in element['parts']:
            value = _get(fields, part['path'])
            if type(value) is bool:
                value = int(value)
            value -= part.get('subtract', 0)
            if 'mask' in part:
                value &= part['mask']
            result |= value << part.get('shift', 0)
        return result
    value = _get(fields, element['path'])
    if 'catalog' in element:
        if type(value) is not str or value not in element['catalog']:
            raise ValueError('reference must name an existing physical source')
        return element['catalog'][value]
    return value


def _guards(fields, guards):
    for guard in guards:
        kind = guard['kind']
        if kind == 'not_value':
            if _get(fields, guard['path']) == guard['value']:
                raise ValueError('body field would become an early source terminator')
        elif kind == 'not_pair':
            if [_get(fields, path) for path in guard['paths']] == guard['values']:
                raise ValueError('coordinate pair would become an early FFFF terminator')
        elif kind == 'status_font':
            word = _get(fields, guard['word_path'])
            expected = 'procedural_cell' if word & 0x8000 else 'font16_bitmap'
            if not word & 0x8000:
                offset = (((word & 0xFF00) << 3) & 0xFFFF) | (((word & 255) << 5) & 0xFFFF)
                if offset + 32 > 1034 * 32:
                    raise ValueError('positive counted font WORD escapes physical font allocation')
            if _get(fields, guard['kind_path']) != expected:
                raise ValueError('font sign-branch kind does not match the full WORD')
        else:
            raise ValueError('unknown original source framing guard')


def encode_fields(fields, contract):
    """Serialize a complete own field package into explicitly owned blocks.

    Field order and bit allocations are frozen format geometry, not hidden
    payload values. Framing controls are pinned in the supplied source schema
    and still consumed from source. Neither bytes equality nor an alias view
    permits duplicate physical output.
    """
    if type(contract) is not dict or contract.get('adapter') != 'encode_fields':
        raise ValueError('wrong pure field-format contract')
    if contract.get('adapter_module') != 'tools.high_level_rom.resource_adapters_fields':
        raise ValueError('wrong independent field serializer module')
    _validate(fields, contract['schema'])
    _guards(fields, contract['guards'])
    rows = []
    for allocation in contract['allocations']:
        raw = bytearray()
        for element in allocation['elements']:
            value = _value(fields, element)
            width = element['width']
            if type(value) is not int or width not in (1, 2, 4):
                raise ValueError('typed original integer and BYTE/WORD/LONG width required')
            if element.get('signed'):
                if not -(1 << (width * 8 - 1)) <= value < 1 << (width * 8 - 1):
                    raise ValueError('signed original field outside encoded width')
                raw.extend(value.to_bytes(width, 'big', signed=True))
            else:
                if not 0 <= value < 1 << (width * 8):
                    raise ValueError('complete source bits outside encoded width')
                raw.extend(value.to_bytes(width, 'big'))
        if len(raw) != allocation['end'] - allocation['start']:
            raise ValueError('explicit fixed physical allocation cost differs')
        rows.append(_block(allocation['start'], bytes(raw), allocation['id'], allocation['role']))
    return _finish(rows, contract)
