import xml.etree.ElementTree as ET

import utils.appdata as appdata
import utils.log as log

class xmlManipulator():

    def __init__(self, filename : str):
        log.log_init_object(self)
        self.filename = filename
        tree = ET.parse('data/' + self.filename)
        self.root = tree.getroot()

    def __del__(self):
        log.log_del_object(self)

    def __str__(self):
        return str(self.__class__)

    def getChildTextbyId(self, id):
        for child in self.root.iter():
            if 'id' in child.attrib and child.attrib['id'] == str(id):
                return appdata.Bunch(
                    email= int(child[0].text),
                    prenom= int(child[1].text),
                    nom= int(child[2].text),
                    interet= int(child[3].text),
                    site= child.get('name')
                    )

    def getElementbyId(self, id):
        for child in self.root.iter():
            if 'id' in child.attrib and child.attrib['id'] == str(id):
                return child

    def getChildId(self, element):
        return range(len(element))

if __name__ == "__main__":
    xml = xmlManipulator('site.xml')
    print(xml.getChildTextbyId(0))
    print(xml.getChildId(xml.root))
