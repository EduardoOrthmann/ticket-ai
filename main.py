from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import ValidationError

from mail.email_client import EmailClient
from mail.email_monitor import EmailMonitor
from mail.email_parser import EmailParser
from ai.open_ai_client import OpenAIClient
from models import TicketRequest, TicketResponse, EmailStatus
from ticket.ticket_manager import TicketManager
from dotenv import load_dotenv
import os

from utils.excel_util import ExcelUtil

app = Flask(__name__)
CORS(app)
load_dotenv()

ticket_database: list[TicketResponse] = []

email_client = EmailClient(os.getenv("IMAP_SERVER"), os.getenv("EMAIL_ACCOUNT"), os.getenv("EMAIL_PASSWORD"))
email_parser = EmailParser()
email_monitor = EmailMonitor(email_client, email_parser)
excel_util = ExcelUtil("C:\\Users\\Eduardo\\Downloads\\L1-Email-to-SNOW\\Relação de Cause Code ECS-eEVN - Dicas e descrição - Dez_2019 1 - Copy.xlsx")
openai_client = OpenAIClient(os.getenv("OPENAI_API_KEY"), os.getenv("OPENAI_API_VERSION"), os.getenv("OPENAI_API_BASE"), os.getenv("OPENAI_GPT35TURBO_MODEL"))
ticket_manager = TicketManager(openai_client, excel_util)

@app.route("/email", methods=["GET"])
def get_emails():
    try:
        return jsonify([email.model_dump() for email in email_monitor.check_for_new_emails()])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ticket/generate", methods=["POST"])
def generate_ticket():
    try:
        ticket_request = TicketRequest(**request.get_json())
        ticket_data = ticket_manager.get_data_from_email(ticket_request.subject, ticket_request.body)
        ticket_response = TicketResponse(**ticket_data)

        ticket_database.append(ticket_response)

        for email in email_monitor.emails:
            if email.subject == ticket_request.subject:
                email.status = EmailStatus.processed
                break

        return jsonify(ticket_response.model_dump())
    except ValidationError as e:
        return jsonify({"error": "Invalid data", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ticket", methods=["GET"])
def get_tickets():
    return jsonify([ticket.model_dump() for ticket in ticket_database])

@app.route("/excel", methods=["GET"])
def download_excel():
    return excel_util.get_data().to_csv()

if __name__ == "__main__":
    app.run(debug=True)