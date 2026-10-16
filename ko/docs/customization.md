# 설치와 커스터마이징 안내 (1.0 preview.2)

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

태그의 소스 압축 파일을 받아 `ko/adaptive-sdd/`를 프로젝트의 `.adaptive-sdd/`로 **바이트 그대로** 복사한다. 텍스트 편집 도구나 Agent의 파일 쓰기 도구로 다시 쓰지 않는다. Windows PowerShell 예:

```powershell
$zip = Join-Path $env:TEMP "adaptive-sdd-v1.0.0-preview.2.zip"
Invoke-WebRequest "https://github.com/seok-jun/adaptive-agentic-sdd/archive/refs/tags/v1.0.0-preview.2.zip" -OutFile $zip
$tmp = Join-Path $env:TEMP "adaptive-sdd-preview"
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Expand-Archive $zip -DestinationPath $tmp
$src = (Get-ChildItem $tmp -Directory | Select-Object -First 1).FullName
foreach ($p in "methodology","workflow","templates","tools","LICENSE","MANIFEST.json") { Remove-Item ".adaptive-sdd/$p" -Recurse -Force -ErrorAction SilentlyContinue }
New-Item -ItemType Directory -Force .adaptive-sdd | Out-Null
Copy-Item "$src/ko/adaptive-sdd/*" .adaptive-sdd -Recurse -Force
Remove-Item $tmp -Recurse -Force; Remove-Item $zip -Force
```

태그가 가리키는 commit을 확인해 둔다: `git ls-remote https://github.com/seok-jun/adaptive-agentic-sdd "refs/tags/v1.0.0-preview.2^{}"`.

## 2. 프로젝트 값 만들기

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
| `human_judgment` | Large/Epic 병합을 사람이 하는지, 추가 판단 지점, 기록된 위임(범위·날짜·확인자) | **사람만** |
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
| `grade_mapping` | `{"change": "변경 조건", "min_grade": "Medium"}` |
| `human_judgment.delegations` | `{"scope": "위임 범위", "date": "YYYY-MM-DD", "confirmed_by": "기록한 사람"}` |
| `build.verification` | `{"scope": "변경 범위", "commands": "실행할 명령"}` |
| `modules.list` | `{"path": "모듈 경로", "role": "역할"}` |
| `priority.product_examples` | `{"input": "작업 유형", "examples": "Priority 사례"}` |

빈 값은 생성물에 "미정"으로 드러난다. 미정인 채로도 생성되지만, 그 값에 기대는 절차(예: 로컬 문서 방식에서 `tracker.root`나 `merge_method` 없이 작업 항목 만들기·병합 확인)는 멈춘다.

로컬 문서 방식도 git 절차는 그대로라서 코드 원격 `origin`이 필요하다(새 lane은 `origin/main`에서 만든다). 원격이 없으면 W `tracker/local-docs.md`의 `코드 원격`을 따른다.

## 3. Agent에게 시키는 순서

이 안내는 사본에 없으므로 Agent에게 주소를 함께 준다: https://raw.githubusercontent.com/seok-jun/adaptive-agentic-sdd/v1.0.0-preview.2/ko/docs/customization.md (웹에 접근하지 못하는 Agent에게는 이 파일을 붙여 주거나 저장소 밖 임시 위치에 두고 경로를 준다).

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
python -I -B .adaptive-sdd/tools/install.py render --project-root . --source-tag v1.0.0-preview.2 --source-commit <ls-remote로 확인한 SHA>
python -I -B .adaptive-sdd/tools/install.py check --project-root .
로컬 문서 방식이면 tracker.root 아래에 items/와 claims/ 폴더를 만들어줘.
생성된 AGENTS.md·CLAUDE.md·.gitattributes 구간과 .adaptive-sdd/project/ 문서를 보여줘.
```

`render`는 고정 사본이 `MANIFEST.json`과 다르면 생성을 거부한다. 이미 생성된 파일을 누가 손으로 고쳤거나, 설치 전부터 같은 경로에 사람의 파일이 있으면 덮어쓰지 않고 `KEPT`로 알린다(다음 `render`에서도 그대로 둔다). 그 파일을 바꿀지는 사람이 정한다(`--accept-overwrite <경로>`).

**저장소 밖 쓰기 허용.** `tracker.root`와 `worktree_root`는 저장소 밖이다. Agent 도구의 기본 작업 범위가 저장소 안뿐이면 그 쓰기가 막히거나 매번 확인을 묻는다. 두 폴더를 도구의 추가 작업 폴더로 허용한다. 예: Claude Code는 실행 시 `--add-dir <경로>` 또는 설정의 `permissions.additionalDirectories`, Codex CLI는 `--add-dir <경로>` 또는 `config.toml`의 `[sandbox_workspace_write]` `writable_roots`. 옵션 이름은 도구 버전마다 다를 수 있으니 쓰는 버전의 문서로 확인한다. 허용은 사람이 한다.

**commit과 push.** ⑤ 전에 설치 결과를 main에 commit하고 `origin`에 push한다: `.adaptive-sdd/`(고정 사본, `project.json`, `install.lock.json`, `project/`), `.claude/skills/`, `.agents/skills/`, `AGENTS.md`, `CLAUDE.md`, `.gitattributes`. 새 lane은 `origin/main`에서 만들어지므로, push하지 않으면 lane worktree에 사본이 없어 Skill 입구의 `check`가 `BLOCKED: pinned workflow unavailable`로 멈춘다. 공유 main에 직접 push할지는 사람이 정한다.

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

1. 1절로 새 태그의 사본을 받는다. 고정 사본 폴더는 먼저 지우고 통째로 바꾼다. `project.json`, `project/`, `install.lock.json`은 그대로 둔다.
2. `render`를 새 태그와 commit으로 다시 실행하고 `check`로 확인한다. 생성물이 어떻게 바뀌었는지 사람이 diff로 본다.
3. 진행 중인 작업 도중에는 묵시적으로 바꾸지 않는다. 바꾸면 그 시점부터의 구간으로 기록한다(`core.md`).

## 공통 문제를 알릴 때

`project.json`으로 풀 수 없고 고정 사본을 고쳐야만 풀리는 문제는 공개 저장소(`seok-jun/adaptive-agentic-sdd`)의 이슈로 알린다. 그 전에 회사나 프로젝트의 정보 공개 정책을 확인한다. 회사·제품 이름, 코드, 데이터, 내부 경로는 빼고, 일반화한 문제와 필요한 변경만 적는다.
