import csv

class csvManipulator():

    def __init__(self, filename : str):

        self.filename = filename

    def write(self, items):
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|',
                quoting=csv.QUOTE_MINIMAL)
            writer.writerows(items)

    #INUTILE
    def read(self):
        with open(self.filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            return reader

    def _get_filename(self):
        return self._filename

    def _set_filename(self, value : str):
        self._filname = value

    filname = property(fget=_get_filename, fset=_set_filename)
