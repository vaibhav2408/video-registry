import requests
from starlette.status import HTTP_200_OK
from structlog import get_logger

from app.core.exception_handler.video_registry_exception import VideoRegistryException

logger = get_logger()


class BaseApiCaller:
    """
    The api client
    """

    INTERNAL_SERVER_ERROR_KEY = "Internal server error."

    base_url = None
    path = None
    params = None

    def __init__(self, base_url, path, params=None):
        self.base_url = base_url
        self.path = path
        self.params = params

    def get(self):
        url = f"{self.base_url}{self.path}"
        try:
            resp = requests.get(url=url, params=self.params)
            if resp.status_code == HTTP_200_OK:
                response = resp.json()
                return response
            elif 400 <= resp.status_code < 500:
                logger.exception(
                    "Get operation failed.",
                    status_code=resp.status_code,
                    path=self.path,
                    response=None,
                )
                return None
            else:
                logger.exception(
                    message="Get operation failed.",
                    url=url,
                    params=self.params,
                    status_code=resp.status_code,
                    content=resp.text,
                )
                raise VideoRegistryException(resp.status_code, resp.text)
        except requests.exceptions.ConnectTimeout as e:
            logger.exception(
                message="Connection timed out",
                url=url,
                params=self.params,
                exception=str(e),
            )
            raise VideoRegistryException(408, self.INTERNAL_SERVER_ERROR_KEY)
