
import os
import importlib
import importlib.util
import inspect

from execution.executor import Executor
from naiback.data.feeds.genericcsvfeed import GenericCSVFeed

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.mainwindow import Ui_MainWindow
from ui.strategywidget import StrategyWidget

from naiback.strategy import Strategy

def is_strategy(obj):
    return inspect.isclass(obj) and Strategy in inspect.getmro(obj)[1:]

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.sources = []

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def openTrades(self):
        pass

    def newStrategy(self):
        self._makeEditor()

    def openStrategy(self):
        settings = QtCore.QSettings()
        filename = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Select a file..."), settings.value("open_strategy_path"), self.tr("Python (*.py);;All (*.*, *)"))[0]
        if filename != "":
            with open(filename, "r") as f:
                self._makeEditor(filename, os.path.basename(filename), f.read())
                settings.setValue("open_strategy_path", os.path.dirname(filename))

    def executeStrategy(self):
        source_file = self.sources[self.ui.tabs.currentIndex()]
        executor = Executor()
        result = executor.execute_from_file(source_file, [])
        print(result)

#        spec = importlib.util.spec_from_file_location("m", source_file)
#        mod = importlib.util.module_from_spec(spec)
#        spec.loader.exec_module(mod)
#        classes = inspect.getmembers(mod, is_strategy)
#        strategy_class = classes[0][0]
       
        
    def tabCloseRequested(self, tab_index):
        del self.sources[tab_index]
        self.ui.tabs.removeTab(tab_index)

    def _makeEditor(self, source_file=None, tab_name="Untitled", content=None):
        editor = StrategyWidget(self, content)
        self.sources.append(source_file)
        self.ui.tabs.addTab(editor, tab_name)
