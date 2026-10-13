[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://lazying.art)

# Phân đoạn Organoid (Web + CLI)

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

Ứng dụng Python phân đoạn organoid trong ảnh hiển vi bằng các mô hình của OpenAI có khả năng thị giác.

> Thiết kế cho thử nghiệm cục bộ nhanh: chỉ cần tải ảnh một lần, kiểm tra overlay/mask/JSON, rồi chỉnh lại lựa chọn mô hình.

## 📋 Tóm tắt nhanh

| Khía cạnh | Chi tiết |
|---|---|
| Đầu vào | Ảnh hiển vi (tải lên nội bộ, đường dẫn CLI, hoặc multipart của API) |
| Đầu ra chính | Một polygon organoid kèm độ tin cậy |
| Tập artifact | PNG đã chú thích, PNG mặt nạ nhị phân, JSON polygon |
| Giao diện | UI web, CLI, endpoint REST |
| Đường đi AI | OpenAI Responses API với fallback Chat Completions |

---

## 🧩 Tóm tắt thực thi

| Kênh | Điểm vào | Mục đích tối ưu |
|---|---|---|
| Web | `python server.py` | Kiểm tra trực quan nhanh và tinh chỉnh |
| CLI | `python segment_organoid.py ...` | Chạy theo kịch bản hoặc sẵn sàng xử lý hàng loạt |
| API | `POST /api/segment` | Tự động hóa và tích hợp dịch vụ |

---

Kho này bao gồm:
- Một máy chủ web Tornado cùng giao diện upload.
- Quy trình CLI cho dùng theo lô hoặc theo kịch bản.
- Trích xuất polygon, tạo mask và dựng ảnh có chú thích.
- Hỗ trợ PWA tối thiểu (manifest + cache service worker cho các tài nguyên tĩnh cốt lõi).

## 🧭 Điều hướng nhanh

| Mục | Mục đích |
|---|---|
| [Tổng quan](#overview) | Hiểu phần mềm làm gì và tạo ra gì |
| [Tính năng](#features) | Xem các năng lực chính của luồng web, CLI và API |
| [Cấu trúc dự án](#project-structure) | Xác định các tệp chính và thư mục runtime |
| [Điều kiện tiên quyết](#prerequisites) | Kiểm tra yêu cầu môi trường |
| [Cài đặt](#installation) | Thiết lập môi trường Python và phụ thuộc |
| [Cách dùng](#usage) | Chạy web app, CLI hoặc gọi API trực tiếp |
| [Cấu hình](#configuration) | Điều chỉnh mô hình và tham số runtime |
| [Ví dụ](#examples) | Tái sử dụng snippet cho CLI và Python |
| [Ghi chú phát triển](#development-notes) | Nắm chi tiết triển khai và mẹo local |
| [Khắc phục sự cố](#troubleshooting) | Giải quyết lỗi runtime và model thường gặp |
| [Lộ trình](#roadmap) | Các cải tiến tiếp theo dự kiến |
| [Đóng góp](#contributing) | Gửi thay đổi hiệu quả |
| [Hỗ trợ](#support) | Các tùy chọn quyên góp |
| [Giấy phép](#license) | Trạng thái cấp phép hiện tại |

<a id="overview"></a>
## 🔍 Tổng quan

Ứng dụng nhận một ảnh hiển vi đầu vào, gửi ảnh tới mô hình OpenAI với prompt JSON schema nghiêm ngặt, và trả về một polygon duy nhất mô tả ranh giới organoid.

### 🔄 Luồng end-to-end

1. Nhận ảnh từ upload web, đường dẫn CLI, hoặc form multipart của API.
2. Gọi model OpenAI để tạo output polygon có cấu trúc.
3. Kiểm tra hợp lệ và ép toạ độ polygon vào giới hạn ảnh.
4. Tạo và lưu ba artifact: ảnh có chú thích, mask nhị phân, polygon JSON.
5. Trả về URL/đường dẫn và metadata (`width`, `height`, `confidence`).

### 📌 Tóm tắt nhanh

| Khu vực | Chi tiết |
|---|---|
| Đầu vào | Ảnh hiển vi |
| Output cốt lõi | Polygon organoid (`x`, `y`) |
| Tệp dẫn xuất | Annotated overlay PNG, mask nhị phân PNG, polygon JSON |
| Chế độ truy cập | Web UI, CLI, gọi API trực tiếp |
| Backend | Tornado (`server.py`) |
| Đường đi AI | Ưu tiên OpenAI Responses API, fallback sang Chat Completions |

Artifact được tạo:
- `*_annotated.png`: ảnh gốc với lớp phủ đỏ trong suốt một phần.
- `*_mask.png`: mặt nạ nhị phân organoid.
- `*_polygon.json`: output có cấu trúc (`width`, `height`, `polygon`, `confidence`).

Tệp runtime chính:
- `server.py`: web app + tuyến API.
- `organoid_segmenter.py`: logic phân đoạn và dựng ảnh/mask.
- `segment_organoid.py`: wrapper CLI.

<a id="features"></a>
## ✨ Tính năng

- Web UI tại `http://localhost:8888` cho phân đoạn tương tác nhanh.
- Endpoint kiểu REST `POST /api/segment` hỗ trợ upload multipart.
- Cho phép cấu hình tên model từ UI và CLI (mặc định `gpt-4o-2024-08-06`).
- Kiểm tra hợp lệ và ràng buộc toạ độ polygon trong biên ảnh.
- Tự động tạo thư mục output (`uploads/`, `outputs/`).
- OpenAI Responses API được ưu tiên trước, Chat Completions là fallback trong code path.
- Hỗ trợ service worker để cache tài nguyên tĩnh cốt lõi.

<a id="project-structure"></a>
## 🗂️ Cấu trúc dự án

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

### Tệp thường sửa

- `server.py` cho xử lý request, routing và định dạng response.
- `organoid_segmenter.py` cho prompt mô hình, schema và logic dựng output.
- `templates/index.html` / `static/app.js` cho hành vi UI.
- `segment_organoid.py` cho ergonomics và mặc định của CLI.

<a id="prerequisites"></a>
## ✅ Điều kiện tiên quyết

- Python 3.10+ (3.11 khuyến nghị).
- `pip` và hỗ trợ môi trường ảo (`venv`).
- OpenAI API key có quyền truy cập model hỗ trợ thị giác.
- Môi trường runtime có kết nối mạng tới các API của OpenAI.

<a id="installation"></a>
## ⚙️ Cài đặt

```bash
# 1) Clone và mở repository

git clone <your-repo-url>
cd Yinghan

# 2) Tạo và kích hoạt môi trường ảo
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 3) Cài đặt dependencies
pip install -r requirements.txt
```

Thiết lập API key trong shell đang active:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

Giả định: không có cơ chế load `.env` đi kèm, nên cần thiết lập biến môi trường theo cách thủ công.

<a id="usage"></a>
## 🚀 Cách dùng

### ⚡ Bảng lệnh nhanh

| Nhiệm vụ | Lệnh |
|---|---|
| Khởi động web server | `python server.py` |
| Chạy phân đoạn CLI cho một ảnh | `python segment_organoid.py /path/to/image.jpg` |
| Chạy CLI với model và output dir rõ ràng | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| Gọi API endpoint | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Chạy Web App

```bash
python server.py
```

Mở:

```text
http://localhost:8888
```

Luồng web:
1. Chọn một ảnh.
2. Tùy chọn thay đổi model trong trường input.
3. Nhấn **Segment**.
4. Kiểm tra overlay, ảnh đã chú thích và mask.

### 🧪 Chạy CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

Tham số tùy chọn:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI in ra các đường dẫn output và bản tóm tắt gồm kích thước ảnh cùng số điểm polygon.

### 🔌 Gọi API trực tiếp

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Ví dụ cấu trúc phản hồi:

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
## 🛠️ Cấu hình

Tham số có thể cấu hình hiện tại:

| Tham số | Mặc định | Nơi thiết lập |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Web form `model`, CLI `--model`, trường API `model` |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | none | Biến môi trường `OPENAI_API_KEY` |

Giả định:
- Client `OpenAI()` dùng credentials từ môi trường.
- Không cần thiết lập base URL hoặc org/project custom trừ khi tài khoản yêu cầu.

<a id="examples"></a>
## 🧾 Ví dụ

### 🐍 Sử dụng Python theo kiểu lập trình

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

### 📄 Kiểm tra Polygon JSON

```bash
cat outputs/<name>_polygon.json
```

### 🧱 Tệp output điển hình

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

<a id="development-notes"></a>
## 🧠 Ghi chú phát triển

- Framework backend: Tornado (`server.py`).
- Stack frontend: HTML/CSS/JS tĩnh (`templates/index.html`, `static/app.js`).
- Service worker được đăng ký khi tải trang và cache các asset cốt lõi trong `static/sw.js`.
- Kiểm tra polygon đảm bảo có ít nhất 3 điểm và clamp vào biên ảnh.
- Việc tạo output dùng Pillow (`PIL.Image`, `ImageDraw`).

Mẹo phát triển cục bộ:

```bash
# Chạy server
python server.py

# Chạy CLI với ảnh mẫu đi kèm
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

<a id="troubleshooting"></a>
## 🩺 Khắc phục sự cố

Bản đồ nhanh:

| Triệu chứng | Nguyên nhân có thể | Kiểm tra nhanh |
|---|---|---|
| Lỗi xác thực | Thiếu/sai API key | `echo $OPENAI_API_KEY` trong shell active |
| Lỗi parse JSON hoặc schema | Kết quả model không hợp lệ | Thử lại, hoặc đổi model trên UI/CLI |
| Ít hơn 3 điểm polygon | Thuật toán contour độ tin cậy thấp | Dùng ảnh rõ hơn rồi chạy lại |
| UI chạy nhưng phân đoạn lỗi | Ngoại lệ backend khi gọi API | Kiểm tra log server cho `error_type` |
| Lỗi import/module | Môi trường lệch | Cài lại dependencies trong venv đang active |

- `openai.AuthenticationError` (hoặc tương đương):
  - Xác minh `OPENAI_API_KEY` đã được set trong cùng phiên shell.
- `Model response did not contain valid JSON`:
  - Thử lại hoặc dùng model khác; mặc dù có cơ chế fallback parse, nhưng output sai định dạng vẫn có thể lỗi.
- `Polygon must contain at least 3 points`:
  - Output model không hợp lệ; chạy lại với ảnh rõ hơn, độ tương phản cao hơn.
- UI tải được nhưng phân đoạn thất bại:
  - Kiểm tra log server, xem `error_type` và stack trace chi tiết từ `/api/segment`.
- `ModuleNotFoundError`:
  - Cài lại dependencies trong venv đang active bằng `pip install -r requirements.txt`.

<a id="roadmap"></a>
## 🛣️ Lộ trình

Những bước phát triển tiếp theo:

1. Thêm test tự động cho validation polygon và tạo output.
2. Bổ sung CI (lint, kiểm tra kiểu dữ liệu, và smoke tests).
3. Thêm CLI chế độ batch xử lý theo thư mục.
4. Hỗ trợ nhiều mặt nạ đối tượng hoặc output dạng instance segmentation.
5. Thêm Dockerfile và tài liệu triển khai.
6. Bổ sung benchmark và bộ dữ liệu mẫu cùng đầu ra tham chiếu.
7. Hoàn thiện các README đa ngôn ngữ trong `i18n/`.

<a id="contributing"></a>
## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh.

Quy trình đề xuất:

1. Fork repo và tạo nhánh tính năng.
2. Thực hiện thay đổi tập trung với commit message rõ ràng.
3. Kiểm tra thủ công luồng web + CLI tại local.
4. Mở pull request mô tả thay đổi hành vi và bằng chứng kiểm chứng.

Các hướng đóng góp gợi ý:
- Thiết kế prompt tốt hơn để trích xuất polygon ổn định hơn.
- Cải thiện trực quan frontend (zoom/pan, làm mượt contour).
- Dựng test harness và fixture mẫu tái lập được.
- Cải thiện tài liệu và bản địa hóa.

<a id="support"></a>

## 📄 Giấy phép

Không có tệp giấy phép nào hiện diện trong repo này.

Giả định: mọi quyền được bảo lưu theo mặc định cho đến khi có tệp giấy phép được thêm rõ ràng.

Nếu bạn muốn chia sẻ hoặc phân phối dự án này, hãy thêm file `LICENSE` và cập nhật phần này.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
