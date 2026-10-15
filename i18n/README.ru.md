[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://lazying.art/media/brand/lazyingart-intro.gif)](https://lazying.art)

# Сегментация органоидов (Web + CLI)

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

Python-приложение для сегментации органоидов на микроскопических изображениях с использованием моделей OpenAI с поддержкой зрения.

> Оптимизировано для быстрых локальных экспериментов: загрузите изображение один раз, проверьте overlay/mask/JSON-результаты и подберите модель.

<a id="at-a-glance"></a>
## 📋 В одном взгляде

| Аспект | Детали |
|---|---|
| Входные данные | Микроскопические изображения (локальная загрузка, путь в CLI или multipart API) |
| Основной результат | Один полигон органоида с оценкой уверенности |
| Набор артефактов | Аннотированный PNG, бинарная маска PNG, polygon JSON |
| Интерфейсы | Web UI, CLI, REST endpoint |
| Путь ИИ | OpenAI Responses API с резервным Chat Completions |

---

<a id="execution-summary"></a>
## 🧩 Итог выполнения

| Канал | Точка входа | Лучшее применение |
|---|---|---|
| Web | `python server.py` | Быстрая визуальная проверка и донастройка |
| CLI | `python segment_organoid.py ...` | Пакетные или скриптовые запуски |
| API | `POST /api/segment` | Автоматизация и интеграция в сервисы |

---

В репозитории есть:
- Tornado-веб-сервер с UI загрузки.
- CLI-процесс для пакетного/скриптового запуска.
- Извлечение полигона, генерация маски и отрисовка аннотированного изображения.
- Минимальная поддержка PWA (manifest + кэш service worker для основных статических файлов).

<a id="project-overview"></a>
## 🧭 Быстрая навигация

| Раздел | Назначение |
|---|---|
| [Обзор](#overview) | Понимание, что делает проект и какие выводы он выдаёт |
| [Возможности](#features) | Ключевые возможности для Web, CLI и API |
| [Структура проекта](#project-structure) | Где находятся основные файлы и рабочие директории |
| [Требования](#prerequisites) | Проверка требований окружения |
| [Установка](#installation) | Подготовка Python и зависимостей |
| [Использование](#usage) | Запуск веб-приложения, CLI или прямые API-запросы |
| [Настройки](#configuration) | Корректировка параметров модели и исполнения |
| [Примеры](#examples) | Готовые фрагменты для CLI и Python |
| [Заметки по разработке](#development-notes) | Детали реализации и советы по локальной работе |
| [Устранение неполадок](#troubleshooting) | Решение типичных ошибок runtime и модели |
| [Дорожная карта](#roadmap) | Запланированные улучшения |
| [Вклад](#contributing) | Как правильно вносить изменения |
| [Поддержка](#support) | Варианты пожертвований |
| [Лицензия](#license) | Текущий статус лицензирования |

<a id="overview"></a>
## 🔍 Обзор

Приложение принимает входное микроскопическое изображение, отправляет его модели OpenAI со строгим prompt со схемой JSON и возвращает один полигон, описывающий границу органоида.

### 🔄 Полный рабочий цикл

1. Получение изображения через веб-загрузку, путь в CLI или multipart-форму API.
2. Запрос модели OpenAI для построения структурированного полигона.
3. Проверка и обрезка координат полигона в пределах изображения.
4. Рендер и сохранение трёх артефактов: аннотированного изображения, бинарной маски, polygon JSON.
5. Возврат URL/путей и метаданных (`width`, `height`, `confidence`).

### 📌 Кратко

| Область | Детали |
|---|---|
| Вход | Микроскопическое изображение |
| Основной результат | Полигон органоида (точки `x, y`) |
| Производные файлы | Аннотированный overlay PNG, бинарная mask PNG, polygon JSON |
| Режимы доступа | Web UI, CLI, прямой API-вызов |
| Backend | Tornado (`server.py`) |
| Путь ИИ | Сначала OpenAI Responses API, затем Chat Completions |

Сформированные артефакты:
- `*_annotated.png`: исходное изображение с полупрозрачным красным overlay.
- `*_mask.png`: бинарная маска органоида.
- `*_polygon.json`: структурированный вывод (`width`, `height`, `polygon`, `confidence`).

Основные файлы запуска:
- `server.py`: веб-приложение + маршруты API.
- `organoid_segmenter.py`: логика сегментации и генерации изображений/маски.
- `segment_organoid.py`: CLI-обёртка.

<a id="features"></a>
## ✨ Возможности

- Web UI по адресу `http://localhost:8888` для быстрой интерактивной сегментации.
- REST-подобный endpoint `POST /api/segment` с поддержкой multipart upload.
- Настраиваемое имя модели в UI и CLI (`gpt-4o-2024-08-06` по умолчанию).
- Проверка и обрезка точек полигона по границам изображения.
- Автоматическое создание директорий результатов (`uploads/`, `outputs/`).
- В коде сначала используется OpenAI Responses API, затем fallback на Chat Completions.
- Поддержка service worker для кэширования основных статических файлов.

<a id="project-structure"></a>
## 🗂️ Структура проекта

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
└─ .auto-readme-work/             # Context and artifacts for README generation
```

### Файлы, которые обычно редактируют

- `server.py` — обработка запросов, маршруты и формат ответа.
- `organoid_segmenter.py` — prompt, схема и рендеринг выхода.
- `templates/index.html` и `static/app.js` — поведение интерфейса.
- `segment_organoid.py` — удобство CLI и значения аргументов по умолчанию.

<a id="prerequisites"></a>
## ✅ Предварительные требования

- Python 3.10+ (рекомендуется 3.11).
- `pip` и поддержка виртуального окружения (`venv`).
- API-ключ OpenAI с доступом к модели с поддержкой vision.
- Сетевой доступ из среды выполнения к API OpenAI.

<a id="installation"></a>
## ⚙️ Установка

```bash
# 1) Clone and enter the repository
git clone <your-repo-url>
cd Yinghan

# 2) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt
```

Установите API-ключ в текущей оболочке:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

Предположение: загрузчик `.env` не поставляется, поэтому настройка переменной окружения обязательна.

<a id="usage"></a>
## 🚀 Использование

### ⚡ Шпаргалка по командам

| Задача | Команда |
|---|---|
| Запустить веб-сервер | `python server.py` |
| Запустить сегментацию одного изображения в CLI | `python segment_organoid.py /path/to/image.jpg` |
| Запустить CLI с явной моделью и директорией вывода | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| Вызвать API endpoint | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Запуск веб-приложения

```bash
python server.py
```

Откройте:

```text
http://localhost:8888
```

Веб-поток:
1. Выберите изображение.
2. По желанию измените модель в поле ввода.
3. Нажмите **Segment**.
4. Проверьте overlay, аннотированное изображение и маску.

### 🧪 Запуск CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

Необязательные аргументы:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI выводит пути к артефактам и сводную информацию с размерами изображения и числом точек полигона.

### 🔌 Прямой вызов API

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Пример формы ответа:

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
## 🛠️ Конфигурация

Текущие настраиваемые параметры:

| Параметр | Значение по умолчанию | Где настраивается |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Поле web `model`, CLI `--model`, поле API `model` |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | отсутствует | Переменная окружения `OPENAI_API_KEY` |

Предположения:
- Клиент `OpenAI()` использует учётные данные из окружения.
- Пользовательские настройки base URL или org/project не нужны, если только они не требуются вашей конфигурацией аккаунта.

<a id="examples"></a>
## 🧾 Примеры

### 🐍 Программное использование на Python

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

### 📄 Просмотр polygon JSON

```bash
cat outputs/<name>_polygon.json
```

### 🧱 Пример типичных выходных файлов

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

<a id="development-notes"></a>
## 🧠 Заметки по разработке

- Backend framework: Tornado (`server.py`).
- Frontend stack: static HTML/CSS/JS (`templates/index.html`, `static/app.js`).
- Service worker регистрируется при загрузке страницы и кэширует базовые assets из `static/sw.js`.
- Проверка полигона гарантирует минимум 3 точки и ограничение их координат изображением.
- Генерация выходных данных использует Pillow (`PIL.Image`, `ImageDraw`).

Советы по локальной разработке:

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

<a id="troubleshooting"></a>
## 🩺 Устранение неполадок

Краткая диагностика:

| Симптом | Возможная причина | Быстрая проверка |
|---|---|---|
| Ошибка аутентификации | Отсутствует/неверный API key | `echo $OPENAI_API_KEY` в активной оболочке |
| Ошибка разбора JSON или схемы | Модель вернула некорректный JSON | Повторите попытку или смените модель в UI/CLI |
| Меньше 3 точек в полигоне | Низкая уверенность при выделении контура | Возьмите более чёткое изображение и запустите повторно |
| Web доступен, но сегментация падает | Исключение в backend во время API-вызова | Проверьте server logs на `error_type` |
| Ошибка импорта/модуля | Несовпадение окружения | Переустановите зависимости в активном `venv` |

- `openai.AuthenticationError` (или аналогичная):
  - Проверьте, что `OPENAI_API_KEY` задан в той же сессии shell.
- `Model response did not contain valid JSON`:
  - Повторите попытку или используйте другую модель; есть fallback-парсинг, но некорректный вывод может всё равно приводить к ошибке.
- `Polygon must contain at least 3 points`:
  - Вывод модели некорректен; повторите с более контрастным изображением.
- UI загружается, но сегментация не работает:
  - Проверьте server logs на `error_type` и трассировку стека по `/api/segment`.
- `ModuleNotFoundError`:
  - Переустановите зависимости в активном окружении через `pip install -r requirements.txt`.

<a id="roadmap"></a>
## 🛣️ Дорожная карта

Потенциальные следующие шаги для этого репозитория:

1. Добавить автоматические тесты для валидации полигона и генерации выходных данных.
2. Добавить CI (lint, проверка типов, smoke-тесты).
3. Добавить пакетный режим CLI для обработки директорий.
4. Поддержать несколько масок объектов или instance segmentation.
5. Добавить Dockerfile и документацию по деплою.
6. Добавить эталоны и примеры датасетов с ожидаемыми результатами.
7. Завершить многоязычные README-файлы в `i18n/`.

<a id="contributing"></a>
## 🤝 Участие в разработке

Вклады приветствуются.

Рекомендуемый workflow:

1. Сделайте форк репозитория и создайте feature-ветку.
2. Делайте целевые изменения с понятными сообщениями коммитов.
3. Локально проверяйте web + CLI сценарии вручную.
4. Откройте pull request с описанием изменений поведения и подтверждением тестирования.

Предлагаемые направления для вклада:
- Улучшение prompt для более стабильного выделения полигона.
- Улучшение визуализации фронтенда (zoom/pan, сглаживание контуров).
- Harness для тестов и воспроизводимые sample-fixtures.
- Улучшение документации и локализации.

<a id="support"></a>

## 📄 Лицензия

В этом репозитории сейчас отсутствует файл лицензии.

Предположение: все права считаются защищёнными, пока лицензия явно не добавлена.

Если вы планируете делиться или распространять проект, добавьте файл `LICENSE` и обновите этот раздел.


## ❤️ Support

<!-- support:start -->
[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-EA4AAA?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)
[![LazyingArt Support](https://img.shields.io/badge/LazyingArt-Support-0EA5E9?style=for-the-badge)](https://chat.lazying.art/donate)
[![PayPal Support](https://img.shields.io/badge/PayPal-Support-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen)
[![Stripe Support](https://img.shields.io/badge/Stripe-Support-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400)
<!-- support:end -->
