[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://github.com/lachlanchen/LazyingArtWebsite/raw/main/media/brand/lazyingart-intro.gif)](https://lazying.art)

# Segmentación de Organoides (Web + CLI)

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

Una aplicación Python para segmentar organoides en imágenes de microscopía mediante modelos de OpenAI con capacidades de visión.

> Diseñada para experimentos locales rápidos: carga una imagen una vez, revisa las salidas de superposición/máscara/JSON y ajusta el modelo.

## 📋 Resumen rápido

| Aspecto | Detalles |
|---|---|
| Entrada | Imágenes de microscopía (carga local, ruta CLI o multipart por API) |
| Salida principal | Un polígono de organoide con puntaje de confianza |
| Conjunto de artefactos | PNG anotado, máscara binaria PNG, JSON de polígono |
| Interfaces | UI web, CLI, endpoint REST |
| Ruta de IA | OpenAI Responses API con fallback a Chat Completions |

---

## 🧩 Resumen de ejecución

| Canal | Punto de acceso | Mejor uso |
|---|---|---|
| Web | `python server.py` | Verificación visual rápida y ajustes |
| CLI | `python segment_organoid.py ...` | Ejecuciones por script o en lote |
| API | `POST /api/segment` | Automatización e integración de servicios |

---

Este repositorio incluye:
- Un servidor web Tornado con interfaz de carga.
- Un flujo de trabajo CLI para uso por lotes o automatizado.
- Extracción de polígonos, generación de máscaras y renderizado de imágenes anotadas.
- Soporte PWA mínimo (manifest + caché del service worker para activos estáticos principales).

## 🧭 Navegación rápida

| Sección | Propósito |
|---|---|
| [Visión general](#visión-general) | Entender qué hace el proyecto y qué produce |
| [Características](#características) | Ver capacidades clave en los flujos web, CLI y API |
| [Estructura del proyecto](#estructura-del-proyecto) | Encontrar archivos principales y directorios de ejecución |
| [Requisitos previos](#requisitos-previos) | Confirmar requisitos del entorno |
| [Instalación](#instalación) | Configurar el entorno Python y dependencias |
| [Uso](#uso) | Ejecutar app web, CLI o llamadas directas a la API |
| [Configuración](#configuración) | Ajustar parámetros de modelo y tiempo de ejecución |
| [Ejemplos](#ejemplos) | Reutilizar fragmentos para flujos CLI y Python |
| [Notas de desarrollo](#notas-de-desarrollo) | Entender detalles de implementación y consejos locales |
| [Solución de problemas](#solución-de-problemas) | Resolver problemas comunes de ejecución y modelo |
| [Hoja de ruta](#hoja-de-ruta) | Próximas mejoras planificadas |
| [Contribución](#contribución) | Enviar cambios de forma efectiva |
| [Support](#support) | Opciones de donación |
| [Licencia](#licencia) | Estado de licencias actual |

## 🔍 Visión general

La app recibe una imagen de microscopía de entrada, la envía a un modelo de OpenAI con un prompt de esquema JSON estricto y devuelve un único polígono que traza el borde del organoide.

### 🔄 Flujo de extremo a extremo

1. Recibe la imagen mediante carga web, ruta CLI o formulario multipart de API.
2. Invoca el modelo de OpenAI para generar una salida estructurada de polígono.
3. Valida y ajusta las coordenadas del polígono a los límites de la imagen.
4. Renderiza y guarda tres artefactos: imagen anotada, máscara binaria, JSON del polígono.
5. Devuelve URLs/rutas y metadatos (`width`, `height`, `confidence`).

### 📌 Resumen rápido

| Área | Detalles |
|---|---|
| Entrada | Imagen de microscopía |
| Salida principal | Polígono de organoide (`x, y`) |
| Archivos derivados | PNG de superposición anotada, PNG de máscara binaria, JSON de polígono |
| Modos de acceso | UI web, CLI, llamada directa a API |
| Backend | Tornado (`server.py`) |
| Ruta de IA | OpenAI Responses API primero, fallback a Chat Completions |

Artefactos generados:
- `*_annotated.png`: imagen original con superposición roja semitransparente.
- `*_mask.png`: máscara binaria del organoide.
- `*_polygon.json`: salida estructurada (`width`, `height`, `polygon`, `confidence`).

Archivos de ejecución principales:
- `server.py`: app web + rutas API.
- `organoid_segmenter.py`: lógica de segmentación y renderizado de imágenes/máscaras.
- `segment_organoid.py`: wrapper de CLI.

## ✨ Características

- Interfaz web en `http://localhost:8888` para segmentación interactiva rápida.
- Endpoint estilo REST `POST /api/segment` con soporte de carga multipart.
- Nombre de modelo configurable desde UI y CLI (`gpt-4o-2024-08-06` por defecto).
- Validación y recorte de puntos de polígono a los límites de la imagen.
- Creación automática del directorio de salida (`uploads/`, `outputs/`).
- OpenAI Responses API primero, fallback a Chat Completions en la ruta de código.
- Soporte de service worker para cacheo de archivos estáticos principales.

## 🗂️ Estructura del proyecto

```text
Yinghan/
├─ organoid_segmenter.py          # Lógica central de segmentación y renderizado de salidas
├─ segment_organoid.py            # Punto de entrada de CLI
├─ server.py                      # Servidor Tornado + API
├─ requirements.txt               # Dependencias de Python
├─ templates/
│  └─ index.html                  # Estructura base de UI web
├─ static/
│  ├─ app.js                      # Lógica frontend de carga + renderizado de resultados
│  ├─ styles.css                  # Estilos de UI
│  ├─ manifest.json               # Manifiesto PWA
│  └─ sw.js                       # Lógica de caché del service worker
├─ i18n/                          # Archivos README localizados
├─ uploads/                       # Almacenamiento de cargas en ejecución (gitignored)
├─ outputs/                       # Salidas de segmentación en ejecución (gitignored, creadas en runtime)
└─ .auto-readme-work/             # Contexto/artefactos del pipeline de README
```

### Archivos que sueles editar

- `server.py` para manejo de solicitudes, enrutado y formato de respuesta.
- `organoid_segmenter.py` para prompt del modelo, esquema y renderizado de salida.
- `templates/index.html` / `static/app.js` para comportamiento de UI.
- `segment_organoid.py` para ergonomía de CLI y valores por defecto.

## ✅ Requisitos previos

- Python 3.10+ (se recomienda 3.11).
- `pip` y soporte de entorno virtual (`venv`).
- API key de OpenAI con acceso a un modelo con capacidades de visión.
- Acceso a red desde el entorno de ejecución para llegar a las APIs de OpenAI.

## ⚙️ Instalación

```bash
git clone <your-repo-url>
cd Yinghan

# 1) Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 2) Instalar dependencias
pip install -r requirements.txt
```

Configura tu API key en la shell activa:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

Supuesto: no se incluye un cargador de `.env`, así que la configuración vía variable de entorno es necesaria.

## 🚀 Uso

### ⚡ Hoja de comandos

| Tarea | Comando |
|---|---|
| Iniciar servidor web | `python server.py` |
| Ejecutar segmentación CLI de una sola imagen | `python segment_organoid.py /path/to/image.jpg` |
| Ejecutar CLI con modelo + directorio de salida explícitos | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| Llamar endpoint API | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Ejecutar app web

```bash
python server.py
```

Abrir:

```text
http://localhost:8888
```

Flujo web:
1. Selecciona una imagen.
2. Cambia opcionalmente el modelo en el campo de entrada.
3. Haz clic en **Segment**.
4. Revisa la superposición, imagen anotada y máscara.

### 🧪 Ejecutar CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

Argumentos opcionales:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

La CLI imprime rutas de salida y un resumen con el tamaño de la imagen y el número de puntos del polígono.

### 🔌 Llamar API directamente

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Ejemplo de respuesta:

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

| Parámetro | Predeterminado | Dónde configurar |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Campo `model` en UI, CLI `--model`, campo API `model` |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API key | none | variable de entorno `OPENAI_API_KEY` |

Supuestos:
- El cliente `OpenAI()` usa credenciales basadas en entorno.
- No se requieren URL base personalizada ni ajustes de organización/proyecto salvo que tu cuenta lo exija.

## 🧾 Ejemplos

### 🐍 Uso programático en Python

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

### 📄 Inspeccionar JSON de polígono

```bash
cat outputs/<name>_polygon.json
```

### 🧱 Archivos de salida típicos

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

## 🧠 Notas de desarrollo

- Framework de backend: Tornado (`server.py`).
- Stack frontend: HTML/CSS/JS estático (`templates/index.html`, `static/app.js`).
- El service worker se registra al cargar la página y cachea activos principales listados en `static/sw.js`.
- La validación de polígono garantiza al menos 3 puntos y recorta los valores a los límites de la imagen.
- La generación de salida usa Pillow (`PIL.Image`, `ImageDraw`).

Consejos de desarrollo local:

```bash
# Ejecutar servidor
python server.py

# Ejecutar CLI con la imagen de muestra incluida
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 Solución de problemas

Resumen rápido:

| Síntoma | Causa probable | Verificación rápida |
|---|---|---|
| Error de autenticación | Falta o clave API inválida | `echo $OPENAI_API_KEY` en la shell activa |
| Error de parseo JSON o de esquema | Salida del modelo malformada | Reintenta o cambia el modelo en UI/CLI |
| Menos de 3 puntos de polígono | Extracción de contorno con baja confianza | Prueba con una imagen más clara y vuelve a ejecutarlo |
| La UI funciona pero falla la segmentación | Excepción backend durante llamada API | Revisa logs del servidor para `error_type` |
| Error de importación/módulo | Incompatibilidad de entorno | Reinstala dependencias en el venv activo |

- `openai.AuthenticationError` (o similar):
  - Verifica que `OPENAI_API_KEY` esté definida en la misma sesión de shell.
- `Model response did not contain valid JSON`:
  - Reintenta o usa otro modelo; existe fallback de parseo, pero la salida malformada puede seguir fallando.
- `Polygon must contain at least 3 points`:
  - La salida del modelo fue inválida; reintenta con una imagen más clara y de mayor contraste.
- La UI carga, pero la segmentación falla:
  - Revisa logs del servidor para `error_type` y el `stack trace` de `/api/segment`.
- `ModuleNotFoundError`:
  - Reinstala las dependencias en el entorno virtual activo con `pip install -r requirements.txt`.

## 🛣️ Hoja de ruta

Próximos pasos potenciales para este repositorio:

1. Añadir pruebas automatizadas para validación de polígono y generación de salidas.
2. Añadir CI (lint, chequeos de tipos y smoke tests).
3. Añadir CLI en modo lote para procesamiento por directorios.
4. Dar soporte a múltiples máscaras de objetos o salida de segmentación por instancias.
5. Añadir Dockerfile y documentación de despliegue.
6. Añadir ejemplos de benchmark y datasets de muestra con salidas esperadas.
7. Finalizar README multilingües bajo `i18n/`.

## 🤝 Contribución

Las contribuciones son bienvenidas.

Flujo recomendado:

1. Haz un fork del repositorio y crea una rama de características.
2. Haz cambios enfocados con mensajes de commit claros.
3. Valida localmente los flujos manuales web + CLI.
4. Abre un pull request describiendo los cambios de comportamiento y evidencia de prueba.

Áreas sugeridas para contribuir:
- Mejor diseño de prompts para una extracción de polígonos más estable.
- Visualización frontend mejorada (zoom/pan, suavizado de contornos).
- Harnesses de pruebas y fixtures reproducibles de ejemplo.
- Mejoras de documentación y localización.

## 📄 Licencia

Actualmente no hay ningún archivo de licencia en este repositorio.

Supuesto: todos los derechos están reservados por defecto hasta que se agregue una licencia explícita.

Si planeas compartir o distribuir este proyecto, añade un archivo `LICENSE` y actualiza esta sección.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
