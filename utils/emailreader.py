# -*-coding:Latin-1 -*
import imaplib as imap
import pickle
import os.path
import email
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup as bs
from PySide2.QtCore import QObject, Signal, Slot
from email.header import decode_header
import string
import csv
import re

from utils.threadpool import threaded
import utils.appdata as appdata
from utils.appdata import Data
from utils.dbsqlite import PostulantDB
from utils.myxml import xmlManipulator
import utils.log as log

email_regex = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"

class GmailReader(QObject):
    """
    Classe qui intéragie avec Gmail en plus de fournir des méthodes pour traiter
    les messages courriels

    Méthodes publiques:
    + init()
        Appel des fonction d'initialisation de la classe (connection)
    + readMail(select="INBOX", critere="ALL", callback=None, delete=True)
        Méthodes permettant de lire et d'extraire l'information des courriels
    + getMailsList(select="INBOX", critere="UNSEEN", callback=None)
        Méthodes qui émet une liste de messages correspondants aux critères donnés
    + getSubjects(messages)
        Retourne une liste de sujets des messages
    + getSubject(msg)
        Retourne le sujet d'un message
    + close()
        Ferme la connection et déconnect l'utilisateur
    + getdataList(msg)
        Retourne une liste des lignes du message en string et le message
    """
    #Define signal
    sig_readMail = Signal(str, str)
    sig_getMsgList = Signal()
    sig_receivedMsgList = Signal(appdata.Array)
    updateProgress = Signal(float)
    #_updateProgress = Signal(float)

    def __init__(self, username=None, parent=None):
        super(self.__class__, self).__init__(parent)

        self._SCOPES = ["https://mail.google.com/"]
        self._CLIENT_SECRET = "secret/client_secret.json"
        self._API_SERVICE_NAME = "gmail"
        self._API_VERSION = "v1"

        self._credentials = None
        self._service = None
        self._mail = None
        self._user = None
        self.user = username

        self._db = None

    def __del__(self):
        log.log_del_object(self)

    def __str__(self):
        return str(self.__class__)

    @Slot()
    def init(self):
        """ Appel des fonction d'initialisation de la classe (connection)"""
        log.log_init_object(self)
        self.credentials = self._get_authenticated()
        self.mail = self._imap_connection()

        self._updateProgress = Signal(float)
        self.finished_readMail = Signal()

        self.sig_readMail.connect(self.readMail)
        self.sig_getMsgList.connect(self.getMailsList)

        self._initNameList()

        self.sites = xmlManipulator('site.xml')


    def _get_authenticated(self):
        """
        Authentification
        Vérification des credentials et mise à jour
        """
        credentials = None
        if os.path.exists('secret/token.pickle'):
            with open('secret/token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        #Login si il n'y a pas d'indentifiant valide
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRET,  scopes=self.SCOPES)
                credentials = flow.run_local_server(host='localhost',
                    port=8080,
                    authorization_prompt_message='Redirection...',
                    success_message="""L'authentification est terminer vous pouvez fermer cette page""",
                    open_browser=True)
                #Enregistrer l'identifiant pour la prochaine exécution
                with open('secret/token.pickle', 'wb') as token:
                    pickle.dump(credentials, token)
        return credentials

    def _imap_connection(self):
        """
        Connection par le protocole IMAP au serveur de GMail
        """
        try:
            auth_string = 'user=%s\1auth=Bearer %s\1\1' % (self.user, self.credentials.token)
            mail = imap.IMAP4_SSL('imap.gmail.com')
            mail.authenticate('XOAUTH2', lambda x: auth_string)
            return mail
        except Exception:
            os.remove('secret/token.pickle')
            self.credentials = self._get_authenticated()
            return self._imap_connection()


    @threaded
    def readMail(self, select="INBOX", critere="ALL", callback=None, delete=True):
        """
        Méthodes permettant de lire et d'extraire l'information des courriels

        Paramètre:
        * select : str, dossier dans lequel lire, default="INBOX"
        * critere : str, critère de lecture, default="ALL"
        * callback : fonction, permet de faire d'autre opération sur le message
                     lu au lieu d'extraire l'informations
        * delete : bool, supprime le message après l'avoir traité, default=True
        """
        log.log_start_method(self, self.readMail)

        rv, data = self.mail.select(select)

        if rv == 'OK':
            rv, data = self.mail.search("utf-8", critere)
            if rv != 'OK':
                raise Exception("Auncun message")

            dataLen = len(data[0].split())
            if dataLen == 0:
                log.log_err('Aucun message')
                raise Exception("Auncun message")

            for i,index in enumerate(data[0].split()):
                self.updateProgress.emit(((i+1)/dataLen)*100)

                rv, data = self.mail.fetch(index, "(RFC822)")
                if rv != 'OK':
                    log.log_err("Erreur en lisant le message {}".format(index))
                    raise Exception("Erreur en lisant le message {}".format(index))

                msg = email.message_from_bytes(data[0][1]) #MESSAGE

                if callback:
                    callback(msg);
                else:
                    if delete:
                        self._storedata(self._getdata(msg, index, delete=True))
                    else:
                        self._storedata(self._getdata(msg))

        #def store(msg, index, delete=delete):
        #    if delete:
        #        self._storedata(self._getdata(msg, index))
        #    else:
        #        self._storedata(self._getdata(msg))

        #alist, index = self._parseMail(select, critere, callback)
        #map(lambda x,y:store(x,y,delete=delete), alist, index)


    @threaded
    def getMailsList(self, select="INBOX", critere="UNSEEN", callback=None):
        """
        Méthodes qui émet une liste de messages correspondants aux critères donnés

        Paramètre:
        * select : str, dossier dans lequel lire, default="INBOX"
        * critere : str, critère de lecture, default="ALL"
        * callback : fonction, permet de faire d'autre opération sur le message
                     lu au lieu d'extraire l'informations
        """
        log.log_start_method(self, self.getMailsList)
        alist = self._parseMail(select, critere, callback)
        self.sig_receivedMsgList.emit(alist)

    def _parseMail(self, select="INBOX", critere="ALL", callback=None):
        """
        Méthodes qui retourne la liste de messages correspondants aux critère donnés

        Paramètre:
        * select : str, dossier dans lequel lire, default="INBOX"
        * critere : str, critère de lecture, default="ALL"
        * callback : fonction, permet de faire d'autre opération sur le message
                     lu au lieu d'extraire l'informations
        """
        msgList = []
        indexList = []
        rv, data = self.mail.select(select, readonly=True)

        if rv == 'OK':
            rv, data = self.mail.search("utf-8", critere)
            if rv != 'OK':
                raise Exception("Auncun message")

            dataLen = len(data[0].split())
            if dataLen == 0:
                raise Exception("Auncun message")

            for i,index in enumerate(data[0].split()):
                self.updateProgress.emit(((i+1)/dataLen)*100)

                rv, data = self.mail.fetch(index, "(RFC822)")
                if rv != 'OK':
                    raise Exception("Erreur en lisant le message {}".format(index))

                msg = email.message_from_bytes(data[0][1]) #MESSAGE
                msgList.append(msg)
                indexList.append(index)

            return msgList#, index

    def getSubjects(self, messages):
        """
        Retourne une liste de sujets des messages

        Paramètre
        * messages : list, liste d'objet message
        """
        alist = []
        for msg in messages:
            alist.append(self.getSubject(msg))
        return alist

    def getSubject(self, msg):
        """
        Retourne le sujet d'un message

        Paramètre:
        * msg : objet message
        """
        subject, encoding = decode_header(msg['subject'])[0]
        if type(subject) is bytes:
            return subject.decode(encoding)
        else:
            return subject

    def _html2string(self, payload):
        """
         Tranforme un texte HTML en string
         Retourne str

         Paramètre:
         * payload : str, String composé de balsie HTML
        """
        soup = bs(payload, "html.parser")
        [s.decompose() for s in soup(['script','style'])]
        text = "\n".join(s for s in soup.stripped_strings)
        return text

    def close(self):
        """
        Ferme la connection et déconnect l'utilisateur
        """
        self.mail.close()
        self.mail.logout()

    def _structure(self, msg):
        """
        Retourne la structure d'un message
        """
        for part in msg.walk():
            if part.is_multipart():
                yield part.get_content_type()
            else:
                yield '    ' + part.get_content_type()

    def _readType(self, msg):
        """
        Retourne le message en str avec le bon encodage

        Paramètre:
        * msg : objet message
        """
        if msg.get_content_type() == 'text/plain':
            try:
                return msg.get_payload(decode=True).decode('utf-8')
            except UnicodeDecodeError:
                return msg.get_payload(decode=True).decode('latin-1')
        elif msg.get_content_type() == 'text/html':
            try:
                return self._html2string(msg.get_payload(decode=True).decode('utf-8'))
            except UnicodeDecodeError:
                return self._html2string(msg.get_payload(decode=True).decode('latin-1'))

    def _getdata(self, msg, emailID=None, delete=False):
        """
        Retourne les informations contenu dans le message

        Paramètre:
        * msg : objet message
        * emailID : int, ID du message
        * delete : bool, Supprimer ou non le message après traitement, default=False
        """
        listLine, message = self.getdataList(msg)
        if(listLine is None):
            return None

        self.mail.store(emailID, '-FLAGS', '\\Seen')

        for id in self.sites.getChildId(self.sites.root):
            childs = self.sites.getChildTextbyId(id)
            if childs['site'] in message:
                if delete:
                    self.mail.store(emailID, '+X-GM-LABELS', '\\Trash')
                return appdata.Bunch(
                    email= re.search(email_regex, listLine[childs['email']]).group(),
                    sexe= self._defineSexe(listLine[childs['prenom']].strip(":").strip()),
                    prenom= listLine[childs['prenom']].strip(":").strip(),
                    nom= listLine[childs['nom']].strip(":").strip(),
                    interet= self._defineInteret(listLine[childs['interet']].strip(":").strip()),
                    site= childs['site']
                    )

    def getdataList(self, msg):
        """
        Retourne une liste des lignes du message en string et le message

        Paramètre:
        * msg : objet message
        """
        log.log_start_method(self, self.getdataList)
        if msg.is_multipart():
            message = ''
            listLine = []
            for i in list(msg.walk()):
                if 'text/html' in i.get_content_type():
                    message += self._readType(i)
                    message += '\nENDL\n'

            for i in message.splitlines():
                if i == 'ENDL':
                    listLine.append('-----------------------------------------')
                else:
                    listLine.append(i)

            return listLine, message
        else:
            message = self._readType(msg)
            listLine = message.splitlines()
            return listLine, message
            #return None

    def _storedata(self, adict : dict):
        """
        Insertion du contenu d'un dictionnaire dans la base de données

        Paramètre:
        * adict: dict
        """
        if adict == None:
            return
        self._db = PostulantDB()
        self._db.insert(**adict)

    def _cleanName(self, name : str):
        """
        Retourn le string name sans ponctuation

        Paramètre:
        * name : str
        """
        unwanted = string.punctuation
        tmp = ''.join(char for char in name if char not in unwanted)
        return tmp

    def _initNameList(self):
        """
        Stock les prénoms et noms dans une liste membre de la classe
        """
        with open("data/filles1980-2017.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            self._filles = list([i[0] for i in reader])

        with open("data/gars1980-2017.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            self._gars = list([i[0] for i in reader])

    def _defineSexe(self, firstname : str):
        """
        Défini le genre en fonction du prenom
        Retourne le genre

        Paramètre:
        * firstname : str

        Note: Ce n'est pas une bonne pratique il faut éventuellement retirer
              cette fonctionnalité du programme.
        """
        if firstname.upper() in (self._filles and self._gars):
            return None
        elif firstname.upper() in self._filles:
            return "Madame"
        elif firstname.upper() in self._gars:
            return "Monsieur"
        else:
            return None

    def _defineInteret(self, work : str):
        """
        Retourne l'intéret en fonction du string en paramètre

        Paramètre:
        * work : str
        """
        dt = Data()
        interet = work.lower()
        if interet in dt.readAdmin():
            return "Administration soutien et services"
        elif interet in dt.readGenie():
            return "Genie"
        elif interet in dt.readManuels():
            return "Metiers manuels"
        elif interet in dt.readOp():
            return "Operations tactiques et securite"
        elif interet in dt.readMedic():
            return "Soins de la sante"
        elif interet in dt.readTech():
            return "Technologies"
        else:
            log.log_err(interet)
            return

    #===========================================================================
    # get
    #===========================================================================
    def _get_SCOPES(self):
        return self._SCOPES

    def _get_CLIENT_SECRET(self):
        return self._CLIENT_SECRET

    def _get_API_SERVICE_NAME(self):
        return self._API_SERVICE_NAME

    def _get_API_VERSION(self):
        return self._API_VERSION

    def _get_service(self):
        return self._service

    def _get_credentials(self):
        return self._credentials

    def _get_mail(self):
        return self._mail

    def _get_user(self):
        return self._user

    #===========================================================================
    # set
    #===========================================================================
    def _set_service(self, service):
        self._service = service

    def _set_credentials(self, credentials):
        self._credentials = credentials

    def _set_mail(self, mail):
        self._mail = mail

    def _set_user(self, user):
        self._user = user

    #===========================================================================
    # Propriété
    #===========================================================================
    SCOPES = property(fget=_get_SCOPES)
    CLIENT_SECRET = property(fget=_get_CLIENT_SECRET)
    API_SERVICE_NAME = property(fget=_get_API_SERVICE_NAME)
    API_VERSION = property(fget=_get_API_VERSION)

    service = property(fget=_get_service, fset=_set_service)
    credentials = property(fget=_get_credentials, fset=_set_credentials)
    mail = property(fget=_get_mail, fset=_set_mail)
    user = property(fget=_get_user, fset=_set_user)

if __name__ == "__main__":
    er = GmailReader(input("Username: "))
    er.readMail()
    er.close()
