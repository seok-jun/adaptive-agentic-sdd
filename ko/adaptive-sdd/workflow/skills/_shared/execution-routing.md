# execution-routing.md 수행 절차

입력은 명시한 P/W/M 절대 root다. P 적용 문서 `P/.adaptive-sdd/project/execution-routing.md`의 모델 제한·영향 분석·probe 조건을 먼저 확인한다.

# Execution routing과 packet contract

이 문서는 Issue grade와 phase risk를 분리해 host-neutral 실행 route를 정하고, coarse-grained agent handoff의 packet 계약을 정의한다. 관련 route 또는 packet을 실제로 판정하는 phase에서만 읽는다. fixed pre-read 입력은 아니다.

## Source of Truth

우선순위는 `AGENTS.md hard guard > canonical Skill/process > current Issue + reviewed SDD/PLAN > Execution Packet`이다. Execution Packet은 상위 source를 대체하지 않는 derived cache다. 상위 source와 충돌하거나 provenance/freshness를 증명하지 못하면 해당 packet 항목을 실행하지 않는다.

`guard applied: true` 같은 자기신고 boolean만으로 hard guard 적용이나 재사용을 증명할 수 없다. standalone/subagent runtime이 guard 전파를 보장하지 않으면 worker가 `AGENTS.md`의 필요한 hard guard section을 직접 읽는다.

공통 routing/qualification/packet 계약은 W가 소유하고 P가 적용한 프로필·명시 모델 제한·권한·로컬 영향 분석 입력은 P가 소유한다.

## 두 축 routing

grade는 orchestration shape만 정한다.

| grade | orchestration |
| --- | --- |
| Trivial / Small | current agent 한 명이 model switch와 delegation 없이 완료; current concrete model이 role DENIED이면 한 명의 qualified replacement로 교체 |
| Medium | 단일 agent가 기본이며 실제 unresolved PLAN decision 또는 required independent review phase만 bounded delegation |
| Large | root/orchestrator가 검토를 통과한 설계와 경계를 소유하고 `PLAN / IMPLEMENT / REVIEW` coarse-grained phase만 위임 가능 |
| Epic | root/orchestrator가 breakdown/shared contract/dependency graph를 소유하고 구현은 child Issue execution으로 넘김; giant implementation worker 금지 |

phase risk와 decision complexity가 abstract tier를 정한다.

- model tier: `current | cheap | strong | frontier`
- reasoning tier: `current | medium | high | extra-high`
- canonical 문서에 vendor/model 이름을 tier mapping이나 가격 정보로 저장하지 않는다. 단, qualification 전 사용을 막는 canonical safety deny는 stable normalized model identifier를 명시할 수 있다.
- `current`는 capability rank가 아니라 현재 실행 model/reasoning을 뜻한다. capability 비교 rank는 `cheap < strong < frontier`만 사용하고, `current` 선택은 fresh current-model capability evidence가 해당 phase floor를 충족하는지 별도로 판정한다.

| phase/risk | minimum model tier | reasoning tier |
| --- | --- | --- |
| approved mechanical IMPLEMENT | cheap | medium |
| TEST_DOCS | cheap | medium |
| ordinary Large IMPLEMENT | current | high |
| required independent REVIEW | strong | high |
| competing design choice가 남은 PLAN | strong | high |
| destructive/shared-contract/migration/security/authority/recovery/atomicity PLAN | strong | extra-high |
| 위 고위험 phase가 strong에서도 unresolved | frontier candidate | extra-high |

`frontier`는 기본 금지다. 명시된 고위험 escalation evidence와 strong tier에서 해결되지 않았다는 evidence가 모두 있을 때만 bounded candidate가 되며 자동 선택하지 않는다. compile failure, command typo, fixture correction은 risk 승격 evidence가 아니다.

fallback은 다음 순서를 바꾸지 않는다. **이미 실행 중이거나 사용자가 현재 phase에 명시적으로 선택한 current/manual model**과 **Agent가 자동으로 switch/delegate하는 후보**의 qualification 규칙은 구분한다.

1. grade로 orchestration shape를 고정한다.
2. phase risk로 minimum capability floor를 고정한다.
3. current/manual concrete model이면 canonical safety deny와 그 model에 실제로 존재하는 explicit qualification record를 먼저 확인한다. `DENIED`면 사용할 수 없고, explicit record가 존재하지만 stale/incomplete이면 이를 무시해 우회하지 않는다. explicit record 자체가 없으면 positive PASS registry가 없다는 이유만으로 차단하지 않으며, fresh Host Capability evidence가 phase floor를 충족하면 current/manual route를 유지할 수 있다.
4. Execution Profile의 explicit model/tier가 현재 model에서 switch를 요구하거나 Agent가 worker/reviewer/fallback concrete model을 자동 선택하면 해당 development role의 **fresh qualification PASS**가 필요하다.
5. 자동 후보의 tier가 floor 이상이고 fresh role qualification PASS이면 사용한다.
6. explicit fallback이 없거나 부적격이면 floor 이상인 나머지 fresh host mapping을 낮은 적격 tier부터 결정적으로 탐색하되, 각 자동 후보에 fresh role qualification PASS를 요구한다. `frontier`는 기존 escalation evidence 없이 이 fallback에 포함하지 않는다.
7. 자동 선택이 필요한데 capability 후보가 모두 역할 부적격이면 `BLOCKED: model role unqualified`, capability 후보 자체를 증명할 수 없으면 `BLOCKED: routing capability unavailable`이다.

Profile과 fallback은 floor 아래로 downgrade할 수 없다. 존재하지 않거나 지원 여부가 확인되지 않은 concrete model/tier를 추정하지 않는다. **아직 진입하지 않은 future phase의 concrete model qualification은 선결 조건으로 미리 요구하지 않는다.** 해당 phase에서 실제 current/manual model을 확인하거나 switch/delegation 후보를 선택하기 직전에 위 규칙으로 just-in-time 검증한다.

## Host Capability Map

concrete mapping은 runtime 또는 host adapter가 소유하고 canonical Skill은 다음 schema만 소비한다.

- host identity
- supported model tiers
- tier별 concrete model identifier 목록
- current concrete model identifier와 current-model capability
- supported reasoning levels
- native model switching 지원 여부
- native delegation 지원 여부
- separate reviewer/session 지원 여부
- mapping source와 version/immutable identity, freshness

mapping이 없더라도 fresh evidence가 current model의 phase floor 충족을 증명하면 current/manual eligibility 규칙에 따라 계속할 수 있다. native delegation이 없지만 current model이 floor를 충족하면 current agent가 IMPLEMENT를 직접 수행하며, 이 사유만으로 Large 전체를 차단하지 않는다. required independent REVIEW는 IMPLEMENT delegation 지원 여부와 무관하게 구현 주체와 분리된 agent/session에서 수행한다. capability provenance가 stale이면 concrete mapping을 사용하지 않고 fresh current capability evidence를 확인하거나 차단한다.

Host capability는 automatic route의 role qualification을 대신하지 않으며 canonical safety deny를 덮어쓰지 않는다. current/manual route는 위 bootstrap 규칙에 따라 positive qualification record 부재만으로 차단하지 않는다.

Medium/Large/Epic에서 independent review가 required인데 분리된 reviewer agent/session capability가 없으면 valid execution trace를 만들지 않고 `BLOCKED: separate reviewer unavailable`로 중단한다. future reviewer의 concrete model role qualification은 PLAN 시작 조건이 아니라 실제 review actor 선택 직전에 검증한다.

Large/Epic AS-IS/PLAN의 Review B는 예외적으로 Human이 concrete model과 reasoning level을 선택한 뒤에만 route한다. 선택이 없으면 automatic reviewer mapping이나 fallback을 탐색하지 않고 `BLOCKED: blind-audit reviewer selection required`다. 선택값은 `strong + high` 이상의 canonical REVIEW floor, supported reasoning, canonical deny와 independent-reviewer role qualification을 모두 만족해야 한다. 선택된 model/session을 host에서 사용할 수 없거나 부적격이면 silent fallback 없이 `BLOCKED: selected blind-audit reviewer unavailable`로 중단하고 Human 재선택을 요청한다. Human 선택은 `review-mode = blind-audit`와 author/Review A actor 모두와 다른 별도 agent/session 요구를 바꾸지 않는다.

## Model Role Qualification

role qualification evidence는 concrete model identifier, `PASS | DENIED`, 허용 역할 목록, immutable evidence identity와 freshness를 가진다. 대상 역할은 다음과 같다.

- standalone Issue owner
- orchestrator / PLAN owner
- bounded IMPLEMENT worker
- TEST_DOCS worker
- independent reviewer
- finishing / PR / merge / release owner

Model Role Qualification은 **모든 운영 모델을 사전에 등록해야 하는 universal positive allowlist가 아니다.** canonical safety deny와 explicit qualification 결과는 강제 정책이고, Agent가 자동으로 model을 switch/delegate할 때는 fresh PASS가 필요하다.

- explicit qualification record가 `DENIED`면 current/manual/profile/fallback 어디에서도 일반 development role로 사용할 수 없다.
- explicit positive record가 존재하지만 누락·불완전·stale이면 PASS로 추정하거나 그 record를 무시해 우회하지 않는다.
- explicit qualification record가 없는 current/manual model은 canonical DENIED가 아니고 fresh Host Capability evidence가 현재 phase floor를 충족하면 positive registry 부재만으로 차단하지 않는다.
- Agent가 자동으로 선택하는 switch/delegated worker/reviewer/fallback model은 해당 role의 fresh qualification PASS가 없으면 선택하지 않는다.
- future phase의 qualification은 실제 actor 선택 직전에 검증한다. PLAN 시작 시점에 아직 선택하지 않은 reviewer model의 PASS 링크를 요구해 현재 phase를 차단하지 않는다.

제품별 concrete deny와 probe 권한은 P 적용 문서 `execution-routing.md`의 `모델 제한`을 확인한다. 공통 schema나 PASS가 이 제한을 완화하지 않는다.

## qualification probe 예외

조건은 P 적용 문서 `execution-routing.md`의 `qualification probe 예외`를 확인한다. W는 제품 제한·자격·권한·impact 소비를 변경하지 않는다.

## Execution Profile

Issue body의 optional `## Execution Profile`은 phase별 `model-tier`, optional concrete `model`, `reasoning-tier`, optional `fallback-model-tier`/`fallback-model`, `ESCALATION.only-if`를 제공한다.

- Profile이 없으면 current execution model/reasoning과 기존 흐름을 유지한다.
- Profile은 hard guard, SDD gate, claim, allowed/forbidden, required verification, required review를 덮어쓰지 않는다.
- Trivial/Small single-agent policy가 여러 phase route보다 우선한다. 단, current concrete model이 role DENIED이면 actor 수를 늘리지 않고 qualified replacement 한 명으로 교체한다.
- Profile이 이미 실행 중인 current/manual model을 유지하는 경우 current/manual bootstrap 규칙을 적용한다. Profile 때문에 model switch/delegation이 생기거나 Agent가 concrete fallback/reviewer를 고르면 fresh role qualification PASS가 필요하다.

## Execution Packet

Execution Packet은 전체 source 묶음이 아니라 orchestrator가 이미 판정한 결정을 전달하는 cache다. 최소 field는 다음과 같다.

- issue identity: id, title, snapshot identity
- phase, recommended model tier와 reasoning tier
- reviewed PLAN reference와 immutable identity
- goal
- allowed paths와 forbidden paths
- required public contracts
- already-resolved decisions와 핵심 이유의 불변 참조
- failure/recovery conditions 또는 명시적 not-applicable 근거
- context transition: 실제 host capability 근거, 사용한 방법, 실행 evidence, 최소 입력 참조, fallback 사유와 한계(해당 시)
- target paths/symbols
- phase acceptance criteria
- required verification
- required review 여부
- PLAN implementation finding handoff identity와 resolution expectation list
- known blockers
- escalation conditions
- provenance: hard guard, canonical process, direct contract의 reference와 immutable identity
- SDD grade gate와 claim의 immutable evidence
- host-enforced propagation 또는 worker direct-read의 immutable guard application evidence object

guard application evidence는 `kind`, `reference`, 적용한 hard guard의 `source identity`, evidence 자체의 immutable identity를 가진 object여야 한다. evidence 누락·빈 값·형식 오류는 `INVALID`, current source와의 identity/freshness mismatch는 `STALE`다. 둘 다 fail-closed하고 hard guard direct read 또는 `BLOCKED`로만 진행한다. `runtime_guard_propagation: true` 또는 `guard applied: true` 같은 boolean은 증거가 아니다.

issue snapshot, PLAN identity/reference, goal, allowed/forbidden, required contracts, phase acceptance, verification, escalation, provenance identity, gate/claim evidence는 nested field까지 존재하고 nonempty여야 한다. `implementation_findings`는 명시적 list이며 검토를 통과한 PLAN에 handoff가 없을 때만 비어 있을 수 있다. handoff가 있으면 각 item의 stable identity, PLAN exact target과 resolution expectation이 nonempty여야 하고 누락은 `INVALID`, current PLAN identity와 불일치는 `STALE`다. 필수 field 누락·빈 값·형식 오류는 `INVALID`다. packet이 상위 source와 충돌하면 관련 지시를 버리고 필요한 canonical source만 bounded refresh한다. freshness를 증명할 수 없으면 `STALE`이며 bounded refresh 후 새 provenance로 `VALID`가 되거나 `BLOCKED`한다.

다음 event는 관련 항목만 invalidate한다.

- Issue body/labels 변경
- reviewed PLAN artifact 변경
- direct contract의 base/head/ref 변경
- packet에 없는 새 direct dependency 발견
- architecture assumption과 모순되는 compile/test failure
- active lane/path conflict 발생
- hard guard/canonical Skill version 변경

### 구현 진입의 문맥·최신성 확인

Execution Packet은 새 계층을 만들지 않고 기존 필드에 인계 근거를 연결한다. host-supported `fresh-context`, `verified-compaction`, `direct-fallback` 중 실제 수행한 방법을 기록한다. 같은 모델의 새 문맥도 가능하며 이 선택은 model tier/qualification/grade별 actor 수 규칙을 변경하지 않는다. 압축은 필수 입력 보존과 현재 source 대조를 검증해야 성공이다. 미지원·압축 실패는 사유와 남은 이력의 한계를 남기고 직접 구현하며 분리 성공으로 표시하지 않는다. 필수 source 복구 실패는 BLOCKED다.

첫 edit 전 current Issue snapshot, PLAN identity, claim, guard와 직접 contract를 대조한다. Large/Epic에는 설계 단계 사람 승인 원본이 없으며 검토한 PLAN의 exact target과 Decision scope를 연결한다. PLAN이 달라지면 `STALE`이다. implementation finding은 검토를 통과한 PLAN의 list와 비교해 누락을 검출한다. resolved decision 이유, failure/recovery, verification 또는 required review 누락도 INVALID다. 현재 source mismatch는 STALE이며 관련 source만 bounded refresh한다. 대화·여러 설계 버전·전체 tool log는 기본 payload가 아니며 불변 source reference를 우선한다.

## 공통 영향 결과 참조와 로컬 소비

조건은 P 적용 문서 `execution-routing.md`의 `영향 분석`을 확인한다. P가 영향 분석 도구를 선언하지 않았으면 이 절은 적용하지 않는다. W는 제품 제한·자격·권한·impact 소비를 변경하지 않는다.

## Result Packet

어느 phase의 worker/reviewer든 실제 문제를 발견했으면 기존 반환 결과에 `P/.adaptive-sdd/project/sdd-workflow.md` (조건) / `W/process/sdd-workflow.md` (수행법)의 `문제 발견 시 기록과 종료 연결`에 따른 사건 정보/원본 참조를 포함한다. 상위 담당자가 Issue에 보존하고 종료 SUMMARY에 취합한다. 수행 담당자와 발견자를 구분하며 요청 model/reasoning과 실제 host metadata·미확인을 섞지 않는다. 같은 사건의 참조와 최초 실패/보정 결과를 유지한다. 문제가 없으면 이 사건 필드나 빈 목록을 추가하지 않는다. 이 조건부 관측은 아래 필수 `implementation_findings`나 acceptance/verification과 별개이며 새 packet 유효성 gate가 아니다.

IMPLEMENT worker는 full reasoning이나 전체 command log 대신 다음 field를 반환한다.

- base SHA와 head SHA
- changed files
- current head의 전체 changed-file inventory 또는 그 immutable reference
- current diff/patch immutable reference
- acceptance criterion별 `PASS | FAIL | BLOCKED`
- verification item별 실행 commit SHA, command, exit code/outcome, evidence kind, immutable evidence identity/reference
- scope drift
- unresolved decisions
- escalation evidence
- compact diff summary
- new direct dependencies
- freshness issues
- PLAN implementation finding handoff와 항목별 current-head resolution evidence

verification의 command, exit code, outcome은 metadata이며 그것만으로 PASS evidence가 아니다. immutable evidence identity는 CI check/run identity 또는 same-run host tool-result의 stable identity/content digest이며 verification commit SHA에 결합해야 한다. verification commit, evidence identity의 commit, Result head가 다르면 해당 item은 `STALE`이다. Result base/head, inventory, diff reference가 현재 검토 대상과 다르거나 inventory가 불완전해도 `STALE` 또는 `INVALID`다.

changed files, acceptance map, verification list는 nonempty여야 한다. scope drift는 boolean, unresolved/escalation/dependency/freshness field와 `implementation_findings`는 명시적 list여야 한다. PLAN에 Implementation finding handoff가 없으면 빈 list를 사용한다. handoff가 있으면 각 item은 finding identity, 검토를 통과한 PLAN exact target, resolution expectation, `resolved | unresolved`, current head에 결합된 code evidence identity와 fixture/test evidence identity를 가진다. PLAN handoff item 누락, code 또는 fixture evidence 한쪽 누락, evidence/current Result head 불일치, `unresolved` item은 complete로 판정하지 않는다. 각 verification item은 실행 commit과 같은 commit에 결합된 immutable evidence identity를 가져야 한다. 필수 field가 없거나 비어 있거나 acceptance가 `FAIL/BLOCKED`, scope drift, unresolved decision, freshness issue가 있으면 complete로 판정하지 않는다.

## Review Packet

모든 required review packet은 `review_phase: AS-IS | PLAN | CODE`, `review_mode: contract-review | blind-audit | reconfirmation`, exact remote target identity와 reviewer/author identity를 가진다. phase에 존재하지 않는 artifact를 nonempty 필드로 강제하지 않는다.

### Contract Review Packet

Review A와 기본 CODE reviewer 입력은 phase별로 제한한다.

- `AS-IS`: current Issue id/title/acceptance, AS-IS artifact 경로와 remote-resolvable exact SHA, remote base/head, 대상 inventory 또는 immutable reference, 직접 contract/source evidence, document author identity
- `PLAN`: current Issue id/title/acceptance, reviewed AS-IS identity, PLAN과 change-plan artifact 경로 및 remote-resolvable exact SHA, remote base/head, 대상 inventory 또는 immutable reference, 필요한 direct contract/evidence, document author identity
- `CODE`: current Issue acceptance, reviewed PLAN identity, base/head SHA, current head의 전체 changed-file inventory 또는 immutable reference, current diff/patch reference와 필요한 diff hunk, 필요한 public contract, verification evidence identity, implementation actor identity, PLAN implementation finding handoff와 항목별 code+fixture resolution evidence

해당 phase의 필수 field는 nested value까지 nonempty여야 한다. Contract reviewer는 제공 목록을 그대로 신뢰하지 않고 phase target/inventory를 독립 확인한 뒤 bounded artifact/diff와 contract를 검토한다. CODE reviewer는 current head의 전체 changed-file inventory를 독립 확인하고 PLAN의 모든 Implementation finding identity가 handoff됐는지와 각 item의 code+fixture evidence가 current head에서 실제 resolution을 증명하는지 확인한다. handoff가 없었던 경우에는 빈 list를 허용한다. reviewer identity는 document/implementation actor와 달라야 한다. 확인을 solution discovery, repository-wide 탐색, full-source handoff로 확장하지 않는다. target/head, inventory, diff, verification evidence 또는 implementation finding resolution evidence가 applicable current target과 다르면 review를 `STALE`로 처리한다. handoff 누락이나 unresolved item이 있으면 review를 complete로 판정하지 않는다.

### Blind Audit Packet

Large/Epic AS-IS/PLAN의 Review B에만 다음 최소 입력을 전달한다.

- Issue id와 title
- `review_phase: AS-IS | PLAN`
- `review_mode: blind-audit`
- target artifact 경로와 remote-resolvable exact SHA
- 상위 목표와 직접 소유 경계
- `solution implementation/repository-wide redesign 금지`
- `빠진 사실·숨은 가정·scope/boundary-changing omission 또는 blocking risk 탐색` 요청
- document author와 Review A actor/session identity는 중복 방지용 metadata로만 제공

Review B의 최초 verdict 전에는 Review A의 verdict, finding 목록, detailed Contract Review Packet과 이전 Review B finding detail을 제공하지 않는다. Blind Audit reviewer는 exact target에서 직접 인접한 caller/consumer/contract를 열어볼 수 있지만 전면 solution discovery를 수행하지 않는다. reviewer는 author와 Review A reviewer 모두와 다른 agent/session이어야 한다. target identity가 current candidate와 다르거나 actor/session 분리를 증명할 수 없으면 `STALE` 또는 `INVALID`다.

최초 verdict output은 exact target과 결합된 immutable verdict identity와 신규 finding 목록을 가진다. 각 신규 finding은 stable identity, 다음 severity 중 하나, exact-candidate evidence를 포함한다.

- `Human Decision blocker`
- `Execution-contract blocker`
- `Implementation finding`
- `Non-blocking observation`

두 blocker severity는 추가로 깨지는 artifact/확정된 상위 contract/direct-boundary invariant와 다음 phase 전에 해결하지 않을 때 구현자에게 남는 의미 선택 또는 충돌하는 결정 의미를 포함한다. 이 qualification이 없고 code+fixture에서 contract-preserving 정답 하나로 수렴하면 `Implementation finding`이다. `Human Decision blocker`는 기존 `[HUMAN DECISION REQUIRED]` 절차를 사용하고, `Execution-contract blocker`는 change-plan execution contract와 fixture expectation에 한 방향을 고정한다. `Implementation finding`은 PLAN을 차단하지 않지만 IMPLEMENT handoff로 보존한다. `Non-blocking observation`은 PLAN/IMPLEMENT gate가 아니다.

최초 verdict가 immutable identity로 고정된 뒤에만 같은 Review B reviewer/session에 다음 reconciliation input을 별도 전달한다.

- current exact target identity와 initial verdict identity
- 이전 Review B finding별 stable identity와 resolution expectation ledger

reconciliation output은 이전 finding마다 `resolved | unresolved | regressed | not-applicable`과 current exact-candidate evidence를 가진다. 이전 finding을 자동 PASS로 처리하지 않으며, 최초 verdict에서 생성한 신규 finding 목록과 prior ledger 결과를 별도 list로 유지한다. 이전 ledger가 없으면 reconciliation은 `not-required`로 명시한다.

Review B 최종 PASS는 initial blind audit이 완료되고, 후속 revision이면 아래 current-target 재확인 chain과 필요한 reconciliation이 유효하며, unresolved Human Decision blocker와 unresolved Execution-contract blocker가 각각 0일 때 성립한다. Implementation finding과 Non-blocking observation의 개수는 PASS를 막지 않는다. review round 또는 finding 개수의 고정 상한으로 PASS를 강제하지 않는다.

### 후속 재확인과 반복 정체

재검토 dispatch 전에 phase artifact inventory·bytes, Decision scope·upstream, 직접 계약/소비자와 감사 전제의 차이를 전체 변경 inventory로 판정한다. 기록/head-only에 모두 불변이면 기존 review target을 유지하며 최신 head와 다르다는 이유로 A/B를 반복하지 않는다. artifact 변경 뒤에는 새 target의 관련 판단만 재확인하되 A 보정/PASS 고정 후 B를 dispatch한다. 핵심 전제 변경/영향 불명은 A 이후 새 blind B로 연결한다.


기존 Review Packet의 `review_mode`는 최초 `blind-audit`과 후속 `reconfirmation`을 구분한다. 후속 packet은 이전/현재 remote target identity, 전체 변경 inventory/diff reference, prior finding identity와 resolution expectation, 영향받는 contract·완료 기준·직접 소비자, 영향 없음의 근거, current-target 재확인 evidence를 포함한다. reviewer는 inventory와 주변 source 접근 가능성을 독립 확인한다. 필수 근거 누락은 INVALID, 이전 target 결과를 current로 이름만 바꾸면 STALE다.

SHA 변경 뒤 검토 범위는 `P/.adaptive-sdd/project/sdd-workflow.md` (조건) / `W/process/sdd-workflow.md` (수행법)의 `의미·영향에 따른 설계 재검토`로 정한다. 결과 기록은 target artifact와 분리하고 대상 bytes가 불변이면 그 검토를 재실행하지 않는다. 설명 보완/국소 실행 계약 수정은 invalidated 판단과 직접 영향만 재확인한다. 핵심 Decision·상위 계약·작업 경계·실패/복구 의미·감사 전제 변경 또는 영향 불명확이면 무효화된 phase를 확장하고 새 blind B를 요구한다. 새 B는 author/A와 다른 fresh session에서 최초 verdict 전에 A 결과·prior B detail을 받지 않으며 이후에만 reconciliation한다. 후속 재확인은 prior finding을 받을 수 있으나 최초 blind를 대체하지 않는다.

현재 review 근거는 최초 blind verdict의 immutable identity와 이후 target 차이/영향/A·B 재확인 chain으로 연결한다. current target에서 prior finding 상태를 직접 증명하고 미해결 blocker 0을 확인한다.

같은 phase·영역의 동일 finding/의미 충돌이 수정·재확인 뒤 2회 연속 unresolved/regressed이면 다음 자동 리뷰를 멈춘다. 기존 packet에 영역/충돌 identity, 수정·재확인 target과 근거, 원인·선택지를 기록한다. 총 리뷰 수나 무관한 신규 finding은 이 streak가 아니다. SHA/이름 변경만으로 reset하지 않으며 해결 근거 또는 Human 범위 결정/새 근거에 따른 명시적 재검토 사유가 있어야 재개한다. blocker를 PASS로 강제하거나 요구사항을 임의 삭제하지 않는다.


## Deterministic measurement

paired Large fixture는 동일 issue/PLAN/contract의 `full_source_handoff`와 `execution_packet`을 함께 둔다. canonical JSON은 UTF-8에서 `sort_keys=True`, `separators=(",", ":")`, `ensure_ascii=False`로 직렬화한다.

- `input_bytes = len(serialized.encode("utf-8"))`
- `token_proxy = ceil(input_bytes / 4)`
- token proxy는 실제 host token 수가 아니다.
- packet bytes와 token proxy는 full-source handoff보다 모두 작아야 한다.
- hard guard provenance/application evidence, SDD grade gate evidence, claim evidence, allowed/forbidden, nonempty required verification, required review를 실제 Execution Packet 구조와 immutable identity에서 derive한다. `preserved_controls: true` 같은 boolean 자기신고는 사용하지 않는다.
- 위 control을 하나씩 제거하거나 무효화한 negative fixture가 모두 실패해야 하며, 하나라도 통과하면 byte 절감과 무관하게 metric은 실패다.

## Guard 적용과 packet 공통 검증

- host-enforced propagation 또는 worker direct-read의 immutable guard application evidence object
guard application evidence는 `kind`, `reference`, 적용한 hard guard의 `source identity`, evidence 자체의 immutable identity를 가진 object여야 한다. evidence 누락·빈 값·형식 오류는 `INVALID`, current source와의 identity/freshness mismatch는 `STALE`다. 둘 다 fail-closed하고 hard guard direct read 또는 `BLOCKED`로만 진행한다. `runtime_guard_propagation: true` 또는 `guard applied: true` 같은 boolean은 증거가 아니다.
issue snapshot, PLAN identity/reference, goal, allowed/forbidden, required contracts, phase acceptance, verification, escalation, provenance identity, gate/claim evidence는 nested field까지 존재하고 nonempty여야 한다. `implementation_findings`는 명시적 list이며 검토를 통과한 PLAN에 handoff가 없을 때만 비어 있을 수 있다. handoff가 있으면 각 item의 stable identity, PLAN exact target과 resolution expectation이 nonempty여야 하고 누락은 `INVALID`, current PLAN identity와 불일치는 `STALE`다. 필수 field 누락·빈 값·형식 오류는 `INVALID`다. packet이 상위 source와 충돌하면 관련 지시를 버리고 필요한 canonical source만 bounded refresh한다. freshness를 증명할 수 없으면 `STALE`이며 bounded refresh 후 새 provenance로 `VALID`가 되거나 `BLOCKED`한다.
