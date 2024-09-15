# src\RAD_trading\backtester\backtester.py
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime


class Backtester:
    def __init__(self):
        self.exchange_rate = 1
        self.commission = 0
        self.swap_long = 0
        self.swap_short = 0
        self.triple_swap_day = 4
        self.slippage = 0
        self.ohlc_data = None
        self.on_bar = None
        self.trades = pd.DataFrame(
            columns=[
                "state",
                "symbol",
                "order_type",
                "tick_volume",
                "open_time",
                "open_price",
                "close_time",
                "close_price",
                "sl",
                "tp",
                "profit",
                "commission",
                "swap",
                "info",
            ]
        )
        self.equity_curve = pd.DataFrame(columns=["time", "equity"])

    def set_starting_balance(self, starting_balance, currency="USD"):
        self.starting_balance = starting_balance
        self.currency = currency

    def set_exchange_rate(self, exchange_rate):
        self.exchange_rate = exchange_rate

    def set_commission(self, commission):
        self.commission = commission

    def set_swaps(self, swap_long, swap_short, triple_swap_day):
        self.swap_long = swap_long
        self.swap_short = swap_short
        self.triple_swap_day = triple_swap_day

    def set_slippage(self, slippage):
        self.slippage = slippage

    def set_historical_data(self, ohlc_data):
        self.ohlc_data = ohlc_data

    def set_on_bar(self, on_bar):
        self.on_bar = on_bar

    def run_backtest(self):
        if self.commission >= 0:
            self.commission = self.commission * -1
        current_balance = self.starting_balance
        for i in self.ohlc_data.index:
            data = self.ohlc_data.loc[i]
            orders = _Orders()
            # Generate Orders
            self.on_bar(data, self.trades, orders)
            for order in orders.orders:
                if order["action"] == "entry":
                    entry_price = self._apply_slippage(
                        data["open"], order["order_type"]
                    )
                    self.trades.loc[len(self.trades), self.trades.columns] = [
                        "open",
                        order["symbol"],
                        order["order_type"],
                        order["tick_volume"],
                        data["time"],
                        entry_price,
                        "",
                        "",
                        order["sl"],
                        order["tp"],
                        0,
                        0,
                        0,
                        order["info"],
                    ]
                elif order["action"] == "exit":
                    exit_price = self._apply_slippage(data["open"], order["order_type"])
                    trade = self.trades.loc[order["trade_id"]]
                    profit = self._calculate_profit(trade, exit_price)
                    commission = self._calculate_commission(trade)
                    swap = self._calculate_swap(trade, data["time"])
                    self.trades.loc[
                        order["trade_id"],
                        [
                            "state",
                            "close_time",
                            "close_price",
                            "profit",
                            "commission",
                            "swap",
                        ],
                    ] = ["closed", data["time"], exit_price, profit, commission, swap]
                    current_balance += profit + commission + swap
                elif order["action"] == "modify_sl":
                    self.trades.loc[order["trade_id"], ["sl"]] = [order["sl"]]
                elif order["action"] == "modify_tp":
                    self.trades.loc[order["trade_id"], ["tp"]] = [order["tp"]]
            open_trades = self.trades[self.trades["state"] == "open"]
            for x in open_trades.index:
                t = open_trades.loc[x]
                if t["order_type"] == "buy":
                    if t["sl"] >= data["low"] and t["sl"] != 0:
                        exit_price = t["sl"]
                        profit = self._calculate_profit(t, exit_price)
                        commission = self._calculate_commission(t)
                        swap = self._calculate_swap(t, data["time"])
                        self.trades.loc[
                            x,
                            [
                                "state",
                                "close_time",
                                "close_price",
                                "profit",
                                "commission",
                                "swap",
                            ],
                        ] = [
                            "closed",
                            data["time"],
                            exit_price,
                            profit,
                            commission,
                            swap,
                        ]
                        current_balance += profit + commission + swap
                    elif t["tp"] <= data["high"] and t["tp"] != 0:
                        exit_price = t["tp"]
                        profit = self._calculate_profit(t, exit_price)
                        commission = self._calculate_commission(t)
                        swap = self._calculate_swap(t, data["time"])
                        self.trades.loc[
                            x,
                            [
                                "state",
                                "close_time",
                                "close_price",
                                "profit",
                                "commission",
                                "swap",
                            ],
                        ] = [
                            "closed",
                            data["time"],
                            exit_price,
                            profit,
                            commission,
                            swap,
                        ]
                        current_balance += profit + commission + swap
                elif t["order_type"] == "sell":
                    if t["sl"] <= data["high"] and t["sl"] != 0:
                        exit_price = t["sl"]
                        profit = self._calculate_profit(t, exit_price)
                        commission = self._calculate_commission(t)
                        swap = self._calculate_swap(t, data["time"])
                        self.trades.loc[
                            x,
                            [
                                "state",
                                "close_time",
                                "close_price",
                                "profit",
                                "commission",
                                "swap",
                            ],
                        ] = [
                            "closed",
                            data["time"],
                            exit_price,
                            profit,
                            commission,
                            swap,
                        ]
                        current_balance += profit + commission + swap
                    elif t["tp"] >= data["low"] and t["tp"] != 0:
                        exit_price = t["tp"]
                        profit = self._calculate_profit(t, exit_price)
                        commission = self._calculate_commission(t)
                        swap = self._calculate_swap(t, data["time"])
                        self.trades.loc[
                            x,
                            [
                                "state",
                                "close_time",
                                "close_price",
                                "profit",
                                "commission",
                                "swap",
                            ],
                        ] = [
                            "closed",
                            data["time"],
                            exit_price,
                            profit,
                            commission,
                            swap,
                        ]
                        current_balance += profit + commission + swap
            self.equity_curve = self.equity_curve.append(
                {"time": data["time"], "equity": current_balance}, ignore_index=True
            )
        # Close all open positions at the end of backtest
        last_time = self.ohlc_data.iloc[-1]["time"]
        last_close = self.ohlc_data.iloc[-1]["close"]
        open_trades = self.trades[self.trades["state"] == "open"]
        for x in open_trades.index:
            t = open_trades.loc[x]
            profit = self._calculate_profit(t, last_close)
            commission = self._calculate_commission(t)
            swap = self._calculate_swap(t, last_time)
            self.trades.loc[
                x,
                ["state", "close_time", "close_price", "profit", "commission", "swap"],
            ] = ["closed", last_time, last_close, profit, commission, swap]
            current_balance += profit + commission + swap
        self.trades["profit_net"] = (
            self.trades["profit"] + self.trades["commission"] + self.trades["swap"]
        )
        self.trades["profit_cumulative"] = self.trades["profit_net"].cumsum()
        self.trades["balance"] = (
            self.trades["profit_cumulative"] + self.starting_balance
        )
        return self.trades

    def _apply_slippage(self, price, order_type):
        slippage_factor = (
            1 + self.slippage if order_type == "buy" else 1 - self.slippage
        )
        return price * slippage_factor

    def _calculate_profit(self, trade, exit_price):
        if trade["order_type"] == "buy":
            return (
                (exit_price - trade["open_price"]) * trade["tick_volume"]
            ) * self.exchange_rate
        elif trade["order_type"] == "sell":
            return (
                (trade["open_price"] - exit_price) * trade["tick_volume"]
            ) * self.exchange_rate

    def _calculate_commission(self, trade):
        return self.commission * trade["tick_volume"]

    def _calculate_swap(self, trade, close_time):
        days_held = (close_time - trade["open_time"]).days
        swap_rate = self.swap_long if trade["order_type"] == "buy" else self.swap_short
        swap = swap_rate * days_held * trade["tick_volume"]
        # Apply triple swap
        triple_swap_days = days_held // 7
        swap += 2 * swap_rate * triple_swap_days * trade["tick_volume"]
        return swap

    def visualize_backtest(self, indicators=[], num_trades=None):
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=("Price", "Equity"),
            row_heights=[0.7, 0.3],
        )
        # Price chart
        fig.add_trace(
            go.Candlestick(
                x=self.ohlc_data["time"],
                open=self.ohlc_data["open"],
                high=self.ohlc_data["high"],
                low=self.ohlc_data["low"],
                close=self.ohlc_data["close"],
                name="OHLC Data",
            ),
            row=1,
            col=1,
        )
        for indicator in indicators:
            fig.add_trace(
                go.Scatter(
                    x=self.ohlc_data["time"],
                    y=self.ohlc_data[indicator],
                    name=indicator,
                ),
                row=1,
                col=1,
            )
        # Equity curve
        fig.add_trace(
            go.Scatter(
                x=self.equity_curve["time"],
                y=self.equity_curve["equity"],
                name="Equity",
            ),
            row=2,
            col=1,
        )
        # Add trade markers
        trades_to_plot = self.trades.tail(num_trades) if num_trades else self.trades
        for i, trade in trades_to_plot.iterrows():
            color = "green" if trade["profit"] > 0 else "red"
            fig.add_shape(
                type="line",
                x0=trade["open_time"],
                y0=trade["open_price"],
                x1=trade["close_time"],
                y1=trade["close_price"],
                line=dict(color=color, width=2),
                row=1,
                col=1,
            )
        fig.update_layout(height=800, title="Backtest Results")
        fig.update_xaxes(rangeslider_visible=False, row=1, col=1)
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Equity", row=2, col=1)
        return fig

    def plot_pnl(self):
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=self.trades["close_time"],
                    y=self.trades["profit_cumulative"],
                    mode="lines",
                )
            ]
        )
        fig.update_layout(
            title="Cumulative PnL", xaxis_title="Time", yaxis_title="Profit/Loss"
        )
        return fig

    def plot_drawdown(self):
        equity_curve = self.trades["balance"]
        previous_peaks = equity_curve.cummax()
        drawdowns = (equity_curve - previous_peaks) / previous_peaks
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=self.trades["close_time"],
                    y=drawdowns,
                    mode="lines",
                    fill="tozeroy",
                )
            ]
        )
        fig.update_layout(title="Drawdown", xaxis_title="Time", yaxis_title="Drawdown")
        return fig

    def calculate_sharpe_ratio(self, risk_free_rate=0.02):
        returns = self.trades["profit_net"] / self.trades["balance"].shift(1)
        excess_returns = returns - risk_free_rate / 252  # Assuming daily returns
        return np.sqrt(252) * excess_returns.mean() / excess_returns.std()

    def calculate_sortino_ratio(self, risk_free_rate=0.02):
        returns = self.trades["profit_net"] / self.trades["balance"].shift(1)
        excess_returns = returns - risk_free_rate / 252
        downside_returns = excess_returns[excess_returns < 0]
        return np.sqrt(252) * excess_returns.mean() / downside_returns.std()

    def calculate_max_drawdown(self):
        equity_curve = self.trades["balance"]
        previous_peaks = equity_curve.cummax()
        drawdowns = (equity_curve - previous_peaks) / previous_peaks
        return drawdowns.min()

    def export_to_json(self, filename, symbol="", indicators=[]):
        data = {
            "symbol": symbol,
            "indicators": indicators,
            "starting_balance": self.starting_balance,
            "exchange_rate": self.exchange_rate,
            "commission": self.commission,
            "swap_long": self.swap_long,
            "swap_short": self.swap_short,
            "triple_swap_day": self.triple_swap_day,
            "slippage": self.slippage,
            "ohlc_history": self.ohlc_data.to_dict("records"),
            "trade_history": self.trades.to_dict("records"),
            "equity_curve": self.equity_curve.to_dict("records"),
        }
        with open(filename, "w") as jsonfile:
            json.dump(data, jsonfile, default=self._json_serial)
        return 1

    @staticmethod
    def _json_serial(obj):
        if isinstance(obj, (datetime, np.datetime64)):
            return obj.isoformat()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")


class _Orders:
    def __init__(self):
        self.orders = []

    def open_trade(self, symbol, tick_volume, order_type, sl=0, tp=0, info={}):
        order = {
            "action": "entry",
            "symbol": symbol,
            "tick_volume": tick_volume,
            "order_type": order_type,
            "sl": sl,
            "tp": tp,
            "info": info,
        }
        self.orders.append(order)

    def close_trade(self, trade):
        order = {
            "action": "exit",
            "trade_id": trade.name,
        }
        self.orders.append(order)

    def modify_sl(self, trade, sl):
        order = {"action": "modify_sl", "trade_id": trade.name, "sl": sl}
        self.orders.append(order)

    def modify_tp(self, trade, tp):
        order = {"action": "modify_tp", "trade_id": trade.name, "tp": tp}
        self.orders.append(order)
