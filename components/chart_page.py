from typing import Tuple

import streamlit as st

import datetime
import FinanceDataReader as fdr


from components.stock_info import get_stock_code_by_company
from components.chart_indicator_form import chart_indicator_form
from components.plot import show_sentiment_analysis
from chart_modules.candle import make_stock_candle
from chart_modules.candle_index import add_indicator_to_candle

def rend_chart_page(company_name: str, selected_dates: Tuple):
    # 우리가 필요로하는 코드조각들
    stock_code = get_stock_code_by_company(company_name) # 종목 코드 받기
    start_date = selected_dates[0].strftime(r"%Y-%m-%d")
    end_date = (selected_dates[1] + datetime.timedelta(days=1)).strftime(r"%Y-%m-%d")

    # 주가 데이터 저장
    st.session_state['ohlcv'] = fdr.DataReader(f'KRX:{stock_code}', start_date, end_date)

    st.header(f"{company_name}의 주가") # 제목 표시
    st.session_state['candle_fig'] = make_stock_candle(company_name) # 캔들차트 생성


    # 캔틀 차트 | 지표 입력창
    chart_container, index_container = st.columns([2, 1], gap="small")

    with index_container:
        chart_indicator_form()

    add_indicator_to_candle()
    print(st.session_state['indicators'])
    with chart_container:
        with st.container():
            # 차트 시각화
            st.plotly_chart(st.session_state.get('candle_fig'))
    
    
    st.header(f"{company_name} 뉴스 데이터")
    show_sentiment_analysis(company_name)


