class GTException(Exception):
    """
    Base exception for GTbot-related errors.
    """

    pass


class SilentError(GTException):
    """
    An error was already handled and should be silent,
    but still propagate and cancel the stack call.
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


class NotAllowed(GTException):
    """
    Someone is trying to perform an action he is not allowed to do.
    """
    pass
