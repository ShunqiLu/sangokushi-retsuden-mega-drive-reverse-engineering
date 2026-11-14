"""Source-derived original Timer-B tail return to009B, not a CPU scheduler."""
import ast
import copy
import inspect
import re
from types import FunctionType

from tools.high_level_audio_engine import business_hardware
from tools.high_level_audio_engine.domain import AudioBoundary


def _dump(node):
    return ast.dump(node,include_attributes=False)


def _source(function):
    if type(function) is not FunctionType or function.__module__!=business_hardware.__name__:
        raise AudioBoundary('actual existing original SFX owner identity required')
    parsed=ast.parse(inspect.getsource(function))
    if len(parsed.body)!=1 or type(parsed.body[0]) is not ast.FunctionDef:
        raise AudioBoundary('one complete actual SFX source owner required')
    namespace=dict(function.__globals__)
    exec(compile(parsed,'<plain original SFX owner guard>','exec'),namespace)
    plain=namespace[function.__name__]
    for name in ('co_code','co_consts','co_names','co_varnames','co_argcount','co_kwonlyargcount'):
        if getattr(plain.__code__,name)!=getattr(function.__code__,name):
            raise AudioBoundary('loaded complete SFX callable differs from source')
    return parsed.body[0]


def _normalized(statements):
    """Only generated temporary suffixes and the equivalent result ABI differ."""
    class Names(ast.NodeTransformer):
        def __init__(self):
            self.names={}
            self.counts={}
        def visit_Name(self,node):
            if node.id in ('InitializeAudioDriverResult','UpdateSfxChannelGroupsResult'):
                node.id='_equivalent_result_type'
            matched=re.fullmatch(r'(updated_audio_values|observed_byte|arithmetic_result|saved_audio_word)_[0-9]+',node.id)
            if matched:
                prefix=matched.group(1)
                if node.id not in self.names:
                    self.counts[prefix]=self.counts.get(prefix,0)+1
                    self.names[node.id]=prefix+'_'+str(self.counts[prefix])
                node.id=self.names[node.id]
            return node
    return _dump(Names().visit(ast.Module(body=copy.deepcopy(statements),type_ignores=[])))


class TimerBTailPatch:
    """Exact whole-owner reversible view change for one real nonlocal RET.

    The complete original source tail stays as the inverse authority. The
    only relocated branch is its original008B..0098 prefix; JP010F enters the
    existing proven-equivalent SFX owner with the already-live009B stack WORD.
    Its real RET returns009B and then the original A-status branch continues.
    """
    def __init__(self,view,main,carriers):
        self.main_index=view.body.index(main)
        suffix=view.body[self.main_index+1:]
        start_ast=_dump(ast.parse('sample = u8(1)').body[0])
        starts=[index for index,node in enumerate(suffix) if _dump(node)==start_ast]
        original_sfx=business_hardware.update_sfx_channel_groups
        named=_source(original_sfx)
        named_starts=[index for index,node in enumerate(named.body) if _dump(node)==start_ast]
        if len(starts)!=1 or len(named_starts)!=1:
            raise AudioBoundary('unique original010F tail start required')
        if _normalized(suffix[starts[0]:])!=_normalized(named.body[named_starts[0]:]):
            raise AudioBoundary('original complete inline010F..0138 and named SFX body differ')
        prefix=copy.deepcopy(suffix[:starts[0]])
        expected_push=_dump(ast.parse('stack_cursor = state.push_word(stack_cursor,lookup_cursor)').body[0])
        if (sum(_dump(node)==expected_push for node in prefix)!=1
                or not any(_dump(node)==_dump(ast.parse('lookup_cursor = u16(155)').body[0]) for node in prefix)):
            raise AudioBoundary('original Timer-B prefix lacks its actual009B return push')
        branches=[(index,node) for index,node in enumerate(main.body)
            if type(node) is ast.If and len(node.body)==1 and type(node.body[0]) is ast.Break]
        if len(branches)!=1:
            raise AudioBoundary('unique original0089 Timer-B branch required')
        self.branch_index,branch=branches[0]
        self.original_branch=copy.deepcopy(branch)
        call='from .business_hardware import update_sfx_channel_groups\nfrom .contexts import UpdateSfxChannelGroupsInput\n'
        call+='_timer_b_returned = update_sfx_channel_groups(state,UpdateSfxChannelGroupsInput('
        call+=','.join(name+'='+name for name in carriers)+',continuation=Continuation("driver",0x009B)))\n'
        call+='\n'.join(name+' = _timer_b_returned.'+name for name in carriers)+'\n'
        call+='_startup_resumed = yield _startup_point(0x009B,DriverFrame('+','.join(carriers)+'))\n'
        call+='('+','.join(carriers)+') = _startup_carriers(_startup_resumed)\n'
        branch.body=prefix+ast.parse(call).body
        self.changed_branch=copy.deepcopy(branch)

    def undo(self,inverse):
        main=inverse.body[self.main_index]
        if (type(main) is not ast.While or self.branch_index>=len(main.body)
                or _dump(main.body[self.branch_index])!=_dump(self.changed_branch)):
            raise AudioBoundary('actual Timer-B relocation inverse differs')
        main.body[self.branch_index]=copy.deepcopy(self.original_branch)
