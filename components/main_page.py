import datetime

import streamlit as st

from components.chart_page import rend_chart_page
if 'top50_companies' not in st.session_state:
    from components.top50_companies import company_list
    st.session_state['top50_companies'] = company_list

def _change_page_state_to_chart(company_name: str):
    st.session_state['page'] = 'chart'
    st.session_state['selected_company'] = company_name
    print("호출 되나??", st.session_state['selected_company'])
    today = datetime.date.today()
    jan_1 = datetime.date(today.year, 1, 1)
    st.session_state['selected_date'] = (jan_1, today)


def rend_main_page():
    left_col, right_col = st.columns([1.5, 1])  # 왼쪽 사이드바와 오른쪽 메인 콘텐츠 영역


    with left_col:
        # 메인 페이지에 사용법 안내 및 기능 소개
        st.title("✨ 스마트 주식 분석 대시보드 ✨")
        st.markdown("### 당신의 현명한 투자를 위한 최고의 파트너")
        st.markdown("---") # 구분선 추가

        # 환영 섹션 - 중앙 정렬 및 배경색 강조 (HTML/CSS 사용)
        st.markdown("<h1 style='text-align: center; color: #2E86C1; font-size: 3em;'>환영합니다! 👋</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #5D6D7E;'>기업 정보를 한눈에, 스마트하게 분석해보세요.</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True) # 줄 간격 추가
        
        # 기능 소개 섹션
        st.subheader("💡 주요 기능")
        st.markdown("""
        * **📊 지수 확인**: 왼쪽 사이드바에서 코스피, 코스닥, 환율, 나스닥 등 주요 금융 지수를 확인하세요. 시장의 흐름을 놓치지 마세요!
        
        * **📈 상세 주식 차트**: 입력하신 회사의 주가 흐름을 기간별 차트로 시각화하여 제공합니다. 추세 분석이 쉬워지겠죠!
                    
        * **📰 최신 뉴스 분석**: 해당 기업과 관련된 최신 뉴스를 수집하고 키워드를 분석하여 제공합니다. 시장의 반응을 빠르게 읽어보세요!
        """)
        st.info("⬅️ 왼쪽에 있는 검색창에 분석하고 싶은 회사 이름과 기간을 입력하고 확인 버튼 눌러주세요!")
        st.info("➡️ 오른쪽에 있는 버튼을 눌러서 종목 정보를 확인하세요!")
    
    with right_col: # 오른쪽 컬럼에 이미지 배치
        st.header("시가 총액 상위 50위 종목")
        col1, col2 = st.columns(2)

        for i, company_name in enumerate(st.session_state['top50_companies'], start=1):
            if i % 2 == 1:
                with col1:
                    st.button(
                        f"{i} - {company_name}",  # 사용자에게는 "1 - 삼성전자"로 보이게
                        key=f"top50_{i}",
                        on_click=_change_page_state_to_chart,
                        args=[company_name]  # 실제 넘기는 값은 "삼성전자"만
                    )
            else:
                with col2:
                    st.button(
                        f"{i} - {company_name}",
                        key=f"top50_{i}",
                        on_click=_change_page_state_to_chart,
                        args=[company_name]
                    )

    # if st.session_state.get('page') == 'chart':
    #     company_name = st.session_state.get('selected_company')
    #     selected_dates = st.session_state.get('selected_date')

    #     # 유효성 검사
    #     if company_name is not None and selected_dates is not None:
    #         rend_chart_page(company_name, selected_dates)
    #     else:
    #         st.error("회사명이나 날짜가 설정되지 않았습니다.")