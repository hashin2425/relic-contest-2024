""" GroqのAPIクライアントを提供するサービスモジュール """

import asyncio
from typing import Dict, List, Any
from app.utils.log_utils import logging

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logging("Groq API client is not available. Install with: pip install groq")


class GroqClient:
    """GroqのAPIクライアントを提供するサービスクラス"""

    def __init__(self, api_key: str):
        if not GROQ_AVAILABLE:
            raise ImportError("Groq package is not installed. Install with: pip install groq")
        # GroqのAPIクライアントを初期化
        self.client = Groq(api_key=api_key)

    async def chat(self, messages: List[Dict[str, Any]], max_tokens: int = 8192, temperature: float = 0.2) -> str:
        """GroqのAPIを呼び出してチャットの応答を取得"""
        try:
            loop = asyncio.get_running_loop()
            completion = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model="llama-3.2-90b-vision-preview",  # 使用するモデル
                    messages=messages,  # メッセージのリスト
                    max_tokens=max_tokens,  # 最大トークン数
                    temperature=temperature,  # 温度パラメータ（応答のランダム性）
                )
            )
            return completion.choices[0].message.content or ""
        except Exception as e:
            logging(f"Error in Groq chat: {e}")
            return ""
