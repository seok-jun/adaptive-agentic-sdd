# SDD completion

For the SUMMARY and human-judgment contract at closing, apply [issue](issue.md); for required verification and PASS validity, apply [verification](../verification.md). Reuse the same version you have checked.

## Document roles

| Kind | Location | Lifetime | Role |
| --- | --- | --- | --- |
| Business documents | `docs/domains/**` | Permanent | Current product behavior that remains after implementation is complete |
| SDD working documents | `docs/sdd/{feature}/` | During the work | AS-IS evidence, Human Decision Contract, Agent Execution Spec |
| Decision records | `docs/reviews/**` | Permanent | Evidence and alternatives for past decisions |
| Architecture documents | `docs/architecture/**` | Permanent | Module responsibilities, dependencies, work boundaries |

The locations above are defaults; the actual locations follow the `Document roles` table of the P project documents. SDD working documents are cleaned up at completion, but evidence that an active consumer references is either converted to an immutable reference under [finishing's reference preservation conditions](../../skills/finishing-issues/SKILL.md#4-remove-temporary-sdd) or preserved with an owner and release conditions set. Business documents are updated **by reading the final code behavior**, not by copying SDD documents or the Issue.

## Business document update

After implementation is complete, business documents record **what the current code actually does**.

1. Find the direct user/background entry points of the changed symbols.
2. Edit only the rules whose actual behavior changed because of the change.
3. Do not rewrite rules that did not change.
4. Do not copy sentences from the Issue, commit messages or SDD as they are.
5. If the code and an existing business document differ, apply the drift rules of `W/process/agent-instruction-policy.md`.

If a one-line rule exceeds 150 characters because it carries all of its conditions, exceptions and retries, split it into a detailed topic document and keep only the ID, a one-line summary and a link in the business index.

## Completion procedure

After implementation, do not change the order below.

1. Read the diff and settle the actual behavior changes.
2. Update the business documents directly connected to the changed behavior, based on the final code.
3. Before deleting the SDD, check the evidence of the required verification of the implementation under the Verification Strategy, and perform any missing or invalidated verification.
4. Delete the current work folder in the SDD working document location P declares, according to the [reference preservation conditions](../../skills/finishing-issues/SKILL.md#4-remove-temporary-sdd), or preserve it with its owner and release conditions stated.
5. Remove only the unnecessary SDD links from P's document index and other documents, and keep or convert the references active consumers need.
6. If related review documents have a current-status field, update it to match the actual status. Do not rewrite the content of past decisions themselves.
7. Fix the candidate after all planned repository file changes are finished, secure the final required verification evidence, and then perform the CODE Review/self-review for the grade. At closing, confirm the validity of both kinds of evidence together; earlier verification is reused only when there is evidence that its inputs did not change. The detailed order and reconfirmation after changes follow [finishing-issues' final candidate check](../../skills/finishing-issues/SKILL.md#5-prepareverify-pr-closure).
8. Leave one `[IMPLEMENTATION SUMMARY]` comment and add the closing reference to this Issue (`Closes #{issue-number}`, written as the declared tracker method defines) to the PR. Do not use the summary as substitute evidence for verification or for passing the required review.
9. After the PR is merged, confirm that the Issue was closed.

Do not delete SDD documents before updating the business documents.

If even one acceptance criterion fails or is unverified, do not check that item; leave it in the completion report.
