# build-preflight.md 수행 절차

입력은 명시한 P/W/M 절대 root다. 빌드 도구·JDK 버전·추가 JDK 후보·정리 명령·기기 절차·설치 금지 조건은 P 적용 문서 `P/.adaptive-sdd/project/build.md`가 선언한다. 이 문서는 그 선언을 실행하는 공통 순서다. 선언이 없거나 빈 값이면 추정하지 않고 해당 단계를 미검증으로 남긴다.

## 적용 대상

`build.md`가 선언한 빌드·테스트·정리 명령을 실행하기 전에만 적용한다. 문서·문구만 바꾸는 Trivial처럼 빌드 결과에 영향이 없는 변경에는 적용하지 않는다.

## JDK resolve order

JVM 기반 빌드 도구(예: Gradle, Maven)를 쓰는 프로젝트에서 적용한다. 아래 순서에서 처음 사용 가능한 JDK를 선택한다.

1. 현재 shell에서 `java` command를 실행할 수 있으면 그대로 선택한다.
2. `JAVA_HOME`이 비어 있지 않고 그 아래 `bin/java`(`bin/java.exe`)가 실행 가능하면 해당 JDK를 선택한다.
3. `build.md`가 선언한 추가 JDK 후보 경로만 확인한다.

경로가 존재하는 것만으로 성공으로 판정하지 않는다. 선택한 JDK로 `java -version`을 한 번 실행해 성공해야 resolve 완료다. 현재 `java`가 실행되지 않거나 후보 검증이 실패하면 다음 순서로 진행한다. 후보 탐색은 위 목록으로 한정한다. filesystem 전체 scan이나 repository-wide 탐색으로 JDK를 찾지 않는다.

required 빌드 검증이면 resolve한 JDK가 아니라 **빌드 도구가 실제로 쓰는 launcher/daemon JVM**의 major version이 `build.md`의 `JDK major`와 같은지 빌드 도구의 version 명령(Gradle이면 `gradlew --version`)으로 확인한다.

## 기기·에뮬레이터

`build.md`가 기기 절차를 선언한 경우에만 그 절차를 따른다. 선언이 없으면 기기·에뮬레이터 작업을 하지 않으며, 그 작업이 필요하면 `BLOCKED: device procedure undeclared`로 해당 작업만 멈춘다. 기기 확인 결과는 구현·병합·완료 gate가 아니다.

## Process/run scope

- 현재 `java`가 사용 가능하면 기존 shell 환경을 바꾸지 않는다.
- 유효한 `JAVA_HOME` 또는 선언된 후보를 선택했는데 `java`가 PATH에 없으면 현재 shell process에만 `JAVA_HOME`을 설정하고 해당 `bin`을 PATH 앞에 추가한다.
- `setx`, registry 변경, shell profile 수정, 시스템/사용자 영구 환경변수 변경, 빌드 설정 파일 수정을 하지 않는다.
- resolve source, JDK home, `java -version`과 빌드 도구 version 결과를 현재 agent run context에 기록한다. repository 파일이나 영구 host 설정에 cache하지 않는다.
- 후속 빌드 command가 새 shell process에서 실행되면 기록한 동일 값을 그 process의 환경에 다시 주입한다. 후보 탐색과 version 확인은 같은 agent run에서 반복하지 않는다.

## Install / download 금지

JDK·빌드 도구·SDK를 자동 설치하거나 내려받지 않는다. `build.md`가 별도로 허용한 범위가 있으면 그 범위만 따른다. 빌드 도구가 의존성을 내려받는 것은 프로젝트의 정상 빌드 동작이며 이 금지에 포함하지 않는다. 다만 그 접근이 막혀 실패하면 환경 failure로 분리한다.

## Stop condition

- JDK를 resolve할 수 없으면 `BLOCKED: JDK unavailable`로 빌드 명령을 실행하지 않는다.
- required 빌드 검증에서 선언 버전 JDK를 확인할 수 없으면 `BLOCKED: canonical build JDK unavailable`로 중단하고 미실행 command를 기록한다.
- 위 상태를 PASS로 기록하지 않는다.

## 조건부 진단 모드

정확한 트리거 키워드는 `[BUILD-PREFLIGHT-DIAG]`다.

- 현재 작업 지시 또는 해당 run의 명시적 실행 입력에 이 키워드가 있을 때만 활성화한다.
- 키워드가 없으면 진단 기록을 만들지 않고, 진단을 위한 추가 repository-wide 탐색이나 반복 command도 실행하지 않는다.
- 활성화되면 같은 agent run의 preflight 실행 경로를 Issue 기록 **1개**로 통합한다. 같은 run에 이미 기록한 진단이 있으면 중복 기록을 만들지 않는다.

기록하는 decision metadata는 현재 shell 종류, JDK resolve source와 `java -version` 성공/실패, 빌드 도구 JVM major 확인 결과, fallback 발생 여부와 원인 category, install/download 시도 여부로 한정한다. 실제 사용자명, 전체 환경변수 값, 전체 PATH, API key/token은 기록하지 않는다. host 경로가 필요하면 사용자 식별 구간을 `<user>` 같은 placeholder로 정규화한다.

## Output

- 적용 대상 판정
- JDK resolve source: current `java` / `JAVA_HOME` / 선언된 후보
- resolved JDK home 또는 executable, `java -version` 결과
- 빌드 도구 JVM major와 `build.md` 선언의 일치 여부
- 같은 run의 후속 command에서 reuse 여부
- install/download 시도 여부
- 실패 시 `BLOCKED: JDK unavailable` / `BLOCKED: canonical build JDK unavailable` / `BLOCKED: device procedure undeclared`, 확인한 후보 범주, 미실행 command
