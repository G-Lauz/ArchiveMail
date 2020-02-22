import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtGui import QIntValidator
from PySide2.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QMessageBox, QComboBox, QLineEdit, QScrollArea, QMessageBox,
    QGroupBox)

from utils.emailreader import GmailReader
import utils.log as log
import utils.appdata as appdata
from utils.myxml import xmlManipulator

class ScrollQLabel(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        log.log_init_object(self)

        self.content = QWidget()
        self.lay = QVBoxLayout(self.content)
        self.lay.addStretch()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.content)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll)

        #self.layout().addWidget(scroll, 0,0,1, self.layout().columnCount())
        self.setStyleSheet("QScrollArea{min-width:300 px; min-height: 400px}")

    def __del__(self):
        log.log_del_object(self)

    def __str__(self):
        return str(self.__class__)

    def delList(self):
        while self.lay.count():
            item = self.lay.itemAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            self.lay.removeWidget(widget)
            if widget:
                widget.setParent(None)

    def setList(self, list):
        self.delList()
        for i, item in enumerate(list):
            self.lay.insertWidget(i, QLabel(str(i) + " ..... "+ item))
            #self.lay.count() -1

class ClickableLineEdit(QLineEdit):
    clicked = Signal()

    def mousePressEvent(self, event):
        super(ClickableLineEdit, self).mousePressEvent(event)
        self.clicked.emit()

class addGUI(QWidget):
    sig_getMsgList = Signal()
    sig_receivedMsgList = Signal(appdata.Array)

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        log.log_init_object(self)

        self.msgList = []
        self.messages_dict = None
        self.reader = GmailReader() #   Reader agent

        self.sites = xmlManipulator('site.xml')

        self.initUI()
        self._connectSignals()

    def __del__(self):
        log.log_del_object(self)

    def initUI(self):
        # Layout principal
        self.layout = QVBoxLayout()

        # Layout de la barre de recherche de courriel
        self.searchGroup = QGroupBox("Exemple de courriel à ouvrir:")
        self.searchLayout = QVBoxLayout()

        self.mailsComboBox = QComboBox()
        self.searchLayout.addWidget(self.mailsComboBox)
        self.searchGroup.setLayout(self.searchLayout)


        self.layout.addWidget(self.searchGroup)


        self.fieldGroup = QGroupBox("Infos:")
        # Layout de sélection de ligne
        self.selectionLayout = QHBoxLayout()

        # Layout des champs à entrer
        self.descriptionLayout = QVBoxLayout()
        self.champLayout = QVBoxLayout()

        # Layout individuelle des champs
        #self.emailLayout = QHBoxLayout()
        self.emailText = QLabel("Email:")
        self.emailBar = ClickableLineEdit()
        self.emailBar.clicked.connect(self.emailBar.clear)
        self.emailBar.setPlaceholderText("# de ligne")
        self.emailBar.setValidator(QIntValidator(0,1024,None))
        #self.emailLayout.addWidget(self.emailText)
        #self.emailLayout.addWidget(self.emailBar)
        self.descriptionLayout.addWidget(self.emailText)
        self.champLayout.addWidget(self.emailBar)
        #self.champLayout.addLayout(self.emailLayout)

        #self.prenomLayout = QHBoxLayout()
        self.prenomText = QLabel("Prenom:")
        self.prenomBar = ClickableLineEdit()
        self.prenomBar.clicked.connect(self.prenomBar.clear)
        self.prenomBar.setPlaceholderText("# de ligne")
        self.prenomBar.setValidator(QIntValidator(0,1024,None))
        #self.prenomLayout.addWidget(self.prenomText)
        #self.prenomLayout.addWidget(self.prenomBar)
        #self.champLayout.addLayout(self.prenomLayout)
        self.descriptionLayout.addWidget(self.prenomText)
        self.champLayout.addWidget(self.prenomBar)

        #self.nomLayout = QHBoxLayout()
        self.nomText = QLabel("Nom:")
        self.nomBar = ClickableLineEdit()
        self.nomBar.clicked.connect(self.nomBar.clear)
        self.nomBar.setPlaceholderText("# de ligne")
        self.nomBar.setValidator(QIntValidator(0,1024,None))
        #self.nomLayout.addWidget(self.nomText)
        #self.nomLayout.addWidget(self.nomBar)
        #self.champLayout.addLayout(self.nomLayout)
        self.descriptionLayout.addWidget(self.nomText)
        self.champLayout.addWidget(self.nomBar)

        #self.interetLayout = QHBoxLayout()
        self.interetText = QLabel("Intérêt:")
        self.interetBar = ClickableLineEdit()
        self.interetBar.clicked.connect(self.interetBar.clear)
        self.interetBar.setPlaceholderText("# de ligne")
        self.interetBar.setValidator(QIntValidator(0,1024,None))
        #self.interetLayout.addWidget(self.interetText)
        #self.interetLayout.addWidget(self.interetBar)
        #self.champLayout.addLayout(self.interetLayout)
        self.descriptionLayout.addWidget(self.interetText)
        self.champLayout.addWidget(self.interetBar)

        #self.siteLayout = QHBoxLayout()
        self.siteText = QLabel("Site:")
        self.siteBar = ClickableLineEdit()
        self.siteBar.clicked.connect(self.siteBar.clear)
        self.siteBar.setPlaceholderText("Nom ex: Jobboom")
        #self.siteLayout.addWidget(self.siteText)
        #self.siteLayout.addWidget(self.siteBar)
        #self.champLayout.addLayout(self.siteLayout)
        self.descriptionLayout.addWidget(self.siteText)
        self.champLayout.addWidget(self.siteBar)

        self.fieldLayout = QHBoxLayout()
        self.fieldLayout.addLayout(self.descriptionLayout)
        self.fieldLayout.addLayout(self.champLayout)
        self.fieldGroup.setLayout(self.fieldLayout)

        self.selectionLayout.addWidget(self.fieldGroup)

        self.scrollBox = ScrollQLabel(None)
        self.selectionLayout.addWidget(self.scrollBox)

        self.layout.addLayout(self.selectionLayout)

        self.addButton = QPushButton("Ajouter")
        self.addButton.clicked.connect(self.writeXML)

        self.layout.addWidget(self.addButton)

        self.setLayout(self.layout)

    def _connectSignals(self):
        self.sig_receivedMsgList.connect(self.buildComboBox)
        self.mailsComboBox.currentTextChanged.connect(self.openMail)

    def buildComboBox(self, alist):
        log.log_start_method(self, self.buildComboBox)

        subjects = self.reader.getSubjects(alist)
        # Create a dictionary with subject as keys and alist as values
        self.messages_dict = dict(zip(subjects, alist))
        for i in subjects:
            self.mailsComboBox.addItem(i)

    def openMail(self):
        log.log_start_method(self, self.openMail)

        text = self.mailsComboBox.currentText()#.encode('utf-8')
        self.msgList, msg = self.reader.getdataList(self.messages_dict[text])

        if self.msgList:
            self.scrollBox.setList(self.msgList)
        else:
            self.scrollBox.setList(["Impossible d'ouvrir le couriel"])

        self.selectionLayout.addWidget(self.scrollBox)


    def writeXML(self):
        log.log_start_method(self, self.writeXML)

        msgBox = QMessageBox();
        msgBox.setText("Le site de provenance a été sauvegardé")
        msgBox.exec()

        self.sites.write_data(appdata.Bunch(
            email= self.emailBar.text(),
            prenom= self.prenomBar.text(),
            nom= self.nomBar.text(),
            interet= self.interetBar.text(),
            site= self.siteBar.text()
        ))

        self.emailBar.clear()
        self.prenomBar.clear()
        self.nomBar.clear()
        self.interetBar.clear()
        self.siteBar.clear()


if __name__ == "__main__":
   app = QApplication(sys.argv)
   gui = W()
   sys.exit(app.exec_())
