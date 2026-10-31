# macOS 첫 사용 점검 — 핸즈오프 (2026-10-31)

지금까지 모든 검증은 Windows 한 대에서만 했다. 이 점검은 macOS 노트북에서 두 가지를 확인한다.

1. 저장소 테스트가 macOS(POSIX)에서 통과하는가.
2. 처음 쓰는 사람처럼 Agent가 README만 보고 **설치 → 첫 Small 작업 → 설치 되돌리기**를 끝낼 수 있는가.

Windows에서 같은 방식으로 한 점검 기록: [first-use record](../../eval-results/2026-10-31-first-use/README.md).

## 대상 버전

PR #6 브랜치(`eval/harness-v2`)의 `1d91d9448621c29e39c248bf1c1f23a098ecb02d`. c′ 정책(Trivial/Small은 금지 모델이 아니면 현재 모델로 진행)이 들어 있는 최신 후보다. 공개된 `v1.0.0-preview.6`에는 첫 작업 차단 규칙이 남아 있어서, 그걸로 하면 이미 아는 문제에서 멈춘다. 브랜치가 그 뒤로 바뀌었으면 `setup.sh`의 두 번째 인자로 새 SHA를 넘긴다.

## 0. 준비 확인

```bash
python3 --version; git --version; claude --version
```

Python 3.8 이상, Git 2.38 이상(`git merge-tree --write-tree` 사용). Codex로도 할 거면 `codex --version`.

## 1. 저장소 테스트

```bash
git clone https://github.com/seok-jun/adaptive-agentic-sdd.git ~/aasdd-src
```

```bash
cd ~/aasdd-src && git checkout 1d91d9448621c29e39c248bf1c1f23a098ecb02d && python3 -I -B -m unittest discover -s tests 2>&1 | tail -15
```

Windows에서는 88개가 통과했다. 마지막 15줄을 그대로 남긴다.

## 2. 일회용 샘플 저장소 만들기

이 폴더의 `setup.sh`가 `~/adaptive-sdd-mac-test` 아래에 샘플 저장소(일부러 심은 페이지 계산 버그 포함), 로컬 bare `origin`, `tracker/`, `wt/`, 그리고 Agent에게 줄 `prompt.md`를 만든다. 다시 실행하면 그 폴더를 지우고 새로 만든다.

```bash
bash ~/aasdd-src/docs/handoff/macos-first-use/setup.sh
```

위치나 SHA를 바꾸려면 `bash setup.sh <폴더> <SHA>`. 폴더는 `$HOME` 아래여야 한다.

## 3. Agent 실행

```bash
cd ~/adaptive-sdd-mac-test/sample && claude --add-dir ~/adaptive-sdd-mac-test
```

열리면 `~/adaptive-sdd-mac-test/prompt.md` 내용을 통째로 붙여 넣는다.

- 권한 요청은 허용하되, **어떤 명령에서 물어봤는지 메모**한다. 첫 경험 자료다.
- macOS에서 예상되는 문제는 Agent에게 **미리 알려 주지 않는다.** 그대로 겪는지를 봐야 한다.
- Codex로도 할 거면 같은 `prompt.md`로 한 번 더 한다. Codex `workspace-write` 샌드박스는 `.agents/`와 `.git`을 읽기 전용으로 둔다. `--add-dir ~/adaptive-sdd-mac-test/sample/.agents`가 필요하고, Git 쓰기는 막힐 수 있다. 막히면 그 사실 자체를 기록한다.

## 4. 끝나면 남길 것

1. `~/adaptive-sdd-mac-test/report.md` 내용
2. 아래 출력

```bash
cd ~/adaptive-sdd-mac-test/sample && git log --oneline -8 && git ls-remote origin && git status --short --ignored && grep -n "end =" catalog/search.py && python3 -m unittest discover -s tests -t . 2>&1 | tail -1 && ls ../tracker/items ../tracker/claims
```

3. 1단계 테스트 결과(마지막 15줄)
4. 권한 요청 메모, 그리고 Agent가 `python`/`python3` 때문에 막히거나 우회했는지

## 미리 알고 있는 의심 지점 (Agent에게는 말하지 않음)

| 의심 | 근거 | 확인할 것 |
| --- | --- | --- |
| 생성 파일의 `python` 고정 | `tools/install.py:411`, `:413`이 스킬 입구와 AGENTS 블록에 `python -I -B ... check`를 쓴다. README·안내도 `python`이다 | macOS 기본 환경에 `python`이 없을 때 입구의 첫 점검이 실패해 `BLOCKED: pinned workflow unavailable`로 멈추는지, Agent가 `python3`로 바꿔 쓰는지 |
| 전체 설치 안내가 PowerShell 전용 | `docs/customization.md` 1절 복사 스크립트 | Agent가 POSIX 명령으로 무엇을 추측했는지 |
| POSIX에서 테스트를 돌린 적 없음 | CI 없음, Windows 전용 분기 테스트(`tests/test_installer.py:381`) | 1단계 결과 |

## 이 점검이 아닌 것

한 번의 실행은 Mac 사용자가 막힐 수 있는 곳을 보여 줄 뿐, 얼마나 자주 막히는지나 결과·재작업·비용에 대한 효과를 재지 않는다. 결과를 받으면 확인된 마찰만 고친다. 평가 실행기는 고치지 않는다.
