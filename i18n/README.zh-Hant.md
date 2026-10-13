[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://github.com/lachlanchen/LazyingArtWebsite/raw/main/media/brand/lazyingart-intro.gif)](https://lazying.art)

# 類器官分割（Web + CLI）

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

這是一個 Python 應用程式，使用具備影像辨識能力的 OpenAI 模型，對顯微影像中的類器官進行分割。

> 針對快速本機實驗設計：上傳一次、檢查 overlay/mask/JSON 輸出，並可反覆微調模型。

## 📋 一頁總覽

| 項目 | 詳細內容 |
|---|---|
| 輸入 | 顯微影像（本機上傳、CLI 路徑或 API multipart） |
| 核心輸出 | 單一類器官多邊形與信心分數 |
| 成果物 | 標註 PNG、二值遮罩 PNG、polygon JSON |
| 介面 | Web UI、CLI、REST 端點 |
| AI 流程 | OpenAI Responses API，並備援 Chat Completions |

---

## 🧩 執行摘要

| 通道 | 進入點 | 最適用途 |
|---|---|---|
| Web | `python server.py` | 快速視覺驗證與微調 |
| CLI | `python segment_organoid.py ...` | 適合腳本化或批次執行 |
| API | `POST /api/segment` | 自動化與服務整合 |

---

此儲存庫包含：
- 一個具上傳介面的 Tornado Web 伺服器。
- 可批次或腳本化使用的 CLI 流程。
- 多邊形擷取、遮罩產生與標註影像渲染。
- 最小化 PWA 支援（Manifest + service worker 快取核心靜態資源）。

## 🧭 快速導覽

| 區段 | 用途 |
|---|---|
| [概述](#overview) | 了解專案功能與輸出內容 |
| [特性](#features) | 查看 Web、CLI、API 工作流程的主要能力 |
| [專案結構](#project-structure) | 找到核心檔案與執行期目錄 |
| [先決條件](#prerequisites) | 確認環境需求 |
| [安裝](#installation) | 設定 Python 環境與安裝套件 |
| [使用方式](#usage) | 執行網頁版、CLI 或直接呼叫 API |
| [設定](#configuration) | 調整模型與執行參數 |
| [範例](#examples) | 重複使用 CLI 與 Python 範例 |
| [開發筆記](#development-notes) | 了解實作細節與本機建議 |
| [疑難排解](#troubleshooting) | 解決常見執行與模型問題 |
| [開發路線](#roadmap) | 預計下一步改進 |
| [貢獻](#contributing) | 有效提交變更 |
| [Support](#support) | 捐款方式 |
| [授權](#license) | 目前授權狀態 |

## 🔍 概述

應用程式會接收一張顯微影像，透過嚴格的 JSON schema 提示詞送入 OpenAI 模型，並回傳一個描繪類器官邊界的單一路徑多邊形。

### 🔄 端對端流程

1. 透過網頁上傳、CLI 路徑或 API multipart form 接收影像。
2. 呼叫 OpenAI 模型以產生結構化多邊形輸出。
3. 驗證並將多邊形座標限制在影像邊界內。
4. 產生並儲存三種成果物：標註影像、二值遮罩、polygon JSON。
5. 回傳 URL/路徑與中繼資料（`width`、`height`、`confidence`）。

### 📌 重點一覽

| 區域 | 詳細內容 |
|---|---|
| 輸入 | 顯微影像 |
| 核心輸出 | 類器官多邊形（`x, y` 點） |
| 衍生檔案 | 標註 overlay PNG、二值遮罩 PNG、polygon JSON |
| 存取模式 | Web UI、CLI、直接 API 呼叫 |
| 後端 | Tornado（`server.py`） |
| AI 流程 | OpenAI Responses API（優先），備援 Chat Completions |

產生的成果物：
- `*_annotated.png`：含半透明紅色覆蓋層的原始影像。
- `*_mask.png`：類器官二值遮罩。
- `*_polygon.json`：結構化輸出（`width`、`height`、`polygon`、`confidence`）。

主要的執行期檔案：
- `server.py`：Web 應用程式與 API 路由。
- `organoid_segmenter.py`：分割邏輯及影像/遮罩輸出。
- `segment_organoid.py`：CLI 包裝介面。

## ✨ 特性

- 在 `http://localhost:8888` 提供 Web UI，供快速互動式分割使用。
- 提供類 REST 端點 `POST /api/segment`，支援 multipart 上傳。
- 可在 UI 與 CLI 中設定模型名稱（預設值 `gpt-4o-2024-08-06`）。
- 驗證並將多邊形點位約束到影像邊界內。
- 自動建立輸出目錄（`uploads/`、`outputs/`）。
- 以 OpenAI Responses API 為主要路徑，程式中也保留 Chat Completions 備援。
- Service Worker 支援快取核心靜態檔案。

## 🗂️ 專案結構

```text
Yinghan/
├─ organoid_segmenter.py          # 核心分割邏輯與輸出渲染
├─ segment_organoid.py            # CLI 入口
├─ server.py                      # Tornado 伺服器 + API
├─ requirements.txt               # Python 相依套件
├─ templates/
│  └─ index.html                  # Web UI 外殼
├─ static/
│  ├─ app.js                      # 前端上傳與結果渲染邏輯
│  ├─ styles.css                  # 介面樣式
│  ├─ manifest.json               # PWA manifest
│  └─ sw.js                       # Service worker 快取邏輯
├─ i18n/                          # 本地化 README 檔案
├─ uploads/                       # 執行期上傳儲存（gitignored）
├─ outputs/                       # 執行期分割輸出（gitignored，執行時建立）
└─ .auto-readme-work/             # README 產生流程 context/artifacts
```

### 常用修改檔案

- `server.py`：處理請求、路由與回傳格式。
- `organoid_segmenter.py`：模型提示詞、結構定義與輸出渲染。
- `templates/index.html` / `static/app.js`：前端行為。
- `segment_organoid.py`：CLI 體驗與預設參數。

## ✅ 先決條件

- Python 3.10+（建議 3.11）。
- `pip` 與虛擬環境支援（`venv`）。
- 有可使用影像模型的 OpenAI API Key。
- 執行環境可存取 OpenAI API 網路。

## ⚙️ 安裝

```bash
# 1) Clone 並進入此儲存庫
git clone <your-repo-url>
cd Yinghan

# 2) 建立並啟用虛擬環境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 3) 安裝相依套件
pip install -r requirements.txt
```

在目前 shell 設定 API Key：

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

假設：此專案未內建 `.env` 載入機制，因此需要以環境變數方式設定。

## 🚀 使用方式

### ⚡ 指令速查表

| 任務 | 指令 |
|---|---|
| 啟動網頁伺服器 | `python server.py` |
| 執行單張影像 CLI 分割 | `python segment_organoid.py /path/to/image.jpg` |
| 使用指定模型與輸出目錄執行 CLI | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| 呼叫 API 端點 | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 執行 Web 應用

```bash
python server.py
```

開啟：

```text
http://localhost:8888
```

網頁流程：
1. 選擇影像。
2. 於輸入欄位中選擇性調整模型。
3. 點擊 **Segment**。
4. 檢視 overlay、標註影像與遮罩。

### 🧪 執行 CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

可選參數：

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI 會輸出結果路徑，並在摘要中包含影像尺寸與多邊形點數。

### 🔌 直接呼叫 API

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

回應格式範例：

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

## 🛠️ 設定

目前可調整參數：

| 參數 | 預設值 | 設定位置 |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Web 表單 `model`、CLI `--model`、API `model` 欄位 |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | 無 | 環境變數 `OPENAI_API_KEY` |

假設：
- `OpenAI()` 用戶端使用環境變數憑證。
- 除非你的帳號設定需要，否則不必指定 custom base URL 或 org/project 設定。

## 🧾 範例

### 🐍 程式化 Python 用法

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

### 📄 檢視 Polygon JSON

```bash
cat outputs/<name>_polygon.json
```

### 🧱 典型輸出檔案

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

## 🧠 開發筆記

- 後端框架：Tornado（`server.py`）。
- 前端技術：靜態 HTML/CSS/JS（`templates/index.html`、`static/app.js`）。
- Service worker 於頁面載入時註冊，並快取 `static/sw.js` 中列出的核心資產。
- 多邊形驗證會確保至少有 3 點，並將座標限制在影像邊界。
- 輸出產生使用 Pillow（`PIL.Image`、`ImageDraw`）。

本機開發建議：

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 疑難排解

快速對照表：

| 症狀 | 可能原因 | 快速檢查 |
|---|---|---|
| 認證錯誤 | 缺少/無效 API Key | 在目前 shell 執行 `echo $OPENAI_API_KEY` |
| JSON 解析或 schema 錯誤 | 模型輸出格式異常 | 重試，或切換 UI/CLI 的模型 |
| 少於 3 點多邊形 | 輪廓擷取信心不足 | 改用更清晰影像後重跑 |
| 介面可用但分割失敗 | API 呼叫時後端發生例外 | 檢查 server log 是否有 `error_type` |
| 匯入/模組錯誤 | 環境不一致 | 在目前啟用的 venv 重新安裝相依套件 |

- `openai.AuthenticationError`（或同類）：
  - 確認 `OPENAI_API_KEY` 已在同一個 shell 工作階段設定。
- `Model response did not contain valid JSON`：
  - 重試或改用其他模型；雖有 fallback parsing，但格式錯誤嚴重時仍會失敗。
- `Polygon must contain at least 3 points`：
  - 模型輸出無效；請使用更清晰、對比更高的影像重試。
- UI 可載入但分割失敗：
  - 檢查 `/api/segment` 的 server logs，查看 `error_type` 與 stack trace。
- `ModuleNotFoundError`：
  - 在啟用的虛擬環境中執行 `pip install -r requirements.txt` 重新安裝。

## 🛣️ 開發路線

此儲存庫後續可考慮的項目：

1. 為多邊形驗證與輸出產生加入自動化測試。
2. 加入 CI（lint、型別檢查、smoke tests）。
3. 新增目錄層級批次處理 CLI 模式。
4. 支援多物件遮罩或 instance segmentation 輸出。
5. 補上 Dockerfile 與部署文件。
6. 增加效能基準範例與預期輸出的範例資料集。
7. 完成 `i18n/` 下的多語 README。

## 🤝 貢獻

歡迎提交貢獻。

建議流程：

1. Fork 儲存庫並建立功能分支。
2. 進行聚焦修改並使用清楚的 commit 訊息。
3. 在本機驗證手動 Web + CLI 流程。
4. 開啟 pull request，描述行為變更與測試證據。

建議的貢獻方向：
- 改進 prompt 設計，提高多邊形擷取穩定性。
- 強化前端視覺化（縮放/平移、輪廓平滑）。
- 建立測試工具與可重現的樣本固定檔。
- 文件與在地化品質提升。

## 📄 授權

此儲存庫目前沒有授權檔案。

假設：在明確加入授權檔前，預設保留所有權利。

若你要分享或散佈此專案，請新增 `LICENSE` 檔並更新此區塊。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
