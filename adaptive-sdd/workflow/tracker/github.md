# Work tracking: GitHub

## Trivial/Small compact grouping

For Trivial/Small on the [compact route](../process/small-work.md), use three normal comments: `[CLAIM]` for ownership/start facts, `[IMPLEMENTATION SUMMARY]` for implementation/verification/observations, and `[CLOSED]` with separately labelled `merged`, `closed`, `product-complete`, `cleanup` and `release` fields. Keep each action's actual time and evidence; later facts may update the same comment with their times. Failures and corrections may exceed three comments. Confirm repository, allowed authors and capabilities at setup, then check for changes; inaccessible or unsupported operations stop dependent work, without token creation/search/registration.

CLAIM contains the ownership payload `agent`, `branch`, `allowed`, `forbidden` and start facts. CLAIM still requires assignee/status and conflict re-query before edits; losing acquisition does not authorize clearing another owner's state. Exactly one priority and grade are set at creation where supported, otherwise immediately after, then re-read; the compact body may combine headings and any duplicated values must agree.

Immediately before authorized merge re-query the explicit PR base, metadata, mergeability, required checks/reviews and authority. After merge, fetch the declared target and capture its tip separately from the PR's observed merge-result SHA (`merged.main`). Verify actual PR merged state and result identity in that target; for squash/rebase use the PR's resulting commit identity, not task-head ancestry or the fetched tip as a substitute. Confirm `Closes #N` targets this Issue and re-query actual Issue closed state. `product-complete` preserves exactly the adapter JSON `{"schema_version":1,"issue":N,"pull_request":PR,"merge_commit":"40-character SHA"}` with the actual merge-result SHA and completion time, independently of cleanup.

`cleanup` records actual state/time and remaining work. Preserve product completion and retain ownership while required cleanup remains incomplete. Release follows this sequence:

1. Re-check the matching active CLAIM. In `CLOSED.release`, record `claim` (the exact CLAIM comment ID/URL), matching `agent` and `branch`, `state: prepared` and the preparation time. Preparation does not terminate a claim.
2. Clear only owned assignee/status metadata and re-query to verify its removal. Never change a competitor's metadata. If removal or verification fails, leave the claim active and record release incomplete.
3. Only after that check, update the same `CLOSED.release` to `state: released` with the actual release time, retaining the preparation facts. This is the terminal release record for that exact CLAIM, equivalent to `[RELEASE]`; it does not delete the CLAIM comment.
4. Re-read CLOSED and the Issue metadata. Report success only when the matching terminal release and absence of owned active metadata are observed. A failed update or unreadable result leaves release unconfirmed; preserve product completion and record a correction/incomplete release even beyond three records.

Later readers match releases by exact CLAIM ID/URL plus agent/branch. A CLAIM is active unless it has a matching terminal `state: released` record; a missing, prepared, incomplete or unreadable release cannot establish release. A release for an earlier claim does not release a later claim, even for the same agent/branch. Conflict checks use active claims' allowed/forbidden paths and re-query owned metadata; remaining or unverifiable metadata prevents treating ownership as fully cleared. Preserve historical CLAIM/RELEASE comments and the facts/times in CLOSED when updating it.

This document describes how the Issue, comment, label, assignee, PR and closing reference expressions of the W procedures are realized with **GitHub Issues and PRs**. W uses tracker-neutral terms (see the workflow README); this table is the GitHub realization of each. P's application document `tracker.md` declares this method and sets the repository (`owner/name`) and the allowed authors.

| Expression in the W procedures | GitHub |
| --- | --- |
| Issue, `#N` | A GitHub Issue in the declared repository |
| `priority:*`, `grade:*`, `status:*` labels | Issue labels with the same names |
| Setting the Priority/grade values at creation | Include both labels in the creation request when the API allows it; otherwise add them right after creation |
| Replacing a `priority:*` value | Remove the existing `priority:*` label, then add the new one |
| Order of Issue numbers | The GitHub Issue number |
| Epic management document | The `type:epic` label and `Epic` under `## Work type` in the body. No `grade:*`. Child Issues are linked from the body, and the management Issue is closed after the evidence of overall completion is checked |
| assignee | Issue assignee |
| Issue comment, URL, `updated_at` | Issue comment and its URL and `updated_at` |
| `[CLAIM]` / `[RELEASE]` | An Issue comment that starts with that tag. On the compact route, the terminal RELEASE is the matching `CLOSED.release` defined above |
| PR, `Closes #N` | A PR in the declared repository and the closing reference `Closes #N` in its body |
| The `product-complete:` JSON of `[PRODUCT COMPLETE]` | `{"schema_version":1,"issue":N,"pull_request":PR,"merge_commit":"40-character SHA"}` with the Issue and PR numbers |
| merged / closed | The PR merged state and merge commit, the Issue closed state |
| CI | The repository's required checks. P declares the actual verification commands |

P and humans manage GitHub write permissions, tokens and secrets. The Agent does not create, look up or register tokens.

The code remote, the base of new lanes and the PR base follow the git.remote/base_branch/merge_branch declarations in P's tracker.md. When creating a PR, state the base explicitly and do not guess the default branch. The SDD publication repository, remote and branch follow the review declaration and are kept distinct from the product PR head and the claim branch. External ID settings do not change GitHub's actually issued IDs or closing reference syntax, and no API adapter for other services is provided.
