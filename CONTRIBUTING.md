# Contributing

Adaptive Agentic SDD is a working methodology. This branch carries the 1.0 preview; the v0.2 contribution guide remains on `main`.

Contributions are most useful with operational evidence:

- Which slot was missing from the adapter, so that a project had to edit the common copy?
- Which rule prevented a real failure, and which only added cost?
- Which observation was recorded but never used in a later judgment?
- What can be removed safely?

Prefer removing or simplifying over adding ceremony by default.

## Public-content boundary

Extract general rules and write new fictional examples. Do not copy private material and merely rename an organization.

Do not publish organization/customer names tied to private work, internal ticket identifiers, directory layouts, business logic, schemas, endpoints, credentials, production data, screenshots, or unsanitized logs. Check documentation, code blocks, images and SVG metadata, commit messages, and PR descriptions. When reporting a problem found while using the methodology at work, check your organization's information-disclosure policy first.

State proposed features as draft. Separate observed evidence, static/self-review, independent review, and unrun checks. Do not invent efficacy claims, token savings, test results, or deployment history.

## Common layer consistency

- The documents in `methodology/` and `ko/methodology/` are the common layer that projects copy and pin. `docs/customization.md` explains how to use them and must not establish competing rules.
- Any change to a document in `methodology/` or `ko/methodology/` regenerates that folder's `manifest.json` in the same change. Its exact bytes are `json.dumps({"files": {<path>: <sha256 hex>, ...}, "schema": 1}, ensure_ascii=False, indent=2, sort_keys=True) + "\n"` encoded as UTF-8.
- Explain whether a change alters meaning. Wording fixes and meaning changes are reviewed differently; a meaning change states which project behavior changes.
- Project-specific facts and adjustments belong in the project's adapter, not in the common layer.
- Published tags are never moved. Fixes are released as new preview tags.

## English / Korean synchronization

The English text at the repository root is canonical; `ko/` holds the Korean edition. When the methodology or the guide changes, update both editions in the same change. Preserve mandatory/optional conditions, ordering, statuses, and authorization semantics across languages. If the editions differ in meaning, the English text is authoritative and the Korean edition is corrected.

Each edition has its own `manifest.json` (`methodology/manifest.json` and `ko/methodology/manifest.json`). If one edition is pending, state that explicitly rather than reporting synchronization complete.
