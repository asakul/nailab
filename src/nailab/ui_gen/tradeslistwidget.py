# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/tradeslistwidget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TradesListWidget(object):
    def setupUi(self, TradesListWidget):
        TradesListWidget.setObjectName("TradesListWidget")
        TradesListWidget.resize(830, 565)
        self.gridLayout = QtWidgets.QGridLayout(TradesListWidget)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.trades = QtWidgets.QTreeWidget(TradesListWidget)
        self.trades.setObjectName("trades")
        self.gridLayout.addWidget(self.trades, 0, 0, 1, 1)

        self.retranslateUi(TradesListWidget)
        QtCore.QMetaObject.connectSlotsByName(TradesListWidget)

    def retranslateUi(self, TradesListWidget):
        _translate = QtCore.QCoreApplication.translate
        TradesListWidget.setWindowTitle(_translate("TradesListWidget", "Form"))
        self.trades.headerItem().setText(0, _translate("TradesListWidget", "D"))
        self.trades.headerItem().setText(1, _translate("TradesListWidget", "Amount"))
        self.trades.headerItem().setText(2, _translate("TradesListWidget", "Security"))
        self.trades.headerItem().setText(3, _translate("TradesListWidget", "Entry time"))
        self.trades.headerItem().setText(4, _translate("TradesListWidget", "Entry price"))
        self.trades.headerItem().setText(5, _translate("TradesListWidget", "Exit time"))
        self.trades.headerItem().setText(6, _translate("TradesListWidget", "Exit price"))
        self.trades.headerItem().setText(7, _translate("TradesListWidget", "PnL"))

