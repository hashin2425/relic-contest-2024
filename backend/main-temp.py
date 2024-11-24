from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import base64
import uvicorn
import requests
from groq import Groq
from datetime import datetime


# 画像をBase64エンコードするユーティリティ関数
def encode_image(file: UploadFile) -> str:
    # 画像ファイルを読み込み、Base64形式でエンコード
    return base64.b64encode(file.file.read()).decode("utf-8")


# Pydanticモデル（入力のバリデーション用）
class Message(BaseModel):
    role: str  # メッセージの役割（userやsystemなど）
    content: str  # メッセージの内容


class MessagesRequest(BaseModel):
    messages: List[Message]  # メッセージのリスト


# Groqクライアントクラス
class GroqClient:
    def __init__(self, api_key: str):
        # GroqのAPIクライアントを初期化
        self.client = Groq(api_key=api_key)

    def chat(self, messages: List[dict], max_tokens: int = 8192, temperature: float = 0.2) -> str:
        # GroqのAPIを呼び出してチャットの応答を取得
        completion = self.client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",  # 使用するモデル
            messages=messages,  # メッセージのリスト
            max_tokens=max_tokens,  # 最大トークン数
            temperature=temperature,  # 温度パラメータ（応答のランダム性）
        )
        # 生成された応答の内容を返す
        return completion.choices[0].message.content


# FastAPIアプリケーションの初期化
app = FastAPI()

# CORSミドルウェアの設定（フロントエンドとの通信を許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groqクライアントのインスタンス作成
groq_client = GroqClient(api_key=os.getenv("GROQ_KEY"))


@app.post("/api/chat")
async def return_message_from_chat(request: MessagesRequest):
    # チャットリクエストをGroqクライアントに送信し、応答を返す
    response = groq_client.chat(messages=request.messages)
    return {"response": response}


@app.post("/api/analyze-image")
async def analyze_image(file: UploadFile):
    # 画像がJPEGまたはPNG形式であることを確認
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG images are supported.")

    # 画像をBase64形式にエンコード
    base64_image = encode_image(file)
    messages = [{"role": "user", "content": [{"type": "text", "text": "この画像は何を表していますか？"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}]
    # Groqに画像を渡して、説明を取得
    description = groq_client.chat(messages)
    return {"description": description}


@app.post("/api/analyze-base64image")
async def analyze_base64image(base64_image: str):
    # Base64エンコードされた画像をGroqに渡して説明を取得
    messages = [{"role": "user", "content": [{"type": "text", "text": "この画像は何を表していますか？"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}]
    description = groq_client.chat(messages)
    return {"description": description}


@app.post("/api/create-image")
async def create_image(prompt: str):
    # 画像生成のためのAPIキーとURL
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
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        # 生成された画像をBase64エンコードして返す
        base64_image = base64.b64encode(response.content).decode("utf-8")
        return {"base64image": base64_image}
    else:
        # エラーが発生した場合
        return {"error": "Image generation failed", "status_code": response.status_code}


@app.get("/api/hello")
async def read_root():
    return {"message": f"Hello from FastAPI! {datetime.now()}"}


# アプリケーションを実行
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
