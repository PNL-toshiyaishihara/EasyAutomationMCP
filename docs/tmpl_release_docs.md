# Release ドキュメント テンプレート

## Title ルール

```
v{major}.{minor}.{patch} — {リリースの一言テーマ}
```

**例:**
```
v1.0.0 — Initial Release
v1.1.0 — New Flow Controls
v1.0.1 — Bug Fixes
```

**ルール:**
- タグ名は `v1.0.0` 形式（semver + `v` プレフィックス）
- タイトルは `v{バージョン} — {テーマ}` 形式
- テーマは英語・短く・1フレーズ

---

## Release Notes テンプレート

```markdown
## Overview

<!-- このリリースの概要を1〜2文で記載 -->

## What's New

- 

## Bug Fixes

- 

## Breaking Changes

<!-- 破壊的変更がなければ "None" と記載 -->

## Installation

`.whl` ファイルをダウンロードしてインストールしてください。

\```bash
uv pip install easy_automation_mcp-{version}-py3-none-any.whl
\```

詳細は [README](https://github.com/PNL-toshiyaishihara/EasyAutomationMCP#インストール) を参照してください。

## Assets

| ファイル | 説明 |
|---|---|
| `easy_automation_mcp-{version}-py3-none-any.whl` | インストール用 Wheel ファイル |
| `Source code (zip/tar.gz)` | ソースコード |
```
