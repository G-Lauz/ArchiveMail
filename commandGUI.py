import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QWidget, QGridLayout, QComboBox, QPushButton,
    QLabel)

from mycsv import csvManipulator
from dbsqlite import PostulantDB

class commandGUI(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        self._db = None
        self._csv = None

        self.interetText = QLabel("Interêt :")

        self.interetComboBox = QComboBox()
        self.interetComboBox.addItem("Test 1")
        self.interetComboBox.addItem("Test 2")
        self.interetComboBox.addItem("Test 3")

        self.dateText = QLabel("Mois :")

        self.dateComboBox = QComboBox()
        self.dateComboBox.addItem("Test 1")
        self.dateComboBox.addItem("Test 2")
        self.dateComboBox.addItem("Test 3")

        self.typeText = QLabel("Type :")

        self.typeComboBox = QComboBox()
        self.typeComboBox.addItem("Test 1")
        self.typeComboBox.addItem("Test 2")
        self.typeComboBox.addItem("Test 3")

        self.exportButton = QPushButton("Exporter")
        self.exportButton.clicked.connect(self.exportcsv("test"))

        layout = QGridLayout()
        layout.addWidget(self.interetText, 0, 0)
        layout.addWidget(self.interetComboBox, 1, 0)
        layout.addWidget(self.dateText, 0, 1)
        layout.addWidget(self.dateComboBox, 1, 1)
        layout.addWidget(self.typeText, 2, 0)
        layout.addWidget(self.typeComboBox, 3, 0)
        layout.addWidget(self.exportButton, 3, 1)
        self.setLayout(layout)

    def exportcsv(self, filname : str):
        self._db = PostulantDB()
        self._csv = csvManipulator(filname)
        data = self._db.selectThese(self._db.TABLETODAY, [self._db.EMAIL,
            self._db.PRENOM, self._db.INTERET])
        self._csv.write(data)
