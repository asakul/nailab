
from ui_gen.settingswindow import Ui_SettingsWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class SettingsWindow(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        self.loadSettings()


    def loadSettings(self):
        s = QtCore.QSettings()

        self.ui.sb_commissionPercentage.setValue(float(s.value("commission/percentage", 0)));
        self.ui.sb_commissionPerShare.setValue(float(s.value("commission/per_share", 0)))

    def saveSettings(self):
        s = QtCore.QSettings()
        
        s.setValue("commission/percentage", float(self.ui.sb_commissionPercentage.value()))
        s.setValue("commission/per_share", float(self.ui.sb_commissionPerShare.value()))
