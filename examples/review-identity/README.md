# Review-target identity

**OPTIONAL / FICTIONAL — an implementation outline, not a supplied capture tool or runtime enforcement.** The [review policy](../../docs/review-gates.md) defines when evidence and approvals remain applicable. A commit or another unambiguous snapshot is sufficient when it identifies the full candidate; this outline is useful when review spans a dirty worktree and an external work item.

## Capture the reviewed inputs

Keep the following in an immutable, locally retained record:

| Part | Contents |
| --- | --- |
| Identity | Review phase, repository, HEAD, fixed comparison base, capture time, snapshot format version |
| Coverage | Included paths/direct dependencies, exclusions and reasons, candidate selection rule |
| Effective files | Sorted path, presence/deletion, effective content digest, relevant file mode or link target |
| Work-item contract | Authoritative item revision or frozen export; ACs, scope, fixed decisions, modification boundaries, applicable policy versions |
| Evidence context | Verification evidence references, test inputs and relevant environment/configuration identities |

Capture the effective candidate the reviewer actually reads. Inventory staged and unstaged changes, tracked deletions, and relevant non-ignored untracked files. Compare the union of paths in the fixed base and current candidate so a deleted path remains represented as absent. Include relevant dependencies and explicitly approved ignored inputs when they affect the claim; do not indiscriminately collect ignored files or secrets.

For this outline, `files` fingerprints effective contents/presence/modes within the recorded coverage, rather than staging labels. Committing an unchanged reviewed file can change its tracked/staged label without changing the effective candidate. Keep the Git inventory separately so the final commit can be checked against that candidate; a staged-only commit may omit reviewed unstaged or untracked content.

Store the work-item export as historical evidence with its source reference; do not create a second editable requirements authority. A URL or issue number alone does not freeze its content. Preserve retrievable inputs alongside digests: a hash cannot explain an absent contract. Reject incomplete, inconsistent, or concurrently changing captures instead of treating missing data as equality.

## Compare two complete captures

Illustrative pseudocode; `same` compares complete, canonically encoded fields or their digests:

```text
require complete_and_consistent(reviewed, current)
require same_repository(reviewed, current)

inputs = [phase, base, format, coverage, candidate_selection,
          files, work_item_contract, evidence_context]

if any input differs:
    return changed
if reviewed.HEAD != current.HEAD:
    return head-only
return identical
```

Capture time and bookkeeping labels are provenance, not content identity. A missing field, unreadable input, or comparison error stops the comparison without one of these three successful results. Report the gap and resolve it before reusing the affected verdict; do not label it `identical`.

| Result | Meaning | Follow-up |
| --- | --- | --- |
| `identical` | HEAD and all compared review inputs match | Reuse only within the original review's scope; this does not prove an AC or grant authorization |
| `head-only` | HEAD differs, but all compared review inputs match | Record the old/new mapping, check final commit contents and continuing evidence relevance, then apply the existing authorization policy to the new candidate |
| `changed` | At least one review input differs | Assess impact; refresh affected evidence/reviews and any required approval rather than repeating every check automatically |

These are comparison results, not review verdicts or verification statuses. `head-only` never automatically transfers approval. Even matching file contents cannot establish equivalent runtime evidence when a build embeds the commit ID or an environment changed. Expand coverage when an outside change affects a reviewed dependency; do not hide it by excluding the path.

## Static walkthroughs — not executed tests

- Same captures, except capture time: `identical`.
- Reviewed untracked file is committed with the same contents and all other inputs match: `head-only`; still verify that the final commit contains the complete candidate.
- HEAD is unchanged but an unstaged file or an issue AC changes: `changed`.
- A tracked file is deleted or a relevant untracked file is added: `changed`.
- Work-item export is unavailable or the candidate changes during capture: no comparison result; obtain a complete capture.
- Source files match but the execution environment identity changes: `changed`; old runtime evidence needs a relevance assessment.
