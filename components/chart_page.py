from typing import Tuple

import streamlit as st

import datetime
import FinanceDataReader as fdr
from ta.trend import SMAIndicator


from components.stock_info import get_stock_code_by_company
from chart_modules.candle import make_stock_candle

def rend_chart_page(company_name: str, selected_dates: Tuple):
# 우리가 필요로하는 코드조각들
    stock_code = get_stock_code_by_company(company_name) # 종목 코드 받기
    start_date = selected_dates[0].strftime(r"%Y-%m-%d")
    end_date = (selected_dates[1] + datetime.timedelta(days=1)).strftime(r"%Y-%m-%d")
    price_df = fdr.DataReader(f'KRX:{stock_code}', start_date, end_date)

    # 지표를 위한 컬럼 준비 - sma, std
    # 일단 종가 기준
    price_df['std'] = price_df['Close'].std()
    price_df['sma'] = SMAIndicator(price_df['Close'], window=20).sma_indicator()

    st.header(f"{company_name}의 주가")
    candle_fig = make_stock_candle(company_name, price_df)


    # ───────────────── 3. 레이아웃 ─────────────────
    #      [  왼쪽  ][      오른쪽       ]
    chart_container, index_container = st.columns([2, 1], gap="small")

    with chart_container:
        # 위쪽
        with st.container():
            # 차트 시각화
            st.plotly_chart(
                candle_fig,
                use_container_width=True,
                use_container_height=True,
            )

    with index_container:
        st.text("지표 조작 칸")
    st.text("뉴스 자연어 처리 및 뉴스 링크 칸")


