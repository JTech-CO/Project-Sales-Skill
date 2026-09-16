# Project Sales | 빠른 시작

## 설치 없이 사용

[LITE-KR.md](LITE-KR.md)의 본문을 텍스트 지침을 받는 에이전트에 붙여넣고 작업을 덧붙인다. 영어 문서는 [LITE.md](LITE.md)이다.

```text
Project Sales 기준으로 첨부한 제품 소개와 기업 명단을 검토합니다.
후보별 적합·제외 근거와 첫 메일 초안 1개를 작성합니다.
확인되지 않은 연락처 검증과 연락 허용 근거는 미확인으로 남깁니다.
실제 발송이나 원격 저장은 하지 않습니다.
```

LITE는 도구나 권한을 설치하지 않는다. 파일 하나를 붙여넣는 경로에는 Python이나 Node가 필요하지 않다.

## SKILL 설치

ZIP을 풀고 `project-sales` 폴더에서 다음을 실행한다. `my-project`는 이 패키지 밖에 있는 실제 작업 프로젝트 이름으로 바꾼다.

```sh
python scripts/install.py --dest ../my-project/.agents/skills --dry-run
python scripts/install.py --dest ../my-project/.agents/skills
```

Claude Code용으로는 경로를 `../my-project/.claude/skills`로 바꾼다. 해당 작업 프로젝트를 호스트에서 열고 스킬 목록에 `project-sales`가 표시되는지 확인한다. 파일 복사 성공과 호스트 활성화는 별개다. [호스트 문서 출처](SOURCES.md)를 참고한다.

네이티브 ZIP 로더가 있는 환경에서는 [기본 스킬 ZIP](dist/project-sales-core.zip)을 활용한다. 일반 파일 첨부를 스킬 설치로 오해하지 않는다.

## 앱 연결 예제 확인

```sh
node adapters/app/example.mjs
```

한국어 LITE와 회신 분류 자료만 읽고 허구 메시지 2개를 가져온다. 출력의 `modelCalled`, `externalNetworkUsed`, `remoteChangesMade`는 모두 false여야 한다. 실서비스의 읽기 도구는 [앱 연결부](adapters/app/README.md)에 호스트 함수와 승인 콜백으로 연결한다.

## 특정 기능만 설치

```sh
python scripts/install.py --dest ../reply-agent/.agents/skills --select triage
```

여섯 기능 모두를 매번 넣을 필요는 없다. 기본 스킬과 전체 선택 스킬을 중복 설치하지 않는 구성을 권장한다.

## 범위

0.1.0은 초안·제안서 전용이며 발송기나 스케줄러가 없다. 실데이터 파일은 비공개 위치에서 다루고 Git에 올리지 않는다. 자체 앱 인증·메일 서비스·CRM·캘린더의 실제 연결은 별도 호스트 작업이다.
