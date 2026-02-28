[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# Organoid-Segmentierung (Web + CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)

Eine Python-Anwendung zur Segmentierung von Organoiden in Mikroskopiebildern mit OpenAI-Modellen, die Bildverarbeitung unterstützen.

Dieses Repository enthält:
- Einen Tornado-Webserver mit Upload-UI.
- Einen CLI-Workflow für Batch- oder skriptbasierte Nutzung.
- Polygon-Extraktion, Maskenerzeugung und Rendering annotierter Bilder.
- Minimale PWA-Unterstützung (Manifest + Service-Worker-Cache für zentrale statische Assets).

## 🔍 Überblick

Die Anwendung nimmt ein Mikroskopiebild als Eingabe, sendet es mit einem Prompt mit strengem JSON-Schema an ein OpenAI-Modell und gibt ein einzelnes Polygon zurück, das die Organoid-Grenze nachzeichnet.

### 📌 Auf Einen Blick

| Bereich | Details |
|---|---|
| Eingabe | Mikroskopiebild |
| Kernausgabe | Organoid-Polygon (`x, y`-Punkte) |
| Abgeleitete Dateien | Annotiertes Overlay-PNG, binäres Masken-PNG, Polygon-JSON |
| Zugriffsmodi | Web-UI, CLI, direkter API-Aufruf |
| Backend | Tornado (`server.py`) |
| AI path | OpenAI Responses API zuerst, Chat Completions als Fallback |

Erzeugte Artefakte:
- `*_annotated.png`: Quellbild mit halbtransparentem rotem Overlay.
- `*_mask.png`: Binäre Organoid-Maske.
- `*_polygon.json`: Strukturierte Ausgabe (`width`, `height`, `polygon`, `confidence`).

Primäre Laufzeitdateien:
- `server.py`: Web-App + API-Routen.
- `organoid_segmenter.py`: Segmentierungslogik sowie Bild-/Maskenausgabe.
- `segment_organoid.py`: CLI-Wrapper.

## ✨ Funktionen

- Web-UI unter `http://localhost:8888` für schnelle interaktive Segmentierung.
- REST-ähnlicher Endpoint `POST /api/segment` mit Multipart-Upload-Unterstützung.
- Konfigurierbarer Modellname aus UI und CLI (`gpt-4o-2024-08-06` standardmäßig).
- Validierung und Begrenzung der Polygonpunkte auf Bildgrenzen.
- Automatische Erstellung von Ausgabeverzeichnissen (`uploads/`, `outputs/`).
- OpenAI Responses API zuerst, Chat Completions als Fallback im Codepfad.
- Service-Worker-Unterstützung zum Cachen zentraler statischer Dateien.

## 🗂️ Projektstruktur

```text
Yinghan/
├─ organoid_segmenter.py          # Kernlogik für Segmentierung und Ausgaberendering
├─ segment_organoid.py            # CLI-Einstiegspunkt
├─ server.py                      # Tornado-Server + API
├─ requirements.txt               # Python-Abhängigkeiten
├─ templates/
│  └─ index.html                  # Web-UI-Shell
├─ static/
│  ├─ app.js                      # Frontend-Logik für Upload + Ergebnisdarstellung
│  ├─ styles.css                  # UI-Stile
│  ├─ manifest.json               # PWA-Manifest
│  └─ sw.js                       # Service-Worker-Cache-Logik
├─ i18n/                          # Lokalisierte README-Dateien (geplant/durch Pipeline generiert)
├─ uploads/                       # Laufzeit-Upload-Speicher (gitignored)
├─ outputs/                       # Laufzeit-Segmentierungsausgaben (gitignored, zur Laufzeit erstellt)
└─ .auto-readme-work/             # Kontext/Artefakte der README-Generierungs-Pipeline
```

## ✅ Voraussetzungen

- Python 3.10+ (3.x erforderlich; 3.11 empfohlen).
- OpenAI-API-Schlüssel mit Zugriff auf ein bildfähiges Modell.
- Netzwerkzugriff von der Laufzeitumgebung auf OpenAI-APIs.

## ⚙️ Installation

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

Setze deinen API-Schlüssel:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

## 🚀 Verwendung

### 🌐 Web-App Starten

```bash
python server.py
```

Öffne:

```text
http://localhost:8888
```

Web-Ablauf:
1. Bild auswählen.
2. Optional das Modell im Eingabefeld ändern.
3. Auf **Segment** klicken.
4. Overlay, annotiertes Bild und Maske prüfen.

### 🧪 CLI Ausführen

```bash
python segment_organoid.py /path/to/image.jpg
```

Optionale Argumente:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

Die CLI gibt Ausgabepfade und eine Zusammenfassung mit Bilddimensionen sowie der Anzahl der Polygonpunkte aus.

### 🔌 API Direkt Aufrufen

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Beispielhafte Response-Struktur:

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

## 🛠️ Konfiguration

Derzeit aus dem Code konfigurierbare Parameter:

- `model`:
  - Standard: `gpt-4o-2024-08-06`
  - Setzbar über Webformular-Eingabe oder CLI `--model`
- `out_dir`:
  - CLI-Option `--out-dir` (Standard `outputs`)
  - Server verwendet intern `outputs/`

Umgebungsvariablen:
- `OPENAI_API_KEY` (erforderlich).

Annahmen:
- Der `OpenAI()`-Client verwendet umgebungsbasierte Zugangsdaten.
- Keine benutzerdefinierte Base-URL oder Org-/Projekt-Einstellungen erforderlich, außer deine OpenAI-Kontoeinrichtung verlangt sie.

## 🧾 Beispiele

### 🐍 Programmatische Python-Verwendung

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

### 📄 Polygon-JSON Prüfen

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

## 🧠 Entwicklungshinweise

- Backend-Framework: Tornado (`server.py`).
- Frontend-Stack: statisches HTML/CSS/JS (`templates/index.html`, `static/app.js`).
- Der Service Worker registriert sich beim Laden der Seite und cached zentrale Assets, die in `static/sw.js` aufgeführt sind.
- Die Polygon-Validierung stellt mindestens 3 Punkte sicher und begrenzt auf Bildgrenzen.
- Die Ausgabeerzeugung verwendet Pillow (`PIL.Image`, `ImageDraw`).

Tipps für die lokale Entwicklung:

```bash
# Server starten
python server.py

# CLI mit einem vorhandenen Bild ausführen
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 Fehlerbehebung

- `openai.AuthenticationError` oder ähnlich:
  - Prüfen, ob `OPENAI_API_KEY` in der Shell gesetzt ist, die Python ausführt.
- `Model response did not contain valid JSON`:
  - Anderes Modell versuchen oder erneut ausführen; Fallback-Parsing ist implementiert, aber fehlerhafte Ausgaben können weiterhin scheitern.
- `Polygon must contain at least 3 points`:
  - Das Modell hat ein ungültiges Polygon zurückgegeben; mit einem klareren Bild erneut versuchen.
- UI lädt, aber Segmentierung schlägt fehl:
  - Server-Logs auf den von `/api/segment` zurückgegebenen Ausnahmetyp prüfen.
- `ModuleNotFoundError`:
  - Abhängigkeiten mit `pip install -r requirements.txt` in der aktiven Umgebung neu installieren.

## 🛣️ Roadmap

Mögliche nächste Schritte für dieses Repository:

1. Automatisierte Tests für Polygon-Validierung und Ausgabeerzeugung ergänzen.
2. CI ergänzen (Linting, Type-Checks und Smoke-Tests).
3. Batch-Modus-CLI für Verarbeitung auf Verzeichnisebene ergänzen.
4. Unterstützung für mehrere Objektmasken oder Instance-Segmentierungsausgabe ergänzen.
5. Dockerfile und Deployment-Dokumentation ergänzen.
6. Benchmark-Beispiele und Beispiel-Datensätze mit erwarteten Ausgaben ergänzen.
7. Mehrsprachige README-Dateien unter `i18n/` finalisieren.

## 🤝 Mitwirken

Beiträge sind willkommen.

Empfohlener Workflow:

1. Repository forken und einen Feature-Branch erstellen.
2. Fokussierte Änderungen mit klaren Commit-Messages vornehmen.
3. Manuelle Web- und CLI-Flows lokal validieren.
4. Pull Request erstellen, der Verhaltensänderungen und Testnachweise beschreibt.

Vorgeschlagene Beitragsbereiche:
- Besseres Prompt-Design für stabilere Polygon-Extraktion.
- Verbesserte Frontend-Visualisierung (Zoom/Pan, Konturglättung).
- Test-Harnesses und reproduzierbare Beispiel-Fixtures.
- Dokumentations- und Lokalisierungsverbesserungen.

## 📄 Lizenz

Derzeit ist in diesem Repository keine Lizenzdatei vorhanden.

Annahme: Standardmäßig sind alle Rechte vorbehalten, bis explizit eine Lizenz hinzugefügt wird.

Wenn du dieses Projekt teilen oder verteilen möchtest, füge eine `LICENSE`-Datei hinzu und aktualisiere diesen Abschnitt.
