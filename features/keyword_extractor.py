"""キーワード・タグ抽出機能。"""
import streamlit as st

from core.gemini_client import generate_text


def render() -> None:
    st.header("🔑 キーワード・タグ抽出")
    st.caption("文章からSEOキーワードやブログのタグ候補を抽出します。")

    text = st.text_area("対象の文章", height=250)
    count = st.slider("抽出する数", 3, 20, 10)

    if st.button("抽出する", type="primary", disabled=not text):
        prompt = f"""以下の文章から、SEOやタグ付けに使える重要なキーワードを{count}個抽出してください。

# 文章
{text}

カンマ区切りのリストとして、重要度が高い順に出力してください。他の説明は不要です。
"""
        with st.spinner("抽出中..."):
            try:
                result = generate_text(prompt, temperature=0.3)
                st.write(result)
                keywords = [k.strip() for k in result.replace("、", ",").split(",") if k.strip()]
                if keywords:
                    st.code(" ".join(f"#{k}" for k in keywords))
            except RuntimeError as e:
                st.error(str(e))
