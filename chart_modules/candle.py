import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import iplot
from plotly.subplots import make_subplots

import streamlit as st

def make_stock_candle(company_name: str):
    df = st.session_state.get('ohlcv')

    # Create subplots with 2 rows; top for candlestick price, and bottom for bar volume
    fig = make_subplots(
        rows = 3, cols = 1, shared_xaxes = True,
        subplot_titles = (company_name, 'Volume'),
        vertical_spacing = 0.1,
        row_width = [0.2, 0.2, 0.7]
    )
    # ----------------
    # Candlestick Plot
    fig.add_trace(
        go.Candlestick(
            # 컬럼명 예외처리 추가 하면 좋음
            x = df.index,
            open = df['Open'],
            high = df['High'],
            low = df['Low'],
            close = df['Close'], showlegend=False,
            name = 'candlestick'
        ), row = 1, col = 1
    )

 
    # ----------------
    # Volume Plot
    fig.add_trace(
        go.Bar(
            x = df.index,
            y = df['Volume'],
            showlegend=False
        ), row = 2, col = 1
    )
    # Remove range slider; (short time frame)
    fig.update(layout_xaxis_rangeslider_visible=False)

    # Stock data has gaps in dates, specifically in weekends and holidays
    # create a list of dates that are NOT included from start to end
    date_gaps = [date for date in pd.date_range(start = '2025-04-01', end = '2025-07-15') if date not in df.index.values]
    
    # Update Xaxes
    # rangebreaks에 전달되는 날짜를 제거해서 연속으로 보여줌
    fig.update_xaxes(rangebreaks = [dict(values = date_gaps)])

    return fig