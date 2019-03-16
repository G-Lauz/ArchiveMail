from functools import wraps
from PySide2.QtCore import QThread, Signal, Slot

class progressThread(QThread):

    exception = Signal(Exception)

    def __init__(self, fct, *args, **kwargs):
        QThread.__init__(self)
        self._fct = fct
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            self._fct(*self._args, **self._kwargs)
        except Exception as e:
            self.exception.emit(e)

def threaded(fct):
    @wraps(fct)
    def wrapper(*args, **kwargs):
        progress = progressThread(fct, *args, **kwargs)
        fct.__runner = progress

        @Slot(Exception)
        def error(exc):
            raise exc

        progress.exception.connect(error)
        progress.start()
    return wrapper
