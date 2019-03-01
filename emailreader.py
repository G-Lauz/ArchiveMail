# -*-coding:Latin-1 -*
from getpass import getpass
import imaplib as imap

import pickle
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GmailReader():

    def __init__(self):
        self._SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.labels",
        "https://www.googleapis.com/auth/gmail.insert"
        ]
        self._CLIENT_SECRET = "../client_secret.json"
        self._API_SERVICE_NAME = "gmail"
        self._API_VERSION = "v1"

        self._credentials = None
        self._service = None

        self.service = self._get_authenticated_service()

    def _get_authenticated_service(self):
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
        return build(self.API_SERVICE_NAME,
            self.API_VERSION, credentials=self.credentials)

    #Test
    def readMail(self):
        results = self.service.users().messages().list(userId="me",
            labelIds = ["INBOX"]).execute()
        messages = results.get("messages",[])

        if not messages:
            print("No messages found.")
        else:
            print("Message snippets:")

            msg = self.service.users().messages().get(userId='me', id=messages[0]['id'],format="full").execute()
            print(msg)

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

    #===========================================================================
    # set
    #===========================================================================
    def _set_service(self, service):
        self._service = service

    def _set_credentials(self, credentials):
        self._credentials = credentials

    #===========================================================================
    # Propriété
    #===========================================================================
    SCOPES = property(fget=_get_SCOPES)
    CLIENT_SECRET = property(fget=_get_CLIENT_SECRET)
    API_SERVICE_NAME = property(fget=_get_API_SERVICE_NAME)
    API_VERSION = property(fget=_get_API_VERSION)

    service = property(fget=_get_service, fset=_set_service)
    credentials = property(fget=_get_credentials, fset=_set_credentials)

if __name__ == "__main__":
    er = GmailReader()
    er.readMail()
