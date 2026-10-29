"""Deterministic document integrity checks; not an LLM behavior evaluation."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'ko/adaptive-sdd'
PROCESS = BUNDLE / 'workflow/process'


def normalize(text):
    # Ignore relocated link destinations, not the contract text.
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    for before, after in {
        '위 `### 일반 자동 격상`': '일반 자동 격상',
        '위 `기존 Epic 전환`': '기존 Epic 전환',
        '`README.md`·`01-as-is.md` → AS-IS required review': '`01-as-is.md` → AS-IS required review',
    }.items():
        text = text.replace(before, after)
    return ' '.join(text.split())


def sections(text):
    return {s.splitlines()[0][3:]: s for s in re.split(r'(?=^## )', text, flags=re.M)[1:]}


class SelectiveReadingTests(unittest.TestCase):
    def test_condensed_list_preserves_unique_conditions(self):
        import copy
        sample = json.loads((ROOT / 'tests/fixtures/sdd-artifact-sample.json').read_text(encoding='utf-8'))['condensation']
        def consumed(after):
            plan = after['RES-1']
            return set(plan['additional']).union(*(set(after[ref]) for ref in plan['references']))
        required = set(sample['required'])
        self.assertEqual(set().union(*map(set, sample['before'].values())), required)
        self.assertEqual(consumed(sample['after']), required)
        # An unchanged AC does not protect conditions unique to the removed list.
        for unique in sample['after']['RES-1']['additional']:
            broken = copy.deepcopy(sample['after'])
            broken['RES-1']['additional'].remove(unique)
            self.assertEqual(broken['AC-1'], sample['before']['AC-1'])
            self.assertEqual(required - consumed(broken), {unique})

    def test_role_inputs_and_existing_guards(self):
        sample = json.loads((ROOT / 'tests/fixtures/sdd-artifact-sample.json').read_text(encoding='utf-8'))
        for path, digest in sample['unchanged_guards'].items():
            self.assertEqual(hashlib.sha256((BUNDLE / path).read_bytes()).hexdigest(), digest)
        packet = (BUNDLE / 'workflow/skills/_shared/execution-packets.md').read_text(encoding='utf-8')
        self.assertEqual(hashlib.sha256(packet.split('### Blind Audit Packet', 1)[1].encode()).hexdigest(), sample['blind_packet_sha256'])
        skill = (BUNDLE / 'workflow/skills/implementing-issues/SKILL.md').read_text(encoding='utf-8').split('## Inputs', 1)[1].split('\n## ', 1)[0]
        for text in (skill, packet.split('### 구현 진입의 문맥·최신성 확인', 1)[1].split('## Result Packet', 1)[0]):
            for term in ('Medium', 'IMPLEMENT', 'README', '기준 revision', 'Blind Audit'):
                self.assertIn(term, text)

    def test_epic_measurement_includes_skill_prerequisites(self):
        from measure_sdd_reading import SCENARIOS
        skill = (BUNDLE / 'workflow/skills/managing-issues/SKILL.md').read_text(encoding='utf-8')
        inputs = skill.split('## Inputs', 1)[1].split('\n## ', 1)[0]
        required = set(re.findall(r'W/process/(sdd/[\w-]+\.md)', inputs))
        selected = set(SCENARIOS['Epic management'][0])
        self.assertTrue(required)
        self.assertFalse(required - selected, f'Missing mandatory inputs: {required - selected}')

    def test_synthetic_split_keeps_each_fact_once(self):
        sample = json.loads((ROOT / 'tests/fixtures/sdd-artifact-sample.json').read_text(encoding='utf-8'))
        self.assertEqual(set(sample['before']), set(sample['after']))
        for side in ('before', 'after'):
            corpus = ''.join(sample[side].values())
            for fact in sample['facts'].values():
                self.assertEqual(corpus.count(fact), 1)
        self.assertNotIn(sample['facts']['agent_evidence'], sample['after']['README.md'])
        self.assertNotIn(sample['facts']['human_as_is'], sample['after']['01-as-is.md'])

    def test_every_original_workflow_section_preserved_once(self):
        mapping = json.loads((ROOT / 'tests/fixtures/sdd-section-map.json').read_text(encoding='utf-8'))
        all_sections = []
        for owner, names in mapping['workflow'].items():
            current = sections((PROCESS / f'sdd/{owner}.md').read_text(encoding='utf-8'))
            self.assertEqual(set(current), set(names))
            for name in names:
                all_sections.append(name)
                digest = hashlib.sha256(normalize(current[name]).encode()).hexdigest()
                self.assertEqual(digest, mapping['section_sha256'][name], name)
        self.assertEqual(len(all_sections), len(set(all_sections)))

    def test_skills_bypass_workflow_index(self):
        for name in ('implementing-issues', 'finishing-issues', 'managing-issues'):
            text = (BUNDLE / f'workflow/skills/{name}/SKILL.md').read_text(encoding='utf-8')
            self.assertNotIn('`W/process/sdd-workflow.md`', text)
            self.assertIn('W/process/sdd/issue.md', text)
            for path in re.findall(r'W/(process/sdd/[\w-]+\.md)', text):
                self.assertTrue((BUNDLE / 'workflow' / path).is_file())

    def test_new_rules_and_templates_are_pinned(self):
        manifest = json.loads((BUNDLE / 'MANIFEST.json').read_text(encoding='utf-8'))['files']
        paths = list((PROCESS / 'sdd').glob('*.md')) + list((BUNDLE / 'templates/sdd').glob('*.tmpl'))
        self.assertEqual(len(paths), 13)
        for path in paths:
            self.assertEqual(manifest[path.relative_to(BUNDLE).as_posix()], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_as_is_review_keeps_both_readers_in_same_target(self):
        review = (PROCESS / 'design-review.md').read_text(encoding='utf-8')
        self.assertIn('AS-IS는 `README.md`와 `01-as-is.md`', review)
        self.assertIn('Review B — Blind Audit', review)
        layout = (PROCESS / 'sdd-artifacts.md').read_text(encoding='utf-8')
        self.assertIn('진행 중 작업은 재작성하지 않는다', layout)
        self.assertIn('별도 `evidence.md`는 필수가 아니며', layout)
        self.assertNotIn('PLAN 작성 뒤에는', layout)
        self.assertIn('README 최초 작성 때 PLAN 위치', layout)
        template = (BUNDLE / 'templates/sdd/README.md.tmpl').read_text(encoding='utf-8')
        self.assertIn('PLAN 예정 경로: `02-to-be.md`', template)


if __name__ == '__main__':
    unittest.main()
