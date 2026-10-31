# Routing policy c′ — behavior check with runner v2 (2026-10-31)

Status: **COMPLETE, not valid as behavior evidence for Codex; partial for Claude.** 16 subject runs and 16 grader calls: 5 PASS, 9 FAIL, 2 INVALID. **No `must_not` item was violated in any of the 14 graded runs.** The grades are kept as recorded in [behavior-v2-results.json](behavior-v2-results.json).

## What ran

- Selection: [selection.json](selection.json), frozen before the run. Korean edition at `cde2cbd`: the six c′ policy cases II-S26 to II-S31 and two reused cases, II-S08 (denied model) and II-S21 (preference is not evidence). One run per case per agent.
- Subjects: Claude Code 2.1.302 `claude-opus-5-5` (medium), Codex CLI 0.163.0 `gpt-6-astra` (medium). Graders as calibrated in [the grader calibration](../2026-10-31-grader-calibration/README.md) (132/132). Subject bundles had no answer keys; no subject changed its project.

| Case | Claude | Codex |
| --- | --- | --- |
| II-S26 Small, empty capability records | FAIL | FAIL |
| II-S27 explicit DENIED / stale / incomplete record | PASS | PASS |
| II-S28 unknown model identity | FAIL | FAIL |
| II-S29 routine testing versus a separate worker | PASS | INVALID |
| II-S30 stricter phase without evidence | PASS | FAIL |
| II-S31 Medium scoped assessment | FAIL | FAIL |
| II-S08 denied model | FAIL | INVALID |
| II-S21 preference is not evidence | PASS | FAIL |

## Why this is weak evidence

These are the author's reading of the private transcripts, not an independent regrade.

- **Runner defect (Codex):** in all eight Codex subject runs the read tool failed with `code-mode host is disabled`, because runner v2 disables the `code_mode*` features for Codex subjects as well as graders. Codex answered without reading the skills or rules. The runner's transcript check did not turn this into INVALID. All Codex results above are therefore not evidence about the method.
- **Case defect (II-S26, positive path):** the fixture describes "a complete Small Issue" without an Issue ID or tracker record, and the subject project's merge method is unset. Claude applied the new rule as written ("the routine Trivial/Small exception applies; proceed on the current model without capability evidence") but then stopped because no Issue was identified, which the entry guard requires. This repeats the fixture problem recorded in [the paired diagnostic follow-up](../2026-10-30-skill-comparison/follow-up-design.md).
- **Remaining Claude misses** were stated-detail items: naming which identity information is needed (II-S28), stating the ranked-floor requirement for a scoped assessment (II-S31), and naming a qualified fallback after rejecting the denied model (II-S08). In each case the protective decision itself was correct.

## Related real run

A separate first-use run with the same candidate (`cde2cbd`) and an empty capability table completed the README's first Small task end to end with Codex: claim, failing regression test first, fix, module tests, full suite, merge, `[PRODUCT COMPLETE]`, release and undo ([first-use record](../2026-10-31-first-use/README.md)). That is the positive-path observation this check could not provide.

## Next run needs

Fix the runner so Codex subjects keep their file-reading tools and any tool failure makes the run INVALID, then recalibrate (the runner hash is part of the calibration identity). Give the positive-path cases an Issue ID and tracker record, and set the merge method through `project_overrides`. Freeze that as a new selection; do not merge its results with these.
