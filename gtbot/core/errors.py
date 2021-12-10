class GTException(Exception):
    """
    Base exception for GTbot-related errors.
    """

    pass


class NotFound(GTException):
    """
    The object you're looking for was not found.
    """

    pass
