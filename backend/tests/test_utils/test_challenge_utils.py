""" test for /backend/app/utils/challenge_utils.py """

import unittest
from unittest.mock import Mock
from dataclasses import dataclass
from app.utils.challenge_utils import convert_challenge_to_json_item, submission_validation


@dataclass
class Challenge:
    """テスト用のChallengeモデルモック"""

    id: int
    title: str
    image_path: str
    result_sample: str


class TestChallengeUtils(unittest.TestCase):
    """/backend/app/utils/challenge_utils.py test"""

    def setUp(self):
        """テストデータのセットアップ"""
        self.challenge = Challenge(id=1, title="テストチャレンジ", image_path="/images/test.jpg", result_sample="Hello World")

    def test_convert_challenge_to_json_item(self):
        """convert_challenge_to_json_itemのテスト"""

        result = convert_challenge_to_json_item(self.challenge)

        self.assertEqual(result["id"], "1")
        self.assertEqual(result["title"], "テストチャレンジ")
        self.assertEqual(result["imgUrl"], "/images/test.jpg")
        self.assertEqual(result["description"], "")
        self.assertEqual(result["result_sample"], "Hello World")

    def test_submission_validation_valid_input(self):
        """submission_validationの正常系テスト"""

        # 正常なケース
        valid_inputs = [
            "Hello World",
            "Test123",
            "This is a valid submission",
            "1234567890",
            "abc.,   ABC",
            "　",  # 全角スペース
        ]

        for input_text in valid_inputs:
            with self.subTest(input_text=input_text):
                self.assertTrue(submission_validation(input_text))

    def test_submission_validation_invalid_input(self):
        """submission_validationの異常系テスト"""

        # 1000文字を超える文字列
        long_text = "a" * 1001
        self.assertFalse(submission_validation(long_text))

        # 無効な文字を含む入力
        invalid_inputs = [
            "Hello!World",  # 感嘆符
            "Test@123",  # @記号
            "Invalid#Chars",  # ハッシュ記号
            "こんにちは",  # 日本語
            "Special$Chars",  # ドル記号
            "New\nLine",  # 改行
        ]

        for input_text in invalid_inputs:
            with self.subTest(input_text=input_text):
                self.assertFalse(submission_validation(input_text))


if __name__ == "__main__":
    unittest.main()
