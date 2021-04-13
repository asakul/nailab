
import os
import importlib
import importlib.util
import inspect
import sys
import traceback

from execution.executor import Executor
from execution.portfolioexecutor import PortfolioExecutor
from data.datasourcemanager import DataSourceManager

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.mainwindow import Ui_MainWindow
from ui.strategywidget import StrategyWidget
from ui.performancewidget import PerformanceWidget
from ui.settingswindow import SettingsWindow

from naiback.strategy import Strategy
from templates.new_strategy import new_strategy_template

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.datasourcemanager = DataSourceManager()
        self.datasourcemanager.load_sources(QtCore.QSettings())

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def savedChanged(self):
        for i in range(0, self.ui.tabs.count()):
            self.update_tab_name(i)

    def newStrategy(self):
        self._makeEditor(content=new_strategy_template)

    def openStrategy(self):
        settings = QtCore.QSettings()
        filename = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Select a file..."), settings.value("open_strategy_path"), self.tr("Python (*.py);;All (*.*, *)"))[0]
        if filename != "":
            with open(filename, "r") as f:
                self._makeEditor(filename, os.path.basename(filename), f.read())
                settings.setValue("open_strategy_path", os.path.dirname(filename))

    def update_tab_name(self, index):
        tabname = os.path.basename(self.ui.tabs.widget(index).source_file)
        if not self.ui.tabs.widget(index).is_saved():
            tabname += " *"
            
        self.ui.tabs.setTabText(index, tabname)

    def saveStrategy(self):
        settings = QtCore.QSettings()
        currentWidget = self.ui.tabs.currentWidget()
        if currentWidget.source_file is None:
            currentWidget.source_file = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Select a file..."), settings.value("save_strategy_path"), self.tr("Python (*.py);;All (*.*, *)"))[0]
            if currentWidget.source_file != "":
                if not currentWidget.source_file.endswith(".py"):
                    currentWidget.source_file += ".py"
                settings.setValue("save_strategy_path", os.path.dirname(currentWidget.source_file))
                self.ui.tabs.setTabText(self.ui.tabs.currentIndex(), os.path.basename(currentWidget.source_file))
        if currentWidget.source_file != "":
            currentWidget.save()

    def saveStrategyAs(self):
        settings = QtCore.QSettings()
        currentWidget = self.ui.tabs.currentWidget()
        new_source_file = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Select a file..."), settings.value("save_strategy_path"), self.tr("Python (*.py);;All (*.*, *)"))[0]
        if new_source_file != "":
            settings.setValue("save_strategy_path", os.path.dirname(currentWidget.source_file))
            self.ui.tabs.setTabText(self.ui.tabs.currentIndex(), os.path.basename(currentWidget.source_file))
            currentWidget.save_as(new_source_file)
        

    def executeStrategy(self):
        source_file = self.ui.tabs.currentWidget().source_file
        executor = Executor()
        selected_feed_ids = self.ui.tabs.currentWidget().get_selected_feeds()
        selected_feeds = []
        for (source_id, feed_id) in selected_feed_ids:
            try:
                selected_feeds.append(self.datasourcemanager.get_source(source_id).get_feed(feed_id))
            except Exception as e:
                self.ui.tabs.currentWidget().setError(traceback.format_exc())

        try:
            result = executor.execute_from_file(source_file, selected_feeds, self.ui.tabs.currentWidget().get_time_window())
            self.ui.tabs.currentWidget().set_result(result)
            self.ui.tabs.currentWidget().setError(self.tr("Successful run"))
        except Exception as e:
            self.ui.tabs.currentWidget().setError(traceback.format_exc())

    def executeStrategyInPortfolioMode(self):
        source_file = self.ui.tabs.currentWidget().source_file
        executor = PortfolioExecutor()
        selected_feed_ids = self.ui.tabs.currentWidget().get_selected_feeds()
        selected_feeds = []
        for (source_id, feed_id) in selected_feed_ids:
            try:
                selected_feeds.append(self.datasourcemanager.get_source(source_id).get_feed(feed_id))
            except Exception as e:
                self.ui.tabs.currentWidget().setError(traceback.format_exc())

        try:
            result = executor.execute_from_file(source_file, selected_feeds, self.ui.tabs.currentWidget().get_time_window())
            self.ui.tabs.currentWidget().set_result(result)
            self.ui.tabs.currentWidget().setError(self.tr("Successful run"))
        except Exception as e:
            self.ui.tabs.currentWidget().setError(traceback.format_exc())
            
    def tabCloseRequested(self, tab_index):
        if self.ui.tabs.widget(tab_index).widget_type() == "strategy":
            self.ui.tabs.widget(tab_index).save_state()
        self.ui.tabs.removeTab(tab_index)

    def showSettingsDialog(self):
        dlg = SettingsWindow(self)
        dlg.exec()
        if dlg.result() == QtWidgets.QDialog.Accepted:
            dlg.saveSettings()

    def performanceAnalysis(self):
        self.ui.tabs.addTab(PerformanceWidget(), self.tr("Performance analysis"))

    def _makeEditor(self, source_file=None, tab_name="Untitled", content=None):
        editor = StrategyWidget(self.datasourcemanager, source_file, self, content)
        self.ui.tabs.addTab(editor, tab_name)
        editor.savedChanged.connect(self.savedChanged)
