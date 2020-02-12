import sys, traceback
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QWidget, QGridLayout, QComboBox, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout, QButtonGroup, QCheckBox, QFileDialog,
    QGroupBox, QProgressBar)

from utils.mycsv import csvManipulator
from utils.dbsqlite import PostulantDB
from utils.appdata import Data
import utils.log as log

class commandGUI(QWidget):

    updateProgress = Signal(float)

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

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setTextVisible(True)
        self.detailLayout.addWidget(self.progressBar)
        self.updateProgress.connect(self.setProgress)

        self.detailGroup.setLayout(self.detailLayout)

        self.dateGroup = QGroupBox("Périodes")
        self.dateLayout = QVBoxLayout()

        self.yearComboBox = QComboBox()
        self.yearComboBox.addItem("Toutes les années")
        for i in self._setYear(self._db.tableList()):
            self.yearComboBox.addItem(i)

        self.yearComboBox.currentIndexChanged.connect(self._lock_monthComboBox)
        self.dateLayout.addWidget(self.yearComboBox)

        self.monthComboBox = QComboBox()
        self.monthComboBox.addItem("Année entière")
        for i in self._setMonth(self._db.tableList()):
            self.monthComboBox.addItem(i)
        self.monthComboBox.setEnabled(False)
        self.dateLayout.addWidget(self.monthComboBox)

        self.dateGroup.setLayout(self.dateLayout)

        self.importButton = QPushButton("Importer")
        self.importButton.clicked.connect(self.importcsv)

        self.exportButton = QPushButton("Exporter")
        self.exportButton.clicked.connect(self.exportcsv)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.domaineGroup)
        self.subLayout = QHBoxLayout()
        self.subLayout.addWidget(self.optionsGroup)
        self.subLayout.addWidget(self.dateGroup)
        self.mainLayout.addLayout(self.subLayout)
        self.mainLayout.addWidget(self.detailGroup)
        self.mainLayout.addWidget(self.importButton)
        self.mainLayout.addWidget(self.exportButton)
        self.setLayout(self.mainLayout)

    def _buildComboBox(self, alist):
        log.log_start_method(self, self._buildComboBox)
        for i in alist:
            self.domaineComboBox.addItem(i)

    def _lock_monthComboBox(self, index):
        if index == 0:
            self.monthComboBox.setEnabled(False)
        else:
            self.monthComboBox.setEnabled(True)

    def exportcsv(self, filname : str):
        log.log_start_method(self, self.exportcsv)
        filename = QFileDialog.getSaveFileName(None, "Save File",
            "data/untitled.csv", "*.csv *.db *.xlsx *.odt")

        table = self._getTables()

        querry = list()
        for i in self.buttonGroup.buttons():
            if i.isChecked():
                querry.append(Data().DICTINFO[i.text()])

        self.infoText.setText("Exportation...")
        try:
            self._csv = csvManipulator(filename[0])

            fulldata = [tuple(querry)]

            dataLen = len(table)

            if self.domaineComboBox.currentIndex() == 0:
                for i, value in enumerate(table):
                    data = self._db.selectThese(value, querry)
                    for j in data:
                        fulldata.append(j)
                    self.updateProgress.emit(((i+1)/dataLen)*100)
            else:
                for i, value in enumerate(table):
                    data = self._db.selectAValue(
                        value, "INTERET", self.domaineComboBox.currentText(),
                        col=querry
                    )
                    for j in data:
                        fulldata.append(j)
                    self.updateProgress.emit(((i+1)/dataLen)*100)

            self._csv.write(fulldata)

            self.infoText.setText("Exportation de " + filename[0] + " réussi")

        except Exception as e:
            self.infoText.setText("Erreur dans l'exportation des données: \n"
                + str(e))

            #tb = traceback.format_exc()
            #print(tb)
            log.log_err(
                "\n" +
                str(traceback.format_exception(*sys.exc_info())[1:2]).strip('[\']') +
                "\nIN\n" +
                str(traceback.format_exception(*sys.exc_info())[-2:-1]).strip('[\']')
            )

    def importcsv(self):
        filename = QFileDialog.getOpenFileName(self,
            "Open CSV", "data/", "CSV Files (*.csv)")

        self.infoText.setText("Importation...")
        try:
            self._csv = csvManipulator(filename[0])
            aListOfDict = self._csv.read()
            dataLen = len(aListOfDict)
            for i, value in enumerate(aListOfDict):
                self._storedata(value)
                self.updateProgress.emit(((i+1)/dataLen)*100)

            self.infoText.setText("Importation de " + filename[0] + " réussi")

        except Exception as e:
            self.infoText.setText("Erreur dans l'importation des données: \n"
                + str(e))

            tb = traceback.format_exc()
            #print(tb)
            log.log_err(tb)

    def _storedata(self, adict : dict):
        if adict == None:
            return
        self._db.insert(**adict)

    def _getTables(self):
        alist = []
        tableList = self._db.tableList()

        if self.yearComboBox.currentIndex() != 0:
            if self.monthComboBox.currentIndex() != 0:
                return [self._db.TABLENAME + self.yearComboBox.currentText()
                    + str(Data().DICTMOIS[self.monthComboBox.currentText ()])]
            else:
                for i in tableList:
                    if self.yearComboBox.currentText() in i:
                        alist.append(self._db.TABLENAME +
                        self.yearComboBox.currentText() + i[13:])
                return alist
        else:
            return tableList


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

    @Slot(float)
    def setProgress(self, progress):
        self.progressBar.setValue(progress)
