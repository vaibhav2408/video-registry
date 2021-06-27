import logging

from elasticsearch_dsl.connections import connections
from structlog import get_logger

from app.core.config import settings

# Setting up logger
logger = get_logger()

es_conn = connections.create_connection(hosts=settings.elasticsearch_url, timeout=20)
logger.info(
    "Created elasticsearch connection.",
    endpoint_url=settings.elasticsearch_url,
)
logger.info("Elasticsearch init.", status=True)
es_logger = logging.getLogger("elasticsearch")
es_logger.setLevel(logging.ERROR)
