"""Typed counted-scan/eligibility FLOW subset lowered to ordinary target operations.

The accepted syntax is a declared semantic topology, not an arbitrary Python
compiler. Every control and expression is consumed; only named typed value
slots below can vary without a new layout. No input byte/assembly payload,
source digest or original sample is consulted.
"""
import ast
from .compiler_common import CompileError, Emitter, require_declared_names
from .target import SELECTION_BINDINGS, TABLE_BINDINGS, SCALAR_BINDINGS


def n(name): return ('name', name)
def i(value): return ('integer', value)
def c(name, *args): return ('call', n(name), tuple(args))
def m(base, name, *args): return ('call', ('attribute', n(base), name), tuple(args))
def view(name): return ('attribute', n('state'), name)
def a(name, value): return ('assign', name, value)
def b(op, left, right): return ('binary', op, left, right)
def cmp(op, left, right): return ('compare', op, left, right)

FLOW = {
 'count_force_cities': (
    a('selector', c('u16', n('selector'))),
    a('assignments', ('call', ('attribute', view('force_city_assignments'), 'cursor'), ())),
    a('count', c('u16', i(0))),
    ('for', 'remaining', c('descending_inclusive', ('slot', 'city_count_latch', 16)), (
        ('if', cmp('Eq', m('assignments', 'next_byte'), c('low8', n('selector'))), (
            a('count', c('u16', b('Add', n('count'), i(1)))),), ()),)),
    ('return', n('count')),
 ),
 'select_force_by_city_count': (
    a('heads', view('force_heads')),
    a('row', ('call', ('attribute', view('force_rows'), 'cursor'), ())),
    a('row_offset', c('u16', b('LShift', m('state', 'force_selector'), i(4)))),
    a('row', m('row', 'at', n('row_offset'))),
    a('best', c('u16', i(0))), a('selected', c('u16', i(65535))),
    a('remaining', c('u16', ('slot', 'force_count_latch', 16))),
    a('mask_offset', c('u16', b('LShift', m('state', 'force_selector'), i(1)))),
    a('masks', view('force_masks')), a('mask', m('masks', 'word', n('mask_offset'))),
    ('for', 'candidate', c('descending_inclusive', n('remaining')), (
        a('value', m('row', 'previous_byte')),
        ('if', cmp('Gt', n('value'), ('slot', 'row_eligibility', 8)), (('continue',),), ()),
        ('if', b('BitAnd', n('mask'), b('LShift', i(1), n('candidate'))), (('continue',),), ()),
        a('head_offset', c('u16', b('LShift', n('candidate'), i(1)))),
        ('if', c('negative_word', m('heads', 'word', n('head_offset'))), (('continue',),), ()),
        a('count', c('count_force_cities', n('state'), n('candidate'))),
        ('if', cmp('Gt', n('count'), n('best')), (a('best', n('count')), a('selected', n('candidate'))), ()),
    )),
    ('return', ('tuple', (n('best'), n('selected')))),
 ),
}
APPROVED = {'AiState', 'Word', 'descending_inclusive', 'low8', 'negative_word', 'u16'}
SIGNATURES = {
 'count_force_cities': (('state', 'AiState'), ('selector', 'Word')),
 'select_force_by_city_count': (('state', 'AiState'),),
}


def expression(node):
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load): return n(node.id)
    if isinstance(node, ast.Constant):
        if type(node.value) is int: return i(node.value)
        if node.value is None: return ('none',)
        raise CompileError('typed numeric expressions reject bool/float/string')
    if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
        return ('attribute', expression(node.value), node.attr)
    if isinstance(node, ast.Call) and not node.keywords:
        return ('call', expression(node.func), tuple(expression(arg) for arg in node.args))
    if isinstance(node, ast.BinOp): return b(type(node.op).__name__, expression(node.left), expression(node.right))
    if isinstance(node, ast.Compare) and len(node.ops)==len(node.comparators)==1:
        return cmp(type(node.ops[0]).__name__, expression(node.left), expression(node.comparators[0]))
    if isinstance(node, ast.Tuple) and isinstance(node.ctx, ast.Load): return ('tuple', tuple(expression(v) for v in node.elts))
    raise CompileError('unsupported typed selection expression')


def statement(node):
    if isinstance(node, ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
        return a(node.targets[0].id, expression(node.value))
    if isinstance(node, ast.If):
        return ('if', expression(node.test), tuple(statement(s) for s in node.body), tuple(statement(s) for s in node.orelse))
    if isinstance(node, ast.For) and isinstance(node.target,ast.Name) and not node.orelse:
        return ('for', node.target.id, expression(node.iter), tuple(statement(s) for s in node.body))
    if isinstance(node, ast.Continue): return ('continue',)
    if isinstance(node, ast.Return): return ('return', expression(node.value))
    raise CompileError('unsupported selection control or statement')


def match(actual, expected, slots):
    if type(expected) is tuple and expected and expected[0]=='slot':
        _, role, bits = expected
        if type(actual) is not tuple or len(actual)!=2 or actual[0]!='integer' or type(actual[1]) is not int or not 0<=actual[1]<1<<bits:
            raise CompileError('strict typed semantic value slot required: '+role)
        if role in slots and slots[role]!=actual[1]: raise CompileError('inconsistent live selection slot: '+role)
        slots[role]=actual[1]; return
    if type(actual) is not type(expected): raise CompileError('unsupported semantic topology or type edit')
    if type(expected) is tuple:
        if len(actual)!=len(expected): raise CompileError('complete semantic control/argument shape required')
        for a_, e_ in zip(actual,expected): match(a_,e_,slots)
    elif actual!=expected: raise CompileError('unsupported semantic selection operation edit')


def parse_source(source):
    if type(source) is not str: raise CompileError('explicit semantic source text required')
    try: tree=ast.parse(source)
    except SyntaxError as error: raise CompileError(str(error)) from error
    functions={}; imported=set()
    for node in tree.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str: continue
        if isinstance(node,ast.ImportFrom) and node.level==1 and node.module=='domain':
            for alias in node.names:
                if alias.asname or alias.name not in APPROVED: raise CompileError('approved explicit domain binding required')
                imported.add(alias.name)
        elif isinstance(node,ast.FunctionDef):
            if node.name not in FLOW or node.name in functions or node.decorator_list or node.type_params: raise CompileError('complete unique non-generic selection functions required')
            args=node.args
            if args.vararg or args.kwarg or args.kwonlyargs or args.posonlyargs or args.defaults:
                raise CompileError('explicit typed original argument shape required')
            if len(args.args)!=len(SIGNATURES[node.name]): raise CompileError('typed signature arity differs')
            for arg,(name,kind) in zip(args.args,SIGNATURES[node.name]):
                if arg.arg!=name or not isinstance(arg.annotation,ast.Name) or arg.annotation.id!=kind:
                    raise CompileError('typed ABI signature differs')
            if node.name=='count_force_cities':
                if not isinstance(node.returns,ast.Name) or node.returns.id!='Word': raise CompileError('explicit WORD result required')
            else:
                result=node.returns
                if not (isinstance(result,ast.Subscript) and isinstance(result.value,ast.Name) and result.value.id=='tuple'
                    and isinstance(result.slice,ast.Tuple) and len(result.slice.elts)==2 and all(isinstance(v,ast.Name) and v.id=='Word' for v in result.slice.elts)):
                    raise CompileError('explicit two-WORD result required')
            locals_={arg.arg for arg in args.args}|{n_.id for n_ in ast.walk(node) if isinstance(n_,ast.Name) and isinstance(n_.ctx,ast.Store)}
            if locals_ & (APPROVED|set(FLOW)): raise CompileError('typed local shadows an imported intrinsic/function')
            functions[node.name]=node
        else: raise CompileError('unsupported module declaration')
    if set(functions)!=set(FLOW): raise CompileError('both complete original selection bodies required')
    require_declared_names(functions,imported)
    slots={}
    for name,node in functions.items():match(tuple(statement(s) for s in node.body),FLOW[name],slots)
    if slots['force_count_latch'] > 15:
        raise CompileError('force-count edit admits only bits 0..15 of the live WORD mask')
    return slots


def short_view(name, register): return f"0x{TABLE_BINDINGS[name]['address']&65535:x}:w,%{register}"
def scalar(name): return f"0x{SCALAR_BINDINGS[name]['address']&65535:x}:w"


def compile_selection(source):
    values=parse_source(source);units=[]
    for binding in SELECTION_BINDINGS:
        e=Emitter(binding);e.begin()
        if binding.name=='count_force_cities':
            loop=e.fresh('count_loop');skip=e.fresh('not_member')
            e.ins('lea.l',short_view('force_city_assignments','a0'),4)
            e.ins('clr.w','%d1');e.ins('move.w',f"#0x{values['city_count_latch']:x},%d2",4)
            e.label(loop);e.ins('cmp.b','(%a0)+,%d0');e.ins('bne.w',skip,4)
            e.ins('addq.w','#1,%d1');e.label(skip);e.ins('dbra','%d2,'+loop,4)
        else:
            loop=e.fresh('candidate_loop');skip=e.fresh('candidate_next')
            e.ins('lea.l',short_view('force_heads','a3'),4)
            pc=binding.entry+sum(i_['encoding_bytes'] for i_ in e.mapping)
            displacement=TABLE_BINDINGS['force_rows']['address']-(pc+2)
            if not -32768<=displacement<=32767:raise CompileError('original readonly PC displacement width')
            e.ins('lea.l',f'{displacement}(%pc),%a1',4);e.ins('nop')
            e.ins('move.w',scalar('force_selector')+',%d0',4);e.ins('lsl.w','#4,%d0');e.ins('adda.w','%d0,%a1')
            e.ins('clr.w','%d3');e.ins('move.w','#0xffff,%d4',4)
            e.ins('move.w',f"#0x{values['force_count_latch']:x},%d0",4)
            e.ins('move.w',scalar('force_selector')+',%d5',4);e.ins('lsl.w','#1,%d5')
            e.ins('lea.l',short_view('force_masks','a2'),4);e.ins('move.w','0(%a2,%d5.w),%d5',4)
            e.label(loop);e.ins('cmpi.b',f"#0x{values['row_eligibility']:x},-(%a1)",4)
            e.ins('bhi.w',skip,4);e.ins('btst.l','%d0,%d5');e.ins('bne.w',skip,4)
            e.ins('move.w','%d0,%d6');e.ins('lsl.w','#1,%d6');e.ins('tst.w','0(%a3,%d6.w)',4)
            e.ins('bmi.w',skip,4);e.ins('bsr.b','count_force_cities');e.ins('cmp.w','%d3,%d1')
            e.ins('bls.w',skip,4);e.ins('move.w','%d1,%d3');e.ins('move.w','%d0,%d4')
            e.label(skip);e.ins('dbra','%d0,'+loop,4)
        e.end()
        if sum(i_['encoding_bytes'] for i_ in e.mapping)!=binding.end-binding.entry:raise CompileError('typed original allocation differs')
        units.append(e.unit(dict(typed_semantic_values=values,ordinary_completion=True,natural_domain='unknown',live_DATA=True)))
    return dict(units=units,effects={u['binding']['name']:u['effects'] for u in units},new_bytes=110,instructions=sum(len(u['instructions']) for u in units),original_generation_input=False)
