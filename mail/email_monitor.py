from mail.email_interface import EmailInterface
from mail.email_parser import EmailParser


class EmailMonitor:
    def __init__(self, email_client: EmailInterface, email_parser: EmailParser) -> None:
        self.email_client = email_client
        self.email_parser = email_parser

    def check_for_new_emails(self) -> list[dict[str, str]]:
        new_emails = []
        mail_ids = self.email_client.fetch_unread_emails()

        if not mail_ids:
            return new_emails

        for mail_id in mail_ids:
            raw_email = self.email_client.fetch_email(mail_id)
            parsed_email = self.email_parser.parse(raw_email)
            new_emails.append(parsed_email)

        return new_emails
