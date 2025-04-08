""" Challengeモデルに関するユーティリティ関数を定義する
"""

import re


def convert_challenge_to_json_item(challenge) -> dict:
    """ChallengeモデルをJSONに変換する"""
    return {
        "id": str(challenge.id),
        "title": challenge.title,
        "imgUrl": challenge.image_path,
        "description": "",  # 未対応
        "result_sample": challenge.result_sample,
        "result_sample_image_paths": challenge.result_sample_image_paths,
    }


def submission_validation(submission: str) -> bool:
    """提出されたテキストのバリデーション"""
    IS_TOO_LONG = len(submission) > 1000
    IS_CONTAIN_INVALID_CHARS = re.match(r"^[a-zA-Z0-9., 　]+$", submission) is None

    if IS_TOO_LONG or IS_CONTAIN_INVALID_CHARS:
        return False
    return True
