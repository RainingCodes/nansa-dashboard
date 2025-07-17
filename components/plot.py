import os
import json
import streamlit as st
from PIL import Image

def show_sentiment_analysis(company_name: str):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # 이미지 경로 맵
    image_map = {
        "상위 10% 키워드 워드클라우드": f"plot/plots/top10/wordcloud_headline_keyword_top10p_{company_name}.png",
        "긍정 워드클라우드": f"plot/plots/posneg/wordcloud_positive_{company_name}.png",
        "부정 워드클라우드": f"plot/plots/posneg/wordcloud_negative_{company_name}.png",
        "감성 비율 파이 차트": f"plot/plots/posneg/pie_posneg_{company_name}.png",
    }

    def load_image(path):
        if os.path.exists(path):
            return Image.open(path)
        return None

    # 최신 뉴스 로드
    news_path = os.path.join(base_dir, "data", "company_latest_news.json")
    news_items = []
    if os.path.exists(news_path):
        with open(news_path, "r", encoding="utf-8") as f:
            news_data = json.load(f)
            news_items = news_data.get(company_name, [])[:5]  # 최대 5개만

    # 1. 상위 10% 워드클라우드 + 최신 뉴스 나란히
    st.subheader("📰 상위 키워드 및 최신 뉴스")
    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown("#### 🔠 상위 10% 키워드 워드클라우드")
        path = os.path.join(base_dir, image_map["상위 10% 키워드 워드클라우드"])
        image = load_image(path)
        if image:
            st.image(image, width=500)
        else:
            st.warning("워드클라우드 이미지를 찾을 수 없습니다.")

    with col2:
        st.markdown("#### 🗞️ 최신 뉴스 (5개)")
        if news_items:
            for news in news_items:
                title = news.get("title", "제목 없음")
                link = news.get("link", "#")
                st.markdown(f"- [{title}]({link})", unsafe_allow_html=True)
        else:
            st.info(f"'{company_name}' 관련 뉴스가 없습니다.")

    # 2. 긍정 / 부정 / 파이차트 나란히
    st.subheader("😊 감성 분석 시각화")
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")
    for col, title in zip([col1, col2, col3], ["긍정 워드클라우드", "부정 워드클라우드", "감성 비율 파이 차트"]):
        path = os.path.join(base_dir, image_map[title])
        image = load_image(path)
        with col:
            st.markdown(f"**{title}**")
            if image:
                st.image(image, width=300)
            else:
                st.warning(f"{title} 이미지를 찾을 수 없습니다.")
