# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 712)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setObjectName("gridLayout")
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setTabsClosable(True)
        self.tabs.setObjectName("tabs")
        self.gridLayout.addWidget(self.tabs, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1050, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuBacktest = QtWidgets.QMenu(self.menubar)
        self.menuBacktest.setObjectName("menuBacktest")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpenTrades = QtWidgets.QAction(MainWindow)
        self.actionOpenTrades.setObjectName("actionOpenTrades")
        self.actionNew_strategy = QtWidgets.QAction(MainWindow)
        self.actionNew_strategy.setObjectName("actionNew_strategy")
        self.actionOpen_strategy = QtWidgets.QAction(MainWindow)
        self.actionOpen_strategy.setObjectName("actionOpen_strategy")
        self.actionExecute = QtWidgets.QAction(MainWindow)
        self.actionExecute.setObjectName("actionExecute")
        self.menuFile.addAction(self.actionNew_strategy)
        self.menuFile.addAction(self.actionOpen_strategy)
        self.menuBacktest.addAction(self.actionExecute)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuBacktest.menuAction())

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(-1)
        self.actionOpen_strategy.triggered.connect(MainWindow.openStrategy)
        self.tabs.tabCloseRequested['int'].connect(MainWindow.tabCloseRequested)
        self.actionNew_strategy.triggered.connect(MainWindow.newStrategy)
        self.actionExecute.triggered.connect(MainWindow.executeStrategy)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Nailab"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuBacktest.setTitle(_translate("MainWindow", "Backtest"))
        self.actionOpenTrades.setText(_translate("MainWindow", "Open..."))
        self.actionNew_strategy.setText(_translate("MainWindow", "New strategy"))
        self.actionOpen_strategy.setText(_translate("MainWindow", "Open strategy"))
        self.actionExecute.setText(_translate("MainWindow", "Execute"))

