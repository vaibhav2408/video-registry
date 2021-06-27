from typing import List, Union

from structlog import get_logger

from app.api.client.apis_helper import Apis
from app.api.client.base_api_caller import BaseApiCaller
from app.core.config import settings

logger = get_logger()


def search_newly_added_videos(
    published_after: str,
    next_page_token: str,
    content_type: str = "video",
    order_by: str = "date",
):
    """
    Fetches the newly added videos
    Args:
        published_after:
        next_page_token:
        content_type:
        order_by:
    Returns:

    """
    result = None
    logger.info(f"Searching for newly published youtube videos.")

    # Checking if api key is already assigned & is a valid API key
    if settings.google_api_key:
        resp = _youtube_search_videos_caller(
            content_type=content_type,
            order_by=order_by,
            published_after=published_after,
            api_key=settings.google_api_key,
            next_page_token=next_page_token,
        )
        if resp:
            return resp

    # If the API key has become invalid, finding a valid key from the list
    for api_key in settings.api_keys:
        resp = _youtube_search_videos_caller(
            content_type=content_type,
            order_by=order_by,
            published_after=published_after,
            api_key=api_key,
            next_page_token=next_page_token,
        )
        if resp:
            settings.google_api_key = api_key
            result = resp
            break
    if not result:
        logger.error(f"Please add a new valid API key at {settings.keys_file_path}")
        logger.error(f"Retrying after {settings.sleep_interval} seconds..")
    return result


def _youtube_search_videos_caller(
    content_type, order_by, published_after, api_key, next_page_token
):
    """
    API builder & caller method for youtube search API
    """
    params = {
        "type": content_type,
        "order": order_by,
        "publishedAfter": published_after,
        "maxResults": 50,
        "key": api_key,
        "q": settings.video_query_string,
    }
    if next_page_token:
        params["pageToken"] = next_page_token
    youtube_search_uri = Apis.search_api
    _base_api_caller = BaseApiCaller(
        base_url=settings.youtube_base_url, path=youtube_search_uri, params=params
    )
    return _base_api_caller.get()


def get_video_details(video_ids: Union[str, List[str]]):
    """
    Method to get details for given video(s)
    """
    result = None

    if isinstance(video_ids, list):
        video_ids = ",".join(video_ids)

    # Checking if api key is already assigned & is a valid API key
    if settings.google_api_key:
        resp = _video_details_caller(video_ids, settings.google_api_key)
        if resp:
            return resp

    # If the API key has become invalid, finding a valid key from the list
    for api_key in settings.api_keys:
        resp = _video_details_caller(video_ids, api_key)
        if resp:
            result = resp
            break
    if not result:
        logger.error(f"Please add a new valid API key at {settings.keys_file_path}")
        logger.error(f"Retrying after {settings.sleep_interval} seconds..")
    return result


def _video_details_caller(video_ids, api_key):
    """
    API builder & caller method for youtube video details API
    """
    params = {
        "key": api_key,
        "id": video_ids,
        "part": "snippet",
    }
    youtube_video_details_uri = Apis.video_details
    _base_api_caller = BaseApiCaller(
        base_url=settings.youtube_base_url,
        path=youtube_video_details_uri,
        params=params,
    )
    return _base_api_caller.get()
