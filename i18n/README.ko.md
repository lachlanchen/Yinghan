[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# 오가노이드 분할 (Web + CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)
![API](https://img.shields.io/badge/API-POST%20%2Fapi%2Fsegment-0f766e)
![Format](https://img.shields.io/badge/Result-Polygon%20JSON-f59e0b)

OpenAI 비전 지원 모델을 사용해 현미경 이미지를 분할하는 Python 애플리케이션입니다.

> 빠른 로컬 실험을 위해 설계되었습니다. 한 번 업로드하고, overlay/mask/JSON 결과를 확인한 뒤 모델 선택을 반복 개선할 수 있습니다.

이 저장소에는 다음이 포함되어 있습니다:
- 업로드 UI가 있는 Tornado 웹 서버
- 배치 또는 스크립트 실행용 CLI 워크플로
- 폴리곤 추출, 마스크 생성, 주석 이미지 렌더링
- 최소한의 PWA 지원(manifest + 핵심 정적 자산용 service worker 캐시)

## 🧭 빠른 탐색

| 섹션 | 목적 |
|---|---|
| [개요](#overview) | 프로젝트가 수행하는 작업과 출력 결과를 이해합니다 |
| [기능](#features) | Web, CLI, API 워크플로의 핵심 기능을 확인합니다 |
| [프로젝트 구조](#project-structure) | 핵심 파일과 런타임 디렉터리 위치를 찾습니다 |
| [사전 요구 사항](#prerequisites) | 환경 요구 사항을 확인합니다 |
| [설치](#installation) | Python 환경과 의존성을 설정합니다 |
| [사용법](#usage) | 웹 앱, CLI, 직접 API 호출을 실행합니다 |
| [설정](#configuration) | 모델 및 런타임 파라미터를 조정합니다 |
| [예시](#examples) | CLI/Python 워크플로 스니펫을 재사용합니다 |
| [개발 노트](#development-notes) | 구현 세부 사항과 로컬 개발 팁을 확인합니다 |
| [문제 해결](#troubleshooting) | 자주 발생하는 런타임/모델 이슈를 해결합니다 |
| [로드맵](#roadmap) | 다음 개선 계획을 확인합니다 |
| [기여](#contributing) | 변경 사항을 효과적으로 제출합니다 |
| [지원](#support) | 후원 옵션을 확인합니다 |
| [라이선스](#license) | 현재 라이선스 상태를 확인합니다 |

## 🔍 개요

앱은 입력 현미경 이미지를 받아, 엄격한 JSON 스키마 프롬프트와 함께 OpenAI 모델로 전송하고, 오가노이드 경계를 추적하는 단일 폴리곤을 반환합니다.

### 🔄 엔드투엔드 워크플로

1. 웹 업로드, CLI 경로, 또는 API multipart form을 통해 이미지를 받습니다.
2. 구조화된 폴리곤 출력을 생성하도록 OpenAI 모델을 호출합니다.
3. 폴리곤 좌표를 검증하고 이미지 경계 안으로 클램프합니다.
4. 주석 이미지, 이진 마스크, 폴리곤 JSON의 3개 산출물을 렌더링하고 저장합니다.
5. URL/경로와 메타데이터(`width`, `height`, `confidence`)를 반환합니다.

### 📌 한눈에 보기

| 영역 | 상세 |
|---|---|
| 입력 | 현미경 이미지 |
| 핵심 출력 | 오가노이드 폴리곤(`x, y` 좌표) |
| 파생 파일 | 주석 overlay PNG, 이진 마스크 PNG, 폴리곤 JSON |
| 접근 방식 | Web UI, CLI, 직접 API 호출 |
| 백엔드 | Tornado (`server.py`) |
| AI 경로 | OpenAI Responses API 우선, Chat Completions 폴백 |

생성되는 산출물:
- `*_annotated.png`: 반투명 빨간 overlay가 적용된 원본 이미지
- `*_mask.png`: 이진 오가노이드 마스크
- `*_polygon.json`: 구조화된 출력(`width`, `height`, `polygon`, `confidence`)

주요 런타임 파일:
- `server.py`: 웹 앱 + API 라우트
- `organoid_segmenter.py`: 분할 및 이미지/마스크 출력 로직
- `segment_organoid.py`: CLI 래퍼

## ✨ 기능

- 빠른 인터랙티브 분할을 위한 `http://localhost:8888` Web UI
- multipart 업로드를 지원하는 REST 스타일 엔드포인트 `POST /api/segment`
- UI/CLI에서 모델 이름 설정 가능(기본값 `gpt-4o-2024-08-06`)
- 폴리곤 포인트 검증 및 이미지 경계 클램프
- 출력 디렉터리 자동 생성(`uploads/`, `outputs/`)
- 코드 경로에서 OpenAI Responses API 우선, Chat Completions 폴백
- 핵심 정적 파일 캐싱을 위한 service worker 지원

## 🗂️ 프로젝트 구조

```text
Yinghan/
├─ organoid_segmenter.py          # 핵심 분할 로직 및 출력 렌더링
├─ segment_organoid.py            # CLI 진입점
├─ server.py                      # Tornado 서버 + API
├─ requirements.txt               # Python 의존성
├─ templates/
│  └─ index.html                  # Web UI 셸
├─ static/
│  ├─ app.js                      # 프런트엔드 업로드 + 결과 렌더링 로직
│  ├─ styles.css                  # UI 스타일
│  ├─ manifest.json               # PWA 매니페스트
│  └─ sw.js                       # Service worker 캐시 로직
├─ i18n/                          # 다국어 README 파일
├─ uploads/                       # 런타임 업로드 저장소(gitignored)
├─ outputs/                       # 런타임 분할 출력(gitignored, 실행 시 생성)
└─ .auto-readme-work/             # README 생성 파이프라인 컨텍스트/산출물
```

## ✅ 사전 요구 사항

- Python 3.10+ (3.11 권장)
- `pip` 및 가상 환경 지원(`venv`)
- 비전 지원 모델에 접근 가능한 OpenAI API 키
- 런타임 환경에서 OpenAI API로의 네트워크 접근

## ⚙️ 설치

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

API 키를 설정합니다:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

## 🚀 사용법

### ⚡ 명령어 치트시트

| 작업 | 명령어 |
|---|---|
| 웹 서버 시작 | `python server.py` |
| 단일 이미지 CLI 분할 실행 | `python segment_organoid.py /path/to/image.jpg` |
| 모델/출력 디렉터리 지정 CLI 실행 | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| API 엔드포인트 호출 | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Web 앱 실행

```bash
python server.py
```

열기:

```text
http://localhost:8888
```

웹 흐름:
1. 이미지를 선택합니다.
2. 필요하면 입력 필드에서 모델을 변경합니다.
3. **Segment**를 클릭합니다.
4. overlay, 주석 이미지, 마스크를 확인합니다.

### 🧪 CLI 실행

```bash
python segment_organoid.py /path/to/image.jpg
```

선택 인자:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI는 출력 경로와 이미지 크기/폴리곤 포인트 수 요약을 출력합니다.

### 🔌 API 직접 호출

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

응답 형태 예시:

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

## 🛠️ 설정

현재 설정 가능한 파라미터:

| 파라미터 | 기본값 | 설정 위치 |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | 웹 폼 `model`, CLI `--model`, API `model` 필드 |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | 없음 | `OPENAI_API_KEY` 환경 변수 |

가정:
- `OpenAI()` 클라이언트는 환경 변수 기반 자격 증명을 사용합니다.
- 계정 설정상 필요하지 않다면, 커스텀 base URL 또는 org/project 설정은 필요하지 않습니다.

## 🧾 예시

### 🐍 Python 코드 사용

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

### 🧱 일반적인 출력 파일

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

## 🧠 개발 노트

- 백엔드 프레임워크: Tornado (`server.py`)
- 프런트엔드 스택: 정적 HTML/CSS/JS (`templates/index.html`, `static/app.js`)
- service worker는 페이지 로드 시 등록되며 `static/sw.js`에 정의된 핵심 자산을 캐시합니다.
- 폴리곤 검증은 최소 3개 포인트를 보장하고 이미지 경계로 클램프합니다.
- 출력 생성은 Pillow(`PIL.Image`, `ImageDraw`)를 사용합니다.

로컬 개발 팁:

```bash
# 서버 실행
python server.py

# 포함된 샘플 이미지로 CLI 실행
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 문제 해결

빠른 매핑:

| 증상 | 가능성이 높은 원인 | 빠른 확인 |
|---|---|---|
| 인증 오류 | API 키 누락/오류 | 활성 셸에서 `echo $OPENAI_API_KEY` |
| JSON 파싱/스키마 오류 | 모델 출력 형식 불량 | 재시도하거나 UI/CLI에서 모델 변경 |
| 폴리곤 포인트가 3개 미만 | 저신뢰 경계 추출 | 더 선명한 이미지로 재실행 |
| UI는 동작하지만 분할 실패 | API 호출 중 백엔드 예외 | 서버 로그의 `error_type` 확인 |
| import/module 오류 | 환경 불일치 | 활성 venv에서 의존성 재설치 |

- `openai.AuthenticationError`(또는 유사 오류):
  - 동일 셸 세션에서 `OPENAI_API_KEY`가 설정되어 있는지 확인하세요.
- `Model response did not contain valid JSON`:
  - 재시도하거나 다른 모델을 사용하세요. 폴백 파싱이 있어도 출력이 손상되면 실패할 수 있습니다.
- `Polygon must contain at least 3 points`:
  - 모델 출력이 유효하지 않았습니다. 대비가 더 뚜렷한 이미지로 다시 시도하세요.
- UI는 로드되지만 분할이 실패하는 경우:
  - `/api/segment`의 `error_type` 및 스택 트레이스 세부 정보를 서버 로그에서 확인하세요.
- `ModuleNotFoundError`:
  - 활성 가상 환경에서 `pip install -r requirements.txt`로 의존성을 다시 설치하세요.

## 🛣️ 로드맵

이 저장소의 다음 단계 후보:

1. 폴리곤 검증 및 출력 생성 자동화 테스트 추가
2. CI 추가(lint, 타입 검사, 스모크 테스트)
3. 디렉터리 단위 처리용 배치 모드 CLI 추가
4. 다중 객체 마스크 또는 인스턴스 분할 출력 지원
5. Dockerfile 및 배포 문서 추가
6. 예상 출력이 포함된 벤치마크 예시와 샘플 데이터셋 추가
7. `i18n/` 아래 다국어 README 최종 정리

## 🤝 기여

기여를 환영합니다.

권장 워크플로:

1. 저장소를 포크하고 기능 브랜치를 생성합니다.
2. 명확한 커밋 메시지와 함께 집중된 변경을 수행합니다.
3. 로컬에서 웹 + CLI 수동 플로를 검증합니다.
4. 동작 변경 사항과 테스트 근거를 설명하는 Pull Request를 엽니다.

권장 기여 영역:
- 더 안정적인 폴리곤 추출을 위한 프롬프트 설계 개선
- 프런트엔드 시각화 개선(줌/팬, 윤곽선 스무딩)
- 테스트 하네스 및 재현 가능한 샘플 픽스처
- 문서화 및 현지화 개선

<a id="support"></a>

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

<a id="license"></a>

## 📄 라이선스

현재 이 저장소에는 라이선스 파일이 없습니다.

가정: 라이선스가 명시적으로 추가되기 전까지 기본적으로 모든 권리는 보유됩니다.

이 프로젝트를 공유하거나 배포할 계획이라면 `LICENSE` 파일을 추가하고 이 섹션을 업데이트하세요.
