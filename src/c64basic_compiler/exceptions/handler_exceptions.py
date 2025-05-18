class HandlerError(Exception):
    """Base exception class for instruction handler errors"""

    pass


class InvalidSyntaxError(HandlerError):
    """Exception raised when a BASIC command has invalid syntax"""

    pass


class EvaluationHandlerError(HandlerError):
    """Exception raised when expression evaluation fails within a handler"""

    pass


class CommandProcessingError(HandlerError):
    """Exception raised when processing a command fails for any other reason"""

    pass
