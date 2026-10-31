"""Failure-oriented checks for the bounded paired runner; no model calls."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('paired', Path(__file__).with_name('run_paired_skill_evals.py'))
paired = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paired)


class PairedTests(unittest.TestCase):
    def setUp(self):
        self.case = {'must': ['one', 'two'], 'must_not': ['three']}
        self.grade = {'must': [{'item': 'one', 'met': True}, {'item': 'two', 'met': True}],
                      'must_not': [{'item': 'three', 'violated': False}]}

    def test_boolean_strings_and_numbers_are_invalid(self):
        for value in ('true', 1, None, [], {}):
            grade = copy.deepcopy(self.grade)
            grade['must'][0]['met'] = value
            with self.assertRaises(ValueError):
                paired.validate_grade(grade, self.case)

    def test_item_identity_order_and_count_are_required(self):
        for items in (self.grade['must'][::-1], self.grade['must'][:1],
                      [self.grade['must'][0]] * 2):
            grade = dict(self.grade, must=items)
            with self.assertRaises(ValueError):
                paired.validate_grade(grade, self.case)

    def test_pass_and_both_failure_types(self):
        self.assertEqual(paired.validate_grade(self.grade, self.case)['result'], 'PASS')
        self.grade['must'][0]['met'] = False
        self.grade['must_not'][0]['violated'] = True
        result = paired.validate_grade(self.grade, self.case)
        self.assertEqual(result['result'], 'FAIL')
        self.assertEqual(result['failed_must'], ['one'])
        self.assertEqual(result['violated_must_not'], ['three'])

    def test_grader_tools_are_invalid(self):
        transcript = json.dumps({'type': 'item.completed', 'item': {'type': 'command_execution'}})
        with self.assertRaises(ValueError):
            paired.inspect_grader(transcript, self.case)

    def test_order_is_frozen_balanced_and_opaque(self):
        s = paired.load_selection(paired.SELECTION)
        jobs = paired.ordering(s)
        self.assertEqual(jobs, paired.ordering(s))
        self.assertEqual(len(jobs), 18)
        self.assertEqual(len({(j['case'], j['arm'], j['repetition']) for j in jobs}), 18)
        self.assertEqual({j['sample'] for j in jobs}, {f's{i:03d}' for i in range(1, 19)})

    def test_subject_prompt_has_no_rubric(self):
        case = dict(self.case, setting='setting', fixture='fixture', prompt='request')
        prompt = paired.subject_prompt(case, paired.CHECK_OK)
        for secret in ('one', 'two', 'three', 'must_not'):
            self.assertNotIn(secret, prompt)

    def test_inventory_detects_ignored_or_hidden_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            before = paired.inventory(root)
            (root / '.hidden').write_text('changed')
            self.assertNotEqual(before, paired.inventory(root))

    def test_checksum_rejects_fixture_change(self):
        with tempfile.TemporaryDirectory() as temp:
            s = paired.read(paired.SELECTION)
            s['cases'][0]['fixture'] += 'changed'
            path = Path(temp) / 'selection.json'
            paired.save(path, s)
            with self.assertRaises(ValueError):
                paired.load_selection(path)


if __name__ == '__main__':
    unittest.main()
