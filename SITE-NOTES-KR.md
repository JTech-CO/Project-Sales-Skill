# Project Sales Skill | 소개 페이지 안내

[소개 페이지 열기](https://jtech-co.github.io/Project-Sales-Skill/) · [English](SITE-NOTES.md)

저장소 루트의 `index.html` 하나가 전체 페이지이다. CSS, JavaScript, EN/KR 문구, 작업 예시, 두 언어의 LITE 원문을 포함한다. 빌드·외부 폰트·CDN·분석 스크립트·백엔드가 필요 없다. `images/`의 캡처와 배지는 README용이며 소개 페이지에서는 불러오지 않는다.

## 테마와 링크

v0.1.2는 운영체제의 라이트 설정과 무관하게 다크 테마를 기본으로 사용한다. 별도의 테마 전환 버튼은 추가하지 않았다. 강조색은 `#76dba3`, 배경은 `#101613`, 패널은 `#171f1a`, 본문은 `#e7eee9`, 보조 문구는 `#a7b7ac`이다. 초록색 주요 버튼에는 어두운 글자를 사용한다. 인쇄 시에는 밝은 용지용 색상을 사용하며 강제 색상·동작 줄이기 설정도 유지한다.

소개 페이지의 정식 주소는 `https://jtech-co.github.io/Project-Sales-Skill/`이다. 저장소 CTA는 `https://github.com/JTech-CO/Project-Sales-Skill/`를 유지한다. 두 README 상단과 캡처 이미지에서 소개 페이지로 이동할 수 있으며 한국어 캡처는 `?lang=ko`로 연결한다.

## 열기와 배포

로컬 파일을 허용하는 브라우저에서 HTML을 직접 열거나, 저장소 루트에서 `python -m http.server 8000`을 실행한다. GitHub Pages에는 `index.html`과 `.nojekyll`이 있는 저장소 루트를 배포한다. 이번 패키지는 저장소 설정·커밋·푸시·실제 사이트 재배포를 수행하지 않는다. 검증 환경의 탐색 제한은 [VALIDATION.md](VALIDATION.md)에 기록한다.

`index.html`만 다른 폴더에 옮겨도 외부 에셋은 필요하지 않다. 저장소·문서 링크는 인터넷 연결이 필요하지만 페이지 내부 기능은 원격 파일을 불러오지 않는다. canonical 등 메타데이터의 주소는 실행 의존성이 아니다.

## 사용 기능

첫 방문 기본 언어는 EN이다. EN/KR 버튼은 본문·예시·LITE·관련 메타데이터를 전환한다. `?lang=en`, `?lang=ko`가 저장된 언어보다 우선하며, 저장소가 차단돼도 수동 전환은 가능하다. 저장하는 설정은 언어 하나뿐이다.

작업 예시는 실제 모델 호출이 아닌 설명용 샘플이다. 웹/앱/CLI 탭에는 패키지의 실제 사용 방법을 제시한다. LITE 복사는 클립보드 API와 선택 기반 복사를 차례로 시도하고, 모두 차단되면 텍스트를 선택한 뒤 수동 복사를 안내한다. 다운로드 파일은 선택 언어의 LITE 원문과 일치한다. JavaScript가 없어도 영문 설명·원문·링크는 남고 동작하지 않는 버튼은 숨긴다.

## README 이미지와 유지보수

EN/KR 이미지는 현재 HTML을 로컬 Chromium에서 실제 렌더링한 캡처이다. 배포 중인 사이트에서 가져온 이미지가 아니다. 로컬 SVG 배지 세 개는 버전·라이선스·문서 언어만 표시하며 테스트나 모델 성능을 나타내지 않는다. 모든 이미지 경로는 저장소 상대경로이며 임시 첨부 주소나 임의의 이미지 호스팅 주소를 사용하지 않는다.

페이지 수정 후 `python scripts/capture_previews.py --chromium /path/to/chromium`으로 캡처를 갱신한다. 선택적 개발 도구이며 Playwright가 필요하다. 원본·이미지 해시와 해상도는 `images/preview-info.json`에 기록하며 회귀검사로 캡처의 구버전 여부를 확인한다. `images/`는 경량 기본·선택 스킬 ZIP에 포함하지 않는다.

LITE 문서를 바꾸면 HTML의 JSON과 초기 textarea도 동기화한다. 릴리스 메타데이터·SKILL·스키마·예시 버전을 함께 갱신하고, 테스트 이후 `dist/`와 `CHECKSUMS.sha256`를 다시 만든다. 자세한 명령은 [검사 안내](tests/README.md)에 있다.
