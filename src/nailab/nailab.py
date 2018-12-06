
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from ui.mainwindow import MainWindow

def main():
    QApplication.setOrganizationDomain("kasan.ws")
    QApplication.setOrganizationName("K.A.S.A.N.")
    QApplication.setApplicationName("nailab")
    app = QApplication(sys.argv)

    wnd = MainWindow()
    wnd.show()
    
    return app.exec_()

if __name__ == '__main__':
    main()
