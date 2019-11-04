
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.tradeslistwidget import Ui_TradesListWidget

import json
import math

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

    def exportToFile(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, self.tr("Select output file"), "", self.tr("JSON files (*.json);;All Files (*)"))
        with open(filename, "wt") as f:
            output = []
            for trade in self.trades:
                if trade["is_long"]:
                    p = 100.0 * (trade["exit_price"] / trade["entry_price"] - 1)
                    log_ret = math.log(trade["exit_price"] / trade["entry_price"])
                else:
                    p = 100.0 * (trade["entry_price"] / trade["exit_price"] - 1)
                    log_ret = math.log(trade["entry_price"] / trade["exit_price"])
                t = { "pnl" : trade["pnl"],
                      "percentage" : p,
                      "log_return" : log_ret,
                      "entry_time" : trade["entry_time"].strftime("%Y-%m-%d %H:%M:%S"),
                      "exit_time" : trade["exit_time"].strftime("%Y-%m-%d %H:%M:%S") }
                output.append(t)
            f.write(json.dumps(output, indent=4, sort_keys=True))

            

