# SDD grade

## SDD grade

실행 Issue의 grade는 다음 네 값만 사용한다. Epic은 실행 등급과 별개인 선택적 관리 단위다.

| grade | 판정 조건 |
| --- | --- |
| **Trivial** | runtime/contract/test expectation/build·dependency/schema·migration/CI·workflow 실행 의미를 바꾸지 않는 문서·문구·링크·주석·비동작 metadata 정리 |
| **Small** | Trivial이 아니며 한 구현 모듈 안에서 끝나고 아래 자동 격상 조건이 하나도 없는 변경 |
| **Medium** | 두 개 이상 구현 모듈 또는 프로젝트가 지정한 공유 contract가 바뀌지만 Large 조건은 없는 변경 |
| **Large** | 보안·개인정보·DB 마이그레이션·백그라운드 재시도/스케줄·비용/quota처럼 실패 영향이 큰 변경 |

Trivial은 **파일 수가 적다는 이유만으로 선택하지 않는다.** 다음 조건을 모두 만족해야 한다.

- 제품 runtime 동작과 사용자 관찰 결과가 바뀌지 않는다.
- public/internal contract, 테스트의 기대 동작, build/dependency, DB schema/migration이 바뀌지 않는다.
- CI, Skill, agent workflow의 실행 step·gate·stop condition 의미가 바뀌지 않는다.
- 보안·개인정보·비용·quota 정책의 의미가 바뀌지 않는다.

대표 예시는 오타/맞춤법 수정, 깨진 링크의 목적지 교정, 동작 의미를 바꾸지 않는 설명 문구·주석 정리, 현재 상태를 반영하는 비동작 metadata 갱신이다. 실행 코드·테스트·빌드 설정·workflow 실행 규칙을 바꾸거나 문서 변경 자체가 agent/product 동작을 바꾸면 최소 Small이다.

### 일반 자동 격상

여러 조건이 해당하면 가장 높은 grade를 적용한다. 프로젝트는 구체적인 모듈·기술·업무 경로를 아래 위험에 매핑하며 공통 최소 등급을 낮추지 않는다. 공유 contract 격상 대상은 프로젝트 매핑에서 지정한다. 단일 모듈의 다른 contract를 이름만으로 이 대상에 추가하지 않는다.

| 변경 행위 | 최소 grade |
| --- | --- |
| 두 개 이상 구현 모듈 또는 프로젝트가 지정한 공유 contract 변경 | Medium |
| 비밀정보·대화 원문·개인정보 저장·전송·로그 정책 변경 | Large |
| DB schema/migration 변경 | Large |
| 백그라운드 재시도·스케줄·중복 실행 방지 정책 변경 | Large |
| 과금 경로·비용 계산·quota/상한 변경 | Large |

새 패키지·모듈 신설이나 의존성 방향 변경만으로 Epic 생성 또는 작업 분해를 강제하지 않는다. 실제 변경 범위와 위 위험 조건으로 실행 grade를 판정한다.

자동 격상 기준보다 낮은 grade를 사용하려면 사용자의 명시적 예외 지시가 Issue 본문에 기록되어 있어야 한다. agent가 스스로 낮추지 않는다.
