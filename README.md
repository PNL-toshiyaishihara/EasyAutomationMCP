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

### インストール手順

```bash
pip install easy-automation-mcp
```

または `uv` を使う場合:

```bash
uv add easy-automation-mcp
```

## Claude Desktop への設定

設定ファイルの場所:

* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### 公開パッケージを使う場合

```json
{
  "mcpServers": {
    "easy-automation-mcp": {
      "command": "uvx",
      "args": [
        "easy-automation-mcp"
      ]
    }
  }
}
```

### ローカルソースから使う場合

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
