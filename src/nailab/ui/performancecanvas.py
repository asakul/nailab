
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np


class PerformanceCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self.trades_series = {}


    def add_trades_series(self, name, trades):
        self.trades_series[name] = trades
        self._refresh()

    def add_trades_series_batched(self, trades_list):
        for series in trades_list:
            self.trades_series[series["name"]] = series["trades"]
        self._refresh()

    def remove_trades_series(self, name):
        del self.trades_series[name]
        self._refresh()

    def _refresh(self):
        self.fig.clear()

        if len(self.trades_series) == 0:
            return

        all_trades = []
        for k, v in self.trades_series.items():
            for trade in v:
                all_trades.append(trade)

        all_trades = sorted(all_trades, key=lambda x: x["exit_time"])

        cumpnl = np.cumsum(list(map(lambda x: x["percentage"], all_trades)))

        max_equity = 0
        drawdown = []
        for x in cumpnl:
            if x > max_equity:
                max_equity = x
                drawdown.append(0)
            else:
                drawdown.append(x - max_equity)

        monthly_returns = {}
        cur_month = None
        cur_pnl = 0
        
        for trade in all_trades:
            trade_month = trade["exit_time"].strftime("%Y-%m")
            if trade_month != cur_month and cur_month is not None:
                monthly_returns[cur_month] = cur_pnl
                cur_pnl = 0
                cur_month = trade_month
            if cur_month is None:
                cur_month = trade_month
            cur_pnl += trade["percentage"]
            
        monthly_returns[cur_month] = cur_pnl
        monthly_returns_raw = []
        for k, v in monthly_returns.items():
            monthly_returns_raw.append((k, v))

        monthly_returns_raw = sorted(monthly_returns_raw, key=lambda x: x[0])
        self.monthly_returns_x = list(map(lambda x: x[0], monthly_returns_raw))
        self.monthly_returns_y = list(map(lambda x: x[1], monthly_returns_raw))

        ax1 = self.figure.add_subplot(211)
        ax1.plot(cumpnl, "b-")
        ax1.set_title("Cumulative PnL")
        ax1_2 = ax1.twinx()
        ax1_2.plot(drawdown, "r-")

        ax2 = self.figure.add_subplot(212)
        ax2.bar(self.monthly_returns_x, self.monthly_returns_y)
        ax2.set_title("Monthly PnL")
        plt.setp(ax2.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor")
        self.draw()
