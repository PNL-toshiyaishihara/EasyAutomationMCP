# EasyAutomationMCP

```
   ______                
  / ____/___ ________  __
 / __/ / __ `/ ___/ / / /
/ /___/ /_/ (__  ) /_/ / 
\____/\__,_/____/\__, /  
                /____/   

    ___         __                        __  _           
   /   | __  __/ /_____  ____ ___  ____ _/ /_(_)___  ____ 
  / /| |/ / / / __/ __ \/ __ `__ \/ __ `/ __/ / __ \/ __ \
 / ___ / /_/ / /_/ /_/ / / / / / / /_/ / /_/ / /_/ / / / /
/_/  |_\__,_/\__/\____/_/ /_/ /_/\__,_/\__/_/\____/_/ /_/ 

    __  _____________ 
   /  |/  / ____/ __ \
  / /|_/ / /   / /_/ /
 / /  / / /___/ ____/ 
/_/  /_/\____/_/      
```

PyAutoGUI を使った GUI 自動化機能を提供する MCP (Model Context Protocol) サーバーです。
マウス・キーボード操作やスクリーンショット取得に加え、YAML 形式で記述したマルチステップの自動化フローを実行できます。
本アプリケーションはv1.0.0時点ではメインディスプレイでの操作のみ対応しています。

## 機能

* マウスの移動・クリック・ドラッグ操作
* キーボード入力・ショートカットキーの送信
* スクリーンショットの取得と画面サイズの取得
* YAML フローによる複数ステップの一括実行（エラーハンドリング・リトライ・ループ対応）

## ツール一覧

### マウス操作

| ツール名 | 説明 |
|---|---|
| `get_mouse_position` | 現在のマウスカーソル座標を取得 |
| `move_mouse` | 指定座標へマウスを移動 |
| `click` | 現在位置で左クリック |
| `double_click` | 現在位置でダブルクリック |
| `triple_click` | 現在位置でトリプルクリック（行全体の選択など） |
| `hold_mouse_button` | マウスボタンを押し続ける（ドラッグ操作の始点に） |
| `release_mouse_button` | 押し続けているマウスボタンを離す |
| `drag_to` | 現在位置から指定座標までドラッグ |
| `scroll_up` | マウスホイールを上方向にスクロール |
| `scroll_down` | マウスホイールを下方向にスクロール |

### キーボード操作

| ツール名 | 説明 |
|---|---|
| `list_available_keys` | 使用可能なキー名の一覧を取得 |
| `press_key` | 指定したキーを押して離す |
| `press_hotkey` | 複数キーを同時押し（ショートカット） |
| `type_text` | テキストをキーボード入力として送信 |

### 画面操作

| ツール名 | 説明 |
|---|---|
| `get_screen_size` | 画面の解像度（幅・高さ）を取得 |
| `screenshot` | 画面全体のスクリーンショットを JPEG で取得 |

### フロー実行

| ツール名 | 説明 |
|---|---|
| `execute_flow` | YAML 形式で定義した自動化フローを実行 |

#### YAML フローの書き方

```yaml
settings:          # 省略可
  on_error: stop   # stop / continue / retry (デフォルト: stop)
  retry_count: 3   # リトライ回数 (on_error: retry の場合)
  retry_delay: 1.0 # リトライ間隔（秒）
  default_wait: 0.5 # 各ステップ後の待機時間（秒）

steps:
  - action: move_mouse
    params: {x: 100, y: 200}
  - action: click
  - action: type_text
    params: {text: "hello"}
  - action: press_key
    params: {key: enter}
  - action: screenshot
    id: after_submit
    capture: true   # このステップ後にスクリーンショットを保存
```

**フロー制御専用アクション:**

| アクション | パラメータ | 説明 |
|---|---|---|
| `wait` | `seconds` | 指定秒数だけ待機 |
| `repeat` | `count`, `steps` | ステップ群を指定回数繰り返す |

## インストール

### 必要環境

* Python 3.10 以上
* [uv](https://docs.astral.sh/uv/) (推奨) または pip

---

### 方法 1: Wheel ファイルからインストール

[Releases](https://github.com/PNL-toshiyaishihara/EasyAutomationMCP/releases) ページから `.whl` ファイルをダウンロードし、インストールします。

**uv を使う場合（推奨）:**

```bash
uv pip install easy_automation_mcp-1.0.0-py3-none-any.whl
```

**pip を使う場合:**

```bash
pip install easy_automation_mcp-1.0.0-py3-none-any.whl
```

---

### 方法 2: ソースコードからインストール

リポジトリをクローンしてローカルでビルド・インストールします。

```bash
git clone https://github.com/PNL-toshiyaishihara/EasyAutomationMCP.git
cd EasyAutomationMCP

# 依存関係のセットアップ
uv sync

# (オプション) Wheel をビルドして pip インストール
uv build
uv pip install dist/easy_automation_mcp-*.whl
```

## Claude Desktop への設定

設定ファイルの場所:

* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### Wheel インストール済みの場合

```json
{
  "mcpServers": {
    "easy-automation-mcp": {
      "command": "easy-automation-mcp"
    }
  }
}
```

### ソースコードから実行する場合

```json
{
  "mcpServers": {
    "easy-automation-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/EasyAutomationMCP",
        "run",
        "easy-automation-mcp"
      ]
    }
  }
}
```

## 開発

### 依存関係のセットアップ

```bash
uv sync
```

### パッケージのビルド

```bash
uv build
```

### デバッグ

MCP Inspector を使ってツールの動作を確認できます:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/EasyAutomationMCP run easy-automation-mcp
```

ブラウザで表示された URL にアクセスするとデバッグ画面が開きます。

### 使い方のコツ

本ツールはスクリーンショットからエージェントが画面上の座標を推定するため、座標を誤ることがあります。
以下のコツを参考にしてください。

**座標確定の手順（初めての画面を操作するとき）**

1. まず `screenshot` で画面全体を取得し、レイアウトを把握する
2. システムプロンプトで「座標が確定するまで `execute_flow` を使わないこと」と LLM に指示する
3. `move_mouse` → `screenshot` を繰り返して目的の要素にカーソルを合わせる
4. `get_mouse_position` で実際の座標を確認・記録する
5. 座標が確定したら `execute_flow` でまとめて実行する

確定した座標はメモアプリや記憶系サービス（Obsidian, Notionなど）に保存しておくと再利用できます。

> **注意:** Windows の表示スケール（125%・150%など）が有効な環境では、
> PyAutoGUI が取得する座標と実際の画面位置がずれる場合があります。
> その場合は表示スケールを 100% に設定するか、オフセットを考慮してください。

## 注意事項

* PyAutoGUI のフェイルセーフ機能により、マウスを画面の角に移動すると操作が中断されます。
* `type_text` はプリンタブル ASCII 文字のみ対応しています。日本語などの Unicode 文字はクリップボード経由で貼り付けてください。
* `hold_mouse_button` で押し続けている間は `click` / `double_click` / `triple_click` が使えません。先に `release_mouse_button` を呼んでください。

## Roadmap

現在のバージョン: v1.0.0（固定座標ベースのGUI自動化 + YAMLフロー実行）

* Unicode/日本語テキスト入力のネイティブ対応
* YAMLフローの `if` 条件分岐
* フロー変数の導入
* 画像マッチングによるクリック
* OCRによるテキスト認識
* スクリーンショットの領域指定
* フロー録画機能（操作を記録して YAML を自動生成）
* フローライブラリ（フローの保存・呼び出し）
* ウィンドウ管理
* 非同期フロー実行
* ブラウザ自動化の統合
* スケジュール実行

---

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。
