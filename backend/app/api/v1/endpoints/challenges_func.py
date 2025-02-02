""" Challenge endpoint module """

import os
import base64
import json
import hashlib
from collections import defaultdict
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi_limiter.depends import RateLimiter
import requests
import asyncio

from app.core.security import require_auth, get_current_user
from app.core.mongodb_core import db
from app.models.pydantic_models import (
    ChallengeRequest,
    SubmitRequest,
    UserChallenges,
    UserSubmission
)
from app.services.groq_services import GroqClient
from app.services.open_ai_services import ChatGPTClient, DallE3Client
from app.services.segmind_services import create_image as create_image_by_segmind
from app.utils.image_utils import encode_image
from app.utils.log_utils import logging
from app.utils.time_utils import get_jst_now
from app.utils.challenge_utils import convert_challenge_to_json_item, submission_validation

api_router = APIRouter()
SUBMIT_INTERVAL = 120  # seconds between submissions
RATE_LIMIT_TIMES = 30  # requests per minute
RATE_LIMIT_SECONDS = 60


@api_router.post("/start-challenge")
@require_auth()
async def start_challenge(
    request: ChallengeRequest,
    current_user: dict = Depends(get_current_user),
    rate_limiter: None = Depends(RateLimiter(times=RATE_LIMIT_TIMES, seconds=RATE_LIMIT_SECONDS))
):
    """Start a challenge for a user"""
    user_id = current_user["sub"]
    challenge_id = request.challenge_id

    # Get challenge data
    challenge_data = await db.get_challenge_by_id(challenge_id)
    challenge = convert_challenge_to_json_item(challenge_data)

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found.")

    # Get or create user challenge data
    user_challenge = await db.get_user_challenge(user_id, challenge_id)
    if not user_challenge:
        user_challenge = await db.create_user_challenge(
            user_id=user_id,
            challenge_id=challenge_id,
            challenge=challenge
        )

    logging("Challenge started: ", challenge_id, current_user)
    return {
        "message": "Challenge started successfully!",
        "submissions": user_challenge.get("submissions", []),
        "last_submitted_text": user_challenge.get("last_submitted_text", ""),
        "last_submission_score": user_challenge.get("last_submission_score", 0),
    }


@api_router.post("/submit")
@require_auth()
async def submit_challenge(
    request: SubmitRequest,
    current_user: dict = Depends(get_current_user),
    rate_limiter: None = Depends(RateLimiter(times=RATE_LIMIT_TIMES, seconds=RATE_LIMIT_SECONDS))
):
    """Submit a challenge solution"""
    user_id = current_user["sub"]
    submission = request.submission
    
    # Get user's current challenge
    user_challenge = await db.get_active_user_challenge(user_id)
    if not user_challenge:
        raise HTTPException(status_code=400, detail="No active challenge found.")
        
    challenge = user_challenge.get("challenge", {})
    return_payload = {}
    logging("Challenge submitted: ", submission, user_id, challenge)

    # Check submission interval
    last_submit_time = user_challenge.get("last_submitted_unix_time", 0)
    if last_submit_time + SUBMIT_INTERVAL > get_jst_now().timestamp():
        raise HTTPException(status_code=400, detail="Submission interval is too short.")

    # Validate submission text
    if not submission_validation(submission):
        raise HTTPException(status_code=400, detail="Submission text is invalid.")

    # Evaluate submission
    score = await evaluate_submission(submission, challenge.get("result_sample", ""))

    # Create submission record
    submission_record = UserSubmission(
        timestamp=get_jst_now().strftime("%Y-%m-%dT %H:%M:%S"),
        content=submission,
        score=score
    )

    # Generate image if score threshold reached
    last_score = user_challenge.get("last_submission_score", 0)
    if (last_score < 50 <= score) or (last_score < 75 <= score) or (last_score < 90 <= score):
        try:
            result = await generate_submission_image(user_id, submission)
            if result.get("url"):
                return_payload["generated_img_url"] = result["url"]
        except Exception as e:
            logging(f"Error generating image: {e}")

    # Update user challenge data
    try:
        await db.update_user_challenge(
            user_id=user_id,
            challenge_id=user_challenge["challenge_id"],
            submission=submission_record.dict(),  # Convert to dict for MongoDB
            last_score=score,
            last_submission=submission
        )
    except Exception as e:
        logging(f"Error updating challenge: {e}")
        # Continue even if update fails
        pass

    # Get updated challenge data
    try:
        updated_challenge = await db.get_active_user_challenge(user_id)
        if updated_challenge:
            return {
                "message": "Submission successful!",
                "submissions": updated_challenge.get("submissions", []),
                "last_submitted_text": updated_challenge.get("last_submitted_text", ""),
                "last_submission_score": updated_challenge.get("last_submission_score", 0),
                **return_payload
            }
    except Exception as e:
        logging(f"Error getting updated challenge: {e}")

    # Fallback response if getting updated data fails
    return {
        "message": "Submission successful!",
        "submissions": [],
        "last_submitted_text": submission,
        "last_submission_score": score,
        **return_payload
    }


async def evaluate_submission(submission: str, result_sample: str) -> int:
    """Evaluate submission using AI"""
    query = f"""
    As an AI evaluator, analyze the English text within the <Submission> tags and assess how comprehensively it covers the content provided in the <Result> tags. Output only a single integer score from 0 to 100, where:

    - 100 indicates the submission fully covers all key points and details from the result
    - 75 indicates most key points are covered with some minor omissions
    - 50 indicates roughly half of the important content is covered
    - 25 indicates only basic or surface-level coverage
    - 0 indicates no relevant content coverage

    Do not provide any explanation or additional text - output only the integer score.

    <Result>
    {result_sample}
    </Result>

    <Submission>
    {submission}
    </Submission>
    """
    
    try:
        IS_USE_GROQ = False
        chat_response = ""
        
        if IS_USE_GROQ:
            try:
                groq_client = GroqClient(api_key=os.getenv("GROQ_API_KEY", ""))
                chat_response = await groq_client.chat(
                    messages=[{"role": "user", "content": query}]
                )
            except ImportError:
                logging("Groq not available, falling back to ChatGPT")
                IS_USE_GROQ = False
        
        if not IS_USE_GROQ:
            open_ai_client = ChatGPTClient()
            chat_response = await open_ai_client.chat(query)

        try:
            # Remove any non-numeric characters
            score_str = ''.join(c for c in chat_response if c.isdigit())
            score = int(score_str) if score_str else 0
            return max(0, min(100, score))  # Ensure score is between 0 and 100
        except (ValueError, TypeError):
            logging(f"Error converting response to int: {chat_response}")
            return 0
    except Exception as e:
        logging(f"Error evaluating submission: {e}")
        return 0


def generate_filename(user_id: str) -> str:
    """Generate unique filename for submission image"""
    timestamp = get_jst_now().strftime('%Y%m%d%H%M%S')
    return f"gen_{hashlib.sha256(f'{user_id}_{timestamp}'.encode()).hexdigest()}"


async def _attempt_image_generation(prompt: str, filename: str, use_dalle: bool = True) -> bool:
    """Attempt to generate image using specified service"""
    try:
        if use_dalle:
            client = DallE3Client()
            return await client.generate(prompt, filename)
        return await create_image_by_segmind(prompt, filename)
    except Exception as e:
        logging(f"Error in image generation attempt: {e}")
        return False


async def generate_submission_image(user_id: str, submission: str) -> Dict[str, str]:
    """Generate image for submission"""
    try:
        filename = generate_filename(user_id)
        prompt = f"Create an image that represents the following text: {submission}"
        
        # Try DALL-E 3 first, fallback to Segmind if needed
        USE_DALLE3 = True
        success = await _attempt_image_generation(prompt, filename, use_dalle=USE_DALLE3)
        
        if success:
            return {"url": f"/api/img/{filename}"}
        return {"url": ""}
            
    except Exception as e:
        logging(f"Error in generate_submission_image: {e}")
        return {"url": ""}
