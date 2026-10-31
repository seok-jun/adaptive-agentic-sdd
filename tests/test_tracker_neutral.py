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
    'en': ('Issue creation API', 'Remove the existing `priority:*` label',
           'assumes a GitHub feature', 'first refined on this method'),
    'ko': ('Issue 생성 API', '기존 `priority:*` 라벨 제거', 'GitHub 기능을 전제', '처음 다듬어졌으므로'),
}
# (row label, required text in that row) per adapter. The values carry the moved contracts.
ADAPTER_ROWS = {
    'en': {
        'github.md': (
            ('Setting the Priority/grade values at creation', 'Include both labels in the creation request'),
            ('Replacing a `priority:*` value', 'Remove the existing `priority:*` label, then add the new one'),
            ('Order of Issue numbers', 'The GitHub Issue number'),
            ('PR, `Closes #N`', 'the closing reference `Closes #N` in its body'),
            ('The `product-complete:` JSON of `[PRODUCT COMPLETE]`', '"issue":N,"pull_request":PR'),
        ),
        'local-docs.md': (
            ('Setting the Priority/grade values at creation', 'in the same write that creates the document'),
            ('Replacing a `priority:*` value', 'Rewrite the `priority:` line in `## Meta`'),
            ('Order of Issue numbers', '`<ID>`, the same mapping as the Issue number above'),
            ('`Closes #N` in the PR body', 'The `closes: <ID>` line of the `[IMPLEMENTATION SUMMARY]` entry'),
            ('The `product-complete:` JSON of `[PRODUCT COMPLETE]`', '"issue":"<ID>","pull_request":null'),
        ),
    },
    'ko': {
        'github.md': (
            ('생성할 때 Priority·grade 값 지정', '생성 요청에 두 라벨을 포함'),
            ('`priority:*` 값 교체', '기존 `priority:*` 라벨을 제거한 뒤 새 라벨 추가'),
            ('Issue 번호 순서', 'GitHub Issue 번호'),
            ('PR, `Closes #N`', '본문의 closing reference `Closes #N`'),
            ('`[PRODUCT COMPLETE]`의 `product-complete:` JSON', '"issue":N,"pull_request":PR'),
        ),
        'local-docs.md': (
            ('생성할 때 Priority·grade 값 지정', '문서를 만드는 같은 쓰기에서'),
            ('`priority:*` 값 교체', '`## 메타`의 `priority:` 줄을 고쳐 쓴다'),
            ('Issue 번호 순서', '`<ID>`. 위 Issue 번호와 같은 대응'),
            ('PR body의 `Closes #N`', '`[IMPLEMENTATION SUMMARY]` 항목의 `closes: <ID>` 줄'),
            ('`[PRODUCT COMPLETE]`의 `product-complete:` JSON', '"issue":"<ID>","pull_request":null'),
        ),
    },
}
NEUTRAL_STEPS = {
    'en': {'process/issue-priority.md': ('in the ID order of the declared tracker method',
                                         'If the declared tracker method can set both values when the Issue is created'),
           'process/sdd/completion.md': ('add the closing reference to this Issue',)},
    'ko': {'process/issue-priority.md': ('선언한 작업 관리 방식의 ID 순서로 Issue 번호가 작은 것',
                                         '선언한 작업 관리 방식이 Issue를 만들 때 두 값을 함께 정할 수 있으면'),
           'process/sdd/completion.md': ('이 Issue의 closing reference',)},
}


def row(text, label):
    rows = [line for line in text.splitlines() if line.startswith(f'| {label} |')]
    return rows[0] if len(rows) == 1 else None


class TrackerNeutralTests(unittest.TestCase):
    def test_procedures_do_not_carry_github_only_mechanics(self):
        for edition, workflow in EDITIONS.items():
            for path in workflow.rglob('*.md'):
                if path.parent.name == 'tracker':
                    continue
                text = path.read_text(encoding='utf-8')
                for phrase in GITHUB_ONLY[edition]:
                    self.assertNotIn(phrase, text, f'{edition}: {path.relative_to(workflow)}')

    def test_adapters_map_the_moved_operations_with_their_values(self):
        for edition, adapters in ADAPTER_ROWS.items():
            for adapter, rows in adapters.items():
                text = (EDITIONS[edition] / 'tracker' / adapter).read_text(encoding='utf-8')
                for label, value in rows:
                    line = row(text, label)
                    self.assertIsNotNone(line, f'{edition} {adapter}: exactly one row {label!r}')
                    self.assertIn(value, line, f'{edition} {adapter}: {label}')

    def test_procedures_state_the_neutral_steps(self):
        for edition, files in NEUTRAL_STEPS.items():
            for name, phrases in files.items():
                text = (EDITIONS[edition] / name).read_text(encoding='utf-8')
                for phrase in phrases:
                    self.assertIn(phrase, text, f'{edition}: {name}')

    def test_workflow_readme_defines_neutral_terms(self):
        for edition, workflow in EDITIONS.items():
            text = (workflow / 'README.md').read_text(encoding='utf-8')
            self.assertIn('`Closes #N`', text, edition)
            self.assertIn('tracker.md', text, edition)


if __name__ == '__main__':
    unittest.main()
