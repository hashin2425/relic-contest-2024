""" OpenAI APIクライアントモジュール
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


class ChatGPTClient:
    """OpenAI APIクライアント"""

    def __init__(self):
        OPEN_AI_API_KEY = os.getenv("OPEN_AI_CHATGPT_API_KEY", "")
        OPEN_AI_API_VERSION = os.getenv("OPEN_AI_CHATGPT_API_VERSION", "")
        OPEN_AI_AZURE_ENDPOINT = os.getenv("OPEN_AI_CHATGPT_AZURE_ENDPOINT", "")
        OPEN_AI_DEPLOYMENT_NAME = os.getenv("OPEN_AI_CHATGPT_DEPLOYMENT_NAME", "")

        self.deployed_model = OPEN_AI_DEPLOYMENT_NAME
        self.client = AzureOpenAI(
            api_version=OPEN_AI_API_VERSION,
            api_key=OPEN_AI_API_KEY,
            azure_endpoint=f"https://{OPEN_AI_AZURE_ENDPOINT}.openai.azure.com/",
        )

    def chat(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.deployed_model or "gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message},
            ],
        )
        return response.choices[0].message.content or ""
