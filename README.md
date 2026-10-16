# Adaptive Agentic SDD — 1.0 preview

**English** | [한국어](ko/README.md)

> **Preview.** This branch (`v1-preview`) carries the 1.0 preview of the next-generation methodology. Its effect has not been measured, and its structure may change before 1.0. The v0.2 methodology remains on `main` and at tag [`v0.2.0`](https://github.com/seok-jun/adaptive-agentic-sdd/tree/v0.2.0).

## What this is

A thin common layer that a project copies, pins, and adjusts through its own adapter.

- `methodology/core.md` — a minimal workflow, the human-judgment requirements, and how work records and observations are kept.
- `methodology/adaptation.md` — rules for choosing and re-evaluating supports based on observed evidence rather than model names or confidence.
- `methodology/supports/ordered-changes.md` — one default support: an ordered change list tied to requirements.
- `methodology/manifest.json` — sha256 of the three documents, used to check a copy.
- `docs/customization.md` — how to place the copy in a project, fill the adapter, and instruct an Agent.
- `ko/` — the Korean edition of the README, methodology, and guide. The English text at the root is canonical.

## What this is not

- **Not a replacement for v0.2.** It has no risk grades, review gates, starter, or templates. Everything outside the common layer belongs to the project.
- **Not a verified result.** No effect on outcomes, rework, or cost has been measured. The only checks for this preview are file integrity (the manifest hashes) and one pre-publication rehearsal on Windows, using a locally built archive, of copying, hash checking, line-ending pinning, and the first two Agent prompts (observe, draft the adapter).
- **Not an enforcement mechanism.** It is guidance for agents and people; it is not a security boundary or an agent runner.

## Getting started

Read [docs/customization.md](docs/customization.md). In short:

1. Download the tag archive and copy `methodology/` (or `ko/methodology/` for the Korean edition) and `LICENSE` into the project byte for byte.
2. Check the hashes against `manifest.json` and record the tag, commit SHA, and manifest hash.
3. Pin line endings with `.gitattributes`, add a few lines to the entry file, and write the adapter.
4. Let an Agent observe the repository and draft the adapter; a human decides the human-judgment points.

## Versions

- Preview tags: `v1.0.0-preview.N`. Published tags are never moved; fixes come as new tags.
- Pin a copy by tag, commit SHA, and manifest hash, not by tag name alone.
- Upgrading replaces only the copy; the adapter and work records stay.

## License

[MIT](LICENSE)
