"""Complete Main418/41C/4B8 command panels with their actual nested waits.

All original algorithms and finite complete views are inherited. Only the
three real AF48 returns and the already-entered30A74 shared message are wired.
"""
import ast
import importlib
import inspect
from types import CodeType, FunctionType

from .battle_trigger_steps import BattleScenePrograms, _dump, _code_shape, _top_code
from .contexts_services import SceneRefreshMemory
from .message_scene_steps import GameplayMessageScenePrograms
from .compiler_message_scene_steps import EXPECTED_MODULE_AST as SHARED_SOURCE_AST
from ..high_level_main_flows.compiler_command_message_steps import (
    EXPECTED_MODULE_AST as COMMAND_SOURCE_AST, EXPECTED_OWNER_ASTS)


MAIN_ENTRIES = {0x418:'initialize_city_detail_panel_fields',
    0x41C:'initialize_city_command_panel_fields',
    0x4B8:'initialize_campaign_audio_scene_fields'}
REFRESH_PAIRS = ((0xAF48,0xC9A4),(0xAF48,0xCD70),(0xAF48,0x592))
OWNER_NAMES = {
    'main': ('initialize_city_detail_panel_fields','initialize_city_command_panel_fields',
        'initialize_campaign_audio_scene_fields','_campaign_call_fields'),
    'commands': ('draw_command_cost_panel_frame_fields','draw_command_cost_panel_alternate_1_frame_fields',
        'draw_diplomacy_parameter_panel_alternate_2_frame_fields','_campaign_ui_call_fields'),
}


def _registered_module_bindings(module, expected_ast):
    """Use existing exact registration; pin every actual local callable owner."""
    tree = ast.parse(inspect.getsource(module),filename=module.__file__)
    if _dump(tree)!=expected_ast:
        raise ValueError('complete existing registered command/shared source required')
    plain = compile(tree,module.__file__,'exec',dont_inherit=True)
    bindings = []
    for node in tree.body:
        if isinstance(node,ast.FunctionDef):
            owner = vars(module).get(node.name)
            if (type(owner)is not FunctionType or owner.__globals__ is not vars(module)
                    or owner.__module__!=module.__name__ or owner.__name__!=node.name
                    or owner.__closure__ is not None or owner.__code__.co_freevars
                    or _code_shape(owner.__code__)!=_code_shape(_top_code(plain,node.name))):
                raise ValueError('actual registered command/shared function required: '+node.name)
            bindings.append((module,node.name,owner,owner.__code__))
        elif isinstance(node,ast.ClassDef):
            owner = vars(module).get(node.name)
            if type(owner)is not type or owner.__module__!=module.__name__ or owner.__name__!=node.name:
                raise ValueError('actual registered command/shared class required: '+node.name)
            bindings.append((module,node.name,owner,None))
            class_code = _top_code(plain,node.name)
            for member in node.body:
                if not isinstance(member,ast.FunctionDef):continue
                actual = vars(owner).get(member.name)
                codes = [code for code in class_code.co_consts if type(code)is CodeType
                    and code.co_name==member.name and code.co_qualname==node.name+'.'+member.name]
                if (member.decorator_list or len(codes)!=1 or type(actual)is not FunctionType
                        or actual.__globals__ is not vars(module) or actual.__module__!=module.__name__
                        or actual.__qualname__!=node.name+'.'+member.name or actual.__closure__ is not None
                        or actual.__code__.co_freevars or _code_shape(actual.__code__)!=_code_shape(codes[0])):
                    raise ValueError('actual complete registered command/shared method required: '+member.name)
                bindings.append((owner,member.name,actual,actual.__code__))
    return tuple(bindings)


class CommandPanelScenePrograms(BattleScenePrograms):
    """Keep the existing full parent/view graph and its real physical CALLs."""

    def __init__(self,state):
        super().__init__(state)
        from ..high_level_main_flows import command_message_steps
        from . import message_scene_steps
        self.panel_registered = (
            _registered_module_bindings(command_message_steps,COMMAND_SOURCE_AST)
            +_registered_module_bindings(message_scene_steps,SHARED_SOURCE_AST))
        if (command_message_steps.CommandMessagePrograms not in type(self).__mro__
                or message_scene_steps.GameplayMessageScenePrograms is not GameplayMessageScenePrograms
                or any(command_message_steps.MAIN_MESSAGE_ENTRIES.get(target)!=name
                    for target,name in MAIN_ENTRIES.items())):
            raise ValueError('actual inherited command parents and exact shared message class required')
        self.panel_modules = {group:importlib.import_module(path) for group,path in (
            ('main','tools.high_level_main_flows.business_main'),
            ('commands','tools.high_level_main_flows.business_commands'))}
        self.panel_owners = []
        for group,names in OWNER_NAMES.items():
            module = self.panel_modules[group]
            tree = ast.parse(inspect.getsource(module),filename=module.__file__)
            plain = compile(tree,module.__file__,'exec',dont_inherit=True)
            nodes = {node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
            for name in names:
                owner = getattr(module,name)
                if (name not in nodes or _dump(nodes[name])!=EXPECTED_OWNER_ASTS[group][name]
                        or type(owner)is not FunctionType or owner.__globals__ is not vars(module)
                        or owner.__module__!=module.__name__ or owner.__name__!=name
                        or owner.__closure__ is not None or owner.__code__.co_freevars
                        or _code_shape(owner.__code__)!=_code_shape(_top_code(plain,name))):
                    raise ValueError('complete current registered command-panel owner required: '+name)
                self.panel_owners.append((module,name,owner,owner.__code__))
        self.panel_shared = GameplayMessageScenePrograms(self)
        self.panel_shared_owner = self.panel_shared

    def require_current(self,state):
        super().require_current(state)
        if hasattr(self,'panel_registered'):
            for owner,name,function,code in self.panel_registered:
                if getattr(owner,name)is not function or code is not None and function.__code__ is not code:
                    raise ValueError('actual command/shared source owner changed: '+name)
        if hasattr(self,'panel_owners'):
            for module,name,owner,code in self.panel_owners:
                if getattr(module,name)is not owner or owner.__code__ is not code:
                    raise ValueError('actual complete command-panel owner changed: '+name)
        # Do not call panel_shared.require_current here: its provider guard
        # deliberately calls this method. Identity checks alone avoid recursion.
        if hasattr(self,'panel_shared_owner') and self.panel_shared is not self.panel_shared_owner:
            raise ValueError('the same actual command-panel shared message instance must remain live')

    def _campaign_child(self,state,frame,target,continuation):
        self.require_current(state)
        if (target,continuation) in REFRESH_PAIRS:
            return (yield from self._refresh(SceneRefreshMemory(state),frame))
        return (yield from super()._campaign_child(state,frame,target,continuation))

    def _scene_message(self,memory,frame):
        self.require_current(memory.state)
        return (yield from self._message_waits(self.panel_shared.program(memory,frame)))
