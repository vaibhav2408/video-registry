from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from structlog import get_logger

from app.core.exception_handler.video_registry_exception import VideoRegistryException
from app.data_access_layer.elasticsearch.elasticsearch_dal import ElasticsearchDAL
from app.models.generic.paginate import Paginate
from app.utils import common_utils, shared_constants

logger = get_logger()


def get_youtube_videos(limit: int, offset: int):
    """
    Method to get the videos data stored in the DB
    :param limit: The maximum entries per page
    :param offset: The starting point for a page

    :returns: Stored video' data
    """
    try:
        logger.info(f"Getting the videos-data.")

        search_params = {"limit": limit, "offset": offset}

        elasticsearch_dal = ElasticsearchDAL()
        result, count = elasticsearch_dal.get_all_records(search_params, {})
        logger.debug("Done fetching the docs from the DB", count=count)

        if not result:
            return None

        return _build_response(
            result=result,
            count=count,
            offset=offset,
        )
    except VideoRegistryException:
        logger.exception("Error while fetching the video collection")
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                {
                    "message": "Internal server error",
                    "detail": "Error while fetching the video collection",
                }
            ),
        )


def search_youtube_videos(limit: int, offset: int, search_text: str):
    """
    Method to search the videos using the given search query
    Args:
        limit:
        offset:
        search_text:
    Returns:
    : The filtered data
    """
    logger.info(
        f"Searching videos in the db having title/description as : {search_text}"
    )
    try:
        search_params = {
            "limit": limit,
            "offset": offset,
            shared_constants.VIDEOS_SEARCH_QUERY_KEY: search_text,
        }

        elasticsearch_dal = ElasticsearchDAL()
        result, count = elasticsearch_dal.search_all_records(search_params, {})
        logger.debug("Done fetching the docs from the DB", count=count)

        if not result:
            return None

        return _build_response(
            result=result,
            count=count,
            offset=offset,
        )
    except VideoRegistryException:
        logger.exception("Error while querying the video collection")
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                {
                    "message": "Internal server error",
                    "detail": "Error while querying the video collection",
                }
            ),
        )


def _build_response(result, count, offset):
    """
    Method to build the response from the query output
    Args:
        result: the result of the ES query
        count: the total number of hist
        offset: starting point for the records
    Returns:
        dict containing the fetched video-info
    """
    videos = []  # type:ignore

    if result:
        for video_details in result:
            entry = {
                shared_constants.INDEX_KEY: video_details.meta.index,
                shared_constants.VIDEO_ID_KEY: video_details.meta.id,
            }
            video_info = video_details.to_dict()

            for field, value in video_info.items():
                entry[field] = value
            videos.append(entry)

    pagination = Paginate(offset=offset, count_per_page=len(videos), total_count=count)
    return common_utils.multiple_args_to_single_dict(
        details=videos,
        pagination=pagination.dict(),
    )
