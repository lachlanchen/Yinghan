[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://lazying.art/media/brand/lazyingart-intro.gif)](https://lazying.art)

# Organoid-Segmentierung (Web + CLI)

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

Eine Python-Anwendung zur Segmentierung von Organoiden in Mikroskopie-Bildern mit vision-fähigen OpenAI-Modellen.

> Für schnelle lokale Experimente optimiert: Bild einmal hochladen, Overlay-/Mask-/JSON-Ausgaben prüfen und die Modellwahl iterieren.

## 📋 Kurzüberblick

| Aspekt | Details |
|---|---|
| Eingabe | Mikroskopie-Bilder (lokaler Upload, CLI-Pfad oder API-Multipart) |
| Kernausgabe | Ein Organoid-Polygon mit Konfidenzwert |
| Artefaktsatz | Annotiertes PNG, binäres Masken-PNG, Polygon-JSON |
| Schnittstellen | Web-UI, CLI, REST-Endpunkt |
| KI-Pfad | OpenAI Responses API mit Chat Completions-Fallback |

---

## 🧩 Ausführungsübersicht

| Kanal | Einstiegspunkt | Beste Verwendung |
|---|---|---|
| Web | `python server.py` | Schnelle visuelle Prüfung und Anpassung |
| CLI | `python segment_organoid.py ...` | Skript- oder batchfähige Ausführungen |
| API | `POST /api/segment` | Automatisierung und Service-Integration |

---

Dieses Repository enthält:
- Einen Tornado-Webserver mit Upload-UI.
- Einen CLI-Workflow für Batch- oder Skriptbetrieb.
- Polygon-Extraktion, Maskenerstellung und Rendern von annotierten Bildern.
- Minimale PWA-Unterstützung (Manifest + Service-Worker-Cache für zentrale statische Assets).

## 🧭 Schnellnavigation

| Bereich | Zweck |
|---|---|
| [Überblick](#overview) | Verstehen, was das Projekt tut und welche Ausgaben es erzeugt |
| [Funktionen](#features) | Zentrale Fähigkeiten in Web-, CLI- und API-Flows sehen |
| [Projektstruktur](#project-structure) | Wichtige Dateien und Laufzeitverzeichnisse finden |
| [Voraussetzungen](#prerequisites) | Umgebungsvoraussetzungen prüfen |
| [Installation](#installation) | Python-Umgebung und Abhängigkeiten einrichten |
| [Nutzung](#usage) | Web-App, CLI oder direkte API-Aufrufe ausführen |
| [Konfiguration](#configuration) | Modell- und Laufzeitparameter anpassen |
| [Beispiele](#examples) | Beispielsnippets für CLI- und Python-Workflows wiederverwenden |
| [Entwicklungshinweise](#development-notes) | Implementierungsdetails und lokale Tipps verstehen |
| [Fehlerbehebung](#troubleshooting) | Häufige Laufzeit- und Modellprobleme lösen |
| [Roadmap](#roadmap) | Geplante nächste Verbesserungen |
| [Mitwirken](#contributing) | Änderungen effektiv einreichen |
| [Support](#support) | Spendenoptionen |
| [Lizenz](#license) | Aktueller Lizenzstatus |

<a id="overview"></a>
## 🔍 Überblick

Die App akzeptiert ein Mikroskopie-Eingabebild, sendet es an ein OpenAI-Modell mit einem strikten JSON-Schema-Prompt und gibt genau ein Polygon zurück, das den Organoid-Rand nachzeichnet.

### 🔄 End-to-End-Workflow

1. Bild über Web-Upload, CLI-Pfad oder API-Multipart-Form empfangen.
2. OpenAI-Modell aufrufen, um strukturierte Polygon-Ausgabe zu erzeugen.
3. Polygon-Koordinaten validieren und auf Bildgrenzen begrenzen.
4. Drei Artefakte speichern: annotiertes Bild, binäre Maske, Polygon-JSON.
5. URLs/Pfade und Metadaten (`width`, `height`, `confidence`) zurückgeben.

### 📌 Kurz auf einen Blick

| Bereich | Details |
|---|---|
| Eingabe | Mikroskopie-Bild |
| Kernausgabe | Organoid-Polygon (`x`, `y`-Punkte) |
| Abgeleitete Dateien | Annotiertes Overlay-PNG, binäres Masken-PNG, Polygon-JSON |
| Zugriffsmodi | Web-UI, CLI, direkter API-Aufruf |
| Backend | Tornado (`server.py`) |
| KI-Pfad | OpenAI Responses API zuerst, Chat Completions-Fallback |

Erzeugte Artefakte:
- `*_annotated.png`: Quellbild mit halbtransparentem roten Overlay.
- `*_mask.png`: binäre Organoid-Maske.
- `*_polygon.json`: strukturierte Ausgabe (`width`, `height`, `polygon`, `confidence`).

Primäre Laufzeitdateien:
- `server.py`: Web-App + API-Routen.
- `organoid_segmenter.py`: Segmentierungs- und Bild-/Masken-Rendering-Logik.
- `segment_organoid.py`: CLI-Wrapper.

<a id="features"></a>
## ✨ Funktionen

- Web-UI unter `http://localhost:8888` für interaktive Segmentierung.
- REST-ähnlicher Endpunkt `POST /api/segment` mit Unterstützung für Multipart-Uploads.
- Konfigurierbarer Modellname in UI und CLI (`gpt-4o-2024-08-06` standardmäßig).
- Validierung und Begrenzung von Polygonpunkten auf Bildgrenzen.
- Automatische Erstellung von Ausgabeordnern (`uploads/`, `outputs/`).
- OpenAI Responses API zuerst, Chat Completions-Fallback im Codepfad.
- Service-Worker-Unterstützung zum Caching zentraler statischer Dateien.

<a id="project-structure"></a>
## 🗂️ Projektstruktur

```text
Yinghan/
├─ organoid_segmenter.py          # Kernlogik der Segmentierung und Ausgabeerzeugung
├─ segment_organoid.py            # CLI-Einstiegspunkt
├─ server.py                      # Tornado-Server + API
├─ requirements.txt               # Python-Abhängigkeiten
├─ templates/
│  └─ index.html                  # Shell der Web-UI
├─ static/
│  ├─ app.js                      # Frontend-Upload + Ergebnis-Rendering
│  ├─ styles.css                  # UI-Styles
│  ├─ manifest.json               # PWA-Manifest
│  └─ sw.js                       # Service-Worker-Cache-Logik
├─ i18n/                          # Lokalisierte README-Dateien
├─ uploads/                       # Laufzeit-Upload-Speicher (gitignored)
├─ outputs/                       # Laufzeit-Ausgaben der Segmentierung (gitignored, zur Laufzeit erstellt)
└─ .auto-readme-work/             # Kontext-/Artefakte für README-Generierung
```

### Dateien, die typischerweise geändert werden

- `server.py` für Request-Handling, Routing und Antwortformat.
- `organoid_segmenter.py` für Prompt, Schema und Ausgabe-Rendering.
- `templates/index.html` / `static/app.js` für UI-Verhalten.
- `segment_organoid.py` für CLI-Ergonomie und Standardargumente.

<a id="prerequisites"></a>
## ✅ Voraussetzungen

- Python 3.10+ (3.11 empfohlen).
- `pip` und Unterstützung für virtuelle Umgebungen (`venv`).
- OpenAI-API-Schlüssel mit Zugriff auf ein vision-fähiges Modell.
- Netzwerkanbindung zur OpenAI-API aus der Laufzeitumgebung.

<a id="installation"></a>
## ⚙️ Installation

```bash
# 1) Repository klonen und betreten
git clone <your-repo-url>
cd Yinghan

# 2) Virtuelle Umgebung anlegen und aktivieren
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 3) Abhängigkeiten installieren
pip install -r requirements.txt
```

Setzen Sie Ihren API-Schlüssel in der aktiven Shell:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

Annahme: Es wird kein `.env`-Lader mitgeliefert, daher ist die Umgebungsvariable erforderlich.

<a id="usage"></a>
## 🚀 Nutzung

### ⚡ Befehls-Übersicht

| Aufgabe | Befehl |
|---|---|
| Webserver starten | `python server.py` |
| CLI-Segmentierung einzelner Bilder | `python segment_organoid.py /path/to/image.jpg` |
| CLI mit explizitem Modell + Ausgabeordner | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
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
2. Optional Modell im Eingabefeld ändern.
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

Die CLI gibt Ausgabewege und eine Zusammenfassung mit Bildabmessungen und Anzahl der Polygonpunkte aus.

### 🔌 API direkt aufrufen

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Beispielantwort:

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

| Parameter | Standard | Wo festlegen |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Web-Formular `model`, CLI `--model`, API-Feld `model` |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API-Schlüssel | kein | Umgebungsvariable `OPENAI_API_KEY` |

Annahmen:
- `OpenAI()`-Client nutzt credentials aus der Umgebung.
- Keine eigenen Base-URL- oder Organisations-/Projekt-Einstellungen sind erforderlich, außer wenn Ihr Konto dies verlangt.

<a id="examples"></a>
## 🧾 Beispiele

### 🐍 Programmgesteuerte Python-Nutzung

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
- Der Service Worker registriert beim Laden der Seite und cached Kern-Assets aus `static/sw.js`.
- Polygon-Validierung stellt mindestens 3 Punkte sicher und begrenzt Koordinaten auf Bildgrenzen.
- Ausgabegenerierung nutzt Pillow (`PIL.Image`, `ImageDraw`).

Tipps für die lokale Entwicklung:

```bash
# Server starten
python server.py

# CLI mit dem enthaltenen Beispielbild ausführen
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

<a id="troubleshooting"></a>
## 🩺 Fehlerbehebung

Schnelle Zuordnung:

| Symptom | Wahrscheinliche Ursache | Schneller Check |
|---|---|---|
| Authentifizierungsfehler | Fehlender/ungültiger API-Schlüssel | `echo $OPENAI_API_KEY` in der aktiven Shell |
| JSON-Parsing- oder Schema-Fehler | Modellausgabe ist fehlerhaft | Erneut versuchen oder Modell in UI/CLI wechseln |
| Weniger als 3 Polygonpunkte | Niedrige Kontur-Qualität bei der Extraktion | Verwenden Sie ein klareres Bild und wiederholen Sie den Lauf |
| UI funktioniert, Segmentierung schlägt fehl | Backend-Exception während API-Aufruf | Server-Logs nach `error_type` prüfen |
| Import-/Modulfehler | Versionskonflikt in Umgebung | Abhängigkeiten in aktivem Venv neu installieren |

- `openai.AuthenticationError` (oder ähnlich):
  - Prüfen Sie, dass `OPENAI_API_KEY` in derselben Shell-Sitzung gesetzt ist.
- `Model response did not contain valid JSON`:
  - Wiederholen Sie den Versuch oder wechseln Sie zu einem anderen Modell; Fallback-Parsing ist vorhanden, aber fehlerhafte Ausgaben können weiterhin scheitern.
- `Polygon must contain at least 3 points`:
  - Die Modellausgabe war ungültig; erneut mit kontrastreicherem, klarerem Bild versuchen.
- UI lädt, aber Segmentierung schlägt fehl:
  - Server-Logs auf `error_type` und Stacktrace-Details unter `/api/segment` prüfen.
- `ModuleNotFoundError`:
  - Abhängigkeiten im aktiven virtuellen Umfeld mit `pip install -r requirements.txt` neu installieren.

<a id="roadmap"></a>
## 🛣️ Roadmap

Mögliche nächste Schritte für dieses Repository:

1. Automatisierte Tests für Polygon-Validierung und Ausgabeerzeugung ergänzen.
2. CI hinzufügen (Lint, Typprüfungen, Smoke Tests).
3. Batch-Modus für CLI auf Verzeichnisebene hinzufügen.
4. Mehrere Objektmasken oder Instanzsegmentierung unterstützen.
5. Dockerfile und Deployment-Dokumentation ergänzen.
6. Benchmark-Beispiele und Beispieldatensätze mit erwarteten Ausgaben ergänzen.
7. Multilinguale README-Dateien unter `i18n/` finalisieren.

<a id="contributing"></a>
## 🤝 Mitwirken

Beiträge sind willkommen.

Empfohlener Ablauf:

1. Repository forken und einen Feature-Branch erstellen.
2. Gezielte Änderungen mit klaren Commit-Messages vornehmen.
3. Web- und CLI-Flows lokal manuell validieren.
4. Einen Pull Request mit Verhaltensänderungen und Testnachweis erstellen.

Empfohlene Bereiche für Beiträge:
- Besseres Prompt-Design für stabilere Polygon-Extraktion.
- Verbesserte Frontend-Visualisierung (Zoom/Pan, Konturschärfung).
- Test-Harnesses und reproduzierbare Beispiel-Fixtures.
- Dokumentation und Lokalisierung verbessern.

<a id="support"></a>
## 📄 Lizenz

Aktuell ist in diesem Repository keine Lizenzdatei vorhanden.

Annahme: Alle Rechte bleiben bis zum expliziten Hinzufügen einer Lizenz standardmäßig vorbehalten.

Wenn Sie dieses Projekt teilen oder verteilen möchten, fügen Sie eine Datei `LICENSE` hinzu und aktualisieren Sie diesen Abschnitt.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
