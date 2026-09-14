"""翻訳機能。"""
import streamlit as st

from core.gemini_client import stream_text

LANGUAGES = ["英語", "日本語", "中国語（簡体字）", "韓国語", "フランス語", "スペイン語", "ドイツ語"]


def render() -> None:
    st.header("🌐 翻訳")
    st.caption("文章を指定した言語に翻訳します。トーンの指定も可能です。")

    text = st.text_area("翻訳したい文章", height=200)
    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox("翻訳先の言語", LANGUAGES)
    with col2:
        tone = st.selectbox("トーン", ["自然な標準訳", "ビジネス・フォーマル", "カジュアル・口語的"])

    if st.button("翻訳する", type="primary", disabled=not text):
        prompt = f"""以下の文章を{target_lang}に翻訳してください。

# トーン
{tone}

# 対象の文章
{text}

翻訳結果のみを出力してください。
"""
        with st.spinner("翻訳中..."):
            try:
                result = st.write_stream(stream_text(prompt, temperature=0.3))
                st.session_state["translate_result"] = result
            except RuntimeError as e:
                st.error(str(e))

    if st.session_state.get("translate_result"):
        st.download_button(
            "翻訳結果をダウンロード",
            st.session_state["translate_result"],
            file_name="translation.txt",
        )
