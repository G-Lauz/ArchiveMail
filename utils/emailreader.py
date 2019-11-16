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

from utils.threadpool import threaded
import utils.appdata as appdata
from utils.appdata import Data
from utils.dbsqlite import PostulantDB
from utils.myxml import xmlManipulator
import utils.log as log

class GmailReader(QObject):
    #Define signal
    sig_readMail = Signal(str, str)
    _updateProgress = Signal(float)

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
        log.log_init_object(self)
        self.credentials = self._get_authenticated()
        self.mail = self._imap_connection()

        self._updateProgress = Signal(float)
        self.finished_readMail = Signal()

        self.sig_readMail.connect(self.readMail)

        self._initNameList()

        self.sites = xmlManipulator('site.xml')


    def _get_authenticated(self):
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
    def readMail(self, select="INBOX", critere="ALL", callback=None):
        log.log_start_method(self, self.readMail)

        log.log_info('select: %s\n %-15s critere: %s' % (select,'', critere))
        rv, data = self.mail.select(select)
        log.log_info('rv : ' + rv)
        if rv == 'OK':
            rv, data = self.mail.search("utf-8", critere)
            if rv != 'OK':
                log.log_info('Aucun message')
                raise Exception("Auncun message")

            dataLen = len(data[0].split())
            if dataLen == 0:
                log.log_info('Aucun message')
                raise Exception("Auncun message")

            for i,index in enumerate(data[0].split()):
                self.updateProgress.emit(((i+1)/dataLen)*100)

                rv, data = self.mail.fetch(index, "(RFC822)")
                if rv != 'OK':
                    log.log_info("Erreur en lisant le message {}".format(index))
                    raise Exception("Erreur en lisant le message {}".format(index))

                msg = email.message_from_bytes(data[0][1]) #MESSAGE

                if callback:
                    callback(msg);
                else:
                    self._storedata(self._getdata(msg))
                    #self._getdata(msg)
                    print('\n')
                    #for i in self._structure(msg):
                    #    print(i)

    def getMailsList(self, select="INBOX", critere="UNSEEN", callback=None):
        alist = []
        rv, data = self.mail.select(select)

        if rv == 'OK':
            rv, data = self.mail.search("utf-8", critere)
            if rv != 'OK':
                raise Exception("Auncun message")

            dataLen = len(data[0].split())
            if dataLen == 0:
                raise Exception("Auncun message")

            for i,index in enumerate(data[0].split()):
                rv, data = self.mail.fetch(index, "(RFC822)")
                if rv != 'OK':
                    raise Exception("Erreur en lisant le message {}".format(index))

                msg = email.message_from_bytes(data[0][1]) #MESSAGE

                subject = u"".join(msg['subject'])
                alist.append(subject)

        return alist

    def _html2string(self, payload):
        soup = bs(payload, "html.parser")
        [s.decompose() for s in soup(['script','style'])]
        text = "\n".join(s for s in soup.stripped_strings)
        return text

    def close(self):
        self.mail.close()
        self.mail.logout()

    def _structure(self, msg):
        for part in msg.walk():
            if part.is_multipart():
                yield part.get_content_type()
            else:
                yield '    ' + part.get_content_type()

    def _readType(self, msg):

        if msg.get_content_type() == 'text/plain':
            print("Plain text")
            try:
                return msg.get_payload(decode=True).decode('utf-8')
            except UnicodeDecodeError:
                return msg.get_payload(decode=True).decode('latin-1')
        elif msg.get_content_type() == 'text/html':
            print("HTML")
            try:
                return self._html2string(msg.get_payload(decode=True).decode('utf-8'))
            except UnicodeDecodeError:
                return self._html2string(msg.get_payload(decode=True).decode('latin-1'))

    def _getdata(self, msg):
        if msg.is_multipart():
            if len(list(msg.walk())) >= 3 + 1:  #TROUVER UNE MEILLEUR SOLUTION
                message = self._readType(list(msg.walk())[3])
                listLine = message.splitlines()
            else:
                print("return")
                return None
        else:
            print("return 1")
            return None

        #for i, item in enumerate(listLine):
        #    print(str(i) + " ..... " + item)

        for id in self.sites.getChildId(self.sites.root):
            childs = self.sites.getChildTextbyId(id)
            if childs['site'] in message:
                return appdata.Bunch(
                    email= listLine[childs['email']],
                    sexe= self._defineSexe(listLine[childs['prenom']].strip(":").strip()),
                    prenom= listLine[childs['prenom']].strip(":").strip(),
                    nom= listLine[childs['nom']].strip(":").strip(),
                    interet= self._defineInteret(listLine[childs['interet']].strip(":").strip()),
                    site= childs['site']
                    )

    def getdataList(self, msg):
        if msg.is_multipart():
            if len(list(msg.walk())) >= 3 + 1:  #TROUVER UNE MEILLEUR SOLUTION
                message = self._readType(list(msg.walk())[3])
                listLine = message.splitlines()
            else:
                print("return")
                return None

            return listLine

        else:
            print("return")
            return None

    def _storedata(self, adict : dict):
        if adict == None:
            return
        self._db = PostulantDB()
        self._db.insert(**adict)

    def _cleanName(self, name : str):
        unwanted = string.punctuation
        tmp = ''.join(char for char in name if char not in unwanted)
        return tmp

    def _initNameList(self):
        with open("data/filles1980-2017.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            self._filles = list([i[0] for i in reader])

        with open("data/gars1980-2017.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            self._gars = list([i[0] for i in reader])

    def _defineSexe(self, firstname : str):
        if firstname.upper() in (self._filles and self._gars):
            return None
        elif firstname.upper() in self._filles:
            return "Madame"
        elif firstname.upper() in self._gars:
            return "Monsieur"
        else:
            return None

    def _defineInteret(self, work : str):
        dt = Data()
        interet = work.lower()
        if interet in dt.readAdmin():
            return "Administration, soutien et services"
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
            print(interet)
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

    def _get_updateProgress(self):
        return self._updateProgress

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

    def _set_updateProgress(self, signal):
        self._updateProgress = signal

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
    updateProgress = property(fget=_get_updateProgress,fset=_set_updateProgress)

if __name__ == "__main__":
    er = GmailReader(input("Username: "))
    er.readMail()
    er.close()
