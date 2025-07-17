from typing import Tuple

import streamlit as st
import pandas as pd

"""
차트에 표시할 지표 등 입력 받는 컴포넌트
"""

import plotly.graph_objs as go

def _line_form(defualt_color: str = "#0000FF", default_width: int = 2) -> Tuple[str, int]:
    color, width = st.columns([1, 4])
    with color:
        line_color = st.color_picker("선 색", defualt_color)
    with width:
        line_width = st.slider("선 굵기", min_value=1, max_value=10, value=default_width)
    
    return line_color, line_width

def _del_indicator(index: int):
    # 선택한 인디케이터 삭제
    del st.session_state['indicators'][index]
    del st.session_state['delete_btns'][index]

def _add_delete_btn():
    st.text("지표 삭제")
    
    # 삭제 버튼 띄우기
    for i, indicator in enumerate(st.session_state['indicators']):
        name = indicator['name']
        if name in ['ma', 'ema', 'rsi']:
            name = name.upper()
            period = indicator.get('period')
            btn_label = f"{name} ({period})"
        elif name == 'bollinger':
            period = indicator.get('period')
            std_dev = indicator.get('std_dev')
            btn_label = f"BB ({period}, {std_dev})"

        delete_btn = st.button(
            btn_label, 
            key=f"delete_indicator_btn_{i}",
            on_click=_del_indicator,
            args=[i]
        )
        st.session_state['delete_btns'].append(delete_btn)


def chart_indicator_form():
    st.header("차트 지표 입력")

    MA = '이동평균선(MA)'
    EMA = '지수이동평균선(EMA)'
    BOLLINGER = '볼린저 밴드(BB)'
    RSI = '상대강도지수(RSI)'

    indicator_list = [MA, EMA, RSI, BOLLINGER]
    selectbox, confirm = st.columns([3, 1])
    with selectbox:
        indicator_choice = st.selectbox(
            '지표선택',
            indicator_list,
            key="indicator_choice",
            label_visibility="collapsed" # 라벨 숨기기
        )
    with confirm:
        add_btn = st.button("추가")

    if indicator_choice in [MA, EMA, RSI]: # 이동평균선 & 지수이동평균선 & rsi
        period = st.number_input("기간", min_value=1, max_value=1000, value=20)
        line_color, line_width = _line_form("#0000FF", 2)

        if add_btn:
            indicator_dict = {
                'period': period,
                'line_color': line_color,
                'line_width': line_width
            }
            # 선택한 인디케이터 이름 설정
            if indicator_choice == MA:
                indicator_dict['name'] = 'ma'
            elif indicator_choice == EMA:
                indicator_dict['name'] = 'ema'
            elif indicator_choice == RSI:
                indicator_dict['name'] = 'rsi'

            # session_state에 선택한 인디케이터 저장
            st.session_state['indicators'].append(indicator_dict)

    elif indicator_choice == BOLLINGER: # 볼린저 밴드
        period = st.number_input("기간", min_value=1, max_value=100, value=20)
        std_dev = st.number_input("표준편차", min_value=1, max_value=5, value=2)
        line_color, line_width = _line_form("#0000FF", 2)

        if add_btn:
            indicator_dict = {
                'name': 'bollinger',
                'period': period,
                'std_dev': std_dev,
                'line_color': line_color,
                'line_width': line_width
            }
            # 선택한 인디케이터 저장
            st.session_state['indicators'].append(indicator_dict)

    # 삭제 버튼 추가
    if st.session_state['indicators']:
        _add_delete_btn()