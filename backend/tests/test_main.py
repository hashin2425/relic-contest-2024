"""Tests for /backend/main.py"""

import unittest

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestMain(unittest.TestCase):
    """/backend/main.py tests"""

    def test_health_check(self):
        """/health-check endpoint test"""
        response = client.get("/health-check")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Server is running.")


if __name__ == "__main__":
    unittest.main()
