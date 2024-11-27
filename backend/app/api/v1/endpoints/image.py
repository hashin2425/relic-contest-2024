""" 画像ファイルをクライアントへ返すエンドポイント """

import re
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Path as FastAPIPath
from fastapi.responses import FileResponse

api_router = APIRouter()


@api_router.get("/{image_id}")
async def get_image(image_id: str = FastAPIPath(..., title="画像ID", description="取得する画像のID（英数字、ハイフン、アンダースコアのみ許可）")):
    """画像ファイルを取得するエンドポイント"""
    try:
        # ベースディレクトリを定義
        base_dir = Path("app/api/v1/endpoints/image")  # TODO: あとでディレクトリを変更する

        # ファイル名を検証
        if not re.match(r"^[a-zA-Z0-9\-_]+$", image_id):
            raise HTTPException(status_code=400, detail="Invalid image ID format.")

        # パスを構築して検証
        image_path = (base_dir / f"{image_id}.png").resolve()
        # if not image_path.is_relative_to(base_dir):
        #     raise HTTPException(status_code=400, detail="Invalid image path.")

        # ファイルの存在確認
        if not image_path.is_file():
            raise HTTPException(status_code=404, detail="Image not found.")

        return FileResponse(str(image_path))

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error.") from exc
