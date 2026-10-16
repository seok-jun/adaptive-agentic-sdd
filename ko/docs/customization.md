# 커스터마이징 안내 (1.0 preview)

이 문서는 방법론 사본을 프로젝트에 두고, 프로젝트에 맞게 조정하고, Agent에게 일을 시키는 방법을 설명한다. 사본에는 넣지 않는다. 영문 `docs/customization.md`의 한국어판이며, 두 판의 뜻이 다르면 영문이 기준이다.

## 이 preview는 무엇인가

- **얇은 공통 계층이다.** `methodology/core.md`는 최소 작업 흐름과 사람 판단 요건, 작업 기록과 관측을 정한다. `methodology/adaptation.md`는 관측에 따라 지원을 고르는 규칙이다. `methodology/supports/ordered-changes.md`는 기본 지원 하나다.
- **v0.2를 대체하지 않는다.** v0.2의 등급, 리뷰 gate, starter, 템플릿은 들어 있지 않다. 그 밖의 작업 방식은 프로젝트가 정한다.
- **효과는 검증되지 않았다.** 구조가 바뀔 수 있다. 정식 1.0 전까지 preview 태그로만 낸다.

## 무엇을 어디에 두나

| 무엇 | 기본 위치(바꿀 수 있음) | 누가 고치나 |
| --- | --- | --- |
| 방법론 사본 | `.adaptive-sdd/methodology/` | 아무도 고치지 않는다. 버전을 올릴 때 통째로 바꾼다 |
| 라이선스 | `.adaptive-sdd/LICENSE` | 고치지 않는다 |
| 어댑터 | `.adaptive-sdd/adapter.md` | 프로젝트. `core.md`는 별도 파일을 요구하지 않으므로 기존 작업 지침 안에 두어도 된다 |
| 진입 파일 | 기존 `AGENTS.md` 또는 `CLAUDE.md` | 프로젝트. 몇 줄만 더한다 |
| 작업 기록 | 어댑터에 정한 곳 | 작업하는 Agent |

기본 위치를 바꾸면 아래의 `.gitattributes` 줄과 진입 파일 문장도 같이 바꾼다.

## 고치는 곳의 원칙

- 공통 사본은 고치지 않는다. 프로젝트에 맞춘 조정은 모두 어댑터에 둔다.
- 버전을 올릴 때는 사본만 통째로 바꾸고 어댑터와 작업 기록은 그대로 둔다. 그래야 공통을 올려도 프로젝트 조정과 부딪히지 않는다.
- 사본을 고쳐야만 풀리는 문제가 생기면 공통에 빠진 자리로 보고 공개 저장소에 알린다(마지막 절).

## 어댑터 자리

`core.md`가 요구하는 자리와 프로젝트가 고르는 자리가 있다. 모르는 자리는 비워 두지 말고 "미정"과 이유를 적는다.

| 자리 | 구분 | 예 |
| --- | --- | --- |
| 작업 식별 방법 | 필수 | 이슈 번호, 없으면 날짜와 작업 이름 |
| 문제 기록 위치 | 필수 | 작업 문서의 사건 절 |
| 종료 요약 위치 | 필수 | 같은 작업 문서의 끝 |
| 최종 종료 판정 | 필수 | 병합 확인, 배포 확인 |
| 허용된 조회·쓰기 수단과 범위 | 필수 | 로컬 저장소와 개발 DB만, 운영 쓰기 금지 |
| 사람 판단 지점 | 필수(`core.md` "사람 판단" 2). 몇 개를 어디에 둘지는 프로젝트가 정한다 | 병합·배포, 설계 승인을 둘지. 고정 지점을 두지 않으면 "고정 지점 없음 — 미해결 판단에서 멈춤"이라고 적는다 |
| 실행할 검사와 금지 범위 | 선택 | 빌드·단위 테스트, 실행하면 안 되는 명령 |
| 리뷰 경로 | 선택 | 독립 리뷰를 언제 몇 번 받는지 |
| 저장소 구성 | 선택 | 코드와 문서를 한 저장소에 두는지 |
| 기기마다 다른 경로 | 선택 | 도구 설치 경로 |

어댑터의 시작 모양:

```markdown
# 방법론 어댑터

## 고정
- 출처: <저장소 주소> 태그 v1.0.0-preview.1
- 태그 commit: <SHA>
- manifest 해시: <manifest.json 파일의 sha256>
- 사본 위치: .adaptive-sdd/methodology/

## 필수 자리
- 작업 식별 방법:
- 문제 기록 위치:
- 종료 요약 위치:
- 최종 종료 판정:
- 허용된 조회·쓰기 수단과 범위:
- 사람 판단 지점:

## 프로젝트 선택 자리
- 실행할 검사와 금지 범위:
- 리뷰 경로:
- 저장소 구성:
- 기기마다 다른 경로:
```

## 1. 사본 받기와 고정 기록

1. 태그의 소스 압축 파일을 받는다: `https://github.com/seok-jun/adaptive-agentic-sdd/archive/refs/tags/v1.0.0-preview.1.zip`. 압축 안에는 최상위 폴더가 하나 있다.
2. 압축의 `ko/methodology/` 내용(`core.md`, `adaptation.md`, `supports/`, `manifest.json`)을 `.adaptive-sdd/methodology/`에, `LICENSE`를 `.adaptive-sdd/LICENSE`에 **바이트 그대로** 복사한다. LICENSE(MIT)는 복사본에 저작권·허가 고지를 남기라고 요구하므로 함께 둔다. 텍스트 편집 도구나 Agent의 파일 쓰기 도구로 다시 쓰지 않는다. BOM이나 CRLF가 들어가 해시가 바뀐다. Windows PowerShell 예:

```powershell
$zip = "v1.0.0-preview.1.zip"
Invoke-WebRequest "https://github.com/seok-jun/adaptive-agentic-sdd/archive/refs/tags/v1.0.0-preview.1.zip" -OutFile $zip
$tmp = Join-Path $env:TEMP "adaptive-sdd-preview"
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Expand-Archive $zip -DestinationPath $tmp
$src = (Get-ChildItem $tmp -Directory | Select-Object -First 1).FullName
New-Item -ItemType Directory -Force .adaptive-sdd | Out-Null
Remove-Item .adaptive-sdd/methodology -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item "$src/ko/methodology" .adaptive-sdd/methodology -Recurse
Copy-Item "$src/LICENSE" .adaptive-sdd/LICENSE
```
3. 태그가 가리키는 commit SHA를 확인한다: `git ls-remote https://github.com/seok-jun/adaptive-agentic-sdd "refs/tags/v1.0.0-preview.1^{}"`. git이 없으면 저장소의 태그 페이지에서 commit을 확인한다.
4. 해시를 대조한다. 세 문서의 sha256이 `manifest.json`의 값과 같아야 한다. **manifest 해시**는 `manifest.json` 파일 자체의 sha256이다.

Windows PowerShell:

```powershell
$d = ".adaptive-sdd/methodology"
$m = Get-Content "$d/manifest.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$m.files.PSObject.Properties | ForEach-Object { $h = (Get-FileHash "$d/$($_.Name)" -Algorithm SHA256).Hash; if ($h -eq $_.Value) { "OK   $($_.Name)" } else { "DIFF $($_.Name)" } }
(Get-FileHash "$d/manifest.json" -Algorithm SHA256).Hash.ToLower()
```

`Get-FileHash`는 대문자 16진수를 출력한다. PowerShell의 `-eq`는 대소문자를 구분하지 않으므로 그대로 비교된다. 마지막 줄이 manifest 해시다.

macOS·Linux에서는 아래 출력의 앞 세 줄을 `manifest.json`의 값과 비교한다. 마지막 줄이 manifest 해시다. Agent에게 계산과 대조를 시켜도 된다.

```bash
cd .adaptive-sdd/methodology && sha256sum core.md adaptation.md supports/ordered-changes.md manifest.json
```

macOS에서는 `sha256sum` 대신 `shasum -a 256`을 쓴다.

5. 어댑터의 "고정" 절에 태그, commit SHA, manifest 해시를 적는다. 태그 이름만으로는 원본을 대신하지 못한다(`core.md` "실제 적용과 개선 관측").

## 2. 프로젝트에 두기

**줄바꿈 고정.** 프로젝트의 `.gitattributes`에 아래 줄을 더한다. 없으면 Windows에서 `core.autocrlf=true`로 새로 checkout할 때마다 사본이 CRLF로 바뀌어 해시가 맞지 않는다.

```text
.adaptive-sdd/methodology/** text eol=lf
```

**진입 파일.** 기존 `AGENTS.md` 또는 `CLAUDE.md`에 아래와 같은 몇 줄을 더한다. 기존 내용은 덮어쓰지 않는다.

```markdown
## 작업 방법론

작업을 시작할 때 `.adaptive-sdd/methodology/core.md`와 그 문서가 가리키는 문서, `.adaptive-sdd/adapter.md`를 읽고 따른다.
`.adaptive-sdd/methodology/`는 고치지 않는다. 프로젝트 조정은 어댑터에만 둔다.
```

## 3. Agent에게 시키는 순서

처음 한 번은 아래 순서로 시킨다. 각 단계의 결과를 보고 다음으로 넘어간다. 이 안내는 사본에 없으므로 Agent가 읽을 수 있게 주소를 함께 준다: https://raw.githubusercontent.com/seok-jun/adaptive-agentic-sdd/v1.0.0-preview.1/ko/docs/customization.md

**① 관찰.** 코드를 고치지 않고 사실만 모은다.

```text
.adaptive-sdd/methodology/core.md를 읽어줘. 제품 코드는 수정하지 마.
이 저장소의 빌드·테스트 명령, CI, 작업 관리 방식, 기존 규칙 파일,
위험한 공유 경로를 실제로 확인해서 사실로 정리해줘. 확인하지 못한 것은 따로 적어줘.
```

**② 어댑터 초안.**

```text
core.md와 커스터마이징 안내(https://raw.githubusercontent.com/seok-jun/adaptive-agentic-sdd/v1.0.0-preview.1/ko/docs/customization.md)의 어댑터 자리마다 제안 값, 근거(파일·명령),
확인하지 못한 것을 나눠서 보여줘. 내가 정해야 할 것은 따로 모아줘.
```

**③ 사람 몫 결정.** 사람이 답한다. 보통 쓰기 범위, 최종 종료 판정, 사람 판단 지점, 실행 금지 범위는 사람이 정한다. Agent가 대신 정하지 않는다(`core.md` "사람 판단" 3).

**④ 어댑터 작성과 연결.**

```text
방금 정한 대로 .adaptive-sdd/adapter.md를 작성하고, 진입 파일과 .gitattributes에
커스터마이징 안내(https://raw.githubusercontent.com/seok-jun/adaptive-agentic-sdd/v1.0.0-preview.1/ko/docs/customization.md)의 줄을 더해줘.
.adaptive-sdd/methodology/는 수정하지 마. 고정 정보 중 해시는 다시 계산해서 확인한 값으로,
commit SHA는 git ls-remote 결과로 적어줘. 기존 진입 파일 내용은 덮어쓰지 마.
```

**⑤ 작은 작업으로 시운전.**

```text
[작은 작업]을 방법론대로 진행해줘. 끝나면 시작 기록과 종료 요약이
어댑터에 정한 위치에 실제로 남았는지 보여줘.
```

**⑥ 실작업 뒤 조정.** 작업을 마칠 때마다 시킨다.

```text
이번 작업 기록을 보고 어댑터에서 바꿀 것이 있는지 판단해줘.
근거가 있는 것만 제안하고, 공통 사본의 문제로 보이는 것은 따로 분리해줘.
```

## 버전 올리기

1. 새 태그의 압축 파일로 1절을 다시 한다. 사본 폴더는 먼저 지우고 통째로 바꾼다. 남은 옛 파일은 해시 대조에 잡히지 않는다.
2. 어댑터의 "고정" 절을 새 값으로 바꾸고, 바꾼 날짜를 적는다. 앞 구간의 기록은 고치지 않는다.
3. 진행 중인 작업 도중에는 묵시적으로 바꾸지 않는다. 바꾸면 그 시점부터의 구간으로 기록한다.

## 공통 문제를 알릴 때

어댑터로 풀 수 없고 사본을 고쳐야만 풀리는 문제는 공개 저장소(`seok-jun/adaptive-agentic-sdd`)의 이슈로 알린다. 그 전에 회사나 프로젝트의 정보 공개 정책을 확인한다. 회사·제품 이름, 코드, 데이터, 내부 경로는 빼고, 일반화한 문제와 필요한 변경만 적는다.
