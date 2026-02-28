[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# Segmentación de Organoides (Web + CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)

Una aplicación en Python para segmentar organoides en imágenes de microscopía mediante modelos de OpenAI con capacidades de visión.

Este repositorio incluye:
- Un servidor web Tornado con interfaz de carga.
- Un flujo de trabajo CLI para uso por lotes o mediante scripts.
- Extracción de polígonos, generación de máscaras y renderizado de imágenes anotadas.
- Soporte PWA mínimo (manifest + caché de service worker para recursos estáticos principales).

## 🔍 Resumen

La app acepta una imagen de microscopía de entrada, la envía a un modelo de OpenAI con un prompt de esquema JSON estricto y devuelve un único polígono que traza el límite del organoide.

### 📌 Vista Rápida

| Área | Detalles |
|---|---|
| Entrada | Imagen de microscopía |
| Salida principal | Polígono del organoide (puntos `x, y`) |
| Archivos derivados | Overlay anotado PNG, máscara binaria PNG, polígono JSON |
| Modos de acceso | Interfaz web, CLI, llamada directa a la API |
| Backend | Tornado (`server.py`) |
| Ruta de IA | OpenAI Responses API primero, Chat Completions como respaldo |

Artefactos generados:
- `*_annotated.png`: imagen de origen con overlay rojo semitransparente.
- `*_mask.png`: máscara binaria del organoide.
- `*_polygon.json`: salida estructurada (`width`, `height`, `polygon`, `confidence`).

Archivos principales de ejecución:
- `server.py`: app web + rutas de API.
- `organoid_segmenter.py`: lógica de segmentación y salida de imagen/máscara.
- `segment_organoid.py`: envoltorio de CLI.

## ✨ Funcionalidades

- Interfaz web en `http://localhost:8888` para segmentación interactiva rápida.
- Endpoint tipo REST `POST /api/segment` con soporte de carga multipart.
- Nombre de modelo configurable desde la UI y la CLI (`gpt-4o-2024-08-06` por defecto).
- Validación y ajuste (clamping) de los puntos del polígono a los límites de la imagen.
- Creación automática de directorios de salida (`uploads/`, `outputs/`).
- OpenAI Responses API como primera opción, Chat Completions como respaldo en la ruta de código.
- Soporte de service worker para cachear archivos estáticos principales.

## 🗂️ Estructura del Proyecto

```text
Yinghan/
├─ organoid_segmenter.py          # Lógica principal de segmentación y renderizado de salida
├─ segment_organoid.py            # Punto de entrada de CLI
├─ server.py                      # Servidor Tornado + API
├─ requirements.txt               # Dependencias de Python
├─ templates/
│  └─ index.html                  # Contenedor de la interfaz web
├─ static/
│  ├─ app.js                      # Lógica frontend de carga y renderizado de resultados
│  ├─ styles.css                  # Estilos de la UI
│  ├─ manifest.json               # Manifest de PWA
│  └─ sw.js                       # Lógica de caché del service worker
├─ i18n/                          # Archivos README localizados (planificados/generados por pipeline)
├─ uploads/                       # Almacenamiento de cargas en ejecución (gitignored)
├─ outputs/                       # Salidas de segmentación en ejecución (gitignored, creadas en runtime)
└─ .auto-readme-work/             # Contexto/artefactos del pipeline de generación de README
```

## ✅ Requisitos Previos

- Python 3.10+ (se requiere 3.x; 3.11 recomendado).
- Clave de API de OpenAI con acceso a un modelo con capacidades de visión.
- Acceso de red desde el entorno de ejecución hacia las APIs de OpenAI.

## ⚙️ Instalación

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

Configura tu clave de API:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

## 🚀 Uso

### 🌐 Ejecutar la App Web

```bash
python server.py
```

Abrir:

```text
http://localhost:8888
```

Flujo web:
1. Elige una imagen.
2. Opcionalmente cambia el modelo en el campo de entrada.
3. Haz clic en **Segment**.
4. Revisa el overlay, la imagen anotada y la máscara.

### 🧪 Ejecutar CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

Argumentos opcionales:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

La CLI imprime las rutas de salida y un resumen con las dimensiones de la imagen y el número de puntos del polígono.

### 🔌 Llamar a la API Directamente

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Forma de respuesta de ejemplo:

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

## 🛠️ Configuración

Parámetros configurables actuales en el código:

- `model`:
  - Predeterminado: `gpt-4o-2024-08-06`
  - Se puede establecer mediante la entrada del formulario web o la opción CLI `--model`
- `out_dir`:
  - Opción de CLI `--out-dir` (predeterminado `outputs`)
  - El servidor usa `outputs/` internamente

Variables de entorno:
- `OPENAI_API_KEY` (obligatoria).

Supuestos:
- El cliente `OpenAI()` usa credenciales basadas en variables de entorno.
- No se requieren configuraciones personalizadas de base URL ni de org/proyecto, salvo que la configuración de tu cuenta OpenAI lo necesite.

## 🧾 Ejemplos

### 🐍 Uso Programático en Python

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

### 📄 Inspeccionar el JSON del Polígono

```bash
cat outputs/<name>_polygon.json
```

### 🧱 Archivos de Salida Típicos

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

## 🧠 Notas de Desarrollo

- Framework backend: Tornado (`server.py`).
- Stack frontend: HTML/CSS/JS estático (`templates/index.html`, `static/app.js`).
- El service worker se registra al cargar la página y cachea los recursos principales listados en `static/sw.js`.
- La validación de polígonos garantiza al menos 3 puntos y ajusta los límites a los bordes de la imagen.
- La generación de salida usa Pillow (`PIL.Image`, `ImageDraw`).

Consejos para desarrollo local:

```bash
# Run server
python server.py

# Run CLI against an existing image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 Resolución de Problemas

- `openai.AuthenticationError` o similar:
  - Verifica que `OPENAI_API_KEY` esté definida en la shell donde ejecutas Python.
- `Model response did not contain valid JSON`:
  - Prueba con otro modelo o vuelve a ejecutar; hay parsing de respaldo, pero la salida malformada puede seguir fallando.
- `Polygon must contain at least 3 points`:
  - El modelo devolvió un polígono no válido; vuelve a intentar con una imagen más clara.
- La UI carga, pero la segmentación falla:
  - Revisa los logs del servidor para ver el tipo de excepción devuelto por `/api/segment`.
- `ModuleNotFoundError`:
  - Reinstala dependencias con `pip install -r requirements.txt` en el entorno activo.

## 🛣️ Hoja de Ruta

Posibles siguientes pasos para este repositorio:

1. Añadir pruebas automatizadas para la validación de polígonos y la generación de salidas.
2. Añadir CI (lint, comprobaciones de tipos y smoke tests).
3. Añadir modo por lotes en la CLI para procesamiento a nivel de directorio.
4. Soportar múltiples máscaras de objetos o salida de segmentación por instancias.
5. Añadir Dockerfile y documentación de despliegue.
6. Añadir ejemplos de benchmark y datasets de muestra con salidas esperadas.
7. Finalizar los archivos README multilingües en `i18n/`.

## 🤝 Contribuir

Las contribuciones son bienvenidas.

Flujo de trabajo recomendado:

1. Haz un fork del repositorio y crea una rama de funcionalidad.
2. Realiza cambios enfocados con mensajes de commit claros.
3. Valida localmente los flujos manuales web + CLI.
4. Abre un pull request describiendo los cambios de comportamiento y la evidencia de pruebas.

Áreas sugeridas para contribuir:
- Mejor diseño del prompt para una extracción de polígonos más estable.
- Mejora de visualización en frontend (zoom/pan, suavizado de contornos).
- Harnesses de pruebas y fixtures de muestra reproducibles.
- Mejoras de documentación y localización.

## 📄 Licencia

Actualmente no hay un archivo de licencia en este repositorio.

Supuesto: por defecto, todos los derechos están reservados hasta que se añada explícitamente una licencia.

Si planeas compartir o distribuir este proyecto, añade un archivo `LICENSE` y actualiza esta sección.
