""" OpenAI APIクライアントモジュール
"""

import os
import json
import asyncio
import aiohttp
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

    async def chat(self, message: str) -> str:
        """Async chat completion"""
        OPEN_AI_DEPLOYMENT_NAME = os.getenv("OPEN_AI_CHATGPT_DEPLOYMENT_NAME", "")
        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=OPEN_AI_DEPLOYMENT_NAME or "gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": message},
                    ],
                )
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

    async def generate(self, prompt: str, filename: str) -> bool:
        """Asynchronously generate image"""
        try:
            OPEN_AI_DEPLOYMENT_NAME = os.getenv("OPEN_AI_DALLE3_DEPLOYMENT_NAME", "")
            BASE_IMAGE_DIR = os.getenv("BASE_IMAGE_DIR", "app/data/images")

            # Generate image URL asynchronously
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.client.images.generate(
                    model=OPEN_AI_DEPLOYMENT_NAME,
                    prompt=prompt,
                    n=1,  # 生成数
                )
            )

            # Parse the response
            json_response = json.loads(result.model_dump_json())
            image_path = os.path.join(BASE_IMAGE_DIR, f"{filename}.png")
            image_url = json_response["data"][0]["url"]

            # Download image asynchronously
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        with open(image_path, "wb") as image_file:
                            image_file.write(image_data)
                        logging("DallE3Client.generate: ", image_path)
                        return True
                    else:
                        logging("DallE3Client.generate: Failed to download image")
                        return False

        except Exception as e:
            logging("DallE3Client.generate", e)
            return False
