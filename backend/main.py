"""FastAPIアプリケーションのメインファイル"""

from datetime import datetime
import os

import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.v1.endpoints import (
    challenges_list as challenges_list_v1,
    challenges_func as challenges_func_v1,
    users as users_v1,
    image as image_v1,
    auth as auth_v1,
)
from app.core.mongodb_core import db
from app.utils.log_utils import logging

logging("Starting FastAPI server...")
dotenv.load_dotenv()
server_start_time = datetime.now()

# FastAPIアプリケーションの作成
app = FastAPI(
    title=os.getenv("PROJECT_NAME", "relic-contest-2024"),
    description=os.getenv("PROJECT_DESCRIPTION", "relic-contest-2024"),
    version=os.getenv("PROJECT_VERSION", "1.0.0"),
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    """アプリケーション起動時の処理"""
    if os.getenv("PASS_INITIALIZE_MONGO_SETUP", "True") == "False":
        logging("Initializing MongoDB setup...")
        await db.connect()
        await db.init_challenges()
    else:
        logging("Skip initializing MongoDB setup.")


@app.on_event("shutdown")
async def shutdown_db_client():
    """アプリケーション終了時の処理"""
    await db.close()


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
app.include_router(
    auth_v1.api_router,
    prefix="/api/auth",
    tags=["auth"],
)


@app.get("/", tags=["others"])
@app.get("/api", tags=["others"])
@app.get("/health-check", tags=["others"])
@app.get("/api/health-check", tags=["others"])
async def health_check():
    """ヘルスチェック用のエンドポイント"""
    response = {"message": "Server is running."}

    if os.getenv("DEBUG", "False") == "True":
        response["server_internal_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        server_running_time = datetime.now() - server_start_time
        server_running_time_seconds = int(server_running_time.total_seconds())
        response["server_running_time"] = f"{server_running_time_seconds // 3600}h {(server_running_time_seconds % 3600) // 60}m {server_running_time_seconds % 60}s"

    return response


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=5000,
        reload=os.getenv("DEBUG", "False") == "True",
        access_log=os.getenv("DEBUG", "False") == "True",
    )
