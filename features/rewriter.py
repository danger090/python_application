"""文章校正・リライト機能。"""
import streamlit as st

from core.gemini_client import stream_text

INSTRUCTIONS = {
    "誤字脱字・文法チェックのみ": (
        "誤字脱字・文法上の誤りのみを修正してください。文体や表現は変えないでください。"
        "修正後の全文と、修正点の一覧を示してください。"
    ),
    "自然な文章にリライト": "意味を変えずに、より自然で読みやすい文章にリライトしてください。",
    "もっと丁寧にする": "意味を変えずに、より丁寧でフォーマルな文章にリライトしてください。",
    "もっとカジュアルにする": "意味を変えずに、より親しみやすくカジュアルな文章にリライトしてください。",
    "簡潔にする": "意味を変えずに、冗長な部分を削り簡潔な文章にリライトしてください。",
}


def render() -> None:
    st.header("✨ 文章校正・リライト")
    st.caption("誤字脱字のチェックや、文章の言い回しの改善を行います。")

    text = st.text_area("校正・リライトしたい文章", height=300)
    mode = st.radio("モード", list(INSTRUCTIONS.keys()))

    if st.button("実行", type="primary", disabled=not text):
        prompt = f"""以下の文章について、次の指示に従って処理してください。

# 指示
{INSTRUCTIONS[mode]}

# 対象の文章
{text}
"""
        with st.spinner("処理中..."):
            try:
                result = st.write_stream(stream_text(prompt, temperature=0.4))
                st.session_state["rewrite_result"] = result
            except RuntimeError as e:
                st.error(str(e))

    if st.session_state.get("rewrite_result"):
        st.download_button(
            "結果をダウンロード",
            st.session_state["rewrite_result"],
            file_name="rewrite_result.txt",
        )
