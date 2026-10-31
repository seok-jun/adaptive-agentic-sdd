# Paired diagnostic

Status: COMPLETE. Subject calls: 18/18; grader calls: 16/18.

| Case | Before PASS/FAIL/INVALID | After PASS/FAIL/INVALID |
| --- | --- | --- |
| II-S02-small-one-module | 0/3/0 | 0/2/1 |
| FI-S02-required-check-failing | 3/0/0 | 3/0/0 |
| FI-S02b-required-check-failure-evidence-missing | 2/0/1 | 3/0/0 |

Per-repetition outcomes and exact per-item misses are in `paired-results.json`.

Post-hoc diagnostic on three motivating cases, three repetitions per arm. Action plans do not prove actual command ordering. This is not a broad regression or adoption evaluation. A 3/3 versus 3/3 result is no observed improvement (ceiling). INVALID is not FAIL. No automatic retry, release, merge, or adoption.

Instruction hashes record discovered user/ancestor CLAUDE.md files, not proof of complete prompt isolation. Restricted mode confines file tools to each project. Codex uses an empty grading directory, replacement grader instructions, disabled tools and per-transcript tool-use validation. CLI-returned model metadata is checked; provider-internal routing cannot be independently verified.

## Interpretation

**2026-10-31 subsequent evaluation-quality audit:** The original scores below are retained unchanged, but should not be interpreted as validated skill regressions. The II-S02 fixture does not identify an Issue or supply its authoritative record, while the installed workflow requires a specified Issue. Its allowed-path text also abbreviates the test path as `src/test`, whereas the rubric requires containment in `loan-service/**`. The grading instruction demands literal path matching without defining equivalent narrower path sets. Manual inspection of the private evidence raised a boundary-item false-negative concern and a precondition confound. This is an author audit, not an independent regrade. The earlier statement that the allowed-boundary behavior regressed is therefore not established. See [follow-up-design.md](follow-up-design.md). No original score or frozen fixture has been changed.

No overall PASS-rate improvement was observed. II-S02 remained FAIL in every valid run: before 0/3 PASS, after 0/2 PASS with one pre-inference authentication INVALID. Its targeted first-verification item improved from 0/3 met before to 2/2 met after, but the allowed-boundary item fell from 3/3 to 0/2. The claim item was met in 2/3 before and 1/2 after. No must_not item was violated in these valid runs. This is a mixed item-level observation, not evidence to adopt the change.

FI-S02 passed 3/3 in both arms: no observed improvement / ceiling. FI-S02b passed every valid answer (before 2/2 plus one authentication INVALID; after 3/3). Unequal valid sample counts must not be presented as a reliability gain.

The first two calls used unsuccessful authentication contexts and completed no inference. After user-authorized account switching and user-completed reauthentication, all 16 remaining samples ran under the default-home subscription account. Both earlier samples remain INVALID; none were replaced. Total: 18 subject CLI attempts, 16 successful subject inferences, 16 grader calls; PASS 11, FAIL 5, INVALID 2. No automatic retries, skill changes, merge, release or adoption decision occurred.

Final audit rechecked all 18 project inventories and the 16 successful subject/grader transcripts, exact rubric item correspondence and booleans, normalized-text answer/transcript hashes, configured grader model/effort, and frozen runner/selection hashes. The grader CLI JSONL does not independently attest the provider-side served model; its configured model/effort and transcript tool-use checks are the available evidence.

## All repetitions

| Case | Arm | Repetition 1 | Repetition 2 | Repetition 3 |
| --- | --- | --- | --- | --- |
| II-S02-small-one-module | before | FAIL | FAIL | FAIL |
| II-S02-small-one-module | after | INVALID | FAIL | FAIL |
| FI-S02-required-check-failing | before | PASS | PASS | PASS |
| FI-S02-required-check-failing | after | PASS | PASS | PASS |
| FI-S02b-required-check-failure-evidence-missing | before | PASS | PASS | INVALID |
| FI-S02b-required-check-failure-evidence-missing | after | PASS | PASS | PASS |
