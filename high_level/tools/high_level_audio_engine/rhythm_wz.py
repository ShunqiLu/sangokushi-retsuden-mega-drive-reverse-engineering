"""Scoped WZ witnesses for the two original rhythm BIT2,(HL) sites.

Only the complete rhythm readers receive a reversible source-derived view.
The hardware rule is the existing probable NMOS-Z80 MEMPTR profile, not a
locally verified silicon model or a general processor/WZ implementation.
"""
import ast
import copy
from dataclasses import dataclass
from functools import wraps
import inspect
from types import CodeType, FunctionType

from tools.high_level_audio_engine.domain import (
    AudioBoundary, AudioState, MemoryBitContext, byte, tested_bit_conditions, word,
)


OWNERS = ('read_rhythm_note', 'resume_rhythm_parameter_stream')
_SOURCE_MODULE = 'tools.high_level_audio_engine.business_notes'


def _dump(node):
    return ast.dump(node, include_attributes=False)


def _statement(source):
    nodes = ast.parse(source).body
    if len(nodes) != 1:
        raise AudioBoundary('one rhythm witness statement required')
    return nodes[0]


def _code_shape(code):
    """All executable CodeType fields, excluding source-location metadata."""
    if type(code) is not CodeType:
        raise AudioBoundary('actual complete loaded rhythm CodeType required')
    constants = tuple(_code_shape(value) if type(value) is CodeType else value
                      for value in code.co_consts)
    return (code.co_name, getattr(code, 'co_qualname', code.co_name),
            code.co_argcount, code.co_posonlyargcount, code.co_kwonlyargcount,
            code.co_nlocals, code.co_stacksize, code.co_flags, code.co_code,
            constants, code.co_names, code.co_varnames, code.co_freevars,
            code.co_cellvars, getattr(code, 'co_exceptiontable', b''))


def _loaded_source(original, module_name, function_name):
    """Validate a complete actual callable against its own fresh namespace."""
    if (type(original) is not FunctionType or original.__name__ != function_name
            or original.__module__ != module_name or original.__closure__
            or inspect.isgeneratorfunction(original)
            or inspect.iscoroutinefunction(original)):
        raise AudioBoundary('actual finite original rhythm/return owner required')
    tree = ast.parse(inspect.getsource(original))
    if (len(tree.body) != 1 or type(tree.body[0]) is not ast.FunctionDef
            or tree.body[0].decorator_list):
        raise AudioBoundary('one complete undecorated rhythm/return owner required')
    namespace = dict(original.__globals__)
    exec(compile(tree, '<plain complete rhythm owner identity guard>', 'exec'), namespace)
    if _code_shape(namespace[function_name].__code__) != _code_shape(original.__code__):
        raise AudioBoundary('loaded rhythm/return owner differs from its complete source')
    return tree.body[0]


class _WitnessInverse(ast.NodeTransformer):
    """Remove only the explicitly recorded witness edits, not original effects."""
    def __init__(self, edits):
        self.edits = edits
        self.counts = {key: 0 for key in edits}

    def visit(self, node):
        if isinstance(node, ast.stmt):
            key = _dump(node)
            if key in self.edits:
                self.counts[key] += 1
                original = self.edits[key]
                return None if original is None else copy.deepcopy(original)
        return super().visit(node)


def _guarded_rhythm_view(original, service):
    function = _loaded_source(original, _SOURCE_MODULE, original.__name__)
    if original.__name__ not in OWNERS:
        raise AudioBoundary('only the two original complete rhythm readers are owned')
    if any(isinstance(node, ast.Name) and node.id.startswith('_rhythm_')
           for node in ast.walk(function)):
        raise AudioBoundary('original rhythm reader competes with private witness names')
    view = copy.deepcopy(function)
    edits = {}

    def record(new, old=None):
        key = _dump(new)
        if key in edits:
            raise AudioBoundary('rhythm witness edit is not unique')
        edits[key] = copy.deepcopy(old)
        return new

    def added(source):
        return record(_statement(source))

    def replace_bit(node, witness_name):
        old = copy.deepcopy(node)
        call = node.value
        if (type(node) is not ast.Assign or len(node.targets) != 1
                or _dump(node.targets[0]) != _dump(ast.Name(id='conditions', ctx=ast.Store()))
                or type(call) is not ast.Call or call.keywords
                or _dump(call.func) != _dump(ast.parse('state.memory_bit_conditions', mode='eval').body)
                or len(call.args) != 5 or type(call.args[0]) is not ast.Name
                or [_dump(value) for value in call.args[1:]] != [_dump(value) for value in
                    ast.parse('(2, conditions, lookup_cursor, False)', mode='eval').body.elts]):
            raise AudioBoundary('exact original rhythm BIT2 memory conditions call required')
        node.value = ast.Call(
            func=ast.Attribute(value=ast.Name(id='_rhythm_wz', ctx=ast.Load()),
                               attr='consume_bit', ctx=ast.Load()),
            args=[ast.Name(id='state', ctx=ast.Load()),
                  ast.Name(id=witness_name, ctx=ast.Load()),
                  ast.Call(func=ast.Name(id='_rhythm_MemoryBitContext', ctx=ast.Load()),
                           args=copy.deepcopy(call.args), keywords=[])], keywords=[])
        record(node, old)

    # The source's IF body is the JP09A9 *not taken* path. Only PUSH DE and
    # LD HL,1D60 separate that decision from the first actual memory BIT.
    prefix = [_statement('stack_cursor = state.push_word(stack_cursor, parameter_cursor)'),
              _statement('lookup_cursor = u16(7520)')]
    jp_test = ast.parse('not (bool(conditions & 0x40))', mode='eval').body
    candidates = [node for node in ast.walk(view) if type(node) is ast.If
                  and _dump(node.test) == _dump(jp_test) and len(node.body) >= 8
                  and [_dump(part) for part in node.body[:2]] == [_dump(part) for part in prefix]]
    if len(candidates) != 1:
        raise AudioBoundary('one exact09A9/09B0 rhythm block required')
    jp = candidates[0]
    if (type(jp.body[2]) is not ast.Assign or len(jp.body[2].targets) != 1
            or type(jp.body[2].targets[0]) is not ast.Name
            or _dump(jp.body[2].value) != _dump(ast.parse('state.read(lookup_cursor)', mode='eval').body)
            or type(jp.body[3]) is not ast.Assign
            or type(jp.body[3].value) is not ast.Call
            or _dump(jp.body[3].value.args[0]) != _dump(ast.Name(
                id=jp.body[2].targets[0].id, ctx=ast.Load()))):
        raise AudioBoundary('09B0 must consume its adjacent original operand read')
    first_bit, first_jr = jp.body[3:5]
    second_load, second_read, second_bit = jp.body[5:8]
    if (type(first_jr) is not ast.If or first_jr.orelse
            or _dump(first_jr.test) != _dump(ast.parse('not (not (conditions & 0x40))', mode='eval').body)
            or len(first_jr.body) != 3
            or [_dump(node) for node in first_jr.body[:2]] != [_dump(node) for node in
                ast.parse('sample = u8(sample & 15)\nconditions = logic_conditions(sample, True)').body]
            or type(first_jr.body[2]) is not ast.If
            or _dump(second_load) != _dump(_statement('lookup_cursor = u16(7664)'))
            or type(second_read) is not ast.Assign or len(second_read.targets) != 1
            or type(second_read.targets[0]) is not ast.Name
            or _dump(second_read.value) != _dump(ast.parse('state.read(lookup_cursor)', mode='eval').body)
            or type(second_bit) is not ast.Assign or type(second_bit.value) is not ast.Call
            or _dump(second_bit.value.args[0]) != _dump(ast.Name(
                id=second_read.targets[0].id, ctx=ast.Load()))):
        raise AudioBoundary('exact09B2/09B6 paths and09F8/09FB adjacency required')
    second_jr = first_jr.body[2]
    if _dump(second_jr.test) != _dump(jp_test) or second_jr.orelse:
        raise AudioBoundary('original09B6 fallthrough/empty taken branch required')

    # Guard the existing final original CALL and all eight carrier adoptions.
    calls = [index for index, node in enumerate(second_jr.body)
             if type(node) is ast.Assign and type(node.value) is ast.Call
             and _dump(node.value.func) == _dump(ast.Name(id='reset_timer_control', ctx=ast.Load()))]
    if len(calls) != 1:
        raise AudioBoundary('one actual09F5 reset_timer_control call required')
    call_index = calls[0]
    call = second_jr.body[call_index]
    if (call_index < 1 or len(call.targets) != 1 or type(call.targets[0]) is not ast.Name
            or call.value.keywords or len(call.value.args) != 2
            or _dump(second_jr.body[call_index - 1]) != _dump(_statement(
                'stack_cursor = state.push_word(stack_cursor, 2552)'))):
        raise AudioBoundary('original09F5 must push its actual09F8 return word')
    fields = ('auxiliary_cursor', 'channel_cursor', 'conditions', 'count_and_data',
              'lookup_cursor', 'parameter_cursor', 'sample', 'stack_cursor')
    expected_call = _statement(
        call.targets[0].id + ' = reset_timer_control(state, ResetTimerControlInput('
        + ', '.join(name + '=' + name for name in fields)
        + ', continuation=Continuation("driver", 2552)))')
    expected_adoptions = [_statement(name + ' = ' + call.targets[0].id + '.' + name)
                          for name in fields]
    if (_dump(call) != _dump(expected_call)
            or [_dump(node) for node in second_jr.body[call_index + 1:]] !=
            [_dump(node) for node in expected_adoptions]):
        raise AudioBoundary('09F5 complete original call/returned carrier suffix differs')

    owner_name = repr(original.__name__)
    replace_bit(first_bit, '_rhythm_witness_09b0')
    replace_bit(second_bit, '_rhythm_witness_09fb')
    jp.body.insert(0, added('_rhythm_witness_09b0 = _rhythm_wz.completed_jp('
                           'state, ' + owner_name + ', conditions)'))
    # These new ELSEs are exactly the two original taken JR paths; no flag or
    # original branch expression is changed. The long path keeps both ELSEs out.
    first_jr.orelse = [added('_rhythm_witness_09fb = _rhythm_wz.completed_jr('
                            'state, ' + owner_name + ', 0x09B2, conditions)')]
    second_jr.orelse = [added('_rhythm_witness_09fb = _rhythm_wz.completed_jr('
                             'state, ' + owner_name + ', 0x09B6, conditions)')]
    second_jr.body.insert(call_index - 1, added('_rhythm_return_caller_sp = stack_cursor'))
    second_jr.body.insert(call_index + 1, added('_rhythm_return_entered_sp = stack_cursor'))
    second_jr.body.append(added('_rhythm_witness_09fb = _rhythm_wz.completed_return('
                               'state, ' + owner_name + ', conditions, '
                               '_rhythm_return_caller_sp, _rhythm_return_entered_sp, stack_cursor)'))

    inverse = _WitnessInverse(edits)
    restored = inverse.visit(copy.deepcopy(view))
    if (any(count != 1 for count in inverse.counts.values())
            or _dump(restored) != _dump(function)):
        raise AudioBoundary('rhythm witnesses do not invert to the complete original AST')
    # Only this owner's globals are copied; the added bindings are private and
    # never installed in the business module's global namespace.
    namespace = dict(original.__globals__)
    namespace.update(_rhythm_wz=service, _rhythm_MemoryBitContext=MemoryBitContext)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[view], type_ignores=[])),
                 '<reversible rhythm JP/JR/RET WZ witness view>', 'exec'), namespace)
    program = namespace[original.__name__]

    @wraps(original)
    def execute(state, inputs):
        try:
            return program(state, inputs)
        finally:
            service.expire_owner(state, original.__name__)
    return execute


@dataclass(frozen=True)
class RhythmControlWitness:
    owner: object
    state: object
    call_scope: object
    function_name: str
    generation: int
    reset_epoch: int
    producer_pc: int
    bit_pc: int
    memptr: int
    address: int
    conditions: int
    stack_evidence: tuple


class RhythmWzService:
    """Two rhythm BIT sites under the existing exclusive WZ/session owner.

    Pending evidence is separate from the mailbox ADD witness. There is no
    initial WZ, global register state, general opcode dispatcher or fallback.
    """
    def __init__(self, mailbox_owner):
        self.mailbox = mailbox_owner
        self.state = mailbox_owner.state
        self.pending = None
        self.views = {}
        self.return_owners = None

    def _scope(self, state, function_name):
        self.mailbox._active(state)
        scopes = self.mailbox.session.scopes
        if function_name not in OWNERS or not scopes or scopes[-1].name != function_name:
            raise AudioBoundary('actual owning complete rhythm call scope required')
        return scopes[-1]

    def require_idle(self):
        if self.pending is not None:
            raise AudioBoundary('unconsumed rhythm WZ witness cannot enter another scope')

    def expire_scope(self):
        if self.pending is not None:
            self.mailbox.events.append(('unconsumed_rhythm_witness_expired',
                                        self.pending.function_name, self.pending.bit_pc))
        self.pending = None

    def expire_owner(self, state, function_name):
        if (state is self.state and self.pending is not None
                and self.pending.function_name == function_name):
            self.expire_scope()

    def _guard_return_chain(self, initial=False):
        from tools.high_level_audio_engine import (
            business_loaders, business_lifecycle_reset, business_lifecycle_shared,
        )
        specifications = (
            (business_loaders, 'reset_timer_control'),
            (business_lifecycle_reset, 'run_reset_timer_control'),
            (business_lifecycle_reset, 'commit_timer_reset'),
            (business_lifecycle_shared, 'finish_sound_command'),
        )
        if initial:
            owners = []
            for module, name in specifications:
                function = getattr(module, name)
                _loaded_source(function, module.__name__, name)
                owners.append((module, name, function, function.__code__))
            self.return_owners = tuple(owners)
        if self.return_owners is None:
            raise AudioBoundary('complete actual0811 return-owner evidence required')
        for module, name, function, code in self.return_owners:
            if getattr(module, name) is not function or function.__code__ is not code:
                raise AudioBoundary('actual rhythm reset/return owner changed')
        reset, run, commit, finish = (row[2] for row in self.return_owners)
        if (reset.__globals__.get('run_reset_timer_control') is not run
                or run.__globals__.get('commit_timer_reset') is not commit
                or commit.__globals__.get('finish_sound_command') is not finish
                or getattr(self.state.consume_return, '__func__', None) is not AudioState.consume_return
                or 'consume_return' in self.state.__dict__):
            raise AudioBoundary('original0811 shared actual consume_return chain required')

    def view_for(self, original):
        if original.__name__ not in OWNERS:
            return original
        if original not in self.views:
            self._guard_return_chain(initial=self.return_owners is None)
            self.views[original] = _guarded_rhythm_view(original, self)
        return self.views[original]

    def _issue(self, state, function_name, producer_pc, bit_pc, memptr, address,
               conditions, stack_evidence=()):
        scope = self._scope(state, function_name)
        byte(conditions)
        self.require_idle()
        witness = RhythmControlWitness(self, state, scope, function_name,
            self.mailbox.generation, self.mailbox.reset_epoch, producer_pc,
            bit_pc, memptr, address, conditions, stack_evidence)
        self.pending = witness
        self.mailbox.events.append(('actual_rhythm_WZ_producer', function_name,
                                    producer_pc, bit_pc, memptr, conditions, stack_evidence))
        return witness

    def completed_jp(self, state, function_name, conditions):
        byte(conditions)
        if conditions & 0x40:
            raise AudioBoundary('09A9 must actually fall through to09B0')
        # Conditional JP sets WZ even when not taken. The original target is
        # 0A26, not the following BIT's effective address1D60.
        return self._issue(state, function_name, 0x09A9, 0x09B0, 0x0A26,
                           0x1D60, conditions)

    def completed_jr(self, state, function_name, producer_pc, conditions):
        byte(conditions)
        if ((producer_pc == 0x09B2 and not conditions & 0x40)
                or (producer_pc == 0x09B6 and conditions & 0x40)):
            return self._issue(state, function_name, producer_pc, 0x09FB,
                               0x09F8, 0x1DF0, conditions)
        raise AudioBoundary('only an actually taken09B2/09B6 JR may witness09FB')

    def completed_return(self, state, function_name, conditions,
                         caller_sp, entered_sp, returned_sp):
        self._scope(state, function_name)
        for value in (caller_sp, entered_sp, returned_sp):
            word(value)
        self._guard_return_chain()
        if entered_sp != (caller_sp - 2) & 0xFFFF or returned_sp != caller_sp:
            raise AudioBoundary('09F5 must complete its original real09F8 RET and SP restoration')
        # This is after the original callable succeeded and all returned live
        # carriers were adopted. Its own consume_return already checked09F8;
        # no new RAM read, stack write or synthetic return is introduced here.
        return self._issue(state, function_name, 0x05E2, 0x09FB, 0x09F8,
                           0x1DF0, conditions, (0x09F5, caller_sp, entered_sp, returned_sp))

    def consume_bit(self, state, witness, context):
        if type(context) is not MemoryBitContext:
            raise ValueError('actual complete rhythm memory BIT context required')
        context.validate()
        if type(witness) is not RhythmControlWitness:
            raise AudioBoundary('actual one-shot rhythm control-flow witness required')
        scope = self._scope(state, witness.function_name)
        if (witness is not self.pending or witness.owner is not self
                or witness.state is not state or witness.call_scope is not scope
                or witness.generation != self.mailbox.generation
                or witness.reset_epoch != self.mailbox.reset_epoch
                or context.indexed or context.bit_index != 2
                or context.address != witness.address
                or context.previous_conditions != witness.conditions
                or (witness.bit_pc, witness.address) not in ((0x09B0, 0x1D60), (0x09FB, 0x1DF0))):
            raise AudioBoundary('rhythm BIT lacks its own fresh same-State/site control-flow witness')
        self.pending = None
        flags = tested_bit_conditions(context.value, 2, context.previous_conditions,
                                      address_high=witness.memptr >> 8)
        self.mailbox.events.append(('actual_rhythm_BIT', witness.function_name,
                                    witness.bit_pc, witness.producer_pc, witness.memptr,
                                    context.address, context.value, context.previous_conditions, flags))
        return flags
