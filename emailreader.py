# -*-coding:Latin-1 -*
import imaplib as imap
from getpass import getpass

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class EmailReader():

    def __init__(self):
        self.SCOPE = "https://mail.google.com/"
        self.CLIENT_SECRET = "../ASTRING"
        self.API_SERVICE_NAME = "gmail"
        self.API_VERSION = "v1"

        self.service = self._get_authenticated_service()

        #self._mail = None
        #self._SMTP_SERVER = "imap.gmail.com"
        #self._SMTP_PORT = 993

        #while True:
        #    print("Connexion:")
        #    self._user = input("Adresse courriel: ")
        #    self._pwd = getpass("Mot de passe: ")

        #    try:
        #        self.mail = imap.IMAP4_SSL(self._SMTP_SERVER)
        #        self.mail.login(self.user,self.pwd)
        #        break
        #    except Exception as e:
        #        print("ConnectionError", e)

    #def readmail(self):
    #    print(mail.list())

    def _get_authenticated_service(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.CLIENT_SECRET,  scopes=[self.SCOPE])
        credentials = flow.run_local_server(host='localhost',
            port=8080,
            authorization_prompt_message='Redirection...',
            success_message="""L'authentification est terminer vous pouvez fermer cette page""",
            open_browser=True)
        return build(self.API_SERVICE_NAME,
            self.API_VERSION, credentials=credentials)

    #===========================================================================
    # get
    #===========================================================================
    def _get_user(self):
        return self._user

    def _get_pwd(self):
        return self._pwd

    def _get_mail(self):
        return self._mail

    def _get_SMTP_SERVER(self):
        return self._SMTP_SERVER

    def _get_SMTP_PORT(self):
        return self._SMTP_PORT

    #===========================================================================
    # set
    #===========================================================================
    def _set_user(self, user : str):
        self._user = user

    def _set_pwd(self, pwd : str):
        self._pwd = pwd

    def _set_mail(self, mail):
        self._mail = mail

    #===========================================================================
    # Propriété
    #===========================================================================
    user = property(fget=_get_user,fset=_set_user)
    pwd = property(fget=_get_pwd,fset=_set_pwd)
    mail = property(fget=_get_mail,fset=_set_mail)

    SMTP_SERVER = property(fget=_get_SMTP_SERVER)
    SMTP_PORT = property(fget=_get_SMTP_PORT)

if __name__ == "__main__":
    er = EmailReader()
    er.readmail()
