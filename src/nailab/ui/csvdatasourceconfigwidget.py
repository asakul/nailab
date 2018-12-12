
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.csvdatasourceconfigwidget import Ui_CSVDataSourceConfigWidget

class CSVDataSourceConfigWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_CSVDataSourceConfigWidget()
        self.ui.setupUi(self)

    def browse(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select a directory..."), "", QtWidgets.QFileDialog.ShowDirsOnly)
        if dirname != "":
            self.ui.e_path.setText(dirname)
    
