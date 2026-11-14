"""Persistent whole original battle round and its actual Main498 BRA parent.

Four finite source views preserve every original operation and physical CALL.
Only Allocation/Duel propagation becomes cooperative. No global callable is
rebound, no original prefix is restarted and no hardware progress is invented.
"""
import ast
import copy
import inspect
import threading
from types import CodeType,FunctionType

from ..high_level_scene_flows.domain import SceneState,Boundary,checked_state,uint
from ..high_level_main_flows.contexts_gameplay import FirstDeploymentFrame,MovementContinuationBoundary
from ..high_level_main_flows.business_movement_support import _movement_frame
from ..high_level_dynamic_flows.allocation_steps import AllocationSceneWait
from ..high_level_scene_flows.duel_scene_steps import DuelSceneWait

EXPECTED_WHOLE_SOURCES={'battle': {'_presentation_call_fields': "FunctionDef(name='_presentation_call_fields', args=arguments(posonlyargs=[], args=[arg(arg='memory'), arg(arg='frame'), arg(arg='continuation'), arg(arg='algorithm')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Expr(value=Constant(value='A known direct child owns only its actual internal JSR/RTS slot.')), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_presentation_frame', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load())], keywords=[])), Expr(value=Call(func=Name(id='uint', ctx=Load()), args=[Name(id='continuation', ctx=Load()), Constant(value=32)], keywords=[])), If(test=Compare(left=Attribute(value=Name(id='frame', ctx=Load()), attr='stack_cursor', ctx=Load()), ops=[Is()], comparators=[Constant(value=None)]), body=[Return(value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='finish', ctx=Load()), args=[Call(func=Name(id='algorithm', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load())], keywords=[])], keywords=[]))], orelse=[]), Assign(targets=[Name(id='stack', ctx=Store())], value=Call(func=Attribute(value=Attribute(value=Name(id='frame', ctx=Load()), attr='stack_cursor', ctx=Load()), attr='advance', ctx=Load()), args=[UnaryOp(op=USub(), operand=Constant(value=4))], keywords=[])), Expr(value=Call(func=Attribute(value=Name(id='stack', ctx=Load()), attr='set_long', ctx=Load()), args=[Constant(value=0), Name(id='continuation', ctx=Load())], keywords=[])), Assign(targets=[Name(id='entered', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='stack_cursor', value=Name(id='stack', ctx=Load()))])), Expr(value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='finish', ctx=Load()), args=[Name(id='entered', ctx=Load())], keywords=[])), Assign(targets=[Name(id='returned', ctx=Store())], value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='finish', ctx=Load()), args=[Call(func=Name(id='algorithm', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='entered', ctx=Load())], keywords=[])], keywords=[])), Assign(targets=[Name(id='actual', ctx=Store())], value=Call(func=Attribute(value=Attribute(value=Name(id='returned', ctx=Load()), attr='stack_cursor', ctx=Load()), attr='long', ctx=Load()), args=[], keywords=[])), If(test=Compare(left=Name(id='actual', ctx=Load()), ops=[NotEq()], comparators=[Name(id='continuation', ctx=Load())]), body=[Raise(exc=Call(func=Name(id='Boundary', ctx=Load()), args=[BinOp(left=Constant(value='original presentation child return slot changed to '), op=Add(), right=Call(func=Name(id='str', ctx=Load()), args=[Name(id='actual', ctx=Load())], keywords=[]))], keywords=[]))], orelse=[]), Return(value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='returned', ctx=Load())], keywords=[keyword(arg='stack_cursor', value=Call(func=Attribute(value=Attribute(value=Name(id='returned', ctx=Load()), attr='stack_cursor', ctx=Load()), attr='advance', ctx=Load()), args=[Constant(value=4)], keywords=[]))]))], decorator_list=[], type_params=[])", '_battle_scene_round_call_fields': "FunctionDef(name='_battle_scene_round_call_fields', args=arguments(posonlyargs=[], args=[arg(arg='memory'), arg(arg='frame', annotation=Name(id='FirstDeploymentFrame', ctx=Load())), arg(arg='target', annotation=Name(id='Long', ctx=Load())), arg(arg='continuation', annotation=Name(id='Long', ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Expr(value=Constant(value='Own exactly one DC0 JSR slot; dispatch only recovered typed children.')), ImportFrom(module='contexts_services', names=[alias(name='SceneRefreshMemory'), alias(name='SceneRefreshBoundary')], level=1), If(test=Compare(left=Tuple(elts=[Name(id='target', ctx=Load()), Name(id='continuation', ctx=Load())], ctx=Load()), ops=[NotIn()], comparators=[Tuple(elts=[Tuple(elts=[Constant(value=120186), Constant(value=3532)], ctx=Load()), Tuple(elts=[Constant(value=251476), Constant(value=3548)], ctx=Load()), Tuple(elts=[Constant(value=26662), Constant(value=3554)], ctx=Load()), Tuple(elts=[Constant(value=100518), Constant(value=3572)], ctx=Load()), Tuple(elts=[Constant(value=159156), Constant(value=3624)], ctx=Load()), Tuple(elts=[Constant(value=26662), Constant(value=3634)], ctx=Load()), Tuple(elts=[Constant(value=101120), Constant(value=3640)], ctx=Load()), Tuple(elts=[Constant(value=120216), Constant(value=3648)], ctx=Load()), Tuple(elts=[Constant(value=118844), Constant(value=3680)], ctx=Load()), Tuple(elts=[Constant(value=120130), Constant(value=3706)], ctx=Load())], ctx=Load())]), body=[Raise(exc=Call(func=Name(id='ValueError', ctx=Load()), args=[Constant(value='original battle-round child and JSR continuation required')], keywords=[]))], orelse=[]), Expr(value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='frame', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[])), FunctionDef(name='child', args=arguments(posonlyargs=[], args=[arg(arg='actual_memory'), arg(arg='entered')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[If(test=Compare(left=Name(id='target', ctx=Load()), ops=[Eq()], comparators=[Constant(value=120186)]), body=[ImportFrom(module='high_level_remaining_flows.business_city', names=[alias(name='initialize_prebattle_head_bytes_fields')], level=2), Return(value=Call(func=Name(id='initialize_prebattle_head_bytes_fields', ctx=Load()), args=[Attribute(value=Name(id='actual_memory', ctx=Load()), attr='state', ctx=Load()), Name(id='entered', ctx=Load())], keywords=[]))], orelse=[]), If(test=Compare(left=Name(id='target', ctx=Load()), ops=[Eq()], comparators=[Constant(value=251476)]), body=[ImportFrom(module='high_level_scene_flows.business_objects', names=[alias(name='run_scene_object_controller_fields')], level=2), Return(value=Call(func=Name(id='run_scene_object_controller_fields', ctx=Load()), args=[Call(func=Name(id='SceneRefreshMemory', ctx=Load()), args=[Attribute(value=Name(id='actual_memory', ctx=Load()), attr='state', ctx=Load())], keywords=[]), Name(id='entered', ctx=Load())], keywords=[]))], orelse=[]), If(test=Compare(left=Name(id='target', ctx=Load()), ops=[Eq()], comparators=[Constant(value=26662)]), body=[ImportFrom(module='business_services', names=[alias(name='initialize_video_registers_and_planes_fields')], level=1), Return(value=Call(func=Name(id='initialize_video_registers_and_planes_fields', ctx=Load()), args=[Call(func=Name(id='SceneRefreshMemory', ctx=Load()), args=[Attribute(value=Name(id='actual_memory', ctx=Load()), attr='state', ctx=Load())], keywords=[]), Name(id='entered', ctx=Load())], keywords=[]))], orelse=[]), If(test=Compare(left=Name(id='target', ctx=Load()), ops=[Eq()], comparators=[Constant(value=100518)]), body=[ImportFrom(module='business_reuse', names=[alias(name='settle_duel_training_and_troops_fields')], level=1), Return(value=Call(func=Name(id='settle_duel_training_and_troops_fields', ctx=Load()), args=[Name(id='actual_memory', ctx=Load()), Name(id='entered', ctx=Load())], keywords=[]))], orelse=[]), If(test=Compare(left=Name(id='target', ctx=Load()), ops=[Eq()], comparators=[Constant(value=101120)]), body=[ImportFrom(module='business_reuse', names=[alias(name='settle_duel_packets_fields')], level=1), Return(value=Call(func=Name(id='settle_duel_packets_fields', ctx=Load()), args=[Name(id='actual_memory', ctx=Load()), Name(id='entered', ctx=Load())], keywords=[]))], orelse=[]), If(test=Compare(left=Name(id='target', ctx=Load()), ops=[Eq()], comparators=[Constant(value=120216)]), body=[ImportFrom(module='high_level_remaining_flows.business_city', names=[alias(name='classify_duel_object_result_fields')], level=2), Return(value=Call(func=Name(id='classify_duel_object_result_fields', ctx=Load()), args=[Attribute(value=Name(id='actual_memory', ctx=Load()), attr='state', ctx=Load()), Name(id='entered', ctx=Load())], keywords=[]))], orelse=[]), If(test=Compare(left=Name(id='target', ctx=Load()), ops=[Eq()], comparators=[Constant(value=118844)]), body=[Return(value=Call(func=Name(id='settle_battle_packed_armies_fields', ctx=Load()), args=[Name(id='actual_memory', ctx=Load()), Name(id='entered', ctx=Load())], keywords=[]))], orelse=[]), If(test=Compare(left=Name(id='target', ctx=Load()), ops=[Eq()], comparators=[Constant(value=120130)]), body=[ImportFrom(module='high_level_remaining_flows.business_city', names=[alias(name='rebuild_city_links_from_primary_roster_fields')], level=2), Return(value=Call(func=Name(id='rebuild_city_links_from_primary_roster_fields', ctx=Load()), args=[Attribute(value=Name(id='actual_memory', ctx=Load()), attr='state', ctx=Load()), Name(id='entered', ctx=Load())], keywords=[]))], orelse=[]), If(test=Compare(left=Name(id='target', ctx=Load()), ops=[Eq()], comparators=[Constant(value=159156)]), body=[ImportFrom(module='high_level_scene_flows.business_duel', names=[alias(name='run_duel_scene_fields')], level=2), Return(value=Call(func=Name(id='run_duel_scene_fields', ctx=Load()), args=[Attribute(value=Name(id='actual_memory', ctx=Load()), attr='state', ctx=Load()), Name(id='entered', ctx=Load())], keywords=[]))], orelse=[]), Raise(exc=Call(func=Name(id='SceneRefreshBoundary', ctx=Load()), args=[Name(id='target', ctx=Load()), Name(id='entered', ctx=Load()), Name(id='continuation', ctx=Load())], keywords=[]))], decorator_list=[], type_params=[]), Return(value=Call(func=Name(id='_presentation_call_fields', ctx=Load()), args=[Call(func=Name(id='BattlePresentationMemory', ctx=Load()), args=[Attribute(value=Name(id='memory', ctx=Load()), attr='state', ctx=Load())], keywords=[]), Name(id='frame', ctx=Load()), Name(id='continuation', ctx=Load()), Name(id='child', ctx=Load())], keywords=[]))], decorator_list=[], returns=Name(id='FirstDeploymentFrame', ctx=Load()), type_params=[])", 'run_battle_scene_round_fields': "FunctionDef(name='run_battle_scene_round_fields', args=arguments(posonlyargs=[], args=[arg(arg='memory'), arg(arg='frame', annotation=Name(id='FirstDeploymentFrame', ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Expr(value=Constant(value='DC0..E7C: sole battle/duel round control with complete live fields.\\n\\n    Both original return routes share their actual 1D542 tail. Carry retry\\n    goes back to DCC, not to the initial head/status save at DC0.\\n    ')), ImportFrom(module='contexts_services', names=[alias(name='SceneRefreshBoundary')], level=1), ImportFrom(module='high_level_main_flows.business_movement_support', names=[alias(name='_movement_test'), alias(name='_movement_compare')], level=2), Expr(value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='frame', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[])), If(test=Compare(left=Attribute(value=Name(id='frame', ctx=Load()), attr='stack_cursor', ctx=Load()), ops=[Is()], comparators=[Constant(value=None)]), body=[Raise(exc=Call(func=Name(id='SceneRefreshBoundary', ctx=Load()), args=[Constant(value=3520), Name(id='frame', ctx=Load()), Constant(value=None)], keywords=[]))], orelse=[]), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='sync_status', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[])), Assign(targets=[Name(id='presentation', ctx=Store())], value=Call(func=Name(id='BattlePresentationMemory', ctx=Load()), args=[Attribute(value=Name(id='memory', ctx=Load()), attr='state', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294963168), Call(func=Attribute(value=Attribute(value=Name(id='memory', ctx=Load()), attr='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=4294964932), Constant(value=2)], keywords=[])], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_battle_scene_round_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=120186), Constant(value=3532)], keywords=[])), While(test=Constant(value=True), body=[Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964932), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294963998), Constant(value=0), Constant(value=True)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_battle_scene_round_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=251476), Constant(value=3548)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_battle_scene_round_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=26662), Constant(value=3554)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_movement_compare', ctx=Load()), args=[Attribute(value=Name(id='memory', ctx=Load()), attr='state', ctx=Load()), Name(id='frame', ctx=Load()), Call(func=Attribute(value=Attribute(value=Name(id='memory', ctx=Load()), attr='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=4294934804), Constant(value=2)], keywords=[]), Constant(value=1), Constant(value=16)], keywords=[])), If(test=UnaryOp(op=Not(), operand=BinOp(left=Attribute(value=Name(id='frame', ctx=Load()), attr='status', ctx=Load()), op=BitAnd(), right=Constant(value=4))), body=[Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_battle_scene_round_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=100518), Constant(value=3572)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_movement_test', ctx=Load()), args=[Attribute(value=Name(id='memory', ctx=Load()), attr='state', ctx=Load()), Name(id='frame', ctx=Load()), Call(func=Attribute(value=Attribute(value=Name(id='memory', ctx=Load()), attr='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=4294963168), Constant(value=2)], keywords=[]), Constant(value=16)], keywords=[])), If(test=UnaryOp(op=Not(), operand=BinOp(left=Attribute(value=Name(id='frame', ctx=Load()), attr='status', ctx=Load()), op=BitAnd(), right=Constant(value=4))), body=[Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964754), Constant(value=1024)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964066), Constant(value=0), Constant(value=True)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964050), Constant(value=0), Constant(value=True)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964932), Constant(value=1)], keywords=[])), Break()], orelse=[])], orelse=[Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964932), Constant(value=3)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=16740596), Constant(value=1)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_battle_scene_round_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=159156), Constant(value=3624)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='status_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value=9984)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_battle_scene_round_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=26662), Constant(value=3634)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_battle_scene_round_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=101120), Constant(value=3640)], keywords=[])), If(test=BinOp(left=Attribute(value=Name(id='frame', ctx=Load()), attr='status', ctx=Load()), op=BitAnd(), right=Constant(value=1)), body=[Continue()], orelse=[]), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_battle_scene_round_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=120216), Constant(value=3648)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_movement_test', ctx=Load()), args=[Attribute(value=Name(id='memory', ctx=Load()), attr='state', ctx=Load()), Name(id='frame', ctx=Load()), Call(func=Attribute(value=Attribute(value=Name(id='memory', ctx=Load()), attr='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=4294963168), Constant(value=2)], keywords=[]), Constant(value=16)], keywords=[])), If(test=UnaryOp(op=Not(), operand=BinOp(left=Attribute(value=Name(id='frame', ctx=Load()), attr='status', ctx=Load()), op=BitAnd(), right=Constant(value=4))), body=[Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964754), Constant(value=1024)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964066), Constant(value=0), Constant(value=True)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964050), Constant(value=0), Constant(value=True)], keywords=[])), Break()], orelse=[])]), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_battle_scene_round_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=118844), Constant(value=3680)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964932), Constant(value=0)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964754), Constant(value=512)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964050), Constant(value=0), Constant(value=True)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_outcome_store_word_fields', ctx=Load()), args=[Name(id='presentation', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294965092), Constant(value=0), Constant(value=True)], keywords=[])), Break()], orelse=[]), Return(value=Call(func=Name(id='_battle_scene_round_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=120130), Constant(value=3706)], keywords=[]))], decorator_list=[], returns=Name(id='FirstDeploymentFrame', ctx=Load()), type_params=[])"}, 'main': {'continue_campaign_action_display_fields': "FunctionDef(name='continue_campaign_action_display_fields', args=arguments(posonlyargs=[], args=[arg(arg='state', annotation=Name(id='SceneState', ctx=Load())), arg(arg='frame', annotation=Name(id='FirstDeploymentFrame', ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Expr(value=Constant(value='498: continue campaign action display; original stage and child tokens.')), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_city_ui_frame_fields', ctx=Load()), args=[Name(id='state', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=1176)], keywords=[])), Return(value=Call(func=Name(id='_campaign_tail_fields', ctx=Load()), args=[Name(id='state', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=3520)], keywords=[]))], decorator_list=[], returns=Name(id='FirstDeploymentFrame', ctx=Load()), type_params=[])"}, 'allocation': {'allocation_scene_program': "FunctionDef(name='allocation_scene_program', args=arguments(posonlyargs=[], args=[arg(arg='state', annotation=Name(id='SceneState', ctx=Load())), arg(arg='frame', annotation=Name(id='FirstDeploymentFrame', ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Expr(value=Constant(value='Yield from the whole original3D654 invocation, without owning outer RTS.\\n\\n    Other persistent software parents may yield from this function directly.\\n    It neither enters an IRQ nor supplies a pad, clock, status bit or DATA read.\\n    ')), Assign(targets=[Name(id='state', ctx=Store())], value=Call(func=Name(id='checked_state', ctx=Load()), args=[Name(id='state', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_movement_frame', ctx=Load()), args=[Name(id='state', ctx=Load()), Name(id='frame', ctx=Load())], keywords=[])), Expr(value=Call(func=Attribute(value=Name(id='frame', ctx=Load()), attr='validate', ctx=Load()), args=[Name(id='state', ctx=Load()), Constant(value=True)], keywords=[])), If(test=Compare(left=Attribute(value=Name(id='frame', ctx=Load()), attr='status', ctx=Load()), ops=[NotEq()], comparators=[BinOp(left=Attribute(value=Name(id='state', ctx=Load()), attr='sr', ctx=Load()), op=BitAnd(), right=Constant(value=31))]), body=[Raise(exc=Call(func=Name(id='ValueError', ctx=Load()), args=[Constant(value='actual allocation entry full SR and CCR-X must agree')], keywords=[]))], orelse=[]), Return(value=YieldFrom(value=Call(func=Subscript(value=Call(func=Name(id='_make_views', ctx=Load()), args=[], keywords=[]), slice=Constant(value='parent'), ctx=Load()), args=[Call(func=Name(id='SceneRefreshMemory', ctx=Load()), args=[Name(id='state', ctx=Load())], keywords=[]), Name(id='frame', ctx=Load())], keywords=[])))], decorator_list=[], type_params=[])"}, 'duel': {'duel_scene_program': "FunctionDef(name='duel_scene_program', args=arguments(posonlyargs=[], args=[arg(arg='state', annotation=Name(id='SceneState', ctx=Load())), arg(arg='frame', annotation=Name(id='FirstDeploymentFrame', ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Expr(value=Constant(value='Forward the existing whole26DB4 lifetime; its caller owns the outer LONG.\\n\\n    The current PersistentDuelSession retains its37 finite source views and\\n    checks actual callable identities at every resume. No algorithm is copied.\\n    ')), Assign(targets=[Name(id='session', ctx=Store())], value=Call(func=Name(id='PersistentDuelSession', ctx=Load()), args=[Name(id='state', ctx=Load()), Name(id='frame', ctx=Load())], keywords=[])), Assign(targets=[Name(id='current', ctx=Store())], value=Call(func=Attribute(value=Name(id='session', ctx=Load()), attr='start', ctx=Load()), args=[], keywords=[])), While(test=Compare(left=Call(func=Name(id='type', ctx=Load()), args=[Name(id='current', ctx=Load())], keywords=[]), ops=[Is()], comparators=[Name(id='DuelSceneWait', ctx=Load())]), body=[Assign(targets=[Name(id='returned', ctx=Store())], value=Yield(value=Name(id='current', ctx=Load()))), Assign(targets=[Name(id='current', ctx=Store())], value=Call(func=Attribute(value=Name(id='session', ctx=Load()), attr='resume', ctx=Load()), args=[Name(id='returned', ctx=Load()), Attribute(value=Name(id='current', ctx=Load()), attr='poll', ctx=Load())], keywords=[]))], orelse=[]), Return(value=Name(id='current', ctx=Load()))], decorator_list=[], type_params=[])"}}
BATTLE_VIEWS=('_presentation_call_fields','_battle_scene_round_call_fields','run_battle_scene_round_fields')
MAIN_VIEW='continue_campaign_action_display_fields'


def _dump(node):
    return ast.dump(node,include_attributes=False)


def _code_shape(code):
    return tuple(getattr(code,name) for name in (
        'co_code','co_names','co_varnames','co_argcount','co_posonlyargcount',
        'co_kwonlyargcount','co_flags','co_freevars','co_cellvars'))+(tuple(
            _code_shape(value) if type(value)is CodeType else value for value in code.co_consts),)


def _top_code(module_code,name):
    found=[value for value in module_code.co_consts if type(value)is CodeType
        and value.co_name==name and value.co_qualname==name]
    if len(found)!=1:raise ValueError('one complete top-level battle-round owner required: '+name)
    return found[0]


def _cooperative_battle_tree(original_tree):
    """Lift only two algorithm calls, two child branches and eleven propagations."""
    if set(EXPECTED_WHOLE_SOURCES['battle'])!=set(BATTLE_VIEWS):
        raise ValueError('exact three whole battle-round views required')
    result=copy.deepcopy(original_tree);inverse_nodes={}
    for index,node in enumerate(original_tree.body):
        if not isinstance(node,ast.FunctionDef) or node.name not in BATTLE_VIEWS:continue
        if node.name in inverse_nodes or _dump(node)!=EXPECTED_WHOLE_SOURCES['battle'][node.name]:
            raise ValueError('complete battle-round source changed: '+node.name)
        if any(isinstance(item,(ast.Yield,ast.YieldFrom)) for item in ast.walk(node)):
            raise ValueError('original battle-round function must be synchronous')
        expected=({'algorithm':2} if node.name=='_presentation_call_fields' else
            {'run_scene_object_controller_fields':1,'run_duel_scene_fields':1,'_presentation_call_fields':1}
            if node.name=='_battle_scene_round_call_fields' else {'_battle_scene_round_call_fields':10})
        counts={name:0 for name in expected};substitutions=[]

        class Lift(ast.NodeTransformer):
            def visit_Call(self,item):
                item=self.generic_visit(item)
                if not isinstance(item.func,ast.Name) or item.func.id not in expected:return item
                before=copy.deepcopy(item);name=item.func.id;counts[name]+=1
                if name in ('run_scene_object_controller_fields','run_duel_scene_fields'):
                    wanted=('run_scene_object_controller_fields','run_duel_scene_fields').index(name)
                    call=ast.parse(('_battle_round_allocation_program' if wanted==0 else
                        '_battle_round_duel_program')+'(actual_memory.state, entered)').body[0].value
                    if _dump(item)!=_dump(ast.parse(name+'('+('SceneRefreshMemory(actual_memory.state)'
                            if wanted==0 else 'actual_memory.state')+', entered)').body[0].value):
                        raise ValueError('exact original Allocation/Duel child expression required')
                    item=ast.copy_location(call,item)
                substitutions.append((before,copy.deepcopy(item)))
                return ast.copy_location(ast.YieldFrom(value=item),item)

        derived=Lift().visit(copy.deepcopy(node))
        if counts!=expected:raise ValueError('exact battle-round propagation counts differ: '+node.name)
        remaining=list(substitutions)

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self,item):
                for position,(before,after) in enumerate(remaining):
                    if _dump(item.value)==_dump(after):
                        remaining.pop(position)
                        return ast.copy_location(copy.deepcopy(before),item)
                raise ValueError('unknown battle-round cooperative substitution')

        inverse=Inverse().visit(copy.deepcopy(derived))
        if remaining or _dump(inverse)!=_dump(node):
            raise ValueError('complete original battle-round FN inverse differs')
        result.body[index]=derived;inverse_nodes[node.name]=(index,inverse)
    if set(inverse_nodes)!=set(BATTLE_VIEWS):raise ValueError('all three original battle views required')
    restored=copy.deepcopy(result)
    for index,inverse in inverse_nodes.values():restored.body[index]=inverse
    if _dump(restored)!=_dump(original_tree):raise ValueError('whole battle business-module inverse differs')
    ast.fix_missing_locations(result)
    return result


def _cooperative_main_tree(original_tree):
    """498 is a true BRA to DC0, not a new physical CALL or outer RTS pop."""
    result=copy.deepcopy(original_tree);found=[]
    old=ast.parse('_campaign_tail_fields(state, frame, 0xDC0)').body[0].value
    new=ast.parse('battle_scene_round_program(state, frame)').body[0].value
    for index,node in enumerate(original_tree.body):
        if not isinstance(node,ast.FunctionDef) or node.name!=MAIN_VIEW:continue
        if found or _dump(node)!=EXPECTED_WHOLE_SOURCES['main'][MAIN_VIEW]:
            raise ValueError('complete actual Main498 source required')
        count=[]

        class Lift(ast.NodeTransformer):
            def visit_Call(self,item):
                if _dump(item)==_dump(old):
                    count.append(item)
                    return ast.copy_location(ast.YieldFrom(value=copy.deepcopy(new)),item)
                return self.generic_visit(item)

        derived=Lift().visit(copy.deepcopy(node))
        if len(count)!=1:raise ValueError('only actual Main498 BRA tail may propagate')
        inverses=[]

        class Inverse(ast.NodeTransformer):
            def visit_YieldFrom(self,item):
                if _dump(item.value)!=_dump(new):raise ValueError('unknown Main498 propagation')
                inverses.append(item)
                return ast.copy_location(copy.deepcopy(old),item)

        inverse=Inverse().visit(copy.deepcopy(derived))
        if len(inverses)!=1 or _dump(inverse)!=_dump(node):raise ValueError('whole Main498 FN inverse differs')
        result.body[index]=derived;found.append((index,inverse))
    if len(found)!=1:raise ValueError('one complete Main498 view required')
    restored=copy.deepcopy(result);restored.body[found[0][0]]=found[0][1]
    if _dump(restored)!=_dump(original_tree):raise ValueError('whole Main business-module inverse differs')
    ast.fix_missing_locations(result)
    return result


class _BattleRoundPrograms:
    """Finite private views with actual full-module CodeType identity guards."""
    def __init__(self,state):
        from . import business_battle as battle
        from ..high_level_main_flows import business_main as main
        from ..high_level_dynamic_flows import allocation_steps as allocation
        from ..high_level_scene_flows import duel_scene_steps as duel
        self.state=checked_state(state);self.thread=threading.get_ident()
        self.modules=dict(battle=battle,main=main,allocation=allocation,duel=duel)
        self.originals={};self.views={};self.namespaces={}
        for group,module in self.modules.items():
            tree=ast.parse(inspect.getsource(module),filename=module.__file__)
            functions={node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
            plain=compile(tree,module.__file__,'exec',dont_inherit=True)
            for name,expected in EXPECTED_WHOLE_SOURCES[group].items():
                original=getattr(module,name)
                if name not in functions or _dump(functions[name])!=expected or \
                        type(original)is not FunctionType or original.__module__!=module.__name__ or \
                        original.__name__!=name or original.__globals__ is not vars(module) or \
                        original.__closure__ is not None or original.__code__.co_freevars or \
                        _code_shape(_top_code(plain,name))!=_code_shape(original.__code__):
                    raise ValueError('actual complete loaded battle-round source owner required: '+name)
                if inspect.isgeneratorfunction(original)!=(group in ('allocation','duel')):
                    raise ValueError('only the two declared whole child programs may be generators')
                self.originals[group,name]=original
            if group not in ('battle','main'):continue
            derived=(_cooperative_battle_tree if group=='battle' else _cooperative_main_tree)(tree)
            compiled=compile(derived,module.__file__,'exec',dont_inherit=True)
            namespace=dict(vars(module));self.namespaces[group]=namespace
            if any(name in namespace for name in (
                    '_battle_round_allocation_program','_battle_round_duel_program','battle_scene_round_program')):
                raise ValueError('new private battle-round bindings must not replace original business names')
            for name in EXPECTED_WHOLE_SOURCES[group]:
                original=self.originals[group,name]
                view=FunctionType(_top_code(compiled,name),namespace,name,original.__defaults__,None)
                view.__kwdefaults__=original.__kwdefaults__;view.__annotations__=dict(original.__annotations__)
                if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
                    raise ValueError('every finite whole battle-round view must be cooperative')
                self.views[group,name]=view;namespace[name]=view
        self.namespaces['battle'].update(
            _battle_round_allocation_program=self.originals['allocation','allocation_scene_program'],
            _battle_round_duel_program=self.originals['duel','duel_scene_program'])
        self.namespaces['main']['battle_scene_round_program']=battle_scene_round_program

    def require_current(self,state):
        if state is not self.state or threading.get_ident()!=self.thread:
            raise ValueError('battle-round invocation belongs to another Scene or thread')
        for (group,name),original in self.originals.items():
            if getattr(self.modules[group],name)is not original:
                raise ValueError('actual battle-round owner was rebound during invocation: '+name)

    def program(self,frame,main=False):
        self.require_current(self.state)
        if type(main)is not bool:raise ValueError('exact directDC0 or Main498 program role required')
        if main:return self.views['main',MAIN_VIEW](self.state,frame)
        from .contexts_services import SceneRefreshMemory
        return self.views['battle','run_battle_scene_round_fields'](SceneRefreshMemory(self.state),frame)


def _battle_round_forward(programs,program):
    """Forward only genuine same-Scene typed child waits and real IRQ returns."""
    received=None
    while True:
        programs.require_current(programs.state)
        try:waiting=next(program) if received is None else program.send(received)
        except StopIteration as finished:return _movement_frame(programs.state,finished.value)
        if type(waiting) not in (AllocationSceneWait,DuelSceneWait) or waiting.state is not programs.state:
            raise ValueError('actual same-Scene Allocation/Duel wait required')
        received=yield waiting.validate()
        received=_movement_frame(programs.state,received)


def battle_scene_round_program(state: SceneState,frame: FirstDeploymentFrame):
    """WholeDC0..E7C; the caller's original incoming LONG is not added or popped."""
    state=checked_state(state);frame=_movement_frame(state,frame);frame.validate(state,True)
    if frame.status!=(state.sr&31):raise ValueError('actual battle-round full SR/CCR-X required')
    programs=_BattleRoundPrograms(state)
    return (yield from _battle_round_forward(programs,programs.program(frame)))


def battle_main_scene_program(state: SceneState,frame: FirstDeploymentFrame):
    """WholeMain498 actual BRA to the wholeDC0 parent, no invented physical slot."""
    state=checked_state(state);frame=_movement_frame(state,frame);frame.validate(state,True)
    if frame.status!=(state.sr&31):raise ValueError('actual Main498 full SR/CCR-X required')
    programs=_BattleRoundPrograms(state)
    return (yield from _battle_round_forward(programs,programs.program(frame,main=True)))


class BattleRoundSession:
    """One complete original round lifetime, from real DC0 entry through E7A RTS."""
    entry_pc=0xDC0
    completion_pc=0xE7A

    def __init__(self,state: SceneState,frame: FirstDeploymentFrame):
        self.state=checked_state(state);self.entry=_movement_frame(state,frame)
        self.entry.validate(state,True)
        if frame.status!=(state.sr&31):raise ValueError('battle-round entry SR/CCR-X disagree')
        self._programs=_BattleRoundPrograms(state)
        self._program=self._programs.program(frame)
        self._started=self._complete=self._failed=False
        self.waiting=self.result=None;self.suspensions=0

    @property
    def complete(self):return self._complete

    @property
    def failed(self):return self._failed

    def _take(self,received=None):
        self._programs.require_current(self.state)
        try:waiting=next(self._program) if received is None else self._program.send(received)
        except StopIteration as finished:
            try:
                self.result=_movement_frame(self.state,finished.value)
                if self.result.stack_cursor.base!=self.entry.stack_cursor.base:
                    raise Boundary('wholeDC0 round did not preserve its original outer physical SP')
                if self.result.status!=(self.state.sr&31):raise ValueError('round result SR/CCR-X disagree')
            except BaseException:self._failed=True;raise
            self.waiting=None;self._complete=True
            return self.result
        except BaseException:self._failed=True;raise
        try:
            if type(waiting) not in (AllocationSceneWait,DuelSceneWait) or waiting.state is not self.state:
                raise ValueError('one actual same-Scene Allocation/Duel wait required')
            self.waiting=waiting.validate()
        except BaseException:self._failed=True;raise
        self.suspensions+=1
        return self.waiting

    def start(self):
        self._programs.require_current(self.state)
        if self._started:raise ValueError('cannot replay originalDC0 status/head initialization')
        self._started=True
        return self._take()

    def resume(self,returned: FirstDeploymentFrame,pc: int):
        self._programs.require_current(self.state)
        if not self._started or self._complete or self._failed or self.waiting is None:
            raise ValueError('one actual live battle-round suspension required')
        returned=_movement_frame(self.state,returned);returned.validate(self.state,True);uint(pc,32)
        if pc!=self.waiting.poll:
            raise MovementContinuationBoundary(pc,returned,'IRQ did not RTE to the actual nested round wait')
        if returned.stack_cursor.base!=self.waiting.frame.stack_cursor.base:
            raise Boundary('IRQ did not preserve the original battle-round child CALL/WORD stack')
        if self.state.sr!=self.waiting.status_word or returned.status!=(self.state.sr&31):
            raise ValueError('actual IRQ must restore the complete battle-round SR/CCR-X')
        return self._take(returned)
