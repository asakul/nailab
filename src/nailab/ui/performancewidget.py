
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.performancewidget import Ui_PerformanceWidget

from pathlib import PurePath

import datetime
import json
import numpy as np

class PerformanceWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_PerformanceWidget()
        self.ui.setupUi(self)
        self.trades_series = {}

    def widget_type(self):
        return "performance"

    def dailyToggled(self, v):
        if v:
            self.ui.correlationCanvas.setMode("daily")

    def monthlyToggled(self, v):
        if v:
            self.ui.correlationCanvas.setMode("monthly")

    def addResults(self):
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self, self.tr("Select file to open"), "", self.tr("JSON files (*.json);;All Files (*)"))
        results = []
        for filename in filenames:
            with open(filename, "rt") as f:
                name = PurePath(filename).name
                QtWidgets.QListWidgetItem(name, self.ui.lw_strategies)
                trades = json.loads(f.read())
                for trade in trades:
                    trade["entry_time"] = datetime.datetime.strptime(trade["entry_time"], "%Y-%m-%d %H:%M:%S") 
                    trade["exit_time"] = datetime.datetime.strptime(trade["exit_time"], "%Y-%m-%d %H:%M:%S") 

                self.trades_series[name] = trades
                results.append({"name" : name, "trades" : trades})

        self.ui.canvas.add_trades_series_batched(results)
        self.ui.correlationCanvas.add_trades_series_batched(results)
        self.update_stats()


    def removeResults(self):
        selected_rows = sorted(map(lambda x: self.ui.lw_strategies.row(x), self.ui.lw_strategies.selectedItems()))
        for row in reversed(selected_rows):
            item = self.ui.lw_strategies.takeItem(row)
            self.ui.canvas.remove_trades_series(item.text())
            self.ui.correlationCanvas.remove_trades_series(item.text())

        self.update_stats()

    def update_stats(self):
        self.ui.tw_stats.clear()
        monmean = np.mean(self.ui.canvas.monthly_returns_y)
        monstd = np.std(self.ui.canvas.monthly_returns_y)
        if monstd == 0:
            monz = 0
        else:
            monz = monmean / monstd
        self.add_stat("Monthly mean", monmean)
        self.add_stat("Monthly std. dev.", monstd)
        self.add_stat("Z-Score", monz)

        self.ui.tw_stats.resizeColumnToContents(0)
        self.ui.tw_stats.resizeColumnToContents(1)
        

    def add_stat(self, name, value):
        item = QtWidgets.QTreeWidgetItem(self.ui.tw_stats)
        item.setText(0, name)
        if isinstance(value, str):
            item.setText(1, str)
        elif isinstance(value, float):
            item.setText(1, "{:.3f}".format(value))
        else:
            item.setText(1, str(value))

