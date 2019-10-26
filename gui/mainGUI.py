import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QMenuBar,
    QAction)

import gui.stackedGUI as stackedGUI

class mainGUI(QMainWindow):

    userEdited = Signal(str)

    def __init__(self):
        super(mainGUI, self).__init__()

        self.setWindowTitle("ArchiveMail")
        #self.setFixedSize(400,300)

        self.stacked = stackedGUI.stackedGUI()
        self.setCentralWidget(self.stacked)

        self.createActions()
        self.createMenus()
        self._connectSignals()

    def createActions(self):
        self.readAct = QAction("&Lire",statusTip="un test",
            triggered=self.stacked.openRead)
        self.exportAct = QAction("&Exporter",statusTip="un test",
            triggered=self.stacked.openCommand)
        self.addAct = QAction("&Ajouter un site", statusTip="un test",
            triggered=self.stacked.openAddSite)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.readAct)
        self.fileMenu.addAction(self.exportAct)
        self.fileMenu.addAction(self.addAct)

    def _connectSignals(self):
        self.stacked.userEdited.connect(self.on_userEdited)

    def on_userEdited(self, user):
        self.userEdited.emit(user)
