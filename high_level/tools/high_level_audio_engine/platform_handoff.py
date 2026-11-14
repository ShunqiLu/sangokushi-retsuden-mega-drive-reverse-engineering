"""Explicit expired-cold platform handoff on the same actual AudioState.

No continuation guard is broadened. The only ownership commit replaces the
existing AudioState.platform reference with an exact ExplicitAudioPlatform.
Sound RAM, bus/devices, Scene, control, epochs, alternate values and providers
remain real explicitly supplied state. This module runs no game startup.
"""
from dataclasses import dataclass
import threading

from tools.high_level_audio_engine.cold_workspace import (
    ColdWorkspacePlatform,ColdWorkspaceSession,ColdWorkspaceIdlePoint,
)
from tools.high_level_audio_engine.control_reset import AudioControlOwner
from tools.high_level_audio_engine.domain import AudioBoundary,AudioState,AlternateGroup,word
from tools.high_level_audio_engine.hardware_scene import SoundDevice,SharedSoundAudioBus
from tools.high_level_audio_engine.owned_runtime import ExplicitAudioPlatform


_BASE_METHODS = (
    'set_interrupt_vector','set_refresh','interrupt_control','interrupt_mode',
    'exchange_alternate_accumulator','exchange_alternate_group','read_refresh','memory_bit_conditions',
)


def _original_method(instance,name,owner):
    method = getattr(instance,name,None)
    if (name in instance.__dict__ or getattr(method,'__self__',None) is not instance
            or getattr(method,'__func__',None) is not getattr(owner,name)):
        raise AudioBoundary('actual original platform/state method required: '+name)


@dataclass(frozen=True)
class PlatformHandoffWitness:
    """Actual atomic migration evidence, not a driver entry/execution lease."""
    sound: object
    scene: object
    audio_state: object
    shared_bus: object
    ram: object
    device_bus: object
    control: object
    previous_platform: object
    platform: object
    expired_cold_session: object
    installation: object
    reset_epoch: int
    generation: int
    alternate_AF_at_commit: int
    alternate_group_at_commit: AlternateGroup
    refresh_provider_retained: bool
    memory_bit_provider_retained: bool
    audio_DATA_operations_at_commit: int

    def require_attached(self,sound,control):
        """Check attachment/epoch only, even after genuine driver state writes.

        Installation RAM readiness is separately owned by the installation
        witness and fresh driver authority. This method does not re-run that
        pre-entry RAM comparison after the driver legitimately changes RAM.
        """
        if (sound is not self.sound or control is not self.control
                or sound.scene is not self.scene or sound.audio_state is not self.audio_state
                or sound.audio_state.platform is not self.platform
                or type(self.platform) is not ExplicitAudioPlatform
                or self.platform.control_owner is not control
                or self.audio_state.bus is not self.shared_bus or self.shared_bus.device is not sound
                or self.shared_bus.ram is not self.ram or sound.ram is not self.ram
                or self.shared_bus.devices is not self.device_bus
                or sound.reset_epoch != self.reset_epoch or control.generation != self.generation):
            raise AudioBoundary('platform handoff belongs to another current owner/reset attachment')
        return self.platform

    def describe(self):
        """Compact serializable facts; never serialize RAM, callbacks or devices."""
        return dict(confidence='confirmed_explicit_same_AudioState_platform_owner_commit',
            previous_platform_type=type(self.previous_platform).__name__,
            current_platform_type=type(self.platform).__name__,reset_epoch=self.reset_epoch,generation=self.generation,
            same_Scene=True,same_SoundDevice=True,same_AudioState=True,same_shared_bus_RAM_devices=True,
            same_control_owner=True,alternate_AF_at_commit=self.alternate_AF_at_commit,
            alternate_BC_DE_HL_at_commit=dict(count_and_data=self.alternate_group_at_commit.count_and_data,
                parameter_cursor=self.alternate_group_at_commit.parameter_cursor,
                lookup_cursor=self.alternate_group_at_commit.lookup_cursor),
            refresh_provider_retained=self.refresh_provider_retained,
            memory_bit_provider_retained=self.memory_bit_provider_retained,
            read_providers_invoked_by_handoff=False,audio_DATA_operations_at_commit=self.audio_DATA_operations_at_commit,
            sole_ownership_commit='existing_audio_state.platform=new_exact_ExplicitAudioPlatform',
            RAM_control_epoch_or_claim_mutated=False,continuation_guards_changed=False,
            driver_entry_lease_granted=False,driver_program_executed=False)


def handoff_expired_cold_platform(sound,control,*,expired_cold_session,installation,
        refresh_reader,memory_bit_reader):
    """Migrate only a genuinely reset-expired cold platform after real6950.

    installation is the exact peer-owned DriverInstallationWitness. Its
    require_current method must validate the actual ordered6950 installation
    without granting a bus/entry or mutating state. Import is deferred so this
    small module may be inspected before that independent additive dependency
    is installed; use still stops honestly if the dependency is missing.

    Caller explicitly retains the old R/BIT providers by passing those actual
    callables, or explicitly supplies new bounded driver read authorities.
    No callback is invoked or consumed by this ownership handoff.
    """
    from tools.high_level_audio_engine.driver_installation import DriverInstallationWitness
    from tools.high_level_audio_engine import continuations

    if (type(sound) is not SoundDevice or sound.scene is None or type(control) is not AudioControlOwner
            or control.sound is not sound or type(sound.audio_state) is not AudioState
            or type(sound.audio_state.bus) is not SharedSoundAudioBus):
        raise ValueError('exact same bound sound/control/AudioState/shared-bus owners required')
    if type(installation) is not DriverInstallationWitness:
        raise AudioBoundary('actual exact ordered-copy driver installation witness required')
    validator = installation.require_current
    if (getattr(validator,'__self__',None) is not installation
            or getattr(validator,'__func__',None) is not DriverInstallationWitness.require_current):
        raise AudioBoundary('original exact installation witness validator required')
    if type(expired_cold_session) is not ColdWorkspaceSession:
        raise AudioBoundary('actual prior cold-workspace session witness required')
    if not callable(refresh_reader) or not callable(memory_bit_reader):
        raise ValueError('both explicit retained-or-new R/BIT provider callables required')

    # This is the existing scoped continuation lock. No existing guard, callee,
    # binding provider or global active-session value is changed here.
    with continuations._SESSION_LOCK:
        state = sound.audio_state
        bus = state.bus
        old = state.platform
        cold = expired_cold_session
        if (type(old) is not ColdWorkspacePlatform or old.control_owner is not control
                or bus.device is not sound or bus.ram is not sound.ram):
            raise AudioBoundary('exact current cold platform and same shared RAM attachment required')
        if (threading.get_ident() != cold.thread or cold.sound is not sound or cold.state is not state
                or cold.scene is not sound.scene or cold.control is not control or cold.failed
                or not cold.started or old.workspace_session is not cold
                or type(cold.waiting) is not ColdWorkspaceIdlePoint or cold.waiting.session is not cold
                or cold.waiting.pc != 0 or cold.waiting.generation != cold.generation
                or cold.waiting.reset_epoch != cold.reset_epoch):
            raise AudioBoundary('actual completed cold idle lineage belongs to another invocation')
        if (control.generation <= cold.generation or sound.reset_epoch <= cold.reset_epoch
                or ('reset_asserted',cold.reset_epoch,cold.generation+1) not in control.events):
            raise AudioBoundary('cold session must have expired through the actual later RESET owner')
        if (sound.executing or sound.reset_asserted or control.reset_asserted
                or sound.bus_requested or sound.m68k_granted
                or control.phase != 'startup-pending' or control.control.pc_entry != 0
                or control._lease is not None or control._frame_session is not None):
            raise AudioBoundary('handoff requires real released pending-driver state without a live claim')
        if continuations._ACTIVE_SESSION is not None:
            raise AudioBoundary('platform handoff cannot overlap a scoped audio continuation')
        _original_method(state,'indirect_transfer',AudioState)
        _original_method(old,'indirect_transfer',ColdWorkspacePlatform)
        for name in _BASE_METHODS:
            _original_method(old,name,ExplicitAudioPlatform)
        word(old.alternate_accumulator)
        if type(old.alternate_group) is not AlternateGroup:
            raise AudioBoundary('actual current alternate register group required')
        old.alternate_group.validate()

        # Copy/source semantics and current installation RAM are exclusively
        # checked by the exact peer-owned witness, not a duplicate count test.
        before_operations = state.data_operations
        before_control_state = control.control
        installation.require_current(sound,control)
        if (installation.sound is not sound or installation.scene is not sound.scene
                or installation.audio_state is not state or installation.shared_bus is not bus
                or installation.ram is not sound.ram or installation.control is not control
                or installation.source_data is not sound.scene.data
                or installation.reset_epoch != sound.reset_epoch or installation.generation != control.generation
                or state.data_operations != before_operations or control.control is not before_control_state
                or state.platform is not old):
            raise AudioBoundary('validated driver installation/current platform authority changed during handoff')

        new = ExplicitAudioPlatform(alternate_accumulator=old.alternate_accumulator,
            alternate_group=old.alternate_group,refresh_reader=refresh_reader,
            memory_bit_reader=memory_bit_reader,control_owner=control)
        witness = PlatformHandoffWitness(sound,sound.scene,state,bus,sound.ram,bus.devices,control,
            old,new,cold,installation,sound.reset_epoch,control.generation,
            old.alternate_accumulator,old.alternate_group,
            refresh_reader is old.refresh_reader,memory_bit_reader is old.memory_bit_reader,before_operations)
        # The sole ownership commit. In particular no claim, RAM byte, chip,
        # epoch, alternate register or generic continuation guard is edited.
        state.platform = new
        return witness
