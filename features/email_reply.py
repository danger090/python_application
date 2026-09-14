"""メール返信文作成機能。"""
import streamlit as st

from core.gemini_client import stream_text


def render() -> None:
    st.header("📧 メール返信文作成")
    st.caption("受信したメールと返信の要点を入力すると、返信文の下書きを作成します。")

    original = st.text_area(
        "受信したメール本文（任意）", height=200, placeholder="相手からのメールを貼り付けてください"
    )
    intent = st.text_area(
        "返信で伝えたいこと（要点）", height=100, placeholder="例: 提案は了承。納期だけ1週間伸ばしてほしい"
    )

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(
            "トーン",
            ["丁寧・ビジネス標準", "フォーマル・かしこまった", "フレンドリー・カジュアル", "簡潔・要点のみ"],
        )
    with col2:
        signature = st.text_input("署名（任意）", placeholder="例: 山田太郎")

    if st.button("返信文を生成", type="primary", disabled=not intent):
        signature_text = f"最後に署名として「{signature}」を入れてください。" if signature else ""
        prompt = f"""あなたは優秀なビジネスアシスタントです。以下の情報からメールの返信文を作成してください。

# 受信したメール
{original or "(内容の指定なし。要点のみから新規に作成)"}

# 返信で伝えたい要点
{intent}

# トーン
{tone}

日本語のビジネスメールとして、宛名・書き出し・本文・結びの挨拶を含めて自然な形で作成してください。
{signature_text}
"""
        with st.spinner("作成中..."):
            try:
                result = st.write_stream(stream_text(prompt, temperature=0.6))
                st.session_state["email_result"] = result
            except RuntimeError as e:
                st.error(str(e))

    if st.session_state.get("email_result"):
        st.download_button(
            "返信文をダウンロード",
            st.session_state["email_result"],
            file_name="email_reply.txt",
        )
