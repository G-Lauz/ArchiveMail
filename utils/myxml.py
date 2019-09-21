import xml.etree.ElementTree as ET

import appdata

class xmlManipulator():

    def __init__(self, filename : str):
        self.filename = filename
        tree = ET.parse('../data/' + self.filename)
        self.root = tree.getroot()

    def getChildTextbyId(self, id):
        for child in self.root.iter():
            if 'id' in child.attrib and child.attrib['id'] == str(id):
                return appdata.Bunch(
                    email= child[0].text,
                    prenom= child[1].text,
                    nom= child[2].text,
                    interet= child[3].text,
                    site= child.get('name')
                    )

if __name__ == "__main__":
    xml = xmlManipulator('site.xml')
    print(xml.getChildTextbyId(0))
