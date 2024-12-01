"""FastAPIアプリケーションのメインファイル"""

from datetime import datetime
import os

import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.v1.endpoints import challenges_list as challenges_list_v1, challenges_func as challenges_func_v1, users as users_v1, image as image_v1

dotenv.load_dotenv()
server_start_time = datetime.now()

# FastAPIアプリケーションの作成
app = FastAPI(
    title=os.getenv("PROJECT_NAME", "relic-contest-2024"),
    description=os.getenv("PROJECT_DESCRIPTION", "relic-contest-2024"),
    version=os.getenv("PROJECT_VERSION", "1.0.0"),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # フロントエンドのURL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(
    challenges_list_v1.api_router,
    prefix="/api/challenges-list",
    tags=["challenges"],
)
app.include_router(
    challenges_func_v1.api_router,
    prefix="/api/challenges-func",
    tags=["challenges"],
)
app.include_router(
    users_v1.api_router,
    prefix="/api/users",
    tags=["users"],
)
app.include_router(
    image_v1.api_router,
    prefix="/api/img",
    tags=["image"],
)


@app.get("/health-check", tags=["others"])
async def health_check():
    """ヘルスチェック用のエンドポイント"""
    return {
        "message": "Server is running.",
        "server_internal_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "server_running_time": str(datetime.now() - server_start_time),
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=5000,
        reload=os.getenv("DEBUG", "False") == "True",
        access_log=os.getenv("DEBUG", "False") == "True",
    )
