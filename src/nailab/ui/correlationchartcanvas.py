
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib

import numpy as np


class CorrelationChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=6, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self.trades_series = {}
        self.mode = "daily"

    def setMode(self, mode):
        if mode not in ["daily", "monthly"]:
            return

        self.mode = mode
        self._refresh()

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

        corr_matrix = np.zeros((len(self.trades_series), len(self.trades_series)))
        x = 0
        y = 0
        names = []
        for n1, trades1 in self.trades_series.items():
            names.append(n1)
            for n2, trades2 in self.trades_series.items():
                corr_matrix[x][y] = self._calc_correlation(trades1, trades2)
                y += 1
            x += 1
            y = 0
                
        ax1 = self.figure.add_subplot(111)
        ax1.imshow(corr_matrix, cmap="BrBG", norm=matplotlib.colors.Normalize(vmin=-1.0, vmax=1.0))
        ax1.set_title("Returns correlation")
        ax1.set_xticks(np.arange(len(names)))
        ax1.set_yticks(np.arange(len(names)))
        ax1.set_xticklabels(names)
        ax1.set_yticklabels(names)
        for i in range(len(self.trades_series)):
            for j in range(len(self.trades_series)):
                col = 'k'
                if corr_matrix[i, j] > 0.7:
                    col = 'w'
                text = ax1.text(j, i, "{:.2f}".format(corr_matrix[i, j]), ha="center", va="center", color=col, fontsize="x-small")

        plt.setp(ax1.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        self.draw()

    def _calc_correlation(self, trades1, trades2):
        t1 = {}
        all_dates = set()
        for trade in trades1:
            all_dates.add(self._trade_date(trade))
            try:
                t1[self._trade_date(trade)] += trade["percentage"]
            except KeyError:
                t1[self._trade_date(trade)] = trade["percentage"]

        t2 = {}
        for trade in trades2:
            all_dates.add(self._trade_date(trade))
            try:
                t2[self._trade_date(trade)] += trade["percentage"]
            except KeyError:
                t2[self._trade_date(trade)] = trade["percentage"]

            
        ret1 = []
        for d in all_dates:
            try:
                ret1.append(t1[d])
            except KeyError:
                ret1.append(0)

        ret2 = []
        for d in all_dates:
            try:
                ret2.append(t2[d])
            except KeyError:
                ret2.append(0)

        mean1 = np.mean(ret1)
        mean2 = np.mean(ret2)
        sigma1 = np.std(ret1)
        sigma2 = np.std(ret2)

        s = 0
        for i in range(len(all_dates)):
            x1 = ret1[i] - mean1
            x2 = ret2[i] - mean2
            s += x1 * x2
        s /= len(all_dates)
        s /= (sigma1 * sigma2)

        return s


    def _trade_date(self, trade):
        if self.mode == "daily":
            return trade["exit_time"].date()
        else:
            return trade["exit_time"].date().replace(day=1)
            
            
            


        
