""" パスワードのハッシュ化ツール """

import os, sys
from typing import Tuple
import bcrypt


def generate_password_hash(plain_password: str, rounds: int = 12) -> Tuple[str, str]:
    """
    平文のパスワードからbcryptハッシュを生成する
    """
    # パスワードをバイト列に変換
    password_bytes = plain_password.encode("utf-8")

    # ソルトを生成してハッシュ化
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password_bytes, salt)

    # バイト列を文字列に変換
    hashed_str = hashed.decode("utf-8")

    return hashed_str


if __name__ == "__main__":
    test_password = sys.argv[1]
    hashed = generate_password_hash(test_password)
    print("\nGenerated bcrypt hash:")
    print(hashed)

    verification = bcrypt.checkpw(test_password.encode("utf-8"), hashed.encode("utf-8"))
    print("\nVerification test:", "PASSED" if verification else "FAILED")
