""" チャレンジに関するエンドポイントを記述するモジュール """

from fastapi import APIRouter
from app.core.mongodb_core import db


api_router = APIRouter()


def convert_challenge_to_json_item(challenge) -> dict:
    """ChallengeモデルをJSONに変換する"""
    return {
        "id": str(challenge.id),
        "title": challenge.title,
        "imgUrl": challenge.image_path,
        "description": "",  # 未対応
    }


@api_router.get("/get-all")
async def get_challenges():
    """チャレンジ一覧を取得するエンドポイント"""
    challenge_data = await db.get_all_challenges()

    if challenge_data is None:
        challenge_data = []
    else:
        challenge_data = [convert_challenge_to_json_item(challenge) for challenge in challenge_data]

    response = {"problems": challenge_data}
    return response


@api_router.get("/get/{challenge_id}")
async def get_challenge(challenge_id: str):
    """チャレンジ詳細を取得するエンドポイント"""
    challenge_data = await db.get_challenge_by_id(challenge_id)

    if challenge_data is None:
        challenge_data = {}
    else:
        challenge_data = convert_challenge_to_json_item(challenge_data)

    response = {"problem": challenge_data}
    return response
