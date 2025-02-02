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
        # デフォルトのタイムゾーン(JST)でのテスト
        result = parse_str_as_jst("2024-01-30 12:00:00", "%Y-%m-%d %H:%M:%S")
        self.assertEqual(result.year, 2024)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 30)
        self.assertEqual(result.hour, 12)
        self.assertEqual(result.minute, 0)
        self.assertEqual(result.second, 0)
        self.assertEqual(str(result.tzinfo), "Asia/Tokyo")

        # 指定したタイムゾーンでのテスト
        result = parse_str_as_jst("2024-01-30 12:00:00", "%Y-%m-%d %H:%M:%S", "UTC")
        self.assertEqual(str(result.tzinfo), "UTC")

        # 無効なタイムゾーンでのテスト
        with self.assertRaises(ZoneInfoNotFoundError):
            parse_str_as_jst("2024-01-30 12:00:00", "%Y-%m-%d %H:%M:%S", "Invalid/Timezone")

        # 無効な日付文字列でのテスト
        with self.assertRaises(ValueError):
            parse_str_as_jst("invalid-date", "%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    unittest.main()
