from functools import wraps
from PySide2.QtCore import QThread, Signal, Slot

import utils.log as log

class CustomThread(QThread):
    _class_instance = 0

    def __init__(self, parent=None, name=None):
        QThread.__init__(self, parent)
        log.log_init_object(self)
        self.__class__._class_instance += 1
        self.id = self.__class__._class_instance
        self.name = name

    def __del__(self):
        self.__class__._class_instance -= 1
        log.log_del_object(self)
        self.terminate()

    def __repr__(self):
        return 'utils.threadpool.CustomThread'

    def __str__(self):
        return str(self.__class__)

class Thread(QThread):

    exception = Signal(Exception)

    def __init__(self, fct, *args, **kwargs):
        QThread.__init__(self)
        self._fct = fct
        self._args = args
        self._kwargs = kwargs
        self.name = 'threaded'

    def run(self):
        log.log_start_method(self,self.run)
        try:
            self._fct(*self._args, **self._kwargs)
        except Exception as e:
            self.exception.emit(e)

def threaded(fct):
    @wraps(fct)
    def wrapper(*args, **kwargs):
        progress = Thread(fct, *args, **kwargs)
        fct.__runner = progress

        @Slot(Exception)
        def error(exc):
            raise exc

        progress.exception.connect(error)
        progress.start()

    wrapper._original = fct
    return wrapper
