from __future__ import annotations

from pydantic import BaseModel


class YoutubeVideoDetails(BaseModel):
    """
    Youtube videos-details API wrapper
    """

    kind: str
    id: str
    publishedAt: str
    title: str
    description: str
    thumbnail_url: str
    channelTitle: str
