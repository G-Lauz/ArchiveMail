import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit

import utils.log as log

class homeGUI(QWidget):

    userEdited = Signal(str)

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        log.log_init_object(self)

        self.userText = QLabel("Adresse courriel :")

        self.userEdit = QLineEdit()
        self.userEdit.returnPressed.connect(self.openRead)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.userText)
        layout.addWidget(self.userEdit)
        self.setLayout(layout)

    def __del__(self):
        log.log_del_object(self)

    def __str__(self):
        return str(self.__class__)

    def openRead(self):
        user = self.userEdit.text()
        self.userEdited.emit(user)

    #class Communicate(QtCore.QObject):
        #speak = Signal(str)
