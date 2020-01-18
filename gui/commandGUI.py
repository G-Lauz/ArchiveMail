import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QWidget, QGridLayout, QComboBox, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout, QButtonGroup, QCheckBox, QFileDialog,
    QGroupBox)

from utils.mycsv import csvManipulator
from utils.dbsqlite import PostulantDB
from utils.appdata import Data
import utils.log as log

class commandGUI(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        log.log_init_object(self)

        self._db = PostulantDB()
        self._csv = None

        self.initUI()

    def __del__(self):
        log.log_del_object(self)

    def __str__(self):
        return str(self.__class__)

    def initUI(self):

        self.domaineGroup = QGroupBox("Domaines")
        self.domaineLayout = QVBoxLayout()
        self.domaineComboBox = QComboBox()
        self._buildComboBox([
            "Tout les domaines",
            "Administration soutien et services",
            "Genie",
            "Metiers manuels",
            "Operations tactiques et securite",
            "Soins de la sante",
            "Technologies"
        ])
        self.domaineLayout.addWidget(self.domaineComboBox)
        self.domaineGroup.setLayout(self.domaineLayout)

        self.optionsGroup = QGroupBox("Options")
        self.checkboxLayout = QVBoxLayout()
        self.buttonGroup = QButtonGroup()
        for i, info in enumerate(Data().INFO):
            checkbox = QCheckBox(info, self)
            self.buttonGroup.addButton(checkbox, i)
            self.checkboxLayout.addWidget(checkbox)
        self.buttonGroup.setExclusive(False)
        self.optionsGroup.setLayout(self.checkboxLayout)

        self.detailGroup = QGroupBox("Détails")
        self.detailLayout = QVBoxLayout()
        self.infoText = QLabel()
        self.infoText.setWordWrap(True)
        self.detailLayout.addWidget(self.infoText)
        self.detailGroup.setLayout(self.detailLayout)

        self.dateGroup = QGroupBox("Périodes")
        self.dateLayout = QVBoxLayout()

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

        self.dateGroup.setLayout(self.dateLayout)

        self.exportButton = QPushButton("Exporter")
        self.exportButton.clicked.connect(self.exportcsv)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.domaineGroup)
        self.subLayout = QHBoxLayout()
        self.subLayout.addWidget(self.optionsGroup)
        self.subLayout.addWidget(self.dateGroup)
        self.mainLayout.addLayout(self.subLayout)
        self.mainLayout.addWidget(self.detailGroup)
        self.mainLayout.addWidget(self.exportButton)
        self.setLayout(self.mainLayout)

    def _buildComboBox(self, alist):
        log.log_start_method(self, self._buildComboBox)
        for i in alist:
            self.domaineComboBox.addItem(i)

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

            if self.domaineComboBox.currentIndex() == 0:
                for i in table:
                    data = self._db.selectThese(i, querry)
                    for j in data:
                        fulldata.append(j)
            else:
                for i in table:
                    data = self._db.selectAValue(
                        i, "INTERET", self.domaineComboBox.currentText(),
                        col=querry
                    )
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
