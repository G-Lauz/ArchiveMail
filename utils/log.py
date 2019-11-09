# -*-coding:Latin-1 -*
from PySide2.QtCore import Signal, Slot, QThread

def log_thread(msg:str):
    currentThread = QThread.currentThread()
    try:
        print('%-15s: %s' % (currentThread.name, msg))
    except AttributeError as err:
        try:
            print('%s %-15s: \n\t%s' % (currentThread, currentThread.id, msg))
        except AttributeError as err:
            print('%-15s: %s' % ('main-thread', msg))

def log_init_object(object):
    msg = 'Init %s ...' % (object)
    log_thread(msg)

def log_del_object(object):
    msg = 'Destruction of %s ...' % (object)
    log_thread(msg)

def log_start_method(object, method):
    msg = 'Start %s from %s ...' % (method.__name__, type(object).__name__)

def log_info(message : str):
    log_thread(message)
