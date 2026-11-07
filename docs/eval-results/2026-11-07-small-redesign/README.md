# Small redesign: before/after runs — 2026-11-07

Three Codex runs of the same Small task on the workflow before the 1.1.0 Small redesign, and three on the workflow after it. This measures what the redesign changed in one planted task. It does not measure effect on outcomes, rework or cost in real projects.

## Setup

- Before: `20b72b0` (`aa29adf`, the pre-redesign distribution, merged with `348c2d2` from PR #16). After: `b81c618` (`7007e4c`, the redesign, merged with the same `348c2d2`). The two differ only in the redesign.
- Each run used its own fresh sandbox from that version's `try/setup.py` (English edition) and the selection prompt from its `START-HERE.md`, with the last line replaced by the Small task: fix `catalog.search.page` so `page([1, 2, 3, 4], 1, 3)` returns `[1, 2, 3]` and add regression tests.
- Agent: Codex CLI 0.163.0, requested `gpt-6-astra` / `high`, `codex exec --json`, workspace-write sandbox on Windows. Served model identity was not separately verified.
- All six runs ran at the same time on one machine.
- Deviations from START-HERE:
  - Each sandbox was created under the Codex sandbox account, so Git accepts its repositories without a trust override.
  - Codex started in the folder above the sandbox, not in `product/`, because the workspace-write sandbox makes the `.git` of its starting folder read-only.
  - Two earlier attempts of all six runs are not counted. In the first, the resolver returned BLOCKED (Git ownership). In the second, every run stopped at `git fetch` (read-only `.git`). Both are environment problems, and they affected the two versions the same way.

## Results

All six runs fixed the bug, added regression tests, merged into the local origin `main`, closed the item and released the claim. For every run, a fresh clone of origin `main` passed all product tests, and `page([1, 2, 3, 4], 1, 3)` returned `[1, 2, 3]`.

| Mean of 3 runs | Before | After | Change |
| --- | --- | --- | --- |
| Records in the work item | 7 | 3 | identical in every run |
| Lines in the item's Records section | 107 | 57 | −47% |
| Command output returned to the agent (characters) | 276k | 186k | −33% |
| Workflow files named in the agent's commands | 15–18 | 14 | same 14 files in every run |
| Words in those files | 26.5k | 22.9k | −14% |
| Input tokens | 906k | 829k | −8% |
| Output tokens | 8.5k | 8.7k | about the same |
| Wall time | 268 s | 278 s | no difference shown |

Records before: CLAIM, IMPLEMENTATION SUMMARY, MERGED, CLOSED, PRODUCT COMPLETE, LOCAL CLEANUP, RELEASE. After: CLAIM, IMPLEMENTATION SUMMARY, CLOSED.

Per-run values are in [`results.json`](results.json).

## Limits

- One planted Python task, one agent, the English edition, three runs per version.
- Wall time is noisy because the six runs shared one machine.
- File and word counts are an upper bound. A file counts as read when the agent's commands name it, but agents sometimes read only matching lines. Command output is the more direct measure of what the agent took in.
- Input tokens fall less than command output because each step resends the conversation so far.
- The fixed reading set is still about 23k words for a one-line fix, and wall time did not improve. Shortening that reading set is not part of this release.
