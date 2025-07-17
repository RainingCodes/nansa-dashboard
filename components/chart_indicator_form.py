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
        line_width = st.slider("선 굵기", min_value=1, max_value=10, value=2)
    
    return line_color, line_width

def chart_indicator_form():
    st.header("차트 지표 입력")

    indicator_choice = st.radio("지표 선택", ["이동평균선", "볼린저 밴드"], key="indicator_choice")

    match indicator_choice:
        case "이동평균선":
            period = st.number_input("이동평균선 기간", min_value=1, max_value=100, value=20)
            line_color, line_width = _line_form("#0000FF", 2)

            confirm_btn = st.button("추가")

            if confirm_btn:
                indicator_dict = {
                    'name': 'ma',
                    'period': period,
                    'line_color': line_color,
                    'line_width': line_width
                }
                # session_state에 선택한 인디케이터 저장
                st.session_state['indicators'].append(indicator_dict)

        case "볼린저 밴드":
            period = st.number_input("볼린저 밴드 기간", min_value=1, max_value=100, value=20)
            std_dev = st.number_input("표준편차", min_value=1, max_value=5, value=2)
            line_color, line_width = _line_form("#0000FF", 2)

            confirm_btn = st.button("추가")

            if confirm_btn:
                indicator_dict = {
                    'name': 'bollinger',
                    'period': period,
                    'std_dev': std_dev,
                    'line_color': line_color,
                    'line_width': line_width
                }
                # 선택한 인디케이터 저장
                st.session_state['indicators'].append(indicator_dict)