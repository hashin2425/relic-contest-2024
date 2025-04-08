"""MongoDBモデル定義"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Challenge(BaseModel):
    """チャレンジモデル"""

    id: str = Field(..., alias="_id")
    title: str
    image_path: str
    image_hash: str
    result_sample: str
    result_sample_image_paths: list[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        """MongoDBモデル設定"""

        allow_population_by_alias = True
        json_encoders = {datetime: lambda v: v.isoformat()}
