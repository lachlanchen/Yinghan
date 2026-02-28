[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# 類器官分割（Web + CLI）

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)

這是一個 Python 應用程式，使用具備視覺能力的 OpenAI 模型，對顯微鏡影像中的類器官進行分割。

此儲存庫包含：
- 一個帶有上傳 UI 的 Tornado Web 伺服器。
- 可用於批次或腳本化流程的 CLI 工作流程。
- 多邊形擷取、遮罩產生與標註影像渲染。
- 基本 PWA 支援（manifest + 針對核心靜態資源的 service worker 快取）。

## 🔍 概覽

應用程式會接收輸入的顯微鏡影像，透過嚴格 JSON schema 提示將影像送至 OpenAI 模型，並回傳一個描繪類器官邊界的單一多邊形。

### 📌 快速總覽

| 區域 | 詳細內容 |
|---|---|
| 輸入 | 顯微鏡影像 |
| 核心輸出 | 類器官多邊形（`x, y` 點） |
| 衍生檔案 | 標註疊加 PNG、二值遮罩 PNG、多邊形 JSON |
| 存取方式 | Web UI、CLI、直接 API 呼叫 |
| 後端 | Tornado（`server.py`） |
| AI 路徑 | 以 OpenAI Responses API 為優先，Chat Completions 為備援 |

產生的工件：
- `*_annotated.png`：含半透明紅色疊加層的原始影像。
- `*_mask.png`：類器官二值遮罩。
- `*_polygon.json`：結構化輸出（`width`、`height`、`polygon`、`confidence`）。

主要執行期檔案：
- `server.py`：Web 應用程式 + API 路由。
- `organoid_segmenter.py`：分割與影像/遮罩輸出邏輯。
- `segment_organoid.py`：CLI 包裝器。

## ✨ 功能

- 提供 `http://localhost:8888` 的 Web UI，可快速互動式分割。
- 提供類 REST 端點 `POST /api/segment`，支援 multipart 上傳。
- 可於 UI 與 CLI 設定模型名稱（預設為 `gpt-4o-2024-08-06`）。
- 驗證多邊形點位並限制於影像邊界內。
- 自動建立輸出目錄（`uploads/`、`outputs/`）。
- 程式路徑中以 OpenAI Responses API 優先，Chat Completions 作為備援。
- 支援 service worker 快取核心靜態檔案。

## 🗂️ 專案結構

```text
Yinghan/
├─ organoid_segmenter.py          # 核心分割邏輯與輸出渲染
├─ segment_organoid.py            # CLI 入口點
├─ server.py                      # Tornado 伺服器 + API
├─ requirements.txt               # Python 相依套件
├─ templates/
│  └─ index.html                  # Web UI 外殼
├─ static/
│  ├─ app.js                      # 前端上傳 + 結果渲染邏輯
│  ├─ styles.css                  # UI 樣式
│  ├─ manifest.json               # PWA manifest
│  └─ sw.js                       # Service worker 快取邏輯
├─ i18n/                          # 本地化 README 檔案（由流程規劃/產生）
├─ uploads/                       # 執行期上傳儲存（gitignored）
├─ outputs/                       # 執行期分割輸出（gitignored，於執行時建立）
└─ .auto-readme-work/             # README 產生流程脈絡/工件
```

## ✅ 先決條件

- Python 3.10+（需要 3.x；建議 3.11）。
- 具備可存取視覺模型的 OpenAI API 金鑰。
- 執行環境可連線至 OpenAI APIs。

## ⚙️ 安裝

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

設定你的 API 金鑰：

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

## 🚀 使用方式

### 🌐 執行 Web 應用程式

```bash
python server.py
```

開啟：

```text
http://localhost:8888
```

Web 流程：
1. 選擇影像。
2. 視需要在輸入欄位中更改模型。
3. 點擊 **Segment**。
4. 檢視疊加圖、標註影像與遮罩。

### 🧪 執行 CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

可選參數：

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI 會列印輸出路徑，以及包含影像尺寸與多邊形點數的摘要。

### 🔌 直接呼叫 API

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

回應範例結構：

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

程式碼中目前可設定的參數：

- `model`：
  - 預設：`gpt-4o-2024-08-06`
  - 可透過 Web 表單輸入或 CLI `--model` 設定
- `out_dir`：
  - CLI 選項 `--out-dir`（預設 `outputs`）
  - 伺服器內部使用 `outputs/`

環境變數：
- `OPENAI_API_KEY`（必填）。

假設：
- `OpenAI()` client 使用環境變數中的憑證。
- 除非你的 OpenAI 帳戶設定有需要，否則不需自訂 base URL 或 org/project 設定。

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

## 🧠 開發備註

- 後端框架：Tornado（`server.py`）。
- 前端技術棧：靜態 HTML/CSS/JS（`templates/index.html`、`static/app.js`）。
- Service worker 會在頁面載入時註冊，並快取 `static/sw.js` 中列出的核心資源。
- 多邊形驗證會確保至少有 3 個點，並限制在影像邊界內。
- 輸出產生使用 Pillow（`PIL.Image`、`ImageDraw`）。

本機開發建議：

```bash
# Run server
python server.py

# Run CLI against an existing image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 疑難排解

- `openai.AuthenticationError` 或類似錯誤：
  - 確認執行 Python 的 shell 已設定 `OPENAI_API_KEY`。
- `Model response did not contain valid JSON`：
  - 嘗試其他模型或重新執行；雖然已實作備援解析，但輸出格式錯誤仍可能失敗。
- `Polygon must contain at least 3 points`：
  - 模型回傳了無效多邊形；請使用更清晰的影像重試。
- UI 可載入但分割失敗：
  - 檢查伺服器日誌中 `/api/segment` 回傳的例外型別。
- `ModuleNotFoundError`：
  - 在目前啟用的環境中，重新執行 `pip install -r requirements.txt` 安裝相依套件。

## 🛣️ 路線圖

此儲存庫可能的下一步：

1. 為多邊形驗證與輸出產生加入自動化測試。
2. 加入 CI（lint、型別檢查與 smoke tests）。
3. 為目錄層級處理加入批次模式 CLI。
4. 支援多物件遮罩或實例分割輸出。
5. 新增 Dockerfile 與部署文件。
6. 加入基準測試範例與含預期輸出的樣本資料集。
7. 完成 `i18n/` 下的多語 README 檔案。

## 🤝 貢獻

歡迎貢獻。

建議流程：

1. Fork 此儲存庫並建立功能分支。
2. 進行聚焦修改，並撰寫清楚的 commit 訊息。
3. 在本機驗證手動 Web + CLI 流程。
4. 開啟 pull request，描述行為變更與測試證據。

建議貢獻方向：
- 改進 prompt 設計，提升多邊形擷取穩定性。
- 改善前端視覺化（縮放/平移、輪廓平滑）。
- 測試框架與可重現的樣本 fixture。
- 文件與在地化改進。

## 📄 授權

此儲存庫目前尚未提供授權檔案。

假設：在明確加入授權之前，預設為保留所有權利。

若你計畫分享或散佈此專案，請新增 `LICENSE` 檔案並更新本節。
