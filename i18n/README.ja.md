[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# オルガノイド分割（Web + CLI）

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/Backend-Tornado-009688.svg)
![AI](https://img.shields.io/badge/OpenAI-Vision%20Segmentation-412991.svg)
![Status](https://img.shields.io/badge/README-First%20Complete%20Draft-success.svg)
![Interface](https://img.shields.io/badge/UI-Web%20%2B%20CLI-0ea5e9)
![Outputs](https://img.shields.io/badge/Artifacts-Overlay%20%7C%20Mask%20%7C%20JSON-f97316)
![PWA](https://img.shields.io/badge/PWA-Minimal%20Support-22c55e)
![API](https://img.shields.io/badge/API-POST%20%2Fapi%2Fsegment-0f766e)
![Format](https://img.shields.io/badge/Result-Polygon%20JSON-f59e0b)

OpenAI のビジョン対応モデルを使って、顕微鏡画像内のオルガノイドを分割する Python アプリケーションです。

> ローカルで素早く検証できるよう設計されています。1回アップロードすれば、overlay/mask/JSON の出力を確認しながらモデル選択を反復できます。

このリポジトリには次が含まれます。
- アップロード UI を備えた Tornado Web サーバー
- バッチ処理やスクリプト実行に使える CLI ワークフロー
- ポリゴン抽出、マスク生成、注釈付き画像レンダリング
- 最小限の PWA サポート（manifest + 主要静的アセット向け service worker キャッシュ）

## 🧭 クイックナビゲーション

| セクション | 目的 |
|---|---|
| [概要](#overview) | プロジェクトの機能と出力内容を把握する |
| [機能](#features) | Web・CLI・API の主要機能を確認する |
| [プロジェクト構成](#project-structure) | 主要ファイルと実行時ディレクトリを見つける |
| [前提条件](#prerequisites) | 環境要件を確認する |
| [インストール](#installation) | Python 環境と依存関係をセットアップする |
| [使い方](#usage) | Web アプリ、CLI、API 呼び出しを実行する |
| [設定](#configuration) | モデルや実行パラメータを調整する |
| [例](#examples) | CLI と Python のスニペットを再利用する |
| [開発メモ](#development-notes) | 実装の要点とローカル開発のヒントを把握する |
| [トラブルシューティング](#troubleshooting) | よくある実行時・モデル関連の問題を解決する |
| [ロードマップ](#roadmap) | 今後の改善予定を確認する |
| [コントリビューション](#contributing) | 変更提案の進め方を確認する |
| [Support](#support) | 寄付オプション |
| [ライセンス](#license) | 現在のライセンス状況 |

<a id="overview"></a>

## 🔍 概要

このアプリは顕微鏡画像を受け取り、厳密な JSON スキーマを指定したプロンプトで OpenAI モデルを呼び出し、オルガノイド境界をトレースする単一ポリゴンを返します。

### 🔄 エンドツーエンドの処理フロー

1. Web アップロード、CLI パス指定、または API の multipart form で画像を受け取る
2. OpenAI モデルを呼び出し、構造化ポリゴン出力を生成する
3. ポリゴン座標を検証し、画像境界内にクランプする
4. 3 つの成果物（注釈画像・2値マスク・ポリゴン JSON）をレンダリングして保存する
5. URL/パスとメタデータ（`width`、`height`、`confidence`）を返す

### 📌 ひと目でわかる仕様

| 項目 | 詳細 |
|---|---|
| 入力 | 顕微鏡画像 |
| コア出力 | オルガノイドポリゴン（`x, y` 点列） |
| 派生ファイル | 注釈オーバーレイ PNG、2値マスク PNG、ポリゴン JSON |
| 利用方法 | Web UI、CLI、直接 API 呼び出し |
| バックエンド | Tornado（`server.py`） |
| AI 経路 | OpenAI Responses API 優先、Chat Completions フォールバック |

生成される成果物:
- `*_annotated.png`: 半透明の赤色オーバーレイを重ねた元画像
- `*_mask.png`: オルガノイドの 2値マスク
- `*_polygon.json`: 構造化出力（`width`, `height`, `polygon`, `confidence`）

主要な実行時ファイル:
- `server.py`: Web アプリ + API ルート
- `organoid_segmenter.py`: 分割処理と画像/マスク出力ロジック
- `segment_organoid.py`: CLI ラッパー

<a id="features"></a>

## ✨ 機能

- `http://localhost:8888` で使える、対話的分割向け Web UI
- multipart アップロードに対応した REST 風エンドポイント `POST /api/segment`
- UI/CLI からモデル名を設定可能（デフォルト `gpt-4o-2024-08-06`）
- ポリゴン点の検証と画像境界内へのクランプ
- 出力ディレクトリを自動作成（`uploads/`, `outputs/`）
- コード経路で OpenAI Responses API を優先し、Chat Completions にフォールバック
- 主要静的ファイルをキャッシュする service worker サポート

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

<a id="prerequisites"></a>

## ✅ 前提条件

- Python 3.10+（3.11 推奨）
- `pip` と仮想環境サポート（`venv`）
- ビジョン対応モデルへアクセス可能な OpenAI API キー
- 実行環境から OpenAI API へ到達できるネットワーク接続

<a id="installation"></a>

## ⚙️ インストール

```bash
git clone <your-repo-url>
cd Yinghan

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt
```

API キーを設定します:

```bash
export OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell: $env:OPENAI_API_KEY="your_api_key_here"
```

<a id="usage"></a>

## 🚀 使い方

### ⚡ コマンド早見表

| タスク | コマンド |
|---|---|
| Web サーバー起動 | `python server.py` |
| 単一画像で CLI 分割 | `python segment_organoid.py /path/to/image.jpg` |
| モデルと出力先を明示して CLI 実行 | `python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06` |
| API エンドポイント呼び出し | `curl -X POST http://localhost:8888/api/segment -F "image=@/path/to/image.jpg" -F "model=gpt-4o-2024-08-06"` |

### 🌐 Web アプリを実行

```bash
python server.py
```

開く URL:

```text
http://localhost:8888
```

Web の手順:
1. 画像を選択します。
2. 必要に応じて入力欄でモデルを変更します。
3. **Segment** をクリックします。
4. オーバーレイ、注釈画像、マスクを確認します。

### 🧪 CLI を実行

```bash
python segment_organoid.py /path/to/image.jpg
```

任意引数:

```bash
python segment_organoid.py /path/to/image.jpg --out-dir outputs --model gpt-4o-2024-08-06
```

CLI は出力パスと、画像サイズおよびポリゴン点数を含むサマリーを表示します。

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
| `model` | `gpt-4o-2024-08-06` | Web フォーム `model`、CLI `--model`、API `model` フィールド |
| `out_dir` | `outputs` | CLI `--out-dir` |
| API キー | なし | 環境変数 `OPENAI_API_KEY` |

前提:
- `OpenAI()` クライアントは環境変数ベースの認証情報を使用する
- アカウント設定上必要な場合を除き、カスタム base URL や org/project 設定は不要

<a id="examples"></a>

## 🧾 例

### 🐍 Python からのプログラム利用

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

### 📄 Polygon JSON を確認

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

## 🧠 開発メモ

- バックエンドフレームワーク: Tornado（`server.py`）
- フロントエンド構成: 静的 HTML/CSS/JS（`templates/index.html`, `static/app.js`）
- service worker はページ読み込み時に登録され、`static/sw.js` に列挙された主要アセットをキャッシュする
- ポリゴン検証では 3 点以上を必須とし、画像境界にクランプする
- 出力生成には Pillow（`PIL.Image`, `ImageDraw`）を使用

ローカル開発のヒント:

```bash
# Run server
python server.py

# Run CLI against the included sample image
python segment_organoid.py 6f1e1874eacffe1dbae0393f48811e74.jpg
```

<a id="troubleshooting"></a>

## 🩺 トラブルシューティング

クイック対応表:

| 症状 | よくある原因 | すぐできる確認 |
|---|---|---|
| 認証エラー | API キー未設定または不正 | 有効なシェルで `echo $OPENAI_API_KEY` |
| JSON パース/スキーマエラー | モデル出力の形式不正 | 再実行、または UI/CLI でモデルを変更 |
| ポリゴン点が 3 未満 | 低信頼の輪郭抽出 | より鮮明な画像で再実行 |
| UI は動くが分割に失敗 | API 呼び出し中のバックエンド例外 | サーバーログの `error_type` を確認 |
| Import/module エラー | 環境不一致 | アクティブな venv で依存関係を再インストール |

- `openai.AuthenticationError`（または類似）:
  - 同じシェルセッションで `OPENAI_API_KEY` が設定されているか確認してください。
- `Model response did not contain valid JSON`:
  - 再試行するか別モデルを使ってください。フォールバック解析はありますが、出力形式が壊れていると失敗することがあります。
- `Polygon must contain at least 3 points`:
  - モデル出力が無効です。より鮮明でコントラストの高い画像で再実行してください。
- UI は表示されるが分割に失敗する:
  - `/api/segment` の `error_type` とスタックトレースをサーバーログで確認してください。
- `ModuleNotFoundError`:
  - アクティブな仮想環境で `pip install -r requirements.txt` を再実行してください。

<a id="roadmap"></a>

## 🛣️ ロードマップ

このリポジトリの次の候補:

1. ポリゴン検証と出力生成の自動テスト追加
2. CI（lint、型チェック、スモークテスト）追加
3. ディレクトリ単位処理向けバッチモード CLI 追加
4. 複数オブジェクトマスクやインスタンス分割出力の対応
5. Dockerfile とデプロイ手順ドキュメント追加
6. ベンチマーク例と期待出力付きサンプルデータセット追加
7. `i18n/` 配下の多言語 README の完成

<a id="contributing"></a>

## 🤝 コントリビューション

コントリビューションを歓迎します。

推奨ワークフロー:

1. リポジトリを Fork して機能ブランチを作成する
2. 変更は焦点を絞り、明確なコミットメッセージを付ける
3. ローカルで Web + CLI の手動フローを検証する
4. 振る舞いの変更点とテスト証跡を記載した Pull Request を作成する

推奨されるコントリビューション領域:
- より安定したポリゴン抽出のためのプロンプト設計改善
- フロントエンド可視化の改善（ズーム/パン、輪郭スムージング）
- テストハーネスと再現可能なサンプルフィクスチャ
- ドキュメントとローカライゼーション改善

<a id="support"></a>

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

<a id="license"></a>

## 📄 ライセンス

現在、このリポジトリにはライセンスファイルが含まれていません。

前提: ライセンスが明示的に追加されるまでは、デフォルトで all rights reserved です。

このプロジェクトを共有または配布する予定がある場合は、`LICENSE` ファイルを追加し、このセクションを更新してください。
