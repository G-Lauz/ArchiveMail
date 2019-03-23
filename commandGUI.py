import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QWidget, QGridLayout, QComboBox, QPushButton,
    QLabel, QVBoxLayout, QButtonGroup, QCheckBox, QFileDialog)

from mycsv import csvManipulator
from dbsqlite import PostulantDB
import appdata

class commandGUI(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        self._db = None
        self._csv = None

        self.initUI()

    def initUI(self):
        self.checkboxLayout = QVBoxLayout()
        self.choiceText = QLabel("Options :")
        self.checkboxLayout.addWidget(self.choiceText)

        self.buttonGroup = QButtonGroup()
        for i, info in enumerate(appdata.INFO):
            checkbox = QCheckBox(info, self)
            self.buttonGroup.addButton(checkbox, i)
            self.checkboxLayout.addWidget(checkbox)
        self.buttonGroup.setExclusive(False)

        self.detailLayout = QVBoxLayout()
        self.detailText = QLabel("Détails :")
        self.detailLayout.addWidget(self.detailText)
        self.infoText = QLabel()
        self.detailLayout.addWidget(self.infoText)

        self.dateLayout = QVBoxLayout()
        self.dateText = QLabel("Période :")
        self.dateLayout.addWidget(self.dateText)

        self.yearComboBox = QComboBox()
        self.yearComboBox.addItem("Tout les années")
        for i in range(10):     #REVOIR POUR UNE MEILLEUR MODULARITÉ
            self.yearComboBox.addItem(str(2019+i))
        self.dateLayout.addWidget(self.yearComboBox)

        self.monthComboBox = QComboBox()
        self.monthComboBox.addItem("Année entière")
        for i in appdata.MOIS:
            self.monthComboBox.addItem(i)
        self.dateLayout.addWidget(self.monthComboBox)

        self.exportButton = QPushButton("Exporter")
        self.exportButton.clicked.connect(self.exportcsv)

        layout = QGridLayout()
        layout.addLayout(self.checkboxLayout, 0, 0)
        layout.addLayout(self.detailLayout, 1, 0)
        layout.addLayout(self.dateLayout, 0, 1)
        layout.addWidget(self.exportButton, 2, 1)
        self.setLayout(layout)

    def exportcsv(self, filname : str):
        filename = QFileDialog.getSaveFileName(None, "Save F:xile",
            "data/untitled.csv", "*.csv *.db *.xlsx *.odt")

        self._db = PostulantDB()
        self._csv = csvManipulator(filename[0])

        table = (self._db.TABLENAME + self.yearComboBox.currentText()
            + str(self.monthComboBox.currentIndex ()))

        querry = list()
        for i in self.buttonGroup.buttons():
            if i.isChecked():
                querry.append(appdata.DICTINFO[i.text()])
        #try:
        data = self._db.selectThese(table, querry)
        self._csv.write(data)
        #except Exception as e:
        #    self.infoText.setText("Erreur dans l'exportation des données: \n"
        #        + str(e))
        #    print(e)
