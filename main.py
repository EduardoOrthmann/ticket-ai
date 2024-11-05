from mail.email_client import EmailClient
from mail.email_file_client import EmailFileClient
from mail.email_monitor import EmailMonitor
from mail.email_parser import EmailParser
from ai.open_ai_client import OpenAIClient
from ticket.ticket_manager import TicketManager
from dotenv import load_dotenv
import time
import os

from utils.excel_util import ExcelUtil


def main() -> None:
    load_dotenv()

    # email_client = EmailClient(os.getenv("IMAP_SERVER"), os.getenv("EMAIL_ACCOUNT"), os.getenv("EMAIL_PASSWORD"))
    email_client = EmailFileClient("C:\\Users\\Eduardo\\Downloads\\emails")
    email_parser = EmailParser()
    email_monitor = EmailMonitor(email_client, email_parser)
    excel_util = ExcelUtil("C:\\Users\\Eduardo\\Downloads\\L1-Email-to-SNOW\\Relação de Cause Code ECS-eEVN - Dicas e descrição - Dez_2019.xlsx")
    openai_client = OpenAIClient(os.getenv("OPENAI_API_KEY"), os.getenv("OPENAI_API_VERSION"), os.getenv("OPENAI_API_BASE"), os.getenv("OPENAI_GPT35TURBO_MODEL"))
    ticket_manager = TicketManager(openai_client, excel_util)

    while True:
        print("Checking for new emails...")
        new_emails = email_monitor.check_for_new_emails()

        for email in new_emails:
            ticket_data = ticket_manager.get_data_from_email(email['subject'], email['body'])

            print("Generated Ticket: {")
            for key, value in ticket_data.items():
                print(f"\t{key}: {value}")
            print("}\n")

        time.sleep(10)

if __name__ == "__main__":
    main()