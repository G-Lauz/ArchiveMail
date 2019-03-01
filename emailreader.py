# -*-coding:Latin-1 -*
from getpass import getpass
import imaplib as imap

import pickle
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import base64

#9h à 10h30
class GmailReader():

    def __init__(self):
        #Supprimer le fichier token.pickle si on change le scopes
        self._SCOPES = ["https://mail.google.com/"]
        self._CLIENT_SECRET = "../client_secret.json"
        self._API_SERVICE_NAME = "gmail"
        self._API_VERSION = "v1"

        self._credentials = None
        self._service = None
        self._mail = None
        self._user = None

        self.user = input("Username: ")
        self._get_authenticated()
        self._imap_connection()


    def _get_authenticated(self):
        if os.path.exists('../token.pickle'):
            with open('../token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)
        #Login si il n'y a pas d'indentifiant valide
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRET,  scopes=self.SCOPES)
                self.credentials = flow.run_local_server(host='localhost',
                    port=8080,
                    authorization_prompt_message='Redirection...',
                    success_message="""L'authentification est terminer vous pouvez fermer cette page""",
                    open_browser=True)
                #Enregistrer l'identifiant pour la prochaine exécution
                with open('../token.pickle', 'wb') as token:
                    pickle.dump(self.credentials, token)
        #Changer?
        #return build(self.API_SERVICE_NAME,
            #self.API_VERSION, credentials=self.credentials)

    def _imap_connection(self):
        auth_string = 'user=%s\1auth=Bearer %s\1\1' % (self.user, self.credentials.token)
        self.mail = imap.IMAP4_SSL('imap.gmail.com')
        self.mail.authenticate('XOAUTH2', lambda x: auth_string)

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
    er = GmailReader()
    #er.readMail()
