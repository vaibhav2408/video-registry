from elasticsearch_dsl import Q
from structlog import get_logger

from app.core.exception_handler.video_registry_exception import VideoRegistryException
from app.data_access_layer.elasticsearch import elasticsearch_constants
from app.utils import shared_constants
from app.utils.common_utils import string_unquote

logger = get_logger()


def get_all_docs():
    """
    Returns the ES query to fetch all docs in ES
    Returns:
        returns a match-all query instance
    """
    query = Q({"match_all": {}})
    return query


def get_search_query(search_text):
    """
    Returns the ES query based on the given search params
    Args:
        search_text: the search text
    Returns:
        returns the final query instance
    """
    try:
        query_by, query_for = _get_es_simple_query_string(search_text)
        query = Q({query_by: query_for})
        return query
    except VideoRegistryException as ex:
        logger.exception("Failed to search the videos collections.", exception=str(ex))
        raise VideoRegistryException(500, "Failed to search the videos collections.")


def _get_es_simple_query_string(value):
    f"""
    Method to get elasticsearch query using 'simple_query_string' for title & description fields.
    Args:
        value: the query value
    Returns:
        query_by, query_for dict
    """
    default_operator = "OR"
    if not isinstance(value, list):
        value = string_unquote(value).split(" ")
        query = f" {default_operator.upper()} ".join(value)
    else:
        query = f" {default_operator.upper()} ".join(set(value))

    query_by = elasticsearch_constants.ES_SIMPLE_QUERY_STRING_KEY
    query_for = {
        "query": query,
        "fields": [shared_constants.TITLE_KEY, shared_constants.DESCRIPTION_KEY],
        "default_operator": default_operator,
    }
    return query_by, query_for
