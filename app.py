import streamlit as st

from components.stock_info import sidebar_inputs

st.write("난사 대시보드")

# 사이드바에 종목명 입력 -> 
company_name, selected_dates, confirm_btn = sidebar_inputs()


# >>>>> 테스트 코드
import fear_and_greed # 공탐 지수 가져오기 라이브러리
from chart_modules.fear_greed import make_fear_greed_gauge # 공탐지수 게이지차트 시각화 함수 fig 반환

fear_and_greed_index = fear_and_greed.get() # 공탐지수 가져오기
# 공탐 지수 게이지 시각화 fig 오브젝트
fear_greed_gauge = make_fear_greed_gauge(fear_and_greed_index.value)
# streamlit에 띄우기
st.plotly_chart(fear_greed_gauge, use_container_width=True)
# <<<<< 테스트 코드