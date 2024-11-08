from email.message import Message


class EmailInterface:
    def fetch_emails(self) -> list[str]:
        # Fetches unread emails from the email server
        pass

    def fetch_email(self, mail_id: str) -> Message:
        # Fetches the email with the given mail_id from the email server
        pass
