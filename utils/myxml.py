import xml.etree.ElementTree as ET
#import xml.etree.cElementTree as ET

import utils.appdata as appdata
import utils.log as log

class xmlManipulator():

    def __init__(self, filename : str):
        log.log_init_object(self)
        self.filename = filename
        self.tree = ET.parse('data/' + self.filename)
        self.root = self.tree.getroot()

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

    def write_data(self, adict: dict):
        site_count = len(self.root.getchildren()) + 1

        site = ET.SubElement(
            self.root, "site", id=str(site_count), name=adict['site']
        )

        ET.SubElement(site, "email").text = adict['email']
        ET.SubElement(site, "prenom").text = adict['prenom']
        ET.SubElement(site, "nom").text = adict['nom']
        ET.SubElement(site, "interet").text = adict['interet']

        self.tree.write('data/' + self.filename)

if __name__ == "__main__":
    xml = xmlManipulator('site.xml')
    print(xml.getChildTextbyId(0))
    print(xml.getChildId(xml.root))
