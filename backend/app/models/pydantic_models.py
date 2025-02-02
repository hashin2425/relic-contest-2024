""" Pydantic models definition module """

from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    """Message model for AI communication"""
    role: str
    content: str


class MessagesRequest(BaseModel):
    """Messages request model"""
    messages: List[Message]


class ChallengeRequest(BaseModel):
    """Challenge start request"""
    challenge_id: str


class SubmitRequest(BaseModel):
    """Challenge submission request"""
    submission: str


class UserSubmission(BaseModel):
    """Challenge submission record"""
    timestamp: str
    content: str
    score: int


class UserChallenge(BaseModel):
    """User's active challenge"""
    challenge_id: str
    challenge: dict
    submissions: List[UserSubmission] = []
    last_submitted_text: str = ""
    last_submitted_unix_time: float = 0
    last_submission_score: int = 0
    generated_images: List[str] = []
    started_at: datetime
    updated_at: datetime


class UserChallenges(BaseModel):
    """User's challenge history"""
    user_id: str
    active_challenge: Optional[UserChallenge] = None
    completed_challenges: List[str] = []
    created_at: datetime
    updated_at: datetime
