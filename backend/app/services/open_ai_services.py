""" OpenAI APIクライアントモジュール
"""

import os
import json
import requests
from openai import AzureOpenAI
from dotenv import load_dotenv
from app.utils.log_utils import logging

load_dotenv()


class ChatGPTClient:
    """OpenAI APIクライアント"""

    def __init__(self):
        OPEN_AI_API_KEY = os.getenv("OPEN_AI_CHATGPT_API_KEY", "")
        OPEN_AI_API_VERSION = os.getenv("OPEN_AI_CHATGPT_API_VERSION", "")
        OPEN_AI_AZURE_ENDPOINT = os.getenv("OPEN_AI_CHATGPT_AZURE_ENDPOINT", "")
        OPEN_AI_DEPLOYMENT_NAME = os.getenv("OPEN_AI_CHATGPT_DEPLOYMENT_NAME", "")

        if "" in [OPEN_AI_API_KEY, OPEN_AI_API_VERSION, OPEN_AI_AZURE_ENDPOINT]:
            logging("ChatGPTClient.__init__: ", "API Key or Version or Endpoint is not set.")

        self.client = AzureOpenAI(
            api_version=OPEN_AI_API_VERSION,
            api_key=OPEN_AI_API_KEY,
            azure_endpoint=f"https://{OPEN_AI_AZURE_ENDPOINT}.openai.azure.com/",
        )

    def chat(self, message: str) -> str:
        OPEN_AI_DEPLOYMENT_NAME = os.getenv("OPEN_AI_CHATGPT_DEPLOYMENT_NAME", "")
        try:
            response = self.client.chat.completions.create(
                model=OPEN_AI_DEPLOYMENT_NAME or "gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": message},
                ],
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logging("ChatGPTClient.chat: ", e)
            return ""


class DallE3Client:
    """OpenAI DALL-E2 APIクライアント"""

    def __init__(self):
        OPEN_AI_API_KEY = os.getenv("OPEN_AI_DALLE3_API_KEY", "")
        OPEN_AI_API_VERSION = os.getenv("OPEN_AI_DALLE3_API_VERSION", "")
        OPEN_AI_AZURE_ENDPOINT = os.getenv("OPEN_AI_DALLE3_AZURE_ENDPOINT", "")
        OPEN_AI_DEPLOYMENT_NAME = os.getenv("OPEN_AI_DALLE3_DEPLOYMENT_NAME", "")

        if "" in [OPEN_AI_API_KEY, OPEN_AI_API_VERSION, OPEN_AI_AZURE_ENDPOINT, OPEN_AI_DEPLOYMENT_NAME]:
            logging("DallE3Client.__init__: ", "API Key or Version or Endpoint is not set.")

        self.client = AzureOpenAI(
            api_version=OPEN_AI_API_VERSION,
            api_key=OPEN_AI_API_KEY,
            azure_endpoint=f"https://{OPEN_AI_AZURE_ENDPOINT}.openai.azure.com/",
        )

    def generate(self, prompt: str, filename: str) -> str:
        try:
            OPEN_AI_DEPLOYMENT_NAME = os.getenv("OPEN_AI_DALLE3_DEPLOYMENT_NAME", "")
            BASE_IMAGE_DIR = os.getenv("BASE_IMAGE_DIR", "app/data/images")
            result = self.client.images.generate(
                model=OPEN_AI_DEPLOYMENT_NAME,
                prompt=prompt,
                n=1,  # 生成数
            )

            json_response = json.loads(result.model_dump_json())
            image_path = os.path.join(BASE_IMAGE_DIR, f"{filename}.png")
            image_url = json_response["data"][0]["url"]
            generated_image = requests.get(image_url, timeout=30).content

            with open(image_path, "wb") as image_file:
                image_file.write(generated_image)

            logging("DallE3Client.generate: ", image_path)

            return image_path
        except Exception as e:
            logging("DallE3Client.generate", e)
            return ""
