from pydantic import ValidationError

from mail.email_interface import EmailInterface
from mail.email_parser import EmailParser
from models import EmailResponse, EmailStatus


class EmailMonitor:
    def __init__(self, email_client: EmailInterface, email_parser: EmailParser) -> None:
        self.email_client = email_client
        self.email_parser = email_parser
        self.emails = []

    def check_for_new_emails(self) -> list[EmailResponse]:
        if not self.emails:
            mail_ids = self.email_client.fetch_emails()

            for mail_id in mail_ids:
                raw_email = self.email_client.fetch_email(mail_id)
                parsed_email = self.email_parser.parse(raw_email)
                parsed_email["id"] = mail_id

                try:
                    email_response = EmailResponse(
                        id=parsed_email["id"],
                        subject=parsed_email["subject"],
                        from_=parsed_email["from"],
                        body=parsed_email["body"],
                        status=EmailStatus.unprocessed
                    )
                    self.emails.append(email_response)
                except ValidationError as e:
                    print(f"Validation error for email: {mail_id}")
                    print(e.errors())
        return self.emails
