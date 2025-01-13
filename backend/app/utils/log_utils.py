""" ログ出力関連のユーティリティ関数を提供するモジュール
    TODO: いったん仮で作成したもので、後で変更する可能性がある
"""

from typing import Any
from app.utils.time_utils import get_jst_now


def logging(*args: Any) -> None:
    """ログを出力する"""
    print(get_jst_now().isoformat(), end=": ")
    print(*args)
