from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.statisticwidget import Ui_StatisticWidget

import math

def calc_ratio(a, b):
    if b != 0:
        return a / b
    else:
        return 0

class StatisticWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_StatisticWidget()
        self.ui.setupUi(self)

        self.trades = []


    def set_trades(self, trades):
        self.trades = trades

        self.update_statistic()

    def update_statistic(self):

        self.update_by_ticker()
        self.update_seasonality()

    def update_by_ticker(self):
        self.ui.tw_byTicker.clear()
        by_ticker = {}
        for trade in self.trades:
            try:
                by_ticker[trade["security"]].append(trade)
            except KeyError:
                by_ticker[trade["security"]] = [trade]

        for ticker, trades in by_ticker.items():
            item = QtWidgets.QTreeWidgetItem(self.ui.tw_byTicker)
            stats = self.calc_stats(trades)
            item.setText(0, ticker)
            item.setText(1, "{:.4f}".format(stats["net_profit"]))
            item.setText(2, "{}".format(stats["total_trades"]))
            item.setText(3, "{:.2f}%".format(stats["avg_percentage"]))


    def calc_stats(self, trades):
        net_profit = 0
        sum_percentage = 0
        for trade in trades:
            sum_percentage += trade["profit_percentage"]
            net_profit += trade["pnl"]

        return { "net_profit" : net_profit,
                 "total_trades" : len(trades),
                 "avg_percentage" : calc_ratio(sum_percentage, len(trades)) }
            

    def update_seasonality(self ):
        self.ui.tw_seasonality.clear()

        by_weekday = {}
        by_monthday = {}
        by_month = {}

        for trade in self.trades:
            try:
                by_weekday[trade["entry_time"].date().isoweekday()].append(trade)
            except KeyError:
                by_weekday[trade["entry_time"].date().isoweekday()] = [trade]

            try:
                by_monthday[trade["entry_time"].date().day].append(trade)
            except KeyError:
                by_monthday[trade["entry_time"].date().day] = [trade]

            try:
                by_month[trade["entry_time"].date().month].append(trade)
            except KeyError:
                by_month[trade["entry_time"].date().month] = [trade]

        item_by_weekday = QtWidgets.QTreeWidgetItem(self.ui.tw_seasonality)
        item_by_weekday.setText(0, "By weekday")
        for weekday, trades in sorted(by_weekday.items()):
            item = QtWidgets.QTreeWidgetItem(item_by_weekday)
            stats = self.calc_stats(trades)
            item.setText(0, "{}".format(weekday))
            item.setText(1, "{:.4f}".format(stats["net_profit"]))
            item.setText(2, "{}".format(stats["total_trades"]))
            item.setText(3, "{:.2f}%".format(stats["avg_percentage"]))

        item_by_monthday = QtWidgets.QTreeWidgetItem(self.ui.tw_seasonality)
        item_by_monthday.setText(0, "By day-of-month")
        for monthday, trades in sorted(by_monthday.items()):
            item = QtWidgets.QTreeWidgetItem(item_by_monthday)
            stats = self.calc_stats(trades)
            item.setText(0, "{:02d}".format(monthday))
            item.setText(1, "{:.4f}".format(stats["net_profit"]))
            item.setText(2, "{}".format(stats["total_trades"]))
            item.setText(3, "{:.2f}%".format(stats["avg_percentage"]))

        item_by_month = QtWidgets.QTreeWidgetItem(self.ui.tw_seasonality)
        item_by_month.setText(0, "By month")
        for month, trades in sorted(by_month.items()):
            item = QtWidgets.QTreeWidgetItem(item_by_month)
            stats = self.calc_stats(trades)
            item.setText(0, "{:02d}".format(month))
            item.setText(1, "{:.4f}".format(stats["net_profit"]))
            item.setText(2, "{}".format(stats["total_trades"]))
            item.setText(3, "{:.2f}%".format(stats["avg_percentage"]))

