
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.tradeslistwidget import Ui_TradesListWidget

class TradesListWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_TradesListWidget()
        self.ui.setupUi(self)

        self.trades = []


    def set_trades(self, trades):
        self.trades = trades

        self.ui.trades.clear()

        for trade in trades:
            item = QtWidgets.QTreeWidgetItem(self.ui.trades)
            if trade["is_long"]:
                item.setText(0, "L")
            else:
                item.setText(0, "S")

            item.setText(1, trade["security"])
            item.setText(2, str(trade["entry_time"]))
            item.setText(3, str(trade["entry_price"]))
            item.setText(4, str(trade["exit_time"]))
            item.setText(5, str(trade["exit_price"]))
            item.setText(6, str(trade["pnl"]))

