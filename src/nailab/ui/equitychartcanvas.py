
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class EquityChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.pnl_data = None

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def set_data(self, cumulative_pnl):
        self.pnl_data = cumulative_pnl
        self.plot()

    def plot(self):
        if self.pnl_data is not None:
            ax = self.figure.add_subplot(111)
            ax.plot(self.pnl_data, 'r-')
            ax.set_title("Equity")
            self.draw()
