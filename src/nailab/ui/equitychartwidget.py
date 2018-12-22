
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.equitychartwidget import Ui_EquityChartWidget

class EquityChartWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_EquityChartWidget()
        self.ui.setupUi(self)


    def set_data(self, pnl, drawdown):
        self.ui.chart.set_data(pnl, drawdown)
