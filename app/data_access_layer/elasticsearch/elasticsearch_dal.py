from elasticsearch import exceptions
from elasticsearch_dsl import Search
from structlog import get_logger

from app.core.exception_handler.video_registry_exception import VideoRegistryException
from app.data_access_layer import es_conn
from app.data_access_layer.elasticsearch import (
    elasticsearch_constants,
    elasticsearch_query_builder,
    elasticsearch_util,
)
from app.data_access_layer.generic.video_registry_db_interface import (
    VideoRegistryDBInterface,
)
from app.utils import common_utils, shared_constants

logger = get_logger()

# Error messages
INDEX_NOT_FOUND_MESSAGE = "Index not found in the elasticsearch database"
QUERYING_FAILURE_MESSAGE = "Exception while fetching video records from Elasticsearch"


class ElasticsearchDAL(VideoRegistryDBInterface):
    """
    Data access layer for the Elasticsearch ops.

    This Class contains basic Write/Read documents operations.
    It has functions to add a new document and fetch document(s)
    based on the search parameters
    """

    INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error."

    def add_records(self, data: dict, execution_context: dict):
        """
        Method to index an youtube-videos entry to the elasticsearch
        Args:
            data: the data to be indexed into the ES
            execution_context: additional information required for indexing the data
        Returns:
            returns boolean based on the indexing result. True- success, False- Failure
        """
        try:
            index_name = elasticsearch_util.get_index()
            created_at = common_utils.get_epoch_millis()
            data[shared_constants.CREATED_AT_KEY] = created_at
            doc_id = data["id"]

            res = es_conn.index(index=index_name, id=doc_id, body=data)

            if res["result"] == "created":
                logger.info(
                    "Done writing data to elasticsearch",
                    index=index_name,
                    video_doc_id=res["_id"],
                    result=res,
                )
        except exceptions.NotFoundError as nfe:
            logger.exception(
                INDEX_NOT_FOUND_MESSAGE,
                index_alias=elasticsearch_constants.YOUTUBE_VIDEOS_ALIAS,
                exception=str(nfe),
            )
            raise VideoRegistryException(500, detail=self.INTERNAL_SERVER_ERROR_MESSAGE)
        except exceptions.SerializationError as se:
            logger.exception(
                f"Failed to index the document.", data=data, exception=str(se)
            )
            raise VideoRegistryException(500, detail=self.INTERNAL_SERVER_ERROR_MESSAGE)
        except exceptions.TransportError as te:
            logger.exception(
                f"Failed to index the document.", data=data, exception=str(te)
            )
            raise VideoRegistryException(500, detail=self.INTERNAL_SERVER_ERROR_MESSAGE)
        except VideoRegistryException as ae:
            logger.exception(
                f"Failed to index the document.", data=data, exception=str(ae)
            )
            raise VideoRegistryException(500, detail=self.INTERNAL_SERVER_ERROR_MESSAGE)

    def get_all_records(self, data: dict, execution_context: dict):
        """
        Method to get youtube-videos entries from the elasticsearch index
        Args:
            data: the data to be indexed into the ES
            execution_context: additional information required for reading the data
        Returns:
            returns the response & the count of videos in the response
        """
        try:
            logger.debug(
                "Reading all the youtube-videos.",
                search_params=data,
            )

            limit = (
                int(data[shared_constants.LIMIT_KEY])
                if shared_constants.LIMIT_KEY in data
                else shared_constants.DEFAULT_PER_PAGE_LIMIT
            )
            offset = (
                int(data[shared_constants.OFFSET_KEY])
                if shared_constants.OFFSET_KEY in data
                else shared_constants.DEFAULT_OFFSET
            )

            search_query = elasticsearch_query_builder.get_all_docs()
            logger.debug("Done building the ES search query", search_query=search_query)
            sort = data.pop("sort", None)

            index = elasticsearch_constants.YOUTUBE_VIDEOS_ALIAS
            s = Search(index=index).query(search_query)
            sort = sort.lstrip("+") if sort else f"-{shared_constants.PUBLISHED_AT}"
            s = s.sort(sort)
            s = s[offset : (offset + limit)]
            resp = s.execute()
            count = resp.hits.total

            return resp, count["value"]

        except exceptions.NotFoundError as nfe:
            logger.exception(
                INDEX_NOT_FOUND_MESSAGE,
                index_alias=elasticsearch_constants.YOUTUBE_VIDEOS_ALIAS,
                exception=str(nfe),
            )
            return None, None
        except exceptions.SerializationError as se:
            logger.exception(QUERYING_FAILURE_MESSAGE, data=data, exception=str(se))
            raise VideoRegistryException(500, detail=self.INTERNAL_SERVER_ERROR_MESSAGE)
        except exceptions.TransportError as te:
            logger.exception(QUERYING_FAILURE_MESSAGE, data=data, exception=str(te))
            raise VideoRegistryException(500, detail=self.INTERNAL_SERVER_ERROR_MESSAGE)
        except VideoRegistryException as ae:
            logger.exception(
                QUERYING_FAILURE_MESSAGE,
                exception=str(ae),
            )
            raise VideoRegistryException(500, self.INTERNAL_SERVER_ERROR_MESSAGE)
        except Exception as e:
            logger.exception(
                QUERYING_FAILURE_MESSAGE,
                exception=str(e),
            )
            raise VideoRegistryException(500, self.INTERNAL_SERVER_ERROR_MESSAGE)

    def search_all_records(self, data: dict, execution_context: dict):
        """
        Method to get youtube-videos entries from the elasticsearch index
        Args:
            data: the data to be indexed into the ES
            execution_context: additional information required for reading the data
        Returns:
            returns the response & the count of videos in the response
        """
        try:
            search_query_string = data.get(shared_constants.VIDEOS_SEARCH_QUERY_KEY)
            limit = (
                int(data[shared_constants.LIMIT_KEY])
                if shared_constants.LIMIT_KEY in data
                else shared_constants.DEFAULT_PER_PAGE_LIMIT
            )
            offset = (
                int(data[shared_constants.OFFSET_KEY])
                if shared_constants.OFFSET_KEY in data
                else shared_constants.DEFAULT_OFFSET
            )

            logger.debug(
                "Querying data with user specific string.",
                search_query_string=search_query_string,
                limit=limit,
                offset=offset,
            )

            search_query = elasticsearch_query_builder.get_search_query(
                search_query_string
            )
            logger.debug("Done building the ES search query", search_query=search_query)
            sort = data.pop("sort", None)

            index = elasticsearch_constants.YOUTUBE_VIDEOS_ALIAS
            s = Search(index=index).query(search_query)
            sort = sort.lstrip("+") if sort else f"-{shared_constants.PUBLISHED_AT}"
            s = s.sort(sort)
            s = s[offset : (offset + limit)]
            resp = s.execute()
            count = resp.hits.total

            return resp, count["value"]

        except exceptions.NotFoundError as nfe:
            logger.exception(
                INDEX_NOT_FOUND_MESSAGE,
                index_alias=elasticsearch_constants.YOUTUBE_VIDEOS_ALIAS,
                exception=str(nfe),
            )
            return None, None
        except exceptions.SerializationError as se:
            logger.exception(QUERYING_FAILURE_MESSAGE, data=data, exception=str(se))
            raise VideoRegistryException(500, detail=self.INTERNAL_SERVER_ERROR_MESSAGE)
        except exceptions.TransportError as te:
            logger.exception(QUERYING_FAILURE_MESSAGE, data=data, exception=str(te))
            raise VideoRegistryException(500, detail=self.INTERNAL_SERVER_ERROR_MESSAGE)
        except VideoRegistryException as ae:
            logger.exception(
                QUERYING_FAILURE_MESSAGE,
                exception=str(ae),
            )
            raise VideoRegistryException(500, self.INTERNAL_SERVER_ERROR_MESSAGE)
        except Exception as e:
            logger.exception(
                QUERYING_FAILURE_MESSAGE,
                exception=str(e),
            )
            raise VideoRegistryException(500, self.INTERNAL_SERVER_ERROR_MESSAGE)
