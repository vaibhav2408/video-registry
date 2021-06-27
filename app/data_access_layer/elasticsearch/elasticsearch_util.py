from datetime import datetime

from elasticsearch_dsl import Index
from structlog import get_logger

from app.core.exception_handler.video_registry_exception import VideoRegistryException
from app.data_access_layer.elasticsearch.elasticsearch_constants import (
    ES_INDEX_REFRESH_INTERVAL_DEFAULT,
    ES_INDEX_REPLICAS_DEFAULT,
    ES_INDEX_SHARDS_DEFAULT,
    ES_REFRESH_INTERVAL,
    YOUTUBE_VIDEOS_ALIAS,
    YOUTUBE_VIDEOS_INDEX_NAME,
)

logger = get_logger()

current_index = ""


def get_index():
    """
    Method to get the index-name
    Returns:
        returns the ES index-name
    """
    index_name = _get_current_index(YOUTUBE_VIDEOS_INDEX_NAME)
    if not is_index_created(index_name):
        create_index(index_name)
    return index_name


def is_index_created(index):
    """
    Method to check if the given index exists or not
    Args:
        index: the index value
    Returns:
        returns True if true else False
    """
    try:
        global current_index
        if not current_index:
            ind = Index(index)
            if ind.exists():
                current_index = index
        return index == current_index
    except VideoRegistryException as ex:
        logger.exception(
            "Exception while creating ES index", index=index, exception=str(ex)
        )
        raise VideoRegistryException(500, f"Exception while creating ES index: {index}")


def create_index(index_name):
    """
    Method to create an index in ES
    Args:
        index_name: the name of the index to be created
    """
    global current_index
    create_index_with_properties(
        index_name, YOUTUBE_VIDEOS_ALIAS, refresh_interval=ES_REFRESH_INTERVAL
    )


def create_index_with_properties(
    name,
    alias,
    num_shards=ES_INDEX_SHARDS_DEFAULT,
    num_replicas=ES_INDEX_REPLICAS_DEFAULT,
    refresh_interval=ES_INDEX_REFRESH_INTERVAL_DEFAULT,
    analyzer_dict=None,
):
    """
    Method to create an index in with pre-defined properties
    Args:
        name: index name
        alias: the alias to be used for the index
        num_shards: number of shards
        num_replicas: number of replicas
        refresh_interval: refresh intervals
        analyzer_dict: ES analyzer
    """
    try:
        index = Index(name)

        """ Check if the index already exists. If it does, do nothing"""
        if index.exists():
            logger.info("Index {} already exists, can't create it".format(name))
            return
        settings_dict = dict(
            number_of_shards=num_shards,
            number_of_replicas=num_replicas,
            refresh_interval=refresh_interval,
        )
        if analyzer_dict:
            settings_dict["analysis"] = analyzer_dict
        """ Index doesn't exist. Set properties and create one """
        index.settings(**settings_dict)
        if alias:
            alias_kwargs = {alias: {}}
            index.aliases(**alias_kwargs)

        """ Create the index """
        index.create()
        logger.info("Created index {} in ElasticSearch".format(name))
    except VideoRegistryException as ex:
        logger.exception(f"Failed to create index {name}", exception=str(ex))
        raise VideoRegistryException(500, f"Failed to create index {name}")


def _get_current_index(index_name_placeholder: str):
    """
    Returns the current index as per the syntax defined
    Args:
        index_name_placeholder: index name string format
    Returns:
        formatted index name
    """
    index_suffix = _get_month_of_year(datetime.now())
    return index_name_placeholder.format(index_suffix)


def _get_month_of_year(date):
    """
    Method to get the <Year>_<month> string corresponding to given date
    i.e., 2021_6
    Args:
        date: date object
    Returns:
        formatted data string
    """
    year = int(date.strftime("%Y"))
    month_of_year = int(date.strftime("%m"))
    return "{}_{}".format(year, month_of_year)
