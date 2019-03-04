import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QWidget, QGridLayout

class commandGUI(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
