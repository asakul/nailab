# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/equitychartwidget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EquityChartWidget(object):
    def setupUi(self, EquityChartWidget):
        EquityChartWidget.setObjectName("EquityChartWidget")
        EquityChartWidget.resize(618, 433)
        self.gridLayout = QtWidgets.QGridLayout(EquityChartWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.chart = EquityChartCanvas(EquityChartWidget)
        self.chart.setObjectName("chart")
        self.gridLayout.addWidget(self.chart, 0, 0, 1, 1)

        self.retranslateUi(EquityChartWidget)
        QtCore.QMetaObject.connectSlotsByName(EquityChartWidget)

    def retranslateUi(self, EquityChartWidget):
        _translate = QtCore.QCoreApplication.translate
        EquityChartWidget.setWindowTitle(_translate("EquityChartWidget", "Form"))

from ui.equitychartcanvas import EquityChartCanvas
