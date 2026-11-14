"""Generate explicit finite hardware supplies before a normal application run.

This is a JSON producer, not an application constructor or timing oracle. It
preserves the supplied complete profile's cold/device initial state and all
clocks. Only declared finite capacities and a disclosed experimental R sequence
are expanded; no running supplier is refilled or game RAM written.
"""
from copy import deepcopy
from dataclasses import dataclass, asdict, fields
import json


FORMAT = 'g5510-finite-application-hardware-capacities-v1'
PROFILE_FORMAT = 'g5510-unified-cold-driver-finite-inputs-v1'
MAX_PROFILE_BYTES = 4_000_000


@dataclass(frozen=True)
class HardwareCapacityPlan:
    max_frames: int
    refresh_observations: int
    refresh_value_start: int
    refresh_value_step: int
    future_bus_permits: int
    future_dma_slots: int
    future_dma_units_per_slot: int
    video_edge_pairs: int
    scene_max_reads: int
    audio_max_data_operations: int
    driver_progressive_permits: int
    fm_busy_permits: int
    max_materialized_items: int
    max_output_bytes: int

    @classmethod
    def from_dict(cls, document):
        names = {item.name for item in fields(cls)}
        if (type(document) is not dict or set(document) != names | {'format'}
                or document['format'] != FORMAT):
            raise ValueError('complete explicit finite hardware-capacity plan required')
        result = cls(**{name: document[name] for name in names})
        result.validate()
        return result

    def validate(self):
        for item in fields(self):
            value = getattr(self, item.name)
            minimum = 0 if item.name == 'refresh_value_start' else 1
            if type(value) is not int or value < minimum:
                raise ValueError('explicit in-range finite integer required: ' + item.name)
        if not 0 <= self.refresh_value_start <= 255 or not 1 <= self.refresh_value_step <= 255:
            raise ValueError('explicit BYTE start/step required for the experimental R sequence')
        if self.future_dma_units_per_slot > 65536:
            raise ValueError('VDP progress grant cannot exceed65536 transfer units')
        if not 1024 <= self.max_output_bytes <= MAX_PROFILE_BYTES:
            raise ValueError('explicit output bound must be1024..4000000 bytes')
        if self.max_materialized_items > 1_000_000:
            raise ValueError('finite materialization reserve cannot exceed one million items')
        count = (self.refresh_observations + self.future_bus_permits
            + self.future_dma_slots + 2 * self.video_edge_pairs)
        if count > self.max_materialized_items:
            raise ValueError('declared finite arrays exceed the explicit materialization reserve')
        return self


def _json_bytes(value):
    """Compact JSON keeps finite scalar supplies small without encoded blobs."""
    return (json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def _edge_template(profile):
    edges = profile['live_extension']['video_edges']
    if type(edges) is not list or len(edges) < 2 or len(edges) % 2:
        raise ValueError('the explicit baseline must contain complete VBlank edge pairs')
    pair = edges[:2]
    if any(row != pair[index % 2] for index, row in enumerate(edges)):
        raise ValueError('nonrepeating baseline edges cannot be silently expanded')
    for row, reason in zip(pair, ('vblank-end', 'vblank-start')):
        if (type(row) is not dict or set(row) != {'reason', 'bus_state'}
                or row['reason'] != reason or type(row['bus_state']) is not dict
                or set(row['bus_state']) != {'status_without_dma', 'hv', 'open_bus'}):
            raise ValueError('complete explicitly ordered existing edge snapshots required')
    return pair


def make_hardware_fields(baseline, capacity: HardwareCapacityPlan, *, source_profile: str):
    """Return new whole input fields; never execute their software/device owners.

    Cold RESET pulses, original-prefix DMA/BUS supplies, control/register/RAM
    initial values, clock frequencies, BUSY quantum and startup IM1 timestamps
    remain the baseline's exact values. Capacities are not elapsed time or
    guaranteed gameplay coverage. Exhaustion remains a real runtime boundary.
    """
    if type(capacity) is not HardwareCapacityPlan:
        raise ValueError('one exact explicit HardwareCapacityPlan required')
    capacity.validate()
    if (type(baseline) is not dict or baseline.get('format') != PROFILE_FORMAT
            or baseline.get('experimental_inputs_not_hardware_reset_defaults') is not True
            or type(source_profile) is not str or not source_profile):
        raise ValueError('one complete disclosed experimental baseline profile required')
    pair = _edge_template(baseline)
    if (baseline['live_extension'].get('format') != 'g5510-live-cold-driver-extension-v1'
            or baseline['live_extension'].get('main_loop_points') is not True
            or baseline['live_extension'].get('timer_b_continuation') is not True
            or baseline['providers']['memory_BIT'] != 'indexed_EA_high_XY_only_nonindexed_boundary'):
        raise ValueError('the actual finite live driver/condition-provider interface changed')
    # Reserve before allocating any expanded list. This conservatively counts
    # the complete old JSON too, despite replacing rather than copying arrays.
    predicted = (len(_json_bytes(baseline)) + 16 * capacity.refresh_observations
        + 6 * capacity.future_bus_permits + 7 * capacity.future_dma_slots
        + capacity.video_edge_pairs * len(_json_bytes(pair)) + 8192)
    if predicted > capacity.max_output_bytes:
        raise ValueError('conservative profile-size reservation exceeds the explicit output cap')

    small = dict(baseline)
    small.pop('application_profile', None)
    small['providers'] = {key: value for key, value in baseline['providers'].items()
        if key != 'refresh_observations'}
    replaced = {'future_DMA_units', 'future_bus_transfer_permits', 'video_edges'}
    small['live_extension'] = {key: value for key, value in baseline['live_extension'].items()
        if key not in replaced}
    result = deepcopy(small)
    result['main']['max_reads'] = capacity.scene_max_reads
    result['sound']['max_DATA_operations'] = capacity.audio_max_data_operations
    result['transfers']['driver'] = capacity.driver_progressive_permits
    result['clocks']['fm_busy_permits'] = capacity.fm_busy_permits
    result['providers']['refresh_observations'] = [
        {'value': (capacity.refresh_value_start + capacity.refresh_value_step * index) & 255}
        for index in range(capacity.refresh_observations)]
    extension = result['live_extension']
    extension.pop('future_experiment_not_executed_by_factory', None)
    extension['future_bus_transfer_permits'] = [True] * capacity.future_bus_permits
    extension['future_DMA_units'] = [capacity.future_dma_units_per_slot] * capacity.future_dma_slots
    extension['video_edges'] = [deepcopy(row) for unused in range(capacity.video_edge_pairs) for row in pair]
    result['application_profile'] = dict(
        format='g5510-reviewed-finite-application-hardware-v2',
        confidence='explicit_experimental_supplies_not_runtime_or_timing_acceptance',
        source_profile=source_profile, declared_max_frames=capacity.max_frames,
        capacities=asdict(capacity), materialized_items=(capacity.refresh_observations
            + capacity.future_bus_permits + capacity.future_dma_slots + 2 * capacity.video_edge_pairs),
        conservative_JSON_byte_reservation=predicted,
        cold_RESET_and_prefix_supplies_unchanged=True,
        clock_frequencies_busy_quantum_startup_IM1_unchanged=True,
        live_physical_pad_changes_owned_by_frontend=True,
        scripted_buttons_or_menu_results=False,
        R_observations='explicit (start+step*ordinal)&255; probable XY/actual IFF2, not measured M1 history',
        nonindexed_BIT_policy='scoped mailbox ADD/BIT and rhythm JP/JR/RET WZ owners; other sites remain unbound',
        automatic_refill=False, capacities_are_not_time_or_guaranteed_gameplay_coverage=True,
        original_ROM_or_host_seed_phase_money_writes=False,
        complete_game_or_audible_acceptance_claimed=False)
    if len(_json_bytes(result)) > capacity.max_output_bytes:
        raise ValueError('complete resulting JSON exceeds the explicit output cap')
    return result


def main(argv=None):
    """Publish one new normal JSON input, without loading configuration/game."""
    import argparse
    from pathlib import Path
    from .config import _no_duplicate_keys
    from ..high_level_rom.native import fresh_output

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--base-hardware', type=Path, required=True)
    parser.add_argument('--capacity-plan', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    project = args.project_root.resolve(strict=True)
    output = fresh_output(args.output)
    if (not project.is_dir() or not output.is_relative_to(project / 'build')
            or output == project / 'build' or not output.parent.is_dir() or output.suffix != '.json'):
        raise ValueError('one absent project/build JSON with existing parent required')

    def read_json(path, maximum):
        with path.open('rb') as stream:
            raw = stream.read(maximum + 1)
        if len(raw) > maximum:
            raise ValueError('explicit input JSON size bound exceeded: ' + str(path))
        return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_no_duplicate_keys)

    capacity = HardwareCapacityPlan.from_dict(read_json(args.capacity_plan, 65536))
    baseline = read_json(args.base_hardware, capacity.max_output_bytes)
    document = make_hardware_fields(baseline, capacity, source_profile=str(args.base_hardware))
    encoded = _json_bytes(document)
    with output.open('xb') as destination:
        destination.write(encoded)
    print(json.dumps(dict(output=str(output), bytes=len(encoded),
        declared_frames=capacity.max_frames, finite_supply_source_generated=True,
        application_started=False, game_or_timing_acceptance=False), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
