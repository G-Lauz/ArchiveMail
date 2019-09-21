import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit

class homeGUI(QWidget):

    userEdited = Signal(str)

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        self.userText = QLabel("Adresse courriel :")

        self.userEdit = QLineEdit()
        self.userEdit.returnPressed.connect(self.openRead)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.userText)
        layout.addWidget(self.userEdit)
        self.setLayout(layout)

    def openRead(self):
        user = self.userEdit.text()
        self.userEdited.emit(user)

    class Communicate(QtCore.QObject):
        speak = Signal(str)
