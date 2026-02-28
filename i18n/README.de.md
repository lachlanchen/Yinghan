[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# Organoid-Segmentierung (Web + CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)
![API](https://img.shields.io/badge/API-POST%20%2Fapi%2Fsegment-0f766e)
![Format](https://img.shields.io/badge/Result-Polygon%20JSON-f59e0b)

Eine Python-Anwendung zur Segmentierung von Organoiden in Mikroskopiebildern mit OpenAI-Modellen mit Vision-Fähigkeiten.

> Für schnelle lokale Experimente ausgelegt: einmal hochladen, Overlay/Masken/JSON-Ausgaben prüfen und die Modellauswahl iterativ verbessern.

Dieses Repository enthält:
- Einen Tornado-Webserver mit Upload-UI.
- Einen CLI-Workflow für Batch- oder skriptbasierte Nutzung.
- Polygon-Extraktion, Maskengenerierung und Rendering annotierter Bilder.
- Minimale PWA-Unterstützung (Manifest + Service-Worker-Cache für zentrale statische Assets).

<a id="quick-navigation"></a>

## 🧭 Schnelle Navigation

| Abschnitt | Zweck |
|---|---|
| [Überblick](#overview) | Verstehen, was das Projekt macht und welche Ausgaben es erzeugt |
| [Funktionen](#features) | Zentrale Fähigkeiten für Web-, CLI- und API-Workflows |
| [Projektstruktur](#project-structure) | Kern-Dateien und Laufzeitverzeichnisse finden |
| [Voraussetzungen](#prerequisites) | Umgebungsanforderungen prüfen |
| [Installation](#installation) | Python-Umgebung und Abhängigkeiten einrichten |
| [Nutzung](#usage) | Web-App, CLI oder direkte API-Aufrufe ausführen |
| [Konfiguration](#configuration) | Modell- und Laufzeitparameter anpassen |
| [Beispiele](#examples) | Snippets für CLI- und Python-Workflows nutzen |
| [Entwicklungshinweise](#development-notes) | Implementierungsdetails und lokale Tipps verstehen |
| [Fehlerbehebung](#troubleshooting) | Häufige Laufzeit- und Modellprobleme lösen |
| [Roadmap](#roadmap) | Geplante nächste Verbesserungen |
| [Mitwirken](#contributing) | Änderungen effizient beitragen |
| [Support](#support) | Spendenoptionen |
| [Lizenz](#license) | Aktueller Lizenzstatus |

<a id="overview"></a>

## 🔍 Überblick

Die App akzeptiert ein Mikroskopiebild als Eingabe, sendet es mit einem strikten JSON-Schema-Prompt an ein OpenAI-Modell und liefert ein einzelnes Polygon zurück, das die Organoid-Grenze nachzeichnet.

### 🔄 End-to-End-Workflow

1. Bild über Web-Upload, CLI-Pfad oder API-Multipart-Formular empfangen.
2. OpenAI-Modell aufrufen, um strukturierte Polygon-Ausgabe zu erzeugen.
3. Polygon-Koordinaten validieren und auf Bildgrenzen begrenzen.
4. Drei Artefakte rendern und speichern: annotiertes Bild, Binärmaske, Polygon-JSON.
5. URLs/Pfade und Metadaten (`width`, `height`, `confidence`) zurückgeben.

### 📌 Auf einen Blick

| Bereich | Details |
|---|---|
| Eingabe | Mikroskopiebild |
| Kernausgabe | Organoid-Polygon (`x, y`-Punkte) |
| Abgeleitete Dateien | Annotiertes Overlay-PNG, Binärmasken-PNG, Polygon-JSON |
| Zugriffsarten | Web-UI, CLI, direkter API-Aufruf |
| Backend | Tornado (`server.py`) |
| AI-Pfad | OpenAI Responses API zuerst, Chat Completions als Fallback |

Erzeugte Artefakte:
- `*_annotated.png`: Quellbild mit halbtransparentem rotem Overlay.
- `*_mask.png`: Binärmaske des Organoids.
- `*_polygon.json`: strukturierte Ausgabe (`width`, `height`, `polygon`, `confidence`).

Primäre Laufzeitdateien:
- `server.py`: Web-App + API-Routen.
- `organoid_segmenter.py`: Segmentierungs- sowie Bild/Masken-Ausgabelogik.
- `segment_organoid.py`: CLI-Wrapper.

<a id="features"></a>

## ✨ Funktionen

- Web-UI unter `http://localhost:8888` für schnelle interaktive Segmentierung.
- REST-ähnlicher Endpunkt `POST /api/segment` mit Multipart-Upload-Unterstützung.
- Konfigurierbarer Modellname aus UI und CLI (`gpt-4o-2024-08-06` als Standard).
- Validierung und Begrenzung von Polygonpunkten auf Bildgrenzen.
- Automatische Erstellung von Ausgabeordnern (`uploads/`, `outputs/`).
- OpenAI Responses API zuerst, Chat Completions als Fallback im Codepfad.
- Service-Worker-Unterstützung zum Cachen zentraler statischer Dateien.

<a id="project-structure"></a>

## 🗂️ Projektstruktur

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

<a id="prerequisites"></a>

## ✅ Voraussetzungen

- Python 3.10+ (3.11 empfohlen).
- `pip` und Unterstützung für virtuelle Umgebungen (`venv`).
- OpenAI-API-Schlüssel mit Zugriff auf ein visionfähiges Modell.
- Netzwerkzugriff aus der Laufzeitumgebung auf OpenAI-APIs.

<a id="installation"></a>

## ⚙️ Installation

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

API-Schlüssel setzen:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

<a id="usage"></a>

## 🚀 Nutzung

### ⚡ Befehlsübersicht

| Aufgabe | Befehl |
|---|---|
| Webserver starten | `python server.py` |
| CLI-Segmentierung für einzelnes Bild ausführen | `python segment_organoid.py /path/to/image.jpg` |
| CLI mit explizitem Modell + Ausgabeverzeichnis ausführen | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| API-Endpunkt aufrufen | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Web-App starten

```bash
python server.py
```

Öffnen:

```text
http://localhost:8888
```

Web-Ablauf:
1. Bild auswählen.
2. Optional das Modell im Eingabefeld ändern.
3. Auf **Segment** klicken.
4. Overlay, annotiertes Bild und Maske prüfen.

### 🧪 CLI ausführen

```bash
python segment_organoid.py /path/to/image.jpg
```

Optionale Argumente:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

Die CLI gibt Ausgabepfade und eine Zusammenfassung mit Bilddimensionen sowie der Anzahl an Polygonpunkten aus.

### 🔌 API direkt aufrufen

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Beispielhafte Antwortstruktur:

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

## 🛠️ Konfiguration

Aktuell konfigurierbare Parameter:

| Parameter | Standard | Wo einstellen |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Webformular `model`, CLI `--model`, API-Feld `model` |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | none | Umgebungsvariable `OPENAI_API_KEY` |

Annahmen:
- Der `OpenAI()`-Client nutzt auf Umgebungsvariablen basierende Zugangsdaten.
- Es sind keine benutzerdefinierte Base-URL oder Org-/Projekt-Einstellungen erforderlich, außer Ihre Account-Konfiguration verlangt dies.

<a id="examples"></a>

## 🧾 Beispiele

### 🐍 Programmatische Python-Nutzung

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

### 📄 Polygon-JSON prüfen

```bash
cat outputs/<name>_polygon.json
```

### 🧱 Typische Ausgabedateien

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

<a id="development-notes"></a>

## 🧠 Entwicklungshinweise

- Backend-Framework: Tornado (`server.py`).
- Frontend-Stack: statisches HTML/CSS/JS (`templates/index.html`, `static/app.js`).
- Der Service Worker wird beim Seitenladen registriert und cached zentrale Assets, die in `static/sw.js` gelistet sind.
- Polygon-Validierung stellt mindestens 3 Punkte sicher und begrenzt auf Bildgrenzen.
- Die Ausgabeerzeugung nutzt Pillow (`PIL.Image`, `ImageDraw`).

Tipps für lokale Entwicklung:

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

<a id="troubleshooting"></a>

## 🩺 Fehlerbehebung

Schnelle Zuordnung:

| Symptom | Wahrscheinliche Ursache | Schneller Check |
|---|---|---|
| Authentifizierungsfehler | Fehlender/ungültiger API-Schlüssel | `echo $OPENAI_API_KEY` in aktiver Shell |
| JSON-Parse- oder Schema-Fehler | Modellausgabe fehlerhaft formatiert | Erneut versuchen oder Modell in UI/CLI wechseln |
| Weniger als 3 Polygonpunkte | Konturextraktion mit niedriger Sicherheit | Klareres Bild probieren und erneut ausführen |
| UI funktioniert, aber Segmentierung schlägt fehl | Backend-Exception während API-Aufruf | Server-Logs auf `error_type` prüfen |
| Import-/Modulfehler | Umgebungs-Mismatch | Abhängigkeiten in aktiver venv neu installieren |

- `openai.AuthenticationError` (oder ähnlich):
  - Prüfen, ob `OPENAI_API_KEY` in derselben Shell-Session gesetzt ist.
- `Model response did not contain valid JSON`:
  - Erneut versuchen oder ein anderes Modell nutzen; Fallback-Parsing existiert, aber fehlerhafte Ausgabe kann weiterhin scheitern.
- `Polygon must contain at least 3 points`:
  - Modellausgabe war ungültig; mit einem klareren, kontrastreicheren Bild erneut versuchen.
- UI lädt, aber Segmentierung schlägt fehl:
  - Server-Logs auf `error_type` und Stacktrace-Details aus `/api/segment` prüfen.
- `ModuleNotFoundError`:
  - Abhängigkeiten in der aktiven virtuellen Umgebung mit `pip install -r requirements.txt` neu installieren.

<a id="roadmap"></a>

## 🛣️ Roadmap

Mögliche nächste Schritte für dieses Repository:

1. Automatisierte Tests für Polygon-Validierung und Ausgabeerzeugung hinzufügen.
2. CI hinzufügen (Lint, Type Checks und Smoke Tests).
3. Batch-Modus-CLI für die Verarbeitung auf Verzeichnisebene hinzufügen.
4. Unterstützung für mehrere Objektmasken oder Instance-Segmentierungsausgabe hinzufügen.
5. Dockerfile und Deployment-Dokumentation hinzufügen.
6. Benchmark-Beispiele und Sample-Datensätze mit erwarteten Ausgaben hinzufügen.
7. Mehrsprachige README-Dateien unter `i18n/` finalisieren.

<a id="contributing"></a>

## 🤝 Mitwirken

Beiträge sind willkommen.

Empfohlener Workflow:

1. Repository forken und einen Feature-Branch erstellen.
2. Fokusierte Änderungen mit klaren Commit-Messages umsetzen.
3. Manuelle Web- und CLI-Flows lokal validieren.
4. Pull Request öffnen und Verhaltensänderungen sowie Testnachweise beschreiben.

Empfohlene Beitragsbereiche:
- Besseres Prompt-Design für stabilere Polygon-Extraktion.
- Verbesserte Frontend-Visualisierung (Zoom/Pan, Kontur-Glättung).
- Test-Harnesses und reproduzierbare Sample-Fixtures.
- Dokumentations- und Lokalisierungsverbesserungen.

<a id="support"></a>

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

<a id="license"></a>

## 📄 Lizenz

Derzeit ist in diesem Repository keine Lizenzdatei vorhanden.

Annahme: Ohne explizit hinzugefügte Lizenz sind standardmäßig alle Rechte vorbehalten.

Wenn Sie dieses Projekt teilen oder verteilen möchten, fügen Sie eine `LICENSE`-Datei hinzu und aktualisieren Sie diesen Abschnitt.
