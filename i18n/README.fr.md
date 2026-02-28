[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# Segmentation d’organoïdes (Web + CLI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)
![API](https://img.shields.io/badge/API-POST%20%2Fapi%2Fsegment-0f766e)
![Format](https://img.shields.io/badge/Result-Polygon%20JSON-f59e0b)

Une application Python pour segmenter des organoïdes dans des images de microscopie à l’aide de modèles OpenAI compatibles vision.

> Conçue pour des expérimentations locales rapides : téléversez une fois, inspectez les sorties overlay/mask/JSON, puis itérez sur le choix du modèle.

Ce dépôt comprend :
- Un serveur web Tornado avec une interface de téléversement.
- Un flux CLI pour l’usage par lot ou scripté.
- L’extraction de polygones, la génération de masques et le rendu d’images annotées.
- Une prise en charge PWA minimale (manifest + cache service worker pour les assets statiques principaux).

## 🧭 Navigation rapide

| Section | Objectif |
|---|---|
| [Aperçu](#aperçu) | Comprendre ce que fait le projet et ce qu’il produit |
| [Fonctionnalités](#fonctionnalités) | Voir les capacités clés des flux web, CLI et API |
| [Structure du projet](#structure-du-projet) | Localiser les fichiers principaux et les répertoires d’exécution |
| [Prérequis](#prérequis) | Vérifier les exigences de l’environnement |
| [Installation](#installation) | Préparer l’environnement Python et les dépendances |
| [Utilisation](#utilisation) | Exécuter l’app web, la CLI ou des appels API directs |
| [Configuration](#configuration) | Ajuster les paramètres du modèle et de l’exécution |
| [Exemples](#exemples) | Réutiliser des extraits pour les flux CLI et Python |
| [Notes de développement](#notes-de-développement) | Comprendre les détails d’implémentation et les astuces locales |
| [Dépannage](#dépannage) | Résoudre les problèmes d’exécution et de modèle courants |
| [Feuille de route](#feuille-de-route) | Améliorations prévues |
| [Contribution](#contribution) | Soumettre des changements efficacement |
| [Support](#support) | Options de don |
| [Licence](#licence) | Statut actuel de la licence |

## 🔍 Aperçu

L’application reçoit une image de microscopie en entrée, l’envoie à un modèle OpenAI avec un prompt à schéma JSON strict, puis renvoie un polygone unique traçant la frontière de l’organoïde.

### 🔄 Flux de bout en bout

1. Réception de l’image via téléversement web, chemin CLI ou formulaire multipart API.
2. Appel du modèle OpenAI pour produire une sortie de polygone structurée.
3. Validation et limitation des coordonnées du polygone aux bornes de l’image.
4. Rendu et persistance de trois artefacts : image annotée, masque binaire, JSON du polygone.
5. Renvoi des URL/chemins et des métadonnées (`width`, `height`, `confidence`).

### 📌 En un coup d’œil

| Zone | Détails |
|---|---|
| Entrée | Image de microscopie |
| Sortie principale | Polygone d’organoïde (points `x, y`) |
| Fichiers dérivés | PNG d’overlay annoté, PNG de masque binaire, JSON du polygone |
| Modes d’accès | Interface web, CLI, appel API direct |
| Backend | Tornado (`server.py`) |
| Parcours IA | OpenAI Responses API d’abord, repli sur Chat Completions |

Artefacts générés :
- `*_annotated.png` : image source avec overlay rouge semi-transparent.
- `*_mask.png` : masque binaire de l’organoïde.
- `*_polygon.json` : sortie structurée (`width`, `height`, `polygon`, `confidence`).

Fichiers d’exécution principaux :
- `server.py` : application web + routes API.
- `organoid_segmenter.py` : logique de segmentation et de génération image/masque.
- `segment_organoid.py` : wrapper CLI.

## ✨ Fonctionnalités

- Interface web sur `http://localhost:8888` pour une segmentation interactive rapide.
- Endpoint de type REST `POST /api/segment` avec support du téléversement multipart.
- Nom de modèle configurable depuis l’interface et la CLI (`gpt-4o-2024-08-06` par défaut).
- Validation et limitation des points du polygone aux bornes de l’image.
- Création automatique des répertoires de sortie (`uploads/`, `outputs/`).
- OpenAI Responses API en priorité, avec repli Chat Completions dans le flux de code.
- Prise en charge du service worker pour mettre en cache les fichiers statiques principaux.

## 🗂️ Structure du projet

```text
Yinghan/
├─ organoid_segmenter.py          # Logique de segmentation principale et rendu des sorties
├─ segment_organoid.py            # Point d’entrée CLI
├─ server.py                      # Serveur Tornado + API
├─ requirements.txt               # Dépendances Python
├─ templates/
│  └─ index.html                  # Shell de l’interface web
├─ static/
│  ├─ app.js                      # Logique frontend de téléversement + rendu des résultats
│  ├─ styles.css                  # Styles de l’interface
│  ├─ manifest.json               # Manifest PWA
│  └─ sw.js                       # Logique de cache du service worker
├─ i18n/                          # Fichiers README localisés
├─ uploads/                       # Stockage des téléversements à l’exécution (gitignored)
├─ outputs/                       # Sorties de segmentation à l’exécution (gitignored, créé au runtime)
└─ .auto-readme-work/             # Contexte/artefacts du pipeline de génération README
```

## ✅ Prérequis

- Python 3.10+ (3.11 recommandé).
- `pip` et prise en charge des environnements virtuels (`venv`).
- Clé API OpenAI avec accès à un modèle compatible vision.
- Accès réseau depuis l’environnement d’exécution vers les API OpenAI.

## ⚙️ Installation

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

Définissez votre clé API :

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

## 🚀 Utilisation

### ⚡ Aide-mémoire des commandes

| Tâche | Commande |
|---|---|
| Démarrer le serveur web | `python server.py` |
| Lancer la segmentation CLI d’une image unique | `python segment_organoid.py /path/to/image.jpg` |
| Lancer la CLI avec modèle explicite + répertoire de sortie | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| Appeler l’endpoint API | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Exécuter l’application web

```bash
python server.py
```

Ouvrez :

```text
http://localhost:8888
```

Flux web :
1. Choisissez une image.
2. Modifiez éventuellement le modèle dans le champ de saisie.
3. Cliquez sur **Segment**.
4. Vérifiez l’overlay, l’image annotée et le masque.

### 🧪 Exécuter la CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

Arguments optionnels :

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

La CLI affiche les chemins de sortie et un résumé contenant les dimensions de l’image et le nombre de points du polygone.

### 🔌 Appeler l’API directement

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Exemple de format de réponse :

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

## 🛠️ Configuration

Paramètres configurables actuels :

| Paramètre | Défaut | Où le définir |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Formulaire web `model`, CLI `--model`, champ API `model` |
| `out_dir` | `outputs` | CLI `--out-dir` |
| Clé API | aucune | Variable d’environnement `OPENAI_API_KEY` |

Hypothèses :
- Le client `OpenAI()` utilise des identifiants basés sur l’environnement.
- Aucune URL de base personnalisée ni réglage org/projet n’est requis, sauf si votre configuration de compte l’exige.

## 🧾 Exemples

### 🐍 Utilisation Python programmatique

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

### 📄 Inspecter le JSON du polygone

```bash
cat outputs/<name>_polygon.json
```

### 🧱 Fichiers de sortie typiques

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

## 🧠 Notes de développement

- Framework backend : Tornado (`server.py`).
- Stack frontend : HTML/CSS/JS statique (`templates/index.html`, `static/app.js`).
- Le service worker s’enregistre au chargement de la page et met en cache les assets principaux listés dans `static/sw.js`.
- La validation du polygone garantit au moins 3 points et borne les coordonnées aux limites de l’image.
- La génération des sorties utilise Pillow (`PIL.Image`, `ImageDraw`).

Astuces de développement local :

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

## 🩺 Dépannage

Correspondance rapide :

| Symptôme | Cause probable | Vérification rapide |
|---|---|---|
| Erreur d’authentification | Clé API manquante/invalide | `echo $OPENAI_API_KEY` dans le shell actif |
| Erreur d’analyse JSON ou de schéma | Sortie du modèle mal formée | Réessayez, ou changez de modèle dans l’UI/CLI |
| Moins de 3 points de polygone | Extraction de contour de faible confiance | Essayez une image plus nette puis relancez |
| L’UI fonctionne mais la segmentation échoue | Exception backend durant l’appel API | Inspectez les logs serveur pour `error_type` |
| Erreur d’import/module | Environnement incohérent | Réinstallez les dépendances dans le venv actif |

- `openai.AuthenticationError` (ou similaire) :
  - Vérifiez que `OPENAI_API_KEY` est défini dans la même session shell.
- `Model response did not contain valid JSON` :
  - Réessayez ou utilisez un autre modèle ; un parsing de secours existe, mais une sortie mal formée peut toujours échouer.
- `Polygon must contain at least 3 points` :
  - La sortie du modèle était invalide ; réessayez avec une image plus nette et plus contrastée.
- L’UI se charge mais la segmentation échoue :
  - Vérifiez les logs serveur pour `error_type` et les détails de stack trace depuis `/api/segment`.
- `ModuleNotFoundError` :
  - Réinstallez les dépendances dans l’environnement virtuel actif avec `pip install -r requirements.txt`.

## 🛣️ Feuille de route

Prochaines étapes potentielles pour ce dépôt :

1. Ajouter des tests automatisés pour la validation des polygones et la génération des sorties.
2. Ajouter la CI (lint, vérifications de type et smoke tests).
3. Ajouter un mode CLI batch pour le traitement au niveau répertoire.
4. Prendre en charge plusieurs masques d’objets ou la sortie de segmentation d’instances.
5. Ajouter un Dockerfile et une documentation de déploiement.
6. Ajouter des exemples de benchmark et des jeux de données d’exemple avec sorties attendues.
7. Finaliser les fichiers README multilingues sous `i18n/`.

## 🤝 Contribution

Les contributions sont les bienvenues.

Workflow recommandé :

1. Forkez le dépôt et créez une branche de fonctionnalité.
2. Faites des changements ciblés avec des messages de commit clairs.
3. Validez localement les flux web + CLI manuels.
4. Ouvrez une pull request décrivant les changements de comportement et les preuves de test.

Domaines de contribution suggérés :
- Meilleure conception de prompt pour une extraction de polygone plus stable.
- Visualisation frontend améliorée (zoom/pan, lissage de contour).
- Harnais de test et fixtures d’exemple reproductibles.
- Améliorations de documentation et de localisation.

<a id="support"></a>

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

<a id="license"></a>

## 📄 Licence

Aucun fichier de licence n’est actuellement présent dans ce dépôt.

Hypothèse : tous droits réservés par défaut tant qu’une licence n’est pas explicitement ajoutée.

Si vous prévoyez de partager ou distribuer ce projet, ajoutez un fichier `LICENSE` et mettez cette section à jour.
