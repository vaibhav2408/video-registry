import logging
import sys

from pydantic.error_wrappers import ValidationError
from structlog import get_logger

# Need to set log stream in addition to main since this executed before main.
# configure logging with filename, function name and line numbers
from app.utils import config_utils

"""
Setting the date format for log message
"""
date_str = "%I:%M:%S %p %Z"

"""
Setting up the format of the log message.
"""
fmt_str = "%(asctime)s: %(levelname)s: [%(threadName)-2.12s - %(filename)s:%(funcName)s::%(lineno)s]- %(message)s"

logging.basicConfig(
    level=logging.INFO,
    datefmt=date_str,
    format=fmt_str,
    stream=sys.stdout,
)

logger = get_logger()


class Settings:
    APP_NAME: str = "video-registry"

    DB_INIT_SUCCESS: bool = True

    google_api_key = None

    @property
    def elasticsearch_url(self):
        try:
            host = "elasticsearch"
            port = 9200
            protocol = "http"

            return f"{protocol}://{host}:{port}"
        except Exception as ex:
            raise ValueError(f"Exception while getting the ES Url : {str(ex)}")

    @property
    def elasticsearch_user(self):
        return ""

    @property
    def elasticsearch_password(self):
        return ""

    @property
    def elasticsearch_init_complete(self):
        return self.DB_INIT_SUCCESS

    @property
    def youtube_base_url(self):
        return "https://www.googleapis.com"

    @property
    def sleep_interval(self):
        return 10

    @property
    def video_query_string(self):
        return "football"

    @property
    def keys_file_path(self):
        return "/var/keys.txt"

    @property
    def api_keys(self):
        """
        Reads the api_keys from the file
        Args:
        Returns:
            the json content
        """
        logger.info("Reading API Keys from the file.")
        expected_data = config_utils.read_file(self.keys_file_path)
        return [data.strip() for data in expected_data]


try:
    settings = Settings()
except ValidationError as e:
    logger.exception(e)
    sys.exit(1)
