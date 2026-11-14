"""Editable movement, arrival and neighbor rules with a finite target compiler."""
from .domain import MovementState,GameState,ReadOnlyData,Table,Cursor,Boundary,PathResult,PathCoordinates,CarryOutcome,BlockingMaskContext

def compile_modules(*texts):
    from .compiler_common import compile_modules as compile_texts
    return compile_texts(*texts)
