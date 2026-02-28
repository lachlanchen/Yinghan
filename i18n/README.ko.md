[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# 오가노이드 분할 (Web + CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg?style=flat-square)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg?style=flat-square)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg?style=flat-square)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg?style=flat-square)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9?style=flat-square)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316?style=flat-square)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e?style=flat-square)
![API](https://img.shields.io/badge/API-POST%20%2Fapi%2Fsegment-0f766e?style=flat-square)
![Format](https://img.shields.io/badge/Result-Polygon%20JSON-f59e0b?style=flat-square)
![Mode](https://img.shields.io/badge/Run-Web%20%2F%20CLI%20%2F%20API-8B5CF6?style=flat-square)

OpenAI의 비전 모델을 활용해 현미경 이미지에서 오가노이드를 분할하는 Python 애플리케이션입니다.

> 로컬 실험을 빠르게 수행할 수 있도록 설계되었습니다. 이미지를 한 번 업로드하고 overlay/mask/JSON 결과를 확인하면서 모델을 반복 조정하세요.

## 📋 한눈에 보기

| 항목 | 세부 내용 |
|---|---|
| 입력 | 현미경 이미지(로컬 업로드, CLI 경로, API multipart) |
| 핵심 출력 | 신뢰도 점수와 함께 단일 오가노이드 폴리곤 |
| 산출물 세트 | 주석 PNG, 이진 마스크 PNG, 폴리곤 JSON |
| 인터페이스 | 웹 UI, CLI, REST 엔드포인트 |
| AI 경로 | Chat Completions 폴백이 포함된 OpenAI Responses API |

---

## 🧩 실행 요약

| 채널 | 진입점 | 권장 사용 |
|---|---|---|
| 웹 | `python server.py` | 시각적 확인 및 조정을 빠르게 수행 |
| CLI | `python segment_organoid.py ...` | 스크립트 실행 또는 배치 처리 준비 |
| API | `POST /api/segment` | 자동화 및 서비스 통합 |

---

이 저장소에는 다음이 포함됩니다:
- 업로드 UI가 있는 Tornado 웹 서버
- 배치 또는 스크립트용 CLI 워크플로
- 폴리곤 추출, 마스크 생성, 주석 이미지 렌더링
- 핵심 정적 자산을 위한 manifest + service worker 캐시로 구현한 최소 PWA 지원

## 🧭 빠른 탐색

| 섹션 | 목적 |
|---|---|
| [개요](#overview) | 프로젝트의 기능과 출력 내용을 이해 |
| [기능](#features) | 웹, CLI, API 워크플로의 핵심 기능 확인 |
| [프로젝트 구조](#project-structure) | 핵심 파일과 런타임 디렉터리 찾기 |
| [사전 요구사항](#prerequisites) | 환경 요구사항 확인 |
| [설치](#installation) | Python 환경 및 의존성 설정 |
| [사용법](#usage) | 웹 앱, CLI, API 직접 호출 실행 |
| [설정](#configuration) | 모델 및 런타임 파라미터 조정 |
| [예시](#examples) | CLI/Python 스니펫 재사용 |
| [개발 노트](#development-notes) | 구현 상세와 로컬 팁 이해 |
| [문제 해결](#troubleshooting) | 자주 발생하는 런타임/모델 이슈 해결 |
| [로드맵](#roadmap) | 다음 개선 항목 확인 |
| [기여](#contributing) | 변경사항을 효과적으로 제출 |
| [지원](#support) | 후원 옵션 |
| [라이선스](#license) | 현재 라이선스 상태 |

<a id="overview"></a>

## 🔍 개요

앱은 입력된 현미경 이미지를 엄격한 JSON 스키마 프롬프트와 함께 OpenAI 모델에 전달하고, 오가노이드 경계를 추적하는 단일 폴리곤을 반환합니다.

### 🔄 엔드투엔드 워크플로

1. 웹 업로드, CLI 경로 또는 API multipart form으로 이미지를 받습니다.
2. OpenAI 모델을 호출해 구조화된 폴리곤 출력을 생성합니다.
3. 폴리곤 좌표를 검증하고 이미지 경계로 클램프 처리합니다.
4. 세 가지 산출물을 생성해 저장합니다: 주석 이미지, 이진 마스크, 폴리곤 JSON.
5. URL/경로와 메타데이터(`width`, `height`, `confidence`)를 반환합니다.

### 📌 한눈에 보기

| 영역 | 세부 내용 |
|---|---|
| 입력 | 현미경 이미지 |
| 핵심 출력 | 오가노이드 폴리곤 (`x, y` 좌표) |
| 파생 파일 | 주석이 적용된 오버레이 PNG, 이진 마스크 PNG, 폴리곤 JSON |
| 접근 방식 | 웹 UI, CLI, 직접 API 호출 |
| 백엔드 | Tornado (`server.py`) |
| AI 경로 | OpenAI Responses API 우선, Chat Completions 폴백 |

생성되는 산출물:
- `*_annotated.png`: 반투명 빨간 오버레이가 적용된 원본 이미지
- `*_mask.png`: 이진 오가노이드 마스크
- `*_polygon.json`: 구조화된 출력 (`width`, `height`, `polygon`, `confidence`).

주요 런타임 파일:
- `server.py`: 웹 앱 + API 라우트
- `organoid_segmenter.py`: 세그멘테이션 및 이미지/마스크 출력 로직
- `segment_organoid.py`: CLI 진입점

<a id="features"></a>

## ✨ 기능

- 빠른 대화형 분할을 위한 웹 UI: `http://localhost:8888`
- multipart 업로드를 지원하는 REST 유사 엔드포인트 `POST /api/segment`
- UI 및 CLI에서 모델 이름을 설정할 수 있음 (`gpt-4o-2024-08-06` 기본값)
- 폴리곤 좌표 검증 및 이미지 경계로 클램프
- 출력 디렉터리 자동 생성 (`uploads/`, `outputs/`)
- 코드 경로에서 OpenAI Responses API 우선 사용, Chat Completions 폴백
- 핵심 정적 파일 캐싱을 위한 service worker 지원

<a id="project-structure"></a>

## 🗂️ 프로젝트 구조

```text
Yinghan/
├─ organoid_segmenter.py          # Core segmentation logic and output rendering
├─ segment_organoid.py            # CLI entrypoint
├─ server.py                      # Tornado server + API
├─ requirements.txt               # Python dependencies
├─ templates/
│  └─ index.html                  # Web UI shell
├─ static/
│  ├─ app.js                      # Frontend upload + result rendering logic
│  ├─ styles.css                  # UI styles
│  ├─ manifest.json               # PWA manifest
│  └─ sw.js                       # Service worker cache logic
├─ i18n/                          # Localized README files
├─ uploads/                       # Runtime upload storage (gitignored)
├─ outputs/                       # Runtime segmentation outputs (gitignored, created at runtime)
└─ .auto-readme-work/             # README generation pipeline context/artifacts
```

### 주로 수정하는 파일

- `server.py`: 요청 처리, 라우팅, 응답 형식 조정
- `organoid_segmenter.py`: 모델 프롬프트, 스키마, 출력 렌더링 수정
- `templates/index.html` / `static/app.js`: UI 동작 조정
- `segment_organoid.py`: CLI 사용성 및 기본 인자 설정 조정

<a id="prerequisites"></a>

## ✅ 사전 요구사항

- Python 3.10+ (3.11 권장)
- `pip` 및 가상 환경 지원 (`venv`)
- 비전 모델 사용이 가능한 OpenAI API 키
- 실행 환경에서 OpenAI API로의 네트워크 접근

<a id="installation"></a>

## ⚙️ 설치

```bash
# 1) Clone and enter the repository
git clone <your-repo-url>
cd Yinghan

# 2) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 3) Install dependencies
pip install -r requirements.txt
```

활성 셸에서 API 키를 설정하세요.

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

가정: `.env` 로더는 포함되어 있지 않으므로 환경 변수 설정이 필수입니다.

<a id="usage"></a>

## 🚀 사용법

### ⚡ 명령어 치트시트

| 작업 | 명령 |
|---|---|
| 웹 서버 시작 | `python server.py` |
| 단일 이미지 CLI 분할 실행 | `python segment_organoid.py /path/to/image.jpg` |
| 모델 + 출력 디렉터리 지정 CLI 실행 | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| API 엔드포인트 호출 | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 웹 앱 실행

```bash
python server.py
```

열기:

```text
http://localhost:8888
```

웹 흐름:
1. 이미지를 선택합니다.
2. 필요하면 입력란에서 모델을 변경합니다.
3. **Segment**를 클릭합니다.
4. overlay, 주석 이미지, 마스크를 검토합니다.

### 🧪 CLI 실행

```bash
python segment_organoid.py /path/to/image.jpg
```

선택 인자:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI는 출력 경로와 이미지 크기, 폴리곤 점 개수를 요약해 출력합니다.

### 🔌 API 직접 호출

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

응답 예시 형태:

```json
{
  "width": 1024,
  "height": 1024,
  "polygon": [[100.0, 120.0], [110.0, 125.0]],
  "confidence": 0.92,
  "annotated_url": "/outputs/example_annotated.png",
  "mask_url": "/outputs/example_mask.png",
  "json_url": "/outputs/example_polygon.json",
  "upload_url": "/uploads/upload.jpg"
}
```

<a id="configuration"></a>

## 🛠️ 설정

현재 조정 가능한 파라미터:

| 파라미터 | 기본값 | 설정 위치 |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | 웹 폼 `model`, CLI `--model`, API `model` 필드 |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API 키 | 없음 | `OPENAI_API_KEY` 환경 변수 |

가정:
- `OpenAI()` 클라이언트는 환경 변수 기반 자격 증명을 사용합니다.
- 계정 설정에서 필요하지 않다면, 사용자 지정 base URL이나 org/project 설정이 필요하지 않습니다.

<a id="examples"></a>

## 🧾 예시

### 🐍 프로그래밍 방식 Python 사용

```python
from organoid_segmenter import segment_organoid

result = segment_organoid(
    image_path="sample.jpg",
    out_dir="outputs",
    model="gpt-4o-2024-08-06",
)

print(result.annotated_path)
print(result.mask_path)
print(result.json_path)
print(result.confidence)
```

### 📄 폴리곤 JSON 확인

```bash
cat outputs/<name>_polygon.json
```

### 🧱 전형적인 출력 파일

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

<a id="development-notes"></a>

## 🧠 개발 노트

- 백엔드 프레임워크: Tornado (`server.py`).
- 프런트엔드 스택: 정적 HTML/CSS/JS (`templates/index.html`, `static/app.js`).
- service worker는 페이지 로드 시 등록되며 `static/sw.js`에 나열된 핵심 자산을 캐시합니다.
- 폴리곤 검증은 최소 3점 이상을 보장하고, 이미지 경계로 클램프합니다.
- 출력 생성은 Pillow (`PIL.Image`, `ImageDraw`)를 사용합니다.

로컬 개발 팁:

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

<a id="troubleshooting"></a>

## 🩺 문제 해결

빠른 진단:

| 증상 | 가능한 원인 | 즉시 확인 |
|---|---|---|
| 인증 오류 | API 키 누락 또는 유효하지 않음 | 활성 셸에서 `echo $OPENAI_API_KEY` 실행 |
| JSON 파싱 또는 스키마 오류 | 모델 출력 형식 손상 | 재시도하거나 UI/CLI에서 모델 변경 |
| 폴리곤 점이 3개 미만 | 경계 추출 신뢰도가 낮음 | 더 선명한 이미지로 다시 실행 |
| UI는 작동하지만 분할 실패 | API 호출 시 백엔드 예외 | `/api/segment`의 `error_type` 확인 |
| Import/module 오류 | 환경 불일치 | 활성 venv에서 의존성 재설치 |

- `openai.AuthenticationError` (또는 유사 오류):
  - 동일한 셸 세션에서 `OPENAI_API_KEY`가 설정되어 있는지 확인하세요.
- `Model response did not contain valid JSON`:
  - 재시도하거나 다른 모델로 변경하세요. 폴백 파싱은 있지만 손상된 출력은 여전히 실패할 수 있습니다.
- `Polygon must contain at least 3 points`:
  - 모델 출력이 유효하지 않습니다. 더 선명하고 대비가 높은 이미지로 다시 시도하세요.
- UI가 로드되지만 분할이 실패:
  - 서버 로그에서 `/api/segment`의 `error_type` 및 스택 트레이스 상세를 확인하세요.
- `ModuleNotFoundError`:
  - 활성 가상환경에서 `pip install -r requirements.txt`로 의존성 재설치.

<a id="roadmap"></a>

## 🛣️ 로드맵

이 저장소의 향후 계획 항목:

1. 폴리곤 검증 및 출력 생성에 대한 자동화 테스트 추가.
2. CI 추가 (lint, 타입 검사, smoke 테스트).
3. 디렉터리 단위 처리용 배치 모드 CLI 추가.
4. 다중 객체 마스크 또는 인스턴스 분할 출력 지원.
5. Dockerfile 및 배포 문서 추가.
6. 벤치마크 예시와 예상 출력이 포함된 샘플 데이터셋 추가.
7. `i18n/` 아래 다국어 README 파일 마무리.

<a id="contributing"></a>

## 🤝 기여

기여를 환영합니다.

권장 워크플로:

1. 저장소를 Fork하고 기능 브랜치 생성.
2. 핵심 변경만 수행하고 명확한 커밋 메시지 사용.
3. 로컬에서 웹 + CLI 흐름을 수동으로 검증.
4. 동작 변경 및 테스트 근거를 설명한 Pull Request 작성.

권장 기여 영역:
- 더 안정적인 폴리곤 추출을 위한 프롬프트 설계 개선.
- 프런트엔드 시각화 개선(줌/패닝, 윤곽선 부드럽게 처리).
- 테스트 하네스와 재현 가능한 샘플 픽스처.
- 문서화 및 현지화 개선.

<a id="support"></a>

## 📄 라이선스

이 저장소에는 현재 라이선스 파일이 없습니다.

가정: 라이선스 파일이 명시적으로 추가되기 전까지 기본적으로 모든 권한이 보유됩니다.

이 프로젝트를 공유하거나 배포할 계획이라면 `LICENSE` 파일을 추가하고 이 섹션을 업데이트하세요.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
