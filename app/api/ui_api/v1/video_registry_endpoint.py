from typing import Union

from fastapi import APIRouter, Query, status
from structlog import get_logger

from app.core.video_management import video_manager
from app.models.generic.empty_response import EmptyResponse
from app.models.video_registry.video_details import VideosDetails

app = APIRouter()

logger = get_logger(__name__)


@app.get(
    "/collections",
    response_model=Union[VideosDetails, EmptyResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all the videos",
    tags=["videos"],
    description="Get the all the stored videos",
    responses={
        status.HTTP_200_OK: {"model": Union[VideosDetails, EmptyResponse]},
        status.HTTP_404_NOT_FOUND: {"model": EmptyResponse},
        status.HTTP_403_FORBIDDEN: {"model": EmptyResponse},
    },
)
def get_video_details(
    limit: int = Query(
        default=50,
        ge=1,
        le=2000,
        title="Pagination Limit",
        description="Maximum number of video_registry entries per request.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        le=10000,
        title="Pagination offset",
        description="Starting index for the video_registry search.",
    ),
):
    result = video_manager.get_youtube_videos(limit, offset)
    if not result:
        logger.info("Did not find any video entries.")
        return EmptyResponse()
    return result


@app.get(
    "/collections/search",
    response_model=Union[VideosDetails, EmptyResponse],
    status_code=status.HTTP_200_OK,
    summary="Search for a video",
    tags=["videos"],
    description="Search for all the videos containing the query string in either title/description",
    responses={
        status.HTTP_200_OK: {"model": Union[VideosDetails, EmptyResponse]},
        status.HTTP_404_NOT_FOUND: {"model": EmptyResponse},
        status.HTTP_403_FORBIDDEN: {"model": EmptyResponse},
    },
)
async def search_videos(
    limit: int = Query(
        default=50,
        ge=1,
        le=2000,
        title="Pagination Limit",
        description="Maximum number of video_registry entries per request.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        le=10000,
        title="Pagination offset",
        description="Starting index for the video_registry search.",
    ),
    query: str = Query(..., title="Video search query", description="String to"),
):
    result = video_manager.search_youtube_videos(limit, offset, query)
    if not result:
        logger.info("No video entries found with the given query.")
        return EmptyResponse()
    return result
