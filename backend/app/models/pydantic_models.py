""" Pydanticモデルを定義するモジュール """

from typing import List

from pydantic import BaseModel


class Message(BaseModel):
    """Pydanticモデル（入力のバリデーション用）"""

    role: str  # メッセージの役割（userやsystemなど）
    content: str  # メッセージの内容


class MessagesRequest(BaseModel):
    """Pydanticモデル（入力のバリデーション用）"""

    messages: List[Message]  # メッセージのリスト


class ChallengeRequest(BaseModel):
    """チャレンジを開始するためのリクエスト"""

    challenge_id: str


class SubmitRequest(BaseModel):
    """チャレンジの提出リクエスト"""

    submission: str


class UserChallenges:
    """ユーザーが取り組んでいるチャレンジを管理するクラス"""

    def __init__(self, now_challenge_id: str, now_challenge: dict):
        self.now_challenge_id = now_challenge_id
        self.now_challenge = now_challenge
        self.submissions = []  # [{"timestamp": "2021-09-01T00:00:00", "content": "Hello, World!", "score": 100}, ...]
        self.last_submitted_unix_time = 0
        self.last_submitted_text = ""
        self.last_submission_score = 0
        self.generated_image = []  # [{"timestamp": "2021-09-01T00:00:00", "base64": "base64image"}, ...]
