# SDD to-be

### `02-to-be.md`

Human Decision Contract다. Issue의 목표·경계와 상위 contract 안에서 제품·설계 결정의 기준이 되며, 이들을 독자적으로 변경하지 않는다.

- 현재 문제와 AS-IS → TO-BE 동작 변화. 정책·선택지는 비교표, 소유·경계는 관계도/경계 표, 흐름·상태는 다이어그램/상태표 등 이해에 필요한 표현을 먼저 둔다. 단순 변경은 한 문장 허용
- 변경하지 않을 동작, 실패/오류 시 동작, 명시적인 데이터/상태 정의
- Decision별 `D-xxx`, 선택, 선택 이유, 실제 대안과 trade-off, 주요 비용/위험, 채택하면 생기는 의미
- Acceptance Criteria별 Verification Strategy. 실행 세부는 해당 change-plan을 참조한다.

AS-IS에서 미확인으로 남긴 외부 동작을 설계 사실로 확정하지 않는다. 설계 결정을 좌우하는 전제는 [조사 근거](as-is.md#판단에-필요한-조사)로 확인하거나 [미결 사항과 단계별 의존성](issue.md#미결-사항과-단계별-의존성)에 따라 확인 담당·필요 시점을 연결한다. 실행으로만 확인할 수 있는 전제는 해당 검증/구현 인계에 남기고, 전제에 의존하는 실행 전에 확인한다.

클래스/메서드/line evidence는 최소화한다. 중요한 제품·설계 결정을 Agent spec에만 숨기지 않는다. Human-facing Decision이 짧은 리뷰 세션에서 이해하기 어려울 만큼 많으면 issue/plan 분리를 검토하되 고정 개수 상한이나 추가 taxonomy는 만들지 않는다.

작성 순서는 변화 → 선택과 이유·비용 → 유지할 경계와 실패·미결 → 완료 기준과 확인 방법으로 잡는다. 필요한 경우만 [TO-BE 합성 예시](../visual-writing-examples.md#sdd-to-be)를 참고한다. 위 현황·계획 예시의 전체 선행 로딩이나 새 산출물은 요구하지 않으며, 실행 세부는 기존 change-plan의 해당 절로 연결한다.

### Bounded trade-off capture

Issue, 선언한 기준 revision의 AS-IS, direct dependency를 확인하는 과정에서 실제 경쟁 선택지가 둘 이상 드러난 경우에만 선택, 대안, 선택 이유, 감수 비용을 짧게 기록한다. Medium 이상에서 중요한 제품·설계 trade-off는 `02-to-be.md`의 Decision에 두고 change-plan은 그 ID를 참조한다. Trivial/Small은 Issue를 사용하며 별도 trade-off 문서를 만들지 않는다.

경쟁 선택지를 찾기 위한 repository-wide 탐색이나 별도 brainstorming은 하지 않는다. 재검토 조건도 이미 명확한 trigger가 있을 때만 기록한다.
