""" 画像処理に関するユーティリティ関数を提供するモジュール """

import base64
import hashlib

from fastapi import UploadFile


def encode_image(file: UploadFile) -> str:
    """
    画像をBase64エンコードするユーティリティ関数
    画像ファイルを読み込み、Base64形式でエンコードする
    """
    return base64.b64encode(file.file.read()).decode("utf-8")


def image_bytes_to_sha256(image: bytes) -> str:
    """
    画像のハッシュ値を取得するユーティリティ関数
    画像のBase64エンコード文字列を受け取り、ハッシュ値を返す
    """
    return hashlib.sha256(image).hexdigest()
