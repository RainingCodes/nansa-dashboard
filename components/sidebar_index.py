import streamlit as st
import sys
import os

# 현재 파일(sidebar_index.py)의 절대 경로를 얻습니다.
current_file_path = os.path.abspath(__file__)

# components 디렉토리의 경로를 얻습니다.
components_dir = os.path.dirname(current_file_path)

# 루트 디렉토리의 경로를 얻습니다.
project_root_dir = os.path.dirname(components_dir)

# 프로젝트 루트 디렉토리를 sys.path에 추가합니다.
# 이렇게 하면 Python이 my_streamlit_app 디렉토리 안의 모듈들을 찾을 수 있게 됩니다.
sys.path.append(project_root_dir)

from data.get_index import get_financial_indices

indices = get_financial_indices()

def sidebar_indices() -> tuple[str, str, str, str]:
    """
    Streamlit 사이드바에 kospi, kosdaq, usd/krw, nasdaq 지수를 반환합니다.

    Returns:
        tuple: (kospi(str), kosdaq(str), usd/krw(str), nasdaq(str))
    """
    s_kospi = st.sidebar.write(f"KOSPI: {indices['KOSPI']}")
    s_kosdaq = st.sidebar.write(f"KOSDAQ: {indices['KOSDAQ']}")
    s_usdkrw = st.sidebar.write(f"USD/KRW: {indices['USD/KRW']}")
    s_nasdaq = st.sidebar.write(f"NASDAQ: {indices['NASDAQ']}")

    return s_kospi, s_kosdaq, s_usdkrw, s_nasdaq
