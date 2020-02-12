import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton

import utils.log as log

class homeGUI(QWidget):

    userEdited = Signal(str)

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        log.log_init_object(self)

        self.userText = QLabel("Adresse courriel :")

        self.userEdit = QLineEdit()
        self.userEdit.setPlaceholderText("exemple@gmail.com")
        self.button = QPushButton("Continuer")

        self.button.clicked.connect(self.openRead)
        self.userEdit.returnPressed.connect(self.openRead)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.userText)
        layout.addWidget(self.userEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def __del__(self):
        log.log_del_object(self)

    def __str__(self):
        return str(self.__class__)

    def openRead(self):
        log.log_start_method(self, self.openRead)
        user = self.userEdit.text()
        self.userEdited.emit(user)

    #class Communicate(QtCore.QObject):
        #speak = Signal(str)
