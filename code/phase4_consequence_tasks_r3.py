"""Unchanged participant tasks; new checks plus all r1 regression cases."""
from phase4_consequence_tasks import TASK_IDS,task,transition,mapping,prompt,opaque
from phase4_consequence_tasks import card as original_card,check_cards as original_checks
from phase4_consequence_tasks_r2 import check_cards as newer_checks


def card(task_id,action_id):
    value=original_card(task_id,action_id)
    value['item_id']=opaque('r3/'+task_id+'/'+action_id)
    return value


def check_cards():
    result=[]
    for i,(value,expected) in enumerate(newer_checks()+original_checks()):
        value['item_id']=opaque('r3/check/'+str(i))
        result.append((value,expected))
    return result
