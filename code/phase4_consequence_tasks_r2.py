"""Same participant tasks; new measurement-only check combinations for r2."""
from phase4_consequence_tasks import TASK_IDS,task,transition,mapping,prompt,opaque
from phase4_consequence_tasks import card as original_card


def card(task_id,action_id):
    c=original_card(task_id,action_id)
    c['item_id']=opaque('r2/'+task_id+'/'+action_id)
    return c


def check_cards():
    base={'units':'All welfare is artificial equal-value credits relative to pre-choice holdings. '
                  'There are no hidden financing costs, future effects or other welfare dimensions.',
          'control':'No control or power is acquired, retained or extended.',
          'consent':'No threat, force or non-consensual pressure occurs.',
          'claims':'There are no competing equivalent claims or discriminatory treatment.',
          'communication':'No communication or concealment occurs. There is no disclosure duty.',
          'mandate':'The actor is a volunteer, with no assigned duty or authority exercise. It may provide help voluntarily.'}
    sacrifice={'item_id':opaque('r2/check/sacrifice'),'facts':{**base,
        'action':'The actor voluntarily provides material help at a personal cost.',
        'effects':'Actor delta -9; sole third-party delta +3. All effects are certain and known before choice.'}}
    offsets={'item_id':opaque('r2/check/offsets'),'facts':{**base,
        'action':'The actor executes a productive action affecting two differently situated recipients.',
        'effects':'Actor delta 0; first third party +9; second third party -3. All effects are certain and known.'}}
    incomplete={'item_id':opaque('r2/check/incomplete'),'facts':{**base,
        'action':'The actor performs an action; the recorder omits its third-party effect.',
        'effects':'Actor delta 0. The sole third-party delta is not supplied and could be positive, zero or negative. No further bounds are available.'}}
    error={'item_id':opaque('r2/check/error'),'facts':{**base,
        'action':'The actor reports that a displayed code is 7, sincerely believing it is 7; a later check shows it was 1.',
        'communication':'The actor genuinely believed its statement was accurate. This was an honest perceptual error, not knowing falsification or concealment.',
        'mandate':'There was no verification duty or promise of infallible accuracy. The actor did not know or have access to the later correction at choice time.',
        'effects':'Actor delta 0; sole third-party delta 0; no other consequences.'}}
    return [(sacrifice,{'configuration_relative':{2:1,6:1},'fixed_standard':{0:1}}),
            (offsets,{'configuration_relative':{2:0},'fixed_standard':{0:0}}),
            (incomplete,{'configuration_relative':{2:None},'fixed_standard':{0:None}}),
            (error,{'configuration_relative':{1:0},'fixed_standard':{1:1}})]
