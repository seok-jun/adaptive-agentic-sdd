# Execution routing

입력은 진입 파일에 명시한 M·W·P 경로다. 외부 설치 경로는 설치 도구의 옵션이며 별도 실행 역할이 아니다. P 적용 문서 `W/../project/execution-routing.md`의 모델 제한·영향 분석·probe 조건을 먼저 확인한다.

현재 phase/role 진입·유지의 current/manual 적격 확인, model/reasoning 선택, switch/delegation 또는 reviewer 배정 시 읽는다. 같은 run의 해당 role에서 여전히 유효한 근거는 재사용하며, model switch가 없다는 이유로 자격 확인을 생략하지 않는다. fixed pre-read 입력은 아니다. packet 작성·수신·검증만 필요하면 [Execution Packet과 인계 계약](execution-packets.md)의 해당 절을 읽는다.

## 목차

- [두 축 routing](#두-축-routing)
- [Host Capability Map](#host-capability-map)
- [Model Role Qualification](#model-role-qualification)
- [qualification probe 예외](#qualification-probe-예외)
- [Execution Profile](#execution-profile)
- [Packet과 영향 결과 인계](#packet과-영향-결과-인계)

## Source of Truth

공통 routing/qualification 계약은 W가 소유하고 P가 적용한 프로필·명시 모델 제한·권한·로컬 영향 분석 입력은 P가 소유한다. packet의 Source of Truth·guard 적용·최신성 검증은 [인계 계약](execution-packets.md#source-of-truth)이 소유한다.

## 두 축 routing

grade는 orchestration shape만 정한다.

| grade | orchestration |
| --- | --- |
| Trivial / Small | current agent 한 명이 model switch와 delegation 없이 완료; current concrete model이 role DENIED이면 한 명의 qualified replacement로 교체 |
| Medium | 단일 agent가 기본이며 실제 unresolved PLAN decision 또는 required independent review phase만 bounded delegation |
| Large | root/orchestrator가 검토를 통과한 설계와 경계를 소유하고 `PLAN / IMPLEMENT / REVIEW` coarse-grained phase만 위임 가능 |

Epic은 위 실행 grade와 별개인 선택적 관리 단위다. 담당은 목표·가이드·작업 구성·의존성·전체 완료를 조율하고, 각 하위 실행 Issue는 자체 grade로 routing한다. Epic 생성·분해에 별도 worker·독립 reviewer·model 선택을 요구하지 않으며 단일 Large 수행도 허용한다.

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
3. current/manual concrete model이면 아래 [Model Role Qualification](#model-role-qualification)의 current/manual 규칙으로 canonical safety deny와 실제 explicit record를 먼저 판정한다. 그 조건과 fresh Host Capability evidence가 phase floor를 충족하면 current/manual route를 유지한다.
4. Execution Profile의 explicit model/tier가 현재 model에서 switch를 요구하거나 Agent가 worker/reviewer/fallback concrete model을 자동 선택하면 해당 development role의 **fresh qualification PASS**가 필요하다.
5. 자동 후보의 tier가 floor 이상이고 fresh role qualification PASS이면 사용한다.
6. explicit fallback이 없거나 부적격이면 floor 이상인 나머지 fresh host mapping을 낮은 적격 tier부터 결정적으로 탐색하되, 각 자동 후보에 fresh role qualification PASS를 요구한다. `frontier`는 기존 escalation evidence 없이 이 fallback에 포함하지 않는다.
7. 자동 선택이 필요한데 capability 후보가 모두 역할 부적격이면 `BLOCKED: model role unqualified`, capability 후보 자체를 증명할 수 없으면 `BLOCKED: routing capability unavailable`이다.

Profile과 fallback은 floor 아래로 downgrade할 수 없다. 존재하지 않거나 지원 여부가 확인되지 않은 concrete model/tier를 추정하지 않는다. **아직 진입하지 않은 future phase의 concrete model qualification은 선결 조건으로 미리 요구하지 않는다.** 해당 phase에서 실제 current/manual model을 확인하거나 switch/delegation 후보를 선택하기 직전에 위 규칙으로 just-in-time 검증한다.

## Host Capability Map

P의 `routing.role_defaults`는 선호 후보이고 `routing.capabilities`는 host mapping의 근거 참조다. 사람이 설정 파일에 적었다는 사실만으로 능력·가용성·role qualification이 증명되지는 않는다. 선택 시 host·concrete model·supported reasoning·원천 identity·유효 기한을 확인한다. role qualification은 P의 `qualification_records` 참조나 실제 runtime evidence를 별도로 사용한다.

현재/사람이 선택한 모델을 바꾸지 않고 별도 reviewer session에 그대로 상속하는 경우, 실제 concrete model과 reasoning의 동일성을 host가 확인하면 current/manual 경로로 판정한다. 별도 session이라는 이유만으로 자동 모델 선택으로 분류하지 않는다. 모델이나 reasoning을 Agent가 새로 고르면 기존 자동 선택 qualification 규칙을 적용한다. reasoning을 host에서 확인할 수 없으면 확인된 요청값과 제공값 미확인을 구별한다. 지원 설정을 실제 적용했다는 fresh host 근거로 floor 충족을 확인할 수 없으면 충족을 추정하지 않고 해당 reviewer 배정을 차단한다. 별도 actor/session·Human-selected B 선택 조건은 유지한다.

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

Medium/Large에서 independent review가 required인데 분리된 reviewer agent/session capability가 없으면 valid execution trace를 만들지 않고 `BLOCKED: separate reviewer unavailable`로 중단한다. future reviewer의 concrete model role qualification은 PLAN 시작 조건이 아니라 실제 review actor 선택 직전에 검증한다.

Large AS-IS/PLAN의 Review B는 예외적으로 Human이 concrete model과 reasoning level을 선택한 뒤에만 route한다. 선택이 없으면 automatic reviewer mapping이나 fallback을 탐색하지 않고 `BLOCKED: blind-audit reviewer selection required`다. 선택값은 `strong + high` 이상의 canonical REVIEW floor, supported reasoning, canonical deny와 independent-reviewer role qualification을 모두 만족해야 한다. 선택된 model/session을 host에서 사용할 수 없거나 부적격이면 silent fallback 없이 `BLOCKED: selected blind-audit reviewer unavailable`로 중단하고 Human 재선택을 요청한다. Human 선택은 `review-mode = blind-audit`와 author/Review A actor 모두와 다른 별도 agent/session 요구를 바꾸지 않는다.

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

차단 model은 사용자가 명시적으로 지시한 별도 qualification probe Issue에서 synthetic/docs-only fixture, orchestrator-owned claim/isolation/lifecycle, bounded `qualification_probe` role, main 직접 push와 Issue/PR/merge/release 권한 금지, raw observation 보존 조건을 모두 만족할 때만 제한적으로 호출한다. 이 예외는 일반 개발 역할의 PASS가 아니며 일반 제품 Issue에는 적용하지 않는다.

제품별 조건은 P 적용 문서 `execution-routing.md`의 `qualification probe 예외`를 함께 확인한다. W는 제품 제한·자격·권한·impact 소비를 변경하지 않는다.

## Execution Profile

Issue body의 optional `## Execution Profile`은 phase별 `model-tier`, optional concrete `model`, `reasoning-tier`, optional `fallback-model-tier`/`fallback-model`, `ESCALATION.only-if`를 제공한다.

- Profile이 없으면 current execution model/reasoning과 기존 흐름을 유지한다.
- Profile은 hard guard, SDD gate, claim, allowed/forbidden, required verification, required review를 덮어쓰지 않는다.
- Trivial/Small single-agent policy가 여러 phase route보다 우선한다. 단, current concrete model이 role DENIED이면 actor 수를 늘리지 않고 qualified replacement 한 명으로 교체한다.
- Profile의 current/manual 유지 또는 model switch/delegation·fallback/reviewer 선택은 위 [fallback 순서](#두-축-routing)와 [Model Role Qualification](#model-role-qualification)을 적용한다.

## Packet과 영향 결과 인계

배정 뒤 packet을 만들거나 소비하는 시점에 필요한 계약만 읽는다.

- worker 지시·첫 edit 전 입력 확인: [Execution Packet](execution-packets.md#execution-packet).
- worker 결과 반환·finishing의 결과 소비: [Result Packet](execution-packets.md#result-packet).
- required reviewer 입력·결과 확인: [Review Packet](execution-packets.md#review-packet). Large 리뷰 순서와 진행·중단 조건은 [설계 리뷰](../../process/design-review.md#large-설계-이중-독립-리뷰)를 함께 적용한다.
- P가 선언한 영향 분석 결과 소비: [공통 영향 결과 참조와 로컬 소비](execution-packets.md#공통-영향-결과-참조와-로컬-소비).

fixture 평가·직렬화·token proxy 측정은 [skill-evals의 Packet 직렬화와 측정](../../process/skill-evals.md#packet-직렬화와-측정)을 따른다. 운영 배정의 선행 입력으로 읽지 않는다.
