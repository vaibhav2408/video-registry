class VideoRegistryException(Exception):
    """base exception class."""

    def __init__(self, error_code, detail=None):
        Exception.__init__(self, error_code)
        self.error_code = error_code
        self.detail = detail
