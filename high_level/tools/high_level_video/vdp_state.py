"""Lossless immutable state for the existing VDP command/memory-effects owner.

Confirmed scope: four complete backings and every VdpController/DmaTransfer
state field declared in hardware_vdp.py. This is not external raster timing,
FIFO/open-bus, IRQ, CPU-hold or complete-console state. Saving this record does
not qualify a natural capture or a device-aware behavioral case by itself.

Import performs no I/O or execution. Snapshot reads exact live storage only;
restore builds new backings with explicitly supplied external owners. Neither
operation reads a port, advances DMA, supplies an ACK or invents ready state.
"""
from __future__ import annotations

from dataclasses import dataclass

from .hardware_vdp import (
    DmaTransfer, SceneDataDmaSource, SceneRamDmaSource, VdpController,
    VdpMemory, VdpStatusSource,
)


FORMAT = 'g5510-vdp-command-memory-state-v1'
SCOPE = 'vdp_command_memory_effects_only'
BACKING_LAYOUT = (('vram', 0, 65536), ('cram', 65536, 128),
    ('vsram', 65664, 80), ('registers', 65744, 32))
PAYLOAD_BYTES = 65776
_DMA_FIELDS = ('kind', 'remaining', 'source_counter', 'source_bank',
    'destination_code', 'increment', 'fill_byte')
_CONTROL_FIELDS = ('address', 'address_high_latch', 'code', 'command_pending',
    'fill_armed', 'pending_dma', 'hv_latch')
_STATE_FIELDS = ('vram', 'cram', 'vsram', 'registers', *_CONTROL_FIELDS)
_LIVE_CONTROL_FIELDS = ('memory', 'status', 'dma_source', *_CONTROL_FIELDS)


class VdpStateError(ValueError):
    """An incomplete, unknown or inconsistent state is not silently repaired."""


def _require(condition, message):
    if not condition:
        raise VdpStateError(message)


def _uint(value, maximum, name):
    _require(type(value) is int and 0 <= value <= maximum,
        name + ': exact unsigned integer required, never bool')


def _mapping(value, fields, name):
    _require(type(value) is dict and all(type(key) is str for key in value)
        and set(value) == set(fields), name + ': complete exact fields required')
    return value


def _storage(value, fields, name):
    """Copy only known instance storage, without invoking live properties."""
    values = vars(value)
    _mapping(values, fields, name)
    return dict(values)


@dataclass(frozen=True)
class DmaState:
    """All transfer fields, including an explicit None for non-fill transfers."""

    kind: str
    remaining: int
    source_counter: int
    source_bank: int
    destination_code: int
    increment: int
    fill_byte: int | None

    def __post_init__(self):
        _dma_values(self)


@dataclass(frozen=True)
class VdpState:
    """Caller-owned immutable bytes and complete saved controller state."""

    vram: bytes
    cram: bytes
    vsram: bytes
    registers: bytes
    address: int
    address_high_latch: int
    code: int
    command_pending: bool
    fill_armed: bool
    pending_dma: DmaState | None
    hv_latch: int | None

    def __post_init__(self):
        _state_values(self)


def _dma_values(transfer):
    _require(type(transfer) is DmaState, 'exact immutable DmaState required')
    values = _storage(transfer, _DMA_FIELDS, 'DMA state')
    _require(type(values['kind']) is str and values['kind'] in ('ram', 'copy', 'fill'),
        'DMA kind must be the existing ram/copy/fill operation')
    for name, maximum in (('remaining', 65536), ('source_counter', 65535),
            ('source_bank', 0xFE0000), ('destination_code', 15), ('increment', 255)):
        _uint(values[name], maximum, 'DMA ' + name)
    _require(values['remaining'] > 0 and values['source_bank'] & 0x1FFFF == 0,
        'a pending DMA needs positive remaining units and its full aligned source bank')
    if values['kind'] == 'fill':
        _uint(values['fill_byte'], 255, 'DMA fill_byte')
    else:
        _require(values['fill_byte'] is None, 'non-fill DMA must preserve an explicit None fill byte')
    return values


def _backing_bytes(values):
    for name, _, size in BACKING_LAYOUT:
        _require(type(values[name]) is bytes and len(values[name]) == size,
            name + ': complete immutable backing required')
    for name, mask in (('cram', 0x0EEE), ('vsram', 0x07FF)):
        data = values[name]
        _require(all(int.from_bytes(data[index:index + 2], 'big') & ~mask == 0
            for index in range(0, len(data), 2)), name + ': unsupported reserved bits are not normalized')


def _dma_consistency(values):
    transfer = values['pending_dma']
    if transfer is None and not values['fill_armed']:
        return
    registers, code = values['registers'], values['code']
    _require(not values['command_pending'] and bool(code & 0x20)
        and bool(registers[1] & 0x10), 'active/armed DMA contradicts command or DMA-enable state')
    mode = registers[23] >> 6
    if values['fill_armed']:
        _require(transfer is None and mode == 2 and code & 15 == 1,
            'armed fill must await its data word, not coexist with a pending transfer')
        return
    dma = _dma_values(transfer)
    _require(dma['destination_code'] == code & 15 and dma['increment'] == registers[15]
        and dma['source_bank'] == (registers[23] & 0x7F) << 17
        and dma['source_counter'] == registers[21] | (registers[22] << 8)
        and dma['remaining'] & 65535 == registers[19] | (registers[20] << 8),
        'pending DMA and its live length/source/increment/command registers differ')
    if dma['kind'] == 'ram':
        _require(mode in (0, 1) and dma['destination_code'] in (1, 3, 5),
            'RAM DMA needs its existing supported mode and destination command')
    elif dma['kind'] == 'copy':
        _require(mode == 3 and bool(code & 0x10), 'copy DMA requires its original CD4/mode bits')
    else:
        _require(mode == 2 and dma['destination_code'] == 1, 'fill DMA requires the VRAM fill mode')


def _state_values(state):
    _require(type(state) is VdpState, 'exact immutable VdpState required')
    values = _storage(state, _STATE_FIELDS, 'VDP state')
    _backing_bytes(values)
    _uint(values['address'], 65535, 'VDP address')
    _uint(values['address_high_latch'], 0xC000, 'VDP address_high_latch')
    _require(values['address_high_latch'] & 0x3FFF == 0, 'VDP high latch must retain exactly two address bits')
    _uint(values['code'], 63, 'VDP code')
    for name in ('command_pending', 'fill_armed'):
        _require(type(values[name]) is bool, name + ': exact bool required')
    if values['hv_latch'] is not None:
        _uint(values['hv_latch'], 65535, 'VDP hv_latch')
    if values['pending_dma'] is not None:
        _dma_values(values['pending_dma'])
    _require(not (values['fill_armed'] and values['pending_dma'] is not None),
        'an armed fill and an active DMA cannot coexist')
    # Address increments can cross 14-bit boundaries without updating the
    # command high latch; equality is intentionally not imposed on idle/DMA.
    if values['command_pending'] or values['fill_armed']:
        _require(values['address'] & 0xC000 == values['address_high_latch'],
            'an unconsumed command/fill must retain its actual high-address latch')
    _dma_consistency(values)
    return values


def _suppliers(status, dma_source):
    _require(status is None or isinstance(status, VdpStatusSource),
        'explicit VdpStatusSource or explicit unsupplied None required')
    _require(dma_source is None or type(dma_source) in (SceneRamDmaSource, SceneDataDmaSource),
        'explicit existing Scene DMA source or explicit unsupplied None required')


def snapshot_vdp_state(controller):
    """Copy exact live storage only; same-owner/thread proof belongs to caller.

    No supplier method is called. The snapshot does not establish that the
    external status/DMA supplier, FIFO, scheduler or bus CPU hold was captured.
    """
    _require(type(controller) is VdpController, 'exact live VdpController required')
    live = _storage(controller, _LIVE_CONTROL_FIELDS, 'live VDP controller')
    _suppliers(live['status'], live['dma_source'])
    _require(type(live['memory']) is VdpMemory, 'exact live VdpMemory required')
    backings = _storage(live['memory'], tuple(name for name, _, _ in BACKING_LAYOUT), 'live VDP memory')
    for name, _, size in BACKING_LAYOUT:
        _require(type(backings[name]) is bytearray and len(backings[name]) == size,
            name + ': actual complete live bytearray required')
    dma = live['pending_dma']
    if dma is not None:
        _require(type(dma) is DmaTransfer, 'exact live DmaTransfer or actual None required')
        dma = DmaState(**_storage(dma, _DMA_FIELDS, 'live DMA transfer'))
    return VdpState(*(bytes(backings[name]) for name, _, _ in BACKING_LAYOUT),
        live['address'], live['address_high_latch'], live['code'], live['command_pending'],
        live['fill_armed'], dma, live['hv_latch'])


def _controller_metadata(values):
    result = {name: values[name] for name in _CONTROL_FIELDS}
    result['pending_dma'] = None if values['pending_dma'] is None else _dma_values(values['pending_dma'])
    return result


def encode_vdp_state(state):
    """Return structural JSON-ready metadata and all 65,776 backing bytes.

    This function serializes no JSON and writes no file. The capture store
    separately owns fresh paths, budgets, metadata/payload publication and
    same-App provenance. No backing is omitted because it appears unchanged.
    """
    values = _state_values(state)
    metadata = dict(format=FORMAT, scope=SCOPE, external_timing_FIFO_IRQ_included=False,
        payload_bytes=PAYLOAD_BYTES,
        backings={name: dict(offset=offset, size=size) for name, offset, size in BACKING_LAYOUT},
        controller=_controller_metadata(values))
    return metadata, b''.join(values[name] for name, _, _ in BACKING_LAYOUT)


def _metadata_backings(metadata):
    _mapping(metadata, ('format', 'scope', 'external_timing_FIFO_IRQ_included',
        'payload_bytes', 'backings', 'controller'), 'VDP metadata')
    _require(type(metadata['format']) is str and metadata['format'] == FORMAT
        and type(metadata['scope']) is str and metadata['scope'] == SCOPE
        and metadata['external_timing_FIFO_IRQ_included'] is False
        and type(metadata['payload_bytes']) is int and metadata['payload_bytes'] == PAYLOAD_BYTES,
        'the exact VDP command/memory schema and complete payload size are required')
    rows = _mapping(metadata['backings'], tuple(name for name, _, _ in BACKING_LAYOUT), 'VDP backing geometry')
    for name, offset, size in BACKING_LAYOUT:
        row = _mapping(rows[name], ('offset', 'size'), name + ' geometry')
        _require(type(row['offset']) is type(row['size']) is int
            and (row['offset'], row['size']) == (offset, size), 'complete fixed backing layout required: ' + name)


def decode_vdp_state(metadata, payload):
    """Reject unknown/missing fields and reconstruct the immutable full state."""
    _metadata_backings(metadata)
    _require(type(payload) is bytes and len(payload) == PAYLOAD_BYTES,
        'one complete immutable VDP payload required; no truncation or trailing bytes')
    control = dict(_mapping(metadata['controller'], _CONTROL_FIELDS, 'VDP controller metadata'))
    if control['pending_dma'] is not None:
        control['pending_dma'] = DmaState(**_mapping(control['pending_dma'], _DMA_FIELDS, 'DMA metadata'))
    return VdpState(*(payload[offset:offset + size] for _, offset, size in BACKING_LAYOUT),
        **control)


def restore_vdp_state(state, *, status, dma_source):
    """Build a new owner, retaining active DMA without granting any progress.

    Both external supplier keywords are mandatory. Explicit None preserves
    an unsupplied boundary, never an always-ready device. The composing caller
    must bind actual suppliers and bus owners to the same intended Scene;
    their external state and CPU hold are not reconstructed by this codec.
    """
    values = _state_values(state)
    _suppliers(status, dma_source)
    memory = VdpMemory(*(bytearray(values[name]) for name, _, _ in BACKING_LAYOUT))
    controller = VdpController(memory, status=status, dma_source=dma_source)
    restored = {name: values[name] for name in _CONTROL_FIELDS}
    if values['pending_dma'] is not None:
        restored['pending_dma'] = DmaTransfer(**_dma_values(values['pending_dma']))
    # Constructor-only values are overwritten in full before the owner is
    # exposed. This is restoration, not a control-port write or DMA restart.
    vars(controller).update(restored)
    return controller
