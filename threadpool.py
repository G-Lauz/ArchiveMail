from functools import wraps
from PySide2.QtCore import QThread, Signal

from time import sleep

class progressThread(QThread):

    progress_update = Signal(float)

    def __init__(self, fct, *args, **kwargs):
        QThread.__init__(self)
        self._fct = fct
        self._args = args
        self._kwargs = kwargs

    def run(self):
        self._fct(*self._args, **self._kwargs)

def threaded(fct):
    @wraps(fct)
    def wrapper(*args, **kwargs):
        progress = progressThread(fct, *args, **kwargs)
        fct.__runner = progress
        progress.start()
    return wrapper
