"""Complete budget/recruitment carriers over the existing real memory ports.

confirmed: D0..D7/A0..A7 are supplied LONGs, not reconstructed zero registers.
The memory port delegates the already sealed DecimalMemory Game/Scene pair;
neither old checked_state nor either independent RAM model is widened.
"""
from dataclasses import dataclass, replace
from .domain import uint, u16, u32, s16, Boundary
from .contexts_numeric import DecimalMemory


@dataclass(frozen=True)
class CommandFrame:
    data: tuple
    addresses: tuple
    status_word: int

    def __post_init__(self):
        if type(self.data) is not tuple or type(self.addresses) is not tuple:
            raise ValueError('eight actual immutable data/address carriers required')
        if len(self.data) != 8 or len(self.addresses) != 8:
            raise ValueError('complete D0..D7/A0..A7 required')
        for value in self.data + self.addresses:
            uint(value, 32)
        uint(self.status_word, 16)

    def with_data(self, index, value, width=32):
        if type(index) is not int or not 0 <= index <= 7 or width not in (8,16,32):
            raise ValueError('actual data carrier width required')
        mask = (1 << width) - 1
        uint(value, width)
        values = list(self.data)
        values[index] = (values[index] & (0xFFFFFFFF ^ mask)) | value
        return replace(self, data=tuple(values))

    def with_address(self, index, address):
        if type(index) is not int or not 0 <= index <= 7:
            raise ValueError('actual address carrier required')
        values = list(self.addresses)
        values[index] = u32(address)
        return replace(self, addresses=tuple(values))


@dataclass(frozen=True)
class CommandBitObservation:
    zero: bool


class CommandMenuMemory:
    """No copied DATA: only the existing exact typed decimal memory port."""
    def __init__(self, state):
        self.decimal = DecimalMemory(state)
        self.state = self.decimal.state

    def cursor_at(self, address):
        from .domain import GameState
        if type(self.state) is GameState:
            return self.state.table(u32(address)).cursor()
        return self.state.table_at(u32(address)).cursor()

    def enter(self, frame):
        if type(self) is not CommandMenuMemory or type(frame) is not CommandFrame:
            raise ValueError('actual complete command entry fields required')
        self.state.sr = frame.status_word
        return frame

    def first_fields(self, frame):
        from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
        return FirstDeploymentFrame(*frame.data,
            *(self.cursor_at(address) for address in frame.addresses),
            frame.status_word & 31)

    def from_first(self, frame):
        from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
        from .domain import GameState, checked_table as checked_command_table
        from ..high_level_scene_flows.domain import checked_table as checked_scene_table
        if type(frame) is not FirstDeploymentFrame:
            raise ValueError('actual complete named child fields required')
        names = ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')
        views = (frame.roster,frame.candidates,frame.controller,frame.scan,
            frame.opponent,frame.scratch,frame.auxiliary,frame.stack_cursor)
        table_check = checked_command_table if type(self.state) is GameState else checked_scene_table
        for view in views:
            table_check(view, self.state)
        self.decimal.check_cursor(frame.stack_cursor)
        uint(frame.status,8)
        if frame.status > 31:
            raise ValueError('actual low-five-bit CCR required')
        self.state.sr = (self.state.sr & 0xFFE0) | frame.status
        return CommandFrame(tuple(frame.carrier(name) for name in names),
            tuple(view.base for view in views),self.state.sr)

    def stop(self, frame, target, reason):
        from ..high_level_scene_flows.domain import SceneState
        if type(self.state) is SceneState:
            from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
            raise MovementContinuationBoundary(target,self.first_fields(frame),reason)
        raise Boundary(reason + ' at ' + hex(target))


def _command_test_fields(memory, frame, value, width):
    from ..high_level_main_flows.business_movement_support import _movement_test, _movement_test_long
    actual = memory.first_fields(frame)
    if width == 32:
        actual = _movement_test_long(memory.state,actual,value)
    else:
        actual = _movement_test(memory.state,actual,value,width)
    return memory.from_first(actual)


def _command_load_fields(memory, frame, index, value, width):
    from ..high_level_main_flows.business_movement_support import _movement_move, _movement_move_long
    names = ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')
    actual = memory.first_fields(frame)
    if width == 32:
        actual = _movement_move_long(memory.state,actual,names[index],value)
    else:
        actual = _movement_move(memory.state,actual,names[index],value,width)
    return memory.from_first(actual)


def _command_binary_fields(memory, frame, destination, source, width, subtract=False, compare=False):
    from ..high_level_main_flows.business_movement_support import _movement_binary_flags
    previous_x = frame.status_word & 16
    actual, result = _movement_binary_flags(memory.state,memory.first_fields(frame),
        destination,source,width,subtract)
    if compare:
        memory.state.sr = (memory.state.sr & 0xFFEF) | previous_x
        actual = replace(actual,status=memory.state.sr & 31)
    return replace(memory.from_first(actual),status_word=memory.state.sr), result


def _command_store_fields(memory, frame, address, value, width, clear=False):
    uint(value,width)
    if clear:
        memory.state.read(u32(address),width//8)
    memory.state.write(u32(address),width//8,value)
    return _command_test_fields(memory,frame,value,width)


def _command_shift_fields(memory, frame, index, amount, width, right=False):
    from ..high_level_main_flows.business_movement_support import _movement_fixed_shift_word, _movement_shift_long
    names = ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')
    actual = memory.first_fields(frame)
    if width == 16:
        actual = _movement_fixed_shift_word(memory.state,actual,names[index],amount,right)
    elif width == 32 and amount == 8:
        actual = _movement_shift_long(memory.state,actual,names[index],right)
    else:
        raise ValueError('only the original closed command shifts required')
    return memory.from_first(actual)


def _command_product_fields(memory, frame, index, source):
    from ..high_level_main_flows.business_movement_support import _movement_multiply_word
    names = ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')
    return memory.from_first(_movement_multiply_word(memory.state,
        memory.first_fields(frame),names[index],source))


def _command_quotient_fields(memory, frame, index, divisor, instruction):
    from ..high_level_main_flows.business_movement_support import _movement_divu_word
    names = ('target_x','target_y','unit','count','distance','offset_x','offset_y','choice')
    return memory.from_first(_movement_divu_word(memory.state,
        memory.first_fields(frame),names[index],divisor,instruction))


def _command_bit_fields(memory, frame, value, bit):
    from ..high_level_main_flows.business_gameplay import _render_bit
    actual = _render_bit(CommandBitObservation(bool(frame.status_word & 4)),value,bit)
    memory.state.sr = (frame.status_word & 0xFFFB) | (4 if actual.zero else 0)
    return replace(frame,status_word=memory.state.sr)


def _command_dbra_fields(frame, index):
    result = u16((frame.data[index] & 0xFFFF) - 1)
    return frame.with_data(index,result,16), result != 0xFFFF


def _command_numbered_pair_fields(memory, frame, layout):
    """Four physical owners share the existing sole two-row tile algorithm."""
    from .contexts_equipment import EquipmentMenuMemory
    from .business_recruitment import _paired_tiles_fields
    if layout == 'budget':
        pitch, tile, counter = 16, 1, 2
    elif layout == 'recruitment_equipment':
        pitch, tile, counter = 34, 0, 1
    elif layout == 'candidate':
        pitch, tile, counter = 20, 0, 1
    else:
        raise ValueError('one original numbered-pair layout required')
    actual = _paired_tiles_fields(EquipmentMenuMemory(memory.state),
        memory.cursor_at(frame.addresses[0]),frame.data[tile] & 0xFFFF,
        frame.data[counter] & 0xFFFF,pitch)
    frame = frame.with_data(tile,actual.value,16)
    frame = frame.with_data(counter,actual.field_if_written,16)
    frame = frame.with_address(0,actual.destination.base)
    status = (17 if actual.carry else 0) | (8 if actual.negative else 0) | (4 if actual.zero else 0) | (2 if actual.overflow else 0)
    memory.state.sr = (frame.status_word & 0xFFE0) | status
    return replace(frame,status_word=memory.state.sr)


def _command_decimal_transaction_fields(memory, frame):
    """1270A whole-frame facade of the old unique kernel, not another digit loop."""
    from .business_budget import _six_place_decimal_fields
    numeric = DecimalMemory(memory.state,memory.cursor_at(frame.addresses[7]))
    digit_tile = frame.data[1] & 0xFFFF
    actual = _six_place_decimal_fields(numeric,frame.data[0],digit_tile,
        frame.data[2] & 0xFFFF,memory.cursor_at(frame.addresses[6]))
    frame = frame.with_data(0,actual.remainder)
    frame = frame.with_data(3,actual.divisor,16)
    frame = frame.with_data(4,actual.started,16)
    frame = frame.with_data(5,actual.glyph,16)
    frame = frame.with_address(6,actual.destination.base)
    frame = frame.with_address(7,numeric.stack_cursor.base)
    # Final ADD.W D1,D5 provides X; final MOVE.W to (A6)+ provides NZVC.
    frame, ignored_sum = _command_binary_fields(memory,frame,digit_tile,
        u16(actual.glyph-digit_tile),16)
    return _command_test_fields(memory,frame,actual.glyph,16)


def _command_decimal_place_fields(memory, frame):
    """12760 complete middle entry shares the same old packed-DIVU place core."""
    from .business_budget import _decimal_value_place_fields
    divisor = frame.data[3] & 0xFFFF
    if divisor == 0:
        memory.stop(frame,0x12762,'original DIVU divide-by-zero needs actual exception fields')
    digit_tile = frame.data[1] & 0xFFFF
    actual = _decimal_value_place_fields(memory.decimal,frame.data[0],divisor,
        digit_tile,frame.data[2] & 0xFFFF,frame.data[4] & 0xFFFF,
        memory.cursor_at(frame.addresses[6]))
    frame = frame.with_data(0,actual.remainder)
    frame = frame.with_data(4,actual.started,16)
    frame = frame.with_data(5,actual.glyph,16)
    frame = frame.with_address(6,actual.destination.base)
    if actual.started != 0:
        frame, ignored_sum = _command_binary_fields(memory,frame,digit_tile,
            u16(actual.glyph-digit_tile),16)
    # Actual CLR.W D0 followed by SWAP leaves remainder in the full LONG.
    return _command_test_fields(memory,frame,actual.remainder,32)


def _command_call_fields(memory, frame, target, continuation):
    """Original BSR/JSR owns exactly one physical LONG; callee owns no duplicate."""
    uint(target,32); uint(continuation,32)
    frame = frame.with_address(7,frame.addresses[7]-4)
    memory.state.write(frame.addresses[7],4,continuation)
    from .business_budget import _budget_known_fields
    from .business_recruitment import _recruitment_known_fields
    result = _budget_known_fields(memory,frame,target)
    if result is None:
        result = _recruitment_known_fields(memory,frame,target)
    if result is None and target == 0xAC08:
        from .contexts_display import SpritePacketMemory
        from .business_display import append_live_command_sprite_fields
        result = memory.from_first(append_live_command_sprite_fields(
            SpritePacketMemory(memory.state),memory.first_fields(frame)))
    if result is None:
        memory.stop(frame,target,'menu child has no actual complete entry ABI')
    actual = memory.state.read(result.addresses[7],4)
    if actual != continuation:
        memory.stop(result,actual,'original menu return LONG was modified')
    return result.with_address(7,result.addresses[7]+4)


def _command_tail_fields(memory, frame, target):
    """A real BRA shares the parent's return slot and changes neither CCR nor SP."""
    from .business_budget import _budget_known_fields
    from .business_recruitment import _recruitment_known_fields
    result = _budget_known_fields(memory,frame,target)
    if result is None:
        result = _recruitment_known_fields(memory,frame,target)
    if result is None:
        memory.stop(frame,target,'menu tail has no actual complete entry ABI')
    return result


def execute_command_menu_scene_fields(state, target, frame):
    """Typed Scene entry adapter; the actual parent already owns its outer LONG."""
    from ..high_level_scene_flows.domain import SceneState
    from ..high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
    from .business_budget import _budget_known_fields
    from .business_recruitment import _recruitment_known_fields
    if type(state) is not SceneState or type(frame) is not FirstDeploymentFrame:
        raise ValueError('actual Scene command-menu bridge required')
    frame.validate(state,True)
    memory = CommandMenuMemory(state)
    entered = memory.from_first(frame)
    actual = _budget_known_fields(memory,entered,target)
    if actual is None:
        actual = _recruitment_known_fields(memory,entered,target)
    if actual is None:
        memory.stop(entered,target,'target outside the closed command menu family')
    return memory.first_fields(actual)
