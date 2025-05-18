# --- Custom Exceptions ---
class EvaluationError(Exception):
    pass


class MismatchedParenthesesError(EvaluationError):
    pass


class TypeMismatchError(EvaluationError):
    pass


class NotEnoughOperandsError(EvaluationError):
    pass


class ExpressionReduceError(EvaluationError):
    pass


class UnhandledTokenError(EvaluationError):
    pass
