# src/RAD_trading/visualization/performance.py

import plotly.graph_objects as go


def plot_equity_curve(equity_curve):
    fig = go.Figure(
        data=[go.Scatter(x=equity_curve.index, y=equity_curve, mode="lines")]
    )
    fig.update_layout(title="Equity Curve", xaxis_title="Date", yaxis_title="Equity")
    return fig.to_json()


def plot_drawdown(equity_curve):
    peak = equity_curve.cummax()
    drawdown = (equity_curve - peak) / peak
    fig = go.Figure(
        data=[go.Scatter(x=drawdown.index, y=drawdown, mode="lines", fill="tozeroy")]
    )
    fig.update_layout(title="Drawdown", xaxis_title="Date", yaxis_title="Drawdown")
    return fig.to_json()
