import streamlit as st

from components.stock_info import (
    get_stock_code_by_company,
    sidebar_inputs
)

st.write("난사 대시보드")

# 사이드바에 종목명 입력 -> 
company_name, selected_dates, confirm_btn = sidebar_inputs()


# >>>>> 테스트 코드 - 공탐지수
import fear_and_greed # 공탐 지수 가져오기 라이브러리
from chart_modules.fear_greed import make_fear_greed_gauge # 공탐지수 게이지차트 시각화 함수 fig 반환

fear_and_greed_index = fear_and_greed.get() # 공탐지수 가져오기
# 공탐 지수 게이지 시각화 fig 오브젝트
fear_greed_gauge = make_fear_greed_gauge(fear_and_greed_index.value)
# streamlit에 띄우기
st.plotly_chart(fear_greed_gauge, use_container_width=True)
# <<<<< 테스트 코드


# >>>>> 테스트코드 - 캔들 차트 with 지표
import datetime
import plotly.graph_objects as go
import FinanceDataReader as fdr
from ta.trend import SMAIndicator

from chart_modules.candle import make_stock_candle

if confirm_btn:
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
    fig = make_stock_candle(company_name, price_df)

    st.plotly_chart(fig)
# <<<<< 테스트코드




# 최초에는 캔들차트랑 MA 정도만 보여주고
# 체크박스로 MA, EMA, 볼벨 이런지표를 on/off (지표에 들어가는 수치도 입력받고)