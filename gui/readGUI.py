# -*-coding:utf-8 -*
import sys, traceback
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QProgressBar,
    QLabel, QGroupBox)

from utils.emailreader import GmailReader
import utils.log as log

class readGUI(QWidget):
    sig_readMail = Signal(str, str)
    updateProgress = Signal(float)

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        #self.updateProgress.connect(self.setProgress)
        log.log_init_object(self)

        self.readButton = QPushButton("Lire")
        self.readButton.clicked.connect(self.read)

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setTextVisible(True)

        self.detailGroup = QGroupBox("Détails")
        self.detailLayout = QVBoxLayout()
        self.detailText = QLabel(" ")
        self.detailText.setWordWrap(True)
        self.detailLayout.addWidget(self.detailText)
        self.detailGroup.setLayout(self.detailLayout)

        layout = QVBoxLayout()
        layout.addWidget(self.readButton)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.detailGroup)
        self.setLayout(layout)

        self._connectSignals()

    def __del__(self):
        log.log_del_object(self)

    def __str__(self):
        return str(self.__class__)

    def _connectSignals(self):
        self.updateProgress.connect(self.setProgress)

    @Slot(float)
    def setProgress(self, progress):
        self.progressBar.setValue(progress)
        if progress == 100:
            self.detailText.setText("Lecture terminé!")

    @Slot(Exception)
    def setDetails(self, e):
        self.detailText.setText(e)

    def read(self):
        log.log_start_method(self, self.read)
        self.sig_readMail.emit('INBOX','UNSEEN')
        self.detailText.setText("Lecture...")

        def exception_hook(type, value, tb):
            self.detailText.setText(str(value) + '\n' + "--------------------\n"
                + str(traceback.format_exception(type,value,tb)[-2:-1]).strip())
        sys.excepthook = exception_hook
