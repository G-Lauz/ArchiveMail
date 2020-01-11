# -*-coding:Latin-1 -*
from PySide2.QtCore import Signal, Slot, QThread

class Colors():
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

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
    msg = 'Init ' + str(object) + ' ...'
    log_thread(msg)

def log_del_object(object):
    msg = 'Destruction of ' + str(object) + ' ...'
    log_thread(msg)

def log_start_method(object, method):
    msg = (Colors.fg.lightcyan +
           'Start ' + method.__name__ + ' from ' + type(object).__name__ +
           ' ...' +
           Colors.reset)
    log_thread(msg)

def log_info(message : str):
    msg = Colors.fg.lightgreen + message + Colors.reset
    log_thread(msg)

def log_err(message : str):
    msg = Colors.fg.lightred + message + Colors.reset
    log_thread(msg)
