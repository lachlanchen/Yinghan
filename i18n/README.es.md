[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# Segmentación de Organoides (Web + CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)
![API](https://img.shields.io/badge/API-POST%20%2Fapi%2Fsegment-0f766e)
![Format](https://img.shields.io/badge/Result-Polygon%20JSON-f59e0b)

Una aplicación en Python para segmentar organoides en imágenes de microscopía usando modelos con capacidad de visión de OpenAI.

> Diseñada para experimentos locales rápidos: sube una imagen una vez, revisa los resultados de superposición/máscara/JSON e itera en la elección del modelo.

Este repositorio incluye:
- Un servidor web Tornado con interfaz de carga.
- Un flujo CLI para uso por lotes o mediante scripts.
- Extracción de polígonos, generación de máscaras y renderizado de imágenes anotadas.
- Soporte PWA mínimo (manifest + caché con service worker para recursos estáticos principales).

## 🧭 Navegación Rápida

| Sección | Propósito |
|---|---|
| [Resumen](#resumen) | Entender qué hace el proyecto y qué genera |
| [Características](#características) | Ver capacidades clave en flujos web, CLI y API |
| [Estructura del Proyecto](#estructura-del-proyecto) | Ubicar archivos principales y directorios de ejecución |
| [Prerrequisitos](#prerrequisitos) | Confirmar requisitos del entorno |
| [Instalación](#instalación) | Configurar entorno Python y dependencias |
| [Uso](#uso) | Ejecutar la app web, la CLI o llamadas directas a la API |
| [Configuración](#configuración) | Ajustar parámetros de modelo y ejecución |
| [Ejemplos](#ejemplos) | Reutilizar fragmentos para flujos CLI y Python |
| [Notas de Desarrollo](#notas-de-desarrollo) | Entender detalles de implementación y consejos locales |
| [Solución de Problemas](#solución-de-problemas) | Resolver incidencias comunes de ejecución y modelo |
| [Hoja de Ruta](#hoja-de-ruta) | Próximas mejoras planificadas |
| [Contribuir](#contribuir) | Enviar cambios de forma efectiva |
| [Support](#support) | Opciones de donación |
| [Licencia](#license) | Estado actual de licenciamiento |

## 🔍 Resumen

La app acepta una imagen de microscopía, la envía a un modelo de OpenAI con un prompt de esquema JSON estricto y devuelve un único polígono que traza el contorno del organoide.

### 🔄 Flujo Completo

1. Recibe la imagen mediante carga web, ruta CLI o formulario multipart de API.
2. Invoca el modelo de OpenAI para producir una salida estructurada de polígono.
3. Valida y limita las coordenadas del polígono a los límites de la imagen.
4. Renderiza y guarda tres artefactos: imagen anotada, máscara binaria, JSON del polígono.
5. Devuelve URLs/rutas y metadatos (`width`, `height`, `confidence`).

### 📌 Vista Rápida

| Área | Detalles |
|---|---|
| Entrada | Imagen de microscopía |
| Salida principal | Polígono del organoide (puntos `x, y`) |
| Archivos derivados | Superposición anotada PNG, máscara binaria PNG, JSON del polígono |
| Modos de acceso | Web UI, CLI, llamada directa a API |
| Backend | Tornado (`server.py`) |
| Ruta de IA | OpenAI Responses API primero, fallback a Chat Completions |

Artefactos generados:
- `*_annotated.png`: imagen de origen con superposición roja semitransparente.
- `*_mask.png`: máscara binaria del organoide.
- `*_polygon.json`: salida estructurada (`width`, `height`, `polygon`, `confidence`).

Archivos principales en ejecución:
- `server.py`: app web + rutas API.
- `organoid_segmenter.py`: lógica de segmentación y salida de imagen/máscara.
- `segment_organoid.py`: wrapper CLI.

## ✨ Características

- Web UI en `http://localhost:8888` para segmentación interactiva rápida.
- Endpoint tipo REST `POST /api/segment` con soporte de carga multipart.
- Nombre de modelo configurable desde UI y CLI (`gpt-4o-2024-08-06` por defecto).
- Validación y limitación de puntos de polígono a los límites de la imagen.
- Creación automática de directorios de salida (`uploads/`, `outputs/`).
- OpenAI Responses API primero y fallback a Chat Completions en la ruta de código.
- Soporte de service worker para cachear archivos estáticos principales.

## 🗂️ Estructura del Proyecto

```text
Yinghan/
├─ organoid_segmenter.py          # Lógica principal de segmentación y renderizado de salidas
├─ segment_organoid.py            # Punto de entrada CLI
├─ server.py                      # Servidor Tornado + API
├─ requirements.txt               # Dependencias de Python
├─ templates/
│  └─ index.html                  # Shell de la interfaz web
├─ static/
│  ├─ app.js                      # Lógica frontend de carga y renderizado de resultados
│  ├─ styles.css                  # Estilos de la UI
│  ├─ manifest.json               # Manifest de PWA
│  └─ sw.js                       # Lógica de caché del service worker
├─ i18n/                          # Archivos README localizados
├─ uploads/                       # Almacenamiento de cargas en ejecución (gitignored)
├─ outputs/                       # Salidas de segmentación en ejecución (gitignored, se crea en runtime)
└─ .auto-readme-work/             # Contexto/artefactos del pipeline de generación de README
```

## ✅ Prerrequisitos

- Python 3.10+ (3.11 recomendado).
- `pip` y soporte de entorno virtual (`venv`).
- Clave API de OpenAI con acceso a un modelo con capacidad de visión.
- Acceso de red desde el entorno de ejecución a las APIs de OpenAI.

## ⚙️ Instalación

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

Configura tu clave API:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

## 🚀 Uso

### ⚡ Resumen de Comandos

| Tarea | Comando |
|---|---|
| Iniciar servidor web | `python server.py` |
| Ejecutar segmentación CLI de una sola imagen | `python segment_organoid.py /path/to/image.jpg` |
| Ejecutar CLI con modelo + directorio de salida explícitos | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| Llamar al endpoint API | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Ejecutar la App Web

```bash
python server.py
```

Abre:

```text
http://localhost:8888
```

Flujo web:
1. Elige una imagen.
2. Opcionalmente cambia el modelo en el campo de entrada.
3. Haz clic en **Segment**.
4. Revisa la superposición, la imagen anotada y la máscara.

### 🧪 Ejecutar CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

Argumentos opcionales:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

La CLI imprime rutas de salida y un resumen con las dimensiones de la imagen y el número de puntos del polígono.

### 🔌 Llamar a la API Directamente

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Ejemplo de estructura de respuesta:

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

Parámetros configurables actuales:

| Parámetro | Valor por defecto | Dónde configurarlo |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Formulario web `model`, CLI `--model`, campo API `model` |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | none | Variable de entorno `OPENAI_API_KEY` |

Supuestos:
- El cliente `OpenAI()` usa credenciales basadas en entorno.
- No se requiere URL base personalizada ni ajustes de org/proyecto, salvo que tu cuenta los necesite.

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

### 📄 Inspeccionar JSON del Polígono

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

- Framework de backend: Tornado (`server.py`).
- Stack de frontend: HTML/CSS/JS estático (`templates/index.html`, `static/app.js`).
- El service worker se registra al cargar la página y cachea recursos principales listados en `static/sw.js`.
- La validación de polígonos garantiza al menos 3 puntos y limita los valores a los bordes de la imagen.
- La generación de salidas usa Pillow (`PIL.Image`, `ImageDraw`).

Consejos para desarrollo local:

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 Solución de Problemas

Mapa rápido:

| Síntoma | Causa probable | Verificación rápida |
|---|---|---|
| Error de autenticación | API key ausente/incorrecta | `echo $OPENAI_API_KEY` en la shell activa |
| Error de parseo JSON o de esquema | Salida de modelo malformada | Reintentar o cambiar modelo en UI/CLI |
| Menos de 3 puntos de polígono | Extracción de contorno de baja confianza | Probar una imagen más clara y volver a ejecutar |
| La UI funciona pero falla la segmentación | Excepción de backend durante llamada API | Revisar logs del servidor para `error_type` |
| Error de importación/módulo | Desajuste de entorno | Reinstalar dependencias en el venv activo |

- `openai.AuthenticationError` (o similar):
  - Verifica que `OPENAI_API_KEY` esté definida en la misma sesión de shell.
- `Model response did not contain valid JSON`:
  - Reintenta o usa otro modelo; existe parseo de fallback, pero salidas malformadas pueden seguir fallando.
- `Polygon must contain at least 3 points`:
  - La salida del modelo fue inválida; reintenta con una imagen más clara y de mayor contraste.
- La UI carga, pero falla la segmentación:
  - Revisa logs del servidor para `error_type` y detalles del stack trace de `/api/segment`.
- `ModuleNotFoundError`:
  - Reinstala dependencias en el entorno virtual activo con `pip install -r requirements.txt`.

## 🛣️ Hoja de Ruta

Posibles próximos pasos para este repositorio:

1. Añadir pruebas automatizadas para validación de polígonos y generación de salidas.
2. Añadir CI (lint, comprobaciones de tipos y smoke tests).
3. Añadir CLI en modo batch para procesar directorios completos.
4. Soportar múltiples máscaras de objeto o salida de segmentación por instancias.
5. Añadir Dockerfile y documentación de despliegue.
6. Añadir ejemplos de benchmark y datasets de muestra con salidas esperadas.
7. Completar los README multilingües bajo `i18n/`.

## 🤝 Contribuir

Las contribuciones son bienvenidas.

Flujo de trabajo recomendado:

1. Haz un fork del repositorio y crea una rama de funcionalidad.
2. Realiza cambios acotados con mensajes de commit claros.
3. Valida localmente los flujos manuales web + CLI.
4. Abre un pull request describiendo cambios de comportamiento y evidencia de pruebas.

Áreas sugeridas para contribuir:
- Mejor diseño de prompts para una extracción de polígonos más estable.
- Visualización frontend mejorada (zoom/pan, suavizado de contorno).
- Arneses de pruebas y fixtures de ejemplo reproducibles.
- Mejoras de documentación y localización.

<a id="support"></a>

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

<a id="license"></a>

## 📄 Licencia

Actualmente no hay ningún archivo de licencia en este repositorio.

Supuesto: todos los derechos están reservados por defecto hasta que se añada explícitamente una licencia.

Si planeas compartir o distribuir este proyecto, añade un archivo `LICENSE` y actualiza esta sección.
