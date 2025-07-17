import streamlit as st
import sys
import os

from components.stock_info import sidebar_inputs

from components.chart_page import rend_chart_page
# components 디렉토리 아래에 있는 sidebar_index 모듈에서 함수를 임포트합니다.
from components.sidebar_index import sidebar_indices


# ───────────────── 1. 페이지 설정 ─────────────────
st.set_page_config(layout="wide")
st.session_state.setdefault('page', 'main')  # 기본 페이지를 설정
st.session_state.setdefault('indicators', [])

# 사이드바에 종목명 입력 -> 
company_name, selected_dates, confirm_btn = sidebar_inputs()


# 사이드바에 코스피, 코스닥, 환율, 나스닥 지수 제시

current_file_path = os.path.abspath(__file__)
project_root_dir = os.path.dirname(current_file_path)

if project_root_dir not in sys.path:
    sys.path.append(project_root_dir)

# 사이드바에 지수를 표시하는 함수를 호출합니다.
sidebar_indices()


# 종목명 입력 후 확인 클릭 시 차트 페이지 로드
if confirm_btn or st.session_state['page'] == 'chart': # 차트 화면 (차트, 지표 조작, 뉴스 정보)
    st.session_state['page'] = 'chart'
    rend_chart_page(company_name, selected_dates)
else: # 메인 화면
    st.title(":반짝임: 스마트 주식 분석 대시보드 :반짝임:")
    st.markdown("### 당신의 현명한 투자를 위한 최고의 파트너")
    st.markdown("---") # 구분선 추가
    # 환영 섹션 - 중앙 정렬 및 배경색 강조 (HTML/CSS 사용)
    st.markdown("<h1 style='text-align: center; color: #2E86C1; font-size: 3em;'>환영합니다! :손인사:</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #5D6D7E;'>기업 정보를 한눈에, 스마트하게 분석해보세요.</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True) # 줄 간격 추가
    # 기능 소개 섹션 - 컬럼을 사용하여 레이아웃 분할
    col1, col2, col3 = st.columns([1, 2, 1]) # 이미지, 텍스트, 빈 공간으로 레이아웃 조정
    with col2: # 중앙 컬럼에 기능 설명 배치
        st.subheader(":전구: 주요 기능")
        st.markdown("""
        * **:막대_차트: 실시간 지수 확인**: 왼쪽 사이드바에서 코스피, 코스닥, 환율, 나스닥 등 주요 금융 지수를 실시간으로 확인하세요. 시장의 흐름을 놓치지 마세요!
        * **:상승세인_차트: 상세 주식 차트**: 입력하신 회사의 주가 흐름을 기간별 차트로 시각화하여 제공합니다. 추세 분석이 쉬워집니다.
        * **:신문: 최신 뉴스 분석**: 해당 기업과 관련된 최신 뉴스를 수집하고 키워드를 분석하여 제공합니다. 시장의 반응을 빠르게 읽어보세요.
        """)
        st.info(":왼쪽_화살표: 왼쪽에 있는 검색창에 분석하고 싶은 회사 이름과 기간을 입력하고 확인 버튼 눌러주세요!")

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