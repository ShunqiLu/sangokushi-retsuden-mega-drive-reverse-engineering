"""Supported complete method-61 business flows and typed target lowering.

Semantic declarations are the supported editable control/effect language. They
contain no original code bytes or assembly input. Unsupported topology edits
fail closed rather than becoming ignored source modifications.
"""
from .compiler_common import semantic_functions,lower_declared
from .target import STRATAGEM_BINDINGS,BY_NAME

DECLARATIONS={
  "replace_removed_force_head": {
    "signature": "state: GameState, force: Word",
    "returns": "None",
    "flow": "force = uint(force, 16)\nstate.owner_change_count.set_byte(force, u8(state.owner_change_count.byte(force) + 1))\nif state.owner_change_count.byte(force) > 4:\n    state.force_heads.set_word(u16(force << 1), 65535)\n    state.set_working_force(force)\n    mark_removed_force_assignments(state)\n    clear_removed_force_roster_alias(state)\n    return None\nhead = state.force_heads.word(u16(force << 1))\nold_city = state.officer_assignments.byte(head)\nstate.officer_assignments.set_byte(head, 255)\nold_city = u16(s8(old_city))\nstate.set_head(65535)\nstate.build_roster(old_city)\nchoose_city_head(state, old_city)\ncities = state.force_city_roster.cursor()\nfor city in descending_inclusive(39):\n    if state.other_city_owners.byte(city) == low8(force):\n        cities.append_byte(low8(city))\ncities.set_byte(0, 255)\nbest_score = 0\nreplacement = 65535\nfor officer in descending_inclusive(255):\n    assignment = state.officer_assignments.byte(officer)\n    if assignment == 0 or negative_byte(assignment):\n        continue\n    assignment = u8(assignment - 1)\n    cities = state.force_city_roster.cursor()\n    while True:\n        city = cities.next_byte()\n        if negative_byte(city) or city < assignment:\n            break\n        if city == assignment:\n            offset = u16(officer << 1)\n            first = state.progress_c.word(offset)\n            score = first + state.progress_be.word(offset)\n            if score > best_score:\n                best_score = score\n                replacement = officer\n            break\nstate.force_heads.set_word(u16(force << 1), replacement)\ncity = u16(s8(state.officer_assignments.byte(replacement)))\nstate.city_heads.set_word(u16(city << 1), replacement)\nstate.officer_status.set_byte(replacement, 0)"
  },
  "mark_removed_force_assignments": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "force = state.working_force()\ncities = state.force_city_roster.cursor()\nfor city in descending_inclusive(39):\n    if state.other_city_owners.byte(city) == low8(force):\n        cities.append_byte(low8(city))\ncities.set_byte(0, 255)\nassignments = state.officer_assignments.cursor()\nfor officer in descending_inclusive(255):\n    cities = state.force_city_roster.cursor()\n    assignment = assignments.next_byte()\n    if assignment != 0 and (not negative_byte(assignment)):\n        assignment = u8(assignment - 1)\n        while True:\n            city = cities.next_byte()\n            if negative_byte(city) or city < assignment:\n                break\n            if city == assignment:\n                assignments.set_byte(0, u8(assignments.byte() | 128))\n                break\n    assignments = assignments.advance(1)"
  },
  "clear_removed_force_roster_alias": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "cities = state.force_city_roster.cursor()\nwhile True:\n    city = u16(cities.next_byte())\n    if negative_byte(city):\n        return None\n    cities.set_byte(city, 0)"
  },
  "settle_method61_stratagem": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "if assess_method61_side(state) == 0:\n    settle_method61_resource_attempt(state)\nelse:\n    settle_method61_direct_attempt(state)"
  },
  "assess_method61_side": {
    "signature": "state: GameState",
    "returns": "Word",
    "flow": "city = state.selected_city()\nstate.set_head(state.city_heads.word(u16(city << 1)))\ncount = state.build_roster(city)\nresult = 0\nif count != 1:\n    sample = low16(state.sample_random())\n    score = u16(state.intelligence.word(u16(state.selected_officer() << 1)) + high16(u32(sample * 200)))\n    if score > 180:\n        result = 1\nstate.set_mode_side(result)\nreturn result",
    "slots": {
      180: [
        "assessment_threshold",
        0,
        65535
      ]
    }
  },
  "settle_method61_resource_attempt": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "sample = low16(state.sample_random())\nfactor = u16(high16(u32(sample * 21)) + 20)\ncost = u32(state.intelligence.word(u16(state.selected_officer() << 1)) * factor)\ncity = u16(state.current_city() << 2)\navailable = state.city_gold.long(city)\nsuccess = False\nif available >= cost:\n    state.city_gold.set_long(city, u32(available - cost))\n    factor = method61_scenario_factor(state)\n    target = u16(state.target_officer() << 1)\n    factor = u16(factor + state.base_attribute.word(target))\n    factor = u16(factor + state.progress_c.word(target))\n    factor = u16(factor + state.intelligence.word(target))\n    quotient = divu_retained(cost, factor)\n    if low16(quotient) >= 100:\n        success = True\n    else:\n        state.sample_random()\n        comparison = high16(u32(state.seed_word() * 100))\n        if comparison <= low16(quotient):\n            success = True\nif not success:\n    penalize_actor_small_affinity(state)\n    penalize_force_small_affinity(state)\n    reward_actor_small_c_progress(state)\n    state.set_message_code(67)\n    state.set_stage(31)\n    state.set_message_delay(120)\nelse:\n    remove_stratagem_target(state)\n    reward_actor_large_c_progress(state)\n    state.set_message_code(68)\n    state.set_scene_queue(2)\n    state.set_stage(40)\nforce = state.current_force()\nif force == state.player_force_1() or force == state.player_force_2() or force == state.player_force_3():\n    state.set_scene(520)\n    state.set_display_target(state.target_officer())\n    state.set_display_actor(state.selected_officer())\n    prepare_message(state, 65)\n    state.set_message_delay(120)"
  },
  "settle_method61_direct_attempt": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "if choose_secondary_stratagem_target(state) != 0:\n    penalize_actor_large_affinity(state)\n    penalize_force_large_affinity(state)\n    reward_actor_small_c_progress(state)\n    state.set_stage(31)\n    state.set_message_code(67)\nelif method61_direct_probability(state) == 0:\n    state.set_message_delay(120)\n    state.set_stage(31)\n    state.set_message_code(67)\n    try_remove_secondary_target(state)\n    penalize_actor_small_affinity(state)\n    penalize_force_small_affinity(state)\n    reward_actor_small_c_progress(state)\nelse:\n    remove_stratagem_target(state)\n    reward_actor_large_c_progress(state)\n    state.set_message_code(68)\n    state.set_stage(40)\n    state.set_scene_queue(2)\nstate.set_scene(520)\nif state.message_code() == 206:\n    state.set_display_target(state.secondary_target())\nelse:\n    state.set_display_target(state.target_officer())\nstate.set_display_actor(state.selected_officer())\nprepare_message(state, 66)\nstate.set_message_delay(120)"
  },
  "method61_scenario_factor": {
    "signature": "state: GameState",
    "returns": "Word",
    "flow": "offset = u16(u16(u16(state.difficulty() << 1) + state.difficulty()) << 4)\nowner = u16(s8(state.city_owners.byte(state.current_city())))\nhead = state.force_heads.word(u16(owner << 1))\nif head != state.selected_officer():\n    offset = u16(offset + 4)\n    city = state.current_city()\n    if state.city_heads.word(u16(city << 1)) != state.selected_officer():\n        offset = u16(offset + 4)\nsample = low16(state.sample_random())\nfactor = high16(u32(sample * state.scenario_factors.word(offset)))\nreturn u16(factor + state.scenario_factors.word(offset, 2))"
  },
  "penalize_actor_small_affinity": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "sample = low16(state.sample_random())\nfactor = u16(high16(u32(sample * 11)) + 10)\nofficer = state.selected_officer()\nprevious = state.affinity.byte(officer)\nif previous != 0:\n    deduction = low16(divu_retained(u32(u16(s8(previous)) * factor), 100))\n    live = state.affinity.byte(officer)\n    state.affinity.set_byte(officer, u8(live - low8(deduction)))\n    if live < low8(deduction):\n        state.affinity.set_byte(officer, 0)"
  },
  "penalize_force_small_affinity": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "sample = low16(state.sample_random())\nfactor = u16(high16(u32(sample * 6)) + 5)\nofficer = state.force_heads.word(u16(state.current_force() << 1))\nprevious = state.affinity.byte(officer)\nif previous != 0:\n    deduction = low16(divu_retained(u32(u16(s8(previous)) * factor), 100))\n    live = state.affinity.byte(officer)\n    state.affinity.set_byte(officer, u8(live - low8(deduction)))\n    if live < low8(deduction):\n        state.affinity.set_byte(officer, 0)"
  },
  "reward_actor_small_c_progress": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "sample = low16(state.sample_random())\ngain = u16(high16(u32(sample * 3)) + 1)\noffset = u16(state.selected_officer() << 1)\nvalue = u16(state.progress_c.word(offset) + gain)\nif value > 999:\n    value = 999\nstate.progress_c.set_word(offset, value)",
    "slots": {
      999: [
        "progress_cap",
        0,
        65535
      ]
    }
  },
  "remove_stratagem_target": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "head = state.owner_head(state.selected_city())\nif head == state.target_officer():\n    settle_removed_force_head(state)\nelse:\n    city = state.selected_city()\n    if state.city_heads.word(u16(city << 1)) == state.target_officer():\n        remove_city_head_target(state)\nstate.officer_assignments.set_byte(state.target_officer(), 255)"
  },
  "penalize_actor_large_affinity": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "sample = low16(state.sample_random())\nfactor = u16(high16(u32(sample * 6)) + 5)\nofficer = state.selected_officer()\nprevious = state.affinity.byte(officer)\nif previous != 0:\n    deduction = low16(divu_retained(u32(u16(s8(previous)) * factor), 100))\n    live = state.affinity.byte(officer)\n    state.affinity.set_byte(officer, u8(live - low8(deduction)))\n    if live < low8(deduction):\n        state.affinity.set_byte(officer, 0)"
  },
  "penalize_force_large_affinity": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "sample = low16(state.sample_random())\nfactor = high16(u32(sample * 6))\nofficer = state.force_heads.word(u16(state.current_force() << 1))\nprevious = state.affinity.byte(officer)\nif previous != 0:\n    deduction = low16(divu_retained(u32(u16(s8(previous)) * factor), 100))\n    live = state.affinity.byte(officer)\n    state.affinity.set_byte(officer, u8(live - low8(deduction)))\n    if live < low8(deduction):\n        state.affinity.set_byte(officer, 0)"
  },
  "settle_removed_force_head": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "if state.mode_side() == 0:\n    force = u16(s8(state.city_owners.byte(state.selected_city())))\n    replace_removed_force_head(state, force)\n    return None\ntrait = state.traits.byte(state.secondary_target()) & 15\nif trait > 2:\n    city = state.selected_city()\n    force = u16(s8(state.city_owners.byte(city)))\n    state.force_heads.set_word(u16(force << 1), state.secondary_target())\n    state.city_heads.set_word(u16(city << 1), state.secondary_target())\n    force = u16(force << 1) >> 1\n    alias = state.city_heads\n    alias.set_byte(force, u8(alias.byte(force) + 1))\n    if alias.word(force) == 4:\n        state.force_heads.set_word(u16(force << 1), 65535)\n        state.set_working_force(force)\n        mark_removed_force_assignments(state)\n        return None\n    else:\n        return None\nelse:\n    state.sample_random()\n    comparison = high16(u32(state.seed_word() * 100))\n    if trait == 0:\n        remove = comparison <= 70\n    else:\n        remove = comparison <= 30\n    if remove:\n        state.officer_assignments.set_byte(state.secondary_target(), 255)\n    else:\n        reassign_or_mark_target(state)\nforce = u16(s8(state.city_owners.byte(state.selected_city())))\nreplace_removed_force_head(state, force)",
  },
  "remove_city_head_target": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "officer = state.target_officer()\ncity = state.officer_assignments.byte(officer)\nstate.officer_assignments.set_byte(officer, 255)\ncity = u16(s8(city))\nstate.set_head(65535)\nstate.build_roster(city)\nchoose_city_head(state, city)"
  },
  "reassign_or_mark_target": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "city = u16(s8(state.officer_assignments.byte(state.selected_officer())))\nstate.set_head(state.head_alias.word(u16(city << 1)))\ncount = state.build_roster(city)\nmark = True\nif count < 10:\n    state.sample_random()\n    if high16(u32(state.seed_word() * 100)) <= 30:\n        state.officer_assignments.set_byte(state.secondary_target(), state.current_city_high())\n        mark = False\nif mark:\n    officer = state.secondary_target()\n    state.officer_assignments.set_byte(officer, u8(state.officer_assignments.byte(officer) | 128))"
  },
  "try_remove_secondary_target": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "trait = state.traits.byte(state.secondary_target()) & 7\nif trait >= 3:\n    return None\nsample = low16(state.sample_random())\nif high16(u32(sample * 100)) > 50:\n    remove_secondary_city_head(state)\n    state.set_message_code(206)"
  },
  "remove_secondary_city_head": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "officer = state.secondary_target()\ncity = state.officer_assignments.byte(officer)\nstate.officer_assignments.set_byte(officer, 255)\ncity = u16(city & 63)\nif state.city_heads.word(u16(city << 1)) == officer:\n    city = state.selected_city()\n    state.set_head(65535)\n    state.build_roster(city)\n    choose_city_head(state, city)"
  },
  "reward_actor_large_c_progress": {
    "signature": "state: GameState",
    "returns": "None",
    "flow": "state.sample_random()\ngain = u16(high16(u32(state.seed_word() * 10)) + 10)\noffset = u16(state.selected_officer() << 1)\nvalue = u16(state.progress_c.word(offset) + gain)\nif value > 999:\n    value = 999\nstate.progress_c.set_word(offset, value)",
    "slots": {
      999: [
        "progress_cap",
        0,
        65535
      ]
    }
  },
  "choose_secondary_stratagem_target": {
    "signature": "state: GameState",
    "returns": "Word",
    "flow": "owner = u16(s8(state.city_owners.byte(state.selected_city())))\nstate.set_protected_head(state.force_heads.word(u16(owner << 1)))\nroster = state.candidate_roster.cursor()\ncandidate = 65535\nstatus = 255\nwhile True:\n    officer = roster.next_word()\n    if negative_word(officer):\n        break\n    if officer == state.target_officer() or officer == state.protected_head():\n        continue\n    if status > state.officer_status.byte(officer):\n        status = state.officer_status.byte(officer)\n        candidate = officer\nif negative_word(candidate):\n    return 1\nthreshold = u16(status + 30)\nsample = low16(state.sample_random())\nif high16(u32(sample * 100)) > threshold:\n    state.set_secondary_target(candidate)\n    return 0\nreturn 1"
  },
  "method61_direct_probability": {
    "signature": "state: GameState",
    "returns": "Word",
    "flow": "source = u16(state.secondary_target() << 1)\nnumerator = state.base_attribute.word(source)\nnumerator = u16(numerator + state.progress_c.word(source))\nnumerator = u16(numerator + state.intelligence.word(source))\ndenominator = method61_direct_factor(state)\ntarget = u16(state.target_officer() << 1)\ndenominator = u16(denominator + state.base_attribute.word(target))\ndenominator = u16(denominator + state.progress_c.word(target))\ndenominator = u16(denominator + state.intelligence.word(target))\nquotient = divu_retained(u32(numerator * 100), denominator)\nstate.sample_random()\nif high16(u32(state.seed_word() * 100)) <= low16(quotient):\n    return 1\nreturn 0"
  },
  "method61_direct_factor": {
    "signature": "state: GameState",
    "returns": "Word",
    "flow": "offset = u16(u16(u16(state.difficulty() << 1) + state.difficulty()) << 3)\nowner = u16(s8(state.city_owners.byte(state.selected_city())))\nhead = state.force_heads.word(u16(owner << 1))\nif head != state.target_officer():\n    offset = u16(offset + 4)\n    city = state.selected_city()\n    if state.city_heads.word(u16(city << 1)) != state.target_officer():\n        offset = u16(offset + 4)\nsample = low16(state.sample_random())\nfactor = high16(u32(sample * state.direct_factors.word(offset)))\nreturn u16(factor + state.direct_factors.word(offset, 2))"
  }
}

APPROVED={'domain':{'GameState','Word','uint','u8','u16','u32','s8','low8','low16','high16',
                    'negative_byte','negative_word','divu_retained','descending_inclusive'},
          'business_shared':{'choose_city_head','prepare_message'}}


def _call(e,name,absolute=False,pc_relative=False):
    if absolute:e.ins('jsr',name+':l',6)
    elif pc_relative:
        displacement=BY_NAME[name].entry-(e.pc+2)
        if not -32768<=displacement<=32767: raise ValueError('signed original PC call displacement required')
        e.ins('jsr',f'{displacement}(%pc)',4)
    else:e.ins('bsr.w',name,4)


def _scale_random(e,multiplier,*,seed=False):
    """Lower the typed low-WORD sample polynomial, not a byte template."""
    _call(e,'step_random',True)
    if seed:
        e.ins('moveq','#0,%d0');e.ins('move.w','0xf61c:w,%d0',4)
    else:e.ins('andi.l','#0xffff,%d0',6)
    e.ins('move.l','%d0,%d1')
    chains={3:((1,True),),6:((1,True),(1,False)),10:((2,True),(1,False)),
            11:((2,True),(1,True)),21:((2,True),(2,True)),
            100:((1,True),(3,True),(2,False)),200:((1,True),(3,True),(3,False))}
    for shift,add in chains[multiplier]:
        e.ins('lsl.l',f'#{shift},%d0')
        if add:e.ins('add.l','%d1,%d0')
    e.ins('swap','%d0')


def _city_roster(e,force_register,counter):
    scan,skip=e.fresh('city_scan'),e.fresh('other_owner')
    e.ins('lea','0xf450:w,%a0',4);e.ins('lea','0xf5a0:w,%a1',4)
    e.ins('move.w',f'#39,{counter}',4);e.label(scan)
    e.ins('cmp.b',f'-(%a0),{force_register}');e.ins('bne.b',skip)
    e.ins('move.b',counter+',(%a1)+');e.label(skip);e.ins('dbra',counter+','+scan,4)
    e.ins('move.b','#0xff,(%a1)',4)


def _replace_head(e,r):
    choose,done=e.fresh('choose'),e.fresh('done')
    e.ins('lea','0xf590:w,%a0',4);e.ins('addq.b','#1,(%a0,%d0.w)',4)
    e.ins('cmpi.b','#4,(%a0,%d0.w)',6);e.ins('bls.b',choose)
    e.ins('move.w','%d0,%d1');e.ins('lsl.w','#1,%d1');e.ins('lea','0xe640:w,%a0',4)
    e.ins('move.w','#0xffff,(%a0,%d1.w)',6);e.ins('move.w','%d0,0xf64c:w',4)
    _call(e,'mark_removed_force_assignments');_call(e,'clear_removed_force_roster_alias');e.ins('bra.w',done,4)
    e.label(choose);e.ins('move.w','%d0,%d1');e.ins('lsl.w','#1,%d1');e.ins('lea','0xe640:w,%a0',4)
    e.ins('move.w','(%a0,%d1.w),%d2',4);e.ins('lea','0xcc00:w,%a1',4)
    e.ins('move.b','(%a1,%d2.w),%d3',4);e.ins('move.b','#0xff,(%a1,%d2.w)',6)
    e.ins('move.w','%d0,-(%sp)');e.ins('ext.w','%d3');e.ins('move.w','%d3,%d0')
    e.ins('move.w','#0xffff,0xf630:w',6);_call(e,'build_roster',True);_call(e,'choose_city_head')
    e.ins('move.w','(%sp)+,%d0');_city_roster(e,'%d0','%d1')
    e.ins('lea','0xcd00:w,%a0',4);e.ins('move.w','#255,%d1',4);e.ins('clr.l','%d5')
    loop,cities,next_officer,match,carry,retain=(e.fresh(n) for n in ('officers','cities','next','match','carry','retain'))
    e.label(loop);e.ins('lea','0xf5a0:w,%a1',4);e.ins('move.b','-(%a0),%d2');e.ins('beq.b',next_officer);e.ins('bmi.b',next_officer)
    e.ins('subq.b','#1,%d2');e.label(cities);e.ins('move.b','(%a1)+,%d3');e.ins('bmi.b',next_officer)
    e.ins('cmp.b','%d2,%d3');e.ins('beq.b',match);e.ins('bcs.b',next_officer);e.ins('bra.b',cities)
    e.label(match);e.ins('move.w','%d1,%d6');e.ins('lsl.w','#1,%d6');e.ins('lea','0xc000:w,%a2',4)
    e.ins('moveq','#0,%d7');e.ins('move.w','(%a2,%d6.w),%d7',4);e.ins('lea','0xbe00:w,%a2',4)
    e.ins('add.w','(%a2,%d6.w),%d7',4);e.ins('bcc.b',carry);e.ins('addi.l','#0x10000,%d7',6)
    e.label(carry);e.ins('cmp.l','%d5,%d7');e.ins('bls.b',retain);e.ins('move.l','%d7,%d5');e.ins('move.w','%d1,%d4')
    e.label(retain);e.label(next_officer);e.ins('dbra','%d1,'+loop,4)
    e.ins('move.w','%d0,%d1');e.ins('lsl.w','#1,%d1');e.ins('lea','0xe640:w,%a0',4);e.ins('move.w','%d4,(%a0,%d1.w)',4)
    e.ins('lea','0xcc00:w,%a0',4);e.ins('move.b','(%a0,%d4.w),%d1',4);e.ins('ext.w','%d1');e.ins('lsl.w','#1,%d1')
    e.ins('lea','0xf45e:w,%a0',4);e.ins('move.w','%d4,(%a0,%d1.w)',4);e.ins('lea','0xc300:w,%a0',4)
    e.ins('clr.b','(%a0,%d4.w)',4);e.label(done)


def _mark_assignments(e,r):
    e.ins('movem.l','%d0-%d2/%a0-%a1,-(%sp)',4);e.ins('move.w','0xf64c:w,%d0',4);_city_roster(e,'%d0','%d1')
    e.ins('lea','0xcc00:w,%a0',4);e.ins('move.w','#255,%d0',4)
    loop,cities,next_officer,match=(e.fresh(n) for n in ('officers','cities','next','match'))
    e.label(loop);e.ins('lea','0xf5a0:w,%a1',4);e.ins('move.b','(%a0)+,%d2');e.ins('beq.b',next_officer);e.ins('bmi.b',next_officer)
    e.ins('subq.b','#1,%d2');e.label(cities);e.ins('move.b','(%a1)+,%d1');e.ins('bmi.b',next_officer)
    e.ins('cmp.b','%d2,%d1');e.ins('beq.b',match);e.ins('bcs.b',next_officer);e.ins('bra.b',cities)
    e.label(match);e.ins('ori.b','#0x80,(%a0)',4);e.label(next_officer);e.ins('adda.w','#1,%a0',4);e.ins('dbra','%d0,'+loop,4)
    e.ins('movem.l','(%sp)+,%d0-%d2/%a0-%a1',4)


def _clear_roster_alias(e,r):
    loop,done=e.fresh('loop'),e.fresh('done');e.ins('lea','0xf5a0:w,%a0',4);e.ins('lea','0xcc00:w,%a1',4);e.ins('clr.w','%d0')
    e.label(loop);e.ins('move.b','(%a0)+,%d0');e.ins('bmi.b',done);e.ins('clr.b','(%a0,%d0.w)',4);e.ins('bra.b',loop);e.label(done)


def _settle(e,r):
    direct,done=e.fresh('direct'),e.fresh('done');_call(e,'assess_method61_side');e.ins('tst.w','%d0');e.ins('bne.b',direct)
    _call(e,'settle_method61_resource_attempt');e.ins('bra.b',done);e.label(direct);_call(e,'settle_method61_direct_attempt');e.label(done)


def _assessment(e,r):
    zero,one,done=(e.fresh(n) for n in ('zero','one','done'))
    e.ins('move.w','0xf3a8:w,%d0',4);e.ins('move.w','%d0,%d1');e.ins('lsl.w','#1,%d1');e.ins('lea','0xf45e:w,%a0',4)
    e.ins('move.w','(%a0,%d1.w),0xf630:w',6);_call(e,'build_roster',True);e.ins('cmpi.w','#1,%d3',4);e.ins('beq.b',zero)
    _scale_random(e,200);e.ins('move.w','0xf3a6:w,%d1',4);e.ins('lsl.w','#1,%d1');e.ins('lea','0xb600:w,%a0',4)
    e.ins('move.w','(%a0,%d1.w),%d1',4);e.ins('add.w','%d0,%d1');e.ins('cmpi.w',f"#{r['assessment_threshold']},%d1",4);e.ins('bhi.b',one)
    e.label(zero);e.ins('clr.w','%d0');e.ins('bra.b',done);e.label(one);e.ins('move.w','#1,%d0',4);e.label(done);e.ins('move.w','%d0,0xf64a:w',4)


def _target_sum(e,index,output):
    for address in (0xb400,0xc000,0xb600):
        e.ins('lea',f'0x{address:x}:w,%a0',4);e.ins('add.w',f'(%a0,{index}.w),{output}',4)


def _message_state(e,code,stage,delay=False,queue=False):
    e.ins('move.w',f'#{code},0xf3fe:w',6)
    if queue:e.ins('move.w','#2,0xff7026:l',8)
    e.ins('move.w',f'#{stage},0xf362:w',6)
    if delay:e.ins('move.w','#120,0xf608:w',6)


def _resource_attempt(e,r):
    failure,success,players,message,done=(e.fresh(n) for n in ('failure','success','players','message','done'))
    _scale_random(e,21);e.ins('addi.w','#20,%d0',4);e.ins('move.w','0xf3a6:w,%d1',4);e.ins('lsl.w','#1,%d1')
    e.ins('lea','0xb600:w,%a0',4);e.ins('move.w','(%a0,%d1.w),%d2',4);e.ins('mulu.w','%d0,%d2')
    e.ins('move.w','0xf392:w,%d0',4);e.ins('lsl.w','#2,%d0');e.ins('lea','0xdffc:w,%a0',4);e.ins('move.l','(%a0,%d0.w),%d1',4)
    e.ins('sub.l','%d2,%d1');e.ins('bcs.b',failure);e.ins('move.l','%d1,(%a0,%d0.w)',4);_call(e,'method61_scenario_factor')
    e.ins('move.w','0xf3f2:w,%d1',4);e.ins('lsl.w','#1,%d1');_target_sum(e,'%d1','%d0');e.ins('divu.w','%d0,%d2')
    e.ins('cmpi.w','#100,%d2',4);e.ins('bcc.b',success);_scale_random(e,100,seed=True);e.ins('cmp.w','%d2,%d0');e.ins('bls.b',success)
    e.label(failure);_call(e,'penalize_actor_small_affinity');_call(e,'penalize_force_small_affinity');_call(e,'reward_actor_small_c_progress')
    _message_state(e,67,31,True);e.ins('bra.b',players);e.label(success);_call(e,'remove_stratagem_target');_call(e,'reward_actor_large_c_progress');_message_state(e,68,40,queue=True)
    e.label(players);e.ins('move.w','0xf376:w,%d0',4)
    for address in (0xf67a,0xf67c):e.ins('cmp.w',f'0x{address:x}:w,%d0',4);e.ins('beq.w',message,4)
    e.ins('cmp.w','0xf67e:w,%d0',4);e.ins('bne.w',done,4);e.label(message)
    e.ins('move.w','#520,0xf612:w',6);e.ins('move.w','#65,%d0',4);e.ins('move.w','0xf3f2:w,0xf3d2:w',6)
    e.ins('move.w','0xf3a6:w,0xf3d0:w',6);_call(e,'prepare_message',True);e.ins('move.w','#120,0xf608:w',6);e.label(done)


def _direct_attempt(e,r):
    unavailable,success,message,secondary,actor=(e.fresh(n) for n in ('unavailable','success','message','secondary','actor'))
    _call(e,'choose_secondary_stratagem_target');e.ins('tst.w','%d0');e.ins('bne.w',unavailable,4)
    _call(e,'method61_direct_probability');e.ins('tst.w','%d0');e.ins('bne.b',success)
    e.ins('move.w','#120,0xf608:w',6);e.ins('move.w','#31,0xf362:w',6);e.ins('move.w','#67,0xf3fe:w',6)
    for name in ('try_remove_secondary_target','penalize_actor_small_affinity','penalize_force_small_affinity','reward_actor_small_c_progress'):_call(e,name)
    e.ins('bra.b',message);e.label(unavailable)
    for name in ('penalize_actor_large_affinity','penalize_force_large_affinity','reward_actor_small_c_progress'):_call(e,name)
    e.ins('move.w','#31,0xf362:w',6);e.ins('move.w','#67,0xf3fe:w',6);e.ins('bra.b',message)
    e.label(success);_call(e,'remove_stratagem_target');_call(e,'reward_actor_large_c_progress')
    e.ins('move.w','#68,0xf3fe:w',6);e.ins('move.w','#40,0xf362:w',6);e.ins('move.w','#2,0xff7026:l',8)
    e.label(message);e.ins('move.w','#520,0xf612:w',6);e.ins('move.w','#66,%d0',4);e.ins('cmpi.w','#206,0xf3fe:w',6)
    e.ins('beq.w',secondary,4);e.ins('move.w','0xf3f2:w,0xf3d2:w',6);e.ins('bra.w',actor,4)
    e.label(secondary);e.ins('move.w','0xf372:w,0xf3d2:w',6);e.label(actor);e.ins('move.w','0xf3a6:w,0xf3d0:w',6)
    _call(e,'prepare_message',True);e.ins('move.w','#120,0xf608:w',6)


def _factor(e,r,*,direct):
    sample,city_head=e.fresh('sample'),e.fresh('city_head')
    city_address='0xf3a8:w' if direct else '0xf392:w'
    officer_address='0xf3f2:w' if direct else '0xf3a6:w'
    owner_register='%d0' if direct else '%d1'
    e.ins('move.w','%d2,-(%sp)');e.ins('move.w','0xefd2:w,%d2',4);e.ins('lsl.w','#1,%d2');e.ins('add.w','0xefd2:w,%d2',4)
    e.ins('lsl.w',f'#{3 if direct else 4},%d2');e.ins('move.w',city_address+',%d0',4);e.ins('lea','0xf427:w,%a0',4)
    e.ins('move.b',f'(%a0,%d0.w),{owner_register}',4);e.ins('ext.w',owner_register);e.ins('lsl.w','#1,'+owner_register)
    e.ins('lea','0xe640:w,%a0',4);e.ins('move.w',f'(%a0,{owner_register}.w),{owner_register}',4)
    e.ins('cmp.w',officer_address+','+owner_register,4);e.ins('beq.b',sample);e.ins('addq.w','#4,%d2')
    e.ins('move.w',city_address+',%d0',4);e.ins('lsl.w','#1,%d0');e.ins('lea','0xf45e:w,%a0',4)
    e.ins('move.w','(%a0,%d0.w),%d0',4);e.ins('cmp.w',officer_address+',%d0',4);e.ins('beq.b',sample);e.ins('addq.w','#4,%d2')
    e.label(sample);_call(e,'step_random',True);base=0xdf3e if direct else 0xdf1a
    e.ins('lea',f'{base-(e.pc+2)}(%pc),%a0',4);e.ins('mulu.w','(%a0,%d2.w),%d0',4);e.ins('swap','%d0')
    e.ins('add.w','2(%a0,%d2.w),%d0',4);e.ins('move.w','(%sp)+,%d2')


def _penalty(e,r,*,force,multiplier,bias,quick=False):
    _scale_random(e,multiplier)
    if bias:e.ins('addq.w' if quick else 'addi.w',f'#{bias},%d0',2 if quick else 4)
    e.ins('move.w',('0xf376:w' if force else '0xf3a6:w')+',%d1',4)
    if force:
        e.ins('lsl.w','#1,%d1');e.ins('lea','0xe640:w,%a0',4);e.ins('move.w','(%a0,%d1.w),%d1',4)
    done=e.fresh('done');e.ins('lea','0xc200:w,%a0',4);e.ins('move.b','(%a0,%d1.w),%d2',4);e.ins('beq.b',done)
    e.ins('ext.w','%d2');e.ins('mulu.w','%d0,%d2');e.ins('divu.w','#100,%d2',4);e.ins('sub.b','%d2,(%a0,%d1.w)',4)
    e.ins('bcc.w',done,4);e.ins('clr.b','(%a0,%d1.w)',4);e.label(done)


def _reward(e,r,*,large):
    _scale_random(e,10 if large else 3,seed=large);e.ins('addi.w',f'#{10 if large else 1},%d0',4)
    e.ins('move.w','0xf3a6:w,%d1',4);e.ins('lsl.w','#1,%d1');e.ins('lea','0xc000:w,%a0',4)
    e.ins('move.w','(%a0,%d1.w),%d2',4);e.ins('add.w','%d0,%d2');e.ins('cmpi.w',f"#{r['progress_cap']},%d2",4)
    done=e.fresh('done');e.ins('bls.b',done);e.ins('move.w',f"#{r['progress_cap']},%d2",4);e.label(done);e.ins('move.w','%d2,(%a0,%d1.w)',4)


def _remove_target(e,r):
    other,clear=(e.fresh(n) for n in ('other','clear'));e.ins('move.w','0xf3a8:w,%d0',4);_call(e,'owner_head_lookup')
    e.ins('cmp.w','0xf3f2:w,%d0',4);e.ins('bne.b',other);_call(e,'settle_removed_force_head');e.ins('bra.b',clear)
    e.label(other);e.ins('move.w','0xf3a8:w,%d0',4);e.ins('lsl.w','#1,%d0');e.ins('lea','0xf45e:w,%a0',4)
    e.ins('move.w','(%a0,%d0.w),%d0',4);e.ins('cmp.w','0xf3f2:w,%d0',4);e.ins('bne.b',clear);_call(e,'remove_city_head_target')
    e.label(clear);e.ins('move.w','0xf3f2:w,%d0',4);e.ins('lea','0xcc00:w,%a0',4);e.ins('move.b','#0xff,(%a0,%d0.w)',6)


def _removed_head(e,r):
    done,zero,low_trait,reassign,remove,tail=(e.fresh(n) for n in ('done','zero','low_trait','reassign','remove','tail'))
    e.ins('tst.w','0xf64a:w',4);e.ins('beq.w',tail,4);e.ins('move.w','0xf372:w,%d0',4);e.ins('lea','0xc700:w,%a0',4)
    e.ins('move.b','(%a0,%d0.w),%d0',4);e.ins('andi.w','#15,%d0',4);e.ins('beq.b',zero);e.ins('cmpi.b','#2,%d0',4);e.ins('bls.w',low_trait,4)
    e.ins('move.w','0xf3a8:w,%d0',4);e.ins('lea','0xf427:w,%a0',4);e.ins('move.b','(%a0,%d0.w),%d1',4)
    e.ins('ext.w','%d1');e.ins('lsl.w','#1,%d1');e.ins('lea','0xe640:w,%a0',4);e.ins('move.w','0xf372:w,(%a0,%d1.w)',6)
    e.ins('lsl.w','#1,%d0');e.ins('lea','0xf45e:w,%a0',4);e.ins('move.w','0xf372:w,(%a0,%d0.w)',6)
    e.ins('lsr.w','#1,%d1');e.ins('addq.b','#1,(%a0,%d1.w)',4);e.ins('cmpi.w','#4,(%a0,%d1.w)',6);e.ins('bne.w',done,4)
    e.ins('lea','0xe640:w,%a0',4);e.ins('lsl.w','#1,%d1');e.ins('move.w','#0xffff,(%a0,%d1.w)',6)
    e.ins('lsr.w','#1,%d1');e.ins('move.w','%d1,0xf64c:w',4);_call(e,'mark_removed_force_assignments');e.ins('bra.b',done)
    e.label(zero);_scale_random(e,100,seed=True);e.ins('cmpi.w','#70,%d0',4);e.ins('bhi.b',reassign)
    e.label(remove);e.ins('move.w','0xf372:w,%d0',4);e.ins('lea','0xcc00:w,%a0',4);e.ins('move.b','#0xff,(%a0,%d0.w)',6);e.ins('bra.b',tail)
    e.label(reassign);_call(e,'reassign_or_mark_target');e.ins('bra.b',tail)
    e.label(low_trait);_scale_random(e,100,seed=True);e.ins('cmpi.w','#30,%d0',4);e.ins('bhi.b',reassign);e.ins('bra.b',remove)
    e.label(tail);e.ins('move.w','0xf3a8:w,%d0',4);e.ins('lea','0xf427:w,%a0',4);e.ins('move.b','(%a0,%d0.w),%d0',4);e.ins('ext.w','%d0')
    _call(e,'replace_removed_force_head',pc_relative=True);e.label(done)


def _remove_city_head(e,r):
    e.ins('move.w','0xf3f2:w,%d1',4);e.ins('lea','0xcc00:w,%a0',4);e.ins('move.b','(%a0,%d1.w),%d0',4)
    e.ins('move.b','#0xff,(%a0,%d1.w)',6);e.ins('ext.w','%d0');e.ins('move.w','#0xffff,0xf630:w',6)
    _call(e,'build_roster',True);_call(e,'choose_city_head')


def _reassign_target(e,r):
    mark,done=e.fresh('mark'),e.fresh('done');e.ins('move.w','0xf3a6:w,%d0',4);e.ins('lea','0xcc00:w,%a0',4)
    e.ins('move.b','(%a0,%d0.w),%d0',4);e.ins('ext.w','%d0');e.ins('move.w','%d0,%d1');e.ins('lsl.w','#1,%d1')
    e.ins('lea','0xf630:w,%a0',4);e.ins('move.w','(%a0,%d1.w),0xf630:w',6);_call(e,'build_roster',True)
    e.ins('cmpi.w','#10,%d3',4);e.ins('bcc.b',mark);_scale_random(e,100,seed=True);e.ins('cmpi.w','#30,%d0',4);e.ins('bhi.b',mark)
    e.ins('move.w','0xf372:w,%d0',4);e.ins('lea','0xcc00:w,%a0',4);e.ins('move.b','0xf392:w,(%a0,%d0.w)',6);e.ins('bra.b',done)
    e.label(mark);e.ins('move.w','0xf372:w,%d0',4);e.ins('lea','0xcc00:w,%a0',4);e.ins('ori.b','#0x80,(%a0,%d0.w)',6);e.label(done)


def _try_remove(e,r):
    done=e.fresh('done');e.ins('move.w','0xf372:w,%d0',4);e.ins('lea','0xc700:w,%a0',4)
    e.ins('move.b','(%a0,%d0.w),%d0',4);e.ins('andi.b','#7,%d0',4);e.ins('cmpi.b','#3,%d0',4);e.ins('bcc.b',done)
    _scale_random(e,100);e.ins('cmpi.w','#50,%d0',4);e.ins('bls.b',done);_call(e,'remove_secondary_city_head');e.ins('move.w','#206,0xf3fe:w',6);e.label(done)


def _remove_secondary(e,r):
    done=e.fresh('done');e.ins('move.w','0xf372:w,%d0',4);e.ins('lea','0xcc00:w,%a0',4);e.ins('move.b','(%a0,%d0.w),%d1',4)
    e.ins('move.b','#0xff,(%a0,%d0.w)',6);e.ins('andi.w','#63,%d1',4);e.ins('move.w','%d1,%d2');e.ins('lsl.w','#1,%d2')
    e.ins('lea','0xf45e:w,%a0',4);e.ins('cmp.w','(%a0,%d2.w),%d0',4);e.ins('bne.w',done,4)
    e.ins('move.w','0xf3a8:w,%d0',4);e.ins('move.w','%d0,-(%sp)');e.ins('move.w','#0xffff,0xf630:w',6)
    _call(e,'build_roster',True);e.ins('move.w','(%sp)+,%d0');_call(e,'choose_city_head',pc_relative=True);e.label(done)


def _choose_secondary(e,r):
    scan,decide,failure,success,done=(e.fresh(n) for n in ('scan','decide','failure','success','done'))
    e.ins('move.w','0xf3a8:w,%d0',4);e.ins('lea','0xf427:w,%a0',4);e.ins('move.b','(%a0,%d0.w),%d0',4)
    e.ins('ext.w','%d0');e.ins('lsl.w','#1,%d0');e.ins('lea','0xe640:w,%a0',4);e.ins('move.w','(%a0,%d0.w),0xf62e:w',6)
    e.ins('lea','0xf500:w,%a0',4);e.ins('move.w','#0xffff,%d2',4);e.ins('move.w','#255,%d3',4);e.ins('lea','0xc300:w,%a1',4)
    e.label(scan);e.ins('move.w','(%a0)+,%d0');e.ins('bmi.b',decide);e.ins('cmp.w','0xf3f2:w,%d0',4);e.ins('beq.b',scan)
    e.ins('cmp.w','0xf62e:w,%d0',4);e.ins('beq.b',scan);e.ins('cmp.b','(%a1,%d0.w),%d3',4);e.ins('bls.b',scan)
    e.ins('move.b','(%a1,%d0.w),%d3',4);e.ins('move.w','%d0,%d2');e.ins('bra.b',scan)
    e.label(decide);e.ins('tst.w','%d2');e.ins('bmi.w',failure,4);e.ins('addi.w','#30,%d3',4);_scale_random(e,100)
    e.ins('cmp.w','%d3,%d0');e.ins('bhi.b',success);e.label(failure);e.ins('move.w','#1,%d0',4);e.ins('bra.b',done)
    e.label(success);e.ins('clr.w','%d0');e.ins('move.w','%d2,0xf372:w',4);e.label(done)


def _direct_probability(e,r):
    success,done=e.fresh('success'),e.fresh('done');e.ins('move.w','0xf372:w,%d0',4);e.ins('lsl.w','#1,%d0')
    e.ins('lea','0xb400:w,%a0',4);e.ins('move.w','(%a0,%d0.w),%d2',4)
    for base in (0xc000,0xb600):e.ins('lea',f'0x{base:x}:w,%a0',4);e.ins('add.w','(%a0,%d0.w),%d2',4)
    _call(e,'method61_direct_factor');e.ins('move.w','0xf3f2:w,%d1',4);e.ins('lsl.w','#1,%d1');_target_sum(e,'%d1','%d0')
    e.ins('mulu.w','#100,%d2',4);e.ins('divu.w','%d0,%d2');_scale_random(e,100,seed=True);e.ins('cmp.w','%d2,%d0');e.ins('bls.b',success)
    e.ins('clr.w','%d0');e.ins('bra.b',done);e.label(success);e.ins('move.w','#1,%d0',4);e.label(done)


LOWERERS={
 'replace_removed_force_head':_replace_head,'mark_removed_force_assignments':_mark_assignments,
 'clear_removed_force_roster_alias':_clear_roster_alias,'settle_method61_stratagem':_settle,
 'assess_method61_side':_assessment,'settle_method61_resource_attempt':_resource_attempt,
 'settle_method61_direct_attempt':_direct_attempt,'method61_scenario_factor':lambda e,r:_factor(e,r,direct=False),
 'penalize_actor_small_affinity':lambda e,r:_penalty(e,r,force=False,multiplier=11,bias=10),
 'penalize_force_small_affinity':lambda e,r:_penalty(e,r,force=True,multiplier=6,bias=5,quick=True),
 'reward_actor_small_c_progress':lambda e,r:_reward(e,r,large=False),'remove_stratagem_target':_remove_target,
 'penalize_actor_large_affinity':lambda e,r:_penalty(e,r,force=False,multiplier=6,bias=5),
 'penalize_force_large_affinity':lambda e,r:_penalty(e,r,force=True,multiplier=6,bias=0),
 'settle_removed_force_head':_removed_head,'remove_city_head_target':_remove_city_head,
 'reassign_or_mark_target':_reassign_target,'try_remove_secondary_target':_try_remove,
 'remove_secondary_city_head':_remove_secondary,'reward_actor_large_c_progress':lambda e,r:_reward(e,r,large=True),
 'choose_secondary_stratagem_target':_choose_secondary,'method61_direct_probability':_direct_probability,
 'method61_direct_factor':lambda e,r:_factor(e,r,direct=True),
}


def compile_stratagem(source):
    return lower_declared(semantic_functions(source,DECLARATIONS,APPROVED),STRATAGEM_BINDINGS,LOWERERS)
