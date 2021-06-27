from __future__ import annotations

import time
from datetime import datetime

import pytz
from structlog import get_logger

logger = get_logger()
"""
holds all the common_utils methods which are used by the endpoints
"""

RFC_339_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def get_epoch_millis():
    """
    returns the current epoch timestamp in milliseconds
    """
    return int(time.time() * 1000)


def string_unquote(value: str):
    """
    Method to unquote a string
    Args:
        value: the value to unquote
    Returns:
        unquoted string
    """
    if not isinstance(value, str):
        return value
    return value.replace('"', "").replace("'", "")


def get_published_after(date_format=RFC_339_DATE_FORMAT, timezone=pytz.utc):
    """
    Method to convert the epoch time to a given string format
    Params:
        epoch_time
        format
        timezone
    Return:
        formatted date string
    """
    # Checking for newly added videos since last 30 minutes
    epoch_time = round(time.time() - 1800)
    if not epoch_time:
        return None
    return datetime.fromtimestamp(epoch_time, timezone).strftime(date_format)


def multiple_args_to_single_dict(**kwargs):
    """
    This method stores all the arguments into a dict
    Args:
        kwargs: all the arguments to be stored in the dick
    Returns:
        A dict containing all arguments as key:value pairs
    """
    data = dict()
    for key, value in kwargs.items():
        data[key] = value

    return data
