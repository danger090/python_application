"""文章要約機能。"""
import streamlit as st

from core.gemini_client import stream_text


def render() -> None:
    st.header("📄 文章要約")
    st.caption("長い文章を貼り付けると、指定した形式で要約します。")

    text = st.text_area("要約したい文章", height=300)

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("要約の形式", ["段落で要約", "箇条書きで要約", "一言（1文）で要約"])
    with col2:
        length = st.select_slider(
            "要約の分量", options=["とても短く", "短め", "標準", "やや詳しく"], value="標準"
        )

    if st.button("要約する", type="primary", disabled=not text):
        prompt = f"""以下の文章を要約してください。

# 要約の形式
{style}

# 分量の目安
{length}

# 対象の文章
{text}

日本語で、元の文章の意図やニュアンスを損なわないように要約してください。
"""
        with st.spinner("要約中..."):
            try:
                result = st.write_stream(stream_text(prompt, temperature=0.3))
                st.session_state["summary_result"] = result
            except RuntimeError as e:
                st.error(str(e))

    if st.session_state.get("summary_result"):
        st.download_button(
            "要約をダウンロード",
            st.session_state["summary_result"],
            file_name="summary.txt",
        )
