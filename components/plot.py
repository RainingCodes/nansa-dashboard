import os
import streamlit as st
from PIL import Image

def show_sentiment_analysis(company_name: str):
    """
    회사명을 기준으로 감성 분석 이미지(워드클라우드, 파이차트 등)를 표시합니다.
    저장된 이미지 경로: plot/plots/top10/, plot/plots/posneg/
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) 

    image_map = {
        "상위 10% 키워드 워드클라우드": f"plot/plots/top10/wordcloud_headline_keyword_top10p_{company_name}.png",
        "긍정 워드클라우드": f"plot/plots/posneg/wordcloud_positive_{company_name}.png",
        "부정 워드클라우드": f"plot/plots/posneg/wordcloud_negative_{company_name}.png",
        "감성 통합 워드클라우드": f"plot/plots/posneg/wordcloud_sentiment_colored_{company_name}.png",
        "감성 비율 파이 차트": f"plot/plots/posneg/pie_posneg_{company_name}.png",
    }


    # ───────────────────────────────
    # 1. 상위 10% 키워드 (전체 너비)
    # ───────────────────────────────
    title = "상위 10% 키워드 워드클라우드"
    path = os.path.join(base_dir, image_map[title])
    if os.path.exists(path):
        st.subheader(title)
        st.image(Image.open(path), use_container_width=True)
    else:
        st.warning(f"{title} 이미지를 찾을 수 없습니다.\n(경로: {path})")

    # ───────────────────────────────
    # 2. 긍정 / 부정 워드클라우드
    # ───────────────────────────────
    cols1 = st.columns(2)
    for i, title in enumerate(["긍정 워드클라우드", "부정 워드클라우드"]):
        path = os.path.join(base_dir, image_map[title])
        with cols1[i]:
            if os.path.exists(path):
                st.markdown(f"#### {title}")
                st.image(Image.open(path), use_container_width=True)
            else:
                st.warning(f"{title} 이미지를 찾을 수 없습니다.\n(경로: {path})")

    # ───────────────────────────────
    # 3. 감성 통합 / 감성 비율
    # ───────────────────────────────
    cols2 = st.columns([3, 2])  # 왼쪽: 워드클라우드, 오른쪽: 파이차트
    for i, title in enumerate(["감성 통합 워드클라우드", "감성 비율 파이 차트"]):
        path = os.path.join(base_dir, image_map[title])
        with cols2[i]:
            if os.path.exists(path):
                st.markdown(f"#### {title}")
                st.image(Image.open(path), use_container_width=True)
            else:
                st.warning(f"{title} 이미지를 찾을 수 없습니다.\n(경로: {path})")
