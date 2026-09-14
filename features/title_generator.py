"""タイトル・見出し生成機能。"""
import streamlit as st

from core.gemini_client import generate_text


def render() -> None:
    st.header("💡 タイトル・見出し生成")
    st.caption("記事の内容やキーワードから、複数のタイトル案を生成します。")

    content = st.text_area("記事の内容・概要 または本文", height=200)
    count = st.slider("生成する案の数", 3, 15, 8)
    style = st.multiselect(
        "含めたいスタイル（任意）",
        ["数字を入れる", "疑問形", "感嘆・煽り気味", "SEOを意識したシンプルな形式"],
        default=[],
    )

    if st.button("タイトル案を生成", type="primary", disabled=not content):
        style_text = "・" + "\n・".join(style) if style else "特になし"
        prompt = f"""以下の内容をもとに、記事のタイトル案を{count}個、日本語で提案してください。

# 内容
{content}

# 条件
{style_text}

番号付きの箇条書きでタイトル案のみを出力してください。
"""
        with st.spinner("生成中..."):
            try:
                result = generate_text(prompt, temperature=0.9)
                st.markdown(result)
            except RuntimeError as e:
                st.error(str(e))
