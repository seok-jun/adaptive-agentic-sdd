# Adaptive Agentic SDD — 1.0 preview

**English** | [한국어](ko/README.md)

> **Preview.** This branch (`v1-preview`) carries the 1.0 preview of the next-generation methodology. Its effect has not been measured, and its structure may change before 1.0. The v0.2 methodology remains on `main` and at tag [`v0.2.0`](https://github.com/seok-jun/adaptive-agentic-sdd/tree/v0.2.0).

## What this is

A common layer that a project copies, pins, and adjusts to itself.

- `methodology/core.md` — a minimal workflow, the human-judgment requirements, and how work records and observations are kept.
- `methodology/adaptation.md` — rules for choosing and re-evaluating supports based on observed evidence rather than model names or confidence.
- `methodology/supports/ordered-changes.md` — one default support: an ordered change list tied to requirements.
- `methodology/manifest.json` — sha256 of the three documents, used to check a copy.
- `docs/customization.md` — how to place the copy in a project, fill the adapter, and instruct an Agent.
- `ko/` — the Korean edition. The English text at the root is canonical.

### Korean edition only in this preview

`ko/adaptive-sdd/` is a full pinned copy that adds, on top of the methodology:

- **Workflow procedures and four skills** — organizing work items (including creating them), isolating work in a worktree, design and implementation, and verification and closing. They were extracted from procedures refined over a long period in one product, with product-specific parts moved out.
- **An eval structure** — static checks, behavior cases, cross-agent comparison, grading and result records, fictional seed and policy-regression cases, and rules for turning a recorded incident into a diagnostic case. New policy cases distinguish expected behavior from executed results.
- **An improvement loop** — closing records → re-evaluation under `adaptation.md` → incident cases → a comparison whose scope a human approves → adoption decided and recorded by a human.
- **An installer** — `tools/install.py` (Python 3.8+, standard library only) generates the project-dependent files (project documents, skill entry files for Claude Code and Codex, marked blocks in `AGENTS.md`, `CLAUDE.md`, and `.gitattributes`) from the project's `project.json`, and checks the copy and generated files against their hashes.

The English edition of these parts is pending and planned for a later preview. Until then, the Korean edition is the only source for them, and English-only projects use the methodology documents above.

The unreleased Korean workflow uses four execution grades (Trivial, Small, Medium, Large). Epic is an optional grouping for independently tracked issues, with no separate decomposition review gate. A single Large issue remains valid; shared-change verification, human-decision boundaries, and evidence for the overall outcome remain required. See the [Korean workflow](ko/adaptive-sdd/workflow/process/sdd/epic.md#epic-관리-단위) for the policy; its English edition is still pending.

## What this is not

- **Not a replacement for v0.2.** It does not carry over v0.2's documents, starter, or templates. v0.2 remains on `main`.
- **Not a verified result.** No effect on outcomes, rework, or cost has been measured. The procedures and skills were used in one product; that experience does not establish the effectiveness of this generalized preview. Checks and reviews have the revision-specific scope below.
- **Not an enforcement mechanism.** It is guidance for agents and people; it is not a security boundary or an agent runner.

## Verification scope

- **Published `v1.0.0-preview.2`:** manifest checks, installer unit tests, one Windows installation rehearsal using a locally built archive and a fictional project, and one independent review were recorded for that release. They do not validate subsequent changes.
- **Unreleased commit `068618bdda2f8d0571da3099f5e132e4ff17ff1e`, checked on 2026-10-27:** all 25 executable tests passed on Windows with Python 3.14.7; both methodology manifests and the 51-file bundle manifest matched. A ZIP built from that commit passed `init`, `render`, `check`, and `check-evals` in a disposable project. The 60 cases across four skills passed structural checks; they were not executed as model behavior evaluations.
- **Integration candidate, checked on 2026-10-30:** based on `5a81d647771cb56fcf1f1d84e94d580f2ca2d963` plus the guide, verification-scope, changelog, observation-evidence and manifest corrections in this change. All 35 executable tests passed on Windows with Python 3.14.7. Both methodology manifests and the 64-file bundle manifest matched. A ZIP of the candidate passed `init`, `render`, `check`, and `check-evals` in disposable local-docs and GitHub-adapter projects; 70 cases across four skills passed structural checks. No live GitHub tracker operations or model behavior evaluations were run.
- **Review and remaining limits:** [CHANGELOG.md](CHANGELOG.md) records the scope and timing of earlier reviews. The checks above are not a new independent review. Actual POSIX execution, live remote/host integration, model behavior, and effects on outcomes, rework, or cost remain unverified.

## Getting started

- **English (methodology only):** read [docs/customization.md](docs/customization.md). Copy `methodology/` and `LICENSE` byte for byte, check the hashes, pin line endings, add a few lines to the entry file, and let an Agent draft the adapter; a human decides the human-judgment points.
- **Korean (full copy with installer):** read [ko/docs/customization.md](ko/docs/customization.md). Copy `ko/adaptive-sdd/` to `.adaptive-sdd/`, run `install.py init`, fill `project.json` (an Agent drafts, a human decides), then run `install.py render` and `install.py check`.

These guides cover the unreleased branch and use a reviewed commit SHA. For a published tag, use the guide from that same tag; `v1.0.0-preview.2` does not include the external installer features described on this branch.

## Versions

- Preview tags: `v1.0.0-preview.N`. Published tags are never moved; fixes come as new tags.
- Pin a copy by tag, commit SHA, and manifest hash, not by tag name alone.
- Upgrading replaces only the copy; project values, the adapter, and work records stay.

## License

[MIT](LICENSE)
