# Execution Packet과 인계 계약

입력은 명시한 P/W/M 절대 root다. 이 문서는 packet을 작성·수신·검증하는 해당 phase에서만 읽으며 fixed pre-read 입력이 아니다. 모델 배정·qualification 판정이 필요하면 [execution-routing](execution-routing.md)의 해당 절을 읽는다.

## 읽는 조건과 목차

- worker 지시를 구성하거나 첫 edit 전에 입력을 확인할 때: [Source of Truth](#source-of-truth), [Execution Packet](#execution-packet)과 그 guard·문맥·최신성 검증.
- worker가 결과를 반환하거나 finishing에서 소비할 때: [Result Packet](#result-packet).
- required review를 준비하거나 결과를 확인할 때: [Review Packet](#review-packet)의 해당 phase/mode.
- P가 선언한 영향 분석 결과를 소비할 때: [공통 영향 결과 참조와 로컬 소비](#공통-영향-결과-참조와-로컬-소비).
- fixture 평가·직렬화·token proxy 측정 시: [skill-evals의 Packet 직렬화와 측정](../../process/skill-evals.md#packet-직렬화와-측정). 운영 packet 인계의 선행 입력은 아니다.

## Source of Truth

우선순위는 `AGENTS.md hard guard > canonical Skill/process > current Issue + reviewed SDD/PLAN > Execution Packet`이다. Execution Packet은 상위 source를 대체하지 않는 derived cache다. 상위 source와 충돌하거나 provenance/freshness를 증명하지 못하면 해당 packet 항목을 실행하지 않는다.

공통 packet 계약은 W가 소유하며 모델 배정·tier·qualification과 grade별 actor 수는 [execution-routing](execution-routing.md)의 계약을 그대로 적용한다. P가 선언한 모델 제한·권한·영향 분석 조건을 packet으로 변경하지 않는다.

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

### Guard 적용과 packet 공통 검증

standalone/subagent runtime이 guard 전파를 보장하지 않으면 worker가 `AGENTS.md`의 필요한 hard guard section을 직접 읽는다.

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

Execution Packet은 새 계층을 만들지 않고 기존 필드에 인계 근거를 연결한다. Large의 검토를 통과한 PLAN에서 IMPLEMENT로 전환할 때 host가 지원하면 같은 모델이라도 별도 구현 문맥을 선택한다. 실제 fresh session/agent 또는 검증된 압축을 사용하며 model tier/qualification/grade별 actor 수 규칙은 변경하지 않는다. host-supported `fresh-context`, `verified-compaction`, `direct-fallback` 중 실제 수행한 방법과 실행 evidence를 기록한다. 압축은 필수 입력 보존과 현재 source 대조를 검증해야 성공이다. 미지원·압축 실패는 사유·최소 입력 참조·실제 남은 이력의 한계를 남기고 직접 구현하며 분리 성공으로 표시하지 않는다. shell에서 대화 명령을 실행하거나 전환을 선언한 것만으로 성공 처리하지 않는다. 필수 source 복구 실패는 `BLOCKED`다.

첫 edit 전 current Issue snapshot, PLAN identity, claim, guard와 직접 contract를 대조한다. Large에는 설계 단계 사람 승인 원본이 없으며 검토한 PLAN의 exact target과 Decision scope를 연결한다. PLAN이 달라지면 `STALE`이다. implementation finding은 검토를 통과한 PLAN의 list와 비교해 누락을 검출한다. resolved decision 이유, failure/recovery, verification 또는 required review 누락도 INVALID다. 현재 source mismatch는 STALE이며 관련 source만 bounded refresh한다. 대화·여러 설계 버전·전체 tool log는 기본 payload가 아니며 불변 source reference를 우선한다.

수신자는 필요한 source만 bounded refresh해 유효성을 증명할 때까지 edit하지 않는다. root에는 Result Packet과 필요한 변경·검증 근거만 반환하고 전체 worker 로그를 재합치지 않는다. 이미 IMPLEMENT 중인 lane의 session/branch를 이 규칙 때문에 소급 초기화하지 않는다.

## Result Packet

어느 phase의 worker/reviewer든 실제 문제를 발견했으면 기존 반환 결과에 P 적용 문서 `P/.adaptive-sdd/project/sdd-workflow.md`의 조건과 [문제 발견 시 기록과 종료 연결](../../process/observations.md#문제-발견-시-기록과-종료-연결)에 따른 사건 정보/원본 참조를 포함한다. 시작·인계 관측은 [관측 시점별 소비와 기록](../../process/observations.md#차세대-방법론의-적용과-개선-관측)을 연결한다. 이 조건부 사건 정보는 아래 필수 `implementation_findings`나 acceptance/verification과 별개이며 새 packet 유효성 gate가 아니다.

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

verification의 command, exit code, outcome은 metadata이며 그것만으로 PASS evidence가 아니다. immutable evidence identity는 CI check/run identity 또는 same-run host tool-result의 stable identity/content digest이며 **실제 실행 commit SHA**에 결합해야 한다. 실행 commit과 evidence identity의 commit이 다르면 해당 item은 `STALE`이다. Result base/head, inventory, diff reference는 현재 검토 대상과 일치해야 하며 불일치·불완전이면 `STALE` 또는 `INVALID`다.

실행 commit과 Result head가 다른 검증은 [PASS 유효성](../../process/verification.md#검증-시퀀싱과-pass-유효성)의 입력 불변 조건을 증명한 경우에만 재사용한다. 해당 verification item에 원래 실행 commit·불변 evidence identity, 현재 Result head, 두 revision 사이의 전체 변경 inventory·diff 참조, 해당 command가 소비하거나 assertion하는 입력의 불변 근거를 연결하고 **재사용**으로 표시한다. CODE reviewer와 종료 담당자는 그 차이와 직접 근거를 확인한다. 자기신고 boolean, 같은 branch·명령, 문서 확장자만으로 입력 불변을 판정하지 않는다.

원래 실행 근거를 현재 head에서 새로 실행한 것처럼 바꾸지 않는다. 입력이 바뀌었거나 불변 여부를 증명할 수 없으면 `STALE`로 두고 검증 계약의 targeted → 안정화된 후보의 invalidated required command 순서로 재실행한다. 이 재사용 조건은 verification item에만 적용하며 현재 diff·inventory와 PLAN finding의 current-head code+fixture 해결 근거를 면제하지 않는다.

changed files, acceptance map, verification list는 nonempty여야 한다. scope drift는 boolean, unresolved/escalation/dependency/freshness field와 `implementation_findings`는 명시적 list여야 한다. PLAN에 Implementation finding handoff가 없으면 빈 list를 사용한다. handoff가 있으면 각 item은 finding identity, 검토를 통과한 PLAN exact target, resolution expectation, `resolved | unresolved`, current head에 결합된 code evidence identity와 fixture/test evidence identity를 가진다. PLAN handoff item 누락, code 또는 fixture evidence 한쪽 누락, evidence/current Result head 불일치, `unresolved` item은 complete로 판정하지 않는다. 각 verification item은 실행 commit과 같은 commit에 결합된 immutable evidence identity를 가져야 한다. 필수 field가 없거나 비어 있거나 acceptance가 `FAIL/BLOCKED`, scope drift, unresolved decision, freshness issue가 있으면 complete로 판정하지 않는다.

## Review Packet

이 절은 review 입력·출력 필드와 유효성을 소유한다. Large의 severity 판정, reviewer 선택·독립성, A/B 순서, blind isolation, reconciliation과 다음 phase 진행 조건은 [Large 설계 이중 독립 리뷰](../../process/design-review.md#large-설계-이중-독립-리뷰)를 따른다. 변경 뒤 검토와 중단은 [의미·영향에 따른 설계 재검토](../../process/design-review.md#의미영향에-따른-설계-재검토)와 [반복 정체 시 전환](../../process/design-review.md#반복-정체-시-전환)을 적용한다.

모든 required review packet은 `review_phase: AS-IS | PLAN | CODE`, `review_mode: contract-review | blind-audit | reconfirmation`, exact remote target identity와 reviewer/author identity를 가진다. phase에 존재하지 않는 artifact를 nonempty 필드로 강제하지 않는다.

### Contract Review Packet

Review A와 기본 CODE reviewer 입력은 phase별로 제한한다.

- `AS-IS`: current Issue id/title/acceptance, AS-IS artifact 경로와 remote-resolvable exact SHA, remote base/head, 대상 inventory 또는 immutable reference, 직접 contract/source evidence, document author identity
- `PLAN`: current Issue id/title/acceptance, reviewed AS-IS identity, PLAN과 change-plan artifact 경로 및 remote-resolvable exact SHA, remote base/head, 대상 inventory 또는 immutable reference, 필요한 direct contract/evidence, document author identity
- `CODE`: current Issue acceptance, reviewed PLAN identity, base/head SHA, current head의 전체 changed-file inventory 또는 immutable reference, current diff/patch reference와 필요한 diff hunk, 필요한 public contract, verification evidence identity, implementation actor identity, PLAN implementation finding handoff와 항목별 code+fixture resolution evidence

해당 phase의 필수 field는 nested value까지 nonempty여야 한다. Contract reviewer는 제공 목록을 그대로 신뢰하지 않고 phase target/inventory를 독립 확인한 뒤 bounded artifact/diff와 contract를 검토한다. CODE reviewer는 current head의 전체 changed-file inventory를 독립 확인하고 PLAN의 모든 Implementation finding identity가 handoff됐는지와 각 item의 code+fixture evidence가 current head에서 실제 resolution을 증명하는지 확인한다. handoff가 없었던 경우에는 빈 list를 허용한다. reviewer identity는 document/implementation actor와 달라야 한다. 확인을 solution discovery, repository-wide 탐색, full-source handoff로 확장하지 않는다. target/head, inventory, diff 또는 implementation finding resolution evidence가 applicable current target과 다르면 review를 `STALE`로 처리한다. verification evidence는 위 Result Packet의 실제 실행 identity와 필요한 입력 불변·재사용 근거를 함께 확인하며, 그 조건이 유효하지 않으면 `STALE`로 처리한다. handoff 누락이나 unresolved item이 있으면 review를 complete로 판정하지 않는다.

### Blind Audit Packet

Large AS-IS/PLAN의 Review B에만 다음 최소 입력을 전달한다.

- Issue id와 title
- `review_phase: AS-IS | PLAN`
- `review_mode: blind-audit`
- target artifact 경로와 remote-resolvable exact SHA
- 상위 목표와 직접 소유 경계
- `solution implementation/repository-wide redesign 금지`
- `빠진 사실·숨은 가정·scope/boundary-changing omission 또는 blocking risk 탐색` 요청
- document author와 Review A actor/session identity는 중복 방지용 metadata로만 제공

최초 packet에는 Review A verdict/finding/detailed Contract Review Packet과 이전 Review B finding detail을 포함하지 않는다. reviewer는 exact target에서 직접 인접한 caller/consumer/contract를 확인할 수 있지만 전면 solution discovery로 확장하지 않는다. target identity가 current candidate와 다르거나 author/Review A와의 actor/session 분리를 증명할 수 없으면 `STALE` 또는 `INVALID`다.

최초 verdict output은 exact target과 결합된 immutable verdict identity와 신규 finding 목록을 가진다. 각 신규 finding은 stable identity, 다음 severity 중 하나, exact-candidate evidence를 포함한다.

- `Human Decision blocker`
- `Execution-contract blocker`
- `Implementation finding`
- `Non-blocking observation`

두 blocker severity의 추가 필드는 깨지는 artifact/확정된 상위 contract/direct-boundary invariant와 다음 phase 전에 해결하지 않을 때 구현자에게 남는 의미 선택 또는 충돌하는 결정 의미다. qualification과 severity 판정·해결 위치·handoff 의무는 [Large 설계 이중 독립 리뷰](../../process/design-review.md#large-설계-이중-독립-리뷰)가 원본이다.

별도 reconciliation input은 위 프로토콜이 정한 시점과 동일 Review B reviewer/session에 다음을 전달한다.

- current exact target identity와 initial verdict identity
- 이전 Review B finding별 stable identity와 resolution expectation ledger

reconciliation output은 이전 finding마다 `resolved | unresolved | regressed | not-applicable`과 current exact-candidate evidence를 가진다. 최초 verdict의 신규 finding 목록과 prior ledger 결과는 별도 list로 유지한다. 이전 ledger가 없으면 reconciliation은 `not-required`로 명시한다. 이전 finding을 자동 PASS로 처리하지 않으며 최종 PASS와 다음 phase 진행 조건은 [설계 리뷰의 진행 조건](../../process/design-review.md#large-설계-이중-독립-리뷰)을 따른다.

### 후속 재확인과 반복 정체

재검토 dispatch, 기존 target 유지, 새 blind B 필요 여부는 [의미·영향에 따른 설계 재검토](../../process/design-review.md#의미영향에-따른-설계-재검토)로 판정한다. 같은 finding/의미 충돌의 정체 판정·중단·재개 조건은 [반복 정체 시 전환](../../process/design-review.md#반복-정체-시-전환)을 따른다.

기존 Review Packet의 `review_mode`는 최초 `blind-audit`과 후속 `reconfirmation`을 구분한다. 후속 packet은 이전/현재 remote target identity, 전체 변경 inventory/diff reference, prior finding identity와 resolution expectation, 영향받는 contract·완료 기준·직접 소비자, 영향 없음의 근거, current-target 재확인 evidence를 포함한다. reviewer는 inventory와 주변 source 접근 가능성을 독립 확인한다. 필수 근거 누락은 `INVALID`, 이전 target 결과를 current로 이름만 바꾸면 `STALE`다.

현재 review 근거에는 최초 blind verdict의 immutable identity와 이후 target 차이/영향/A·B 재확인 chain, current target의 prior finding 상태에 대한 직접 근거를 연결한다. 정체 시에는 기존 packet에 영역/충돌 identity, 수정·재확인 target과 근거, 원인·선택지를 기록한다. packet 필드를 채운 사실만으로 unresolved blocker를 PASS로 처리하지 않는다.

## 공통 영향 결과 참조와 로컬 소비

조건은 P 적용 문서 `execution-routing.md`의 `영향 분석`을 확인한다. P가 영향 분석 도구를 선언하지 않았으면 이 절은 적용하지 않는다. W는 제품 제한·자격·권한·impact 소비를 변경하지 않는다.
