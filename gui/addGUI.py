import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QMessageBox, QComboBox, QLineEdit, QScrollArea)

from utils.emailreader import GmailReader
import utils.log as log

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

    def setList(self, list):
        for i, item in enumerate(list):
            self.lay.insertWidget(self.lay.count() - 1, QLabel(str(i) + " ..... "+ item))

class addGUI(QWidget, GmailReader):

    def __init__(self, username=None, parent=None):
        QWidget.__init__(self,parent)
        GmailReader.__init__(self,username=username)

        log_init_object(self)

        self.msgList = []

        self.initUI()

    def __del__(self):
        log_del_object(self)

    def initUI(self):
        # Layout principal
        self.layout = QVBoxLayout()

        # Layout de la barre de recherche de courriel
        self.searchLayout = QHBoxLayout()
        self.searchText = QLabel("Exemple de courriel à ouvrir:")
        self.searchLayout.addWidget(self.searchText)

        self.mailsComboBox = QComboBox()
        for i in self.getMailsList():
            self.mailsComboBox.addItem(i)
        self.searchLayout.addWidget(self.mailsComboBox)
        #self.searchBar = QLineEdit("Objet")
        #self.searchLayout.addWidget(self.searchBar)

        self.openButton = QPushButton("Ouvrir")
        self.openButton.clicked.connect(self.openMail)
        self.searchLayout.addWidget(self.openButton)

        self.layout.addLayout(self.searchLayout)

        # Layout de sélection de ligne
        self.selectionLayout = QHBoxLayout()

        # Layout des champs à entrer
        self.champLayout = QVBoxLayout()

        # Layout individuelle des champs
        self.emailLayout = QHBoxLayout()
        self.emailText = QLabel("Email:")
        self.emailBar = QLineEdit("# de ligne")
        self.emailLayout.addWidget(self.emailText)
        self.emailLayout.addWidget(self.emailBar)
        self.champLayout.addLayout(self.emailLayout)

        self.prenomLayout = QHBoxLayout()
        self.prenomText = QLabel("Prenom:")
        self.prenomBar = QLineEdit("# de ligne")
        self.prenomLayout.addWidget(self.prenomText)
        self.prenomLayout.addWidget(self.prenomBar)
        self.champLayout.addLayout(self.prenomLayout)

        self.nomLayout = QHBoxLayout()
        self.nomText = QLabel("Nom:")
        self.nomBar = QLineEdit("# de ligne")
        self.nomLayout.addWidget(self.nomText)
        self.nomLayout.addWidget(self.nomBar)
        self.champLayout.addLayout(self.nomLayout)

        self.interetLayout = QHBoxLayout()
        self.interetText = QLabel("Intérêt:")
        self.interetBar = QLineEdit("# de ligne")
        self.interetLayout.addWidget(self.interetText)
        self.interetLayout.addWidget(self.interetBar)
        self.champLayout.addLayout(self.interetLayout)

        self.siteLayout = QHBoxLayout()
        self.siteText = QLabel("Site:")
        self.siteBar = QLineEdit("# de ligne")
        self.siteLayout.addWidget(self.siteText)
        self.siteLayout.addWidget(self.siteBar)
        self.champLayout.addLayout(self.siteLayout)

        self.selectionLayout.addLayout(self.champLayout)

        self.scrollBox = ScrollQLabel(None)
        self.selectionLayout.addWidget(self.scrollBox)

        self.layout.addLayout(self.selectionLayout)

        self.addButton = QPushButton("Ajouter")
        self.addButton.clicked.connect(self.writeXML)

        self.layout.addWidget(self.addButton)

        self.setLayout(self.layout)

    def openMail(self):
        msgList = ["Hello", "World", "Gabriel", "Lauzier", "Hockey"]
        critere = b'(SUBJECT "%s")' % self.mailsComboBox.currentText().encode('utf-8')
        print(type(critere))
        self.readMail._original(self, critere=critere, callback=self._getMsgList)
        self.scrollBox.setList(self.msgList)

        self.selectionLayout.addWidget(self.scrollBox)

    def _getMsgList(self, msg):
        print(callback)
        self.msgList = self.getdataList(msg)

    def writeXML(self):
        return

if __name__ == "__main__":
   app = QApplication(sys.argv)
   gui = W()
   sys.exit(app.exec_())
