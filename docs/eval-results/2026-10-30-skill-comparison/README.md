# Pending Claude skill comparison

Status: **NOT RUN**. Prepared on 2026-10-30 for continuation on the home machine. No subject or grader model calls have been made. The user deferred execution because the Claude allowance was exhausted.

Branch: `codex/claude-skill-ab-experiment`.

## Question and evidence

Does the wording change in `721e086a7c7312c5fd6a590325bde87666c0629c` improve Claude's action plans for II-S02 and FI-S02, while handling missing evidence correctly?

In the [original evaluation](../2026-10-30/README.md), Claude failed II-S02 and FI-S02 in all three runs; Codex passed both in all three runs. Thus **Claude is the subject and Codex is the independent grader**, not the other way around. Original Claude requests used `opus`, with `claude-opus-5-5` reported by the CLI. Original answers were not retained in the repository and cannot be regraded from repository files.

The skill changes are already committed locally in `721e086`. They clarify the first targeted verification and incomplete-status reporting. They are not proven improvements. `v1.0.0-preview.5` remains published at `ee5c60a246a95218e0f429681036fa9bd4bd1e03`; do not move it or merge this experiment into `v1-preview` automatically.

## Frozen comparison

`selection.json` contains the three complete Korean fixtures and rubrics, copied from `721e086`, and a checksum. Freeze these before the first model call; do not change them after seeing results.

- Subject: Claude Code, three independent fresh sessions per case per arm. Pin one exact available Claude model for both arms; prefer the original served model if available. Do not silently substitute a different model mid-run. Record CLI version, requested model, returned model identity, reasoning/effort, loaded instructions and usage.
- Grader: Codex CLI, `gpt-6-astra`, reasoning `medium`, one fresh independent session per answer. Pin that setting across all grades. Hide arm, source SHA, prior scores, other answers and the intended improvement from the grader.
- Budget: 18 subject calls (3 cases × 2 arms × 3 repeats), at most 18 grader calls. No automatic retries. This is a call-count bound, not a currency estimate. Before execution, confirm the home account has sufficient allowance and record the exact Claude model/effort in the selection. No model calls are authorized merely by checking out this branch; resume the user's requested experiment explicitly.
- Use the Korean edition to match the original failures. English static synchronization has been checked, but English behavior is outside this experiment.
- Before arm: skill bodies from `ee5c60a246a95218e0f429681036fa9bd4bd1e03`.
- After arm: skill bodies from `721e086a7c7312c5fd6a590325bde87666c0629c`.
- Everything else comes from `721e086` in both arms. Replace only `workflow/skills/implementing-issues/SKILL.md` and `workflow/skills/finishing-issues/SKILL.md` in the before arm, then regenerate the derived bundle manifest. Assert that the only bundle differences are those two bodies and `MANIFEST.json`.
- Use the **corrected FI-S02 fixture in both arms**. Comparing the old incomplete fixture against the corrected one would confound fixture repair with skill wording. Likewise supply the new missing-evidence case to both arms.
- Every session gets a fresh disposable installation outside the repository. Run `init → render → check` before the subject. Do not expose case rubrics or past results: remove all four `workflow/skills/*/evals/cases.json` answer-key files identically from both disposable bundles before regenerating manifests and installing. Keep the frozen fixtures/rubrics outside subject-accessible projects. These derived bundles are evaluation-only and must not be shipped.
- Allow Claude only `Read`, `Grep`, `Glob`; prohibit writes, shell execution and network tools. Include the truthful harness `install.py check` result in the prompt. The task is an action plan, not actual implementation or command execution. Do not supply `must` / `must_not` to the subject.
- Interleave before/after runs in a reproducible shuffled order, seed `20261030`. Use opaque sample names so paths do not reveal the arm. Keep project settings and source inputs identical except for the intended skill bodies and unavoidable per-run paths/pin hashes.
- Check project inventories before and after every run. A file write, rubric exposure, model mismatch, environment failure or unusable grading is `INVALID`, not `FAIL` or `PASS`. Retain the invalid run and reason; do not silently replace it.

## Runner work still needed

**There is no ready-to-run paired Claude runner in this branch.** The interrupted Codex-subject draft was removed because it targeted the wrong subject and had not been tested. Do not invoke the existing runner blindly for this experiment.

`tests/run_behavior_evals.py` is a useful source for Claude read-only invocation, disposable installation and rubric handling, but currently runs both agents, grades Codex with Claude, reads cases from each bundle, and writes an old hard-coded preview.5 commit label. Those behaviors do not implement this comparison. Add a separate paired runner or explicit paired-mode options that:

1. Read the frozen selection, verify its hash and the exact source commits, and prepare both decontaminated bundles as above.
2. Support a **prepare-only** mode that performs no model calls. Verify installation, fixture equality, allowed source differences, sample ordering and absence of answer keys. Do this first on the home machine.
3. Use Claude only as subject, with an explicit model/effort. Preserve per-item Codex grading booleans and derive PASS from all `must=true` and all `must_not=false`; require actual booleans and exact item correspondence. A grader response without these is invalid.
4. Disable grader tools and use an empty isolated working directory. Supply only fixture, rubric and one untrusted answer as grading data. Check the actual transcript for tool use or leakage.
5. Save each result immediately, so interruption preserves completed runs. Resume must never rerun completed PASS/FAIL or silently mix model/fixture/manifest identities. Do not automatically retry invalid runs.
6. Keep prompts, raw answers and CLI transcripts **outside the repository**. Repository results contain source/model identities, item outcomes, usage, hashes, validity checks and limitations, not raw conversations or reconstructed answers.
7. Produce a three-row before/after table with PASS/FAIL/INVALID counts, per-item misses and all three repetitions. Do not stop early on favorable results or edit the skills during the comparison.

The existing runner's `--setting-sources project` did not exclude the user-level `CLAUDE.md` in the original run. Verify and record the actual home-machine instruction context; use the same context for both arms. Do not claim user instruction isolation from that flag alone. If the exact old served model is unavailable, label this a new-model comparison, not a reproduction of the original failures.

## Interpretation and next decision

This is a **post-hoc diagnostic**: the candidate was already written before these cases and repeats were frozen. The three cases also overlap the incidents motivating the change. It does not meet the procedure's full pre-registered adoption comparison or broader regression requirements.

- Report whether the observed sample improved, regressed or stayed unchanged; three repeats cannot establish a general reliability gain.
- If before and after both pass 3/3, report **no observed improvement / ceiling**, not that the fix was effective.
- FI-S02's historical FAILs cannot be used as the before scores for this corrected-fixture comparison.
- A plan mentioning tests does not prove actual tool order. State this limitation.
- Keep historical results unchanged. Do not change skill text to chase failures inside this run. Any follow-up hypothesis requires a separately frozen experiment.
- Leave adoption, rejection, a new preview release and any merge to the user. No automatic publication.

## 집에서 이어가기

```powershell
git fetch origin
git switch --track origin/codex/claude-skill-ab-experiment
```

이미 로컬 브랜치가 있으면 `git switch codex/claude-skill-ab-experiment`를 사용한다. 작업 트리에 변경이 있으면 먼저 보존한다.

다음 요청을 그대로 전달하면 된다:

> 이 브랜치의 docs/eval-results/2026-10-30-skill-comparison/README.md와 selection.json을 읽고 실험을 이어서 진행해줘. Claude를 평가 대상으로, Codex를 독립 채점자로 사용해 세 사례를 수정 전후 각각 3회 비교해. 먼저 paired runner를 완성하고 모델 호출 없는 prepare-only 검증을 해줘. Claude의 실제 사용 가능한 모델과 effort를 양쪽에 동일하게 고정하고 설정을 기록한 뒤, 18회 행동 실행과 최대 18회 채점 안에서 실행해. 원답변은 저장소 밖에 두고 결과와 한계만 저장소에 남겨. 자동 재시도·스킬 추가 수정·병합·출시는 하지 마.

현재 상태: 스킬 수정 `721e086`의 관련 자동 테스트 44개, 양 언어 설치 및 77개 사례 구조 검사는 통과했다. **이번 전후 모델 비교는 0회 실행**이며 새 PASS나 개선 결론은 없다.
