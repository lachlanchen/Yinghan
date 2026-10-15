[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://lazying.art/media/brand/lazyingart-intro.gif)](https://lazying.art)

# 类器官分割（网页 + CLI）

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

这是一个使用支持视觉能力的 OpenAI 模型，对显微镜图像中的类器官进行分割的 Python 应用。

> 为快速本地实验而设计：上传一次图片，检查 overlay/mask/JSON 输出，并持续调整模型选择。

## 📋 概览

| 方面 | 说明 |
|---|---|
| 输入 | 显微镜图像（本地上传、CLI 路径或 API multipart） |
| 核心输出 | 一个带置信度分数的类器官多边形 |
| 成果物集合 | 标注 PNG、二值掩码 PNG、polygon JSON |
| 接口 | Web UI、CLI、REST 端点 |
| AI 路径 | OpenAI Responses API（含 Chat Completions 回退） |

---

## 🧩 执行摘要

| 通道 | 入口 | 最佳场景 |
|---|---|---|
| Web | `python server.py` | 快速可视化验证和调整 |
| CLI | `python segment_organoid.py ...` | 脚本化或批处理运行 |
| API | `POST /api/segment` | 自动化和服务集成 |

---

本仓库包含：
- 一个带上传 UI 的 Tornado Web 服务器。
- 一个支持批处理/脚本化的 CLI 流程。
- 多边形提取、掩码生成和标注图像渲染。
- 仅核心静态资源的最小 PWA 支持（manifest + service worker 缓存）。

## 🧭 快速导航

| 章节 | 用途 |
|---|---|
| [Overview](#overview) | 了解项目功能及输出内容 |
| [Features](#features) | 查看 Web、CLI 和 API 工作流的关键能力 |
| [Project Structure](#project-structure) | 定位核心文件和运行目录 |
| [Prerequisites](#prerequisites) | 确认环境要求 |
| [Installation](#installation) | 配置 Python 环境和依赖 |
| [Usage](#usage) | 运行 Web 应用、CLI 或直接调用 API |
| [Configuration](#configuration) | 调整模型和运行参数 |
| [Examples](#examples) | 复用 CLI 与 Python 示例 |
| [Development Notes](#development-notes) | 理解实现细节和本地开发建议 |
| [Troubleshooting](#troubleshooting) | 处理常见运行与模型问题 |
| [Roadmap](#roadmap) | 查看后续改进计划 |
| [Contributing](#contributing) | 高效提交变更 |
| [Support](#support) | 捐赠方式 |
| [License](#license) | 当前许可证状态 |

<a id="overview"></a>

## 🔍 概览

应用接收一张显微镜图像，并通过严格 JSON schema 提示词发送给 OpenAI 模型，返回一条用于描绘类器官边界的单一多边形。

### 🔄 端到端流程

1. 通过网页上传、CLI 路径或 API multipart 表单接收图像。
2. 调用 OpenAI 模型生成结构化多边形输出。
3. 校验并裁剪多边形坐标到图像边界内。
4. 渲染并持久化三类产物：标注图像、二值掩码、多边形 JSON。
5. 返回 URL/路径及元数据（`width`、`height`、`confidence`）。

### 📌 快速一览

| 范围 | 详情 |
|---|---|
| 输入 | 显微镜图像 |
| 核心输出 | 类器官多边形（`x, y` 点） |
| 衍生文件 | 标注叠加 PNG、二值掩码 PNG、多边形 JSON |
| 访问方式 | Web UI、CLI、直接 API 调用 |
| 后端 | Tornado（`server.py`） |
| AI 路径 | OpenAI Responses API 优先，Chat Completions 回退 |

生成的产物：
- `*_annotated.png`: 原图加半透明红色叠加。
- `*_mask.png`: 二值类器官掩码。
- `*_polygon.json`: 结构化输出（`width`、`height`、`polygon`、`confidence`）。

主要运行时文件：
- `server.py`：Web 应用与 API 路由。
- `organoid_segmenter.py`：分割与图像/掩码输出逻辑。
- `segment_organoid.py`：CLI 入口。

## ✨ 功能

- 在 `http://localhost:8888` 提供 Web UI，用于快速交互式分割。
- 支持 multipart 上传的 REST 风格端点 `POST /api/segment`。
- 支持在 UI 和 CLI 配置模型（默认 `gpt-4o-2024-08-06`）。
- 对多边形点进行校验并裁剪到图像边界。
- 自动创建输出目录（`uploads/`、`outputs/`）。
- 先使用 OpenAI Responses API，代码路径中保留 Chat Completions 回退。
- 支持 service worker 缓存核心静态文件。

<a id="project-structure"></a>

## 🗂️ 项目结构

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

### 通常会修改的文件

- `server.py`：请求处理、路由和响应格式。
- `organoid_segmenter.py`：模型提示词、schema 与输出渲染。
- `templates/index.html` / `static/app.js`：前端行为。
- `segment_organoid.py`：CLI 使用体验和默认参数。

<a id="prerequisites"></a>

## ✅ 前提条件

- Python 3.10+（推荐 3.11）。
- `pip` 与虚拟环境支持（`venv`）。
- 可访问具备视觉能力模型的 OpenAI API 密钥。
- 运行环境需能访问 OpenAI API 的网络。

<a id="installation"></a>

## ⚙️ 安装

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

在活动 shell 中设置 API Key：

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

默认假设：项目中未提供 `.env` 加载器，因此需要手动设置环境变量。

<a id="usage"></a>

## 🚀 使用方式

### ⚡ 命令速查表

| 任务 | 命令 |
|---|---|
| 启动 Web 服务器 | `python server.py` |
| 运行单张图像的 CLI 分割 | `python segment_organoid.py /path/to/image.jpg` |
| 使用明确模型和输出目录运行 CLI | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| 调用 API 端点 | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 运行 Web 应用

```bash
python server.py
```

打开地址：

```text
http://localhost:8888
```

Web 流程：
1. 选择一张图片。
2. 可选：在输入框中修改模型。
3. 点击 **Segment**。
4. 查看叠加图、标注图和掩码。

### 🧪 运行 CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

可选参数：

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI 会输出路径和摘要，包括图像尺寸以及多边形点数量。

### 🔌 直接调用 API

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

响应示例：

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

## 🛠️ 配置

当前可配置参数：

| 参数 | 默认值 | 设置位置 |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Web 表单 `model`，CLI `--model`，API 的 `model` 字段 |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API Key | none | `OPENAI_API_KEY` 环境变量 |

默认约定：
- `OpenAI()` 客户端使用基于环境变量的凭据。
- 除非你的账号配置需要，否则不需要自定义 base URL 或 org/project 设置。

<a id="examples"></a>

## 🧾 示例

### 🐍 编程式 Python 用法

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

### 📄 检查 Polygon JSON

```bash
cat outputs/<name>_polygon.json
```

### 🧱 典型输出文件

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

<a id="development-notes"></a>

## 🧠 开发说明

- 后端框架：Tornado（`server.py`）。
- 前端技术栈：静态 HTML/CSS/JS（`templates/index.html`、`static/app.js`）。
- Service worker 在页面加载时注册，并在 `static/sw.js` 中缓存核心资产。
- 多边形校验确保至少有 3 个点，并将其夹紧到图像边界内。
- 输出生成使用 Pillow（`PIL.Image`、`ImageDraw`）。

本地开发建议：

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

<a id="troubleshooting"></a>

## 🩺 故障排查

快速定位：

| 症状 | 可能原因 | 快速检查 |
|---|---|---|
| 认证错误 | API Key 缺失或无效 | 在当前 shell 中执行 `echo $OPENAI_API_KEY` |
| JSON 解析或 schema 错误 | 模型输出格式不符合预期 | 重试，或在 UI/CLI 中切换模型 |
| 多边形点不足 3 个 | 轮廓提取置信度过低 | 更换更清晰的图像后重试 |
| UI 可用但分割失败 | 调用 API 时后端异常 | 检查服务端日志中的 `error_type` |
| Import/module 错误 | 环境不一致 | 在当前 venv 中重装依赖 |

- `openai.AuthenticationError`（或类似）：
  - 确认 `OPENAI_API_KEY` 在同一 shell 会话中已设置。
- `Model response did not contain valid JSON`：
  - 重试或更换模型；即使存在回退解析，格式错误输出仍可能失败。
- `Polygon must contain at least 3 points`：
  - 模型输出无效；请使用更清晰且高对比度的图像重试。
- UI 能打开但分割失败：
  - 查看服务端日志中的 `/api/segment` `error_type` 与堆栈信息。
- `ModuleNotFoundError`：
  - 在活动虚拟环境中重新运行 `pip install -r requirements.txt`。

<a id="roadmap"></a>

## 🛣️ 路线图

此仓库的潜在下一步：

1. 为多边形校验与输出生成添加自动化测试。
2. 新增 CI（lint、类型检查和冒烟测试）。
3. 增加目录级批处理 CLI 模式。
4. 支持多个对象掩码或实例分割输出。
5. 增加 Dockerfile 与部署文档。
6. 增加基准测试示例和带预期输出的示例数据集。
7. 完善 `i18n/` 下的多语言 README 文件。

<a id="contributing"></a>

## 🤝 贡献

欢迎贡献。

推荐流程：

1. Fork 仓库并创建功能分支。
2. 做集中改动，并写清晰的提交信息。
3. 在本地手动验证 Web + CLI 流程。
4. 提交 PR，说明行为变更和测试依据。

建议的贡献方向：
- 改进提示词以提高多边形提取稳定性。
- 改善前端可视化（缩放/平移、轮廓平滑）。
- 测试框架与可复现示例 fixture。
- 文档与本地化改进。

<a id="support"></a>

## 📄 许可证

当前仓库中尚未包含许可证文件。

默认假设：在明确添加许可证之前，项目默认处于保留所有权利状态。

如果你打算共享或发布该项目，请添加 `LICENSE` 文件并更新此部分。


## ❤️ Support

<!-- support:start -->
[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-EA4AAA?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)
[![LazyingArt Support](https://img.shields.io/badge/LazyingArt-Support-0EA5E9?style=for-the-badge)](https://chat.lazying.art/donate)
[![PayPal Support](https://img.shields.io/badge/PayPal-Support-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen)
[![Stripe Support](https://img.shields.io/badge/Stripe-Support-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400)
<!-- support:end -->
