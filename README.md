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
- **An eval structure** — static checks, behavior cases, cross-agent comparison, grading and result records, 30 fictional seed cases, and rules for turning a recorded incident into a diagnostic case.
- **An improvement loop** — closing records → re-evaluation under `adaptation.md` → incident cases → a comparison whose scope a human approves → adoption decided and recorded by a human.
- **An installer** — `tools/install.py` (Python 3.8+, standard library only) generates the project-dependent files (project documents, skill entry files for Claude Code and Codex, marked blocks in `AGENTS.md`, `CLAUDE.md`, and `.gitattributes`) from the project's `project.json`, and checks the copy and generated files against their hashes.

The English edition of these parts is pending and planned for a later preview. Until then, the Korean edition is the only source for them, and English-only projects use the methodology documents above.

## What this is not

- **Not a replacement for v0.2.** It does not carry over v0.2's documents, starter, or templates. v0.2 remains on `main`.
- **Not a verified result.** No effect on outcomes, rework, or cost has been measured. The procedures and skills were used in one product; their generalized form is published here for the first time. The checks for this preview are file integrity (the manifest hashes), the installer's unit tests, one pre-publication install rehearsal on Windows into a fictional project using a locally built archive, and one independent review.
- **Not an enforcement mechanism.** It is guidance for agents and people; it is not a security boundary or an agent runner.

## Getting started

- **English (methodology only):** read [docs/customization.md](docs/customization.md). Copy `methodology/` and `LICENSE` byte for byte, check the hashes, pin line endings, add a few lines to the entry file, and let an Agent draft the adapter; a human decides the human-judgment points.
- **Korean (full copy with installer):** read [ko/docs/customization.md](ko/docs/customization.md). Copy `ko/adaptive-sdd/` to `.adaptive-sdd/`, run `install.py init`, fill `project.json` (an Agent drafts, a human decides), then run `install.py render` and `install.py check`.

## Versions

- Preview tags: `v1.0.0-preview.N`. Published tags are never moved; fixes come as new tags.
- Pin a copy by tag, commit SHA, and manifest hash, not by tag name alone.
- Upgrading replaces only the copy; project values, the adapter, and work records stay.

## License

[MIT](LICENSE)
