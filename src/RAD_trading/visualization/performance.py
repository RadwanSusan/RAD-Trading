# src\RAD_trading\visualization\performance.py
import plotly.graph_objects as go
def plot_equity_curve(equity_data):
    fig = go.Figure(data=[go.Scatter(x=equity_data.index, y=equity_data, mode='lines')])
    fig.update_layout(title='Equity Curve', xaxis_title='Date', yaxis_title='Equity')
    return fig
def plot_drawdown(drawdown_data):
    fig = go.Figure(data=[go.Scatter(x=drawdown_data.index, y=drawdown_data, mode='lines', fill='tozeroy')])
    fig.update_layout(title='Drawdown', xaxis_title='Date', yaxis_title='Drawdown')
    return fig
