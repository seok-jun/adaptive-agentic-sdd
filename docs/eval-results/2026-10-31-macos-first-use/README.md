# macOS handoff check — 2026-10-31

An assisted walkthrough of the [PR #6 macOS handoff](../../handoff/macos-first-use/README.md), on macOS 12.7.6 Intel, Python 3.14.10 and Apple Git 2.37.1. Candidate installed: `1d91d9448621c29e39c248bf1c1f23a098ecb02d`; repository tests used the source of PR head `2900393c7b33b1775c6e3c62d35256df9c7e756e`. The English bundle trees are identical.

- Native repository tests: 88 tests run, two subtest failures in generated external commands because `python` is unavailable. [Native log](repository-tests-native.log), [last 15 lines](repository-tests-native-last15.log).
- Controlled diagnostic: adding a `python` symlink to the existing Python 3 interpreter to the test process PATH, without source changes, yielded 88 tests passing. [Diagnostic log](repository-tests-python-compat.log).
- Installation succeeded using `python3`; pinned-copy checks and all 83 eval specifications passed validation. No behavior eval model calls were made.
- Small task T-1 corrected the catalog pagination endpoint, demonstrated regression failure before the fix, and passed module tests (3) and the complete sample suite (4). Merged and pushed to the disposable local bare origin; task closed and claim released.
- Git 2.37 lacks `merge-tree --write-tree`; the adapter's existing disposable-worktree merge fallback succeeded.
- Reverting the installation and pushing left the product fix and regression tests intact. Installation paths are absent on main, existing AGENTS.md restored, sample status clean. Task branches retain installation history as the README describes.

This is **not blind first-use evidence**: the same agent had read the evaluator's suspected-friction notes and performed the walkthrough. Shell GitHub DNS failed, so repository files were restored through GitHub's connector and checked against source hashes; this was not an archive installation from a full original clone. Required historical commit metadata was separately restored with exact Git SHA verification for the unit tests. Claude was unavailable and no separate Codex session was run. The [full Korean report](report.md) records source reconstruction, manual workarounds, agent mistakes and limits.

The source methodology and evaluation runners were not changed. These observations identify Python command portability as a follow-up candidate; they do not establish methodology effectiveness or a failure rate.

The remaining files preserve the sample's [final state](final-state.log), [task record](tracker/items/T-1.md), installation inventory and validation logs. No upstream GitHub comments or changes were published.

Export note: local source and disposable-project paths are normalized to `<source-root>` and `<demo-root>` in the published evidence. The installation lock and project draft are retained locally and excluded from this export.
