import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QProgressBar,
    QLabel)

from emailreader import GmailReader

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

    @Slot(float)
    def setProgress(self, progress):
        self.detailText.setText(str(progress))
        self.progressBar.setValue(progress)

    def read(self):
        self.readMail()
