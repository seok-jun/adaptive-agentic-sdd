# Changelog

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
