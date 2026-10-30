# Adaptive Agentic SDD — 1.0 preview.5 candidate (unreleased)

**English** | [한국어](ko/README.md)

> **Preview.** This branch is the candidate for `v1.0.0-preview.5`. The latest published release is `v1.0.0-preview.4` on the `v1-preview` branch; to use preview.4, take the files and guide from that tag. Its effect has not been measured, and its structure may change before 1.0. The English v0.2 methodology remains on `main` and at tag [`v0.2.0`](https://github.com/seok-jun/adaptive-agentic-sdd/tree/v0.2.0). The Korean v0.2 edition is no longer provided.

The preview.5 candidate adds:

- **Three execution-profile settings** — `review.large_mode` (dual or single Large design review), `review.blind_reviewer_selection` (whether a human must choose the Review B model) and `sdd.medium_artifacts` (four documents or one page for a Medium SDD). The defaults keep the earlier behavior; none of them reduces M's human-judgment requirements, automatic grade escalation, required verification, the CODE Review or human judgment on Large merges.
- **A glossary** (`adaptive-sdd/workflow/glossary.md`) and **plain-language rewording of the four skills** (Korean edition). The meaning, order and stop conditions of the rules are unchanged.
- **The full English edition** — `adaptive-sdd/` at the repository root. The installer is byte-identical in both editions; edition wording lives in each bundle's `templates/strings.json`.
- **A first executed behavior evaluation record** — `docs/eval-results/2026-10-30/`. See the verification scope below.

## What this is

A common layer that a project copies, pins, and adjusts to itself.

- `adaptive-sdd/` — the full pinned copy (English, canonical):
  - `methodology/` — `core.md` (a minimal workflow, the human-judgment requirements, and how work records and observations are kept), `adaptation.md` (rules for choosing and re-evaluating supports based on observed evidence rather than model names or confidence), `supports/ordered-changes.md` (the default support), `manifest.json`. Byte-identical to `methodology/` at the root.
  - `workflow/` — workflow procedures and four skills (organizing and creating work items, isolating work in a worktree, design and implementation, verification and closing), a [glossary](adaptive-sdd/workflow/glossary.md), an eval structure (static checks, behavior cases, cross-agent comparison, grading and result records, fictional seed and policy-regression cases, rules for turning a recorded incident into a diagnostic case) and work-tracking mappings (local documents, GitHub). The new policy cases distinguish expected behavior from execution results. They were extracted from procedures refined over a long period in one product, with product-specific parts moved out.
  - `templates/` — templates for project-dependent files and the edition wording (`strings.json`); the installer fills them from `project.json`.
  - `tools/install.py` — the installer (Python 3.8+, standard library only). It generates project documents, skill entry files for Claude Code and Codex, and marked blocks in `AGENTS.md`, `CLAUDE.md` and `.gitattributes`, and checks the copy and generated files against their hashes. It recognizes marked blocks written by the other edition.
  - `MANIFEST.json` — sha256 of every file in the pinned copy.
- `methodology/` — the methodology documents alone, for projects that copy only the methodology.
- `docs/customization.md` — how to place the copy in a project, fill the values, and instruct an Agent.
- `ko/` — the Korean edition with the same layout. The English text at the root is canonical.

Improvement loop: closing records → re-evaluation under `adaptation.md` → incident cases → a comparison whose scope a human approves → adoption decided and recorded by a human.

The workflow uses four execution grades (Trivial, Small, Medium, Large). Epic is an optional grouping for independently tracked issues, with no separate decomposition review gate. A single Large issue remains valid; shared-change verification, human-decision boundaries, and evidence for the overall outcome remain required. See [Epic management unit](adaptive-sdd/workflow/process/sdd/epic.md#epic-management-unit).

## What this is not

- **Not a replacement for v0.2.** It does not carry over v0.2's documents, starter, or templates. v0.2 remains on `main`.
- **Not a verified result.** No effect on outcomes, rework, or cost has been measured. The procedures and skills were used in one product; that experience does not establish the effectiveness of this generalized preview. Checks and reviews have the revision-specific scope below.
- **Not an enforcement mechanism.** It is guidance for agents and people; it is not a security boundary or an agent runner.

## Verification scope

- **Published `v1.0.0-preview.2`:** manifest checks, installer unit tests, one Windows installation rehearsal using a locally built archive and a fictional project, and one independent review were recorded for that release. They do not validate subsequent changes.
- **Unreleased commit `068618bdda2f8d0571da3099f5e132e4ff17ff1e`, checked on 2026-10-27:** all 25 executable tests passed on Windows with Python 3.14.7; both methodology manifests and the 51-file bundle manifest matched. A ZIP built from that commit passed `init`, `render`, `check`, and `check-evals` in a disposable project. The 60 cases across four skills passed structural checks; they were not executed as model behavior evaluations.
- **Integration candidate, checked on 2026-10-30:** based on `5a81d647771cb56fcf1f1d84e94d580f2ca2d963` plus the guide, verification-scope, changelog, observation-evidence and manifest corrections in this change. All 35 executable tests passed on Windows with Python 3.14.7. Both methodology manifests and the 64-file bundle manifest matched. A ZIP of the candidate passed `init`, `render`, `check`, and `check-evals` in disposable local-docs and GitHub-adapter projects; 70 cases across four skills passed structural checks. No live GitHub tracker operations or model behavior evaluations were run.
- **preview.5 candidate, checked on 2026-10-30 (uncommitted working tree):** all 53 executable tests passed on Windows with Python 3.14.7, including execution-profile checks, cross-edition comparison of file sets, headings, template tokens and case IDs, link and anchor resolution after an English install, re-installation after switching editions, and edition-wording validation. Both bundle manifests (66 files each) matched, and both editions passed `init`, `render`, `check` and `check-evals` (76 cases) in disposable projects. The Korean edition's generated files are byte-identical to preview.4 except `sdd-workflow.md`, which gains the execution-profile table. The English edition is a translation. It had one independent translation review against the Korean edition on 2026-10-30 (gpt-6-astra, reasoning medium); the accepted findings are fixed in this change. Behavior evaluation results are in the [evaluation record](docs/eval-results/2026-10-30/README.md).
- **Review and remaining limits:** [CHANGELOG.md](CHANGELOG.md) records the scope and timing of earlier reviews. Apart from that translation review, the checks above are not a new independent review. Actual POSIX execution, live remote/host integration, and effects on outcomes, rework, or cost remain unverified.

## Getting started

Read [docs/customization.md](docs/customization.md) (Korean: [ko/docs/customization.md](ko/docs/customization.md)).

1. Following the guide, download the archive of a reviewed commit SHA and copy `adaptive-sdd/` (or `ko/adaptive-sdd/`) byte for byte to the project's `.adaptive-sdd/`.
2. Run `install.py init` to create `project.json`; an Agent drafts it and a human decides. Only a human decides the human-judgment points, delegations and the execution profile.
3. Run `install.py render` to generate the project-dependent files and `install.py check` to verify them.
4. Instruct the Agent through the skills.

For a methodology-only copy, see the last section of the guide.

These guides cover `v1.0.0-preview.5`; verify its full commit SHA and use the matching archive and guide. `v1.0.0-preview.2` does not include the external installer features described here.

## Versions

- Latest published preview: [`v1.0.0-preview.4`](https://github.com/seok-jun/adaptive-agentic-sdd/releases/tag/v1.0.0-preview.4). This branch is the `v1.0.0-preview.5` candidate.
- Preview tags: `v1.0.0-preview.N`. Published tags are never moved; fixes come as new tags.
- Pin a copy by tag, commit SHA, and manifest hash, not by tag name alone.
- When upgrading, replace only the pinned copy, keep `project.json`, the adapter and work records, and regenerate the project-dependent files.

## License

[MIT](LICENSE)
