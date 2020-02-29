class Data():
    """
    Classe utilitaire, permet de lire les fichier de Domaines

    Membres publiques:
    + SITE : list,
    + INFO : list,
    + DICTINFO : list,
    + MOIS : list,
    + DICTMOIS : list,
    + ADMIN : list,
    + MANUELS : list,
    + GENIE : list,
    + OP : list,
    + MEDIC : list,
    + TECH : list,

    Méthodes publiques:
    + readAdmin()
        Retourne les métiers du domaine de l'administration soutien et services
    + readGenie()
        Retourne les métiers du domaine du Génie
    + readManuels()
        Retourne les métiers du domaine des métiers manuels
    + readOp()
        Retourne les métiers du domaine de l'opération tactiques et sécurité
    + readMedic()
        Retourne les métiers du domaine des soins de la santé
    + readTech()
        Retourne les métiers du domaine des Technologies
    + readSite() -> (obsolète)
        Retourne une liste de site internet contenu dans le fichier data/site.txt
    + readInfo() -> (obsolète)
        Retourne une list et une dictionnaire des informations contenu dans le
        fichier data/info.txt
    + readMois() -> (obsolète)
        Retourne une list et une dictionnaire des mois contenu dans le
        fichier data/mois.txt
    """
    def readAdmin(self):
        with open("data/Domaines/Administration-soutien-et-services.txt",
            'r') as file:
            return file.read()

    def readGenie(self):
        with open("data/Domaines/Genie.txt", 'r') as file:
            return file.read()

    def readManuels(self):
        with open("data/Domaines/Metiers-manuels.txt", 'r') as file:
            return file.read()

    def readOp(self):
        with open("data/Domaines/Operations-tactiques-et-securite.txt",
            'r') as file:
            return file.read()

    def readMedic(self):
        with open("data/Domaines/Soins-de-la-sante.txt", 'r') as file:
            return file.read()

    def readTech(self):
        with open("data/Domaines/Technologies.txt", 'r') as file:
            return file.read()

    def readSite(self):
        with open("data/site.txt", 'r') as file:
            textbyline = file.readlines()
            alist = [i.strip() for i in textbyline]
            return alist

    def readInfo(self):
        with open("data/info.txt", 'r') as file:
            textbyline = file.readlines()
            alist = [i.split()[0] for i in textbyline]
            adict = {}
            for i in textbyline:
                items = i.split()
                adict[items[0]] = items[1]
            return alist, adict

    def readMois(self):
        with open("data/mois.txt", 'r') as file:
            alist = file.readlines()
            adict = {}
            for i, item in enumerate(alist):
                adict[item] = i + 1
            return alist, adict

    #===========================================================================
    # get
    #===========================================================================
    def _get_site(self):
        return self.readSite()

    def _get_info(self):
        return self.readInfo()[0]

    def _get_dictinfo(self):
        return self.readInfo()[1]

    def _get_mois(self):
        return self.readMois()[0]

    def _get_dictmois(self):
        return self.readMois()[1]

    def _get_admin(self):
        return self.readAdmin()

    def _get_manuels(self):
        return self.readManuels()

    def _get_genie(self):
        return self.readGenie()

    def _get_op(self):
        return self.readOp()

    def _get_medic(self):
        return self.readMedic()

    def _get_tech(self):
        return self.readTech()

    #===========================================================================
    # property
    #===========================================================================
    SITE = property(fget=_get_site)
    INFO = property(fget=_get_info)
    DICTINFO = property(fget=_get_dictinfo)
    MOIS = property(fget=_get_mois)
    DICTMOIS = property(fget=_get_dictmois)
    ADMIN = property(fget=_get_admin)
    MANUELS = property(fget=_get_manuels)
    GENIE = property(fget=_get_genie)
    OP = property(fget=_get_op)
    MEDIC = property(fget=_get_medic)
    TECH = property(fget=_get_tech)

class Bunch(dict):
    """
    Objet dict
    """
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self

class Array(list):
    """
    Objet list
    """
    def __init__(self, **kwargs):
        list.__init__(self, kwargs)
        self.__list__ = self
