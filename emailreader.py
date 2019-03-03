# -*-coding:Latin-1 -*
from getpass import getpass
import imaplib as imap

import pickle
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import email
from bs4 import BeautifulSoup as bs

import os

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
        self.credentials = self._get_authenticated()
        self.mail = self._imap_connection()


    def _get_authenticated(self):
        credentials = None
        if os.path.exists('../token.pickle'):
            with open('../token.pickle', 'rb') as token:
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
                with open('../token.pickle', 'wb') as token:
                    pickle.dump(credentials, token)
        return credentials

    def _imap_connection(self):
        auth_string = 'user=%s\1auth=Bearer %s\1\1' % (self.user, self.credentials.token)
        mail = imap.IMAP4_SSL('imap.gmail.com')
        mail.authenticate('XOAUTH2', lambda x: auth_string)
        return mail

    def readMail(self, select="INBOX", critere="ALL"):
        rv, data = self.mail.select(select)
        if rv == 'OK':
            rv, data = self.mail.search(None, critere)
            if rv != 'OK':
                print("Auncun message trouvé!")

            for i in data[0].split():
                rv, data = self.mail.fetch(i, "(RFC822)")
                if rv != 'OK':
                    print("Erreur en lisant le message ", i)
                    return

                msg = email.message_from_bytes(data[0][1])
                print("Message {}: {}".format(i,msg['Subject']))
                print("From {}".format(msg["From"]))

                print("=====================================================\n")

                if msg.is_multipart():
                    print("Message Multipart")
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True)
                            #print(body)
                            print(body.decode())
                        elif part.get_content_type() == 'text/html':
                            print("HTML 2")
                            body = part.get_payload(decode=True)
                            soup = bs(body.decode())
                            print(self._html2string(part.get_payload(decode=True).decode()))
                else:
                    if msg.get_content_type() == 'text/plain':
                        body = msg.get_payload(decode=True)
                        #print(body)
                        print(body.decode())
                    elif msg.get_content_type() == 'text/html':
                        print("HTML 1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        try:
                            print(self._html2string(msg.get_payload(decode=True).decode('utf-8')))
                        except Exception:
                            print(self._html2string(msg.get_payload(decode=True).decode('latin-1')))

                print("=====================================================\n")

    def _html2string(self, payload):
        soup = bs(payload, "html.parser")
        [s.decompose() for s in soup(['script','style'])]
        #text = soup.get_text()
        text = " ".join(s for s in soup.stripped_strings)
        return text

    def close(self):
        self.mail.close()
        self.mail.logout()

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
    er.readMail()
    er.close()
    #os.system("pause")
