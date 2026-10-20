# Changelog

## 1.0 preview — unreleased

Meaning change in the Korean workflow (English workflow edition still pending):

- Uses four execution grades: Trivial, Small, Medium, Large. Epic becomes an optional management type for separately tracked issues; a single Large issue remains valid. New packages/modules no longer force an Epic or decomposition.
- Removes the mandatory decomposition publication and Review A/B gate. Unresolved questions alone do not block child investigation; decisions are dependencies of the later steps that need them.
- Assigns shared-change verification, consumer compatibility, and transition effects to an owning execution issue. Reuses applicable upstream analysis without waiving required current-target reviews or verification.
- Keeps orchestration within authorized scope, human control over goal/acceptance reductions and prior decisions, and evidence for overall completion. Documents and generated tracker guidance distinguish management-only closure from implementation/PR closure.
- Rejects `grade_mapping.min_grade: Epic` rather than silently converting it. Documents migration and retains the legacy `human_judgment.large_epic_merge` setting key without automatically waiving existing human permissions.
- Adds seven fictional policy-regression cases. They are expected behavior specifications, not evidence of executed model behavior or operational improvement. No published tag is changed.

Workflow organization in the same preview branch:

- Keeps classification, entry conditions, and Epic orchestration in `sdd-workflow.md`. Moves SDD artifact details, design reviews, verification, observations, and optional token diagnostics into dedicated process documents with explicit read conditions.
- Makes model routing/qualification and execution/result/review packet contracts separate owners. Execution and finishing skills call the relevant contract at the point of use; same-run valid evidence is reused. Packet serialization and size measurement belong to skill evaluation, outside routine execution inputs.
- Clarifies that read-only investigation does not require an edit claim or a new lane, and that overlapping reads are not write conflicts. Product edits retain claim, grade, access, and dependency requirements.
- Preserves current/manual model eligibility checks even without a model switch. Aligns packet evidence with existing input-based verification reuse: keep the actual execution identity and prove unchanged command inputs against the current candidate; missing or mismatched evidence remains stale.
- Adds an installed Markdown target/anchor regression check and two fictional verification-reuse cases. The cases specify intended behavior; they are not executed model evaluations.

Checked locally: six installer regression tests, including both tracker adapters, retained merge-setting values, legacy Epic rejection before output writes, and installed workflow/project links; integrity of the 50-file copy; structural checks for 39 cases / four skills in disposable installations. The installer's built-in skill/frontmatter checks passed. A separate source review and four scenario walkthroughs are document-level checks, not end-to-end model behavior evals. Operational outcomes and actual token use have not been measured.

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
