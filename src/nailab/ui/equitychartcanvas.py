
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class EquityChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.pnl_data = None
        self.drawdown_data = None

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

    def set_data(self, cumulative_pnl, drawdown):
        self.pnl_data = cumulative_pnl
        self.drawdown_data = drawdown
        self.plot()

    def plot(self):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        if self.pnl_data is not None:
            ax = self.figure.add_subplot(111)
            ax.plot(self.pnl_data, "b-")
            ax2 = ax.twinx()
            ax2.plot(self.drawdown_data, "r-")
            ax.set_title("Equity & drawdown")
            self.draw()
