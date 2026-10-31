# Work tracking: local documents

This document describes how the Issue, comment, label, assignee, PR and closing-reference expressions in the W procedures are realized as **work documents in a shared folder outside the repository**. The P project document `tracker.md` declares this method and sets `tracker_root` (an absolute path) and the ID format. When reading W documents, translate them with the mapping table below. A tracker operation that is not in the mapping table is not run; stop with `BLOCKED: tracker operation unsupported`.

## Why a shared folder outside the repository

Parallel lanes work in different worktrees and branches. If claims and work records live only on one lane's branch, other lanes cannot see them. So work documents and claims are kept in `tracker_root`, which every worktree reads and writes at the same absolute path. `tracker_root` is not placed inside any lane's worktree. If history is needed, `tracker_root` can be its own git repository with a commit for each record (P declares this).

## Folder structure

```text
<tracker_root>/
  items/<ID>.md        work document (= Issue)
  claims/<ID>.claim    active claim (= [CLAIM] + assignee + status:in-progress)
  index.md             optional. A list for people; the source is items/
```

## Mapping table

| Expression in the W procedures | Local document method |
| --- | --- |
| Create an Issue | Create `items/<ID>.md` in a way that **fails if it already exists**. On an ID collision, check P's id_source. Only `generated` reissues a number; for `external`, check the source/existing work and never increment arbitrarily |
| Issue number `#N` | `<ID>` |
| Issue body | The body sections of the work document excluding `## Meta` and `## Records` |
| `priority:*`, `grade:*`, `status:*` labels | The `priority:`, `grade:`, `status:` lines in `## Meta`, exactly one each |
| An Epic's `type:epic` label | `type: epic` in the management document's `## Meta` and `Epic` in the body's `## Work type`. No `grade:` line. priority and status are kept |
| assignee | The `owner:` line in `## Meta` |
| Setting the Priority/grade values at creation | Write the `priority:` and `grade:` lines in `## Meta` in the same write that creates the document |
| Replacing a `priority:*` value | Rewrite the `priority:` line in `## Meta` (only the lane or Agent allowed to edit the body and meta) |
| Creation order of Issues | The `created:` time in `## Meta` |
| Issue comment | An entry appended to `## Records`, in the "Record entries" format below |
| Comment URL / ID | `items/<ID>.md#<entry id>` |
| Comment `updated_at` | The entry's `written` time. Entries are never edited, so the written time is the update time |
| `[CLAIM]` | Create `claims/<ID>.claim` in a way that fails if it already exists, and record the same content in `## Records` |
| `[RELEASE]` | Record `[RELEASE]` in `## Records`, then delete `claims/<ID>.claim` |
| open PR | The task's branch that has not yet been merged into the declared merge branch |
| PR head / base SHA | Branch head SHA / SHA of the declared merge target |
| `Closes #N` in the PR body | The `closes: <ID>` line of the `[IMPLEMENTATION SUMMARY]` entry |
| PR mergeability | Exit code 0 of `git merge-tree --write-tree <code-remote>/<merge-branch> <branch>` (Git 2.38 or later) means no conflicts. If that cannot be used, try the merge in a disposable worktree, record only the result and discard it |
| PR merge | Merge the branch into the merge target branch of the declared code remote with the `Merge method` (merge, squash, rebase) of the P project document `tracker.md`, and push. Who merges follows P's human judgment points. The merging side records a `[MERGED]` entry in `## Records` (`branch:`, `head:` branch head SHA, `main:` the resulting SHA of the declared merge branch, `method:`). If the merge method is not set, `BLOCKED: tracker operation unsupported` |
| Merged check | After `git fetch <code-remote> <merge-branch>`, for `merge`, `git merge-base --is-ancestor <branch head> <code-remote>/<merge-branch>` must succeed. For `squash` and `rebase`, the original branch head may not be in the merge branch, so check that the `main:` SHA of `[MERGED]` is an ancestor of `<code-remote>/<merge-branch>` and that its commit message contains the task ID. Record the confirmed <code-remote>/<merge-branch> SHA |
| CI | The local commands set by `## Verification baseline` of the P project document `build.md`. If there is CI, the `CI` entry of the same document declares it too |
| PR-based review candidate publication | Push the artifacts to P's publication repository, remote and branch and record the exact SHA. Distinguish it from the product claim branch and follow the publication conditions of W design-review |
| Issue closed (automatic closing after merge) | There is no counterpart to GitHub's automatic closing, so after the merged check the Agent performing the closing procedure writes `status: closed` and the `closed:` time in `## Meta` and records a `[CLOSED]` entry (`by-merge: <main SHA>`) in `## Records`. Do this only when `closes:` of `[IMPLEMENTATION SUMMARY]` is this task ID |
| Issue not-planned | `status: not-planned` and the `closed:` time in `## Meta`, and an entry with the reason in `## Records` |
| The `product-complete:` JSON of `[PRODUCT COMPLETE]` | `{"schema_version":1,"issue":"<ID>","pull_request":null,"branch":"<branch>","head":"<branch head SHA>","merge_commit":"<main SHA of [MERGED]>"}` |
| Updating a comment (for example updating the same `[IMPLEMENTATION SUMMARY]`) | Do not edit the earlier entry; append a new entry with the same tag and write `supersedes: <earlier entry id>`. The most recent entry of a tag that no other entry supersedes is the current value. The first entry stays as it is, which satisfies W's "preserve the first original" |
| Issue search / duplicate check | Search titles, meta and bodies under `items/`. Report the search scope and the number of results |
| reopen | Reopen `status:` and record `[REOPEN]` in `## Records`. Do not delete the earlier closing records |

## Code remote

The local document method changes the Issue, comment, label and PR expressions. The code remote, new lane base, product merge target and SDD publication repository/remote/branch follow the declarations in P tracker.md (default origin/main). The publication remote may be a local bare repository outside the repository, but the reviewer must be able to read the same path and the exact commit. Repository creation, connection and push permissions are checked separately; the existence of a local file alone does not count as publication. The `main:` field name of existing records is kept for compatibility, but its value is the resulting SHA of the declared merge branch.

## Review input

The Issue body under review is, as in the mapping table above, the body excluding `## Meta` and `## Records`. Adding a review record alone does not change the body's review identity to a new head. The conditions for confirming that the target body and direct contracts are unchanged follow `process/design-review.md`.

The initial blind review receives only the body extracted from the exact candidate and the required artifacts. The side preparing the reviewer input performs the extraction preserving UTF-8 bytes; it does not hide the records by filtering the full `git show` output with shell string filters. The procedure for checking the extraction scope, original/copy hashes, actual read permissions and finding mentions left in the body follows [Blind input preparation and check](../skills/_shared/execution-packets.md#blind-input-preparation-and-check). Do not delete the original's meta or records or change another lane's record format.

## Work document format

```markdown
# <ID> <title>

## Meta
priority: P2
grade: Small
status: open
owner: none
created: 2026-10-19T09:00:00+09:00

<!-- Below is the required body of a new Issue from W process/issue-priority.md -->
## Priority
...
## Acceptance criteria
- [ ] ...

## Records
```

The values in `## Meta` and the values of `## Priority` and `## SDD grade` in the body must always be the same (W's body–label consistency rule).

An Epic management document uses the work type above instead of a grade. Closing children does not automatically close the Epic; the owner confirms the evidence that the overall goal was achieved, then updates the status and records the closing evidence in `## Records`. The management document itself is not required to have the product PR's `[MERGED]` or `[PRODUCT COMPLETE]`.

## Record entries

`## Records` is **append only**. Do not edit or delete an entry already written. A wrong entry is corrected with a new entry that points to the original entry id.

```markdown
### r-20261019T091500-a1 [CLAIM]
written: 2026-10-19T09:15:00+09:00
author: <agent or human identifier>

agent: <agent-id>
branch: <branch-name>
allowed:
- <path glob>
forbidden:
- <path glob>
```

- The entry id has the form `r-<UTC time>-<short random value>`. If it is duplicated within the same document, make a new one.
- First-line tags (`[CLAIM]`, `[RELEASE]`, `[IMPLEMENTATION SUMMARY]`, `[PRODUCT COMPLETE]`, `[LOCAL CLEANUP]`, `[HUMAN DECISION REQUIRED]`, `[OBSERVATION REVIEW]`, `[WORKFLOW][TOKEN ...]` and so on) use the comment tags of the W procedures as they are.
- W's conversation-content gate applies to record entries too.

## Concurrency

- A claim creates `claims/<ID>.claim` with **creation that fails if the file already exists**. Use a method where an atomic creation failure can be detected, such as PowerShell `New-Item -ItemType File` (errors if it exists) or Python `open(path, "x")`. If it fails, the task is already claimed.
- The claim file's content is the same as the body of the `[CLAIM]` record entry (`agent:`, `branch:`, `allowed:`, `forbidden:`). Fill the content in the same write as the creation. An empty or unreadable claim file is treated as another lane's claim and as an overlap.
- Use this method only on a local disk or an SMB shared folder. Synchronized folders such as OneDrive or Dropbox do not guarantee atomic creation and immediate visibility, so do not use them as `tracker_root`.
- The path-overlap check compares the allowed paths of all `claims/*.claim` with the current task's allowed paths. Read again after creating the claim; if a competing claim exists, release immediately as the W procedure says.
- When appending to a work document, do not rewrite the whole file; write one entry at once in append mode (PowerShell `Add-Content -Encoding utf8`, Python `open(path, "a", encoding="utf-8")`). Rewriting the whole file loses entries another Agent appended in the meantime. To avoid overwriting another Agent's entry, read the file again right before writing and check that your own entry id is there after writing.
- No procedure requires two Agents to edit the same work document at the same time. Only the lane holding the claim (or, without a claim, the Agent responsible for organizing work items) edits the body and `## Meta`, and only then is the whole file rewritten.

## Failures and limits

- If `tracker_root` cannot be accessed or a write fails, stop the dependent work with `BLOCKED: tracker unavailable`. Do not save elsewhere inside the repository or in another arbitrary location.
- A shared folder does not enforce author authentication and permissions as GitHub does. Author identification is self-reported, and W's "allowed authors" condition is checked only by matching the identification values P declared.
- Local files have no remote backup. If P does not keep `tracker_root` as a git repository, record the limit that lost records cannot be recovered.
