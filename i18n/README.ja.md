[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# オルガノイド分割（Web + CLI）

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

OpenAIのビジョン対応モデルを使って、顕微鏡画像内のオルガノイドをセグメントする Python アプリケーションです。

> ローカルで素早く実験するために設計されています。画像を1回アップロードして overlay/mask/JSON の出力を確認し、モデル選択を反復できます。

## 📋 概要

| 観点 | 詳細 |
|---|---|
| 入力 | 顕微鏡画像（ローカルアップロード、CLI パス、API の multipart） |
| コア出力 | 信頼度スコア付きの1つのオルガノイドポリゴン |
| 成果物セット | 注釈付き PNG、2値マスク PNG、ポリゴン JSON |
| インターフェース | Web UI、CLI、REST エンドポイント |
| AI 経路 | Chat Completions フォールバック付き OpenAI Responses API |

---

## 🧩 実行サマリー

| チャネル | エントリ | 最適用途 |
|---|---|---|
| Web | `python server.py` | 画面で素早く確認し、調整する |
| CLI | `python segment_organoid.py ...` | 自動化・バッチ化に向いた実行 |
| API | `POST /api/segment` | 自動化やサービス統合 |

---

このリポジトリには以下が含まれます。
- Tornado の Web サーバー（アップロード UI 付き）。
- バッチ処理やスクリプト実行向けの CLI フロー。
- ポリゴン抽出、マスク生成、注釈付き画像レンダリング。
- コア静的アセットに対する manifest + service worker キャッシュによる最小限の PWA サポート。

## 🧭 クイックナビゲーション

| セクション | 目的 |
|---|---|
| [概要](#overview) | このプロジェクトの内容と出力内容を理解する |
| [機能](#features) | Web、CLI、API ワークフローの主要機能を確認する |
| [プロジェクト構成](#project-structure) | 主要ファイルと実行時ディレクトリを確認する |
| [前提条件](#prerequisites) | 環境要件を確認する |
| [インストール](#installation) | Python 環境と依存関係をセットアップする |
| [使い方](#usage) | Web アプリ、CLI、API 呼び出しを実行する |
| [設定](#configuration) | モデルや実行パラメータを調整する |
| [例](#examples) | CLI と Python のスニペットを再利用する |
| [開発ノート](#development-notes) | 実装の詳細とローカル開発のコツを把握する |
| [トラブルシューティング](#troubleshooting) | よくある実行時・モデルの問題を解決する |
| [ロードマップ](#roadmap) | 将来の改善予定を確認する |
| [コントリビューション](#contributing) | 変更提案の進め方 |
| [サポート](#support) | 寄付オプション |
| [ライセンス](#license) | 現在のライセンス状況 |

<a id="overview"></a>

## 🔍 概要

アプリは顕微鏡画像を受け取り、厳密な JSON スキーマのプロンプトで OpenAI モデルに渡し、オルガノイド境界をトレースする単一ポリゴンを返します。

### 🔄 エンドツーエンドのワークフロー

1. Web アップロード、CLI パス、または API multipart で画像を受け取ります。
2. OpenAI モデルを呼び出し、構造化されたポリゴン出力を生成します。
3. ポリゴン座標を検証し、画像境界内にクランプします。
4. 3 つの成果物（注釈付き画像、2 値マスク、ポリゴン JSON）を生成・保存します。
5. URL/パスとメタデータ（`width`、`height`、`confidence`）を返します。

### 📌 サマリー

| 項目 | 詳細 |
|---|---|
| 入力 | 顕微鏡画像 |
| コア出力 | オルガノイドポリゴン（`x`, `y` 座標） |
| 派生ファイル | 注釈付きオーバーレイ PNG、2 値マスク PNG、ポリゴン JSON |
| アクセス方法 | Web UI、CLI、直接 API 呼び出し |
| バックエンド | Tornado（`server.py`） |
| AI 経路 | OpenAI Responses API 優先、Chat Completions フォールバック |

生成される成果物:
- `*_annotated.png`: 半透明の赤いオーバーレイを重ねた元画像
- `*_mask.png`: 2 値オルガノイドマスク
- `*_polygon.json`: 構造化出力（`width`、`height`、`polygon`、`confidence`）

主な実行時ファイル:
- `server.py`: Web アプリ + API ルート
- `organoid_segmenter.py`: セグメント処理と画像／マスク出力ロジック
- `segment_organoid.py`: CLI エントリーポイント

## ✨ 機能

- `http://localhost:8888` の Web UI で対話的にすぐ分割できる。
- multipart アップロード対応の REST 風エンドポイント `POST /api/segment`。
- UI と CLI でモデル名を指定可能（デフォルト `gpt-4o-2024-08-06`）。
- ポリゴン点の検証と画像境界へのクランプ処理。
- 出力ディレクトリを自動作成（`uploads/`、`outputs/`）。
- OpenAI Responses API を先に使用し、コード上で Chat Completions をフォールバックとして使用。
- 主要な静的ファイルをキャッシュする service worker のサポート。

<a id="project-structure"></a>

## 🗂️ プロジェクト構成

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

### 通常編集するファイル

- `server.py`: リクエスト処理、ルーティング、レスポンス形式の調整。
- `organoid_segmenter.py`: モデルプロンプト、スキーマ、出力レンダリング。
- `templates/index.html` / `static/app.js`: UI 挙動。
- `segment_organoid.py`: CLI の操作性と既定引数。

<a id="prerequisites"></a>

## ✅ 前提条件

- Python 3.10+（3.11 推奨）。
- `pip` と仮想環境サポート（`venv`）。
- ビジョン対応モデルにアクセス可能な OpenAI API キー。
- 実行環境から OpenAI API へのネットワーク到達性。

<a id="installation"></a>

## ⚙️ インストール

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

アクティブなシェルで API キーを設定してください:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

仮定: `.env` ローダーは同梱されていないため、環境変数設定が必須です。

<a id="usage"></a>

## 🚀 使い方

### ⚡ コマンド早見表

| タスク | コマンド |
|---|---|
| Web サーバー起動 | `python server.py` |
| 単一画像 CLI 分割 | `python segment_organoid.py /path/to/image.jpg` |
| モデルと出力先を明示して CLI を実行 | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| API エンドポイント呼び出し | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Web アプリ実行

```bash
python server.py
```

開く:

```text
http://localhost:8888
```

Web フロー:
1. 画像を選択する。
2. 必要に応じて入力欄のモデルを変更する。
3. **Segment** をクリックする。
4. オーバーレイ、注釈付き画像、マスクを確認する。

### 🧪 CLI 実行

```bash
python segment_organoid.py /path/to/image.jpg
```

任意の引数:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI は出力パスと、画像の寸法とポリゴン点数の要約を表示します。

### 🔌 API を直接呼び出す

```bash
curl -X POST http://localhost:8888/api/segment \
  -F "image=@/path/to/image.jpg" \
  -F "model=gpt-4o-2024-08-06"
```

レスポンス例:

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

## 🛠️ 設定

現在の設定可能パラメータ:

| パラメータ | デフォルト | 設定場所 |
|---|---|---|
| `model` | `gpt-4o-2024-08-06` | Web フォーム `model`、CLI `--model`、API の `model` フィールド |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API キー | none | `OPENAI_API_KEY` 環境変数 |

前提:
- `OpenAI()` クライアントは環境変数ベースの認証情報を利用します。
- アカウント設定で必要な場合を除き、カスタム base URL や org/project 設定は不要です。

<a id="examples"></a>

## 🧾 例

### 🐍 Python からのプログラミング利用

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

### 📄 ポリゴン JSON を確認

```bash
cat outputs/<name>_polygon.json
```

### 🧱 典型的な出力ファイル

```text
outputs/
├─ <base>_<timestamp>_annotated.png
├─ <base>_<timestamp>_mask.png
└─ <base>_<timestamp>_polygon.json
```

<a id="development-notes"></a>

## 🧠 開発ノート

- バックエンドフレームワーク: Tornado（`server.py`）。
- フロントエンド構成: 静的 HTML/CSS/JS（`templates/index.html`、`static/app.js`）。
- Service worker はページ読み込み時に登録され、`static/sw.js` に列挙されたコアアセットをキャッシュします。
- ポリゴン検証は最低 3 点を保証し、画像境界にクランプします。
- 出力生成には Pillow（`PIL.Image`、`ImageDraw`）を使用します。

ローカル開発のヒント:

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

<a id="troubleshooting"></a>

## 🩺 トラブルシューティング

クイック確認:

| 症状 | 主な原因 | すぐ確認すること |
|---|---|---|
| 認証エラー | API キー未設定/無効 | 有効なシェルで `echo $OPENAI_API_KEY` を実行 |
| JSON パースまたはスキーマエラー | モデル出力の形式不正 | 再試行するか、UI/CLI でモデルを切り替える |
| ポリゴン点が 3 点未満 | 輪郭抽出の信頼度が低い | より鮮明な画像で再試行 |
| UI は動作するが分割が失敗 | API 呼び出し時のバックエンド例外 | `/api/segment` の `error_type` を含むサーバーログを確認 |
| Import/module エラー | 環境の不一致 | アクティブな venv で依存関係を再インストール |

- `openai.AuthenticationError`（または同等）:
  - 同じシェルセッションで `OPENAI_API_KEY` が設定されているか確認。
- `Model response did not contain valid JSON`:
  - 再試行するか、別モデルを使う。フォールバック解析がありますが、形式不正な出力は失敗することがあります。
- `Polygon must contain at least 3 points`:
  - モデル出力が無効です。より鮮明でコントラストの高い画像で再試行してください。
- UI が表示されるのに分割が失敗する:
  - サーバーログから `/api/segment` の `error_type` とスタックトレースを確認。
- `ModuleNotFoundError`:
  - アクティブな仮想環境で `pip install -r requirements.txt` を再実行。

<a id="roadmap"></a>

## 🛣️ ロードマップ

このリポジトリの次の検討項目:

1. ポリゴン検証と出力生成の自動テスト追加。
2. CI（lint、型チェック、スモークテスト）追加。
3. ディレクトリ単位処理向けのバッチモード CLI 追加。
4. 複数オブジェクトマスク／インスタンスセグメンテーション出力に対応。
5. Dockerfile とデプロイメント手順の文書化。
6. ベンチマーク例と期待される出力付きサンプルデータセット追加。
7. `i18n/` 下の多言語 README ファイルを完成。

<a id="contributing"></a>

## 🤝 コントリビュート

コントリビューションは歓迎します。

推奨ワークフロー:

1. リポジトリを Fork してフィーチャーブランチを作成。
2. 変更は焦点を絞り、明確なコミットメッセージを付与。
3. ローカルで Web + CLI フローを手動で検証。
4. 挙動の変更点とテスト証拠を記載したプルリクエストを作成。

推奨される貢献領域:
- より安定したポリゴン抽出のためのプロンプト設計改善。
- UI の可視化改善（ズーム/パン、輪郭のスムージング）。
- テストハーネスと再現可能なサンプルフィクスチャ。
- ドキュメントとローカライゼーションの改善。

<a id="support"></a>

## 📄 ライセンス

このリポジトリには現在ライセンスファイルがありません。

前提: 明示的なライセンスが追加されるまでは、デフォルトで all rights reserved です。

このプロジェクトを共有または配布する場合は、`LICENSE` ファイルを追加し、このセクションを更新してください。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
