import streamlit as st

from components.stock_info import (
    get_stock_code_by_company,
    sidebar_inputs
)

from components.chart_page import rend_chart_page

import plotly.express as px


# ───────────────── 1. 페이지 설정 ─────────────────
st.set_page_config(layout="wide")

# 사이드바에 종목명 입력 -> 
company_name, selected_dates, confirm_btn = sidebar_inputs()


# 종목명 입력 후 확인 클릭 시 차트 페이지 로드
if confirm_btn: # 차트 화면 (차트, 지표 조작, 뉴스 정보)
    rend_chart_page(company_name, selected_dates)
else: # 메인 화면
    st.header("난사 대시보드")


# # >>>>> 테스트 코드 - 공탐지수
# import fear_and_greed # 공탐 지수 가져오기 라이브러리
# from chart_modules.fear_greed import make_fear_greed_gauge # 공탐지수 게이지차트 시각화 함수 fig 반환

# fear_and_greed_index = fear_and_greed.get() # 공탐지수 가져오기
# # 공탐 지수 게이지 시각화 fig 오브젝트
# fear_greed_gauge = make_fear_greed_gauge(fear_and_greed_index.value)
# # streamlit에 띄우기
# st.plotly_chart(fear_greed_gauge, use_container_width=True)
# # <<<<< 테스트 코드






# 최초에는 캔들차트랑 MA 정도만 보여주고
# 체크박스로 MA, EMA, 볼벨 이런지표를 on/off (지표에 들어가는 수치도 입력받고)