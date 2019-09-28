import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QApplication, QStackedWidget, QWidget, QMenuBar,
    QAction)

import gui.homeGUI as homeGUI
import gui.readGUI as readGUI
import gui.commandGUI as commandGUI
import gui.addGUI as addGUI

class stackedGUI(QStackedWidget):

    def __init__(self):
        super(stackedGUI, self).__init__()

        self.setWindowTitle("ArchiveMail")

        self.home = homeGUI.homeGUI()
        self.home.userEdited.connect(self.openRead)
        self.addWidget(self.home)

        self.setCurrentWidget(self.home)

    def openCommand(self):
        self.command = commandGUI.commandGUI()
        self.addWidget(self.command)
        self.setCurrentWidget(self.command)

    def openLire(self):
        self.setCurrentWidget(self.read)

    def openAdd(self):
        self.add = addGUI.addGUI()
        self.addWidget(self.add)
        self.setCurrentWidget(self.add)

    @Slot(str)
    def openRead(self, username):
        self.username = username
        self.read = readGUI.readGUI(username=username)
        self.addWidget(self.read)
        self.setCurrentWidget(self.read)
