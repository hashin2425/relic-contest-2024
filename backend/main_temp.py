""" フロントエンドと通信するためのAPIを提供するFastAPIアプリケーション """

import asyncio
import base64
from datetime import datetime
from typing import List

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn


class Message(BaseModel):
    """Pydanticモデル

    Attributes:
        role: メッセージの役割（userやsystemなど）
        content: メッセージの内容
    """

    role: str
    content: str


class MessagesRequest(BaseModel):
    """チャットリクエストのPydanticモデル

    Attributes:
        messages: メッセージのリスト
    """

    messages: List[Message]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_now_as_string() -> str:
    """現在時刻を文字列として取得する

    Returns:
        str: フォーマットされた現在時刻の文字列
    """
    now = datetime.now().replace(microsecond=0).isoformat()  # like: 2021-09-01T12:34:56
    return f"（Time: {now}）"


@app.get("/api/img/{img_id}")
async def get_img(img_id: str) -> FileResponse:
    """画像を取得するエンドポイント

    Args:
        img_id: 画像ID

    Returns:
        FileResponse: 画像ファイルのレスポンス
    """
    del img_id  # 未使用の引数を明示的に削除
    return FileResponse("sample-problem/sample-problem.png")


@app.get("/api/get-problems/{problem_id}")
async def get_problem(problem_id: int) -> dict:
    """指定されたIDの問題を取得するエンドポイント

    Args:
        problem_id: 問題ID

    Returns:
        dict: 問題の情報を含む辞書
    """
    del problem_id  # 未使用の引数を明示的に削除
    return {"problem": {"id": "1", "title": "問題1", "description": "問題1の説明", "imgUrl": "/api/img/sample-problem/"}}


@app.get("/api/get-problems")
async def get_problems() -> dict:
    """全ての問題を取得するエンドポイント

    Returns:
        dict: 問題のリストを含む辞書
    """
    return {
        "problems": [
            {"id": "1", "title": "問題1", "description": "問題1の説明", "imgUrl": "/api/img/sample-problem/"},
            {"id": "2", "title": "問題2", "description": "問題2の説明", "imgUrl": "/api/img/sample-problem/"},
            {"id": "3", "title": "問題3", "description": "問題3の説明", "imgUrl": "/api/img/sample-problem/"},
        ]
    }


@app.post("/api/chat")
async def return_message_from_chat(request: MessagesRequest) -> dict:
    """チャットメッセージに応答するエンドポイント

    Args:
        request: チャットリクエスト

    Returns:
        dict: チャットレスポンス
    """
    del request  # 未使用の引数を明示的に削除
    await asyncio.sleep(3)  # (テスト用)レスポンスを遅らせる
    return {"response": f"チャットのレスポンス結果が返されます。{get_now_as_string()}"}


@app.post("/api/analyze-image")
async def analyze_image(file: UploadFile) -> dict:
    """アップロードされた画像を分析するエンドポイント

    Args:
        file: アップロードされた画像ファイル

    Returns:
        dict: 画像分析結果

    Raises:
        HTTPException: サポートされていない画像形式の場合
    """
    # 画像がJPEGまたはPNG形式であることを確認
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG images are supported.")

    return {"description": f"与えられた画像の説明が返されます。{get_now_as_string()}"}


@app.post("/api/analyze-base64image")
async def analyze_base64image(base64_image: str) -> dict:
    """Base64エンコードされた画像を分析するエンドポイント

    Args:
        base64_image: Base64エンコードされた画像データ

    Returns:
        dict: 画像分析結果
    """
    del base64_image  # 未使用の引数を明示的に削除
    return {"description": f"与えられたBase64画像の説明が返されます。{get_now_as_string()}"}


@app.post("/api/create-image")
async def create_image(prompt: str) -> dict:
    """プロンプトから画像を生成するエンドポイント

    Args:
        prompt: 画像生成のためのプロンプト

    Returns:
        dict: 生成された画像のBase64エンコードデータ
    """
    del prompt  # 未使用の引数を明示的に削除
    encoded_bytes = base64.b64encode(b"dummy data")
    base64_image = encoded_bytes.decode("utf-8")
    return {"base64image": base64_image}


@app.get("/api/hello")
async def read_root() -> dict:
    """ヘルスチェック用のエンドポイント

    Returns:
        dict: 現在時刻を含むメッセージ
    """
    return {"message": f"Hello from FastAPI! {datetime.now()}"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
