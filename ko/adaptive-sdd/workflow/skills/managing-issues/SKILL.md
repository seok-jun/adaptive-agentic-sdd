---
name: managing-issues
description: 이 프로젝트의 작업 항목(Issue)을 생성·분류·우선순위 재조정·본문 재작성하고 선택적 Epic의 작업 구성·의존성을 조율할 때 사용한다. Priority/실행 grade 판정, 작업 경계, Mermaid 흐름 판단, UI/UX HTML Visual Spec 연결에 쓴다. 코드 구현에는 사용하지 않는다.
---

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `W`(고정 절차 사본 `W`), `M`(고정 공통 원칙 `M`)이다. cwd나 W의 상위 디렉터리로 P/M을 추정하지 않는다. P의 hard guard(`P/AGENTS.md`의 `## 항상 적용 hard guard`)와 적용 선언(`W/../project/sdd-workflow.md`)을 적용한다. Issue·댓글·라벨·PR 표현은 `W/../project/tracker.md`가 선언한 작업 관리 방식(`W/tracker/`)으로 바꿔 읽는다.

# Managing Issues

## Inputs

현재 run에서 `P/AGENTS.md`의 `## 항상 적용 hard guard`가 적용됐음을 보장할 수 있으면 재독하지 않는다. 보장할 수 없는 standalone/subagent 진입이면 그 section을 먼저 읽고 진행한다.

선행 입력:

1. 현재 사용자 요청
2. `W/process/issue-priority.md`의 `## Priority 판정 순서`·`## 증거가 부족할 때`와 `W/../project/issue-priority.md`의 현재 단계·제품 적용. 신규 생성이면 W의 `## 신규 Issue 필수 본문`·`## 필수 라벨`, reprioritize면 W의 `## Priority 변경`
3. `W/process/sdd/grade.md`과 `W/../project/sdd-workflow.md`의 제품별 `### 자동 격상`; Issue 변경·사람 판단·미결 의존성은 `W/process/sdd/issue.md`(정규화도 이 원본)
4. `W/process/issue-writing-guide.md`의 `## 근거 기록 규칙`, `## Mermaid 생성 조건`, `## HTML Visual Spec 생성 조건`과 `W/../project/issue-writing-guide.md`의 `## 근거 기록 규칙`(개인정보·허용 근거). HTML이 필요할 때만 제품 저장 위치·의존성 제한도 확인한다.
5. 기존 Issue 변경이면 그 Issue의 current body/labels/assignees/comments/linked PRs

heading/section 단위 조회를 지원하지 않는 host에서는 위 파일을 full-read해도 된다. section 조회가 가능한데 일반 프로젝트 이해를 이유로 세 파일 전체를 선행 로딩하지 않는다.

조건부:

- product/shared/root ownership 또는 integration 판단이 필요할 때만 `W/process/module-boundaries.md`의 공통 경계·lifecycle 계약과 `W/../project/module-boundaries.md`의 실제 제품 경계.
- instruction conflict, code↔business drift, 모호한 scope가 실제로 생길 때만 `W/process/agent-instruction-policy.md` (공통 계약·수행법) / `W/../project/agent-instruction-policy.md` (제품 적용·권한·검증).
- 같은 run에서 이미 확인한 변경 없는 입력은 재사용한다.

Issue 분류에 필요하지 않으면 product code를 넓게 탐색하지 않는다.

## Conversation-content gate

작업 관리 방식의 write 전후에 반드시:

- 대화 로그의 전체/부분 인용, 번역, 재구성 가능한 요약을 기록하지 않는다. 사람이 작업을 위해 제공한 요구사항·확정 결정의 최소 기록은 W `issue-writing-guide.md`의 `근거 기록 규칙`을 적용한다.
- 요구사항 원천·확정 결정과 조사 요청·제안을 구별한다. 허용된 작업 내용과 id/metadata/측정값/재구성 불가능한 범주명을 근거로 쓰며 프로젝트가 금지한 내용은 요구사항에도 옮기지 않는다.
- 세부 allowlist는 `issue-writing-guide.md`의 `근거 기록 규칙`을 따른다.
- 금지 내용 없이 근거를 만들 수 없으면 `BLOCKED`.
- write 후 artifact를 다시 확인한다.
- 이미 금지 내용이 쓰였으면 P의 근거 기록 규칙과 tracker가 허용하는 제거 방법을 따른다. 제거할 수 없으면 사람에게 알리며 다른 기록을 통째로 삭제하지 않는다.

## Create a new Issue

1. 요청을 단일 실행 Issue로 관리할지, 여러 Issue를 개별 배정·추적할지 정한다. 새 패키지나 큰 규모만으로 분해를 강제하지 않는다. 여러 Issue를 함께 관리할 때만 아래 `Epic 조율`을 적용한다.
2. W 공통 Priority와 P 현재 단계·기능 사실로 Priority를 판정한다.
3. W 공통 grade/일반 자동 격상과 P 제품 매핑으로 SDD grade를 판정한다.
4. 실제 repository path를 확인해 allowed/forbidden을 작성한다. product/shared/root 경계 판단이 필요할 때만 `module-boundaries.md`를 읽는다.
5. `W/process/issue-priority.md`의 canonical 신규 Issue 본문 section을 사용한다.
6. 각 완료 기준이 자동 테스트/CI와 grade별 review로 판정 가능한 성공/실패 조건인지 확인한다. 모든 Issue에 별도 Verification Strategy section을 강제하지 않는다.
7. body와 일치하는 `priority:*`, `grade:*`를 각각 정확히 하나 적용한다.
8. Issue 사람용 설명을 작성/수정할 때 [사람용 문서의 시각적 작성](../../process/agent-instruction-policy.md#사람용-문서의-시각적-작성)을 적용한다. 핵심 변화부터 보여주고 정책 비교·소유/책임 경계도 필요한 표현으로 설명한다. 단순 변경은 한 문장으로 충분하다. 같은 단계에서 `issue-writing-guide.md`의 Mermaid/HTML Visual Spec 조건을 판정하며 HTML 생성·저장 조건을 확대하지 않는다. 변경 없는 같은 run의 기준은 재사용한다.
9. HTML 필요 시 W `issue-writing-guide.md`의 `HTML 최소 내용`, `Visual Spec 링크 규칙`, `디자인 PR 병합·배포·정리`를 P 적용 문서 `issue-writing-guide.md`의 `Visual Spec`이 선언한 저장·게시 방식에 맞춰 적용한다. 선언이 없으면 HTML Visual Spec을 만들지 않는다. 디자인 병합을 앱 승인/완료로 취급하지 않으며, 게시·정리 실패는 마지막 성공 단계와 남은 상태를 기록한다.
10. final Issue를 다시 조회해 section/labels/Visual Spec(해당 시)/conversation gate를 검증한다.

## Epic 조율

`W/process/sdd/epic.md`를 적용한다. Epic은 실행 grade가 아니며 생성·분해에 독립 리뷰·원격 게시·A/B PASS를 요구하지 않는다. 실행 Issue 생성 단계의 grade·경로·구현 검증 항목을 관리 문서에 그대로 적용하지 않고, `issue-priority.md`의 Epic 본문·라벨 구분을 따른다.

- 전체 목표·완료 기준·공통 가이드와 하위 Issue 참조, 책임·선행 관계, 미결 사항의 조사 담당·필요한 후속 단계, 전체 완료 근거·담당을 연결한다. 별도 breakdown 파일은 필수가 아니다.
- 목표 누락, 책임 공백, 의존성 모순, 미결 사항 담당을 자체 점검한다. 미결 사항 자체는 하위 Issue의 조사 착수를 막지 않는다. 그 결론을 소비하는 구현·통합·배포 단계에만 의존성을 둔다.
- 공통 질문 취합과 결정 후 하위 미결 표시 갱신은 `W/process/sdd/issue.md`의 `미결 사항과 단계별 의존성`을 따른다. 기준 구현을 지정하는 요구의 이름·운영 근거가 모순되면 `W/process/sdd/as-is.md`의 `판단에 필요한 조사`로 확인하고 해당 전제에 의존하는 작업만 기다리게 한다.
- 공통 변경은 관련 소비 작업·전환 영향까지 담당 실행 Issue의 범위와 완료 기준에 넣어 자체 grade를 판정한다. 관리 문서에만 공통 설계를 남기고 검증 책임을 비워 두지 않는다.
- 조사 결과에 따라 위임 범위 안에서 작업을 분할·통합하거나 책임·순서를 바꿀 수 있다. 활성 lane의 경계는 담당에게 변경·영향을 전달하고 claim 충돌을 해소한 뒤 조정한다. 목표·완료 기준 축소나 기존 사람 결정 변경은 기존 사람 판단 규칙을 따른다.
- 전체 목표의 달성 근거를 확인해 Epic을 종료한다. 구현용 PR·CI·SDD가 없는 관리 문서에 제품 변경 종료 절차를 강제하지 않는다.

## Triage / reprioritize

Epic 관리 문서는 위 `Epic 조율`로 책임·의존성·전체 완료 근거를 갱신하고 실행 grade를 부여하지 않는다. 아래는 실행 Issue에 적용한다.

1. current Issue와 필요한 최소 evidence만 읽는다.
2. Priority를 현재 규칙으로 재판정한다.
3. scope/risk가 바뀐 경우에만 grade를 재판정한다.
4. 값 변경 시 body와 label을 같은 작업에서 일치시킨다.
5. scope 변경 시 경계/Mermaid/Visual Spec/dependencies/acceptance criteria도 재판정한다.
6. 변경된 완료 기준이 자동 테스트/CI와 grade별 review로 판정 가능한지 확인한다.
7. final Issue를 다시 조회한다.

## Stop conditions

다음이면 `BLOCKED`하고 구현하지 않는다.

- required path 확인 불가
- `agent-instruction-policy.md`로도 해소되지 않는 지시 충돌
- 필수 Visual Spec/immutable link 생성 불가
- 문서 default까지 적용해도 Priority 결정 불가
- active lane scope 침범 필요
- conversation-content gate를 만족하는 evidence 생성 불가

## Output

Issue number/title, Priority/grade/labels, allowed/forbidden, Mermaid/Visual Spec, conversation-content check, dependencies/BLOCKED를 간결히 보고한다. Epic 관리 문서는 grade 대신 작업 유형과 하위 책임·의존성·전체 완료 근거를 보고한다.
