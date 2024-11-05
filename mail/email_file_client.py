import os
from email.message import Message

import extract_msg

from mail.email_interface import EmailInterface


class EmailFileClient(EmailInterface):
    def __init__(self, directory_path: str) -> None:
        self.directory_path = directory_path

    def fetch_unread_emails(self) -> list[str]:
        return [os.path.join(self.directory_path, file) for file in os.listdir(self.directory_path) if
                file.endswith(".msg")]

    def fetch_email(self, mail_id: str) -> Message:
        return self._convert_to_email_message(extract_msg.Message(mail_id))

    def _convert_to_email_message(self, msg: extract_msg.Message) -> Message:
        email_message = Message()
        email_message["Subject"] = msg.subject
        email_message["From"] = msg.sender
        email_message.set_payload(msg.body.encode('utf-8'))

        return email_message
