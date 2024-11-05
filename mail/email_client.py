import imaplib
from email.message import Message
from imaplib import IMAP4_SSL
import email

from mail.email_interface import EmailInterface


class EmailClient(EmailInterface):
    def __init__(self, server: str, email_account: str, email_password: str, folder: str = "inbox") -> None:
        self.server = server
        self.email_account = email_account
        self.email_password = email_password
        self.folder = folder
        self.connection = self._connect_to_server()

    def _connect_to_server(self) -> IMAP4_SSL:
        connection = imaplib.IMAP4_SSL(self.server)
        connection.login(self.email_account, self.email_password)
        connection.select(self.folder)

        return connection

    def fetch_unread_emails(self) -> list[str]:
        self.connection.select(self.folder)
        _, data = self.connection.search(None, 'UNSEEN')
        mail_ids = data[0].split()

        return mail_ids

    def fetch_email(self, mail_id: str) -> Message:
        _, data = self.connection.fetch(mail_id, "(RFC822)")

        return email.message_from_bytes(data[0][1])
