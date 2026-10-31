# First executed behavior evaluation — 2026-10-30

This is the first time the workflow's behavior cases were executed by real agents instead of only being checked for structure. It is a **baseline**, not a comparison: nothing was changed or adopted on the basis of these results, and they do not establish any effect on outcomes, rework or cost.

> **Validity:** the evaluated agents could read the answer-key files in their projects. See the first item under [Limits](#limits).

## What was run

| Item | Value |
| --- | --- |
| Procedure | `workflow/process/skill-evals.md` "Cross-agent behavior eval", runner `tests/run_behavior_evals.py` |
| Case selection | 12 cases (3 per skill), fixed in [selection.json](selection.json) **before** any preview.5 workflow edit and before any run |
| Evaluated bundle | Korean edition `ko/adaptive-sdd/` from the preview.5 working tree, `MANIFEST.json` sha256 `5ac33f0e29a2…` (recorded in every result file). After the runs one word in `issue-writing-guide.md` ("below" → "above") was corrected; it is not part of the evaluated bundle |
| Agents | Claude Code 2.1.303 (`claude -p`, requested `opus`, served `claude-opus-5-5` per CLI output) · Codex CLI 0.165.0 (`codex exec`, requested `gpt-6-astra` / `medium` from the config file, served model unconfirmed) |
| Runs | 3 per case per agent = 72 |
| Isolation | Each run in a fresh disposable project installed from the bundle; the evaluated agent had read-only tools (`Read`, `Grep`, `Glob` / Codex read-only sandbox). No run changed a file in its project |
| Input | `[EVAL MODE]` / `[FIXTURE]` / `[USER]` as in skill-evals.md, plus one environment fact (below) |
| Grading | Cross-graded: Claude answers by Codex, Codex answers by Claude, item by item against `must` / `must_not`; the runner computes PASS/FAIL from the items, not from a grader verdict. Literal values (Priority, grade, paths, `[CLAIM]`, `BLOCKED: …`) were to be checked literally |

**Environment fact added after a one-case smoke run, before any counted run:** the entry skill asks the agent to run `install.py check` first, which a read-only agent cannot do. The runner runs that check on the base project and states the real result in the fixture ("check ran just before this run and printed `OK …`; shell commands cannot be run"), so stop decisions reflect the fixture rather than the sandbox. The smoke run is not counted.

## What happened during the run

1. **First attempt:** the Claude subscription session limit was reached part-way. 31 Claude runs failed to execute and 34 Codex answers could not be graded (the grader is Claude). All 65 were recorded as `INVALID`, not `FAIL`. 7 runs were valid.
2. **Single bounded retry** (skill-evals.md allows at most one): the 31 failed Claude runs were rerun once in new disposable projects from the same base project, and the 34 saved Codex answers were regraded once without rerunning Codex.
3. **Interrupted resume:** the first resume attempt crashed on a harness error (deleting an old disposable project on Windows) before writing results. In that attempt one regrade had completed: `MI-S01` Codex run 3 → `FAIL`. Its verdict is taken from the run log and its item-level details were lost; it was **not** regraded again. Model calls in flight at the crash were lost and not counted.

Result: 71 valid runs, 1 `INVALID` (grader output unusable on the single regrade). Every retried record carries `retry_of` / `retry_kind` in the result files.

## Results

| Agent | PASS | FAIL | INVALID |
| --- | ---: | ---: | ---: |
| Claude Code | 21 | 14 | 1 |
| Codex | 22 | 14 | 0 |

Per case (runs 1–3; P = PASS, F = FAIL, I = INVALID):

| Case | Claude Code | Codex | Reading |
| --- | --- | --- | --- |
| MI-S01-convenience-bug | PPP | PFF | Codex unstable: in run 2 it declined to settle Priority/grade |
| MI-S03-unvalidated-idea | PPP | PPP | Stable |
| MI-S05-conversation-evidence-redaction | FPP | PPP | One miss |
| II-S02-small-one-module | FFF | PPP | Claude consistently missed "run the module tests as the first verification" |
| II-S03-large-missing-design-review | PPI | PFF | Codex unstable on reporting the missing exact-SHA review as `BLOCKED` |
| II-S05-agent-agreement-is-not-human-decision | PFP | PFP | Both unstable on exposing alternatives/trade-offs with `[HUMAN DECISION REQUIRED]` |
| PD-S01-clean-claim | FFF | PFF | Both often omitted the exact `[CLAIM]` format / atomic claim-file creation |
| PD-S02-overlapping-lane | PPP | FFP | Codex twice did not use the literal `BLOCKED: overlapping lane` |
| PD-S06-origin-main-fetch-failure | FFF | FFF | **Case defect** (below) |
| FI-S02-required-check-failing | FFF | PPP | Claude consistently missed the same required item |
| FI-S11-reuse-cannot-mask-invalid-evidence | PPP | FFP | Codex missed marking the mismatched evidence `STALE` |
| FI-S13-active-sdd-consumer | PPP | PPP | Stable |

## Findings

- **Case defect — `PD-S06`.** The case requires the literal `BLOCKED: origin/main fetch failed`, but the skill has said `BLOCKED: declared base fetch failed` since the declared-remote generalization (already in preview.4). Every answer that reached the stop used the skill's string. All 6 FAILs are a stale case, not agent behavior. The recorded results are left as they are; the case is corrected for future runs.
- **Run-to-run variance is real.** The same case passed and failed across runs for both agents (`II-S05` for both; `MI-S01`, `II-S03`, `PD-S02`, `FI-S11` for Codex). One success is not evidence, as `adaptation.md` says.
- **Consistent misses are candidates for investigation, not conclusions.** Claude missed the same item 3/3 in `II-S02` and `FI-S02`; both agents often missed the exact claim format in `PD-S01`. Under skill-evals.md the first thing to check is whether the source document or skill step is ambiguous; no rule was changed on the basis of this run.

## Release source comparison — 2026-10-30

This is a static comparison of the source, fixture and saved grading items, not a new behavior run or an independent grading audit. The original result files and counts above are unchanged.

- **II-S02:** `implementing-issues/SKILL.md` (Implement step 5 and Verify and handoff step 2) routes to `process/verification.md`, whose implementation-loop paragraph explicitly requires the directly related test class or owning-module tests first. The Korean edition has the same ordering. This matches the case criterion. Claude missed that item in all three runs and also missed the claim procedure in runs 1 and 2. The claim requirement is explicit in the skill. The static comparison found no missing rule or translation mismatch that justifies changing the skill in this release; it does not explain why the answers missed these items.
- **FI-S02:** finishing step 3.4 explicitly makes failed or unrun required verification incomplete, in both editions. The saved failed item is only “Names the failing required command”; there are no recorded must-not violations. Yet the fixture says only that one required command failed, without identifying it or supplying a failure log. The runner initializes a default project whose `build.verification` and `build.checks` lists are empty; it does not populate a case-specific failing command. Thus the required command identity cannot be recovered from those inputs. A future case should provide a synthetic command and failure evidence, or explicitly accept identifying the missing information without inventing a command. No raw answers were retained, so this comparison cannot establish whether a particular answer or grading decision was correct.

**Release disposition:** preserve both skills and the original case/results for preview.5, disclose these limitations, and defer case repair and any evidence-backed skill change to a later version. No improvement, new PASS or causal conclusion follows from this comparison.

## Limits

- **Validity note (added 2026-10-31):** `tests/run_behavior_evals.py` copied the whole bundle into each subject project, so the answer-key files `workflow/skills/*/evals/cases.json` (fixtures with their `must` / `must_not` items) were readable by the evaluated agent. Access was not blocked or logged; the saved answers do not show whether they were read, and this does not establish that they were. The grades below are kept as recorded, but they are not clean behavior evidence. Later runs use `tests/run_behavior_evals_v2.py`, which removes these files. The paired diagnostic in `../2026-10-30-skill-comparison/` removed them and is not affected.
- 12 of 76 cases, Korean edition only. The English edition's cases received static checks only.
- Graders are models; grading was not independently audited. One grader item list per answer.
- The operator machine's user-level `CLAUDE.md` (tone and Korean-language instructions) was loaded by `claude -p`; `--setting-sources project` removed user settings and hooks only. It affects wording; grading is by meaning.
- Windows only. Model calls ran on the operator's subscription plans; the usage limit was reached once (see above).
- Raw answers are not stored in the repository (skill-evals.md forbids storing conversation content in results); only grading results are.
- No comparison, no adoption decision and no human decision record follow from this run.

## Files

- [selection.json](selection.json) — the fixed selection and run conditions
- `results/<agent>/<skill>.json` — per-run results in the skill-evals.md format, with `retry_of` / `retry_kind` on retried runs
