"""SNS投稿文作成機能。"""
import streamlit as st

from core.gemini_client import generate_text

PLATFORM_LIMITS = {
    "X（Twitter）": "140字程度に収め、ハッシュタグを2〜3個含める",
    "Instagram": "改行を活かした読みやすい文章にし、最後にハッシュタグを5〜10個つける",
    "Threads": "500字程度までのカジュアルな文章にする",
    "Facebook": "丁寧で少し長めの文章にする",
    "LinkedIn": "ビジネス向けのフォーマルな文章にする",
}


def render() -> None:
    st.header("📱 SNS投稿文作成")
    st.caption("伝えたい内容から、SNSごとに最適化された投稿文を作成します。")

    content = st.text_area("投稿したい内容", height=150, placeholder="例: 新商品のカフェラテを発売しました")
    platforms = st.multiselect("投稿先", list(PLATFORM_LIMITS.keys()), default=["X（Twitter）"])
    tone = st.selectbox("トーン", ["親しみやすい", "フォーマル", "テンション高め・煽り気味", "落ち着いた・上品"])

    if st.button("投稿文を生成", type="primary", disabled=not content or not platforms):
        with st.spinner("生成中..."):
            for platform in platforms:
                prompt = f"""以下の内容から{platform}向けの投稿文を作成してください。

# 内容
{content}

# トーン
{tone}

# {platform}向けの条件
{PLATFORM_LIMITS[platform]}

投稿文のみを出力してください。
"""
                try:
                    result = generate_text(prompt, temperature=0.8)
                    st.subheader(platform)
                    st.text_area(f"{platform}の投稿文", result, height=150, key=f"sns_{platform}")
                except RuntimeError as e:
                    st.error(str(e))
                    break
