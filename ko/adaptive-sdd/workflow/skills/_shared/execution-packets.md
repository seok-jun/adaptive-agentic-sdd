# Execution Packet과 인계 계약

입력은 명시한 P/S/W/M 절대 root다. S는 설치 root이며 in-repo에서는 P와 같다. 이 문서는 packet을 작성·수신·검증하는 해당 phase에서만 읽으며 fixed pre-read 입력이 아니다. 모델 배정·qualification 판정이 필요하면 [execution-routing](execution-routing.md)의 해당 절을 읽는다.

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

적용할 P 코드 컨벤션이 있으면 provenance에 해당 문서·절·identity(또는 확인 시점)를 연결하고 PLAN의 명시적 이탈/예외를 함께 인계한다. 선언이 없으면 그 사실을 표시하며 새 컨벤션 문서를 강제하지 않는다. known blockers에는 [미결 사항의 담당·필요 단계](../../process/sdd-workflow.md#미결-사항과-단계별-의존성)를 연결하고, 미래 단계의 미결을 현재 작업 전체의 blocker로 확대하지 않는다.

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

이 event가 계획 전제 오류나 진행 중 정책 변경이면 [계획 정정과 정책 전환](../../process/sdd-artifacts.md#계획-정정과-정책-전환)으로 원본부터 정정한다. Packet만 수정해 기존 PLAN·정책과의 충돌을 덮지 않는다. 새 Packet에는 현재 적용할 원본과 필요한 재검토 근거를 연결한다.

### 구현 진입의 문맥·최신성 확인

Execution Packet은 새 계층을 만들지 않고 기존 필드에 인계 근거를 연결한다. Large의 검토를 통과한 PLAN에서 IMPLEMENT로 전환할 때 host가 지원하면 같은 모델이라도 별도 구현 문맥을 선택한다. 실제 fresh session/agent 또는 검증된 압축을 사용하며 model tier/qualification/grade별 actor 수 규칙은 변경하지 않는다. host-supported `fresh-context`, `verified-compaction`, `direct-fallback` 중 실제 수행한 방법과 실행 evidence를 기록한다. 압축은 필수 입력 보존과 현재 source 대조를 검증해야 성공이다. 미지원·압축 실패는 사유·최소 입력 참조·실제 남은 이력의 한계를 남기고 직접 구현하며 분리 성공으로 표시하지 않는다. shell에서 대화 명령을 실행하거나 전환을 선언한 것만으로 성공 처리하지 않는다. 필수 source 복구 실패는 `BLOCKED`다.

첫 edit 전 current Issue snapshot, PLAN identity, claim, guard와 직접 contract를 대조한다. Large에는 설계 단계 사람 승인 원본이 없으며 검토한 PLAN의 exact target과 Decision scope를 연결한다. PLAN이 달라지면 `STALE`이다. implementation finding은 검토를 통과한 PLAN의 list와 비교해 누락을 검출한다. resolved decision 이유, failure/recovery, verification 또는 required review 누락도 INVALID다. 현재 source mismatch는 STALE이며 관련 source만 bounded refresh한다. 대화·여러 설계 버전·전체 tool log는 기본 payload가 아니며 불변 source reference를 우선한다.

수신자는 필요한 source만 bounded refresh해 유효성을 증명할 때까지 edit하지 않는다. root에는 Result Packet과 필요한 변경·검증 근거만 반환하고 전체 worker 로그를 재합치지 않는다. 이미 IMPLEMENT 중인 lane의 session/branch를 이 규칙 때문에 소급 초기화하지 않는다.

## Result Packet

P의 검증 선언은 [검증 계약](../../process/verification.md#verification-strategy)을 따른다. 아래 code+fixture/test 해결 근거에는 P가 선언한 동등한 동작 관찰 근거도 포함할 수 있지만, 현재 head에서 finding의 resolution expectation을 증명해야 한다. temporary test는 보존 위치·test/fixture hash·실행 당시 제품 입력 identity와 최종 후보 대응을 연결한다. 파일이 현재 제품 트리에 없다는 이유로 증거를 생략하지 않는다.

수동 검증 item은 command/exit code 대신 `method: manual`, 확인자·확인 시점·절차·실제 관찰 결과를 사용한다. 실행하지 않은 command를 만들지 않는다. 나머지 대상 commit·immutable evidence identity·입력 불변/재사용·필수 검증 결과 요건은 자동 검증과 동일하며, 값 부재가 허용되는 것은 manual 항목의 command/exit code뿐이다.

어느 phase의 worker/reviewer든 실제 문제를 발견했으면 기존 반환 결과에 P 적용 문서 `S/.adaptive-sdd/project/sdd-workflow.md`의 조건과 [문제 발견 시 기록과 종료 연결](../../process/observations.md#문제-발견-시-기록과-종료-연결)에 따른 사건 정보/원본 참조를 포함한다. 시작·인계 관측은 [관측 시점별 소비와 기록](../../process/observations.md#차세대-방법론의-적용과-개선-관측)을 연결한다. 이 조건부 사건 정보는 아래 필수 `implementation_findings`나 acceptance/verification과 별개이며 새 packet 유효성 gate가 아니다.

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

AS-IS/PLAN의 direct evidence에는 판단을 좌우하는 [조사 근거와 남은 전제](../../process/sdd-artifacts.md#판단에-필요한-조사)를 연결한다. PLAN/CODE에는 선언된 P 컨벤션 참조와 이탈 이유·예외 결정 근거를 포함한다. reviewer는 적용 가능한 기준과 실제 지시/변경을 대조하고, 개인 선호를 새 계약으로 만들지 않는다. 미결의 담당·필요 시점은 reviewer 발견 여부와 별개로 다음 작업의 의존성에 반영한다.

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

#### Blind 입력 준비와 확인

최초 blind에 제공하는 자료는 리뷰 결과와 분리해 준비한다. 혼합 파일을 통째로 전달하고 reviewer에게 뒤쪽을 읽지 말라고만 지시하지 않는다. 원격 exact candidate 게시 조건은 유지하며, 아래 사본은 게시된 원문의 전달 형식이지 local-only 후보를 인정하는 예외가 아니다.

1. target artifact·Issue 본문·상위 목표·직접 계약/컨벤션의 필요한 범위를 고정한다. 원문 자체에 A/B verdict·finding ID·리뷰 유래 설명이 섞였는지 작성자가 먼저 확인한다. 사람 결정과 실질적인 제약·미결·실패 근거는 유지하고 리뷰 결과의 식별/평가 정보만 분리한다. 내용 정정이 필요하면 원본을 정정·게시하고 기존 영향별 재검토를 적용한다. 사본만 임의 요약·삭제해 검토 의미를 바꾸지 않는다.
2. 원본의 remote·exact commit·path, 선택한 본문/줄 범위, 원본과 출력의 hash를 기록한 불변 사본 또는 동등한 제한 조회를 제공한다. 전체 파일·기록·commit 메시지가 먼저 도구 출력에 나타난 뒤 필터링하는 방식은 쓰지 않는다. local-docs는 [리뷰 입력](../../tracker/local-docs.md#리뷰-입력)의 본문 경계를 사용한다. 기록은 원본에 보존하며 리뷰를 위해 삭제하지 않는다.
3. reviewer에게는 검토 자료 root와 고정 manifest identity를 전달하고 원본 history·feedback·리뷰 기록을 입력 root에 포함하지 않는다. 실제 reviewer의 OS 계정/host에서 읽을 수 있는 위치와 범위를 확인한다. host가 접근 제한을 제공하면 사용하고, 실제 강제한 범위와 지시로만 제한한 범위를 구별해 Packet에 남긴다. 해시 일치만으로 OS 격리나 의미상 누출 없음이 증명됐다고 하지 않는다.
4. 최초 verdict 전 추가 직접 근거가 필요하면 같은 exact revision과 결과 제외 조건으로 준비·검증해 추가한다. 자료 제한 때문에 필수 직접 계약을 확인할 수 없으면 범위를 보완하기 전 PASS하지 않는다. 추가 manifest identity도 기록하며 기존 입력을 조용히 덮어쓰지 않는다.
5. 이전 리뷰 결과가 노출되면 최초 blind 실행은 무효로 기록하고 입력을 고친 뒤 새 분리 session으로 다시 시작한다. 노출된 내용을 잊었다는 자기보고로 계속하지 않는다. 후속 `reconfirmation`은 이전 finding을 받을 수 있지만 최초 blind로 표시하지 않는다.

Git 자료 추출에는 [review_snapshot.py](../../../tools/review_snapshot.py)를 사용할 수 있다. UTF-8 source blob을 직접 읽어 byte를 보존하고 `tracker-body`는 `## 메타`와 `## 기록`을 제외한다. `artifact`는 파일 전체이므로 본문에 섞인 리뷰 결과를 자동 탐지하지 않는다. spec은 `[{"path":"items/T-1.md","kind":"tracker-body"},{"path":"docs/plan.md","kind":"artifact"}]` 형식이며 필요한 source만 지정한다.

```text
python review_snapshot.py create --repo <원본 저장소> --commit <전체 commit SHA> --spec <spec.json> --output <새 자료 폴더>
python review_snapshot.py check --repo <원본 저장소> --bundle <자료 폴더> --manifest-sha256 <create 출력 digest>
```

준비 담당은 원본과의 `check`를 수행하고 Packet에 그 근거와 digest를 연결한다. reviewer 또는 제한된 검증 수단이 동일 digest와 원본 대응을 확인할 수 있게 하되, 검증 명령은 제외한 원문을 출력하지 않아야 한다. 도구는 기존 출력 폴더를 덮어쓰지 않으며 `check`는 원본 선택·내용 변경·추가 파일을 검사한다. 폴더가 파일시스템 수준에서 immutable이 되는 것은 아니므로 전달 후 변경 시 같은 입력으로 취급하지 않는다. 도구 성공은 원격 게시·host 접근·내용 격리 확인을 대체하지 않는다.

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
