[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://lazying.art/media/brand/lazyingart-intro.gif)](https://lazying.art)

# Segmentation d'organoïdes (Web + CLI)

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

Une application Python pour segmenter des organoïdes dans des images de microscopie à l'aide de modèles OpenAI capables de vision.

> Pensée pour des expérimentations locales rapides : téléversez une image, consultez les résultats overlay/mask/JSON, puis itérez sur le choix du modèle.

## 📋 Vue d'ensemble

| Aspect | Détails |
|---|---|
| Entrée | Images de microscopie (téléversement local, chemin CLI, ou multipart API) |
| Sortie principale | Un polygone d'organoïde avec score de confiance |
| Ensemble d'artefacts | PNG annoté, PNG de masque binaire, JSON de polygone |
| Interfaces | Interface web, CLI, endpoint REST |
| Chemin IA | API Responses d'OpenAI avec fallback Chat Completions |

---

## 🧩 Résumé d'exécution

| Canal | Entrée | Utilisation recommandée |
|---|---|---|
| Web | `python server.py` | Vérification visuelle rapide et ajustements |
| CLI | `python segment_organoid.py ...` | Exécutions scriptées ou prêtes pour le batch |
| API | `POST /api/segment` | Automatisation et intégration de service |

---

Ce dépôt comprend :
- Un serveur web Tornado avec interface de téléversement.
- Un flux de travail CLI pour usage batch ou script.
- Extraction de polygones, génération de masque et rendu d'image annotée.
- Support PWA minimal (manifest + cache service worker pour les actifs statiques principaux).

## 🧭 Navigation rapide

| Section | Objectif |
|---|---|
| [Aperçu](#aperçu) | Comprendre le fonctionnement du projet et les sorties produites |
| [Fonctionnalités](#fonctionnalités) | Voir les capacités clés en modes web, CLI et API |
| [Structure du projet](#structure-du-projet) | Localiser les fichiers principaux et les dossiers d'exécution |
| [Prérequis](#prérequis) | Vérifier les exigences d'environnement |
| [Installation](#installation) | Mettre en place l'environnement Python et les dépendances |
| [Utilisation](#utilisation) | Lancer l'application web, CLI, ou des appels API directs |
| [Configuration](#configuration) | Ajuster le modèle et les paramètres d'exécution |
| [Exemples](#exemples) | Réutiliser des extraits pour les flux CLI et Python |
| [Notes de développement](#notes-de-développement) | Comprendre les détails d'implémentation et astuces locales |
| [Dépannage](#dépannage) | Résoudre les erreurs courantes de runtime et de modèle |
| [Feuille de route](#feuille-de-route) | Améliorations prévues |
| [Contribuer](#contribuer) | Soumettre des changements efficacement |
| [Support](#support) | Options de dons |
| [Licence](#licence) | Statut de licence actuel |

## 🔍 Aperçu

L'application accepte une image de microscopie en entrée, l'envoie à un modèle OpenAI avec une consigne JSON stricte, puis renvoie un unique polygone décrivant la frontière de l'organoïde.

### 🔄 Flux de bout en bout

1. Réception de l'image via téléversement web, chemin CLI, ou formulaire multipart API.
2. Appel du modèle OpenAI pour produire une sortie polygone structurée.
3. Validation et contrainte des coordonnées du polygone dans les limites de l'image.
4. Rendu et persistance de trois artefacts : image annotée, masque binaire, JSON de polygone.
5. Retour des URLs/chemins et des métadonnées (`width`, `height`, `confidence`).

### 📌 En bref

| Domaine | Détails |
|---|---|
| Entrée | Image de microscopie |
| Sortie principale | Polygone de l'organoïde (`x, y`) |
| Fichiers dérivés | PNG overlay annoté, PNG masque binaire, JSON de polygone |
| Modes d'accès | UI web, CLI, appel API direct |
| Backend | Tornado (`server.py`) |
| Chemin IA | API Responses d'OpenAI en priorité, fallback Chat Completions |

Artefacts générés :
- `*_annotated.png` : image source avec overlay rouge semi-transparent.
- `*_mask.png` : masque binaire de l'organoïde.
- `*_polygon.json` : sortie structurée (`width`, `height`, `polygon`, `confidence`).

Fichiers d'exécution principaux :
- `server.py` : application web + routes API.
- `organoid_segmenter.py` : logique de segmentation et génération image/masque.
- `segment_organoid.py` : wrapper CLI.

## ✨ Fonctionnalités

- UI web sur `http://localhost:8888` pour une segmentation interactive rapide.
- Endpoint de type REST `POST /api/segment` avec support du multipart upload.
- Nom de modèle configurable depuis l'UI et la CLI (`gpt-4o-2024-08-06` par défaut).
- Validation et contrainte des points du polygone dans les limites de l'image.
- Création automatique des répertoires de sortie (`uploads/`, `outputs/`).
- Utilisation prioritaire de l'API Responses d'OpenAI, fallback Chat Completions côté code.
- Prise en charge du service worker pour mettre en cache les fichiers statiques principaux.

## 🗂️ Structure du projet

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

### Fichiers que vous modifierez généralement

- `server.py` pour la gestion des requêtes, le routage et le format de réponse.
- `organoid_segmenter.py` pour l'invite du modèle, le schéma et le rendu des sorties.
- `templates/index.html` / `static/app.js` pour le comportement de l'UI.
- `segment_organoid.py` pour l'ergonomie CLI et les valeurs par défaut des arguments.

## ✅ Prérequis

- Python 3.10+ (3.11 recommandé).
- `pip` et support d'environnement virtuel (`venv`).
- Clé API OpenAI avec accès à un modèle capable de vision.
- Accès réseau à partir de l'environnement d'exécution vers les API OpenAI.

## ⚙️ Installation

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

Définissez votre clé API dans le shell actif :

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

Hypothèse : aucun chargeur `.env` n'est fourni, donc la configuration via variable d'environnement est requise.

## 🚀 Utilisation

### ⚡ Référentiel de commandes

| Tâche | Commande |
|---|---|
| Démarrer le serveur web | `python server.py` |
| Lancer une segmentation CLI sur une seule image | `python segment_organoid.py /path/to/image.jpg` |
| Lancer la CLI avec modèle explicite + dossier de sortie | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| Appeler l'endpoint API | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Lancer l'application web

```bash
python server.py
```

Ouvrez :

```text
http://localhost:8888
```

Parcours web :
1. Choisir une image.
2. Modifier éventuellement le modèle dans le champ de saisie.
3. Cliquer sur **Segment**.
4. Vérifier overlay, image annotée et masque.

### 🧪 Utiliser la CLI

```bash
python segment_organoid.py /path/to/image.jpg
```

Arguments optionnels :

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

La CLI affiche les chemins de sortie et un résumé incluant dimensions de l'image et nombre de points du polygone.

### 🔌 Appeler l'API directement

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

Format de réponse attendu :

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

| Paramètre | Valeur par défaut | Où définir |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Formulaire web `model`, CLI `--model`, champ API `model` |
| `out_dir` | `outputs` | CLI `--out-dir` |
| Clé API | none | Variable d'environnement `OPENAI_API_KEY` |

Hypothèses :
- Le client `OpenAI()` utilise des identifiants basés sur l'environnement.
- Aucune URL de base personnalisée ou réglage d'organisation/projet n'est requis sauf si votre configuration de compte l'exige.

## 🧾 Exemples

### 🐍 Utilisation Python programmative

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

### 📄 Examiner le JSON du polygone

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
- Le service worker s'enregistre au chargement de la page et met en cache les actifs principaux listés dans `static/sw.js`.
- La validation du polygone garantit au moins 3 points et le clamp aux limites de l'image.
- La génération des sorties utilise Pillow (`PIL.Image`, `ImageDraw`).

Conseils de développement local :

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
| Erreur d'authentification | Clé API manquante/invalid | `echo $OPENAI_API_KEY` dans le shell actif |
| Erreur d'analyse JSON ou de schéma | Sortie du modèle malformée | Réessayez, ou changez le modèle dans l'UI/CLI |
| Moins de 3 points de polygone | Extraction de contour à faible confiance | Essayez une image plus claire et relancez |
| L'UI fonctionne mais la segmentation échoue | Exception backend pendant l'appel API | Consultez les logs serveur pour `error_type` |
| Erreur d'import/module | Incompatibilité d'environnement | Réinstallez les dépendances dans le venv actif |

- `openai.AuthenticationError` (ou similaire) :
  - Vérifiez que `OPENAI_API_KEY` est défini dans la même session shell.
- `Model response did not contain valid JSON` :
  - Réessayez ou utilisez un modèle différent ; un parsing de secours existe mais une sortie malformée peut encore échouer.
- `Polygon must contain at least 3 points` :
  - La sortie du modèle était invalide ; réessayez avec une image plus claire et au meilleur contraste.
- UI loads but segmentation fails:
  - Check server logs for `error_type` and stack trace details from `/api/segment`.
- `ModuleNotFoundError` :
  - Réinstallez les dépendances dans l'environnement virtuel actif avec `pip install -r requirements.txt`.

## 🛣️ Feuille de route

Prochaines étapes possibles pour ce dépôt :

1. Ajouter des tests automatisés pour la validation de polygone et la génération de sortie.
2. Ajouter la CI (lint, vérification de types et tests smoke).
3. Ajouter un mode CLI batch pour le traitement par dossier.
4. Prendre en charge plusieurs masques d'objets ou une sortie de segmentation d'instances.
5. Ajouter un Dockerfile et une documentation de déploiement.
6. Ajouter des exemples de benchmark et jeux de données d'exemple avec sorties attendues.
7. Finaliser les fichiers README multilingues sous `i18n/`.

## 🤝 Contribuer

Les contributions sont bienvenues.

Flux recommandé :

1. Forker le dépôt et créer une branche de fonctionnalité.
2. Effectuer des changements ciblés avec des messages de commit explicites.
3. Valider localement les flux web + CLI manuellement.
4. Ouvrir une pull request décrivant les changements de comportement et les éléments de preuve des tests.

Domaines de contribution suggérés :
- Meilleure conception d'invite pour une extraction de polygones plus stable.
- Visualisation frontend améliorée (zoom/pan, lissage des contours).
- Jauges de test et jeux d'échantillons reproductibles.
- Documentation et améliorations de localisation.

## 📄 Licence

Aucun fichier de licence n'est actuellement présent dans ce dépôt.

Hypothèse : tous les droits sont réservés par défaut jusqu'à l'ajout explicite d'une licence.

Si vous prévoyez de partager ou distribuer ce projet, ajoutez un fichier `LICENSE` et mettez à jour cette section.


## ❤️ Support

<!-- support:start -->
[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-EA4AAA?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)
[![LazyingArt Support](https://img.shields.io/badge/LazyingArt-Support-0EA5E9?style=for-the-badge)](https://chat.lazying.art/donate)
[![PayPal Support](https://img.shields.io/badge/PayPal-Support-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen)
[![Stripe Support](https://img.shields.io/badge/Stripe-Support-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400)
<!-- support:end -->
