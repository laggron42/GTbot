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


class AlreadyPresent(GTException):
    """
    You're trying to assign someone to solething he is already assigned to.
    """

    pass
