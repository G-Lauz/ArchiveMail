import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QMenuBar,
    QAction)

import homeGUI
import readGUI

class mainGUI(QMainWindow):

    def __init__(self):
        super(mainGUI, self).__init__()

        self.setWindowTitle("ArchiveMail")

        self.home = homeGUI.homeGUI()
        self.home.userEdited.connect(self.openRead)
        self.setCentralWidget(self.home)

        self.createActions()
        self.createMenus()

    def createActions(self):
        self.newAct = QAction("&New",statusTip="un test", triggered=self.test)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)

    def test(self):
        print("Test")

    @Slot(str)
    def openRead(self, username):
        self.read = readGUI.readGUI(username=username)
        self.setCentralWidget(self.read)
        del self.home

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = mainGUI()
    mainWin.show()
    sys.exit(app.exec_())
