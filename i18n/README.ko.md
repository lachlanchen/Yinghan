[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# 오가노이드 분할 (Web + CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)

OpenAI 비전 지원 모델을 사용해 현미경 이미지에서 오가노이드를 분할하는 Python 애플리케이션입니다.

이 저장소에는 다음이 포함됩니다:
- 업로드 UI를 제공하는 Tornado 웹 서버
- 배치 또는 스크립트 실행용 CLI 워크플로우
- 폴리곤 추출, 마스크 생성, 주석 이미지 렌더링
- 최소 PWA 지원(매니페스트 + 핵심 정적 자산용 서비스 워커 캐시)

## 🔍 개요

앱은 입력된 현미경 이미지를 엄격한 JSON 스키마 프롬프트와 함께 OpenAI 모델에 전송한 뒤, 오가노이드 경계를 추적하는 단일 폴리곤을 반환합니다.

### 📌 한눈에 보기

| 영역 | 상세 |
|---|---|
| 입력 | 현미경 이미지 |
| 핵심 출력 | 오가노이드 폴리곤(`x, y` 좌표) |
| 파생 파일 | 주석 오버레이 PNG, 바이너리 마스크 PNG, 폴리곤 JSON |
| 접근 방식 | Web UI, CLI, 직접 API 호출 |
| 백엔드 | Tornado (`server.py`) |
| AI 경로 | OpenAI Responses API 우선, Chat Completions 폴백 |

생성되는 산출물:
- `*_annotated.png`: 반투명 빨간색 오버레이가 적용된 원본 이미지
- `*_mask.png`: 오가노이드 바이너리 마스크
- `*_polygon.json`: 구조화된 출력(`width`, `height`, `polygon`, `confidence`)

주요 런타임 파일:
- `server.py`: 웹 앱 + API 라우트
- `organoid_segmenter.py`: 분할 및 이미지/마스크 출력 로직
- `segment_organoid.py`: CLI 래퍼

## ✨ 기능

- 빠른 인터랙티브 분할을 위한 `http://localhost:8888` Web UI
- multipart 업로드를 지원하는 REST 유사 엔드포인트 `POST /api/segment`
- UI와 CLI에서 모델 이름 설정 가능(기본값 `gpt-4o-2024-08-06`)
- 이미지 경계 내로 폴리곤 좌표 검증 및 클램핑
- 출력 디렉터리 자동 생성(`uploads/`, `outputs/`)
- 코드 경로에서 OpenAI Responses API 우선, Chat Completions 폴백
- 핵심 정적 파일 캐싱을 위한 서비스 워커 지원

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
│  └─ sw.js                       # 서비스 워커 캐시 로직
├─ i18n/                          # 로컬라이즈된 README 파일(파이프라인으로 계획/생성)
├─ uploads/                       # 런타임 업로드 저장소(gitignored)
├─ outputs/                       # 런타임 분할 출력(gitignored, 런타임에 생성)
└─ .auto-readme-work/             # README 생성 파이프라인 컨텍스트/산출물
```

## ✅ 사전 요구사항

- Python 3.10+(3.x 필수, 3.11 권장)
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

API 키 설정:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

## 🚀 사용법

### 🌐 Web 앱 실행

```bash
python server.py
```

열기:

```text
http://localhost:8888
```

Web 흐름:
1. 이미지 선택
2. 필요 시 입력 필드에서 모델 변경
3. **Segment** 클릭
4. 오버레이, 주석 이미지, 마스크 확인

### 🧪 CLI 실행

```bash
python segment_organoid.py /path/to/image.jpg
```

선택 인수:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI는 출력 경로와 함께 이미지 크기 및 폴리곤 포인트 개수가 포함된 요약을 출력합니다.

### 🔌 API 직접 호출

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

응답 형식 예시:

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

## 🛠️ 구성

현재 코드에서 설정 가능한 파라미터:

- `model`:
  - 기본값: `gpt-4o-2024-08-06`
  - Web 폼 입력 또는 CLI `--model`로 설정 가능
- `out_dir`:
  - CLI 옵션 `--out-dir`(기본값 `outputs`)
  - 서버는 내부적으로 `outputs/` 사용

환경 변수:
- `OPENAI_API_KEY` (필수)

가정:
- `OpenAI()` 클라이언트는 환경 변수 기반 인증 정보를 사용합니다.
- OpenAI 계정 설정상 필요하지 않다면 custom base URL 또는 org/project 설정은 필요하지 않습니다.

## 🧾 예시

### 🐍 Python에서 프로그래밍 방식으로 사용

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
- 서비스 워커는 페이지 로드 시 등록되며 `static/sw.js`에 나열된 핵심 자산을 캐시합니다.
- 폴리곤 검증은 최소 3개 포인트를 보장하고 이미지 경계로 클램핑합니다.
- 출력 생성에는 Pillow(`PIL.Image`, `ImageDraw`)를 사용합니다.

로컬 개발 팁:

```bash
# 서버 실행
python server.py

# 기존 이미지로 CLI 실행
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 문제 해결

- `openai.AuthenticationError` 또는 유사 오류:
  - Python을 실행하는 셸에 `OPENAI_API_KEY`가 설정되어 있는지 확인하세요.
- `Model response did not contain valid JSON`:
  - 다른 모델을 시도하거나 다시 실행하세요. 폴백 파싱이 구현되어 있지만 잘못된 형식의 출력은 여전히 실패할 수 있습니다.
- `Polygon must contain at least 3 points`:
  - 모델이 유효하지 않은 폴리곤을 반환했습니다. 더 선명한 이미지로 재시도하세요.
- UI는 로드되지만 분할이 실패하는 경우:
  - `/api/segment`가 반환한 예외 유형을 서버 로그에서 확인하세요.
- `ModuleNotFoundError`:
  - 활성 환경에서 `pip install -r requirements.txt`로 의존성을 다시 설치하세요.

## 🛣️ 로드맵

이 저장소의 잠재적 다음 단계:

1. 폴리곤 검증 및 출력 생성 자동 테스트 추가
2. CI 추가(lint, 타입 체크, 스모크 테스트)
3. 디렉터리 단위 처리를 위한 배치 모드 CLI 추가
4. 다중 객체 마스크 또는 인스턴스 분할 출력 지원
5. Dockerfile 및 배포 문서 추가
6. 예상 출력이 포함된 벤치마크 예시와 샘플 데이터셋 추가
7. `i18n/` 아래 다국어 README 파일 마무리

## 🤝 기여

기여를 환영합니다.

권장 워크플로우:

1. 저장소를 포크하고 기능 브랜치를 생성합니다.
2. 명확한 커밋 메시지와 함께 집중된 변경을 만듭니다.
3. 로컬에서 웹 + CLI 흐름을 수동 검증합니다.
4. 동작 변경 사항과 테스트 근거를 설명하는 풀 리퀘스트를 엽니다.

추천 기여 영역:
- 더 안정적인 폴리곤 추출을 위한 프롬프트 설계 개선
- 향상된 프런트엔드 시각화(줌/팬, 윤곽선 스무딩)
- 테스트 하네스 및 재현 가능한 샘플 픽스처
- 문서화 및 현지화 품질 개선

## 📄 라이선스

현재 이 저장소에는 라이선스 파일이 없습니다.

가정: 라이선스가 명시적으로 추가되기 전까지 기본적으로 모든 권리가 보유됩니다.

이 프로젝트를 공유하거나 배포할 계획이라면 `LICENSE` 파일을 추가하고 이 섹션을 업데이트하세요.
