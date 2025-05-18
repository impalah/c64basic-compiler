from c64basic_compiler.basic.basic_function import BasicFunction, Type


class AddOperator(BasicFunction):
    """
    Implements the BASIC '+' addition operator.

    Performs addition between two operands. It can add:
    - Two numbers together
    - Two strings together (concatenation)

    Args:
        First operand: Number or string
        Second operand: Number or string (must be same type as first operand)

    Returns:
        Sum of two numbers or concatenation of two strings

    Examples:
        5 + 3 = 8
        "HELLO" + " WORLD" = "HELLO WORLD"
    """

    name = "+"
    arity = 2
    arg_types = [Type.ANY, Type.ANY]
    return_type = Type.ANY

    def is_type_compatible(self, args: list[Type]) -> bool:
        # Special case for addition which can handle strings or numbers
        if args == [Type.STR, Type.STR]:
            return True
        if all(t in (Type.NUM, Type.INT) for t in args):
            return True
        return False


class SubtractOperator(BasicFunction):
    """
    Implements the BASIC '-' subtraction operator.

    Performs subtraction between two numeric operands.

    Args:
        First operand: Numeric value (minuend)
        Second operand: Numeric value (subtrahend)

    Returns:
        Difference between the two numbers

    Examples:
        5 - 3 = 2
        10 - 15 = -5
    """

    name = "-"
    arity = 2
    arg_types = [Type.NUM, Type.NUM]
    return_type = Type.NUM


class MultiplyOperator(BasicFunction):
    """
    Implements the BASIC '*' multiplication operator.

    Performs multiplication between two numeric operands.

    Args:
        First operand: Numeric value
        Second operand: Numeric value

    Returns:
        Product of the two numbers

    Examples:
        5 * 3 = 15
        -2 * 4 = -8
    """

    name = "*"
    arity = 2
    arg_types = [Type.NUM, Type.NUM]
    return_type = Type.NUM


class DivideOperator(BasicFunction):
    """
    Implements the BASIC '/' division operator.

    Performs floating-point division between two numeric operands.

    Args:
        First operand: Numeric value (dividend)
        Second operand: Numeric value (divisor, non-zero)

    Returns:
        Quotient of the division

    Examples:
        10 / 2 = 5
        5 / 2 = 2.5
    """

    name = "/"
    arity = 2
    arg_types = [Type.NUM, Type.NUM]
    return_type = Type.NUM


class PowerOperator(BasicFunction):
    """
    Implements the BASIC '^' exponentiation operator.

    Raises the first operand to the power of the second operand.

    Args:
        First operand: Numeric value (base)
        Second operand: Numeric value (exponent)

    Returns:
        First operand raised to the power of the second operand

    Examples:
        2 ^ 3 = 8
        5 ^ 2 = 25
        2 ^ 0.5 = 1.414... (square root of 2)
    """

    name = "^"
    arity = 2
    arg_types = [Type.NUM, Type.NUM]
    return_type = Type.NUM
