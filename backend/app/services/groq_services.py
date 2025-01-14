""" GroqのAPIクライアントを提供するサービスモジュール """

from typing import List
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam


class GroqClient:
    """GroqのAPIクライアントを提供するサービスクラス"""

    def __init__(self, api_key: str):
        # GroqのAPIクライアントを初期化
        self.client = Groq(api_key=api_key)

    def chat(self, messages: List[ChatCompletionMessageParam], max_tokens: int = 8192, temperature: float = 0.2) -> str:
        """GroqのAPIを呼び出してチャットの応答を取得"""
        completion = self.client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",  # 使用するモデル
            messages=messages,  # メッセージのリスト
            max_tokens=max_tokens,  # 最大トークン数
            temperature=temperature,  # 温度パラメータ（応答のランダム性）
        )
        return completion.choices[0].message.content or ""
