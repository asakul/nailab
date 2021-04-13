# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/settingswindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(SettingsWindow)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.sb_commissionPercentage = QtWidgets.QDoubleSpinBox(SettingsWindow)
        self.sb_commissionPercentage.setDecimals(4)
        self.sb_commissionPercentage.setObjectName("sb_commissionPercentage")
        self.gridLayout.addWidget(self.sb_commissionPercentage, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(SettingsWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(SettingsWindow)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.sb_commissionPerShare = QtWidgets.QDoubleSpinBox(SettingsWindow)
        self.sb_commissionPerShare.setDecimals(4)
        self.sb_commissionPerShare.setObjectName("sb_commissionPerShare")
        self.gridLayout.addWidget(self.sb_commissionPerShare, 1, 1, 1, 1)

        self.retranslateUi(SettingsWindow)
        self.buttonBox.accepted.connect(SettingsWindow.accept)
        self.buttonBox.rejected.connect(SettingsWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Settings"))
        self.label.setText(_translate("SettingsWindow", "Commission (%)"))
        self.label_2.setText(_translate("SettingsWindow", "Commission (per share)"))