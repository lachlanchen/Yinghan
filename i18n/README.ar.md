[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://lazying.art)

# تجزئة العضيات (ويب + سطر الأوامر)

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

تطبيق بايثون لتجزئة العضيات في صور المجهر باستخدام نماذج OpenAI القادرة على الرؤية.

> مصمم للتجارب المحلية السريعة: ارفع الصورة مرة واحدة، راجع مخرجات التراكب/القناع/JSON، وكرر اختيار النموذج حسب الحاجة.

## 📋 ملخص سريع

| الجانب | التفاصيل |
|---|---|
| الإدخال | صور المجهر (رفع محلي، مسار CLI، أو multipart عبر API) |
| الإخراج الأساسي | مضلع واحد للعضية مع درجة ثقة |
| مجموعة المخرجات | صورة PNG موسومة، PNG للقناع الثنائي، JSON المضلع |
| الواجهات | واجهة الويب، سطر الأوامر، نقطة نهاية REST |
| مسار الذكاء الاصطناعي | OpenAI Responses API مع fallback لــ Chat Completions |

---

## 🧩 ملخص التنفيذ

| القناة | نقطة الدخول | الاستخدام الأمثل |
|---|---|---|
| الويب | `python server.py` | التحقق البصري السريع والتعديلات |
| سطر الأوامر | `python segment_organoid.py ...` | تشغيلات قابلة للتنفيذ أو الدُفعات |
| API | `POST /api/segment` | الأتمتة وتكامل الخدمات |

---

يتضمن هذا المستودع:
- خادم ويب مبني على Tornado مع واجهة رفع الملفات.
- سير عمل CLI للاستخدام التلقائي أو على دفعات.
- استخراج المضلع، توليد القناع، وعرض الصورة المعلّمة.
- دعم PWA محدود (manifest + cache في service worker للأصول الثابتة الأساسية).

## 🧭 التنقل السريع

| القسم | الغرض |
|---|---|
| [نظرة عامة](#overview) | فهم ما يقوم به المشروع ونوع المخرجات |
| [الميزات](#features) | عرض القدرات الأساسية في مسارات الويب وCLI وAPI |
| [هيكل المشروع](#project-structure) | تحديد ملفات التشغيل والمجلدات الأساسية |
| [المتطلبات المسبقة](#prerequisites) | التحقق من متطلبات البيئة |
| [التثبيت](#installation) | إعداد بيئة بايثون والتبعيات |
| [طريقة الاستخدام](#usage) | تشغيل واجهة الويب، أو CLI، أو استدعاءات API المباشرة |
| [الإعدادات](#configuration) | ضبط النموذج ومعلمات التشغيل |
| [الأمثلة](#examples) | إعادة استخدام المقاطع لأساليب CLI وPython |
| [ملاحظات التطوير](#development-notes) | فهم تفاصيل التنفيذ ونصائح العمل المحلي |
| [استكشاف الأخطاء](#troubleshooting) | حل مشكلات التشغيل الشائعة ومشكلات النموذج |
| [خريطة الطريق](#roadmap) | التحسينات القادمة |
| [المساهمة](#contributing) | إرسال تغييرات بشكل فعّال |
| [الدعم](#support) | خيارات التبرع |
| [الترخيص](#license) | حالة الترخيص الحالي |

<a id="overview"></a>
## 🔍 نظرة عامة

يقبل التطبيق صورة مجهرية، ويُرسلها إلى نموذج OpenAI باستخدام قالب JSON صارم، ثم يعيد مضلعًا واحدًا يتبع حدود العضية.

### 🔄 سير العمل من البداية إلى النهاية

1. استلام الصورة عبر رفع الويب أو مسار CLI أو نموذج multipart عبر API.
2. تشغيل نموذج OpenAI لإنتاج مخرجات مضلع منظمة.
3. التحقق من صحة نقاط المضلع وتثبيتها داخل حدود الصورة.
4. عرض وحفظ ثلاثة مخرجات: صورة موسومة، قناع ثنائي، JSON المضلع.
5. إرجاع الروابط/المسارات والبيانات الوصفية (`width`, `height`, `confidence`).

### 📌 نظرة إجمالية

| المجال | التفاصيل |
|---|---|
| الإدخال | صورة مجهرية |
| الإخراج الأساسي | مضلع العضية (`x, y` points) |
| الملفات المشتقة | PNG للتراكب المعلَّم، PNG للقناع الثنائي، JSON المضلع |
| أوضاع الوصول | واجهة الويب، CLI، استدعاء API مباشر |
| الواجهة الخلفية | Tornado (`server.py`) |
| مسار الذكاء الاصطناعي | OpenAI Responses API أولًا، fallback لـ Chat Completions |

المخرجات المولدة:
- `*_annotated.png`: الصورة الأصلية مع تراكب أحمر نصف شفاف.
- `*_mask.png`: قناع العضية الثنائي.
- `*_polygon.json`: مخرج منظم (`width`, `height`, `polygon`, `confidence`).

ملفات التشغيل الأساسية:
- `server.py`: تطبيق الويب + مسارات API.
- `organoid_segmenter.py`: منطق التجزئة ومنطق إخراج الصور/الأقنعة.
- `segment_organoid.py`: غلاف CLI.

<a id="features"></a>
## ✨ الميزات

- واجهة ويب على `http://localhost:8888` للتجزئة التفاعلية السريعة.
- نقطة نهاية على نمط REST `POST /api/segment` مع دعم رفع multipart.
- اسم نموذج قابل للتكوين من الواجهة وCLI (`gpt-4o-2024-08-06` افتراضيًا).
- التحقق من نقاط المضلع وتثبيتها داخل حدود الصورة.
- إنشاء أدلة الإخراج تلقائيًا (`uploads/`, `outputs/`).
- OpenAI Responses API أولًا، وChat Completions كبديل في مسار الكود.
- دعم Service Worker لتخزين الملفات الثابتة الأساسية.

<a id="project-structure"></a>
## 🗂️ هيكل المشروع

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

### الملفات التي عادةً ما يتم تعديلها

- `server.py` لمعالجة الطلبات والتوجيه وتنسيق الاستجابة.
- `organoid_segmenter.py` لقالب النموذج، المخطط، وعرض المخرجات.
- `templates/index.html` / `static/app.js` لسلوك واجهة المستخدم.
- `segment_organoid.py` لراحة استخدام CLI وقيم الخيارات الافتراضية.

<a id="prerequisites"></a>
## ✅ المتطلبات المسبقة

- Python 3.10+ (موصى به 3.11).
- دعم `pip` وبيئات افتراضية (`venv`).
- مفتاح واجهة OpenAI API مع وصول إلى نموذج قادر على الرؤية.
- وصول شبكي من بيئة التشغيل إلى واجهات OpenAI.

<a id="installation"></a>
## ⚙️ التثبيت

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

اضبط مفتاح API في الجلسة النشطة:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

الافتراض: لا يوجد loader خاص بـ `.env` مضمّن، لذلك يلزم إعداد متغير البيئة.

<a id="usage"></a>
## 🚀 طريقة الاستخدام

### ⚡ ملخص الأوامر

| المهمة | الأمر |
|---|---|
| تشغيل خادم الويب | `python server.py` |
| تنفيذ تجزئة صورة واحدة عبر CLI | `python segment_organoid.py /path/to/image.jpg` |
| تشغيل CLI مع نموذج ومسار إخراج صريحين | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| استدعاء نقطة النهاية API | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 تشغيل تطبيق الويب

```bash
python server.py
```

افتح:

```text
http://localhost:8888
```

تدفق الويب:
1. اختر صورة.
2. غير النموذج اختياريًا من حقل الإدخال.
3. انقر على **Segment**.
4. راجع التراكب والصورة الموصوفة والقناع.

### 🧪 تشغيل CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

الوسيطات الاختيارية:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

يطبع CLI مسارات الإخراج وملخصًا يتضمن أبعاد الصورة وعدد نقاط المضلع.

### 🔌 استدعاء API مباشرة

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

شكل الاستجابة النموذجي:

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
## 🛠️ الإعدادات

المعايير القابلة للتكوين حاليًا:

| المعامل | القيمة الافتراضية | مكان الإعداد |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | حقل النموذج في الويب، CLI `--model`، حقل API `model` |
| `out_dir` | `outputs` | CLI `--out-dir` |
| مفتاح API | لا شيء | متغير البيئة `OPENAI_API_KEY` |

الافتراضات:
- عميل `OpenAI()` يستخدم بيانات اعتماد مبنية على البيئة.
- لا يلزم رابط قاعدة مخصص أو إعدادات org/project ما لم تتطلب إعدادات حسابك ذلك.

<a id="examples"></a>
## 🧾 أمثلة

### 🐍 استخدام Python برمجيًا

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

### 📄 فحص JSON المضلع

```bash
cat outputs/<name>_polygon.json
```

### 🧱 ملفات الإخراج النموذجية

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

<a id="development-notes"></a>
## 🧠 ملاحظات التطوير

- إطار العمل الخلفي: Tornado (`server.py`).
- واجهة أمامية ثابتة: HTML/CSS/JS (`templates/index.html`, `static/app.js`).
- يسجّل Service Worker عند تحميل الصفحة ويخزن الأصول الأساسية المذكورة في `static/sw.js`.
- التحقق من المضلع يضمن وجود 3 نقاط على الأقل ويثبتها ضمن حدود الصورة.
- توليد المخرجات يستخدم Pillow (`PIL.Image`, `ImageDraw`).

نصائح تطوير محلي:

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

<a id="troubleshooting"></a>
## 🩺 استكشاف الأخطاء

تطابق سريع:

| العرض | السبب المرجّح | فحص سريع |
|---|---|---|
| خطأ في المصادقة | مفتاح API مفقود/غير صحيح | تنفيذ `echo $OPENAI_API_KEY` في نفس الجلسة النشطة |
| خطأ في تحليل JSON أو المخطط | خرج النموذج بتنسيق خاطئ | أعد المحاولة، أو بدّل النموذج في الواجهة/CLI |
| أقل من 3 نقاط للمضلع | انخفاض ثقة استخراج الحد | جرّب صورة أوضح ثم أعد التشغيل |
| الواجهة تعمل لكن التجزئة تفشل | استثناء في الخلفية أثناء استدعاء API | افحص سجلات الخادم للبحث عن `error_type` |
| خطأ import/module | عدم تطابق البيئة | أعد تثبيت التبعيات داخل venv النشط |

- `openai.AuthenticationError` (أو مشابه):
  - تحقق من ضبط `OPENAI_API_KEY` في نفس جلسة التشغيل.
- `Model response did not contain valid JSON`:
  - أعد المحاولة أو استخدم نموذجًا مختلفًا؛ يوجد parsing احتياطي لكن إخراجًا غير صحيح قد يفشل.
- `Polygon must contain at least 3 points`:
  - خرج النموذج غير صالح؛ أعد المحاولة بصورة أوضح وأكثر تباينًا.
- UI loads but segmentation fails:
  - تحقق من سجلات الخادم لـ `error_type` وتفاصيل stack trace من `/api/segment`.
- `ModuleNotFoundError`:
  - أعد تثبيت المتطلبات داخل البيئة الافتراضية النشطة باستخدام `pip install -r requirements.txt`.

<a id="roadmap"></a>
## 🛣️ خريطة الطريق

خطوات مستقبلية محتملة لهذا المستودع:

1. إضافة اختبارات آلية للتحقق من المضلع وتوليد المخرجات.
2. إضافة CI (تحليل ثابت، تحقق نوعي، واختبارات smoke).
3. إضافة وضع CLI دفعي لمعالجة مجلد كامل.
4. دعم أكثر من قناع/مستخرج instances متعددة في نفس الصورة.
5. إضافة Dockerfile وتوثيق النشر.
6. إضافة أمثلة معيارية ومجموعات بيانات نموذجة مع المخرجات المتوقعة.
7. إكمال ملفات README متعددة اللغات داخل `i18n/`.

<a id="contributing"></a>
## 🤝 المساهمة

المساهمات مرحب بها.

المسار المقترح:

1. اعمل fork للمستودع وأنشئ فرع ميزة.
2. اجعل التغييرات مركزة برسائل commit واضحة.
3. تحقق يدويًا من مسارات الويب وCLI محليًا.
4. افتح طلب دمج يصف تغييرات السلوك وأدلة الاختبار.

المجالات المقترحة للمساهمة:
- تصميم prompt أفضل لتثبيت استخراج المضلع.
- تحسين عرض الواجهة الأمامية (zoom/pan، تنعيم الحواف).
- أدوات اختبارات وبيانات نمطية قابلة لإعادة التشغيل.
- تحسينات الوثائق والتوطين.

<a id="support"></a>
## 📄 الترخيص

لا يوجد ملف ترخيص في هذا المستودع حاليًا.

الافتراض: جميع الحقوق محفوظة افتراضًا حتى تتم إضافة ترخيص صريح.

إذا كنت تنوي مشاركة هذا المشروع أو توزيعه، أضف ملف `LICENSE` وحدث هذا القسم.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
