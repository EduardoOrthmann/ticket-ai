from openai import AzureOpenAI

from exceptions.failed_to_interpret_email_exception import FailedToInterpretEmailException


class OpenAIClient:
    def __init__(self, openai_api_key: str, openai_api_version: str, azure_endpoint: str, openai_model: str) -> None:
        self.client = AzureOpenAI(api_key=openai_api_key, api_version=openai_api_version, azure_endpoint=azure_endpoint)
        self.model = openai_model

    def interpret_email(self, system_prompt: str, prompt: str, examples: list[dict], context: str, cause_code: str) -> str:
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                *examples,
                {"role": "assistant", "content": f"Here is the provided context: {context}"},
            ]

            if cause_code:
                messages.append({
                    "role": "user",
                    "content": f"Previous cause_code '{cause_code}' was invalid. Please try another."
                })

            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0
            )

            return response.choices[0].message.content

        except Exception as e:
            raise FailedToInterpretEmailException(str(e))
