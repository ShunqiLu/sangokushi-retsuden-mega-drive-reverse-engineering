"""Lower the four complete deployment queue/carry Scene functions.

The selection compiler admits the current complete business_city functions
before calling this backend. ``effects`` is that admitted whole-function
record, not the historical PreparationState projection. Emission uses the
fixed original Frame ABI; no assembly listing, object, ROM or old snapshot is
read here. Original quirks, partial-register writes and full-SR operations are
intentionally retained.
"""
from .compiler_common import CompileError, Emitter


def _submit_deployment_queue(emitter):
    """Preserve A0, append the six-byte record, and call its real cleanup."""
    ins, mark = emitter.ins, emitter.label
    check_city = emitter.fresh('check_city')
    restore = emitter.fresh('restore_object')
    ins('move.l', '%a0,-(%a7)')
    ins('cmpi.w', '#521,0xf612:w', 6)
    ins('bne.w', check_city, 4)
    ins('cmpi.w', '#5,0xf362:w', 6)
    ins('beq.w', restore, 4)
    mark(check_city)
    ins('move.w', '0xf392:w,%d0', 4)
    ins('lea.l', '0xea37:w,%a1', 4)
    ins('btst.b', '#1,(%a1,%d0.w)', 6)
    ins('bne.w', restore, 4)
    ins('move.b', '#2,(%a1,%d0.w)', 6)
    ins('move.b', '13(%a0),%d0', 4)
    ins('lea.l', '0xff3000:l,%a1', 6)
    ins('adda.w', '0xff3826:l,%a1', 6)
    ins('move.b', '#0,(%a1)+', 4)
    ins('move.b', '%d0,(%a1)+')
    ins('move.b', '3(%a0),(%a1)+', 4)
    ins('move.b', '#128,(%a1)+', 4)
    ins('move.b', '0xf393:w,(%a1)+', 4)
    ins('clr.b', '(%a1)+')
    ins('move.b', '#255,(%a1)', 4)
    ins('addi.w', '#6,0xff3826:l', 8)
    # The BSR owns the physical return LONG at 1B574. The final MOVEA
    # restores the independently saved object pointer without changing CCR.
    ins('bsr.w', 'clear_original_tail_coordinate', 4)
    mark(restore)
    ins('movea.l', '(%a7)+,%a0')


def _clear_original_tail_coordinate(emitter):
    """Keep the original one-member comparison and DBRA-to-itself quirk."""
    ins = emitter.ins
    latch = emitter.fresh('counter_latch')
    ins('lea.l', '0xcc00:w,%a0', 4)
    ins('move.w', '0xf68a:w,%d0', 4)
    ins('move.w', '#255,%d1', 4)
    ins('lea.l', '0xa150:w,%a1', 4)
    ins('cmp.b', '(%a0,%d1.w),%d0', 4)
    ins('bne.w', latch, 4)
    ins('move.w', '%d1,%d2')
    ins('lsl.w', '#2,%d2')
    ins('clr.l', '(%a1,%d2.w)', 4)
    emitter.label(latch)
    # Do not turn this into a roster scan: the branch target is this very
    # DBRA, so only D1's low WORD changes after the single comparison.
    ins('dbra', '%d1,' + latch, 4)


def _compact_active_deployment_queue(emitter):
    """Search the actual delimited queues and copy with live A0 ordering."""
    ins, mark = emitter.ins, emitter.label
    next_record = emitter.fresh('next_record')
    delimiter = emitter.fresh('delimiter')
    matched = emitter.fresh('matched_record')
    next_pair = emitter.fresh('next_pair')
    copy_pair = emitter.fresh('copy_pair')
    done = emitter.fresh('done')
    ins('lea.l', '0x9000:w,%a0', 4)
    ins('lea.l', '0xefbe:w,%a1', 4)
    ins('move.w', '0xefc6:w,%d0', 4)
    ins('adda.w', '(%a1,%d0.w),%a0', 4)
    ins('move.b', '13(%a0),%d0', 4)
    ins('lea.l', '0xff3000:l,%a0', 6)
    mark(next_record)
    ins('tst.b', '(%a0)')
    ins('bmi.w', done, 4)
    ins('cmp.b', '1(%a0),%d0', 4)
    ins('beq.w', matched, 4)
    ins('addq.w', '#2,%a0')
    mark(delimiter)
    ins('tst.b', '(%a0)+')
    ins('bne.b', delimiter)
    ins('bra.b', next_record)
    mark(matched)
    ins('cmpi.b', '#144,3(%a0)', 6)
    ins('bne.w', done, 4)
    ins('lea.l', '0xff39b2:l,%a0', 6)
    ins('adda.w', '0xff3bb2:l,%a0', 6)
    mark(next_pair)
    ins('tst.b', '(%a0)+')
    ins('beq.w', done, 4)
    ins('cmp.b', '(%a0)+,%d0')
    ins('bne.b', next_pair)
    mark(copy_pair)
    # Both destination EAs use A0 after the corresponding source
    # postincrement, exactly as in the complete Scene function.
    ins('move.b', '(%a0)+,-3(%a0)', 4)
    ins('beq.w', done, 4)
    ins('move.b', '(%a0)+,-3(%a0)', 4)
    ins('bra.b', copy_pair)
    mark(done)


def _deployment_force_carry(emitter):
    """Compare both live forces and retain the privileged full-SR RMW."""
    ins, mark = emitter.ins, emitter.label
    clear = emitter.fresh('clear_carry')
    done = emitter.fresh('done')
    ins('movea.l', '0xff382c:l,%a0', 6)
    ins('move.b', '4(%a0),%d0', 4)
    for address in ('f67b', 'f67d', 'f67f'):
        ins('cmp.b', '0x' + address + ':w,%d0', 4)
        ins('beq.w', clear, 4)
    ins('lea.l', '0x9000:w,%a0', 4)
    ins('lea.l', '0xefbe:w,%a1', 4)
    ins('move.w', '0xefc6:w,%d0', 4)
    ins('adda.w', '(%a1,%d0.w),%a0', 4)
    ins('move.b', '4(%a0),%d0', 4)
    for address in ('f67b', 'f67d', 'f67f'):
        ins('cmp.b', '0x' + address + ':w,%d0', 4)
        ins('beq.w', clear, 4)
    ins('ori.w', '#1,%sr', 4)
    ins('bra.w', done, 4)
    mark(clear)
    ins('andi.w', '#65534,%sr', 4)
    mark(done)


_LOWERERS = {
    'submit_deployment_queue': _submit_deployment_queue,
    'clear_original_tail_coordinate': _clear_original_tail_coordinate,
    'compact_active_deployment_queue': _compact_active_deployment_queue,
    'deployment_force_carry': _deployment_force_carry,
}


def lower_frame_selection_tail(binding, effects):
    """Return one ordinary native unit from an admitted whole Scene body.

    The caller owns complete source/effect admission. This backend preserves
    those exact effect records in the returned unit and emits only the four
    exact current Binding names, with the declared complete byte extent.
    """
    emitter = Emitter(binding)
    if binding.name not in _LOWERERS:
        raise CompileError('one of the four complete Scene queue/carry Bindings required')
    emitter.begin()
    _LOWERERS[binding.name](emitter)
    emitter.end()
    if sum(row['encoding_bytes'] for row in emitter.mapping) != binding.end - binding.entry:
        raise CompileError('complete Scene queue/carry rule changed its physical allocation')
    return emitter.unit(effects)
