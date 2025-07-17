import streamlit as st
import sys
import os

from components.stock_info import sidebar_inputs

from components.main_page import rend_main_page
from components.chart_page import rend_chart_page
# components 디렉토리 아래에 있는 sidebar_index 모듈에서 함수를 임포트합니다.
from components.sidebar_index import sidebar_indices
from components.top50_companies import company_list

# ───────────────── 1. 페이지 설정 ─────────────────
st.set_page_config(layout="wide")
st.session_state.setdefault('page', 'main')  # 기본 페이지를 설정
st.session_state.setdefault('indicators', [])
st.session_state.setdefault('delete_btns', [])
st.session_state.setdefault('top50_companies', company_list)

# 사이드바에 종목명 입력 ->
company_name, selected_dates, confirm_btn = sidebar_inputs()
# confirm_btn = sidebar_inputs()


# 사이드바에 코스피, 코스닥, 환율, 나스닥 지수 제시
st.sidebar.markdown("---")
st.sidebar.title("📊 주요 금융 지수")

current_file_path = os.path.abspath(__file__)
project_root_dir = os.path.dirname(current_file_path)

if project_root_dir not in sys.path:
    sys.path.append(project_root_dir)

# 사이드바에 지수를 표시하는 함수를 호출합니다.
sidebar_indices()


# 종목명 입력 후 확인 클릭 시 차트 페이지 로드
if confirm_btn or st.session_state['page'] == 'chart': # 차트 화면 (차트, 지표 조작, 뉴스 정보)
    st.session_state['page'] = 'chart'
    
    selected_company = st.session_state.get('selected_company') if not company_name else company_name
    selected_dates = st.session_state.get('selected_date') if not selected_dates else selected_dates
    
    rend_chart_page(selected_company, selected_dates)
else: # 메인 화면
    rend_main_page()







# 최초에는 캔들차트랑 MA 정도만 보여주고
# 체크박스로 MA, EMA, 볼벨 이런지표를 on/off (지표에 들어가는 수치도 입력받고)