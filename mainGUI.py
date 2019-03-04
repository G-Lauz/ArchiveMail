import sys
from PySide2 import QtWidgets
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QMenuBar,
    QAction)

import homeGUI

class mainGUI(QMainWindow):

    def __init__(self):
        super(mainGUI, self).__init__()

        self.setFixedSize(400,240)

        #self.home = homeGUI.homeGUI()
        #self.setCentralWidget(self.home)

        self.createActions()
        self.createMenus()

    def createActions(self):
        self.newAct = QAction("&New",statusTip="un test", triggered=self.test)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)

    def test(self):
        print("Test")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = mainGUI()
    mainWin.show()
    sys.exit(app.exec_())
