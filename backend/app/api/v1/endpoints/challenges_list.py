""" チャレンジに関するエンドポイントを記述するモジュール """

from fastapi import APIRouter
from app.core.mongodb_core import db
from app.core.security import require_auth
from app.utils.log_utils import logging
from app.utils.challenge_utils import convert_challenge_to_json_item

api_router = APIRouter()

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
@require_auth()
async def get_challenge(challenge_id: str):
    """チャレンジ詳細を取得するエンドポイント"""
    challenge_data = await db.get_challenge_by_id(challenge_id)

    if challenge_data is None:
        challenge_data = {}
    else:
        challenge_data = convert_challenge_to_json_item(challenge_data)

    response = {"problem": challenge_data}
    return response
