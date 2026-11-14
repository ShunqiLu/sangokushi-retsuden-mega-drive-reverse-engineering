"""Current whole Scene preparation rules to ordinary fixed-ABI instructions.

These emitters consume effects admitted from the complete editable Scene
catalog. The historical scalar projection frontend is not a code authority.
No ROM, assembly listing, object file or cached generated body is read here.
"""
from .compiler_common import CompileError, Emitter


def _finish(emitter, effects):
    emitter.end()
    binding = emitter.binding
    if sum(row['encoding_bytes'] for row in emitter.mapping) != binding.end - binding.entry:
        raise CompileError('complete Scene preparation rule changed its physical allocation')
    return emitter.unit(effects)


def lower_frame_selection(binding, effects):
    """Lower the four complete live count/assignment/weight/average bodies."""
    e = Emitter(binding)
    e.begin()
    ins, mark = e.ins, e.label
    label = lambda role: binding.name + '_' + role
    branch = lambda operation, role, width=4: ins(operation, label(role), width)
    name = binding.name

    if name == 'count_selected_deployment':
        ins('lea.l', '0xf500:w,%a1', 4)
        ins('clr.w', '%d7')
        mark(label('next'))
        ins('move.w', '(%a1)+,%d0')
        branch('bmi.w', 'done')
        ins('btst.l', '#14,%d0', 4)
        branch('beq.b', 'next', 2)
        ins('addq.w', '#1,%d7')
        branch('bra.b', 'next', 2)
        mark(label('done'))
    elif name == 'initialize_selected_assignment':
        ins('lea.l', '0xa050:w,%a1', 4)
        ins('lea.l', '0xf500:w,%a2', 4)
        ins('lea.l', '0xa150:w,%a4', 4)
        ins('move.b', '4(%a0),%d0', 4)
        ins('lea.l', '0xf427:w,%a3', 4)
        ins('move.w', '0xf392:w,%d1', 4)
        ins('cmp.b', '(%a3,%d1.w),%d0', 4)
        branch('bne.w', 'next')
        ins('bset.l', '#6,%d1', 4)
        mark(label('next'))
        ins('move.w', '(%a2)+,%d0')
        branch('bmi.w', 'done')
        ins('btst.l', '#14,%d0', 4)
        branch('beq.b', 'next', 2)
        ins('andi.w', '#255,%d0', 4)
        ins('move.b', '%d1,(%a1,%d0.w)', 4)
        ins('lsl.w', '#2,%d0')
        ins('clr.l', '(%a4,%d0.w)', 4)
        branch('bra.b', 'next', 2)
        mark(label('done'))
    elif name == 'selected_troop_weights':
        ins('lea.l', '0xf500:w,%a1', 4)
        ins('lea.l', '0xc800:w,%a2', 4)
        ins('moveq', '#0,%d5')
        ins('moveq', '#0,%d6')
        mark(label('next'))
        ins('move.w', '(%a1)+,%d2')
        branch('bmi.w', 'finish')
        ins('move.w', '%d2,%d3')
        ins('lsl.w', '#2,%d3')
        ins('btst.l', '#14,%d2', 4)
        branch('beq.w', 'all')
        ins('add.l', '(%a2,%d3.w),%d5', 4)
        ins('addi.l', '#100,%d5', 6)
        mark(label('all'))
        ins('add.l', '(%a2,%d3.w),%d6', 4)
        ins('addi.l', '#100,%d6', 6)
        branch('bra.b', 'next', 2)
        mark(label('finish'))
        ins('lsr.w', '#5,%d5')
        ins('lsr.w', '#5,%d6')
    elif name == 'refresh_object_attribute_average':
        ins('move.b', '(%a0),%d0')
        ins('andi.w', '#15,%d0', 4)
        ins('move.w', '%d0,%d1')
        ins('subi.b', '#1,%d1', 4)
        ins('lea.l', '0xc400:w,%a1', 4)
        ins('moveq', '#0,%d2')
        ins('clr.w', '%d3')
        mark(label('next'))
        ins('move.b', '13(%a0,%d1.w),%d3', 4)
        ins('add.b', '(%a1,%d3.w),%d2', 4)
        ins('dbra', '%d1,' + label('next'), 4)
        ins('divu.w', '%d0,%d2')
        ins('move.b', '%d2,3(%a0)', 4)
    else:
        raise CompileError('one of the four exact Scene selection Bindings required')
    return _finish(e, effects)
