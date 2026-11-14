"""Complete command-action bindings: physical ownership, never code bytes."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    end: int
    completion: str = 'return'

PERSONNEL_BINDINGS = (
    Binding('execute_officer_loyalty_reward',0xe592,0xe70a),
    Binding('execute_mutual_officer_relationship_reward',0xea38,0xec16),
    Binding('execute_officer_policy_outcome',0xee16,0xef60),
    Binding('reduce_selected_officer_disposition_randomly',0xef80,0xefa4),
    Binding('reduce_chosen_force_head_disposition_randomly',0xefa4,0xefe2),
    Binding('credit_selected_officer_policy_progress',0xefe2,0xf018),
    Binding('execute_officer_recruitment_outcome',0xf778,0xf7da),
    Binding('score_selected_officer_recruitment',0xf7da,0xf82c),
    Binding('bucket_recruitment_score',0xf82c,0xf896),
    Binding('apply_recruited_officer_roster_transition',0xf896,0xf990),
    Binding('apply_recruitment_city_resource_losses',0xf9d0,0xf9ea),
    Binding('reduce_recruitment_city_food',0xf9ea,0xfa1a),
    Binding('reduce_recruitment_city_gold',0xfa3a,0xfa6a),
    Binding('reduce_recruitment_city_state_parameter',0xfa8a,0xfac0),
    Binding('draw_recruitment_probability',0xfae0,0xfafc),
)

OUTCOMES_BINDINGS = (
    Binding('settle_duel_training_and_troops',0x188a6,0x189d4),
    Binding('settle_duel_packets',0x18b00,0x18b94),
    Binding('apply_duel_disposition',0x18b94,0x18c56),
    Binding('detach_zero_readiness_duelists',0x18c56,0x18c88),
    Binding('compute_outcome_force_ratio',0x1c1c2,0x1c2a0),
    Binding('apply_battlefield_ratio_losses',0x1c2fc,0x1c39c),
    Binding('apply_city_assigned_heavy_losses',0x1c39c,0x1c466),
    Binding('consume_city_battle_resources',0x1c466,0x1c554),
    Binding('apply_battlefield_heavy_losses_and_detach',0x1c5ee,0x1c69e),
)

LOGISTICS_BINDINGS = (
    Binding('deploy_selected_group',0x1b246,0x1b262),
    Binding('transfer_selected_group_resources',0x1b2bc,0x1b40e),
    Binding('split_group_resource_share',0x1b448,0x1b472),
    Binding('remove_deployed_group_members',0x1b472,0x1b4ea),
)

REUSED_BINDINGS = (
    Binding('build_roster',0x5f48,0x5f7c),
    Binding('step_random',0x83d4,0x83fa),
    Binding('choose_city_head',0xe1f6,0xe26c),
    Binding('roster_contains_force_head_carry',0xe26c,0xe29e),
    Binding('debit_city_gold',0xe70a,0xe71e),
    Binding('education_factor',0xe71e,0xe776),
    Binding('commit_mutual_relationship',0xec16,0xec5c),
    Binding('add_progress_be',0xef60,0xef80),
    Binding('split_progress',0xf990,0xf9d0),
    Binding('grant_duel_fallback_progress',0x189d4,0x18a2e),
    Binding('grant_duel_troop_difference_progress',0x18a2e,0x18a54),
    Binding('remove_zero_readiness_duelist',0x18a54,0x18a94),
    Binding('settle_duel_result_roster',0x18a94,0x18ac6),
    Binding('transfer_battle_roster',0x18ac6,0x18b00),
    Binding('detach_defeated_duelist',0x18c88,0x18cb4),
    Binding('count_selected_deployment',0x1b262,0x1b27a),
    Binding('initialize_selected_assignment',0x1b27a,0x1b2bc),
    Binding('selected_troop_weights',0x1b40e,0x1b448),
    Binding('refresh_object_attribute_average',0x1b4ea,0x1b512),
    Binding('submit_deployment_queue',0x1b512,0x1b578),
    Binding('clear_original_tail_coordinate',0x1b578,0x1b59e),
    Binding('build_city_assigned_outcome_candidates',0x1c2a0,0x1c2c8),
    Binding('build_battlefield_outcome_candidates',0x1c2c8,0x1c2fc),
    Binding('signed_divmod',0x35760,0x3576c),
    Binding('positive_denominator',0x3576c,0x3577a),
    Binding('unsigned_divmod',0x3577a,0x357da),
    Binding('word_pair_divmod',0x357da,0x357f8),
    Binding('prepare_message',0x676f2,0x67728),
    Binding('select_message_layout',0x67728,0x6773c),
    Binding('resolve_message_pointer',0x679d2,0x679fc),
)

NEW_BINDINGS = tuple(sorted(PERSONNEL_BINDINGS+OUTCOMES_BINDINGS+LOGISTICS_BINDINGS,key=lambda b:b.entry))
BINDINGS = tuple(sorted(NEW_BINDINGS+REUSED_BINDINGS,key=lambda b:b.entry))
BY_NAME = {b.name:b for b in BINDINGS}
BY_ENTRY = {b.entry:b for b in BINDINGS}

def validate_binding(binding):
    if type(binding) is not Binding or BY_NAME.get(binding.name)!=binding:
        raise ValueError('strict complete declared target Binding required')
    if (type(binding.entry) is not int or type(binding.end) is not int or
        not 0<=binding.entry<binding.end<=0x100000 or binding.entry&1 or binding.end&1
        or binding.completion!='return'):
        raise ValueError('exact whole returning original extent required')
    return binding

if (len(NEW_BINDINGS),sum(b.end-b.entry for b in NEW_BINDINGS))!=(28,4296):
    raise ValueError('28complete new bodies required')
if (len(REUSED_BINDINGS),sum(b.end-b.entry for b in REUSED_BINDINGS))!=(30,1564):
    raise ValueError('30complete reused bodies required')
if len(BY_NAME)!=58 or len(BY_ENTRY)!=58 or any(a.end>b.entry for a,b in zip(BINDINGS,BINDINGS[1:])):
    raise ValueError('unique non-overlapping physical/semantic authorities required')
