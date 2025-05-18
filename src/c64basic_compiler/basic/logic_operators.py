from c64basic_compiler.basic.basic_function import BasicFunction, Type


class AndOperator(BasicFunction):
    """
    Implements the BASIC 'AND' binary operator.

    Performs a bitwise AND operation between two integer arguments.
    Each bit in the result is set if the corresponding bits in both
    operands are set.

    Args:
        First operand: Integer value
        Second operand: Integer value

    Returns:
        Integer result of the bitwise AND operation

    Examples:
        5 AND 3 = 1  (0101 AND 0011 = 0001)
        10 AND 7 = 2  (1010 AND 0111 = 0010)
    """

    name = "AND"
    arity = 2
    arg_types = [Type.INT, Type.INT]
    return_type = Type.INT


class OrOperator(BasicFunction):
    """
    Implements the BASIC 'OR' binary operator.

    Performs a bitwise OR operation between two integer arguments.
    Each bit in the result is set if at least one of the corresponding bits
    in either operand is set.

    Args:
        First operand: Integer value
        Second operand: Integer value

    Returns:
        Integer result of the bitwise OR operation

    Examples:
        5 OR 3 = 7  (0101 OR 0011 = 0111)
        10 OR 7 = 15  (1010 OR 0111 = 1111)
    """

    name = "OR"
    arity = 2
    arg_types = [Type.INT, Type.INT]
    return_type = Type.INT


class NotOperator(BasicFunction):
    """
    Implements the BASIC 'NOT' unary operator.

    Performs a bitwise NOT (complement) operation on an integer argument.
    Each bit in the result is inverted from the corresponding bit in the operand.
    In most BASIC implementations, this is a 16-bit operation.

    Args:
        Operand: Integer value to be complemented

    Returns:
        Integer result of the bitwise NOT operation

    Examples:
        NOT 5 = -6  (NOT 0000000000000101 = 1111111111111010, which is -6 in two's complement)
        NOT 0 = -1  (NOT 0000000000000000 = 1111111111111111)
    """

    name = "NOT"
    arity = 1
    arg_types = [Type.INT]
    return_type = Type.INT
