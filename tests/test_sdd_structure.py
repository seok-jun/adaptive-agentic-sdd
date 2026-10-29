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


if __name__ == '__main__':
    unittest.main()
