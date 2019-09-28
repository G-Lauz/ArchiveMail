import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QMenuBar,
    QAction)

import gui.stackedGUI as stackedGUI

class mainGUI(QMainWindow):

    def __init__(self):
        super(mainGUI, self).__init__()

        self.setWindowTitle("ArchiveMail")
        #self.setFixedSize(400,300)

        self.stacked = stackedGUI.stackedGUI()
        self.setCentralWidget(self.stacked)

        self.createActions()
        self.createMenus()

    def createActions(self):
        self.readAct = QAction("&Lire",statusTip="un test",
            triggered=self.stacked.openLire)
        self.exportAct = QAction("&Exporter",statusTip="un test",
            triggered=self.stacked.openCommand)
        self.addAct = QAction("&Ajouter un site", statusTip="un test",
            triggered=self.stacked.openAdd)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.readAct)
        self.fileMenu.addAction(self.exportAct)
        self.fileMenu.addAction(self.addAct)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = mainGUI()
    mainWin.show()
    sys.exit(app.exec_())
