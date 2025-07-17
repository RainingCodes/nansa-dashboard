"""
st.ssession_state['indicators'] 기반으로 캔들차트에 시각화
"""
import streamlit as st
import plotly.graph_objs as go

from ta.trend import (
    SMAIndicator,
    EMAIndicator
)
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator


def _add_ma(indicator_info):
    df = st.session_state['ohlcv']

    sma = SMAIndicator(
        df['Close'], window=indicator_info['period']
    ).sma_indicator()

    
    st.session_state['candle_fig'].add_trace(
        go.Scatter(
            x=df.index,
            y=sma,
            line_color=indicator_info['line_color'],
            line_width=indicator_info['line_width'],
            name=f"MA ({indicator_info['period']})"
        ), row=1, col=1
    )


def _add_ema(indicator_info):
    df = st.session_state['ohlcv']

    ema = EMAIndicator(
        close=df['Close'],
        window=indicator_info.get('period', 20) # EMA 기본 기간은 SMA와 유사하게 20을 많이 사용
    ).ema_indicator()
    
    ema_go = go.Scatter(
        x=df.index,
        y=ema,
        line_color='blue', # EMA는 보통 다른 색상으로 구분합니다.
        name=f'EMA ({indicator_info.get("period", 20)})',
        showlegend=True,
        mode='lines'
    )

    st.session_state['candle_fig'].add_trace(ema_go, row=1, col=1)

def _add_bollinger(indicator_info):
    df = st.session_state['ohlcv']

    bollinger = BollingerBands(
        close=df['Close'],
        window=indicator_info.get('period', 20),
        window_dev=indicator_info.get('deviation', 2)
    )
    
    upper_band = bollinger.bollinger_hband()
    lower_band = bollinger.bollinger_lband()
    
    bol_upper_go = go.Scatter(
        x=df.index,
        y=upper_band,
        line_color='gray',
        line={'dash': 'dash'},
        name='Upper Band',
        opacity=0.5,
        showlegend=True
    )
    bol_lower_go = go.Scatter(
        x=df.index,
        y=lower_band,
        line_color='gray',
        line={'dash': 'dash'},
        fill='tonexty',
        name='Lower Band',
        opacity=0.5,
        showlegend=True
    )

    st.session_state['candle_fig'].add_traces([bol_upper_go, bol_lower_go], rows=1, cols=1)

def _add_rsi(indicator_info):
    df = st.session_state['ohlcv']

    rsi = RSIIndicator(
        close=df['Close'],
        window=indicator_info.get('period', 14) # RSI 기본 기간은 14
    ).rsi()
    
    rsi_go = go.Scatter(
        x=df.index,
        y=rsi,
        line_color='purple',
        name=f'RSI ({indicator_info.get("period", 14)})',
        showlegend=True,
        mode='lines'
    )

    st.session_state['candle_fig'].add_trace(rsi_go, row=3, col=1)  # RSI는 보통 하단에 표시합니다.

def add_indicator_to_candle():
    # 메인페이지인 경우 스킵
    if st.session_state.get('page') == 'main':
        return
    
    # # 지정된 지표가 없을 경우 스킵
    # if not st.session_state.get('indicators'):
    #     return
    
    for indicator in st.session_state.get('indicators'):
        match indicator['name']:
            case 'ma':
                _add_ma(indicator)
            case 'ema':
                _add_ema(indicator)
            case 'bollinger':
                _add_bollinger(indicator)
            case 'rsi':
                _add_rsi(indicator)

