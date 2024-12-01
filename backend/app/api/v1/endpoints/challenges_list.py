""" チャレンジに関するエンドポイントを記述するモジュール """

from fastapi import APIRouter
from app.core.mongodb_core import db

api_router = APIRouter()


@api_router.get("/get-all")
async def get_challenges():
    """チャレンジ一覧を取得するエンドポイント"""
    return await db.get_all_challenges()


@api_router.get("/get/{challenge_id}")
async def get_challenge(challenge_id: str):
    """チャレンジ詳細を取得するエンドポイント"""
    return await db.get_challenge_by_id(challenge_id)
