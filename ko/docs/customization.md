# 설치와 커스터마이징 안내 (1.0 preview.4)

이 안내는 M·W·P 설치 경로 보정이 포함된 `v1.0.0-preview.4`를 다룬다. 태그의 전체 commit SHA를 확인하고 사본과 안내를 그 commit으로 고정한다. 공개된 preview.3은 [태그의 안내](https://github.com/seok-jun/adaptive-agentic-sdd/blob/v1.0.0-preview.3/ko/docs/customization.md)를 따른다. 공개된 `v1.0.0-preview.2`를 설치하려면 [해당 태그의 한국어 설치 안내](https://github.com/seok-jun/adaptive-agentic-sdd/blob/v1.0.0-preview.2/ko/docs/customization.md) 또는 [영문 안내](https://github.com/seok-jun/adaptive-agentic-sdd/blob/v1.0.0-preview.2/docs/customization.md)를 사용한다. 그 태그는 여기서 설명하는 `--harness-root`와 새 운영 설정을 지원하지 않는다.

생성된 기본 check/check-evals 명령은 Windows에서는 PowerShell, 그 외에서는 POSIX sh의 경로 리터럴 인용을 사용한다. 표시된 셸에서 실행한다. 사용자 지정 명령의 인용은 프로젝트가 관리한다.

이 문서는 방법론 사본을 프로젝트에 두고, 프로젝트 값으로 프로젝트 종속 파일을 생성하고, Agent에게 일을 시키는 방법을 설명한다. 사본에는 넣지 않는다.

## 이 preview는 무엇인가

- **공통 원칙(M)**: `methodology/`의 `core.md`(최소 작업 흐름, 사람 판단 요건, 작업 기록과 관측), `adaptation.md`(관측에 따른 지원 선택), `supports/ordered-changes.md`(기본 지원).
- **실행 절차(W)**: `workflow/`의 절차 문서와 Skill 4개(작업 정리, 작업 격리, 설계와 구현, 검증과 종료), eval 체계와 가상 대표 사례. 한 제품에서 오래 운영하며 다듬은 절차를 제품 종속 부분만 덜어내 옮겼다.
- **설치 도구**: `tools/install.py`(Python 표준 라이브러리만). 프로젝트 값으로 프로젝트 종속 파일을 생성하고, 고정 사본과 생성물이 맞는지 확인한다.
- **효과는 검증되지 않았다.** 절차는 한 제품에서 운영됐지만, 다른 프로젝트로 옮긴 형태는 이번이 첫 preview다.

## 무엇을 어디에 두나

| 무엇 | 위치 | 누가 고치나 |
| --- | --- | --- |
| 고정 사본 | `.adaptive-sdd/methodology/`, `workflow/`, `templates/`, `tools/`, `LICENSE`, `MANIFEST.json` | 아무도 고치지 않는다. 버전을 올릴 때 통째로 바꾼다 |
| 프로젝트 값 | `.adaptive-sdd/project.json` | 사람(Agent는 초안을 제안) |
| P 적용 문서 | `.adaptive-sdd/project/*.md` | 생성물. 직접 고치지 않는다 |
| 도구별 Skill 입구 | `.claude/skills/<이름>/SKILL.md`, `.agents/skills/<이름>/SKILL.md` | 생성물 |
| 표시 구간 | `AGENTS.md`, `CLAUDE.md`, `.gitattributes`의 `adaptive-sdd:begin`~`end` | 생성물. 구간 밖의 기존 내용은 그대로 둔다 |
| 생성 기록 | `.adaptive-sdd/install.lock.json` | 설치 도구 |
| 작업 기록(로컬 문서 방식) | `project.json`의 `tracker.root` (저장소 밖 공유 폴더) | 작업하는 Agent |

**원칙**: 고정 사본과 생성물은 고치지 않는다. 바꿀 것이 있으면 `project.json`을 고치고 다시 생성한다. 고정 사본을 고쳐야만 풀리는 문제는 공통에 빠진 자리이므로 알린다(마지막 절).

## 1. 사본 받기

기본은 저장소 안 설치다. 외부 설치를 선택하면 아래 파일 복사의 목적지를 제품 checkout 밖의 전용 설치 경로 아래 `.adaptive-sdd/`로 바꾸고 다음 절의 명시적 root 옵션을 사용한다. OS junction·하드링크는 필요하지 않다.

`git ls-remote https://github.com/seok-jun/adaptive-agentic-sdd "refs/tags/v1.0.0-preview.4^{}"`로 이 릴리스의 전체 commit SHA를 확인해 고정한다. 이후 `v1-preview` 브랜치가 이동해도 확인한 SHA를 유지한다. 그 commit의 소스 압축 파일을 받아 `ko/adaptive-sdd/`를 프로젝트의 `.adaptive-sdd/`로 **바이트 그대로** 복사한다. 텍스트 편집 도구나 Agent의 파일 쓰기 도구로 다시 쓰지 않는다. Windows PowerShell 예:

```powershell
$sourceCommit = "<v1.0.0-preview.4에서 확인한 전체 commit SHA>"
if ($sourceCommit -notmatch '^[0-9a-f]{40}$') { throw "sourceCommit에 검토한 전체 commit SHA를 입력하세요." }
$zip = Join-Path $env:TEMP "adaptive-sdd-$sourceCommit.zip"
Invoke-WebRequest "https://github.com/seok-jun/adaptive-agentic-sdd/archive/$sourceCommit.zip" -OutFile $zip
$tmp = Join-Path $env:TEMP "adaptive-sdd-preview"
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Expand-Archive $zip -DestinationPath $tmp
$src = (Get-ChildItem $tmp -Directory | Select-Object -First 1).FullName
foreach ($p in "methodology","workflow","templates","tools","LICENSE","MANIFEST.json") { Remove-Item ".adaptive-sdd/$p" -Recurse -Force -ErrorAction SilentlyContinue }
New-Item -ItemType Directory -Force .adaptive-sdd | Out-Null
Copy-Item "$src/ko/adaptive-sdd/*" .adaptive-sdd -Recurse -Force
Remove-Item $tmp -Recurse -Force; Remove-Item $zip -Force
```

같은 압축 파일의 `ko/docs/customization.md` 또는 3절의 commit 고정 주소를 사용한다. 아래 `<확인한 SHA>`에는 압축 파일을 받을 때 선택한 SHA를 그대로 넣는다. 미출시 commit에는 `--source-tag`를 지정하지 않는다. 공개 태그를 사용할 때만 그 태그와 commit의 대응을 확인해 함께 기록한다.

## 2. 프로젝트 값 만들기

### 외부 설치와 연결

M·W·P는 각각 공통 원칙·실행 절차·제품 사실과 설정의 소유 구분이다. 외부 설치 경로는 저장 위치 옵션이며 S라는 별도 계층이나 실행 입력을 추가하지 않는다. 제품 checkout과 서로 포함하지 않는 전용 폴더를 선택하고 그 아래 `.adaptive-sdd/`에 사본을 둔다. 다음 명령은 경로 예시이며 실제 허용된 위치로 바꾼다. Windows JSON 경로에는 `/`를 쓰면 역슬래시 이스케이프 혼동을 줄일 수 있다.

```text
python -I -B <외부 설치 경로>/.adaptive-sdd/tools/install.py init --project-root <제품 checkout> --harness-root <외부 설치 경로>
python -I -B <외부 설치 경로>/.adaptive-sdd/tools/install.py render --project-root <제품 checkout> --harness-root <외부 설치 경로> --source-tag v1.0.0-preview.4 --source-commit <확인한 SHA>
python -I -B <외부 설치 경로>/.adaptive-sdd/tools/install.py check --project-root <제품 checkout> --harness-root <외부 설치 경로>
```

P 소유 설정·적용 문서·lock은 외부 설치 경로에, `.agentics/adaptive-sdd.json`·도구별 Skill 입구·AGENTS/CLAUDE 표시 구간은 P에 생성한다. 외부 설치 경로에는 중복 Skill 입구를 만들지 않는다. 연결의 manifest hash, 외부 설치 경로의 lock source, 사본 byte, 제품·설치 경로의 생성물을 함께 검사한다. 연결이 없거나 접근/고정 정보가 틀리면 다른 사본으로 fallback하지 않는다. 사본 업그레이드 후에는 검토한 외부 설치 경로를 `--harness-root`로 명시해 render하고 연결을 갱신한다. 도구가 원격 source commit의 진위를 검증하는 것은 아니다.

한 외부 설치 경로의 lock은 한 P checkout에만 묶인다. 새 worktree/다른 checkout은 전용 설치 경로와 연결을 만들고 같은 tracker_root를 공유할 수 있다. 이미 연결된 설치 경로를 다른 P로 몰래 재지정하지 않는다. 여러 checkout에 하나의 생성물 lock을 공유하는 모드는 지원하지 않는다. 클라우드 host가 외부 설치 경로를 읽을 수 없으면 in-repo 설치를 사용하거나 접근 가능한 배치를 별도로 정해야 한다.

기존 설치를 옮길 때는 새 설치 경로에 고정 사본과 검토한 project.json을 복사하고 위 명령으로 연결한다. P에 남은 손편집 입구는 KEPT로 보존되므로 diff 검토 후 해당 경로에만 `--accept-overwrite`를 사용한다. 옛 사본·입구·연결은 도구가 자동 삭제하지 않는다. 검증 후 소유·사용 여부를 확인해 별도로 정리한다. 로컬 전용이면 생성 경로의 commit/exclude 여부를 P에서 정하며 설치가 push 권한을 부여하지 않는다. 외부 설치 경로를 Git으로 관리할 때에도 사본은 LF byte를 유지한다.

### 프로젝트별 운영 설정

기존 schema 1 값은 계속 읽으며 생략된 Git 값은 origin/main/main, ID는 generated, 테스트 수명은 persistent다.

| 값 | 의미 |
| --- | --- |
| `git.remote`, `git.base_branch`, `git.merge_branch` | 코드 원격, 새 lane 기준, 제품 병합 대상. 실제 Git 권한과 별개 |
| `review.repository`, `review.remote`, `review.branch` | SDD 게시 저장소 절대 경로·원격·branch. 빈 값은 각각 P·git.remote·Issue branch. 로컬 bare 원격도 exact artifact 조회가 가능해야 함 |
| `tracker.id_source`, `id_format`, `child_id_rule` | generated 또는 external. external은 형식 필수이며 원천 ID를 유지. 하위 접미 규칙과 발급 권한은 사람이 선언 |
| `project.conversation_language`, `project.conventions` | 대화/진행 보고 언어, 프로젝트 컨벤션 원본 참조 |
| `build.checks` | `scope, method, actor, instructions, evidence, required` 문자열을 가진 목록. method는 command/manual, actor는 agent/human, required는 required/optional |
| `build.test_mode`, `test_format`, `test_preserve_at` | persistent/temporary/none, 테스트 형식, 임시 증거 보존 위치(temporary에 필수). 상대 경로는 P 기준 |
| `routing.role_defaults` | `role, model, reasoning` 목록. role은 PLAN/IMPLEMENT/REVIEW/TEST_DOCS/FINISH. 선호이며 qualification이나 B의 사람 선택을 대체하지 않음 |
| `routing.capabilities` | `host, model, tier, reasoning, source, identity, valid_until` 목록. tier는 cheap/strong/frontier, 기한은 timezone 포함 ISO 시각. 선택 시 실제 원천·freshness·host 지원을 확인 |
| `routing.qualification_records` | 별도 role qualification 기록 참조. capability와 구분 |

`build.verification`의 기존 명령과 `build.checks`는 함께 적용된다. 수동 결과는 대상·확인자·시점·관찰 증거를 확보해야 하며 필수 미확인은 완료가 아니다. temporary는 테스트/fixture·실행 근거를 보존·재조회한 뒤 제거하며 최종 코드와 입력 대응을 증명한다. none도 완료 기준과 PLAN finding을 증명할 동등 근거가 없으면 차단한다. 새 설정은 과거 지시를 묵시적으로 덮지 않으며 진행 중 적용은 기존 정책 전환 절차를 따른다.

### 저장소 안 기본 설치

```bash
python -I -B .adaptive-sdd/tools/install.py init --project-root .
```

`.adaptive-sdd/project.json`이 없을 때만 예제를 복사한다. 이미 있으면 건드리지 않는다. 값은 아래 3절의 순서로 Agent가 초안을 만들고 사람이 정한다.

| 값 | 내용 | 정하는 사람 |
| --- | --- | --- |
| `project.name`, `project.artifact_language` | 이름, 사람이 읽는 산출물의 언어 | 사람 |
| `tools` | `claude-code`, `codex` 중 쓰는 것 | 사람 |
| `tracker` | `kind`(`local-docs` 또는 `github`), 로컬 문서면 `root`(저장소 밖 절대 경로, 로컬 디스크나 SMB 공유 — 동기화 폴더 금지)·`id_prefix`·`merge_method`(`merge`·`squash`·`rebase`), 허용 작성자 | 사람 |
| `docs` | business·SDD·결정 기록·구조 문서·목차 위치 | Agent 제안, 사람 확인 |
| `grade_mapping` | 프로젝트별 자동 격상(예: 특정 공유 모듈 변경 → Medium) | Agent 제안, 사람 확인 |
| `human_judgment` | Large 실행 변경의 사람 병합, 추가 판단 지점, 기록된 위임(범위·날짜·확인자). `large_epic_merge` 키는 호환을 위해 유지하며 기존 사람 권한을 자동 면제하지 않음 | **사람만** |
| `worktree_root` | 병렬 lane worktree를 둘 짧은 절대 경로 | 사람 |
| `build` | 빌드 도구, JDK major, 실행 wrapper, 정리 명령, 변경 범위별 검증 명령 | Agent 제안, 사람 확인 |
| `modules` | 모듈 목록, 공유 contract, root·integration 전용 경로, 의존성 규칙 | Agent 제안, 사람 확인 |
| `routing.deny_models` | 쓰지 않을 모델 | 사람 |
| `priority` | 현재 단계, 구현 queue 규칙, 제품별 Priority 사례 | 사람 |
| `evidence` | 그대로 적어도 되는 근거와 옮기면 안 되는 것 | 사람 |
| `visual_spec` | HTML Visual Spec 저장소(없으면 비워 둔다) | 사람 |
| `token_diagnostic` | `ENABLED` 또는 `DISABLED` | 사람 |
| `hard_guard_extra` | 프로젝트 고유의 항상 적용 규칙 | 사람 |
| `skill_eval.cases_dir` | 사건에서 만든 eval 사례를 둘 위치 | 사람 |

목록 값 중 다음은 항목마다 정해진 키만 쓴다. 키가 다르거나 값이 비면 `render`가 거부한다. 나머지 목록은 문자열 목록이다.

| 값 | 항목 형식 |
| --- | --- |
| `grade_mapping` | `{"change": "변경 조건", "min_grade": "Medium"}`. min_grade는 Trivial·Small·Medium·Large만 허용. Epic은 선택적 관리 단위 |
| `human_judgment.delegations` | `{"scope": "위임 범위", "date": "YYYY-MM-DD", "confirmed_by": "기록한 사람"}` |
| `build.verification` | `{"scope": "변경 범위", "commands": "실행할 명령"}` |
| `modules.list` | `{"path": "모듈 경로", "role": "역할"}` |
| `priority.product_examples` | `{"input": "작업 유형", "examples": "Priority 사례"}` |

빈 값은 생성물에 "미정"으로 드러난다. 미정인 채로도 생성되지만, 그 값에 기대는 절차(예: 로컬 문서 방식에서 `tracker.root`나 `merge_method` 없이 작업 항목 만들기·병합 확인)는 멈춘다.

로컬 문서 방식의 Git·SDD 게시 원격은 위 선언을 따른다. 원격이 없으면 W `tracker/local-docs.md`의 `코드 원격`을 따른다.

## 3. Agent에게 시키는 순서

이 안내는 사본에 없으므로 Agent에게 주소를 함께 준다: `https://raw.githubusercontent.com/seok-jun/adaptive-agentic-sdd/<commit-sha>/ko/docs/customization.md`. `<commit-sha>`를 압축 파일에 사용한 SHA로 바꾸고 아래 `<주소>`에도 그 주소를 넣는다. 웹에 접근하지 못하는 Agent에게는 같은 압축 파일의 안내를 붙여 주거나 저장소 밖 임시 위치에 두고 경로를 준다.

**① 관찰.** 코드를 고치지 않고 사실만 모은다.

```text
.adaptive-sdd/methodology/core.md와 .adaptive-sdd/workflow/README.md를 읽어줘. 제품 코드는 수정하지 마.
이 저장소의 빌드·테스트 명령, CI, 모듈 구조와 의존 방향, 작업 관리 방식, 기존 규칙 파일(AGENTS.md, CLAUDE.md),
위험한 공유 경로를 실제로 확인해서 사실로 정리해줘. 확인하지 못한 것은 따로 적어줘.
```

**② project.json 초안.**

```text
설치 안내(<주소>)의 project.json 값 표를 기준으로 .adaptive-sdd/project.json 초안을 보여줘.
값마다 근거(파일·명령)와 확인하지 못한 것을 나누고, "사람만" 또는 "사람"이 정하는 값은 비워 둔 채 질문으로 모아줘.
아직 파일에 쓰지는 마.
```

**③ 사람 몫 결정.** 사람이 답한다. 사람 판단 지점, 위임, 쓰기 범위, 작업 관리 위치, worktree root, 병합 방법, 금지 모델은 Agent가 대신 정하지 않는다(`core.md` `사람 판단` 3). 위임은 사람이 범위·날짜를 직접 말하고, Agent는 그 말을 그대로 옮기며 `confirmed_by`에 그 사람을 적는다. Agent가 위임을 제안하거나 넓혀 적지 않는다.

**④ 쓰고 생성하기.**

```text
방금 정한 대로 .adaptive-sdd/project.json을 쓰고, 아래 명령으로 생성해줘. 고정 사본은 수정하지 마.
python -I -B .adaptive-sdd/tools/install.py render --project-root . --source-tag v1.0.0-preview.4 --source-commit <확인한 SHA>
python -I -B .adaptive-sdd/tools/install.py check --project-root .
로컬 문서 방식이면 tracker.root 아래에 items/와 claims/ 폴더를 만들어줘.
생성된 AGENTS.md·CLAUDE.md·.gitattributes 구간과 .adaptive-sdd/project/ 문서를 보여줘.
```

`render`는 고정 사본이 `MANIFEST.json`과 다르면 생성을 거부한다. 이미 생성된 파일을 누가 손으로 고쳤거나, 설치 전부터 같은 경로에 사람의 파일이 있으면 덮어쓰지 않고 `KEPT`로 알린다(다음 `render`에서도 그대로 둔다). 그 파일을 바꿀지는 사람이 정한다(`--accept-overwrite <경로>`).

**저장소 밖 쓰기 허용.** `tracker.root`와 `worktree_root`는 저장소 밖이다. Agent 도구의 기본 작업 범위가 저장소 안뿐이면 그 쓰기가 막히거나 매번 확인을 묻는다. 두 폴더를 도구의 추가 작업 폴더로 허용한다. 예: Claude Code는 실행 시 `--add-dir <경로>` 또는 설정의 `permissions.additionalDirectories`, Codex CLI는 `--add-dir <경로>` 또는 `config.toml`의 `[sandbox_workspace_write]` `writable_roots`. 옵션 이름은 도구 버전마다 다를 수 있으니 쓰는 버전의 문서로 확인한다. 허용은 사람이 한다.

**commit과 push.** 저장소 안 설치는 생성물과 고정 사본을 검토한 뒤 P가 선언한 코드 원격·기준 브랜치에 반영한다. 새 lane에서 같은 사본을 조회할 수 있어야 한다. 병합·push 주체와 방법은 P 권한을 따르며 공유 기준 브랜치 직접 push를 강제하지 않는다. 외부 설치는 checkout별 외부 설치 경로와 연결을 준비하고 check한다. 로컬 절대 경로를 담은 연결의 공유 여부와 설치 파일의 commit/exclude 정책은 P에서 정한다.

**⑤ 작은 작업으로 시운전.**

```text
[작은 작업]을 작업 항목으로 만들고(managing-issues), lane을 잡고(parallel-development), 구현하고(implementing-issues),
종료해줘(finishing-issues). 끝나면 작업 문서의 메타·기록 항목과 claim 파일이 W tracker 대응표대로 남았는지 보여줘.
```

**⑥ 실작업 뒤 개선.** 작업을 마칠 때마다 시킨다.

```text
이번 작업의 종료 요약과 사건 기록을 M adaptation.md의 "관측을 다음 판단에 사용하기"로 검토해줘.
근거가 있는 것만 처분을 제안하고, project.json으로 풀 수 있는 것과 고정 사본을 고쳐야 하는 것을 나눠줘.
사건으로 eval 사례를 만들 가치가 있으면 W process/skill-evals.md의 "사건을 사례로 만들기" 규칙으로 초안만 보여줘.
```

사례를 실제로 돌려 보조를 비교하는 일은 모델 호출과 비용이 든다. W `skill-evals.md`의 "비교와 채택" 조건대로 사람이 범위·횟수·모델·예산을 정한 뒤에만 한다.

## 4. 확인과 검사

```bash
python -I -B .adaptive-sdd/tools/install.py check --project-root .
python -I -B .adaptive-sdd/tools/install.py check-evals --project-root .
```

`check`는 아무것도 바꾸지 않는다. 고정 사본·lock·생성물을 다시 계산해 비교하고, 다르면 무엇이 다른지만 알린다. 고정 사본에 manifest에 없는 파일이 있거나(`EXTRA`), 더 이상 생성하지 않는 파일이 남아 있으면(`STALE`, 예: `tools`에서 codex를 뺀 뒤의 `.agents/skills`) 함께 알린다. 도구별 Skill 입구도 같은 run에서 한 번 이 검사를 실행하게 되어 있다.

Python을 쓸 수 없으면 고정 사본만 `MANIFEST.json`의 해시와 PowerShell로 대조할 수 있다(생성물은 확인하지 못한다). 이 경우 Skill 입구는 `BLOCKED`로 멈추므로, 사람이 확인한 뒤 진행 여부를 정한다:

```powershell
$m = Get-Content .adaptive-sdd/MANIFEST.json -Raw -Encoding UTF8 | ConvertFrom-Json
$m.files.PSObject.Properties | ForEach-Object { $h = (Get-FileHash ".adaptive-sdd/$($_.Name)" -Algorithm SHA256).Hash; if ($h -eq $_.Value) { "OK   $($_.Name)" } else { "DIFF $($_.Name)" } }
```

## 버전 올리기

1. 1절로 새로 검토한 commit의 사본과 같은 버전의 안내를 받는다. 공개 릴리스라면 태그의 commit을 확인하고 그 태그의 안내를 따른다. 고정 사본 폴더는 먼저 지우고 통째로 바꾼다. `project.json`, `project/`, `install.lock.json`은 그대로 둔다.
2. `render`를 새 commit으로 다시 실행하고 `check`로 확인한다. 태그는 아래 조건에 맞을 때만 함께 지정한다. 생성물이 어떻게 바뀌었는지 사람이 diff로 본다.
3. 진행 중인 작업 도중에는 묵시적으로 바꾸지 않는다. 바꾸면 그 시점부터의 구간으로 기록한다(`core.md`). 활성 담당·실행 중 리뷰·미커밋 변경·최근 작업 기록을 확인하고 적용할 Issue·시점을 조율한다. 프로젝트 정책 변경도 W [계획 정정과 정책 전환](../adaptive-sdd/workflow/process/sdd/plan-change.md#계획-정정과-정책-전환)을 따른다. 유효한 기존 결정을 다시 승인받거나 전체 리뷰를 자동 반복하지 않고 실제 무효화된 근거만 갱신한다.

태그 없는 revision으로 올릴 때는 `render --project-root . --source-commit <확인한 SHA>`를 사용하고 브랜치 이름을 `--source-tag`로 넘기지 않는다. commit이 이전 값과 달라지고 새 태그를 명시하지 않으면 이전 `source.tag`를 제거한다. 같은 commit의 재생성이나 source 옵션 없는 재생성은 기존 값을 보존한다. 이미 잘못 남은 태그는 `--clear-source-tag`로 제거할 수 있다. 새 태그는 반드시 `--source-tag <실제 태그> --source-commit <확인한 SHA>`를 함께 지정한다. 설치 도구는 원격 태그의 대응을 조회하지 않으므로 그 대응 확인은 호출자의 책임이며 `check` 성공이 태그 출처 검증을 뜻하지 않는다.

이번 요구사항·결정 기록 규칙을 적용할 때는 생성 `project/issue-writing-guide.md`와 프로젝트가 직접 둔 금지 규칙의 차이를 확인한다. 작업 요구의 최소 기록과 대화 로그 수집을 구별하되 프로젝트의 정보 공개·비밀정보 보호 제한을 자동으로 완화하지 않는다. 손으로 고친 생성물이 `KEPT`이면 diff를 검토하고 허용된 범위에서만 갱신한다.

### Epic 실행 등급에서 관리 단위로 전환

preview.3의 W 정책은 실행 grade를 Trivial·Small·Medium·Large로 한정한다. Epic 관리·공통 변경 검증·전환의 원본은 W [Epic 관리 단위](../adaptive-sdd/workflow/process/sdd/epic.md#epic-관리-단위)와 [기존 Epic 전환](../adaptive-sdd/workflow/process/sdd/epic.md#기존-epic-전환)이며, 조사 착수와 분석 재사용은 [착수 조건](../adaptive-sdd/workflow/process/sdd/entry.md)과 [기존 분석 재사용](../adaptive-sdd/workflow/process/sdd/entry.md#기존-분석-재사용)을 따른다.

- `grade_mapping`에 `min_grade: Epic`이 있으면 실제 전체 변경의 위험으로 실행 등급을 다시 정해 사람이 프로젝트 값을 갱신한다. 설치 도구는 자동으로 Large로 치환하지 않고 render 전에 오류를 낸다.
- 기존 `grade:Epic` Issue는 관리 문서(`작업 유형: Epic`, `type:epic`, grade 없음)로 유지하거나 실제 범위에 따라 하나의 실행 Issue로 전환한다. local-docs의 관리 메타는 `type: epic`을 쓴다.
- 기존 목표·사람 결정·병합 권한과 유효한 분석·검증은 보존한다. 전환만을 이유로 활성 lane을 초기화하거나 분석·리뷰를 반복하지 않는다. `human_judgment.large_epic_merge` 키는 호환을 위해 유지한다.

## 공통 문제를 알릴 때

`project.json`으로 풀 수 없고 고정 사본을 고쳐야만 풀리는 문제는 공개 저장소(`seok-jun/adaptive-agentic-sdd`)의 이슈로 알린다. 그 전에 회사나 프로젝트의 정보 공개 정책을 확인한다. 회사·제품 이름, 코드, 데이터, 내부 경로는 빼고, 일반화한 문제와 필요한 변경만 적는다.
