
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

            item.setText(1, str(trade["size"]))
            item.setText(2, trade["security"])
            item.setText(3, str(trade["entry_time"]))
            item.setText(4, "{:.4f}".format(trade["entry_price"]))
            item.setText(5, str(trade["exit_time"]))
            item.setText(6, "{:.4f}".format(trade["exit_price"]))
            item.setText(7, "{:.4f}".format(trade["pnl"]))

            if trade["pnl"] > 0:
                brush = QtGui.QBrush(QtGui.QColor(180, 255, 180))
            else:
                brush = QtGui.QBrush(QtGui.QColor(255, 180, 180))
                
            for i in range(0, 8):
                item.setBackground(i, brush)

