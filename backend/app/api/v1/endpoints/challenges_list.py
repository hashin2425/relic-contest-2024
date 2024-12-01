""" チャレンジに関するエンドポイントを記述するモジュール """

from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/get-all")
async def get_challenges():
    """チャレンジ一覧を取得するエンドポイント"""
    return {"message": "Challenges list."}


@api_router.get("/get/{challenge_id}")
async def get_challenge(challenge_id: int):
    """チャレンジ詳細を取得するエンドポイント"""
    return {"message": f"Challenge ID: {challenge_id}"}
