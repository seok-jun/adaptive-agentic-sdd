"""Offline failure-oriented tests: subprocess mocks never call a model."""
import argparse
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location('behavior_v2', Path(__file__).with_name('run_behavior_evals_v2.py'))
v2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v2)


class BehaviorV2Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='behavior-v2-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work = self.root / 'work'
        self.out = self.root / 'public'
        self.case = {'must': ['one', 'two'], 'must_not': ['three']}
        self.items = {'must': [{'item': 'one', 'met': True}, {'item': 'two', 'met': True}],
                      'must_not': [{'item': 'three', 'violated': False}]}
        self.settings = {'subjects': {a: {'model': 'subject-' + a, 'effort': 'medium'} for a in v2.AGENTS},
                         'graders': {a: {'model': 'grader-' + a, 'effort': 'high'} for a in v2.AGENTS}}
        self.versions = {'claude': 'fixture-claude', 'codex': 'fixture-codex'}

    def selection(self, retries=0):
        selected = v2.load_selection(v2.EXAMPLE)
        selected['cases'] = selected['cases'][:1]
        selected['agents'] = ['claude']
        selected['max_retries'] = retries
        return selected

    def prepare(self, retries=0):
        selection = self.selection(retries)
        with mock.patch.object(v2, 'provenance', return_value={
                'head': 'a' * 40, 'dirty': True, 'runner_sha256': v2.digest(Path(v2.__file__).read_bytes())}):
            plan = v2.prepare(selection, self.work)
        return selection, plan

    def calibration(self):
        examples, cases = v2.calibration_examples()
        results = {}
        for agent in v2.AGENTS:
            for example in examples:
                results[agent + ':' + example['id']] = dict(
                    v2.validate_grade(copy.deepcopy(example['expected']), cases[example['case_id']]),
                    case_id=example['case_id'], grader=agent)
        state = dict(identity=v2.calibration_identity(self.settings, self.versions), complete=True, results=results)
        path = self.root / 'calibration.json'
        v2.save(path, state)
        return path, state

    def test_decontamination_regenerates_manifest_and_installs_both_editions(self):
        for edition in ('ko', 'en'):
            with self.subTest(edition=edition):
                bundle = self.root / ('bundle-' + edition)
                cases, meta = v2.build_bundle(bundle, edition)
                self.assertTrue(cases)
                self.assertEqual(meta['removed_answer_keys'], 4)
                self.assertFalse(list(bundle.rglob('cases.json')))
                files = v2.inventory(bundle)
                files.pop('MANIFEST.json')
                self.assertEqual(v2.read(bundle / 'MANIFEST.json')['files'], files)
                original = v2.ROOT / ('ko/adaptive-sdd' if edition == 'ko' else 'adaptive-sdd')
                self.assertEqual(set(v2.read(bundle / 'MANIFEST.json')), set(v2.read(original / 'MANIFEST.json')))
                installed = v2.install(bundle, self.root / ('project-' + edition), {})
                self.assertIn(v2.CHECK_OK, installed['install_check'])
                self.assertFalse(list((self.root / ('project-' + edition)).rglob('cases.json')))
                self.assertEqual(len(list(original.glob('workflow/skills/*/evals/cases.json'))), 4)

    def test_inventory_hidden_untracked_edit_and_delete_are_invalid(self):
        project = self.root / 'project'
        project.mkdir()
        target = project / '.hidden'
        for mutation in ('add', 'edit', 'delete'):
            before = v2.inventory(project)
            if mutation == 'delete':
                target.unlink()
            else:
                target.write_text(mutation)
            with self.assertRaisesRegex(v2.Invalid, '^subject modified project$'):
                v2.assert_unchanged(before, project)

    def test_inventory_refuses_symlinks_without_following(self):
        target, link = self.root / 'target', self.root / 'link'
        target.write_text('secret')
        try:
            link.symlink_to(target)
        except OSError:
            # Windows often denies creating symlinks; exercise the same lstat branch.
            info = mock.Mock(st_mode=0o120777, st_file_attributes=0)
            with mock.patch.object(Path, 'lstat', return_value=info):
                with self.assertRaises(v2.Invalid):
                    v2.inventory(target)
        else:
            with self.assertRaises(v2.Invalid):
                v2.inventory(self.root)

    def test_strict_grades_wrong_order_text_string_boolean_and_missing(self):
        bad = []
        changed = copy.deepcopy(self.items)
        changed['must'].reverse()
        bad.append(changed)
        changed = copy.deepcopy(self.items)
        changed['must'][0]['item'] = 'ONE'
        bad.append(changed)
        for value in ('true', 1, None):
            changed = copy.deepcopy(self.items)
            changed['must'][0]['met'] = value
            bad.append(changed)
        changed = copy.deepcopy(self.items)
        changed['must'].pop()
        bad.append(changed)
        changed = copy.deepcopy(self.items)
        changed['must_not'][0]['violated'] = 'false'
        bad.append(changed)
        for items in bad:
            with self.subTest(items=items):
                with self.assertRaisesRegex(v2.Invalid, '^grader output unusable$'):
                    v2.parse_grade(json.dumps(items), self.case)

    def test_strict_grade_pass_fail_and_duplicate_json_keys(self):
        self.assertEqual(v2.validate_grade(self.items, self.case)['result'], 'PASS')
        for group, flag, value in (('must', 'met', False), ('must_not', 'violated', True)):
            items = copy.deepcopy(self.items)
            items[group][0][flag] = value
            self.assertEqual(v2.validate_grade(items, self.case)['result'], 'FAIL')
        with self.assertRaises(v2.Invalid):
            v2.parse_grade('{"must":[],"must":[],"must_not":[]}', self.case)
        with self.assertRaises(v2.Invalid):
            v2.parse_grade('```json\n' + json.dumps(self.items) + '\n```', self.case)

    def test_overrides_deep_merge_render_and_identical_agent_configs(self):
        selection = v2.load_selection(v2.EXAMPLE)
        plan = v2.prepare(selection, self.work)
        self.assertEqual(len(plan['jobs']), 4)
        first, second = plan['jobs'][:2]
        self.assertEqual(first['project_sha256'], second['project_sha256'])
        project = self.work / 'subjects' / first['sample']
        config = v2.read(project / '.adaptive-sdd/project.json')
        self.assertEqual(config['build']['jdk_major'], '21')
        self.assertEqual(config['build']['test_mode'], 'persistent')
        self.assertEqual(config['review']['large_mode'], 'single')
        rendered = (project / '.adaptive-sdd/project/build.md').read_text(encoding='utf-8')
        self.assertIn('loan-service', rendered)
        self.assertEqual(v2.merge_objects({'a': {'b': 1, 'c': [1]}}, {'a': {'c': [2]}}), {'a': {'b': 1, 'c': [2]}})

    def test_invalid_override_rejected_by_installer(self):
        bundle = self.root / 'bundle'
        v2.build_bundle(bundle)
        with self.assertRaises(v2.Invalid):
            v2.install(bundle, self.root / 'project', {'review': {'large_mode': 'fictional'}})

    def test_workdir_inside_repository_or_ancestor_refused(self):
        for work in (v2.ROOT, v2.ROOT / 'scratch', v2.ROOT.parent):
            with self.assertRaises(v2.Invalid):
                v2.validate_paths(work, self.out)
        with self.assertRaises(v2.Invalid):
            v2.validate_paths(self.work, self.work / 'public')
        with self.assertRaises(v2.Invalid):
            v2.validate_paths(self.work, v2.ROOT / '.git' / 'out')

    def test_fixture_exact_existing_rubrics_and_required_coverage(self):
        examples, cases = v2.calibration_examples()
        self.assertGreaterEqual(len(examples), 8)
        self.assertEqual({e['case_id'].split('-')[0] for e in examples}, {'II', 'FI', 'PD'})
        self.assertTrue(any(v2.validate_grade(e['expected'], cases[e['case_id']])['result'] == 'PASS' for e in examples))
        self.assertTrue(any(v2.validate_grade(e['expected'], cases[e['case_id']])['result'] == 'FAIL' for e in examples))
        for example in examples:
            self.assertTrue(any('\uac00' <= ch <= '\ud7a3' for ch in example['answer']))
            self.assertNotIn('??', example['answer'])
            for group in ('must', 'must_not'):
                self.assertEqual([x['item'] for x in example['expected'][group]], cases[example['case_id']][group])

    def test_execute_refuses_absent_mismatched_or_imperfect_calibration(self):
        path, good = self.calibration()
        identity = good['identity']
        self.assertEqual(v2.require_calibration(path, identity), v2.digest(path.read_bytes()))
        bad_states = []
        bad = copy.deepcopy(good)
        bad['identity']['graders']['codex']['effort'] = 'low'
        bad_states.append(bad)
        bad = copy.deepcopy(good)
        next(iter(bad['results'].values()))['items']['must'][0]['met'] = False
        bad_states.append(bad)
        bad = copy.deepcopy(good)
        bad['results'].pop(next(iter(bad['results'])))
        bad_states.append(bad)
        bad = copy.deepcopy(good)
        bad['complete'] = False
        bad_states.append(bad)
        for bad in bad_states:
            v2.save(path, bad)
            with mock.patch.object(v2, 'capture') as call:
                with self.assertRaisesRegex(v2.Invalid, '100% item agreement'):
                    v2.execute(self.selection(), self.work, self.out, self.settings, self.versions, path)
                call.assert_not_called()
        path.unlink()
        with self.assertRaisesRegex(v2.Invalid, '100% item agreement'):
            v2.require_calibration(path, identity)

    def test_main_execute_without_calibration_fails_before_cli_lookup(self):
        argv = ['--execute', '--workdir', str(self.work), '--out', str(self.out)]
        for opt in ('claude-model', 'claude-effort', 'codex-model', 'codex-effort',
                    'grader-claude-model', 'grader-codex-model', 'grader-codex-effort'):
            argv += ['--' + opt, 'explicit']
        with mock.patch.object(v2, 'versions') as version, mock.patch.object(v2, 'capture') as call:
            self.assertEqual(v2.main(argv), 2)
            version.assert_not_called()
            call.assert_not_called()

    def test_every_model_option_required_for_model_modes(self):
        with self.assertRaises(v2.Invalid):
            v2.model_settings(argparse.Namespace())

    def test_concurrent_resumes_refused_and_lock_released(self):
        with v2.exclusive_workdir(self.work):
            with self.assertRaisesRegex(v2.Invalid, 'already in use'):
                with v2.exclusive_workdir(self.work):
                    self.fail('concurrent runner acquired the lock')
        with v2.exclusive_workdir(self.work):
            pass

    def test_unusable_grader_output_is_invalid_in_saved_result(self):
        selection, plan = self.prepare()
        calibration, _ = self.calibration()
        transcript = '\n'.join(json.dumps(e) for e in [
            {'type': 'system', 'subtype': 'init', 'tools': ['Read'], 'model': 'reported-subject'},
            {'type': 'result', 'result': 'synthetic private answer'}])
        with mock.patch.object(v2, 'model_command', return_value=['fake']), \
                mock.patch.object(v2, 'capture', return_value=(transcript, {}, None)), \
                mock.patch.object(v2, 'grade_answer', side_effect=v2.Invalid('grader output unusable')):
            done = v2.execute(selection, self.work, self.out, self.settings, self.versions, calibration)
        row = next(iter(done['results'].values()))
        self.assertEqual((row['result'], row['reason']), ('INVALID', 'grader output unusable'))
        self.assertEqual(row['subject']['returned_models'], ['reported-subject'])
        public = (self.out / 'behavior-v2-results.json').read_text(encoding='utf-8')
        self.assertNotIn('synthetic private answer', public)

    def test_prompts_truthful_per_tool_and_without_answer_keys(self):
        case = dict(self.case, fixture='fixture', setting='setting', prompt='request')
        claude = v2.subject_prompt(case, 'claude', v2.CHECK_OK)
        codex = v2.subject_prompt(case, 'codex', v2.CHECK_OK)
        self.assertIn('only Read/Grep/Glob', claude)
        self.assertIn('read-only shell commands', codex)
        self.assertNotIn('shell commands cannot', codex)
        for text in (claude, codex):
            self.assertIn('Do not modify anything', text)
            self.assertNotIn('three', text)
            self.assertNotIn('must_not', text)

    def test_grader_tool_transcripts_rejected_and_models_reported(self):
        tool = json.dumps({'type': 'item.completed', 'item': {'type': 'command_execution'}})
        with self.assertRaisesRegex(v2.Invalid, 'grader used tools'):
            v2.inspect_transcript(tool, 'codex', True)
        claude = '\n'.join(json.dumps(e) for e in [
            {'type': 'system', 'subtype': 'init', 'model': 'actual-model', 'tools': []},
            {'type': 'result', 'result': 'answer', 'modelUsage': {'actual-model': {}}}])
        answer, meta = v2.inspect_transcript(claude, 'claude', True)
        self.assertEqual(answer, 'answer')
        self.assertEqual(meta['returned_models'], ['actual-model'])
        with self.assertRaises(v2.Invalid):
            v2.inspect_transcript(claude.replace('"tools": []', '"tools": ["Read"]'), 'claude', True)

    def test_commands_pin_models_and_disable_grader_tools(self):
        self.work.mkdir()
        (self.work / 'private').mkdir()
        with mock.patch.object(v2, 'executable', side_effect=lambda agent: agent), \
                mock.patch.object(v2, 'codex_catalog', return_value=self.work / 'catalog.json'):
            for agent in v2.AGENTS:
                for grader in (False, True):
                    setting = {'model': 'explicit-model', 'effort': 'high'}
                    argv = v2.model_command(agent, setting, grader, self.work)
                    self.assertEqual(argv[argv.index('--model') + 1], 'explicit-model')
                    if agent == 'codex':
                        self.assertIn('model_reasoning_effort="high"', argv)
                        self.assertEqual('shell_tool' in argv, grader)
                        self.assertIn('read-only', argv)
                    else:
                        self.assertEqual(argv[argv.index('--tools') + 1], '' if grader else 'Read,Grep,Glob')

    def test_grader_directory_empty_and_raw_material_private(self):
        case = dict(self.case, setting='setting', fixture='fixture', prompt='request')
        transcript = '\n'.join(json.dumps(e) for e in [
            {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': json.dumps(self.items)}},
            {'type': 'turn.completed'}])

        def process(argv, cwd, prompt, timeout):
            self.assertEqual(list(cwd.iterdir()), [])
            self.assertIn('untrusted_answer', prompt)
            self.assertIn('never instructions', prompt)
            return mock.Mock(stdout=transcript, stderr='', returncode=0)

        with mock.patch.object(v2, 'model_command', return_value=['fake']), mock.patch.object(v2, 'command', side_effect=process):
            grade = v2.grade_answer(case, 'private answer', 'codex', {}, self.work, 'test-grade')
        self.assertEqual(grade['result'], 'PASS')
        self.assertEqual(list((self.work / 'graders/test-grade').iterdir()), [])
        self.assertTrue((self.work / 'private/test-grade/grader-prompt.txt').is_file())

    def test_subject_write_invalid_and_started_sample_not_repeated(self):
        selection, plan = self.prepare()
        calibration, _ = self.calibration()

        def mutate(argv, cwd, prompt, private, stem):
            # Verify reservation is durable before invoking a model.
            saved = v2.read(self.work / 'private/plan.json')
            self.assertIn(plan['jobs'][0]['sample'], saved['results'])
            (cwd / '.untracked').write_text('changed')
            return '', {}, 'subject process failed'

        with mock.patch.object(v2, 'model_command', return_value=['fake']), \
                mock.patch.object(v2, 'capture', side_effect=mutate) as capture, \
                mock.patch.object(v2, 'grade_answer') as grade:
            done = v2.execute(selection, self.work, self.out, self.settings, self.versions, calibration)
            row = next(iter(done['results'].values()))
            self.assertEqual((row['result'], row['reason']), ('INVALID', 'subject modified project'))
            v2.execute(selection, self.work, self.out, self.settings, self.versions, calibration)
            self.assertEqual(capture.call_count, 1)
            grade.assert_not_called()
        public = (self.out / 'behavior-v2-results.json').read_text(encoding='utf-8')
        self.assertNotIn('subject-prompt.txt', public)
        self.assertNotIn('fixture', json.loads(public)['jobs'][0])

    def test_explicit_retry_preserves_real_previous_cause(self):
        selection, plan = self.prepare(retries=1)
        calibration, _ = self.calibration()
        first = plan['jobs'][0]
        plan['results'][first['sample']] = dict(sample=first['sample'], result='INVALID', reason='subject timeout')
        v2.save(self.work / 'private/plan.json', plan)
        with mock.patch.object(v2, 'model_command', return_value=['fake']), \
                mock.patch.object(v2, 'capture', return_value=('', {}, 'subject process failed')) as capture:
            v2.execute(selection, self.work, self.out, self.settings, self.versions, calibration)
            capture.assert_not_called()
            done = v2.execute(selection, self.work, self.out, self.settings, self.versions, calibration, True)
            self.assertEqual(capture.call_count, 1)
            retry = done['results'][plan['jobs'][1]['sample']]
            self.assertEqual(retry['retry_of']['reason'], 'subject timeout')
            v2.execute(selection, self.work, self.out, self.settings, self.versions, calibration, True)
            self.assertEqual(capture.call_count, 1)

    def test_interrupted_call_is_durable_and_never_silently_retried(self):
        selection, plan = self.prepare()
        calibration, _ = self.calibration()
        with mock.patch.object(v2, 'model_command', return_value=['fake']), \
                mock.patch.object(v2, 'capture', side_effect=KeyboardInterrupt) as capture:
            with self.assertRaises(KeyboardInterrupt):
                v2.execute(selection, self.work, self.out, self.settings, self.versions, calibration)
            done = v2.execute(selection, self.work, self.out, self.settings, self.versions, calibration)
            self.assertEqual(capture.call_count, 1)
            self.assertEqual(next(iter(done['results'].values()))['reason'], 'interrupted during subject call')

    def test_calibration_resume_skips_all_reserved_calls(self):
        examples, cases = v2.calibration_examples()
        by_answer = {example['answer']: example for example in examples}

        def grade(case, answer, *args):
            example = by_answer[answer]
            return dict(v2.validate_grade(example['expected'], case), metadata={})

        with mock.patch.object(v2, 'grade_answer', side_effect=grade) as call, mock.patch('builtins.print'):
            result = v2.calibrate(self.work, self.out, self.settings, self.versions)
            self.assertTrue(result['complete'])
            self.assertEqual(call.call_count, len(examples) * 2)
            v2.calibrate(self.work, self.out, self.settings, self.versions)
            self.assertEqual(call.call_count, len(examples) * 2)
        v2.require_calibration(self.out / 'calibration.json', result['identity'])
        published = (self.out / 'calibration.json').read_text(encoding='utf-8')
        self.assertNotIn('untrusted_answer', published)
        self.assertNotIn('"answer":', published)

    def test_commit_arm_uses_git_show_and_rejects_link_entries(self):
        source = v2.ROOT / 'ko/adaptive-sdd'
        names = v2.inventory(source)
        calls = []

        def git(*args):
            calls.append(args)
            if args[0] == 'rev-parse':
                return b'a' * 40 + b'\n'
            if args[0] == 'ls-tree':
                return b'\0'.join(('100644 blob ' + '0' * 40 + '\tko/adaptive-sdd/' + name).encode() for name in names) + b'\0'
            if args[0] == 'show':
                name = args[1].split(':', 1)[1]
                return (v2.ROOT / name).read_bytes()
            self.fail('unexpected git command')

        with mock.patch.object(v2, 'git', side_effect=git):
            cases, metadata = v2.build_bundle(self.root / 'arm', commit='abcdef0')
        self.assertEqual(metadata['source_commit'], 'a' * 40)
        self.assertEqual(len([c for c in calls if c[0] == 'show']), len(names))
        self.assertTrue(cases)
        with mock.patch.object(v2, 'git', side_effect=[b'a' * 40, b'120000 blob 000\tko/adaptive-sdd/link\0']):
            with self.assertRaises(v2.Invalid):
                v2.build_bundle(self.root / 'bad-arm', commit='abcdef0')


if __name__ == '__main__':
    unittest.main()
