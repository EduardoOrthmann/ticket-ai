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

        while not valid_cause_code and attempt < 3:
            email_data_str = self.openai_client.interpret_email(
                f"""
                The context is divided into two parts: 'Cause Code' is the key and 'Atividades' is the value.
                Fill the cause_code based on the context provided in 'Atividades' field. 
                Only select a cause_code that exists in the valid list provided.
                {f"Previous cause_code '{cause_code}' was invalid. Please try to select another." if cause_code else ""}
                Return only a JSON object with the extracted data:
                
                {{
                    "cause_code": "",
                    "summarized_issue": "",
                    "raw_email": ""
                }}
                """,
                subject,
                body,
                str(self.excel_util.get_key_value_clean_data())
            )

            print(f"Email data attempt {attempt + 1}: ", email_data_str, "\n")
            email_data = eval(email_data_str)

            if email_data.get("cause_code") and self.excel_util.get_data_by_cause_code(email_data.get("cause_code")):
                valid_cause_code = True
            else:
                attempt += 1

        if not valid_cause_code:
            print("Unable to find a valid cause code after multiple attempts.")
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
