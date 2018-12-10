# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/strategywidget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StrategyWidget(object):
    def setupUi(self, StrategyWidget):
        StrategyWidget.setObjectName("StrategyWidget")
        StrategyWidget.resize(977, 569)
        self.gridLayout_3 = QtWidgets.QGridLayout(StrategyWidget)
        self.gridLayout_3.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabs = QtWidgets.QTabWidget(StrategyWidget)
        self.tabs.setObjectName("tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(self.tab)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.gridLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dte_to = QtWidgets.QDateTimeEdit(self.gridLayoutWidget)
        self.dte_to.setObjectName("dte_to")
        self.gridLayout_2.addWidget(self.dte_to, 3, 1, 1, 1)
        self.dte_from = QtWidgets.QDateTimeEdit(self.gridLayoutWidget)
        self.dte_from.setObjectName("dte_from")
        self.gridLayout_2.addWidget(self.dte_from, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)
        self.rb_allData = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.rb_allData.setChecked(True)
        self.rb_allData.setObjectName("rb_allData")
        self.gridLayout_2.addWidget(self.rb_allData, 0, 0, 1, 2)
        self.tw_feeds = QtWidgets.QTreeWidget(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tw_feeds.sizePolicy().hasHeightForWidth())
        self.tw_feeds.setSizePolicy(sizePolicy)
        self.tw_feeds.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tw_feeds.setHeaderHidden(True)
        self.tw_feeds.setObjectName("tw_feeds")
        self.tw_feeds.headerItem().setText(0, "1")
        self.gridLayout_2.addWidget(self.tw_feeds, 4, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.rb_timeWindow = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.rb_timeWindow.setObjectName("rb_timeWindow")
        self.gridLayout_2.addWidget(self.rb_timeWindow, 1, 0, 1, 2)
        self.editor = Qsci.QsciScintilla(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editor.sizePolicy().hasHeightForWidth())
        self.editor.setSizePolicy(sizePolicy)
        self.editor.setMinimumSize(QtCore.QSize(300, 0))
        self.editor.setObjectName("editor")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabs.addTab(self.tab, "")
        self.gridLayout_3.addWidget(self.tabs, 0, 0, 1, 1)

        self.retranslateUi(StrategyWidget)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(StrategyWidget)

    def retranslateUi(self, StrategyWidget):
        _translate = QtCore.QCoreApplication.translate
        StrategyWidget.setWindowTitle(_translate("StrategyWidget", "Form"))
        self.dte_to.setDisplayFormat(_translate("StrategyWidget", "dd.MM.yyyy H:mm"))
        self.dte_from.setDisplayFormat(_translate("StrategyWidget", "dd.MM.yyyy H:mm"))
        self.label_2.setText(_translate("StrategyWidget", "To"))
        self.rb_allData.setText(_translate("StrategyWidget", "All data"))
        self.label.setText(_translate("StrategyWidget", "From"))
        self.rb_timeWindow.setText(_translate("StrategyWidget", "Time window"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), _translate("StrategyWidget", "Code"))

from PyQt5 import Qsci
