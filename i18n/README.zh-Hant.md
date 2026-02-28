[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# 類器官分割（Web + CLI）

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)
![API](https://img.shields.io/badge/API-POST%20%2Fapi%2Fsegment-0f766e)
![Format](https://img.shields.io/badge/Result-Polygon%20JSON-f59e0b)

這是一個 Python 應用程式，使用具備視覺能力的 OpenAI 模型，將顯微影像中的類器官進行分割。

> 為快速本機實驗而設計：一次上傳、檢視 overlay/mask/JSON 輸出，並迭代調整模型選擇。

此儲存庫包含：
- 一個具上傳 UI 的 Tornado Web 伺服器。
- 可用於批次或腳本化使用情境的 CLI 流程。
- 多邊形擷取、遮罩產生與標註影像渲染。
- 最小化 PWA 支援（manifest + service worker 快取核心靜態資源）。

<a id="quick-navigation"></a>

## 🧭 快速導覽

| 區段 | 用途 |
|---|---|
| [概覽](#overview) | 了解專案用途與輸出內容 |
| [功能](#features) | 查看 Web、CLI 與 API 流程的主要能力 |
| [專案結構](#project-structure) | 快速定位核心檔案與執行期目錄 |
| [先決條件](#prerequisites) | 確認環境需求 |
| [安裝](#installation) | 建立 Python 環境並安裝相依套件 |
| [使用方式](#usage) | 執行 Web 應用、CLI 或直接呼叫 API |
| [設定](#configuration) | 調整模型與執行參數 |
| [範例](#examples) | 重用 CLI 與 Python 範例片段 |
| [開發說明](#development-notes) | 掌握實作細節與本機開發建議 |
| [疑難排解](#troubleshooting) | 排除常見執行與模型問題 |
| [路線圖](#roadmap) | 已規劃的下一步改進 |
| [貢獻](#contributing) | 了解如何有效提交變更 |
| [Support](#support) | 捐助方式 |
| [授權](#license) | 目前授權狀態 |

<a id="overview"></a>

## 🔍 概覽

此應用會接收輸入的顯微影像，透過嚴格 JSON schema prompt 送至 OpenAI 模型，回傳一個描繪類器官邊界的單一多邊形。

### 🔄 端到端流程

1. 透過 Web 上傳、CLI 路徑或 API multipart form 接收影像。
2. 呼叫 OpenAI 模型產生結構化多邊形輸出。
3. 驗證多邊形座標，並限制在影像邊界內。
4. 產生並保存三種工件：標註影像、二值遮罩、多邊形 JSON。
5. 回傳 URL/路徑與中繼資料（`width`、`height`、`confidence`）。

### 📌 重點速覽

| 項目 | 詳細內容 |
|---|---|
| 輸入 | 顯微影像 |
| 核心輸出 | 類器官多邊形（`x, y` 點位） |
| 衍生檔案 | 標註 overlay PNG、二值遮罩 PNG、多邊形 JSON |
| 存取方式 | Web UI、CLI、直接 API 呼叫 |
| 後端 | Tornado（`server.py`） |
| AI 路徑 | 優先 OpenAI Responses API，備援 Chat Completions |

產生工件：
- `*_annotated.png`：帶半透明紅色覆蓋的原始影像。
- `*_mask.png`：類器官二值遮罩。
- `*_polygon.json`：結構化輸出（`width`、`height`、`polygon`、`confidence`）。

主要執行期檔案：
- `server.py`：Web 應用 + API 路由。
- `organoid_segmenter.py`：分割與影像/遮罩輸出邏輯。
- `segment_organoid.py`：CLI 包裝入口。

<a id="features"></a>

## ✨ 功能

- 提供 `http://localhost:8888` Web UI，適合快速互動式分割。
- 提供類 REST 端點 `POST /api/segment`，支援 multipart 上傳。
- UI 與 CLI 皆可設定模型名稱（預設 `gpt-4o-2024-08-06`）。
- 驗證並限制多邊形點位在影像邊界內。
- 自動建立輸出目錄（`uploads/`、`outputs/`）。
- 程式路徑中優先使用 OpenAI Responses API，並含 Chat Completions 備援。
- 支援 service worker 快取核心靜態檔案。

<a id="project-structure"></a>

## 🗂️ 專案結構

```text
Yinghan/
├─ organoid_segmenter.py          # 核心分割邏輯與輸出渲染
├─ segment_organoid.py            # CLI 入口點
├─ server.py                      # Tornado 伺服器 + API
├─ requirements.txt               # Python 相依套件
├─ templates/
│  └─ index.html                  # Web UI 框架頁
├─ static/
│  ├─ app.js                      # 前端上傳 + 結果渲染邏輯
│  ├─ styles.css                  # UI 樣式
│  ├─ manifest.json               # PWA manifest
│  └─ sw.js                       # Service worker 快取邏輯
├─ i18n/                          # 多語 README 檔案
├─ uploads/                       # 執行期上傳儲存（gitignored）
├─ outputs/                       # 執行期分割輸出（gitignored，執行時建立）
└─ .auto-readme-work/             # README 產生流程 context/artifacts
```

<a id="prerequisites"></a>

## ✅ 先決條件

- Python 3.10+（建議 3.11）。
- `pip` 與虛擬環境支援（`venv`）。
- 具備可使用視覺模型的 OpenAI API key。
- 執行環境可連線至 OpenAI APIs。

<a id="installation"></a>

## ⚙️ 安裝

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

設定 API key：

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

<a id="usage"></a>

## 🚀 使用方式

### ⚡ 指令速查表

| 任務 | 指令 |
|---|---|
| 啟動 Web 伺服器 | `python server.py` |
| 對單張圖片執行 CLI 分割 | `python segment_organoid.py /path/to/image.jpg` |
| 以指定模型與輸出目錄執行 CLI | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| 呼叫 API 端點 | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 執行 Web 應用

```bash
python server.py
```

開啟：

```text
http://localhost:8888
```

Web 流程：
1. 選擇影像。
2. 視需要在輸入欄位修改模型。
3. 點擊 **Segment**。
4. 查看 overlay、標註影像與遮罩。

### 🧪 執行 CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

可選參數：

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI 會印出輸出路徑，以及包含影像尺寸和多邊形點數的摘要。

### 🔌 直接呼叫 API

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

回應結構範例：

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

## 🛠️ 設定

目前可設定的參數：

| 參數 | 預設值 | 設定位置 |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Web 表單 `model`、CLI `--model`、API `model` 欄位 |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | 無 | `OPENAI_API_KEY` 環境變數 |

假設：
- `OpenAI()` client 使用環境變數中的憑證。
- 除非你的帳戶設定需要，否則不需自訂 base URL 或 org/project 設定。

<a id="examples"></a>

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

<a id="development-notes"></a>

## 🧠 開發說明

- 後端框架：Tornado（`server.py`）。
- 前端技術：靜態 HTML/CSS/JS（`templates/index.html`、`static/app.js`）。
- Service worker 於頁面載入時註冊，並快取 `static/sw.js` 中列出的核心資源。
- 多邊形驗證確保至少 3 個點，並限制於影像邊界內。
- 輸出生成使用 Pillow（`PIL.Image`、`ImageDraw`）。

本機開發建議：

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

<a id="troubleshooting"></a>

## 🩺 疑難排解

快速對照：

| 症狀 | 可能原因 | 快速檢查 |
|---|---|---|
| 驗證失敗錯誤 | API key 缺失或無效 | 在當前 shell 執行 `echo $OPENAI_API_KEY` |
| JSON 解析或 schema 錯誤 | 模型輸出格式異常 | 重試，或於 UI/CLI 切換模型 |
| 多邊形點少於 3 個 | 輪廓擷取信心不足 | 使用更清晰影像後重跑 |
| UI 可用但分割失敗 | API 呼叫時後端例外 | 檢查 server logs 的 `error_type` |
| 匯入/模組錯誤 | 環境不一致 | 在啟用的 venv 重新安裝相依套件 |

- `openai.AuthenticationError`（或類似錯誤）：
  - 確認 `OPENAI_API_KEY` 已在同一個 shell session 設定。
- `Model response did not contain valid JSON`：
  - 重試或改用其他模型；雖有備援解析，但輸出格式嚴重異常時仍可能失敗。
- `Polygon must contain at least 3 points`：
  - 模型輸出無效；請使用更清晰、對比更高的影像重試。
- UI 可載入但分割失敗：
  - 檢查 `/api/segment` 的 server logs，查看 `error_type` 與 stack trace。
- `ModuleNotFoundError`：
  - 在目前啟用的虛擬環境中執行 `pip install -r requirements.txt` 重新安裝。

<a id="roadmap"></a>

## 🛣️ 路線圖

此儲存庫可考慮的下一步：

1. 為多邊形驗證與輸出生成加入自動化測試。
2. 導入 CI（lint、型別檢查、smoke tests）。
3. 增加支援目錄層級處理的批次 CLI 模式。
4. 支援多目標遮罩或實例分割輸出。
5. 加入 Dockerfile 與部署文件。
6. 加入基準範例與附預期輸出的樣本資料集。
7. 完成 `i18n/` 下的多語 README。

<a id="contributing"></a>

## 🤝 貢獻

歡迎貢獻。

建議流程：

1. Fork 此儲存庫並建立功能分支。
2. 進行聚焦修改，並撰寫清楚的 commit 訊息。
3. 在本機驗證手動 Web + CLI 流程。
4. 開啟 pull request，描述行為變更與測試證據。

建議貢獻方向：
- 改進 prompt 設計，提高多邊形擷取穩定性。
- 強化前端視覺化（縮放/平移、輪廓平滑）。
- 建立測試框架與可重現樣本 fixtures。
- 文件與在地化改進。

<a id="support"></a>

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

<a id="license"></a>

## 📄 授權

此儲存庫目前尚未提供授權檔。

假設：在明確加入授權前，預設保留所有權利。

若你計畫分享或散布此專案，請新增 `LICENSE` 檔並更新本節。
