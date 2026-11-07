# Contributing

Adaptive Agentic SDD is a working methodology. For the 1.0.2 stable release and its verification scope, see [the release record](docs/releases/1.0.2.md).

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

- The documents in `methodology/`, `adaptive-sdd/` and `ko/adaptive-sdd/` are public sources and starter material. Projects may derive and evolve their own W/P; continued M use is optional. Immutable-copy checks apply only to the explicit legacy installer. `docs/customization.md` explains how to use them and must not establish competing rules.
- Keep `adaptive-sdd/methodology/` byte-identical to canonical `methodology/`. M changes regenerate all three M `manifest.json` files. Any change under either distribution also regenerates its `MANIFEST.json` (`adaptive-sdd/MANIFEST.json` or `ko/adaptive-sdd/MANIFEST.json`). Its exact bytes are `json.dumps({"files": {<path>: <sha256 hex>, ...}, "schema": 1}, ensure_ascii=False, indent=2, sort_keys=True) + "\n"` encoded as UTF-8.
- Explain whether a change alters meaning. Wording fixes and meaning changes are reviewed differently; a meaning change states which project behavior changes.
- Product facts and authority stay in P originals; project method adjustments belong in its own external W. Public contributions must remain general.
- Published tags are never moved. Fixes are released as new version tags.

## English / Korean synchronization

The English text at the repository root is canonical; `ko/` holds the Korean edition. When the methodology or the guide changes, update both editions in the same change. Preserve mandatory/optional conditions, ordering, statuses, and authorization semantics across languages. If the editions differ in meaning, the English text is authoritative and the Korean edition is corrected.

The three M manifests are `methodology/manifest.json`, `adaptive-sdd/methodology/manifest.json` and `ko/adaptive-sdd/methodology/manifest.json`. If one edition is pending, state that explicitly rather than reporting synchronization complete. The English and Korean bundles both contain workflow, templates and tools. Shared Python tools must remain byte-identical. Regenerate both bundle manifests after changes, and both English M manifests plus the Korean M manifest after M changes.
