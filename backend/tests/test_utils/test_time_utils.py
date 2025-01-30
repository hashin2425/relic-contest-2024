""" Test for /backend/app/utils/time_utils.py """

import unittest
from unittest.mock import patch
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.utils.time_utils import get_utc_now, get_jst_now, parse_str_as_jst


class TestDatetimeFunctions(unittest.TestCase):
    """/backend/app/utils/time_utils.py tests"""

    def setUp(self):
        # テストで使用する固定の日時を設定
        self.fixed_dt = datetime(2024, 1, 30, 12, 0, 0)

    @patch("app.utils.time_utils.datetime")
    def test_get_utc_now(self, mock_datetime):
        # モックの設定
        mock_datetime.now.return_value = self.fixed_dt.replace(tzinfo=ZoneInfo("UTC"))

        # テスト実行
        result = get_utc_now()

        # アサーション
        self.assertEqual(result.year, 2024)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 30)
        self.assertEqual(result.hour, 12)
        self.assertEqual(result.minute, 0)
        self.assertEqual(result.second, 0)
        self.assertEqual(str(result.tzinfo), "UTC")

    @patch("app.utils.time_utils.datetime")
    def test_get_jst_now(self, mock_datetime):
        # モックの設定
        mock_datetime.now.return_value = self.fixed_dt.replace(tzinfo=ZoneInfo("Asia/Tokyo"))

        # テスト実行
        result = get_jst_now()

        # アサーション
        self.assertEqual(result.year, 2024)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 30)
        self.assertEqual(result.hour, 12)
        self.assertEqual(result.minute, 0)
        self.assertEqual(result.second, 0)
        self.assertEqual(str(result.tzinfo), "Asia/Tokyo")

    def test_parse_str_as_jst(self):
        # テストケース
        test_cases = [
            {"input": "2024-01-30 12:00:00", "format": "%Y-%m-%d %H:%M:%S", "expected": datetime(2024, 1, 30, 12, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))},
            {"input": "2024/01/30 12:00:00", "format": "%Y/%m/%d %H:%M:%S", "expected": datetime(2024, 1, 30, 12, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))},
        ]

        for case in test_cases:
            with self.subTest(input=case["input"]):
                result = parse_str_as_jst(case["input"], case["format"])
                self.assertEqual(result, case["expected"])

    def test_parse_str_as_jst_with_different_timezone(self):
        # 異なるタイムゾーンでのテスト
        dt_str = "2024-01-30 12:00:00"
        dt_format = "%Y-%m-%d %H:%M:%S"
        timezone = "America/New_York"

        result = parse_str_as_jst(dt_str, dt_format, timezone)

        # JST(UTC+9)からEST(UTC-5)への変換で14時間の差があるため前日の22:00となる
        expected = datetime(2024, 1, 29, 22, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        self.assertEqual(result, expected)

    def test_parse_str_as_jst_invalid_format(self):
        # 無効な日付文字列でのテスト
        with self.assertRaises(ValueError):
            parse_str_as_jst("invalid-date", "%Y-%m-%d %H:%M:%S")

    def test_parse_str_as_jst_invalid_timezone(self):
        # 無効なタイムゾーンでのテスト
        with self.assertRaises(ZoneInfoNotFoundError):
            parse_str_as_jst("2024-01-30 12:00:00", "%Y-%m-%d %H:%M:%S", "Invalid/Timezone")


if __name__ == "__main__":
    unittest.main()
