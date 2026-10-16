---
name: parallel-development
description: 이 프로젝트의 병렬 agent 작업의 claim·격리·동기화·해제·통합을 관리한다. Issue 코드 수정 전, branch/worktree 생성, 경로 충돌 확인, 공유 contract 처리에 사용한다. Issue 초안만 작성할 때는 사용하지 않는다.
---

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `W`(고정 절차 사본 `P/.adaptive-sdd/workflow`), `M`(고정 공통 원칙 `P/.adaptive-sdd/methodology`)이다. cwd나 W의 상위 디렉터리로 P/M을 추정하지 않는다. P의 hard guard(`P/AGENTS.md`의 `## 항상 적용 hard guard`)와 적용 선언(`P/.adaptive-sdd/project/sdd-workflow.md`)을 적용한다. Issue·댓글·라벨·PR 표현은 `P/.adaptive-sdd/project/tracker.md`가 선언한 작업 관리 방식(`W/tracker/`)으로 바꿔 읽는다.

# Parallel Development

## Inputs

현재 run에서 `P/AGENTS.md`의 `## 항상 적용 hard guard`가 적용됐음을 보장할 수 있으면 재독하지 않는다. 보장할 수 없는 standalone/subagent 진입이면 그 section을 먼저 읽고 진행한다. 공통 policy는 충돌 조건이 없으면 선행 full-read하지 않는다.

필수:
1. Current Issue body/labels에서 `수정 허용` / `수정 금지`
2. Current Issue assignees, latest comments, linked/open PRs
3. 같은 repository의 active claim/PR 중 path overlap 판단에 필요한 metadata

implementing 단계가 이미 Issue 경계와 shared 여부를 확인했다면 그대로 재사용한다.

조건부:
- standalone으로 호출됐거나 allowed path가 P 적용 문서 `module-boundaries.md`의 shared/root 후보(root build/settings 포함)를 포함하면 `W/process/module-boundaries.md`의 공통 경계·lifecycle 계약과 `P/.adaptive-sdd/project/module-boundaries.md`의 실제 제품 경계의 관련 경계를 확인한다.
- 지시/ownership 충돌을 기존 규칙으로 판정할 수 없을 때만 `W/process/agent-instruction-policy.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/agent-instruction-policy.md` (제품 적용·권한·검증)를 읽는다.

Issue에 allowed/forbidden이 없으면 신규 lane을 만들거나 claim하지 않고 issue-management workflow로 정규화한다.

## 신규 lane 생성과 isolation

이 절차는 새 Issue branch 또는 worktree를 만들 때만 적용한다. 신규 lane의 canonical base는 freshly fetched `origin/main`이다. current local HEAD, local `main`, 이전 Issue branch를 implicit base로 사용하지 않는다.

1. 현재 repository와 remote가 예상 대상인지 확인하고, current worktree/branch, dirty 상태, branch/worktree path 충돌을 확인한다. 이 local state는 오염·충돌 safety check에만 사용하며 base 선택에는 사용하지 않는다.
2. Issue allowed path를 active `[CLAIM]`/open PR과 비교하고 shared/root integration-only 경계를 확인한다. overlap 또는 허용되지 않은 shared 경계면 branch/worktree를 만들지 않고 해당 stop condition으로 중단한다.
3. branch/worktree 생성 직전에 현재 shell에서 `git fetch origin main`을 실행한다. 실패하면 `BLOCKED: origin/main fetch failed`로 중단하고, 기존 remote-tracking ref, local `main`, current HEAD로 fallback하지 않는다.
4. fetch 성공 직후 `git rev-parse --verify origin/main`으로 base SHA를 확정하고 작업 근거에 기록한다. SHA를 확인할 수 없으면 branch/worktree를 만들지 않는다.
5. 확인한 base SHA를 explicit start-point로 사용한다.
   - 같은 local clone에서 둘 이상 lane이면 Issue별 branch와 repository-external worktree를 `git worktree add <path> -b <branch> <base-sha>`로 함께 만든다.
   - 독립 cloud clone/sandbox면 추가 worktree를 만들지 않고 `git switch -c <branch> <base-sha>`로 Issue branch를 만든 뒤 sandbox 자체를 lane으로 사용한다.
   - Windows local worktree는 짧은 경로를 선호한다(P 적용 문서 `sdd-workflow.md`의 `worktree root`).
6. 생성된 lane의 HEAD가 기록한 base SHA와 같은지 확인한 뒤, 그 lane에서 아래 Claim 절차를 수행한다.

W·M 고정 사본(`P/.adaptive-sdd/workflow`, `P/.adaptive-sdd/methodology`)은 lane 작업에서 수정하지 않는다.


- fetch 뒤 branch/worktree 생성 사이에 다른 base를 선택하거나 local `main` checkout/pull을 끼워 넣지 않는다.
- 두 agent가 같은 branch에 동시에 commit하지 않는다.
- 이미 생성되어 진행 중인 branch/worktree는 이 규칙 때문에 자동 rebase하거나 재생성하지 않는다. 기존 lane 갱신은 Synchronization 절차만 적용한다.

## Claim

1. Priority와 현재 사용자 지시상 구현 가능한지 확인한다.
2. allowed path를 active `[CLAIM]`/open PR path와 비교한다.
3. overlap이면 `BLOCKED: overlapping lane`.
4. shared/root integration-only path가 필요한 ordinary lane이면 claim하지 않는다.
5. 현재 agent를 assignee로 설정한다.
6. `status:in-progress`를 붙인다.
7. 다음 형식으로 comment한다.

```text
[CLAIM]
agent: <agent-id>
branch: <branch-name>
allowed:
- <path glob>
forbidden:
- <path glob>
```

8. comments/labels/assignees/open PR을 다시 확인한다.
9. 경쟁 claim이 생겼으면 즉시 release하고 code를 수정하지 않는다.

## Synchronization

다른 PR이 `main`에 merge된 뒤 다음 push 전:
1. current main을 fetch한다.
2. rebase 또는 merge한다.
3. Issue allowed path 안에서만 conflict를 해결한다.
4. forbidden/shared path가 필요하면 `BLOCKED`.
5. 영향받은 verification을 다시 실행한다.

## SDD review candidate publication

Large/Epic AS-IS·PLAN independent review candidate는 현재 Issue branch의 exact commit으로 고정한다.

1. 초안 중 local commit은 허용한다.
2. review handoff 직전에 candidate commit을 현재 Issue branch의 remote branch로 push한다.
3. remote branch history가 exact candidate SHA를 포함하고 해당 SHA의 artifact 경로가 remote에서 조회되는지 확인한다. local remote-tracking ref나 작성자의 worktree 존재만으로 remote-resolvable 상태를 추정하지 않는다.
4. Issue handoff에는 Issue 번호, remote branch, phase, exact SHA와 artifact 경로를 기록한다. reviewer의 local path 접근을 요구하지 않는다.
5. finding 반영으로 review-affecting artifact가 바뀌면 새 commit을 push하고 새 SHA에서 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 의미·영향 판정과 current-target 재확인 chain을 적용한다. 이전 PASS를 자동 승계하지 않는다. 기록/head만 바뀌고 검토 artifact inventory·bytes, Decision scope·upstream과 검토 전제가 불변이면 기존 검토 target을 유지한다. branch head 변경만으로 A/B를 다시 요구하지 않는다.

push 또는 remote resolution 확인이 실패하면 상태를 반드시 `BLOCKED: SDD candidate remote push failed`로 기록해 중단하고 local-only review로 fallback하지 않는다. remote branch와 exact SHA만으로 publication은 충분하므로 이 단계에서 PR이나 draft PR을 만들지 않는다. 모든 commit의 즉시 push를 요구하지 않으며, 신규 lane의 freshly fetched `origin/main` base와 기존 worktree/claim lifecycle을 변경하지 않는다. Medium 이하에는 새로운 gate를 만들지 않는다.

## Shared contracts

ordinary lane에서 shared/root change 필요성이 새로 확인되면:
1. 해당 path를 수정하지 않는다.
2. 필요한 contract/symbol/file을 식별한다.
3. `W/process/module-boundaries.md`의 공통 경계·lifecycle 계약과 `P/.adaptive-sdd/project/module-boundaries.md`의 실제 제품 경계의 integration 규칙을 확인한다.
4. integration Issue/선행 변경으로 분리하고 dependent lane을 pause/release한다.
5. shared change merge 후 main을 반영하고 재개한다.

## Release

handoff/중단/merge cleanup 시 먼저 uncommitted/unpushed state, PR 상태, worktree registration, local/remote branch 상태를 기록한다.

- handoff/중단으로 ownership만 넘기는 경우 dirty/unmerged worktree를 제거하거나 force-delete하지 않는다. `[RELEASE]` comment, `status:in-progress` 제거, assignee 제거 뒤 worktree가 유지됨을 별도로 보고한다.
- independent cloud sandbox처럼 등록된 local worktree가 없는 경우에는 상태 기록 뒤 일반 release 절차를 적용한다.
- 제품 반영 완료는 merged PR·closed Issue와 `[PRODUCT COMPLETE]`로 판정한다. local cleanup과 ownership release 상태는 독립적이며 cleanup 실패가 제품 완료를 취소하지 않는다. local cleanup·lane release는 아래 절차를 따른다.

### Merged local worktree cleanup

1. PR이 merged이고 worktree가 clean한지 확인한다. dirty/unmerged이면 제거하지 않고 중단한다.
2. 먼저 no-artifact 예외를 판정한다. 해당 lane에서 로컬 빌드 도구를 실행하지 않았다는 작업 근거가 있고, `git status --porcelain --untracked-files=all --ignored`가 비어 tracked/untracked/ignored 산출물과 사용자 파일이 없음을 확인했으면 빌드 정리를 skip하고 이유·근거를 기록한다. 어느 하나라도 미확인 또는 산출물이 있으면 이 예외를 적용하지 않는다. 예외가 아니면 registration 제거 전 P 적용 문서 `build.md`의 정리 명령을 확인한다. 선언이 없으면 cleanup skip 이유를 기록한다. 있으면 `W/skills/_shared/build-preflight.md`를 적용(같은 run JDK 재사용)하고 worktree에서 그 정리 명령을 실행·기록한다.
3. preflight가 `BLOCKED: JDK unavailable`이면 registration 제거로 진행하지 않고 그 상태로 중단한다. JDK는 resolve됐지만 빌드 정리 실패 또는 cleanup 후 dirty 상태이면 `CLEANUP_BLOCKED`로 중단한다.
4. Windows worktree root는 P가 선언한 `worktree root` 형태의 짧은 경로를 유지한다. removal 전에 command-local `core.longpaths=true`가 유효한지 확인하고 결과를 기록한다. long-path 지원을 확인할 수 없으면 `CLEANUP_BLOCKED`로 중단한다.
5. primary clone에서 force 없이 worktree removal을 실행한다. Windows에서는 `git -c core.longpaths=true worktree remove <exact-path>`를 사용한다.
   모든 worktree에 위 no-artifact 예외와 나머지 정리 보호를 적용한다.
6. removal command 결과와 별도로 다음 두 조건을 각각 확인한다.
   - `git worktree list --porcelain`에 exact path registration이 없다.
   - physical directory가 존재하지 않는다.
7. 둘 중 하나라도 남으면 exact root 아래를 read-only로 측정해 다음 값을 기록한다.
   - 잔여 파일 수와 디렉터리 수
   - 최장 경로와 그 길이
   - worktree registration 상태
   - local/remote branch 상태
8. 소수의 검증된 잔여 파일이나 빈 디렉터리만 canonical worktree root 아래에 남은 경우에만 개별 정리한 뒤 두 조건을 다시 확인할 수 있다. 수천 개처럼 개별 검증이 불가능한 대량 잔여물에서는 다른 recursive delete나 파일별 command/loop로 우회하지 않고 `CLEANUP_BLOCKED`로 fail-closed한다.
9. `[LOCAL CLEANUP]`에 `complete` 또는 `pending`과 registration/physical 확인·branch 상태·근거/재개 조건을 기록한다. complete는 두 부재가 모두 확인된 경우에만 사용한다. cleanup pending도 제품 완료·관측 수집을 막지 않는다. registration 부재와 physical directory 부재가 모두 확인된 뒤에만 `[RELEASE]` comment, `status:in-progress` 제거, assignee 제거를 수행한다. 하나라도 남으면 worktree cleanup과 lane release는 incomplete다. 이후 cleanup 상태만의 갱신은 LOCAL CLEANUP에 남기며 제품 완료 기록을 다시 작성하지 않는다. 사용자 파일 삭제·force removal 금지는 유지한다.

## Output

- claim status / agent / branch
- origin/main fetch 결과 / 신규 lane base SHA
- allowed paths / conflicts
- isolation mode
- shared dependency
- release status
- JDK/빌드 도구 preflight·cleanup·reuse 결과
- Windows long-path 확인 결과
- local worktree registration / physical cleanup 상태
- `CLEANUP_BLOCKED`이면 exact root, 잔여 파일·디렉터리 수, 최장 경로, registration, local/remote branch 상태
