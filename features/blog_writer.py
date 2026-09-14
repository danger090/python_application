"""ブログ記事作成機能。"""
import streamlit as st

from core.gemini_client import stream_text

SEO_SYSTEM_INSTRUCTION = """あなたはSEOに精通したプロのブログライター兼Webマーケターです。
検索エンジンで上位表示されやすく、かつ読者にとって本当に価値のある記事を書くことを常に意識してください。

執筆時は必ず以下のSEOの原則を守ってください。
- 指定されたキーワードを、タイトル・導入文・見出し(H2/H3)・本文に自然な頻度で含める（不自然な詰め込みはしない）
- タイトルは32文字前後を目安に、キーワードをできるだけ前方に配置する
- 導入文（リード文）の最初の2〜3文で、記事が何を扱い、読者のどんな悩みをどう解決するかを明示する
- 見出し(##, ###)は、それだけ読んでも要点が伝わる具体的な文言にする
- 1段落は3〜4文程度までにし、専門用語には簡潔な説明を添える
- 記事の最後に「メタディスクリプション案」として、記事内容を100〜120文字程度で要約した文を1つ追記する
"""


def render() -> None:
    st.header("📝 ブログ記事作成")
    st.caption("テーマや条件を入力すると、AIがブログ記事の下書きを作成します。")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("テーマ・タイトル案", placeholder="例: 在宅ワークの生産性を上げる方法")
        keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）")
        target = st.text_input("想定読者（任意）", placeholder="例: 20代の会社員")
    with col2:
        tone = st.selectbox(
            "文体・トーン",
            ["丁寧・フォーマル", "カジュアル・親しみやすい", "専門的・硬め", "ユーモラス"],
        )
        length = st.select_slider(
            "記事の長さ",
            options=["短め（500字程度）", "標準（1200字程度）", "長め（2000字以上）"],
            value="標準（1200字程度）",
        )
        structure = st.checkbox("見出し（##, ###）付きで構成する", value=True)

    if st.button("記事を生成", type="primary", disabled=not topic):
        structure_text = (
            "Markdownの見出し(##, ###)を使って構成する"
            if structure
            else "見出しなしで自然な文章にする"
        )
        prompt = f"""あなたはプロのブログライターです。以下の条件でブログ記事を執筆してください。

# テーマ
{topic}

# 条件
- 文体・トーン: {tone}
- 長さ: {length}
- 想定読者: {target or "指定なし"}
- 含めたいキーワード: {keywords or "指定なし"}
- 見出し構成: {structure_text}

読者の関心を引く導入、本文、まとめの流れで、日本語で執筆してください。
"""
        with st.spinner("執筆中..."):
            try:
                result = st.write_stream(
                    stream_text(
                        prompt,
                        system_instruction=SEO_SYSTEM_INSTRUCTION,
                        temperature=0.8,
                    )
                )
                st.session_state["blog_result"] = result
            except RuntimeError as e:
                st.error(str(e))

    if st.session_state.get("blog_result"):
        st.download_button(
            "記事をダウンロード（.md）",
            st.session_state["blog_result"],
            file_name="blog_post.md",
        )
