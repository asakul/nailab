# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/csvdatasourceconfigwidget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CSVDataSourceConfigWidget(object):
    def setupUi(self, CSVDataSourceConfigWidget):
        CSVDataSourceConfigWidget.setObjectName("CSVDataSourceConfigWidget")
        CSVDataSourceConfigWidget.resize(529, 313)
        self.gridLayout = QtWidgets.QGridLayout(CSVDataSourceConfigWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(CSVDataSourceConfigWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.e_path = QtWidgets.QLineEdit(CSVDataSourceConfigWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.e_path.sizePolicy().hasHeightForWidth())
        self.e_path.setSizePolicy(sizePolicy)
        self.e_path.setObjectName("e_path")
        self.gridLayout.addWidget(self.e_path, 0, 1, 1, 1)
        self.b_browse = QtWidgets.QPushButton(CSVDataSourceConfigWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_browse.sizePolicy().hasHeightForWidth())
        self.b_browse.setSizePolicy(sizePolicy)
        self.b_browse.setObjectName("b_browse")
        self.gridLayout.addWidget(self.b_browse, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)

        self.retranslateUi(CSVDataSourceConfigWidget)
        self.b_browse.clicked.connect(CSVDataSourceConfigWidget.browse)
        QtCore.QMetaObject.connectSlotsByName(CSVDataSourceConfigWidget)

    def retranslateUi(self, CSVDataSourceConfigWidget):
        _translate = QtCore.QCoreApplication.translate
        CSVDataSourceConfigWidget.setWindowTitle(_translate("CSVDataSourceConfigWidget", "Form"))
        self.label.setText(_translate("CSVDataSourceConfigWidget", "CSV folder path"))
        self.b_browse.setText(_translate("CSVDataSourceConfigWidget", "..."))

