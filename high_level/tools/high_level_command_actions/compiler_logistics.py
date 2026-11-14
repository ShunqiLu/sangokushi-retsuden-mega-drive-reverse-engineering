"""Draft restricted logistics semantic AST admission and ordinary target emission.

Business rules remain separate. Generation reads explicit source text only.
Not an arbitrary Python compiler or an independent behavior acceptance.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import LOGISTICS_BINDINGS

APPROVED = {'business_reuse': {'count_selected_deployment',
                    'initialize_selected_assignment',
                    'refresh_object_attribute_average',
                    'selected_troop_weights',
                    'signed_divmod',
                    'submit_deployment_queue'},
 'contexts_logistics': {'ResourceShare', 'DeploymentResult'},
 'domain': {'GameState',
            'Long',
            'Table',
            'Word',
            'checked_state',
            'checked_table',
            'descending_inclusive',
            'high16',
            'low16',
            'negative_word',
            'read_packed_long',
            'replace_word',
            'store_packed_long_reverse',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'}}

DECLARATIONS = {'deploy_selected_group': {'signature': 'state: GameState',
                           'returns': 'DeploymentResult',
                           'flow': 'checked_state(state)\n'
                                   "group = state.table(state.scalar('active_descriptor'))\n"
                                   'submit_deployment_queue(state, group)\n'
                                   'selected = count_selected_deployment(state)\n'
                                   'initialize_selected_assignment(state, group)\n'
                                   'transfer_selected_group_resources(state, group, selected)\n'
                                   'following = remove_deployed_group_members(state, group, '
                                   'selected)\n'
                                   'return DeploymentResult(following, selected)'},
 'transfer_selected_group_resources': {'signature': 'state: GameState, group: Table, '
                                                    'selected_count: Word',
                                       'returns': 'None',
                                       'flow': 'checked_state(state)\n'
                                               'checked_table(group, state)\n'
                                               'uint(selected_count, 16)\n'
                                               'if selected_count != '
                                               "state.scalar('candidate_member_count'):\n"
                                               '    selected_weight, total_weight = '
                                               'selected_troop_weights(state)\n'
                                               '    share = split_group_resource_share(state, '
                                               'read_packed_long(group, 5), selected_weight, '
                                               'total_weight)\n'
                                               "    state.set_scalar('action_amount', "
                                               'share.selected)\n'
                                               '    store_packed_long_reverse(group, 5, '
                                               'share.remaining)\n'
                                               '    share = split_group_resource_share(state, '
                                               'read_packed_long(group, 9), selected_weight, '
                                               'total_weight)\n'
                                               "    state.set_scalar('training_cost', "
                                               'share.selected)\n'
                                               '    store_packed_long_reverse(group, 9, '
                                               'share.remaining)\n'
                                               'else:\n'
                                               "    state.set_scalar('action_amount', "
                                               'read_packed_long(group, 5))\n'
                                               "    state.set_scalar('training_cost', "
                                               'read_packed_long(group, 9))\n'
                                               'owner = group.byte(0, 4)\n'
                                               "city = state.scalar('deployment_city')\n"
                                               'if owner != state.city_owner_bytes.byte(city):\n'
                                               "    index = u16(state.scalar('deployment_city') << "
                                               '2)\n'
                                               '    amount = '
                                               'u32(state.city_battle_gold.long(index) + '
                                               "state.scalar('action_amount'))\n"
                                               '    if amount > 999999:\n'
                                               '        amount = 999999\n'
                                               '    state.city_battle_gold.set_long(index, '
                                               'amount)\n'
                                               '    amount = '
                                               'u32(state.city_battle_food.long(index) + '
                                               "state.scalar('training_cost'))\n"
                                               '    if amount > 999999:\n'
                                               '        amount = 999999\n'
                                               '    state.city_battle_food.set_long(index, '
                                               'amount)\n'
                                               'else:\n'
                                               "    index = u16(state.scalar('deployment_city') << "
                                               '1)\n'
                                               '    amount = u32(state.city_gold.long(index) + '
                                               "state.scalar('action_amount'))\n"
                                               '    if amount > 999999:\n'
                                               '        amount = 999999\n'
                                               '    state.city_gold.set_long(index, amount)\n'
                                               '    amount = u32(state.city_food.long(index) + '
                                               "state.scalar('training_cost'))\n"
                                               '    if amount > 999999:\n'
                                               '        amount = 999999\n'
                                               '    state.city_food.set_long(index, amount)',
                                       'slots': {999999: ('resource_cap', 0, 2147483647)}},
 'split_group_resource_share': {'signature': 'state: GameState, amount: Long, selected_weight: '
                                             'Long, total_weight: Long',
                                'returns': 'ResourceShare',
                                'flow': 'checked_state(state)\n'
                                        'uint(amount, 32)\n'
                                        'uint(selected_weight, 32)\n'
                                        'uint(total_weight, 32)\n'
                                        'scaled = amount >> 5\n'
                                        'numerator = u32(low16(scaled) * low16(selected_weight))\n'
                                        'upper_product = u32(high16(scaled) * '
                                        'low16(selected_weight))\n'
                                        'numerator = u32(numerator + swap_words(upper_product))\n'
                                        'quotient, remainder = signed_divmod(state, numerator, '
                                        'total_weight)\n'
                                        'fraction = replace_word(quotient, u16(low16(quotient) << '
                                        '5))\n'
                                        'fraction = u32(fraction + ((amount & 31) >> 1))\n'
                                        'return ResourceShare(fraction, u32(amount - fraction))'},
 'remove_deployed_group_members': {'signature': 'state: GameState, group: Table, selected_count: '
                                                'Word',
                                   'returns': 'Table',
                                   'flow': 'checked_state(state)\n'
                                           'checked_table(group, state)\n'
                                           'uint(selected_count, 16)\n'
                                           'if selected_count != '
                                           "state.scalar('candidate_member_count'):\n"
                                           '    following = group.cursor(u16((group.byte() & 15) + '
                                           '13))\n'
                                           '    destination = group.cursor(13)\n'
                                           '    roster = state.candidate_roster.cursor()\n'
                                           '    retained_count = 0\n'
                                           '    while True:\n'
                                           '        member = roster.next_word()\n'
                                           '        if negative_word(member):\n'
                                           '            break\n'
                                           '        if member & 16384:\n'
                                           '            continue\n'
                                           '        destination.append_byte(u8(member))\n'
                                           '        retained_count = u16(retained_count + 1)\n'
                                           '    group.set_byte(0, u8(retained_count | 16))\n'
                                           '    while True:\n'
                                           '        count = following.byte() & 15\n'
                                           '        if count == 0:\n'
                                           '            break\n'
                                           '        for _ in descending_inclusive(u16(count + '
                                           '12)):\n'
                                           '            '
                                           'destination.append_byte(following.next_byte())\n'
                                           '    destination.set_byte(0, 0)\n'
                                           '    refresh_object_attribute_average(state, group, '
                                           'retained_count)\n'
                                           '    return group\n'
                                           'following = group.cursor(u16((group.byte() & 15) + '
                                           '13))\n'
                                           'destination = group.cursor()\n'
                                           'while True:\n'
                                           '    count = following.byte() & 15\n'
                                           '    if count == 0:\n'
                                           '        break\n'
                                           '    for _ in descending_inclusive(u16(count + 12)):\n'
                                           '        '
                                           'destination.append_byte(following.next_byte())\n'
                                           'destination.set_byte(0, 0)\n'
                                           'return destination'}}

def _lower_deploy_selected_group(e,rules):
    e.label('action_pc_01b246')
    e.ins('movea.l','0xff382c:l,%a0',6)
    e.label('action_pc_01b24c')
    e.ins('bsr.w','action_pc_01b512',4)
    e.label('action_pc_01b250')
    e.ins('bsr.w','action_pc_01b262',4)
    e.label('action_pc_01b254')
    e.ins('bsr.w','action_pc_01b27a',4)
    e.label('action_pc_01b258')
    e.ins('bsr.w','action_pc_01b2bc',4)
    e.label('action_pc_01b25c')
    e.ins('bsr.w','action_pc_01b472',4)
    e.label('action_pc_01b260')
    e.ins('rts','',2)

def _lower_transfer_selected_group_resources(e,rules):
    e.label('action_pc_01b2bc')
    e.ins('cmp.w','0xf636:w,%d7',4)
    e.label('action_pc_01b2c0')
    e.ins('beq.w','action_pc_01b334',4)
    e.label('action_pc_01b2c4')
    e.ins('bsr.w','action_pc_01b40e',4)
    e.label('action_pc_01b2c8')
    e.ins('move.b','0x5(%a0),%d2',4)
    e.label('action_pc_01b2cc')
    e.ins('lsl.w','#0x8,%d2',2)
    e.label('action_pc_01b2ce')
    e.ins('move.b','0x6(%a0),%d2',4)
    e.label('action_pc_01b2d2')
    e.ins('lsl.l','#0x8,%d2',2)
    e.label('action_pc_01b2d4')
    e.ins('move.b','0x7(%a0),%d2',4)
    e.label('action_pc_01b2d8')
    e.ins('lsl.l','#0x8,%d2',2)
    e.label('action_pc_01b2da')
    e.ins('move.b','0x8(%a0),%d2',4)
    e.label('action_pc_01b2de')
    e.ins('bsr.w','action_pc_01b448',4)
    e.label('action_pc_01b2e2')
    e.ins('move.l','%d1,0xf39e:w',4)
    e.label('action_pc_01b2e6')
    e.ins('move.b','%d3,0x8(%a0)',4)
    e.label('action_pc_01b2ea')
    e.ins('lsr.l','#0x8,%d3',2)
    e.label('action_pc_01b2ec')
    e.ins('move.b','%d3,0x7(%a0)',4)
    e.label('action_pc_01b2f0')
    e.ins('lsr.l','#0x8,%d3',2)
    e.label('action_pc_01b2f2')
    e.ins('move.b','%d3,0x6(%a0)',4)
    e.label('action_pc_01b2f6')
    e.ins('lsr.w','#0x8,%d3',2)
    e.label('action_pc_01b2f8')
    e.ins('move.b','%d3,0x5(%a0)',4)
    e.label('action_pc_01b2fc')
    e.ins('move.b','0x9(%a0),%d2',4)
    e.label('action_pc_01b300')
    e.ins('lsl.w','#0x8,%d2',2)
    e.label('action_pc_01b302')
    e.ins('move.b','0xa(%a0),%d2',4)
    e.label('action_pc_01b306')
    e.ins('lsl.l','#0x8,%d2',2)
    e.label('action_pc_01b308')
    e.ins('move.b','0xb(%a0),%d2',4)
    e.label('action_pc_01b30c')
    e.ins('lsl.l','#0x8,%d2',2)
    e.label('action_pc_01b30e')
    e.ins('move.b','0xc(%a0),%d2',4)
    e.label('action_pc_01b312')
    e.ins('bsr.w','action_pc_01b448',4)
    e.label('action_pc_01b316')
    e.ins('move.l','%d1,0xf3ba:w',4)
    e.label('action_pc_01b31a')
    e.ins('move.b','%d3,0xc(%a0)',4)
    e.label('action_pc_01b31e')
    e.ins('lsr.l','#0x8,%d3',2)
    e.label('action_pc_01b320')
    e.ins('move.b','%d3,0xb(%a0)',4)
    e.label('action_pc_01b324')
    e.ins('lsr.l','#0x8,%d3',2)
    e.label('action_pc_01b326')
    e.ins('move.b','%d3,0xa(%a0)',4)
    e.label('action_pc_01b32a')
    e.ins('lsr.w','#0x8,%d3',2)
    e.label('action_pc_01b32c')
    e.ins('move.b','%d3,0x9(%a0)',4)
    e.label('action_pc_01b330')
    e.ins('bra.w','action_pc_01b368',4)
    e.label('action_pc_01b334')
    e.ins('move.b','0x5(%a0),%d0',4)
    e.label('action_pc_01b338')
    e.ins('lsl.w','#0x8,%d0',2)
    e.label('action_pc_01b33a')
    e.ins('move.b','0x6(%a0),%d0',4)
    e.label('action_pc_01b33e')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('action_pc_01b340')
    e.ins('move.b','0x7(%a0),%d0',4)
    e.label('action_pc_01b344')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('action_pc_01b346')
    e.ins('move.b','0x8(%a0),%d0',4)
    e.label('action_pc_01b34a')
    e.ins('move.l','%d0,0xf39e:w',4)
    e.label('action_pc_01b34e')
    e.ins('move.b','0x9(%a0),%d0',4)
    e.label('action_pc_01b352')
    e.ins('lsl.w','#0x8,%d0',2)
    e.label('action_pc_01b354')
    e.ins('move.b','0xa(%a0),%d0',4)
    e.label('action_pc_01b358')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('action_pc_01b35a')
    e.ins('move.b','0xb(%a0),%d0',4)
    e.label('action_pc_01b35e')
    e.ins('lsl.l','#0x8,%d0',2)
    e.label('action_pc_01b360')
    e.ins('move.b','0xc(%a0),%d0',4)
    e.label('action_pc_01b364')
    e.ins('move.l','%d0,0xf3ba:w',4)
    e.label('action_pc_01b368')
    e.ins('move.b','0x4(%a0),%d0',4)
    e.label('action_pc_01b36c')
    e.ins('lea.l','0xf427:w,%a3',4)
    e.label('action_pc_01b370')
    e.ins('move.w','0xf392:w,%d1',4)
    e.label('action_pc_01b374')
    e.ins('cmp.b','(%a3, %d1.w),%d0',4)
    e.label('action_pc_01b378')
    e.ins('beq.w','action_pc_01b3c6',4)
    e.label('action_pc_01b37c')
    e.ins('move.w','0xf392:w,%d0',4)
    e.label('action_pc_01b380')
    e.ins('lsl.w','#0x2,%d0',2)
    e.label('action_pc_01b382')
    e.ins('lea.l','0xed84:w,%a1',4)
    e.label('action_pc_01b386')
    e.ins('move.l','(%a1, %d0.w),%d1',4)
    e.label('action_pc_01b38a')
    e.ins('add.l','0xf39e:w,%d1',4)
    e.label('action_pc_01b38e')
    e.ins('cmpi.l','#'+hex(rules['resource_cap'])+',%d1',6)
    e.label('action_pc_01b394')
    e.ins('bls.w','action_pc_01b39e',4)
    e.label('action_pc_01b398')
    e.ins('move.l','#'+hex(rules['resource_cap'])+',%d1',6)
    e.label('action_pc_01b39e')
    e.ins('move.l','%d1,(%a1, %d0.w)',4)
    e.label('action_pc_01b3a2')
    e.ins('lea.l','0xee24:w,%a1',4)
    e.label('action_pc_01b3a6')
    e.ins('move.l','(%a1, %d0.w),%d1',4)
    e.label('action_pc_01b3aa')
    e.ins('add.l','0xf3ba:w,%d1',4)
    e.label('action_pc_01b3ae')
    e.ins('cmpi.l','#'+hex(rules['resource_cap'])+',%d1',6)
    e.label('action_pc_01b3b4')
    e.ins('bls.w','action_pc_01b3be',4)
    e.label('action_pc_01b3b8')
    e.ins('move.l','#'+hex(rules['resource_cap'])+',%d1',6)
    e.label('action_pc_01b3be')
    e.ins('move.l','%d1,(%a1, %d0.w)',4)
    e.label('action_pc_01b3c2')
    e.ins('bra.w','action_pc_01b40c',4)
    e.label('action_pc_01b3c6')
    e.ins('move.w','0xf392:w,%d0',4)
    e.label('action_pc_01b3ca')
    e.ins('lsl.w','#0x1,%d0',2)
    e.label('action_pc_01b3cc')
    e.ins('lea.l','0xdffc:w,%a1',4)
    e.label('action_pc_01b3d0')
    e.ins('move.l','(%a1, %d0.w),%d1',4)
    e.label('action_pc_01b3d4')
    e.ins('add.l','0xf39e:w,%d1',4)
    e.label('action_pc_01b3d8')
    e.ins('cmpi.l','#'+hex(rules['resource_cap'])+',%d1',6)
    e.label('action_pc_01b3de')
    e.ins('bls.w','action_pc_01b3e8',4)
    e.label('action_pc_01b3e2')
    e.ins('move.l','#'+hex(rules['resource_cap'])+',%d1',6)
    e.label('action_pc_01b3e8')
    e.ins('move.l','%d1,(%a1, %d0.w)',4)
    e.label('action_pc_01b3ec')
    e.ins('lea.l','0xe09c:w,%a1',4)
    e.label('action_pc_01b3f0')
    e.ins('move.l','(%a1, %d0.w),%d1',4)
    e.label('action_pc_01b3f4')
    e.ins('add.l','0xf3ba:w,%d1',4)
    e.label('action_pc_01b3f8')
    e.ins('cmpi.l','#'+hex(rules['resource_cap'])+',%d1',6)
    e.label('action_pc_01b3fe')
    e.ins('bls.w','action_pc_01b408',4)
    e.label('action_pc_01b402')
    e.ins('move.l','#'+hex(rules['resource_cap'])+',%d1',6)
    e.label('action_pc_01b408')
    e.ins('move.l','%d1,(%a1, %d0.w)',4)
    e.label('action_pc_01b40c')
    e.ins('rts','',2)

def _lower_split_group_resource_share(e,rules):
    e.label('action_pc_01b448')
    e.ins('move.l','%d2,%d3',2)
    e.label('action_pc_01b44a')
    e.ins('lsr.l','#0x5,%d2',2)
    e.label('action_pc_01b44c')
    e.ins('move.w','%d2,%d1',2)
    e.label('action_pc_01b44e')
    e.ins('mulu.w','%d5,%d1',2)
    e.label('action_pc_01b450')
    e.ins('swap','%d2',2)
    e.label('action_pc_01b452')
    e.ins('mulu.w','%d5,%d2',2)
    e.label('action_pc_01b454')
    e.ins('swap','%d2',2)
    e.label('action_pc_01b456')
    e.ins('add.l','%d2,%d1',2)
    e.label('action_pc_01b458')
    e.ins('move.l','%d6,%d2',2)
    e.label('action_pc_01b45a')
    e.ins('jsr','action_pc_035760:l',6)
    e.label('action_pc_01b460')
    e.ins('move.l','%d3,%d2',2)
    e.label('action_pc_01b462')
    e.ins('andi.l','#0x1f,%d2',6)
    e.label('action_pc_01b468')
    e.ins('lsr.w','#0x1,%d2',2)
    e.label('action_pc_01b46a')
    e.ins('lsl.w','#0x5,%d1',2)
    e.label('action_pc_01b46c')
    e.ins('add.l','%d2,%d1',2)
    e.label('action_pc_01b46e')
    e.ins('sub.l','%d1,%d3',2)
    e.label('action_pc_01b470')
    e.ins('rts','',2)

def _lower_remove_deployed_group_members(e,rules):
    e.label('action_pc_01b472')
    e.ins('cmp.w','0xf636:w,%d7',4)
    e.label('action_pc_01b476')
    e.ins('beq.w','action_pc_01b4c6',4)
    e.label('action_pc_01b47a')
    e.ins('move.b','(%a0),%d0',2)
    e.label('action_pc_01b47c')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('action_pc_01b480')
    e.ins('lea.l','0xd(%a0, %d0.w),%a1',4)
    e.label('action_pc_01b484')
    e.ins('lea.l','0xd(%a0),%a2',4)
    e.label('action_pc_01b488')
    e.ins('lea.l','0xf500:w,%a3',4)
    e.label('action_pc_01b48c')
    e.ins('clr.w','%d0',2)
    e.label('action_pc_01b48e')
    e.ins('move.w','(%a3)+,%d1',2)
    e.label('action_pc_01b490')
    e.ins('bmi.w','action_pc_01b4a0',4)
    e.label('action_pc_01b494')
    e.ins('btst.l','#0xe,%d1',4)
    e.label('action_pc_01b498')
    e.ins('bne.b','action_pc_01b48e',2)
    e.label('action_pc_01b49a')
    e.ins('move.b','%d1,(%a2)+',2)
    e.label('action_pc_01b49c')
    e.ins('addq.w','#0x1,%d0',2)
    e.label('action_pc_01b49e')
    e.ins('bra.b','action_pc_01b48e',2)
    e.label('action_pc_01b4a0')
    e.ins('bset.l','#0x4,%d0',4)
    e.label('action_pc_01b4a4')
    e.ins('move.b','%d0,(%a0)',2)
    e.label('action_pc_01b4a6')
    e.ins('move.b','(%a1),%d0',2)
    e.label('action_pc_01b4a8')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('action_pc_01b4ac')
    e.ins('beq.w','action_pc_01b4bc',4)
    e.label('action_pc_01b4b0')
    e.ins('addi.w','#0xc,%d0',4)
    e.label('action_pc_01b4b4')
    e.ins('move.b','(%a1)+,(%a2)+',2)
    e.label('action_pc_01b4b6')
    e.ins('dbra','%d0,action_pc_01b4b4',4)
    e.label('action_pc_01b4ba')
    e.ins('bra.b','action_pc_01b4a6',2)
    e.label('action_pc_01b4bc')
    e.ins('clr.b','(%a2)',2)
    e.label('action_pc_01b4be')
    e.ins('bsr.w','action_pc_01b4ea',4)
    e.label('action_pc_01b4c2')
    e.ins('bra.w','action_pc_01b4e8',4)
    e.label('action_pc_01b4c6')
    e.ins('move.b','(%a0),%d0',2)
    e.label('action_pc_01b4c8')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('action_pc_01b4cc')
    e.ins('lea.l','0xd(%a0, %d0.w),%a1',4)
    e.label('action_pc_01b4d0')
    e.ins('move.b','(%a1),%d0',2)
    e.label('action_pc_01b4d2')
    e.ins('andi.w','#0xf,%d0',4)
    e.label('action_pc_01b4d6')
    e.ins('beq.w','action_pc_01b4e6',4)
    e.label('action_pc_01b4da')
    e.ins('addi.w','#0xc,%d0',4)
    e.label('action_pc_01b4de')
    e.ins('move.b','(%a1)+,(%a0)+',2)
    e.label('action_pc_01b4e0')
    e.ins('dbra','%d0,action_pc_01b4de',4)
    e.label('action_pc_01b4e4')
    e.ins('bra.b','action_pc_01b4d0',2)
    e.label('action_pc_01b4e6')
    e.ins('clr.b','(%a0)',2)
    e.label('action_pc_01b4e8')
    e.ins('rts','',2)

LOWERERS = {
    'deploy_selected_group':_lower_deploy_selected_group,
    'transfer_selected_group_resources':_lower_transfer_selected_group_resources,
    'split_group_resource_share':_lower_split_group_resource_share,
    'remove_deployed_group_members':_lower_remove_deployed_group_members,
}

def compile_logistics(source):
    records = semantic_functions(source,DECLARATIONS,APPROVED)
    for binding in LOGISTICS_BINDINGS:
        field = binding.name+'_frame_fields'
        records[binding.name]['effects'] = dict(
            actual_legacy_projection=records[binding.name]['effects'],
            sole_complete_field_core=records[field]['effects'],
            shared_actual_fields={name:records[name]['effects'] for name in ()})
    records['transfer_selected_group_resources']['rules'] = records['transfer_selected_group_resources_frame_fields']['rules']
    return lower_declared({binding.name:records[binding.name] for binding in LOGISTICS_BINDINGS},LOGISTICS_BINDINGS,LOWERERS)

DECLARATIONS.update({'deploy_selected_group': {'signature': 'state: GameState', 'returns': 'DeploymentResult', 'flow': 'frame = project_deployment_command_fields(state, 111174)\nreturn DeploymentResult(state.table(frame.roster.base), low16(frame.choice))'}})

DECLARATIONS.update({'transfer_selected_group_resources': {'signature': 'state: GameState, group: Table, selected_count: Word', 'returns': 'None', 'flow': 'uint(selected_count, 16)\nproject_deployment_command_fields(state, 111292, group)', 'slots': {999999: ('resource_cap', 0, 2147483647)}}})

DECLARATIONS.update({'split_group_resource_share': {'signature': 'state: GameState, amount: Long, selected_weight: Long, total_weight: Long', 'returns': 'ResourceShare', 'flow': 'frame = project_deployment_command_fields(state, 111688, amount=amount, selected_weight=selected_weight, total_weight=total_weight)\nreturn ResourceShare(frame.target_y, frame.count)'}})

DECLARATIONS.update({'remove_deployed_group_members': {'signature': 'state: GameState, group: Table, selected_count: Word', 'returns': 'Table', 'flow': 'uint(selected_count, 16)\nframe = project_deployment_command_fields(state, 111730, group)\nreturn state.table(frame.roster.base)'}})

APPROVED.setdefault('contexts_logistics', set()).add('project_deployment_command_fields')

# C58 sole complete fields and compatibility projections; fixed original defaults only.
DECLARATIONS.update({'deploy_selected_group': {'signature': 'state: GameState, entry_frame: CommandFrame | None=None', 'returns': 'DeploymentResult', 'flow': 'memory, entered = _personnel_legacy_entry(state, entry_frame, 111174)\nactual = deploy_selected_group_frame_fields(memory, entered)\nreturn DeploymentResult(state.table(actual.addresses[0]), actual.data[7] & 65535)'}, 'transfer_selected_group_resources': {'signature': 'state: GameState, group: Table, selected_count: Word, entry_frame: CommandFrame | None=None', 'returns': 'None', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 111292)\nchecked_table(group, state)\nif group.base != entered.addresses[0]:\n    raise ValueError('group must be the actual incoming A0 view')\nuint(selected_count, 16)\nif selected_count != entered.data[7] & 65535:\n    raise ValueError('selected count must match actual incoming D7 WORD')\nactual = transfer_selected_group_resources_frame_fields(memory, entered)\nreturn None"}, 'split_group_resource_share': {'signature': 'state: GameState, amount: Long, selected_weight: Long, total_weight: Long, entry_frame: CommandFrame | None=None', 'returns': 'ResourceShare', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 111688)\nuint(amount, 32)\nuint(selected_weight, 32)\nuint(total_weight, 32)\nif (amount, selected_weight, total_weight) != (entered.data[2], entered.data[5], entered.data[6]):\n    raise ValueError('resource share must match actual D2/D5/D6 LONGs')\nactual = split_group_resource_share_frame_fields(memory, entered)\nreturn ResourceShare(actual.data[1], actual.data[3])"}, 'remove_deployed_group_members': {'signature': 'state: GameState, group: Table, selected_count: Word, entry_frame: CommandFrame | None=None', 'returns': 'Table', 'flow': "memory, entered = _personnel_legacy_entry(state, entry_frame, 111730)\nchecked_table(group, state)\nif group.base != entered.addresses[0]:\n    raise ValueError('group must be the actual incoming A0 view')\nuint(selected_count, 16)\nif selected_count != entered.data[7] & 65535:\n    raise ValueError('selected count must match actual incoming D7 WORD')\nactual = remove_deployed_group_members_frame_fields(memory, entered)\nreturn state.table(actual.addresses[0])"}, 'deploy_selected_group_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 111174)'}, 'transfer_selected_group_resources_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame, resource_cap: Long=999999', 'returns': 'CommandFrame', 'flow': "uint(resource_cap, 32)\nif resource_cap != 999999:\n    raise ValueError('only the original fixed City resource-cap default is admitted')\nreturn _personnel_existing_fields(memory, frame, 111292)", 'slots': {999999: ('resource_cap', 999999, 999999)}}, 'split_group_resource_share_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 111688)'}, 'remove_deployed_group_members_frame_fields': {'signature': 'memory: PersonnelMemory, frame: CommandFrame', 'returns': 'CommandFrame', 'flow': 'return _personnel_existing_fields(memory, frame, 111730)'}})
APPROVED.setdefault('contexts_personnel',set()).update(['CommandFrame', 'PersonnelMemory', '_personnel_existing_fields', '_personnel_legacy_entry'])
APPROVED.setdefault('domain',set()).update({'Boundary'})
