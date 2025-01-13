""" MongoDBを操作するクラス """

from datetime import datetime
from typing import List
import json
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.mongodb_models import Challenge
from app.core.exceptions import ServiceUnavailableError
from app.utils.log_utils import logging


load_dotenv()


class MongoDB:
    """MongoDBを操作するクラス"""

    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        """MongoDBに接続"""
        MONGO_USER = os.getenv("MONGO_USER", "")
        MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")
        MONGO_URL = os.getenv("MONGO_URL", "mongodb:27017")

        if MONGO_USER == "" or MONGO_PASSWORD == "":
            raise ValueError("MongoDB username and password are required")

        mongodb_url = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_URL}/challenges_db?authSource=admin"
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client.challenges_db

        # 接続テスト
        try:
            await self.client.admin.command("ping")
            logging("Successfully connected to MongoDB")
        except Exception as e:
            logging(f"Failed to connect to MongoDB: {e}")
            raise

    async def close(self):
        """MongoDB接続を閉じる"""
        if self.client:
            self.client.close()

    async def init_challenges(self):
        """初期チャレンジデータの読み込みと保存"""
        if self.db is None or self.db.challenges is None:
            return

        if await self.db.challenges.count_documents({}) > 0:
            return

        try:
            with open("app/data/initial_challenges.json", "r", encoding="utf-8") as f:
                challenges = json.load(f)

            for challenge in challenges:
                challenge["created_at"] = datetime.utcnow()
                await self.db.challenges.insert_one(challenge)
        except Exception as e:
            logging(f"Error loading initial challenges: {e}")

    async def get_all_challenges(self) -> List[Challenge]:
        """全チャレンジを取得"""
        if self.db is None or self.db.challenges is None:
            raise ServiceUnavailableError("Could not connect to the service")

        cursor = self.db.challenges.find()
        challenges = await cursor.to_list(length=None)
        return [Challenge(**challenge) for challenge in challenges]

    async def get_challenge_by_id(self, challenge_id: str) -> Challenge:
        """IDによるチャレンジ取得"""
        if self.db is None or self.db.challenges is None:
            raise ServiceUnavailableError("Could not connect to the service")

        challenge = await self.db.challenges.find_one({"_id": challenge_id})
        if not challenge:
            raise ServiceUnavailableError("Could not find the challenge")

        return Challenge(**challenge)


# グローバルなMongoDBインスタンス
db = MongoDB()
