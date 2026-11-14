"""Original five narrative JMP206 transfers from the live Main4B4 parent.

Private finite views reuse the original story algorithms. A real terminal JMP
unwinds the existing generator, retaining its actual frame, SR and CALL slots.
This module supplies proof of that transfer, never reset/IRQ/device authority.
"""
import ast
import copy
import inspect
import threading
from types import CodeType, FunctionType

from ..high_level_gameplay_flow import repeating_scene_steps as repeating
from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
from ..high_level_main_flows.business_movement_support import _movement_frame
from ..high_level_main_flows.domain import Boundary

RepeatingScenePrograms = repeating.RepeatingScenePrograms
EXPECTED_SOURCE = {'support': {'dispatch_repeating_scene_presentation_fields': 'def '
                                                             'dispatch_repeating_scene_presentation_fields(state: '
                                                             'SceneState, frame: FirstDeploymentFrame) -> '
                                                             'FirstDeploymentFrame:\n'
                                                             '    """3B794 real indexed JMP: enter the five '
                                                             'genuine story-table BRA owners with the same '
                                                             'full frame and caller slot. Unknown computed '
                                                             'targets retain their boundary."""\n'
                                                             '    frame = _resource_cost_frame(state, frame, '
                                                             '243604)\n'
                                                             '    frame = _movement_move(state, frame, '
                                                             "'target_x', state.read(4294934746, 2), 16)\n"
                                                             '    frame = _setup_asl_word_fields(state, '
                                                             "frame, 'target_x', 2)\n"
                                                             '    target = u32(243614 + '
                                                             's16(low16(frame.target_x)))\n'
                                                             '    if target in (243614, 243618, 243622, '
                                                             '243626, 243630):\n'
                                                             '        from '
                                                             '..high_level_scene_flows.business_scene import '
                                                             '_story_known_fields\n'
                                                             '        return '
                                                             '_story_known_fields(SceneRefreshMemory(state), '
                                                             'frame, target)\n'
                                                             '    raise MovementContinuationBoundary(target, '
                                                             "frame, 'computed presentation JMP entry "
                                                             "requires its genuine owner facade')"},
 'story': {'dispatch_prologue_story_fields': 'def dispatch_prologue_story_fields(memory: SceneRefreshMemory, '
                                             'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                             '    return _story_dispatch_fields(memory, frame, 243644)',
           'dispatch_departure_story_fields': 'def dispatch_departure_story_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    return _story_dispatch_fields(memory, frame, 246172)',
           'dispatch_interlude_story_fields': 'def dispatch_interlude_story_fields(memory: '
                                              'SceneRefreshMemory, frame: FirstDeploymentFrame) -> '
                                              'FirstDeploymentFrame:\n'
                                              '    return _story_dispatch_fields(memory, frame, 248186)',
           'dispatch_arrival_story_fields': 'def dispatch_arrival_story_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    return _story_dispatch_fields(memory, frame, 248484)',
           'dispatch_finale_story_fields': 'def dispatch_finale_story_fields(memory: SceneRefreshMemory, '
                                           'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                           '    return _story_dispatch_fields(memory, frame, 250236)',
           '_story_dispatch_fields': 'def _story_dispatch_fields(memory: SceneRefreshMemory, frame: '
                                     'FirstDeploymentFrame, table: Long) -> FirstDeploymentFrame:\n'
                                     '    """Original live stage WORD selects actual four-byte BRA CODE, not '
                                     'a fake callback."""\n'
                                     '    memory.frame(frame)\n'
                                     "    frame = _story_ram_move_fields(memory, frame, 'target_x', 33002)\n"
                                     "    frame = _scene_render_asl_word(memory, frame, 'target_x', "
                                     'low16(frame.target_x), 2)\n'
                                     '    return _story_known_fields(memory, frame, table + '
                                     's16(low16(frame.target_x)))',
           '_story_known_fields': 'def _story_known_fields(memory: SceneRefreshMemory, frame: FirstDeploymentFrame, target: Long) -> FirstDeploymentFrame:\n    """Genuine complete story children, including402C2 live officer-name rendering. The real caller already owns the LONG; same-state full frame and all actual DATA/device boundaries survive."""\n    memory.frame(frame)\n    if target == 26570:\n        from ..high_level_main_flows.business_lowbank import poll_controller_with_z80_bus_fields\n        return poll_controller_with_z80_bus_fields(memory.state, frame)\n    if target == 18754:\n        from ..high_level_remaining_flows.business_lowbank import lowbank_process_device_control_9_fields\n        return lowbank_process_device_control_9_fields(memory.state, frame)\n    if target == 518:\n        from ..high_level_main_flows.business_boot import reset_console_frame_fields\n        return reset_console_frame_fields(memory.state, frame)\n    if target == 238902:\n        return transfer_story_plane_dma_fields(memory, frame)\n    elif target == 239772:\n        return transfer_story_overlay_dma_fields(memory, frame)\n    elif target == 243614:\n        return dispatch_prologue_story_fields(memory, frame)\n    elif target == 243618:\n        return dispatch_departure_story_fields(memory, frame)\n    elif target == 243622:\n        return dispatch_arrival_story_fields(memory, frame)\n    elif target == 243626:\n        return dispatch_finale_story_fields(memory, frame)\n    elif target == 243630:\n        return dispatch_interlude_story_fields(memory, frame)\n    elif target == 243644:\n        return initialize_prologue_story_fields(memory, frame)\n    elif target == 243648:\n        return reveal_prologue_caption_fields(memory, frame)\n    elif target == 243652:\n        return wait_prologue_portrait_fields(memory, frame)\n    elif target == 243656:\n        return confirm_prologue_first_page_fields(memory, frame)\n    elif target == 243660:\n        return wait_prologue_second_page_fields(memory, frame)\n    elif target == 243664:\n        return reveal_prologue_second_portrait_fields(memory, frame)\n    elif target == 243668:\n        return confirm_prologue_second_page_fields(memory, frame)\n    elif target == 243672:\n        return begin_prologue_closing_caption_fields(memory, frame)\n    elif target == 243676:\n        return finish_prologue_closing_caption_fields(memory, frame)\n    elif target == 243680:\n        return confirm_prologue_exit_fields(memory, frame)\n    elif target == 243920:\n        return draw_prologue_portrait_fields(memory, frame)\n    elif target == 244400:\n        return animate_prologue_portrait_fields(memory, frame)\n    elif target == 244454:\n        return cycle_prologue_colors_fields(memory, frame)\n    elif target == 244674:\n        return select_prologue_sprite_fields(memory, frame)\n    elif target == 246172:\n        return initialize_departure_story_fields(memory, frame)\n    elif target == 246176:\n        return reveal_departure_caption_fields(memory, frame)\n    elif target == 246180:\n        return confirm_departure_first_page_fields(memory, frame)\n    elif target == 246184:\n        return wait_departure_second_page_fields(memory, frame)\n    elif target == 246188:\n        return confirm_departure_second_page_fields(memory, frame)\n    elif target == 246192:\n        return begin_departure_closing_caption_fields(memory, frame)\n    elif target == 246196:\n        return finish_departure_closing_caption_fields(memory, frame)\n    elif target == 246200:\n        return confirm_departure_exit_fields(memory, frame)\n    elif target == 246330:\n        return load_departure_tile_rows_fields(memory, frame)\n    elif target == 246402:\n        return write_departure_tile_row_fields(memory, frame)\n    elif target == 246692:\n        return animate_departure_three_layers_fields(memory, frame)\n    elif target == 246942:\n        return animate_departure_transition_fields(memory, frame)\n    elif target == 247238:\n        return animate_departure_closing_layers_fields(memory, frame)\n    elif target == 247500:\n        return select_departure_sprite_fields(memory, frame)\n    elif target == 248186:\n        return initialize_interlude_story_fields(memory, frame)\n    elif target == 248190:\n        return reveal_interlude_caption_fields(memory, frame)\n    elif target == 248194:\n        return confirm_interlude_exit_fields(memory, frame)\n    elif target == 248484:\n        return initialize_arrival_story_fields(memory, frame)\n    elif target == 248488:\n        return reveal_arrival_caption_fields(memory, frame)\n    elif target == 248492:\n        return confirm_arrival_first_page_fields(memory, frame)\n    elif target == 248496:\n        return wait_arrival_second_page_fields(memory, frame)\n    elif target == 248500:\n        return confirm_arrival_second_page_fields(memory, frame)\n    elif target == 248504:\n        return begin_arrival_closing_caption_fields(memory, frame)\n    elif target == 248508:\n        return finish_arrival_closing_caption_fields(memory, frame)\n    elif target == 248512:\n        return confirm_arrival_exit_fields(memory, frame)\n    elif target == 248766:\n        return animate_arrival_portrait_fields(memory, frame)\n    elif target == 248962:\n        return animate_arrival_zoom_fields(memory, frame)\n    elif target == 249240:\n        return animate_arrival_closing_portrait_fields(memory, frame)\n    elif target == 249352:\n        return select_arrival_sprite_fields(memory, frame)\n    elif target == 250236:\n        return initialize_finale_story_fields(memory, frame)\n    elif target == 250240:\n        return reveal_finale_caption_fields(memory, frame)\n    elif target == 250244:\n        return confirm_finale_first_page_fields(memory, frame)\n    elif target == 250248:\n        return wait_finale_scroll_fields(memory, frame)\n    elif target == 250252:\n        return advance_finale_scroll_fields(memory, frame)\n    elif target == 250256:\n        return finish_finale_closing_caption_fields(memory, frame)\n    elif target == 250260:\n        return confirm_finale_exit_fields(memory, frame)\n    elif target == 250496:\n        return animate_finale_portrait_fields(memory, frame)\n    elif target == 250694:\n        return move_finale_actor_diagonally_fields(memory, frame)\n    elif target == 250908:\n        return animate_finale_closing_portrait_fields(memory, frame)\n    elif target == 250972:\n        return select_finale_sprite_fields(memory, frame)\n    elif target == 250976:\n        return select_finale_sprite_with_attributes_fields(memory, frame)\n    elif target == 262058:\n        return advance_story_text_stream_fields(memory, frame)\n    elif target == 262398:\n        return append_story_officer_number_fields(memory, frame)\n    elif target == 262526:\n        return append_story_counter_pair_fields(memory, frame)\n    elif target == 262670:\n        return append_story_counter_triple_fields(memory, frame)\n    elif target == 240160:\n        return begin_scene_palette_darken_fields(memory, frame)\n    elif target == 240184:\n        from ..high_level_dynamic_flows.business_early_phase import begin_scene_palette_lighten_fields\n        return begin_scene_palette_lighten_fields(memory, frame)\n    elif target == 240334:\n        return read_vdp_plane_rle_rows_fields(memory, frame)\n    elif target == 242352:\n        return set_vram_write_address_fields(memory, frame)\n    elif target == 240532:\n        return copy_scene_palette_variant_fields(memory, frame)\n    elif target == 44682:\n        return decode_glyph_rows_to_buffers_fields(memory, frame)\n    elif target == 242392:\n        from ..high_level_dynamic_flows.business_early_phase import encode_six_decimal_digits_fields\n        return encode_six_decimal_digits_fields(memory, frame)\n    if target == 262850:\n        from ..high_level_dynamic_flows.business_actions import upload_object_officer_name_frame_fields\n        return upload_object_officer_name_frame_fields(memory.state, frame)\n    if target == 0x3AAC2:\n        from ..high_level_main_flows.business_scene_support import decode_high_plane_rows_fields\n        return decode_high_plane_rows_fields(memory.state, frame)\n    raise SceneRefreshBoundary(target, frame, None)\n',
           'confirm_prologue_exit_fields': 'def confirm_prologue_exit_fields(memory: SceneRefreshMemory, '
                                           'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                           '    """Original 3B7E0 complete story role; BRA prefixes add no '
                                           'slot."""\n'
                                           '    memory.frame(frame)\n'
                                           '    frame = _story_call_fields(memory, frame, 244400, 244656)\n'
                                           '    return _story_exit_fields(memory, frame)',
           'confirm_departure_exit_fields': 'def confirm_departure_exit_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    """Original 3C1B8 complete story role; BRA prefixes add no '
                                            'slot."""\n'
                                            '    memory.frame(frame)\n'
                                            '    frame = _story_call_fields(memory, frame, 247238, 247482)\n'
                                            '    return _story_exit_fields(memory, frame)',
           'confirm_interlude_exit_fields': 'def confirm_interlude_exit_fields(memory: SceneRefreshMemory, '
                                            'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                            '    """Original 3C982 complete story role; BRA prefixes add no '
                                            'slot."""\n'
                                            '    memory.frame(frame)\n'
                                            '    frame = _story_call_fields(memory, frame, 246692, 248456)\n'
                                            '    return _story_exit_fields(memory, frame)',
           'confirm_arrival_exit_fields': 'def confirm_arrival_exit_fields(memory: SceneRefreshMemory, '
                                          'frame: FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                          '    """Original 3CAC0 complete story role; BRA prefixes add no '
                                          'slot."""\n'
                                          '    memory.frame(frame)\n'
                                          '    return _story_exit_fields(memory, frame)',
           'confirm_finale_exit_fields': 'def confirm_finale_exit_fields(memory: SceneRefreshMemory, frame: '
                                         'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                         '    """Original 3D194 complete story role; BRA prefixes add no '
                                         'slot."""\n'
                                         '    memory.frame(frame)\n'
                                         '    frame = _story_call_fields(memory, frame, 250908, 250954)\n'
                                         '    return _story_exit_fields(memory, frame)',
           '_story_exit_fields': 'def _story_exit_fields(memory: SceneRefreshMemory, frame: '
                                 'FirstDeploymentFrame) -> FirstDeploymentFrame:\n'
                                 '    frame, pressed = _story_pressed_fields(memory, frame)\n'
                                 '    if pressed:\n'
                                 '        return _story_known_fields(memory, frame, 518)\n'
                                 '    return memory.sync_status(frame)'}}
EXPECTED_BASE = {'_dump': 'def _dump(node):\n    return ast.dump(node, include_attributes=False)',
 '_code_shape': 'def _code_shape(code):\n'
                "    return tuple((getattr(code, name) for name in ('co_code', 'co_names', 'co_varnames', "
                "'co_argcount', 'co_posonlyargcount', 'co_kwonlyargcount', 'co_flags', 'co_freevars', "
                "'co_cellvars'))) + (tuple((_code_shape(value) if type(value) is CodeType else value for "
                'value in code.co_consts)),)',
 '_code_at': 'def _code_at(code, name):\n'
             '    found = [item for item in code.co_consts if type(item) is CodeType and item.co_name == '
             'name]\n'
             '    if len(found) != 1:\n'
             "        raise ValueError('one complete original code owner required: ' + name)\n"
             '    return found[0]',
 '_cooperative_tree': 'def _cooperative_tree(group, original_tree):\n'
                      '    """Exact finite call/progress changes; inverse every whole FN and module."""\n'
                      '    result = copy.deepcopy(original_tree)\n'
                      '    inverses = {}\n'
                      '    for index, node in enumerate(original_tree.body):\n'
                      '        if not isinstance(node, ast.FunctionDef) or node.name not in '
                      'VIEW_SPECS[group]:\n'
                      '            continue\n'
                      '        if _dump(node) != '
                      '_dump(ast.parse(EXPECTED_SOURCE[group][node.name]).body[0]):\n'
                      "            raise ValueError('reviewed complete repeating-scene function changed: ' + "
                      'node.name)\n'
                      '        if any((isinstance(n, (ast.Yield, ast.YieldFrom)) for n in ast.walk(node))):\n'
                      "            raise ValueError('original repeating-scene business owner must remain "
                      "synchronous')\n"
                      '        spec = VIEW_SPECS[group][node.name]\n'
                      "        counts = {name: 0 for name in spec['calls']}\n"
                      '        changes = []\n'
                      '        waits = []\n'
                      "        old_wait = ast.parse(spec['wait'][0]).body[0] if spec['wait'] else None\n"
                      "        new_wait = ast.parse(spec['wait'][1]).body[0] if spec['wait'] else None\n"
                      '\n'
                      '        class Lift(ast.NodeTransformer):\n'
                      '\n'
                      '            def visit_Call(self, item):\n'
                      '                item = self.generic_visit(item)\n'
                      '                if isinstance(item.func, ast.Name) and item.func.id in counts:\n'
                      '                    before = copy.deepcopy(item)\n'
                      '                    name = item.func.id\n'
                      '                    counts[name] += 1\n'
                      "                    item.func.id = spec['calls'][name][1]\n"
                      '                    after = ast.copy_location(ast.YieldFrom(value=item), item)\n'
                      '                    changes.append((before, copy.deepcopy(after)))\n'
                      '                    return after\n'
                      '                return item\n'
                      '\n'
                      '            def visit_Expr(self, item):\n'
                      '                if old_wait is not None and _dump(item) == _dump(old_wait):\n'
                      '                    waits.append(item)\n'
                      '                    return ast.copy_location(copy.deepcopy(new_wait), item)\n'
                      '                return self.generic_visit(item)\n'
                      '        derived = Lift().visit(copy.deepcopy(node))\n'
                      "        if counts != {name: rule[0] for name, rule in spec['calls'].items()} or "
                      "len(waits) != (1 if spec['wait'] else 0):\n"
                      "            raise ValueError('exact original repeating-scene call/wait count differs: "
                      "' + node.name)\n"
                      '        remaining = list(changes)\n'
                      '\n'
                      '        class Inverse(ast.NodeTransformer):\n'
                      '\n'
                      '            def visit_Assign(self, item):\n'
                      '                if new_wait is not None and _dump(item) == _dump(new_wait):\n'
                      '                    return copy.deepcopy(old_wait)\n'
                      '                return self.generic_visit(item)\n'
                      '\n'
                      '            def visit_YieldFrom(self, item):\n'
                      '                for position, (before, after) in enumerate(remaining):\n'
                      '                    if _dump(item) == _dump(after):\n'
                      '                        remaining.pop(position)\n'
                      '                        return copy.deepcopy(before)\n'
                      "                raise ValueError('unadmitted repeating-scene cooperative call')\n"
                      '        inverse = Inverse().visit(copy.deepcopy(derived))\n'
                      '        if remaining or _dump(inverse) != _dump(node):\n'
                      "            raise ValueError('complete original repeating-scene function inverse "
                      "differs')\n"
                      '        result.body[index] = derived\n'
                      '        inverses[index] = inverse\n'
                      '    if len(inverses) != len(VIEW_SPECS[group]):\n'
                      "        raise ValueError('every finite repeating-scene view required')\n"
                      '    restored = copy.deepcopy(result)\n'
                      '    for index, node in inverses.items():\n'
                      '        restored.body[index] = node\n'
                      '    if _dump(restored) != _dump(original_tree):\n'
                      "        raise ValueError('complete original business module inverse differs')\n"
                      '    return ast.fix_missing_locations(result)',
 '_pin_base': 'def _pin_base():\n'
              '    """Pin the actual reviewed base class, methods and complete-module codes."""\n'
              '    if BattleScenePrograms is not _battle.BattleScenePrograms or '
              'RepeatingScenePrograms.__bases__ != (BattleScenePrograms,):\n'
              "        raise ValueError('one actual unchanged BattleScenePrograms base required')\n"
              '    tree = ast.parse(inspect.getsource(_battle), filename=_battle.__file__)\n'
              '    candidates = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name '
              "== 'BattleScenePrograms']\n"
              '    if len(candidates) != 1 or _dump(candidates[0]) != '
              "_dump(ast.parse(EXPECTED_BASE['BattleScenePrograms']).body[0]):\n"
              "        raise ValueError('complete reviewed BattleScenePrograms source changed')\n"
              "    compiled = compile(tree, _battle.__file__, 'exec', dont_inherit=True)\n"
              "    cls_code = _code_at(compiled, 'BattleScenePrograms')\n"
              '    methods = {}\n'
              '    for method in candidates[0].body:\n'
              '        if not isinstance(method, ast.FunctionDef):\n'
              '            continue\n'
              '        descriptor = vars(BattleScenePrograms).get(method.name)\n'
              '        function = descriptor.__func__ if type(descriptor) is staticmethod else descriptor\n'
              '        if type(function) is not FunctionType or function.__globals__ is not vars(_battle) or '
              "function.__module__ != _battle.__name__ or (function.__qualname__ != 'BattleScenePrograms.' + "
              'method.name) or (_code_shape(function.__code__) != _code_shape(_code_at(cls_code, '
              'method.name))):\n'
              "            raise ValueError('actual complete-module battle base method required: ' + "
              'method.name)\n'
              '        methods[method.name] = (function, function.__code__)\n'
              '    functions = {}\n'
              '    for name, source in EXPECTED_BASE.items():\n'
              "        if name == 'BattleScenePrograms':\n"
              '            continue\n'
              '        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]\n'
              '        function = getattr(_battle, name)\n'
              '        if len(nodes) != 1 or _dump(nodes[0]) != _dump(ast.parse(source).body[0]) or '
              'type(function) is not FunctionType or (function.__globals__ is not vars(_battle)) or '
              '(_code_shape(function.__code__) != _code_shape(_code_at(compiled, name))):\n'
              "            raise ValueError('actual complete battle base utility required: ' + name)\n"
              '        functions[name] = (function, function.__code__)\n'
              '    return (methods, functions)',
 'RepeatingScenePrograms': 'class RepeatingScenePrograms(BattleScenePrograms):\n'
                           '    """Actual Main4B4/3CE and never-reentered3B732/580, on the same Scene."""\n'
                           '\n'
                           '    def __init__(self, state):\n'
                           '        self._repeat_base_methods, self._repeat_base_functions = _pin_base()\n'
                           '        self._repeat_base_class = BattleScenePrograms\n'
                           '        self._repeat_class = RepeatingScenePrograms\n'
                           '        self._repeat_methods = {name: (function, function.__code__) for name, '
                           'function in vars(RepeatingScenePrograms).items() if type(function) is '
                           'FunctionType}\n'
                           "        self._repeat_base_methods['__init__'][0](self, state)\n"
                           '        import importlib\n'
                           '        self.repeat_modules = {group: importlib.import_module(path) for group, '
                           'path in MODULE_PATHS.items()}\n'
                           '        self.repeat_originals = {}\n'
                           '        self.repeat_original_codes = {}\n'
                           '        self.repeat_views = {}\n'
                           '        self.repeat_namespaces = {}\n'
                           '        self.repeat_bindings = {}\n'
                           '        for group, module in self.repeat_modules.items():\n'
                           '            tree = ast.parse(inspect.getsource(module), '
                           'filename=module.__file__)\n'
                           '            nodes = {n.name: n for n in tree.body if isinstance(n, '
                           'ast.FunctionDef)}\n'
                           "            plain = compile(tree, module.__file__, 'exec', dont_inherit=True)\n"
                           '            for name, source in EXPECTED_SOURCE[group].items():\n'
                           '                function = getattr(module, name)\n'
                           '                if name not in nodes or _dump(nodes[name]) != '
                           '_dump(ast.parse(source).body[0]) or type(function) is not FunctionType or '
                           '(function.__globals__ is not vars(module)) or (function.__module__ != '
                           'module.__name__) or (function.__name__ != name) or (function.__closure__ is not '
                           'None) or function.__code__.co_freevars or (_code_shape(function.__code__) != '
                           '_code_shape(_code_at(plain, name))):\n'
                           "                    raise ValueError('actual complete repeating-scene dependency "
                           "required: ' + name)\n"
                           '                self.repeat_originals[group, name] = function\n'
                           '                self.repeat_original_codes[group, name] = function.__code__\n'
                           '            derived = compile(_cooperative_tree(group, tree), module.__file__, '
                           "'exec', dont_inherit=True)\n"
                           '            namespace = dict(vars(module))\n'
                           '            self.repeat_namespaces[group] = namespace\n'
                           '            for name in VIEW_SPECS[group]:\n'
                           '                original = self.repeat_originals[group, name]\n'
                           '                view = FunctionType(_code_at(derived, name), namespace, name, '
                           'original.__defaults__, None)\n'
                           '                view.__kwdefaults__ = original.__kwdefaults__\n'
                           '                view.__annotations__ = dict(original.__annotations__)\n'
                           '                if not inspect.isgeneratorfunction(view):\n'
                           "                    raise ValueError('whole repeating-scene view must be "
                           "cooperative')\n"
                           '                self.repeat_views[group, name] = view\n'
                           '        self._repeat_view_owners = dict(self.repeat_views)\n'
                           '        self._repeat_view_codes = {key: view.__code__ for key, view in '
                           'self.repeat_views.items()}\n'
                           "        aliases = {'_repeat_call': self.repeat_views['support', "
                           "'_aux_text_call_fields'], '_repeat_campaign_call': self.views['main', "
                           "'_campaign_call_fields'], '_repeat_clear_video': self._clear_video, "
                           "'_repeat_enqueue_sound': self._enqueue_sound, '_repeat_wait_sound': "
                           "self.repeat_views['services', 'wait_for_scene_sound_byte_fields'], "
                           "'_repeat_wait': self._repeat_wait}\n"
                           '        for group, namespace in self.repeat_namespaces.items():\n'
                           '            for name, value in aliases.items():\n'
                           '                if name in namespace:\n'
                           "                    raise ValueError('private repeating-scene alias must not "
                           "shadow original owner')\n"
                           '                namespace[name] = value\n'
                           '                self.repeat_bindings[group, name] = value\n'
                           '        self.repeat_admissions = dict(whole_cooperative_views=4, '
                           'source_owners=sum((len(v) for v in EXPECTED_SOURCE.values())), '
                           'physical_outer_slots=[974, 1408], sound_wait_return=243570, '
                           'prefix_reentered=False, new_wait_types=0)\n'
                           '\n'
                           '    def _require_repeat_base(self):\n'
                           '        if BattleScenePrograms is not self._repeat_base_class or '
                           '_battle.BattleScenePrograms is not self._repeat_base_class or '
                           'RepeatingScenePrograms is not self._repeat_class or '
                           '(RepeatingScenePrograms.__bases__ != (self._repeat_base_class,)):\n'
                           "            raise ValueError('actual repeating-scene base class changed')\n"
                           '        for name, (function, code) in self._repeat_methods.items():\n'
                           '            if vars(self._repeat_class).get(name) is not function or '
                           'function.__code__ is not code:\n'
                           "                raise ValueError('actual repeating-scene coordinator method "
                           "changed: ' + name)\n"
                           '        for name, (function, code) in self._repeat_base_methods.items():\n'
                           '            descriptor = vars(self._repeat_base_class).get(name)\n'
                           '            actual = descriptor.__func__ if type(descriptor) is staticmethod '
                           'else descriptor\n'
                           '            if actual is not function or function.__code__ is not code:\n'
                           "                raise ValueError('actual battle base method changed across "
                           "repeating wait: ' + name)\n"
                           '        for name, (function, code) in self._repeat_base_functions.items():\n'
                           '            if getattr(_battle, name) is not function or function.__code__ is '
                           'not code:\n'
                           "                raise ValueError('actual battle base utility changed across "
                           "repeating wait: ' + name)\n"
                           '\n'
                           '    def require_current(self, state):\n'
                           '        self._require_repeat_base()\n'
                           "        self._repeat_base_methods['require_current'][0](self, state)\n"
                           "        if not hasattr(self, 'repeat_originals'):\n"
                           '            return\n'
                           '        for (group, name), original in self.repeat_originals.items():\n'
                           '            if getattr(self.repeat_modules[group], name) is not original or '
                           'original.__code__ is not self.repeat_original_codes[group, name]:\n'
                           "                raise ValueError('actual repeating-scene dependency changed: ' + "
                           'name)\n'
                           '        if self.repeat_views.keys() != self._repeat_view_owners.keys():\n'
                           "            raise ValueError('finite repeating-scene graph changed')\n"
                           '        for key, view in self._repeat_view_owners.items():\n'
                           '            if self.repeat_views[key] is not view or view.__code__ is not '
                           'self._repeat_view_codes[key]:\n'
                           "                raise ValueError('whole repeating-scene private view changed: ' "
                           '+ key[1])\n'
                           '        for (group, name), value in self.repeat_bindings.items():\n'
                           '            if self.repeat_namespaces[group].get(name) is not value:\n'
                           "                raise ValueError('private repeating-scene continuation binding "
                           "changed: ' + name)\n"
                           '\n'
                           '    def _repeat_wait(self, memory, frame):\n'
                           '        self.require_current(memory.state)\n'
                           '        if type(memory) is not SceneRefreshMemory:\n'
                           "            raise ValueError('actual Scene refresh memory required')\n"
                           '        frame = memory.sync_status(_movement_frame(memory.state, frame))\n'
                           '        wait = GameplaySceneWait(memory.state, frame, memory.state.sr, '
                           "'scene-sound-byte', 33740).validate()\n"
                           '        returned = (yield wait)\n'
                           '        self.require_current(memory.state)\n'
                           '        returned = _movement_frame(memory.state, returned)\n'
                           '        if returned.stack_cursor.base != frame.stack_cursor.base or '
                           'memory.state.sr != wait.status_word or returned.status != wait.status_word & '
                           '31:\n'
                           "            raise ValueError('actual83CC IRQ must restore the same physical SP "
                           "and complete SR')\n"
                           '        return returned\n'
                           '\n'
                           '    def _forward_waits(self, program):\n'
                           '        """Guard both sides of the reused exact device-view suspensions."""\n'
                           '        first = True\n'
                           '        received = None\n'
                           '        try:\n'
                           '            while True:\n'
                           '                self.require_current(self.state)\n'
                           '                try:\n'
                           '                    waiting = next(program) if first else '
                           'program.send(received)\n'
                           '                except StopIteration as finished:\n'
                           '                    return finished.value\n'
                           '                first = False\n'
                           '                if type(waiting) is not GameplaySceneWait or waiting.state is '
                           'not self.state:\n'
                           "                    raise ValueError('one exact same-Scene reused initialization "
                           "wait required')\n"
                           '                waiting.validate()\n'
                           '                received = (yield waiting)\n'
                           '                self.require_current(self.state)\n'
                           '                if waiting.needs_interrupt or received is not waiting.frame or '
                           'self.state.sr != waiting.status_word:\n'
                           "                    raise ValueError('device progress must retain the actual "
                           "waiting frame and full SR')\n"
                           '        finally:\n'
                           '            program.close()\n'
                           '\n'
                           '    def _clear_video(self, memory, frame):\n'
                           '        self.require_current(memory.state)\n'
                           "        return (yield from self._forward_waits(self.battle_views['services', "
                           "'clear_video_sprite_plane_fields'](memory, frame)))\n"
                           '\n'
                           '    def _enqueue_sound(self, memory, frame, command=None):\n'
                           '        self.require_current(memory.state)\n'
                           "        return (yield from self._forward_waits(self.battle_views['services', "
                           "'enqueue_sound_command_fields'](memory, frame, command)))\n"
                           '\n'
                           '    def _campaign_child(self, state, frame, target, continuation):\n'
                           '        self.require_current(state)\n'
                           '        if (target, continuation) == (243506, 1408):\n'
                           "            return (yield from self.repeat_views['support', "
                           "'run_repeating_scene_presentation_fields'](state, frame))\n"
                           '        return (yield from super()._campaign_child(state, frame, target, '
                           'continuation))\n'
                           '\n'
                           '    def _display_child(self, state, frame, target, continuation):\n'
                           '        self.require_current(state)\n'
                           '        if target == 1204:\n'
                           '            if continuation != 974:\n'
                           "                raise MovementContinuationBoundary(target, frame, 'actual "
                           "Main4B4 requires3CE')\n"
                           "            return (yield from self.repeat_views['main', "
                           "'begin_nonreturning_scripted_scene_fields'](state, frame))\n"
                           '        return (yield from super()._display_child(state, frame, target, '
                           'continuation))\n'
                           '\n'
                           '    def main_scene_call(self, state, frame, target, continuation):\n'
                           '        if target != 1204:\n'
                           '            return (yield from super().main_scene_call(state, frame, target, '
                           'continuation))\n'
                           '        self.require_current(state)\n'
                           '        if self._started or continuation != 974:\n'
                           "            raise ValueError('one actual Main4B4/3CE invocation required')\n"
                           '        self._started = True\n'
                           "        return (yield from self.views['display', 'display_call_fields'](state, "
                           'frame, target, continuation))'}
VIEW_NAMES = {'support': ['dispatch_repeating_scene_presentation_fields'],
 'story': ['dispatch_prologue_story_fields',
           'dispatch_departure_story_fields',
           'dispatch_interlude_story_fields',
           'dispatch_arrival_story_fields',
           'dispatch_finale_story_fields',
           '_story_dispatch_fields',
           '_story_known_fields',
           'confirm_prologue_exit_fields',
           'confirm_departure_exit_fields',
           'confirm_interlude_exit_fields',
           'confirm_arrival_exit_fields',
           'confirm_finale_exit_fields',
           '_story_exit_fields']}
EXIT_SITES = {'confirm_prologue_exit_fields': 244666,
 'confirm_departure_exit_fields': 247492,
 'confirm_interlude_exit_fields': 248466,
 'confirm_arrival_exit_fields': 249344,
 'confirm_finale_exit_fields': 250964}


def _dump(node):
    return ast.dump(node,include_attributes=False)


def _code_at(code,name):
    matches=[value for value in code.co_consts if type(value)is CodeType and value.co_name==name]
    if len(matches)!=1:raise Boundary('one complete lexical narrative code owner required: '+name)
    return matches[0]


def _code_shape(code):
    return tuple(getattr(code,name)for name in ('co_code','co_names','co_varnames',
        'co_argcount','co_posonlyargcount','co_kwonlyargcount','co_flags',
        'co_freevars','co_cellvars'))+(tuple(_code_shape(value)if type(value)is CodeType
            else value for value in code.co_consts),)


def _narrative_tree(group,original):
    """Seven exact expression changes, with every whole FN/module inverted."""
    result=copy.deepcopy(original);inverses={}
    for index,node in enumerate(original.body):
        if not isinstance(node,ast.FunctionDef)or node.name not in VIEW_NAMES[group]:continue
        if _dump(node)!=_dump(ast.parse(EXPECTED_SOURCE[group][node.name]).body[0]):
            raise Boundary('reviewed entire narrative owner changed: '+node.name)
        changes=[]

        class Lift(ast.NodeTransformer):
            def visit_Call(self,item):
                item=self.generic_visit(item)
                if not isinstance(item.func,ast.Name):return item
                name=item.func.id;before=copy.deepcopy(item)
                if group=='support' and node.name=='dispatch_repeating_scene_presentation_fields' and name=='_story_known_fields':
                    item.func.id='_narrative_story'
                elif group=='story' and node.name in EXIT_SITES and name=='_story_exit_fields':
                    if len(item.args)!=2 or item.keywords:
                        raise Boundary('actual complete story exit argument shape required')
                    item.func.id='_narrative_exit';item.args.append(ast.Constant(EXIT_SITES[node.name]))
                elif group=='story' and node.name=='_story_exit_fields' and name=='_story_known_fields':
                    if (len(item.args)!=3 or item.keywords or not isinstance(item.args[2],ast.Constant)
                            or item.args[2].value!=0x206):
                        raise Boundary('only original pressed terminal206 expression is admitted')
                    item.func.id='_narrative_jump'
                else:return item
                changes.append((before,copy.deepcopy(item)));return item

        derived=Lift().visit(copy.deepcopy(node))
        wanted=int((group=='support')or node.name in EXIT_SITES or node.name=='_story_exit_fields')
        if len(changes)!=wanted:raise Boundary('exact original narrative terminal expression count differs')
        remaining=list(changes)

        class Inverse(ast.NodeTransformer):
            def visit_Call(self,item):
                for position,(before,after)in enumerate(remaining):
                    if _dump(item)==_dump(after):remaining.pop(position);return copy.deepcopy(before)
                return self.generic_visit(item)

        inverse=Inverse().visit(copy.deepcopy(derived))
        if remaining or _dump(inverse)!=_dump(node):
            raise Boundary('entire narrative terminal function inverse differs: '+node.name)
        if any(isinstance(value,(ast.Yield,ast.YieldFrom))for value in ast.walk(derived)):
            raise Boundary('original once-per-frame narrative algorithm must remain synchronous')
        result.body[index]=derived;inverses[index]=inverse
    if len(inverses)!=len(VIEW_NAMES[group]):raise Boundary('complete finite narrative source graph required')
    restored=copy.deepcopy(result)
    for index,node in inverses.items():restored.body[index]=node
    if _dump(restored)!=_dump(original):raise Boundary('whole original narrative module inverse differs')
    return ast.fix_missing_locations(result)


def _pin_base():
    """Keep the actual existing Main4B4 source-derived parent, not a copy."""
    if (RepeatingScenePrograms is not repeating.RepeatingScenePrograms
            or NarrativeScenePrograms.__bases__!=(RepeatingScenePrograms,)):
        raise Boundary('actual unchanged repeating-scene base class required')
    tree=ast.parse(inspect.getsource(repeating),filename=repeating.__file__)
    nodes={node.name:node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))}
    compiled=compile(tree,repeating.__file__,'exec',dont_inherit=True)
    methods={};functions={}
    for name,source in EXPECTED_BASE.items():
        if name not in nodes or _dump(nodes[name])!=_dump(ast.parse(source).body[0]):
            raise Boundary('entire reviewed narrative parent source changed: '+name)
        if name=='RepeatingScenePrograms':
            class_code=_code_at(compiled,name)
            for method in nodes[name].body:
                if not isinstance(method,ast.FunctionDef):continue
                function=vars(RepeatingScenePrograms).get(method.name)
                if (type(function)is not FunctionType or function.__globals__ is not vars(repeating)
                        or function.__qualname__!='RepeatingScenePrograms.'+method.name
                        or _code_shape(function.__code__)!=_code_shape(_code_at(class_code,method.name))):
                    raise Boundary('actual complete-module parent method required: '+method.name)
                methods[method.name]=(function,function.__code__)
        else:
            function=getattr(repeating,name)
            if (type(function)is not FunctionType or function.__globals__ is not vars(repeating)
                    or _code_shape(function.__code__)!=_code_shape(_code_at(compiled,name))):
                raise Boundary('actual complete-module parent source utility required: '+name)
            functions[name]=(function,function.__code__)
    return methods,functions


def _pin_own():
    """Match loaded new owner methods to their actual whole-module context."""
    module=inspect.getmodule(NarrativeScenePrograms)
    if module is None or vars(module)is not globals():
        raise Boundary('actual narrative provider module required')
    tree=ast.parse(inspect.getsource(module),filename=module.__file__)
    compiled=compile(tree,module.__file__,'exec',dont_inherit=True);bindings=[]
    for node in tree.body:
        if isinstance(node,ast.ClassDef)and node.name in ('OriginalNarrativeResetJump','NarrativeScenePrograms'):
            cls=getattr(module,node.name);class_code=_code_at(compiled,node.name)
            for method in node.body:
                if not isinstance(method,ast.FunctionDef):continue
                function=vars(cls).get(method.name)
                if (type(function)is not FunctionType or function.__globals__ is not globals()
                        or function.__qualname__!=node.name+'.'+method.name
                        or _code_shape(function.__code__)!=_code_shape(_code_at(class_code,method.name))):
                    raise Boundary('actual complete-module narrative method required: '+method.name)
                bindings.append((cls,method.name,function,function.__code__))
        elif isinstance(node,ast.FunctionDef):
            function=getattr(module,node.name)
            if (type(function)is not FunctionType or function.__globals__ is not globals()
                    or _code_shape(function.__code__)!=_code_shape(_code_at(compiled,node.name))):
                raise Boundary('actual complete-module narrative source helper required: '+node.name)
            bindings.append((module,node.name,function,function.__code__))
    return tuple(bindings)


class OriginalNarrativeResetJump(Exception):
    """An actual nonreturning JMP, not a new IRQ, RTS or reset completion."""
    def __init__(self,owner,frame,full_sr,source_pc):
        self.owner,self.state,self.frame=owner,owner.state,frame
        self.full_sr,self.source_pc,self.target=full_sr,source_pc,0x206
        super().__init__('original narrative JMP206 terminated its Main4B4 continuation')


class NarrativeScenePrograms(RepeatingScenePrograms):
    """Finite same-Scene narrative terminal provider for the actual Main4B4."""
    def __init__(self,state):
        self._narrative_own_bindings=_pin_own()
        self._narrative_base_methods,self._narrative_base_functions=_pin_base()
        self._narrative_base=RepeatingScenePrograms
        self._narrative_class=NarrativeScenePrograms
        self._narrative_methods={name:(function,function.__code__)
            for name,function in vars(NarrativeScenePrograms).items()if type(function)is FunctionType}
        self._narrative_jump_class=OriginalNarrativeResetJump
        self._narrative_jump_init=(OriginalNarrativeResetJump.__init__,OriginalNarrativeResetJump.__init__.__code__)
        self._narrative_base_methods['__init__'][0](self,state)
        self.thread=threading.get_ident();self.active=False;self.entered=None
        self.pending=self.claimed_jump=self.terminated_jump=None
        self.terminated=False;self.exit_site=None;self.jumps=self.claimed=0
        self.narrative_originals={};self.narrative_views={};self.narrative_namespaces={}
        self.narrative_bindings={}
        modules={'support':self.repeat_modules['support'],'story':self.repeat_modules['story']}
        for group,module in modules.items():
            tree=ast.parse(inspect.getsource(module),filename=module.__file__)
            nodes={node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
            plain=compile(tree,module.__file__,'exec',dont_inherit=True)
            derived=compile(_narrative_tree(group,tree),module.__file__,'exec',dont_inherit=True)
            namespace=dict(vars(module));self.narrative_namespaces[group]=namespace
            for name in VIEW_NAMES[group]:
                function=getattr(module,name)
                if (name not in nodes or _dump(nodes[name])!=_dump(ast.parse(EXPECTED_SOURCE[group][name]).body[0])
                        or type(function)is not FunctionType or function.__globals__ is not vars(module)
                        or function.__module__!=module.__name__ or function.__name__!=name
                        or function.__closure__ is not None or function.__code__.co_freevars
                        or _code_shape(function.__code__)!=_code_shape(_code_at(plain,name))):
                    raise Boundary('actual complete original story owner required: '+name)
                self.narrative_originals[group,name]=(module,function,function.__code__)
                view=FunctionType(_code_at(derived,name),namespace,name,function.__defaults__,None)
                view.__kwdefaults__=function.__kwdefaults__;view.__annotations__=dict(function.__annotations__)
                namespace[name]=view;self.narrative_views[group,name]=(view,view.__code__)
                self.narrative_bindings[group,name]=view
        self._narrative_view_owners=dict(self.narrative_views)
        aliases={'_narrative_story':self._story,'_narrative_exit':self._exit,'_narrative_jump':self._jump}
        for group,namespace in self.narrative_namespaces.items():
            for name,value in aliases.items():
                if name in namespace:raise Boundary('private narrative alias cannot replace original source name')
                namespace[name]=value;self.narrative_bindings[group,name]=value
        name='dispatch_repeating_scene_presentation_fields'
        self._narrative_route=self.narrative_views['support',name][0]
        # Only the same instance's private238 helper sees the new finite owner.
        # No original module function, global dispatcher or original code is rebound.
        self.repeat_namespaces['support'][name]=self._narrative_route
        self.repeat_bindings['support',name]=self._narrative_route
        self.source_contract=dict(confidence='confirmed_source_candidate_runtime_unverified',
            whole_private_views=14,changed_original_expressions=7,whole_FN_inverse=True,
            whole_module_inverse=True,actual_jump_sites=tuple(EXIT_SITES.values()),target=0x206,
            physical_retained_LONGs=(0x3B77E,0x580,0x3CE),new_IRQ_or_RTS=False,
            reset_authority_supplied=False,default_clock_or_budget_added=False)

    def require_current(self,state):
        if (RepeatingScenePrograms is not self._narrative_base
                or repeating.RepeatingScenePrograms is not self._narrative_base
                or NarrativeScenePrograms is not self._narrative_class
                or NarrativeScenePrograms.__bases__!=(self._narrative_base,)
                or OriginalNarrativeResetJump is not self._narrative_jump_class):
            raise Boundary('actual narrative/source parent class identity changed')
        for owner,name,function,code in self._narrative_own_bindings:
            if getattr(owner,name)is not function or function.__code__ is not code:
                raise Boundary('actual complete-module narrative provider binding changed: '+name)
        for name,(function,code)in self._narrative_methods.items():
            if vars(self._narrative_class).get(name)is not function or function.__code__ is not code:
                raise Boundary('actual narrative owner method changed: '+name)
        function,code=self._narrative_jump_init
        if OriginalNarrativeResetJump.__init__ is not function or function.__code__ is not code:
            raise Boundary('actual narrative transfer class changed')
        for name,(function,code)in self._narrative_base_methods.items():
            if vars(self._narrative_base).get(name)is not function or function.__code__ is not code:
                raise Boundary('actual repeating parent method changed: '+name)
        for name,(function,code)in self._narrative_base_functions.items():
            if getattr(repeating,name)is not function or function.__code__ is not code:
                raise Boundary('actual repeating parent utility changed: '+name)
        self._narrative_base_methods['require_current'][0](self,state)
        if not hasattr(self,'narrative_originals'):return
        if threading.get_ident()!=self.thread:raise Boundary('narrative transfer belongs to its actual Scene thread')
        for (group,name),(module,function,code)in self.narrative_originals.items():
            if getattr(module,name)is not function or function.__code__ is not code:
                raise Boundary('actual original narrative callable changed: '+name)
        if self.narrative_views.keys()!=self._narrative_view_owners.keys():
            raise Boundary('finite complete narrative graph inventory changed')
        for (group,name),(view,code)in self._narrative_view_owners.items():
            if (self.narrative_views[group,name]!=(view,code)
                    or self.narrative_namespaces[group].get(name)is not view or view.__code__ is not code):
                raise Boundary('private complete narrative view changed: '+name)
        for (group,name),value in self.narrative_bindings.items():
            if self.narrative_namespaces[group].get(name)is not value:
                raise Boundary('private narrative source binding changed: '+name)
        if (self.repeat_namespaces['support'].get('dispatch_repeating_scene_presentation_fields')is not self._narrative_route
                or self.repeat_bindings.get(('support','dispatch_repeating_scene_presentation_fields'))is not self._narrative_route):
            raise Boundary('same-instance Main4B4 terminal dispatcher binding changed')

    def _story(self,memory,frame,target):
        self.require_current(memory.state)
        if (type(memory)is not SceneRefreshMemory or not self.active
                or target not in (0x3B79E,0x3B7A2,0x3B7A6,0x3B7AA,0x3B7AE)):
            raise Boundary('actual running Main4B4 narrative dispatcher required')
        return self.narrative_views['story','_story_known_fields'][0](memory,frame,target)

    def _exit(self,memory,frame,source_pc):
        self.require_current(memory.state)
        if (type(memory)is not SceneRefreshMemory or not self.active or self.exit_site is not None
                or source_pc not in EXIT_SITES.values()):
            raise Boundary('one actual finite original story exit caller required')
        self.exit_site=source_pc
        try:return self.narrative_views['story','_story_exit_fields'][0](memory,frame)
        finally:self.exit_site=None

    def _jump(self,memory,frame,target):
        self.require_current(memory.state)
        frame=_movement_frame(self.state,frame)
        if (type(memory)is not SceneRefreshMemory or memory.state is not self.state
                or not self.active or self.entered is None or self.pending is not None
                or self.claimed_jump is not None or self.exit_site not in EXIT_SITES.values()
                or target!=0x206 or frame.status!=(self.state.sr&31)
                or frame.stack_cursor.base!=self.entered.stack_cursor.base-12):
            raise Boundary('actual pressed five-story JMP with its three original LONG slots required')
        jump=OriginalNarrativeResetJump(self,frame,self.state.sr,self.exit_site)
        self.pending=jump;self.jumps+=1
        self._jump_proof=(jump,self.state,frame,self.state.sr,self.exit_site,0x206,frame.stack_cursor.base)
        self.state.events.append(('original_narrative_jump',self.exit_site,0x206,
            frame.stack_cursor.base,self.state.sr))
        raise jump

    def main_scene_call(self,state,frame,target,continuation):
        if (target,continuation)!=(0x4B4,0x3CE):
            return (yield from super().main_scene_call(state,frame,target,continuation))
        self.require_current(state)
        if type(self)is not NarrativeScenePrograms or self.active or self.entered is not None:
            raise Boundary('one exact actual Main4B4 narrative lifetime required')
        frame=_movement_frame(state,frame)
        self.active=True;self.entered=frame
        try:
            return (yield from super().main_scene_call(state,frame,target,continuation))
        except OriginalNarrativeResetJump as jump:
            if type(jump)is not OriginalNarrativeResetJump or jump is not self.pending or jump.owner is not self:
                raise Boundary('only this actual narrative lifetime may terminate with its own JMP')
            self.terminated=True;self.terminated_jump=jump
            raise
        finally:self.active=False

    def _require_jump(self,jump):
        self.require_current(self.state)
        if (type(self)is not NarrativeScenePrograms or type(jump)is not OriginalNarrativeResetJump
                or self.active or not self.terminated or self.terminated_jump is not jump
                or jump.owner is not self or self.exit_site is not None
                or jump is not self._jump_proof[0] or jump.frame is not self._jump_proof[2]
                or (jump,jump.state,jump.frame,jump.full_sr,jump.source_pc,jump.target,
                    jump.frame.stack_cursor.base)!=self._jump_proof
                or jump.state is not self.state or jump.full_sr!=self.state.sr
                or jump.frame.status!=(self.state.sr&31)):
            raise Boundary('actual terminated unchanged Main4B4 jump proof required')
        return jump.frame

    def claim(self,jump):
        """Consume once only after the real source generator has unwound."""
        frame=self._require_jump(jump)
        if jump is not self.pending or self.claimed_jump is not None:
            raise Boundary('one pending unclaimed original narrative transfer required')
        self.pending=None;self.claimed_jump=jump;self.claimed+=1
        return frame

    def require_claimed(self,jump):
        """Read-only exact claimed proof for the new independent warm capture."""
        frame=self._require_jump(jump)
        if self.pending is not None or self.claimed_jump is not jump or self.claimed!=1:
            raise Boundary('one actual already-claimed narrative JMP proof required')
        return frame
