""" 画像ファイルをクライアントへ返すエンドポイントを提供するモジュール """

from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import FileResponse


api_router = APIRouter()


@api_router.get("/{image_id}")
async def get_image(image_id: int = Path(..., title="画像ID")):
    """画像ファイルを取得するエンドポイント"""
    try:
        return FileResponse(f"app/api/v1/endpoints/image/{image_id}.png")
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Image not found.") from exc
