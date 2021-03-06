# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/statisticwidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StatisticWidget(object):
    def setupUi(self, StatisticWidget):
        StatisticWidget.setObjectName("StatisticWidget")
        StatisticWidget.resize(548, 418)
        self.gridLayout = QtWidgets.QGridLayout(StatisticWidget)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(StatisticWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tw_byTicker = QtWidgets.QTreeWidget(self.tab)
        self.tw_byTicker.setObjectName("tw_byTicker")
        self.gridLayout_2.addWidget(self.tw_byTicker, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tw_seasonality = QtWidgets.QTreeWidget(self.tab_2)
        self.tw_seasonality.setObjectName("tw_seasonality")
        self.gridLayout_3.addWidget(self.tw_seasonality, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(StatisticWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(StatisticWidget)

    def retranslateUi(self, StatisticWidget):
        _translate = QtCore.QCoreApplication.translate
        StatisticWidget.setWindowTitle(_translate("StatisticWidget", "StatisticWidget"))
        self.tw_byTicker.setSortingEnabled(True)
        self.tw_byTicker.headerItem().setText(0, _translate("StatisticWidget", "Ticker"))
        self.tw_byTicker.headerItem().setText(1, _translate("StatisticWidget", "Net profit"))
        self.tw_byTicker.headerItem().setText(2, _translate("StatisticWidget", "Total trades"))
        self.tw_byTicker.headerItem().setText(3, _translate("StatisticWidget", "Avg. return"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("StatisticWidget", "By ticker"))
        self.tw_seasonality.setSortingEnabled(True)
        self.tw_seasonality.headerItem().setText(1, _translate("StatisticWidget", "Net profit"))
        self.tw_seasonality.headerItem().setText(2, _translate("StatisticWidget", "Total trades"))
        self.tw_seasonality.headerItem().setText(3, _translate("StatisticWidget", "Avg. return"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("StatisticWidget", "Seasonal"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("StatisticWidget", "Returns"))
