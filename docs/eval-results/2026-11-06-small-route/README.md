# Five-language routine-work trial — 2026-11-06

## Scope and result

Five synthetic one-module Small tasks used the improved English external workflow at `99cf49d12106afe31fdff69718bef5c74f45e835`. All five eventually completed implementation, required checks, authorized local merge, closure and claim release. An independent auditor cloned each local bare remote's final `main` and checked behavior, scope and completion identities.

First attempts completed **3/5**. Python stopped at Git's sandbox-account ownership check, and Go stopped because the existing toolchain location was inaccessible. Those original attempts and records were retained. After bounded environment fixes, the same cases ran in fresh sessions and completed. This is five cases with two additional task attempts, not five uninterrupted first-attempt successes. Infrastructure/configuration probes are separate from the five cases.

The task commands and file-change events showed **no observed agent-directed writes outside the authorized session areas** in the completed runs. A separate preflight using the same sandbox mode confirmed an allowed scratch write and rejection of a harmless sibling write. This is bounded sandbox evidence and log inspection, not a complete filesystem trace or proof against every escape.

## Configuration

- Requested model/reasoning for every subject: **`gpt-6.1-sol` / `high`**, explicitly passed to Codex CLI 0.163.0. The local model catalog advertised this combination. Actual provider-side served identity was not separately exposed or verified. No live Claude invocation was used for this trial.
- Native Windows workspace-write sandbox; approval policy never; default OS-temp allowances excluded; TMP/TEMP/TMPDIR and language cache/build outputs directed to per-task scratch. No sandbox disablement or denial bypass was used.
- Fresh CLI processes, no resumed model conversation, no model delegation or automatic fallback. Existing Codex app execution-bridge environment variables were omitted from these independent CLI processes; the initial bridge-launch failure was retained as infrastructure evidence.
- Python 3.12.2, Node.js 20.11.1, TypeScript 7.0.2, Java 21.0.11, Go 1.27.0. Dependencies/toolchains were provisioned before implementation; no subject performed network installation.
- Separate P, read-only external W, declared local-docs tracker, local bare code remote, exact W pin, product authority and required verification. P and workflow setup were prepared for the subjects; this does not measure unassisted first adoption.
- Single isolated clone/task branch per case, allowed product files restricted to one source and its test file, explicit local merge authority. No production or public GitHub tracker writes.
- The Git ownership fix trusted only exact disposable repository paths via a session-specific config. The Go fix copied the same installed toolchain into an accessible test-owned location and redirected caches. The original ownership/access failures were not erased.

## Cases and independent outcomes

Times are process wall time for the completed attempt only; they exclude setup and independent audit. The two stopped attempts are reported separately below.

| Language | Requirement | Completed attempt | Independent behavior and lifecycle |
| --- | --- | --- | --- |
| Python | Parse comma-separated tags, trim edges, discard empties, preserve order/duplicates/case | 315.8 s | PASS; whitespace/empty/duplicate/case inputs checked |
| JavaScript | Case-insensitive deduplication preserving first spelling, order, whitespace and input array | 315.2 s | PASS; mutation and empty-input checks included |
| TypeScript | Use fallback only for null/undefined, preserving empty string and strict typing | 268.4 s | PASS; strict compilation and separate runtime inputs checked |
| Java | Inclusive integer clamp, reject reversed bounds, avoid overflow | 326.0 s | PASS; MIN_VALUE/MAX_VALUE and equal bounds checked |
| Go | First complete Unicode code point, empty input, no grapheme-cluster expansion | 340.0 s | PASS; Korean, emoji and combining-sequence inputs checked |

The stopped Python attempt took 23.2 s; the stopped Go attempt took 171.4 s. They did not implement or merge unverified product work. A JavaScript record-print operation encountered a terminal encoding error; the persisted record remained intact and was re-read. Expected red regression tests before the fixes are not counted as new process incidents. Git home-ignore permission warnings were retained, without broadening permissions to suppress them.

For every final remote clone the audit confirmed:

- Required product tests and separately authored behavior checks passed.
- Changes relative to the product baseline stayed within the two allowed files.
- Selected W commit and checkout remained unchanged; the original P checkout was clean.
- CLAIM, IMPLEMENTATION SUMMARY, MERGED, CLOSED, PRODUCT COMPLETE and RELEASE markers existed; status was closed, owner none, and active claims empty.
- PRODUCT COMPLETE's merge SHA matched actual remote main and its implementation head was an ancestor of that merge.

## Procedure burden and boundary observations

The compact route explicitly allows start facts in CLAIM and closing updates without repeating the full SUMMARY. Each completed trial wrote **one SUMMARY entry**. Work records had **7, 8, 7, 7 and 8 entries**, including the retained Go environment failure/resumption. An earlier five-case Claude/Python exercise had 8–10 entries; three of those cases wrote two SUMMARY entries.

This is evidence that the new grouping can be used, not a controlled efficiency comparison. Model, language, task, sandbox, batching and environment all changed. Completed attempts still took about **4.5–5.7 minutes**, and records remain substantial. No productivity, cost or causal speed improvement is claimed.

Earlier trials had agent-created helpers in OS temp outside their declared roots. This trial combined explicit scratch scope with actual host write restrictions. The outcome cannot isolate the contribution of wording from sandbox enforcement or model behavior. The methodology and resolver do not themselves install or enforce an OS sandbox.

## Repository validation and evidence handling

- Final workflow candidate: 117 existing executable tests passed; both 70-file distribution manifests matched exact serialized bytes and source hashes; changed-document local link targets passed.
- Three new cases per edition specify scratch scope, compact entry and closure evidence. They are policy regression specifications, not new graded model-evaluation scores. Existing M files and high-risk review/verification rules were not edited.
- Local evidence retains invocation arguments, environment overrides, initial failed attempts, complete CLI output, work records, local Git histories, independent clones, behavior check outputs and completion-identity results. Raw host logs include local paths and are intentionally not copied into this public report. The summary was reconciled with those artifacts by the preparing agent; there was no separate blind grader.
- No Medium/Large, competing-claim race, native macOS/Linux, Korean-subject or live GitHub tracker lifecycle was exercised here. Passing the bounded outcome checks does not establish compliance with every instruction sentence.

The published `v1.0.0` tag remains unchanged. This record describes a subsequent improvement candidate, not a retroactive test of that immutable release.
