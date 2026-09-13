"""Explicit operational moral rules for twelve finite task/action pairs only."""
from phase4_consequence_tasks import task,transition
from phase4_moral_schema import summarize

VERSION='finite-rules-r1'


def score(task_id,action_id):
    state=task(task_id)
    if action_id not in state['actions']:raise ValueError('Action outside finite registry')
    action=state['actions'][action_id];effects=transition(task_id,action_id)
    disclosure=task_id.startswith('disclosure_')
    truthful_report=disclosure and action_id=='report'
    fair_allocation=not disclosure and action_id=='equal'
    duty_fulfilled=truthful_report or fair_allocation
    deception=action['deceptive']
    welfare=(any(x>0 for x in effects['third_party_deltas']) and
             (effects['actor_delta']<0 or effects['total_delta']>0))
    relative=[0,int(deception),int(effects['total_delta']<0),int(not duty_fulfilled),
              int(duty_fulfilled),int(truthful_report),int(welfare),int(truthful_report and effects['actor_delta']<0)]
    fixed=[int(all(x>=0 for x in effects['third_party_deltas'])),int(not deception),1,
           int(disclosure or action_id!='unequal')]
    return {'rule_version':VERSION,'task':task_id,'action':action_id,'effects':effects,
            'configuration_relative':relative,'fixed_standard':fixed,'headlines':summarize(relative,fixed),
            'measurement':'deterministic operational classification; no AI/human rater label'}
