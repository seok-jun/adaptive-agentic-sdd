---
name: implementing-issues
description: 이 프로젝트의 승인된 작업 항목(Issue)을 Issue 번호나 명시한 Issue 참조로 받아 명시한 모듈 경계 안에서 구현한다. 사용자가 기존 Issue의 진행·구현·작업·마무리를 요청할 때 사용하며, Issue 기준 실행, 토큰 효율적 탐색, SDD gate, 병렬 격리, 범위 제한 수정과 검증을 적용한다. 새 Issue만 작성할 때는 사용하지 않는다.
---

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `W`(고정 절차 사본 `P/.adaptive-sdd/workflow`), `M`(고정 공통 원칙 `P/.adaptive-sdd/methodology`)이다. cwd나 W의 상위 디렉터리로 P/M을 추정하지 않는다. P의 hard guard(`P/AGENTS.md`의 `## 항상 적용 hard guard`)와 적용 선언(`P/.adaptive-sdd/project/sdd-workflow.md`)을 적용한다. Issue·댓글·라벨·PR 표현은 `P/.adaptive-sdd/project/tracker.md`가 선언한 작업 관리 방식(`W/tracker/`)으로 바꿔 읽는다.

# Implementing Issues

## Issue dispatch

Issue 번호 또는 명확한 기존 Issue가 주어지면:

1. 전체 open Issue 목록보다 그 Issue의 현재 body/labels를 먼저 읽는다.
2. Issue를 primary execution specification으로 사용한다.
3. Priority, grade, blockers, allowed/forbidden, acceptance criteria, Visual Spec, shared-contract refs만 작업 컨텍스트로 유지한다.
4. Issue가 이미 결정한 요구를 다시 탐색하거나 사용자에게 재입력시키지 않는다.

Epic 관리 문서가 주어지면 `managing-issues`의 `Epic 조율`로 작업 구성·의존성을 갱신하고 실제 요청된 하위 실행 Issue에 dispatch한다. 관리 문서 자체에 구현 claim·실행 grade·AS-IS/PLAN/BREAKDOWN 리뷰를 요구하지 않는다. 아직 하위 작업이 없으면 필요한 만큼 정의하고 조사할 수 있으며, 분해 PASS를 기다리지 않는다.

## Inputs

현재 run에서 `P/AGENTS.md`의 `## 항상 적용 hard guard`가 적용됐음을 보장할 수 있으면 재독하지 않는다. 보장할 수 없는 standalone/subagent 진입이면 그 section을 먼저 읽고 진행한다.

필수:

1. Current Issue body/labels
2. `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)
3. Issue와 직접 연결된 business/architecture 문서
4. target code, direct public contracts, direct callers/callees

조건부:

- Issue `Execution Profile`, phase routing, model/reasoning 선택 또는 worker handoff를 실제로 판정할 때 `W/skills/_shared/execution-routing.md`를 읽는다. 이 shared contract는 fixed pre-read 입력이 아니다.
- claim/isolation은 `W/skills/parallel-development/SKILL.md`를 적용한다. 같은 run에서 이미 확인한 Issue 경계와 metadata를 전달해 재사용한다.
- Issue가 shared/root/integration 경로를 참조하거나 현재 코드가 Issue 경계를 넘을 가능성이 생길 때만 `W/process/module-boundaries.md`의 공통 경계·lifecycle 계약과 `P/.adaptive-sdd/project/module-boundaries.md`의 실제 제품 경계를 읽는다.
- instruction conflict, code↔business drift, 승인된 scope로 판정할 수 없는 상황에서만 `W/process/agent-instruction-policy.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/agent-instruction-policy.md` (제품 적용·권한·검증)를 읽는다.

무관한 domain이나 process 문서를 일반 프로젝트 이해 목적으로 읽지 않는다.

## Preflight

1. Issue에 Priority/grade, 사용자 영향, 목표, 작업 범위, allowed/forbidden, 완료 기준, dependencies가 있는지 확인한다.
2. body Priority/grade와 labels가 일치하는지 확인한다.
3. 현재 Priority와 사용자 지시상 구현 가능한지 확인한다.
4. dependencies/blockers가 어느 단계에 필요한지 확인한다. 상위의 미결 사항 자체로 하위 조사를 막지 않고, 그 결론을 필요로 하는 구현·통합·배포만 기다린다. 실제 접근·사람 판단 등 현재 조사 자체의 조건은 유지한다.
5. Issue의 allowed/forbidden 경계를 확인한다.
6. `parallel-development` claim 절차를 완료한다.
7. grade에 맞는 SDD gate를 적용한다.
8. `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 `Token diagnostic mode`가 `ENABLED`이고 authoritative goal tracker 값이 있으면 실제 작업 직전에 `[WORKFLOW][TOKEN START]`를 한 번 기록한다. 기존 START가 있으면 재기록하지 않는다.
   같은 실제 변경 전 경계에서 `차세대 방법론의 적용과 개선 관측` 절을 적용한다. 고정 문서·버전과 지원·적용 구간, 이전 관측의 실제 읽기/사용 판단, Issue 보존 위치를 작업별 시작 기록 한 곳에 남긴다. 재개·인계는 그 원본을 직접 참조하고 변경·새 관측만 덧붙인다. 접근 가능과 실제 읽기를 구별하며 새 작업의 읽기·비용·모델 관측을 이전 작업에서 상속하지 않는다. tracker unavailable이면 TOKEN checkpoint만 생략하며 다른 관측을 생략하지 않는다. 문서 미조회·pin 불일치는 적용 미확인으로 남기고 기존 제품 절차의 허용 범위에서 계속한다.
9. routing이 필요한 **현재 phase**면 grade로 orchestration shape를 고정하고 phase risk로 minimum model/reasoning tier를 정한 뒤 `W/skills/_shared/execution-routing.md`의 current/manual vs automatic route 규칙을 적용한다. 이미 실행 중이거나 사용자가 현재 phase에 명시적으로 선택한 current/manual model은 canonical DENY와 실제로 존재하는 explicit qualification record를 확인하고 fresh Host Capability evidence로 floor를 증명한다. positive qualification record가 없다는 사실만으로 차단하지 않는다. Agent가 model switch/delegated worker/reviewer/fallback을 자동 선택할 때는 해당 role의 fresh qualification PASS가 필요하다. 아직 진입하지 않은 future phase의 concrete model PASS는 현재 phase preflight의 선결 조건으로 요구하지 않는다. capability를 증명할 수 없으면 `BLOCKED: routing capability unavailable`, 자동 후보가 모두 부적격이면 `BLOCKED: model role unqualified`을 적용한다.

실패하면 제품 코드를 수정하지 않는다.

## SDD gate

작업 중 실제 문제를 발견하면 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 `문제 발견 시 기록과 종료 연결`을 적용한다. Trivial/Small도 기존 Issue 작업 댓글을 사용하고 정상 진행에는 사건 기록을 추가하지 않는다. worker/reviewer의 발견 내용은 기존 결과 인계로 받아 원본 참조를 보존한다. 해결됐더라도 최초 문제·담당 metadata·조치/결과를 종료 담당자에게 전달하며 새로운 SDD나 승인 gate를 만들지 않는다.

- Trivial: 별도 `P/docs/sdd/**` 없이 진행. 먼저 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 Trivial 조건을 모두 만족하는지 확인하고, 조건을 벗어나면 수정 전에 최소 Small로 재판정한다.
- Small: 별도 `P/docs/sdd/**` 없이 진행.
- Medium: 필요한 SDD를 작성하고 conflict가 없으면 추가 승인 없이 계속.
- Large: AS-IS와 PLAN 각각 아래 required review의 다음 phase 진행 조건을 만족해야 다음 단계로 간다. 사람 승인 단계는 없으며 사람 판단 지점은 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 `사람 판단 지점`을 따른다.

grade gate와 실행 routing은 다른 축이다. Trivial/Small은 Profile과 무관하게 single-agent/no-switch가 기본이다. 다만 current concrete model이 role DENIED이면 actor 수를 늘리지 않고 qualified replacement 한 명으로 교체한다. Medium은 unresolved PLAN decision 또는 required review phase만 bounded delegation한다. Large는 검토를 통과한 설계와 경계를 root가 소유한 상태에서만 `PLAN / IMPLEMENT / REVIEW` coarse-grained phase 위임을 허용한다. Epic 소속 여부로 actor 수·병렬 실행·리뷰를 추가하지 않고 각 실행 Issue의 grade와 phase를 따른다.

파일 존재나 오래된 review, 일반 Agent 댓글의 합의를 Human Decision으로 추정하지 않는다. 상세 코드 정합성은 Agent와 grade별 review가 책임진다. 문서 역할·적용 시점·상세 검증 기준은 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)가 Source of Truth다.

### Remote review candidate gate

Large AS-IS와 PLAN은 초안 작성 중 local commit을 허용하지만 independent review candidate가 되는 시점에는 다음을 모두 확인한다.

1. candidate를 현재 Issue branch에 commit하고 같은 branch를 remote에 push한다.
2. exact candidate SHA가 remote branch history에서 resolve되고, reviewer가 local worktree path 없이 Issue 번호, remote branch, SHA와 artifact 경로만으로 원문을 읽을 수 있는지 확인한다.
3. required review/PASS는 그 remote-resolvable exact SHA를 target으로 사용한다.
4. finding 반영으로 review-affecting artifact가 바뀌면 새 commit을 push하고 새 SHA에서 영향 판정에 따른 required review와 재확인을 수행한다. 이전 SHA PASS를 자동 승계하지 않고 current-target chain을 연결한다.

push 실패, remote branch에서 exact SHA 확인 실패 또는 remote artifact 조회 실패 시 local-only 원문이나 Issue comment 재서술로 fallback하지 않고 상태를 반드시 `BLOCKED: SDD candidate remote push failed`로 기록해 중단한다. remote Issue branch와 exact SHA만으로 publication은 충분하다. 이 단계에서 PR이나 draft PR을 새로 만들지 않으며, 기존 PR이 없더라도 그대로 review handoff를 진행한다. 이 gate 때문에 기존 lane을 재생성·자동 rebase하거나 Medium 이하에 새 gate를 추가하지 않는다.

### Large dual design review gate

Large의 AS-IS와 PLAN 최초 candidate에는 같은 remote-resolvable exact candidate에 다음 review를 순서대로 수행한다. 이후 revision은 7번의 영향 판정과 current-target 재확인 chain으로 다음 phase 전 review 유효성을 증명한다. Trivial/Small/Medium 또는 기본 CODE review에는 Review B를 추가하지 않는다.

1. **Review A — Contract Review**: author와 다른 agent/session에 phase-aware Contract Review Packet을 전달한다. Issue/acceptance, phase artifact, reviewed upstream contract, direct caller/callee·invariant·allowed/forbidden과 applicable evidence의 correctness/consistency만 bounded하게 검토한다. blocking finding은 보정 후 A re-check한다.
2. **Review B — Blind Audit**: A가 통과한 뒤 Human이 선택한 model + reasoning을 사용한다. 선택 전에는 임의 reviewer를 배정하지 않고 `BLOCKED: blind-audit reviewer selection required`로 중단한다. 선택된 reviewer가 canonical REVIEW floor/role qualification을 만족하지 않거나 host에서 unavailable이면 자동 fallback하지 않고 `BLOCKED: selected blind-audit reviewer unavailable`로 중단해 Human 재선택을 요청한다.
3. B는 author와 Review A actor/session 모두와 다른 별도 agent/session에서 `review-mode = blind-audit`으로 실행한다. Human model 선택은 이 분리, mode 또는 capability floor를 완화하지 않는다.
4. B 최초 verdict 전에는 A의 PASS/BLOCKED verdict, finding 목록, detailed packet 또는 이전 B finding detail을 전달하지 않는다. shared routing의 최초 Blind Audit Packet만 주고 omission, hidden assumption, scope/ownership boundary-changing risk를 찾게 한다. solution implementation이나 repository-wide redesign을 요청하지 않는다.
5. 최초 verdict가 고정된 뒤에만 같은 B reviewer에게 이전 B finding identity와 resolution expectation ledger를 제공한다. 이전 finding마다 현재 exact candidate에서 `resolved / unresolved / regressed / not-applicable`과 직접 근거를 남기고, 최초 verdict의 신규 finding과 ledger reconciliation을 분리한다. 이전 B finding이 없으면 reconciliation은 해당 없음으로 명시한다.
6. B finding은 `Human Decision blocker / Execution-contract blocker / Implementation finding / Non-blocking observation` 중 하나로 분류한다. PLAN blocker는 severity, 깨지는 artifact/상위 contract/direct-boundary invariant, 다음 phase 전에 해결하지 않을 때 구현자에게 남는 의미 선택 또는 충돌하는 결정 의미를 모두 설명해야 한다. 이 qualification이 없고 code+fixture에서 contract-preserving 정답 하나로 수렴하면 `Implementation finding`이다.
7. unresolved Human Decision blocker 또는 unresolved Execution-contract blocker가 하나라도 있으면 다음 phase를 중단한다. SHA 변경 뒤에는 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 `의미·영향에 따른 설계 재검토`를 적용한다. 기존 Review Packet에 target 차이·전체 inventory·finding·직접 영향·current-target 근거를 연결하고 국소 변경은 관련 판단만 재확인한다. 핵심 Decision/상위 계약/경계/감사 전제 변경 또는 영향 불명확이면 무효화된 phase를 확장 검토하고 새 독립 blind B를 수행한다. 새 최초 verdict에는 A 결과와 이전 B detail을 숨기고 고정 후 reconciliation한다. 후속 재확인을 최초 blind로 기록하거나 이전 PASS를 자동 승계하지 않는다. 같은 영역의 충돌이 수정·재확인 뒤 2회 연속 남으면 다음 자동 리뷰 전에 canonical `반복 정체 시 전환`을 적용하고 blocker를 유지한다.

`Human Decision blocker`는 확정된 상위 contract/Decision 충돌, 제품 의미·ownership·failure behavior·acceptance 해석의 경쟁 선택, 기존 Human Decision scope 변경 또는 새 중요한 Decision이 필요한 경우다. 기존 `[HUMAN DECISION REQUIRED]`를 사용하며 새 결정 taxonomy를 만들지 않는다. `Execution-contract blocker`는 Human 제품 판단 없이도 복수의 합리적 기술 선택이 public/internal contract, persistence lineage, eligibility, schema mapping, recovery convergence 또는 scope 의미를 바꾸는 경우다. 이를 해결할 때 Human Decision을 불필요하게 늘리지 않고 change-plan execution contract와 fixture expectation에 한 방향을 고정한다.

`Implementation finding`은 확정된 Decision/contract/scope를 바꾸지 않고 정답이 하나인 caller/fence/race-fixture/mechanical defect다. finding 기록만을 위한 PLAN artifact revision을 강제하지 않고 Result/Review Packet 또는 동등한 IMPLEMENT handoff에 identity와 resolution expectation을 보존한다. `Non-blocking observation`은 향후 최적화·선호·추가 방어·현재 acceptance 밖 개선이며 PLAN/IMPLEMENT gate로 승격하지 않는다.

A가 current exact candidate에서 PASS하고 B initial blind audit 및 필요한 current-target 재확인 chain/reconciliation이 완료됐으며 unresolved Human Decision blocker와 unresolved Execution-contract blocker가 각각 0일 때만 다음 phase로 진행한다. Implementation finding과 Non-blocking observation의 개수는 이 PLAN gate를 막지 않는다. review round나 finding 개수 상한으로 PASS를 강제하지 않는다. IMPLEMENT/CODE는 기존 independent code review 1회를 유지하고 destructive migration, cross-DB atomicity, recovery 같은 명시적 high-risk escalation에서만 추가 code audit을 허용한다.

### 재검토 dispatch 전 target 유지 확인

먼저 기존 review target과 current head의 전체 변경 inventory, 해당 phase artifact inventory·bytes, Decision scope·upstream·직접 소비자/감사 전제를 대조한다. 기록/head-only이고 모두 불변이면 기존 target과 A/B 근거를 유지한다. 새 SHA를 만들었다는 이유로 target을 최신 head로 옮기거나 A/B를 반복하지 않는다. 기록 오류는 원본을 보존한 채 보정한다.

artifact 변경이면 canonical 의미·영향 표를 적용한다. 국소 보정은 invalidated 판단·finding·직접 영향만 독립 재확인하고, A의 보정 및 PASS가 고정된 candidate에 대해서만 B를 dispatch한다. A가 수정 중인 candidate에 B를 미리 실행하지 않는다. 핵심 Decision/상위 계약/경계/복구/감사 전제 변경 또는 영향 불명이면 A 이후 새 blind B가 필요하다. 새 target의 구조화 A/B 근거는 current-target 재확인 결과를 기록하며 과거 PASS의 target만 치환하지 않는다. 최초 검토와 reviewer 분리·B 선택·blind isolation은 그대로 유지한다.

### 사람 판단 지점

P 적용 문서 `P/.adaptive-sdd/project/sdd-workflow.md`의 `사람 판단 지점`을 직접 확인한다. M `core.md`의 `사람 판단` 요건은 이 선언으로 면제되지 않는다.

## Determine as-is and to-be

상위·관련 작업의 분석은 `W/process/sdd-workflow.md`의 `기존 분석 재사용`에 따라 기준 revision·적용 범위·전제·직접 근거를 확인해 이어 쓴다. 유효한 조사는 참조하고 부족하거나 바뀐 부분만 조사하며, 그 사실만으로 해당 grade의 검토를 면제하지 않는다. 함께 검토할 공통 변경은 소비 작업·호환성·전환 영향까지 담당 Issue의 범위와 검증에 포함한다.

1. 현재 `main` code = observed as-is.
2. current Issue = requested to-be.
3. 직접 관련된 `P/docs/domains/**`만 code와 비교한다.
4. business drift만으로 기능을 과거 문서에 맞추지 않는다.
5. Issue와 architecture/acceptance criteria가 충돌하면 `agent-instruction-policy.md`를 확인하고 해소되지 않으면 `BLOCKED: instruction conflict`로 중단한다.

Trivial은 제품 AS-IS discovery를 확장하지 않는다. 대상 text/metadata와 직접 연결된 검증 근거만 확인한다.

## Design and verification gate

제품 파일 수정 전에 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)에 따라 다음을 완료한다.

1. 기준 revision의 요구와 각 Acceptance Criterion의 적용 진입점·조건·기대 결과를 실제 필요한 unit/integration/lint/build/CI와 grade별 review 근거에 대응시킨다. workflow의 Verification Strategy에 따라 기존 계획을 재사용하고 누락된 대응만 보완한다. 복수 진입점 중 하나의 검증으로 전체 충족을 대신하지 않는다.
2. Medium 이상은 `02-to-be.md`를 Human Decision Contract로 작성하고 완료 기준별 Verification Strategy를 유지한다. 상세 path/symbol/caller/invariant·실행 순서·test/명령/evidence는 Agent Execution Spec인 `change-plans`로 이관하고 `D-xxx`를 참조해 rationale을 중복하지 않는다. Small은 기존 검증 기준만으로 증명할 수 있으면 별도 문서를 만들지 않는다. Trivial은 별도 문서 없이 변경 종류에 맞는 targeted validation을 정한다.
   현황·계획 등 사람용 설명에는 [사람용 문서의 시각적 작성](../../process/agent-instruction-policy.md#사람용-문서의-시각적-작성)을 적용한다. 현재/변경 모습·선택을 먼저 보여주고, 비교·소유/경계·흐름/상태 중 필요한 관계를 표현한다. 단순 변경은 한 문장으로 충분하다. 전체 가이드/예시를 선행 로딩하거나 그림 수·새 승인 단계를 요구하지 않으며 이미 적용한 같은 기준은 재사용한다.
3. `Independent Review: REQUIRED | NOT REQUIRED`를 판정한다. Trivial은 항상 `NOT REQUIRED`다.
4. Device QA / Runtime QA를 판정하거나 handoff하지 않는다. 선택적 기기 확인은 P가 기기 확인 문서를 선언했으면 참고할 수 있지만 구현/PR/merge gate에 포함하지 않는다.
5. grade별 design review gate를 통과한다. Large AS-IS/PLAN은 최초 Review A와 Human-selected blind B 및 필요한 current-target 재확인 chain이 유효하지 않으면 다음 phase로 진행하지 않는다.
6. phase risk가 destructive/shared-contract/migration/security/authority/recovery/atomicity PLAN이면 grade와 무관하게 `strong + extra-high` floor를 적용한다. `frontier`는 명시된 고위험 evidence가 strong에서도 unresolved일 때만 bounded candidate이며 compile failure, command typo, fixture correction은 escalation 근거가 아니다.
7. Issue에 optional `## Execution Profile`이 있으면 phase별 tier/concrete model과 explicit fallback을 routing input으로만 사용한다. Profile이 없으면 current execution model/reasoning을 유지하되 current/manual eligibility를 shared routing contract로 검증한다. Profile 때문에 model switch/delegation이 생기면 fresh role qualification PASS를 요구한다. Profile로 hard guard·SDD·boundary·verification·review·canonical deny를 완화하지 않는다.
8. P 적용 문서 `execution-routing.md`가 선언한 safety deny 모델은 standalone owner, PLAN/IMPLEMENT/TEST_DOCS worker, independent reviewer, finishing/lifecycle owner에서 DENIED다. `current`, cheap mapping, explicit profile, fallback은 이를 덮어쓰지 않는다.
9. 차단 model qualification probe는 별도 probe Issue, 명시적 사용자 지시, synthetic/docs-only fixture, orchestrator-owned claim/isolation/lifecycle, main push와 Issue/PR/merge/release 권한 금지, raw observation 보존 조건을 모두 갖춘 bounded `qualification_probe` 역할에서만 허용한다. 일반 제품 Issue에는 예외를 적용하지 않는다.

완료 기준을 증명할 수 없거나 검증이 allowed 경계를 넘어야 하면 제품 파일을 수정하지 않고 `BLOCKED`한다.

Issue/current main/direct dependency 분석 중 실제 경쟁 선택지가 둘 이상 확인된 경우에만 선택, 대안, 이유, 감수 비용을 짧게 기록한다. trade-off 후보를 만들기 위한 repository-wide 탐색이나 brainstorming은 하지 않는다. Trivial/Small에는 별도 trade-off 문서를 만들지 않는다.

## Implement

- delegated phase worker는 `W/skills/_shared/execution-routing.md`의 Execution Packet을 받는다. hard guard 재사용에는 immutable identity가 있는 host-enforced propagation evidence object 또는 worker direct-read evidence object가 필요하다. standalone runtime에서 이를 증명하지 못하면 `runtime_guard_propagation: true`나 `guard applied: true` 같은 boolean을 신뢰하지 않고 필요한 hard guard section을 직접 읽는다.
- current/manual agent가 현재 role을 계속하는 경우 canonical DENY와 실제 explicit qualification record를 다시 확인하고 fresh Host Capability evidence가 phase floor를 충족하는지 확인한다. explicit record가 `DENIED`이거나 존재하는 positive record가 stale/incomplete이면 우회하지 않는다. explicit positive record가 아예 없다는 이유만으로 current/manual route를 차단하지 않는다. Agent가 worker/reviewer/fallback model을 자동 선택하거나 switch하기 직전에는 해당 concrete role의 fresh qualification PASS를 요구하며, 없으면 적격 fallback을 찾거나 `BLOCKED: model role unqualified`로 중단한다.
- Execution Packet의 required field, nested/nonempty 값, SDD gate/claim evidence, canonical provenance, Issue/PLAN/direct-contract freshness와 명시적 `implementation_findings` list를 첫 edit 전에 검증한다. 검토를 통과한 PLAN에 handoff item이 있으면 identity, PLAN exact target과 resolution expectation이 모두 있어야 한다. guard application을 포함한 evidence 누락·빈 값·형식 오류는 `INVALID`, current source와의 identity/freshness 충돌·version mismatch는 관련 항목만 `STALE`로 둔다. 둘 다 fail-closed하고 필요한 hard guard direct read 또는 bounded refresh 후 새 provenance로 증명할 수 없으면 `BLOCKED`한다.
- native delegation이 없더라도 fresh evidence가 current model의 IMPLEMENT floor 충족을 증명하면 current agent가 직접 수행한다. required independent REVIEW는 이 fallback과 무관하게 구현 주체와 분리한다.
- Medium/Large에서 required reviewer를 별도 agent/session으로 제공할 수 없으면 valid trace를 만들지 않고 `BLOCKED: separate reviewer unavailable`로 중단한다. Large AS-IS/PLAN Review B는 Human 선택 전 임의 route하지 않고, 선택 reviewer unavailable/부적격 시 automatic fallback하지 않는 전용 stop condition을 우선 적용한다. future reviewer의 concrete model qualification은 PLAN/IMPLEMENT 시작 전에 미리 요구하지 않고 실제 reviewer actor를 선택하는 시점에 shared routing contract로 검증한다.
- product file은 Issue allowed에 매칭되고 forbidden에 매칭되지 않는 path만 수정한다.
- root/shared integration-only path가 필요해지면 직접 수정하지 말고 `module-boundaries.md`를 확인해 integration dependency로 전환한다.
- lifecycle artifact는 해당 절차가 허용한 범위만 변경한다.
- acceptance criteria 밖 동작, refactor, rename, formatting, dependency, feature를 추가하지 않는다.
- 작업 지시·확정된 설계 범위를 벗어나는 새 중요한 제품/설계 Decision은 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)에 따라 `[HUMAN DECISION REQUIRED]`로 올리고 영향 작업을 STOP한다. 사람 결정을 Human View와 필요한 Issue 본문에 반영한 뒤 재개한다. 일반 Agent 합의로 결정하거나 change-plan에만 결정을 두지 않는다. Decision 노출 자체는 추가 gate가 아니며, 확정된 의미·불변조건을 바꾸지 않는 실행 세부는 Agent가 계속 처리한다.
- allowed path 안의 직접 regression test를 추가/수정한다.
- 검토를 통과한 PLAN에 `Implementation finding` handoff가 있으면 Result Packet까지 identity와 resolution expectation을 보존하고 각 항목의 code와 fixture/test 해결 evidence를 current head에 결합한다. 한쪽 근거가 없거나 handoff item이 누락되면 구현 완료로 넘기지 않는다. `Non-blocking observation`은 별도 구현 gate로 승격하지 않는다.
- `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 verification-affecting input을 changed file에서 식별하고 실제 path의 owning 빌드 모듈(P 적용 문서 `build.md`의 모듈 단위)을 기본 선택 검증 단위로 사용한다. test 이름에 다른 domain 용어가 있어도 파일이 위치한 module의 소유권을 바꾸지 않는다.
- 구현 루프에서는 직접 관련 test class 또는 owning-module test를 먼저 실행한다. 여러 module 변경은 changed module을 검증하고, public/behavioral contract의 immediate consumer, Issue Verification Strategy의 명시 범위, 구체적 compile/test failure로 증명된 direct-impact module까지만 확장한다. transitive consumer를 찾기 위한 repository-wide 추측은 하지 않는다.
- targeted verification 실패는 전체 suite보다 실패 test 또는 owning module부터 수정·재실행한다. P 적용 문서 `build.md`가 선언한 계측·기기 테스트 경로는 Issue Verification Strategy나 repository command contract의 명시적 요구가 있을 때만 기본 targeted 범위에 포함한다.
- UI Issue의 required Visual Spec은 Issue에 고정된 immutable permalink를 사용한다.
- targeted verification 뒤 diff ↔ Issue/Verification Strategy self-review를 수행한다.
- TEST_DOCS와 finishing handoff도 shared routing contract의 current/manual vs automatic qualification 규칙을 적용하며 safety deny 모델에 lifecycle ownership을 넘기지 않는다. qualification probe model에는 main push, Issue/PR lifecycle, merge/release 권한을 포함한 Result Packet을 만들지 않는다.
- Trivial은 실행 코드·테스트 기대값·build/dependency·schema·contract·CI/workflow 실행 의미를 바꾸지 않는다. 필요해지면 즉시 최소 Small로 재판정한다.

### PLAN → IMPLEMENT handoff

`W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 `PLAN 확정 뒤 구현 문맥 인계`와 shared Execution Packet을 적용한다. 현재 Issue/PLAN·review 근거·경계·확정 결정과 이유·실패/복구·implementation finding·검증 의무를 최소 입력으로 연결한다. 지원 host에서 별도 구현 문맥 또는 검증된 압축을 사용하며 같은 모델이라는 이유로 큰 설계 이력을 기본 상속하지 않는다. 수신자는 guard/claim/direct source 최신성을 첫 edit 전에 확인한다.

전환 방법·실행 evidence와 입력 참조를 기록한다. 미지원/압축 실패는 직접 구현 fallback의 사유·최소 입력·남은 문맥 한계를 명시하고 수행하지 않은 분리를 성공으로 기록하지 않는다. INVALID/STALE 또는 압축 중 필수 근거 유실은 bounded refresh 후 VALID가 되기 전 구현을 막는다. root에는 compact Result Packet을 반환하며 전체 worker 로그를 재합치지 않는다. 이미 IMPLEMENT 중인 lane을 소급 초기화하지 않는다.

## Token-efficient execution

- P가 영향 분석 도구를 선언했으면 검증 범위 선정 시 shared routing의 `공통 영향 결과 참조와 로컬 소비`를 적용한다. 그 도구의 현재 결과를 기존 required verification에 연결하고, 결과가 stale/불완전하면 재계산 또는 전체 검증으로 확장한다. 자체 경로 매핑을 만들거나 영향 집합으로 Issue·grade 필수 명령을 삭제하지 않는다. 변경분 재리뷰·관측도 같은 참조 계약을 사용한다.
- Issue가 이미 정한 결정을 다시 product discovery하지 않는다.
- direct path/symbol에서 시작하고 repository-wide 탐색은 concrete dependency/compile failure가 있을 때만 확장한다.
- 같은 run에서 읽은 변경 없는 Issue/정책/source와 이미 확보한 GitHub Issue/PR metadata는 아래 invalidation trigger가 없으면 재조회하지 않는다.
  - Large AS-IS 또는 PLAN candidate를 새 commit으로 push해 review target SHA가 바뀜
  - 현재 lane의 push로 PR head SHA가 바뀜
  - 현재 run에서 Issue/PR을 merge·close·reopen하거나 label/assignee/state를 변경함
  - base ref 또는 base SHA 변경 근거가 확인됨
  - webhook/wake, 외부 tool result, GitHub 상태 변경을 알리는 사용자 지시 같은 외부 상태 변경 신호를 받음
  - merge 직전 또는 merge 후 closure 확인 직전 lifecycle boundary에 도달함
- 상태·라벨·mergeability·head/base SHA만 필요하면 metadata-first로 조회하고 host/tool이 지원하는 metadata 전용 또는 field 한정 조회를 우선한다. invalidation 뒤에도 그 시점의 판정에 필요한 metadata만 갱신하고 full body/comments/diff로 자동 escalation하지 않는다.
- full Issue/PR body·comments·diff는 그 내용 자체가 판단 근거일 때만 읽는다. 방금 자신이 작성한 Issue/PR 본문을 상태·mergeability·라벨·head/base 확인 목적으로 재조회하지 않고, metadata 조회 뒤 무조건 full read하는 이중 호출도 만들지 않는다. metadata로 안전하게 판정할 수 없으면 필요한 범위만 escalation하고 token 절감보다 correctness를 우선한다.
- 개발 중에는 owning/direct-impact module의 targeted verification을 먼저 실행하고 root aggregate 같은 required broad command set은 diff와 review finding이 안정화된 stable final candidate에서 실행한다. Issue가 명시한 더 넓은 검증은 이 최적화보다 우선한다.
- final self-check는 repository 재탐색 대신 diff ↔ Issue boundary/acceptance criteria를 비교한다.
- worker는 full reasoning/전체 log 대신 base/head, 전체 changed-file inventory 또는 immutable reference, diff reference, criterion outcome, commit-bound verification evidence, scope drift, unresolved/escalation 상태, compact summary, new dependency, freshness issue를 포함한 Result Packet을 반환한다.
- Result Packet의 verification command/exit/outcome만으로 PASS를 증명하지 않는다. immutable evidence identity가 실행 commit에 결합되고 Result head와 같아야 하며 mismatch는 `STALE`이다.
- token checkpoint는 lifecycle event에서만 tracker를 한 번 조회한다. 값이 없으면 추정·repository 탐색·별도 분석 없이 생략하고 구현 단계별 token 댓글을 만들지 않는다.
- Trivial은 대상 파일과 직접 검증 근거만 읽고 빌드 도구 검증은 변경 영향 근거가 없으면 실행하지 않는다.

## External blocker lifecycle

- START 이후 사용자 입력, 외부 인증, 외부 승인 같은 외부 상태가 필요해 중단하면 명시한 `P/.adaptive-sdd/project/sdd-workflow.md`의 mode 값이 `ENABLED`이고 authoritative goal tracker 값이 있으면 중단 직전에 `[WORKFLOW][TOKEN BLOCKED]`를 한 번 기록한다. blocker는 대화 내용을 재구성할 수 없는 category만 사용한다.
- 동일 blocker가 미해소인 동안 자동 재확인하거나 TOKEN BLOCKED를 반복하지 않는다.
- 새로운 사용자 지시 또는 상태 변경 근거로 실제 구현을 재개할 때만 `[WORKFLOW][TOKEN RESUME]`를 한 번 기록하고 직전 BLOCKED 댓글 URL을 `from`으로 연결한다. 근거가 없으면 재개하거나 RESUME을 기록하지 않는다.
- tracker 값이 없으면 checkpoint만 생략하며 기존 stop condition과 verification 범위를 바꾸지 않는다.

## Verify

`W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 grade/change-scope 검증 기준을 적용한다.

- Trivial은 변경 종류에 맞는 targeted validation과 diff self-review를 수행한다. 빌드 도구 검증은 변경이 그 결과에 영향을 주는 근거가 있을 때만 실행한다.
- 빌드·테스트 명령 전에 `W/skills/_shared/build-preflight.md`를 적용한다. 환경변수가 비어 있다는 사실만으로 dependency 미설치를 판정하지 않는다. 기기·에뮬레이터가 필요한 작업은 P 적용 문서 `build.md`가 선언한 기기 절차만 따르며, 선언이 없으면 수행하지 않는다.
- required local 빌드 검증이면 preflight 뒤 intended process environment에서 빌드 도구의 version 명령(Gradle이면 `gradlew --version`)으로 실제 launcher/daemon JVM major version이 P 적용 문서 `build.md`의 `JDK major`와 같은지 확인한다. usable current Java/`JAVA_HOME`이라는 이유만으로 통과시키지 않는다. 다르면 required command를 실행하거나 canonical PASS로 기록하지 않고, 이미 설치되어 검증 가능한 선언 버전의 JDK를 현재 process에만 주입해 version 확인 후 같은 command를 실행한다. 자동 설치·다운로드·영속 환경 변경은 금지한다.
- 선언과 다른 JVM에서 먼저 발생한 정적 분석/빌드 도구 failure는 product/code regression으로 판정하지 않는다. 선언 버전 JDK에서 같은 required command를 재실행해 결과를 판정하며, 선언 버전 JDK 또는 실제 빌드 JVM을 확인할 수 없으면 `BLOCKED: canonical build JDK unavailable`로 중단하고 미검증을 PASS로 기록하지 않는다. 이 규칙은 원래 빌드 검증이 required인 변경에만 적용한다.
- 같은 run에서 검증한 JDK와 도구 확인 결과는 후속 shell에 재주입하고 탐색·version 확인을 반복하지 않는다.
- `BLOCKED: JDK unavailable`이면 빌드 도구를 실행하지 않는다.
- 성공한 expensive command는 그 command가 소비하거나 assertion하는 verification-affecting input이 바뀌지 않았다면 반복하지 않는다. input이 바뀌면 affected targeted verification부터 재실행하고 stable한 새 candidate에서 invalidated된 required broad command를 다시 실행한다.
- 실행하지 않은 검증은 `미검증`이며 pass가 아니다. 단, grade 규칙상 필요하지 않은 빌드 도구 검증은 미검증 blocker가 아니다.
- 실패 수정이 forbidden path를 요구하면 `BLOCKED`한다.
- handoff 전 changed-file list에 forbidden/unrelated path가 없는지 확인한다.
- PLAN implementation finding handoff가 있으면 current Result/Review Packet에 모든 item과 code+fixture resolution evidence가 있는지 확인한다. 누락·unresolved·stale이면 handoff를 complete로 표시하지 않는다.
- 선택적 기기 확인의 실행 여부나 report를 merge 가능 또는 complete 판정에 사용하지 않는다.

## Handoff

구현/필수 local verification 후 `W/skills/finishing-issues/SKILL.md`를 적용한다. 이미 읽은 Issue/경계/검증 결과를 전달하고 공통 문서를 처음부터 다시 로딩하지 않는다. delegated worker의 Result Packet이 있으면 current head/diff/inventory/evidence identity에 맞는지 검증한 뒤 bounded Review Packet을 구성하며, stale 또는 incomplete packet으로 완료를 판정하지 않는다.

인계·외부 중단에는 workflow의 개선 관측 시작 URL과 현재 관측/원본·수집 공백·다음 조치를 기존 인계에 포함한다. 기존 시작 구간을 보존하며 담당자 변경이나 중간 버전 도입을 전체 작업의 새 적용으로 소급하지 않는다.

## Output

- Issue / grade / gate
- claim / isolation
- changed files
- acceptance criteria
- Verification Strategy / trade-off / review gate
- token diagnostic START 기록 또는 authoritative tracker unavailable
- verification / unverified
- drift / BLOCKED
- routing route / Host Capability Map freshness
- Execution Packet provenance / Result Packet base·head·diff·inventory·verification evidence identity / implementation finding handoff resolution
