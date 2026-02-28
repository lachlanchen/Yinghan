[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# Phân đoạn Organoid (Web + CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)
![API](https://img.shields.io/badge/API-POST%20%2Fapi%2Fsegment-0f766e)
![Format](https://img.shields.io/badge/Result-Polygon%20JSON-f59e0b)

Một ứng dụng Python để phân đoạn organoid trong ảnh hiển vi bằng các mô hình có khả năng thị giác của OpenAI.

> Được thiết kế cho thử nghiệm cục bộ nhanh: tải ảnh một lần, kiểm tra overlay/mask/JSON, rồi lặp lại với model khác.

Kho lưu trữ này bao gồm:
- Máy chủ web Tornado với giao diện tải ảnh lên.
- Quy trình CLI cho xử lý hàng loạt hoặc tích hợp script.
- Trích xuất polygon, tạo mask, và dựng ảnh chú thích.
- Hỗ trợ PWA tối thiểu (manifest + cache service worker cho các static asset cốt lõi).

## 🧭 Điều Hướng Nhanh

| Mục | Mục đích |
|---|---|
| [Tổng quan](#-tổng-quan) | Hiểu dự án làm gì và trả ra những gì |
| [Tính năng](#-tính-năng) | Xem các khả năng chính của luồng web, CLI và API |
| [Cấu trúc dự án](#-cấu-trúc-dự-án) | Xác định vị trí tệp chính và thư mục runtime |
| [Điều kiện tiên quyết](#-điều-kiện-tiên-quyết) | Xác nhận yêu cầu môi trường |
| [Cài đặt](#-cài-đặt) | Thiết lập môi trường Python và dependency |
| [Cách dùng](#-cách-dùng) | Chạy web app, CLI hoặc gọi API trực tiếp |
| [Cấu hình](#️-cấu-hình) | Điều chỉnh model và tham số runtime |
| [Ví dụ](#-ví-dụ) | Tái sử dụng snippet cho CLI và Python |
| [Ghi chú phát triển](#-ghi-chú-phát-triển) | Nắm chi tiết triển khai và mẹo local |
| [Khắc phục sự cố](#-khắc-phục-sự-cố) | Xử lý các lỗi runtime/model phổ biến |
| [Lộ trình](#-lộ-trình) | Các cải tiến dự kiến tiếp theo |
| [Đóng góp](#-đóng-góp) | Cách gửi thay đổi hiệu quả |
| [Support](#support) | Các lựa chọn ủng hộ |
| [Giấy phép](#license) | Trạng thái giấy phép hiện tại |

## 🔍 Tổng quan

Ứng dụng nhận ảnh hiển vi đầu vào, gửi ảnh đến model OpenAI với prompt JSON schema nghiêm ngặt, và trả về một polygon duy nhất biểu diễn biên organoid.

### 🔄 Luồng End-to-End

1. Nhận ảnh qua upload web, đường dẫn CLI, hoặc multipart form API.
2. Gọi model OpenAI để tạo output polygon có cấu trúc.
3. Kiểm tra hợp lệ và giới hạn tọa độ polygon trong biên ảnh.
4. Dựng và lưu ba artifact: ảnh chú thích, mask nhị phân, JSON polygon.
5. Trả về URL/đường dẫn và metadata (`width`, `height`, `confidence`).

### 📌 Tóm tắt nhanh

| Khu vực | Chi tiết |
|---|---|
| Input | Ảnh hiển vi |
| Output cốt lõi | Polygon organoid (các điểm `x, y`) |
| Tệp phát sinh | Overlay PNG có chú thích, mask nhị phân PNG, polygon JSON |
| Cách truy cập | Web UI, CLI, gọi API trực tiếp |
| Backend | Tornado (`server.py`) |
| Luồng AI | Ưu tiên OpenAI Responses API, fallback sang Chat Completions |

Các artifact được tạo:
- `*_annotated.png`: ảnh nguồn với lớp phủ đỏ bán trong suốt.
- `*_mask.png`: mask nhị phân của organoid.
- `*_polygon.json`: output có cấu trúc (`width`, `height`, `polygon`, `confidence`).

Các tệp runtime chính:
- `server.py`: ứng dụng web + route API.
- `organoid_segmenter.py`: logic phân đoạn và xuất ảnh/mask.
- `segment_organoid.py`: wrapper CLI.

## ✨ Tính năng

- Web UI tại `http://localhost:8888` cho phân đoạn tương tác nhanh.
- Endpoint kiểu REST `POST /api/segment` hỗ trợ upload multipart.
- Có thể cấu hình tên model từ UI và CLI (mặc định `gpt-4o-2024-08-06`).
- Kiểm tra hợp lệ và giới hạn điểm polygon trong biên ảnh.
- Tự động tạo thư mục output (`uploads/`, `outputs/`).
- Luồng code ưu tiên OpenAI Responses API, fallback sang Chat Completions.
- Hỗ trợ service worker để cache các tệp static cốt lõi.

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

## ✅ Điều kiện tiên quyết

- Python 3.10+ (khuyến nghị 3.11).
- `pip` và hỗ trợ môi trường ảo (`venv`).
- OpenAI API key có quyền truy cập model hỗ trợ thị giác.
- Môi trường runtime có kết nối mạng tới OpenAI APIs.

## ⚙️ Cài đặt

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

Thiết lập API key:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

## 🚀 Cách dùng

### ⚡ Bảng lệnh nhanh

| Tác vụ | Lệnh |
|---|---|
| Khởi động web server | `python server.py` |
| Chạy phân đoạn CLI cho một ảnh | `python segment_organoid.py /path/to/image.jpg` |
| Chạy CLI với model + thư mục output tường minh | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| Gọi API endpoint | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Chạy Web App

```bash
python server.py
```

Mở:

```text
http://localhost:8888
```

Luồng trên web:
1. Chọn một ảnh.
2. Có thể đổi model trong ô input nếu cần.
3. Nhấn **Segment**.
4. Xem overlay, ảnh annotated và mask.

### 🧪 Chạy CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

Tham số tùy chọn:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI sẽ in ra đường dẫn output và bản tóm tắt chứa kích thước ảnh cùng số điểm polygon.

### 🔌 Gọi API trực tiếp

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Ví dụ cấu trúc response:

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

## 🛠️ Cấu hình

Các tham số hiện có thể cấu hình:

| Tham số | Mặc định | Nơi thiết lập |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Web form `model`, CLI `--model`, trường API `model` |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | none | Biến môi trường `OPENAI_API_KEY` |

Giả định:
- Client `OpenAI()` dùng thông tin xác thực dựa trên biến môi trường.
- Không cần custom base URL hoặc cấu hình org/project trừ khi thiết lập tài khoản của bạn yêu cầu.

## 🧾 Ví dụ

### 🐍 Dùng Python theo kiểu lập trình

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

### 🧱 Các tệp output điển hình

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

## 🧠 Ghi chú phát triển

- Framework backend: Tornado (`server.py`).
- Stack frontend: HTML/CSS/JS tĩnh (`templates/index.html`, `static/app.js`).
- Service worker được đăng ký khi tải trang và cache các asset cốt lõi được liệt kê trong `static/sw.js`.
- Kiểm tra polygon đảm bảo có ít nhất 3 điểm và giới hạn trong biên ảnh.
- Việc tạo output dùng Pillow (`PIL.Image`, `ImageDraw`).

Mẹo phát triển cục bộ:

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 Khắc phục sự cố

Bảng đối chiếu nhanh:

| Triệu chứng | Nguyên nhân có thể | Cách kiểm tra nhanh |
|---|---|---|
| Lỗi xác thực | Thiếu/sai API key | `echo $OPENAI_API_KEY` trong shell hiện tại |
| Lỗi parse JSON hoặc schema | Output model sai định dạng | Chạy lại hoặc đổi model trong UI/CLI |
| Ít hơn 3 điểm polygon | Trích xuất contour độ tin cậy thấp | Dùng ảnh rõ hơn rồi chạy lại |
| UI chạy nhưng phân đoạn thất bại | Backend exception khi gọi API | Kiểm tra log server với `error_type` |
| Lỗi import/module | Sai lệch môi trường | Cài lại dependency trong venv đang dùng |

- `openai.AuthenticationError` (hoặc tương tự):
  - Xác minh `OPENAI_API_KEY` được thiết lập trong đúng shell session.
- `Model response did not contain valid JSON`:
  - Thử lại hoặc dùng model khác; đã có fallback parse nhưng output sai định dạng vẫn có thể lỗi.
- `Polygon must contain at least 3 points`:
  - Output model không hợp lệ; thử lại với ảnh rõ hơn và tương phản cao hơn.
- UI tải được nhưng phân đoạn thất bại:
  - Kiểm tra log server để xem `error_type` và stack trace từ `/api/segment`.
- `ModuleNotFoundError`:
  - Cài lại dependency trong môi trường ảo đang kích hoạt bằng `pip install -r requirements.txt`.

## 🛣️ Lộ trình

Các bước tiềm năng tiếp theo cho kho này:

1. Thêm test tự động cho kiểm tra polygon và tạo output.
2. Thêm CI (lint, type checks và smoke tests).
3. Thêm CLI chế độ batch để xử lý theo thư mục.
4. Hỗ trợ nhiều object mask hoặc output dạng instance segmentation.
5. Thêm Dockerfile và tài liệu triển khai.
6. Thêm ví dụ benchmark và sample dataset kèm output kỳ vọng.
7. Hoàn thiện các README đa ngôn ngữ trong `i18n/`.

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh.

Quy trình khuyến nghị:

1. Fork repo và tạo feature branch.
2. Thực hiện thay đổi tập trung với commit message rõ ràng.
3. Kiểm tra thủ công luồng web + CLI trên máy local.
4. Mở pull request mô tả thay đổi hành vi và bằng chứng kiểm thử.

Các hạng mục đóng góp gợi ý:
- Thiết kế prompt tốt hơn để trích xuất polygon ổn định hơn.
- Cải thiện trực quan frontend (zoom/pan, làm mượt contour).
- Bộ khung kiểm thử và sample fixture có thể tái lập.
- Cải thiện tài liệu và bản địa hóa.

<a id="support"></a>

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

<a id="license"></a>

## 📄 Giấy phép

Hiện tại kho này chưa có tệp giấy phép.

Giả định: mặc định mọi quyền đều được bảo lưu cho đến khi có giấy phép được thêm rõ ràng.

Nếu bạn dự định chia sẻ hoặc phân phối dự án này, hãy thêm tệp `LICENSE` và cập nhật mục này.
