import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QMenuBar,
    QAction)

import gui.stackedGUI as stackedGUI

import utils.log as log
import utils.appdata as appdata

class mainGUI(QMainWindow):
    #Define signal
    userEdited = Signal(str)
    sig_readMail = Signal(str, str)
    updateProgress = Signal(float)
    sig_getMsgList = Signal()
    sig_receivedMsgList = Signal(appdata.Array)

    aboutToClose = Signal()

    def __init__(self, parent=None):
        super(mainGUI, self).__init__(parent)

        log.log_init_object(self)

        self.setWindowTitle("ArchiveMail")
        #self.setFixedSize(400,300)

        self.stacked = stackedGUI.stackedGUI()
        self.setCentralWidget(self.stacked)

        self.createActions()
        self.createMenus()
        self._connectSignals()

    def __del__(self):
        log.log_del_object(self)

    def __str__(self):
        return str(self.__class__)

    def closeEvent(self,event):
        self.aboutToClose.emit()
        event.accept()

    def createActions(self):
        self.readAct = QAction("&Lire",statusTip="un test",
            triggered=self.stacked.openRead)
        self.exportAct = QAction("&Exporter / Importer",statusTip="un test",
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
        self.stacked.sig_readMail.connect(self.on_sig_readMail)
        self.stacked.sig_getMsgList.connect(self.on_getMsgList)

        self.sig_receivedMsgList.connect(self.on_receivedMsgList)
        self.updateProgress.connect(self.on_updateProgress)

    def on_userEdited(self, user):
        log.log_start_method(self, self.on_userEdited)
        self.userEdited.emit(user)

    def on_sig_readMail(self, select=None, critere=None):
        log.log_start_method(self, self.on_sig_readMail)
        self.sig_readMail.emit(select, critere)

    def on_updateProgress(self, progress):
        log.log_start_method(self, self.on_updateProgress)
        self.stacked.updateProgress.emit(progress)

    def on_getMsgList(self):
        log.log_start_method(self, self.on_getMsgList)
        self.sig_getMsgList.emit()

    def on_receivedMsgList(self, alist):
        log.log_start_method(self, self.on_receivedMsgList)
        self.stacked.sig_receivedMsgList.emit(alist)
