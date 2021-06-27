from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from app.models.generic.paginate import Paginate


class VideoMeta(BaseModel):
    """Wrapper for video meta-data"""

    video_index: str
    kind: str
    id: str
    published_at: str
    title: str
    description: str
    thumbnail_url: str
    channel_title: str
    created_at: int


class VideosDetails(BaseModel):
    """
    Response model for the videos details
    """

    details: List[VideoMeta] = Field(...)
    pagination: Paginate = Field(...)
