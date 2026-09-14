# AIライティングツール

Streamlit + Gemini API で作った個人用のAIライティング支援ツールです。データベースや認証は使わず、ローカルで動かすことを想定しています。

## 機能

- 📝 ブログ記事作成
- 📧 メール返信文作成
- 📄 文章要約
- ✨ 文章校正・リライト
- 💡 タイトル・見出し生成
- 📱 SNS投稿文作成（X, Instagram, Threads, Facebook, LinkedIn）
- 🌐 翻訳
- 🔑 キーワード・タグ抽出

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. Gemini APIキーの設定

[Google AI Studio](https://aistudio.google.com/apikey) でAPIキーを取得し、以下のどちらかの方法で設定します。

- `.env.example` を `.env` にコピーし、`GEMINI_API_KEY=取得したキー` を記入する
- アプリ起動後、サイドバーの「API設定」からその都度入力する

### 3. アプリの起動

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` が開きます。

## 技術スタック

- Python
- Streamlit
- Gemini API（`google-genai` SDK）

## ディレクトリ構成

```
app.py                  # エントリーポイント（サイドバー・ページ切り替え）
core/
  gemini_client.py      # Gemini API 呼び出しの共通処理
features/
  blog_writer.py        # ブログ記事作成
  email_reply.py        # メール返信文作成
  summarizer.py         # 文章要約
  rewriter.py           # 校正・リライト
  title_generator.py    # タイトル生成
  sns_post.py           # SNS投稿文作成
  translator.py         # 翻訳
  keyword_extractor.py  # キーワード・タグ抽出
```

新しいライティング機能を追加したい場合は、`features/` に同じ形式（`render()` 関数を持つモジュール）を追加し、`app.py` の `PAGES` に登録してください。
