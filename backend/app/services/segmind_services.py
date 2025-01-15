""" Segmind APIを利用して画像生成を行うためのサービスモジュール
"""

import os
import base64
import requests

from dotenv import load_dotenv
from app.utils.log_utils import logging

load_dotenv()


def create_image(prompt: str, filename: str) -> str:
    """画像生成のためのAPIキーとURL"""
    BASE_IMAGE_DIR = os.getenv("BASE_IMAGE_DIR", "app/data/images")

    api_key = os.getenv("SEGMIND_KEY")
    url = "https://api.segmind.com/v1/sdxl1.0-newreality-lightning"
    payload = {
        "prompt": prompt,  # 画像生成のプロンプト
        "negative_prompt": "((close up)),(octane render, render, drawing, bad photo, bad photography:1.3)",  # ネガティブプロンプト
        "samples": 1,  # 生成する画像の数
        "scheduler": "DPM++ SDE",  # スケジューラー設定
        "num_inference_steps": 7,  # 推論ステップ数
        "guidance_scale": 1,  # ガイダンススケール
        "seed": 1220429729,  # ランダムシード
        "img_width": 1024,  # 画像の幅
        "img_height": 1024,  # 画像の高さ
        "base64": False,  # Base64で返すかどうか
    }

    logging("Segmind_services.create_image: ", prompt)
    response = requests.post(
        url,
        json=payload,
        headers={"x-api-key": api_key},
        timeout=30,
    )
    if response.ok:
        image_path = os.path.join(BASE_IMAGE_DIR, f"{filename}.png")
        with open(image_path, "wb") as image_file:
            image_file.write(response.content)
        logging("Segmind_services.create_image: ", image_path)
        return image_path
    else:
        logging("Segmind_services.create_image: ", response.text, response.status_code)
        return ""
