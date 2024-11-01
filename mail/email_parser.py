from email.header import decode_header
from email.message import Message


class EmailParser:
    @staticmethod
    def parse(msg: Message) -> dict[str, str]:
        subject, encoding = decode_header(msg.get("Subject"))[0]

        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        from_ = msg.get("From")
        body = EmailParser._get_email_body(msg)

        return {"subject": subject, "from": from_, "body": body}

    @staticmethod
    def _get_email_body(msg: Message) -> str:
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode("utf-8")
                    except Exception:
                        pass
        else:
            body = msg.get_payload(decode=True).decode("utf-8")
        return body