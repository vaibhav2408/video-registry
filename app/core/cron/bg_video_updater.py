import asyncio

from structlog import get_logger

from app.api.client import fetch_youtube_videos
from app.core.config import settings
from app.core.exception_handler.video_registry_exception import VideoRegistryException
from app.data_access_layer.elasticsearch.elasticsearch_dal import ElasticsearchDAL
from app.models.youtube.youtube_search_results import YoutubePublishedVideos
from app.utils.common_utils import get_published_after

logger = get_logger()


def insert_new_videos(
    published_after: str, content_type: str = "video", order_by: str = "date"
):
    """
    Method to get the youtube published videos based on the filters provided
    """
    try:
        next_page_token = None
        while True:
            video_ids = []

            youtube_published_videos = fetch_youtube_videos.search_newly_added_videos(
                published_after=published_after,
                content_type=content_type,
                order_by=order_by,
                next_page_token=next_page_token,
            )
            if not youtube_published_videos:
                break
            youtube_published_videos_instance = YoutubePublishedVideos(
                **youtube_published_videos
            )

            # Adding all the videos' id to a list to get their details as part of Single API call
            for published_video in youtube_published_videos_instance.items:
                if published_video.id.videoId:
                    video_ids.append(published_video.id.videoId)

            if settings.google_api_key and not video_ids:
                # If API key was valid but no new videos were published.
                logger.info(f"No new videos published since {published_after}")
                return None

            if not video_ids:
                return None

            # Getting details of 50 videos at a time
            video_details = fetch_youtube_videos.get_video_details(video_ids)

            if not video_details:
                return None

            # Writing each video-details as an individual document in the DB
            elasticsearch_dal = ElasticsearchDAL()
            for data_to_insert in video_details.get("items"):
                elasticsearch_dal.add_records(
                    _get_only_relevant_data(data_to_insert), {}
                )

            if not youtube_published_videos_instance.nextPageToken:
                break
            else:
                next_page_token = youtube_published_videos_instance.nextPageToken
    except VideoRegistryException as e:
        logger.error(
            "Error occurred while fetching newly published videos", error=str(e)
        )


def _get_only_relevant_data(video_data):
    """
    Method to build ES document with only the relevant information
    """
    return {
        "kind": video_data["kind"],
        "id": video_data["id"],
        "published_at": video_data["snippet"]["publishedAt"],
        "title": video_data["snippet"]["title"],
        "description": video_data["snippet"]["description"],
        "thumbnail_url": video_data["snippet"]["thumbnails"]["default"]["url"],
        "channel_title": video_data["snippet"]["channelTitle"],
    }


async def insert_newly_published_videos():
    """
    A background task which keeps checking
    for newly published youtube videos after a
    given interval of time
    """
    while True:
        published_after = get_published_after()
        logger.debug("Checking for new video uploads.", published_after=published_after)
        insert_new_videos(published_after)
        await asyncio.sleep(settings.sleep_interval)
