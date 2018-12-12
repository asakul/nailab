# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/newdatasourcedialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewDataSourceDialog(object):
    def setupUi(self, NewDataSourceDialog):
        NewDataSourceDialog.setObjectName("NewDataSourceDialog")
        NewDataSourceDialog.resize(786, 334)
        self.gridLayout = QtWidgets.QGridLayout(NewDataSourceDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.widgets = QtWidgets.QStackedWidget(NewDataSourceDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgets.sizePolicy().hasHeightForWidth())
        self.widgets.setSizePolicy(sizePolicy)
        self.widgets.setObjectName("widgets")
        self.gridLayout.addWidget(self.widgets, 3, 0, 1, 2)
        self.e_sourceName = QtWidgets.QLineEdit(NewDataSourceDialog)
        self.e_sourceName.setObjectName("e_sourceName")
        self.gridLayout.addWidget(self.e_sourceName, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(NewDataSourceDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.cb_sourceType = QtWidgets.QComboBox(NewDataSourceDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_sourceType.sizePolicy().hasHeightForWidth())
        self.cb_sourceType.setSizePolicy(sizePolicy)
        self.cb_sourceType.setObjectName("cb_sourceType")
        self.cb_sourceType.addItem("")
        self.gridLayout.addWidget(self.cb_sourceType, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(NewDataSourceDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewDataSourceDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)

        self.retranslateUi(NewDataSourceDialog)
        self.widgets.setCurrentIndex(-1)
        self.buttonBox.accepted.connect(NewDataSourceDialog.accept)
        self.buttonBox.rejected.connect(NewDataSourceDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewDataSourceDialog)

    def retranslateUi(self, NewDataSourceDialog):
        _translate = QtCore.QCoreApplication.translate
        NewDataSourceDialog.setWindowTitle(_translate("NewDataSourceDialog", "New data source"))
        self.label.setText(_translate("NewDataSourceDialog", "Data source type"))
        self.cb_sourceType.setItemText(0, _translate("NewDataSourceDialog", "CSV"))
        self.label_2.setText(_translate("NewDataSourceDialog", "Data source name"))

