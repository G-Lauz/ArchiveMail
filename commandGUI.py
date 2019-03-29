import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QWidget, QGridLayout, QComboBox, QPushButton,
    QLabel, QVBoxLayout, QButtonGroup, QCheckBox, QFileDialog)

from mycsv import csvManipulator
from dbsqlite import PostulantDB
from appdata import Data

class commandGUI(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        self._db = PostulantDB()
        self._csv = None

        self.initUI()

    def initUI(self):
        self.checkboxLayout = QVBoxLayout()
        self.choiceText = QLabel("Options :")
        self.checkboxLayout.addWidget(self.choiceText)

        self.buttonGroup = QButtonGroup()
        for i, info in enumerate(Data().INFO):
            checkbox = QCheckBox(info, self)
            self.buttonGroup.addButton(checkbox, i)
            self.checkboxLayout.addWidget(checkbox)
        self.buttonGroup.setExclusive(False)

        self.detailLayout = QVBoxLayout()
        self.detailText = QLabel("Détails :")
        self.detailLayout.addWidget(self.detailText)
        self.infoText = QLabel()
        self.infoText.setWordWrap(True)
        self.detailLayout.addWidget(self.infoText)

        self.dateLayout = QVBoxLayout()
        self.dateText = QLabel("Période :")
        self.dateLayout.addWidget(self.dateText)

        self.yearComboBox = QComboBox()
        #self.yearComboBox.addItem("Tout les années")
        for i in self._setYear(self._db.tableList()):
            self.yearComboBox.addItem(i)
        self.dateLayout.addWidget(self.yearComboBox)

        self.monthComboBox = QComboBox()
        self.monthComboBox.addItem("Année entière")
        for i in self._setMonth(self._db.tableList()):
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

        table = self._getTables()

        querry = list()
        for i in self.buttonGroup.buttons():
            if i.isChecked():
                querry.append(Data().DICTINFO[i.text()])

        try:
            self._csv = csvManipulator(filename[0])

            fulldata = []
            for i in table:
                data = self._db.selectThese(i, querry)
                for j in data:
                    fulldata.append(j)

            self._csv.write(fulldata)

        except Exception as e:
            self.infoText.setText("Erreur dans l'exportation des données: \n"
                + str(e))

    def _getTables(self):
        if self.monthComboBox.currentIndex() != 0:
            return [self._db.TABLENAME + self.yearComboBox.currentText()
                + str(Data().DICTMOIS[self.monthComboBox.currentText ()])]
        else:
            alist = []
            for i in self._db.tableList():
                if self.yearComboBox.currentText() in i:
                    alist.append(self._db.TABLENAME +
                        self.yearComboBox.currentText() + i[13:])
            return alist

    def _setYear(self, tables : list):
        seen = set()
        seen_add = seen.add
        for i in tables:
            if i[9:13] not in seen:
                seen_add(i[9:13])
                yield i[9:13]

    def _setMonth(self, tables : list):
        seen = set()
        seen_add = seen.add
        for i in tables:
            if len(seen) == 12:
                return
            if i[13:] not in seen:
                seen_add(i[13:])
                yield Data().MOIS[int(i[13:])-1]
