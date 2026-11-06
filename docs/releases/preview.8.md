# v1.0.0-preview.8 release preparation

Status: locally prepared candidate on `release/preview.8-agentics`, not published. No tag has been created or moved by this work. The candidate identity is the commit containing this preparation record; resolve it with `git rev-parse HEAD`.

## Behavior change

- M improvement selection now considers cause, expected benefit and cost, reuse of existing measures, mechanical checks or execution controls for decidable conditions, and guidance/review for remaining interpretation. Useful partial coverage is sufficient to consider adoption; required protections, verification and existing authority remain in place. This principle adds no new document, classification table or approval step.
- Public M is an optional starting reference. Continued adaptation of derived project W/P to their project is recommended; continued M use, update tracking and conformance are not obligations.
- Recommended adoption keeps editable W outside P, P originals/authority inside P, and only a portable area connection in P. Explicit task selection precedes method loading.
- `tools/agentics.py` performs read-only local resolution. It does not scaffold W, migrate products, fetch sources, execute a workflow, install host skills or reset sessions.
- Existing `install.py` users retain the legacy contract. Storage-only relocation does not remove old automatic activation; follow the reviewed migration steps.

## Verification of the original local candidate (before the 2026-11-06 integration)

- Windows / Python 3.12.2 / Git 2.39.1.windows.1: `python -I -B -m unittest discover -s tests` — 111 tests passed (22 resolver tests plus 89 existing regressions). The suite's printed synthetic ERROR/INVALID cases are expected fixture assertions, not live agent calls.
- Both editions' real starter trees resolve in disposable Git repositories without legacy installation. Resolver tests also cover no-read unselected mode, custom W with no M dependency, changed W commit selection, another P checkout, fail-closed inputs, duplicate keys and preservation of P files.
- Both 69-file bundle manifests and all three 3-file M manifests regenerated; exact checks are repeated before handoff.
- Local links/anchors checked in 10 changed/release documents: no failures.
- Post-change independent Claude review: four read-only calls, requested `opus` / high; each CLI response reported `claude-opus-5-5`. First review found no P1 and four P2s. All four were fixed: Git index writes, missing explicit W/support paths, unnamed task guards, and first-task selection/provisional labels. The second review resolved all P2s and found no new P1/P2. The third and fourth were bounded reconfirmations of the subsequent path/environment/partial-clone fixes and found no new P1/P2.
- Review-driven checks include index-byte preservation, explicit directory resolution, no-M custom W, ignored/hidden-index content rejection, tracked entry/directory requirements, repository-redirect environment isolation and rejection of partial/promisor clones before status. English/Korean activation meaning, tool byte parity and both licenses were checked.
- Review scope: actual supplied code/tests, both activation/guard/core editions, READMEs and adoption guides; the first pass also included the design proposal and release record. Claude executed no tests and did not audit every repository file. Final narrow passes covered only their changed source areas. Source/manifest consistency and the complete executable suite were checked separately by Codex.
- Remaining optional observation: a multiline Git config value can cause a conservative false rejection in the full-clone check; it cannot select another source or bypass the check. Native host activation and effect on outcomes/rework/cost remain untested. Git/host documentation was read for invocation and locking semantics; documentation support is not behavioral evidence.

The pre-existing uncommitted W clarifications are included and reviewed as part of the original local candidate. Historical preview.7 behavior evaluations and the earlier bounded M/W review do not validate preview.8 activation.

## Integration verification — 2026-11-06

- Integrated remote `v1-preview` at `09aa2ac` (readability change `ff6e7a3` and its merge) with local preview.8 candidate `fa7e3b6`. The remote readability changes do not change rule meaning; they and the local adoption changes are retained. Only the two bundle manifests conflicted; they were regenerated from the combined file sets and final bytes.
- Added the improvement-selection principle to canonical English M, the English bundle and Korean M. This is guidance for choosing improvements, not evidence of improved agent behavior.
- `python -X utf8 -I -B -m unittest discover -s tests`: 111 tests passed. All five manifests matched their files and canonical JSON serialization; shared Python tools remained byte-identical across editions. A reverse-application check confirmed all remote workflow readability edits are present.
- Independent read-only Claude review (CLI-reported `claude-opus-5-5`) found no P1 or rule-text regression and one P2: release records did not distinguish the integration from earlier verification. This dated section and the historical heading address that finding. Claude also checked the newly added link anchors; it did not run tests. Its scope was the integration diff, M editions and release records, not a full repository audit. Optional M terminology and Korean wording suggestions were incorporated. A bounded follow-up review of both M editions and the release records confirmed the P2 resolved and found no unresolved or new P1/P2.
- No behavior/effect experiment, product migration, push, tag or publication was performed in this integration.

## Publication handoff

1. Commit the reviewed candidate on a release branch; review the diff and ensure no private product material is present.
2. Run the complete executable suite, all manifests, edition equality, document links and diff checks on that candidate.
3. Review the candidate PR and publication scope. Preparation alone does not publish a tag or release.
4. On publication, identify the final commit, create a new immutable annotated `v1.0.0-preview.8` tag, and publish prerelease notes from this record. Never move preview.7 or an existing preview.8 tag.
5. Replace candidate wording with the actual published status and record post-publication tag/commit verification. Do not invent a release SHA before committing.

## Limits

Fresh-session is a caller assertion, origin checks are local consistency rather than authentication, and READY is not proof of reading/activation/compliance. Tracker access is checked by the selected workflow, not the resolver. A native host loader, automatic setup/migration, cloud provisioning and version revocation feeds are not shipped. No live product migration or new behavior/effect experiment is part of this preparation.
