"""Finite default-only bridge from current sole fields to existing lowerers.

This reads literal parameters and real CCR predicates in already fully admitted
business ASTs. It emits no code, does not import business implementations, and
does not use original bytes, old projection constants, or default fallback rules.
Policy editing is deliberately NOT_AVAILABLE in this selected-family interface.
"""
import ast
from .compiler_common import CompileError,semantic_functions

SELECTED_DUEL_NAMES=('advance_duel_entry_palette','show_active_duel_turn_label','wait_active_duel_action','upload_duel_officer_name','clear_duel_text_plane','choose_duel_two_option_menu','choose_first_duel_equipment','choose_duel_action_menu','decode_duel_byte_lanes','choose_duel_status_text')
CORE_NAMES={'advance_duel_entry_palette':'advance_duel_entry_palette_fields','show_active_duel_turn_label':'show_active_duel_turn_label_fields','wait_active_duel_action':'wait_active_duel_action_fields','upload_duel_officer_name':'upload_duel_officer_name_fields','clear_duel_text_plane':'clear_duel_text_plane_fields','choose_duel_two_option_menu':'choose_duel_two_option_menu_fields','choose_first_duel_equipment':'choose_first_duel_equipment_fields','choose_duel_action_menu':'choose_duel_action_menu_fields','decode_duel_byte_lanes':'decode_duel_byte_lanes_fields','choose_duel_status_text':'choose_duel_status_text_fields'}

def admit_selected_duel_fields(source,declarations,approved,selected_names):
    if type(selected_names) is not tuple or selected_names!=SELECTED_DUEL_NAMES:
        raise CompileError('exact ten complete default duel owners required')
    records=semantic_functions(source,declarations,approved)
    functions={n.name:n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)}
    provenance=[]
    def walk(node):
        yield node
        for child in ast.iter_child_nodes(node):yield from walk(child)
    def remember(function,kind,node,value,locator):
        provenance.append(dict(function=function,kind=kind,locator=locator,value=value,supplied_node=ast.dump(node,include_attributes=False)))
        return value
    def literal(fn,call,index,arg,tail=()):
        matches=[n for n in walk(functions[fn]) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==call]
        try:node=matches[index].args[arg]
        except IndexError as exc:raise CompileError('fixed field parameter call absent') from exc
        for attr in tail:node=getattr(node,attr)
        if not isinstance(node,ast.Constant) or type(node.value) is not int or not 0<=node.value<=4294967295:
            raise CompileError('actual bounded literal field parameter required')
        return remember(fn,'actual_field_literal',node,node.value,[call,index,arg,*tail])
    def branch(fn,index,invert=False):
        tests=[n.test for n in walk(functions[fn]) if isinstance(n,ast.If)]
        node=tests[index];actual=node;negated=False
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.Not):negated=True;node=node.operand
        if not (isinstance(node,ast.BinOp) and isinstance(node.op,ast.BitAnd) and isinstance(node.left,ast.Attribute) and isinstance(node.left.value,ast.Name) and node.left.value.id=='frame' and node.left.attr=='status' and isinstance(node.right,ast.Constant) and node.right.value in (1,4,8)):
            raise CompileError('original frame CCR predicate required')
        codes={1:('bcs','bcc'),4:('beq','bne'),8:('bmi','bpl')}
        value=codes[node.right.value][int(negated!=invert)]
        return remember(fn,'actual_CCR_branch',actual,value,['If',index,'test',invert])
    def assign_branch(fn,name):
        matches=[n for n in walk(functions[fn]) if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id==name]
        if len(matches)!=1:raise CompileError('unique actual CCR assignment required')
        node=matches[0].value
        if not (isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='bool' and len(node.args)==1 and ast.unparse(node.args[0])=='frame.status & 4'):
            raise CompileError('actual equality CCR selection required')
        return remember(fn,'actual_equal_CCR_branch',node,'beq',['assignment',name])
    T='choose_duel_two_option_menu_fields';E='choose_duel_equipment_fields';H='_duel_menu_loadout_highlight_fields';Q='_duel_menu_adjust_memory_word_fields'
    A='choose_duel_action_menu_fields';D='_duel_action_direction_fields';R='_duel_action_restricted_choice_fields';K='_duel_action_menu_highlight_fields'
    P='advance_duel_entry_palette_fields';L='show_active_duel_turn_label_fields';W='_wait_duel_action_fields';Y='wait_either_duel_action_fields'
    S='choose_duel_status_text_fields';N='upload_duel_officer_name_fields';U='_upload_duel_glyph_buffers_fields';C='clear_duel_text_plane_fields';J='decode_duel_byte_lane_fields'
    def menu(fn,equipment):
        return dict(direction_mask=literal(fn,'_movement_move',2 if equipment else 1,3,('right',)),
            direction_step=literal(fn,'_movement_move',3 if equipment else 2,3),positive_mask=literal(fn,'_movement_move',4 if equipment else 3,3,('right',)),
            confirm_bit=literal(fn,'_duel_menu_button_fields',0,2),cursor_direction_mask=literal(H,'_movement_move',0,3,('right',)),cursor_blink_mask=literal(H,'_movement_move',2,3,('right',)),
            cursor_coordinate=literal(H,'_movement_move',3,3),cursor_stride=literal(H,'_movement_multiply_word',0,3),cursor_bias=literal(fn,'_duel_menu_loadout_highlight_fields',0,2),
            cursor_pattern=literal(H,'_movement_move',5,3),cursor_attributes=literal(H,'_movement_move',6,3),timer_step=literal(Q,'_movement_binary_flags',0,3))
    rules={}
    rules['choose_duel_two_option_menu']=dict(menu(T,False),accept_bound=literal(T,'_movement_compare',0,3),accept_branch=branch(T,2,True))
    rules['choose_first_duel_equipment']=dict(menu(E,True),repair_step=literal(Q,'_movement_binary_flags',0,3))
    rules['advance_duel_entry_palette']=dict(flow_entry_palette_bound=literal(P,'_movement_compare',0,3),flow_entry_palette_relation_true_branch=branch(P,0),flow_entry_palette_complement=literal(P,'_movement_move',0,3),flow_entry_palette_count=literal(P,'_movement_move',1,3),flow_entry_palette_step=literal(P,'_movement_binary_flags',0,3))
    rules['show_active_duel_turn_label']=dict(flow_first_label_position=literal(L,'_movement_move',0,3),flow_label_tick_mask=literal(L,'_movement_move',2,3,('right',)),flow_second_label_position=literal(L,'_movement_move',3,3))
    rules['wait_active_duel_action']=dict(flow_active_wait_timer_step=literal(W,'_movement_binary_flags',0,3),flow_either_wait_timer_step=literal(W,'_movement_binary_flags',0,3),flow_active_wait_accept_mask=literal(W,'_movement_move',2,3,('right',)),flow_either_wait_accept_mask=literal(W,'_movement_move',2,3,('right',)),flow_automatic_mode=literal(Y,'_movement_compare',0,3),flow_active_wait_pending_relation_true_branch=branch(W,2),flow_either_wait_pending_relation_true_branch=branch(W,2),flow_active_wait_confirm_relation_false_branch=branch(W,5,True),flow_either_wait_confirm_relation_false_branch=branch(W,5,True))
    rules['choose_duel_status_text']=dict(flow_status_text_command=literal(S,'_duel_scene_store_fields',1,3))
    rules['upload_duel_officer_name']=dict(name_default_rows=literal(N,'_movement_move',0,3),name_terminator_rows=literal(N,'_movement_move',1,3),name_shade_shift=literal(N,'_scene_render_asl_word',0,4),name_buffer_bytes_counter=literal(N,'_movement_move',4,3),name_upload_count=literal(U,'_movement_move',0,3))
    rules['clear_duel_text_plane']=dict(text_clear_fill=literal(C,'_movement_move_long',0,3),text_clear_words_counter=literal(C,'_movement_move',0,3))
    rules['decode_duel_byte_lanes']=dict(lane_ramp_step=literal(J,'_movement_add_word',0,3))
    rules['choose_duel_action_menu']=dict(restricted_branch=assign_branch(A,'restricted'),direction_mask=literal(A,'_movement_move',2,3,('right',)),vertical_step=literal(D,'_movement_move',0,3),horizontal_step=literal(D,'_movement_move',1,3),vertical_forward_bit=literal(D,'_duel_menu_button_fields',0,2),vertical_backward_bit=literal(D,'_duel_menu_button_fields',1,2),horizontal_forward_bit=literal(D,'_duel_menu_button_fields',2,2),unrestricted_bound=literal(A,'_movement_compare',1,3),unrestricted_branch=branch(A,2,True),restricted_forward_step=literal(R,'_movement_add_word',0,3),restricted_forward_skip_value=literal(R,'_movement_compare',0,3),restricted_forward_skip_branch=branch(R,1,True),restricted_forward_skip_step=literal(R,'_movement_add_word',1,3),restricted_forward_bound=literal(R,'_movement_compare',1,3),restricted_forward_branch=branch(R,2,True),restricted_forward_wrap=literal(R,'_movement_move_long',1,3),restricted_backward_skip_value=literal(R,'_movement_compare',2,3),restricted_backward_skip_branch=branch(R,4,True),restricted_backward_skip_step=literal(R,'_duel_commit_sub_word_fields',0,3),restricted_backward_step=literal(R,'_duel_commit_sub_word_fields',1,3),restricted_backward_wrap=literal(R,'_movement_move_long',2,3),confirm_bit=literal(A,'_duel_menu_button_fields',0,2),timer_step=literal(Q,'_movement_binary_flags',0,3),cursor_direction_mask=literal(K,'_movement_move',0,3,('right',)),cursor_blink_mask=literal(K,'_movement_move',2,3,('right',)),restricted_cursor_index_mask=literal(K,'_movement_move',4,3,('right',)),restricted_cursor_x=literal(K,'_movement_move',5,3),cursor_x_mask=literal(K,'_movement_move',8,3,('right',)),cursor_x_stride=literal(K,'_movement_multiply_word',0,3),cursor_x_bias=literal(K,'_movement_add_word',0,3),cursor_y_mask=literal(K,'_movement_move',10,3,('right',)),cursor_y_stride=literal(K,'_movement_multiply_word',1,3),cursor_y_bias=literal(K,'_movement_add_word',1,3),cursor_pattern=literal(K,'_movement_move',11,3),cursor_attributes=literal(K,'_movement_move',12,3))
    for owner in selected_names:
        core=CORE_NAMES[owner]
        dependencies=set()
        def visit(name):
            if name in dependencies:return
            dependencies.add(name)
            for n in walk(functions[name]):
                if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load) and n.id in functions:visit(n.id)
        visit(core)
        records[owner]['rules']=rules[owner]
        records[owner]['effects']=dict(previous_projection=records[owner]['effects'],sole_current_fields={name:records[name]['effects'] for name in sorted(dependencies)})
    return records,dict(grammar='selected-duel-current-fields-default-v1',provenance=provenance,owner_rules=rules,parameter_edit_status='NOT_AVAILABLE',reason='exact default-only full AST interface; no new edit authority')
