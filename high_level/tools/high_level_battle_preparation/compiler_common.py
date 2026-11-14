"""Strict shared AST binding gate and ordinary target emission; no file reads."""
import ast
from dataclasses import asdict
from .target import BINDINGS, validate_binding


class CompileError(ValueError):
    pass


def require_declared_names(functions, imported_names):
    if type(functions) is not dict or type(imported_names) is not set or any(type(n) is not str for n in imported_names):
        raise CompileError('strict current Python declaration sets required')
    available = set(functions) | imported_names | {'tuple'}
    for function in functions.values():
        local = {a.arg for a in function.args.args}
        local.update(n.id for n in ast.walk(function) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store))
        used = {n.id for n in ast.walk(function) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
        if used-local-available:
            raise CompileError('used external names need approved current imports: '+','.join(sorted(used-local-available)))


class Emitter:
    def __init__(self, binding):
        validate_binding(binding)
        self.binding,self.lines,self.mapping,self.serial = binding,[],[],0
    def begin(self):
        self.lines += [f'.org 0x{self.binding.entry:x}', '.global '+self.binding.name,self.binding.name+':']
    def label(self,name):
        if type(name) is not str or not name.isidentifier(): raise CompileError('strict label required')
        self.lines.append(name+':')
    def fresh(self,role):
        if type(role) is not str or not role.isidentifier(): raise CompileError('strict label role required')
        self.serial += 1
        return f'{self.binding.name}_{role}_{self.serial}'
    def ins(self,operation,operands='',width=2):
        if type(operation) is not str or type(operands) is not str or type(width) is not int or width not in (2,4,6,8,10):
            raise CompileError('strict ordinary instruction width required')
        if not operation or any(c in operation for c in ('\n',';','.byte','.word','.incbin')) or '\n' in operands or ';' in operands:
            raise CompileError('one ordinary target instruction required')
        symbol=f'hl_{self.binding.name}_{len(self.mapping)}'
        self.lines += ['.global '+symbol,symbol+':','    '+operation+(' '+operands if operands else '')]
        self.mapping.append(dict(symbol=symbol,operation=operation,operands=operands,encoding_bytes=width))
    def end(self,*,emit_completion=True):
        if emit_completion:self.ins('rts')
        self.lines += ['.global '+self.binding.name+'_end',self.binding.name+'_end:']
    def unit(self,effects):
        return dict(binding=asdict(self.binding),assembly='\n'.join(self.lines)+'\n',instructions=self.mapping,effects=effects)


def compile_modules(selection_source,descriptor_source,result_source,data_source=None):
    if data_source is not None: raise CompileError('code generation needs no implicit data image; explicit host ReadOnlyData is separate')
    from .compiler_selection import compile_selection
    from .compiler_descriptor import compile_descriptor
    from .compiler_result import compile_result
    outputs=(compile_selection(selection_source),compile_descriptor(descriptor_source),compile_result(result_source))
    units=sorted([u for output in outputs for u in output['units']],key=lambda u:u['binding']['entry'])
    if [u['binding'] for u in units] != [asdict(b) for b in BINDINGS]:raise CompileError('complete twenty-body preparation/result cluster required')
    if sum(u['binding']['end']-u['binding']['entry'] for u in units)!=1466:raise CompileError('exact new scope required')
    assembly='.cpu 68000\n.text\n'+'\n'.join(u['assembly'] for u in units)
    return dict(assembly=assembly,units=units,new_units=units,reused_units=[],allocated_bytes=1466,
                new_bytes=1466,reused_bytes=0,instructions=sum(len(u['instructions']) for u in units),
                effects={u['binding']['name']:u['effects'] for u in units},original_generation_input=False,
                complete_CPU=False,complete_ROM=False)


def compile_complete_frame_modules(selection_source, descriptor_source, result_source,
                                   complete_city_source):
    """Compile current Scene algorithms, never their legacy scalar projections.

    All projection declarations and the complete current field catalog are
    admitted before selecting the thirteen real Scene roots. Their existing
    physical preparation ownership is unchanged. The old scalar frontend is
    intentionally neither widened nor supplied with historical source text.
    """
    from .compiler_selection import compile_selection
    from .compiler_descriptor import (
        DECLARATIONS as descriptor_declarations,
        _lower_maximum_three_live_lookup_attributes_fields,
    )
    from .compiler_fields import lower_frame_selection
    from .compiler_frame_selection_tail import lower_frame_selection_tail
    from .compiler_frame_descriptor import lower_frame_descriptor
    from .compiler_result import compile_result
    from .target import SELECTION_BINDINGS, DESCRIPTOR_BINDINGS
    from ..high_level_remaining_flows import compiler_city

    # The one still-logical scalar rule is compiled normally; this call also
    # admits all nine current selection declarations without lowering facades.
    units = compile_selection(selection_source, ('selected_attribute_average',))['units']
    descriptor_approved = {
        'domain': {'PreparationState', 'Table', 'Word', 'Long', 'u16', 'low8',
                   'low16', 'replace_byte', 'replace_word', 'uint'},
        'business_selection': {'compact_active_deployment_queue'},
        'contexts_counter': {'project_preparation_selection_fields'},
    }
    descriptor_records = compiler_city.semantic_functions(
        descriptor_source, descriptor_declarations, descriptor_approved)
    if set(descriptor_records) != {binding.name for binding in DESCRIPTOR_BINDINGS}:
        raise CompileError('all five complete current descriptor projections required')
    records = compiler_city.semantic_functions(
        complete_city_source, compiler_city.DECLARATIONS, compiler_city.APPROVED)

    front = {'count_selected_deployment', 'initialize_selected_assignment',
             'selected_troop_weights', 'refresh_object_attribute_average'}
    tail = {'submit_deployment_queue', 'clear_original_tail_coordinate',
            'compact_active_deployment_queue', 'deployment_force_carry'}
    bindings = tuple(binding for binding in SELECTION_BINDINGS
                     if binding.name != 'selected_attribute_average') + DESCRIPTOR_BINDINGS
    for binding in bindings:
        root = binding.name + '_fields'
        declaration = compiler_city.DECLARATIONS.get(root)
        if (declaration is None or declaration['signature'] !=
                'state: SceneState, frame: FirstDeploymentFrame' or
                declaration['returns'] != 'FirstDeploymentFrame' or records[root]['rules']):
            raise CompileError('complete fixed-ABI current preparation Scene rule required: ' + root)
        effects = records[root]['effects']
        if binding.name in front:
            unit = lower_frame_selection(binding, effects)
        elif binding.name in tail:
            unit = lower_frame_selection_tail(binding, effects)
        elif binding.name == 'maximum_three_live_lookup_attributes':
            unit = _lower_maximum_three_live_lookup_attributes_fields(binding, effects)
        else:
            unit = lower_frame_descriptor(binding, effects)
        unit['actual_scene_algorithm'] = root
        unit['actual_scene_source'] = 'tools/high_level_remaining_flows/business_city.py'
        units.append(unit)
    units.extend(compile_result(result_source)['units'])
    units.sort(key=lambda unit: unit['binding']['entry'])
    if [unit['binding'] for unit in units] != [asdict(binding) for binding in BINDINGS]:
        raise CompileError('complete twenty-body current preparation ownership required')
    for unit in units:
        binding = unit['binding']
        if sum(row['encoding_bytes'] for row in unit['instructions']) != binding['end'] - binding['entry']:
            raise CompileError('complete current preparation instruction extent differs: ' + binding['name'])
    return dict(assembly='.cpu 68000\n.text\n' + '\n'.join(unit['assembly'] for unit in units),
                units=units, new_units=units, reused_units=[], allocated_bytes=1466,
                new_bytes=1466, reused_bytes=0,
                instructions=sum(len(unit['instructions']) for unit in units),
                effects={unit['binding']['name']: unit['effects'] for unit in units},
                complete_current_scene_catalog_count=len(records),
                current_scene_roots=[binding.name + '_fields' for binding in bindings],
                legacy_projection_lowered=False, original_generation_input=False,
                complete_CPU=False, complete_ROM=False)
