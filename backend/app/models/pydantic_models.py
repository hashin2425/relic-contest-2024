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
