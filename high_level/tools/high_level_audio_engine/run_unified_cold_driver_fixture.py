"""One new live cold206→cold38 idle→same reset→installed driverPC0→006F case.

Only public semantic owners execute. Every hardware observation/grant comes
from an explicit finite caller profile. No old fixture.run is called, no ROM,
host checksum, opcode interpreter, audio image installer or device replacement.
"""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
import traceback


def _json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def _source_epoch(project):
    names = (
        'tools/high_level_main_flows/business_boot.py',
        'tools/high_level_main_flows/bootstrap_reset.py',
        'tools/high_level_main_flows/bootstrap_steps.py',
        'tools/high_level_audio_engine/cold_workspace.py',
        'tools/high_level_audio_engine/driver_installation.py',
        'tools/high_level_audio_engine/platform_handoff.py',
        'tools/high_level_audio_engine/driver_startup.py',
        'tools/high_level_audio_engine/business_hardware.py',
        'tools/high_level_audio_engine/business_lifecycle_reset.py',
        'tools/high_level_audio_engine/business_lifecycle_loading.py',
    )
    result = []
    for name in names:
        info = (project/name).stat()
        result.append(dict(path=name, bytes=info.st_size, modified_ns=info.st_mtime_ns))
    return result


def _source_summary(source):
    evidence = source.evidence
    return dict(format=evidence['format'], confidence=evidence['confidence'],
        source_root=evidence['source_root'], resource_manifest=evidence['resource_manifest'],
        whole_cartridge=evidence['whole_cartridge'], original_checksum_body=evidence['original_checksum_body'],
        M68K=dict(authorities=len(evidence['m68k']['authorities']),
            instructions=evidence['m68k']['instructions'], CODE_bytes=evidence['m68k']['CODE_bytes'],
            current_source_and_object_instructions_match=True),
        Z80=evidence['z80'], registered_DATA=dict(packages=evidence['registered_DATA']['packages'],
            bytes=evidence['registered_DATA']['bytes']),
        native_rebuilds=0, hashes_computed=0, original_ROM_or_bank_input=False,
        full_per_authority_source_evidence_retained_on_live_source_object=True)


def run(project_root, sound_native_root, sources, audio_root, chip_library, inputs, output):
    project_root = project_root.resolve(strict=True)
    sound_native_root = sound_native_root.resolve(strict=True)
    sources, audio_root = sources.resolve(strict=True), audio_root.resolve(strict=True)
    chip_library, inputs = chip_library.resolve(strict=True), inputs.resolve(strict=True)
    if (output.exists() or not output.parent.is_dir()
            or not output.resolve().is_relative_to(project_root/'build')):
        raise ValueError('one fresh explicit workspace build output required')
    profile = json.loads(inputs.read_text(encoding='utf-8'))
    if (type(profile) is not dict
            or profile.get('format') != 'g5510-unified-cold-driver-finite-inputs-v1'
            or profile.get('experimental_inputs_not_hardware_reset_defaults') is not True):
        raise ValueError('complete explicit experimental finite input profile required')
    output.mkdir()
    sys.path.insert(0, str(project_root))

    from tools.high_level_audio_engine import target
    from tools.high_level_audio_engine.cold_workspace import ColdWorkspacePlatform, ColdWorkspaceCopyAuthority, ColdWorkspaceSession
    from tools.high_level_audio_engine.control_reset import AudioControlOwner, AudioControlState, FinitePulseSoundSchedule
    from tools.high_level_audio_engine.domain import AudioBoundary, AudioState, AlternateGroup, tested_bit_conditions, byte
    from tools.high_level_audio_engine.driver_installation import DriverInstallationCapture, DriverInstalledAuthority
    from tools.high_level_audio_engine.driver_startup import AudioDriverStartupSession, Im1ClockGrant
    from tools.high_level_audio_engine.hardware_scene import SharedSoundAudioBus, SoundDevice, SceneSoundHardwareBus
    from tools.high_level_audio_engine.hardware_scene_psg import ScenePsgHardwareBus
    from tools.high_level_audio_engine.owned_runtime import DriverFrame, ExplicitAudioPlatform, OwnedAudioDeviceBus, OwnedSoundMaterial, OWN_RESOURCE_IDS
    from tools.high_level_audio_engine.platform_handoff import handoff_expired_cold_platform
    from tools.high_level_audio_engine.psg_device import SegaPsgDevice, SegaPsgState
    from tools.high_level_audio_engine.ymfm_device import YmfmDevice
    from tools.high_level_input.hardware_controller import SceneControllerHardwareBus, ThreeButtonPad, PadButtons, DisconnectedPort
    from tools.high_level_main_flows.bootstrap_reset import PersistentColdResetSession, ResetAudioReleasePoint
    from tools.high_level_main_flows.bootstrap_stacks import BankedStackControl
    from tools.high_level_main_flows.bootstrap_steps import BootstrapMainWait
    from tools.high_level_main_flows.cartridge_source_data import load_cartridge_source_data, project_cartridge_m68k_authorities
    from tools.high_level_main_flows.contexts_boot import ResetProfile
    from tools.high_level_main_flows.contexts_gameplay import FirstDeploymentFrame
    from tools.high_level_main_flows.runtime import create_linked_scene_state
    from tools.high_level_main_flows.runtime_resources import load_scene_resources
    from tools.high_level_main_flows.services import LogicalServices
    from tools.high_level_scene_flows.domain import HardwareBus
    from tools.high_level_video.frame_interrupts import SuppliedVideoEvents, VideoBusState
    from tools.high_level_video.hardware_vdp import VdpMemory, VdpController, SceneVdpHardwareBus
    from tools.high_level_video.write_dma_events import SceneWriteDmaEvents, WriteDmaGrant
    # Pure bounded-result observers only, not old191.run or any old fixture.
    from tools.high_level_video.run_cold_bootstrap_fixture import _frame_fields, _actual_checksum_read_sequence

    state = sound = audio = control = reset = cold = startup = fm = psg = devices = None
    receipt = dict(status='running_only_new_unified_cold_driver_combination', stage='construct',
        new_formal_CODE_bytes=0, original_ROM_or_bank_input=False, native_rebuilds=0, hashes_computed=0,
        host_checksum_calculated=False, host_audio_RAM_clear=False, host_return_WORDs_pushed=0,
        old191_192_193_188_cases_replayed=False, music_or_title_or_map_executed=False,
        exact_CPU_relative_timing_or_full_game_boot_claimed=False)
    transfer_counts = dict(cold=0, driver=0)
    busy_grants = dict(used=0, chip_clocks=0)
    provider_counts = dict(refresh=0, indexed_BIT=0)
    invalidated_at_reset = []
    grant_phase = 'cold'
    try:
        receipt['source_epoch_before'] = _source_epoch(project_root)
        receipt['explicit_paths'] = dict(project_root=str(project_root), sound_native_root=str(sound_native_root),
            sources=str(sources), audio_root=str(audio_root), chip_library=str(chip_library), inputs=str(inputs))
        receipt['explicit_inputs'] = profile
        main_input, sound_input = profile['main'], profile['sound']
        clock_input, video_input = profile['clocks'], profile['video']
        provider_input, transfer_input = profile['providers'], profile['transfers']
        if sound_input['RAM_pattern'] != 'BYTE(i%255+1),8192':
            raise ValueError('this new case requires explicitly nonzero experimental initial sound RAM')
        if provider_input['memory_BIT'] != 'indexed_EA_high_XY_only_nonindexed_boundary':
            raise ValueError('explicit narrow indexed BIT conditions profile required')
        for value in (clock_input['fm_busy_quantum'], clock_input['fm_busy_permits']):
            if type(value) is not int or value <= 0:
                raise ValueError('finite positive externally supplied FM clock quantum/permit count required')
        if (type(clock_input['IM1_timestamps']) is not list or len(clock_input['IM1_timestamps']) != 3
                or clock_input['PSG_clock_grants'] != []):
            raise ValueError('exact three explicit IM1 times and no implicit PSG clocks required')
        if any(type(transfer_input[name]) is not int or transfer_input[name] < 1 for name in ('cold', 'driver')):
            raise ValueError('both progressive-copy phases require finite positive permit bounds')
        if len(main_input['D_LONGs']) != 8 or len(main_input['A0_A6_LONGs']) != 7:
            raise ValueError('all sixteen original68000 carriers must be supplied')

        logical_root = project_root/'tools/high_level_audio_engine'
        logical = {name:(logical_root/name).read_text(encoding='utf-8') for name in target.BUSINESS_MODULES}
        source = load_cartridge_source_data(project_root,
            m68k_authorities=project_cartridge_m68k_authorities(), sound_native_root=sound_native_root,
            sound_logical_sources=logical, resource_manifest=sources)
        bank = load_scene_resources(audio_root, OWN_RESOURCE_IDS)
        receipt['source_authority'] = _source_summary(source)
        receipt['owned_audio_bank'] = dict(root=str(audio_root), resource_ids=list(bank.resource_ids),
            encoded_DATA_bytes=bank.encoded_bytes, initial_bank_base=sound_input['bank_base'],
            installed_to_RAM_by_host=False, same_material_retained_through_entire_case=True)
        control = AudioControlOwner(AudioControlState(**sound_input['initial_control']), reset_asserted=False)

        def refresh(previous):
            # This is a finite caller observation, not an M1/CPU timing guess.
            ordinal = provider_counts['refresh']
            observations = provider_input['refresh_observations']
            if ordinal >= len(observations):
                raise AudioBoundary('explicit finite refresh/full-condition observations exhausted')
            value, conditions = observations[ordinal]['value'], observations[ordinal]['conditions']
            byte(previous); byte(value); byte(conditions)
            provider_counts['refresh'] += 1
            return value, conditions

        def indexed_bit(context):
            context.validate()
            if not context.indexed:
                raise AudioBoundary('unified case supplies no nonindexed memory BIT/WZ observation')
            provider_counts['indexed_BIT'] += 1
            return tested_bit_conditions(context.value, context.bit_index,
                context.previous_conditions, address_high=context.address >> 8)

        platform = ColdWorkspacePlatform(alternate_accumulator=sound_input['alternate_AF'],
            alternate_group=AlternateGroup(**sound_input['alternate_group']), refresh_reader=refresh,
            memory_bit_reader=indexed_bit, control_owner=control)

        def busy_clock(chip, observed):
            if observed & 0x80:
                if busy_grants['used'] >= clock_input['fm_busy_permits']:
                    raise AudioBoundary('explicit finite fixed-quantum FM BUSY clock grants exhausted')
                chip.advance(clock_input['fm_busy_quantum'])
                busy_grants['used'] += 1
                busy_grants['chip_clocks'] += clock_input['fm_busy_quantum']

        fm = YmfmDevice(chip_library, clock_hz=clock_input['FM_clock_hz'],
            pcm_sink=None, after_status_read=busy_clock)
        psg_state = dict(sound_input['PSG_initial_state'])
        for name in ('tone_periods', 'attenuation', 'tone_counters', 'tone_outputs'):
            psg_state[name] = tuple(psg_state[name])
        psg = SegaPsgDevice(SegaPsgState(**psg_state), clock_hz=clock_input['PSG_clock_hz'],
            sample_rate_hz=clock_input['PSG_sample_rate_hz'],
            channel_gain=tuple(sound_input['PSG_channel_gain']), pcm_sink=None)

        def transfer(reason):
            if (reason != 'progressive-block-copy' or grant_phase not in transfer_counts
                    or transfer_counts[grant_phase] >= transfer_input[grant_phase]):
                raise AudioBoundary('explicit finite '+grant_phase+' progressive-copy permits exhausted/unbound')
            transfer_counts[grant_phase] += 1

        devices = OwnedAudioDeviceBus(OwnedSoundMaterial(bank.data, (), bank.resource_ids, bank.encoded_bytes),
            fm, bank_base=sound_input['bank_base'], psg_write=psg.write, transfer_boundary=transfer)
        audio = AudioState(SharedSoundAudioBus(bytearray((index%255)+1 for index in range(8192)), devices),
            platform, sound_input['max_DATA_operations'])

        class WitnessedFiniteReset(FinitePulseSoundSchedule):
            def reset_changed(self, device, asserted):
                super().reset_changed(device, asserted)
                if asserted and cold is not None and control.generation == cold.generation+1:
                    try:
                        cold.observe_idle()
                    except AudioBoundary as boundary:
                        invalidated_at_reset.append(dict(original_reset_store=0x288,
                            old_generation=cold.generation, current_generation=control.generation,
                            reset_epoch=device.reset_epoch, actual_boundary=str(boundary),
                            claim_cleared_by_actual_RESET=control._frame_session is None))
                    else:
                        raise AssertionError('real288 RESET must invalidate the actual cold idle claim')

        schedule_input = profile['reset_and_bus']
        open_bus = schedule_input['BUSACK_open_bus_value']
        schedule = WitnessedFiniteReset(control, reset_pulse_clocks=tuple(schedule_input['reset_pulse_clocks']),
            bus_transfer_permits=tuple(schedule_input['bus_transfer_permits']),
            open_bus_reader=lambda address,size: open_bus)
        sound = SoundDevice(audio, schedule, reset_asserted=False, bus_requested=False, m68k_granted=False)
        control.bind(sound)
        memory = VdpMemory(bytearray([video_input['initial_memory_fill']])*65536,
            bytearray([video_input['initial_memory_fill']])*128,
            bytearray([video_input['initial_memory_fill']])*80,
            bytearray([video_input['initial_memory_fill']])*32)
        video_events = SuppliedVideoEvents(VideoBusState(video_input['status_without_dma'],
            video_input['hv'], video_input['open_bus']), tuple(video_input['wait_DMA_units']), cpu_dma_stalls=True)
        vdp = VdpController(memory, status=video_events)
        video = SceneVdpHardwareBus(vdp, HardwareBus(), replace_vdp_mapping=True)
        inputs_bus = SceneControllerHardwareBus(bytearray(main_input['GPIO']),
            (ThreeButtonPad(PadButtons()), ThreeButtonPad(PadButtons()), DisconnectedPort()),
            video, replace_controller_mapping=True)
        sound_bus = SceneSoundHardwareBus(sound, inputs_bus, replace_sound_mapping=True)
        write_events = SceneWriteDmaEvents(sound_bus, vdp,
            tuple(WriteDmaGrant(**row) for row in video_input['write_DMA_grants']))
        hardware = ScenePsgHardwareBus(psg, write_events, replace_psg_mapping=True)
        state = create_linked_scene_state(bytearray([main_input['initial_RAM_fill']])*65536,
            data=source.data, hardware=hardware, services=LogicalServices(()),
            max_reads=main_input['max_reads'], max_samples=8, sr=main_input['SR'])
        video.bind_scene(state); sound_bus.bind_scene(state); video_events.bind_scene(state, vdp)
        write_events.bind_scene(state); hardware.bind_scene(state)
        incoming = FirstDeploymentFrame(*main_input['D_LONGs'],
            *(state.table_at(address).cursor() for address in main_input['A0_A6_LONGs']),
            state.table_at(main_input['A7']).cursor(), main_input['CCR_X'])
        stacks = BankedStackControl(state, user_stack=main_input['USP'], supervisor_stack=main_input['A7'])
        reset_profile = ResetProfile(stacks, state.table_at(main_input['boot_table']).cursor(), incoming.choice)
        identities = (state, sound, audio, audio.bus, sound.ram, devices, fm, psg, devices.material, control)
        reset = PersistentColdResetSession(state, incoming, reset_profile)
        receipt['stage'] = 'original_reset206_to_release262'
        release = reset.start()
        if type(release) is not ResetAudioReleasePoint or release.pc != 0x262:
            raise AssertionError('complete original206 must suspend only after260 before262')
        suspended_SR, suspended_events, suspended_frame = state.sr, len(state.events), release.frame
        receipt['stage'] = 'actual_cold_workspace_PC0_to_self_modified_idle'
        authority = ColdWorkspaceCopyAuthority(sound, control, DriverFrame(**sound_input['cold_entry_frame']), source.data)
        cold_lease = control.acquire_frame('startup', 0, authority=authority)
        cold = ColdWorkspaceSession(sound, control, cold_lease)
        idle = cold.start()
        if (idle.pc != 0 or idle.frame != DriverFrame(0,0,0,0,0,0,0,0) or sound.ram[0] != 0xE9
                or audio.data_operations != 16326 or transfer_counts['cold'] != 8153
                or control._frame_session is not cold or release.frame is not suspended_frame
                or state.sr != suspended_SR or len(state.events) != suspended_events):
            raise AssertionError('same-State real cold38 idle must preserve suspended68000 owner')
        if fm.events or fm.status_reads or fm.tick or psg.events:
            raise AssertionError('cold38 prefix must not invent any earlier chip execution')
        receipt['actual_cold_idle'] = dict(pc=idle.pc, frame=asdict(idle.frame), reset_epoch=idle.reset_epoch,
            generation=idle.generation, Audio_DATA_operations=audio.data_operations,
            progressive_transfers=transfer_counts['cold'], actual_RAM0=sound.ram[0],
            actual_copy_authority=authority.evidence, startup_claim_retained=True,
            actual68000_release_PC=release.pc, suspended_frame=_frame_fields(release.frame),
            suspended_full_SR=suspended_SR)
        receipt['stage'] = 'capture_installation_and_resume_same_reset262_checksum_to_first3BC'
        capture = DriverInstallationCapture(sound, control, source, reset_session=reset)
        waiting = reset.resume_release(release)
        if (type(waiting) is not BootstrapMainWait or waiting.poll != 0x3BC
                or waiting is not reset.main_session.waiting or reset.main_session.suspensions != 1):
            raise AssertionError('same persistent original reset/main first3BC required')
        installation = capture.finish(waiting)
        if len(invalidated_at_reset) != 1 or not invalidated_at_reset[0]['claim_cleared_by_actual_RESET']:
            raise AssertionError('actual288 must expire cold claim without a host clear/release')
        installation_evidence = dict(installation.evidence)
        installation_evidence.pop('source_provenance')
        installation_evidence['source_provenance_receipt_field'] = 'source_authority'
        receipt['actual_driver_installation'] = installation_evidence
        receipt['actual288_expired_cold_idle'] = invalidated_at_reset
        receipt['actual_checksum'] = _actual_checksum_read_sequence(state.events)
        receipt['first68000_main_wait'] = dict(poll=waiting.poll, frame=_frame_fields(waiting.frame),
            full_SR=state.sr, suspensions=reset.main_session.suspensions,
            F612=state.read(0xFFFFF612, 2), F600=state.read(0xFFFFF600, 2))
        if (receipt['first68000_main_wait']['F612'] != 0x100
                or receipt['first68000_main_wait']['F600'] != 0):
            raise AssertionError('actual original300 must naturally select0100 without a host phase write')
        write_events.require_consumed()
        if video_events.dma_slots or video_events.consumed_slots != len(video_input['wait_DMA_units']):
            raise AssertionError('only explicit finite VDP grants may complete original fill/copy')
        receipt['stage'] = 'exact_same_AudioState_platform_handoff_and_fresh_driver_authority'
        handoff = handoff_expired_cold_platform(sound, control, expired_cold_session=cold,
            installation=installation, refresh_reader=refresh, memory_bit_reader=indexed_bit)
        handoff.require_attached(sound, control)
        receipt['actual_platform_handoff'] = handoff.describe()
        entry_frame = DriverFrame(**sound_input['future_driver_entry_frame'])
        driver_authority = DriverInstalledAuthority(installation, entry_frame)
        driver_lease = control.acquire_frame('driver', 0, authority=driver_authority)
        if type(audio.platform) is not ExplicitAudioPlatform or audio.data_operations != 16326:
            raise AssertionError('fresh actual driver lease must precede any driver DATA execution')
        receipt['driver_entry'] = dict(kind=driver_lease.entry_kind, fresh_frame=asdict(entry_frame),
            reset_epoch=driver_lease.reset_epoch, generation=driver_lease.generation,
            Audio_DATA_operations_before_PC0=audio.data_operations,
            cold_lease_reused=False, installer_called=False)
        grant_phase = 'driver'
        receipt['stage'] = 'actual_driver_PC0_three_explicit_IM1_to006F'
        startup = AudioDriverStartupSession(sound, control, driver_lease,
            irq_clock_hz=clock_input['IM1_clock_hz'], initial_irq_clock=clock_input['IM1_initial_timestamp'])
        point = startup.start()
        if point.pc != 0x5F or point.frame.sample != 3 or sound.ram[0x1FFF] != 3:
            raise AssertionError('actual fresh driver PC0 must enter its own real three-count wait')
        snapshots = []
        for timestamp in clock_input['IM1_timestamps']:
            point = startup.deliver_im1(Im1ClockGrant(timestamp, clock_input['IM1_clock_hz']))
            snapshots.append(dict(timestamp=timestamp, pc=point.pc, frame=asdict(point.frame),
                actual_1FFF=sound.ram[0x1FFF]))
        if ([item['actual_1FFF'] for item in snapshots] != [2,1,0] or point.pc != 0x6F
                or point.kind != 'main-loop-boundary' or control.require_frame(startup.ready_lease) != point.frame):
            raise AssertionError('three real IM1/return transactions must naturally reach actual006F')
        handoff.require_attached(sound, control)
        current = (sound.scene, sound, sound.audio_state, sound.audio_state.bus, sound.ram,
            audio.bus.devices, devices.fm, devices.psg_write.__self__, devices.material, control)
        if any(first is not last for first,last in zip(identities,current)):
            raise AssertionError('cold→driver must retain all original Scene/RAM/chip/material/control owners')
        if ([item.value for item in psg.events[:4]] != [0x9F,0xBF,0xDF,0xFF]
                or psg.tick != 0 or not fm.events or not psg.events):
            raise AssertionError('same actual PSG must receive original reset mutes and real driver writes')
        if (schedule._pulse_index != len(schedule_input['reset_pulse_clocks'])
                or schedule._permit_index != len(schedule_input['bus_transfer_permits'])):
            raise AssertionError('all consumed reset/bus events must match declared finite profile')
        receipt.update(status='passed_new_sameScene_cold38_actual_reset_install_handoff_driver_three_IM1_006F',
            stage='checkpoint_actual006F_before_006F_EI_mailbox',
            confidence='confirmed_one_continuous_semantic_cold_to_initialized_driver_path_under_explicit_external_schedule',
            same_Scene_AudioState_shared_RAM_FM_PSG_bank_material_control_from_cold=True,
            full_reset_invocations=1, cold_workspace_invocations=1, driver_PC0_invocations=1,
            reset_source_contract=reset.source_contract, reset_session_events=reset.events,
            actual_IM1_events=[event for event in startup.events if event[0]=='actual_IM1'],
            IM1_snapshots=snapshots, actual_driver_PC=point.pc, actual_driver_frame=asdict(point.frame),
            final_audio_control=asdict(control.control), final_control_phase=control.phase,
            reset_epoch=sound.reset_epoch, generation=control.generation,
            original_main_still_suspended_at_same_first3BC=reset.main_session.waiting is waiting,
            continuous_music_or_006F_mailbox_execution=False,
            limits=['This executes both original cold38 and fresh installed driver PC0 on the same live state.',
                    '68000 remains at its true first3BC; no IRQ/title/menu/map path is entered.',
                    'Three IM1 grants and FM busy clock grants are separate external experiment inputs.',
                    '006F is a typed boundary before its EI/mailbox body, not music or full-game boot.',
                    'YMFM may generate discarded initialization frames; no PCM/WAV or music proof is claimed.',
                    'This is not an exact CPU instruction-cycle/refresh or analog hardware equivalence proof.'])
    except BaseException as error:
        receipt.update(status='preserved_only_new_unified_cold_driver_boundary', boundary=str(error),
            traceback=traceback.format_exc())
        raise
    finally:
        receipt['finite_transfer_permits_used'] = transfer_counts
        receipt['finite_FM_busy_grants'] = busy_grants
        receipt['explicit_read_providers_used'] = provider_counts
        receipt['source_epoch_after'] = _source_epoch(project_root)
        if state is not None:
            receipt.update(Scene_reads=state.reads, Scene_event_count=len(state.events), last_Scene_events=state.events[-12:])
        if audio is not None:
            receipt['Audio_DATA_operations'] = audio.data_operations
        if control is not None:
            receipt['actual_control_events'] = control.events
            receipt['last_control_phase'] = control.phase
        if startup is not None:
            receipt['startup_session_events'] = startup.events
            if not startup.closed:
                startup.close()  # Close the fixture-owned continuation, never run006F onward.
        if fm is not None:
            receipt['actual_YMFM'] = dict(clock=fm.tick, busy_until=fm.busy_until, timer_flags=fm.timer_flags,
                status_reads=len(fm.status_reads), events=len(fm.events),
                register_writes=sum(event[0]=='register' for event in fm.events),
                generated_initialization_frames=fm.generated_frames, PCM_sink='explicitly_discarded_no_WAV',
                last_events=fm.events[-8:])
            fm.close()
        if psg is not None:
            receipt['actual_same_PSG'] = dict(clock=psg.tick, writes=len(psg.events),
                first_four_writes=[asdict(event) for event in psg.events[:4]],
                generated_samples=psg.generated_samples, PCM_sink='explicitly_discarded_no_WAV')
        if devices is not None:
            receipt['actual_owned_bank'] = dict(final_base=devices.bank_base, serial_writes=len(devices.bank_writes),
                DATA_reads=len(devices.bank_reads), last_reads=devices.bank_reads[-6:])
        _json(output/'receipt.json', receipt)
        print(json.dumps(dict(status=receipt['status'], stage=receipt['stage'], output=str(output),
            boundary=receipt.get('boundary'), Scene_reads=receipt.get('Scene_reads'),
            Audio_DATA_operations=receipt.get('Audio_DATA_operations'), driver_PC=receipt.get('actual_driver_PC'),
            old_cases_replayed=False, music_proved=False), ensure_ascii=False))
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('project-root', 'sound-native-root', 'sources', 'audio-root', 'chip-library', 'inputs', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    run(args.project_root, args.sound_native_root, args.sources, args.audio_root,
        args.chip_library, args.inputs, args.output)


if __name__ == '__main__':
    main()
