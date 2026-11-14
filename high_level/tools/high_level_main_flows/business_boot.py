"""Original platform reset, checksum gate, and asynchronous main state loop.

Resources are external views. Processor bootstrap transitions are explicit
ports, and no infinite hardware loop is shortened to a successful return.
"""
from .domain import (SceneState, Cursor, Long, uint, checked_state, u8, u16,
                     u32, s16, replace_byte, replace_word, low16, swap_words,
                     negative_long, descending_inclusive, data_view, ram_view)
from .contexts_boot import ResetProfile, BootstrapOutcome
from .contexts_main import SceneTick
from .services import call_target, initialize_video_registers_and_planes


def _ram(state, address):
    return ram_view(state, 'ram_%04x' % address)


def _checksum_failed(state):
    from .contexts_display_fields import display_legacy_frame_fields
    return display_legacy_frame_fields(state, None, 1224)


def reset_console(state: SceneState, profile: ResetProfile):
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from .contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, profile, 518)
    return reset_console_frame_fields(state, entered)


def start_game_main_loop(state: SceneState, profile: ResetProfile):
    """Historical convenience API projects the sole complete core; absent D/A/CCR-X/SP remain a true boundary."""
    from .contexts_display_fields import display_legacy_frame_fields
    entered = display_legacy_frame_fields(state, profile, 768)
    return start_game_main_loop_frame_fields(state, entered)


# C59 complete display/order ABI; historical algorithms are projections only.

from .domain import low8

from .contexts_gameplay import FirstDeploymentFrame, first_replace
"""Complete original reset/checksum/main-loop fields, never finite credit.

The separate existing BootstrapControl owns USP. Physical VDP, sound-bus
polls and the endless main loop remain real boundaries/waits; no handshake
is synthesized and no outer RTS is invented for this nonreturning owner.
"""
from .contexts_gameplay import FirstDeploymentFrame, first_replace, MovementContinuationBoundary
from .contexts_display_fields import (
    display_frame_fields, display_move_fields, display_store_fields,
    display_address_fields, display_loop_fields, display_call_fields,
    display_status_fields,
)


def _bootstrap_checksum_failed_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4C8 actual video fill and4E6 infinite BRA, not a successful return."""
    frame = display_call_fields(state, frame, 0x6826, 0x4CE)
    frame = display_store_fields(state, frame, 0x4CE, 0xC00004, 0xC0000000, 4)
    frame = display_move_fields(state, frame, 'choice', 0x3F, 32)
    while True:
        frame = display_store_fields(state, frame, 0x4DA, 0xC00000, 0xE)
        frame, more = display_loop_fields(frame, 'choice')
        if not more:
            break
    while True:
        state.progress('original4E6 fatal cartridge checksum loop')


def _bootstrap_checksum_extent_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """ASR.L1 extends sign after the existing shift owns original X/C."""
    from ..high_level_remaining_flows.business_city import _recruitment_right_long
    original = frame.target_x
    frame = _recruitment_right_long(state, frame, 'target_x', 1)
    value = frame.target_x | (original & 0x80000000)
    status = (frame.status & 17) | (8 if value & 0x80000000 else 0) | (4 if value == 0 else 0)
    state.sr = (state.sr & 65504) | status
    return first_replace(frame, target_x=value, status=status)


def reset_console_frame_fields(state: SceneState, frame: FirstDeploymentFrame,
        profile: ResetProfile | None = None) -> FirstDeploymentFrame:
    """206→300, retaining all real bootstrap MOVEM and device effects."""
    from .business_movement_support import (
        _movement_test_long, _movement_test, _movement_add_word)
    from .business_map import _world_map_bit_fields
    frame = display_frame_fields(state, frame)
    frame = _movement_test_long(state, frame, state.read(0xA10008, 4))
    if frame.status & 4:
        frame = _movement_test(state, frame, state.read(0xA1000C, 2), 16)
    if not frame.status & 4:
        return start_game_main_loop_frame_fields(state, frame)
    frame = display_address_fields(state, frame, 'scratch', 0x294)
    for name in ('offset_x', 'offset_y', 'choice'):
        value = u32(s16(frame.scratch.word()))
        frame = first_replace(frame, **{name: value}, scratch=frame.scratch.advance(2))
    for name in ('roster', 'candidates', 'controller', 'scan', 'opponent'):
        value = frame.scratch.long()
        frame = first_replace(frame, scratch=frame.scratch.advance(4))
        frame = display_address_fields(state, frame, name, value)
    frame = display_move_fields(state, frame, 'target_x',
        state.read(u32(frame.candidates.base - 0x10FF), 1), 8)
    frame = display_move_fields(state, frame, 'target_x', low8(frame.target_x) & 0xF, 8)
    if not frame.status & 4:
        frame = display_store_fields(state, frame, 0x22C,
            u32(frame.candidates.base + 0x2F00), 0x53454741, 4)
    frame = display_move_fields(state, frame, 'target_x', frame.opponent.word())
    frame = display_move_fields(state, frame, 'target_x', 0, 32)
    frame = display_address_fields(state, frame, 'auxiliary', frame.target_x)
    if type(profile) is not ResetProfile:
        raise MovementContinuationBoundary(0x23A, frame,
            'original MOVE A6,USP requires the existing explicit BootstrapControl')
    profile.validate(state)
    profile.processor.set_user_stack(state, frame.auxiliary.base)
    frame = display_move_fields(state, frame, 'target_y', 0x17, 32)
    while True:
        value = frame.scratch.byte()
        frame = first_replace(frame, scratch=frame.scratch.advance(1))
        frame = display_move_fields(state, frame, 'offset_x', value, 8)
        frame = display_store_fields(state, frame, 0x240,
            frame.opponent.base, low16(frame.offset_x))
        frame = _movement_add_word(state, frame, 'offset_x', low16(frame.choice))
        frame, more = display_loop_fields(frame, 'target_y')
        if not more:
            break
    value = frame.scratch.long()
    frame = first_replace(frame, scratch=frame.scratch.advance(4))
    frame = display_store_fields(state, frame, 0x248, frame.opponent.base, value, 4)
    frame = display_store_fields(state, frame, 0x24A, frame.scan.base, low16(frame.target_x))
    frame = display_store_fields(state, frame, 0x24C, frame.candidates.base, low16(frame.choice))
    frame = display_store_fields(state, frame, 0x24E, frame.controller.base, low16(frame.choice))
    while True:
        frame = _world_map_bit_fields(state, frame, frame.candidates.byte(), frame.target_x & 7)
        if frame.status & 4:
            break
        state.progress('original250 sound bus request bit0')
    frame = display_move_fields(state, frame, 'unit', 0x25, 32)
    while True:
        value = frame.scratch.byte()
        frame = first_replace(frame, scratch=frame.scratch.advance(1))
        frame = display_store_fields(state, frame, 0x256, frame.roster.base, value, 1)
        frame = first_replace(frame, roster=frame.roster.advance(1))
        frame, more = display_loop_fields(frame, 'unit')
        if not more:
            break
    frame = display_store_fields(state, frame, 0x25C, frame.controller.base, low16(frame.target_x))
    frame = display_store_fields(state, frame, 0x25E, frame.candidates.base, low16(frame.target_x))
    frame = display_store_fields(state, frame, 0x260, frame.controller.base, low16(frame.choice))
    while True:
        frame = first_replace(frame, auxiliary=frame.auxiliary.advance(-4))
        frame = display_store_fields(state, frame, 0x262, frame.auxiliary.base, frame.target_x, 4)
        frame, more = display_loop_fields(frame, 'offset_y')
        if not more:
            break
    for pc in (0x268, 0x26A):
        value = frame.scratch.long()
        frame = first_replace(frame, scratch=frame.scratch.advance(4))
        frame = display_store_fields(state, frame, pc, frame.opponent.base, value, 4)
    frame = display_move_fields(state, frame, 'count', 0x1F, 32)
    while True:
        frame = display_store_fields(state, frame, 0x26E, frame.scan.base, frame.target_x, 4)
        frame, more = display_loop_fields(frame, 'count')
        if not more:
            break
    value = frame.scratch.long()
    frame = first_replace(frame, scratch=frame.scratch.advance(4))
    frame = display_store_fields(state, frame, 0x274, frame.opponent.base, value, 4)
    frame = display_move_fields(state, frame, 'distance', 0x13, 32)
    while True:
        frame = display_store_fields(state, frame, 0x278, frame.scan.base, frame.target_x, 4)
        frame, more = display_loop_fields(frame, 'distance')
        if not more:
            break
    frame = display_move_fields(state, frame, 'offset_x', 3, 32)
    while True:
        value = frame.scratch.byte()
        frame = first_replace(frame, scratch=frame.scratch.advance(1))
        frame = display_store_fields(state, frame, 0x280, u32(frame.scan.base + 17), value, 1)
        frame, more = display_loop_fields(frame, 'offset_x')
        if not more:
            break
    frame = display_store_fields(state, frame, 0x288, frame.controller.base, low16(frame.target_x))
    source = frame.auxiliary
    for name in ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x',
            'offset_y', 'choice', 'roster', 'candidates', 'controller', 'scan',
            'opponent', 'scratch', 'auxiliary'):
        value = source.long()
        source = source.advance(4)
        if name in ('roster', 'candidates', 'controller', 'scan', 'opponent', 'scratch', 'auxiliary'):
            frame = display_address_fields(state, frame, name, value)
        else:
            frame = first_replace(frame, **{name: value})
    frame = display_status_fields(state, frame, 0x2700)
    return start_game_main_loop_frame_fields(state, frame)


def start_game_main_loop_frame_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Whole original invocation, retaining its actual 003BC continuation."""
    from .bootstrap_steps import run_bootstrap_main_blocking_fields
    return run_bootstrap_main_blocking_fields(state, frame)
