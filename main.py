import sys

from PySide2.QtCore import QObject, Signal, Slot, QThread
from PySide2.QtWidgets import QApplication

import gui.mainGUI as mainGUI

import utils.emailreader as GmailReader
from utils.threadpool import CustomThread
import utils.log as log

import ctypes #Color cmd

class Main(QObject):
    #Define Signal

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        # color cmd
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


        log.log_init_object(self)

        #Create GUI Object
        self.mainGUI = mainGUI.mainGUI()

        #Make cross object connections
        self._connectSignals()

        #Show initial GUI
        self.mainGUI.show()

    def __del__(self):
        log.log_del_object(self)

    def __str__(self):
        return str(self.__class__)

    #Make the different signal's conenctions
    def _connectSignals(self):
        self.mainGUI.userEdited.connect(self.start)
        self.mainGUI.sig_readMail.connect(self.on_sig_readMail)
        self.mainGUI.sig_getMsgList.connect(self.on_getMsgList)
        self.mainGUI.aboutToClose.connect(self.on_aboutToClose)

    #Init the program
    @Slot(str)
    def start(self, user):
        log.log_start_method(self, self.start)
        #Create a new thread
        self.createThread(user)

    def createThread(self, user):
        # Add condition to select wich client to connect to

        # setup de Email reader thread
        self.reader = GmailReader.GmailReader(user)
        self.reader_thread = CustomThread(name='reader_thread')

        self.reader.moveToThread(self.reader_thread)
        self.reader_thread.start()

        # Connect reader Signal to the thread Slot
        self.reader_thread.started.connect(self.reader.init)
        self.reader.updateProgress.connect(self.on_updateProgress)
        self.reader.sig_receivedMsgList.connect(self.on_receivedMsgList)

    def on_sig_readMail(self, select=None, critere=None):
        log.log_start_method(self, self.on_sig_readMail)
        self.reader.sig_readMail.emit(select, critere)

    def on_updateProgress(self, progress):
        log.log_start_method(self, self.on_updateProgress)
        self.mainGUI.updateProgress.emit(progress)

    def on_getMsgList(self):
        log.log_start_method(self, self.on_getMsgList)
        self.reader.sig_getMsgList.emit()

    def on_receivedMsgList(self, alist):
        log.log_start_method(self, self.on_receivedMsgList)
        self.mainGUI.sig_receivedMsgList.emit(alist)

    def on_aboutToClose(self):
        if self.reader_thread:
            self.reader_thread.quit()
        if self.reader:
            del self.reader
        del self.mainGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
