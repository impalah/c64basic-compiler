import pytest
from c64basic_compiler.evaluate import (
    evaluate_expression,
    TypeMismatchError,
    EvaluationError,
)

# --- Expresiones válidas ---
valid_expressions = [
    "STR$(ABS(X * -1)) + CHR$(65)",
    'VAL("123") + 5',
    "RND(1) * 10 + 5",
    "INT(3.7 + RND(0))",
    "ABS(-99) + SGN(-5)",
    "SQR(16) + LOG(100)",
    "EXP(1) + 1",
    "SIN(3.14 / 2) + COS(0)",
    "TAN(1) + ATN(1)",
    "X * Y + Z / 2",
    "INT(SQR(81)) * 2",
    "STR$(RND(1) * 100)",
    "STR$(VAL(A$) + 1)",
    "LEN(A$) * 2 + 1",
    'CHR$(ASC("A") + 1)',
    "STR$(SGN(-42)) + STR$(INT(3.99))",
    "ABS(X - Y) + SQR(Z)",
    "RND(1) + SQR(LOG(1000))",
    "STR$(RND(0) * 50 + VAL(A$))",
    "VAL(STR$(65)) + 5",
    "STR$(LEN(A$) + SGN(-1))",
    "STR$(ABS(-1) + SQR(4))",
]

# --- Expresiones con error ---
invalid_expressions = [
    '"A" + 1',
    "STR$(ABS(X * -1) + CHR$(65))",
    "STR$(ABS(X * -1) + STR$(X))",
    "STR$(ABS(X * -1) + STR$(X) + 1)",
    "STR$(ABS(X * -1) + STR$(X) + 1.0)",
    "STR$(ABS(X * -1) + STR$(X) + 1.0 + 2)",
    "STR$(ABS(X * -1) + STR$(X) + 1.0 + 2.0)",
]


@pytest.mark.parametrize("expr", valid_expressions)
def test_valid_expressions(expr):
    try:
        result = evaluate_expression(expr)
        assert isinstance(result, list)
        assert all(isinstance(line, str) for line in result)
    except EvaluationError:
        pytest.fail(f"Expression raised EvaluationError unexpectedly: {expr}")


@pytest.mark.parametrize("expr", invalid_expressions)
def test_invalid_expressions(expr):
    with pytest.raises(TypeMismatchError):
        evaluate_expression(expr)
