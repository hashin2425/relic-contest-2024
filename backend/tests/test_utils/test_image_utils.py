""" test for /backend/app/utils/image_utils.py """

import unittest
from unittest.mock import Mock, patch
import base64
import io
import hashlib
from fastapi import UploadFile

from app.utils.image_utils import encode_image, image_bytes_to_sha256


class TestImageUtils(unittest.TestCase):
    """/backend/app/utils/image_utils.py test"""

    def setUp(self):
        """テストの前準備"""
        # テスト用のダミー画像データ
        self.test_image_data = b"dummy image data"

        # UploadFileのモック作成
        self.mock_file = Mock(spec=UploadFile)
        self.mock_file.file = io.BytesIO(self.test_image_data)

    def test_encode_image(self):
        """encode_image関数のテスト"""
        # 期待される結果を計算
        expected_encoded = base64.b64encode(self.test_image_data).decode("utf-8")

        # 関数を実行
        result = encode_image(self.mock_file)

        # 結果を検証
        self.assertEqual(result, expected_encoded)

        # ファイルが読み込まれたことを確認
        self.mock_file.file.seek(0)  # ファイルポインタをリセット

    def test_image_bytes_to_sha256(self):
        """image_bytes_to_sha256関数のテスト"""
        # 期待されるハッシュ値を計算
        expected_hash = hashlib.sha256(self.test_image_data).hexdigest()

        # 関数を実行
        result = image_bytes_to_sha256(self.test_image_data)

        # 結果を検証
        self.assertEqual(result, expected_hash)

    def test_encode_image_with_empty_file(self):
        """空のファイルでencode_image関数をテスト"""
        # 空のファイルをモック
        empty_mock_file = Mock(spec=UploadFile)
        empty_mock_file.file = io.BytesIO(b"")

        # 期待される結果を計算
        expected_encoded = base64.b64encode(b"").decode("utf-8")

        # 関数を実行
        result = encode_image(empty_mock_file)

        # 結果を検証
        self.assertEqual(result, expected_encoded)

    def test_image_bytes_to_sha256_with_empty_bytes(self):
        """空のバイト列でimage_bytes_to_sha256関数をテスト"""
        # 空のバイト列に対する期待されるハッシュ値を計算
        expected_hash = hashlib.sha256(b"").hexdigest()

        # 関数を実行
        result = image_bytes_to_sha256(b"")

        # 結果を検証
        self.assertEqual(result, expected_hash)


if __name__ == "__main__":
    unittest.main()
