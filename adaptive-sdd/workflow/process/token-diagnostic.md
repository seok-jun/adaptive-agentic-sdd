# Token diagnostic

Read only when `Token diagnostic mode` in `W/../project/sdd-workflow.md` is `ENABLED`. General application and incident observations follow [observations](observations.md) and are not disabled by this mode.

| Actual lifecycle event | Section to read |
| --- | --- |
| Start of Issue work | [START](#start) |
| Interruption that needs state outside the lane | [BLOCKED](#blocked) |
| Resumption with evidence of a state change | [RESUME](#resume) |
| Final closing as completed or not-planned | [END](#end) |

## Stabilization-period token diagnostic

The mode value is read from the specified `W/../project/sdd-workflow.md`

This mode is temporary instrumentation for the workflow stabilization period. After collecting a sample of about 20–30 Issues or about two weeks, review the baseline, and if there is no decision to keep it, change the value above to `DISABLED`. Skills record the checkpoints below only when the mode in the P application document above is `ENABLED`, so disabling it does not require redesigning each execution procedure.

The authoritative current run token total is queried from the host's authoritative goal tracker only once, at the time of the lifecycle event. If there is no tracker value, do not estimate a number or do a repository-wide search or separate analysis; skip the checkpoint. Whether instrumentation succeeds does not change implementation decisions, review, test, CI scope or completion verdicts.

The token checkpoints recorded in Issue comments are only the following four kinds. Do not create checkpoints per command, per implementation step or per review turn.

### START

Record once when actual Issue work starts after passing a valid claim and the grade gate. If the same Issue already has a `TOKEN START`, do not record a new one.

```text
[WORKFLOW][TOKEN START]
issue: #NNN
grade: Trivial | Small | Medium | Large
tokens: {current}
```

### BLOCKED

Record just before stopping at a blocker that needs state outside the current lane, such as user input, external authentication or external approval. While the same blocker remains unresolved, record only once the first time, and do not create automatic re-checks or additional checkpoints.

```text
[WORKFLOW][TOKEN BLOCKED]
issue: #NNN
tokens: {current}
reason: external-blocker
blocker: {non-sensitive category}
resume-condition: {non-sensitive condition}
```

### RESUME

Record once when the previous token lifecycle is `BLOCKED` and actual work resumes on a new user instruction or evidence of a state change. `from` uses the URL of the previous `TOKEN BLOCKED` comment to link the spans.

```text
[WORKFLOW][TOKEN RESUME]
issue: #NNN
tokens: {current}
from: {previous TOKEN BLOCKED comment URL}
```

### END

Record once when the Issue is finally closed as `completed` or `not-planned`. `start` is the token of the first START, `end` is the current token, and `used` is `end - start`. From the tokens, blocker categories and URL links of the BLOCKED/RESUME comments, it must be possible to calculate separately the increase in each blocker span, the number of resumes and whether the same category recurred.

```text
[WORKFLOW][TOKEN END]
issue: #NNN
result: completed | not-planned
start: {start}
end: {end}
used: {delta}
```

The current lifecycle state is determined from the Issue's existing token checkpoint comments. For an Issue that ended without BLOCKED, do not create `TOKEN BLOCKED` or `TOKEN RESUME`; do not create duplicate comments for the same event or any token checkpoint other than START/BLOCKED/RESUME/END.

END for `completed` is recorded after product completion is confirmed, separately from local cleanup. `not-planned` is recorded at the time final closing is settled. If an END already exists, do not record it again. If there is no tracker, only the checkpoint is skipped; general observations, verification and the review gate remain.
