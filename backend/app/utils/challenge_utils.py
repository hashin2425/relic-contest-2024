def convert_challenge_to_json_item(challenge) -> dict:
    """ChallengeモデルをJSONに変換する"""
    return {
        "id": str(challenge.id),
        "title": challenge.title,
        "imgUrl": challenge.image_path,
        "description": "",  # 未対応
    }
