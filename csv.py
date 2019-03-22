import csv

class csvManipulator():

    def __init__(self, filename : str, format : str):

        self.filename = filename
        self.format = format

    def write(self):
        with open(self.filename + self.format, 'wb') as csvfile:
            pass

    def read(self, filename : str, format : str):
        with open(self.filename + self.format, 'rb') as csvfile:
            pass

    def _get_filename(self):
        return self._filename

    def _get_format(self):
        return self._format

    def _set_filename(self, value : str):
        self._filname = value

    def _set_format(self, value : str):
        self._format = value

    filname = property(fget=_get_filename, fset=_set_filename)
    format = property(fget=_get_format, fset=_set_format)
