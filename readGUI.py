import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QProgressBar

from emailreader import GmailReader

class readGUI(QWidget):

    def __init__(self, username=None, parent=None):
        QWidget.__init__(self,parent)
        #GmailReader.__init__(self,username=username)

        self.reader = GmailReader(username=username)

        self.readButton = QPushButton("Lire")
        self.readButton.clicked.connect(self.readMail)

        self.progress = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.readButton)
        layout.addWidget(self.progress)
        self.setLayout(layout)

    def readMail(self):
        print("Lecture...")
        self.reader.readMail()
