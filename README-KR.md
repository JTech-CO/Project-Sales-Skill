# Project Sales Skill

**근거를 바탕으로 조사하고, 필요한 메시지를 작성하며, 관심 대화를 명확하게 인계하는 B2B 영업 스킬.**

[English](README.md) · [빠른 시작](QUICKSTART-KR.md) · [LITE 한국어](LITE-KR.md) · [기본 SKILL](SKILL.md) · [소개 페이지](index.html) · [저장소](https://github.com/JTech-CO/Project-Sales-Skill/)

Project Sales는 제품·고객군 분석, 후보 평가, 아웃리치 초안, 회신 분류, 미팅 인계, 성과 검토를 제공하는 공급자 독립형 스킬 패키지이다. 현재 에이전트가 가진 도구와 맥락에 필요한 영업 기능을 더한다.

**0.1.1은 바로 사용할 수 있는 초안 전용 스킬 릴리스이다.** 현재 에이전트의 도구를 활용하며 로컬 설치 도구·CSV 정리 도구·앱의 지침 로더와 읽기 연결 코드를 포함한다. 실제 발송, 원격 초안 저장, CRM 수정, 일정 초대, 상시 스케줄러, 계정 인증, 공개 플러그인은 포함하지 않는다. 저장소에 등록된 [MIT 라이선스](LICENSE)를 적용한다.

## 사용 경로

| 방식 | 파일 | 적용 상황 |
|---|---|---|
| 어디든 붙여넣기 | [LITE-KR.md](LITE-KR.md) / [LITE.md](LITE.md) | 텍스트 지침을 받는 웹·앱·CLI 에이전트 |
| 기본 스킬 설치 | [SKILL.md](SKILL.md)와 관련 폴더 | SKILL.md 형식을 읽는 호스트 |
| 기능별 스킬 설치 | [optional-skills](optional-skills/README.md) | 좁은 역할이나 여러 에이전트에 기능을 분배 |
| 자체 앱 연결 | [연결 안내](adapters/README-KR.md) | 필요한 지침만 로드하고 허가된 읽기 도구를 연결 |

기본은 **project-sales 하나**이다. 기본 SKILL은 작은 라우터이며 관련 자료만 선택해서 읽는다. 선택 스킬 여섯 개는 각각 독립적으로 설치할 수 있다. 일곱 개를 전부 설치해야 하는 구조가 아니며, 고정된 작업 순서나 다중 에이전트 팀을 강제하지 않는다.

## 여섯 기능

| 기능 | 결과 | 혼동하지 않는 것 |
|---|---|---|
| Discovery | 제품 사실·고객군 가설·제외 기준 | 적합성이 실제 구매 의사는 아님 |
| Qualification | 후보별 근거·출처·미확인 사항 | 주소 검증이 연락 허가는 아님 |
| Outreach | 첫 메일·후속 메시지 초안 | 초안 작성이 발송·원격 저장은 아님 |
| Triage | 회신 의도·근거·다음 행동 | 예의상 회신·부재중은 관심 리드가 아님 |
| Handoff | 대화 맥락·약속·담당자·예약 상태 | 링크나 일방적 일정 생성은 예약 완료가 아님 |
| Review | 관측 범위와 비용이 명확한 성과 | 미확인은 0이 아니며 발송량이 성과는 아님 |

LITE는 PS01-PS10 공통 규칙만 담는다. 범위·근거·적합성·도구 부재 처리·초안 기본값·승인·중지·회신·성과·자료와 권한의 분리를 다룬다. 상세 참고자료는 필요한 작업에서만 읽으며 전체 하네스로 매번 주입하지 않는다.

## 바로 사용

가장 간단한 방법은 LITE-KR 본문과 작업 입력을 함께 제공하는 것이다. 네이티브 스킬을 설치하려면 이 저장소 루트에서 다음을 실행한다.

```sh
python scripts/install.py --dest ../my-project/.agents/skills --dry-run
python scripts/install.py --dest ../my-project/.agents/skills
```

설치 대상은 이 패키지 바깥의 실제 작업 프로젝트이다. Claude Code용 경로는 `../my-project/.claude/skills`로 바꾼다. 호스트별 설치 위치와 최신 지원 여부는 [출처](SOURCES.md) 및 [CLI 안내](adapters/cli/README.md)에 구분했다. Windows에서 Python 실행 명령이 `py -3`이면 `python` 대신 사용할 수 있다.

회신 분류와 인계만 필요한 경우:

```sh
python scripts/install.py --dest ../my-project/.agents/skills --select triage handoff
```

기존 스킬 폴더나 호스트 설정은 덮어쓰지 않는다. 스킬을 인식하지 않는 환경에서는 LITE를 사용한다. 파일을 첨부했다는 사실만으로 네이티브 스킬이 설치되지는 않는다.

## ZIP 구성

```text
project-sales/
  index.html                     EN/KR 단일 파일 소개 페이지
  LITE.md, LITE-KR.md             복사형 최소 지침
  SKILL.md, SKILL-KR.md           기본 라우터와 한국어 안내
  references/                    기능 6종 및 선택 공통 자료
  optional-skills/               독립 설치 가능한 기능별 스킬 6종
  adapters/                      웹·앱·CLI·MCP 연결 자료
  assets/, schemas/              근거·실행 제안·인계 템플릿
  scripts/                       설치·CSV 정리·검증 도구
  examples/                      허구 입력과 사용 예시
  evals/                         모델 행동 평가용 사례와 기준
  tests/                         실제 실행한 로컬 코드 테스트
  dist/                          기본·선택 스킬 설치용 소형 ZIP
```

전체 ZIP은 개발·배포 자료까지 묶은 패키지이다. 실제 스킬만 가져가려면 [기본 스킬 ZIP](dist/project-sales-core.zip) 또는 [기능별 스킬 ZIP](dist/project-sales-specialists.zip)을 사용한다. 모든 문서를 매번 모델에 넣을 필요는 없다.

## 웹·앱·CLI 연결 범위

[앱 연결 코드](adapters/app/project-sales.mjs)는 LITE와 선택한 기능 문서를 로드하고, 호스트가 연결한 허가된 읽기 함수를 호출한다. 매 호출마다 호스트 승인 콜백을 확인하며 도구 결과는 지시가 아닌 자료로 반환한다. 비용·계정·데이터 제공 범위·실제 읽기 동작은 호스트가 검토해야 한다.

```sh
node adapters/app/example.mjs
```

이 예제는 **허구의 로컬 스레드**만 읽는다. 실제 모델이나 계정을 호출하지 않는다. MCP 폴더는 기능 연결 계약이며 실행 중인 서버가 아니다. LITE를 붙여넣어도 웹 검색이나 메일 도구가 자동 생성되지는 않는다.

## 실행 경계와 검증

사용자가 발송을 요청하거나 입력 JSON에 승인 표시가 있어도 이 릴리스는 초안·제안서만 반환한다. 실제 실행기는 별도의 승인 저장소, 수신거부·중지 재확인, 예산 통제, 중복 방지, 결과 조정, 연락 적격성 검토가 필요하다. [실행 경계](references/EXECUTION-BOUNDARY.md)에 요구사항을 명시했으며 구현된 보호장치라고 주장하지 않는다.

```sh
python scripts/validate_package.py
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/bridge.test.mjs
```

실제 수행한 검사는 [VALIDATION.md](VALIDATION.md)에 기록했다. 로컬 코드 테스트와 모델별 응답 품질, 각 앱의 설치 UI, 실제 메일·CRM·캘린더 연동, 운영 환경 보안 검증은 별개다. 평가 사례만 제공한 항목은 통과했다고 표시하지 않았다.

## 소개 페이지

[index.html](index.html)을 직접 열거나 정적 HTTP 서버로 제공한다. CSS, JavaScript, EN/KR 설명, 작업별 예시, LITE 전체 원문이 파일 안에 포함되어 빌드·CDN·외부 폰트·분석 스크립트·백엔드가 필요하지 않다. 언어 전환, LITE 복사·다운로드, 환경별 사용 안내, 저장소 링크가 작동한다. 화면의 작업 예시는 설명용이며 실제 모델을 호출하지 않는다.

GitHub Pages에서는 저장소 루트의 `index.html`이 제공되도록 배포한다. CTA는 `https://github.com/JTech-CO/Project-Sales-Skill/`로 연결된다. 이 패키지는 Pages 설정이나 공개 사이트 배포를 자동 실행하지 않는다. [페이지 안내](SITE-NOTES-KR.md)에 사용법을 정리했다.

[설계 결정](DESIGN-DECISIONS.md)은 현재 패키지의 범위를, [출처](SOURCES.md)는 사용한 디자인·형식 참고자료를 기록한다. 변경 사항은 [CHANGELOG.md](CHANGELOG.md)에서 확인한다. 저장소의 [MIT 라이선스](LICENSE) 원문과 기존 저작권 표기를 기본·선택 스킬에 함께 포함했다.
