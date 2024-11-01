from openai import AzureOpenAI
from pandas import DataFrame

from utils.excel_util import ExcelUtil


class OpenAIClient:
    def __init__(self, openai_api_key: str, openai_api_version: str, azure_endpoint: str, openai_model: str) -> None:
        self.client = AzureOpenAI(api_key=openai_api_key, api_version=openai_api_version, azure_endpoint=azure_endpoint)
        self.model = openai_model

    def interpret_email(self, ai_action: str, subject: str, body: str, context: DataFrame | str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": ai_action
                },
                {
                    "role": "user",
                    "content": f"Context: {context} \n\n Email: \n\n Subject: {subject}\nBody: {body}",
                }
            ],
        )

        data = response.choices[0].message.content
        return data
