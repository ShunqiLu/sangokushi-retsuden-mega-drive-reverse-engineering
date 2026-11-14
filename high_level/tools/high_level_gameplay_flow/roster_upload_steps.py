"""Complete Main414 roster upload with its one actual refresh continuation.

The original53E6 body is retained whole. Names, glyphs, label dispatch and CPU
VDP submissions remain their existing synchronous owners on the same Scene.
"""
import ast
import copy
import importlib
import inspect
from types import FunctionType

from .battle_trigger_steps import BattleScenePrograms, _dump, _code_shape, _top_code
from .contexts_services import SceneRefreshMemory
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from .compiler_roster_upload_steps import EXPECTED_OWNER_ASTS


MAIN_ENTRY = 0x414
MAIN_OWNER = 'upload_officer_roster_panel_frame_fields'
MAIN_MODULE = 'tools.high_level_main_flows.business_main'
ORIGINAL_CALLS = ((0x54CA,0x5452),(0xAE8A,0x5460),(0xAE8A,0x5496),
    (0x506C,0x54BE),(0xAF48,0x54C4))
VIEW_GLOBALS = ('display_frame_fields','display_status_fields','display_store_fields',
    'display_move_fields','display_loop_fields','display_address_fields','display_shift_word_fields',
    '_roster_panel_pixels_frame_fields','first_replace','low16','s16')


def _roster_upload_tree(original_tree):
    """Lift five actual calls; invert the complete FN and complete Main module."""
    result = copy.deepcopy(original_tree)
    selected = [(index,node) for index,node in enumerate(original_tree.body)
        if isinstance(node,ast.FunctionDef) and node.name==MAIN_OWNER]
    if len(selected)!=1:raise ValueError('one complete original Main414 body required')
    index,original = selected[0]
    if _dump(original)!=EXPECTED_OWNER_ASTS[MAIN_MODULE][MAIN_OWNER]:
        raise ValueError('complete current roster upload source required')
    replacements = []
    calls = []

    class Lift(ast.NodeTransformer):
        def visit_Call(self,node):
            node = self.generic_visit(node)
            if not isinstance(node.func,ast.Name) or node.func.id!='display_call_fields':return node
            if node.keywords or len(node.args)!=4:
                raise ValueError('actual four-argument display CALL required')
            pair = tuple(ast.literal_eval(value) for value in node.args[2:])
            if pair not in ORIGINAL_CALLS:raise ValueError('unadmitted roster CALL/return pair')
            before = copy.deepcopy(node)
            calls.append(pair)
            node.func.id = '_roster_upload_display_call'
            after = ast.copy_location(ast.YieldFrom(value=node),node)
            replacements.append((before,copy.deepcopy(after)))
            return after

    changed = Lift().visit(copy.deepcopy(original))
    if tuple(calls)!=ORIGINAL_CALLS:raise ValueError('all five original roster CALL sites required')
    pending = list(replacements)

    class Inverse(ast.NodeTransformer):
        def visit_YieldFrom(self,node):
            for position,(before,after) in enumerate(pending):
                if _dump(node)==_dump(after):
                    pending.pop(position)
                    return copy.deepcopy(before)
            raise ValueError('unadmitted roster upload continuation expression')

    inverse = Inverse().visit(copy.deepcopy(changed))
    if pending or _dump(inverse)!=_dump(original):
        raise ValueError('complete original roster FN inverse differs')
    result.body[index] = changed
    restored = copy.deepcopy(result)
    restored.body[index] = inverse
    if _dump(restored)!=_dump(original_tree):
        raise ValueError('complete original Main module inverse differs')
    return ast.fix_missing_locations(result)


class RosterUploadScenePrograms(BattleScenePrograms):
    """One real414/3CE invocation; no independent53E6 or559E entry admission."""

    def __init__(self,state):
        super().__init__(state)
        self.upload_modules = {path:importlib.import_module(path) for path in EXPECTED_OWNER_ASTS}
        self.upload_owners = []
        originals = {}
        for path,expected in EXPECTED_OWNER_ASTS.items():
            module = self.upload_modules[path]
            tree = ast.parse(inspect.getsource(module),filename=module.__file__)
            plain = compile(tree,module.__file__,'exec',dont_inherit=True)
            nodes = {node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
            for name,source_ast in expected.items():
                owner = getattr(module,name)
                if (name not in nodes or _dump(nodes[name])!=source_ast
                        or type(owner)is not FunctionType or owner.__globals__ is not vars(module)
                        or owner.__module__!=module.__name__ or owner.__name__!=name
                        or owner.__closure__ is not None or owner.__code__.co_freevars
                        or _code_shape(owner.__code__)!=_code_shape(_top_code(plain,name))):
                    raise ValueError('actual complete roster upload dependency required: '+name)
                self.upload_owners.append((module,name,owner,owner.__code__))
                originals[path,name] = owner
        module = self.upload_modules[MAIN_MODULE]
        tree = ast.parse(inspect.getsource(module),filename=module.__file__)
        derived = compile(_roster_upload_tree(tree),module.__file__,'exec',dont_inherit=True)
        original = originals[MAIN_MODULE,MAIN_OWNER]
        self.upload_namespace = dict(vars(module))
        alias = '_roster_upload_display_call'
        if alias in self.upload_namespace:raise ValueError('private roster alias must not shadow original source')
        self.upload_display_call = self.views['display','display_call_fields']
        self.upload_display_call_code = self.upload_display_call.__code__
        self.upload_namespace[alias] = self.upload_display_call
        self.upload_bindings = {name:self.upload_namespace[name] for name in VIEW_GLOBALS+(alias,)}
        view = FunctionType(_top_code(derived,MAIN_OWNER),self.upload_namespace,MAIN_OWNER,original.__defaults__,None)
        view.__kwdefaults__,view.__annotations__ = original.__kwdefaults__,dict(original.__annotations__)
        if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
            raise ValueError('one complete closure-free roster upload generator required')
        self.upload_view,self.upload_view_owner,self.upload_view_code = view,view,view.__code__

    def require_current(self,state):
        super().require_current(state)
        if hasattr(self,'upload_owners'):
            for module,name,owner,code in self.upload_owners:
                if getattr(module,name)is not owner or owner.__code__ is not code:
                    raise ValueError('actual roster upload dependency changed: '+name)
        if hasattr(self,'upload_view_owner'):
            if self.upload_view is not self.upload_view_owner or self.upload_view.__code__ is not self.upload_view_code:
                raise ValueError('complete roster upload view changed')
            if (self.views['display','display_call_fields']is not self.upload_display_call
                    or self.upload_display_call.__code__ is not self.upload_display_call_code):
                raise ValueError('the same complete inherited display CALL view is required')
            for name,owner in self.upload_bindings.items():
                if self.upload_namespace.get(name)is not owner:
                    raise ValueError('private roster upload binding changed: '+name)

    def _display_child(self,state,frame,target,continuation):
        self.require_current(state)
        if target==MAIN_ENTRY:
            if continuation!=0x3CE:
                raise MovementContinuationBoundary(target,frame,'Main414 requires its actual3CE LONG')
            return (yield from self.upload_view(state,frame))
        if (target,continuation)==(0xAF48,0x54C4):
            return (yield from self._refresh(SceneRefreshMemory(state),frame))
        return (yield from super()._display_child(state,frame,target,continuation))

    def main_scene_call(self,state,frame,target,continuation):
        if target!=MAIN_ENTRY:
            return (yield from super().main_scene_call(state,frame,target,continuation))
        self.require_current(state)
        if self._started or continuation!=0x3CE:
            raise ValueError('one actual indexed Main414 invocation required')
        self._started = True
        return (yield from self.upload_display_call(state,frame,target,continuation))
