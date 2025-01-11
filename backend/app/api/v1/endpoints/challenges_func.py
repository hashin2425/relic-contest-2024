""" チャレンジに取り組んでいるユーザーに機能を提供するエンドポイント """

import os
import base64
import requests
from fastapi import APIRouter, HTTPException, UploadFile
from app.models.pydantic_models import MessagesRequest
from app.services.groq_services import GroqClient
from app.utils.image_utils import encode_image
from app.core.security import require_auth

api_router = APIRouter()


@api_router.post("/chat")
@require_auth()
async def return_message_from_chat(request: MessagesRequest):
    """チャットリクエストをGroqクライアントに送信し、応答を返す"""
    groq_client = GroqClient(api_key=os.getenv("GROQ_API_KEY", ""))
    response = groq_client.chat(messages=request.messages)
    return {"response": response}


@api_router.post("/analyze-image")
@require_auth()
async def analyze_image(file: UploadFile):
    """画像がJPEGまたはPNG形式であることを確認"""
    groq_client = GroqClient(api_key=os.getenv("GROQ_API_KEY", ""))
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG images are supported.")

    # 画像をBase64形式にエンコード
    base64_image = encode_image(file)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "この画像は何を表していますか？"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        },
    ]
    # Groqに画像を渡して、説明を取得
    description = groq_client.chat(messages)
    return {"description": description}


@api_router.post("/analyze-base64image")
@require_auth()
async def analyze_base64image(base64_image: str):
    """Base64エンコードされた画像をGroqに渡して説明を取得"""
    groq_client = GroqClient(api_key=os.getenv("GROQ_API_KEY", ""))
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "この画像は何を表していますか？"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        },
    ]
    description = groq_client.chat(messages)
    return {"description": description}


@api_router.post("/create-image")
@require_auth()
async def create_image(prompt: str):
    """画像生成のためのAPIキーとURL"""
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

    headers = {"x-api-key": api_key}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    if response.ok:
        # 生成された画像をBase64エンコードして返す
        base64_image = base64.b64encode(response.content).decode("utf-8")
        return {"base64image": base64_image}

    # エラーが発生した場合
    return {"error": "Image generation failed", "status_code": response.status_code}
