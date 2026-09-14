# セキュリティチェックレポート — 2026-09-13

対象: `app.py`, `core/`, `features/`（アプリのコード全体）
ツール: `pip-audit` 2.10.1 / `bandit` 1.9.4 / 独自パターンスキャン（`.claude/skills/security-check/scripts/scan.py`）

## サマリー

| チェック項目 | 結果 |
|---|---|
| 依存パッケージの既知の脆弱性（pip-audit） | ✅ 検出なし |
| 静的解析（bandit） | ✅ 検出なし（408行スキャン） |
| ハードコードされたAPIキー・シークレット | ✅ 検出なし |
| 危険な関数呼び出し（eval/exec/os.system等） | ✅ 検出なし |
| 広すぎるexcept節 | ✅ 検出なし |
| `.gitignore` に `.env` が含まれているか | ✅ 含まれている |
| `.env` ファイルの存在 | ℹ️ 存在しない（`.env.example` のみ） |

自動チェックでは深刻な問題は見つかりませんでした。以下は自動チェックでは拾えない、コードの設計を読んだ上での所見です。

## 所見（手動レビュー）

### 1. Gemini SDKの未捕捉例外がブラウザにスタックトレースを表示しうる（Low）

`core/gemini_client.py` の `generate_text` / `stream_text` は APIキー未設定時のみ `RuntimeError` を送出し、各 `features/*.py` はこの `RuntimeError` だけを `try/except` で捕捉しています（`CLAUDE.md` に明記された意図的な設計）。しかしGemini SDK（`google-genai`）がネットワークエラーや認証エラーなどで送出する他の例外型は捕捉されないため、Streamlitのデフォルト設定では未処理例外がブラウザにフルスタックトレースとして表示されます。

ローカル・単一ユーザー・認証なし運用という前提では実害は小さいですが、内部ファイルパスやライブラリ内部構造が画面に出る点は留意事項として記録します。対応するなら `features/*.py` 側ではなく `core/gemini_client.py` 側で共通の例外ラップを追加するのが、既存の「`RuntimeError`のみ捕捉する」規約と整合的です。

### 2. ユーザー入力がそのままプロンプトに埋め込まれる設計（Info）

全 `features/*.py` はユーザー入力を f-string でそのままGeminiへのプロンプトに埋め込んでいます（`CLAUDE.md` に明記された規約どおり）。単一ユーザーがローカルで自分の入力に対して使う分にはリスクはほぼありませんが、将来的に複数ユーザーで共有する／出力を別の自動処理に渡す、といった使い方に拡張する場合は、プロンプトインジェクションの入口になる点を認識しておく必要があります。現状のスコープでは対応不要と判断します。

### 3. APIキーの取り扱いは想定どおり（問題なし）

`get_api_key()` は `st.session_state` → 環境変数 `GEMINI_API_KEY` の順で読み、UI側は `type="password"` でマスクしています。ディスクへの永続化は `.env`（`.gitignore` 済み）経由のみで、コード中にハードコードされたキーもありません。設計どおりです。

### 4. `requirements.txt` は下限のみ指定（Info）

`streamlit>=1.38` のように下限のみのバージョン指定のため、新規インストール時は常に最新版が入り、セキュリティパッチも自動的に取り込まれます。裏を返すと今回の `pip-audit` 結果は「現在インストールされているバージョン」に対するスナップショットに過ぎないため、依存パッケージを更新した際は再スキャンを推奨します。

## 生ログ

<details>
<summary>pip-audit</summary>

```
No known vulnerabilities found
```
</details>

<details>
<summary>bandit</summary>

```
Run started:2026-09-13 12:22:40
Test results:
	No issues identified.
Code scanned:
	Total lines of code: 408
	Total lines skipped (#nosec): 0
Run metrics:
	Total issues (by severity): Undefined: 0, Low: 0, Medium: 0, High: 0
```
</details>
