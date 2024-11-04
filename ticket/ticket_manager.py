import json
from typing import Any

from ai.open_ai_client import OpenAIClient
from utils.excel_util import ExcelUtil


class TicketManager:
    def __init__(self, openai_client: OpenAIClient, excel_util: ExcelUtil) -> None:
        self.openai_client = openai_client
        self.excel_util = excel_util

    def get_data_from_email(self, subject: str, body: str) -> dict[str, str | Any]:
        attempt = 0
        email_data = {}
        cause_code = ""
        valid_cause_code = False
        context = str(self.excel_util.get_key_value_clean_data())

        while not valid_cause_code and attempt < 3:
            prompt = f"""
                You are tasked with matching an email's content to a 'cause_code' based on contextual information in an Excel sheet.
                Each 'cause_code' has a description of relevant activities in the 'Atividades' field. Match the cause_code to the email based on these descriptions.
                Return ONLY a JSON object with this format:
                {{
                    "cause_code": "", 
                    "summarized_issue": "", 
                    "raw_email": ""
                }}
    
                Example:
                Context: [{{"E-COLLABORATION.NOTIFICATION.CREATE.CHANGE": "Incluir notificações, Remover notificações, Alterar e-mail de notificações"}}]
                Email: "Please add the email below to receive notifications for CNPJ 76639285003516"
                Expected Output:
                {{
                    "cause_code": "E-COLLABORATION.NOTIFICATION.CREATE.CHANGE",
                    "summarized_issue": "Request to add an email to receive notifications",
                    "raw_email": "Please add the email below to receive notifications for CNPJ 76639285003516"
                }}
    
                {f"Previous cause_code '{cause_code}' was invalid. Please try another." if cause_code else ""}
                Context: {context}
                
                Email:
                Subject: {subject}
                Body: {body}
                """

            email_data_str = self.openai_client.interpret_email(prompt)

            try:
                email_data = json.loads(email_data_str)
                if email_data.get("cause_code") and self.excel_util.get_data_by_cause_code(email_data.get("cause_code")):
                    valid_cause_code = True
                else:
                    attempt += 1
                    cause_code = email_data.get("cause_code", "")
            except json.JSONDecodeError:
                print("Invalid JSON format received from AI. Retrying...")
                attempt += 1

        if not valid_cause_code:
            print("Failed to get valid 'cause_code' after 3 attempts. Returning default values.")

            return {
                "cause_code": "N/A",
                "priority": "N/A",
                "brief_description": "N/A",
                "assignment": "N/A",
                "summarized_issue": "N/A",
                "raw_email": body
            }

        filtered_data = self.excel_util.get_data_by_cause_code(email_data['cause_code'])

        return {
            "cause_code": email_data['cause_code'],
            "priority": filtered_data.get('Priority', 'N/A'),
            "brief_description": filtered_data.get('Brief Description', 'N/A'),
            "assignment": filtered_data.get('Assignment', 'N/A'),
            "summarized_issue": email_data['summarized_issue'],
            "raw_email": body
        }
