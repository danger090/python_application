"""個人用 AIライティングツール（Streamlit + Gemini API）のエントリーポイント。"""
import streamlit as st
from dotenv import load_dotenv

from core.gemini_client import DEFAULT_MODEL, MODEL_OPTIONS, get_api_key
from features import (
    blog_writer,
    email_reply,
    keyword_extractor,
    rewriter,
    sns_post,
    summarizer,
    title_generator,
    translator,
)

load_dotenv()

st.set_page_config(page_title="AIライティングツール", page_icon="✍️", layout="wide")

PAGES = {
    "📝 ブログ記事作成": blog_writer,
    "📧 メール返信文作成": email_reply,
    "📄 文章要約": summarizer,
    "✨ 文章校正・リライト": rewriter,
    "💡 タイトル・見出し生成": title_generator,
    "📱 SNS投稿文作成": sns_post,
    "🌐 翻訳": translator,
    "🔑 キーワード・タグ抽出": keyword_extractor,
}


def render_sidebar() -> str:
    st.sidebar.title("✍️ AIライティングツール")
    st.sidebar.caption("Gemini APIを使った個人用ライティング支援ツール")
    st.sidebar.divider()

    page_name = st.sidebar.radio("ツールを選択", list(PAGES.keys()))

    st.sidebar.divider()
    with st.sidebar.expander("⚙️ API設定", expanded=not bool(get_api_key())):
        api_key_input = st.text_input(
            "Gemini APIキー",
            type="password",
            value=st.session_state.get("gemini_api_key", ""),
            help="環境変数 GEMINI_API_KEY からも読み込めます。"
            "取得はこちら: https://aistudio.google.com/apikey",
        )
        if api_key_input:
            st.session_state["gemini_api_key"] = api_key_input

        model_label = st.selectbox(
            "使用モデル",
            list(MODEL_OPTIONS.keys()),
            index=list(MODEL_OPTIONS.values()).index(
                st.session_state.get("gemini_model", DEFAULT_MODEL)
            ),
        )
        st.session_state["gemini_model"] = MODEL_OPTIONS[model_label]

    if not get_api_key():
        st.sidebar.warning("APIキーを入力してください。")

    return page_name


def main() -> None:
    page_name = render_sidebar()
    PAGES[page_name].render()


if __name__ == "__main__":
    main()
