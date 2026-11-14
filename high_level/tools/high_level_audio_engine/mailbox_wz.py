"""One-shot WZ evidence for original08A2 ADD immediately before08A3 BIT.

The probable real-Z80 profile is WZ=(old HL+1)&FFFF. This is neither the BIT
effective address nor merely its old high byte. No global CPU/WZ model is
claimed. Two complete mailbox owners and the separately scoped rhythm owners
receive reversible views; each family retains independent pending evidence.
"""
import ast
import copy
from dataclasses import dataclass
from functools import wraps
import inspect
import threading
from types import FunctionType

from tools.high_level_audio_engine.domain import AudioBoundary, MemoryBitContext, tested_bit_conditions, word
from tools.high_level_audio_engine.hardware_scene import SoundDevice


OWNERS=('poll_command_mailboxes','arbitrate_command_slot')


def memptr_after_word_add(before_hl):
    """Probable NMOS-Z80 profile, including low-byte carry and16-bit wrap."""
    word(before_hl)
    return (before_hl+1)&0xffff


@dataclass(frozen=True)
class MailboxAddWitness:
    owner: object
    state: object
    function_name: str
    generation: int
    reset_epoch: int
    before_hl: int
    operand_bc: int
    result_hl: int
    memptr: int


def _dump(node):
    return ast.dump(node,include_attributes=False)


def _guarded_mailbox_view(original, service):
    if (type(original) is not FunctionType or original.__name__ not in OWNERS
            or original.__module__!='tools.high_level_audio_engine.business_mailbox'
            or inspect.isgeneratorfunction(original)):
        raise AudioBoundary('actual finite mailbox function identity required')
    tree=ast.parse(inspect.getsource(original))
    if len(tree.body)!=1 or type(tree.body[0]) is not ast.FunctionDef:
        raise AudioBoundary('one complete mailbox owner required')
    namespace=dict(original.__globals__)
    exec(compile(tree,'<plain mailbox owner identity guard>','exec'),namespace)
    plain=namespace[original.__name__]
    for name in ('co_code','co_consts','co_names','co_varnames','co_argcount','co_kwonlyargcount'):
        if getattr(plain.__code__,name)!=getattr(original.__code__,name):
            raise AudioBoundary('actual loaded mailbox owner differs from its full source')
    function=tree.body[0]
    if any(isinstance(node,ast.Name) and node.id.startswith('_mailbox_') for node in ast.walk(function)):
        raise AudioBoundary('original mailbox competes with private witness locals')
    view=copy.deepcopy(function)
    add_sites=[index for index,node in enumerate(view.body)
        if isinstance(node,ast.Assign) and isinstance(node.value,ast.Call)
        and _dump(node.value)==_dump(ast.parse('sum_word(lookup_cursor,count_and_data,conditions)',mode='eval').body)]
    bit_sites=[index for index,node in enumerate(view.body)
        if isinstance(node,ast.Assign) and isinstance(node.value,ast.Call)
        and isinstance(node.value.func,ast.Attribute)
        and _dump(node.value.func)==_dump(ast.parse('state.memory_bit_conditions',mode='eval').body)]
    if len(add_sites)!=1 or len(bit_sites)!=1:
        raise AudioBoundary('one actual08A2/08A3 pair required in each complete owner')
    add_index,bit_index=add_sites[0],bit_sites[0]
    assignment=ast.parse('lookup_cursor = u16('+view.body[add_index].targets[0].elts[0].id+')').body[0]
    if (bit_index!=add_index+3 or _dump(view.body[add_index+1])!=_dump(assignment)
            or not isinstance(view.body[add_index+2],ast.Assign)
            or _dump(view.body[bit_index].value.args[-3:][0])!=_dump(ast.Name(id='conditions',ctx=ast.Load()))
            or len(view.body[bit_index].value.args)!=5
            or _dump(view.body[bit_index].value.args[-2])!=_dump(ast.Name(id='lookup_cursor',ctx=ast.Load()))
            or _dump(view.body[bit_index].value.args[-1])!=_dump(ast.Constant(value=False))):
        raise AudioBoundary('08A2 ADD/carrier commit/memory read/08A3 BIT adjacency differs')
    saved_before=ast.parse('_mailbox_old_hl = lookup_cursor').body[0]
    witnessed=ast.parse('_mailbox_witness = _mailbox_wz.completed_add(state,'+repr(original.__name__)+
        ',_mailbox_old_hl,count_and_data,lookup_cursor)').body[0]
    original_bit=copy.deepcopy(view.body[bit_index])
    view.body[bit_index].value=ast.Call(func=ast.Attribute(value=ast.Name(id='_mailbox_wz',ctx=ast.Load()),
        attr='consume_bit',ctx=ast.Load()),args=[ast.Name(id='state',ctx=ast.Load()),
        ast.Name(id='_mailbox_witness',ctx=ast.Load()),ast.Call(func=ast.Name(id='MemoryBitContext',ctx=ast.Load()),
        args=copy.deepcopy(original_bit.value.args),keywords=[])],keywords=[])
    replacement_bit=copy.deepcopy(view.body[bit_index])
    view.body[add_index+2:add_index+2]=[witnessed]
    view.body[add_index:add_index]=[saved_before]
    inverse=copy.deepcopy(view)
    if (_dump(inverse.body[add_index])!=_dump(saved_before)
            or _dump(inverse.body[add_index+3])!=_dump(witnessed)
            or _dump(inverse.body[bit_index+2])!=_dump(replacement_bit)):
        raise AudioBoundary('mailbox witness inverse locations differ')
    inverse.body[bit_index+2]=copy.deepcopy(original_bit)
    del inverse.body[add_index+3]
    del inverse.body[add_index]
    if _dump(inverse)!=_dump(function):
        raise AudioBoundary('mailbox view does not invert to the complete actual original owner')
    namespace=dict(original.__globals__)
    namespace.update(_mailbox_wz=service,MemoryBitContext=MemoryBitContext)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[view],type_ignores=[])),
        '<reversible mailbox08A2 WZ witness view>','exec'),namespace)
    program=namespace[original.__name__]
    @wraps(original)
    def execute(state,inputs):
        try:
            return program(state,inputs)
        finally:
            service.expire_owner(state,original.__name__)
    return execute


class MailboxWzService:
    """Explicit per-AudioState probable-silicon profile, not a general CPU model.

    Only real scoped original mailbox calls can issue a witness. No initial WZ,
    fixed F, indexed-address substitution or unrelated nonindexed BIT fallback.
    The existing scoped continuation router owns all temporary callee binding.
    """
    def __init__(self,sound):
        if type(sound) is not SoundDevice or sound.scene is None:
            raise ValueError('one actual same-Scene sound device required')
        control=getattr(sound.audio_state.platform,'control_owner',None)
        if control is None or control.sound is not sound:
            raise ValueError('actual bound reset/control owner required')
        self.sound,self.state,self.control,self.scene=sound,sound.audio_state,control,sound.scene
        self.session=self.pending=None
        self.thread=None
        self.generation=self.reset_epoch=None
        self.views={}
        self.events=[]
        from tools.high_level_audio_engine.rhythm_wz import RhythmWzService
        self.rhythm=RhythmWzService(self)

    def bind(self):
        if getattr(self.state,'mailbox_wz_service',None) is not None:
            raise AudioBoundary('cannot replace an actual mailbox WZ service owner')
        self.state.mailbox_wz_service=self
        return self

    def require_bound(self,sound):
        if (sound is not self.sound or sound.audio_state is not self.state or sound.scene is not self.scene
                or getattr(self.state,'mailbox_wz_service',None) is not self):
            raise AudioBoundary('mailbox WZ evidence belongs to another AudioState/Scene')

    def begin_scope(self,session):
        self.require_bound(session.sound)
        if self.session is not None or self.pending is not None or session.thread!=threading.get_ident():
            raise AudioBoundary('one owning scoped mailbox WZ lease required')
        self.rhythm.require_idle()
        self.session,self.thread=session,threading.get_ident()
        self.generation,self.reset_epoch=self.control.generation,self.sound.reset_epoch

    def end_scope(self,session):
        if self.session is not session or self.thread!=threading.get_ident():
            raise AudioBoundary('only the actual WZ scope may release its evidence')
        self.rhythm.expire_scope()
        self.pending=self.session=self.thread=None

    def _active(self,state):
        self.require_bound(self.sound)
        if (state is not self.state or self.session is None or not self.session.entered
                or self.thread!=threading.get_ident() or not self.sound.executing
                or self.generation!=self.control.generation or self.reset_epoch!=self.sound.reset_epoch
                or self.sound.reset_asserted or self.sound.bus_requested or self.sound.m68k_granted):
            raise AudioBoundary('actual active same-State/reset/thread WZ scope required')

    def view_for(self,original):
        if original.__name__ not in OWNERS:
            return self.rhythm.view_for(original)
        if original not in self.views:
            self.views[original]=_guarded_mailbox_view(original,self)
        return self.views[original]

    def completed_add(self,state,function_name,before_hl,operand_bc,result_hl):
        self._active(state)
        for value in (before_hl,operand_bc,result_hl):
            word(value)
        if (function_name not in OWNERS or self.pending is not None
                or result_hl!=(before_hl+operand_bc)&0xffff
                or not self.session.scopes or self.session.scopes[-1].name!=function_name):
            raise AudioBoundary('one completed actual08A2 ADD witness required')
        witness=MailboxAddWitness(self,state,function_name,self.generation,self.reset_epoch,
            before_hl,operand_bc,result_hl,memptr_after_word_add(before_hl))
        self.pending=witness
        self.events.append(('actual08A2_ADD',function_name,before_hl,operand_bc,result_hl,witness.memptr))
        return witness

    def consume_bit(self,state,witness,context):
        self._active(state)
        if type(context) is not MemoryBitContext:
            raise ValueError('actual complete memory BIT context required')
        context.validate()
        if (witness is not self.pending or type(witness) is not MailboxAddWitness
                or witness.owner is not self or witness.state is not state
                or witness.generation!=self.generation or witness.reset_epoch!=self.reset_epoch
                or not self.session.scopes or self.session.scopes[-1].name!=witness.function_name
                or context.indexed or context.bit_index!=7 or context.address!=witness.result_hl):
            raise AudioBoundary('08A3 BIT lacks its same-State/site one-shot08A2 witness')
        self.pending=None
        flags=tested_bit_conditions(context.value,7,context.previous_conditions,
            address_high=witness.memptr>>8)
        self.events.append(('actual08A3_BIT',witness.function_name,context.address,
            witness.memptr,context.value,context.previous_conditions,flags))
        return flags

    def expire_owner(self,state,function_name):
        if state is self.state and self.pending is not None and self.pending.function_name==function_name:
            self.events.append(('unconsumed_witness_expired',function_name))
            self.pending=None

    def unbind(self):
        self.require_bound(self.sound)
        if self.session is not None or self.pending is not None or self.sound.executing:
            raise AudioBoundary('cannot unbind live mailbox WZ evidence')
        self.rhythm.expire_scope()
        del self.state.mailbox_wz_service
