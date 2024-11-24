""" フロントエンドと通信するためのAPIを提供するFastAPIアプリケーション """

import base64
from datetime import datetime
from typing import List

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn


class Message(BaseModel):
    """Pydanticモデル"""

    role: str  # メッセージの役割（userやsystemなど）
    content: str  # メッセージの内容


class MessagesRequest(BaseModel):
    """チャットリクエストのPydanticモデル"""

    messages: List[Message]  # メッセージのリスト


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_now_as_string():
    now = datetime.now().replace(microsecond=0).isoformat()  # like: 2021-09-01T12:34:56
    return f"（Time: {now}）"


@app.get("/api/img/{img_id}")
async def get_img(img_id: str):
    return FileResponse("sample-problem/sample-problem.png")


@app.get("/api/get-problems/{problem_id}")
async def get_problem(problem_id: int):
    return {"problem": {"id": "1", "title": "問題1", "description": "問題1の説明", "imgUrl": "/api/img/sample-problem/"}}


@app.get("/api/get-problems")
async def get_problems():
    return {
        "problems": [
            {"id": "1", "title": "問題1", "description": "問題1の説明", "imgUrl": "/api/img/sample-problem/"},
            {"id": "2", "title": "問題2", "description": "問題2の説明", "imgUrl": "/api/img/sample-problem/"},
            {"id": "3", "title": "問題3", "description": "問題3の説明", "imgUrl": "/api/img/sample-problem/"},
        ]
    }


@app.post("/api/chat")
async def return_message_from_chat(request: MessagesRequest):
    return {"response": f"チャットのレスポンス結果が返されます。{get_now_as_string()}"}


@app.post("/api/analyze-image")
async def analyze_image(file: UploadFile):
    # 画像がJPEGまたはPNG形式であることを確認
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG images are supported.")

    return {"description": f"与えられた画像の説明が返されます。{get_now_as_string()}"}


@app.post("/api/analyze-base64image")
async def analyze_base64image(base64_image: str):
    return {"description": f"与えられたBase64画像の説明が返されます。{get_now_as_string()}"}


@app.post("/api/create-image")
async def create_image(prompt: str):
    base64_image = base64.b64encode().decode("utf-8")
    return {"base64image": base64_image}


@app.get("/api/hello")
async def read_root():
    return {"message": f"Hello from FastAPI! {datetime.now()}"}


# アプリケーションを実行
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
