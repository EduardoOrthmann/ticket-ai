import json
from openai import AzureOpenAI


class OpenAIClient:
    def __init__(self, openai_api_key: str, openai_api_version: str, azure_endpoint: str, openai_model: str) -> None:
        self.client = AzureOpenAI(api_key=openai_api_key, api_version=openai_api_version, azure_endpoint=azure_endpoint)
        self.model = openai_model

    def interpret_email(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an assistant that generates cause codes for emails based on context provided."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )

            data = response.choices[0].message.content
            parsed_data = json.loads(data)

            if "cause_code" in parsed_data and "summarized_issue" in parsed_data and "raw_email" in parsed_data:
                return data

            print("Received response in unexpected format:", data)
            return '{"cause_code": "N/A", "summarized_issue": "N/A", "raw_email": ""}'

        except Exception as e:
            print("Error occurred while calling the OpenAI API:", e)
            return '{"cause_code": "N/A", "summarized_issue": "N/A", "raw_email": ""}'
