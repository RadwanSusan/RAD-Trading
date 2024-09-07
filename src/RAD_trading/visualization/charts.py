# src\RAD_trading\visualization\charts.py
import plotly.graph_objects as go
def plot_ohlc(data, title='OHLC Chart'):
    fig = go.Figure(data=[go.Candlestick(x=data['time'],
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'])])
    fig.update_layout(title=title, xaxis_rangeslider_visible=False)
    return fig
def plot_indicator_overlay(fig, data, column, name, color):
    fig.add_trace(go.Scatter(x=data['time'], y=data[column], name=name, line=dict(color=color)))
    return fig
