import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QApplication, QStackedWidget, QWidget, QMenuBar,
    QAction)

import gui.homeGUI as homeGUI
import gui.readGUI as readGUI
import gui.commandGUI as commandGUI
import gui.addGUI as addGUI

import utils.log as log

class stackedGUI(QStackedWidget):

    userEdited = Signal(str)

    def __init__(self, parent=None):
        QStackedWidget.__init__(self,parent)
        #super(stackedGUI, self).__init__()

        log.log_init_object(self)

        self.setWindowTitle("ArchiveMail")

        self.home = homeGUI.homeGUI()
        #self.home.userEdited.connect(self.openRead)
        self._connectSignals()
        self.addWidget(self.home)

        self.setCurrentWidget(self.home)

    def __del__(self):
        log.log_del_object(self)

    def __str__(self):
        return str(self.__class__)

    def openCommand(self):
        self.command = commandGUI.commandGUI()
        self.addWidget(self.command)
        self.setCurrentWidget(self.command)

    #def openLire(self):
    #    self.setCurrentWidget(self.read)

    def openAddSite(self):
        self.add = addGUI.addGUI(username=self.username)
        self.addWidget(self.add)
        self.setCurrentWidget(self.add)

    #@Slot(str)
    def openRead(self):
        self.read = readGUI.readGUI()
        self.addWidget(self.read)
        self.setCurrentWidget(self.read)

    def _connectSignals(self):
        self.home.userEdited.connect(self.on_userEdited)

    @Slot(str)
    def on_userEdited(self, user):
        self.openRead()
        self.userEdited.emit(user)
