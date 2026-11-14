"""Persistent view of the whole original3969A scripted-scene owner.

confirmed: the sole cooperative substitution is397CE's actual BYTE/IRQ wait.
The complete original initialization and every unchanged renderer call execute
in their real order. No callable in the business module is rebound, no Boundary
is caught to re-enter a prefix, and no PC/opcode interpreter or host ACK exists.
"""
import ast
import copy
import inspect
import threading
from dataclasses import dataclass
from types import CodeType, FunctionType

from ..high_level_main_flows.domain import SceneState, Boundary, checked_state, uint
from ..high_level_main_flows.contexts_gameplay import FirstDeploymentFrame, MovementContinuationBoundary
from ..high_level_main_flows.business_movement_support import _movement_frame


# The publication producer replaces this one token with the complete reviewed
# original function AST. It is not a runtime source/registry fallback.
EXPECTED_ORIGINAL_AST = "FunctionDef(name='_play_scripted_scene_core', args=arguments(posonlyargs=[], args=[arg(arg='state', annotation=Name(id='SceneState', ctx=Load())), arg(arg='frame', annotation=Name(id='FirstDeploymentFrame', ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Expr(value=Constant(value='3969A unique setup/play loop; remaining mode bodies stay explicit.')), Assign(targets=[Name(id='memory', ctx=Store())], value=Call(func=Name(id='SceneRefreshMemory', ctx=Load()), args=[Name(id='state', ctx=Load())], keywords=[])), Expr(value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='frame', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='status_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value=9984)], keywords=[])), Expr(value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=4294964754), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_refresh_emit', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964754), Constant(value=2), Constant(value=0)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=239454), Constant(value=235174)], keywords=[])), For(target=Tuple(elts=[Name(id='address', ctx=Store()), Name(id='size', ctx=Store())], ctx=Store()), iter=Tuple(elts=[Tuple(elts=[Constant(value=16740398), Constant(value=4)], ctx=Load()), Tuple(elts=[Constant(value=16740410), Constant(value=4)], ctx=Load()), Tuple(elts=[Constant(value=16740352), Constant(value=2)], ctx=Load()), Tuple(elts=[Constant(value=16740356), Constant(value=2)], ctx=Load()), Tuple(elts=[Constant(value=16740414), Constant(value=2)], ctx=Load()), Tuple(elts=[Constant(value=16740406), Constant(value=2)], ctx=Load()), Tuple(elts=[Constant(value=16740420), Constant(value=2)], ctx=Load()), Tuple(elts=[Constant(value=16740412), Constant(value=2)], ctx=Load())], ctx=Load()), body=[Expr(value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Name(id='address', ctx=Load()), Name(id='size', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_refresh_emit', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Name(id='address', ctx=Load()), Name(id='size', ctx=Load()), Constant(value=0)], keywords=[]))], orelse=[]), Assign(targets=[Name(id='mode', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740390), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_compare', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Name(id='mode', ctx=Load()), Constant(value=24), Constant(value=16)], keywords=[])), If(test=Compare(left=Name(id='mode', ctx=Load()), ops=[Eq()], comparators=[Constant(value=24)]), body=[Assign(targets=[Tuple(elts=[Name(id='secondary_x', ctx=Store()), Name(id='secondary_y', ctx=Store())], ctx=Store())], value=Tuple(elts=[Constant(value=96), Constant(value=48)], ctx=Load()))], orelse=[Assign(targets=[Name(id='mode', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740390), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_compare', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Name(id='mode', ctx=Load()), Constant(value=28), Constant(value=16)], keywords=[])), If(test=Compare(left=Name(id='mode', ctx=Load()), ops=[Eq()], comparators=[Constant(value=28)]), body=[Assign(targets=[Tuple(elts=[Name(id='secondary_x', ctx=Store()), Name(id='secondary_y', ctx=Store())], ctx=Store())], value=Tuple(elts=[Constant(value=96), Constant(value=48)], ctx=Load()))], orelse=[Assign(targets=[Tuple(elts=[Name(id='secondary_x', ctx=Store()), Name(id='secondary_y', ctx=Store())], ctx=Store())], value=Tuple(elts=[Constant(value=144), Constant(value=96)], ctx=Load()))])]), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_refresh_emit', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=16740402), Constant(value=2), Name(id='secondary_x', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_refresh_emit', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=16740404), Constant(value=2), Name(id='secondary_y', ctx=Load())], keywords=[])), Assign(targets=[Name(id='mode', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740390), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_x'), Name(id='mode', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_asl_word', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value='target_x'), Name(id='mode', ctx=Load()), Constant(value=1)], keywords=[])), Assign(targets=[Name(id='offset', ctx=Store())], value=Call(func=Name(id='u16', ctx=Load()), args=[BinOp(left=Name(id='mode', ctx=Load()), op=LShift(), right=Constant(value=1))], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='roster', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Constant(value=232328)], keywords=[])), keyword(arg='candidates', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Constant(value=232408)], keywords=[]))])), Assign(targets=[Name(id='x', ctx=Store())], value=Call(func=Attribute(value=Attribute(value=Name(id='frame', ctx=Load()), attr='roster', ctx=Load()), attr='word', ctx=Load()), args=[Name(id='offset', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_y'), Name(id='x', ctx=Load())], keywords=[])), Assign(targets=[Name(id='y', ctx=Store())], value=Call(func=Attribute(value=Attribute(value=Name(id='frame', ctx=Load()), attr='candidates', ctx=Load()), attr='word', ctx=Load()), args=[Name(id='offset', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='unit'), Name(id='y', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_refresh_emit', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=16740392), Constant(value=2), Name(id='x', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_refresh_emit', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=16740394), Constant(value=2), Name(id='y', ctx=Load())], keywords=[])), Assign(targets=[Name(id='mode', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740390), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_x'), Name(id='mode', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='roster', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Constant(value=233040)], keywords=[]))])), Assign(targets=[Name(id='movement', ctx=Store())], value=Call(func=Attribute(value=Attribute(value=Name(id='frame', ctx=Load()), attr='roster', ctx=Load()), attr='byte', ctx=Load()), args=[Name(id='mode', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_byte', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_y'), Name(id='movement', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_refresh_emit', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=16740396), Constant(value=1), Name(id='movement', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_x'), Constant(value=0)], keywords=[])), Assign(targets=[Name(id='mode', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740390), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_compare', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Name(id='mode', ctx=Load()), Constant(value=10), Constant(value=16)], keywords=[])), Assign(targets=[Name(id='video', ctx=Store())], value=Constant(value=0)), If(test=Compare(left=Name(id='mode', ctx=Load()), ops=[Eq()], comparators=[Constant(value=10)]), body=[Assign(targets=[Name(id='video', ctx=Store())], value=Constant(value=8192)), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_x'), Name(id='video', ctx=Load())], keywords=[]))], orelse=[]), Assign(targets=[Name(id='mode', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740390), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='count'), Name(id='mode', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_asl_word', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value='count'), Name(id='mode', ctx=Load()), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='candidates', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Constant(value=231354)], keywords=[]))])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='roster', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Call(func=Attribute(value=Attribute(value=Name(id='frame', ctx=Load()), attr='candidates', ctx=Load()), attr='long', ctx=Load()), args=[Call(func=Name(id='u16', ctx=Load()), args=[BinOp(left=Name(id='mode', ctx=Load()), op=LShift(), right=Constant(value=2))], keywords=[])], keywords=[])], keywords=[]))])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=235096), Constant(value=235378), Name(id='video', ctx=Load())], keywords=[])), Assign(targets=[Name(id='mode', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740390), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_x'), Name(id='mode', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='auxiliary', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Constant(value=231834)], keywords=[]))])), Assign(targets=[Name(id='dual', ctx=Store())], value=Call(func=Attribute(value=Attribute(value=Name(id='frame', ctx=Load()), attr='auxiliary', ctx=Load()), attr='byte', ctx=Load()), args=[Name(id='mode', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_byte', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_y'), Name(id='dual', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_compare', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Name(id='dual', ctx=Load()), Constant(value=1), Constant(value=8)], keywords=[])), If(test=Compare(left=Name(id='dual', ctx=Load()), ops=[Eq()], comparators=[Constant(value=1)]), body=[Assign(targets=[Name(id='mode', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740390), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='count'), Name(id='mode', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_arithmetic', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value='count'), Name(id='mode', ctx=Load()), Constant(value=1), Constant(value=16)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_asl_word', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value='count'), Call(func=Name(id='u16', ctx=Load()), args=[BinOp(left=Name(id='mode', ctx=Load()), op=Add(), right=Constant(value=1))], keywords=[]), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='candidates', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Constant(value=231354)], keywords=[]))])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='roster', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Call(func=Attribute(value=Attribute(value=Name(id='frame', ctx=Load()), attr='candidates', ctx=Load()), attr='long', ctx=Load()), args=[Call(func=Name(id='u16', ctx=Load()), args=[BinOp(left=Call(func=Name(id='u16', ctx=Load()), args=[BinOp(left=Name(id='mode', ctx=Load()), op=Add(), right=Constant(value=1))], keywords=[]), op=LShift(), right=Constant(value=2))], keywords=[])], keywords=[])], keywords=[]))])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_x'), Constant(value=8192)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=235096), Constant(value=235426), Constant(value=8192)], keywords=[]))], orelse=[]), Assign(targets=[Name(id='mode', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740390), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='count'), Name(id='mode', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_asl_word', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value='count'), Name(id='mode', ctx=Load()), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='candidates', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Constant(value=231674)], keywords=[]))])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='roster', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Call(func=Attribute(value=Attribute(value=Name(id='frame', ctx=Load()), attr='candidates', ctx=Load()), attr='long', ctx=Load()), args=[Call(func=Name(id='u16', ctx=Load()), args=[BinOp(left=Name(id='mode', ctx=Load()), op=LShift(), right=Constant(value=2))], keywords=[])], keywords=[])], keywords=[]))])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_copy_scene_palette_longs_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_long', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_x'), Constant(value=0)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='status_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value=9472)], keywords=[])), While(test=Constant(value=True), body=[Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_refresh_emit', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=4294964754), Constant(value=2), Constant(value=1536)], keywords=[])), While(test=Constant(value=True), body=[Assign(targets=[Name(id='value', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=4294964754), Constant(value=1)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_refresh_flags', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Name(id='value', ctx=Load()), Constant(value=1)], keywords=[])), If(test=Compare(left=Name(id='value', ctx=Load()), ops=[Eq()], comparators=[Constant(value=0)]), body=[Break()], orelse=[]), Expr(value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='progress', ctx=Load()), args=[Constant(value='scripted-scene-sound-byte')], keywords=[]))], orelse=[]), Assign(targets=[Name(id='previous', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740414), Constant(value=2)], keywords=[])), Assign(targets=[Tuple(elts=[Name(id='frame', ctx=Store()), Name(id='elapsed', ctx=Store())], ctx=Store())], value=Call(func=Name(id='_movement_binary_flags', ctx=Load()), args=[Name(id='state', ctx=Load()), Name(id='frame', ctx=Load()), Name(id='previous', ctx=Load()), Constant(value=1), Constant(value=16)], keywords=[])), Expr(value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='write', ctx=Load()), args=[Constant(value=16740414), Constant(value=2), Name(id='elapsed', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_long', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_x'), Constant(value=0)], keywords=[])), Assign(targets=[Name(id='mode', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740390), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_x'), Name(id='mode', ctx=Load())], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_asl_word', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value='target_x'), Name(id='mode', ctx=Load()), Constant(value=1)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_long', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_y'), Constant(value=0)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='first_replace', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[keyword(arg='roster', value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='cursor_at', ctx=Load()), args=[Constant(value=231874)], keywords=[]))])), Assign(targets=[Name(id='duration', ctx=Store())], value=Call(func=Attribute(value=Attribute(value=Name(id='frame', ctx=Load()), attr='roster', ctx=Load()), attr='word', ctx=Load()), args=[Call(func=Name(id='u16', ctx=Load()), args=[BinOp(left=Name(id='mode', ctx=Load()), op=LShift(), right=Constant(value=1))], keywords=[])], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_first_word', ctx=Load()), args=[Name(id='frame', ctx=Load()), Constant(value='target_y'), Name(id='duration', ctx=Load())], keywords=[])), Assign(targets=[Name(id='elapsed', ctx=Store())], value=Call(func=Attribute(value=Name(id='state', ctx=Load()), attr='read', ctx=Load()), args=[Constant(value=16740414), Constant(value=2)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_compare', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Name(id='duration', ctx=Load()), Name(id='elapsed', ctx=Load()), Constant(value=16)], keywords=[])), If(test=Compare(left=Name(id='duration', ctx=Load()), ops=[Eq()], comparators=[Name(id='elapsed', ctx=Load())]), body=[Return(value=Call(func=Attribute(value=Name(id='memory', ctx=Load()), attr='sync_status', ctx=Load()), args=[Name(id='frame', ctx=Load())], keywords=[]))], orelse=[]), If(test=Compare(left=Attribute(value=Name(id='frame', ctx=Load()), attr='stack_cursor', ctx=Load()), ops=[Is()], comparators=[Constant(value=None)]), body=[Raise(exc=Call(func=Name(id='SceneRefreshBoundary', ctx=Load()), args=[Constant(value=239406), Name(id='frame', ctx=Load()), Constant(value=235520)], keywords=[]))], orelse=[]), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_scene_render_call_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load()), Constant(value=239406), Constant(value=235520)], keywords=[])), Assign(targets=[Name(id='frame', ctx=Store())], value=Call(func=Name(id='_draw_scripted_scene_frame_fields', ctx=Load()), args=[Name(id='memory', ctx=Load()), Name(id='frame', ctx=Load())], keywords=[]))], orelse=[])], decorator_list=[], returns=Name(id='FirstDeploymentFrame', ctx=Load()), type_params=[])"


def _dump(node):
    return ast.dump(node,include_attributes=False)


def _code_shape(code):
    """Actual structural code identity, including every nested code constant."""
    return tuple(getattr(code,name) for name in (
        'co_code','co_names','co_varnames','co_argcount','co_posonlyargcount',
        'co_kwonlyargcount','co_flags','co_freevars','co_cellvars'))+(tuple(
            _code_shape(value) if type(value)is CodeType else value for value in code.co_consts),)


def _top_function_code(module_code,name):
    candidates=[value for value in module_code.co_consts if type(value)is CodeType
        and value.co_name==name and value.co_qualname==name]
    if len(candidates)!=1:
        raise ValueError('one actual complete top-level scripted-scene code owner required')
    return candidates[0]


def _cooperative_module_tree(original_tree):
    """Exactly one progress expression changes; inverse restores the whole module."""
    tree=copy.deepcopy(original_tree)
    candidates=[node for node in tree.body if type(node)is ast.FunctionDef
        and node.name=='_play_scripted_scene_core']
    if len(candidates)!=1 or _dump(candidates[0])!=EXPECTED_ORIGINAL_AST:
        raise ValueError('exact complete reviewed3969A function AST required')
    original=candidates[0]
    if any(isinstance(node,(ast.Yield,ast.YieldFrom,ast.AsyncFunctionDef)) for node in ast.walk(original)):
        raise ValueError('original scripted-scene owner must not already be cooperative')
    old=ast.parse("state.progress('scripted-scene-sound-byte')").body[0]
    new=ast.parse('frame = (yield ScriptedSceneWait(state, frame, state.sr).validate())').body[0]
    hits=[]

    class Lift(ast.NodeTransformer):
        def visit_Expr(self,node):
            if _dump(node)==_dump(old):
                hits.append(node)
                replacement=copy.deepcopy(new)
                ast.increment_lineno(replacement,node.lineno-1)
                return ast.copy_location(replacement,node)
            return self.generic_visit(node)

    lifted=Lift().visit(copy.deepcopy(original))
    if len(hits)!=1:
        raise ValueError('exact one original397CE asynchronous progress site required')
    inverse_hits=[]

    class Inverse(ast.NodeTransformer):
        def visit_Assign(self,node):
            if _dump(node)==_dump(new):
                inverse_hits.append(node)
                return ast.copy_location(copy.deepcopy(old),node)
            return self.generic_visit(node)

    inverse=Inverse().visit(copy.deepcopy(lifted))
    if len(inverse_hits)!=1 or _dump(inverse)!=_dump(original):
        raise ValueError('whole scripted-scene function inverse differs')
    index=tree.body.index(original)
    tree.body[index]=lifted
    restored=copy.deepcopy(tree)
    restored.body[index]=inverse
    if _dump(restored)!=_dump(original_tree):
        raise ValueError('entire scripted-scene business module inverse differs')
    ast.fix_missing_locations(tree)
    return tree


def _make_scripted_scene_program(state,frame):
    """Compile complete modules without executing imports/body; bind one private view.

    Complete-module context is retained on both sides, including Python3.13's
    import/name code-generation context. Source identity never drops co_code,
    nested constants or any complete-function inverse to make a candidate pass.
    """
    from . import business_scene
    name='_play_scripted_scene_core'
    original=getattr(business_scene,name)
    if (type(original)is not FunctionType or original.__module__!=business_scene.__name__
            or original.__name__!=name or original.__globals__ is not vars(business_scene)
            or original.__closure__ is not None or original.__code__.co_freevars
            or inspect.isgeneratorfunction(original)):
        raise ValueError('actual complete unwrapped scripted-scene function required')
    filename=original.__code__.co_filename
    tree=ast.parse(inspect.getsource(business_scene),filename=filename)
    plain=compile(tree,filename,'exec',dont_inherit=True)
    plain_code=_top_function_code(plain,name)
    if _code_shape(plain_code)!=_code_shape(original.__code__):
        raise ValueError('loaded whole scripted-scene owner differs from actual complete-module source')
    cooperative_tree=_cooperative_module_tree(tree)
    cooperative_code=_top_function_code(compile(cooperative_tree,filename,'exec',dont_inherit=True),name)
    namespace=dict(original.__globals__)
    if 'ScriptedSceneWait' in namespace:
        raise ValueError('scripted-scene private Wait namespace must not replace a business binding')
    namespace['ScriptedSceneWait']=ScriptedSceneWait
    view=FunctionType(cooperative_code,namespace,name,original.__defaults__,None)
    view.__kwdefaults__=original.__kwdefaults__
    view.__annotations__=dict(original.__annotations__)
    if not inspect.isgeneratorfunction(view) or view.__closure__ is not None:
        raise ValueError('one complete private cooperative scripted-scene view required')
    return view(state,frame)


@dataclass(frozen=True)
class ScriptedSceneWait:
    """One actual397CE TST.B poll with full software state and no clock/ACK."""
    state: SceneState
    frame: FirstDeploymentFrame
    status_word: int
    poll: int = 0x397CE

    @property
    def stage(self):
        return 'original_scripted_scene_frame'

    def validate(self):
        checked_state(self.state)
        _movement_frame(self.state,self.frame)
        uint(self.status_word,16)
        if self.poll!=0x397CE:
            raise ValueError('actual original397CE scripted-scene BYTE wait required')
        if self.status_word!=self.state.sr or self.frame.status!=(self.status_word&31):
            raise ValueError('scripted-scene wait must retain actual complete Scene SR and CCR-X')
        return self


class PersistentScriptedSceneSession:
    """One whole3969A invocation; initialization and real CALL stack remain live.

    A caller delivers actual external IRQs through the existing runtime at the
    exposed poll and resumes with its real complete frame. It does not supply a
    result/elapsed value and cannot replay the prefix after failure or finish.
    Completion is only the original duration-equality branch to397FA RTS; the
    incoming outer return LONG belongs to the original caller, not this class.
    """
    entry_pc=0x3969A
    completion_pc=0x397FA

    def __init__(self,state: SceneState,frame: FirstDeploymentFrame):
        self.state=checked_state(state)
        self.entry=_movement_frame(state,frame)
        if frame.status!=(state.sr&31):
            raise ValueError('scripted-scene entry CCR and actual full SR disagree')
        self._thread=threading.get_ident()
        self._program=_make_scripted_scene_program(state,frame)
        self._started=self._complete=self._failed=False
        self.waiting=self.result=None
        self.suspensions=0

    @property
    def complete(self):
        return self._complete

    @property
    def failed(self):
        return self._failed

    def _same_thread(self):
        if threading.get_ident()!=self._thread:
            raise ValueError('one original scripted-scene invocation must stay on its actual thread')

    def _take(self,received=None):
        self._same_thread()
        try:
            waiting=next(self._program) if received is None else self._program.send(received)
        except StopIteration as finished:
            self.result=_movement_frame(self.state,finished.value)
            if self.result.stack_cursor.base!=self.entry.stack_cursor.base:
                self._failed=True
                raise Boundary('completed scripted-scene owner did not retain its incoming physical SP')
            if self.result.status!=(self.state.sr&31):
                self._failed=True
                raise ValueError('completed scripted-scene frame and actual full Scene SR disagree')
            self.waiting=None
            self._complete=True
            return self.result
        except BaseException:
            self._failed=True
            raise
        if type(waiting)is not ScriptedSceneWait or waiting.state is not self.state:
            self._failed=True
            raise ValueError('one actual same-Scene scripted-scene wait required')
        try:
            self.waiting=waiting.validate()
        except BaseException:
            self._failed=True
            raise
        self.suspensions+=1
        return self.waiting

    def start(self):
        self._same_thread()
        if self._started:
            raise ValueError('cannot replay original3969A initialization')
        self._started=True
        return self._take()

    def resume(self,returned: FirstDeploymentFrame,pc: int):
        self._same_thread()
        if not self._started or self._complete or self._failed or self.waiting is None:
            raise ValueError('one live suspended original3969A invocation required')
        returned=_movement_frame(self.state,returned)
        uint(pc,32)
        if pc!=self.waiting.poll:
            raise MovementContinuationBoundary(pc,returned,'IRQ did not return to original397CE BYTE poll')
        if returned.stack_cursor.base!=self.waiting.frame.stack_cursor.base:
            raise Boundary('IRQ return did not preserve actual scripted-scene SP')
        if self.state.sr!=self.waiting.status_word or returned.status!=(self.state.sr&31):
            raise ValueError('actual IRQ RTE did not restore scripted-scene complete SR/CCR-X')
        return self._take(returned)


def run_scripted_scene_blocking_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Optional retained-Session boundary; never catches a failure to replay it."""
    session=PersistentScriptedSceneSession(state,frame)
    returned=session.start()
    if type(returned)is ScriptedSceneWait:
        boundary=MovementContinuationBoundary(returned.poll,returned.frame,
            'original scripted-scene wait requires actual external IRQ progress')
        boundary.scripted_scene_session=session
        boundary.scripted_scene_wait=returned
        raise boundary
    return returned
