
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.newdatasourcedialog import Ui_NewDataSourceDialog
from ui.csvdatasourceconfigwidget import CSVDataSourceConfigWidget

from data.csvfolderdatasource import CsvFolderDataSource
from data.yahoocsvfolderdatasource import YahooCsvFolderDataSource

class NewDataSourceDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.ui = Ui_NewDataSourceDialog()
        self.ui.setupUi(self)

        index = self.ui.widgets.addWidget(CSVDataSourceConfigWidget())
        self.ui.widgets.setCurrentIndex(index)

    def get_data_source(self):
        if self.ui.cb_sourceType.currentText() == "CSV":
            return CsvFolderDataSource(self.ui.e_sourceName.text(), self.ui.widgets.currentWidget().ui.e_path.text())
        else:
            return YahooCsvFolderDataSource(self.ui.e_sourceName.text(), self.ui.widgets.currentWidget().ui.e_path.text())
