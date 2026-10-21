# SDD 작업 문서

Medium·Large의 해당 문서를 작성·수정할 때 필요한 절만 읽는다. Trivial·Small 및 Epic 관리 문서 자체에는 SDD 디렉터리를 요구하지 않는다. 문서 역할·수명은 [sdd-workflow](sdd-workflow.md#문서-역할), 검증 대응과 실행은 [verification](verification.md)이 원본이다.

| 작성 대상 | 읽을 절 |
| --- | --- |
| 폴더·작업 인덱스 | [구조](#sdd-작업-문서-구조), [README](#readmemd) |
| 현재 동작·조사 근거 | [AS-IS](#01-as-ismd) |
| 목표 동작·결정·완료 기준 | [TO-BE](#02-to-bemd) |
| 실제 변경 지시와 검증 세부 | [change-plan](#change-plansidmd) |
| 실제 경쟁 대안 발견 | [Bounded trade-off capture](#bounded-trade-off-capture) |

## SDD 작업 문서 구조

Medium 이상에서 다음 구조를 사용한다. 새로 시작하는 SDD 작업부터 적용하며, 이미 진행 중인 작업과 종료된 작업에는 소급 적용하지 않는다. 이 규칙만으로 기존 설계를 재작성하지 않는다.

```text
docs/sdd/{feature}/
  README.md
  01-as-is.md
  02-to-be.md
  change-plans/{ID}.md
```

필요한 경우에만 `backlog/{ID}.md`를 추가한다. `{feature}`는 kebab-case, `{ID}`는 Issue 안에서 중복되지 않는 대문자 prefix + 번호를 사용한다.

각 문서의 필수 내용은 다음과 같다.

사람용 현황·계획에는 [사람용 문서의 시각적 작성](agent-instruction-policy.md#사람용-문서의-시각적-작성)을 적용한다. 현재 모습과 변화·선택을 먼저 보여주고 Agent 실행 세부는 분리한다. 한 문장으로 충분한 변경은 그 문장으로 설명하며 그림 개수를 채우지 않는다. 표현 선택에 예시가 필요하면 [작성 예시](visual-writing-examples.md)만 참고한다. 이 연결은 문서 구조·승인 권한·review 회차를 바꾸거나 전체 가이드의 선행 로딩을 요구하지 않는다.

### `README.md`

- Issue 번호
- Priority
- grade
- 수정 허용/금지 경로
- 연결된 business/architecture 문서

### `01-as-is.md`

- 문제 정의·원인 모델·범위/경계와 설계에 영향을 주는 핵심 사실·위험을 먼저 짧게 제시
- 현황 이해에 필요한 소유·연결·흐름·상태는 관계도나 작은 표로 먼저 보여주고 사실·가설·미조사를 구별. 단순 변경은 한 문장 허용
- 현재 동작과 확인하지 못한 사실을 구분한 Agent evidence
- 확인한 코드 경로와 심볼
- 재현 또는 검증 근거
- 문서와 코드가 다르면 drift 항목

작성 순서는 문제 → 현재 관계·동작 → 사실/가설/미조사 → 직접 근거로 잡는다. 구체적인 표현이 필요할 때만 W의 [AS-IS 합성 예시](visual-writing-examples.md#sdd-as-is)를 참고한다. 예시의 가상 사실을 실제 제품 근거로 사용하지 않는다.

### `02-to-be.md`

Human Decision Contract다. Issue의 목표·경계와 상위 contract 안에서 제품·설계 결정의 기준이 되며, 이들을 독자적으로 변경하지 않는다.

- 현재 문제와 AS-IS → TO-BE 동작 변화. 정책·선택지는 비교표, 소유·경계는 관계도/경계 표, 흐름·상태는 다이어그램/상태표 등 이해에 필요한 표현을 먼저 둔다. 단순 변경은 한 문장 허용
- 변경하지 않을 동작, 실패/오류 시 동작, 명시적인 데이터/상태 정의
- Decision별 `D-xxx`, 선택, 선택 이유, 실제 대안과 trade-off, 주요 비용/위험, 채택하면 생기는 의미
- Acceptance Criteria별 Verification Strategy. 실행 세부는 해당 change-plan을 참조한다.

클래스/메서드/line evidence는 최소화한다. 중요한 제품·설계 결정을 Agent spec에만 숨기지 않는다. Human-facing Decision이 짧은 리뷰 세션에서 이해하기 어려울 만큼 많으면 issue/plan 분리를 검토하되 고정 개수 상한이나 추가 taxonomy는 만들지 않는다.

작성 순서는 변화 → 선택과 이유·비용 → 유지할 경계와 실패·미결 → 완료 기준과 확인 방법으로 잡는다. 필요한 경우만 [TO-BE 합성 예시](visual-writing-examples.md#sdd-to-be)를 참고한다. 위 현황·계획 예시의 전체 선행 로딩이나 새 산출물은 요구하지 않으며, 실행 세부는 기존 change-plan의 해당 절로 연결한다.

### `change-plans/{ID}.md`

Agent Execution Spec이다. Human Decision의 rationale을 다시 서술하지 않고 적용하는 `D-xxx`를 참조한다. `02-to-be.md`와 경쟁하는 설계 권위를 만들지 않는다.

- target file/symbol과 직접 caller/callee, 필요한 코드 근거
- 변경 내용·구현 순서·보존할 invariant, 해당하는 schema/migration
- test case·검증 명령·실행 evidence
- 롤백 또는 실패 시 확인 지점

`관련 파일`, `필요한 부분`, `적절한 처리`처럼 정확한 대상을 특정하지 않는 문장을 change plan에 쓰지 않는다.

### Bounded trade-off capture

Issue, current main AS-IS, direct dependency를 확인하는 과정에서 실제 경쟁 선택지가 둘 이상 드러난 경우에만 선택, 대안, 선택 이유, 감수 비용을 짧게 기록한다. Medium 이상에서 중요한 제품·설계 trade-off는 `02-to-be.md`의 Decision에 두고 change-plan은 그 ID를 참조한다. Trivial/Small은 Issue를 사용하며 별도 trade-off 문서를 만들지 않는다.

경쟁 선택지를 찾기 위한 repository-wide 탐색이나 별도 brainstorming은 하지 않는다. 재검토 조건도 이미 명확한 trigger가 있을 때만 기록한다.
