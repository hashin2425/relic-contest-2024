""" 画像ファイルをクライアントへ返すエンドポイント """

import re
from pathlib import Path
import traceback
from typing import Optional
from fastapi import APIRouter, HTTPException, Path as FastAPIPath
from fastapi.responses import FileResponse

api_router = APIRouter()

# 画像ファイルの保存ディレクトリ（生成AIが作った画像・あらかじめ作っておいたチャレンジ用の画像）
IMAGE_STORAGE_PATH = Path("app/data/images")


class SecureImageHandler:
    """セキュアな画像ファイルハンドラ"""

    ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
    IMAGE_ID_PATTERN = re.compile(r"^[a-zA-Z0-9][-_a-zA-Z0-9]{64,70}$")

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir.resolve()
        if not self.base_dir.exists():
            raise RuntimeError(f"Base directory {self.base_dir} does not exist")

    def validate_image_id(self, image_id: str) -> bool:
        """
        画像IDのバリデーション
        - 先頭は英数字
        - 2文字目以降は英数字、ハイフン、アンダースコア
        - 長さは64-70文字（ファイル名が識別子とSHA256なので64文字以上に）
        """
        return bool(self.IMAGE_ID_PATTERN.match(image_id))

    def get_secure_image_path(self, image_id: str) -> Optional[Path]:
        """安全な画像パスの取得"""
        if not self.validate_image_id(image_id):
            return None

        # 拡張子を試す
        for ext in self.ALLOWED_EXTENSIONS:
            image_path = (self.base_dir / f"{image_id}{ext}").resolve()

            # パストラバーサル対策
            try:
                if image_path.is_file() and image_path.is_relative_to(self.base_dir):
                    return image_path
            except (RuntimeError, ValueError):
                continue
        return None


@api_router.get("/{image_id}")
async def get_image(
    image_id: str = FastAPIPath(..., title="画像ID", description="取得する画像のID（英数字、ハイフン、アンダースコアのみ許可）"),
):
    """画像ファイルを取得するエンドポイント"""
    try:
        # セキュアなパス解決
        image_security_handler = SecureImageHandler(IMAGE_STORAGE_PATH)
        image_path = image_security_handler.get_secure_image_path(image_id)
        if image_path is None:
            raise HTTPException(status_code=404, detail="Image not found or invalid image ID format.")

        image_id += ".png"  # 現在のシステムではPNG画像のみを使う

        # Content-Typeヘッダーを設定してファイルを返す
        return FileResponse(
            str(image_path),
            headers={"X-Content-Type-Options": "nosniff", "Cache-Control": "no-store, no-cache, must-revalidate"},
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error.") from exc
