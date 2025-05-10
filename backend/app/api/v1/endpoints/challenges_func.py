"""チャレンジに取り組んでいるユーザーに機能を提供するエンドポイント"""

import os
import base64
import json
import hashlib
import uuid
from collections import defaultdict

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
import requests

from app.core.security import require_auth, get_current_user
from app.core.mongodb_core import db
from app.models.pydantic_models import ChallengeRequest, SubmitRequest, UserChallenges
from app.services.groq_services import GroqClient
from app.services.open_ai_services import ChatGPTClient, DallE3Client
from app.services.segmind_services import create_image as create_image_by_segmind
from app.utils.image_utils import encode_image
from app.utils.log_utils import logging
from app.utils.time_utils import get_jst_now
from app.utils.challenge_utils import convert_challenge_to_json_item, submission_validation

load_dotenv()
api_router = APIRouter()
user_challenges = defaultdict(None)
SUBMIT_INTERVAL_FOR_TRIAL = 5  # 提出の間隔（秒）
SUBMIT_INTERVAL_FOR_LOGGED_IN = 60  # 提出の間隔（秒）
SCORE_MAGNIFICATION_TRIAL = 300  # 体験版のスコア倍率


@api_router.get("/get-challenge-progress")
@require_auth()
async def get_challenge_progress(current_user: dict = Depends(get_current_user)):
    """ユーザーのチャレンジ進捗を取得するエンドポイント"""
    user_id = current_user["sub"]
    if user_id not in user_challenges:
        return {
            "in_progress": [
                {
                    "now_challenge_id": "",
                    "submissions": [],
                    "image_paths": [],
                }
            ],
        }

    challenge_progress = user_challenges[user_id]
    return {
        "in_progress": [
            {
                "now_challenge_id": challenge_progress.now_challenge_id,
                "submissions": challenge_progress.submissions,
                "image_paths": challenge_progress.generated_image[-1:] if challenge_progress.generated_image else [],
            }
        ]
    }


@api_router.get("/give-up-challenge")
@require_auth()
async def give_up_challenge(current_user: dict = Depends(get_current_user)):
    """ユーザーのチャレンジ進捗をリセットするエンドポイント"""
    user_id = current_user["sub"]
    logging("Challenge progress reset for user: ", user_id)
    del user_challenges[user_id]

    return {"message": "Challenge progress reset successfully."}


@api_router.get("/complete-challenge")
@require_auth()
async def complete_challenge(current_user: dict = Depends(get_current_user)):
    """ユーザーのチャレンジを完了するエンドポイント"""
    user_id = current_user["sub"]
    if user_id in user_challenges:
        submission_id = str(uuid.uuid4())
        await db.insert_submission(
            _submission_id=submission_id,
            _user_id=user_id,
            _challenge_id=user_challenges[user_id].now_challenge_id,
            _created_at=get_jst_now(),
            _images=user_challenges[user_id].generated_image,
            _submissions=user_challenges[user_id].submissions,
        )

        del user_challenges[user_id]

        logging("Challenge completed for user: ", user_id)
        return {"submission_id": submission_id}
    else:
        raise HTTPException(status_code=404, detail="No challenge progress found for this user.")


@api_router.get("/get-all-submission")
@require_auth()
async def get_all_submission(current_user: dict = Depends(get_current_user)):
    """ユーザーの全提出物を取得するエンドポイント"""
    user_id = current_user["sub"]
    submissions = await db.get_all_submissions_by_user(user_id)

    if not submissions:
        return {"submissions": []}
    return {"submissions": submissions}


@api_router.get("/get-submission/{submission_id}")
@require_auth()
async def get_submission(submission_id: str, current_user: dict = Depends(get_current_user)):
    """ユーザーの提出物を取得するエンドポイント"""
    user_id = current_user["sub"]
    submission = await db.get_submissions_by_submission_id(submission_id)

    if not submission or submission["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="Submission not found.")
    return {
        "submission_id": submission["submission_id"],
        "challenge_id": submission["challenge_id"],
        "created_at": submission["created_at"],
        "images": submission["images"],
        "submissions": submission["submissions"],
    }


@api_router.post("/start-challenge")
@require_auth()
async def start_challenge(request: ChallengeRequest, current_user: dict = Depends(get_current_user)):
    """チャレンジを開始するためのエンドポイント"""
    user_id = current_user["sub"]
    challenge_id = request.challenge_id

    challenge_data = await db.get_challenge_by_id(challenge_id)
    challenge = convert_challenge_to_json_item(challenge_data)

    if challenge is None or challenge is {}:
        # チャレンジが存在しない場合
        raise HTTPException(status_code=404, detail="Challenge not found.")

    if user_id not in user_challenges:
        user_challenges[user_id] = UserChallenges(now_challenge_id=challenge_id, now_challenge=challenge)

    # debug用
    # user_challenges[user_id].submissions = [
    #     {
    #         "timestamp": get_jst_now().strftime("%Y-%m-%dT %H:%M:%S"),
    #         "content": "This is a sample submission text.",
    #         "score": 50,
    #     },
    #     {
    #         "timestamp": get_jst_now().strftime("%Y-%m-%dT %H:%M:%S"),
    #         "content": "This is a sample submission text.",
    #         "score": 95,
    #     },
    # ]
    # user_challenges[user_id].generated_image = [
    #     "/api/img/ch_f011aa5b7e209c2566cfcc49143b1ab713016351f0727938cbf93f7e155f5126",
    #     "/api/img/ch_f011aa5b7e209c2566cfcc49143b1ab713016351f0727938cbf93f7e155f5126",
    # ]
    # user_challenges[user_id].last_submitted_text = "This is a sample submission text."
    # user_challenges[user_id].last_submission_score = 95
    # debug用

    logging("Challenge started: ", challenge_id, current_user)
    response = {}

    response["message"] = "Start the challenge!"
    if user_challenges[user_id].submissions:
        response["submissions"] = user_challenges[user_id].submissions
    if user_challenges[user_id].generated_image:
        response["generated_img_url"] = user_challenges[user_id].generated_image[0]
        if not response["generated_img_url"].startswith("/api/img/"):
            response["generated_img_url"] = "/api/img/" + user_challenges[user_id].generated_image[0]
    if user_challenges[user_id].last_submitted_text:
        response["last_submitted_text"] = user_challenges[user_id].last_submitted_text
    if user_challenges[user_id].last_submission_score:
        response["last_submission_score"] = user_challenges[user_id].last_submission_score
    return response


@api_router.post("/submit")
@require_auth()
async def submit_challenge(request: SubmitRequest, current_user: dict = Depends(get_current_user)):
    submission = request.submission
    challenge = user_challenges[current_user["sub"]].now_challenge
    return_payload = {}
    logging("Challenge submitted: ", request.submission, current_user["sub"], challenge)

    # 提出の間隔をチェック
    if user_challenges[current_user["sub"]].last_submitted_unix_time + SUBMIT_INTERVAL_FOR_LOGGED_IN > get_jst_now().timestamp():
        raise HTTPException(status_code=400, detail="Submission interval is too short.")
    user_challenges[current_user["sub"]].last_submitted_unix_time = get_jst_now().timestamp()

    # 提出テキストのバリデーション
    if not submission_validation(submission):
        raise HTTPException(status_code=400, detail="Submission text is invalid.")

    user_id = current_user["sub"]

    # groqによるチェック
    score = user_challenges[user_id].last_submission_score
    query_submission_to_score = f"""
    As an AI evaluator, analyze the English text within the <Submission> tags and assess how comprehensively it covers the content provided in the <Result> tags. Output only a single integer score from 0 to 100, where:

    - 100 indicates the submission fully covers all key points and details from the result
    - 75 indicates most key points are covered with some minor omissions
    - 50 indicates roughly half of the important content is covered
    - 25 indicates only basic or surface-level coverage
    - 0 indicates no relevant content coverage

    Do not provide any explanation or additional text - output only the integer score.

    <Result>
    {challenge.get("result_sample", "")}
    </Result>

    <Submission>
    {submission}
    </Submission>
    """
    IS_USE_GROQ = False  # いったんFalseにしておく
    if IS_USE_GROQ:
        groq_client = GroqClient(api_key=os.getenv("GROQ_API_KEY", ""))
        response = groq_client.chat(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": query_submission_to_score},
                    ],
                }
            ]
        )
    else:
        open_ai_client = ChatGPTClient()
        response = open_ai_client.chat(query_submission_to_score)
    try:
        score = int(response)
    except ValueError:
        pass

    user_challenges[user_id].submissions.append(
        {
            "timestamp": get_jst_now().strftime("%Y-%m-%dT %H:%M:%S"),
            "content": submission,
            "score": score,
        }
    )

    last_submission_score = user_challenges[user_id].last_submission_score
    new_submission_score = score
    if (last_submission_score < 50 <= new_submission_score) or (last_submission_score < 75 <= new_submission_score) or (last_submission_score < 90 <= new_submission_score):
        filename = "gen_" + hashlib.sha256(f"{user_id}_{get_jst_now().strftime('%Y%m%d%H%M%S')}".encode()).hexdigest()
        prompt = f"Create an image that represents the following text: {submission}"
        USE_DALLE3 = True
        if USE_DALLE3:
            open_ai_client = DallE3Client()
            open_ai_client.generate(prompt, filename)
            user_challenges[user_id].generated_image.append(filename)
            return_payload["generated_img_url"] = "/api/img/" + filename
        else:
            _ = create_image_by_segmind(prompt, filename)
            return_payload["generated_img_url"] = "/api/img/" + filename

    user_challenges[user_id].last_submitted_text = submission
    user_challenges[user_id].last_submission_score = score

    return_payload["message"] = "Submission successful!"
    return_payload["submissions"] = user_challenges[user_id].submissions
    return_payload["last_submitted_text"] = user_challenges[user_id].last_submitted_text
    return_payload["last_submission_score"] = user_challenges[user_id].last_submission_score
    return return_payload


@api_router.post("/submit-for-trial")
async def submit_challenge_for_trial(request: SubmitRequest):
    submission = request.submission
    challenge_id = request.challenge_id
    challenge_data = await db.get_challenge_by_id(challenge_id)
    challenge = convert_challenge_to_json_item(challenge_data)
    return_payload = {}

    # 提出テキストのバリデーション
    if not submission_validation(submission):
        raise HTTPException(status_code=400, detail="Submission text is invalid.")

    # 体験版のため、簡易的なスコア算出を行う
    score = 0
    word_list_submission = set([word.lower() for word in submission.split()])
    word_list_result = set([word.lower() for word in challenge.get("result_sample", "").split()])
    common_words = word_list_submission.intersection(word_list_result)
    score = int(len(common_words) / len(word_list_result) * SCORE_MAGNIFICATION_TRIAL) if word_list_result else 0
    score = min(max(score, 0), 100)

    if 50 <= score < 75:
        return_payload["generated_img_url"] = challenge["result_sample_image_paths"][0]
    elif 75 <= score < 90:
        return_payload["generated_img_url"] = challenge["result_sample_image_paths"][1]
    elif score >= 90:
        return_payload["generated_img_url"] = challenge["result_sample_image_paths"][2]

    return_payload["message"] = "Submission successful!"
    return_payload["submissions"] = [
        {
            "timestamp": get_jst_now().strftime("%Y-%m-%dT %H:%M:%S"),
            "content": submission,
            "score": score,
        }
    ]
    return_payload["last_submitted_text"] = score
    return_payload["last_submission_score"] = score
    return return_payload


#
# @api_router.post("/chat")
# @require_auth()
# async def return_message_from_chat(request: MessagesRequest):
#    """チャットリクエストをGroqクライアントに送信し、応答を返す"""
#    groq_client = GroqClient(api_key=os.getenv("GROQ_API_KEY", ""))
#    messages_dict = [message.dict() for message in request.messages]
#    response = groq_client.chat(messages=messages_dict)
#    return {"response": response}
#
#
# @api_router.post("/analyze-image")
# @require_auth()
# async def analyze_image(file: UploadFile):
#    """画像がJPEGまたはPNG形式であることを確認"""
#    groq_client = GroqClient(api_key=os.getenv("GROQ_API_KEY", ""))
#    if file.content_type not in ["image/jpeg", "image/png"]:
#        raise HTTPException(status_code=400, detail="Only JPEG or PNG images are supported.")
#
#    # 画像をBase64形式にエンコード
#    base64_image = encode_image(file)
#    messages = [
#        {
#            "role": "user",
#            "content": [
#                {"type": "text", "text": "この画像は何を表していますか？"},
#                {
#                    "type": "image_url",
#                    "image_url": {
#                        "url": f"data:image/jpeg;base64,{base64_image}",
#                    },
#                },
#            ],
#        },
#    ]
#    # Groqに画像を渡して、説明を取得
#    description = groq_client.chat(messages)
#    return {"description": description}
#
#
# @api_router.post("/analyze-base64image")
# @require_auth()
# async def analyze_base64image(base64_image: str):
#    """Base64エンコードされた画像をGroqに渡して説明を取得"""
#    groq_client = GroqClient(api_key=os.getenv("GROQ_API_KEY", ""))
#    messages = [
#        {
#            "role": "user",
#            "content": [
#                {"type": "text", "text": "この画像は何を表していますか？"},
#                {
#                    "type": "image_url",
#                    "image_url": {
#                        "url": f"data:image/jpeg;base64,{base64_image}",
#                    },
#                },
#            ],
#        },
#    ]
#    description = groq_client.chat(messages)
#    return {"description": description}
#
#
# @api_router.post("/create-image")
# @require_auth()
# async def create_image(prompt: str):
#    """画像生成のためのAPIキーとURL"""
#    api_key = os.getenv("SEGMIND_KEY")
#    url = "https://api.segmind.com/v1/sdxl1.0-newreality-lightning"
#    payload = {
#        "prompt": prompt,  # 画像生成のプロンプト
#        "negative_prompt": "((close up)),(octane render, render, drawing, bad photo, bad photography:1.3)",  # ネガティブプロンプト
#        "samples": 1,  # 生成する画像の数
#        "scheduler": "DPM++ SDE",  # スケジューラー設定
#        "num_inference_steps": 7,  # 推論ステップ数
#        "guidance_scale": 1,  # ガイダンススケール
#        "seed": 1220429729,  # ランダムシード
#        "img_width": 1024,  # 画像の幅
#        "img_height": 1024,  # 画像の高さ
#        "base64": False,  # Base64で返すかどうか
#    }
#
#    headers = {"x-api-key": api_key}
#    response = requests.post(url, json=payload, headers=headers, timeout=30)
#    if response.ok:
#        # 生成された画像をBase64エンコードして返す
#        base64_image = base64.b64encode(response.content).decode("utf-8")
#        return {"base64image": base64_image}
#
#    # エラーが発生した場合
#    return {"error": "Image generation failed", "status_code": response.status_code}
#
