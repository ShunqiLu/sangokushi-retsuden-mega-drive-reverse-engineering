"""Persistent complete206 reset owner across its actual260 audio-release point.

The complete original function is retained. A reversible two-statement yield
view pauses only after260's real write and CCR update, before262's real loop.
The original nonreturning tail calls00300 once; its actual MainSession owns
the later3BC wait. No reset prefix, RAM clear, CALL/RTS or checksum is replayed.
"""
import ast
import copy
from dataclasses import dataclass
import inspect
import sys
import threading
from types import FunctionType

from tools.high_level_main_flows import business_boot
from tools.high_level_main_flows.bootstrap_steps import BootstrapMainSession, BootstrapMainWait
from tools.high_level_main_flows.contexts_boot import ResetProfile
from tools.high_level_main_flows.contexts_gameplay import FirstDeploymentFrame, MovementContinuationBoundary
from tools.high_level_main_flows.business_movement_support import _movement_frame
from tools.high_level_scene_flows.domain import Boundary, checked_state


def _dump(node):
    if sys.version_info >= (3,13):
        return ast.dump(node,include_attributes=False,show_empty=True)
    return ast.dump(node,include_attributes=False)


def _complete_reset_view(point_factory,returned_frame):
    original = business_boot.reset_console_frame_fields
    if (type(original) is not FunctionType or original.__module__ != business_boot.__name__
            or original.__name__ != 'reset_console_frame_fields' or inspect.isgeneratorfunction(original)):
        raise Boundary('actual complete original206 reset owner required')
    parsed = ast.parse(inspect.getsource(original))
    if len(parsed.body) != 1 or type(parsed.body[0]) is not ast.FunctionDef:
        raise Boundary('one complete original reset function source required')
    namespace = dict(vars(business_boot))
    exec(compile(parsed,'<plain complete original reset identity>','exec'),namespace)
    plain = namespace[original.__name__]
    for attribute in ('co_code','co_consts','co_names','co_varnames','co_argcount','co_kwonlyargcount',
            'co_freevars','co_cellvars','co_flags'):
        if getattr(plain.__code__,attribute) != getattr(original.__code__,attribute):
            raise Boundary('actual loaded reset owner differs from its whole source')
    function = parsed.body[0]
    if any(isinstance(node,ast.Name) and node.id.startswith('_cold_reset_') for node in ast.walk(function)):
        raise Boundary('original reset source competes with private continuation names')
    anchor = ast.parse('frame = display_store_fields(state, frame, 0x260, frame.controller.base, low16(frame.choice))').body[0]
    sites = [index for index,node in enumerate(function.body) if _dump(node) == _dump(anchor)]
    if len(sites) != 1:
        raise Boundary('exact single completed original260 RESET release site required')
    inserted = ast.parse('_cold_reset_resumed = yield _cold_reset_point(0x262, frame)\n'
        'frame = _cold_reset_returned_frame(_cold_reset_resumed)').body
    view = copy.deepcopy(function)
    site = sites[0]+1
    view.body[site:site] = copy.deepcopy(inserted)
    inverse = copy.deepcopy(view)
    if [_dump(node) for node in inverse.body[site:site+2]] != [_dump(node) for node in inserted]:
        raise Boundary('the two reset suspension inverse statements differ')
    del inverse.body[site:site+2]
    if _dump(inverse) != _dump(function):
        raise Boundary('reset continuation view failed complete-function inverse AST identity')
    namespace = dict(vars(business_boot))
    namespace.update(_cold_reset_point=point_factory,_cold_reset_returned_frame=returned_frame)
    module = ast.fix_missing_locations(ast.Module(body=[view],type_ignores=[]))
    exec(compile(module,'<complete reset view with one reversible260 suspension>','exec'),namespace)
    program = namespace[original.__name__]
    if not inspect.isgeneratorfunction(program):
        raise Boundary('reset view must own its actual suspended Python frame')
    return original,program,dict(confidence='confirmed_complete_current_FN_inverse_AST_identity',
        original_function=original.__name__,original_module=original.__module__,
        original_top_level_statements=len(function.body),inserted_statements=2,
        original_reset_write=0x260,next_original_point=0x262,whole_FN_inverse=True,
        changed_original_statements=0,callee_or_global_replacement=False)


@dataclass(frozen=True)
class ResetAudioReleasePoint:
    session: object
    pc: int
    frame: FirstDeploymentFrame
    full_sr: int


class PersistentColdResetSession:
    """One original cold reset, one AudioOnly interleave, then true00300 tail.

    At262 no68000 IRQ or fabricated full frame is accepted: resume_release
    adopts only this exact captured point/frame after external audio work.
    Audio and devices still own every reset pulse, bus permit and DATA grant.
    After the true00300 owner reaches3BC, main_session is its actual persistent
    owner, not a second invocation created from an observed screenshot/state.
    """
    def __init__(self,state,frame,profile):
        self.state = checked_state(state)
        self.entry = _movement_frame(state,frame)
        if type(profile) is not ResetProfile or frame.status != state.sr&31:
            raise ValueError('actual explicit reset profile and full frame/SR required')
        profile.validate(state)
        self.profile,self.thread = profile,threading.get_ident()
        self.original,self.program_factory,self.source_contract = _complete_reset_view(self._point,self._returned_frame)
        self.program = self.waiting = self.main_session = None
        self.started = self.failed = False
        self.phase = 'not-started'
        self.events = []

    def _guard(self):
        if (threading.get_ident() != self.thread or business_boot.reset_console_frame_fields is not self.original
                or self.failed):
            raise Boundary('persistent reset owner/thread/source is no longer available')

    def _point(self,pc,frame):
        _movement_frame(self.state,frame)
        if pc != 0x262 or frame.status != self.state.sr&31:
            raise Boundary('actual completed260 full-frame continuation required')
        return ResetAudioReleasePoint(self,pc,frame,self.state.sr)

    def _returned_frame(self,frame):
        if (type(self.waiting) is not ResetAudioReleasePoint or frame is not self.waiting.frame
                or self.state.sr != self.waiting.full_sr):
            raise Boundary('audio-only interleave may not replace suspended68000 carriers/SR')
        return _movement_frame(self.state,frame)

    def _advance(self,frame=None):
        self._guard()
        try:
            point = next(self.program) if frame is None else self.program.send(frame)
        except MovementContinuationBoundary as boundary:
            main = getattr(boundary,'bootstrap_main_session',None)
            waiting = getattr(boundary,'bootstrap_main_wait',None)
            if (type(main) is not BootstrapMainSession or type(waiting) is not BootstrapMainWait
                    or main.state is not self.state or waiting.state is not self.state
                    or waiting is not main.waiting or boundary.target != waiting.poll
                    or boundary.context is not waiting.frame):
                self.failed = True
                raise
            # Original reset's tail has entered the actual nonreturning300.
            # Its existing façade retains the whole MainSession at real3BC.
            self.main_session,self.waiting,self.phase = main,waiting,'original-main-tail'
            self.events.append(('actual_original300_tail_handoff',waiting.poll,
                waiting.frame.stack_cursor.base,main.suspensions))
            return waiting
        except StopIteration as completion:
            self.failed = True
            raise Boundary('original nonreturning206/300 unexpectedly returned ordinarily') from completion
        except BaseException:
            self.failed = True
            raise
        if type(point) is not ResetAudioReleasePoint or point.session is not self:
            self.failed = True
            raise Boundary('reset owner yielded a foreign or untyped point')
        self.waiting,self.phase = point,'actual-audio-release'
        self.events.append(('completed_original260_suspend_before262',point.pc,
            point.frame.stack_cursor.base,point.full_sr))
        return point

    def start(self):
        self._guard()
        if self.started:
            raise Boundary('original reset206 prefix must never replay')
        self.started = True
        self.program = self.program_factory(self.state,self.entry,self.profile)
        return self._advance()

    def resume_release(self,point):
        self._guard()
        if (not self.started or self.phase != 'actual-audio-release' or point is not self.waiting
                or type(point) is not ResetAudioReleasePoint or point.session is not self):
            raise Boundary('the actual live262 audio-release point is required')
        frame = self._returned_frame(point.frame)
        return self._advance(frame)

    def resume_main(self,frame,pc):
        self._guard()
        if self.phase != 'original-main-tail' or self.main_session is None:
            raise Boundary('reset has not tail-handed to its actual original main owner')
        self.waiting = self.main_session.resume(frame,pc)
        return self.waiting
