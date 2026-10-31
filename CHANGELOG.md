# Changelog

## Unreleased

- c′ checks: a Codex first-use run on candidate `cde2cbd` with an empty capability table completed the first Small task end to end ([first-use record](docs/eval-results/2026-10-31-first-use/README.md)). A runner v2 behavior check of II-S26 to II-S31, II-S08 and II-S21 scored 5 PASS / 9 FAIL / 2 INVALID with no `must_not` violation, but every Codex subject run failed to read files (`code-mode host is disabled`) and the positive-path case lacked an Issue ID, so it is weak evidence ([record](docs/eval-results/2026-10-31-routing-cprime/README.md)). The runner fix and a new frozen run are pending.
- Policy relaxation c′, approved by the repository owner on 2026-10-31: the routine Trivial/Small current/manual lifecycle no longer requires positive capability evidence; other current/manual routes require fresh host evidence or a human-confirmed scoped assessment citing observed results. This is a limited policy relaxation, not a meaning-preserving fix. Canonical/P denies, explicit DENIED and incomplete/stale record handling, automatic switch/delegation/fallback PASS, separate reviewer sessions and identical-model inheritance, Large Review B human selection and its existing optional rules, the frontier default ban, and core.md human judgment remain unchanged. Six policy-regression specifications are added in both editions; behavior checks follow and are not yet executed results.
- First-use runs ([record](docs/eval-results/2026-10-31-first-use/README.md)): with the published preview.6 tag, a Codex run installed, committed and undid the installation once `.agents/` was made writable, then stopped at implementation entry because no fresh current-model capability evidence existed. An earlier Claude agent run finished the first task by treating the host-reported model as enough. This observation led to the c′ decision above; the READMEs also explain Codex's read-only `.agents/` and `.git`.
- Behavior runner v2 (`tests/run_behavior_evals_v2.py`, 23 new tests, implemented by Codex `gpt-6-astra`/high): clean subject bundles without answer keys, read-only runs with full file inventories, per-case project overrides, pinned models, strict grader output, real provenance, and a calibration gate. Grader calibration on 11 synthetic answers agreed on 132 of 132 items for both graders ([record](docs/eval-results/2026-10-31-grader-calibration/README.md)). No subject run yet. The old runners are unchanged.
- Evaluation records: the 2026-10-30 baseline and the 2026-10-31 tracker-neutral check ran with the answer-key files (`workflow/skills/*/evals/cases.json`) readable inside each subject project, because `tests/run_behavior_evals.py` copied the whole bundle. Access was not blocked or logged. Both records and the README status now say so; their grades are unchanged and are no longer presented as clean behavior evidence. The paired diagnostic removed the files and is unaffected.

## 1.0.0-preview.6 — 2026-10-31

Follows preview.5 (`ee5c60a246a95218e0f429681036fa9bd4bd1e03`). Earlier tags are unchanged.

First experience (no rule change):

- Both READMEs are rewritten around what a visitor needs first: the value, how depth scales by grade, two illustrative transcripts, a paste-in installation prompt, the expected `check`/`check-evals` output, the list of added files, how to undo the installation, the first task and when it counts as done. The verification history moves to this changelog; a short status section keeps the limits and links the evaluation records.
- Both installation guides target preview.6, and their first paragraph points to the guide inside each earlier tag instead of listing earlier tags.

Tracker-neutral W (meaning unchanged for both existing adapters):

- `workflow/README.md` defines W's terms (Issue, comment, field values in label notation, assignee, PR, closing reference) as tracker-neutral; the declared tracker method decides syntax and API.
- GitHub-only mechanics move from W to `tracker/github.md`: labels in the creation request, removing and adding a `priority:*` label, the Issue-number order, `Closes #N` syntax and the numeric `product-complete:` JSON. `tracker/local-docs.md` gains the matching rows (creation write, meta rewrite, and the Issue-number order as the existing `<ID>` mapping). W now says "set both values at creation if the method allows it", "replace the value and re-read", "the lower Issue number in the declared method's ID order" and "add the closing reference". Markers, the `Meta`/`Records` headings, the installer's `github | local-docs` choices and Epic's grade exception are unchanged. This does not add support for other trackers.
- The pinned Korean `completion.md` guard is proven unchanged except for the one closing-reference sentence (the test reverts exactly that sentence and compares the pinned hash). New `tests/test_tracker_neutral.py` keeps GitHub-only phrases out of W outside `tracker/` and checks that both adapters map the moved operations.

Skill and evaluation clarity (carried from the unreleased 721e086 change and corrected):

- II-S02: both editions restate the existing owning-module/test-class-first rule at the implementation step. It now applies to each *verification-affecting* changed file, matching `verification.md`; the 721e086 wording ("changed files") was broader than its source. The English edition also states that the scope follows that source.
- FI-S02: the fixture supplies the synthetic failing command and its result. New FI-S02b covers a missing command name and log; the agent must not invent them. Both editions clarify the incomplete-status report at the finishing step.
- A post-hoc paired diagnostic (`docs/eval-results/2026-10-30-skill-comparison/`, Korean, Claude `claude-opus-5-5`/medium as subject, Codex `gpt-6-astra`/medium as grader, 3 cases × 2 arms × 3 runs) graded 16 answers: 11 PASS, 5 FAIL, 2 pre-inference authentication INVALIDs kept without retry. No overall improvement was observed; II-S02 failed in every valid run, and its fixture lacked an Issue identity and full paths, so it does not establish a skill regression either. It evaluated the 721e086 wording, not the final wording or the English edition. Known runner limits: the grader model and effort are fixed in code, and resuming does not re-hash the generated grader model and instruction files; the recorded run used the configured values.
- Case notes in both editions record that diagnostic instead of saying the revised cases are unrun.

Validation: (2026-10-31, Windows, Python 3.12.2) on the reviewed candidate `277cfc58a5523f4bfe02c06fe67864d852ae897e`: all 65 executable tests passed; both 66-file bundle manifests matched; `git diff --check` passed; a `git archive` of the candidate installed in disposable projects for both editions with `local-docs` and `github` passed `init`, `render --source-commit`, `check` and `check-evals` (77 cases); relative links and anchors in both READMEs and guides resolved. The release commit after it changes only these validation lines in the READMEs and this changelog.

- Independent review: a fresh Codex session (`gpt-6-astra`, reasoning high, read-only, no conversation history) reviewed `ee5c60a..0327cb5`: no P1, five P2, two P3. All were fixed in `249176c`; a narrow reconfirmation found one partial fix and two new wording issues, fixed in `277cfc5` and reconfirmed with no remaining finding. The reviewer did not run the write-heavy installer tests; the served model identity was not independently verified.
- First-use runs from the README at `d7a2b27` with prepared human answers, in disposable repositories with a local bare remote: a fresh Claude Code agent installed the English edition, completed a Small task (claim, module tests first, full suite, merge, `[PRODUCT COMPLETE]`, release) and reverted the installation. A Codex run installed the Korean edition (`check` OK, 77 cases) but its sandbox denied writes to `.git`, so it stopped before the task. Their README findings (empty `ls-remote`, example values versus human decisions, local-docs folders, undo after push) are fixed in this release.
- Bounded behavior check: [record](docs/eval-results/2026-10-31-tracker-neutral/README.md), 4 PASS / 6 FAIL, no failure traced to the wording change, weak evidence.
- Open points from the first-use run, not changed in this release: no record tag for the observation start record in local-docs, module ownership of a top-level `tests/` folder, whether `merge` allows a fast-forward, when acceptance-criteria checkboxes are ticked, what counts as fresh capability evidence for the current model, and CRLF product files in lanes under `core.autocrlf=true`. The behavior runner's "shell commands cannot be run" text makes Codex skip reading files, and its example project conflicts with FI-S03/FI-S20.
- Not run: POSIX execution, live GitHub tracker operations, effect on outcomes, rework or cost.

## 1.0.0-preview.5 — 2026-10-30

Packages the candidate from `110d943c6db638d72bbafbbdc2bad4037e66b45c` on `v1-preview`, following preview.4 (`5760ac66b2a4c943360a56c22892fe35e1a076db`). This packaging step changes release documentation and records the evaluation limitations; both bundles and earlier tags are unchanged. `methodology/` (English M) is unchanged.

- Independent translation review (2026-10-30): gpt-6-astra (reasoning medium) compared the entire English edition against the Korean edition in five groups. It reported 14 findings (2 P1, 10 P2, 2 P3): 11 accepted, 2 partially accepted and 1 rejected. Partial acceptance: the README upgrade sentence was corrected, but the finding was treated as P2 because the sentence already existed in preview.4; the Methodology-only copy section was retained as existing content carried over from the preview.4 English guide, with its provenance stated and a pointer added in the Korean guide. The proposed `cross-agent` → `cross-tool` change was rejected to follow the source term `Cross-agent behavior eval` and the preview.4 English README. The finishing-issues cleanup exception was clarified in both editions; its ambiguity originated in the Korean plain-language rewording.

Execution profile (meaning change, opt-in; defaults keep preview.4 behavior):

- `review.large_mode: dual | single` — `single` replaces the Large AS-IS/PLAN Review A + Blind Audit B with one independent review in a separate session that also covers Review B's questions, uses the same four severities and keeps the blocker-0 progress condition. Blind isolation, the human's B selection and reconciliation do not apply in `single`.
- `review.blind_reviewer_selection: required | optional` — with `optional`, when no human has chosen, an agent may choose the Review B reviewer under the automatic-candidate rules (fresh role qualification PASS, `strong + high` floor, separate from the author and Review A, no `frontier` without escalation evidence) and records that it did. A human's choice is still never replaced automatically.
- `sdd.medium_artifacts: full | condensed` — `condensed` writes a new Medium SDD as one `README.md` with `## AS-IS`, `## PLAN`, `## Implementation specification`; the required content of each part is unchanged, and re-grading to Large splits it into the four documents before the AS-IS review.
- None of the values reduces M's human-judgment requirements, automatic grade escalation, required verification, the CODE Review or human judgment on Large merges. Changes apply to newly started reviews and SDDs. Owners: `design-review.md` (new section "Large design review mode"), `sdd-artifacts.md` (new section "Medium condensed layout"), `execution-routing.md`; project template `sdd-workflow.md` gains an "Execution profile" table.
- The installer rejects values outside the choices, non-string values and unknown keys in `review` and `sdd` (a misspelled key would otherwise silently keep the default), before writing anything.
- `design-review.md` is a hash-pinned guard in the structure tests. The change is additive only; the test now proves that removing exactly the added section, index row and sentence reproduces the earlier pinned bytes, instead of re-pinning the file.

Readability (Korean edition):

- New `workflow/glossary.md` (both editions), linked from the workflow README and each skill. It explains terms and adds no rules.
- The four `SKILL.md` bodies were reworded in plain Korean. Headings, `description`, literal markers, stop strings, paths and the order and conditions of every step are unchanged; skill headings referenced by other documents keep their anchors.
- One wording fix in `issue-writing-guide.md` (a pointer said "below" for a section above).

English edition:

- New full bundle `adaptive-sdd/` at the repository root with the same file set as `ko/adaptive-sdd/`; its `methodology/` is byte-identical to the root `methodology/`. Workflow, templates, eval cases and both guides (`docs/customization.md` now covers the full installation, with a methodology-only section; `docs/sdd-reading-audit.md`) are translated. The English text is canonical.
- The translation was produced by the coordinating agent and translation subagents with a fixed heading map and shared term list, then checked mechanically (no Korean text left, same heading structure, same template-token sequence, same case IDs and item counts, all installed links and anchors resolve). It then had one independent agent translation review (recorded above); it has not had an independent human review.
- The installer is byte-identical in both bundles. Edition wording (skill entry descriptions, marker note) moved to each bundle's `templates/strings.json`, which the installer validates. Marked blocks written by either edition are recognized, so switching editions re-renders instead of failing; look-alike or duplicated markers are still rejected. Korean generated files are byte-identical to preview.4 except `sdd-workflow.md`.
- `tools/review_snapshot.py` accepts the English tracker headings `Meta` / `Records` as well as the Korean ones; a document with headings of both editions is rejected.

Evaluation:

- First executed cross-agent behavior run of 12 pre-selected Korean cases × Claude Code and Codex × 3 runs, cross-graded; runner `tests/run_behavior_evals.py`; record in `docs/eval-results/2026-10-30/`. 71 valid runs: Claude Code 21 PASS / 14 FAIL / 1 INVALID, Codex 22 PASS / 14 FAIL. A usage limit invalidated 65 first-attempt runs; each was retried once (31 reruns, 34 regrades of saved answers) as skill-evals.md allows. This is a baseline, not evidence of effect.
- It found one case defect: `PD-S06` required `BLOCKED: origin/main fetch failed`, while the skill says `BLOCKED: declared base fetch failed`; all six FAILs of that case came from the stale case. The recorded results are unchanged; the case is corrected in both editions.
- Known limitations: `II-S02` missed the explicit first-targeted-verification requirement in all three Claude runs. `FI-S02` requires naming a failing command but supplies neither its name nor a failure log; this is an evaluation-input limitation, not established evidence of a skill defect. Raw answers are unavailable for a grading audit. Skill changes and case repair are deferred to a later version; existing results remain unchanged. See the source comparison in the evaluation record.
- Six execution-profile policy-regression cases (`II-K01`–`K06` and their English counterparts) were added; they are expected-behavior specifications and were not executed.

Release-commit validation (2026-10-30, Windows, Python 3.14.7): all 53 executable tests passed, both bundle manifests (66 files each) matched, and both editions passed `init`, `render`, `check` and `check-evals` (76 cases) in disposable projects. The initial sandbox run hit Windows temporary-directory locks (WinError 32) and a Git/MSYS access denial; the full suite was rerun outside the sandbox. Actual POSIX execution, live remote/host integration and an independent review of this change remain undone.

## 1.0.0-preview.4 — 2026-10-30

Packages the M/W/P correction from `6d37203f23d9fbe640b93c57930e3d3164ebfd76`. Only release documentation changes in this packaging step; the reviewed and tested bundle is unchanged. Earlier preview tags are preserved.

- Validation (2026-10-30): 36 Windows tests passed, including default/external entry-path resolution, existing connection and tamper checks, hand-edit protection, cross-host rendering and policy preservation. Original policy fixture hashes remain unchanged; only the renamed project-document path prefix is normalized for that comparison.
- Independent read-only review requested as `gpt-6.1-sol/high` found no actionable issue in the change against `bd3dd97`; manifest bytes and paths were independently checked. Served model identity and model behavior were not independently verified. Real consumer deployment and actual POSIX execution remain unverified.

- Retains M/W/P ownership and treats external installation solely as the `--harness-root` storage option. Removes S as a required workflow/Skill role. Generated entries and project documents now declare concrete bundle paths; fixed workflow documents reference M/W and the adjacent P-owned project documents.
- Preserves the connection schema, CLI option, checkout binding, integrity checks and hand-edit protection. Existing installations must explicitly adopt the new bundle and render/check; previous tags are unchanged.

## 1.0.0-preview.3 — 2026-10-30

Packages the changes since preview.2 as a new pre-release. The README and both installation guides identify preview.3, resolve the annotated tag to its full commit SHA, and keep the archive, guide and recorded pin aligned. The methodology, workflow, installer and bundle manifest are unchanged from integration commit `01ca9a69bcb6a6267b4b4c703c0562ed878f362f`; earlier validation and independent-review scopes below remain limited to their stated revisions and changes.

Preview synchronization (2026-10-30):

- Integrates the outstanding guide, README, changelog and observation-document corrections with merged public PRs #1–#3. The installation guides now pin the archive and matching guide to the same reviewed commit and distinguish post-preview.2 changes from the immutable `v1.0.0-preview.2` tag. Fixes both README links to the split Epic contract and the guides' references to relocated Epic, entry and plan-change policies.
- Clarifies revision-specific validation and moves the third feedback pass and its review history into the current preview section. Earlier test and review scopes remain historical evidence.
- Korean workflow meaning change: required verification remains mandatory; valid evidence for the same candidate and verification inputs can be reused. Keep detailed evidence at one source and reference its results, gaps and findings from reviews, SUMMARY and Epic records. Add tools or evidence files only when required evidence is missing from existing sources. The bundle manifest is regenerated; this Korean workflow still has no English edition.
- Validation: all 35 existing executable tests passed on Windows with Python 3.14.7. Both methodology manifests and all 64 bundle files matched. A ZIP of the integration candidate passed init/render/check/check-evals in disposable local-docs and GitHub-adapter installations; 70 cases across four skills passed structure checks. No live tracker operation, actual POSIX execution, model behavior evaluation or efficacy measurement was run.
- Independent integration review: a separate same-provider subagent requested as `gpt-6.1-sol/high` reviewed the seven-file integration diff against `5a81d647771cb56fcf1f1d84e94d580f2ca2d963`. It independently checked original-change preservation, guide/pin consistency, evidence-reuse semantics, links and exact manifest bytes. One P3 finding about relocated guide references was corrected and narrowly reconfirmed; no unresolved finding remains in that scope. This read-only review does not independently attest the implementing agent's test executions or review the entire cumulative workflow. The served model identity was not independently verified.
- The preview.2 tag remains unchanged. Preview.3 is a separate annotated tag and GitHub pre-release.

Selective reading and artifact layout (Korean workflow only; English workflow remains pending):

- Splits grade, entry, issue, Epic, completion, AS-IS, TO-BE, execution spec, and plan corrections into directly addressable files. Skills bypass the small index; rule owners, human boundaries, review independence, and verification gates remain intact.
- For new Medium/Large work, the existing README carries the human AS-IS view and `01-as-is.md` carries detailed evidence. `02-to-be.md` and change plans retain their human/agent roles. Issue metadata is referenced rather than maintained twice; no extra required artifact or approval is added. AS-IS review includes both views at the same candidate. Existing work is not migrated automatically.
- Adds optional artifact templates, pinned-manifest coverage, preservation and installation tests, ten synthetic behavior cases, and a reproducible static cost comparison. Model behavior and total host input/output tokens have not been measured. See [analysis and limitations](ko/docs/sdd-reading-audit.md).
- Clarifies relevant README inputs for Medium and separate implementation contexts without expanding Blind Audit inputs. Change plans reference Decision/AC owners while retaining unique fixture expectations; current contracts, conditional investigation history, and progress records remain distinct.

Meaning change in the Korean workflow (English workflow edition still pending):

- Uses four execution grades: Trivial, Small, Medium, Large. Epic becomes an optional management type for separately tracked issues; a single Large issue remains valid. New packages/modules no longer force an Epic or decomposition.
- Removes the mandatory decomposition publication and Review A/B gate. Unresolved questions alone do not block child investigation; decisions are dependencies of the later steps that need them.
- Assigns shared-change verification, consumer compatibility, and transition effects to an owning execution issue. Reuses applicable upstream analysis without waiving required current-target reviews or verification.
- Keeps orchestration within authorized scope, human control over goal/acceptance reductions and prior decisions, and evidence for overall completion. Documents and generated tracker guidance distinguish management-only closure from implementation/PR closure.
- Rejects `grade_mapping.min_grade: Epic` rather than silently converting it. Documents migration and retains the legacy `human_judgment.large_epic_merge` setting key without automatically waiving existing human permissions.
- Adds seven fictional policy-regression cases. They are expected behavior specifications, not evidence of executed model behavior or operational improvement. No published tag is changed.

Workflow organization in the same preview branch:

- The earlier organization kept classification, entry conditions, and Epic orchestration in `sdd-workflow.md`; the selective-reading change above now separates those owners as well. SDD artifact details, design reviews, verification, observations, and optional token diagnostics have explicit read conditions.
- Makes model routing/qualification and execution/result/review packet contracts separate owners. Execution and finishing skills call the relevant contract at the point of use; same-run valid evidence is reused. Packet serialization and size measurement belong to skill evaluation, outside routine execution inputs.
- Clarifies that read-only investigation does not require an edit claim or a new lane, and that overlapping reads are not write conflicts. Product edits retain claim, grade, access, and dependency requirements.
- Preserves current/manual model eligibility checks even without a model switch. Aligns packet evidence with existing input-based verification reuse: keep the actual execution identity and prove unchanged command inputs against the current candidate; missing or mismatched evidence remains stale.
- Adds an installed Markdown target/anchor regression check and two fictional verification-reuse cases. The cases specify intended behavior; they are not executed model evaluations.

External-review follow-up:

- Requires a lane and claim before the first execution-issue repository file write, including SDD and tests, while preserving read-only investigation, tracker management, and Epic-management exceptions. Applies current-phase prerequisites so claiming an AS-IS writing task does not require its future design reviews.
- Places final CODE Review after business synchronization and SDD/link/status cleanup. Earlier CODE Review remains historical evidence when the repository candidate changes; unchanged verification inputs and an unchanged review candidate can reuse their valid evidence. Does not add a default second review or build run.
- Prepares valid required verification evidence before final CODE Review, including validators invalidated by closure edits. Review corrections refresh the candidate and affected verification before its review; unchanged verification inputs do not trigger repeated runs. Extends FI-S12 to specify this order without adding a new case or gate.
- Adds two fictional regression specifications for first SDD write ownership and the final review target after closure edits. These remain document-level expected behavior specifications.

First feedback implementation pass (meaning changes):

- Clarifies requirement and confirmed-decision recording in both English and Korean `core.md`. Task-relevant requirements delivered through conversation can be recorded with provenance; investigation requests and proposals do not become decisions. Conversation-log collection and protected-content restrictions remain. Updates the Korean issue-writing template and skill consistently.
- Defines implementation-time plan correction and in-progress policy transitions, preserving prior revisions and replacing current instructions explicitly. Review and verification are refreshed by actual impact. Verification-only strengthening with unchanged product contracts and audit assumptions uses A reconfirmation; B is called again only when its finding evidence is affected, without automatically starting a new blind audit.
- Prevents stale installer tags: a changed source commit without a supplied tag clears the old tag. Same-source renders retain it; `--clear-source-tag` repairs an existing incorrect tag. Supplying a tag requires a commit before any output is written. Remote tag correspondence is still the caller's responsibility.
- Preserves active consumers of SDD contracts before cleanup, using accessible immutable references or retained documents with a cleanup owner and release condition. Confirmed retention does not itself block product completion. Missing references or unowned retention are not accepted as cleanup complete.
- Adds seven original fictional policy-regression specifications and four executable installer regression tests. Korean workflow/template/tool editions remain pending in English; the shared methodology clarification and upgrade guidance are synchronized.

Checked locally after this pass: ten installer regression tests, including both tracker adapters, source-tag upgrade/repair/rejection before writes, and installed workflow/project links; integrity of the 50-file copy and both methodology manifests; structural checks for 48 cases / four skills in disposable installations. The installer's built-in skill/frontmatter checks passed. The separate skill-creator validator could not run because PyYAML is unavailable. New behavior cases are specifications only: no model behavior evaluation or independent review was run for this pass. Operational outcomes and actual token use have not been measured. Earlier source review and scenario walkthroughs apply to earlier revisions, not this pass.

Second feedback implementation pass (Korean workflow; English workflow edition pending):

- Bounds AS-IS investigation to evidence that affects decisions: baseline identity and operational use, relevant introduction/disablement history, exact dependency behavior, and external consumers. Separates observed facts from intent and frequency guesses; conflicts stop dependent work without stopping unrelated investigation.
- Separates review PASS from readiness of the next action. Unresolved questions carry an owner and the step that needs their answer, including questions not found by reviewers. Shared questions are coordinated once and current child instructions are updated after decisions.
- Connects declared project conventions and documented exceptions to change plans, execution packets, and contract review. Does not turn personal style preferences or absent conventions into new requirements.
- Prepares blind inputs separately from review records, preserves substantive contracts and unresolved facts, and records source identity, selected ranges, access checks, and enforced versus instruction-only isolation. Exposure invalidates the initial blind run; reconfirmation remains distinct.
- Adds the optional standard-library `review_snapshot.py` helper for exact-commit UTF-8 artifacts and local-docs bodies. It exports source/output hashes and line selections, rejects mutable refs and unsafe paths, and checks source correspondence, altered bytes, and unexpected files. It does not prove remote publication, semantic redaction, or host isolation.

Checked after the second pass: all 17 executable tests passed, including seven snapshot tests with Korean CRLF text, fenced heading examples, hidden metadata/records, changed worktree versus exact commit, tampering, and a bare-source CLI run. The sandbox blocked Git's shell during the initial local bare-clone fixture setup; the full suite then passed with approved execution permissions. Installed links/frontmatter, both tracker adapters, the 51-file bundle, both methodology manifests, and structure of 54 cases / four skills were checked. Six new behavior specifications were added; model behavior evaluation and independent review remain unrun. Actual reviewer-account access and end-to-end blind isolation are not claimed from synthetic tool tests. The separate skill-creator validator remains unavailable without PyYAML.

Third feedback implementation pass (meaning changes):

- Adds optional external harness installation with checkout-bound connection, lock, manifest and generated-entry checks. One harness root serves one checkout; migration preserves hand edits and does not remove old copies.
- Declares code remote/base/merge target separately from review publication repository/remote/branch, and external/child ID rules. Existing installations keep defaults; no service adapter or Git authorization is inferred.
- Adds manual verification ownership/evidence and persistent/temporary/no-new-test policy, preserving required checks, temporary evidence and current-target correspondence.
- Adds conversation/convention references, role preferences and capability/qualification references. Inherited current/manual reviewers still need verified identity/reasoning; preferences do not bypass qualification or human Review B selection.
- Aligns generated AGENTS privacy guidance with the first-pass permission to record minimal requirements and explicit decisions. Normalizes generated marker-block boundaries for repeatable rendering.
- English/Korean customization guides describe these settings and limitations. Full English workflow/templates/tools remain pending. Synthetic tests and behavioral specifications do not establish live-host or operational efficacy.

Context-inheriting auxiliary review follow-up (not an independent review):

- Resolves three P2 findings: completion uses the declared merge target; explicit required device/runtime checks remain mandatory without adding a universal QA gate; Git and publication names share validation before writes. Adds invalid-name regression inputs and two fictional behavior specifications.
- A context-inheriting auxiliary reviewer confirmed all three fixes with no new actionable finding in the corrected scope. Installer regressions passed again; live publication and host behavior remain unverified.

Context-isolated Astra high review:

- A fresh gpt-6-astra/high reviewer received no conversation history or previous findings/test results. It inspected the cumulative working-tree changes independently; earlier review statements were excluded as evidence.
- Fixes two P2 findings: external default check-evals now uses explicit harness/product roots, and generated external commands quote paths literally for the named PowerShell/POSIX shell.
- Fixes a follow-up P2 regression by keeping in-repository output independent of the generating OS. Adds actual Windows-shell execution tests for special-character paths and a win32-render/linux-check branch test.
- The reviewer confirmed all findings resolved. Initial full suite: 23 tests passed; final changed installer suite: 18 tests passed. Actual POSIX execution, live remote operations and model behavior evaluations remain unverified.

## 1.0.0-preview.2

Adds executable procedures, skills, an eval structure, and an installer to the Korean edition, and fixes three human-judgment gaps in the common methodology for both editions.

- `methodology/core.md` (both editions): human-judgment requirements cannot be waived by host or project rules; lists the minimum questions that need human judgment; a delegation counts as a human decision only when a human records it with its scope, date, and confirmer, and the Agent never creates, extends, or finalizes one; when a human cannot be asked, the dependent work stops and the question is recorded as unresolved; the adapter gains a slot for the work-record reference location and how to find earlier records.
- `methodology/adaptation.md` (both editions): adds `awaiting human confirmation` to the re-evaluation dispositions.
- `methodology/supports/ordered-changes.md` (both editions): progress that depends on human judgment stops and asks a human under `core.md`.
- `docs/customization.md`: adds the new adapter slot and the delegation rule, and points to preview.2.
- Korean edition: `ko/methodology/` is replaced by the full pinned copy `ko/adaptive-sdd/`:
  - `workflow/` — workflow procedures and four skills (organizing and creating work items, isolating work, design and implementation, verification and closing), extracted from procedures used in one product with product-specific parts moved out; tracker mappings for local documents and GitHub.
  - `workflow/process/skill-evals.md` and `workflow/skills/*/evals/` — eval kinds, grading, result records, 30 fictional seed cases, turning recorded incidents into diagnostic cases, and validity conditions for comparing and adopting a change.
  - `templates/` and `tools/install.py` — generate project documents, skill entry files for Claude Code and Codex, and marked blocks in `AGENTS.md`, `CLAUDE.md`, and `.gitattributes` from `project.json`; check the copy and generated files against their hashes.
  - `MANIFEST.json` — sha256 of every file in the copy.
- Known limitations: the local-documents tracker mapping replaces GitHub issues and pull requests only; git still needs a code remote named `origin`. Squash and rebase merges are confirmed from a recorded merge entry rather than from git ancestry. The guidance for re-evaluating observations is condensed until its skill ships, and no deterministic routing validator is included. Some workflow references point to project-document sections that the generated documents do not carry yet.
- Pending: the English edition of `workflow/`, `templates/`, `tools/`, and the installer guide. Until then the Korean edition is the only source for them. A skill for re-evaluating observations is also deferred.

Checked: manifest hashes, the installer's unit tests, one install rehearsal on Windows into a fictional project using a locally built archive, and one independent review whose should-fix findings were addressed before publication. Effect on outcomes has not been measured.

## 1.0.0-preview.1

First preview of the next-generation methodology, published on the `v1-preview` branch. `main` still carries v0.2.

- Adds `methodology/core.md`: a minimal workflow, human-judgment requirements, and work records and observation.
- Adds `methodology/adaptation.md`: choosing and re-evaluating supports from observed evidence.
- Adds `methodology/supports/ordered-changes.md`: the default ordered change list support.
- Adds `methodology/manifest.json`: sha256 of the three documents.
- Adds `docs/customization.md`: placing a pinned copy, filling the adapter, and instructing an Agent.
- Includes the Korean edition under `ko/` (README, methodology, guide). The separate Korean repository is retired, and the Korean v0.2 edition is no longer published. The English text at the root is canonical.
- Removes the v0.2 documents, starter, templates, examples, and assets from this branch. They remain on `main` and at tag `v0.2.0`.

This preview does not replace v0.2. Its effect has not been measured, and its structure may change before 1.0.

## Unreleased

_v0.2 line: unreleased changes on `main`, not part of this preview._

- Adds optional review-target identity and completion-evidence walkthroughs, with explicit comparison and retention limits.
- Adds full/correction review briefings and a draft human-executed verification handoff form.
- Clarifies TC expectation corrections, approved AC changes, administrative TC closure, and affected reruns without weakening required evidence or authorization.
- Keeps restricted-environment handoff DRAFT / OPTIONAL. The new examples are fictional; static checks are not operational validation.
- Updates the English source and Korean edition together; the Korean changelog records its matching English source revision.

## 0.2.0

Portable agent-runtime update based on repeated repository operation.

Adds:

- Trivial fast-track grade;
- progressive disclosure (`AGENTS.md` -> Skill -> conditional docs);
- portable-core versus project-local policy separation;
- bootstrap guidance and starter contracts;
- phase-aware review packets and finding classification;
- revision-bound Human approval;
- updated token/context efficiency guidance.

### Pre-merge hardening

- Clarifies separate Large AS-IS and PLAN independent review decisions.
- Defines reviewer independence and optional Blind Audit input/result boundaries.
- Connects ACs to actual verification results, revision/environment, and evidence.
- Separates design approval from final Human integration authorization.
- Clarifies bounded handoffs, write versus read scope, and context invalidation.
- Adds a developer execution guide and fictional Trivial/updated Large examples.
- Restores editable overview and detailed SVG diagrams aligned with the lifecycle.
- Adds public-content review guidance.
- Adds an **optional draft** for restricted-environment API/DB verification handoff; no connector, direct DB access, execution automation, or operational validation is claimed.

These are methodology/starter changes, not a claim of runtime enforcement or completed agent integration tests. Project-specific model routing, build workarounds, and universal Blind Audit remain outside the portable core.

## 0.1.0

Initial public working methodology: Issue-first execution, information-specific Source of Truth, risk grades, bounded AS-IS analysis, Verification Strategy, Trade-off Capture, grade-based review, conditional Device QA, token/context efficiency, and lifecycle cleanup.
