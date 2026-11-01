# 프로젝트가 발전시키는 W와 명시적 활성화

- 상태: preview.8 구현 후보; 공개 전 검토
- 제안자: Codex, 소유자의 적용 관점 반영
- 작성일: 2026-11-01
- 관련 Issue: 없음
- 변경 대상: `tools/agentics.py::resolve`, `workflow/activation.md`, `methodology/core.md` 적용 범위

## 문제

| 경계 | 기존 설치 | preview.8 권장 경로 |
| --- | --- | --- |
| M | 고정 사본의 지속 준수를 전제 | 최초 참고, 이후 지속 사용·업데이트는 사용자 판단 |
| W | 공개 사본을 통째 교체 | 프로젝트가 절차까지 수정하며 발전 |
| P | 방법론 번들·스킬·상시 AGENTS 구간 | 제품 원본·공통 규칙·권한, 선택적 영역 연결 |
| 활성화 | 저장소 진입 때 자동 적용 | 사용자가 작업·대표 영역을 선택할 때만 |
| SHA | 공개 사본과 생성물 유지 | 작업에 선택한 프로젝트 W 식별 |

근거: `adaptive-sdd/templates/blocks/AGENTS.block.md.tmpl`의 Start order와 always-applied 선언, `adaptive-sdd/tools/install.py::plan_outputs`, `adaptive-sdd/workflow/README.md`의 기존 설치 정의. 변경 후 근거: `adaptive-sdd/tools/agentics.py::resolve`, `adaptive-sdd/workflow/activation.md`, `adaptive-sdd/methodology/core.md` 첫 적용 범위 문단.

배경은 [방법론을 강요하지 않고 공유하는 방법](https://seok-jun.github.io/ai-agent-diary/series/agent-sdd/010-agentics-sharing-methodology/)의 공통 규칙/선택 방법론 분리다. 해당 글은 아이디어 단계이며 M/W/P 업데이트 프로토콜을 확정한 문서는 아니다. M의 지속 사용은 사용자 판단이라는 이번 소유자 결정을 명시적 설계 기준으로 삼았다. 이전의 모든 구현이 당시 결정에 위배됐다는 역사적 결론은 내리지 않는다.

## 변경 조건

활성화·소유·설치 public contract 변경이다. 대상 저장소에 별도의 필수 review 번호 체계가 확인되지 않아 템플릿의 1~7을 임의로 부여하지 않는다. 변경 후 독립 Claude 리뷰를 수행하고 실행 검증과 분리해 기록한다.

## 선택지

| 선택지 | 동작/구조 | 장점 | 위험/비용 |
| --- | --- | --- | --- |
| A: 새 외부 적용 경로 | 수정 가능한 프로젝트 W, 연결만 P에, 명시 선택 | 소유자의 독립 발전 모델에 맞음 | 최초 W 적용 문서 작성, 새 세션 전환 필요 |
| B: 위치와 기본값만 변경 | 기존 renderer 유지, 외부 설치 기본, AGENTS 생성 선택 | 이전 비용 일부 감소 | 기존 W의 생성 hard guard·pin 전제가 남아 활성화 문제 미해결 |

A를 목표로 구현한다. 기존 설치기는 명시적인 호환 경로로만 유지한다. 점진 이전은 A에 도달하는 순서이며 B를 최종 구조로 간주하지 않는다. 새 경로의 자동 scaffold/host loader는 이번 범위에서 구현하지 않고 실제 제공 범위를 명시한다.

## 활성화 계약

| 상태 | 읽기/적용 | 금지 | 판정 가능한 수용 기준 |
| --- | --- | --- | --- |
| 미선택 | P 공통 규칙만 | 연결 부재를 이유로 중단, W 절차·기록 강제 | `resolve(..., selected=False)`가 파일/Git 접근 없이 INACTIVE |
| 선택·연결 없음 | 선택 입력만 확인 | 일반 모드로 조용히 전환 | BLOCKED exit 2, 쓰기 없음 |
| 선택·출처 없음 | 사용자 허용 목록 확인 | P가 지정한 임의 원격 실행 | 미매핑 이름 거부 |
| 선택·SHA/origin 불일치 | 로컬 Git 식별 확인 | 최신판 fetch·대체 | 선택 commit과 다른 HEAD/origin 거부 |
| 선택·필수 파일 실패 | 입구·선언 P 원본 존재 확인 | 접근 실패를 읽기 성공으로 기록 | 누락/탈출 경로 거부 |
| READY | Agent가 입구·해당 P/W를 읽고 기록 접근/권한 확인 | READY를 실제 수행/활성화 증거로 간주 | resolver 결과와 실제 읽기·작업 증거 구분 |
| 활성 작업 | 선택 W snapshot, 전체 영향 영역의 P 규칙 | 중간 W 수정으로 gate 우회 | 선택 commit과 소비 문서, 실제 수행을 기존 작업 기록에 연결 |
| 작업 종료 | 선언 위치에 종료 증거 보존 | 종료 선언으로 문맥 삭제 주장 | 다음 작업은 새 세션에서 선택 |
| 대표 영역/방법 전환 | 새 세션·명시 선택·재확인 | 이미 읽은 W를 지웠다고 가정 | fresh-session 선언과 새 작업 식별; 호스트 강제는 미구현 |
| 다른 영역 코드 수정 | 대표 W 하나 + 영향 영역 P 규칙 | 두 번째 방법 자동 활성화 | 충돌하는 P 요구는 의존 작업만 중단·질문 |

코드 근거: `agentics.py::resolve`, `::connection`, `::within`, `::main`. Agent 수행 근거: `workflow/activation.md::Task boundaries`. **추론/한계:** read-only resolver가 Agent의 실제 사용 의사나 새 세션을 관측할 수는 없다. 플래그는 호출자 선언이다. 선택되지 않은 세션에 W를 넣지 않는 것은 호스트 사용 절차의 책임이다.

## 목표 구조와 스키마

실제 트리·관계도·세 스키마 예시는 [적용 가이드](../../ko/docs/customization.md)에 있다. P 연결에는 methodology/version/전체 W commit만 둔다. 사용자 허용 목록은 P 밖에서 이름을 승인 origin과 기기별 root에 연결한다. cloud도 같은 origin/commit을 별도 경로에 준비한다. 자체 일치 manifest만으로 출처를 인증하지 않는다. 원격 획득과 로더 최초 배포의 신뢰 설정은 사용자 책임이다.

`profile.json`은 입구·P 원본 참조·기록 선언이다. 방법론 선호는 외부 `project/*.md`에서 직접 관리한다. 제품 원본을 외부에 복제하지 않는다. `product_sources.revision=task-start`만 구현했다. HEAD와 dirty 상태를 출력하지만 실제 dirty 출처의 content identity와 기록 접근 확인은 Agent가 한다.

## 기존 project.json 필드의 이동

분류는 키 이름이 아닌 값의 의미로 한다. 표는 `adaptive-sdd/templates/project.example.json`의 최상위 키를 모두 포함한다.

| 기존 키 | P 원본/권한 참조 | 외부 W 선택·설정 |
| --- | --- | --- |
| schema | 없음 | 기존 포맷 식별; 새 profile은 별도 schema |
| project | 제품 이름·팀 convention 원본 | 대화·산출물 언어 선호(팀 필수면 P 참조) |
| tools | 제품/조직의 도구 금지 | 선택 호스트 |
| tracker | 기존 작업 체계·접근·작성 권한 | adapter·ID 매핑; 기록 선언과 연결 |
| docs | 업무·구조·문서 index 원본 | SDD·리뷰 산출물의 명시적 선택 위치 |
| grade_mapping | 제품이 강제한 위험 조건 | 방법론 등급 매핑 |
| human_judgment | 승인·위임·확인자·제품 판단 지점 | 추가 방법론 판단 지점; 권한 완화 불가 |
| worktree_root | 조직 경로 제한 | 사용자 작업 경로 |
| build | 빌드 사실·필수 검증·테스트 보존 규칙 | 검증 순서/환경 선택의 허용 범위 |
| modules | 모듈·경계·공유 계약 원본 | 원본 경로 참조 |
| routing | 모델 금지·예산·승인·역량 근거 원본 | 역할별 선택 선호; 금지 우회 불가 |
| priority | 제품 단계·우선순위 결정 | 작업 정렬 방식 |
| evidence | 비밀·개인정보·공개·보존 권한 | 허용된 기록 수단 선택 |
| visual_spec | 제품 화면 결정 원본 | 작업용 명세 위치/수단 선택 |
| token_diagnostic | 수집·공개·비용 권한 | 허용 범위 내 진단 사용 여부 |
| hard_guard_extra | 항목별 공통 규칙/권한 원본 | 항목별 방법론 절차; 일괄 이동 금지 |
| skill_eval | 평가 데이터의 보호·실행 권한 | W 평가 사례·명령 |
| git | 제품 원격·병합 대상·권한 | 허용된 작업 전략 |
| review | 리뷰 권한·공개 대상 제한 | single/dual·리뷰어 선택·외부 리뷰 위치 |
| sdd | 제품 필수 문서 조건 | full/condensed 선호 |

## 현재 hard guard 분류

근거: `adaptive-sdd/templates/blocks/AGENTS.block.md.tmpl::Always-applied hard guard`. 공통 후보라는 분류가 P에 새 규칙을 승인하거나 삽입하지 않는다.

| 항목 | 분류·처리 |
| --- | --- |
| 무관한 변경 reset/checkout/clean/revert 금지 | 공통 보호 규칙 후보 |
| 비밀·개인정보 금지 | 공통 보호 규칙 후보; P 정책 참조 |
| 대화 원문 금지·요구/결정 기록 예외 | P 정보 보호와 방법 기록 절차를 분리 |
| 존재하지 않는 이름 추측 금지 | 공통 정확성 규칙 후보 |
| Issue 밖 변경 금지 | 범위 권한은 P, Issue 표현은 W |
| Allowed/Forbidden edits | P 작업 권한 + W 표현 방식 |
| 통합 경로·일반 lane 제한 | 제품 경계 원본 P + lane 절차 W |
| 활성 lane 겹침 금지 | W 조율 방식; 팀 공통 채택 시 P 원본 |
| 미실행 PASS 금지·완료 판단 | 검증 사실은 공통 후보, 완료 절차는 W |
| 현재 shell 우선 | W 실행 지원; 조직 제한은 P |
| UTF-8 우선 | W 읽기 지원 |
| 고정 사본·생성물 수정 금지 | 기존 설치 계약; 새 W 영구 수정 금지로 이식하지 않음 |
| 판단 지점·위임을 Agent가 만들지 않음 | P 권한 원본 유지; M 미선택 때도 권한 생성 불가 |
| hard_guard_extra | 실제 항목별 분류; 자동 위임/완화 금지 |

## 기존 W 재사용과 이견

등급·SDD·검증·리뷰·tracker·작업 격리 절차는 시작본으로 재사용한다. 프로젝트는 그 절차도 바꿀 수 있다. 현재 네 스킬의 기존 입력과 고정 사본 표현에는 새 activation 계약을 연결했다. profile의 paths.workflow/supports로 절대 실행 경로를 출력하며 supports는 M 호출부를 제거한 W에서 null일 수 있다. 선택한 시작본의 보호 규칙은 별도 task-guard.md로 읽는다. `W/../project/`는 외부의 직접 수정 가능한 적용 문서이며 P 원본과 선호를 구분한다. 이전 lock 참조는 작업 W commit과 P revision으로 대체한다. 변경 근거: `workflow/activation.md::Meaning of M, W and P after adoption`, 네 `skills/*/SKILL.md`의 진입 문장.

**이견:** 초안은 사람 판단 지점 전체를 방법론 선호로 분류했다. 기존 template은 판단 지점과 명시적 위임을 함께 담고 있다. 권한까지 선택 해제되는 것을 막기 위해 위 표처럼 분리했다. 또한 작업 기록 의무를 공개 M의 영구 요구로 만들지 않았다. 시작본을 선택하는 범위에서는 해당 기록 절차를 유지하며 프로젝트가 W를 변경할 수 있다.

**한계:** 호환 의미를 입구에서 정의하므로 기존 절차를 읽는 Agent가 이를 실제로 지키는지는 별도 행동 검증이 필요하다. 단위 테스트나 텍스트 리뷰로 이를 입증하지 않는다. 장기적으로 프로젝트가 재사용하지 않는 절차와 오래된 용어를 정리할 수 있으며 모든 W의 자동 재작성은 제공하지 않는다.

## 영향 범위

- 공개 배포: 양쪽 M 적용 범위, W 입구, 새 resolver, 문서·manifest·테스트.
- P 변경: 이번 출시 준비에서는 없음. 기존 P overlay·생성 지침 제거는 별도 이전 대상이다.
- DB/migration: 데이터베이스 변경 없음. 설치 모델 이전은 수동 검토 절차.
- secret/개인정보: 공개 예시는 가상이며 개인 제품의 경로·Issue·내용을 넣지 않는다.
- 비용: 자동 모델 호출이나 외부 게시 없음. 요청받은 Claude 리뷰만 별도 수행한다.

## 제외 범위와 미해결 항목

- 실제 태그·release 게시, 기존 제품 자동 이전, 자동 W 생성, native host loader 배포.
- 버전 폐기/취약 공지 feed와 자동 업그레이드. 사용자 판단으로 매핑/commit을 거부할 수 있다.
- 클라우드 자동 provisioning. 같은 origin/commit과 로더를 준비하는 절차만 제공한다.
- resolver의 session lifecycle 강제·실행 증명. fresh-session은 호출자 선언이다.
- 실행 효과·비용 우수성 실험은 출시 gate로 추가하지 않는다.

## 검증 기준

- [x] 미선택에서 파일/Git 접근 없음; 선택 실패는 BLOCKED, 쓰기 없음.
- [x] W 변경 후 새 commit 선택 가능; 공개 M 파일/연결 없이 성공.
- [x] P checkout을 옮겨도 같은 연결 동작; P dirty 변경 보존.
- [x] origin·SHA·경로·중복 키·누락 출처·기록 선언 오류 거부.
- [x] 기존 installer 회귀·두 판 대응·manifest·문서 링크 검사.
- [x] 변경 후 Claude 독립 리뷰와 지적 처리 기록. 실행 테스트와 구별.

실행 결과와 미실행 범위의 최신 원본은 [출시 준비 기록](../releases/preview.8.md)이다.

## 결정 질문

이미 정한 방향을 재승인받는 질문이 아니라 이후 확장 선택이다.

1. 다음 단계에서 A: Agent 지원 W 구성 절차 유지 / B: 자동 scaffold 도구 추가?
2. 호스트 진입은 A: 명시적 경로 읽기 유지 / B: 개인 native loader 배포 추가?
3. 기존 프로젝트 이전은 A: 별도 검토 PR / B: 현재 설치 유지? 이번 공개 준비는 A/B를 대신 결정하지 않는다.
