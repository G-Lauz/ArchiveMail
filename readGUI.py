# -*-coding:utf-8 -*
import sys, traceback
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QProgressBar,
    QLabel)

from emailreader import GmailReader
import threadpool

class readGUI(QWidget, GmailReader):

    def __init__(self, username=None, parent=None):
        QWidget.__init__(self,parent)
        GmailReader.__init__(self,username=username)

        #self.reader = GmailReader(username=username)

        self.updateProgress.connect(self.setProgress)

        self.readButton = QPushButton("Lire")
        self.readButton.clicked.connect(self.read)

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setTextVisible(True)

        self.detailTitle = QLabel("Détails :")

        self.detailText = QLabel(" ")

        layout = QVBoxLayout()
        layout.addWidget(self.readButton)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.detailTitle)
        layout.addWidget(self.detailText)
        self.setLayout(layout)

    def __del__(self):
        print("Destruction : ", self)

    @Slot(float)
    def setProgress(self, progress):
        self.progressBar.setValue(progress)

    @Slot(Exception)
    def setDetails(self, e):
        self.detailText.setText(e)

    def read(self):
        self.readMail(critere="UNSEEN")
        self.detailText.setText("Lecture...")

        def exception_hook(type, value, tb):
            self.detailText.setText(str(value))
        sys.excepthook = exception_hook
