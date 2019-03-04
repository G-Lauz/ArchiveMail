import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit
from PySide2.QtCore import QObject, Signal, Slot

class homeGUI(QWidget):

    userEdited = Signal(str)

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        self.userText = QLabel("Username :")

        self.userEdit = QLineEdit("Adresse courriel")
        self.userEdit.editingFinished.connect(self.openCommand)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.userText)
        layout.addWidget(self.userEdit)

        self.setLayout(layout)
        
    @Slot
    def openCommand(self):
        user = self.userEdit.text()
        self.userEdited.emit(user)

    class Communicate(QtCore.QObject):
        speak = Signal(str)
