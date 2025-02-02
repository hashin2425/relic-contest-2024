""" MongoDB operations class """

from datetime import datetime
from typing import List, Optional
import json
import os
from bson import ObjectId

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.mongodb_models import Challenge
from app.models.auth_models import UserInDB, UserCreate
from app.core.exceptions import ServiceUnavailableError
from app.utils.log_utils import logging


load_dotenv()


class MongoDB:
    """MongoDB operations class"""

    def __init__(self):
        self.client = None
        self.db = None
        self.users = None
        self.challenges = None

    async def connect(self):
        """Connect to MongoDB"""
        MONGO_USER = os.getenv("MONGO_USER", "")
        MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")
        MONGO_URL = os.getenv("MONGO_URL", "mongodb:27017")

        if MONGO_USER == "" or MONGO_PASSWORD == "":
            raise ValueError("MongoDB username and password are required")

        mongodb_url = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_URL}/challenges_db?authSource=admin"
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client.challenges_db
        
        # Initialize collections
        self.users = self.db.users
        self.challenges = self.db.challenges
        self.user_challenges = self.db.user_challenges

        # Create indexes
        await self.users.create_index("email", unique=True)
        await self.user_challenges.create_index([
            ("user_id", 1),
            ("challenge_id", 1)
        ], unique=True)
        await self.user_challenges.create_index([
            ("user_id", 1),
            ("completed_at", 1)
        ])

        # Connection test
        try:
            await self.client.admin.command("ping")
            logging("Successfully connected to MongoDB")
        except Exception as e:
            logging(f"Failed to connect to MongoDB: {e}")
            raise

    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()

    # User operations
    async def create_user(self, user: UserCreate) -> UserInDB:
        """Create a new user"""
        if self.users is None:
            raise ServiceUnavailableError("Could not connect to the service")

        user_dict = user.dict()
        user_dict["created_at"] = datetime.utcnow()
        result = await self.users.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        return UserInDB(**user_dict)

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email"""
        if self.users is None:
            raise ServiceUnavailableError("Could not connect to the service")
        return await self.users.find_one({"email": email})

    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        if self.users is None:
            raise ServiceUnavailableError("Could not connect to the service")
        return await self.users.find_one({"_id": ObjectId(user_id)})

    async def update_user_last_login(self, user_id: str):
        """Update user's last login time"""
        if self.users is None:
            raise ServiceUnavailableError("Could not connect to the service")
        await self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_login": datetime.utcnow()}}
        )

    # User Challenge Operations
    async def get_user_challenge(self, user_id: str, challenge_id: str) -> Optional[dict]:
        """Get a specific user challenge"""
        if self.user_challenges is None:
            raise ServiceUnavailableError("Could not connect to the service")
        return await self.user_challenges.find_one({
            "user_id": user_id,
            "challenge_id": challenge_id
        })

    async def get_active_user_challenge(self, user_id: str) -> Optional[dict]:
        """Get user's active challenge"""
        if self.user_challenges is None:
            raise ServiceUnavailableError("Could not connect to the service")
        return await self.user_challenges.find_one({
            "user_id": user_id,
            "completed_at": None
        })

    async def create_user_challenge(self, user_id: str, challenge_id: str, challenge: dict) -> dict:
        """Create a new user challenge"""
        if self.user_challenges is None:
            raise ServiceUnavailableError("Could not connect to the service")
        challenge_data = {
            "user_id": user_id,
            "challenge_id": challenge_id,
            "challenge": challenge,
            "submissions": [],
            "last_submitted_text": "",
            "last_submitted_unix_time": datetime.utcnow().timestamp(),
            "last_submission_score": 0,
            "generated_images": [],
            "started_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "completed_at": None
        }
        result = await self.user_challenges.insert_one(challenge_data)
        challenge_data["_id"] = result.inserted_id
        return challenge_data

    async def update_user_challenge(
        self,
        user_id: str,
        challenge_id: str,
        submission: dict,
        last_score: int,
        last_submission: str
    ) -> None:
        """Update user challenge with new submission"""
        if self.user_challenges is None:
            raise ServiceUnavailableError("Could not connect to the service")
        now = datetime.utcnow()
        await self.user_challenges.update_one(
            {
                "user_id": user_id,
                "challenge_id": challenge_id
            },
            {
                "$push": {"submissions": submission},
                "$set": {
                    "last_submitted_text": last_submission,
                    "last_submitted_unix_time": now.timestamp(),
                    "last_submission_score": last_score,
                    "updated_at": now
                }
            }
        )

    # Challenge operations
    async def init_challenges(self):
        """Load and save initial challenge data"""
        if self.db is None or self.challenges is None:
            return

        try:
            with open("app/data/initial_challenges.json", "r", encoding="utf-8") as f:
                challenges = json.load(f)

            for challenge in challenges:
                challenge["created_at"] = datetime.utcnow()
                logging(challenge)
                await self.challenges.delete_one({"_id": challenge["_id"]})
                await self.challenges.insert_one(challenge)
        except Exception as e:
            logging(f"Error loading initial challenges: {e}")

    async def get_all_challenges(self) -> List[Challenge]:
        """Get all challenges"""
        if self.db is None or self.challenges is None:
            raise ServiceUnavailableError("Could not connect to the service")

        cursor = self.challenges.find()
        challenges = await cursor.to_list(length=None)
        return [Challenge(**challenge) for challenge in challenges]

    async def get_challenge_by_id(self, challenge_id: str) -> Challenge:
        """Get challenge by ID"""
        if self.db is None or self.challenges is None:
            raise ServiceUnavailableError("Could not connect to the service")

        challenge = await self.challenges.find_one({"_id": challenge_id})
        if not challenge:
            raise ServiceUnavailableError("Could not find the challenge")

        return Challenge(**challenge)


# Global MongoDB instance
db = MongoDB()
