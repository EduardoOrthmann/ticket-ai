from typing import Any

from ai.open_ai_client import OpenAIClient
from utils.excel_util import ExcelUtil


class TicketManager:
    def __init__(self, openai_client: OpenAIClient, excel_util: ExcelUtil) -> None:
        self.openai_client = openai_client
        self.excel_util = excel_util

    def get_data_from_email(self, subject: str, body: str) -> dict[str, str | Any]:
        email_data = self.openai_client.interpret_email(
            """
            Fill the cause_code based on the context provided in "Atividades" field. 
            Return only a JSON object in this format with the data you extracted:
            
            {
                "cause_code": "",
                "summarized_issue": "",
                "raw_email": ""
            }
            """,
            subject,
            body,
            self.excel_util.get_clean_data(self.excel_util.get_data())
        )

        email_data = eval(email_data)

        filtered_data = self.excel_util.get_data_by_cause_code(email_data['cause_code'])

        return {
            "cause_code": email_data['cause_code'],
            "priority": filtered_data['Priority'],
            "brief_description": filtered_data['Brief Description'],
            "assignment": filtered_data['Assignment'],
            "summarized_issue": email_data['summarized_issue'],
            "raw_email": body
        }
