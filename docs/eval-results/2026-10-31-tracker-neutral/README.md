# Tracker-neutral wording — bounded behavior check (2026-10-31)

Status: **COMPLETE, weak evidence.** 10 graded runs: 4 PASS, 6 FAIL. No failure was traced to the preview.6 wording change. Most failures come from the evaluation environment, described below. This check does not show that the change improves or preserves behavior in general.

## What ran

- Selection: [selection.json](selection.json), frozen before the first run at `1b99d2187ab4d3650e716f1abf0c498b2c229ca0`. Five existing Korean cases whose expected behavior touches a moved operation, one run per case per agent, cross-graded with `tests/run_behavior_evals.py`.
- Evaluated bundle: `ko/adaptive-sdd`, MANIFEST sha256 `38c130ee855f91db1af3a4b463de0dfc7aeaee9eb76ebd5159ea009eb044a6a5`. The `commit` field in each result file carries the runner's fixed "uncommitted preview.5 working tree" label; the manifest hash is the identity.
- Claude Code 2.1.302 (`claude-opus-5-5` returned), Codex CLI 0.163.0 (configured default model; served model unconfirmed).
- First attempt: all 10 runs INVALID. Every Claude call (as subject and as grader) returned HTTP 403 `oauth_not_allowed_for_organization` from the inherited Claude configuration directory, before inference. The runner's `--resume` then did one bounded retry, as `skill-evals.md` allows: the five Claude runs were rerun once and the five saved Codex answers were regraded once, with the Claude CLI using the default home sign-in. No second retry was made.

## Results

| Case | Claude Code | Codex |
| --- | --- | --- |
| MI-S01 convenience bug (create with Priority/grade) | PASS | FAIL |
| MI-S08 optional Epic, unresolved investigation | PASS | FAIL |
| FI-S03 closing reference (local-docs) | FAIL | FAIL |
| FI-S20 declared merge target (`release`) | FAIL | PASS |
| PD-S01 clean claim | PASS | FAIL |

Item-level misses are in `results/<agent>/<skill>.json`. Raw answers stay outside the repository.

## Why the failures do not point at the wording change

These are the author's reading of the private answers, not an independent regrade.

- **Codex did not read the rules in three runs.** The runner tells the subject "shell commands cannot be run", and Codex reads files through the shell. In MI-S01, MI-S08 and PD-S01 Codex said it could not read the skill or project rules and answered without them. In the 2026-10-30 baseline Codex passed MI-S01 and PD-S01 in only 1 of 3 runs each, with the same runner text.
- **The disposable project conflicts with two finishing fixtures.** The runner installs the example `project.json`, whose merge method is empty and whose merge branch is `main`. FI-S03 expects a merge confirmation, and FI-S20 says the merge branch is `release`. Claude followed the declared values: it stopped with `BLOCKED: tracker operation unsupported` for the missing merge method and refused to check against `release` while `main` was declared. The graders counted those stops as misses.
- **The moved wording was applied where it was exercised.** In FI-S03 Claude mapped the closing reference to `closes: T-42` and said not to write the GitHub `Closes #42` form for local documents. In FI-S20 it wrote the local-docs `product-complete:` JSON (`"issue":"T-N","pull_request":null`). MI-S08 kept the Epic without a grade.

## Limits

- One run per case per agent is a smoke check, not a reliability estimate.
- Only the local-docs adapter was exercised. The GitHub adapter rows are covered by static tests (`tests/test_tracker_neutral.py`) only.
- The two environment problems above are runner and fixture issues. They are recorded here and left unchanged in this release; fixing them needs a separately frozen run.
- The Claude retry used a different sign-in from the first attempt. No observations from the failed sign-in are pooled; all 10 graded results come from the retry or regrade.
