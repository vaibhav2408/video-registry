from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class PageInfo(BaseModel):
    totalResults: int
    resultsPerPage: int


class Id(BaseModel):
    kind: str
    videoId: str


class PublishedVideo(BaseModel):
    kind: str
    etag: str
    id: Id


class YoutubePublishedVideos(BaseModel):
    """
    Youtube videos search API wrapper
    """

    kind: str
    etag: str
    nextPageToken: Optional[str]
    regionCode: str
    pageInfo: PageInfo
    items: List[PublishedVideo]
