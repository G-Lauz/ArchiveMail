import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QWidget, QGridLayout, QComboBox, QPushButton,
    QLabel)

class commandGUI(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

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
        self.exportButton.clicked.connect(lambda x : print("Bouton exporter"))

        layout = QGridLayout()
        layout.addWidget(self.interetText, 0, 0)
        layout.addWidget(self.interetComboBox, 1, 0)
        layout.addWidget(self.dateText, 0, 1)
        layout.addWidget(self.dateComboBox, 1, 1)
        layout.addWidget(self.typeText, 2, 0)
        layout.addWidget(self.typeComboBox, 3, 0)
        layout.addWidget(self.exportButton, 3, 1)
        self.setLayout(layout)
