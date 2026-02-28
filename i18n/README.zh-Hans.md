[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# 类器官分割（Web + CLI）

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)
![API](https://img.shields.io/badge/API-POST%20%2Fapi%2Fsegment-0f766e)
![Format](https://img.shields.io/badge/Result-Polygon%20JSON-f59e0b)

这是一个 Python 应用，使用具备视觉能力的 OpenAI 模型对显微镜图像中的类器官进行分割。

> 面向本地快速实验：一次上传，即可查看 overlay/mask/JSON 输出，并快速迭代模型选择。

本仓库包含：
- 基于 Tornado 的 Web 服务器与上传界面。
- 适用于批处理或脚本化调用的 CLI 工作流。
- 多边形提取、mask 生成与标注图渲染。
- 最小化 PWA 支持（manifest + service worker 缓存核心静态资源）。

## 🧭 快速导航

| 章节 | 用途 |
|---|---|
| [概览](#-概览) | 了解项目功能与输出内容 |
| [特性](#-特性) | 查看 Web、CLI 与 API 的关键能力 |
| [项目结构](#️-项目结构) | 定位核心文件与运行目录 |
| [前置要求](#-前置要求) | 确认环境要求 |
| [安装](#️-安装) | 配置 Python 环境与依赖 |
| [使用](#-使用) | 运行 Web 应用、CLI 或直接调用 API |
| [配置](#️-配置) | 调整模型与运行参数 |
| [示例](#-示例) | 复用 CLI 与 Python 示例片段 |
| [开发说明](#-开发说明) | 了解实现细节与本地开发建议 |
| [故障排查](#️-故障排查) | 解决常见运行与模型问题 |
| [路线图](#️-路线图) | 规划中的后续改进 |
| [贡献](#-贡献) | 高效提交变更 |
| [Support](#support) | 捐赠方式 |
| [许可证](#license) | 当前许可状态 |

## 🔍 概览

应用接收显微镜图像输入，将其发送给 OpenAI 模型并使用严格 JSON schema 提示词，返回用于勾勒类器官边界的单个多边形。

### 🔄 端到端流程

1. 通过 Web 上传、CLI 路径或 API multipart 表单接收图像。
2. 调用 OpenAI 模型生成结构化多边形输出。
3. 校验多边形坐标，并将其限制在图像边界内。
4. 渲染并保存三类产物：标注图、二值 mask、多边形 JSON。
5. 返回 URL/路径及元数据（`width`、`height`、`confidence`）。

### 📌 一览

| 项目 | 说明 |
|---|---|
| 输入 | 显微镜图像 |
| 核心输出 | 类器官多边形（`x, y` 点） |
| 衍生文件 | 标注 overlay PNG、二值 mask PNG、多边形 JSON |
| 访问方式 | Web UI、CLI、直接 API 调用 |
| 后端 | Tornado（`server.py`） |
| AI 路径 | 优先 OpenAI Responses API，回退 Chat Completions |

生成产物：
- `*_annotated.png`：带半透明红色 overlay 的原图。
- `*_mask.png`：类器官二值 mask。
- `*_polygon.json`：结构化输出（`width`、`height`、`polygon`、`confidence`）。

主要运行文件：
- `server.py`：Web 应用与 API 路由。
- `organoid_segmenter.py`：分割与图像/mask 输出逻辑。
- `segment_organoid.py`：CLI 封装。

## ✨ 特性

- Web UI：`http://localhost:8888`，用于快速交互式分割。
- 类 REST 端点：`POST /api/segment`，支持 multipart 上传。
- 可在 UI 和 CLI 中配置模型名（默认 `gpt-4o-2024-08-06`）。
- 对多边形点进行校验并限制在图像边界内。
- 自动创建输出目录（`uploads/`、`outputs/`）。
- 代码路径优先 OpenAI Responses API，回退 Chat Completions。
- 支持 service worker 缓存核心静态文件。

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

## ✅ 前置要求

- Python 3.10+（推荐 3.11）。
- `pip` 与虚拟环境支持（`venv`）。
- 可访问视觉模型的 OpenAI API Key。
- 运行环境可联网访问 OpenAI APIs。

## ⚙️ 安装

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

设置 API key：

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

## 🚀 使用

### ⚡ 命令速查

| 任务 | 命令 |
|---|---|
| 启动 Web 服务器 | `python server.py` |
| 运行单图 CLI 分割 | `python segment_organoid.py /path/to/image.jpg` |
| 使用指定模型与输出目录运行 CLI | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| 调用 API 端点 | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 运行 Web 应用

```bash
python server.py
```

打开：

```text
http://localhost:8888
```

Web 流程：
1. 选择图像。
2. 可选：在输入框中修改模型。
3. 点击 **Segment**。
4. 查看 overlay、annotated image 与 mask。

### 🧪 运行 CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

可选参数：

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI 会输出结果路径及摘要信息（包含图像尺寸和多边形点数量）。

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

## 🛠️ 配置

当前可配置参数：

| 参数 | 默认值 | 设置位置 |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Web 表单 `model`、CLI `--model`、API `model` 字段 |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | 无 | `OPENAI_API_KEY` 环境变量 |

假设：
- `OpenAI()` client 使用基于环境变量的凭据。
- 除非你的账号配置有要求，否则不需要自定义 base URL 或 org/project 设置。

## 🧾 示例

### 🐍 Python 编程调用

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

### 📄 查看多边形 JSON

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

## 🧠 开发说明

- 后端框架：Tornado（`server.py`）。
- 前端栈：静态 HTML/CSS/JS（`templates/index.html`、`static/app.js`）。
- 页面加载时注册 service worker，并缓存 `static/sw.js` 中列出的核心资源。
- 多边形校验要求至少 3 个点，并限制在图像边界内。
- 输出生成依赖 Pillow（`PIL.Image`、`ImageDraw`）。

本地开发建议：

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 故障排查

快速映射：

| 现象 | 可能原因 | 快速检查 |
|---|---|---|
| 认证错误 | API key 缺失或无效 | 在当前 shell 执行 `echo $OPENAI_API_KEY` |
| JSON 解析或 schema 错误 | 模型输出格式异常 | 重试，或在 UI/CLI 切换模型 |
| 多边形点少于 3 个 | 轮廓提取置信度低 | 使用更清晰图像后重试 |
| UI 可用但分割失败 | API 调用时后端异常 | 查看服务端日志中的 `error_type` |
| 导入/模块错误 | 环境不一致 | 在当前 venv 重新安装依赖 |

- `openai.AuthenticationError`（或类似错误）：
  - 确认在同一个 shell 会话中设置了 `OPENAI_API_KEY`。
- `Model response did not contain valid JSON`：
  - 重试或更换模型；虽然有回退解析，但输出严重异常时仍会失败。
- `Polygon must contain at least 3 points`：
  - 模型输出无效；请使用更清晰、对比度更高的图像重试。
- UI 正常加载但分割失败：
  - 查看 `/api/segment` 的服务端日志中的 `error_type` 与堆栈信息。
- `ModuleNotFoundError`：
  - 在当前激活的虚拟环境中执行 `pip install -r requirements.txt` 重新安装依赖。

## 🛣️ 路线图

该仓库可考虑的后续工作：

1. 为多边形校验与输出生成增加自动化测试。
2. 增加 CI（lint、类型检查、冒烟测试）。
3. 增加目录级批处理 CLI。
4. 支持多个对象 mask 或实例分割输出。
5. 增加 Dockerfile 与部署文档。
6. 增加基准示例与带期望输出的数据集样例。
7. 完成 `i18n/` 下的多语言 README。

## 🤝 贡献

欢迎贡献。

建议流程：

1. Fork 仓库并创建功能分支。
2. 提交聚焦且信息清晰的变更。
3. 在本地验证 Web + CLI 手工流程。
4. 提交 Pull Request，说明行为变化与测试依据。

建议贡献方向：
- 优化提示词设计以提升多边形提取稳定性。
- 改进前端可视化（缩放/平移、轮廓平滑）。
- 构建测试工具链与可复现样例。
- 文档与本地化改进。

<a id="support"></a>

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

<a id="license"></a>

## 📄 许可证

当前仓库尚未包含许可证文件。

默认假设：在明确添加许可证前，项目保留所有权利。

如果你计划共享或分发该项目，请添加 `LICENSE` 文件并更新本节。
