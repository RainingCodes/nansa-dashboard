import os
import streamlit as st
from PIL import Image

def show_sentiment_analysis(company_name: str):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    image_map = {
        "상위 10% 키워드 워드클라우드": f"plot/plots/top10/wordcloud_headline_keyword_top10p_{company_name}.png",
        "긍정 워드클라우드": f"plot/plots/posneg/wordcloud_positive_{company_name}.png",
        "부정 워드클라우드": f"plot/plots/posneg/wordcloud_negative_{company_name}.png",
        "감성 통합 워드클라우드": f"plot/plots/posneg/wordcloud_sentiment_colored_{company_name}.png",
        "감성 비율 파이 차트": f"plot/plots/posneg/pie_posneg_{company_name}.png",
    }

    def load_image(path):
        if os.path.exists(path):
            return Image.open(path)
        return None

    st.title(f"{company_name} 뉴스 데이터")

    # 1. 상위 10% 워드클라우드 (넓게 1열 전체 사용)
    title = "상위 10% 키워드 워드클라우드"
    path = os.path.join(base_dir, image_map[title])
    st.subheader(title)
    image = load_image(path)
    if image:
        st.image(image, width=700)  # use_container_width=False로 고정 크기
    else:
        st.warning(f"{title} 이미지를 찾을 수 없습니다.")

    # 2. 긍정 / 부정 나란히

    col1, col2 = st.columns([1, 1], gap="small")
    for col, title in zip([col1, col2], ["긍정 워드클라우드", "부정 워드클라우드"]):
        path = os.path.join(base_dir, image_map[title])
        image = load_image(path)
        with col:
            st.markdown(f"**{title}**")
            if image:
                st.image(image, width=350)
            else:
                st.warning(f"{title} 이미지를 찾을 수 없습니다.")

    # 3. 감성 통합 / 파이 차트 나란히

    col3, col4 = st.columns([1, 1], gap="small")
    for col, title in zip([col3, col4], ["감성 통합 워드클라우드", "감성 비율 파이 차트"]):
        path = os.path.join(base_dir, image_map[title])
        image = load_image(path)
        with col:
            st.markdown(f"**{title}**")
            if image:
                st.image(image, width=400 if "파이" not in title else 300)
            else:
                st.warning(f"{title} 이미지를 찾을 수 없습니다.")
