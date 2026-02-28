[English](README.md) · [العربية](i18n/README.ar.md) · [Español](i18n/README.es.md) · [Français](i18n/README.fr.md) · [日本語](i18n/README.ja.md) · [한국어](i18n/README.ko.md) · [Tiếng Việt](i18n/README.vi.md) · [中文 (简体)](i18n/README.zh-Hans.md) · [中文（繁體）](i18n/README.zh-Hant.md) · [Deutsch](i18n/README.de.md) · [Русский](i18n/README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# Organoid Segmentation (Web + CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)
![API](https://img.shields.io/badge/API-POST%20%2Fapi%2Fsegment-0f766e)
![Format](https://img.shields.io/badge/Result-Polygon%20JSON-f59e0b)

A Python application for segmenting organoids in microscopy images using OpenAI vision-capable models.

> Designed for quick local experiments: upload once, inspect overlay/mask/JSON outputs, and iterate on model choice.

This repository includes:
- A Tornado web server with upload UI.
- A CLI workflow for batch or scripted use.
- Polygon extraction, mask generation, and annotated image rendering.
- Minimal PWA support (manifest + service worker cache for core static assets).

## 🧭 Quick Navigation

| Section | Purpose |
|---|---|
| [Overview](#overview) | Understand what the project does and what it outputs |
| [Features](#features) | See key capabilities in web, CLI, and API workflows |
| [Project Structure](#project-structure) | Locate core files and runtime directories |
| [Prerequisites](#prerequisites) | Confirm environment requirements |
| [Installation](#installation) | Set up Python environment and dependencies |
| [Usage](#usage) | Run web app, CLI, or direct API calls |
| [Configuration](#configuration) | Adjust model and runtime parameters |
| [Examples](#examples) | Reuse snippets for CLI and Python workflows |
| [Development Notes](#development-notes) | Understand implementation details and local tips |
| [Troubleshooting](#troubleshooting) | Resolve common runtime and model issues |
| [Roadmap](#roadmap) | Planned next improvements |
| [Contributing](#contributing) | Submit changes effectively |
| [Support](#support) | Donation options |
| [License](#license) | Current licensing status |

## 🔍 Overview

The app accepts an input microscopy image, sends it to an OpenAI model with a strict JSON schema prompt, and returns a single polygon tracing the organoid boundary.

### 🔄 End-to-End Workflow

1. Receive image via web upload, CLI path, or API multipart form.
2. Invoke OpenAI model to produce structured polygon output.
3. Validate and clamp polygon coordinates to image bounds.
4. Render and persist three artifacts: annotated image, binary mask, polygon JSON.
5. Return URLs/paths and metadata (`width`, `height`, `confidence`).

### 📌 At a Glance

| Area | Details |
|---|---|
| Input | Microscopy image |
| Core output | Organoid polygon (`x, y` points) |
| Derived files | Annotated overlay PNG, binary mask PNG, polygon JSON |
| Access modes | Web UI, CLI, direct API call |
| Backend | Tornado (`server.py`) |
| AI path | OpenAI Responses API first, Chat Completions fallback |

Generated artifacts:
- `*_annotated.png`: source image with semi-transparent red overlay.
- `*_mask.png`: binary organoid mask.
- `*_polygon.json`: structured output (`width`, `height`, `polygon`, `confidence`).

Primary runtime files:
- `server.py`: web app + API routes.
- `organoid_segmenter.py`: segmentation and image/mask output logic.
- `segment_organoid.py`: CLI wrapper.

## ✨ Features

- Web UI at `http://localhost:8888` for quick interactive segmentation.
- REST-like endpoint `POST /api/segment` with multipart upload support.
- Configurable model name from UI and CLI (`gpt-4o-2024-08-06` default).
- Validation and clamping of polygon points to image bounds.
- Automatic output directory creation (`uploads/`, `outputs/`).
- OpenAI Responses API first, Chat Completions fallback in code path.
- Service worker support for caching core static files.

## 🗂️ Project Structure

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

## ✅ Prerequisites

- Python 3.10+ (3.11 recommended).
- `pip` and virtual environment support (`venv`).
- OpenAI API key with access to a vision-capable model.
- Network access from runtime environment to OpenAI APIs.

## ⚙️ Installation

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

Set your API key:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

## 🚀 Usage

### ⚡ Command Cheat Sheet

| Task | Command |
|---|---|
| Start web server | `python server.py` |
| Run single-image CLI segmentation | `python segment_organoid.py /path/to/image.jpg` |
| Run CLI with explicit model + output dir | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| Call API endpoint | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Run Web App

```bash
python server.py
```

Open:

```text
http://localhost:8888
```

Web flow:
1. Choose an image.
2. Optionally change model in the input field.
3. Click **Segment**.
4. Review overlay, annotated image, and mask.

### 🧪 Run CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

Optional arguments:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI prints output paths and a summary containing image dimensions and number of polygon points.

### 🔌 Call API Directly

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Example response shape:

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

## 🛠️ Configuration

Current configurable parameters:

| Parameter | Default | Where to set |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Web form `model`, CLI `--model`, API `model` field |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | none | `OPENAI_API_KEY` environment variable |

Assumptions:
- `OpenAI()` client uses environment-based credentials.
- No custom base URL or org/project settings are required unless your account setup needs them.

## 🧾 Examples

### 🐍 Programmatic Python Usage

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

### 📄 Inspect Polygon JSON

```bash
cat outputs/<name>_polygon.json
```

### 🧱 Typical Output Files

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

## 🧠 Development Notes

- Backend framework: Tornado (`server.py`).
- Frontend stack: static HTML/CSS/JS (`templates/index.html`, `static/app.js`).
- Service worker registers on page load and caches core assets listed in `static/sw.js`.
- Polygon validation ensures at least 3 points and clamps to image boundaries.
- Output generation uses Pillow (`PIL.Image`, `ImageDraw`).

Local development tips:

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 Troubleshooting

Quick mapping:

| Symptom | Likely cause | Fast check |
|---|---|---|
| Authentication error | Missing/invalid API key | `echo $OPENAI_API_KEY` in active shell |
| JSON parse or schema error | Model output malformed | Retry, or switch model in UI/CLI |
| Fewer than 3 polygon points | Low-confidence contour extraction | Try a clearer image and rerun |
| UI works but segmentation fails | Backend exception during API call | Inspect server logs for `error_type` |
| Import/module error | Environment mismatch | Reinstall dependencies in active venv |

- `openai.AuthenticationError` (or similar):
  - Verify `OPENAI_API_KEY` is set in the same shell session.
- `Model response did not contain valid JSON`:
  - Retry or use a different model; fallback parsing exists but malformed output can still fail.
- `Polygon must contain at least 3 points`:
  - Model output was invalid; retry with a clearer, higher-contrast image.
- UI loads but segmentation fails:
  - Check server logs for `error_type` and stack trace details from `/api/segment`.
- `ModuleNotFoundError`:
  - Reinstall dependencies in the active virtual environment with `pip install -r requirements.txt`.

## 🛣️ Roadmap

Potential next steps for this repository:

1. Add automated tests for polygon validation and output generation.
2. Add CI (lint, type checks, and smoke tests).
3. Add batch-mode CLI for directory-level processing.
4. Support multiple object masks or instance segmentation output.
5. Add Dockerfile and deployment documentation.
6. Add benchmark examples and sample datasets with expected outputs.
7. Finalize multilingual README files under `i18n/`.

## 🤝 Contributing

Contributions are welcome.

Recommended workflow:

1. Fork the repo and create a feature branch.
2. Make focused changes with clear commit messages.
3. Validate manual web + CLI flows locally.
4. Open a pull request describing behavior changes and test evidence.

Suggested contribution areas:
- Better prompt design for more stable polygon extraction.
- Improved frontend visualization (zoom/pan, contour smoothing).
- Test harnesses and reproducible sample fixtures.
- Documentation and localization improvements.

<a id="support"></a>

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

<a id="license"></a>

## 📄 License

No license file is currently present in this repository.

Assumption: all rights are reserved by default until a license is explicitly added.

If you plan to share or distribute this project, add a `LICENSE` file and update this section.
