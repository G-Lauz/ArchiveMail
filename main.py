import sys

from PySide2.QtCore import QObject, Signal, Slot, QThread
from PySide2.QtWidgets import QApplication

import gui.mainGUI as mainGUI

import utils.emailreader as GmailReader

class Main(QObject):
    #Define Signal

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        #Create GUI Object
        self.mainGUI = mainGUI.mainGUI()

        #Make cross object connections
        self._connectSignals()

        #Show initial GUI
        self.mainGUI.show()

    #Make the different signal's conenctions
    def _connectSignals(self):
        self.mainGUI.userEdited.connect(self.start)

    #@Slot(str)
    #Init the program
    def start(self, user):
        #Create a new thread
        self.createThread(user)

    def createThread(self, user):
        # Add condition to select wich client to connect to

        # setup de Email reader thread (main thread)
        self.reader = GmailReader.GmailReader(user)
        self.reader_thread = QThread()

        self.reader.moveToThread(self.reader_thread)

        # Connect reader Signal to the thread Slot
        self.reader_thread.started.connect(self.reader.init)

        self.reader_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
