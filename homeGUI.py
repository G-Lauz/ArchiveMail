import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QWidget

class homeGUI(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)

        self.setFixedSize(400,240)

        self.quit = QtWidgets.QPushButton("Quit", self)
        self.quit.setGeometry(62, 40, 75, 30)
        self.quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(self.quit, QtCore.SIGNAL("clicked()"),
                     QtWidgets.qApp, QtCore.SLOT("quit()"))
