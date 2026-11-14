"""Actual cold-resume/6950 copy witness and fresh driver-entry authority.

No RAM/chip/control/stack is written here. This is entry provenance over the
same persistent original reset/main owner, exact source/read/write sequence,
real resets and current RAM, not a count-only or byte-pattern-ready shortcut.
"""
from dataclasses import dataclass
import threading
from types import GeneratorType

from tools.high_level_audio_engine.control_reset import AudioEntryAuthority,AudioControlState
from tools.high_level_audio_engine.cold_workspace import ColdWorkspacePlatform,ColdWorkspaceSession
from tools.high_level_audio_engine.domain import AudioBoundary,byte,word
from tools.high_level_audio_engine.hardware_scene import SoundDevice,SharedSoundAudioBus
from tools.high_level_audio_engine.owned_runtime import DriverFrame,OwnedAudioDeviceBus
from tools.high_level_main_flows import business_lowbank,bootstrap_steps
from tools.high_level_main_flows.bootstrap_reset import PersistentColdResetSession,ResetAudioReleasePoint
from tools.high_level_main_flows.bootstrap_steps import BootstrapMainSession,BootstrapMainWait
from tools.high_level_main_flows.cartridge_source_data import CartridgeSourceData


COPY_SPANS=((0x69d2,0x0000,4096),(0x799c,0x1000,3584),(0x69aa,0x1c00,13))


def _callback(value):
    return getattr(value,'__self__',None),getattr(value,'__func__',value)


def _same_callback(left,right):
    a,b=_callback(left),_callback(right)
    return a[0] is b[0] and a[1] is b[1]


@dataclass(frozen=True)
class DriverInstallationWitness:
    sound: object
    scene: object
    audio_state: object
    shared_bus: object
    ram: object
    control: object
    source_data: object
    reset_epoch: int
    generation: int
    _capture: object
    evidence: dict

    def require_current(self,sound,control):
        """Validate only: no lease, bus/chip read, callbacks or state mutation."""
        return self._capture.require_witness(self,sound,control)


class DriverInstallationCapture:
    """Arm after real cold JP0 idle, before the same reset resumes at262.

    Finish only at its actual first3BC. That interval naturally includes288's
    assertion, the original6950's two releases, all three source copies and
    final BUSREQ release. Never invoke6950 again merely to acquire evidence.
    """
    def __init__(self,sound,control,source,*,reset_session):
        if (type(sound) is not SoundDevice or sound.scene is None or control.sound is not sound
                or type(source) is not CartridgeSourceData or sound.scene.data is not source.data
                or type(reset_session) is not PersistentColdResetSession or reset_session.state is not sound.scene):
            raise ValueError('same actual cold Scene/sound/reset and complete typed own-source authority required')
        reset_session._guard()
        release=reset_session.waiting
        platform=sound.audio_state.platform
        if (reset_session.phase!='actual-audio-release' or type(release) is not ResetAudioReleasePoint
                or release.session is not reset_session or release.pc!=0x262
                or type(platform) is not ColdWorkspacePlatform or platform.control_owner is not control):
            raise AudioBoundary('actual cold-release/cold-platform continuation required before resume')
        cold=platform.workspace_session
        if type(cold) is not ColdWorkspaceSession or cold.sound is not sound:
            raise AudioBoundary('actual same-State completed cold idle owner required')
        idle=cold.observe_idle()
        if idle.session is not cold or control._frame_session is not cold:
            raise AudioBoundary('actual live cold idle claim must precede real288 invalidation')
        bus=sound.audio_state.bus
        if type(bus) is not SharedSoundAudioBus or bus.device is not sound or bus.ram is not sound.ram:
            raise AudioBoundary('one actual shared8192-byte sound RAM bus required')
        devices=bus.devices
        if (type(devices) is not OwnedAudioDeviceBus or not devices.material.data.segments
                or not callable(devices.psg_write) or not callable(devices.on_transfer)):
            raise AudioBoundary('same explicit nonempty owned bank DATA and device owners required')
        if sound.executing or sound.reset_asserted or sound.bus_requested or sound.m68k_granted:
            raise AudioBoundary('inactive released actual cold idle required')
        if (len(source.data.segments)!=1 or source.data.segments[0][0]!=0
                or len(source.data.segments[0][1])!=0x100000
                or source.evidence.get('format')!='g5510-explicit-complete-cartridge-source-DATA-v1'):
            raise AudioBoundary('complete explicit own-source partition required, not opaque ROM fallback')
        self.sound,self.control,self.scene,self.audio_state=sound,control,sound.scene,sound.audio_state
        self.source,self.source_data,self.source_segments=source,source.data,source.data.segments
        self.reset_session,self.release,self.cold,self.idle=reset_session,release,cold,idle
        self.shared_bus,self.ram,self.devices=bus,sound.ram,devices
        self.platform,self.schedule=platform,sound.schedule
        self.fm,self.material,self.bank_data=devices.fm,devices.material,devices.material.data
        self.bank_segments,self.bank_base=self.bank_data.segments,devices.bank_base
        self.psg_write,self.transfer=devices.psg_write,devices.on_transfer
        self.scene_events,self.control_events=self.scene.events,control.events
        self.scene_start,self.control_start=len(self.scene_events),len(self.control_events)
        self.epoch,self.generation=sound.reset_epoch,control.generation
        self.operations,self.pre_ram=self.audio_state.data_operations,bytes(self.ram)
        self.thread=threading.get_ident()
        self.copy_function=business_lowbank.initialize_z80_sound_image_fields
        self.reset_function=business_lowbank.release_z80_reset_fields
        self.main_function=bootstrap_steps.bootstrap_main_program
        self.copy_code,self.reset_code,self.main_code=(self.copy_function.__code__,
            self.reset_function.__code__,self.main_function.__code__)
        self.witness=None
        self.after_ram=self.after_control=None
        self.sealed_waiting=None
        self.finished=False

    def _identities(self):
        s,a,c=self.sound,self.audio_state,self.control
        d=self.devices
        if (threading.get_ident()!=self.thread or s.scene is not self.scene or s.audio_state is not a
                or a.bus is not self.shared_bus or self.shared_bus.device is not s
                or s.ram is not self.ram or self.shared_bus.ram is not self.ram
                or self.shared_bus.devices is not d or d.fm is not self.fm or d.material is not self.material
                or d.material.data is not self.bank_data or self.bank_data.segments is not self.bank_segments
                or d.bank_base!=self.bank_base or not _same_callback(d.psg_write,self.psg_write)
                or not _same_callback(d.on_transfer,self.transfer) or s.schedule is not self.schedule
                or self.scene.data is not self.source_data or self.source_data.segments is not self.source_segments
                or self.scene.events is not self.scene_events or c.events is not self.control_events
                or c.sound is not s or getattr(a.platform,'control_owner',None) is not c
                or a.data_operations!=self.operations):
            raise AudioBoundary('copy installation State/source/device/control identity or audio-execution history changed')
        if (business_lowbank.initialize_z80_sound_image_fields is not self.copy_function
                or business_lowbank.release_z80_reset_fields is not self.reset_function
                or bootstrap_steps.bootstrap_main_program is not self.main_function
                or self.copy_function.__code__ is not self.copy_code or self.reset_function.__code__ is not self.reset_code
                or self.main_function.__code__ is not self.main_code):
            raise AudioBoundary('actual named copy/reset/main owner changed during installation evidence')

    def finish(self,waiting):
        if self.finished:
            raise AudioBoundary('one real cold-resume installation window may be sealed once')
        self._identities()
        reset=self.reset_session
        reset._guard()
        main=reset.main_session
        if (self.audio_state.platform is not self.platform or reset.phase!='original-main-tail'
                or type(waiting) is not BootstrapMainWait or waiting is not reset.waiting
                or waiting.state is not self.scene or waiting.poll!=0x3bc
                or type(main) is not BootstrapMainSession or main.waiting is not waiting
                or main.state is not self.scene or main.suspensions!=1 or main._failed
                or type(main._program) is not GeneratorType or main._program.gi_running
                or main._program.gi_code is not self.main_function.__code__
                or waiting.frame.stack_cursor.base!=0x00fffe00):
            raise AudioBoundary('the same actual original reset/main first3BC continuation required')
        waiting.validate()
        if (self.sound.reset_epoch!=self.epoch+2 or self.control.generation!=self.generation+2
                or self.control.phase!='startup-pending' or self.control._frame_session is not None
                or self.control._lease is not None or self.sound.executing or self.sound.reset_asserted
                or self.sound.bus_requested or self.sound.m68k_granted
                or self.control.control!=AudioControlState(0,0,0,False,False,0,False)):
            raise AudioBoundary('actual288/two6950 releases must leave fresh pending PC0 with released bus')
        resets=[event for event in self.control_events[self.control_start:]
            if event[0] in ('reset_asserted','reset_released_pending')]
        expected=[('reset_asserted',self.epoch,self.generation+1),
            ('reset_released_pending',self.epoch+1,self.generation+1),
            ('reset_asserted',self.epoch+1,self.generation+2),
            ('reset_released_pending',self.epoch+2,self.generation+2)]
        if (len(resets)!=4 or any(tuple(event[:3])!=row for event,row in zip(resets,expected))
                or any(event[3]<3 for event in resets if event[0]=='reset_released_pending')):
            raise AudioBoundary('real reset assertion/release ordering or explicit pulse clocks differ')
        events=self.scene_events
        start,end=self.scene_start,len(events)
        sources=[index for index in range(start,end) if events[index][:3]==('read',0x69d2,1)]
        if len(sources)!=1:
            raise AudioBoundary('one actual original6950 first source BYTE read required in this window')
        cursor=sources[0]
        expected_ram=bytearray(self.pre_ram)
        write_indices=[]
        span_evidence=[]
        for source,destination,length in COPY_SPANS:
            first=cursor
            for offset in range(length):
                value=self.source_data.read(source+offset,1)
                expected_read=('read',source+offset,1,value)
                expected_write=('write',0xa00000+destination+offset,1,value)
                if cursor+1>=end or events[cursor]!=expected_read or events[cursor+1]!=expected_write:
                    raise AudioBoundary('actual ordered source/read/write copy differs at source '+hex(source+offset))
                expected_ram[destination+offset]=value
                write_indices.append(cursor+1)
                cursor+=2
            span_evidence.append(dict(source=source,destination=destination,bytes=length,
                first_read_event=first,last_write_event=cursor-1))
        all_ram_writes=[index for index in range(start,end) if events[index][0]=='write'
            and 0xa00000<=events[index][1]&0xffffff<0xa02000]
        if all_ram_writes!=write_indices or bytes(self.ram)!=bytes(expected_ram):
            raise AudioBoundary('additional/omitted sound writes or final8192-byte retained RAM differs')
        requests=[index for index in range(start,sources[0]) if events[index]==('write',0xa11100,2,0x100)]
        releases=[index for index in range(cursor,end) if events[index]==('write',0xa11100,2,0)]
        if len(requests)!=1 or not releases:
            raise AudioBoundary('actual6950 BUSREQ request/final release not found uniquely')
        request,release=requests[0],releases[0]
        control_trace=[event for event in events[request:release+1]
            if event[0] in ('read','write') and event[1]&0xffffff in (0xa11100,0xa11200)]
        prefix=[('write',0xa11100,2,0x100),('write',0xa11200,2,0),('write',0xa11200,2,0x100)]
        suffix=[('write',0xa11200,2,0),('write',0xa11200,2,0x100),('write',0xa11100,2,0)]
        ack=control_trace[len(prefix):-len(suffix)]
        if (control_trace[:3]!=prefix or control_trace[-3:]!=suffix or not ack
                or any(event[:3]!=('read',0xa11100,1) for event in ack)
                or any(not event[3]&1 for event in ack[:-1]) or ack[-1][3]&1):
            raise AudioBoundary('actual6950 control/BUSACK/read-copy-release sequence differs')
        self.finished=True
        self.after_ram,self.after_control=bytes(self.ram),self.control.control
        self.sealed_waiting=waiting
        evidence=dict(confidence='confirmed_same_live_original_reset_main_and_three_ordered_copy_sequences',
            source_provenance=self.source.evidence,source_union_bytes=7639,actual_BYTE_writes=7693,
            physical_source_alias_bytes=54,last_seed_overwrite_Z80=[0x1c00,0x1c0d],
            copied_Z80_extent=[0,0x1e00],retained_Z80_extent=[0x1e00,0x2000],
            spans=span_evidence,Scene_window=[start,end],actual_BUSREQ_request_event=request,
            actual_BUSREQ_release_event=release,actual_BUSACK_samples=len(ack),
            actual_reset_transitions=resets,Audio_DATA_operations_unchanged=self.operations,
            same_full_RAM=True,host_installer=False,original_ROM_input=False,new_CODE_bytes=0)
        self.witness=DriverInstallationWitness(self.sound,self.scene,self.audio_state,
            self.shared_bus,self.ram,self.control,self.source_data,self.sound.reset_epoch,
            self.control.generation,self,evidence)
        return self.witness

    def require_witness(self,witness,sound,control):
        self._identities()
        if (not self.finished or witness is not self.witness or sound is not self.sound or control is not self.control
                or self.sound.reset_epoch!=witness.reset_epoch or self.control.generation!=witness.generation
                or self.control.control is not self.after_control or self.control.phase!='startup-pending'
                or self.control._lease is not None or self.control._frame_session is not None
                or self.reset_session.waiting is not self.sealed_waiting
                or self.reset_session.main_session.suspensions!=1
                or self.sound.executing or self.sound.reset_asserted or self.sound.bus_requested
                or self.sound.m68k_granted or bytes(self.ram)!=self.after_ram):
            raise AudioBoundary('expired/altered driver installation witness cannot authorize entry')
        return witness


class DriverInstalledAuthority(AudioEntryAuthority):
    """Single-use actual-copy entry authority, with all eight carriers supplied.

    It does not infer reset general registers, reuse a cold lease, install RAM,
    select an audio platform, write a return slot or execute driver PC0 itself.
    """
    def __init__(self,installation,entry_frame):
        if type(installation) is not DriverInstallationWitness or type(entry_frame) is not DriverFrame:
            raise ValueError('exact sealed installation and explicit complete initial driver frame required')
        for name,value in vars(entry_frame).items():
            (byte if name in ('conditions','sample') else word)(value)
        installation.require_current(installation.sound,installation.control)
        self.installation,self.frame,self.used=installation,entry_frame,False

    def provide_frame(self,sound,entry_kind,entry_address,control_state):
        witness=self.installation
        witness.require_current(sound,witness.control)
        if (self.used or entry_kind!='driver' or entry_address!=0
                or control_state is not witness.control.control):
            raise AudioBoundary('fresh original installed-driver PC0 authority required')
        self.used=True
        return self.frame
