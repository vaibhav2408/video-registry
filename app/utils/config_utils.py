"""Util for helping with the configs/files"""
import os

from fastapi import status
from structlog import get_logger

from app.core.exception_handler.video_registry_exception import VideoRegistryException

logger = get_logger()


def read_file(filepath) -> list:
    """
    Reads the yaml/text file and returns the content of the file
    :param filepath: the path of the config file
    :returns: file contents
    """
    try:
        if os.path.isfile(filepath):
            with open(filepath) as f:
                expected_data = f.readlines()
        else:
            logger.exception(
                f"Please check the file path & ensure that the correct path is given."
            )
            raise VideoRegistryException(500, "Internal server error.")
        return expected_data
    except Exception as ex:
        logger.exception(
            f"Exception while reading the file {filepath}", exceptiion=str(ex)
        )
        raise VideoRegistryException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )
