import xml.etree.ElementTree as ET

import utils.appdata as appdata

class xmlManipulator():

    def __init__(self, filename : str):
        self.filename = filename
        tree = ET.parse('data/' + self.filename)
        self.root = tree.getroot()

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
