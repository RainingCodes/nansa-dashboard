"""gauges.py
============
공포·탐욕 지수(0~100)를 **Plotly** 게이지 차트로 시각화하는 유틸리티.

색상 & 레이블 (CNN Fear & Greed Index 기준)
-------------------------------------------
-  0-20  : Extreme Fear 🟥
- 20-40  : Fear 🟥🟧
- 40-60  : Neutral 🟨
- 60-80  : Greed 🟩
- 80-100 : Extreme Greed 🟩🟢

Example
-------
>>> from modules.gauges import make_fear_greed_gauge
>>> fig = make_fear_greed_gauge(72)
>>> fig.show()
"""
from __future__ import annotations

import plotly.graph_objects as go

# __all__ = ["make_fear_greed_gauge"]

# -----------------------------------------------------------------------------
# 내부 헬퍼: 값 → 레이블 매핑
# -----------------------------------------------------------------------------

def _label(value: int) -> str:
    if value < 20:
        return "Extreme Fear"
    if value < 40:
        return "Fear"
    if value < 60:
        return "Neutral"
    if value < 80:
        return "Greed"
    return "Extreme Greed"


# -----------------------------------------------------------------------------
# 게이지 생성 함수
# -----------------------------------------------------------------------------

def make_fear_greed_gauge(value: float, *, title: str = "Fear & Greed Index") -> go.Figure:  # noqa: D401
    """Fear & Greed Index 값을 게이지 차트로 렌더링.

    Parameters
    ----------
    value : int
        0~100 범위의 지수 값.
    title : str, default "Fear & Greed Index"
        차트 상단 타이틀.

    Returns
    -------
    go.Figure
        Plotly 게이지형 Indicator Figure.
    """
    if not 0 <= value <= 100:
        raise ValueError("value must be between 0 and 100 (inclusive)")

    label = _label(value)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"font": {"size": 20, "weight": "bold", "color": "black"}},
            title={"text": title, "font": {"size": 25}},
            
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "darkgray"},
                "bar": {"color": "rgba(31, 119, 180, 0.8)"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": [
                    {"range": [0, 20], "color": "#d62728"},     # Extreme Fear
                    {"range": [20, 40], "color": "#ff9896"},    # Fear
                    {"range": [40, 60], "color": "#f4d44d"},    # Neutral
                    {"range": [60, 80], "color": "#98df8a"},    # Greed
                    {"range": [80, 100], "color": "#2ca02c"},   # Extreme Greed
                ],
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": value,
                },
            },
        )
    )

    # 현재 구간 텍스트(Extreme Fear / Fear / Neutral / Greed / Extreme Greed) 추가
    fig.add_annotation(
        x=0.5,
        y=0.45,
        xref="paper",
        yref="paper",
        text=label,
        showarrow=False,
        font=dict(size=20, color="black", weight="bold"),
    )

    # Plotly Figure의 전체 배경을 투명하게 설정
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Figure 전체 배경색 (투명)
        plot_bgcolor='rgba(0,0,0,0)'    # Plotting 영역 배경색 (투명)
    )

    return fig