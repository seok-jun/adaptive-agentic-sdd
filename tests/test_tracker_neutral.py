"""W procedures stay tracker-neutral; GitHub-only mechanics live in the GitHub adapter.

Run with: python -I -B -m unittest discover -s tests -v
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
EDITIONS = {
    'en': ROOT / 'adaptive-sdd/workflow',
    'ko': ROOT / 'ko/adaptive-sdd/workflow',
}
# Phrases that describe a GitHub API or label operation rather than a tracker-neutral step.
GITHUB_ONLY = {
    'en': ('Issue creation API', 'Remove the existing `priority:*` label', 'is equal, the lower Issue number',
           'assumes a GitHub feature', 'first refined on this method'),
    'ko': ('Issue 생성 API', '기존 `priority:*` 라벨 제거', 'Issue 번호가 작은 것\n',
           'GitHub 기능을 전제', '처음 다듬어졌으므로'),
}
ADAPTER_ROWS = {
    'en': ('Setting the Priority/grade values at creation', 'Replacing a `priority:*` value',
           'Creation order of Issues'),
    'ko': ('생성할 때 Priority·grade 값 지정', '`priority:*` 값 교체', 'Issue 생성 순서'),
}


class TrackerNeutralTests(unittest.TestCase):
    def test_procedures_do_not_carry_github_only_mechanics(self):
        for edition, workflow in EDITIONS.items():
            for path in workflow.rglob('*.md'):
                if path.parent.name == 'tracker':
                    continue
                text = path.read_text(encoding='utf-8')
                for phrase in GITHUB_ONLY[edition]:
                    self.assertNotIn(phrase, text, f'{edition}: {path.relative_to(workflow)}')

    def test_both_adapters_map_the_moved_operations(self):
        for edition, workflow in EDITIONS.items():
            for adapter in ('github.md', 'local-docs.md'):
                text = (workflow / 'tracker' / adapter).read_text(encoding='utf-8')
                for row in ADAPTER_ROWS[edition]:
                    self.assertIn(f'| {row} |', text, f'{edition}: {adapter}')

    def test_workflow_readme_defines_neutral_terms(self):
        for edition, workflow in EDITIONS.items():
            text = (workflow / 'README.md').read_text(encoding='utf-8')
            self.assertIn('`Closes #N`', text, edition)
            self.assertIn('tracker.md', text, edition)


if __name__ == '__main__':
    unittest.main()
