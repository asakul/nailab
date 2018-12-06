
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.strategywidget import Ui_StrategyWidget

class StrategyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, content=None):
        super().__init__(parent)

        self.ui = Ui_StrategyWidget()
        self.ui.setupUi(self)

        self.ui.splitter.setSizes([20, 80])
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 1)

        font = QtGui.QFont("DejaVu Sans Mono")
        font.setPointSize(10)
        self.ui.editor.setFont(font)
        if content is not None:
            self.ui.editor.setText(content)

        lexer = QsciLexerPython()
        lexer.setFont(font)
        self.ui.editor.setLexer(lexer)
        self.ui.editor.setUtf8(True)
