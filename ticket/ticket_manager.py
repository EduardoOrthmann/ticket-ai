import json
from typing import Any

from ai.open_ai_client import OpenAIClient
from exceptions.failed_to_interpret_email_exception import FailedToInterpretEmailException
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
            (system_prompt, prompt, examples) = self._generate_prompt(subject, body)
            email_data = self._interpret_email(system_prompt, prompt, examples, context, cause_code)

            cause_code = email_data.get("cause_code", "")

            if self._is_valid_cause_code(cause_code):
                valid_cause_code = True
            else:
                attempt += 1

        if not valid_cause_code:
            print("Failed to get valid 'cause_code' after 3 attempts. Returning default values.")
            return self._default_response(body)

        return self._construct_response(email_data, body)

    def _generate_prompt(self, subject: str, body: str) -> tuple[str, str, list[dict]]:
        system_prompt = (
            """
            You are an assistant that matches cause codes for emails based on provided context and examples. Interpret each email to return a structured JSON response.
            Each cause code has a description of relevant activities in the 'Atividades' field. Match the cause code to the email based on these descriptions.
            
            This is the JSON structure of the response you should return:
            
            {
                "cause_code": "",
                "summarized_issue": "",
                "reason": ""
            }
            """
        )

        prompt = f"""
                Email:
                Subject: {subject}
                Body: {body}
                """

        examples = []

        return system_prompt, prompt, examples

    def _interpret_email(
            self, system_prompt: str, prompt: str, examples: list[dict], context: str, cause_code: str
    ) -> dict[str, str | Any]:
        try:
            email_data_str = self.openai_client.interpret_email(system_prompt, prompt, examples, context, cause_code)
            return json.loads(email_data_str)
        except json.JSONDecodeError:
            print("Invalid JSON format received from AI. Retrying...")
            return {}
        except FailedToInterpretEmailException as e:
            print("Error occurred while calling the OpenAI API:", e)
            return self._default_response("")

    def _is_valid_cause_code(self, cause_code: str) -> bool:
        return bool(self.excel_util.get_data_by_cause_code(cause_code))

    def _default_response(self, body: str) -> dict:
        return {
            "cause_code": "N/A",
            "priority": "N/A",
            "brief_description": "N/A",
            "assignment": "N/A",
            "summarized_issue": "N/A",
            "reason": "N/A",
            "raw_email": body
        }

    def _construct_response(self, email_data: dict, body: str) -> dict:
        filtered_data = self.excel_util.get_data_by_cause_code(email_data['cause_code'])

        return {
            "cause_code": email_data['cause_code'],
            "priority": filtered_data.get('Priority', 'N/A'),
            "brief_description": filtered_data.get('Brief Description', 'N/A'),
            "assignment": filtered_data.get('Assignment', 'N/A'),
            "summarized_issue": email_data['summarized_issue'],
            "reason": email_data['reason'],
            "raw_email": body
        }
