"""New complete206→300 checksum→first3BC, with no Z80 program execution."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
import traceback


def _write_json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def _frame_fields(frame):
    return dict(D_LONGs=[frame.carrier(name) for name in
        ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')],
        A0_A6_LONGs=[getattr(frame, name).base for name in
        ('roster','candidates','controller','scan','opponent','scratch','auxiliary')],
        A7=frame.stack_cursor.base, CCR_X=frame.status)


def _actual_checksum_read_sequence(events):
    """Count original reads and branch ordering; never calculate their sum."""
    begin = next(index for index, event in enumerate(events)
        if event[:3] == ('read', 0x1A4, 4))
    cursor, count, compare_index = 0x200, 0, None
    for index in range(begin + 1, len(events)):
        event = events[index]
        if event[0] != 'read':
            continue
        if cursor < 0x100000:
            if event[1:3] != (cursor, 2):
                raise AssertionError('actual original checksum read sequence differs at ' + hex(cursor))
            cursor += 2
            count += 1
        else:
            if event[1:3] != (0x18E, 2):
                raise AssertionError('original checksum loop did not next read stored18E WORD')
            compare_index = index
            break
    if count != 524032 or cursor != 0x100000 or compare_index is None:
        raise AssertionError('actual complete original524032 WORD checksum source traversal required')
    marker_index = next(index for index in range(compare_index + 1, len(events))
        if events[index] == ('write', 0xFFFFFFFC, 4, 0x696E6974))
    return dict(confidence='confirmed_original_read_sequence_and_cold_success_branch',
        first_read=0x200, last_read=0xFFFFE, exclusive_end=0x100000,
        actual_WORD_reads=count, actual_body_bytes=count*2,
        inclusive_end_LONG=events[begin][3], stored_checksum_WORD=events[compare_index][3],
        compare_read_event=compare_index, later_original_init_write_event=marker_index,
        host_checksum_calculated=False, header_or_result_modified=False)


def run(project_root, sound_native_root, sources, output):
    project_root = project_root.resolve(strict=True)
    if output.exists() or not output.parent.is_dir() or not output.resolve().is_relative_to(project_root/'build'):
        raise ValueError('fresh explicit workspace build output required')
    output.mkdir()
    sys.path.insert(0, str(project_root))
    from tools.high_level_audio_engine import target
    from tools.high_level_audio_engine.control_reset import AudioControlOwner, AudioControlState, FinitePulseSoundSchedule
    from tools.high_level_audio_engine.domain import AudioBoundary, AudioState, AlternateGroup
    from tools.high_level_audio_engine.fm_ports import FmPortDevice
    from tools.high_level_audio_engine.hardware_scene import SharedSoundAudioBus, SoundDevice, SceneSoundHardwareBus
    from tools.high_level_audio_engine.hardware_scene_psg import ScenePsgHardwareBus
    from tools.high_level_audio_engine.owned_runtime import ExplicitAudioPlatform, OwnedAudioDeviceBus, OwnedSoundMaterial
    from tools.high_level_audio_engine.psg_device import SegaPsgState, SegaPsgDevice
    from tools.high_level_input.hardware_controller import SceneControllerHardwareBus, ThreeButtonPad, PadButtons, DisconnectedPort
    from tools.high_level_main_flows.bootstrap_stacks import BankedStackControl
    from tools.high_level_main_flows.bootstrap_steps import BootstrapMainSession, BootstrapMainWait
    from tools.high_level_main_flows.business_boot import reset_console_frame_fields
    from tools.high_level_main_flows.cartridge_source_data import load_cartridge_source_data, project_cartridge_m68k_authorities
    from tools.high_level_main_flows.contexts_boot import ResetProfile
    from tools.high_level_main_flows.contexts_gameplay import FirstDeploymentFrame, MovementContinuationBoundary
    from tools.high_level_main_flows.runtime import create_linked_scene_state
    from tools.high_level_main_flows.services import LogicalServices
    from tools.high_level_scene_flows.domain import HardwareBus, ReadOnlyData
    from tools.high_level_video.frame_interrupts import SuppliedVideoEvents, VideoBusState
    from tools.high_level_video.hardware_vdp import VdpMemory, VdpController, SceneVdpHardwareBus
    from tools.high_level_video.write_dma_events import SceneWriteDmaEvents, WriteDmaGrant

    report = dict(status='running_new_cold68000_only_reset_checksum_case',
        original_ROM_or_emulator_input=False, native_rebuilds=0, hashes_computed=0,
        host_checksum_calculated=False, original_code_or_header_modified=False,
        old_case_or_API_replays=0, new_formal_CODE_bytes=0,
        cold_Z80_startup_executed=False, dual_CPU_cold_boot_success=False)
    state = sound = audio = psg = control = write_events = video_events = None
    try:
        logical_root = project_root/'tools/high_level_audio_engine'
        logical_sources = {name: (logical_root/name).read_text(encoding='utf-8') for name in target.BUSINESS_MODULES}
        cartridge = load_cartridge_source_data(project_root,
            m68k_authorities=project_cartridge_m68k_authorities(),
            sound_native_root=sound_native_root, sound_logical_sources=logical_sources,
            resource_manifest=sources)
        report['source_authority'] = cartridge.evidence

        class UnboundFm(FmPortDevice):
            def read_status(self):
                raise AudioBoundary('cold68000-only case supplied no FM execution/status')

            def write(self, port, value):
                raise AudioBoundary('cold68000-only case supplied no FM execution')

        def no_audio_transfer(reason):
            raise AudioBoundary('cold68000-only case supplied no running audio transfer')

        # Preserve187's explicit digital experiment, not guessed chip defaults.
        psg = SegaPsgDevice(SegaPsgState((41,67,89), (0,1,2,3), 0,
            (41,67,89), (1,1,1), 4,16,0,1,7),
            clock_hz=3579545, sample_rate_hz=44100,
            channel_gain=(4096,2048,2048,4096), pcm_sink=None)
        control = AudioControlOwner(AudioControlState(None,None,None,None,None,None,None), reset_asserted=False)
        platform = ExplicitAudioPlatform(alternate_accumulator=0x5AA5,
            alternate_group=AlternateGroup(0x1234,0x5678,0x9ABC),
            refresh_reader=lambda previous: (0xA7,previous),
            memory_bit_reader=lambda context: context.previous_conditions, control_owner=control)
        ports = OwnedAudioDeviceBus(OwnedSoundMaterial(ReadOnlyData(),(),(),0), UnboundFm(),
            bank_base=0, psg_write=psg.write, transfer_boundary=no_audio_transfer)
        audio = AudioState(SharedSoundAudioBus(bytearray(8192),ports), platform,100)
        schedule = FinitePulseSoundSchedule(control, reset_pulse_clocks=(5,4,4),
            bus_transfer_permits=(True,True), open_bus_reader=lambda address,size: 0)
        sound = SoundDevice(audio,schedule,reset_asserted=False,bus_requested=False,m68k_granted=False)
        control.bind(sound)
        memory = VdpMemory(bytearray(65536),bytearray(128),bytearray(80),bytearray(32))
        video_events = SuppliedVideoEvents(VideoBusState(0,None,None),(65535,18431),cpu_dma_stalls=True)
        vdp = VdpController(memory,status=video_events)
        video = SceneVdpHardwareBus(vdp,HardwareBus(),replace_vdp_mapping=True)
        io = bytearray(16)
        inputs = SceneControllerHardwareBus(io,
            (ThreeButtonPad(PadButtons()),ThreeButtonPad(PadButtons()),DisconnectedPort()),
            video,replace_controller_mapping=True)
        sound_bus = SceneSoundHardwareBus(sound,inputs,replace_sound_mapping=True)
        write_events = SceneWriteDmaEvents(sound_bus,vdp,
            (WriteDmaGrant(0xFFFFFC,4,0,1,65536),))
        hardware = ScenePsgHardwareBus(psg,write_events,replace_psg_mapping=True)
        state = create_linked_scene_state(bytearray(65536),data=cartridge.data,hardware=hardware,
            services=LogicalServices(()),max_reads=1000000,max_samples=8,sr=0x271B)
        video.bind_scene(state); sound_bus.bind_scene(state)
        video_events.bind_scene(state,vdp); write_events.bind_scene(state); hardware.bind_scene(state)
        frame = FirstDeploymentFrame(*(0xA1100100+index for index in range(8)),
            *(state.table_at(0xFFFF1000+index*0x100).cursor() for index in range(7)),
            state.table_at(0x00FFFC00).cursor(),0x1B)
        stacks = BankedStackControl(state,user_stack=0,supervisor_stack=frame.stack_cursor.base)
        profile = ResetProfile(stacks,state.table_at(0x294).cursor(),frame.choice)
        report['explicit_inputs'] = dict(IO_16_registers=list(io), retained_init_marker=0,
            SR=state.sr, frame=_frame_fields(frame), USP=0,
            reset_pulse_Z80_clocks=[5,4,4], bus_transfer_permits=[True,True],
            VDP_wait_transfer_units=[65535,18431],
            physical_write_DMA_grant=dict(address=0xFFFFFC,size=4,value=0,occurrence=1,units=65536),
            PSG=asdict(psg.state), Z80_program_execution_grants=0, PSG_clock_grants=0)
        entered_marker = int.from_bytes(state.ram[0xFFFC:0x10000],'big')
        if entered_marker != 0 or io[6] != 0:
            raise AssertionError('explicit cold profile must not preload retained init or warm GPIO')
        caught = None
        try:
            reset_console_frame_fields(state,frame,profile)
        except MovementContinuationBoundary as error:
            caught = error
        if caught is None:
            raise AssertionError('original nonreturning reset/main invocation did not retain its actual first wait')
        session = getattr(caught,'bootstrap_main_session',None)
        waiting = getattr(caught,'bootstrap_main_wait',None)
        if (type(session) is not BootstrapMainSession or type(waiting) is not BootstrapMainWait
                or session.state is not state or waiting.state is not state
                or waiting is not session.waiting or caught.target != 0x3BC
                or caught.context is not waiting.frame or session.suspensions != 1):
            raise caught
        if waiting.frame.stack_cursor.base != 0x00FFFE00:
            raise AssertionError('original00380 must set the actual supervisor SP to00FFFE00')
        point = stacks.capture(waiting.poll,waiting.frame)
        if state.read(0xFFFFF600,2) != 0 or state.read(0xFFFFF612,2) != 0x100:
            raise AssertionError('first real3BC must naturally follow startup0100/F600 clear')
        report['game_checksum'] = _actual_checksum_read_sequence(state.events)
        if state.read(0xFFFFFFFC,4) != 0x696E6974:
            raise AssertionError('original cold success branch must write and retain its real init marker')
        # The cold startup was later overwritten by6950; prove the original
        # temporary copy from ordered Scene source/read-write accesses instead.
        first_startup = next(index for index,event in enumerate(state.events)
            if event[:3] == ('read',0x2CA,1))
        for offset in range(38):
            read,write = state.events[first_startup+2*offset:first_startup+2*offset+2]
            if read[:3] != ('read',0x2CA+offset,1) or write != ('write',0xA00000+offset,1,read[3]):
                raise AssertionError('actual cold38-byte source/copy event sequence differs')
        original_psg = [event for event in state.events if event[0]=='write'
            and event[1]&0xFFFFFF in hardware.BYTE_PORTS]
        if original_psg != [('write',0xC00011,1,value) for value in (0x9F,0xBF,0xDF,0xFF)]:
            raise AssertionError('original complete reset must own exactly its four mute writes')
        if (audio.data_operations != 0 or psg.tick != 0 or psg.generated_samples != 0
                or control.phase != 'startup-pending' or sound.reset_epoch != 3):
            raise AssertionError('cold68000-only scope must retain unexecuted startup-pending audio')
        write_events.require_consumed()
        if video_events.dma_slots or video_events.consumed_slots != 2:
            raise AssertionError('exactly two supplied original6826/68CE DMA slots must be consumed')
        if schedule._pulse_index != 3 or schedule._permit_index != 2:
            raise AssertionError('actual complete original reset/copy path must use its explicit finite supplies')
        report.update(status='passed_new_cold68000_original_checksum_to_first3BC',
            confidence='confirmed_new_original_68000_cold_software_path_under_explicit_finite_schedule',
            first_wait=dict(poll=waiting.poll,frame=_frame_fields(waiting.frame),
                full_SR=state.sr,inactive_stack=point.inactive_stack.base,
                natural_request=state.read(0xFFFFF600,2),natural_phase=state.read(0xFFFFF612,2),
                software_suspensions=session.suspensions),
            cold_startup_38bytes_copied=True, cold_Z80_startup_executed=False,
            audio_reset_epoch=sound.reset_epoch,audio_control_phase=control.phase,
            audio_data_operations=audio.data_operations,PSG_CPU_writes=original_psg,
            PSG_clock_grants=0,actual_write_DMA_grants=write_events.consumed_grants,
            actual_wait_DMA_slots=video_events.consumed_slots,
            dual_CPU_cold_boot_success=False,
            limits=['original68000 cold checksum and startup0100 first wait only',
                    'short Z80 startup copied but never executed; no FM/audio startup success',
                    'no IRQ/title/menu/map frames and no relative hardware-cycle equivalence'])
    except BaseException as error:
        report.update(status='preserved_new_cold68000_checksum_boundary',boundary=str(error),
            traceback=traceback.format_exc())
        raise
    finally:
        if state is not None:
            report['Scene_reads'] = state.reads
            report['Scene_event_count'] = len(state.events)
            report['last_events'] = state.events[-20:]
            report['selected_actual_device_events'] = [event for event in state.events
                if event[0] in ('bootstrap_USP','external_dma_slot','external_write_dma_grant')]
        if control is not None:
            report['audio_control_events'] = control.events
        if sound is not None:
            report['last_audio_reset_epoch'] = sound.reset_epoch
        if psg is not None:
            report['PSG_device_events'] = [asdict(event) for event in psg.events]
        _write_json(output/'receipt.json',report)
        print(json.dumps(dict(status=report['status'],output=str(output),
            boundary=report.get('boundary'),Scene_reads=report.get('Scene_reads'),
            host_checksum_calculated=False,dual_CPU_cold_boot_success=False),ensure_ascii=False))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root',type=Path,required=True)
    parser.add_argument('--sound-native-root',type=Path,required=True)
    parser.add_argument('--sources',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    run(args.project_root,args.sound_native_root,args.sources,args.output)
