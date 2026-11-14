"""Four original Main title entries with actual VDP and sound-bus continuations.

Complete existing title parents and their physical CALL helper are retained.
Only finite propagation expressions change; all title and rendering algorithms
remain their current complete owners on the same Scene and hardware.
"""
import ast
import copy
import importlib
import inspect
from types import FunctionType

from .battle_trigger_steps import BattleScenePrograms, _dump, _code_shape, _top_code
from .contexts_services import SceneRefreshMemory
from ..high_level_main_flows.contexts_gameplay import MovementContinuationBoundary
from .compiler_title_scene_steps import EXPECTED_TITLE_AST, EXPECTED_REUSED_ASTS
from .compiler_roster_panel_steps import EXPECTED_MODULE_AST as ROSTER_REGISTRY_MODULE_AST


TITLE_MODULE = 'tools.high_level_main_flows.business_title'
MAIN_ENTRIES = {0x3E0:'initialize_title_scene_fields',0x3E4:'initialize_title_scene_preserving_mode_fields',
    0x3EC:'initialize_secondary_title_scene_fields',0x3F0:'initialize_title_transition_scene_fields'}
VIEW_SPECS = {
    'initialize_title_scene_fields':{'initialize_title_scene_preserving_mode_fields':(1,'_title_view_initialize_title_scene_preserving_mode_fields')},
    'initialize_title_scene_preserving_mode_fields':{'_begin_title_transfer_fields':(1,'_title_view__begin_title_transfer_fields'),
        '_title_child_fields':(9,'_title_view__title_child_fields')},
    'initialize_secondary_title_scene_fields':{'_begin_title_transfer_fields':(1,'_title_view__begin_title_transfer_fields'),
        '_title_child_fields':(2,'_title_view__title_child_fields')},
    'initialize_title_transition_scene_fields':{'_begin_title_transfer_fields':(1,'_title_view__begin_title_transfer_fields'),
        '_title_child_fields':(1,'_title_view__title_child_fields')},
    '_begin_title_transfer_fields':{'_title_child_fields':(1,'_title_view__title_child_fields')},
    '_title_child_fields':{
        'clear_video_sprite_plane_fields':(1,'clear_video_sprite_plane_fields'),
        'initialize_video_registers_and_planes_fields':(1,'initialize_video_registers_and_planes_fields'),
        'enqueue_sound_command_fields':(1,'enqueue_sound_command_fields')},
}
SERVICE_NAMES = ('clear_video_sprite_plane_fields','initialize_video_registers_and_planes_fields','enqueue_sound_command_fields')
REGISTERED_PORTRAIT_MODULE = 'tools.high_level_dynamic_flows.business_actions'
REGISTERED_PORTRAIT_NAMES = ('upload_portrait_tiles_frame_fields','_portrait_banked_strip_frame_fields',
    'upload_scene_tile_block_frame_fields','upload_one_scene_tile_frame_fields')


def _title_tree(original_tree):
    """Twenty finite expressions; inverse each complete FN and entire module."""
    if _dump(original_tree)!=EXPECTED_TITLE_AST:raise ValueError('complete current original title module required')
    result = copy.deepcopy(original_tree)
    inverses = {}
    for index,original in enumerate(original_tree.body):
        if not isinstance(original,ast.FunctionDef) or original.name not in VIEW_SPECS:continue
        wanted = VIEW_SPECS[original.name]
        counts = {name:0 for name in wanted}
        replacements = []

        class Lift(ast.NodeTransformer):
            def visit_Call(self,node):
                node = self.generic_visit(node)
                if not isinstance(node.func,ast.Name) or node.func.id not in wanted:return node
                name = node.func.id
                before = copy.deepcopy(node)
                counts[name] += 1
                if original.name=='_title_child_fields':
                    if (node.keywords or _dump(node)!=_dump(ast.parse(
                            name+'(SceneRefreshMemory(state),entered)',mode='eval').body)):
                        raise ValueError('one actual same-Scene complete title service call required')
                    changed = ast.parse('_title_service(state,entered,'+repr(name)+')',mode='eval').body
                else:
                    changed = copy.deepcopy(node)
                    changed.func.id = wanted[name][1]
                after = ast.copy_location(ast.YieldFrom(value=changed),node)
                replacements.append((before,copy.deepcopy(after)))
                return after

        changed = Lift().visit(copy.deepcopy(original))
        if counts!={name:pair[0] for name,pair in wanted.items()}:
            raise ValueError('exact full title propagation counts differ: '+original.name)
        pending = list(replacements)

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self,node):
                for position,(before,after) in enumerate(pending):
                    if _dump(node)==_dump(after):
                        pending.pop(position)
                        return copy.deepcopy(before)
                raise ValueError('unadmitted title continuation expression')

        inverse = Inverse().visit(copy.deepcopy(changed))
        if pending or _dump(inverse)!=_dump(original):raise ValueError('complete title FN inverse differs: '+original.name)
        result.body[index],inverses[index] = changed,inverse
    if len(inverses)!=6:raise ValueError('all six complete title parent/helper views required')
    restored = copy.deepcopy(result)
    for index,inverse in inverses.items():restored.body[index]=inverse
    if _dump(restored)!=_dump(original_tree):raise ValueError('whole original title module inverse differs')
    return ast.fix_missing_locations(result)


class TitleScenePrograms(BattleScenePrograms):
    """Exact3E0/3E4/3EC/3F0 with their original3CE and physical child returns."""

    def __init__(self,state):
        super().__init__(state)
        self.title_module = importlib.import_module(TITLE_MODULE)
        tree = ast.parse(inspect.getsource(self.title_module),filename=self.title_module.__file__)
        if _dump(tree)!=EXPECTED_TITLE_AST:raise ValueError('complete current title source required')
        plain = compile(tree,self.title_module.__file__,'exec',dont_inherit=True)
        self.title_owners = []
        for node in tree.body:
            if isinstance(node,ast.FunctionDef):self._remember(self.title_module,node.name,node,plain)
        derived = compile(_title_tree(tree),self.title_module.__file__,'exec',dont_inherit=True)
        self.title_namespace = dict(vars(self.title_module))
        self.title_views = {}
        for name in VIEW_SPECS:
            original = getattr(self.title_module,name)
            view = FunctionType(_top_code(derived,name),self.title_namespace,name,original.__defaults__,None)
            view.__kwdefaults__,view.__annotations__ = original.__kwdefaults__,dict(original.__annotations__)
            if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                raise ValueError('one complete closure-free title generator required: '+name)
            self.title_views[name] = view
        aliases = {'_title_view_'+name:view for name,view in self.title_views.items()}
        aliases['_title_service'] = self._service
        for name,value in aliases.items():
            if name in self.title_namespace:raise ValueError('title continuation alias must not shadow original source')
            self.title_namespace[name] = value
        self.title_bindings = dict(aliases)
        # Retain every function-valued original global used by the private
        # module too: private namespace mutation must not bypass source checks.
        self.title_namespace_functions = {name:(value,value.__code__) for name,value in vars(self.title_module).items()
            if type(value)is FunctionType}
        self.title_view_owners = {name:(view,view.__code__) for name,view in self.title_views.items()}
        self.title_service_owners = {name:(self.battle_views['services',name],self.battle_views['services',name].__code__)
            for name in SERVICE_NAMES}
        for path,expected in EXPECTED_REUSED_ASTS.items():
            module = importlib.import_module(path)
            current = ast.parse(inspect.getsource(module),filename=module.__file__)
            code = compile(current,module.__file__,'exec',dont_inherit=True)
            nodes = {node.name:node for node in current.body if isinstance(node,ast.FunctionDef)}
            for name,source_ast in expected.items():
                if name not in nodes or _dump(nodes[name])!=source_ast:
                    raise ValueError('complete synchronous title dependency differs: '+name)
                self._remember(module,name,nodes[name],code)
        # The transition's actual355DA/3C34 child owns661D4/355F0. Reuse
        # the already registered four complete portrait owners, not a copy.
        from . import roster_panel_steps
        if _dump(ast.parse(inspect.getsource(roster_panel_steps)))!=ROSTER_REGISTRY_MODULE_AST:
            raise ValueError('existing exact roster/portrait source registration required')
        registry_tree = ast.parse(inspect.getsource(roster_panel_steps))
        registry_values = [ast.literal_eval(node.value) for node in registry_tree.body
            if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)
            and node.targets[0].id=='EXPECTED_REUSED_SOURCE']
        if len(registry_values)!=1 or roster_panel_steps.EXPECTED_REUSED_SOURCE!=registry_values[0]:
            raise ValueError('actual existing portrait registry must retain its source literal')
        portrait = importlib.import_module(REGISTERED_PORTRAIT_MODULE)
        portrait_tree = ast.parse(inspect.getsource(portrait),filename=portrait.__file__)
        portrait_code = compile(portrait_tree,portrait.__file__,'exec',dont_inherit=True)
        for name in REGISTERED_PORTRAIT_NAMES:
            text = roster_panel_steps.EXPECTED_REUSED_SOURCE[REGISTERED_PORTRAIT_MODULE][name]
            node = next(node for node in portrait_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
            if _dump(node)!=_dump(ast.parse(text).body[0]):raise ValueError('registered complete title portrait dependency differs')
            self._remember(portrait,name,node,portrait_code)

    def _remember(self,module,name,node,compiled):
        owner = getattr(module,name)
        if (type(owner)is not FunctionType or owner.__globals__ is not vars(module)
                or owner.__module__!=module.__name__ or owner.__name__!=name
                or owner.__closure__ is not None or owner.__code__.co_freevars
                or _code_shape(owner.__code__)!=_code_shape(_top_code(compiled,name))):
            raise ValueError('actual complete unwrapped title dependency required: '+name)
        self.title_owners.append((module,name,owner,owner.__code__))

    def require_current(self,state):
        super().require_current(state)
        if hasattr(self,'title_owners'):
            for module,name,owner,code in self.title_owners:
                if getattr(module,name)is not owner or owner.__code__ is not code:
                    raise ValueError('actual title dependency changed: '+name)
        if hasattr(self,'title_view_owners'):
            if self.title_views.keys()!=self.title_view_owners.keys():raise ValueError('finite title view set changed')
            for name,(owner,code) in self.title_view_owners.items():
                if self.title_views[name]is not owner or owner.__code__ is not code:
                    raise ValueError('actual complete title continuation changed: '+name)
            for name,value in self.title_bindings.items():
                if self.title_namespace.get(name)is not value:raise ValueError('private title continuation binding changed')
            for name,(owner,code) in self.title_namespace_functions.items():
                if self.title_namespace.get(name)is not owner or owner.__code__ is not code:
                    raise ValueError('private original title dependency binding changed: '+name)
            for name,(owner,code) in self.title_service_owners.items():
                if self.battle_views['services',name]is not owner or owner.__code__ is not code:
                    raise ValueError('same inherited complete title service view required: '+name)

    def _service(self,state,frame,name):
        self.require_current(state)
        if name not in SERVICE_NAMES:raise ValueError('only three actual complete title services admitted')
        # _title_child_fields already pushed its original return LONG. These
        # existing service views execute that entered child, never another CALL.
        return (yield from self._message_waits(self.battle_views['services',name](SceneRefreshMemory(state),frame)))

    def _display_child(self,state,frame,target,continuation):
        self.require_current(state)
        if target in MAIN_ENTRIES:
            if continuation!=0x3CE:raise MovementContinuationBoundary(target,frame,'title Main requires actual3CE LONG')
            return (yield from self.title_views[MAIN_ENTRIES[target]](state,frame))
        return (yield from super()._display_child(state,frame,target,continuation))

    def main_scene_call(self,state,frame,target,continuation):
        if target not in MAIN_ENTRIES:return (yield from super().main_scene_call(state,frame,target,continuation))
        self.require_current(state)
        if self._started or continuation!=0x3CE:raise ValueError('one actual indexed title Main invocation required')
        self._started = True
        return (yield from self.views['display','display_call_fields'](state,frame,target,continuation))
