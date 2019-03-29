# -*-coding:Latin-1 -*
import sqlite3
from urllib.request import pathname2url
import datetime as dt

class PostulantDB():
    """
    Classe définisant une base de donné de postulant

    Attributs publique:
    - TABLENAME : str, nom de base des tables de données
    - TABLETODAY : str, nom de la table du mois présent
    - DBFILE : str, nom du fichier de la base de données
    - EMAIL : str
    - SEXE : str
    - PRENOM : str
    - NOM : str
    - INTERET : str
    - SITE : str

    Méthodes publique:
    - insert(email='', sexe='', prenom='', nom='', interet='', site='')
        Insèrer des valeurs dans la table du mois présent
    - select(table : str, data : str)
        Sélectionner et retourner une colonne de valeurs d'une table
    - selectThese(table : str, data : list)
        Sélectionner et retourner plusieurs colonne de valeurs d'une table
    - selectAValue(table : str, type : str, data : str)
        Sélectionner et retourner tout les lignes contenant la valeur cherché
    - countAValue(table : str, type : str, data : str)
        Compte le nombre d'instance d'une valeur dans une table donnée
    - deleteTable(tableName : str, year : int, month : int)
        Supprime une table de la base de données
    - tableList()
        Retourne la liste des tables de la base de données
    - close()
        Ferme la database
    """

    #Constructeur de la class
    def __init__(self):
        self._DBFILE = "data/postulantdb.db"
        self._TABLENAME = "POSTULANT"
        self._conn = None
        self._cursor = None

        #Constante
        self._EMAIL = "COURIEL"
        self._SEXE = "SEXE"
        self._PRENOM = "PRENOM"
        self._NOM = "NOM"
        self._INTERET = "INTERET"
        self._SITE = "SITE"

        #Vérifier si un fichier postulantdb.py existe en créé un si non
        #et établir la conenction à la DB
        #Finalement initialiser le curseur
        try:
            dburi = "file:{}?mode=rw".format(pathname2url(self.DBFILE))
            self.conn = sqlite3.connect(dburi,uri=True)

        except sqlite3.OperationalError:
            self.conn = sqlite3.connect(self.DBFILE)

        finally:
            self.cursor = self.conn

            command = '''CREATE TABLE IF NOT EXISTS {}
                (COURIEL TEXT,
                SEXE TEXT,
                PRENOM TEXT,
                NOM TEXT,
                INTERET TEXT,
                SITE TEXT,
                MOIS INT);'''.format(self._scrub(self.TABLETODAY))
            self.cursor.execute(command)

    #Destructeur de la class
    def __del__(self):
        self.conn.close()

    def insert(self, email:str="none", sexe:str="none", prenom:str="none",
        nom:str="none", interet:str="none", site:str="none"):
        """Méthode permettant d'insérer des valeurs dans DB du mois présent
        Paramètre:
        - email : str
        - sexe : str
        - prenom : str
        - nom : str
        - interet : str
        - site : str"""

        mois = self._time()[1]
        info = [email,sexe,prenom,nom,interet,site,mois]
        command = '''INSERT INTO {}
            (COURIEL,SEXE,PRENOM,NOM,INTERET,SITE,MOIS)
            VALUES (?,?,?,?,?,?,?)'''.format(self._scrub(self.TABLETODAY))

        self.cursor.execute(command, info)
        self.conn.commit()
        return

    def select(self, table : str, data : str):
        """Méthode permettant de sélectionner et retourner une colonne de valeurs
        d'une table donnée
        Paramètre:
        - table : str, le nom de table ou sélectionner la colonne
        - data : str, le nom de la colonne sélectionner
        Return:
        - : list, retourn une list des éléments de la colonne"""

        items = []
        command = "SELECT {} from {}".format(self._scrub(data),
            self._scrub(table))

        for row in self.cursor.execute(command).fetchall():
            items.append(row[0])
        return items

    def selectThese(self, table : str, data : list):
        """Sélectionner et retourner plusieurs colonne de valeurs d'une table
        Paramètre:
        - table : str, nom de la table
        - data : list, noms des colonnes
        Retourne:
        - : list, retourne une liste des éléments des colonnes"""

        items = []
        command = "SELECT "

        for i in data:
            if i == data[-1]:
                command = command + "".join(self._scrub(i) + " ")
            else:
                command = command + "".join(self._scrub(i) + ", ")

        command = command + "from {}".format(self._scrub(table))

        try:
            for row in self.cursor.execute(command).fetchall():
                items.append(row)
        except sqlite3.OperationalError as e:
            if len(data) == 0:
                raise Exception("Aucune options choisi")

        return items

    def selectAValue(self, table : str, type : str, data : str):
        """Sélectionner et retourner tout les lignes contenant la valeur cherché
        Paramètre:
        - table : str, nom de la table
        - type : str, colonne de la table
        - data : str, valeur recherché
        Retourne:
        - : list, lignes contenant la valeur recherché"""

        items = []
        command = "SELECT * FROM {} WHERE trim({}) = \"{}\"".format(
            self._scrub(table),self._scrub(type),self._scrub(data))

        for row in self.cursor.execute(command).fetchall():
            items.append(tuple(i for i in row if i != "none"))
        return items

    def countAValue(self, table : str, type : str, data : str):
        """Compte le nombre d'instance d'une valeur dans une table donnée
        Paramètre:
        - table : str, nom de la table
        - type : str, colonne de la table
        - data : str, valeur recherché
        Retourne:
        - : int, nombre d'instance de la valeur dans la table"""

        command = "SELECT * FROM {} WHERE trim({}) = \"{}\"".format(
            self._scrub(table),self._scrub(type),self._scrub(data))

        return len(self.cursor.execute(command).fetchall())

    #Revoir les paramètres****
    def deleteTable(self, tableName : str, year : int, month : int):
        """Supprime une table de la base de données
        Paramètre:
        - tableName : str, nom de base de la table
        - year : int, année de création de la table
        - month : int, mois de création de la table"""

        table = tableName + str(year) + str(month)
        command = "DROP table if exists {}".format(self._scrub(table))
        self.cursor.execute(command)
        self.conn.commit()

    def tableList(self):
        """Retourne la liste des tables de la base de données"""

        items = []
        command = "SELECT NAME FROM SQLITE_MASTER WHERE TYPE= \"table\""
        for row in self.cursor.execute(command).fetchall():
            items.append(row[0])
        return items

    def close(self):  #TMP
        """Ferme la base de donnée"""
        print("Fermeture de la DB")
        self.conn.close()

    def _time(self):
        return dt.date.today().year, dt.date.today().month

    def _scrub(self, name : str):
        return ''.join(char for char in name if char.isalnum())

    #====================================================================
    #get/set
    #====================================================================
    def _get_DBFILE(self):
        return self._DBFILE

    def _get_TABLETODAY(self):
        return self._TABLENAME + str(self._time()[0]) + str(self._time()[1])

    def _get_TABLENAME(self):
        return self._TABLENAME

    def _get_conn(self):
        return self._conn

    def _get_EMAIL(self):
        return self._EMAIL

    def _get_SEXE(self):
        return self._SEXE

    def _get_PRENOM(self):
        return self._PRENOM

    def _get_NOM(self):
        return self._NOM

    def _get_INTERET(self):
        return self._INTERET

    def _get_SITE(self):
        return self._SITE

    def _set_conn(self, conn):
        self._conn = conn

    def _get_cursor(self):
        return self._cursor

    def _set_cursor(self, conn):
        self._cursor = conn.cursor()

    #====================================================================
    #Propriété
    #====================================================================
    DBFILE = property(fget=_get_DBFILE)
    TABLETODAY = property(fget=_get_TABLETODAY)
    TABLENAME = property(fget=_get_TABLENAME)
    conn = property(fget=_get_conn, fset=_set_conn)
    cursor = property(fget=_get_cursor,fset=_set_cursor)

    EMAIL = property(fget=_get_EMAIL)
    SEXE = property(fget=_get_SEXE)
    PRENOM = property(fget=_get_PRENOM)
    NOM = property(fget=_get_NOM)
    INTERET = property(fget=_get_INTERET)
    SITE = property(fget=_get_SITE)

#Main temporaire pour tester la class individuellement
if __name__ == "__main__":
    db = PostulantDB()
    #db.insert(email="etienne@gmail.com",prenom="etienne", interet="Mecanique")
    alist = [db.EMAIL,db.PRENOM, db.SEXE, db.INTERET, db.SITE]
    #print(db.select(db.TABLETODAY, db.EMAIL))
    #print("\n")
    print(db.selectThese(db.TABLETODAY, alist))
    #print("\n")
    #print(db.selectAValue(db.TABLETODAY, db.PRENOM, "etienne"))
    #print("\n")
    #print(db.countAValue(db.TABLETODAY, db.PRENOM, "etienne"))

    #db.deleteTable(db.TABLENAME, 2019, 2)
    print(db.tableList())
    #db.close()
