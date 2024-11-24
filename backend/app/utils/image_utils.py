""" 画像処理に関するユーティリティ関数を提供するモジュール """

import base64

from fastapi import UploadFile


def encode_image(file: UploadFile) -> str:
    """画像をBase64エンコードするユーティリティ関数
    画像ファイルを読み込み、Base64形式でエンコードする
    """
    return base64.b64encode(file.file.read()).decode("utf-8")
