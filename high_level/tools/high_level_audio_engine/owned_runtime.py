"""Owned material, explicit chip register effects, and finite recovered stages.

No driver opcode image is fetched/executed. Static tables remain editable DATA.
The register model does not synthesize PCM or claim cycle-exact YM2612 timing.
"""
from dataclasses import dataclass, fields, replace
from pathlib import Path

from tools.high_level_audio_engine.domain import (
    AudioBoundary, AudioPlatform, AlternateGroup, Continuation, byte, word,
)
from tools.high_level_audio_engine.hardware_scene import SoundDevice
from tools.high_level_audio_engine.fm_ports import FmPortDevice
from tools.high_level_scene_flows.domain import Boundary, ReadOnlyData
from tools.high_level_main_flows.runtime_resources import load_scene_resources


OWN_RESOURCE_IDS = ('audio_build', 'audio_root_resources', 'z80_startup_seed_fields',
                    'audio_dispatch_fields', 'audio_frequency_fields')


def driver_static_data(source):
    """Encode named fixed-shape driver fields, not a saved executable payload."""
    if type(source) is not dict or source.get('format') != 'g5510-audio-driver-static-fields-v1':
        raise ValueError('explicit editable driver DATA fields required')
    registers, defaults, mute = (source.get(key) for key in
        ('instrument_register_order', 'music_channel_defaults', 'psg_mute_commands'))
    if type(registers) is not list or len(registers) != 25:
        raise ValueError('25 original ordered register selectors required')
    if type(defaults) is not list or len(defaults) != 10:
        raise ValueError('ten original flags/channel pairs required')
    if type(mute) is not list or len(mute) != 4:
        raise ValueError('four original PSG mute commands required')
    pairs = bytearray()
    for row in defaults:
        if type(row) is not dict or set(row) != {'flags', 'channel_id'}:
            raise ValueError('named complete channel seed required')
        pairs.extend((byte(row['flags']), byte(row['channel_id'])))
    return ((0x04C8, bytes(byte(value) for value in registers)),
            (0x05E3, bytes(pairs)), (0x0862, bytes(byte(value) for value in mute)))


@dataclass(frozen=True)
class OwnedSoundMaterial:
    data: ReadOnlyData
    ram_segments: tuple
    resource_ids: tuple
    encoded_bytes: int


def project_copied_sound_data(data: ReadOnlyData) -> dict[int, int]:
    """Project only owned DATA through all three original ordered boot copies.

    The first 4096-byte source ends at79D2, not799C. Consequently the first54
    bytes of the second source also appear at the end of the first RAM copy.
    The final13-byte seed copy intentionally overrides its destination. These
    are real physical aliases and ordered writes, not competing source owners.
    Unpublished executable/data holes are never filled as a claimed image.
    """
    if type(data) is not ReadOnlyData:
        raise ValueError('one explicit nonoverlapping owned DATA authority required')
    ram = {}
    for first, end, destination in ((0x69D2, 0x79D2, 0),
                                    (0x799C, 0x879C, 0x1000),
                                    (0x69AA, 0x69B7, 0x1C00)):
        for base, payload in data.segments:
            for physical in range(max(first, base), min(end, base + len(payload))):
                ram[destination + physical - first] = payload[physical - base]
    return ram


def load_owned_sound_material(source_root: Path, driver_fields: dict):
    """Load complete selected own packages, then map only copied DATA to RAM.

    The original two source-copy regions have different physical→RAM mappings.
    No absent executable bytes are zero-filled as a claimed reconstructed image.
    Remaining RAM is the caller's explicit initial backing and writable workspace.
    """
    bundle = load_scene_resources(source_root, OWN_RESOURCE_IDS)
    ram = project_copied_sound_data(bundle.data)
    for base, payload in driver_static_data(driver_fields):
        for offset, value in enumerate(payload):
            if base + offset in ram:
                raise ValueError('static driver field competes with registered DATA')
            ram[base + offset] = value
    chunks = []
    for address in sorted(ram):
        if chunks and chunks[-1][0] + len(chunks[-1][1]) == address:
            chunks[-1][1].append(ram[address])
        else:
            chunks.append((address, bytearray((ram[address],))))
    return OwnedSoundMaterial(bundle.data, tuple((base, bytes(raw)) for base, raw in chunks),
                              bundle.resource_ids, bundle.encoded_bytes + 49)


def install_owned_sound_data(scene, sound, material):
    """Write explicit initial copied DATA through the actual granted Scene bus.

    This is a DATA-only preparation service, not a claim to have executed the
    complete original boot copy. It neither writes code nor edits active mailboxes
    after a game command has been queued; install before normal Scene enqueue.
    """
    if type(sound) is not SoundDevice or type(material) is not OwnedSoundMaterial:
        raise ValueError('actual sound owner and selected own material required')
    if sound.scene is not scene:
        raise ValueError('same bound Scene required')
    sound.require_m68k_owner()
    for base, raw in material.ram_segments:
        for offset, value in enumerate(raw):
            scene.write(0xA00000 + base + offset, 1, value)


class FmRegisterDevice(FmPortDevice):
    """Finite port/latch/register state, with explicit busy-duration authority.

    Every accepted data write sets a real busy deadline. Reading does not advance
    time by itself. The supplied after_status_read scheduler may explicitly move
    the clock; the default leaves BUSY asserted. Timer flags are separately supplied
    live state. Timing parameters are not claimed as a silicon-level model.
    """

    def __init__(self, registers, address_latches, *, tick, busy_until, busy_ticks,
                 timer_flags, after_status_read=None):
        if type(registers) is not bytearray or len(registers) != 512:
            raise ValueError('one live 512-byte FM register backing required')
        if type(address_latches) is not bytearray or len(address_latches) != 2:
            raise ValueError('two explicit FM address latches required')
        for value in (tick, busy_until, busy_ticks):
            if type(value) is not int or value < 0:
                raise ValueError('explicit nonnegative chip clock values required')
        if busy_ticks == 0 or type(timer_flags) is not int or not 0 <= timer_flags <= 3:
            raise ValueError('positive explicit BUSY duration and timer flags required')
        if after_status_read is not None and not callable(after_status_read):
            raise ValueError('explicit chip-clock scheduler required')
        self.registers, self.address_latches = registers, address_latches
        self.tick, self.busy_until, self.busy_ticks = tick, busy_until, busy_ticks
        self.timer_flags, self.after_status_read = timer_flags, after_status_read
        self.events, self.status_reads = [], []

    def advance(self, ticks):
        if type(ticks) is not int or ticks < 0:
            raise ValueError('explicit nonnegative chip-clock grant required')
        self.tick += ticks

    def read_status(self):
        value = (0x80 if self.tick < self.busy_until else 0) | self.timer_flags
        self.status_reads.append((self.tick, value))
        if self.after_status_read is not None:
            self.after_status_read(self, value)
        return value

    def write(self, port, value):
        byte(value)
        if type(port) is not int or not 0 <= port <= 3:
            raise ValueError('actual FM port index required')
        bank = port // 2
        if not port & 1:
            self.address_latches[bank] = value
            self.events.append(('address', self.tick, bank, value))
        else:
            register = self.address_latches[bank]
            self.registers[bank * 256 + register] = value
            self.events.append(('register', self.tick, bank, register, value))
            self.busy_until = self.tick + self.busy_ticks


class OwnedAudioDeviceBus:
    """Actual serial-bank mapping and FM port writes over owned physical DATA."""

    def __init__(self, material, fm, *, bank_base, psg_write, transfer_boundary):
        if type(material) is not OwnedSoundMaterial or not isinstance(fm, FmPortDevice):
            raise ValueError('owned sound material and real register device required')
        if type(bank_base) is not int or not 0 <= bank_base <= 0xFF8000 or bank_base & 0x7FFF:
            raise ValueError('explicit 24-bit 32 KiB bank base required')
        if not callable(psg_write) or not callable(transfer_boundary):
            raise ValueError('explicit PSG and progressive scheduling owners required')
        self.material, self.fm, self.bank_base = material, fm, bank_base
        self.psg_write, self.on_transfer = psg_write, transfer_boundary
        self.bank_writes, self.bank_reads = [], []

    def read_byte(self, address):
        word(address)
        if 0x4000 <= address < 0x6000:
            return self.fm.read_status()
        if address >= 0x8000:
            physical = self.bank_base | (address & 0x7FFF)
            value = self.material.data.read(physical, 1)
            self.bank_reads.append((address, physical, value))
            return value
        raise AudioBoundary('unbound non-RAM sound read')

    def write_byte(self, address, value):
        word(address); byte(value)
        if 0x4000 <= address < 0x6000:
            return self.fm.write(address & 3, value)
        if 0x6000 <= address < 0x6100:
            self.bank_base = (self.bank_base >> 1 | (value & 1) << 23) & 0xFF8000
            self.bank_writes.append(value & 1)
            return
        if address == 0x7F11:
            return self.psg_write(value)
        raise AudioBoundary('unbound non-RAM sound write')

    def progress(self, reason):
        raise AudioBoundary('unbound asynchronous chip progress; supply explicit clock grants')

    def transfer_boundary(self, reason):
        return self.on_transfer(reason)


class ExplicitAudioPlatform(AudioPlatform):
    """Supplied alternate groups and condition providers, no guessed refresh/WZ."""

    def __init__(self, *, alternate_accumulator, alternate_group, refresh_reader,
                 memory_bit_reader, control_owner=None):
        word(alternate_accumulator)
        if type(alternate_group) is not AlternateGroup:
            raise ValueError('explicit complete alternate word group required')
        alternate_group.validate()
        if not callable(refresh_reader) or not callable(memory_bit_reader):
            raise ValueError('actual refresh and memory-BIT condition providers required')
        self.alternate_accumulator, self.alternate_group = alternate_accumulator, alternate_group
        self.refresh_reader, self.memory_bit_reader = refresh_reader, memory_bit_reader
        if control_owner is not None and any(not callable(getattr(control_owner, name, None))
                for name in ('set_interrupt_vector', 'set_refresh', 'interrupt_control', 'interrupt_mode')):
            raise ValueError('explicit complete audio control owner required')
        self.control_owner = control_owner

    def set_interrupt_vector(self, value):
        if self.control_owner is None:
            return super().set_interrupt_vector(value)
        return self.control_owner.set_interrupt_vector(value)

    def set_refresh(self, value):
        if self.control_owner is None:
            return super().set_refresh(value)
        return self.control_owner.set_refresh(value)

    def interrupt_control(self, enabled, deferred_one_instruction):
        if self.control_owner is None:
            return super().interrupt_control(enabled, deferred_one_instruction)
        return self.control_owner.interrupt_control(enabled, deferred_one_instruction)

    def interrupt_mode(self, mode):
        if self.control_owner is None:
            return super().interrupt_mode(mode)
        return self.control_owner.interrupt_mode(mode)

    def exchange_alternate_accumulator(self, current):
        word(current)
        previous, self.alternate_accumulator = self.alternate_accumulator, current
        return previous

    def exchange_alternate_group(self, current):
        if type(current) is not AlternateGroup:
            raise ValueError('actual alternate word group required')
        current.validate()
        previous, self.alternate_group = self.alternate_group, current
        return previous

    def read_refresh(self, previous_conditions):
        value, conditions = self.refresh_reader(byte(previous_conditions))
        return byte(value), byte(conditions)

    def memory_bit_conditions(self, context):
        return byte(self.memory_bit_reader(context.validate()))

    def indirect_transfer(self, image, target, context):
        raise AudioBoundary('unbound owned sound tail: ' + image + ':' + hex(target)
            + ' context=' + type(context).__name__ + ' live=' + repr(context))


@dataclass(frozen=True)
class DriverFrame:
    auxiliary_cursor: int
    channel_cursor: int
    conditions: int
    count_and_data: int
    lookup_cursor: int
    parameter_cursor: int
    sample: int
    stack_cursor: int

    def __post_init__(self):
        for field in fields(self):
            (byte if field.name in ('conditions', 'sample') else word)(getattr(self, field.name))


def run_driver_stage(sound, stage, frame, *, return_word, reset_epoch):
    """Call one existing recovered stage under explicit sound execution ownership.

    Real call pushes and consumes its return word in shared RAM. Every returned
    context field is adopted; absent fields retain their actual incoming carrier.
    This adds finite semantic adapters, not an opcode execution loop.
    """
    if type(sound) is not SoundDevice or type(frame) is not DriverFrame:
        raise ValueError('one real sound owner and complete actual driver frame required')
    word(return_word)
    if type(reset_epoch) is not int or reset_epoch != sound.reset_epoch:
        raise AudioBoundary('stage frame belongs to a different reset epoch')
    if sound.executing or sound.reset_asserted or sound.bus_requested or sound.m68k_granted:
        raise AudioBoundary('stage requires actual released sound execution ownership')
    from tools.high_level_audio_engine import business_loaders, business_hardware, business_mailbox, business_sequence, contexts
    entries = {
        'initialize_audio_bank': (business_loaders.initialize_audio_bank, contexts.InitializeAudioBankInput),
        'poll_command_mailboxes': (business_mailbox.poll_command_mailboxes, contexts.PollCommandMailboxesInput),
        'dispatch_sound_command': (business_loaders.dispatch_sound_command, contexts.DispatchSoundCommandInput),
        'update_audio_driver': (business_hardware.update_audio_driver, contexts.UpdateAudioDriverInput),
        'select_instrument': (business_sequence.select_instrument, contexts.SelectInstrumentInput),
    }
    if type(stage) is not str or stage not in entries:
        raise AudioBoundary('unbound recovered driver stage')
    function, input_type = entries[stage]
    sound.executing = True
    try:
        stack = sound.audio_state.push_word(frame.stack_cursor, return_word)
        values = {field.name: getattr(frame, field.name) for field in fields(input_type)
                  if field.name not in ('stack_cursor', 'continuation')}
        values.update(stack_cursor=stack, continuation=Continuation('driver', return_word))
        result = function(sound.audio_state, input_type(**values))
        returned = replace(frame, **{field.name: getattr(result, field.name) for field in fields(result)})
        if returned.stack_cursor != frame.stack_cursor:
            raise AudioBoundary('stage returned through a different shared stack extent')
        return returned
    finally:
        sound.executing = False
