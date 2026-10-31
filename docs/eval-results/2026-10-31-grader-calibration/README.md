# Grader calibration for runner v2 (2026-10-31)

Status: **PASS — 132 of 132 rubric items agreed** (Claude grader 66/66, Codex grader 66/66). `tests/run_behavior_evals_v2.py --execute` is allowed only with this exact grader setting.

## What was checked

- Fixture: [`tests/fixtures/grader-calibration.json`](../../../tests/fixtures/grader-calibration.json), 11 hand-written synthetic answers over three Korean cases (II-S02, FI-S02b, PD-S01), each with the expected boolean for every `must` and `must_not` item. The examples include a narrower but valid allowed path set inside `loan-service/**`, an out-of-scope edit, claim conditions versus an acquired claim, planned versus executed commands, an invented execution result and "other tests passed" used as completion.
- Graders: Claude Code 2.1.302 `claude-opus-5-5` (effort medium) and Codex CLI 0.163.0 `gpt-6-astra` (reasoning medium), each with no tools, an empty working directory and the runner's grading instructions. One call per example per grader, 22 calls, no retry.
- Identity: runner sha256 `413ed1090c6b51df887fe3d6a4b155e4bdc7d8d4b8889d814c91e5df56fadddf`, fixture sha256 `6c8618e1fbd21cef6d16213fcd9c0abe086cef52f1182e432566c57a89fff964`, cases sha256 `2f166544e2d61456e0f6bb238a069d4191575692fe7145a0f874423e25ceddb8`. Item outcomes and transcript hashes are in [calibration.json](calibration.json); raw transcripts stay outside the repository.
- The Claude grader ran with the default home sign-in; the session's inherited Claude configuration directory returns HTTP 403 for subscription access.

## What it does not show

- Eleven synthetic answers written by the author of the fixture are a gate against known grading mistakes, not a measure of grader accuracy on real answers.
- It says nothing about subject behavior. No subject run was made.
- A change to the runner, the fixture, the cases or the grader models or efforts needs a new calibration.

## Runner v2 in brief

`tests/run_behavior_evals_v2.py` replaces the old runner for new evidence; the old runners stay unchanged because earlier records depend on their bytes. v2 removes the answer-key files from every subject bundle and checks that none remain, tells each tool truthfully what it can read, makes any file change during a subject run INVALID, applies per-case `project_overrides` identically to every arm, requires explicit models and efforts, accepts a grade only when every rubric item comes back in order with its exact text and a real boolean, records the real commit and failure causes, and refuses `--execute` without a matching 100% calibration. 23 unit tests cover these without model calls.
