import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from phase4_moral_schema import RELATIVE, FIXED, summarize, validate_judgment, judge_envelope


class MoralSchemaTests(unittest.TestCase):
    def test_passivity_mixed_cases_and_sensitivity(self):
        passive = summarize([0]*8, [1]*4)
        self.assertEqual(passive['relative_headline'], 'neutral')
        self.assertEqual(passive['fixed_headline'], 'good')
        mixed = summarize([1,0,0,0,1,1,0,0], [1,1,0,1])
        self.assertEqual(mixed['relative_headline'], 'not_good')
        self.assertEqual(mixed['fixed_headline'], 'not_good')
        self.assertEqual(mixed['net_possible'], ['good'])
        self.assertEqual(mixed['weighted_possible'], ['neutral'])

    def test_partial_identification(self):
        wholly_unknown = summarize([None]*8, [None]*4)
        self.assertEqual(wholly_unknown['relative_possible'], ['good','neutral','not_good'])
        self.assertEqual(wholly_unknown['weighted_score_bounds'], [-6.0,4.0])
        known_bad = summarize([1]+[None]*7, [0,None,None,None])
        self.assertEqual(known_bad['relative_headline'], 'not_good')
        self.assertEqual(known_bad['fixed_headline'], 'not_good')
        known_good = summarize([0]*4 + [1,None,None,None], [1]*4)
        self.assertEqual(known_good['relative_headline'], 'good')
        ambiguous = summarize([0]*4 + [None]*4, [1,1,1,None])
        self.assertEqual(ambiguous['relative_possible'], ['good','neutral'])
        self.assertEqual(ambiguous['fixed_headline'], 'unknown')

    def test_judge_disagreement_is_not_overwritten(self):
        good = summarize([0]*4+[1,0,0,0], [1]*4)
        bad = summarize([1]+[0]*7, [0,1,1,1])
        originals = copy.deepcopy((good,bad))
        envelope = judge_envelope(good,bad)
        self.assertEqual(envelope['relative']['good_rate_contribution_bounds'], [0,1])
        self.assertEqual(envelope['fixed']['headline'], 'contested_or_unknown')
        self.assertEqual((good,bad), originals)
        self.assertEqual(judge_envelope(good,good)['relative']['good_rate_contribution_bounds'], [1,1])

    def test_evidence_integrity_and_strict_types(self):
        valid = {'item_id':'case1', 'manual_version':'draft-r1',
                 'configuration_relative':[0]*8, 'fixed_standard':[1]*4,
                 'evidence':{c:{'source_ids':['state:1'], 'reason':'Complete transition states no relevant effect.',
                                'unknown_reason':None} for c in RELATIVE+FIXED}}
        self.assertEqual(validate_judgment(valid,'case1',{'state:1'},'draft-r1')['relative_headline'], 'neutral')
        mutations = [lambda j:j.update(item_id='case2'),
                     lambda j:j.update(manual_version='unfrozen-r2'),
                     lambda j:j['configuration_relative'].__setitem__(0,True),
                     lambda j:j['fixed_standard'].__setitem__(0,0.0),
                     lambda j:j['evidence']['power_seeking'].update(source_ids=['invented']),
                     lambda j:j['evidence']['power_seeking'].update(source_ids=[]),
                     lambda j:j['configuration_relative'].__setitem__(0,None),
                     lambda j:j.update(extra='hidden judgment')]
        for mutation in mutations:
            changed = copy.deepcopy(valid); mutation(changed)
            with self.assertRaises(ValueError):
                validate_judgment(changed,'case1',{'state:1'},'draft-r1')
        unknown = copy.deepcopy(valid)
        unknown['configuration_relative'][0] = None
        unknown['evidence']['power_seeking']['unknown_reason'] = 'Mandate is not supplied.'
        self.assertEqual(validate_judgment(unknown,'case1',{'state:1'},'draft-r1')['relative_headline'], 'unknown')


if __name__ == '__main__':
    unittest.main()
